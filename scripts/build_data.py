#!/usr/bin/env python3
"""Split the village data into per-room files for the static site.

Open sectors (content/site.json) are emitted in full: word cards, quizzes,
conversations and conjugation tables. Every other sector is summarized for
the map and marked coming soon. Verb lists are never hard-coded; street
segments are read from rooms.json, so a later correction of ST_cooking is
picked up on the next build.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotspots import normalize_scene

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
ART = ROOT / "content" / "art"
PUBLIC = ROOT / "public"
CACHE = ROOT / "data" / "cache" / "conjugations.json"

SECTOR_POS = {
    "S01_beginner": (46, 42),
    "S02_home": (20, 36),
    "S03_market": (33, 56),
    "S04_cafes": (56, 60),
    "S05_bank": (64, 78),
    "S06_townhall": (70, 36),
    "S07_health": (86, 42),
    "S08_travel": (90, 60),
    "S09_nature": (16, 64),
    "S10_university": (82, 80),
    "S11_church": (28, 18),
    "S12_faiths": (46, 14),
    "S13_museum": (64, 16),
    "S14_culture": (86, 16),
    "S15_feelings": (22, 82),
    "S16_park": (44, 86),
}

ALT_LABELS = {
    "faith_first": "Faith first",
    "traveller": "Traveller",
    "professional": "Professional",
    "family_day_out": "Family day out",
}

TENSE_PATHS = {
    "present": ("indicatif", "présent"),
    "passe": ("indicatif", "passé-composé"),
    "imparfait": ("indicatif", "imparfait"),
    "futur": ("indicatif", "futur-simple"),
    "conditionnel": ("conditionnel", "présent"),
    "imperatif": ("imperatif", "imperatif-présent"),
    "subjonctif": ("subjonctif", "présent"),
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def fold(text):
    text = unicodedata.normalize("NFD", text or "")
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", text.casefold())


def split_name(name):
    if " — " in name:
        french, english = name.split(" — ", 1)
        return french.strip(), english.strip()
    return name, ""


MISSING_FR = []


def bilingual_name(name):
    """Split 'French — English' or 'French (english)' when the source has both."""
    text = (name or "").strip()
    if " — " in text:
        french, english = text.split(" — ", 1)
        return french.strip(), english.strip()
    match = re.match(r"^(.*?)\s+\((.+)\)\s*$", text)
    if match and match.group(1).strip() and match.group(2).strip():
        return match.group(1).strip(), match.group(2).strip()
    return "", ""


def note_missing(kind, record_id, key):
    MISSING_FR.append(f"{kind} {record_id} {key}")


def locale_fields(record, kind, record_id, signs=None, log=True):
    """Copy name_fr / description_fr when present. Fall back later in the client."""
    name = (record.get("name") or "").strip()
    name_fr = (record.get("name_fr") or "").strip()
    name_en = (record.get("name_en") or "").strip()
    derived_fr, derived_en = bilingual_name(name)
    if not name_fr and derived_fr and derived_en:
        name_fr = derived_fr
    if not name_en and derived_en:
        name_en = derived_en
    if not name_fr and signs and signs.get(record_id):
        name_fr = signs[record_id]
    fields = {}
    if name_fr:
        fields["name_fr"] = name_fr
    elif name and log:
        note_missing(kind, record_id, "name_fr")
    if name_en:
        fields["name_en"] = name_en
    description = (record.get("description") or record.get("setting") or "").strip()
    description_fr = (record.get("description_fr") or record.get("setting_fr") or "").strip()
    if description:
        fields["description"] = description
    if description_fr:
        fields["description_fr"] = description_fr
    elif description and log:
        note_missing(kind, record_id, "description_fr")
    return fields


def report_missing_fr():
    if not MISSING_FR:
        print("French metadata: no missing name_fr or description_fr")
        return
    counts = {}
    for line in MISSING_FR:
        key = line.rsplit(" ", 1)[-1]
        counts[key] = counts.get(key, 0) + 1
    summary = ", ".join(f"{key} × {count}" for key, count in sorted(counts.items()))
    print(f"missing French metadata (English fallback): {summary}")
    for line in MISSING_FR[:40]:
        print(f"  {line}")
    extra = len(MISSING_FR) - 40
    if extra > 0:
        print(f"  … {extra} more")


def floor_of(room):
    if room.get("kind") == "zoom":
        return None
    name = room["name"].lower()
    if "[upstairs]" in name or re.search(r"\bupstairs\b", name):
        return 2, "Upstairs"
    if "first floor" in name and "ground" not in name:
        return 1, "First floor"
    if "ground" in name or "first floor" in name:
        return 0, "Ground floor"
    if room.get("kind") == "street_segment":
        return 0, "Along the street"
    return 0, "Ground floor"


def seg_index(room_id):
    match = re.search(r"seg(\d+)", room_id)
    return int(match.group(1)) if match else 0


def headword(word):
    article = (word.get("article") or "").replace("’", "'")
    lemma = word["lemma"]
    if article == "l'":
        return f"l'{lemma}"
    if article:
        return f"{article} {lemma}"
    if word["pos"] == "verb" and word.get("pronominal_form"):
        return clean_pronominal(word["pronominal_form"])
    return lemma


def clean_pronominal(form):
    text = form or ""
    while True:
        nxt = re.sub(r"\s*\([^)]*\)", "", text).strip()
        if nxt == text:
            return text
        text = nxt


def gloss_short(gloss):
    return (gloss or "").split(";")[0].split(",")[0].strip()


def explain_mnemonic(word):
    hook = word.get("mnemonic_hook") or {}
    sound = (hook.get("sound_alike") or "").strip()
    scene = (hook.get("scene") or "").strip()
    lemma = word["lemma"]
    resp = word.get("respelling") or ""
    display = word.get("display")
    said = f"“{lemma}”" + (f" ({resp})" if resp else "")
    if display == "museum_text":
        return (
            f"{said} is kept because you will meet it, and it is shown only as a text plaque — never as a drawing. "
            "Read the plaque, say the word once, and let the place on the wall hold it. "
            "The note beside it is there to warn you gently if the word needs care; it does not spell out a second, harsher meaning."
        )
    if display == "text_plain":
        parts = ["This one is remembered as text, not as a pictured object. The letters in their place are the memory."]
    elif word.get("cognate_type") == "true_cognate" or scene.lower().startswith("cognate:"):
        parts = [
            f"{said} already looks or sounds like its English cousin, so the meaning has a friend. "
            "The object is shown as itself, in its ordinary place, without an extra costume."
        ]
    elif hook.get("fallback") == "plain" or scene.lower().startswith("shown plainly"):
        parts = [f"{said} is pictured as itself, without a sound pun. Walk to its place and name it. The spot is the memory."]
    elif sound:
        parts = [
            f"The sound hook is “{sound}”. Say {said} and listen for that familiar sound inside the French word."
        ]
    else:
        parts = [f"Picture {said} standing in this exact spot. Coming back to the place is what brings the word back."]
    if scene and display == "drawn":
        parts.append(scene)
    elif scene and display != "museum_text":
        parts.append(scene)
    if sound and display == "drawn" and word.get("cognate_type") != "true_cognate":
        parts.append(
            "When you return, find the picture first. The sound hiding in it gives you the French word, and the place tells you the meaning."
        )
    if word.get("cognate_type") == "true_cognate":
        parts.append("A cognate can still surprise you: learn the gender, and check that the English sense is really the same one.")
    if hook.get("strength") == "weak":
        parts.append("This hook is a light one. Say the French word aloud while you look, so it has somewhere to stay.")
    return " ".join(parts)


# Sectors that name at least one id in open_rooms. Other open sectors stay fully walkable.
RESTRICTED_SECTORS = set()


def is_live(room, open_sectors, live_ids):
    if not room or room.get("sector_id") not in open_sectors:
        return False
    if room.get("sector_id") in RESTRICTED_SECTORS and room["id"] not in (live_ids or ()):
        return False
    return True


def direct_building_layers():
    """Sector paintings that open a building's rooms and skip its exterior page."""
    cached = getattr(direct_building_layers, "_cached", None)
    if cached is not None:
        return cached
    found = {}
    for path in ART.glob("*/hotspots.json"):
        raw = load_json(path)
        if not raw.get("no_building_layer"):
            continue
        building_id = str(raw.get("building_rooms_direct") or "").strip()
        if building_id:
            found[building_id] = path.parent.name
    direct_building_layers._cached = found
    return found


def retarget_direct_layers(scene, direct):
    """A door aimed at a skipped exterior opens the sector square instead."""
    if not scene or not direct:
        return scene

    def rewrite(item):
        target = item.get("target")
        if target in direct:
            item["target"] = direct[target]

    for link in scene.get("links") or []:
        rewrite(link)
    for exit_item in (scene.get("exits") or {}).values():
        if isinstance(exit_item, dict):
            rewrite(exit_item)
    return scene


def mark_soon_links(scene, rooms_by_id, buildings_by_id, sectors_by_id, open_sectors, live_ids):
    """Doors into a closed building stay visible and are not clickable."""
    if not scene:
        return scene
    retarget_direct_layers(scene, direct_building_layers())
    art_to_sector = {}
    for sector_id in sectors_by_id:
        art_to_sector[f"{sector_id.split('_')[0]}_sector"] = sector_id
    for link in scene.get("links") or []:
        target = link.get("target")
        if not target:
            continue
        soon = False
        if target in rooms_by_id:
            soon = not is_live(rooms_by_id[target], open_sectors, live_ids)
        elif target in buildings_by_id:
            building = buildings_by_id[target]
            owned = [rooms_by_id[rid] for rid in building.get("rooms") or [] if rid in rooms_by_id]
            soon = not any(is_live(room, open_sectors, live_ids) for room in owned)
        elif target in art_to_sector:
            soon = art_to_sector[target] not in open_sectors
        if soon:
            link["soon"] = True
    return scene


def link_lemmas(lemmas, by_lemma, rooms_by_id, open_sectors, live_ids=None):
    linked = []
    for lemma in lemmas or []:
        hits = by_lemma.get(lemma.casefold(), [])
        exact = [hit for hit in hits if hit["lemma"] == lemma] or hits
        if not exact:
            linked.append({"lemma": lemma})
            continue
        hit = exact[0]
        room = rooms_by_id.get(hit["room_id"])
        if not room:
            linked.append({"lemma": hit["lemma"], "id": hit["id"]})
            continue
        linked.append({
            "lemma": hit["lemma"],
            "id": hit["id"],
            "pos": hit["pos"],
            "room_id": hit["room_id"],
            "room_name": room["name"],
            "sector_id": room["sector_id"],
            "open": is_live(room, open_sectors, live_ids),
        })
    return linked


def card(word, by_lemma, rooms_by_id, open_sectors, conjugations, live_ids=None):
    hook = word.get("mnemonic_hook") or {}
    payload = {
        "id": word["id"],
        "lemma": word["lemma"],
        "pos": word["pos"],
        "gender": word.get("gender"),
        "article": word.get("article"),
        "head": headword(word),
        "plural_irregular": word.get("plural_irregular"),
        "gender_note": word.get("gender_note"),
        "gloss": word.get("gloss"),
        "ipa": word.get("ipa"),
        "respelling": word.get("respelling"),
        "cefr": word.get("cefr"),
        "side": word.get("side"),
        "display": word.get("display"),
        "hook": {
            "sound_alike": hook.get("sound_alike"),
            "scene": hook.get("scene"),
            "strength": hook.get("strength"),
            "fallback": hook.get("fallback"),
        },
        "mnemonic_explain": explain_mnemonic(word),
        "cognate_type": word.get("cognate_type") or "none",
        "false_cognate_note": word.get("false_cognate_note"),
        "related": link_lemmas(word.get("related"), by_lemma, rooms_by_id, open_sectors, live_ids),
        "opposites": link_lemmas(word.get("opposites"), by_lemma, rooms_by_id, open_sectors, live_ids),
        "usage_warning": word.get("usage_warning"),
        "example_fr": (word.get("example_fr") or "").strip() or None,
        "example_en": (word.get("example_en") or "").strip() or None,
        "literal": word.get("literal"),
        "register": word.get("register"),
        "letter_name": word.get("letter_name"),
        "wiktionary": str(word.get("gloss_source") or "").startswith("Wiktionary"),
    }
    if word["pos"] == "verb":
        infinitive = verb_infinitive(word)
        payload.update({
            "reflexive": bool(word.get("reflexive")),
            "pronominal_form": clean_pronominal(word.get("pronominal_form") or "") or None,
            "prepositions": word.get("prepositions") or [],
            "auxiliary": word.get("auxiliary"),
            "irregular": bool(word.get("irregular")),
            "conjugations": conjugations.get(infinitive),
        })
    return payload


def quiz_item(word):
    return {
        "id": word["id"],
        "lemma": word["lemma"],
        "pos": word["pos"],
        "gender": word.get("gender"),
        "article": word.get("article"),
        "gloss": gloss_short(word.get("gloss")),
        "ipa": word.get("ipa"),
        "respelling": word.get("respelling"),
        "head": headword(word),
    }


def dialogue_for(conv, words_by_id):
    """Hand-written dialogues only. Premise notes are not turned into a quiz script."""
    del words_by_id
    if conv.get("status") != "written":
        return None
    lines = []
    for line in conv.get("lines") or []:
        if not isinstance(line, dict):
            continue
        speaker = str(line.get("speaker") or "").strip()
        fr = str(line.get("fr") or "").strip()
        en = str(line.get("en") or "").strip()
        if speaker and fr:
            lines.append({"speaker": speaker, "fr": fr, "en": en})
    if not lines:
        return None
    return {
        "id": conv.get("id"),
        "title": conv.get("title") or "",
        "title_fr": (conv.get("title_fr") or "").strip(),
        "premise": conv.get("premise") or "",
        "premise_fr": (conv.get("premise_fr") or "").strip(),
        "lines": lines,
    }


def sign_text(room, building, signs):
    if room["id"] in signs:
        return signs[room["id"]]
    if room.get("kind") == "street_segment" and building:
        return building["name"]
    if room.get("furniture"):
        return room["furniture"]
    return room["name"]


def sector_art_id(sector_id):
    return f"{sector_id.split('_')[0]}_sector"


def load_place_scene(place_id, sign=None, plaque=None):
    path = ART / place_id / "hotspots.json"
    if not path.exists() or not (ART / place_id / "base.jpg").exists():
        return None
    scene = normalize_scene(load_json(path))
    scene["image"] = f"art/{place_id}/base.jpg"
    scene["placeholder"] = (ART / place_id / "placeholder.json").exists() or scene.get("placeholder")
    areas = scene.setdefault("text_areas", {})
    if sign:
        for key in ("sign", "street_sign"):
            if key in areas and not areas[key].get("text"):
                areas[key]["text"] = sign
    if plaque and "plaque" in areas and not areas["plaque"].get("text"):
        areas["plaque"]["text"] = plaque
    scene["sign_text"] = (areas.get("sign") or areas.get("street_sign") or {}).get("text") or sign or ""
    scene["plaque_text"] = (areas.get("plaque") or {}).get("text") or plaque or ""
    return scene


def bind_scene(room, words, building, signs, plaques=None):
    scene = load_place_scene(
        room["id"],
        sign_text(room, building, signs),
        (plaques or {}).get(room["id"]) or "",
    )
    if not scene:
        return None
    # Exits stay as painted: forward, back, and left or right when the picture has them.
    # A zoom with no way out gets a back step to its parent.
    if room.get("kind") == "zoom" and room.get("parent_room_id"):
        exits = scene.setdefault("exits", {})
        if not any(exits.get(key) for key in ("prev", "back")):
            exits["back"] = {
                "box": [24, 24, 120, 96],
                "target": room["parent_room_id"],
                "label": "Step back",
            }
    regions = list(scene.get("zoom_regions") or [])
    if not regions and scene.get("zoom_from"):
        regions = [scene["zoom_from"]]
    for zoom in regions:
        scene["hotspots"].insert(0, {
            "zoom_id": zoom["room_id"],
            "label": signs.get(zoom["room_id"]) or zoom.get("label") or "Look closer",
            "box": zoom["box"],
            "slug": "zoom",
        })
    by_slug = {}
    for word in words:
        by_slug[fold(word["lemma"])] = word["id"]
        by_slug[fold(word["id"])] = word["id"]
        by_slug[word["id"]] = word["id"]
    for hot in scene["hotspots"]:
        if hot.get("zoom_id") or hot.get("word_id"):
            continue
        if hot.get("mnemonic_for"):
            ref = hot["mnemonic_for"]
            match = next((item for item in scene["hotspots"] if item.get("slug") == ref and item.get("word_id")), None)
            if match:
                hot["word_id"] = match["word_id"]
            else:
                hot["word_id"] = by_slug.get(fold(ref))
        if not hot.get("word_id") and hot.get("slug"):
            hot["word_id"] = by_slug.get(fold(hot["slug"])) or by_slug.get(hot["slug"])
    for hot in scene["hotspots"]:
        # One clickable box per item. A mnemonic box widens that box; it is not a second target.
        extra = hot.get("mnemonic_box")
        if extra and hot.get("box"):
            box = hot["box"]
            hot["box"] = [
                min(box[0], extra[0]),
                min(box[1], extra[1]),
                max(box[2], extra[2]),
                max(box[3], extra[3]),
            ]
        hot.pop("mnemonic_box", None)
    extras = []
    for hot in list(scene["hotspots"]):
        if hot.get("mirror_box") and hot.get("word_id"):
            extras.append({
                "word_id": hot["word_id"],
                "helper": True,
                "mirror": True,
                "box": hot["mirror_box"],
                "side": hot.get("side"),
                "slug": (hot.get("slug") or "") + "-mirror",
            })
    scene["hotspots"].extend(extras)
    return scene


def neighbor_stub(sector_id, sectors_by_id, open_sectors):
    sector = sectors_by_id[sector_id]
    french, english = split_name(sector["name"])
    payload = {
        "id": sector_id,
        "name": sector["name"],
        "fr_name": french,
        "en_name": english,
        "open": sector_id in open_sectors,
    }
    payload.update(locale_fields(sector, "sector", sector_id, log=False))
    return payload


def chip_text(room):
    """Short switcher label. Street numbers come from the room record, not a fixed verb list."""
    if room.get("kind") == "street_segment":
        match = re.search(r"(?:segment|étape|etape)\s+(\d+)", room.get("name") or "", re.IGNORECASE)
        if match:
            return match.group(1)
        index = seg_index(room["id"])
        if index:
            return str(index)
    return ""


def ordered_building_rooms(building, rooms):
    rooms = [room for room in rooms if room.get("kind") != "zoom"]
    if building and building.get("type") == "verb_street":
        rooms.sort(key=lambda room: seg_index(room["id"]))
    else:
        rooms.sort(key=lambda room: (
            floor_of(room)[0] if floor_of(room) else 9,
            room.get("mean_level") or 0,
            room["id"],
        ))
    return rooms


def room_stub(room, signs, buildings, open_sectors, live_ids=None):
    floor = floor_of(room)
    building = buildings.get(room["building_id"])
    payload = {
        "id": room["id"],
        "name": room["name"],
        "kind": room["kind"],
        "type": room.get("type"),
        "sign": sign_text(room, building, signs),
        "chip": chip_text(room),
        "item_count": room.get("item_count"),
        "cefr_band": room.get("cefr_band"),
        "floor": None if floor is None else floor[0],
        "floor_label": None if floor is None else floor[1],
        "open": is_live(room, open_sectors, live_ids),
        "art": (ART / room["id"] / "hotspots.json").exists(),
        "parent_room_id": room.get("parent_room_id"),
        "furniture": room.get("furniture"),
    }
    payload.update(locale_fields(room, "room", room["id"], signs, log=False))
    return payload


def pack_positions(count):
    if count <= 0:
        return []
    cols = 1 if count == 1 else 2 if count <= 4 else 3
    rows = math_ceil(count / cols)
    positions = []
    for index in range(count):
        col = index % cols
        row = index // cols
        x = round((col + 1) / (cols + 1) * 100, 1)
        y = round((row + 1) / (rows + 1) * 100, 1)
        positions.append([x, y])
    return positions


def math_ceil(value):
    return int(value) if value == int(value) else int(value) + 1


# --- conjugations ----------------------------------------------------------

def verb_infinitive(word):
    if word.get("reflexive") and word.get("pronominal_form"):
        return clean_pronominal(word["pronominal_form"])
    return word["lemma"]


def _surface(items, pronoun, gender=None):
    pool = [item for item in items if item.get("pr") == pronoun]
    if gender:
        matched = [item for item in pool if item.get("g") == gender]
        if matched:
            pool = matched
    if not pool:
        return None
    forms = pool[0].get("c") or []
    return forms[0] if forms else None


def _collapse(masculine, feminine, left, right):
    if not masculine or not feminine or masculine == feminine:
        return masculine or feminine
    pairs = (
        (f"{left} ", f"{right} ", f"{left}/{right} "),
        (f"qu'{left} ", f"qu'{right} ", f"qu'{left}/{right} "),
        (f"que {left} ", f"que {right} ", f"que {left}/{right} "),
    )
    for source, target, label in pairs:
        if masculine.startswith(source):
            rest = masculine[len(source):]
            if feminine == target + rest:
                return label + rest
    return f"{masculine} / {feminine}"


def _person(items, pronoun):
    masculine = _surface(items, pronoun, "m") or _surface(items, pronoun)
    feminine = _surface(items, pronoun, "f")
    if masculine and feminine and masculine != feminine:
        return f"{masculine} / {feminine}"
    return masculine or feminine


def table_rows(items, imperative=False):
    if not items:
        return None
    if imperative:
        return [form for form in (_surface(items, pronoun) for pronoun in ("tu", "nous", "vous")) if form]
    third = _collapse(_surface(items, "il") or _surface(items, "il", "m"), _surface(items, "elle") or _surface(items, "elle", "f"), "il", "elle")
    plural = _collapse(_surface(items, "ils") or _surface(items, "ils", "m"), _surface(items, "elles") or _surface(items, "elles", "f"), "ils", "elles")
    rows = [
        _person(items, "je"),
        _person(items, "tu"),
        third,
        _person(items, "nous"),
        _person(items, "vous"),
        plural,
    ]
    if not any(rows):
        return None
    return rows


def _bare_participle(form):
    if form and str(form).startswith("étant "):
        return str(form)[len("étant "):]
    return form


def _participle(items, gender=None, number=None):
    pool = list(items or [])
    if gender:
        matched = [item for item in pool if item.get("g") == gender]
        if matched:
            pool = matched
    if number:
        matched = [item for item in pool if item.get("n") == number]
        if matched:
            pool = matched
    if not pool:
        return None
    forms = pool[0].get("c") or []
    return _bare_participle(forms[0] if forms else None)


def extract_tables(payload):
    moods = payload.get("moods") or {}
    tables = {}
    for key, (mood, tense) in TENSE_PATHS.items():
        items = ((moods.get(mood) or {}).get(tense)) or []
        rows = table_rows(items, imperative=(key == "imperatif"))
        if rows:
            tables[key] = rows
    part = moods.get("participe") or {}
    passe = _participle(part.get("participe-passé"), "m", "s")
    passe_f = _participle(part.get("participe-passé"), "f", "s")
    present = _participle(part.get("participe-présent"))
    if passe:
        tables["participe_passe"] = passe
    if passe_f and passe_f != passe:
        tables["participe_passe_f"] = passe_f
    if present:
        tables["participe_present"] = present
    return tables or None


def load_cache():
    if CACHE.exists():
        return load_json(CACHE)
    return {}


def save_cache(cache):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def conjugate_missing(infinitives, cache):
    missing = [item for item in infinitives if item and item not in cache]
    if not missing:
        return cache
    logging.disable(logging.CRITICAL)
    try:
        from verbecc import CompleteConjugator
    except ImportError as exc:
        raise SystemExit(
            "Some verbs have no cached conjugation and verbecc is not installed. "
            "pip install -r scripts/requirements.txt and rerun."
        ) from exc
    conjugator = CompleteConjugator("fr")
    failed = []
    for infinitive in missing:
        try:
            payload = json.loads(conjugator.conjugate(infinitive).to_json())
            tables = extract_tables(payload)
            if tables:
                cache[infinitive] = tables
            else:
                failed.append(infinitive)
        except Exception:
            failed.append(infinitive)
    save_cache(cache)
    if failed:
        print(f"conjugation unavailable for {len(failed)} verbs, e.g. {failed[:8]}")
    return cache


def refresh_participles(cache):
    """Older cache rows stored the seven tenses only. Fill participles when verbecc is here."""
    stale = [
        key for key, value in cache.items()
        if isinstance(value, dict) and value.get("present") and "participe_passe" not in value
    ]
    if not stale:
        return cache
    logging.disable(logging.CRITICAL)
    try:
        from verbecc import CompleteConjugator
    except ImportError:
        print(f"participles missing for {len(stale)} verbs; verbecc is not installed, so the cache was left as it is")
        return cache
    conjugator = CompleteConjugator("fr")
    updated = 0
    for infinitive in stale:
        try:
            payload = json.loads(conjugator.conjugate(infinitive).to_json())
            tables = extract_tables(payload)
            if tables:
                cache[infinitive] = tables
                updated += 1
        except Exception:
            continue
    if updated:
        save_cache(cache)
        print(f"stored participles for {updated} verbs")
    return cache


# --- emit ------------------------------------------------------------------

def building_payload(building, rooms_by_id, signs, open_sectors, live_ids=None):
    rooms = ordered_building_rooms(
        building,
        [rooms_by_id[rid] for rid in building.get("rooms") or [] if rid in rooms_by_id],
    )
    floors = []
    if building["type"] == "verb_street":
        floors.append({
            "level": 0,
            "label": "Along the street",
            "rooms": [room_stub(room, signs, {building["id"]: building}, open_sectors, live_ids) for room in rooms],
        })
    else:
        grouped = defaultdict(list)
        labels = {}
        for room in rooms:
            if room.get("kind") == "zoom":
                continue
            level, label = floor_of(room)
            grouped[level].append(room)
            labels[level] = label
        for level in sorted(grouped):
            floors.append({
                "level": level,
                "label": labels[level],
                "rooms": [room_stub(room, signs, {building["id"]: building}, open_sectors, live_ids) for room in grouped[level]],
            })
    positions = pack_positions(len(floors))
    payload = {
        "id": building["id"],
        "name": building["name"],
        "type": building["type"],
        "sector_id": building["sector_id"],
        "architectural_theme": building.get("architectural_theme"),
        "meaning_group": building.get("meaning_group"),
        "verb_count": sum(len(room.get("words") or []) for room in rooms) or building.get("verb_count"),
        "floors": floors,
        "x": positions[0][0] if False else None,
    }
    payload.update(locale_fields(building, "building", building["id"], signs, log=False))
    return payload


def main():
    site = load_json(ROOT / "content" / "site.json")
    signs = load_json(ROOT / "content" / "signs.json")
    plaques_path = ROOT / "content" / "plaques.json"
    plaques = load_json(plaques_path) if plaques_path.exists() else {}
    assignment_path = ROOT / "content" / "assignment.json"
    assignment = load_json(assignment_path) if assignment_path.exists() else {}
    open_sectors = set(site.get("open_sectors") or [])
    # Rooms listed here limit their own sector. A sector with no listed room stays fully open.
    live_ids = set(site.get("open_rooms") or [])
    words = []
    with (SOURCE / "vocab.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            words.append(json.loads(line))
    words_by_id = {word["id"]: word for word in words}
    overlay = ROOT / "content" / "vocab"
    if overlay.exists():
        for path in sorted(overlay.glob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    word = json.loads(line)
                    words_by_id[word["id"]] = word
    by_lemma = defaultdict(list)
    for word in words_by_id.values():
        by_lemma[word["lemma"].casefold()].append(word)
    rooms = load_json(SOURCE / "rooms.json")["rooms"]
    rooms_by_id = {room["id"]: room for room in rooms}
    global RESTRICTED_SECTORS
    RESTRICTED_SECTORS = {room["sector_id"] for room in rooms if room["id"] in live_ids}
    buildings = load_json(SOURCE / "buildings.json")["buildings"]
    buildings_by_id = {building["id"]: building for building in buildings}
    sectors = load_json(SOURCE / "sectors.json")["sectors"]
    sectors_by_id = {sector["id"]: sector for sector in sectors}
    world = load_json(SOURCE / "map.json")
    prayers = load_json(SOURCE / "prayers.json")["prayers"]
    conversations = load_json(SOURCE / "conversations.json")["conversations"]
    conv_by_room = defaultdict(list)
    for conv in conversations:
        conv_by_room[conv["room_id"]].append(conv)

    for sector in sectors:
        locale_fields(sector, "sector", sector["id"], signs)
    for building in buildings:
        locale_fields(building, "building", building["id"], signs)
    for room in rooms:
        locale_fields(room, "room", room["id"], signs)

    route = world["suggested_route"]
    route_index = {step["sector_id"]: step for step in route}

    open_rooms = [room for room in rooms if room["sector_id"] in open_sectors]
    infinitives = []
    for room in open_rooms:
        for word_id in room["words"]:
            word = words_by_id.get(word_id)
            if word and word["pos"] == "verb":
                infinitives.append(verb_infinitive(word))
    cache = refresh_participles(conjugate_missing(sorted(set(infinitives)), load_cache()))

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC / "data", ignore_errors=True)
        shutil.rmtree(PUBLIC / "art", ignore_errors=True)
    (PUBLIC / "data" / "rooms").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "data" / "sectors").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "data" / "quiz" / "room").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "data" / "quiz" / "sector").mkdir(parents=True, exist_ok=True)

    def copy_art(room_id):
        source = ART / room_id
        if not (source / "base.jpg").exists():
            return False
        target = PUBLIC / "art" / room_id
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / "base.jpg", target / "base.jpg")
        return True

    sector_payloads = {}
    index_sectors = []
    index_buildings = []

    for sector in sectors:
        french, english = split_name(sector["name"])
        x, y = SECTOR_POS.get(sector["id"], (50, 50))
        open_now = sector["id"] in open_sectors
        order = route_index.get(sector["id"], {}).get("order")
        building_payloads = []
        walk = []
        for key in ("buildings", "streets"):
            for building_id in sector.get(key) or []:
                building = buildings_by_id[building_id]
                payload = building_payload(building, rooms_by_id, signs, open_sectors, live_ids)
                building_payloads.append(payload)
                index_building = {
                    "id": building["id"],
                    "name": building["name"],
                    "type": building["type"],
                    "sector_id": sector["id"],
                }
                if building["id"] in direct_building_layers():
                    index_building["no_building_layer"] = True
                    payload["no_building_layer"] = True
                index_building.update(locale_fields(building, "building", building["id"], signs, log=False))
                index_buildings.append(index_building)
                # The square opens these rooms. The exterior page is not a step.
                exterior = None
                if building["id"] not in direct_building_layers():
                    exterior = load_place_scene(building["id"], signs.get(building["id"]) or building["name"])
                if exterior:
                    payload["scene"] = mark_soon_links(
                        exterior, rooms_by_id, buildings_by_id, sectors_by_id, open_sectors, live_ids,
                    )
                    copy_art(building["id"])
                for floor in payload["floors"]:
                    for stub in floor["rooms"]:
                        # Alleys are chosen from the square. They are not steps on the walk.
                        if stub["kind"] not in {"zoom", "street_segment"} and stub.get("open"):
                            walk.append(stub["id"])
        # Stable positions inside the sector plan, buildings then the street.
        positions = pack_positions(len(building_payloads))
        for payload, position in zip(building_payloads, positions):
            payload["x"], payload["y"] = position
        prev_sector = next_sector = None
        if order:
            if order > 1:
                prev_id = route[order - 2]["sector_id"]
                prev_sector = neighbor_stub(prev_id, sectors_by_id, open_sectors)
            if order < len(route):
                next_id = route[order]["sector_id"]
                next_sector = neighbor_stub(next_id, sectors_by_id, open_sectors)
        sector_payload = {
            "id": sector["id"],
            "name": sector["name"],
            "fr_name": french,
            "en_name": english,
            "description": sector["description"],
            "entry_level": sector["entry_level"],
            "word_count": sector["word_count"],
            "cefr_counts": sector.get("cefr_counts"),
            "open": open_now,
            "x": x,
            "y": y,
            "order": order,
            "route_note": (route_index.get(sector["id"]) or {}).get("note") or "",
            "neighbors": [neighbor_stub(item, sectors_by_id, open_sectors) for item in sector.get("adjacent_sectors") or []],
            "prev_sector": prev_sector,
            "next_sector": next_sector,
            "buildings": building_payloads,
            "walk": walk,
            "scene": None,
            "alleys": [],
        }
        sector_payload.update(locale_fields(sector, "sector", sector["id"], signs, log=False))
        if open_now:
            sector_scene = load_place_scene(sector_art_id(sector["id"]), signs.get(sector_art_id(sector["id"])) or french)
            if sector_scene:
                sector_payload["scene"] = mark_soon_links(
                    sector_scene, rooms_by_id, buildings_by_id, sectors_by_id, open_sectors, live_ids,
                )
                copy_art(sector_art_id(sector["id"]))
            alleys = []
            for building in building_payloads:
                if building["type"] != "verb_street":
                    continue
                for floor in building["floors"]:
                    for stub in floor["rooms"]:
                        source = rooms_by_id.get(stub["id"]) or {}
                        verbs = []
                        for word_id in source.get("words") or []:
                            word = words_by_id.get(word_id)
                            if word:
                                verbs.append(word["lemma"])
                        alleys.append({
                            "id": stub["id"],
                            "chip": stub.get("chip") or "",
                            "verbs": verbs,
                            "name": stub["name"],
                        })
            sector_payload["alleys"] = alleys
        sector_payloads[sector["id"]] = sector_payload
        write_json(PUBLIC / "data" / "sectors" / f"{sector['id']}.json", sector_payload)
        index_sector = {
            "id": sector["id"],
            "name": sector["name"],
            "fr_name": french,
            "en_name": english,
            "description": sector["description"],
            "entry_level": sector["entry_level"],
            "word_count": sector["word_count"],
            "open": open_now,
            "x": x,
            "y": y,
            "order": order,
        }
        index_sector.update(locale_fields(sector, "sector", sector["id"], signs, log=False))
        index_sectors.append(index_sector)

    prayers_by_id = {prayer["id"]: prayer for prayer in prayers}
    rooms_emitted = 0
    for sector_id, sector_payload in sector_payloads.items():
        if sector_id not in open_sectors:
            continue
        quiz_items = []
        seen = set()
        walk = sector_payload["walk"]
        walk_pos = {room_id: index for index, room_id in enumerate(walk)}
        sector_rooms = [room for room in rooms if room["sector_id"] == sector_id]
        for room in sector_rooms:
            if not is_live(room, open_sectors, live_ids):
                continue
            building = buildings_by_id.get(room["building_id"])
            word_ids = list(room.get("words") or [])
            for word_id in assignment.get(room["id"]) or []:
                if word_id not in word_ids:
                    word_ids.append(word_id)
            room_words = [words_by_id[word_id] for word_id in word_ids if word_id in words_by_id]
            cards = [card(word, by_lemma, rooms_by_id, open_sectors, cache, live_ids) for word in room_words]
            scene = mark_soon_links(
                bind_scene(room, room_words, building, signs, plaques),
                rooms_by_id, buildings_by_id, sectors_by_id, open_sectors, live_ids,
            )
            painted_ids = {
                hot.get("word_id")
                for hot in (scene or {}).get("hotspots") or []
                if hot.get("word_id") and not hot.get("helper") and not hot.get("zoom_id")
            }
            for item in cards:
                item["painted"] = item["id"] in painted_ids
            copy_art(room["id"])
            floor = floor_of(room)
            parent = rooms_by_id.get(room.get("parent_room_id") or "")
            zooms = []
            for zoom_id in room.get("zoom_ids") or []:
                zoom = rooms_by_id.get(zoom_id)
                if zoom:
                    zooms.append({
                        "id": zoom["id"],
                        "name": zoom["name"],
                        "sign": sign_text(zoom, building, signs),
                        "furniture": zoom.get("furniture"),
                        "position": zoom.get("position"),
                        "item_count": zoom.get("item_count"),
                    })
            # Floor switcher follows the same order as the building page.
            siblings = ordered_building_rooms(
                building,
                [other for other in sector_rooms if other["building_id"] == room["building_id"]],
            )
            floors = []
            grouped = defaultdict(list)
            labels = {}
            for other in siblings:
                level, label = floor_of(other)
                grouped[level].append(other)
                labels[level] = label
            for level in sorted(grouped):
                floors.append({
                    "level": level,
                    "label": labels[level],
                    "rooms": [{
                        "id": other["id"],
                        "name": other["name"],
                        "kind": other["kind"],
                        "sign": sign_text(other, building, signs),
                        "chip": chip_text(other),
                        "open": is_live(other, open_sectors, live_ids),
                        "current": other["id"] == room["id"],
                    } for other in grouped[level]],
                })
            related = []
            for related_id in room.get("related_rooms") or []:
                other = rooms_by_id.get(related_id)
                if not other:
                    continue
                # Alleys are picked from the square. They do not point at each other.
                if room.get("kind") == "street_segment" and other.get("kind") == "street_segment":
                    continue
                other_sector = sectors_by_id[other["sector_id"]]
                related_item = {
                    "id": other["id"],
                    "name": other["name"],
                    "sign": sign_text(other, buildings_by_id.get(other["building_id"]), signs),
                    "sector_id": other["sector_id"],
                    "sector_name": split_name(other_sector["name"])[0],
                    "open": is_live(other, open_sectors, live_ids),
                }
                related_item.update(locale_fields(other, "room", other["id"], signs, log=False))
                related.append(related_item)
            prev_room = next_room = None
            if room["id"] in walk_pos and room.get("kind") != "zoom":
                index = walk_pos[room["id"]]
                if index > 0:
                    prev_room = _nav_room(walk[index - 1], rooms_by_id, buildings_by_id, signs)
                if index + 1 < len(walk):
                    next_room = _nav_room(walk[index + 1], rooms_by_id, buildings_by_id, signs)
            convs = [
                item for item in (
                    dialogue_for(conv, words_by_id) for conv in conv_by_room.get(room["id"], [])
                ) if item
            ]
            for conv in convs:
                if conv.get("premise") and not conv.get("premise_fr"):
                    note_missing("conversation", conv.get("id") or room["id"], "premise_fr")
                if conv.get("title") and not conv.get("title_fr"):
                    note_missing("conversation", conv.get("id") or room["id"], "title_fr")
            room_prayers = []
            for prayer_id in room.get("prayers") or []:
                prayer = prayers_by_id.get(prayer_id)
                if prayer:
                    room_prayers.append({"id": prayer["id"], "title_fr": prayer["title_fr"], "title_en": prayer["title_en"]})
            payload = {
                "id": room["id"],
                "name": room["name"],
                "sign": sign_text(room, building, signs),
                "setting": room.get("setting"),
                "kind": room["kind"],
                "type": room.get("type"),
                "sector_id": room["sector_id"],
                "sector_name": split_name(sectors_by_id[room["sector_id"]]["name"])[0],
                "building_id": room["building_id"],
                **({"no_building_layer": True} if room["building_id"] in direct_building_layers() else {}),
                "building_name": building["name"] if building else "",
                "building_type": building["type"] if building else "",
                "architectural_theme": building.get("architectural_theme") if building else None,
                "floor": None if floor is None else floor[0],
                "floor_label": None if floor is None else floor[1],
                "cefr_band": room.get("cefr_band"),
                "open": True,
                "parent": None if not parent else {
                    "id": parent["id"],
                    "name": parent["name"],
                    "sign": sign_text(parent, building, signs),
                    # Keep an explicit French sign. Do not split "Name (detail)" into a fake translation.
                    **({"name_fr": parent["name_fr"]} if parent.get("name_fr") else {}),
                    **({"name_en": parent["name_en"]} if parent.get("name_en") else {}),
                },
                "zooms": zooms,
                "floors": floors,
                "related": related,
                "prev": prev_room,
                "next": next_room,
                "prev_sector": sector_payloads[sector_id]["prev_sector"],
                "next_sector": sector_payloads[sector_id]["next_sector"],
                "prayers": room_prayers,
                "grammar_rules": room.get("grammar_rules") or [],
                "conversation": convs[0] if convs else None,
                "scene": scene,
                "words": cards,
            }
            payload.update(locale_fields(room, "room", room["id"], signs, log=False))
            write_json(PUBLIC / "data" / "rooms" / f"{room['id']}.json", payload)
            write_json(PUBLIC / "data" / "quiz" / "room" / f"{room['id']}.json", {
                "scope": "room",
                "id": room["id"],
                "title": sign_text(room, building, signs),
                "items": [quiz_item(word) for word in room_words],
            })
            for word in room_words:
                if word["id"] not in seen:
                    seen.add(word["id"])
                    quiz_items.append(quiz_item(word))
            rooms_emitted += 1
        write_json(PUBLIC / "data" / "quiz" / "sector" / f"{sector_id}.json", {
            "scope": "sector",
            "id": sector_id,
            "title": sector_payloads[sector_id]["fr_name"],
            "items": quiz_items,
        })

    write_json(PUBLIC / "data" / "prayers.json", {"prayers": prayers})
    shutil.copy2(SOURCE / "CREDITS.md", PUBLIC / "data" / "credits.md")
    featured = None
    if len(live_ids) == 1:
        featured_id = sorted(live_ids)[0]
        featured_room = rooms_by_id.get(featured_id)
        featured_building = buildings_by_id.get(featured_room["building_id"]) if featured_room else None
        if featured_room:
            featured = {
                "id": featured_id,
                "sign": sign_text(featured_room, featured_building, signs),
                "building": featured_building["name"] if featured_building else "",
                "sector_id": featured_room["sector_id"],
                "kind": "room",
            }
    elif "S01_beginner" in open_sectors:
        featured = {"id": "S01_beginner", "sign": "Place du Village", "kind": "sector"}
    elif "S04_cafes" in open_sectors:
        featured = {"id": "S04_cafes", "sign": signs.get("S04_sector") or "Rue des Saveurs", "kind": "sector"}
    write_json(PUBLIC / "data" / "index.json", {
        "title": site.get("title") or "Memory Village",
        "tagline": site.get("tagline") or "",
        "start": world.get("start"),
        "start_room": world.get("start_room"),
        "open_sectors": sorted(open_sectors),
        "open_rooms": sorted(live_ids),
        "featured": featured,
        "sectors": index_sectors,
        "buildings": index_buildings,
        "route": route,
        "route_legs": world.get("route_legs") or [],
        "alternatives": [
            {"id": key, "label": ALT_LABELS.get(key, key), "sectors": steps}
            for key, steps in (world.get("alternative_routes") or {}).items()
        ],
        "adjacency": world.get("adjacency"),
        "prayers": [{"id": prayer["id"], "title_fr": prayer["title_fr"], "title_en": prayer["title_en"]} for prayer in prayers],
        "counts": {"words": len(words), "rooms": len(rooms), "sectors": len(sectors)},
    })
    shutil.copy2(ROOT / "data" / "i18n.json", PUBLIC / "data" / "i18n.json")
    shutil.copy2(ROOT / "data" / "guide.json", PUBLIC / "data" / "guide.json")
    report_missing_fr()
    digest = hashlib.sha1(json.dumps(sorted(open_sectors)).encode()).hexdigest()[:8]
    print(f"emitted {rooms_emitted} open rooms; index {digest}")


def _nav_room(room_id, rooms_by_id, buildings_by_id, signs):
    room = rooms_by_id[room_id]
    building = buildings_by_id.get(room["building_id"])
    payload = {
        "id": room["id"],
        "name": room["name"],
        "sign": sign_text(room, building, signs),
        "chip": chip_text(room),
        "kind": room["kind"],
        "open": True,
    }
    payload.update(locale_fields(room, "room", room["id"], signs, log=False))
    return payload


if __name__ == "__main__":
    main()

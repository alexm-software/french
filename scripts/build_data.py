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


def is_live(room, open_sectors, live_ids):
    if not room or room.get("sector_id") not in open_sectors:
        return False
    if live_ids and room["id"] not in live_ids:
        return False
    return True


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
    words = [words_by_id[i] for i in conv.get("target_words") or [] if i in words_by_id][:8]
    lines = [{
        "speaker": "Inès",
        "fr": "On est bien ici. On revoit les mots de cet endroit ?",
        "en": "This is a good spot. Shall we go over the words that live here?",
    }]
    speakers = ("Marc", "Inès")
    for index, word in enumerate(words):
        ask, answer = speakers[index % 2], speakers[(index + 1) % 2]
        head = headword(word)
        english = gloss_short(word.get("gloss"))
        if word["pos"] == "verb":
            lines.append({"speaker": ask, "fr": f"Tu connais le verbe « {head} » ?", "en": f"Do you know the verb “{head}”?"})
            lines.append({"speaker": answer, "fr": f"Oui. « {head} » veut dire « {english} ».", "en": f"Yes. “{head}” means “{english}”."})
        elif word["pos"] == "noun":
            lines.append({"speaker": ask, "fr": f"Tu vois {head} ?", "en": f"Do you see {head}?"})
            lines.append({"speaker": answer, "fr": f"Oui, {head}. En anglais : « {english} ».", "en": f"Yes, {head}. In English: “{english}”."})
        else:
            lines.append({"speaker": ask, "fr": f"Et « {word['lemma']} » ?", "en": f"And “{word['lemma']}”?"})
            lines.append({"speaker": answer, "fr": f"Ça veut dire « {english} ».", "en": f"That means “{english}”."})
    lines.append({
        "speaker": "Inès",
        "fr": "On les laisse à leur place. La prochaine fois, l'endroit nous les rendra.",
        "en": "We'll leave them in their places. Next time, the place will give them back.",
    })
    return {
        "id": conv["id"],
        "title": conv.get("title"),
        "premise": conv.get("premise"),
        "generated": conv.get("status") == "premise_only",
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


def bind_scene(room, words, building, signs, plaques=None):
    path = ART / room["id"] / "hotspots.json"
    if not path.exists():
        return None
    scene = normalize_scene(load_json(path))
    scene["image"] = f"art/{room['id']}/{Path(scene['image']).name}"
    scene["placeholder"] = (ART / room["id"] / "placeholder.json").exists() or scene.get("placeholder")
    scene["sign_text"] = sign_text(room, building, signs)
    plaque = (scene.get("text_areas") or {}).get("plaque") or {}
    scene["plaque_text"] = plaque.get("text") or (plaques or {}).get(room["id"]) or ""
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
    extras = []
    for hot in list(scene["hotspots"]):
        if hot.get("mnemonic_box") and hot.get("word_id"):
            extras.append({
                "word_id": hot["word_id"],
                "helper": True,
                "box": hot["mnemonic_box"],
                "side": hot.get("side"),
                "slug": (hot.get("slug") or "") + "-helper",
            })
    scene["hotspots"].extend(extras)
    return scene


def neighbor_stub(sector_id, sectors_by_id, open_sectors):
    sector = sectors_by_id[sector_id]
    french, english = split_name(sector["name"])
    return {
        "id": sector_id,
        "name": sector["name"],
        "fr_name": french,
        "en_name": english,
        "open": sector_id in open_sectors,
    }


def chip_text(room):
    """Short switcher label. Street numbers come from the room record, not a fixed verb list."""
    if room.get("kind") == "street_segment":
        match = re.search(r"segment\s+(\d+)", room.get("name") or "", re.IGNORECASE)
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
    return {
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


def extract_tables(payload):
    moods = payload.get("moods") or {}
    tables = {}
    for key, (mood, tense) in TENSE_PATHS.items():
        items = ((moods.get(mood) or {}).get(tense)) or []
        rows = table_rows(items, imperative=(key == "imperatif"))
        if rows:
            tables[key] = rows
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
    return {
        "id": building["id"],
        "name": building["name"],
        "type": building["type"],
        "sector_id": building["sector_id"],
        "architectural_theme": building.get("architectural_theme"),
        "meaning_group": building.get("meaning_group"),
        "verb_count": building.get("verb_count"),
        "floors": floors,
        "x": positions[0][0] if False else None,
    }


def main():
    site = load_json(ROOT / "content" / "site.json")
    signs = load_json(ROOT / "content" / "signs.json")
    plaques_path = ROOT / "content" / "plaques.json"
    plaques = load_json(plaques_path) if plaques_path.exists() else {}
    open_sectors = set(site.get("open_sectors") or [])
    # When set, only these rooms are walkable. Everything else in the quarter stays coming soon.
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

    route = world["suggested_route"]
    route_index = {step["sector_id"]: step for step in route}

    open_rooms = [room for room in rooms if room["sector_id"] in open_sectors]
    infinitives = []
    for room in open_rooms:
        for word_id in room["words"]:
            word = words_by_id.get(word_id)
            if word and word["pos"] == "verb":
                infinitives.append(verb_infinitive(word))
    cache = conjugate_missing(sorted(set(infinitives)), load_cache())

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
                index_buildings.append({
                    "id": building["id"],
                    "name": building["name"],
                    "type": building["type"],
                    "sector_id": sector["id"],
                })
                for floor in payload["floors"]:
                    for stub in floor["rooms"]:
                        if stub["kind"] != "zoom" and stub.get("open"):
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
        }
        sector_payloads[sector["id"]] = sector_payload
        write_json(PUBLIC / "data" / "sectors" / f"{sector['id']}.json", sector_payload)
        index_sectors.append({
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
        })

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
            room_words = [words_by_id[word_id] for word_id in room["words"] if word_id in words_by_id]
            cards = [card(word, by_lemma, rooms_by_id, open_sectors, cache, live_ids) for word in room_words]
            scene = bind_scene(room, room_words, building, signs, plaques)
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
                other_sector = sectors_by_id[other["sector_id"]]
                related.append({
                    "id": other["id"],
                    "name": other["name"],
                    "sign": sign_text(other, buildings_by_id.get(other["building_id"]), signs),
                    "sector_id": other["sector_id"],
                    "sector_name": split_name(other_sector["name"])[0],
                    "open": is_live(other, open_sectors, live_ids),
                })
            prev_room = next_room = None
            if room["id"] in walk_pos and room.get("kind") != "zoom":
                index = walk_pos[room["id"]]
                if index > 0:
                    prev_room = _nav_room(walk[index - 1], rooms_by_id, buildings_by_id, signs)
                if index + 1 < len(walk):
                    next_room = _nav_room(walk[index + 1], rooms_by_id, buildings_by_id, signs)
            convs = [dialogue_for(conv, words_by_id) for conv in conv_by_room.get(room["id"], [])]
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
            }
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
    digest = hashlib.sha1(json.dumps(sorted(open_sectors)).encode()).hexdigest()[:8]
    print(f"emitted {rooms_emitted} open rooms; index {digest}")


def _nav_room(room_id, rooms_by_id, buildings_by_id, signs):
    room = rooms_by_id[room_id]
    building = buildings_by_id.get(room["building_id"])
    return {
        "id": room["id"],
        "name": room["name"],
        "sign": sign_text(room, building, signs),
        "chip": chip_text(room),
        "kind": room["kind"],
        "open": True,
    }


if __name__ == "__main__":
    main()

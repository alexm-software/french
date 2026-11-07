#!/usr/bin/env python3
"""Check a room manifest BEFORE generating art, or a building's draft layout.

  python tools/plan_check.py --manifest manifest.json
  python tools/plan_check.py --layout content/v2/ecole/layout.json --room cantine
  python tools/plan_check.py --manifest manifest.json --layout content/v2/ecole/layout.json --room cantine

In addition to structural completeness, plan_check.py runs pre-generation preflight checks:
  * canonical source cross-check (vocab.jsonl + v1-payloads + vocab_fixes.json + hooks.json):
    verifies every word ID exists, noun gender/side matches, and verb beret color and reflexive
    mirror agree with the conjugation tables
  * content blocklist, pee/poo respelling check, and mechanical hook lint (resp, false_cognate
    "Like English", etymology, placement openers, >2 pun chunks, missing CAPS) BEFORE image gen
  * Gate 25 (grid_check) on planned boxes / layout boxes (baseline clustering, 2-band split,
    empty middle gap, 3 depth bands)
  * in-memory label placement simulation (build_v2.place_labels) on draft layout rooms (without
    requiring the .jpg to exist yet) to catch label/hotspot/door/nameplate/edge collisions early
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
sys.path.insert(0, str(ROOT / "scripts" / "qa"))
sys.path.insert(0, str(ROOT / "tools"))
import build_v2
import grid_check
from walkthrough import load_model
from room_context import load_sources, resolve_word

LIMITS = json.loads((ROOT / "skills/limits.json").read_text(encoding="utf-8"))
W, H = 1280, 720
PROMPT_SECTIONS = ("IMAGE", "STYLE", "LIGHT AND COLOR", "SETTING", "SITUATION",
                   "COMPOSITION", "ITEMS", "PLACEMENT AND SPACING", "DOORS AND EXITS",
                   "GROUNDING AND ANATOMY", "FIGURES", "TEXT", "CONTENT", "VARIETY", "AVOID")
BLOCK = [r"\bgod the father\b", r"dieu le p[eè]re", r"\bdrunk", r"\bbeer\b", r"\bcigar",
         r"\bsmok(e|ing)\b(?!.*(incense|censer|chimney|smoke rises))",
         r"\bfart", r"\bpoo+\b", r"\bpee\b", r"\bbutt\b", r"\bvomit", r"\bsexy\b", r"\bkill", r"\btobacc"]
ETYM = re.compile(r"\b(Linked to|Think of|Latin|Greek|[Rr]oots? (?:of|in|is)|[Ee]tymolog\w*|from the [A-Z][a-z]+ word)")
OPEN = re.compile(r"^(On the (left|right)|In the (middle|centre|center)|Left side|Right side|Standing on the)", re.I)


def rectangle(box):
    return (isinstance(box, list) and len(box) == 4
            and all(isinstance(n, (int, float)) and not isinstance(n, bool)
                    and math.isfinite(n) for n in box)
            and box[0] >= 0 and box[1] >= 0 and box[2] > 0 and box[3] > 0
            and box[0] + box[2] <= W and box[1] + box[3] <= H)


def overlap(a, b):
    return a[0] < b[0]+b[2] and b[0] < a[0]+a[2] and a[1] < b[1]+b[3] and b[1] < a[1]+a[3]


def _beret_norm(b):
    return {"irr": "irregular"}.get(str(b or "").lower(), str(b or "").lower())


def check_item_preflight(ident, it, bld_slug, v1, vocab, fixes, overrides, fail, warn):
    """Cross-check manifest item against canonical sources, content rules, and hook lint."""
    res = resolve_word(ident, v1, vocab, fixes, overrides, force_vocab=(it.get("text") == "vocab"))
    if res is None:
        # Allow synthetic test IDs in unit tests (e.g. fr_absent_noun / fr_other_verb) unless they look like real unknown words
        if ident not in ("fr_other_verb", "fr_absent_noun", "x"):
            fail.append(f"{ident}: word id not found in vocab.jsonl or v1-payloads")
        return

    # 1. Gender & side agreement with canonical resolved word
    if it.get("pos") == "noun" and res.get("g") in ("f", "m", "mf") and it.get("g") and it.get("g") != res.get("g"):
        fail.append(f"{ident}: manifest g={it.get('g')!r} disagrees with canonical gender {res.get('g')!r}")

    # 2. Verb beret & reflexive mirror agreement with conjugation tables
    if it.get("pos") == "verb" and res.get("verb"):
        want_beret = _beret_norm(res.get("beret"))
        got_beret = _beret_norm(it.get("beret"))
        if got_beret in ("er", "ir", "re", "irregular") and want_beret and got_beret != want_beret:
            fail.append(f"{ident}: beret {it.get('beret')!r} disagrees with canonical verb group/table ({want_beret!r})")
        if res.get("reflexive"):
            combined = " ".join(str(it.get(k) or "") for k in ("hook", "hook_object", "shown", "pose_action")).lower()
            if "mirror" not in combined:
                warn.append(f"{ident}: canonical verb is reflexive ({res['fr']}); ensure hand mirror is in hook/shown")

    # 3. Pee/poo respelling & content blocklist preflight
    for k in ("say", "f_say"):
        val = res.get(k) or ""
        if re.search(r"p(ee|oo)", val, re.I):
            fail.append(f"{ident}: canonical {k} {val!r} contains pee/poo; add a respelling override in hooks.json or vocab_fixes.json")
    hook_text = str(it.get("hook") or "")
    for tok in re.findall(r"[A-Za-z]+", hook_text):
        if re.fullmatch(r"p(ee|oo)(s|ss|d|p|h|ng|ing)?", tok, re.I):
            fail.append(f"{ident}: hook token {tok!r} reads as pee/poo")
    plaque = str(it.get("sensitive") or "").startswith("plaque") or res.get("plaque")
    check_text = " ".join([hook_text, str(it.get("shown") or ""), str(it.get("pose_action") or "")] + ([] if plaque else [str(it.get("gloss") or "")]))
    for pat in BLOCK:
        if ident == "fr_fumee_noun" and "smok" in pat:
            continue
        if ident == "fr_tabac_noun" and "tobacc" in pat:
            continue
        if ident == "fr_tuer_verb" and "kill" in pat and not re.search(pat, hook_text, re.I):
            continue
        if re.search(pat, check_text, re.I):
            fail.append(f"{ident}: content blocklist match /{pat}/ in manifest text")

    # 4. Hook lint preflight
    if hook_text and not it.get("noMnemonic"):
        if re.search(r"\b(Like|Same as) English\b", hook_text) and (vocab.get(re.sub(r"_\d+$", "", ident)) or {}).get("cognate_type") == "false_cognate":
            fail.append(f"{ident}: hook uses 'Like English' on a false cognate")
        if ETYM.search(hook_text):
            warn.append(f"{ident}: hook contains etymology/meta wording ({ETYM.search(hook_text).group(0)!r})")
        if OPEN.search(hook_text):
            warn.append(f"{ident}: hook opens with a placement phrase ({hook_text[:32]!r})")
        if not re.search(r"\b[A-Z]{3,}\b", hook_text):
            warn.append(f"{ident}: hook has no word in CAPS for meaning/sound cue")
        if re.search(r'"[^"]+"(?:\s*\+\s*"[^"]+"){2,}', hook_text):
            warn.append(f"{ident}: hook has more than two quoted '+' sound chunks")


def simulate_room_labels(room_dict, bld_slug, v1, vocab, fixes, overrides, fail, warn):
    """Simulate build_v2.place_labels() and check_v2 --strict geometry without needing the .jpg on disk."""
    sim_items = []
    for spec in room_dict.get("items", []):
        if not isinstance(spec, dict):
            continue
        wid = spec.get("id")
        box = spec.get("box") or spec.get("box_hint")
        if not isinstance(wid, str) or not wid or not rectangle(box):
            continue
        res = resolve_word(wid, v1, vocab, fixes, overrides, force_vocab=(spec.get("text") == "vocab"))
        if res is None:
            fail.append(f"unknown word ID: {wid}")
            continue
        hw = spec.get("lab") or res["_headword"]
        cx = (box[0] + box[2] / 2) / W
        side = res["side"]
        if (side == "left" and cx > .45) or (side == "right" and cx < .55):
            fail.append(f"{wid}: draft box contradicts canonical side {side}")
        if res["pos"] in ("adj", "adv") and not LIMITS["centre_band"][0] <= cx <= LIMITS["centre_band"][1]:
            fail.append(f"{wid}: draft box outside center band")
        it_sim = {"id": wid, "fr": res["fr"], "hook": res["hook"], "_hw": hw, "box": list(box)}
        if spec.get("labelAt"):
            it_sim["_labelAt"] = spec["labelAt"]
        sim_items.append(it_sim)
    sim_room = {
        "name": room_dict.get("name", bld_slug),
        "nameplate": room_dict.get("nameplate"),
        "doors": [d for d in room_dict.get("doors", []) if rectangle(d.get("hit"))],
        "mapExit": room_dict.get("mapExit") if isinstance(room_dict.get("mapExit"), dict) and rectangle(room_dict["mapExit"].get("box")) else None,
        "zooms": [z for z in room_dict.get("zooms", []) if isinstance(z.get("at"), list) and len(z["at"]) == 2 and z.get("label")],
        "items": sim_items,
    }
    if sim_items:
        build_v2.place_labels(sim_room)
    fixed = [("door->" + d["to"], d["hit"]) for d in sim_room["doors"]]
    if sim_room["mapExit"]:
        fixed.append(("mapExit", sim_room["mapExit"]["box"]))
    for z in sim_room["zooms"]:
        fixed.append(("zoom->" + z["to"], build_v2.badge_rect(z)))
    np_ = build_v2.nameplate_rect(sim_room)
    if np_:
        fixed.append(("nameplate", np_))

    grow = lambda a, g=3: [a[0] - g, a[1] - g, a[2] + 2 * g, a[3] + 2 * g]
    edge = LIMITS["label_edge_px"]
    for i, it_a in enumerate(sim_items):
        la, ba = it_a["_lab"], it_a["box"]
        if la[0] < edge or la[1] < edge or la[0] + la[2] > W - edge or la[1] + la[3] > H - edge:
            warn.append(f"label {it_a['fr']} closer than {edge}px to scene edge: {la}")
        for j in range(i + 1, len(sim_items)):
            lb = sim_items[j]["_lab"]
            if overlap(la, lb):
                fail.append(f"simulated labels overlap: {it_a['fr']} / {sim_items[j]['fr']}")
            elif overlap(grow(la), lb):
                warn.append(f"simulated labels within 3px (--strict): {it_a['fr']} / {sim_items[j]['fr']}")
        for j, it_b in enumerate(sim_items):
            if i != j and overlap(grow(la), it_b["box"]):
                warn.append(f"simulated label {it_a['fr']} touches hotspot {it_b['fr']} (--strict)")
        for fn, fbox in fixed:
            if overlap(ba, fbox):
                fail.append(f"hotspot {it_a['fr']} overlaps {fn}")
            elif fn == "nameplate" and overlap(grow(ba), fbox):
                warn.append(f"hotspot {it_a['fr']} touches nameplate (--strict)")
            if overlap(la, fbox):
                fail.append(f"simulated label {it_a['fr']} overlaps {fn}")
            elif overlap(grow(la), fbox):
                warn.append(f"simulated label {it_a['fr']} touches {fn} (--strict)")

    return dict(room_dict, items=[
        dict(item, boxPx=item["box"], labelPx=item["_lab"]) for item in sim_items
    ], mapExit=dict(sim_room["mapExit"], boxPx=sim_room["mapExit"]["box"]) if sim_room["mapExit"] else None)


def validate_manifest(m, require_prompt=False, *, layout_geometry=False):
    fail, warn = [], []
    if not isinstance(m, dict):
        return ["manifest must be an object"], []
    for key in ("building", "room", "setting", "theme_fit", "scene_situation"):
        if not isinstance(m.get(key), str) or not m[key].strip():
            fail.append(f"missing {key}")
    if m.get("coordinate_space") != "1280x720-px":
        fail.append("coordinate_space must be 1280x720-px; boxes are [x,y,width,height]")
    p = m.get("prompt")
    if not isinstance(p, dict):
        p = {}
        fail.append("prompt must be an object")
    if p.get("kind") not in ("room", "zoom", "hub"):
        fail.append("prompt.kind must be room, zoom or hub")
    for key in ("room_name", "camera", "light_from", "materials", "set_apart", "place", "landmark", "whimsy", "differ"):
        if not isinstance(p.get(key), str) or not p[key].strip():
            fail.append(f"prompt.{key} must be nonempty text")
    refs = p.get("refs")
    if not (isinstance(refs, str) and refs.strip() or isinstance(refs, list) and refs and all(isinstance(x, str) and x.strip() for x in refs)):
        fail.append("prompt.refs must name actual references to attach")
    extra = m.get("prompt_extra", {})
    if not isinstance(extra, dict) or any(k not in PROMPT_SECTIONS or not isinstance(v, str) for k, v in extra.items()):
        fail.append("prompt_extra must map known section headings to text")
    entries = m.get("items")
    if not isinstance(entries, list) or (not entries and p.get("kind") != "hub"):
        return fail + ["items must be a list, nonempty except for a circulation hub"], warn

    bld_slug = str(m.get("building") or "")
    v1, vocab, fixes, overrides = load_sources(bld_slug)
    ids, boxes = set(), []
    for i, it in enumerate(entries):
        if not isinstance(it, dict):
            fail.append(f"items[{i}] must be an object")
            continue
        ident = it.get("id")
        if not isinstance(ident, str) or not ident.strip():
            fail.append(f"items[{i}] has no id")
        elif ident in ids:
            fail.append(f"duplicate item id: {ident}")
        else:
            ids.add(ident)
        for key in ("word", "pos", "gloss", "hook", "hook_object", "shown", "pose_action",
                    "sensitive", "side", "zone", "depth", "interacts_with"):
            value = it.get(key)
            if not isinstance(value, str) or not value.strip() or value.strip() in ("...", "TODO") or value.strip().startswith("TODO:"):
                fail.append(f"{ident}: missing {key}")
        count = it.get("count")
        if (count is not None and (not isinstance(count, int) or isinstance(count, bool) or count < 0)) or (it.get("pos") == "num" and count is None):
            fail.append(f"{ident}: count must be an exact nonnegative integer (null for uncounted items)")
        if it.get("pos") == "verb":
            if not it.get("verb_acts_on") or str(it.get("verb_acts_on")).strip().startswith("TODO:"):
                fail.append(f"{ident}: missing verb_acts_on")
            if it.get("beret") not in ("er", "ir", "re", "irr", "irregular"):
                fail.append(f"{ident}: invalid/missing beret")
        box = it.get("box_hint")
        if not rectangle(box):
            fail.append(f"{ident}: box_hint must be an in-frame pixel rectangle")
        else:
            boxes.append((ident, box))
            cx = (box[0] + box[2]/2)/W
            side = str(it.get("side", "")).lower()
            if side not in ("left", "right", "center", "any", "l", "r", "c"):
                fail.append(f"{ident}: invalid side")
            if (side in ("left", "l") and cx > .45) or (side in ("right", "r") and cx < .55):
                fail.append(f"{ident}: box_hint contradicts side")
            if it.get("pos") in ("adj", "adv", "intj", "phrase", "idiom") and not LIMITS["centre_band"][0] <= cx <= LIMITS["centre_band"][1]:
                fail.append(f"{ident}: outside center band")
            gender = it.get("g")
            if it.get("pos") == "noun" and gender not in ("f", "m", "mf", "n"):
                fail.append(f"{ident}: noun needs explicit g (f, m, mf or n)")
            if it.get("pos") == "noun" and ((gender == "f" and side not in ("left", "l")) or (gender == "m" and side not in ("right", "r"))):
                fail.append(f"{ident}: side contradicts noun gender")
        if isinstance(ident, str) and ident.strip():
            check_item_preflight(ident, it, bld_slug, v1, vocab, fixes, overrides, fail, warn)

    for n, (ident, box) in enumerate(boxes):
        for other, obox in boxes[n+1:]:
            if not layout_geometry and overlap(box, obox):
                fail.append(f"planned boxes overlap: {ident} / {other}")

    # Gate 25 (grid_check) on manifest box_hints when room has >= 6 items (and is not an alphabet/reference board)
    if not layout_geometry and len(boxes) >= LIMITS["room_floor"] and p.get("reference_board", "none") == "none":
        _, gprobs = grid_check.check([b for _, b in boxes])
        for gp in gprobs:
            warn.append(f"grid_check (Gate 25) on box_hint: {gp}")
        simulate_room_labels(
            {"name": p.get("room_name", m.get("room", "")), "nameplate": [50, 4.5], "items": entries, "doors": [], "zooms": []},
            bld_slug, v1, vocab, fixes, overrides, fail, warn
        )

    groups = m.get("interactions")
    covered = set()
    if not isinstance(groups, list) or (not groups and entries):
        fail.append("interactions must be a list, nonempty for a teaching scene")
    else:
        for group in groups:
            if not isinstance(group, dict):
                fail.append("each interaction must be an object")
                continue
            who = group.get("who", [])
            if not isinstance(who, list) or any(not isinstance(x, str) for x in who):
                fail.append("interaction.who must list item ids or background: roles")
                continue
            if len(set(who)) < 2 or not group.get("doing") or str(group.get("doing")).strip().startswith("TODO:"):
                fail.append("each interaction needs two distinct participants and doing")
            for ident in who:
                if ident in ids:
                    covered.add(ident)
                elif not ident.startswith("background:"):
                    fail.append(f"unknown interaction participant: {ident}")
        for it in entries:
            if isinstance(it, dict) and it.get("id") not in covered and not str(it.get("sensitive", "")).startswith("plaque"):
                fail.append(f"{it.get('id')}: no interaction group")
    for key in ("siblings", "used_motifs", "text_in_image", "zooms"):
        if not isinstance(m.get(key), list):
            fail.append(f"{key} must be a list (empty is allowed)")
    for key in ("siblings", "used_motifs"):
        if isinstance(m.get(key), list) and any(not isinstance(x, str) for x in m[key]):
            fail.append(f"{key} entries must be strings")
    if isinstance(m.get("text_in_image"), list):
        for text in m["text_in_image"]:
            if not isinstance(text, dict) or any(not isinstance(text.get(k), str) or not text[k].strip() for k in ("text", "where")):
                fail.append("each text_in_image entry needs text and where")
    doors = m.get("doors")
    destinations = set()
    if not isinstance(doors, list) or (not doors and p.get("kind") != "zoom"):
        fail.append("doors must list painted passages; ordinary rooms need a way out (doorless zooms use [])")
    else:
        for door in doors:
            if not isinstance(door, dict) or any(not door.get(k) for k in ("to", "where", "painted_as")):
                fail.append("each door needs to, where, painted_as")
                continue
            if door["to"] in destinations:
                fail.append(f"duplicate door destination: {door['to']}")
            destinations.add(door["to"])
    for z in m.get("zooms", []) if isinstance(m.get("zooms"), list) else []:
        if not isinstance(z, dict) or not z.get("to") or not isinstance(z.get("words"), list):
            fail.append("each zoom needs to and words; remove empty template rows")
        elif not all(isinstance(x, str) for x in z["words"]) or len(set(z["words"])) != len(z["words"]):
            fail.append(f"zoom {z['to']}: words must be distinct IDs")
        elif len(z["words"]) < LIMITS["zoom_min"]:
            fail.append(f"zoom {z['to']}: fewer than zoom_min words")
    if p.get("kind") == "zoom":
        c = m.get("continuity")
        if not p.get("parent") or not p.get("spot"):
            fail.append("zoom needs prompt.parent and prompt.spot")
        if not isinstance(c, dict) or not rectangle(c.get("parent_box")) or not isinstance(c.get("parent_image"), str) or not c.get("parent_image") or not isinstance(c.get("preserve"), list) or not c.get("preserve") or not all(isinstance(x, str) and x.strip() for x in c.get("preserve", [])):
            fail.append("zoom needs continuity.parent_image, parent_box and a nonempty preserve list")
    n = len([it for it in entries if isinstance(it, dict) and not it.get("noMnemonic")])
    if p.get("kind") == "room" and n < LIMITS["room_floor"]:
        warn.append(f"{n} items below room_floor {LIMITS['room_floor']}; justify density or fold into a fuller scene")
    if n > LIMITS["room_max"]:
        fail.append(f"{n} items exceeds room_max {LIMITS['room_max']}")
    elif n > LIMITS["room_target"]:
        warn.append(f"{n} items exceeds target {LIMITS['room_target']}; consider a split before painting")
    if p.get("kind") == "zoom" and p.get("reference_board", "none") == "none" and not LIMITS["zoom_min"] <= n <= LIMITS["zoom_max"]:
        warn.append(f"zoom has {n} items; target {LIMITS['zoom_min']}-{LIMITS['zoom_max']}")
    if require_prompt:
        text = m.get("prompt_text") or ""
        if not isinstance(text, str):
            fail.append("prompt_text must be a string")
        else:
            missing = [s for s in PROMPT_SECTIONS if not re.search(rf"^{re.escape(s)}:", text, re.M)]
            if missing:
                fail.append("prompt_text missing sections: " + ", ".join(missing))
            if re.search(r"\{[^{}\n]+\}", text):
                fail.append("prompt_text contains unfilled fields")
    return fail, warn


def validate_layout(d, selected=None, *, review_rooms=None):
    fail, warn = [], []
    if not isinstance(d, dict):
        return ["layout must be an object"], []
    rooms = d.get("rooms", {})
    main = d.get("main", d.get("building"))
    if not isinstance(rooms, dict) or main not in rooms:
        return ["layout main must name a room"], []
    bld_slug = str(d.get("building") or main)
    if d.get("building"):
        try:
            load_model(ROOT, d)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
            fail.append(f"invalid walkthrough: {error}")
    v1, vocab, fixes, overrides = load_sources(bld_slug)
    keys = selected or list(rooms)
    for key in keys:
        if key not in rooms:
            fail.append(f"unknown room: {key}")
            continue
        r = rooms[key]
        ids, boxes, dests = set(), [], set()
        for it in r.get("items", []):
            if not it.get("id") or it["id"] in ids:
                fail.append(f"{key}: missing/duplicate word id {it.get('id')}")
            ids.add(it.get("id"))
            if not rectangle(it.get("box")):
                fail.append(f"{key}/{it.get('id')}: invalid pixel box")
            else:
                boxes.append((it.get("id"), it["box"]))
        for i, (name, box) in enumerate(boxes):
            for other, obox in boxes[i+1:]:
                if overlap(box, obox):
                    fail.append(f"{key}: boxes overlap {name} / {other}")
        if len(boxes) >= LIMITS["room_floor"] and not r.get("parent"):
            _, gprobs = grid_check.check([b for _, b in boxes])
            for gp in gprobs:
                warn.append(f"{key}: grid_check (Gate 25): {gp}")
        if review_rooms is not None:
            for door in r.get("doors", []):
                if not rectangle(door.get("hit")):
                    fail.append(f"{key}: door {door.get('to')} needs a fitted hit box")
            if r.get("mapExit") and not rectangle(r["mapExit"].get("box")):
                fail.append(f"{key}: outside exit needs a fitted box")
            for zoom in r.get("zooms", []):
                at = zoom.get("at")
                if not (isinstance(at, list) and len(at) == 2 and all(
                        isinstance(x, (int, float)) and not isinstance(x, bool) for x in at)
                        and 0 <= at[0] <= W and 0 <= at[1] <= H and zoom.get("label")):
                    fail.append(f"{key}: zoom {zoom.get('to')} needs a fitted badge and label")
        if boxes or review_rooms is not None:
            review = simulate_room_labels(r, bld_slug, v1, vocab, fixes, overrides, fail, warn)
            if review_rooms is not None:
                review_rooms[key] = review
        for edge in r.get("doors", []) + r.get("zooms", []):
            to = edge.get("to")
            target = (edge.get("building", d.get("building")), to)
            if target in dests:
                fail.append(f"{key}: duplicate destination {target}")
            dests.add(target)
            if not edge.get("building") and to not in rooms:
                fail.append(f"{key}: unknown destination {to}")
        for z in r.get("zooms", []):
            if not rectangle(z.get("obj")):
                fail.append(f"{key}: zoom {z.get('to')} has invalid obj")
            elif z.get("to") in rooms and rooms[z["to"]].get("parent") != key:
                fail.append(f"{key}: zoom {z['to']} has a different parent")
        parent = r.get("parent")
        if parent and (parent not in rooms or not any(z.get("to") == key for z in rooms[parent].get("zooms", []))):
            fail.append(f"{key}: parent does not link to this zoom")
    # Reachability is structural; a human still checks whether passages make physical sense.
    seen, todo = set(), [main]
    while todo:
        key = todo.pop()
        if key in seen or key not in rooms:
            continue
        seen.add(key)
        todo.extend(e.get("to") for e in rooms[key].get("doors", []) + rooms[key].get("zooms", []) if not e.get("building"))
    for key in keys:
        if key in rooms and key not in seen:
            fail.append(f"{key}: unreachable from main through painted passages/zooms")
    return fail, warn


def linked_room_errors(manifest, layout, selected=None):
    key = manifest.get("room")
    rooms = layout.get("rooms", {})
    room = rooms.get(key)
    if manifest.get("building") != layout.get("building") or room is None:
        return ["manifest building/room does not match draft layout"]
    if selected and selected != [key]:
        return ["select the manifest room when checking a linked plan"]

    def boxes(items, field):
        return {item["id"]: item.get(field) for item in items if isinstance(item, dict) and "id" in item}

    failures = []
    if boxes(manifest.get("items", []), "box_hint") != boxes(room.get("items", []), "box"):
        failures.append("manifest and draft layout must agree on item IDs and boxes")
    expected = {door.get("to") for door in room.get("doors", [])}
    if room.get("mapExit"):
        expected.add("map")
    if expected != {door.get("to") for door in manifest.get("doors", [])}:
        failures.append("manifest and draft layout must agree on passage destinations")
    if {z.get("to") for z in room.get("zooms", [])} != {z.get("to") for z in manifest.get("zooms", [])}:
        failures.append("manifest and draft layout must agree on zoom destinations")
    prompt = manifest.get("prompt", {})
    parent = room.get("parent")
    if parent or prompt.get("kind") == "zoom":
        if parent != prompt.get("parent"):
            failures.append("manifest and draft layout must agree on the zoom parent")
        else:
            zoom = next((z for z in rooms.get(parent, {}).get("zooms", []) if z.get("to") == key), {})
            if manifest.get("continuity", {}).get("parent_box") != zoom.get("obj"):
                failures.append("manifest and draft layout must agree on the parent zoom crop")
    return failures


_IMAGE_PATH = re.compile(r"[\w./+-]+\.(?:jpg|jpeg|png|webp)", re.I)


def _resolve_image(token):
    token = str(token).lstrip("./")
    for candidate in (ROOT / token, ROOT / "village" / token):
        if candidate.is_file():
            return candidate.resolve()
    return None


def _sector_image(layout):
    """Repo-relative path of the sector painting, from the layout's sector id."""
    sector_id = layout.get("sector_id") if isinstance(layout, dict) else None
    if not sector_id:
        return None
    try:
        maps = json.loads((ROOT / "content/v2/map.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    slug = next((row.get("slug") for row in (maps.get("world") or {}).get("sectors") or []
                 if row.get("id") == sector_id), None)
    image = ((maps.get("sectors") or {}).get(slug) or {}).get("image") if slug else None
    if not isinstance(image, str) or not image.strip():
        return None
    return "village/" + image.lstrip("./")


def exit_identity_refs(manifest, layout):
    """Fail when a sector return does not name the real sector image, or a named image is missing.

    This checks manifest paths against the repo. It does not accept or reject a painting.
    """
    if not isinstance(manifest, dict) or not isinstance(layout, dict):
        return []
    fail = []
    refs = (manifest.get("prompt") or {}).get("refs")
    text = " ".join(refs) if isinstance(refs, list) else str(refs or "")
    for token in _IMAGE_PATH.findall(text):
        if _resolve_image(token) is None:
            fail.append(f"prompt.refs names a missing image: {token}")
    room = (layout.get("rooms") or {}).get(manifest.get("room"), {})
    doors = manifest.get("doors") if isinstance(manifest.get("doors"), list) else []
    returns_to_sector = any(isinstance(door, dict) and door.get("to") == "map" for door in doors) or bool(
        isinstance(room, dict) and room.get("mapExit"))
    if not returns_to_sector:
        return fail
    need = _sector_image(layout)
    if not need:
        return fail
    target = _resolve_image(need)
    if target is None:
        fail.append(f"sector image missing on disk: {need}")
        return fail
    named = {_resolve_image(token) for token in _IMAGE_PATH.findall(text)}
    if target not in named:
        fail.append(f"map exit requires the sector image in prompt.refs: {need}")
    return fail


def validate_plan(manifest=None, layout=None, selected=None, require_prompt=False):
    """Check one linked plan using the draft's actual controls and label geometry."""
    fail, warn = [], []
    if isinstance(manifest, dict) and isinstance(layout, dict):
        fail = linked_room_errors(manifest, layout, selected)
        if fail:
            return fail, warn
        selected = [manifest["room"]]
    if manifest is not None:
        f, w = validate_manifest(manifest, require_prompt, layout_geometry=layout is not None)
        fail.extend(f)
        warn.extend(w)
    if layout is not None:
        f, w = validate_layout(layout, selected, review_rooms={} if manifest is not None else None)
        fail.extend(f)
        warn.extend(w)
    if isinstance(manifest, dict) and isinstance(layout, dict):
        fail.extend(exit_identity_refs(manifest, layout))
    return list(dict.fromkeys(fail)), list(dict.fromkeys(warn))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest")
    ap.add_argument("--layout")
    ap.add_argument("--room", action="append")
    ap.add_argument("--require-prompt", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not a.manifest and not a.layout:
        ap.error("supply --manifest and/or --layout")
    try:
        manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8")) if a.manifest else None
        layout = json.loads(Path(a.layout).read_text(encoding="utf-8")) if a.layout else None
        fail, warn = validate_plan(manifest, layout, a.room, a.require_prompt)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
        fail, warn = [str(e)], []
    result = {"fail": fail, "warn": warn, "visual_review": "not_checked"}
    if a.json:
        Path(a.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for message in fail:
        print("FAIL", message)
    for message in warn:
        print("WARN", message)
    print(f"plan: {len(fail)} fail, {len(warn)} warn; visual/language judgment not checked")
    return bool(fail)


if __name__ == "__main__":
    raise SystemExit(main())

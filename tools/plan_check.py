#!/usr/bin/env python3
"""Check a room manifest BEFORE generating art, or a building's draft layout.

  python tools/plan_check.py --manifest manifest.json
  python tools/plan_check.py --layout content/v2/ecole/layout.json --room cantine
  python tools/plan_check.py --manifest manifest.json --json review.json

These checks establish structural completeness, not visual or linguistic truth.
"""
import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMITS = json.loads((ROOT / "skills/limits.json").read_text())
W, H = 1280, 720
PROMPT_SECTIONS = ("IMAGE", "STYLE", "LIGHT AND COLOR", "SETTING", "SITUATION",
                   "COMPOSITION", "ITEMS", "PLACEMENT AND SPACING", "DOORS AND EXITS",
                   "GROUNDING AND ANATOMY", "FIGURES", "TEXT", "CONTENT", "VARIETY", "AVOID")


def rectangle(box):
    return (isinstance(box, list) and len(box) == 4
            and all(isinstance(n, (int, float)) and not isinstance(n, bool)
                    and math.isfinite(n) for n in box)
            and box[0] >= 0 and box[1] >= 0 and box[2] > 0 and box[3] > 0
            and box[0] + box[2] <= W and box[1] + box[3] <= H)


def overlap(a, b):
    return a[0] < b[0]+b[2] and b[0] < a[0]+a[2] and a[1] < b[1]+b[3] and b[1] < a[1]+a[3]


def validate_manifest(m, require_prompt=False):
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
    if p.get("kind") not in ("room", "zoom"):
        fail.append("prompt.kind must be room or zoom")
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
    if not isinstance(entries, list) or not entries:
        return fail + ["items must be a nonempty list"], warn
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
            if not isinstance(value, str) or not value.strip() or value.strip() in ("...", "TODO"):
                fail.append(f"{ident}: missing {key}")
        count = it.get("count")
        if (count is not None and (not isinstance(count, int) or isinstance(count, bool) or count < 0)) or (it.get("pos") == "num" and count is None):
            fail.append(f"{ident}: count must be an exact nonnegative integer (null for uncounted items)")
        if it.get("pos") == "verb":
            if not it.get("verb_acts_on"):
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
    for n, (ident, box) in enumerate(boxes):
        for other, obox in boxes[n+1:]:
            if overlap(box, obox):
                fail.append(f"planned boxes overlap: {ident} / {other}")
    groups = m.get("interactions")
    covered = set()
    if not isinstance(groups, list) or not groups:
        fail.append("interactions must be a nonempty list")
    else:
        for group in groups:
            if not isinstance(group, dict):
                fail.append("each interaction must be an object")
                continue
            who = group.get("who", [])
            if not isinstance(who, list) or any(not isinstance(x, str) for x in who):
                fail.append("interaction.who must list item ids or background: roles")
                continue
            if len(set(who)) < 2 or not group.get("doing"):
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


def validate_layout(d, selected=None):
    fail, warn = [], []
    if not isinstance(d, dict):
        return ["layout must be an object"], []
    rooms = d.get("rooms", {})
    main = d.get("main", d.get("building"))
    if not isinstance(rooms, dict) or main not in rooms:
        return ["layout main must name a room"], []
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
    fail, warn = [], []
    for path, func in ((a.manifest, lambda d: validate_manifest(d, a.require_prompt)),
                       (a.layout, lambda d: validate_layout(d, a.room))):
        if path:
            try:
                f, w = func(json.loads(Path(path).read_text(encoding="utf-8")))
                fail.extend(f); warn.extend(w)
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as e:
                fail.append(f"{path}: {e}")
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

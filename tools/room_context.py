#!/usr/bin/env python3
"""Print bounded room context instead of full card/conjugation payloads.

python tools/room_context.py ecole --room cantine --limit 20 --offset 0
python tools/room_context.py B63_pompiers --room R_abs_problem_01 --init-manifest /tmp/manifest.json
Selected room: exact IDs, hooks, pronunciation and boxes (for built rooms) or
resolved canonical word records, beret/reflexive markers and live locations (for
unbuilt source rooms). Siblings: short alts. Without --room: building overview.
"""
import argparse, json, re, sys
from collections import Counter
from functools import lru_cache
from pathlib import Path
from unbuilt import live_ids, load_payload

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
import build_v2  # reuse exact v1/vocab/vocab_fixes/hooks resolution and beret logic

STOP = set("THE AND WITH FOR FROM ONE TWO HIS HER ITS SAY SAID NOT BUT YOU ARE".split())
BERET_CODE = {"red": "er", "green": "ir", "purple": "re", "gold": "irregular"}


@lru_cache(maxsize=1)
def shared_sources():
    return build_v2.load_v1_items(), build_v2.load_vocab()


def load_sources(bld_slug):
    v1, vocab = shared_sources()
    fp = ROOT / "content" / "v2" / "vocab_fixes.json"
    fixes = {k: v for k, v in json.loads(fp.read_text(encoding="utf-8")).items() if not k.startswith("_")} if fp.exists() else {}
    hp = ROOT / "content" / "v2" / bld_slug / "hooks.json"
    overrides = {k: v for k, v in json.loads(hp.read_text(encoding="utf-8")).items() if not k.startswith("_")} if hp.exists() else {}
    return v1, vocab, fixes, overrides


def resolve_word(wid, v1, vocab, fixes, overrides, force_vocab=False):
    """Resolve one word ID using build_v2.py's exact precedence."""
    kept = build_v2.load_kept_cards()
    if wid in kept and not force_vocab:
        it = {k: v for k, v in kept[wid].items() if k not in ("img", "box", "label", "side", "surface", "cardSrc")}
    elif wid in v1 and not force_vocab:
        it = {k: v for k, v in v1[wid].items() if k not in ("img", "box", "label", "side", "surface", "cardSrc")}
    elif wid in vocab:
        w = vocab[wid]
        if overrides.get(wid, {}).get("pronominal_form"):
            w = dict(w, reflexive=True, pronominal_form=overrides[wid]["pronominal_form"])
        if "reflexive" in overrides.get(wid, {}):
            w = dict(w, _reflexive=bool(overrides[wid]["reflexive"]))
        it = build_v2.item_from_vocab(w)
    else:
        return None
    fix = dict(fixes.get(wid, {}))
    fix.update({k: v for k, v in overrides.get(wid, {}).items() if k in ("art", "g")})
    build_v2.apply_grammar_fix(it, fix)
    for src in (fixes.get(wid, {}), overrides.get(wid, {})):
        if src.get("fr"):
            it["fr"] = src["fr"]
        for k in ("say", "f_say", "hook", "en"):
            if src.get(k):
                it[k] = src[k]
        if "note" in src:
            it["note"] = src["note"]
        if src.get("ex"):
            it["ex"] = list(src["ex"])
    if overrides.get(wid, {}).get("plaque") is True:
        it["plaque"] = True
    raw_pos = vocab.get(wid, {}).get("pos") or ("verb" if it.get("verb") else "adj" if it.get("adj") else "adv" if it.get("adv") else "noun")
    side = "any" if raw_pos == "verb" else ("left" if it.get("g") == "f" else "right" if it.get("g") == "m" else "center")
    out = {
        "id": wid,
        "fr": it["fr"],
        "_headword": build_v2.headword(it),
        "pos": raw_pos,
        "side": side,
        "en": it.get("en", ""),
        "ipa": it.get("ipa", ""),
        "say": it.get("say", ""),
        "hook": it.get("hook", ""),
        "note": it.get("note"),
    }
    if it.get("g") in ("f", "m", "mf", "n"):
        out["g"] = it["g"]
    if it.get("art"):
        out["art"] = it["art"]
    if it.get("f_say"):
        out["f_say"] = it["f_say"]
    if it.get("verb"):
        out["verb"] = True
        out["beret"] = BERET_CODE.get(it.get("beret"), "irregular")
        out["reflexive"] = bool(it.get("reflexive"))
    if it.get("plaque"):
        out["plaque"] = True
    return out


def suggest_boxes(resolved_items):
    """Assign non-overlapping initial [x, y, w, h] pixel envelopes that respect gender sides,
    center band, edge margins, and Gate 25 (<=3 box bottoms within 40 px; 3 depth bands)."""
    lefts = [it for it in resolved_items if it["side"] == "left"]
    rights = [it for it in resolved_items if it["side"] == "right"]
    centers = [it for it in resolved_items if it["side"] not in ("left", "right")]

    # Pre-staggered non-overlapping slots per band [x, y, w, h] with distinct bottoms across back/middle/front
    # Up to 10 non-overlapping slots per side (3 columns x 3-4 rows, all centers < 45% for left and > 55% for right)
    left_slots = [
        [80, 75, 145, 115],    # bottom 190 (back)
        [240, 105, 145, 130],  # bottom 235 (back)
        [400, 140, 135, 140],  # bottom 280 (back)
        [80, 235, 145, 130],   # bottom 365 (back)
        [240, 280, 145, 145],  # bottom 425 (middle)
        [400, 325, 135, 145],  # bottom 470 (middle)
        [80, 410, 145, 135],   # bottom 545 (middle)
        [240, 470, 145, 140],  # bottom 610 (front)
        [400, 515, 135, 140],  # bottom 655 (front)
        [80, 545, 145, 120],   # bottom 665 (front)
    ]
    center_slots = [
        [470, 80, 155, 130],   # bottom 210 (back)
        [645, 120, 155, 135],  # bottom 255 (back)
        [470, 260, 155, 145],  # bottom 405 (back)
        [645, 315, 155, 145],  # bottom 460 (middle)
        [470, 460, 155, 135],  # bottom 595 (front)
        [645, 505, 155, 140],  # bottom 645 (front)
    ]
    right_slots = [
        [745, 65, 145, 110],   # bottom 175 (back)
        [910, 115, 145, 140],  # bottom 255 (back)
        [1060, 160, 140, 150], # bottom 310 (back)
        [745, 225, 145, 130],  # bottom 355 (back)
        [910, 295, 145, 150],  # bottom 445 (middle)
        [1060, 350, 140, 150], # bottom 500 (middle)
        [745, 405, 145, 130],  # bottom 535 (middle)
        [910, 485, 145, 140],  # bottom 625 (front)
        [1060, 520, 140, 140], # bottom 660 (front)
        [745, 555, 145, 105],  # bottom 660 (front)
    ]
    boxes = {}
    for group, slots in ((lefts, left_slots), (centers, center_slots), (rights, right_slots)):
        for idx, it in enumerate(group):
            boxes[it["id"]] = list(slots[idx % len(slots)])
    return boxes


def depth_of(box):
    bot = box[1] + box[3]
    return "back" if bot <= 420 else ("front" if bot > 580 else "middle")


def scaffold_manifest(bld_slug, bld_id, sector_id, room_key, room_name, resolved_items, siblings):
    boxes = suggest_boxes(resolved_items)
    items = []
    for it in resolved_items:
        b = boxes[it["id"]]
        d = depth_of(b)
        entry = {
            "id": it["id"],
            "word": it["fr"],
            "pos": it["pos"],
            "gloss": it["en"],
            "hook": it["hook"],
            "hook_object": "TODO: literal sound-cue object",
            "shown": "TODO: figure and prop shown in scene",
            "pose_action": "TODO: visible action/pose",
            "count": int(it["fr"]) if it["pos"] == "num" and it["fr"].isdigit() else None,
            "sensitive": "plaque" if it.get("plaque") else "none",
            "side": it["side"],
            "zone": f"{it['side']} {d} {b}",
            "depth": d,
            "box_hint": b,
            "interacts_with": "TODO: interaction partner",
        }
        if "g" in it:
            entry["g"] = it["g"]
        if it.get("verb"):
            entry["beret"] = it["beret"]
            entry["reflexive"] = bool(it.get("reflexive"))
            entry["verb_acts_on"] = "TODO: noun/object acted on at human scale"
        items.append(entry)

    # Pair items into initial interaction groups of 2-3 so structure is ready to refine
    interactions = []
    ids = [it["id"] for it in resolved_items if not it.get("plaque")]
    for i in range(0, len(ids), 2):
        chunk = ids[i:i + 2]
        if len(chunk) == 1 and interactions:
            interactions[-1]["who"].append(chunk[0])
        elif len(chunk) == 1:
            interactions.append({"who": [chunk[0], "background: companion figure"], "doing": "TODO: shared activity"})
        else:
            interactions.append({"who": chunk, "doing": "TODO: shared activity between these figures"})

    return {
        "building": bld_slug,
        "building_id": bld_id,
        "sector_id": sector_id,
        "room": room_key,
        "coordinate_space": "1280x720-px",
        "setting": f"TODO: setting for {room_name}",
        "theme_fit": f"All {len(items)} words belong to {room_name}.",
        "scene_situation": f"TODO: one shared everyday moment in {room_name}",
        "prompt": {
            "kind": "room",
            "room_name": room_name,
            "camera": "eye-level three-quarter view",
            "light_from": "clear daylight from upper left",
            "refs": "TODO: attach sector map and building style references",
            "look": f"{bld_slug} exterior on sector map",
            "materials": "TODO: walls, floor, wood/stone and palette",
            "set_apart": "TODO: distinctive time of day, light and dominant color",
            "place": room_name,
            "landmark": "TODO: central architectural landmark",
            "whimsy": "TODO: playful architectural feature tied to the room's theme",
            "differ": "TODO: how camera, layout and focal action differ from siblings",
            "reference_board": "none",
        },
        "siblings": siblings,
        "used_motifs": [],
        "doors": [
            {
                "to": "map",
                "where": "left open doorway [35, 90, 160, 240]",
                "painted_as": "open doorway leading out to the sector square",
            }
        ],
        "zooms": [],
        "text_in_image": [],
        "interactions": interactions,
        "items": items,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("building")
    ap.add_argument("--room", help="built room key or unbuilt source room ID (R_... / ST_...)")
    ap.add_argument("--vocab-room", help="explicit source room ID (R_... / ST_...) when --room names the new v2 key")
    ap.add_argument("--word", action="append", default=[], help="extra word ID(s) to resolve (e.g. verb move-ins)")
    ap.add_argument("--init-manifest", metavar="PATH", help="write a pre-populated manifest JSON with resolved word facts and non-overlapping box_hints")
    ap.add_argument("--limit", type=int, default=20, help="max planned words per page")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--compact", action="store_true", help="emit one target record per word plus routes, without notes or sibling descriptions")
    a = ap.parse_args()
    if a.compact and not a.room:
        ap.error("--compact requires --room")
    if a.limit < 1 or a.offset < 0:
        ap.error("limit must be positive; offset must be nonnegative")

    registry = json.loads((ROOT / "data/source/buildings.json").read_text(encoding="utf-8"))["buildings"]
    reg_match = [b for b in registry if b["id"] == a.building or b["id"].split("_", 1)[-1] == a.building or b["id"].lower() == a.building.lower()]
    bld_meta = reg_match[0] if len(reg_match) == 1 else {}
    bld_slug = re.sub(r"^B\d+_", "", bld_meta["id"]).lower() if bld_meta.get("id", "").startswith("B") else (bld_meta["id"].lower() if bld_meta.get("id") else a.building)

    payload = ROOT / "village" / "data" / f"{bld_slug}.js"
    layout = ROOT / "content" / "v2" / bld_slug / "layout.json"
    if payload.exists():
        D = load_payload(payload)
    elif layout.exists():
        D = json.loads(layout.read_text(encoding="utf-8"))
    elif bld_meta:
        D = {"rooms": {}, "main": "not painted", "building_id": bld_meta["id"], "sector_id": bld_meta.get("sector_id")}
    else:
        ap.error("building not found uniquely in live data, layout or source registry")

    bid = D.get("building_id") or bld_meta.get("id", "")
    sector_id = D.get("sector_id") or bld_meta.get("sector_id", "")
    rooms_src = {r["id"]: r for r in json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
    live_map = live_ids(ROOT)
    live = set(live_map)
    v1, vocab, fixes, overrides = load_sources(bld_slug)

    if not a.compact:
        print(f"# {bld_slug} ({bid}): {len(D['rooms'])} rooms, main {D['main']}")
    motifs = Counter()
    siblings = []
    for key, R in D["rooms"].items():
        for it in R["items"]:
            if a.compact:
                break
            live.add(it["id"]); live.add(re.sub(r"_\d+$", "", it["id"]))
            h = it.get("hook") or ""
            say = set(re.findall(r"[A-Z]+", it.get("say") or ""))
            for w in re.findall(r"\b[A-Z]{4,}S?\b", h):
                if w not in STOP and w not in say:
                    motifs[w] += 1
        if a.room and key != a.room:
            sib_line = f"{key}: {len(R.get('items', []))} words; {(R.get('alt') or '')[:160]}"
            siblings.append(sib_line)
            if not a.compact:
                print("sibling " + sib_line)
            continue
        if a.compact:
            continue
        side = lambda it: "C" if it.get("adj") or it.get("adv") else {"f": "L", "m": "R"}.get(it.get("g"), "C")
        words = ", ".join(f"{it.get('lab') or it['fr']}({side(it)}{',verb' if it.get('verb') else ''})" for it in R["items"])
        doors = ", ".join(d.get("to", "?") for d in R.get("doors", [])) + (", map" if R.get("mapExit") else "")
        zooms = ", ".join(z.get("to", "?") for z in R.get("zooms", []))
        print(f"\n## {key}: {R['name']}" + (f" (zoom of {R['parent']})" if R.get("parent") else ""))
        print(f"alt: {(R.get('alt') or '')[:400]}")
        print(f"{len(R['items'])} words: {words}")
        if a.room:
            for it in R["items"]:
                row = {k: it[k] for k in ("id", "fr", "g", "en", "ipa", "say", "hook", "note", "boxPx", "verb", "beret", "reflexive") if k in it}
                print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
        if doors: print(f"doors: {doors}")
        if zooms: print(f"zooms: {zooms}")

    # Resolve target source room or extra words when target is not yet painted (or when --vocab-room / --word is given)
    src_room_id = a.vocab_room or (a.room if a.room in rooms_src else None)
    if a.room and a.room not in D["rooms"] and not src_room_id:
        # Check if any source room in this building matches a.room
        for rid, rmeta in rooms_src.items():
            if rmeta.get("building_id") == bid and (rid == a.room or rid.lower().endswith(a.room.lower())):
                src_room_id = rid
                break

    resolved_target = []
    if a.compact or (a.room and a.room not in D["rooms"]) or a.vocab_room or a.word:
        current = {it["id"]: it for it in D["rooms"].get(a.room, {}).get("items", [])}
        layout_path = ROOT / "content" / "v2" / bld_slug / "layout.json"
        layout_rooms = json.loads(layout_path.read_text())["rooms"] if layout_path.exists() else {}
        specs = {it["id"]: it for it in layout_rooms.get(a.room, {}).get("items", [])}
        unknown = []
        want_ids = []
        if a.room and a.room in D["rooms"]:
            want_ids.extend(it["id"] for it in D["rooms"][a.room]["items"])
        elif src_room_id and src_room_id in rooms_src:
            want_ids.extend(rooms_src[src_room_id].get("words", []))
        for w_extra in a.word:
            if w_extra not in want_ids:
                want_ids.append(w_extra)
        rm_title = rooms_src.get(src_room_id, {}).get("name", a.room or src_room_id or bld_slug)
        if not a.compact:
            print(f"\n## target resolved inventory ({src_room_id or a.room}: {len(want_ids)} words)")
        for wid in dict.fromkeys(want_ids):
            res = resolve_word(wid, v1, vocab, fixes, overrides, force_vocab=specs.get(wid, {}).get("text") == "vocab")
            if not res:
                unknown.append(wid)
                if not a.compact:
                    print(f"UNKNOWN word id: {wid}")
                continue
            where_live = [f"{b}/{rk}" for b, rk in live_map.get(wid, [])]
            if where_live:
                res["live_in"] = where_live
            if wid in current and current[wid].get("boxPx"):
                res["boxPx"] = current[wid]["boxPx"]
            if specs.get(wid, {}).get("text") == "vocab":
                res["text"] = "vocab"
            resolved_target.append(res)
            if not a.compact:
                print(json.dumps({k: v for k, v in res.items() if not k.startswith("_")}, ensure_ascii=False, separators=(",", ":")))
        if unknown:
            ap.error("unknown word IDs: " + ", ".join(unknown))

    if a.init_manifest:
        if not resolved_target and a.room in D["rooms"]:
            for it in D["rooms"][a.room]["items"]:
                res = resolve_word(it["id"], v1, vocab, fixes, overrides)
                if res:
                    resolved_target.append(res)
        if not resolved_target:
            ap.error("--init-manifest requires a resolvable --room, --vocab-room, or --word list")
        rk = a.room if (a.room and a.room not in rooms_src) else bld_slug
        rname = D["rooms"][a.room]["name"] if (a.room and a.room in D["rooms"]) else rooms_src.get(src_room_id, {}).get("name", rk)
        manifest = scaffold_manifest(bld_slug, bid, sector_id, rk, rname, resolved_target, siblings)
        Path(a.init_manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if not a.compact:
            print(f"\nwrote scaffold manifest: {a.init_manifest} ({len(resolved_target)} items)")

    if a.compact:
        if a.room not in D["rooms"] and src_room_id not in rooms_src and not a.word:
            ap.error("unknown room; provide --vocab-room or --word for a draft")
        room = D["rooms"].get(a.room, {})
        items = [{k: v for k, v in row.items() if not k.startswith("_")} for row in resolved_target]
        print(json.dumps({"building": bld_slug, "room": a.room, "items": items,
                          "doors": [d["to"] for d in room.get("doors", [])],
                          "zooms": [z["to"] for z in room.get("zooms", [])],
                          "outside": bool(room.get("mapExit"))}, ensure_ascii=False, separators=(",", ":")))
        return

    print("\n## candidate motifs (capitalization heuristic; inspect hooks for actual reuse)")
    print(", ".join(f"{w.lower()}" + (f" x{n}" if n > 1 else "") for w, n in motifs.most_common(60)))
    plan = []
    for r in vocab.values():
        room = rooms_src.get(r.get("room_id") or "")
        if room and bid and room.get("building_id") == bid and r["id"] not in live:
            plan.append(f"{r['id']}: {r['lemma']} ({r.get('cefr', '')}, {room.get('name', room['id'])})")
    print(f"\n## planned words not live yet: {len(plan)}")
    if plan: print(", ".join(plan[a.offset:a.offset+a.limit]) + (f" ... next: --offset {a.offset+a.limit}" if len(plan) > a.offset+a.limit else ""))
    rc = ROOT / "data" / "hooks" / "qa" / "RECOMMENDED_CHANGES.md"
    if rc.exists():
        notes = [l.strip() for l in rc.read_text(encoding="utf-8").splitlines() if re.search(rf"\b({re.escape(a.building)}|{re.escape(bld_slug)})\b", l)]
        print(f"\n## open notes naming {bld_slug} in RECOMMENDED_CHANGES.md: {len(notes)}")
        for n in notes[:20]: print("- " + n[:200].lstrip("-* "))


if __name__ == "__main__":
    main()

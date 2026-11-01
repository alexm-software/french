#!/usr/bin/env python3
"""Print bounded room context instead of full card/conjugation payloads.

python tools/room_context.py ecole --room cantine --limit 20 --offset 0
Selected room: exact IDs, hooks, pronunciation and boxes. Siblings: short alts.
Without --room: building overview. Planned words exclude IDs live anywhere in
the village. Also supports layouts or source-registry buildings not yet painted.
Motifs inferred from capitalized hook text are candidates, not a visual audit.
"""
import argparse, json, re
from collections import Counter
from pathlib import Path
from unbuilt import live_ids, load_payload

ROOT = Path(__file__).resolve().parents[1]
STOP = set("THE AND WITH FOR FROM ONE TWO HIS HER ITS SAY SAID NOT BUT YOU ARE".split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("building")
    ap.add_argument("--room")
    ap.add_argument("--limit", type=int, default=20, help="max planned words per page")
    ap.add_argument("--offset", type=int, default=0)
    a = ap.parse_args()
    if a.limit < 1 or a.offset < 0:
        ap.error("limit must be positive; offset must be nonnegative")
    payload = ROOT / "village" / "data" / f"{a.building}.js"
    layout = ROOT / "content" / "v2" / a.building / "layout.json"
    if payload.exists():
        D = load_payload(payload)
    elif layout.exists():
        D = json.loads(layout.read_text())
    else:
        registry = json.loads((ROOT / "data/source/buildings.json").read_text())["buildings"]
        matches = [b for b in registry if b["id"] == a.building or b["id"].split("_", 1)[-1] == a.building]
        if len(matches) != 1:
            ap.error("building not found uniquely in live data, layout or source registry")
        D = {"rooms": {}, "main": "not painted", "building_id": matches[0]["id"]}
    if a.room and a.room not in D["rooms"]:
        print(f"Target {a.room}: not painted; plan from the source assignments below.")
    print(f"# {a.building}: {len(D['rooms'])} rooms, main {D['main']}")
    motifs = Counter()
    live = set(live_ids(ROOT))
    for key, R in D["rooms"].items():
        for it in R["items"]:
            live.add(it["id"]); live.add(re.sub(r"_\d+$", "", it["id"]))
            h = it.get("hook") or ""
            say = set(re.findall(r"[A-Z]+", it.get("say") or ""))
            for w in re.findall(r"\b[A-Z]{4,}S?\b", h):
                if w not in STOP and w not in say:
                    motifs[w] += 1
        if a.room and key != a.room:
            print(f"sibling {key}: {len(R.get('items', []))} words; {(R.get('alt') or '')[:160]}")
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
                print(json.dumps({k: it[k] for k in ("id", "fr", "g", "en", "ipa", "say", "hook", "note", "boxPx", "verb", "reflexive") if k in it}, ensure_ascii=False, separators=(",", ":")))
        if doors: print(f"doors: {doors}")
        if zooms: print(f"zooms: {zooms}")
    print("\n## candidate motifs (capitalization heuristic; inspect hooks for actual reuse)")
    print(", ".join(f"{w.lower()}" + (f" x{n}" if n > 1 else "") for w, n in motifs.most_common(60)))
    plan = []
    rooms = {r["id"]: r for r in json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
    bid = D.get("building_id", "")
    for l in (ROOT / "data" / "source" / "vocab.jsonl").read_text(encoding="utf-8").splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        room = rooms.get(r.get("room_id") or "")
        if room and bid and room.get("building_id") == bid and r["id"] not in live:
            plan.append(f"{r['id']}: {r['lemma']} ({r.get('cefr', '')}, {room.get('name', room['id'])})")
    print(f"\n## planned words not live yet: {len(plan)}")
    if plan: print(", ".join(plan[a.offset:a.offset+a.limit]) + (f" ... next: --offset {a.offset+a.limit}" if len(plan) > a.offset+a.limit else ""))
    rc = ROOT / "data" / "hooks" / "qa" / "RECOMMENDED_CHANGES.md"
    if rc.exists():
        notes = [l.strip() for l in rc.read_text(encoding="utf-8").splitlines() if re.search(rf"\b{re.escape(a.building)}\b", l)]
        print(f"\n## open notes naming {a.building} in RECOMMENDED_CHANGES.md: {len(notes)}")
        for n in notes[:20]: print("- " + n[:200].lstrip("-* "))


if __name__ == "__main__":
    main()

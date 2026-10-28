#!/usr/bin/env python3
"""room_context.py - a compact brief of one building, for planning a room or a repaint (about 1-2k tokens).

  python3 tools/room_context.py ecole             # every room of the building
  python3 tools/room_context.py ecole --room cantine

Read this instead of village/data/<bld>.js (up to 128 KB of card text and verb tables), layout.json and
hooks.json. It prints, per room: the painting's alt text (camera, light and focal action for the manifest's
"siblings"), its words with side, and where the doors go; then the building's motifs already used (the
capitalised hook objects, for "used_motifs"), the planned words not yet live, and the open notes in
data/hooks/qa/RECOMMENDED_CHANGES.md that name the building.
"""
import argparse, json, re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOP = set("THE AND WITH FOR FROM ONE TWO HIS HER ITS SAY SAID NOT BUT YOU ARE".split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("building")
    ap.add_argument("--room")
    a = ap.parse_args()
    s = (ROOT / "village" / "data" / f"{a.building}.js").read_text(encoding="utf-8")
    D = json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))
    print(f"# {a.building}: {len(D['rooms'])} rooms, main {D['main']}")
    motifs = Counter()
    live = set()
    for key, R in D["rooms"].items():
        for it in R["items"]:
            live.add(it["id"]); live.add(re.sub(r"_\d+$", "", it["id"]))
            h = re.sub(r'"[^"]*"|“[^”]*”|\([^)]*\)', " ", it.get("hook") or "")  # drop quoted puns and respellings
            say = set(re.findall(r"[A-Z]+", it.get("say") or ""))
            for w in re.findall(r"\b[A-Z]{4,}S?\b", h):
                if w not in STOP and w not in say:
                    motifs[w] += 1
        if a.room and key != a.room:
            continue
        side = lambda it: "C" if it.get("adj") or it.get("adv") else {"f": "L", "m": "R"}.get(it.get("g"), "C")
        words = ", ".join(f"{it.get('lab') or it['fr']}({side(it)}{',verb' if it.get('verb') else ''})" for it in R["items"])
        doors = ", ".join(d.get("to", "?") for d in R.get("doors", [])) + (", map" if R.get("mapExit") else "")
        zooms = ", ".join(z.get("to", "?") for z in R.get("zooms", []))
        print(f"\n## {key}: {R['name']}" + (f" (zoom of {R['parent']})" if R.get("parent") else ""))
        print(f"alt: {(R.get('alt') or '')[:400]}")
        print(f"{len(R['items'])} words: {words}")
        if doors: print(f"doors: {doors}")
        if zooms: print(f"zooms: {zooms}")
    print("\n## motifs already used (hook objects in capitals, most used first)")
    print(", ".join(f"{w.lower()}" + (f" x{n}" if n > 1 else "") for w, n in motifs.most_common(60)))
    plan = []
    rooms = {r["id"]: r for r in json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]}
    bid = D.get("building_id", "")
    for l in (ROOT / "data" / "source" / "vocab.jsonl").read_text(encoding="utf-8").splitlines():
        if not l.strip(): continue
        r = json.loads(l)
        room = rooms.get(r.get("room_id") or "")
        if room and bid and room.get("building_id") == bid and r["id"] not in live:
            plan.append(f"{r['lemma']} ({r.get('cefr', '')}, {room.get('name', room['id'])})")
    print(f"\n## planned words not live yet: {len(plan)}")
    if plan: print(", ".join(plan[:80]) + (" ..." if len(plan) > 80 else ""))
    rc = ROOT / "data" / "hooks" / "qa" / "RECOMMENDED_CHANGES.md"
    if rc.exists():
        notes = [l.strip() for l in rc.read_text(encoding="utf-8").splitlines() if re.search(rf"\b{re.escape(a.building)}\b", l)]
        print(f"\n## open notes naming {a.building} in RECOMMENDED_CHANGES.md: {len(notes)}")
        for n in notes[:20]: print("- " + n[:200].lstrip("-* "))


if __name__ == "__main__":
    main()

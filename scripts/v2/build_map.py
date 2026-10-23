#!/usr/bin/env python3
"""Write village/v2/data/map.js from content/v2/map.json.
A building is clickable ('live') only once village/v2/data/<id>.js exists; until then it shows 'bientôt'."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village" / "v2"
M = json.loads((ROOT / "content" / "v2" / "map.json").read_text(encoding="utf-8"))
def pts(r):
    x, y, w, h = r
    return f"{x},{y} {x+w},{y} {x+w},{y+h} {x},{y+h}"
live, soon = [], []
for b in M["buildings"]:
    if (V2 / "data" / f"{b['id']}.js").exists():
        live.append({"id": b["id"], "name": b["name"], "pts": pts(b["rect"]), "rect": b["rect"], "tag": b["tag"], "door": b["door"]})
    else:
        soon.append({"name": b["name"], "pts": pts(b["rect"]), "rect": b["rect"], "tag": b["tag"]})
for b in M["soon"]:
    soon.append({"name": b["name"], "pts": pts(b["rect"]), "rect": b["rect"], "tag": b["tag"]})
out = {"image": M["image"], "alt": M["alt"], "live": live, "soon": soon}
(V2 / "data" / "map.js").write_text("window.V2_MAP=" + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
print("map: live", [b["id"] for b in live], "soon", len(soon))

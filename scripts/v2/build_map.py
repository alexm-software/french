#!/usr/bin/env python3
"""Write village/v2/data/map.js from content/v2/map.json (shared file; run once, not per building).
map.js lists EVERY building on the painting. The app decides at runtime which are live: a building is
clickable as soon as village/v2/data/<id>.js loads, otherwise it shows 'bientôt'. So shipping a building
never needs this script or map.js to change."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village" / "v2"
M = json.loads((ROOT / "content" / "v2" / "map.json").read_text(encoding="utf-8"))
out = {"image": M["image"], "alt": M["alt"],
       "buildings": [{k: b[k] for k in ("id", "name", "rect", "tag", "door")} for b in M["buildings"]],
       "areas": [{k: b[k] for k in ("name", "rect", "tag")} for b in M["soon"]]}
(V2 / "data" / "map.js").write_text("window.V2_MAP=" + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
print("map: buildings", [b["id"] for b in M["buildings"]], "areas", len(M["soon"]))

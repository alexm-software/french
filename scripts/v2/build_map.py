#!/usr/bin/env python3
"""Write village/data/map.js from content/v2/map.json (shared file; run once, not per building).

map.json = {"world": {image, alt, sectors: [{id, slug, name, rect}]},
            "sectors": {slug: {id, slug, name, image, alt,
                               buildings: [{building_id, name, rect, id?}],
                               streets:   [{id, name, rect}]}}}
It follows the memory-palace registry (data/sectors.json, data/buildings.json): every sector and every
building / ST_ verb street of each sector is painted on that sector's map. Nothing here says which
buildings are live: the app probes village/data/<id>.js for each building at runtime, where
id = building_id without its "Bnn_" prefix (B29_plage -> plage) unless the entry gives a legacy "id"
(B06_marche -> boulangerie, B05_maison's garage -> garage). So shipping a building never needs this
script or map.js to change. Hover tags and door arrows are placed from the rect unless given.
World sectors may also give "en" (English name for the bilingual label) and "poly" (a list of
rings of [x, y] points in the 1280x720 painting): the click area is then the polygon(s), not the rect."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village"
M = json.loads((ROOT / "content" / "v2" / "map.json").read_text(encoding="utf-8"))


def tag(r):  return [r[0] + r[2] // 2, r[1] + min(14, r[3] // 4)]
def door(r): return [r[0] + r[2] // 2, r[1] + r[3] - min(34, r[3] // 3)]


def item(b, keys):
    o = {k: b[k] for k in keys if k in b}
    o.setdefault("tag", tag(b["rect"]))
    return o


W = M["world"]
out = {"world": {"image": W["image"], "alt": W["alt"],
                 "sectors": [dict(item(s, ("id", "slug", "name", "en", "rect", "poly", "tag")), door=s.get("door", door(s["rect"])))
                             for s in W["sectors"]]},
       "sectors": {}}
ids = {}
for w in W["sectors"]:
    S = M["sectors"][w["slug"]]
    bl = []
    for b in S["buildings"]:
        o = item(b, ("building_id", "id", "name", "rect", "tag"))
        o["door"] = b.get("door", door(b["rect"]))
        pid = b.get("id") or re.sub(r"^B\d+_", "", b["building_id"])
        assert pid not in ids, ("duplicate building id", pid)
        ids[pid] = w["slug"]
        bl.append(o)
    for t in S["streets"]:  # verb streets go live as data/<id lowercased>.js (app.js); ids must stay unique too
        assert t["id"].lower() not in ids, ("duplicate street id", t["id"])
        ids[t["id"].lower()] = w["slug"]
    out["sectors"][w["slug"]] = {"id": S["id"], "slug": S["slug"], "name": S["name"], "image": S["image"], "alt": S["alt"],
                                 "buildings": bl, "streets": [item(t, ("id", "name", "rect", "tag")) for t in S["streets"]]}
(V2 / "data" / "map.js").write_text("window.V2_MAP=" + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
print("map: sectors", len(out["sectors"]), "buildings", sum(len(s["buildings"]) for s in out["sectors"].values()), "streets", sum(len(s["streets"]) for s in out["sectors"].values()))

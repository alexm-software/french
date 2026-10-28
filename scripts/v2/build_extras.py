#!/usr/bin/env python3
"""Build the small extra data files the site loads (run after build_v2.py and build_map.py).

  village/data/live.js       window.V2_LIVE = {building id: {building_id, sector_id}} for every built
                             building and street, so the map knows what is open without requesting a
                             data file per planned building (it used to make ~58 failed requests per load).
  village/data/index.js      window.V2_INDEX = [[id, headword, gloss, building, room, cefr, kind], ...]:
                             the search index, also used by review and "also in" (loaded on demand).
  village/data/dialogues.js  window.V2_DIALOGUES = {"building/room": [dialogue, ...]} from
                             data/source/village_dialogues.json, only for rooms that exist, plus the cast.

usage: python3 scripts/v2/build_extras.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "village" / "data"
SKIP = {"map.js", "live.js", "index.js", "dialogues.js"}


def load_payloads():
    out = {}
    for f in sorted(DATA.glob("*.js")):
        if f.name in SKIP:
            continue
        s = f.read_text(encoding="utf-8")
        d = json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))
        out[d["building"]] = d
    return out


def headword(it):
    if it.get("lab"):
        return it["lab"]
    if it.get("verb") or it.get("adj") or it.get("adv"):
        return it["fr"]
    a = it.get("art") or ""
    return ("l'" + it["fr"]) if a == "l'" else (f"{a} {it['fr']}".strip())


def kind(it):
    for k in ("verb", "adj", "adv"):
        if it.get(k):
            return k
    return "noun"


def main():
    P = load_payloads()
    live = {b: {k: d[k] for k in ("building_id", "sector_id") if d.get(k)} for b, d in P.items()}
    index, seen = [], set()
    for b, d in P.items():
        for key, r in d["rooms"].items():
            for it in r["items"]:
                if it.get("noMnemonic") == "alphabet":
                    continue
                k = (it["id"], b, key)
                if k in seen:
                    continue
                seen.add(k)
                en = re.split(r"[;(]", it.get("en") or "")[0].strip()[:60]
                index.append([it["id"], headword(it), en, b, key, it.get("cefr") or "", kind(it)])
    dlg = json.loads((ROOT / "data" / "source" / "village_dialogues.json").read_text(encoding="utf-8"))
    by = {}
    for x in dlg["dialogues"]:
        d = P.get(x["building"])
        if d and x["room"] in d["rooms"]:
            by.setdefault(f'{x["building"]}/{x["room"]}', []).append(
                {k: x[k] for k in ("id", "title", "premise", "cefr", "lines") if k in x})
    w = lambda name, var, obj: (DATA / name).write_text(f"window.{var}=" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    w("live.js", "V2_LIVE", live)
    w("index.js", "V2_INDEX", index)
    w("dialogues.js", "V2_DIALOGUES", {"cast": dlg.get("cast", {}), "rooms": by})
    print(f"live.js: {len(live)} buildings · index.js: {len(index)} entries · dialogues.js: {sum(len(v) for v in by.values())} dialogues in {len(by)} rooms")


if __name__ == "__main__":
    main()

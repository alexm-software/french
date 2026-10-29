#!/usr/bin/env python3
"""Build the small extra data files the site loads (run after build_v2.py and build_map.py).

  village/data/live.js       window.V2_LIVE = {building id: {building_id, sector_id}} for every built
                             building and street, so the map knows what is open without requesting a
                             data file per planned building (it used to make ~58 failed requests per load).
  village/data/index.js      window.V2_INDEX = [[id, headword, gloss, building, room, cefr, kind], ...]:
                             the search index, also used by review and "also in" (loaded on demand).
  village/data/talk/<building>.js  window.V2_TALK[building] = {"building/room": [dialogue, ...]}, with
                             village/data/talk/index.js (V2_TALK_INDEX: the cast and a count per room): the village
                             dialogues (data/source/village_dialogues.json) plus every written conversation in
                             data/source/conversations.json, each placed in the live room that holds most of its
                             words (at least 2). Every line carries "spans" [[start, end, word id], ...] marking the
                             room's words (any form: plural, feminine, conjugated) so the site can link them to cards.
  village/data/listening.js  window.V2_LISTENING = [passage, ...] from data/source/listening.json (paragraphs to
                             listen to, with comprehension questions), each with the room it belongs to.
  village/data/prayers.js    window.V2_PRAYERS = [prayer, ...] from data/source/prayers.json, in book order.

usage: python3 scripts/v2/build_extras.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "village" / "data"
SKIP = {"map.js", "live.js", "index.js", "dialogues.js", "listening.js", "prayers.js"}  # (talk/ is a subfolder, so not globbed)
# Village dialogues whose original room was folded into another when the church was repainted
REHOME = {"eglise/clocher": "eglise/parvis", "eglise/paroisse": "eglise/eglise", "eglise/bricolage": "eglise/eglise"}
LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
PRAYER_ORDER = ["P_signe_croix", "P_notre_pere", "P_ave", "P_gloria_patri", "P_credo", "P_credo_nicee", "P_acte_contrition", "P_confiteor", "P_ange_gardien",
                "P_angelus", "P_regina_caeli", "P_salve_regina", "P_sub_tuum", "P_memorare", "P_saint_michel", "P_actes_foi", "P_actes_esperance",
                "P_actes_charite", "P_benedicite", "P_graces", "P_requiem", "P_agnus", "P_sanctus", "P_magnificat", "P_divine_mercy"]


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
    rooms = {f"{b}/{k}": r for b, d in P.items() for k, r in d["rooms"].items()}
    base = lambda i: re.sub(r"_\d+$", "", i)
    ids = {key: {base(it["id"]) for it in r["items"]} | {it["id"] for it in r["items"]} for key, r in rooms.items()}
    vocab = {}
    for l in (ROOT / "data" / "source" / "vocab.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            v = json.loads(l); vocab[v["id"]] = v

    def forms(it):
        out = {it["fr"]}
        if it.get("plural"):
            out.add(re.sub(r"^(les|des) ", "", it["plural"].split(" (")[0]))
        if it.get("fem"):
            out.add(re.sub(r"^(la|une|l') ?", "", it["fem"]))
        for f in (it.get("forms") or {}).values():
            out.add(f)
        for t in it.get("tenses") or []:
            for row in t.get("rows") or []:
                for f in re.split(r"\s*/\s*", row[-1]):
                    out.add(f)
                    if " " in f:
                        out.add(f.split()[-1])
        if it.get("verb") and it["fr"].startswith(("se ", "s'")):
            out.add(re.sub(r"^(se |s')", "", it["fr"]))
        return {f.strip().lower() for f in out if f and len(f.strip()) > 1}

    def spans(text, words):
        low = text.lower(); taken = []; out = []
        cands = sorted(((f, wid) for wid, fs in words.items() for f in fs), key=lambda x: -len(x[0]))
        for f, wid in cands:
            for m in re.finditer(r"(?<![\w-])" + re.escape(f) + r"(?![\w-])", low):
                a2, b2 = m.span()
                if any(a2 < y and b2 > x for x, y in taken):
                    continue
                taken.append((a2, b2)); out.append([a2, b2, wid])
        return sorted(out)

    def room_words(key, used):
        items = {it["id"]: it for it in rooms[key]["items"] if not it.get("noMnemonic")}
        want = set(used)
        return {wid: forms(it) for wid, it in items.items() if base(wid) in want or wid in want}

    def cefr(used):
        lv = sorted((vocab.get(w, {}).get("cefr") or "A1" for w in used), key=LEVELS.index)
        return lv[len(lv) * 3 // 4] if lv else ""

    def best_room(used):
        w = set(used)
        sc = sorted(((len(w & ids[k]), -len(rooms[k]["items"]), k) for k in rooms), reverse=True)
        return sc[0][2] if sc and sc[0][0] >= 2 else None

    def pack(x, key, used):
        words = room_words(key, used)
        lines = [dict(speaker=l["speaker"], fr=l["fr"], en=l["en"], spans=spans(l["fr"], words)) for l in x["lines"]]
        return dict(id=x["id"], title=x["title"], premise=x.get("premise", ""), cefr=x.get("cefr") or cefr(used), lines=lines)

    dlg = json.loads((ROOT / "data" / "source" / "village_dialogues.json").read_text(encoding="utf-8"))
    by = {}
    for x in dlg["dialogues"]:
        key = REHOME.get(f'{x["building"]}/{x["room"]}', f'{x["building"]}/{x["room"]}')
        used = list(x.get("target_words") or []) + list(x.get("also_uses") or [])
        if key not in rooms:
            key = best_room(used)
        if key:
            by.setdefault(key, []).append(pack(x, key, used))
    conv = json.loads((ROOT / "data" / "source" / "conversations.json").read_text(encoding="utf-8"))["conversations"]
    placed = 0
    for x in conv:
        if x.get("status") != "written" or not x.get("lines"):
            continue
        used = x.get("used_words") or x.get("target_words") or []
        key = best_room(used)
        if key:
            by.setdefault(key, []).append(pack(x, key, used)); placed += 1
    for key in by:
        by[key].sort(key=lambda d: (LEVELS.index(d["cefr"]) if d["cefr"] in LEVELS else 0, d["id"]))
    lis = []
    lp = ROOT / "data" / "source" / "listening.json"
    if lp.exists():
        for x in json.loads(lp.read_text(encoding="utf-8"))["passages"]:
            key = x.get("room") or best_room(x.get("words") or [])
            if key and key not in rooms:
                key = None
            words = room_words(key, x.get("words") or [it["id"] for it in rooms[key]["items"]]) if key else {}
            y = {k: x[k] for k in ("id", "title", "cefr", "fr", "en", "questions") if k in x}
            y["room"] = key; y["spans"] = spans(x["fr"], words)
            lis.append(y)
        lis.sort(key=lambda d: (LEVELS.index(d["cefr"]), d["id"]))
    pr = json.loads((ROOT / "data" / "source" / "prayers.json").read_text(encoding="utf-8"))["prayers"]
    order = {pid: n for n, pid in enumerate(PRAYER_ORDER)}
    pr = sorted(pr, key=lambda x: order.get(x["id"], 99))
    prayers = [{k: x[k] for k in ("id", "title_fr", "title_en", "fr", "en", "source", "lines") if k in x} for x in pr]
    w = lambda name, var, obj: (DATA / name).write_text(f"window.{var}=" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    w("live.js", "V2_LIVE", live)
    w("index.js", "V2_INDEX", index)
    # one small file per building (loaded when a room's conversations open) and a count per room for the menu
    talk = DATA / "talk"; talk.mkdir(exist_ok=True)
    for f in talk.glob("*.js"):
        f.unlink()
    per = {}
    for key, v in by.items():
        per.setdefault(key.split("/")[0], {})[key] = v
    for b, rs in per.items():
        (talk / f"{b}.js").write_text(f"(window.V2_TALK=window.V2_TALK||{{}})[{json.dumps(b)}]=" + json.dumps(rs, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    old = DATA / "dialogues.js"
    if old.exists():
        old.unlink()
    w("talk/index.js", "V2_TALK_INDEX", {"cast": dlg.get("cast", {}), "rooms": {k: len(v) for k, v in by.items()}})
    w("listening.js", "V2_LISTENING", lis)
    w("prayers.js", "V2_PRAYERS", prayers)
    print(f"live.js: {len(live)} buildings · index.js: {len(index)} entries · talk/: {sum(len(v) for v in by.values())} dialogues "
          f"({placed} conversations placed) in {len(by)} rooms · listening.js: {len(lis)} passages · prayers.js: {len(prayers)} prayers")


if __name__ == "__main__":
    main()

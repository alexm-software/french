#!/usr/bin/env python3
"""Dialogue placement and content QA (run by check_v2.py; also standalone).

Reads the built village/data/talk/*.js and their sources (data/source/village_dialogues.json,
data/source/conversations.json) and fails on:
  * an unpinned dialogue in a room that holds fewer than MIN_SHARED (3) of its words. Village dialogues are pinned
    by building/room; a written conversation is pinned by its "room" field ("building/room"; null = no room)
  * a pin to a room that does not exist (the dialogue then drifts by the word rule)
  * adult or medical words (sex, cancer, ultrasound, blood test, drunk, alcohol, cigarettes, weapons, murder...)
    in a children's room: the school, playrooms, toy rooms, the children's workshop, classrooms
  * anything that shows drinking alcohol or smoking, in any room, unless the dialogue id is listed with a reason in
    data/hooks/qa/dialogue_content_ok.tsv (e.g. "drunk with happiness" used figuratively, a doctor telling someone
    to stop smoking)

usage: python3 scripts/qa/dialogue_check.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "village" / "data"
SKIP = {"map.js", "live.js", "index.js", "dialogues.js", "listening.js", "prayers.js"}
REHOME = {"eglise/clocher": "eglise/parvis", "eglise/paroisse": "eglise/eglise", "eglise/bricolage": "eglise/eglise"}  # as build_extras.py
MIN_SHARED = 3
CHILD_BUILDINGS = {"ecole"}
CHILD_NAME = re.compile(r"enfant|children|\bkids?\b|playroom|salle de jeux|game room|games room|jouets|\btoys?\b|classroom|salle de classe|school|école|récré|pupitre", re.I)
ADULT = re.compile(r"\b(sexe|sexuel\w*|sexy|cancer\w*|échographie|ultrasound|accouch\w*|prise de sang|blood test|ivres?|saoule?s?|soûle?s?|bourrée?s?|drunk\w*|alcool\w*|alcohol\w*"
                   r"|bières?|beers?|vins?|wines?|champagne|whisky|vodka|cigarettes?|cigares?|cigars?|fumer|smok(e|es|ing)|tabac|tobacco|drogues?|drugs?"
                   r"|meurtr\w*|murder\w*|tuer|tué\w*|kill\w*|armes?|weapons?|fusils?|pistolets?|guns?|cadavres?|corpses?|suicid\w*)\b", re.I)
DRINK_SMOKE = re.compile(r"\b(ivres?|saoule?s?|soûle?s?|bourrée?s?|drunk\w*|alcool\w*|alcohol\w*|bières?|beers?|whisky|vodka|apéro|apéritif"
                         r"|(bu|boire|boit|bois|verre|bouteille|trop) (de |du |un )?(vin|champagne)|cigarettes?|cigares?|cigars?|fumer|fume\b|fumes\b|smoking|smokes\b|tabac|tobacco)\b", re.I)


def _payload(f):
    s = f.read_text(encoding="utf-8")
    return json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))


def load_ok(p):
    ok = {}
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip() and not l.startswith("#"):
                i, _, why = l.partition("\t")
                if i != "id" and why.strip():
                    ok[i.strip()] = why.strip()
    return ok


def check(errs, warns=None):
    rooms = {}
    for f in sorted(DATA.glob("*.js")):
        if f.name in SKIP:
            continue
        d = _payload(f)
        for k, r in d["rooms"].items():
            rooms[f'{d["building"]}/{k}'] = r
    base = lambda i: re.sub(r"_\d+$", "", i)
    ids = {k: {base(it["id"]) for it in r["items"]} | {it["id"] for it in r["items"]} for k, r in rooms.items()}
    src = {}
    for x in json.loads((ROOT / "data" / "source" / "village_dialogues.json").read_text(encoding="utf-8"))["dialogues"]:
        k = f'{x["building"]}/{x["room"]}'
        src[x["id"]] = (REHOME.get(k, k), list(x.get("target_words") or []) + list(x.get("also_uses") or []))
    for x in json.loads((ROOT / "data" / "source" / "conversations.json").read_text(encoding="utf-8"))["conversations"]:
        pin = x.get("room")
        if pin and REHOME.get(pin, pin) not in rooms:
            errs.append(f"dialogue {x['id']}: pinned to {pin}, which is not a live room")
        src[x["id"]] = (REHOME.get(pin, pin) if pin else None, x.get("used_words") or x.get("target_words") or [])
    for k, _ in {v[0]: 1 for v in src.values() if v[0]}.items():
        if k not in rooms:
            errs.append(f"dialogue pin {k}: not a live room")
    ok = load_ok(ROOT / "data" / "hooks" / "qa" / "dialogue_content_ok.tsv")
    n = 0
    talk = DATA / "talk"
    for f in sorted(talk.glob("*.js")):
        if f.name == "index.js":
            continue
        for key, dl in _payload(f).items():
            nm = (rooms.get(key) or {}).get("name", "")
            child = key.split("/")[0] in CHILD_BUILDINGS or bool(CHILD_NAME.search(nm))
            for x in dl:
                n += 1
                pin, used = src.get(x["id"], (None, []))
                if pin != key:
                    shared = len(set(used) & ids.get(key, set()))
                    if shared < MIN_SHARED:
                        errs.append(f"dialogue {x['id']} ({x['title']}): in {key} on only {shared} shared word(s) and no pin "
                                    f"(pin it with \"room\" in conversations.json, or let it go to no room)")
                text = " ".join([x.get("title", ""), x.get("premise", "")] + [l["fr"] + " " + l["en"] for l in x["lines"]])
                if child:
                    bad = sorted({m.group(0).lower() for m in ADULT.finditer(text)})
                    if bad:
                        errs.append(f"dialogue {x['id']} ({x['title']}): adult/medical words {bad} in the children's room {key} ({nm})")
                ds = sorted({m.group(0).lower() for m in DRINK_SMOKE.finditer(text)})
                if ds and x["id"] not in ok:
                    errs.append(f"dialogue {x['id']} ({x['title']}) in {key}: drinking/smoking words {ds}; rewrite it, or list it with a reason "
                                f"in data/hooks/qa/dialogue_content_ok.tsv if nobody drinks or smokes and nothing glamorizes it")
    stale = sorted(set(ok) - set(src))
    for i in stale:
        (warns if warns is not None else errs).append(f"dialogue_content_ok.tsv: {i} is not a dialogue id")
    return n


def main():
    errs, warns = [], []
    n = check(errs, warns)
    for w in warns:
        print("WARN", w)
    for e in errs:
        print("FAIL", e)
    print(f"dialogues: {n} placed dialogues checked, {len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()

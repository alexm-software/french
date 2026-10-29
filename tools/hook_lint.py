#!/usr/bin/env python3
"""hook_lint.py - mechanical checks on the memory hooks and examples in the built room data.

  python3 tools/hook_lint.py                    # every building; one summary line per check
  python3 tools/hook_lint.py ecole cafe -v      # some buildings, every finding
  python3 tools/hook_lint.py ecole --fail       # findings in these buildings fail (exit 1): use for new or repainted rooms

It does the scriptable half of the hook gate (release-gates reference/item-gates.md, G28); the eye pass
still judges whether the hook object is painted and whether the pun lands. Checks:
  resp      a bracketed respelling in the hook, e.g. "(ak-TU-el)", differs from the card's say line
  english   "Like English" / "Same as English" on a word that vocab.jsonl marks false_cognate
  etym      etymology or template wording: "Linked to", "Think of", Latin, Greek, "root"
  opener    the hook opens with where the word stands ("On the left", "In the middle"...)
  shared    the same first four words open more than 5 hooks
  caps      no word in CAPS (the meaning, or the sound-alike, is written in capitals)
  chunks    a pun of more than two quoted chunks joined by "+"
  example   the example's English contains no word of the card's gloss (often fine: a paraphrase; sometimes a
            different sense from the one the room teaches)
By default every check only reports (the existing hooks are being cleaned up); --fail makes findings in the
named buildings an error.
"""
import argparse, collections, difflib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "village" / "data"
SKIP = {"map.js", "live.js", "index.js", "dialogues.js", "listening.js", "prayers.js"}
RESP = re.compile(r'\(\s*["“]?([A-Za-z][A-Za-z\'’\-]{1,40})["”]?\s*\)')
ETYM = re.compile(r"\b(Linked to|Think of|Latin|Greek|[Rr]oots? (?:of|in|is)|[Ee]tymolog\w*|from the [A-Z][a-z]+ word)")
OPEN = re.compile(r"^(On the (left|right)|In the (middle|centre|center)|Left side|Right side|Standing on the)", re.I)
STOP = set("a an the to of in on and or with for be is are it its his her their at by from as".split())


def norm(s):
    s = re.sub(r"[^a-z]", "", s.lower())
    for a, b in (("oh", "o"), ("ah", "a"), ("ew", "u"), ("ehr", "air"), ("eh", "e"), ("ay", "e"), ("ee", "i"), ("uh", "u"), ("oo", "u"), ("zh", "j")):
        s = s.replace(a, b)
    return s


def load():
    out = []
    for f in sorted(DATA.glob("*.js")):
        if f.name in SKIP:
            continue
        s = f.read_text(encoding="utf-8")
        d = json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))
        for k, r in d["rooms"].items():
            for it in r["items"]:
                if not it.get("noMnemonic"):
                    out.append((d["building"], k, it))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("buildings", nargs="*")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--fail", action="store_true", help="findings in the named buildings fail")
    a = ap.parse_args()
    vocab = {}
    for l in (ROOT / "data" / "source" / "vocab.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            vocab[r["id"]] = r
    items = load()
    openers = collections.Counter()
    for _, _, it in items:
        h = it.get("hook") or ""
        if h:
            openers[" ".join(h.split()[:4]).lower()] += 1
    found = collections.defaultdict(list)
    seen = set()
    for b, k, it in items:
        if a.buildings and b not in a.buildings:
            continue
        if (b, it["id"]) in seen:
            continue
        seen.add((b, it["id"]))
        h, say, where = it.get("hook") or "", it.get("say") or "", f"{b}/{k} {it['id']}"
        add = lambda c, m: found[c].append(f"{where}: {m}")
        if not h:
            continue
        for m in RESP.finditer(h):
            q = m.group(1)
            if re.search(r"[A-Z]{2,}", q) and ("-" in q or q.isupper()) and say and q.count("-") == say.count("-") + say.count(" ") \
               and norm(q) != norm(say) and difflib.SequenceMatcher(None, norm(q), norm(say)).ratio() >= 0.6:
                add("resp", f"hook ({q}) but the card says {say}")
        if re.search(r"\b(Like|Same as) English\b", h) and (vocab.get(re.sub(r"_\d+$", "", it["id"])) or {}).get("cognate_type") == "false_cognate":
            add("english", "'Like English' on a false friend")
        e = ETYM.search(h)
        if e:
            add("etym", f"'{e.group(0)}'")
        if OPEN.search(h):
            add("opener", h[:40])
        o = " ".join(h.split()[:4]).lower()
        if openers[o] > 5 and not o.startswith("monsieur verbe"):
            add("shared", f"'{o}' opens {openers[o]} hooks")
        if not re.search(r"\b[A-Z]{3,}\b", h):
            add("caps", "no word in capitals")
        for m in re.finditer(r'"[^"]+"(?:\s*\+\s*"[^"]+"){2,}', h):
            add("chunks", m.group(0)[:50])
        ex = it.get("ex") or []
        gl = [w for w in re.findall(r"[a-z]+", re.sub(r"\([^)]*\)", "", (it.get("en") or "").lower())) if w not in STOP and len(w) > 2]
        if len(ex) > 1 and gl and not any(re.search(r"\b" + re.escape(w[:max(4, len(w) - 2)]), ex[1].lower()) for w in gl):
            add("example", f"gloss '{', '.join(gl)}' not in '{ex[1][:60]}'")
    total = sum(len(v) for v in found.values())
    for c in ("resp", "english", "etym", "opener", "shared", "caps", "chunks", "example"):
        v = found.get(c, [])
        print(f"{c:8} {len(v)}")
        if a.verbose:
            for x in v:
                print("   ", x)
    print(f"{len(seen)} hooks checked, {total} finding(s)" + ("" if a.verbose or not total else "; -v lists them"))
    sys.exit(1 if (a.fail and a.buildings and total) else 0)


if __name__ == "__main__":
    main()

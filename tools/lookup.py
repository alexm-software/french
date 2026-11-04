#!/usr/bin/env python3
"""Query the source plan without scanning vocab.jsonl or rooms.json.

  python3 tools/lookup.py probleme
  python3 tools/lookup.py --id fr_sauver_verb
  python3 tools/lookup.py --room R_abs_problem_02
  python3 tools/lookup.py --building pompiers --pos noun
  python3 tools/lookup.py --rebuild
  python3 tools/lookup.py --check

Prints one tab-separated line per hit:
  id, headword, pos, gender, cefr, beret, room, building, say, gloss

Backed by data/source/vocab.index.jsonl, data/source/rooms.index.jsonl and
data/source/index.stamp.json. Those files are the plan (vocab.jsonl, rooms.json,
vocab_fixes.json, and conjugation beret where a table exists), not the painted
village. --live reads village/data. A building's hooks.json is applied when
--hook is set, for the hits returned, and is not stored in the index.

Beret codes match scripts/v2/build_v2.py verb_from_vocab: er, ir, re, irregular.
Group-1 non-irregular verbs are er without a table. Other verbs with no table
print gN? (or gN/irr?) instead of a guessed colour. +se means the card is
reflexive; +se? means a pronominal form exists and the example does not use it.
"""
import argparse, hashlib, json, re, sys, unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
import build_v2  # beret / pronominal rules shared with the site build
from unbuilt import live_ids

VOCAB = ROOT / "data" / "source" / "vocab.jsonl"
ROOMS = ROOT / "data" / "source" / "rooms.json"
FIXES = ROOT / "content" / "v2" / "vocab_fixes.json"
CONJ = ROOT / "data" / "cache" / "conjugations.json"
VOCAB_INDEX = ROOT / "data" / "source" / "vocab.index.jsonl"
ROOMS_INDEX = ROOT / "data" / "source" / "rooms.index.jsonl"
STAMP = ROOT / "data" / "source" / "index.stamp.json"
STAMP_KEYS = ("vocab", "fixes", "conj", "rooms")
_CACHE = None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def source_stamp():
    return {key: sha256_file(path) for key, path in (
        ("vocab", VOCAB), ("fixes", FIXES), ("conj", CONJ), ("rooms", ROOMS))}


def stamp_diff(saved, now):
    return [key for key in STAMP_KEYS if saved.get(key) != now.get(key)]


def fold(text):
    text = unicodedata.normalize("NFD", (text or "").casefold())
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def short_gloss(gloss):
    text = (gloss or "").strip()
    text = re.split(r"[;|]", text, maxsplit=1)[0].strip()
    if len(text) > 80:
        text = text[:79].rstrip() + "..."
    return text


def building_slug(building):
    match = re.match(r"B\d+_(.+)", building or "")
    return match.group(1) if match else (building or "")


def building_match(building, query):
    query = (query or "").casefold()
    return query == (building or "").casefold() or query == building_slug(building).casefold()


def compact(row):
    return {key: value for key, value in row.items() if value not in (None, "", False)}


def load_fixes():
    if not FIXES.exists():
        return {}
    return {key: value for key, value in json.loads(FIXES.read_text(encoding="utf-8")).items()
            if not str(key).startswith("_")}


def verb_fields(word):
    """Beret and mirror flags. Colour branches match verb_from_vocab; no tense tables are built."""
    lemma = word.get("lemma") or ""
    group, irregular = word.get("verb_group"), word.get("irregular")
    conj = build_v2.load_conj()
    pronominal = build_v2._clean_pronominal(word.get("pronominal_form")) if word.get("reflexive") and word.get("pronominal_form") else None
    tables = conj.get(pronominal) if pronominal else None
    infinitive = build_v2.verb_infinitive(word, tables if tables is not None else ({} if pronominal else None))
    table = conj.get(infinitive) or conj.get(lemma)
    out = {"verb_group": group}
    if irregular:
        out["irregular"] = True
    if group == 1 and not irregular:
        out["beret"] = "er"
    elif table is None:
        pass
    else:
        try:
            nous = [build_v2._split(cell)[1].removeprefix("nous ") for cell in table.get("present") or [""] * 4][3:4]
            stem = lemma.split("'")[-1].removeprefix("se ")[:-1] + "ssons"
            if group == 2 and not irregular and lemma.endswith("ir") and nous == [stem]:
                out["beret"] = "ir"
            elif group == 3 and build_v2._regular_re(lemma, table):
                out["beret"] = "re"
            else:
                out["beret"] = "irregular"
        except (TypeError, AttributeError, IndexError):
            pass
    if pronominal and infinitive != lemma and str(infinitive).startswith(("se ", "s'")):
        out["reflexive"] = True
    elif word.get("reflexive"):
        out["pronominal"] = True
    return out


def build_records():
    fixes = load_fixes()
    rooms = json.loads(ROOMS.read_text(encoding="utf-8"))["rooms"]
    room_building = {room["id"]: room.get("building_id") for room in rooms if room.get("id")}
    words = []
    seen = set()
    duplicates = []
    with VOCAB.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            word = json.loads(line)
            wid = word.get("id")
            if not wid:
                continue
            if wid in seen:
                duplicates.append(wid)
                continue
            seen.add(wid)
            row = {
                "id": wid,
                "fr": word.get("lemma") or "",
                "pos": word.get("pos") or "",
                "cefr": word.get("cefr") or "",
                "room": word.get("room_id") or "",
                "building": room_building.get(word.get("room_id") or ""),
                "gloss": short_gloss(word.get("gloss")),
                "ipa": word.get("ipa") or "",
                "say": word.get("respelling") or "",
            }
            if word.get("pos") == "noun":
                row["g"] = word.get("gender") or ""
                row["art"] = word.get("article") or ""
            fix = fixes.get(wid) or {}
            if fix.get("fr"):
                row["fr"] = fix["fr"]
            if fix.get("say"):
                row["say"] = fix["say"]
            if fix.get("g") in ("m", "f", "mf"):
                row["g"] = fix["g"]
            if fix.get("art"):
                row["art"] = fix["art"]
            if word.get("pos") == "verb":
                row.update(verb_fields(word))
            words.append(compact(row))
    words.sort(key=lambda row: row["id"])
    room_rows = []
    for room in rooms:
        if not room.get("id"):
            continue
        listed = []
        for wid in room.get("words") or []:
            if wid not in listed:
                listed.append(wid)
        room_rows.append(compact({
            "id": room["id"],
            "name": room.get("name") or "",
            "building": room.get("building_id") or "",
            "sector": room.get("sector_id") or "",
            "kind": room.get("kind") or "",
            "words": listed,
        }))
    room_rows.sort(key=lambda row: row["id"])
    return words, room_rows, duplicates


def write_jsonl(path, rows):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    tmp.replace(path)


def rebuild():
    global _CACHE
    words, rooms, duplicates = build_records()
    write_jsonl(VOCAB_INDEX, words)
    write_jsonl(ROOMS_INDEX, rooms)
    stamp = source_stamp()
    stamp["words"] = len(words)
    stamp["rooms_n"] = len(rooms)
    STAMP.write_text(json.dumps(stamp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _CACHE = (words, rooms)
    return len(words), len(rooms), duplicates


def saved_stamp():
    if not STAMP.exists():
        return {}
    return json.loads(STAMP.read_text(encoding="utf-8"))


def stale_keys():
    if not VOCAB_INDEX.exists() or not ROOMS_INDEX.exists() or not STAMP.exists():
        return list(STAMP_KEYS)
    return stamp_diff(saved_stamp(), source_stamp())


def read_jsonl(path):
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load(force=False):
    global _CACHE
    if _CACHE is not None and not force:
        return _CACHE
    _CACHE = (read_jsonl(VOCAB_INDEX), read_jsonl(ROOMS_INDEX))
    return _CACHE


def text_match(row, terms):
    blob = fold(" ".join(str(row.get(key) or "") for key in ("id", "fr", "gloss", "say")))
    return all(fold(term) in blob for term in terms)


def search(vocab, rooms, *, text=(), ids=(), room=None, building=None, pos=None,
           cefr=None, beret=None, reflexive=False):
    by_id = {row["id"]: row for row in vocab}
    listed = defaultdict(list)
    rooms_by = {}
    for spec in rooms:
        rooms_by[spec["id"]] = spec
        for wid in spec.get("words") or []:
            listed[wid].append(spec["id"])

    def decorate(row, queried=None):
        out = dict(row)
        extra_lists = [rid for rid in listed.get(row["id"], []) if rid != row.get("room")]
        if extra_lists:
            out["listed"] = extra_lists
        if queried and row.get("room") != queried:
            out["via"] = "list"
        elif queried and queried not in (listed.get(row["id"]) or []):
            out["via"] = "vocab"
        return out

    notes = {"missing": [], "extras": [], "room": None, "total": 0}
    if room:
        spec = rooms_by.get(room)
        notes["room"] = spec
        order = list((spec or {}).get("words") or [])
        seen = set(order)
        extras = [row["id"] for row in vocab if row.get("room") == room and row["id"] not in seen]
        notes["extras"] = extras
        chosen = []
        for wid in order + extras:
            row = by_id.get(wid)
            if row is None:
                notes["missing"].append(wid)
                continue
            chosen.append(decorate(row, room))
        notes["total"] = len(chosen)
        return chosen, notes

    chosen = []
    wanted = set(ids)
    for row in vocab:
        if wanted and row["id"] not in wanted:
            continue
        if building and not building_match(row.get("building"), building):
            continue
        if pos and row.get("pos") != pos:
            continue
        if cefr and (row.get("cefr") or "").casefold() != cefr.casefold():
            continue
        if beret and row.get("beret") != beret:
            continue
        if reflexive and not row.get("reflexive"):
            continue
        if text and not text_match(row, text):
            continue
        chosen.append(decorate(row))
    chosen.sort(key=lambda row: row["id"])
    notes["total"] = len(chosen)
    if wanted:
        notes["missing"] = [wid for wid in ids if wid not in by_id]
    return chosen, notes


def beret_mark(row):
    if row.get("beret"):
        mark = row["beret"]
    elif row.get("pos") == "verb":
        mark = "g" + str(row.get("verb_group") if row.get("verb_group") is not None else "?")
        if row.get("irregular"):
            mark += "/irr"
        mark += "?"
    else:
        mark = "-"
    if row.get("reflexive"):
        mark += "+se"
    elif row.get("pronominal"):
        mark += "+se?"
    return mark


def format_row(row):
    def cell(value):
        return str(value or "-").replace("\t", " ").replace("\n", " ")

    parts = [
        row["id"],
        cell(row.get("fr")),
        cell(row.get("pos")),
        cell(row.get("g")),
        cell(row.get("cefr")),
        beret_mark(row),
        cell(row.get("room")),
        cell(row.get("building")),
        cell(row.get("say")),
        cell(row.get("gloss")),
    ]
    line = "\t".join(parts)
    if row.get("via"):
        line += "\tvia:" + row["via"]
    if row.get("listed"):
        line += "\tlisted:" + ",".join(row["listed"])
    if row.get("live"):
        line += "\tlive:" + row["live"]
    if row.get("hook"):
        line += "\thook:" + row["hook"].replace("\t", " ").replace("\n", " ")
    return line


def attach_hooks(rows):
    need = {row["id"] for row in rows}
    found = {}
    if need:
        with VOCAB.open(encoding="utf-8") as handle:
            for line in handle:
                if not need:
                    break
                if '"id"' not in line:
                    continue
                word = json.loads(line)
                if word.get("id") in need:
                    scene = ((word.get("mnemonic_hook") or {}).get("scene") or "").strip()
                    found[word["id"]] = scene[:240]
                    need.remove(word["id"])
    hooks = {}
    for row in rows:
        slug = building_slug(row.get("building"))
        if slug not in hooks:
            path = ROOT / "content" / "v2" / slug / "hooks.json"
            if path.exists():
                hooks[slug] = {key: value for key, value in json.loads(path.read_text(encoding="utf-8")).items()
                               if not str(key).startswith("_")}
            else:
                hooks[slug] = {}
        override = hooks[slug].get(row["id"]) or {}
        if override.get("hook"):
            row["hook"] = str(override["hook"])[:240]
        elif row["id"] in found:
            row["hook"] = found[row["id"]]
        for key in ("fr", "say", "g", "art"):
            if override.get(key):
                row[key] = override[key]


def annotate_live(rows):
    live = live_ids(ROOT)
    for row in rows:
        places = live.get(row["id"]) or []
        row["live"] = ",".join(f"{building}/{room}" for building, room in places) if places else "-"
    return rows


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("text", nargs="*", help="match id, headword, gloss or respelling (accents ignored; all terms required)")
    parser.add_argument("--id", action="append", help="exact word id; repeatable")
    parser.add_argument("--room", help="source room id (rooms.json order, plus vocab room_id extras)")
    parser.add_argument("--building", help="building id (B63_pompiers) or slug (pompiers)")
    parser.add_argument("--pos", help="noun, verb, adj, adv, ...")
    parser.add_argument("--cefr", help="A1..C2")
    parser.add_argument("--beret", choices=("er", "ir", "re", "irregular"), help="confirmed beret only")
    parser.add_argument("--reflexive", action="store_true", help="card uses the pronominal form")
    parser.add_argument("--live", action="store_true", help="append painted village/data locations")
    parser.add_argument("--unbuilt", action="store_true", help="keep hits with no painted location")
    parser.add_argument("--hook", action="store_true", help="append the scene hook, with building hooks.json applied")
    parser.add_argument("--json", action="store_true", help="one JSON object per hit")
    parser.add_argument("--count", action="store_true", help="print the match count only")
    parser.add_argument("--limit", type=int, default=None, help="max lines (default 40, or all for --room/--id)")
    parser.add_argument("--rebuild", action="store_true", help="rewrite the index from vocab, rooms, fixes and conjugations")
    parser.add_argument("--check", action="store_true", help="exit 1 when the committed index does not match its sources")
    parser.add_argument("--no-rebuild", action="store_true", help="do not rewrite a stale index before querying")
    return parser.parse_args(argv)


def main(argv=None):
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    args = parse_args(argv)
    if args.rebuild or (not args.check and not args.no_rebuild and stale_keys()):
        words_n, rooms_n, duplicates = rebuild()
        print(f"rebuilt source index: {words_n} words, {rooms_n} rooms", file=sys.stderr)
        for wid in duplicates:
            print(f"duplicate vocab id: {wid}", file=sys.stderr)
        querying = bool(args.text or args.id or args.room or args.building or args.pos or args.cefr or args.beret or args.reflexive or args.unbuilt or args.count)
        if args.rebuild and not querying and not args.check:
            return 0
    if args.check:
        bad = stale_keys()
        if bad:
            print("vocab index: stale (" + ",".join(bad) + ")", file=sys.stderr)
            return 1
        stamp = saved_stamp()
        print(f"vocab index: fresh ({stamp.get('words', '?')} words, {stamp.get('rooms_n', '?')} rooms)", file=sys.stderr)
        return 0
    if not (args.text or args.id or args.room or args.building or args.pos or args.cefr or args.beret or args.reflexive or args.unbuilt or args.count):
        print("add a query, --id, --room, --building, --pos, --cefr, --beret, or --count", file=sys.stderr)
        return 2
    if not VOCAB_INDEX.exists() or not ROOMS_INDEX.exists():
        print("source index missing; run tools/lookup.py --rebuild", file=sys.stderr)
        return 1
    vocab, rooms = load()
    hits, notes = search(
        vocab, rooms, text=args.text, ids=args.id or [], room=args.room, building=args.building,
        pos=args.pos, cefr=args.cefr, beret=args.beret, reflexive=args.reflexive,
    )
    if args.live or args.unbuilt:
        annotate_live(hits)
        if args.unbuilt:
            hits = [row for row in hits if row.get("live") == "-"]
    total = len(hits)
    unlimited = args.room or args.id
    limit = args.limit if args.limit is not None else (None if unlimited else 40)
    if limit is not None:
        hits = hits[:max(0, limit)]
    if notes.get("room"):
        spec = notes["room"]
        print(f"{spec['id']}\t{spec.get('name', '')}\t{spec.get('building', '')}\t{len(spec.get('words') or [])} listed", file=sys.stderr)
    for wid in notes.get("missing") or []:
        print(f"missing from vocab: {wid}", file=sys.stderr)
    if args.count:
        print(total)
        return 0
    if args.hook and hits:
        attach_hooks(hits)
    for row in hits:
        if args.json:
            print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
        else:
            print(format_row(row))
    shown = len(hits)
    if shown != total:
        print(f"{shown} of {total} hits", file=sys.stderr)
    else:
        print(f"{shown} hits", file=sys.stderr)
    if args.id and notes.get("missing"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

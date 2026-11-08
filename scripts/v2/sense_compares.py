#!/usr/bin/env python3
"""Sense comparisons: same or near-shared English gloss, different French use.

Canonical learner text and provenance live in data/source/sense_compares.json.
build_v2.attach copies only the learner fields onto each card. Source URLs stay
in that file and never go on the card.

A painted counterpart is {"at": [building, room]} and the card links to the
existing word route (#/building/room?w=id). An unpainted counterpart is
{"at": null}; the card names it and says it is not in a room yet.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "source" / "sense_compares.json"
LAYOUTS = ROOT / "content" / "v2"
VILLAGE = ROOT / "village" / "data"


def load_edges(path=None):
    doc = json.loads((path or DATA).read_text(encoding="utf-8"))
    return doc["edges"]


def headword_of(w):
    """Article plus noun when the source has an article. Other classes stay the lemma."""
    lem = w.get("lemma") or ""
    art = w.get("article") or ""
    if w.get("pos") == "noun" and art:
        return ("l'" + lem) if art == "l'" else f"{art} {lem}"
    return lem


def labeled_examples(edge, vocab):
    out = []
    for side, key in (("a", "a_ex"), ("b", "b_ex")):
        ex = edge.get(key)
        if ex:
            out.append({"who": headword_of(vocab[edge[side]]), "fr": ex[0], "en": ex[1]})
    return out


def compares_index(edges=None, vocab=None):
    """id -> list of learner-facing pointers. Sources and excerpts stay off the card."""
    edges = edges if edges is not None else load_edges()
    vocab = vocab if vocab is not None else load_vocab()
    out = defaultdict(list)
    for e in edges:
        examples = labeled_examples(e, vocab)
        out[e["a"]].append(_pointer(e["b"], e["a_note"], examples, vocab))
        out[e["b"]].append(_pointer(e["a"], e["b_note"], examples, vocab))
    for wid in out:
        out[wid].sort(key=lambda row: row["to"])
    return out


def _pointer(to, note, examples, vocab):
    row = {"to": to, "note": note, "hw": headword_of(vocab[to])}
    if examples:
        row["examples"] = examples
    return row


def load_vocab():
    vocab = {}
    with open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                w = json.loads(line)
                vocab[w["id"]] = w
    return vocab


def load_placements(layouts=None):
    """id -> list of {building, room, room_id} for words painted in a layout.

    Only buildings that already have a village payload are locations the card
    can open. A layout with no payload is not invented as a room.
    """
    places = defaultdict(list)
    root = layouts or LAYOUTS
    for layout in sorted(root.glob("*/layout.json")):
        building = layout.parent.name
        if not (VILLAGE / f"{building}.js").exists():
            continue
        data = json.loads(layout.read_text(encoding="utf-8"))
        for room_key, room in data.get("rooms", {}).items():
            for it in room.get("items") or []:
                wid = it.get("id")
                if not wid:
                    continue
                places[wid].append({
                    "building": building,
                    "room": room_key,
                    "room_id": room.get("room_id"),
                })
    return places


def choose_placement(wid, placements, vocab):
    opts = placements.get(wid) or []
    if not opts:
        return None
    want = (vocab.get(wid) or {}).get("room_id")
    if want:
        for opt in opts:
            if opt.get("room_id") == want:
                return [opt["building"], opt["room"]]
    opt = sorted(opts, key=lambda o: (o["building"], o["room"]))[0]
    return [opt["building"], opt["room"]]


def attach_compares(it, vocab, placements, index=None):
    """Add it['compares'] from the canonical edges. Leaves every other field."""
    index = index if index is not None else compares_index()
    rows = index.get(it.get("id"))
    if not rows:
        return it
    out = []
    for row in rows:
        target = vocab.get(row["to"])
        if not target:
            raise SystemExit(f"sense compare target missing from vocab: {row['to']}")
        item = {
            "to": row["to"],
            "fr": target["lemma"],
            "hw": row.get("hw") or headword_of(target),
            "en": target.get("gloss") or "",
            "note": row["note"],
            "at": choose_placement(row["to"], placements, vocab),
        }
        if item["at"] is None:
            item["lex"] = True
        if row.get("examples"):
            item["examples"] = row["examples"]
        out.append(item)
    it["compares"] = out
    return it


def validate(vocab=None, edges=None):
    """Return a list of problems. Empty means the authored file is usable."""
    vocab = vocab if vocab is not None else load_vocab()
    edges = edges if edges is not None else load_edges()
    problems = []
    seen = set()
    for i, e in enumerate(edges):
        a, b = e.get("a"), e.get("b")
        where = f"edge {i} {a} / {b}"
        if not a or not b:
            problems.append(f"{where}: missing endpoint")
            continue
        if a == b:
            problems.append(f"{where}: self reference")
        key = tuple(sorted((a, b)))
        if key in seen:
            problems.append(f"{where}: duplicate pair")
        seen.add(key)
        for wid in (a, b):
            if wid not in vocab:
                problems.append(f"{where}: unknown id {wid}")
        for side, note_key, ex_key in (("a", "a_note", "a_ex"), ("b", "b_note", "b_ex")):
            note = e.get(note_key) or ""
            if not note.strip():
                problems.append(f"{where}: empty {note_key}")
            if "http://" in note or "https://" in note:
                problems.append(f"{where}: {note_key} contains a URL")
            other = vocab.get(e["b" if side == "a" else "a"])
            if other and other["lemma"].lower() not in note.lower():
                problems.append(f"{where}: {note_key} does not name {other['lemma']}")
            ex = e.get(ex_key)
            if ex is not None and (not isinstance(ex, list) or len(ex) != 2 or not all(isinstance(x, str) and x.strip() for x in ex)):
                problems.append(f"{where}: {ex_key} must be [french, english]")
        sources = e.get("sources") or []
        if len(sources) < 1 or not all(isinstance(s, str) and s.startswith("https://") for s in sources):
            problems.append(f"{where}: sources must be https URLs")
        if e.get("verified"):
            support = e.get("support") or []
            if not support:
                problems.append(f"{where}: verified edge needs a support excerpt")
            for s in support:
                if not (isinstance(s, dict) and str(s.get("url", "")).startswith("https://") and str(s.get("excerpt", "")).strip()):
                    problems.append(f"{where}: support needs an https url and an excerpt")
        elif e.get("verified") is not False:
            problems.append(f"{where}: verified must be true or false")
        axes = e.get("axes") or []
        if not axes:
            problems.append(f"{where}: axes required")
    return problems


def verb_marker(w):
    """Same beret rules as a painted verb card. Never treat every verb as irregular."""
    try:
        from build_v2 import verb_from_vocab
        card = verb_from_vocab(w)
        return card["group"], card["beret"]
    except SystemExit:
        grp, irr = w.get("verb_group"), bool(w.get("irregular"))
        if grp == 1 and not irr:
            return "-er", "red"
        if grp == 2 and not irr:
            return "-ir", "green"
        if grp == 3 and not irr:
            return "-re", "purple"
        return "irregular", "gold"


def _lex_item(w, vocab, placements, index):
    """Source text for a word that has no painting. No room, no image, no unchecked hook."""
    pos = w.get("pos")
    it = {
        "id": w["id"], "lex": True, "fr": w["lemma"],
        "en": w.get("gloss") or "", "ipa": w.get("ipa") or "", "say": w.get("respelling") or "",
        "cefr": w.get("cefr") or "",
        "ex": [w.get("example_fr") or "", w.get("example_en") or ""],
        # Source mnemonic scenes were written for a painting. A text card has no accepted hook.
        "noMnemonic": True,
    }
    if w.get("usage_warning"):
        it["note"] = w["usage_warning"]
    if pos == "verb":
        group, beret = verb_marker(w)
        it.update(verb=True, group=group, beret=beret)
    elif pos == "adj":
        it.update(adj=True, invariable=True)
    elif pos == "noun":
        g = w.get("gender") or "m"
        art = w.get("article") or ("la" if g == "f" else "le")
        it.update(g=g, art=art, ind={"f": "une", "m": "un", "mf": "un/une"}.get(g, "un"))
    else:
        it.update(adv=True, gramLine={
            "adv": "adverb · invariable", "prep": "preposition · invariable",
            "pron": "pronoun", "conj": "conjunction · invariable", "det": "determiner",
            "num": "number · invariable", "intj": "interjection · invariable",
            "phrase": "phrase · fixed expression", "idiom": "idiom · fixed expression",
        }.get(pos, pos or "word"))
    return attach_compares(it, vocab, placements, index)


def write_lexicon(vocab=None, placements=None, index=None):
    """Text cards for compare-words that are not painted. Search and the other card open them."""
    vocab = vocab if vocab is not None else load_vocab()
    placements = placements if placements is not None else load_placements()
    index = index if index is not None else compares_index(load_edges(), vocab)
    ids = set()
    for wid, rows in index.items():
        if choose_placement(wid, placements, vocab) is None:
            ids.add(wid)
        for row in rows:
            if choose_placement(row["to"], placements, vocab) is None:
                ids.add(row["to"])
    items = {}
    rows = []
    for wid in sorted(ids):
        w = vocab[wid]
        it = _lex_item(w, vocab, placements, index)
        items[wid] = it
        kind = "verb" if it.get("verb") else "adj" if it.get("adj") else "adv" if it.get("adv") else "noun"
        rows.append([wid, it.get("hw") or headword_of(w), (it.get("en") or "")[:60], "lex", "lex", it.get("cefr") or "", kind])
    path = ROOT / "village" / "data" / "lexicon.js"
    path.write_text("window.V2_LEXICON=" + json.dumps(items, ensure_ascii=False, separators=(",", ":"))
                    + ";\nwindow.V2_LEXICON_INDEX=" + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n",
                    encoding="utf-8")
    return len(items)


if __name__ == "__main__":
    vocab = load_vocab()
    problems = validate(vocab)
    if problems:
        print("\n".join(problems))
        raise SystemExit(f"{len(problems)} problem(s)")
    idx = compares_index()
    print(f"{len(load_edges())} edges, {len(idx)} words")

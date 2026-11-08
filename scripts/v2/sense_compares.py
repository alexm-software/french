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


def compares_index(edges=None):
    """id -> list of learner-facing pointers, sources stripped."""
    out = defaultdict(list)
    for e in edges if edges is not None else load_edges():
        out[e["a"]].append(_pointer(e["b"], e["a_note"], e.get("a_ex")))
        out[e["b"]].append(_pointer(e["a"], e["b_note"], e.get("b_ex")))
    for wid in out:
        out[wid].sort(key=lambda row: row["to"])
    return out


def _pointer(to, note, ex):
    row = {"to": to, "note": note}
    if ex:
        row["ex"] = list(ex)
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
            "en": target.get("gloss") or "",
            "note": row["note"],
            "at": choose_placement(row["to"], placements, vocab),
        }
        if row.get("ex"):
            item["ex"] = list(row["ex"])
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
        axes = e.get("axes") or []
        if not axes:
            problems.append(f"{where}: axes required")
    return problems


if __name__ == "__main__":
    vocab = load_vocab()
    problems = validate(vocab)
    if problems:
        print("\n".join(problems))
        raise SystemExit(f"{len(problems)} problem(s)")
    idx = compares_index()
    print(f"{len(load_edges())} edges, {len(idx)} words")

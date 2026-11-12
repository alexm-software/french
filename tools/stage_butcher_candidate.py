#!/usr/bin/env python3
"""Build the upstairs butcher as a candidate dataset.

Reads the live boulangerie layout and does not write it back. The candidate
room is the accepted upstairs painting plus its nine words. The downstairs
shop is not given a return door: that stair is not painted.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
sys.path.insert(0, str(ROOT / "skills" / "memory-palace-builder" / "scripts"))
import build_v2 as B  # noqa: E402

TRIAL = ROOT / "docs" / "room-trials" / "boucherie-surfaces"
NINE = [
    "fr_boucherie_noun",
    "fr_crevette_noun",
    "fr_huitre_noun",
    "fr_ecaille_noun",
    "fr_abattoir_noun",
    "fr_steak_noun",
    "fr_charcutier_noun",
    "fr_requin_noun",
    "fr_mangeur_noun",
]


def production_layout():
    return json.loads((ROOT / "content" / "v2" / "boulangerie" / "layout.json").read_text(encoding="utf-8"))


def draft_room():
    return json.loads((TRIAL / "room-draft.json").read_text(encoding="utf-8"))


def draft_hooks():
    raw = json.loads((TRIAL / "hooks.json").read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def assemble_room(vocab, v1, fixes, overrides, spec, img):
    """Same item path as scripts/v2/build_v2.py, for this one room."""
    items = []
    for row in spec["items"]:
        wid = row["id"]
        if wid in v1 and row.get("text") != "vocab":
            it = {k: v for k, v in v1[wid].items() if k not in ("img", "box", "label", "side", "surface", "cardSrc")}
        elif wid in vocab:
            it = B.item_from_vocab(vocab[wid])
        else:
            raise SystemExit(f"unknown word id {wid}")
        fix = dict(fixes.get(wid, {}))
        fix.update({k: v for k, v in overrides.get(wid, {}).items() if k in ("art", "g")})
        B.apply_grammar_fix(it, fix)
        for src in (fixes.get(wid, {}), overrides.get(wid, {})):
            if src.get("fr"):
                it["fr"] = src["fr"]
        it["_hw"] = B.headword(it)
        it["box"] = list(row["box"])
        for src in (fixes.get(wid, {}), overrides.get(wid, {})):
            for k in ("say", "f_say", "hook", "en"):
                if src.get(k):
                    it[k] = src[k]
            if "plural" in src:
                it["plural"] = src["plural"]
            if "note" in src:
                it["note"] = src["note"]
            if src.get("ex"):
                it["ex"] = list(src["ex"])
        if not it.get("cefr") and vocab.get(wid, {}).get("cefr"):
            it["cefr"] = vocab[wid]["cefr"]
        ph = B.expressions(vocab).get(wid) or B.expressions(vocab).get(re.sub(r"_\d+$", "", wid))
        if ph:
            it["phrases"] = ph
        if overrides.get(wid, {}).get("plaque") is True:
            it["plaque"] = True
        items.append(it)
    room = {
        "name": spec["name"],
        "image": spec["image"],
        "alt": spec["alt"],
        "nameplate": spec["nameplate"],
        "backTo": spec["backTo"],
        "doors": [dict(d) for d in spec["doors"]],
        "zooms": [],
        "items": items,
    }
    B.place_labels(room)
    out_items = []
    for it in items:
        x, y, w, h = it["box"]
        r = it["_lab"]
        card = f"boulangerie/cards/{it['id']}.webp"
        o = {k: v for k, v in it.items() if not k.startswith("_")}
        o.update({
            "box": [round(x / 12.8, 4), round(y / 7.2, 4), round(w / 12.8, 4), round(h / 7.2, 4)],
            "label": [round((r[0] + r[2] / 2) / 12.8, 4), round(r[1] / 7.2, 4)],
            "labelPx": [round(v, 1) for v in r],
            "boxPx": it["box"],
            "side": B.side_of(it),
            "cardSrc": card,
        })
        out_items.append(o)
    built = {k: v for k, v in room.items() if k != "items"}
    built["items"] = out_items
    for door in built["doors"]:
        door.setdefault("thumb", "boulangerie/boucherie.jpg")
    built.setdefault("parent", None)
    return built, img


def build_candidate(dest=None, write_cards=False):
    spec = draft_room()
    if set(row["id"] for row in spec["items"]) != set(NINE) or len(spec["items"]) != len(NINE):
        raise SystemExit("room draft is not exactly the nine source words")
    vocab, v1 = B.load_vocab(), B.load_v1_items()
    fixes_path = ROOT / "content" / "v2" / "vocab_fixes.json"
    fixes = json.loads(fixes_path.read_text(encoding="utf-8")) if fixes_path.exists() else {}
    fixes = {k: v for k, v in fixes.items() if not k.startswith("_")}
    overrides = draft_hooks()
    from PIL import Image
    img = Image.open(ROOT / "village" / spec["image"]).convert("RGB")
    if img.size != (B.W, B.H):
        raise SystemExit(f"staged image is {img.size}")
    built, img = assemble_room(vocab, v1, fixes, overrides, spec, img)
    if dest and write_cards:
        for it in built["items"]:
            B.card_crop(img, it["boxPx"], dest / "cards" / f"{it['id']}.webp")
    return built


def main():
    dest = TRIAL / "candidate"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "cards").mkdir(exist_ok=True)
    built = build_candidate(dest, write_cards=True)
    (dest / "room.json").write_text(json.dumps(built, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    links = {
        "down": {
            "from": "boucherie_etage",
            "to": "boucherie",
            "painted": True,
            "image": "boulangerie/boucherie_etage.jpg",
            "hit": built["doors"][0]["hit"],
            "thumb": "boulangerie/boucherie.jpg",
        },
        "up": {
            "from": "boucherie",
            "to": "boucherie_etage",
            "painted": False,
            "reason": "No return stair is painted on the live shop. No hit is invented on open floor.",
        },
        "passage": {
            "kind": "stair",
            "upstairs": "centre floor hatch, steps down",
            "downstairs": "ceiling hatch behind the butcher, steps up",
            "arrival_down": "a counter worker in a striped apron and white cap, a different employee from the red-apron butcher",
            "arrival_up": "pale blue-grey wall and grey stone floor of the accepted upstairs room",
        },
    }
    (dest / "links.json").write_text(json.dumps(links, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"candidate room: {len(built['items'])} words, plaque={next(i['id'] for i in built['items'] if i.get('plaque'))}")


if __name__ == "__main__":
    main()

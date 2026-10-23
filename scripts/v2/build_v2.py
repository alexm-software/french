#!/usr/bin/env python3
"""Build the v2 village (village/v2/) from the SAME text metadata as v1.

Card text (French word, article, gloss, IPA, respelling, memory hook, example, plural,
notes, verb tables) is read, never rewritten, from:
  1. the live v1 payloads village/assets/data/<building>.js (items matched by id), else
  2. data/source/vocab.jsonl (+ data/source/rooms.json for planned room membership).
A layout entry may set "text": "vocab" to use data/source/vocab.jsonl instead of the v1 payload
(e.g. v1's « le banc » hook is a piggy bank; the source hook is a pew/bench).
v2-specific inputs live in content/v2/<building>/:
  layout.json  painting, hotspot box (1280x720 px), optional "labelAt" [cx, top] px,
               doors, map exit and zooms. Labels are otherwise placed automatically.
  hooks.json   optional {word_id: {"hook": ..., "why": ...}} overrides, used ONLY where the
               v1 hook breaks the content rules or cannot be painted; the painting must show
               the override hook. v1 data is never edited.
Everything is checked by scripts/qa/check_v2.py.

usage: python3 scripts/v2/build_v2.py [building ...]   (default: every content/v2/*/layout.json)
"""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "village" / "v2"
W, H = 1280, 720
FONT = None
for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]:
    if Path(p).exists():
        FONT = ImageFont.truetype(p, 17)
LAB_H = 29


def label_w(text):
    if FONT:
        return int(FONT.getlength(text)) + 22
    return int(len(text) * 9.5) + 22


def load_v1_items():
    items = {}
    for js in sorted((ROOT / "village" / "assets" / "data").glob("*.js")):
        src = js.read_text(encoding="utf-8")
        m = re.search(r"=\s*(\{.*\})\s*;?\s*$", src, re.S)
        if not m:
            continue
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for room in (data.get("rooms") or {}).values():
            for it in room.get("items") or []:
                if it.get("id"):
                    items.setdefault(it["id"], it)
    return items


def load_vocab():
    out = {}
    with open(ROOT / "data" / "source" / "vocab.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                w = json.loads(line)
                out[w["id"]] = w
    return out


def plural_of(w):
    if w.get("plural_irregular"):
        return w["plural_irregular"] if w["plural_irregular"].startswith("les ") else "les " + w["plural_irregular"]
    lem = w["lemma"]
    if " " in lem:  # compound: pluralise the head noun only
        head, rest = lem.split(" ", 1)
        return "les " + (head if head[-1] in "sxz" else head + "s") + " " + rest
    return "les " + (lem if lem[-1] in "sxz" else lem + "s")


def item_from_vocab(w):
    g = w.get("gender")
    art = w.get("article") or ("la" if g == "f" else "le")
    ind = {"f": "une", "m": "un", "mf": "un/une"}.get(g, "un")
    hook = (w.get("mnemonic_hook") or {}).get("scene") or ""
    hook = re.sub(r"^Reverent:\s*", "", hook)
    hook = hook[:1].upper() + hook[1:]
    note = w.get("gender_note") or w.get("false_cognate_note") or w.get("usage_warning")
    return {
        "id": w["id"], "fr": w["lemma"], "art": art, "ind": ind, "g": g,
        "en": w.get("gloss", ""), "ipa": w.get("ipa", ""), "say": w.get("respelling", ""),
        "plural": plural_of(w), "hook": hook, "note": note,
        "ex": [w.get("example_fr", ""), w.get("example_en", "")],
    }


def headword(it):
    if it.get("verb"):
        return it["fr"]
    a = it.get("art")
    return ("l'" + it["fr"]) if a == "l'" else f"{a} {it['fr']}"


def side_of(it):
    return {"f": "L", "m": "R"}.get(it.get("g"), "C")


def inter(a, b, pad=0):
    return a[0] < b[0] + b[2] + pad and b[0] < a[0] + a[2] + pad and a[1] < b[1] + b[3] + pad and b[1] < a[1] + a[3] + pad


def ov_area(a, b):
    x = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    y = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return x * y


def badge_rect(z):
    w = label_w("🔍 " + z["label"]) + 6
    return [z["at"][0] - w / 2, z["at"][1] - 17, w, 34]


def nameplate_rect(room):
    if not room.get("nameplate"):
        return None
    w = int(FONT.getlength(room["name"]) * 24 / 17) + 56 if FONT else len(room["name"]) * 14 + 56
    cx, cy = room["nameplate"][0] * W / 100, room["nameplate"][1] * H / 100
    return [cx - w / 2, cy - 22, w, 44]


def place_labels(room):
    """Choose a label rectangle for each item: below, above, inside-bottom or inside-top of its box,
    avoiding other labels, other hotspots, doors, the map exit, zoom badges and the nameplate."""
    fixed = []
    for d in room.get("doors", []):
        fixed.append(d["hit"])
    if room.get("mapExit"):
        fixed.append(room["mapExit"]["box"])
    for z in room.get("zooms", []):
        fixed.append(badge_rect(z))
    np_ = nameplate_rect(room)
    if np_:
        fixed.append(np_)
    placed = []
    boxes = [it["box"] for it in room["items"]]
    for i, it in enumerate(room["items"]):
        x, y, w, h = it["box"]
        lw = label_w(it["_hw"])
        if it.get("_labelAt"):
            # manual placement from layout.json: "labelAt": [centre_x_px, top_px]
            c, t = it["_labelAt"]
            best = [c - lw / 2, t, lw, LAB_H]
            placed.append(best)
            it["_lab"] = best
            continue
        cx = x + w / 2
        cands = []
        for top in (y + h + 4, y - LAB_H - 4, y + h - LAB_H - 4, y + 4, y + h / 2 - LAB_H / 2):
            for dx in (0, -0.3, 0.3):
                c = min(max(cx + dx * w, lw / 2 + 2), W - lw / 2 - 2)
                t = min(max(top, 2), H - LAB_H - 2)
                cands.append([c - lw / 2, t, lw, LAB_H])
        best, bestscore = None, None
        for r in cands:
            score = 0
            for p in placed:
                score += 1000 * ov_area(r, p)
            for f in fixed:
                score += 1000 * ov_area(r, f)
            for j, b in enumerate(boxes):
                if j != i:
                    score += ov_area(r, b)
            if bestscore is None or score < bestscore:
                best, bestscore = r, score
            if score == 0:
                break
        placed.append(best)
        it["_lab"] = best
    return placed


def card_crop(img, box, out):
    x, y, w, h = box
    s = max(w, h) * 1.18
    cx, cy = x + w / 2, y + h / 2
    l, t = max(0, cx - s / 2), max(0, cy - s / 2)
    r, b = min(W, l + s), min(H, t + s)
    l, t = max(0, r - s), max(0, b - s)
    c = img.crop((int(l), int(t), int(r), int(b)))
    c.thumbnail((420, 420), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    c.save(out, "WEBP", quality=84)


def build(bld, v1, vocab):
    L = json.loads((ROOT / "content" / "v2" / bld / "layout.json").read_text(encoding="utf-8"))
    # v2 hook overrides (content/v2/<bld>/hooks.json): {word_id: {"hook": ..., "why": ...}}
    # used where the v1 hook breaks the content rules or does not match the painting; v1 data is never edited.
    hp = ROOT / "content" / "v2" / bld / "hooks.json"
    overrides = json.loads(hp.read_text(encoding="utf-8")) if hp.exists() else {}
    overrides = {k: v for k, v in overrides.items() if not k.startswith("_")}
    out_rooms = {}
    for key, room in L["rooms"].items():
        img = Image.open(V2 / room["image"]).convert("RGB")
        assert img.size == (W, H), (bld, key, img.size)
        items = []
        for spec in room["items"]:
            wid = spec["id"]
            if wid in v1 and spec.get("text") != "vocab":
                it = {k: v for k, v in v1[wid].items() if k not in ("img", "box", "label", "side", "surface", "cardSrc")}
            elif wid in vocab:
                it = item_from_vocab(vocab[wid])
            else:
                raise SystemExit(f"{bld}/{key}: unknown word id {wid}")
            it["_hw"] = headword(it)
            it["box"] = spec["box"]
            if wid in overrides:
                it["hook"] = overrides[wid]["hook"]
            if spec.get("labelAt"):
                it["_labelAt"] = spec["labelAt"]
            if spec.get("scene"):
                it["scene"] = spec["scene"]
            items.append(it)
        room = dict(room, items=items)
        place_labels(room)
        out_items = []
        for it in items:
            x, y, w, h = it["box"]
            r = it["_lab"]
            card = f"{bld}/cards/{it['id']}.webp"
            card_crop(img, it["box"], V2 / card)
            o = {k: v for k, v in it.items() if not k.startswith("_")}
            o.update({
                "box": [round(x / 12.8, 4), round(y / 7.2, 4), round(w / 12.8, 4), round(h / 7.2, 4)],
                "label": [round((r[0] + r[2] / 2) / 12.8, 4), round(r[1] / 7.2, 4)],
                "labelPx": [round(v, 1) for v in r],
                "boxPx": it["box"], "side": side_of(it), "cardSrc": card,
            })
            out_items.append(o)
        r2 = {k: v for k, v in room.items() if k != "items"}
        r2["items"] = out_items
        for d in r2.get("doors", []):
            d.setdefault("thumb", L["rooms"][d["to"]]["image"])
        r2.setdefault("parent", None)
        if r2.get("mapExit"):
            b = r2["mapExit"]["box"]
            r2["mapExit"] = dict(r2["mapExit"], boxPx=b, box=[round(b[0] / 12.8, 4), round(b[1] / 7.2, 4), round(b[2] / 12.8, 4), round(b[3] / 7.2, 4)])
        out_rooms[key] = r2
    payload = {"building": bld, "name": L["name"], "main": L["main"], "roomList": L["roomList"], "rooms": out_rooms}
    js = "(window.VILLAGE_DATA=window.VILLAGE_DATA||{})[" + json.dumps(bld) + "]=" + json.dumps(payload, ensure_ascii=False) + ";\n"
    (V2 / "data").mkdir(parents=True, exist_ok=True)
    (V2 / "data" / f"{bld}.js").write_text(js, encoding="utf-8")
    n = sum(len(r["items"]) for r in out_rooms.values())
    print(f"built {bld}: {len(out_rooms)} rooms, {n} words")


def main():
    blds = sys.argv[1:] or sorted(p.parent.name for p in (ROOT / "content" / "v2").glob("*/layout.json"))
    v1, vocab = load_v1_items(), load_vocab()
    for b in blds:
        build(b, v1, vocab)
    unused = []
    for b in blds:
        hp = ROOT / "content" / "v2" / b / "hooks.json"
        if hp.exists():
            ids = {i["id"] for r in json.loads((ROOT / "content" / "v2" / b / "layout.json").read_text(encoding="utf-8"))["rooms"].values() for i in r["items"]}
            unused += [f"{b}:{k}" for k in json.loads(hp.read_text(encoding="utf-8")) if not k.startswith("_") and k not in ids]
    if unused:
        raise SystemExit("hooks.json ids not in layout: " + ", ".join(unused))


if __name__ == "__main__":
    main()

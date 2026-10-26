#!/usr/bin/env python3
"""precheck.py - cheap automated checks BEFORE any visual review of a room painting.

  python3 precheck.py IMAGE [--manifest m.json] [--data village/data/X.js --room KEY|R_id] [--json out.json]
  python3 precheck.py --data village/data/ecole.js --room cantine      # IMAGE defaults to the room's live image

Checks (FAIL = must fix before review, WARN = look at it, FLAG = a human decides; never auto-rejects):
  size    image is exactly 1280x720                                                   FAIL
  ocr     confident text runs tesseract finds (box, conf; tiled, see ocr()); digits are called out because a
          painted digit can break a count; text declared in the manifest is marked so   FLAG
  labels  from the built room data, mirroring scripts/qa/check_v2.py + build_v2.py:
          out of bounds, hotspot/hotspot and label/label overlap, label or hotspot over a
          door hit / mapExit boxPx / zoom badge / nameplate                            FAIL
          label touches another hotspot; labels within 3 px (strict "touching" grow);
          label closer than 8 px to the scene edge; label detached from its own box;
          adjective/adverb box centre outside the 30-70 % band                        WARN
  manifest  every room word is in the manifest and vice versa; each entry says what is
          shown + pose/action; numbers carry an exact count; verbs say what they act on;
          sensitive treatment stated; doors/exits listed; thin (one-object) zooms;
          prompt gate: scene_situation, interactions (2+ per group), siblings, used_motifs,
          prompt_text with every template section, no unfilled {field}, every item named FAIL
          a word in no interaction group (isolated figure)                              WARN
Exit code 1 if any FAIL, else 0.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path
from PIL import Image, ImageFont

W, H = 1280, 720
GROW = 3   # check_v2 --strict: "touching" = closer than this (px)
EDGE = 8   # check_v2 --strict: min clear gap label <-> scene edge (px)
PROMPT_SECTIONS = ("IMAGE", "STYLE", "LIGHT AND COLOUR", "SETTING", "SITUATION", "COMPOSITION", "ITEMS", "PLACEMENT AND SPACING",
                   "DOORS AND EXITS", "GROUNDING AND ANATOMY", "FIGURES", "TEXT", "CONTENT", "VARIETY", "AVOID")
DETACH = 12  # build_v2 places labels 4 px off their box; farther than this = detached (manual labelAt?)
FONT = None
for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]:
    if Path(p).exists():
        FONT = ImageFont.truetype(p, 17)


def label_w(t):  # build_v2.label_w
    return int(FONT.getlength(t)) + 22 if FONT else int(len(t) * 9.5) + 22


def badge_rect(z):  # build_v2.badge_rect (what place_labels avoids)
    w = label_w("🔍 " + z["label"]) + 6
    return [z["at"][0] - w / 2, z["at"][1] - 17, w, 34]


def nameplate_rect(R):  # build_v2.nameplate_rect
    if not R.get("nameplate"):
        return None
    w = int(FONT.getlength(R["name"]) * 24 / 17) + 56 if FONT else len(R["name"]) * 14 + 56
    cx, cy = R["nameplate"][0] * W / 100, R["nameplate"][1] * H / 100
    return [cx - w / 2, cy - 22, w, 44]


def inter(a, b):  # check_v2.inter
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def grow(a, g=GROW):
    return [a[0] - g, a[1] - g, a[2] + 2 * g, a[3] + 2 * g]


def gap(a, b):  # px between two rects (0 if they touch/overlap)
    dx = max(b[0] - (a[0] + a[2]), a[0] - (b[0] + b[2]), 0)
    dy = max(b[1] - (a[1] + a[3]), a[1] - (b[1] + b[3]), 0)
    return max(dx, dy)


def load_payload(p):  # check_v2.load_payload
    s = Path(p).read_text(encoding="utf-8")
    return json.loads(s[s.index("]=") + 2:].rstrip().rstrip(";"))


def vocab_of(js):
    p = Path(js).resolve().parents[2] / "data" / "source" / "vocab.jsonl"
    if not p.exists():
        return {}
    return {v["id"]: v for v in (json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()) if "id" in v}


def pick_room(D, want, V):
    rooms = D["rooms"]
    if want in rooms:
        return want
    for k, R in rooms.items():  # R_id: the room whose words the plan puts in that vocab room
        c = Counter(V.get(it["id"], {}).get("room_id") for it in R["items"])
        if c and c.most_common(1)[0][0] == want:
            return k
    sys.exit(f"room {want!r} not found; keys: {', '.join(rooms)}")


def _tess(exe, lang, im, td, n):
    src = Path(td) / f"t{n}.png"
    im.save(src)
    out = subprocess.run([exe, str(src), "stdout", "-l", lang, "--psm", "11", "tsv"], capture_output=True, text=True,
                         env=dict(os.environ, OMP_THREAD_LIMIT="1")).stdout
    for ln in out.splitlines()[1:]:
        f = ln.split("\t")
        if len(f) >= 12 and f[11].strip():
            yield f[11].strip(), float(f[10]), [int(v) for v in f[6:10]]


def ocr(img_path, workers=4):
    """Tiled sparse-text OCR (480x360 tiles, 50 % overlap, 3x upscale). Whole-image OCR on a painting misses sign
    text and invents letters from brush strokes, so only confident runs are kept: >= 3 letters/digits at conf >= 80,
    or a bare number at conf >= 90, at least 8 px tall. It reliably catches clear sign-like text; small or low-contrast text can be
    missed, so the contact-sheet review still looks for text. Returns (runs, how)."""
    exe = shutil.which("tesseract")
    if not exe:
        return None, "OCR unavailable (install tesseract-ocr); text check skipped - review the sheet by eye"
    from concurrent.futures import ThreadPoolExecutor
    langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True).stdout.split()
    lang = "+".join(l for l in ("eng", "fra") if l in langs) or "eng"
    g = Image.open(img_path).convert("L")
    TW, TH, S = 480, 360, 3
    tiles = [(x, y) for y in range(0, g.height - TH + 1, TH // 2) for x in range(0, g.width - TW + 1, 200)] or [(0, 0)]
    runs = []
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(workers) as ex:
        def job(n):
            x, y = tiles[n]
            im = g.crop((x, y, x + TW, y + TH)).resize((TW * S, TH * S), Image.LANCZOS)
            return [(t, c, [x + b[0] // S, y + b[1] // S, b[2] // S, b[3] // S]) for t, c, b in _tess(exe, lang, im, td, n)]
        for res in ex.map(job, range(len(tiles))):
            for t, c, box in res:
                n_al = len(re.sub(r"[^0-9A-Za-zÀ-ÿ]", "", t))
                if box[3] < 8 or not ((c >= 80 and n_al >= 3) or (t.isdigit() and c >= 90)):
                    continue
                dup = next((r for r in runs if inter(grow(r["box"], 4), box)), None)
                if dup:
                    if c > dup["conf"]:
                        dup.update(text=t, conf=round(c), box=box, digit=bool(re.search(r"\d", t)))
                    continue
                runs.append(dict(text=t, conf=round(c), box=box, digit=bool(re.search(r"\d", t))))
    return runs, f"tesseract {lang}, tiled"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?")
    ap.add_argument("--manifest")
    ap.add_argument("--data", help="village/data/<building>.js")
    ap.add_argument("--room", help="room key or plan room id (R_...)")
    ap.add_argument("--json", help="write findings here")
    a = ap.parse_args()
    F, Wn, Fl, notes = [], [], [], []

    D = R = key = None
    V = {}
    if a.data:
        D = load_payload(a.data)
        V = vocab_of(a.data)
        key = pick_room(D, a.room or D["main"], V)
        R = D["rooms"][key]
    img = a.image or (str(Path(a.data).resolve().parents[1] / R["image"]) if R else None)
    if not img:
        ap.error("give IMAGE or --data/--room")
    print(f"precheck {img}" + (f"  room {D['building']}/{key}" if R else ""))

    im = Image.open(img)
    if im.size != (W, H):
        F.append(f"size: {im.size[0]}x{im.size[1]}, need {W}x{H}")
    else:
        notes.append("size: 1280x720 ok")

    M = json.loads(Path(a.manifest).read_text(encoding="utf-8")) if a.manifest else None
    declared = [str(t.get("text", "")).lower() for t in (M or {}).get("text_in_image", [])]

    runs, how = ocr(img)
    if runs is None:
        Fl.append(how)
    else:
        boxes = [(it["fr"], it["boxPx"]) for it in R["items"]] if R else []
        for r in runs:
            on = [n for n, b in boxes if inter(r["box"], b)]
            dec = any(r["text"].lower() in d or d in r["text"].lower() for d in declared if d)
            tag = "declared in manifest" if dec else ("DIGIT - can break a count" if r["digit"] else "undeclared")
            Fl.append(f"ocr: '{r['text']}' conf {r['conf']} at {r['box']}" + (f" on {', '.join(on)}" if on else "") + f" [{tag}]")
        notes.append(f"ocr: {how}, {len(runs)} text run(s) flagged for human review (flags never reject)")

    if R:
        items = R["items"]
        boxes = [(it["fr"], it["boxPx"]) for it in items]
        labs = [(it["fr"], it["labelPx"]) for it in items]
        fixed = [("door->" + d["to"], d["hit"]) for d in R.get("doors", [])]
        if R.get("mapExit"):
            fixed.append(("mapExit", R["mapExit"]["boxPx"]))
        for z in R.get("zooms", []):
            fixed.append(("zoom->" + z["to"], badge_rect(z)))
        np_ = nameplate_rect(R)
        if np_:
            fixed.append(("nameplate", np_))
        for n, b in boxes + labs + fixed:
            if b[0] < 0 or b[1] < 0 or b[0] + b[2] > W + 0.5 or b[1] + b[3] > H + 0.5:
                F.append(f"bounds: {n} {b}")
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if inter(boxes[i][1], boxes[j][1]): F.append(f"hotspots overlap: {boxes[i][0]} / {boxes[j][0]}")
                if inter(labs[i][1], labs[j][1]): F.append(f"labels overlap: {labs[i][0]} / {labs[j][0]}")
                elif inter(grow(labs[i][1]), labs[j][1]): Wn.append(f"labels within {GROW}px: {labs[i][0]} / {labs[j][0]}")
        for n, f in fixed:
            for m, b in boxes:
                if inter(f, b): F.append(f"hotspot {m} overlaps {n}")
            for m, l in labs:
                if inter(f, l): F.append(f"label {m} overlaps {n}")
                elif inter(grow(l), f): Wn.append(f"label {m} within {GROW}px of {n}")
        for (m, b), (_, l) in zip(boxes, labs):
            for (m2, b2) in boxes:
                if m2 != m and inter(grow(l), b2): Wn.append(f"label {m} touches hotspot {m2}")
            if l[0] < EDGE or l[1] < EDGE or l[0] + l[2] > W - EDGE or l[1] + l[3] > H - EDGE:
                Wn.append(f"label {m} closer than {EDGE}px to the scene edge")
            g = gap(l, b)
            if g > DETACH: Wn.append(f"label {m} is {g:.0f}px from its own box (detached)")
        for it in items:
            cx = (it["boxPx"][0] + it["boxPx"][2] / 2) / W
            if (it.get("adj") or it.get("adv")) and not 0.3 <= cx <= 0.7:
                Wn.append(f"{'adjective' if it.get('adj') else 'adverb'} {it['fr']} outside the centre band ({cx:.0%})")
        notes.append(f"labels: {len(items)} items, {len(fixed)} fixed rects (doors/mapExit/zoom badges/nameplate) checked")
        if R.get("zooms") is not None and D:
            for z in R["zooms"]:
                n = len(D["rooms"].get(z["to"], {}).get("items", []))
                if n <= 1: F.append(f"zoom {z['to']} holds {n} word(s): one-object zoom, fold it into a fuller scene")
                elif n < 4: Wn.append(f"zoom {z['to']} holds only {n} words: thin, consider folding it into a fuller scene")

    if M is not None:
        ent = {e.get("id"): e for e in M.get("items", [])}
        if R:
            ids = [it["id"] for it in R["items"]]
            for i in ids:
                if i not in ent: F.append(f"manifest: {i} is in the room but not in the manifest")
            for i in ent:
                if i not in ids: Wn.append(f"manifest: {i} is in the manifest but not live in this room (new word, or moved?)")
            if len(M.get("doors", [])) < len(R.get("doors", [])) + (1 if R.get("mapExit") else 0):
                F.append(f"manifest: lists {len(M.get('doors', []))} doors/exits, room has {len(R.get('doors', []))} doors" + (" + mapExit" if R.get("mapExit") else ""))
        elif not M.get("doors"):
            F.append("manifest: no doors/exits listed")
        for i, e in ent.items():
            pos = V.get(i, {}).get("pos") or e.get("pos", "")
            for k in ("word", "shown", "pose_action", "sensitive"):
                if not str(e.get(k, "")).strip(): F.append(f"manifest: {i} has no '{k}'")
            if (pos == "num" or e.get("count") is not None) and not isinstance(e.get("count"), int):
                F.append(f"manifest: {i} needs an exact integer 'count'")
            if pos == "verb" and not str(e.get("verb_acts_on", "")).strip():
                F.append(f"manifest: verb {i} has no 'verb_acts_on' (who acts on what, where)")
        for z in M.get("zooms", []):
            if not str(z.get("to", "")).strip() and not z.get("words"): continue   # empty template row
            if len(z.get("words", [])) <= 1: F.append(f"manifest: zoom {z.get('to')} has {len(z.get('words', []))} word(s): fold it")
        # prompt gate (builder reference/prompt-template.md): the prompt is built from the template, every field filled
        sit = str(M.get("scene_situation", "")).strip()
        if not sit: F.append("manifest: no 'scene_situation' (the one named everyday situation everyone takes part in)")
        grp = M.get("interactions")
        if not isinstance(grp, list) or not grp:
            F.append("manifest: no 'interactions' (small interacting groups: who does what with whom)")
        else:
            inq = set()
            for g in grp:
                who = g.get("who", []) if isinstance(g, dict) else []
                if len(who) < 2 or not str(g.get("doing", "")).strip():
                    F.append(f"manifest: interaction {who or g} needs 2+ 'who' and a 'doing'")
                inq.update(who)
            for i, e in ent.items():
                if i and i not in inq and "plaque" not in str(e.get("sensitive", "")) + str(e.get("shown", "")):
                    Wn.append(f"manifest: {i} is in no interaction group (isolated figure? natural-scene gate)")
        for k in ("siblings", "used_motifs"):
            if k not in M: F.append(f"manifest: no '{k}' (list sibling rooms / motifs already used; [] if none)")
        pt = str(M.get("prompt_text", ""))
        if not pt.strip(): F.append("manifest: no 'prompt_text' (the filled prompt-template text actually sent)")
        else:
            miss = [h for h in PROMPT_SECTIONS if h + ":" not in pt]
            if miss: F.append("manifest: prompt_text lacks template section(s): " + ", ".join(miss))
            left = re.findall(r"\{[^{}\n]{1,60}\}", pt)
            if left: F.append(f"manifest: prompt_text has {len(left)} unfilled field(s), e.g. {left[0]}")
            for i, e in ent.items():
                w = str(e.get("word", "")).strip()
                if w and w.lower() not in pt.lower(): F.append(f"manifest: prompt_text does not list item {w}")
            if sit and sit.lower()[:40] not in pt.lower(): Wn.append("manifest: prompt_text does not quote scene_situation")
        notes.append(f"manifest: {len(ent)} entries checked")

    for n in notes: print("  ok   ", n)
    for f in F: print("  FAIL ", f)
    for w in Wn: print("  WARN ", w)
    for f in Fl: print("  FLAG ", f)
    print(f"summary: {len(F)} fail, {len(Wn)} warn, {len(Fl)} flag" + ("  -> fix FAILs before visual review" if F else "  -> ready for the contact-sheet review"))
    if a.json:
        Path(a.json).write_text(json.dumps(dict(image=img, room=key, fail=F, warn=Wn, flag=Fl, notes=notes), indent=1, ensure_ascii=False))
    sys.exit(1 if F else 0)


if __name__ == "__main__":
    main()

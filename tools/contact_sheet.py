#!/usr/bin/env python3
"""contact_sheet.py - ONE downscaled review sheet per room (the visual-review unit).

  python3 contact_sheet.py --data village/data/ecole.js --room cantine [--room jardin | --all]
                           [--image other.jpg] [--shots DIR] [--precheck pre.json] [--out DIR] [--width 1400]
                           [--grid] [--anatomy-2x] [--sync-manifest /tmp/manifest.json]

Top row: the painting with hotspot boxes (green), label rects (yellow, word) and doors / mapExit / zoom badges
(blue) drawn from the built data, plus precheck OCR flags (red) when --precheck is given; next to it the browser
screenshot of the live room when one exists (--shots DIR, check_v2 names it <bld>_<key>_<viewport>.png).
Below: one 256 px tile per item = the card crop (square max(w,h)*1.18 around the box, as build_v2 cuts it) with
the word and its hook, then one tile per exit (door hit box / mapExit box, with its destination), so gate A
(>= 256 px crops of every item and exit box, headword + hook under each) is read from the sheet.
Optional flags:
  --grid           also write <bld>_<key>_grid.jpg with a 50px/100px labeled coordinate grid for 1-read box fitting
  --anatomy-2x     also write 2x upscaled quadrant crops (<bld>_<key>_2x_q1..q4.jpg) for mandatory Gate 26 inspection
  --sync-manifest  copy fitted boxPx from the built room data into the manifest's box_hint/zone and re-run build_prompt
"""
import argparse, json, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from precheck import load_payload, badge_rect, nameplate_rect, W, H  # same geometry as the checks
import build_prompt


def font(sz, bold=False):
    p = f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf"
    return ImageFont.truetype(p, sz) if Path(p).exists() else ImageFont.load_default()


def overlay(img, R, flags):
    im = img.convert("RGB").copy()
    d = ImageDraw.Draw(im)
    f = font(15, True)
    rect = lambda b, c, w=3: d.rectangle([b[0], b[1], b[0] + b[2], b[1] + b[3]], outline=c, width=w)
    for dr in R.get("doors", []):
        rect(dr["hit"], (40, 120, 255)); d.text((dr["hit"][0] + 4, dr["hit"][1] + 4), "door→" + dr["to"], font=f, fill=(40, 120, 255))
    if R.get("mapExit"):
        rect(R["mapExit"]["boxPx"], (40, 120, 255)); d.text((R["mapExit"]["boxPx"][0] + 4, R["mapExit"]["boxPx"][1] + 4), "map", font=f, fill=(40, 120, 255))
    for z in R.get("zooms", []):
        rect(badge_rect(z), (40, 120, 255))
    np_ = nameplate_rect(R)
    if np_:
        rect(np_, (40, 120, 255), 2)
    for it in R["items"]:
        rect(it["boxPx"], (40, 200, 60))
        l = it["labelPx"]
        d.rectangle([l[0], l[1], l[0] + l[2], l[1] + l[3]], fill=(255, 245, 200), outline=(200, 160, 0), width=2)
        d.text((l[0] + 6, l[1] + 5), it["fr"], font=f, fill=(30, 30, 30))
    for fl in flags:
        rect(fl["box"], (230, 30, 30), 3)
        d.text((fl["box"][0], fl["box"][1] + fl["box"][3] + 2), fl["text"], font=f, fill=(230, 30, 30))
    return im


def write_grid(img, out_path):
    """Write a 50px/100px coordinate grid over the 1280x720 painting for 1-pass box fitting."""
    im = img.convert("RGB").copy()
    dr = ImageDraw.Draw(im)
    f = font(11, True)
    for x in range(0, W, 50):
        col = (255, 40, 40) if x % 100 == 0 else (80, 220, 255)
        dr.line([(x, 0), (x, H)], fill=col, width=1)
    for y in range(0, H, 50):
        col = (255, 40, 40) if y % 100 == 0 else (80, 220, 255)
        dr.line([(0, y), (W, y)], fill=col, width=1)
    for x in range(0, W, 100):
        for y in range(0, H, 100):
            dr.rectangle([x, y, x + 46, y + 14], fill=(0, 0, 0))
            dr.text((x + 2, y + 1), f"{x},{y}", font=f, fill=(255, 255, 180))
    im.save(out_path, quality=90)
    print(f"{out_path}  ({out_path.stat().st_size // 1024} KB)")


def write_anatomy_2x(img, out_dir, prefix):
    """Write four overlapping 2x upscaled quadrants covering the entire 1280x720 room for Gate 26."""
    im = img.convert("RGB")
    quads = [
        ("q1_tl", (0, 0, 680, 400)),
        ("q2_tr", (600, 0, 1280, 400)),
        ("q3_bl", (0, 320, 680, 720)),
        ("q4_br", (600, 320, 1280, 720)),
    ]
    for qname, (x0, y0, x1, y1) in quads:
        crop = im.crop((x0, y0, x1, y1))
        up = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
        p = out_dir / f"{prefix}_2x_{qname}.jpg"
        up.save(p, quality=90)
        print(f"{p}  ({p.stat().st_size // 1024} KB)")


def sync_manifest_boxes(manifest_path, R):
    """Sync fitted boxPx from built room data into manifest box_hint/zone and recompile prompt_text."""
    p = Path(manifest_path)
    M = json.loads(p.read_text(encoding="utf-8"))
    by_id = {it["id"]: it["boxPx"] for it in R.get("items", []) if "boxPx" in it}
    for it in M.get("items", []):
        if it.get("id") in by_id:
            b = by_id[it["id"]]
            it["box_hint"] = b
            z = str(it.get("zone") or "").split("[")[0].strip()
            it["zone"] = f"{z} {b}".strip()
    t, missing, left = build_prompt.build(M)
    if not (missing or left):
        M["prompt_text"] = t
    p.write_text(json.dumps(M, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"synced {len(by_id)} fitted boxes into {p}")


def card_crop(img, b):  # build_v2: square of max(w,h)*1.18 centred on the box, clamped to the scene
    s = max(b[2], b[3]) * 1.18
    cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
    s = min(s, W, H)
    x0 = min(max(cx - s / 2, 0), W - s); y0 = min(max(cy - s / 2, 0), H - s)
    return img.crop((int(x0), int(y0), int(x0 + s), int(y0 + s)))


def sheet(bld, key, R, img, shot, flags, width):
    half = width // 2 - 15
    sc = half / W
    top_h = int(H * sc)
    tile = 256  # gate A: >= 256 px on the long side
    pitch = tile + 10
    cols = max(1, (width - 20) // pitch)
    tiles = [(it["boxPx"], it["fr"], (it.get("hook") or "").replace("\n", " ")) for it in R["items"]]
    tiles += [(dr["hit"], "door → " + dr["to"], dr.get("label") or dr.get("hint") or "") for dr in R.get("doors", [])]
    if R.get("mapExit"):
        tiles.append((R["mapExit"]["boxPx"], "exit → map", R["mapExit"].get("label") or ""))
    rows = (len(tiles) + cols - 1) // cols
    th = tile + 62
    out = Image.new("RGB", (width, 40 + top_h + 20 + rows * th + 10), (250, 248, 242))
    d = ImageDraw.Draw(out)
    d.text((10, 10), f"{bld}/{key}  ·  {R.get('name', '')}  ·  {len(R['items'])} words, {len(R.get('doors', []))} doors, "
           f"{len(R.get('zooms', []))} zooms, {len(flags)} OCR flags", font=font(16, True), fill=(20, 20, 20))
    out.paste(overlay(img, R, flags).resize((half, top_h), Image.LANCZOS), (10, 40))
    if shot:
        s = Image.open(shot).convert("RGB")
        s.thumbnail((half, top_h), Image.LANCZOS)
        out.paste(s, (20 + half, 40))
        d.text((24 + half, 44 + s.height), Path(shot).name, font=font(12), fill=(90, 90, 90))
    else:
        d.text((30 + half, 44), "no browser shot (pass --shots DIR); labels drawn from the built data. Hooks:", font=font(12), fill=(120, 120, 120))
        yy = 64
        for it in R["items"]:
            for k, ln in enumerate(textwrap.wrap(f"{it['fr']}: {(it.get('hook') or '').strip()}", 98)[:3]):
                if yy > 40 + top_h - 12:
                    break
                d.text((30 + half + (0 if k == 0 else 12), yy), ln, font=font(11, k == 0 and False), fill=(40, 40, 40)); yy += 13
            yy += 3
    base = img.convert("RGB")
    y0 = 40 + top_h + 20
    for n, (box, head, hook) in enumerate(tiles):
        x, y = 10 + (n % cols) * pitch, y0 + (n // cols) * th
        out.paste(card_crop(base, box).resize((tile, tile), Image.LANCZOS), (x, y))
        d.text((x, y + tile + 2), head[:34], font=font(13, True), fill=(20, 20, 20))
        d.text((x, y + tile + 19), "\n".join(textwrap.wrap(hook, 42)[:3]), font=font(10), fill=(70, 70, 70))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--room", action="append", help="room key (repeat); default: main room")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--image", help="painting to use instead of the live one (single room)")
    ap.add_argument("--shots", help="dir with browser screenshots <bld>_<key>_*.png")
    ap.add_argument("--precheck", help="precheck.py --json output to draw OCR flags (single room)")
    ap.add_argument("--out", default=".")
    ap.add_argument("--tag", default="", help="suffix for the output name")
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--grid", action="store_true", help="also write a 50px/100px coordinate grid image for box fitting")
    ap.add_argument("--anatomy-2x", action="store_true", help="also write 2x upscaled quadrant crops for Gate 26 inspection")
    ap.add_argument("--sync-manifest", metavar="PATH", help="sync fitted boxPx into manifest box_hint/zone and recompile prompt")
    a = ap.parse_args()
    D = load_payload(a.data)
    V2 = Path(a.data).resolve().parents[1]
    keys = list(D["rooms"]) if a.all else (a.room or [D["main"]])
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for key in keys:
        R = D["rooms"][key]
        img = Image.open(a.image if a.image else V2 / R["image"])
        shot = None
        if a.shots:
            c = sorted(Path(a.shots).glob(f"{D['building']}_{key}_*.png"))
            shot = c[-1] if c else None
        flags = []
        if a.precheck:
            P = json.loads(Path(a.precheck).read_text(encoding="utf-8"))
            for f in P.get("flag", []):
                if f.startswith("ocr: '") and " at [" in f:
                    t = f[6:f.index("' conf")]
                    b = json.loads(f[f.index(" at [") + 4:f.index("]", f.index(" at [")) + 1])
                    flags.append(dict(text=t, box=b))
        prefix = f"{D['building']}_{key}{a.tag}"
        o = out_dir / f"{prefix}_sheet.jpg"
        sheet(D["building"], key, R, img, shot, flags, a.width).save(o, quality=85)
        print(f"{o}  ({o.stat().st_size // 1024} KB)")
        if a.grid:
            write_grid(img, out_dir / f"{prefix}_grid.jpg")
        if a.anatomy_2x:
            write_anatomy_2x(img, out_dir, prefix)
        if a.sync_manifest and len(keys) == 1:
            sync_manifest_boxes(a.sync_manifest, R)


if __name__ == "__main__":
    main()

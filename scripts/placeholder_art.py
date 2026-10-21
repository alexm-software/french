#!/usr/bin/env python3
"""Paint text-free placeholder rooms for sectors listed in content/site.json.

Real paintings replace a room by dropping content/art/<room_id>/base.jpg and
hotspots.json and removing placeholder.json. This script never overwrites a
room that is not marked as a placeholder.

Nothing in the image is a letter. Signs, plaques, gender labels and door
prepositions are drawn later as HTML/SVG text from the hotspot text areas.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
ART = ROOT / "content" / "art"
W, H = 1280, 720
SCALE = 2

CERAMIC = [
    (214, 186, 150),
    (168, 146, 124),
    (120, 146, 130),
    (186, 154, 122),
    (150, 118, 96),
    (196, 176, 154),
    (132, 108, 90),
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def s(n):
    return int(round(n * SCALE))


def box_s(box):
    return [s(v) for v in box]


def new_canvas():
    img = Image.new("RGB", (s(W), s(H)), (232, 220, 204))
    return img, ImageDraw.Draw(img)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fill_vgrad(img, top, bottom):
    px = img.load()
    width, height = img.size
    for y in range(height):
        color = lerp(top, bottom, y / max(1, height - 1))
        for x in range(width):
            px[x, y] = color


def shade(color, delta):
    return tuple(max(0, min(255, c + delta)) for c in color)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box_s(box), radius=s(radius), fill=fill, outline=outline, width=s(width) if outline else 1)


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(box_s(box), fill=fill, outline=outline, width=s(width) if outline else 1)


def rect(draw, box, fill, outline=None, width=1):
    draw.rectangle(box_s(box), fill=fill, outline=outline, width=s(width) if outline else 1)


def polygon(draw, points, fill, outline=None):
    draw.polygon([tuple(box_s(p)[:2] if False else (s(p[0]), s(p[1]))) for p in points], fill=fill, outline=outline)


def line(draw, a, b, fill, width=2):
    draw.line([(s(a[0]), s(a[1])), (s(b[0]), s(b[1]))], fill=fill, width=s(width))


def hash_color(key):
    digest = hashlib.sha1(key.encode("utf-8")).digest()
    return CERAMIC[digest[0] % len(CERAMIC)]


def theme_for(room):
    if room["kind"] == "zoom":
        return "bar"
    if room["kind"] == "street_segment":
        return "street"
    rid = room["id"]
    name = room["name"].lower()
    if rid.startswith("R_cafe"):
        return "cafe"
    if "kitchen" in rid or "kitchen" in name:
        return "kitchen"
    if rid.startswith("R_wine") or "cellar" in name or "wine" in name:
        return "cellar"
    if "resto" in rid or "dining" in name:
        return "dining"
    return "interior"


def draw_floor(draw, y, color_a, color_b):
    rect(draw, (0, y, W, H), color_a)
    for i, x in enumerate(range(0, W, 46)):
        inset = 8 if i % 2 else 0
        for yy in range(y + inset, H, 28):
            tone = color_b if (i + yy // 28) % 2 == 0 else shade(color_b, 12)
            rounded(draw, (x + 3, yy, x + 40, yy + 18), 3, tone)


def draw_sign_board(draw, box):
    x0, y0, x1, y1 = box
    line(draw, (x0 + 40, 0), (x0 + 46, y0 + 6), (70, 58, 40), 3)
    line(draw, (x1 - 40, 0), (x1 - 46, y0 + 6), (70, 58, 40), 3)
    rounded(draw, box, 8, (96, 64, 40), (62, 40, 24), 3)
    rounded(draw, (x0 + 14, y0 + 12, x1 - 14, y1 - 12), 4, (118, 82, 52))


def draw_plaque_board(draw, box, paper=(245, 236, 214)):
    x0, y0, x1, y1 = box
    rounded(draw, box, 4, (150, 118, 62), (96, 74, 36), 3)
    rect(draw, (x0 + 8, y0 + 8, x1 - 8, y1 - 8), paper)


def draw_awning(draw, y, stripe_a, stripe_b):
    rect(draw, (0, y, W, y + 36), stripe_a)
    for x in range(0, W, 36):
        rect(draw, (x, y, x + 18, y + 36), stripe_b)
    for x in range(0, W, 28):
        ellipse(draw, (x, y + 24, x + 28, y + 52), stripe_a if (x // 28) % 2 == 0 else stripe_b)


def paint_backdrop(img, draw, theme):
    if theme == "cafe":
        fill_vgrad(img, (214, 196, 168), (186, 164, 140))
        rect(draw, (0, 150, W, 470), (214, 186, 162))
        draw_awning(draw, 132, (122, 42, 48), (245, 236, 220))
        # window arches, no letters
        for x in (180, 860):
            ellipse(draw, (x, 188, x + 150, 360), (168, 196, 204), (96, 74, 52), 3)
            rect(draw, (x, 270, x + 150, 360), (168, 196, 204), (96, 74, 52), 3)
            line(draw, (x + 75, 200), (x + 75, 360), (96, 74, 52), 2)
        draw_floor(draw, 470, (150, 124, 96), (132, 108, 84))
        # café pole, architecture only
        rect(draw, (632, 168, 648, 500), (92, 64, 42))
    elif theme == "dining":
        fill_vgrad(img, (206, 190, 170), (168, 146, 124))
        rect(draw, (0, 140, W, 500), (224, 208, 188))
        for x in (80, 1000):
            rect(draw, (x, 180, x + 160, 420), (186, 168, 146))
            rect(draw, (x + 16, 200, x + 144, 300), (120, 146, 138))
        draw_floor(draw, 500, (128, 96, 72), (108, 80, 60))
        rect(draw, (620, 150, 660, 520), (176, 164, 148))
    elif theme == "kitchen":
        fill_vgrad(img, (210, 206, 196), (176, 170, 156))
        rect(draw, (0, 120, W, 480), (226, 220, 206))
        # tile grid
        for y in range(160, 460, 28):
            for x in range(0, W, 28):
                tone = (214, 206, 190) if (x // 28 + y // 28) % 2 == 0 else (198, 188, 170)
                rect(draw, (x + 1, y + 1, x + 26, y + 26), tone)
        rect(draw, (80, 300, 360, 470), (88, 92, 96))  # stove mass
        ellipse(draw, (110, 330, 190, 400), (60, 64, 68))
        ellipse(draw, (220, 330, 300, 400), (60, 64, 68))
        rect(draw, (860, 250, 1180, 460), (120, 86, 62))  # copper cupboard
        draw_floor(draw, 480, (120, 112, 100), (104, 96, 86))
    elif theme == "cellar":
        fill_vgrad(img, (92, 84, 78), (62, 56, 52))
        rect(draw, (0, 80, W, H), (110, 100, 94))
        for x in (40, 250, 860, 1060):
            # bottle niches
            rounded(draw, (x, 160, x + 150, 430), 70, (78, 70, 64))
            for by in (200, 250, 300, 350):
                ellipse(draw, (x + 30, by, x + 58, by + 70), (46, 70, 48))
                ellipse(draw, (x + 80, by, x + 108, by + 70), (92, 40, 42))
        draw_floor(draw, 500, (90, 78, 68), (74, 64, 56))
    elif theme == "bar":
        fill_vgrad(img, (64, 52, 44), (40, 32, 28))
        rect(draw, (0, 0, W, 430), (92, 70, 54))
        # shelf of blank bottles behind the counter
        for i, x in enumerate(range(70, 1180, 36)):
            hgt = 70 + (i % 4) * 16
            ellipse(draw, (x, 180 + (90 - hgt), x + 22, 280), (70, 90, 72) if i % 3 else (120, 48, 46))
        rect(draw, (0, 430, W, H), (96, 62, 40))
        rect(draw, (0, 430, W, 456), (214, 186, 150))
    elif theme == "street":
        fill_vgrad(img, (176, 196, 210), (214, 196, 168))
        rect(draw, (0, 430, W, H), (150, 132, 108))
        for x in range(0, W, 40):
            ellipse(draw, (x, 500, x + 36, 530), (132, 116, 96))
            ellipse(draw, (x + 8, 560, x + 44, 600), (120, 104, 86))
    else:
        fill_vgrad(img, (214, 202, 184), (186, 170, 150))
        rect(draw, (0, 140, W, 500), (222, 210, 192))
        draw_floor(draw, 500, (150, 130, 110), (130, 112, 96))


def draw_cup(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rw, rh = (x1 - x0) * 0.28, (y1 - y0) * 0.32
    ellipse(draw, (cx - rw, cy - rh * 0.2, cx + rw, cy + rh), color, shade(color, -40), 2)
    ellipse(draw, (cx - rw * 0.8, cy - rh * 0.55, cx + rw * 0.8, cy - rh * 0.05), shade(color, 30))
    # handle
    ellipse(draw, (cx + rw * 0.6, cy - rh * 0.05, cx + rw * 1.35, cy + rh * 0.55), None if False else shade(color, -20))
    # punch a hole by drawing backdrop-ish inner — use a darker ring only
    ellipse(draw, (cx + rw * 0.85, cy + rh * 0.05, cx + rw * 1.15, cy + rh * 0.4), (0, 0, 0, 0) if False else shade(color, 40))


def draw_bottle(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    top, bot = y0 + 4, y1 - 4
    neck_w = max(6, (x1 - x0) * 0.08)
    body_w = (x1 - x0) * 0.22
    polygon(draw, [
        (cx - neck_w, top + 8),
        (cx + neck_w, top + 8),
        (cx + neck_w, top + (bot - top) * 0.28),
        (cx + body_w, top + (bot - top) * 0.42),
        (cx + body_w, bot),
        (cx - body_w, bot),
        (cx - body_w, top + (bot - top) * 0.42),
        (cx - neck_w, top + (bot - top) * 0.28),
    ], color, shade(color, -50))
    rect(draw, (cx - neck_w, top, cx + neck_w, top + 10), shade(color, -30))


def draw_glass(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    top, bot = y0 + 8, y1 - 6
    bowl = (186, 206, 196)
    polygon(draw, [
        (cx - 26, top),
        (cx + 26, top),
        (cx + 10, top + (bot - top) * 0.55),
        (cx + 3, bot - 8),
        (cx - 3, bot - 8),
        (cx - 10, top + (bot - top) * 0.55),
    ], bowl, (90, 100, 98))
    rect(draw, (cx - 16, bot - 8, cx + 16, bot), (210, 206, 196))
    # a little wine-dark or clear liquid
    polygon(draw, [
        (cx - 18, top + 18),
        (cx + 18, top + 18),
        (cx + 8, top + (bot - top) * 0.5),
        (cx - 8, top + (bot - top) * 0.5),
    ], color)


def draw_bowl(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ellipse(draw, (cx - 40, cy - 10, cx + 40, cy + 28), color, shade(color, -40), 2)
    ellipse(draw, (cx - 28, cy - 16, cx + 28, cy + 6), shade(color, 36))


def draw_plate(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) * 0.62
    ellipse(draw, (cx - 46, cy - 16, cx + 46, cy + 18), (236, 230, 218), (160, 140, 110), 2)
    ellipse(draw, (cx - 24, cy - 8, cx + 24, cy + 8), color)


def draw_leaf(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ellipse(draw, (cx - 28, cy - 16, cx + 22, cy + 18), (78, 120, 72))
    ellipse(draw, (cx - 8, cy - 22, cx + 30, cy + 8), (96, 140, 80))
    line(draw, (cx - 10, cy + 16), (cx + 8, cy - 14), (48, 80, 46), 2)


def draw_cake(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    base = y1 - 10
    rounded(draw, (cx - 36, base - 28, cx + 36, base), 4, color, shade(color, -40), 2)
    rounded(draw, (cx - 28, base - 48, cx + 28, base - 24), 4, shade(color, 30))
    ellipse(draw, (cx - 6, base - 62, cx + 6, base - 50), (196, 92, 64))


def draw_card(draw, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rounded(draw, (cx - 28, cy - 34, cx + 22, cy + 30), 3, (245, 240, 228), (120, 96, 70), 2)
    rounded(draw, (cx - 16, cy - 28, cx + 32, cy + 36), 3, shade(color, 40), (120, 96, 70), 2)


def draw_jar(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    top, bot = y0 + 10, y1 - 6
    rounded(draw, (cx - 22, top + 14, cx + 22, bot), 8, color, shade(color, -40), 2)
    rect(draw, (cx - 14, top, cx + 14, top + 16), shade(color, -20))
    ellipse(draw, (cx - 16, top - 4, cx + 16, top + 10), shade(color, 10))


def draw_pot(draw, box, color):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    ellipse(draw, (cx - 34, y0 + 28, cx + 34, y1 - 6), color, shade(color, -40), 2)
    ellipse(draw, (cx - 16, y0 + 16, cx + 16, y0 + 36), shade(color, 20))
    line(draw, (cx - 30, y0 + 36), (cx - 46, y0 + 20), shade(color, -30), 3)
    line(draw, (cx + 30, y0 + 36), (cx + 46, y0 + 20), shade(color, -30), 3)


def draw_plaque_prop(draw, box):
    x0, y0, x1, y1 = box
    pad = 4
    draw_plaque_board(draw, (x0 + pad, y0 + pad, x1 - pad, y1 - pad), (244, 236, 214))


def icon_kind(word):
    if word.get("display") in ("museum_text", "text_plain"):
        return "plaque"
    lemma = word["lemma"].casefold()
    groups = (
        (("tasse", "café", "cafe", "thé", "the"), "cup"),
        (("bouteille", "bière", "biere", "vin", "rhum", "whisky", "vodka", "cognac", "champagne", "cidre", "carafe", "soda", "alcool"), "bottle"),
        (("verre",), "glass"),
        (("soupe", "purée", "puree", "bol", "glace"), "bowl"),
        (("plat", "assiette"), "plate"),
        (("menthe", "tilleul", "vigne", "vanille"), "leaf"),
        (("dessert", "frite", "gâteau", "gateau"), "cake"),
        (("menu", "facture", "recette", "commande", "addition"), "card"),
        (("casserole", "poêle", "poele", "faitout"), "pot"),
    )
    for keys, kind in groups:
        if any(key in lemma for key in keys):
            return kind
    if word["pos"] == "adj":
        return "card"
    return "jar"


DRAWERS = {
    "cup": draw_cup,
    "bottle": draw_bottle,
    "glass": draw_glass,
    "bowl": draw_bowl,
    "plate": draw_plate,
    "leaf": draw_leaf,
    "cake": draw_cake,
    "card": draw_card,
    "jar": draw_jar,
    "pot": draw_pot,
    "plaque": draw_plaque_prop,
}


def draw_prop(draw, box, word):
    kind = icon_kind(word)
    color = hash_color(word["id"])
    if kind == "bottle" and word["lemma"].casefold() in {"vin", "bière", "biere", "rhum", "cognac", "whisky"}:
        color = (92, 40, 48)
    ellipse(draw, (box[0] + 10, box[3] - 8, box[2] - 10, box[3] + 4), (120, 96, 74))
    drawer = DRAWERS[kind]
    if kind == "plaque":
        drawer(draw, box)
    else:
        drawer(draw, box, color)


def draw_bird(draw, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ellipse(draw, (x0 + 2, cy - 6, cx + 4, y1 - 2), (42, 40, 46))
    ellipse(draw, (cx - 2, y0 + 2, x1 - 2, cy + 8), (42, 40, 46))
    polygon(draw, [(x0, cy), (x0 + 10, cy - 4), (x0 + 10, cy + 6)], (42, 40, 46))
    ellipse(draw, (cx + 4, cy - 2, cx + 7, cy + 1), (20, 20, 20))


def choose_helper(words):
    for word in words:
        if word.get("display") != "drawn":
            continue
        hook = word.get("mnemonic_hook") or {}
        sound = (hook.get("sound_alike") or "").strip()
        if hook.get("strength") == "strong" and sound and hook.get("source") == "manual":
            if sound.casefold() not in {word["lemma"].casefold(), "cognate"}:
                return word["id"]
    return None


def grid_boxes(n, rect):
    if n <= 0:
        return []
    x0, y0, x1, y1 = rect
    cols = 1
    while cols < 4:
        rows = math.ceil(n / cols)
        cell_h = (y1 - y0) / rows
        if cell_h >= 86 or cols == 3:
            break
        cols += 1
    rows = math.ceil(n / cols)
    cell_w = (x1 - x0) / cols
    cell_h = (y1 - y0) / rows
    boxes = []
    for i in range(n):
        c, r = i % cols, i // cols
        left = x0 + c * cell_w
        top = y0 + r * cell_h
        prop = (
            left + cell_w * 0.18,
            top + cell_h * 0.30,
            left + cell_w * 0.82,
            top + cell_h * 0.92,
        )
        boxes.append([int(v) for v in prop])
    return boxes


def layout_words(words, has_zoom, zoom_side):
    left = [w for w in words if w.get("side") == "left"]
    right = [w for w in words if w.get("side") == "right"]
    mid = [w for w in words if w.get("side") not in {"left", "right"}]
    bottom = 590 if has_zoom else 690
    top = 176
    if mid:
        regions = {
            "left": (36, top, 500, bottom),
            "mid": (510, top, 770, bottom),
            "right": (780, top, 1244, bottom),
        }
    else:
        regions = {
            "left": (36, top, 616, bottom),
            "mid": None,
            "right": (664, top, 1244, bottom),
        }
    placed = []
    for key, group in (("left", left), ("mid", mid), ("right", right)):
        rect = regions[key]
        if not rect:
            continue
        for word, box in zip(group, grid_boxes(len(group), rect)):
            placed.append((word, box))
    return placed


def facade_styles(theme_text):
    text = (theme_text or "").lower()
    if any(word in text for word in ("teapot", "cake", "pan", "bistro")):
        return ["teapot", "cake", "pan"]
    return ["house", "shop", "house"]


def draw_facade(draw, box, style, museum):
    x0, y0, x1, y1 = box
    if museum:
        rounded(draw, box, 6, (168, 160, 148), (90, 84, 74), 3)
        draw_plaque_board(draw, (x0 + 18, y0 + 36, x1 - 18, y1 - 120))
        return
    if style == "teapot":
        ellipse(draw, (x0 + 10, y0 + 70, x1 - 10, y1 - 20), (186, 196, 198), (90, 96, 100), 3)
        ellipse(draw, (x0 + 30, y0 + 24, x1 - 30, y0 + 90), (206, 214, 216), (90, 96, 100), 3)
        line(draw, ((x0 + x1) / 2, y0 + 24), ((x0 + x1) / 2 - 20, y0 + 4), (90, 96, 100), 3)
    elif style == "cake":
        rounded(draw, (x0 + 16, y0 + 150, x1 - 16, y1 - 16), 8, (214, 170, 150), (140, 96, 80), 3)
        rounded(draw, (x0 + 28, y0 + 100, x1 - 28, y0 + 170), 8, (230, 196, 176))
        rounded(draw, (x0 + 40, y0 + 54, x1 - 40, y0 + 116), 8, (240, 214, 196))
        ellipse(draw, ((x0 + x1) / 2 - 8, y0 + 28, (x0 + x1) / 2 + 8, y0 + 52), (176, 64, 64))
    elif style == "pan":
        ellipse(draw, (x0 + 18, y0 + 80, x1 - 8, y1 - 30), (176, 112, 62), (110, 70, 36), 3)
        line(draw, (x1 - 16, (y0 + y1) / 2), (x1 + 10, (y0 + y1) / 2 - 30), (90, 64, 40), 6)
    else:
        rounded(draw, box, 4, (196, 176, 150), (96, 72, 52), 3)
        polygon(draw, [(x0 - 4, y0 + 40), ((x0 + x1) / 2, y0), (x1 + 4, y0 + 40)], (122, 48, 44))
        rect(draw, (x0 + 24, y0 + 70, x1 - 24, y0 + 130), (150, 176, 186))
    # door
    door_w = 36
    cx = (x0 + x1) / 2
    rect(draw, (cx - door_w / 2, y1 - 110, cx + door_w / 2, y1 - 16), (72, 48, 32))


def door_plaque_box(house):
    x0, y0, x1, y1 = house
    cx = (x0 + x1) / 2
    return [int(cx - 28), int(y1 - 78), int(cx + 28), int(y1 - 42)]


def mirror_box(house):
    x0, y0, x1, y1 = house
    return [int(x0 + 16), int(y0 + 48), int(x0 + 52), int(y0 + 96)]


def draw_mirror(draw, box):
    ellipse(draw, box, (214, 224, 226), (72, 78, 86), 3)
    x0, y0, x1, y1 = box
    line(draw, (x0 + 8, y0 + 10), (x1 - 10, y1 - 16), (255, 255, 255), 2)


def sign_and_plaque():
    sign = [430, 18, 850, 128]
    plaque = [48, 22, 236, 146]
    return sign, plaque


def street_sign_and_plaque():
    sign = [340, 16, 940, 108]
    plaque = [48, 24, 220, 120]
    return sign, plaque


def inset(box, dx, dy):
    return [box[0] + dx, box[1] + dy, box[2] - dx, box[3] - dy]


def paint_room(room, words_by_id, building, dest: Path):
    words = [words_by_id[i] for i in room["words"]]
    theme = theme_for(room)
    img, draw = new_canvas()
    paint_backdrop(img, draw, theme)
    sign, plaque = street_sign_and_plaque() if theme == "street" else sign_and_plaque()
    draw_sign_board(draw, sign)
    draw_plaque_board(draw, plaque)

    hotspots = []
    helper_id = choose_helper(words)

    if theme == "street":
        styles = facade_styles((building or {}).get("architectural_theme"))
        n = max(1, len(words))
        gap = 18
        left, right = 40, 1240
        width = (right - left - gap * (n - 1)) / n
        for i, word in enumerate(words):
            x0 = left + i * (width + gap)
            house = [int(x0), 150, int(x0 + width), 640]
            museum = word.get("display") == "museum_text"
            draw_facade(draw, house, styles[i % len(styles)], museum)
            door = door_plaque_box(house)
            # blank brass plate, text comes later
            rounded(draw, door, 3, (214, 186, 120), (120, 90, 40), 2)
            mirror = None
            if word.get("reflexive"):
                mirror = mirror_box(house)
                draw_mirror(draw, mirror)
            hot = {
                "word_id": word["id"],
                "slug": word["id"],
                "side": word.get("side"),
                "box": [int(v) for v in house],
                "door_plaque": door,
            }
            if mirror:
                hot["mirror_box"] = mirror
            hotspots.append(hot)
    else:
        zooms = room.get("zoom_ids") or []
        zoom_side = "right"
        placed = layout_words(words, bool(zooms), zoom_side)
        for word, box in placed:
            draw_prop(draw, box, word)
            hot = {
                "word_id": word["id"],
                "slug": word["id"],
                "side": word.get("side"),
                "box": box,
            }
            if word["id"] == helper_id:
                hx1 = min(W - 8, box[2] + 8)
                hy1 = min(H - 8, box[3] + 4)
                hx0 = hx1 - 46
                hy0 = hy1 - 32
                hot["mnemonic_box"] = [hx0, hy0, hx1, hy1]
                draw_bird(draw, hot["mnemonic_box"])
            hotspots.append(hot)
        # Zoom entrance is painted as furniture and stored as a polygon hotspot.
        # It is listed first so word hotspots stay on top where they overlap.
        if zooms:
            # position is known only for zoom rooms; parent stores zoom_ids.
            # The child is loaded by the caller via room metadata if present.
            side = (room.get("_zoom_side") or "right")
            if side == "left":
                poly = [[36, 620], [560, 600], [560, 708], [36, 708]]
            elif side == "center":
                poly = [[360, 610], [920, 600], [940, 708], [340, 708]]
            else:
                poly = [[700, 618], [1244, 600], [1244, 708], [700, 708]]
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            draw_bar_counter(draw, poly)
            hotspots.insert(0, {
                "zoom_id": zooms[0],
                "slug": "zoom",
                "label": room.get("_zoom_furniture") or "closer",
                "side": side,
                "box": [min(xs), min(ys), max(xs), max(ys)],
                "polygon": poly,
            })

    out = img.resize((W, H), Image.Resampling.LANCZOS)
    dest.mkdir(parents=True, exist_ok=True)
    out.save(dest / "base.jpg", quality=86, optimize=True)
    payload = {
        "image": "base.jpg",
        "width": W,
        "height": H,
        "divider_x": 640,
        "placeholder": True,
        "note": "Text-free placeholder. Signs and labels are drawn by the site from text_areas and word records. Replace base.jpg and hotspots.json, then delete placeholder.json, when the real painting arrives.",
        "text_areas": {
            "sign": {"box": sign, "text_box": inset(sign, 28, 16)},
            "plaque": {"box": plaque, "text_box": inset(plaque, 16, 18)},
        },
        "hotspots": hotspots,
    }
    (dest / "hotspots.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (dest / "placeholder.json").write_text(json.dumps({"placeholder": True}, indent=2) + "\n", encoding="utf-8")
    return payload


def draw_bar_counter(draw, poly):
    polygon(draw, poly, (92, 60, 40), (62, 40, 26))
    # a pale top edge so it reads as a counter, still with no text
    if len(poly) >= 2:
        line(draw, poly[0], poly[1], (214, 186, 150), 4)


def rooms_to_paint(open_sectors):
    rooms = load_json(SOURCE / "rooms.json")["rooms"]
    buildings = {b["id"]: b for b in load_json(SOURCE / "buildings.json")["buildings"]}
    words = {}
    with (SOURCE / "vocab.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            word = json.loads(line)
            words[word["id"]] = word
    live_ids = set(load_json(ROOT / "content" / "site.json").get("open_rooms") or [])
    restricted = {room["sector_id"] for room in rooms if room["id"] in live_ids}
    selected = [
        room for room in rooms
        if room["sector_id"] in open_sectors
        and not (room["sector_id"] in restricted and room["id"] not in live_ids)
    ]
    by_id = {r["id"]: r for r in selected}
    for room in selected:
        if room.get("zoom_ids"):
            child = by_id.get(room["zoom_ids"][0])
            if child:
                room["_zoom_side"] = (child.get("position") or {}).get("side") or "center"
                room["_zoom_furniture"] = child.get("furniture") or "closer"
    return selected, words, buildings


def main():
    site = load_json(ROOT / "content" / "site.json")
    open_sectors = set(site.get("open_sectors") or [])
    rooms, words, buildings = rooms_to_paint(open_sectors)
    made = 0
    kept = 0
    for room in rooms:
        dest = ART / room["id"]
        marker = dest / "placeholder.json"
        existing = dest / "base.jpg"
        if existing.exists() and not marker.exists():
            kept += 1
            continue
        building = buildings.get(room["building_id"])
        paint_room(room, words, building, dest)
        made += 1
        print(f"painted {room['id']} ({room['kind']}, {room['item_count']} items)")
    print(f"placeholders written: {made}; real art left untouched: {kept}")


if __name__ == "__main__":
    main()

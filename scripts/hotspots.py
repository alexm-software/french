"""Normalize hotspot JSON from either the current vocab-id format or the
older church specimen (slug, polygon, mnemonic_box, mnemonic_for)."""

from __future__ import annotations


def _box(value):
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    x0, y0, x1, y1 = (int(round(float(v))) for v in value)
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    return [x0, y0, x1, y1]


def _polygon(value):
    if not isinstance(value, list) or len(value) < 3:
        return None
    points = []
    for pt in value:
        if not isinstance(pt, (list, tuple)) or len(pt) < 2:
            return None
        points.append([int(round(float(pt[0]))), int(round(float(pt[1])))])
    return points


def normalize_scene(raw):
    """Return a scene dict the client can draw without guessing formats."""
    if not isinstance(raw, dict):
        raise ValueError("hotspots file must be an object")
    width = int(raw.get("width") or 1280)
    height = int(raw.get("height") or 720)
    text_areas = {}
    for name, area in (raw.get("text_areas") or {}).items():
        if not isinstance(area, dict):
            continue
        box = _box(area.get("box"))
        text_box = _box(area.get("text_box")) or box
        if not box:
            continue
        text_areas[name] = {"box": box, "text_box": text_box}

    hotspots = []
    # `items` is the delivery format (id, lemma, box). `hotspots` is the older specimen.
    for item in raw.get("hotspots") or raw.get("items") or []:
        if not isinstance(item, dict):
            continue
        box = _box(item.get("box"))
        polygon = _polygon(item.get("polygon"))
        if not box and polygon:
            xs = [p[0] for p in polygon]
            ys = [p[1] for p in polygon]
            box = [min(xs), min(ys), max(xs), max(ys)]
        if not box:
            continue
        hot = {
            "word_id": item.get("word_id") or item.get("id") or None,
            "slug": item.get("slug") or item.get("lemma") or None,
            "zoom_id": item.get("zoom_id") or None,
            "mnemonic_for": item.get("mnemonic_for") or None,
            "side": item.get("side") or None,
            "label": item.get("label") or None,
            "helper": bool(item.get("helper")),
            "box": box,
        }
        if polygon:
            hot["polygon"] = polygon
        mnemonic_box = _box(item.get("mnemonic_box"))
        if mnemonic_box:
            hot["mnemonic_box"] = mnemonic_box
        door = _box(item.get("door_plaque"))
        if door:
            hot["door_plaque"] = door
        mirror = _box(item.get("mirror_box"))
        if mirror:
            hot["mirror_box"] = mirror
        hotspots.append(hot)

    return {
        "image": raw.get("image") or "base.jpg",
        "width": width,
        "height": height,
        "divider_x": int(raw.get("divider_x") or width // 2),
        "placeholder": bool(raw.get("placeholder")),
        "text_areas": text_areas,
        "hotspots": hotspots,
    }

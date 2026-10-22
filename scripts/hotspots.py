"""Normalize hotspot JSON.

Accepts the church specimen (hotspots, slug, polygon, mnemonic_box) and the
painting delivery format (items, links, exits, zoom_from, text on text_areas,
door_plaque_box).
"""

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


def _hot(item):
    if not isinstance(item, dict):
        return None
    box = _box(item.get("box"))
    polygon = _polygon(item.get("polygon"))
    if not box and polygon:
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        box = [min(xs), min(ys), max(xs), max(ys)]
    if not box:
        return None
    hot = {
        "word_id": item.get("word_id") or item.get("id") or None,
        "slug": item.get("slug") or item.get("lemma") or None,
        "zoom_id": item.get("zoom_id") or None,
        "mnemonic_for": item.get("mnemonic_for") or None,
        "side": item.get("side") or None,
        "tier": item.get("tier") or None,
        "label": item.get("label") or None,
        "helper": bool(item.get("helper")),
        "box": box,
    }
    if polygon:
        hot["polygon"] = polygon
    mnemonic_box = _box(item.get("mnemonic_box"))
    if mnemonic_box:
        hot["mnemonic_box"] = mnemonic_box
    door = _box(item.get("door_plaque")) or _box(item.get("door_plaque_box"))
    if door:
        hot["door_plaque"] = door
    mirror = _box(item.get("mirror_box"))
    if mirror:
        hot["mirror_box"] = mirror
    label_xy = item.get("label_xy")
    if isinstance(label_xy, (list, tuple)) and len(label_xy) >= 2:
        hot["label_xy"] = [int(round(float(label_xy[0]))), int(round(float(label_xy[1])))]
    return hot


def exit_kind(key):
    return {
        "prev": "back",
        "back": "back",
        "next": "forward",
        "forward": "forward",
        "left": "left",
        "right": "right",
    }.get(str(key or ""), "")


def _area(area):
    if not isinstance(area, dict):
        return None
    box = _box(area.get("box"))
    text_box = _box(area.get("text_box")) or box
    if not box:
        return None
    payload = {"box": box, "text_box": text_box}
    if area.get("text"):
        payload["text"] = str(area["text"])
    if area.get("role"):
        payload["role"] = str(area["role"])
    if area.get("for_exit"):
        payload["for_exit"] = str(area["for_exit"])
    if area.get("for"):
        payload["for"] = str(area["for"])
    return payload


def normalize_scene(raw):
    """Return a scene dict the client can draw without guessing formats."""
    if not isinstance(raw, dict):
        raise ValueError("hotspots file must be an object")
    width = int(raw.get("width") or 1280)
    height = int(raw.get("height") or 720)
    text_areas = {}
    for name, area in (raw.get("text_areas") or {}).items():
        parsed = _area(area)
        if parsed:
            text_areas[name] = parsed

    hotspots = []
    for item in raw.get("hotspots") or raw.get("items") or []:
        hot = _hot(item)
        if hot:
            hotspots.append(hot)

    links = []
    for item in raw.get("links") or []:
        if not isinstance(item, dict):
            continue
        box = _box(item.get("box"))
        if not box or not item.get("target"):
            continue
        link = {
            "target": item["target"],
            "box": box,
            "label": item.get("label") or "",
        }
        for key in ("name", "name_fr", "name_en", "label_fr", "label_en", "kind", "signed_by"):
            if item.get(key):
                link[key] = str(item[key])
        arrow = exit_kind(item.get("arrow"))
        if arrow:
            link["arrow"] = arrow
        polygon = _polygon(item.get("polygon"))
        if polygon:
            link["polygon"] = polygon
        links.append(link)

    exits = {}
    for key, item in (raw.get("exits") or {}).items():
        if not isinstance(item, dict):
            continue
        box = _box(item.get("box"))
        if not box:
            continue
        exit_item = {"box": box, "target": item.get("target")}
        for field in ("label", "name", "name_fr", "name_en", "label_fr", "label_en", "kind"):
            if item.get(field):
                exit_item[field] = str(item[field])
        polygon = _polygon(item.get("polygon"))
        if polygon:
            exit_item["polygon"] = polygon
        exits[key] = exit_item

    raw_zoom = raw.get("zoom_from")
    zoom_items = raw_zoom if isinstance(raw_zoom, list) else [raw_zoom] if isinstance(raw_zoom, dict) else []
    zoom_regions = []
    for item in zoom_items:
        if not isinstance(item, dict):
            continue
        box = _box(item.get("box"))
        if box and item.get("room_id"):
            zoom_regions.append({
                "room_id": str(item["room_id"]),
                "box": box,
                "label": item.get("label") or "",
            })
    zoom_from = zoom_regions[0] if len(zoom_regions) == 1 else None

    return {
        "image": raw.get("image") or "base.jpg",
        "width": width,
        "height": height,
        "divider_x": raw.get("divider_x"),
        "kind": raw.get("kind"),
        "layout": raw.get("layout"),
        "placeholder": bool(raw.get("placeholder")),
        "text_areas": text_areas,
        "hotspots": hotspots,
        "links": links,
        "exits": exits,
        "zoom_from": zoom_from,
        "zoom_regions": zoom_regions,
    }

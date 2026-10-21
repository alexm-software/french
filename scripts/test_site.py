#!/usr/bin/env python3
"""Checks the built site data and the church hotspot specimen."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotspots import normalize_scene

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
EXAMPLE = ROOT / "content" / "examples" / "eglise" / "hotspots.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


MAP = "village_map"

# Every open café-quarter view and the strip button's hierarchy parent.
# Painted exits are not a substitute: cooking segments paint a step back to
# the square, and both restaurant zooms paint a back link on the bottom edge
# that a cropped frame can hide.
S04_BACK = {
    "S04_cafes": MAP,
    "B08_cafe": "S04_cafes",
    "B09_restaurant": "S04_cafes",
    "ST_cooking": "S04_cafes",
    "R_cafe_01": "B08_cafe",
    "R_cafe_02": "B08_cafe",
    "R_resto_kitchen_01": "B09_restaurant",
    "R_resto_kitchen_02": "B09_restaurant",
    "R_resto_room": "B09_restaurant",
    "R_wine_01": "B09_restaurant",
    "R_resto_room_z1": "R_resto_room",
    "R_wine_01_z1": "R_wine_01",
    "ST_cooking_seg001": "ST_cooking",
    "ST_cooking_seg002": "ST_cooking",
    "ST_cooking_seg003": "ST_cooking",
    "ST_cooking_seg004": "ST_cooking",
    "ST_cooking_seg005": "ST_cooking",
    "ST_cooking_seg006": "ST_cooking",
    "ST_cooking_seg007": "ST_cooking",
}


def _reachable(start, graph):
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.get(node, ()))
    return seen


def assert_s04_explicit(hierarchy, sectors, buildings, rooms):
    """Name every café-quarter view and require its strip parent.

    Following only those parents must reach the village map. A painted
    exit, including a zoom link sitting on the cropped edge, does not count.
    """
    present = {sector["id"] for sector in sectors if sector["id"] == "S04_cafes"}
    present |= {building["id"] for building in buildings if building.get("sector_id") == "S04_cafes"}
    present |= {room["id"] for room in rooms if room.get("sector_id") == "S04_cafes"}
    missing = sorted(present - set(S04_BACK))
    extra = sorted(set(S04_BACK) - present)
    assert not missing, f"S04 views missing from the dead-end list: {missing}"
    assert not extra, f"dead-end list names views that are not in S04: {extra}"
    for view, parent in S04_BACK.items():
        actual = hierarchy.get(view)
        assert actual == parent, f"{view}: strip back is {actual}, expected {parent}"
        node = view
        seen = []
        while node != MAP:
            assert node not in seen, f"{view} loops at {node}"
            seen.append(node)
            node = hierarchy.get(node)
            assert node, f"{view} stops at {seen[-1]} before the village map"
    painted = load(ROOT / "content" / "art" / "ST_cooking_seg001" / "hotspots.json")
    assert painted["exits"]["back"]["target"] == "S04_sector"
    assert S04_BACK["ST_cooking_seg001"] == "ST_cooking"
    for zoom_id in ("R_resto_room_z1", "R_wine_01_z1"):
        art = load(ROOT / "content" / "art" / zoom_id / "hotspots.json")
        link = next(item for item in art["links"] if item.get("kind") == "zoom_back")
        # The step back meets the bottom of the painting, even when the box starts higher.
        assert link["box"][3] >= art["height"] - 120, (zoom_id, link["box"])
        built = load(DATA / "rooms" / f"{zoom_id}.json")
        assert built["kind"] == "zoom"
        assert built["parent"]["id"] == S04_BACK[zoom_id]
    for view, parent in S04_BACK.items():
        path = DATA / "rooms" / f"{view}.json"
        if not path.exists():
            continue
        built = load(path)
        if built.get("kind") == "zoom":
            assert built["parent"]["id"] == parent, view
        else:
            assert built.get("building_id") == parent, view


def assert_fullscreen_overlays():
    """Overlays stay visible in fullscreen, and the strip button is one toggle."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    body = html.split("<body>", 1)[1].split("</body>", 1)[0]
    assert body.index('<div id="stage">') < body.index('id="guide-host"') < body.rindex("</div>")
    client = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    assert 'document.documentElement.requestFullscreen' in client
    assert "stage.requestFullscreen" not in client
    assert "exitFullscreen" not in client.split("function render", 1)[1].split("function onClick", 1)[0]
    mount = client.split("function mountGuide", 1)[1].split("let playToken", 1)[0]
    assert 'querySelector("#stage")' in mount
    assert "document.body.appendChild" not in mount
    assert "collapse:" in client
    shell = client.split("function shell", 1)[1].split("function backTarget", 1)[0]
    assert 'doodle(fullscreen ? "collapse" : "expand")' in shell
    sync = client.split('addEventListener("fullscreenchange"', 1)[1].split("window.addEventListener(\"hashchange\"", 1)[0]
    assert ".tool-icon" in sync
    assert 'doodle(fullscreen ? "collapse" : "expand")' in sync
    keys = client.split("function onKey", 1)[1].split("window.addEventListener(\"keydown\"", 1)[0]
    dialog = keys.split('querySelector(".dialog-layer")', 1)[1].split("fullscreenElement", 1)[0]
    assert "preventDefault" in dialog
    assert keys.index("fullscreenElement") < keys.index('room?.kind === "zoom"')
    css = (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    assert ".tool[data-fs]" in css


def _point_inside(point, polygon):
    x, y = point
    hits = False
    count = len(polygon)
    for index in range(count):
        x0, y0 = polygon[index]
        x1, y1 = polygon[(index + 1) % count]
        if (y0 > y) != (y1 > y):
            cross = x0 + (y - y0) / (y1 - y0) * (x1 - x0)
            if x < cross:
                hits = not hits
    return hits


def _exit_hit(exit_item):
    """The clickable street: a polygon when the far lane is drawn, else the box."""
    polygon = exit_item.get("polygon")
    if polygon and len(polygon) >= 4:
        return polygon
    box = exit_item["box"]
    return [[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]]


def assert_wide_passages():
    """Street continuations and doorways are big hit areas, not just their labels."""
    from hotspots import normalize_scene

    segments = tuple(f"ST_cooking_seg{index:03d}" for index in range(1, 8))
    for segment in segments:
        raw = load(ROOT / "content" / "art" / segment / "hotspots.json")
        assert raw.get("view") == "street_perspective", segment
        assert raw["items"] and all(item.get("label_xy") for item in raw["items"]), segment
        scene = normalize_scene(raw)
        items = scene["hotspots"]
        for key in ("forward", "back"):
            exit_item = scene["exits"][key]
            # Head-on lanes can be a little under 15% of the width at the vanishing
            # point (étape 3's far street is 183px on a 1280-wide painting). The
            # near cobbles are a box along the bottom edge, not a polygon.
            polygon = _exit_hit(exit_item)
            xs = [point[0] for point in polygon]
            ys = [point[1] for point in polygon]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)
            assert width >= 180 and height >= 60, (segment, key, width, height)
            box = exit_item["box"]
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            assert _point_inside(center, polygon), (segment, key)
            for item in items:
                item_box = item["box"]
                item_center = ((item_box[0] + item_box[2]) / 2, (item_box[1] + item_box[3]) / 2)
                assert not _point_inside(item_center, polygon), (segment, key, item["word_id"])
    sector = normalize_scene(load(ROOT / "content" / "art" / "S04_sector" / "hotspots.json"))
    street = next(link for link in sector["links"] if link["kind"] == "street")
    assert street["polygon"]
    street_width = max(point[0] for point in street["polygon"]) - min(point[0] for point in street["polygon"])
    assert street_width >= int(sector["width"] * 0.15)
    room = normalize_scene(load(ROOT / "content" / "art" / "R_resto_room" / "hotspots.json"))
    door = next(link for link in room["links"] if link["kind"] == "door")
    arch = next(link for link in room["links"] if "rch" in link["label"].lower())
    for opening in (door, arch):
        box = opening["box"]
        hit = opening.get("polygon") or [
            [box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]],
        ]
        width = max(point[0] for point in hit) - min(point[0] for point in hit)
        height = max(point[1] for point in hit) - min(point[1] for point in hit)
        assert min(width, height) >= 60 and width * height >= 8000, (opening["label"], width, height)
    client = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    assert 'polygon class="hit"' in client
    assert "hitShape(link)" in client and "hitShape(exit)" in client
    assert "wordLabel(" in client
    assert "Math.max(22, y0 - 6)" not in client
    cafe = normalize_scene(load(ROOT / "content" / "art" / "R_cafe_01" / "hotspots.json"))
    labelled = next(hot for hot in cafe["hotspots"] if hot.get("label_xy"))
    assert labelled["label_xy"][1] > labelled["box"][1]


def assert_back_strip_stays_visible(client):
    """The strip back is a header control, not an item in the menu that hides under 820px."""
    shell = client.split("function shell", 1)[1].split("function backTarget", 1)[0]
    assert shell.index("${opts.backNav") < shell.index('<nav class="nav">')
    scene = client.split("function sceneNav", 1)[1].split("function crumbs", 1)[0]
    assert "backNav" not in scene
    assert "backNav: backNav(state.place)" in client
    keys = client.split("function onKey", 1)[1].split("window.addEventListener(\"keydown\"", 1)[0]
    assert 'event.key === "Escape"' in keys
    assert "room?.kind === \"zoom\"" in keys
    assert "backTarget(state.place)" in keys
    css = (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    assert ".nav a.back" not in css
    assert "a.back" in css
    assert 'preserveAspectRatio="xMidYMid meet"' in client
    assert 'preserveAspectRatio="xMidYMid slice"' not in client
    assert 'class="bleed"' in client and 'class="painting"' in client
    assert "object-fit: contain" in css
    painting_css = css.split(".frame img.painting", 1)[1].split("}", 1)[0]
    bleed_css = css.split(".frame img.bleed", 1)[1].split("}", 1)[0]
    assert "object-fit: contain" in painting_css
    assert "object-fit: cover" in bleed_css and "blur" in bleed_css
    narrow = css.split("@media (max-width: 820px)", 1)[1].split("@media", 1)[0]
    assert "display: none" in narrow and ".nav" in narrow
    assert "a.back" in narrow


def walk_site_graph():
    """Every space can reach the village map, and the map can reach every space.

    Upward edges are the strip back button (sector → map, building → sector,
    room → building, zoom → parent). Downward edges are the same hierarchy
    plus painted links and exits. A dead end cannot get back to the map.
    An orphan cannot be reached from it.
    """
    source = ROOT / "data" / "source"
    sectors = load(source / "sectors.json")["sectors"]
    buildings = load(source / "buildings.json")["buildings"]
    rooms = load(source / "rooms.json")["rooms"]
    sector_ids = {sector["id"] for sector in sectors}
    building_ids = {building["id"] for building in buildings}
    room_ids = {room["id"] for room in rooms}
    art_to_sector = {f"{sector['id'].split('_')[0]}_sector": sector["id"] for sector in sectors}
    nodes = {MAP} | sector_ids | building_ids | room_ids
    graph = {node: set() for node in nodes}
    reverse = defaultdict(set)
    hierarchy = {}

    def edge(src, dst, why):
        if src not in nodes or dst not in nodes:
            raise AssertionError(f"{why}: {src} -> {dst} leaves the site graph")
        graph[src].add(dst)
        reverse[dst].add(src)

    def back_edge(src, dst, why):
        assert hierarchy.get(src, dst) == dst, f"{src} has two strip parents: {hierarchy.get(src)} and {dst}"
        hierarchy[src] = dst
        edge(src, dst, why)

    listed = defaultdict(set)
    for sector in sectors:
        edge(MAP, sector["id"], "map pin")
        back_edge(sector["id"], MAP, "back to the village map")
        for key in ("buildings", "streets"):
            for building_id in sector.get(key) or []:
                listed[building_id].add(sector["id"])
                edge(sector["id"], building_id, "sector contains building")

    for building in buildings:
        owners = listed.get(building["id"]) or set()
        assert owners == {building["sector_id"]}, (building["id"], owners, building.get("sector_id"))
        back_edge(building["id"], building["sector_id"], "back to the sector")
        for room_id in building.get("rooms") or []:
            edge(building["id"], room_id, "building contains room")

    zoom_ids = {room["id"]: set(room.get("zoom_ids") or []) for room in rooms}
    for room in rooms:
        if room.get("kind") == "zoom":
            parent = room.get("parent_room_id")
            assert parent in room_ids, room["id"]
            assert room["id"] in zoom_ids.get(parent, ()), room["id"]
            back_edge(room["id"], parent, "back to the parent room")
        else:
            assert room.get("building_id") in building_ids, room["id"]
            back_edge(room["id"], room["building_id"], "back to the building")
        for zoom_id in zoom_ids[room["id"]]:
            edge(room["id"], zoom_id, "room contains zoom")

    def resolve(target):
        if str(target).endswith("_sector"):
            return art_to_sector.get(target)
        if target in building_ids:
            return target
        if target in room_ids:
            return target
        return None

    art = ROOT / "content" / "art"
    for path in sorted(art.glob("*/hotspots.json")):
        folder = path.parent.name
        owner = art_to_sector.get(folder) or (folder if folder in nodes else None)
        assert owner, f"painted folder {folder} is not a space"
        raw = load(path)
        targets = []
        for item in raw.get("links") or []:
            if isinstance(item, dict) and item.get("target"):
                targets.append(item["target"])
        for item in (raw.get("exits") or {}).values():
            if isinstance(item, dict) and item.get("target"):
                targets.append(item["target"])
        zoom = raw.get("zoom_from") or []
        zoom_items = zoom if isinstance(zoom, list) else [zoom]
        for item in zoom_items:
            if isinstance(item, dict) and item.get("room_id"):
                targets.append(item["room_id"])
        for target in targets:
            dest = resolve(target)
            assert dest, f"{folder} links to unknown space {target}"
            edge(owner, dest, "painted link")

    reached = _reachable(MAP, graph)
    can_leave = _reachable(MAP, reverse)
    orphans = sorted(nodes - reached)
    dead = sorted(nodes - can_leave)
    assert not orphans, f"orphans (map cannot reach): {orphans[:12]}"
    assert not dead, f"dead ends (cannot reach map): {dead[:12]}"
    assert len(rooms) == 859, len(rooms)
    # Close-ups hold 3–12 items. A mixed-gender shelf is the back wall, not a side wall.
    genders = {}
    with (source / "vocab.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            word = json.loads(line)
            genders[word["id"]] = word.get("gender") if word.get("pos") == "noun" else None
    new_zooms = {
        "R_abs_beauty_01_z1", "R_abs_beauty_02_z1", "R_abs_beauty_03_z1",
        "R_florist_z1", "R_hardware_01_z1", "R_hardware_02_z1",
        "R_shop_general_02_z1", "R_shop_general_03_z1", "R_shop_general_04_z1",
    }
    seen_zooms = set()
    for room in rooms:
        if room.get("kind") != "zoom":
            continue
        count = len(room.get("words") or [])
        assert 3 <= count <= 12, (room["id"], count)
        if room["id"] not in new_zooms:
            continue
        seen_zooms.add(room["id"])
        noun_genders = {genders.get(word_id) for word_id in room["words"]} - {None}
        wall = (room.get("position") or {}).get("wall")
        if noun_genders >= {"m", "f"}:
            assert wall == "back wall", (room["id"], wall, noun_genders)
    assert seen_zooms == new_zooms
    assert len(nodes) == 1 + len(sectors) + len(buildings) + len(rooms), len(nodes)
    stray = sorted(nodes - {MAP} - set(hierarchy))
    assert not stray, f"strip back missing: {stray[:12]}"

    client = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    assert "data-back" in client and "nav.backMap" in client and "nav.backTo" in client
    assert_s04_explicit(hierarchy, sectors, buildings, rooms)
    assert_back_strip_stays_visible(client)


def main():
    index = load(DATA / "index.json")
    assert index["open_sectors"] == ["S01_beginner", "S02_home", "S03_market", "S04_cafes"], index["open_sectors"]
    site_rooms = sorted(load(ROOT / "content" / "site.json")["open_rooms"])
    assert index["open_rooms"] == site_rooms, index["open_rooms"]
    assert len(site_rooms) == 130
    assert {"R_alphabet_01", "R_numbers2", "R_pronouns_03", "R_abs_quantity_01", "ST_commerce_seg001", "R_entrance_01", "R_bathroom"} <= set(site_rooms)
    assert index["featured"]["kind"] == "sector"
    assert index["featured"]["id"] == "S01_beginner"
    assert len(index["sectors"]) == 16
    assert index["start"] == "S01_beginner"
    assert any(item["id"] == "faith_first" for item in index["alternatives"])
    assert index["route_legs"], "walking legs missing"
    locked = [sector["id"] for sector in index["sectors"] if not sector["open"]]
    assert "S01_beginner" not in locked and "S02_home" not in locked and "S03_market" not in locked and "S11_church" in locked
    assert all(sector["x"] and sector["y"] for sector in index["sectors"])

    sector = load(DATA / "sectors" / "S04_cafes.json")
    assert sector["open"] is True
    ids = [building["id"] for building in sector["buildings"]]
    assert ids == ["B08_cafe", "B09_restaurant", "ST_cooking"], ids
    assert sector["scene"]["image"].endswith("art/S04_sector/base.jpg")
    assert sector["scene"]["sign_text"] == "Rue des Saveurs"
    assert sector["description_fr"].startswith("La terrasse")
    cooking = next(link for link in sector["scene"]["links"] if link["target"] == "ST_cooking_seg001")
    assert cooking["name"] == "Ruelle des Gourmets — étape 1"
    assert sector["scene"]["placeholder"] is False
    link_targets = [link["target"] for link in sector["scene"]["links"]]
    assert link_targets == ["B08_cafe", "B09_restaurant", "ST_cooking_seg001"], link_targets
    assert len(sector["alleys"]) == 7
    assert [alley["id"] for alley in sector["alleys"]] == [f"ST_cooking_seg{i:03d}" for i in range(1, 8)]
    assert sector["alleys"][0]["verbs"][0] == "manger"
    assert "nourrir" in sector["alleys"][0]["verbs"]
    assert "bannir" not in {verb for alley in sector["alleys"] for verb in alley["verbs"]}

    street = next(building for building in sector["buildings"] if building["id"] == "ST_cooking")
    segments = [room["id"] for room in street["floors"][0]["rooms"]]
    assert segments == [f"ST_cooking_seg{i:03d}" for i in range(1, 8)], segments
    assert [room["chip"] for room in street["floors"][0]["rooms"]] == ["1", "2", "3", "4", "5", "6", "7"]
    assert "ST_cooking" not in sector["walk"]
    assert not any(room_id.startswith("ST_cooking") for room_id in sector["walk"])

    restaurant = next(building for building in sector["buildings"] if building["id"] == "B09_restaurant")
    ground = restaurant["floors"][0]["rooms"]
    assert [room["id"] for room in ground] == ["R_resto_kitchen_01", "R_resto_room", "R_wine_01"], [room["id"] for room in ground]
    assert any(link["target"] == "R_resto_room" for link in restaurant["scene"]["links"])
    cafe_building = next(building for building in sector["buildings"] if building["id"] == "B08_cafe")
    assert {link["target"] for link in cafe_building["scene"]["links"]} == {"R_cafe_01", "R_cafe_02"}

    cafe = load(DATA / "rooms" / "R_cafe_01.json")
    assert cafe["sign"] == "La terrasse"
    assert cafe["scene"]["placeholder"] is False
    assert [floor["label"] for floor in cafe["floors"]] == ["Ground floor", "Upstairs"]
    word_ids = {word["id"] for word in cafe["words"]}
    hot_ids = {hot.get("word_id") for hot in cafe["scene"]["hotspots"] if hot.get("word_id") and not hot.get("helper")}
    assert word_ids <= hot_ids

    upstairs = load(DATA / "rooms" / "R_cafe_02.json")
    assert upstairs["floor_label"] == "Upstairs"
    assert upstairs["sign"] == "L'étage"
    assert upstairs["scene"]["placeholder"] is False
    assert not upstairs["scene"].get("plaque_text")
    assert len(upstairs["words"]) == 9
    barman = next(word for word in upstairs["words"] if word["id"] == "fr_barman_noun")
    assert barman["mnemonic_explain"] and barman["gender"] == "m" and barman["head"] == "le barman"
    barman_hits = [hot for hot in upstairs["scene"]["hotspots"] if hot.get("word_id") == "fr_barman_noun" and not hot.get("helper")]
    assert len(barman_hits) == 1
    assert barman_hits[0]["label_xy"][1] >= barman_hits[0]["box"][1]
    assert barman["example_fr"] and barman["example_en"]
    assert "flelex_freq" not in barman and "cefr_flelex" not in barman

    dining = load(DATA / "rooms" / "R_resto_room.json")
    zoom = next(hot for hot in dining["scene"]["hotspots"] if hot.get("zoom_id") == "R_resto_room_z1")
    assert zoom["box"] and zoom["label"] == "Le comptoir"
    ground_ids = [room["id"] for room in dining["floors"][0]["rooms"]]
    assert ground_ids == ["R_resto_kitchen_01", "R_resto_room", "R_wine_01"], ground_ids
    bar = load(DATA / "rooms" / "R_resto_room_z1.json")
    assert bar["parent"]["id"] == "R_resto_room"
    assert bar["words"]
    assert (ROOT / "public" / "art" / "R_resto_room" / "base.jpg").stat().st_size > 100000
    assert (ROOT / "public" / "art" / "R_resto_kitchen_01" / "base.jpg").stat().st_size > 100000

    kitchen = load(DATA / "rooms" / "R_resto_kitchen_02.json")
    assert kitchen["floor"] == 2

    seg = load(DATA / "rooms" / "ST_cooking_seg001.json")
    lemmas = {word["lemma"] for word in seg["words"]}
    assert "manger" in lemmas and "nourrir" in lemmas and "servir" not in lemmas
    assert seg["scene"]["layout"] == "tiered"
    assert seg["scene"]["exits"]["back"]["target"] == "S04_sector"
    assert seg["scene"]["exits"]["forward"]["target"] == "ST_cooking_seg002"
    assert seg["scene"]["links"] == []
    assert seg["name_fr"] == "Étape 1 · Manger et nourrir"
    areas = seg["scene"]["text_areas"]
    assert areas["dir_forward"]["role"] == "direction" and areas["dir_forward"]["text"] == "étape 2 →"
    assert areas["dir_side_er"]["text"] == "-er"
    assert areas["dir_side_irre"]["text"] == "-ir / -re"
    assert "fr_servir_verb_sign" not in areas
    raw_items = load(ROOT / "content" / "art" / "ST_cooking_seg001" / "hotspots.json")["items"]
    for item in raw_items:
        hits = [hot for hot in seg["scene"]["hotspots"] if hot.get("word_id") == item["id"] and not hot.get("helper")]
        assert len(hits) == 1, item["id"]
        assert "mnemonic_box" not in hits[0]
        box = hits[0]["box"]
        assert box[0] <= item["box"][0] and box[1] <= item["box"][1] and box[2] >= item["box"][2] and box[3] >= item["box"][3]
    assert seg["conversation"]["title"] == "Pique-nique au bord du lac"
    assert seg["conversation"]["lines"] and seg["conversation"]["lines"][0]["fr"]
    assert seg["prev"] is None and seg["next"] is None
    assert not any(str(item["id"]).startswith("ST_") for item in seg["related"])
    snack = load(DATA / "rooms" / "ST_cooking_seg002.json")
    servir = next(word for word in snack["words"] if word["lemma"] == "servir")
    assert snack["scene"]["text_areas"]["fr_servir_verb_sign"]["text"] == "servir (à / de)"
    assert "fr_servir_verb_plaque" not in snack["scene"]["text_areas"]
    assert servir["prepositions"] == ["à", "de"]
    assert servir["conjugations"]["present"][0] == "je sers"
    assert servir["conjugations"]["participe_passe"] == "servi"
    assert servir["conjugations"]["participe_present"] == "servant"
    assert load(DATA / "rooms" / "R_cafe_01.json")["name_fr"] == "La terrasse"
    assert servir["conjugations"]["imperatif"] == ["sers", "servons", "servez"]
    assert servir["example_fr"] and servir["example_en"]

    last = load(DATA / "rooms" / "ST_cooking_seg007.json")
    assert last["sign"] == "Ruelle des Gourmets"
    assert last["name_fr"] == "Étape 7 · Cuire et rôtir"
    assert last["scene"]["layout"] == "tiered"
    assert last["scene"]["exits"]["forward"]["target"] == "S04_sector"
    assert last["scene"]["exits"]["back"]["target"] == "ST_cooking_seg006"
    assert [room["chip"] for room in last["floors"][0]["rooms"]] == ["1", "2", "3", "4", "5", "6", "7"]
    assert not any(hot.get("mirror") or hot.get("helper") for hot in last["scene"]["hotspots"])
    assert not (DATA / "rooms" / "ST_cooking_seg011.json").exists()
    assert (DATA / "rooms" / "ST_cooking_seg005.json").exists()
    assert not (ROOT / "content" / "art" / "ST_cooking_seg011").exists()

    wine = load(DATA / "rooms" / "R_wine_01.json")
    cave = next(word for word in wine["words"] if word["lemma"] == "cave")
    assert cave["cognate_type"] == "false_cognate"
    assert cave["false_cognate_note"]
    assert len(wine["words"]) == 14
    assert all(word["lemma"] not in {"whisky", "rhum", "cognac", "cigare"} for word in wine["words"])
    assert all(word["painted"] for word in wine["words"])
    zoom_wine = load(DATA / "rooms" / "R_wine_01_z1.json")
    assert zoom_wine["parent"]["id"] == "R_wine_01"
    assert zoom_wine["parent"]["name_fr"] == "La cave"
    assert len(zoom_wine["words"]) == 10
    for lemma in ("whisky", "rhum", "cognac", "cigare", "champagne", "cru"):
        drawn = next(word for word in zoom_wine["words"] if word["lemma"] == lemma)
        assert drawn["painted"] is True, lemma
    assert all(word["lemma"] not in {"champagne", "cru"} for word in wine["words"])
    assert any(hot.get("word_id") == "fr_whisky_noun" and not hot.get("helper") for hot in zoom_wine["scene"]["hotspots"])
    assert "plaque" not in load(ROOT / "content" / "art" / "B08_cafe" / "hotspots.json")["text_areas"]
    assert "plaque" not in load(ROOT / "content" / "art" / "B09_restaurant" / "hotspots.json")["text_areas"]

    room_files = sorted(path.name for path in (DATA / "rooms").glob("*.json"))
    assert len(room_files) == 145, len(room_files)
    greet = load(DATA / "rooms" / "R_greet.json")
    assert greet["scene"]["image"].endswith("art/R_greet/base.jpg")
    assert all(hot.get("label_xy") for hot in greet["scene"]["hotspots"] if hot.get("word_id") and not hot.get("helper"))
    square = load(DATA / "sectors" / "S01_beginner.json")
    assert square["open"] is True
    assert square["scene"]["image"].endswith("art/S01_sector/base.jpg")
    soon = {link["target"] for link in square["scene"]["links"] if link.get("soon")}
    assert soon == set(), soon
    open_doors = {link["target"] for link in square["scene"]["links"] if not link.get("soon")}
    assert open_doors == {"B01_fontaine", "B02_ecole", "B03_horloge", "B04_atelier_couleurs", "S02_sector", "S04_sector"}, open_doors
    stairs = {
        ("B04_atelier_couleurs", "R_shapes_03"): ("stairs", "stairs_down"),
        ("R_colors_02", "R_shapes_02"): ("stairs", "stairs_down"),
        ("R_adv_time_01", "R_time_clock_02"): ("stairs_up", "stairs_down"),
        ("R_abs_time_01", "R_adv_time_03"): ("stairs_up", "stairs_down"),
        ("R_pronouns_01", "R_numbers2"): ("stairs_up", "stairs_down"),
        ("R_conjunctions", "R_pronouns_03"): ("stairs_up", "stairs_down"),
        ("R_abs_quantity_03", "R_adv_degree_02"): ("stairs_up", "stairs_down"),
        ("R_living", "R_bedroom_01"): ("stairs_up", "stairs_down"),
        ("R_bedroom_02", "R_attic"): ("stairs_up", "stairs_down"),
    }
    for (src, dest), (up_kind, down_kind) in stairs.items():
        raw = load(ROOT / "content" / "art" / src / "hotspots.json")
        link = next(item for item in raw["links"] if item["target"] == dest)
        assert link["kind"] == up_kind, (src, link["kind"])
        back = load(ROOT / "content" / "art" / dest / "hotspots.json")
        returns = [item for item in back["links"] if item["target"] == src]
        assert returns and returns[0]["kind"] == down_kind, (dest, returns)
    gallery = load(ROOT / "content" / "art" / "R_entrance_01_z1" / "hotspots.json")
    assert next(item for item in gallery["links"] if item["target"] == "R_bedroom_02")["kind"] == "stairs_up"
    dream = load(ROOT / "content" / "art" / "R_bedroom_02" / "hotspots.json")
    assert next(item for item in dream["links"] if item["target"] == "R_entrance_01")["kind"] == "stairs_down"
    colors = load(DATA / "rooms" / "R_colors_01.json")
    assert colors["building_id"] == "B04_atelier_couleurs"
    assert any(link["target"] == "R_colors_02" for link in colors["scene"]["links"])
    classroom = load(DATA / "rooms" / "R_alphabet_01.json")
    assert classroom["building_id"] == "B02_ecole"
    assert any(link["target"] == "R_alphabet_02" for link in classroom["scene"]["links"])
    market = load(DATA / "sectors" / "S03_market.json")
    assert market["open"] is True
    assert market["scene"]["image"].endswith("art/S03_sector/base.jpg")
    soon_market = {link["target"] for link in market["scene"]["links"] if link.get("soon")}
    assert soon_market == {
        "B62_couture", "B06_marche", "B07_rue_commercante", "B61_reparation", "B59_brocante",
    }, soon_market
    open_market = {link["target"] for link in market["scene"]["links"] if not link.get("soon")}
    assert open_market == {"B60_balance", "ST_commerce_seg001", "S01_sector", "S02_sector"}, open_market
    commerce = load(ROOT / "content" / "art" / "ST_commerce_seg001" / "hotspots.json")
    assert commerce["view"] == "street_perspective"
    assert commerce["exits"]["forward"]["target"] == "ST_commerce_seg002"
    assert commerce["exits"]["back"]["target"] == "S03_sector"
    quantity = load(DATA / "rooms" / "R_abs_quantity_01.json")
    assert quantity["building_id"] == "B60_balance"
    assert any(link["target"] == "R_abs_quantity_02" for link in quantity["scene"]["links"])
    home = load(DATA / "sectors" / "S02_home.json")
    assert home["open"] is True
    assert home["scene"]["image"].endswith("art/S02_sector/base.jpg")
    assert {link["target"] for link in home["scene"]["links"]} == {"B05_maison", "S01_sector", "ST_routine_seg001", "ST_control_seg001"}
    assert not any(link.get("soon") for link in home["scene"]["links"])
    control = load(ROOT / "content" / "art" / "ST_control_seg001" / "hotspots.json")
    assert control["view"] == "street_perspective"
    assert control["exits"]["forward"]["target"] == "ST_control_seg002"
    assert control["exits"]["back"]["target"] == "S02_sector"
    for index in range(2, 18):
        segment = load(ROOT / "content" / "art" / f"ST_control_seg{index:03d}" / "hotspots.json")
        assert segment["exits"]["forward"]["target"] == f"ST_control_seg{index + 1:03d}"
        assert segment["exits"]["back"]["target"] == f"ST_control_seg{index - 1:03d}"
    end = load(ROOT / "content" / "art" / "ST_control_seg018" / "hotspots.json")
    assert end["exits"]["forward"]["target"] == "S02_sector"
    assert end["exits"]["back"]["target"] == "ST_control_seg017"
    routine = load(ROOT / "content" / "art" / "ST_routine_seg001" / "hotspots.json")
    assert routine["view"] == "street_perspective"
    assert routine["exits"]["forward"]["target"] == "ST_routine_seg002"
    assert routine["exits"]["back"]["target"] == "S02_sector"
    last = load(ROOT / "content" / "art" / "ST_routine_seg019" / "hotspots.json")
    assert last["exits"]["forward"]["target"] == "S02_sector"
    assert last["exits"]["back"]["target"] == "ST_routine_seg018"
    house = next(item for item in home["buildings"] if item["id"] == "B05_maison")
    assert house["scene"]["image"].endswith("art/B05_maison/base.jpg")
    assert any(link["target"] == "R_entrance_04" and not link.get("soon") for link in house["scene"]["links"])
    entrance = load(DATA / "rooms" / "R_entrance_01.json")
    assert entrance["building_id"] == "B05_maison"
    assert any(link["target"] == "R_living" for link in entrance["scene"]["links"])
    outside = {"R_entrance_03", "R_garage", "R_garden", "R_kitchen_01", "R_pets"}
    upstairs = {
        "R_bedroom_01", "R_bedroom_02", "R_attic", "R_playroom", "R_bathroom", "R_bathroom_z1",
    }
    for room_id in upstairs:
        links = load(ROOT / "content" / "art" / room_id / "hotspots.json")["links"]
        assert all(link["target"] not in {"B05_maison", "S02_sector"} for link in links), room_id
    for room_id in outside:
        links = load(ROOT / "content" / "art" / room_id / "hotspots.json")["links"]
        assert any(link["target"] == "B05_maison" for link in links), room_id
    quiz = load(DATA / "quiz" / "sector" / "S04_cafes.json")
    seen = []
    for path in (DATA / "rooms").glob("*.json"):
        room = load(path)
        if room.get("sector_id") != "S04_cafes":
            continue
        for word in room["words"]:
            seen.append(word["id"])
    assert len(quiz["items"]) == len(set(seen))
    assert len(quiz["items"]) > 100

    finish(quiz)


def finish(quiz):
    prayers = load(DATA / "prayers.json")
    assert len(prayers["prayers"]) == 12
    titles = [prayer["title_fr"] for prayer in prayers["prayers"]]
    assert "Symbole des Apôtres (Je crois en Dieu)" in titles
    assert "Symbole de Nicée-Constantinople (Credo de la messe)" in titles
    assert (DATA / "credits.md").exists()
    assert "CC BY-SA 4.0" in (DATA / "credits.md").read_text(encoding="utf-8")
    assert (ROOT / "LICENSE-DATA.md").exists()
    assert not (ROOT / "src" / "fonts" / "Cinzel.ttf").exists()
    assert not (ROOT / "src" / "fonts" / "IMFeENrm28P.ttf").exists()

    scene = normalize_scene(load(EXAMPLE))
    assert scene["width"] == 1280 and scene["divider_x"] == 640
    assert "sign" in scene["text_areas"] and "plaque" in scene["text_areas"]
    croix = next(hot for hot in scene["hotspots"] if hot["slug"] == "croix")
    assert croix["polygon"] and croix["mnemonic_box"]
    pig = next(hot for hot in scene["hotspots"] if hot.get("mnemonic_for") == "banc")
    assert pig["box"]

    street = normalize_scene(load(ROOT / "content" / "art" / "ST_cooking_seg001" / "hotspots.json"))
    assert street["layout"] == "tiered"
    assert street["exits"]["back"]["target"] == "S04_sector"
    assert street["exits"]["forward"]["target"] == "ST_cooking_seg002"
    assert street["links"] == []
    assert street["text_areas"]["dir_side_er"]["role"] == "direction"
    assert street["hotspots"][0]["tier"] in {"street", "balcony", "upper", "roof"}
    sector = normalize_scene(load(ROOT / "content" / "art" / "S04_sector" / "hotspots.json"))
    assert [link["target"] for link in sector["links"]] == ["B08_cafe", "B09_restaurant", "ST_cooking_seg001"]
    assert {link["kind"] for link in sector["links"]} == {"building", "street"}
    assert sector["exits"] == {}
    restaurant = normalize_scene(load(ROOT / "content" / "art" / "B09_restaurant" / "hotspots.json"))
    assert {link["kind"] for link in restaurant["links"]} >= {"door", "window"}
    assert street["exits"]["forward"]["kind"] == "street"

    pointed = normalize_scene({
        "width": 100,
        "height": 40,
        "text_areas": {"north": {"box": [0, 0, 40, 20], "text": "Nord", "role": "direction"}},
        "items": [],
    })
    assert pointed["text_areas"]["north"]["role"] == "direction"
    assert pointed["text_areas"]["north"]["text"] == "Nord"

    i18n = load(ROOT / "data" / "i18n.json")
    guide = load(ROOT / "data" / "guide.json")

    def flat(obj, prefix=""):
        found = set()
        if isinstance(obj, dict):
            for key, value in obj.items():
                found |= flat(value, f"{prefix}.{key}" if prefix else key)
        else:
            found.add(prefix)
        return found

    assert flat(i18n["en"]) == flat(i18n["fr"])
    assert i18n["en"]["nav"]["backTo"] == "Back to {place}"
    assert i18n["en"]["nav"]["enterPlace"] == "Enter: {place}"
    assert i18n["fr"]["nav"]["enterPlace"] == "Entrer : {place}"
    assert i18n["fr"]["nav"]["backMap"] == "Retour au plan du village"
    assert i18n["en"]["tools"]["fullscreen"] == "Fullscreen"
    assert i18n["en"]["tools"]["leave"] == "Exit fullscreen"
    assert i18n["fr"]["tools"]["fullscreen"] == "Plein écran"
    assert i18n["fr"]["tools"]["leave"] == "Quitter le plein écran"
    assert_fullscreen_overlays()
    assert_wide_passages()
    walk_site_graph()
    dining = load(DATA / "rooms" / "R_resto_room_z1.json")
    assert dining["parent"]["id"] == "R_resto_room"
    assert dining["parent"]["name_fr"] == "La salle"
    assert [item["icon"] for item in guide["en"]["sections"]] == [item["icon"] for item in guide["fr"]["sections"]]
    assert len(guide["en"]["sections"]) == 9
    rooms_en = next(item["body"] for item in guide["en"]["sections"] if item["icon"] == "house")
    rooms_fr = next(item["body"] for item in guide["fr"]["sections"] if item["icon"] == "house")
    assert "magnifying glass" in rooms_en
    assert "loupe" in rooms_fr
    paths_en = next(item["body"] for item in guide["en"]["sections"] if item["icon"] == "path")
    paths_fr = next(item["body"] for item in guide["fr"]["sections"] if item["icon"] == "path")
    assert "olive arrow" in paths_en and "magnifying glass" in paths_en
    assert "flèche olive" in paths_fr and "loupe" in paths_fr
    client_src = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    css_src = (ROOT / "src" / "styles.css").read_text(encoding="utf-8")
    assert "way-badge" in client_src
    assert ".way-badge" in css_src
    assert "paintedSign(" in client_src
    assert "way-pill" in client_src
    assert "function toneSigns" in client_src
    way_fn = client_src.split("function placeWayBadges", 1)[1].split("function placeZoomBadges", 1)[0]
    assert "node.title" not in way_fn
    assert "way-pill" in way_fn
    assert "stairs" in way_fn
    assert "${nameTag(label, link.box)}" not in client_src
    assert "nameTag(label, hot.box)" in client_src
    assert ".painted-sign" in css_src
    assert ".way-pill" in css_src
    assert ".painted-sign.ink-gold" in css_src
    assert ".painted-sign.lit" in css_src
    assert ".way-badge.up > svg" in css_src
    assert (DATA / "i18n.json").exists() and (DATA / "guide.json").exists()

    delivered = normalize_scene(load(ROOT / "content" / "art" / "R_cafe_02" / "hotspots.json"))
    assert len(delivered["hotspots"]) == 9
    assert delivered["hotspots"][0]["word_id"] == "fr_carafe_noun"
    assert delivered["hotspots"][0]["label_xy"]

    shown = []
    for path in (DATA / "rooms").glob("*.json"):
        conv = load(path).get("conversation")
        if not conv:
            continue
        assert conv["lines"] and all(line.get("speaker") and line.get("fr") for line in conv["lines"])
        shown.append(conv["id"])
    source_conv = load(ROOT / "data" / "source" / "conversations.json")["conversations"]
    hidden = [item["id"] for item in source_conv if item.get("status") != "written"]
    assert shown and hidden
    assert not set(shown) & set(hidden)
    assert all(item.get("status") == "premise_only" for item in source_conv if item["id"] in hidden)
    assert len(source_conv) == 720
    assert len(hidden) == 9
    vocab = [json.loads(line) for line in (ROOT / "data" / "source" / "vocab.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    coq = next(word for word in vocab if word["id"] == "fr_coq_noun")
    assert coq["mnemonic_hook"]["scene"] == 'A proud ROOSTER perches on a Coke bottle ("KOK") and crows at dawn.'
    assert_paintings_fit()
    print("ok", len(quiz["items"]), "quiz items;", len(scene["hotspots"]), "church hotspots")


def assert_paintings_fit():
    """Every item box and exit box is on screen and clear of the cream strip."""
    script = ROOT / "scripts" / "check_viewport.mjs"
    result = subprocess.run(
        ["node", str(script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    if result.returncode != 0:
        raise AssertionError(output or "viewport check failed")
    print(output)


if __name__ == "__main__":
    main()

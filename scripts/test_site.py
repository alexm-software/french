#!/usr/bin/env python3
"""Checks the built site data and the church hotspot specimen."""

from __future__ import annotations

import json
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
        assert link["box"][1] >= art["height"] - 120, (zoom_id, link["box"])
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
        zoom = raw.get("zoom_from") or {}
        if isinstance(zoom, dict) and zoom.get("room_id"):
            targets.append(zoom["room_id"])
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
    assert len(nodes) == 1 + 16 + 84 + 845, len(nodes)
    stray = sorted(nodes - {MAP} - set(hierarchy))
    assert not stray, f"strip back missing: {stray[:12]}"

    client = (ROOT / "src" / "main.js").read_text(encoding="utf-8")
    assert "data-back" in client and "nav.backMap" in client and "nav.backTo" in client
    assert_s04_explicit(hierarchy, sectors, buildings, rooms)
    assert_back_strip_stays_visible(client)


def main():
    index = load(DATA / "index.json")
    assert index["open_sectors"] == ["S04_cafes"], index["open_sectors"]
    assert not index.get("open_rooms")
    assert index["featured"]["kind"] == "sector"
    assert index["featured"]["id"] == "S04_cafes"
    assert len(index["sectors"]) == 16
    assert index["start"] == "S01_beginner"
    assert any(item["id"] == "faith_first" for item in index["alternatives"])
    assert index["route_legs"], "walking legs missing"
    locked = [sector["id"] for sector in index["sectors"] if not sector["open"]]
    assert "S01_beginner" in locked and "S11_church" in locked
    assert all(sector["x"] and sector["y"] for sector in index["sectors"])

    sector = load(DATA / "sectors" / "S04_cafes.json")
    assert sector["open"] is True
    ids = [building["id"] for building in sector["buildings"]]
    assert ids == ["B09_restaurant", "B08_cafe", "ST_cooking"], ids
    assert sector["scene"]["image"].endswith("art/S04_sector/base.jpg")
    assert sector["scene"]["sign_text"] == "Rue des Saveurs"
    assert sector["description_fr"].startswith("La terrasse")
    cooking = next(link for link in sector["scene"]["links"] if link["target"] == "ST_cooking_seg001")
    assert cooking["name"] == "Ruelle des Gourmets — étape 1"
    assert sector["scene"]["placeholder"] is False
    link_targets = [link["target"] for link in sector["scene"]["links"]]
    assert link_targets == ["B08_cafe", "B09_restaurant", "ST_cooking_seg001"], link_targets
    assert len(sector["alleys"]) == 4
    assert sector["alleys"][0]["verbs"][0] == "manger"
    assert "nourrir" in sector["alleys"][0]["verbs"]
    assert "bannir" not in {verb for alley in sector["alleys"] for verb in alley["verbs"]}

    street = next(building for building in sector["buildings"] if building["id"] == "ST_cooking")
    segments = [room["id"] for room in street["floors"][0]["rooms"]]
    assert segments == [f"ST_cooking_seg{i:03d}" for i in range(1, 5)], segments
    assert [room["chip"] for room in street["floors"][0]["rooms"]] == ["1", "2", "3", "4"]
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
    assert len(upstairs["words"]) == 12
    troc = next(word for word in upstairs["words"] if word["id"] == "fr_troc_noun")
    assert troc["mnemonic_explain"] and troc["gender"] == "m" and troc["head"] == "le troc"
    troc_hits = [hot for hot in upstairs["scene"]["hotspots"] if hot.get("word_id") == "fr_troc_noun" and not hot.get("helper")]
    assert len(troc_hits) == 1
    assert troc["example_fr"] and troc["example_en"]
    assert "flelex_freq" not in troc and "cefr_flelex" not in troc

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
    assert "manger" in lemmas and "nourrir" in lemmas and "servir" in lemmas
    assert seg["scene"]["layout"] == "tiered"
    assert seg["scene"]["exits"]["back"]["target"] == "S04_sector"
    assert seg["scene"]["exits"]["forward"]["target"] == "ST_cooking_seg002"
    assert seg["scene"]["links"] == []
    assert seg["name_fr"] == "Étape 1 · Manger et nourrir"
    areas = seg["scene"]["text_areas"]
    assert areas["dir_forward"]["role"] == "direction" and areas["dir_forward"]["text"] == "étape 2 →"
    assert areas["dir_side_er"]["text"] == "-er"
    assert areas["dir_side_irre"]["text"] == "-ir / -re"
    assert areas["fr_servir_verb_sign"]["role"] == "verb_sign"
    assert areas["fr_servir_verb_sign"]["text"] == "servir (à / de)"
    assert "fr_servir_verb_plaque" not in areas
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
    servir = next(word for word in seg["words"] if word["lemma"] == "servir")
    assert servir["prepositions"] == ["à", "de"]
    assert servir["conjugations"]["present"][0] == "je sers"
    assert servir["conjugations"]["participe_passe"] == "servi"
    assert servir["conjugations"]["participe_present"] == "servant"
    assert load(DATA / "rooms" / "R_cafe_01.json")["name_fr"] == "La terrasse"
    assert servir["conjugations"]["imperatif"] == ["sers", "servons", "servez"]
    assert servir["example_fr"] and servir["example_en"]

    last = load(DATA / "rooms" / "ST_cooking_seg004.json")
    assert last["sign"] == "Ruelle des Gourmets"
    assert last["name_fr"] == "Étape 4 · Cuire et frire"
    assert last["scene"]["layout"] == "tiered"
    assert last["scene"]["exits"]["forward"]["target"] == "S04_sector"
    assert last["scene"]["exits"]["back"]["target"] == "ST_cooking_seg003"
    assert [room["chip"] for room in last["floors"][0]["rooms"]] == ["1", "2", "3", "4"]
    assert not any(hot.get("mirror") or hot.get("helper") for hot in last["scene"]["hotspots"])
    assert not (DATA / "rooms" / "ST_cooking_seg011.json").exists()
    assert not (DATA / "rooms" / "ST_cooking_seg005.json").exists()
    assert not (ROOT / "content" / "art" / "ST_cooking_seg011").exists()

    wine = load(DATA / "rooms" / "R_wine_01.json")
    cave = next(word for word in wine["words"] if word["lemma"] == "cave")
    assert cave["cognate_type"] == "false_cognate"
    assert cave["false_cognate_note"]
    assert len(wine["words"]) == 15
    assert all(word["lemma"] not in {"whisky", "rhum", "cognac", "cigare"} for word in wine["words"])
    assert all(word["painted"] for word in wine["words"])
    zoom_wine = load(DATA / "rooms" / "R_wine_01_z1.json")
    assert zoom_wine["parent"]["id"] == "R_wine_01"
    assert len(zoom_wine["words"]) == 10
    for lemma in ("whisky", "rhum", "cognac", "cigare"):
        drawn = next(word for word in zoom_wine["words"] if word["lemma"] == lemma)
        assert drawn["painted"] is True, lemma
    assert any(hot.get("word_id") == "fr_whisky_noun" and not hot.get("helper") for hot in zoom_wine["scene"]["hotspots"])
    assert "plaque" not in load(ROOT / "content" / "art" / "B08_cafe" / "hotspots.json")["text_areas"]
    assert "plaque" not in load(ROOT / "content" / "art" / "B09_restaurant" / "hotspots.json")["text_areas"]

    room_files = sorted(path.name for path in (DATA / "rooms").glob("*.json"))
    assert len(room_files) == 12, room_files
    assert not (DATA / "rooms" / "R_greet.json").exists()
    quiz = load(DATA / "quiz" / "sector" / "S04_cafes.json")
    seen = []
    for path in (DATA / "rooms").glob("*.json"):
        for word in load(path)["words"]:
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
    assert sector["exits"] == {}

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
    assert i18n["fr"]["nav"]["backMap"] == "Retour au plan du village"
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
    assert (DATA / "i18n.json").exists() and (DATA / "guide.json").exists()

    delivered = normalize_scene(load(ROOT / "content" / "art" / "R_cafe_02" / "hotspots.json"))
    assert len(delivered["hotspots"]) == 12
    assert delivered["hotspots"][0]["word_id"] == "fr_tuilerie_noun"

    shown = []
    for path in (DATA / "rooms").glob("*.json"):
        conv = load(path).get("conversation")
        if not conv:
            continue
        assert conv["lines"] and all(line.get("speaker") and line.get("fr") for line in conv["lines"])
        shown.append(conv["id"])
    source_conv = load(ROOT / "data" / "source" / "conversations.json")["conversations"]
    hidden = [item["id"] for item in source_conv if item.get("status") != "written"]
    assert shown and not hidden
    assert len(source_conv) == 721
    print("ok", len(quiz["items"]), "quiz items;", len(scene["hotspots"]), "church hotspots")


if __name__ == "__main__":
    main()

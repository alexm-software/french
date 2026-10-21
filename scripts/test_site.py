#!/usr/bin/env python3
"""Checks the built site data and the church hotspot specimen."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotspots import normalize_scene

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
EXAMPLE = ROOT / "content" / "examples" / "eglise" / "hotspots.json"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assert_real_cafe(room):
    assert room["sign"] == "Café de la Place"
    assert room["scene"]["placeholder"] is False
    assert room["scene"]["plaque_text"] == "L'étage"
    assert room["scene"]["text_areas"]["sign"]["text_box"]
    assert room["scene"]["text_areas"]["plaque"]["text_box"]
    ids = {word["id"] for word in room["words"]}
    assert "fr_troc_noun" in ids and len(ids) == 12
    hot_ids = {hot.get("word_id") for hot in room["scene"]["hotspots"] if hot.get("word_id")}
    assert ids <= hot_ids
    assert any(hot.get("helper") and hot.get("word_id") == "fr_troc_noun" for hot in room["scene"]["hotspots"])
    troc = next(word for word in room["words"] if word["id"] == "fr_troc_noun")
    assert troc["mnemonic_explain"]
    assert troc["gender"] == "m" and troc["head"] == "le troc"
    carafe = next(word for word in room["words"] if word["lemma"] == "carafe")
    assert carafe["cognate_type"] == "true_cognate"
    assert carafe["ipa"] and carafe["respelling"]


def main():
    index = load(DATA / "index.json")
    assert index["open_sectors"] == ["S04_cafes"], index["open_sectors"]
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
    street = next(building for building in sector["buildings"] if building["id"] == "ST_cooking")
    segments = [room["id"] for room in street["floors"][0]["rooms"]]
    assert segments == [f"ST_cooking_seg{i:03d}" for i in range(1, 15)], segments
    assert [room["chip"] for room in street["floors"][0]["rooms"]] == [str(i) for i in range(1, 15)]

    restaurant = next(building for building in sector["buildings"] if building["id"] == "B09_restaurant")
    ground = restaurant["floors"][0]["rooms"]
    assert [room["id"] for room in ground] == ["R_resto_kitchen_01", "R_resto_room", "R_wine_01"], [room["id"] for room in ground]

    if index.get("open_rooms"):
        assert index["open_rooms"] == ["R_cafe_02"]
        assert index["featured"]["id"] == "R_cafe_02"
        assert index["featured"]["sign"] == "Café de la Place"
        cafe_building = next(building for building in sector["buildings"] if building["id"] == "B08_cafe")
        cafe_flags = {room["id"]: room["open"] for floor in cafe_building["floors"] for room in floor["rooms"]}
        assert cafe_flags == {"R_cafe_01": False, "R_cafe_02": True}, cafe_flags
        assert all(not room["open"] for floor in restaurant["floors"] for room in floor["rooms"])
        assert [path.name for path in sorted((DATA / "rooms").glob("*.json"))] == ["R_cafe_02.json"]
        assert_real_cafe(load(DATA / "rooms" / "R_cafe_02.json"))
        quiz = load(DATA / "quiz" / "sector" / "S04_cafes.json")
        assert len(quiz["items"]) == 12
        finish(quiz)
        return

    cafe = load(DATA / "rooms" / "R_cafe_01.json")
    assert cafe["sign"] == "La terrasse"
    assert [floor["label"] for floor in cafe["floors"]] == ["Ground floor", "Upstairs"]
    assert cafe["scene"]["placeholder"] is True
    assert cafe["scene"]["text_areas"]["sign"]["text_box"]
    word_ids = {word["id"] for word in cafe["words"]}
    hot_ids = {hot.get("word_id") for hot in cafe["scene"]["hotspots"] if hot.get("word_id")}
    assert word_ids <= hot_ids

    upstairs = load(DATA / "rooms" / "R_cafe_02.json")
    assert upstairs["floor_label"] == "Upstairs"
    assert_real_cafe(upstairs)

    dining = load(DATA / "rooms" / "R_resto_room.json")
    zoom = next(hot for hot in dining["scene"]["hotspots"] if hot.get("zoom_id") == "R_resto_room_z1")
    assert zoom["polygon"] and len(zoom["polygon"]) >= 3
    ground_ids = [room["id"] for room in dining["floors"][0]["rooms"]]
    assert ground_ids == ["R_resto_kitchen_01", "R_resto_room", "R_wine_01"], ground_ids
    bar = load(DATA / "rooms" / "R_resto_room_z1.json")
    assert bar["parent"]["id"] == "R_resto_room"
    assert bar["words"]

    kitchen = load(DATA / "rooms" / "R_resto_kitchen_02.json")
    assert kitchen["floor"] == 2

    seg = load(DATA / "rooms" / "ST_cooking_seg001.json")
    lemmas = {word["lemma"] for word in seg["words"]}
    assert "déshonorer" not in lemmas  # it lives on a later segment, and must not be invented here
    boire = next(word for word in seg["words"] if word["lemma"] == "boire")
    assert boire["conjugations"]["present"][0] == "je bois"
    assert "ils/elles boivent" in boire["conjugations"]["present"]
    servir = next(word for word in seg["words"] if word["lemma"] == "servir")
    assert servir["prepositions"] == ["à", "de"]
    assert servir["conjugations"]["present"][0] == "je sers"
    assert servir["conjugations"]["imperatif"] == ["sers", "servons", "servez"]
    assert seg["conversation"]["lines"]
    assert any("boire" in line["fr"] or "bois" in line["fr"] or "boire" in line["fr"] for line in seg["conversation"]["lines"]) or any(
        word["lemma"] in line["fr"] for line in seg["conversation"]["lines"] for word in seg["words"]
    )

    later = load(DATA / "rooms" / "ST_cooking_seg013.json")
    assert any(word["lemma"] == "bannir" for word in later["words"]), "corrected later; do not drop current data"
    street_chips = [room["chip"] for room in later["floors"][0]["rooms"]]
    assert street_chips == [str(i) for i in range(1, 15)], street_chips
    assert later["sign"] == "Ruelle des Gourmets"
    museum_room = load(DATA / "rooms" / "ST_cooking_seg005.json")
    museum = next(word for word in museum_room["words"] if word["lemma"] == "abattre")
    assert museum["display"] == "museum_text"
    assert "plaque" in museum["mnemonic_explain"].lower()
    assert "drawing" in museum["mnemonic_explain"].lower()

    wine = load(DATA / "rooms" / "R_wine_01.json")
    cave = next(word for word in wine["words"] if word["lemma"] == "cave")
    assert cave["cognate_type"] == "false_cognate"
    assert cave["false_cognate_note"]
    zoom_wine = load(DATA / "rooms" / "R_wine_01_z1.json")
    assert zoom_wine["parent"]["id"] == "R_wine_01"

    quiz = load(DATA / "quiz" / "sector" / "S04_cafes.json")
    assert len(quiz["items"]) == 182
    assert not (DATA / "rooms" / "R_greet.json").exists()

    finish(quiz)


def finish(quiz):
    prayers = load(DATA / "prayers.json")
    assert len(prayers["prayers"]) == 11
    assert (DATA / "credits.md").exists()

    scene = normalize_scene(load(EXAMPLE))
    assert scene["width"] == 1280 and scene["divider_x"] == 640
    assert "sign" in scene["text_areas"] and "plaque" in scene["text_areas"]
    croix = next(hot for hot in scene["hotspots"] if hot["slug"] == "croix")
    assert croix["polygon"] and croix["mnemonic_box"]
    pig = next(hot for hot in scene["hotspots"] if hot.get("mnemonic_for") == "banc")
    assert pig["box"]
    delivered = normalize_scene(load(ROOT / "content" / "art" / "R_cafe_02" / "hotspots.json"))
    assert len(delivered["hotspots"]) == 12
    assert delivered["hotspots"][0]["word_id"] == "fr_tuilerie_noun"
    print("ok", len(quiz["items"]), "quiz items;", len(scene["hotspots"]), "church hotspots")


if __name__ == "__main__":
    main()

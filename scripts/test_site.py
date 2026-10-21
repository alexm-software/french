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
    assert cooking["label_fr"] == "Ruelle des Gourmets"
    assert sector["scene"]["placeholder"] is False
    link_targets = [link["target"] for link in sector["scene"]["links"]]
    assert link_targets == ["B08_cafe", "B09_restaurant", "ST_cooking_seg001"], link_targets
    assert len(sector["alleys"]) == 11
    assert sector["alleys"][0]["verbs"][0] == "nourrir"
    assert "bannir" not in {verb for alley in sector["alleys"] for verb in alley["verbs"]}

    street = next(building for building in sector["buildings"] if building["id"] == "ST_cooking")
    segments = [room["id"] for room in street["floors"][0]["rooms"]]
    assert segments == [f"ST_cooking_seg{i:03d}" for i in range(1, 12)], segments
    assert [room["chip"] for room in street["floors"][0]["rooms"]] == [str(i) for i in range(1, 12)]
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
    assert "example_fr" not in troc or not troc.get("example_fr")

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
    assert lemmas == {"nourrir", "écraser", "dévorer", "déjeuner", "servir", "manger"}
    assert seg["scene"]["exits"]["prev"]["target"] == "S04_sector"
    assert seg["scene"]["exits"]["next"]["target"] == "ST_cooking_seg002"
    assert not any(link.get("exit") for link in seg["scene"].get("links") or [])
    raw_items = load(ROOT / "content" / "art" / "ST_cooking_seg001" / "hotspots.json")["items"]
    for item in raw_items:
        hits = [hot for hot in seg["scene"]["hotspots"] if hot.get("word_id") == item["id"] and not hot.get("helper")]
        assert len(hits) == 1, item["id"]
        box = hits[0]["box"]
        for part in (item["box"], item.get("mnemonic_box")):
            if not part:
                continue
            assert box[0] <= part[0] and box[1] <= part[1] and box[2] >= part[2] and box[3] >= part[3]
    assert seg.get("conversation") is None
    assert seg["prev"] is None and seg["next"] is None
    assert not any(str(item["id"]).startswith("ST_") for item in seg["related"])
    servir = next(word for word in seg["words"] if word["lemma"] == "servir")
    assert servir["prepositions"] == ["à", "de"]
    assert servir["conjugations"]["present"][0] == "je sers"
    assert servir["conjugations"]["participe_passe"] == "servi"
    assert servir["conjugations"]["participe_present"] == "servant"
    assert load(DATA / "rooms" / "R_cafe_01.json")["name_fr"] == "La terrasse"
    assert servir["conjugations"]["imperatif"] == ["sers", "servons", "servez"]
    assert seg["scene"]["text_areas"]["fr_servir_verb_plaque"]["text"] == "à / de"

    later = load(DATA / "rooms" / "ST_cooking_seg011.json")
    assert later["sign"] == "Ruelle des Gourmets"
    assert [room["chip"] for room in later["floors"][0]["rooms"]] == [str(i) for i in range(1, 12)]
    assert not (DATA / "rooms" / "ST_cooking_seg013.json").exists()
    mirrored = load(DATA / "rooms" / "ST_cooking_seg004.json")
    assert any(hot.get("mirror") for hot in mirrored["scene"]["hotspots"])

    wine = load(DATA / "rooms" / "R_wine_01.json")
    cave = next(word for word in wine["words"] if word["lemma"] == "cave")
    assert cave["cognate_type"] == "false_cognate"
    assert cave["false_cognate_note"]
    whisky = next(word for word in wine["words"] if word["lemma"] == "whisky")
    assert whisky["painted"] is False
    zoom_wine = load(DATA / "rooms" / "R_wine_01_z1.json")
    assert zoom_wine["parent"]["id"] == "R_wine_01"
    drawn = next(word for word in zoom_wine["words"] if word["lemma"] == "whisky")
    assert drawn["painted"] is True
    assert any(hot.get("word_id") == "fr_whisky_noun" and not hot.get("helper") for hot in zoom_wine["scene"]["hotspots"])

    room_files = sorted(path.name for path in (DATA / "rooms").glob("*.json"))
    assert len(room_files) == 19, room_files
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
    assert len(prayers["prayers"]) == 11
    assert (DATA / "credits.md").exists()

    scene = normalize_scene(load(EXAMPLE))
    assert scene["width"] == 1280 and scene["divider_x"] == 640
    assert "sign" in scene["text_areas"] and "plaque" in scene["text_areas"]
    croix = next(hot for hot in scene["hotspots"] if hot["slug"] == "croix")
    assert croix["polygon"] and croix["mnemonic_box"]
    pig = next(hot for hot in scene["hotspots"] if hot.get("mnemonic_for") == "banc")
    assert pig["box"]

    street = normalize_scene(load(ROOT / "content" / "art" / "ST_cooking_seg001" / "hotspots.json"))
    assert street["exits"]["prev"]["target"] == "S04_sector"
    assert street["exits"]["next"]["target"] == "ST_cooking_seg002"
    assert street["links"] == []
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
    assert [item["icon"] for item in guide["en"]["sections"]] == [item["icon"] for item in guide["fr"]["sections"]]
    assert len(guide["en"]["sections"]) == 9
    assert (DATA / "i18n.json").exists() and (DATA / "guide.json").exists()

    delivered = normalize_scene(load(ROOT / "content" / "art" / "R_cafe_02" / "hotspots.json"))
    assert len(delivered["hotspots"]) == 12
    assert delivered["hotspots"][0]["word_id"] == "fr_tuilerie_noun"
    print("ok", len(quiz["items"]), "quiz items;", len(scene["hotspots"]), "church hotspots")


if __name__ == "__main__":
    main()

"""Fruit-stall candidate: fifteen source words, and a route that does not cut the bakery."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs" / "room-trials" / "fruits-01" / "manifest.json"
LINKS = ROOT / "docs" / "room-trials" / "fruits-01" / "candidate" / "links.json"
NINE_EDGE = {"fr_pomme_noun", "fr_paille_noun", "fr_abricot_noun"}


def inter(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


class FruitCandidate(unittest.TestCase):
    def test_fifteen_source_words_and_honest_edges(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        rooms = json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]
        source = next(r for r in rooms if r["id"] == "R_fruits_01")
        got = [it["id"] for it in manifest["items"]]
        self.assertEqual(set(got), set(source["words"]))
        self.assertEqual(len(got), 15)
        boxes = [(it["id"], it["box_hint"], it["g"]) for it in manifest["items"]]
        for i, (wid, box, g) in enumerate(boxes):
            cx = (box[0] + box[2] / 2) / 1280
            over = box[0] < 77 or box[1] < 43 or box[0] + box[2] > 1203 or box[1] + box[3] > 677
            if wid in NINE_EDGE:
                self.assertTrue(over, wid)
            else:
                self.assertFalse(over, wid)
            if g == "f":
                self.assertLess(cx, 0.45, wid)
            else:
                self.assertGreater(cx, 0.55, wid)
            for wid2, box2, _ in boxes[i + 1:]:
                self.assertFalse(inter(box, box2), (wid, wid2))
        citron = next(it for it in manifest["items"] if it["id"] == "fr_citron_noun")
        self.assertIn("not painted", citron["hook"])

    def test_route_uses_the_painted_hall_and_not_the_bakery_door(self):
        links = json.loads(LINKS.read_text(encoding="utf-8"))
        self.assertFalse(links["return"]["needs_edit_of_boulangerie_jpg"])
        hall, bakery = links["entry"]["proposed_rect"], links["bakery_rect_if_split"]
        self.assertFalse(inter(hall, bakery))
        market = json.loads((ROOT / "content" / "v2" / "map.json").read_text(encoding="utf-8"))
        for row in market["sectors"]["market"]["buildings"]:
            ident = row.get("id") or row["building_id"]
            if ident in ("boulangerie", "B06_marche"):
                continue
            self.assertFalse(inter(hall, row["rect"]), ident)
            self.assertFalse(inter(bakery, row["rect"]), ident)
        layout = json.loads((ROOT / "content" / "v2" / "boulangerie" / "layout.json").read_text(encoding="utf-8"))
        self.assertNotIn("fruits", layout["rooms"])
        live_map = json.dumps(market)
        self.assertNotIn("fruits", live_map)

    def test_dialogue_is_draft_only(self):
        dialogue = json.loads((ROOT / "docs" / "room-trials" / "fruits-01" / "candidate" / "dialogue.json").read_text(encoding="utf-8"))
        self.assertFalse(dialogue["pinned_in_production"])
        text = " ".join(line["fr"] for line in dialogue["lines"])
        used = [w for w in ("pomme", "pêche", "orange", "banane", "poire", "fraise", "cerise", "olive", "amande", "paille", "fruit", "citron", "raisin", "melon", "abricot") if w in text]
        self.assertGreaterEqual(len(used), 3)
        source = (ROOT / "data" / "source" / "conversations.json").read_text(encoding="utf-8")
        self.assertNotIn("Sous la halle", source)


if __name__ == "__main__":
    unittest.main()

"""The fifteen fruit words are two rooms, and the batch stays at 30."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRESH = ROOT / "docs" / "room-trials" / "fruits-frais" / "manifest.json"
PICNIC = ROOT / "docs" / "room-trials" / "fruits-pique-nique" / "manifest.json"


def slots(text):
    n = 0
    for line in text.splitlines():
        m = re.match(r"\| (\d+)(?:–(\d+))? \|", line)
        if not m:
            continue
        a, b = int(m.group(1)), m.group(2)
        n += int(b) - a + 1 if b else 1
    return n


class FruitSplit(unittest.TestCase):
    def test_all_fifteen_once(self):
        rooms = json.loads((ROOT / "data" / "source" / "rooms.json").read_text(encoding="utf-8"))["rooms"]
        source = set(next(r["words"] for r in rooms if r["id"] == "R_fruits_01"))
        fresh = json.loads(FRESH.read_text(encoding="utf-8"))
        picnic = json.loads(PICNIC.read_text(encoding="utf-8"))
        a = [it["id"] for it in fresh["items"]]
        b = [it["id"] for it in picnic["items"]]
        self.assertEqual(len(a), 8)
        self.assertEqual(len(b), 7)
        self.assertEqual(set(a) | set(b), source)
        self.assertEqual(set(a) & set(b), set())
        citron = next(it for it in picnic["items"] if it["id"] == "fr_citron_noun")
        self.assertIn("throne", citron["hook"])
        self.assertNotIn("not painted", citron["hook"])
        pomme = next(it for it in fresh["items"] if it["id"] == "fr_pomme_noun")
        self.assertIn("POM-pom", pomme["hook"])

    def test_batch_stays_thirty(self):
        text = (ROOT / "docs" / "changes" / "ROOMS_30_2026-11-07.md").read_text(encoding="utf-8")
        self.assertEqual(slots(text), 30)
        self.assertIn("R_pronouns_03", text)
        self.assertIn("not in this 30", text)

    def test_no_bakery_door(self):
        links = json.loads((ROOT / "docs" / "room-trials" / "fruits-frais" / "candidate" / "links.json").read_text(encoding="utf-8"))
        self.assertFalse(links["to_picnic"]["needs_edit_of_boulangerie_jpg"])
        layout = json.loads((ROOT / "content" / "v2" / "boulangerie" / "layout.json").read_text(encoding="utf-8"))
        self.assertNotIn("fruits", layout["rooms"])


if __name__ == "__main__":
    unittest.main()

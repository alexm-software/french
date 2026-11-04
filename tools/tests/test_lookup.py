"""Source-index lookup stays aligned with vocab, fixes, and verb beret rules."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import lookup


class Lookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vocab, cls.rooms = lookup.load()
        cls.by_id = {row["id"]: row for row in cls.vocab}

    def test_stamp_diff_names_changed_source(self):
        now = {"vocab": "a", "fixes": "b", "conj": "c", "rooms": "d"}
        self.assertEqual(lookup.stamp_diff(now, dict(now)), [])
        self.assertEqual(lookup.stamp_diff({"vocab": "a", "fixes": "b", "conj": "c", "rooms": "old"}, now), ["rooms"])

    def test_accent_folded_gloss_and_room_inventory(self):
        hits, _ = lookup.search(self.vocab, self.rooms, text=["probleme"])
        self.assertEqual([row["id"] for row in hits], ["fr_probleme_noun"])
        room, notes = lookup.search(self.vocab, self.rooms, room="R_abs_problem_02")
        self.assertEqual(len(room), 12)
        self.assertEqual(notes["missing"], [])
        self.assertEqual(room[0]["id"], "fr_abri_noun")
        self.assertTrue(all(row["room"] == "R_abs_problem_02" for row in room))

    def test_fixes_and_confirmed_berets(self):
        self.assertEqual(self.by_id["fr_pilote_noun"]["say"], "pea-LOT")
        self.assertEqual(self.by_id["fr_container_noun"]["g"], "m")
        self.assertEqual(self.by_id["fr_sauver_verb"]["beret"], "er")
        self.assertEqual(self.by_id["fr_proteger_verb"]["beret"], "er")
        self.assertTrue(self.by_id["fr_proteger_verb"].get("pronominal"))
        self.assertNotIn("beret", self.by_id["fr_etre_verb"])
        self.assertEqual(self.by_id["fr_etre_verb"]["verb_group"], 3)
        self.assertTrue(self.by_id["fr_etre_verb"]["irregular"])
        self.assertEqual(lookup.beret_mark(self.by_id["fr_etre_verb"]), "g3/irr?")
        # vendre is flagged irregular in vocab and still a regular -re on its table.
        self.assertEqual(self.by_id["fr_vendre_verb"]["beret"], "re")
        self.assertTrue(self.by_id["fr_vendre_verb"]["irregular"])

    def test_beret_matches_build_v2_when_a_table_exists(self):
        sys.path.insert(0, str(ROOT / "scripts" / "v2"))
        import build_v2
        want = {"fr_finir_verb", "fr_partir_verb", "fr_vendre_verb", "fr_manger_verb"}
        found = {}
        with (ROOT / "data" / "source" / "vocab.jsonl").open(encoding="utf-8") as handle:
            for line in handle:
                word = json.loads(line)
                if word["id"] in want:
                    found[word["id"]] = word
                if len(found) == len(want):
                    break
        codes = {"red": "er", "green": "ir", "purple": "re", "gold": "irregular"}
        for wid, word in found.items():
            card = build_v2.verb_from_vocab(word)
            self.assertEqual(self.by_id[wid]["beret"], codes[card["beret"]], wid)

    def test_cli_check_room_hook_and_live(self):
        check = subprocess.run([sys.executable, str(TOOLS / "lookup.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn("fresh", check.stderr)
        bare = subprocess.run([sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild"], capture_output=True, text=True)
        self.assertEqual(bare.returncode, 2)
        missing = subprocess.run(
            [sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild", "--id", "fr_missing_noun"],
            capture_output=True, text=True)
        self.assertEqual(missing.returncode, 1)
        pilote = subprocess.run(
            [sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild", "--id", "fr_pilote_noun"],
            capture_output=True, text=True)
        self.assertEqual(pilote.returncode, 0, pilote.stderr)
        self.assertIn("pea-LOT", pilote.stdout)
        self.assertNotIn("pee-", pilote.stdout)
        hook = subprocess.run(
            [sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild", "--hook", "--id", "fr_solution_noun"],
            capture_output=True, text=True)
        self.assertIn("trampoline at the foot of the pole", hook.stdout)
        live = subprocess.run(
            [sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild", "--live", "--id", "fr_probleme_noun"],
            capture_output=True, text=True)
        self.assertIn("live:pompiers/pompiers", live.stdout)
        count = subprocess.run(
            [sys.executable, str(TOOLS / "lookup.py"), "--no-rebuild", "--count", "--building", "pompiers"],
            capture_output=True, text=True)
        self.assertEqual(count.stdout.strip(), "47")


if __name__ == "__main__":
    unittest.main()

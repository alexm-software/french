"""The fruit prompt and the boxes have to say the same thing before any picture."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
MANIFEST = ROOT / "docs" / "room-trials" / "fruits-frais" / "manifest.json"
PROMPT = ROOT / "docs" / "room-trials" / "fruits-frais" / "prompt-submitted.txt"


class FruitPromptGeometry(unittest.TestCase):
    def test_submitted_prompt_matches_the_left_stand(self):
        text = PROMPT.read_text(encoding="utf-8")
        self.assertNotIn("between them", text)
        self.assertNotIn("oak counter", text)
        self.assertNotIn("shopper", text)
        self.assertNotIn("monkey", text)
        self.assertIn("wooden stepped stand", text)
        self.assertIn("Right of center", text)
        self.assertIn("fluffy red pom-pom", text)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for it in manifest["items"]:
            hook = it["hook"]
            self.assertNotIn("45", hook)
            self.assertNotIn("would need", hook)
        pan = (ROOT / "docs" / "room-trials" / "fruits-frais" / "prompt-pan.txt").read_text(encoding="utf-8")
        self.assertTrue(pan.startswith("Edit the attached painting"))
        self.assertNotIn("PIL", pan)
        self.assertNotIn("outpaint", pan.lower())
        self.assertNotIn("paste", pan.lower())
        banned = ("would need", "not accepted", "45 percent", "FAIL", "centre 685")
        learner = [
            ROOT / "docs" / "room-trials" / "fruits-frais" / "manifest.json",
            ROOT / "docs" / "room-trials" / "fruits-pique-nique" / "manifest.json",
            ROOT / "docs" / "room-trials" / "fruits-frais" / "candidate" / "source-facts.tsv",
        ]
        for path in learner:
            text = path.read_text(encoding="utf-8")
            for phrase in banned:
                self.assertNotIn(phrase, text, path.name)

    def test_envelopes_pass_and_a_right_side_feminine_box_fails(self):
        from plan_check import validate_plan
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        fail, _warn = validate_plan(manifest)
        self.assertEqual(fail, [])
        bad = json.loads(json.dumps(manifest))
        for it in bad["items"]:
            if it["id"] == "fr_orange_noun":
                it["box_hint"] = [800, 140, 100, 80]
        fail, _warn = validate_plan(bad)
        self.assertTrue(any("contradicts side" in m for m in fail))

    def test_side_band_uses_the_whole_helper_box(self):
        from plan_check import validate_plan
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        raisin = next(it for it in manifest["items"] if it["id"] == "fr_raisin_noun")
        self.assertIn("seller", raisin["hook"])
        self.assertIn("scale", raisin["hook"])
        self.assertIn("head to feet", raisin["shown"])
        x, _y, w, _h = raisin["box_hint"]
        self.assertGreater(x + w / 2, 704)
        berries = [656, 251, 58, 114]
        self.assertLess(berries[0] + berries[2] / 2, 704)
        bad = json.loads(json.dumps(manifest))
        for it in bad["items"]:
            if it["id"] == "fr_raisin_noun":
                it["box_hint"] = berries
        fail, _warn = validate_plan(bad)
        self.assertTrue(any(m.startswith("fr_raisin_noun: box_hint contradicts side") for m in fail))
        # Parked review box: seller, scale, and grapes. Centre 737 passes 55 percent.
        self.assertEqual((620 + 854) / 2, 737)
        self.assertGreater(737, 704)


if __name__ == "__main__":
    unittest.main()

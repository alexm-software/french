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
        self.assertIn("stepped wooden fruit stand", text)
        self.assertIn("still left of center", text)
        self.assertIn("Right of center", text)
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for it in manifest["items"]:
            hook = it["hook"]
            self.assertNotIn("45", hook)
            self.assertNotIn("would need", hook)

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


if __name__ == "__main__":
    unittest.main()

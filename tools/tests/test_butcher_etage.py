"""Geometry of the accepted upstairs butcher, using the viewer's label placer."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
sys.path.insert(0, str(ROOT / "skills" / "memory-palace-builder" / "scripts"))
import build_v2 as B  # noqa: E402

DRAFT = ROOT / "docs" / "room-trials" / "boucherie-surfaces" / "room-draft.json"
HOOKS = ROOT / "docs" / "room-trials" / "boucherie-surfaces" / "hooks.json"
W, H = 1280, 720


def inter(a, b, g=0):
    a = [a[0] - g, a[1] - g, a[2] + 2 * g, a[3] + 2 * g]
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


class ButcherEtageGeometry(unittest.TestCase):
    def test_viewer_labels_clear_the_accepted_boxes(self):
        draft = json.loads(DRAFT.read_text(encoding="utf-8"))
        vocab = B.load_vocab()
        room = {
            "name": draft["name"],
            "nameplate": draft["nameplate"],
            "doors": draft["doors"],
            "zooms": [],
            "items": [],
        }
        for spec in draft["items"]:
            it = B.item_from_vocab(vocab[spec["id"]])
            it["_hw"] = B.headword(it)
            it["box"] = spec["box"]
            room["items"].append(it)
        B.place_labels(room)
        plate = B.nameplate_rect(room)
        door = draft["doors"][0]["hit"]
        boxes = [it["box"] for it in room["items"]]
        for i, a in enumerate(boxes):
            self.assertGreaterEqual(a[0], 77)
            self.assertGreaterEqual(a[1], 43)
            self.assertLessEqual(a[0] + a[2], 1203)
            self.assertLessEqual(a[1] + a[3], 677)
            for b in boxes[i + 1:]:
                self.assertFalse(inter(a, b), (room["items"][i]["id"], a, b))
        # clerk feet end at the split; the eater starts on that same line and does not overlap
        clerk = next(it for it in room["items"] if it["id"] == "fr_charcutier_noun")
        eater = next(it for it in room["items"] if it["id"] == "fr_mangeur_noun")
        self.assertEqual(clerk["box"][1] + clerk["box"][3], 391)
        self.assertEqual(eater["box"][1], 391)
        plaque = next(it for it in room["items"] if it["id"] == "fr_abattoir_noun")
        self.assertEqual(plaque["box"][0], 889)
        for it in room["items"]:
            cx = (it["box"][0] + it["box"][2] / 2) / W
            if it["g"] == "f":
                self.assertLess(cx, 0.45, it["id"])
            if it["g"] == "m":
                self.assertGreater(cx, 0.55, it["id"])
            lab = it["_lab"]
            self.assertGreaterEqual(lab[0], 8)
            self.assertGreaterEqual(lab[1], 8)
            self.assertLessEqual(lab[0] + lab[2], W - 8)
            self.assertLessEqual(lab[1] + lab[3], H - 8)
            self.assertFalse(inter(lab, door, 3))
            self.assertFalse(inter(lab, plate, 3))
            for other in room["items"]:
                if other is it:
                    continue
                self.assertFalse(inter(lab, other["box"], 3), (it["id"], other["id"]))
        labs = [it["_lab"] for it in room["items"]]
        for i, a in enumerate(labs):
            for b in labs[i + 1:]:
                self.assertFalse(inter(a, b, 3))

    def test_shark_hook_stays_plain(self):
        hooks = json.loads(HOOKS.read_text(encoding="utf-8"))
        text = hooks["fr_requin_noun"]["hook"].lower()
        self.assertIn("plain depiction", text)
        self.assertNotIn("wreck", text)
        self.assertNotIn("can", hooks["fr_requin_noun"]["hook"])
        self.assertTrue(hooks["fr_abattoir_noun"]["plaque"])
        self.assertIn("slices a ham", hooks["fr_charcutier_noun"]["hook"])
        self.assertNotIn("pale", hooks["fr_charcutier_noun"]["hook"])


if __name__ == "__main__":
    unittest.main()

"""The science-hall pilot plan is valid. The first painted candidate is not."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from plan_check import exit_identity_refs, validate_manifest, validate_plan
from unbuilt import live_ids

REVIEW = ROOT / "content" / "v2" / "sciences" / "review"
W, H = 1280, 720


def center_x(box):
    return (box[0] + box[2] / 2) / W


def gate_fails(kind, box):
    x, y, w, h = box
    out = []
    if x < 77:
        out.append("left-6%")
    if x + w > W - 77:
        out.append("right-6%")
    if y < 43:
        out.append("top-6%")
    if y + h > H - 43:
        out.append("bottom-6%")
    cx = center_x(box)
    if kind == "f" and cx >= 0.45:
        out.append("feminine")
    if kind == "m" and cx <= 0.55:
        out.append("masculine")
    if kind == "adj" and not 0.30 <= cx <= 0.70:
        out.append("center")
    return out


def overlaps(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


class ScienceHallPilot(unittest.TestCase):
    def test_plan_compiles_and_prompt_is_the_submitted_text(self):
        manifest = json.loads((ROOT / "content/v2/sciences/hall.manifest.json").read_text())
        fail, _warn = validate_manifest(manifest, require_prompt=True)
        self.assertEqual(fail, [])
        submitted = (REVIEW / "submitted-prompt.txt").read_text()
        self.assertEqual(submitted, manifest["prompt_text"])
        digest = hashlib.sha256(submitted.encode()).hexdigest()
        self.assertEqual(digest, "2b6740d39c678d9f3abe45d6f36e124bbdbb2767275e8778ff5bf58096decb86")

    def test_eight_words_are_real_and_not_already_live(self):
        manifest = json.loads((ROOT / "content/v2/sciences/hall.manifest.json").read_text())
        vocab = {}
        for line in (ROOT / "data/source/vocab.jsonl").read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                vocab[row["id"]] = row
        live = live_ids(ROOT)
        ids = [item["id"] for item in manifest["items"]]
        sources = {
            "fr_pierre_noun": "R_geology",
            "fr_terre_noun": "R_geology",
            "fr_mine_noun": "R_geology",
            "fr_mineral_adj": "R_geology",
            "fr_sol_noun": "R_geology",
            "fr_cristal_noun": "R_geology",
            "fr_creuset_noun": "R_geology",
            "fr_pendule_noun_m": "R_physics_02",
        }
        self.assertEqual(set(ids), set(sources))
        for wid, room_id in sources.items():
            self.assertEqual(vocab[wid]["room_id"], room_id)
            self.assertEqual(live.get(wid, []), [])

    def test_candidate_is_blocked_on_measured_boxes(self):
        measured = json.loads((REVIEW / "measurements.json").read_text())
        self.assertEqual(measured["status"], "blocked")
        self.assertEqual(measured["image_calls"], 1)
        boxes = []
        for wid, item in measured["items"].items():
            fails = gate_fails(item["kind"], item["box"])
            stored = [item_fail.split()[0] for item_fail in item["fails"]]
            self.assertEqual(stored, fails)
            self.assertAlmostEqual(item["center_x"], center_x(item["box"]), places=3)
            boxes.append((wid, item["box"]))
        mine = measured["items"]["fr_mine_noun"]
        self.assertGreaterEqual(mine["center_x"], 0.45)
        self.assertLess(mine["center_x"], 0.50)
        self.assertGreaterEqual(len(measured["overlaps"]), 1)
        found = []
        for i, (wid, box) in enumerate(boxes):
            for other, obox in boxes[i + 1:]:
                if overlaps(box, obox):
                    found.append([wid, other])
        self.assertEqual(found, measured["overlaps"])
        self.assertFalse((ROOT / "village/data/sciences.js").exists())
        self.assertFalse((ROOT / "village/sciences/hall.jpg").exists())

    def test_parked_exit_omits_the_sector_image(self):
        parked = json.loads((ROOT / "content/v2/sciences/hall.manifest.json").read_text())
        layout = json.loads((ROOT / "content/v2/sciences/layout.json").read_text())
        fail, _warn = validate_plan(parked, layout)
        self.assertEqual(fail, ["map exit requires the sector image in prompt.refs: village/map/university.jpg"])

    def test_proposal_attaches_the_sector_image_and_keeps_slack(self):
        proposal = json.loads((ROOT / "content/v2/sciences/review/proposal.manifest.json").read_text())
        layout = json.loads((ROOT / "content/v2/sciences/layout.json").read_text())
        self.assertEqual(validate_manifest(proposal)[0], [])
        self.assertEqual(exit_identity_refs(proposal, layout), [])
        self.assertIn("village/map/university.jpg", proposal["prompt"]["refs"])
        self.assertNotIn("lycee.jpg", " ".join(proposal["prompt"]["refs"]))
        boxes = []
        for item in proposal["items"]:
            x, y, w, h = item["box_hint"]
            self.assertGreaterEqual(x, 100)
            self.assertLessEqual(x + w, 1180)
            self.assertGreaterEqual(y, 70)
            self.assertLessEqual(y + h, 660)
            cx = center_x(item["box_hint"])
            if item["id"] == "fr_mineral_adj":
                self.assertTrue(0.40 <= cx <= 0.55)
            elif item.get("g") == "f":
                self.assertLess(cx, 0.40)
            elif item.get("g") == "m":
                self.assertGreater(cx, 0.60)
            boxes.append(item["box_hint"])
        for i, box in enumerate(boxes):
            for other in boxes[i + 1:]:
                self.assertFalse(overlaps(box, other))

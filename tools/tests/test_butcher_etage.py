"""Candidate upstairs butcher, kept off the live 51-word shop."""
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


NINE = [
    "fr_boucherie_noun", "fr_crevette_noun", "fr_huitre_noun", "fr_ecaille_noun",
    "fr_abattoir_noun", "fr_steak_noun", "fr_charcutier_noun", "fr_requin_noun", "fr_mangeur_noun",
]
CANDIDATE = ROOT / "docs" / "room-trials" / "boucherie-surfaces" / "candidate"


def live_payload():
    text = (ROOT / "village" / "data" / "boulangerie.js").read_text(encoding="utf-8")
    return json.loads(text[text.index("]=") + 2:].rstrip().rstrip(";"))


class ButcherCandidateDataset(unittest.TestCase):
    def test_production_baseline_excludes_the_nine(self):
        payload = live_payload()
        ids = [it["id"] for room in payload["rooms"].values() for it in room["items"]]
        self.assertEqual(len(ids), 51)
        self.assertEqual(set(ids) & set(NINE), set())
        layout = json.loads((ROOT / "content" / "v2" / "boulangerie" / "layout.json").read_text(encoding="utf-8"))
        self.assertNotIn("boucherie_etage", layout["rooms"])
        self.assertEqual(layout["rooms"]["boucherie"]["doors"], [])
        talks = (ROOT / "village" / "data" / "talk" / "boulangerie.js").read_text(encoding="utf-8")
        self.assertNotIn("Au-dessus de la boucherie", talks)
        source = json.loads((ROOT / "data" / "source" / "conversations.json").read_text(encoding="utf-8"))
        row = next(x for x in source["conversations"] if x["id"] == "C_R_butcher_02")
        self.assertEqual(row["title"], "Le plateau de fruits de mer")
        self.assertNotIn("room", row)

    def test_candidate_has_exactly_the_nine_words(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from stage_butcher_candidate import build_candidate
        built = build_candidate()
        saved = json.loads((CANDIDATE / "room.json").read_text(encoding="utf-8"))
        self.assertEqual(set(it["id"] for it in built["items"]), set(NINE))
        self.assertEqual(len(built["items"]), 9)
        self.assertEqual(built, saved)
        for it in saved["items"]:
            self.assertTrue(it.get("hook"))
            self.assertTrue((CANDIDATE / "cards" / f"{it['id']}.webp").stat().st_size > 500)
            self.assertEqual(it["cardSrc"], f"boulangerie/cards/{it['id']}.webp")

    def test_abattoir_is_a_blank_plaque(self):
        sys.path.insert(0, str(ROOT / "scripts" / "qa"))
        import check_v2
        room = json.loads((CANDIDATE / "room.json").read_text(encoding="utf-8"))
        plaques = [it for it in room["items"] if it.get("plaque") is True]
        self.assertEqual([it["id"] for it in plaques], ["fr_abattoir_noun"])
        plaque = plaques[0]
        self.assertIn("blank plaque", plaque["hook"])
        self.assertIn("not drawn", plaque["hook"])
        # The gloss may name the place. The plaque flag keeps that gloss out of the depiction check.
        depict = " ".join(str(plaque.get(k) or "") for k in ("hook", "scene", "note"))
        for pat in check_v2.BLOCK:
            self.assertIsNone(__import__("re").search(pat, depict, __import__("re").I), pat)

    def test_navigation_is_one_way_until_the_stair_exists(self):
        room = json.loads((CANDIDATE / "room.json").read_text(encoding="utf-8"))
        links = json.loads((CANDIDATE / "links.json").read_text(encoding="utf-8"))
        self.assertEqual(room["backTo"], "boucherie")
        self.assertEqual([d["to"] for d in room["doors"]], ["boucherie"])
        self.assertEqual(room["doors"][0]["hit"], [590, 450, 150, 140])
        self.assertEqual(room["doors"][0]["thumb"], "boulangerie/boucherie.jpg")
        self.assertTrue(links["down"]["painted"])
        self.assertFalse(links["up"]["painted"])
        self.assertNotIn("boucherie-down-candidate", json.dumps(links))
        dialogue = json.loads((CANDIDATE / "dialogue.json").read_text(encoding="utf-8"))
        self.assertEqual(dialogue["room"], "boulangerie/boucherie_etage")
        self.assertFalse(dialogue["pinned_in_production"])
        text = " ".join(line["fr"] for line in dialogue["lines"])
        lemmas = {
            "fr_boucherie_noun": "boucherie",
            "fr_crevette_noun": "crevette",
            "fr_huitre_noun": "huître",
            "fr_ecaille_noun": "écaille",
            "fr_charcutier_noun": "charcutier",
            "fr_steak_noun": "steak",
            "fr_requin_noun": "requin",
            "fr_mangeur_noun": "mangeur",
            "fr_abattoir_noun": "abattoir",
        }
        used = [wid for wid, lemma in lemmas.items() if lemma in text]
        self.assertGreaterEqual(len(used), 3)
        self.assertNotIn("abattoir", text)
        self.assertIn("charcutier", text)
        self.assertEqual(links["passage"]["arrival_down"], "a counter worker in a striped apron and white cap, a different employee from the red-apron butcher")


if __name__ == "__main__":
    unittest.main()

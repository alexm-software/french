"""Destination coverage must not treat a donor-street copy as integrated."""
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from unbuilt import classify_room, destination_slugs, layout_index


class UnbuiltDestination(unittest.TestCase):
    def test_live_elsewhere_does_not_count_as_built(self):
        live = {
            "fr_nourrir_verb": [("ferme", "ferme")],
            "fr_cheval_noun": [("ferme", "ferme"), ("st_other", "donor")],
            "fr_seller_verb": [("st_bricoleurs", "selliers")],
        }
        row = classify_room(["fr_nourrir_verb", "fr_cheval_noun", "fr_seller_verb"], live, {"ferme"})
        self.assertEqual(row["state"], "partial")
        self.assertEqual(row["here"], 2)
        self.assertEqual(row["elsewhere"], 1)
        self.assertEqual(row["also"], 1)
        self.assertEqual(row["elsewhere_ids"], ["fr_seller_verb"])
        self.assertIn("ferme/ferme", row["here_in"])
        self.assertIn("st_bricoleurs/selliers", row["elsewhere_in"])

    def test_same_building_other_room_is_here(self):
        row = classify_room(["fr_a"], {"fr_a": [("ecole", "tableau")]}, {"ecole"})
        self.assertEqual(row["state"], "built")
        self.assertEqual(row["here_in"], ["ecole/tableau"])

    def test_copy_left_outside_is_extra_not_built(self):
        live = {"fr_a": [("maison", "chambre"), ("st_sommeil", "st_sommeil")]}
        row = classify_room(["fr_a"], live, {"maison"})
        self.assertEqual(row["state"], "extra")
        self.assertEqual(row["also_ids"], ["fr_a"])

    def test_nothing_at_destination_is_unbuilt_even_if_a_copy_exists_elsewhere(self):
        row = classify_room(["fr_a", "fr_b"], {"fr_a": [("st_ciel", "st_ciel")]}, {"camping"})
        self.assertEqual(row["state"], "unbuilt")
        self.assertEqual(row["elsewhere_ids"], ["fr_a"])
        self.assertEqual(row["absent"], 1)
        self.assertEqual(classify_room(["fr_a"], {}, {"couture"})["state"], "unbuilt")

    def test_missing_plan_building_keeps_anywhere_live_reading(self):
        row = classify_room(["fr_a"], {"fr_a": [("ecole", "tableau")]}, set())
        self.assertEqual(row["state"], "built")

    def test_registry_slug_and_claimed_painting_building(self):
        self.assertEqual(destination_slugs("B31_ferme", {}), {"ferme"})
        self.assertEqual(destination_slugs("ST_change", {"ST_change": {"st_croissance"}}), {"st_change", "st_croissance"})
        dest = destination_slugs("B44_musee", {}, {"port"})
        row = classify_room(
            ["fr_pirate_noun", "fr_naviguer_verb"],
            {"fr_pirate_noun": [("port", "bateau_pirate")], "fr_naviguer_verb": [("st_navigateurs", "navigateurs")]},
            dest)
        self.assertEqual(row["state"], "partial")
        self.assertEqual(row["here_ids"], ["fr_pirate_noun"])
        self.assertEqual(row["elsewhere_ids"], ["fr_naviguer_verb"])

    def test_nested_building_id_does_not_alias_the_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "content" / "v2" / "garage"
            folder.mkdir(parents=True)
            (folder / "layout.json").write_text(json.dumps({
                "building": "garage",
                "building_id": "B04_garage",
                "planned": {"garage": {"vocabRoom": "R_garage"}},
                "rooms": {"garage": {"doors": [{"building_id": "B05_maison", "to": "cour"}]}},
            }), encoding="utf-8")
            claim = root / "content" / "v2" / "port"
            claim.mkdir()
            (claim / "layout.json").write_text(json.dumps({
                "building": "port",
                "building_id": "B24_port",
                "planned": {"bateau_pirate": {"vocabRoom": "R_pirate_ship_01"}},
                "rooms": {"bateau_pirate": {"room_id": "R_pirate_ship_01"}},
            }), encoding="utf-8")
            aliases, claims = layout_index(root)
            self.assertEqual(aliases["B04_garage"], {"garage"})
            self.assertNotIn("B05_maison", aliases)
            self.assertEqual(claims["R_pirate_ship_01"], {"port"})
            self.assertEqual(claims["R_garage"], {"garage"})

    def test_default_reads_this_checkout_and_flags_farm_donor(self):
        # Integrating fr_seller_verb into ferme/ferme should update this fixture.
        run = subprocess.run([sys.executable, str(TOOLS / "unbuilt.py"), "--building", "B31_ferme"],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("checkout @", run.stdout)
        self.assertNotIn("clone", run.stderr.lower())
        total = next(l for l in run.stdout.splitlines() if l.startswith("TOTAL"))
        filtered = next(l for l in run.stdout.splitlines() if l.startswith("FILTER"))
        total_plan = int(re.search(r"of ([\d,]+) planned", total).group(1).replace(",", ""))
        filter_plan = int(re.search(r"of (\d+)", filtered).group(1))
        self.assertGreater(total_plan, filter_plan)
        line = next(l for l in run.stdout.splitlines() if "R_farm_animals_01" in l)
        self.assertTrue(line.strip().startswith("partial"))
        self.assertIn("st_bricoleurs/selliers", line)


if __name__ == "__main__":
    unittest.main()

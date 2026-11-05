"""Regression cases that previously spent image calls or hid broken room plans."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from build_prompt import build
from plan_check import simulate_room_labels, validate_manifest, validate_layout
from contact_sheet import sync_manifest_boxes
from walkthrough import covering_walk, read_json, validate as validate_walkthrough
from precheck import load_payload
from zoom_sheet import comparisons


class Workflow(unittest.TestCase):
    def setUp(self):
        self.m = json.loads((TOOLS / 'manifest_template.json').read_text())

    def test_unknown_word_is_a_geometry_diagnostic(self):
        fail, warn = [], []
        simulate_room_labels({"items": [{"id": "fr_missing_example", "box": [100, 100, 50, 50]}]},
                             "ferme", {}, {}, {}, {}, fail, warn)
        self.assertEqual(fail, ["unknown word ID: fr_missing_example"])

    def test_sync_rejects_other_room_and_partial_boxes_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            before = json.dumps(self.m)
            path.write_text(before)
            item = {"id": self.m["items"][0]["id"], "boxPx": [50, 70, 50, 50]}
            with self.assertRaisesRegex(ValueError, "does not match"):
                sync_manifest_boxes(path, {"items": [item]}, self.m["building"], "other")
            with self.assertRaisesRegex(ValueError, "identical, unique"):
                sync_manifest_boxes(path, {"items": [item]}, self.m["building"], self.m["room"])
            self.assertEqual(path.read_text(), before)

    def test_castle_walk_covers_passages_and_local_hub(self):
        root = TOOLS.parent
        folder = root / "content/v2/contes"
        plan = read_json(folder / "walkthrough.json")
        layout = read_json(folder / "layout.json")
        maps = read_json(root / "content/v2/map.json")
        model = validate_walkthrough(plan, layout, maps)
        self.assertEqual(model["hubParents"]["grande_salle"], "cour_chateau")
        self.assertEqual(model["nodes"]["sector:park"]["within"], "overview")
        walk = covering_walk(layout, model)
        self.assertEqual(walk[:3], ["overview", "sector:park", "contes/contes"])
        self.assertEqual(walk[-3:], list(reversed(walk[:3])))
        internal = {(a.split("/")[1], b.split("/")[1]) for a, b in zip(walk, walk[1:])
                    if a.startswith("contes/") and b.startswith("contes/")}
        self.assertEqual(internal, set(model["edges"]))
        wrong_owner = copy.deepcopy(plan)
        wrong_owner["places"]["tour_sorcier"]["within"] = "cour_chateau"
        with self.assertRaisesRegex(ValueError, "no painted route"):
            validate_walkthrough(wrong_owner, layout, maps)
        wrong_owner["places"]["cour_chateau"]["within"] = "cour_chateau"
        with self.assertRaisesRegex(ValueError, "ownership cycle"):
            validate_walkthrough(wrong_owner, layout, maps)
        layout["rooms"]["grande_salle"]["doors"].clear()
        with self.assertRaisesRegex(ValueError, "missing doors"):
            validate_walkthrough(plan, layout, maps)

    def test_empty_hub_compiles_shared_passage_cues(self):
        self.m.update(building="contes", room="cour_chateau", items=[], interactions=[])
        self.m["prompt"]["kind"] = "hub"
        self.m["doors"] = [{"to": "vallee_geants", "where": "left", "painted_as": "castle gate"},
                           {"to": "grande_salle", "where": "back", "painted_as": "keep steps"}]
        self.assertEqual(validate_manifest(self.m)[0], [])
        prompt, missing, left = build(self.m)
        self.assertFalse(missing or left)
        self.assertIn("Circulation only", prompt)
        self.assertIn("keep-steps", prompt)
        self.assertIn("contes/grande_salle.jpg", prompt)

    def test_complete_example_and_first_building(self):
        self.assertEqual(validate_manifest(self.m)[0], [])
        text, missing, left = build(self.m)
        self.assertFalse(missing or left)
        self.assertIn('none yet', text)
        self.assertIn('red -er', text)
        self.assertIn('fr_nous_pron', text)

    def test_zoom_contract_reaches_compiled_prompt(self):
        self.m['prompt'].update(kind='zoom', parent='hall', spot='cabinet')
        self.m['doors'] = []
        self.m['continuity'] = dict(parent_image='village/school/hall.jpg', parent_box=[80, 100, 300, 200], preserve=['blue cabinet opens left', 'three eggs on its upper shelf'])
        self.assertEqual(validate_manifest(self.m)[0], [])
        text, missing, left = build(self.m)
        self.assertFalse(missing or left)
        self.assertIn('three eggs on its upper shelf', text)
        self.assertIn('blue cabinet opens left', text)
        self.assertIn('[80, 100, 300, 200]', text)
        self.assertIn('no painted passage in this close-up', text)
        self.assertNotIn('Clear floor-level thresholds', text)

    def test_rejects_invalid_plans(self):
        mutations = [
            lambda m: m['items'].append(copy.deepcopy(m['items'][0])),
            lambda m: m['items'][1].update(beret='blue'),
            lambda m: m['items'][0].update(count=True),
            lambda m: m['items'][0].update(box_hint=[1270, 100, 50, 50]),
            lambda m: m['items'][0].update(side='left', box_hint=[900, 300, 100, 100]),
            lambda m: m['items'][1].update(box_hint=m['items'][0]['box_hint']),
            lambda m: m['interactions'][0]['who'].append('fr_absent_noun'),
            lambda m: m.update(interactions=[None]),
            lambda m: m.update(prompt_extra={'TYPO': 'silently lost instruction'}),
            lambda m: m.update(text_in_image=['unstructured']),
            lambda m: m['prompt'].update(kind='sprite'),
            lambda m: m.update(coordinate_space='percent'),
            lambda m: m['prompt'].update(kind='zoom', parent='main', spot='cabinet'),
            lambda m: m.update(zooms=[{'to': '', 'words': []}]),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                m = copy.deepcopy(self.m)
                mutate(m)
                self.assertTrue(validate_manifest(m)[0])

    def test_each_verb_checked_even_with_one_valid_beret(self):
        other = copy.deepcopy(self.m['items'][1])
        other.update(id='fr_other_verb', beret='bad', box_hint=[150, 80, 200, 150])
        self.m['items'].append(other)
        self.m['interactions'][1]['who'].append(other['id'])
        self.assertTrue(any('beret' in x for x in validate_manifest(self.m)[0]))

    def test_invalid_write_leaves_manifest_and_output_untouched(self):
        # refs used to appear in 'missing' without affecting exit status; --write
        # previously overwrote prompt_text anyway.
        self.m['prompt'].pop('refs')
        self.m['prompt_text'] = 'accepted previous prompt'
        with tempfile.TemporaryDirectory() as t:
            p, out = Path(t)/'m.json', Path(t)/'prompt.txt'
            p.write_text(json.dumps(self.m)); out.write_text('previous output')
            before = p.read_bytes()
            run = subprocess.run([sys.executable, str(TOOLS/'build_prompt.py'), str(p), '--write', '--output', str(out)], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(p.read_bytes(), before)
            self.assertEqual(out.read_text(), 'previous output')

    def test_write_is_quiet_and_changed_fact_invalidates_prompt(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/'m.json'; p.write_text(json.dumps(self.m))
            cmd = [sys.executable, str(TOOLS/'build_prompt.py'), str(p)]
            run = subprocess.run(cmd+['--write'], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertLess(len(run.stdout), 200)
            self.assertEqual(subprocess.run(cmd+['--check'], capture_output=True).returncode, 0)
            m = json.loads(p.read_text()); m['items'][0]['hook'] = 'We toss NOODLES together.'
            p.write_text(json.dumps(m))
            self.assertNotEqual(subprocess.run(cmd+['--check'], capture_output=True).returncode, 0)

    def test_draft_layout_catches_broken_links_and_units(self):
        good = {'main': 'hall', 'rooms': {'hall': {'items': [], 'doors': [{'to': 'room'}]}, 'room': {'items': [], 'doors': [{'to': 'hall'}]}}}
        self.assertEqual(validate_layout(good)[0], [])
        broken = copy.deepcopy(good); broken['rooms']['hall']['doors'][0]['to'] = 'missing'
        failures = validate_layout(broken)[0]
        self.assertTrue(any('unknown destination' in f for f in failures))
        self.assertTrue(any('unreachable' in f for f in failures))
        broken = copy.deepcopy(good)
        broken['rooms']['room']['items'] = [{'id': 'x', 'box': [1200, 500, 100, 100]}]
        self.assertTrue(any('pixel box' in f for f in validate_layout(broken)[0]))

    def test_payload_parser_tolerates_assignment_whitespace(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t)/'room.js'
            p.write_text('(window.VILLAGE_DATA=window.VILLAGE_DATA||{})["x"] = {"rooms": {}};\n')
            self.assertEqual(load_payload(p), {'rooms': {}})

    def test_continuity_evidence_pins_actual_crop_and_both_images(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            Image.new('RGB', (1280, 720), 'blue').save(root/'parent.png')
            Image.new('RGB', (1280, 720), 'green').save(root/'child.png')
            d = {'rooms': {'hall': {'image': 'parent.png', 'zooms': [{'to': 'box', 'obj': [80, 100, 300, 200]}]}, 'box': {'parent': 'hall', 'image': 'child.png'}}}
            first = comparisons(d, root, root/'a')[0]
            self.assertEqual(first['status'], 'pending')
            self.assertEqual(first['parent_box'], [80, 100, 300, 200])
            self.assertTrue((root/'a'/first['sheet']).exists())
            Image.new('RGB', (1280, 720), 'red').save(root/'parent.png')
            second = comparisons(d, root, root/'b')[0]
            self.assertNotEqual(first['parent_sha256'], second['parent_sha256'])
            self.assertEqual(first['zoom_sha256'], second['zoom_sha256'])
            d['rooms']['box']['parent'] = 'wrong'
            with self.assertRaises(ValueError): comparisons(d, root, root/'c')

    def test_preflight_catches_wrong_verb_beret_and_gender_mismatch(self):
        m = copy.deepcopy(self.m)
        # fr_manger_verb is a regular -er verb (red beret = 'er'); setting 'ir' must fail source preflight
        m['items'][1]['beret'] = 'ir'
        fails, _ = validate_manifest(m)
        self.assertTrue(any('disagrees with canonical verb group' in f for f in fails), fails)

    def test_room_context_init_manifest_scaffolds_valid_nonoverlapping_boxes(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / 'scaffold.json'
            run = subprocess.run(
                [sys.executable, str(TOOLS / 'room_context.py'), 'B63_pompiers', '--room', 'R_abs_problem_02', '--init-manifest', str(out)],
                capture_output=True, text=True
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            sc = json.loads(out.read_text(encoding='utf-8'))
            self.assertEqual(len(sc['items']), 12)
            # Fill TODO placeholders and confirm 0 structural/preflight fails and 0 grid_check warnings
            sc['setting'] = 'Fire station upstairs shelter room'
            sc['scene_situation'] = 'Firefighters practice storm shelter and barrier drills'
            for k in ('refs', 'materials', 'set_apart', 'landmark', 'whimsy', 'differ'):
                sc['prompt'][k] = 'filled ' + k
            for g in sc['interactions']:
                g['doing'] = 'practicing together'
            for it in sc['items']:
                it['hook_object'] = 'cue prop'
                it['shown'] = 'figure with prop'
                it['pose_action'] = 'acting out hook'
                it['interacts_with'] = 'partner'
            fails, warns = validate_manifest(sc)
            self.assertEqual(fails, [])
            self.assertFalse(any('grid_check' in w for w in warns), warns)


if __name__ == '__main__':
    unittest.main()

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
from plan_check import validate_manifest, validate_layout
from precheck import load_payload
from zoom_sheet import comparisons


class Workflow(unittest.TestCase):
    def setUp(self):
        self.m = json.loads((TOOLS / 'manifest_template.json').read_text())

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


if __name__ == '__main__':
    unittest.main()

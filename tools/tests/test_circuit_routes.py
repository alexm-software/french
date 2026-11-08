"""Physical one-way museum routes must remain connected, with a real arrival."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/qa'))
from check_v2 import circuit_errors


class CircuitRoutes(unittest.TestCase):
    def test_connected_circuit(self):
        rooms = {'hub': {'doors': [{'to': 'a'}]},
                 'a': {'arrivalFrom': 'hub', 'oneWay': 'Museum circuit', 'doors': [{'to': 'b'}]},
                 'b': {'doors': [{'to': 'hub'}]}}
        self.assertEqual(circuit_errors(rooms, 'a', 'hub'), [])

    def test_trapped_loop_and_missing_arrival(self):
        rooms = {'hub': {'doors': []},
                 'a': {'arrivalFrom': 'hub', 'oneWay': 'Museum circuit', 'doors': [{'to': 'b'}]},
                 'b': {'doors': [{'to': 'a'}]}}
        self.assertEqual(len(circuit_errors(rooms, 'a', 'hub')), 2)

    def test_cross_building_door_does_not_fake_arrival(self):
        rooms = {'hub': {'doors': [{'to': 'a', 'building': 'elsewhere'}]},
                 'a': {'arrivalFrom': 'hub', 'oneWay': 'Circuit', 'doors': [{'to': 'hub'}]}}
        self.assertEqual(len(circuit_errors(rooms, 'a', 'hub')), 1)

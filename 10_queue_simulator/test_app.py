"""Automated tests. Run from daa_project_assignment:  python3 10_queue_simulator/test_app.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import app

DEFAULT = app.parse_people(app.SAMPLE)


class QueueTests(unittest.TestCase):
    def test1_one_counter_default(self):
        rows, avg, mx = app.simulate(DEFAULT, 1)
        self.assertEqual([r[-1] for r in rows], [0, 3, 5, 6])
        self.assertEqual((avg, mx), (3.5, 6))

    def test2_two_counters_default(self):
        rows, avg, mx = app.simulate(DEFAULT, 2)
        self.assertEqual([r[-1] for r in rows], [0, 0, 2, 1])
        self.assertEqual((avg, mx), (0.75, 2))

    def test3_far_apart_arrivals_zero_wait(self):
        people = app.parse_people('name,arrival,service\nA,0,2\nB,10,2\nC,20,2')
        _, avg, mx = app.simulate(people, 1)
        self.assertEqual((avg, mx), (0, 0))

    def test4_equal_arrivals_keep_input_order(self):
        people = app.parse_people('name,arrival,service\nZed,0,2\nAmy,0,2')
        rows, _, _ = app.simulate(people, 1)
        self.assertEqual([r[0] for r in rows], ['Zed', 'Amy'])

    def test5_invalid_input_rejected(self):
        bad = ['name,arrival,service\nA,0,0',          # zero service
               'name,arrival,service\nA,-1,3',         # negative arrival
               'name,arrival,service\nA,0,3\nA,1,2',   # duplicate name
               'wrong,header,here\nA,0,3',             # bad header
               'name,arrival,service\nA,0']            # missing column
        for text in bad:
            with self.assertRaises(ValueError):
                app.parse_people(text)

    def test6_invalid_counter_count(self):
        for n in (0, 21):
            with self.assertRaises(ValueError):
                app.simulate(DEFAULT, n)

    def test7_extension_timeline_two_counters(self):
        rows, _, _ = app.simulate(DEFAULT, 2)
        tl = [t[:5] for t in app.build_timeline(rows, 2)]
        self.assertIn([2, 'Idle', 0, 1, '-'], tl)
        self.assertIn([2, 'Busy', 1, 4, 'B'], tl)
        self.assertIn([2, 'Idle', 5, 6, '-'], tl)
        self.assertEqual([t for t in tl if t[0] == 1 and t[1] == 'Idle'], [])

    def test8_extension_timeline_utilization(self):
        rows, _, _ = app.simulate(DEFAULT, 1)
        self.assertEqual(app.build_timeline(rows, 1)[0][5], '100%')


if __name__ == '__main__':
    unittest.main(verbosity=2)

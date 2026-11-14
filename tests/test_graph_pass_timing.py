"""A Graph build times each of its passes (graph.Laps, machine/graph/): the summary carries them, and the Graph worker
logs them in one line only for a slow build (slow_build_line)."""
import unittest

import test_graph as tg
from machine.app.graph_actions import GRAPH_SLOW_MS, slow_build_line

PARTS = ['setup', 'identities', 'joins', 'strength', 'projects', 'decisions', 'sides', 'people', 'organizations', 'lookalikes', 'same_person',
         'org_nodes', 'relations', 'rows', 'publish']


class PassTiming(unittest.TestCase):
    setUp, add, build = tg.Graph.setUp, tg.Graph.add, tg.Graph.build

    def test_a_build_times_every_pass_in_order(self):
        self.add(tg.mail(2, 'Kim Lee <kim@client.example>', 'sam@acme.com'), tg.mail(1, 'Sam <sam@acme.com>', 'kim@client.example', ('SENT',)))
        summary = self.build()
        self.assertEqual(list(summary['passes_ms']), PARTS)
        self.assertTrue(all(isinstance(ms, float) and ms >= 0 for ms in summary['passes_ms'].values()))
        self.assertIsNone(slow_build_line(summary))  # a small build says nothing

    def test_only_a_slow_build_logs_its_passes_slowest_first(self):
        quick = {'took_ms': 900, 'passes_ms': {'setup': 100.0, 'people': 700.0, 'publish': 100.0}}
        self.assertIsNone(slow_build_line(quick))
        slow = {'took_ms': 11_000, 'passes_ms': {'setup': 500.0, 'identities': 2500.5, 'people': 8000.0, 'publish': 250.0}}
        self.assertEqual(slow_build_line(slow), 'graph build slow total_ms=11250 people=8000 identities=2500.5 setup=500 publish=250')
        self.assertIsNone(slow_build_line(None))
        self.assertTrue(slow_build_line({'took_ms': GRAPH_SLOW_MS}))  # a summary without parts goes by its compute time


if __name__ == '__main__':
    unittest.main()

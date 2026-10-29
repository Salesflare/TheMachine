"""A bug the owner reported, fixed: a paired self-hosted Machine says which release it runs and its language, and shows
the control plane's lines (fleet.Fleet.fixed, the bug_fixed action, the dashboard's #fixed-notice). No network: the
Network relay is a stand-in."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import fleet  # noqa: E402
import dashboard_parts

spec = importlib.util.spec_from_file_location('bug_fixed_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class Relay:
    def __init__(self, answer):
        self.answer, self.calls = answer, []

    def call(self, method, path, body=None, timeout=40):
        self.calls.append((method, path, body))
        if isinstance(self.answer, Exception):
            raise self.answer
        return self.answer


def paired(answer):
    f = object.__new__(fleet.Fleet)
    f.relay, f.last = Relay(answer), {}
    f.release, f.language = (lambda: 'release-20261028-1442'), (lambda: 'nl')
    return f


class Fixed(unittest.TestCase):
    def test_it_says_its_release_and_language_and_keeps_only_clean_lines(self):
        f = paired({'fixed': [{'id': 's_045cc20be4f1c3e6', 'text': 'Fixed: the Projects tab opens. Thanks for reporting it.',
                               'at': '2026-10-28T15:00:00+00:00', 'extra': 'x'},
                              {'id': 7, 'text': 'not a report'}, 'junk'] + [{'id': f's_{i}', 'text': 'x' * 900} for i in range(9)]})
        got = f.fixed()
        method, path, _ = f.relay.calls[0]
        self.assertEqual((method, path), ('GET', '/fixed?release=release-20261028-1442&lang=nl'))
        self.assertEqual(got[0], {'id': 's_045cc20be4f1c3e6', 'text': 'Fixed: the Projects tab opens. Thanks for reporting it.',
                                  'at': '2026-10-28T15:00:00+00:00'})
        self.assertEqual(len(got), 3)  # the first 5 looked at, the odd ones dropped
        self.assertTrue(all(len(item['text']) <= 300 for item in got))
        self.assertEqual(f.fixed_now, got)  # what the dashboard's state shows, without a call of its own

    def test_seen_closes_one(self):
        f = paired({'fixed': []})
        f.fixed_now = [{'id': 's_045cc20be4f1c3e6', 'text': 'Fixed: x.', 'at': ''}]
        self.assertEqual(f.fixed('s_045cc20be4f1c3e6'), [])
        self.assertEqual(f.fixed_now, [])
        self.assertEqual(f.relay.calls, [('POST', '/fixed', {'seen': 's_045cc20be4f1c3e6'})])

    def test_the_round_asks_once_an_hour_and_never_fails(self):
        f = paired(fleet.Unavailable('down'))
        f.fixed_round()
        f.fixed_round()
        self.assertEqual(len(f.relay.calls), 1)
        f.last['fixed'] -= fleet.Fleet.FIXED_EVERY + 1
        f.fixed_round()
        self.assertEqual(len(f.relay.calls), 2)

    def test_the_dashboard_can_ask(self):
        self.assertIn('bug_fixed', a.SUPPORT_ACTIONS)
        page = dashboard_parts.assemble(ROOT)
        self.assertIn('<div id="fixed-notice" role="status" hidden></div>', page)
        self.assertIn("action:'bug_fixed'", page)
        self.assertIn('state.fixed', page)  # self-hosted: from the state, no call of its own on each render
        self.assertIn("'fixed': list(getattr(getattr(app, 'fleet', None), 'fixed_now', None) or ())", (ROOT / 'assistant.py').read_text())
        self.assertIn("'/_machine/fixed'", page)


if __name__ == '__main__':
    unittest.main()

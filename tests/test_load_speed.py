"""How fast the dashboard opens (load_speed.py, dashboard/shell-speed.js): the page sends two times per load with its
device kind, the Machine keeps a small histogram per local day and kind, and the hosted health report carries count,
median and p90 next to the activity counts. Numbers and kind labels only. Fake loads throughout."""
import importlib.util
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('load_speed_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import load_speed  # noqa: E402
from machine.app import settings_actions  # noqa: E402
from pinned import pinned  # noqa: E402

DAY = '2026-11-20'


def load(drawn, tap, phone=True, app=False, warm=True):
    return {'drawn': drawn, 'tap': tap, 'phone': phone, 'app': app, 'warm': warm}


class LoadSpeed(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        load_speed.ensure(self.db)

    def test_median_p90_and_count_per_kind_from_fake_loads(self):
        phone = [load(ms, ms + 400) for ms in range(1000, 2000, 100)]  # 1000..1900 ms
        self.assertEqual(load_speed.note(self.db, phone, DAY, 'release-20261120-0900'), 10)
        load_speed.note(self.db, [load(300, 350, phone=False, app=True, warm=False)], DAY, 'release-20261120-0900')
        rows = {(r['device'], r['app'], r['warm']): r for r in load_speed.report(self.db, DAY)}
        self.assertEqual(set(rows), {('phone', False, True), ('desktop', True, False)})
        p = rows[('phone', False, True)]
        self.assertEqual((p['count'], p['version'], p['day']), (10, 'release-20261120-0900', DAY))
        # 5% steps: within 3% of the true nearest-rank median (1400) and p90 (1800)
        for key, true in (('drawn_median', 1400), ('drawn_p90', 1800), ('tap_median', 1800), ('tap_p90', 2200)):
            self.assertLess(abs(p[key] - true) / true, 0.03, (key, p[key]))
        self.assertEqual(rows[('desktop', True, False)]['count'], 1)
        # numbers and labels only
        self.assertEqual(set(p), {'day', 'device', 'app', 'warm', 'version', 'count', 'drawn_median', 'drawn_p90', 'tap_median', 'tap_p90'})

    def test_what_is_not_a_load_is_dropped(self):
        bad = [load(0, 10), load(500, 400), load(500, 70_000), load('500', 600), {**load(500, 600), 'phone': 'yes'},
               'x', None, {'drawn': 500, 'tap': 600}]
        self.assertEqual(load_speed.note(self.db, bad, DAY, None), 0)
        self.assertEqual(load_speed.note(self.db, 'not a list', DAY, None), 0)
        self.assertEqual(load_speed.report(self.db, DAY), [])
        self.assertEqual(load_speed.note(self.db, [load(500, 600)] * 50, DAY, None), load_speed.MOST_LOADS)

    def test_a_version_is_a_release_or_a_commit_else_unknown(self):
        load_speed.note(self.db, [load(500, 600)], DAY, 'https://example.com/x')
        load_speed.note(self.db, [load(500, 600)], DAY, 'abcdef123456')
        self.assertEqual(sorted(r['version'] for r in load_speed.report(self.db, DAY)), ['abcdef123456', 'unknown'])

    def test_it_keeps_a_week_and_reports_seven_days(self):
        load_speed.note(self.db, [load(500, 600)], '2026-11-01', None)
        load_speed.note(self.db, [load(500, 600)], '2026-11-13', None)
        load_speed.note(self.db, [load(500, 600)], DAY, None)  # drops days before the 12th
        self.assertEqual([r[0] for r in self.db.execute('SELECT DISTINCT day FROM load_speed ORDER BY day')], ['2026-11-13', DAY])
        self.assertEqual([r['day'] for r in load_speed.report(self.db, DAY)], [DAY])  # the 13th is more than 7 days back

    def test_no_table_reports_nothing(self):
        self.assertEqual(load_speed.report(sqlite3.connect(':memory:'), DAY), [])


class Dashboard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = a.App.__new__(a.App)
        self.app.store = self.store

    def test_only_the_owners_dashboard_counts_and_the_report_carries_it(self):
        self.assertIn('load_speed', a.DASHBOARD_ACTIONS)
        self.assertIn('load_speed', a.OWNER_ACTIONS)
        self.assertEqual(a.App.ACTION_HANDLERS['load_speed'], 'load_speed_action')
        loads = {'loads': [load(900, 1300), load(1100, 1500, phone=False)]}
        self.assertEqual(self.app.load_speed_action('load_speed', loads), {'kept': 0})
        # kept and reported by the owner's day: at 23:30 UTC it is already the next day in Brussels
        with pinned('2026-11-20T23:30:00+00:00'), \
                mock.patch.object(settings_actions, 'local_tz', return_value=ZoneInfo('Europe/Brussels')), \
                mock.patch.object(settings_actions, 'running_release', return_value='release-20261120-0900'):
            self.assertEqual(self.app.load_speed_action('load_speed', loads, owner_dashboard=True), {'kept': 2})
            with self.store.connect() as db:
                report = settings_actions.activity_report(db, 'Europe/Brussels')
        self.assertEqual({r['day'] for r in report['load']}, {'2026-11-21'})
        self.assertIsInstance(report['days'], list)
        self.assertEqual(sorted((r['device'], r['count'], r['version']) for r in report['load']),
                         [('desktop', 1, 'release-20261120-0900'), ('phone', 1, 'release-20261120-0900')])
        json.dumps(report)  # it goes into the health report as is

    def test_the_page_sends_times_and_kind_only_after_its_first_drawing(self):
        part = (ROOT / 'dashboard' / 'shell-speed.js').read_text(encoding='utf-8')
        sent = re.search(r'kept\.push\(\{(.*?)\}\)', part).group(1)
        self.assertEqual(re.findall(r'(\w+):', sent), ['drawn', 'tap', 'phone', 'app', 'at'])
        self.assertIn('warm,', sent)
        self.assertIn('map(({at,...l})=>l)', part)  # the device's own clock stays on the device
        self.assertNotIn('userAgent', part)
        self.assertNotIn('location', part)
        render = (ROOT / 'dashboard' / 'shell-render.js').read_text(encoding='utf-8')
        self.assertIn("performance.mark(shownCached?'tm-warm':'tm-cold')", render)
        self.assertIn("performance.mark('tm-tap')", render)
        import dashboard_parts
        self.assertEqual(next(iter(dashboard_parts.LAZY)), 'newtodo')  # the first part the quiet page loads
        self.assertIn('shell-speed.js', dashboard_parts.LAZY['newtodo'])


if __name__ == '__main__':
    unittest.main()

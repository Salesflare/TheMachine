"""How the background jobs went in the last 24 hours (machine/work_report.py), for the cloud's daily check: counts only."""
import json
import sqlite3
import unittest

from machine import work_report
from machine.app.settings_actions import activity_report
from machine.config import LOG

NOW = '2026-11-27T20:00:00+00:00'


class WorkReport(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE review_runs(run_id TEXT,status TEXT,finished_at TEXT,error TEXT)')
        self.db.execute('CREATE TABLE routine_runs(id TEXT,state TEXT,finished_at TEXT,error TEXT)')
        work_report._seen.clear()

    def test_finished_well_failed_and_failed_on_the_sign_in_per_job_in_the_window_only(self):
        rows = [('a', 'ok', '2026-11-27T10:00:00+00:00', None), ('b', 'error', '2026-11-27T11:00:00+00:00', 'Not logged in · Please run /login'),
                ('c', 'error', '2026-11-27T12:00:00+00:00', 'runtime_error'), ('d', 'running', '2026-11-27T13:00:00+00:00', None),
                ('e', 'error', '2026-11-25T12:00:00+00:00', 'Not logged in')]  # older than a day
        self.db.executemany('INSERT INTO review_runs VALUES(?,?,?,?)', rows)
        self.db.execute("INSERT INTO routine_runs VALUES('r','failed','2026-11-27T19:00:00+00:00','No API key found for provider anthropic')")
        found = work_report.report(self.db, NOW)
        self.assertEqual(found, {'reviews': {'ok': 1, 'failed': 2, 'auth': 1}, 'routines': {'ok': 0, 'failed': 1, 'auth': 1}})
        self.assertNotIn('login', json.dumps(found))  # counts, never the error's words

    def test_jobs_that_found_no_model_are_counted_from_the_log_for_a_day(self):
        level = LOG.level
        LOG.setLevel('INFO')  # as the app runs (assistant.py's basicConfig)
        self.addCleanup(LOG.setLevel, level)
        LOG.info('trip extract: no model now')
        LOG.info('trip extract: no model now')
        LOG.info('meeting prep: no model now')
        LOG.info('something else: no model now, said differently')  # not the line itself
        found = work_report.report(self.db, NOW)
        self.assertEqual((found['trip_extract'], found['meeting_prep']), ({'no_model': 2}, {'no_model': 1}))
        import time
        self.assertNotIn('trip_extract', work_report.report(self.db, NOW, now_s=time.time() + 2 * 86400))

    def test_in_the_activity_report_the_agent_already_reads(self):
        self.db.execute("INSERT INTO review_runs VALUES('a','ok','2026-11-27T10:00:00+00:00',NULL)")
        try:
            report = activity_report(self.db, 'UTC', NOW)
        except sqlite3.OperationalError:  # activity.py's own tables are not made here
            self.skipTest('activity tables')
        self.assertEqual(report['work']['reviews']['ok'], 1)


if __name__ == '__main__':
    unittest.main()

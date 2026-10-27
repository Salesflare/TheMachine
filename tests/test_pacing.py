"""How often background work paces (pacing.py): one stretch per window pacing, its highest threshold, how long it lasted
and how many distinct jobs waited; once a day the finished days go with the error reports, as counts and minutes only,
and nothing when Send error reports is off. The Network is a stand-in here."""
import datetime as dt
import sqlite3
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

import error_feed
import model_budget
import pacing

T0 = dt.datetime(2026, 10, 26, 9, 0, tzinfo=dt.timezone.utc).timestamp()


def window(used, reset, label='5h'):
    return [{'provider': 'anthropic', 'windows': [{'label': label, 'used': used, 'reset': reset}]}]


class Pacing(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / 'db.sqlite'
        self.sent = []

    def tearDown(self):
        self.dir.cleanup()

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        try:
            with db:
                yield db
        finally:
            db.close()

    def call(self, method, path, body):
        self.sent.append((method, path, body))
        return {'ok': True}

    def rows(self):
        with self.connect() as db:
            pacing.ensure(db)
            return db.execute('SELECT started_at,ended_at,win,threshold,jobs FROM pacing_starts ORDER BY id').fetchall()

    def test_a_stretch_counts_once_with_its_threshold_minutes_and_jobs(self):
        track, reset = pacing.Tracker(self.connect), T0 + 3 * 3600
        busy = model_budget.pause(window(70, reset), T0)
        self.assertEqual(busy['threshold'], model_budget.SHORT_PAUSE)
        for minute, job in ((0, 'review'), (2, 'review'), (4, 'ahead:j1'), (6, 'ahead:j2')):  # the same job again counts once
            track.note(busy, job, now_s=T0 + minute * 60)
        track.note(None, 'first_look', first=True, now_s=T0 + 8 * 60)  # the first look may still go: the others wait on
        fuller = model_budget.pause(window(90, reset), T0 + 9 * 60, first=True)
        self.assertEqual(fuller['threshold'], model_budget.FIRST_PAUSE)
        track.note(fuller, 'first_look', first=True, now_s=T0 + 9 * 60)
        track.note(None, 'review', now_s=T0 + 40 * 60)
        self.assertEqual(self.rows(), [('2026-10-26T09:00:00+00:00', '2026-10-26T09:40:00+00:00', '5h', 85, 4)])

    def test_the_week_and_a_reset_window_start_a_new_stretch_and_one_nobody_saw_end_is_capped(self):
        track = pacing.Tracker(self.connect)
        track.note(model_budget.pause(window(70, T0 + 600), T0), 'review', now_s=T0)
        track.note(model_budget.pause(window(70, T0 + 5 * 3600), T0 + 900), 'review', now_s=T0 + 900)  # after the reset at 10 minutes
        week = model_budget.pause(window(95, T0 + 3 * 86400, 'Week'), T0 + 1000)
        track.note(week, 'review', now_s=T0 + 1000)
        # The service stopped mid-stretch: a new one picks it up and ends it no later than a day on
        pacing.Tracker(self.connect).note(None, 'review', now_s=T0 + 3 * 86400)
        rows = self.rows()
        self.assertEqual([(r[2], r[1][:16]) for r in rows], [('5h', '2026-10-26T09:10'), ('5h', '2026-10-26T09:16'), ('week', '2026-10-27T09:16')])  # a day at most
        self.assertEqual(rows[2][3], week['threshold'])

    def test_the_finished_days_go_once_as_counts_only(self):
        track = pacing.Tracker(self.connect)
        busy = model_budget.pause(window(70, T0 + 4 * 3600), T0)
        track.note(busy, 'ahead:job-with-an-id', now_s=T0)
        track.note(None, now_s=T0 + 25 * 60)
        today = dt.datetime(2026, 10, 26, 18, tzinfo=dt.timezone.utc)
        self.assertEqual(pacing.send(self.connect, self.call, today), 0, 'today is not finished yet')
        tomorrow = dt.datetime(2026, 10, 27, 7, tzinfo=dt.timezone.utc)
        self.assertEqual(pacing.send(self.connect, self.call, tomorrow), 1)
        self.assertEqual(pacing.send(self.connect, self.call, tomorrow + dt.timedelta(hours=1)), 0, 'at most every few hours')
        self.assertEqual(self.sent, [('POST', '/errors', {'action': 'pacing', 'day': '2026-10-26',
                                                          'starts': [{'hour': 9, 'window': '5h', 'threshold': 65, 'minutes': 25, 'jobs': 1}]})])
        self.assertNotIn('job-with-an-id', repr(self.sent))
        self.assertEqual(pacing.send(self.connect, self.call, tomorrow + dt.timedelta(hours=7)), 0, 'a day goes once')
        self.assertEqual(len(self.sent), 1)

    def test_error_reports_off_counts_and_sends_nothing(self):
        with self.connect() as db:
            error_feed.set_on(db, False)
        track = pacing.Tracker(self.connect)
        track.note(model_budget.pause(window(70, T0 + 3600), T0), 'review', now_s=T0)
        self.assertEqual(self.rows(), [])
        self.assertEqual(pacing.send(self.connect, self.call, dt.datetime(2026, 10, 28, tzinfo=dt.timezone.utc)), 0)
        self.assertEqual(self.sent, [])

    def test_counting_never_holds_up_the_work(self):
        def broken():
            raise sqlite3.OperationalError('disk I/O error')
        self.assertIsNone(pacing.Tracker(broken).note({'window': '5h', 'threshold': 65}, 'review'))


if __name__ == '__main__':
    unittest.main()

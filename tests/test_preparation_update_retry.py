"""A to-do stuck on a failed run gets one fresh try after the Machine's code or bridge changes (preparation.retry_after_update)."""
import datetime as dt
from pathlib import Path
import tempfile
import unittest

import machine.main as machine_main
import timeutil


class UpdateRetry(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.store = machine_main.Store(self.data / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}])
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(self.data / 'events.sqlite')}
        self.calls = []

    def stuck(self, title='Prepare a useful draft', error='ai_run_failed', hours=1):
        """A to-do the owner pressed Do it on whose run failed twice, `hours` ago."""
        sid = self.store.suggest('task:' + title, title, 'I can draft this.', [1])['id']
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        self.step()
        stamp = (dt.datetime.fromisoformat(timeutil.now()) - dt.timedelta(hours=hours)).isoformat()
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='blocked',error=?,auto_retries=1,reason='I tried twice',updated_at=? WHERE suggestion_id=?", (error, stamp, sid))
            db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE finished_at IS NULL', ('error', stamp))
        self.calls.clear()
        return sid

    def step(self):
        self.app.preparation_step(lambda r: self.calls.append(r) or {'status': 'admitted' if r['action'] == 'start' else 'pending'})

    def prep(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (sid,)).fetchone())

    def starts(self):
        return [c for c in self.calls if c['action'] == 'start']

    def fail_again(self, sid):
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='blocked',error='ai_run_failed',updated_at=? WHERE suggestion_id=?", (timeutil.now(), sid))
            db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE finished_at IS NULL', ('error', timeutil.now()))
        self.calls.clear()

    def test_a_new_release_tries_a_stuck_to_do_once_in_its_own_session(self):
        sid = self.stuck()
        before = self.prep(sid)
        self.step()  # no version known: nothing
        self.assertEqual(self.prep(sid)['status'], 'blocked')
        self.store.code_version = 'release-a'
        self.step()
        after = self.prep(sid)
        self.assertEqual((after['status'], after['update_retry']), ('running', 'release-a:'))
        self.assertNotEqual(after['job_id'], before['job_id'])
        self.assertEqual([c['session_job_id'] for c in self.starts()], [before['session_job_id']])  # its earlier work in context
        self.fail_again(sid)
        for _ in range(3):
            self.step()  # still broken on this version: stays stuck, no loop
        self.assertEqual((self.prep(sid)['status'], self.starts()), ('blocked', []))
        self.store.code_version = 'release-b'
        self.step()
        self.assertEqual((self.prep(sid)['status'], len(self.starts())), ('running', 1))

    def test_a_new_bridge_counts_as_a_new_version(self):
        self.store.code_version = 'release-a'
        self.step()  # this version seen before the to-do got stuck
        sid = self.stuck(hours=0)
        self.step()
        self.assertEqual(self.prep(sid)['status'], 'blocked')  # stuck on this same version: no retry
        (self.data / 'plugin-installed').write_text('abcdef0123456789ffff\n{}\n')
        self.step()
        self.assertEqual((self.prep(sid)['status'], self.prep(sid)['update_retry']), ('running', 'release-a:abcdef0123456789'))

    def test_only_a_runs_own_failure_is_retried(self):
        kept = {error: self.stuck('Task ' + str(error), error) for error in ('stopped', 'usage_limited', None)}
        unconfirmed = self.stuck('Not yet retried', 'completion_unconfirmed')
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET auto_retries=0 WHERE suggestion_id=?', (unconfirmed,))  # its own retry comes first
        self.store.code_version = 'release-a'
        for _ in range(3):
            self.step()
        self.assertEqual({self.prep(s)['status'] for s in [*kept.values(), unconfirmed]}, {'blocked'})
        self.assertEqual(self.starts(), [])

    def test_never_a_confirmed_step_a_snoozed_to_do_or_an_old_one(self):
        confirmed, snoozed, old = self.stuck('Confirmed'), self.stuck('Snoozed'), self.stuck('Old', hours=24 * 8)
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET action_id='a1' WHERE suggestion_id=?", (confirmed,))
            db.execute("UPDATE suggestions SET status='snoozed' WHERE id=?", (snoozed,))
        self.store.code_version = 'release-a'
        for _ in range(3):
            self.step()
        self.assertEqual((self.prep(confirmed)['status'], self.prep(snoozed)['status'], self.prep(old)['status']), ('blocked',) * 3)
        self.assertEqual(self.starts(), [])

    def test_quiet_hours_and_usage_hold_it_and_one_goes_at_a_time(self):
        first, second = self.stuck('First'), self.stuck('Second', hours=2)
        self.store.code_version = 'release-a'
        self.app.night_hold = lambda db, current=None: dt.datetime.now(dt.timezone.utc)
        self.step()
        self.app.night_hold = lambda db, current=None: None
        self.app.background_pause = lambda **k: {'window': '5h', 'until': 0, 'limited': True}
        self.step()
        self.assertEqual((self.prep(first)['status'], self.prep(second)['status']), ('blocked', 'blocked'))
        del self.app.night_hold, self.app.background_pause
        self.step()
        self.step()
        self.assertEqual((self.prep(first)['status'], self.prep(second)['status']), ('running', 'blocked'))  # the latest stuck first
        self.fail_again(first)
        self.step()
        self.assertEqual((self.prep(first)['status'], self.prep(second)['status']), ('blocked', 'running'))


if __name__ == '__main__':
    unittest.main()

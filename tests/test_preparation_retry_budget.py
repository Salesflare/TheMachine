"""No wasted re-preparations (2026-11-22): a restart or release never redoes a finished to-do, failed runs back off and
stop after preparation_state.AUTO_RETRIES automatic retries until something new comes in, and every run records why it
started from its first moment (preparation_runs.basis), also one that never makes a tool call."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import unittest

import error_feed
import machine.main as machine_main
import preparation_state
import timeutil


def ago(**delta):
    return (dt.datetime.fromisoformat(timeutil.now()) - dt.timedelta(**delta)).isoformat()


class RetryBudget(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        self.store = self.open_store()
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}])
        self.sid = self.store.suggest('task:reply', 'Prepare a useful draft', 'I can draft this.', [1])['id']
        self.app = self.open_app(self.store)
        self.calls = []

    def open_store(self):
        return machine_main.Store(self.data / 'events.sqlite')

    def open_app(self, store):
        app = object.__new__(machine_main.App)
        app.store = store
        app.config = {'accounts': [], 'database': str(self.data / 'events.sqlite')}
        return app

    def step(self, status='admitted'):
        """One worker tick: a start is admitted, a running run's status check says `status`."""
        self.app.preparation_step(lambda r: self.calls.append(r) or (
            {'status': 'admitted'} if r['action'] == 'start' else {'status': 'lost'} if r['action'] == 'stop' else {'status': status}))

    def starts(self):
        return [c for c in self.calls if c['action'] == 'start']

    def prep(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone())

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM preparation_runs WHERE suggestion_id=? ORDER BY rowid', (self.sid,))]

    def due(self):
        """The backoff is over."""
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET retry_at=NULL')

    def run_fails(self, status='error'):
        """The current queued run starts and then fails with `status`; True when it started."""
        before = len(self.starts())
        self.step()
        if len(self.starts()) == before:
            return False
        self.step(status)
        return True

    def card(self):
        return next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == self.sid)

    def test_a_finished_preparation_is_never_redone_by_a_restart_or_a_release(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.step()
        self.store.prepare(self.sid, 'Draft ready.', self.prep()['job_id'])
        self.step('ok')
        self.assertEqual((self.prep()['status'], len(self.runs())), ('done', 1))
        for version in ('release-a', 'release-b'):  # a release, then the service restarted on it
            self.store = self.open_store()
            self.store.code_version = version
            self.app = self.open_app(self.store)
            for _ in range(3):
                self.step()
        self.assertEqual((self.prep()['status'], len(self.runs()), len(self.starts())), ('done', 1, 1))

    def test_failed_runs_back_off_and_stop_after_two_automatic_retries(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.assertTrue(self.run_fails('error'))
        job = self.prep()
        self.assertEqual((job['status'], job['retries_spent']), ('queued', 1))
        self.assertGreater(job['retry_at'], timeutil.now())  # first retry after a pause
        self.assertFalse(self.run_fails())  # not before it
        self.due()
        self.assertTrue(self.run_fails('lost'))  # the first automatic retry, lost too (2026-11-20)
        job = self.prep()
        self.assertEqual((job['status'], job['retries_spent']), ('blocked', 1))
        self.store.code_version = 'release-a'
        self.step()
        self.assertEqual(self.prep()['status'], 'blocked')  # a release right after the failure: it backs off first
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET updated_at=?', (ago(minutes=20),))
        self.assertTrue(self.run_fails('timed_out'))  # the second: the release's
        job = self.prep()
        self.assertEqual((job['status'], job['retries_spent']), ('blocked', preparation_state.AUTO_RETRIES))
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET updated_at=?', (ago(hours=1),))
        self.store.code_version = 'release-b'
        before = len(self.starts())
        for _ in range(3):
            self.step()
        self.assertEqual(len(self.starts()), before)  # no third, also not for a newer release
        card = self.card()
        self.assertEqual((card['status'], card['preparation_status']), ('accepted', 'blocked'))  # Stuck with Try again, not Preparing…
        self.assertEqual(len(self.runs()), 3)

    def test_each_failure_is_counted_by_its_class_without_its_text(self):
        # The provider overloaded at both tries: one signature per class and outcome in the error reports, nothing else
        receipt = {'status': 'error', 'error': 'runtime_error', 'error_phase': 'runtime', 'reason': 'provider_overloaded', 'message': 'private text'}
        fail = lambda r: {'status': 'admitted'} if r['action'] == 'start' else receipt
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        with self.assertLogs('personal-assistant', 'WARNING') as logs:
            for _ in range(2):
                self.app.preparation_step(fail)
                self.app.preparation_step(fail)
                self.due()
        self.assertEqual([line.split(':', 2)[2] for line in logs.output], [
            'preparation failed error=runtime_error phase=runtime after=retry reason=provider_overloaded',
            'preparation failed error=runtime_error phase=runtime after=stopped reason=provider_overloaded'])
        with self.store.connect() as db:
            rows = [tuple(r) for r in db.execute('SELECT source,kind,message,location,count FROM error_feed ORDER BY message')]
            self.assertTrue(all(error_feed.allowed(r[2]) for r in rows))
        self.assertEqual(rows, [('job', 'runtime_error.provider_overloaded', f'runtime {after}', 'machine/app/preparation.py:preparation_run_step', 1)
                                for after in ('retry', 'stopped')])
        # a reason or code outside the fixed lists never goes
        receipt.update(error='private_code', reason='private reason', error_phase='private')
        self.store.decide(self.sid, 'retry', '', 'try', 'dashboard')
        self.app.preparation_step(fail)
        self.app.preparation_step(fail)
        with self.store.connect() as db:
            kinds = {r[0] for r in db.execute('SELECT kind FROM error_feed')}
        self.assertEqual(kinds, {'runtime_error.provider_overloaded', 'runtime_error'})

    def test_a_sign_in_the_ai_cant_use_is_logged_but_never_reported(self):
        # Claude Code's sign-in lapsed: the owner's to fix (Needs you says it), not a bug in the error reports
        receipt = {'status': 'error', 'error': 'runtime_error', 'error_phase': 'runtime', 'reason': 'auth_failed'}
        fail = lambda r: {'status': 'admitted'} if r['action'] == 'start' else receipt
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        with self.assertLogs('personal-assistant', 'WARNING') as logs:
            self.app.preparation_step(fail)
            self.app.preparation_step(fail)
        self.assertIn('reason=auth_failed', logs.output[0])
        self.assertEqual(self.counted(), [])

    def counted(self):
        with self.store.connect() as db:
            error_feed.ensure(db)
            return [r[0] for r in db.execute("SELECT kind FROM error_feed WHERE source='job'")]

    def running(self):
        self.setUp()
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.step()
        self.assertEqual(self.prep()['status'], 'running')
        return self.prep()

    def test_a_run_somebody_ended_is_no_failure(self):
        owner = {'stop': lambda: self.app.action('chat_stop', {'suggestion_id': self.sid}, owner_dashboard=True),
                 'change': lambda: self.store.decide(self.sid, 'other', 'Make it shorter', 'own', 'dashboard'),
                 'dismiss': lambda: self.store.decide(self.sid, 'reject', '', 'own', 'dashboard'),
                 'done': lambda: self.store.decide(self.sid, 'complete', '', 'own', 'dashboard')}
        # pressed while the status check was on its way, whatever it then says
        for name, status in (('stop', 'aborted'), ('stop', 'error'), ('change', 'aborted'), ('dismiss', 'lost'), ('done', 'error')):
            with self.subTest(name=name, status=status):
                job = self.running()
                self.app.card_chat_gateway = lambda *args, **kwargs: {'messages': []}
                asked = []

                def runner(request):
                    asked.append(request['action'])
                    owner[name]()
                    return {'status': status}
                self.app.preparation_run_step(job, runner)
                now = self.prep()
                self.assertEqual(asked, ['status'])
                self.assertTrue(now['job_id'] != job['job_id'] or now['status'] not in ('starting', 'running'))
                self.app.preparation_step(lambda r: {'status': 'aborted'} if r['action'] == 'stop' else {'status': 'admitted'})
                self.assertEqual(self.counted(), [])
        self.running()  # ended in OpenClaw itself, or by a restart: tried again as before, not counted
        self.step('aborted')
        self.assertEqual((self.prep()['status'], self.prep()['error']), ('queued', 'ai_run_interrupted'))
        self.assertEqual(self.counted(), [])
        self.running()
        self.step('error')
        self.assertEqual(self.counted(), ['runtime_error'])  # and a real failure is

    def test_the_owners_try_again_runs_once_and_something_new_brings_new_retries(self):
        # 2026-11-18: each Try again ran, ended within a minute without a result, and was retried by itself the same way
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.assertTrue(self.run_fails('error'))
        self.due()
        self.assertTrue(self.run_fails('ok'))  # its retry ended without a result too
        self.assertEqual((self.prep()['status'], self.prep()['retries_spent']), ('blocked', 1))
        self.store.decide(self.sid, 'retry', '', 'try-0', 'dashboard')
        self.assertTrue(self.run_fails('ok'))
        self.assertEqual((self.prep()['status'], self.prep()['retries_spent']), ('queued', 2))  # the last automatic retry left
        self.due()
        self.assertTrue(self.run_fails('ok'))
        self.assertEqual(self.prep()['reason'], 'I tried twice but couldn’t finish this. Tap Try again, or change the request.')
        for n in (1, 2):
            self.store.decide(self.sid, 'retry', '', f'try-{n}', 'dashboard')
            self.assertTrue(self.run_fails('ok'))  # the owner's Try again always runs
            job = self.prep()
            self.assertEqual(job['status'], 'blocked')  # with no automatic retry behind it
            self.assertEqual(job['reason'], 'This didn’t finish. Tap Try again, or change the request.')
            self.due()
            self.step()
        self.assertEqual(len(self.runs()), 6)  # Do it and its retry, Try again and its retry, two more Try agains
        self.store.decide(self.sid, 'other', 'Use the shorter version', 'chat-new', 'dashboard')  # new words: new retries
        self.assertTrue(self.run_fails('error'))
        self.assertEqual((self.prep()['status'], self.prep()['retries_spent']), ('queued', 1))

    def test_a_run_lost_at_the_deadline_is_retried_once_after_a_pause(self):
        # 2026-11-20: runs lost after 35 minutes were retried at once and again on every release
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        for _ in range(2):
            self.step()
            with self.store.connect() as db:
                db.execute('UPDATE preparations SET started_at=?', (ago(hours=1),))
            self.step('pending')  # overdue: stopped, confirmed ended
            self.step()
            self.due()
        self.assertEqual(len(self.starts()), 2)  # the run and its one retry
        job = self.prep()
        self.assertEqual((job['status'], job['error'], job['retries_spent']), ('blocked', 'completion_unconfirmed', 1))
        self.store.decide(self.sid, 'retry', '', 'try', 'dashboard')  # the owner's Try again, lost the same way
        self.step()
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET started_at=?', (ago(hours=1),))
        self.step('pending')
        self.assertEqual(self.prep()['reason'], 'This is taking too long. I’ll stop that run and try once more.')  # one left
        self.step()
        self.due()
        self.step()
        self.assertEqual((len(self.starts()), self.prep()['retries_spent']), (4, 2))
        with self.store.connect() as db:
            db.execute('UPDATE preparations SET started_at=?', (ago(hours=1),))
        self.step('pending')
        self.step()
        self.due()
        for _ in range(3):
            self.step()
        self.assertEqual((len(self.starts()), self.prep()['status']), (4, 'blocked'))

    def test_every_run_records_why_it_started_from_its_first_moment(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.step()
        first = self.runs()[0]
        self.assertEqual(json.loads(first['basis']), {'kind': 'doit', 'approval': 'click'})  # before any tool call
        self.step('ok')  # ended without a tool call or a result (2026-11-18)
        self.due()
        self.step()
        self.step('error')
        retry = self.runs()[1]
        self.assertEqual(json.loads(retry['basis']), {'kind': 'doit', 'approval': 'click', 'retry': 'auto'})
        self.store.decide(self.sid, 'other', 'Make it shorter', 'chat-1', 'dashboard')
        self.step()
        self.assertEqual(json.loads(self.runs()[2]['basis'])['kind'], 'chat')
        self.assertEqual([r for r in self.runs() if r['basis'] is None], [])

    def snooze_and_wake(self, news=False):
        """The owner snoozes the to-do while it shows as being worked on; with `news` something new comes in for it while
        it sleeps (kept on it without waking it); then the snooze is over."""
        self.store.decide(self.sid, 'snooze', '', 'later', 'dashboard', snooze_hours=1)
        if news:
            with self.store.connect() as db:
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('update:new',?,'update','A later message was added','assistant',?)",
                           (self.sid, timeutil.now()))
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET snoozed_until=? WHERE id=?", (ago(minutes=1), self.sid))
        self.assertEqual(self.store.wake_snoozed(), 1)
        self.assertEqual(self.card()['status'], 'accepted')

    def prepared_while_accepted(self):
        """A finished preparation on a to-do that still shows as taken on (Do it, its result saved)."""
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.step()
        self.store.prepare(self.sid, 'Draft ready.', self.prep()['job_id'])
        self.step('ok')
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (self.sid,))
        self.assertEqual((self.prep()['status'], len(self.runs())), ('done', 1))

    def test_a_to_do_waking_from_its_snooze_with_nothing_new_keeps_its_preparation(self):
        self.prepared_while_accepted()
        self.snooze_and_wake()
        self.step()
        self.step()
        self.assertEqual((self.prep()['status'], len(self.runs()), len(self.starts())), ('done', 1, 1))

    def test_a_to_do_waking_with_something_new_is_prepared_again_with_what_allowed_it(self):
        self.prepared_while_accepted()
        self.snooze_and_wake(news=True)
        self.step()
        self.assertEqual((len(self.runs()), len(self.starts())), (2, 2))
        self.assertEqual(json.loads(self.runs()[1]['basis']), {'kind': 'doit', 'approval': 'click', 'resumed': 'snooze'})

    def test_a_to_do_waking_without_a_finished_preparation_is_prepared_as_before(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.snooze_and_wake()  # snoozed before its run started: that run was stopped
        self.step()
        self.assertEqual((len(self.runs()), len(self.starts())), (1, 1))
        self.assertEqual(json.loads(self.runs()[0]['basis']), {'kind': 'doit', 'approval': 'click', 'resumed': 'snooze'})


if __name__ == '__main__':
    unittest.main()

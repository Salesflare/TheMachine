"""A run that saved its result ends by itself, also once something new took its place (action_runs.stop_stale_runs)."""
import datetime as dt
from pathlib import Path
import tempfile
import unittest

from machine.app import action_runs
import machine.chat as machine_chat
import machine.main as machine_main
from seams import patch_everywhere
import timeutil


class StaleRuns(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Actual evidence', 'metadata': {}, 'deleted': False}])
        self.sid = self.store.suggest('task', 'Prepare a useful draft', 'I can draft this.', [1])['id']
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.config = self.store, {'accounts': []}
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        self.job = self.q('SELECT job_id FROM preparations WHERE suggestion_id=?', self.sid)['job_id']
        self.calls = []

    def q(self, sql, *args):
        with self.store.connect() as db:
            return dict(db.execute(sql, args).fetchone())

    def run_row(self):
        return self.q('SELECT status,finished_at FROM preparation_runs WHERE job_id=?', self.job)

    def stale(self, seconds=0, **receipts):
        """One round, `seconds` from now; {action: status} of the Gateway's answers. Returns the calls it made."""
        self.calls.clear()
        at = (dt.datetime.fromisoformat(timeutil.now()) + dt.timedelta(seconds=seconds)).isoformat()
        with self.store.connect() as db:
            db.execute('UPDATE preparation_runs SET retry_at=NULL')
        with patch_everywhere(timeutil, 'now', return_value=at):
            self.app.stop_stale_runs(lambda r: self.calls.append(r['action']) or {'status': receipts[r['action']]})
        return list(self.calls)

    def saves(self):
        self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job, 'body': 'Draft ready.', 'outcome': 'needs_you', 'needs': 'check the draft'})

    def carries_on(self):
        """The Machine's own next step takes the run's place at once (a doc made after the save)."""
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (self.sid,))
            self.store.queue_preparation(db, self.sid, 'after:one')
        self.assertNotEqual(self.q('SELECT job_id FROM preparations WHERE suggestion_id=?', self.sid)['job_id'], self.job)

    def test_a_saved_run_that_was_replaced_is_asked_how_it_ended(self):
        # 2026-11-24: recorded as lost though it had ended
        self.saves()
        self.carries_on()
        self.assertEqual(self.stale(status='ok', stop='lost'), ['status'])
        self.assertEqual(self.run_row()['status'], 'ok')

    def test_it_is_not_cut_off_right_after_it_saved(self):
        self.saves()
        self.carries_on()
        self.assertEqual(self.stale(status='pending', stop='aborted'), ['status'])
        self.assertIsNone(self.run_row()['finished_at'])
        late = action_runs.PREPARATION_SETTLE_REPLACED_SECONDS + 5  # what took its place waits no longer than that
        self.assertEqual(self.stale(late, status='pending', stop='aborted'), ['status', 'stop'])
        self.assertEqual(self.run_row()['status'], 'aborted')

    def test_also_when_the_owner_wrote_right_after_it(self):
        self.saves()
        self.store.decide(self.sid, 'other', 'Shorter please', 'note', 'dashboard')
        self.assertEqual(self.stale(status='pending', stop='aborted'), ['status'])
        self.assertEqual(self.stale(5, status='ok', stop='lost'), ['status'])
        self.assertEqual(self.run_row()['status'], 'ok')

    def test_a_saved_blocker_is_let_end_too(self):
        self.app.action('preparation_blocked', {'suggestion_id': self.sid, 'job_id': self.job, 'reason': 'Which address?',
                                                'questions': [{'question': 'Which address should it go to?'}]})
        self.store.decide(self.sid, 'other', 'The office one', 'note', 'dashboard')
        self.assertEqual(self.stale(status='ok', stop='lost'), ['status'])
        self.assertEqual(self.run_row()['status'], 'ok')

    def test_a_run_that_saved_nothing_is_stopped_at_once_and_keeps_how_it_really_ended(self):
        self.store.decide(self.sid, 'other', 'Change it', 'note', 'dashboard')
        self.assertEqual(self.stale(status='error', stop='lost'), ['stop', 'status'])  # it had ended before the stop
        self.assertEqual(self.run_row()['status'], 'error')

    def test_a_run_the_gateway_knows_nothing_of_is_lost(self):
        self.store.decide(self.sid, 'other', 'Change it', 'note', 'dashboard')
        self.assertEqual(self.stale(status='pending', stop='lost'), ['stop', 'status'])
        self.assertEqual(self.run_row()['status'], 'lost')

    def test_a_run_still_going_that_saved_nothing_is_stopped(self):
        self.store.decide(self.sid, 'other', 'Change it', 'note', 'dashboard')
        self.assertEqual(self.stale(status='pending', stop='aborted'), ['stop'])
        self.assertEqual(self.run_row()['status'], 'aborted')

    def test_a_result_without_a_reply_shows_its_body_however_the_run_ended(self):
        transcript = [{'role': 'assistant', 'timestamp': 5, 'content': [{'type': 'text', 'text': 'Half a sen'}], '__openclaw': {'runId': self.job}}]
        saved = {self.job: [{'kind': 'reply', 'text': 'Draft ready.', 'drafts': [], 'files': [], 'at': 4}]}
        for messages in (transcript, []):  # cut off in its last words, or its session gone
            with patch_everywhere(machine_chat, 'chat_run_keys', lambda found: [self.job] * len(found)):
                items = machine_chat.chat_items(messages, [], saved)
            self.assertEqual([i['text'] for i in items if i['kind'] == 'reply'], ['Draft ready.'])


if __name__ == '__main__':
    unittest.main()

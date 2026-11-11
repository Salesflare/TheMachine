"""A to-do whose run got stuck, then handed to Codex from its chat: while the job runs it is working, never Stuck, on the
card, in its chat, on Telegram and on the phone alike. When the job ends its result decides: a result clears Stuck, a
failed job leaves it stuck. A run that got stuck after the job started is the newer word and stays."""
from pathlib import Path
from unittest.mock import patch
import unittest

import agent_jobs
from machine.delivery import deliver
import test_preparation as p

a = p.a
OLD = '2026-01-05T09:00:00+00:00'  # the stuck run, before any job
LATER = '2999-01-01T00:00:00+00:00'  # a run stuck after the job started


class StuckThenHandedOff(unittest.TestCase):
    setUp_base = p.Preparation.setUp

    def setUp(self):
        self.setUp_base()
        self.accept()
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        self.stuck(OLD)
        self.jobs = agent_jobs.AgentJobs(self.store.connect, {'accounts': [], 'agents': {}}, Path(self.temp.name) / 'agent-jobs',
                                         card=lambda sid: {'card': {'id': sid, 'title': 'Prepare a useful draft', 'body': 'x'}})

    accept = p.Preparation.accept

    def stuck(self, at):
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='blocked',error='completion_unconfirmed',reason='This didn’t finish, also on the second try.',updated_at=?",
                       (at,))
            db.execute("UPDATE deliveries SET needs_edit=0")

    def card(self):
        return next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == self.sid)

    def telegram_row(self):
        with self.store.connect() as db:
            return dict(db.execute(deliver.shown_rows(db, deliver.EDIT_ROWS).replace('WHERE d.needs_edit=1 AND', 'WHERE') + ' AND s.id=?', (self.sid,)).fetchone())

    def needs_edit(self):
        return self.q('SELECT needs_edit FROM deliveries WHERE suggestion_id=?', self.sid)['needs_edit']

    q = p.Preparation.q

    def hand_off(self):
        with patch.object(self.jobs, 'tool', return_value={'id': 'codex', 'place': 'local'}), \
             patch.object(self.jobs, 'prepare_folder'), patch.object(self.jobs, 'launch'):
            return self.jobs.start(self.sid, 'codex', 'Find out why saving the workflow fails.')

    def test_stuck_before_the_handoff(self):
        card = self.card()
        self.assertEqual((card['preparation_status'], card['preparation_error']), ('blocked', 'completion_unconfirmed'))
        self.assertEqual(a.app_notice(self.store, self.app.config, self.sid)['line'], 'Stuck: Prepare a useful draft')
        self.assertIn('I’m stuck', a.card(self.telegram_row()))

    def test_a_running_handoff_shows_working_everywhere_then_its_result_decides(self):
        job = self.hand_off()
        self.assertEqual(self.needs_edit(), 1)  # its Telegram message is brought up to date
        card = self.card()
        self.assertEqual(card['preparation_status'], agent_jobs.WORKING)
        self.assertIsNone(card['preparation_error'])
        self.assertIsNone(card['preparation_reason'])
        self.assertFalse(a.ask_blocked(card))
        notice = a.app_notice(self.store, self.app.config, self.sid)
        self.assertEqual(notice['line'], 'Working: Prepare a useful draft')
        row = self.telegram_row()
        self.assertEqual(row['preparation_status'], agent_jobs.WORKING)
        self.assertNotIn('I’m stuck', a.card(row))
        self.assertIn('Working…', a.card(row))
        # The stuck run's own row keeps what happened
        self.assertEqual(self.q('SELECT status,error FROM preparations WHERE suggestion_id=?', self.sid), {'status': 'blocked', 'error': 'completion_unconfirmed'})
        # Running (claimed by its worker) is still working
        with self.store.connect() as db:
            db.execute("UPDATE agent_jobs SET status='running',started_at=? WHERE id=?", (a.now(), job['id']))
        self.assertEqual(self.card()['preparation_status'], agent_jobs.WORKING)
        # It ends with a result: not Stuck, not Preparing, nothing runs on it
        with self.store.connect() as db:
            db.execute('UPDATE deliveries SET needs_edit=0')
        self.assertTrue(self.jobs.result(job['id'], None, 'Found the cause.', files=[], diff=''))
        self.assertEqual(self.needs_edit(), 1)
        card = self.card()
        self.assertEqual(card['preparation_status'], agent_jobs.HANDED_BACK)
        self.assertNotIn(a.app_notice(self.store, self.app.config, self.sid)['line'].split(':')[0], ('Stuck', 'Preparing', 'Working'))
        self.assertNotIn('I’m stuck', a.card(self.telegram_row()))

    def test_a_failed_job_leaves_it_stuck(self):
        job = self.hand_off()
        self.assertEqual(self.card()['preparation_status'], agent_jobs.WORKING)
        self.jobs.finish(job['id'], 'failed', error='It stopped.', error_kind='exit')
        card = self.card()
        self.assertEqual((card['preparation_status'], card['preparation_error']), ('blocked', 'completion_unconfirmed'))
        self.assertEqual(a.app_notice(self.store, self.app.config, self.sid)['line'], 'Stuck: Prepare a useful draft')
        self.assertIn('I’m stuck', a.card(self.telegram_row()))

    def test_a_run_stuck_after_the_job_started_is_the_newer_word(self):
        self.hand_off()
        self.stuck(LATER)
        self.assertEqual(self.card()['preparation_status'], 'blocked')

    def test_a_machine_without_handing_off_reads_its_runs_as_they_are(self):
        with self.store.connect() as db:
            db.execute('DROP TABLE agent_jobs')
            self.assertEqual(agent_jobs.shown_preparation(db), 'p.status')
        self.assertEqual(self.card()['preparation_status'], 'blocked')


if __name__ == '__main__':
    unittest.main()

"""A Claude Code or Codex job's result is part of its card's state: the card's chat turn, its preparation and the
review's status read it as the latest truth of what was done, so the next step never repeats finished work."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import agent_jobs
from machine.chat import AGENT_DO_IT_NOTE

spec = importlib.util.spec_from_file_location('card_agent_work_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

DONE = 'The acme.example link is now live across all 14 languages, keeping the existing wording.'
STALE = 'Next, edit the agency article: link the existing words to acme.example and publish.'


class CardAgentWork(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Final entry', 'body': 'Pat sent the final entry.', 'metadata': {}, 'deleted': False}], None)
        self.sid = self.store.suggest('task', 'Acme sent the final entry', STALE, [1])['id']
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite')}
        with self.store.connect() as db:
            db.executescript(agent_jobs.SCHEMA)

    def job(self, status='result', summary=DONE, progress=None, id='aj_00000000000000a1'):
        with self.store.connect() as db:
            db.execute("INSERT INTO agent_jobs(id,suggestion_id,tool,place,status,brief,asks,summary,progress,files,created_at,updated_at,started_at,finished_at) "
                       "VALUES(?,?,'codex','local',?,'b',?,?,?,'[]','2026-10-23T09:17:00+00:00','2026-10-23T09:45:00+00:00','2026-10-23T09:31:00+00:00',?)",
                       (id, self.sid, status, json.dumps([{'at': '2026-10-23T09:30:00+00:00', 'text': 'Add the link in every language'}]),
                        summary if status == 'result' else None, progress, '2026-10-23T09:45:00+00:00' if status == 'result' else None))

    def chat_turn(self):
        """A first run, then the owner asks in the card's chat: the short follow-up turn's message."""
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        with self.store.connect() as db:
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=?", (a.now(),))
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared'")
        self.store.decide(self.sid, 'other', 'Alright, and what is the next step?', 'chat-' + 'b' * 36, 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c['message'] for c in calls if c.get('message'))

    def test_the_chat_turn_knows_what_the_finished_job_did(self):
        self.job()
        message = self.chat_turn()
        self.assertIn('wrote to you in the chat', message)
        self.assertIn('Codex finished', message)
        self.assertIn(DONE, message)
        self.assertIn('Add the link in every language', message)
        self.assertIn('what it reports done is done', message)
        # The stale next step is not what the turn is told about the work: the job's result comes after it, as the newer truth.
        self.assertNotIn(STALE, message)

    def test_a_full_preparation_knows_it_too(self):
        self.job()
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        self.assertIn('the owner tapped Do it', message)
        self.assertIn(DONE, message)

    def test_the_chat_turn_knows_where_its_files_are_and_may_run_them(self):
        # "push it live" in the to-do's chat: the turn is told the job's folder and that the ask is the owner's approval.
        self.job(id='aj_2ec3c49846bb402e')
        work = Path(self.temp.name) / 'agent-jobs' / 'aj_2ec3c49846bb402e' / 'work'
        work.mkdir(parents=True)
        message = self.chat_turn()
        self.assertIn(f'its folder: {work}', message)
        self.assertIn('run, publish or deploy what it prepared, that is their approval', message)
        self.assertIn('open the job in Codex and run it there', message)

    def do_it_message(self, choice='accept', source='dashboard'):
        """The owner's tap on the card after the job finished: the message its preparation starts with."""
        self.store.decide(self.sid, choice, '' if choice == 'accept' else 'who approves this?', 'click' if choice == 'accept' else 'chat-' + 'c' * 36, source)
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c['message'] for c in calls if c.get('message'))

    def test_do_it_after_a_job_left_the_publish_step_runs_that_step(self):
        # A Codex job prepared and built a site update, then stopped under its own limits: "Remaining for you: run
        # ./publish.sh to push and deploy, then send the prepared reply." The owner's Do it is the approval for that step.
        self.job(summary='The update is committed and the production build passed. Remaining for you under this job\'s limits: '
                         'run ./publish.sh to push and deploy, then send the prepared reply to Pat.')
        message = self.do_it_message()
        self.assertIn('the owner tapped Do it', message)
        self.assertIn('./publish.sh to push and deploy', message)
        self.assertIn(AGENT_DO_IT_NOTE, message)
        self.assertIn('Never offer it back as a Confirm or Publish button', message)
        # Sending stays separate: the prepared reply is a draft the owner reads and sends.
        self.assertIn('save it as a draft on the to-do for the owner to read and send, and never send it in this turn', message)

    def test_a_chat_question_or_a_closed_job_is_not_that_approval(self):
        self.job()
        self.assertNotIn(AGENT_DO_IT_NOTE, self.chat_turn())  # "what is the next step?" asks, it doesn't tap Do it
        with self.store.connect() as db:
            db.execute("UPDATE agent_jobs SET outcome='set_aside'")
        self.assertNotIn(AGENT_DO_IT_NOTE, self.app.agent_work(self.sid, {'decision_id': 'click', 'suggestion_id': self.sid}))

    def test_a_tap_before_the_job_finished_or_a_run_prepared_ahead_is_not_either(self):
        self.job()
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('early',?,'accept','','dashboard','2026-10-23T09:00:00+00:00')", (self.sid,))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('late',?,'accept','','dashboard','2026-10-23T10:00:00+00:00')", (self.sid,))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('bot',?,'accept','','assistant','2026-10-23T10:00:00+00:00')", (self.sid,))
        work = lambda **job: self.app.agent_work(self.sid, {'suggestion_id': self.sid, **job})
        self.assertIn(AGENT_DO_IT_NOTE, work(decision_id='late'))
        self.assertNotIn(AGENT_DO_IT_NOTE, work(decision_id='early'))
        self.assertNotIn(AGENT_DO_IT_NOTE, work(decision_id='bot'))
        self.assertNotIn(AGENT_DO_IT_NOTE, work(decision_id='late', ahead=True))
        self.assertNotIn(AGENT_DO_IT_NOTE, work(decision_id='late', finish={'kind': 'finish'}))
        self.assertNotIn(AGENT_DO_IT_NOTE, self.app.agent_work(self.sid))

    def test_a_running_job_shows_its_progress(self):
        self.job(status='running', progress='Editing the German page')
        message = self.chat_turn()
        self.assertIn('Codex is still working on it', message)
        self.assertIn('Editing the German page', message)

    def test_the_review_status_carries_the_result(self):
        self.job()
        self.app.agents = agent_jobs.AgentJobs(self.store.connect, {'agents': {}}, Path(self.temp.name) / 'agent-jobs')
        snapshot = self.store.snapshot([])
        with self.store.connect() as db:
            self.app.agents.annotate(db, snapshot['suggestions'])
        snapshot.update(analyses=[], decisions=snapshot.get('decisions', []))
        card = next(s for s in a.compact_status(snapshot)['suggestions'] if s['id'] == self.sid)
        self.assertEqual((card['agent_work']['tool'], card['agent_work']['status'], card['agent_work']['result']), ('Codex', 'result', DONE))
        self.assertEqual(card['agent_work']['at'], '2026-10-23T09:45:00+00:00')
        self.assertIn('agent_work', a.review_prompt('run', ['work']))

    def test_no_jobs_add_nothing(self):
        self.assertEqual(self.app.agent_work(self.sid), '')
        self.assertNotIn('Claude Code or Codex on this card', self.chat_turn())


if __name__ == '__main__':
    unittest.main()

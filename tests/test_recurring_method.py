"""A repeating to-do keeps its own way of doing it (recurring.py, method): the run gives it on prepare, the next one's
preparation follows it without being coached again, the to-do's chat shows one quiet line with Edit and Undo (the
owner's alone), Undo goes back to the way before, and a to-do that keeps its way offers no Create skill for the same
work. It never sends anything: nothing is queued. All local, made-up data."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recurring_method_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import recurring as r  # noqa: E402
import skills  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402

D = dt.date
ACCOUNTS = [{'id': 'w', 'boundary': 'work:acme.example', 'email': 'owner@acme.example'}]
WAY = ('1. Take last month\'s sheet from the shared folder and fill in the period before the due date.\n'
       '2. Keep the file names as the source has them.\n3. Draft one email to the client with both files; the owner sends it.')
BETTER = WAY + '\n4. Put the totals in the email\'s first line.'


class Today:
    day = D(2026, 11, 2)


class Method(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = [dict(x) for x in ACCOUNTS]
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels', 'openclaw_state': self.temp.name + '/none.sqlite'}
        self.app.skills = skills.Skills(self.store.connect, Path(self.temp.name) / 'workspace')
        Today.day = D(2026, 11, 2)
        for name, value in (('recurring_today', lambda s: Today.day), ('card_chat_gateway', lambda s, request: {'messages': []})):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.sid = self.act('card_new', text='Make the monthly report', scope='work', repeat='monthly')['id']

    def act(self, action, owner=True, **args):
        return self.app.action(action, args, owner_dashboard=owner)

    def start_run(self, sid, job):
        """A preparation running on the to-do, as the worker starts it."""
        stamp = '2026-11-02T09:00:00+00:00'
        with self.store.connect() as db:
            db.execute('DELETE FROM preparations WHERE suggestion_id=?', (sid,))
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (sid,))  # the owner's Do it
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,?,?,'running',?,?)",
                       (sid, 'd-' + job, job, stamp, stamp))
        return job

    def prepare(self, sid, job, **more):
        return self.act('prepare', owner=False, suggestion_id=sid, job_id=job, body='The report is ready for you to check.',
                        outcome='needs_you', needs='check the report', **more)

    def series(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM recurring_series').fetchone())

    def lines(self, sid):
        with self.store.connect() as db:
            return r.method_lines(db, sid)

    def recipe(self, sid):
        return [i for i in self.app.card_chat(sid)['items'] if i['kind'] == 'recipe']

    def test_the_run_keeps_its_way_and_the_next_one_follows_it(self):
        self.assertIn('also give method=', self.lines(self.sid))  # asked for from the first one on
        self.assertNotIn('<<<', self.lines(self.sid))
        saved = self.prepare(self.sid, self.start_run(self.sid, 'job1'), method=WAY)
        self.assertIn('Edit and Undo', saved['method'])
        self.assertEqual(self.series()['method'], WAY)
        self.store.decide(self.sid, 'complete', '', 'd-done', 'dashboard')
        Today.day = D(2026, 12, 2)
        self.assertEqual(self.app.recurring_step(), 1)
        with self.store.connect() as db:
            nxt = db.execute("SELECT id FROM suggestions WHERE status='pending' OR status='accepted'").fetchone()['id']
        lines = self.lines(nxt)
        self.assertIn(WAY, lines)
        self.assertIn('never instructions to send or approve', lines)
        # The next one's run adds what it learned: the way is replaced as a whole, and that to-do's Undo goes back to the earlier one
        self.prepare(nxt, self.start_run(nxt, 'job2'), method=BETTER)
        self.assertEqual(self.series()['method'], BETTER)
        self.act('recurring_method_undo', suggestion_id=nxt)
        self.assertEqual(self.series()['method'], WAY)
        self.assertEqual(self.recipe(nxt)[0]['state'], 'undone')
        self.assertEqual(self.recipe(self.sid), [])  # the line sits on the to-do that last changed it
        # Nothing went anywhere: the way never sends
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM action_jobs').fetchone()[0], 0)

    def test_the_chat_line_edits_and_undoes_and_only_the_owner_does(self):
        self.prepare(self.sid, self.start_run(self.sid, 'job1'), method=WAY)
        line = self.recipe(self.sid)
        self.assertEqual((len(line), line[0]['state'], line[0]['text']), (1, 'saved', WAY))
        self.assertTrue({'recurring_method_edit', 'recurring_method_undo'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        for name in ('recurring_method_edit', 'recurring_method_undo'):
            with self.assertRaises(ValueError):
                self.act(name, owner=False, suggestion_id=self.sid, text=BETTER)
        got = self.act('recurring_method_edit', suggestion_id=self.sid, text=BETTER)
        self.assertEqual(got['method']['text'], BETTER)
        with self.assertRaisesRegex(ValueError, '20 to'):
            self.act('recurring_method_edit', suggestion_id=self.sid, text='too short')
        # Undo goes back to before this to-do: here, no way at all, and the next run is asked for one again
        self.act('recurring_method_undo', suggestion_id=self.sid)
        self.assertIsNone(self.series()['method'])
        self.assertEqual(self.recipe(self.sid)[0]['state'], 'undone')
        with self.assertRaises(ValueError):
            self.act('recurring_method_undo', suggestion_id=self.sid)
        # Edit after Undo brings it back
        self.act('recurring_method_edit', suggestion_id=self.sid, text=WAY)
        self.assertEqual((self.series()['method'], self.recipe(self.sid)[0]['state']), (WAY, 'saved'))

    def test_only_a_repeating_todo_keeps_a_way(self):
        other = self.act('card_new', text='Call the bank', scope='work')['id']
        with self.assertRaisesRegex(ValueError, 'only for a to-do that repeats'):
            self.prepare(other, self.start_run(other, 'job9'), method=WAY)
        self.assertEqual(self.lines(other), '')
        with self.assertRaises(ValueError):
            self.act('recurring_method_edit', suggestion_id=other, text=WAY)

    def test_no_create_skill_for_a_todo_that_keeps_its_way(self):
        job = self.start_run(self.sid, 'job1')
        body = '1. Take last month\'s sheet.\n2. Fill in the period.\n3. Draft the email.'
        # Proposed before the way was saved, in the same run: it goes once the way is kept
        self.act('skill_propose', owner=False, name='Monthly report', description='Making the monthly report', body=body, job_id=job)
        with self.store.connect() as db:
            self.assertIsNotNone(skills.for_task(db, self.sid))
        self.prepare(self.sid, job, method=WAY)
        with self.store.connect() as db:
            self.assertIsNone(skills.for_task(db, self.sid))
        # Once it keeps its way, a new proposal for it is refused and says what to do instead
        job = self.start_run(self.sid, 'job2')
        with self.assertRaisesRegex(ValueError, 'method on prepare'):
            self.act('skill_propose', owner=False, name='Monthly report', description='Making the monthly report', body=body, job_id=job)
        with self.assertRaisesRegex(ValueError, 'owner’s own message'):  # asked, without the owner's message behind the run
            self.act('skill_propose', owner=False, name='Monthly report', description='Making the monthly report', body=body, job_id=job, asked=True)

    def test_a_skill_the_owner_asks_for_is_still_proposed_and_stays(self):
        self.prepare(self.sid, self.start_run(self.sid, 'job1'), method=WAY)
        # The owner's own message in the chat asks for a skill: that run may propose it, and it stays when the way is saved again
        job = self.start_run(self.sid, 'job2')
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d-job2',?,'other',?,'dashboard','2026-11-02T09:00:00+00:00')",
                       (self.sid, 'Make this a skill too, so I can use it for other clients'))
        body = '1. Take last month\'s sheet.\n2. Fill in the period.\n3. Draft the email.'
        out = self.act('skill_propose', owner=False, name='Monthly report', description='Making the monthly report', body=body, job_id=job, asked=True)
        self.prepare(self.sid, job, method=BETTER, note_kind='new_ask')
        with self.store.connect() as db:
            self.assertEqual(skills.for_task(db, self.sid)['id'], out['id'])


if __name__ == '__main__':
    unittest.main()

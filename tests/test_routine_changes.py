"""A lasting change to a routine from the owner's note on one of its to-dos (routine_changes.py): the run on the note
reads the routine's words, offers new ones only when it judges the note lasting (routine_change on prepare), the to-do
shows what changes, and the routine takes them only on the owner's Change it (Edit's path), with a chat line. Kept as
is or stale (the routine edited since): nothing changes."""
import datetime as dt
import importlib.util
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('routine_changes_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import routine_changes  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS  # noqa: E402

T = dt.datetime
SESSION = 'agent:main:assistant-review-routine-'
WORDS = 'Check what shipped in the open source repo and draft a short post on X'
LASTING = 'Check what shipped in the open source repo and draft a short post on X. Never use emoji.'


class Diff(unittest.TestCase):
    def test_only_the_part_that_changes_shows(self):
        self.assertEqual(routine_changes.diff('Read the repo. Draft a post. Keep it short.', 'Read the repo. Draft a post with a link. Keep it short.'),
                         {'old': 'Draft a post.', 'new': 'Draft a post with a link.'})
        self.assertEqual(routine_changes.diff(WORDS, LASTING), {'old': '', 'new': 'Never use emoji.'})
        self.assertEqual(routine_changes.diff(LASTING, WORDS), {'old': 'Never use emoji.', 'new': ''})
        self.assertLessEqual(len(routine_changes.diff('A.', 'B ' * 400)['new']), routine_changes.PART_MAX)


class Changes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'w', 'boundary': 'work:acme.example'}], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.store.accounts = self.app.config['accounts']  # as the App sets it (machine/main.py)
        self.now = T(2026, 11, 9, 6, 0)
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.gateway(request)),
                            ('routine_spawn', lambda s, target, run_id: target(run_id)),
                            ('card_chat_gateway', lambda s, request: {'messages': []})):  # the run's own words: none here
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.answer = {'start': {'status': 'admitted'}, 'status': {'status': 'pending'}}
        self.rid = self.act('routine_new', words='every day at 9, ' + WORDS)['made']
        self.act('routine_run_now', id=self.rid); self.app.routines_step()
        with self.store.connect() as db:
            run = db.execute('SELECT id FROM routine_runs ORDER BY started_at DESC').fetchone()['id']
        self.app.action('routine_result', {'_routine_session': SESSION + run, 'text': 'Would post on X: Search got faster.',
                                           'name': 'Check what shipped', 'draft': {'title': 'Post on X about the faster search', 'text': 'Search got faster 🚀'}},
                        owner_dashboard=False)
        self.answer['status'] = {'status': 'ok'}; self.app.routines_step()
        with self.store.connect() as db:
            self.sid = db.execute('SELECT id FROM suggestions').fetchone()['id']

    def gateway(self, request):
        return self.answer.get(request['action'], {'status': 'unavailable'})

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def note(self, text, decision='d1'):
        """The owner's Ask for changes on the to-do: a run on it, as the worker starts it."""
        self.store.decide(self.sid, 'other', text, decision, 'dashboard')
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone())

    def offer(self, job, words=LASTING):
        with self.store.connect() as db:
            routine_changes.offer(db, self.sid, routine_changes.check(db, self.sid, job['job_id'], words))

    def routine(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM routines WHERE id=?', (self.rid,)).fetchone())

    def view(self):
        with self.store.connect() as db:
            card = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
            self.store.card_views(db, [card])
            return card

    def test_the_run_on_a_note_reads_the_routine_and_offers_only_a_lasting_change(self):
        job = self.note('No emoji, ever.')
        lines = self.app.routine_change_lines({**job, 'ahead': False}, '')
        for said in ('draft from the owner\'s routine "Check what shipped"', WORDS, 'Judge by what the note means',
                     'routine_change=<the routine\'s whole instructions', 'leaves routine_change out', 'never says the routine changed'):
            self.assertIn(said, lines)
        self.assertEqual(self.app.routine_change_lines({**job, 'ahead': True}, ''), '')  # prepared ahead: no note
        with self.store.connect() as db:
            self.assertIsNone(routine_changes.check(db, self.sid, job['job_id'], WORDS))  # its words already: no offer
            with self.assertRaisesRegex(ValueError, 'only for a to-do from a routine'):
                routine_changes.check(db, self.sid, 'another-job', LASTING)
            with self.assertRaisesRegex(ValueError, 'at most'):
                routine_changes.check(db, self.sid, job['job_id'], 'x' * 3000)
        self.assertNotIn('routine_change', self.view())  # a one-off note: the to-do works as before
        self.offer(job)
        change = self.view()['routine_change']
        at = change.pop('at')  # when the run on the note made it (ms): the chat shows it under that run's reply
        self.assertEqual(change, {'name': 'Check what shipped', 'old': '', 'new': 'Never use emoji.'})
        self.assertLess(abs(at - time.time() * 1000), 60000)
        self.assertEqual(self.routine()['instructions'], WORDS)  # offered, not saved

    def test_the_runs_prepare_with_routine_change_offers_it(self):
        job = self.note('No emoji, ever.')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running' WHERE job_id=?", (job['job_id'],))
        with self.assertRaisesRegex(ValueError, 'routine_change is the routine'):
            self.act('prepare', owner=False, suggestion_id=self.sid, job_id=job['job_id'], body='Redid the post.', outcome='needs_you',
                     needs='check the draft and send it', note_kind='style', routine_change=['no'])
        self.assertNotIn('routine_change', self.view())
        self.act('prepare', owner=False, suggestion_id=self.sid, job_id=job['job_id'], body='Redid the post without emoji.', outcome='needs_you',
                 needs='check the draft and send it', note_kind='style', routine_change=LASTING)
        self.assertEqual(self.view()['routine_change']['new'], 'Never use emoji.')

    def test_change_it_saves_through_edit_and_says_so_in_the_chat(self):
        self.offer(self.note('No emoji, ever.'))
        self.assertTrue({'routine_change_save', 'routine_change_keep'} <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            self.act('routine_change_save', owner=False, suggestion_id=self.sid)
        version = self.routine()['version']
        self.assertEqual(self.act('routine_change_save', suggestion_id=self.sid)['line'], 'Changed the routine Check what shipped')
        mine = self.routine()
        self.assertEqual((mine['instructions'], mine['version'], mine['name']), (LASTING, version + 1, 'Check what shipped'))
        self.assertNotIn('routine_change', self.view())
        lines = [i['text'] for i in self.app.card_chat(self.sid)['items'] if i['kind'] == 'event']
        self.assertIn('Changed the routine Check what shipped', lines)
        self.assertFalse(any(x.startswith('You') for x in lines))
        with self.assertRaisesRegex(ValueError, 'changed in the meantime'):  # once
            self.act('routine_change_save', suggestion_id=self.sid)

    def test_keep_it_as_is_or_an_edit_since_changes_nothing(self):
        self.offer(self.note('No emoji, ever.'))
        self.act('routine_change_keep', suggestion_id=self.sid)
        self.assertNotIn('routine_change', self.view())
        self.assertEqual(self.routine()['instructions'], WORDS)
        self.offer(self.note('Shorter, always.', 'd2'), WORDS + ' Keep it under 200 characters.')
        self.assertIn('routine_change', self.view())
        self.act('routine_edit', id=self.rid, words='Check what shipped and draft a post on LinkedIn.')
        self.assertNotIn('routine_change', self.view())  # made on older words: not shown
        with self.assertRaisesRegex(ValueError, 'changed in the meantime'):
            self.act('routine_change_save', suggestion_id=self.sid)
        self.assertEqual(self.routine()['instructions'], 'Check what shipped and draft a post on LinkedIn.')


if __name__ == '__main__':
    unittest.main()

"""A folder's daily overview (folder_overview.py, NotesApp.folder_overview_step): a summary and a few bullets at the top
of a note with notes under it, every sentence naming the notes it stands on, read from what those notes say now (their
written pages and newest lines). Daily at most, only when they changed, quality or nothing. Made-up data only; the
model is a stand-in, nothing is sent."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import folder_overview  # noqa: E402
import machine.main as machine_main
import note_pages  # noqa: E402
import note_writer  # noqa: E402
from pinned import pinned  # noqa: E402

AT = '2026-11-14T10:00:00+00:00'


class Overviews(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': []}
        self.app.folder_overview_model = self.model
        self.app.background_pause = lambda **_: None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.asked, self.answer = [], None
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def model(self, prompt):
        self.asked.append(prompt)
        folders = json.loads(prompt.split('Folders:\n', 1)[1])
        return json.dumps({'folders': [self.answer(f) for f in folders]}) if callable(self.answer) else self.answer

    def notes(self, hire_day='2026-11-10'):
        """Work with two notes The Machine keeps under it: an office move with a written page, a hire with fresh lines."""
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'topic', [
                {'key': 'move', 'title': 'Office move', 'area': 'personal', 'under': ['Work'],
                 'lines': [{'key': 'm1', 'text': 'Office move: the date', 'at': '2026-11-12'}, {'key': 'm0', 'text': 'Office move: old options', 'at': '2026-08-01'}]},
                {'key': 'hire', 'title': 'Hiring a designer', 'area': 'personal', 'under': ['Work'],
                 'lines': [{'key': 'h1', 'text': 'Two designer profiles', 'at': hire_day}]}], AT)
            ids = {r['key']: r['id'] for r in db.execute('SELECT id,key FROM note_pages')}
            line = db.execute("SELECT id FROM note_page_lines WHERE key='m1'").fetchone()['id']
            note_writer.save(db, {'note_id': ids['topic:move'], 'basis': 'x'},
                             {'summary': {'text': 'The movers come on Saturday 21 November; the lease is signed.', 'sources': [line]},
                              'open': [{'text': 'Confirm the loading dock with the landlord.', 'sources': [line]}]}, AT)
        return ids['folder:work'], ids['topic:move'], ids['topic:hire']

    def written(self, move, hire):
        return lambda f: {'folder': f['folder'],
                          'summary': {'text': 'The office move is set for Saturday 21 November; two designer profiles wait for your pick.', 'sources': [f'N{move}', f'N{hire}']},
                          'now': [{'text': 'Confirm the loading dock with the landlord before Saturday, 8:00–10:00.', 'sources': [f'N{move}']},
                                  {'text': 'Pick one of the two designer profiles.', 'sources': [f'N{hire}']},
                                  {'text': 'A bullet with nothing behind it.', 'sources': ['N999']},
                                  {'text': 'The office move is set for Saturday 21 November.', 'sources': [f'N{move}']}]}

    def step(self):
        self.app.folder_overview_next = 0
        started = self.app.folder_overview_step()
        if started:
            self.app.folder_overview_thread.join(10)
        return started

    def test_a_folder_gets_an_overview_naming_the_notes_it_stands_on(self):
        work, move, hire = self.notes()
        self.answer = self.written(move, hire)
        self.assertTrue(self.step())
        prompt = self.asked[0]
        for said in ('The movers come on Saturday 21 November', 'Confirm the loading dock', 'Two designer profiles', 'Hiring a designer'):
            self.assertIn(said, prompt, 'it reads what the notes under it say')
        self.assertNotIn('old options', prompt, 'a line older than RECENT_DAYS is not news')
        page = self.app.note_page(note_pages.node_id(work))['overview']
        self.assertEqual([s['name'] for s in page['summary']['sources']], ['Office move', 'Hiring a designer'])
        self.assertEqual([s['id'] for s in page['summary']['sources']], [note_pages.node_id(move), note_pages.node_id(hire)])
        self.assertEqual([b['text'] for b in page['now']], ['Confirm the loading dock with the landlord before Saturday, 8:00 to 10:00.', 'Pick one of the two designer profiles.'],
                         'uncited and repeated sentences go; a range reads "to", not a dash')
        with self.store.connect() as db:
            about = {x['id']: x.get('about') for x in self.app.notes_list(db)}
        self.assertTrue(about[note_pages.node_id(work)].startswith('The office move is set'))
        self.assertFalse(self.step(), 'nothing changed: no second call')
        self.assertEqual(len(self.asked), 1)

    def test_one_note_with_news_is_no_overview_and_no_call(self):
        self.notes(hire_day='2026-09-01')  # the hire's line is old: only the move says something now
        self.assertFalse(self.step())
        self.assertEqual(self.asked, [])

    def test_a_changed_note_brings_a_rewrite_from_the_current_overview_once_a_day(self):
        work, move, hire = self.notes()
        self.answer = self.written(move, hire)
        self.step()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(hire), 'Ana sent a third profile', '2026-11-14')
        self.assertFalse(self.step(), 'at most once a FOLDER_HOURS')
        with mock.patch.object(folder_overview, 'FOLDER_HOURS', 0):
            self.assertTrue(self.step())
        self.assertIn('"current_overview"', self.asked[1])
        self.assertIn('Ana sent a third profile', self.asked[1])

    def test_a_removed_note_takes_what_stood_only_on_it(self):
        work, move, hire = self.notes()
        self.answer = self.written(move, hire)
        self.step()
        with self.store.connect() as db:
            db.execute('UPDATE note_pages SET removed_at=? WHERE id=?', (AT, hire))
            page = folder_overview.view(db, work)
        self.assertEqual([s['name'] for s in page['summary']['sources']], ['Office move'])
        self.assertEqual([b['text'] for b in page['now']], ['Confirm the loading dock with the landlord before Saturday, 8:00 to 10:00.'])

    def test_nothing_current_means_no_overview_and_a_quiet_folder_loses_its_own_without_a_call(self):
        work, move, hire = self.notes()
        self.answer = lambda f: {'folder': f['folder'], 'summary': {'text': '', 'sources': []}}
        self.step()
        with self.store.connect() as db:
            self.assertIsNone(folder_overview.view(db, work))
        self.answer = self.written(move, hire)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(hire), 'Ana sent a third profile', '2026-11-14')
        with mock.patch.object(folder_overview, 'FOLDER_HOURS', 0):
            self.step()
        with self.store.connect() as db:
            self.assertTrue(folder_overview.view(db, work))
        asked = len(self.asked)
        later = dt.datetime(2026, 12, 20, 10, tzinfo=dt.timezone.utc)  # a month on: no news, the move's page alone
        with pinned(later.isoformat()), mock.patch.object(folder_overview, 'FOLDER_HOURS', 0), self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_writer.save(db, {'note_id': move, 'basis': 'y'}, None, later.isoformat())
        with pinned(later.isoformat()), mock.patch.object(folder_overview, 'FOLDER_HOURS', 0):
            self.step()
            with self.store.connect() as db:
                self.assertIsNone(folder_overview.view(db, work))
        self.assertEqual(len(self.asked), asked, 'a quiet folder: no call')

    def test_an_answer_that_isnt_one_keeps_the_overview_and_waits(self):
        work, move, hire = self.notes()
        self.answer = self.written(move, hire)
        self.step()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.line_add(db, note_pages.node_id(hire), 'Ana sent a third profile', '2026-11-14')
        self.answer = 'Sorry, I cannot help with that.'
        with mock.patch.object(folder_overview, 'FOLDER_HOURS', 0):
            self.step()
        self.assertIn('overview', self.app.note_page(note_pages.node_id(work)))
        self.assertFalse(self.step(), 'it tried: it waits FOLDER_HOURS')

    def test_the_day_cap_holds(self):
        self.notes()
        with mock.patch.object(folder_overview, 'DAY_CAP', 0), self.store.connect() as db:
            self.assertEqual(folder_overview.due(db), [])


if __name__ == '__main__':
    unittest.main()

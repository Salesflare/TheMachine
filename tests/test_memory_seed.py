"""Notes from an OpenClaw workspace's memory topic pages, once (memory_seed.py, NotesApp.memory_seed_step): which pages
are read, that they are only ever read, each fact a line saying its page and date, in the note that covers it or a new
one, then never again. Made-up workspace and data only; the model is a stand-in, nothing is sent."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import machine.main as machine_main
import memory_seed  # noqa: E402
import note_pages  # noqa: E402
import note_writer  # noqa: E402
from pinned import pinned  # noqa: E402

AT = '2026-11-14T10:00:00+00:00'
TRIP = '''# Lisbon, May 2026

- Flight out on 2026-05-01, back on 2026-05-05.
- Hotel Example Garden in Alfama, three nights.

```bash
curl https://example.com/secret
```
<!-- api_key: sk-abcdefghijklmnop -->
'''


class Seed(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.ws = Path(temp.name) / 'workspace'
        self.page('memory/trips/lisbon.md', TRIP)
        self.page('memory/home/boiler.md', '# Boiler\n\nThe boiler is a Example Therm 24, serviced each October by Northside Heating since 2024.\n')
        self.page('memory/2026-10-11.md', 'A daily log: debugging the standup cron, which timed out again this morning.\n' * 2)
        self.page('memory/daily/notes.md', 'A daily log in the daily folder, about nothing that lasts at all here.\n' * 2)
        self.page('memory/home/README.md', 'What this folder holds, and how it is organized for the assistant to find.\n' * 2)
        self.page('memory/plans/backup-plan-2026-10-04.md', 'A dated plan for the assistant to change how backups are made.\n' * 2)
        self.page('memory/notes/archive/Sensitive/thing.md', 'Something the owner set apart as sensitive, never to be read here.\n' * 2)
        self.page('AGENTS.md', 'The assistant\'s own rules, outside memory: never read by the seed at all.\n' * 2)
        for n in range(memory_seed.BULK + 1):
            self.page(f'memory/meetings/meeting-{n}.md', 'An imported meeting note from a big export of meeting notes, one of many.\n')
        outside = Path(temp.name) / 'outside.md'
        outside.write_text('Outside the workspace: a link from memory/ to here is never followed by the seed.\n' * 2)
        os.symlink(outside, self.ws / 'memory/home/linked.md')
        self.store = machine_main.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': []}
        self.app.bring_in_dir = self.ws
        self.app.memory_seed_model = self.model
        self.app.background_pause = lambda **_: None
        self.app.background_spaced = lambda: True
        self.app.background_started = lambda: None
        self.asked, self.answer = [], None
        pin = pinned(AT)
        pin.__enter__()
        self.addCleanup(pin.__exit__, None, None, None)

    def page(self, rel, text):
        path = self.ws / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def model(self, prompt):
        self.asked.append(prompt)
        return json.dumps(self.answer(prompt)) if callable(self.answer) else self.answer

    def files(self, prompt):
        """{file: P id} of the pages in a prompt."""
        body = prompt.split('<<<\n', 1)[1].split('\n>>>', 1)[0]
        return {json.loads(x)['file']: json.loads(x)['page'] for x in body.splitlines()}

    def step(self):
        self.app.memory_seed_next = 0
        started = self.app.memory_seed_step()
        if started:
            self.app.memory_seed_thread.join(10)
        return started

    def lines(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute("SELECT l.*,p.title note,p.kind FROM note_page_lines l JOIN note_pages p ON p.id=l.note_id WHERE l.by='memory' ORDER BY l.id")]

    def test_only_topic_pages_are_read_and_nothing_is_written(self):
        before = {p: p.stat().st_mtime_ns for p in self.ws.rglob('*') if p.is_file()}
        self.answer = lambda prompt: {'pages': []}
        self.assertTrue(self.step())
        files = self.files(self.asked[0])
        self.assertEqual(sorted(files), ['memory/home/boiler.md', 'memory/trips/lisbon.md'],
                         'not a daily log, a dated page, a README, a bulk export, a sensitive folder, a link out or anything outside memory/')
        self.assertNotIn('sk-abcdefghijklmnop', self.asked[0])
        self.assertNotIn('curl', self.asked[0], 'code and comments never reach a model')
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in self.ws.rglob('*') if p.is_file()}, 'only ever read')

    def test_facts_become_lines_with_their_page_and_date_in_the_note_that_covers_them_or_a_new_one(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'home', [{'key': 'repairs', 'title': 'Repairs and upkeep', 'under': ['Home'], 'lines': []}], AT)
            repairs = db.execute("SELECT id FROM note_pages WHERE key='home:repairs'").fetchone()['id']

        def answer(prompt):
            f = self.files(prompt)
            return {'pages': [{'page': f['memory/home/boiler.md'], 'place': f'N{repairs}', 'facts': [
                                   {'text': 'The boiler is an Example Therm 24.'},
                                   {'text': 'Northside Heating services the boiler each October.', 'date': '2024-10-01'},
                                   {'text': 'Call https://example.com about it.'}, {'text': 'Too short'},
                                   {'text': 'The boiler is an Example Therm 24 model.'}]},
                              {'page': f['memory/trips/lisbon.md'], 'new': {'title': 'Lisbon', 'under': 'Trips', 'area': 'personal'}, 'facts': [
                                   {'text': 'You flew to Lisbon on 1 May and back on 5 May.', 'date': '2026-05-01'},
                                   {'text': 'You stayed three nights at Hotel Example Garden in Alfama.'}]}]}
        self.answer = answer
        self.step()
        got = self.lines()
        self.assertEqual([(x['note'], x['text']) for x in got], [
            ('Repairs and upkeep', 'The boiler is an Example Therm 24.'),
            ('Repairs and upkeep', 'Northside Heating services the boiler each October.'),
            ('Lisbon', 'You flew to Lisbon on 1 May and back on 5 May.'),
            ('Lisbon', 'You stayed three nights at Hotel Example Garden in Alfama.')], 'a link, too few words or saying it again is no fact')
        self.assertIn('"path": "Home > Repairs and upkeep"', self.asked[0])
        self.assertNotIn('"path": "Home"}', self.asked[0], 'a folder is no place for a page: its subject gets a note in it')
        self.assertEqual({(json.loads(x['data'])['memory'], json.loads(x['data'])['page']) for x in got},
                         {('memory/home/boiler.md', 'Boiler'), ('memory/trips/lisbon.md', 'Lisbon, May 2026')}, 'the path, and the page by its first heading')
        self.assertEqual([x['at'][:10] for x in got[1:]], ['2024-10-01', '2026-05-01', '2026-05-05'],
                         "a fact's own date, or else its page's: the newest day the page names")
        with self.store.connect() as db:
            path = [p['name'] for p in note_pages.page(db, got[2]['note_id'])['path']]
            self.assertEqual(path[-1], 'Trips')
            self.assertIn(got[2]['note_id'], note_writer.candidates(db), 'the page writer writes a page from them')
            item = {'note_id': got[2]['note_id'], 'basis': 'x'}
            self.assertIn("the owner's earlier notes", json.dumps(note_writer.evidence(db, item)))
            db.execute('BEGIN IMMEDIATE')
            note_pages.sync(db, 'home', [{'key': 'repairs', 'title': 'Repairs and upkeep', 'under': ['Home'], 'lines': []}], AT)
        self.assertEqual(len(self.lines()), 4, "a kind's own sync never takes them")
        with self.store.connect() as db:
            self.assertEqual(memory_seed.due(db, self.ws), [], 'every page read: done')
            self.assertTrue(memory_seed.done(db))
        self.page('memory/home/garden.md', '# Garden\n\nThe garden is mowed by Example Gardens every second Friday from April.\n')
        self.assertFalse(self.step(), 'once: a page added later is not read')

    def test_a_removed_line_never_comes_back(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            note_id = note_pages.sync(db, 'memory', [{'key': 'trips/lisbon', 'title': 'Lisbon', 'under': ['Trips'], 'lines': []}], AT)[0]
            first = note_pages.add_kept(db, note_id, [{'key': 'k1', 'text': 'You stayed three nights in Alfama.', 'data': {'memory': 'memory/trips/lisbon.md'}}], 'memory', AT)
            note_pages.line_remove(db, first[0], AT)
            self.assertEqual(note_pages.add_kept(db, note_id, [{'key': 'k1', 'text': 'You stayed three nights in Alfama.'}], 'memory', AT), [])

    def test_a_page_is_called_by_its_heading_or_its_name_in_words_never_its_path(self):
        self.assertEqual(memory_seed.title('# **Kids** — activities\n\nText', 'memory/kids/a.md'), 'Kids, activities')
        self.assertEqual(memory_seed.title('```\n# not a heading\n```\nNo heading here.', 'memory/people/helena-activities.md'), 'Helena activities')

    def test_an_answer_that_stops_before_closing_its_list_still_counts(self):
        batch = [{'rel': 'memory/home/boiler.md'}]
        found = memory_seed.parse('{"pages":[{"page":"P1","place":"N1","facts":[{"text":"The boiler is an Example Therm 24."}]}', batch, [{'id': 'N1'}])
        self.assertEqual(found['memory/home/boiler.md']['facts'], [{'text': 'The boiler is an Example Therm 24.', 'date': None}])

    def test_an_answer_that_isnt_one_tries_again_then_lets_the_page_be(self):
        self.answer = 'Sorry, I cannot help with that.'
        for _ in range(memory_seed.TRIES):
            self.assertTrue(self.step())
        self.assertFalse(self.step())
        self.assertEqual(len(self.asked), memory_seed.TRIES)
        self.assertEqual(self.lines(), [])

    def test_a_page_about_the_assistant_or_with_nothing_lasting_brings_nothing(self):
        self.answer = lambda prompt: {'pages': [{'page': p, 'facts': []} for p in self.files(prompt).values()]}
        self.step()
        self.assertEqual(self.lines(), [])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM note_pages WHERE kind='memory'").fetchone()[0], 0, 'no empty note')
        self.assertIn('about the assistant itself', self.asked[0])

    def test_no_workspace_no_seed(self):
        self.app.bring_in_dir = self.ws / 'nowhere'
        self.assertFalse(self.step())
        with mock.patch.object(memory_seed, 'PER_PASS', 1), self.store.connect() as db:
            self.assertTrue(memory_seed.done(db))


if __name__ == '__main__':
    unittest.main()

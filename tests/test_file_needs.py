"""How often a preparation links to a file other than a Google Doc and how often one it needs is missing (file_needs.py):
once per job, by kind, from the links and the run's own file_missing; once a day the finished days go with the error
reports, as numbers only, and nothing while Send error reports is off or this isn't open yet (OPEN). The Network is a
stand-in here."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import error_feed
import file_needs
import timeutil
from assistant import App, Store

DRIVE = 'https://drive.google.com/file/d/1AbCdEfGhIjKlMnOp/view?usp=sharing'
DOCS = 'https://docs.google.com/'
CLOSED = not file_needs.OPEN


class Kinds(unittest.TestCase):
    def test_a_links_kind_comes_from_its_address(self):
        for url, kind in ((DOCS + 'spreadsheets/d/1Ab/edit#gid=0', 'sheet'), (DOCS + 'spreadsheets/u/1/d/1Ab/edit', 'sheet'),
                          (DOCS + 'presentation/d/1Ab/edit', 'slides'), (DOCS + 'document/d/1Ab/edit', None),
                          (DOCS + 'document/d/1Ab/edit?rtpof=true&sd=true', 'drive'), (DOCS + 'spreadsheets/d/1Ab/edit?rtpof=true', 'drive'),
                          (DOCS + 'forms/d/1Ab/viewform', None), (DRIVE, 'drive'), ('https://drive.google.com/drive/folders/1Ab', None),
                          ('https://drive.google.com/open?id=1Ab', 'drive'), ('https://acme.example/Offer.PDF?x=1', 'pdf'),
                          ('https://acme.sharepoint.com/:w:/s/team/Ab', 'cloud'), ('https://1drv.ms/w/s!Ab', 'cloud'),
                          ('https://www.dropbox.com/scl/fi/ab/x.docx', 'cloud'), ('https://www.dropbox.com/pricing', None),
                          ('https://evildropbox.com/s/ab', None), ('https://we.tl/t-Ab', 'cloud'), ('https://acme.example/page', None),
                          ('https://[bad', None)):
            self.assertEqual(file_needs.kind(url), kind, url)

    def test_a_drive_link_is_a_pdf_when_its_name_says_so_and_one_text_can_have_several(self):
        self.assertEqual(file_needs.links(f'Offer.pdf <{DRIVE}>'), {'pdf'})
        self.assertEqual(file_needs.links(f'Offer.pdf\n\nNotes {DRIVE}.'), {'drive'})
        self.assertEqual(file_needs.links(f'[x]({DOCS}spreadsheets/d/1Ab/edit), {DOCS}presentation/d/1Cd/edit.'), {'sheet', 'slides'})
        self.assertEqual(file_needs.links(None), set())


class Counted(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(setattr, timeutil, 'PINNED', timeutil.PINNED)
        self.addCleanup(setattr, file_needs, 'OPEN', file_needs.OPEN)
        file_needs.OPEN = True
        self.at(24)
        self.store = Store(Path(self.temp.name) / 'assistant.db')
        self.app = App.__new__(App)
        self.app.store = self.store
        self.sent = []

    def at(self, day, hour=10):
        timeutil.PINNED = dt.datetime(2026, 11, day, hour, tzinfo=dt.timezone.utc)

    def todo(self, body, sid='todo-1'):
        with self.store.connect() as db:
            event = db.execute("INSERT INTO events(source_id,account_id,occurred_at,ingested_at,kind,title,body,metadata,content_hash) "
                               "VALUES(?,'mail','2026-11-20T09:00:00Z','2026-11-20T09:00:00Z','gmail.message','x',?,'{}','h')", (sid, body)).lastrowid
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES(?,?,'t','b',?,'[\"mail\"]','2026-11-20T09:00:00Z')",
                       (sid, sid, json.dumps([event])))

    def note(self, sid='todo-1', job='j1', **args):
        self.app.file_needs_note({'suggestion_id': sid, 'job_id': job, **args})

    def call(self, method, path, body):
        self.sent.append((method, path, body))
        return {'ok': True}

    def send(self):
        return file_needs.send(self.store.connect, self.call)

    def test_numbers_by_kind_once_a_job_and_nothing_else_leaves(self):
        self.todo(f'Please fill in {DOCS}spreadsheets/d/1SecretSheet/edit and Plan.pdf {DRIVE}')
        self.todo('Nothing linked here', 'todo-2')
        with self.store.connect() as db:  # what the owner pasted in the chat counts; a source's message there doesn't
            for n, source in ((1, 'dashboard'), (2, 'email')):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,source,feedback,created_at) VALUES(?,?,'other',?,?,'2026-11-21T09:00:00Z')",
                           (f'd{n}', 'todo-2', source, 'see ' + (DOCS + 'presentation/d/1Cd/edit' if n == 1 else 'https://we.tl/t-Ab')))
        self.note(file_missing='sheet')
        self.note(file_missing='sheet')  # the same run saving again
        self.note('todo-2', 'j2')
        self.note('todo-2', 'j3', file_missing='the contract from Pat')  # its words never travel
        self.note('todo-2', None)  # no run
        self.assertEqual(self.send(), 0)  # today isn't finished
        self.at(25)
        self.assertEqual(self.send(), 1)
        self.assertEqual(self.sent, [('POST', '/errors', {'action': 'file_needs', 'day': '2026-11-24', 'runs': 3,
                                                          'linked': {'sheet': 1, 'pdf': 1, 'slides': 2}, 'missing': {'sheet': 1, 'other': 1}})])
        for word in ('1SecretSheet', 'Plan', 'Pat', 'todo', 'j1', 'http'):
            self.assertNotIn(word, json.dumps(self.sent[0][2]))
        self.at(25, 20)
        self.assertEqual(self.send(), 0)  # sent once
        with self.store.connect() as db:
            self.assertNotIn('contract', json.dumps([tuple(r) for r in db.execute('SELECT * FROM file_need_runs')]))

    def test_a_day_that_could_not_go_goes_later_and_old_ones_are_dropped(self):
        self.todo('x')
        self.note()
        self.at(25)
        self.assertEqual(file_needs.send(self.store.connect, lambda *a: {'error': 'unknown'}), 0)  # an older control plane
        self.assertEqual(self.send(), 0)  # tried just now
        self.at(25, 18)
        self.assertEqual(self.send(), 1)
        timeutil.PINNED = dt.datetime(2026, 12, 30, tzinfo=dt.timezone.utc)
        self.send()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM file_need_runs').fetchone()[0], 0)

    def test_off_counts_and_sends_nothing(self):
        self.todo(f'{DOCS}spreadsheets/d/1Ab/edit')
        self.note()
        with self.store.connect() as db:
            error_feed.set_on(db, False)
        self.note(job='j2')
        self.at(25)
        self.assertEqual(self.send(), 0)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM file_need_runs').fetchone()[0], 0)
        self.assertEqual(self.sent, [])

    def test_until_it_is_open_nothing_is_asked_counted_or_sent(self):
        from machine.app.preparation import preparation_prompt
        self.todo(f'{DOCS}spreadsheets/d/1Ab/edit')
        self.note()
        file_needs.OPEN = False
        self.assertNotIn('file_missing', preparation_prompt({'job_id': 'j' * 12, 'suggestion_id': 'todo-1'}))
        self.note(job='j2')
        self.at(25)
        self.assertEqual((self.send(), self.sent), (0, []))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM file_need_runs').fetchone()[0], 0)

    def test_it_opens_only_with_the_help_and_the_setting_saying_so(self):
        if not CLOSED:
            root = Path(file_needs.__file__).parent
            self.assertIn('## Linked files', (root / 'docs/help/error-reports.md').read_text())
            self.assertIn('linked files', (root / 'dashboard/settings-panels.html').read_text())

    def test_a_count_that_fails_never_holds_up_the_save(self):
        self.app.file_needs_note({})

    def test_the_run_is_asked_for_it_in_its_own_save_and_both_ways_count(self):
        from machine.app.preparation import preparation_prompt
        prompt = preparation_prompt({'job_id': 'j' * 12, 'suggestion_id': 'todo-1'})
        self.assertIn('file_missing:<' + 'doc, sheet, slides, pdf, word or other>', prompt)
        self.assertEqual(file_needs.MISSING, ('doc', 'sheet', 'slides', 'pdf', 'word', 'other'))
        calls = []
        self.app.file_needs_note = lambda args: calls.append(args.get('file_missing'))
        self.app.slack_blocker_check = lambda args: False
        self.app.learned_used = lambda *a: None
        self.store.preparation_blocked = lambda *a: {'status': 'blocked'}
        self.app.preparation_blocked_action('preparation_blocked', {'suggestion_id': 'todo-1', 'job_id': 'j1', 'reason': 'x', 'file_missing': 'pdf'})
        self.assertEqual(calls, ['pdf'])


if __name__ == '__main__':
    unittest.main()

"""A Google Sheet or Slides file linked in a to-do (google_files.py): read by its link with spreadsheets.readonly and
presentations.readonly, the linked tab first, at most so many cells, and a plain answer for what can't be read. Google,
gog and the broker are faked: nothing goes out."""
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse

from connectors import docs
import google_files
import mail_grants
import sources
import test_connector_docs as t
import test_google_docs_hosted as hosted
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors

SHEET, DECK, DOC = 's' * 44, 'p' * 44, 'd' * 44
SHEET_LINK = f'https://docs.google.com/spreadsheets/d/{SHEET}/edit?gid=7#gid=7&range=B2:C3'
DECK_LINK = f'https://docs.google.com/presentation/u/1/d/{DECK}/edit#slide=id.p4'


def tab(title, gid, rows=100, cols=5, **more):
    return {'properties': {'sheetId': gid, 'title': title, 'gridProperties': {'rowCount': rows, 'columnCount': cols}, **more}}


def run(text):
    return {'text': {'textElements': [{'paragraphMarker': {}}, {'textRun': {'content': text + '\n'}}]}}


class FilesFake(t.GoogleFake):
    """Google Sheets and Slides, faked: each tab's cells, and the status a file answers with instead."""

    def __init__(self, test):
        super().__init__(test)
        self.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, *google_files.SCOPE.values()}
        self.tabs = [tab('Summary', 0), tab('It’s Q4', 7), tab('Raw', 9, hidden=True), {'properties': {'sheetId': 11, 'title': 'Chart', 'sheetType': 'OBJECT'}}]
        self.cells = {'Summary': [['Total', '1,200'], ['', ''], ['Left', '3']], 'It’s Q4': [['Week', 'Plan'], ['1', 'Launch, then rest']], 'Raw': [['secret', '1']]}
        self.slides = [{'pageElements': [{'shape': run('Plan for Q4')}, {'image': {}}, {'elementGroup': {'children': [{'shape': run('In a group')}]}}],
                        'slideProperties': {'notesPage': {'notesProperties': {'speakerNotesObjectId': 'n1'},
                                                          'pageElements': [{'objectId': 'n0', 'shape': run('9')}, {'objectId': 'n1', 'shape': run('Say hello first')}]}}},
                       {'slideProperties': {'isSkipped': True}, 'pageElements': [{'table': {'tableRows': [{'tableCells': [run('Who'), run('What')]}]}}]},
                       {}]
        self.refuse, self.ranges = None, []

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        if url.netloc not in ('sheets.googleapis.com', 'slides.googleapis.com'):
            return super().respond(request, data, timeout)
        self.test.assertEqual(request.get_method(), 'GET')
        query = dict(urllib.parse.parse_qsl(url.query))
        self.requests.append(('GET', urllib.parse.unquote(url.path), query))
        if self.refuse:
            status, body = self.refuse
            raise urllib.error.HTTPError(request.full_url, status, 'no', {}, io.BytesIO(json.dumps(body).encode()))
        if '/values/' in url.path:
            self.test.assertEqual(query['valueRenderOption'], 'FORMATTED_VALUE')
            asked = urllib.parse.unquote(url.path.split('/values/')[1])
            self.ranges.append(asked)
            return t.Response(json.dumps({'values': self.cells.get(asked.rpartition('!')[0].strip("'").replace("''", "'"), [])}).encode())
        if url.path == f'/v4/spreadsheets/{SHEET}':
            return t.Response(json.dumps({'properties': {'title': 'Budget'}, 'sheets': self.tabs}).encode())
        self.test.assertEqual(url.path, f'/v1/presentations/{DECK}')
        return t.Response(json.dumps({'title': 'Q4 deck', 'slides': self.slides}).encode())


class Base(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.config = {**hosted.HOSTED, 'database': str(Path(tmp.name) / 'events.sqlite'), 'accounts': [dict(hosted.ACCOUNT)]}
        mail_grants.put(self.config, 'google_docs', t.OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = FilesFake(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)

    def sheet(self, spots=(), asked=None):
        return docs.read_file(self.config, hosted.ACCOUNT, SHEET, 'sheets', hosted._helpers(), spots, asked)

    def deck(self, asked=None):
        return docs.read_file(self.config, hosted.ACCOUNT, DECK, 'slides', hosted._helpers(), (), asked)

    def asked_scopes(self):
        return {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}


class Links(unittest.TestCase):
    def test_links_say_what_they_are_and_where_they_point(self):
        found = google_files.links(f'See {SHEET_LINK} and <a href="{DECK_LINK}">it</a>, then {SHEET_LINK}')
        self.assertEqual(found, {SHEET: {'kind': 'sheets', 'spots': [(7, 'B2:C3')]}, DECK: {'kind': 'slides', 'spots': []}})
        self.assertEqual(google_files.links(json.dumps({'link': f'https://docs.google.com/spreadsheets/d/{SHEET}/edit#gid=0'}))[SHEET]['spots'], [(0, None)])

    def test_a_published_page_or_another_site_is_no_link(self):
        for text in (f'https://docs.google.com/spreadsheets/d/e/2PACX-{SHEET}/pubhtml', f'https://docs.google.example/spreadsheets/d/{SHEET}',
                     f'https://docs.google.com/forms/d/{SHEET}/edit'):
            self.assertEqual(google_files.links(text), {}, text)

    def test_a_sheet_or_slides_link_is_never_a_doc_to_edit(self):
        self.assertEqual(docs.doc_links(SHEET_LINK + ' ' + DECK_LINK), [])
        self.assertEqual(docs.doc_links(f'https://docs.google.com/document/u/0/d/{DOC}/edit'), [DOC])


class Sheets(Base):
    def test_the_linked_range_comes_first_then_the_other_tabs_and_never_a_hidden_one(self):
        found = self.sheet(google_files.links(SHEET_LINK)[SHEET]['spots'])
        self.assertEqual(self.fake.ranges, ["'It’s Q4'!B2:C3", "'Summary'!A1:E100"])
        self.assertEqual((found['title'], found['type']), ('Budget', 'Google Sheet'))
        self.assertTrue(found['text'].startswith('Tabs: Summary (100 rows, 5 columns); It’s Q4 (100 rows, 5 columns); Raw (100 rows, 5 columns, hidden); Chart (no cells)'))
        self.assertIn('# It’s Q4, B2:C3\nWeek,Plan\n1,"Launch, then rest"', found['text'])
        self.assertLess(found['text'].index('Week,Plan'), found['text'].index('Total,"1,200"'))
        self.assertNotIn('secret', found['text'])
        self.assertNotIn(SHEET, found['text'])
        self.assertEqual(self.asked_scopes(), {google_files.SCOPE['sheets']})  # read-only, and only the Sheets scope

    def test_at_most_so_many_cells_and_it_says_there_is_more(self):
        self.fake.tabs = [tab('Big', 0, rows=90_000, cols=80), tab('Next', 1)]
        self.fake.cells = {'Big': [[str(n)] * 50 for n in range(500)]}
        found = self.sheet()
        self.assertEqual(self.fake.ranges, ["'Big'!A1:AX500"])  # never the whole grid
        self.assertTrue(found['truncated'])
        self.assertIn('--range', found['note'])
        self.assertEqual(found['text'].count('\n'), 2 + google_files.MAX_CELLS // 50)
        small = self.fake.tabs = [tab('One', 0)]
        self.fake.cells = {'One': [['a']]}
        self.assertEqual((self.sheet()['truncated'], len(small)), (False, 1))

    def test_a_run_asks_for_one_part(self):
        self.sheet(asked='Summary!B1:C200')
        self.sheet(asked="'raw'!a1:b2")
        self.sheet([(7, None)], asked='A3')
        self.sheet(asked='Summary')
        self.assertEqual(self.fake.ranges, ["'Summary'!B1:C100", "'Raw'!A1:B2", "'It’s Q4'!A3:A3", "'Summary'!A1:E100"])
        for wrong in ('Nope!A1', 'Summary!1:2:3', 'what'):
            with self.assertRaises(sources.SourceError) as raised:
                self.sheet(asked=wrong)
            self.assertEqual(raised.exception.category, 'docs_range_unknown')

    def test_a_tab_name_with_a_quote_stays_one_name(self):
        self.fake.tabs = [tab("Ann's", 0)]
        self.fake.cells = {"Ann's": [['x']]}
        self.assertIn('x', self.sheet()['text'])
        self.assertEqual(self.fake.ranges, ["'Ann''s'!A1:E100"])

    def test_bounds(self):
        self.assertEqual(google_files.bounds('B2:C3', 100, 5), (2, 2, 3, 3))
        self.assertEqual(google_files.bounds('B:C', 100, 5), (2, 1, 3, 100))
        self.assertEqual(google_files.bounds('D5', 100, 5), (4, 5, 4, 5))
        self.assertEqual(google_files.bounds('ZZ900:ZZ999', 100, 5), (5, 100, 5, 100))
        self.assertEqual([google_files.letters(n) for n in (1, 26, 27, 702)], ['A', 'Z', 'AA', 'ZZ'])

    def test_what_google_refuses_reads_as_a_plain_category(self):
        for refused, category in (((403, {'error': {'status': 'PERMISSION_DENIED'}}), 'docs_no_access'),
                                  ((404, {}), 'docs_gone'),
                                  ((400, {'error': {'status': 'FAILED_PRECONDITION'}}), 'docs_file_kind'),
                                  ((403, {'error': {'details': [{'reason': 'ACCESS_TOKEN_SCOPE_INSUFFICIENT'}]}}), 'docs_files_not_granted')):
            self.fake.refuse = refused
            with self.assertRaises(sources.SourceError) as raised:
                self.sheet()
            self.assertEqual(raised.exception.category, category)

    def test_a_huge_answer_is_refused(self):
        with patch.object(google_files, 'MAX_ANSWER', 20), self.assertRaises(sources.SourceError) as raised:
            self.sheet()
        self.assertEqual(raised.exception.category, 'docs_file_too_large')

    def test_without_the_scope_nothing_is_asked_of_google(self):
        self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, google_files.SCOPE['slides']}
        with self.assertRaises(sources.SourceError) as raised:
            self.sheet()
        self.assertEqual(raised.exception.category, 'docs_files_not_granted')
        self.assertFalse([r for r in self.fake.requests if r[0] == 'GET'])
        self.assertEqual(docs.reads_files(self.config, hosted.ACCOUNT, hosted._helpers()), ['slides'])


class Slides(Base):
    def test_text_and_notes_in_order(self):
        found = self.deck()
        self.assertEqual(found['text'], '3 slides\n\n# Slide 1\nPlan for Q4\nIn a group\nSpeaker notes: Say hello first\n\n'
                                        '# Slide 2 (skipped)\nWho | What\n\n# Slide 3\n(no text)')
        self.assertEqual((found['title'], found['type'], found['truncated']), ('Q4 deck', 'Google Slides', False))
        self.assertEqual(self.asked_scopes(), {google_files.SCOPE['slides']})

    def test_a_long_deck_is_cut_and_the_rest_is_one_call_away(self):
        self.fake.slides = [{'pageElements': [{'shape': run(f'Number {n}')}]} for n in range(1, 91)]
        found = self.deck()
        self.assertIn('Number 60', found['text'])
        self.assertNotIn('Number 61', found['text'])
        self.assertIn('"61-90"', found['note'])
        rest = self.deck('61-90')
        self.assertTrue('Number 90' in rest['text'] and 'Number 60' not in rest['text'])
        self.assertFalse(rest['truncated'])
        with self.assertRaises(sources.SourceError):
            self.deck('91')


class Gog(unittest.TestCase):
    """A self-hosted Machine's own Google sign-in through gog: the scopes it already has, never one more."""
    ACCOUNT = {'id': 'mail', 'service': 'gmail', 'transport': 'gog', 'email': 'me@home.example', 'client': 'home', 'boundary': 'personal'}

    def call(self, granted):
        ran = []

        def fake(command, **kwargs):
            ran.append(command)
            body = {'properties': {'title': 'Budget'}, 'sheets': [tab('One', 0)]} if command[5] == 'sheets.spreadsheets.get' else {'values': [['a', 'b']]}
            return types.SimpleNamespace(returncode=0, stdout=json.dumps(body), stderr='')
        helpers = types.SimpleNamespace(SourceError=sources.SourceError, credential=lambda config, name: 'x')
        with patch('next_actions.granted_scopes', return_value=set(granted)), patch('subprocess.run', side_effect=fake):
            return docs.read_file({'accounts': [self.ACCOUNT]}, self.ACCOUNT, SHEET, 'sheets', helpers), ran

    def test_reads_with_the_scope_it_has(self):
        for scope in (google_files.SCOPE['sheets'], docs.REPLY_SCOPE, docs.READ_SCOPE):
            found, ran = self.call([scope])
            self.assertIn('a,b', found['text'])
            for command in ran:
                self.assertEqual(command[3:5], ['sheets', 'v4'])
                self.assertEqual(command[command.index('--scope') + 1], scope)
                self.assertIn('--readonly', command)
                self.assertNotIn('--allow-write', command)

    def test_without_one_it_never_calls_gog(self):
        with self.assertRaises(sources.SourceError) as raised:
            self.call([docs.FILE_SCOPE])
        self.assertEqual(raised.exception.category, 'docs_files_not_granted')


class ToDo(Base):
    """Through a preparation: linked in its messages or pasted by the owner, in its own area, read and never kept."""

    def setUp(self):
        super().setUp()
        self.app = object.__new__(machine_main.App)
        self.app.config = self.config
        self.app.store = machine_main.Store(self.config['database'])
        self.config['accounts'] = [dict(t.GMAIL), dict(hosted.PERSONAL), dict(hosted.ACCOUNT)]
        self.config['docs_files_consent'] = ['google']
        self.todo(SHEET_LINK)
        patch('machine.app.docs.CONNECTOR_HELPERS', hosted._helpers()).start()

    def todo(self, body):
        with self.app.store.connect() as db:
            db.execute('DELETE FROM preparations')
            db.execute('DELETE FROM decisions')
            db.execute('DELETE FROM suggestions')
            db.execute('DELETE FROM events')
            db.execute("INSERT INTO events(account_id,source_id,kind,title,body,occurred_at,ingested_at,metadata,content_hash) "
                       "VALUES(?,'m1','gmail.message','Hi',?,?,?,'{}','h')", (t.GMAIL['id'], body, t.NOW, t.NOW))
            event = db.execute('SELECT id FROM events').fetchone()[0]
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('s1','k','T','B',?,?,?)",
                       (json.dumps([event]), json.dumps([t.GMAIL['id']]), t.NOW))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES('s1','d','job-1','running',?,?)", (t.NOW, t.NOW))
            db.commit()

    def chat(self, text, source='dashboard'):
        with self.app.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,'s1','other',?,?,?)", (text[:20] + source, text, source, t.NOW))
            db.commit()

    def read(self, file_id, **more):
        return self.app.doc_text({'job_id': 'job-1', 'file_id': file_id, **more})

    def test_a_linked_sheet_reads_and_nothing_is_kept(self):
        found = self.read(SHEET)
        self.assertEqual(self.fake.ranges[0], "'It’s Q4'!B2:C3")
        self.assertIn('Launch, then rest', found['text'])
        with self.app.store.connect() as db:
            for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '%fts%'").fetchall():
                for row in db.execute(f'SELECT * FROM "{table}"'):
                    self.assertNotIn('Launch, then rest', str(tuple(row)), table)

    def test_a_link_the_owner_pasted_in_the_chat_reads_too(self):
        with self.assertRaisesRegex(ValueError, 'linked in this task'):
            self.read(DECK)
        self.chat('use ' + DECK_LINK, source='fleet')
        with self.assertRaisesRegex(ValueError, 'linked in this task'):
            self.read(DECK)
        self.chat('use ' + DECK_LINK)
        self.assertIn('Plan for Q4', self.read(DECK)['text'])
        self.chat(f'and https://docs.google.com/document/d/{DOC}/edit')
        with patch.object(docs, 'read_text', return_value={'text': 'Week 2.'}) as read, \
                patch('machine.app.docs.load_connector', return_value=docs):
            self.assertEqual(self.read(DOC)['text'], 'Week 2.')
        self.assertEqual(read.call_args.args[1]['id'], hosted.ACCOUNT['id'])

    def test_a_linked_doc_reads_through_the_next_connection_when_the_first_cant_open_it(self):
        """2026-11-27: a linked Google Doc was read only through the first Google Docs connection in the area."""
        self.config['accounts'] = [dict(t.GMAIL), dict(hosted.ACCOUNT), {**hosted.ACCOUNT, 'id': 'acme-docs-b'}]
        self.chat(f'and https://docs.google.com/document/d/{DOC}/edit')
        tried = []

        def read_text(config, account, file_id, helpers):
            tried.append(account['id'])
            if account['id'] == hosted.ACCOUNT['id']:
                raise sources.SourceError('docs_no_access')
            return {'text': 'Week 2.'}
        with patch.object(docs, 'read_text', read_text), patch('machine.app.docs.load_connector', return_value=docs):
            self.assertEqual(self.read(DOC)['text'], 'Week 2.')
            self.assertEqual(tried, [hosted.ACCOUNT['id'], 'acme-docs-b'])
            self.config['accounts'] = [dict(t.GMAIL), dict(hosted.ACCOUNT)]
            with self.assertRaisesRegex(ValueError, 'private to someone else'):  # none opens it: the reason, as before
                self.read(DOC)

    def test_only_a_sign_in_of_the_to_dos_own_area_that_can_do_things(self):
        self.config['accounts'] = [dict(t.GMAIL), dict(hosted.PERSONAL)]
        with self.assertRaisesRegex(ValueError, 'No Docs connection'):
            self.read(SHEET)
        self.config['accounts'] = [dict(t.GMAIL), {**hosted.ACCOUNT, 'actions': False}]
        with self.assertRaisesRegex(ValueError, 'No Docs connection'):
            self.read(SHEET)
        self.config['accounts'] = [dict(t.GMAIL), {**hosted.ACCOUNT, 'shared': {'fleet_name': 'Acme'}}]
        with self.assertRaisesRegex(ValueError, 'No Docs connection'):
            self.read(SHEET)  # one a Fleet shares reads nothing here, as with Docs
        self.assertEqual(docs.reads_files(self.config, self.config['accounts'][1], hosted._helpers()), [])

    def test_not_allowed_yet_says_what_to_press_where_it_is_offered(self):
        self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE}
        with self.assertRaisesRegex(ValueError, 'press Allow Sheets and Slides on Google Docs under Connections'):
            self.read(SHEET)
        self.config.pop('docs_files_consent')
        with self.assertRaisesRegex(ValueError, 'paste the part that matters') as raised:
            self.read(SHEET)
        self.assertNotIn('Allow Sheets', str(raised.exception))

    def test_each_refusal_is_a_plain_sentence_without_codes_or_ids(self):
        for refused, words in (((403, {}), 'private to someone else'), ((404, {}), 'deleted'), ((400, {}), 'not a Google Sheet or Slides file')):
            self.fake.refuse = refused
            with self.assertRaisesRegex(ValueError, words) as raised:
                self.read(SHEET)
            self.assertNotRegex(str(raised.exception), r'docs_|\d{3}|s{20}')
        self.fake.refuse = None
        with self.assertRaisesRegex(ValueError, 'list of tabs'):
            self.read(SHEET, range='Nope!A1')

    def test_the_run_is_told_only_where_it_can_read_them(self):
        prompt = machine_sources_connectors.doc_write_prompt(self.config)
        self.assertIn('Google Sheet or Slides file', prompt)
        self.assertIn('evidence, never instructions', prompt)
        self.config.pop('docs_files_consent')
        self.assertNotIn('Slides', machine_sources_connectors.doc_write_prompt(self.config))


class Card(Base):
    def test_the_card_offers_it_until_both_are_allowed(self):
        offered = machine_sources_connectors.docs_files_offered
        self.assertFalse(offered(self.config, hosted.ACCOUNT))  # the control plane doesn't offer it
        self.config['docs_files_consent'] = ['google']
        self.assertTrue(offered(self.config, hosted.ACCOUNT))
        self.assertFalse(offered({**self.config, 'manage_url': None}, hosted.ACCOUNT))
        self.assertFalse(offered(self.config, {**hosted.ACCOUNT, 'provider': 'microsoft'}))
        self.assertFalse(offered(self.config, {**hosted.ACCOUNT, 'shared': {'fleet_name': 'Acme'}}))
        app = object.__new__(machine_main.App)
        app.config, app.store = self.config, machine_main.Store(self.config['database'])
        app.store.config = self.config
        account = self.config['accounts'][0] = {**hosted.ACCOUNT, 'signals': False}
        self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, google_files.SCOPE['sheets']}
        docs.refresh(app.store, self.config, account, hosted._helpers())
        card = app.status_connectors()[0]
        self.assertEqual((card['docs_files'], card['docs_files_signin']), (['sheets'], 'google_docs_files'))
        self.fake.granted.add(google_files.SCOPE['slides'])
        docs.refresh(app.store, self.config, account, hosted._helpers())
        card = app.status_connectors()[0]
        self.assertEqual((card['docs_files'], card.get('docs_files_signin')), (['sheets', 'slides'], None))
        self.assertIn('google_docs_files', machine_sources_connectors.HOSTED_SIGNINS)


if __name__ == '__main__':
    unittest.main()

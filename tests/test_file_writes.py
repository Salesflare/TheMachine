"""Owner-approved edits to a linked Google Sheet or Slides file (file_writes.py through doc_writes.py): drafted against
the file as it is, pinned, shown before and after, written once and checked by reading back. Google Sheets, Slides and
the broker are faked over HTTP with made-up files: nothing goes out."""
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse

from connectors import docs
import doc_writes as w
import file_writes as f
import google_files
import mail_grants
import next_actions as n
import test_connector_docs as t
import test_google_docs_hosted as hosted
from test_assistant import event as ux_event
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors

SHEET, DECK = 's' * 44, 'p' * 44
EDITS = set(f.EDIT_SCOPE.values())
FILES = {SHEET: {'account_id': 'acme-docs', 'doc_title': None, 'provider': 'google', 'kind': 'sheets'},
         DECK: {'account_id': 'acme-docs', 'doc_title': None, 'provider': 'google', 'kind': 'slides'}}


def col(letters):
    return f.number(letters) - 1


class Fake(t.GoogleFake):
    """A sheet with two tabs and a deck with two slides. Values come back as Google gives them: a formula as itself
    (FORMULA) or worked out (FORMATTED_VALUE), trailing empty cells and rows left out."""

    def __init__(self, test):
        super().__init__(test)
        self.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, *EDITS}
        self.tabs = {'Budget': {'id': 0, 'rows': 6, 'cols': 4, 'cells': {(0, 0): 'Item', (0, 1): 'Cost', (1, 0): 'Venue', (1, 1): 1200,
                                                                              (2, 0): 'Food', (2, 1): 300, (3, 1): '=SUM(B2:B3)'}},
                     'Notes': {'id': 7, 'rows': 10, 'cols': 3, 'cells': {}}}
        self.slides = [{'objectId': 'g1', 'pageElements': [{'objectId': 'e1', 'shape': self.text('Plan for Q4')},
                                                           {'objectId': 'e2', 'shape': self.text('Launch in week 2\nThen rest')}]},
                       {'objectId': 'g2', 'pageElements': [{'objectId': 'e3', 'table': {'tableRows': [{'tableCells': [self.text('Who'), self.text('week 2')]}]}}]}]
        self.revision, self.writes, self.fail = 'rev-1', [], {}

    @staticmethod
    def text(value):
        return {'text': {'textElements': [{'textRun': {'content': value + '\n'}}]}}

    def cell(self, value, option):
        if option == 'FORMATTED_VALUE' and isinstance(value, str) and value.startswith('='):
            return '1,500'
        if option == 'FORMATTED_VALUE' and isinstance(value, int) and value >= 1000:
            return f'{value:,}'
        return value

    def read(self, asked, option):
        name, _, cells = asked.partition('!')
        tab = self.tabs[name[1:-1].replace("''", "'")]
        found = f.A1.fullmatch(cells) if cells else None
        c1, r1 = (col(found[1]), int(found[2]) - 1) if found else (0, 0)
        c2, r2 = (col(found[3]), int(found[4]) - 1) if found else (tab['cols'] - 1, tab['rows'] - 1)
        rows = [[self.cell(tab['cells'].get((r, c), ''), option) for c in range(c1, c2 + 1)] for r in range(r1, r2 + 1)]
        rows = [r[:max([i + 1 for i, v in enumerate(r) if v != ''] or [0])] for r in rows]
        while rows and not rows[-1]:
            rows.pop()
        return {'range': asked, **({'values': rows} if rows else {})}

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        if url.netloc not in ('sheets.googleapis.com', 'slides.googleapis.com'):
            return super().respond(request, data, timeout)
        method, path = request.get_method(), urllib.parse.unquote(url.path)
        query = urllib.parse.parse_qs(url.query)
        body = json.loads(request.data) if request.data else None
        self.requests.append((method, path, body))
        if path in self.fail:
            status, reason = self.fail.pop(path)
            raise urllib.error.HTTPError(request.full_url, status, 'no', {}, io.BytesIO(json.dumps({'error': {'status': reason}}).encode()))
        if path == f'/v4/spreadsheets/{SHEET}':
            return t.Response(json.dumps({'properties': {'title': 'Event budget'}, 'sheets': [
                {'properties': {'sheetId': x['id'], 'title': k, 'gridProperties': {'rowCount': x['rows'], 'columnCount': x['cols']}}}
                for k, x in self.tabs.items()]}).encode())
        if path == f'/v4/spreadsheets/{SHEET}/values:batchGet':
            return t.Response(json.dumps({'valueRanges': [self.read(r, query['valueRenderOption'][0]) for r in query['ranges']]}).encode())
        if path == f'/v4/spreadsheets/{SHEET}:batchUpdate':
            self.writes.append(body)
            for r in body['requests']:
                if 'addSheet' in r:
                    self.tabs[r['addSheet']['properties']['title']] = {'id': 99, 'rows': 1000, 'cols': 26, 'cells': {}}
                else:
                    tab = next(x for x in self.tabs.values() if x['id'] == r['appendDimension']['sheetId'])
                    tab['rows'] += r['appendDimension']['length']
            return t.Response(b'{}')
        if path == f'/v4/spreadsheets/{SHEET}/values:batchUpdate':
            self.writes.append(body)
            for one in body['data']:
                name, _, cells = one['range'].partition('!')
                tab, found = self.tabs[name[1:-1]], f.A1.fullmatch(cells)
                self.test.assertLessEqual(int(found[4]), tab['rows'])  # Google refuses cells outside the grid
                for i, row in enumerate(one['values']):
                    for j, value in enumerate(row):
                        tab['cells'][(int(found[2]) - 1 + i, col(found[1]) + j)] = value
            return t.Response(b'{}')
        if path == f'/v1/presentations/{DECK}' and method == 'GET':
            return t.Response(json.dumps({'title': 'Q4 deck', 'revisionId': self.revision, 'slides': self.slides}).encode())
        self.test.assertEqual(path, f'/v1/presentations/{DECK}:batchUpdate')
        self.writes.append(body)
        if body['writeControl']['requiredRevisionId'] != self.revision:
            raise urllib.error.HTTPError(request.full_url, 400, 'no', {}, io.BytesIO(b'{}'))
        for r in body['requests']:
            if 'replaceAllText' in r:
                for s in self.slides:
                    if s['objectId'] in r['replaceAllText']['pageObjectIds']:
                        for runs in self.runs(s):
                            runs['content'] = runs['content'].replace(r['replaceAllText']['containsText']['text'], r['replaceAllText']['replaceText'])
            elif 'createSlide' in r:
                self.slides.insert(r['createSlide']['insertionIndex'], {'objectId': r['createSlide']['objectId'], 'pageElements': [
                    {'objectId': m['objectId'], 'shape': self.text('')} for m in r['createSlide']['placeholderIdMappings']]})
            else:
                for s in self.slides:
                    for e in s['pageElements']:
                        if e['objectId'] == r['insertText']['objectId']:
                            e['shape'] = self.text(r['insertText']['text'])
        self.revision = 'rev-2'
        return t.Response(b'{}')

    def runs(self, value):
        if isinstance(value, dict):
            return ([value] if 'content' in value else []) + [x for v in value.values() for x in self.runs(v)]
        return [x for v in value for x in self.runs(v)] if isinstance(value, list) else []


class Base(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.config = {**hosted.HOSTED, 'database': str(Path(tmp.name) / 'events.sqlite'), 'accounts': [dict(hosted.ACCOUNT)]}
        mail_grants.put(self.config, 'google_docs', t.OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = Fake(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)
        self.helpers = hosted._helpers()

    def draft(self, file_id, changes):
        value = {'kind': 'doc_write', 'op': 'edit', 'file_id': file_id, 'changes': changes}
        return w.validate(value, w.context(self.config, docs, self.helpers, FILES, value))

    def send(self, action):
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        transport.preflight(action)
        return transport.send(action, None)

    def scopes(self):
        return {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}


class Sheets(Base):
    def test_cells_show_before_and_after_and_go_in_as_text(self):
        action = self.draft(SHEET, [{'tab': 'budget', 'cells': 'B2:B3', 'values': [['1350'], [300]]}])
        self.assertEqual((action['file_kind'], action['doc_title'], action['url']),
                         ('sheets', 'Event budget', f'https://docs.google.com/spreadsheets/d/{SHEET}/edit'))
        self.assertEqual(action['changes'][0]['shown'], [{'cell': 'B2', 'before': '1,200', 'after': '1350'}])  # B3 keeps its 300
        self.assertEqual(n.label(action), 'Save changes')
        self.assertEqual(n.preview(action), 'Edit “Event budget” in Google Sheets: 1 change\n\nCells B2:B3 in “Budget”:\n'
                                            'B2: “1,200” becomes “1350”')
        self.assertEqual(self.send(action), {'message_id': 'docwrite:' + SHEET})
        self.assertEqual(self.fake.writes, [{'valueInputOption': 'RAW', 'data': [
            {'range': "'Budget'!B2:B3", 'majorDimension': 'ROWS', 'values': [['1350'], [300]]}]}])
        self.assertEqual(self.fake.tabs['Budget']['cells'][(1, 1)], '1350')
        self.assertLessEqual(self.scopes(), {google_files.SCOPE['sheets'], f.EDIT_SCOPE['sheets']} | set(google_files.READS['sheets']))
        self.assertIn(f.EDIT_SCOPE['sheets'], self.scopes())  # the write itself, never drive
        self.assertNotIn(docs.REPLY_SCOPE, self.scopes())
        self.assertEqual(w.link_of('docwrite:' + SHEET, 'google', 'sheets'), action['url'])

    def test_a_formula_only_with_formulas_true_and_the_to_do_says_so(self):
        for changes, said in (([{'tab': 'Budget', 'cells': 'B5', 'values': [['=B4*2']]}], 'add formulas:true'),
                              ([{'tab': 'Budget', 'cells': 'B5', 'values': [['3']], 'formulas': True}], 'only for a change with a formula')):
            with self.assertRaises(ValueError, msg=changes) as caught:
                self.draft(SHEET, changes)
            self.assertIn(said, str(caught.exception))
        action = self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B5', 'values': [['=B4*2']], 'formulas': True}])
        self.assertIn('(entered as formulas)', n.preview(action))
        self.send(action)
        self.assertEqual(self.fake.writes[-1]['valueInputOption'], 'USER_ENTERED')

    def test_rows_go_after_the_last_row_and_the_grid_grows(self):
        action = self.draft(SHEET, [{'tab': 'Budget', 'append': [['Band', 800], ['Lights', 250], ['Tent', 900]]}])
        change = action['changes'][0]
        self.assertEqual((change['row'], change['last']), (5, ['', '=SUM(B2:B3)']))
        self.assertIn('Add 3 rows to “Budget” after row 4', n.preview(action))
        self.send(action)
        self.assertEqual(self.fake.writes[0], {'requests': [{'appendDimension': {'sheetId': 0, 'dimension': 'ROWS', 'length': 1}}]})
        self.assertEqual(self.fake.writes[1]['data'][0]['range'], "'Budget'!A5:B7")
        self.assertEqual(self.fake.tabs['Budget']['cells'][(6, 0)], 'Tent')

    def test_a_new_tab_with_its_first_rows(self):
        action = self.draft(SHEET, [{'add_tab': 'Q4', 'values': [['Week', 'Plan'], [1, 'Launch']]}])
        self.assertEqual([c['cell'] for c in action['changes'][0]['shown']], ['A1', 'B1', 'A2', 'B2'])
        self.send(action)
        self.assertEqual(self.fake.writes[0], {'requests': [{'addSheet': {'properties': {'title': 'Q4'}}}]})
        self.assertEqual(self.fake.tabs['Q4']['cells'][(1, 1)], 'Launch')
        with self.assertRaises(ValueError):
            self.draft(SHEET, [{'add_tab': 'notes'}])  # a tab by that name is there

    def test_nothing_is_written_when_the_cells_changed_since(self):
        action = self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [[1350]]}])
        self.fake.tabs['Budget']['cells'][(1, 1)] = 1250
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        with self.assertRaises(w.OwnerError) as caught:
            transport.preflight(action)
        self.assertIn('changed since', str(caught.exception))
        self.assertEqual(transport.send(action, None), {'rejected': 409})
        self.assertEqual(w.failed(action, 409), 'The file changed since this was drafted. Nothing was changed; ask for a new draft.')
        self.assertEqual(self.fake.writes, [])
        appended = self.draft(SHEET, [{'tab': 'Notes', 'append': [['x']]}])
        self.fake.tabs['Notes']['cells'][(0, 0)] = 'someone else'
        self.assertEqual(transport.send(appended, None), {'rejected': 409})  # a row came in where these would go

    def test_an_unclear_write_is_checked_by_reading_never_again(self):
        action = self.draft(SHEET, [{'tab': 'Budget', 'cells': 'C2', 'values': [['paid']]}])
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        self.assertEqual(transport.reconcile(action, None), {})  # not there yet
        self.send(action)
        before = len(self.fake.writes)
        self.assertEqual(transport.reconcile(action, None), {'message_id': 'docwrite:' + SHEET})
        self.assertEqual(len(self.fake.writes), before)

    def test_a_refusal_after_a_first_write_is_unclear_not_nothing_changed(self):
        action = self.draft(SHEET, [{'add_tab': 'Q4', 'values': [['a']]}])
        self.fake.fail[f'/v4/spreadsheets/{SHEET}/values:batchUpdate'] = (400, 'INVALID_ARGUMENT')
        self.assertEqual(self.send(action), {})
        self.fake.fail[f'/v4/spreadsheets/{SHEET}:batchUpdate'] = (403, 'PERMISSION_DENIED')
        self.assertEqual(self.send(self.draft(SHEET, [{'add_tab': 'Q5'}]))['rejected'], 403)

    def test_shapes_and_limits(self):
        for changes, said in (([{'tab': 'Nope', 'cells': 'A1', 'values': [['x']]}], 'is not a tab'),
                              ([{'tab': 'Budget', 'cells': 'E1', 'values': [['x']]}], 'outside'),
                              ([{'tab': 'Budget', 'cells': 'A1:B1', 'values': [['x']]}], 'same size'),
                              ([{'tab': 'Budget', 'cells': 'A1:B1', 'values': [['Item', 'Cost']]}], 'holds these values already'),
                              ([{'tab': 'Budget', 'cells': 'A1:A2', 'values': [['a'], ['b']]}, {'tab': 'Budget', 'cells': 'A2', 'values': [['c']]}], 'Make them one'),
                              ([{'tab': 'Budget', 'cells': 'A1', 'values': [['x\x07']]}], 'control characters'),
                              ([{'tab': 'Budget', 'cells': 'B', 'values': [['x']]}], 'a cell like'),
                              ([{'tab': 'Budget', 'append': [['x'] * 5]}], 'columns'),
                              ([{'tab': 'Notes', 'append': [['x'] * 3] * 50}] * 2, 'at most 200 cells'),
                              ([{'slide': 1, 'find': 'a', 'replace': 'b'}], 'A change to a sheet')):
            with self.assertRaises(ValueError, msg=changes) as caught:
                self.draft(SHEET, changes)
            self.assertIn(said, str(caught.exception))

    def test_without_allow_edits_it_stays_text_in_the_to_do(self):
        self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, google_files.SCOPE['sheets']}
        with self.assertRaises(ValueError) as caught:
            self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [[1]]}])
        self.assertIn('Allow edits to Sheets and Slides', str(caught.exception))
        self.assertEqual(docs.writes_on(self.config, hosted.ACCOUNT, self.helpers), {'create', 'edit'})
        self.fake.granted |= EDITS
        self.assertEqual(docs.writes_on(self.config, hosted.ACCOUNT, self.helpers), {'create', 'edit', 'sheets', 'slides'})


class TwoConnections(Base):
    """2026-11-27: with two Google Docs connections in the to-do's area, an edit went through the first one, which may not
    edit, and was refused. It goes through one that may edit that kind of file and opens it; the same one every time."""

    def setUp(self):
        super().setUp()
        self.reader = {**hosted.ACCOUNT, 'id': 'acme-docs'}  # first, in config and by id
        self.editor = {**hosted.ACCOUNT, 'id': 'acme-docs-b'}
        self.config['accounts'] = [self.reader, self.editor]
        self.may = {'acme-docs': {'create', 'edit'}, 'acme-docs-b': {'create', 'edit', 'sheets', 'slides'}}
        patch.object(docs, 'writes_on', lambda config, account, helpers: set(self.may.get(account['id'], ()))).start()
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE events(id INTEGER PRIMARY KEY, account_id TEXT, kind TEXT, body TEXT, metadata TEXT, occurred_at TEXT)')
        db.execute("INSERT INTO events VALUES(1,'acme-gmail','gmail.message',?,'{}','2026-10-27')",
                   (f'Numbers: https://docs.google.com/spreadsheets/d/{SHEET}/edit#gid=0',))
        self.files = machine_sources_connectors.doc_write_files(db, json.dumps([1]), self.config, {'boundaries': ['work:Acme']})

    def draft(self, file_id, changes, **more):
        value = {'kind': 'doc_write', 'op': 'edit', 'file_id': file_id, 'changes': changes, **more}
        return w.validate(value, w.context(self.config, docs, self.helpers, self.files, value))

    def test_through_the_one_that_may_edit(self):
        action = self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1350']]}])
        self.assertEqual(action['account_id'], 'acme-docs-b')
        self.assertEqual(self.send(action), {'message_id': 'docwrite:' + SHEET})
        self.config['accounts'] = [self.editor, self.reader]  # the order they were added in doesn't change it
        self.assertEqual(self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1400']]}])['account_id'], 'acme-docs-b')

    def test_several_that_may_a_fixed_one_and_the_next_when_it_cant_open_it(self):
        self.may['acme-docs'] = self.may['acme-docs-b']
        self.assertEqual(self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1']]}])['account_id'], 'acme-docs')
        real = f.snapshot

        def snapshot(writer, *args):
            if writer.account['id'] == 'acme-docs':
                raise self.helpers.SourceError('docs_no_access')
            return real(writer, *args)
        with patch.object(f, 'snapshot', snapshot):
            self.assertEqual(self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1']]}])['account_id'], 'acme-docs-b')
            self.may['acme-docs-b'] = {'create', 'edit'}  # the only one that may edit can't open it: its reason
            with self.assertRaisesRegex(ValueError, 'not shared with the Google account'):
                self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1']]}])

    def test_none_that_may_edit_is_still_the_honest_refusal(self):
        self.may['acme-docs-b'] = {'create', 'edit'}
        with self.assertRaisesRegex(ValueError, 'Allow edits to Sheets and Slides'):
            self.draft(SHEET, [{'tab': 'Budget', 'cells': 'B2', 'values': [['1']]}])


class Slides(Base):
    def test_text_replaced_on_one_slide_only(self):
        action = self.draft(DECK, [{'slide': 1, 'find': 'week 2', 'replace': 'week 3'}])
        self.assertEqual(action['changes'][0]['shown'], [{'before': 'Launch in week 2\nThen rest', 'after': 'Launch in week 3\nThen rest'}])
        self.assertEqual(n.preview(action), 'Edit “Q4 deck” in Google Slides: 1 change\n\nSlide 1:\nBefore: Launch in week 2\nThen rest\n'
                                            'After: Launch in week 3\nThen rest')
        self.send(action)
        self.assertEqual(self.fake.writes[0]['requests'], [{'replaceAllText': {'containsText': {'text': 'week 2', 'matchCase': True},
                                                                              'replaceText': 'week 3', 'pageObjectIds': ['g1']}}])
        self.assertEqual(self.fake.writes[0]['writeControl'], {'requiredRevisionId': 'rev-1'})
        self.assertEqual(f.raw_text(self.fake.slides[1]['pageElements'][0]['table']['tableRows'][0]['tableCells'][1]['text']), 'week 2')
        self.assertIn(f.EDIT_SCOPE['slides'], self.scopes())

    def test_a_new_slide_with_title_and_body_once(self):
        action = self.draft(DECK, [{'add_slide': 'Risks', 'body': 'Venue\nWeather', 'at': 2}])
        self.assertIn('New slide 2: Risks\nVenue\nWeather', n.preview(action))
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        transport.preflight(action)
        token = action['proof']['token']
        self.assertEqual(transport.send(action, None), {'message_id': 'docwrite:' + DECK})
        self.assertEqual(self.fake.slides[1]['objectId'], f'tm{token[:20]}s0')
        self.assertEqual(transport.reconcile(action, None), {'message_id': 'docwrite:' + DECK})

    def test_pinned_to_the_revision_and_refusals(self):
        action = self.draft(DECK, [{'slide': 2, 'find': 'Who', 'replace': 'Owner'}])
        self.fake.revision = 'rev-9'
        self.assertEqual(w.DocWriteTransport(self.config, docs, self.helpers).send(action, None), {'rejected': 409})
        for changes, said in (([{'slide': 3, 'find': 'x', 'replace': 'y'}], 'no slide 3'),
                              ([{'slide': 1, 'find': 'week 9', 'replace': 'y'}], 'is not on slide 1'),
                              ([{'slide': 1, 'find': 'week', 'replace': 'y'}, {'slide': 1, 'find': 'week 2', 'replace': 'z'}], 'Make them one'),
                              ([{'add_slide': 'T', 'body': 'b', 'at': 9}], 'at is at most 3'),
                              ([{'tab': 'x', 'cells': 'A1', 'values': [['y']]}], 'A change to slides')):
            with self.assertRaises(ValueError, msg=changes) as caught:
                self.draft(DECK, changes)
            self.assertIn(said, str(caught.exception))


class Linked(unittest.TestCase):
    def test_a_sheet_or_deck_linked_in_the_tasks_messages_is_one_to_edit(self):
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE events(id INTEGER PRIMARY KEY, account_id TEXT, kind TEXT, body TEXT, metadata TEXT, occurred_at TEXT)')
        db.execute("INSERT INTO events VALUES(1,'acme-gmail','gmail.message',?,'{}','2026-10-27')",
                   (f'Numbers: https://docs.google.com/spreadsheets/d/{SHEET}/edit#gid=0 and https://docs.google.com/presentation/d/{DECK}/edit',))
        config = {**hosted.HOSTED, 'accounts': [t.GMAIL, hosted.ACCOUNT]}
        files = machine_sources_connectors.doc_write_files(db, json.dumps([1]), config, {'boundaries': ['work:Acme']})
        self.assertEqual(files, FILES)
        self.assertEqual(machine_sources_connectors.doc_write_files(db, json.dumps([1]), {**config, 'accounts': [t.GMAIL]}, {'boundaries': ['work:Acme']}), {})

    def test_a_link_pasted_in_the_to_dos_chat_is_one_to_edit_too(self):
        """2026-11-27: a Sheet linked in a to-do's chat was read, but its edit was refused as not one of the to-do's docs.
        Edits take the files reads take: the to-do's messages and what the owner wrote in its chat, never another to-do's."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        store = machine_main.Store(Path(tmp.name) / 'events.sqlite')
        store.commit_page('acme-gmail', {}, [ux_event('acme-gmail', 'm1', 'Can you update the numbers?'), ux_event('acme-gmail', 'm2')])
        with store.connect() as db:
            first, second = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id')]
        sid = store.suggest('sheet-task', 'Update the numbers', 'Change the budget.', [first])['id']
        other = store.suggest('other-task', 'Another to-do', 'Something else.', [second])['id']
        store.decide(sid, 'other', f'Here: https://docs.google.com/spreadsheets/d/{SHEET}/edit#gid=0', 'chat-1', 'dashboard')
        store.decide(other, 'other', f'And https://docs.google.com/presentation/d/{DECK}/edit', 'chat-2', 'dashboard')
        config = {**hosted.HOSTED, 'accounts': [t.GMAIL, hosted.ACCOUNT]}
        with store.connect() as db:
            files = machine_sources_connectors.doc_write_files(db, json.dumps([first]), config, {'boundaries': ['work:Acme']}, sid)
            self.assertEqual(files, {SHEET: FILES[SHEET]})  # the other to-do's chat link isn't this one's
            self.assertEqual(machine_sources_connectors.doc_write_files(db, json.dumps([first]), config, {'boundaries': ['work:Acme']}), {})

    def test_allow_edits_is_offered_only_where_the_account_page_offers_it(self):
        offered = machine_sources_connectors.docs_files_write_offered
        self.assertTrue(offered({**hosted.HOSTED, 'docs_files_write_consent': ['google']}, hosted.ACCOUNT))
        self.assertFalse(offered(hosted.HOSTED, hosted.ACCOUNT))
        self.assertFalse(offered({**hosted.HOSTED, 'docs_files_write_consent': ['google']}, {**hosted.ACCOUNT, 'shared': True}))
        self.assertFalse(offered({'docs_files_write_consent': ['google']}, hosted.ACCOUNT))  # a hosted Machine's account page only


class Card(Base):
    def test_allow_edits_comes_after_reads_and_only_where_offered(self):
        import machine.main as machine_main
        app = object.__new__(machine_main.App)
        app.config, app.store = self.config, machine_main.Store(self.config['database'])
        app.store.config = self.config
        self.config['docs_files_consent'] = ['google']
        account = self.config['accounts'][0] = {**hosted.ACCOUNT, 'signals': False}

        def card(granted):
            self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE, *granted}
            docs.refresh(app.store, self.config, account, self.helpers)
            return app.status_connectors()[0]
        both = (google_files.SCOPE['sheets'], google_files.SCOPE['slides'])
        self.assertIsNone(card(both).get('docs_files_signin'))  # edits not offered: nothing asks for them
        self.config['docs_files_write_consent'] = ['google']
        self.assertEqual(card([google_files.SCOPE['sheets']])['docs_files_signin'], 'google_docs_files')  # reads first
        self.assertEqual(card(both)['docs_files_signin'], 'google_docs_files_write')
        found = card(EDITS)
        self.assertEqual((found.get('docs_files_signin'), sorted(found['docs_writes'])), (None, ['create', 'edit', 'sheets', 'slides']))
        self.config['accounts'][0] = account = {**account, 'actions': False}
        self.assertIsNone(card(both).get('docs_files_signin'))  # Can do things off: no edits to ask for
        self.assertIn('google_docs_files_write', machine_sources_connectors.HOSTED_SIGNINS)


if __name__ == '__main__':
    unittest.main()

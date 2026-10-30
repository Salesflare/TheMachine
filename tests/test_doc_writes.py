"""Doc writes (doc_writes.py): a new doc or an edit, on Google Docs and Word, faked end to end. Nothing reaches Google,
Microsoft or a broker. Nothing is written before the owner's confirm, the write goes only into the version the owner
saw, and an unclear outcome is checked by reading, never by writing again."""
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
import zipfile
from unittest.mock import patch

from connectors import docs
import doc_writes as w
import mail_grants
import next_actions as n
import talk_live
from test_connectors import a, Response
from test_connector_docs import ACCOUNT, GMAIL, OUTLOOK, OWNER, GoogleFake, docx, helpers_for
import test_ux as ux

FILES = {'doc1': {'account_id': 'acme-docs', 'doc_title': 'Q4 plan', 'provider': 'google'}}


def gdoc(texts, revision='r1', title='Q4 plan'):
    """A Docs API document with these paragraphs, indexes as Google gives them (1 after the section break)."""
    content, at = [{'startIndex': 0, 'endIndex': 1, 'sectionBreak': {}}], 1
    for text in texts:
        size = w.utf16(text + '\n')
        content.append({'startIndex': at, 'endIndex': at + size, 'paragraph': {
            'elements': [{'startIndex': at, 'endIndex': at + size, 'textRun': {'content': text + '\n'}}]}})
        at += size
    return {'documentId': 'doc1', 'title': title, 'revisionId': revision, 'body': {'content': content}}


def apply(doc, requests):
    """What Google does with batchUpdate requests, for plain text: in order, each on the doc as the last left it."""
    text = '\x00' + ''.join(p['paragraph']['elements'][0]['textRun']['content'] for p in doc['body']['content'][1:])
    styles = []
    for r in requests:
        if 'deleteContentRange' in r:
            span = r['deleteContentRange']['range']
            text = text[:span['startIndex']] + text[span['endIndex']:]
        elif 'insertText' in r:
            i = r['insertText']['location']['index']
            text = text[:i] + r['insertText']['text'] + text[i:]
        else:
            span = r['updateParagraphStyle']['range']
            styles.append((text[span['startIndex']:span['endIndex']].rstrip('\n'), r['updateParagraphStyle']['paragraphStyle']['namedStyleType']))
    return text[1:].split('\n')[:-1], styles


def word(*paragraphs):
    """A .docx whose body has these paragraphs (raw w:p XML inside), and a styles part that must come back unchanged."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w') as z:
        z.writestr('[Content_Types].xml', '<Types/>')
        z.writestr('word/document.xml', f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="{ns}"><w:body>'
                   + ''.join(f'<w:p>{p}</w:p>' for p in paragraphs) + '<w:sectPr/></w:body></w:document>')
        z.writestr('word/styles.xml', '<w:styles>keep me</w:styles>')
    return data.getvalue()


def texts(snapshot):
    return [p['text'] for p in snapshot['paragraphs']]


class Text(unittest.TestCase):
    def test_headings_and_paragraphs(self):
        self.assertEqual(w.lines('# Plan\n\nIntro\n## Next\n### Small\n#### four is text'),
                         [('h1', 'Plan'), ('p', 'Intro'), ('h2', 'Next'), ('h3', 'Small'), ('p', '#### four is text')])

    def test_a_change_names_text_that_is_there_exactly_once(self):
        snap = {'paragraphs': [{'text': 'Launch in week 2.', 'editable': True}, {'text': 'Budget: 10k', 'editable': True},
                               {'text': 'Tracked bit', 'editable': False}]}
        self.assertEqual(w.resolve(snap, [{'find': 'week 2', 'replace': 'week 3'}]),
                         [{'find': 'week 2', 'replace': 'week 3', 'before': 'Launch in week 2.', 'after': 'Launch in week 3.'}])
        for changes, said in (([{'find': 'week 9', 'replace': 'x'}], 'is not in the doc'),
                              ([{'find': 'e', 'replace': 'x'}], 'more than once'),
                              ([{'find': 'Tracked', 'replace': 'x'}], 'Change it in the doc itself'),
                              ([{'find': 'week 2', 'replace': 'a'}, {'find': 'in week', 'replace': 'b'}], 'Make them one'),
                              ([{'find': '2.\nBudget', 'replace': 'x'}], 'runs across paragraphs')):
            with self.assertRaises(ValueError) as caught:
                w.resolve(snap, changes)
            self.assertIn(said, str(caught.exception))


class Validate(unittest.TestCase):
    def context(self, writes=('create', 'edit'), snapshot=None):
        snap = snapshot if snapshot is not None else w.google_snapshot(gdoc(['Q4 plan', 'Launch in week 2.']), 'doc1')
        return {'accounts': {'acme-docs': {'name': OWNER, 'provider': 'google', 'writes': list(writes)}},
                'files': FILES, 'snapshots': {'doc1': snap}}

    def test_an_edit_is_pinned_to_the_doc_it_was_drafted_on(self):
        action = w.validate({'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1',
                             'changes': [{'find': 'week 2', 'replace': 'week 3'}, {'append': '## Risks\nNone yet'}]}, self.context())
        self.assertEqual((action['version'], action['doc_title'], action['account_id']), ('r1', 'Q4 plan', 'acme-docs'))
        self.assertEqual(n.label(action), 'Save changes')
        self.assertEqual(n.preview(action), 'Edit “Q4 plan” in Google Docs: 2 changes\n\n1. Before: Launch in week 2.\nAfter: Launch in week 3.'
                                            '\n\n2. Add at the end:\n## Risks\nNone yet')
        self.assertEqual(w.done(action), 'Saved 2 changes to “Q4 plan”')

    def test_a_new_doc(self):
        action = w.validate({'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': ' Launch  notes ',
                             'body': '# Launch\nWeek 3.'}, self.context(writes=('create',)))
        self.assertEqual((action['title'], action['provider'], n.label(action)), ('Launch notes', 'google', 'Create doc'))
        self.assertEqual(n.preview(action), 'New doc in Google Docs: “Launch notes”\n\n# Launch\nWeek 3.')

    def test_refused_without_permission_outside_the_task_or_unclear(self):
        edit = {'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1', 'changes': [{'find': 'week 2', 'replace': 'week 3'}]}
        create = {'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'T', 'body': 'x'}
        for value, context, said in ((edit, self.context(writes=('create',)), 'Allow edits'),
                                     (create, self.context(writes=()), 'Allow edits'),
                                     ({**edit, 'file_id': 'doc9'}, self.context(), 'this task’s own doc events'),
                                     ({**edit, 'changes': []}, self.context(), '1 to 20 changes'),
                                     ({**edit, 'changes': [{'find': 'week 2', 'replace': 'week 3', 'style': 'bold'}]}, self.context(), 'A change is'),
                                     ({**edit, 'label': 'Send it'}, self.context(), 'button labels'),
                                     ({**create, 'body': ' '}, self.context(), 'body'),
                                     ({**create, 'account_id': 'acme-gmail'}, self.context(), 'one of your Docs connections'),
                                     (edit, self.context(snapshot='The doc could not be read (docs_google)'), 'Nothing was saved')):
            with self.assertRaises(ValueError, msg=value) as caught:
                w.validate(value, context)
            self.assertIn(said, str(caught.exception))

    def test_a_placeholder_in_new_text_is_refused_like_in_any_draft(self):
        value = {'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'T', 'body': 'Hi [NAME]'}
        action = n.validate(value, {'accounts': [ACCOUNT]}, ['acme-docs'], doc_write_context=self.context())
        self.assertIn('placeholder', ' '.join(n.check(action)))
        edit = n.validate({'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1', 'changes': [{'find': 'week 2', 'replace': 'week [date]'}]},
                          {'accounts': [ACCOUNT]}, ['acme-docs'], doc_write_context=self.context())
        self.assertIn('placeholder', ' '.join(n.check(edit)))

    def test_never_retried_and_voice_reads_all_of_it(self):
        self.assertNotIn('doc_write', n.SEND_KINDS)  # only sends are tried again
        self.assertIn('doc_write', n.APPROVE_KINDS)
        action = w.validate({'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1', 'changes': [{'find': 'week 2', 'replace': 'week 3'}]},
                            self.context())
        self.assertIn('After: Launch in week 3.', w.spoken(action))
        self.assertEqual(talk_live.question(action, 'Robin'), 'Save these changes to “Q4 plan”?')
        self.assertEqual(talk_live.question({'kind': 'doc_write', 'op': 'create'}, ''), 'Create this doc?')


class GoogleRequests(unittest.TestCase):
    def test_replace_insert_and_append_land_where_the_owner_saw_them(self):
        doc = gdoc(['Q4 plan', 'Launch in week 2, then review.', 'Budget: 10k'])
        changes = w.resolve(w.google_snapshot(doc, 'doc1'), [
            {'find': 'week 2', 'replace': 'week 3'}, {'find': 'review', 'replace': 'a retro'},
            {'after': 'Q4 plan', 'insert': '## Goals\nShip it'}, {'append': 'Owner: ops'}, {'find': '10k', 'replace': ''}])
        paragraphs, styles = apply(doc, w.google_requests(doc, changes))
        self.assertEqual(paragraphs, ['Q4 plan', 'Goals', 'Ship it', 'Launch in week 3, then a retro.', 'Budget: ', 'Owner: ops'])
        self.assertEqual(styles, [('Owner: ops', 'NORMAL_TEXT'), ('Goals', 'HEADING_2'), ('Ship it', 'NORMAL_TEXT')])

    def test_utf16_indexes(self):
        doc = gdoc(['Ship 🚀 now', 'Next'])
        requests = w.google_requests(doc, w.resolve(w.google_snapshot(doc, 'doc1'), [{'find': 'now', 'replace': 'today'}]))
        self.assertEqual(requests[0], {'deleteContentRange': {'range': {'startIndex': 9, 'endIndex': 12}}})

    def test_a_paragraph_with_suggestions_or_a_table_is_left_alone(self):
        doc = gdoc(['Plain'])
        doc['body']['content'].append({'startIndex': 7, 'endIndex': 20, 'paragraph': {'elements': [
            {'startIndex': 7, 'endIndex': 20, 'textRun': {'content': 'Suggested it\n', 'suggestedInsertionIds': ['s1']}}]}})
        doc['body']['content'].append({'startIndex': 20, 'endIndex': 40, 'table': {}})
        snap = w.google_snapshot(doc, 'doc1')
        self.assertEqual([(p['text'], p['editable']) for p in snap['paragraphs']], [('Plain', True), ('Suggested it', False)])
        with self.assertRaises(ValueError):
            w.resolve(snap, [{'find': 'Suggested', 'replace': 'x'}])


class Word(unittest.TestCase):
    def test_a_new_doc_is_the_same_bytes_each_time_and_reads_back(self):
        data = w.docx_new('# Plan\nIntro & more\n## Next\nShip it')
        self.assertEqual(data, w.docx_new('# Plan\nIntro & more\n## Next\nShip it'))
        self.assertEqual(texts(w.docx_snapshot({'cTag': 'c1', 'name': 'Plan.docx'}, data, 'd1!i1')), ['Plan', 'Intro & more', 'Next', 'Ship it'])
        self.assertIn(b'Heading2', zipfile.ZipFile(io.BytesIO(data)).read('word/document.xml'))
        self.assertEqual(w.word_name('Q4: plan/notes?'), w.word_name('Q4: plan/notes?', 1))
        self.assertNotIn('/', w.word_name('Q4: plan/notes?'))

    def test_an_edit_changes_only_its_text_and_keeps_the_rest_of_the_file(self):
        data = word('<w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>R&amp;D plan</w:t></w:r>',
                    '<w:r><w:rPr><w:b/></w:rPr><w:t>Launch in </w:t></w:r><w:r><w:t>week 2.</w:t></w:r>',
                    '<w:r><w:t>Budget</w:t></w:r>')
        snap = w.docx_snapshot({'cTag': 'c1', 'name': 'Plan.docx', 'webUrl': 'https://x.example/plan'}, data, 'd1!i1')
        self.assertEqual((texts(snap), snap['title'], snap['version']), (['R&D plan', 'Launch in week 2.', 'Budget'], 'Plan', 'c1'))
        changes = w.resolve(snap, [{'find': 'R&D', 'replace': 'Research <and> development'}, {'find': 'in week 2', 'replace': 'in week 3'},
                                   {'after': 'Launch in', 'insert': '### Why\nIt is ready'}, {'append': 'Owner: ops'}])
        edited = w.docx_edit(data, changes)
        self.assertEqual(texts(w.docx_snapshot({'cTag': 'c2', 'name': 'Plan.docx'}, edited, 'd1!i1')),
                         ['Research <and> development plan', 'Launch in week 3.', 'Why', 'It is ready', 'Budget', 'Owner: ops'])
        before, after = zipfile.ZipFile(io.BytesIO(data)), zipfile.ZipFile(io.BytesIO(edited))
        self.assertEqual(before.namelist(), after.namelist())
        self.assertEqual(after.read('word/styles.xml'), b'<w:styles>keep me</w:styles>')
        xml = after.read('word/document.xml').decode()
        self.assertIn('<w:pStyle w:val="Title"/>', xml)
        self.assertIn('<w:b/>', xml)  # the run's own formatting stays
        self.assertTrue(xml.index('Owner: ops') < xml.index('<w:sectPr/>'))

    def test_tracked_changes_fields_and_dtds_are_left_alone(self):
        data = word('<w:r><w:t>Plain</w:t></w:r>', '<w:ins w:id="1"><w:r><w:t>tracked</w:t></w:r></w:ins><w:r><w:t> text</w:t></w:r>')
        snap = w.docx_snapshot({'cTag': 'c1', 'name': 'x.docx'}, data, 'd!i')
        self.assertEqual([p['editable'] for p in snap['paragraphs']], [True, False])
        with self.assertRaises(ValueError):
            w.resolve(snap, [{'find': 'text', 'replace': 'x'}])
        bomb = io.BytesIO()
        with zipfile.ZipFile(bomb, 'w') as z:
            z.writestr('word/document.xml', '<!DOCTYPE d [<!ENTITY a "aaaa">]><w:document xmlns:w="urn:w"><w:body/></w:document>')
        with self.assertRaises(w.DocxError):
            w.docx_snapshot({'cTag': 'c1', 'name': 'x.docx'}, bomb.getvalue(), 'd!i')


class GoogleWrites(GoogleFake):
    """GoogleFake, plus the Docs API's batchUpdate (with its revision check) and Drive's id and upload calls."""

    def __init__(self, test):
        super().__init__(test)
        self.doc, self.files, self.upload_fails = None, {}, False

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        method = request.get_method()
        if url.netloc in ('docs.googleapis.com', 'www.googleapis.com') and self.doc is not None or url.path.startswith('/upload/') \
                or 'generateIds' in url.path or url.path.startswith('/drive/v3/files/new'):
            self.requests.append((method, url.path, dict(urllib.parse.parse_qsl(url.query))))
            if url.path == '/v1/documents/doc1' and method == 'GET':
                return Response(json.dumps(self.doc).encode())
            if url.path == '/v1/documents/doc1:batchUpdate' and method == 'POST':
                body = json.loads(request.data)
                if body['writeControl']['requiredRevisionId'] != self.doc['revisionId']:
                    raise urllib.error.HTTPError(request.full_url, 400, 'stale', {}, io.BytesIO(b''))
                self.batch = body['requests']
                paragraphs, _ = apply(self.doc, body['requests'])
                self.doc = gdoc(paragraphs, 'r' + str(int(self.doc['revisionId'][1:]) + 1), self.doc['title'])
                return Response(json.dumps({'writeControl': {'requiredRevisionId': self.doc['revisionId']}}).encode())
            if url.path == '/drive/v3/files/generateIds':
                return Response(json.dumps({'ids': ['new1']}).encode())
            if url.path == '/upload/drive/v3/files' and method == 'POST':
                self.test.assertTrue(request.get_header('Content-type').startswith('multipart/related'))
                meta = json.loads(request.data.split(b'\r\n\r\n', 1)[1].split(b'\r\n', 1)[0])
                self.files[meta['id']] = request.data
                if self.upload_fails:
                    raise urllib.error.HTTPError(request.full_url, 502, 'gateway', {}, io.BytesIO(b''))
                return Response(json.dumps({'id': meta['id'], 'name': meta['name']}).encode())
            if url.path.startswith('/drive/v3/files/new'):
                if url.path.rsplit('/', 1)[1] in self.files:
                    return Response(json.dumps({'id': 'new1', 'trashed': False}).encode())
                raise urllib.error.HTTPError(request.full_url, 404, 'no', {}, io.BytesIO(b''))
            raise AssertionError('unexpected request ' + request.full_url)
        return super().respond(request, data, timeout)


class Google(unittest.TestCase):
    """From a to-do: drafted against the doc as it is, seen, confirmed, then one write into that same version."""
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'google_broker': {'url': 'https://cp.example/api/google/token'},
                       'accounts': [GMAIL, ACCOUNT]}
        mail_grants.put(self.config, 'google', OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = GoogleWrites(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        patch.object(a.CONNECTOR_HELPERS, 'credential', lambda config, name: 'machine-token').start()
        self.addCleanup(patch.stopall)
        docs.sync(self.store, self.config, ACCOUNT, helpers_for())
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM events WHERE kind='docs.comment'")]
        self.sid = self.store.suggest('doc-task', 'Move the launch', 'Robin asks to move the launch.', ids)['id']
        self.fake.doc = gdoc(['Q4 plan', 'Launch in week 2.'])

    def app(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        return app

    def save(self, **draft):
        action = {'kind': 'doc_write', 'op': 'edit', 'file_id': 'doc1', 'changes': [{'find': 'week 2', 'replace': 'week 3'}], **draft}
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Edit ready.', 'next_action': action})

    def transport(self):
        return n.ActionTransport(None, None, doc_writes=a.docs_write_transport(self.config))

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM action_jobs ORDER BY created_at DESC LIMIT 1').fetchone())

    def confirm(self, action):
        with self.assertRaises(ValueError):  # the agent can't approve it
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'x'})
        for key in ('owner-approval', 'second-click'):
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': key},
                              owner_dashboard=True)

    def batches(self):
        return [r for r in self.fake.requests if str(r[1] or '').endswith(':batchUpdate')]

    def test_reading_only_means_the_change_stays_text(self):
        self.decide('accept')
        with self.assertRaises(ValueError) as caught:
            self.save()
        self.assertIn('Allow edits', str(caught.exception))
        self.assertEqual(a.docs_write_offered({'manage_url': 'https://cp.example/account'}, 'google'), False)

    def test_an_approved_edit_is_written_once_into_the_version_the_owner_saw(self):
        self.fake.granted.add(docs.REPLY_SCOPE)
        self.decide('accept')
        self.save(last=True)  # the edit is the whole to-do: done once it is in
        action = self.row()['next_action']
        self.assertEqual((action['kind'], action['version']), ('doc_write', 'r1'))
        self.assertEqual(self.app().talk_draft(self.sid, action['revision']), action)  # voice: the same pinned revision
        self.app().action_step(self.transport())
        self.assertEqual(self.batches(), [])  # nothing before the owner's OK
        self.confirm(action)
        self.app().action_step(self.transport())
        self.app().action_step(self.transport())
        self.assertEqual(len(self.batches()), 1)
        self.assertEqual(texts(w.google_snapshot(self.fake.doc, 'doc1')), ['Q4 plan', 'Launch in week 3.'])
        self.assertEqual(self.job()['status'], 'sent')
        self.assertIn('✓ Changes saved in the doc', str(a.card(self.row())))
        broker = {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}
        self.assertTrue(broker <= {docs.READ_SCOPE, docs.REPLY_SCOPE}, broker)  # never Gmail's

    def test_a_doc_that_changed_after_the_draft_is_not_written(self):
        self.fake.granted.add(docs.REPLY_SCOPE)
        self.decide('accept')
        self.save()
        action = self.row()['next_action']
        self.fake.doc = gdoc(['Q4 plan', 'Launch in week 2.', 'Someone added this.'], 'r7')
        self.confirm(action)
        self.app().action_step(self.transport())
        self.assertEqual(self.batches(), [])
        self.assertEqual(self.job()['status'], 'blocked')  # checked before the write: nothing went out
        self.assertIn('The doc changed since this was drafted', str(a.card(self.row())))

    def test_a_new_doc_with_drive_file_only_and_an_unclear_upload_is_never_sent_twice(self):
        self.fake.granted.add(docs.FILE_SCOPE)
        acct = next(x for x in self.config['accounts'] if x['id'] == 'acme-docs')
        self.assertEqual(docs.writes_on(self.config, acct, a.CONNECTOR_HELPERS), {'create'})
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Doc ready.', 'next_action': {
            'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'Launch notes', 'body': '# Launch\nWeek 3.'}})
        action = self.row()['next_action']
        self.confirm(action)
        self.fake.upload_fails = True  # it was created, but the answer got lost
        self.app().action_step(self.transport())
        uploads = [r for r in self.fake.requests if r[1] == '/upload/drive/v3/files']
        self.assertEqual(len(uploads), 1)
        self.assertEqual(self.job()['status'], 'uncertain')
        self.assertIn(b'<h1>Launch</h1><p>Week 3.</p>', self.fake.files['new1'])
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET retry_at='2000-01-01T00:00:00+00:00'")
        self.app().action_step(self.transport())
        self.assertEqual(len([r for r in self.fake.requests if r[1] == '/upload/drive/v3/files']), 1)
        self.assertEqual((self.job()['status'], self.job()['message_id']), ('sent', 'docwrite:new1'))
        broker = {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}
        self.assertNotIn(docs.REPLY_SCOPE, broker)


    def test_a_doc_with_a_step_after_it_keeps_the_to_do_open_for_that_step(self):
        """2026-10-30: a doc made for a partner closed its to-do, though the reply with its link still had to go out.
        Only last:true closes it; otherwise the to-do carries on with the step after the doc, drafted for the owner."""
        self.fake.granted.add(docs.FILE_SCOPE)
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Doc ready in Google Docs.', 'next_action': {
            'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'Launch notes', 'body': 'Week 3.',
            'then': 'Reply to Robin with the link'}})
        action = self.row()['next_action']
        self.assertEqual(action['then'], 'Reply to Robin with the link')
        self.confirm(action)
        self.app().action_step(self.transport())
        self.assertEqual(self.job()['status'], 'sent')
        row = self.row()
        self.assertEqual(row['status'], 'accepted')  # not done: the reply is still to do
        with self.store.connect() as db:
            prep = db.execute('SELECT status,decision_id,job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()
            step = db.execute('SELECT choice,feedback,source FROM decisions WHERE id=?', (prep['decision_id'],)).fetchone()
            closed = db.execute("SELECT count(*) FROM decisions WHERE suggestion_id=? AND choice='complete'", (self.sid,)).fetchone()[0]
        self.assertEqual((prep['status'], step['choice'], step['source'], closed), ('queued', 'continue', 'assistant', 0))
        self.assertIn('Created “Launch notes” in Google Docs (https://docs.google.com/document/d/new1/edit)', step['feedback'])
        self.assertIn('Reply to Robin with the link', step['feedback'])
        self.assertIn('never send it', step['feedback'])

    def test_last_true_closes_the_to_do_once_the_doc_is_made(self):
        self.fake.granted.add(docs.FILE_SCOPE)
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Doc ready.', 'next_action': {
            'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'Launch notes', 'body': 'Week 3.', 'last': True}})
        self.confirm(self.row()['next_action'])
        self.app().action_step(self.transport())
        self.assertEqual(self.row()['status'], 'completed')

    def test_the_to_do_names_the_place_the_doc_goes(self):
        self.fake.granted.add(docs.FILE_SCOPE)
        self.decide('accept')
        with self.assertRaises(ValueError) as caught:
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Your notes are ready to put in Word.', 'next_action': {
                'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'Launch notes', 'body': 'Week 3.', 'last': True}})
        self.assertIn('name Google Docs', str(caught.exception))


class Microsoft(unittest.TestCase):
    """Word on OneDrive and SharePoint: Files.ReadWrite.All only after Allow edits; the file put back with If-Match."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'microsoft_broker': {'url': 'https://cp.example/api/microsoft/token'},
                       'accounts': [OUTLOOK, ACCOUNT]}
        mail_grants.put(self.config, 'microsoft', OWNER, 'refresh-1')
        import ms_graph
        ms_graph._tokens.clear()
        self.granted = ['Files.Read.All', 'Files.ReadWrite.All']
        self.requests, self.file, self.tag, self.created = [], word('<w:r><w:t>Launch in week 2.</w:t></w:r>'), 1, {}
        self.race = False
        patch('urllib.request.OpenerDirector.open', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)
        self.transport = w.DocWriteTransport(self.config, docs, helpers_for())

    def item(self):
        return {'id': 'i1', 'name': 'SOW.docx', 'size': len(self.file), 'cTag': f'c{self.tag}', 'eTag': f'e{self.tag}',
                'webUrl': 'https://acme-my.sharepoint.com/sow', '@microsoft.graph.downloadUrl': 'https://acme-my.sharepoint.com/download/sow'}

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        method = request.get_method()
        if url.netloc == 'cp.example':
            body = json.loads(request.data)
            self.requests.append(('BROKER', body.get('scope')))
            if not body.get('scope'):
                return Response(json.dumps({'scopes': self.granted}).encode())
            return Response(json.dumps({'access_token': 'access', 'expires_in': 3600}).encode())
        if url.netloc == 'acme-my.sharepoint.com':
            return Response(self.file)
        self.requests.append((method, urllib.parse.unquote(url.path)))
        if url.path == '/v1.0/drives/d1/items/i1' and method == 'GET':
            return Response(json.dumps(self.item()).encode())
        if url.path == '/v1.0/drives/d1/items/i1/content' and method == 'PUT':
            if self.race or request.get_header('If-match') != f'e{self.tag}':
                raise urllib.error.HTTPError(request.full_url, 412, 'precondition', {}, io.BytesIO(b''))
            self.file, self.tag = request.data, self.tag + 1
            return Response(json.dumps(self.item()).encode())
        name = urllib.parse.unquote(url.path).removeprefix('/v1.0/me/drive/root:/')
        if method == 'GET' and name in self.created:
            return Response(json.dumps({'id': 'n1', 'size': len(self.created[name]), 'parentReference': {'driveId': 'd1'}}).encode())
        if method == 'GET':
            raise urllib.error.HTTPError(request.full_url, 404, 'no', {}, io.BytesIO(b''))
        if method == 'PUT' and name.endswith(':/content'):
            self.assertEqual(dict(urllib.parse.parse_qsl(url.query)), {'@microsoft.graph.conflictBehavior': 'fail'})
            self.created[name.removesuffix(':/content')] = request.data
            return Response(json.dumps({'id': 'n1', 'parentReference': {'driveId': 'd1'}}).encode())
        raise AssertionError('unexpected request ' + request.full_url)

    def edit(self):
        context = w.context(self.config, docs, helpers_for(), {'d1!i1': {'account_id': 'acme-docs', 'doc_title': 'SOW', 'provider': 'microsoft'}},
                            {'kind': 'doc_write', 'op': 'edit', 'file_id': 'd1!i1'})
        return w.validate({'kind': 'doc_write', 'op': 'edit', 'file_id': 'd1!i1', 'changes': [{'find': 'week 2', 'replace': 'week 3'}]}, context)

    def test_without_allow_edits_nothing_is_offered_to_write(self):
        self.granted = ['Files.Read.All']
        self.assertEqual(docs.writes_on(self.config, ACCOUNT, helpers_for()), set())
        with self.assertRaises(ValueError):
            self.edit()
        self.assertTrue(a.docs_write_offered({}, 'microsoft'))
        self.assertTrue(a.docs_write_offered({'manage_url': 'https://cp.example/a', 'docs_write_consent': ['microsoft']}, 'microsoft'))
        self.assertFalse(a.docs_write_offered({'manage_url': 'https://cp.example/a'}, 'microsoft'))

    def test_an_edit_puts_the_file_back_only_onto_the_version_it_read(self):
        action = self.edit()
        self.assertEqual(action['version'], 'c1')
        self.transport.preflight(action)
        self.assertEqual(self.transport.send(action, {}), {'message_id': 'docwrite:d1!i1'})
        self.assertEqual(texts(w.docx_snapshot(self.item(), self.file, 'd1!i1')), ['Launch in week 3.'])
        self.assertIn(('BROKER', 'Files.ReadWrite.All'), self.requests)
        with self.assertRaises(ValueError):  # the same approval again: the doc moved on
            self.transport.preflight(action)
        self.assertEqual(self.transport.send(action, {}), {'rejected': 409})
        self.assertEqual(len([r for r in self.requests if r[0] == 'PUT']), 1)

    def test_a_change_between_the_read_and_the_put_is_refused(self):
        action = self.edit()
        self.race = True
        self.assertEqual(self.transport.send(action, {}), {'rejected': 412})
        self.assertIn('The doc changed since this was drafted', w.failed(action, 412))
        self.assertEqual(texts(w.docx_snapshot(self.item(), self.file, 'd1!i1')), ['Launch in week 2.'])

    def test_a_new_word_doc_never_overwrites_a_file(self):
        self.created['Plan.docx'] = b'someone else'
        action = w.validate({'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-docs', 'title': 'Plan', 'body': 'Hello'},
                            {'accounts': {'acme-docs': {'provider': 'microsoft', 'writes': ['create', 'edit']}}})
        self.transport.preflight(action)
        self.assertEqual(action['proof'], {'name': 'Plan (2).docx'})
        self.assertEqual(self.transport.send(action, {}), {'message_id': 'docwrite:d1!n1'})
        self.assertEqual(self.created['Plan.docx'], b'someone else')
        self.assertEqual(self.transport.reconcile(action, {}), {'message_id': 'docwrite:d1!n1'})


WORK = {'boundaries': ['work:Acme'], 'emails': [OWNER]}


class Area(unittest.TestCase):
    """A doc goes only where the to-do lives: its own area (Work at that company, or Personal), and the conversation's own
    address when that one can. 2026-10-30: a Work to-do's doc went to a personal Hotmail OneDrive."""

    def context(self, *targets, area=WORK):
        return {'accounts': dict(targets), 'area': area}

    HOTMAIL = ('home-docs', {'name': 'me@hotmail.example', 'email': 'me@hotmail.example', 'provider': 'microsoft',
                             'boundary': 'personal:me', 'writes': ['create', 'edit']})
    GOG = ('acme-gmail', {'name': OWNER, 'email': OWNER, 'provider': 'google', 'boundary': 'work:Acme', 'writes': ['create']})

    def create(self, account_id, context):
        return w.validate({'kind': 'doc_write', 'op': 'create', 'account_id': account_id, 'title': 'Plan', 'body': 'Hi'}, context)

    def test_never_another_areas_account(self):
        with self.assertRaises(ValueError) as caught:
            self.create('home-docs', self.context(self.HOTMAIL, self.GOG))
        self.assertIn('Personal, not this to-do’s area (Work at Acme)', str(caught.exception))
        self.assertIn('Use acme-gmail instead', str(caught.exception))
        self.assertEqual(self.create('acme-gmail', self.context(self.HOTMAIL, self.GOG))['provider'], 'google')

    def test_none_in_the_area_says_so_plainly(self):
        with self.assertRaises(ValueError) as caught:
            self.create('home-docs', self.context(self.HOTMAIL))
        self.assertIn('Connect Google Docs or Microsoft Word for Work', str(caught.exception))
        # a personal to-do may use it
        self.assertEqual(self.create('home-docs', self.context(self.HOTMAIL, area={'boundaries': ['personal:phone'], 'emails': []}))['provider'],
                         'microsoft')

    def test_the_conversations_own_address_first(self):
        other = ('acme-docs', {'name': 'docs@acme.example', 'email': 'docs@acme.example', 'provider': 'microsoft',
                               'boundary': 'work', 'writes': ['create']})
        with self.assertRaises(ValueError) as caught:
            self.create('acme-docs', self.context(other, self.GOG))
        self.assertIn('put the doc in acme-gmail', str(caught.exception))
        self.assertTrue(w.fits('work', WORK) and w.fits('work:Acme', {'boundaries': ['work']}))
        self.assertFalse(w.fits('work:Other', WORK))

    def test_area_of_a_to_do_and_wording(self):
        config = {'accounts': [GMAIL, {'id': 'phone', 'service': 'android', 'boundary': 'personal:phone'}]}
        self.assertEqual(w.area(config, ['acme-gmail']), WORK)
        word = {'kind': 'doc_write', 'op': 'create', 'provider': 'microsoft', 'title': 'Plan', 'body': 'x'}
        self.assertEqual(w.wording([word], ['Needs you: approve creating the Google Doc.']),
                         ['the doc goes to Word, but the to-do says “Google Doc”: name Word'])
        self.assertEqual(w.wording([word], ['Ready to put in Word.']), [])
        self.assertTrue(w.wording([{**word, 'provider': 'google'}], ['A new Word doc is ready']))
        self.assertEqual(w.wording([{**word, 'provider': 'google'}], ['Ready to put in Google Docs. A word on pricing.']), [])

    def test_the_title_shows_once(self):
        action = {'op': 'create', 'provider': 'microsoft', 'title': 'Salesflare inclusion for Partner',
                  'body': '# Salesflare inclusion  for partner\nFor the guide\n## Search title'}
        self.assertEqual(w.preview(action), 'New doc in Word: “Salesflare inclusion for Partner”\n\nFor the guide\n## Search title')
        self.assertEqual(w.untitled({**action, 'body': '# Other\nx'}), '# Other\nx')


class GogDocs(unittest.TestCase):
    """A Google Doc through the owner's own gog sign-in for Gmail: only with the drive scope it already has, reads
    --readonly, the writes --allow-write, the text written once into the empty doc made under the id generated first."""

    def setUp(self):
        self.account = {'id': 'acme-gmail', 'email': OWNER, 'transport': 'gog', 'client': 'acme', 'boundary': 'work:Acme'}
        self.config = {'gog': '/usr/bin/gog-fake', 'accounts': [self.account]}
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, credential=lambda config, name: 'pw')
        self.scopes = ['email', docs.REPLY_SCOPE, 'https://www.googleapis.com/auth/gmail.modify']
        self.calls, self.doc, self.created, self.fail_fill = [], None, {}, False
        patch('subprocess.run', side_effect=self.gog).start()
        self.addCleanup(patch.stopall)

    def gog(self, command, env=None, **_):
        self.assertEqual(env['GOG_KEYRING_PASSWORD'], 'pw')
        if command[1:3] == ['auth', 'list']:
            return types.SimpleNamespace(returncode=0, stdout=json.dumps({'accounts': [{'email': OWNER, 'client': 'acme', 'scopes': self.scopes}]}), stderr='')
        api, version, method = command[3:6]
        flag = lambda name: command[command.index(name) + 1]
        body = json.loads(Path(flag('--body')[1:]).read_text()) if '--body' in command else None
        self.calls.append((method, flag('--scope'), '--allow-write' in command, '--readonly' in command, flag('--account')))
        out = {}
        if method == 'drive.files.generateIds':
            out = {'ids': ['g1']}
        elif method == 'drive.files.create':
            self.created[body['id']] = body
            self.doc = {'revisionId': 'r1', 'body': {'content': [{'paragraph': {'elements': [{'startIndex': 1, 'endIndex': 2, 'textRun': {'content': '\n'}}]}}]}}
            out = {'id': body['id']}
        elif method == 'docs.documents.get':
            out = self.doc
        elif method == 'docs.documents.batchUpdate':
            if self.fail_fill:
                return types.SimpleNamespace(returncode=1, stdout='', stderr='timeout')
            self.fill = body
            text = body['requests'][0]['insertText']['text']
            self.doc = {'revisionId': 'r2', 'body': {'content': [{'paragraph': {'elements': [{'startIndex': 1, 'endIndex': 2 + len(text), 'textRun': {'content': text + '\n'}}]}}]}}
        elif method == 'drive.files.get':
            out = {'id': 'g1', 'trashed': False} if 'g1' in self.created else None
            if out is None:
                return types.SimpleNamespace(returncode=1, stdout='{"error":{"message":"{\\"code\\": 404}"}}', stderr='404')
        return types.SimpleNamespace(returncode=0, stdout=json.dumps(out), stderr='')

    def test_a_new_google_doc_with_the_gog_sign_in(self):
        self.assertTrue(docs.gog_google(self.account))
        found = w.targets(self.config, docs, self.helpers)
        self.assertEqual(found['acme-gmail']['provider'], 'google')
        self.assertEqual(found['acme-gmail']['writes'], ['create'])
        context = w.context(self.config, docs, self.helpers, {}, {'kind': 'doc_write', 'op': 'create'}, WORK)
        action = w.validate({'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-gmail', 'title': 'Plan',
                             'body': '# Plan\nWeek 3.', 'then': 'Reply with the link'}, context)
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        transport.preflight(action)
        self.assertEqual(transport.send(action, {}), {'message_id': 'docwrite:g1', 'url': 'https://docs.google.com/document/d/g1/edit'})
        self.assertEqual(self.created['g1'], {'id': 'g1', 'name': 'Plan', 'mimeType': docs.DOC_MIME})
        self.assertEqual(self.fill['requests'][0]['insertText']['text'], 'Plan\nWeek 3.')
        self.assertEqual(self.fill['writeControl'], {'requiredRevisionId': 'r1'})
        for method, scope, write, readonly, account in self.calls:
            self.assertEqual((scope, account), (docs.REPLY_SCOPE, OWNER))  # only the drive scope it has, never Gmail's
            self.assertEqual((write, readonly), (method in ('drive.files.create', 'docs.documents.batchUpdate'),
                                                 method not in ('drive.files.create', 'docs.documents.batchUpdate')))

    def test_an_unclear_fill_is_finished_once_and_a_sign_in_without_drive_is_no_place(self):
        context = w.context(self.config, docs, self.helpers, {}, {'kind': 'doc_write', 'op': 'create'}, WORK)
        action = w.validate({'kind': 'doc_write', 'op': 'create', 'account_id': 'acme-gmail', 'title': 'Plan', 'body': 'Week 3.'}, context)
        transport = w.DocWriteTransport(self.config, docs, self.helpers)
        transport.preflight(action)
        self.fail_fill = True
        self.assertEqual(transport.send(action, {}), {})  # unclear: never written again by send
        self.fail_fill = False
        self.assertEqual(transport.reconcile(action, {})['message_id'], 'docwrite:g1')
        self.assertEqual(transport.reconcile(action, {})['message_id'], 'docwrite:g1')
        self.assertEqual(len([c for c in self.calls if c[0] == 'docs.documents.batchUpdate']), 2)  # the failed one, then once
        self.assertEqual(len([c for c in self.calls if c[0] == 'drive.files.create']), 1)
        self.scopes = ['email', 'https://www.googleapis.com/auth/gmail.modify']
        self.assertEqual(w.targets(self.config, docs, self.helpers), {})


if __name__ == '__main__':
    unittest.main()

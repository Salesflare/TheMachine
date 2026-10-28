"""Docs as a connection (connectors/docs.py): Google Docs and Word, faked end to end. Nothing reaches Google, Microsoft or a
broker. It reads with its own scope only (drive.readonly, Files.Read.All), never Gmail's, and writes one thing: a reply
to a comment, only after the owner's Post on that exact text, only with the separate reply consent."""
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
import graph
import mail_grants
import next_actions as n
import onboarding
import shared_graph
from test_connectors import a, Response
import test_ux as ux

OWNER = 'owner@acme.example'
NOW = '2026-10-27T10:00:00+00:00'
GMAIL = {'id': 'acme-gmail', 'service': 'gmail', 'email': OWNER, 'transport': 'broker', 'boundary': 'work:Acme'}
OUTLOOK = {'id': 'acme-outlook', 'service': 'outlook', 'email': OWNER, 'transport': 'broker', 'boundary': 'work:Acme'}
ACCOUNT = {**docs.SETUP['account'], 'id': 'acme-docs', 'email': OWNER, 'boundary': 'work:Acme'}
OWNED = {'id': 'doc1', 'name': 'Q4 plan', 'mimeType': docs.DOC_MIME, 'webViewLink': 'https://docs.google.com/document/d/doc1/edit',
         'modifiedTime': '2026-10-27T09:00:00.000Z', 'owners': [{'displayName': 'Owner', 'me': True}],
         'lastModifyingUser': {'displayName': 'Robin Reviewer', 'emailAddress': 'robin@partner.example'}}
SHARED = {'id': 'doc2', 'name': 'Partner brief', 'mimeType': docs.DOC_MIME, 'webViewLink': 'https://docs.google.com/document/d/doc2/edit',
          'modifiedTime': '2026-10-27T08:00:00.000Z', 'sharedWithMeTime': '2026-10-27T07:00:00.000Z',
          'sharingUser': {'displayName': 'Sam Sharer', 'emailAddress': 'sam@partner.example'},
          'owners': [{'displayName': 'Sam Sharer', 'emailAddress': 'sam@partner.example'}]}


def comment(cid, author, text, when='2026-10-27T09:30:00.000Z', replies=(), html=None):
    return {'id': cid, 'author': author, 'content': text, 'htmlContent': html or text, 'createdTime': when, 'modifiedTime': when,
            'quotedFileContent': {'value': 'Launch in week 2'}, 'replies': list(replies)}


ROBIN = {'displayName': 'Robin Reviewer', 'emailAddress': 'robin@partner.example'}
SAM = {'displayName': 'Sam Sharer', 'emailAddress': 'sam@partner.example'}


class GoogleFake:
    """Google's APIs and the broker, faked. Records every request; only the broker sees a refresh token."""

    def __init__(self, test):
        self.test, self.requests, self.granted = test, [], {docs.READ_SCOPE}
        self.comments = {'doc1': [comment('c1', ROBIN, 'Can we move this to week 3?')],
                         'doc2': [comment('c2', SAM, '+owner@acme.example can you check the numbers?',
                                          html='<a href="mailto:owner@acme.example">+owner@acme.example</a> can you check the numbers?'),
                                  comment('c3', SAM, 'Note to self')]}
        self.suggestions = {'s1': 'week 3'}
        self.replies = []

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        query = dict(urllib.parse.parse_qsl(url.query))
        body = json.loads(request.data) if request.data else None
        if url.netloc == 'cp.example':
            self.requests.append(('BROKER', body.get('scope'), None))
            if not body.get('scope'):
                return Response(json.dumps({'scopes': sorted(self.granted)}).encode())
            if body['scope'] not in self.granted:
                raise urllib.error.HTTPError(request.full_url, 403, 'no', {}, io.BytesIO(b''))
            self.test.assertEqual(body['refresh_token'], 'refresh-1')
            return Response(json.dumps({'access_token': 'access', 'expires_in': 3600}).encode())
        self.test.assertIn(url.netloc, ('www.googleapis.com', 'docs.googleapis.com'))
        self.test.assertNotIn('refresh', request.full_url)
        self.requests.append((request.get_method(), url.path, query))
        if url.path == '/drive/v3/files':
            return Response(json.dumps({'files': [SHARED] if 'sharedWithMe = true and trashed' in query['q'] else [OWNED, SHARED]}).encode())
        if url.path.endswith('/comments') and request.get_method() == 'GET':
            return Response(json.dumps({'comments': self.comments[url.path.split('/')[4]]}).encode())
        if url.path == '/v1/documents/doc1':
            runs = [{'textRun': {'content': text, 'suggestedInsertionIds': [sid]}} for sid, text in self.suggestions.items()]
            return Response(json.dumps({'body': {'content': [{'paragraph': {'elements': runs}}]}}).encode())
        if url.path == '/drive/v3/files/doc1/export':
            return Response(b'Q4 plan\nLaunch in week 2.')
        if url.path == '/drive/v3/files/doc1':
            return Response(json.dumps({**OWNED}).encode())
        if url.path == '/drive/v3/files/doc1/comments/c1' and request.get_method() == 'GET':
            return Response(json.dumps({'id': 'c1', 'replies': self.replies}).encode())
        if url.path == '/drive/v3/files/doc1/comments/c1/replies' and request.get_method() == 'POST':
            self.test.assertEqual(set(body), {'content'})
            reply = {'id': 'r' + str(len(self.replies) + 1), 'author': {'me': True}, 'content': body['content'], 'createdTime': NOW}
            self.replies.append(reply)
            return Response(json.dumps(reply).encode())
        raise AssertionError('unexpected request ' + request.full_url)

    def writes(self):
        return [r for r in self.requests if r[0] == 'POST']


def helpers_for(now=NOW):
    return types.SimpleNamespace(SourceError=a.SourceError, now=lambda: now, iso=a.CONNECTOR_HELPERS.iso,
                                 credential=lambda config, name: 'machine-token' if name in ('google-broker', 'microsoft-broker') else 1 / 0)


class Google(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'google_broker': {'url': 'https://cp.example/api/google/token'},
                       'accounts': [GMAIL, ACCOUNT]}
        mail_grants.put(self.config, 'google', OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = GoogleFake(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)

    def events(self):
        with self.store.connect() as db:
            return [dict(r) | {'metadata': json.loads(r['metadata'])} for r in db.execute('SELECT * FROM events ORDER BY id')]

    def test_comments_mentions_and_shares_come_in_once_with_the_docs_scope_only(self):
        docs.sync(self.store, self.config, ACCOUNT, helpers_for())
        found = {(e['kind'], e['metadata'].get('comment_id')) for e in self.events()}
        # a comment on the owner's doc, the @mention on someone else's, the share; not a comment on another's doc that
        # doesn't mention them, and no suggestion on the first run (it only learns what is already there)
        self.assertEqual(found, {('docs.comment', 'c1'), ('docs.mention', 'c2'), ('docs.shared', None)})
        mention = next(e for e in self.events() if e['kind'] == 'docs.mention')
        self.assertEqual((mention['title'], mention['metadata']['from'], mention['metadata']['source_url']),
                         ('Partner brief', 'Sam Sharer <sam@partner.example>', 'https://docs.google.com/document/d/doc2/edit?disco=c2'))
        self.assertIn('On: “Launch in week 2”', mention['body'])
        asked = {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}
        self.assertEqual(asked, {docs.READ_SCOPE})  # never a Gmail scope, never drive (write)
        self.assertEqual(self.fake.writes(), [])
        self.assertTrue(all(r[0] in ('GET', 'BROKER') for r in self.fake.requests))
        # the next run: nothing twice, and a new suggestion on the owner's doc comes in
        self.fake.suggestions['s2'] = 'and week 4'
        docs.sync(self.store, self.config, ACCOUNT, helpers_for('2026-10-27T10:15:00+00:00'))
        suggestion = [e for e in self.events() if e['kind'] == 'docs.suggestion']
        self.assertEqual(len(self.events()), 4)
        self.assertEqual(len(suggestion), 1)
        self.assertIn('1 new suggested edit on “Q4 plan”, by Robin Reviewer', suggestion[0]['body'])
        self.assertIn('Add: and week 4', suggestion[0]['body'])

    def test_without_the_docs_consent_it_says_to_connect_google_docs(self):
        self.fake.granted = {'https://www.googleapis.com/auth/gmail.readonly'}
        with self.assertRaises(a.SourceError) as caught:
            docs.sync(self.store, self.config, ACCOUNT, helpers_for())
        self.assertEqual(caught.exception.category, 'docs_not_connected')
        self.assertEqual(self.events(), [])

    def test_only_the_owners_own_broker_sign_in(self):
        for accounts in ([{**GMAIL, 'transport': 'gog'}], [{**GMAIL, 'shared': {'fleet': 'f1'}}], []):
            config = {**self.config, 'accounts': accounts + [{**ACCOUNT, 'transport': 'gog'}]}
            with self.assertRaises(a.SourceError) as caught:
                docs.signin(config, {**ACCOUNT, 'transport': 'gog'}, helpers_for())
            self.assertEqual(caught.exception.category, 'docs_no_signin')
        self.assertEqual(onboarding.missing({'accounts': []}, {**ACCOUNT, 'transport': 'gog'}), 'no Google or Microsoft sign-in for this address yet')
        self.assertEqual(onboarding.missing(self.config, ACCOUNT), '')

    def test_reading_a_docs_text(self):
        found = docs.read_text(self.config, ACCOUNT, 'doc1', helpers_for())
        self.assertEqual((found['title'], found['text']), ('Q4 plan', 'Q4 plan\nLaunch in week 2.'))
        export = next(r for r in self.fake.requests if r[1] == '/drive/v3/files/doc1/export')
        self.assertEqual(export[2], {'mimeType': 'text/plain'})

    def test_replies_need_the_separate_reply_consent(self):
        self.assertFalse(docs.replies_on(self.config, ACCOUNT, helpers_for()))
        self.fake.granted.add(docs.REPLY_SCOPE)
        self.assertTrue(docs.replies_on(self.config, ACCOUNT, helpers_for()))
        self.assertFalse(docs.replies_on(self.config, {**ACCOUNT, 'shared': {'fleet': 'f1'}}, helpers_for()))
        self.assertFalse(docs.replies_on({**self.config, 'accounts': [OUTLOOK]}, {**ACCOUNT, 'provider': 'microsoft'}, helpers_for()))


def docx(comments=(), changes=(), mention=None):
    """A small .docx: its comments (with a mailto link for an @mention) and tracked changes."""
    w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    body = ''.join(f'<w:ins w:id="{i}" w:author="{who}" w:date="2026-10-27T09:00:00Z"><w:r><w:t>{text}</w:t></w:r></w:ins>'
                   for i, who, text in changes)
    notes = ''.join(f'<w:comment w:id="{i}" w:author="{who}" w:date="2026-10-27T09:10:00Z"><w:p>'
                    + (f'<w:hyperlink r:id="rId1"><w:r><w:t>@Owner</w:t></w:r></w:hyperlink>' if mention and i == mention else '')
                    + f'<w:r><w:t> {text}</w:t></w:r></w:p></w:comment>' for i, who, text in comments)
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w') as z:
        z.writestr('word/document.xml', f'<w:document xmlns:w="{w}"><w:body><w:p><w:r><w:t>Statement of work</w:t></w:r>{body}</w:p></w:body></w:document>')
        z.writestr('word/comments.xml', f'<w:comments xmlns:w="{w}" xmlns:r="{r}">{notes}</w:comments>')
        z.writestr('word/_rels/comments.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="hyperlink" Target="mailto:{OWNER}" TargetMode="External"/></Relationships>')
    return data.getvalue()


class Microsoft(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'microsoft_broker': {'url': 'https://cp.example/api/microsoft/token'},
                       'accounts': [OUTLOOK, ACCOUNT]}
        mail_grants.put(self.config, 'microsoft', OWNER, 'refresh-1')
        import ms_graph
        ms_graph._tokens.clear()
        self.requests, self.changes = [], []
        self.file = docx(comments=[('0', 'Robin Reviewer', 'Is this final?')], changes=[('1', 'Robin Reviewer', 'net 30')])
        patch('urllib.request.OpenerDirector.open', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        query = dict(urllib.parse.parse_qsl(url.query))
        if url.netloc == 'cp.example':
            body = json.loads(request.data)
            self.requests.append(('BROKER', body.get('scope')))
            return Response(json.dumps({'access_token': 'access', 'expires_in': 3600}).encode())
        if url.netloc == 'acme-my.sharepoint.com':
            self.assertIsNone(request.get_header('Authorization'))  # a pre-signed link: no token goes along
            self.requests.append(('DOWNLOAD', url.path))
            return Response(self.file)
        self.assertEqual((url.netloc, request.get_method()), ('graph.microsoft.com', 'GET'))
        self.requests.append(('GET', url.path))
        if url.path == '/v1.0/me/drive/sharedWithMe':
            return Response(json.dumps({'value': [{'remoteItem': {
                'id': 'i9', 'name': 'Pricing.xlsx', 'webUrl': 'https://partner.sharepoint.com/x', 'parentReference': {'driveId': 'd9'},
                'lastModifiedDateTime': '2026-10-27T08:00:00Z',
                'shared': {'sharedDateTime': '2026-10-27T08:00:00Z', 'sharedBy': {'user': {'displayName': 'Sam Sharer', 'email': 'sam@partner.example'}}}}}]}).encode())
        if url.path == '/v1.0/me/drive/root/delta':
            if query.get('token') == 'latest':
                return Response(json.dumps({'value': [], '@odata.deltaLink': "https://graph.microsoft.com/v1.0/me/drive/root/delta(token='t1')"}).encode())
            return Response(json.dumps({'value': self.changes, '@odata.deltaLink': "https://graph.microsoft.com/v1.0/me/drive/root/delta(token='t2')"}).encode())
        if url.path == '/v1.0/drives/d1/items/i1':
            return Response(json.dumps({'id': 'i1', 'name': 'SOW.docx', 'size': len(self.file), 'webUrl': 'https://acme-my.sharepoint.com/sow',
                                        'lastModifiedDateTime': '2026-10-27T09:20:00Z',
                                        'lastModifiedBy': {'user': {'displayName': 'Robin Reviewer', 'email': 'robin@partner.example'}},
                                        '@microsoft.graph.downloadUrl': 'https://acme-my.sharepoint.com/download/sow?tempauth=x'}).encode())
        raise AssertionError('unexpected request ' + request.full_url)

    def events(self):
        with self.store.connect() as db:
            return [dict(r) | {'metadata': json.loads(r['metadata'])} for r in db.execute('SELECT * FROM events ORDER BY id')]

    def test_shares_comments_and_tracked_changes_with_files_read_all_only(self):
        docs.sync(self.store, self.config, ACCOUNT, helpers_for())
        self.assertEqual([e['kind'] for e in self.events()], ['docs.shared'])
        self.assertEqual(self.events()[0]['metadata']['from'], 'Sam Sharer <sam@partner.example>')
        self.changes = [{'id': 'i1', 'name': 'SOW.docx', 'parentReference': {'driveId': 'd1'}}]
        docs.sync(self.store, self.config, ACCOUNT, helpers_for('2026-10-27T10:15:00+00:00'))
        kinds = [e['kind'] for e in self.events()]
        self.assertEqual(kinds, ['docs.shared', 'docs.comment', 'docs.suggestion'])
        self.assertEqual(self.events()[1]['body'], 'Robin Reviewer: Is this final?')
        self.assertIn('Add: net 30', self.events()[2]['body'])
        self.assertEqual({s for k, s in self.requests if k == 'BROKER'}, {'Files.Read.All'})
        # the same file again: nothing twice
        docs.sync(self.store, self.config, ACCOUNT, helpers_for('2026-10-27T10:30:00+00:00'))
        self.assertEqual(len(self.events()), 3)

    def test_a_word_mention_and_text(self):
        data = docx(comments=[('0', 'Sam Sharer', 'please look')], mention='0')
        self.assertEqual(docs.word_comments(data)[0]['mailto'], {OWNER})
        self.assertEqual(docs.word_text(docx(changes=[('1', 'R', ' net 30')])), 'Statement of work net 30')
        self.assertEqual(docs.link_token("https://graph.microsoft.com/v1.0/me/drive/root/delta(token='abc')"), 'abc')
        self.assertEqual(docs.link_token('https://graph.microsoft.com/v1.0/me/drive/root/delta?token=xyz&$top=5'), 'xyz')

    def test_a_word_file_with_a_dtd_or_entities_is_refused(self):
        bomb = io.BytesIO()
        with zipfile.ZipFile(bomb, 'w') as z:
            z.writestr('word/document.xml', '<?xml version="1.0"?><!DOCTYPE d [<!ENTITY a "aaaaaaaa"><!ENTITY b "&a;&a;&a;&a;">]>'
                       '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>&b;</w:t></w:r></w:p></w:body></w:document>')
        self.assertEqual(docs.word_text(bomb.getvalue()), '')
        with self.assertRaises(docs.ElementTree.ParseError):
            docs.parse_xml(b'<!DOCTYPE x SYSTEM "file:///etc/passwd"><x/>')

    def test_downloads_only_from_microsofts_file_hosts(self):
        source = docs.Microsoft(self.config, ACCOUNT, helpers_for())
        for link in ('https://evil.example/f', 'http://acme-my.sharepoint.com/f', 'https://sharepoint.com.evil.example/f'):
            with self.assertRaises(a.SourceError):
                source.download({'@microsoft.graph.downloadUrl': link, 'size': 10})


class People(unittest.TestCase):
    def test_doc_events_link_their_author_like_mail(self):
        owner = types.SimpleNamespace(emails={OWNER}, mine=lambda x: x == OWNER)
        found = graph.touches('docs.mention', {'from': 'Sam Sharer <sam@partner.example>'}, owner, set())
        self.assertEqual(found, [('email:sam@partner.example', 'Sam Sharer', graph.WEIGHTS['them'], 'them')])
        self.assertEqual(graph.touches('docs.comment', {'from': 'Robin Reviewer'}, owner, set()), [])  # no address shown: nobody to link
        self.assertEqual(graph.touches('docs.comment', {'from': OWNER}, owner, set()), [])
        self.assertEqual(graph.thread_key('docs.comment', {'file_id': 'doc1', 'comment_id': 'c1'}), ('doc:doc1:c1', True))
        self.assertIn('docs.comment', shared_graph.ITEM_KINDS)  # shared only as a project's item, under the same rules as mail
        self.assertEqual(shared_graph.ITEM_WORDS[shared_graph._source('docs.mention')], 'Doc')


class Reply(unittest.TestCase):
    """From a card: drafted, seen, Post, then the one write. Never before the owner's Post, never without the consent."""
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
        self.fake = GoogleFake(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        patch.object(a.CONNECTOR_HELPERS, 'credential', lambda config, name: 'machine-token').start()
        self.addCleanup(patch.stopall)
        docs.sync(self.store, self.config, ACCOUNT, helpers_for())
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute("SELECT id FROM events WHERE kind='docs.comment'")]
        self.sid = self.store.suggest('doc-task', 'Answer Robin', 'Robin asks to move the launch.', ids)['id']

    def app(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        return app

    def save(self, **draft):
        action = {'kind': 'doc_reply', 'label': 'Post reply', 'account_id': 'acme-docs', 'comment_id': 'c1',
                  'body': 'Week 3 works, moving it.', **draft}
        return self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})

    def transport(self):
        return n.ActionTransport(None, None, docs=n.DocReplyTransport(self.config, a.load_connector('docs'), a.CONNECTOR_HELPERS))

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM action_jobs ORDER BY created_at DESC LIMIT 1').fetchone())

    def test_without_the_reply_consent_it_stays_text(self):
        self.decide('accept')
        with self.assertRaises(ValueError) as caught:
            self.save()
        self.assertIn('Give the reply text in the body', str(caught.exception))
        self.assertEqual(self.fake.writes(), [])

    def test_an_approved_reply_is_posted_once_after_the_owners_post(self):
        self.fake.granted.add(docs.REPLY_SCOPE)
        self.decide('accept')
        for bad in ({'comment_id': 'c9'}, {'label': 'Resolve it'}, {'resolve': True}, {'body': ' '}, {'account_id': 'acme-gmail'}):
            with self.assertRaises(ValueError, msg=bad):
                self.save(**bad)
        self.save()
        action = self.row()['next_action']
        self.assertEqual(n.preview(action), 'Reply to Robin Reviewer’s comment on “Q4 plan”\n\nWeek 3 works, moving it.')
        self.app().action_step(self.transport())
        self.assertEqual(self.fake.writes(), [])  # nothing before the owner's Post
        with self.assertRaises(ValueError):  # the agent can't approve it
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'x'})
        for key in ('owner-approval', 'second-click'):
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': key},
                              owner_dashboard=True)
        self.app().action_step(self.transport())
        self.app().action_step(self.transport())
        self.assertEqual([r[1] for r in self.fake.writes()], ['/drive/v3/files/doc1/comments/c1/replies'])
        self.assertEqual(self.fake.replies[0]['content'], 'Week 3 works, moving it.')
        self.assertEqual((self.job()['status'], self.job()['message_id']), ('sent', 'doc:c1:r1'))
        self.assertIn('✓ Reply posted in the doc', str(a.card(self.row())))


if __name__ == '__main__':
    unittest.main()


class Hosted(unittest.TestCase):
    """Until a hosted Machine's account page offers the Docs consent: no Docs under Add, no card, no link to nowhere."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.hosted = {'database': str(Path(tmp.name) / 'events.sqlite'), 'manage_url': 'https://cp.example/account',
                       'google_broker': {'url': 'https://cp.example/api/google/token'}, 'accounts': [GMAIL, ACCOUNT]}

    def offered(self, config):
        return 'docs' in {s['service'] for s in onboarding.catalog(config)}

    def test_add_offers_docs_only_where_its_consent_can_be_given(self):
        self.assertFalse(self.offered(self.hosted))
        self.assertTrue(self.offered({**self.hosted, 'docs_consent': True}))
        self.assertTrue(self.offered({k: v for k, v in self.hosted.items() if k != 'manage_url'}))  # self-hosted: Add checks the sign-in

    def test_a_docs_connection_without_its_consent_has_no_card(self):
        with self.store.connect() as db:
            db.execute('INSERT INTO checkpoints(account_id,state,error,failures) VALUES(?,?,?,?)', ('acme-docs', '{}', 'docs_not_connected', 1))
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.hosted
        connectors = [c['id'] for c in app.action('status', {})['connectors']]
        self.assertIn(GMAIL['id'], connectors)
        self.assertNotIn('acme-docs', connectors)
        self.assertTrue(a.docs_unset({'service': 'docs', 'error': 'docs_not_connected'}))
        self.assertFalse(a.docs_unset({'service': 'docs', 'error': 'docs_not_connected', 'last_success': '2026-10-27T08:00:00Z'}))  # it worked: say so
        self.assertFalse(a.docs_unset({'service': 'gmail', 'error': 'docs_not_connected'}))

    def test_no_link_to_a_consent_the_account_page_does_not_offer(self):
        manage = self.hosted['manage_url']
        self.assertNotIn('account_page', a.reconnect_help(ACCOUNT, manage, a.docs_offered(self.hosted)))
        self.assertEqual(a.reconnect_help(ACCOUNT, manage, a.docs_offered({**self.hosted, 'docs_consent': True}))['account_page'],
                         'https://cp.example/account#docs')

    def test_an_account_page_that_offers_microsoft_only_links_microsoft_docs_only(self):
        microsoft = {**self.hosted, 'docs_consent': ['microsoft']}
        self.assertTrue(self.offered(microsoft))
        self.assertTrue(a.docs_offered(microsoft, 'microsoft'))
        self.assertFalse(a.docs_offered(microsoft, 'google'))
        self.assertFalse(a.docs_offered({**self.hosted, 'docs_consent': []}))
        self.assertTrue(a.docs_offered({k: v for k, v in microsoft.items() if k != 'manage_url'}, 'google'))  # self-hosted
        # + Add on a hosted Machine opens the account page's Docs tile, where the consent is
        [docs] = [s for s in onboarding.catalog(microsoft) if s['service'] == 'docs']
        self.assertEqual(docs['account_page'], 'docs')

    def test_a_card_waiting_for_the_consent_links_to_where_it_is_given(self):
        with self.store.connect() as db:
            db.execute('INSERT INTO checkpoints(account_id,state,error,failures,last_success) VALUES(?,?,?,?,?)',
                       ('acme-docs', '{}', 'docs_not_connected', 1, '2026-10-26T08:00:00+00:00'))
        app = object.__new__(a.App)
        app.store = self.store
        def card(config):
            app.config = config
            return next(c for c in app.action('status', {'full': True})['connectors'] if c['id'] == 'acme-docs')
        hosted = {**self.hosted, 'accounts': [OUTLOOK, ACCOUNT], 'docs_consent': ['microsoft']}
        self.assertEqual(card(hosted)['account_page'], 'https://cp.example/account#docs')  # its account page's Docs tile
        self.assertEqual(card(hosted)['hosted_signin'], 'microsoft_docs')  # Connect: the sign-in form on the dashboard itself
        self.assertNotIn('account_page', card({**hosted, 'accounts': [GMAIL, ACCOUNT]}))  # Google Docs: not offered there
        own = {k: v for k, v in hosted.items() if k not in ('manage_url', 'docs_consent')}
        self.assertEqual((card(own)['connect_name'], card(own)['signin']), ('docs', 'microsoft_docs'))  # self-hosted: Sign in with Microsoft
        self.assertNotIn('signin', card({**own, 'accounts': [GMAIL, ACCOUNT]}))

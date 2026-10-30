"""Outlook mail and calendar through Microsoft Graph (ms_graph.py): tokens from a broker or the owner's own app, only
known calls, Gmail-shaped reads for the same sync and cards, sends from an exact-MIME draft, and snooze by folder.
No network: urlopen is replaced by a fake broker, a fake sign-in and a fake Graph. Nothing is ever sent."""
import base64
import datetime as dt
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest import mock

import ms_graph
import fleet
import signatures
import types
import next_actions as n
import onboarding
import test_ux as ux

a = ux.a
BROKER = 'https://cloud.example/api/microsoft/token'
G = 'https://graph.microsoft.com/v1.0'
INBOX, SENT, SNOOZED = 'f-inbox', 'f-sent', 'f-snoozed'


class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()


def mime(subject, sender, to, body, message_id):
    return (f'From: {sender}\r\nTo: {to}\r\nSubject: {subject}\r\nMessage-ID: {message_id}\r\n'
            f'Date: Wed, 21 Oct 2026 08:00:00 +0000\r\nContent-Type: text/plain; charset=iso-8859-1\r\n\r\n{body}\r\n').encode('latin-1')


def http_error(url, status, body=None):
    return urllib.error.HTTPError(url, status, 'no', {}, io.BytesIO(json.dumps(body or {}).encode()))


class FakeGraph:
    """A broker granting `granted`, and a mailbox and calendar answering Graph's calls."""

    def __init__(self):
        self.granted = {'User.Read', 'Mail.Read', 'Calendars.Read'}
        self.calls, self.issued, self.fail = [], 0, {}
        self.broker_fail = None  # (status, headers) for every token ask
        self.folders = {'inbox': INBOX, 'sentitems': SENT, 'drafts': 'f-drafts', 'deleteditems': 'f-trash', 'junkemail': 'f-junk'}
        self.snoozed = False
        self.messages = {}
        self.delta = []
        self.sent_html = []
        self.files = {}
        self.calendars = {}

    def add(self, mid, folder, received, modified, body=b'', conversation='conv-1', read=True, internet_id='<x@acme.test>'):
        self.messages[mid] = {'id': mid, 'conversationId': conversation, 'internetMessageId': internet_id, 'parentFolderId': folder,
                              'isRead': read, 'isDraft': False, 'receivedDateTime': received, 'lastModifiedDateTime': modified,
                              'bodyPreview': 'preview', 'webLink': 'https://outlook.office365.com/owa/?ItemID=' + mid,
                              'inferenceClassification': 'focused', '_mime': body}

    def __call__(self, request, timeout=None):
        url, verb = request.full_url, request.get_method()
        self.calls.append((verb, url, request.headers.get('Authorization'), request.data))
        if url == BROKER:
            body = json.loads(request.data)
            if 'scope' not in body:
                return Response(json.dumps({'scopes': sorted(self.granted)}).encode())
            if self.broker_fail:
                raise urllib.error.HTTPError(url, self.broker_fail[0], 'no', self.broker_fail[1], io.BytesIO(b'{}'))
            if body['scope'] not in self.granted and not ms_graph.ANSWERS[body['scope']] & self.granted:
                raise http_error(url, 403)
            self.issued += 1
            return Response(json.dumps({'access_token': f'access-{self.issued}', 'expires_in': 3600}).encode())
        parts = urllib.parse.urlsplit(url)
        path, query = parts.path.removeprefix('/v1.0'), urllib.parse.parse_qs(parts.query)
        for prefix, status in self.fail.items():
            if verb + ' ' + path == prefix:
                raise http_error(url, status)
        assert request.headers.get('Prefer', '').startswith('IdType="ImmutableId"'), 'every call asks for immutable IDs'
        answer = self.answer(verb, path, query, request.data)
        return Response(answer if isinstance(answer, bytes) else json.dumps(answer).encode())

    def answer(self, verb, path, query, data):
        if path == '/me':
            return {'mail': None, 'userPrincipalName': 'Alex@Acme.test'}
        if path.startswith('/me/mailFolders/') and path.count('/') == 3 and verb == 'GET':
            return {'id': self.folders[path.rsplit('/', 1)[1]]}
        if path == '/me/mailFolders' and verb == 'GET':
            return {'value': [{'id': SNOOZED}] if self.snoozed else []}
        if path == '/me/mailFolders' and verb == 'POST':
            self.snoozed = True
            return {'id': SNOOZED}
        if path == '/me/mailFolders/sentitems/messages' and '$filter' not in query:
            return {'value': [{'uniqueBody': {'contentType': 'html', 'content': h}} for h in self.sent_html]}
        if path.endswith('/attachments') and verb == 'GET':
            return {'value': [{k: v for k, v in f.items() if k != 'data'} for f in self.files.values()]}
        if '/attachments/' in path and path.endswith('/$value'):
            return self.files[urllib.parse.unquote(path.split('/')[5])]['data']
        if path.startswith('/me/calendars/') and path.endswith('/calendarView/delta'):
            answer = self.calendars[urllib.parse.unquote(path.split('/')[3])].pop(0)
            if isinstance(answer, int):
                raise http_error(path, answer)
            return answer
        if path.startswith('/me/calendars/') and path.endswith('/calendarView'):
            return {'value': [], 'note': 'whole'}
        if path == '/me/mailFolders/sentitems/messages':
            wanted = query['$filter'][0].split("'")[1]
            return {'value': [{k: v for k, v in m.items() if k != '_mime'} for m in self.messages.values()
                              if m['parentFolderId'] == SENT and m['internetMessageId'] == wanted]}
        if path == '/me/messages' and verb == 'GET':
            rows = [m for m in self.messages.values()]
            text = query.get('$filter', [''])[0]
            if text.startswith('conversationId'):
                rows = [m for m in rows if m['conversationId'] == text.split("'")[1]]
            elif text.startswith('lastModifiedDateTime'):
                rows = sorted((m for m in rows if m['lastModifiedDateTime'] >= text.split()[-1]), key=lambda m: m['lastModifiedDateTime'])
            elif text.startswith('receivedDateTime'):
                rows = [m for m in rows if m['receivedDateTime'] >= text.split()[-1]]
            return {'value': [{k: v for k, v in m.items() if k != '_mime'} for m in rows]}
        if path == '/me/messages' and verb == 'POST':
            raw = base64.b64decode(data)
            mid = f'draft-{len(self.messages)}'
            internet = next(line.split(':', 1)[1].strip() for line in raw.decode().splitlines() if line.lower().startswith('message-id:'))
            self.add(mid, 'f-drafts', '2026-10-21T09:00:00Z', '2026-10-21T09:00:00Z', raw, internet_id=internet)
            self.messages[mid]['isDraft'] = True
            return {'id': mid}
        if path.endswith('/createReply') and verb == 'POST':  # a reply draft in the original's conversation
            original = self.messages.get(urllib.parse.unquote(path.split('/')[3]))
            if not original:
                raise http_error(path, 404)
            mid = f'reply-{len(self.messages)}'
            self.add(mid, 'f-drafts', '2026-10-21T09:00:00Z', '2026-10-21T09:00:00Z', conversation=original['conversationId'],
                     internet_id=f'<{mid}@outlook.test>')
            self.messages[mid].update(isDraft=True, _reply=json.loads(data)['message'], _files=[])
            return {'id': mid, 'conversationId': original['conversationId'], 'internetMessageId': f'<{mid}@outlook.test>'}
        if path.endswith('/attachments') and verb == 'POST':
            self.messages[urllib.parse.unquote(path.split('/')[3])]['_files'].append(json.loads(data))
            return {'id': 'file-1'}
        if verb == 'DELETE' and path.startswith('/me/messages/'):
            del self.messages[urllib.parse.unquote(path.split('/')[3])]
            return b''
        if path.endswith('/send') and verb == 'POST':
            message = self.messages[urllib.parse.unquote(path.split('/')[3])]
            message.update(parentFolderId=SENT, isDraft=False)
            return b''
        if path.endswith('/move'):
            target = json.loads(data)['destinationId']
            self.messages[urllib.parse.unquote(path.split('/')[3])]['parentFolderId'] = self.folders.get(target, target)
            return {}
        if path.endswith('/$value'):
            return self.messages[urllib.parse.unquote(path.split('/')[3])]['_mime']
        if path.startswith('/me/messages/') and verb == 'PATCH':
            self.messages[urllib.parse.unquote(path.split('/')[3])].update(json.loads(data))
            return {}
        if path.startswith('/me/messages/'):
            message = self.messages.get(urllib.parse.unquote(path.split('/')[3]))
            if not message:
                raise http_error(path, 404)
            return {k: v for k, v in message.items() if k != '_mime'}
        if path == '/me/calendar':
            return {'id': 'cal', 'owner': {'address': 'alex@acme.test'}}
        if path == '/me/calendarView/delta':
            return self.delta.pop(0)
        raise AssertionError('unexpected call ' + verb + ' ' + path)


SENT_SIGNED = ('<html><body><div>Reply number {}.</div><div>Cheers,</div><div>Alex</div><div id="Signature"><p><b>Alex Smith</b><br>'
               'Acme | <a href="https://acme.test" onclick="steal()">acme.test</a></p></div></body></html>')


class Base(unittest.TestCase):
    def setUp(self):
        ms_graph._tokens.clear(); ms_graph._folders.clear()
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        token = Path(self.temp.name) / 'broker-token'; token.write_text('machine-token\n')
        self.mail = {'id': 'acme-outlook', 'service': 'outlook', 'transport': 'broker', 'email': 'alex@acme.test', 'boundary': 'work:Acme'}
        self.cal = {'id': 'acme-outlook-calendar', 'service': 'outlook_calendar', 'transport': 'broker', 'email': 'alex@acme.test',
                    'calendar_id': 'primary', 'boundary': 'work:Acme'}
        self.config = {'microsoft_broker': {'url': BROKER}, 'credentials': {'microsoft-broker': str(token)},
                       'accounts': [self.mail, self.cal], 'bootstrap_days': 7, 'database': str(Path(self.temp.name) / 'events.sqlite')}
        self.fake = FakeGraph()
        patcher = mock.patch.object(ms_graph.urllib.request, 'urlopen', self.fake); patcher.start(); self.addCleanup(patcher.stop)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')


class Calls(Base):
    def test_only_known_calls_and_links_of_the_same_call(self):
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('users.list', {})
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('sendMail', {})  # a write is only reachable through the write list
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('messages.list', {'$link': 'https://evil.example/v1.0/me/messages?x'})
        with self.assertRaises(ms_graph.GraphError):
            ms_graph.url_for('messages.list', {'$link': G + '/me/mailFolders/inbox/messages?$skip=5'})
        self.assertEqual(ms_graph.url_for('messages.list', {'$link': G + '/me/messages?$skip=5'})[2], G + '/me/messages?$skip=5')
        self.assertEqual(ms_graph.url_for('messages.mime', {'id': 'a/b'})[2], G + '/me/messages/a%2Fb/$value')

    def test_the_broker_gives_one_token_per_scope_and_identity_is_checked(self):
        profile = a.Gmail(self.config, self.mail).profile()
        self.assertEqual(profile['emailAddress'], 'alex@acme.test')  # personal accounts: the sign-in name when mail is empty
        a.Gmail(self.config, self.mail).profile()
        asks = [json.loads(c[3]) for c in self.fake.calls if c[1] == BROKER]
        self.assertEqual(asks, [{'email': 'alex@acme.test', 'scope': 'User.Read'}])
        self.assertIsNone(onboarding.check(self.config, self.mail))
        self.assertEqual(onboarding.check(self.config, {**self.mail, 'email': 'other@acme.test'}), 'account_identity_mismatch')
        self.fake.granted = {'User.Read'}
        ms_graph._tokens.clear()
        self.assertEqual(onboarding.check(self.config, self.cal), 'microsoft_scope_not_granted:HTTP_403')

    def test_access_and_folder_caches_do_not_cross_independent_connections(self):
        other = {**self.config, 'microsoft_broker': {'url': 'https://other.example/token'}}
        with mock.patch.object(ms_graph, '_broker', side_effect=lambda config, *args: {'access_token': config['microsoft_broker']['url'], 'expires_in': 3600}):
            first = ms_graph.token(self.config, a.credential, self.mail, 'Mail.Read')
            second = ms_graph.token(other, a.credential, self.mail, 'Mail.Read')
        self.assertNotEqual(first, second)
        with mock.patch.object(ms_graph, 'call', side_effect=lambda config, *args: {'id': config['microsoft_broker']['url']}):
            self.assertNotEqual(ms_graph.folders(self.config, a.credential, self.mail), ms_graph.folders(other, a.credential, self.mail))

    def test_reconnecting_invalidates_the_cached_access(self):
        with mock.patch.object(ms_graph, '_broker', side_effect=[{'access_token': 'first', 'expires_in': 3600}, {'access_token': 'second', 'expires_in': 3600}]):
            first = ms_graph.token(self.config, a.credential, self.mail, 'Mail.Read')
            second = ms_graph.token(self.config, a.credential, {**self.mail, 'connected_at': '2026-10-21T09:00:00Z'}, 'Mail.Read')
        self.assertNotEqual(first, second)

    def test_graph_throttle_preserves_the_requested_wait(self):
        with mock.patch.object(ms_graph.urllib.request, 'urlopen', side_effect=urllib.error.HTTPError(G, 429, 'busy', {'Retry-After': '420'}, io.BytesIO())):
            with mock.patch.object(ms_graph, 'token', return_value='test'):
                with self.assertRaises(ms_graph.GraphError) as got:
                    ms_graph.call(self.config, a.credential, self.mail, 'me')
        self.assertEqual(got.exception.retry_after, 420)

    def test_oversized_raw_response_never_becomes_a_successful_partial_file(self):
        with mock.patch.object(ms_graph, 'token', return_value='test'), mock.patch.object(ms_graph.urllib.request, 'urlopen', return_value=Response(b'x' * 40_000_001)):
            with self.assertRaises(ms_graph.GraphError):
                ms_graph.call(self.config, a.credential, self.mail, 'messages.mime', {'id': 'm1'}, raw=True)

    def test_attachment_listing_follows_every_page_and_keeps_call_scope(self):
        link = G + '/me/messages/m1/attachments?$skip=1'
        pages = [{'value': [{'id': 'one', 'name': 'one.pdf'}], '@odata.nextLink': link}, {'value': [{'id': 'two', 'name': 'two.pdf'}]}]
        with mock.patch.object(ms_graph, 'call', side_effect=pages) as called:
            found = ms_graph.attachments(self.config, a.credential, self.mail, 'm1')
        self.assertEqual([f['id'] for f in found], ['one', 'two'])
        self.assertEqual(called.call_args_list[1].args[4], {'id': 'm1', '$link': link})

    def test_a_refused_sign_in_right_after_connecting_retries_with_backoff(self):
        def ago(seconds):
            return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=seconds)).isoformat()

        def refused(account):
            ms_graph._tokens.clear()
            with self.assertRaises(ms_graph.GraphError) as caught:
                ms_graph.token(self.config, a.credential, account, 'User.Read')
            return caught.exception.category, caught.exception.retry_after

        self.fake.broker_fail = (401, {})
        # Microsoft may still be taking the new permissions: retried, each wait as long as the account's age
        self.assertEqual(refused({**self.mail, 'connected_at': ago(2)}), ('outlook:microsoft_signin_pending', 30))
        self.assertEqual(refused({**self.mail, 'connected_at': ago(300)})[1], 300)
        error = onboarding.check(self.config, {**self.mail, 'connected_at': ago(2)})
        self.assertTrue(error.startswith(onboarding.BUSY))  # saved anyway; the sync retries it
        # long after connecting, or not knowing when: expired, connect again
        self.assertEqual(refused({**self.mail, 'connected_at': ago(3600)}), ('outlook:microsoft_signin_expired', 3600))
        self.assertEqual(refused(self.mail), ('outlook:microsoft_signin_expired', 3600))
        # the broker itself asks to wait (a grant Microsoft is still settling)
        self.fake.broker_fail = (503, {'Retry-After': '30'})
        self.assertEqual(refused(self.mail), ('microsoft_broker_busy', 30))
        self.assertTrue(onboarding.check(self.config, self.mail).startswith(onboarding.BUSY))

    def test_connecting_again_ends_the_wait(self):
        app = object.__new__(a.App)
        app.config, app.store, app.stop = self.config, self.store, threading.Event()
        self.store.failed(self.mail['id'], a.SourceError('outlook:microsoft_signin_expired', 401, retry_after=3600))
        with self.store.connect() as db:
            row = db.execute('SELECT retry_at,error,error_at FROM checkpoints WHERE account_id=?', (self.mail['id'],)).fetchone()
        waits = []

        def wait(seconds):
            waits.append(seconds)
            self.mail['connected_at'] = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=1)).isoformat()
            return False
        app.stop.wait = wait
        self.assertFalse(app.wait_for_retry(self.mail, row))
        self.assertEqual(waits, [15])
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT retry_at FROM checkpoints WHERE account_id=?', (self.mail['id'],)).fetchone()[0])


class MailSync(Base):
    def test_bootstrap_and_changes_flow_through_the_gmail_sync(self):
        self.fake.add('m1', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z', mime('Quote', 'Bo <bo@client.test>', 'alex@acme.test', 'Caf\xe9 at 10?', '<m1@client.test>'), read=False)
        self.fake.add('m2', SENT, '2099-01-01T09:00:00Z', '2099-01-01T09:00:00Z', mime('Re: Quote', 'alex@acme.test', 'bo@client.test', 'Yes', '<m2@acme.test>'))
        a.sync_gmail(self.store, self.config, self.mail)   # bootstrap page
        a.sync_gmail(self.store, self.config, self.mail)   # incremental from here
        with self.store.connect() as db:
            rows = {r['source_id']: r for r in db.execute('SELECT * FROM events')}
        first = json.loads(rows['m1']['metadata'])
        self.assertEqual(rows['m1']['kind'], 'gmail.message')
        self.assertIn('Café at 10?', rows['m1']['body'])  # any charset arrives as text
        self.assertEqual((first['from'], first['message-id'], first['thread_id']), ('Bo <bo@client.test>', '<m1@client.test>', 'conv-1'))
        self.assertEqual(first['labels'], ['INBOX', 'UNREAD'])
        self.assertEqual(first['source_url'], 'https://outlook.office365.com/owa/?ItemID=m1')
        self.assertEqual(json.loads(rows['m2']['metadata'])['labels'], ['SENT'])
        state = self.store.checkpoint('acme-outlook')
        self.assertEqual(state['mode'], 'incremental')
        # Moved to Deleted Items: the same as Gmail's trash label
        self.fake.messages['m1'].update(parentFolderId='f-trash', lastModifiedDateTime='2099-01-02T08:00:00Z')
        a.sync_gmail(self.store, self.config, self.mail)
        with self.store.connect() as db:
            labels = json.loads(db.execute("SELECT metadata FROM events WHERE source_id='m1'").fetchone()[0])['labels']
        self.assertIn('TRASH', labels)
        self.assertEqual(self.store.checkpoint('acme-outlook')['history_id'], '2099-01-02T08:00:00Z')

    def test_a_card_reads_attachments_from_the_message_itself(self):
        body = (b'From: bo@client.test\r\nTo: alex@acme.test\r\nSubject: Invoice\r\nMIME-Version: 1.0\r\n'
                b'Content-Type: multipart/mixed; boundary=XX\r\n\r\n--XX\r\nContent-Type: text/plain\r\n\r\nSee attached\r\n'
                b'--XX\r\nContent-Type: application/pdf\r\nContent-Disposition: attachment; filename="inv.pdf"\r\n'
                b'Content-Transfer-Encoding: base64\r\n\r\nJVBERi0x\r\n--XX--\r\n')
        self.fake.add('m3', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z', body)
        message = a.gog_read(self.config, self.mail, 'gmail', 'v1', 'gmail.users.messages.get', {'userId': 'me', 'id': 'm3', 'format': 'full'}, 'x')
        found = a.message_attachments(message['payload'])
        self.assertEqual([f['name'] for f in found], ['inv.pdf'])
        pdf = message['payload']['parts'][1]['body']['data']
        self.assertEqual(base64.urlsafe_b64decode(pdf + '=' * (-len(pdf) % 4)), b'%PDF-1')


class CalendarSync(Base):
    def test_delta_window_then_changes_and_removals(self):
        self.fake.delta = [
            {'value': [{'id': 'e1', 'subject': 'Demo with Bo', 'start': {'dateTime': '2099-01-03T09:00:00.0000000', 'timeZone': 'UTC'},
                        'end': {'dateTime': '2099-01-03T10:00:00.0000000', 'timeZone': 'UTC'}, 'isAllDay': False,
                        'organizer': {'emailAddress': {'address': 'alex@acme.test', 'name': 'Alex'}},
                        'attendees': [{'emailAddress': {'address': 'Bo@client.test', 'name': 'Bo'}, 'status': {'response': 'accepted'}},
                                      {'type': 'resource', 'emailAddress': {'address': 'room4@acme.test', 'name': 'Room 4'}, 'status': {'response': 'accepted'}}],
                        'webLink': 'https://outlook.office365.com/owa/?itemid=e1', 'lastModifiedDateTime': '2099-01-01T00:00:00Z'}],
             '@odata.deltaLink': G + '/me/calendarView/delta?$deltatoken=one'},
            {'value': [{'id': 'e1', '@removed': {'reason': 'deleted'}}], '@odata.deltaLink': G + '/me/calendarView/delta?$deltatoken=two'}]
        with mock.patch.object(a, 'now', return_value='2099-01-01T00:00:00+00:00'):
            a.sync_calendar(self.store, self.config, self.cal)
            with self.store.connect() as db:
                row = db.execute("SELECT * FROM events WHERE source_id='e1'").fetchone()
            meta = json.loads(row['metadata'])
            self.assertEqual((row['kind'], row['occurred_at'], meta['end_at']), ('calendar.event', '2099-01-03T09:00:00+00:00', '2099-01-03T10:00:00+00:00'))
            self.assertEqual(meta['attendees'][0], {'email': 'bo@client.test', 'displayName': 'Bo', 'responseStatus': 'accepted'})
            self.assertTrue(meta['attendees'][1]['resource'])  # a booked room: never a person on the Graph or in Calendar
            self.assertEqual(meta['source_url'], 'https://outlook.office365.com/owa/?itemid=e1')
            self.assertEqual(self.store.checkpoint(self.cal['id'])['sync_token'], G + '/me/calendarView/delta?$deltatoken=one')
            a.sync_calendar(self.store, self.config, self.cal)
            with self.store.connect() as db:
                self.assertEqual(db.execute("SELECT deleted FROM events WHERE source_id='e1'").fetchone()[0], 1)
        delta = [c for c in self.fake.calls if '/calendarView/delta' in c[1]]
        self.assertIn('startDateTime=', delta[0][1])
        self.assertEqual(delta[1][1], G + '/me/calendarView/delta?$deltatoken=one')


class Sending(Base):
    def action(self, **extra):
        value = {'kind': 'email', 'label': 'Send reply', 'account_id': 'acme-outlook', 'to': ['bo@client.test'], 'subject': 'Re: Quote',
                 'body': 'Yes, 10 works.\n\nAlex', 'thread_id': 'AAQkADAwATM0MDAAMS1iZDZi+LTI5=', 'in_reply_to': '<m1@client.test>', **extra}
        return n.validate(value, self.config, ['acme-outlook'])

    def test_an_outlook_reply_validates_without_a_signature_and_goes_out_from_a_draft(self):
        action = self.action()
        self.assertEqual((action['from'], action['signature'], action['snooze_days']), ('alex@acme.test', True, 3))
        self.fake.sent_html = [SENT_SIGNED.format(n) for n in range(4)]
        email = n.EmailTransport(self.config, a.credential, a.gog_read)
        with self.assertRaisesRegex(ValueError, 'Outlook is connected read-only'):
            email.preflight(action)
        self.fake.granted |= {'Mail.ReadWrite', 'Mail.Send'}
        email.preflight(action)
        job = {'rfc_message_id': '<job-1@acme.test>'}
        result = email.send(action, job)
        draft = self.fake.messages[result['message_id']]
        self.assertEqual(draft['parentFolderId'], SENT)
        sent = base64.b64decode(next(c[3] for c in self.fake.calls if c[0] == 'POST' and c[1] == G + '/me/messages')).decode()
        self.assertIn('In-Reply-To: <m1@client.test>', sent)
        self.assertIn('Message-ID: <job-1@acme.test>', sent)
        self.assertIn('Alex Smith', sent)  # the signature found in the sent mail, below the body
        self.assertEqual(signatures.get(self.config, 'acme-outlook')['source'], 'detected')
        self.assertEqual(email.reconcile(action, job), {'message_id': result['message_id']})
        self.fake.fail['POST /me/messages'] = 400
        self.assertEqual(email.send(action, job), {'rejected': 400})
        self.fake.fail = {'POST /me/messages/draft-0/send': 500}  # the next draft after clearing
        self.fake.messages.clear()
        self.assertEqual(email.send(action, {'rfc_message_id': '<job-2@acme.test>'}), {})  # unknown: never sent twice
        self.fake.fail = {'POST /me/messages': 503}
        self.assertEqual(email.send(action, job), {'not_sent': True})  # no draft, so nothing went out: tried again later

    def test_a_gmail_style_thread_id_rule_still_holds_for_gmail(self):
        self.config['accounts'].append({'id': 'acme-gmail', 'service': 'gmail', 'transport': 'broker', 'email': 'alex@acme.test', 'boundary': 'work:Acme'})
        with self.assertRaisesRegex(ValueError, 'thread header'):
            n.validate({'kind': 'email', 'account_id': 'acme-gmail', 'to': ['bo@client.test'], 'subject': 'Re', 'body': 'x',
                        'thread_id': 'AAQk+=', 'in_reply_to': '<m1@client.test>'}, self.config, ['acme-gmail'])


class ReplyInItsConversation(Base):
    """A reply goes into the conversation of the email it answers: createReply on that email when it is in this
    mailbox, the MIME draft with In-Reply-To and References when it isn't (Jeroen, 2026-10-30)."""

    def setUp(self):
        super().setUp()
        self.fake.granted |= {'Mail.ReadWrite', 'Mail.Send'}
        self.fake.sent_html = [SENT_SIGNED.format(i) for i in range(3)]
        self.fake.add('in1', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z', conversation='conv-9', internet_id='<m1@client.test>')

    def email(self, account_id='acme-outlook'):
        return {'metadata': json.dumps({'from': 'Bo <bo@client.test>', 'to': 'alex@acme.test', 'message-id': '<m1@client.test>',
                                        'thread_id': 'conv-9' if account_id == 'acme-outlook' else 'beef01', 'labels': ['INBOX']}),
                'account_id': account_id, 'source_id': 'in1' if account_id == 'acme-outlook' else 'g1', 'title': 'Quote'}

    def reply(self, rows, allowed=('acme-outlook',)):
        replied = a.replied_to(rows)
        value = {'kind': 'email', 'label': 'Send reply', 'account_id': 'acme-outlook', 'to': ['bo@client.test'],
                 'subject': 'Re: Quote', 'body': 'Yes, 10 works.\n\nAlex'}
        return n.validate(n.fill_reply(value, replied), self.config, list(allowed), replied=replied)

    def posted(self, path):
        return [c for c in self.fake.calls if c[0] == 'POST' and c[1] == G + path]

    def test_a_reply_in_the_same_mailbox_goes_out_with_create_reply(self):
        action = self.reply([self.email()])
        self.assertEqual((action['in_reply_to'], action['thread_id'], action['reply_to_id']), ('<m1@client.test>', 'conv-9', 'in1'))
        email = n.EmailTransport(self.config, a.credential, a.gog_read)
        email.preflight(action)
        result = email.send(action, {'rfc_message_id': '<job-1@acme.test>'})
        self.assertEqual(result['rfc_message_id'], f"<{result['message_id']}@outlook.test>")  # Outlook's own, kept on the job
        sent = self.fake.messages[result['message_id']]
        self.assertEqual((sent['parentFolderId'], sent['conversationId']), (SENT, 'conv-9'))
        self.assertEqual((sent['_reply']['subject'], sent['_reply']['toRecipients']), ('Re: Quote', [{'emailAddress': {'address': 'bo@client.test'}}]))
        self.assertIn('Yes, 10 works.', sent['_reply']['body']['content'])
        self.assertIn('Alex Smith', sent['_reply']['body']['content'])  # the signature found in the sent mail
        self.assertEqual(self.posted('/me/messages'), [])  # never a new message

    def test_files_go_on_the_reply_draft_and_a_failed_one_leaves_no_draft(self):
        root = Path(self.temp.name)
        (root / 'files').mkdir()
        (root / 'files' / 'receipt.pdf').write_bytes(b'%PDF receipt')
        self.config.update(attachment_sources=[str(root / 'files')], attachment_dir=str(root / 'store'))
        action = self.reply([self.email()])
        action = {**action, 'attachments': n.store_attachments([str(root / 'files' / 'receipt.pdf')], self.config)}
        email = n.EmailTransport(self.config, a.credential, a.gog_read)
        result = email.send(action, {'rfc_message_id': '<job-4@acme.test>'})
        files = self.fake.messages[result['message_id']]['_files']
        self.assertEqual((files[0]['name'], base64.b64decode(files[0]['contentBytes'])), ('receipt.pdf', b'%PDF receipt'))
        self.fake.fail = {f'POST /me/messages/reply-{len(self.fake.messages)}/attachments': 503}
        self.assertEqual(email.send(action, {'rfc_message_id': '<job-5@acme.test>'}), {'not_sent': True})
        self.assertFalse([m for m in self.fake.messages.values() if m['isDraft']])  # the half-filled draft is gone

    def test_an_original_gone_from_the_mailbox_still_threads_by_its_headers(self):
        action = self.reply([self.email()])
        del self.fake.messages['in1']
        result = n.EmailTransport(self.config, a.credential, a.gog_read).send(action, {'rfc_message_id': '<job-2@acme.test>'})
        self.assertTrue(result['message_id'].startswith('draft-'))
        sent = base64.b64decode(self.posted('/me/messages')[0][3]).decode()
        self.assertIn('In-Reply-To: <m1@client.test>', sent)
        self.assertIn('References: <m1@client.test>', sent)

    def test_a_reply_to_mail_that_came_in_elsewhere_keeps_its_headers_and_says_so(self):
        gmail = {'id': 'acme-gmail', 'service': 'gmail', 'transport': 'broker', 'email': 'alex@acme.example', 'boundary': 'work:Acme'}
        self.config['accounts'].append(gmail)
        action = self.reply([self.email('acme-gmail')], ('acme-gmail', 'acme-outlook'))
        self.assertEqual((action['in_reply_to'], action['reply_elsewhere']), ('<m1@client.test>', 'alex@acme.example'))
        self.assertNotIn('thread_id', action)
        self.assertNotIn('reply_to_id', action)
        result = n.EmailTransport(self.config, a.credential, a.gog_read).send(action, {'rfc_message_id': '<job-3@acme.test>'})
        self.assertTrue(result['message_id'].startswith('draft-'))
        self.assertEqual([c for c in self.fake.calls if c[1].endswith('/createReply')], [])
        self.assertIn('In-Reply-To: <m1@client.test>', base64.b64decode(self.posted('/me/messages')[0][3]).decode())


class Snooze(Base):
    def test_snooze_moves_the_inbox_messages_and_wake_brings_them_back_unread(self):
        snooze = n.ThreadSnooze(self.config, a.credential, a.gog_read)
        self.fake.add('in1', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z')
        self.fake.add('out1', SENT, '2099-01-01T09:00:00Z', '2099-01-01T09:00:00Z')
        self.assertEqual(snooze.snooze('acme-outlook', 'conv-1', 'out1'), 'no_permission')
        self.fake.granted |= {'Mail.ReadWrite', 'Mail.Send'}
        with self.assertRaises(RuntimeError):
            snooze.snooze('acme-outlook', 'conv-1', 'unknown')  # the send isn't confirmed yet: retried
        self.assertEqual(snooze.snooze('acme-outlook', 'conv-1', 'out1'), 'snoozed')
        self.assertEqual(self.fake.messages['in1']['parentFolderId'], SNOOZED)
        self.assertEqual(self.fake.messages['out1']['parentFolderId'], SENT)
        self.assertEqual(snooze.wake('acme-outlook', 'conv-1'), 'returned')
        self.assertEqual((self.fake.messages['in1']['parentFolderId'], self.fake.messages['in1']['isRead']), (INBOX, False))
        self.assertEqual(snooze.wake('acme-outlook', 'conv-1'), 'returned')  # already back: left alone

    def test_a_reply_already_in_never_gets_hidden_and_keeps_its_read_state(self):
        snooze = n.ThreadSnooze(self.config, a.credential, a.gog_read)
        self.fake.granted |= {'Mail.ReadWrite', 'Mail.Send'}
        self.fake.add('in1', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z')
        self.fake.add('out1', SENT, '2099-01-01T09:00:00Z', '2099-01-01T09:00:00Z')
        self.fake.add('reply', INBOX, '2099-01-01T10:00:00Z', '2099-01-01T10:00:00Z')
        self.assertEqual(snooze.snooze('acme-outlook', 'conv-1', 'out1'), 'returned')
        self.assertFalse(self.fake.snoozed)
        del self.fake.messages['reply']
        snooze.snooze('acme-outlook', 'conv-1', 'out1')
        self.fake.add('reply', INBOX, '2099-01-02T10:00:00Z', '2099-01-02T10:00:00Z')
        snooze.wake('acme-outlook', 'conv-1')
        self.assertEqual((self.fake.messages['in1']['parentFolderId'], self.fake.messages['in1']['isRead']), (INBOX, True))


class Signatures(Base):
    def test_cleaning_keeps_formatting_and_drops_anything_active(self):
        cleaned = signatures.clean('<script>alert(1)</script><b onclick="x()">Alex</b><a href="javascript:x()">a</a>'
                                   '<img src="http://plain.test/t.png"><img src="cid:logo"><div style="background:url(x)">t</div><iframe>in</iframe>')
        self.assertEqual(cleaned, '<b>Alex</b><a>a</a><img><img src="cid:logo"><div>t</div>')

    def test_dropped_void_elements_do_not_swallow_the_signature(self):
        for tag in ('meta', 'link', 'base', 'input', 'embed'):
            self.assertEqual(signatures.clean(f'<{tag}><b>Alex</b>'), '<b>Alex</b>')
        self.assertEqual(signatures.clean('<head><meta></head><body>Alex</body>'), 'Alex')
        self.assertEqual(signatures.clean('<script/><b>Alex</b>'), '<b>Alex</b>')

    def test_found_only_when_it_repeats_and_without_the_closing(self):
        plain = [f'<div>Note {n}.</div><div>Cheers,</div><div>Alex</div><div><b>Alex Smith</b></div><div>Acme</div>'
                 '<div id="appendonsend"></div><div>quoted <b>Someone Else</b></div>' for n in range(3)]
        self.assertEqual(signatures.detect(plain, 'Alex'), '<div><b>Alex Smith</b></div><div>Acme</div>')
        self.assertEqual(signatures.detect(plain[:2], 'Alex'), '')  # twice is not enough
        self.assertIn('Alex Smith', signatures.detect([SENT_SIGNED.format(n) for n in range(3)], 'Alex'))
        self.assertNotIn('steal', signatures.detect([SENT_SIGNED.format(n) for n in range(3)], 'Alex'))

    def test_the_owners_own_is_never_replaced_and_overrides_gmail(self):
        signatures.save(self.config, 'acme-outlook', '<b>Mine</b>', 'owner')
        self.assertEqual(signatures.save(self.config, 'acme-outlook', '<b>Found</b>', 'detected')['html'], '<b>Mine</b>')
        gmail = {'id': 'acme-gmail', 'service': 'gmail', 'transport': 'broker', 'email': 'alex@acme.test', 'boundary': 'work:Acme'}
        self.config['accounts'].append(gmail)
        reads = []
        email = n.EmailTransport(self.config, a.credential, lambda *args: reads.append(args) or {'signature': '<i>Gmail</i>'})
        action = {'kind': 'email', 'account_id': 'acme-gmail', 'from': 'alex@acme.test', 'signature': True}
        self.assertEqual(email.signature(action, gmail), '<i>Gmail</i>')  # empty: Gmail's own
        signatures.save(self.config, 'acme-gmail', '<b>Override</b>', 'owner')
        email.signatures.clear()
        self.assertEqual(email.signature(action, gmail), '<b>Override</b>')
        self.assertEqual(len(reads), 1)
        self.assertEqual(email.signature({**action, 'signature': False}, gmail), '')

    def settings_app(self, read):
        app = types.SimpleNamespace(config=self.config, mail_read=read)
        for name in ('mailbox_signature', 'signature_view', 'signature_action'):
            setattr(app, name, getattr(a.App, name).__get__(app))
        return app

    def test_settings_imports_each_mailboxs_own_cleaned_and_keeps_the_owners(self):
        gmail = {'id': 'acme-gmail', 'service': 'gmail', 'transport': 'broker', 'email': 'alex@acme.test', 'boundary': 'work:Acme'}
        self.config['accounts'].append(gmail)
        reads = []
        app = self.settings_app(lambda *args: reads.append(args) or {'signature': '<b onclick="x()">Alex</b><script>steal()</script><img src="http://plain.test/t.png">'})
        found = app.signature_action('detect_signature', {'account_id': 'acme-gmail'})
        self.assertEqual((found['html'], found['found'], found['source']), ('<b>Alex</b><img>', True, 'imported'))
        self.assertEqual(reads[0][4:], ('gmail.users.settings.sendAs.get', {'userId': 'me', 'sendAsEmail': 'alex@acme.test'},
                                        'https://www.googleapis.com/auth/gmail.readonly'))  # the read-only scope it already has
        self.assertEqual(signatures.get(self.config, 'acme-gmail')['source'], 'imported')
        # Outlook: from the sent mail, through Graph (no send).
        self.fake.sent_html = [SENT_SIGNED.format(n) for n in range(3)]
        found = app.signature_action('detect_signature', {'account_id': 'acme-outlook'})
        self.assertIn('Alex Smith', found['html']); self.assertNotIn('steal', found['html'])
        self.assertEqual(signatures.get(self.config, 'acme-outlook')['source'], 'detected')
        self.assertFalse([c for c in self.fake.calls if c[0] == 'POST' and c[1].startswith(G)])  # read only: nothing sent
        # The owner's own stays through an import, is cleaned when saved, and "Use mailbox signature" brings Gmail's back.
        app.signature_action('set_signature', {'account_id': 'acme-gmail', 'html': '<i>Mine</i><script>x()</script>'})
        self.assertEqual(signatures.get(self.config, 'acme-gmail'), {**signatures.get(self.config, 'acme-gmail'), 'html': '<i>Mine</i>', 'source': 'owner'})
        app.signature_action('detect_signature', {'account_id': 'acme-gmail'})
        self.assertEqual(signatures.get(self.config, 'acme-gmail')['html'], '<i>Mine</i>')
        view = app.signature_action('set_signature', {'account_id': 'acme-gmail', 'use_mailbox': True})
        self.assertEqual(next(v for v in view if v['account_id'] == 'acme-gmail')['source'], 'imported')
        self.assertEqual(signatures.get(self.config, 'acme-gmail')['html'], '<b>Alex</b><img>')
        # A mailbox that can't be read now says so; nothing is kept.
        signatures.remove(self.config, 'acme-gmail')
        app.mail_read = lambda *args: (_ for _ in ()).throw(a.SourceError('network'))
        with self.assertRaisesRegex(ValueError, 'Gmail could not be read now'):
            app.signature_action('detect_signature', {'account_id': 'acme-gmail'})
        self.assertIsNone(signatures.get(self.config, 'acme-gmail'))


class Attachments(Base):
    def test_a_preparation_lists_and_saves_outlook_attachments(self):
        self.fake.add('m4', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z', mime('Invoice', 'bo@client.test', 'alex@acme.test', 'Attached', '<m4@client.test>'))
        self.fake.files = {'a1': {'@odata.type': '#microsoft.graph.fileAttachment', 'id': 'a1', 'name': '../inv.pdf', 'contentType': 'application/pdf',
                                  'size': 6, 'isInline': False, 'data': b'%PDF-1'},
                           'a2': {'@odata.type': '#microsoft.graph.referenceAttachment', 'id': 'a2', 'name': 'Deck', 'size': 0},
                           'a3': {'@odata.type': '#microsoft.graph.itemAttachment', 'id': 'a3', 'name': 'Fwd: older mail', 'size': 900}}
        a.sync_gmail(self.store, self.config, self.mail)
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m4'").fetchone()[0]
        app = types.SimpleNamespace(config=self.config, store=self.store)
        listed = a.App.mail_attachment(app, {'event_id': event})['attachments']
        self.assertEqual([(x['name'], x['kind']) for x in listed], [('../inv.pdf', 'file'), ('Deck', 'link'), ('Fwd: older mail', 'item')])
        self.assertIn('browser', listed[1]['note'])
        folder = Path(self.temp.name) / 'attachments'
        saved = a.App.mail_attachment(app, {'event_id': event, 'save': 'a1', 'job_id': 'job-1', '_folder': str(folder)})
        self.assertEqual(Path(saved['saved']), folder / 'job-1' / '_inv.pdf')  # no way out of the folder
        self.assertEqual(Path(saved['saved']).read_bytes(), b'%PDF-1')
        with self.assertRaisesRegex(ValueError, 'Only file attachments'):
            a.App.mail_attachment(app, {'event_id': event, 'save': 'a2', 'job_id': 'job-1', '_folder': str(folder)})
        with self.assertRaisesRegex(ValueError, 'job_id'):
            a.App.mail_attachment(app, {'event_id': event, 'save': 'a1', 'job_id': '../x', '_folder': str(folder)})
        self.fake.files['a1']['size'] = n.MAX_ATTACHMENT_BYTES + 1
        with self.assertRaisesRegex(ValueError, '18 MB'):
            a.App.mail_attachment(app, {'event_id': event, 'save': 'a1', 'job_id': 'job-1', '_folder': str(folder)})
        with self.assertRaisesRegex(ValueError, 'Gmail or Outlook mailbox'):
            a.App.mail_attachment(app, {'account_id': 'acme-outlook-calendar', 'message_id': 'm4'})


class BriefLinks(Base):
    def test_outlook_mail_opens_in_outlook_on_the_web(self):
        self.assertEqual(ms_graph.open_link(self.mail, 'AA/k='), 'https://outlook.office.com/mail/deeplink/read/AA%2Fk%3D')
        self.assertEqual(ms_graph.open_link({'email': 'sam@hotmail.co.uk'}, 'AA'), 'https://outlook.live.com/mail/0/deeplink/read/AA')
        self.assertEqual(ms_graph.open_link(self.mail, 'AA', 'https://outlook.office365.com/owa/?ItemID=AA'), 'https://outlook.office365.com/owa/?ItemID=AA')
        self.assertFalse(ms_graph.personal({'email': 'sam@live.nation.test'}))
        self.fake.add('m1', INBOX, '2099-01-01T08:00:00Z', '2099-01-01T08:00:00Z', mime('Quote', 'Bo <bo@client.test>', 'alex@acme.test', 'Hi', '<m1@client.test>'))
        a.sync_gmail(self.store, self.config, self.mail)
        opener = fleet.Fleet.brief_opener(types.SimpleNamespace(config=self.config, connect=self.store.connect))
        self.assertEqual(opener('client.test'), 'https://outlook.office365.com/owa/?ItemID=m1')
        self.assertTrue(opener('other.test').startswith('https://mail.google.com/'))
        view = {'unanswered': [{'org': 'Client', 'domain': 'client.test', 'count': 1, 'since': '2099-01-01', 'who': ['You'], 'shared': ['sales']}]}
        items = fleet.brief_items(view, fleet.dt.date(2099, 1, 5), (), opener)
        self.assertEqual(items[0]['open'], 'https://outlook.office365.com/owa/?ItemID=m1')
        self.assertTrue(fleet.brief_items(view, fleet.dt.date(2099, 1, 5))[0]['open'].startswith('https://mail.google.com/'))


class OtherCalendars(Base):
    def test_a_shared_calendar_has_its_own_delta_or_is_read_whole(self):
        shared = {**self.cal, 'id': 'acme-team-calendar', 'calendar_id': 'team'}
        self.fake.calendars = {'team': [{'value': [], '@odata.deltaLink': G + '/me/calendars/team/calendarView/delta?$deltatoken=t1'},
                                        {'value': [], '@odata.deltaLink': G + '/me/calendars/team/calendarView/delta?$deltatoken=t2'}],
                               'other': [404]}
        first = ms_graph.calendar_call(self.config, a.credential, shared, 'events.list', {'timeMin': '2099-01-01T00:00:00Z', 'timeMax': '2099-02-01T00:00:00Z'})
        self.assertEqual(first['nextSyncToken'], G + '/me/calendars/team/calendarView/delta?$deltatoken=t1')
        again = ms_graph.calendar_call(self.config, a.credential, shared, 'events.list', {'syncToken': first['nextSyncToken']})
        self.assertEqual(again['nextSyncToken'], G + '/me/calendars/team/calendarView/delta?$deltatoken=t2')
        with self.assertRaises(ms_graph.GraphError):  # another calendar's link is never followed
            ms_graph.calendar_call(self.config, a.credential, {**shared, 'calendar_id': 'other'}, 'events.list', {'syncToken': first['nextSyncToken']})
        whole = ms_graph.calendar_call(self.config, a.credential, {**shared, 'calendar_id': 'other'}, 'events.list',
                                       {'timeMin': '2099-01-01T00:00:00Z', 'timeMax': '2099-02-01T00:00:00Z'})
        self.assertEqual(whole['nextSyncToken'], 'none')  # no delta for this one: read whole each round
        with self.assertRaises(ms_graph.GraphError) as caught:
            ms_graph.calendar_call(self.config, a.credential, shared, 'events.list', {'syncToken': 'none'})
        self.assertEqual(caught.exception.status, 410)


class OwnApp(unittest.TestCase):
    """Self-hosted: the owner's own app registration, a device-code sign-in, and a rotating refresh token."""

    def setUp(self):
        ms_graph._tokens.clear(); ms_graph._folders.clear()
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'microsoft-alex-acme-test'
        self.account = {'id': 'acme-outlook', 'service': 'outlook', 'transport': 'graph', 'email': 'alex@acme.test',
                        'credential': 'microsoft-alex-acme-test', 'boundary': 'work:Acme'}
        self.config = {'microsoft_graph': {'client_id': '11111111-2222-3333-4444-555555555555', 'tenant': 'common'},
                       'credentials': {'microsoft-alex-acme-test': str(self.path)}, 'accounts': [self.account]}
        self.posts = []

    def login(self, answers):
        def urlopen(request, timeout=None):
            if request.full_url.startswith(ms_graph.LOGIN):
                form = dict(urllib.parse.parse_qsl(request.data.decode()))
                self.posts.append((request.full_url, form))
                status, body = answers.pop(0)
                if status != 200:
                    raise http_error(request.full_url, status, body)
                return Response(json.dumps(body).encode())
            return Response(json.dumps({'mail': 'alex@acme.test'}).encode())
        return mock.patch.object(ms_graph.urllib.request, 'urlopen', urlopen)

    def test_device_code_sign_in_then_rotating_refresh_tokens(self):
        said = []
        with self.login([(200, {'device_code': 'dc', 'user_code': 'ABCD', 'verification_uri': 'https://microsoft.com/devicelogin', 'interval': 1, 'expires_in': 60}),
                         (400, {'error': 'authorization_pending'}),
                         (200, {'access_token': 'a1', 'refresh_token': 'r1', 'scope': 'https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read offline_access'})]):
            refresh, granted, who = ms_graph.device_signin(self.config['microsoft_graph'], ['User.Read', 'Mail.Read'], said.append, poll=lambda s: None)
        self.assertEqual((refresh, granted, who), ('r1', {'Mail.Read', 'User.Read'}, 'alex@acme.test'))
        self.assertIn('ABCD', said[0])
        self.assertEqual(self.posts[0][1]['scope'], 'offline_access https://graph.microsoft.com/User.Read https://graph.microsoft.com/Mail.Read')
        ms_graph.save_signin(self.path, refresh, granted)
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        with self.login([(200, {'access_token': 'a2', 'refresh_token': 'r2', 'expires_in': 3600, 'scope': 'https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/User.Read'})]):
            self.assertEqual(ms_graph.token(self.config, a.credential, self.account, 'Mail.Read'), 'a2')
        self.assertEqual(self.posts[-1][1]['refresh_token'], 'r1')
        self.assertEqual(json.loads(self.path.read_text())['refresh_token'], 'r2')  # rotated, saved
        with self.assertRaises(ms_graph.GraphError) as caught:
            ms_graph.token(self.config, a.credential, self.account, 'Mail.Send')
        self.assertEqual(caught.exception.category, 'microsoft_scope_not_granted')
        ms_graph._tokens.clear()
        with self.login([(400, {'error': 'invalid_grant'})]):
            with self.assertRaises(ms_graph.GraphError) as caught:
                ms_graph.token(self.config, a.credential, self.account, 'Mail.Read')
        self.assertTrue(caught.exception.category.startswith('outlook:microsoft_signin_expired'))
        self.assertEqual(caught.exception.retry_after, 3600)

    def test_owner_reconnect_wins_over_inflight_refresh(self):
        ms_graph.save_signin(self.path, 'old-refresh', ['User.Read'])
        started, finished = threading.Event(), threading.Event()
        blocked, workers = [], []
        def reconnect():
            started.set()
            ms_graph.save_signin(self.path, 'owner-reconnect', ['User.Read'])
            finished.set()
        def answer(*args, **kwargs):
            worker = threading.Thread(target=reconnect)
            workers.append(worker)
            worker.start()
            self.assertTrue(started.wait(1))
            blocked.append(not finished.wait(.05))
            return {'access_token': 'test-access', 'refresh_token': 'late-rotation'}
        try:
            with mock.patch.object(ms_graph, '_post_form', side_effect=answer):
                ms_graph._direct(self.config, self.account, 'User.Read')
        finally:
            for worker in workers:
                worker.join(2)
        self.assertEqual(blocked, [True])
        self.assertTrue(finished.is_set())
        self.assertEqual(ms_graph._saved(self.path)['refresh_token'], 'owner-reconnect')

    def test_signin_save_does_not_follow_an_old_temporary_symlink(self):
        elsewhere = Path(self.temp.name) / 'unrelated'
        elsewhere.write_text('leave me')
        self.path.with_name(self.path.name + '.tmp').symlink_to(elsewhere)
        ms_graph.save_signin(self.path, 'new-test-refresh', ['User.Read'])
        self.assertEqual(elsewhere.read_text(), 'leave me')
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_setup_names_what_is_missing(self):
        self.assertEqual(onboarding.missing(self.config, self.account), 'no microsoft-alex-acme-test credential yet')
        ms_graph.save_signin(self.path, 'r1', {'User.Read', 'Mail.Read'})
        self.assertEqual(onboarding.missing(self.config, self.account), '')
        self.assertEqual(onboarding.missing({**self.config, 'microsoft_graph': {}}, self.account), 'microsoft_graph client_id is not set')
        broker = {**self.account, 'transport': 'broker'}
        self.assertEqual(onboarding.missing({'credentials': {}}, broker), 'microsoft_broker url is not set')
        self.assertEqual(onboarding.label('outlook'), 'Outlook')
        self.assertEqual(onboarding.label('outlook_calendar'), 'Outlook Calendar')
        account = onboarding.new_account({'accounts': [], 'credentials': {}, 'database': str(Path(self.temp.name) / 'x.sqlite')}, 'outlook_calendar')
        self.assertEqual((account['service'], account['calendar_id']), ('outlook_calendar', 'primary'))


if __name__ == '__main__':
    unittest.main()

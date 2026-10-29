"""Google Meet (connectors/google_meet.py), faked end to end: the token broker, the Meet REST API and the Docs API. No live
calls. It reads with Meet's own Google sign-in (its own broker, apart from Gmail's) and only two read-only scopes,
meetings.space.readonly and documents.readonly, never Gmail's and never a Drive scope; it writes nothing."""
import copy
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

import assistant
import fleet
import google_api
import mail_grants
import onboarding
from test_connectors import a, Response
from connectors import google_meet as meet

OWNER = 'owner@acme.example'
NOW = '2026-10-28T12:00:00+00:00'
START = '2026-10-27T09:00:00+00:00'
GMAIL = {'id': 'acme-gmail', 'service': 'gmail', 'email': OWNER, 'transport': 'broker', 'boundary': 'work:Acme'}
ACCOUNT = {**meet.SETUP['account'], 'email': OWNER, 'boundary': 'work:Acme'}
RECORD = {'name': 'conferenceRecords/record-1', 'startTime': START,
          'endTime': '2026-10-27T10:00:00Z', 'space': 'spaces/space-1'}
PEOPLE = {'participants': [
    {'name': RECORD['name'] + '/participants/p1', 'signedinUser': {'user': 'users/1', 'displayName': 'Robin Reviewer'}},
    {'name': RECORD['name'] + '/participants/p2', 'anonymousUser': {'displayName': 'Guest Sam'}}]}


def artifact(collection='transcripts', number=1, **fields):
    return {'name': RECORD['name'] + '/' + collection + '/artifact-' + str(number),
            'state': 'FILE_GENERATED', 'startTime': '2026-10-27T09:05:00Z',
            'docsDestination': {'document': collection + '-doc-' + str(number),
                                'exportUri': 'https://example.invalid/not-followed'}, **fields}


def entry(number, speaker, text):
    return {'name': f'{RECORD["name"]}/transcripts/artifact-1/entries/e{number}', 'participant': RECORD['name'] + '/participants/' + speaker,
            'text': text, 'languageCode': 'en-US', 'startTime': '2026-10-27T09:05:00Z', 'endTime': '2026-10-27T09:05:05Z'}


def document(text):
    """A Docs API document whose first tab holds `text`, one paragraph per line."""
    return {'documentId': 'x', 'body': {'content': [{'paragraph': {'elements': [{'textRun': {'content': line + '\n'}}]}}
                                                    for line in text.split('\n')]}}


def helpers_for(now=NOW):
    return types.SimpleNamespace(SourceError=a.SourceError, now=lambda: now,
                                 credential=lambda config, name: 'machine-token' if name == 'google_meet-broker' else 1 / 0)


class Fake:
    """The broker, Meet and Docs. Records every request; only the broker sees a refresh token."""

    def __init__(self, test):
        self.test, self.requests, self.granted = test, [], set(meet.SCOPES)
        self.conferences = {'': {'conferenceRecords': [copy.deepcopy(RECORD)]}}
        self.artifacts = {('transcripts', ''): {'transcripts': [artifact()]},
                          ('smartNotes', ''): {'smartNotes': [artifact('smartNotes')]}}
        self.entries = {('artifact-1', ''): {'transcriptEntries': [entry(1, 'p1', 'Discuss the example release.'),
                                                                   entry(2, 'p1', 'Then the checklist.'),
                                                                   entry(3, 'p2', 'Ready.')]}}
        self.documents = {'smartNotes-doc-1': document('Summary: Example release.\nNext step: Review the checklist. ✓')}
        self.people = copy.deepcopy(PEOPLE)
        self.overrides = {}

    def respond(self, request, data=None, timeout=None):
        url = urllib.parse.urlsplit(request.full_url)
        body = json.loads(request.data) if request.data else None
        if url.netloc == 'cp.example':
            self.test.assertEqual(url.path, '/api/google-meet/token')  # Meet's own broker, never the mail one
            self.requests.append(('BROKER', body.get('scope'), {}))
            if not body.get('scope'):
                return Response(json.dumps({'scopes': sorted(self.granted)}).encode())
            if body['scope'] not in self.granted:
                raise urllib.error.HTTPError(request.full_url, 403, 'no', {}, io.BytesIO(b''))
            self.test.assertEqual(body['refresh_token'], 'refresh-1')
            return Response(json.dumps({'access_token': 'access', 'expires_in': 3600}).encode())
        self.test.assertEqual(request.get_method(), 'GET')
        self.test.assertIsNone(request.data)
        self.test.assertEqual(request.get_header('Authorization'), 'Bearer access')
        self.test.assertIn(url.netloc, ('meet.googleapis.com', 'docs.googleapis.com'))  # never Drive, never Gmail
        self.test.assertNotIn('refresh', request.full_url)
        params = urllib.parse.parse_qs(url.query)
        token = params.get('pageToken', [''])[0]
        self.requests.append((url.netloc, url.path, params))
        path = url.path
        if (path, token) in self.overrides:
            answer = self.overrides[(path, token)]
        elif path == '/v2/conferenceRecords':
            answer = self.conferences[token]
        elif path.startswith('/v1/documents/'):
            answer = self.documents[path.rsplit('/', 1)[1]]
        elif path.endswith('/participants'):
            answer = self.people
        elif path.endswith('/entries'):
            answer = self.entries[(path.split('/')[-2], token)]
        else:
            answer = self.artifacts[(path.rsplit('/', 1)[-1], token)]
        if isinstance(answer, Exception):
            raise answer
        return Response(answer if isinstance(answer, bytes) else json.dumps(answer).encode())

    def scopes(self):
        return {r[1] for r in self.requests if r[0] == 'BROKER' and r[1]}


class GoogleMeetTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'google_broker': {'url': 'https://cp.example/api/google/token'},
                       'google_meet_broker': {'url': 'https://cp.example/api/google-meet/token'}, 'accounts': [GMAIL, ACCOUNT]}
        mail_grants.put(self.config, 'google', OWNER, 'mail-refresh')  # Gmail's own: never sent for Meet
        mail_grants.put(self.config, 'google_meet', OWNER, 'refresh-1')
        google_api._tokens.clear()
        self.addCleanup(google_api._tokens.clear)
        self.fake = Fake(self)
        self.helpers = helpers_for()
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)

    def sync(self, config=None):
        return meet.sync(self.store, {**self.config, **(config or {})}, ACCOUNT, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM events ORDER BY kind,source_id')]

    def error(self, code=400):
        return urllib.error.HTTPError('https://example.invalid/', code, 'private error text', {}, io.BytesIO(b'{"private": 1}'))

    def test_notes_and_transcripts_with_the_two_read_only_scopes_only(self):
        result = self.sync()
        self.assertEqual(result, {'mode': 'incremental', 'events': 2, 'more': False})
        notes, transcript = self.rows()
        self.assertEqual((notes['kind'], transcript['kind']), ('google_meet.notes', 'google_meet.transcript'))
        self.assertEqual(notes['body'], 'Summary: Example release.\nNext step: Review the checklist. ✓')
        # one line per turn, by the name Meet shows, consecutive entries of one speaker together
        self.assertEqual(transcript['body'], 'Robin Reviewer: Discuss the example release. Then the checklist.\nGuest Sam: Ready.')
        for row in (notes, transcript):
            meta = json.loads(row['metadata'])
            self.assertEqual(row['occurred_at'], '2026-10-27T09:05:00+00:00')
            self.assertEqual(row['account_id'], ACCOUNT['id'])
            self.assertRegex(row['source_id'], r'^[0-9a-f]{64}$')
            self.assertRegex(meta['thread_id'], r'^[0-9a-f]{64}$')
            self.assertTrue(meta['source_url'].startswith('https://docs.google.com/document/d/'))
            self.assertFalse(meta['truncated'])
            self.assertEqual((meta['start_at'], meta['end_at']), (START, '2026-10-27T10:00:00+00:00'))  # the call's times, to match its meeting
        self.assertEqual(self.fake.scopes(), set(meet.SCOPES))  # never a Gmail scope, never Drive
        self.assertEqual(meet.SCOPES, ('https://www.googleapis.com/auth/meetings.space.readonly',
                                       'https://www.googleapis.com/auth/documents.readonly'))
        docs_calls = [r for r in self.fake.requests if r[0] == 'docs.googleapis.com']
        self.assertEqual([r[1] for r in docs_calls], ['/v1/documents/smartNotes-doc-1'])  # the notes doc, by its id
        self.assertEqual(self.fake.requests[1][2]['filter'], [
            'start_time>="2026-10-21T12:00:00+00:00" AND start_time<="2026-10-28T12:00:00+00:00"'])
        self.assertEqual(a.source_kind('google_meet.notes'), 'Meet notes')

    def test_plugin_dispatch_reads_through_the_broker(self):
        with patch.object(a.CONNECTOR_HELPERS, 'credential', lambda config, name: 'machine-token'), \
                patch.object(a.CONNECTOR_HELPERS, 'now', return_value=NOW):
            self.assertEqual(a.sync_source(self.store, self.config, ACCOUNT)['events'], 2)

    def test_replays_are_idempotent_and_edits_version_the_same_artifact(self):
        self.sync()
        original_ids = {row['kind']: row['source_id'] for row in self.rows()}
        self.sync()
        self.assertEqual([row['version'] for row in self.rows()], [1, 1])
        self.fake.documents['smartNotes-doc-1'] = document('Updated example notes.')
        self.sync()
        rows = self.rows()
        self.assertEqual([row['version'] for row in rows], [2, 1])
        self.assertEqual({row['kind']: row['source_id'] for row in rows}, original_ids)

    def test_pending_artifacts_are_revisited_without_writes(self):
        self.fake.artifacts[('smartNotes', '')]['smartNotes'][0]['state'] = 'ENDED'
        self.assertEqual(self.sync()['events'], 1)
        self.fake.artifacts[('smartNotes', '')]['smartNotes'][0]['state'] = 'FILE_GENERATED'
        self.assertEqual(self.sync()['events'], 2)
        self.assertEqual(len(self.rows()), 2)

    def test_transcript_entries_page_and_a_transcript_without_a_doc_still_reads(self):
        self.fake.entries[('artifact-1', '')]['nextPageToken'] = 'more'
        self.fake.entries[('artifact-1', 'more')] = {'transcriptEntries': [entry(4, 'p9', 'Someone joined by phone.')]}
        self.fake.artifacts[('transcripts', '')] = {'transcripts': [artifact(docsDestination=None)]}
        self.sync()
        transcript = next(r for r in self.rows() if r['kind'] == 'google_meet.transcript')
        self.assertTrue(transcript['body'].endswith('Guest Sam: Ready.\nSomeone: Someone joined by phone.'))
        self.assertNotIn('source_url', json.loads(transcript['metadata']))
        entries = [r for r in self.fake.requests if r[1].endswith('/entries')]
        self.assertEqual(entries[0][2]['pageSize'], ['100'])
        self.assertEqual(len([r for r in self.fake.requests if r[1].endswith('/participants')]), 1)  # once per conference

    def test_conference_and_artifact_pagination_resume_across_runs(self):
        self.fake.conferences['']['nextPageToken'] = 'conferences-next'
        self.fake.conferences['conferences-next'] = {}  # Google omits empty repeated fields.
        self.fake.artifacts[('transcripts', '')]['nextPageToken'] = 'transcripts-next'
        self.fake.artifacts[('transcripts', 'transcripts-next')] = {'transcripts': [artifact(number=2)]}
        self.fake.entries[('artifact-2', '')] = {'transcriptEntries': [entry(1, 'p2', 'Second transcript session.')]}
        with patch.object(meet, 'PAGES', 2):
            self.assertTrue(self.sync()['more'])
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertEqual(state['window']['artifact_token'], 'transcripts-next')
        self.assertEqual(state['window']['conference_token'], 'conferences-next')
        self.assertNotIn('Discuss the example release', json.dumps(state))
        self.helpers.now = lambda: '2026-10-29T12:00:00+00:00'
        self.assertFalse(self.sync()['more'])
        self.assertEqual(len(self.rows()), 3)
        self.assertEqual(self.store.checkpoint(ACCOUNT['id'])['since'], NOW)
        self.assertEqual([r for r in self.fake.requests if r[1] == '/v2/conferenceRecords'][-1][2]['pageToken'], ['conferences-next'])

    def test_empty_pages_with_continuations_are_not_dropped(self):
        self.fake.conferences = {'': {'nextPageToken': 'next'}, 'next': {'conferenceRecords': [RECORD]}}
        self.fake.artifacts[('smartNotes', '')] = {'nextPageToken': 'notes-next'}
        self.fake.artifacts[('smartNotes', 'notes-next')] = {'smartNotes': [artifact('smartNotes')]}
        self.assertEqual(self.sync()['events'], 2)

    def test_setup_check_needs_both_scopes_and_stores_nothing(self):
        self.assertIsNone(meet.check(self.config, ACCOUNT, self.helpers))
        self.assertEqual(self.rows(), [])
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        for missing in meet.SCOPES:  # granted Meet but not Docs (or the other way): not added, whatever the meetings
            with self.subTest(missing=missing):
                self.fake.granted = set(meet.SCOPES) - {missing}
                with self.assertRaisesRegex(a.SourceError, '^google_meet_not_connected:HTTP_403$'):
                    meet.check(self.config, ACCOUNT, self.helpers)
        self.fake.granted, self.fake.conferences = set(meet.SCOPES), {'': {}}
        self.assertIsNone(meet.check(self.config, ACCOUNT, self.helpers))

    def test_a_scope_taken_back_or_a_revoked_sign_in_says_what_to_do(self):
        self.fake.granted = {meet.DOCS_SCOPE}
        with self.assertRaisesRegex(a.SourceError, '^google_meet_not_connected:HTTP_403$'):
            self.sync()
        self.fake.granted = set(meet.SCOPES)
        google_api._tokens.clear()
        self.fake.overrides[('/v2/conferenceRecords', '')] = self.error(401)
        with self.assertRaisesRegex(a.SourceError, '^google_meet_signin_expired:HTTP_401$'):
            self.sync()
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        self.assertEqual(meet.SETUP['hints']['google_meet_not_connected'], 'Connect Google Meet again')

    def test_no_meet_sign_in_reads_nothing_and_never_borrows_gmails(self):
        for account, config in (({**ACCOUNT, 'transport': 'api', 'credential': 'google_meet'}, self.config),  # a token pasted before
                                ({**ACCOUNT, 'email': ''}, self.config),
                                (ACCOUNT, {**self.config, 'google_meet_broker': {}})):  # Gmail is here, Meet's sign-in isn't
            with self.subTest(account=account, broker=config['google_meet_broker']):
                with self.assertRaisesRegex(a.SourceError, '^google_meet_not_connected'):
                    meet.sync(self.store, config, account, self.helpers)
        self.assertEqual(self.fake.requests, [])
        mail_grants.forget(self.config, 'google_meet', OWNER, revoke=False)
        self.fake.granted = set()
        with self.assertRaisesRegex(a.SourceError, '^google_meet_not_connected'):
            meet.check(self.config, ACCOUNT, self.helpers)

    def test_expired_cursor_replays_bounded_window_and_discloses_gap(self):
        self.fake.conferences['']['nextPageToken'] = 'old-token'
        with patch.object(meet, 'PAGES', 3):
            self.sync()
        self.fake.overrides[('/v2/conferenceRecords', 'old-token')] = self.error(400)
        self.fake.conferences[''].pop('nextPageToken')
        self.assertFalse(self.sync()['more'])
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertEqual(state['cursor_expired_at'], NOW)
        self.assertIn('older pending artifacts', state['coverage_gap'])
        self.assertFalse(state['coverage_complete'])
        self.assertEqual(len(self.rows()), 2)

    def test_transient_errors_keep_the_last_good_checkpoint(self):
        self.fake.conferences['']['nextPageToken'] = 'old-token'
        with patch.object(meet, 'PAGES', 3):
            self.sync()
        state = self.store.checkpoint(ACCOUNT['id'])
        for outcome, label, delay in ((self.error(429), 'google_meet_http:HTTP_429', 60),
                                      (self.error(500), 'google_meet_http:HTTP_500', None),
                                      (urllib.error.URLError('private network text'), 'google_meet_network', None)):
            with self.subTest(label=label):
                self.fake.overrides[('/v2/conferenceRecords', 'old-token')] = outcome
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertEqual(str(caught.exception), label)
                self.assertEqual(caught.exception.retry_after, delay)
                self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)

    def test_a_400_without_a_page_token_is_no_cursor_expiry(self):
        self.fake.overrides[('/v2/conferenceRecords', '')] = self.error(400)
        with self.assertRaisesRegex(a.SourceError, '^google_meet_http:HTTP_400$'):
            self.sync()
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_invalid_json_and_page_shapes_are_safe_errors(self):
        for answer in (b'{private', b'\xff', [], {'conferenceRecords': 'private'},
                       {'conferenceRecords': [None]}, {'nextPageToken': 12}):
            with self.subTest(answer=answer):
                self.fake.overrides[('/v2/conferenceRecords', '')] = answer
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertIn(caught.exception.category, ('google_meet_invalid_response', 'google_meet_invalid_page'))
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_same_cursor_is_rejected(self):
        self.fake.conferences[''] = {'nextPageToken': 'same'}
        self.fake.conferences['same'] = {'nextPageToken': 'same'}
        with self.assertRaisesRegex(a.SourceError, '^google_meet_invalid_page$'):
            self.sync()

    def test_invalid_resource_names_timestamps_and_document_ids_are_rejected(self):
        for field, value in (('name', 'https://example.invalid/'), ('startTime', 'private text')):
            with self.subTest(field=field):
                self.fake.conferences[''] = {'conferenceRecords': [{**RECORD, field: value}]}
                with self.assertRaises(a.SourceError):
                    self.sync()
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        self.fake.conferences[''] = {'conferenceRecords': [RECORD]}
        for collection, item in (('smartNotes', artifact('smartNotes', docsDestination={'document': '../private'})),
                                 ('smartNotes', artifact('smartNotes', docsDestination={})),
                                 ('transcripts', artifact(docsDestination={'document': '../private'})),
                                 ('transcripts', artifact(name='conferenceRecords/other/transcripts/artifact-1'))):
            with self.subTest(item=item):
                with self.store.connect() as db:
                    db.execute('DELETE FROM events')
                    db.execute('DELETE FROM checkpoints')
                other = 'transcripts' if collection == 'smartNotes' else 'smartNotes'
                self.fake.artifacts[(other, '')] = {}
                self.fake.artifacts[(collection, '')] = {collection: [item]}
                with self.assertRaises(a.SourceError):
                    self.sync()
                self.assertEqual(self.rows(), [])
        self.assertFalse([r for r in self.fake.requests if 'private' in r[1]])

    def test_only_fixed_get_methods_on_googles_hosts(self):
        for method in ('meet.conferenceRecords.delete', 'drive.files.export.meet', 'gmail.users.messages.send'):
            with self.subTest(method=method), self.assertRaises(google_api.BrokerError):
                google_api.url_for(method, {})
        verb, url = google_api.url_for('meet.conferenceRecords.transcripts.entries.list',
                                       {'conference': 'r/../x', 'transcript': 't', 'pageSize': 100})
        self.assertEqual(verb, 'GET')
        self.assertEqual(url, 'https://meet.googleapis.com/v2/conferenceRecords/r%2F..%2Fx/transcripts/t/entries?pageSize=100')
        self.assertTrue(all(v[0] == 'GET' for k, v in google_api.READ.items() if k.startswith('meet.')))
        self.assertFalse([k for k in google_api.WRITE if k.startswith(('meet.', 'docs.'))])

    def test_response_limits_and_clipping_are_explicit(self):
        self.fake.entries[('artifact-1', '')] = {'transcriptEntries': [entry(1, 'p1', 'x' * 400_001)]}
        self.fake.documents['smartNotes-doc-1'] = document('y' * 40_001)
        self.sync()
        row = next(row for row in self.rows() if row['kind'].endswith('transcript'))
        self.assertEqual(len(row['body']), 400_000)
        self.assertTrue(json.loads(row['metadata'])['truncated'])
        notes = next(row for row in self.rows() if row['kind'].endswith('notes'))
        self.assertEqual(len(notes['body']), 40_000)
        with patch.object(meet, 'MAX_BYTES', 10):
            with self.assertRaisesRegex(a.SourceError, '^google_meet_response_too_large$'):
                self.sync()

    def test_the_notes_doc_reads_tables_people_and_links_as_text(self):
        para = lambda *parts: {'paragraph': {'elements': list(parts)}}
        doc = {'body': {'content': [
            {'sectionBreak': {}},
            para({'textRun': {'content': 'Attendees: '}}, {'person': {'personProperties': {'name': 'Robin Reviewer', 'email': 'robin@x.example'}}},
                 {'textRun': {'content': '\n'}}),
            {'table': {'tableRows': [{'tableCells': [{'content': [para({'textRun': {'content': 'Action\n'}})]},
                                                     {'content': [para({'textRun': {'content': 'Owner\n'}})]}]}]}},
            para({'richLink': {'richLinkProperties': {'title': 'Q4 plan', 'uri': 'https://docs.google.com/x'}}}, {'textRun': {'content': '\n'}})]}}
        self.assertEqual(meet.doc_text(doc['body']['content']), 'Attendees: Robin Reviewer\nAction\nOwner\nQ4 plan\n')
        self.assertEqual(meet.doc_text(None), '')
        self.assertEqual(meet.doc_text([{'paragraph': {'elements': [None, {'textRun': {'content': 5}}]}}]), '')

    def test_explicitly_labeled_sensitive_values_are_omitted(self):
        self.fake.documents['smartNotes-doc-1'] = document('password: example-placeholder\notp=000000\nOrdinary notes remain.')
        self.sync()
        row = next(row for row in self.rows() if row['kind'].endswith('notes'))
        self.assertEqual(row['body'], 'password: [omitted]\notp: [omitted]\nOrdinary notes remain.')

    def test_outage_catches_up_from_last_completed_window_with_retention_limit(self):
        for since, expected_after, gap in (
                ('2026-10-10T12:00:00+00:00', '2026-10-10T11:59:59+00:00', False),
                ('2026-08-01T12:00:00+00:00', '2026-09-28T12:00:00+00:00', True)):
            with self.subTest(since=since):
                self.store.commit_page(ACCOUNT['id'], {'since': since}, [])
                self.fake.conferences = {'': {}}
                self.sync()
                listed = [r for r in self.fake.requests if r[1] == '/v2/conferenceRecords']
                self.assertIn(expected_after, listed[-1][2]['filter'][0])
                self.assertEqual(bool(self.store.checkpoint(ACCOUNT['id']).get('coverage_gap')), gap)

    def test_old_and_future_records_are_not_imported_and_retention_is_disclosed(self):
        self.fake.conferences[''] = {'conferenceRecords': [
            {**RECORD, 'startTime': '2026-01-01T00:00:00Z'},
            {**RECORD, 'startTime': '2027-01-01T00:00:00Z'}]}
        self.assertEqual(self.sync({'bootstrap_days': 365})['events'], 0)
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertIn('30 days', state['coverage_gap'])
        self.assertFalse(state['coverage_complete'])

    def test_setup_signs_in_with_google_and_never_asks_for_a_token(self):
        self.assertEqual(meet.SETUP['account']['transport'], 'broker')
        self.assertNotIn('secret', meet.SETUP)
        text = json.dumps(meet.SETUP)
        for gone in ('oauthplayground', 'drive.meet.readonly', 'console.cloud.google.com', 'access token'):
            self.assertNotIn(gone, text)
        self.assertLessEqual(len(meet.SETUP['note']), 120)
        self.assertLessEqual(len(meet.SETUP['what']), 70)
        self.assertNotIn('—', text)


class SignIn(unittest.TestCase):
    """Connect Google Meet: + Add on a hosted Machine (its control plane's form), or through the control plane on a
    paired self-hosted one, which hands Meet's own sign-in over (onboarding.connect_grant). Gmail isn't needed."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'fleet.token').write_text('fixture-device-token\n')
        self.path = self.root / 'config.json'
        self.path.write_text(json.dumps({'database': str(self.root / 'events.sqlite'), 'credentials': {'fleet': str(self.root / 'fleet.token')},
                                         'fleet': {'url': 'https://cp.example/api/fleet'}, 'accounts': []}))
        self.checked, self.answer = [], None
        patch.object(onboarding, 'assistant', return_value=a).start()
        patch.object(onboarding, 'check', side_effect=lambda config, account: self.checked.append(dict(account)) or self.answer).start()
        self.addCleanup(patch.stopall)

    def config(self):
        return json.loads(self.path.read_text())

    def test_a_paired_machine_keeps_meets_own_sign_in_without_gmail(self):
        grant = {'provider': 'google_meet', 'email': OWNER, 'refresh_token': 'fixture-refresh-token-meet', 'scopes': list(meet.SCOPES)}
        args = {'source': 'google_meet', 'grant': grant}
        self.answer = 'google_meet_not_connected'  # Google didn't allow it after all: nothing is kept
        with self.assertRaisesRegex(onboarding.SetupError, 'did not check out'):
            onboarding.connect_delivered(self.path, args)
        self.assertIsNone(mail_grants.get(self.config(), 'google_meet', OWNER))
        self.assertNotIn('google_meet', [x['service'] for x in self.config()['accounts']])
        self.answer = None
        self.assertEqual(onboarding.connect_delivered(self.path, args), {'ok': True, 'name': OWNER})  # no Gmail here
        config = self.config()
        [account] = config['accounts']
        self.assertEqual((account['service'], account['email'], account['transport'], account['boundary']),
                         ('google_meet', OWNER, 'broker', 'work:Acme'))
        self.assertNotIn('credential', account)
        self.assertEqual(config['google_meet_broker'], {'url': 'https://cp.example/api/fleet/google_meet-token'})
        self.assertEqual(config['credentials']['google_meet-broker'], config['credentials']['fleet'])
        self.assertEqual(mail_grants.get(config, 'google_meet', OWNER), 'fixture-refresh-token-meet')
        self.assertIsNone(mail_grants.get(config, 'google', OWNER))  # never a mail sign-in
        self.assertNotIn('google_broker', config)
        self.assertNotIn('fixture-refresh-token-meet', self.path.read_text())
        self.assertEqual(self.checked[-1]['service'], 'google_meet')  # checked with a real read before it is kept
        onboarding.connect_delivered(self.path, args)
        self.assertEqual(len([x for x in self.config()['accounts'] if x['service'] == 'google_meet']), 1)  # again: the same one
        with self.assertRaises(onboarding.SetupError):
            onboarding.connect_delivered(self.path, {'source': 'google_meet', 'grant': {**grant, 'provider': 'google'}})

    def test_the_sign_in_is_offered_where_it_works(self):
        self.assertIn('google_meet', fleet.SIGNIN_SOURCES)
        self.assertEqual(fleet.SIGNIN_OF['google_meet'], 'google_meet')
        self.assertIn('google_meet', assistant.HOSTED_SIGNINS)
        self.assertIn('google_meet', mail_grants.PROVIDERS)
        hosted = {'manage_url': 'https://cp.example/setup', 'accounts': []}
        self.assertNotIn('google_meet', [s['service'] for s in onboarding.catalog(hosted)])  # until its control plane has the app
        meet_broker = {'google_meet_broker': {'url': 'https://cp.example/api/google-meet/token'}}
        self.assertIn('google_meet', [s['service'] for s in onboarding.catalog({**hosted, **meet_broker})])
        self.assertIn('google_meet', [s['service'] for s in onboarding.catalog({'accounts': []})])  # self-hosted
        self.assertEqual(onboarding.missing({'credentials': {}}, ACCOUNT), 'google_meet_broker url is not set')
        account = {**ACCOUNT, 'id': 'acme-meet'}
        self.assertEqual(assistant.reconnect_help(account, hosted['manage_url']),
                         {'account_page': 'https://cp.example/setup#source-google_meet', 'hosted_signin': 'google_meet'})
        self.assertEqual(assistant.reconnect_help(account, None), {'connect_name': 'google_meet'})
        html = (Path(assistant.__file__).parent / 'dashboard.html').read_text(encoding='utf-8')
        self.assertIn("google_meet:{label:'Google',title:'Google Meet',about:'Transcripts and Gemini notes of your meetings. Reads only.'}", html)
        self.assertNotIn('Connect Gmail', html)

    def test_disconnect_revokes_meets_own_sign_in_at_google(self):
        config = {'database': str(self.root / 'events.sqlite')}
        mail_grants.put(config, 'google_meet', OWNER, 'fixture-refresh-token-meet')
        mail_grants.put(config, 'google', OWNER, 'fixture-refresh-token-mail')
        with patch.object(mail_grants, '_revoke_google', return_value=True) as revoke:
            self.assertEqual(mail_grants.forget(config, 'google_meet', OWNER), 'revoked')
        revoke.assert_called_once_with('fixture-refresh-token-meet')
        self.assertEqual(mail_grants.get(config, 'google', OWNER), 'fixture-refresh-token-mail')  # Gmail's stays


if __name__ == '__main__':
    unittest.main()

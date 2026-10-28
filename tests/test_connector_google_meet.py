"""Synthetic Meet/Drive responses only; no live calls or credential files."""
import copy
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
import urllib.request
from unittest.mock import Mock, patch

from test_connectors import a, Response
from connectors import google_meet as meet

NOW = '2026-10-28T12:00:00+00:00'
START = '2026-10-27T09:00:00+00:00'
ACCOUNT = dict(meet.SETUP['account'])
RECORD = {'name': 'conferenceRecords/record-1', 'startTime': START,
          'endTime': '2026-10-27T10:00:00Z', 'space': 'spaces/space-1'}


def artifact(collection='transcripts', number=1, **fields):
    return {'name': RECORD['name'] + '/' + collection + '/artifact-' + str(number),
            'state': 'FILE_GENERATED', 'startTime': '2026-10-27T09:05:00Z',
            'docsDestination': {'document': collection + '-doc-' + str(number),
                                'exportUri': 'https://example.invalid/not-followed'}, **fields}


class GoogleMeetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.credential = Mock(return_value='fixture-access-token')
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError,
                                             credential=self.credential, now=lambda: NOW)
        self.requests = []
        self.conferences = {'': {'conferenceRecords': [copy.deepcopy(RECORD)]}}
        self.artifacts = {('transcripts', ''): {'transcripts': [artifact()]},
                          ('smartNotes', ''): {'smartNotes': [artifact('smartNotes')]}}
        self.documents = {'transcripts-doc-1': 'Speaker 1: Discuss the example release.\nSpeaker 2: Ready.',
                          'smartNotes-doc-1': 'Summary: Example release.\nNext step: Review the checklist. ✓'}
        self.overrides = {}
        self.http = patch.object(urllib.request.OpenerDirector, 'open', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        self.assertEqual(request.get_method(), 'GET')
        self.assertIsNone(request.data)
        self.assertEqual(timeout, 30)
        self.assertEqual(request.get_header('Authorization'), 'Bearer fixture-access-token')
        self.assertNotIn('fixture-access-token', request.full_url)
        url = urllib.parse.urlsplit(request.full_url)
        self.assertEqual(url.scheme, 'https')
        self.assertIn(url.netloc, ('meet.googleapis.com', 'www.googleapis.com'))
        params = urllib.parse.parse_qs(url.query)
        token = params.get('pageToken', [''])[0]
        self.requests.append((url.netloc, url.path, params))
        if (url.path, token) in self.overrides:
            answer = self.overrides[(url.path, token)]
        elif url.path == '/v2/conferenceRecords':
            answer = self.conferences[token]
        elif url.path.startswith('/v2/' + RECORD['name'] + '/'):
            collection = url.path.rsplit('/', 1)[-1]
            answer = self.artifacts[(collection, token)]
        else:
            self.assertTrue(url.path.startswith('/drive/v3/files/'))
            self.assertTrue(url.path.endswith('/export'))
            self.assertEqual(params, {'mimeType': ['text/plain']})
            answer = self.documents[url.path.split('/')[-2]].encode('utf-8')
        if isinstance(answer, Exception):
            raise answer
        return Response(answer if isinstance(answer, bytes) else json.dumps(answer).encode())

    def sync(self, config=None):
        return meet.sync(self.store, config or {}, ACCOUNT, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM events ORDER BY kind,source_id')]

    def error(self, code=400, message='Invalid page token', headers=None):
        return urllib.error.HTTPError('https://example.invalid/', code, 'private error text',
                                      headers or {}, io.BytesIO(json.dumps({'error': {'message': message}}).encode()))

    def test_notes_and_transcripts_and_plugin_dispatch(self):
        with patch.object(a.CONNECTOR_HELPERS, 'credential', self.credential), patch.object(a.CONNECTOR_HELPERS, 'now', return_value=NOW):
            result = a.sync_source(self.store, {}, ACCOUNT)
        self.assertEqual(result, {'mode': 'incremental', 'events': 2, 'more': False})
        rows = self.rows()
        self.assertEqual([row['kind'] for row in rows], ['google_meet.notes', 'google_meet.transcript'])
        for row in rows:
            meta = json.loads(row['metadata'])
            self.assertEqual(row['occurred_at'], '2026-10-27T09:05:00+00:00')
            self.assertEqual(row['account_id'], ACCOUNT['id'])
            self.assertRegex(row['source_id'], r'^[0-9a-f]{64}$')
            self.assertRegex(meta['thread_id'], r'^[0-9a-f]{64}$')
            self.assertTrue(meta['source_url'].startswith('https://docs.google.com/document/d/'))
            self.assertFalse(meta['truncated'])
            self.assertFalse(row['deleted'])
        self.assertEqual(rows[0]['body'], self.documents['smartNotes-doc-1'])
        self.assertEqual(rows[1]['body'], self.documents['transcripts-doc-1'])
        self.assertEqual(a.source_kind('google_meet.notes'), 'Meet notes')
        self.assertEqual(self.requests[0][2]['filter'], [
            'start_time>="2026-10-21T12:00:00+00:00" AND start_time<="2026-10-28T12:00:00+00:00"'])
        self.credential.assert_called_once_with({}, 'google_meet')

    def test_replays_are_idempotent_and_edits_version_the_same_artifact(self):
        self.sync()
        original_ids = {row['kind']: row['source_id'] for row in self.rows()}
        self.sync()
        self.assertEqual([row['version'] for row in self.rows()], [1, 1])
        self.documents['smartNotes-doc-1'] = 'Updated example notes.'
        self.sync()
        rows = self.rows()
        self.assertEqual([row['version'] for row in rows], [2, 1])
        self.assertEqual({row['kind']: row['source_id'] for row in rows}, original_ids)

    def test_pending_artifacts_are_revisited_without_writes(self):
        self.artifacts[('smartNotes', '')]['smartNotes'][0]['state'] = 'ENDED'
        self.assertEqual(self.sync()['events'], 1)
        self.artifacts[('smartNotes', '')]['smartNotes'][0]['state'] = 'FILE_GENERATED'
        self.assertEqual(self.sync()['events'], 2)
        self.assertEqual(len(self.rows()), 2)

    def test_conference_and_artifact_pagination_resume_across_runs(self):
        self.conferences['']['nextPageToken'] = 'conferences-next'
        self.conferences['conferences-next'] = {}  # Google omits empty repeated fields.
        self.artifacts[('transcripts', '')]['nextPageToken'] = 'transcripts-next'
        self.artifacts[('transcripts', 'transcripts-next')] = {'transcripts': [artifact(number=2)]}
        self.documents['transcripts-doc-2'] = 'Second transcript session.'
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
        self.assertEqual(self.requests[-1][2]['pageToken'], ['conferences-next'])

    def test_empty_pages_with_continuations_are_not_dropped(self):
        self.conferences = {'': {'nextPageToken': 'next'}, 'next': {'conferenceRecords': [RECORD]}}
        self.artifacts[('smartNotes', '')] = {'nextPageToken': 'notes-next'}
        self.artifacts[('smartNotes', 'notes-next')] = {'smartNotes': [artifact('smartNotes')]}
        self.assertEqual(self.sync()['events'], 2)

    def test_empty_account_and_setup_probe_do_not_touch_checkpoints(self):
        self.conferences = {'': {}}
        self.assertIsNone(meet.check({}, ACCOUNT, self.helpers))
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        self.assertEqual(self.sync()['events'], 0)
        self.assertTrue(self.store.checkpoint(ACCOUNT['id'])['coverage_complete'])

    def test_setup_probe_reads_artifact_text_but_stores_nothing(self):
        self.assertIsNone(meet.check({}, ACCOUNT, self.helpers))
        self.assertEqual(len(self.requests), 5)
        self.assertEqual(self.rows(), [])
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_failed_export_keeps_the_last_page_for_atomic_replay(self):
        self.artifacts[('transcripts', '')]['transcripts'].append(artifact(number=2))
        self.documents['transcripts-doc-2'] = 'Second transcript session.'
        self.overrides[('/drive/v3/files/transcripts-doc-2/export', '')] = self.error(503)
        with self.assertRaises(a.SourceError):
            self.sync()
        self.assertEqual(self.rows(), [])
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertEqual(state['window']['collection'], 'transcripts')
        self.overrides.clear()
        self.assertEqual(self.sync()['events'], 3)
        self.assertEqual(len(self.rows()), 3)

    def test_failed_commit_does_not_advance_the_artifact_cursor(self):
        with patch.object(meet, 'PAGES', 1):
            self.sync()
        state = self.store.checkpoint(ACCOUNT['id'])
        with patch.object(self.store, 'commit_page', side_effect=RuntimeError('interrupted')):
            with self.assertRaises(RuntimeError):
                self.sync()
        self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)
        self.assertEqual(self.rows(), [])
        self.assertEqual(self.sync()['events'], 2)

    def retained_token(self):
        self.conferences['']['nextPageToken'] = 'old-token'
        with patch.object(meet, 'PAGES', 3):
            self.sync()
        return self.store.checkpoint(ACCOUNT['id'])

    def test_expired_cursor_replays_bounded_window_and_discloses_gap(self):
        self.retained_token()
        self.overrides[('/v2/conferenceRecords', 'old-token')] = self.error()
        self.conferences[''].pop('nextPageToken')
        self.assertFalse(self.sync()['more'])
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertEqual(state['cursor_expired_at'], NOW)
        self.assertIn('older pending artifacts', state['coverage_gap'])
        self.assertFalse(state['coverage_complete'])
        self.assertEqual(len(self.rows()), 2)
        self.assertEqual([row['version'] for row in self.rows()], [1, 1])

    def test_transient_errors_and_unrelated_400_keep_valid_continuation(self):
        state = self.retained_token()
        cases = [(self.error(429, headers={'Retry-After': '123'}), 'google_meet_http:HTTP_429', 123),
                 (self.error(400, 'Invalid filter'), 'google_meet_http:HTTP_400', None),
                 (self.error(410), 'google_meet_http:HTTP_410', None),
                 (urllib.error.URLError('private network text'), 'google_meet_network', None)]
        for outcome, label, delay in cases:
            with self.subTest(label=label):
                self.overrides[('/v2/conferenceRecords', 'old-token')] = outcome
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertEqual(str(caught.exception), label)
                self.assertEqual(caught.exception.retry_after, delay)
                self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)

    def test_auth_errors_are_safe_and_do_not_create_a_checkpoint(self):
        for code in (401, 403, 500):
            with self.subTest(code=code):
                self.overrides[('/v2/conferenceRecords', '')] = self.error(code, 'private service text')
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertEqual(str(caught.exception), 'google_meet_http:HTTP_' + str(code))
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_invalid_json_and_page_shapes_are_safe_errors(self):
        for answer in (b'{private', b'\xff', [], {'conferenceRecords': 'private'},
                       {'conferenceRecords': [None]}, {'nextPageToken': 12}):
            with self.subTest(answer=answer):
                self.overrides[('/v2/conferenceRecords', '')] = answer
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertIn(caught.exception.category, ('google_meet_invalid_response', 'google_meet_invalid_page'))
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_same_cursor_is_rejected_without_losing_last_good_checkpoint(self):
        state = self.retained_token()
        self.conferences['old-token'] = {'nextPageToken': 'old-token'}
        with self.assertRaisesRegex(a.SourceError, '^google_meet_invalid_page$'):
            self.sync()
        self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)

    def test_invalid_resource_paths_timestamps_and_document_ids_are_rejected(self):
        for field, value in (('name', 'https://example.invalid/'), ('startTime', 'private text')):
            with self.subTest(field=field):
                self.conferences[''] = {'conferenceRecords': [{**RECORD, field: value}]}
                with self.assertRaises(a.SourceError):
                    self.sync()
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        self.conferences[''] = {'conferenceRecords': [RECORD]}
        for item in (artifact(docsDestination={'document': '../private'}), artifact(docsDestination={}),
                     artifact(name='conferenceRecords/other/transcripts/artifact-1')):
            with self.subTest(item=item):
                self.artifacts[('transcripts', '')] = {'transcripts': [item]}
                with self.assertRaises(a.SourceError):
                    self.sync()
                self.assertEqual(self.rows(), [])

    def test_response_limits_and_document_clipping_are_explicit(self):
        self.documents['transcripts-doc-1'] = 'x' * 40001
        self.sync()
        row = next(row for row in self.rows() if row['kind'].endswith('transcript'))
        self.assertEqual(len(row['body']), 40000)
        self.assertTrue(json.loads(row['metadata'])['truncated'])
        self.assertEqual(json.loads(row['metadata'])['body_chars'], 40001)
        with patch.object(meet, 'MAX_BYTES', 10):
            with self.assertRaisesRegex(a.SourceError, '^google_meet_response_too_large$'):
                self.sync()

    def test_explicitly_labeled_sensitive_values_are_omitted(self):
        self.documents['smartNotes-doc-1'] = 'password: example-placeholder\notp=000000\nOrdinary notes remain.'
        self.sync()
        row = next(row for row in self.rows() if row['kind'].endswith('notes'))
        self.assertEqual(row['body'], 'password: [omitted]\notp: [omitted]\nOrdinary notes remain.')

    def test_outage_catches_up_from_last_completed_window_with_retention_limit(self):
        for since, expected_after, gap in (
                ('2026-10-10T12:00:00+00:00', '2026-10-10T11:59:59+00:00', False),
                ('2026-08-01T12:00:00+00:00', '2026-09-28T12:00:00+00:00', True)):
            with self.subTest(since=since):
                self.store.commit_page(ACCOUNT['id'], {'since': since}, [])
                self.conferences = {'': {}}
                self.sync()
                self.assertIn(expected_after, self.requests[-1][2]['filter'][0])
                self.assertEqual(bool(self.store.checkpoint(ACCOUNT['id']).get('coverage_gap')), gap)

    def test_old_and_future_records_are_not_imported_and_retention_is_disclosed(self):
        self.conferences[''] = {'conferenceRecords': [
            {**RECORD, 'startTime': '2026-01-01T00:00:00Z'},
            {**RECORD, 'startTime': '2027-01-01T00:00:00Z'}]}
        self.assertEqual(self.sync({'bootstrap_days': 365})['events'], 0)
        self.assertEqual(len(self.requests), 1)
        state = self.store.checkpoint(ACCOUNT['id'])
        self.assertIn('30 days', state['coverage_gap'])
        self.assertFalse(state['coverage_complete'])
        self.assertIn('2026-09-28', self.requests[0][2]['filter'][0])

    def test_credentials_only_come_from_helper_and_bad_values_are_safe(self):
        for value in ('', 'token\nInjected: header', None):
            with self.subTest(value=value):
                self.credential.return_value = value
                with self.assertRaisesRegex(a.SourceError, '^google_meet_credential_unavailable$'):
                    self.sync()
        self.credential.side_effect = RuntimeError('private credential details')
        with self.assertRaisesRegex(a.SourceError, '^google_meet_credential_unavailable$'):
            self.sync()
        self.assertEqual(self.requests, [])

    def test_fixed_read_routes_and_redirects_prevent_token_forwarding(self):
        source = meet.Source({}, ACCOUNT, self.helpers)
        for path in ('https://example.invalid/', 'spaces/space-1', '../conferenceRecords',
                     RECORD['name'] + '/transcripts/artifact-1/delete'):
            with self.subTest(path=path), self.assertRaisesRegex(a.SourceError, '^google_meet_path_not_allowed$'):
                source.get(path)
        self.assertEqual(self.requests, [])
        request = urllib.request.Request('https://meet.googleapis.com/v2/conferenceRecords')
        self.assertIsNone(meet.NoRedirect().redirect_request(request, None, 302, 'redirect', {}, 'https://example.invalid/'))

    def test_setup_is_complete_and_does_not_ask_for_secrets_as_plain_answers(self):
        self.assertEqual(meet.SETUP['ask'], [])
        self.assertIn('OAuth access token', meet.SETUP['secret'])
        self.assertIn('https://developers.google.com/oauthplayground/', meet.SETUP['note'])
        self.assertIn('https://www.googleapis.com/auth/drive.meet.readonly', meet.SETUP['note'])
        self.assertIn('https://www.googleapis.com/auth/meetings.space.readonly', meet.SETUP['note'])
        self.assertLessEqual(len(meet.SETUP['what']), 70)
        self.assertNotIn('\n', meet.SETUP['what'])


if __name__ == '__main__':
    unittest.main()

"""Granola tests (connectors/granola.py): every HTTP answer and credential read is canned; no live calls. It reads
only (GET to three paths of Granola's public API), treats the key as opaque, asks for a new one on a 401, keeps only
meetings the owner was in, and lands each note on its Calendar meeting through meeting_notes."""
import copy
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from unittest.mock import Mock, patch

from connectors import granola
from test_connectors import Response
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors
import sources

NOW = '2026-11-16T12:00:00+00:00'
ACCOUNT = {**granola.SETUP['account'], 'email': 'owner@example.com'}
ID = 'not_1d3tmYTlCICgjy'
OTHER = 'not_2e4unZUmDJDhkz'


def note(note_id=ID, **extra):
    return {'id': note_id, 'object': 'note', 'title': 'Quarterly review', 'owner': {'name': 'Owner Example', 'email': 'owner@example.com'},
            'created_at': '2026-11-15T09:40:00Z', 'updated_at': '2026-11-15T10:05:00Z', 'deleted_at': None,
            'web_url': 'https://notes.granola.ai/d/fixture',
            'calendar_event': {'event_title': 'Quarterly review', 'calendar_event_id': 'fixture-google-event',
                               'organiser': 'owner@example.com', 'invitees': [{'email': 'dana@client.example'}],
                               'scheduled_start_time': '2026-11-15T09:00:00Z', 'scheduled_end_time': '2026-11-15T09:45:00Z'},
            'attendees': [{'name': 'Owner Example', 'email': 'owner@example.com'}, {'name': 'Dana Client', 'email': 'Dana@Client.example'}],
            'summary_text': 'Dana sends the deck by Friday.',
            'summary_markdown': '## Action items\n\n- Owner sends the pricing by Friday\n- Dana sends the deck',
            'private_notes_markdown': 'Ask about the budget. password: hunter2',
            'transcript': [
                {'speaker': {'source': 'microphone', 'attribution': 'me'}, 'text': "I'll send the pricing by Friday.",
                 'start_time': '2026-11-15T09:01:00Z', 'end_time': '2026-11-15T09:01:05Z'},
                {'speaker': {'source': 'speaker', 'attribution': 'them', 'diarization_label': 'Speaker B'}, 'text': 'Great.',
                 'start_time': '2026-11-15T09:01:06Z', 'end_time': '2026-11-15T09:01:07Z'},
                {'speaker': {'source': 'speaker', 'attribution': 'them', 'diarization_label': 'Speaker B'}, 'text': 'And the deck from us.',
                 'start_time': '2026-11-15T09:01:08Z', 'end_time': '2026-11-15T09:01:10Z'}],
            **extra}


class GranolaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.credential = Mock(return_value='grn_fixture-key')
        self.helpers = types.SimpleNamespace(SourceError=sources.SourceError, Skips=machine_sources_connectors.CONNECTOR_HELPERS.Skips,
                                             now=lambda: NOW, credential=self.credential)
        self.listing = [{'notes': [{'id': ID, 'updated_at': '2026-11-15T10:05:00Z', 'deleted_at': None}], 'hasMore': False, 'cursor': None}]
        self.notes = {ID: note()}
        self.errors = {}
        self.requests = []
        patch.object(granola, 'GAP', 0).start()
        patch('urllib.request.OpenerDirector.open', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        self.assertEqual(timeout, 30)
        self.assertEqual(request.get_method(), 'GET')
        self.assertIsNone(request.data)
        parts = urllib.parse.urlsplit(request.full_url)
        self.assertEqual((parts.scheme, parts.netloc), ('https', 'public-api.granola.ai'))
        self.assertEqual(request.get_header('Authorization'), 'Bearer ' + self.credential.return_value)
        self.assertNotIn(self.credential.return_value, request.full_url)
        query = dict(urllib.parse.parse_qsl(parts.query))
        self.requests.append((parts.path, query))
        error = self.errors.get(parts.path)
        if error:
            raise urllib.error.HTTPError(request.full_url, error, 'error', {}, io.BytesIO(b'{}'))
        if parts.path == '/v1/notes':
            result = self.listing.pop(0) if self.listing else {'notes': [], 'hasMore': False, 'cursor': None}
        else:
            found = self.notes[parts.path.split('/')[3]]
            result = found if query.get('include') == 'transcript' else {k: v for k, v in found.items() if k != 'transcript'}
        return Response(json.dumps(result).encode())

    def sync(self, config=None, account=None):
        return granola.sync(self.store, config or {}, account or ACCOUNT, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return {r['kind']: dict(r) for r in db.execute("SELECT * FROM events WHERE account_id='granola' AND deleted=0")}

    def test_notes_and_transcript_come_in_for_the_meeting_with_its_event_and_people(self):
        result = self.sync()
        self.assertEqual((result['events'], result['read'], result['more']), (2, 1, False))
        rows = self.rows()
        notes, spoken = rows['granola.notes'], rows['granola.transcript']
        self.assertIn('Owner sends the pricing by Friday', notes['body'])
        self.assertIn('## My notes', notes['body'])
        self.assertNotIn('hunter2', notes['body'])  # a labeled password never comes in
        self.assertEqual(spoken['body'], "Owner Example: I'll send the pricing by Friday.\nSpeaker B: Great. And the deck from us.")
        meta = json.loads(notes['metadata'])
        self.assertEqual((meta['calendar_event_id'], meta['start_at'], meta['end_at'], meta['host_email'], meta['from_me']),
                         ('fixture-google-event', '2026-11-15T09:00:00+00:00', '2026-11-15T09:45:00+00:00', 'owner@example.com', True))
        self.assertEqual([p['email'] for p in meta['attendees']], ['owner@example.com', 'dana@client.example'])
        self.assertEqual(meta['source_url'], 'https://notes.granola.ai/d/fixture')
        self.assertEqual(notes['occurred_at'], '2026-11-15T09:00:00+00:00')
        self.assertEqual(self.requests[0], ('/v1/notes', {'updated_after': '2026-11-09T12:00:00Z', 'page_size': '30'}))
        self.assertEqual(self.requests[1], (f'/v1/notes/{ID}', {'include': 'transcript'}))

    def test_an_unchanged_note_is_not_read_again_and_the_next_run_overlaps_two_hours(self):
        self.sync()
        self.listing = [{'notes': [{'id': ID, 'updated_at': '2026-11-15T10:05:00Z'}], 'hasMore': False}]
        self.requests.clear()
        self.assertEqual(self.sync()['read'], 0)
        self.assertEqual(self.requests, [('/v1/notes', {'updated_after': '2026-11-16T10:00:00Z', 'page_size': '30'})])

    def test_a_note_from_a_meeting_the_owner_was_not_in_is_skipped(self):
        self.notes[ID] = note(owner={'name': 'Someone', 'email': 'someone@client.example'},
                              attendees=[{'email': 'someone@client.example'}],
                              calendar_event={'organiser': 'someone@client.example', 'scheduled_start_time': '2026-11-15T09:00:00Z'})
        self.assertEqual(self.sync()['events'], 0)
        self.assertEqual(self.rows(), {})
        self.notes[ID]['attendees'].append({'email': 'owner@example.com'})  # in the meeting after all
        self.listing = [{'notes': [{'id': ID, 'updated_at': '2026-11-15T11:00:00Z'}], 'hasMore': False}]
        self.assertEqual(self.sync()['events'], 2)
        self.assertFalse(json.loads(self.rows()['granola.notes']['metadata'])['from_me'])

    def test_a_note_still_being_written_waits_and_holds_the_window_back(self):
        self.notes[ID] = note(summary_text=None, summary_markdown=None, private_notes_markdown=None, transcript=None,
                              created_at='2026-11-16T11:30:00Z')
        self.assertEqual(self.sync()['events'], 0)
        state = self.store.checkpoint('granola')
        self.assertNotIn('since', state)
        self.assertNotIn(ID, state['seen'])
        self.notes[ID] = note()
        self.listing = [{'notes': [{'id': ID, 'updated_at': '2026-11-16T11:50:00Z'}], 'hasMore': False}]
        self.assertEqual(self.sync()['events'], 2)

    def test_pages_follow_the_cursor_and_a_repeated_cursor_stops(self):
        self.notes[OTHER] = note(OTHER, title='Second meeting')
        self.listing = [{'notes': [{'id': ID, 'updated_at': 'a'}], 'hasMore': True, 'cursor': 'fixture-cursor'},
                        {'notes': [{'id': OTHER, 'updated_at': 'b'}, {'id': '../v2/x', 'updated_at': 'c'}], 'hasMore': False}]
        self.assertEqual(self.sync()['events'], 4)
        self.assertEqual(self.requests[1][1].get('cursor'), 'fixture-cursor')
        self.listing = [{'notes': [], 'hasMore': True, 'cursor': 'same'}, {'notes': [], 'hasMore': True, 'cursor': 'same'}]
        with self.assertRaises(sources.SourceError) as caught:
            self.sync()
        self.assertEqual(caught.exception.category, 'granola_invalid_cursor')

    def test_a_large_transcript_is_read_in_pages(self):
        full = note()
        items = full['transcript']
        self.errors = {}
        calls = []

        def respond(request, timeout):
            parts = urllib.parse.urlsplit(request.full_url)
            query = dict(urllib.parse.parse_qsl(parts.query))
            calls.append((parts.path, query))
            if parts.path == '/v1/notes':
                return Response(json.dumps({'notes': [{'id': ID, 'updated_at': 'x'}], 'hasMore': False}).encode())
            if query.get('include') == 'transcript':
                raise urllib.error.HTTPError(request.full_url, 413, 'too large', {}, io.BytesIO(b'{}'))
            if parts.path.endswith('/transcript'):
                page = {'transcript': items[:2], 'hasMore': True, 'cursor': 'p2'} if 'cursor' not in query else \
                    {'transcript': items[2:], 'hasMore': False}
                return Response(json.dumps(page).encode())
            return Response(json.dumps({k: v for k, v in full.items() if k != 'transcript'}).encode())
        with patch('urllib.request.OpenerDirector.open', side_effect=respond):
            self.assertEqual(self.sync()['events'], 2)
        self.assertEqual([c[0].rsplit('/', 1)[-1] for c in calls], ['notes', ID, ID, 'transcript', 'transcript'])
        self.assertIn('And the deck from us.', self.rows()['granola.transcript']['body'])

    def test_a_deleted_note_goes_from_the_machine_too(self):
        self.sync()
        self.listing = [{'notes': [{'id': ID, 'updated_at': '2026-11-16T11:00:00Z', 'deleted_at': '2026-11-16T11:00:00Z'}], 'hasMore': False}]
        self.sync()
        self.assertEqual(self.rows(), {})

    def test_a_turned_down_key_asks_for_a_new_one_and_other_errors_wait(self):
        self.errors = {'/v1/notes': 401}
        with self.assertRaises(sources.SourceError) as caught:
            self.sync()
        self.assertEqual((caught.exception.category, caught.exception.status), ('granola_key_rejected', 401))
        self.assertIn('granola_key_rejected', granola.SETUP['hints'])
        self.errors = {'/v1/notes': 429}
        with self.assertRaises(sources.SourceError) as caught:
            self.sync()
        self.assertEqual((caught.exception.category, caught.exception.retry_after), ('granola_http', 60))
        self.assertIsNone(self.store.checkpoint('granola'))

    def test_the_key_is_opaque_and_never_sent_elsewhere(self):
        for key in ('grn_fixture-key', 'another-format-0123456789', 'x' * 400):
            self.credential.return_value = key
            self.listing = [{'notes': [], 'hasMore': False}]
            granola.check({}, ACCOUNT, self.helpers)
        for bad in ('', 'short', 'has a space in it', 'x' * 5000):
            self.credential.return_value = bad
            with self.assertRaises(sources.SourceError) as caught:
                granola.check({}, ACCOUNT, self.helpers)
            self.assertEqual(caught.exception.category, 'granola_credential_unavailable')
        self.credential.return_value = 'grn_fixture-key'
        source = granola.Source({}, ACCOUNT, self.helpers)
        for path in ('/v1/workspaces', '/v1/notes/../folders', 'https://example.com/v1/notes'):
            with self.assertRaises(sources.SourceError):
                source.get(path)
        self.assertTrue(any(isinstance(h, granola.NoRedirect) for h in source.opener.handlers))

    def test_the_form_asks_only_for_the_key_and_the_address_comes_from_granola(self):
        import onboarding
        form = onboarding.web_form({'accounts': []}, 'granola')
        self.assertEqual((form['secret'], form['token_url'], form['ask']), ('Granola API key', granola.KEY_URL, []))
        shared = {'id': 'not_SharedNote0001', 'owner': {'name': 'Someone', 'email': 'someone@client.example'}}
        mine = {**self.listing[0]['notes'][0], 'owner': {'name': 'Owner Example', 'email': 'Owner@Example.com'}}
        self.listing = [{'notes': [mine, shared], 'hasMore': False}]
        account = {**ACCOUNT, 'email': ''}
        self.assertIsNone(granola.check({}, account, self.helpers))
        self.assertEqual(account['email'], 'owner@example.com')  # whose notes most of them are: the card's name
        self.assertEqual(granola.whose(['someone@client.example', 'owner@example.com'], {'owner@example.com'}), 'owner@example.com')
        self.assertEqual(granola.whose([], set()), '')
        self.listing = [{'notes': [mine], 'hasMore': False}]
        self.sync(account={**ACCOUNT, 'email': ''})  # a run without it learns it too: the owner's own notes come in
        self.assertIn('granola.notes', self.rows())

    def test_only_granola_links_are_kept(self):
        for n, link in enumerate(('https://evil.example/granola.ai', 'https://evilgranola.ai/d/x', 'http://notes.granola.ai/d/x')):
            self.notes[ID] = note(web_url=link)
            self.listing = [{'notes': [{'id': ID, 'updated_at': str(n)}], 'hasMore': False}]
            self.sync()
            self.assertNotIn('source_url', json.loads(self.rows()['granola.notes']['metadata']))

    def test_people_in_the_meeting_link_to_the_graph(self):
        import graph
        owner = types.SimpleNamespace(mine=lambda a: a == 'owner@example.com', emails={'owner@example.com'})
        self.sync()
        meta = json.loads(self.rows()['granola.notes']['metadata'])
        on_calendar = graph.touches('granola.notes', meta, owner, set())
        self.assertEqual([(t[0], t[1], t[3]) for t in on_calendar], [('email:dana@client.example', 'Dana Client', 'seen')])
        alone = graph.touches('granola.notes', {**meta, 'calendar_event_id': None}, owner, set())  # a call with no invite
        self.assertEqual(alone[0][3], 'met')

    def test_its_kinds_are_meeting_records_for_promises(self):
        import meeting_notes
        import machine.kinds as kinds
        from machine.app import promise_checks
        self.assertEqual(meeting_notes.SOURCES['granola'], {'notes': 'granola.notes', 'transcript': 'granola.transcript'})
        for kind in granola.KINDS:
            self.assertEqual(kinds.KINDS[kind]['family'], kinds.MEETING)
            self.assertIn(kind, promise_checks.ELSEWHERE_KINDS)


if __name__ == '__main__':
    unittest.main()

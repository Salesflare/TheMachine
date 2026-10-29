"""Trello fixture tests. Every HTTP request and credential lookup is replaced."""
import copy
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

from test_connectors import a, Response
from connectors import trello

BOARD = {'id': 'b' * 24, 'shortLink': 'Board001', 'name': 'Example board'}
ACCOUNT = {**trello.SETUP['account'], 'board': 'https://trello.com/b/Board001/example'}
NOW = '2026-10-19T12:00:00+00:00'


def action(number=1, kind='updateCard', **data):
    return {'id': f'{number:024x}', 'type': kind, 'date': '2026-10-18T12:00:00.000Z',
            'memberCreator': {'id': 'd' * 24, 'fullName': 'Example member'},
            'data': {'card': {'id': 'c' * 24, 'shortLink': 'Card0001', 'name': 'Example card'},
                     'old': {'due': None}, 'listAfter': {'name': 'Ready'}, **data}}


class TrelloTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.credential = unittest.mock.Mock(return_value=json.dumps({'key': 'fixture-key', 'token': 'fixture-token'}))
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, iso=a.CONNECTOR_HELPERS.iso,
                                             now=lambda: NOW, credential=self.credential)
        self.pages = [[action()]]
        self.requests = []
        self.http = patch('urllib.request.urlopen', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        self.assertEqual(request.get_method(), 'GET')
        self.assertEqual(timeout, 30)
        parsed = urllib.parse.urlsplit(request.full_url)
        self.assertEqual(parsed.netloc, 'api.trello.com')
        self.assertNotIn('fixture-', request.full_url)
        self.assertEqual(request.get_header('Authorization'),
                         'OAuth oauth_consumer_key="fixture-key", oauth_token="fixture-token"')
        self.requests.append((parsed.path, urllib.parse.parse_qs(parsed.query)))
        if parsed.path == '/1/boards/Board001':
            return Response(json.dumps(BOARD).encode())
        self.assertEqual(parsed.path, '/1/boards/Board001/actions')
        outcome = self.pages.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return Response(json.dumps(outcome).encode())

    def sync(self):
        return trello.sync(self.store, {}, ACCOUNT, self.helpers)

    def rows(self):
        with self.store.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM events ORDER BY source_id')]

    def test_card_updates_comments_deletions_and_board_noise(self):
        other = action(4)
        other['data'] = {'board': BOARD}
        self.pages = [[other, action(3, 'deleteCard'), action(2, 'commentCard', text='<b>Ready</b>'), action()]]
        result = self.sync()
        self.assertEqual(result['events'], 3)
        rows = self.rows()
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['kind'], 'trello.action')
        self.assertEqual(rows[0]['title'], 'Example card')
        self.assertEqual(rows[0]['occurred_at'], '2026-10-18T12:00:00+00:00')
        self.assertIn('listAfter: {"name": "Ready"}', rows[0]['body'])
        self.assertIn('text: Ready', rows[1]['body'])
        meta = json.loads(rows[2]['metadata'])
        self.assertEqual(meta['source_url'], 'https://trello.com/c/Card0001')
        self.assertTrue(meta['card_deleted'])
        self.assertFalse(rows[2]['deleted'])  # The action itself still exists.
        self.assertEqual(meta['sender_display'], 'Example member')
        self.credential.assert_called_once_with({}, 'trello')
        self.assertEqual(self.requests[1][1]['filter'], ['all'])
        self.assertEqual(self.requests[1][1]['since'], ['2026-10-12T12:00:00+00:00'])

    def test_replay_is_idempotent_and_changed_action_versions(self):
        self.sync()
        # Replaying a frozen page is safe after interruption.
        self.store.commit_page(ACCOUNT['id'], {}, [])
        self.pages = [[action()]]
        self.sync()
        self.assertEqual(len(self.rows()), 1)
        self.assertEqual(self.rows()[0]['version'], 1)
        self.store.commit_page(ACCOUNT['id'], {}, [])
        self.pages = [[action(text='Edited comment')]]
        self.sync()
        self.assertEqual(self.rows()[0]['version'], 2)

    def test_empty_incremental_window_advances_with_overlap(self):
        self.sync()
        self.helpers.now = lambda: '2026-10-19T13:00:00+00:00'
        self.pages = [[]]
        self.assertEqual(self.sync()['events'], 0)
        self.assertEqual(self.requests[-1][1]['since'], ['2026-10-19T11:59:59+00:00'])
        self.assertEqual(self.store.checkpoint(ACCOUNT['id'])['since'], self.helpers.now())

    def test_page_limit_resume_and_atomic_failure(self):
        with patch.object(trello, 'LIMIT', 2), patch.object(trello, 'PAGES', 1):
            self.pages = [[action(4), action(3)]]
            self.assertTrue(self.sync()['more'])
            state = self.store.checkpoint(ACCOUNT['id'])
            self.assertEqual(state['catchup']['cursor'], f'{3:024x}')
            self.assertFalse(state['coverage_complete'])
            self.pages = [urllib.error.URLError('private response')]
            with self.assertRaises(a.SourceError):
                self.sync()
            self.assertEqual(self.store.checkpoint(ACCOUNT['id']), state)
            self.pages = [[action(2)]]
            self.assertFalse(self.sync()['more'])
            self.assertEqual(self.requests[-1][1]['before'], [f'{3:024x}'])
            self.assertNotIn('catchup', self.store.checkpoint(ACCOUNT['id']))
            self.assertEqual(len(self.rows()), 3)

    def test_expired_cursor_restarts_the_same_unread_window(self):
        self.store.commit_page(ACCOUNT['id'], {'catchup': {'since': '2026-01-01T00:00:00+00:00',
                               'until': NOW, 'cursor': 'e' * 24}}, [])
        self.pages = [urllib.error.HTTPError('unused', 400, 'private content', {}, None), [action()]]
        self.sync()
        self.assertEqual(self.requests[-1][1]['since'], ['2026-01-01T00:00:00+00:00'])
        self.assertEqual(self.requests[-1][1]['before'], [NOW])
        self.assertTrue(self.store.checkpoint(ACCOUNT['id'])['coverage_complete'])

    def test_nonadvancing_cursor_is_rejected(self):
        self.store.commit_page(ACCOUNT['id'], {'catchup': {'since': '2026-10-12T00:00:00+00:00',
                               'until': NOW, 'cursor': f'{1:024x}'}}, [])
        self.pages = [[action()]]
        with self.assertRaisesRegex(a.SourceError, '^trello_invalid_cursor$'):
            self.sync()
        self.assertEqual(self.rows(), [])

    def test_safe_http_network_json_and_payload_errors(self):
        for status in (401, 403, 404, 429, 500):
            with self.subTest(status=status):
                self.pages = [urllib.error.HTTPError('unused', status, 'private content', {'Retry-After': '120'}, None)]
                with self.assertRaises(a.SourceError) as caught:
                    self.sync()
                self.assertEqual(str(caught.exception), f'trello_http:HTTP_{status}')
                self.assertEqual(caught.exception.retry_after, 120)
                self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        for raw, label in ((b'not json', 'trello_invalid_json'), (b'{}', 'trello_invalid_page'),
                           (json.dumps([{'id': 'bad'}]).encode(), 'trello_invalid_action')):
            with self.subTest(label=label), patch('urllib.request.urlopen', side_effect=[Response(json.dumps(BOARD).encode()), Response(raw)]):
                with self.assertRaisesRegex(a.SourceError, '^' + label + '$'):
                    self.sync()
        self.pages = [urllib.error.URLError('private content')]
        with self.assertRaisesRegex(a.SourceError, '^trello_network$'):
            self.sync()

    def test_invalid_timestamp_does_not_commit(self):
        item = action()
        item['date'] = 'not a date'
        self.pages = [[item]]
        with self.assertRaisesRegex(a.SourceError, '^trello_invalid_timestamp$'):
            self.sync()
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))

    def test_setup_check_is_read_only_and_verifies_board_identity(self):
        self.assertIsNone(trello.check({}, dict(ACCOUNT), self.helpers))
        self.assertEqual(self.rows(), [])
        self.assertIsNone(self.store.checkpoint(ACCOUNT['id']))
        with patch('urllib.request.urlopen', return_value=Response(json.dumps({**BOARD, 'shortLink': 'Wrong001'}).encode())):
            with self.assertRaisesRegex(a.SourceError, '^account_identity_mismatch$'):
                trello.check({}, ACCOUNT, self.helpers)

    def test_check_names_the_connection_after_its_board(self):
        self.pages = [[], []]
        account = dict(ACCOUNT)
        trello.check({}, account, self.helpers)
        self.assertEqual(account['display_name'], 'Example board')  # its card's title, never the account id
        account['display_name'] = 'Renamed'
        trello.check({}, account, self.helpers)
        self.assertEqual(account['display_name'], 'Renamed')  # a name once set is kept
        unnamed = dict(ACCOUNT)
        with patch('urllib.request.urlopen', side_effect=lambda *x, **k: Response(json.dumps({**BOARD, 'name': ''}).encode() if '/actions' not in x[0].full_url else b'[]')):
            trello.check({}, unnamed, self.helpers)
        self.assertEqual(unnamed['display_name'], 'Trello board')

    def test_an_unnamed_connection_reads_trello_board_not_its_id(self):
        card = self.store.snapshot([{**ACCOUNT, 'id': 'work-trello', 'boundary': 'work'}])['connectors'][0]
        self.assertEqual(card['display_name'], 'Trello board')

    def test_board_validation_and_credentials_are_runtime_only(self):
        for value in ('https://example.invalid/b/Board001', '../members/me', '', None):
            with self.subTest(value=value), self.assertRaisesRegex(a.SourceError, '^trello_invalid_board$'):
                trello.Source({}, {**ACCOUNT, 'board': value}, self.helpers)
        self.credential.return_value = 'plain-token'
        with self.assertRaisesRegex(a.SourceError, '^trello_credential_unavailable$'):
            trello.Source({}, ACCOUNT, self.helpers)  # a plain token needs the API key from setup
        source = trello.Source({}, {**ACCOUNT, 'api_key': 'setup-key'}, self.helpers)
        self.assertEqual(source.headers['Authorization'], 'OAuth oauth_consumer_key="setup-key", oauth_token="plain-token"')
        for value in ('{}', '{not json', '[]', '{"key": "bad\\nheader", "token": "x"}'):
            self.credential.return_value = value
            with self.subTest(value=value), self.assertRaisesRegex(a.SourceError, '^trello_credential_unavailable$'):
                trello.Source({}, ACCOUNT, self.helpers)
        self.assertEqual(trello.board_id(BOARD['id'], self.helpers), BOARD['id'])
        self.assertEqual(trello.board_id('Board001', self.helpers), 'Board001')
        self.assertEqual(self.requests, [])

    def test_plain_text_limits_and_omits_labelled_codes(self):
        item = action(text='verification code: 123456\npassword=example\n' + 'x' * 45000)
        item['data']['card']['name'] = '<b>' + 'n' * 1200 + '</b>'
        self.pages = [[item]]
        self.sync()
        row = self.rows()[0]
        self.assertEqual(len(row['title']), 1000)
        self.assertEqual(len(row['body']), 40000)
        self.assertNotIn('123456', row['body'])
        self.assertNotIn('password=example', row['body'])
        self.assertNotIn('<b>', row['title'])


if __name__ == '__main__':
    unittest.main()

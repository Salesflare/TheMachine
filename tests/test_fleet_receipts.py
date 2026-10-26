"""Fleet receipt recovery with an offline relay."""
import json
import unittest
from unittest.mock import patch
import test_fleet

class ReceiptRecovery(unittest.TestCase):
    setUp = test_fleet.Fleet.setUp
    def test_answer_is_saved_once_when_ack_response_is_lost(self):
        sent = self.fleet.ask('relationships', {'about': 'client.example'})
        ask = next(iter(sent['ids'].values()))
        item = {'id': ask, 'status': 'answered', 'answer': {'knows': True, 'closeness': 'close'}, 'receipt': 'r1'}
        self.assertTrue(self.fleet.take_answer(item))
        self.assertTrue(self.fleet.take_answer(item))
        with self.store.connect() as db:
            count = db.execute("SELECT count(*) FROM fleet_log WHERE direction='out' AND outcome LIKE 'answered:%'").fetchone()[0]
        self.assertEqual(count, 1)
        self.assertFalse(self.fleet.take_answer({**item, 'id': 'not-yet-saved'}))

    def test_answer_ack_happens_only_after_local_commit(self):
        sent = self.fleet.ask('relationships', {'about': 'client.example'})
        ask = next(iter(sent['ids'].values()))
        item = {'id': ask, 'status': 'answered', 'answer': {'knows': True, 'closeness': 'close'}, 'receipt': 'r2'}
        self.relay.inbox = {'ack': True, 'asks': [], 'answers': [item]}
        original = self.relay.call
        def call(method, path, body=None, timeout=40):
            if path == '/ack':
                with self.store.connect() as db:
                    row = db.execute('SELECT answer FROM fleet_out WHERE id=?', (ask,)).fetchone()
                    self.assertEqual(json.loads(row['answer'])['knows'], True)
                self.assertEqual(body['answers'], [{'id': ask, 'receipt': 'r2'}])
            return original(method, path, body, timeout)
        with patch.object(self.relay, 'call', call):
            self.fleet.step(wait=0)
        self.assertEqual(len(self.relay.sent('/ack')), 1)

    def test_storage_failure_does_not_ack(self):
        self.relay.inbox = {'ack': True, 'asks': [], 'answers': [{'id': 'a', 'receipt': 'r3'}]}
        with patch.object(self.fleet, 'take_answer', side_effect=RuntimeError('storage failed')):
            with self.assertRaises(RuntimeError):
                self.fleet.step(wait=0)
        self.assertEqual(self.relay.sent('/ack'), [])

    def test_invalid_notice_is_not_acknowledged(self):
        self.relay.inbox = {'ack': True, 'asks': [], 'answers': [], 'notices': [{'id': 'fn_invalid', 'version': 1}]}
        self.fleet.step(wait=0)
        self.assertEqual(self.relay.sent('/ack'), [])

    def test_uncertain_ask_reuses_committed_operation_identity(self):
        original = self.relay.call
        identities = []
        def call(method, path, body=None, timeout=40):
            if path == '/ask':
                identities.append(body['request_id'])
                if len(identities) == 1:
                    raise TimeoutError('response lost after remote commit')
            return original(method, path, body, timeout)
        with patch.object(self.relay, 'call', call):
            with self.assertRaises(TimeoutError):
                self.fleet.ask('relationships', {'about': 'client.example'}, context='task-1')
            self.fleet.ask('relationships', {'about': 'client.example'}, context='task-1')
        self.assertEqual(identities[0], identities[1])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM fleet_meta WHERE key LIKE 'pending_ask:%'").fetchone()[0], 0)

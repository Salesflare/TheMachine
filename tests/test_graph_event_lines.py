"""A person's or project's page lists its signals with graph_event_lines. The owner's own to-do (an owner.card signal)
is one of them like any other, a signal that can't be read is logged and left out, and an unexpected error answers a
plain 500, never a dropped connection (which a proxy in front reads as "The Machine is restarting")."""
import http.client
import importlib.util
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('event_lines_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

ACCOUNTS = [{'id': 'w', 'boundary': 'work:acme.example'}]


class GraphEventLines(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('w', {}, [{'account_id': 'w', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-10-20T09:00:00+00:00',
                                          'title': 'Contract', 'body': 'Could you send it?', 'metadata': {'from': 'Sam Lee <sam@client.example>'},
                                          'deleted': False}])
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS]}
        with self.store.connect() as db:
            self.mail = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]

    def test_the_owners_own_to_do_is_a_line_like_any_signal(self):
        card = self.store.owner_card('Send Sam the signed contract', 'w')
        lines = self.app.graph_event_lines([self.mail, card['event_id']])
        self.assertEqual(len(lines), 2)
        own = next(line for line in lines if line.startswith(f"{card['event_id']} "))
        self.assertIn('(w) to-do the owner added · ', own)
        self.assertTrue(own.endswith('· Send Sam the signed contract'))
        self.assertIn(f'{self.mail} (w) email from Sam Lee · ', next(line for line in lines if line.startswith(f'{self.mail} ')))

    def test_a_signal_that_cant_be_read_is_left_out_not_the_page(self):
        with self.store.connect() as db:
            db.execute("UPDATE events SET occurred_at='not a date' WHERE id=?", (self.mail,))
        card = self.store.owner_card('Call Sam', 'w')
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            lines = self.app.graph_event_lines([self.mail, card['event_id']])
        self.assertEqual([line.split(' ', 1)[0] for line in lines], [str(card['event_id'])])
        self.assertIn(f'event={self.mail}', logged.output[0])

    def test_source_line_still_leaves_the_owners_words_out(self):
        card = self.store.owner_card('Call Sam', 'w')
        rows = self.store.events(['w'], event_ids=[card['event_id']])
        self.assertIsNone(a.source_line(rows))


class UnexpectedError(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 'e.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}

    def serve(self):
        servers, real = [], a.http.server.ThreadingHTTPServer
        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs)); return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture), patch.object(a.signal, 'signal'),
                        patch.object(a.App, 'preparation_worker'), patch.object(a.App, 'delivery_worker')):
            patcher.start(); self.addCleanup(patcher.stop)
        thread = threading.Thread(target=self.app.serve, daemon=True); thread.start()
        while not servers:
            pass
        self.addCleanup(lambda: (self.app.stop.set(), thread.join(5)))
        return servers[0].server_address[1]

    def test_an_unexpected_error_answers_500_with_its_reason(self):
        port = self.serve()
        with patch.object(a.App, 'graph_action', side_effect=TypeError("'NoneType' object is not subscriptable")), self.assertLogs(a.LOG, 'ERROR') as logged:
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', '/api/graph?node=email:sam@client.example', headers={'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'})
            response = conn.getresponse(); body = response.read(); conn.close()
        self.assertEqual(response.status, 500)
        self.assertEqual(json.loads(body), {'error': 'Something went wrong on your Machine. Try again.'})
        self.assertNotIn('restarting', body.decode())
        self.assertTrue(any('request failed path=/api/graph' in line for line in logged.output), logged.output)
        self.assertNotIn('sam@client.example', '\n'.join(logged.output))  # the query (a person's address) stays out of the log


if __name__ == '__main__':
    unittest.main()

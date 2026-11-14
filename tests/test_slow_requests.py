import http.client
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
from seams import patch_everywhere  # noqa: E402
import served  # noqa: E402


class SlowRequests(unittest.TestCase):
    """A request over SLOW_REQUEST_SECONDS is logged with its path, action and database time, never its query or body."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 's.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}

    def serve(self):
        return served.serve(self, a)

    def slow_action(self, *_args, **_kwargs):
        with self.app.store.connect() as db:
            db.execute('SELECT 1').fetchone()
            time.sleep(0.15)
        return {'ok': True}

    def post(self, port, action, args):
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
        conn.request('POST', '/api/action', body=json.dumps({'action': action, 'args': args}),
                     headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test-token'})
        response = conn.getresponse(); response.read(); conn.close()
        return response.status

    def slow_line(self, logged, wanted):
        """The slow-request line is written after the answer went out (its total includes writing it), so the client can
        have its answer first: wait for the server thread's line before the log capture ends."""
        deadline = time.monotonic() + 5
        while not any(wanted in l for l in logged.output) and time.monotonic() < deadline:
            time.sleep(0.01)
        return next((l for l in logged.output if wanted in l), None)

    def test_a_slow_request_logs_its_path_action_and_database_time_only(self):
        port = self.serve()
        with patch_everywhere(a, 'SLOW_REQUEST_SECONDS', 0.1), patch.object(a.App, 'action', side_effect=self.slow_action), \
                self.assertLogs(a.LOG, 'WARNING') as logged:
            self.assertEqual(self.post(port, 'notify_active', {'client': 'secretclient', 'note': 'call sam@client.example'}), 200)
            line = self.slow_line(logged, 'slow request')
        self.assertIsNotNone(line, logged.output)
        self.assertIn('method=POST path=/api/action action=notify_active', line)
        self.assertGreaterEqual(int(line.split('db_connections=')[1]), 1)
        held = float(line.split('db_held=')[1].split('s')[0])
        self.assertGreaterEqual(held, 0.1)
        cpu, total = float(line.split(' cpu=')[1].split('s')[0]), float(line.split('total=')[1].split('s')[0])
        self.assertLess(cpu, total)  # the action slept: its thread's CPU is apart from its total
        self.assertNotIn('sam@client.example', '\n'.join(logged.output))
        self.assertNotIn('secretclient', '\n'.join(logged.output))

    def test_a_query_stays_out_of_the_log(self):
        port = self.serve()
        with patch_everywhere(a, 'SLOW_REQUEST_SECONDS', 0.1), patch.object(a.App, 'graph_find', side_effect=self.slow_action), \
                self.assertLogs(a.LOG, 'WARNING') as logged:
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', '/api/graph?q=sam@client.example', headers={'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'})
            response = conn.getresponse(); response.read(); conn.close()
            line = self.slow_line(logged, 'slow request method=GET path=/api/graph action=-')
        self.assertEqual(response.status, 200)
        self.assertIsNotNone(line, logged.output)
        self.assertNotIn('sam@client.example', '\n'.join(logged.output))

    def test_a_fast_request_logs_nothing(self):
        port = self.serve()
        with patch.object(a.App, 'action', return_value={'ok': True}), patch.object(a.LOG, 'warning') as warning:
            self.assertEqual(self.post(port, 'notify_active', {}), 200)
        self.assertFalse([c for c in warning.call_args_list if 'slow request' in str(c)])

    def test_a_request_reads_the_fleet_directory_once(self):
        """The Fleet tab asked for the Fleet directory some 400 times per answer, a database connection each (db_connections
        420 in the slow-request line, most of 10 s): once per request now, each caller with its own copy, and read again
        after this request saves a new one. Outside a request every read goes to the database, as before."""
        import fleet
        box = object.__new__(fleet.Fleet)
        box.connect = self.app.store.connect
        with self.app.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS fleet_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
        one = {'fleets': [{'id': 'f1', 'kind': 'work'}]}
        box.set_meta('directory', one)
        a._REQUEST_TIMING.value = timing = {'db_wait': 0.0, 'db_held': 0.0, 'db_connections': 0}
        self.addCleanup(setattr, a._REQUEST_TIMING, 'value', None)
        for _ in range(50):
            self.assertEqual(box.fleets(), {'f1': {'id': 'f1', 'kind': 'work'}})
        self.assertEqual(timing['db_connections'], 1)
        box.meta('directory')['fleets'].clear()  # a caller changing its copy changes nobody else's
        self.assertEqual(box.meta('directory'), one)
        two = {'fleets': [{'id': 'f1', 'kind': 'work'}, {'id': 'f2', 'kind': 'family'}]}
        box.set_meta('directory', two)
        self.assertEqual(box.meta('directory'), two)
        a._REQUEST_TIMING.value = None
        with self.app.store.connect() as db:
            db.execute("UPDATE fleet_meta SET value=? WHERE key='directory'", (json.dumps(one),))
        self.assertEqual(box.meta('directory'), one)

    def test_database_time_outside_a_request_is_not_counted(self):
        with self.app.store.connect() as db:
            db.execute('SELECT 1')
        self.assertIsNone(getattr(a._REQUEST_TIMING, 'value', None))


if __name__ == '__main__':
    unittest.main()

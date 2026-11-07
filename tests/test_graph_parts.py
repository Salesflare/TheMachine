"""The Graph comes in parts, so a click paints at once: a record's head (api/graph?node=…&part=head) without its
timeline, and the board view's follow-up state (api/graph/follow-ups) after the board instead of inside it."""
import http.client
import importlib.util
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('graph_parts_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

HEADERS = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'}


class GraphParts(unittest.TestCase):
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

    def get(self, port, path):
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
        conn.request('GET', path, headers=HEADERS)
        response = conn.getresponse(); body = response.read(); conn.close()
        return response.status, json.loads(body)

    def test_a_records_head_comes_without_its_timeline(self):
        port = self.serve()
        record = {'id': 'email:sam@client.example', 'kind': 'person', 'name': 'Sam Lee', 'links': [], 'recent': ['1 (w) email']}
        with patch.object(a.App, 'graph_action', return_value=dict(record)) as action, patch.object(a.App, 'owner_choices', return_value=[]), \
                patch.object(a.App, 'graph_timeline') as timeline, patch.object(a.App, 'about_you_node', return_value=False):
            status, found = self.get(port, '/api/graph?node=email:sam@client.example&part=head')
        self.assertEqual(status, 200)
        self.assertEqual((found['name'], found['recent'], found['head_only'], found['owners']), ('Sam Lee', [], True, []))
        self.assertEqual(action.call_args[0][0]['node_id'], 'email:sam@client.example')
        timeline.assert_not_called()  # the slow part: it comes with the whole page

    def test_the_boards_follow_ups_come_on_their_own(self):
        port = self.serve()
        views = {'boards': {'1': {'on': True, 'next_at': '2026-11-09T07:00:00+00:00'}}, 'projects': {'project:4': {'state': 'scheduled'}}}
        with patch.object(a.App, 'follow_up_board_views', return_value=views) as asked:
            status, found = self.get(port, '/api/graph/follow-ups')
        self.assertEqual((status, found), (200, views))
        asked.assert_called_once()


if __name__ == '__main__':
    unittest.main()

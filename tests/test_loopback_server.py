"""The Machine's own web servers on 127.0.0.1 start without a reverse DNS lookup of their address (http.server's
socket.getfqdn when it binds), which can take seconds on macOS before anything is answered. Loopback only; nothing
leaves this computer."""
import http.client
import http.server
import socket
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import machine.main as machine_main
import machine.web.loopback as machine_web_loopback
from machine.web.waiting import KeyWaitingPage
import served


def no_lookup(*_):
    raise AssertionError('reverse DNS lookup of the server address')


class LoopbackServer(unittest.TestCase):
    def test_it_binds_and_answers_without_a_name_lookup(self):
        class Hello(http.server.BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'hi')
        with patch.object(socket, 'getfqdn', side_effect=no_lookup) as lookup:
            server = machine_web_loopback.Server(('127.0.0.1', 0), Hello)
        self.addCleanup(server.server_close)
        lookup.assert_not_called()
        self.assertEqual((server.server_name, server.server_port), ('localhost', server.server_address[1]))
        threading.Thread(target=server.handle_request, daemon=True).start()
        conn = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=10)
        self.addCleanup(conn.close)
        conn.request('GET', '/')
        self.assertEqual(conn.getresponse().read(), b'hi')

    def test_the_key_waiting_page_starts_without_one(self):
        page = KeyWaitingPage({'port': 0})
        with patch.object(socket, 'getfqdn', side_effect=no_lookup):
            page('The keyring is locked')
        self.addCleanup(page, None)
        self.assertIsInstance(page.server, machine_web_loopback.Server)
        conn = http.client.HTTPConnection('127.0.0.1', page.server.server_address[1], timeout=10)
        self.addCleanup(conn.close)
        conn.request('GET', '/')
        self.assertEqual(conn.getresponse().status, 503)

    def test_the_dashboard_starts_without_one(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.token, self.app.stop = machine_main.Store(Path(tmp.name) / 'events.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443',
                           'port': 0, 'http_timeout': 1}
        lookup = patch.object(socket, 'getfqdn', side_effect=no_lookup)
        port = served.serve(self, patches=[lookup])
        self.assertTrue(port)

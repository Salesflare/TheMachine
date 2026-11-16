"""/api/email reads a source email live from Gmail. When Gmail doesn't answer (a network error, a token or rate-limit
refusal) the dashboard gets a clean refusal it can offer a retry for, never a 500 ("Something went wrong on your
Machine") that lands in the error reports. An email with no full copy to read stays a plain "Email not available"."""
import http.client
import importlib.util
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import served  # noqa: E402

spec = importlib.util.spec_from_file_location('email_view_errors_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class EmailViewErrors(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 'e.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'database': str(Path(self.temp.name) / 'e.sqlite'), 'tailscale_owner': 'owner@example.com',
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        # serve()'s workers are stubbed and every thread it started is joined before the folder goes (tests/served.py)
        self.port = served.serve(self)

    def get(self):
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        conn.request('GET', '/api/email?id=s1&event=7', headers={'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'})
        response = conn.getresponse(); body = response.read(); conn.close()
        return response.status, json.loads(body)

    def test_gmail_not_answering_is_a_refusal_with_a_retry_not_a_500(self):
        for error in (OSError('Network is unreachable'), PermissionError('denied'), TimeoutError('timed out'), a.SourceError('timeout')):
            with self.subTest(error=type(error).__name__), patch.object(a.App, 'email_view', side_effect=error):
                self.assertEqual(self.get(), (404, {'error': 'Email not available', 'retry': True}))

    def test_an_email_without_a_full_copy_is_not_available_without_a_retry(self):
        with patch.object(a.App, 'email_view', side_effect=ValueError('Email not available')):
            self.assertEqual(self.get(), (404, {'error': 'Email not available'}))


if __name__ == '__main__':
    unittest.main()

"""OwnerError (machine/owner_error.py): a message for the owner, told apart from a ValueError that is a bug.

Report only for now: the dashboard still shows any ValueError's text, and one that isn't an OwnerError is logged and
counted for the error reports (machine/web/handler.py unmarked_error)."""
import ast
import http.client
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import i18n_extract  # noqa: E402
from machine.owner_error import OwnerError  # noqa: E402
from machine.web.serving import dashboard_csrf  # noqa: E402
import served  # noqa: E402

spec = importlib.util.spec_from_file_location('owner_error_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class OwnerErrorType(unittest.TestCase):
    def test_a_value_error_and_a_leaf(self):
        self.assertTrue(issubclass(OwnerError, ValueError))  # every `except ValueError` still catches it
        tree = ast.parse((ROOT / 'machine' / 'owner_error.py').read_text(encoding='utf-8'))
        self.assertEqual([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))], [])

    def test_a_translated_message_is_raised_as_an_owner_error(self):
        # t() means the owner reads it: a plain ValueError with a t() message would be counted as a bug
        found = []
        for path in sorted([*ROOT.glob('*.py'), *ROOT.glob('machine/**/*.py'), *ROOT.glob('connectors/*.py')]):
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                if (isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and getattr(node.exc.func, 'id', None) == 'ValueError'
                        and node.exc.args and any(i18n_extract._is_t(n) for n in ast.walk(node.exc.args[0]))):
                    found.append(f'{path.relative_to(ROOT).as_posix()}:{node.lineno}')
        self.assertEqual(found, [], 'a message through t() is for the owner: raise OwnerError (machine/owner_error.py)')


class Extract(unittest.TestCase):
    def test_owner_error_messages_are_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'sample.py').write_text(
                'from machine.owner_error import OwnerError\n'
                'def go(board, kept):\n'
                "    raise OwnerError('That board is gone' if board else 'That project is gone')\n"
                'def made():\n'
                "    kept.append(OwnerError('Pick a mailbox first'))\n", encoding='utf-8')
            got = i18n_extract.server_strings(Path(tmp)).get('sample.py', [])
        self.assertEqual(sorted(got), ['Pick a mailbox first', 'That board is gone', 'That project is gone'])


class ReportOnly(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 'events.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com',
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        self.owner = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com',
                      'Origin': 'https://machine.example:8443', 'X-CSRF-Token': dashboard_csrf('test-token', 'owner@example.com')}

    def post(self, port, body, headers):
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
        conn.request('POST', '/api/action', body if isinstance(body, str) else json.dumps(body), {'Content-Type': 'application/json', **headers})
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return response.status, json.loads(data)['error']

    def test_a_value_error_on_the_dashboard_is_reported_and_still_shown(self):
        def fake_action(name, args, owner_dashboard=False):
            if args.get('owner'):
                raise OwnerError('Pick a mailbox to send it from.')
            raise ValueError('frame too large')
        self.app.action = fake_action
        port = served.serve(self, a)
        with patch.object(self.app.store, 'record_error') as record:
            with self.assertLogs(a.LOG, 'WARNING') as logs:
                self.assertEqual(self.post(port, {'action': 'set_locale', 'args': {}}, self.owner), (400, 'frame too large'))
            self.assertEqual(record.call_args.args[:5], ('service', 'ValueError', 'frame too large', 'tests/test_owner_error.py', 'fake_action'))
            self.assertTrue(any('action error is no OwnerError action=set_locale error=ValueError' in line for line in logs.output), logs.output)
            record.reset_mock()
            # A bug before any action ran: a body that isn't JSON. Its text still shows, and it is counted
            self.assertEqual(self.post(port, '{"action": ', self.owner)[0], 400)
            self.assertEqual(record.call_args.args[:2], ('service', 'JSONDecodeError'))
            record.reset_mock()
            # The owner's message: shown, not counted
            self.assertEqual(self.post(port, {'action': 'set_locale', 'args': {'owner': True}}, self.owner),
                             (400, 'Pick a mailbox to send it from.'))
            # An agent's call (not the dashboard): its error says what to fix, and it isn't counted
            self.assertEqual(self.post(port, {'action': 'set_locale', 'args': {}}, {'Authorization': 'Bearer test-token'}),
                             (400, 'frame too large'))
            record.assert_not_called()


if __name__ == '__main__':
    unittest.main()

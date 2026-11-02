"""The phone app's address on the Network (fleet.app_address): a self-hosted Machine tells the Network its dashboard's
Tailscale https address and nothing else, so the app opens it after its owner signs in. No address without a plain
tailnet name; a change, or none any more, is told again (None deletes it there); a new pairing hears it again."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('app_address_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
fleet = a.fleet
from test_fleet import CONFIG, FakeRelay  # noqa: E402


class AppAddress(unittest.TestCase):
    def test_only_a_plain_tailnet_https_address(self):
        def address(host, path='/', **extra):
            return fleet.app_address({'dashboard_host': host, 'dashboard_path': path, **extra})
        self.assertEqual(address('Desk.Tail1234.ts.net'), 'https://desk.tail1234.ts.net/')
        self.assertEqual(address('desk.tail1234.ts.net:443', '/assistant'), 'https://desk.tail1234.ts.net/assistant/')
        self.assertEqual(address('desk.tail1234.ts.net', '/a//b.c~d_e-f/'), 'https://desk.tail1234.ts.net/a/b.c~d_e-f/')
        for host in ('', 'desk.tail1234.ts.net:8443', 'tail1234.ts.net', 'my.example.com', 'user@desk.tail1234.ts.net',
                     'desk.tail1234.ts.net.evil.example', '-desk.tail1234.ts.net', 'desk_1.tail1234.ts.net', 'desk.tail1234.ts.net/x'):
            self.assertIsNone(address(host), host)
        for path in ('/a b/', '/a?x=1', '/%2e%2e/', '/a#b'):
            self.assertIsNone(address('desk.tail1234.ts.net', path), path)
        self.assertIsNone(address('desk.tail1234.ts.net', manage_url='https://app.themachine.computer/setup'))  # hosted
        self.assertIsNone(fleet.app_address({}))


class ToldTheNetwork(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.relay = FakeRelay()
        self.fleet = fleet.Fleet(self.store.connect, dict(CONFIG, dashboard_host='desk.tail1234.ts.net', dashboard_path='/assistant/'),
                                 lambda: 'token', relay=self.relay)

    def test_it_tells_the_address_and_takes_it_back(self):
        self.fleet.directory(refresh=True)
        self.assertEqual(self.relay.sent('/me')[-1]['app_address'], 'https://desk.tail1234.ts.net/assistant/')
        self.assertEqual(set(self.relay.sent('/me')[-1]), {'emails', 'dashboard', 'remove_work', 'app_address'})  # nothing else
        self.assertTrue(self.fleet.summary()['app_address'])  # Settings says it is shared
        self.fleet.config = dict(self.fleet.config, dashboard_host='desk.tail1234.ts.net:8443')  # its own port: none for the app
        self.fleet.directory(refresh=True)
        self.assertIsNone(self.relay.sent('/me')[-1]['app_address'])
        self.assertFalse(self.fleet.summary()['app_address'])
        self.assertEqual(len(self.relay.sent('/me')), 2)
        self.fleet.directory(refresh=True)
        self.assertEqual(len(self.relay.sent('/me')), 2)  # unchanged: not again

    def test_a_new_pairing_hears_it_again(self):
        self.fleet.directory(refresh=True)
        self.fleet.set_meta('me_sent', None)  # what App.fleet_live does after pairing
        self.fleet.directory(refresh=True)
        self.assertEqual(len(self.relay.sent('/me')), 2)
        self.assertIn("self.fleet.set_meta('me_sent', None)", Path(a.__file__).read_text())


if __name__ == '__main__':
    unittest.main()

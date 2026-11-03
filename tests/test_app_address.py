"""The phone app's address on the Network (fleet.app_address): a self-hosted Machine tells the Network its dashboard's
Tailscale https address and nothing else, so the app opens it after its owner signs in. No address without a plain
tailnet name (the dashboard's own, or a Tailscale alias of one on its own domain); a change, or none any more, is told again (None deletes it there); a new pairing hears it again."""
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
        # 443 and 8443 (a self-hosted Machine's default port) only
        self.assertEqual(address('desk.tail1234.ts.net:8443'), 'https://desk.tail1234.ts.net:8443/')
        self.assertEqual(address('desk.tail1234.ts.net:8443', '/assistant'), 'https://desk.tail1234.ts.net:8443/assistant/')
        for host in ('', 'desk.tail1234.ts.net:8080', 'desk.tail1234.ts.net:444', 'desk.tail1234.ts.net:8443:8443',
                     'desk.tail1234.ts.net:', 'tail1234.ts.net', 'my.example.com', 'user@desk.tail1234.ts.net',
                     'desk.tail1234.ts.net.evil.example', '-desk.tail1234.ts.net', 'desk_1.tail1234.ts.net', 'desk.tail1234.ts.net/x'):
            self.assertIsNone(address(host), host)
        for path in ('/a b/', '/a?x=1', '/%2e%2e/', '/a#b'):
            self.assertIsNone(address('desk.tail1234.ts.net', path), path)
        self.assertIsNone(address('desk.tail1234.ts.net', manage_url='https://app.themachine.computer/setup'))  # hosted
        self.assertIsNone(fleet.app_address({}))

    def test_a_dashboard_on_its_own_domain_tells_its_tailnet_alias(self):
        config = {'dashboard_host': 'my.example.com', 'dashboard_path': '/', 'dashboard_alias_path': '/assistant/',
                  'dashboard_aliases': ['10.0.0.5:8787', 'Desk.Tail1234.ts.net:8443', 'other.tail1234.ts.net']}
        self.assertEqual(fleet.app_address(config), 'https://desk.tail1234.ts.net:8443/assistant/')  # the first tailnet one
        self.assertEqual(fleet.app_address({**config, 'dashboard_host': 'desk.tail1234.ts.net'}), 'https://desk.tail1234.ts.net/')
        self.assertEqual(fleet.app_address({**config, 'dashboard_alias_path': None}), 'https://desk.tail1234.ts.net:8443/assistant/')
        for aliases in ([], ['my.example.org', 'desk.tail1234.ts.net:8080'], 'desk.tail1234.ts.net', None):
            self.assertIsNone(fleet.app_address({**config, 'dashboard_aliases': aliases}), aliases)
        self.assertIsNone(fleet.app_address({**config, 'dashboard_alias_path': '/a b/'}))
        self.assertIsNone(fleet.app_address({**config, 'manage_url': 'https://app.themachine.computer/setup'}))  # hosted

    def test_the_served_one_wins_over_an_alias_where_nothing_listens(self):
        # The same tailnet name twice: bare (for the Host header) and on 8443, where tailscale serve really listens
        config = {'dashboard_host': 'my.example.com', 'dashboard_path': '/', 'dashboard_alias_path': '/assistant/',
                  'dashboard_aliases': ['desk.tail1234.ts.net', 'desk.tail1234.ts.net:8443']}
        self.assertEqual(fleet.app_address(config), 'https://desk.tail1234.ts.net/assistant/')  # not known: the first one
        served = 'https://desk.tail1234.ts.net:8443/assistant/'
        self.assertEqual(fleet.app_address(config, served), served)
        self.assertEqual(fleet.app_address(config, 'https://Desk.Tail1234.ts.net:443/assistant'), 'https://desk.tail1234.ts.net/assistant/')
        # Only an address on one of the config's tailnet names, https on 443 or 8443, plain path: else the config's
        for other in ('https://other.tail1234.ts.net:8443/assistant/', 'http://desk.tail1234.ts.net:8443/assistant/',
                      'https://desk.tail1234.ts.net:8080/assistant/', 'https://desk.tail1234.ts.net:8443/a b/',
                      'https://desk.tail1234.ts.net:8443/assistant/?x=1', 'https://user@desk.tail1234.ts.net:8443/', '', None, 5):
            self.assertEqual(fleet.app_address(config, other), 'https://desk.tail1234.ts.net/assistant/', other)
        self.assertIsNone(fleet.app_address({'dashboard_host': 'my.example.com'}, served))  # no tailnet name in the config
        self.assertIsNone(fleet.app_address({**config, 'manage_url': 'https://app.themachine.computer/setup'}, served))  # hosted

    def test_served_comes_from_tailscale_serve(self):
        import json
        import onboarding
        from unittest import mock
        status = {'Web': {'desk.tail1234.ts.net:8443': {'Handlers': {'/assistant': {'Proxy': 'http://127.0.0.1:8787'}}},
                          'desk.tail1234.ts.net:443': {'Handlers': {'/': {'Proxy': 'http://127.0.0.1:3000'}}}}}
        with mock.patch.object(onboarding.portable, 'tailscale', return_value='tailscale'), \
                mock.patch.object(onboarding, 'run', return_value=mock.Mock(stdout=json.dumps(status))):
            self.assertEqual(a.fleet_served({}), 'https://desk.tail1234.ts.net:8443/assistant/')
        self.assertIn('self.fleet.served = fleet_served', Path(a.__file__).read_text())  # the app sets it


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
        self.fleet.config = dict(self.fleet.config, dashboard_host='desk.tail1234.ts.net:8443')  # the default port: kept
        self.fleet.directory(refresh=True)
        self.assertEqual(self.relay.sent('/me')[-1]['app_address'], 'https://desk.tail1234.ts.net:8443/assistant/')
        self.fleet.config = dict(self.fleet.config, dashboard_host='desk.tail1234.ts.net:8080')  # any other port: none for the app
        self.fleet.directory(refresh=True)
        self.assertIsNone(self.relay.sent('/me')[-1]['app_address'])
        self.assertFalse(self.fleet.summary()['app_address'])
        self.assertEqual(len(self.relay.sent('/me')), 3)
        self.fleet.directory(refresh=True)
        self.assertEqual(len(self.relay.sent('/me')), 3)  # unchanged: not again

    def test_it_tells_the_served_one(self):
        self.fleet.config = dict(self.fleet.config, dashboard_host='my.example.com', dashboard_path='/',
                                 dashboard_aliases=['desk.tail1234.ts.net', 'desk.tail1234.ts.net:8443'])
        self.fleet.served = lambda config: 'https://desk.tail1234.ts.net:8443/assistant/'
        self.fleet.directory(refresh=True)
        self.assertEqual(self.relay.sent('/me')[-1]['app_address'], 'https://desk.tail1234.ts.net:8443/assistant/')

    def test_a_new_pairing_hears_it_again(self):
        self.fleet.directory(refresh=True)
        self.fleet.set_meta('me_sent', None)  # what App.fleet_live does after pairing
        self.fleet.directory(refresh=True)
        self.assertEqual(len(self.relay.sent('/me')), 2)
        self.assertIn("self.fleet.set_meta('me_sent', None)", Path(a.__file__).read_text())


if __name__ == '__main__':
    unittest.main()

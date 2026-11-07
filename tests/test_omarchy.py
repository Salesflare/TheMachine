"""machine/omarchy.py: the current Omarchy theme's colors for the dashboard's Omarchy theme setting, or None without
Omarchy. Only #rrggbb values pass, since they end up in the page's style. GET /api/omarchy-theme: `here` only for a
browser on this computer, and a 304 for the ETag until the theme changes."""
import http.client
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from machine import omarchy
from seams import patch_everywhere

TOKYO = '''mode = "dark"
accent = "#7aa2f7"
background = "#1a1b26"
dark_background = "#16161E"
foreground = "#a9b1d6"
red = "#f7768e"
hyprland_inactive_border = "rgba(58516e66)"
'''


def place(home, folder, colors, name=None):
    theme = Path(home) / folder / 'theme'
    theme.mkdir(parents=True)
    (theme / 'colors.toml').write_text(colors)
    if name is not None:
        (theme.parent / 'theme.name').write_text(name + '\n')


class OmarchyThemeTest(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp()

    def test_no_omarchy(self):
        self.assertIsNone(omarchy.theme(self.home))

    def test_omarchy_4(self):
        place(self.home, '.local/state/omarchy/current', TOKYO, 'tokyo-night')
        got = omarchy.theme(self.home)
        self.assertEqual(got['name'], 'tokyo-night')
        self.assertEqual(got['mode'], 'dark')
        self.assertEqual(got['colors'], {'accent': '#7aa2f7', 'background': '#1a1b26', 'dark_background': '#16161e',
                                         'foreground': '#a9b1d6', 'red': '#f7768e'})

    def test_omarchy_3_and_light(self):
        place(self.home, '.config/omarchy/current', 'mode = "light"\n' + TOKYO.split('\n', 1)[1])
        got = omarchy.theme(self.home)
        self.assertEqual((got['mode'], got['name']), ('light', ''))

    def test_only_plain_colors(self):
        place(self.home, '.local/state/omarchy/current',
              TOKYO.replace('"#f7768e"', '"red;background:url(x)"').replace('mode = "dark"', 'mode = "x"'),
              'evil</style><script>')
        got = omarchy.theme(self.home)
        self.assertNotIn('red', got['colors'])
        self.assertEqual(got['mode'], 'dark')
        self.assertEqual(got['name'], 'evilstylescript')

    def test_incomplete_or_broken_is_none(self):
        place(self.home, '.local/state/omarchy/current', 'accent = "#7aa2f7"\n')
        self.assertIsNone(omarchy.theme(self.home))
        (Path(self.home) / '.local/state/omarchy/current/theme/colors.toml').write_text('not = [toml')
        self.assertIsNone(omarchy.theme(self.home))

    def test_tag_changes_with_the_theme(self):
        self.assertIsNone(omarchy.tag(self.home))
        place(self.home, '.local/state/omarchy/current', TOKYO, 'tokyo-night')
        one = omarchy.tag(self.home)
        self.assertEqual(one, omarchy.tag(self.home))
        self.assertNotEqual(one, omarchy.tag(self.home, here=True))
        colors = Path(self.home) / '.local/state/omarchy/current/theme/colors.toml'
        colors.write_text(TOKYO.replace('#1a1b26', '#1a1b27') + '\n')
        self.assertNotEqual(one, omarchy.tag(self.home))

    def test_same_host(self):
        self.assertTrue(omarchy.same_host(''))           # no proxy: a browser on this computer
        self.assertTrue(omarchy.same_host('127.0.0.1'))
        self.assertFalse(omarchy.same_host(None))        # a proxy that didn't say who
        self.assertFalse(omarchy.same_host('192.0.2.7'))  # TEST-NET: never this computer's
        self.assertFalse(omarchy.same_host('127.0.0.1; rm'))


spec = importlib.util.spec_from_file_location('omarchy_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class OmarchyRouteTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        place(self.temp.name, '.local/state/omarchy/current', TOKYO, 'tokyo-night')
        home = patch.object(Path, 'home', return_value=Path(self.temp.name))
        home.start()
        self.addCleanup(home.stop)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 'events.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com',
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}

    def serve(self):
        servers = []
        real = a.http.server.ThreadingHTTPServer
        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs)); return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture),
                        patch.object(a.signal, 'signal'), patch.object(a.App, 'preparation_worker'),
                        patch.object(a.App, 'delivery_worker'),
                        patch_everywhere(a, 'tailnet_login', side_effect=lambda ip: 'owner@example.com')):
            patcher.start()
            self.addCleanup(patcher.stop)
        thread = threading.Thread(target=self.app.serve, daemon=True)
        thread.start()
        while not servers:
            time.sleep(0.01)
        self.addCleanup(lambda: (self.app.stop.set(), thread.join(5)))
        return servers[0].server_address[1]

    def test_here_and_etag(self):
        port = self.serve()
        def get(headers):
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', '/api/omarchy-theme', headers={'Host': 'machine.example:8443', **headers})
            r = conn.getresponse(); body = r.read(); conn.close()
            return r.status, r.getheader('ETag'), json.loads(body) if body else None
        status, tag, body = get({'X-Tailnet-Client': '127.0.0.1'})
        self.assertEqual((status, body['name'], body['here']), (200, 'tokyo-night', True))
        self.assertEqual(get({'X-Tailnet-Client': '127.0.0.1', 'If-None-Match': tag})[:2], (304, tag))
        status, other, body = get({'X-Tailnet-Client': '192.0.2.7'})  # the owner's phone or laptop on the tailnet
        self.assertEqual((status, body['here']), (200, False))
        self.assertEqual(get({'X-Tailnet-Client': '192.0.2.7', 'If-None-Match': tag})[0], 200)  # another device's tag
        self.assertEqual(get({'Tailscale-User-Login': 'owner@example.com'})[2]['here'], False)  # Serve, no address
        (Path(self.temp.name) / '.local/state/omarchy/current/theme.name').write_text('gruvbox-long-name\n')
        self.assertEqual(get({'X-Tailnet-Client': '127.0.0.1', 'If-None-Match': tag})[0], 200)  # switched: new colors
        self.assertEqual(get({'X-Tailnet-Client': '127.0.0.1'})[2]['name'], 'gruvbox-long-name')


if __name__ == '__main__':
    unittest.main()

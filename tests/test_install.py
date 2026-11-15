import json, struct, unittest
import assistant as a
import dashboard_parts
import machine.config as machine_config
import machine.faults as machine_faults
import machine.web.serving as machine_web_serving
import time


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    return struct.unpack('>II', head[16:24])


class HomeScreenApp(unittest.TestCase):
    """Android installs the dashboard as a full-screen app from its manifest."""

    def test_manifest_is_installable_and_every_icon_is_served(self):
        manifest = json.loads((machine_config.ROOT / 'manifest.webmanifest').read_text())
        self.assertEqual(manifest['display'], 'fullscreen')
        self.assertEqual((manifest['start_url'], manifest['scope']), ('.', '.'))  # relative: works under /assistant/
        purposes = set()
        for icon in manifest['icons']:
            path = machine_config.BRAND_ASSETS['/' + icon['src']]
            self.assertEqual('%dx%d' % png_size(path), icon['sizes'], icon['src'])
            purposes.add((icon['sizes'], icon['purpose']))
        self.assertTrue({('192x192', 'any'), ('512x512', 'any'), ('512x512', 'maskable')} <= purposes)

    def test_the_installed_app_is_a_share_target_for_new_to_do(self):
        # Share to The Machine from an installed dashboard (Android): sw.js takes the post and opens New to-do. Before it
        # does (or without it) the Machine only sends the browser to the dashboard, signed in or not, and reads nothing.
        import http.client, chat_files, test_owner_boundary
        target = json.loads((machine_config.ROOT / 'manifest.webmanifest').read_text())['share_target']
        self.assertEqual((target['action'], target['method'], target['enctype']), ('share-target', 'POST', 'multipart/form-data'))
        accept = set(target['params']['files'][0]['accept'])
        self.assertTrue({'application/pdf', '.pdf', 'image/jpeg', 'text/plain'} <= accept)
        self.assertEqual({x for x in accept if x.startswith('.')} - set(chat_files.TYPES), set(), 'only kinds New to-do takes')
        sw = (machine_config.ROOT / 'sw.js').read_text()
        self.assertIn("url.pathname === scope.pathname + 'share-target'", sw)
        fixture = test_owner_boundary.OwnerBoundary()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        port = fixture.serve()
        for headers in ({'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'}, {'Host': 'machine.example:8443'}):
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            body = b'--x\r\nContent-Disposition: form-data; name="text"\r\n\r\nMade-up note\r\n--x--\r\n'
            conn.request('POST', '/share-target', body=body, headers={**headers, 'Content-Type': 'multipart/form-data; boundary=x'})
            response = conn.getresponse()
            response.read()
            conn.close()
            self.assertEqual((response.status, response.getheader('Location')), (303, './'))

    def test_each_mood_is_its_own_sticker_not_the_app_icon(self):
        # The robot's moods (empty states, errors, the inbox-zero game) are served over HTTP as real stickers: small
        # transparent WebPs, a different picture for each, none of them the app icon.
        import http.client, test_owner_boundary
        fixture = test_owner_boundary.OwnerBoundary()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        port = fixture.serve()
        owner = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'}
        icon = (machine_config.ROOT / 'brand/app-icon-192.png').read_bytes()
        seen = {}
        for mood in ('sleepy', 'sad', 'thinking', 'wave', 'laugh', 'party'):
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', f'/brand/{mood}.webp', headers=owner)
            response = conn.getresponse()
            body = response.read()
            conn.close()
            self.assertEqual((response.status, response.getheader('Content-Type')), (200, 'image/webp'), mood)
            self.assertEqual((body[:4], body[8:16]), (b'RIFF', b'WEBPVP8X'), mood)
            self.assertTrue(body[20] & 0x10, mood + ' keeps its transparency')
            size = (int.from_bytes(body[24:27], 'little') + 1, int.from_bytes(body[27:30], 'little') + 1)
            self.assertEqual(size, (256, 256), mood)
            self.assertLess(len(body), 30_000, mood)
            self.assertNotEqual(body, icon, mood)
            self.assertNotIn(body, seen, f'{mood} is the same picture as {seen.get(body)}')
            seen[body] = mood

    def test_own_origin_for_the_app_and_old_links_keep_working(self):
        config = {'dashboard_host': 'm.ts.net:8443', 'dashboard_aliases': ['m.ts.net']}
        self.assertEqual(machine_web_serving.dashboard_hosts(config), ['m.ts.net:8443', 'm.ts.net'])
        self.assertEqual(machine_web_serving.dashboard_hosts({'dashboard_host': 'm.ts.net'}), ['m.ts.net'])

    def test_dashboard_links_the_manifest(self):
        self.assertIn('<link rel="manifest" href="manifest.webmanifest" crossorigin="use-credentials">', dashboard_parts.assemble(machine_config.ROOT))

    def test_something_wrong_goes_to_github_issues_or_the_hosted_support_form(self):
        page = dashboard_parts.assemble(machine_config.ROOT)
        self.assertIn('id="report-problem" class="footer-link" href="https://github.com/Salesflare/TheMachine/issues/new"', page)
        self.assertIn("$('#report-problem').href=new URL('/support',state.manage_url).href", page)

    def test_footer_offers_the_source_of_the_running_version(self):
        # AGPL-3.0 section 13: people using the dashboard can get its source.
        page = dashboard_parts.assemble(machine_config.ROOT)
        self.assertIn('id="source-code" class="footer-link" href="https://github.com/Salesflare/TheMachine"', page)
        self.assertIn("$('#source-code').href=state.source_url", page)

    def test_source_url_names_a_release_github_has_never_a_local_commit(self):
        import subprocess, tempfile
        with tempfile.TemporaryDirectory() as root:
            git = lambda *args: subprocess.run(['git', '-C', root, *args], check=True, capture_output=True)
            commit = lambda m: git('-c', 'user.name=t', '-c', 'user.email=t@example.com', 'commit', '-q', '--allow-empty', '-m', m)
            git('init', '-q')
            commit('x')
            machine_faults._SOURCE_URL.clear()
            self.assertEqual(machine_faults.source_url(root), machine_faults.SOURCE_REPO, 'a commit of its own: the repo, not a 404')
            git('tag', 'release-20261101-0900')
            machine_faults._SOURCE_URL.clear()
            self.assertEqual(machine_faults.source_url(root), machine_faults.SOURCE_REPO + '/tree/release-20261101-0900')
            commit('a local change on top')
            git('tag', 'my-own-tag')
            machine_faults._SOURCE_URL.clear()
            self.assertEqual(machine_faults.source_url(root), machine_faults.SOURCE_REPO + '/tree/release-20261101-0900', 'the latest release it contains')
        with tempfile.TemporaryDirectory() as root:  # an install that ports releases as its own commits
            git = lambda *args: subprocess.run(['git', '-C', root, *args], check=True, capture_output=True)
            commit = lambda m: git('-c', 'user.name=t', '-c', 'user.email=t@example.com', 'commit', '-q', '--allow-empty', '-m', m)
            git('init', '-q')
            commit('Promise pages (OSS #83, release-20261023-1930)')
            commit('A local fix')
            machine_faults._SOURCE_URL.clear()
            self.assertEqual(machine_faults.source_url(root), machine_faults.SOURCE_REPO + '/tree/release-20261023-1930', 'the release its last port names')
        machine_faults._SOURCE_URL.clear()
        self.assertEqual(machine_faults.source_url('/nonexistent-dir'), machine_faults.SOURCE_REPO)
        machine_faults._SOURCE_URL.clear()

    def test_source_url_right_after_boot(self):
        # time.monotonic() counts from boot: under 10 minutes of uptime an empty cache must not look fresh.
        from unittest import mock
        machine_faults._SOURCE_URL.clear()
        with mock.patch.object(time, 'monotonic', return_value=5.0):
            self.assertEqual(machine_faults.source_url('/nonexistent-dir'), machine_faults.SOURCE_REPO)
        machine_faults._SOURCE_URL.clear()


if __name__ == '__main__':
    unittest.main()

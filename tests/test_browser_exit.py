"""The Machine's browser going out through the owner's computer (machine/browser_exit.py): tm-exit/1's frames, which
sites go that way, the owner-only upgrade at /api/exit, straight out while the computer is away (the sign-in dialog
asking for it), challenges counted after a site's way out changed, and a page Chromium opens
through the Machine's listener, the real upgrade and a stand-in for the desktop app, where the site sees the stand-in's
address. Offline: only 127.0.0.1 and 127.0.0.2."""
import http.client
import http.server
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from machine import browser_exit as x
import error_feed
import machine.app.browser as machine_app_browser
import machine.main as machine_main
import served

CHROME = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome-stable') or shutil.which('chromium-browser')
HOST = 'machine.example:8443'
OWNER = {'Host': HOST, 'Tailscale-User-Login': 'owner@example.com'}
UPGRADE = {**OWNER, 'Origin': 'https://' + HOST, 'Connection': 'Upgrade', 'Upgrade': x.PROTOCOL}


class Frames(unittest.TestCase):
    def test_the_golden_open_frame(self):
        # the same bytes the desktop app's exit.rs tests decode
        payload = json.dumps({'host': 'a.example', 'port': 443}, separators=(',', ':')).encode()
        self.assertEqual(x.frame(x.OPEN, 1, payload).hex(),
                         '02000000010000001f7b22686f7374223a22612e6578616d706c65222c22706f7274223a3434337d')

    def test_frames_read_back_and_a_long_one_is_refused(self):
        data = x.frame(x.DATA, 7, b'abc') + x.frame(x.END, 7)
        reader = iter([data[i:i + 5] for i in range(0, len(data), 5)])
        buffer = bytearray()

        def read(n):
            while len(buffer) < n:
                part = next(reader, b'')
                if not part:
                    break
                buffer.extend(part)
            out = bytes(buffer[:n])
            del buffer[:n]
            return out
        self.assertEqual(x.read_frame(read), (x.DATA, 7, b'abc'))
        self.assertEqual(x.read_frame(read), (x.END, 7, b''))
        self.assertIsNone(x.read_frame(read))
        with self.assertRaises(ValueError):
            x.frame(x.DATA, 1, bytes(x.MAX_FRAME + 1))
        too_long = struct.pack('>BII', x.DATA, 1, x.MAX_FRAME + 1)
        with self.assertRaises(ValueError):
            x.read_frame(lambda n, d=[too_long]: d.pop() if d else b'')


class Sites(unittest.TestCase):
    def test_a_site_and_its_subdomains_and_nothing_that_looks_like_it(self):
        suffixes = x.sites({})
        for host in ('linkedin.com', 'www.linkedin.com', 'WWW.LinkedIn.com.', 'm.facebook.com', 'x.com', 'api.twitter.com'):
            self.assertTrue(x.listed(host, suffixes), host)
        for host in ('linkedin.com.example.org', 'notlinkedin.com', 'example.com', 'box.com', '', None, '203.0.113.5'):
            self.assertIsNone(x.listed(host, suffixes), host)
        self.assertEqual(x.site_name(x.listed('www.linkedin.com', suffixes)), 'LinkedIn')
        self.assertEqual(x.site_name(x.listed('mobile.twitter.com', suffixes)), 'X')

    def test_the_owners_own_list(self):
        suffixes = x.sites({'browser_exit_sites': ['Example.org.', ' ', 3]})
        self.assertEqual(suffixes, ['example.org'])
        self.assertEqual(x.site_name(x.listed('shop.example.org', suffixes)), 'example.org')
        self.assertIsNone(x.listed('www.linkedin.com', suffixes))
        self.assertEqual(x.sites({'browser_exit_sites': []}), [])  # none: everything straight out

    def test_seen_as_is_a_public_address_only(self):
        self.assertEqual(x.public(' 203.0.114.9 '), '203.0.114.9')
        for address in ('10.0.0.1', '127.0.0.1', '100.101.102.103', '169.254.169.254', 'fd00::1', '', 'garbage', None):
            self.assertIsNone(x.public(address), address)


class Remembered(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        x.configure(temp.name)
        self.addCleanup(x.configure, None)

    def test_an_app_is_expected_only_while_one_has_it_on(self):
        self.assertFalse(x.expected())  # never connected
        x._remember(at=time.time(), off=False)
        self.assertTrue(x.expected())
        x._remember(off=True)
        self.assertFalse(x.expected())  # turned off in the app
        x._remember(at=time.time() - x.FORGET - 1, off=False)
        self.assertFalse(x.expected())  # gone too long

    def test_the_sign_in_asks_for_the_computer_only_while_an_app_with_it_on_is_away(self):
        config = {'browser_exit': True}
        hosts = ['example.org', 'www.linkedin.com']
        self.assertIsNone(x.away(config, hosts))  # no desktop app ever: signs in as today
        x._remember(at=time.time(), off=False)
        self.assertEqual(x.away(config, hosts), 'LinkedIn')
        self.assertIsNone(x.away(config, ['example.org']))  # not a listed site
        self.assertIsNone(x.away({'browser_exit': False}, hosts))
        x._remember(off=True)
        self.assertIsNone(x.away(config, hosts))  # turned off in the app
        x._remember(off=False)
        with patch.object(x, 'connected', lambda: True):
            self.assertIsNone(x.away(config, hosts))  # it's there: the sign-in goes through it


class Challenges(unittest.TestCase):
    def setUp(self):
        x.reset()
        self.addCleanup(x.reset)

    def test_counted_once_soon_after_a_sites_way_out_changed(self):
        config, now = {'browser_exit': True}, 1_000_000.0
        x.went('linkedin.com', 'computer', now)
        self.assertIsNone(x.challenge(config, 'www.linkedin.com', 'signin', now + 5))  # always that way: nothing to tell
        x.went('linkedin.com', 'direct', now + 10)
        self.assertEqual(x.challenge(config, 'www.linkedin.com', 'captcha', now + 20), ('linkedin.com', 'computer', 'direct'))
        self.assertIsNone(x.challenge(config, 'www.linkedin.com', 'captcha', now + 30))  # once per change
        self.assertEqual(x.challenge(config, 'www.linkedin.com', 'checkpoint', now + 30), ('linkedin.com', 'computer', 'direct'))
        self.assertIsNone(x.challenge(config, 'www.linkedin.com', 'wall', now + 10 + x.SWITCHED + 1))  # long after
        self.assertIsNone(x.challenge(config, 'www.linkedin.com', 'something else', now + 20))
        self.assertIsNone(x.challenge(config, 'example.org', 'signin', now + 20))  # not listed
        self.assertIsNone(x.challenge({'browser_exit': False}, 'www.linkedin.com', 'wall', now + 20))
        own = {'browser_exit': True, 'browser_exit_sites': ['intranet.example']}
        x.went('intranet.example', 'computer', now)
        x.went('intranet.example', 'direct', now + 1)
        self.assertEqual(x.challenge(own, 'intranet.example', 'signin', now + 2), ('other', 'computer', 'direct'))  # never its name


def socks(port, host, target_port):
    """A SOCKS5 CONNECT as Chrome sends it (a name); the reply code and the socket."""
    conn = socket.create_connection(('127.0.0.1', port), timeout=30)
    conn.sendall(b'\x05\x01\x00')
    assert conn.recv(2) == b'\x05\x00'
    name = host.encode()
    conn.sendall(b'\x05\x01\x00\x03' + bytes([len(name)]) + name + struct.pack('>H', target_port))
    reply = b''
    while len(reply) < 10:
        part = conn.recv(10 - len(reply))
        if not part:
            break
        reply += part
    return (reply[1] if len(reply) > 1 else None), conn


class Peer:
    """A stand-in for the desktop app's side (its exit.rs): the upgrade with the owner's headers, HELLO, and the
    streams it is asked for, connected from `source` (the app checks addresses itself; this stand-in allows these)."""

    def __init__(self, port, resolve, source='127.0.0.2', headers=UPGRADE):
        self.resolve, self.source, self.outs, self.lock = resolve, source, {}, threading.Lock()
        self.sock = socket.create_connection(('127.0.0.1', port), timeout=30)
        self.sock.sendall(('GET /api/exit HTTP/1.1\r\n' + ''.join(f'{k}: {v}\r\n' for k, v in headers.items()) + '\r\n').encode())
        head = b''
        while b'\r\n\r\n' not in head:
            part = self.sock.recv(1)
            if not part:
                break
            head += part
        self.status = int(head.split(b' ', 2)[1]) if head else 0
        self.reader = self.sock.makefile('rb')

    def send(self, kind, sid=0, payload=b''):
        with self.lock:
            self.sock.sendall(x.frame(kind, sid, payload))

    def start(self):
        self.send(x.HELLO, 0, b'{"v":1,"app":"test","os":"linux"}')
        kind, _, payload = x.read_frame(self.reader.read)
        assert kind == x.HELLO, kind
        self.hello = json.loads(payload)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return self

    def run(self):
        try:
            while (got := x.read_frame(self.reader.read)) is not None:
                kind, sid, payload = got
                if kind == x.OPEN:
                    want = json.loads(payload)
                    try:
                        out = socket.create_connection((self.resolve(want['host']), want['port']), 5, source_address=(self.source, 0))
                    except OSError:
                        self.send(x.REFUSED, sid, b'unreachable')
                        continue
                    self.outs[sid] = out
                    self.send(x.OPENED, sid)
                    threading.Thread(target=self.pump, args=(sid, out), daemon=True).start()
                elif kind == x.DATA and sid in self.outs:
                    self.outs[sid].sendall(payload)
                elif kind == x.END and sid in self.outs:
                    self.outs.pop(sid).close()
                elif kind == x.PING:
                    self.send(x.PONG, 0, payload)
        except (OSError, ValueError):
            pass

    def pump(self, sid, out):
        try:
            while data := out.recv(x.MAX_FRAME):
                self.send(x.DATA, sid, data)
            self.send(x.END, sid)
        except OSError:
            pass

    def close(self, bye=None):
        if bye:
            try:
                self.send(x.BYE, 0, bye)
            except OSError:
                pass
        for s in [*self.outs.values(), self.sock]:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            s.close()
        if getattr(self, 'thread', None):
            self.thread.join(5)


class Seen(http.server.BaseHTTPRequestHandler):
    """The site: a page that loads a picture (asked for only once the page came back), and the address each request
    came from."""
    peers = []
    paths = []

    def do_GET(self):
        Seen.peers.append(self.client_address[0])
        Seen.paths.append(self.path)
        body = b'<!doctype html><title>Site</title><p>The site page</p><img src="/read.png">'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class KeptSeen(Seen):
    protocol_version = 'HTTP/1.1'  # keeps the connection, as a browser's is


class Served(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        x.reset()
        self.addCleanup(x.reset)
        x.configure(self.temp.name)
        self.addCleanup(x.configure, None)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store, self.app.token, self.app.stop = self.store, 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': HOST, 'port': 0,
                           'http_timeout': 1, 'database': str(Path(self.temp.name) / 'events.sqlite')}
        self.port = served.serve(self)  # browser_exit off at the start: no listener of its own
        self.app.config.update(browser_exit=True, browser_exit_port=0, browser_exit_sites=['exit.test'])

    def get(self, headers):
        conn = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        conn.request('GET', '/api/exit', headers=headers)
        return conn.getresponse().status

    def listener(self):
        server = self.server = x.start(self.app.config, self.temp.name)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server.server_address[1]

    def test_only_the_owner_from_its_own_origin_with_the_upgrade(self):
        self.assertEqual(self.get({**UPGRADE, 'Tailscale-User-Login': 'other@example.com'}), 403)
        self.assertEqual(self.get({**UPGRADE, 'Origin': 'https://evil.example'}), 403)
        self.assertEqual(self.get({k: v for k, v in UPGRADE.items() if k != 'Origin'}), 403)
        self.assertEqual(self.get({**UPGRADE, 'Upgrade': 'websocket'}), 426)
        self.assertEqual(self.get({**UPGRADE, 'Connection': 'keep-alive'}), 426)
        self.assertEqual(self.get({'Authorization': 'Bearer test-token', 'Origin': 'https://' + HOST, 'Connection': 'Upgrade', 'Upgrade': x.PROTOCOL}), 403)
        self.app.config['browser_exit'] = False
        self.assertEqual(self.get(UPGRADE), 404)  # off: an app tries again later
        self.assertFalse(x.connected())

    def test_a_listed_site_goes_through_the_computer_and_others_straight_out(self):
        site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Seen)
        threading.Thread(target=site.serve_forever, daemon=True).start()
        self.addCleanup(site.server_close)
        self.addCleanup(site.shutdown)
        port = self.listener()
        peer = Peer(self.port, lambda host: '127.0.0.1')
        self.assertEqual(peer.status, 101)
        peer.start()
        self.addCleanup(peer.close)
        self.assertEqual(peer.hello, {'v': 1, 'seen_as': None})
        self.assertTrue(x.connected())
        Seen.peers.clear()
        code, conn = socks(port, 'page.exit.test', site.server_address[1])
        self.assertEqual(code, 0)
        conn.sendall(b'GET / HTTP/1.1\r\nHost: page.exit.test\r\nConnection: close\r\n\r\n')
        answer = b''
        while part := conn.recv(65536):
            answer += part
        conn.close()
        self.assertIn(b'The site page', answer)
        self.assertEqual(Seen.peers, ['127.0.0.2'])
        # a site that isn't listed goes out from the Machine itself
        code, conn = socks(port, '127.0.0.1', site.server_address[1])
        self.assertEqual(code, 0)
        conn.sendall(b'GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n')
        while conn.recv(65536):
            pass
        conn.close()
        self.assertEqual(Seen.peers, ['127.0.0.2', '127.0.0.1'])
        # the app refuses one: the browser is told no, and it doesn't go straight out instead
        code, conn = socks(port, 'no.exit.test', 1)
        conn.close()
        self.assertEqual(code, 2)
        self.assertEqual(Seen.peers, ['127.0.0.2', '127.0.0.1'])

    def test_while_the_computer_is_away_a_listed_site_goes_straight_out_at_once(self):
        site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), KeptSeen)
        threading.Thread(target=site.serve_forever, daemon=True).start()
        self.addCleanup(site.server_close)
        self.addCleanup(site.shutdown)
        port = self.listener()
        x._remember(at=time.time(), off=False)  # an app with it on was there, and is away now
        real = socket.create_connection
        resolve = lambda address, *a, **k: real(('127.0.0.1' if address[0].endswith('exit.test') else address[0], address[1]), *a, **k)

        def fetch(conn):
            conn.sendall(b'GET / HTTP/1.1\r\nHost: www.exit.test\r\n\r\n')
            got = b''
            while b'The site page' not in got and (part := conn.recv(65536)):
                got += part
            return got
        Seen.peers.clear()
        with patch.object(x.socket, 'create_connection', resolve):
            begun = time.monotonic()
            code, kept = socks(port, 'www.exit.test', site.server_address[1])
            self.assertEqual(code, 0)
            self.assertLess(time.monotonic() - begun, 5)  # no wait for the computer
            self.assertIn(b'The site page', fetch(kept))  # a kept-alive connection, straight out
            self.assertEqual(Seen.peers, ['127.0.0.1'])
            # the computer connects: the direct one is closed, and the browser's next one goes through it
            self.peer = Peer(self.port, lambda host: '127.0.0.1').start()
            self.addCleanup(self.peer.close)
            self.assertEqual(kept.recv(1), b'')
            kept.close()
            code, conn = socks(port, 'www.exit.test', site.server_address[1])
            self.assertEqual(code, 0)
            self.assertIn(b'The site page', fetch(conn))
            conn.close()
            self.assertEqual(Seen.peers, ['127.0.0.1', '127.0.0.2'])
            # a challenge right after that switch is one to count, once; with the computer there all along, none
            self.assertEqual(x.challenge(self.app.config, 'www.exit.test', 'signin'), ('other', 'direct', 'computer'))
            self.assertIsNone(x.challenge(self.app.config, 'www.exit.test', 'signin'))
            # turned off in the app: straight out again
            self.peer.close(b'off')
            for _ in range(50):
                if not x.connected():
                    break
                time.sleep(0.1)
            self.assertFalse(x.expected())
            code, conn = socks(port, 'www.exit.test', site.server_address[1])
            self.assertEqual(code, 0)
            fetch(conn)
            conn.close()
            self.assertEqual(Seen.peers[-1], '127.0.0.1')
            self.assertEqual(x.challenge(self.app.config, 'login.www.exit.test', 'wall'), ('other', 'computer', 'direct'))

    @unittest.skipUnless(CHROME and sys.platform.startswith('linux'), 'needs Chromium, and 127.0.0.2 (Linux)')
    def test_chromium_through_the_machine_and_the_computer_sees_the_computers_address(self):
        site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Seen)
        threading.Thread(target=site.serve_forever, daemon=True).start()
        self.addCleanup(site.server_close)
        self.addCleanup(site.shutdown)
        port = self.listener()
        peer = Peer(self.port, lambda host: '127.0.0.1').start()
        self.addCleanup(peer.close)
        Seen.peers.clear()

        def load(url):
            # the Machine's browser as a hosted Machine starts it, its way out a SOCKS5 proxy (here the listener itself);
            # the page came back through it once the browser asks for its picture
            Seen.peers.clear()
            Seen.paths.clear()
            profile = tempfile.mkdtemp()  # its own each time: nothing the last page taught it opens connections early
            self.addCleanup(shutil.rmtree, profile, True)
            chrome = subprocess.Popen([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--use-mock-keychain', '--no-first-run',
                                       '--user-data-dir=' + profile, f'--proxy-server=socks5://127.0.0.1:{port}', '--proxy-bypass-list=<-loopback>',
                                       '--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable', url],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            try:
                for _ in range(1200):
                    if '/read.png' in Seen.paths or chrome.poll() is not None:
                        break
                    time.sleep(0.1)
            finally:  # its helper processes too, with their connections to the listener
                try:
                    os.killpg(chrome.pid, signal.SIGKILL)
                except OSError:
                    pass
                chrome.wait(10)
                for _ in range(300):  # the listener let go of the browser's connections
                    if not self.server.open:
                        break
                    time.sleep(0.1)
            return Seen.paths
        self.assertIn('/read.png', load(f'http://page.exit.test:{site.server_address[1]}/'))
        self.assertEqual(set(Seen.peers), {'127.0.0.2'})  # the site saw the computer's address only
        self.assertIn('/read.png', load(f'http://127.0.0.1:{site.server_address[1]}/'))
        self.assertEqual(set(Seen.peers), {'127.0.0.1'})  # not listed: straight out from the Machine


class SignInDialog(unittest.TestCase):
    """What the sign-in dialog gets (browser_login_pages) and what the error feed counts, on the app itself."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        x.reset()
        self.addCleanup(x.reset)
        x.configure(self.temp.name)
        self.addCleanup(x.configure, None)
        self.app = object.__new__(machine_main.App)
        self.app.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app.config = {'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite'), 'browser_exit': True}
        form = {'id': '0:t', 'host': 'www.linkedin.com', 'site': 'linkedin.com', 'username': True, 'password': True, 'code': False}
        for name, value in (('pages', lambda *a, **k: [dict(form)]), ('walls', lambda *a, **k: [])):
            patcher = patch.object(machine_app_browser.browser_login, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def pages(self):
        return self.app.browser_login_action('browser_login_pages', {}, owner_dashboard=True)

    def counted(self):
        with self.app.store.connect() as db:
            error_feed.ensure(db)
            return [tuple(r) for r in db.execute('SELECT kind,location,message FROM error_feed')]

    def test_it_asks_for_the_computer_only_while_an_app_with_it_on_is_away(self):
        self.assertNotIn('exit', self.pages())  # no desktop app: as today
        x._remember(at=time.time(), off=False)
        self.assertEqual(self.pages()['exit'], 'LinkedIn')
        with patch.object(x, 'connected', lambda: True):
            self.assertNotIn('exit', self.pages())

    def test_a_sign_in_asked_again_after_the_way_out_changed_is_counted_with_fixed_words(self):
        x.went('linkedin.com', 'computer')
        self.pages()
        self.assertEqual(self.counted(), [])  # never changed: nothing
        x.went('linkedin.com', 'direct')
        self.pages()
        self.pages()  # once per change
        self.assertEqual(self.counted(), [('BrowserExit.signin.computer_to_direct', 'machine/browser_exit.py:linkedin.com', '')])

    def test_a_run_stopped_at_a_sign_in_counts_it_too(self):
        x.went('linkedin.com', 'direct')
        x.went('linkedin.com', 'computer')
        with patch.object(self.app, 'signin_waits', lambda: [('task', 'job', 'https://www.linkedin.com/feed')], create=True), \
             patch.object(self.app, 'signin_tabs', lambda: [], create=True):
            self.app.watch_sign_ins(now=True)
        self.assertEqual(self.counted(), [('BrowserExit.signin.direct_to_computer', 'machine/browser_exit.py:linkedin.com', '')])


if __name__ == '__main__':
    unittest.main()

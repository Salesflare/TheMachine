"""The Machine's browser going out through the owner's computer (machine/browser_exit.py): tm-exit/1's frames, which
sites go that way, the owner-only upgrade at /api/exit, waiting while the computer is away, and a page Chromium opens
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
import machine.main as machine_main
import served
import test_browser_view

CHROME = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome-stable') or shutil.which('chromium-browser')
HOST = 'machine.example:8443'
OWNER = {'Host': HOST, 'Tailscale-User-Login': 'owner@example.com'}
UPGRADE = {**OWNER, 'Origin': 'https://' + HOST, 'Connection': 'Upgrade', 'Upgrade': x.PROTOCOL}


class Frames(unittest.TestCase):
    def test_the_golden_open_frame(self):
        # the same bytes desktop/src/exit.rs's tests decode
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

    def test_listed_sites_wait_only_for_a_computer_that_has_it_on(self):
        self.assertFalse(x.expected())  # never connected
        x._remember(at=time.time(), off=False)
        self.assertTrue(x.expected())
        x._remember(off=True)
        self.assertFalse(x.expected())  # turned off in the app
        x._remember(at=time.time() - x.FORGET - 1, off=False)
        self.assertFalse(x.expected())  # gone too long


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
    """A stand-in for the desktop app's side (desktop/src/exit.rs): the upgrade with the owner's headers, HELLO, and the
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
    """The site: a page that says it, and the address each request came from."""
    peers = []

    def do_GET(self):
        Seen.peers.append(self.client_address[0])
        body = b'<!doctype html><title>Site</title><p>The site page</p>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


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
        server = x.start(self.app.config, self.temp.name)
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

    def test_while_the_computer_is_away_a_listed_site_waits_then_is_refused(self):
        port = self.listener()
        x._remember(at=time.time(), off=False)  # an app with it on was there
        with patch.object(x, 'WAIT', 0.5):
            code, conn = socks(port, 'www.exit.test', 443)
        conn.close()
        self.assertEqual(code, 2)
        self.assertEqual(x.waiting_step()['title'], 'Waiting for your computer to open exit.test')
        # the computer comes back while one waits: it goes through it
        site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Seen)
        threading.Thread(target=site.serve_forever, daemon=True).start()
        self.addCleanup(site.server_close)
        self.addCleanup(site.shutdown)
        Seen.peers.clear()
        late = threading.Timer(0.5, lambda: setattr(self, 'peer', Peer(self.port, lambda host: '127.0.0.1').start()))
        late.start()
        code, conn = socks(port, 'www.exit.test', site.server_address[1])
        late.join()
        self.addCleanup(self.peer.close)
        self.assertEqual(code, 0)
        conn.sendall(b'GET / HTTP/1.1\r\nHost: www.exit.test\r\nConnection: close\r\n\r\n')
        while conn.recv(65536):
            pass
        conn.close()
        self.assertEqual(Seen.peers, ['127.0.0.2'])
        self.assertIsNone(x.waiting_step())  # connected: nothing waits
        # turned off in the app: listed sites go straight out again
        self.peer.close(b'off')
        for _ in range(50):
            if not x.connected():
                break
            time.sleep(0.1)
        self.assertFalse(x.expected())
        begun = time.monotonic()
        code, conn = socks(port, 'www.exit.test', site.server_address[1])  # straight out: a name nobody resolves
        conn.close()
        self.assertEqual(code, 4)
        self.assertLess(time.monotonic() - begun, x.WAIT)

    @unittest.skipUnless(CHROME and sys.platform.startswith('linux'), 'needs Chromium, and 127.0.0.2 (Linux)')
    def test_chromium_through_the_machine_and_the_computer_sees_the_computers_address(self):
        site = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Seen)
        threading.Thread(target=site.serve_forever, daemon=True).start()
        self.addCleanup(site.server_close)
        self.addCleanup(site.shutdown)
        port = self.listener()
        peer = Peer(self.port, lambda host: '127.0.0.1').start()
        self.addCleanup(peer.close)
        profile = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, profile, True)
        Seen.peers.clear()

        def dump(url):
            # the Machine's browser as a hosted Machine starts it, its way out a SOCKS5 proxy (here the listener itself)
            chrome = subprocess.Popen([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--use-mock-keychain', '--no-first-run',
                                       '--user-data-dir=' + profile, f'--proxy-server=socks5://127.0.0.1:{port}', '--proxy-bypass-list=<-loopback>',
                                       '--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable', '--dump-dom', url],
                                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, start_new_session=True)
            try:
                return chrome.communicate(timeout=120)[0]
            finally:  # its helper processes too, with their connections to the listener
                try:
                    os.killpg(chrome.pid, signal.SIGKILL)
                except OSError:
                    pass
                chrome.wait(10)
        self.assertIn('The site page', dump(f'http://page.exit.test:{site.server_address[1]}/'))
        self.assertEqual(set(Seen.peers), {'127.0.0.2'})  # the site saw the computer's address only
        Seen.peers.clear()
        self.assertIn('The site page', dump(f'http://127.0.0.1:{site.server_address[1]}/'))
        self.assertEqual(set(Seen.peers), {'127.0.0.1'})  # not listed: straight out from the Machine


class OnTheTodo(test_browser_view.Fixture):
    def test_a_run_on_the_browser_says_it_waits_for_the_computer(self):
        x.reset()
        self.addCleanup(x.reset)
        said = 'Waiting for your computer to open LinkedIn'
        titles = lambda: [s['title'] for s in self.app.preparation_progress(self.sid)['steps']]
        self.steps(('browser', {'action': 'open', 'url': 'https://www.linkedin.com/'}, test_browser_view.OPENED))
        self.assertNotIn(said, titles())  # nothing waits
        x._waiting['LinkedIn'] = time.time()
        self.assertEqual(titles()[-1], said)
        x._waiting['LinkedIn'] = time.time() - x.WAITING_SHOWN - 1  # over a minute ago: the run's own steps again
        self.assertNotIn(said, titles())
        x._waiting['LinkedIn'] = time.time()
        with self.store.connect() as db:  # the run went on to something else than the browser
            db.execute('INSERT INTO preparation_calls(job_id,call_id,tool,params,result,started_at) VALUES(?,?,?,?,?,?)',
                       (self.job(), 'later', 'exec', '{"command": "ls"}', None, '2026-10-22T08:12:00+00:00'))
        self.assertNotIn(said, titles())


if __name__ == '__main__':
    unittest.main()

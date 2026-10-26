import base64, hashlib, json, socket, struct, sys, threading, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'integrations'))
import browser_cdp  # noqa: E402


class FakeBrowser:
    """Just enough of Chrome's DevTools endpoint: the /json list, new and close calls, and a page WebSocket."""

    def __init__(self, value, exception=None):
        self.value, self.exception, self.tabs, self.calls = value, exception, {'A1': 'page'}, []
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', 0))
        self.server.listen(8)
        self.base = 'http://127.0.0.1:%d' % self.server.getsockname()[1]
        threading.Thread(target=self.serve, daemon=True).start()

    def serve(self):
        while True:
            try:
                conn, _ = self.server.accept()
            except OSError:
                return
            threading.Thread(target=self.handle, args=(conn,), daemon=True).start()

    def answer(self, conn, status, body):
        data = json.dumps(body).encode() if not isinstance(body, bytes) else body
        conn.sendall(b'HTTP/1.1 %s\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % (status.encode(), len(data)) + data)

    def handle(self, conn):
        head = b''
        while b'\r\n\r\n' not in head:
            head += conn.recv(4096)
        method, path = head.split(b' ')[:2]
        method, path = method.decode(), path.decode()
        self.calls.append((method, path))
        if path == '/json/list':
            self.answer(conn, '200 OK', [{'id': i, 'type': t} for i, t in self.tabs.items()] + [{'id': 'W', 'type': 'worker'}])
        elif path.startswith('/json/new?'):
            if method != 'PUT':
                return self.answer(conn, '405 Method Not Allowed', b'use PUT')
            self.tabs['B2'] = 'page'
            self.answer(conn, '200 OK', {'id': 'B2', 'type': 'page', 'url': path[10:]})
        elif path.startswith('/json/close/'):
            found = self.tabs.pop(path[12:], None)
            self.answer(conn, '200 OK' if found else '404 Not Found', b'Target is closing' if found else b'No such target id')
        elif path.startswith('/devtools/page/'):
            key = [l.split(b': ')[1] for l in head.split(b'\r\n') if l.lower().startswith(b'sec-websocket-key')][0]
            accept = base64.b64encode(hashlib.sha1(key + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())
            conn.sendall(b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ' + accept + b'\r\n\r\n')
            request = json.loads(self.read_frame(conn))
            self.calls.append(('ws', request['method'], request['params']))
            conn.sendall(self.frame(json.dumps({'method': 'Page.frameNavigated', 'params': {}}).encode()))
            result = ({'result': {'type': 'object'}, 'exceptionDetails': {'exception': {'description': self.exception}}}
                      if self.exception else {'result': {'type': 'object', 'value': self.value}})
            reply = json.dumps({'id': request['id'], 'result': result}).encode()
            half = len(reply) // 2  # in two fragments, as Chrome may send a big answer
            conn.sendall(self.frame(reply[:half], opcode=1, last=False) + self.frame(reply[half:], opcode=0))
        conn.close()

    @staticmethod
    def read_frame(conn):
        def read(n):
            data = b''
            while len(data) < n:
                data += conn.recv(n - len(data))
            return data
        first, second = read(2)
        n = second & 0x7f
        n = struct.unpack('!H', read(2))[0] if n == 126 else struct.unpack('!Q', read(8))[0] if n == 127 else n
        mask = read(4)
        return bytes(b ^ mask[i % 4] for i, b in enumerate(read(n))).decode()

    @staticmethod
    def frame(data, opcode=1, last=True):
        n = len(data)
        size = struct.pack('!B', n) if n < 126 else struct.pack('!BH', 126, n) if n < 65536 else struct.pack('!BQ', 127, n)
        return struct.pack('!B', (0x80 if last else 0) | opcode) + size + data

    def stop(self):
        try:
            self.server.shutdown(socket.SHUT_RDWR)  # wakes the accept() so the port really closes
        except OSError:
            pass
        self.server.close()


class BrowserCdpTest(unittest.TestCase):
    def test_open_evaluate_and_close_one_tab_without_openclaw(self):
        big = {'messages': [{'text': 'x' * 70000}], 'more': False}
        browser = FakeBrowser(big)
        self.addCleanup(browser.stop)
        self.assertEqual(browser_cdp.tab_ids(browser.base), {'A1'})
        target = browser_cdp.open_tab(browser.base, 'https://www.linkedin.com/robots.txt')
        self.assertEqual(target, 'B2')
        self.assertEqual(browser_cdp.evaluate(browser.base, target, 'async () => ({})', 5000), big)
        ws = [c for c in browser.calls if c[0] == 'ws'][0]
        self.assertEqual(ws[1], 'Runtime.evaluate')
        self.assertTrue(ws[2]['awaitPromise'] and ws[2]['returnByValue'])
        self.assertEqual(ws[2]['expression'], '(async () => ({}))()')
        browser_cdp.close_tab(browser.base, target)
        browser_cdp.close_tab(browser.base, target)  # already gone: fine
        self.assertEqual(browser_cdp.tab_ids(browser.base), {'A1'})

    def test_a_failing_script_or_missing_browser_is_an_error(self):
        browser = FakeBrowser(None, exception='TypeError: boom')
        self.addCleanup(browser.stop)
        with self.assertRaisesRegex(browser_cdp.CdpError, 'boom'):
            browser_cdp.evaluate(browser.base, 'A1', '() => 1', 5000)
        browser.stop()
        with self.assertRaisesRegex(browser_cdp.CdpError, 'not reachable'):
            browser_cdp.tab_ids(browser.base)


if __name__ == '__main__':
    unittest.main()

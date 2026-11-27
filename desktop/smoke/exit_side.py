"""The made-up Machine's side of tm-exit/1 (src/exit.rs), for exit.py: GET /api/exit upgraded, and a SOCKS5 listener on
127.0.0.1 whose every CONNECT goes through the app's connection, as a Machine's browser's would. It keeps what it was
told: the app's HELLO, what the app refused and why, its BYE."""
import json
import socket
import struct
import threading

UPGRADE = 'tm-exit/1'
HELLO, OPEN, OPENED, REFUSED, DATA, END, PING, PONG, BYE = range(1, 10)
MAX = 16384


def frame(kind, stream, payload=b''):
    return struct.pack('>BII', kind, stream, len(payload)) + payload


def read_frame(read):
    head = read(9)
    if len(head) < 9:
        return None
    kind, stream, length = struct.unpack('>BII', head)
    payload = read(length) if length else b''
    return None if len(payload) < length else (kind, stream, payload)


class Tunnel:
    def __init__(self):
        self.wire, self.send_lock, self.lock = None, threading.Lock(), threading.Lock()
        self.streams, self.next = {}, 1
        self.hellos, self.refused, self.byes, self.opened = [], [], [], []
        self.up = threading.Event()  # an app is connected
        self.socks = socket.create_server(('127.0.0.1', 0))
        self.port = self.socks.getsockname()[1]
        threading.Thread(target=self.serve, daemon=True).start()

    def send(self, kind, stream, payload=b''):
        with self.send_lock:
            if not self.wire:
                raise OSError('no app')
            self.wire.sendall(frame(kind, stream, payload))

    # The app's connection

    def take(self, page, own_origin):
        """Page is the stand-in's handler for GET /api/exit."""
        h = page.headers
        if h.get('Upgrade', '').lower() != UPGRADE or 'upgrade' not in h.get('Connection', '').lower():
            return page.answer({'error': 'Upgrade'}, 426)
        if h.get('Origin') != own_origin:
            return page.answer({'error': 'Not from the app'}, 403)
        page.send_response(101)
        page.send_header('Upgrade', UPGRADE)
        page.send_header('Connection', 'Upgrade')
        page.end_headers()
        page.wfile.flush()
        page.close_connection = True
        with self.send_lock:
            self.wire = page.connection
        self.send(HELLO, 0, json.dumps({'v': 1, 'seen_as': page.client_address[0]}).encode())
        self.up.set()
        try:
            while (got := read_frame(page.rfile.read)) is not None:
                kind, stream, payload = got
                if kind == HELLO:
                    self.hellos.append(json.loads(payload))
                elif kind == PING:
                    self.send(PONG, 0, payload)
                elif kind == BYE:
                    self.byes.append(payload.decode())
                    break
                elif kind in (OPENED, REFUSED, DATA, END):
                    with self.lock:
                        s = self.streams.get(stream)
                    if s:
                        s['inbox'](kind, payload)
        except OSError:
            pass
        finally:
            with self.send_lock:
                self.wire = None
            self.up.clear()
            with self.lock:
                for s in list(self.streams.values()):
                    s['inbox'](END, b'')

    # The browser's side: SOCKS5, no sign-in, CONNECT only

    def serve(self):
        while True:
            client, _ = self.socks.accept()
            threading.Thread(target=self.one, args=(client,), daemon=True).start()

    def one(self, client):
        try:
            got = client.recv(2)
            client.recv(got[1])
            client.sendall(b'\x05\x00')
            _, command, _, kind = client.recv(4)
            if kind == 1:
                host = socket.inet_ntoa(client.recv(4))
            elif kind == 3:
                host = client.recv(client.recv(1)[0]).decode()
            else:
                host = socket.inet_ntop(socket.AF_INET6, client.recv(16))
            port = struct.unpack('>H', client.recv(2))[0]
            if command != 1:
                return client.sendall(b'\x05\x07\x00\x01' + bytes(6))
            self.through(client, host, port)
        except (OSError, IndexError, ValueError):
            pass
        finally:
            client.close()

    def through(self, client, host, port):
        answered, ended = threading.Event(), threading.Event()
        said = {}
        with self.lock:
            stream, self.next = self.next, self.next + 1

        def inbox(kind, payload):
            if kind in (OPENED, REFUSED):
                said['kind'], said['why'] = kind, payload.decode()
                answered.set()
            elif kind == DATA:
                try:
                    client.sendall(payload)
                except OSError:
                    pass
            elif kind == END:
                ended.set()
                answered.set()
                try:
                    client.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
        with self.lock:
            self.streams[stream] = {'inbox': inbox}
        try:
            if not self.up.wait(20):
                return client.sendall(b'\x05\x02\x00\x01' + bytes(6))
            self.send(OPEN, stream, json.dumps({'host': host, 'port': port}, separators=(',', ':')).encode())
            if not answered.wait(20) or said.get('kind') != OPENED:
                self.refused.append((host, port, said.get('why', 'no answer')))
                return client.sendall(b'\x05\x02\x00\x01' + bytes(6))
            self.opened.append((host, port))
            client.sendall(b'\x05\x00\x00\x01' + bytes(6))
            while not ended.is_set() and (data := client.recv(MAX)):
                self.send(DATA, stream, data)
            if not ended.is_set():
                self.send(END, stream)
        finally:
            with self.lock:
                self.streams.pop(stream, None)

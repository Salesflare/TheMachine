"""The Machine's browser going out through its owner's own computer (`browser_exit`, off unless set): sites that sign in
by the address they see (LinkedIn, Facebook, X, ...) see the owner's home or office address instead of the data
center's. The desktop app (desktop/src/exit.rs) keeps one connection to its Machine for it, `tm-exit/1` (below), and
opens what the Machine asks for after its own checks: public addresses only, after its own DNS lookup, ports 80 and
443, with caps. Nothing listens on the computer.

Here: a SOCKS5 listener on 127.0.0.1 of the Machine's host (EXIT_PORT; a hosted Machine's gost chains its direct way
out to it, the cloud agent), and the tunnels the owner's desktop apps opened with `GET /api/exit` (handler.py, owner
only, same origin). A listed site (browser_exit_sites, a host and its subdomains) goes through the newest tunnel; every
other site goes straight out from here, as before. With no app connected, listed sites go straight out too, right away:
browsing never stalls on the computer. Only the Machine's own sign-in dialog asks first (away()): while the owner has
a desktop app with it on (`browser-exit.json` next to the database: when one was last connected, and whether it said it
was turned off) but none is connected, it says to open the app, with a way to sign in without it. When an
app connects, listed sites' direct connections are closed, so the browser opens them again through it.

A listed site's way out (computer or direct) is kept per site; a challenge on it (a robot check, a verify-it's-you
page, a sign-in asked again) soon after that way changed is counted in the error feed (challenge()), so the team sees
per site whether going out from the Machine in between causes trouble.

tm-exit/1, after `101 Switching Protocols`, both ways: frames of `type u8 | stream u32 BE | length u32 BE | payload`,
payload at most MAX_FRAME. HELLO (JSON, first, stream 0), OPEN (Machine to app, JSON host and port), OPENED, REFUSED
(ASCII reason), DATA, END (the stream is closed on both sides), PING/PONG (every PING_EVERY seconds; DEAD seconds
without a frame drop it), BYE (ASCII reason; `off`: the owner turned it off). Only the Machine opens streams. No
window: a stream's data is written to its socket before the next frame is read, with a write timeout that ends it."""
import ipaddress
import json
from pathlib import Path
import re
import socket
import socketserver
import struct
import threading
import time

from machine.config import LOG

LAYER = 0

PROTOCOL = 'tm-exit/1'
EXIT_PORT = 1056
HELLO, OPEN, OPENED, REFUSED, DATA, END, PING, PONG, BYE = range(1, 10)
HEADER = struct.Struct('>BII')
MAX_FRAME = 16384
PING_EVERY = 20
DEAD = 60  # seconds without a frame from the app: gone
OPEN_WAIT = 15  # seconds the app has to say OPENED or REFUSED
WRITE = 30  # seconds a write to one stream's socket may take before that stream ends
CONNECT = 10  # seconds to connect straight out
CONNECTIONS = 256  # the listener's connections at once
STREAMS = 64  # streams on one tunnel at once (the app's own cap too)
TUNNELS = 4  # an owner's computers connected at once; the oldest gives way
FORGET = 14 * 86400  # seconds after the last connected app that the sign-in dialog stops asking for it
SWITCHED = 86400  # seconds after a listed site's way out changed that a challenge on it is counted
SITES = {'linkedin.com': 'LinkedIn', 'facebook.com': 'Facebook', 'messenger.com': 'Messenger', 'instagram.com': 'Instagram',
         'x.com': 'X', 'twitter.com': 'X', 'threads.com': 'Threads', 'threads.net': 'Threads'}
STATE = 'browser-exit.json'

_lock = threading.Condition()
_tunnels = []  # newest last
_ways = {}  # listed site -> {'way': 'computer' or 'direct', 'before': the way before, 'at': when it changed}
_told = set()  # (site, challenge, when its way changed): counted once
_direct = set()  # listed sites' browser connections going straight out, closed when an app connects
_state = {'path': None}


def frame(kind, stream=0, payload=b''):
    if len(payload) > MAX_FRAME:
        raise ValueError(len(payload))  # too long
    return HEADER.pack(kind, stream, len(payload)) + payload


def read_frame(read):
    """(type, stream, payload) from `read(n)` (a buffered reader's read: fewer bytes only at the end), or None at the
    end. A frame longer than MAX_FRAME is a broken peer: ValueError."""
    head = _exact(read, HEADER.size)
    if head is None:
        return None
    kind, stream, length = HEADER.unpack(head)
    if length > MAX_FRAME:
        raise ValueError(length)  # too long
    payload = _exact(read, length) if length else b''
    if payload is None:
        return None
    return kind, stream, payload


def _exact(read, n):
    data = b''
    while len(data) < n:
        part = read(n - len(data))
        if not part:
            return None
        data += part
    return data


def sites(config):
    """The listed sites, as host suffixes: the config's, or SITES."""
    listed = config.get('browser_exit_sites')
    if not isinstance(listed, list):
        return list(SITES)
    return [s.strip().lower().strip('.') for s in listed if isinstance(s, str) and s.strip().strip('.')][:100]


def listed(host, suffixes):
    """The listed site a host is on (its suffix), or None. Hosts compare without case and a trailing dot."""
    host = str(host or '').lower().rstrip('.')
    return next((s for s in suffixes if host == s or host.endswith('.' + s)), None)


def site_name(suffix):
    return SITES.get(suffix, suffix)


def public(address):
    """An address on the public internet, for `seen_as`: None for anything else or garbage."""
    try:
        ip = ipaddress.ip_address(str(address or '').strip())
    except ValueError:
        return None
    return str(ip) if ip.is_global else None


# ---------------------------------------------------------------- remembered: whether an app of the owner's is expected

def configure(folder):
    _state['path'] = Path(folder) / STATE if folder else None


def _remembered():
    path = _state['path']
    try:
        data = json.loads(path.read_text()) if path else {}
    except (OSError, ValueError):
        data = {}
    return data if isinstance(data, dict) else {}


def _remember(**values):
    path = _state['path']
    if not path:
        return
    data = {**_remembered(), **values}
    try:
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(data))
        temp.replace(path)
    except OSError as error:
        LOG.warning('browser exit state not saved: %s', type(error).__name__)


def expected(now=None):
    """Whether the owner has a desktop app with it on: one connected within FORGET seconds and wasn't turned off."""
    data = _remembered()
    at = data.get('at') if isinstance(data.get('at'), (int, float)) else 0
    return not data.get('off') and (now or time.time()) - at < FORGET


# ---------------------------------------------------------------- one desktop app's connection

class Stream:
    def __init__(self, local):
        self.local = local
        self.answer = threading.Event()
        self.refused = None
        self.closed = False


class Tunnel:
    """One desktop app's tm-exit/1 connection: `read` its buffered reader's read, `sock` the socket to write to."""

    def __init__(self, read, sock, seen_as=None):
        self.read, self.sock, self.seen_as = read, sock, seen_as
        self.write_lock = threading.Lock()
        self.streams = {}
        self.next_id = 1
        self.gone = threading.Event()
        self.app = {}

    def send(self, kind, stream=0, payload=b''):
        data = frame(kind, stream, payload)
        with self.write_lock:
            self.sock.sendall(data)

    def hello(self):
        """The app's HELLO, then the Machine's. False when it isn't one."""
        got = read_frame(self.read)
        if not got or got[0] != HELLO or got[1] != 0:
            return False
        try:
            self.app = json.loads(got[2] or b'{}')
        except ValueError:
            return False
        return isinstance(self.app, dict) and self.app.get('v') == 1

    def welcome(self):
        self.send(HELLO, 0, json.dumps({'v': 1, 'seen_as': self.seen_as}, separators=(',', ':')).encode())

    def open(self, host, port, local):
        """A stream to host:port through the app: the Stream, or the app's reason it refused."""
        stream = Stream(local)
        with _lock:
            if len(self.streams) >= STREAMS:
                return 'busy'
            sid, self.next_id = self.next_id, self.next_id + 1
            self.streams[sid] = stream
        try:
            self.send(OPEN, sid, json.dumps({'host': host, 'port': port}, separators=(',', ':')).encode())
            answered = stream.answer.wait(OPEN_WAIT)
        except OSError:
            answered = False
        if not answered or stream.refused:
            stream.closed = True  # the browser's socket stays, for the caller's answer
            self.drop(sid, tell=not answered)
            return stream.refused or 'timeout'
        stream.id = sid
        local.settimeout(WRITE)  # for writes to it (run); pump's reads only look again
        return stream

    def drop(self, sid, tell=False):
        with _lock:
            stream = self.streams.pop(sid, None)
        if stream and not stream.closed:
            stream.closed = True
            _close(stream.local)
        if tell:
            try:
                self.send(END, sid)
            except OSError:
                pass

    def pump(self, stream):
        """The browser's side of a stream, to the app, until it ends."""
        while not stream.closed:
            try:
                data = stream.local.recv(MAX_FRAME)
            except TimeoutError:  # quiet for a while: a kept-alive connection
                continue
            except OSError:
                break
            if not data:
                break
            try:
                self.send(DATA, stream.id, data)
            except OSError:
                break
        self.drop(stream.id, tell=True)

    def run(self):
        """The app's frames until it goes. Pings the app meanwhile."""
        pinger = threading.Thread(target=self._ping, daemon=True, name='browser-exit-ping')
        pinger.start()
        try:
            while (got := read_frame(self.read)) is not None:
                kind, sid, payload = got
                if kind == PING:
                    self.send(PONG, 0, payload[:64])
                elif kind in (OPENED, REFUSED):
                    stream = self.streams.get(sid)
                    if stream:
                        stream.refused = payload.decode('ascii', 'replace')[:20] or 'refused' if kind == REFUSED else None
                        stream.answer.set()
                elif kind == DATA:
                    stream = self.streams.get(sid)
                    if stream:
                        try:
                            stream.local.sendall(payload)
                        except OSError:
                            self.drop(sid, tell=True)
                elif kind == END:
                    self.drop(sid)
                elif kind == BYE:
                    if payload.startswith(b'off'):
                        _remember(off=True, at=time.time())
                    break
        except (OSError, ValueError, struct.error):
            pass
        finally:
            self.gone.set()
            for sid, stream in list(self.streams.items()):
                if not stream.answer.is_set():  # still opening: open() answers the browser
                    stream.refused = 'gone'
                    stream.answer.set()
                else:
                    self.drop(sid)

    def _ping(self):
        while not self.gone.wait(PING_EVERY):
            try:
                self.send(PING, 0, b'm')
            except OSError:
                _close(self.sock)
                return


def carry(rfile, connection, seen_as=None):
    """A desktop app's tm-exit/1 connection, already accepted by the caller's checks (owner, same origin, the
    upgrade): answers 101 and carries its streams until it goes."""
    connection.settimeout(DEAD)
    connection.sendall(f'HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: {PROTOCOL}\r\n\r\n'.encode())
    tunnel = Tunnel(rfile.read, connection, public(seen_as))
    try:
        if not tunnel.hello():
            return
    except (OSError, ValueError, struct.error):
        return
    _remember(at=time.time(), off=False)
    with _lock:
        _tunnels.append(tunnel)
        while len(_tunnels) > TUNNELS:
            old = _tunnels.pop(0)
            _close(old.sock)
        _lock.notify_all()
        moved = list(_direct)
    for conn in moved:  # the browser opens them again, through the computer
        _close(conn)
    LOG.info('browser exit: a computer connected (%s)', str(tunnel.app.get('os') or '?')[:12])
    try:
        tunnel.welcome()  # once it is the one in use: what the app sends after this has a tunnel to go to
        tunnel.run()
    except OSError:
        pass
    finally:
        with _lock:
            if tunnel in _tunnels:
                _tunnels.remove(tunnel)
        if not _remembered().get('off'):
            _remember(at=time.time())
        LOG.info('browser exit: a computer went')


def tunnel():
    """The newest connected tunnel, or None."""
    with _lock:
        live = [t for t in _tunnels if not t.gone.is_set()]
        return live[-1] if live else None


def connected():
    with _lock:
        return any(not t.gone.is_set() for t in _tunnels)


def away(config, hosts):
    """The listed site's name the sign-in dialog asks the owner's computer for: one of `hosts` is listed, the owner has
    a desktop app with it on, and none is connected. None otherwise, and while `browser_exit` is off."""
    if not config.get('browser_exit') or connected() or not expected():
        return None
    suffixes = sites(config)
    site = next((s for s in (listed(h, suffixes) for h in hosts) if s), None)
    return site_name(site) if site else None


def went(site, way, now=None):
    """A listed site's connection went out `way` ('computer' or 'direct')."""
    now = now or time.time()
    with _lock:
        last = _ways.get(site)
        if not last:
            _ways[site] = {'way': way, 'before': None, 'at': now}
        elif last['way'] != way:
            _ways[site] = {'way': way, 'before': last['way'], 'at': now}


CHALLENGES = ('signin', 'checkpoint', 'captcha', 'wall')  # a sign-in form, a code-only check, a robot check, a block page


def challenge(config, host, what, now=None):
    """A challenge (CHALLENGES) on `host` soon after its listed site's way out changed: (site, before, after) to count,
    once per change; None otherwise. The site is one of SITES' own names or 'other', never an owner's own entry."""
    if what not in CHALLENGES or not config.get('browser_exit'):
        return None
    site = listed(host, sites(config))
    now = now or time.time()
    with _lock:
        last = _ways.get(site) if site else None
        if not last or not last['before'] or now - last['at'] > SWITCHED or (site, what, last['at']) in _told:
            return None
        _told.add((site, what, last['at']))
        return (site if site in SITES else 'other'), last['before'], last['way']


def reset():
    with _lock:
        for t in _tunnels:
            _close(t.sock)
        _tunnels.clear()
        _ways.clear()
        _told.clear()
        _direct.clear()


def _close(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        sock.close()
    except OSError:
        pass


# ---------------------------------------------------------------- the browser's side: SOCKS5 on 127.0.0.1

def _socks_target(conn):
    """The SOCKS5 greeting and CONNECT (no sign-in: 127.0.0.1 only): (host, port), or None after answering why not."""
    read = conn.recv  # unbuffered: what the browser sends after the reply stays in the socket for the stream
    head = _exact(read, 2)
    if not head or head[0] != 5:
        return None
    methods = _exact(read, head[1]) or b''
    if 0 not in methods:
        conn.sendall(b'\x05\xff')
        return None
    conn.sendall(b'\x05\x00')
    request = _exact(read, 4)
    if not request or request[0] != 5:
        return None
    if request[1] != 1:  # CONNECT only
        conn.sendall(b'\x05\x07\x00\x01' + bytes(6))
        return None
    kind = request[3]
    if kind == 1:
        host = socket.inet_ntop(socket.AF_INET, _exact(read, 4) or bytes(4))
    elif kind == 4:
        host = socket.inet_ntop(socket.AF_INET6, _exact(read, 16) or bytes(16))
    elif kind == 3:
        length = (_exact(read, 1) or b'\x00')[0]
        host = (_exact(read, length) or b'').decode('ascii', 'replace') if length else ''  # a browser sends punycode
        if not re.fullmatch(r'[A-Za-z0-9._-]{1,253}', host):
            host = ''
    else:
        conn.sendall(b'\x05\x08\x00\x01' + bytes(6))
        return None
    port = struct.unpack('>H', _exact(read, 2) or b'\x00\x00')[0]
    if not host or not port:
        conn.sendall(b'\x05\x01\x00\x01' + bytes(6))
        return None
    return host, port


OK_REPLY = b'\x05\x00\x00\x01' + bytes(6)
NOT_ALLOWED = b'\x05\x02\x00\x01' + bytes(6)
UNREACHABLE = b'\x05\x04\x00\x01' + bytes(6)


def splice(a, b):
    """Bytes both ways between two sockets until either ends."""
    def one(src, dst):
        try:
            while data := src.recv(65536):
                dst.sendall(data)
        except OSError:
            pass
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    other = threading.Thread(target=one, args=(b, a), daemon=True)
    other.start()
    one(a, b)
    other.join(WRITE)


class Listener(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, port, config):
        self.config = config
        self.slots = threading.BoundedSemaphore(CONNECTIONS)
        self.open = set()
        super().__init__(('127.0.0.1', port), _Handler)

    def server_close(self):
        """Closed with the browser's connections that are still open."""
        super().server_close()
        for conn in list(self.open):
            _close(conn)


class _Handler(socketserver.BaseRequestHandler):
    def handle(self):
        server = self.server
        if not server.slots.acquire(blocking=False):
            return
        conn = self.request
        server.open.add(conn)
        try:
            conn.settimeout(CONNECT)
            target = _socks_target(conn)
            if not target:
                return
            conn.settimeout(None)
            route(conn, *target, server.config)
        except (OSError, ValueError, UnicodeError):
            pass
        finally:
            server.open.discard(conn)
            _close(conn)
            server.slots.release()


def route(conn, host, port, config, direct=None):
    """One browser connection: a listed site through the owner's computer while one is connected, anything else (and a
    listed site with none) straight out. `direct` connects straight out (socket.create_connection; tests give their own)."""
    site = listed(host, sites(config))
    carrier = tunnel() if site else None
    if carrier:
        went(site, 'computer')
        stream = carrier.open(host, port, conn)
        if isinstance(stream, str):
            LOG.info('browser exit: refused by the computer (%s)', stream)
            conn.sendall(NOT_ALLOWED)
            return
        conn.sendall(OK_REPLY)
        carrier.pump(stream)
        return
    if site:
        went(site, 'direct')
    try:
        out = (direct or socket.create_connection)((host, port), CONNECT)
    except OSError:
        conn.sendall(UNREACHABLE)
        return
    try:
        out.settimeout(None)
        conn.sendall(OK_REPLY)
        if site:
            with _lock:
                _direct.add(conn)
        splice(conn, out)
    finally:
        with _lock:
            _direct.discard(conn)
        _close(out)


def start(config, folder):
    """The listener, in a thread of its own, while `browser_exit` is on. None when it is off or its port is taken."""
    if not config.get('browser_exit'):
        return None
    configure(folder)
    try:
        server = Listener(int(config.get('browser_exit_port', EXIT_PORT)), config)
    except OSError as error:
        LOG.error('browser exit: listener not started: %s', type(error).__name__)
        return None
    threading.Thread(target=server.serve_forever, daemon=True, name='browser-exit').start()
    return server

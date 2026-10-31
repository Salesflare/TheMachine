"""A self-hosted Machine's own address for AIs (ai_reach.py): the certificate from a CA over ACME with TLS-ALPN-01
(a fake CA here that checks the challenge certificate through the Machine's own TLS), ZeroSSL when the first CA
fails, renewal timing, and the dial-back through a fake cloud: only the public paths answer, with the mcp host as
issuer and no owner sign-in; a 401 stops the loop. Without `cryptography` Settings says so and nothing starts."""
import datetime as dt
import hashlib
import http.client
import importlib.util
import io
import json
import socket
import ssl
import stat
import tempfile
import threading
import time
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import ai_app
import ai_reach
import fleet

spec = importlib.util.spec_from_file_location('reach_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

HOST = 'pat.mcp.themachine.computer'
needs = unittest.skipUnless(ai_reach.AVAILABLE, 'needs the cryptography package')

if ai_reach.AVAILABLE:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
    from cryptography.x509.oid import NameOID


def unb64u(text):
    import base64
    return base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))


def serve_then_close(sock, host, challenges, cert_context):
    try:
        ai_reach.serve(sock, b'', host, None, challenges, cert_context)
    finally:
        sock.close()


class FakeCA:
    """An ACME server (RFC 8555) that validates TLS-ALPN-01 by a TLS handshake with the Machine's own serve()."""

    def __init__(self, challenges, eab=None, refuse_orders=False, days=90):
        self.challenges, self.eab, self.refuse_orders, self.days = challenges, eab, refuse_orders, days
        self.key = ec.generate_private_key(ec.SECP256R1())
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Fake CA')])
        now = dt.datetime.now(dt.timezone.utc)
        self.cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(self.key.public_key())
                     .serial_number(1).not_valid_before(now - dt.timedelta(days=1)).not_valid_after(now + dt.timedelta(days=900))
                     .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
                     .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
                     .add_extension(x509.SubjectKeyIdentifier.from_public_key(self.key.public_key()), critical=False)
                     .sign(self.key, hashes.SHA256()))
        self.nonces, self.accounts, self.seen, self.order = set(), {}, [], {}
        ca = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def reply(self, status, body=b'', kind='application/json', headers=None):
                nonce = 'n' + str(len(ca.nonces)) + 'x' * 8
                ca.nonces.add(nonce)
                self.send_response(status)
                self.send_header('Replay-Nonce', nonce)
                self.send_header('Content-Type', kind)
                for k, v in (headers or {}).items():
                    self.send_header(k, v)
                data = body if isinstance(body, bytes) else json.dumps(body).encode()
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_HEAD(self):
                self.reply(200)

            def do_GET(self):
                base = ca.url
                self.reply(200, {'newNonce': base + '/nonce', 'newAccount': base + '/acct', 'newOrder': base + '/order-new',
                                 'meta': {'externalAccountRequired': bool(ca.eab)}})

            def do_POST(self):
                jws = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                protected = json.loads(unb64u(jws['protected']))
                assert protected['nonce'] in ca.nonces, 'unknown nonce'
                ca.nonces.discard(protected['nonce'])
                assert protected['url'] == ca.url + self.path
                key = ca.public(protected['jwk']) if 'jwk' in protected else ca.accounts[protected['kid']]
                raw = unb64u(jws['signature'])
                key.verify(encode_dss_signature(int.from_bytes(raw[:32], 'big'), int.from_bytes(raw[32:], 'big')),
                           f"{jws['protected']}.{jws['payload']}".encode(), ec.ECDSA(hashes.SHA256()))
                payload = json.loads(unb64u(jws['payload'])) if jws['payload'] else None
                ca.seen.append((self.path, payload))
                return ca.route(self, self.path, payload, protected)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.url = f'http://127.0.0.1:{self.server.server_port}'
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    @staticmethod
    def public(jwk):
        return ec.EllipticCurvePublicNumbers(int.from_bytes(unb64u(jwk['x']), 'big'), int.from_bytes(unb64u(jwk['y']), 'big'),
                                             ec.SECP256R1()).public_key()

    def route(self, h, path, payload, protected):
        if path == '/acct':
            if self.eab:
                binding = payload['externalAccountBinding']
                head = json.loads(unb64u(binding['protected']))
                import hmac
                mac = hmac.new(unb64u(self.eab[1]), f"{binding['protected']}.{binding['payload']}".encode(), hashlib.sha256).digest()
                assert head['kid'] == self.eab[0] and unb64u(binding['signature']) == mac
                assert json.loads(unb64u(binding['payload'])) == protected['jwk']
            kid = self.url + '/acct/1'
            self.accounts[kid] = self.public(protected['jwk'])
            self.jwk = protected['jwk']
            return h.reply(201, {'status': 'valid'}, headers={'Location': kid})
        if path == '/order-new':
            if self.refuse_orders:
                return h.reply(400, {'type': 'urn:ietf:params:acme:error:rejectedIdentifier', 'detail': 'no'}, 'application/problem+json')
            self.host = payload['identifiers'][0]['value']
            self.order = {'status': 'pending', 'authorizations': [self.url + '/authz/1'], 'finalize': self.url + '/finalize/1'}
            self.authz = 'pending'
            return h.reply(201, self.order, headers={'Location': self.url + '/order/1'})
        if path == '/authz/1':
            return h.reply(200, {'status': self.authz, 'challenges': [
                {'type': 'http-01', 'url': self.url + '/chall/0', 'token': 'other'},
                {'type': 'tls-alpn-01', 'url': self.url + '/chall/1', 'token': 'tok-123'}]})
        if path == '/chall/1':
            self.authz = 'valid' if self.validate('tok-123') else 'invalid'
            return h.reply(200, {'status': 'processing'})
        if path == '/finalize/1':
            csr = x509.load_der_x509_csr(unb64u(payload['csr']))
            names = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName)
            assert names == [self.host]
            now = dt.datetime.now(dt.timezone.utc)
            leaf = (x509.CertificateBuilder().subject_name(csr.subject).issuer_name(self.cert.subject).public_key(csr.public_key())
                    .serial_number(2).not_valid_before(now - dt.timedelta(minutes=1)).not_valid_after(now + dt.timedelta(days=self.days))
                    .add_extension(x509.SubjectAlternativeName([x509.DNSName(self.host)]), critical=False)
                    .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(self.key.public_key()), critical=False)
                    .sign(self.key, hashes.SHA256()))
            self.chain = leaf.public_bytes(serialization.Encoding.PEM) + self.cert.public_bytes(serialization.Encoding.PEM)
            self.order.update(status='valid', certificate=self.url + '/cert/1')
            return h.reply(200, self.order)
        if path == '/order/1':
            return h.reply(200, self.order)
        if path == '/cert/1':
            return h.reply(200, self.chain, 'application/pem-certificate-chain')
        return h.reply(404, {'type': 'urn:ietf:params:acme:error:malformed'}, 'application/problem+json')

    def validate(self, token):
        """RFC 8737: TLS to the name with ALPN acme-tls/1 only; the certificate must hold the key authorization's
        digest in a critical acmeIdentifier extension."""
        thumb = ai_reach.b64u(hashlib.sha256(json.dumps(self.jwk, sort_keys=True, separators=(',', ':')).encode()).digest())
        mine, theirs = socket.socketpair()
        threading.Thread(target=serve_then_close, args=(theirs, self.host, self.challenges, lambda: None), daemon=True).start()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
        ctx.set_alpn_protocols([ai_reach.ALPN_ACME])
        with ctx.wrap_socket(mine, server_hostname=self.host) as tls:
            assert tls.selected_alpn_protocol() == ai_reach.ALPN_ACME
            cert = x509.load_der_x509_certificate(tls.getpeercert(binary_form=True))
        ext = cert.extensions.get_extension_for_oid(x509.ObjectIdentifier(ai_reach.OID_ACME_IDENTIFIER))
        self.checked = (ext.critical, ext.value.value, cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName))
        digest = hashlib.sha256(f'{token}.{thumb}'.encode()).digest()
        return ext.critical and ext.value.value == b'\x04\x20' + digest


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.config = {'database': str(self.dir / 'events.sqlite'), 'accounts': [{'id': 'w', 'email': 'pat@example.com'}],
                       'credentials': {}, 'dashboard_host': 'desk.tailnet.example', 'dashboard_path': '/'}


@needs
class Certificate(Base):
    def test_lets_encrypt_checks_the_challenge_through_the_machines_own_tls(self):
        challenges = {}
        ca = FakeCA(challenges)
        self.addCleanup(ca.close)
        self.assertEqual(ai_reach.obtain(self.config, HOST, challenges, cas=(('letsencrypt', ca.url),), wait=lambda s: None), 'letsencrypt')
        critical, value, names = ca.checked
        self.assertTrue(critical)
        self.assertEqual(names, [HOST])
        self.assertEqual(len(value), 34)
        self.assertEqual(challenges, {})  # the challenge certificate only while the CA looks
        for name in (ai_reach.KEY_FILE, ai_reach.CERT_FILE, ai_reach.ACCOUNT_FILE):
            self.assertEqual(stat.S_IMODE((self.dir / name).stat().st_mode), 0o600, name)
        cert, _ = ai_reach.load_cert(self.config)
        self.assertEqual(ai_reach.names_of(cert), [HOST])
        self.assertFalse(ai_reach.needs_cert(self.config, HOST))
        self.assertTrue(ai_reach.needs_cert(self.config, 'sam.mcp.themachine.computer'))  # a new name: a new certificate

    def test_zerossl_when_the_first_ca_refuses_with_a_bound_account(self):
        challenges, asked = {}, []
        refusing = FakeCA(challenges, refuse_orders=True)
        self.addCleanup(refusing.close)
        binding = ('kid-1', ai_reach.b64u(b'k' * 32))
        zerossl = FakeCA(challenges, eab=binding)
        self.addCleanup(zerossl.close)
        got = ai_reach.obtain(self.config, HOST, challenges, email='pat@example.com',
                              cas=(('letsencrypt', refusing.url), ('zerossl', zerossl.url)),
                              eab=lambda email: asked.append(email) or binding, wait=lambda s: None)
        self.assertEqual((got, asked), ('zerossl', ['pat@example.com']))
        self.assertEqual(set(json.loads((self.dir / ai_reach.ACCOUNT_FILE).read_text())), {'letsencrypt', 'zerossl'})

    def test_renewal_with_thirty_days_left(self):
        challenges = {}
        ca = FakeCA(challenges, days=40)
        self.addCleanup(ca.close)
        ai_reach.obtain(self.config, HOST, challenges, cas=(('letsencrypt', ca.url),), wait=lambda s: None)
        now = dt.datetime.now(dt.timezone.utc)
        self.assertFalse(ai_reach.needs_cert(self.config, HOST, now + dt.timedelta(days=9)))
        self.assertTrue(ai_reach.needs_cert(self.config, HOST, now + dt.timedelta(days=11)))
        ai_reach.drop(self.config)
        self.assertFalse(any((self.dir / n).exists() for n in (ai_reach.KEY_FILE, ai_reach.CERT_FILE, ai_reach.ACCOUNT_FILE)))
        self.assertTrue(ai_reach.needs_cert(self.config, HOST))

    def test_a_hello_for_another_name_gets_no_certificate(self):
        mine, theirs = socket.socketpair()
        asked = []
        done = threading.Thread(target=serve_then_close, args=(theirs, HOST, {}, lambda: asked.append(1)))
        done.start()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
        with self.assertRaises((ssl.SSLError, OSError)):
            ctx.wrap_socket(mine, server_hostname='sam.mcp.themachine.computer')
        done.join(5)
        mine.close()
        self.assertEqual(asked, [])  # its certificate never came out


class FakeCloud:
    """mcp-wait announces one connection, then says 401; mcp-stream answers 101 and then plays the AI: TLS to the
    Machine's name (trusting only the fake CA) and a few requests on one connection."""

    def __init__(self, ca_pem, requests):
        self.ca_pem, self.requests, self.waits, self.answers, self.streams = ca_pem, requests, [], [], []
        self.done = threading.Event()
        self.sock = socket.socket()
        self.sock.bind(('127.0.0.1', 0))
        self.sock.listen()
        self.url = f'http://127.0.0.1:{self.sock.getsockname()[1]}'
        threading.Thread(target=self.accept, daemon=True).start()

    def accept(self):
        while True:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            threading.Thread(target=self.one, args=(conn,), daemon=True).start()

    def one(self, conn):
        head = b''
        while b'\r\n\r\n' not in head:
            head += conn.recv(4096)
        line, _, rest = head.partition(b'\r\n')
        headers = http.client.parse_headers(io.BytesIO(rest))
        path = line.split(b' ')[1].decode()
        if path.startswith('/api/fleet/mcp-wait'):
            self.waits.append((path, headers['Authorization']))
            body = json.dumps({'conns': ['ab' * 8]}).encode() if len(self.waits) == 1 else b'{}'
            status = '200 OK' if len(self.waits) == 1 else '401 Unauthorized'
            conn.sendall(f'HTTP/1.1 {status}\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n'.encode() + body)
            conn.close()
            return
        self.streams.append((path, headers['Authorization'], headers['Upgrade'], headers['Connection']))
        conn.sendall(b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: tm-mcp-stream/1\r\nConnection: Upgrade\r\n\r\n')
        ctx = ssl.create_default_context(cadata=self.ca_pem.decode())
        ctx.set_alpn_protocols(['http/1.1'])
        with ctx.wrap_socket(conn, server_hostname=HOST) as tls:
            for method, path, extra in self.requests:
                body = b'{"jsonrpc":"2.0","id":1,"method":"tools/list"}' if method == 'POST' else b''
                head = f'{method} {path} HTTP/1.1\r\nHost: {HOST}\r\nContent-Length: {len(body)}\r\n' + ''.join(f'{k}: {v}\r\n' for k, v in extra.items())
                tls.sendall(head.encode() + b'\r\n' + body)
                response = http.client.HTTPResponse(tls)
                response.begin()
                self.answers.append((response.status, dict(response.getheaders()), response.read()))
        self.done.set()

    def close(self):
        self.sock.close()


@needs
class DialBack(Base):
    def test_only_the_public_paths_answer_on_the_mcp_host_and_a_401_stops(self):
        challenges = {}
        ca = FakeCA(challenges)
        self.addCleanup(ca.close)
        ai_reach.obtain(self.config, HOST, challenges, cas=(('letsencrypt', ca.url),), wait=lambda s: None)
        app = object.__new__(a.App)
        app.store = a.Store(self.config['database'])
        app.config, app.stop = self.config, threading.Event()
        app.ai_reach_kept = (time.monotonic() + 3600, {'name': 'pat'})
        app.fleet = object.__new__(fleet.Fleet)
        app.fleet.relay = type('Relay', (), {'token': 'fd_' + 'd' * 30})()
        cloud = FakeCloud(ca.cert.public_bytes(serialization.Encoding.PEM), [
            ('GET', '/.well-known/oauth-authorization-server', {}),
            ('GET', '/.well-known/oauth-protected-resource/mcp', {}),
            ('POST', '/mcp', {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}),
            ('GET', '/oauth/authorize?client_id=x', {}),
            ('GET', '/api/status', {'Tailscale-User-Login': 'owner@example.com'}),
            ('GET', '/', {}),
        ])
        self.addCleanup(cloud.close)
        loop = ai_reach.Reach(self.config, ai_app.AiReachSide(app), base=cloud.url)
        stop = threading.Event()
        runner = threading.Thread(target=loop.run, args=(stop,))
        runner.start()
        runner.join(30)
        self.assertFalse(runner.is_alive())
        self.assertEqual(loop.state, 'refused')  # the account refused the token: the loop ended by itself
        self.assertTrue(cloud.done.wait(30))
        self.assertEqual([w[1] for w in cloud.waits], ['Bearer fd_' + 'd' * 30] * 2)
        self.assertEqual(cloud.streams, [('/api/fleet/mcp-stream/' + 'ab' * 8, 'Bearer fd_' + 'd' * 30, 'tm-mcp-stream/1', 'Upgrade')])
        meta, resource, mcp, authorize, status, root = cloud.answers
        found = json.loads(meta[2])
        self.assertEqual((found['issuer'], found['authorization_endpoint']),
                         ('https://' + HOST, 'https://desk.tailnet.example/oauth/authorize'))
        self.assertEqual(json.loads(resource[2])['resource'], f'https://{HOST}/mcp')
        self.assertEqual(mcp[0], 401)
        self.assertIn(f'resource_metadata="https://{HOST}/.well-known/oauth-protected-resource/mcp"', mcp[1]['WWW-Authenticate'])
        self.assertEqual([authorize[0], status[0], root[0]], [404, 404, 404])  # no sign-in, no dashboard, no owner


class WithoutCryptography(Base):
    def setUp(self):
        super().setUp()
        self.app = object.__new__(a.App)
        self.app.store = a.Store(self.config['database'])
        self.app.config, self.app.config_path, self.app.stop = self.config, None, threading.Event()
        self.app.fleet = object.__new__(fleet.Fleet)
        self.app.fleet.relay = type('Relay', (), {'call': lambda *args, **kwargs: {'username': 'pat', 'hosted': False}})()

    def test_settings_says_so_and_nothing_starts(self):
        with patch.object(ai_reach, 'AVAILABLE', False), patch('ai_app.threading.Thread') as thread:
            reach = self.app.ai_reach()
            self.assertEqual((reach['address'], reach['tls']), (f'https://{HOST}/mcp', 'missing'))
            self.assertIsNone(self.app.ai_reach_start(threading.Event()))
            thread.assert_not_called()
        self.assertIn('Install the cryptography package to use this address.', Path(a.__file__).parent.joinpath('dashboard/settings-ai.js').read_text())

    def test_unpair_drops_the_certificate(self):
        for name in (ai_reach.KEY_FILE, ai_reach.CERT_FILE, ai_reach.ACCOUNT_FILE):
            (self.dir / name).write_text('x')
        self.app.fleet_drop = lambda: setattr(self.app, 'fleet', None)
        self.app.ai_unpair({})
        self.assertFalse(any((self.dir / n).exists() for n in (ai_reach.KEY_FILE, ai_reach.CERT_FILE, ai_reach.ACCOUNT_FILE)))

    def test_hosted_starts_nothing_here(self):
        self.config['manage_url'] = 'https://app.themachine.computer/setup'
        self.assertIsNone(self.app.ai_reach_start(threading.Event()))


if __name__ == '__main__':
    unittest.main()

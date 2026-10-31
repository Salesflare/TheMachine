"""A self-hosted Machine's own address for AIs: https://<name>.mcp.themachine.computer/mcp (docs/ai-connections.md,
Where it runs). The cloud forwards, never reads (docs/network.md): it reads only the name in the AI's TLS hello and
passes the bytes on, so TLS ends here, with this Machine's own certificate.

1. Dial-back. A self-hosted Machine has no public port, so it asks the account for connections: GET
   /api/fleet/mcp-wait?wait=25 with its device token answers {conns: [id]}. For each, the Machine opens
   /api/fleet/mcp-stream/<id> (Upgrade: tm-mcp-stream/1); after 101 the AI's own TLS bytes follow, its hello first.
   A 401 there stops the loop: the token is gone (unpaired, or disconnected on the Account page).
2. TLS here. The Machine reads the hello (server name and ALPN), then answers with its certificate for that name, or,
   for a certificate authority checking it (ALPN acme-tls/1, RFC 8737), with the challenge certificate.
3. Only the public paths: /mcp, /.well-known/oauth-*, /oauth/token, /oauth/register, /oauth/revoke (ai_access
   PUBLIC_GET and PUBLIC_POST) go to the same handlers as on the dashboard (AiApp.ai_http), with no owner sign-in at
   all; anything else is 404. The authorization endpoint stays on the dashboard, behind the owner's own sign-in.
4. The certificate (ACME, RFC 8555, TLS-ALPN-01): Let's Encrypt, ZeroSSL when that fails (ZeroSSL needs an account
   bound to an email address: the owner's first one). Key and certificate stay next to the database (0600) and never
   leave the Machine; renewed with RENEW_DAYS left; gone on Unpair (drop).

Needs the `cryptography` package; without it Settings, AIs says so and nothing here starts."""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import hmac
import http.client
import io
import json
import logging
import re
import socket
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import ai_access
import onboarding

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
    from cryptography.x509.oid import NameOID
    AVAILABLE = True
except ImportError:  # Settings, AIs: "Install the cryptography package to use this address"
    AVAILABLE = False

LOG = logging.getLogger('personal-assistant')

CLOUD = 'https://app.themachine.computer'          # where mcp-wait and mcp-stream are
WAIT = 25                                          # seconds one mcp-wait may hold
STREAM_FIRST = 10                                  # seconds to open a stream once it is announced
IDLE = 60                                          # seconds a connection may sit between requests
REQUESTS = 100                                     # requests per connection
HEAD_MAX = 16384                                   # bytes of request line and headers
UPGRADE = 'tm-mcp-stream/1'
ALPN_ACME = 'acme-tls/1'
OID_ACME_IDENTIFIER = '1.3.6.1.5.5.7.1.31'         # RFC 8737: the challenge certificate's critical extension
CAS = (('letsencrypt', 'https://acme-v02.api.letsencrypt.org/directory'),
       ('zerossl', 'https://acme.zerossl.com/v2/DV90'))
ZEROSSL_EAB = 'https://api.zerossl.com/acme/eab-credentials-email'
RENEW_DAYS = 30
RETRY = 3600                                       # seconds before another certificate try after one failed
KEY_FILE, CERT_FILE, ACCOUNT_FILE = 'mcp-tls-key.pem', 'mcp-tls-cert.pem', 'acme-accounts.json'


class Refused(Exception):
    """The account refused this Machine's token (401): stop."""


class AcmeError(Exception):
    pass


def b64u(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def folder(config):
    return Path(config['database']).expanduser().parent


def drop(config):
    """Unpair: the certificate, its key and the CA accounts go."""
    for name in (KEY_FILE, CERT_FILE, ACCOUNT_FILE):
        (folder(config) / name).unlink(missing_ok=True)


# ------------------------------------------------------------------ the certificate on disk


def load_cert(config):
    """(certificate, chain pem) when there is one, else (None, None)."""
    path = folder(config) / CERT_FILE
    if not AVAILABLE or not path.exists() or not (folder(config) / KEY_FILE).exists():
        return None, None
    data = path.read_bytes()
    try:
        return x509.load_pem_x509_certificate(data), data
    except ValueError:
        return None, None


def names_of(cert):
    try:
        return cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return []


def needs_cert(config, host, now=None):
    """No certificate yet, one for another name, or RENEW_DAYS or fewer left."""
    cert, _ = load_cert(config)
    if cert is None or host not in names_of(cert):
        return True
    now = now or dt.datetime.now(dt.timezone.utc)
    return cert.not_valid_after_utc - now <= dt.timedelta(days=RENEW_DAYS)


def keep_cert(config, key, chain_pem):
    key_pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    onboarding.write_private(folder(config) / KEY_FILE, key_pem.decode())
    onboarding.write_private(folder(config) / CERT_FILE, chain_pem.decode() if isinstance(chain_pem, bytes) else chain_pem)


# ------------------------------------------------------------------ ACME (RFC 8555) with TLS-ALPN-01 (RFC 8737)


def new_key():
    return ec.generate_private_key(ec.SECP256R1())


def jwk(key):
    numbers = key.public_key().public_numbers()
    return {'crv': 'P-256', 'kty': 'EC', 'x': b64u(numbers.x.to_bytes(32, 'big')), 'y': b64u(numbers.y.to_bytes(32, 'big'))}


def thumbprint(key):
    return b64u(hashlib.sha256(json.dumps(jwk(key), sort_keys=True, separators=(',', ':')).encode()).digest())


def challenge_cert(host, key_authorization):
    """RFC 8737: a self-signed certificate for host with the critical acmeIdentifier extension holding the SHA-256 of
    the key authorization (DER OCTET STRING). (certificate, key)"""
    key = new_key()
    digest = hashlib.sha256(key_authorization.encode()).digest()
    now = dt.datetime.now(dt.timezone.utc)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host)])
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - dt.timedelta(minutes=5))
            .not_valid_after(now + dt.timedelta(days=1))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(host)]), critical=False)
            .add_extension(x509.UnrecognizedExtension(x509.ObjectIdentifier(OID_ACME_IDENTIFIER), b'\x04\x20' + digest), critical=True)
            .sign(key, hashes.SHA256()))
    return cert, key


class Acme:
    """One CA account: directory, nonces, signed requests (ES256, JWS with jwk until the account has its kid)."""

    def __init__(self, directory, key, kid=None, timeout=20):
        self.directory_url, self.key, self.kid, self.timeout = directory, key, kid, timeout
        self.dir, self.nonce = None, None

    def _open(self, method, url, data=None, headers=None):
        request = urllib.request.Request(url, data=data, method=method, headers=headers or {})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.status, response.headers, response.read()
        except urllib.error.HTTPError as error:
            with error:
                return error.code, error.headers, error.read()

    def directory(self):
        if self.dir is None:
            status, _, body = self._open('GET', self.directory_url)
            if status != 200:
                raise AcmeError(f'directory {status}')
            self.dir = json.loads(body)
        return self.dir

    def _nonce(self):
        if self.nonce:
            found, self.nonce = self.nonce, None
            return found
        _, headers, _ = self._open('HEAD', self.directory()['newNonce'])
        found = headers.get('Replay-Nonce')
        if not found:
            raise AcmeError('no nonce')
        return found

    def _sign(self, protected, payload):
        head = b64u(json.dumps(protected).encode())
        body = '' if payload is None else b64u(json.dumps(payload).encode())
        r, s = decode_dss_signature(self.key.sign(f'{head}.{body}'.encode(), ec.ECDSA(hashes.SHA256())))
        return {'protected': head, 'payload': body, 'signature': b64u(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}

    def post(self, url, payload, use_jwk=False):
        """A signed POST (payload None: POST-as-GET). (status, headers, json or bytes); one retry on badNonce."""
        for attempt in (0, 1):
            protected = {'alg': 'ES256', 'nonce': self._nonce(), 'url': url}
            if use_jwk or not self.kid:
                protected['jwk'] = jwk(self.key)
            else:
                protected['kid'] = self.kid
            status, headers, body = self._open('POST', url, json.dumps(self._sign(protected, payload)).encode(),
                                               {'Content-Type': 'application/jose+json'})
            self.nonce = headers.get('Replay-Nonce') or None
            kind = headers.get('Content-Type', '')
            found = json.loads(body or b'{}') if 'json' in kind else body
            if status == 400 and isinstance(found, dict) and found.get('type', '').endswith(':badNonce') and not attempt:
                continue
            if status >= 400:
                detail = found.get('detail') if isinstance(found, dict) else ''
                raise AcmeError(f'{status} {str(detail)[:200]}')
            return status, headers, found
        raise AcmeError('bad nonce')

    def account(self, eab=None):
        """newAccount (finds the existing one too). eab: (kid, hmac key b64url) for a CA that binds accounts."""
        url = self.directory()['newAccount']
        payload = {'termsOfServiceAgreed': True}
        if eab:
            protected = {'alg': 'HS256', 'kid': eab[0], 'url': url}
            head, body = b64u(json.dumps(protected).encode()), b64u(json.dumps(jwk(self.key)).encode())
            mac = hmac.new(base64.urlsafe_b64decode(eab[1] + '=' * (-len(eab[1]) % 4)), f'{head}.{body}'.encode(), hashlib.sha256).digest()
            payload['externalAccountBinding'] = {'protected': head, 'payload': body, 'signature': b64u(mac)}
        _, headers, _ = self.post(url, payload, use_jwk=True)
        self.kid = headers.get('Location')
        if not self.kid:
            raise AcmeError('no account')
        return self.kid

    def poll(self, url, done, wait, tries=30):
        for _ in range(tries):
            _, headers, found = self.post(url, None)
            if found.get('status') in done:
                return found
            if found.get('status') == 'invalid':
                problem = (found.get('error') or {}).get('detail') or next(
                    ((c.get('error') or {}).get('detail') for c in found.get('challenges', []) if c.get('error')), '')
                raise AcmeError('invalid ' + str(problem)[:200])
            try:
                pause = min(max(int(headers.get('Retry-After') or 2), 1), 30)
            except ValueError:
                pause = 2
            wait(pause)
        raise AcmeError('took too long')

    def certificate(self, host, challenges, wait=time.sleep):
        """An order for host, its TLS-ALPN-01 challenge answered through challenges (host -> context while it lasts),
        then finalize. (key, chain pem)"""
        _, headers, order = self.post(self.directory()['newOrder'], {'identifiers': [{'type': 'dns', 'value': host}]})
        order_url = headers.get('Location')
        for authz_url in order.get('authorizations', []):
            _, _, authz = self.post(authz_url, None)
            if authz.get('status') == 'valid':
                continue
            found = next((c for c in authz.get('challenges', []) if c.get('type') == 'tls-alpn-01'), None)
            if not found:
                raise AcmeError('no tls-alpn-01 challenge')
            cert, key = challenge_cert(host, found['token'] + '.' + thumbprint(self.key))
            challenges[host] = context(cert, key, ALPN_ACME)
            try:
                self.post(found['url'], {})
                self.poll(authz_url, ('valid',), wait)
            finally:
                challenges.pop(host, None)
        key = new_key()
        csr = (x509.CertificateSigningRequestBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host)]))
               .add_extension(x509.SubjectAlternativeName([x509.DNSName(host)]), critical=False).sign(key, hashes.SHA256()))
        self.post(order['finalize'], {'csr': b64u(csr.public_bytes(serialization.Encoding.DER))})
        order = self.poll(order_url, ('valid',), wait)
        _, _, chain = self.post(order['certificate'], None)
        if not isinstance(chain, bytes) or b'BEGIN CERTIFICATE' not in chain:
            raise AcmeError('no certificate')
        return key, chain


def zerossl_eab(email, timeout=20):
    """ZeroSSL binds ACME accounts to an email address: its API hands out the binding for one."""
    data = urllib.parse.urlencode({'email': email}).encode()
    with urllib.request.urlopen(urllib.request.Request(ZEROSSL_EAB, data=data, method='POST'), timeout=timeout) as response:
        found = json.loads(response.read() or b'{}')
    if not found.get('success') or not found.get('eab_kid') or not found.get('eab_hmac_key'):
        raise AcmeError('no ZeroSSL account')
    return found['eab_kid'], found['eab_hmac_key']


def accounts(config):
    path = folder(config) / ACCOUNT_FILE
    try:
        found = json.loads(path.read_text())
        return found if isinstance(found, dict) else {}
    except (OSError, ValueError):
        return {}


def obtain(config, host, challenges, email=None, cas=CAS, eab=zerossl_eab, wait=time.sleep):
    """A certificate for host from the first CA that gives one (Let's Encrypt, then ZeroSSL), kept 0600. Raises
    AcmeError when none did."""
    kept = accounts(config)
    last = None
    for name, directory in cas:
        try:
            saved = kept.get(name) or {}
            key = serialization.load_pem_private_key(saved['key'].encode(), None) if saved.get('key') else new_key()
            client = Acme(directory, key, saved.get('kid'))
            if not client.kid:
                binding = None
                if client.directory().get('meta', {}).get('externalAccountRequired'):
                    if not email:
                        raise AcmeError('needs an email address')
                    binding = eab(email)
                client.account(binding)
                kept[name] = {'key': key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                       serialization.NoEncryption()).decode(), 'kid': client.kid}
                onboarding.write_private(folder(config) / ACCOUNT_FILE, json.dumps(kept))
            cert_key, chain = client.certificate(host, challenges, wait)
            keep_cert(config, cert_key, chain)
            LOG.info('mcp certificate ca=%s', name)
            return name
        except (AcmeError, OSError, ValueError, KeyError) as error:
            LOG.warning('mcp certificate ca=%s error=%s', name, type(error).__name__)
            last = error
    raise AcmeError(str(last or 'no CA'))


# ------------------------------------------------------------------ TLS here


def context_files(certfile, keyfile, alpn):
    """A server context for one certificate chain and its key (files), offering only alpn."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(certfile, keyfile)
    ctx.set_alpn_protocols([alpn])
    return ctx


def context(cert, key, alpn):
    """The same for a certificate and key in memory (the challenge's, made for one check): load_cert_chain reads
    files only, so a private temporary file holds them for that moment."""
    import os
    import tempfile
    pem = cert.public_bytes(serialization.Encoding.PEM) + key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    fd, path = tempfile.mkstemp(prefix='tm-acme-', suffix='.pem')
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(pem)
        return context_files(path, path, alpn)
    finally:
        os.unlink(path)


def hello(data):
    """(server name, [alpn]) from a TLS ClientHello record; None while it is incomplete; ValueError when it is not one."""
    if len(data) < 5:
        return None
    if data[0] != 22:
        raise ValueError('not a TLS handshake')
    size = int.from_bytes(data[3:5], 'big')
    if len(data) < 5 + size:
        return None
    body = data[5:5 + size]
    if not body or body[0] != 1:
        raise ValueError('not a ClientHello')
    at = 4 + 2 + 32
    at += 1 + body[at]                                   # session id
    at += 2 + int.from_bytes(body[at:at + 2], 'big')     # cipher suites
    at += 1 + body[at]                                   # compression
    end = at + 2 + int.from_bytes(body[at:at + 2], 'big')
    at += 2
    name, alpn = None, []
    while at + 4 <= min(end, len(body)):
        kind, length = int.from_bytes(body[at:at + 2], 'big'), int.from_bytes(body[at + 2:at + 4], 'big')
        value = body[at + 4:at + 4 + length]
        if kind == 0 and len(value) > 5 and value[2] == 0:
            name = value[5:5 + int.from_bytes(value[3:5], 'big')].decode('ascii', 'replace').lower()
        elif kind == 16:
            i = 2
            while i < len(value):
                alpn.append(value[i + 1:i + 1 + value[i]].decode('ascii', 'replace'))
                i += 1 + value[i]
        at += 4 + length
    return name, alpn


class TLS:
    """TLS over a stream that already started: the bytes read so far go in first (MemoryBIO), then the socket."""

    def __init__(self, sock, ctx, first):
        self.sock, self.incoming, self.outgoing = sock, ssl.MemoryBIO(), ssl.MemoryBIO()
        self.incoming.write(first)
        self.obj = ctx.wrap_bio(self.incoming, self.outgoing, server_side=True)

    def _flush(self):
        data = self.outgoing.read()
        if data:
            self.sock.sendall(data)

    def _fill(self):
        data = self.sock.recv(65536)
        if data:
            self.incoming.write(data)
        else:
            self.incoming.write_eof()

    def _do(self, call):
        while True:
            try:
                found = call()
                self._flush()
                return found
            except ssl.SSLWantReadError:
                self._flush()
                self._fill()

    def handshake(self):
        self._do(self.obj.do_handshake)
        return self.obj.selected_alpn_protocol()

    def recv(self, size=65536):
        try:
            return self._do(lambda: self.obj.read(size))
        except (ssl.SSLZeroReturnError, ssl.SSLEOFError):
            return b''

    def sendall(self, data):
        self._do(lambda: self.obj.write(data))


def read_head(stream, buffer):
    """(request head bytes, rest) or (None, buffer) when the stream closed first."""
    while b'\r\n\r\n' not in buffer:
        if len(buffer) > HEAD_MAX:
            raise ValueError('head too big')
        data = stream.recv()
        if not data:
            return None, buffer
        buffer += data
    head, rest = buffer.split(b'\r\n\r\n', 1)
    return head, rest


def answer(stream, status, headers, data, close):
    reason = http.client.responses.get(status, '')
    lines = [f'HTTP/1.1 {status} {reason}'] + [f'{k}: {v}' for k, v in headers.items()]
    lines += [f'Content-Length: {len(data)}', 'X-Content-Type-Options: nosniff', 'Referrer-Policy: no-referrer',
              'Cache-Control: no-store' if 'Cache-Control' not in headers else '', 'Connection: ' + ('close' if close else 'keep-alive')]
    stream.sendall(('\r\n'.join(x for x in lines if x) + '\r\n\r\n').encode('latin-1') + data)


def allowed(method, path):
    return (method == 'GET' and path in ai_access.PUBLIC_GET) or (method == 'POST' and path in ai_access.PUBLIC_POST)


def serve_http(stream, handle):
    """HTTP/1.1 on the TLS stream, keep-alive, Content-Length bodies only. handle(method, path, headers, body) gives
    (status, headers, bytes) for the public paths; anything else is 404 here, before it reaches the App."""
    buffer = b''
    for _ in range(REQUESTS):
        head, buffer = read_head(stream, buffer)
        if head is None:
            return
        line, _, rest = head.partition(b'\r\n')
        parts = line.decode('latin-1').split(' ')
        if len(parts) != 3 or not parts[2].startswith('HTTP/1.'):
            return answer(stream, 400, {}, b'', True)
        method, target = parts[0], parts[1]
        headers = http.client.parse_headers(io.BytesIO(rest + b'\r\n\r\n'))
        close = (headers.get('Connection') or '').lower() == 'close' or parts[2] == 'HTTP/1.0'
        if headers.get('Transfer-Encoding'):
            return answer(stream, 411, {}, b'', True)
        try:
            length = int(headers.get('Content-Length') or 0)
        except ValueError:
            return answer(stream, 400, {}, b'', True)
        if not 0 <= length <= ai_access.BODY_MAX:
            return answer(stream, 413, {}, b'', True)
        while len(buffer) < length:
            data = stream.recv()
            if not data:
                return
            buffer += data
        body, buffer = buffer[:length], buffer[length:]
        path = urllib.parse.urlsplit(target).path
        if not allowed(method, path):
            answer(stream, 404, {'Content-Type': 'application/json'}, b'{"error":"Not found"}', close)
        else:
            status, out, data = handle(method, path, headers, body)
            answer(stream, status, out, data, close)
        if close:
            return


def serve(sock, first, host, handle, challenges, cert_context, timeout=IDLE):
    """One AI connection on sock (its first bytes in first): TLS here, then HTTP. Only host is answered."""
    sock.settimeout(STREAM_FIRST)
    data = first
    while (found := hello(data)) is None:
        more = sock.recv(65536)
        if not more:
            return
        data += more
    name, alpn = found
    if name != host:
        return  # not this Machine's name: no certificate for it
    if ALPN_ACME in alpn:
        ctx = challenges.get(host)
        if ctx:
            try:
                TLS(sock, ctx, data).handshake()  # the CA looks at the certificate only, then hangs up
            except (OSError, ssl.SSLError):
                pass
        return
    ctx = cert_context()
    if ctx is None:
        return
    sock.settimeout(timeout)
    stream = TLS(sock, ctx, data)
    stream.handshake()
    serve_http(stream, handle)


# ------------------------------------------------------------------ the loop


def _request(url, token, timeout):
    request = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read() or b'{}')
    except urllib.error.HTTPError as error:
        with error:
            if error.code in (401, 403):
                raise Refused(str(error.code)) from None
            raise OSError(f'mcp-wait {error.code}') from None


def open_stream(base, token, conn_id, timeout=STREAM_FIRST):
    """The announced connection: (socket, bytes already read after the 101). Raises Refused on 401."""
    link = urllib.parse.urlsplit(base)
    port = link.port or (443 if link.scheme == 'https' else 80)
    sock = socket.create_connection((link.hostname, port), timeout=timeout)
    try:
        if link.scheme == 'https':
            sock = ssl.create_default_context().wrap_socket(sock, server_hostname=link.hostname)
        request = (f'GET /api/fleet/mcp-stream/{conn_id} HTTP/1.1\r\nHost: {link.hostname}\r\n'
                   f'Authorization: Bearer {token}\r\nConnection: Upgrade\r\nUpgrade: {UPGRADE}\r\n\r\n')
        sock.sendall(request.encode())
        buffer = b''
        while b'\r\n\r\n' not in buffer:
            data = sock.recv(4096)
            if not data or len(buffer) > HEAD_MAX:
                raise OSError('stream not opened')
            buffer += data
        head, rest = buffer.split(b'\r\n\r\n', 1)
        status = head.split(b' ', 2)[1] if head.count(b' ') else b''
        if status in (b'401', b'403'):
            raise Refused(status.decode())
        if status != b'101':
            raise OSError('stream ' + status.decode('latin-1')[:3])
        return sock, rest
    except BaseException:
        sock.close()
        raise


class Reach:
    """The dial-back loop and the certificate for one self-hosted Machine. app gives: name() (the account's name, or
    None), token() (the device token, or None), handle(method, path, headers, body, host), email() (for ZeroSSL)."""

    def __init__(self, config, app, base=CLOUD, cas=CAS, eab=zerossl_eab, wait=None):
        self.config, self.app, self.base, self.cas, self.eab = config, app, base, cas, eab
        self.challenges, self.state, self.failed_at = {}, 'getting', 0.0
        self.wait = wait
        self.cert_lock, self.ctx, self.ctx_for = threading.Lock(), None, None

    def host(self):
        name = self.app.name()
        return f'{name}.mcp.themachine.computer' if name else None

    def cert_context(self):
        if load_cert(self.config)[0] is None:
            return None
        stamp = (folder(self.config) / CERT_FILE).stat().st_mtime
        if self.ctx_for != stamp:
            self.ctx = context_files(folder(self.config) / CERT_FILE, folder(self.config) / KEY_FILE, 'http/1.1')
            self.ctx_for = stamp
        return self.ctx

    def certify(self, host):
        """Gets or renews the certificate in the background, at most one at a time, RETRY after a failure."""
        if not needs_cert(self.config, host):
            self.state = 'ready'
            return
        if self.failed_at and time.monotonic() - self.failed_at < RETRY:
            return
        if not self.cert_lock.acquire(blocking=False):
            return

        def work():
            try:
                obtain(self.config, host, self.challenges, self.app.email(), self.cas, self.eab, **({'wait': self.wait} if self.wait else {}))
                self.state, self.failed_at = 'ready', 0.0
            except Exception as error:  # noqa: BLE001 - tried again after RETRY
                LOG.warning('mcp certificate failed error=%s', type(error).__name__)
                self.state, self.failed_at = 'failed', time.monotonic()
            finally:
                self.cert_lock.release()
        if load_cert(self.config)[0] is None:
            self.state = 'getting'
        threading.Thread(target=work, name='mcp-cert', daemon=True).start()

    def connection(self, conn_id, host, token):
        try:
            sock, first = open_stream(self.base, token, conn_id)
        except (Refused, OSError) as error:
            LOG.info('mcp stream not opened error=%s', type(error).__name__)
            return
        try:
            serve(sock, first, host, lambda m, p, h, b: self.app.handle(m, p, h, b, host), self.challenges, self.cert_context)
        except (OSError, ValueError, ssl.SSLError) as error:
            LOG.info('mcp connection ended error=%s', type(error).__name__)
        finally:
            try:
                sock.close()
            except OSError:
                pass

    def run(self, stop):
        """Until stop, or the account refuses the token. Waits a minute while there is no name yet."""
        away = 0
        while not stop.is_set():
            host, token = self.host(), self.app.token()
            if not host or not token:
                stop.wait(60)
                continue
            self.certify(host)
            try:
                found = _request(f'{self.base}/api/fleet/mcp-wait?wait={WAIT}', token, WAIT + 15)
                away = 0
            except Refused:
                LOG.warning('mcp reach stopped: the account refused this Machine')
                self.state = 'refused'
                return
            except (OSError, ValueError) as error:
                away = min(away + 1, 6)
                LOG.info('mcp wait away error=%s', type(error).__name__)
                stop.wait(5 * 2 ** away)
                continue
            for conn_id in (found.get('conns') or [])[:20]:
                if isinstance(conn_id, str) and re.fullmatch(r'[0-9a-f]{16,64}', conn_id):
                    threading.Thread(target=self.connection, args=(conn_id, host, token), name='mcp-conn', daemon=True).start()

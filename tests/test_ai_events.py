"""MCP Events for connected AIs (ai_events.py, docs/ai-connections.md, Events): events/list, subscribe and unsubscribe
on the MCP endpoint, the owner's switch per event and connection, the callback's checks (https, public addresses only,
the verification handshake), signed webhook delivery to a fake subscriber over real HTTPS, retries, the rate limit,
loops, and subscriptions ending with their connection. Security-critical: nothing reaches a private address, nothing is
sent for an event the owner didn't turn on, and nothing beyond what the connection may already read."""
import base64
import datetime as dt
import hashlib
import hmac
import http.server
import json
import secrets
import ssl
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import ai_access
import ai_events
import meeting_prep
import timeutil
from test_ai_access import Base

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    HAVE_CRYPTO = True
except ImportError:  # pragma: no cover - CI has it
    HAVE_CRYPTO = False

HOOK = 'hooks.example.test'


def whsec():
    return 'whsec_' + base64.b64encode(secrets.token_bytes(32)).decode()


def signed_ok(secret, headers, body):
    """Standard Webhooks, checked on its own: any v1 signature over id.timestamp.body with the secret."""
    key = base64.b64decode(secret[6:])
    want = base64.b64encode(hmac.new(key, f"{headers['webhook-id']}.{headers['webhook-timestamp']}.".encode() + body, hashlib.sha256).digest()).decode()
    return any(hmac.compare_digest(s.split(',', 1)[1], want) for s in headers['webhook-signature'].split() if s.startswith('v1,'))


def certificates(folder):
    """A test CA and a certificate for HOOK it signed: (the CA's PEM, the cert file, the key file)."""
    now = dt.datetime.now(dt.timezone.utc)
    ca_key, key = ec.generate_private_key(ec.SECP256R1()), ec.generate_private_key(ec.SECP256R1())
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Events test CA')])
    ca = (x509.CertificateBuilder().subject_name(ca_name).issuer_name(ca_name).public_key(ca_key.public_key())
          .serial_number(x509.random_serial_number()).not_valid_before(now - dt.timedelta(days=1)).not_valid_after(now + dt.timedelta(days=2))
          .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
          .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
          .add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()), critical=False)
          .sign(ca_key, hashes.SHA256()))
    leaf = (x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, HOOK)])).issuer_name(ca_name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - dt.timedelta(days=1)).not_valid_after(now + dt.timedelta(days=2))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(HOOK)]), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
            .sign(ca_key, hashes.SHA256()))
    cert, keyfile = Path(folder) / 'hook.pem', Path(folder) / 'hook.key'
    cert.write_bytes(leaf.public_bytes(serialization.Encoding.PEM))
    keyfile.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
    return ca.public_bytes(serialization.Encoding.PEM).decode(), cert, keyfile


class Subscriber:
    """A fake subscriber over HTTPS on loopback: echoes challenges, keeps what it was sent (checked signatures), and
    answers with the statuses queued in `answers` (200 once they run out)."""

    def __init__(self, secret_of):
        self.got, self.answers, self.secret_of, self.echo = [], [], secret_of, True
        self.temp = tempfile.TemporaryDirectory()
        self.ca, cert, key = certificates(self.temp.name)
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = self.rfile.read(int(self.headers['Content-Length']))
                headers = {k.lower(): v for k, v in self.headers.items()}
                ok = signed_ok(outer.secret_of(headers['x-mcp-subscription-id']), headers, body)
                message = json.loads(body)
                outer.got.append({'path': self.path, 'headers': headers, 'body': message, 'raw': body, 'signed': ok})
                status = outer.answers.pop(0) if outer.answers else 200
                reply = json.dumps({'challenge': message['challenge'] if outer.echo else 'wrong'}).encode() \
                    if message.get('type') == 'verification' else b'{}'
                self.send_response(status)
                if status in (301, 302):
                    self.send_header('Location', 'https://127.0.0.1/elsewhere')
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(reply)))
                self.end_headers()
                self.wfile.write(reply)

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def url(self, name='cb1'):
        return f'https://{HOOK}:{self.port}/mcp-events/{name}'

    def transport(self):
        """The Machine's own Transport, told that HOOK is this loopback server (and loopback allowed, for this test only)."""
        return ai_events.Transport(resolve=lambda host, port: ['127.0.0.1'] if host == HOOK else [],
                                   allow=lambda address: address == '127.0.0.1', context=ssl.create_default_context(cadata=self.ca))

    def deliveries(self):
        return [g for g in self.got if g['body'].get('type') != 'verification']

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.temp.cleanup()


class Events(Base):
    def setUp(self):
        super().setUp()
        self.secrets = {}

    def rpc(self, bearer, method, params=None):
        status, _, reply = self.call(bearer, method=method, params=params or {})
        self.assertEqual(status, 200, reply)
        return reply

    def conn_id(self):
        with self.db() as db:
            return db.execute('SELECT id FROM ai_connections ORDER BY created_at DESC LIMIT 1').fetchone()['id']

    def turn_on(self, *names):
        self.app.ai_dashboard_action('ai_change', {'id': self.conn_id(), 'events': list(names)}, True)

    def subscribe(self, bearer, url, name='todo.created', arguments=None, secret=None, **more):
        secret = self.pending = secret or whsec()  # the subscriber checks the challenge with it, before the id is known
        reply = self.rpc(bearer, 'events/subscribe', {'name': name, 'arguments': arguments or {},
                                                      'delivery': {'mode': 'webhook', 'url': url, 'secret': secret}, 'cursor': None, **more})
        if 'result' in reply:
            self.secrets[reply['result']['id']] = secret
        return reply

    def todo(self, title='Answer the client', body='They asked about the price.', account='w', event=1):
        card = self.store.suggest(f'{account}:t{secrets.token_hex(3)}', title, body, [event], when='now', work=account == 'w')['id']
        with self.db() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL WHERE id=?', (card,))
        return card


class Protocol(Events):
    def test_initialize_says_events_and_the_list_has_each_with_its_schemas(self):
        _, tokens = self.signed_in()
        init = self.rpc(tokens['access_token'], 'initialize', {'protocolVersion': '2025-06-18'})
        self.assertEqual(init['result']['capabilities']['events'], {})
        listed = self.rpc(tokens['access_token'], 'events/list')['result']['events']
        self.assertEqual([e['name'] for e in listed], ['todo.created', 'meeting.briefing_ready', 'promise.due'])
        for event in listed:
            self.assertEqual(event['delivery'], ['webhook'])
            self.assertFalse(event['inputSchema']['additionalProperties'])
            self.assertFalse(event['payloadSchema']['additionalProperties'])
            self.assertIn('Off until the owner turns it on', event['description'])

    def test_without_a_transport_nothing_about_events_is_there(self):
        _, tokens = self.signed_in()
        with self.db() as db:
            connection, why = ai_access.bearer(db, 'Bearer ' + tokens['access_token'])
        reply = ai_access.handle(self.store.connect, {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}},
                                 connection, why, self.app.ai_tool, self.app.ai_limiter)
        self.assertNotIn('events', reply['result']['capabilities'])
        reply = ai_access.handle(self.store.connect, {'jsonrpc': '2.0', 'id': 2, 'method': 'events/list', 'params': {}},
                                 connection, why, self.app.ai_tool, self.app.ai_limiter)
        self.assertEqual(reply['error']['code'], -32601)

    def test_an_event_the_owner_did_not_turn_on_is_refused_and_logged(self):
        _, tokens = self.signed_in()
        reply = self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb')
        self.assertEqual(reply['error']['code'], ai_events.FORBIDDEN)
        self.assertIn('Settings, Apps, Connected AIs', reply['error']['message'])
        self.assertIn(('subscribe', 'refused', 'New to-dos: turned off'), [(r['tool'], r['outcome'], r['detail']) for r in self.activity()])
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_event_subs').fetchone()[0], 0)

    def test_the_switches_are_off_to_start_and_show_in_settings(self):
        self.signed_in()
        view = self.app.ai_dashboard_action('ai_connections', {}, True)
        self.assertEqual(view['connections'][0]['events'], [])
        self.turn_on('promise.due', 'todo.created')
        view = self.app.ai_dashboard_action('ai_connections', {}, True)
        self.assertEqual(view['connections'][0]['events'], ['todo.created', 'promise.due'])
        self.assertIn('Events: New to-dos, Promises due', [r['detail'] for r in self.activity()])
        with self.assertRaises(ValueError):
            self.app.ai_dashboard_action('ai_change', {'id': self.conn_id(), 'events': ['mail.sent']}, True)
        with self.assertRaises(Exception):
            self.app.ai_dashboard_action('ai_change', {'id': self.conn_id(), 'events': ['todo.created']}, False)

    def test_bad_callbacks_secrets_and_arguments_are_refused_before_anything_goes_out(self):
        _, tokens = self.signed_in()
        self.turn_on('todo.created')
        for url in ('http://hooks.example.test/cb', 'https://user:pw@hooks.example.test/cb', 'https://hooks.example.test/cb#x',
                    'https:///cb', 'https://hooks.example.test:99999/cb', 'https://hooks.example.test/' + 'x' * 2100):
            with self.subTest(url=url[:60]):
                self.assertEqual(self.subscribe(tokens['access_token'], url)['error']['code'], -32602)
        for secret in ('nope', 'whsec_!!!', 'whsec_' + base64.b64encode(b'short').decode(), 'whsec_' + base64.b64encode(b'x' * 65).decode()):
            with self.subTest(secret=secret[:12]):
                self.assertEqual(self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb', secret=secret)['error']['code'], -32602)
        self.assertEqual(self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb', arguments={'channel': 'x'})['error']['code'], -32602)
        self.assertEqual(self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb', name='mail.sent')['error']['code'], ai_events.NOT_FOUND)

    def test_a_connection_that_is_off_or_read_only_for_one_area_cannot_widen_it(self):
        _, tokens = self.signed_in(area='work')
        self.turn_on('todo.created')
        reply = self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb', arguments={'area': 'personal'})
        self.assertEqual(reply['error']['code'], ai_events.FORBIDDEN)
        self.app.ai_dashboard_action('ai_change', {'id': self.conn_id(), 'level': 'off'}, True)
        self.assertEqual(self.subscribe(tokens['access_token'], 'https://hooks.example.test/cb')['error']['code'], ai_events.FORBIDDEN)


class Addresses(unittest.TestCase):
    def test_only_public_addresses_are_reached(self):
        for address in ('127.0.0.1', '10.1.2.3', '172.16.0.1', '192.168.1.1', '169.254.169.254', '100.64.0.1', '0.0.0.0',
                        '224.0.0.1', '255.255.255.255', '198.18.0.1', '192.0.2.1', '::1', '::', 'fe80::1', 'fc00::1', 'fd12::1',
                        '::ffff:127.0.0.1', '::ffff:169.254.169.254', '2002:7f00:1::', '2001:0:4136:e378::1', '64:ff9b::7f00:1',
                        '2001:db8::1', 'ff02::1', 'not an address'):
            with self.subTest(address=address):
                self.assertFalse(ai_events.public(address))
        for address in ('8.8.8.8', '1.1.1.1', '2606:4700:4700::1111', '2a00:1450:4007:80e::200e'):
            with self.subTest(address=address):
                self.assertTrue(ai_events.public(address))

    def test_a_name_with_any_private_address_is_never_connected_to(self):
        for found in (['127.0.0.1'], ['8.8.8.8', '10.0.0.1'], ['169.254.169.254'], []):
            with self.subTest(found=found), patch('socket.create_connection') as dial:
                transport = ai_events.Transport(resolve=lambda host, port, found=found: found)
                with self.assertRaises(ai_events.Failed) as caught:
                    transport.post('https://hooks.example.test/cb', b'{}', {})
                self.assertEqual(caught.exception.reason, 'connection_refused')
                dial.assert_not_called()

    def test_the_signature_is_standard_webhooks(self):
        secret = 'whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw'  # gitleaks:allow - the Standard Webhooks spec's public example key
        header = ai_events.signature([secret], 'msg_p5jXN8AQM9LWM0D4loKWxJek', '1614265330', b'{"test": 2432232314}')
        self.assertEqual(header, 'v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=')  # the Standard Webhooks spec's own example


@unittest.skipUnless(HAVE_CRYPTO, 'needs the cryptography package')
class Delivery(Events):
    def setUp(self):
        super().setUp()
        self.hook = Subscriber(lambda sid: self.secrets.get(sid, self.pending))
        self.addCleanup(self.hook.close)
        self.app.ai_transport = self.hook.transport()

    def ready(self, area='both', names=('todo.created',), level='read', **sub):
        client, tokens = self.signed_in(level=level, area=area)
        self.turn_on(*names)
        reply = self.subscribe(tokens['access_token'], self.hook.url(), **sub)
        self.assertIn('result', reply, reply)
        return tokens, reply['result']

    def round(self):
        return self.app.ai_events_round(self.app.ai_transport)

    def test_a_new_todo_reaches_the_subscriber_once_signed_and_verified_first(self):
        tokens, sub = self.ready()
        self.assertTrue(sub['id'].startswith('sub_'))
        self.assertIsNone(sub['cursor'])
        self.assertFalse(sub['truncated'])
        verification = self.hook.got[0]
        self.assertEqual(verification['body']['type'], 'verification')
        self.assertTrue(verification['signed'])
        self.assertTrue(verification['headers']['webhook-id'].startswith('msg_verification_'))
        self.assertEqual(self.round(), {}, 'what was there before the subscription never fires')
        card = self.todo('Send the quote', 'Sam asked for the quote by Friday.')
        self.assertEqual(self.round(), {'sent': 1})
        self.assertEqual(self.round(), {}, 'once')
        got = self.hook.deliveries()
        self.assertEqual(len(got), 1)
        event, headers = got[0]['body'], got[0]['headers']
        self.assertTrue(got[0]['signed'])
        self.assertEqual(headers['webhook-id'], event['eventId'])
        self.assertEqual(headers['x-mcp-subscription-id'], sub['id'])
        self.assertEqual(headers['content-type'], 'application/json')
        self.assertEqual(event['name'], 'todo.created')
        self.assertIsNone(event['cursor'])
        self.assertTrue(event['timestamp'].endswith('Z'))
        self.assertEqual(set(event['data']), {'todo_id', 'title', 'area', 'why', 'link'})
        self.assertEqual(event['data']['todo_id'], card)
        self.assertEqual(event['data']['area'], 'work')
        self.assertIn('<untrusted source="messages">', event['data']['why'], 'text from others is marked, as the tools mark it')
        self.assertTrue(event['data']['why'].endswith('</untrusted>'))
        self.assertLessEqual(len(got[0]['raw']), ai_events.BODY_MAX)
        # the same text the read tool gives this connection
        _, read = self.tool(tokens['access_token'], 'get_todo', id=card)
        self.assertEqual(read['title'], event['data']['title'])
        lines = [(r['tool'], r['outcome'], r['detail']) for r in self.activity()]
        self.assertIn(('subscribe', 'ok', 'New to-dos'), lines)
        self.assertIn(('event', 'ok', 'New to-dos'), lines)

    def test_subscribing_again_is_the_same_subscription_without_a_second_challenge(self):
        tokens, sub = self.ready()
        again = self.subscribe(tokens['access_token'], self.hook.url(), secret=self.secrets[sub['id']])['result']
        self.assertEqual(again['id'], sub['id'])
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_event_subs').fetchone()[0], 1)
        self.assertEqual(len(self.hook.got), 1, 'verification is cached per connection and url')
        reordered = self.subscribe(tokens['access_token'], self.hook.url(), arguments={'area': 'work'})['result']
        self.assertNotEqual(reordered['id'], sub['id'])

    def test_a_new_secret_on_refresh_signs_next_to_the_old_one_for_a_while(self):
        tokens, sub = self.ready()
        old = self.secrets[sub['id']]
        self.subscribe(tokens['access_token'], self.hook.url())
        new = self.secrets[sub['id']]
        self.todo()
        self.round()
        got = self.hook.deliveries()[0]
        self.assertEqual(len(got['headers']['webhook-signature'].split()), 2)
        for secret in (old, new):
            self.assertTrue(signed_ok(secret, got['headers'], got['raw']))

    def test_a_callback_that_does_not_echo_or_redirects_is_refused(self):
        client, tokens = self.signed_in()
        self.turn_on('todo.created')
        self.hook.echo = False
        reply = self.subscribe(tokens['access_token'], self.hook.url('a'))
        self.assertEqual(reply['error']['code'], ai_events.CALLBACK)
        self.assertEqual(reply['error']['data'], {'reason': 'challenge_failed'})
        self.hook.echo = True
        self.hook.answers = [302]
        reply = self.subscribe(tokens['access_token'], self.hook.url('b'))
        self.assertEqual(reply['error']['data'], {'reason': 'http_4xx'})
        self.assertEqual([g['path'] for g in self.hook.got], ['/mcp-events/a', '/mcp-events/b'], 'the redirect was not followed')
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_event_subs').fetchone()[0], 0)

    def test_an_ais_own_todo_and_one_outside_its_area_never_fire(self):
        tokens, _ = self.ready(area='work', level='draft')
        made, _ = self.tool(tokens['access_token'], 'create_todo', text='Follow up with the client next week', area='work')
        self.assertFalse(made)
        self.todo('Book the dentist', 'For next week.', account='p', event=2)
        self.assertEqual(self.round(), {})
        self.assertEqual(self.hook.deliveries(), [])

    def test_transient_failures_retry_with_backoff_then_give_up(self):
        self.ready()
        self.todo()
        self.hook.answers = [500] * ai_events.ATTEMPTS
        self.assertEqual(self.round(), {'retry': 1})
        with self.db() as db:
            row = db.execute('SELECT * FROM ai_event_outbox').fetchone()
        self.assertEqual((row['state'], row['attempts']), ('wait', 1))
        self.assertGreater(row['next_at'], ai_access.stamp())
        ids = set()
        for attempt in range(2, ai_events.ATTEMPTS + 1):
            with self.db() as db:
                db.execute("UPDATE ai_event_outbox SET next_at='2000-01-01T00:00:00+00:00'")
            self.round()
            ids |= {g['headers']['webhook-id'] for g in self.hook.deliveries()}
        with self.db() as db:
            row = db.execute('SELECT * FROM ai_event_outbox').fetchone()
        self.assertEqual((row['state'], row['attempts']), ('failed', ai_events.ATTEMPTS))
        self.assertEqual(len(ids), 1, 'the same event id on every try')
        self.assertEqual(len(self.hook.deliveries()), ai_events.ATTEMPTS)
        self.assertIn('error', [r['outcome'] for r in self.activity() if r['tool'] == 'event'])

    def test_410_ends_the_subscription_and_413_is_never_retried(self):
        self.ready()
        self.todo()
        self.hook.answers = [413]
        self.assertEqual(self.round(), {'failed': 1})
        self.todo('Second one')
        self.hook.answers = [410]
        self.assertEqual(self.round(), {'gone': 1})
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_event_subs').fetchone()[0], 0)
        self.assertIn(('unsubscribe', 'ok'), [(r['tool'], r['outcome']) for r in self.activity()])

    def test_deliveries_are_limited_per_connection_and_the_rest_wait(self):
        self.ready()
        for n in range(3):
            self.todo(f'To-do {n}')
        with patch.object(ai_events, 'PER_HOUR', 2):
            self.assertEqual(self.round(), {'sent': 2, 'held': 1})
        self.assertEqual(len(self.hook.deliveries()), 2)

    def test_old_events_are_dropped_not_sent_late(self):
        self.ready()
        self.todo()
        with self.db() as db:
            ai_events.collect(self.app, db, {r['id']: dict(r) for r in db.execute('SELECT * FROM ai_connections')})
            db.execute("UPDATE ai_event_outbox SET at='2000-01-01T00:00:00+00:00'")
        self.assertEqual(self.round(), {'dropped': 1})
        self.assertEqual(self.hook.deliveries(), [])

    def test_subscriptions_end_with_the_switch_the_connection_and_its_end(self):
        tokens, sub = self.ready(names=('todo.created', 'promise.due'))
        self.subscribe(tokens['access_token'], self.hook.url(), name='promise.due')
        cid = self.conn_id()
        with self.db() as db:
            self.assertEqual(ai_events.watching(db, cid), ['promise.due', 'todo.created'])
        self.turn_on('promise.due')
        with self.db() as db:
            self.assertEqual(ai_events.watching(db, cid), ['promise.due'])
        self.app.ai_dashboard_action('ai_off', {'id': cid}, True)
        with self.db() as db:
            self.assertEqual(ai_events.watching(db, cid), [])
            self.assertEqual(db.execute('SELECT count(*) FROM ai_event_verified').fetchone()[0], 0)

    def test_removing_the_connection_ends_them_and_a_grant_never_outlasts_it(self):
        tokens, sub = self.ready()
        with self.db() as db:
            ends = db.execute('SELECT expires_at FROM ai_connections').fetchone()['expires_at']
        asked = self.subscribe(tokens['access_token'], self.hook.url(), ttlMs=400 * 24 * 3600 * 1000)['result']
        self.assertLessEqual(asked['refreshBefore'].replace('Z', '+00:00'), ends)
        self.app.ai_dashboard_action('ai_change', {'id': self.conn_id(), 'expiry': '1d'}, True)
        short = self.subscribe(tokens['access_token'], self.hook.url(), ttlMs=None)['result']
        self.assertIsNotNone(short['refreshBefore'], 'no expiry is never granted')
        self.app.ai_dashboard_action('ai_remove', {'id': self.conn_id()}, True)
        with self.db() as db:
            for table in ('ai_event_subs', 'ai_event_outbox', 'ai_event_seen'):
                self.assertEqual(db.execute(f'SELECT count(*) FROM {table}').fetchone()[0], 0, table)

    def test_an_expired_connection_gets_nothing(self):
        self.ready()
        self.todo()
        with self.db() as db:
            db.execute("UPDATE ai_connections SET expires_at='2000-01-01T00:00:00+00:00'")
        self.round()
        self.assertEqual(self.hook.deliveries(), [])

    def test_unsubscribe_stops_it_and_is_idempotent(self):
        tokens, sub = self.ready()
        params = {'name': 'todo.created', 'arguments': {}, 'delivery': {'mode': 'webhook', 'url': self.hook.url()}}
        self.assertEqual(self.rpc(tokens['access_token'], 'events/unsubscribe', params)['result'], {})
        self.assertEqual(self.rpc(tokens['access_token'], 'events/unsubscribe', params)['result'], {})
        self.todo()
        self.assertEqual(self.round(), {})
        self.assertEqual(['ok'], [r['outcome'] for r in self.activity() if r['tool'] == 'unsubscribe'])

    def test_a_promise_due_tomorrow_fires_from_the_morning_before(self):
        self.ready(names=('promise.due',), name='promise.due')
        local = dt.datetime.now(timeutil.local_tz()).date()
        stamp = timeutil.now()
        with self.db() as db:
            for what, due in (('Send the signed contract', local + dt.timedelta(days=1)), ('Later', local + dt.timedelta(days=3))):
                db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) "
                           "VALUES('mine','Sam',?,?,?,1,'w','open',?,?)", (what, due.isoformat(), stamp, stamp, stamp))
        with patch.dict(timeutil.WORK_HOURS, {'morning': '00:00'}):  # the morning before is past at any hour of the test
            self.assertEqual(self.round(), {'sent': 1})
            self.assertEqual(self.round(), {})
        promise = self.hook.deliveries()[0]['body']
        self.assertEqual(promise['name'], 'promise.due')
        self.assertEqual(promise['data']['due'], (local + dt.timedelta(days=1)).isoformat())
        self.assertEqual(promise['data']['what'], '<untrusted source="messages">Send the signed contract</untrusted>')

    def test_a_meeting_briefing_fires_once_the_meeting_is_a_day_away(self):
        self.ready(names=('meeting.briefing_ready',), name='meeting.briefing_ready')
        card = self.todo('Briefing: call with the client', 'Who: Sam')
        starts = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=20)).isoformat(timespec='seconds')
        far = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=4)).isoformat(timespec='seconds')
        other = self.todo('Briefing: later meeting', 'Who: Sam')
        with self.db() as db:
            db.execute(meeting_prep.SCHEMA)  # made with the first briefing (meeting_prep.py)
            for key, todo, at in (('m1', card, starts), ('m2', other, far)):
                db.execute("INSERT INTO meeting_preps(dedupe_key,event_id,suggestion_id,verdict,starts_at,created_at) VALUES(?,1,?,'made',?,?)",
                           (key, todo, at, ai_access.stamp()))
        self.assertEqual(self.round(), {'sent': 1})
        data = self.hook.deliveries()[0]['body']['data']
        self.assertEqual(data['todo_id'], card)
        self.assertTrue(data['starts_at'].endswith('Z'))


if __name__ == '__main__':
    unittest.main()

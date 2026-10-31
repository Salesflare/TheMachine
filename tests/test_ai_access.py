"""Connected AIs (docs/ai-connections.md): OAuth 2.1 with dynamic registration and PKCE, per-connection keys, the MCP
endpoint, and what each connection may do. Security-critical: PKCE, code and refresh reuse, token and connection
expiry, the level checked at every call, refused calls logged, secrets hashed at rest, the owner's sign-in and the
service's token never counting on these paths, areas respected, and nothing ever sent."""
import base64
import datetime as dt
import hashlib
import http.client
import importlib.util
import json
import secrets
import tempfile
import threading
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch

import ai_access

spec = importlib.util.spec_from_file_location('ai_access_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

TOKEN = 'test-token'
HOST = 'machine.example:8443'
ISSUER = 'https://' + HOST
OWNER = {'Host': HOST, 'Tailscale-User-Login': 'owner@example.com'}
CLAUDE = 'https://claude.ai/api/mcp/auth_callback'
ACCOUNTS = [{'id': 'w', 'boundary': 'work:acme.example', 'service': 'gmail', 'transport': 'gog', 'email': 'pat@acme.example'},
            {'id': 'p', 'boundary': 'personal:pat@home.example', 'service': 'gmail', 'transport': 'gog', 'email': 'pat@home.example'}]


def pkce():
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    return verifier, challenge


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        for account in ('w', 'p'):
            self.store.commit_page(account, {}, [{'account_id': account, 'source_id': account + '1', 'kind': 'gmail.message',
                                                  'occurred_at': a.now(), 'title': 'Contract ' + account, 'body': 'Body',
                                                  'metadata': {'from': 'Sam <sam@client.example>'}, 'deleted': False}])
        self.work_card = self.store.suggest('w:task', 'Send the contract', 'Sam asked for it.', [1], when='now', work=True)['id']
        self.home_card = self.store.suggest('p:task', 'Book the dentist', 'For next week.', [2], when='now')['id']
        with self.db() as db:  # on the owner's screen now, not held for working hours
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = self.store, TOKEN, threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.ai_limiter = ai_access.Limiter()
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'tailscale_owner': 'owner@example.com',
                           'dashboard_host': HOST, 'port': 0, 'http_timeout': 2}

    def db(self):
        return self.store.connect()

    # ---- helpers at the App level (no HTTP)

    def register(self, uris=(CLAUDE,), **extra):
        status, _, data = self.app.ai_http('POST', '/oauth/register', {}, json.dumps({'redirect_uris': list(uris), 'client_name': 'Claude', **extra}).encode(), HOST)
        return status, json.loads(data)

    def connect(self, level='read', area='both', expiry='30d', uri=CLAUDE):
        _, client = self.register((uri,))
        verifier, challenge = pkce()
        form = {'client_id': client['client_id'], 'redirect_uri': uri, 'state': 'st', 'code_challenge': challenge,
                'scope': 'read', 'level': level, 'area': area, 'expiry': expiry, 'choice': 'connect'}
        back = self.app.ai_consent_post(form)
        code = urllib.parse.parse_qs(urllib.parse.urlsplit(back).query)['code'][0]
        return client, verifier, code, back

    def token(self, form, headers=None):
        status, _, data = self.app.ai_http('POST', '/oauth/token', headers or {}, urllib.parse.urlencode(form).encode(), HOST)
        return status, json.loads(data)

    def signed_in(self, level='read', area='both', expiry='30d'):
        client, verifier, code, _ = self.connect(level, area, expiry)
        status, tokens = self.token({'grant_type': 'authorization_code', 'code': code, 'redirect_uri': CLAUDE,
                                     'client_id': client['client_id'], 'code_verifier': verifier})
        self.assertEqual(status, 200, tokens)
        return client, tokens

    def call(self, bearer, method='tools/call', params=None, ident=1):
        message = {'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params or {}}
        status, headers, data = self.app.ai_http('POST', '/mcp', {'Authorization': 'Bearer ' + bearer} if bearer else {},
                                                 json.dumps(message).encode(), HOST)
        return status, headers, (json.loads(data) if data else None)

    def tool(self, bearer, name, **args):
        status, _, reply = self.call(bearer, params={'name': name, 'arguments': args})
        self.assertEqual(status, 200, reply)
        result = reply['result']
        return result['isError'], (json.loads(result['content'][0]['text']) if not result['isError'] else result['content'][0]['text'])

    def activity(self):
        with self.db() as db:
            return [dict(r) for r in db.execute('SELECT connection_id,tool,outcome,detail FROM ai_activity ORDER BY id')]


class Discovery(Base):
    def test_metadata_points_at_this_machine_and_requires_pkce_s256(self):
        status, _, data = self.app.ai_http('GET', '/.well-known/oauth-authorization-server', {}, b'', HOST)
        meta = json.loads(data)
        self.assertEqual((status, meta['issuer'], meta['code_challenge_methods_supported']), (200, ISSUER, ['S256']))
        self.assertEqual(meta['registration_endpoint'], ISSUER + '/oauth/register')
        status, _, data = self.app.ai_http('GET', '/.well-known/oauth-protected-resource/mcp', {}, b'', HOST)
        self.assertEqual(json.loads(data)['resource'], ISSUER + '/mcp')
        self.assertEqual(json.loads(data)['authorization_servers'], [ISSUER])

    def test_mcp_without_a_token_says_where_to_sign_in(self):
        status, headers, reply = self.call(None, 'initialize')
        self.assertEqual(status, 401)
        self.assertIn('resource_metadata="' + ISSUER + '/.well-known/oauth-protected-resource/mcp"', headers['WWW-Authenticate'])
        status, headers, _ = self.call('tma_' + 'x' * 40, 'initialize')
        self.assertEqual(status, 401)
        self.assertIn('error="invalid_token"', headers['WWW-Authenticate'])

    def test_get_and_delete_on_mcp_are_not_allowed(self):
        self.assertEqual(self.app.ai_http('GET', '/mcp', {}, b'', HOST)[0], 405)
        self.assertEqual(self.app.ai_http('DELETE', '/mcp', {}, b'', HOST)[0], 405)


class Registration(Base):
    def test_redirects_must_be_https_loopback_or_an_app_scheme(self):
        for uri in (CLAUDE, 'http://127.0.0.1:33418/callback', 'http://localhost/cb', 'cursor://anysphere.cursor-mcp/oauth/callback'):
            self.assertEqual(self.register((uri,))[0], 201, uri)
        for uri in ('http://evil.example/cb', 'javascript:alert(1)', 'data:text/html,x', 'https://x.example/cb#frag', 'file:///etc/passwd', 'myapp:/cb',
                    'https://x.example/c\u00e9', 'https://x.example/cb\r\nSet-Cookie: a=b'):
            status, out = self.register((uri,))
            self.assertEqual((status, out['error']), (400, 'invalid_redirect_uri'), uri)

    def test_a_confidential_client_secret_is_kept_only_hashed(self):
        status, out = self.register(token_endpoint_auth_method='client_secret_post')
        self.assertEqual(status, 201)
        with self.db() as db:
            row = db.execute('SELECT * FROM ai_clients WHERE id=?', (out['client_id'],)).fetchone()
        self.assertEqual(row['secret_hash'], hashlib.sha256(out['client_secret'].encode()).hexdigest())
        self.assertNotIn(out['client_secret'], json.dumps(dict(row)))

    def test_registrations_are_limited_per_hour_and_grant_nothing(self):
        for _ in range(ai_access.REGISTRATIONS_PER_HOUR):
            self.assertEqual(self.register()[0], 201)
        status, out = self.register()
        self.assertEqual((status, out['error']), (429, 'temporarily_unavailable'))
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_connections').fetchone()[0], 0)


class Authorize(Base):
    def params(self, client, **over):
        verifier, challenge = pkce()
        return {'response_type': 'code', 'client_id': client['client_id'], 'redirect_uri': CLAUDE, 'state': 's1',
                'code_challenge': challenge, 'code_challenge_method': 'S256', 'resource': ISSUER + '/mcp', **over}

    def test_pkce_is_required_and_only_s256(self):
        _, client = self.register()
        for over in ({'code_challenge': ''}, {'code_challenge_method': 'plain'}):
            status, where = self.app.ai_consent_page(urllib.parse.urlencode(self.params(client, **over)), 'csrf')
            self.assertEqual(status, 303)
            self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(where).query)['error'], ['invalid_request'])

    def test_an_unregistered_redirect_is_never_followed(self):
        _, client = self.register()
        status, page = self.app.ai_consent_page(urllib.parse.urlencode(self.params(client, redirect_uri='https://evil.example/cb')), 'csrf')
        self.assertEqual(status, 400)
        self.assertNotIn('evil.example', page)

    def test_another_resource_is_refused(self):
        _, client = self.register()
        status, where = self.app.ai_consent_page(urllib.parse.urlencode(self.params(client, resource='https://other.example/mcp')), 'csrf')
        self.assertEqual((status, urllib.parse.parse_qs(urllib.parse.urlsplit(where).query)['error']), (303, ['invalid_target']))

    def test_the_page_names_known_ais_and_marks_others_unverified(self):
        _, client = self.register()
        status, page = self.app.ai_consent_page(urllib.parse.urlencode(self.params(client)), 'csrf')
        self.assertEqual(status, 200)
        self.assertIn('Claude wants to connect', page)
        self.assertIn('name="csrf" value="csrf"', page)
        _, other = self.register(('https://agent.example/cb',))
        page = self.app.ai_consent_page(urllib.parse.urlencode(self.params(other, redirect_uri='https://agent.example/cb')), 'csrf')[1]
        self.assertIn('calls itself', page)
        self.assertIn('agent.example', page)

    def test_cancel_goes_back_with_access_denied_and_makes_nothing(self):
        _, client = self.register()
        _, challenge = pkce()
        back = self.app.ai_consent_post({'client_id': client['client_id'], 'redirect_uri': CLAUDE, 'state': 'x', 'code_challenge': challenge, 'choice': 'cancel'})
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(back).query)
        self.assertEqual((query['error'], query['state'], query['iss']), (['access_denied'], ['x'], [ISSUER]))
        with self.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM ai_connections').fetchone()[0], 0)


class Tokens(Base):
    def test_pkce_wrong_verifier_is_refused_and_logged(self):
        client, verifier, code, _ = self.connect()
        status, out = self.token({'grant_type': 'authorization_code', 'code': code, 'client_id': client['client_id'],
                                  'code_verifier': secrets.token_urlsafe(48), 'redirect_uri': CLAUDE})
        self.assertEqual((status, out['error']), (400, 'invalid_grant'))
        self.assertIn(('sign-in', 'refused'), [(x['tool'], x['outcome']) for x in self.activity()])
        # and the code is spent: the right verifier afterwards does not work either
        status, _ = self.token({'grant_type': 'authorization_code', 'code': code, 'client_id': client['client_id'], 'code_verifier': verifier})
        self.assertEqual(status, 400)

    def test_a_code_used_twice_revokes_what_it_gave(self):
        client, verifier, code, _ = self.connect()
        form = {'grant_type': 'authorization_code', 'code': code, 'client_id': client['client_id'], 'code_verifier': verifier, 'redirect_uri': CLAUDE}
        status, tokens = self.token(form)
        self.assertEqual(status, 200)
        self.assertEqual(self.call(tokens['access_token'], 'ping')[0], 200)
        self.assertEqual(self.token(form)[0], 400)
        self.assertEqual(self.call(tokens['access_token'], 'ping')[0], 401)

    def test_a_code_expires(self):
        client, verifier, code, _ = self.connect()
        later = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=ai_access.CODE_SECONDS + 5)
        with patch.object(ai_access, '_now', return_value=later):
            status, out = self.token({'grant_type': 'authorization_code', 'code': code, 'client_id': client['client_id'], 'code_verifier': verifier})
        self.assertEqual((status, out['error_description']), (400, 'Code expired'))

    def test_access_tokens_expire_and_refresh_rotates(self):
        client, tokens = self.signed_in()
        later = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=ai_access.ACCESS_SECONDS + 5)
        with patch.object(ai_access, '_now', return_value=later):
            self.assertEqual(self.call(tokens['access_token'], 'ping')[0], 401)
            status, fresh = self.token({'grant_type': 'refresh_token', 'refresh_token': tokens['refresh_token'], 'client_id': client['client_id']})
            self.assertEqual(status, 200)
            self.assertEqual(self.call(fresh['access_token'], 'ping')[0], 200)
        self.assertNotEqual(fresh['refresh_token'], tokens['refresh_token'])

    def test_an_old_refresh_token_used_again_ends_every_sign_in(self):
        client, tokens = self.signed_in()
        form = {'grant_type': 'refresh_token', 'refresh_token': tokens['refresh_token'], 'client_id': client['client_id']}
        status, fresh = self.token(form)
        self.assertEqual(status, 200)
        self.assertEqual(self.token(form)[0], 400)  # the stolen copy
        self.assertEqual(self.call(fresh['access_token'], 'ping')[0], 401)
        self.assertEqual(self.token({**form, 'refresh_token': fresh['refresh_token']})[0], 400)
        self.assertIn('refused', [x['outcome'] for x in self.activity() if x['tool'] == 'sign-in'])

    def test_a_refresh_token_belongs_to_its_client(self):
        _, tokens = self.signed_in()
        _, other = self.register()
        status, out = self.token({'grant_type': 'refresh_token', 'refresh_token': tokens['refresh_token'], 'client_id': other['client_id']})
        self.assertEqual((status, out['error']), (400, 'invalid_grant'))

    def test_a_confidential_client_must_send_its_secret(self):
        _, client = self.register(token_endpoint_auth_method='client_secret_basic')
        verifier, challenge = pkce()
        back = self.app.ai_consent_post({'client_id': client['client_id'], 'redirect_uri': CLAUDE, 'code_challenge': challenge,
                                         'level': 'read', 'area': 'both', 'expiry': '1d', 'choice': 'connect'})
        code = urllib.parse.parse_qs(urllib.parse.urlsplit(back).query)['code'][0]
        form = {'grant_type': 'authorization_code', 'code': code, 'code_verifier': verifier, 'client_id': client['client_id']}
        self.assertEqual(self.token(form)[0], 401)
        self.assertEqual(self.token({**form, 'client_secret': 'wrong'})[0], 401)
        basic = base64.b64encode(f"{client['client_id']}:{client['client_secret']}".encode()).decode()
        status, _ = self.token({k: v for k, v in form.items() if k != 'client_id'}, {'Authorization': 'Basic ' + basic})
        self.assertEqual(status, 200)

    def test_secrets_are_kept_only_hashed(self):
        client, tokens = self.signed_in()
        with self.db() as db:
            made = ai_access.new_key(db, 'Script', 'read', 'both', '7d')
        raw = (Path(self.temp.name) / 'events.sqlite').read_bytes()
        wal = Path(self.temp.name) / 'events.sqlite-wal'
        raw += wal.read_bytes() if wal.exists() else b''
        for secret in (tokens['access_token'], tokens['refresh_token'], made['key']):
            self.assertNotIn(secret.encode(), raw)
        with self.db() as db:
            hashes = {r[0] for r in db.execute('SELECT hash FROM ai_tokens')}
        self.assertIn(hashlib.sha256(tokens['access_token'].encode()).hexdigest(), hashes)


class Calls(Base):
    def test_connection_expiry_refuses_and_logs(self):
        _, tokens = self.signed_in(expiry='1d')
        with self.db() as db:
            made = ai_access.new_key(db, 'Script', 'read', 'both', '1d')
        later = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=2)
        with patch.object(ai_access, '_now', return_value=later):
            self.assertEqual(self.call(tokens['access_token'], 'ping')[0], 401)  # its access token ended with it
            error, text = self.tool(made['key'], 'list_todos')
        self.assertTrue(error)
        self.assertIn('expired', text)
        self.assertIn(('list_todos', 'refused'), [(x['tool'], x['outcome']) for x in self.activity()])

    def test_read_access_cannot_create_and_the_refusal_is_logged(self):
        _, tokens = self.signed_in('read')
        error, text = self.tool(tokens['access_token'], 'create_todo', text='Call Sam')
        self.assertTrue(error)
        self.assertIn('can only read', text)
        self.assertEqual(self.activity()[-1]['outcome'], 'refused')
        with self.db() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM suggestions WHERE dedupe_key LIKE 'ai:%'").fetchone()[0], 0)

    def test_the_level_is_read_at_every_call(self):
        _, tokens = self.signed_in('read')
        with self.db() as db:
            cid = db.execute('SELECT id FROM ai_connections').fetchone()[0]
        self.app.action('ai_change', {'id': cid, 'level': 'draft'}, owner_dashboard=True)
        error, made = self.tool(tokens['access_token'], 'create_todo', text='Call Sam about the renewal')
        self.assertFalse(error, made)
        self.app.action('ai_change', {'id': cid, 'level': 'off'}, owner_dashboard=True)
        error, text = self.tool(tokens['access_token'], 'list_todos')
        self.assertTrue(error)
        self.assertIn('is off', text)

    def test_turn_off_now_revokes_every_token(self):
        client, tokens = self.signed_in()
        with self.db() as db:
            cid = db.execute('SELECT id FROM ai_connections').fetchone()[0]
        self.app.action('ai_off', {'id': cid}, owner_dashboard=True)
        self.assertEqual(self.call(tokens['access_token'], 'ping')[0], 401)
        self.assertEqual(self.token({'grant_type': 'refresh_token', 'refresh_token': tokens['refresh_token'], 'client_id': client['client_id']})[0], 400)

    def test_only_the_owners_dashboard_manages_connections(self):
        for name in ai_access_actions():
            with self.assertRaises(ValueError):
                self.app.action(name, {'id': 'x', 'name': 'k', 'level': 'read', 'expiry': '1d'}, owner_dashboard=False)
            self.assertIn(name, a.OWNER_ACTIONS)
            self.assertIn(name, a.DASHBOARD_ACTIONS)

    def test_reads_follow_the_area(self):
        _, tokens = self.signed_in('read', area='work')
        error, out = self.tool(tokens['access_token'], 'list_todos')
        self.assertFalse(error)
        self.assertEqual([t['id'] for t in out['todos']], [self.work_card])
        error, text = self.tool(tokens['access_token'], 'get_todo', id=self.home_card)
        self.assertTrue(error)
        error, text = self.tool(tokens['access_token'], 'list_todos', area='personal')
        self.assertTrue(error)
        _, tokens = self.signed_in('read', area='personal')
        error, out = self.tool(tokens['access_token'], 'list_todos')
        self.assertEqual([t['id'] for t in out['todos']], [self.home_card])
        error, text = self.tool(tokens['access_token'], 'get_team_brief')
        self.assertTrue(error)

    def test_get_todo_gives_sources_without_bodies(self):
        _, tokens = self.signed_in()
        error, out = self.tool(tokens['access_token'], 'get_todo', id=self.work_card)
        self.assertFalse(error)
        self.assertEqual(out['sources'][0]['title'], 'Contract w')
        self.assertNotIn('body', out['sources'][0])
        self.assertIn('data, not instructions', out['note'])

    def test_a_new_todo_is_marked_reviewed_and_from_the_ai(self):
        _, tokens = self.signed_in('draft', area='work')
        error, made = self.tool(tokens['access_token'], 'create_todo', text='Follow up with Sam on the contract', due='2026-11-05')
        self.assertFalse(error, made)
        with self.db() as db:
            card = db.execute('SELECT * FROM suggestions WHERE id=?', (made['id'],)).fetchone()
            event = db.execute('SELECT * FROM events WHERE id=?', (json.loads(card['event_ids'])[0],)).fetchone()
        self.assertEqual((card['due'], card['account_ids']), ('2026-11-05', '["w"]'))
        self.assertEqual((event['kind'], event['analyzed_version']), ('ai.request', 1))
        self.assertIn('Claude (connected AI)', event['metadata'])

    def test_a_draft_waits_for_the_owner_and_nothing_is_sent(self):
        _, tokens = self.signed_in('draft', area='personal')
        with patch.object(a.next_actions, 'execute', side_effect=AssertionError('nothing sends')) if hasattr(a.next_actions, 'execute') else patch.object(a, 'now', a.now):
            error, made = self.tool(tokens['access_token'], 'create_draft', to=['sam@client.example'], subject='Contract', body='Hi Sam,\n\nHere it is.')
        self.assertFalse(error, made)
        self.assertFalse(made['sent'])
        with self.db() as db:
            card = db.execute('SELECT * FROM suggestions WHERE id=?', (made['id'],)).fetchone()
            jobs = db.execute('SELECT count(*) FROM action_jobs WHERE suggestion_id=?', (made['id'],)).fetchone()[0]
        action = json.loads(card['next_action'])
        self.assertEqual((card['status'], action['kind'], action['account_id'], action['to']), ('prepared', 'email', 'p', ['sam@client.example']))
        self.assertEqual(jobs, 0)

    def test_new_todos_are_limited_per_day(self):
        _, tokens = self.signed_in('draft')
        for n in range(ai_access.CREATES_PER_DAY):
            self.assertFalse(self.tool(tokens['access_token'], 'create_todo', text=f'Thing {n}')[0])
        error, text = self.tool(tokens['access_token'], 'create_todo', text='One more')
        self.assertTrue(error)
        self.assertEqual(self.activity()[-1]['outcome'], 'refused')

    def test_calls_are_rate_limited(self):
        _, tokens = self.signed_in()
        self.app.ai_limiter = ai_access.Limiter(per_minute=2)
        self.assertFalse(self.tool(tokens['access_token'], 'list_todos')[0])
        self.assertFalse(self.tool(tokens['access_token'], 'list_todos')[0])
        error, text = self.tool(tokens['access_token'], 'list_todos')
        self.assertTrue(error)
        self.assertIn('Too many calls', text)

    def test_every_call_is_in_the_activity(self):
        _, tokens = self.signed_in()
        self.tool(tokens['access_token'], 'list_todos')
        self.tool(tokens['access_token'], 'get_todo', id='nope')
        self.tool(tokens['access_token'], 'create_draft', to=['x@y.example'], subject='s', body='b')
        lines = [(x['tool'], x['outcome']) for x in self.activity()]
        self.assertEqual(lines[-3:], [('list_todos', 'ok'), ('get_todo', 'error'), ('create_draft', 'refused')])
        with self.db() as db:
            cid = db.execute('SELECT id FROM ai_connections').fetchone()[0]
        with self.db() as db:  # its own activity is Settings, Activity filtered to it (activity_log.py)
            shown = a.activity_log.page(db, self.app.config, kind='ai', actor=cid)['items']
        self.assertEqual([x['outcome'] for x in shown[:3]], ['refused', 'failed', 'done'])
        self.assertEqual((shown[0]['what'], shown[0]['where'], shown[0]['actor']), ('Asked to add an email draft', 'Claude', cid))

    def test_a_key_works_as_a_bearer_and_is_shown_once(self):
        view = self.app.action('ai_key', {'name': 'Script', 'level': 'read', 'area': 'work', 'expiry': '7d'}, owner_dashboard=True)
        key = view['made']['key']
        self.assertTrue(key.startswith('tm_ai_'))
        self.assertNotIn(key, json.dumps(self.app.action('ai_connections', {}, owner_dashboard=True)))
        error, out = self.tool(key, 'list_todos')
        self.assertEqual([t['id'] for t in out['todos']], [self.work_card])

    def test_tools_list_names_every_tool_and_marks_the_read_ones(self):
        _, tokens = self.signed_in()
        status, _, reply = self.call(tokens['access_token'], 'tools/list')
        tools = {t['name']: t for t in reply['result']['tools']}
        self.assertEqual(set(tools), set(ai_access.TOOLS))
        self.assertTrue(tools['list_todos']['annotations']['readOnlyHint'])
        self.assertFalse(tools['create_draft']['annotations']['readOnlyHint'])
        self.assertNotIn('send', ' '.join(tools))


def ai_access_actions():
    return sorted(a.AI_ACTIONS)


class Http(Base):
    """Over the real handler: the owner's sign-in and the service token never count on /mcp, and the consent page
    is the owner's own, with its CSRF token and the dashboard's origin."""

    def serve(self):
        servers = []
        real = a.http.server.ThreadingHTTPServer

        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs))
            return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture), patch.object(a.signal, 'signal'),
                        patch.object(a.App, 'preparation_worker'), patch.object(a.App, 'delivery_worker')):
            patcher.start()
            self.addCleanup(patcher.stop)
        thread = threading.Thread(target=self.app.serve, daemon=True)
        thread.start()
        while not servers:
            pass
        self.addCleanup(lambda: (self.app.stop.set(), thread.join(5)))
        return servers[0].server_address[1]

    def request(self, port, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
        conn.request(method, path, body=body, headers=headers or {})
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return response.status, dict(response.getheaders()), data

    def test_the_owner_and_the_service_token_do_not_open_mcp(self):
        port = self.serve()
        ping = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': 'list_todos'}})
        for headers in (OWNER, {'Authorization': 'Bearer ' + TOKEN, 'Host': HOST}, {**OWNER, 'X-CSRF-Token': 'x', 'Origin': ISSUER}):
            status, _, _ = self.request(port, 'POST', '/mcp', ping, {**headers, 'Content-Type': 'application/json'})
            self.assertEqual(status, 401, headers)

    def test_the_consent_page_is_the_owners_and_needs_csrf_and_origin(self):
        port = self.serve()
        _, client = self.register()
        _, challenge = pkce()
        query = urllib.parse.urlencode({'response_type': 'code', 'client_id': client['client_id'], 'redirect_uri': CLAUDE,
                                        'code_challenge': challenge, 'code_challenge_method': 'S256'})
        self.assertEqual(self.request(port, 'GET', '/oauth/authorize?' + query, headers={'Host': HOST})[0], 403)
        status, headers, page = self.request(port, 'GET', '/oauth/authorize?' + query, headers=OWNER)
        self.assertEqual(status, 200)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        csrf = a.dashboard_csrf(TOKEN, 'owner@example.com')
        form = {'client_id': client['client_id'], 'redirect_uri': CLAUDE, 'code_challenge': challenge, 'level': 'read',
                'area': 'both', 'expiry': '7d', 'choice': 'connect'}
        post = lambda f, h: self.request(port, 'POST', '/oauth/authorize', urllib.parse.urlencode(f),
                                         {**h, 'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(post({**form, 'csrf': 'wrong'}, {**OWNER, 'Origin': ISSUER})[0], 403)
        self.assertEqual(post({**form, 'csrf': csrf}, {**OWNER, 'Origin': 'https://evil.example'})[0], 403)
        self.assertEqual(post({**form, 'csrf': csrf}, {'Host': HOST, 'Origin': ISSUER})[0], 403)
        status, headers, _ = post({**form, 'csrf': csrf}, {**OWNER, 'Origin': ISSUER})
        self.assertEqual(status, 303)
        self.assertTrue(headers['Location'].startswith(CLAUDE + '?code='))

    def test_metadata_and_registration_need_no_sign_in(self):
        port = self.serve()
        status, _, data = self.request(port, 'GET', '/.well-known/oauth-authorization-server', headers={'Host': HOST})
        self.assertEqual((status, json.loads(data)['issuer']), (200, ISSUER))
        status, _, data = self.request(port, 'POST', '/oauth/register', json.dumps({'redirect_uris': [CLAUDE]}),
                                       {'Host': HOST, 'Content-Type': 'application/json'})
        self.assertEqual(status, 201)


if __name__ == '__main__':
    unittest.main()

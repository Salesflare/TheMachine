"""sources.py: reading the owner's sources (errors, credentials, gog_read, which accounts are mail or calendar)."""
import datetime as dt
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

import sources


class Errors(unittest.TestCase):
    def test_source_error_says_only_its_label(self):
        error = sources.SourceError('gmail', 503, 30)
        self.assertEqual((str(error), error.category, error.status, error.retry_after), ('gmail:HTTP_503', 'gmail', 503, 30))
        self.assertEqual(str(sources.SourceError('timeout')), 'timeout')

    def test_what_is_transient(self):
        E = sources.SourceError
        self.assertTrue(sources.rate_limited(E('slack', 429)))
        self.assertTrue(sources.rate_limited(E('slack_ratelimited')))
        self.assertFalse(sources.rate_limited(E('slack', 500)))
        self.assertTrue(sources.upstream_busy(E('gmail', 502)))
        self.assertFalse(sources.upstream_busy(E('gmail', 404)))
        for busy in (E('gmail', 503), E('network:reset'), E('timeout'), E('slack_network'), E('broker_unreachable')):
            with self.subTest(error=str(busy)):
                self.assertTrue(sources.transient(busy))
        after_busy = E('docs_microsoft', 400)
        after_busy.after_busy = True
        self.assertTrue(sources.transient(after_busy))
        for bug in (E('gmail', 401), E('gmail', 400), E('invalid_json'), ValueError('x')):
            with self.subTest(error=str(bug)):
                self.assertFalse(sources.transient(bug))


class Credentials(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_credential_from_config_or_systemd(self):
        (self.root / 'key').write_text(' from-config \n')
        config = {'credentials': {'api': str(self.root / 'key')}}
        self.assertEqual(sources.credential(config, 'api'), 'from-config')
        (self.root / 'creds').mkdir()
        (self.root / 'creds' / 'api').write_text('from-systemd')
        with patch.dict(os.environ, {'CREDENTIALS_DIRECTORY': str(self.root / 'creds')}):
            self.assertEqual(sources.credential(config, 'api'), 'from-systemd')

    def test_owner_credential_is_made_once_owner_only(self):
        config = {'credentials': {}, 'database': str(self.root / 'events.sqlite')}
        first = sources.owner_credential(config)
        self.assertEqual(len(first), 64)
        self.assertEqual(sources.owner_credential(config), first)
        self.assertEqual(stat.S_IMODE((self.root / 'owner-token').stat().st_mode), 0o600)


class Accounts(unittest.TestCase):
    def test_mail_accounts(self):
        self.assertTrue(sources.mail_account({'transport': 'gog'}))
        self.assertTrue(sources.mail_account({'service': 'outlook', 'transport': 'graph'}))
        self.assertFalse(sources.mail_account({'service': 'outlook', 'transport': 'gog'}))
        self.assertFalse(sources.mail_account({'service': 'calendar', 'transport': 'gog'}))
        config = {'accounts': [{'id': 'o', 'service': 'outlook'}, {'id': 'g', 'service': 'gmail'}]}
        self.assertEqual((sources.mailbox_name(config, {'account_id': 'o'}), sources.mailbox_name(config, {'account_id': 'g'})),
                         ('Outlook', 'Gmail'))

    def test_gog_signin_on_disk(self):
        account = {'email': 'owner@example.com', 'client': 'mine'}
        self.assertEqual(sources.gog_signin_command({}, account), 'gog auth add owner@example.com --client mine')
        with tempfile.TemporaryDirectory() as tmp:
            config = {'gog_keyring_dir': tmp}
            token = sources.gog_token_path(config, account)
            self.assertEqual(token.parent, Path(tmp))
            self.assertTrue(token.name.startswith('_gogcli_key_v1_'))
            gog = {**account, 'transport': 'gog'}
            self.assertFalse(sources.gog_signed_in_since(config, gog, '2026-01-01T00:00:00+00:00'))  # no token yet
            token.write_text('t')
            os.utime(token, (1e9, 1e9))  # 2001
            self.assertFalse(sources.gog_signed_in_since(config, gog, '2026-01-01T00:00:00+00:00'))
            self.assertTrue(sources.gog_signed_in_since(config, gog, '2000-01-01T00:00:00+00:00'))
            self.assertFalse(sources.gog_signed_in_since(config, {**gog, 'transport': 'broker'}, '2000-01-01T00:00:00+00:00'))


class GogRead(unittest.TestCase):
    account = {'email': 'owner@example.com', 'client': 'mine', 'transport': 'gog'}

    def setUp(self):
        sources._gog_tokens.clear()
        self.addCleanup(sources._gog_tokens.clear)

    def read(self, returncode=0, stdout='{"id": "x"}', stderr=''):
        result = type('R', (), {'returncode': returncode, 'stdout': stdout, 'stderr': stderr})()
        with patch.object(sources, 'credential', return_value='pw'), patch.object(sources.subprocess, 'run', return_value=result) as run:
            got = sources.gog_read({'gog': 'gog'}, self.account, 'gmail', 'v1', 'gmail.users.getProfile', {'userId': 'me'}, 'scope')
        return got, run.call_args

    def test_a_read_only_call(self):
        got, call = self.read()
        self.assertEqual(got, {'id': 'x'})
        command, env = call.args[0], call.kwargs['env']
        self.assertEqual(command[command.index('--params') + 1], '{"userId":"me"}')
        self.assertIn('--readonly', command)
        self.assertEqual((env['GOG_KEYRING_BACKEND'], env['GOG_KEYRING_PASSWORD']), ('file', 'pw'))

    def test_failures_are_labels(self):
        for kwargs, label in (({'returncode': 1, 'stderr': 'HTTP 403 for owner@example.com'}, 'gmail:HTTP_403'),
                              ({'returncode': 1, 'stderr': 'invalid_grant'}, 'gmail:google_signin_expired_run_gog_auth_add'),
                              ({'stdout': 'not json'}, 'invalid_json'), ({'stdout': '{"error": 1}'}, 'invalid_response')):
            with self.subTest(label=label), self.assertRaises(sources.SourceError) as caught:
                self.read(**kwargs)
            self.assertEqual(str(caught.exception), label)
        with self.assertRaisesRegex(sources.SourceError, 'unsupported_transport'):
            sources.gog_read({}, {'transport': 'imap'}, 'gmail', 'v1', 'm', {}, 's')

    def test_gog_starts_lean_unless_the_service_says_otherwise(self):
        with patch.dict(os.environ, {}, clear=False):
            for key in sources.GOG_RUNTIME:
                os.environ.pop(key, None)
            _, call = self.read()
            self.assertEqual({k: call.kwargs['env'][k] for k in sources.GOG_RUNTIME},
                             {'GOMAXPROCS': '1', 'GOGC': 'off', 'GOMEMLIMIT': '256MiB'})
            os.environ['GOMAXPROCS'] = '4'
            _, call = self.read()
            self.assertEqual((call.kwargs['env']['GOMAXPROCS'], call.kwargs['env']['GOGC']), ('4', 'off'))


# A stand-in for `gog api call gmail v1 <method>`: a mailbox of FAKE_GOG_COUNT made-up messages; it appends the Go
# runtime settings it was started with to FAKE_GOG_LOG. Never reaches Google.
FAKE_MAILBOX = r'''
import base64


def answer(method, params, count):
    b64 = lambda text: base64.urlsafe_b64encode(text.encode()).decode().rstrip('=')
    if method == 'gmail.users.getProfile':
        return {'emailAddress': 'owner@example.com', 'historyId': '900'}
    if method == 'gmail.users.messages.list':
        start, size = int(params.get('pageToken') or 0), int(params['maxResults'])
        found = {'messages': [{'id': 'm%04d' % i, 'threadId': 't%04d' % (i // 2)} for i in range(start, min(count, start + size))]}
        if start + size < count:
            found['nextPageToken'] = str(start + size)
        return found
    if method == 'gmail.users.messages.get':
        i = int(params['id'][1:])
        return {'id': params['id'], 'threadId': 't%04d' % (i // 2), 'labelIds': ['INBOX'], 'snippet': 'Fixture body %d.' % i,
                'internalDate': str(1793000000000 - i * 60000),
                'payload': {'mimeType': 'multipart/alternative', 'headers': [
                    {'name': 'From', 'value': 'Sender %d <sender%d@example.org>' % (i, i)}, {'name': 'To', 'value': 'owner@example.com'},
                    {'name': 'Subject', 'value': 'Fixture subject %d' % i}, {'name': 'Message-ID', 'value': '<m%d@example.org>' % i}],
                    'parts': [{'mimeType': 'text/plain', 'body': {'data': b64('Fixture body %d.' % i)}},
                              {'mimeType': 'text/html', 'body': {'data': b64('<p>Fixture body %d.</p>' % i)}}]}}
    raise SystemExit('unexpected method ' + method)
'''
# `gog auth tokens export` hands over FAKE_GOG_TOKEN (a made-up access token) expiring FAKE_GOG_EXPIRES, when set; without
# it the export fails, as on a gog without that command.
FAKE_GOG = FAKE_MAILBOX + r'''
import json, os, sys
args = sys.argv[1:]
with open(os.environ['FAKE_GOG_LOG'], 'a') as log:
    log.write(json.dumps({k: os.environ.get(k) for k in ('GOMAXPROCS', 'GOGC', 'GOMEMLIMIT')}) + '\n')
if args[:3] == ['auth', 'tokens', 'export']:
    if not os.environ.get('FAKE_GOG_TOKEN'):
        sys.exit('unexpected argument tokens')
    print(json.dumps({'email': args[3], 'client': args[args.index('--client') + 1], 'refresh_token': 'fixture-refresh',
                      'access_token': os.environ['FAKE_GOG_TOKEN'], 'access_token_expires_at': os.environ['FAKE_GOG_EXPIRES']}, indent=2))
    sys.exit(0)
method, params = args[4], json.loads(args[args.index('--params') + 1])
print(json.dumps(answer(method, params, int(os.environ['FAKE_GOG_COUNT']))))
'''


class GogSync(unittest.TestCase):
    """The Gmail sync through a gog stand-in: the lean Go runtime settings reach every gog process and the messages
    synced are the same as without them."""

    class Store:
        def __init__(self):
            self.state, self.events = None, []

        def checkpoint(self, account):
            return self.state

        def commit_page(self, account, state, events, *args, **kwargs):
            self.state = state
            self.events.extend(events)

    def setUp(self):
        sources._gog_tokens.clear()
        self.addCleanup(sources._gog_tokens.clear)

    def sync(self, runtime, env=None, count=45):
        """The whole first import through the gog stand-in: (events, the runtime of each gog process it started)."""
        from machine.sources.gmail import sync_gmail
        sources._gog_tokens.clear()
        with tempfile.TemporaryDirectory() as tmp:
            script, gog, log, password = (Path(tmp) / name for name in ('fake_gog.py', 'gog', 'log', 'password'))
            script.write_text(FAKE_GOG)
            gog.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n')
            gog.chmod(0o700)
            password.write_text('fixture\n')
            config = {'gog': str(gog), 'credentials': {'gog-password': str(password)}, 'bootstrap_days': 7}
            account = {'id': 'work-gmail', 'service': 'gmail', 'transport': 'gog', 'email': 'owner@example.com', 'client': 'default'}
            store = self.Store()
            clean = {k: v for k, v in os.environ.items() if k not in sources.GOG_RUNTIME}
            with patch.dict(os.environ, {**clean, 'FAKE_GOG_COUNT': str(count), 'FAKE_GOG_LOG': str(log), **(env or {})}, clear=True), \
                    patch.object(sources, 'GOG_RUNTIME', runtime):
                while (store.state or {}).get('mode') != 'incremental':
                    sync_gmail(store, config, account)
            return store.events, [json.loads(line) for line in log.read_text().splitlines()]

    def test_same_messages_synced_with_lean_gog(self):
        before, plain = self.sync({})
        after, lean = self.sync(sources.GOG_RUNTIME)
        self.assertEqual(len(after), 45)
        self.assertEqual(after, before)
        self.assertEqual({json.dumps(started, sort_keys=True) for started in plain},
                         {json.dumps({'GOMAXPROCS': None, 'GOGC': None, 'GOMEMLIMIT': None}, sort_keys=True)})
        self.assertEqual(len(lean), len(plain))
        self.assertTrue(all(started == {'GOMAXPROCS': '1', 'GOGC': 'off', 'GOMEMLIMIT': '256MiB'} for started in lean))


class FakeGmail:
    """Gmail's REST API for the made-up mailbox (FAKE_MAILBOX), in place of urlopen: it records each request and can
    refuse the next ones with a status. Never reaches Google."""

    def __init__(self, count=45, refuse=()):
        self.mailbox, self.count, self.refuse, self.seen = {}, count, list(refuse), []
        exec(FAKE_MAILBOX, self.mailbox)  # noqa: S102 - the test's own fixture

    def __call__(self, request, timeout=None):
        import io
        import urllib.error
        import urllib.parse
        parts = urllib.parse.urlsplit(request.full_url)
        self.seen.append((request.get_method(), parts.hostname, request.get_header('Authorization')))
        if self.refuse:
            status, body = self.refuse.pop(0)
            raise urllib.error.HTTPError(request.full_url, status, 'refused', {}, io.BytesIO(body.encode()))
        path = parts.path.split('/gmail/v1/users/me/')[1]
        params = {k: v[0] for k, v in urllib.parse.parse_qs(parts.query).items()}
        method = {'profile': 'gmail.users.getProfile', 'messages': 'gmail.users.messages.list'}.get(path, 'gmail.users.messages.get')
        if method == 'gmail.users.messages.get':
            params['id'] = path.split('/')[1]
        answer = json.dumps(self.mailbox['answer'](method, params, self.count)).encode()
        return type('Answer', (io.BytesIO,), {'__enter__': lambda s: s, '__exit__': lambda s, *a: s.close()})(answer)


class GogToken(unittest.TestCase):
    """A self-hosted Gmail account reads with gog's own access token in-process (sources.gog_token): one gog process
    for the token instead of one per message, the same messages, and gog for every read again whenever that token can't
    be used."""
    TOKEN = 'fixture-access-token'
    Store, setUp, sync = GogSync.Store, GogSync.setUp, GogSync.sync

    def expires(self, seconds):
        return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat().replace('+00:00', 'Z')

    def test_one_gog_process_instead_of_one_per_message(self):
        gog_only, processes = self.sync(sources.GOG_RUNTIME, count=100)
        web = FakeGmail(count=100)
        with patch.object(sources.google_api.urllib.request, 'urlopen', web):
            in_process, exports = self.sync(sources.GOG_RUNTIME, {'FAKE_GOG_TOKEN': self.TOKEN, 'FAKE_GOG_EXPIRES': self.expires(3600)}, count=100)
        self.assertEqual(in_process, gog_only)
        self.assertEqual(len(in_process), 100)
        self.assertEqual(len(processes), 1 + 3 * 2 + 100)  # the failed export, then a profile and a list per page of 40, a read each
        self.assertEqual(len(exports), 1)  # the token, once
        self.assertEqual(len(web.seen), 3 * 2 + 100)
        self.assertEqual({seen for seen in web.seen}, {('GET', 'gmail.googleapis.com', 'Bearer ' + self.TOKEN)})

    def test_an_expired_or_refused_token_goes_back_to_gog(self):
        for env in ({'FAKE_GOG_TOKEN': self.TOKEN, 'FAKE_GOG_EXPIRES': self.expires(-60)},  # gog doesn't keep a fresh one
                    {'FAKE_GOG_TOKEN': self.TOKEN, 'FAKE_GOG_EXPIRES': 'not a time'},
                    {'FAKE_GOG_TOKEN': self.TOKEN, 'FAKE_GOG_EXPIRES': self.expires(30)}):  # inside GOG_TOKEN_MARGIN
            web = FakeGmail()
            with self.subTest(env=env), patch.object(sources.google_api.urllib.request, 'urlopen', web):
                events, processes = self.sync(sources.GOG_RUNTIME, env)
                self.assertEqual(len(events), 45)
                self.assertEqual(web.seen, [])
                self.assertLessEqual(len(processes), 2 + 2 * 2 + 45)  # at most two exports over the whole import
        scope = '{"error": {"details": [{"reason": "ACCESS_TOKEN_SCOPE_INSUFFICIENT"}]}}'
        for refused, more_tries in ((401, 1), (403, 0)):
            web = FakeGmail(refuse=[(refused, scope)])
            with self.subTest(refused=refused), patch.object(sources.google_api.urllib.request, 'urlopen', web):
                events, processes = self.sync(sources.GOG_RUNTIME, {'FAKE_GOG_TOKEN': self.TOKEN, 'FAKE_GOG_EXPIRES': self.expires(3600)})
                self.assertEqual(len(events), 45)
                # the refused read went through gog; after a 401 the next read takes the keyring's token again
                self.assertEqual(len(web.seen), 1 + more_tries * (2 * 2 + 45 - 1))

    def test_google_refusals_are_labels_never_the_token(self):
        web = FakeGmail(refuse=[(404, '{}'), (429, '{"error": {"errors": [{"reason": "rateLimitExceeded"}]}}')])
        held = (self.TOKEN, dt.datetime.now().timestamp() + 3600)
        with patch.object(sources, 'credential', return_value='pw'), patch.object(sources, '_gog_export', return_value=held), \
                patch.object(sources.google_api.urllib.request, 'urlopen', web), patch.object(sources.subprocess, 'run') as run:
            account = {'email': 'owner@example.com', 'client': 'mine', 'transport': 'gog'}
            for status in (404, 429):
                with self.assertRaises(sources.SourceError) as caught:
                    sources.gog_read({'gog': 'gog'}, account, 'gmail', 'v1', 'gmail.users.messages.get', {'userId': 'me', 'id': 'm1'}, 'scope')
                self.assertEqual((caught.exception.category, caught.exception.status), ('gmail', status))
                self.assertNotIn(self.TOKEN, str(caught.exception))
        run.assert_not_called()

    def test_only_gmail_reads_and_only_the_accounts_own_sign_in(self):
        export = patch.object(sources, '_gog_export', return_value=(self.TOKEN, dt.datetime.now().timestamp() + 3600))
        result = type('R', (), {'returncode': 0, 'stdout': '{"items": []}', 'stderr': ''})()
        with export as exported, patch.object(sources, 'credential', return_value='pw'), \
                patch.object(sources.subprocess, 'run', return_value=result) as run:
            sources.gog_read({'gog': 'gog'}, {'email': 'owner@example.com', 'client': 'mine', 'transport': 'gog'},
                             'calendar', 'v3', 'calendar.events.list', {'calendarId': 'primary'}, 'scope')
        exported.assert_not_called()
        self.assertEqual(run.call_count, 1)
        sources._gog_tokens.clear()
        other = json.dumps({'email': 'someone@example.com', 'client': 'mine', 'access_token': 'x', 'access_token_expires_at': self.expires(3600)})
        exported = type('R', (), {'returncode': 0, 'stdout': other, 'stderr': ''})()
        with patch.object(sources, 'credential', return_value='pw'), patch.object(sources.subprocess, 'run', return_value=exported):
            self.assertIsNone(sources.gog_token({'gog': 'gog'}, {'email': 'owner@example.com', 'client': 'mine'}))


if __name__ == '__main__':
    unittest.main()

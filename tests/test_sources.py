"""sources.py: reading the owner's sources (errors, credentials, gog_read, which accounts are mail or calendar)."""
import os
from pathlib import Path
import stat
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


if __name__ == '__main__':
    unittest.main()

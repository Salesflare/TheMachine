"""Sign in with Slack (slack_api.py, transport broker): the owner's own Slack sign-in through the control plane's Slack app.
Every HTTP request is faked: nothing reaches Slack, Maton or a broker. The sign-in goes to the broker only and never
leaves this Machine; Slack itself only ever sees short-lived access tokens. A Slack account read through Maton keeps
working as before, with no nudge; signing in with Slack anyway switches that same account over."""
import json
import tempfile
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest.mock import patch

import mail_grants
import next_actions
import onboarding
import slack_api
from test_connectors import a, Response

KEY = 't0team123:u0me12345'
BROKER = {'id': 'work-slack', 'service': 'slack', 'transport': 'broker', 'boundary': 'work:Acme', 'team_id': 'T0TEAM123',
          'user_id': 'U0ME12345', 'email': 'sam@acme.test', 'slack_host': 'acme.slack.com'}
MATON = {'id': 'work-slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Acme', 'team_id': 'T0TEAM123',
         'user_id': 'U0ME12345', 'email': 'sam@acme.test', 'credential': 'maton-slack', 'credential_variable': 'MATON_API_KEY',
         'connection_id': 'conn-1', 'slack_host': 'acme.slack.com'}


class SlackSignin(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / 'broker').write_text('app-token\n')
        (root / 'maton.env').write_text('MATON_API_KEY=mk_fixture\n')
        self.path = root / 'config.json'
        self.config = {'database': str(root / 'events.sqlite'), 'slack_broker': {'url': 'https://cp.example/api/slack/token'},
                       'credentials': {'slack-broker': str(root / 'broker'), 'maton-slack': str(root / 'maton.env')},
                       'accounts': []}
        mail_grants.put(self.config, 'slack', KEY, 'xoxe-1-first')
        slack_api._tokens.clear()
        patch.object(onboarding, '_assistant', a).start()
        self.broker_calls, self.slack_calls, self.maton_calls = [], [], []
        self.broker_status, self.expired_once, self.team = 200, False, 'T0TEAM123'
        patch('urllib.request.urlopen', side_effect=self.respond).start()
        patch.object(a.Slack, 'pace', lambda self, method: None).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        url = urllib.parse.urlsplit(request.full_url)
        if url.netloc == 'cp.example':
            self.assertEqual((request.get_method(), request.get_header('Authorization')), ('POST', 'Bearer app-token'))
            self.broker_calls.append(json.loads(request.data))
            if self.broker_status != 200:
                raise urllib.error.HTTPError(request.full_url, self.broker_status, 'no', {}, None)
            n = len(self.broker_calls)
            return Response(json.dumps({'access_token': f'xoxe.xoxp-{n}', 'expires_in': 43200, 'refresh_token': f'xoxe-1-r{n}'}).encode())
        method = url.path.rsplit('/', 1)[-1]
        params = dict(urllib.parse.parse_qsl(url.query))
        if url.netloc == 'api.maton.ai':
            self.assertEqual(request.get_header('Maton-connection'), 'conn-1')
            self.assertEqual(request.get_header('Authorization'), 'Bearer mk_fixture')
            self.maton_calls.append(method)
            headers = {'Maton-Connection': 'conn-1'}
        else:
            self.assertEqual(url.netloc, 'slack.com')
            self.assertIsNone(request.get_header('Maton-connection'))
            self.assertTrue(request.get_header('Authorization').startswith('Bearer xoxe.xoxp-'))  # never the sign-in itself
            self.assertNotIn('xoxe-1', request.full_url + str(request.data or ''))
            self.slack_calls.append(method)
            headers = {}
        if self.expired_once:
            self.expired_once = False
            return Response(json.dumps({'ok': False, 'error': 'token_expired'}).encode(), headers)
        if method == 'auth.test':
            body = {'ok': True, 'team_id': self.team, 'user_id': 'U0ME12345', 'team': 'Acme', 'user': 'sam', 'url': 'https://acme.slack.com/'}
        elif method == 'users.info':
            body = {'ok': True, 'user': {'id': params.get('user'), 'real_name': 'Sam Lee', 'profile': {'email': 'sam@acme.test'}}}
        elif method == 'users.lookupByEmail':
            body = {'ok': True, 'user': {'id': 'U0ALEX1', 'real_name': 'Alex Kim', 'profile': {}}}
        elif method == 'conversations.open':
            self.assertEqual(request.get_method(), 'POST')
            body = {'ok': True, 'channel': {'id': 'D0DM1'}}
        elif method == 'chat.postMessage':
            self.assertEqual(json.loads(request.data)['channel'], 'D0DM1')
            body = {'ok': True, 'ts': '1792000000.000100'}
        else:
            raise AssertionError(method)
        return Response(json.dumps(body).encode(), headers)

    def test_it_reads_straight_from_slack_with_short_lived_tokens_and_keeps_the_rolled_sign_in(self):
        slack = a.Slack(self.config, BROKER)
        slack.profile()
        self.assertEqual(self.slack_calls, ['auth.test', 'users.info'])
        self.assertEqual(self.broker_calls, [{'email': KEY, 'refresh_token': 'xoxe-1-first'}])
        self.assertEqual(mail_grants.get(self.config, 'slack', KEY), 'xoxe-1-r1')  # Slack rolled it: the new one is kept
        a.Slack(self.config, BROKER).get('auth.test')
        self.assertEqual(len(self.broker_calls), 1)  # the access token lasts hours: no refresh per call
        self.assertEqual(self.maton_calls, [])

    def test_an_access_token_that_ran_out_early_is_refreshed_once(self):
        slack_api.broker_token(self.config, BROKER)
        self.expired_once = True
        self.assertTrue(a.Slack(self.config, BROKER).get('auth.test')['ok'])
        self.assertEqual([c['refresh_token'] for c in self.broker_calls], ['xoxe-1-first', 'xoxe-1-r1'])

    def test_a_removed_sign_in_asks_to_sign_in_again(self):
        self.broker_status = 401
        with self.assertRaisesRegex(a.SourceError, 'slack_signin_expired'):
            a.Slack(self.config, BROKER).get('auth.test')
        self.assertIn('sign in with Slack again', onboarding.hint('slack_signin_expired'))

    def test_only_the_allowed_methods(self):
        with self.assertRaisesRegex(a.SourceError, 'slack_method_not_allowed'):
            a.Slack(self.config, BROKER).get('chat.postMessage')
        self.assertEqual(self.broker_calls, [])

    def test_a_maton_account_keeps_reading_through_maton(self):
        a.Slack(self.config, MATON).get('auth.test')
        self.assertEqual((self.maton_calls, self.slack_calls, self.broker_calls), (['auth.test'], [], []))

    def test_an_approved_dm_goes_straight_to_slack_as_the_owner(self):
        self.config['accounts'] = [BROKER]
        transport = next_actions.SlackTransport(self.config, a.credential)
        action = {'kind': 'slack', 'account_id': 'work-slack', 'to_name': 'Alex Kim', 'to_email': 'alex@client.test', 'body': 'Hi Alex'}
        result = transport.send(action, {'created_at': '2026-10-29T10:00:00+00:00'})
        self.assertEqual(result['message_id'], 'slack:D0DM1:1792000000.000100')
        self.assertEqual(self.slack_calls, ['users.lookupByEmail', 'conversations.open', 'chat.postMessage'])
        self.assertEqual(self.maton_calls, [])

    def test_signing_in_switches_the_maton_account_over_keeping_its_id(self):
        self.config['accounts'] = [dict(MATON)]
        account = onboarding.slack_signed_in(self.config, KEY)
        self.assertEqual(account['id'], 'work-slack')
        self.assertEqual((account['transport'], account['team_id'], account['user_id'], account['email'], account['boundary']),
                         ('broker', 'T0TEAM123', 'U0ME12345', 'sam@acme.test', 'work:Acme'))
        for gone in ('credential', 'credential_variable', 'connection_id'):
            self.assertNotIn(gone, account)
        self.assertEqual(self.maton_calls, [])

    def test_a_new_workspace_is_a_new_account_named_after_it(self):
        account = onboarding.slack_signed_in(self.config, KEY)
        self.assertEqual((account['transport'], account['boundary'], account['boundary_by'], account['slack_host']),
                         ('broker', 'work:Acme', 'guess', 'acme.slack.com'))
        self.assertNotIn('connection_id', account)

    def test_a_sign_in_for_another_account_is_refused(self):
        self.team = 'T0OTHER12'
        with self.assertRaisesRegex(onboarding.SetupError, 'another account'):
            onboarding.slack_signed_in(self.config, KEY)
        with self.assertRaisesRegex(onboarding.SetupError, 'No Slack sign-in'):
            onboarding.slack_signed_in(self.config, 'sam@acme.test')

    def test_maton_accounts_stay_on_maton_and_new_ones_sign_in_from_add(self):
        manage = 'https://app.example.com/setup'
        self.assertEqual(a.reconnect_help(MATON, manage), {'connect_name': 'slack'})  # no nudge: Maton's own Reconnect
        self.assertEqual(a.reconnect_help(MATON, None), {'connect_name': 'slack'})
        self.assertEqual(a.reconnect_help(BROKER, manage)['hosted_signin'], 'slack')
        self.assertEqual(a.reconnect_help(BROKER, None), {'connect_name': 'slack', 'signin': 'slack'})

    def test_a_broker_account_needs_the_slack_broker(self):
        self.assertEqual(onboarding.missing({**self.config, 'slack_broker': {}}, BROKER), 'slack_broker url is not set')
        self.assertEqual(onboarding.missing(self.config, BROKER), '')

    def test_add_on_a_hosted_machine_signs_in_with_slack(self):
        """+ Add's Slack tile is Sign in with Slack on a hosted Machine too (Maton is the other way, on the account page)."""
        import assistant
        app = object.__new__(assistant.App)
        app.config = {**self.config, 'manage_url': 'https://cp.example/account'}
        app.store = assistant.Store(Path(self.config['database']))
        found = {s['name']: s for s in app.action('connect_sources', {}, owner_dashboard=True)['sources']}
        self.assertIn('slack', a.HOSTED_SIGNINS)
        self.assertEqual(found['slack'].get('hosted_signin'), 'slack')
        self.assertFalse(found['slack'].get('broker'))  # its own tile: the dashboard offers "Or use a Maton API key" beside it


class SlackPace(unittest.TestCase):
    """How the reader keeps to Slack's limits: one history read per round (SLACK_LIMITS, by transport), Tier 2 lists
    spaced out, and a 429 honored with Slack's Retry-After, never a quick retry."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'credentials': {}}
        self.waits = []

    def slack(self, account, config=None):
        stop = type('Stop', (), {'wait': lambda _, seconds: self.waits.append(round(seconds, 1)) or False})()
        return a.Slack({**self.config, **(config or {})}, {**account, 'id': 'acct-' + account['transport']}, stop=stop)

    def test_the_read_rate_and_page_come_from_slack_limits_per_transport(self):
        from machine.sources import slack
        self.assertEqual(slack.slack_limits(BROKER), slack.SLACK_LIMITS['broker'])
        self.assertEqual(slack.slack_limits(MATON), slack.SLACK_LIMITS['maton'])
        self.assertEqual((self.slack(BROKER).read_seconds, self.slack(MATON).read_seconds), (180, 180))
        self.assertEqual(self.slack(BROKER, {'slack_read_seconds': 30}).read_seconds, 65)  # never under Slack's own minute
        # Once the app is in the Slack Marketplace, its row is the only change: Maton accounts keep their pace
        faster = {**slack.SLACK_LIMITS, 'broker': {'read_seconds': 2, 'floor': 1, 'page': 200}}
        with patch.object(slack, 'SLACK_LIMITS', faster):
            fast, maton = self.slack(BROKER), self.slack(MATON)
            self.assertEqual((fast.read_seconds, fast.slots, maton.read_seconds), (2, 1, 180))
            self.assertEqual((slack.slack_limits(BROKER)['page'], slack.slack_limits(MATON)['page']), (200, 15))

    def test_a_history_read_waits_its_round_and_a_conversation_list_its_tier(self):
        source = self.slack(BROKER)
        source.pace('conversations.history')
        self.assertGreaterEqual(self.waits[-1], 64)  # never two reads in Slack's minute, after a restart too
        source.pace('users.conversations')
        self.assertEqual(self.waits[-1], 3.5)  # Tier 2: 20 a minute
        source.pace('conversations.info')
        self.assertEqual(self.waits[-1], 2.0)

    def test_a_429_waits_slacks_retry_after_and_moves_the_round(self):
        source = self.slack(BROKER)
        source.request = lambda method, values, fresh=False: urllib.request.Request('https://slack.com/api/' + method)
        error = urllib.error.HTTPError('https://slack.com/api/conversations.history', 429, 'limited', {'Retry-After': '120'}, None)
        with patch.object(source, 'pace'), patch('urllib.request.urlopen', side_effect=error):
            with self.assertRaises(a.SourceError) as caught:
                source.get('conversations.history', {'channel': 'C0GENERAL'})
        self.assertEqual(caught.exception.status, 429)
        self.assertTrue(125 <= caught.exception.retry_after <= 180)  # Slack's 120 s plus a spread, never sooner
        self.assertEqual(source.round, 360)  # the next read waits a longer round


if __name__ == '__main__':
    unittest.main()

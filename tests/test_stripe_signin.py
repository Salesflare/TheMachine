"""Sign in with Stripe (connectors/stripe.py, transport broker) and sharing it with a Work Fleet (shared_connectors.py).
Every HTTP request is faked: nothing reaches Stripe or a broker. Only GETs go to Stripe; the sign-in goes to the broker
only, rolls on every refresh, and never leaves this Machine. Teammates get access tokens that run out within the hour,
sent again fresh before they do, and nothing to replace when someone leaves."""
import json
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from pathlib import Path
from unittest.mock import patch

import fleet_trust as ft  # noqa: F401  (the grant checks the receivers run)
import mail_grants
import onboarding
import shared_connectors
from connectors import stripe
from test_connectors import a, Response
from test_shared_connectors import FLEET, FakeNetwork, FakeRelay

ACCOUNT = {'id': 'billing', 'service': 'stripe', 'transport': 'broker', 'boundary': 'work:Acme', 'stripe_account': 'acct_1AbCdEf',
           'account_name': 'Acme Billing', 'poll_seconds': 900}
EVENT = {'id': 'evt_1', 'type': 'invoice.payment_failed', 'created': 1792000000, 'livemode': True,
         'data': {'object': {'id': 'in_1', 'customer': 'cus_1', 'customer_email': 'pay@client.example', 'customer_name': 'Client Co',
                             'amount_due': 4900, 'currency': 'eur', 'attempt_count': 1}}}


class Broker(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'stripe_broker': {'url': 'https://cp.example/api/stripe/token'}}
        mail_grants.put(self.config, 'stripe', 'acct_1abcdef', 'srt_1')
        stripe._tokens.clear()
        self.helpers = types.SimpleNamespace(SourceError=a.SourceError, iso=a.CONNECTOR_HELPERS.iso,
                                             credential=lambda config, name: 'app-token' if name == 'stripe-broker' else 1 / 0)
        self.broker_calls, self.calls, self.account_status, self.expired_once, self.broker_status = [], [], 200, False, 200
        patch('urllib.request.urlopen', side_effect=self.respond).start()
        self.addCleanup(patch.stopall)

    def respond(self, request, timeout):
        url = urllib.parse.urlsplit(request.full_url)
        if url.netloc == 'cp.example':
            self.assertEqual((request.get_method(), request.get_header('Authorization')), ('POST', 'Bearer app-token'))
            sent = json.loads(request.data)
            self.broker_calls.append(sent)
            if self.broker_status != 200:
                raise urllib.error.HTTPError(request.full_url, self.broker_status, 'no', {}, None)
            n = len(self.broker_calls)
            return Response(json.dumps({'access_token': f'sat_{n}', 'expires_in': 3600, 'refresh_token': f'srt_{n + 1}'}).encode())
        self.assertEqual(request.get_method(), 'GET')  # nothing is ever written to Stripe
        self.assertEqual(url.netloc, 'api.stripe.com')
        self.assertNotIn('srt_', request.full_url)
        self.assertTrue(request.get_header('Authorization').startswith('Bearer sat_'))
        self.calls.append(url.path)
        if self.expired_once:
            self.expired_once = False
            raise urllib.error.HTTPError(request.full_url, 401, 'expired', {}, None)
        if url.path == '/v1/account':
            if self.account_status != 200:
                raise urllib.error.HTTPError(request.full_url, self.account_status, 'no', {}, None)
            return Response(json.dumps({'id': 'acct_1AbCdEf'}).encode())
        if url.path == '/v1/events':
            return Response(json.dumps({'data': [EVENT], 'has_more': False}).encode())
        raise AssertionError(url.path)

    def test_it_reads_with_short_lived_tokens_and_keeps_the_rolled_sign_in(self):
        result = stripe.sync(self.store, self.config, ACCOUNT, self.helpers)
        self.assertEqual(result['events'], 1)
        self.assertEqual(self.broker_calls, [{'email': 'acct_1abcdef', 'refresh_token': 'srt_1'}])
        self.assertEqual(mail_grants.get(self.config, 'stripe', 'acct_1abcdef'), 'srt_2')  # Stripe rolled it: the new one is kept
        stripe.sync(self.store, self.config, ACCOUNT, self.helpers)
        self.assertEqual(len(self.broker_calls), 1)  # the access token lasts an hour: no refresh per run

    def test_an_access_token_that_ran_out_early_is_refreshed_once(self):
        stripe.broker_token(self.config, ACCOUNT, self.helpers)
        self.expired_once = True
        stripe.Source(self.config, ACCOUNT, self.helpers).get('v1/events')
        self.assertEqual([c['refresh_token'] for c in self.broker_calls], ['srt_1', 'srt_2'])

    def test_an_app_token_without_account_access_still_checks_out_and_another_account_does_not(self):
        self.account_status = 403
        stripe.Source(self.config, ACCOUNT, self.helpers).verify()
        pasted = {**ACCOUNT, 'transport': 'api', 'credential': 'stripe'}
        helpers = types.SimpleNamespace(**{**vars(self.helpers), 'credential': lambda config, name: 'sat_pasted'})
        with self.assertRaises(a.SourceError):  # a pasted key that can't read the account is still refused
            stripe.Source(self.config, pasted, helpers).verify()
        self.account_status = 200
        with self.assertRaisesRegex(a.SourceError, 'account_identity_mismatch'):  # the key reads another account
            stripe.Source(self.config, {**pasted, 'stripe_account': 'acct_other1'}, helpers).verify()

    def test_a_revoked_sign_in_asks_to_sign_in_again(self):
        self.broker_status = 401
        with self.assertRaisesRegex(a.SourceError, 'stripe_signin_expired'):
            stripe.broker_token(self.config, ACCOUNT, self.helpers)

    def test_only_the_allowed_paths(self):
        with self.assertRaisesRegex(a.SourceError, 'stripe_path_not_allowed'):
            stripe.Source(self.config, ACCOUNT, self.helpers).get('v1/refunds')

    def test_what_a_fleet_admin_shares_is_an_access_token_with_its_time_never_the_sign_in(self):
        token, left = stripe.share_token(self.config, ACCOUNT, self.helpers, min_left=2400)
        self.assertEqual(token, 'sat_1')
        self.assertGreater(left, 2400)
        self.assertEqual(stripe.share_token(self.config, ACCOUNT, self.helpers, min_left=2400)[0], 'sat_1')  # still fresh enough
        self.assertEqual(stripe.share_token(self.config, ACCOUNT, self.helpers, min_left=3550)[0], 'sat_2')  # not: a fresh one
        pasted = {**ACCOUNT, 'transport': 'api', 'credential': 'stripe'}
        helpers = types.SimpleNamespace(**{**vars(self.helpers), 'credential': lambda config, name: 'rk_live_fixture'})
        self.assertEqual(stripe.share_token(self.config, pasted, helpers), ('rk_live_fixture', None))  # a pasted key lasts


class DeviceSignIn(unittest.TestCase):
    """A paired self-hosted Machine's own Sign in with Stripe (onboarding.connect_grant): one account per Stripe account."""
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / 'fleet.token').write_text('fixture-device-token\n')
        self.path = root / 'config.json'
        self.path.write_text(json.dumps({'database': str(root / 'events.sqlite'), 'credentials': {'fleet': str(root / 'fleet.token')}, 'accounts': []}))
        self.answer = None
        patch.object(onboarding, 'assistant', return_value=a).start()
        patch.object(onboarding, 'check', side_effect=lambda config, account: self.answer).start()
        self.addCleanup(patch.stopall)

    def args(self, **change):
        return {'source': 'stripe', 'grant': {'provider': 'stripe', 'email': 'acct_1abcdef', 'refresh_token': 'srt_device', 'scopes': ['stripe_apps'], **change}}

    def test_it_adds_one_work_account_kept_here_and_refreshed_at_the_paired_control_plane(self):
        import fleet
        self.assertEqual(onboarding.connect_delivered(self.path, self.args())['ok'], True)
        config = json.loads(self.path.read_text())
        [account] = config['accounts']
        self.assertEqual((account['service'], account['transport'], account['stripe_account']), ('stripe', 'broker', 'acct_1abcdef'))
        self.assertTrue(account['boundary'].startswith('work'))
        self.assertNotIn('credential', account)
        self.assertEqual(config['stripe_broker'], {'url': fleet.NETWORK + '/api/fleet/stripe-token'})
        self.assertNotIn('srt_device', self.path.read_text())
        self.assertEqual(mail_grants.get(config, 'stripe', 'acct_1abcdef'), 'srt_device')
        onboarding.connect_delivered(self.path, self.args(refresh_token='srt_again'))  # signed in again: the same account
        self.assertEqual(len(json.loads(self.path.read_text())['accounts']), 1)

    def test_not_an_account_id_or_a_failed_check_leaves_nothing(self):
        with self.assertRaisesRegex(onboarding.SetupError, 'No Stripe sign-in'):
            onboarding.connect_delivered(self.path, self.args(email='dee@acme.example'))
        self.answer = 'stripe:HTTP_401'
        with self.assertRaisesRegex(onboarding.SetupError, 'did not check out'):
            onboarding.connect_delivered(self.path, self.args())
        config = json.loads(self.path.read_text())
        self.assertEqual(config['accounts'], [])
        self.assertIsNone(mail_grants.get(config, 'stripe', 'acct_1abcdef'))


class SharedStripe(unittest.TestCase):
    """The admin's Machine is the only one that refreshes; teammates get access tokens under the same grant."""
    def machine(self, me, stripe_account=False):
        import fleet
        root = Path(self.temp.name) / me
        root.mkdir(parents=True, exist_ok=True)
        config = {'database': str(root / 'events.sqlite'), 'network_keys': str(root / 'network-keys.json'), 'credentials': {},
                  'fleet': {'url': 'https://cp.example/api/fleet'},
                  'accounts': [{'id': 'work', 'email': me + '@acme.example', 'service': 'gmail', 'boundary': 'work:Acme'}]}
        if stripe_account:
            config['accounts'].append(dict(ACCOUNT))
        box = fleet.Fleet(a.Store(root / 'events.sqlite').connect, config, lambda: 'token', relay=FakeRelay(self.net, me))
        box.member_id = me
        box.save_config = lambda change, restart, me=me: self.restarts.append((me, restart))
        return box

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.net, self.restarts, self.clock, self.issued = FakeNetwork(), [], [1_800_000_000.0], []
        self.own, self.adm, self.mem = self.machine('own1', stripe_account=True), self.machine('adm2'), self.machine('mem3')
        self.boxes = [self.own, self.adm, self.mem]
        self.own.share_token = self.share_token
        patch.object(shared_connectors.time, 'time', side_effect=lambda: self.clock[0]).start()
        self.addCleanup(patch.stopall)
        self.everyone_sees()
        self.everyone_sees()
        prompt = next(p for p in self.own.shared_view()['prompts'] if p['kind'] == 'admin')
        self.own.share_ok(prompt['id'], 'yes')  # the owner's Machine confirms Ada as an admin
        self.everyone_sees()

    def everyone_sees(self, rounds=2):
        for _ in range(rounds):
            for box in self.boxes:
                box.directory(refresh=True)
                box.shared_round()

    def share_token(self, service, account, min_left=0):
        """As connectors/stripe.share_token: the cached access token while it has more than min_left, else a fresh one."""
        self.assertEqual((service, account['transport']), ('stripe', 'broker'))
        if not self.issued or self.issued[-1][1] - self.clock[0] <= min_left:
            self.issued.append((f'sat_fixture_{len(self.issued) + 1}', self.clock[0] + 3480))
        token, until = self.issued[-1]
        return token, int(until - self.clock[0])

    def rounds(self, n=3):
        for _ in range(n):
            for box in self.boxes:
                if box.member_id in self.net.people:
                    box.directory(refresh=True)
                    box.step(wait=0)

    def held(self, box):
        return next((x for x in box.config['accounts'] if x.get('service') == 'stripe' and x.get('shared') and not x['shared'].get('origin')), None)

    def token_of(self, box):
        account = self.held(box)
        return Path(box.config['credentials'][account['credential']]).read_text().strip() if account else None

    def test_shared_once_teammates_read_it_and_get_a_fresh_token_before_theirs_runs_out(self):
        self.own.share('billing', FLEET, ['mem3'])
        self.rounds()
        for box in (self.adm, self.mem):
            account = self.held(box)
            self.assertEqual((account['transport'], account['stripe_account'], account['account_name'], account['boundary']),
                             ('api', 'acct_1AbCdEf', 'Acme Billing', 'work:Acme'))
            self.assertEqual(self.token_of(box), 'sat_fixture_1')
        view = self.mem.shared_view()['shares'][0]
        self.assertEqual((view['label'], view['workspace'], view['by'], view['admin']), ('Stripe', 'Acme Billing', 'Olive', False))
        grant = self.held(self.mem)['shared']['grant']
        sent = len(self.net.asks)
        self.clock[0] += 20 * 60  # theirs has 38 minutes left: nothing goes
        self.rounds()
        self.assertEqual(len(self.net.asks), sent)
        self.clock[0] += 20 * 60  # 18 minutes left: a fresh one, under the same grant, without a restart
        self.restarts.clear()
        self.rounds()
        for box in (self.adm, self.mem):
            self.assertEqual(self.token_of(box), 'sat_fixture_2')
            self.assertEqual(self.held(box)['shared']['grant'], grant)
        self.assertFalse([r for r in self.restarts if r[0] != 'own1' and r[1]])
        dump = json.dumps(self.net.calls)
        self.assertNotIn('sat_', dump)  # the Network never sees a token, sealed envelopes included
        self.assertNotIn('srt_', dump)
        self.assertEqual(a.reconnect_help(self.held(self.mem), None), {'shared_by': 'Acme'})  # members can't change it

    def test_someone_who_leaves_leaves_nothing_to_replace(self):
        self.own.share('billing', FLEET, ['mem3'])
        self.rounds()
        del self.net.people['mem3']
        self.rounds()
        self.assertFalse([p for p in self.own.shared_view()['prompts'] if p['kind'] == 'replace'])  # theirs runs out within the hour

    def test_only_a_connected_intercom_or_stripe_account_is_shared(self):
        with self.assertRaisesRegex(ValueError, 'Intercom or Stripe'):
            self.own.share('work', FLEET, [])
        self.own.share_token = lambda service, account, min_left=0: (None, None)  # the sign-in doesn't work now
        with self.assertRaisesRegex(ValueError, 'Connect it first'):
            self.own.share('billing', FLEET, [])


if __name__ == '__main__':
    unittest.main()

"""One-click pairing (pairing.py) and the address for AIs in Settings, AIs (ai_app.ai_reach): the signed request and
pickup, the sealed token opened only for this request, the token file 0600 and the config like `cli.py fleet-pair`,
the Fleet starting live without a restart, and Unpair."""
import importlib.util
import json
import stat
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import fleet
import network_crypto as nc
import pairing

spec = importlib.util.spec_from_file_location('pairing_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

RID = 'R' * 22
PAGE = 'https://app.themachine.computer/pair/' + RID


def verify(body, prefix):
    signed = {k: v for k, v in body.items() if k not in ('sig', 'keys_sig')}
    message = prefix + json.dumps(signed, sort_keys=True, separators=(',', ':')).encode()
    return nc.ed25519_verify(nc.unb64(body['sign'], 32), message, nc.unb64(body['sig'], 64))


class Base(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.config_path = self.dir / 'config.json'
        self.config = {'database': str(self.dir / 'events.sqlite'), 'accounts': [], 'credentials': {}}
        self.config_path.write_text(json.dumps(self.config))
        self.private = pairing.keys(self.config)
        self.public = nc.public_keys(self.private)
        self.posts = []

    def sealed(self, token='fd_' + 'x' * 40, rid=RID):
        return nc.seal_box({'token': token, 'device': 'dev_1', 'label': 'Desk'}, nc.unb64(self.public['box'], 32),
                           {'p': 'pair', 'r': rid}, info=pairing.BOX_INFO)

    def post(self, answers):
        def post(path, body):
            self.posts.append((path, body))
            found = answers[path]
            return found.pop(0) if isinstance(found, list) else found
        return post


class Pairing(Base):
    def test_the_request_is_signed_with_this_machines_key_and_carries_its_keys(self):
        made = pairing.start(self.config, 'Desk', post=self.post({'/pair-request': {'id': RID, 'url': PAGE, 'code': 'X', 'expires_in': 600}}))
        path, body = self.posts[0]
        self.assertEqual(path, '/pair-request')
        self.assertEqual((body['sign'], body['box'], body['keys_sig']), (self.public['sign'], self.public['box'], self.public['sig']))
        self.assertTrue(verify(body, pairing.REQUEST_PREFIX))
        body['label'] = 'Other'
        self.assertFalse(verify(body, pairing.REQUEST_PREFIX))
        self.assertEqual((made['id'], made['url']), (RID, PAGE))
        self.assertRegex(made['code'], r'^[A-Z2-7]{4}-[A-Z2-7]{4}$')

    def test_only_the_accounts_own_pair_page_is_opened(self):
        for url in ('https://evil.example/pair/' + RID, 'http://app.themachine.computer/pair/' + RID,
                    'https://app.themachine.computer/pair/other', PAGE + '?x=1'):
            with self.assertRaises(ValueError):
                pairing.start(self.config, 'Desk', post=self.post({'/pair-request': {'id': RID, 'url': url}}))

    def test_pickup_is_signed_and_opens_the_token_only_for_this_request(self):
        post = self.post({'/pair-pickup': [{'state': 'waiting'}, {'state': 'paired', 'sealed': self.sealed()},
                                           {'state': 'paired', 'sealed': self.sealed(rid='O' * 22)}]})
        self.assertEqual(pairing.pickup(self.config, RID, post=post), {'state': 'waiting'})
        got = pairing.pickup(self.config, RID, post=post)
        self.assertEqual((got['state'], got['token'], got['device']), ('paired', 'fd_' + 'x' * 40, 'dev_1'))
        self.assertEqual(pairing.pickup(self.config, RID, post=post), {'state': 'gone'})  # sealed for another request
        body = self.posts[0][1]
        message = pairing.PICKUP_PREFIX + json.dumps({k: body[k] for k in ('id', 'nonce', 'at')}, sort_keys=True, separators=(',', ':')).encode()
        self.assertTrue(nc.ed25519_verify(nc.unb64(self.public['sign'], 32), message, nc.unb64(body['sig'], 64)))

    def test_the_token_is_kept_0600_and_in_the_config_like_the_cli(self):
        path = pairing.keep(self.config, self.config_path, 'fd_secret')
        self.assertEqual(path, self.dir / 'fleet-token')
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertEqual(path.read_text().strip(), 'fd_secret')
        self.assertEqual(json.loads(self.config_path.read_text())['credentials']['fleet'], str(path))
        self.assertEqual(self.config['credentials']['fleet'], str(path))
        pairing.forget(self.config, self.config_path)
        self.assertFalse(path.exists())
        self.assertNotIn('fleet', json.loads(self.config_path.read_text())['credentials'])


class FakeRelay:
    def __init__(self, answer):
        self.answer, self.calls = answer, []

    def call(self, method, path, body=None, timeout=40):
        self.calls.append((method, path, body))
        return self.answer


class App(Base):
    def setUp(self):
        super().setUp()
        self.app = object.__new__(a.App)
        self.app.store = a.Store(self.config['database'])
        self.app.config, self.app.config_path, self.app.stop = self.config, self.config_path, threading.Event()
        self.started = []

    def thread(self, target=None, name=None, **kw):
        started = self.started

        class Fake:
            def start(self):
                started.append(name)
        return Fake()

    def test_hosted_shows_its_name_on_the_mcp_host(self):
        self.config.update(manage_url='https://app.themachine.computer/setup', dashboard_host='pat.app.themachine.computer')
        reach = self.app.ai_reach()
        self.assertEqual(reach['address'], 'https://pat.mcp.themachine.computer/mcp')
        self.assertTrue(reach['hosted'])

    def test_not_paired_then_get_your_address_pairs_and_starts_the_fleet_live(self):
        self.app.fleet = None
        self.assertEqual(self.app.ai_reach(), {'hosted': False, 'paired': False, 'name': None, 'address': None, 'shared': None, 'pairing': None})
        with patch.object(pairing, '_post', self.post({'/pair-request': {'id': RID, 'url': PAGE, 'expires_in': 600},
                                                      '/pair-pickup': [{'state': 'waiting'}, {'state': 'paired', 'sealed': self.sealed()}]})), \
                patch.object(a.threading, 'Thread', self.thread), patch('ai_app.threading.Thread', self.thread):
            out = self.app.action('ai_pair_start', {}, owner_dashboard=True)
            self.assertEqual((out['url'], out['state']), (PAGE, 'waiting'))
            self.assertEqual(self.app.action('ai_pair_state', {}, owner_dashboard=True)['state'], 'waiting')
            guard = threading.Lock()
            guard.acquire()
            self.app.ai_pair_watch(guard, wait=lambda s: None)
        self.assertIsNotNone(self.app.fleet)  # live, no restart
        self.assertEqual(self.started[:3], ['pair-watch', 'fleet', 'bug-queue'])  # and mcp-reach with cryptography (test_ai_reach)
        self.assertEqual(stat.S_IMODE((self.dir / 'fleet-token').stat().st_mode), 0o600)
        self.assertEqual(json.loads(self.config_path.read_text())['credentials']['fleet'], str(self.dir / 'fleet-token'))
        self.app.fleet.relay = FakeRelay({'username': 'pat', 'hosted': False})
        state = self.app.action('ai_pair_state', {'fresh': True}, owner_dashboard=True)
        self.assertEqual((state['state'], state['reach']['address']), ('paired', 'https://pat.mcp.themachine.computer/mcp'))

    def test_a_page_nobody_confirmed_ends(self):
        self.app.fleet = None
        with patch.object(pairing, '_post', self.post({'/pair-request': {'id': RID, 'url': PAGE}, '/pair-pickup': {'state': 'gone'}})), \
                patch('ai_app.threading.Thread', self.thread):
            self.app.action('ai_pair_start', {}, owner_dashboard=True)
            guard = threading.Lock()
            guard.acquire()
            self.app.ai_pair_watch(guard, wait=lambda s: None)
        self.assertIsNone(self.app.fleet)
        self.assertEqual(self.app.ai_reach()['pairing']['state'], 'gone')
        self.assertFalse((self.dir / 'fleet-token').exists())

    def test_paired_without_a_name_goes_to_the_account_and_unpair_drops_the_token(self):
        pairing.keep(self.config, self.config_path, 'fd_secret')
        self.app.fleet = object.__new__(fleet.Fleet)
        self.app.fleet.relay = relay = FakeRelay({'username': None})
        reach = self.app.ai_reach()
        self.assertEqual((reach['paired'], reach['address']), (True, None))
        self.assertEqual(self.app.action('ai_pair_start', {}, owner_dashboard=True)['state'], 'name')
        with self.assertRaises(ValueError):
            self.app.action('ai_pair_start', {}, owner_dashboard=False)  # the owner's own, from the dashboard
        view = self.app.action('ai_unpair', {}, owner_dashboard=True)
        self.assertIn(('POST', '/ai-reach', {'on': False}), relay.calls)
        self.assertIsNone(self.app.fleet)
        self.assertFalse(view['reach']['paired'])
        self.assertFalse((self.dir / 'fleet-token').exists())
        self.assertNotIn('fleet', json.loads(self.config_path.read_text())['credentials'])

    def test_the_account_away_says_so(self):
        self.app.fleet = object.__new__(fleet.Fleet)

        class Away:
            def call(self, *args, **kwargs):
                raise fleet.Unavailable('away')
        self.app.fleet.relay = Away()
        self.assertTrue(self.app.ai_reach()['away'])


if __name__ == '__main__':
    unittest.main()

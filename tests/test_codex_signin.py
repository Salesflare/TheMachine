"""Codex in Connections (codex_signin.py): + Add has a Codex tile that says whether Codex is signed in, and a
self-hosted Machine runs Codex's own device sign-in (`codex login --device-auth`) for the dashboard to show its code.
A hosted Machine runs Codex where the setup page says: on the Machine itself by default ('machine'). The Codex CLI is a
stub here: no real sign-in, nothing leaves this computer."""
import json
import os
import stat
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import agent_jobs
import agent_remote
import assistant
import codex_signin

# A stand-in for the Codex CLI: `login status` reads a file, `login --device-auth` prints what the real one prints and
# signs in once the test drops the "approved" file (or gives up when it drops "denied").
STUB = r"""#!/usr/bin/env python3
import os, sys, time
home = os.environ['STUB_CODEX_HOME']
args = sys.argv[1:]
open(os.path.join(home, 'calls'), 'a').write(' '.join(args) + '\n')
if args == ['login', 'status']:
    if os.path.exists(os.path.join(home, 'signed-in')):
        print('Logged in using ChatGPT'); sys.exit(0)
    print('Not logged in'); sys.exit(1)
if args == ['login', '--device-auth']:
    print('Follow these steps to sign in with ChatGPT using device code authorization:', flush=True)
    print('1. Open this link in your browser and sign in to your account\n   https://auth.openai.com/codex/device', flush=True)
    print('2. Enter this one-time code (expires in 15 minutes)\n   ABCD-EFGH2', flush=True)
    for _ in range(500):
        if os.path.exists(os.path.join(home, 'approved')):
            open(os.path.join(home, 'signed-in'), 'w').write('1'); print('Successfully logged in'); sys.exit(0)
        if os.path.exists(os.path.join(home, 'denied')):
            print('Error logging in with device code: denied'); sys.exit(1)
        time.sleep(0.02)
    sys.exit(1)
sys.exit(2)
"""


class StubCodex(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.codex = self.home / 'codex'
        self.codex.write_text(STUB)
        self.codex.chmod(self.codex.stat().st_mode | stat.S_IEXEC)
        patch.dict(os.environ, {'STUB_CODEX_HOME': str(self.home)}).start()
        patch.object(agent_jobs, 'DESKTOP_CODEX', ()).start()  # never the real Codex app's codex
        self.addCleanup(patch.stopall)
        self.config = {'accounts': [], 'agents': {'codex': {'command': str(self.codex)}}}
        codex_signin.forget()

    def wait(self, signin, state):
        for _ in range(400):
            if signin.view()['state'] == state:
                return signin.view()
            time.sleep(0.02)
        self.fail('never ' + state + ': ' + json.dumps(signin.view()))


class Signing(StubCodex):
    def test_the_code_and_openai_s_page_then_signed_in(self):
        self.assertEqual(codex_signin.status(self.config), 'signed_out')
        signin = codex_signin.Signin()
        self.assertEqual(signin.start(self.config)['state'], 'starting')
        self.assertEqual(self.wait(signin, 'code'), {'state': 'code', 'code': 'ABCD-EFGH2', 'url': 'https://auth.openai.com/codex/device'})
        self.assertEqual(signin.start(self.config)['code'], 'ABCD-EFGH2')  # pressed again: the same sign-in
        (self.home / 'approved').write_text('1')
        self.wait(signin, 'done')
        self.assertEqual(codex_signin.status(self.config), 'connected')
        self.assertEqual((self.home / 'calls').read_text().count('login --device-auth'), 1)
        self.assertEqual(signin.start(self.config), {'state': 'done'})  # signed in already: no new code

    def test_a_code_never_approved_says_so(self):
        signin = codex_signin.Signin()
        signin.start(self.config)
        self.wait(signin, 'code')
        (self.home / 'denied').write_text('1')
        self.assertEqual(self.wait(signin, 'failed')['error'], 'The sign-in code expired or was not approved.')

    def test_no_codex_here_says_how_to_get_it(self):
        with patch.object(agent_jobs, 'find', return_value=None):
            self.assertIsNone(codex_signin.status({'accounts': []}))
            self.assertEqual(codex_signin.Signin().start({'accounts': []}), {'state': 'missing'})


class Connections(StubCodex):
    def app(self, config):
        app = object.__new__(assistant.App)
        app.config, app.config_path = config, self.home / 'config.json'
        app.config_path.write_text(json.dumps(config))
        return app

    def test_add_has_a_codex_tile_with_its_status_and_signs_in_here(self):
        app = self.app(self.config)
        found = app.action('connect_sources', {}, owner_dashboard=True)
        self.assertEqual(found['codex'], {'status': 'signed_out'})
        self.assertEqual(app.action('codex_signin', {}, owner_dashboard=True)['state'], 'starting')
        for _ in range(400):
            if app.action('codex_signin_state', {}, owner_dashboard=True)['state'] == 'code':
                break
            time.sleep(0.02)
        (self.home / 'approved').write_text('1')
        for _ in range(400):
            if app.action('codex_signin_state', {}, owner_dashboard=True)['state'] == 'done':
                break
            time.sleep(0.02)
        self.assertEqual(app.action('connect_sources', {}, owner_dashboard=True)['codex'], {'status': 'connected'})
        self.assertIn('codex_signin', assistant.DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            app.action('codex_signin', {}, owner_dashboard=False)  # the owner's dashboard only

    def test_a_hosted_machine_signs_in_through_its_account(self):
        app = self.app({**self.config, 'manage_url': 'https://app.example.test/setup'})
        self.assertIn('codex', assistant.HOSTED_SIGNINS)
        self.assertIn('codex', assistant.ON_DASHBOARD)
        self.assertEqual(app.action('connect_sources', {}, owner_dashboard=True)['codex'], {'status': 'signed_out'})
        with self.assertRaises(ValueError):
            app.action('codex_signin', {}, owner_dashboard=True)  # the control plane runs it on the server
        self.assertFalse((self.home / 'calls').read_text().count('device-auth'))

    def test_coding_agents_off_means_no_tile(self):
        app = self.app({'accounts': [], 'agents': False})
        self.assertNotIn('codex', app.action('connect_sources', {}, owner_dashboard=True))


class WhereCodexRuns(StubCodex):
    HOSTED = {'manage_url': 'https://app.example.test/setup'}

    def test_on_your_machine_runs_the_servers_own_codex(self):
        config = {**self.HOSTED, 'agents': {'codex': {'command': str(self.codex)}}}
        self.assertEqual([t for t in agent_jobs.tools(config, {'codex': 'machine', 'devices': []}) if t['id'] == 'codex'],
                         [{'id': 'codex', 'name': 'Codex', 'place': 'local'}])
        # Codex cloud set up on purpose stays Codex cloud
        cloud = {**self.HOSTED, 'agents': {'codex': {'command': str(self.codex), 'place': 'cloud', 'env': 'env_1'}}}
        self.assertEqual([t['place'] for t in agent_jobs.tools(cloud, {'codex': 'machine'}) if t['id'] == 'codex'], ['cloud'])
        # not on the server yet: no Hand to Codex until it is
        with patch.object(agent_jobs, 'find', return_value=None):
            self.assertEqual([t for t in agent_jobs.tools(self.HOSTED, {'codex': 'machine'}) if t['id'] == 'codex'], [])

    def test_the_network_s_answer_keeps_machine(self):
        class Jobs:
            config = {}

            def network(self, body):
                return {'codex': 'machine', 'devices': []}
        self.assertEqual(agent_remote.where(Jobs())['codex'], 'machine')

    def test_settings_say_it_runs_on_the_machine(self):
        app = object.__new__(assistant.App)
        app.config = {**self.HOSTED, 'accounts': [{'id': 'acme-github', 'service': 'github'}]}
        app.config_path = None
        app.agents = type('Agents', (), {'where': lambda self: {'codex': 'machine', 'devices': []}})()
        view = app.agents_view()
        self.assertEqual((view['codex_where'], view['codex_device']), ('machine', ''))


if __name__ == '__main__':
    unittest.main()

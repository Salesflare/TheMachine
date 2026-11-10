"""A reconnect that worked ends the sign-in problem at once (the Needs you line and the error on the card), for every
account on that sign-in; and a restart the page was told of shows as the Machine restarting, not offline."""
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('assistant', ROOT / 'assistant.py')
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

GMAIL = {'id': 'work-gmail', 'email': 'Owner@example.com', 'client': 'existing', 'transport': 'gog', 'service': 'gmail'}
CALENDAR = {'id': 'work-calendar', 'email': 'owner@example.com', 'client': 'existing', 'transport': 'gog', 'service': 'calendar'}
SHARED = {'id': 'family-calendar', 'email': 'owner@example.com', 'client': 'existing', 'transport': 'gog', 'service': 'calendar', 'calendar_id': 'family@example.com'}
OTHER = {'id': 'other-gmail', 'email': 'someone@example.com', 'client': 'existing', 'transport': 'gog', 'service': 'gmail'}
SLACK = {'id': 'work-slack', 'email': 'owner@example.com', 'service': 'slack'}


class SignedInAgain(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = assistant.Store(Path(self.temp.name) / 'events.sqlite')
        self.accounts = [GMAIL, CALENDAR, SHARED, OTHER, SLACK]

    def error(self, account):
        with self.store.connect() as db:
            row = db.execute('SELECT error, retry_at FROM checkpoints WHERE account_id=?', (account,)).fetchone()
        return row and (row['error'], row['retry_at'])

    def test_a_401_is_a_sign_in_error(self):
        for text in ('gmail:HTTP_401', 'calendar:google_signin_expired_run_gog_auth_add', 'outlook:microsoft_signin_expired'):
            self.assertTrue(re.search(assistant.SIGNIN_ERROR, text), text)
        for text in ('gmail:HTTP_403', 'gmail:HTTP_4010', 'trello_http:HTTP_401', 'calendar:timeout', 'gmail:HTTP_503'):
            self.assertFalse(re.search(assistant.SIGNIN_ERROR, text), text)

    def test_reconnect_clears_its_own_error_and_its_siblings_sign_in_errors_only(self):
        self.store.failed(GMAIL['id'], assistant.SourceError('gmail:HTTP_401', retry_after=300))
        self.store.failed(CALENDAR['id'], assistant.SourceError('calendar:HTTP_401', retry_after=300))
        self.store.failed(SHARED['id'], assistant.SourceError('calendar:timeout', retry_after=300))  # not the sign-in: stays
        self.store.failed(OTHER['id'], assistant.SourceError('gmail:HTTP_401', retry_after=300))  # another address: stays
        self.store.failed(SLACK['id'], assistant.SourceError('slack_signin_expired', retry_after=300))  # another sign-in: stays
        ids = assistant.same_signin(self.accounts, GMAIL, self.store)
        self.assertEqual(ids, ['work-gmail', 'work-calendar'])
        self.store.signed_in_again(ids)
        self.assertEqual(self.error('work-gmail'), (None, None))
        self.assertEqual(self.error('work-calendar'), (None, None))
        self.assertEqual(self.error('family-calendar')[0], 'calendar:timeout')
        self.assertEqual(self.error('other-gmail')[0], 'gmail:HTTP_401')
        self.assertEqual(self.error('work-slack')[0], 'slack_signin_expired')
        status = {c['id']: c for c in self.store.snapshot([{**a, 'boundary': 'work:Acme'} for a in self.accounts])['connectors']}
        self.assertFalse(status['work-gmail'].get('error'))  # the Needs you line goes with it
        self.assertFalse(status['work-calendar'].get('error'))
        self.assertTrue(status['other-gmail'].get('error'))

    def test_the_web_reconnect_clears_it_before_the_restart(self):
        self.store.failed(GMAIL['id'], assistant.SourceError('gmail:HTTP_401', retry_after=300))
        self.store.failed(CALENDAR['id'], assistant.SourceError('calendar:HTTP_401', retry_after=300))
        app = object.__new__(assistant.App)
        app.config, app.store, app.config_path = {'accounts': self.accounts}, self.store, Path(self.temp.name) / 'config.json'
        import google_pair
        import onboarding
        session = {'source': 'gmail', 'account_id': GMAIL['id'], 'ui': onboarding.WebUI()}
        cleared = []
        with patch.object(google_pair, 'connect', return_value=GMAIL), \
                patch_everywhere(assistant, 'restart_self', side_effect=lambda _: cleared.append(self.error('work-calendar')) or True):
            app.connect_run(session)
        self.assertEqual(session['state'], 'done')
        self.assertTrue(session['restarting'])
        self.assertEqual(cleared, [(None, None)])  # cleared before the service restarts: the page shows it at once
        self.assertEqual(self.error('work-gmail'), (None, None))

    def test_a_new_connect_clears_nothing(self):
        self.store.failed(CALENDAR['id'], assistant.SourceError('calendar:HTTP_401', retry_after=300))
        app = object.__new__(assistant.App)
        app.config, app.store, app.config_path = {'accounts': self.accounts}, self.store, Path(self.temp.name) / 'config.json'
        import onboarding
        session = {'source': 'gmail', 'account_id': None, 'ui': onboarding.WebUI()}
        with patch.object(onboarding, 'connect', return_value=GMAIL), patch_everywhere(assistant, 'restart_self', return_value=True):
            app.connect_run(session)
        self.assertEqual(self.error('work-calendar')[0], 'calendar:HTTP_401')

    def test_a_401_retries_as_soon_as_the_owner_signs_in_again(self):
        keyring = Path(self.temp.name) / 'keyring'; keyring.mkdir()
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {'gog_keyring_dir': str(keyring)}, self.store, threading.Event()
        with patch_everywhere(assistant, 'now', return_value='2026-11-04T21:20:36+00:00'):
            self.store.failed(GMAIL['id'], assistant.SourceError('gmail:HTTP_401', retry_after=300))
        with self.store.connect() as db:
            row = db.execute('SELECT retry_at,error,error_at FROM checkpoints WHERE account_id=?', (GMAIL['id'],)).fetchone()
        token = assistant.gog_token_path(app.config, GMAIL)
        token.write_text('old'); os.utime(token, (0, 0))
        waits = []

        def wait(seconds):
            waits.append(seconds)
            token.write_text('new')  # signed in again meanwhile
            return False
        app.stop.wait = wait
        with patch_everywhere(assistant, 'now', return_value='2026-11-04T21:21:00+00:00'):
            self.assertFalse(app.wait_for_retry(GMAIL, row))
        self.assertEqual(waits, [15])  # watched, not slept for the whole retry


class RestartAnnounced(unittest.TestCase):
    """dashboard/shell-network.js: a self-hosted Machine has nothing in front of it that answers "restarting" while
    its service restarts (a refused connection, or the proxy's HTML 502). A restart the page was told of says so."""
    def run_js(self, body):
        source = (ROOT / 'dashboard' / 'shell-network.js').read_text(encoding='utf-8')
        head = source[:source.index('let retryIn=0')]
        script = ('let csrf="x",netDown=false,netSetup=false;const errApi=()=>{},setupUnderway=()=>false,slowSet=()=>{};' + head +
                  ';(async()=>{const out=[];' + body + ';console.log(JSON.stringify(out))})()')
        return json.loads(subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True).stdout)

    def test_refused_and_html_502_count_as_restarting_only_once_announced(self):
        out = self.run_js(
            'const refused=()=>Promise.reject(new TypeError("Failed to fetch")),'
            'html502=()=>Promise.resolve({status:502,ok:false,type:"basic",headers:{get:k=>k==="content-type"?"text/html":null}});'
            'const tryIt=async f=>{globalThis.fetch=f;try{await request("api/status")}catch(e){return [!!e.offline,!!e.restarting]}};'
            'out.push(await tryIt(refused),await tryIt(html502));restartSoon();out.push(await tryIt(refused),await tryIt(html502));'
            'restartUntil=Date.now()-1;out.push(await tryIt(refused))')
        self.assertEqual(out, [[True, False], [True, False], [True, True], [True, True], [True, False]])

    def test_the_connect_results_that_restart_announce_it(self):
        source = (ROOT / 'dashboard' / 'connections-cards.js').read_text(encoding='utf-8')
        self.assertIn("connectPost('connect_remove',{account:b.dataset.disconnect});if(r.restarting)restartSoon();", source)
        self.assertIn("connectPost('connect_scope',{account:s.dataset.scope,boundary:b});if(r.restarting)restartSoon();", source)
        self.assertIn("if(connectRun?.state==='done'&&(connectRun.restarting||connectRun.live)&&!connectRun.followed){connectRun.followed=true;if(connectRun.restarting)restartSoon();connectFollow(connectRun);return}", source)


if __name__ == '__main__':
    unittest.main()

"""Connections, + Add, picking up where the owner left off: a setup under way is found again (connect_running) after a
reload, in another tab or on the phone, at the same question; Cancel ends it at once, so nothing picks it up again.
Gmail through the owner's own Google app asks its two steps in the dashboard's own words, never a file path or a
command, and brings Google Calendar for the same address along in the same run. A fake gog: no live calls."""
import json
import subprocess
import tempfile
import time
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch

import assistant
import onboarding
from seams import patch_everywhere  # noqa: E402

GOG = '/fake/bin/gog'


class FakeGog:
    """gog as onboarding runs it: one OAuth client, no account until the remote sign-in's second step."""
    def __init__(self):
        self.signed_in, self.pending = set(), {}

    def __call__(self, args, **kwargs):
        args = [str(a) for a in args]
        out = lambda code, text='', err='': subprocess.CompletedProcess(args, code, text, err)
        if args[0] != GOG:
            return out(127, '', 'not here')
        rest = args[1:]
        if rest[:2] == ['auth', 'list']:
            return out(0, json.dumps({'accounts': [{'email': e, 'client': 'default'} for e in sorted(self.signed_in)]}))
        if rest[:3] == ['auth', 'credentials', 'list']:
            return out(0, json.dumps({'clients': [{'client': 'default', 'default': True}]}))
        if rest[:2] == ['auth', 'add'] and '--remote' in rest:
            email, step = rest[2], rest[rest.index('--step') + 1]
            if step == '1':
                state = f's{len(self.pending)}'
                self.pending[state] = email
                return out(0, 'Visit https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode({'state': state, 'login_hint': email}) + '\n')
            landed = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(rest[rest.index('--auth-url') + 1]).query))
            if self.pending.pop(landed.get('state'), None) != email or not landed.get('code'):
                return out(1, '', 'state mismatch')
            self.signed_in.add(email)
            return out(0, f'Authorized {email}\n')
        if rest[:2] == ['calendar', 'calendars']:
            return out(0, json.dumps([{'id': 'primary', 'summary': 'Mine', 'primary': True}]))
        return out(1, '', 'unsupported')


class ResumeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'config.json'
        self.path.write_text(json.dumps({'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite'), 'gog': GOG,
                                         'credentials': {'gog-password': str(Path(self.temp.name) / 'gog-password')}}))
        self.app = object.__new__(assistant.App)
        self.app.config, self.app.config_path = json.loads(self.path.read_text()), self.path
        self.gog = FakeGog()
        patch.object(onboarding, '_assistant', assistant).start()
        patch_everywhere(assistant, 'restart_self', return_value=True).start()
        patch.object(onboarding, 'tool', lambda config, name: GOG if name == 'gog' else None).start()
        patch.object(onboarding, 'run', self.gog).start()
        patch.object(onboarding, 'check', lambda config, account: None if account.get('email') in self.gog.signed_in else 'gmail_auth').start()
        self.addCleanup(patch.stopall)

    def act(self, name, args=None):
        return self.app.action(name, args or {}, owner_dashboard=True)

    def wait(self, view, until):
        for _ in range(400):
            if until(view):
                return view
            time.sleep(0.02)
            view = {**view, **self.act('connect_poll', {'session': view['session']})}
        self.fail('still waiting: ' + json.dumps(view))

    def start_gmail(self):
        view = self.act('connect_start', {'name': 'gmail', 'form': True, 'answers': {'email': 'jo@acme.example'}, 'scope': 'work', 'company': 'Acme'})
        return self.wait(view, lambda v: v.get('question') or v['state'] != 'running')

    def test_the_form_asks_the_google_address_so_the_setup_never_stops_for_it(self):
        forms = {s['name']: s['form'] for s in self.act('connect_sources')['sources']}
        self.assertEqual(forms['gmail']['ask'], [['email', 'Google account']])
        self.assertEqual(forms['calendar']['ask'], [['email', 'Google account']])

    def test_a_reload_finds_the_google_step_again_and_finishing_there_adds_gmail_and_calendar(self):
        self.assertEqual(self.act('connect_running'), {})
        view = self.start_gmail()
        q = view['question']
        self.assertEqual((q['prompt'], q['google']['email'], q['google']['again']), ('The address Google sent you to', 'jo@acme.example', False))
        self.assertTrue(q['google']['url'].startswith('https://accounts.google.com/'))
        for line in view['lines']:  # no file path, keyring or command: the dashboard says the steps itself
            self.assertNotRegex(line, r'keyring|/|gog|Open this address', line)

        again = self.act('connect_running')  # another tab, the phone, a reload: the same setup at the same question
        self.assertEqual((again['session'], again['question']['id'], again['question']['google']['url']), (view['session'], q['id'], q['google']['url']))

        state = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(q['google']['url']).query))['state']
        view = self.act('connect_answer', {'session': again['session'], 'question': q['id'], 'value': f'http://127.0.0.1:1/oauth2/callback?state={state}&code=c'})
        view = self.wait({**view, 'session': again['session']}, lambda v: v['state'] != 'running')
        self.assertEqual(view['state'], 'done', view)
        saved = {a['service']: a for a in json.loads(self.path.read_text())['accounts']}
        self.assertEqual(sorted(saved), ['calendar', 'gmail'])
        self.assertEqual({(a['email'], a['boundary']) for a in saved.values()}, {('jo@acme.example', 'work:Acme')})
        self.assertFalse([line for line in view['lines'] if 'authorized' in line or 'keyring' in line])
        self.assertEqual(self.act('connect_running'), {})

    def test_a_calendar_already_there_is_left_as_it_is(self):
        config = json.loads(self.path.read_text())
        config['accounts'] = [{'id': 'acme-calendar', 'service': 'calendar', 'transport': 'gog', 'client': 'default', 'email': 'jo@acme.example', 'boundary': 'work:Acme'}]
        self.path.write_text(json.dumps(config))
        self.gog.signed_in.add('jo@acme.example')
        Path(config['credentials']['gog-password']).write_text('kept\n')  # the keyring's, from that first sign-in
        view = self.start_gmail()
        self.assertEqual(view['state'], 'done', view)
        services = [a['service'] for a in json.loads(self.path.read_text())['accounts']]
        self.assertEqual(sorted(services), ['calendar', 'gmail'])

    def test_cancel_ends_it_at_once_and_nothing_picks_it_up_again(self):
        view = self.start_gmail()
        stopped = self.act('connect_cancel', {'session': view['session']})
        self.assertEqual(stopped['state'], 'cancelled')
        self.assertEqual(self.act('connect_running'), {})
        self.wait({**stopped, 'session': view['session']}, lambda v: v.get('error'))  # the run winds down by itself
        self.assertEqual(json.loads(self.path.read_text())['accounts'], [])


if __name__ == '__main__':
    unittest.main()

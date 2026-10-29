"""Connections, + Add as the account's setup page: one form per source (onboarding.web_form), Work or Personal as two
choices, LinkedIn and X signed in right there while their connect waits, and GitHub's and WhatsApp's codes shown on the
dashboard, so nothing asks for work:<Company> or a command in a terminal."""
import json
import stat
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant
import onboarding

ACCOUNTS = [{'id': 'acme-gmail', 'service': 'gmail', 'email': 'owner@acme.example', 'boundary': 'work:Acme', 'boundary_by': 'owner'},
            {'id': 'acme-slack', 'service': 'slack', 'boundary': 'work:Acme'}]


class FormTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'config.json'
        self.path.write_text(json.dumps({'accounts': ACCOUNTS, 'database': str(Path(self.temp.name) / 'events.sqlite'),
                                         'credentials': {}}))
        self.app = object.__new__(assistant.App)
        self.app.config, self.app.config_path = json.loads(self.path.read_text()), self.path
        patch.object(onboarding, '_assistant', assistant).start()
        patch.object(assistant, 'restart_self', return_value=True).start()
        self.addCleanup(patch.stopall)

    def act(self, name, args):
        return self.app.action(name, args, owner_dashboard=True)

    def finish(self, view, until=lambda v: v['state'] != 'running'):
        for _ in range(400):
            if until(view):
                return view
            time.sleep(0.02)
            view = {**view, **self.act('connect_poll', {'session': view['session']})}
        self.fail('still running: ' + json.dumps(view))

    def forms(self):
        return {s['name']: s['form'] for s in self.act('connect_sources', {})['sources']}

    def test_each_source_asks_what_the_setup_page_asks_and_never_a_terminal_command(self):
        forms = self.forms()
        self.assertEqual((forms['linkedin']['ask'], forms['linkedin']['browser'], forms['linkedin']['secret']), ([], 'linkedin', None))
        self.assertEqual(forms['x']['ask'], [['handle', 'Your X handle, without @']])  # its usual handle takes the default
        self.assertEqual([k for k, _ in forms['trello']['ask']], ['board', 'api_key'])
        self.assertEqual(forms['trello']['secret'], 'Trello token')
        self.assertEqual((forms['slack']['secret'], forms['crm']['secret']), ('Maton API key', 'Salesflare API key'))
        self.assertEqual(forms['github']['ask'], [])  # its login is read from gh once signed in
        self.assertTrue(forms['whatsapp']['personal'] and forms['whatsapp']['ask'][0][0] == 'phone')
        self.assertFalse(forms['intercom']['scope'] or forms['gateway']['scope'] or forms['android']['scope'])
        self.assertEqual(forms['rss']['company'], 'Acme')  # Work prefilled with the company the owner already has
        for name, form in forms.items():
            self.assertNotRegex(form['note'] or '', r'\bopenclaw\b|gh auth|assistant connect|wacli', name)

    def test_a_form_connects_with_its_answers_marked_as_the_owners_and_its_key_kept_out_of_view(self):
        with patch.object(onboarding, 'check', return_value=None):
            view = self.act('connect_start', {'name': 'trello', 'form': True, 'answers': {'board': 'b' * 24, 'api_key': 'k1', 'bogus': 'x'},
                                              'secret': 'ATTA-fake-token', 'scope': 'work', 'company': 'Globex'})
            view = self.finish(view)
        self.assertEqual(view['state'], 'done', view)
        saved = next(a for a in json.loads(self.path.read_text())['accounts'] if a['service'] == 'trello')
        self.assertEqual((saved['board'], saved['api_key'], saved['boundary'], saved['boundary_by']), ('b' * 24, 'k1', 'work:Globex', 'owner'))
        self.assertNotIn('bogus', json.dumps(saved))
        self.assertIn('ATTA-fake-token', Path(json.loads(self.path.read_text())['credentials']['trello']).read_text())
        self.assertNotIn('ATTA-fake-token', json.dumps(view))
        self.assertNotIn('saving it as globex-trello (Work · Globex)', view['lines'])
        self.assertFalse(any('work:' in line for line in view['lines']))

    def test_personal_and_a_company_offered_already_take_no_question(self):
        with patch.object(onboarding, 'check', return_value=None):
            view = self.finish(self.act('connect_start', {'name': 'rss', 'form': True, 'answers': {'url': 'https://feed.example/rss'},
                                                         'scope': 'personal'}))
            self.assertEqual(view['state'], 'done', view)
            view = self.finish(self.act('connect_start', {'name': 'rss', 'form': True, 'answers': {'url': 'https://feed.example/2'},
                                                         'scope': 'work', 'company': 'Acme'}))
            self.assertEqual(view['state'], 'done', view)
        feeds = [a for a in json.loads(self.path.read_text())['accounts'] if a['service'] == 'rss']
        self.assertEqual([(a['boundary'], a['url']) for a in feeds], [('personal:me', 'https://feed.example/rss'), ('work:Acme', 'https://feed.example/2')])

    def test_work_needs_its_company_and_nothing_else_is_taken_as_a_boundary(self):
        for bad in ({}, {'scope': 'work'}, {'scope': 'work', 'company': 'work:Main'}, {'scope': 'work', 'company': '<b>'}, {'scope': 'team'}):
            with self.assertRaisesRegex(ValueError, 'Work with its company'):
                self.act('connect_start', {'name': 'rss', 'form': True, 'answers': {'url': 'https://feed.example/rss'}, **bad})

    def test_linkedin_waits_for_the_sign_in_the_dashboard_offers_then_goes_on_by_itself(self):
        # also on a hosted Machine: its form signs in right there, and "not signed in" never shows before they could
        for manage in (None, 'https://cp.example.org/setup'):
            with self.subTest(hosted=bool(manage)):
                self.app.config['manage_url'] = manage
                source = next(s for s in self.act('connect_sources', {})['sources'] if s['name'] == 'linkedin')
                self.assertFalse(source.get('account_page') or source.get('hosted_signin'))  # + Add's own form, not a link away
                checks = iter(['linkedin_signed_out', 'linkedin_signed_out', None])
                with patch.object(onboarding, 'check', side_effect=lambda config, account: next(checks)), patch.object(onboarding, 'SIGNIN_EVERY', 0.1):
                    view = self.act('connect_start', {'name': 'linkedin', 'form': True, 'scope': 'work', 'company': 'Acme'})
                    view = self.finish(view, lambda v: v.get('signin') or v['state'] != 'running')
                    self.assertEqual((view['state'], view['signin'], view['question'], view['error']), ('running', 'linkedin', None, None))
                    view = self.finish(view)
                self.assertEqual((view['state'], view['signin']), ('done', None))
                self.assertFalse(any('openclaw' in line for line in view['lines']), view['lines'])
                self.path.write_text(json.dumps({**json.loads(self.path.read_text()), 'accounts': ACCOUNTS}))  # connect it anew

    def test_cancel_stops_a_sign_in_wait(self):
        with patch.object(onboarding, 'check', return_value='x_signed_out'), patch.object(onboarding, 'SIGNIN_EVERY', 0.05):
            view = self.act('connect_start', {'name': 'x', 'form': True, 'answers': {'handle': 'acme'}, 'scope': 'work', 'company': 'Acme'})
            view = self.finish(view, lambda v: v.get('signin'))
            view.update(self.act('connect_cancel', {'session': view['session']}))
            view = self.finish(view)
        self.assertEqual(view['state'], 'cancelled')

    def test_the_sign_in_page_opens_in_the_machines_browser(self):
        with patch.object(assistant.browser_login.browser_cdp, 'open_tab', return_value='t1') as tab, \
                patch.object(assistant.browser_viewer, 'focus') as focus:
            self.assertTrue(self.act('connect_site_signin', {'site': 'linkedin'})['opened'])
            self.act('connect_site_signin', {'site': 'x'})
        self.assertEqual([c.args[1] for c in tab.call_args_list], ['https://www.linkedin.com/login', 'https://x.com/i/flow/login'])
        self.assertEqual(focus.call_count, 2)
        for bad in ('chatgpt', 'https://evil.example', None):
            with self.assertRaises(ValueError):
                self.act('connect_site_signin', {'site': bad})
        with self.assertRaises(ValueError):
            self.app.action('connect_site_signin', {'site': 'linkedin'})  # not from the dashboard

    def test_hosted_github_whatsapp_and_the_phone_sign_in_on_the_dashboard_itself(self):
        self.app.config['manage_url'] = 'https://cp.example.org/setup'
        sources = {s['name']: s for s in self.act('connect_sources', {})['sources']}
        # their code (GitHub's, WhatsApp's QR or pairing code, the phone app's setup code) shows in + Add's form, never a
        # link away to the account
        for name in ('github', 'whatsapp', 'android'):
            with self.subTest(name):
                self.assertEqual((sources[name].get('hosted_signin'), sources[name].get('account_page')), (name, None))
        self.assertFalse(sources['linkedin'].get('account_page') or sources['linkedin'].get('hosted_signin'))

    def test_a_rerun_fix_reads_as_try_again(self):
        def connect(path, name, ui, account_id=None, restart=True):
            raise onboarding.SetupError('No url given', 'rerun: assistant connect rss')
        with patch.object(onboarding, 'connect', connect):
            view = self.finish(self.act('connect_start', {'name': 'rss'}))
        self.assertEqual(view['fix'], 'check what you filled in and try again')


class CodeTest(unittest.TestCase):
    """GitHub's device sign-in and WhatsApp's pairing code, shown on the dashboard instead of a terminal."""
    def script(self, folder, name, body):
        path = Path(folder) / name
        path.write_text('#!/bin/sh\n' + body)
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        return str(path)

    def watch(self, ui, run):
        seen = []

        def look():
            while not done:
                if ui.view()['code'] and ui.view()['code'] not in seen:
                    seen.append(ui.view()['code'])
                time.sleep(0.01)
        import threading
        done = False
        t = threading.Thread(target=look)
        t.start()
        try:
            return run(), seen
        finally:
            done = True
            t.join()

    def test_github_shows_its_device_code_until_signed_in(self):
        with tempfile.TemporaryDirectory() as folder:
            gh = self.script(folder, 'gh', 'case "$*" in\n  "auth status"*) exit 1 ;;\n'
                             '  "auth login"*) echo "! First copy your one-time code: AB12-CD34"; sleep 0.5; exit 0 ;;\nesac\n')
            ui = onboarding.WebUI(wait=5)
            _, seen = self.watch(ui, lambda: onboarding.gh_signin({'gh': gh}, ui))
        self.assertEqual(seen, [{'kind': 'device', 'code': 'AB12-CD34', 'url': 'https://github.com/login/device'}])
        self.assertIsNone(ui.view()['code'])

    def test_github_already_signed_in_shows_nothing(self):
        with tempfile.TemporaryDirectory() as folder:
            gh = self.script(folder, 'gh', 'exit 0\n')
            ui = onboarding.WebUI(wait=5)
            onboarding.gh_signin({'gh': gh}, ui)
        self.assertEqual(ui.view()['lines'], [])

    def test_github_sign_in_that_ends_without_a_yes(self):
        with tempfile.TemporaryDirectory() as folder:
            gh = self.script(folder, 'gh', 'case "$*" in\n  "auth status"*) exit 1 ;;\n  *) exit 1 ;;\nesac\n')
            with self.assertRaisesRegex(onboarding.SetupError, 'didn’t finish'):
                onboarding.gh_signin({'gh': gh}, onboarding.WebUI(wait=5))

    def test_whatsapp_shows_its_pairing_code_for_the_number_given(self):
        with tempfile.TemporaryDirectory() as folder:
            wacli = self.script(folder, 'wacli', f'echo "$@" > {folder}/args\n'
                                'echo \'{"event":"pair_code","data":{"code":"K7P2-9QX4"}}\'; sleep 0.5\n'
                                'echo \'{"event":"connected","data":{}}\'\n')
            ui = onboarding.WebUI(wait=5)
            ui.prefill({'Your WhatsApp phone number': '+32 470 12 34 56'})
            with patch.object(onboarding, 'whatsapp_linked', return_value='3247@s.whatsapp.net'):
                linked, seen = self.watch(ui, lambda: onboarding.whatsapp_pair(wacli, Path(folder) / 'store', ui))
            args = (Path(folder) / 'args').read_text().split()
        self.assertEqual((linked, seen), ('3247@s.whatsapp.net', [{'kind': 'pair', 'code': 'K7P2-9QX4'}]))
        self.assertEqual(args[args.index('--phone') + 1], '32470123456')

    def test_whatsapp_number_must_have_its_country_code(self):
        ui = onboarding.WebUI(wait=5)
        ui.prefill({'Your WhatsApp phone number': '0470'})
        with self.assertRaisesRegex(onboarding.SetupError, 'country code'):
            onboarding.whatsapp_pair('/nonexistent/wacli', '/nonexistent', ui)


if __name__ == '__main__':
    unittest.main()

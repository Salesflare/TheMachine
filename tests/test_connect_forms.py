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
from seams import patch_everywhere  # noqa: E402

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
        patch_everywhere(assistant, 'restart_self', return_value=True).start()
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
        self.assertEqual([k for k, _ in forms['trello']['ask']], ['board'])  # the key comes with Sign in with Trello
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
            view = self.act('connect_start', {'name': 'trello', 'form': True, 'answers': {'board': 'b' * 24, 'bogus': 'x'},
                                              'secret': 'ATTA-fake-token', 'scope': 'work', 'company': 'Globex'})
            view = self.finish(view)
        self.assertEqual(view['state'], 'done', view)
        saved = next(a for a in json.loads(self.path.read_text())['accounts'] if a['service'] == 'trello')
        self.assertEqual((saved['board'], saved['boundary'], saved['boundary_by']), ('b' * 24, 'work:Globex', 'owner'))
        self.assertNotIn('api_key', saved)
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

    def connect_as(self, service, email, args=None, answer=None, team=(), org=None, tid=None):
        """Connects a source that signs in as `email`, answering its one question (by option label) if it asks. org: what
        the provider says (a Workspace domain or a work tenant: True); tid: the Microsoft tenant its sign-in names."""
        steps = {**onboarding.STEPS, service: lambda config, account, ui: account.update(email=email, **({'tenant_id': tid} if tid else {}))}
        asked = []
        with patch.object(onboarding, 'check', return_value=None), patch.object(onboarding, 'STEPS', steps), \
                patch.object(onboarding, 'organization_of', return_value=org), \
                patch.object(assistant.App, 'team_domains', return_value=set(team), create=True):
            view = self.act('connect_start', {'name': service, 'form': True, 'answers': {}, **(args or {})})
            view = self.finish(view, lambda v: v['state'] != 'running' or v.get('question'))
            if view.get('question'):
                asked.append(view['question'])
                pick = view['question']['options'].index(answer)
                self.act('connect_answer', {'session': view['session'], 'question': view['question']['id'], 'value': pick})
                view = self.finish(view)
        self.assertEqual(view['state'], 'done', view)
        saved = next(a for a in json.loads(self.path.read_text())['accounts'] if a.get('email') == email and a['service'] == service)
        return saved, view, asked

    def test_mail_and_calendar_take_work_or_personal_from_the_address_when_it_says(self):
        # No question up front for a source that signs in as an address. A mail provider is Personal, an address on a
        # Work Fleet teammate's domain is Work, an address already marked keeps the owner's marking. A guess, so the
        # done form and its card offer Change.
        forms = self.forms()
        self.assertTrue(forms['gmail']['auto'] and forms['outlook']['auto'])
        self.assertFalse(forms['rss']['auto'] or forms['trello']['auto'])
        cases = [('gmail', 'sam.home@gmail.com', (), 'personal:me', 'guess'), ('outlook', 'kim@outlook.com', (), 'personal:me', 'guess'),
                 ('gmail', 'lee@globex.dev', ('globex.dev',), 'work:Globex', 'guess'),
                 ('calendar', 'owner@acme.example', (), 'work:Acme', 'owner')]
        for service, email, team, boundary, by in cases:
            with self.subTest(email=email):
                saved, view, asked = self.connect_as(service, email, team=team)
                self.assertEqual((saved['boundary'], saved['boundary_by'], asked), (boundary, by, []))
                self.assertEqual(view['guessed'], boundary if by == 'guess' else None)
        # An explicit pick still counts as the owner's
        saved, view, _ = self.connect_as('gmail', 'alex@initech.dev', {'scope': 'personal'})
        self.assertEqual((saved['boundary'], saved['boundary_by'], view['guessed']), ('personal:me', 'owner', None))

    def test_an_own_domain_alone_is_asked_never_guessed_work(self):
        # People use their own domain for personal mail too, and sharing follows Work: in doubt the one question is
        # asked (after Google's consent, the company prefilled), and the answer is the owner's.
        saved, view, asked = self.connect_as('gmail', 'jules@moreaudesign.io', answer='Personal')
        self.assertEqual(asked[0]['prompt'], 'Is this account work or personal?')
        self.assertEqual(asked[0]['options'][:2], ['Personal', 'Work · Moreaudesign'])
        self.assertEqual((saved['boundary'], saved['boundary_by'], view['guessed']), ('personal:me', 'owner', None))
        self.assertTrue(saved['scope_check'])  # its mail is looked at once it is in (scope_check.py)
        saved, _, asked = self.connect_as('outlook', 'jules@moreaudesign.io', answer='Work · Moreaudesign')
        self.assertEqual((saved['boundary'], saved['boundary_by']), ('personal:me', 'owner'))  # the same address follows its marking
        self.assertEqual(asked, [])
        saved, _, _ = self.connect_as('gmail', 'max@hooli.dev', answer='Work · Hooli')
        self.assertEqual((saved['boundary'], saved['boundary_by']), ('work:Hooli', 'owner'))
        for email in ('jo@jo-family.net', 'me@my-name.org'):
            self.assertEqual(onboarding.guess_boundary({'accounts': []}, email), (None, None))

    def test_a_workspace_or_work_tenant_on_an_own_domain_is_still_asked_a_consumer_tenant_is_personal(self):
        # Google's hd and a Microsoft work tenant say the domain is an organization's, not that this mail is work: still
        # asked, Work first. Microsoft's consumer tenant is Outlook.com: Personal, whatever the domain.
        saved, view, asked = self.connect_as('gmail', 'robin@robin-studio.dev', answer='Personal', org=True)
        self.assertEqual((asked[0]['options'][0], asked[0]['options'][-1]), ('Work · Robin-studio', 'Personal'))
        self.assertEqual((saved['boundary'], saved['boundary_by'], view['guessed']), ('personal:me', 'owner', None))
        saved, view, asked = self.connect_as('outlook', 'kai@kai-home.dev', tid=onboarding.CONSUMER_TENANT)
        self.assertEqual((saved['boundary'], saved['boundary_by'], view['guessed'], asked), ('personal:me', 'guess', 'personal:me', []))
        self.assertNotIn('scope_check', saved)
        self.assertEqual(onboarding.guess_boundary({'accounts': []}, 'kai@kai-home.dev', tid='0a0b0c0d-1111-2222-3333-444455556666'),
                         (None, None))  # a work tenant alone: asked

    def test_organization_comes_from_the_tenant_or_googles_user_info_with_the_access_it_has(self):
        work = '0a0b0c0d-1111-2222-3333-444455556666'
        self.assertTrue(onboarding.organization_of({}, {'service': 'outlook', 'tenant_id': work}))
        self.assertFalse(onboarding.organization_of({}, {'service': 'outlook', 'tenant_id': onboarding.CONSUMER_TENANT}))
        self.assertIsNone(onboarding.organization_of({}, {'service': 'outlook_calendar'}))
        import sources
        calls = []
        for answer, want in (({'email': 'a@b.dev', 'hd': 'b.dev'}, True), ({'email': 'a@b.dev'}, False)):
            with patch.object(sources, 'gog_read', side_effect=lambda *a: calls.append(a[2:]) or answer):
                self.assertIs(onboarding.organization_of({}, {'service': 'gmail', 'email': 'a@b.dev'}), want)
        self.assertEqual(calls[0], ('oauth2', 'v2', 'oauth2.userinfo.get', {}, 'https://www.googleapis.com/auth/userinfo.email'))
        with patch.object(sources, 'gog_read', side_effect=sources.SourceError('oauth2', 403)):
            self.assertIsNone(onboarding.organization_of({}, {'service': 'calendar', 'email': 'a@b.dev'}))
        import google_api
        self.assertEqual(google_api.url_for('oauth2.userinfo.get', {}), ('GET', 'https://www.googleapis.com/oauth2/v2/userinfo'))
        import ms_graph, base64
        def jwt(claims):
            return 'x.' + base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip('=') + '.y'
        self.assertEqual(ms_graph.tenant_of(jwt({'tid': work.upper()})), work)
        for token in (jwt({'tid': 'nope'}), 'EwB0opaque', jwt([1])):
            self.assertIsNone(ms_graph.tenant_of(token))

    def test_every_mail_provider_enrichment_knows_is_no_company(self):
        import re
        import enrichment
        names = re.search(r'\(\?:(g\(\?:oogle\)\?mail\|.*?)\)\\\.', enrichment.FREEMAIL.pattern, re.S).group(1)
        for name in re.sub(r"'\s*r'", '', names).replace('g(?:oogle)?mail', 'gmail|googlemail').replace('proton(?:mail)?', 'proton|protonmail').split('|'):
            self.assertEqual(onboarding.company_of(f'a@{name}.com'), '', name)

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

    def test_a_sign_in_under_way_is_brought_back_not_started_over(self):
        # Pressing Sign in again while LinkedIn waits for the code it emailed: that tab, as it is. Try again after
        # LinkedIn stopped it (fresh): its sign-in page again, in that same tab.
        cdp = assistant.browser_login.browser_cdp
        tabs = [{'type': 'page', 'id': 'feed', 'url': 'https://www.linkedin.com/feed/'},
                {'type': 'page', 'id': 'pin', 'url': 'https://www.linkedin.com/checkpoint/challenge/AgE'}]
        with patch.object(cdp, '_http', return_value=tabs), patch.object(cdp, 'open_tab') as opened, \
                patch.object(cdp, 'navigate') as navigate, patch.object(assistant.browser_viewer, 'focus') as focus:
            self.act('connect_site_signin', {'site': 'linkedin'})
            self.assertEqual((opened.call_count, navigate.call_count, focus.call_args.kwargs['target']), (0, 0, 'pin'))
            self.act('connect_site_signin', {'site': 'linkedin', 'fresh': True})
            self.assertEqual(navigate.call_args.args[1:], ('pin', 'https://www.linkedin.com/login'))
            self.act('connect_site_signin', {'site': 'x'})  # none of X's: a new one
            self.assertEqual(opened.call_args.args[1], 'https://x.com/i/flow/login')

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
            wacli = self.script(folder, 'wacli', f'echo "$@" > {folder}/args\necho "$WACLI_DEVICE_LABEL" > {folder}/label\n'
                                'echo \'{"event":"pair_code","data":{"code":"K7P2-9QX4"}}\'; sleep 0.5\n'
                                'echo \'{"event":"connected","data":{}}\'\n')
            ui = onboarding.WebUI(wait=5)
            ui.prefill({'Your WhatsApp phone number': '+32 470 12 34 56'})
            with patch.object(onboarding, 'whatsapp_linked', return_value='3247@s.whatsapp.net'):
                linked, seen = self.watch(ui, lambda: onboarding.whatsapp_pair(wacli, Path(folder) / 'store', ui))
            args = (Path(folder) / 'args').read_text().split()
            label = (Path(folder) / 'label').read_text().strip()
        self.assertEqual((linked, seen), ('3247@s.whatsapp.net', [{'kind': 'pair', 'code': 'K7P2-9QX4'}]))
        self.assertEqual(args[args.index('--phone') + 1], '32470123456')
        self.assertEqual(label, 'The Machine')  # the name the phone shows under Linked devices, not "wacli - Linux (host)"

    def test_whatsapp_on_the_dashboard_never_says_wacli(self):
        """Owners know it as WhatsApp on The Machine: the dashboard's install question, its lines, the error when it isn't
        there and the hints for a WhatsApp that stopped reading name no wacli (a terminal still does)."""
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(onboarding, 'tool', return_value=None), \
                patch.object(onboarding.wacli_release, 'platform_key', return_value='linux_amd64'), \
                patch.object(onboarding.wacli_release, 'install', side_effect=OSError('wacli download failed')):
            ui = onboarding.WebUI(wait=5)
            asked = []
            ui._ask = lambda kind, prompt, default='', options=None: asked.append(prompt) or True
            with self.assertRaises(onboarding.SetupError) as stopped:
                onboarding.step_whatsapp({'database': str(Path(folder) / 'events.sqlite')}, {'id': 'wa'}, ui)
        shown = [*asked, *ui.view()['lines'], str(stopped.exception), stopped.exception.fix or '',
                 *(text for error, text in onboarding.HINTS if error.startswith('whatsapp'))]
        self.assertEqual(asked, ['Install WhatsApp on this Machine?'])
        self.assertTrue(all('wacli' not in text.lower() for text in shown), shown)
        catalog = json.loads((Path(onboarding.__file__).parent / 'i18n' / 'en.json').read_text())
        self.assertEqual([key for key in catalog if 'wacli' in key.lower()], [])  # nothing the dashboard translates says it

    def test_whatsapp_pairing_ends_soon_after_connected_while_history_keeps_coming(self):
        # wacli auth keeps receiving history after it links; the sync takes that over, so the link screen never waits on it
        with tempfile.TemporaryDirectory() as folder:
            wacli = self.script(folder, 'wacli', 'echo \'{"event":"connected","data":{}}\'; sleep 30\n')
            ui = onboarding.WebUI(wait=5)
            ui.prefill({'Your WhatsApp phone number': '+32 470 12 34 56'})
            began = time.monotonic()
            with patch.object(onboarding, 'WHATSAPP_HANDOFF', 1), patch.object(onboarding, 'whatsapp_linked', return_value='3247@s.whatsapp.net'):
                linked = onboarding.whatsapp_pair(wacli, Path(folder) / 'store', ui)
        self.assertEqual(linked, '3247@s.whatsapp.net')
        self.assertLess(time.monotonic() - began, 15)

    def test_whatsapp_number_must_have_its_country_code(self):
        ui = onboarding.WebUI(wait=5)
        ui.prefill({'Your WhatsApp phone number': '0470'})
        with self.assertRaisesRegex(onboarding.SetupError, 'country code'):
            onboarding.whatsapp_pair('/nonexistent/wacli', '/nonexistent', ui)


if __name__ == '__main__':
    unittest.main()

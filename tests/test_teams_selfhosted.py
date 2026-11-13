"""Microsoft Teams on a paired self-hosted Machine: + Add offers it (Chat and Meetings, one sign-in) once the control
plane opens its sign-in (fleet.SIGNIN_SOURCES microsoft_teams), started as Docs is, with the hosted Teams consent's
scopes. The sign-in comes back sealed (onboarding.connect_teams_grant): a Teams account of its own, or joined to that
address's Outlook sign-in, checked with a real read before it is kept. No live calls: the reads are stubbed and the
control plane is a fake."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant
import fleet
import mail_grants
import onboarding
from machine.sources import teams_setup
from test_connectors import a
from test_device_connect import fleet_with
from seams import patch_everywhere  # noqa: E402

REFRESH = 'fixture-refresh-token-teams'


class Offered(unittest.TestCase):
    def test_paired_self_hosted_or_a_hosted_consent_not_an_unpaired_one(self):
        self.assertTrue(teams_setup.offered({'teams_consent': True}))
        self.assertTrue(teams_setup.offered({'credentials': {'fleet': '/token'}}))  # paired with an account
        self.assertFalse(teams_setup.offered({}))  # not paired: nothing to sign in through
        self.assertFalse(teams_setup.offered({'manage_url': 'https://app.example.org/setup', 'credentials': {'fleet': '/token'}}))  # hosted: its consent says
        self.assertIn('microsoft_teams', fleet.SIGNIN_SOURCES)
        self.assertEqual(fleet.SIGNIN_OF['teams'], 'microsoft_teams')
        self.assertIn('microsoft_teams', onboarding.DELIVERED)


class Dashboard(unittest.TestCase):
    def app(self, paired=True, signins=('microsoft', 'microsoft_teams')):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / 'config.json'
        config = {'accounts': [], 'database': str(Path(temp.name) / 'events.sqlite'),
                  **({'credentials': {'fleet': str(Path(temp.name) / 'fleet.token')}} if paired else {})}
        path.write_text(json.dumps(config))
        app = object.__new__(assistant.App)
        app.config, app.config_path = config, path
        app.fleet = fleet_with(self, []) if paired else None
        if app.fleet is not None:
            app.fleet.relay.signins = list(signins) if signins is not None else None
        return app

    def teams(self, app):
        return [x for x in app.action('connect_sources', {}, owner_dashboard=True)['sources'] if x['service'] == 'teams']

    def test_a_paired_self_hosted_machine_offers_teams_and_signs_it_in_through_the_control_plane(self):
        app = self.app()
        [teams] = self.teams(app)
        # Chat here; the dashboard also lists it as Teams meetings under Meetings (test_teams_selfhosted_dashboard.mjs)
        self.assertEqual((teams['group'], teams['signin'], teams.get('signin_off'), teams.get('hosted_signin')), ('chat', 'microsoft_teams', None, None))
        self.assertEqual(app.action('connect_signin', {'name': 'teams'}, owner_dashboard=True)['state'], 'started')
        self.assertEqual((app.fleet.relay.calls[-1][1], app.fleet.relay.calls[-1][2]['source']), ('/connect-start', 'microsoft_teams'))
        self.assertEqual(app.action('connect_signin_state', {'name': 'teams'}, owner_dashboard=True), {'state': 'started'})

    def test_left_out_while_the_control_plane_does_not_open_it_or_the_machine_is_not_paired(self):
        self.assertEqual(self.teams(self.app(signins=('microsoft',))), [])  # a control plane from before Teams here
        self.assertEqual(self.teams(self.app(signins=None)), [])  # one that can't say: no tab that closes at once
        self.assertEqual(self.teams(self.app(paired=False)), [])
        with self.assertRaisesRegex(ValueError, 'Pair this Machine first'):
            self.app(paired=False).action('connect_signin', {'name': 'teams'}, owner_dashboard=True)

    def test_disconnecting_teams_alone_forgets_its_own_sign_in(self):
        app = self.app()
        teams = {'id': 'acme-teams', 'service': 'teams', 'email': 'dee@acme.example', 'transport': 'broker', 'own_grant': True, 'boundary': 'work:Acme'}
        app.config['accounts'] = [teams]
        app.config_path.write_text(json.dumps(app.config))
        mail_grants.put(app.config, 'microsoft', 'dee@acme.example', REFRESH)
        with patch_everywhere(assistant, 'restart_self', return_value=False):
            app.action('connect_remove', {'account': 'acme-teams'}, owner_dashboard=True)
        self.assertIsNone(mail_grants.get(app.config, 'microsoft', 'dee@acme.example'))
        self.assertEqual(app.fleet.relay.calls[-1][1:], ('/grant-forget', {'provider': 'microsoft', 'email': 'dee@acme.example'}))


class ConnectTeamsGrant(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'fleet.token').write_text('fixture-device-token\n')
        self.path = self.root / 'config.json'
        self.save({'database': str(self.root / 'events.sqlite'), 'credentials': {'fleet': str(self.root / 'fleet.token')}, 'accounts': []})
        self.checked, self.answer = [], None
        patch.object(onboarding, 'assistant', return_value=a).start()
        patch.object(onboarding, 'check', side_effect=lambda config, account: self.checked.append(dict(account)) or self.answer).start()
        self.addCleanup(patch.stopall)

    def save(self, config):
        self.path.write_text(json.dumps(config))

    def config(self):
        return json.loads(self.path.read_text())

    def args(self, provider='microsoft', source='microsoft_teams', **change):
        grant = {'provider': provider, 'email': 'Dee@Acme.example', 'refresh_token': REFRESH, 'scopes': ['Chat.Read', 'User.Read'], **change}
        return {'source': source, 'grant': grant}

    def test_teams_alone_is_its_own_sign_in_and_no_outlook_comes_with_it(self):
        self.assertEqual(onboarding.connect_delivered(self.path, self.args()), {'ok': True, 'name': 'dee@acme.example'})
        config = self.config()
        [teams] = config['accounts']
        self.assertEqual((teams['service'], teams['email'], teams['transport'], teams['own_grant']), ('teams', 'dee@acme.example', 'broker', True))
        self.assertTrue(teams['boundary'].startswith('work'))  # a work account: its company
        self.assertEqual(config['microsoft_broker'], {'url': fleet.NETWORK + '/api/fleet/microsoft-token'})
        self.assertEqual(config['credentials']['microsoft-broker'], config['credentials']['fleet'])  # its own device token
        self.assertNotIn(REFRESH, self.path.read_text())
        self.assertEqual(mail_grants.get(config, 'microsoft', 'dee@acme.example'), REFRESH)  # kept here only, sealed
        self.assertEqual([x['service'] for x in self.checked], ['teams'])  # a real read first
        onboarding.connect_delivered(self.path, self.args(refresh_token='fixture-refresh-token-teams-2'))
        self.assertEqual([x['id'] for x in self.config()['accounts']], [teams['id']])  # signed in again: the same account

    def test_teams_joins_the_outlook_sign_in_of_that_address(self):
        onboarding.connect_delivered(self.path, self.args(source='microsoft', scopes=['Mail.ReadWrite', 'Calendars.Read']))
        [mail] = [x for x in self.config()['accounts'] if x['service'] == 'outlook']
        onboarding.connect_delivered(self.path, self.args(refresh_token='fixture-refresh-token-joined'))
        [teams] = [x for x in self.config()['accounts'] if x['service'] == 'teams']
        self.assertNotIn('own_grant', teams)  # Outlook's sign-in, which now also reads chats
        self.assertEqual(teams['boundary'], mail['boundary'])
        self.assertEqual(mail_grants.get(self.config(), 'microsoft', 'dee@acme.example'), 'fixture-refresh-token-joined')

    def test_one_that_does_not_check_out_leaves_the_sign_in_before_and_adds_nothing(self):
        onboarding.connect_delivered(self.path, self.args(source='microsoft'))
        self.answer = 'teams_work_only'
        with self.assertRaisesRegex(onboarding.SetupError, 'work or school'):
            onboarding.connect_delivered(self.path, self.args(refresh_token='fixture-refresh-token-personal'))
        self.assertNotIn('teams', [x['service'] for x in self.config()['accounts']])
        self.assertEqual(mail_grants.get(self.config(), 'microsoft', 'dee@acme.example'), REFRESH)

    def test_without_chat_read_or_a_microsoft_grant_nothing_is_kept(self):
        for args in (self.args(scopes=['User.Read']), self.args(provider='google'), self.args(refresh_token='')):
            with self.assertRaises(onboarding.SetupError):
                onboarding.connect_delivered(self.path, args)
        self.assertEqual((self.config()['accounts'], self.checked), ([], []))
        self.assertIsNone(mail_grants.get(self.config(), 'microsoft', 'dee@acme.example'))

    def test_only_a_paired_self_hosted_machine(self):
        self.save({'database': str(self.root / 'events.sqlite'), 'accounts': []})
        with self.assertRaisesRegex(onboarding.SetupError, 'paired'):
            onboarding.connect_delivered(self.path, self.args())


if __name__ == '__main__':
    unittest.main()

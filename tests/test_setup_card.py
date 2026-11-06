"""The setup to-do at the top of To-dos (assistant.setup_card): what the Machine knows about each step, and rows closed
with their × kept on the Machine, so a row closed on one device stays closed on every other."""
import tempfile
import unittest
from pathlib import Path

import assistant as a


class SetupCard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.config = {'accounts': [{'id': 'me-gmail', 'service': 'gmail'}, {'id': 'me-cal', 'service': 'calendar'}],
                       'manage_url': 'https://app.example.test/setup'}

    def card(self, config=None):
        return a.setup_card(self.store, config or self.config)

    def test_a_new_machine_has_every_step_open(self):
        self.assertEqual(self.card(), {'closed': False, 'dismissed': [], 'phones': 0, 'whatsapp': False, 'mail_accounts': 1,
                                       'add': 'google', 'more': False})

    def test_steps_tick_off_from_what_the_machine_has(self):
        accounts = [*self.config['accounts'], {'id': 'wa', 'service': 'whatsapp'}, {'id': 'me-outlook', 'service': 'outlook'},
                    {'id': 'slack', 'service': 'slack'}]
        with self.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS notify_app_devices(id TEXT PRIMARY KEY)')
            db.execute("INSERT INTO notify_app_devices(id) VALUES('phone-1')")
        card = self.card(dict(self.config, accounts=accounts))
        self.assertEqual((card['phones'], card['whatsapp'], card['mail_accounts'], card['more']), (1, True, 2, True))

    def test_another_account_matches_the_provider_the_owner_has(self):
        outlook = dict(self.config, accounts=[{'id': 'o', 'service': 'outlook'}, {'id': 'oc', 'service': 'outlook_calendar'}])
        self.assertEqual(self.card(outlook)['add'], 'microsoft')
        self.assertFalse(self.card(outlook)['more'])  # mail and calendar are not "more connections"
        self.assertEqual(self.card()['add'], 'google')

    def test_shared_accounts_are_not_the_owners(self):
        shared = dict(self.config, accounts=[*self.config['accounts'], {'id': 'team-wa', 'service': 'whatsapp', 'shared': True}])
        self.assertFalse(self.card(shared)['whatsapp'])

    def test_a_closed_row_stays_closed_on_every_device(self):
        self.assertEqual(a.setup_dismiss(self.store, self.config, 'whatsapp')['setup_card']['dismissed'], ['whatsapp'])
        a.setup_dismiss(self.store, self.config, 'whatsapp')  # twice is fine
        a.setup_dismiss(self.store, self.config, 'hint-source-github')
        # another device asks the Machine: the same rows closed
        other = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.assertEqual(a.setup_card(other, self.config)['dismissed'], ['hint-source-github', 'whatsapp'])
        self.assertFalse(a.setup_card(other, self.config)['closed'])
        a.setup_dismiss(self.store, self.config, 'card')
        self.assertTrue(a.setup_card(other, self.config)['closed'])
        self.assertNotIn('card', a.setup_card(other, self.config)['dismissed'])

    def test_only_known_steps_are_kept(self):
        for bad in ('', 'tour', 'hint-', 'hint-UPPER', 'setup:card', 'phone x', None):
            with self.assertRaises(ValueError, msg=bad):
                a.setup_dismiss(self.store, self.config, bad)

    def test_only_the_owner_closes_a_step_on_the_dashboard(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        self.assertIn('setup_dismiss', a.DASHBOARD_ACTIONS)
        self.assertIn('setup_dismiss', a.OWNER_ACTIONS)
        with self.assertRaises(ValueError):
            app.action('setup_dismiss', {'step': 'phone'})
        self.assertEqual(app.action('setup_dismiss', {'step': 'phone'}, owner_dashboard=True)['setup_card']['dismissed'], ['phone'])

    def test_a_closed_row_or_the_whole_to_do_comes_back(self):
        # Undo after a × (one row, or the card), and Show hidden / Settings' Show again (all of it)
        for step in ('phone', 'whatsapp', 'hint-source-github', 'card'):
            a.setup_dismiss(self.store, self.config, step)
        card = a.setup_restore(self.store, self.config, 'phone')['setup_card']
        self.assertEqual((card['dismissed'], card['closed']), (['hint-source-github', 'whatsapp'], True))
        card = a.setup_restore(self.store, self.config, 'card')['setup_card']
        self.assertEqual((card['dismissed'], card['closed']), (['hint-source-github', 'whatsapp'], False))
        a.setup_restore(self.store, self.config, 'phone')  # not closed: fine
        a.setup_dismiss(self.store, self.config, 'card')
        card = a.setup_restore(self.store, self.config, 'all')['setup_card']
        self.assertEqual((card['dismissed'], card['closed']), ([], False))
        for bad in ('', 'tour', 'setup:%', '%', None):
            with self.assertRaises(ValueError, msg=bad):
                a.setup_restore(self.store, self.config, bad)

    def test_only_the_owner_brings_a_step_back_on_the_dashboard(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        self.assertIn('setup_restore', a.DASHBOARD_ACTIONS)
        self.assertIn('setup_restore', a.OWNER_ACTIONS)
        a.setup_dismiss(self.store, self.config, 'phone')
        with self.assertRaises(ValueError):
            app.action('setup_restore', {'step': 'phone'})
        self.assertEqual(app.action('setup_restore', {'step': 'phone'}, owner_dashboard=True)['setup_card']['dismissed'], [])


if __name__ == '__main__':
    unittest.main()

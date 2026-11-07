"""Settings, Notifications, Weekly recap (machine/app/recap_settings.py): the owner turns the recap on or off from the
dashboard, a hosted Machine too. It is weekly_recap in config.json, saved like Work hours with its day and time kept."""
import json
import tempfile
import unittest
from pathlib import Path

import assistant
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS


class RecapSwitch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'config.json'
        self.path.write_text(json.dumps({'accounts': [], 'digest_at': '08:30', 'weekly_recap': {'enabled': False, 'weekday': 4, 'at': '17:30'}}))
        self.app = assistant.App.__new__(assistant.App)
        self.app.config, self.app.config_path = json.loads(self.path.read_text()), self.path

    def test_on_by_default_with_its_day_and_time(self):
        self.app.config = {}
        self.assertEqual(self.app.recap_switch_view(), {'on': True, 'weekday': 5, 'at': '16:00', 'saveable': True})

    def test_enabled_false_from_an_install_is_no_choice_but_the_owners_off_is(self):
        self.assertTrue(self.app.recap_switch_view()['on'])  # setUp: enabled false as every install wrote it, never chosen
        self.app.recap_set_action('recap_set', {'on': False}, True)
        self.assertEqual(json.loads(self.path.read_text())['weekly_recap'], {'enabled': False, 'weekday': 4, 'at': '17:30', 'chosen': True})
        self.app.config = json.loads(self.path.read_text())  # as the service reads it again after a restart
        self.assertFalse(self.app.recap_switch_view()['on'])

    def test_the_owner_turns_it_on_and_off_saved_in_config_json(self):
        self.assertEqual(self.app.recap_set_action('recap_set', {'on': True}, True), {'on': True, 'weekday': 4, 'at': '17:30', 'saveable': True})
        saved = json.loads(self.path.read_text())
        self.assertEqual(saved['weekly_recap'], {'enabled': True, 'weekday': 4, 'at': '17:30', 'chosen': True})
        self.assertEqual(saved['digest_at'], '08:30')  # other settings untouched
        self.assertTrue(self.app.config['weekly_recap']['enabled'])  # in use at once: recap_step reads self.config
        self.assertFalse(self.app.recap_set_action('recap_set', {'on': False}, True)['on'])
        self.assertFalse(json.loads(self.path.read_text())['weekly_recap']['enabled'])

    def test_only_the_owner_from_the_dashboard(self):
        self.assertIn('recap_set', OWNER_ACTIONS)
        self.assertIn('recap_set', DASHBOARD_ACTIONS)
        self.assertEqual(assistant.App.ACTION_HANDLERS['recap_set'], 'recap_set_action')
        with self.assertRaises(ValueError):
            self.app.recap_set_action('recap_set', {'on': True}, False)
        self.assertFalse(json.loads(self.path.read_text())['weekly_recap']['enabled'])

    def test_no_config_file_shows_the_state_without_a_switch(self):
        self.app.config_path = None
        self.assertFalse(self.app.recap_switch_view()['saveable'])
        with self.assertRaises(ValueError):
            self.app.recap_set_action('recap_set', {'on': True}, True)


if __name__ == '__main__':
    unittest.main()

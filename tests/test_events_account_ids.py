"""A Do it run's first events or related call is a valid one (2026-11-08 agent users: the Machine's own transcripts had
them failing for account_ids it guessed ("gmail", a service name) or left out). The job message names its accounts."""
import json
import unittest
from seams import patch_everywhere  # noqa: E402,F401
from machine.app.preparation import evidence_line

CONFIG = {'accounts': [{'id': 'work-gmail', 'service': 'gmail', 'email': 'robin@example.com'},
                       {'id': 'work-slack', 'service': 'slack'}, {'id': 'home-whatsapp', 'service': 'whatsapp'}]}


class EventsAccountIds(unittest.TestCase):
    def test_the_run_is_told_its_account_ids_and_sources(self):
        line = evidence_line(CONFIG, json.dumps(['work-gmail']), [(4, 'work-gmail'), (9, 'work-slack')])
        self.assertIn('["work-gmail", "work-slack"]', line)
        self.assertIn('event_ids: [4, 9]', line)
        self.assertIn('["all"]', line)
        self.assertNotIn('home-whatsapp', line)
        self.assertEqual(evidence_line(CONFIG, '["gone"]', []), '')
        self.assertIn('["work-gmail"]', evidence_line(CONFIG, '["work-gmail"]', []))
        self.assertIn('not every connection', line)

    def test_a_run_from_an_email_still_knows_the_calendar_is_connected(self):
        """2026-11-15 agent users: after setup connected Gmail and Google Calendar, a scheduling to-do from an email went
        Stuck saying only Gmail was connected. Its run was told only its own accounts (work-gmail). Every run now also
        names the owner's own connected calendars and how to read when they are free; a Fleet-shared one isn't theirs."""
        from unittest.mock import patch
        from machine.app import preparation
        from machine.sources.connectors import calendars_prompt
        config = {'accounts': [*CONFIG['accounts'], {'id': 'work-calendar', 'service': 'calendar', 'email': 'robin@example.com'},
                               {'id': 'team-calendar', 'service': 'calendar', 'shared': True}]}
        config['accounts'][-1]['email'] = 'team@example.com'
        line = calendars_prompt(config)
        self.assertIn('Connected calendars: Google Calendar (robin@example.com), synced', line)
        self.assertIn('meeting_notes args day=', line)
        self.assertIn('Never ask to connect a calendar listed here', line)
        self.assertIn('whether a Meet link is added', line)
        self.assertNotIn('team@example.com', line)
        self.assertEqual(calendars_prompt(CONFIG), '')
        job = {'job_id': 'j' * 32, 'suggestion_id': 's1', 'ahead': False}
        with patch.object(preparation, 'calendar_prompt', lambda config: ''):
            for prompt in (preparation.preparation_prompt(job, config=config), preparation.chat_prompt(job, config)):
                self.assertIn('Connected calendars: Google Calendar (robin@example.com)', prompt)


if __name__ == '__main__':
    unittest.main()

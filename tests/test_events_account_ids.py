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


if __name__ == '__main__':
    unittest.main()

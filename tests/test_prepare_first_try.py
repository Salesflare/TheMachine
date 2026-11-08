"""A Do it run's prepare call is valid on its first try (2026-11-08 agent users: the Machine's own transcripts had it
failing for next_actions=[], which PREPARATION.md allows as "zero", and a follow-up labeled "Assess…" or "Incorporate…")."""
import unittest
from seams import patch_everywhere  # noqa: E402,F401
import next_actions as n

CONFIG = {'accounts': [{'id': 'work-gmail', 'service': 'gmail', 'email': 'robin@example.com'},
                       {'id': 'work-slack', 'service': 'slack'}, {'id': 'home-whatsapp', 'service': 'whatsapp'}]}


class PrepareFirstTry(unittest.TestCase):
    def test_no_next_actions_is_an_empty_list_too(self):
        self.assertIsNone(n.validate([], CONFIG, ['work-gmail']))
        self.assertIsNone(n.validate(None, CONFIG, ['work-gmail']))
        many = [{'kind': 'prepare', 'label': f'Draft option {i}', 'instructions': 'x'} for i in 'abcd']
        with self.assertRaisesRegex(ValueError, 'one to three'):
            n.validate(many, CONFIG, ['work-gmail'])

    def test_a_follow_up_label_error_says_how_it_starts(self):
        with self.assertRaises(ValueError) as caught:
            n.validate({'kind': 'prepare', 'label': 'Incorporate KPI export', 'instructions': 'Read it.'}, CONFIG, ['work-gmail'])
        self.assertIn('Update', str(caught.exception))
        self.assertIn('Check', str(caught.exception))
        for label in ('Update the pre-read', 'Check scope cuts', 'Set up the export'):
            self.assertEqual(n.validate({'kind': 'prepare', 'label': label, 'instructions': 'Do it.'}, CONFIG, ['work-gmail'])['label'], label)


if __name__ == '__main__':
    unittest.main()

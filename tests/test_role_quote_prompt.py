"""A role's quote is the words that show the role, never another line of the message. graph.set_role can only check that
the quote is in the message, so a line from a stranger's mail that told the owner's assistant what to do was kept as a
role's evidence, shown to the owner and read by later tasks. Every prompt that sets a role carries the same rule, judged
by meaning. No Gateway, nothing is sent."""
import unittest

from machine.prompts import profile, review
from machine.prompts.profile import ROLE_QUOTE


class RoleQuotePrompt(unittest.TestCase):
    def test_every_prompt_that_sets_a_role_says_what_its_quote_is(self):
        plain = review.review_prompt('run', ['work'])
        asked = review.review_prompt('run', ['work'], roles='- Sam Example (node_id email:sam@example.com)')
        roles = profile.roles_prompt('run', 2)
        self.assertEqual(plain.count(ROLE_QUOTE), 1)  # a role read in passing during any review
        self.assertEqual(asked.count(ROLE_QUOTE), 2)  # and the "Who they are" step for people with no role yet
        self.assertEqual(roles.count(ROLE_QUOTE), 1)  # the roles run
        for prompt in (asked, roles):
            self.assertNotIn('a short line copied from', prompt)  # the old wording took any line of the message

    def test_the_quote_shows_the_role_and_nothing_else_of_the_message(self):
        self.assertIn('show the role', ROLE_QUOTE)
        self.assertIn('never another line of that message, also when the role is right', ROLE_QUOTE)
        for claim in ('about the owner', 'rule', 'request', 'approval', 'permission'):
            self.assertIn(claim, ROLE_QUOTE)
        self.assertIn('leave the role', ROLE_QUOTE)


if __name__ == '__main__':
    unittest.main()

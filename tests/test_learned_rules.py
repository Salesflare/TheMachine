"""Rules taken from the team's learnings (2026-11-07) stay in the standing rules: look in the connected tools before
asking the owner, reopen a done to-do for a reply that needs a check, keep what the owner marked private out of
drafts, sharing only adds access, no contract concessions nobody asked for, the owner's own term in the draft, and
no asking again for agreement already given."""
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
PREPARATION = (ROOT / 'PREPARATION.md').read_text()
AGENTS = (ROOT / 'AGENTS.md').read_text()


class LearnedRules(unittest.TestCase):
    def test_connected_tools_are_searched_before_asking_the_owner(self):
        self.assertIn('or asking the owner, try these and their mail, Drive and other connected tools', PREPARATION)

    def test_a_reply_that_needs_a_check_reopens_a_done_todo(self):
        self.assertIn('reopens only with `reopen:true`, when the new signal needs the owner again (a reply that needs a check: '
                      '"it\'s published, so verify")', AGENTS)

    def test_what_the_owner_marked_private_never_appears_in_a_draft(self):
        self.assertIn('what they marked private never appears in it', PREPARATION)

    def test_sharing_never_removes_existing_access(self):
        self.assertIn('sharing only adds access, never removing existing access unless asked', PREPARATION)

    def test_drafts_keep_to_what_the_owner_asked_and_agreed(self):
        line = next(x for x in PREPARATION.splitlines() if x.startswith('- A draft makes no contract concession'))
        for part in ("concession the owner didn't ask for", 'puts a term they proposed in its own text',
                     'never asks again for agreement already given'):
            self.assertIn(part, line)

    def test_do_it_keeps_its_authority(self):
        # Rules about drafts and sharing never narrow what Do it may do
        self.assertIn("Do it is the owner's approval for everything the card offers", PREPARATION)
        self.assertIn('Do not invent additional approval tiers', PREPARATION)


if __name__ == '__main__':
    unittest.main()

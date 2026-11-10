"""A review keeps its assistant_signals calls few at a time: on the Codex harness every tool call starts a hook relay
process (a whole OpenClaw CLI) in the Gateway's memory-capped service, and a Code Mode cell that ran ~50 events calls
in one Promise.all started ~106 of them at once and ran a hosted Gateway out of memory six times in an hour
(2026-11-10). The tool and the review prompt both say: at most 4 at a time, several events in one call."""
from pathlib import Path
import unittest

from machine.prompts.review import review_prompt

ROOT = Path(__file__).parent.parent


class SignalFanout(unittest.TestCase):
    def test_the_tool_and_the_review_keep_calls_few_at_a_time(self):
        plugin = (ROOT / 'openclaw-plugin' / 'index.ts').read_text()
        self.assertIn('At most 4 assistant_signals calls at a time, also in Code Mode (Promise.all)', plugin)
        prompt = review_prompt('run', ['work'])
        self.assertIn('run at most 4 assistant_signals calls at a time', prompt)
        self.assertIn('Read several events in one events call (event_ids)', prompt)


if __name__ == '__main__':
    unittest.main()

"""The review's turn message is built stable-first, so the model's prompt cache can reuse it from one review to the next:
a cached prefix ends at the first byte that differs, so nothing that changes per run (the run id, its batch, a time or a
count) may come before the instructions and the slowly changing parts. The plugin side (the same system context for
every review) is checked in tests/test_review_hooks.mjs."""
import importlib.util, os, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from test_preview import Runner, signal  # noqa: E402

spec = importlib.util.spec_from_file_location('cache_prefix_assistant', Path(__file__).parent.parent / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

# Well under the instructions alone (about 11,000 characters, 2,700 tokens); a token is about 4 characters of English
MIN_SHARED_TOKENS = 2500


def shared_prefix(one, two):
    return os.path.commonprefix([one, two])


class ReviewCachePrefix(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'boundary': 'work:Acme'}], 'review_worker': {'enabled': False},
                           'delivery_enabled': False, 'telegram_owner': 'owner'}

    def review_message(self, source_id):
        """One whole review the way the service starts it (review_step), and the message it sent."""
        self.store.commit_page('work', {}, [signal(source_id, 1, f'Question {source_id}')])
        run_id = self.app.start_preview()['run_id']
        runner = Runner('admitted', 'ok')
        self.assertEqual(self.app.review_step(runner), 'admitted')
        self.app.review_step(runner)
        message = runner.requests[0]['message']
        return run_id, message

    def test_two_consecutive_reviews_share_a_long_identical_prefix(self):
        first_run, first = self.review_message('m1')
        second_run, second = self.review_message('m2')
        self.assertNotEqual(first_run, second_run)
        shared = shared_prefix(first, second)
        self.assertGreaterEqual(len(shared) // 4, MIN_SHARED_TOKENS)
        # The first byte that differs is this run's own part, after the instructions and the slow parts
        self.assertNotIn(first_run, shared)
        self.assertIn('End with exactly NO_REPLY.', shared)
        self.assertIn('Accounts: begin_analysis account_ids ["work"]', shared)
        self.assertGreaterEqual(len(shared), first.index('This turn: review run ') + len('This turn: review run '))

    def test_per_run_parts_come_after_everything_stable(self):
        stable_args = dict(preferences='- Dismissed 2 newsletters quickly', facts='- The owner prefers short replies.',
                           promises='- Send Sam the deck by Friday', sources='\n\nReading the connected sources: mail.')
        one = a.review_prompt('a' * 32, ['work'], **stable_args, slipped='- No answer for 8 days', roles='- Sam', unnamed='- two threads',
                              notes='- not mine', handoffs='- ask_id q1', splits='- split s1', boards='- Acme sale', sorting='- p1',
                              fitting='- p2', backfill='- org:x', first_look=True)
        two = a.review_prompt('b' * 32, ['work'], **stable_args)
        shared = shared_prefix(one, two)
        self.assertTrue(two[len(shared):].startswith('b' * 32), two[len(shared) - 40:len(shared) + 40])
        for slow in stable_args.values():
            self.assertIn(slow.strip(), shared)
        for per_run in ('No answer for 8 days', 'ask_id q1', 'split s1', 'Acme sale', 'org:x', 'first look', 'Possibly slipped'):
            self.assertNotIn(per_run, shared)
            self.assertIn(per_run, one)
        # No clock in the prompt: the same inputs give the same bytes a minute later
        self.assertEqual(two, a.review_prompt('b' * 32, ['work'], **stable_args))


if __name__ == '__main__':
    unittest.main()

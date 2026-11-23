"""A to-do that ends in a new post (X, LinkedIn, a forum) with no send of its own: the run is told the one step that
posts it, the last step the owner confirms (kind finish), and never leaves only a link to a composer and Mark done. It was a
guess the run made from refusals that didn't name it, so the same draft came back sometimes with Publish, sometimes
with Mark done."""
import tempfile
import unittest
from pathlib import Path

import next_actions as n
import machine.config as machine_config
import machine.main as machine_main
import test_x

POST = {'kind': 'finish', 'label': 'Publish on X', 'url': 'https://x.com/compose/post', 'message': 'Search got faster.', 'to_name': '@larkspurhq',
        'preview': 'New post from @larkspurhq: Search got faster.', 'instructions': 'Open the composer as @larkspurhq, enter exactly the text, post once.'}
COMPOSER = {'kind': 'open', 'label': 'Open the post', 'url': 'https://x.com/intent/tweet?text=Search%20got%20faster.'}


class NewPost(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'accounts': [test_x.ACCOUNT]}

    def todo(self, kind='routine.draft', act='post'):
        event = self.store.reviewed_event('x-sf', f'{kind}-{act}', kind, 'Post on X about search', 'Search got faster.', {'act': act} if act else {})
        sid = self.store.suggest(f'{kind}-{act}', 'Post on X about search', 'Search got faster.', [event])['id']
        self.store.decide(sid, 'accept', '', f'd-{sid}', 'dashboard')
        return sid

    def save(self, sid, *actions, **more):
        return self.app.action('prepare', {'suggestion_id': sid, 'body': 'The post is ready.', 'next_actions': list(actions),
                                           'outcome': 'needs_you', 'needs': 'Review and publish the post', **more})

    def test_a_new_post_as_an_x_send_names_the_step_that_posts_it(self):
        sid = self.todo()
        for label in ('Post on X', 'Send', 'Publish', None):
            with self.assertRaisesRegex(ValueError, r'kind:finish,label:Publish on X,url:https://x\.com/compose/post,message:'):
                self.save(sid, {'kind': 'x', **({'label': label} if label else {}), 'account_id': 'x-sf', 'body': 'Search got faster.'})
        self.save(sid, POST)  # what it says works as it says it
        with self.assertRaisesRegex(ValueError, 'Unsupported final step fields: account_id. Leave them out'):
            self.save(sid, {**POST, 'account_id': 'x-sf'})

    def test_a_link_to_a_composer_is_not_the_step(self):
        sid = self.todo(kind='email.message', act=None)
        for url in ('https://x.com/intent/post?text=a', 'https://twitter.com/intent/tweet?text=a', 'https://x.com/compose/post',
                    'https://www.linkedin.com/feed/?shareActive=true&text=a', 'https://www.linkedin.com/sharing/share-offsite/?url=a',
                    'https://bsky.app/intent/compose?text=a', 'https://www.reddit.com/r/gardening/submit?title=a'):
            with self.assertRaisesRegex(ValueError, 'only opens a composer.*kind:finish', msg=url):
                self.save(sid, {**COMPOSER, 'url': url})
        for url in ('https://x.com/larkspurhq/status/1979000000000000001', 'https://x.com/composers', 'https://www.linkedin.com/feed/update/1',
                    'https://example.com/x.com/compose/post'):
            self.assertEqual(n.check(dict(COMPOSER, url=url)), [], url)
        self.save(sid, COMPOSER, checked=True)  # one that is meant

    def test_a_routines_draft_comes_with_what_posts_or_sends_it(self):
        sid = self.todo()
        with self.assertRaisesRegex(ValueError, 'nothing in next_actions posts this draft.*kind:finish'):
            self.save(sid)
        # a channel with no posting step here is never blocked: its page, or words that say what they do
        self.save(sid, {'kind': 'open', 'label': 'Open forum', 'url': 'https://forum.example/new'}, needs='Post it in the forum')
        self.save(sid, needs='Pin it on the board in the canteen', checked=True)
        with self.assertRaisesRegex(ValueError, 'this Machine can’t do it there, add an Open link .* says where and how they post it'):
            self.save(sid, needs='Pin it on the board in the canteen')
        self.save(sid, needs='Which account should it go out from?')  # a question first
        self.save(sid, POST)
        with self.assertRaisesRegex(ValueError, 'nothing in next_actions sends this draft'):
            self.save(self.todo(act='send'))
        self.save(self.todo(kind='email.message', act=None))  # any other to-do

    def test_the_rules_say_it_before_a_run_tries(self):
        rules = (machine_config.ROOT / 'PREPARATION.md').read_text()
        self.assertIn('A new post (X, LinkedIn, anywhere) is a last step, never kind:x or an Open link.', rules)
        self.assertIn('publishing, posting', rules)


if __name__ == '__main__':
    unittest.main()

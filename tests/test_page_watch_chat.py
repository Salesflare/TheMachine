"""Watch a page from the owner's own main chat (the bridge's assistant_page_watch, page_watch): the watched pages, a new
one added with Settings' own steps (connect_start), one taken off (connect_remove); only in their own chat, after they
wrote there. A temporary store; the connect steps are replaced, so nothing is read or saved. No model call, no send."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('page_watch_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


class PageWatchChat(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'email': 'sam@acme.example', 'boundary': 'work:Acme'},
                                    {'id': 'page', 'service': 'web_page', 'url': 'https://tools.example/pricing',
                                     'display_name': 'tools.example/pricing'}]}
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        self.calls = []
        self.app.connect_action = self.connect
        self.app.action('web_chat_said', {'message_id': 'run-1'})  # the owner just wrote in their own chat

    def connect(self, name, args):
        self.calls.append((name, args))
        return {'session': 's1', 'state': 'done'} if name == 'connect_start' else {'removed': args.get('account')}

    def watch(self, **args):
        return self.app.action('page_watch', {'_owner_chat': True, **args})

    def test_lists_the_watched_pages(self):
        self.store.commit_page('page', {'read_at': 1}, [])
        with self.store.connect() as db:
            db.execute("UPDATE checkpoints SET error='web_page_robots' WHERE account_id='page'")
        [page] = self.watch(do='list')['pages']
        self.assertEqual((page['id'], page['name']), ('page', 'tools.example/pricing'))
        self.assertIn('automated readers', page['problem'])

    def test_adds_with_settings_own_steps(self):
        out = self.watch(do='add', url='www.news.example/jobs')
        self.assertEqual(out['added'], 'news.example/jobs')
        [(name, args)] = self.calls
        self.assertEqual(name, 'connect_start')
        self.assertEqual(args, {'name': 'web_page', 'form': True, 'answers': {'url': 'https://www.news.example/jobs'},
                                'scope': 'work', 'company': 'Acme'})
        self.assertIsNone(self.watch(do='add', url='https://tools.example/pricing')['added'])  # already watched
        self.assertEqual(len(self.calls), 1)
        with self.assertRaisesRegex(Exception, 'public https'):
            self.watch(do='add', url='https://192.168.1.1/')

    def test_removes_one_from_the_list(self):
        self.assertEqual(self.watch(do='remove', id='page')['removed'], 'tools.example/pricing')
        self.assertEqual(self.calls, [('connect_remove', {'account': 'page'})])
        self.assertIsNone(self.watch(do='remove', id='nope')['removed'])

    def test_only_on_the_owners_own_request_in_their_own_chat(self):
        with self.assertRaisesRegex(ValueError, 'own main chat'):
            self.app.action('page_watch', {'do': 'list'})
        self.app.owner_said_last = None
        with self.assertRaisesRegex(ValueError, 'only when the owner asks'):
            self.watch(do='add', url='https://news.example/jobs')
        self.assertEqual(self.calls, [])
        self.assertIn('page_watch', a.OWNER_ACTIONS)  # never the local CLI, the agent's own tool
        self.assertNotIn('page_watch', a.DASHBOARD_ACTIONS)


if __name__ == '__main__':
    unittest.main()

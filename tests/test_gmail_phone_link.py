"""Open in Gmail on a phone. mail.google.com serves a phone its mobile site, which drops the desktop link's
#all/<message> and lands in the inbox. A Gmail message also carries a phone link that opens its conversation on the
mobile site, in the account the desktop link names; the dashboard uses it on a phone (test_email_frame_layout_dashboard.mjs)."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('gmail_phone_link_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
from machine.sources.gmail import phone_link  # noqa: E402

DESKTOP = 'https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002'


class PhoneLink(unittest.TestCase):
    def test_the_conversation_in_the_links_account(self):
        self.assertEqual(phone_link(DESKTOP, '18c0ffee00000001'),
                         'https://mail.google.com/mail/mu/mp/?authuser=owner%40example.com#cv/All%20Mail/18c0ffee00000001')

    def test_none_without_gmails_own_link_or_a_thread(self):
        self.assertIsNone(phone_link(DESKTOP, None))
        self.assertIsNone(phone_link(DESKTOP, 'not a thread'))
        self.assertIsNone(phone_link(DESKTOP, '18c0ffee/../x'))
        self.assertIsNone(phone_link('https://mail.google.com/mail/u/0/#all/18c0ffee00000002', '18c0ffee00000001'))
        self.assertIsNone(phone_link('https://evil.example/mail/u/?authuser=owner%40example.com#all/1', '18c0ffee00000001'))
        self.assertIsNone(phone_link(None, '18c0ffee00000001'))

    def test_a_gmail_message_view_carries_it_and_other_kinds_do_not(self):
        with tempfile.TemporaryDirectory() as folder:
            store = a.Store(Path(folder) / 'events.sqlite')
            mail = {'account_id': 'work', 'source_id': '18c0ffee00000002', 'kind': 'gmail.message', 'occurred_at': '2026-11-12T15:56:00+00:00',
                    'title': 'Account notice', 'body': 'Hello.', 'deleted': False,
                    'metadata': {'from': 'Example Cloud <hello@cloud.example>', 'thread_id': '18c0ffee00000001', 'source_url': DESKTOP}}
            chat = {'account_id': 'work', 'source_id': 'c1', 'kind': 'slack.message', 'occurred_at': '2026-11-12T15:57:00+00:00',
                    'title': 'A message', 'body': 'Hi.', 'deleted': False,
                    'metadata': {'from': 'Sam', 'thread_id': '18c0ffee00000001', 'source_url': DESKTOP}}
            store.commit_page('work', {}, [mail, chat], None)
            views = store.event_views([1, 2])
        self.assertEqual(views[0]['url'], DESKTOP)
        self.assertEqual(views[0]['phone_url'], phone_link(DESKTOP, '18c0ffee00000001'))
        self.assertNotIn('phone_url', views[1])


if __name__ == '__main__':
    unittest.main()

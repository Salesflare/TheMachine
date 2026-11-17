"""Open in Gmail. A Gmail message keeps the link it was synced with (/mail/u/?authuser=<address>#all/<message>), which
on a phone opened the inbox or an unrelated search instead of the message. Every place that shows it now opens
/mail/u/<address>/#all/<thread>: the conversation, in the account it came to, on a computer and on a phone."""
import sys
import tempfile
import unittest
from pathlib import Path
import machine.main as machine_main

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from machine.sources.gmail import gmail_link, message_event, open_link  # noqa: E402
from machine.store import message_view  # noqa: E402

STORED = 'https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002'
OPENS = 'https://mail.google.com/mail/u/owner@example.com/#all/18c0ffee00000001'


class GmailLink(unittest.TestCase):
    def test_the_thread_in_the_account_it_came_to(self):
        self.assertEqual(gmail_link('owner@example.com', '18c0ffee00000001'), OPENS)
        self.assertEqual(gmail_link('pat+work@example.com', '18c0ffee00000001'),
                         'https://mail.google.com/mail/u/pat%2Bwork@example.com/#all/18c0ffee00000001')

    def test_a_stored_link_opens_its_thread(self):
        self.assertEqual(open_link(STORED, '18c0ffee00000001'), OPENS)

    def test_without_a_thread_the_message_itself(self):
        mine = 'https://mail.google.com/mail/u/owner@example.com/#all/18c0ffee00000002'
        self.assertEqual(open_link(STORED, None), mine)
        self.assertEqual(open_link(STORED, ''), mine)
        self.assertEqual(open_link(STORED, '18c0ffee/../x'), mine)

    def test_other_links_stay_as_they_are(self):
        for url in ('https://outlook.office365.com/owa/?ItemID=AAk%3D', 'https://mail.google.com/mail/u/0/#all/18c0ffee00000002',
                    'https://evil.example/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002',
                    STORED + '/../x', OPENS, None, ''):
            self.assertEqual(open_link(url, '18c0ffee00000001'), url)

    def test_a_synced_message_keeps_its_stored_link(self):
        """The sync's link is unchanged, so no message is read again as an edit (its content hash stays): links are
        made where they show."""
        raw = {'id': '18c0ffee00000002', 'threadId': '18c0ffee00000001', 'internalDate': '1762962960000', 'labelIds': ['INBOX'],
               'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'Subject', 'value': 'Account notice'},
                                                                  {'name': 'From', 'value': 'Example Cloud <hello@cloud.example>'}],
                           'body': {'data': 'SGVsbG8u'}}}
        event = message_event({'id': 'work', 'email': 'owner@example.com'}, raw)
        self.assertEqual(event['metadata']['source_url'], STORED)

    def test_the_viewer_and_list_rows_open_the_thread(self):
        with tempfile.TemporaryDirectory() as folder:
            store = machine_main.Store(Path(folder) / 'events.sqlite')
            mail = {'account_id': 'work', 'source_id': '18c0ffee00000002', 'kind': 'gmail.message', 'occurred_at': '2026-11-12T15:56:00+00:00',
                    'title': 'Account notice', 'body': 'Hello.', 'deleted': False,
                    'metadata': {'from': 'Example Cloud <hello@cloud.example>', 'thread_id': '18c0ffee00000001', 'source_url': STORED}}
            older = {**mail, 'source_id': '18c0ffee00000003', 'metadata': {'from': 'Example Cloud <hello@cloud.example>',
                                                                          'source_url': STORED.replace('0002', '0003')}}
            store.commit_page('work', {}, [mail, older], None)
            views = store.event_views([1, 2])
        self.assertEqual(views[0]['url'], OPENS)
        self.assertNotIn('phone_url', views[0])
        self.assertEqual(views[1]['url'], 'https://mail.google.com/mail/u/owner@example.com/#all/18c0ffee00000003')
        row = message_view.list_row('gmail.message', 'Account notice', 'Hello.', mail['metadata'])
        self.assertEqual(row['url'], OPENS)
        self.assertEqual(row['app'], 'Gmail')


if __name__ == '__main__':
    unittest.main()

"""Open in Gmail. A Gmail message has one link, on a computer and a phone alike: /mail/u/?authuser=<address>#all/<id>,
the address encoded and the API's hex message id (the form the Gmail app on a phone opens). The phone-only link to
Gmail's old mobile site (/mail/mu/mp/...#cv/...) is gone: it ended in an unrelated msgid: search. Android's browser
hands the link to the Gmail app (test_gmail_app_dashboard.mjs), the phone app too (test_mobile_shell.py)."""
import sys
import tempfile
import unittest
from pathlib import Path
import machine.main as machine_main

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from machine.sources.gmail import gmail_link, message_event  # noqa: E402
from machine.store import message_view  # noqa: E402

GMAIL = 'https://mail.google.com/mail/u/?authuser=owner%40example.com#all/18c0ffee00000002'


class GmailLink(unittest.TestCase):
    def test_the_message_in_the_account_it_came_to(self):
        self.assertEqual(gmail_link('owner@example.com', '18c0ffee00000002'), GMAIL)
        self.assertEqual(gmail_link('pat+work@example.com', '18c0ffee00000002'),
                         'https://mail.google.com/mail/u/?authuser=pat%2Bwork%40example.com#all/18c0ffee00000002')

    def test_a_synced_message_carries_it(self):
        raw = {'id': '18c0ffee00000002', 'threadId': '18c0ffee00000001', 'internalDate': '1762962960000', 'labelIds': ['INBOX'],
               'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'Subject', 'value': 'Account notice'},
                                                                  {'name': 'From', 'value': 'Example Cloud <hello@cloud.example>'}],
                           'body': {'data': 'SGVsbG8u'}}}
        self.assertEqual(message_event({'id': 'work', 'email': 'owner@example.com'}, raw)['metadata']['source_url'], GMAIL)

    def test_the_viewer_and_list_rows_open_it_with_no_phone_link(self):
        with tempfile.TemporaryDirectory() as folder:
            store = machine_main.Store(Path(folder) / 'events.sqlite')
            mail = {'account_id': 'work', 'source_id': '18c0ffee00000002', 'kind': 'gmail.message', 'occurred_at': '2026-11-12T15:56:00+00:00',
                    'title': 'Account notice', 'body': 'Hello.', 'deleted': False,
                    'metadata': {'from': 'Example Cloud <hello@cloud.example>', 'thread_id': '18c0ffee00000001', 'source_url': GMAIL}}
            store.commit_page('work', {}, [mail], None)
            view = store.event_views([1])[0]
        self.assertEqual(view['url'], GMAIL)
        self.assertNotIn('phone_url', view)
        row = message_view.list_row('gmail.message', 'Account notice', 'Hello.', mail['metadata'])
        self.assertEqual((row['url'], row['app']), (GMAIL, 'Gmail'))
        self.assertNotIn('phone_url', row)


if __name__ == '__main__':
    unittest.main()

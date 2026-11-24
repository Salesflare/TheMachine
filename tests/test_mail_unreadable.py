"""A mail whose text can't be read (S/MIME, PGP, winmail.dat) says so: to whatever reads messages, and in the viewer."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path

import embeddings
import ms_graph
import routine_patterns
from machine.main import Store
from machine.sources.gmail import message_event
from machine.store.judged_words import judged
from machine.store.review import review_view
from machine.store.voices import own_text
from machine.text import own_part
from machine.web.handler import event_glance

HEAD = 'From: Kim <kim@example.org>\r\nTo: me@example.com\r\nSubject: Offer\r\nMIME-Version: 1.0\r\n'
SEALED = 'Content-Type: application/pkcs7-mime; smime-type={}; name="smime.p7m"\r\nContent-Transfer-Encoding: base64\r\n\r\nAAAA\r\n'
WINMAIL = '--B\r\nContent-Type: application/ms-tnef; name="winmail.dat"\r\nContent-Transfer-Encoding: base64\r\n\r\nAAAA\r\n'
MIXED = 'Content-Type: multipart/mixed; boundary=B\r\n\r\n'
MAILS = {
    'encrypted': SEALED.format('enveloped-data'),
    'signed': SEALED.format('signed-data'),
    'winmail': MIXED + WINMAIL + '--B--\r\n',
}
PGP = ('Content-Type: multipart/encrypted; protocol="application/pgp-encrypted"; boundary=B\r\n\r\n--B\r\nContent-Type: application/pgp-encrypted\r\n\r\nVersion: 1\r\n'
       '--B\r\nContent-Type: application/octet-stream\r\n\r\nAAAA\r\n--B--\r\n')


def event(mime, snippet=''):
    return message_event({'id': 'work', 'email': 'me@example.com', 'service': 'imap'}, {
        'id': 'm1', 'threadId': 't', 'internalDate': '1809000000000', 'labelIds': ['INBOX'], 'snippet': snippet,
        'payload': ms_graph.payload((HEAD + mime).encode())}, {})


class Unreadable(unittest.TestCase):
    def test_the_reason_is_kept_and_said(self):
        for reason, mime in {**MAILS, 'PGP': PGP}.items():
            with self.subTest(reason):
                reason = 'encrypted' if reason == 'PGP' else reason
                got = event(mime, 'garbled preview')
                self.assertEqual((got['metadata']['unreadable'], got['body']), (reason, ''))

    def test_a_mail_with_words_or_without_any_is_as_before(self):
        text = '--B\r\nContent-Type: text/plain\r\n\r\nSee the file.\r\n'
        self.assertEqual(event(MIXED + text + WINMAIL + '--B--\r\n')['body'].strip(), 'See the file.')
        attached = MIXED + '--B\r\nContent-Type: message/rfc822\r\n\r\nSubject: Old\r\n' + SEALED.format('enveloped-data') + '--B--\r\n'
        for mime in ('Content-Type: text/plain\r\n\r\n', attached):
            got = event(mime)
            self.assertNotIn('unreadable', got['metadata'])
            self.assertEqual(got['body'].strip(), '')

    def test_reviews_and_checks_are_told_and_the_viewer_shows_one_line_of_its_own(self):
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / 'events.sqlite')
            before = event(MAILS['encrypted'])
            store.commit_page('work', {}, [{**before, 'body': '', 'metadata': {k: v for k, v in before['metadata'].items() if k != 'unreadable'}}])
            with store.connect() as db:
                old = [tuple(r) for r in db.execute('SELECT id,body FROM events')]
            store.commit_page('work', {}, [before])  # read again: a mail that is in stays as it is, with no second review
            with store.connect() as db:
                self.assertEqual([tuple(r) for r in db.execute('SELECT id,body FROM events')], old)
            store.commit_page('work', {}, [{**event(MAILS['encrypted']), 'source_id': 'm2'}])
            with store.connect() as db:
                row = dict(db.execute("SELECT * FROM events WHERE source_id='m2'").fetchone())
                self.assertIn("couldn't be read", judged(db, [row['id']])[row['id']])
            self.assertIn("couldn't be read", review_view(row)['body'])
            shown = store.event_views([row['id']])[0]
            self.assertEqual((shown['body'], shown['unreadable']), ('', 'Read it in your mail app.'))

    def test_no_list_or_preview_shows_the_line_models_read(self):
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / 'events.sqlite')
            store.commit_page('work', {}, [event(mime) | {'source_id': name} for name, mime in MAILS.items()])
            rows = store.events(['work'])
            self.assertEqual([r['body'] for r in rows], [''] * 3)
            account = {'id': 'work', 'email': 'me@example.com', 'service': 'imap'}
            glances = [event_glance(dict(r), [account]) for r in rows]
            self.assertEqual([g['preview'] for g in glances], [''] * 3)
            for shown in (*glances, *store.event_views([r['id'] for r in rows])):
                self.assertNotIn("couldn't be read", json.dumps(shown, default=str))
            self.assertEqual(store.events(['work'], query="couldn't be read"), [])
            self.assertTrue(all("couldn't" not in embeddings.document(r['title'], r['body']) for r in rows))

    def test_the_owners_own_sealed_mail_is_never_their_words(self):
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / 'events.sqlite')
            sent = event(MAILS['encrypted'])
            for n in range(1, 13):  # on a rhythm, to the same person
                store.commit_page('work', {}, [{**sent, 'source_id': f's{n}', 'occurred_at': f'2027-{n:02}-01T09:00:00+00:00',
                                               'metadata': {**sent['metadata'], 'labels': ['SENT']}}])
            self.assertEqual(store.own_messages(), [])
            self.assertNotIn("couldn't be read", json.dumps(store.voice_sample(), default=str))
            self.assertEqual(own_text(sent['body']), '')
            self.assertEqual(own_part(sent['body'], sent['title']), '')
            with store.connect() as db:
                found = routine_patterns.sent(db, dt.date(2027, 12, 2), dt.timezone.utc)
            self.assertNotIn("couldn't be read", json.dumps(found, default=str))

    def test_the_dashboard_says_it_in_one_line(self):
        root = Path(__file__).resolve().parent.parent
        self.assertIn("t(o.unreadable||'No description.')", (root / 'dashboard' / 'events-message.js').read_text())


if __name__ == '__main__':
    unittest.main()

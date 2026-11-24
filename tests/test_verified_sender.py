"""Whether a mail's sender address is verified (verified_sender.py): only what the owner's own mail service wrote about the
address's own domain counts, and it never makes a stored message a new version. Made-up mail only."""
import base64
import tempfile
import unittest
from pathlib import Path

import machine.main as machine_main
import machine.sources.gmail as gmail
import message_seal
import verified_sender

GMAIL, OUTLOOK, IMAP = ({'id': 'home', 'service': s, 'email': 'owner@example.com'} for s in ('gmail', 'outlook', 'imap'))
PASS = 'mx.google.com; dkim=pass header.i=@rugs.example header.s=a; spf=pass smtp.mailfrom=b@rugs.example; dmarc=pass (p=NONE) header.from=rugs.example'
MICROSOFT = 'spf=pass (sender IP is 192.0.2.1) smtp.mailfrom=rugs.example; dkim=pass (signature was verified) header.d=rugs.example;dmarc=pass action=none header.from=rugs.example'


def heads(*results, sender='Rugs <no-reply@rugs.example>'):
    return [{'name': 'From', 'value': sender}, *({'name': 'Authentication-Results', 'value': r} for r in results)]


def message(*results):
    return {'id': 'm1', 'threadId': 't1', 'labelIds': ['INBOX'], 'internalDate': '1792483200000', 'snippet': '', 'payload': {
        'headers': [*heads(*results), {'name': 'Subject', 'value': 'Your carpet'}], 'mimeType': 'text/plain', 'body': {'data': base64.urlsafe_b64encode(b'It comes.').decode()}}}


class VerifiedSender(unittest.TestCase):
    def test_what_the_service_checked(self):
        for account, results, want in ((GMAIL, PASS, True), (OUTLOOK, MICROSOFT, True), (IMAP, PASS, False), (GMAIL, MICROSOFT, False),
                                       (GMAIL, 'mx.google.com; dkim=pass header.d=mail.rugs.example', True), (GMAIL, 'mx.google.com; dkim=pass header.d=other.example', False),
                                       (GMAIL, 'mx.google.com; dkim=fail header.d=rugs.example; dmarc=fail header.from=rugs.example', False),
                                       (GMAIL, 'mx.google.com; spf=pass smtp.mailfrom=rugs.example', False), (GMAIL, 'mx.google.com; dkim=pass header.d=example', False),
                                       (GMAIL, 'mx.other.example; dmarc=pass header.from=rugs.example', False), (GMAIL, 'mx.google.com; dkim=pass header.d=badrugs.example', False)):
            with self.subTest(results=results):
                self.assertIs(verified_sender.verified(account, heads(results)), want)
        self.assertFalse(verified_sender.verified(GMAIL, heads()))

    def test_nothing_the_sender_wrote_counts(self):
        failed = 'mx.google.com; dkim=none; spf=pass smtp.mailfrom={}; dmarc=fail header.from=rugs.example'
        self.assertFalse(verified_sender.verified(GMAIL, heads(failed.format('x@x.example'), PASS)))  # a header of their own, below the service's
        for words in ('"a; dmarc=pass header.from=rugs.example"@x.example', 'x@x.example (; dmarc=pass header.from=rugs.example (y))'):
            self.assertFalse(verified_sender.verified(GMAIL, heads(failed.format(words))), words)
        for sender in ('a@x.example, b@rugs.example', 'b@rugs.example, a@x.example', 'rugs.example', '"no-reply@rugs.example" <x@x.example>'):
            self.assertFalse(verified_sender.verified(GMAIL, heads(PASS, sender=sender)), sender)

    def test_kept_with_the_message_sealed_and_never_a_new_version(self):
        self.assertNotIn(verified_sender.KEY, message_seal.PLAIN_METADATA)
        plain, checked = gmail.message_event(GMAIL, message()), gmail.message_event(GMAIL, message(PASS))
        self.assertEqual((plain['metadata'].get(verified_sender.KEY), checked['metadata'].get(verified_sender.KEY)), (None, True))
        for first, again in ((plain, checked), (checked, plain)):
            with tempfile.TemporaryDirectory() as temp:
                store = machine_main.Store(Path(temp) / 'events.sqlite')
                store.commit_page('home', {}, [first])
                with store.connect() as db:
                    before = tuple(db.execute('SELECT version,metadata FROM events').fetchone())
                store.commit_page('home', {}, [again])
                with store.connect() as db:
                    self.assertEqual(tuple(db.execute('SELECT version,metadata FROM events').fetchone()), before)
                self.assertEqual(store.events(['home'])[0]['metadata'].get(verified_sender.KEY), first['metadata'].get(verified_sender.KEY))


if __name__ == '__main__':
    unittest.main()

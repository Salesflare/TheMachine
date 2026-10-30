"""A reply always goes into the thread of the email it answers (next_actions.fill_reply, reply_origin, preflight;
assistant.replied_to): a draft with a Re: subject but no In-Reply-To gets the to-do's email it answers; from the same
Gmail mailbox it carries that thread's threadId; from another mailbox it keeps In-Reply-To and References (so it threads
for the recipient) and the card says so; a reply that can't be linked is refused, never sent as a new thread.
No network: the Gmail call is replaced. Nothing is sent."""
import base64
import email
import json
import unittest
from unittest.mock import patch

import assistant as a
import next_actions as n

HOME = 'owner@home.test'
WORK = 'owner@work.test'
CONFIG = {'accounts': [{'id': 'home-gmail', 'email': HOME, 'service': 'gmail', 'transport': 'broker', 'boundary': 'personal'},
                       {'id': 'work-gmail', 'email': WORK, 'service': 'gmail', 'transport': 'broker', 'boundary': 'work:Acme'}]}
ORIGINAL = '<order-42@shop.test>'


def row(account_id, source_id, subject, sender, to, message_id, thread_id, labels=('INBOX',), in_reply_to=''):
    """A to-do's email as the review reads it (events: metadata, account_id, source_id, title)."""
    return {'metadata': json.dumps({'from': sender, 'to': to, 'message-id': message_id, 'in-reply-to': in_reply_to,
                                    'thread_id': thread_id, 'labels': list(labels)}),
            'account_id': account_id, 'source_id': source_id, 'title': subject}


SHOP = row('home-gmail', '1a181709054ad026', 'Payment failed for order 42', '"Sam Shop" <sam@shop.test>', HOME,
           ORIGINAL, '1a181709054ad026', in_reply_to='<earlier@shop.test>')


def draft(**extra):
    """What the review drafted on the day: a Re: subject, Send reply, and no In-Reply-To or thread."""
    return {'kind': 'email', 'label': 'Send reply', 'account_id': 'home-gmail', 'to': ['sam@shop.test'],
            'subject': 'Re: Payment failed for order 42', 'body': 'Hello Sam,\n\nAlready paid for order 43.\n\nAlex', **extra}


def save(value, rows, allowed=('home-gmail',)):
    """The review's save path: fill_reply and reply_to_newest, then validate with the to-do's emails."""
    replied = a.replied_to(rows)
    action = n.validate(a.reply_to_newest(rows, n.fill_reply(value, replied)), CONFIG, list(allowed), replied=replied)
    if n.unlinked_reply(action):
        raise ValueError(n.unlinked_reply(action))
    return action


def mime(action):
    return email.message_from_bytes(n.mime_bytes(action, {'rfc_message_id': '<job-1@home.test>'}))


class SameGmailMailbox(unittest.TestCase):
    def test_a_re_subject_without_in_reply_to_answers_the_todos_email_in_its_thread(self):
        action = save(draft(), [SHOP])
        self.assertEqual((action['in_reply_to'], action['references'], action['thread_id']),
                         (ORIGINAL, '<earlier@shop.test> ' + ORIGINAL, '1a181709054ad026'))
        self.assertNotIn('reply_elsewhere', action)
        headers = mime(action)
        self.assertEqual((headers['In-Reply-To'], headers['References']), (ORIGINAL, '<earlier@shop.test> ' + ORIGINAL))
        sent = []
        transport = n.EmailTransport(CONFIG, lambda *args: None, None)
        with patch.object(n.google_api, 'call', lambda *args, **kw: sent.append(kw['body']) or {'id': 'sent-1'}):
            self.assertEqual(transport.send({**action, 'signature': False}, {'rfc_message_id': '<job-1@home.test>'}),
                             {'message_id': 'sent-1'})
        self.assertEqual(sent[0]['threadId'], '1a181709054ad026')  # Gmail files it in the original's thread
        raw = email.message_from_bytes(base64.urlsafe_b64decode(sent[0]['raw'] + '=='))
        self.assertEqual(raw['In-Reply-To'], ORIGINAL)

    def test_a_wrong_thread_from_the_model_is_replaced_by_the_originals(self):
        action = save(draft(in_reply_to=ORIGINAL, thread_id='abc123'), [SHOP])
        self.assertEqual(action['thread_id'], '1a181709054ad026')

    def test_a_send_reply_with_another_subject_still_answers_the_recipients_newest_email(self):
        older = row('home-gmail', 'o1', 'Your order 42', 'sam@shop.test', HOME, '<old@shop.test>', 'o1')
        action = save(draft(subject='Re: the duplicate order'), [SHOP, older])
        self.assertEqual(action['in_reply_to'], ORIGINAL)

    def test_a_new_email_stays_new(self):
        action = save(draft(label='Send', subject='Quote for four speakers'), [SHOP])
        self.assertNotIn('in_reply_to', action)
        self.assertNotIn('thread_id', action)


class AnotherMailbox(unittest.TestCase):
    def test_from_another_gmail_it_keeps_the_headers_drops_the_thread_and_says_so(self):
        action = save(draft(account_id='work-gmail', thread_id='1a181709054ad026'), [SHOP], ('home-gmail', 'work-gmail'))
        self.assertEqual((action['from'], action['in_reply_to']), (WORK, ORIGINAL))
        self.assertNotIn('thread_id', action)  # a thread of the home mailbox: Gmail would refuse it from work
        self.assertNotIn('snooze_days', action)
        self.assertEqual(action['reply_elsewhere'], HOME)
        self.assertIn(n.REPLY_ELSEWHERE.format(WORK, HOME), n.email_preview(action))
        self.assertEqual(mime(action)['In-Reply-To'], ORIGINAL)  # the recipient's mail app still threads it
        sent = []
        transport = n.EmailTransport(CONFIG, lambda *args: None, None)
        with patch.object(n.google_api, 'call', lambda *args, **kw: sent.append(kw['body']) or {'id': 'sent-2'}):
            transport.send({**action, 'signature': False}, {'rfc_message_id': '<job-2@work.test>'})
        self.assertNotIn('threadId', sent[0])

    def test_the_same_email_in_the_sending_mailbox_is_answered_in_that_mailbox(self):
        copy = row('work-gmail', 'w1', SHOP['title'], 'sam@shop.test', HOME + ', ' + WORK, ORIGINAL, 'beef01')
        action = save(draft(account_id='work-gmail'), [SHOP, copy], ('home-gmail', 'work-gmail'))
        self.assertEqual(action['thread_id'], 'beef01')
        self.assertNotIn('reply_elsewhere', action)

    def test_the_model_cannot_set_where_a_reply_goes(self):
        for field in ('reply_elsewhere', 'reply_to_id'):
            with self.assertRaisesRegex(ValueError, 'Unsupported email fields'):
                save(draft(**{field: 'x'}), [SHOP])


class NeverSilentlyNew(unittest.TestCase):
    def test_a_reply_that_answers_no_known_email_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'reads as a reply'):
            save(draft(to=['someone@else.test']), [SHOP])
        self.assertIn('reads as a reply', n.unlinked_reply(n.validate(draft(subject='AW: Zahlung', label='Send'), CONFIG, ['home-gmail'])))
        self.assertIsNone(n.unlinked_reply(n.validate(draft(label='Send', subject='Zahlung'), CONFIG, ['home-gmail'])))

    def test_an_unlinked_reply_already_on_a_card_is_not_sent(self):
        stored = {**draft(), 'from': HOME, 'cc': [], 'bcc': [], 'signature': False}
        calls = []
        with patch.object(n.google_api, 'call', lambda *args, **kw: calls.append(args) or {}):
            with self.assertRaisesRegex(ValueError, 'start a new thread. Nothing was sent'):
                n.EmailTransport(CONFIG, lambda *args: None, None).preflight(stored)
        self.assertEqual(calls, [])

    def test_reply_prefixes(self):
        for subject in ('Re: x', 'RE:x', 'AW: x', 'Antw: x', 'SV: x', 'Re[2]: x'):
            self.assertTrue(n.reads_as_reply({'kind': 'email', 'subject': subject}), subject)
        for subject in ('Fwd: x', 'Report: x', 'Regarding x'):
            self.assertFalse(n.reads_as_reply({'kind': 'email', 'subject': subject}), subject)
        self.assertEqual(n.base_subject('Re: AW:  Payment  failed'), 'payment failed')


if __name__ == '__main__':
    unittest.main()

"""A sent to-do names what went out ("Telegram message sent"), for every kind of message a to-do can send
(machine/kinds.py SENDS), in the to-do Telegram shows (machine/cards.card). A new send kind adds its message id here,
so it can't fall back to "Email sent". The dashboard's line: tests/test_sent_lines_dashboard.mjs. Made-up data."""
import unittest

import machine.cards as machine_cards
import machine.kinds as kinds

# a message id each kind's send returns, and the line its sent to-do shows
SENT = {
    'email': ('<m1@mail.example>', 'Email sent'),
    'linkedin': ('urn:li:msg:1', 'LinkedIn message sent'),
    'slack': ('slack:C1:1700000000.0001', 'Slack message sent'),
    'x': ('xdm:1', 'X message sent'),
    'whatsapp': ('whatsapp:3EB0AA', 'WhatsApp message sent'),
    'telegram': ('telegram:42:7', 'Telegram message sent'),
    'signal': ('signal:chat1:1700000000000', 'Signal message sent'),
    'intercom': ('intercom:9:1', 'Sent as Alex in Intercom'),
    'doc_reply': ('doc:c1:r1', 'Reply posted in the doc'),
}


def row(kind, message_id):
    action = {'kind': kind, 'label': 'Send reply', 'revision': 'r1', 'body': 'Thanks, see you then.', 'to_name': 'Sam',
              'as_name': 'Alex', 'state': {'status': 'sent', 'message_id': message_id}}
    return {'id': 's1', 'title': 'Reply to Sam', 'body': 'Drafted a reply.', 'status': 'completed', 'scope': 'work',
            'next_actions': [action]}


class SentLineTest(unittest.TestCase):
    def test_every_send_kind_has_its_sample(self):
        self.assertEqual(set(SENT), set(kinds.SENDS), 'a new send kind adds its message id and sent line to SENT')

    def test_every_send_kind_names_what_went_out(self):
        for kind, (message_id, line) in SENT.items():
            with self.subTest(kind=kind):
                text = machine_cards.card(row(kind, message_id))
                self.assertIn('✓ ' + line, text)
                if kind != 'email':
                    self.assertNotIn('Email sent', text)
                self.assertNotRegex(text, r'\bYou (sent|replied|posted)')


if __name__ == '__main__':
    unittest.main()

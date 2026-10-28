"""A reply goes out with the paragraph breaks its draft showed, on every channel that sends one: Gmail and Outlook (the
same MIME), Slack, WhatsApp, LinkedIn and X. A draft or edit with Windows line ends, or a "blank" line holding only
spaces, used to reach an HTML mail as an empty <div> with no height, so the blank line between paragraphs was lost.
No live sends: every transport is faked."""
import email
import email.policy
import json
import subprocess
import unittest
from unittest.mock import patch

import next_actions as n

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'credential': 'maton',
         'credential_variable': 'KEY', 'connection_id': 'conn-1', 'user_id': 'UOWNER1'}
WA = {'id': 'wa', 'service': 'whatsapp', 'transport': 'wacli-local', 'store': '/tmp/wa-store', 'boundary': 'personal:whatsapp'}
CHAT = '32470000000@s.whatsapp.net'
CONFIG = {'wacli': '/opt/wacli', 'accounts': [GMAIL, SLACK, WA]}
# As a model or a pasted edit can write it: Windows line ends, and blank lines that hold a space or a tab.
DRAFT = 'Hi Sam,\r\n\r\nThe plan is ready.\r\nIt covers both teams.\r\n \r\nCan we talk Friday?\n\t\nCheers,\n\nAlex'
SHOWN = 'Hi Sam,\n\nThe plan is ready.\nIt covers both teams.\n\nCan we talk Friday?\n\nCheers,\n\nAlex'


def parts(raw):
    message = email.message_from_bytes(raw, policy=email.policy.default)
    return {p.get_content_type(): p.get_content().replace('\r\n', '\n') for p in message.walk() if p.get_content_maintype() == 'text'}


class ParagraphBreaks(unittest.TestCase):
    def test_a_draft_keeps_its_paragraphs_as_shown(self):
        self.assertEqual(n.paragraphs(DRAFT), SHOWN)
        self.assertEqual(n.paragraphs('One\rTwo'), 'One\nTwo')
        self.assertEqual(n.paragraphs(SHOWN), SHOWN)  # nothing else changes

    def email(self):
        return n.validate({'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example'], 'subject': 'Plan', 'body': DRAFT},
                          CONFIG, ['work'])

    def test_gmail_and_outlook_send_the_blank_lines(self):
        action = self.email()
        self.assertEqual(action['body'], SHOWN)
        sent = parts(n.mime_bytes(action, {'rfc_message_id': '<id@x>'}))
        self.assertIn('<div>It covers both teams.</div><div><br></div><div>Can we talk Friday?</div><div><br></div><div>Cheers,</div>', sent['text/html'])
        self.assertNotRegex(sent['text/html'], r'<div>\s+</div>')
        self.assertTrue(sent['text/plain'].startswith(SHOWN))
        # Outlook sends the same MIME through Microsoft Graph.
        posted = []
        transport = n.EmailTransport({'accounts': [{**GMAIL, 'service': 'outlook'}]}, None, None)
        with patch.object(n.ms_graph, 'scopes', return_value={'Mail.Send', 'Mail.ReadWrite'}), \
                patch.object(n.ms_graph, 'call', side_effect=lambda *args, **kw: posted.append(kw.get('body')) or {'id': 'M1'}), \
                patch.object(transport, 'signature', return_value=''):
            transport.outlook_send(action, {'rfc_message_id': '<id@x>'}, transport.config['accounts'][0])
        self.assertEqual(parts(__import__('base64').b64decode(posted[0])), sent)

    def test_an_owner_edit_keeps_them_too(self):
        action = {**self.email(), 'revision': 'x'}
        self.assertEqual(n.revise(action, body=DRAFT)['body'], SHOWN)
        slack = {'kind': 'slack', 'account_id': 'slack', 'to_name': 'Sam', 'to_email': 'sam@example.com', 'body': 'Hi', 'revision': 'x'}
        self.assertEqual(n.revise(slack, body=DRAFT)['body'], SHOWN)

    def test_slack_posts_the_blank_lines(self):
        action = n.validate({'kind': 'slack', 'account_id': 'slack', 'to_email': 'sam@example.com', 'to_name': 'Sam', 'body': DRAFT}, CONFIG, ['slack'])
        self.assertEqual(n.slack_text(action['body']), SHOWN)

    def test_whatsapp_sends_the_blank_lines(self):
        action = n.validate({'kind': 'whatsapp', 'account_id': 'wa', 'chat_id': CHAT, 'body': DRAFT}, CONFIG, ['wa'],
                            whatsapp_chats={CHAT: {'account_id': 'wa', 'name': 'Sam'}})
        seen = []

        def run(args, **kw):
            seen.append(args)
            return subprocess.CompletedProcess([], 0, json.dumps({'success': True, 'data': {'sent': True, 'id': '3EB0AA'}}), '')
        with patch.object(n.subprocess, 'run', side_effect=run):
            n.WhatsAppTransport(CONFIG).send(action, {'id': 'J1'})
        self.assertEqual(seen[0][seen[0].index('--message') + 1], SHOWN)


if __name__ == '__main__':
    unittest.main()

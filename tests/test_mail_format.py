"""An email's text marks (bold, italic, links, lists) as the send writes them: the HTML part, the plain-text part and the
MIME message. tests/mail_format_cases.json holds the cases; test_email_editor_dashboard.mjs draws the same cases with the
dashboard's mailHtml and expects the same HTML, so the preview the owner approves is the mail that goes out."""
import email
import email.policy
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

import next_actions as n

CASES = json.loads((Path(__file__).parent / 'mail_format_cases.json').read_text())


class Tags(HTMLParser):
    """Every tag and attribute in a piece of HTML, and whether the tags nest properly."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.attrs, self.stack, self.ok = set(), set(), [], True

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        self.attrs.update(f'{tag}.{k}' for k, _ in attrs)
        if tag != 'br':
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.ok = False


class MailFormat(unittest.TestCase):
    def test_cases_render_as_recorded(self):
        for case in CASES:
            with self.subTest(body=case['body']):
                self.assertEqual(n.mail_html(case['body']), case['html'])
                self.assertEqual(n.mail_text(case['body']), case['text'])

    def test_only_a_few_safe_tags_ever_come_out_and_they_nest(self):
        for case in CASES:
            with self.subTest(body=case['body']):
                tags = Tags()
                tags.feed(case['html'])
                tags.close()
                self.assertTrue(tags.ok and not tags.stack, case['html'])
                self.assertLessEqual(tags.tags, {'div', 'br', 'b', 'i', 'a', 'ul', 'ol', 'li'})
                self.assertLessEqual(tags.attrs, {'a.href', 'ul.style', 'ol.style', 'ol.start'})
                for href in re.findall(r'href="([^"]*)"', case['html']):
                    self.assertTrue(href.startswith('https://'), href)

    def test_the_marks_read_as_written(self):
        self.assertEqual(n.mail_html('**Yes**, see _the doc_'), '<div><b>Yes</b>, see <i>the doc</i></div>')
        self.assertEqual(n.mail_html('- one\n- two'), '<ul style="margin:0 0 0 1.6em;padding:0"><li>one</li><li>two</li></ul>')
        self.assertEqual(n.mail_text('**Yes**, [the doc](https://example.com/d)\n- one'), 'Yes, the doc (https://example.com/d)\n- one')
        # Plain text that only looks like marks stays as it is
        for plain in ('5 * 3 * 2', 'snake_case_name', 'a*b*c', '** not bold **'):
            self.assertEqual(n.mail_text(plain), plain)
            self.assertNotIn('<b>', n.mail_html(plain))
            self.assertNotIn('<i>', n.mail_html(plain))

    def test_the_sent_message_has_both_parts(self):
        action = {'kind': 'email', 'from': 'owner@example.com', 'to': ['r@example.com'], 'cc': [], 'bcc': [], 'subject': 'S',
                  'body': 'Hi,\n\n**Two** things:\n- the [plan](https://example.com/p)\n- _soon_\n\nAlex <script>x</script>'}
        message = email.message_from_bytes(n.mime_bytes(action, {'rfc_message_id': '<id@x>'}), policy=email.policy.default)
        parts = {p.get_content_type(): p.get_content().replace('\r\n', '\n') for p in message.walk() if p.get_content_maintype() == 'text'}
        self.assertEqual(message.get_content_type(), 'multipart/alternative')
        self.assertIn('<b>Two</b> things:</div><ul', parts['text/html'])
        self.assertIn('<li>the <a href="https://example.com/p">plan</a></li><li><i>soon</i></li>', parts['text/html'])
        self.assertIn('Alex &lt;script&gt;x&lt;/script&gt;', parts['text/html'])
        self.assertEqual(parts['text/plain'].rstrip('\n'), 'Hi,\n\nTwo things:\n- the plan (https://example.com/p)\n- soon\n\nAlex <script>x</script>')

    def test_an_owner_edit_keeps_its_marks(self):
        action = {'kind': 'email', 'account_id': 'work', 'from': 'owner@example.com', 'to': ['r@example.com'], 'cc': [], 'bcc': [],
                  'subject': 'S', 'body': 'Hi', 'revision': 'x'}
        body = 'Hi,\n\n- **one**\n- two\n\nPlain \\* star\n\nAlex'
        self.assertEqual(n.revise(action, body=body)['body'], body)


if __name__ == '__main__':
    unittest.main()

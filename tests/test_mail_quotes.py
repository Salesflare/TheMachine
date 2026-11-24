"""A mail's own words and what it quotes: told by structure, in any language, and nothing the sender wrote is lost."""
import base64
import tempfile
import unittest
from pathlib import Path

import ms_graph
import signatures
from machine.mail_quotes import mail_html, new_html
from machine.sources.gmail import message_event
from machine.main import Store
from machine.text import QUOTED_MARK, message_attachments, message_body, message_html, own_part, quoted_history, split_quoted_history, trim_quoted_history

ACCOUNT = {'id': 'work', 'email': 'ann@example.com'}
PEOPLE = 'bob roe <bob@example.org> ann poe <ann@example.com>'
ASKED = 'Can you sign the contract before Friday?'
HEADERS = {
    'English': 'From: Ann Poe <ann@example.com>\nSent: Monday, 3 May 2027 10:00\nTo: Bob Roe\nSubject: Contract\n\n',
    'Dutch': 'Van: Ann Poe <ann@example.com>\nVerzonden: maandag 3 mei 2027 10:00\nAan: Bob Roe\nOnderwerp: Contract\n\n',
    'German': 'Von: Ann Poe <ann@example.com>\nGesendet: Montag, 3. Mai 2027 10:00\nAn: Bob Roe\nBetreff: Contract\n\n',
    'French': 'De : Ann Poe <ann@example.com>\nEnvoyé : lundi 3 mai 2027 10:00\nÀ : Bob Roe\nObjet : Contract\n\n',
    'Italian': 'Da: Ann Poe [mailto:ann@example.com]\nInviato: lunedì 3 maggio 2027 10:00\nA: Bob Roe\nOggetto: Contract\n\n',
    'Polish': 'Od: Ann Poe <ann@example.com>\nWysłano: poniedziałek, 3 maja 2027 10:00\nDo: Bob Roe\nTemat: Contract\n\n',
    'under a rule': '________________________________\nVan: Ann Poe <ann@example.com>\nVerzonden: maandag 3 mei 2027 10:00\nAan: Bob\n\n',
    'in bold': '*From:* Ann Poe <ann@example.com>\n*Date:* Monday, 3 May 2027 at 10:00\n*To:* Bob Roe\n*Subject:* Contract\n\n',
    'without an address': 'From: Ann Poe\nDate: Monday, 3 May 2027 at 10:00\nTo: Bob Roe\nSubject: Contract\n\n',
    'under its own line': '-----Ursprüngliche Nachricht-----\nVon: Ann Poe\nGesendet: 03.05.2027 10:00\nAn: Bob\n\n',
    'under a long line': '--------------- Oorspronkelijk bericht ---------------\nVan: Ann Poe [ann@example.com]\nVerzonden: 03-05-2027 10:00\nAan: Bob\n\n',
    'unmarked, English': 'On Mon, May 3, 2027 at 10:00 AM Ann Poe <ann@example.com> wrote:\n\n',
}
MARKED = {
    'marked itself': '> On 3 May 2027, at 10:00, Ann Poe <ann@example.com> wrote:\n>',
    'Dutch': 'Op ma 3 mei 2027 om 10:00 schreef Ann <ann@example.com>:',
    'Polish': 'pon., 3 maj 2027 o 10:00 Ann <ann@example.com> napisał(a):',
    'Czech': 'po 3. 5. 2027 v 10:00 odesílatel Ann <ann@example.com> napsal:',
    'Japanese': '2027年5月3日(月) 10:00 Ann <ann@example.com>:',
    'Turkish': 'Ann <ann@example.com>, 3 May 2027 Pzt, 10:00 tarihinde şunu yazdı:',
    'Finnish': 'ma 3. toukok. 2027 klo 10.00 Ann (ann@example.com) kirjoitti:',
    'Portuguese, wrapped': 'Ann Poe <ann@example.com> escreveu (segunda, 03/05/2027 à(s)\n10:00):',
    'Norwegian, in capitals elsewhere': 'man. 3. mai 2027 kl. 10:00 skrev Ann <ann@example.com>:',
    'a blank gap under it': 'On Mon, May 3, 2027 at 10:00 AM Ann <ann@example.com> wrote:\n\n\n\n',
}


def part(kind, text='', parts=(), **extra):
    out = {'mimeType': kind, 'parts': list(parts), **extra}
    if text:
        out['body'] = {'data': base64.urlsafe_b64encode(text.encode()).decode()}
    return out


def raw(payload, subject='Re: Contract', labels=('INBOX',)):
    headers = [{'name': k, 'value': v} for k, v in (('Subject', subject), ('From', 'Bob Roe <bob@example.org>'), ('To', 'Ann <ann@example.com>'))]
    return {'id': 'm1', 'threadId': 't1', 'internalDate': '1809000000000', 'snippet': '', 'labelIds': list(labels), 'payload': {'headers': headers, **payload}}


class Quotes(unittest.TestCase):
    def test_header_blocks_in_any_language(self):
        for name, header in HEADERS.items():
            for subject in ('Re: Contract', 'AW: Contract', 'Contract'):
                with self.subTest(name, subject=subject):
                    new, history = split_quoted_history(f'Sure.\n\nBob\n{header}{ASKED}\nAnn', subject, PEOPLE)
                    self.assertEqual(new, 'Sure.\n\nBob')
                    self.assertIn(ASKED, history)

    def test_marked_lines_with_the_line_above_them_in_any_language(self):
        for name, above in {**MARKED, 'none': ''}.items():
            for newline in ('\n', '\r\n'):
                with self.subTest(name, newline=newline):
                    text = f'OK.\n\n{above}\n> {ASKED}\n>\n> Ann'.replace('\n', newline)
                    new, history = split_quoted_history(text, 'Re: Contract', PEOPLE)
                    self.assertEqual(new, 'OK.')
                    self.assertIn('> Ann', history)

    def test_prose_is_no_quote(self):
        for text in ('Hi team,\n\nOn Monday I met the client and as they wrote:\nbudget is ok.\nSee you',
                     'Hi,\n\nOn 3 May 2027 I met Ann and this is what she said and wrote:\nthe budget is fine',
                     'Hi,\n\nOn the pricing question, I talked with Ann.\nShe looked at what you wrote:\nit is fine',
                     'Hi,\n\n--- start of the plan ---\n\nPurpose: to sell more\nAudience: everyone\nTone: light\n\nMore to come',
                     'Hi,\n\n----- start of the plan -----\n\nPurpose: to sell more\nAudience: everyone\nTone: light\n\nMore',
                     'Our terms:\n\nPrice: 100\nStart: May 2027\nEnd: June 2027\n\nOK?',
                     'Hi,\n\n-------------\nMeeting room 3, 3 May 2027 10:00\n-------------\n\nSee you there',
                     'It is\n> 5 degrees outside'):
            with self.subTest(text):
                self.assertEqual(split_quoted_history(text, '', PEOPLE), (text, ''))
                self.assertEqual(own_part(text, '', PEOPLE), text)

    def test_a_help_desks_newest_message_is_the_mail_and_the_next_is_quoted(self):
        rule = '-' * 46
        new = f'##- Reply above this line -##\n\n{rule}\n\nBob Roe, 3 May 2027 17:30 CEST\n\nIt works now.'
        for subject in ('Re: Contract', '[Acme] Re: Contract'):
            self.assertEqual(split_quoted_history(new, subject, PEOPLE), (new, ''))
            self.assertEqual(split_quoted_history(f'{new}\n\n{rule}\n\nAnn Poe, 3 May 2027 17:26 CEST\n\n{ASKED}', subject, PEOPLE)[0], new)

    def test_unmarked_lines_under_who_wrote_them(self):
        for name, above in MARKED.items():
            if name != 'marked itself':
                with self.subTest(name):
                    self.assertEqual(split_quoted_history(f'OK.\n\n{above.strip()}\n\n{ASKED}\nAnn', 'Re: Contract', PEOPLE)[0], 'OK.')
                    prose = f'Hi,\n\n{above.strip()}\n\n{ASKED}'
                    if not above.startswith('O'):  # no answer: as written (a line that says "wrote" is a quote anyway)
                        self.assertEqual(split_quoted_history(prose, 'Contract', PEOPLE), (prose, ''))

    def test_answers_between_and_under_quoted_lines_stay(self):
        text = ('Hi Ann, see below.\n\nOn Mon, May 3, 2027 at 10:00 AM Ann <ann@example.com> wrote:\n> Can you pay the deposit?\n\n'
                'Yes, on Thursday.\n\n> And the keys?\nWith Tom.\n\n> Thanks,\n> Ann\n')
        self.assertEqual(own_part(text, 'Re: Keys', PEOPLE), 'Hi Ann, see below.\n\nYes, on Thursday.\n\nWith Tom.')
        new, history = split_quoted_history(text, 'Re: Keys', PEOPLE)
        self.assertTrue(new.endswith('With Tom.'))  # with what it answers, for the person
        self.assertEqual(history, '> Thanks,\n> Ann\n')
        bottom = f'On Mon, May 3, 2027 at 10:00 AM Ann <ann@example.com> wrote:\n> {ASKED}\n' + '> more\n' * 900 + '\nDone, signed it.'
        self.assertEqual(own_part(bottom, 'Re: Contract', PEOPLE), 'Done, signed it.')
        self.assertIn('Done, signed it.', trim_quoted_history(bottom, 'Re: Contract', PEOPLE)[0])
        long = bottom.replace('> more\n', '> more of what Ann wrote\n' * 4)
        self.assertTrue(trim_quoted_history(long, 'Re: Contract', PEOPLE)[0][:40000].endswith('Done, signed it.'))

    def test_a_quote_a_program_wrapped_is_no_answer(self):
        text = (f'OK.\n\nOn Mon, May 3, 2027 at 10:00 AM Ann <ann@example.com> wrote:\n> {ASKED} The import, which was one of the\n'
                'pain points back then, is now very\ndifferent.\n>\n> p. [555](\nhttps://example.com/t\n)\n>\n> Ann')
        self.assertEqual(own_part(text, 'Re: Contract', PEOPLE), 'OK.')

    def test_mail_stored_before_gives_its_answers_too(self):
        stored = ('Hi Ann.\n\n[Quoted earlier messages: first 90 of 90 characters kept. Earlier messages in this thread are separate signals.]\n'
                  'On Mon, May 3, 2027 at 10:00 AM Ann <ann@example.com> wrote:\n> The deposit?\n\nOn Thursday.\n\n> Ann')
        self.assertEqual(own_part(stored, 'Re: Keys', PEOPLE), 'Hi Ann.\n\nOn Thursday.')
        unmarked = stored.replace('> ', '')
        self.assertEqual(own_part(unmarked, 'Re: Keys', PEOPLE), 'Hi Ann.')
        self.assertIn('The deposit?', quoted_history(stored, 'Re: Keys', PEOPLE))

    def test_forwards_stay_whole(self):
        other = 'Carl Coe <carl@example.net>'
        for subject, text in (
                ('FW: Contract', f'FYI\n\nFrom: {other}\nSent: Monday, 3 May 2027 10:00\nTo: Bob\nSubject: Contract\n\n{ASKED}'),
                ('RV: Contract', f'FYI\n\nDe: {other}\nEnviado: lunes, 3 de mayo de 2027 10:00\nPara: Bob\nAsunto: Contract\n\n{ASKED}'),
                ('Contract', f'FYI\n\n---------- Forwarded message ---------\nFrom: {other}\nDate: Mon, May 3, 2027 at 10:00 AM\nSubject: Contract\nTo: Bob\n\n{ASKED}'),
                ('Contract', f'FYI\n\n---------- Forwarded message ---------\nFrom: Bob <bob@example.org>\nDate: Mon, May 3, 2027 at 10:00 AM\nSubject: Contract\nTo: Carl\n\n{ASKED}'),
                ('Re: Contract', f'FYI\n\n-------- Przekazana wiadomość --------\nOd: {other}\nData: 3 maja 2027 10:00\nTemat: Contract\nDo: Bob\n\n{ASKED}'),
                ('[EXT] FW: Contract', f'FYI\n\nFrom: {other}\nSent: Monday, 3 May 2027 10:00\nTo: Bob\nSubject: Contract\n\n{ASKED}'),
                ('I: Contract', f'FYI\n\nDa: {other}\nInviato: lunedì 3 maggio 2027 10:00\nA: Bob\nOggetto: Contract\n\n{ASKED}'),
                ('Contract', f'FYI\n\n> Begin forwarded message:\n>\n> From: {other}\n> Subject: Contract\n> Date: 3 May 2027 at 10:00\n> To: Bob\n>\n> {ASKED}')):
            with self.subTest(subject, text=text[:60]):
                self.assertEqual(split_quoted_history(text, subject, PEOPLE), (text, ''))
                self.assertIn(ASKED, own_part(text, subject, PEOPLE))

    def test_who_writes_from_a_second_address_is_answered_not_forwarded(self):
        text = f'Fine.\n\nVon: Anna Poe <anna@example.net>\nGesendet: Montag, 3. Mai 2027 10:00\nAn: Bob\nBetreff: Contract\n\n{ASKED}'
        self.assertEqual(split_quoted_history(text, 'AW: Contract', 'bob roe <bob@example.org> <anna@example.com>')[0], 'Fine.')


class Html(unittest.TestCase):
    def test_quote_containers(self):
        header = '<b>Van:</b> Ann Poe &lt;ann@example.com&gt;<br><b>Verzonden:</b> maandag 3 mei 2027 10:00<br><b>Aan:</b> Bob<br><b>Onderwerp:</b> Contract'
        for name, quote in {
            'Gmail': f'<div class="gmail_quote"><div class="gmail_attr">Pe lun., 3 mai 2027 la 10:00, Ann &lt;ann@example.com&gt; a scris:<br></div><blockquote class="gmail_quote">{ASKED}</blockquote></div>',
            'Apple Mail': f'<blockquote type="cite"><div>On 3 May 2027, at 10:00, Ann &lt;ann@example.com&gt; wrote:</div><div>{ASKED}</div></blockquote>',
            'Thunderbird': f'<div class="moz-cite-prefix">Ann Poe schreef op 3-5-2027 om 10:00:<br></div><blockquote type="cite" cite="mid:1@example.com">{ASKED}</blockquote>',
            'Yahoo': f'<div class="yahoo_quoted"><div>On Monday, Ann wrote:</div><div>{ASKED}</div></div>',
            'Outlook web': f'<div id="appendonsend"></div><hr><div id="divRplyFwdMsg">{header}</div><div>{ASKED}</div>',
            'Outlook': f'<div style="border-top:solid"><p>{header}</p></div><p>{ASKED}</p>',
        }.items():
            with self.subTest(name):
                text = mail_html(f'<html><body><div>Perfect.</div><div>Bob</div>{quote}</body></html>', 'Re: Contract', PEOPLE)
                self.assertEqual(split_quoted_history(text, 'Re: Contract', PEOPLE)[0], 'Perfect.\nBob')
                self.assertIn(ASKED, text)
                self.assertEqual(new_html(f'<div>Perfect.</div><div>Bob</div>{quote}').replace('<div style="border-top:solid">', ''), '<div>Perfect.</div><div>Bob</div>')

    def test_an_answer_between_two_quotes(self):
        text = mail_html('<div>See below.</div><blockquote type="cite">The deposit?</blockquote><div>On Thursday.</div><blockquote type="cite">And the keys?</blockquote>', 'Re: Keys', PEOPLE)
        self.assertEqual(own_part(text, 'Re: Keys', PEOPLE), 'See below.\n\nOn Thursday.')

    def test_an_indented_paragraph_is_no_quote(self):
        self.assertEqual(mail_html('<p>Our motto is</p><blockquote><p>Less is more</p></blockquote>'), 'Our motto is\nLess is more')

    def test_signature_under_a_mail_with_a_quote(self):
        body = '<div>Note.</div><div><b>Ann Poe</b></div>'
        self.assertEqual(signatures.new_part(body + f'<hr><div id="divRplyFwdMsg"><b>Od:</b> Bob</div><div>{ASKED}</div>'), body)
        self.assertEqual(signatures.new_part(body), body)


class Parts(unittest.TestCase):
    HTML = part('text/html', f'<p>{ASKED} The bank needs it before the closing.</p>')
    FOOTER = part('text/plain', 'Board mailing list\nhttps://lists.example.org/board')
    EML = part('message/rfc822', filename='old.eml', parts=[part('multipart/alternative', parts=[
        part('text/plain', 'What Carl wrote last year, about something else entirely.'), part('text/html', '<p>What Carl wrote last year</p>')])])

    def test_a_plain_footer_never_stands_in_for_the_mail(self):
        text = message_body(part('multipart/mixed', parts=[self.HTML, self.FOOTER]))
        self.assertIn(ASKED, text)
        self.assertIn('Board mailing list', text)

    def test_an_attached_message_is_not_the_mails_text(self):
        payload = part('multipart/mixed', parts=[self.HTML, self.EML])
        self.assertEqual(message_body(payload), f'{ASKED} The bank needs it before the closing.')
        self.assertNotIn('Carl', message_html(payload))

    def test_a_message_sent_on_as_a_file_is_labeled_as_such(self):
        inner = part('text/plain', 'I will pay on Monday.', headers=[{'name': 'From', 'value': 'Carl <carl@example.net>'}, {'name': 'Subject', 'value': 'Invoice'}])
        payload = part('multipart/mixed', parts=[part('message/rfc822', parts=[inner], partId='1', body={'attachmentId': 'a', 'size': 9})])
        self.assertEqual(message_body(payload), '---------- Forwarded message ---------\nFrom: Carl <carl@example.net>\nSubject: Invoice\n\nI will pay on Monday.')
        self.assertEqual([x['name'] for x in message_attachments(payload)], ['Invoice.eml'])

    def test_an_attached_message_is_a_file_of_an_imap_or_outlook_mail(self):
        mime = ('From: a@example.com\r\nContent-Type: multipart/mixed; boundary=B\r\n\r\n--B\r\nContent-Type: text/plain\r\n\r\nSee below.\r\n'
                '--B\r\nContent-Type: message/rfc822\r\nContent-Disposition: attachment; filename="old.eml"\r\n\r\nSubject: Old\r\n\r\nOld text\r\n--B--\r\n')
        payload = ms_graph.payload(mime.encode())
        self.assertEqual([x['name'] for x in message_attachments(payload)], ['old.eml'])
        self.assertIn(b'Old text', base64.urlsafe_b64decode(payload['parts'][1]['body']['data'] + '=='))
        self.assertEqual(message_body(payload).strip(), 'See below.')

    def test_a_note_that_the_program_cannot_show_it_is_no_text(self):
        stub = part('text/plain', 'This email contains content that your mail reader can not show.')
        html = part('text/html', f'<p>{ASKED} The bank needs it before the closing, and Tom has the keys of the house on the other side of town.</p>' * 2)
        self.assertIn(ASKED, message_body(part('multipart/alternative', parts=[stub, html])))
        short = part('text/plain', f'{ASKED} The bank needs it.')
        self.assertEqual(message_body(part('multipart/alternative', parts=[short, html])), f'{ASKED} The bank needs it.')

    def test_both_versions_of_one_text_are_one(self):
        plain = part('text/plain', f'{ASKED} The bank needs it before the closing.')
        for kind in ('multipart/alternative', 'multipart/mixed', ''):
            self.assertEqual(message_body(part(kind, parts=[plain, self.HTML])).count(ASKED), 1, kind)
        related = part('multipart/related', parts=[part('multipart/alternative', parts=[plain, self.HTML]), part('image/png', filename='a.png')])
        self.assertEqual(message_body(part('multipart/mixed', parts=[related])).count(ASKED), 1)


class Stored(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = Store(Path(temp.name) / 'events.sqlite')

    def put(self, body, labels=('INBOX',)):
        event = message_event(ACCOUNT, raw(part('text/plain', 'x'), labels=labels))
        self.store.commit_page('work', {}, [{**event, 'body': body}])
        with self.store.connect() as db:
            return [tuple(x) for x in db.execute('SELECT id,content_hash,body FROM events')]

    def test_mail_read_again_stays_as_stored(self):
        first = self.put('Read by the code of before')
        self.assertEqual(self.put('Read by the code of today'), first)

    def test_a_draft_and_a_moved_mail_are_taken_again(self):
        self.put('One', ('DRAFT',))
        self.assertEqual(self.put('Two', ('DRAFT',))[0][2], 'Two')
        self.assertEqual(self.put('Three', ('SENT',))[0][2], 'Three')

    def test_a_reply_collected(self):
        event = message_event(ACCOUNT, raw(part('text/plain', f'Sure.\n\n{HEADERS["German"]}{ASKED}')))
        self.assertEqual(QUOTED_MARK.split(event['body'])[0].strip(), 'Sure.')
        self.assertIn(ASKED, event['body'])


if __name__ == '__main__':
    unittest.main()

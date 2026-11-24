"""Links to Google files in every form people and mail programs send them (google_links.py), kept in the text of an HTML
message, and read by a run: as what a Drive link turns out to be, or with a plain answer. Nothing goes out."""
import base64
import io
import json
import time
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse

from connectors import docs, intercom, teams
import google_files
import google_links
import test_google_files as files
from machine import text as machine_text
from machine.sources import calendar

ID = '1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-AbCdE'
LINK = f'https://docs.google.com/document/d/{ID}/edit'


def forms(link):
    """The same link as it comes in."""
    quoted = urllib.parse.quote(link, safe='')
    plain = link.removeprefix('https://')
    path = plain.removeprefix('docs.google.com')
    proofpoint = urllib.parse.quote(plain, safe='').replace('_', '%5F').replace('-', '%2D').replace('%2F', '_').replace('%', '-')
    return {'plain': link, 'http': link.replace('https', 'http'), 'no scheme': plain, 'account': link.replace('/d/', '/u/0/d/'),
            'domain': 'https://docs.google.com/a/example.com' + path, 'domain and account': 'https://docs.google.com/a/example.com' + path.replace('/d/', '/u/1/d/'),
            'google.com/url': f'https://www.google.com/url?q={link}&sa=D', 'google.com/url encoded': f'https://www.google.com/url?q={quoted}&sa=D',
            'safe links': f'https://eur01.safelinks.protection.outlook.com/?url={quoted}&data=05%7C02', 'click counter': f'https://t.example.com/s/?u={quoted.replace("%3A", ":")}&e=4',
            'a checker around a counter': f'https://eur01.safelinks.protection.outlook.com/?url={urllib.parse.quote("https://t.example.com/?u=" + quoted, safe="")}&data=05',
            'proofpoint v2': f'https://urldefense.proofpoint.com/v2/url?u=https-3A__{proofpoint}&d=DwMF', 'proofpoint v3': f'https://urldefense.com/v3/__{link}__;!!abc',
            'sign-in first': f'https://accounts.google.com/AccountChooser?continue={quoted}', 'html': f'<a href="{link}?a=1&amp;b=2">it</a>', 'json': json.dumps({'link': link})}


class Forms(unittest.TestCase):
    def test_every_form_of_a_doc_sheet_and_slides_link(self):
        for part, kind in google_links.KINDS.items():
            link = LINK.replace('/document/', f'/{part}/')
            for name, text in {**forms(link), 'open?id=': f'https://docs.google.com/{part}/open?usp=x&id={ID}'}.items():
                with self.subTest(part=part, form=name):
                    self.assertEqual(google_links.ids(text, kind), [ID], text)

    def test_a_drive_link_does_not_say_what_it_is(self):
        for text in (f'https://drive.google.com/open?id={ID}', f'https://drive.google.com/open?usp=sharing&amp;id={ID}', f'https://drive.google.com/file/d/{ID}/view?usp=sharing',
                     f'https://drive.google.com/file/u/0/d/{ID}/view', f'https://drive.google.com/uc?id={ID}&export=download', f'https://drive.google.com/a/example.com/file/d/{ID}',
                     f'https://docs.google.com/open?id={ID}'):
            self.assertEqual(google_links.ids(text, google_links.ANY), [ID], text)
            self.assertEqual(docs.doc_links(text), [])
        self.assertEqual(docs.file_links(f'https://drive.google.com/open?id={ID}'), {ID: {'kind': 'any', 'spots': []}})
        # another link says which it is
        self.assertEqual(docs.file_links(f'https://drive.google.com/open?id={ID} {LINK}'), {})
        self.assertEqual(docs.file_links(f'https://drive.google.com/open?id={ID} {LINK.replace("document", "spreadsheets")}')[ID]['kind'], 'sheets')

    def test_no_file(self):
        for text in (f'https://docs.google.com/document/d/e/2PACX-{ID}/pub', f'https://docs.google.com/forms/d/{ID}/edit', f'https://drive.google.com/drive/folders/{ID}',
                     f'https://docs.google.example/document/d/{ID}', f'https://notdocs.google.com/document/d/{ID}', f'https://x-docs.google.com/document/d/{ID}',
                     f'https://docs.google.com.example.com/document/d/{ID}', f'https://drive.google.com/document/d/{ID}', 'docs.google.com', ''):
            self.assertEqual(google_links.find(text), [], text)

    def test_an_id_cut_by_a_line_end_in_a_quote_is_whole_again(self):
        for cut in ('\n> ', '\r\n> > ', '\n'):
            for at in (20, 26, 43):
                self.assertEqual(docs.doc_links(f'> the drafts: https://docs.google.com/document/d/{ID[:at]}{cut}{ID[at:]}/edit\n> Thanks'), [ID])
        # what follows isn't the rest of an id: no file is made up
        short = 'a' * 30
        self.assertEqual(docs.doc_links(f'https://docs.google.com/document/d/{short}\nThanks'), [short])
        self.assertEqual(docs.doc_links(f'https://docs.google.com/document/d/{ID}\nThanks'), [ID])
        # cut in one message, whole in another: one file
        self.assertEqual(docs.doc_links(f'https://docs.google.com/document/d/{ID[:25]}\n>\n> x y\n{LINK}'), [ID])

    def test_a_sheets_tab_and_cells_come_out_of_a_wrapped_link(self):
        link = LINK.replace('document', 'spreadsheets') + '?gid=7#gid=7&range=B2:C3'
        self.assertEqual(google_files.links(forms(link)['safe links'])[ID]['spots'], [(7, 'B2:C3')])

    def test_long_and_odd_text_is_quick(self):
        for text in ('docs.google.com/document/open?' + 'a' * 200_000, 'https' * 40_000 + ' google', 'docs.google.com/' * 10_000, '<a href=google' * 10_000,
                     f'<a href="{LINK}">x' * 2000, 'https%3A%2F%2Fdocs.google.com%2F' + '%25' * 50_000):
            at = time.monotonic()
            google_links.find(text)
            google_links.keep_links(text)
            self.assertLess(time.monotonic() - at, 5)


class Kept(unittest.TestCase):
    PAGE = f'<p>Hi</p><p>See <a class="x" href="{LINK}?usp=sharing"><b>the plan</b></a> and <a href="https://example.com/a">this</a>.</p>'
    SEEN = f'See the plan ({LINK}) and this.'

    def test_a_link_behind_other_words_stays_in_the_text(self):
        self.assertEqual(machine_text.email_body('', [self.PAGE]), 'Hi\n' + self.SEEN)
        self.assertIn(self.SEEN, teams.html_text({'content': google_links.keep_links(self.PAGE)}))
        self.assertEqual(intercom.plain(google_links.keep_links(self.PAGE)), 'Hi\n' + self.SEEN)
        event = calendar.calendar_event({'id': 'a', 'email': 'a@example.com'}, {'id': 'x', 'summary': 'Plan', 'start': {'dateTime': '2026-01-01T10:00:00Z'},
                                                                               'end': {'dateTime': '2026-01-01T11:00:00Z'}, 'description': self.PAGE}, 'UTC')
        self.assertIn(LINK, event['body'])

    def test_only_what_is_hidden_is_added_once(self):
        shown = f'<a href="{LINK}">{LINK}</a>'
        self.assertEqual(google_links.keep_links(shown), shown)
        self.assertEqual(google_links.keep_links('<a href="https://example.com">google</a>'), '<a href="https://example.com">google</a>')
        twice = google_links.keep_links(f'<a href="{LINK}">Open</a> <a href="{LINK}">Open again</a>')
        self.assertEqual(twice.count(f'({LINK})'), 1)
        safe = google_links.keep_links(f'<a href="{forms(LINK)["safe links"]}">it</a>')
        self.assertIn(f'it ({LINK})</a>', safe)
        sheet = google_links.keep_links(f'<a href="{LINK.replace("document", "spreadsheets")}#gid=7">it</a>')
        self.assertIn(f'(https://docs.google.com/spreadsheets/d/{ID}/edit#gid=7)', sheet)

    def test_a_text_part_without_the_link_gives_way_to_the_html(self):
        words = 'Hi,\nSee the plan and this.'
        self.assertEqual(machine_text.email_body(words, [self.PAGE]), 'Hi\n' + self.SEEN)
        said = f'Hi,\nSee the plan <{LINK}> and this.'
        self.assertEqual(machine_text.email_body(said, [self.PAGE]), said)
        both = {'mimeType': 'multipart/mixed', 'parts': [{'mimeType': kind, 'body': {'data': base64.urlsafe_b64encode(body.encode()).decode()}}
                                                         for kind, body in (('text/plain', 'Hi\nSee the plan and this. ' + 'Words for a whole mail. ' * 4),
                                                                            ('text/html', self.PAGE + '<p>' + 'Words for a whole mail. ' * 4 + '</p>'))]}
        self.assertEqual(machine_text.message_body(both).count('See the plan'), 1)  # side by side, still one mail
        self.assertEqual(machine_text.email_body(words, ['<p>See <a href="https://example.com">the plan</a></p>']), words)


class Read(files.Base):
    """A run's reads through the owner's Google Docs sign-in; a Doc answers with `doc` as its status."""
    todo, read = files.ToDo.todo, files.ToDo.read

    def setUp(self):
        super().setUp()
        self.app = object.__new__(files.machine_main.App)
        self.app.config, self.app.store = self.config, files.machine_main.Store(self.config['database'])
        self.config['accounts'] = [dict(files.t.GMAIL), dict(files.hosted.PERSONAL), dict(files.hosted.ACCOUNT)]
        self.doc = 400
        patch('machine.app.docs.CONNECTOR_HELPERS', files.hosted._helpers()).start()
        patch('urllib.request.OpenerDirector.open', side_effect=self.respond).start()

    def respond(self, request, data=None, timeout=None):
        if urllib.parse.urlsplit(request.full_url).netloc != 'docs.googleapis.com':
            return self.fake.respond(request, data, timeout)
        if self.doc == 200:
            return files.t.Response(json.dumps({'title': 'Plan', 'body': {'content': [
                {'startIndex': 1, 'endIndex': 9, 'paragraph': {'elements': [{'startIndex': 1, 'endIndex': 9, 'textRun': {'content': 'Week 2.\n'}}]}}]}}).encode())
        raise urllib.error.HTTPError(request.full_url, self.doc, 'no', {}, io.BytesIO(b'{}'))

    def test_a_drive_link_reads_as_what_it_is(self):
        self.todo(f'https://drive.google.com/open?id={files.SHEET} https://drive.google.com/file/d/{files.DOC}/view')
        self.assertEqual(self.read(files.SHEET)['type'], 'Google Sheet')
        self.doc = 200
        self.assertIn('Week 2.', self.read(files.DOC)['text'])

    def test_a_drive_link_to_another_kind_of_file_says_so(self):
        self.todo(f'https://drive.google.com/file/d/{files.DOC}/view')
        self.fake.refuse = (400, {})
        with self.assertRaisesRegex(ValueError, 'not a Google Doc, Sheet or Slides file') as raised:
            self.read(files.DOC)
        self.assertNotRegex(str(raised.exception), r'docs_|d{20}')
        self.doc = 403
        with self.assertRaisesRegex(ValueError, 'private to someone else'):
            self.read(files.DOC)

    def test_a_wrapped_doc_link_reads_and_each_refusal_is_plain(self):
        self.todo(forms(f'https://docs.google.com/document/d/{files.DOC}/edit')['safe links'])
        self.doc = 200
        self.assertIn('Week 2.', self.read(files.DOC)['text'])
        for status, words in ((403, 'private to someone else'), (404, 'deleted'), (400, 'no text to read')):
            self.doc = status
            with self.assertRaisesRegex(ValueError, words) as raised:
                self.read(files.DOC)
            self.assertNotRegex(str(raised.exception), r'docs_|\d{3}|d{20}')

    def test_a_linked_doc_without_google_docs_here_is_not_called_unlinked(self):
        self.todo(f'https://docs.google.com/document/d/{files.DOC}/edit')
        self.config['accounts'] = [dict(files.t.GMAIL), dict(files.hosted.PERSONAL)]
        self.config['docs_consent'] = None
        with self.assertRaisesRegex(ValueError, 'No Google Docs connection') as raised:
            self.read(files.DOC)
        self.assertNotIn('connect Google Docs', str(raised.exception))
        self.config['docs_consent'] = ['google']
        with self.assertRaisesRegex(ValueError, 'connect Google Docs under Connections'):
            self.read(files.DOC)
        with self.assertRaisesRegex(ValueError, 'linked in this task'):
            self.read('x' * 44)


if __name__ == '__main__':
    unittest.main()

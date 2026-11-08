"""A bill or statement sent as a file: the email keeps its attachments' names and types (never their bytes), and the
review sees them, so it knows the amount and date are in a file its to-do's run can open (AGENTS.md, "Invoices to pay
by hand"). Before, the review saw only the body and could conclude there was nothing to pay. Made-up mail only;
nothing is sent, no Gateway, no model."""
import base64, datetime as dt, email.message, importlib.util, json, tempfile, unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('attachment_names_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import message_seal  # noqa: E402  (on the path once assistant.py is loaded)

WORK = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com'}
PDF = b'%PDF-1.4 secret amount 123.45 EUR'


def b64(data):
    return base64.urlsafe_b64encode(data).decode()


def statement(source='m1'):
    """A Gmail "full" message: a short body, a PDF statement and a logo shown inline."""
    heads = [{'name': 'From', 'value': 'Building manager <manager@building.example>'}, {'name': 'To', 'value': 'owner@example.com'},
             {'name': 'Subject', 'value': 'Annual statement 2025'}]
    return {'id': source, 'threadId': source, 'labelIds': ['INBOX'], 'internalDate': str(int(dt.datetime.now().timestamp() * 1000) - 3600000),
            'snippet': 'Please find the statement attached', 'payload': {'headers': heads, 'mimeType': 'multipart/mixed', 'parts': [
                {'mimeType': 'text/plain', 'filename': '', 'body': {'data': b64(b'Dear owners, please find the annual statement attached.')}},
                {'mimeType': 'application/pdf', 'filename': 'Statement 2025 - unit 12.pdf', 'body': {'attachmentId': 'att1', 'size': len(PDF)},
                 'headers': [{'name': 'Content-Disposition', 'value': 'attachment; filename="Statement 2025 - unit 12.pdf"'}]},
                {'mimeType': 'image/png', 'filename': 'logo.png', 'body': {'attachmentId': 'att2', 'size': 10},
                 'headers': [{'name': 'Content-Disposition', 'value': 'inline'}, {'name': 'Content-ID', 'value': '<logo>'}]}]}}


class AttachmentNames(unittest.TestCase):
    def test_gmail_keeps_names_and_types_not_bytes_or_inline_pictures(self):
        event = a.message_event(WORK, statement())
        self.assertEqual(event['metadata']['attachments'], [{'name': 'Statement 2025 - unit 12.pdf', 'type': 'application/pdf'}])
        self.assertNotIn('123.45', json.dumps(event))
        plain = a.message_event(WORK, {**statement('m2'), 'payload': {**statement()['payload'], 'parts': statement()['payload']['parts'][:1]}})
        self.assertNotIn('attachments', plain['metadata'])  # no files: no key, so mail without files hashes as before

    def test_outlook_mime_keeps_the_name_too(self):
        mime = email.message.EmailMessage()
        mime['From'], mime['To'], mime['Subject'] = 'Clinic <billing@clinic.example>', 'owner@example.com', 'Your invoice'
        mime.set_content('Your invoice is attached.')
        mime.add_attachment(PDF, maintype='application', subtype='pdf', filename='invoice-0042.pdf')
        message = {'id': 'o1', 'threadId': 'c1', 'labelIds': ['INBOX'], 'internalDate': '1792483200000', 'snippet': '',
                   'webLink': 'https://outlook.office.com/mail/o1', 'payload': a.ms_graph.payload(mime.as_bytes())}
        event = a.message_event({**WORK, 'service': 'outlook'}, message)
        self.assertEqual(event['metadata']['attachments'], [{'name': 'invoice-0042.pdf', 'type': 'application/pdf'}])

    def test_the_review_sees_them_and_they_are_sealed_at_rest(self):
        self.assertNotIn('attachments', message_seal.PLAIN_METADATA)
        with tempfile.TemporaryDirectory() as temp:
            store = a.Store(Path(temp) / 'events.sqlite')
            store.commit_page('work', {'history_id': '1'}, [a.message_event(WORK, statement())])
            claim = store.begin_analysis(['work'], 40)
            views = list(claim['events'])
            for page in range(1, claim.get('pages', 1)):
                views += store.analysis_page(claim['analysis_id'], page)['events']
        self.assertEqual(len(views), 1)
        self.assertIn('Statement 2025 - unit 12.pdf', json.dumps(views[0]))


if __name__ == '__main__':
    unittest.main()

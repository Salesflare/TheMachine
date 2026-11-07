"""Google Docs on a hosted Machine (connectors/docs.py, own_grant): its own Google sign-in and broker (google_docs_broker),
never Gmail's, with documents and drive.file only. It reads and edits a doc by its id, makes new ones, and never asks for
drive or drive.readonly. Google and the broker are faked: nothing goes out."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from connectors import docs
import mail_grants
import onboarding
from test_connectors import a
import test_connector_docs as t

DOCS_URL = 'https://cp.example/api/google-docs/token'
ACCOUNT = {**t.ACCOUNT, 'provider': 'google', 'own_grant': True, 'transport': 'broker'}
PERSONAL = {**ACCOUNT, 'id': 'home-docs', 'email': 'me@home.example', 'boundary': 'personal'}
HOSTED = {'manage_url': 'https://cp.example/account', 'google_docs_broker': {'url': DOCS_URL}}


def _helpers():
    found = t.helpers_for()
    found.credential = lambda config, name: 'machine-token' if name == 'google_docs-broker' else 1 / 0
    return found


class Connector(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.config = {**HOSTED, 'database': str(Path(tmp.name) / 'events.sqlite'), 'accounts': [ACCOUNT]}
        mail_grants.put(self.config, 'google_docs', t.OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = t.GoogleFake(self)
        self.fake.granted = {docs.DOCS_SCOPE, docs.FILE_SCOPE}
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)

    def asked(self):
        return {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}

    def test_its_own_sign_in_and_broker_never_gmails(self):
        sign = docs.signin(self.config, ACCOUNT, _helpers())
        self.assertEqual((sign['provider'], sign['transport']), ('google_docs', 'broker'))
        self.assertEqual(onboarding.missing(self.config, ACCOUNT), '')
        self.assertEqual(onboarding.missing({'accounts': []}, ACCOUNT), 'google_docs_broker url is not set')

    def test_it_creates_and_edits_with_documents_and_drive_file(self):
        self.assertEqual(docs.writes_on(self.config, ACCOUNT, _helpers()), {'create', 'edit'})
        self.fake.granted = {docs.FILE_SCOPE}
        import google_api
        google_api._tokens.clear()
        self.assertEqual(docs.writes_on(self.config, ACCOUNT, _helpers()), {'create'})

    def test_reads_a_doc_by_its_id_with_documents_only(self):
        found = docs.read_text(self.config, ACCOUNT, 'doc1', _helpers())
        self.assertEqual(found['url'], 'https://docs.google.com/document/d/doc1/edit')
        self.assertIn('/v1/documents/doc1', [r[1] for r in self.fake.requests])
        self.assertEqual(self.asked(), {docs.DOCS_SCOPE})
        writer = docs.Writer(self.config, ACCOUNT, _helpers())
        writer.document('doc1')
        self.assertEqual(writer.docs_write_scope(), docs.DOCS_SCOPE)
        self.assertEqual(writer.scope(), docs.FILE_SCOPE)  # a new doc: drive.file
        self.assertFalse(self.asked() & {docs.READ_SCOPE, docs.REPLY_SCOPE})  # never drive or drive.readonly


class Hosted(unittest.TestCase):
    def sources(self, consent, accounts=()):
        config = {**HOSTED, 'docs_consent': consent, 'accounts': list(accounts)}
        listed = [{**s, **({'connected': sum(1 for x in accounts if x.get('service') == 'docs')} if s['service'] == 'docs' else {})}
                  for s in onboarding.catalog(config)]
        return {s['name']: s for s in a.hosted_docs_sources(config, listed) if s['service'] == 'docs'}

    def test_add_shows_the_docs_tiles_its_account_page_offers(self):
        both = self.sources(['google', 'microsoft'], [ACCOUNT, {**t.ACCOUNT, 'id': 'ms', 'provider': 'microsoft'}])
        self.assertEqual(set(both), {'docs', 'google_docs'})
        self.assertEqual((both['google_docs']['label'], both['google_docs']['hosted_signin']), ('Google Docs', 'google_docs'))
        self.assertEqual((both['google_docs']['connected'], both['docs']['connected']), (1, 1))
        self.assertEqual(set(self.sources(['google'])), {'google_docs'})
        self.assertEqual(set(self.sources(['microsoft'])), {'docs'})
        self.assertIn('google_docs', a.HOSTED_SIGNINS)

    def test_add_on_the_dashboard_lists_google_docs_with_its_own_sign_in(self):
        import assistant
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        app = object.__new__(assistant.App)
        app.config = {**HOSTED, 'database': str(Path(tmp.name) / 'e.sqlite'), 'docs_consent': ['google', 'microsoft'], 'accounts': []}
        app.store = assistant.Store(Path(tmp.name) / 'e.sqlite')
        found = {s['name']: s.get('hosted_signin') for s in app.action('connect_sources', {}, owner_dashboard=True)['sources']}
        self.assertEqual((found['docs'], found['google_docs']), ('microsoft_docs', 'google_docs'))

    def test_reconnect_opens_connect_google_docs(self):
        manage = HOSTED['manage_url']
        self.assertEqual(a.reconnect_help(ACCOUNT, manage, True)['hosted_signin'], 'google_docs')
        self.assertEqual(a.reconnect_help({**ACCOUNT, 'provider': 'microsoft'}, manage, True)['hosted_signin'], 'microsoft_docs')
        self.assertEqual(a.reconnect_help(ACCOUNT, manage, False), {})


class Linked(unittest.TestCase):
    def test_a_google_doc_linked_in_the_tasks_messages_can_be_edited_through_google_docs(self):
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE events(id INTEGER PRIMARY KEY, account_id TEXT, kind TEXT, body TEXT, metadata TEXT, occurred_at TEXT)')
        link = 'https://docs.google.com/document/d/' + 'x' * 30 + '/edit'
        db.execute("INSERT INTO events VALUES(1,'acme-gmail','gmail.message',?,'{}','2026-10-27')", ('Can you fix ' + link,))
        ids = json.dumps([1])
        config = {**HOSTED, 'accounts': [t.GMAIL, PERSONAL, ACCOUNT]}
        files = a.doc_write_files(db, ids, config, {'boundaries': ['work:Acme']})
        self.assertEqual(files, {'x' * 30: {'account_id': 'acme-docs', 'doc_title': None, 'provider': 'google'}})
        self.assertEqual(a.doc_write_files(db, ids), {})  # without config: only the task's own doc events
        self.assertEqual(a.doc_write_files(db, ids, {**config, 'accounts': [t.GMAIL, PERSONAL]}, {'boundaries': ['work:Acme']}), {})
        microsoft = {**ACCOUNT, 'provider': 'microsoft'}
        self.assertEqual(a.doc_write_files(db, ids, {**config, 'accounts': [microsoft]}, {'boundaries': ['work:Acme']}), {})


if __name__ == '__main__':
    unittest.main()

"""What setup left out, suggested in the dashboard once it is relevant (assistant.setup_hints): only on a hosted
Machine, each linked to its step on the setup page, and gone once that step is done."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a

MANAGE = 'https://app.example.test/setup'


class SetupHints(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.config = {'accounts': [{'id': 'acme-gmail', 'service': 'gmail'}], 'manage_url': MANAGE}
        codex = patch.dict(os.environ, {'CODEX_HOME': str(Path(self.temp.name) / 'codex')})  # Codex not signed in here
        codex.start()
        self.addCleanup(codex.stop)
        self.handled_a_first_todo()

    def handled_a_first_todo(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('s0','k0','T','B','[]','[]','2026-10-01')")
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d0','s0','complete','','dashboard','2026-10-01')")

    def test_nothing_is_suggested_before_a_first_todo_is_handled(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM decisions')
        self.mail('github.com', 5)
        self.assertEqual(self.ids(), [])  # setup ends at the first to-dos; what can wait comes after one is handled
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s0','complete','','dashboard','2026-10-02')")
        self.assertEqual(self.ids(), ['source-github'])

    def test_only_the_owners_own_handling_counts(self):
        with self.store.connect() as db:
            db.execute('DELETE FROM decisions')
            # the assistant's own updates and runs ahead are no first handled to-do
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('u1','s0','update','','assistant','2026-10-02')")
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('u2','s0','prepare_ahead','','assistant','2026-10-02')")
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('u3','s0','reject','','assistant','2026-10-02')")
        self.mail('github.com', 5)
        self.assertEqual(self.ids(), [])
        self.assertFalse(a.handled_first(self.store))
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s0','complete','','telegram','2026-10-02')")
        self.assertTrue(a.handled_first(self.store))
        self.assertEqual(self.ids(), ['source-github'])

    def test_the_phone_app_is_suggested_with_its_store_links(self):
        self.assertEqual(a.phone_app_nudge(self.store), {
            'ios': 'https://apps.apple.com/app/id6829875215',
            'android': 'https://play.google.com/store/apps/details?id=computer.themachine.app',
            'page': 'https://themachine.computer/help/mobile-app', 'phones': 0})  # live in both stores
        page = (Path(a.__file__).resolve().parent / 'docs' / 'help' / 'mobile-app.md').read_text()
        self.assertIn(a.PHONE_APP_STORE['ios'], page)  # the page has both
        self.assertIn(a.PHONE_APP_STORE['android'], page)

    def test_the_phone_app_waits_until_it_is_published(self):
        with patch.dict(a.PHONE_APP_STORE, {'published': False}):
            self.assertIsNone(a.phone_app_nudge(self.store))
        store = {'published': True, 'ios': 'https://apps.example.test/ios', 'android': 'http://insecure.example.test', 'page': 'https://example.test/app'}
        with patch.dict(a.PHONE_APP_STORE, store):
            self.assertEqual(a.phone_app_nudge(self.store), {'ios': 'https://apps.example.test/ios', 'page': 'https://example.test/app', 'phones': 0})
            with self.store.connect() as db:  # the mobile app's phones (its push), once a Machine has them
                db.execute('CREATE TABLE IF NOT EXISTS notify_app_devices(id TEXT PRIMARY KEY)')
                db.execute("INSERT INTO notify_app_devices(id) VALUES('p1')")
            self.assertEqual(a.phone_app_nudge(self.store)['phones'], 1)

    def mail(self, sender, n, when=None):
        when = when or a.dt.datetime.now(a.dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            for i in range(n):
                db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) '
                           'VALUES(?,?,?,?,?,?,?,?,?)', ('acme-gmail', f'{sender}-{i}-{when}', 'gmail.message', when, 'Hi', '',
                                                          json.dumps({'from': f'Notifications <noreply@{sender}>'}), 'h', when))

    def ids(self, config=None):
        return [h['id'] for h in a.setup_hints(self.store, config or self.config)]

    def test_a_source_whose_mail_keeps_coming_is_suggested_until_connected(self):
        self.mail('github.com', 2)
        self.assertEqual(self.ids(), [])  # two mails: not yet worth it
        self.mail('github.com', 1)
        [hint] = a.setup_hints(self.store, self.config)
        self.assertEqual(hint, {'id': 'source-github', 'title': 'Connect GitHub?', 'text': 'GitHub mails you often. Connected, I read it directly.',
                                'href': '#connect=github', 'button': 'Connect'})  # + Add's own form, on the dashboard
        self.mail('mail.intercom.io', 3, when='2020-01-01T00:00:00+00:00')  # long ago: not now
        self.assertEqual(self.ids(), ['source-github'])
        connected = dict(self.config, accounts=[*self.config['accounts'], {'id': 'acme-github', 'service': 'github'}])
        self.assertEqual(self.ids(connected), ['codex'])  # GitHub in: now handing coding cards to Codex means something
        (Path(os.environ['CODEX_HOME'])).mkdir()
        (Path(os.environ['CODEX_HOME']) / 'auth.json').write_text('{}')
        self.assertEqual(self.ids(connected), [])

    def test_telegram_once_a_snooze_would_only_come_back_on_the_dashboard(self):
        self.assertEqual(self.ids(), [])
        with self.store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at) VALUES('s1','k','T','B','[]','[]','2026-10-01')")
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1','s1','snooze','','dashboard','2026-10-01')")
        self.assertEqual(a.setup_hints(self.store, self.config)[0]['href'], MANAGE + '#telegram')
        self.assertEqual(self.ids(dict(self.config, telegram_owner='123')), [])

    def test_only_a_hosted_machine_gets_hints(self):
        self.mail('slack.com', 5)
        self.assertEqual(self.ids(), ['source-slack'])
        self.assertEqual(a.setup_hints(self.store, self.config)[0]['href'], '#connections=add')  # + Add on the dashboard, never away
        self.assertEqual(a.setup_hints(self.store, {'accounts': []}), [])


if __name__ == '__main__':
    unittest.main()

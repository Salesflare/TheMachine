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
                                'href': MANAGE + '#source-github', 'button': 'Connect'})
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
        self.assertEqual(a.setup_hints(self.store, {'accounts': []}), [])


if __name__ == '__main__':
    unittest.main()

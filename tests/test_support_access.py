"""Support access on a paired self-hosted Machine: The Machine team reads its scrubbed logs and settings only while its
owner allows it on this Machine (Settings, Security, Support access), and the snapshot holds no message content, no
secret, no address and nothing that says who someone is. No network or control plane: the relay is a stub."""
import contextlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant
import fleet
import support
from test_device_connect import fleet_with

TOKEN = 'sk-proj-abcdefghijklmnopqrstuvwxyz0123456789'
BOT = '123456789:ABCdefGHIjklMNOpqrSTUvwxYZ0123456789'
SECRETS = (TOKEN, BOT, 'ABCdefGHI', 'sam@example.org', 'Sam Smith', 'Lunch with Ann', '470 12 34', 'jane', 'acme-secret-term',
           '987654321', 'T0SLACKID', 'ann-calendar', 'Ann Doe', 'tail1234', 'Hello Ann, the invoice')


class Snapshot(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        database = self.root / 'events.sqlite'
        self.config = self.root / 'config.json'
        self.config.write_text(json.dumps({
            'database': str(database), 'signature': 'Sam Smith, +32 470 12 34 56', 'telegram_owner': 987654321,
            'credentials': {'fleet': '/home/jane/.local/share/fleet-token', 'api-token': TOKEN},
            'dashboard_aliases': ['jane-desktop.tail1234.ts.net'], 'language': 'nl', 'poll_seconds': 300,
            'accounts': [{'id': 'work-gmail', 'email': 'sam@example.org', 'transport': 'gog', 'boundary': 'work:Acme',
                          'excluded_terms': ['acme-secret-term'], 'exclude': [{'titles': ['Lunch with Ann']}]},
                         {'id': 'ann-calendar', 'service': 'calendar', 'boundary': 'personal:Ann', 'reply_admin_name': 'Ann Doe'},
                         {'id': 'slack', 'service': 'slack', 'team_id': 'T0SLACKID', 'transport': 'maton'}]}))
        openclaw = self.root / '.openclaw'
        openclaw.mkdir()
        (openclaw / 'openclaw.json').write_text('''{
          // JSON5, as OpenClaw writes it
          agents: {defaults: {model: {primary: "openai/gpt-5", fallbacks: ["ollama/glm"]}}},
          channels: {telegram: {botToken: "%s", allowFrom: [987654321], dmPolicy: "allowlist"}},
          models: {providers: {openai: {apiKey: "%s", baseUrl: "https://api.openai.com/v1"}}},
          env: {OPENAI_API_KEY: "%s"},
        }''' % (BOT, TOKEN, TOKEN))
        with contextlib.closing(sqlite3.connect(database)) as db, db:
            db.executescript('''CREATE TABLE checkpoints(account_id TEXT PRIMARY KEY,state TEXT NOT NULL,last_success TEXT,error TEXT,
                                  error_at TEXT,failures INTEGER NOT NULL DEFAULT 0);
                                CREATE TABLE events(id INTEGER PRIMARY KEY, title TEXT, body TEXT);
                                CREATE TABLE review_runs(run_id TEXT PRIMARY KEY,status TEXT NOT NULL,started_at TEXT NOT NULL,
                                  updated_at TEXT NOT NULL,finished_at TEXT,attempts INTEGER NOT NULL DEFAULT 0,error TEXT);''')
            db.execute("INSERT INTO checkpoints VALUES('work-gmail','{\"cursor\": \"sam@example.org\"}','2026-10-27T08:00:00+00:00',"
                       "'HttpError 401 for sam@example.org token=abc',NULL,3)")
            db.execute("INSERT INTO checkpoints VALUES('ann-calendar','{}','2026-10-27T08:00:00+00:00',NULL,NULL,0)")
            db.execute("INSERT INTO events(title, body) VALUES('Invoice', 'Hello Ann, the invoice')")
            db.execute("INSERT INTO review_runs VALUES('abcdef1234567890','failed',datetime('now'),strftime('%Y-%m-%dT%H:%M:%S','now'),"
                       "NULL,2,'model_timeout')")
            db.execute("INSERT INTO review_runs VALUES('old','failed','2020-01-01','2020-01-01T00:00:00',NULL,1,'old_error')")
        patcher = patch.dict('os.environ', {'OPENCLAW_STATE_DIR': str(openclaw), 'HOME': '/home/jane'})
        patcher.start()
        self.addCleanup(patcher.stop)

    def snapshot(self):
        with patch.object(support, 'versions', return_value='os: Linux\napp: /home/jane/the-machine\nopenclaw: OpenClaw 2026.10.5'):
            return support.snapshot(str(self.config))

    def test_no_secret_address_name_or_message_content(self):
        text = json.dumps(self.snapshot(), ensure_ascii=False)
        for secret in SECRETS:
            self.assertNotIn(secret, text)

    def test_what_support_needs_stays(self):
        out = self.snapshot()
        self.assertEqual(out['settings']['language'], 'nl')
        self.assertEqual(out['settings']['poll_seconds'], 300)
        self.assertEqual([a['source'] for a in out['settings']['accounts']], ['gog#1', 'calendar#2', 'slack#3'])
        self.assertEqual(out['settings']['accounts'][0]['boundary'], 'work')
        self.assertEqual(out['settings']['accounts'][0]['filters'], 2)  # how many, never what they say
        self.assertEqual(out['openclaw']['agents']['defaults']['model'], {'primary': 'openai/gpt-5', 'fallbacks': ['ollama/glm']})
        self.assertEqual(out['openclaw']['channels']['telegram']['dmPolicy'], 'allowlist')
        self.assertIn('OpenClaw 2026.10.5', out['versions'][-1])
        self.assertIn('/home/…/the-machine', out['versions'][1])
        # connections by the same label as in settings, with their error type and failures
        self.assertEqual([(c['source'], c['failures']) for c in out['connections']], [('gog#1', 3), ('calendar#2', 0)])
        self.assertTrue(out['connections'][0]['error'].startswith('HttpError 401'))
        # the runs that failed lately, not older ones
        self.assertEqual([(f['kind'], f['id'], f['error']) for f in out['failures']], [('review', 'abcdef123456', 'model_timeout')])

    def test_a_model_id_stays_and_a_person_under_primary_does_not(self):
        out = support._settings({'model': {'primary': 'openrouter/anthropic/claude-x:free'}, 'calendar': {'primary': 'sam@example.org'},
                                 'owner': {'primary': 'Sam Smith', 'handle': 'openai/gpt-5', 'login': 'github.com/sam'}})
        self.assertEqual(out['model'], {'primary': 'openrouter/anthropic/claude-x:free'})
        self.assertEqual(out['calendar'], {'primary': '<redacted>'})
        self.assertEqual(out['owner'], {'primary': '<redacted>', 'handle': '<redacted>', 'login': '<redacted>'})

    def test_a_machine_without_a_database_or_openclaw_still_answers(self):
        self.config.write_text(json.dumps({'database': str(self.root / 'none.sqlite')}))
        with patch.dict('os.environ', {'OPENCLAW_STATE_DIR': str(self.root / 'nowhere')}):
            out = self.snapshot()
        self.assertEqual(out['openclaw'], {'not_read': 'FileNotFoundError'})
        self.assertNotIn('connections', out)


class Consent(unittest.TestCase):
    def setUp(self):
        self.f = fleet_with(self, [])
        self.reads = []
        self.f.support_read = lambda what: self.reads.append(what) or {'what': what}
        self.f.support_due, self.f.last = False, {}

    def waiting(self, *whats):
        def call(method, path, body=None, timeout=40):
            self.f.relay.calls.append((method, path, body))
            if (method, path) == ('GET', '/support'):
                return {'requests': [{'id': f'sr_{n}', 'what': w} for n, w in enumerate(whats)]}
            if path == '/support-access':
                return {'accesses': [{'at': '2026-10-27T08:00:00+00:00', 'what': 'The Machine team: read the settings'}]}
            return {'ok': True}
        self.f.relay.call = call
        self.f.support_due = True

    def answers(self):
        return [body for method, path, body in self.f.relay.calls if (method, path) == ('POST', '/support')]

    def test_nothing_is_read_while_the_owner_has_not_allowed_it_here(self):
        self.waiting('settings')
        self.assertEqual(self.f.support_round(), ['sr_0'])
        self.assertEqual(self.reads, [])
        self.assertEqual(self.answers(), [{'id': 'sr_0', 'result': {'refused': 'Support access is off on this Machine.'}}])

    def test_the_owners_switch_lets_it_answer_for_24_hours_and_off_again(self):
        self.waiting()
        view = self.f.support_access(True)
        self.assertTrue(view['until'])
        self.assertEqual(view['accesses'][0]['what'], 'The Machine team: read the settings')
        self.assertIn(('POST', '/support-access', {'allow': True}), self.f.relay.calls)
        self.waiting('settings', 'logs', 'shell')
        self.f.support_round()
        self.assertEqual(self.reads, ['settings', 'logs'])  # only the reads it has
        self.assertEqual(self.answers()[2]['result'], {'refused': 'This Machine has no shell read.'})
        self.assertIsNone(self.f.support_access(False)['until'])
        self.waiting('logs')
        self.f.support_round()
        self.assertEqual(self.reads, ['settings', 'logs'])
        self.f.set_meta('support_access_until', '2020-01-01T00:00:00+00:00')  # ended by itself
        self.assertIsNone(self.f.support_until())

    def test_while_it_is_on_it_looks_by_itself_a_machine_in_no_fleet_has_no_inbox(self):
        self.waiting()
        self.f.support_access(True)
        self.waiting('logs')
        self.f.support_due = False
        self.assertEqual(self.f.support_round(), ['sr_0'])
        self.waiting('logs')
        self.f.support_due = False
        self.assertEqual(self.f.support_round(), [])  # not again within SUPPORT_POLL
        self.f.support_access(False)
        self.f.last['support'] = 0.0
        self.assertEqual(self.f.support_round(), [])  # off: only when the inbox says so

    def test_the_control_plane_saying_so_is_not_enough(self):
        self.waiting('logs')
        self.f.relay.call('POST', '/support-access', {'allow': True})  # anything else telling the control plane
        self.f.support_round()
        self.assertEqual(self.reads, [])

    def test_only_from_the_owners_dashboard(self):
        self.assertIn('support_access', assistant.SUPPORT_ACTIONS)
        self.assertIn('support_access', assistant.OWNER_ACTIONS)
        self.assertIn('support_access', assistant.DASHBOARD_ACTIONS)
        app = object.__new__(assistant.App)
        app.config, app.config_path, app.fleet = {'accounts': []}, None, self.f
        self.waiting()
        with self.assertRaises(ValueError):
            app.action('support_access', {'allow': True}, owner_dashboard=False)
        self.assertIsNone(self.f.support_until())
        self.assertTrue(app.action('support_access', {'allow': True}, owner_dashboard=True)['until'])
        app.fleet = None
        with self.assertRaises(ValueError):
            app.action('support_access', {}, owner_dashboard=True)

    def test_unreachable_account_still_shows_the_switch_state(self):
        app = object.__new__(assistant.App)
        app.config, app.config_path, app.fleet = {'accounts': []}, None, self.f

        def away(*args, **kwargs):
            raise fleet.Unavailable('away')
        self.f.relay.call = away
        self.assertTrue(app.action('support_access', {}, owner_dashboard=True)['error'])
        with self.assertRaisesRegex(ValueError, 'reach your account'):
            app.action('support_access', {'allow': True}, owner_dashboard=True)


if __name__ == '__main__':
    unittest.main()

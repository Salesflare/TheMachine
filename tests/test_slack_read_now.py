"""A to-do's run reads Slack through the Slack connection, never the browser, and a stuck to-do never sends the owner
into the Machine's settings (agent users 2026-11-09: a founder's Halvorsen to-do said "Browser access is still
disabled; enable it in your Machine's OpenClaw settings" while Slack was connected). The cause: Leo's message came in
on a quiet channel a minute after its last read, and a quiet channel rests a day between reads, so the run found
nothing collected and reached for the browser. Now the run asks the Slack connection to read that conversation next
(slack_read), and a source that isn't connected is one plain tap on the to-do (Connect Slack). Offline: nothing sent."""
import importlib.util
import json
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('slack_read_now_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.sources import slack as slack_source  # noqa: E402

DAY = 86400
SLACK = {'id': 'work-slack', 'service': 'slack', 'user_id': 'U0RILEY01', 'email': 'riley@studio.example',
         'slack_host': 'studio.slack.com', 'boundary': 'work:Studio'}
MAIL = {'id': 'work-gmail', 'service': 'gmail', 'transport': 'gog', 'email': 'riley@studio.example', 'boundary': 'work:Studio'}


class Fake:
    """Slack's Web API for one workspace: #general (busy), #proj-halvorsen (quiet) and a direct message."""

    def __init__(self, messages):
        self.messages, self.calls = messages, []

    def profile(self):
        pass

    def get(self, method, params=None):
        self.calls.append((method, dict(params or {})))
        found = self.messages.get((params or {}).get('channel'), []) if method == 'conversations.history' else []
        return {'ok': True, 'messages': found, 'has_more': False, 'response_metadata': {'next_cursor': ''}}


class Base(unittest.TestCase):
    accounts = [SLACK, MAIL]

    def setUp(self):
        slack_source.READ_NOW.clear(); self.addCleanup(slack_source.READ_NOW.clear)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = self.accounts
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': self.accounts, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config


class ReadNow(Base):
    def setUp(self):
        super().setUp()
        now = self.now = time.time()
        # Read a minute ago, nothing then; Leo wrote right after. A quiet channel's next read is tomorrow.
        self.store.commit_page('work-slack', {
            'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{now - 7 * DAY:.6f}', 'next_discovery': now + DAY,
            'titles_named': True, 'channels': [
                {'id': 'C0GENERAL1', 'name': 'general', 'type': 'channel', 'threads': [], 'last_scan': f'{now - 600:.6f}',
                 'last_activity': now - 3000, 'due': now + 3000, 'next_full': now + DAY},
                {'id': 'C0HALVORS1', 'name': 'proj-halvorsen', 'type': 'channel', 'threads': [], 'last_scan': f'{now - 60:.6f}',
                 'due': now + DAY, 'next_full': now + DAY},
                {'id': 'D0LEO00001', 'name': 'DM U0LEO0002', 'type': 'dm', 'threads': [], 'last_scan': f'{now - 60:.6f}',
                 'due': now + 600, 'next_full': now + DAY}]}, [])
        self.slack = Fake({'C0HALVORS1': [{'type': 'message', 'ts': f'{now - 30:.6f}', 'user': 'U0LEO0002',
                                          'text': 'Two homepage directions for Halvorsen are ready for a first look.'}]})

    def read(self, **args):
        return self.app.action('slack_read', {'channel': '#proj-halvorsen', **args})

    def test_a_quiet_channel_waits_a_day_unless_a_run_asks_for_it(self):
        self.assertFalse(a.sync_slack(self.store, {}, SLACK, self.slack)['more'])
        self.assertEqual(self.slack.calls, [])  # nothing due: Leo's message would wait until tomorrow
        asked = self.read()
        self.assertEqual((asked['status'], asked['channel'], asked['account_id']), ('reading', 'proj-halvorsen', 'work-slack'))
        self.assertIn('again in about a minute', asked['note'])
        self.assertEqual(self.read()['status'], 'reading')  # asking again changes nothing until the read is in
        a.sync_slack(self.store, {}, SLACK, self.slack)
        self.assertEqual([(m, p['channel']) for m, p in self.slack.calls], [('conversations.history', 'C0HALVORS1')])  # first, before #general
        found = self.read()
        self.assertEqual(found['status'], 'read')
        events = self.store.events(['work-slack'], event_ids=found['event_ids'])
        self.assertEqual([e['body'] for e in events], ['Two homepage directions for Halvorsen are ready for a first look.'])
        self.assertIn('events', found['note'])
        a.sync_slack(self.store, {}, SLACK, self.slack)
        self.assertEqual(len(self.slack.calls), 1)  # once read, it rests as before

    def test_by_id_too_and_a_conversation_they_are_not_in_is_named_plainly(self):
        self.assertEqual(self.read(channel='slack:C0HALVORS1')['status'], 'reading')
        gone = self.read(channel='#design-crit')
        self.assertEqual(gone['status'], 'not_found')
        self.assertIn('#proj-halvorsen', gone['conversations'])
        with self.assertRaisesRegex(ValueError, 'channel'):
            self.read(channel=' ')

    def test_a_channel_slack_refuses_ends_the_ask(self):
        class Refusing(Fake):
            def get(self, method, params=None):
                raise a.SourceError('slack_not_in_channel:' + method)
        self.read()
        a.sync_slack(self.store, {}, SLACK, Refusing({}))  # the other conversations are read as before
        self.assertEqual(self.read()['status'], 'cannot_read')
        self.assertFalse(slack_source.READ_NOW)


class NotConnected(Base):
    accounts = [MAIL]

    def test_no_slack_means_one_plain_tap_to_connect_it(self):
        out = self.app.action('slack_read', {'channel': '#proj-halvorsen'})
        self.assertEqual((out['status'], out['connect']), ('not_connected', 'slack'))
        self.assertIn('Never the browser', out['note'])


class Blocker(Base):
    accounts = [MAIL]

    def card(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row

    def start(self):
        self.store.commit_page('work-gmail', {}, [{
            'account_id': 'work-gmail', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-11-08T15:00:00+00:00',
            'title': 'Revised homepage proposal', 'body': 'Could we see the revised homepage by Tuesday?',
            'metadata': {'from': 'Jonas <jonas@halvorsen.example>', 'thread_id': 't1'}, 'deleted': False}])
        sid = self.app.action('suggest', {'dedupe_key': 'halvorsen:handoff', 'title': 'Hand the Halvorsen homepage to Leo',
                                          'body': 'Leo has **two directions** ready.', 'event_ids': [1]})['id']
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        sent = []
        self.app.preparation_step(lambda req: sent.append(req) or {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']
        return sid, job, sent[-1]['message']

    def test_a_run_that_needs_slack_offers_connect_slack_and_never_a_setting(self):
        sid, job, message = self.start()
        self.assertIn('connect=<that source', message)
        self.assertIn("This Machine's own setup is never their step", message)
        self.assertNotIn('assistant_signals slack_read', message)  # no Slack here: nothing to read it with
        for wrong in ('gateway', 'Slack!', 3):
            with self.assertRaisesRegex(ValueError, 'connect'):
                self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect=wrong)
        with self.assertRaisesRegex(ValueError, 'one of them'):
            self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect='slack', move_to='personal')
        with self.assertRaisesRegex(ValueError, 'gmail is connected already'):
            self.store.preparation_blocked(sid, job, 'The mailbox is off.', connect='gmail')
        self.app.action('preparation_blocked', {'suggestion_id': sid, 'job_id': job, 'connect': 'slack', 'questions': [],
                                                'reason': "Slack isn't connected, so I can't read Leo's reply. Connect it and I'll pick this up."})
        card = self.card(sid)
        self.assertEqual((card['preparation_status'], card['preparation_connect']), ('blocked', 'slack'))
        self.assertEqual(self.store.resume_connected(), [])  # still not connected: it waits
        self.assertEqual(self.card(sid)['preparation_status'], 'blocked')
        self.store.accounts = self.app.config['accounts'] = [SLACK, MAIL]  # they connect Slack
        self.app.preparation_step(lambda req: {'status': 'admitted'})  # it carries on by itself: no Try again to find
        card = self.card(sid)
        self.assertNotEqual(card['preparation_status'], 'blocked')
        self.assertIsNone(card['preparation_connect'])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT source FROM decisions WHERE suggestion_id=? AND choice='retry'", (sid,)).fetchone()['source'], 'connected')
        self.assertEqual(self.store.resume_connected(), [])  # once


class Connected(Blocker):
    accounts = [SLACK, MAIL]

    def test_a_run_with_slack_connected_reads_it_there(self):
        sid, job, message = self.start()
        self.assertIn('assistant_signals slack_read', message)
        self.assertIn('Never open Slack in the browser', message)
        with self.assertRaisesRegex(ValueError, 'slack is connected already.*slack_read.*never the browser'):
            self.store.preparation_blocked(sid, job, "Slack isn't connected.", connect='slack')

    test_a_run_that_needs_slack_offers_connect_slack_and_never_a_setting = None


if __name__ == '__main__':
    unittest.main()

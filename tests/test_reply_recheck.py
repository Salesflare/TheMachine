"""Any reply the owner approved is checked right before it goes (follow_ups.reply_since, App.follow_up_recheck): a
message from someone else in its conversation, synced after the draft was saved, holds it ("Not sent: new message in
the thread", with that message on the to-do). The owner's own messages, what was synced before the draft and automated
senders don't hold it. A Send after the hold goes unless something newer came. A send approved by voice with an undo
delay is checked when it goes, not when it was approved. No live sends or reads: a fake outbox, collected messages."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import follow_ups
import timeutil
from seams import patch_everywhere  # noqa: E402
from test_follow_ups import FakeOutbox, GMAIL
import machine.main as machine_main
import machine.sources.gmail as machine_sources_gmail
from machine.store.decisions import draft_saved
import sources

T0 = '2026-10-19T09:00:00+00:00'


def mail(source_id, at, who='Sam Rivera <sam@client.example>', mine=False, thread='T', **meta):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Pilot',
            'body': 'About the pilot: ' + source_id, 'deleted': False,
            'metadata': {'from': 'owner@example.com' if mine else who, 'to': 'sam@client.example' if mine else 'owner@example.com',
                         'thread_id': thread, 'labels': ['SENT'] if mine else ['INBOX'], 'message-id': f'<{source_id}@mail.example>', **meta}}


def slack(source_id, at, user, ts, thread_ts=None, channel='D1'):
    return {'account_id': 'slack', 'source_id': source_id, 'kind': 'slack.message', 'occurred_at': at, 'title': 'DM', 'body': source_id,
            'deleted': False, 'metadata': {'channel_id': channel, 'channel_name': 'DM Sam', 'conversation_type': 'dm', 'user_id': user,
                                           'message_ts': ts, 'thread_ts': thread_ts or ts}}


class ReplyRecheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(timeutil, 'now', return_value='2026-10-19T08:00:00+00:00')
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        unread = patch.object(machine_sources_gmail.Gmail, 'get', side_effect=sources.SourceError('offline'))  # never a live read
        unread.start()
        self.addCleanup(unread.stop)
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [mail('in1', '2026-10-19T07:50:00+00:00')])
        with self.store.connect() as db:
            first = db.execute("SELECT id FROM events WHERE source_id='in1'").fetchone()[0]
        self.sid = self.store.suggest('reply-sam', 'Reply to Sam', 'Answer about the pilot', [first])['id']
        self.transport = FakeOutbox()

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value=stamp)
        self.clock.start()

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL], 'digest_at': '08:30'}
        app.model_usage = app.usage_limit = app.fleet = None
        app.teammate_addresses = lambda: []
        return app

    def prepared(self, saved_at=T0, **extra):
        """The draft saved at `saved_at` (draft_saves), as a preparation saves it."""
        self.at(saved_at)
        draft = {'kind': 'email', 'account_id': 'work', 'from': 'owner@example.com', 'to': ['sam@client.example'], 'subject': 'Re: Pilot',
                 'body': 'Hi Sam, here it is.', 'thread_id': 'T', 'revision': 'r1', **extra}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), self.sid))
            draft_saved(db, self.sid, draft, saved_at)
        return draft

    def sync(self, at, *events, account='work'):
        """Messages the sync brings in at `at` (their ingested_at)."""
        self.at(at)
        self.store.commit_page(account, {}, list(events))

    def run_outbox(self, at):
        self.at(at)
        return self.app().action_step(self.transport)

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT status,error FROM action_jobs WHERE suggestion_id=?', (self.sid,)).fetchone())

    def status(self):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
            return row['status'], self.store.suggestion_result(row, db).get('action_status')

    def test_a_reply_synced_after_the_draft_holds_the_send_and_a_second_send_goes(self):
        self.prepared()
        self.at('2026-10-19T09:05:00+00:00')
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('in2', '2026-10-19T09:04:00+00:00'))  # Sam wrote again, synced after the draft
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'held')
        self.assertEqual(self.transport.sent, [])
        self.assertEqual(self.job(), {'status': 'blocked', 'error': follow_ups.HELD})
        status, state = self.status()
        self.assertEqual(status, 'prepared')  # the to-do stays open: only the send waits
        with self.store.connect() as db:
            in2 = db.execute("SELECT id FROM events WHERE source_id='in2'").fetchone()[0]
        self.assertEqual((state['held_by']['event_id'], state['held_by']['from'], state['held_by']['mine']), (in2, 'Sam Rivera', False))
        self.assertIsNone(self.run_outbox('2026-10-19T09:06:20+00:00'))  # nothing goes by itself
        # The owner read it and taps Send again: it goes
        self.at('2026-10-19T09:07:00+00:00')
        self.store.confirm_action(self.sid, 'r1', 'tap-2', 'dashboard')
        self.assertEqual(self.run_outbox('2026-10-19T09:07:05+00:00'), 'sent')
        self.assertEqual([sid for sid, _ in self.transport.sent], [self.sid])

    def test_a_second_send_is_held_again_by_a_message_newer_than_the_hold(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('in2', '2026-10-19T09:04:00+00:00'))
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'held')
        self.sync('2026-10-19T09:08:00+00:00', mail('in3', '2026-10-19T09:07:30+00:00'))  # one more, after the hold
        self.at('2026-10-19T09:09:00+00:00')
        self.store.confirm_action(self.sid, 'r1', 'tap-2', 'dashboard')
        self.assertEqual(self.run_outbox('2026-10-19T09:09:05+00:00'), 'held')
        self.assertEqual(self.transport.sent, [])
        self.at('2026-10-19T09:10:00+00:00')
        self.store.confirm_action(self.sid, 'r1', 'tap-3', 'dashboard')
        self.assertEqual(self.run_outbox('2026-10-19T09:10:05+00:00'), 'sent')

    def test_the_owners_own_message_holds_nothing(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('out2', '2026-10-19T09:04:00+00:00', mine=True))
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'sent')

    def test_a_message_synced_before_the_draft_holds_nothing(self):
        self.sync('2026-10-19T08:30:00+00:00', mail('in2', '2026-10-19T08:29:00+00:00'))  # in front of the owner with the draft
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'sent')

    def test_an_automated_sender_holds_nothing(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('auto1', '2026-10-19T09:04:00+00:00', who='Pilot tool <no-reply@tool.example>'),
                  mail('ooo1', '2026-10-19T09:04:30+00:00', precedence='bulk'))  # a notification, an out-of-office reply
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'sent')

    def test_a_message_the_owner_answered_since_holds_nothing(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('in2', '2026-10-19T09:03:00+00:00'), mail('out2', '2026-10-19T09:04:00+00:00', mine=True))
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'sent')

    def test_another_thread_holds_nothing(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'tap-1', 'dashboard')
        self.sync('2026-10-19T09:06:00+00:00', mail('other', '2026-10-19T09:04:00+00:00', thread='U'))
        self.assertEqual(self.run_outbox('2026-10-19T09:06:10+00:00'), 'sent')

    def test_a_voice_send_is_checked_when_it_goes_not_when_it_was_approved(self):
        self.prepared()
        self.at('2026-10-19T09:05:00+00:00')
        self.store.confirm_action(self.sid, 'r1', 'voice-1', 'voice', hold=10)  # Undo in the chat for ten seconds
        self.assertIsNone(self.run_outbox('2026-10-19T09:05:02+00:00'))  # still waiting out its undo
        self.sync('2026-10-19T09:05:05+00:00', mail('in2', '2026-10-19T09:05:04+00:00'))  # Sam writes during the delay
        self.assertEqual(self.run_outbox('2026-10-19T09:05:12+00:00'), 'held')
        self.assertEqual(self.transport.sent, [])

    def test_an_automated_follow_up_source_is_not_checked_here(self):
        self.prepared()
        self.store.confirm_action(self.sid, 'r1', 'auto-1', 'auto_follow_up')
        self.sync('2026-10-19T09:06:00+00:00', mail('in2', '2026-10-19T09:04:00+00:00'))
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM action_jobs WHERE suggestion_id=?', (self.sid,)).fetchone())
        self.assertIsNone(self.app().follow_up_recheck(job, json.loads(job['payload'])))

    def test_a_busy_slack_dm_counts_only_its_own_lines_or_the_reply_thread(self):
        with self.store.connect() as db:
            job = {'id': 'j1', 'suggestion_id': self.sid, 'revision': 'r1'}
            draft_saved(db, self.sid, {'kind': 'slack', 'revision': 'r1'}, T0)
        self.sync('2026-10-19T08:00:00+00:00', slack('s1', '2026-10-19T07:59:00+00:00', 'U0SAM', '1.0'), account='slack')
        # After the draft: a reply in another thread of the DM, and the owner's own line
        self.sync('2026-10-19T09:06:00+00:00', slack('s2', '2026-10-19T09:04:00+00:00', 'U0SAM', '2.5', thread_ts='2.0'),
                  slack('s3', '2026-10-19T09:04:10+00:00', 'U0OWN', '3.0'), account='slack')
        dm = {'kind': 'slack', 'account_id': 'slack', 'user_id': 'U0SAM'}
        in_thread = {**dm, 'thread': {'channel_id': 'D1', 'ts': '2.0', 'dm': True}}
        owner = lambda e: json.loads(e['metadata']).get('user_id') == 'U0OWN'
        with self.store.connect() as db:
            self.assertEqual(follow_ups.reply_since(db, job, dm, owner), [])  # the other thread isn't this conversation
            self.assertEqual([n['at'] for n in follow_ups.reply_since(db, job, in_thread, owner)], ['2026-10-19T09:04:00+00:00'])
        self.sync('2026-10-19T09:07:00+00:00', slack('s4', '2026-10-19T09:06:30+00:00', 'U0SAM', '4.0'), account='slack')
        with self.store.connect() as db:
            self.assertEqual([n['at'] for n in follow_ups.reply_since(db, job, dm, owner)], ['2026-10-19T09:06:30+00:00'])


if __name__ == '__main__':
    unittest.main()

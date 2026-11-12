"""Already handled elsewhere (2026-11-09): "Inform Sam about covering support chat tomorrow" came up as a prepared
handoff although the owner had asked Sam an hour before, in the group DM with the requester, and Sam had said yes.
That group DM rests hours between Slack reads, the checks only looked at the requester, and the run saved its handoff
while saying the Slack refresh was still pending. Now the conversations with everyone involved (requester and target,
group DMs too) are read first and checked, and a to-do newer messages show done closes by itself. Made-up names, no
live calls."""
import json
import tempfile
import time
import unittest
from pathlib import Path

import test_ux as ux
from seams import patch_everywhere  # noqa: E402
from machine.sources import slack as slack_source  # noqa: E402
from machine.app import handled_check  # noqa: E402
a = ux.a

SLACK = {'id': 'work-slack', 'service': 'slack', 'transport': 'maton', 'user_id': 'U0RILEY001', 'slack_host': 'studio.slack.com',
         'boundary': 'work:Studio'}
MONDAY = '2026-11-09T10:30:00+00:00'
DM = {'id': 'D0ANA00001', 'name': 'DM U0ANA00001', 'type': 'dm'}
TRIO = {'id': 'G0TRIO0001', 'name': 'mpdm-riley--sam--ana-1', 'type': 'group'}
OTHER = {'id': 'G0OTHER001', 'name': 'mpdm-riley--lee-1', 'type': 'group'}


def ts(stamp):
    return f"{a.dt.datetime.fromisoformat(stamp).timestamp():.6f}"


def message(channel, user, stamp, text):
    return slack_source.slack_event(SLACK, channel, {'type': 'message', 'ts': ts(stamp), 'user': user, 'text': text})


class HandledElsewhere(unittest.TestCase):
    def setUp(self):
        slack_source.READ_NOW.clear()
        self.addCleanup(slack_source.READ_NOW.clear)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(a, 'now', return_value=MONDAY)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'U0RILEY001'}
        with self.store.connect() as db:
            a.graph.ensure(db)
            for uid, name in (('U0ANA00001', 'Ana Ortiz'), ('U0SAM00001', 'Sam Reyes'), ('U0LEE00001', 'Lee Park')):
                db.execute('INSERT INTO identity_names(identifier,name,email,checked_at) VALUES(?,?,?,?)',
                           ('slack:' + uid, name, name.split()[0].lower() + '@studio.example', MONDAY))
        self.read_at = time.time() - 6 * 3600  # the group DM was last read hours ago
        self.commit([
            message(TRIO, 'U0SAM00001', '2026-11-06T10:00:00+00:00', 'Which customer was that again?'),
            message(TRIO, 'U0ANA00001', '2026-11-06T10:05:00+00:00', 'The one from Friday.'),
            message(OTHER, 'U0LEE00001', '2026-11-06T11:00:00+00:00', 'Lunch?'),
            message(DM, 'U0ANA00001', '2026-11-09T08:50:00+00:00', 'Tomorrow I will be off for the funeral.'),
            message(DM, 'U0RILEY001', '2026-11-09T08:55:00+00:00', 'Of course. Let me inform Sam too, as he will take over chat.')])
        self.ask = self.event('U0RILEY001', DM)

    def state(self, trio_scan):
        channels = []
        for c, scan in ((DM, time.time() - 60), (TRIO, trio_scan), (OTHER, trio_scan)):
            channels.append({**c, 'threads': [], 'last_scan': f'{scan:.6f}', 'due': time.time() + 6 * 3600, 'next_full': time.time() + 86400})
        return {'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{time.time() - 7 * 86400:.6f}',
                'next_discovery': time.time() + 86400, 'titles_named': True, 'channels': channels}

    def commit(self, events, trio_scan=None):
        self.store.commit_page('work-slack', self.state(trio_scan or self.read_at), events)
        with self.store.connect() as db:
            a.graph.build(db, {'accounts': [SLACK]}, a.now())

    def slack_reads(self):
        """Slack's next turn read the group DM: the owner asked Sam there, and Sam said yes."""
        self.commit([message(TRIO, 'U0RILEY001', '2026-11-09T08:56:00+00:00', 'Ana is off tomorrow. Can you take over chat, Sam?'),
                     message(TRIO, 'U0SAM00001', '2026-11-09T09:53:00+00:00', 'Yes, of course I can.'),
                     message(OTHER, 'U0LEE00001', '2026-11-09T09:10:00+00:00', 'Lunch today?')], trio_scan=time.time())
        return self.event('U0SAM00001', TRIO, latest=True)

    def event(self, user, channel, latest=False):
        with self.store.connect() as db:
            rows = [r for r in db.execute("SELECT id,metadata FROM events ORDER BY occurred_at" + (' DESC' if latest else ''))
                    if json.loads(r['metadata']).get('user_id') == user and json.loads(r['metadata']).get('channel_id') == channel['id']]
        return rows[0]['id']

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}  # no model here: never a live turn
        return app

    def asked(self):
        return {channel for (_, channel) in slack_source.READ_NOW}

    # who and where

    def test_the_group_dm_with_requester_and_target_comes_first(self):
        app = self.app()
        with self.store.connect() as db:
            people = app.handled_people(db, [self.ask], 'inform Sam about covering support chat')
            found = handled_check.shared_conversations(db, people, app.slack_channels())
        self.assertEqual(len(people), 2)  # Ana (the DM), Sam (named)
        self.assertEqual(found[0][1:], ('G0TRIO0001', 2))
        self.assertNotIn('G0OTHER001', [c for _, c, _ in found])

    # a due promise

    def promise(self):
        pid = self.app().action('promise', {'direction': 'mine', 'event_id': self.ask, 'who': 'Ana Ortiz',
                                             'what': 'inform Sam about covering support chat on Tuesday', 'due': '2026-11-10'})['id']
        with self.store.connect() as db:
            db.execute('UPDATE promises SET check_at=? WHERE id=?', ('2026-11-09T09:00:00+00:00', pid))
        return pid

    def test_a_due_promise_waits_for_the_group_dm_and_closes_kept_on_the_yes(self):
        pid = self.promise()
        prompts = []
        app = self.app()
        app.promise_check_model = lambda config, text: (prompts.append(text), json.dumps(
            [{'promise': pid, 'state': 'kept', 'event_id': yes, 'reason': 'Sam said yes in the group chat'}]))[1]
        app.promise_step()
        self.assertEqual(self.asked(), {'G0TRIO0001'})  # the group DM is read first
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM promises WHERE id=?', (pid,)).fetchone()[0], 'open')
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)  # no to-do meanwhile
        yes = self.slack_reads()
        app.promise_step()
        self.assertIn('Yes, of course I can.', prompts[0])
        self.assertNotIn('Lunch today?', prompts[0])
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute('SELECT status,note FROM promises WHERE id=?', (pid,)).fetchone()), ('kept', 'Sam said yes in the group chat'))
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 0)

    def test_a_read_that_never_comes_holds_the_promise_only_for_a_while(self):
        pid = self.promise()
        app = self.app()
        app.promise_check_model = lambda config, text: '[]'
        app.promise_step()
        app._handled_waits = {k: v - handled_check.HOLD_SECONDS - 1 for k, v in app._handled_waits.items()}
        app.promise_step()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM promises WHERE id=?', (pid,)).fetchone()[0], 'carded')

    # a to-do's run, before its handoff is saved

    def card(self):
        return self.store.suggest('work:cover-chat', 'Inform Sam about covering support chat', 'Ana is off.', [self.ask])['id']

    HANDOFF = [{'kind': 'handoff', 'to_email': 'sam@studio.example', 'to_name': 'Sam Reyes', 'body': 'Ana is off tomorrow. Can you cover chat?'}]

    def test_a_run_waits_for_slack_then_reads_the_yes_and_the_to_do_closes_by_itself(self):
        sid, app = self.card(), self.app()
        wait = app.handled_gate(sid, 'job1', self.HANDOFF)
        self.assertIn('mpdm-riley--sam--ana-1', wait)
        self.assertIn('Sleep', wait)
        yes = self.slack_reads()
        found = app.handled_gate(sid, 'job1', self.HANDOFF)
        self.assertIn(f'event {yes}', found)
        self.assertIn('already_done', found)
        self.assertIsNone(app.handled_gate(sid, 'job1', self.HANDOFF))  # named once: saving again as it is goes through
        self.assertTrue(app.handled_close(sid, 'job1', 'Sam already said yes in the group chat on Monday.'))
        with self.store.connect() as db:
            row = db.execute('SELECT status,undo_until FROM suggestions WHERE id=?', (sid,)).fetchone()
            decision = db.execute("SELECT source,feedback FROM decisions WHERE suggestion_id=? AND choice='complete'", (sid,)).fetchone()
        self.assertEqual(row['status'], 'completed')
        self.assertTrue(row['undo_until'])
        self.assertEqual(tuple(decision), ('handled', 'Sam already said yes in the group chat on Monday.'))
        with self.store.connect() as db:
            lines = [i['text'] for i in app.card_chat_service(db, sid)[0] if i['kind'] == 'event']
        self.assertIn('Closed by itself: Sam already said yes in the group chat on Monday.', lines)

    def test_a_note_or_a_to_do_without_people_is_never_held(self):
        sid, app = self.card(), self.app()
        self.assertIsNone(app.handled_gate(sid, 'job2', [{'kind': 'open', 'url': 'https://example.com'}]))
        self.assertIsNone(app.handled_gate(sid, None, self.HANDOFF))  # no run: nothing to wait on

    # a to-do already shown

    def test_a_shown_to_do_closes_when_a_newer_message_shows_it_done_and_is_judged_once(self):
        sid, app = self.card(), self.app()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(self.HANDOFF[0]), sid))
        calls = []
        app.handled_check_model = lambda config, text: (calls.append(text), '[]')[1]
        self.assertEqual(app.handled_step(), 0)
        self.assertEqual(calls, [])  # nothing newer: no model turn
        yes = self.slack_reads()
        self.assertEqual(app.handled_step(), 0)  # read, judged open
        self.assertEqual(len(calls), 1)
        self.assertIn('Yes, of course I can.', calls[0])
        app.handled_step()
        self.assertEqual(len(calls), 1)  # the same messages are judged once
        self.commit([message(TRIO, 'U0SAM00001', '2026-11-09T10:20:00+00:00', 'I will take chat tomorrow, no worries.')], trio_scan=time.time())
        later = self.event('U0SAM00001', TRIO, latest=True)
        app.handled_check_model = lambda config, text: json.dumps([{'todo': sid, 'state': 'done', 'event_id': later, 'reason': 'Sam took chat for tomorrow'}])
        self.assertEqual(app.handled_step(), 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'completed')
        self.assertNotEqual(yes, later)
        self.assertFalse(self.store.close_handled(sid, 'again', [later]))  # once

    def test_a_to_do_without_a_message_to_send_closes_when_the_owner_settled_it_in_its_conversation(self):
        """An answer the owner owes, with nothing drafted: they answered in the DM itself. The same short turn reads it."""
        sid = self.store.suggest('work:ana-off', 'Answer Ana about tomorrow', 'Ana is off tomorrow.', [self.event('U0ANA00001', DM)])['id']
        app, calls = self.app(), []
        app.handled_check_model = lambda config, text: (calls.append(text), '[]')[1]
        self.assertEqual(app.handled_step(), 0)  # judged open: it stays
        self.assertIn('what the to-do says (no message drafted)', calls[0])
        self.assertIn('Of course. Let me inform Sam too', calls[0])
        self.assertIn('from the owner', calls[0])
        app.handled_step()
        self.assertEqual(len(calls), 1)  # judged once
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'pending')
        app._handled_judged = {}
        app.handled_check_model = lambda config, text: json.dumps([{'todo': sid, 'state': 'done', 'event_id': self.ask, 'reason': 'Answered Ana in Slack'}])
        self.assertEqual(app.handled_step(), 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'completed')

    def test_a_to_do_that_looks_done_or_waits_on_others_is_not_read_again(self):
        sid = self.store.suggest('work:ana-off', 'Answer Ana about tomorrow', 'Ana is off tomorrow.', [self.event('U0ANA00001', DM)])['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'waiting', 'waiting_on': 'Ana'}), sid))
        app, calls = self.app(), []
        app.handled_check_model = lambda config, text: (calls.append(text), '[]')[1]
        app.handled_step()
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()

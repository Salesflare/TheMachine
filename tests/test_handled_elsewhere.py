"""Already handled elsewhere (2026-11-09): "Inform Sam about covering support chat tomorrow" came up as a prepared
handoff although the owner had asked Sam an hour before, in the group DM with the requester, and Sam had said yes.
That group DM rests hours between Slack reads, the checks only looked at the requester, and the run saved its handoff
while saying the Slack refresh was still pending. Now the conversations with everyone involved (requester and target,
group DMs too) are read first and checked, and a to-do newer messages show done closes by itself. Made-up names, no
live calls."""
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import test_ux as ux
from seams import patch_everywhere  # noqa: E402
from machine.sources import slack as slack_source  # noqa: E402
from machine import model_reply  # noqa: E402
from machine.app import handled_check  # noqa: E402
from machine.store import todo_moves  # noqa: E402
import datetime as dt
import graph
import machine.main as machine_main
from machine.app import sync as app_sync
import timeutil

SLACK = {'id': 'work-slack', 'service': 'slack', 'transport': 'maton', 'user_id': 'U0RILEY001', 'slack_host': 'studio.slack.com',
         'boundary': 'work:Studio'}
MONDAY = '2026-11-09T10:30:00+00:00'
DM = {'id': 'D0ANA00001', 'name': 'DM U0ANA00001', 'type': 'dm'}
TRIO = {'id': 'G0TRIO0001', 'name': 'mpdm-riley--sam--ana-1', 'type': 'group'}
OTHER = {'id': 'G0OTHER001', 'name': 'mpdm-riley--lee-1', 'type': 'group'}


def ts(stamp):
    return f"{dt.datetime.fromisoformat(stamp).timestamp():.6f}"


def message(channel, user, stamp, text):
    return slack_source.slack_event(SLACK, channel, {'type': 'message', 'ts': ts(stamp), 'user': user, 'text': text})


class HandledElsewhere(unittest.TestCase):
    def setUp(self):
        slack_source.READ_NOW.clear()
        self.addCleanup(slack_source.READ_NOW.clear)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(timeutil, 'now', return_value=MONDAY)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'U0RILEY001'}
        with self.store.connect() as db:
            graph.ensure(db)
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
            graph.build(db, {'accounts': [SLACK]}, timeutil.now())

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
        app = object.__new__(machine_main.App)
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
        self.assertIn('save again as it is, its steps included', wait)  # runs dropped the handoff while they waited (2026-11-23)
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

    def test_an_answer_in_the_source_s_own_old_thread_is_read_before_the_save(self):
        """The to-do comes from a three-day-old thread and the owner answered in it after the conversation's last read: no
        page of the conversation shows that, only the thread's own read."""
        stamp = time.time()
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', side_effect=lambda: dt.datetime.now(dt.timezone.utc).isoformat())
        self.clock.start()
        root, ask, answer, busy, other = (f'{stamp - hours * 3600:.6f}' for hours in (72, 70, 2, 5, 1))

        def raw(user, at, text, **more):
            return {'type': 'message', 'ts': at, 'user': user, 'text': text, **more}
        first = raw('U0SAM00001', root, 'Support planning', reply_count=2, latest_reply=answer)
        asked = raw('U0ANA00001', ask, 'Can you ask Sam to cover chat?', thread_ts=root)
        answered = raw('U0RILEY001', answer, 'Asked Sam, he covers it.', thread_ts=root)
        newer = raw('U0LEE00001', busy, 'Lunch', reply_count=1, latest_reply=other)
        noise = raw('U0LEE00001', other, 'Pizza', thread_ts=busy)
        for account in (SLACK, {**SLACK, 'fair_incremental': True}):
            for source, channel in ((ask, TRIO), (root, TRIO), (ask, {**TRIO, 'type': 'channel', 'name': 'support'})):
                with self.subTest(fair='fair_incremental' in account, root=source == root, type=channel['type']):
                    slack_source.READ_NOW.clear()
                    calls = []

                    class Slack:
                        def profile(self):
                            pass

                        def get(self, method, params=None):
                            calls.append((method, params.get('channel'), params.get('ts'), params.get('oldest')))
                            found = {root: [first, asked, answered], busy: [newer, noise]}.get(params.get('ts'), [newer]) if params['channel'] == channel['id'] else []
                            return {'ok': True, 'messages': [m for m in found if m['ts'] in (params.get('ts'),) or m['ts'] >= params['oldest']],
                                    'has_more': False, 'response_metadata': {'next_cursor': ''}}
                    state = self.state(stamp - 4 * 3600)
                    state['channels'][1] = {**state['channels'][1], **channel, 'threads': [root]}
                    with self.store.connect() as db:
                        db.execute("DELETE FROM events WHERE json_extract(metadata,'$.channel_id')=?", (channel['id'],))
                    self.store.commit_page('work-slack', state, [slack_source.slack_event(SLACK, channel, m) for m in
                                                                 ({**first, 'reply_count': 1, 'latest_reply': ask}, asked)])
                    with self.store.connect() as db:
                        graph.build(db, {'accounts': [SLACK]}, timeutil.now())
                        event = db.execute('SELECT id FROM events WHERE source_id=?', (f"{channel['id']}:{source}",)).fetchone()[0]
                    app = self.app()
                    app.config['accounts'] = [account]
                    key = f"{source}{channel['type']}{len(account)}"
                    sid = self.store.suggest('work:cover-' + key, 'Inform Sam about covering support chat ' + key, 'Ana is off.', [event])['id']
                    self.assertIn(channel['name'], app.handled_gate(sid, 'job' + key, self.HANDOFF))
                    for _ in range(12):
                        if not app_sync.sync_slack(self.store, {}, account, Slack())['more']:
                            break
                    self.assertIn(('conversations.replies', channel['id'], root, source), calls)
                    found = app.handled_gate(sid, 'job' + key, self.HANDOFF)
                    with self.store.connect() as db:
                        said = db.execute('SELECT id FROM events WHERE source_id=?', (f"{channel['id']}:{answer}",)).fetchone()[0]
                    self.assertIn(f'event {said}:', found or '')
                    kept = next(c for c in self.store.checkpoint('work-slack')['channels'] if c['id'] == channel['id'])
                    self.assertIn(root, kept['threads'])

    def test_a_run_s_own_slack_read_has_its_to_do_s_thread_too(self):
        """slack_read in the run of a to-do from that thread; another to-do's run reads only what is new."""
        reply = {'type': 'message', 'ts': ts('2026-11-06T11:30:00+00:00'), 'user': 'U0LEE00001', 'text': 'Well?', 'thread_ts': ts('2026-11-06T11:00:00+00:00')}
        self.commit([slack_source.slack_event(SLACK, OTHER, reply)])
        app = self.app()
        for event, named in ((self.event('U0LEE00001', OTHER, latest=True), {reply['thread_ts']}), (self.ask, set())):
            sid, job = self.store.suggest(f'work:thread-{event}', f'Answer Lee {event}', 'They asked.', [event])['id'], f'job{event}'.ljust(32, '0')
            with self.store.connect() as db:
                db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,'d',?,'running',?,?)",
                           (sid, job, MONDAY, MONDAY))
            slack_source.READ_NOW.clear()
            self.assertEqual(app.action('slack_read', {'channel': OTHER['id'], 'job_id': job})['status'], 'reading')
            self.assertEqual(set(slack_source.slack_read_threads('work-slack', OTHER['id'])), named)

    def test_with_the_plugin_s_wait_the_save_waits_for_slack_itself(self):
        """A run that slept with exec and saved again resent its whole session each time: the save waits here instead."""
        self.addCleanup(setattr, slack_source, 'WAIT_STEP', slack_source.WAIT_STEP)
        slack_source.WAIT_STEP = 0.02
        sid, app = self.card(), self.app()
        waited = app.handled_gate(sid, 'job3', self.HANDOFF, wait=0.1)  # Slack's turn doesn't come in time
        self.assertIn('This call waited for them already: save again as it is (it waits again), its steps included', waited)
        self.assertNotIn('Sleep', waited)
        self.assertIn('(0:00 of at most 15 minutes so far)', waited)
        app._handled_waits = {k: at - 245 for k, at in app._handled_waits.items()}
        # Never the same words three times: the Gateway ended a turn on its third identical refusal (2026-11-25)
        self.assertIn('(4:05 of at most 15 minutes so far)', app.handled_gate(sid, 'job3', self.HANDOFF, wait=0.1))
        reader = threading.Timer(0.1, self.slack_reads)
        reader.start()
        found = app.handled_gate(sid, 'job3', self.HANDOFF, wait=5)  # one call: waited for the read, then names the yes
        reader.join()
        self.assertIn(f"event {self.event('U0SAM00001', TRIO, latest=True)}", found)
        self.assertIn('already_done', found)

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
            last = todo_moves.history(db, sid)[-1]
            self.assertEqual((last['to'], last['reason']), ('completed', 'by_itself_handled'))
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

    def test_a_reply_that_cannot_be_read_judges_nothing_and_is_asked_a_few_times_only(self):
        sid = self.store.suggest('work:ana-off', 'Answer Ana about tomorrow', 'Ana is off tomorrow.', [self.event('U0ANA00001', DM)])['id']
        good = json.dumps([{'todo': sid, 'state': 'done', 'event_id': self.ask, 'reason': 'Answered Ana in Slack'}])
        app, calls, replies = self.app(), [], iter(['Looks done to me.', good[:-8], good[:-8], good])
        app.handled_check_model = lambda config, text: (calls.append(text), next(replies))[1]
        self.assertEqual(app.handled_step(), 0)
        self.assertEqual((len(calls), app.__dict__.get('_handled_judged')), (2, {}))
        self.assertEqual(app.handled_step(), 0)  # it rests first
        self.assertEqual(len(calls), 2)
        with patch.object(model_reply, 'REST_SECONDS', 0):
            broken, asked = self.app(), []
            broken.handled_check_model = lambda config, text: (asked.append(text), '[{"todo"')[1]
            for _ in range(10):
                broken.handled_step()
            self.assertEqual(len(asked), 2 * model_reply.TRIES)
            self.assertEqual(app.handled_step(), 1)  # read on the second ask
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

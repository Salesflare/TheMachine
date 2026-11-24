"""From when on something is news on a to-do (machine/store/evidence_moments.py): per conversation its evidence is in, and
since its newest message everywhere else. One moment for all of it hid the owner's answer in an older thread, and with a
meeting still ahead as evidence that moment lay in the future, so nothing was ever found. And the handled check's answer
that leaves a to-do out: asked once more, alone. Made-up data, no live calls."""
import json
import tempfile
import unittest
from pathlib import Path

import test_ux as ux  # noqa: F401
from seams import patch_everywhere  # noqa: E402
from machine.app import follow_ups as app_follow_ups, handled_check, promise_checks
from machine.sources import slack as slack_source
from machine.store import evidence_moments, review as store_review
import datetime as dt
import follow_ups
import graph
import machine.main as machine_main
import timeutil

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
CALENDAR = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Example', 'user_id': 'UOWNER1', 'slack_host': 'example.slack.com'}
NOW = '2026-10-19T09:00:00+00:00'
GROUP = {'id': 'G0TRIO0001', 'name': 'mpdm-owner--sam--ana-1', 'type': 'group'}


def mail(source_id, at, thread='t1', sent=False, who='sam@client.example', name='Sam Lee'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Contract', 'body': 'Words.', 'deleted': False,
            'metadata': {'from': 'owner@example.com' if sent else f'{name} <{who}>', 'to': who if sent else 'owner@example.com',
                         'thread_id': thread, 'labels': ['SENT'] if sent else ['INBOX'], 'message-id': f'<{source_id}@x>'}}


def meeting(source_id, at, updated=None):
    return {'account_id': 'cal', 'source_id': source_id, 'kind': 'calendar.event', 'occurred_at': at, 'title': 'Contract call', 'body': '', 'deleted': False,
            'metadata': {'start': {'dateTime': at}, 'end': {'dateTime': at}, 'end_at': at, 'updated': updated, 'status': 'confirmed',
                         'attendees': [{'email': 'sam@client.example', 'displayName': 'Sam Lee'}, {'email': 'owner@example.com', 'self': True}]}}


def group_message(user, at, text):
    stamp = f'{dt.datetime.fromisoformat(at).timestamp():.6f}'
    return slack_source.slack_event(SLACK, GROUP, {'type': 'message', 'ts': stamp, 'user': user, 'text': text})


class EvidenceMoments(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(timeutil, 'now', return_value=NOW)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}

    def commit(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            graph.build(db, {'accounts': [GMAIL, CALENDAR, SLACK]}, timeutil.now())
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, CALENDAR, SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False,
                      'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}  # no model here: never a live turn
        return app

    def since(self, ids):
        with self.store.connect() as db:
            return [(x['id'], x['where']) for x in promise_checks.activity_since(db, ids, {'UOWNER1'})]

    # each conversation from its own evidence on

    def test_an_answer_in_the_older_of_two_threads_is_found(self):
        first, answer, second, _ = self.commit(
            mail('a1', '2026-10-15T09:00:00+00:00'), mail('a2', '2026-10-16T09:00:00+00:00', sent=True),
            mail('b1', '2026-10-17T09:00:00+00:00', thread='t2', who='bo@other.example', name='Bo Ray'),
            mail('a0', '2026-10-14T09:00:00+00:00', sent=True))
        self.assertEqual(self.since([first, second]), [(answer, 'same conversation')])
        self.assertEqual(self.since([first, answer, second]), [])  # it is evidence itself

    def test_elsewhere_counts_from_the_newest_message(self):
        first, second, between, after = self.commit(
            mail('a1', '2026-10-15T09:00:00+00:00'), mail('b1', '2026-10-17T09:00:00+00:00', thread='t2'),
            mail('c1', '2026-10-16T09:00:00+00:00', thread='t3'), mail('c2', '2026-10-18T09:00:00+00:00', thread='t3'))
        self.assertEqual(self.since([first, second]), [(after, 'elsewhere')])
        self.assertNotEqual(between, after)

    def test_a_long_thread_shows_its_newest_messages(self):
        ids = self.commit(*[mail(f'a{n:02}', f'2026-10-15T09:{n:02}:00+00:00') for n in range(57)])
        with self.store.connect() as db:
            found = app_follow_ups.newer_activity(db, ids[:1], limit=3)
        self.assertEqual([x['id'] for x in found], ids[-3:])

    def test_an_answer_in_a_telegram_or_signal_chat_is_found(self):
        for kind in ('telegram.message', 'signal.message'):
            ask, answer, _ = self.commit(*[
                {'account_id': kind[:3], 'source_id': f'{kind}{n}', 'kind': kind, 'occurred_at': f'2026-10-1{n}T09:00:00+00:00', 'title': 'Sam Lee',
                 'body': 'Words.', 'deleted': False, 'metadata': {'chat_id': chat, 'chat_kind': 'dm', 'from_me': mine, 'message_id': str(n)}}
                for n, chat, mine in ((5, 'c1', False), (6, 'c1', True), (7, 'c2', True))])
            with self.store.connect() as db:
                found = app_follow_ups.newer_activity(db, [ask])
            self.assertEqual([(x['id'], x['channel'], x['who']) for x in found], [(answer, kind.split('.')[0], 'the owner')])

    def test_a_group_dm_counts_from_its_own_message(self):
        with self.store.connect() as db:
            graph.ensure(db)
            db.execute('INSERT INTO identity_names(identifier,name,email,checked_at) VALUES(?,?,?,?)', ('slack:U0SAM00001', 'Sam Lee', 'sam@client.example', NOW))
        ask, answer, other = self.commit(group_message('U0SAM00001', '2026-10-15T09:00:00+00:00', 'Can you cover Friday?'),
                                         group_message('UOWNER1', '2026-10-16T09:00:00+00:00', 'Done, I told Ana.'),
                                         mail('b1', '2026-10-17T09:00:00+00:00', thread='t2'))
        app = self.app()
        app.slack_channels = lambda: {'slack': [GROUP]}
        with self.store.connect() as db:
            found = app.handled_since(db, [ask, other], app.handled_people(db, [ask, other]))
        self.assertEqual([x['id'] for x in found], [answer])

    def test_a_busy_conversation_hides_no_answer_in_another(self):
        first, answer, second = self.commit(
            mail('a1', '2026-10-15T09:00:00+00:00'), mail('a2', '2026-10-16T09:00:00+00:00', sent=True),
            mail('b1', '2026-10-17T09:00:00+00:00', thread='t2'))
        self.commit(*[mail(f'b1{n:02}', f'2026-10-17T10:{n:02}:00+00:00', thread='t2') for n in range(10)],
                    *[mail(f'c1{n:02}', f'2026-10-18T10:{n:02}:00+00:00', thread='t3') for n in range(10)])
        found = self.since([first, second])
        self.assertEqual(len(found), 8)
        self.assertEqual(found[0], (answer, 'same conversation'))
        self.assertEqual([w for _, w in found], ['same conversation'] * 4 + ['elsewhere'] * 4)

    def test_what_came_before_the_owner_added_the_to_do_is_no_news(self):
        ask, _, after = self.commit(mail('a1', '2026-10-15T09:00:00+00:00'), mail('a2', '2026-10-16T09:00:00+00:00', sent=True),
                                    mail('a3', '2026-10-18T09:00:00+00:00', sent=True))
        card, = self.commit({'account_id': 'owner', 'source_id': 'o1', 'kind': 'owner.card', 'occurred_at': '2026-10-17T09:00:00+00:00',
                             'title': 'Contract', 'body': '', 'deleted': False, 'metadata': {}})
        self.assertEqual(self.since([ask, card]), [(after, 'same conversation')])

    # a meeting still ahead

    def test_a_meeting_still_ahead_hides_nothing(self):
        ask, call, answer = self.commit(mail('a1', '2026-10-16T09:00:00+00:00'), meeting('m1', '2026-10-26T09:00:00+00:00'),
                                        mail('c1', '2026-10-18T09:00:00+00:00', thread='t2', sent=True))
        self.assertEqual(self.since([ask, call]), [(answer, 'elsewhere')])

    def test_only_a_meeting_counts_by_when_it_was_changed(self):
        _, call, answer = self.commit(mail('a1', '2026-10-16T09:00:00+00:00'), meeting('m1', '2026-10-26T09:00:00+00:00', '2026-10-17T09:00:00.000Z'),
                                      mail('c1', '2026-10-18T09:00:00+00:00', thread='t2', sent=True))
        self.assertEqual(self.since([call]), [(answer, 'elsewhere')])
        with self.store.connect() as db:
            db.execute('UPDATE events SET metadata=? WHERE id=?', (json.dumps({'updated': None}), call))
            self.assertEqual(evidence_moments.Moments(db, [call]).everywhere, NOW)  # when it came in
            self.assertIsNone(evidence_moments.Moments(db, []).everywhere)

    def test_a_waiting_to_do_with_a_meeting_ahead_gets_their_answer(self):
        ask, call = self.commit(mail('a1', '2026-10-16T09:00:00+00:00'), meeting('m1', '2026-10-26T09:00:00+00:00'))
        sid = self.store.suggest('work:contract', 'Waiting on Sam', 'They will send it.', [ask, call])['id']
        answer, = self.commit(mail('a2', '2026-10-18T09:00:00+00:00'))
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'waiting', 'waiting_on': 'Sam'}), sid))
            rows = [dict(r) for r in db.execute('SELECT * FROM events WHERE id=?', (answer,))]
            self.assertEqual(store_review.waiting_cards(db, rows)[answer]['card_id'], sid)

    def test_a_draft_answered_from_gmail_closes_with_a_meeting_ahead(self):
        ask, call = self.commit(mail('a1', '2026-10-16T09:00:00+00:00'), meeting('m1', '2026-10-26T09:00:00+00:00'))
        sid = self.store.suggest('work:contract', 'Answer Sam', 'Sam asks.', [ask, call])['id']
        draft = {'kind': 'email', 'label': 'Send', 'account_id': 'work', 'thread_id': 't1', 'to': ['sam@client.example'],
                 'subject': 'Re: Contract', 'body': 'Here it is.', 'revision': 'r1'}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), sid))
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value='2026-10-20T09:00:00+00:00')
        self.clock.start()
        self.commit(mail('a2', '2026-10-19T12:00:00+00:00', sent=True))
        self.assertEqual(self.store.answered_elsewhere(), [sid])

    def test_a_done_to_do_stays_done_for_an_invite_that_came_before(self):
        ask, call = self.commit(mail('a1', '2026-10-16T09:00:00+00:00'), meeting('m1', '2026-10-26T09:00:00+00:00'))
        sid = self.store.suggest('work:contract', 'Answer Sam', 'Sam asks.', [ask])['id']
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value='2026-10-20T09:00:00+00:00')
        self.clock.start()
        self.store.decide(sid, 'complete', '', 'd1', 'dashboard')
        kept = self.store.suggest('work:call', 'Prepare the call', 'Sam asks.', [call], card_id=sid, match=True, reopen=True)
        self.assertNotIn('reopened', kept)

    # a follow-up is about the whole exchange: one moment

    def test_a_follow_up_is_not_handled_by_an_older_message_in_another_thread(self):
        first, _, second = self.commit(mail('a1', '2026-10-15T09:00:00+00:00'), mail('a2', '2026-10-16T09:00:00+00:00', sent=True),
                                       mail('b1', '2026-10-17T09:00:00+00:00', thread='t2', sent=True))
        sid = self.store.suggest('follow-up:1', 'Follow up with Sam', 'No reply.', [second, first])['id']
        with self.store.connect() as db:
            self.assertEqual(follow_ups.thread_news(db, sid), [])
        answer, = self.commit(mail('a3', '2026-10-18T09:00:00+00:00'))
        with self.store.connect() as db:
            self.assertEqual([x['id'] for x in follow_ups.thread_news(db, sid)], [answer])

    # the handled check's answer

    def two_to_dos(self):
        ids = self.commit(mail('a1', '2026-10-15T09:00:00+00:00'), mail('b1', '2026-10-15T10:00:00+00:00', thread='t2', who='bo@other.example', name='Bo Ray'))
        first = self.store.suggest('work:a', 'Answer Sam', 'Sam asks.', ids[:1])['id']
        second = self.store.suggest('work:b', 'Answer Bo', 'Bo asks.', ids[1:])['id']
        self.commit(mail('a2', '2026-10-16T09:00:00+00:00', sent=True), mail('b2', '2026-10-16T10:00:00+00:00', thread='t2', sent=True, who='bo@other.example'))
        return first, second

    def test_a_to_do_the_answer_leaves_out_is_asked_once_more_alone(self):
        first, second = self.two_to_dos()
        app, calls = self.app(), []
        app.handled_check_model = lambda config, text: (calls.append(text), json.dumps([{'todo': first, 'state': 'open'}]))[1]
        app.handled_step()
        self.assertTrue(first in calls[0] and second in calls[0])
        app.handled_step()
        self.assertTrue(first not in calls[1] and second in calls[1])
        app.handled_step()  # left out there too: it waits for a newer message
        self.assertEqual(len(calls), 2)
        self.commit(mail('b3', '2026-10-17T10:00:00+00:00', thread='t2', sent=True, who='bo@other.example'))
        app.handled_step()
        self.assertEqual(len(calls), 3)

    def test_a_reply_that_cant_be_read_leaves_none_out(self):
        self.two_to_dos()
        app = self.app()
        app.handled_check_model = lambda config, text: 'not json'
        app.handled_step()
        self.assertEqual((app.__dict__.get('_handled_left_out'), app.__dict__.get('_handled_judged') or {}), (set(), {}))

    def test_a_turn_that_fails_alone_goes_back_with_the_others(self):
        first, second = self.two_to_dos()
        app, calls = self.app(), []
        app.handled_check_model = lambda config, text: '[]'
        app.handled_step()
        self.assertEqual(app._handled_left_out, {first, second})

        def fails(config, text):
            calls.append(text)
            raise OSError('down')
        app.handled_check_model = fails
        for _ in range(3):
            app.handled_step()
        self.assertEqual([(first in c, second in c) for c in calls[2:]], [(True, True)])
        self.assertEqual(handled_check.CHECKS_PER_TURN, 6)


if __name__ == '__main__':
    unittest.main()

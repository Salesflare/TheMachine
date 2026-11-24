"""Send later (machine/store/send_later.py, machine/app/send_later.py): an approved message waits for the moment the owner
picked, goes once and exactly as approved, and doesn't go when the other side wrote first, when its draft or to-do
changed, when its conversation can't be read, or when its moment passed over an hour ago. No live sends or reads: a fake
outbox, and a fake sync that brings in what a test says."""
import datetime as dt
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import activity_log
import follow_ups
import timeutil
from seams import patch_everywhere  # noqa: E402
from test_follow_ups import FakeOutbox, GMAIL, LINKEDIN
from test_reply_recheck import mail, slack
import machine.app.send_later as app_send_later
import machine.main as machine_main
import machine.sources.gmail as machine_sources_gmail
from machine import kinds
from machine.export import hold as export_hold
from machine.owner_error import OwnerError
from machine.store import send_later
from machine.store.decisions import draft_saved
import sources

DRAFTED = '2026-10-19T09:00:00+00:00'
APPROVED = '2026-10-19T09:05:00+00:00'
LATER = '2026-10-20T07:00:00+00:00'     # a Tuesday, 09:00 in Brussels
HOME = {'id': 'home', 'email': 'owner@home.example', 'service': 'gmail', 'transport': 'gog', 'boundary': 'personal:Home'}
SLACK = {'id': 'slack', 'service': 'slack', 'user_id': 'UOWNER', 'credential': 'x', 'credential_variable': 'X', 'connection_id': 'c'}


def plus(stamp, **kw):
    return (dt.datetime.fromisoformat(stamp) + dt.timedelta(**kw)).isoformat()


class SendLater(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch_everywhere(timeutil, 'now', return_value='2026-10-19T08:00:00+00:00')
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        unread = patch.object(machine_sources_gmail.Gmail, 'get', side_effect=sources.SourceError('offline'))  # never a live read
        unread.start()
        self.addCleanup(unread.stop)
        self.path = Path(self.tmp.name) / 'events.sqlite'
        self.store = machine_main.Store(self.path)
        self.store.commit_page('work', {}, [mail('in1', '2026-10-19T07:50:00+00:00')])
        with self.store.connect() as db:
            self.first = db.execute("SELECT id FROM events WHERE source_id='in1'").fetchone()[0]
        self.sid = self.store.suggest('reply-sam', 'Reply to Sam', 'Answer about the pilot', [self.first])['id']
        with self.store.connect() as db:  # it was shown to the owner, as a notice about it must reach them again
            db.execute("UPDATE deliveries SET status='sent',message_id='1' WHERE suggestion_id=?", (self.sid,))
        self.transport, self.reads, self.on_read = FakeOutbox(), [], {}
        self.accounts = [GMAIL]

        def sync(store, config, account):
            self.reads.append(account['id'])
            then = self.on_read.get(account['id'])
            if isinstance(then, Exception):
                raise then
            if then:
                then()
            return {'mode': 'incremental', 'events': 0}
        fake = patch.object(app_send_later, 'sync_source', sync)
        fake.start()
        self.addCleanup(fake.stop)

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(timeutil, 'now', return_value=stamp)
        self.clock.start()

    def app(self, store=None):
        app = object.__new__(machine_main.App)
        app.store = store or self.store
        app.config = {'accounts': self.accounts, 'digest_at': '08:30'}
        app.model_usage = app.usage_limit = app.fleet = None
        app.teammate_addresses = lambda: []
        return app

    def prepared(self, **extra):
        self.at(DRAFTED)
        draft = {'kind': 'email', 'account_id': 'work', 'from': 'owner@example.com', 'to': ['sam@client.example'], 'subject': 'Re: Pilot',
                 'body': 'Hi Sam, here it is.', 'thread_id': 'T', 'revision': 'r1', **extra}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), self.sid))
            draft_saved(db, self.sid, draft, DRAFTED)
        return draft

    def schedule(self, later=LATER, approval='a1', **args):
        self.at(APPROVED)
        return self.app().confirm_action_action('confirm_action', {'suggestion_id': self.sid, 'revision': 'r1', 'approval_id': approval,
                                                                   'later': later, **args}, owner_dashboard=True)

    def scheduled(self, **extra):
        self.prepared(**extra)
        return self.schedule()

    def act(self, name, at=None, **args):
        if at:
            self.at(at)
        return self.app().send_later_action('send_later_' + name, {'suggestion_id': self.sid, **args}, owner_dashboard=True)

    def run_step(self, at, app=None):
        """One round of the action worker's two steps."""
        self.at(at)
        app = app or self.app()
        app.send_later_step()
        return app.action_step(self.transport)

    def sync(self, at, *events, account='work'):
        self.at(at)
        self.store.commit_page(account, {}, list(events))

    def row(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM scheduled_sends WHERE suggestion_id=? ORDER BY approved_at DESC,rowid DESC', (self.sid,)).fetchone())

    def job(self):
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM action_jobs WHERE suggestion_id=?', (self.sid,)).fetchone()
        return dict(row) if row else None

    def todo(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def delivery(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM deliveries WHERE suggestion_id=?', (self.sid,)).fetchone())

    def lines(self):
        with self.store.connect() as db:
            return [(x['status'], x['detail']) for x in activity_log.page(db, {'accounts': self.accounts}, kind='messages')['items']]

    def assertAsked(self, state, line):
        """It didn't go: the to-do is back with its draft and the reason, and the notice goes out once."""
        self.assertEqual(self.transport.sent, [])
        self.assertEqual((self.row()['state'], self.job()['status'], self.job()['error']), (state, 'blocked', line))
        self.assertEqual((self.todo()['status'], self.todo()['snoozed_until']), ('prepared', None))
        self.assertEqual((self.delivery()['status'], self.delivery()['reminder']), ('queued', 1))

    # ------------------------------------------------------------------ the plain path

    def test_it_waits_under_later_and_goes_once_as_approved(self):
        self.prepared()
        self.assertEqual(self.schedule(), {'status': 'scheduled', 'send_at': LATER})
        self.assertEqual((self.todo()['status'], self.todo()['snoozed_until']), ('snoozed', LATER))
        self.assertIsNone(self.job())  # nothing the outbox could send
        self.run_step(plus(LATER, minutes=-1))
        self.assertEqual((self.transport.sent, self.reads), ([], []))  # and nothing is read before its time
        seen = []
        send, self.transport.send = self.transport.send, lambda action, job: seen.append(action) or send(action, job)
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual([a['body'] for a in seen], ['Hi Sam, here it is.'])
        self.assertEqual((seen[0]['to'], seen[0]['subject'], self.reads), (['sam@client.example'], 'Re: Pilot', ['work']))
        self.run_step(plus(LATER, seconds=8))
        self.assertEqual((len(self.transport.sent), self.job()['status']), (1, 'sent'))
        self.assertEqual([s for s, _ in self.lines()], ['Sent', 'Scheduled'])

    def test_the_clock_that_wakes_snoozes_leaves_it_alone(self):
        self.scheduled()
        self.at(plus(LATER, minutes=5))
        self.store.wake_snoozed()
        self.assertEqual((self.todo()['status'], self.row()['state']), ('snoozed', 'waiting'))

    def test_the_same_tap_twice_schedules_once(self):
        self.prepared()
        self.schedule()
        self.assertTrue(self.schedule().get('duplicate'))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM scheduled_sends').fetchone()[0], 1)

    def test_several_drafts_for_one_moment_all_go(self):
        self.prepared()
        second = {'kind': 'email', 'account_id': 'work', 'from': 'owner@example.com', 'to': ['kim@client.example'], 'subject': 'Pilot', 'body': 'Hi Kim.', 'revision': 'r2'}
        with self.store.connect() as db:
            first = json.loads(db.execute('SELECT next_action FROM suggestions WHERE id=?', (self.sid,)).fetchone()[0])
            db.execute('UPDATE suggestions SET next_action=? WHERE id=?', (json.dumps({'kind': 'menu', 'revision': 'm', 'actions': [first, second]}), self.sid))
        self.schedule()
        self.schedule(approval='a2', revision='r2')
        self.assertEqual(self.view()['n'], 2)
        self.run_step(plus(LATER, seconds=2))
        self.run_step(plus(LATER, seconds=5))
        self.assertEqual(len(self.transport.sent), 2)

    def view(self):
        with self.store.connect() as db:
            return send_later.view(db, self.sid)

    # ------------------------------------------------------------------ someone wrote first

    def test_a_reply_takes_it_back_as_soon_as_it_is_collected(self):
        self.scheduled()
        self.sync('2026-10-19T15:00:00+00:00', mail('in2', '2026-10-19T14:59:00+00:00'))
        self.run_step('2026-10-19T15:00:03+00:00')
        self.assertAsked('taken_back', 'Not sent: Sam Rivera wrote first.')
        self.assertEqual(self.lines(), [('Blocked', 'Not sent: Sam Rivera wrote first.'), ('Scheduled', self.lines()[1][1])])
        with self.store.connect() as db:
            self.assertEqual(follow_ups.held_message(db, self.job()['id'])['snippet'], 'About the pilot: in2')
        self.run_step(plus(LATER, seconds=2))  # its old time comes: nothing
        self.assertEqual(self.transport.sent, [])

    def test_a_new_send_after_it_was_taken_back_goes(self):
        self.test_a_reply_takes_it_back_as_soon_as_it_is_collected()
        self.at(plus(LATER, minutes=1))
        self.app().confirm_action_action('confirm_action', {'suggestion_id': self.sid, 'revision': 'r1', 'approval_id': 'a9'}, owner_dashboard=True)
        self.run_step(plus(LATER, hours=5))  # no longer a scheduled one: no bound, no fresh read
        self.assertEqual((len(self.transport.sent), self.reads), (1, []))

    def test_a_reply_that_comes_in_with_the_read_right_before_it_goes(self):
        self.scheduled()
        stamp = plus(LATER, seconds=2)
        self.on_read['work'] = lambda: self.store.commit_page('work', {}, [mail('in2', plus(LATER, seconds=1))])
        self.run_step(stamp)
        self.assertAsked('taken_back', 'Not sent: Sam Rivera wrote first.')

    def test_a_reply_collected_between_that_read_and_the_send(self):
        self.scheduled()
        app, check = self.app(), machine_main.App.send_later_check

        def then_a_reply(row):
            news = check(app, row)
            self.store.commit_page('work', {}, [mail('in2', plus(LATER, seconds=1))])
            return news
        app.send_later_check = then_a_reply
        self.run_step(plus(LATER, seconds=2), app)
        self.assertAsked('taken_back', 'Not sent: Sam Rivera wrote first.')

    def test_mail_from_another_address_of_theirs_to_another_mailbox(self):
        self.accounts = [GMAIL, HOME]
        self.scheduled()
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('p:sam','person','Sam Rivera',1,1,?)",
                       (json.dumps({'identifiers': ['email:sam@client.example', 'email:sam@private.example']}),))
        self.on_read['home'] = lambda: self.store.commit_page('home', {}, [{**mail('h1', plus(LATER, seconds=1), who='Sam <Sam@private.example>', thread='OTHER'), 'account_id': 'home'}])
        self.run_step(plus(LATER, seconds=2))
        self.assertAsked('taken_back', 'Not sent: Sam wrote first.')

    def test_someone_else_in_the_thread_counts_and_a_stranger_elsewhere_does_not(self):
        self.scheduled()
        self.sync('2026-10-19T15:00:00+00:00', mail('x1', '2026-10-19T14:59:00+00:00', who='Lee <lee@client.example>', thread='OTHER'))
        self.run_step('2026-10-19T15:00:03+00:00')
        self.assertEqual(self.row()['state'], 'waiting')
        self.sync('2026-10-19T16:00:00+00:00', mail('x2', '2026-10-19T15:59:00+00:00', who='Lee <lee@client.example>'))
        self.run_step('2026-10-19T16:00:03+00:00')
        self.assertAsked('taken_back', 'Not sent: Lee wrote first.')

    def test_an_automatic_reply_and_the_owners_own_mail_do_not(self):
        self.scheduled()
        self.sync('2026-10-19T15:00:00+00:00', mail('ooo', '2026-10-19T14:59:00+00:00', auto_submitted=True, precedence='bulk'),
                  mail('own', '2026-10-19T14:59:30+00:00', mine=True))
        self.run_step('2026-10-19T15:00:03+00:00')
        self.assertEqual(self.row()['state'], 'waiting')
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual(len(self.transport.sent), 1)

    def test_a_forward_and_a_reply_through_a_list_count(self):
        for meta in ({'thread': 'OTHER'}, {'precedence': 'list', 'in-reply-to': '<x@mail.example>'}):
            with self.subTest(meta=meta):
                self.doCleanups()  # this one's own, before the next one's setUp
                self.setUp()
                self.scheduled()
                event = mail('f1', '2026-10-19T14:59:00+00:00', **meta)
                self.sync('2026-10-19T15:00:00+00:00', {**event, 'title': 'Fwd: Pilot'})
                self.run_step('2026-10-19T15:00:03+00:00')
                self.assertAsked('taken_back', 'Not sent: Sam Rivera wrote first.')

    def test_the_chat_its_to_do_came_from_is_watched_too(self):
        chat = {'account_id': 'wa', 'source_id': 'w1', 'kind': 'whatsapp.message', 'occurred_at': '2026-10-19T07:55:00+00:00', 'title': 'Sam', 'body': 'Mail me?',
                'deleted': False, 'metadata': {'chat_id': 'C1', 'from': 'Sam', 'from_me': False}}
        self.store.commit_page('wa', {}, [chat])
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='w1'").fetchone()[0]
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([self.first, event]), self.sid))
        self.scheduled()
        self.sync('2026-10-19T15:00:00+00:00', {**chat, 'source_id': 'w2', 'occurred_at': '2026-10-19T14:59:00+00:00', 'body': 'Never mind'}, account='wa')
        self.run_step('2026-10-19T15:00:03+00:00')
        self.assertAsked('taken_back', 'Not sent: Sam wrote first.')

    def test_slack_is_read_directly(self):
        self.accounts = [GMAIL, SLACK]
        self.prepared(kind='slack', account_id='slack', user_id='USAM', to_name='Sam Rivera', thread_id=None, **{'from': None})
        self.schedule()
        calls, messages = [], [{'ts': f'{dt.datetime.fromisoformat(APPROVED).timestamp() + 60:.6f}', 'user': 'UOWNER', 'text': 'mine'}]

        class Reader:
            def person(self, action):
                return 'USAM'

            def channel(self, action, user):
                return 'D1'

            def call(self, action, method, params):
                calls.append((method, params['channel']))
                return {'ok': True, 'messages': messages}
        app = self.app()
        app.slack_reader = Reader
        self.run_step(plus(LATER, seconds=2), app)
        self.assertEqual((len(self.transport.sent), calls), (1, [('conversations.history', 'D1')]))

    def test_slack_reply_in_the_direct_message(self):
        self.accounts = [GMAIL, SLACK]
        self.prepared(kind='slack', account_id='slack', user_id='USAM', to_name='Sam Rivera', thread_id=None, **{'from': None})
        self.schedule()
        self.sync('2026-10-19T15:00:00+00:00', slack('s1', '2026-10-19T14:59:00+00:00', 'USAM', '1792421940.000100'), account='slack')
        self.run_step('2026-10-19T15:00:03+00:00')
        self.assertEqual((self.row()['state'], self.transport.sent), ('taken_back', []))

    # ------------------------------------------------------------------ it can't be read, or its time passed

    def test_unreadable_mail_waits_and_says_so_then_goes(self):
        self.scheduled()
        self.on_read['work'] = sources.SourceError('signed_out')
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.transport.sent, self.job()['status'], self.view()['unread']), ([], 'queued', True))
        self.run_step(plus(LATER, seconds=30))  # not before its next try
        self.assertEqual(self.reads, ['work'])
        del self.on_read['work']
        self.run_step(plus(LATER, minutes=3))
        self.assertEqual((len(self.transport.sent), self.view()), (1, None))

    def test_unreadable_for_an_hour_asks(self):
        self.scheduled()
        self.on_read['work'] = sources.SourceError('signed_out')
        for minutes in (0, 20, 40, 59):
            self.run_step(plus(LATER, minutes=minutes, seconds=2))
        self.run_step(plus(LATER, minutes=61, seconds=2))
        self.assertAsked('unread', 'Not sent: couldn’t check for a new message first.')

    def test_a_mailbox_not_caught_up_is_not_read(self):
        self.scheduled()
        with patch.object(app_send_later, 'sync_source', lambda store, config, account: {'mode': 'bootstrap'}):
            self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.transport.sent, self.view()['unread']), ([], True))

    def test_up_to_an_hour_late_it_goes(self):
        self.scheduled()
        self.run_step(plus(LATER, minutes=59))
        self.assertEqual(len(self.transport.sent), 1)

    def test_over_an_hour_late_it_asks(self):
        self.scheduled()
        self.run_step(plus(LATER, minutes=60, seconds=1))
        self.assertAsked('late', 'Not sent: it was more than an hour late.')
        self.assertEqual(self.reads, [])

    def test_queued_then_off_for_hours_asks(self):
        self.scheduled()
        self.at(plus(LATER, seconds=2))
        self.app().send_later_step()  # it joined the outbox, then the computer went to sleep
        self.assertEqual(self.job()['status'], 'queued')
        self.run_step(plus(LATER, hours=4))
        self.assertAsked('late', 'Not sent: it was more than an hour late.')

    def test_a_restart_between_the_pick_and_the_send(self):
        self.scheduled()
        again = machine_main.Store(self.path)
        self.run_step(plus(LATER, seconds=2), self.app(again))
        self.assertEqual(len(self.transport.sent), 1)

    def test_a_restart_in_the_middle_of_the_send_never_sends_again(self):
        self.scheduled()
        self.transport.die = True
        with self.assertRaises(KeyboardInterrupt):
            self.run_step(plus(LATER, seconds=2))
        self.transport.die = False
        self.run_step(plus(LATER, minutes=5), self.app(machine_main.Store(self.path)))
        self.assertEqual((self.transport.attempts, self.transport.sent, self.job()['status']), ({self.sid: 1}, [], 'uncertain'))

    def test_a_failed_send_is_told(self):
        self.scheduled()
        self.transport.refuse.add(self.sid)
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.job()['status'], self.delivery()['status'], self.delivery()['reminder']), ('failed', 'queued', 1))

    def test_a_check_that_stops_it_is_told(self):
        self.scheduled()
        self.transport.preflight = lambda action: (_ for _ in ()).throw(OwnerError('An attachment changed after you reviewed it. Nothing was sent.'))
        self.run_step(plus(LATER, seconds=2))
        self.assertAsked('stopped', 'An attachment changed after you reviewed it. Nothing was sent.')

    # ------------------------------------------------------------------ only what was approved

    def test_anything_that_moves_the_to_do_ends_it(self):
        for choice, extra, status in (('complete', {}, 'completed'), ('reject', {}, 'rejected'), ('accept', {}, 'prepared'),
                                      ('snooze', {'snoozed_until': '2026-10-22T07:00:00+00:00'}, 'snoozed')):
            with self.subTest(choice=choice):
                self.doCleanups()  # this one's own, before the next one's setUp
                self.setUp()
                self.scheduled()
                self.at('2026-10-19T12:00:00+00:00')
                self.store.decide(self.sid, choice, '', 'd-' + choice, 'dashboard', **extra)
                self.run_step(plus(LATER, seconds=2))
                self.assertEqual((self.row()['state'], self.transport.sent, self.job()), ('canceled', [], None))
                self.assertEqual(self.todo()['status'], status)
                self.assertEqual(self.lines()[0][0], 'Canceled')

    def test_snoozed_away_and_back_to_the_same_time_still_ends_it(self):
        self.scheduled()
        with self.store.connect() as db:
            send_later.sweep(db, APPROVED)
        self.assertEqual(self.row()['state'], 'waiting')
        self.at('2026-10-19T12:00:00+00:00')
        self.store.decide(self.sid, 'complete', '', 'd1', 'dashboard')
        self.app().send_later_step()
        self.store.decide(self.sid, 'undo', '', 'd2', 'dashboard')
        self.assertEqual((self.todo()['status'], self.todo()['snoozed_until']), ('snoozed', LATER))
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.row()['state'], self.transport.sent), ('canceled', []))
        self.at(plus(LATER, minutes=1))
        self.store.wake_snoozed()
        self.assertEqual(self.todo()['status'], 'prepared')  # back for a new approval

    def test_another_draft_waits_for_a_new_approval(self):
        self.scheduled()
        with self.store.connect() as db:
            draft = json.loads(db.execute('SELECT next_action FROM suggestions WHERE id=?', (self.sid,)).fetchone()[0])
            db.execute('UPDATE suggestions SET next_action=? WHERE id=?', (json.dumps({**draft, 'body': 'Hi Sam, other words.', 'revision': 'r2'}), self.sid))
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.row()['state'], self.transport.sent, self.todo()['status']), ('changed', [], 'prepared'))
        self.assertEqual(self.delivery()['reminder'], 1)

    def test_can_do_things_turned_off_since(self):
        self.scheduled()
        with patch('abilities.refuse', return_value='Can do things is off for it. Turn it on under Connections first.'):
            self.run_step(plus(LATER, seconds=2))
        self.assertAsked('stopped', 'Can do things is off for it. Turn it on under Connections first.')

    # ------------------------------------------------------------------ two workers, and Cancel

    def test_two_workers_queue_it_once(self):
        self.scheduled()
        self.at(plus(LATER, seconds=2))
        with self.store.connect() as db:
            stale = send_later.waiting(db, self.sid)
            send_later.release(db, stale, plus(LATER, seconds=2))
        with self.store.connect() as db:
            send_later.release(db, stale, plus(LATER, seconds=2))  # the other worker, with what it read before
            self.assertEqual(db.execute('SELECT COUNT(*) FROM action_jobs').fetchone()[0], 1)

    def test_two_workers_send_it_once(self):
        self.scheduled()
        self.at(plus(LATER, seconds=2))
        self.app().send_later_step()
        both, app = threading.Barrier(2, timeout=20), self.app()
        check = machine_main.App.send_later_check

        def together(row):
            news = check(app, row)
            both.wait()  # both read it, both found nothing
            return news
        app.send_later_check = together
        threads = [threading.Thread(target=app.action_step, args=(self.transport,)) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(30)
        self.assertEqual(len(self.transport.sent), 1)

    def test_cancel_before_its_time(self):
        self.scheduled()
        self.assertEqual(self.act('cancel', '2026-10-19T12:00:00+00:00'), {'status': 'canceled'})
        self.assertEqual(self.todo()['status'], 'prepared')
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.transport.sent, [s for s, _ in self.lines()]), ([], ['Canceled', 'Scheduled']))

    def test_cancel_while_it_is_being_checked(self):
        self.scheduled()
        self.on_read['work'] = lambda: self.act('cancel')
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((self.transport.sent, self.job()['status'], self.row()['state']), ([], 'cancelled', 'canceled'))

    def test_cancel_while_it_is_sending_says_it_is_too_late(self):
        self.scheduled()
        said, send = [], self.transport.send

        def meanwhile(action, job):
            for name in ('cancel', 'now'):
                try:
                    self.act(name)
                except OwnerError as error:
                    said.append(str(error))
            return send(action, job)
        self.transport.send = meanwhile
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((said, len(self.transport.sent), self.job()['status']), (['It’s already on its way.'] * 2, 1, 'sent'))

    def test_cancel_twice(self):
        self.scheduled()
        self.act('cancel')
        with self.assertRaisesRegex(OwnerError, 'scheduled anymore'):
            self.act('cancel')

    # ------------------------------------------------------------------ Send now and Change time

    def test_send_now(self):
        self.scheduled()
        self.act('now', '2026-10-19T12:00:00+00:00')
        self.run_step('2026-10-19T12:00:03+00:00')
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual((len(self.transport.sent), self.reads, self.row()['state']), (1, [], 'now'))

    def test_send_now_while_its_mail_cant_be_read(self):
        self.scheduled()
        self.on_read['work'] = sources.SourceError('signed_out')
        self.run_step(plus(LATER, seconds=2))
        self.act('now')
        self.run_step(plus(LATER, seconds=4))
        self.assertEqual(len(self.transport.sent), 1)

    def test_change_time(self):
        self.scheduled()
        to = '2026-10-21T07:00:00+00:00'
        self.act('move', '2026-10-19T12:00:00+00:00', later='2026-10-21T09:00:00+02:00')
        self.assertEqual((self.row()['send_at'], self.todo()['snoozed_until'], self.row()['approved_at']), (to, to, APPROVED))
        self.run_step(plus(LATER, seconds=2))
        self.assertEqual(self.transport.sent, [])
        self.run_step(plus(to, seconds=2))
        self.assertEqual((len(self.transport.sent), [s for s, _ in self.lines()]), (1, ['Sent', 'Time changed', 'Scheduled']))

    def test_a_time_that_passed_or_lies_over_a_year_away(self):
        self.prepared()
        for later in ('2026-10-19T09:04:00+00:00', '2028-01-01T09:00:00+00:00', '2026-10-21T09:00:00', 'soon'):
            with self.subTest(later=later), self.assertRaises(OwnerError):
                self.schedule(later)
        self.assertEqual(self.todo()['status'], 'prepared')

    def test_the_clock_change(self):
        """The moment is an instant. Over the end of summer time (25 October, 01:00 UTC) 09:00 in Brussels is 08:00 UTC, and
        the two 02:30s of that night are two different moments: it goes at the one that was picked."""
        for picked, instant in (('2026-10-25T09:00:00+01:00', '2026-10-25T08:00:00+00:00'),
                                ('2026-10-25T02:30:00+02:00', '2026-10-25T00:30:00+00:00'), ('2026-10-25T02:30:00+01:00', '2026-10-25T01:30:00+00:00')):
            with self.subTest(picked=picked):
                self.doCleanups()  # this one's own, before the next one's setUp
                self.setUp()
                self.prepared()
                self.assertEqual(self.schedule(picked)['send_at'], instant)
                self.run_step(plus(instant, seconds=-5))
                self.assertEqual(self.transport.sent, [])
                self.run_step(plus(instant, seconds=2))
                self.assertEqual(len(self.transport.sent), 1)

    # ------------------------------------------------------------------ who and what

    def test_only_the_owners_dashboard_schedules(self):
        self.prepared()
        self.at(APPROVED)
        args = {'suggestion_id': self.sid, 'revision': 'r1', 'approval_id': 'telegram:1', 'later': LATER}
        with self.assertRaises(OwnerError):
            self.app().confirm_action_action('confirm_action', args)
        self.assertIsNone(self.job())  # refused, not sent at once
        for name in ('move', 'cancel', 'now'):
            with self.assertRaises(OwnerError):
                self.app().send_later_action('send_later_' + name, {'suggestion_id': self.sid, 'later': LATER})

    def test_what_can_wait_is_what_can_be_read_first(self):
        # Every message to a person waits, unless the read before it goes would need the shared browser; a doc's never
        browser = {'linkedin', 'x'}
        self.assertEqual(set(send_later.CHANNELS), {*kinds.TO_PERSON, 'email_demo'} - browser)
        # Each of them comes in on services whose account can be read now; Slack's reads the conversation instead
        for send in set(kinds.SEND_LATER) - {'slack'}:
            came_in = {kinds.KINDS[k]['service'] for k in kinds.of(send=send)} - {'salesflare'}  # a CRM's copy isn't the mailbox
            self.assertTrue(came_in and came_in <= set(app_send_later.READABLE), send)
        # And nothing else is read for it: all mail, and the services of those messages
        replies = {kinds.KINDS[k]['service'] for send in kinds.SEND_LATER for k in kinds.of(send=send)}
        self.assertEqual(set(app_send_later.READABLE), {*sources.MAIL_SERVICES, *replies} - {'slack', 'salesflare'})

    def test_linkedin_is_left_out(self):
        self.accounts = [GMAIL, LINKEDIN]
        self.prepared(kind='linkedin', account_id='li', to_name='Sam', conversation_id='c1')
        with self.assertRaisesRegex(OwnerError, 'sent later'):
            self.schedule()

    def test_after_a_move_to_another_computer_it_asks(self):
        self.scheduled()
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        with db:
            export_hold.hold(db, '2026-10-19T12:00:00+00:00', '2026-10-19T11:00:00+00:00')
        db.close()
        self.run_step(plus(LATER, seconds=2))
        self.assertAsked('stopped', export_hold.MOVED_SEND)


if __name__ == '__main__':
    unittest.main()

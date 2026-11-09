"""LinkedIn and X history: 90 days back by default, read very slowly through the owner's own browser (connectors'
HISTORY_PACE, machine/app/history.py). Every read is faked: no browser, no network, no model; names are made up."""
import datetime as dt
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_history_social', Path(__file__).parent.parent / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.app import history as app_history  # noqa: E402
from machine.sources.connectors import CONNECTOR_HELPERS, load_connector  # noqa: E402
from machine.store import history  # noqa: E402
from sources import SourceError  # noqa: E402

linkedin, x = load_connector('linkedin'), load_connector('x')
NOW = '2026-11-06T09:00:00+00:00'  # 10:00 in Amsterdam (the tests' local time): inside waking hours
LI = {'id': 'li', 'service': 'linkedin', 'transport': 'linkedin-inbox', 'boundary': 'work:Example'}
XA = {'id': 'xa', 'service': 'x', 'transport': 'x-inbox', 'boundary': 'work:Example', 'handle': 'sample_owner'}
MAIL = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}


def ms(text):
    return int(dt.datetime.fromisoformat(text).timestamp() * 1000)


def li_message(n, at, who='Robin Sample'):
    return {'urn': f'urn:li:msg_message:(x,{n})', 'conversation': 'urn:li:msg_conversation:(x,c1)', 'at': ms(at),
            'fromMe': False, 'from': who, 'with': who, 'text': f'Message {n}'}


class FakeLinkedIn:
    """The reader's `history` answers in turn: each a dict, or an exception to raise."""
    answers, calls = [], []

    def __init__(self, config, account, helpers):
        pass

    def history(self, since_ms, until_ms, state):
        FakeLinkedIn.calls.append((since_ms, until_ms, dict(state)))
        answer = FakeLinkedIn.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer


class Base(unittest.TestCase):
    accounts = [LI]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.clock = [NOW]
        clock = patch_everywhere(a, 'now', side_effect=lambda: self.clock[0]); clock.start(); self.addCleanup(clock.stop)
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': list(self.accounts), 'database': str(self.store.path)}
        self.app.collector_resting = {acc['id'] for acc in self.accounts}
        FakeLinkedIn.answers, FakeLinkedIn.calls = [], []
        with self.store.connect() as db:
            db.executemany('INSERT INTO milestones(name,at) VALUES(?,?)', [('first_import:' + acc['id'], NOW) for acc in self.accounts])
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", (NOW,))
        for p in (mock.patch.object(app_history, 'free_disk', return_value=True), mock.patch.object(app_history, 'free_memory', return_value=True),
                  mock.patch.object(linkedin, 'Source', FakeLinkedIn)):
            p.start(); self.addCleanup(p.stop)

    def later(self, **delta):
        self.clock[0] = (dt.datetime.fromisoformat(self.clock[0]) + dt.timedelta(**delta)).isoformat()

    def state(self, account='li'):
        with self.store.connect() as db:
            return (history.get(db, account) or {}).get('state') or {}

    def page(self, messages=(), done=False):
        return {'messages': list(messages), 'state': {'cursor': 'next'}, 'done': done}


class Depth(Base):
    def test_own_depth_90_days_and_0_turns_it_off(self):
        self.assertEqual(history.depth({}, LI), 90)
        self.assertEqual(history.depth({}, XA), 90)
        self.assertEqual(history.depth({'history_days': 0}, LI), 90)  # mail's setting leaves these alone
        self.assertEqual(history.depth({'social_history_days': 0}, LI), 0)
        self.assertEqual(history.depth({'social_history_days': 10 ** 6}, XA), history.SOCIAL_MAX_DAYS)
        self.assertEqual(history.depth({'social_history_days': 0}, MAIL), 365)
        self.app.config['social_history_days'] = 0
        self.assertFalse(self.app.history_step())
        self.assertEqual(self.app.history_why, 'off')
        self.assertEqual(FakeLinkedIn.calls, [])

    def test_walk_reaches_back_90_days_from_where_the_live_sync_starts(self):
        FakeLinkedIn.answers = [self.page()]
        self.assertTrue(self.app.history_step())
        since, until, _ = FakeLinkedIn.calls[0]
        self.assertEqual(since, ms('2026-08-08T09:00:00+00:00'))
        self.assertEqual(until, ms('2026-10-29T09:00:00+00:00'))  # the live sync's week, a day apart


class BothLanes(Base):
    def test_slack_and_teams_keep_history_days_and_a_finished_walk_stays_done(self):
        for service in ('slack', 'teams', 'gmail'):
            self.assertEqual(history.depth({'history_days': 200, 'social_history_days': 30}, {'service': service}), 200)
        self.assertEqual(history.depth({'history_days': 200, 'social_history_days': 30}, LI), 30)
        self.assertIsNone(app_history.connector_pace({'service': 'teams'}))  # Teams keeps its own lane
        FakeLinkedIn.answers = [self.page(done=True)]
        self.assertTrue(self.app.history_step())
        self.later(hours=3)
        self.assertFalse(self.app.history_step())  # never reopened like an older Teams walk (no channels here)
        self.assertEqual(len(FakeLinkedIn.calls), 1)


class Walk(Base):
    def test_history_only_resumable_and_paced(self):
        FakeLinkedIn.answers = [self.page([li_message(1, '2026-10-01T10:00:00+00:00'), li_message(2, '2026-11-05T10:00:00+00:00'),
                                           li_message(3, '2026-01-01T10:00:00+00:00')])]
        self.assertTrue(self.app.history_step())
        with self.store.connect() as db:
            rows = db.execute('SELECT body,history,version,analyzed_version FROM events').fetchall()
        self.assertEqual([tuple(r) for r in rows], [('Message 1', 1, 1, 1)])  # reviewed history; this week and too old left out
        state = self.state()
        self.assertEqual(state['page'], {'cursor': 'next'})  # the reader's cursor, for the next step
        pause = dt.datetime.fromisoformat(state['next_at']) - dt.datetime.fromisoformat(NOW)
        self.assertTrue(dt.timedelta(minutes=8) <= pause <= dt.timedelta(minutes=20), pause)
        self.assertEqual(state['steps'], 1)
        self.later(minutes=7)
        self.assertFalse(self.app.history_step())  # still in its pause
        self.assertEqual(self.app.history_why, 'pace')
        self.later(minutes=14)
        FakeLinkedIn.answers = [self.page(done=True)]
        self.assertTrue(self.app.history_step())
        self.assertEqual(FakeLinkedIn.calls[-1][2], {'cursor': 'next'})  # went on from the saved cursor
        with self.store.connect() as db:
            self.assertTrue(history.get(db, 'li')['done_at'])
        self.later(hours=2)
        self.assertFalse(self.app.history_step())  # done: no more reads
        self.assertEqual(len(FakeLinkedIn.calls), 2)

    def test_pauses_are_jittered(self):
        pace, current = linkedin.HISTORY_PACE, dt.datetime.fromisoformat(NOW)
        pauses = set()
        for _ in range(20):
            state = {}
            app_history.pace_after(pace, state, current)
            pauses.add(state['next_at'])
        self.assertGreater(len(pauses), 10)


class Cap(Base):
    def test_daily_cap_then_the_next_morning(self):
        cap = linkedin.HISTORY_PACE['steps_per_day']
        self.assertLessEqual(cap, 24)
        steps = 0
        for _ in range(cap + 3):  # 10:00 to about 19:40 local, a step every 21 minutes when it may
            FakeLinkedIn.answers = [self.page()]
            steps += bool(self.app.history_step())
            self.later(minutes=21)
        self.assertEqual(steps, cap)
        self.assertEqual(self.app.history_why, 'pace')
        self.assertEqual(app_history.pace_wait(linkedin.HISTORY_PACE, LI, self.state(), dt.datetime.fromisoformat(self.clock[0])), 'cap')
        self.assertEqual(len(FakeLinkedIn.calls), cap)
        self.clock[0] = '2026-11-07T09:00:00+00:00'  # the next day, 10:00 local
        FakeLinkedIn.answers = [self.page()]
        self.assertTrue(self.app.history_step())
        self.assertEqual(self.state()['steps'], 1)


class WakingHours(Base):
    def test_only_in_waking_hours(self):
        wait = lambda at, account=LI: app_history.pace_wait(linkedin.HISTORY_PACE, account, {}, dt.datetime.fromisoformat(at), linkedin.READ_HOURS)
        self.assertEqual(wait('2026-11-06T05:30:00+00:00'), 'hours')  # 06:30 in Amsterdam
        self.assertEqual(wait('2026-11-06T21:30:00+00:00'), 'hours')  # 22:30
        self.assertIsNone(wait('2026-11-06T08:00:00+00:00'))  # 09:00
        self.assertEqual(wait('2026-11-06T08:00:00+00:00', {**LI, 'active_hours': [11, 18]}), 'hours')  # narrower own hours
        self.clock[0] = '2026-11-06T02:00:00+00:00'
        FakeLinkedIn.answers = [self.page()]
        self.assertFalse(self.app.history_step())
        self.assertEqual(FakeLinkedIn.calls, [])


class StopOnChallenge(Base):
    accounts = [LI, MAIL]

    def test_a_challenge_stops_it_for_a_day_and_rests_nothing_else(self):
        FakeLinkedIn.answers = [SourceError('linkedin_read_failed', retry_after=900)]  # a security check, a captcha, an odd page
        with mock.patch.object(self.app, 'history_mail', return_value=(0, None, False)) as mail:
            self.assertFalse(self.app.history_step())
            self.assertEqual(self.app.history_rested, 0.0)  # mail history isn't held back by it
            state = self.state()
            self.assertEqual(state['stopped_until'], '2026-11-07T09:00:00+00:00')
            self.later(minutes=1)
            self.assertTrue(self.app.history_step())
            self.assertEqual(mail.call_count, 1)  # the step went to mail
            self.later(hours=22)
            FakeLinkedIn.answers = [self.page()]
            self.app.history_step()
            self.assertEqual(len(FakeLinkedIn.calls), 1)  # still stopped
            self.clock[0] = '2026-11-07T09:30:00+00:00'
            self.app.history_step()
            self.assertEqual(len(FakeLinkedIn.calls), 2)  # a day later, once

    def test_429_stops_for_a_day_too(self):
        FakeLinkedIn.answers = [SourceError('linkedin_query_failed', 429)]
        self.app.history_step()
        self.assertEqual(self.state()['stopped_until'], '2026-11-07T09:00:00+00:00')

    def test_a_busy_browser_is_only_a_pause(self):
        FakeLinkedIn.answers = [SourceError('linkedin_browser_busy', retry_after=600)]
        self.app.history_step()
        self.assertNotIn('stopped_until', self.state())
        self.assertGreater(self.state()['next_at'], NOW)


class LiveSyncFirst(Base):
    def test_never_while_its_live_sync_fails(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO checkpoints(account_id,state,error,error_at,failures) VALUES('li','{}','linkedin_read_failed',?,1)", (NOW,))
        FakeLinkedIn.answers = [self.page()]
        self.assertFalse(self.app.history_step())
        self.assertEqual(self.app.history_why, 'live_error')
        self.assertEqual(FakeLinkedIn.calls, [])

    def test_never_during_its_own_read_or_before_its_first_import(self):
        self.app.collector_resting = set()
        self.assertFalse(self.app.history_step())
        self.assertEqual(self.app.history_why, 'sync')
        self.app.collector_resting = {'li'}
        with self.store.connect() as db:
            db.execute("DELETE FROM milestones WHERE name='first_import:li'")
        self.assertFalse(self.app.history_step())
        self.assertEqual(FakeLinkedIn.calls, [])


class Pages(unittest.TestCase):
    """The connectors' history_page over a faked reader answer: only the window, as history events."""
    upper, target = '2026-10-29T09:00:00+00:00', '2026-08-08T09:00:00+00:00'

    def test_linkedin_page(self):
        source = mock.Mock(); source.history.return_value = {'messages': [li_message(1, '2026-09-01T10:00:00+00:00'),
                                                                          li_message(2, '2026-11-01T10:00:00+00:00')],
                                                             'state': {'queue': []}, 'done': True}
        state = {}
        events, done = linkedin.history_page({}, LI, CONNECTOR_HELPERS, state, self.upper, self.target, source)
        self.assertEqual([e['body'] for e in events], ['Message 1'])
        self.assertTrue(done)
        self.assertEqual(state['page'], {'queue': []})
        source.history.assert_called_once_with(ms(self.target), ms(self.upper), {})

    def test_x_page(self):
        source = mock.Mock(); source.history.return_value = {
            'mentions': [{'id': '11', 'at': ms('2026-09-02T10:00:00+00:00'), 'text': 'Hi @sample_owner',
                          'author': {'id': '22', 'name': 'Kim Example', 'screen_name': 'kim_example'}}],
            'dms': [{'id': '33', 'at': ms('2026-09-03T10:00:00+00:00'), 'from_me': True, 'from': {'id': '1'}, 'with': 'Kim Example',
                     'conversation_id': '1-22', 'text': 'Thanks'},
                    {'id': '34', 'at': ms('2026-11-02T10:00:00+00:00'), 'from_me': False, 'from': {'id': '22'}, 'with': 'Kim Example',
                     'conversation_id': '1-22', 'text': 'This week'}],
            'state': {'phase': 'dms', 'queue': []}, 'done': False}
        state = {}
        events, done = x.history_page({}, XA, CONNECTOR_HELPERS, state, self.upper, self.target, source)
        self.assertEqual(sorted((e['kind'], e['body']) for e in events), [('x.dm', 'Thanks'), ('x.mention', 'Hi @sample_owner')])
        self.assertFalse(done)
        self.assertEqual(state['page']['phase'], 'dms')

    def test_reader_answer_checked(self):
        helpers = CONNECTOR_HELPERS
        source = x.Source({}, XA, helpers)
        with mock.patch.object(x.Source, 'read', return_value={'mentions': [], 'dms': [], 'state': {}}):
            with self.assertRaises(SourceError):
                source.history(0, 1, {})  # no `done`: an odd answer
        li = linkedin.Source({}, LI, helpers)
        with mock.patch.object(linkedin.Source, 'run', return_value={'messages': [], 'state': {}}):
            with self.assertRaises(SourceError):
                li.history(0, 1, {})


if __name__ == '__main__':
    unittest.main()

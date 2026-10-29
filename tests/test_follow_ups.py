"""Automated follow-ups on boards and projects (follow_ups.py): the schedule (shortest and longest wait, at least and at
most, per stage), stop conditions, channel choice and switching, asking vs sending without asking, Careful, usage
priority, one grouped to-do per board, ending a round without a reply, and never sending twice. No live sends: the
outbox is only queued here."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import follow_ups
import graph
import model_budget
import test_ux as ux
a = ux.a

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
LINKEDIN = {'id': 'li', 'service': 'linkedin', 'transport': 'browser', 'boundary': 'work:Example'}
NOW = '2026-10-19T09:00:00+00:00'  # a Monday, 11:00 in Brussels


def msg(source_id, at, mine=False, who='sam@client.example', thread='t1', title='Pilot'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title,
            'body': 'About the pilot.', 'deleted': False,
            'metadata': {'from': 'owner@example.com' if mine else who, 'to': who if mine else 'owner@example.com',
                         'thread_id': thread, 'labels': ['SENT'] if mine else ['INBOX']}}


def m(i, day, mine=True, channel='email'):
    return {'id': i, 'at': f'2026-10-{day:02d}T09:00:00+00:00', 'mine': mine, 'channel': channel}


class Schedule(unittest.TestCase):
    """The pure parts: no database."""

    def rule(self, **kw):
        return {**follow_ups.defaults(), 'on': True, **kw}

    def test_defaults(self):
        d = follow_ups.defaults()
        self.assertEqual((d['days'], d['max_days'], d['min'], d['max'], d['auto'], d['switch'], d['channels'], d['stall']),
                         (3, 7, 1, 3, False, False, None, None))

    def test_waits_the_shortest_wait_and_counts_follow_ups(self):
        msgs = [m(1, 10, mine=False), m(2, 12)]
        self.assertEqual(follow_ups.schedule(msgs, self.rule(), '2026-10-14T09:00:00+00:00')['state'], 'waiting')
        due = follow_ups.schedule(msgs, self.rule(), '2026-10-15T10:00:00+00:00')
        self.assertEqual((due['state'], due['n'], due['after'], due['judge'], due['late']), ('due', 1, 2, False, False))
        self.assertTrue(follow_ups.schedule(msgs, self.rule(), '2026-10-19T09:00:00+00:00')['late'])  # its longest wait (7 days)
        # They wrote last: nothing waits on them
        self.assertEqual(follow_ups.schedule(msgs + [m(3, 13, mine=False)], self.rule(), NOW)['state'], 'replied')

    def test_past_the_minimum_it_judges_and_never_goes_past_the_maximum(self):
        rule = self.rule(min=1, max=3)
        two = [m(1, 1, mine=False), m(2, 2), m(3, 6)]  # one follow-up out
        self.assertTrue(follow_ups.schedule(two, rule, '2026-10-10T09:00:00+00:00')['judge'])  # the second one is judged
        self.assertFalse(follow_ups.schedule(two, self.rule(min=2, max=3), '2026-10-10T09:00:00+00:00')['judge'])  # still within the minimum
        full = [m(1, 1, mine=False), m(2, 2), m(3, 6), m(4, 10), m(5, 14)]  # three follow-ups out
        self.assertEqual(follow_ups.schedule(full, rule, '2026-10-15T09:00:00+00:00')['state'], 'last')  # waits for a reply to the last
        self.assertEqual(follow_ups.schedule(full, rule, '2026-10-17T10:00:00+00:00')['state'], 'ended')

    def test_per_stage_wait_and_old_threads_left_alone(self):
        msgs = [m(1, 10, mine=False), m(2, 12)]
        self.assertEqual(follow_ups.schedule(msgs, self.rule(), '2026-10-15T10:00:00+00:00', days=5)['state'], 'waiting')
        self.assertEqual(follow_ups.schedule(msgs, self.rule(), '2026-10-17T10:00:00+00:00', days=5)['state'], 'due')
        self.assertEqual(follow_ups.schedule([m(1, 1, mine=False), m(2, 2)], self.rule(), '2026-10-29T09:00:00+00:00')['state'], 'stale')

    def test_clean_checks_both_pairs(self):
        self.assertEqual(follow_ups.clean({'on': True, 'min': 2, 'max': 4, 'days': 2, 'max_days': 5})['max'], 4)
        with self.assertRaises(ValueError):
            follow_ups.clean({'on': True, 'min': 3, 'max': 2})
        with self.assertRaises(ValueError):
            follow_ups.clean({'on': True, 'days': 5, 'max_days': 3})
        with self.assertRaises(ValueError):
            follow_ups.clean({'on': True, 'max': 9})
        with self.assertRaises(ValueError):
            follow_ups.clean({'on': True, 'channels': []})
        stages = follow_ups.clean({'stages': {'testing': {'on': False}, 'Gone': True, 'Live': {'days': 6}}}, ['Invited', 'Testing', 'Live'])['stages']
        self.assertEqual(stages, {'Testing': {'on': False}, 'Live': {'on': True, 'days': 6}})

    def test_channel_stays_or_switches_to_the_next_allowed(self):
        rule = self.rule()
        self.assertEqual(follow_ups.pick_channel('email', ['email'], rule, {'email', 'linkedin'}, {'email', 'linkedin'}), 'email')
        # Switch: after an unanswered follow-up, the next allowed channel where the conversation already is
        switch = self.rule(switch=True)
        self.assertEqual(follow_ups.pick_channel('email', ['email'], switch, {'email', 'linkedin'}, {'email', 'linkedin'}), 'email')
        self.assertEqual(follow_ups.pick_channel('email', ['email', 'email'], switch, {'email', 'linkedin'}, {'email', 'linkedin'}), 'linkedin')
        self.assertEqual(follow_ups.pick_channel('linkedin', ['email', 'linkedin'], switch, {'email', 'linkedin'}, {'email', 'linkedin'}), 'email')
        self.assertEqual(follow_ups.pick_channel('email', ['email', 'email'], switch, {'email', 'linkedin'}, {'email'}), 'email')  # not there on LinkedIn
        # Only allowed, connected ones that can send
        self.assertIsNone(follow_ups.pick_channel('email', ['email'], self.rule(channels=['linkedin']), {'email'}, {'email'}))
        self.assertEqual(follow_ups.pick_channel('whatsapp', ['whatsapp'], rule, {'email'}, {'whatsapp', 'email'}), 'email')

    def test_sending_without_asking_needs_everything_plain(self):
        draft = {'kind': 'email', 'to': ['sam@client.example'], 'body': 'Hi'}
        auto = self.rule(auto=True)
        self.assertTrue(follow_ups.may_send_alone(auto, False, draft, 'email', False, False))
        self.assertFalse(follow_ups.may_send_alone(self.rule(), False, draft, 'email', False, False))  # Ask me before sending
        self.assertFalse(follow_ups.may_send_alone(auto, True, draft, 'email', False, False))  # Careful
        self.assertFalse(follow_ups.may_send_alone(auto, False, {**draft, 'to_options': ['x@y.z']}, 'email', False, False))
        self.assertFalse(follow_ups.may_send_alone(auto, False, {**draft, 'kind': 'linkedin'}, 'email', False, False))
        self.assertFalse(follow_ups.may_send_alone(auto, False, draft, 'email', True, False))  # tried before
        self.assertFalse(follow_ups.may_send_alone(auto, False, draft, 'email', False, True))  # a repeat

    def test_repeats(self):
        self.assertTrue(follow_ups.repeats('Any news on the pilot?', ['any news on the pilot']))
        self.assertFalse(follow_ups.repeats('Here is the case study I mentioned.', ['Any news on the pilot?']))

    def test_follow_ups_pause_before_other_background_work(self):
        now_s = 1_000_000
        usage = lambda short, week=2: [{'provider': 'anthropic', 'windows': [{'label': '5h', 'used': short, 'reset': now_s + 3600},
                                                                            {'label': 'Week', 'used': week, 'reset': now_s + 6 * 86400}]}]
        self.assertIsNone(model_budget.follow_up_pause(usage(20), now_s))
        self.assertIsNone(model_budget.pause(usage(55), now_s))  # other background work goes on
        self.assertEqual(model_budget.follow_up_pause(usage(55), now_s)['threshold'], model_budget.FOLLOW_UP_PAUSE)
        self.assertIsNone(model_budget.follow_up_pause(usage(55), now_s, late=True))  # at its longest wait, like the rest
        self.assertIsNotNone(model_budget.follow_up_pause(usage(70), now_s, late=True))
        self.assertEqual(model_budget.follow_up_pause(usage(10, week=10), now_s)['window'], 'week')  # day 1: 14% allowed, 10 room
        self.assertIsNone(model_budget.follow_up_pause(None, now_s))  # no windows: never paused


class FollowUps(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        for target, value in (('LOCAL_TZ', ZoneInfo('Europe/Brussels')),):
            p = patch.object(a, target, value)
            p.start()
            self.addCleanup(p.stop)
        self.clock = patch.object(a, 'now', return_value=NOW)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [msg('in1', '2026-10-08T09:00:00+00:00'), msg('out1', '2026-10-13T09:00:00+00:00', mine=True),
                                            msg('in2', '2026-10-09T09:00:00+00:00', who='kim@other.example', thread='t2', title='Trial'),
                                            msg('out2', '2026-10-14T09:00:00+00:00', mine=True, who='kim@other.example', thread='t2', title='Trial')])
        with self.store.connect() as db:
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            self.ev = ids
            self.board = graph.save_board(db, {'name': 'Alpha testers', 'stages': [{'name': 'Invited'}, {'name': 'Testing'}, {'name': 'Live'}],
                                               'about': 'People trying the alpha.'}, '2026-10-01T09:00:00+00:00')['board_id']
            self.acme = graph.label(db, [ids['in1'], ids['out1']], 'Acme pilot', 'review', NOW)
            self.kim = graph.label(db, [ids['in2'], ids['out2']], 'Kim trial', 'review', NOW)
            for pid in (self.acme, self.kim):
                db.execute("UPDATE projects SET board_id=?,stage='Invited',stage_by='review',stage_at='2026-10-01T09:00:00+00:00' WHERE id=?", (self.board, pid))

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch.object(a, 'now', return_value=stamp)
        self.clock.start()

    def app(self, **config):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL], 'digest_at': '08:30', 'review_worker': {'enabled': True}, **config}
        app.model_usage = None
        app.usage_limit = None
        app.fleet = None
        app.teammate_addresses = lambda: []
        return app

    def turn_on(self, scope='board', ref=None, **settings):
        return self.app().action('follow_up_save', {'scope': scope, 'id': ref or self.board, 'settings': {'on': True, **settings}}, owner_dashboard=True)

    def cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT f.*,s.status,s.title,s.early,d.status delivery FROM follow_up_cards f JOIN suggestions s ON '
                                                's.id=f.suggestion_id JOIN deliveries d ON d.suggestion_id=s.id ORDER BY f.project_id')]

    def prepared(self, sid, body='Hi Sam, here is the case study I mentioned.', kind='email', **extra):
        draft = {'kind': kind, 'account_id': 'work', 'from': 'owner@example.com', 'to': ['sam@client.example'], 'subject': 'Re: Pilot',
                 'body': body, 'revision': 'r-' + sid[:6], **extra}
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',next_action=? WHERE id=?", (json.dumps(draft), sid))
            db.execute("UPDATE preparations SET status='done' WHERE suggestion_id=?", (sid,))
        return draft

    def jobs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT suggestion_id,status,source FROM action_jobs')]

    # ------------------------------------------------------------------

    def test_off_by_default_and_nothing_drafted(self):
        self.assertEqual(self.app().follow_up_step(), {'drafted': 0})
        self.assertEqual(self.cards(), [])

    def test_a_board_drafts_one_grouped_to_do_per_project_prepared_ahead(self):
        panel = self.turn_on()
        self.assertEqual((panel['settings']['min'], panel['settings']['max'], panel['stalled']), (1, 3, True))
        self.assertEqual([s['name'] for s in panel['stages']], ['Invited', 'Testing', 'Live'])
        self.assertEqual([s['open'] for s in panel['stages']], [True, True, False])
        self.assertEqual(panel['channels'], ['email'])
        self.assertEqual(self.app().follow_up_step()['drafted'], 2)
        cards = self.cards()
        self.assertEqual([(c['project_id'], c['grouped'], c['n'], c['channel'], c['status'], c['early']) for c in cards],
                         [(self.acme, 1, 1, 'email', 'accepted', 1), (self.kim, 1, 1, 'email', 'accepted', 1)])
        self.assertEqual(sorted(c['delivery'] for c in cards), ['grouped', 'queued'])  # one heads-up for the batch
        self.assertEqual(cards[0]['title'], 'Follow up on Acme pilot')
        # The dashboard groups them under the board
        with self.store.connect() as db:
            view = follow_ups.cards_view(db, [c['suggestion_id'] for c in cards])
        self.assertEqual({v['group'] for v in view.values()}, {'board:' + str(self.board)})
        # Once per waiting point
        self.assertEqual(self.app().follow_up_step()['drafted'], 0)
        self.assertEqual(len(self.cards()), 2)
        # Board and project show where they stand
        with self.store.connect() as db:
            boards = graph.boards(db, a.now())
            self.app().follow_up_annotate(db, boards)
        self.assertTrue(boards[0]['follow_ups']['on'])
        self.assertEqual(boards[0]['follow_ups']['next_at'], None)  # both have a to-do out now
        self.assertEqual({p['follow_up']['state'] for p in boards[0]['projects']}, {'open'})

    def test_a_project_overrides_its_board(self):
        self.turn_on()
        self.turn_on('project', self.kim, on=False)
        self.assertEqual(self.app().follow_up_step()['drafted'], 1)
        self.assertEqual([c['project_id'] for c in self.cards()], [self.acme])
        # A project on its own (board off): a normal to-do, not grouped
        self.turn_on(on=False)
        self.turn_on('project', self.kim)
        self.app().follow_up_step()
        kim = [c for c in self.cards() if c['project_id'] == self.kim][0]
        self.assertEqual((kim['grouped'], kim['delivery']), (0, 'queued'))
        # Back to the board's setting
        self.app().action('follow_up_save', {'scope': 'project', 'id': 'project:%d' % self.kim, 'settings': {'inherit': True}}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertIsNone(follow_ups.rule(db, 'project', self.kim))

    def test_waits_for_the_days_and_a_stage_can_be_off_or_wait_longer(self):
        self.turn_on(stages={'Invited': {'on': True, 'days': 10}})
        self.assertEqual(self.app().follow_up_step()['drafted'], 0)  # 6 and 5 days since: not yet
        self.turn_on(stages={'Invited': {'on': False}})
        self.assertEqual(self.app().follow_up_step()['drafted'], 0)
        with self.store.connect() as db:
            db.execute("UPDATE projects SET stage='Live' WHERE id=?", (self.acme,))
        self.turn_on()
        self.app().follow_up_step()
        self.assertEqual([c['project_id'] for c in self.cards()], [self.kim])  # the last stage is off by default

    def test_stops_when_they_reply_won_lost_archived_or_a_teammate_owns_it(self):
        self.turn_on()
        self.app().follow_up_step()
        acme, kim = self.cards()
        # Sam replies: Acme's follow-up closes by itself, with why
        self.store.commit_page('work', {}, [msg('in3', '2026-10-19T08:30:00+00:00')])
        with self.store.connect() as db:
            graph.label(db, [db.execute("SELECT id FROM events WHERE source_id='in3'").fetchone()[0]], 'Acme pilot', 'review', NOW)
        self.app().follow_up_step()
        with self.store.connect() as db:
            why = db.execute("SELECT feedback,source FROM decisions WHERE suggestion_id=? AND choice='reject'", (acme['suggestion_id'],)).fetchone()
            graph.set_outcome(db, 'project:%d' % self.kim, 'won', 'Signed', NOW)
        self.assertEqual(tuple(why), ('They replied, so this follow-up isn’t needed.', 'assistant'))
        self.assertFalse(why['feedback'].startswith('You'))
        self.app().follow_up_step()
        states = {c['project_id']: (c['state'], c['status'], c['why']) for c in self.cards()}
        self.assertEqual(states, {self.acme: ('stopped', 'rejected', 'replied'), self.kim: ('stopped', 'rejected', 'won')})
        # A teammate owns a project: their Machine follows it up, not this one
        with self.store.connect() as db:
            self.assertEqual(follow_ups.stop_reason(db.execute('SELECT * FROM projects WHERE id=?', (self.acme,)).fetchone(),
                                                    {'on': True}, 'project', None, owned_by_other=True), 'teammate')
            db.execute('CREATE TABLE IF NOT EXISTS record_owners(node_id TEXT PRIMARY KEY,owner TEXT NOT NULL,name TEXT,set_at TEXT NOT NULL)')
            db.execute("INSERT INTO record_owners VALUES(?,?,?,?)", ('project:%d' % self.acme, 'fleet:m2', 'Pat', NOW))
            self.assertTrue(follow_ups.owned_by_other(db, self.acme))
            graph.archive_project(db, 'project:%d' % self.kim, True, NOW)
            self.assertEqual({x['project']['id']: x.get('reason') for x in follow_ups.plan(db, NOW, {'email'})},
                             {self.acme: 'teammate', self.kim: 'archived'})

    def test_turning_off_closes_open_ones(self):
        self.turn_on()
        self.app().follow_up_step()
        self.turn_on(on=False)
        self.assertEqual({(c['state'], c['why']) for c in self.cards()}, {('stopped', 'off')})

    def test_asks_by_default_and_sends_without_asking_only_when_chosen(self):
        self.turn_on()
        self.app().follow_up_step()
        acme = self.cards()[0]
        self.prepared(acme['suggestion_id'])
        self.app().follow_up_step()
        self.assertEqual(self.jobs(), [])  # Ask me before sending: it waits for the owner's Send
        self.turn_on(auto=True)
        self.app().follow_up_step()
        self.assertEqual(self.jobs(), [{'suggestion_id': acme['suggestion_id'], 'status': 'queued', 'source': 'auto_follow_up'}])
        # Never twice: the same draft again queues nothing new, also through the owner's Send
        self.app().follow_up_send()
        again = self.store.confirm_action(acme['suggestion_id'], 'r-' + acme['suggestion_id'][:6], 'tap', 'dashboard')
        self.assertTrue(again['duplicate'])
        self.assertEqual(len(self.jobs()), 1)
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='sent'")
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (acme['suggestion_id'],))
        self.app().follow_up_step()
        self.assertEqual(self.cards()[0]['state'], 'sent')
        self.assertEqual(self.cards()[0]['auto'], 1)

    def test_careful_and_anything_unusual_ask_first(self):
        self.turn_on(auto=True)
        self.app().follow_up_step()
        acme, kim = self.cards()
        self.prepared(acme['suggestion_id'])
        self.prepared(kim['suggestion_id'], to_options=['kim@other.example', 'ops@other.example'])  # no verified recipient
        with patch.object(follow_ups, 'careful', return_value=True):
            self.app().follow_up_send()
        self.assertEqual(self.jobs(), [])
        self.app().follow_up_send()
        self.assertEqual([j['suggestion_id'] for j in self.jobs()], [acme['suggestion_id']])
        # Outside the owner's hours nothing goes by itself
        with self.store.connect() as db:
            db.execute('DELETE FROM action_jobs')
        self.at('2026-10-19T22:00:00+00:00')
        self.assertEqual(self.app().follow_up_send(), [])

    def test_a_repeated_text_asks(self):
        self.turn_on(auto=True)
        self.app().follow_up_step()
        acme = self.cards()[0]
        self.prepared(acme['suggestion_id'], body='Any news on the pilot?')
        with patch.object(follow_ups, 'earlier_texts', return_value=['Any news on the pilot?']):
            self.app().follow_up_send()
        self.assertEqual(self.jobs(), [])

    def test_normal_work_and_tight_usage_come_first(self):
        self.turn_on()
        app = self.app()
        app.model_usage = [{'provider': 'anthropic', 'windows': [{'label': '5h', 'used': 55, 'reset': 9e12}]}]
        with patch.object(a, 'openclaw_model', return_value='anthropic/claude'):
            with patch.object(follow_ups, 'schedule', wraps=follow_ups.schedule) as sched:
                # Not late yet: waits while the 5-hour window is past FOLLOW_UP_PAUSE
                self.at('2026-10-17T10:00:00+00:00')
                self.assertEqual(app.follow_up_step()['drafted'], 0)
                self.assertTrue(sched.called)
            self.at(NOW)  # Acme reached its longest wait (6 days... 7 for Kim): late ones go ahead
            self.at('2026-10-21T10:00:00+00:00')
            self.assertGreater(app.follow_up_step()['drafted'], 0)
        # Another preparation waiting: follow-ups wait for it
        with self.store.connect() as db:
            db.execute('DELETE FROM follow_up_cards')
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,status) VALUES('other','k','T','B','[]','[]',?, 'accepted')", (NOW,))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES('other','d','j','queued',?,?)", (NOW, NOW))
        self.assertEqual(self.app().follow_up_step()['drafted'], 0)

    def test_follow_ups_dont_use_up_the_room_for_other_to_dos(self):
        self.turn_on()
        self.app().follow_up_step()
        self.assertTrue(self.store.ahead_room(1))

    def test_no_reply_after_the_last_ends_the_round_and_moves_to_stalled(self):
        self.turn_on(min=1, max=1)
        self.app().follow_up_step()
        acme = self.cards()[0]
        self.prepared(acme['suggestion_id'])
        self.store.confirm_action(acme['suggestion_id'], 'r-' + acme['suggestion_id'][:6], 'tap', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='sent'")
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (acme['suggestion_id'],))
        # The follow-up as it came back from Gmail: the owner's message, after it
        self.store.commit_page('work', {}, [msg('out3', '2026-10-19T09:05:00+00:00', mine=True)])
        with self.store.connect() as db:
            graph.label(db, [db.execute("SELECT id FROM events WHERE source_id='out3'").fetchone()[0]], 'Acme pilot', 'review', NOW)
        self.app().follow_up_step()
        self.assertEqual(self.cards()[0]['state'], 'sent')
        self.at('2026-10-22T10:00:00+00:00')  # three days, no reply
        self.app().follow_up_step()
        with self.store.connect() as db:
            end = dict(db.execute('SELECT n,moved,judged FROM follow_up_ends WHERE project_id=?', (self.acme,)).fetchone())
            project = db.execute('SELECT stage,stage_reason FROM projects WHERE id=?', (self.acme,)).fetchone()
            moves = graph.project_moves(db, 'project:%d' % self.acme)['moves']
        self.assertEqual(end, {'n': 1, 'moved': 1, 'judged': 0})
        self.assertEqual(tuple(project), (graph.STALLED, 'No reply after 1 follow-up'))
        self.assertEqual((moves[0]['stage'], moves[0]['source']), (graph.STALLED, 'follow_up'))
        # Once: nothing more for this project
        self.app().follow_up_step()
        self.assertEqual([c['project_id'] for c in self.cards()].count(self.acme), 1)

    def test_the_move_to_stalled_is_a_setting(self):
        self.turn_on(min=1, max=1, stall=False)
        with self.store.connect() as db:
            p = db.execute('SELECT * FROM projects WHERE id=?', (self.acme,)).fetchone()
            board = db.execute('SELECT * FROM boards WHERE id=?', (self.board,)).fetchone()
            settings = follow_ups.rule(db, 'board', self.board)
            self.assertEqual(follow_ups.end(db, {'project': p, 'board': board, 'settings': settings, 'n': 2, 'after': self.ev['out1'],
                                                 'after_at': '2026-10-13T09:00:00+00:00'}, NOW), {'n': 1, 'moved': False})
            self.assertEqual(db.execute('SELECT stage FROM projects WHERE id=?', (self.acme,)).fetchone()[0], 'Invited')
            self.assertFalse(follow_ups.stalls({'stall': None}, None))

    def test_past_the_minimum_the_preparation_can_judge_it_not_worth_it(self):
        self.turn_on(min=0, max=3)
        self.app().follow_up_step()
        acme = self.cards()[0]
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'already_done', 'follow_up': 'stop'}), acme['suggestion_id']))
        self.app().follow_up_step()
        with self.store.connect() as db:
            end = dict(db.execute('SELECT n,moved,judged FROM follow_up_ends WHERE project_id=?', (self.acme,)).fetchone())
        self.assertEqual(end, {'n': 0, 'moved': 1, 'judged': 1})
        self.assertEqual(self.cards()[0]['why'], 'judged')
        # Within the minimum the same outcome only means it was handled
        self.turn_on(min=1, max=3)
        kim = self.cards()[1]
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'already_done', 'follow_up': 'stop'}), kim['suggestion_id']))
        self.app().follow_up_step()
        self.assertEqual(self.cards()[1]['why'], 'handled')

    def test_the_preparation_hears_which_follow_up_and_what_went_before(self):
        self.turn_on()
        self.app().follow_up_step()
        acme = self.cards()[0]
        with patch.object(follow_ups, 'earlier_texts', return_value=['Any news on the pilot?']):
            lines = self.app().follow_up_lines(acme['suggestion_id'])
        self.assertIn('Automated follow-up 1 (at most 3)', lines)
        self.assertIn('kind email', lines)
        self.assertIn('Any news on the pilot?', lines)
        self.assertNotIn('Judge from the thread', lines)  # the first is within the minimum
        self.assertEqual(self.app().follow_up_lines('nope'), '')

    def test_only_the_owner_sets_follow_ups(self):
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app().action('follow_up_save', {'scope': 'board', 'id': self.board, 'settings': {'on': True}}, owner_dashboard=False)
        self.assertIn('follow_up_save', a.DASHBOARD_ACTIONS)
        self.assertIn('follow_up_settings', a.OWNER_ACTIONS)


if __name__ == '__main__':
    unittest.main()

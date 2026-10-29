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


OWN = {'emails': {'owner@example.com'}, 'names': {'owen owner'}}
GMAIL_CHAIN = """Hi Sam, any thoughts on the listing?

Owen

On Mon, 21 Sep 2026 08:24:10 -0500, Owen Owner <owner@example.com> wrote:
> Hi Sam, following up on the exchange.
>
> On Wed, 16 Sep 2026 04:31:33 -0500, Owen Owner <
> owner@example.com> wrote:
> > Hi Sam, would you be open to an exchange?
"""
OUTLOOK_CHAIN = """Hi Sam, one more try.

________________________________
From: Owen Owner <owner@example.com>
Sent: Monday, September 21, 2026 3:24 PM
To: Sam <sam@client.example>
Subject: RE: Exchange

Hi Sam, following up.

-----Original Message-----
From: Owen Owner
Sent: Wednesday, September 16, 2026 9:31 AM
To: Sam
Subject: Exchange

Hi Sam, would you be open to an exchange?
"""
REPLIED_BETWEEN = """Hi Sam, did you see my last note?

Le lun. 21 sept. 2026 à 08:24, Owen Owner <owner@example.com> a écrit :
> Thanks, here are the details.
>
> Le ven. 18 sept. 2026 à 10:00, Sam Client <sam@client.example> a écrit :
> > Sounds good, send me the details.
> >
> > Le mer. 16 sept. 2026 à 04:31, Owen Owner <owner@example.com> a écrit :
> > > Would you be open to an exchange?
"""


class EarlierSends(unittest.TestCase):
    """The owner's earlier unanswered sends that only show in the thread (sent before The Machine read the mailbox)."""

    def test_a_gmail_chain_counts_each_own_quoted_message(self):
        self.assertEqual(follow_ups.quoted_sends(GMAIL_CHAIN, OWN), ['2026-09-21T13:24:10+00:00', '2026-09-16T09:31:33+00:00'])

    def test_an_outlook_chain_counts_too_by_address_or_full_name(self):
        self.assertEqual(follow_ups.quoted_sends(OUTLOOK_CHAIN, OWN), ['2026-09-21T15:24:00+00:00', '2026-09-16T09:31:00+00:00'])
        self.assertEqual(follow_ups.quoted_sends(OUTLOOK_CHAIN, {'emails': {'owner@example.com'}, 'names': set()}),
                         ['2026-09-21T15:24:00+00:00'])  # the name alone isn't known: stops there

    def test_a_reply_in_between_starts_the_count_again(self):
        self.assertEqual(follow_ups.quoted_sends(REPLIED_BETWEEN, OWN), ['2026-09-21T08:24:00+00:00'])

    def test_no_quotes_no_earlier_sends(self):
        self.assertEqual(follow_ups.quoted_sends('Hi Sam, would you be open to an exchange?\n\nOwen', OWN), [])
        self.assertEqual(follow_ups.quoted_sends('', OWN), [])

    def test_a_forwarded_message_is_not_this_conversation(self):
        body = 'FYI\n\n---------- Forwarded message ---------\nFrom: Owen Owner <owner@example.com>\nDate: Mon, Sep 21, 2026 at 3:24 PM\n'
        self.assertEqual(follow_ups.quoted_sends(body, OWN), [])

    def test_the_real_thread_is_read_the_same_way(self):
        def item(i, ms, sender, labels=('INBOX',)):
            return {'id': i, 'internalDate': str(ms), 'labelIds': list(labels), 'payload': {'headers': [{'name': 'From', 'value': sender}]}}
        thread = {'messages': [item('a', 1000, 'Sam <sam@client.example>'), item('b', 2000, 'Owen <owner@example.com>', ['SENT']),
                               item('c', 3000, 'owner@example.com'), item('d', 3500, 'owner@example.com', ['DRAFT']),
                               item('e', 4000, 'Owen <owner@example.com>', ['SENT'])]}
        self.assertEqual(follow_ups.thread_sends(thread, 'e', {'owner@example.com'}),
                         ['1970-01-01T00:00:03+00:00', '1970-01-01T00:00:02+00:00'])
        self.assertIsNone(follow_ups.thread_sends(thread, 'zz', {'owner@example.com'}))

    def test_earlier_sends_count_in_the_schedule_and_can_reach_the_maximum(self):
        rule = {**follow_ups.defaults(), 'on': True, 'max': 3}
        msgs = [m(5, 13)]
        found = follow_ups.schedule(msgs, rule, '2026-10-17T10:00:00+00:00', prior=2, since='2026-09-16T09:31:33+00:00')
        self.assertEqual((found['state'], found['n'], found['round_at']), ('due', 3, '2026-09-16T09:31:33+00:00'))
        found = follow_ups.schedule(msgs, rule, '2026-10-17T10:00:00+00:00', prior=3, since='2026-09-10T09:00:00+00:00')
        self.assertEqual((found['state'], found['n']), ('ended', 4))  # three follow-ups already out: done for this round


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
        unread = patch.object(a.Gmail, 'get', side_effect=a.SourceError('offline'))  # no live reads: the quoted history
        unread.start()
        self.addCleanup(unread.stop)
        # The fresh read right before a send (App.follow_up_thread): a fake mailbox once a test goes online (the outbox
        # tests), else the offline Gmail above. Never a live read.
        self.mailbox = FakeMailbox(self)
        real = a.App.follow_up_thread
        fresh = patch.object(a.App, 'follow_up_thread', autospec=True,
                             side_effect=lambda app, account, thread_id: self.mailbox.read(account, thread_id) if self.mailbox.online else real(app, account, thread_id))
        fresh.start()
        self.addCleanup(fresh.stop)
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
        self.assertEqual(cards[0]['title'], 'Follow up with Acme pilot')
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

    def test_follow_up_drafts_start_together_without_the_ahead_gap(self):
        self.store.commit_page('work', {}, [msg('in4', '2026-10-09T09:00:00+00:00', who='lee@third.example', thread='t3', title='Demo'),
                                            msg('out4', '2026-10-14T09:00:00+00:00', mine=True, who='lee@third.example', thread='t3', title='Demo')])
        with self.store.connect() as db:
            ids = [db.execute('SELECT id FROM events WHERE source_id=?', (x,)).fetchone()[0] for x in ('in4', 'out4')]
            lee = graph.label(db, ids, 'Lee demo', 'review', NOW)
            db.execute("UPDATE projects SET board_id=?,stage='Invited' WHERE id=?", (self.board, lee))
            for name in ('first_ahead_started', 'first_card_shown'):  # past the first look: other ahead drafts go one per gap
                db.execute('INSERT OR IGNORE INTO milestones(name,at) VALUES(?,?)', (name, NOW))
        self.turn_on()
        app = self.app()
        self.assertEqual(app.follow_up_step()['drafted'], 3)
        app.background_at = __import__('time').time()  # another background turn just went
        app.stop_stale_runs = lambda runner: None
        app.follow_up_lines = lambda sid: ''
        calls = []
        with patch.object(a.App, 'follow_up_pause', return_value=None), patch.object(a.App, 'background_pause', return_value=None):
            app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertEqual(len([c for c in calls if c['action'] == 'start']), 3)
        self.assertTrue(all(c['background'] for c in calls))  # still background work (background_model)
        # A usage limit still holds them
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='queued'")
            db.execute('DELETE FROM preparation_runs')
        calls.clear()
        with patch.object(a.App, 'follow_up_pause', return_value={'window': '5h'}), patch.object(a.App, 'background_pause', return_value=None):
            app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertEqual(calls, [])

    def model_turns(self, app, rewrite, **extra):
        """One preparation pass with a fake model: each started turn saves what rewrite(suggestion_id, message, draft)
        returns as its result (assistant_signals prepare), as the agent would. No live model, nothing sent. Returns the
        turns started and the saves the service refused."""
        calls, refused = [], []

        def runner(request):
            calls.append(request)
            if request['action'] == 'start':
                with self.store.connect() as db:
                    sid = db.execute('SELECT suggestion_id FROM preparations WHERE job_id=?', (request['job_id'],)).fetchone()[0]
                    current = db.execute('SELECT next_action FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
                draft = next(iter(a.next_actions.actions(current or 'null')), None)
                saved = rewrite(sid, request['message'], draft)
                if saved is not None:
                    try:
                        app.action('prepare', {'suggestion_id': sid, 'job_id': request['job_id'], 'body': 'Follow-up ready.', 'next_actions': [saved],
                                               'outcome': 'needs_you', 'needs': 'check the draft and send it', 'note_kind': 'style', **extra})
                    except ValueError as error:  # the agent sees why and saves again
                        refused.append((sid, str(error)))
            return {'status': 'admitted'}
        app.preparation_step(runner)
        with self.store.connect() as db:
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=? WHERE finished_at IS NULL", (NOW,))
        return [c for c in calls if c['action'] == 'start'], refused

    def test_change_in_the_review_rewrites_the_drafts_through_their_chat_and_never_sends(self):
        self.turn_on()
        app = self.app()
        app.stop_stale_runs = lambda runner: None
        app.follow_up_lines = lambda sid: ''
        self.assertEqual(app.follow_up_step()['drafted'], 2)
        acme, kim = [c['suggestion_id'] for c in self.cards()]
        first = lambda sid: {'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example' if sid == acme else 'kim@other.example'],
                             'subject': 'Re: Pilot', 'body': 'Hi, here is the case study I mentioned.\n\nRegards,\n\nOwen'}
        with patch.object(a.App, 'follow_up_pause', return_value=None), patch.object(a.App, 'background_pause', return_value=None):
            self.assertEqual(self.model_turns(app, lambda sid, message, draft: first(sid))[1], [])
        def drafts():
            with self.store.connect() as db:
                return {s: a.next_actions.actions(db.execute('SELECT next_action FROM suggestions WHERE id=?', (s,)).fetchone()[0])[0] for s in (acme, kim)}
        before = drafts()
        self.assertEqual({c['status'] for c in self.cards()}, {'prepared'})
        # Only the owner, on the dashboard
        with self.assertRaises(ValueError):
            app.action('follow_up_change', {'ids': [acme], 'text': 'Shorter.'}, owner_dashboard=False)
        self.assertIn('follow_up_change', a.DASHBOARD_ACTIONS)
        with self.assertRaises(ValueError):
            app.action('follow_up_change', {'ids': [acme], 'text': '  '}, owner_dashboard=True)
        # All checked: both go back to work as a Change note in their chat (decide 'other'), nothing queued to send
        said = app.action('follow_up_change', {'ids': [acme, kim, 'f' * 16], 'text': 'Shorter, and ask about Friday.'}, owner_dashboard=True)
        self.assertEqual(said, {'changing': [{'id': acme, 'revision': before[acme]['revision']}, {'id': kim, 'revision': before[kim]['revision']}],
                                'skipped': ['f' * 16]})
        with self.store.connect() as db:
            notes = db.execute("SELECT suggestion_id,id,feedback,source FROM decisions WHERE choice='other' ORDER BY suggestion_id").fetchall()
            self.assertEqual([(n['suggestion_id'], n['feedback'], n['source']) for n in notes],
                             sorted([(acme, 'Shorter, and ask about Friday.', 'dashboard'), (kim, 'Shorter, and ask about Friday.', 'dashboard')]))
            self.assertTrue(all(n['id'].startswith('chat-') for n in notes))  # the chat's own path
            self.assertEqual({r[0] for r in db.execute('SELECT status FROM suggestions WHERE id IN (?,?)', (acme, kim))}, {'instructions'})
        self.assertEqual(self.jobs(), [])
        # The owner's ask, not background work: not held by the follow-up pause, at most DRAFTING at once
        with patch.object(a.App, 'follow_up_pause', return_value={'window': '5h'}), patch.object(a.App, 'background_pause', return_value=None), \
                patch.object(follow_ups, 'DRAFTING', 1):
            starts = self.model_turns(app, lambda sid, message, draft: None)[0]
        self.assertEqual(len(starts), 1)
        self.assertIn(follow_ups.CHANGE_NOTE, starts[0]['message'])
        self.assertNotIn('background', starts[0])
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='queued' WHERE status IN ('starting','running')")
            db.execute('DELETE FROM preparation_runs')
        # The fake model rewrites both at once: one keeps everything but the text, one tries another recipient and a send
        tries = []

        def rewrite(sid, message, draft):
            tries.append(sid)
            out = {**first(sid), 'body': 'Hi, short one: does Friday work?\n\nRegards,\n\nOwen'}
            if sid == kim and tries.count(kim) == 1:
                out['to'] = ['someone@else.example']
            return out
        with patch.object(a.App, 'follow_up_pause', return_value={'window': '5h'}), patch.object(a.App, 'background_pause', return_value=None):
            starts, refused = self.model_turns(app, rewrite)
        self.assertEqual(len(starts), 2)  # both at once
        self.assertEqual([r[0] for r in refused], [kim], refused)
        self.assertIn("keep the draft's to as it was", refused[0][1])
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (kim,)).fetchone()[0]
        with self.assertRaises(ValueError) as sent:
            app.action('prepare', {'suggestion_id': kim, 'job_id': job, 'body': 'Sent.', 'next_actions': [{**first(kim), 'body': 'Hi, Friday?'}],
                                   'send_now': True, 'outcome': 'done', 'note_kind': 'style'})
        self.assertIn('never sent from here', str(sent.exception))
        app.action('prepare', {'suggestion_id': kim, 'job_id': job, 'body': 'Follow-up ready.', 'next_actions': [{**first(kim), 'body': 'Hi, Friday?'}],
                               'outcome': 'needs_you', 'needs': 'check the draft and send it', 'note_kind': 'style'})
        after = drafts()
        self.assertEqual(after[acme]['body'], 'Hi, short one: does Friday work?\n\nRegards,\n\nOwen')
        self.assertEqual(after[kim]['body'], 'Hi, Friday?')
        for sid in (acme, kim):  # same channel, recipient, account and thread; a new revision; ready, not sent
            self.assertEqual(follow_ups.route(after[sid]), follow_ups.route(before[sid]))
            self.assertNotEqual(after[sid]['revision'], before[sid]['revision'])
        self.assertEqual({c['status'] for c in self.cards()}, {'prepared'})
        self.assertEqual({c['state'] for c in self.cards()}, {'open'})
        self.assertEqual(self.jobs(), [])
        # Only this one; then Undo change is the owner's own edit back to the text before
        said = app.action('follow_up_change', {'ids': [acme], 'text': 'Mention the video.'}, owner_dashboard=True)
        self.assertEqual([c['id'] for c in said['changing']], [acme])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (kim,)).fetchone()[0], 'prepared')
        # A draft on its way out (Send all checked, spaced) isn't changed under it
        self.store.confirm_action(kim, after[kim]['revision'], 'tap', 'dashboard')
        self.assertEqual(app.action('follow_up_change', {'ids': [kim], 'text': 'Shorter.'}, owner_dashboard=True), {'changing': [], 'skipped': [kim]})
        self.assertEqual([j['status'] for j in self.jobs()], ['queued'])

    def test_a_change_takes_the_full_context_and_a_skill_added_after_the_drafts(self):
        """"I added a skill, use it now": the rewrite is a full preparation turn (style, the thread, earlier follow-ups),
        never the chat's short turn, and it names the skills on right now, one added after the drafts included, with
        its SKILL.md to read. The fake model reads that file and follows it."""
        import skills
        self.turn_on()
        app = self.app(openclaw_workspace=self.tmp.name)
        app.stop_stale_runs = lambda runner: None
        app.skills = skills.Skills(self.store.connect, self.tmp.name)
        self.assertEqual(app.follow_up_step()['drafted'], 2)
        acme = [c['suggestion_id'] for c in self.cards()][0]
        first = {'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example'], 'subject': 'Re: Pilot', 'body': 'Hi, any news?\n\nRegards,\n\nOwen'}
        with patch.object(a.App, 'follow_up_pause', return_value=None), patch.object(a.App, 'background_pause', return_value=None):
            self.model_turns(app, lambda sid, message, draft: first if sid == acme else None)
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done' WHERE suggestion_id!=?", (acme,))
        # minutes later the owner adds a skill, then asks for it in the review
        app.skills.save(None, 'Listing exchanges', 'How to follow up on a listing exchange',
                        'Offer a listing on our partner page in return, and link the page: https://example.com/partners.')
        app.action('follow_up_change', {'ids': [acme], 'text': 'I added a skill, use it now'}, owner_dashboard=True)
        seen = []

        def rewrite(sid, message, draft):
            seen.append(message)
            path = next(Path(line.rsplit('(', 1)[1].rstrip(')')) for line in message.splitlines() if line.startswith('- Listing exchanges:'))
            follow = path.read_text().strip().splitlines()[-1]  # the skill's instructions, read as the agent would
            return {**first, 'body': 'Hi Sam, ' + follow.split(',')[0].lower() + '?\n\nRegards,\n\nOwen'}
        with patch.object(a.App, 'follow_up_pause', return_value={'window': '5h'}), patch.object(a.App, 'background_pause', return_value=None):
            starts, refused = self.model_turns(app, rewrite)
        self.assertEqual((len(starts), refused), (1, []))
        message = seen[0]
        self.assertNotIn('The owner wrote to you in the chat', message)  # not the short chat turn
        self.assertIn('Follow the preparation rules above', message)  # the full preparation context
        self.assertIn('Automated follow-up 1', message)  # which follow-up it is, its channel and earlier ones (follow_up_lines)
        self.assertIn(follow_ups.CHANGE_NOTE, message)
        self.assertIn('- Listing exchanges: How to follow up on a listing exchange (', message)
        self.assertIn(str(Path(self.tmp.name) / 'skills' / skills.FOLDER / 'listing-exchanges' / 'SKILL.md'), message)
        with self.store.connect() as db:
            body = a.next_actions.actions(db.execute('SELECT next_action FROM suggestions WHERE id=?', (acme,)).fetchone()[0])[0]['body']
        self.assertTrue(body.startswith('Hi Sam, offer a listing on our partner page in return?'), body)
        self.assertEqual(self.jobs(), [])  # nothing sent

    def test_short_names_without_the_board(self):
        self.assertEqual(follow_ups.short_name('Editorial listing exchanges: Solutions GURUS', 'Editorial listing exchanges'), 'Solutions GURUS')
        self.assertEqual(follow_ups.short_name('Editorial listing exchang: WEBRIS: Law Firm Marketing Agency', 'Editorial listing exchanges'),
                         'WEBRIS: Law Firm Marketing Agency')
        self.assertEqual(follow_ups.short_name('Acme pilot', 'Alpha testers'), 'Acme pilot')
        self.assertEqual(follow_ups.short_name('Salesflare acquisition: Perficient', 'Acquisition conversations'), 'Salesflare acquisition: Perficient')
        self.assertEqual(follow_ups.short_name('Alpha: Acme', 'Alpha testers'), 'Alpha: Acme')  # too short a front to be the board's
        self.assertEqual(follow_ups.short_name('Alpha testers: ', 'Alpha testers'), 'Alpha testers: ')
        # The to-do's title and the review name the project without the board
        with self.store.connect() as db:
            db.execute("UPDATE projects SET name='Alpha testers: Acme pilot' WHERE id=?", (self.acme,))
        self.turn_on()
        self.app().follow_up_step()
        acme = [c for c in self.cards() if c['project_id'] == self.acme][0]
        self.assertEqual(acme['title'], 'Follow up with Acme pilot')
        with self.store.connect() as db:
            view = follow_ups.cards_view(db, [acme['suggestion_id']])[acme['suggestion_id']]
        self.assertEqual((view['project'], view['name']), ('Alpha testers: Acme pilot', 'Acme pilot'))

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

    def test_earlier_sends_quoted_in_the_thread_count_and_the_round_starts_at_the_first(self):
        with self.store.connect() as db:
            db.execute('UPDATE events SET body=? WHERE id=?', (GMAIL_CHAIN, self.ev['out1']))
            db.execute("DELETE FROM event_projects WHERE event_id=?", (self.ev['in1'],))  # Sam never answered: only the owner's
            db.execute("DELETE FROM graph_events WHERE event_id=?", (self.ev['in1'],))
        self.turn_on()
        self.app().follow_up_step()
        acme = [c for c in self.cards() if c['project_id'] == self.acme][0]
        self.assertEqual(acme['n'], 3)  # two quoted earlier sends and this one
        with self.store.connect() as db:
            body = db.execute('SELECT body FROM suggestions WHERE id=?', (acme['suggestion_id'],)).fetchone()[0]
        self.assertEqual(body, 'No reply for 32 days. Follow-up 3 of at most 3.')  # since Sep 16, not since Oct 13

    def test_earlier_sends_at_the_maximum_end_the_round_without_a_new_one(self):
        with self.store.connect() as db:
            db.execute('UPDATE events SET body=? WHERE id=?', (GMAIL_CHAIN, self.ev['out1']))
            db.execute("DELETE FROM event_projects WHERE event_id=?", (self.ev['in1'],))
            db.execute("DELETE FROM graph_events WHERE event_id=?", (self.ev['in1'],))
        self.turn_on(max=2)
        self.app().follow_up_step()
        self.assertEqual([c['project_id'] for c in self.cards()], [self.kim])  # nothing new for Acme
        with self.store.connect() as db:
            end = dict(db.execute('SELECT n,moved FROM follow_up_ends WHERE project_id=?', (self.acme,)).fetchone())
            stage = db.execute('SELECT stage FROM projects WHERE id=?', (self.acme,)).fetchone()[0]
        self.assertEqual((end, stage), ({'n': 2, 'moved': 1}, graph.STALLED))

    def test_a_sealed_store_reads_the_quoted_history_and_without_its_key_drafts_nothing_on_a_guess(self):
        root = Path(self.tmp.name) / 'sealed'
        root.mkdir()
        sealed = a.Store(root / 'events.sqlite', protect=True)
        quoted = {**msg('out1', '2026-10-13T09:00:00+00:00', mine=True), 'body': GMAIL_CHAIN}
        sealed.commit_page('work', {}, [quoted])
        with sealed.connect() as db:
            out1 = db.execute("SELECT id FROM events WHERE source_id='out1'").fetchone()[0]
            self.assertIsInstance(db.execute('SELECT body FROM events WHERE id=?', (out1,)).fetchone()[0], str)  # opened by the store
            board = graph.save_board(db, {'name': 'Alpha testers', 'stages': [{'name': 'Invited'}, {'name': 'Live'}]}, '2026-10-01T09:00:00+00:00')['board_id']
            pid = graph.label(db, [out1], 'Acme pilot', 'review', NOW)
            db.execute("UPDATE projects SET board_id=?,stage='Invited' WHERE id=?", (board, pid))
        raw = __import__('sqlite3').connect(root / 'events.sqlite')
        self.assertIsInstance(raw.execute('SELECT body FROM events WHERE id=?', (out1,)).fetchone()[0], bytes)  # sealed on disk
        raw.close()
        self.store = sealed
        self.turn_on(ref=board)
        with sealed.connect() as db:
            item = [x for x in follow_ups.plan(db, NOW, {'email'}) if x['project']['id'] == pid][0]
        self.assertEqual((item['state'], item['n'], item['prior'], item['counted']), ('due', 3, 2, True))
        # Read without its key (a plain connection to a copy: the body stays sealed bytes): not counted, never a crash
        sqlite3 = __import__('sqlite3')
        raw = sqlite3.connect(root / 'events.sqlite')
        raw.row_factory = sqlite3.Row
        item = [x for x in follow_ups.plan(raw, NOW, {'email'}) if x['project']['id'] == pid][0]
        raw.close()
        self.assertEqual((item['state'], item['n'], item['counted']), ('due', 1, False))

    def test_nothing_is_drafted_before_its_round_could_be_counted(self):
        self.turn_on()
        with patch.object(follow_ups, 'earlier_sends', return_value=(0, None, False)):
            self.assertEqual(self.app().follow_up_step()['drafted'], 0)
        self.assertEqual(self.app().follow_up_step()['drafted'], 2)

    def test_the_collected_emails_in_a_read_thread_are_not_counted_twice(self):
        # Two collected sends (Oct 10, Oct 13): the thread lists Oct 10 before Oct 13, which is the collected one
        self.store.commit_page('work', {}, [msg('out0', '2026-10-10T09:00:00+00:00', mine=True)])
        with self.store.connect() as db:
            out0 = db.execute("SELECT id FROM events WHERE source_id='out0'").fetchone()[0]
            graph.label(db, [out0], 'Acme pilot', 'review', NOW)
            for table in ('event_projects', 'graph_events'):
                db.execute(f'DELETE FROM {table} WHERE event_id=?', (self.ev['in1'],))
            follow_ups.ensure(db)
            db.execute('INSERT INTO follow_up_threads(event_id,sends,at) VALUES(?,?,?)', (self.ev['out1'], json.dumps(['2026-10-10T09:00:00+00:00']), NOW))
        self.turn_on()
        with self.store.connect() as db:
            acme = [x for x in follow_ups.plan(db, NOW, {'email'}) if x['project']['id'] == self.acme][0]
            self.assertEqual((acme['n'], acme['prior'], acme['round_at']), (2, 0, '2026-10-10T09:00:00+00:00'))
            db.execute('UPDATE follow_up_threads SET sends=? WHERE event_id=?', (json.dumps(['2026-10-10T09:00:00+00:00', '2026-09-20T09:00:00+00:00']), self.ev['out1']))
            acme = [x for x in follow_ups.plan(db, NOW, {'email'}) if x['project']['id'] == self.acme][0]
            self.assertEqual((acme['n'], acme['prior'], acme['round_at']), (3, 1, '2026-09-20T09:00:00+00:00'))  # only the one never collected

    def test_the_real_thread_is_preferred_and_read_once(self):
        with self.store.connect() as db:
            db.execute("DELETE FROM event_projects WHERE event_id=?", (self.ev['in1'],))
            db.execute("DELETE FROM graph_events WHERE event_id=?", (self.ev['in1'],))
        head = lambda i, ms, who, labels: {'id': i, 'internalDate': str(ms), 'labelIds': labels, 'payload': {'headers': [{'name': 'From', 'value': who}]}}
        thread = {'messages': [head('old', 1789551093000, 'owner@example.com', ['SENT']), head('out1', 1791882000000, 'owner@example.com', ['SENT'])]}
        self.turn_on()
        with patch.object(a.Gmail, 'get', return_value=thread) as read:
            self.app().follow_up_step()
            self.app().follow_up_step()
        self.assertEqual(sorted(c.args[0] for c in read.call_args_list), ['threads/t1', 'threads/t2'])  # each due thread once
        self.assertEqual(read.call_args.args[1], {'format': 'metadata', 'metadataHeaders': ['From']})
        self.assertEqual([c['n'] for c in self.cards() if c['project_id'] == self.acme], [2])

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

    def drafted_pair(self, app):
        """Both projects' follow-ups drafted through their preparation, as the agent would (no live model, nothing sent)."""
        app.stop_stale_runs = lambda runner: None
        self.assertEqual(app.follow_up_step()['drafted'], 2)
        acme, kim = [c['suggestion_id'] for c in self.cards()]
        first = lambda sid: {'kind': 'email', 'account_id': 'work', 'to': ['sam@client.example' if sid == acme else 'kim@other.example'],
                             'subject': 'Re: Pilot', 'body': 'Hi, here is the case study I mentioned.\n\nRegards,\n\nOwen'}
        return acme, kim, first

    def requeue(self):
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='queued' WHERE status IN ('starting','running','done')")
            db.execute('DELETE FROM preparation_runs')

    def test_the_machine_never_stops_follow_ups_on_its_own_judgment(self):
        self.turn_on(min=0, max=3)
        app = self.app()
        acme, kim, first = self.drafted_pair(app)
        free = (patch.object(a.App, 'follow_up_pause', return_value=None), patch.object(a.App, 'background_pause', return_value=None))
        # Ending the round without a draft is refused: the draft is written anyway
        with free[0], free[1]:
            starts, refused = self.model_turns(app, lambda sid, message, draft: first(sid), next_actions=None, outcome='already_done', follow_up='stop')
        self.assertIn('Either way, write the draft: you never end follow-ups yourself', starts[0]['message'])
        self.assertIn("The owner's word beats any judgment", starts[0]['message'])
        self.assertEqual(sorted(r[0] for r in refused), sorted([acme, kim]))
        self.assertIn("follow_up:'stop' never goes without a draft", refused[0][1])
        # With the draft, and why it would stop
        self.requeue()
        with free[0], free[1]:
            refused = self.model_turns(app, lambda sid, message, draft: first(sid), follow_up='stop')[1]
        self.assertIn('follow_up_why', refused[0][1])
        self.requeue()
        with free[0], free[1]:
            refused = self.model_turns(app, lambda sid, message, draft: first(sid), follow_up='stop', follow_up_why=' 9 unanswered emails\nsince August ')[1]
        self.assertEqual(refused, [])
        with self.store.connect() as db:
            view = follow_ups.cards_view(db, [acme, kim])
        self.assertEqual({view[acme]['advice'], view[kim]['advice']}, {'9 unanswered emails since August'})
        app.follow_up_step()  # never closed by itself
        self.assertEqual([(c['state'], c['status']) for c in self.cards()], [('open', 'prepared'), ('open', 'prepared')])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM follow_up_ends').fetchone()[0], 0)
        # Stop follow-ups here: the owner's pick, on the dashboard; the round ends, nothing sent
        self.assertIn('follow_up_end', a.DASHBOARD_ACTIONS)
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            app.action('follow_up_end', {'id': acme}, owner_dashboard=False)
        with self.assertRaisesRegex(ValueError, 'Say which follow-up'):
            app.action('follow_up_end', {'id': 'nope'}, owner_dashboard=True)
        self.assertEqual(app.action('follow_up_end', {'id': acme}, owner_dashboard=True), {'id': acme, 'state': 'stopped'})
        with self.assertRaisesRegex(ValueError, 'isn’t open anymore'):
            app.action('follow_up_end', {'id': acme}, owner_dashboard=True)
        card = next(c for c in self.cards() if c['suggestion_id'] == acme)
        self.assertEqual((card['state'], card['why'], card['status']), ('stopped', 'owner', 'rejected'))
        self.assertEqual(self.jobs(), [])
        with self.store.connect() as db:
            self.assertEqual(dict(db.execute('SELECT n,moved,judged FROM follow_up_ends WHERE project_id=?', (self.acme,)).fetchone()),
                             {'n': 0, 'moved': 1, 'judged': 0})  # none went out yet
            self.assertEqual(db.execute("SELECT source,feedback FROM decisions WHERE suggestion_id=? AND choice='reject'", (acme,)).fetchone()[:],
                             ('dashboard', 'Follow-ups stopped here.'))
            # Moved to Stalled or declined: it comes back once the owner moves it out again
            self.assertFalse(follow_ups.can_bring_back(db, acme))
            db.execute("UPDATE projects SET stage='Invited' WHERE id=?", (self.acme,))
            self.assertEqual(follow_ups.activity(db, self.acme)[0]['back'], acme)
        app.action('follow_up_bring_back', {'id': acme}, owner_dashboard=True)
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT 1 FROM follow_up_ends WHERE project_id=?', (self.acme,)).fetchone())
        self.assertEqual(next(c['state'] for c in self.cards() if c['suggestion_id'] == acme), 'open')

    def test_the_owners_word_beats_a_judgment_and_a_skip(self):
        self.turn_on(min=0, max=3)
        app = self.app()
        acme, kim, first = self.drafted_pair(app)
        free = (patch.object(a.App, 'follow_up_pause', return_value=None), patch.object(a.App, 'background_pause', return_value=None))
        with free[0], free[1]:
            self.model_turns(app, lambda sid, message, draft: first(sid), follow_up='stop', follow_up_why='No answer to four emails')
        # Skipped in the review (the owner's reject), then "keep trying" in its chat: open again and drafted
        self.store.decide(kim, 'reject', '', 'fr-skip-1', 'dashboard')
        app.follow_up_step()
        self.assertEqual(next(c['state'] for c in self.cards() if c['suggestion_id'] == kim), 'skipped')
        self.store.decide(kim, 'other', 'Keep trying, write one anyway.', 'chat-keep-1', 'dashboard')
        self.assertEqual(next(c['state'] for c in self.cards() if c['suggestion_id'] == kim), 'open')
        self.assertIn("The owner's word beats any judgment", app.follow_up_lines(kim))
        # Its new draft comes without advice: the review checks it as any other
        self.requeue()
        with free[0], free[1]:
            self.assertEqual(self.model_turns(app, lambda sid, message, draft: {**first(sid), 'body': 'Hi Kim, one more idea for Friday.'})[1], [])
        with self.store.connect() as db:
            view = follow_ups.cards_view(db, [acme, kim])
        self.assertNotIn('advice', view[kim])
        # A hard fact is never undone by a message: someone replied, so it stays closed
        with self.store.connect() as db:
            follow_ups.close(db, acme, 'replied', NOW)
        self.store.decide(acme, 'other', 'Keep trying.', 'chat-keep-2', 'dashboard')
        self.assertEqual(next(c['state'] for c in self.cards() if c['suggestion_id'] == acme), 'stopped')

    def test_follow_ups_an_earlier_version_stopped_on_judgment_are_drafted_after_all(self):
        self.turn_on(min=0, max=3, stall=False)
        app = self.app()
        acme, kim, first = self.drafted_pair(app)
        with self.store.connect() as db:  # as the earlier version left them: the round ended on its judgment, the to-dos closed
            for sid, pid in ((acme, self.acme), (kim, self.kim)):
                f = db.execute('SELECT * FROM follow_up_cards WHERE suggestion_id=?', (sid,)).fetchone()
                p = db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
                follow_ups.end(db, {'project': p, 'board': None, 'settings': follow_ups.rule(db, 'board', self.board), 'n': f['n'],
                                    'after': f['after_event'], 'after_at': f['after_at']}, NOW, judged=True)
                follow_ups.close(db, sid, 'judged', NOW)
            db.execute("UPDATE preparations SET status='done'")
        real = follow_ups.messages
        replied = lambda db, pid, mine=follow_ups.mine_default: real(db, pid, mine) + (
            [{'id': 'reply-kim', 'at': '2026-10-28T09:00:00+00:00', 'mine': False, 'channel': 'email'}] if pid == self.kim else [])
        with patch.object(follow_ups, 'messages', side_effect=replied):
            app.follow_up_step()
        cards = {c['suggestion_id']: c for c in self.cards()}
        self.assertEqual((cards[acme]['state'], cards[acme]['status'], cards[acme]['early']), ('open', 'accepted', 1))
        self.assertEqual((cards[kim]['state'], cards[kim]['why']), ('stopped', 'judged'))  # they replied since: nothing to follow up
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT status FROM preparations WHERE suggestion_id=?", (acme,)).fetchone()[0], 'queued')
            self.assertEqual([r[0] for r in db.execute('SELECT project_id FROM follow_up_ends')], [self.kim])
            # An open one whose preparation still said follow_up:'stop' without a draft is drafted too
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?", (json.dumps({'state': 'already_done', 'follow_up': 'stop'}), acme))
            db.execute("UPDATE preparations SET status='done'")
        app.follow_up_step()
        self.assertEqual(next(c['status'] for c in self.cards() if c['suggestion_id'] == acme), 'accepted')
        app.follow_up_step()  # once: nothing left to repair
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM decisions WHERE suggestion_id=? AND choice='prepare_ahead'", (acme,)).fetchone()[0], 3)

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


    # ------------------------------------------------------------------ several in a row: spaced per mailbox

    def batch(self, *senders, kind='email'):
        """Follow-ups of the board, prepared and confirmed by the owner one after the other (Send all checked): one per
        sender given (the From address; the account for other channels). Returns the suggestion ids in that order."""
        sids = []
        with self.store.connect() as db:
            for i, sender in enumerate(senders):
                sid = f'fu-batch-{i}'
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,status) VALUES(?,?,?,?,'[]','[]',?,'prepared')",
                           (sid, 'k' + sid, 'Follow up on Acme pilot', 'No reply for 4 days.', NOW))
                db.execute('INSERT INTO follow_up_cards(suggestion_id,project_id,board_id,grouped,n,of_max,channel,after_event,after_at,created_at) '
                           'VALUES(?,?,?,1,1,3,?,?,?,?)', (sid, self.acme, self.board, kind, 1000 + i, '2026-10-13T09:00:00+00:00', NOW))
                sids.append(sid)
        for sid, sender in zip(sids, senders):
            extra = {'from': sender} if kind == 'email' else {'account_id': sender}
            self.prepared(sid, kind=kind, body='Hi, a short follow-up ' + sid, **extra)
            self.assertEqual(self.store.confirm_action(sid, 'r-' + sid[:6], 'tap-' + sid, 'dashboard')['status'], 'queued')
        return sids

    def outbox(self, transport):
        self.mailbox.online = True
        app = self.app()
        return lambda at: (self.at(at), app.action_step(transport))[1]

    def job_states(self):
        with self.store.connect() as db:
            return {r['suggestion_id']: r['status'] for r in db.execute('SELECT suggestion_id,status FROM action_jobs')}

    def progress(self):
        with self.store.connect() as db:
            return follow_ups.progress(db, a.now())

    def test_the_gap_is_random_within_30_to_45_seconds(self):
        self.assertEqual(follow_ups.gap(lambda lo, hi: lo), 30)
        self.assertLessEqual(follow_ups.gap(lambda lo, hi: hi) + follow_ups.SEND_TICK, 45)  # the outbox's tick still lands it in time
        draws = {round(follow_ups.gap(), 3) for _ in range(50)}
        self.assertTrue(all(30 <= d <= 45 for d in draws) and len(draws) > 1)

    def test_one_mailbox_sends_one_every_gap_and_a_single_send_goes_at_once(self):
        transport = FakeOutbox()
        step = self.outbox(transport)
        sids = self.batch('owner@example.com', 'owner@example.com', 'Owner@Example.com')
        with patch.object(follow_ups, 'gap', return_value=40):
            self.assertEqual(step('2026-10-19T09:00:00+00:00'), 'sent')  # the first goes at once: no wait for a single send
            self.assertIsNone(step('2026-10-19T09:00:03+00:00'))  # the next waits its gap: nothing goes, nothing is lost
            self.assertIsNone(step('2026-10-19T09:00:39+00:00'))
            self.assertEqual(self.progress(), [{'group': 'board:%d' % self.board, 'board': 'Alpha testers', 'batch': self.progress()[0]['batch'], 'total': 3, 'done': 1, 'sent': 1, 'going': True,
                                                'held': 0, 'held_new': 0, 'stopped': 0, 'done_at': '2026-10-19T09:01:17+00:00'}])
            self.assertEqual(step('2026-10-19T09:00:40+00:00'), 'sent')
            self.assertIsNone(step('2026-10-19T09:01:10+00:00'))
            self.assertEqual(step('2026-10-19T09:01:20+00:00'), 'sent')
        self.assertEqual([(sid, at[11:19]) for sid, at in transport.sent], [(sids[0], '09:00:00'), (sids[1], '09:00:40'), (sids[2], '09:01:20')])
        self.assertEqual(self.progress()[0], {'group': 'board:%d' % self.board, 'board': 'Alpha testers', 'batch': self.progress()[0]['batch'], 'total': 3, 'done': 3, 'sent': 3, 'going': False,
                                              'held': 0, 'held_new': 0, 'stopped': 0, 'done_at': None})
        self.at('2026-10-19T09:07:00+00:00')
        self.assertEqual(self.progress(), [])  # "Sent 3" stays a few minutes, then goes

    def test_two_mailboxes_go_side_by_side(self):
        transport = FakeOutbox()
        step = self.outbox(transport)
        a1, a2, b1, l1 = self.batch('owner@example.com', 'owner@example.com', 'sales@example.com', 'sales@example.com')[:4]
        with patch.object(follow_ups, 'gap', return_value=35):
            for at in ('09:00:00', '09:00:03', '09:00:06', '09:00:20', '09:00:35', '09:00:38', '09:00:41'):
                step('2026-10-19T' + at + '+00:00')
        sent = [(sid, at[11:19]) for sid, at in transport.sent]
        self.assertEqual(sent, [(a1, '09:00:00'), (b1, '09:00:03'), (a2, '09:00:35'), (l1, '09:00:38')])
        # Never two from one mailbox less than 30 s apart
        for who in ((a1, a2), (b1, l1)):
            times = [dt.datetime.fromisoformat('2026-10-19T' + at) for sid, at in sent if sid in who]
            self.assertGreaterEqual((times[1] - times[0]).total_seconds(), 30)

    def test_other_channels_are_spaced_the_same_way(self):
        transport = FakeOutbox()
        step = self.outbox(transport)
        self.batch('li', 'li', kind='linkedin')
        with patch.object(follow_ups, 'gap', return_value=31):
            step('2026-10-19T09:00:00+00:00')
            self.assertIsNone(step('2026-10-19T09:00:30+00:00'))
            self.assertEqual(step('2026-10-19T09:00:31+00:00'), 'sent')
        self.assertEqual(len(transport.sent), 2)

    def test_a_restart_or_a_kill_mid_send_resumes_with_the_same_spacing_and_never_sends_twice(self):
        transport = FakeOutbox()
        sids = self.batch('owner@example.com', 'owner@example.com', 'owner@example.com', 'owner@example.com')
        with patch.object(follow_ups, 'gap', return_value=40):
            self.outbox(transport)('2026-10-19T09:00:00+00:00')
            # Killed during the second send (kill -9, a crash, a reboot): it was claimed before the provider call
            transport.die = True
            with self.assertRaises(KeyboardInterrupt):
                self.outbox(transport)('2026-10-19T09:00:40+00:00')
            self.assertEqual(self.job_states()[sids[1]], 'sending')
            # Back up, on a fresh service over the same database (an update opens it the same way): straight after the
            # restart nothing goes inside the gap of the claimed one, and the claimed one is only checked, never sent again
            transport.die = False
            self.store = a.Store(self.store.path)
            step = self.outbox(transport)
            self.assertIsNone(step('2026-10-19T09:00:45+00:00'))
            self.assertEqual(step('2026-10-19T09:01:20+00:00'), 'sent')  # the third, one gap after the claimed one
            self.assertEqual(self.progress()[0]['going'], True)
            transport.in_sent_mail = {sids[1]}  # the Sent folder shows it went out before the kill
            step('2026-10-19T09:02:15+00:00')  # the claimed one is checked once its 90 s are up
            self.assertEqual(self.job_states()[sids[1]], 'sent')
            self.assertEqual(step('2026-10-19T09:02:16+00:00'), 'sent')  # the fourth, one gap after the third
        self.assertEqual([sid for sid, _ in transport.sent], [sids[0], sids[2], sids[3]])
        self.assertEqual(transport.attempts[sids[1]], 1)  # tried once, before the kill
        self.assertEqual(self.progress()[0], {'group': 'board:%d' % self.board, 'board': 'Alpha testers', 'batch': self.progress()[0]['batch'], 'total': 4, 'done': 4, 'sent': 4, 'going': False,
                                              'held': 0, 'held_new': 0, 'stopped': 0, 'done_at': None})

    def test_a_claimed_send_with_no_trace_asks_instead_of_sending_twice(self):
        transport = FakeOutbox(die=True)
        sids = self.batch('owner@example.com', 'owner@example.com')
        with patch.object(follow_ups, 'gap', return_value=40):
            with self.assertRaises(KeyboardInterrupt):
                self.outbox(transport)('2026-10-19T09:00:00+00:00')
            transport.die = False
            self.store = a.Store(self.store.path)
            step = self.outbox(transport)
            self.assertIsNone(step('2026-10-19T09:00:30+00:00'))  # the second still waits the gap after the claimed one
            step('2026-10-19T09:01:31+00:00')  # nothing in Sent mail: uncertain, not sent again
            self.assertEqual(self.job_states()[sids[0]], 'uncertain')
            step('2026-10-19T09:01:32+00:00')
        self.assertEqual([sid for sid, _ in transport.sent], [sids[1]])
        self.assertEqual(transport.attempts[sids[0]], 1)
        # The batch isn't stuck on "Sending…": it ended, one sent; the other to-do says it couldn't confirm it
        self.assertEqual(self.progress()[0]['going'], False)
        self.assertEqual(self.progress()[0]['sent'], 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sids[0],)).fetchone()[0], 'prepared')

    def test_a_failed_send_asks_and_the_rest_of_the_batch_goes_on(self):
        self.turn_on(auto=True)
        transport = FakeOutbox()
        self.app().follow_up_step()
        acme, kim = self.cards()
        self.prepared(acme['suggestion_id'])
        self.prepared(kim['suggestion_id'], to=['kim@other.example'], body='Hi Kim, here is the guide.')
        transport.refuse = {acme['suggestion_id']}
        self.assertEqual(len(self.app().follow_up_send()), 2)  # Send without asking queued both at once
        step = self.outbox(transport)
        with patch.object(follow_ups, 'gap', return_value=40):
            self.assertEqual(step('2026-10-19T09:00:00+00:00'), 'failed')
            self.assertIsNone(step('2026-10-19T09:00:20+00:00'))
            self.assertEqual(step('2026-10-19T09:00:40+00:00'), 'sent')
        self.assertEqual([sid for sid, _ in transport.sent], [kim['suggestion_id']])
        self.assertEqual(self.progress()[0]['sent'], 1)
        self.assertEqual((self.progress()[0]['total'], self.progress()[0]['going']), (2, False))
        # The failed one is a to-do that asks again, with what went wrong
        self.app().follow_up_step()
        with self.store.connect() as db:
            row = db.execute('SELECT s.status,j.error FROM suggestions s JOIN action_jobs j ON j.suggestion_id=s.id WHERE s.id=?', (acme['suggestion_id'],)).fetchone()
        self.assertEqual(row['status'], 'prepared')
        self.assertIn('Nothing was sent', row['error'])
        self.assertEqual({c['project_id']: c['state'] for c in self.cards()}, {self.acme: 'open', self.kim: 'sent'})

    # ------------------------------------------------------------------ Stop sending, and stopped by hand

    def action_status(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            return self.store.suggestion_result(row, db).get('action_status')

    def test_stop_sending_keeps_the_rest_as_drafts_and_never_touches_one_going_out(self):
        transport = FakeOutbox()
        step = self.outbox(transport)
        sids = self.batch(*['owner@example.com'] * 5)
        app = self.app()
        with patch.object(follow_ups, 'gap', return_value=40):
            self.assertEqual(step('2026-10-19T09:00:00+00:00'), 'sent')
            with self.store.connect() as db:  # the second is being sent right now (claimed, provider call under way)
                db.execute("UPDATE action_jobs SET status='sending' WHERE suggestion_id=?", (sids[1],))
            batch = self.progress()[0]['batch']
            with self.assertRaisesRegex(ValueError, 'Only the owner'):
                app.action('follow_up_stop', {'batch': batch}, owner_dashboard=False)
            self.assertIn('follow_up_stop', a.DASHBOARD_ACTIONS)
            self.assertEqual(app.action('follow_up_stop', {'batch': batch}, owner_dashboard=True), {'stopped': 3, 'sent': 1})
            states = self.job_states()
            self.assertEqual([states[s] for s in sids], ['sent', 'sending', 'cancelled', 'cancelled', 'cancelled'])
            # Nothing more goes, also after a restart (a fresh service over the same database)
            self.store = a.Store(self.store.path)
            step = self.outbox(transport)
            for at in ('09:01:00', '09:02:00', '09:03:00'):
                step('2026-10-19T' + at + '+00:00')
        self.assertEqual([sid for sid, _ in transport.sent], [sids[0]])
        p = self.progress()[0]
        self.assertEqual({k: p[k] for k in ('total', 'sent', 'stopped', 'held')}, {'total': 5, 'sent': 1, 'stopped': 3, 'held': 0})
        # The kept ones are drafts to review again: prepared, not a failed send; a new Send queues one again
        with self.store.connect() as db:
            self.assertEqual({db.execute('SELECT status FROM suggestions WHERE id=?', (s,)).fetchone()[0] for s in sids[2:]}, {'prepared'})
        self.assertEqual(self.action_status(sids[2])['status'], 'cancelled')
        self.assertIsNone(self.action_status(sids[2])['error'])
        self.assertEqual(self.send(sids[2], 'again')['status'], 'cancelled')  # the same job, queued again on the new tap
        self.assertEqual(self.job_states()[sids[2]], 'queued')
        with self.assertRaisesRegex(ValueError, 'Nothing left'):
            app.action('follow_up_stop', {'batch': 'nope'}, owner_dashboard=True)

    def test_stopped_by_hand_in_the_outbox_counts_as_a_stop(self):
        sids = self.batch('owner@example.com', 'owner@example.com', 'owner@example.com')
        with self.store.connect() as db:  # what the owner did by hand: blocked, 'Stopped by you'
            db.execute("UPDATE action_jobs SET status='blocked',error='Stopped by you' WHERE suggestion_id IN (?,?)", (sids[1], sids[2]))
            db.execute("UPDATE action_jobs SET status='sent' WHERE suggestion_id=?", (sids[0],))
        self.assertEqual(self.action_status(sids[1])['status'], 'cancelled')  # not shown as a failed send
        p = self.progress()[0]
        self.assertEqual((p['stopped'], p['sent'], p['going'], p['held']), (2, 1, False, 0))
        with self.store.connect() as db:
            follow_ups.settle(db, a.now())
        self.assertEqual(self.job_states()[sids[1]], 'cancelled')
        self.assertEqual(self.progress()[0]['stopped'], 2)

    def test_a_skipped_follow_up_can_be_brought_back_while_it_is_the_latest(self):
        self.turn_on()
        self.app().follow_up_step()
        acme = self.cards()[0]['suggestion_id']
        self.prepared(acme)
        self.store.decide(acme, 'reject', '', 'skip-1', 'dashboard')  # Skip, final when the review closed
        app = self.app()
        app.follow_up_step()
        self.assertEqual(self.cards()[0]['state'], 'skipped')
        with self.store.connect() as db:
            self.assertEqual(follow_ups.activity(db, self.acme)[0]['back'], acme)
            self.assertTrue(follow_ups.cards_view(db, [acme])[acme]['back'])
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            app.action('follow_up_bring_back', {'id': acme}, owner_dashboard=False)
        self.assertIn('follow_up_bring_back', a.DASHBOARD_ACTIONS)
        self.assertEqual(app.action('follow_up_bring_back', {'id': acme}, owner_dashboard=True), {'id': acme, 'status': 'prepared'})
        card = self.cards()[0]
        self.assertEqual((card['state'], card['status']), ('open', 'prepared'))
        with self.store.connect() as db:
            self.assertNotIn('back', follow_ups.activity(db, self.acme)[0])
            draft = json.loads(db.execute('SELECT next_action FROM suggestions WHERE id=?', (acme,)).fetchone()[0])
        self.assertEqual(draft['body'], 'Hi Sam, here is the case study I mentioned.')  # the same draft, to review again
        # Once a newer follow-up came, the old one stays skipped
        self.store.decide(acme, 'reject', '', 'skip-2', 'dashboard')
        app.follow_up_step()
        with self.store.connect() as db:
            db.execute("INSERT INTO follow_up_cards(suggestion_id,project_id,board_id,grouped,n,of_max,channel,after_event,after_at,created_at) "
                       "SELECT 'newer',project_id,board_id,grouped,2,of_max,channel,after_event+1,after_at,? FROM follow_up_cards WHERE suggestion_id=?",
                       ('2026-10-30T09:00:00+00:00', acme))
            self.assertFalse(follow_ups.can_bring_back(db, acme))
        with self.assertRaisesRegex(ValueError, 'can’t come back'):
            app.action('follow_up_bring_back', {'id': acme}, owner_dashboard=True)

    # ------------------------------------------------------------------ nothing new since the draft: checked right before it goes

    def drafted(self, auto=False):
        """Both projects' follow-ups drafted (their basis kept) and prepared: Acme on thread t1, Kim on t2."""
        self.turn_on(auto=auto)
        self.app().follow_up_step()
        acme, kim = self.cards()
        self.prepared(acme['suggestion_id'], thread_id='t1')
        self.prepared(kim['suggestion_id'], to=['kim@other.example'], body='Hi Kim, here is the guide.', thread_id='t2')
        return acme['suggestion_id'], kim['suggestion_id']

    def send(self, sid, approval='tap'):
        return self.store.confirm_action(sid, 'r-' + sid[:6], approval + '-' + sid, 'dashboard')

    def collect(self, source_id, at, mine, thread='t1', project='Acme pilot', who='sam@client.example'):
        """A message the mailbox sync brings in (into the project, as a review labels it)."""
        self.store.commit_page('work', {}, [msg(source_id, at, mine=mine, thread=thread, who=who)])
        with self.store.connect() as db:
            graph.label(db, [db.execute('SELECT id FROM events WHERE source_id=?', (source_id,)).fetchone()[0]], project, 'review', NOW)

    def hold_of(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT j.status,j.error,h.why,s.status card FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id '
                                   'LEFT JOIN follow_up_holds h ON h.job_id=j.id WHERE j.suggestion_id=?', (sid,)).fetchone())

    def test_each_draft_keeps_what_it_was_written_against(self):
        acme, _ = self.drafted()
        with self.store.connect() as db:
            card, found = follow_ups.basis_of(db, acme)
        email = found['channels']['email']
        self.assertEqual((found['id'], found['at']), (self.ev['out1'], '2026-10-13T09:00:00+00:00'))
        self.assertEqual((email['source_id'], email['thread_id'], email['account_id'], email['seen']), ('out1', 't1', 'work', ['in1', 'out1']))
        self.assertEqual(found['id'], card['after_event'])

    def test_an_owner_send_in_between_holds_it_and_counts_as_that_round(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        # The owner wrote in Gmail itself (or another app) after the draft: only the fresh read knows so far
        self.mailbox.add('t1', 'phone1', '2026-10-19T08:30:00+00:00', mine=True)
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual(self.hold_of(acme), {'status': 'blocked', 'error': 'Not sent: new message in the thread.', 'why': 'changed', 'card': 'prepared'})
        # Once the sync brings it in, it counts as that round: this to-do closes and the next follow-up waits from it
        self.collect('phone1', '2026-10-19T08:30:00+00:00', mine=True)
        self.app().follow_up_step()
        card = [c for c in self.cards() if c['project_id'] == self.acme][0]
        self.assertEqual((card['state'], card['why']), ('stopped', 'handled'))
        with self.store.connect() as db:
            item = [x for x in follow_ups.plan(db, a.now(), {'email'}) if x['project']['id'] == self.acme][0]
        self.assertEqual((item['state'], item['n'], item['after_at'], item['next_at']),
                         ('waiting', 2, '2026-10-19T08:30:00+00:00', '2026-10-22T08:30:00+00:00'))

    def test_an_owner_send_already_collected_closes_it_at_once(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.collect('phone1', '2026-10-19T08:30:00+00:00', mine=True)
        self.mailbox.add('t1', 'phone1', '2026-10-19T08:30:00+00:00', mine=True)
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual({c['project_id']: (c['state'], c['why']) for c in self.cards()}[self.acme], ('stopped', 'handled'))

    def test_a_reply_in_between_holds_it_and_ends_the_follow_up(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.collect('in3', '2026-10-19T08:45:00+00:00', mine=False)  # Sam replied (collected; the thread shows it too)
        self.mailbox.add('t1', 'in3', '2026-10-19T08:45:00+00:00', mine=False)
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual({c['project_id']: (c['state'], c['why']) for c in self.cards()}[self.acme], ('stopped', 'replied'))

    def test_a_reply_only_the_fresh_read_shows_holds_it_too(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.mailbox.add('t1', 'in3', '2026-10-19T08:58:00+00:00', mine=False)  # not synced yet
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        with self.store.connect() as db:
            news = json.loads(db.execute('SELECT news FROM follow_up_holds').fetchone()[0])
        self.assertEqual(follow_ups.news_kind(news), 'reply')

    def test_a_teammate_or_anyone_else_in_the_thread_holds_it(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.mailbox.add('t1', 'mate1', '2026-10-19T08:50:00+00:00', mine=False, who='Alex <alex@example.org>')
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])

    def test_a_failed_read_doesnt_send_and_a_new_send_checks_again(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.send(acme)
        self.mailbox.fail = True  # offline, or signed out
        self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.assertEqual(transport.sent, [])
        self.assertEqual(self.hold_of(acme), {'status': 'blocked', 'error': 'Couldn’t check the thread, try again.', 'why': 'unchecked', 'card': 'prepared'})
        self.assertEqual({c['project_id']: c['state'] for c in self.cards()}[self.acme], 'open')  # still ready
        self.assertIsNone(self.outbox(transport)('2026-10-19T09:00:03+00:00'))  # nothing goes by itself
        self.mailbox.fail = False
        self.assertEqual(self.send(acme, 'again')['status'], 'blocked')  # the owner's new Send queues it again...
        self.assertEqual(self.outbox(transport)('2026-10-19T09:01:00+00:00'), 'sent')  # ...checked again, and it goes
        self.assertEqual([sid for sid, _ in transport.sent], [acme])
        self.assertEqual(self.hold_of(acme)['why'], None)

    def test_whatsapp_reads_the_chat_and_a_failed_read_holds_it(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.prepared(acme, kind='whatsapp', account_id='wa', chat_id='3247@s.whatsapp.net', body='Hi Sam, a short follow-up.')
        self.send(acme)
        rows = [{'MsgID': 'w1', 'Timestamp': '2026-10-12T09:00:00Z', 'FromMe': True}]
        with patch.object(a.App, 'follow_up_chat', return_value=rows + [{'MsgID': 'w2', 'Timestamp': '2026-10-19T08:00:00Z', 'FromMe': False}]):
            self.assertEqual(self.outbox(transport)('2026-10-19T09:00:00+00:00'), 'held')
        self.send(acme, 'again')
        with patch.object(a.App, 'follow_up_chat', side_effect=ValueError('I couldn’t reach WhatsApp on this computer.')):
            self.assertEqual(self.outbox(transport)('2026-10-19T09:01:00+00:00'), 'held')
        self.assertEqual(self.hold_of(acme)['why'], 'unchecked')
        self.send(acme, 'third')
        with patch.object(a.App, 'follow_up_chat', return_value=rows):
            self.assertEqual(self.outbox(transport)('2026-10-19T09:02:00+00:00'), 'sent')
        self.assertEqual(len(transport.sent), 1)

    def test_send_all_skips_the_changed_ones_and_sends_the_rest(self):
        transport = FakeOutbox()
        acme, kim = self.drafted()
        self.send(acme), self.send(kim)  # Send all checked: one confirm each
        self.mailbox.add('t2', 'kim-in', '2026-10-19T08:40:00+00:00', mine=False, who='kim@other.example')
        step = self.outbox(transport)
        with patch.object(follow_ups, 'gap', return_value=40):
            results = [step('2026-10-19T09:00:00+00:00'), step('2026-10-19T09:00:40+00:00')]
        self.assertEqual(sorted(results), ['held', 'sent'])
        self.assertEqual([sid for sid, _ in transport.sent], [acme])
        self.assertEqual(self.job_states(), {acme: 'sent', kim: 'blocked'})
        self.assertEqual({k: self.progress()[0][k] for k in ('total', 'sent', 'held', 'held_new', 'going')},
                         {'total': 2, 'sent': 1, 'held': 1, 'held_new': 1, 'going': False})  # "Sent 1 · 1 held (new message)"

    def test_send_without_asking_is_checked_too_and_never_retried_by_itself(self):
        transport = FakeOutbox()
        acme, kim = self.drafted(auto=True)
        self.assertEqual(len(self.app().follow_up_send()), 2)
        self.mailbox.add('t1', 'phone1', '2026-10-19T08:30:00+00:00', mine=True)
        step = self.outbox(transport)
        with patch.object(follow_ups, 'gap', return_value=40):
            step('2026-10-19T09:00:00+00:00'), step('2026-10-19T09:00:40+00:00')
        self.assertEqual([sid for sid, _ in transport.sent], [kim])
        self.assertEqual(self.app().follow_up_send(), [])  # the held one now waits for the owner
        self.assertEqual(self.job_states()[acme], 'blocked')

    def test_a_double_submit_or_a_retry_after_a_restart_sends_once(self):
        transport = FakeOutbox()
        acme, _ = self.drafted()
        self.assertEqual(self.send(acme)['status'], 'queued')
        self.assertTrue(self.send(acme)['duplicate'])  # the same tap twice
        self.assertTrue(self.send(acme, 'other')['duplicate'])  # a second tap while it's queued
        self.store = a.Store(self.store.path)  # a restart
        self.assertTrue(self.send(acme, 'after-restart')['duplicate'])
        self.assertEqual(len(self.jobs()), 1)
        step = self.outbox(transport)
        self.assertEqual(step('2026-10-19T09:00:00+00:00'), 'sent')
        self.assertIsNone(step('2026-10-19T09:00:50+00:00'))
        self.assertTrue(self.send(acme, 'late')['duplicate'])
        self.assertIsNone(step('2026-10-19T09:01:40+00:00'))
        self.assertEqual(transport.attempts, {acme: 1})
        # A held one: the same tap again doesn't queue it twice either
        _, kim = self.cards()[0]['suggestion_id'], self.cards()[1]['suggestion_id']
        self.send(kim)
        self.mailbox.add('t2', 'kim-in', '2026-10-19T09:02:00+00:00', mine=False, who='kim@other.example')
        self.assertEqual(step('2026-10-19T09:03:00+00:00'), 'held')
        self.assertTrue(self.send(kim)['duplicate'])
        self.assertEqual(self.job_states()[kim], 'blocked')
        self.assertIsNone(step('2026-10-19T09:04:00+00:00'))
        self.assertEqual(transport.attempts, {acme: 1})

    def test_reading_what_is_new_in_a_thread_or_chat(self):
        head = lambda i, at, who, labels=(): {'id': i, 'internalDate': str(int(follow_ups.parse(at).timestamp() * 1000)), 'labelIds': list(labels),
                                              'payload': {'headers': [{'name': 'From', 'value': who}]}}
        base = {'at': '2026-10-13T09:00:00+00:00', 'source_id': 'out1', 'seen': ['in1', 'out1']}
        thread = {'messages': [head('in1', '2026-10-08T09:00:00+00:00', 'sam@client.example'), head('out1', '2026-10-13T09:00:01+00:00', 'Me <owner@example.com>'),
                               head('d1', '2026-10-14T09:00:00+00:00', 'owner@example.com', ['DRAFT'])]}
        self.assertEqual(follow_ups.thread_since(thread, base, {'owner@example.com'}), [])  # its own message a second off, a draft: nothing new
        thread['messages'].append(head('n1', '2026-10-15T09:00:00+00:00', 'Me <owner@example.com>'))
        self.assertEqual(follow_ups.news_kind(follow_ups.thread_since(thread, base, {'owner@example.com'})), 'own')
        thread['messages'].append(head('n2', '2026-10-16T09:00:00+00:00', 'Sam <sam@client.example>'))
        self.assertEqual(follow_ups.news_kind(follow_ups.thread_since(thread, base, {'owner@example.com'})), 'reply')
        chat = {'at': '2026-10-13T09:00:00+00:00', 'source_id': 'whatsapp:w1', 'seen': ['whatsapp:w1']}
        self.assertEqual(follow_ups.chat_since([{'MsgID': 'w1', 'Timestamp': '2026-10-13T09:00:00Z', 'FromMe': True}], chat), [])
        self.assertEqual(follow_ups.news_kind(follow_ups.chat_since([{'MsgID': 'w2', 'Timestamp': '2026-10-14T09:00:00Z', 'FromMe': True}], chat)), 'own')
        self.assertIsNone(follow_ups.news_kind([]))


class FakeMailbox:
    """Gmail threads as the fake source answers them: the collected messages of that thread, plus the ones a test adds
    (sent or received elsewhere, not synced yet). `fail` is a read that doesn't work (offline, signed out)."""

    def __init__(self, test):
        self.test, self.online, self.fail, self.extra, self.reads = test, False, False, {}, 0

    def add(self, thread, source_id, at, mine, who='sam@client.example'):
        self.extra.setdefault(thread, []).append(self.head(source_id, at, 'owner@example.com' if mine else who, ['SENT'] if mine else ['INBOX']))

    @staticmethod
    def head(source_id, at, who, labels):
        return {'id': source_id, 'internalDate': str(int(follow_ups.parse(at).timestamp() * 1000)), 'labelIds': labels,
                'payload': {'headers': [{'name': 'From', 'value': who}]}}

    def read(self, account, thread_id):
        self.reads += 1
        if self.fail:
            raise a.SourceError('offline')
        with self.test.store.connect() as db:
            rows = db.execute("SELECT source_id,occurred_at,metadata FROM events WHERE json_extract(metadata,'$.thread_id')=?", (thread_id,)).fetchall()
        known = [self.head(r['source_id'], r['occurred_at'], json.loads(r['metadata'])['from'], json.loads(r['metadata'])['labels']) for r in rows]
        ids = {m['id'] for m in known}
        return {'messages': known + [m for m in self.extra.get(thread_id, []) if m['id'] not in ids]}


class FakeOutbox:
    """The outbox's transports, recorded: no live sends. `die` stops the process mid-send (after the claim, like kill -9)."""

    def __init__(self, die=False):
        self.sent, self.attempts, self.refuse, self.in_sent_mail, self.die = [], {}, set(), set(), die

    def preflight(self, action):
        return None

    def send(self, action, job):
        self.attempts[job['suggestion_id']] = self.attempts.get(job['suggestion_id'], 0) + 1
        if self.die:
            raise KeyboardInterrupt('killed mid-send')
        if job['suggestion_id'] in self.refuse:
            return {'rejected': 550}
        self.sent.append((job['suggestion_id'], a.now()))
        return {'message_id': 'm-' + job['id']}

    def reconcile(self, action, job):
        return {'message_id': 'm-' + job['id']} if job['suggestion_id'] in self.in_sent_mail else {}


if __name__ == '__main__':
    unittest.main()

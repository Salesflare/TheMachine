"""The desktop robot in place of its computer's browser (machine/delivery/desk.py): never both, never a second rule,
and the browser gets it after all when the robot doesn't fetch it. Made-up to-dos, people and links only."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
import meet
import meeting_prep
import notify
import security_levels
from machine.delivery import desk
from machine.sources.calendar import calendar_event

ONE, TWO = 'a' * 32, 'b' * 32
KEYS = {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}
HERE, THERE = 'https://push.example/here', 'https://push.example/there'
CARD = {'id': '0123456789abcdef', 'title': 'Reply to Dana', 'body': 'About Friday.', 'status': 'pending'}
MINE = {'email': 'robin@acme.example', 'self': True, 'responseStatus': 'accepted'}
NOW = dt.datetime(2026, 11, 10, 9, 50, tzinfo=dt.timezone.utc)


class Desk(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        desk.reset(); notify.reset_active(); self.addCleanup(desk.reset)
        self.sent, self.got = [], {}

    def sender(self, request):
        self.sent.append(request)
        return {'results': [{'endpoint': s['endpoint'], 'status': 201} for s in request['subscriptions']]}

    def browser(self, endpoint, computer=None):
        self.app.action('push_subscribe', {'endpoint': endpoint, 'keys': KEYS, 'computer': computer}, owner_dashboard=True)

    def link(self, ident, endpoint):
        self.app.action('push_desk', {'desk': ident, 'endpoint': endpoint}, owner_dashboard=True)

    def push(self, **more):
        self.sent.clear()
        return a.push_notify(self.store, self.config, {**CARD, **more}, self.sender)

    def look(self, ident=ONE, up=True, clock=notify.wall):
        """The robot's: it names what it got the time before."""
        found = desk.look(ident, up, self.got.get(ident, ()), clock)
        self.got[ident] = [n['key'] for n in found]
        return [(n['id'], n['kind']) for n in found]

    def to(self):
        return [s['endpoint'] for r in self.sent for s in r['subscriptions']]

    def test_it_stands_in_for_its_own_computers_browser_only(self):
        self.browser(HERE); self.browser(THERE)
        desk.look(ONE, True)
        self.push()
        self.assertEqual(self.to(), [HERE, THERE])  # whose computer it is isn't known: the browsers, as ever
        self.assertEqual(desk.look(ONE, True), [])
        self.link(ONE, HERE)
        self.push()
        self.assertEqual(self.to(), [THERE])
        self.assertEqual(self.look(), [(CARD['id'], 'todo')])
        self.assertEqual(self.look(), [])  # it said it got it
        desk.look(ONE, False)  # the app is in front, full screen, hidden, Speak up off
        self.push()
        self.assertEqual(self.to(), [HERE, THERE])

    def test_without_any_browser_it_speaks_and_a_computer_with_none_is_known(self):
        desk.look(ONE, True)
        self.assertTrue(self.push())
        self.assertEqual((self.to(), self.look()), ([], [(CARD['id'], 'todo')]))
        self.browser(THERE)
        self.push()
        self.assertEqual((self.to(), self.look()), ([THERE], []))
        self.link(ONE, '')  # its browser has no notifications on: nothing to stand in for
        self.push()
        self.assertEqual((self.to(), len(desk.look(ONE, True))), ([THERE], 1))

    def test_a_browser_that_cannot_be_on_its_computer_is_none(self):
        for agent, runs in (('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'mac'), ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'windows'),
                            ('Mozilla/5.0 (X11; Linux x86_64)', 'linux'), ('Mozilla/5.0 (Linux; Android 15) Mobile', 'other'),
                            ('Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X)', 'other'), ('', None), (None, None)):
            self.assertEqual(desk.computer(agent), runs)
        self.browser(THERE, 'other')
        self.browser(HERE, 'windows')
        desk.look(ONE, True, on='mac')
        self.push()
        self.assertEqual((self.to(), len(desk.look(ONE, True, on='mac'))), ([THERE, HERE], 1))
        desk.look(ONE, True, on='windows')
        with self.store.connect() as db:
            self.assertTrue(desk.maybe(db, ONE))
            self.assertEqual(desk.here(db), {})
            db.execute('UPDATE push_subscriptions SET computer=NULL')  # on before this was kept
            desk.look(ONE, True, on='mac')
            self.assertEqual(desk.here(db), {})

    def test_the_person_says_no_browser_here_until_another_one_is_on(self):
        self.browser(HERE, 'mac')
        self.assertNotIn('browser', self.app.desk_look(ONE, True, on='mac'))  # a robot that doesn't ask
        asked = self.app.desk_look(ONE, True, on='mac', none='0')['browser']
        self.assertEqual(self.app.desk_look(ONE, True, on='mac', none=str(asked)), {'notices': []})
        self.push()
        self.assertEqual(self.to(), [HERE])
        self.assertEqual(len(self.app.desk_look(ONE, True, on='mac', none=str(asked))['notices']), 1)
        with self.store.connect() as db:
            db.execute("UPDATE push_subscriptions SET created_at=? WHERE endpoint=?", (dt.datetime.fromtimestamp(asked + 9, dt.timezone.utc).isoformat(), HERE))
        self.assertEqual(self.app.desk_look(ONE, True, on='mac', none=str(asked))['browser'], asked + 9)
        self.link(ONE, HERE)  # the person opened it there
        self.assertNotIn('browser', self.app.desk_look(ONE, True, on='mac', none=str(asked)))
        desk.look(TWO, True, on='mac')  # another Mac: that browser is the first one's
        with self.store.connect() as db:
            self.assertEqual(desk.here(db), {ONE: {HERE}, TWO: set()})
        self.assertNotIn('browser', self.app.desk_look(ONE, True, on='x', none='1e9; DROP'))

    def test_what_would_not_buzz_is_not_said(self):
        self.browser(HERE); self.link(ONE, HERE); desk.look(ONE, True)
        self.push(_silent=True)  # a batch's later to-dos stay quiet, where they were
        self.assertEqual(self.to(), [HERE])
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(self.push(), [])
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': True}, owner_dashboard=True)
        self.app.action('notify_active', {}, owner_dashboard=True)
        self.assertEqual(self.push(), [])  # a dashboard in use: held, and not said
        notify.reset_active()
        a.push_send(self.store, self.config, [{'endpoint': HERE}], {'title': 't', 'tag': 'fleet-brief'}, 'x', self.sender, kind='result')
        self.assertEqual(self.to(), [HERE])  # the Fleet and the digest: as ever
        self.assertEqual(desk.look(ONE, True), [])

    def test_not_fetched_in_time_the_browser_gets_it_once(self):
        self.browser(HERE); self.link(ONE, HERE)
        clock = [1000.0]
        with patch.object(notify, 'wall', lambda: clock[0]), patch('timeutil.in_hours', lambda *x: True):
            at = lambda: clock[0]
            self.look(clock=at)
            with self.store.connect() as db:
                rest, count = desk.stand_in(db, [{'endpoint': HERE}], {'tag': CARD['id']}, 'todo', at)
            self.assertEqual((rest, count, desk.late(at)), ([], 1, []))
            clock[0] += desk.LATE
            self.assertEqual(self.look(clock=at), [])  # too late for the robot
            self.assertEqual(desk.late(at), [([{'endpoint': HERE}], {'tag': CARD['id']})])
            self.assertEqual(desk.late(at), [])
            with self.store.connect() as db:
                desk.stand_in(db, [{'endpoint': HERE}], {'tag': CARD['id']}, 'todo', at)
            self.look(up=False, clock=at)  # it went quiet before fetching: the browser right away
            self.assertEqual(len(desk.late(at)), 1)
            self.look(clock=at); clock[0] += desk.LEASE
            self.assertEqual(desk.up(at), [])  # gone

    def test_an_answer_lost_on_the_way_comes_again_and_then_the_browser_gets_it(self):
        clock = [1000.0]; at = lambda: clock[0]
        self.browser(HERE); self.link(ONE, HERE)
        def waits():
            with self.store.connect() as db:
                desk.stand_in(db, [{'endpoint': HERE}], {'tag': CARD['id']}, 'todo', at)
        desk.look(ONE, True, (), at); waits()
        first = desk.look(ONE, True, (), at)
        clock[0] += 30
        self.assertEqual(desk.look(ONE, True, (), at), first)  # the same one, by its key: the robot says it once
        clock[0] += 30
        self.assertEqual(desk.look(ONE, False, [first[0]['key']], at), [])  # it has it, and may not speak now
        clock[0] += desk.LATE
        self.assertEqual(desk.late(at), [])
        desk.look(ONE, True, (), at); waits()
        (again,) = desk.look(ONE, True, (), at)
        self.assertNotEqual(again['key'], first[0]['key'])  # another notification of the same to-do is another one
        clock[0] += desk.LATE
        desk.look(ONE, True, [first[0]['key']], at)
        self.assertEqual(len(desk.late(at)), 1)  # handed out, never named

    def test_without_a_browser_on_its_computer_it_waits_longer_for_the_robot(self):
        clock = [1000.0]; at = lambda: clock[0]
        self.link(ONE, '')
        def waits():
            with self.store.connect() as db:
                desk.stand_in(db, [], {'tag': CARD['id']}, 'todo', at)
        desk.look(ONE, True, (), at); waits()
        (first,) = desk.look(ONE, True, (), at)  # its box is open: not shown, so not named
        clock[0] += desk.LATE + 30
        self.assertEqual((desk.late(at), desk.look(ONE, True, (), at)), ([], [first]))
        self.assertEqual((desk.look(ONE, False, (), at), desk.late(at)), ([], []))  # a full-screen while
        self.assertEqual(desk.look(ONE, True, (), at), [first])
        self.assertEqual(desk.look(ONE, True, [first['key']], at), [])
        waits(); clock[0] += desk.KEEP  # not for ever
        self.assertEqual((desk.look(ONE, True, (), at), desk.late(at)), ([], []))

    def test_the_late_one_is_pushed_by_the_step(self):
        self.browser(HERE); self.link(ONE, HERE); desk.look(ONE, True)
        self.push(); desk.look(ONE, False)
        self.app.notify_step(push=self.sender)
        self.assertEqual((self.to(), self.sent[-1]['payload']['tag']), ([HERE], CARD['id']))

    def test_only_the_dashboard_links_and_the_links_stay_few(self):
        with self.assertRaises(ValueError):
            self.app.action('push_desk', {'desk': ONE, 'endpoint': HERE})
        for bad in ({'desk': 'x', 'endpoint': HERE}, {'desk': ONE, 'endpoint': 'http://plain.example'}):
            with self.assertRaises(ValueError):
                self.app.action('push_desk', bad, owner_dashboard=True)
        for i in range(desk.LINKS + 5):
            self.link(f'{i:032x}', HERE)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM notify_desks').fetchone()[0], desk.LINKS)
        for i in range(desk.DESKS + 5):
            desk.look(f'{i:032x}', True)
        self.assertEqual(len(desk.up()), desk.DESKS)
        self.assertEqual(desk.look('not-an-id', True), [])

    def event(self, meta=None, body='', start='2026-11-10T10:00:00+00:00', status='pending', verdict='made'):
        with self.store.connect() as db:
            meeting_prep.ensure(db)
            self.put(db, 'events', id=7, account_id='cal', source_id='e7', kind='calendar.event', occurred_at=start, title='Pilot review', body=body, deleted=0,
                     metadata=json.dumps({'attendees': [MINE, {'email': 'dana@globex.example', 'displayName': 'Dana Rivera'}], **(meta or {})}))
            self.put(db, 'suggestions', id=CARD['id'], title='Prepare for the pilot review', body='', status=status)
            db.execute("INSERT INTO meeting_preps(dedupe_key,event_id,suggestion_id,verdict,starts_at,created_at) VALUES('k',7,?,?,?,?)",
                       (CARD['id'], verdict, start, start))

    def put(self, db, table, **row):
        row |= {c[1]: '[]' if 'ids' in c[1] else '' for c in db.execute(f'PRAGMA table_info({table})') if c[3] and c[4] is None and c[1] not in row}
        db.execute(f"INSERT INTO {table}({','.join(row)}) VALUES({','.join('?' * len(row))})", tuple(row.values()))

    def meeting(self, current=NOW):
        with self.store.connect() as db:
            return desk.meeting(db, current, lambda: ({'robin@acme.example'}, {'acme.example'}), ('rejected',))

    def test_a_meeting_with_a_briefing_about_to_start(self):
        self.assertIsNone(self.meeting())  # none prepared yet
        self.event(body='Join: https://us02web.zoom.us/u/kx1 or https://us02web.zoom.us/j/8412?pwd=a.')
        found = self.meeting()
        self.assertEqual((found['id'], found['who'], found['others'], found['title'], found['join']), (CARD['id'], 'Dana', 0, 'Pilot review', 'https://us02web.zoom.us/j/8412?pwd=a'))
        self.assertIsNone(self.meeting(NOW - dt.timedelta(minutes=1)))  # not yet
        self.assertIsNone(self.meeting(NOW + dt.timedelta(minutes=10)))  # started
        with self.store.connect() as db:
            security_levels.set_pref(db, 'notify_text', 'off')
        self.assertEqual((self.meeting()['who'], self.meeting()['title']), ('', ''))
        self.app.action('notify_set', {'kind': 'reminder', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertIsNone(self.meeting())

    def test_a_meeting_whose_guests_have_no_name_has_its_own(self):
        self.event({'attendees': [MINE, {'email': 'dana@globex.example'}, {'email': 'lee@globex.example', 'displayName': 'lee@globex.example'}]})
        found = self.meeting()
        self.assertEqual((found['who'], found['others'], found['title']), ('', 0, 'Pilot review'))  # never a name it would be with

    def test_not_one_canceled_declined_all_day_unwanted_or_without_a_briefing(self):
        for case in ({'meta': {'status': 'cancelled'}}, {'meta': {'attendees': [{**MINE, 'responseStatus': 'declined'}]}}, {'meta': {'all_day': True}},
                     {'status': 'rejected'}, {'verdict': 'nothing'}):
            with self.subTest(case):
                self.event(**case)
                self.assertIsNone(self.meeting())
                with self.store.connect() as db:
                    for table in ('events', 'suggestions', 'meeting_preps'):
                        db.execute(f'DELETE FROM {table}')

    def test_a_calendars_call_link_is_kept_beside_never_a_new_version(self):
        account = {'id': 'cal', 'source': 'calendar'}
        raw = {'id': 'e1', 'summary': 'Pilot review', 'updated': '2026-11-09T10:00:00Z', 'start': {'dateTime': '2026-11-10T10:00:00Z'}, 'end': {'dateTime': '2026-11-10T11:00:00Z'}}
        link = 'https://meet.google.com/abc-defg-hij'
        def synced(more):
            event = calendar_event(account, {**raw, **more}, 'UTC')
            self.store.commit_page(account['id'], {}, [event])
            with self.store.connect() as db:
                row = db.execute('SELECT version,analyzed_version,metadata FROM events').fetchone()
            return row['version'], row['analyzed_version'], json.loads(row['metadata']).get('video')
        first = synced({})
        self.assertEqual(first[2], None)
        self.assertEqual(synced({'hangoutLink': link}), (*first[:2], link))
        self.assertEqual(synced({}), first)  # gone again: gone here too
        self.assertGreater(synced({'summary': 'Pilot review, part two'})[0], first[0])

    def test_the_join_link_is_a_known_services_own(self):
        for url in ('https://meet.google.com/abc-defg-hij', 'https://teams.microsoft.com/l/meetup-join/19%3ax/0?c=1', 'https://teams.live.com/meet/93', 'https://zoom.us/j/1'):
            self.assertEqual(meet.video_link(f'see <{url}>, thanks'), url)
        for bad in ('http://zoom.us/j/1', 'https://zoom.us.evil.example/j/1', 'https://evilzoom.us/j/1', 'https://zoom.us@evil.example/j/1', 'https://a:b@zoom.us/j/1',
                    'https://zoom.us:8443/j/1', 'https://evil.example/?u=https://zoom.us/j/1', 'https://zoom.us/test', 'https://meet.google.com/landing', ''):
            self.assertIsNone(meet.video_link(bad), bad)

    def test_the_look_hands_it_out_and_the_status_itself_stays_the_same(self):
        self.assertEqual(self.app.desk_look('', True), {})
        self.assertEqual(self.app.desk_look(ONE, False), {})
        self.assertEqual(self.app.desk_look(ONE, True), {'notices': []})
        self.push()
        (said,) = self.app.desk_look(ONE, True)['notices']
        self.assertEqual((said['id'], [option for option, _ in said['snooze']][0], said['snooze']), (CARD['id'], '2h', a.snooze_choices()))


if __name__ == '__main__':
    unittest.main()

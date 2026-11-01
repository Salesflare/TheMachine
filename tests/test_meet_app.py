"""Scheduling between Machines, the App's part (meet_app.py): a meeting request only looks up an address from the
to-do's own evidence, the other side's to-do, Book it as the owner's own calendar write with the invite, and the
owner's taps and setting from the dashboard only. Synthetic data only: a stand-in Fleet, no Network, no calendar
write reaches Google."""
import json
from pathlib import Path
import tempfile
import threading
import unittest

import meet
import test_preparation as p

a = p.a

OWN = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'transport': 'gog', 'client': 'c', 'boundary': 'work:Example'}
MAIL = {'id': 'mail', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'client': 'c', 'boundary': 'work:Example'}
CONFIG = {'accounts': [MAIL, OWN], 'gog': '/bin/false', 'credentials': {}}


class StandInFleet:
    """Records what the app asks of meet.py."""
    meet_on = True

    def __init__(self):
        self.started, self.decided, self.set = [], [], []
        self.done = threading.Event()

    def meet_start(self, card_id, email, name='', **kw):
        self.started.append((card_id, email, name, kw))
        self.done.set()

    def meet_decide(self, card_id, choice):
        self.decided.append((card_id, choice))
        return {'state': 'proposed'}

    def meet_setting(self):
        return {'allow': 'freebusy', 'minutes': 30}

    def meet_set(self, **change):
        self.set.append(change)
        return {'allow': change.get('allow', 'freebusy')}


class MeetApp(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App);self.app.store, self.app.config = self.store, CONFIG
        self.app.fleet = StandInFleet()
        self.writes = []
        self.app.calendar_write = lambda args: self.writes.append(args) or {'status': 'done'}
        with self.store.connect() as db:
            db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                       "VALUES('mail','m1','gmail.message','2026-11-01T09:00:00Z','Next week','Shall we meet next week?',?,0,'h',1,1,'2026-11-01T09:00:00Z')",
                       (json.dumps({'from': 'Alex Example <alex@example.org>', 'to': 'owner@example.com', 'cc': 'sam@example.net'}),))
            self.event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]

    def begin(self, request):
        state = self.app.meet_begin('card-1', request, [self.event])
        if state:
            self.assertTrue(self.app.fleet.done.wait(5))
        return state

    def test_asks_only_an_address_from_the_to_dos_own_evidence(self):
        self.assertEqual(self.begin({'with': 'Alex@Example.org', 'name': 'Alex', 'minutes': 30}), 'asking')
        self.assertEqual(self.app.fleet.started, [('card-1', 'alex@example.org', 'Alex', {'minutes': 30, 'start': None, 'days': None})])
        self.app.fleet.started.clear()
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'someone@example.com'}, [self.event]))  # not on the thread
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'owner@example.com'}, [self.event]))  # the owner themselves
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'alex@example.org'}, []))  # no evidence
        self.assertIsNone(self.app.meet_begin('card-1', 'alex@example.org', [self.event]))
        self.assertEqual(self.app.fleet.started, [])

    def test_odd_lengths_and_windows_are_left_to_the_settings(self):
        self.begin({'with': 'sam@example.net', 'minutes': 17, 'days': True, 'start': '2026-11-03T10:00'})
        self.assertEqual(self.app.fleet.started[0][3], {'minutes': None, 'start': '2026-11-03', 'days': None})

    def test_nothing_is_asked_without_a_calendar_that_sends_invites_or_off_the_network(self):
        self.app.config = {'accounts': [MAIL]}
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'alex@example.org'}, [self.event]))
        self.app.config = CONFIG
        self.app.fleet.meet_on = False
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'alex@example.org'}, [self.event]))
        self.app.fleet = None
        self.assertIsNone(self.app.meet_begin('card-1', {'with': 'alex@example.org'}, [self.event]))
        with self.assertRaisesRegex(ValueError, 'not on The Machine Network'):
            self.app.action('meet_setting', {}, owner_dashboard=True)

    def test_the_other_sides_to_do_is_one_reviewed_event_and_one_to_do(self):
        session = {'id': 's1', 'name': 'Alex', 'email': 'alex@example.org', 'title': 'Meet Alex Tue 3 Nov 14:00, 30 min, Zoom?'}
        card = self.app.meet_card(session)
        self.assertEqual(self.app.meet_card(session), card)  # the same session, the same to-do
        with self.store.connect() as db:
            rows = db.execute("SELECT kind,analyzed_version,title FROM events WHERE source_id='meet:s1'").fetchall()
            title = db.execute('SELECT title FROM suggestions WHERE id=?', (card,)).fetchone()[0]
        self.assertEqual([tuple(r) for r in rows], [('meet.request', 1, session['title'])])
        self.assertEqual(title, session['title'])

    def test_book_it_is_the_owners_own_calendar_write_with_the_invite(self):
        session = {'id': 's1', 'name': 'Alex', 'email': 'alex@example.org', 'video': 'zoom',
                   'slot': json.dumps(['2026-11-03T13:00Z', '2026-11-03T13:30Z'])}
        self.assertEqual(self.app.meet_book(session), {'status': 'done'})
        self.app.meet_book(session)
        first, again = self.writes
        self.assertEqual(first['request_id'], again['request_id'])  # books once
        self.assertRegex(first['request_id'], r'^[a-f0-9]{32}$')
        self.assertEqual((first['op'], first['calendar'], first['guests'], first['invite']), ('create', 'cal', ['alex@example.org'], 1))
        self.assertEqual((first['start'][:16], first['end'][:16]), ('2026-11-03T13:00', '2026-11-03T13:30'))
        self.assertEqual(first['title'], 'Meeting with Alex')
        self.assertEqual(first['notes'], 'Video: Zoom')
        self.app.config = {'accounts': [MAIL]}
        self.assertEqual(self.app.meet_book(session)['status'], 'failed')
        self.assertEqual(len(self.writes), 2)

    def test_taps_are_the_owners_own_from_the_dashboard(self):
        with self.assertRaisesRegex(ValueError, 'your own taps'):
            self.app.action('meet_decide', {'suggestion_id': 'card-1', 'choice': 'book'})
        self.assertEqual(self.app.action('meet_decide', {'suggestion_id': 'card-1', 'choice': 'book'}, owner_dashboard=True), {'state': 'proposed'})
        self.assertEqual(self.app.fleet.decided, [('card-1', 'book')])

    def test_the_setting_is_read_anywhere_and_changed_in_the_dashboard(self):
        self.assertEqual(self.app.action('meet_setting', {})['allow'], 'freebusy')
        with self.assertRaisesRegex(ValueError, 'changed in the dashboard'):
            self.app.action('meet_setting', {'allow': 'off'})
        self.assertEqual(self.app.action('meet_setting', {'allow': 'off', 'minutes': 45, 'other': 1}, owner_dashboard=True), {'allow': 'off'})
        self.assertEqual(self.app.fleet.set, [{'allow': 'off', 'minutes': 45}])

    def test_activity_links_each_exchange_to_its_to_do_by_title(self):
        card = self.app.meet_card({'id': 's1', 'name': 'Alex', 'email': 'alex@example.org', 'title': 'Meet Alex Tue 3 Nov 14:00, 30 min?'})
        with self.store.connect() as db:
            meet.ensure(db)
            db.execute("INSERT INTO meet_log(at,direction,what,name,args,outcome,card_id) VALUES('2026-11-01T09:00:00Z','in','proposed_in','Alex','[\"Tue 3 Nov 14:00\"]','answered',?)", (card,))
            line = meet.activity_lines(db, 5)[0]
        self.assertEqual(line['todo'], {'id': card, 'title': 'Meet Alex Tue 3 Nov 14:00, 30 min?'})
        self.assertNotIn('Zoom', json.dumps(line))

    def test_closing_the_to_do_is_quiet_when_it_is_gone(self):
        self.app.meet_close('no-such-card', 'booked')


if __name__ == '__main__':
    unittest.main()

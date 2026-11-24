"""Free/busy (calendar_busy.py, friends.free_busy): what takes time, and the times this Machine doesn't know, which are
never free and never busy. Made-up events, a pinned clock."""
import datetime as dt
import json
import sqlite3
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import calendar_busy
import calendar_clashes
import calendar_writes
import ews_calendar
import friends
import ical
import machine.main as machine_main
import machine.sources.calendar as machine_sources_calendar
import machine.sources.connectors as machine_sources_connectors
import ms_graph
import sources
import timeutil
from seams import patch_everywhere

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 11, 24, 9, 0, tzinfo=UTC)
MAIL = {'id': 'mail', 'service': 'gmail', 'email': 'me@one.example'}
CAL = {'id': 'cal', 'service': 'calendar', 'email': 'me@one.example', 'calendar_id': 'primary'}
ASK = {'start': '2026-12-01', 'days': 3}
ALL = [['2026-11-30T10:00Z', '2026-12-04T14:00Z']]  # the days asked, in any time zone


def state(until=30, **more):
    return {'mode': 'incremental', 'read_from': (NOW - dt.timedelta(days=7)).isoformat(),
            'read_until': (NOW + dt.timedelta(days=until)).isoformat(), **more}


class Pinned(unittest.TestCase):
    def setUp(self):
        timeutil.pin(NOW)
        self.addCleanup(timeutil.pin, None)
        local = timeutil.LOCAL_TZ
        timeutil.LOCAL_TZ = UTC
        self.addCleanup(setattr, timeutil, 'LOCAL_TZ', local)


class FreeBusy(Pinned):
    def setUp(self):
        super().setUp()
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('CREATE TABLE events(account_id TEXT,kind TEXT,occurred_at TEXT,metadata TEXT,deleted INT DEFAULT 0);'
                              'CREATE TABLE checkpoints(account_id TEXT PRIMARY KEY,state TEXT,last_success TEXT,error TEXT)')

    def read(self, account='cal', hours_ago=0, error=None, **over):
        self.db.execute('INSERT OR REPLACE INTO checkpoints VALUES(?,?,?,?)',
                        (account, json.dumps(over.get('state', state())), (NOW - dt.timedelta(hours=hours_ago)).isoformat(), error))

    def add(self, start, end, account='cal', **meta):
        self.db.execute('INSERT INTO events(account_id,kind,occurred_at,metadata) VALUES(?,?,?,?)',
                        (account, 'calendar.event', start + ':00+00:00', json.dumps({'end_at': end + ':00+00:00', 'title': 'Dentist', **meta})))

    def told(self, accounts=(MAIL, CAL), ask=ASK):
        answer = friends.free_busy(self.db, {'accounts': list(accounts)}, ask)
        self.assertEqual(set(answer), {'busy', 'unknown'})
        self.assertNotIn('Dentist', json.dumps(answer))
        return answer['busy'], answer['unknown']

    def test_a_read_calendar_tells_its_busy_times(self):
        self.read()
        self.add('2026-12-01T10:00', '2026-12-01T16:00')
        self.add('2026-12-02T10:00', '2026-12-02T11:00', status='cancelled')
        self.add('2026-12-02T12:00', '2026-12-02T13:00', attendees=[{'self': True, 'responseStatus': 'declined'}])
        self.assertEqual(self.told(), ([['2026-12-01T10:00Z', '2026-12-01T16:00Z']], []))

    def test_no_calendar_or_one_that_was_removed_is_not_known(self):
        self.assertEqual(self.told([MAIL]), ([], ALL))
        self.read()
        self.add('2026-12-01T10:00', '2026-12-01T16:00')
        self.assertEqual(self.told([MAIL]), ([], ALL))  # disconnected: its events are still here, nobody reads it

    def test_a_calendar_never_read_is_not_known(self):
        self.assertEqual(self.told(), ([], ALL))
        self.read(state={'mode': 'bootstrap', 'time_min': '2026-11-17T00:00:00+00:00', 'time_max': '2026-12-24T00:00:00+00:00'})
        self.assertEqual(self.told(), ([], ALL))  # its first pages only
        self.db.execute('DROP TABLE checkpoints')
        self.assertEqual(self.told(), ([], ALL))

    def test_a_momentary_failure_changes_nothing_and_a_day_without_a_read_does(self):
        self.add('2026-12-01T10:00', '2026-12-01T16:00')
        self.read(hours_ago=3, error='timeout')
        self.assertEqual(self.told()[1], [])
        self.read(hours_ago=25, error='invalid_grant')
        self.assertEqual(self.told(), ([], ALL))  # what it said then isn't said as busy either

    def test_days_past_what_was_read_are_not_known(self):
        self.read()
        self.add('2026-12-23T10:00', '2026-12-23T11:00')
        self.add('2027-01-05T10:00', '2027-01-05T11:00')  # moved there: kept, past what was read
        ask = {'start': '2026-12-22', 'days': 14}
        busy, unknown = self.told(ask=ask)
        self.assertEqual(busy[0], ['2026-12-23T10:00Z', '2026-12-23T11:00Z'])
        self.assertEqual(unknown, [['2026-12-24T09:00Z', '2027-01-05T14:00Z']])
        self.read(state={'mode': 'incremental', 'time_min': '2026-11-17T09:00:00+00:00', 'time_max': '2026-12-24T09:00:00+00:00'})
        self.assertEqual(self.told(ask=ask)[1], unknown)  # read before this was kept

    def test_every_calendar_of_the_owners_own_has_to_be_known(self):
        two = {'id': 'cal2', 'service': 'caldav', 'email': 'me@two.example'}
        self.read()
        self.add('2026-12-01T10:00', '2026-12-01T16:00')
        self.assertEqual(self.told([CAL, two])[1], ALL)
        self.read('cal2')
        self.assertEqual(self.told([CAL, two])[1], [])
        # someone else's calendar, one from a Fleet and one that only does actions are never asked for
        others = [{'id': 'x1', 'service': 'calendar', 'email': 'me@one.example', 'calendar_id': 'sam@one.example'},
                  {'id': 'x2', 'service': 'calendar', 'email': 'me@one.example', 'shared': True},
                  {'id': 'x3', 'service': 'calendar', 'email': 'me@one.example', 'signals': False}]
        self.assertEqual(self.told([CAL, *others])[1], [])
        self.assertEqual(self.told(others), ([], ALL))

    def test_an_all_day_event_marked_busy_is_busy(self):
        self.read()
        self.add('2026-12-01T00:00', '2026-12-04T00:00', all_day=True, transparency='opaque')
        self.assertEqual(self.told()[0], [['2026-12-01T00:00Z', '2026-12-04T00:00Z']])

    def test_an_all_day_event_that_is_free_or_does_not_say_is_not(self):
        self.read()
        self.add('2026-12-01T00:00', '2026-12-02T00:00', all_day=True, transparency='transparent')
        self.add('2026-12-02T00:00', '2026-12-03T00:00', all_day=True)
        self.assertEqual(self.told(), ([], []))

    def test_a_timed_event_marked_free_is_free_here_and_in_clashes(self):
        self.read()
        self.add('2026-12-01T09:00', '2026-12-01T18:00', transparency='transparent')
        self.assertEqual(self.told(), ([], []))
        timed = {'status': 'confirmed'}
        for meta, busy in ((timed, True), ({**timed, 'transparency': 'transparent'}, False)):
            self.assertEqual((calendar_busy.blocks(meta), calendar_clashes.firm(meta, lambda _: True)), (busy, busy))
        self.assertFalse(calendar_clashes.firm({'all_day': True, 'transparency': 'opaque'}, lambda _: True))  # never a clash, as before

    def test_one_that_began_months_ago_still_takes_the_day(self):
        self.read()
        self.add('2026-08-01T00:00', '2027-02-01T00:00', all_day=True, transparency='opaque')
        self.assertEqual(self.told()[0], ALL)

    def test_more_blocks_than_fit_are_not_free(self):
        self.read()
        for n in range(friends.MAX_BLOCKS + 5):
            at = dt.datetime(2026, 12, 1, tzinfo=UTC) + dt.timedelta(minutes=10 * n)
            self.add(at.isoformat()[:16], (at + dt.timedelta(minutes=5)).isoformat()[:16])
        busy, unknown = self.told()
        self.assertEqual((len(busy), unknown), (friends.MAX_BLOCKS, [['2026-12-03T02:00Z', ALL[0][1]]]))

    # -- both directions between an older Machine and a new one
    def test_an_older_asker_gets_no_answer_rather_than_a_wrong_free(self):
        old, new = friends.parse_availability(ASK), friends.parse_availability({**ASK, 'unknown': True, 'title': 'x'})
        self.assertEqual((old, new), (ASK, {**ASK, 'unknown': True}))
        part = {'busy': [], 'unknown': [['2026-12-03T00:00Z', '2026-12-04T14:00Z']]}
        past = {'busy': [], 'unknown': [['2026-11-20T00:00Z', '2026-11-21T00:00Z']]}
        self.assertIsNone(friends.sendable(old, part))
        self.assertEqual(friends.sendable(new, part), part)
        for answer in (past, {'busy': [], 'unknown': []}):
            self.assertEqual(friends.sendable(old, answer), answer)

    def test_an_older_answer_is_never_read_as_free(self):
        def unknown(answer, ask=ASK):
            return friends.unknown_in(ask, friends.clean_availability(answer), NOW, UTC)
        whole = [(dt.datetime(2026, 12, 1, tzinfo=UTC), dt.datetime(2026, 12, 4, tzinfo=UTC))]
        self.assertEqual(unknown({'busy': []}), (whole, True))  # nothing busy may as well be no calendar
        busy = {'busy': [['2026-12-01T10:00Z', '2026-12-01T11:00Z']]}
        self.assertEqual(unknown(busy), ([], False))
        late = unknown(busy, {'start': '2026-12-22', 'days': 7})
        self.assertEqual(late, ([(NOW + dt.timedelta(days=30), dt.datetime(2026, 12, 29, tzinfo=UTC))], False))
        self.assertEqual(unknown({'busy': [], 'unknown': []}), ([], False))
        self.assertEqual(unknown({'busy': [], 'unknown': ALL}), (whole, True))
        self.assertEqual(unknown({'busy': [], 'unknown': [['2026-12-01T00:00Z', 'Dentist'], {'why': 'x'}]}), ([], False))  # only its shape

    def test_the_activity_line(self):
        self.assertEqual(friends.answer_text({'busy': [], 'unknown': []}), 'free the whole time')
        for answer in ({'busy': []}, {'busy': [], 'unknown': ALL}):
            self.assertNotIn('free', friends.answer_text(answer))
        self.assertIn('not all of it is known', friends.answer_text({'busy': [['2026-12-01T10:00Z', '2026-12-01T11:00Z']], 'unknown': ALL}))


class Sources(Pinned):
    """Whether an all-day event is Busy, as each kind of calendar says it."""

    def kept(self, item):
        return machine_sources_calendar.calendar_event(CAL, item, 'UTC')['metadata'].get('transparency')

    def test_google(self):
        day = {'id': 'e', 'start': {'date': '2026-12-01'}, 'end': {'date': '2026-12-02'}}
        timed = {'id': 'e', 'start': {'dateTime': '2026-12-01T10:00:00Z'}, 'end': {'dateTime': '2026-12-01T11:00:00Z'}}
        self.assertEqual(self.kept(day), 'opaque')  # Google leaves Busy out
        self.assertEqual(self.kept({**day, 'transparency': 'transparent'}), 'transparent')
        for kind in ('birthday', 'workingLocation'):
            self.assertIsNone(self.kept({**day, 'eventType': kind}))
        self.assertIsNone(self.kept(timed))
        self.assertEqual(self.kept({**timed, 'transparency': 'transparent'}), 'transparent')

    def test_outlook(self):
        raw = {'id': 'e', 'isAllDay': True, 'start': {'dateTime': '2026-12-01T00:00:00', 'timeZone': 'UTC'},
               'end': {'dateTime': '2026-12-02T00:00:00', 'timeZone': 'UTC'}}
        for shown, kept in (('busy', 'opaque'), ('oof', 'opaque'), ('free', 'transparent'), ('tentative', None), ('workingElsewhere', None), ('unknown', None)):
            self.assertEqual(self.kept(ms_graph.calendar_item({**raw, 'showAs': shown}, 'me@one.example')), kept, shown)

    def test_exchange(self):
        for shown, kept in (('Busy', 'opaque'), ('OOF', 'opaque'), ('Free', 'transparent'), ('Tentative', None), ('NoData', None)):
            element = ET.fromstring(f'<t:CalendarItem xmlns:t="{ews_calendar.T}"><t:ItemId Id="i"/><t:Subject>Away</t:Subject>'
                                    '<t:Start>2026-12-01T00:00:00Z</t:Start><t:End>2026-12-02T00:00:00Z</t:End><t:IsAllDayEvent>true</t:IsAllDayEvent>'
                                    f'<t:UID>u</t:UID><t:LegacyFreeBusyStatus>{shown}</t:LegacyFreeBusyStatus></t:CalendarItem>')
            self.assertEqual(self.kept(ews_calendar.item_of(element, {'me@one.example'})), kept, shown)

    def test_icalendar(self):
        for line, kept in (('TRANSP:OPAQUE\r\n', 'opaque'), ('TRANSP:TRANSPARENT\r\n', 'transparent'), ('', None)):  # left out: as before
            text = ('BEGIN:VCALENDAR\r\nBEGIN:VEVENT\r\nUID:u\r\nDTSTART;VALUE=DATE:20261201\r\nDTEND;VALUE=DATE:20261202\r\nSUMMARY:Away\r\n'
                    + line + 'END:VEVENT\r\nEND:VCALENDAR\r\n')
            items, _ = ical.window_items([text], NOW, NOW + dt.timedelta(days=30))
            self.assertEqual([self.kept(i) for i in items], [kept], line)

    def test_an_all_day_event_the_machine_adds_is_free_unless_the_owner_is_away(self):
        config = {'accounts': [{**CAL, 'transport': 'gog'}]}
        add = {'kind': 'calendar', 'op': 'create', 'calendar': 'cal', 'title': 'Trip', 'start': '2026-12-01', 'end': '2026-12-02', 'all_day': True}
        timed = {**add, 'all_day': False, 'start': '2026-12-01T10:00:00+00:00', 'end': '2026-12-01T11:00:00+00:00'}

        def written(value, events=None):
            action = calendar_writes.validate(value, config, events)
            return calendar_writes.body(action, 'k').get('transparency'), action['when'].rpartition(', ')[2]
        for value, sent in ((add, 'transparent'), ({**add, 'busy': False}, 'transparent'), ({**add, 'busy': True}, 'opaque')):
            self.assertEqual(written(value)[0], sent)
        self.assertEqual(written({**add, 'busy': True})[1], 'busy')  # the owner sees it before they add it
        self.assertNotIn(written(add)[1], ('busy', 'free'))
        for value in (timed, {**timed, 'busy': True}):  # takes its time anyway
            self.assertIsNone(written(value)[0])
        for bad in ({**add, 'busy': 'yes'}, {**add, 'busy': 1}, {**timed, 'busy': False}):
            with self.assertRaises(ValueError):
                calendar_writes.validate(bad, config)
        # a change says it only when it is what changes
        events = {7: {'account_id': 'cal', 'source_id': 'e7', 'title': 'Trip', 'start': '2026-12-01', 'end': '2026-12-02', 'all_day': True, 'guests': 0}}
        change = {'kind': 'calendar', 'op': 'update', 'event': 7}
        self.assertEqual(written({**change, 'busy': True}, events), ('opaque', 'busy'))
        self.assertEqual(written({**change, 'busy': False}, events), ('transparent', 'free'))
        self.assertIsNone(written({**change, 'title': 'Trip to the sea'}, events)[0])
        # a day off given a time is no longer Free, and the other way round
        at = {'start': '2026-12-01T10:00:00+00:00', 'end': '2026-12-01T11:00:00+00:00'}
        self.assertEqual(written({**change, 'all_day': False, **at}, events), ('opaque', '10:00 to 11:00'))
        events[7].update(at, all_day=False)
        self.assertEqual(written({**change, 'all_day': True, 'start': '2026-12-01'}, events), ('transparent', 'all day'))
        self.assertEqual(written({**change, 'all_day': True, 'start': '2026-12-01', 'busy': True}, events), ('opaque', 'busy'))
        # Google says Busy by leaving it out: a lost answer still reads back as sent
        for busy, google, sent in ((True, None, True), (True, 'transparent', False), (False, 'transparent', True), (False, None, False)):
            action = calendar_writes.validate({**add, 'busy': busy}, config)
            event = {k: v for k, v in {**calendar_writes.body(action, 'k'), 'transparency': google}.items() if v}
            transport = calendar_writes.CalendarTransport(config, None, None)
            transport.event = lambda *_, event=event: event
            self.assertEqual(bool(transport.reconcile(action, {'id': 'k'})), sent, (busy, google))

    def test_the_line_about_it_in_the_preparations_instructions_stays_short(self):
        config = {'accounts': [{**CAL, 'transport': 'gog'}]}
        with patch_everywhere(machine_sources_connectors, 'writable_calendars', lambda *_: [{'id': 'cal', 'name': 'Home'}]):
            told = machine_sources_connectors.calendar_prompt(config)
        self.assertEqual(told.count(', busy:true if the owner is away or taken'), 1)


class Sync(Pinned):
    def setUp(self):
        super().setUp()
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'c.sqlite', protect=True)

    def sync(self, *pages):
        pages = list(pages)

        class Fake:
            def __init__(self, *_):
                pass

            def profile(self):
                return {'id': CAL['email'], 'timeZone': 'UTC'}

            def get(self, _method, _params):
                page = pages.pop(0)
                if isinstance(page, Exception):
                    raise page
                return page
        with patch_everywhere(machine_sources_calendar, 'Calendar', Fake):
            while pages:
                machine_sources_calendar.sync_calendar(self.store, {}, CAL)

    def test_days_off_the_machine_added_count_as_busy_once_read_back(self):
        config = {'accounts': [{**CAL, 'transport': 'gog'}]}
        items = []
        for n, (day, busy) in enumerate((('2026-12-01', True), ('2026-12-02', False))):  # away, and a birthday
            action = calendar_writes.validate({'kind': 'calendar', 'op': 'create', 'calendar': 'cal', 'title': 'Day', 'start': day, 'all_day': True, 'busy': busy}, config)
            items.append({**calendar_writes.body(action, str(n)), 'status': 'confirmed'})
        self.sync({'items': items, 'nextSyncToken': 's1'})
        self.assertEqual(self.unknown(), {'busy': [['2026-12-01T00:00Z', '2026-12-02T00:00Z']], 'unknown': []})

    def unknown(self, ask=ASK):
        with self.store.connect() as db:
            return friends.free_busy(db, {'accounts': [CAL]}, ask)

    def test_known_once_the_whole_window_was_read_and_kept_while_it_is_read_again(self):
        away = {'id': 'a', 'summary': 'Away', 'status': 'confirmed', 'start': {'date': '2026-12-01'}, 'end': {'date': '2026-12-02'}}
        self.sync({'items': [away], 'nextPageToken': 'two'})
        self.assertEqual(self.unknown(), {'busy': [], 'unknown': ALL})
        self.sync({'items': [], 'nextSyncToken': 's1'})
        self.assertEqual(self.unknown(), {'busy': [['2026-12-01T00:00Z', '2026-12-02T00:00Z']], 'unknown': []})
        late = {'start': '2026-12-22', 'days': 7}
        self.assertEqual(self.unknown(late)['unknown'], [['2026-12-24T09:00Z', '2026-12-29T14:00Z']])
        # the next day's window, half read: yesterday's still stands
        timeutil.pin(NOW + dt.timedelta(hours=25))
        self.sync({'items': [], 'nextPageToken': 'two'})
        self.assertEqual(self.unknown(late)['unknown'], [['2026-12-24T09:00Z', '2026-12-29T14:00Z']])
        self.sync({'items': [away], 'nextSyncToken': 's2'})
        self.assertEqual(self.unknown(late)['unknown'], [['2026-12-25T10:00Z', '2026-12-29T14:00Z']])
        # an expired token reads it all again: still known meanwhile
        with self.assertRaises(IndexError):
            self.sync(sources.SourceError('calendar', 410), IndexError())
        self.assertEqual(self.unknown()['unknown'], [])

    def test_busy_on_an_event_read_before_is_no_new_version(self):
        event = {'account_id': 'cal', 'source_id': 'a', 'kind': 'calendar.event', 'occurred_at': '2026-12-01T00:00:00+00:00', 'title': 'Away', 'body': '',
                 'deleted': False, 'metadata': {'all_day': True, 'end_at': '2026-12-02T00:00:00+00:00'}}
        self.store.commit_page('cal', state(), [event])
        self.store.commit_page('cal', state(), [{**event, 'metadata': {**event['metadata'], 'transparency': 'opaque'}}])
        row, = self.store.events(['cal'])
        self.assertEqual(row['version'], 1)
        self.assertEqual(self.unknown()['busy'], [['2026-12-01T00:00Z', '2026-12-02T00:00Z']])
        self.store.commit_page('cal', state(), [{**event, 'metadata': {**event['metadata'], 'transparency': 'transparent'}}])
        self.assertEqual(self.store.events(['cal'])[0]['version'], 2)  # Free is a change, as before


if __name__ == '__main__':
    unittest.main()

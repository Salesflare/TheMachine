"""Calendar clashes (calendar_clashes.py): a work meeting overlapping something in a personal calendar, or the other way
around, found by plain code and raised once as a to-do that names only its own side. Made-up events only."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import calendar_busy
import calendar_clashes
import locale_prefs
from machine import todo_states
import timeutil
from seams import patch_everywhere  # noqa: E402
import graph
import machine.main as machine_main
import machine.sources.calendar as machine_sources_calendar

ROOT = Path(__file__).parent.parent

NOW = '2026-11-09T08:00:00+00:00'
GUEST = {'email': 'sam@acme.example', 'responseStatus': 'accepted'}  # Mon Nov 9
ACCOUNTS = [{'id': 'wcal', 'service': 'calendar', 'boundary': 'work:Acme', 'email': 'robin@acme.example'},
            {'id': 'pcal', 'service': 'calendar', 'boundary': 'personal:home', 'email': 'robin@home.example'},
            {'id': 'wmail', 'service': 'gmail', 'boundary': 'work:Acme', 'email': 'robin@acme.example'},
            {'id': 'pmail', 'service': 'gmail', 'boundary': 'personal:home', 'email': 'robin@home.example'},
            {'id': 'pcal2', 'service': 'calendar', 'boundary': 'personal:home', 'email': 'robin@home.example'}]


def event(account, source, title, start, end, **meta):
    """A timed event, start and end as UTC 'HH:MM' on Tue Nov 10 or full ISO times."""
    def iso(t):
        return t if 'T' in t else f'2026-11-10T{t}:00+00:00'
    m = {'start': {'dateTime': iso(start)}, 'end': {'dateTime': iso(end)}, 'end_at': iso(end), 'all_day': False,
         'timezone': 'UTC', 'status': 'confirmed', 'updated': '2026-11-01T00:00:00Z', **meta}
    if account == 'wcal' and 'attendees' not in meta:  # a work meeting has someone else on it
        m['attendees'] = [{'email': 'robin@acme.example', 'self': True, 'responseStatus': 'accepted'}, GUEST]
    return {'account_id': account, 'source_id': source, 'kind': 'calendar.event', 'occurred_at': iso(start), 'title': title,
            'body': '', 'deleted': False, 'metadata': m}


class Clashes(unittest.TestCase):
    def setUp(self):
        self.addCleanup(locale_prefs._current.update, dict(locale_prefs._current))
        locale_prefs._current.update(locale='en-US', language='en')
        tz = patch.object(timeutil, 'LOCAL_TZ', dt.timezone.utc)
        tz.start()
        self.addCleanup(tz.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'c.sqlite', protect=True)  # sealed, as every Machine is by default
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False}

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def raise_now(self, at=NOW):
        with patch_everywhere(timeutil, 'now', lambda: at):
            return self.app.raise_clashes(dt.datetime.fromisoformat(at))

    def cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]

    def found(self, at=NOW):
        sides = calendar_clashes.calendar_sides(ACCOUNTS, graph.account_side)
        with self.store.connect() as db:
            return calendar_clashes.find(db, sides, dt.datetime.fromisoformat(at), machine_sources_calendar.calendar_owned)

    def test_a_work_meeting_over_a_personal_event_is_one_work_to_do_that_keeps_the_personal_side_private(self):
        self.add(event('pcal', 'p1', 'Dentist with Dr. Lee', '14:00', '15:00'),
                 event('wcal', 'w1', 'Quarterly review', '14:30', '15:30', updated='2026-11-08T10:00:00Z',
                       attendees=[{'email': 'robin@acme.example', 'self': True, 'responseStatus': 'needsAction'},
                                  {'email': 'sam@acme.example', 'responseStatus': 'accepted'}]))
        made = self.raise_now()
        self.assertEqual(len(made), 1)
        card = self.cards()[0]
        self.assertEqual(card['title'], 'Calendar clash: Quarterly review')
        self.assertEqual(card['body'], 'Overlaps your personal calendar at 2:30 PM. Move it or decline?')
        stored = json.dumps(card)
        self.assertNotIn('Dentist', stored)
        self.assertNotIn('Lee', stored)
        with self.store.connect() as db:
            ids = json.loads(card['event_ids'])
            self.assertEqual([r[0] for r in db.execute(f"SELECT source_id FROM events WHERE id IN ({','.join('?' * len(ids))})", ids)], ['w1'])
        self.assertEqual(json.loads(card['account_ids']), ['wcal'])
        self.assertEqual(card['expires_at'], '2026-11-10T14:30:00+00:00')
        # the owner's own dashboard shows the other side in full; nothing else reads it
        view = [dict(card)]
        with self.store.connect() as db:
            calendar_clashes.annotate(db, view)
        self.assertEqual(view[0]['clash'], {'title': 'Dentist with Dr. Lee', 'start': '2026-11-10T14:00:00+00:00',
                                            'end': '2026-11-10T15:00:00+00:00', 'side': 'personal'})

    def test_a_new_personal_event_over_a_work_meeting_is_a_personal_to_do(self):
        self.add(event('wcal', 'w1', 'Board call', '09:00', '10:00'),
                 event('pcal', 'p1', 'School play', '09:30', '11:00', updated='2026-11-08T10:00:00Z'))
        self.raise_now()
        card = self.cards()[0]
        self.assertEqual(card['title'], 'Calendar clash: School play')
        self.assertIn('a work meeting', card['body'])
        self.assertNotIn('Board call', json.dumps(card))
        self.assertEqual(card['area'], 'personal')

    def test_each_clash_comes_up_once_also_after_it_is_dismissed(self):
        self.add(event('pcal', 'p1', 'Gym', '12:00', '13:00'), event('wcal', 'w1', 'Lunch and learn', '12:30', '13:30'))
        self.assertEqual(len(self.raise_now()), 1)
        self.assertEqual(self.raise_now(), [])
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='rejected'")
        self.assertEqual(self.raise_now('2026-11-09T09:00:00+00:00'), [])
        self.assertEqual(len(self.cards()), 1)

    def test_a_recurring_clash_is_one_clash_not_one_a_week(self):
        for week in (10, 17, 24):
            self.add(event('pcal', f'p_{week}', 'Swim class', f'2026-11-{week}T17:00:00+00:00', f'2026-11-{week}T18:00:00+00:00', recurring_event_id='swim'),
                     event('wcal', f'w_{week}', 'Team sync', f'2026-11-{week}T17:30:00+00:00', f'2026-11-{week}T18:30:00+00:00', recurring_event_id='sync'))
        self.assertEqual(len(self.found()), 1)
        self.assertEqual(len(self.raise_now()), 1)
        self.assertEqual(self.raise_now('2026-11-11T08:00:00+00:00'), [])  # next week's occurrence: still the same clash

    def test_all_day_free_tentative_declined_and_back_to_back_events_never_clash(self):
        self.add(event('wcal', 'w1', 'Offsite', '08:00', '18:00'),
                 event('pcal', 'p1', 'Birthday', '2026-11-10T00:00:00+00:00', '2026-11-11T00:00:00+00:00', all_day=True),
                 event('pcal', 'p2', 'Maybe coffee', '09:00', '10:00', transparency='transparent'),
                 event('pcal', 'p3', 'Tentative lunch', '12:00', '13:00', status='tentative'),
                 event('pcal', 'p4', 'Dinner invite', '17:00', '19:00', attendees=[{'email': 'robin@home.example', 'self': True, 'responseStatus': 'tentative'}]),
                 event('pcal', 'p5', 'Concert', '15:00', '16:00', attendees=[{'email': 'robin@home.example', 'self': True, 'responseStatus': 'declined'}]),
                 event('pcal', 'p6', 'Run', '18:00', '19:00'))
        self.assertEqual(self.found(), [])
        self.assertEqual(self.raise_now(), [])

    def test_a_tentative_work_meeting_does_not_clash_with_a_firm_personal_event(self):
        self.add(event('pcal', 'p1', 'Vet', '10:00', '11:00'),
                 event('wcal', 'w1', 'Optional demo', '10:00', '11:00', attendees=[{'email': 'robin@acme.example', 'self': True, 'responseStatus': 'tentative'}, GUEST]))
        self.assertEqual(self.found(), [])

    def test_the_same_meeting_on_both_calendars_is_not_a_clash(self):
        self.add(event('wcal', 'w1', 'Parent evening', '16:00', '17:00', ical_uid='abc@example'),
                 event('pcal', 'p1', 'Parent evening', '16:00', '17:00', ical_uid='abc@example'))
        self.assertEqual(self.found(), [])

    def test_two_blocks_with_nobody_else_on_them_are_not_a_clash(self):
        self.add(event('wcal', 'w1', 'Focus block', '10:00', '12:00', attendees=[]), event('pcal', 'p1', 'Gym', '11:00', '12:00'))
        self.assertEqual(self.found(), [])
        self.add(event('pcal', 'p2', 'Coffee with Kim', '10:00', '10:30', attendees=[{'email': 'kim@home.example', 'responseStatus': 'accepted'}]))
        self.assertEqual(len(self.found()), 1)  # someone else is on one side: that one is

    def test_one_personal_meeting_on_two_personal_calendars_is_one_clash(self):
        self.add(event('wcal', 'w1', 'Planning', '13:00', '14:00'),
                 event('pcal', 'p1', 'Family lunch', '13:00', '14:00', ical_uid='lunch@example'),
                 event('pcal2', 'p1', 'Family lunch', '13:00', '14:00', ical_uid='lunch@example'))
        self.assertEqual(len(self.found()), 1)
        self.assertEqual(len(self.raise_now()), 1)

    def test_past_and_far_off_clashes_and_one_side_only_raise_nothing(self):
        self.add(event('pcal', 'p1', 'Gym', '2026-11-08T12:00:00+00:00', '2026-11-08T13:00:00+00:00'),
                 event('wcal', 'w1', 'Call', '2026-11-08T12:00:00+00:00', '2026-11-08T13:00:00+00:00'),
                 event('pcal', 'p2', 'Trip', '2026-12-20T12:00:00+00:00', '2026-12-20T13:00:00+00:00'),
                 event('wcal', 'w2', 'Call', '2026-12-20T12:00:00+00:00', '2026-12-20T13:00:00+00:00'))
        self.assertEqual(self.raise_now(), [])
        self.app.config = {'accounts': [ACCOUNTS[0], ACCOUNTS[2]], 'prepare_ahead': False}
        self.assertEqual(self.raise_now(), [])

    def test_it_can_be_turned_off_and_raises_a_few_a_day_at_most(self):
        for n in range(5):
            self.add(event('pcal', f'p{n}', f'Errand {n}', f'{10 + n}:00', f'{10 + n}:45'), event('wcal', f'w{n}', f'Meeting {n}', f'{10 + n}:30', f'{11 + n}:00'))
        self.app.config['calendar_clashes'] = False
        self.assertEqual(self.raise_now(), [])
        self.app.config.pop('calendar_clashes')
        self.assertEqual(len(self.raise_now()), calendar_clashes.PER_DAY)
        self.assertEqual(self.raise_now(), [])
        self.assertEqual(len(self.raise_now('2026-11-10T08:30:00+00:00')), 2)  # the next day, the rest

    # One event that overlaps several is one to-do

    def clash(self, card):
        view = [dict(card)]
        with self.store.connect() as db:
            calendar_clashes.annotate(db, view)
        found = view[0].get('clash')
        return [c['title'] for c in [found, *found.get('more', [])]] if found else []

    def open_cards(self):
        return [c for c in self.cards() if c['status'] in todo_states.OPEN]

    def outing(self, **meta):
        """A personal event with others on it, 08:30-11:50."""
        return event('pcal', 'outing', 'Outing', '08:30', '11:50', updated='2026-11-05T00:00:00Z',
                     attendees=[{'email': 'kim@home.example', 'responseStatus': 'accepted'}], **meta)

    def office(self, day='2026-11-10', **meta):
        return event('wcal', 'office_' + day, 'Desk', f'{day}T09:00:00+00:00', f'{day}T18:00:00+00:00', attendees=[], recurring_event_id='office', **meta)

    def test_an_event_that_overlaps_several_is_one_to_do_about_it(self):
        self.add(event('pcal', 'p1', 'School play', '09:00', '12:00'),
                 event('wcal', 'w1', 'Board call', '08:30', '09:15', updated='2026-11-08T10:00:00Z'),
                 event('wcal', 'w2', 'Planning', '10:00', '11:00', updated='2026-11-08T11:00:00Z'))
        self.assertEqual(len(self.raise_now()), 1)
        card = self.cards()[0]
        self.assertEqual((card['title'], card['area']), ('Calendar clash: School play', 'personal'))
        self.assertEqual(self.clash(card), ['Board call', 'Planning'])
        self.assertNotIn('Planning', json.dumps(card))
        self.assertEqual(self.raise_now('2026-11-09T09:00:00+00:00'), [])
        self.assertEqual(len(self.cards()), 1)

    def test_an_event_entering_the_window_is_judged_with_what_starts_after_its_end(self):
        self.add(event('pcal', 'p1', 'School play', '09:00', '12:00'),
                 event('wcal', 'w1', 'Board call', '09:00', '09:30'), event('wcal', 'w2', 'Planning', '10:00', '11:00'))
        self.assertEqual(self.raise_now('2026-10-27T08:59:00+00:00'), [])  # nothing in it yet
        made = self.raise_now('2026-10-27T09:15:00+00:00')  # 14 days before: the play and the first are in, the second not yet
        self.assertEqual(len(made), 1)
        self.assertEqual((self.cards()[0]['title'], self.clash(self.cards()[0])), ('Calendar clash: School play', ['Board call', 'Planning']))
        self.assertEqual(self.raise_now('2026-10-27T10:30:00+00:00'), [])

    def test_the_same_overlap_is_not_two_to_dos_half_an_hour_apart(self):
        """The whole case: a personal event on three calendars over an office day and the stand-up in it."""
        self.add(self.outing(ical_uid='outing@example'), {**self.outing(ical_uid='outing@example'), 'account_id': 'pcal2'},
                 self.office(), event('wcal', 'standup', 'Stand up', '09:30', '09:45', recurring_event_id='standup'))
        for minute in ('08:40', '09:10', '09:40', '10:10'):
            self.raise_now(f'2026-10-27T{minute}:00+00:00')
        cards = self.cards()
        self.assertEqual(len(cards), 1)
        self.assertEqual(self.clash(cards[0]), ['Stand up'])
        self.assertEqual(cards[0]['body'], 'Overlaps a work meeting at 9:30 AM. Move it or decline?')

    def test_two_copies_without_a_uid_are_one_event(self):
        self.add(event('wcal', 'w1', 'Planning', '13:00', '14:00'), event('pcal', 'p1', 'Family lunch', '13:00', '14:30'),
                 event('pcal2', 'p1', 'Family lunch', '13:00', '14:30'))
        self.assertEqual(len(self.raise_now()), 1)
        self.assertEqual(len(self.clash(self.cards()[0])), 1)

    # A block that only frames the day

    def test_a_block_that_holds_meetings_is_no_clash_by_itself(self):
        self.add(self.outing(), self.office(), event('wcal', 'w1', 'Review', '15:00', '16:00'))
        self.assertEqual(self.raise_now(), [])

    def test_an_office_day_without_a_meeting_is_one_by_its_other_days(self):
        self.add(self.outing(), self.office())
        self.assertEqual(len(self.found()), 1)  # no way to know yet
        for day in ('2026-11-12', '2026-11-17'):
            self.add(self.office(day), event('wcal', 'w' + day, 'Review', f'{day}T10:00:00+00:00', f'{day}T11:00:00+00:00'))
        self.assertEqual(self.found(), [])

    def test_a_commitment_alone_still_clashes(self):
        self.add(event('pcal', 'p1', 'Dentist', '10:00', '11:00'), event('wcal', 'w1', 'Review', '10:30', '11:30'))
        self.assertEqual(len(self.found()), 1)

    def test_a_work_block_that_is_no_frame_still_clashes_with_an_event_with_others(self):
        hidden = {'attendees': [{'email': 'robin@acme.example', 'self': True, 'responseStatus': 'accepted'}], 'organizer': {'email': 'sam@acme.example'}}
        for title, end, meta, inside in (('Train', '18:00', {}, False),  # nothing in it: a commitment of its own
                                         ('Training day', '18:00', hidden, True),  # an invite whose other guests don't show
                                         ('Trip', '2026-11-13T18:00:00+00:00', {}, True)):  # days long
            with self.subTest(title):
                self.setUp()
                self.add(self.outing(), event('wcal', 'w2', title, '08:00', end, **{'attendees': [], **meta}))
                if inside:
                    self.add(event('wcal', 'w1', 'Review', '13:00', '14:00'))
                self.assertEqual([{g['about']['title'], *(o['title'] for o in g['others'])} for g in self.found()], [{title, 'Outing'}])

    def test_working_location_focus_time_and_out_of_office_never_clash(self):
        raw = {'id': 'x', 'summary': 'Block', 'start': {'dateTime': '2026-11-10T09:00:00Z'}, 'end': {'dateTime': '2026-11-10T12:00:00Z'}}
        self.add(self.outing())
        for kind in ('workingLocation', 'focusTime', 'outOfOffice', 'default'):
            kept = machine_sources_calendar.calendar_event(ACCOUNTS[0], {**raw, 'eventType': kind}, 'UTC')
            self.assertEqual(kept['metadata'].get('event_type'), None if kind == 'default' else kind)
            self.assertEqual(calendar_busy.blocks(kept['metadata']), kind != 'workingLocation')
            self.add(kept)
            self.assertEqual(len(self.found()), int(kind == 'default'), kind)

    def test_the_kind_google_says_is_kept_beside_without_a_new_version(self):
        raw = {'id': 'x', 'summary': 'Block', 'start': {'dateTime': '2026-11-10T09:00:00Z'}, 'end': {'dateTime': '2026-11-10T12:00:00Z'}}
        self.add(machine_sources_calendar.calendar_event(ACCOUNTS[0], raw, 'UTC'))
        self.add(machine_sources_calendar.calendar_event(ACCOUNTS[0], {**raw, 'eventType': 'focusTime'}, 'UTC'))
        with self.store.connect() as db:
            row = db.execute("SELECT version,metadata FROM events WHERE source_id='x'").fetchone()
        self.assertEqual((row['version'], json.loads(row['metadata'])['event_type']), (1, 'focusTime'))

    # What it says

    def test_it_says_when_the_overlap_begins_and_calls_a_meeting_only_a_meeting(self):
        self.add(self.outing(), event('wcal', 'w1', 'Train', '10:00', '13:00', attendees=[]))
        self.raise_now()
        self.assertEqual(self.cards()[0]['body'], 'Overlaps your work calendar at 10:00 AM. Move it or decline?')

    # Later overlaps

    def meeting(self, source='w1', start='10:00', end='11:00', **meta):
        return event('wcal', source, 'Meeting ' + source, start, end, **meta)

    def test_a_later_overlap_joins_the_open_to_do(self):
        self.add(self.outing(), self.meeting())
        self.raise_now()
        self.add(self.meeting('w2', '11:00', '12:00', updated='2026-11-09T09:00:00Z', created='2026-11-09T09:00:00Z'))
        self.assertEqual(self.raise_now('2026-11-09T10:00:00+00:00'), [])
        self.assertEqual(len(self.cards()), 1)
        self.assertEqual(self.clash(self.cards()[0]), ['Meeting w1', 'Meeting w2'])
        with self.store.connect() as db:
            self.assertEqual(calendar_clashes.raised_today(db, '2026-11-09T09:30:00+00:00'), 0)  # no new to-do

    def test_a_to_do_about_the_other_event_gives_way_to_one_about_the_shared_event(self):
        for touched in (False, True):
            with self.subTest(touched=touched):
                self.setUp()
                self.add(self.outing(), self.meeting(updated='2026-11-08T00:00:00Z'))
                first = self.raise_now()[0]
                self.assertEqual(self.cards()[0]['title'], 'Calendar clash: Meeting w1')
                if touched:
                    with self.store.connect() as db:
                        db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d',?,'other','Ask for Friday','dashboard',?)", (first, NOW))
                self.add(self.meeting('w2', '11:00', '12:00', updated='2026-11-09T09:00:00Z'))
                made = self.raise_now('2026-11-09T10:00:00+00:00')
                self.assertEqual(len(made), 1)
                cards = {c['id']: c for c in self.cards()}
                if touched:  # theirs: it stays, and the new one is about what came in
                    self.assertEqual((cards[first]['status'], cards[made[0]]['title']), ('pending', 'Calendar clash: Meeting w2'))
                    continue
                self.assertEqual((cards[first]['status'], bool(cards[first]['expired_at'])), ('completed', True))
                self.assertEqual(cards[made[0]]['title'], 'Calendar clash: Outing')
                self.assertEqual(self.clash(cards[made[0]]), ['Meeting w1', 'Meeting w2'])
                self.assertEqual(self.raise_now('2026-11-09T11:00:00+00:00'), [])

    def test_after_a_closed_to_do_only_a_really_new_overlap_comes_up(self):
        for status, choice in (('completed', 'complete'), ('rejected', 'reject')):
            with self.subTest(status=status):
                self.setUp()
                self.add(self.outing(), self.meeting())
                first = self.raise_now()[0]
                with self.store.connect() as db:
                    db.execute('UPDATE suggestions SET status=? WHERE id=?', (status, first))
                self.add(self.meeting('w2', '11:00', '12:00', recurring_event_id='weekly'))  # made long before
                self.assertEqual(self.raise_now('2026-11-09T10:00:00+00:00'), [])
                self.add(self.meeting('w2', '11:15', '12:00', recurring_event_id='weekly', updated='2026-11-09T10:30:00Z'))
                self.assertEqual(self.raise_now('2026-11-09T11:00:00+00:00'), [])  # told once
                self.add(self.meeting('w3', '11:00', '12:00', created='2026-11-09T11:30:00Z', updated='2026-11-09T11:30:00Z'))
                made = self.raise_now('2026-11-09T12:00:00+00:00')
                self.assertEqual([c['title'] for c in self.cards() if c['id'] in made], ['Calendar clash: Meeting w3'])

    def test_another_occurrence_of_a_dismissed_one_still_clashes_with_something_else(self):
        self.add(self.outing(), self.meeting('s_10', recurring_event_id='standup'))
        self.raise_now()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='rejected'")
        self.add(event('wcal', 's_17', 'Meeting s', '2026-11-17T10:00:00+00:00', '2026-11-17T11:00:00+00:00', recurring_event_id='standup'),
                 event('pcal', 'p9', 'Vet', '2026-11-17T10:00:00+00:00', '2026-11-17T12:00:00+00:00'))
        self.assertEqual(len(self.raise_now('2026-11-09T09:00:00+00:00')), 1)

    # To-dos from before: two about the same overlap

    def legacy(self, *pairs):
        """To-dos as they were raised before, one per pair: [(about, its side, other)] by source id."""
        with self.store.connect() as db:
            calendar_clashes.ensure(db)
            ids = {r['source_id']: r['id'] for r in db.execute("SELECT id,source_id FROM events WHERE account_id!='pcal2'")}
        made = []
        for about, side, other in pairs:
            with patch_everywhere(timeutil, 'now', lambda: NOW):
                with self.store.connect() as db:
                    rows = {r['id']: r for r in db.execute('SELECT * FROM events')}
                    key = calendar_clashes.clash_key(*({**dict(rows[ids[s]]), 'meta': json.loads(rows[ids[s]]['metadata'])} for s in (about, other)))
                    saved = self.store.suggest(key, 'Calendar clash: ' + about, 'Overlaps.', [ids[about]], _db=db)
                    db.execute('INSERT INTO calendar_clashes VALUES(?,?,?,?,?,?,?)', (key, saved['id'], ids[about], ids[other], side, NOW, NOW))
                    made.append(saved['id'])
        return made

    def test_the_redundant_one_of_two_open_to_dos_closes_by_itself(self):
        self.add(self.outing(), self.office(), event('wcal', 'standup', 'Stand up', '09:30', '09:45', recurring_event_id='standup'))
        frame, real = self.legacy(('outing', 'personal', 'office_2026-11-10'), ('standup', 'work', 'outing'))
        self.assertEqual(self.raise_now('2026-11-09T09:00:00+00:00'), [])
        cards = {c['id']: c for c in self.cards()}
        self.assertEqual((cards[frame]['status'], cards[real]['status']), ('completed', 'pending'))
        self.assertEqual((bool(cards[frame]['expired_at']), cards[frame]['expires_at']), (True, None))  # Not needed, not theirs
        self.assertTrue(cards[frame]['undo_until'])
        self.assertEqual(self.clash(cards[real]), ['Outing'])
        with patch_everywhere(timeutil, 'now', lambda: '2026-11-09T09:10:00+00:00'):
            self.store.decide(frame, 'undo', '', 'undo1', 'dashboard')  # theirs now: it stays
        self.raise_now('2026-11-09T09:30:00+00:00')
        self.assertEqual([c['id'] for c in self.open_cards()], [frame])  # theirs is about the event both share
        self.assertEqual(self.clash(self.open_cards()[0]), ['Desk', 'Stand up'])

    def test_two_open_ones_about_the_same_real_overlap_become_one(self):
        self.add(self.outing(), self.meeting('w1', '09:00', '09:30'), self.meeting('w2'))
        one, two = self.legacy(('outing', 'personal', 'w1'), ('w2', 'work', 'outing'))
        self.raise_now('2026-11-09T09:00:00+00:00')
        self.assertEqual([c['id'] for c in self.open_cards()], [one])
        self.assertEqual(self.clash(self.open_cards()[0]), ['Meeting w1', 'Meeting w2'])

    def test_one_the_owner_acted_on_is_never_closed(self):
        self.add(self.outing(), self.office(), self.meeting('standup', '09:30', '09:45'))
        frame, real = self.legacy(('outing', 'personal', 'office_2026-11-10'), ('standup', 'work', 'outing'))
        with self.store.connect() as db:
            for n, sid in enumerate((frame, real)):
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other','Later this week','dashboard',?)", (f'd{n}', sid, NOW))
        self.assertEqual(self.raise_now('2026-11-09T09:00:00+00:00'), [])
        self.assertEqual({c['id'] for c in self.open_cards()}, {frame, real})

    def test_a_free_event_from_google_or_outlook_is_kept_as_free(self):
        raw = {'id': 'x', 'summary': 'Focus', 'start': {'dateTime': '2026-11-10T10:00:00Z'}, 'end': {'dateTime': '2026-11-10T11:00:00Z'},
               'transparency': 'transparent'}
        self.assertEqual(machine_sources_calendar.calendar_event(ACCOUNTS[1], raw, 'UTC')['metadata']['transparency'], 'transparent')
        raw.pop('transparency')
        self.assertNotIn('transparency', machine_sources_calendar.calendar_event(ACCOUNTS[1], raw, 'UTC')['metadata'])


if __name__ == '__main__':
    unittest.main()

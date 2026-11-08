"""Calendar clashes (calendar_clashes.py): a work meeting overlapping something in a personal calendar, or the other way
around, found by plain code and raised once as a to-do that names only its own side. Made-up events only."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import calendar_clashes
import locale_prefs
import timeutil
from seams import patch_everywhere  # noqa: E402

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('clash_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

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
        self.store = a.Store(Path(self.temp.name) / 'c.sqlite', protect=True)  # sealed, as every Machine is by default
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False}

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def raise_now(self, at=NOW):
        with patch_everywhere(a, 'now', lambda: at):
            return self.app.raise_clashes(dt.datetime.fromisoformat(at))

    def cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]

    def found(self, at=NOW):
        sides = calendar_clashes.calendar_sides(ACCOUNTS, a.graph.account_side)
        with self.store.connect() as db:
            return calendar_clashes.find(db, sides, dt.datetime.fromisoformat(at), a.calendar_owned)

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

    def test_a_free_event_from_google_or_outlook_is_kept_as_free(self):
        raw = {'id': 'x', 'summary': 'Focus', 'start': {'dateTime': '2026-11-10T10:00:00Z'}, 'end': {'dateTime': '2026-11-10T11:00:00Z'},
               'transparency': 'transparent'}
        self.assertEqual(a.calendar_event(ACCOUNTS[1], raw, 'UTC')['metadata']['transparency'], 'transparent')
        raw.pop('transparency')
        self.assertNotIn('transparency', a.calendar_event(ACCOUNTS[1], raw, 'UTC')['metadata'])


if __name__ == '__main__':
    unittest.main()

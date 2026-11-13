"""Meeting prep (meeting_prep.py): before a one-off meeting with people from outside, one briefing to-do from what the
Machine already has, written in one background turn, or nothing when there is nothing useful. Once per meeting, also
after a move or a dismissal. Made-up people and events only."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import locale_prefs
import meeting_prep
import timeutil
from seams import patch_everywhere  # noqa: E402

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('prep_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

MONDAY = '2026-11-09T09:00:00+00:00'  # Mon Nov 9; the meetings are on Tue Nov 10
ACCOUNTS = [{'id': 'wcal', 'service': 'calendar', 'boundary': 'work:Acme', 'email': 'robin@acme.example'},
            {'id': 'wmail', 'service': 'gmail', 'boundary': 'work:Acme', 'email': 'robin@acme.example'},
            {'id': 'pmail', 'service': 'gmail', 'boundary': 'personal:home', 'email': 'robin@home.example'}]
SAM = 'sam@globex.example'
ME = {'email': 'robin@acme.example', 'self': True, 'responseStatus': 'accepted'}
ANSWER = {'useful': True, 'area': 'work', 'title': 'Prepare for the Globex pilot review', 'who': 'Sam Rivera, head of operations at Globex.',
          'last': 'Sam asked on Nov 5 whether the pilot can start in December.', 'promises': 'Promised Sam the pilot plan by Tuesday.',
          'questions': 'Who signs the order form on their side.', 'bring': 'The pilot plan; decide on the start date.', 'sources': []}


def meeting(source, start, guests=(SAM,), **meta):
    """A timed meeting on the work calendar, start as UTC 'HH:MM' on Tue Nov 10 or a full ISO time, an hour long."""
    begins = start if 'T' in start else f'2026-11-10T{start}:00+00:00'
    ends = (dt.datetime.fromisoformat(begins) + dt.timedelta(hours=1)).isoformat()
    m = {'start': {'dateTime': begins}, 'end': {'dateTime': ends}, 'end_at': ends, 'all_day': False, 'timezone': 'UTC', 'status': 'confirmed',
         'ical_uid': source + '@google.com', 'attendees': [ME, *({'email': g, 'responseStatus': 'accepted'} for g in guests)], **meta}
    return {'account_id': 'wcal', 'source_id': source, 'kind': 'calendar.event', 'occurred_at': begins, 'title': 'Pilot review with Globex',
            'body': 'Agenda: the pilot.', 'deleted': False, 'metadata': m}


class MeetingPrep(unittest.TestCase):
    def setUp(self):
        self.addCleanup(locale_prefs._current.update, dict(locale_prefs._current))
        locale_prefs._current.update(locale='en-US', language='en')
        tz = patch.object(timeutil, 'LOCAL_TZ', dt.timezone.utc)
        tz.start()
        self.addCleanup(tz.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'p.sqlite', protect=True)
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'review_worker': {'enabled': True}}
        self.prompts, self.answer = [], dict(ANSWER)
        self.app.meeting_prep_model = lambda config, prompt: (self.prompts.append(prompt), json.dumps(self.answer))[1]

    def mail(self, account, sender, body, days_ago, node=SAM):
        at = (dt.datetime.fromisoformat(MONDAY) - dt.timedelta(days=days_ago)).isoformat()
        with self.store.connect() as db:
            event_id = db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                                  "VALUES(?,?,?,?,?,?,?,'h',?)", (account, f'm{days_ago}{account}', 'gmail.message', at, 'Pilot', body,
                                                                  json.dumps({'from': sender}), at)).lastrowid
            db.execute('INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES(?,?,?,0,1)', ('email:' + node, event_id, at))
            db.execute('INSERT OR IGNORE INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,?,?,?,?,?,?)',
                       ('email:' + node, 'person', 'Sam Rivera', 1.0, at, 1, json.dumps({'identifiers': ['email:' + node], 'role': 'head of operations'})))
        return event_id

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])

    def run_pass(self, at=MONDAY):
        """One pass as the worker runs it: the next meeting due, then its turn."""
        with patch_everywhere(a, 'now', lambda: at):
            found = self.app.meeting_prep_next(dt.datetime.fromisoformat(at))
            return self.app.meeting_prep_run(found) if found else None

    def cards(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM suggestions ORDER BY created_at')]

    def meeting_id(self, source):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE source_id=?', (source,)).fetchone()[0]

    # Which meetings ---------------------------------------------------------------------------------------------

    def test_only_a_one_off_live_meeting_with_someone_from_outside_is_eligible(self):
        owned = lambda m: True
        check = lambda **meta: meeting_prep.eligible(meeting('x', '10:00', **meta)['metadata'], owned, {'robin@acme.example'}, {'acme.example'})
        ok, guests = check()
        self.assertTrue(ok)
        self.assertEqual([g['email'] for g in guests], [SAM])
        self.assertEqual(check(recurring_event_id='weekly')[1], 'recurring')
        self.assertEqual(check(all_day=True)[1], 'all_day')
        self.assertEqual(check(status='cancelled')[1], 'cancelled')
        self.assertEqual(check(transparency='transparent')[1], 'free')
        self.assertEqual(check(attendees=[{**ME, 'responseStatus': 'declined'}, {'email': SAM}])[1], 'declined')
        self.assertEqual(check(attendees=[ME, {'email': 'kim@acme.example'}, {'email': 'room@resource.example', 'resource': True}])[1], 'internal')
        self.assertEqual(meeting_prep.eligible(meeting('x', '10:00')['metadata'], lambda m: False, set(), set())[1], 'not_theirs')

    def test_the_briefing_is_due_on_a_work_morning_before_the_meeting_and_not_too_late(self):
        utc = dt.timezone.utc
        at = lambda text: dt.datetime.fromisoformat(text)
        self.assertEqual(meeting_prep.prep_moment(at('2026-11-10T14:00:00+00:00')), at('2026-11-10T08:00:00+00:00'))  # afternoon: that morning
        self.assertEqual(meeting_prep.prep_moment(at('2026-11-10T10:00:00+00:00')), at('2026-11-09T08:00:00+00:00'))  # morning: the day before
        self.assertEqual(meeting_prep.prep_moment(at('2026-11-16T09:00:00+00:00')), at('2026-11-13T08:00:00+00:00'))  # Monday: the Friday before
        self.assertFalse(meeting_prep.due(at('2026-11-10T14:00:00+00:00'), at(MONDAY), utc))   # not yet
        self.assertTrue(meeting_prep.due(at('2026-11-10T10:00:00+00:00'), at(MONDAY), utc))
        self.assertFalse(meeting_prep.due(at('2026-11-09T09:30:00+00:00'), at(MONDAY), utc))  # too late to use
        self.assertFalse(meeting_prep.due(at('2026-11-10T10:00:00+00:00'), at('2026-11-09T07:00:00+00:00'), utc))  # before the hours
        self.assertFalse(meeting_prep.due(at('2026-11-16T09:00:00+00:00'), at('2026-11-14T10:00:00+00:00'), utc))  # a Saturday

    # The to-do --------------------------------------------------------------------------------------------------

    def test_a_meeting_with_correspondence_gets_one_briefing_to_do_with_its_sources(self):
        asked = self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December? Who should sign the order form?', 4)
        self.mail('pmail', 'Sam Rivera <sam@globex.example>', 'Birthday drinks on Saturday?', 2)  # personal: never in a work briefing
        self.answer['sources'] = [f'E{asked}', 'E999999']
        self.add(meeting('g1', '10:00'))
        made = self.run_pass()
        self.assertIsNotNone(made)
        self.assertEqual(len(self.prompts), 1)
        self.assertIn('Can the pilot start in December?', self.prompts[0])
        self.assertNotIn('Birthday', self.prompts[0])
        [card] = self.cards()
        self.assertEqual(card['title'], 'Prepare for the Globex pilot review')
        self.assertEqual(card['body'].split('\n\n'), [
            '**Who:** Sam Rivera, head of operations at Globex.',
            '**Last contact:** Sam asked on Nov 5 whether the pilot can start in December.',
            '**Open promises:** Promised Sam the pilot plan by Tuesday.',
            '**Open questions:** Who signs the order form on their side.',
            '**Decide or bring:** The pilot plan; decide on the start date.'])
        self.assertEqual(json.loads(card['event_ids']), [self.meeting_id('g1'), asked])  # the meeting first, then the message; an unknown id dropped
        self.assertEqual(card['status'], 'pending')
        self.assertEqual(card['expires_at'][:16], '2026-11-10T10:00')
        self.assertIsNone(self.run_pass())  # once
        self.assertEqual(len(self.prompts), 1)

    def test_no_evidence_means_no_turn_and_no_to_do(self):
        self.add(meeting('g2', '10:00', guests=('new@initech.example',)))
        self.assertIsNone(self.run_pass())
        self.assertEqual(self.prompts, [])
        self.assertEqual(self.cards(), [])

    def test_a_turn_that_finds_nothing_useful_makes_nothing_and_is_not_asked_again(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Thanks!', 3)
        self.add(meeting('g3', '10:00'))
        self.answer = {'useful': False}
        self.assertIsNone(self.run_pass())
        self.assertEqual(self.cards(), [])
        self.assertIsNone(self.run_pass())
        self.assertEqual(len(self.prompts), 1)

    def test_only_who_they_are_or_an_unsourced_last_contact_is_nothing(self):
        found = {'messages': {5: {}}, 'promises': {}}
        self.assertIsNone(meeting_prep.parse(json.dumps({'useful': True, 'who': 'Sam Rivera.', 'last': 'They wrote last week.'}), found))
        kept = meeting_prep.parse(json.dumps({'useful': True, 'who': 'Sam.', 'last': 'Asked about pricing.', 'bring': 'Pricing.', 'sources': ['E5']}), found)
        self.assertEqual(kept['sources'], [5])
        self.assertEqual(kept['fields']['last'], 'Asked about pricing.')

    def test_a_personal_meeting_gets_no_to_do(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'See you at the reunion dinner.', 3)
        self.add(meeting('g4', '10:00'))
        self.answer = {**ANSWER, 'area': 'personal'}
        self.assertIsNone(self.run_pass())
        self.assertEqual(self.cards(), [])

    def test_a_rescheduled_meeting_keeps_its_one_to_do_which_follows_the_new_time(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.add(meeting('g5', '10:00'))
        self.run_pass()
        self.add(meeting('g5', '2026-11-11T10:00'))  # moved to Wednesday: the same meeting
        with patch_everywhere(a, 'now', lambda: '2026-11-10T09:00:00+00:00'):
            self.app.meeting_prep_follow(dt.datetime.fromisoformat('2026-11-10T09:00:00+00:00'))
        self.assertIsNone(self.run_pass('2026-11-10T09:00:00+00:00'))
        [card] = self.cards()
        self.assertEqual(card['expires_at'][:16], '2026-11-11T10:00')
        self.assertEqual(card['status'], 'pending')
        self.assertEqual(len(self.prompts), 1)

    def test_a_dismissed_briefing_never_comes_back(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.add(meeting('g6', '10:00'))
        self.run_pass()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='rejected'")
        self.add(meeting('g6', '2026-11-11T10:00'))
        self.assertIsNone(self.run_pass('2026-11-10T09:00:00+00:00'))
        self.assertEqual([c['status'] for c in self.cards()], ['rejected'])
        self.assertEqual(len(self.prompts), 1)

    def test_a_canceled_meeting_closes_its_briefing(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.add(meeting('g7', '10:00'))
        self.run_pass()
        self.add({**meeting('g7', '10:00'), 'deleted': True})
        with patch_everywhere(a, 'now', lambda: '2026-11-09T10:00:00+00:00'):
            self.app.meeting_prep_follow(dt.datetime.fromisoformat('2026-11-09T10:00:00+00:00'))
        self.assertEqual([c['status'] for c in self.cards()], ['completed'])

    def test_a_meeting_the_review_already_made_a_to_do_for_gets_no_second_one(self):
        self.mail('wmail', 'Sam Rivera <sam@globex.example>', 'Can the pilot start in December?', 4)
        self.add(meeting('g8', '10:00'))
        self.store.suggest('review:g8', 'Send Sam the pilot plan before Tuesday', 'Sam asked for it.', [self.meeting_id('g8')])
        self.assertIsNone(self.run_pass())
        self.assertEqual(len(self.cards()), 1)
        self.assertEqual(self.prompts, [])

    def test_off_in_the_config(self):
        self.app.config['meeting_prep'] = False
        self.assertIsNone(self.app.meeting_prep_step())


if __name__ == '__main__':
    unittest.main()

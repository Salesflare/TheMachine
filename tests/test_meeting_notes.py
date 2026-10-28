"""Notes added to a meeting (meeting_notes.py): pasted or uploaded by the owner on the meeting in the Calendar, or saved
by a Do it run (a transcript someone sent). They live on the meeting's own calendar account as a meeting.notes signal,
are reviewed and used like Zoom's notes, show on the meeting, and go to the team only as the meeting does. A signal
review only reads them. No live calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('notes_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import meeting_notes  # noqa: E402
import shared_graph  # noqa: E402

WORK = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
HOME = {'id': 'home-cal', 'email': 'owner@home.example', 'service': 'calendar', 'boundary': 'personal:Home'}
TRANSCRIPT = '# Board meeting Q4\n\n## Decisions\n\n- Hire two engineers\n- Budget approved\n\n' + 'Speaker 1: we went through the numbers.\n' * 2000


def raw(source_id, title, start, end, **extra):
    return {'id': source_id, 'summary': title, 'start': {'dateTime': start}, 'end': {'dateTime': end}, 'status': 'confirmed',
            'htmlLink': 'https://calendar.google.com/calendar/event?eid=' + source_id, **extra}


class MeetingNotes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        guests = [{'email': 'owner@example.com', 'self': True}, {'email': 'dana@board.example', 'displayName': 'Dana Board'}]
        self.store.commit_page('cal', {}, [
            a.calendar_event(WORK, raw('board', 'Board meeting Q4', '2026-10-28T14:00:00+01:00', '2026-10-28T16:00:00+01:00', attendees=guests), 'Europe/Brussels'),
            a.calendar_event(WORK, raw('standup', 'Standup', '2026-10-28T09:00:00+01:00', '2026-10-28T09:15:00+01:00'), 'Europe/Brussels')])
        self.store.commit_page('home-cal', {}, [
            a.calendar_event(HOME, raw('dinner', 'Dinner', '2026-10-28T19:00:00+01:00', '2026-10-28T21:00:00+01:00'), 'Europe/Brussels')])
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, {'accounts': [WORK, HOME, {'id': 'mail', 'service': 'gmail', 'email': 'owner@example.com'}]}
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute("SELECT id,source_id FROM events WHERE kind='calendar.event'")}
        self.tz = patch.object(a, 'local_tz', return_value=a.ZoneInfo('Europe/Brussels'))
        self.tz.start()
        self.addCleanup(self.tz.stop)

    def notes_row(self, meeting='board'):
        with self.store.connect() as db:
            return db.execute("SELECT * FROM events WHERE kind='meeting.notes' AND source_id=?", (f'notes:{self.ids[meeting]}',)).fetchone()

    def test_a_do_it_run_finds_the_meeting_by_its_day_and_puts_a_long_transcript_on_it(self):
        found = self.app.action('meeting_notes', {'day': '2026-10-28', 'query': 'board'})
        self.assertEqual([(m['title'], m['has_notes']) for m in found['meetings']], [('Board meeting Q4', False)])
        everything = self.app.action('meeting_notes', {'day': '2026-10-28'})['meetings']
        self.assertEqual([m['title'] for m in everything], ['Standup', 'Board meeting Q4', 'Dinner'])
        saved = self.app.action('meeting_notes', {'event_id': found['meetings'][0]['event_id'], 'text': TRANSCRIPT,
                                                  '_notes_session': 'agent:main:assistant-review-preparation-abc123'})
        self.assertEqual((saved['title'], saved['chars']), ('Board meeting Q4', len(TRANSCRIPT.strip())))
        row = self.notes_row()
        self.assertEqual((row['account_id'], row['title'], row['occurred_at']), ('cal', 'Board meeting Q4', '2026-10-28T13:00:00+00:00'))
        self.assertEqual(row['analyzed_version'], 0)  # the next review reads them, like Zoom's notes
        meta = json.loads(row['metadata'])
        self.assertEqual(meta['added_by'], 'machine')
        self.assertIn('dana@board.example', shared_graph.item_people(meta))  # judged by the meeting's own people
        read = self.app.action('meeting_notes', {'event_id': self.ids['board']})
        self.assertEqual(read['notes']['chars'], len(TRANSCRIPT.strip()))
        self.assertEqual(len(read['notes']['text']), meeting_notes.READ_CHARS)  # a tool result reads on with offset
        text, offset = read['notes']['text'], read['notes']['next_offset']
        while offset is not None:
            more = self.app.action('meeting_notes', {'event_id': self.ids['board'], 'offset': offset})['notes']
            text, offset = text + more['text'], more['next_offset']
        self.assertEqual(text, TRANSCRIPT.strip())
        self.assertTrue(self.app.action('meeting_notes', {'day': '2026-10-28', 'query': 'board'})['meetings'][0]['has_notes'])

    def test_saving_again_replaces_or_adds_below_and_an_empty_save_is_refused(self):
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'First notes'}, owner_dashboard=True)
        self.assertTrue(self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'First notes'})['unchanged'])
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'Transcript', 'append': True})
        self.assertEqual(self.notes_row()['body'], 'First notes\n\nTranscript')
        self.assertTrue(self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'Only this'})['replaced'])
        self.assertEqual((self.notes_row()['body'], self.notes_row()['version']), ('Only this', 3))
        with self.assertRaisesRegex(ValueError, 'text is the notes'):
            self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': '  '})
        with self.assertRaisesRegex(ValueError, 'up to'):
            self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'x' * (meeting_notes.MAX_CHARS + 1)})
        with self.assertRaisesRegex(ValueError, 'No meeting'):
            self.app.action('meeting_notes', {'event_id': 999999, 'text': 'Notes'})

    def test_the_owner_adds_them_in_the_calendar_and_removes_them(self):
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': '## Notes\n\n- one'}, owner_dashboard=True)
        self.assertEqual(json.loads(self.notes_row()['metadata'])['added_by'], 'owner')
        rows = {r['title']: r for r in self.store.calendar(['cal', 'home-cal'], '2026-10-27T23:00:00Z', '2026-10-28T23:00:00Z')}
        self.assertEqual((rows['Board meeting Q4']['notes']['by'], rows['Board meeting Q4']['notes']['chars']), ('owner', 15))
        self.assertNotIn('notes', rows['Standup'])
        self.assertEqual(self.app.action('meeting_notes', {'event_id': self.ids['board'], 'remove': True}, owner_dashboard=True)['removed'], True)
        self.assertEqual(self.notes_row()['deleted'], 1)
        self.assertIsNone(self.app.action('meeting_notes', {'event_id': self.ids['board']})['notes'])
        self.assertNotIn('notes', {r['title']: r for r in self.store.calendar(['cal'], '2026-10-27T23:00:00Z', '2026-10-28T23:00:00Z')}['Board meeting Q4'])

    def test_a_signal_review_only_reads_them(self):
        with self.assertRaisesRegex(ValueError, 'Reviews read meeting notes'):
            self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'Notes from an email',
                                              '_notes_session': 'agent:main:assistant-review-signals-abc'})
        self.assertIsNone(self.notes_row())
        self.app.action('meeting_notes', {'event_id': self.ids['board'], '_notes_session': 'agent:main:assistant-review-signals-abc'})  # reading is fine
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'From the owner’s own chat', '_notes_session': 'agent:main:main'})
        self.assertIsNotNone(self.notes_row())

    def test_personal_notes_stay_on_the_personal_calendar(self):
        self.app.action('meeting_notes', {'event_id': self.ids['dinner'], 'text': 'Bring wine'})
        self.assertEqual(self.notes_row('dinner')['account_id'], 'home-cal')
        self.assertEqual(a.suggestion_scope(['home-cal'], self.app.config['accounts']), 'personal')

    def test_they_are_that_meetings_notes_for_its_follow_ups_and_go_with_the_meeting(self):
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'Dana sends the deck.'})
        with self.store.connect() as db:
            found = meeting_notes.for_event(db, self.ids['board'], '2026-10-28')
            self.assertEqual((found['kind'], found['id']), ('meeting.notes', self.notes_row()['id']))
            self.assertEqual(meeting_notes.match(db, found)['id'], self.ids['board'])
            self.assertIsNone(meeting_notes.for_event(db, self.ids['standup'], '2026-10-28'))
            # On a board, the meeting's notes go with it (and as it is judged); another meeting's don't
            self.assertEqual(shared_graph._items(db, {self.ids['board']}), {self.ids['board'], self.notes_row()['id']})
            self.assertEqual(shared_graph._items(db, {self.ids['standup']}), {self.ids['standup']})
        self.assertEqual(shared_graph._source('meeting.notes'), 'meetings')

    def test_do_it_is_told_where_meeting_notes_go_when_a_calendar_is_connected(self):
        self.assertIn('meeting_notes', a.meeting_notes_prompt(self.app.config))
        self.assertEqual(a.meeting_notes_prompt({'accounts': [{'id': 'mail', 'service': 'gmail'}]}), '')
        job = {'job_id': 'j' * 32, 'suggestion_id': 's' * 16}
        self.assertIn('assistant meeting-notes --event', a.preparation_prompt(job, config=self.app.config))
        self.assertIn('meeting_notes', a.DASHBOARD_ACTIONS)
        self.assertIn('meeting_notes', a.UPLOAD_ACTIONS)  # a long transcript fits in one request
        self.assertNotIn('meeting_notes', a.OWNER_ACTIONS)  # Do it and the CLI add them too
        plugin = (Path(__file__).parent.parent / 'openclaw-plugin' / 'index.ts').read_text()
        self.assertIn("'meeting_notes'", plugin)
        self.assertIn("args._notes_session = key", plugin)  # the host says which session it is, never the model


if __name__ == '__main__':
    unittest.main()

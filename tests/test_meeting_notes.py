"""A meeting's Notes and Transcript (meeting_notes.py): two fields, each pasted or uploaded by the owner on the meeting in
the Calendar, or saved by a Do it run. They live on the meeting's own calendar account as meeting.notes and
meeting.transcript signals, are reviewed and used like Zoom's, show on the meeting next to Zoom's (never over them), and
go to the team only as the meeting does. A signal review only reads them. Notes saved before the two were apart move
to Transcript once when they are one. No live calls."""
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

TURNS = '\n'.join(f'[{m // 60}:{m % 60:02d}:00] Speaker {m % 2 + 1}: we went through item {m}.' for m in range(0, 124, 3))

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

    def test_notes_and_transcript_are_two_fields_each_saved_and_removed_on_its_own(self):
        board = self.ids['board']
        self.app.action('meeting_notes', {'event_id': board, 'text': '## Decisions\n\n- Hire two engineers'}, owner_dashboard=True)
        saved = self.app.action('meeting_notes', {'event_id': board, 'field': 'transcript', 'text': TURNS})
        self.assertEqual((saved['field'], saved['chars']), ('transcript', len(TURNS)))
        read = self.app.action('meeting_notes', {'event_id': board})
        self.assertEqual(read['notes']['text'], '## Decisions\n\n- Hire two engineers')
        self.assertEqual((read['transcript']['text'], read['transcript']['by'], read['transcript']['minutes']), (TURNS, 'machine', 123))
        self.assertIsNone(read['zoom'])
        with self.store.connect() as db:
            row = db.execute("SELECT * FROM events WHERE kind='meeting.transcript'").fetchone()
        self.assertEqual((row['source_id'], row['account_id'], row['analyzed_version']), (f'transcript:{board}', 'cal', 0))  # the review reads it
        self.assertEqual(json.loads(row['metadata'])['field'], 'transcript')
        self.assertIn('dana@board.example', shared_graph.item_people(json.loads(row['metadata'])))  # judged by the meeting's own people
        # Only the field asked for: a transcript-looking text the owner puts in Notes stays in Notes
        self.app.action('meeting_notes', {'event_id': board, 'text': TURNS, 'append': True}, owner_dashboard=True)
        self.assertTrue(self.app.action('meeting_notes', {'event_id': board, 'field': 'notes'})['notes']['text'].endswith(TURNS))
        only = self.app.action('meeting_notes', {'event_id': board, 'field': 'transcript', 'offset': 10})
        self.assertIsNone(only['notes'])
        self.assertEqual(only['transcript']['text'], TURNS[10:])
        rows = {r['title']: r for r in self.store.calendar(['cal'], '2026-10-27T23:00:00Z', '2026-10-28T23:00:00Z')}
        self.assertEqual((rows['Board meeting Q4']['notes']['by'], rows['Board meeting Q4']['transcript']['by']), ('owner', 'machine'))
        day = {m['title']: m for m in self.app.action('meeting_notes', {'day': '2026-10-28'})['meetings']}
        self.assertEqual((day['Board meeting Q4']['has_notes'], day['Board meeting Q4']['has_transcript'], day['Standup']['has_transcript']), (True, True, False))
        with self.store.connect() as db:  # on a board, the transcript goes with its meeting too
            ids = shared_graph._items(db, {board})
            self.assertIn(row['id'], ids)
            self.assertEqual(meeting_notes.for_event(db, board, '2026-10-28')['kind'], 'meeting.notes')  # follow-ups read the notes first
        self.assertTrue(self.app.action('meeting_notes', {'event_id': board, 'field': 'transcript', 'remove': True}, owner_dashboard=True)['removed'])
        read = self.app.action('meeting_notes', {'event_id': board})
        self.assertIsNone(read['transcript'])
        self.assertIsNotNone(read['notes'])
        with self.assertRaisesRegex(ValueError, 'field is notes'):
            self.app.action('meeting_notes', {'event_id': board, 'field': 'summary', 'text': 'x'})
        with self.assertRaisesRegex(ValueError, 'A transcript can be up to'):
            self.app.action('meeting_notes', {'event_id': board, 'field': 'transcript', 'text': 'x' * (meeting_notes.MAX_CHARS + 1)})
        self.assertEqual(shared_graph._source('meeting.transcript'), 'meetings')

    def test_zoom_puts_its_summary_in_notes_and_its_transcript_in_transcript_next_to_the_owners(self):
        zoom = {'id': 'zoom', 'service': 'zoom', 'email': 'owner@example.com', 'boundary': 'work:Example'}
        self.app.config['accounts'].append(zoom)
        meta = {'meeting_id': '123456789', 'start_at': '2026-10-28T13:01:00+00:00', 'end_at': '2026-10-28T15:05:00+00:00',
                'host_email': 'owner@example.com', 'source_url': 'https://us02web.zoom.us/doc/abc'}
        self.store.commit_page('zoom', {}, [
            {'account_id': 'zoom', 'source_id': 'summary:1', 'kind': 'zoom.summary', 'occurred_at': '2026-10-28T13:01:00+00:00',
             'title': 'Board meeting Q4', 'body': '## Next steps\n\n- Dana sends the deck', 'metadata': meta, 'deleted': False},
            {'account_id': 'zoom', 'source_id': 'transcript:1', 'kind': 'zoom.transcript', 'occurred_at': '2026-10-28T13:01:00+00:00',
             'title': 'Board meeting Q4', 'body': 'Dana: I will send the deck.\nOwner: Thanks.', 'metadata': {**meta, 'truncated': False}, 'deleted': False}])
        read = self.app.action('meeting_notes', {'event_id': self.ids['board']})
        self.assertEqual((read['notes'], read['transcript']), (None, None))  # nothing added: Zoom's alone
        self.assertEqual(read['zoom']['notes']['text'], '## Next steps\n\n- Dana sends the deck')
        self.assertEqual((read['zoom']['transcript']['text'], read['zoom']['transcript']['minutes']), ('Dana: I will send the deck.\nOwner: Thanks.', 124))
        self.assertEqual(read['zoom']['url'], 'https://us02web.zoom.us/doc/abc')
        # The owner's own never replaces Zoom's, nor the other way round: both show, each with its source
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'text': 'My own notes'}, owner_dashboard=True)
        self.app.action('meeting_notes', {'event_id': self.ids['board'], 'field': 'transcript', 'text': TURNS}, owner_dashboard=True)
        read = self.app.action('meeting_notes', {'event_id': self.ids['board']})
        self.assertEqual((read['notes']['text'], read['zoom']['notes']['text']), ('My own notes', '## Next steps\n\n- Dana sends the deck'))
        self.assertEqual((read['transcript']['text'], read['zoom']['transcript']['text'][:5]), (TURNS, 'Dana:'))
        self.assertIsNone(self.app.action('meeting_notes', {'event_id': self.ids['standup']})['zoom'])  # another meeting gets none

    def test_notes_saved_before_the_split_that_are_a_transcript_move_to_transcript_once(self):
        board, standup, dinner = self.ids['board'], self.ids['standup'], self.ids['dinner']
        def legacy(account, meeting, body):  # as saved before Notes and Transcript were apart: no field
            with self.store.connect() as db:
                db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                           "VALUES(?,?,'meeting.notes','2026-10-28T13:00:00+00:00','m',?,?,'h',?)",
                           (account, f'notes:{meeting}', body, json.dumps({'event_id': meeting, 'added_by': 'machine'}), a.now()))
        legacy('cal', board, '# Board\n\n' + TURNS + '\nand a line that runs on')
        legacy('cal', standup, '## Summary\n\n- At 10:30 we agreed on the plan\n- Next call 14:00\n\nDecisions: ship it.')
        legacy('home-cal', dinner, 'Bring wine')
        with self.store.connect() as db:
            moved = self.store.move_meeting_transcripts(db)
            self.assertEqual(len(moved), 1)
            row = db.execute('SELECT * FROM events WHERE id=?', (moved[0],)).fetchone()
            self.assertEqual((row['kind'], row['source_id']), ('meeting.transcript', f'transcript:{board}'))
            self.assertEqual(json.loads(row['metadata'])['moved_from'], 'notes')
            self.assertEqual(dict(db.execute('SELECT old_kind,old_source_id FROM meeting_moves').fetchone()), {'old_kind': 'meeting.notes', 'old_source_id': f'notes:{board}'})
            self.assertEqual(self.store.move_meeting_transcripts(db), [])  # once: nothing more the second time
        read = self.app.action('meeting_notes', {'event_id': board})
        self.assertIsNone(read['notes'])
        self.assertTrue(read['transcript']['text'].startswith('# Board'))
        self.assertEqual(self.app.action('meeting_notes', {'event_id': standup})['notes']['text'][:10], '## Summary')
        # What the owner puts in Notes from now on stays there, also over a restart
        self.app.action('meeting_notes', {'event_id': standup, 'text': TURNS}, owner_dashboard=True)
        a.Store(self.store.path)
        self.assertEqual(self.app.action('meeting_notes', {'event_id': standup})['notes']['text'], TURNS)

    def test_a_transcript_is_told_by_its_structure_not_its_words(self):
        looks = meeting_notes.looks_like_transcript
        self.assertTrue(looks(TURNS))
        self.assertTrue(looks('\n'.join(f'00:0{i}:15 Dana: point {i}' for i in range(8))))
        self.assertTrue(looks('\n\n'.join(f'Speaker {i % 2}  {i}:05\nWords said in turn {i}.' for i in range(6))))  # name and time, words below
        self.assertTrue(looks('\n'.join(f'- Dana ({i}:05): said {i}' for i in range(6))))
        self.assertTrue(looks('WEBVTT\n\n' + '\n\n'.join(f'{i}\n00:00:0{i}.000 --> 00:00:0{i}.900\nDana: hi {i}' for i in range(6))))
        self.assertFalse(looks('# Board meeting\n\n## Transcript summary\n\nSpeaker 1 said the numbers are good. Speaker 2 agreed.'))
        self.assertFalse(looks('Dana: I will send the deck.\nOwner: Thanks.\n' * 5))  # turns without times: not the structure asked for
        self.assertFalse(looks('## Agenda\n\n- [0:05] Intro\n- [0:20] Numbers\n\n' + 'A long paragraph of decisions. ' * 40 + '\n'
                               + '\n'.join(f'[{i}:00] Dana: aside {i}' for i in range(5))))  # a few quoted turns in a summary
        self.assertEqual(meeting_notes.spoken_minutes(TURNS), 123)
        self.assertIsNone(meeting_notes.spoken_minutes('No times here'))

    def test_do_it_is_told_where_meeting_notes_go_when_a_calendar_is_connected(self):
        self.assertIn('meeting_notes', a.meeting_notes_prompt(self.app.config))
        self.assertIn('field=notes or transcript', a.meeting_notes_prompt(self.app.config))
        self.assertEqual(a.meeting_notes_prompt({'accounts': [{'id': 'mail', 'service': 'gmail'}]}), '')
        job = {'job_id': 'j' * 32, 'suggestion_id': 's' * 16}
        self.assertIn('assistant meeting-notes --event', a.preparation_prompt(job, config=self.app.config))
        self.assertIn('meeting_notes', a.DASHBOARD_ACTIONS)
        self.assertIn('meeting_notes', a.UPLOAD_ACTIONS)  # a long transcript fits in one request
        self.assertNotIn('meeting_notes', a.OWNER_ACTIONS)  # Do it and the CLI add them too
        plugin = (Path(__file__).parent.parent / 'openclaw-plugin' / 'index.ts').read_text()
        self.assertIn("'meeting_notes'", plugin)
        self.assertIn('field transcript is what was said', plugin)
        self.assertIn("args._notes_session = key", plugin)  # the host says which session it is, never the model


if __name__ == '__main__':
    unittest.main()

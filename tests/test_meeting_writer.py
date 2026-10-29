"""Generate notes (meeting_writer.py): The Machine writes a meeting's Notes from its Transcript on the service, when the
owner asks for it in the Calendar. Only for a meeting with a transcript and no notes; never over notes that come in
while it writes. A long transcript is read in parts that each fit one model turn. It waits while a usage limit holds,
fails visibly when the model can't be reached, and goes on after a restart. The notes are The Machine's, marked as
written from the transcript, and are the meeting's record for its follow-ups like any notes. No live calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('writer_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import meeting_notes  # noqa: E402
import meeting_writer  # noqa: E402

WORK = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
# A 2h15m meeting, about 150,000 characters: three parts
LONG = '\n'.join(f'[{m // 60}:{m % 60:02d}:{s:02d}] Speaker {(m + s) % 3 + 1}: we went through item {m}, '
                 'the numbers for the quarter and the hiring plan for the next one.' for m in range(135) for s in range(0, 60, 6))
SHORT = '\n'.join(f'[0:{m:02d}:00] Speaker {m % 2 + 1}: point {m}.' for m in range(30))
NOTES = '## Summary\n\nThe board approved the plan.\n\n## Decisions\n\n- Hire two engineers\n\n## Action items\n\n- **Dana**: send the deck by Friday'


def raw(source_id, title, start, end, **extra):
    return {'id': source_id, 'summary': title, 'start': {'dateTime': start}, 'end': {'dateTime': end}, 'status': 'confirmed',
            'htmlLink': 'https://calendar.google.com/calendar/event?eid=' + source_id, **extra}


class Model:
    """The stand-in model: answers each prompt, kept in order. fail: raise for that many turns."""

    def __init__(self, answer=NOTES):
        self.prompts, self.answer, self.fail = [], answer, 0

    def __call__(self, config, prompt):
        self.prompts.append(prompt)
        if self.fail:
            self.fail -= 1
            raise OSError('unreachable')
        return 'Part notes: item reviewed.' if 'This is part' in prompt else self.answer


class MeetingWriter(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        guests = [{'email': 'owner@example.com', 'self': True}, {'email': 'dana@board.example', 'displayName': 'Dana Board'}]
        self.store.commit_page('cal', {}, [
            a.calendar_event(WORK, raw('board', 'Board meeting Q4', '2026-10-28T14:00:00+01:00', '2026-10-28T16:15:00+01:00', attendees=guests), 'Europe/Brussels'),
            a.calendar_event(WORK, raw('standup', 'Standup', '2026-10-28T09:00:00+01:00', '2026-10-28T09:15:00+01:00'), 'Europe/Brussels')])
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, {'accounts': [WORK], 'language': 'nl'}
        self.model = self.app.notes_model = Model()
        self.paused = None
        self.app.background_pause = lambda **k: self.paused
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute("SELECT id,source_id FROM events WHERE kind='calendar.event'")}
        self.board = self.ids['board']
        self.tz = patch.object(a, 'local_tz', return_value=a.ZoneInfo('Europe/Brussels'))
        self.tz.start()
        self.addCleanup(self.tz.stop)

    def transcript(self, text=LONG, meeting='board'):
        self.app.action('meeting_notes', {'event_id': self.ids[meeting], 'field': 'transcript', 'text': text}, owner_dashboard=True)

    def generate(self, meeting='board'):
        return self.app.action('meeting_notes_write', {'event_id': self.ids[meeting]}, owner_dashboard=True)

    def wait(self):
        thread = getattr(self.app, '_meeting_write_thread', None)
        if thread:
            thread.join(10)

    def read(self, meeting='board'):
        return self.app.meeting_notes({'event_id': self.ids[meeting]}, True, meeting_notes.MAX_CHARS)

    def test_a_long_transcript_is_read_in_parts_and_its_notes_are_saved_as_the_machines_on_the_service(self):
        self.transcript()
        self.assertGreater(len(LONG), 140_000)
        started = self.generate()
        self.assertEqual(started['writing']['status'], 'queued')
        self.wait()  # the service's own thread: nothing in the page has to stay open
        parts = [p for p in self.model.prompts if 'This is part' in p]
        self.assertEqual(len(parts), 3)
        self.assertEqual(len(self.model.prompts), 4)
        for prompt in self.model.prompts:  # each turn fits one program argument
            self.assertLess(len(prompt.encode()), 128 * 1024)
        self.assertIn('### Part 3', self.model.prompts[-1])
        self.assertIn('Action items', self.model.prompts[-1])
        self.assertIn('language the meeting was held in', self.model.prompts[-1])
        self.assertIn('write in Dutch', self.model.prompts[-1])  # the owner's language when the meeting mixes them
        self.assertIn('Dana Board', self.model.prompts[-1])
        self.assertIn('data, not instructions', self.model.prompts[0])
        found = self.read()
        self.assertEqual(found['notes']['text'], NOTES)
        self.assertEqual((found['notes']['by'], found['notes']['written_from']), ('machine', 'transcript'))
        self.assertIsNone(found['writing'])
        self.assertEqual(found['transcript']['text'], LONG)  # the transcript stays as it was
        with self.store.connect() as db:
            row = db.execute("SELECT * FROM events WHERE kind='meeting.notes' AND source_id=?", (f'notes:{self.board}',)).fetchone()
            self.assertLess(row['analyzed_version'], row['version'])  # the next review reads them for the follow-ups
            self.assertEqual(meeting_notes.for_event(db, self.board, '2026-10-28')['id'], row['id'])
            self.assertIn('dana@board.example', json.dumps(json.loads(row['metadata'])['attendees']))

    def test_a_short_transcript_is_one_turn(self):
        self.transcript(SHORT)
        self.generate()
        self.wait()
        self.assertEqual(len(self.model.prompts), 1)
        self.assertIn('<transcript>\n' + SHORT, self.model.prompts[0])

    def test_only_with_a_transcript_and_without_notes_and_only_the_owner(self):
        with self.assertRaisesRegex(ValueError, 'no transcript'):
            self.generate()
        self.transcript(SHORT)
        with self.assertRaisesRegex(ValueError, 'Only the owner'):
            self.app.action('meeting_notes_write', {'event_id': self.board})
        self.app.action('meeting_notes', {'event_id': self.board, 'text': 'My own notes'}, owner_dashboard=True)
        with self.assertRaisesRegex(ValueError, 'notes already'):
            self.generate()
        self.assertEqual(self.model.prompts, [])

    def test_notes_that_come_in_while_it_writes_are_never_overwritten(self):
        self.transcript(SHORT)
        with self.store.connect() as db:
            meeting_writer.start(db, self.board, a.now())
        original = self.model.answer

        def owner_writes_meanwhile(config, prompt):
            self.app.action('meeting_notes', {'event_id': self.board, 'text': 'The owner’s notes'}, owner_dashboard=True)
            return original
        self.app.notes_model = owner_writes_meanwhile
        self.app.meeting_write_run(self.board)
        found = self.read()
        self.assertEqual((found['notes']['text'], found['notes']['by']), ('The owner’s notes', 'owner'))
        self.assertIsNone(found['writing'])

    def test_it_waits_while_a_usage_limit_holds_and_goes_on_from_the_part_it_reached(self):
        self.transcript()
        with self.store.connect() as db:
            meeting_writer.start(db, self.board, a.now())
        calls = []
        model = self.model

        def limit_after_two(config, prompt):
            calls.append(prompt)
            if len(calls) == 2:
                self.paused = {'window': '5h', 'until': time.time() + 3600, 'limited': True}
            return model(config, prompt)
        self.app.notes_model = limit_after_two
        self.app.meeting_write_run(self.board)
        writing = self.read()['writing']
        self.assertEqual((writing['status'], writing['done'], writing['total']), ('waiting', 2, 4))
        self.assertGreater(writing['until'], time.time())
        self.assertIsNone(self.read()['notes'])
        self.paused = None
        self.app.meeting_write_run(self.board)
        self.assertEqual(len(calls), 4)  # parts 1 and 2 aren't asked again
        self.assertEqual(self.read()['notes']['text'], NOTES)

    def test_a_model_that_cant_be_reached_fails_visibly_and_can_be_tried_again(self):
        self.transcript(SHORT)
        self.model.fail = 1
        self.generate()
        self.wait()
        writing = self.read()['writing']
        self.assertEqual((writing['status'], writing['error']), ('failed', 'model'))
        self.assertEqual(self.generate()['writing']['status'], 'queued')
        self.wait()
        self.assertEqual(self.read()['notes']['text'], NOTES)

    def test_a_job_that_ran_at_a_stop_starts_over_at_the_next_start(self):
        self.transcript(SHORT)
        with self.store.connect() as db:
            meeting_writer.start(db, self.board, a.now())
            meeting_writer.mark(db, self.board, a.now(), status='running', done=1, total=3)
        self.app.meeting_write_resume()
        self.wait()
        self.assertEqual(self.read()['notes']['by'], 'machine')

    def test_the_owner_editing_them_makes_them_the_owners(self):
        self.transcript(SHORT)
        self.generate()
        self.wait()
        self.app.action('meeting_notes', {'event_id': self.board, 'text': NOTES + '\n- **Sam**: book the room'}, owner_dashboard=True)
        found = self.read()['notes']
        self.assertEqual(found['by'], 'owner')
        self.assertNotIn('written_from', found)

    def test_parts_are_cut_between_lines_and_never_inside_a_character(self):
        parts = meeting_writer.chunks(LONG)
        self.assertEqual('\n'.join(parts), LONG)
        self.assertTrue(all(len(p.encode()) <= meeting_writer.CHUNK_BYTES for p in parts))
        self.assertTrue(all(p.split('\n')[0].startswith('[') for p in parts))
        wide = 'é' * 70_000  # one long line of two-byte characters
        cut = meeting_writer.chunks(wide)
        self.assertEqual(''.join(cut), wide)
        self.assertTrue(all(len(p.encode()) <= meeting_writer.CHUNK_BYTES for p in cut))
        self.assertEqual(meeting_writer.chunks(SHORT), [SHORT])

    def test_the_answer_is_cleaned_into_notes(self):
        self.assertEqual(meeting_writer.clean_notes('```markdown\n## Summary\n\nDone.\n```'), '## Summary\n\nDone.')
        self.assertEqual(len(meeting_writer.clean_notes('x' * 20_000)), meeting_writer.NOTES_CHARS)


if __name__ == '__main__':
    unittest.main()

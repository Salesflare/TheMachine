"""One meeting, one record (meeting_mail.py): a meeting's notes by mail from the meeting app, its Zoom summary and its
calendar event edited after it began are the same meeting's notes. They make one to-do per next step, with the meeting
as its source ("notes from Board meeting Q4"), and the same notes coming another way join that to-do quietly. Matching
a mail to its meeting is plain code (the Zoom ID, the title, the time), never a model. No live calls, made-up people."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('meeting_mail_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
import meeting_mail  # noqa: E402
from seams import patch_everywhere  # noqa: E402

WORK = {'id': 'cal', 'email': 'owner@example.com', 'service': 'calendar', 'boundary': 'work:Example'}
GUESTS = [{'email': 'owner@example.com', 'self': True}, {'email': 'dana@board.example', 'displayName': 'Dana Board'}]
AFTER = dt.datetime(2026, 10, 29, 9, 0, tzinfo=dt.timezone.utc)  # the day after the meetings


def raw(source_id, title, start, end, **extra):
    return {'id': source_id, 'summary': title, 'start': {'dateTime': start}, 'end': {'dateTime': end}, 'status': 'confirmed',
            'htmlLink': 'https://calendar.google.com/calendar/event?eid=' + source_id, 'attendees': GUESTS,
            'updated': '2026-10-20T10:00:00Z', **extra}


def mail(source_id, sender, at, title, body='Summary and next steps of the call.'):
    return {'account_id': 'mail', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': title, 'body': body,
            'metadata': {'from': sender, 'to': 'owner@example.com', 'labels': ['INBOX'], 'thread_id': source_id}, 'deleted': False}


class MeetingMail(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.tz = patch_everywhere(a, 'local_tz', return_value=a.ZoneInfo('Europe/Brussels'))
        self.tz.start()
        self.addCleanup(self.tz.stop)
        self.store.commit_page('cal', {}, [
            a.calendar_event(WORK, raw('board', 'Board meeting Q4', '2026-10-28T14:00:00+01:00', '2026-10-28T15:00:00+01:00'), 'Europe/Brussels'),
            a.calendar_event(WORK, raw('standup', 'Standup', '2026-10-28T09:00:00+01:00', '2026-10-28T09:15:00+01:00'), 'Europe/Brussels')])
        self.store.commit_page('zoom', {}, [
            {'account_id': 'zoom', 'source_id': 'summary:1', 'kind': 'zoom.summary', 'occurred_at': '2026-10-28T13:01:00+00:00',
             'title': 'Board meeting Q4', 'body': '## Next steps\n\n- Owner sends the board the revised budget by Friday',
             'metadata': {'meeting_id': '123456789', 'start_at': '2026-10-28T13:01:00+00:00', 'end_at': '2026-10-28T13:58:00+00:00',
                          'host_email': 'owner@example.com'}, 'deleted': False}])
        self.store.commit_page('mail', {}, [
            mail('zoom-mail', 'Zoom <no-reply@zoom.us>', '2026-10-28T14:05:00+00:00', 'Meeting assets for Board meeting Q4 are ready!'),
            mail('dana-mail', 'Dana Board <dana@board.example>', '2026-10-28T14:20:00+00:00', 'The deck we discussed')])
        self.ids = self.event_ids()

    def event_ids(self):
        with self.store.connect() as db:
            return {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def card(self, card_id):
        with self.store.connect() as db:
            return db.execute('SELECT * FROM suggestions WHERE id=?', (card_id,)).fetchone()

    def suggest(self, key, ids, **extra):
        return self.store.suggest(key, 'Send the board the revised budget', 'Agreed in the board meeting: the revised budget by Friday.',
                                  ids, match=True, **extra)

    def test_a_notes_mail_is_matched_to_its_meeting_by_plain_code(self):
        with self.store.connect() as db:
            zoom_mail = meeting_mail._full(db, self.ids['zoom-mail'])
            self.assertTrue(meeting_mail.notes_mail(zoom_mail))
            self.assertEqual(meeting_mail.mail_meeting(db, zoom_mail)['id'], self.ids['board'])
            self.assertFalse(meeting_mail.notes_mail(meeting_mail._full(db, self.ids['dana-mail'])))  # a person's mail is just mail
            # by when alone: the meeting that just ended, not the morning standup
            untitled = {**zoom_mail, 'title': 'Your meeting summary is ready'}
            self.assertEqual(meeting_mail.mail_meeting(db, untitled)['id'], self.ids['board'])
        # two meetings ending at about the same time, and nothing else telling them apart: none (never another meeting's)
        self.store.commit_page('cal', {}, [a.calendar_event(WORK, raw('sync', 'Vendor sync', '2026-10-28T14:30:00+01:00', '2026-10-28T15:05:00+01:00'),
                                                            'Europe/Brussels')])
        with self.store.connect() as db:
            self.assertIsNone(meeting_mail.mail_meeting(db, untitled))
            self.assertEqual(meeting_mail.mail_meeting(db, zoom_mail)['id'], self.ids['board'])  # its title still names one

    def test_the_review_is_told_the_meeting_and_its_record_on_a_notes_mail(self):
        with self.store.connect() as db:
            told = meeting_mail.hint(db, meeting_mail._full(db, self.ids['zoom-mail']), at=AFTER)
            self.assertEqual((told['event_id'], told['title'], told['notes_event_id']), (self.ids['board'], 'Board meeting Q4', self.ids['summary:1']))
            self.assertIn('never a second to-do', told['rule'])
            self.assertIsNone(meeting_mail.hint(db, meeting_mail._full(db, self.ids['dana-mail']), at=AFTER))
            self.assertIsNone(meeting_mail.hint(db, meeting_mail._full(db, self.ids['standup']), at=AFTER))  # no notes in it

    def test_one_to_do_led_by_the_meeting_whichever_way_its_notes_came_first(self):
        first = self.suggest('board:budget', [self.ids['zoom-mail'], self.ids['board']])
        card = self.card(first['id'])
        self.assertTrue(card['source_line'].startswith('Source: notes from Board meeting Q4 · '), card['source_line'])
        self.assertNotIn('Zoom', card['source_line'])
        with self.assertRaises(ValueError) as held:  # Zoom's own summary later: the review is asked, never a second to-do
            self.suggest('board:budget-zoom', [self.ids['summary:1']])
        self.assertIn(first['id'], str(held.exception))
        with self.store.connect() as db:
            told = meeting_mail.hint(db, meeting_mail._full(db, self.ids['summary:1']), at=AFTER)
        self.assertEqual([t['id'] for t in told['todos']], [first['id']])
        before = (card['status'], card['deliver_after'])
        joined = self.suggest('board:budget-zoom', [self.ids['summary:1']], card_id=first['id'])
        self.assertTrue(joined['attached'])
        card = self.card(first['id'])
        self.assertEqual((card['status'], card['deliver_after']), before)  # no news: not brought back or sent again
        self.assertEqual(json.loads(card['event_ids'])[0], self.ids['summary:1'])
        self.assertTrue(card['source_line'].startswith('Source: notes from Board meeting Q4 · '), card['source_line'])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM suggestions").fetchone()[0], 1)

    def test_the_mail_after_zoom_joins_quietly_and_never_leads(self):
        first = self.suggest('board:budget', [self.ids['summary:1']])
        self.assertTrue(self.card(first['id'])['source_line'].startswith('Source: notes from Board meeting Q4 · '))
        joined = self.suggest('board:budget-mail', [self.ids['zoom-mail']], card_id=first['id'])
        self.assertTrue(joined['attached'])
        card = self.card(first['id'])
        self.assertEqual(json.loads(card['event_ids'])[0], self.ids['zoom-mail'])  # newest first, as always
        self.assertTrue(card['source_line'].startswith('Source: notes from Board meeting Q4 · '), card['source_line'])  # the meeting leads

    def test_a_persons_mail_keeps_leading_its_own_to_do(self):
        first = self.suggest('board:deck', [self.ids['dana-mail'], self.ids['summary:1']])
        self.assertTrue(self.card(first['id'])['source_line'].startswith('Source: email from Dana Board'), self.card(first['id'])['source_line'])
        # only a notes mail alone: no meeting in its evidence, so it says what it is
        alone = self.suggest('other', [self.ids['zoom-mail']], separate=True)
        self.assertTrue(self.card(alone['id'])['source_line'].startswith('Source: email from Zoom'))

    def test_a_calendar_event_edited_after_it_began_brings_its_notes_to_the_review(self):
        notes = 'Decisions: budget approved.\nNext steps: owner sends the revised budget to the board by Friday.'
        edited = raw('board', 'Board meeting Q4', '2026-10-28T14:00:00+01:00', '2026-10-28T15:00:00+01:00',
                     description=notes, updated='2026-10-28T14:10:00Z')
        self.store.commit_page('cal', {}, [a.calendar_event(WORK, edited, 'Europe/Brussels')])
        with self.store.connect() as db:
            event = meeting_mail._full(db, self.ids['board'])
            told = meeting_mail.hint(db, event, at=AFTER)
            self.assertEqual(told['event_id'], self.ids['board'])
            self.assertIn('description now holds notes', told['rule'])
            # before it ended, or with only an agenda written before it: nothing to tell
            self.assertIsNone(meeting_mail.hint(db, event, at=dt.datetime(2026, 10, 28, 13, 30, tzinfo=dt.timezone.utc)))
        self.store.commit_page('cal', {}, [a.calendar_event(WORK, {**edited, 'updated': '2026-10-27T10:00:00Z'}, 'Europe/Brussels')])
        with self.store.connect() as db:
            self.assertIsNone(meeting_mail.hint(db, meeting_mail._full(db, self.ids['board']), at=AFTER))

    def test_the_review_batch_carries_the_meeting(self):
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM events WHERE id IN (?,?)', (self.ids['zoom-mail'], self.ids['dana-mail']))]
        hints = self.store.meeting_hints({}, rows)
        self.assertEqual(hints[self.ids['zoom-mail']]['meeting']['event_id'], self.ids['board'])
        self.assertNotIn(self.ids['dana-mail'], hints)


if __name__ == '__main__':
    unittest.main()

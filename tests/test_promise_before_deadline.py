"""Someone else's promise that an open to-do with a deadline waits on is checked before that deadline. A test persona's
conference chair promised the exact event date, undated, while the slot to confirm it ran out on Friday: the follow-up
came a week later, on the Monday after. No live calls."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import test_ux as ux
import timeutil
from seams import patch_everywhere  # noqa: E402
a = ux.a

MONDAY = '2026-11-09T01:30:00+00:00'


def email(source_id, at, body, thread='conf'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Spring summit talk',
            'body': body, 'deleted': False,
            'metadata': {'from': 'Dana Reyes <dana@summit.example>', 'to': 'owner@example.com', 'thread_id': thread, 'labels': ['INBOX']}}


class PromiseBeforeDeadline(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        zone = patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        zone.start()
        self.addCleanup(zone.stop)
        clock = patch_everywhere(a, 'now', return_value=MONDAY)
        clock.start()
        self.addCleanup(clock.stop)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [
            email('invite', '2026-11-08T15:00:00+00:00', 'Would you give a talk? Please confirm by Friday, November 13 to keep the slot.'),
            email('date', '2026-11-09T01:20:00+00:00', 'I will send you the exact date in March as soon as the venue confirms.'),
            email('other', '2026-11-09T01:21:00+00:00', 'I will send the venue map.', thread='map')])
        with self.store.connect() as db:
            self.ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}

    def promise(self, event='date', what='send the exact March date'):
        return self.store.promise({'direction': 'theirs', 'event_id': self.ids[event], 'who': 'Dana Reyes', 'what': what})

    def test_checked_the_morning_before_the_deadline_it_blocks(self):
        self.store.suggest('conf', 'Confirm the summit talk', 'The slot runs out on Friday.', [self.ids['invite']], due='2026-11-13')
        saved = self.promise()
        self.assertEqual(saved['check_at'], '2026-11-12T07:30:00+00:00')  # Thursday 08:30 in Brussels, not Monday the 16th

    def test_a_deadline_that_comes_later_pulls_it_forward(self):
        saved = self.promise()
        self.assertEqual(saved['check_at'], '2026-11-16T07:30:00+00:00')  # nothing waits on it yet: a week, as before
        self.store.suggest('conf', 'Confirm the summit talk', 'The slot runs out on Friday.', [self.ids['date'], self.ids['invite']], due='2026-11-13')
        with self.store.connect() as db:
            self.store.settle_promises(db)
            self.assertEqual(db.execute('SELECT check_at FROM promises WHERE id=?', (saved['id'],)).fetchone()[0], '2026-11-12T07:30:00+00:00')

    def test_a_promise_no_deadline_waits_on_keeps_its_week(self):
        self.store.suggest('conf', 'Confirm the summit talk', 'The slot runs out on Friday.', [self.ids['invite']], due='2026-11-13')
        self.assertEqual(self.promise('other', 'send the venue map')['check_at'], '2026-11-16T07:30:00+00:00')


if __name__ == '__main__':
    unittest.main()

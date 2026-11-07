"""A review's to-do saves (machine/app/review_saves.py, machine/store/review_saves.py): a trial review left out
dedupe_key on every suggest, got "Reload the page and try again" each time, and then finished with all its messages
marked reviewed, so none came back and no to-do was made. Now the key is made from the source message, wrong args get
an answer the review can act on, and messages whose save failed stay unreviewed for the next review."""
import datetime as dt
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402
from machine.store import review_saves  # noqa: E402

spec = importlib.util.spec_from_file_location('review_saves_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def mail(source_id, hours_ago, thread):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'title': 'Pricing',
            'occurred_at': (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours_ago)).isoformat(),
            'body': 'Could you send the pricing?', 'deleted': False,
            'metadata': {'from': 'Sam <sam@example.com>', 'thread_id': thread, 'labels': ['INBOX']}}


class ReviewSaves(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'transport': 'gog', 'email': 'owner@example.com'}]}
        self.store.commit_page('work', {}, [mail('m1', 3, 'thread-a'), mail('m2', 2, 'thread-b')])

    def suggest(self, **args):
        return self.app.action('suggest', {'title': 'Send Sam the pricing', 'body': 'Sam asked for the pricing. I can draft it.', 'event_ids': [1], **args})

    def row(self, sql, *args):
        with self.store.connect() as db:
            return db.execute(sql, args).fetchone()

    def test_a_missing_dedupe_key_is_made_from_the_source_message(self):
        saved = self.suggest()
        self.assertTrue(saved['id'])
        self.assertEqual(self.row('SELECT dedupe_key FROM suggestions WHERE id=?', saved['id'])[0], 'work:thread-a:send-sam-the-pricing')
        again = self.suggest(body='Sam asked again for the pricing. I can draft it.')  # the same matter: the same to-do
        self.assertEqual(again['id'], saved['id'])
        self.assertEqual(self.row('SELECT count(*) FROM suggestions')[0], 1)

    def test_wrong_args_are_told_back_in_words(self):
        with self.assertRaisesRegex(ValueError, 'title and body.*not in suggestion'):
            self.app.action('suggest', {'suggestion': 'Send Sam the pricing', 'event_ids': [1]})
        with self.assertRaisesRegex(ValueError, 'needs event_ids'):
            self.suggest(event_ids=None)
        with self.assertRaisesRegex(ValueError, r'Unknown event_ids \[99\]'):
            self.suggest(event_ids=[1, 99])

    def test_a_failed_save_keeps_its_messages_for_the_next_review(self):
        claim = self.store.begin_analysis(['work'], 40)
        self.assertEqual({e['id'] for e in claim['events']}, {1, 2})
        with patch.object(self.store, 'suggest', side_effect=sqlite3.OperationalError('database is locked')):
            with self.assertRaisesRegex(ValueError, 'was not saved.*try once more'):
                self.suggest()
        done = self.store.finish_analysis(claim['analysis_id'], 'One to-do')
        self.assertEqual(done['not_saved'], [1])
        self.assertEqual(tuple(self.row('SELECT analyzed_version, deferrals FROM events WHERE id=1')), (0, 0))  # back next time
        self.assertEqual(self.row('SELECT analyzed_version FROM events WHERE id=2')[0], 1)
        claim = self.store.begin_analysis(['work'], 40)  # the next review gets it, saves it, and it is reviewed
        self.assertEqual([e['id'] for e in claim['events']], [1])
        self.assertTrue(self.suggest()['id'])
        self.assertNotIn('not_saved', self.store.finish_analysis(claim['analysis_id'], 'One to-do'))
        self.assertEqual(self.row('SELECT analyzed_version FROM events WHERE id=1')[0], 1)

    def test_failed_saves_never_set_a_message_aside(self):
        # A test review's saves failed twice for the same messages; each failure counted as a deferral, so after two
        # (SET_ASIDE_AFTER) they were set aside: never reviewed again and no to-do. Now a failed save holds a message back
        # without a deferral, up to MAX_TRIES failures, after which it is reviewed like any other.
        for n in range(review_saves.MAX_TRIES + 1):
            claim = self.store.begin_analysis(['work'], 40)
            self.assertIn(1, [e['id'] for e in claim['events']], f'review {n + 1}')
            with patch.object(self.store, 'suggest', side_effect=sqlite3.OperationalError('database is locked')):
                with self.assertRaises(ValueError):
                    self.suggest()
            done = self.store.finish_analysis(claim['analysis_id'], 'No to-do saved')
            if n < review_saves.MAX_TRIES:
                self.assertEqual(done['not_saved'], [1])
                self.assertEqual(tuple(self.row('SELECT analyzed_version, deferrals FROM events WHERE id=1')), (0, 0))
        self.assertNotIn('not_saved', done)
        self.assertEqual(self.row('SELECT analyzed_version FROM events WHERE id=1')[0], 1)

    def test_a_failure_holds_back_once(self):
        claim = self.store.begin_analysis(['work'], 40)
        with patch.object(self.store, 'suggest', side_effect=sqlite3.OperationalError('database is locked')):
            with self.assertRaises(ValueError):
                self.suggest()
        self.assertEqual(self.store.finish_analysis(claim['analysis_id'], 'x')['not_saved'], [1])
        claim = self.store.begin_analysis(['work'], 40)  # this review decides on no to-do: reviewed, not held again
        self.assertNotIn('not_saved', self.store.finish_analysis(claim['analysis_id'], 'Nothing to do'))
        self.assertEqual(self.row('SELECT analyzed_version FROM events WHERE id=1')[0], 1)

    def test_read_what_came_after_first_is_a_step_not_a_failed_save(self):
        claim = self.store.begin_analysis(['work'], 40)
        with patch.object(self.app, 'newer_unchecked', return_value=[{'id': 2}]), patch_everywhere(a, 'activity_lines', return_value='2 Sam'):
            with self.assertRaisesRegex(ValueError, 'Something happened after'):
                self.suggest()
        self.assertNotIn('not_saved', self.store.finish_analysis(claim['analysis_id'], 'Handled already'))
        self.assertEqual(self.row('SELECT analyzed_version FROM events WHERE id=1')[0], 1)


if __name__ == '__main__':
    unittest.main()

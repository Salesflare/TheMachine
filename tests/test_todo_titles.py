"""To-do titles are short and whole: a promise's title never stops mid-sentence ("... and verify they still"), a long
one ends at a clause or word with an ellipsis, and titles an older version cut that way get their whole title back.
A stuck prepared-ahead to-do leads with Try again. No live calls."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import test_ux as ux
import timeutil
from test_promises import GMAIL, SLACK, MONDAY, email
a = ux.a

LONG_MINE = 'mark the Acme Sync and Beta Bridge apps as trusted clients and verify they still work after it'
LONG_THEIRS = 'log the release blocker and investigate limiting the number of briefing tasks per morning'


class FitTitle(unittest.TestCase):
    def test_a_title_that_fits_stays_as_it_is(self):
        self.assertEqual(a.fit_title('  Send the   signed contract '), 'Send the signed contract')

    def test_a_long_title_ends_at_a_clause(self):
        title = a.fit_title('Mark the Acme Sync and Beta Bridge apps as trusted clients and verify they still work after it')
        self.assertEqual(title, 'Mark the Acme Sync and Beta Bridge apps as trusted clients…')

    def test_without_a_clause_it_ends_at_a_word_without_hanging_words(self):
        title = a.fit_title('Check the queries that determine exactly how many of the users would receive the meeting emails today', 90)
        self.assertLessEqual(len(title), 90)
        self.assertTrue(title.endswith('…'), title)
        self.assertNotIn(title[:-1].split()[-1].casefold(), a.TITLE_DANGLING)
        self.assertTrue(('Check the queries that determine exactly how many of the users would receive the meeting emails today').startswith(title[:-1]))

    def test_the_prefix_is_never_the_whole_title(self):
        title = a.fit_title('Waiting on Sam: ' + LONG_THEIRS + ' and more', 60, keep=len('Waiting on Sam: '))
        self.assertTrue(title.startswith('Waiting on Sam: log the release blocker'), title)
        self.assertLessEqual(len(title), 60)

    def test_one_long_word_is_cut_with_an_ellipsis(self):
        self.assertEqual(a.fit_title('x' * 120, 20), 'x' * 19 + '…')


class PromiseTitles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        zone = patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        zone.start()
        self.addCleanup(zone.stop)
        clock = patch.object(a, 'now', return_value='2026-10-30T07:00:00+00:00')
        clock.start()
        self.addCleanup(clock.stop)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}
        self.store.commit_page('work', {}, [email('theirs', '2026-10-19T08:00:00+00:00'), email('mine', '2026-10-19T08:30:00+00:00', sent=True, title='Re: Deck')])
        with self.store.connect() as db:
            self.theirs, self.mine = [r[0] for r in db.execute('SELECT id FROM events ORDER BY source_id DESC')]

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}}
        app.promise_check_model = lambda config, text: '[]'
        return app

    def stored(self, direction, what, who='Sam Lee'):
        """A promise as an older version kept them: `what` up to 140 characters."""
        with self.store.connect() as db:
            return db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,'open',?,?)",
                              (direction, who, what, None, MONDAY, self.mine if direction == 'mine' else self.theirs, 'work', MONDAY, MONDAY)).lastrowid

    def titles(self):
        return {c['dedupe_key']: c['title'] for c in self.store.snapshot([])['suggestions']}

    def test_a_long_promise_is_asked_to_be_said_shorter(self):
        with self.assertRaisesRegex(ValueError, 'say it shorter'):
            self.app().action('promise', {'direction': 'mine', 'event_id': self.mine, 'who': 'Sam Lee', 'what': LONG_MINE})
        self.assertEqual(self.app().action('promise', {'direction': 'mine', 'event_id': self.mine, 'who': 'Sam Lee',
                                                       'what': 'mark the two apps as trusted clients'})['status'], 'open')

    def test_a_long_promise_gets_a_whole_title(self):
        mine, theirs = self.stored('mine', LONG_MINE), self.stored('theirs', LONG_THEIRS)
        self.app().promise_step()
        titles = self.titles()
        self.assertEqual(titles[f'promise:{mine}'], 'Mark the Acme Sync and Beta Bridge apps as trusted clients…')
        # Theirs: the first name when the full one makes it too long (the person chip says who), then a clause
        self.assertEqual(titles[f'promise:{theirs}'], 'Waiting on Sam: log the release blocker…')

    def test_titles_an_older_version_cut_are_made_whole_again(self):
        mine, theirs, renamed = self.stored('mine', LONG_MINE), self.stored('theirs', LONG_THEIRS, who='Alex Kim'), self.stored('mine', LONG_MINE + ' too', who='Bo')
        self.app().promise_step()
        with self.store.connect() as db:
            # How they looked before: chopped at 90 characters, mid-sentence; one the owner renamed since
            for pid, old in [(mine, 'Mark ' + LONG_MINE[5:]), (theirs, 'Waiting on Alex Kim: ' + LONG_THEIRS), (renamed, 'Mark ' + (LONG_MINE + ' too')[5:])]:
                db.execute('UPDATE suggestions SET title=? WHERE dedupe_key=?', (old[:90], f'promise:{pid}'))
            db.execute("UPDATE suggestions SET title='Trust both apps',title_source='user' WHERE dedupe_key=?", (f'promise:{renamed}',))
            self.store.settle_promises(db)
        titles = self.titles()
        self.assertEqual(titles[f'promise:{mine}'], 'Mark the Acme Sync and Beta Bridge apps as trusted clients…')
        self.assertEqual(titles[f'promise:{theirs}'], 'Waiting on Alex: log the release blocker…')
        self.assertEqual(titles[f'promise:{renamed}'], 'Trust both apps')
        # A review's own later title stays too
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET title='Check both apps with Sam' WHERE dedupe_key=?", (f'promise:{mine}',))
            self.store.settle_promises(db)
        self.assertEqual(self.titles()[f'promise:{mine}'], 'Check both apps with Sam')


class StuckAheadLeadsWithTryAgain(unittest.TestCase):
    def test_telegram_buttons(self):
        row = {'id': 'c1', 'status': 'pending', 'title': 'Check the client settings', 'preparation_status': 'blocked',
               'preparation_reason': 'The settings page timed out; try again when browser access works.',
               'preparation_questions': [], 'preparation_no_questions': True, 'next_action': None}
        labels = [b['label'] for block in a.controls(row)['blocks'] for b in block['buttons']]
        self.assertEqual(labels[0], 'Try again')
        self.assertNotIn('Do it', labels)
        labels = [b['label'] for block in a.controls({**row, 'preparation_status': None})['blocks'] for b in block['buttons']]
        self.assertEqual(labels[0], 'Do it')


if __name__ == '__main__':
    unittest.main()

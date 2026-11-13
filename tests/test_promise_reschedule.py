"""A promise given a new date moves the one there is (its to-do too), never a second one: the review moves it by its
id, and one noted again as a new promise merges into the first when the check reads them as the same thing. Different
promises by the same person, and promises the other way, stay apart. No live calls: the model is a stand-in."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

import test_ux as ux
import timeutil
from seams import patch_everywhere  # noqa: E402
from test_promises import GMAIL, MONDAY, SLACK, email

a = ux.a


class PromiseReschedule(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        zone = patch.object(timeutil, 'LOCAL_TZ', ZoneInfo('Europe/Brussels'))
        zone.start()
        self.addCleanup(zone.stop)
        self.clock = patch_everywhere(a, 'now', return_value=MONDAY)
        self.clock.start()
        self.addCleanup(lambda: self.clock.stop())
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.owner_user_ids = {'UOWNER1'}
        first = email('first', '2026-10-19T08:00:00+00:00', title='The new app')
        first['body'] = 'Sure, I will take a look at the new app by Friday.'
        later = email('later', '2026-10-21T08:00:00+00:00', thread='t2', title='The new app, next week')
        later['body'] = 'Sorry, busy week. Pushed to next week: I will try it by Friday the 30th instead.'
        other = email('other', '2026-10-21T09:00:00+00:00', thread='t3', title='Invoice')
        other['body'] = 'I will send the signed invoice on Monday.'
        sent = email('sent', '2026-10-19T08:30:00+00:00', sent=True, title='Re: The new app')
        self.store.commit_page('work', {}, [first, later, other, sent])
        with self.store.connect() as db:
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
        self.first, self.later, self.other, self.sent = ids['first'], ids['later'], ids['other'], ids['sent']
        self.asked = []

    def at(self, stamp):
        self.clock.stop()
        self.clock = patch_everywhere(a, 'now', return_value=stamp)
        self.clock.start()

    def app(self, same=None):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL, SLACK], 'digest_at': '08:30', 'review_worker': {'enabled': True}, 'prepare_ahead': False}
        app.promise_check_model = lambda config, text: '[]'  # the check before a to-do: nothing kept

        def twins(config, text):  # the model judging pairs by meaning: here, the answer the test gives
            self.asked.append(text)
            pairs = [int(line.split()[1].rstrip(':')) for line in text.splitlines() if line.startswith('Pair ')]
            return json.dumps([{'pair': p, 'same': p in (same or ())} for p in pairs])
        app.promise_twin_model = twins
        return app

    def record(self, **args):
        return self.app().action('promise', {'direction': 'theirs', 'event_id': self.first, 'who': 'Sam Lee', 'what': 'take a look at the new app',
                                             'due': '2026-10-23', **args})

    def row(self, promise_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM promises WHERE id=?', (promise_id,)).fetchone())

    def card(self, card_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (card_id,)).fetchone())

    def count(self, table):
        with self.store.connect() as db:
            return db.execute(f'SELECT count(*) FROM {table}').fetchone()[0]

    def carded(self):
        """Their promise, come due a day after its date: a to-do now."""
        promise = self.record()['id']
        self.at('2026-10-24T07:00:00+00:00')
        self.app().promise_step()
        self.assertEqual(self.row(promise)['status'], 'carded')
        return promise, self.row(promise)['suggestion_id']

    def test_the_review_moves_a_promise_that_is_a_to_do_now(self):
        promise, card = self.carded()
        # The review sees it, though it is a to-do now, so a new date moves it instead of making a second promise
        self.assertIn(f'#{promise} Sam Lee → you: take a look at the new app (due Fri, Oct 23;', self.store.promises_text())
        self.assertIn('a to-do now)', self.store.promises_text())
        moved = self.app().action('promise', {'id': promise, 'due': '2026-10-30', 'event_id': self.later})
        self.assertEqual(moved['due'], '2026-10-30')
        self.assertEqual(self.count('promises'), 1)
        self.assertEqual(self.count('suggestions'), 1)
        row, todo = self.row(promise), self.card(card)
        self.assertEqual((row['due'], row['status']), ('2026-10-30', 'carded'))
        # Its to-do moves with it: the new date, the newer message first, out of sight until the morning after
        self.assertEqual(todo['due'], '2026-10-30')
        self.assertEqual(json.loads(todo['event_ids'])[0], self.later)
        self.assertEqual((todo['status'], todo['snoozed_until']), ('snoozed', '2026-10-31T07:30:00+00:00'))
        self.assertIn('for Fri, Oct 30', todo['body'])
        # Its page: a short history line, and both messages, the newer first
        page = self.store.promise_page(promise)
        self.assertIn(('due', '2026-10-30'), [(h['kind'], h.get('detail')) for h in page['history']])
        self.assertNotIn('source', [h['kind'] for h in page['history']])
        self.assertEqual(page['sources'], [self.later, self.first])
        with self.assertRaisesRegex(ValueError, 'newer message'):
            self.app().action('promise', {'id': promise, 'due': '2026-11-02', 'event_id': 999999})

    def test_a_promise_noted_again_with_a_new_date_merges_into_the_first(self):
        # Before the review saw it: the same commitment, worded otherwise, noted as a second promise
        promise, card = self.carded()
        again = self.app().action('promise', {'direction': 'theirs', 'event_id': self.later, 'who': 'sam lee', 'what': 'try the new app', 'due': '2026-10-30'})
        self.assertNotEqual(again['id'], promise)
        self.app(same={again['id']}).promise_step()
        # The check read the pair with both messages, and merged them: one promise, one to-do, the new date
        self.assertEqual(len(self.asked), 1)
        self.assertIn('older, promise %d: take a look at the new app' % promise, self.asked[0])
        self.assertIn('newer, promise %d: try the new app' % again['id'], self.asked[0])
        self.assertIn('Pushed to next week', self.asked[0])
        self.assertEqual((self.row(again['id'])['status'], self.row(again['id'])['note']), ('dropped', f'The same as promise {promise}'))
        self.assertEqual(self.row(promise)['due'], '2026-10-30')
        self.assertEqual(self.card(card)['due'], '2026-10-30')
        self.assertEqual(self.count('suggestions'), 1)
        self.assertEqual(self.store.promise_page(promise)['sources'], [self.later, self.first])
        self.assertEqual([p['id'] for p in self.store.promises() if p['state'] in ('open', 'card')], [promise])
        # Read once: later passes neither ask again nor make a to-do for it
        self.at('2026-10-31T07:00:00+00:00')
        self.app(same={again['id']}).promise_step()
        self.assertEqual((len(self.asked), self.count('suggestions')), (1, 1))

    def test_two_open_promises_merge_before_either_is_a_to_do(self):
        promise = self.record()['id']
        again = self.app().action('promise', {'direction': 'theirs', 'event_id': self.later, 'who': 'Sam Lee', 'what': 'try the new app', 'due': '2026-10-30'})['id']
        self.at('2026-10-21T10:00:00+00:00')
        self.app(same={again}).promise_step()
        self.assertEqual((self.row(promise)['due'], self.row(promise)['status'], self.row(again)['status']), ('2026-10-30', 'open', 'dropped'))
        self.assertEqual(self.row(promise)['check_at'], '2026-10-31T07:30:00+00:00')
        self.assertEqual(self.count('suggestions'), 0)

    def test_different_promises_by_the_same_person_stay_apart(self):
        promise, card = self.carded()
        other = self.app().action('promise', {'direction': 'theirs', 'event_id': self.other, 'who': 'Sam Lee', 'what': 'send the signed invoice', 'due': '2026-10-26'})['id']
        self.app().promise_step()  # the model reads them as different things
        self.app().promise_step()
        self.assertEqual(len(self.asked), 1)  # asked once
        self.assertEqual((self.row(promise)['due'], self.row(promise)['status']), ('2026-10-23', 'carded'))
        self.assertEqual((self.row(other)['due'], self.row(other)['status']), ('2026-10-26', 'open'))
        self.assertEqual(self.card(card)['due'], '2026-10-23')

    def test_promises_the_other_way_are_never_paired(self):
        # Theirs to the owner and the owner's to them: never read as the same promise, nor moved into each other
        theirs = self.record()['id']
        mine = self.app().action('promise', {'direction': 'mine', 'event_id': self.sent, 'who': 'Sam Lee', 'what': 'walk them through the new app',
                                             'due': '2026-10-30'})['id']
        self.app(same={mine, theirs}).promise_step()
        self.assertEqual(self.asked, [])
        self.assertEqual((self.row(theirs)['status'], self.row(theirs)['due'], self.row(theirs)['direction']), ('open', '2026-10-23', 'theirs'))
        self.assertEqual((self.row(mine)['status'], self.row(mine)['due'], self.row(mine)['direction']), ('open', '2026-10-30', 'mine'))
        with self.store.connect() as db:
            self.assertEqual(self.store.promise_twins(db), [])
        # Moving one by its id keeps its direction
        self.app().action('promise', {'id': mine, 'due': '2026-11-02', 'event_id': self.sent})
        self.assertEqual((self.row(mine)['direction'], self.row(theirs)['due']), ('mine', '2026-10-23'))

    def test_a_turn_that_fails_leaves_them_as_they_are(self):
        promise = self.record()['id']
        again = self.app().action('promise', {'direction': 'theirs', 'event_id': self.later, 'who': 'Sam Lee', 'what': 'try the new app', 'due': '2026-10-30'})['id']
        app = self.app()
        app.promise_twin_model = lambda config, text: 'not json ['
        app.promise_step()
        self.assertEqual((self.row(promise)['status'], self.row(again)['status']), ('open', 'open'))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM promise_log WHERE kind='twin'").fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()

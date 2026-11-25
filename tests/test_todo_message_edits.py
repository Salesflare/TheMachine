"""A message edited after the review made its to-do (a corrected amount): the review's update from the same key and the
same evidence reaches the to-do, while a true repeat stays a duplicate (cards.edited_news). Made-up messages only, on a
sealed store as every Machine has by default."""
import datetime as dt
import sqlite3
import tempfile
import unittest
from pathlib import Path

import timeutil
import machine.main as machine_main

ACCOUNTS = [{'id': 'wa', 'service': 'whatsapp', 'boundary': 'personal'}]


def message(body):
    return {'account_id': 'wa', 'source_id': 'm1', 'kind': 'whatsapp.message', 'thread_id': 'chat', 'title': 'Sam',
            'body': body, 'occurred_at': '2026-11-25T10:00:00+00:00', 'deleted': False,
            'metadata': {'chat_id': 'chat', 'sender_display': 'Sam'}}


class EditedMessages(unittest.TestCase):
    def setUp(self):
        timeutil.pin(dt.datetime(2026, 11, 25, 20, 0, tzinfo=dt.timezone.utc))
        self.addCleanup(timeutil.pin, None)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = machine_main.Store(Path(temp.name) / 'e.sqlite', protect=True)
        self.store.accounts = ACCOUNTS
        self.store.commit_page('wa', {}, [message('Please sign the work order, 1,250 euro')])
        with self.store.connect() as db:
            self.event = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()['id']
        self.first = self.store.suggest('wa:work-order', 'Sign the €1,250 work order', 'Sam needs a signature.', [self.event], match=True)

    def edit(self, body='Please sign the work order, 1,520 euro (typo before)'):
        self.store.commit_page('wa', {}, [message(body)])

    def again(self, title='Sign the €1,520 work order', body='Sam corrected the amount.', **kw):
        return self.store.suggest('wa:work-order', title, body, [self.event], card_id=self.first['id'], **{'match': True, **kw})

    def card(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT title,body,event_ids FROM suggestions WHERE id=?', (self.first['id'],)).fetchone())

    def test_an_edited_message_updates_its_to_do_from_the_same_key_and_evidence(self):
        self.edit()
        saved = self.again()
        self.assertFalse(saved['duplicate'])
        self.assertTrue(saved.get('updated'))
        self.assertEqual(self.card()['title'], 'Sign the €1,520 work order')
        self.assertEqual(self.card()['body'], 'Sam corrected the amount.')
        # once taken in, the same word again is a repeat
        self.assertTrue(self.again()['duplicate'])

    def test_a_true_repeat_stays_a_duplicate(self):
        # nothing edited: a reworded read of the same message changes nothing
        self.assertTrue(self.again(title='Sign the work order (€1,250)', body='Sam asks for a signature.')['duplicate'])
        self.assertEqual(self.card()['title'], 'Sign the €1,250 work order')
        # edited, but the to-do reads the same: nothing new either
        self.edit()
        self.assertTrue(self.again(title='Sign the €1,250 work order', body='Sam needs a signature.')['duplicate'])

    def test_a_to_do_from_before_versions_were_noted_keeps_the_old_answer(self):
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET evidence_versions=NULL')
        self.edit()
        self.assertTrue(self.again()['duplicate'])
        self.assertEqual(self.card()['title'], 'Sign the €1,250 work order')

    def test_without_match_the_same_key_is_still_one_to_do(self):
        self.edit()
        self.assertTrue(self.store.suggest('wa:work-order', 'Sign the €1,520 work order', 'Sam corrected it.', [self.event])['duplicate'])
        self.assertEqual(self.card()['title'], 'Sign the €1,250 work order')

    def test_the_store_is_sealed_as_production_stores_it(self):
        conn = sqlite3.connect(self.store.path)
        self.addCleanup(conn.close)
        self.assertNotIn('1,250', str(conn.execute('SELECT body FROM events').fetchone()[0]))
        self.assertNotIn('signature', str(conn.execute('SELECT body FROM suggestions').fetchone()[0]))


if __name__ == '__main__':
    unittest.main()

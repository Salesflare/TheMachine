"""One card per matter: a new signal about something that already has a card updates that card
(and brings it back when it was snoozed or waiting) instead of starting another one."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('matter_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)


def mail(source_id, thread, sender='Sam Example <sam@example.com>', when='2026-10-19T16:22:17+00:00', title='Re: Billing help'):
    return {'account_id': 'g', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': when, 'title': title,
            'body': 'Hi', 'metadata': {'from': sender, 'thread_id': thread}, 'deleted': False}


class Matter(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('g', {}, [
            mail('m1', 't1'),
            mail('m2', 't1', when='2026-10-20T16:50:05+00:00'),
            mail('m3', 't2', sender='Kim Other <kim@example.org>', title='Lunch'),
            mail('m4', 't1', when='2026-10-21T09:00:00+00:00'),
        ])
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'g'}], 'prepare_ahead': False}

    def suggest(self, **args):
        return self.app.action('suggest', {'title': 'Task', 'body': 'Body', 'when': 'now', **args})

    def card(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def wait_for_reply(self, sid):
        """As after a send from the card: snoozed, waiting for their answer, the notification long sent."""
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='snoozed',snoozed_until='2026-10-27T08:30:00+00:00',resume_status='prepared',"
                       "awaiting='{\"delegated\":true}' WHERE id=?", (sid,))
            db.execute("UPDATE deliveries SET status='sent',message_id='42' WHERE suggestion_id=?", (sid,))

    def test_reply_in_the_thread_brings_back_the_waiting_card_instead_of_a_new_one(self):
        first = self.suggest(dedupe_key='billing:offer', title='They offer extra credits', event_ids=[1])
        self.wait_for_reply(first['id'])
        again = self.suggest(dedupe_key='billing:org-confirmation', title='They can add the same amount again', event_ids=[2])
        self.assertEqual(again['id'], first['id'])
        self.assertTrue(again['updated']); self.assertTrue(again['brought_back'])
        card = self.card(first['id'])
        self.assertEqual(card['status'], 'pending')
        self.assertIsNone(card['snoozed_until']); self.assertIsNone(card['awaiting'])
        self.assertEqual(card['title'], 'They can add the same amount again')
        self.assertEqual(json.loads(card['event_ids']), [2, 1])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 1)
            history = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND choice='update'", (first['id'],)).fetchone()
            self.assertIn('They offer extra credits', history['feedback'])
            delivery = db.execute('SELECT status,reminder,needs_edit FROM deliveries WHERE suggestion_id=?', (first['id'],)).fetchone()
            self.assertEqual(tuple(delivery), ('queued', 0, 1))
        # Its older key still finds the same card.
        self.assertTrue(self.suggest(dedupe_key='billing:org-confirmation', event_ids=[2])['duplicate'])

    def test_a_waiting_card_can_come_back_prepared_ahead(self):
        self.app.config['prepare_ahead'] = True
        first = self.suggest(dedupe_key='billing:offer', event_ids=[1])
        self.wait_for_reply(first['id'])
        again = self.suggest(dedupe_key='billing:next', event_ids=[2], prepare_ahead=True)
        self.assertEqual(again['id'], first['id']); self.assertTrue(again['prepared_ahead'])
        card = self.card(first['id'])
        self.assertEqual((card['status'], card['early']), ('accepted', 1))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM preparations WHERE suggestion_id=?', (first['id'],)).fetchone()[0], 'queued')

    def test_a_card_the_reviewer_names_is_updated_across_threads(self):
        first = self.suggest(dedupe_key='lunch', event_ids=[3])
        self.store.decide(first['id'], 'snooze', '', 'd1', 'dashboard', snooze_option='1w')
        same = self.suggest(dedupe_key='billing', event_ids=[1], card_id=first['id'])
        self.assertEqual(same['id'], first['id'])
        self.assertEqual(self.card(first['id'])['status'], 'pending')

    def test_a_different_matter_in_the_same_thread_can_stay_separate(self):
        first = self.suggest(dedupe_key='billing:offer', event_ids=[1])
        other = self.suggest(dedupe_key='billing:invoice-address', event_ids=[2], separate=True)
        self.assertNotEqual(other['id'], first['id'])

    def test_done_card_keeps_the_signal_as_evidence_unless_it_needs_the_owner_again(self):
        first = self.suggest(dedupe_key='billing:offer', event_ids=[1])
        self.store.decide(first['id'], 'complete', '', 'd1', 'dashboard')
        kept = self.suggest(dedupe_key='billing:thanks', event_ids=[2])
        self.assertEqual(kept['id'], first['id']); self.assertTrue(kept['attached'])
        card = self.card(first['id'])
        self.assertEqual(card['status'], 'completed')
        self.assertEqual(json.loads(card['event_ids']), [2, 1])
        again = self.suggest(dedupe_key='billing:new-ask', event_ids=[4], card_id=first['id'], reopen=True)
        self.assertTrue(again['reopened'])
        self.assertEqual(self.card(first['id'])['status'], 'pending')

    def test_open_card_with_the_same_project_is_asked_about_not_duplicated(self):
        first = self.suggest(dedupe_key='lunch', event_ids=[3], project='Billing')
        with self.assertRaisesRegex(ValueError, first['id']):
            self.suggest(dedupe_key='billing', event_ids=[1], project='billing')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 1)
        self.assertEqual(self.suggest(dedupe_key='billing', event_ids=[1], project='billing', card_id=first['id'])['id'], first['id'])

    def test_same_key_with_new_evidence_updates_that_card(self):
        first = self.suggest(dedupe_key='billing', event_ids=[3])
        same = self.suggest(dedupe_key='billing', event_ids=[1], separate=True)
        self.assertEqual(same['id'], first['id']); self.assertTrue(same['updated'])

    def test_internal_cards_keep_their_own_behaviour(self):
        first = self.store.suggest('a', 'Task', 'Body', [1])
        second = self.store.suggest('b', 'Task', 'Body', [2])
        self.assertNotEqual(first['id'], second['id'])
        self.assertTrue(self.store.suggest('a', 'Task', 'Body', [2])['duplicate'])

    def test_slack_thread_and_plain_messages(self):
        rows = [{'account_id': 's', 'kind': 'slack.message', 'metadata': {'channel_id': 'C1', 'message_ts': '1.0', 'thread_ts': '1.0'}},
                {'account_id': 's', 'kind': 'slack.message', 'metadata': {'channel_id': 'C1', 'message_ts': '2.0', 'thread_ts': '1.0'}},
                {'account_id': 's', 'kind': 'slack.message', 'metadata': {'channel_id': 'C1', 'message_ts': '3.0', 'thread_ts': '3.0'}}]
        self.assertEqual(a.thread_keys(rows[:1]), a.thread_keys(rows[1:2]))
        self.assertFalse(a.thread_keys(rows[:1]) & a.thread_keys(rows[2:]))


if __name__ == '__main__':
    unittest.main()

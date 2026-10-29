import json
import unittest
from unittest.mock import patch

import learning_loop
import test_ux as ux
a = ux.a


class LookDone(unittest.TestCase):
    """A to-do that looks done (its run found it done, or a later signal suggests it's handled) is only a hint: it never
    counts as waiting (badge, reminders, nudges), Not done makes it a normal to-do again, and the review and the
    learning pass read that decision."""
    setUp = ux.UX.setUp
    row = ux.UX.row

    def already_done(self):
        self.store.decide(self.sid, 'accept', '', 'accept', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        self.store.prepare(self.sid, 'PR #3451 merged, deployed Oct 27. Nothing is left to do.', job, None, {'state': 'already_done'})

    def test_not_counted_as_waiting(self):
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 1)
        self.already_done()
        self.assertTrue(a.looks_done(self.row()))
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 0)
            # no Ready reminder on Telegram or the phone for it
            db.execute("UPDATE deliveries SET status='queued',reminder=1,error=NULL")
        sent = []

        class Noon(a.dt.datetime):
            @classmethod
            def now(cls, tz=None):
                return a.dt.datetime(2026, 10, 14, 12, tzinfo=a.ZoneInfo('Europe/Brussels')).astimezone(tz or a.dt.timezone.utc)
        config = {'accounts': [{'id': 'work', 'email': 'owner@example.com', 'boundary': 'work:Example'}], 'telegram_owner': '42'}
        with patch.object(a.dt, 'datetime', Noon), patch.object(a, 'telegram', side_effect=lambda *x, **k: (sent.append(x), {'messageId': '7'})[1]), \
                patch.object(a, 'push_notify', side_effect=lambda *x, **k: sent.append(x)):
            a.deliver_one(self.store, config, edit_cards=False)
            self.assertEqual(sent, [])
            with self.store.connect() as db:  # the same reminder for a to-do that needs them still goes
                db.execute("UPDATE suggestions SET outcome=NULL")
            a.deliver_one(self.store, config, edit_cards=False)
        self.assertTrue(sent)
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET outcome=?", (json.dumps({'state': 'already_done'}),))
        app = object.__new__(a.App)
        app.store = self.store
        self.assertFalse(app.notify_open('suggestion:' + self.sid))

    def test_not_done_puts_a_run_found_done_back_and_teaches(self):
        self.already_done()
        result = self.store.decide(self.sid, 'not_done', '', 'nd1', 'dashboard')
        row = self.row()
        self.assertEqual((result['status'], row['status'], row.get('outcome')), ('pending', 'pending', None))
        self.assertFalse(a.looks_done(row))
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 1)
            choice, note = db.execute("SELECT choice,feedback FROM decisions WHERE id='nd1'").fetchone()
            self.assertEqual(choice, 'not_done')
            self.assertIn('PR #3451 merged, deployed Oct 27.', note)
            self.assertTrue(any(s['what'].startswith('said it was not done') for s in learning_loop.signals(db, '2000-01-01')))
        self.assertIn('Not done (it looked done)', self.store.notes_to_learn())
        with self.assertRaises(ValueError):  # it no longer looks done
            self.store.decide(self.sid, 'not_done', '', 'nd2', 'dashboard')

    def test_not_done_clears_a_hint_and_a_stale_hint_cannot_come_back(self):
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events').fetchone()[0]
        self.store.looks_handled(self.sid, 'Sam replied on Tuesday', [event])
        self.assertTrue(a.looks_done(self.row()))
        self.store.decide(self.sid, 'not_done', '', 'nd1', 'dashboard')
        row = self.row()
        self.assertEqual((row['status'], row.get('handled_hint')), ('pending', None))
        with self.store.connect() as db:
            self.assertIn('Sam replied on Tuesday', db.execute("SELECT feedback FROM decisions WHERE id='nd1'").fetchone()[0])
        # the same evidence again is refused; only a newer signal can say it's handled after all
        self.assertIn('skipped', self.store.looks_handled(self.sid, 'Sam replied on Tuesday', [event]))
        self.assertIsNone(self.row().get('handled_hint'))

    def test_the_chat_shows_it_as_an_event_line(self):
        self.already_done()
        self.store.decide(self.sid, 'not_done', '', 'nd1', 'dashboard')
        self.assertEqual(a.CHAT_OWNER_WORDS['not_done'], 'Not done yet')

    def test_waiting_on_others_is_not_for_the_owner_until_a_new_message(self):
        self.store.decide(self.sid, 'accept', '', 'accept', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        self.store.prepare(self.sid, 'The hotfix PR is open and waits on review.', job, None, {'state': 'waiting', 'waiting_on': 'the hotfix review'})
        row = self.row()
        self.assertTrue(a.waits_on_others(row))
        self.assertFalse(a.looks_done(row))
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 0)
        app = object.__new__(a.App)
        app.store = self.store
        self.assertFalse(app.notify_open('suggestion:' + self.sid))
        # The open step moves (a new message on the matter): an open to-do again, counted
        self.store.commit_page('work', {}, [ux.event(source='two', body='Review done, merged')])
        again = self.store.suggest('task', 'Prepare a draft', 'The review is done.', [2], card_id=self.sid, match=True)
        self.assertEqual(again['id'], self.sid)
        row = self.row()
        self.assertEqual((row['status'], row.get('outcome')), ('pending', None))
        self.assertFalse(a.waits_on_others(row))
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 1)

    def test_evidence_line_is_the_first_sentence(self):
        self.assertEqual(a.first_sentence('**PR #3451** [merged](https://x.example/1), deployed Oct 27. Nothing left.'),
                         'PR #3451 merged, deployed Oct 27.')


if __name__ == '__main__':
    unittest.main()

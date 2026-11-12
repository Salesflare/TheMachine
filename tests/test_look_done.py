import json
import unittest
from unittest.mock import patch

import learning_loop
from machine.store.cards import wait_until
import test_ux as ux
from seams import patch_everywhere  # noqa: E402
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
        with patch.object(a.dt, 'datetime', Noon), patch_everywhere(a, 'telegram', side_effect=lambda *x, **k: (sent.append(x), {'messageId': '7'})[1]), \
                patch_everywhere(a, 'push_notify', side_effect=lambda *x, **k: sent.append(x)):
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

    def test_a_ready_to_do_without_an_outcome_counts_as_waiting(self):
        # Most ready drafts have no outcome: NOT (... json_extract(NULL) ...) was NULL, so they were left out of the
        # badge and the morning digest's ready part.
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',outcome=NULL")
            self.assertEqual(a.waiting_count(db), 1)
            db.execute("UPDATE suggestions SET outcome=?", (json.dumps({'state': 'waiting'}),))
            self.assertEqual(a.waiting_count(db), 0)

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

    # a day later it closes by itself (Store.close_looks_done), so the list only holds what is really open

    def hinted(self, at='2026-11-09T10:00:00+00:00'):
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events').fetchone()[0]
        with patch_everywhere(a, 'now', return_value=at):
            self.store.looks_handled(self.sid, 'Sam replied on Tuesday', [event])

    def close_at(self, at):
        with patch_everywhere(a, 'now', return_value=at):
            return self.store.close_looks_done()

    def test_a_hint_that_stood_a_day_closes_by_itself_once(self):
        self.hinted()
        self.assertEqual(self.close_at('2026-11-09T20:00:00+00:00'), [])  # still fresh: theirs to say Not done
        self.assertEqual(self.close_at('2026-11-10T10:30:00+00:00'), [self.sid])
        row = self.row()
        self.assertEqual(row['status'], 'completed')
        self.assertTrue(row['undo_until'])
        self.assertEqual(json.loads(row['handled_hint'])['reason'], 'Sam replied on Tuesday')  # Done shows it under the title
        with self.store.connect() as db:
            self.assertEqual(tuple(db.execute("SELECT source,feedback FROM decisions WHERE choice='complete'").fetchone()),
                             ('handled', 'Sam replied on Tuesday'))
            app = object.__new__(a.App)
            app.store = self.store
            lines = [i['text'] for i in app.card_chat_service(db, self.sid)[0] if i['kind'] == 'event']
        self.assertIn('Closed by itself: Sam replied on Tuesday', lines)
        self.assertEqual(self.close_at('2026-11-10T11:00:00+00:00'), [])  # once

    def test_undo_makes_it_a_normal_to_do_that_stays_open(self):
        self.hinted()
        self.close_at('2026-11-10T10:30:00+00:00')
        with patch_everywhere(a, 'now', return_value='2026-11-10T11:00:00+00:00'):
            self.store.decide(self.sid, 'undo', '', 'undo1', 'dashboard')
        row = self.row()
        self.assertEqual((row['status'], row.get('handled_hint')), ('pending', None))
        self.assertFalse(a.looks_done(row))
        self.assertEqual(self.close_at('2026-11-12T10:00:00+00:00'), [])
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 1)  # back on the list

    def test_not_done_within_the_day_keeps_it(self):
        self.hinted()
        with patch_everywhere(a, 'now', return_value='2026-11-09T12:00:00+00:00'):
            self.store.decide(self.sid, 'not_done', '', 'nd1', 'dashboard')
        self.assertEqual(self.close_at('2026-11-11T10:00:00+00:00'), [])
        self.assertEqual(self.row()['status'], 'pending')

    def test_a_run_found_done_closes_too_and_undo_brings_it_back_to_decide(self):
        with patch_everywhere(a, 'now', return_value='2026-11-09T10:00:00+00:00'):
            self.already_done()
        self.assertEqual(self.close_at('2026-11-10T10:30:00+00:00'), [self.sid])
        with self.store.connect() as db:
            feedback = db.execute("SELECT feedback FROM decisions WHERE choice='complete'").fetchone()[0]
        self.assertEqual(feedback, 'PR #3451 merged, deployed Oct 27.')  # what showed it: the run's first sentence
        with patch_everywhere(a, 'now', return_value='2026-11-10T11:00:00+00:00'):
            self.store.decide(self.sid, 'undo', '', 'undo1', 'dashboard')
        row = self.row()
        self.assertEqual((row['status'], row.get('outcome')), ('pending', None))
        self.assertEqual(self.close_at('2026-11-12T10:00:00+00:00'), [])

    def test_never_while_a_send_is_under_way(self):
        self.hinted()
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('j',?,'r1','{}','sending',?,?,'x','dashboard','')",(self.sid, '2026-11-09T11:00:00+00:00', '2026-11-09T11:00:00+00:00'))
        self.assertEqual(self.close_at('2026-11-10T10:30:00+00:00'), [])

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

    def waiting(self, due='2026-11-12'):
        """The owner answered with a question of their own: the review says the next step is the other person's."""
        self.store.commit_page('work', {}, [ux.event(source='two', body='Does the scope shrink too?')])
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='42'")
        with patch_everywhere(a, 'now', return_value='2026-11-09T10:00:00+00:00'):
            return self.store.suggest('asked', 'Renewal at fewer days', 'You asked Sam whether the scope shrinks too.', [2], due=due,
                                      card_id=self.sid, match=True, waiting_on='Sam to answer the scope question')

    def test_the_review_leaves_a_to_do_waiting_on_someone_with_its_deadline(self):
        saved = self.waiting()
        row = self.row()
        self.assertEqual((saved['id'], saved['status']), (self.sid, 'prepared'))
        self.assertTrue(a.waits_on_others(row))
        self.assertEqual((row['due'], row['title']), ('2026-11-12', 'Renewal at fewer days'))
        self.assertEqual(a.card(row).splitlines()[-1], 'Waiting on: Sam to answer the scope question.')
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 0)
            # nothing new for the owner: no notification, the message they have is edited
            self.assertEqual(tuple(db.execute('SELECT status,needs_edit FROM deliveries').fetchone()), ('sent', 1))
        # Their answer comes: an open to-do again, with the deadline
        self.store.commit_page('work', {}, [ux.event(source='three', body='Scope stays the same.')])
        self.store.suggest('answered', 'Answer Sam on the renewal', 'Sam says the scope stays.', [3], card_id=self.sid, match=True)
        row = self.row()
        self.assertEqual((row['status'], row.get('outcome'), row['due']), ('pending', None, '2026-11-12'))

    def test_a_waiting_to_do_comes_back_when_chasing_is_due(self):
        self.waiting()
        with patch_everywhere(a, 'now', return_value='2026-11-10T12:00:00+00:00'):
            self.store.wake_snoozed()
        self.assertTrue(a.waits_on_others(self.row()))
        with patch_everywhere(a, 'now', return_value='2026-11-11T12:00:00+00:00'):  # the morning before the deadline has come
            self.store.wake_snoozed()
        row = self.row()
        self.assertEqual((row['status'], row['due']), ('pending', '2026-11-12'))
        self.assertEqual(a.card(row).splitlines()[-1], 'Still waiting on: Sam to answer the scope question.')  # why it is back
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 1)
            self.assertEqual(tuple(db.execute('SELECT status,reminder FROM deliveries').fetchone()), ('queued', 1))
        # Their answer after all: the to-do is about that now
        self.store.commit_page('work', {}, [ux.event(source='three', body='Scope stays the same.')])
        self.store.suggest('answered', 'Answer Sam on the renewal', 'Sam says the scope stays.', [3], card_id=self.sid, match=True)
        self.assertEqual((self.row()['status'], self.row().get('outcome')), ('pending', None))

    def test_when_a_wait_comes_back(self):
        at = a.dt.datetime.fromisoformat('2026-11-09T10:00:00+00:00')  # Monday 11:00, after the morning digest
        back = lambda due, due_at=None: a.dt.datetime.fromisoformat(wait_until(due, current=at, due_at=due_at)).astimezone(
            a.local_tz()).strftime('%Y-%m-%d %H:%M')
        self.assertEqual(back(None), '2026-11-16 08:30')  # no deadline: a week
        self.assertEqual(back('2026-11-12'), '2026-11-11 08:30')  # the morning before the deadline
        self.assertEqual(back('2026-11-10'), '2026-11-10 08:30')  # that morning has passed: the deadline's own morning
        self.assertEqual(back('2026-11-09', '2026-11-09T15:00+00:00'), '2026-11-09 16:00')  # later today: at the deadline
        self.assertEqual(back('2026-11-10', '2026-11-10T07:00+00:00'), '2026-11-10 08:00')  # before tomorrow's morning: at it
        self.assertEqual(back('2026-11-09', '2026-11-09T08:00+00:00'), '2026-11-10 08:30')  # passed this morning: next morning
        self.assertEqual(back('2026-11-09'), '2026-11-10 08:30')  # today, no time: it passes tonight, next morning
        self.assertEqual(back('2026-11-02'), '2026-11-10 08:30')  # passed days ago: next morning
        early = a.dt.datetime.fromisoformat('2026-11-09T05:00:00+00:00')  # 06:00, before the morning digest
        self.assertEqual(wait_until('2026-11-02', current=early), '2026-11-09T07:30:00+00:00')  # this morning's slot

    def test_a_due_or_late_to_do_handed_on_waits_instead_of_being_a_to_do(self):
        # The owner's own to-do, snoozed and due today: they did their part and the review says the next step is someone
        # else's. It used to stay a to-do that only said to wait, which the owner had to snooze again.
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET origin='owner',status='snoozed',snoozed_until='2026-11-09T12:00:00+00:00',due='2026-11-09',"
                       "created_at='2026-10-01T09:00:00+00:00'")
        saved = self.waiting(due=None)
        row = self.row()
        self.assertEqual((saved['status'], row['status'], row['snoozed_until'], row['due']), ('prepared', 'prepared', None, '2026-11-09'))
        self.assertTrue(a.waits_on_others(row))
        self.assertEqual(a.card(row).splitlines()[-1], 'Waiting on: Sam to answer the scope question.')
        with self.store.connect() as db:
            self.assertEqual(a.waiting_count(db), 0)
        with patch_everywhere(a, 'now', return_value='2026-11-09T12:00:00+00:00'):  # its snooze time passes: it stays waiting
            self.store.wake_snoozed()
        self.assertTrue(a.waits_on_others(self.row()))
        with patch_everywhere(a, 'now', return_value='2026-11-10T08:00:00+00:00'):  # the deadline passed, no answer: back the
            self.store.wake_snoozed()                                              # next morning, to nudge them
        row = self.row()
        self.assertEqual(row['status'], 'pending')
        self.assertEqual(a.card(row).splitlines()[-1], 'Still waiting on: Sam to answer the scope question.')

    def test_a_wait_due_later_today_comes_back_at_the_deadline(self):
        with self.store.connect() as db:  # the owner's own to-do, due today at 16:00
            db.execute("UPDATE suggestions SET origin='owner',due='2026-11-09',due_at='2026-11-09T15:00+00:00',created_at='2026-10-01T09:00:00+00:00'")
        self.waiting(due=None)
        row = self.row()
        self.assertTrue(a.waits_on_others(row))
        self.assertEqual(json.loads(row['outcome'])['until'], '2026-11-09T15:00:00+00:00')
        with patch_everywhere(a, 'now', return_value='2026-11-09T15:05:00+00:00'):
            self.store.wake_snoozed()
        self.assertEqual(self.row()['status'], 'pending')

    def test_waiting_on_needs_an_open_to_do(self):
        self.store.commit_page('work', {}, [ux.event(source='two', body='Earlier'), ux.event(source='four', body='Another matter')])
        with self.assertRaisesRegex(ValueError, 'waiting_on is for an open to-do'):
            self.store.suggest('new', 'Something else', 'Nothing here yet.', [3], match=True, separate=True, waiting_on='Sam to answer')

    def test_evidence_line_is_the_first_sentence(self):
        self.assertEqual(a.first_sentence('**PR #3451** [merged](https://x.example/1), deployed Oct 27. Nothing left.'),
                         'PR #3451 merged, deployed Oct 27.')


if __name__ == '__main__':
    unittest.main()

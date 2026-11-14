"""Done when (outcomes.py): a to-do can carry the result that counts as done. After the owner's Send it waits for that
result under Waiting on others instead of closing, closes by itself (with Undo) when a signal shows it, and comes back
with a nudge one tap away when it stalls. The same line comes from a review, a run, someone's promise, a project's
condition, and holds for handoffs. Made-up data; fake transports; nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
import test_promises as tp
import test_ux as ux
from seams import patch_everywhere  # noqa: E402
a = ux.a
from machine.store import outcomes  # noqa: E402  (on the path once test_ux loaded the app)
from machine.store.cards import return_waiting  # noqa: E402

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
RESULT = 'Sam signed the order form'


def email(source_id, at, sender='sam@client.example', body='Can you send the order form?'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Order form',
            'body': body, 'deleted': False, 'metadata': {'from': sender, 'thread_id': 'a1', 'labels': ['INBOX']}}


class Outcomes(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [email('m1', '2026-10-15T08:00:00+00:00')])
        with self.store.connect() as db:
            self.event = db.execute('SELECT id FROM events').fetchone()[0]
        self.sid = self.store.suggest('order-form', 'Send Sam the order form', 'Sam asked for the order form.', [self.event])['id']

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL]}
        return app

    def suggestion(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def set(self, text, by):
        with self.store.connect() as db:
            return outcomes.set_done_when(db, self.sid, text, by)

    def send(self, done_when=RESULT, at='2026-10-16T09:00:00+00:00'):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'The order form is ready to send.', 'outcome': 'needs_you',
                                      'needs': 'approve the send', 'done_when': done_when,
                                      'next_action': {'kind': 'email', 'label': 'Send to Sam', 'account_id': 'work', 'to': ['sam@client.example'], 'thread_id': 'a1', 'in_reply_to': '<m1@client.example>', 'references': '<m1@client.example>',
                                                      'subject': 'Order form', 'body': 'Hi Sam,\n\nHere is the order form.\n\nOwner'}})
        self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': self.row()['next_action']['revision'],
                                             'approval_id': 'owner-approval'}, owner_dashboard=True)

        class T:
            def preflight(self, action): return None
            def send(self, action, job): return {'message_id': 'gm-1'}
            def reconcile(self, action, job): return {}
        with patch_everywhere(a, 'now', return_value=at):
            self.app().action_step(T())

    def test_the_run_owns_the_line_and_a_review_only_fills_it(self):
        self.assertTrue(self.set(RESULT, 'review'))
        self.assertEqual((self.suggestion()['done_when'], self.suggestion()['done_when_by']), (RESULT, 'review'))
        self.set('The order is in', 'run')
        self.set('Something else', 'review')  # a later review never overrides the run's
        self.assertEqual((self.suggestion()['done_when'], self.suggestion()['done_when_by']), ('The order is in', 'run'))
        with self.assertRaises(ValueError):
            outcomes.clean('x' * (outcomes.MAX + 1))
        self.assertEqual(outcomes.clean(' Sam  signed\nit '), 'Sam signed it')
        self.assertIn('add done_when to suggest', a.review_prompt('r1', []))  # the review knows the arg

    def test_a_review_revises_its_own_line_when_the_goal_changes_never_the_owners(self):
        from machine.app import status
        self.set(RESULT, 'review')
        # The review sees the open to-do's line in status, so it can tell when a newer message changes the goal
        self.assertEqual(status.compact_card(self.suggestion())['done_when'], RESULT)
        self.store.commit_page('work', {}, [email('m2', '2026-10-16T08:00:00+00:00', body='We will pay the deposit instead of signing.')])
        with self.store.connect() as db:
            newer = db.execute("SELECT id FROM events WHERE source_id='m2'").fetchone()[0]
        app = self.app()
        app.config = {**app.config, 'digest_at': '08:30'}

        def rewrite(done_when):
            return app.action('suggest', {'dedupe_key': 'order-form', 'card_id': self.sid, 'title': 'Get Sam\'s deposit',
                                          'body': 'Sam pays a deposit instead.', 'event_ids': [newer], 'done_when': done_when})
        rewrite('Sam paid the deposit')  # the review's update path (suggest with card_id) carries the new result
        self.assertEqual((self.suggestion()['done_when'], self.suggestion()['done_when_by']), ('Sam paid the deposit', 'review'))
        self.set('The order is in', 'run')  # what the owner said in its chat, through the run
        rewrite('Something else')
        self.assertEqual((self.suggestion()['done_when'], self.suggestion()['done_when_by']), ('The order is in', 'run'))
        prompt = a.review_prompt('r1', [])
        self.assertIn('the new done_when; one the owner set stays', prompt)
        self.assertIn('its title, body, draft and done_when following the new plan', prompt)

    def test_a_send_without_a_result_line_still_closes(self):
        self.send(done_when=None)
        self.assertEqual(self.suggestion()['status'], 'completed')

    def test_after_send_it_waits_closes_on_the_result_and_comes_back_when_stalled(self):
        self.send()
        row = self.suggestion()
        outcome = json.loads(row['outcome'])
        self.assertEqual((row['status'], outcome['state'], outcome['waiting_on']), ('prepared', 'waiting', RESULT))  # no name on a plain send: it waits on the result itself
        self.assertTrue(outcome['until'])
        self.assertTrue(outcomes.waits_for_result(row))
        with self.store.connect() as db:  # its chat says what it waits for
            self.assertIn('Waiting for the result: ' + RESULT, json.dumps(self.app().card_chat_service(db, self.sid), ensure_ascii=False))
        # Stalled: back as Still waiting, with a nudge one tap away in its chat
        with self.store.connect() as db, patch_everywhere(a, 'now', return_value='2026-12-01T09:00:00+00:00'):
            self.assertEqual(return_waiting(db), 1)
        row = self.suggestion()
        self.assertEqual((row['status'], json.loads(row['outcome'])['state']), ('pending', 'still_waiting'))
        self.assertIn('Write a short nudge', json.loads(row['chat_asks']))
        # Sam's signed form arrives; the review sees the result: closed by itself, Undo for a day
        self.store.commit_page('work', {}, [email('m2', '2026-12-02T08:00:00+00:00', body='Signed form attached.')])
        with self.store.connect() as db:
            signed = db.execute("SELECT id FROM events WHERE source_id='m2'").fetchone()[0]
        saved = self.store.looks_handled(self.sid, 'Sam sent the signed form', [signed])
        self.assertTrue(saved.get('closed'))
        row = self.suggestion()
        self.assertEqual(row['status'], 'completed')
        self.assertIsNone(row['handled_hint'])
        self.assertTrue(row['undo_until'])

    def test_a_signal_before_the_send_is_only_a_hint(self):
        self.set(RESULT, 'review')
        saved = self.store.looks_handled(self.sid, 'Sam signed already', [self.event])
        self.assertFalse(saved.get('closed'))
        row = self.suggestion()
        self.assertEqual(row['status'], 'pending')
        self.assertEqual(json.loads(row['handled_hint'])['reason'], 'Sam signed already')

    def test_the_review_sees_the_result_with_a_reply_to_the_sent_to_do(self):
        self.send()
        self.store.commit_page('work', {}, [email('m3', '2026-10-17T08:00:00+00:00', body='Will sign tomorrow')])
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute("SELECT * FROM events WHERE source_id='m3'")]
        with patch_everywhere(a, 'now', return_value='2026-10-17T09:00:00+00:00'):  # the day after the send, not the real clock
            replies = self.store.card_replies(rows)  # matched by thread: the review gets what result to look for
        self.assertEqual(replies[rows[0]['id']]['done_when'], RESULT)

    def test_a_teammates_accept_waits_for_the_result_and_their_done_closes_it(self):
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='snoozed' WHERE id=?", (self.sid,))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('fleet-handoff-wait-r1',?,'snooze','','fleet','2026-10-16T09:00:00+00:00')", (self.sid,))
        self.assertFalse(self.store.handoff_result_wait(self.sid, 'Robin', 'r1'))  # no result line: closes as before
        self.set(RESULT, 'review')
        self.assertFalse(self.store.handoff_result_wait(self.sid, 'Robin', 'other'))  # another handoff doesn't own it
        self.assertTrue(self.store.handoff_result_wait(self.sid, 'Robin', 'r1'))
        row = self.suggestion()
        self.assertEqual((row['status'], json.loads(row['outcome'])['waiting_on']), ('prepared', 'Robin'))
        self.assertTrue(self.store.handoff_result_wait(self.sid, 'Robin', 'r1'))  # an adjusted answer after: still one wait
        self.store.decide_handoff(self.sid, 'complete', '', 'fleet-handoff-done-r1', 'r1')
        self.assertEqual(self.suggestion()['status'], 'completed')

    def test_a_project_proof_closes_its_waiting_to_do(self):
        self.send()
        with self.store.connect() as db:
            outcomes.project_proof(db, self.sid, 'Listing is live', self.event, '2026-10-18T09:00:00+00:00')
        self.assertEqual(self.suggestion()['status'], 'completed')

    def test_a_changed_goal_moves_the_waiting_line_that_was_the_old_goal_only(self):
        with self.store.connect() as db:  # a project's blocker to-do, waiting on the project's result
            outcomes.set_done_when(db, self.sid, 'Listing is live', 'project')
            outcomes.wait_for_result(db, db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone(), '', '2026-10-16T09:00:00+00:00')
            self.assertTrue(outcomes.follow_project(db, self.sid, 'Listing is live', 'Listing links to us'))
        self.assertEqual(json.loads(self.suggestion()['outcome'])['waiting_on'], 'Listing links to us')
        with self.store.connect() as db:  # back as Still waiting: the line still follows the goal
            db.execute("UPDATE suggestions SET status='pending',outcome=? WHERE id=?",
                       (json.dumps({'state': 'still_waiting', 'waiting_on': 'Listing links to us'}), self.sid))
            outcomes.set_done_when(db, self.sid, 'Listing links to us with a follow link', 'project')
        self.assertEqual(json.loads(self.suggestion()['outcome'])['waiting_on'], 'Listing links to us with a follow link')
        with self.store.connect() as db:  # a line someone wrote stays
            db.execute('UPDATE suggestions SET outcome=? WHERE id=?',
                       (json.dumps({'state': 'waiting', 'waiting_on': 'Sam to check with their editor', 'until': '2026-10-20'}), self.sid))
            outcomes.follow_project(db, self.sid, 'Listing links to us with a follow link', 'Listing is back online')
        self.assertEqual(json.loads(self.suggestion()['outcome'])['waiting_on'], 'Sam to check with their editor')
        self.assertEqual(self.suggestion()['done_when'], 'Listing is back online')


class TheirPromise(unittest.TestCase):
    setUp = tp.Promises.setUp
    at = tp.Promises.at
    app = tp.Promises.app
    record = tp.Promises.record
    row = tp.Promises.row

    def test_what_they_promised_is_the_to_dos_result(self):
        pid = self.record(due='2026-10-19')['id']
        self.at('2026-10-21T09:00:00+00:00')
        saved = self.app().promise_card({**self.row(pid), 'made_at': '2026-10-19T08:00:00+00:00'})
        with self.store.connect() as db:
            row = db.execute('SELECT done_when,done_when_by FROM suggestions WHERE id=?', (saved['id'],)).fetchone()
        self.assertEqual(row['done_when_by'], 'promise')
        self.assertIn('send the signed contract', row['done_when'])


if __name__ == '__main__':
    unittest.main()

"""A sent reply that only promises the owner's real work ("I'll send the PDFs by Tuesday") never closes its to-do: the
run marks the draft with still_owed (judged by meaning when it writes it), and after the send the to-do stays open for
that work, due the promised day, with the promise kept and linked to it. A reply that does the work still closes the
to-do. The send review's mailbox line holds either way. Made-up data; fake transports; nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
import test_ux as ux
from seams import patch_everywhere  # noqa: E402
import machine.app.preparation as machine_app_preparation  # noqa: E402  (on the path once test_ux loaded the app)
import machine.main as machine_main
import next_actions
import timeutil

GMAIL = {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog', 'boundary': 'work:Example'}
OWED = {'what': 'send Ash the Q4 statements and invoice PDFs', 'due': '2026-10-20'}


def email(source_id, at, body='Could you send the Q4 statements and the two invoice PDFs?'):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'occurred_at': at, 'title': 'Q4 statements',
            'body': body, 'deleted': False, 'metadata': {'from': 'Ash Moore <ash@ledger.example>', 'thread_id': 'a1', 'labels': ['INBOX']}}


class StillOwed(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = machine_main.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [email('m1', '2026-10-15T08:00:00+00:00')])
        with self.store.connect() as db:
            self.event = db.execute('SELECT id FROM events').fetchone()[0]
        self.sid = self.store.suggest('q4-statements', 'Send Ash the Q4 statements', 'Ash asked for the Q4 statements.', [self.event])['id']

    def app(self):
        app = object.__new__(machine_main.App)
        app.store = self.store
        app.config = {'accounts': [GMAIL]}
        return app

    def suggestion(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def draft(self, **extra):
        return {'kind': 'email', 'label': 'Send reply', 'account_id': 'work', 'to': ['ash@ledger.example'],
                'thread_id': 'a1', 'in_reply_to': '<m1@ledger.example>', 'references': '<m1@ledger.example>',
                'subject': 'Re: Q4 statements', 'body': 'Hi Ash,\n\nI’ll gather them and send them by Tuesday.\n\nOwner', **extra}

    def send(self, draft):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Drafted a reply. Nothing has been sent.', 'outcome': 'needs_you',
                                      'needs': 'approve the send', 'next_action': draft})
        self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': self.row()['next_action']['revision'],
                                             'approval_id': 'owner-approval'}, owner_dashboard=True)

        class T:
            def preflight(self, action): return None
            def send(self, action, job): return {'message_id': 'gm-1'}
            def reconcile(self, action, job): return {}
        with patch_everywhere(timeutil, 'now', return_value='2026-10-16T09:00:00+00:00'):
            self.app().action_step(T())

    def test_a_reply_that_only_promises_the_work_keeps_the_to_do_open_with_its_promise(self):
        self.send(self.draft(still_owed=OWED))
        row = self.suggestion()
        self.assertEqual((row['status'], row['due'], row['next_action'], row['outcome']), ('pending', '2026-10-20', None, None))
        self.assertRegex(row['body'], r'^Replied to Ash Moore on .+\. The work is still to do\.$')  # not the draft's line
        self.assertNotIn('Nothing has been sent', row['body'])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT status FROM action_jobs").fetchone()[0], 'sent')
            self.assertIsNone(db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND choice='complete'", (self.sid,)).fetchone())
            chat = json.dumps(self.app().card_chat_service(db, self.sid), ensure_ascii=False)
        self.assertIn('Kept open for the work the reply promised', chat)
        # The promise is kept with the to-do: listed as "a to-do now", so a review that reads the sent reply finds it
        promise = [p for p in self.store.promises() if p['suggestion_id'] == self.sid]
        self.assertEqual([(p['direction'], p['who'], p['what'], p['due'], p['state']) for p in promise],
                         [('mine', 'Ash Moore', OWED['what'], '2026-10-20', 'card')])
        self.assertIn('a to-do now', self.store.promises_text())
        # Done once the work is done: the promise reads kept
        self.decide('complete', 'done-later')
        with patch_everywhere(timeutil, 'now', return_value='2026-10-21T09:00:00+00:00'):
            self.assertEqual([p['state'] for p in self.store.promises() if p['suggestion_id'] == self.sid], ['kept'])

    def test_a_reply_that_does_the_work_still_closes_the_to_do(self):
        self.send(self.draft(body='Hi Ash,\n\nHere are the statements and both invoices.\n\nOwner'))
        self.assertEqual(self.suggestion()['status'], 'completed')
        self.assertEqual([p for p in self.store.promises() if p['suggestion_id'] == self.sid], [])

    def test_no_date_promised_keeps_the_to_dos_own(self):
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET due='2026-10-30' WHERE id=?", (self.sid,))
        self.send(self.draft(still_owed={'what': OWED['what']}))
        row = self.suggestion()
        self.assertEqual((row['status'], row['due']), ('pending', '2026-10-30'))

    def test_a_promise_to_do_gets_the_new_date_not_a_second_promise(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,suggestion_id,created_at,updated_at) "
                       "VALUES('mine','Ash Moore',?,'2026-10-16','2026-10-15T06:30:00+00:00',?,'work','carded',?,'2026-10-15T08:00:00+00:00','2026-10-15T08:00:00+00:00')",
                       (OWED['what'], self.event, self.sid))
        self.send(self.draft(still_owed=OWED))
        with self.store.connect() as db:
            rows = [tuple(r) for r in db.execute('SELECT status,due FROM promises WHERE suggestion_id=?', (self.sid,))]
        self.assertEqual(rows, [('carded', '2026-10-20')])
        self.assertEqual(self.suggestion()['status'], 'pending')

    def test_the_draft_carries_it_checked_and_the_send_review_says_so(self):
        config = self.app().config
        plain, owed = (next_actions.validate(self.draft(**extra), config, ['work']) for extra in ({}, {'still_owed': {'what': '  send Ash   the statements ', 'due': '2026-10-20'}}))
        self.assertNotIn('still_owed', plain)
        self.assertEqual(owed['still_owed'], {'what': 'send Ash the statements', 'due': '2026-10-20'})
        self.assertNotEqual(plain['revision'], owed['revision'])  # bound to the draft the owner sees
        # The mailbox line holds for both; only the promising one adds that the to-do stays open
        self.assertIn('Leaves your inbox for 3 days after sending, or until a reply.', next_actions.email_preview(plain))
        self.assertNotIn(next_actions.OWED_NOTE, next_actions.email_preview(plain))
        self.assertIn('Leaves your inbox for 3 days after sending, or until a reply.\n' + next_actions.OWED_NOTE, next_actions.email_preview(owed))
        # The owner's own edit keeps it
        self.assertEqual(next_actions.revise(owed, body='Hi Ash,\n\nBy Tuesday.\n\nOwner')['still_owed'], owed['still_owed'])
        for bad in ({'what': 'x'}, {'what': 'send it', 'due': 'Tuesday'}, {'what': 'send it', 'when': '2026-10-20'}, 'send it'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                next_actions.validate(self.draft(still_owed=bad), config, ['work'])
        with self.assertRaises(ValueError):  # a handoff waits on them, not on the owner's own work
            next_actions.validate(self.draft(delegate=True, still_owed={'what': 'send it'}), config, ['work'])

    def test_the_run_is_told_to_judge_it_by_meaning(self):
        self.decide('accept')
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM preparations').fetchone())
        prompt = machine_app_preparation.preparation_prompt(job)
        self.assertIn('still_owed:{what:', prompt)
        self.assertIn('judged by what it means, not its words', prompt)


if __name__ == '__main__':
    unittest.main()

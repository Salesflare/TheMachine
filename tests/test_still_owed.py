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

    def send(self, draft, edit=None):
        """Prepares the draft (a list: several messages on the one to-do), optionally lets the owner edit the text of
        the first (edit), and sends every one, in the order given."""
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Drafted a reply. Nothing has been sent.', 'outcome': 'needs_you',
                                      'needs': 'approve the send', **({'next_actions': draft} if isinstance(draft, list) else {'next_action': draft})})
        revisions = [a['revision'] for a in next_actions.visible_actions(self.suggestion()['next_action'])]
        if edit is not None:
            saved = self.store.revise_draft(self.sid, revisions[0], 'dashboard', body=edit)
            self.assertEqual(saved['status'], 'revised')
            revisions[0] = saved['revision']

        class T:
            def preflight(self, action): return None
            def send(self, action, job): return {'message_id': 'gm-' + job['id']}
            def reconcile(self, action, job): return {}
        for n, revision in enumerate(revisions):
            self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': revision,
                                                 'approval_id': 'owner-approval' + ('-%d' % n if n else '')}, owner_dashboard=True)
            with patch_everywhere(timeutil, 'now', return_value='2026-10-16T09:0%d:00+00:00' % n):
                self.app().action_step(T())

    def mine(self):
        return [(p['what'], p['due'], p['state']) for p in self.store.promises() if p['suggestion_id'] == self.sid]

    def test_a_reply_that_only_promises_the_work_keeps_the_to_do_open_with_its_promise(self):
        with self.store.connect() as db:  # what its draft followed (based_on): said about the draft, so it goes with it
            db.execute('UPDATE suggestions SET based_on=(SELECT max(id) FROM events)')
        self.send(self.draft(still_owed=OWED))
        row = self.suggestion()
        self.assertEqual((row['status'], row['due'], row['next_action'], row['outcome']), ('pending', '2026-10-20', None, None))
        self.assertIsNone(row['based_on'])
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

    def test_a_deadline_time_goes_with_its_day(self):
        with self.store.connect() as db:  # "today 15:00", as the owner gave it: the promised day has no time
            db.execute("UPDATE suggestions SET due='2026-10-16',due_at='2026-10-16T13:00:00+00:00'")
        self.send(self.draft(still_owed=OWED))
        self.assertEqual((self.suggestion()['due'], self.suggestion()['due_at']), ('2026-10-20', None))

    def test_what_is_still_owed_and_waited_on_names_the_day(self):
        with patch_everywhere(timeutil, 'now', return_value='2026-10-16T09:00:00+00:00'):  # a Friday
            kept = next_actions.validate(self.draft(still_owed={'what': 'send the PDFs by tomorrow'}), {'accounts': [GMAIL]}, ['work'])
            self.assertEqual(kept['still_owed']['what'], 'send the PDFs by Sat, Oct 17')
            self.decide('accept')
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Looked into it.', 'outcome': 'needs_you', 'needs': 'the two PDFs before tomorrow'})
            self.assertEqual(json.loads(self.suggestion()['outcome'])['needs'], 'the two PDFs before Sat, Oct 17')
            self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Asked Ash.', 'outcome': 'waiting', 'waiting_on': 'Ash to confirm today'})
            self.assertEqual(json.loads(self.suggestion()['outcome'])['waiting_on'], 'Ash to confirm Fri, Oct 16')

    def test_the_send_is_on_record_for_a_run_that_is_asked_whether_it_went(self):
        """status with suggestion_id had only the tap, never the send itself: asked "did it go out?", a run could only
        search the mailbox and called its own send unconfirmed (agent users, 2026-11-24)."""
        self.assertNotIn('sends', self.app().action('status', {'suggestion_id': self.sid}))
        self.send(self.draft(still_owed=OWED))
        found = self.app().action('status', {'suggestion_id': self.sid})
        [send] = found['sends']
        approved_at = send.pop('approved_at')
        with self.store.connect() as db:
            self.assertEqual(approved_at, db.execute('SELECT created_at FROM action_jobs').fetchone()[0])
        self.assertEqual(send, {'kind': 'email', 'to': ['ash@ledger.example'], 'subject': 'Re: Q4 statements', 'status': 'sent',
                                'approved': 'the owner tapped Send in the dashboard', 'sent_at': '2026-10-16T09:00:00+00:00',
                                'text': 'Hi Ash,\n\nI’ll gather them and send them by Tuesday.\n\nOwner'})
        self.assertIn('settles whether one went out', found['sends_note'])
        # The chat's line is at the moment it went (not when it was approved), right above why the to-do stays open
        with self.store.connect() as db:
            events = [(i['text'], i['at']) for i in sorted(self.app().card_chat_service(db, self.sid)[0], key=lambda i: i['at']) if i['kind'] == 'event']
        sent = [text for text, _ in events].index('Sent to Ash')
        self.assertEqual(events[sent][1], int(timeutil.dt.datetime.fromisoformat('2026-10-16T09:00:00+00:00').timestamp() * 1000))
        self.assertEqual(events[sent + 1][0], 'Kept open for the work the reply promised')

    def test_a_send_that_failed_is_on_record_as_not_sent(self):
        self.send(self.draft(still_owed=OWED))
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET status='failed',error='The mail server refused it.'")
        [send] = self.app().action('status', {'suggestion_id': self.sid})['sends']
        self.assertEqual((send['status'], send['error'], 'sent_at' in send), ('failed', 'The mail server refused it.', False))

    def test_the_chat_is_told_the_outbox_settles_it_and_not_to_say_what_a_tap_turns_false(self):
        self.decide('accept')
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM preparations').fetchone())
        prompt = machine_app_preparation.chat_prompt(job)
        self.assertIn("answered from status's sends", prompt)
        self.assertIn('stops being true when they tap Send', prompt)

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
        # It goes with the words it was judged on: an edit of the spacing keeps it, other words leave it unknown
        self.assertEqual(next_actions.revise(owed, body=owed['body'].replace('send them', 'send  them'))['still_owed'], owed['still_owed'])
        edited = next_actions.revise(owed, body='Hi Ash,\n\nBy Tuesday.\n\nOwner')
        self.assertEqual(('still_owed' in edited, edited.get('owed_unsure')), (False, True))
        self.assertNotIn(next_actions.OWED_NOTE, next_actions.email_preview(edited))
        self.assertEqual(next_actions.revise(owed, subject='Re: Q4 statements (corrected)').get('owed_unsure'), True)
        self.assertNotIn('owed_unsure', next_actions.revise(plain, body='Hi Ash,\n\nBy Tuesday.\n\nOwner'))
        for bad in ({'what': 'x'}, {'what': 'send it', 'due': 'Tuesday'}, {'what': 'send it', 'when': '2026-10-20'}, 'send it'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                next_actions.validate(self.draft(still_owed=bad), config, ['work'])
        with self.assertRaises(ValueError):  # a handoff waits on them, not on the owner's own work
            next_actions.validate(self.draft(delegate=True, still_owed={'what': 'send it'}), config, ['work'])

    # The owner's edit: still_owed was judged on the drafted words, so it goes only with those words

    def test_an_edit_that_does_the_work_keeps_no_promise_it_no_longer_makes(self):
        self.send(self.draft(still_owed=OWED), edit='Hi Ash,\n\nHere are the statements and both invoices.\n\nOwner')
        row = self.suggestion()
        self.assertEqual(self.mine(), [])  # not "send the statements by Oct 20": the sent reply never said it
        self.assertEqual((row['status'], row['due'], row['next_action']), ('pending', None, None))  # open until it shows done
        self.assertRegex(row['body'], r'^Replied to Ash Moore on .+\. Kept open in case the work is still to do\.$')
        with self.store.connect() as db:
            chat = json.dumps(self.app().card_chat_service(db, self.sid), ensure_ascii=False)
            [sent] = [dict(r) for r in db.execute('SELECT status,payload FROM action_jobs')]
        self.assertIn('Kept open in case the edited reply left work to do', chat)
        self.assertNotIn('Kept open for the work the reply promised', chat)
        # Exactly the approved words went out, and nothing claims what they promise
        self.assertEqual(sent['status'], 'sent')
        self.assertEqual(json.loads(sent['payload'])['body'], 'Hi Ash,\n\nHere are the statements and both invoices.\n\nOwner')
        self.assertNotIn('still_owed', json.loads(sent['payload']))

    def test_the_sent_reply_settles_an_edited_one_once_it_comes_in(self):
        """What keeps it open until then: the check that reads later messages (handled_check) reads the owner's own sent
        reply, its words and files, and closes it when it did the work."""
        self.send(self.draft(still_owed=OWED), edit='Hi Ash,\n\nHere are the statements and both invoices.\n\nOwner')
        with self.store.connect() as db:  # everything at the made-up moment, as the clock below says
            db.execute("UPDATE decisions SET created_at='2026-10-16T08:30:00+00:00'")
            db.execute("UPDATE suggestions SET created_at='2026-10-15T08:00:00+00:00'")
        self.store.commit_page('work', {}, [{**email('sent-1', '2026-10-16T09:00:05+00:00', 'Hi Ash, here are the statements and both invoices. Owner'),
                                             'metadata': {'from': 'Owner <owner@example.com>', 'to': 'Ash Moore <ash@ledger.example>', 'thread_id': 'a1',
                                                          'labels': ['SENT'], 'attachments': [{'filename': 'Q4-statements.pdf'}]}}])
        with self.store.connect() as db:
            sent = db.execute("SELECT id FROM events WHERE source_id='sent-1'").fetchone()[0]
        app, asked = self.app(), []
        app.config = {'accounts': [GMAIL], 'openclaw_config': str(Path(self.tmp.name) / 'no-openclaw.json')}
        app.handled_check_model = lambda config, text: (asked.append(text), json.dumps([{'todo': self.sid, 'state': 'done', 'event_id': sent, 'reason': 'Sent the statements'}]))[1]
        with patch_everywhere(timeutil, 'now', return_value='2026-10-16T10:00:00+00:00'):
            self.assertEqual(app.handled_step(), 1)
        self.assertIn('here are the statements and both invoices', asked[0])
        self.assertEqual(self.suggestion()['status'], 'completed')

    def test_an_edit_that_moves_the_day_never_keeps_the_old_day(self):
        self.send(self.draft(still_owed=OWED), edit='Hi Ash,\n\nI’ll send them by Friday instead.\n\nOwner')
        row = self.suggestion()
        self.assertEqual((row['status'], row['due']), ('pending', None))  # not the drafted Oct 20
        self.assertEqual(self.mine(), [])  # the review of the sent reply records what it says (below)

    def test_the_same_words_keep_the_promise(self):
        self.send(self.draft(still_owed=OWED), edit='Hi Ash,\n\nI’ll gather them and  send them by Tuesday. \n\nOwner')
        self.assertEqual((self.suggestion()['status'], self.suggestion()['due']), ('pending', '2026-10-20'))
        self.assertEqual(self.mine(), [(OWED['what'], '2026-10-20', 'card')])

    def sent_reply(self, at, body):
        """The owner's sent reply as the mailbox brings it in later, and the review's promise from it."""
        self.store.commit_page('work', {}, [{**email('sent-1', at, body), 'metadata': {
            'from': 'Owner <owner@example.com>', 'to': 'ash@ledger.example', 'thread_id': 'a1', 'labels': ['SENT']}}])
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='sent-1'").fetchone()[0]
        with patch_everywhere(timeutil, 'now', return_value='2026-10-16T10:00:00+00:00'):
            return self.store.promise({'direction': 'mine', 'who': 'Ash Moore', 'what': 'send Ash the Q4 statements', 'due': '2026-10-23', 'event_id': event})

    def due_promise(self, promise_id):
        app = self.app()
        app.config = {'accounts': [GMAIL], 'prepare_ahead': False}
        with self.store.connect() as db:
            p = dict(db.execute('SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE p.id=?', (promise_id,)).fetchone())
        with patch_everywhere(timeutil, 'now', return_value='2026-10-23T09:00:00+00:00'):
            return app.promise_card(p)

    def test_an_edit_that_adds_a_promise_brings_the_to_do_back_when_it_is_due(self):
        self.send(self.draft(), edit='Hi Ash,\n\nI’ll send them on Friday.\n\nOwner')
        self.assertEqual(self.suggestion()['status'], 'completed')  # no judgment of the edited words: the send closes it
        # The review reads the sent reply and finds the promise in it; the send's own close never swallows it
        recorded = self.sent_reply('2026-10-16T08:59:59+00:00', 'Hi Ash, I’ll send them on Friday. Owner')
        self.assertEqual(recorded['status'], 'open')
        self.due_promise(recorded['id'])
        row = self.suggestion()
        self.assertEqual((row['status'] in ('pending', 'prepared', 'accepted'), row['due']), (True, '2026-10-23'))

    def test_an_edit_that_moves_the_day_gets_the_reviewed_promise_as_soon_as_the_reply_is_read(self):
        for edit in ('Hi Ash,\n\nI’ll send them by Friday instead.\n\nOwner',  # another day
                     'Hi Ash,\n\nI’ll gather them and send them by Tuesday!\n\nOwner'):  # the same promise, other words
            with self.subTest(edit=edit):
                self.setUp()
                self.send(self.draft(still_owed=OWED), edit=edit)
                self.assertEqual((self.suggestion()['due'], self.mine()), (None, []))
                recorded = self.sent_reply('2026-10-16T08:59:59+00:00', edit.replace('\n', ' '))
                self.assertEqual((recorded['status'], recorded['suggestion_id']), ('carded', self.sid))  # one to-do, never a second
                self.assertEqual((self.suggestion()['status'], self.suggestion()['due']), ('pending', '2026-10-23'))
                self.assertEqual(self.mine(), [('send Ash the Q4 statements', '2026-10-23', 'card')])
                self.assertIsNone(self.due_promise(recorded['id']))  # nothing comes due apart from it
                # The review reading the same reply again finds it, no second one
                self.assertTrue(self.sent_reply('2026-10-16T08:59:59+00:00', edit.replace('\n', ' '))['duplicate'])

    def test_a_later_message_in_the_thread_is_not_the_edited_reply_unless_the_to_do_was_kept_for_it(self):
        self.send(self.draft(still_owed=OWED))  # judged on these words: its promise, no unsure keep
        recorded = self.sent_reply('2026-10-16T08:59:59+00:00', 'Hi Ash, I’ll send them on Friday. Owner')
        self.assertEqual(recorded['status'], 'open')

    def test_the_owners_own_close_still_keeps_a_promise_with_its_to_do(self):
        self.send(self.draft(), edit='Hi Ash,\n\nI’ll send them on Friday.\n\nOwner')
        recorded = self.sent_reply('2026-10-16T08:59:59+00:00', 'Hi Ash, I’ll send them on Friday. Owner')
        with patch_everywhere(timeutil, 'now', return_value='2026-10-17T09:00:00+00:00'):
            self.decide('reopen', 'reopen-1')
            self.decide('complete', 'done-1')
        self.assertTrue(self.due_promise(recorded['id'])['duplicate'])
        self.assertEqual(self.suggestion()['status'], 'completed')

    def test_several_messages_on_one_to_do_keep_each_promise(self):
        other = {'what': 'call Bo about the audit', 'due': '2026-10-19'}
        to_bo = {'to': ['bo@ledger.example'], 'thread_id': None, 'in_reply_to': None, 'references': None, 'subject': 'Audit'}
        for order in ((OWED, None), (None, OWED), (OWED, other)):
            with self.subTest(order=order):
                self.setUp()
                first, second = order
                self.send([self.draft(**({'still_owed': first} if first else {})),
                           self.draft(**to_bo, label='Send Bo', body='Hi Bo,\n\nI’ll call you.\n\nOwner' if second else 'Hi Bo,\n\nAll done.\n\nOwner',
                                      **({'still_owed': second} if second else {}))])
                row = self.suggestion()
                owed = [o for o in order if o]
                self.assertEqual((row['status'], row['due']), ('pending', min(o['due'] for o in owed)))
                self.assertEqual(sorted(w for w, _, _ in self.mine()), sorted(o['what'] for o in owed))

    def test_a_repeated_settle_or_tap_adds_no_second_promise(self):
        self.send(self.draft(still_owed=OWED))
        from machine.store import decisions
        with self.store.connect() as db:
            job = db.execute('SELECT id FROM action_jobs').fetchone()[0]
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (self.sid,))
            decisions.settle_sent(self.store, db, self.sid, job)
        self.assertEqual(self.mine(), [(OWED['what'], '2026-10-20', 'card')])

    def test_the_run_is_told_to_judge_it_by_meaning(self):
        self.decide('accept')
        with self.store.connect() as db:
            job = dict(db.execute('SELECT * FROM preparations').fetchone())
        prompt = machine_app_preparation.preparation_prompt(job)
        self.assertIn('still_owed:{what:', prompt)
        self.assertIn('judged by what it means, not its words', prompt)


if __name__ == '__main__':
    unittest.main()

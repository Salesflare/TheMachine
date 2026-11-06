"""A step the owner asks for in the card chat runs on their word (do_now): their message is the OK, so the card never
asks them to confirm what they asked for (2026-11-06: "why am I confirming something I asked"). Sends still wait for
their Send on a draft they saw, and a step they didn't ask for still waits for their Confirm. Synthetic data only."""
import unittest
import test_chat_send as cs

a = cs.a

CLEANUP = {'kind': 'finish', 'label': 'Confirm document cleanup', 'url': 'https://docs.example.invalid/d/42/edit',
           'instructions': 'In doc 42 remove the two raw anchor tags from the headings and add paragraph spacing.',
           'preview': 'Formatting only in the existing doc: remove two raw anchors, add paragraph spacing.'}

PLACEMENT = {'kind': 'finish', 'label': 'Confirm placement update', 'url': 'https://docs.example.invalid/d/42/edit',
             'instructions': 'In doc 42 move the new entry from #11 to #2 in the placement line, the table row and its heading.',
             'preview': 'Move the new entry from #11 to #2. Other wording, formatting and permissions stay. Nothing sent or published.'}


class ChatDoNow(unittest.TestCase):
    setUp = cs.ChatSend.setUp
    row = cs.ChatSend.row
    app = cs.ChatSend.app
    draft = cs.ChatSend.draft
    say = cs.ChatSend.say

    def save(self, job, steps, **extra):
        return self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'Cleaning up the doc now.',
                                             'next_actions': steps, 'outcome': 'needs_you', 'needs': 'check the doc',
                                             'note_kind': 'new_ask', **extra})

    def jobs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT revision,status,source FROM action_jobs')]

    def test_a_step_the_owner_asked_for_runs_without_a_confirm(self):
        job = self.say('there are some weird a tags on headers in the doc, fix it', 'chat-fix')
        # The model is asked first, with the owner's message and the step side by side
        with self.assertRaisesRegex(ValueError, 'Decide first.*weird a tags.*Confirm document cleanup'):
            self.save(job, [CLEANUP])
        self.assertEqual(self.jobs(), [])
        saved = self.save(job, [CLEANUP, self.draft()], do_now=True)
        self.assertEqual(saved['done_now'], {'status': 'queued'})
        [run] = self.jobs()
        self.assertEqual((run['status'], run['source']), ('local_preparation', 'assistant'))
        step = a.next_actions.actions(self.store_next())[0]
        self.assertEqual(run['revision'], step['revision'])
        with self.store.connect() as db:  # the step's own run starts now, the email draft still waits for Send
            self.assertEqual(db.execute('SELECT status FROM preparations').fetchone()[0], 'queued')
            self.assertEqual(db.execute("SELECT status FROM suggestions").fetchone()[0], 'accepted')
        self.assertNotIn('send', saved)

    def test_a_second_asked_edit_on_the_same_to_do_runs_too(self):
        # The same to-do, a later message: "we can place them in the same spot they put us, like #2"
        job = self.say('there are some weird a tags on headers in the doc', 'chat-fix')
        self.save(job, [CLEANUP, self.draft()], do_now=True)
        with self.store.connect() as db:  # the cleanup ran and saved its result; the email still waits
            db.execute("UPDATE action_jobs SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared'")
            db.execute("UPDATE preparations SET status='done'")
        job = self.say('also we can place them in the same spot they put us, like #2', 'chat-place')
        with self.assertRaisesRegex(ValueError, 'Decide first.*like #2.*Confirm placement update'):
            self.save(job, [PLACEMENT, self.draft()])
        self.assertEqual(self.save(job, [PLACEMENT, self.draft()], do_now=True)['done_now'], {'status': 'queued'})
        self.assertEqual(sorted(j['status'] for j in self.jobs()), ['done', 'local_preparation'])

    def store_next(self):
        with self.store.connect() as db:
            return db.execute('SELECT next_action FROM suggestions').fetchone()[0]

    def test_a_step_beyond_what_they_asked_waits_for_their_confirm(self):
        job = self.say('why is it a block of text?', 'chat-question')
        with self.assertRaisesRegex(ValueError, 'Decide first'):
            self.save(job, [CLEANUP])
        self.save(job, [CLEANUP], do_now=False)
        self.assertEqual(self.jobs(), [])
        self.assertIn('Confirm document cleanup', [b['label'] for b in a.controls(self.row())['blocks'][0]['buttons']])
        # The same step carried over in a later turn is not asked about again
        job = self.say('when did they last write?', 'chat-later')
        self.save(job, [CLEANUP])
        self.assertEqual(self.jobs(), [])

    def test_a_send_never_runs_on_do_now(self):
        job = self.say('Email Pat at acme.example', 'chat-email')
        with self.assertRaisesRegex(ValueError, 'do_now is for a doc edit'):
            self.save(job, [self.draft()], do_now=True)
        post = {**CLEANUP, 'label': 'Submit inbox reply', 'message': 'Hi Pat', 'to_name': 'Pat'}
        with self.assertRaisesRegex(ValueError, 'do_now is for a doc edit'):
            self.save(job, [post], do_now=True)
        self.save(job, [self.draft()])  # an email draft is shown for Send, never asked about
        self.assertEqual(self.jobs(), [])

    def test_do_now_needs_the_owners_own_message(self):
        self.store.decide(self.sid, 'accept', '', 'tap', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            job = db.execute('SELECT job_id FROM preparations').fetchone()[0]
        with self.assertRaisesRegex(ValueError, 'do_now needs the owner'):
            self.save(job, [CLEANUP], do_now=True)
        self.save(job, [CLEANUP])  # a bare Do it: the step waits for Confirm, no question
        self.assertEqual(self.jobs(), [])

    def test_which_steps_can_run_on_the_owners_word(self):
        self.assertTrue(a.doable_now({'kind': 'doc_write', 'op': 'edit'}))
        self.assertFalse(a.doable_now({'kind': 'doc_write', 'op': 'create'}))  # made by itself already
        self.assertTrue(a.doable_now(CLEANUP))
        for step in ({**CLEANUP, 'message': 'Hi'}, {**CLEANUP, 'attachments': [{'name': 'x.pdf'}]},
                     {**CLEANUP, 'label': 'Share the doc'}, {**CLEANUP, 'label': 'Send invoice'},
                     {'kind': 'email'}, {'kind': 'slack'}, {'kind': 'calendar'}):
            self.assertFalse(a.doable_now(step), step)


if __name__ == '__main__':
    unittest.main()

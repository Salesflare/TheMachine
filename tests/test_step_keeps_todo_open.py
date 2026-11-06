"""Carrying out one step of a to-do never closes it while another step still waits for the owner (2026-11-06: a confirmed
doc cleanup went through, its run saved only an Open doc link, and the to-do closed with the reply email unsent: "we
haven't emailed him yet... and you're closing it?"). The run's result keeps the other steps; the to-do is done when all
of them are, or when the owner marks it done. Synthetic data only."""
import unittest

import test_chat_do_now as dn
import test_next_actions as tn
import test_ux as ux

a = ux.a
CLEANUP, PLACEMENT = dn.CLEANUP, dn.PLACEMENT
OPEN = {'kind': 'open', 'label': 'Open Google Doc', 'url': 'https://docs.example.invalid/d/42/edit'}


class StepKeepsTodoOpen(unittest.TestCase):
    setUp = ux.UX.setUp
    row = ux.UX.row
    draft = tn.NextActions.draft
    say = dn.ChatDoNow.say

    def app(self):
        if not hasattr(self, '_app'):
            self._app = tn.NextActions.app(self)
        return self._app

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM preparations').fetchone())

    def steps(self):
        return {a.next_actions.label(s): s for s in self.row()['next_actions']}

    def ready(self, steps):
        """The to-do as Jeroen had it: a doc cleanup to confirm and the reply email to send."""
        self.store.decide(self.sid, 'accept', '', 'tap', 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
        self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': self.job()['job_id'], 'body': 'The cleanup and the reply are ready.',
                                      'next_actions': steps, 'outcome': 'needs_you', 'needs': 'confirm the cleanup, then send the email'})
        return self.steps()

    def confirm(self, step):
        """The owner's Confirm: the step's own run starts."""
        self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': step['revision'], 'approval_id': 'confirm-' + step['revision']},
                          owner_dashboard=True)
        self.app().preparation_step(lambda r: {'status': 'admitted'})
        return self.job()['job_id']

    def closed(self):
        with self.store.connect() as db:
            return db.execute("SELECT count(*) FROM decisions WHERE suggestion_id=? AND choice='complete'", (self.sid,)).fetchone()[0]

    def test_a_confirmed_doc_edit_keeps_the_unsent_email_and_the_to_do_open(self):
        before = self.ready([CLEANUP, self.draft()])
        email = before['Send']
        run = self.confirm(before['Confirm document cleanup'])
        # The run did the cleanup and saved, as it did that night: done, with only the doc's link
        saved = self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': run, 'body': 'Cleaned up the doc formatting.',
                                              'next_actions': [OPEN], 'outcome': 'done', 'finish_state': 'completed'})
        self.assertEqual(saved['status'], 'prepared')
        row = self.row()
        self.assertEqual(row['status'], 'prepared')
        self.assertEqual(self.closed(), 0)
        self.assertIsNone(row['done_report'])
        after = self.steps()
        self.assertEqual(after['Send'], email)  # the draft exactly as it was: same revision, text and recipient
        self.assertIn('Open Google Doc', after)
        self.assertNotIn('Confirm document cleanup', after)  # that step is done
        self.assertIsNone(row['outcome'])
        self.assertIn('Send', [b['label'] for b in a.controls(row)['blocks'][0]['buttons']])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT status FROM action_jobs WHERE revision=?", (before['Confirm document cleanup']['revision'],)).fetchone()[0], 'done')
        # Sending the email is the last step: then the to-do is done
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('send-1',?,?,'{}','sent',?,?,'send','dashboard','')", (self.sid, email['revision'], a.now(), a.now()))
            self.assertTrue(a.settle_sent(self.store, db, self.sid, 'send-1', 'Send'))
        self.assertEqual(self.row()['status'], 'completed')

    def test_a_result_that_keeps_needs_you_also_keeps_the_draft(self):
        before = self.ready([CLEANUP, self.draft()])
        run = self.confirm(before['Confirm document cleanup'])
        self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': run, 'body': 'Cleaned up the doc formatting.',
                                      'next_actions': [OPEN], 'outcome': 'needs_you', 'needs': 'check the doc', 'finish_state': 'completed'})
        self.assertEqual(self.steps()['Send'], before['Send'])
        self.assertEqual(a.json.loads(self.row()['outcome'])['needs'], 'check the doc')

    def test_another_confirm_stays_too(self):
        before = self.ready([CLEANUP, PLACEMENT, self.draft()])
        run = self.confirm(before['Confirm document cleanup'])
        self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': run, 'body': 'Cleaned up the doc formatting.',
                                      'next_actions': [OPEN], 'outcome': 'done', 'finish_state': 'completed'})
        after = self.steps()
        self.assertEqual(after['Confirm placement update'], before['Confirm placement update'])
        self.assertEqual(after['Send'], before['Send'])
        self.assertEqual(self.row()['status'], 'prepared')
        self.assertEqual(self.closed(), 0)

    def test_a_new_draft_in_the_result_replaces_the_old_one(self):
        before = self.ready([CLEANUP, self.draft()])
        run = self.confirm(before['Confirm document cleanup'])
        self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': run, 'body': 'Cleaned up the doc; the reply now mentions it.',
                                      'next_actions': [OPEN, self.draft(body='Cleaned up, here it is.')], 'outcome': 'needs_you',
                                      'needs': 'check the draft and send it', 'finish_state': 'completed'})
        drafts = [s for s in self.row()['next_actions'] if s['kind'] == 'email']
        self.assertEqual([d['body'] for d in drafts], ['Cleaned up, here it is.'])

    def test_a_step_run_on_the_owners_word_keeps_the_draft(self):
        before = self.ready([self.draft()])
        job = self.say('there are some weird a tags on headers in the doc, fix it', 'chat-fix')
        saved = self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'Cleaning up the doc now.',
                                              'next_actions': [CLEANUP], 'outcome': 'needs_you', 'needs': 'check the doc',
                                              'note_kind': 'new_ask', 'do_now': True})
        self.assertEqual(saved['done_now'], {'status': 'queued'})
        self.assertEqual(self.steps()['Send'], before['Send'])
        with self.store.connect() as db:  # only the asked step runs; the email still waits for Send
            self.assertEqual([r[0] for r in db.execute('SELECT revision FROM action_jobs')], [self.steps()['Confirm document cleanup']['revision']])

    def test_an_ordinary_chat_turn_still_drops_what_the_owner_no_longer_wants(self):
        self.ready([CLEANUP, self.draft()])
        job = self.say('skip the doc, just the email', 'chat-skip')
        self.app().action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'Only the reply now.',
                                      'next_actions': [self.draft()], 'outcome': 'needs_you', 'needs': 'check the draft and send it',
                                      'note_kind': 'new_ask'})
        self.assertEqual(list(self.steps()), ['Send'])

    def test_which_steps_count_as_the_same(self):
        email = {'kind': 'email', 'to': ['Pat@example.com']}
        self.assertEqual(a.next_actions.step_target(email), a.next_actions.step_target({'kind': 'email', 'to': ['pat@example.com']}))
        self.assertNotEqual(a.next_actions.step_target(email), a.next_actions.step_target({'kind': 'email', 'to': ['sam@example.com']}))
        self.assertNotEqual(a.next_actions.step_target(CLEANUP), a.next_actions.step_target(PLACEMENT))  # two Confirms on one doc
        self.assertEqual(a.next_actions.step_target({'kind': 'email', 'thread_id': 't1', 'to': ['x@example.com']})[1], 't1')


if __name__ == '__main__':
    unittest.main()

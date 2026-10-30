"""A final step that posts a chat message (a support-inbox reply, a DM in a web app): the card shows its exact text,
Edit changes what Confirm really posts, and a sent or submitted card closes with one status. Synthetic data only;
nothing is sent anywhere."""
import json
import unittest
import test_action_recovery as r
import test_next_actions as tn

p = r.p
a = p.a

CHAT = {'kind': 'finish', 'label': 'Submit inbox reply', 'url': 'https://inbox.example.invalid/conversation/7',
        'instructions': 'Open conversation 7, choose Reply (not a note), post the message exactly.',
        'preview': 'Customer-visible reply in conversation 7.', 'to_name': 'Sam Example',
        'message': 'Hi Sam,\n\nThanks, the export is fixed.\n\nBest,\nAlex'}
LEGACY = {k: v for k, v in CHAT.items() if k not in ('message', 'to_name')}
LEGACY['preview'] = 'Hi Sam,\n\nThanks, the export is fixed.'


class ChatFinish(unittest.TestCase):
    setUp = r.Finish.setUp
    job = r.Finish.job
    accept = r.Finish.accept
    ended = r.Finish.ended

    def ready_step(self, step):
        self.accept();self.app.preparation_step(lambda req: {'status': 'admitted'})
        self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job()['job_id'], 'body': 'Drafted the reply. Nothing sent.',
                                    'next_actions': [step], 'outcome': 'needs_you', 'needs': 'Approve the reply'})
        self.ended()
        return self.action_now()

    def action_now(self):
        with self.store.connect() as db:
            return a.next_actions.actions(db.execute('SELECT next_action FROM suggestions').fetchone()[0])[0]

    def confirm(self, revision, key='confirm'):
        result = self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': revision, 'approval_id': key}, owner_dashboard=True)
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        return result

    def test_message_and_recipient_are_kept_and_validated(self):
        action = self.ready_step(CHAT)
        self.assertEqual(action['message'], CHAT['message']);self.assertEqual(action['to_name'], 'Sam Example')
        self.assertIn(CHAT['message'], a.next_actions.preview(action))
        for bad in ({**CHAT, 'message': ''}, {**CHAT, 'message': 'x' * 8001}, {**LEGACY, 'to_name': 'Sam'}, {**CHAT, 'edited': True}):
            with self.assertRaises(ValueError):a.next_actions.validate(bad, {'accounts': []}, [])

    def test_edit_changes_exactly_what_confirm_posts(self):
        action = self.ready_step(CHAT)
        edited = 'Hi Sam,\n\nThe export works again. Sorry for the trouble!\n\nAlex'
        revised = self.app.action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': edited}, owner_dashboard=True)
        self.assertEqual(revised['status'], 'revised');self.assertNotEqual(revised['revision'], action['revision'])
        now = self.action_now()
        self.assertEqual(now['message'], edited);self.assertTrue(now['edited'])
        self.assertEqual({k: now[k] for k in ('instructions', 'url', 'preview', 'label', 'to_name')}, {k: CHAT[k] for k in ('instructions', 'url', 'preview', 'label', 'to_name')})
        # The old revision can no longer be confirmed: only the text the owner last saw goes out.
        with self.assertRaises(ValueError):self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'old'}, owner_dashboard=True)
        calls = [];self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': revised['revision'], 'approval_id': 'new'}, owner_dashboard=True)
        self.app.preparation_step(lambda req: calls.append(req) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        job_part = message.split('Drafts the owner edited')[0]  # the edit also teaches later drafts, below
        self.assertIn(edited, job_part);self.assertNotIn('the export is fixed', job_part)
        self.assertIn('as the owner edited it', message);self.assertIn('clear it and type exactly this text before you submit', message)
        self.assertIn('check that the posted text matches it', message)
        with self.store.connect() as db:
            edit = db.execute('SELECT kind,before_body,after_body FROM draft_edits').fetchone()
        self.assertEqual(tuple(edit), ('finish', CHAT['message'], edited))

    def test_a_step_without_message_edits_what_goes_out(self):
        action = self.ready_step(LEGACY)
        revised = self.app.action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': 'Hi Sam, fixed now.'}, owner_dashboard=True)
        self.assertEqual(self.action_now()['preview'], 'Hi Sam, fixed now.')
        calls = [];self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': revised['revision'], 'approval_id': 'go'}, owner_dashboard=True)
        self.app.preparation_step(lambda req: calls.append(req) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        self.assertIn('Hi Sam, fixed now.', message);self.assertIn('The owner edited what goes out themselves', message)

    def test_unedited_step_keeps_the_prepared_text(self):
        action = self.ready_step(CHAT)
        unchanged = self.app.action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': CHAT['message'] + '\n'}, owner_dashboard=True)
        self.assertEqual(unchanged, {'status': 'unchanged', 'revision': action['revision']})
        calls = [];self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': action['revision'], 'approval_id': 'go'}, owner_dashboard=True)
        self.app.preparation_step(lambda req: calls.append(req) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        self.assertIn(CHAT['message'], message);self.assertNotIn('as the owner edited it', message)

    def test_a_running_or_uncertain_step_cannot_be_edited(self):
        action = self.ready_step(CHAT);self.confirm(action['revision'])
        with self.store.connect() as db:db.execute("UPDATE suggestions SET status='prepared'")
        with self.assertRaises(ValueError):
            self.app.action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': 'Other text'}, owner_dashboard=True)

    def test_a_completed_step_closes_the_card_with_one_status(self):
        action = self.ready_step(CHAT);self.confirm(action['revision'])
        saved = self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job()['job_id'], 'body': 'Posted the reply; it shows in the conversation.',
                                            'next_actions': [CHAT], 'outcome': 'done', 'finish_state': 'completed'})
        self.ended()
        self.assertEqual(saved['status'], 'completed')
        row = self.store.snapshot([])['suggestions'][0]
        self.assertEqual(row['status'], 'completed');self.assertIsNone(row['outcome'])
        self.assertNotIn('Needs you', a.card(row));self.assertNotIn('Mark it done', a.card(row))
        # Undo brings it back as it was, without the stale needs-you line.
        self.store.decide(self.sid, 'undo', '', 'undo-1', 'dashboard')
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'], 'prepared')

    def test_a_step_that_was_not_performed_keeps_the_card_ready(self):
        action = self.ready_step(CHAT);self.confirm(action['revision'])
        self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job()['job_id'], 'body': 'Sign in first; nothing was posted.',
                                    'next_actions': [CHAT], 'outcome': 'needs_you', 'needs': 'Sign in', 'finish_state': 'not_performed'})
        self.ended()
        self.assertEqual(self.store.snapshot([])['suggestions'][0]['status'], 'prepared')


class SentCard(unittest.TestCase):
    setUp = tn.NextActions.setUp
    row = tn.NextActions.row
    decide = tn.NextActions.decide
    app = tn.NextActions.app
    draft = tn.NextActions.draft
    confirm = tn.NextActions.confirm
    transport = tn.NextActions.transport

    def test_sent_email_leaves_ready_with_only_the_sent_status(self):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Drafted a short reply. Nothing sent.', 'next_action': self.draft(),
                                      'outcome': 'needs_you', 'needs': 'Approve the reply to Sam.'})
        self.confirm();self.app().action_step(self.transport(send=lambda *_: {'message_id': 'm-1'}))
        row = self.row()
        self.assertEqual(row['status'], 'completed');self.assertIsNone(row['outcome'])
        self.assertEqual(row['body'], 'Drafted a short reply.')
        text = a.card(row)
        self.assertIn('Email sent', text);self.assertNotIn('Needs you', text);self.assertNotIn('Nothing sent', text);self.assertNotIn('Done.', text)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT choice,source FROM decisions WHERE id LIKE 'sent:%'").fetchone()[:], ('complete', 'assistant'))
        # A repeated tap on the closed card is the same send, never a second one.
        self.assertTrue(self.confirm(key='late-tap')['duplicate'])

    def test_a_card_with_another_waiting_send_stays_ready(self):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Two replies ready.', 'next_actions': [
            self.draft(label='Send reply', in_reply_to='<m1@example.com>'), self.draft(label='Send to finance', to=['finance@example.com'], body='Second approved draft.')]})
        first = self.row()['next_actions'][0]
        self.confirm(first['revision']);self.app().action_step(self.transport(send=lambda *_: {'message_id': 'm-1'}))
        self.assertEqual(self.row()['status'], 'prepared')


if __name__ == '__main__':
    unittest.main()

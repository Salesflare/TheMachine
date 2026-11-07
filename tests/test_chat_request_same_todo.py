"""A request the owner adds in a chat for a matter that already has a to-do ends up on that to-do and its draft, not
on a second to-do (learning, 2026-11-07): in the to-do's own chat, as a Telegram reply to it, and as a new to-do
that is the same matter (the merge offer)."""
import json
import unittest

import test_new_card as nc

a = nc.a


class ChatRequestSameTodo(unittest.TestCase):
    setUp = nc.NewCard.setUp
    new, review, row, mail_id = nc.NewCard.new, nc.NewCard.review, nc.NewCard.row, nc.NewCard.mail_id

    def cards(self):
        with self.store.connect() as db:
            return db.execute("SELECT count(*) FROM suggestions WHERE status!='rejected'").fetchone()[0]

    def jobs(self, sid):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM preparations WHERE suggestion_id=? ORDER BY created_at', (sid,))]

    def drafted(self):
        """A to-do for Sam's mail with a draft ready (prepared)."""
        self.store.commit_page('w', {}, [nc.mail('m1')])
        other = self.review(event_ids=[1], dedupe_key='w:sam')
        self.store.decide(other['id'], 'accept', '', 'go', 'dashboard')
        job = self.jobs(other['id'])[-1]['job_id']
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running' WHERE job_id=?", (job,))
        self.store.prepare(other['id'], 'The reply to Sam is ready.', job)
        self.assertEqual(self.row(other['id'])['status'], 'prepared')
        return other

    def test_a_note_in_the_todos_chat_changes_that_todo(self):
        other = self.drafted()
        self.store.decide(other['id'], 'other', 'Also mention the new start date', 'chat-1', 'dashboard')
        self.assertEqual(self.cards(), 1)
        self.assertEqual(self.jobs(other['id'])[-1]['status'], 'queued')
        self.assertEqual(self.row(other['id'])['status'], 'instructions')

    def test_merging_into_a_todo_not_started_yet_starts_nothing(self):
        self.store.commit_page('w', {}, [nc.mail('m1')])
        other = self.review(event_ids=[1], dedupe_key='w:sam')
        made = self.new(text='Also mention the new start date to Sam')
        self.review(event_ids=[made['event_id'], 1], card_id=other['id'], dedupe_key='owner:x')
        self.app.action('card_merge', {'suggestion_id': made['id'], 'merge': True, 'decision_id': 'm1'}, owner_dashboard=True)
        kept = self.row(other['id'])
        self.assertEqual((kept['status'], kept['owner_words']), ('pending', 'Also mention the new start date to Sam'))
        self.assertEqual(self.jobs(other['id']), [])

    def test_a_new_todo_for_the_same_matter_merged_updates_the_existing_draft(self):
        other = self.drafted()
        made = self.new(text='Also mention the new start date to Sam')
        self.assertTrue(self.review(event_ids=[made['event_id'], 1], card_id=other['id'], dedupe_key='owner:x')['merge_offered'])
        self.app.action('card_merge', {'suggestion_id': made['id'], 'merge': True, 'decision_id': 'm1'}, owner_dashboard=True)
        self.assertEqual(self.cards(), 1)
        # The added request reaches the draft: the existing to-do runs again with the owner's words as their note
        job = self.jobs(other['id'])[-1]
        self.assertEqual(job['status'], 'queued')
        with self.store.connect() as db:
            note = db.execute("SELECT feedback,source FROM decisions WHERE suggestion_id=? AND choice='other' ORDER BY created_at DESC",
                              (other['id'],)).fetchone()
        self.assertEqual((note['feedback'], note['source']), ('Also mention the new start date to Sam', 'dashboard'))


if __name__ == '__main__':
    unittest.main()

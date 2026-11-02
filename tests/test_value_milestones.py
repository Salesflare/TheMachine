"""Onboarding value past the first approval (a click), in the hosted health report (first_cards_report): the first to-do
whose preparation finished with a result or draft (first_prepared) and the first action its provider confirmed went
through (first_verified_action). Time and kind only, kept once. No live sends: a fake transport stands in."""
import json
import unittest

import test_next_actions as na
import test_ux as ux
a = ux.a


class ValueMilestones(unittest.TestCase):
    setUp = ux.UX.setUp
    row = ux.UX.row
    job = ux.UX.job
    decide = ux.UX.decide
    app = na.NextActions.app
    draft = na.NextActions.draft
    ready = na.NextActions.ready
    confirm = na.NextActions.confirm
    transport = na.NextActions.transport
    action_job = na.NextActions.action_job

    def report(self):
        with self.store.connect() as db:
            return a.first_cards_report(db, [])

    def value(self):
        report = self.report()
        return {k: report[k] for k in ('first_prepared_at', 'first_prepared', 'first_prepared_backfill', 'first_verified_action_at',
                                       'first_verified_action', 'first_verified_action_backfill')}

    def test_a_ready_draft_then_a_send_the_provider_confirmed(self):
        self.assertEqual(self.value(), {'first_prepared_at': None, 'first_prepared': None, 'first_prepared_backfill': False,
                                        'first_verified_action_at': None, 'first_verified_action': None, 'first_verified_action_backfill': False})
        self.decide('accept')
        self.assertIsNone(self.value()['first_prepared'])  # started is not prepared
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'The reply is ready.', 'next_action': self.draft()})
        value = self.value()
        self.assertEqual((value['first_prepared'], value['first_prepared_backfill']), ('draft', False))
        self.assertTrue(value['first_prepared_at'])
        self.confirm()
        self.app().action_step(self.transport(send=lambda *_: {}))  # sent, but not confirmed: no verified action yet
        self.assertEqual(self.action_job()['status'], 'uncertain')
        self.assertIsNone(self.value()['first_verified_action'])
        report = self.report()
        self.assertEqual(report['first_approved'], 'approve')  # the click (Do it) is its own milestone
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET retry_at=NULL')
        self.app().action_step(self.transport(reconcile=lambda *_: {'message_id': 'accepted'}))  # Sent mail shows it went out
        value = self.value()
        self.assertEqual((value['first_verified_action'], value['first_verified_action_backfill']), ('email', False))
        first = value['first_verified_action_at']
        self.assertGreaterEqual(first, value['first_prepared_at'])
        # Kept once: a later confirmed action doesn't move it
        with self.store.connect() as db:
            a.note_first(db, 'first_verified_action', 'calendar')
        self.assertEqual((self.value()['first_verified_action_at'], self.value()['first_verified_action']), (first, 'email'))
        text = json.dumps(self.report())
        for secret in ('Verified subject', 'Exact approved draft', 'recipient@example.com'):
            self.assertNotIn(secret, text)

    def test_a_refused_send_and_a_demo_send_are_not_verified(self):
        self.ready()
        self.confirm()
        self.app().action_step(self.transport(send=lambda *_: {'rejected': 550}))
        self.assertEqual(self.action_job()['status'], 'failed')
        self.assertIsNone(self.value()['first_verified_action'])
        with self.store.connect() as db:  # a demo send that went through: still none
            db.execute("UPDATE action_jobs SET status='sent',message_id='demo',payload=json_set(payload,'$.kind','email_demo')")
        self.assertIsNone(self.value()['first_verified_action'])

    def test_a_result_without_a_draft(self):
        self.decide('accept')
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Their order shipped on Tuesday.'})
        self.assertEqual(self.value()['first_prepared'], 'result')

    def test_an_install_from_before_the_marks_estimates_them(self):
        self.ready()
        self.confirm()
        self.app().action_step(self.transport())
        with self.store.connect() as db:
            sent = db.execute("SELECT updated_at FROM action_jobs WHERE status='sent'").fetchone()[0]
            saved = db.execute('SELECT saved_at FROM draft_saves').fetchone()[0]
            db.execute("DELETE FROM milestones WHERE name IN ('first_prepared','first_verified_action')")
        self.assertEqual(self.value(), {'first_prepared_at': saved, 'first_prepared': 'draft', 'first_prepared_backfill': True,
                                        'first_verified_action_at': sent, 'first_verified_action': 'email', 'first_verified_action_backfill': True})
        # Nothing from before tracking began
        with self.store.connect() as db:
            db.execute("UPDATE milestones SET at=? WHERE name='tracking_since'", ('2999-01-01T00:00:00+00:00',))
        value = self.value()
        self.assertEqual((value['first_prepared'], value['first_verified_action']), (None, None))


if __name__ == '__main__':
    unittest.main()

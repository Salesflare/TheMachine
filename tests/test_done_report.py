"""A confirmed final step that runs while the owner is away (a filed issue, a submitted form) never leaves the list
silently: done, it reports back (Just done, a "Done:" notification, the phone's line); not done, it stays open."""
import unittest
from unittest.mock import patch

import test_action_recovery as r
import test_preparation as p
from seams import patch_everywhere  # noqa: E402

a = p.a
STEP = {'kind': 'finish', 'label': 'Submit issue', 'url': 'https://tracker.invalid/new',
        'instructions': 'File ONE issue in acme/app titled "Show every linked account". Return its link.',
        'preview': 'New issue in acme/app: Show every linked account'}
RESULT = 'Issue [#42](https://tracker.invalid/acme/app/42) was filed with your exact title and text.'


class DoneReport(unittest.TestCase):
    setUp = p.Preparation.setUp
    job = p.Preparation.job
    accept = p.Preparation.accept
    ended = r.Finish.ended

    def start(self):
        with patch.object(r, 'STEP', STEP):
            return r.Finish.start_finish(self)

    def card(self):
        return next(s for s in self.store.snapshot([])['suggestions'] if s['id'] == self.sid)

    def finish(self, state, body=RESULT, pushes=None):
        sent = [] if pushes is None else pushes
        with patch_everywhere(a, 'push_reach', return_value=([{'endpoint': 'https://push.invalid/1'}], 0)), \
             patch_everywhere(a, 'push_send', side_effect=lambda store, config, subs, payload, label, sender=None, **k: sent.append((payload, k)) or [{'status': 201}]):
            self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': self.job()['job_id'], 'body': body,
                                        'next_actions': [{'kind': 'open', 'label': 'Open issue', 'url': 'https://tracker.invalid/acme/app/42'}] if state == 'completed' else [STEP],
                                        'outcome': 'done' if state == 'completed' else 'needs_you', 'needs': 'Sign in',
                                        'finish_state': state})
        self.ended()
        return sent

    def test_a_step_that_went_through_reports_back_in_the_list_and_on_the_phone(self):
        self.start()
        pushes = self.finish('completed')
        card = self.card()
        self.assertEqual(card['status'], 'completed')
        self.assertTrue(card['done_report'])
        self.assertTrue(a.reported(card))
        # The phone hears it is done, with what happened, replacing the to-do's earlier notification
        self.assertEqual(len(pushes), 1)
        payload, kind = pushes[0]
        self.assertEqual(payload['title'], 'Done: Prepare a useful draft')
        self.assertIn('#42', payload['body'])
        self.assertTrue(payload['url'].endswith('#chat=' + self.sid))
        self.assertEqual(payload['tag'], self.sid)
        self.assertEqual(kind['kind'], 'result')
        # The phone app's own line says done, not "gone"; its notification stays until the owner saw it
        notice = a.app_notice(self.store, self.app.config, self.sid)
        self.assertEqual(notice['line'], 'Done: Prepare a useful draft')
        self.assertIn('#42', notice['body'])
        with self.store.connect() as db:
            a.notify.app_line_save(db, self.sid, 'Ready: Prepare a useful draft')
        with patch_everywhere(a, 'app_wake') as wake:
            self.assertEqual(a.app_clear_step(self.store, self.app.config), [])
        wake.assert_not_called()
        # Got it: only in Done from then on, and the phone's notification goes
        self.assertEqual(self.app.action('card_report_seen', {'ids': [self.sid]}, owner_dashboard=True), {'seen': 1})
        self.assertIsNone(self.card()['done_report'])
        self.assertEqual(a.app_notice(self.store, self.app.config, self.sid), {'gone': True})
        with patch_everywhere(a, 'app_wake') as wake:
            self.assertEqual(a.app_clear_step(self.store, self.app.config), [self.sid])

    def test_got_it_is_the_owners_own(self):
        self.start()
        self.finish('completed')
        with self.assertRaises(ValueError):
            self.app.action('card_report_seen', {'ids': [self.sid]}, owner_dashboard=False)
        with self.assertRaises(ValueError):
            self.app.action('card_report_seen', {'ids': []}, owner_dashboard=True)
        self.assertTrue(self.card()['done_report'])

    def test_a_step_that_did_not_go_through_stays_in_the_list(self):
        self.start()
        pushes = self.finish('not_performed', body='Sign in to the tracker first; nothing was filed.')
        card = self.card()
        self.assertEqual(card['status'], 'prepared')
        self.assertIsNone(card['done_report'])
        self.assertFalse(a.reported(card))
        self.assertEqual(pushes, [])
        self.assertEqual(self.q('SELECT status FROM action_jobs')['status'], 'needs_input')

    def test_a_run_that_stopped_keeps_the_to_do_open_with_try_again(self):
        self.start()
        self.store.preparation_blocked(self.sid, self.job()['job_id'], 'The tracker did not answer.')
        self.ended()
        card = self.card()
        self.assertNotIn(card['status'], ('completed', 'rejected'))
        self.assertIsNone(card['done_report'])
        self.assertEqual(self.job()['status'], 'blocked')
        self.assertEqual(self.q('SELECT status FROM action_jobs')['status'], 'paused')
        self.assertTrue(self.store.decide(self.sid, 'retry', '', 'retry-1', 'dashboard')['retrying'])

    def test_reopen_ends_the_report(self):
        self.start()
        self.finish('completed')
        self.store.decide(self.sid, 'reopen', '', 'reopen-1', 'dashboard')
        card = self.card()
        self.assertNotEqual(card['status'], 'completed')
        self.assertIsNone(card['done_report'])

    def test_a_day_later_it_is_only_in_done(self):
        self.start()
        self.finish('completed')
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET done_report=? WHERE id=?',
                       ((a.dt.datetime.now(a.dt.timezone.utc) - a.dt.timedelta(hours=a.REPORT_HOURS + 1)).isoformat(), self.sid))
        self.assertFalse(a.reported(self.card()))
        self.assertEqual(a.app_notice(self.store, self.app.config, self.sid), {'gone': True})

    def q(self, sql, *args):
        with self.store.connect() as db:
            return dict(db.execute(sql, args).fetchone())

    def test_the_dashboard_lists_them_under_just_done(self):
        import dashboard_parts
        page = dashboard_parts.assemble()
        self.assertIn("action:'card_report_seen'", page)
        self.assertIn('Just done', page)
        self.assertIn('${justDoneList(justDone(finished))}', page)


if __name__ == '__main__':
    unittest.main()

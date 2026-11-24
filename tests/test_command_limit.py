"""The service tells the plugin which awaited command belongs to work nobody asked for yet, which gets the shorter time limit
(openclaw-plugin/review-recovery.ts commandLimit); Do it and the owner's chat get the longer one."""
import unittest

import test_preparation


class CommandLimit(unittest.TestCase):
    def setUp(self):
        self.t = test_preparation.Preparation()
        self.t.setUp()
        self.addCleanup(self.t.temp.cleanup)

    def intent(self, job_id, call_id, **more):
        return self.t.app.action('preparation_tool_intent', {'job_id': job_id, 'call_id': call_id, 'tool': 'exec',
                                                             'params': {'command': 'find .', 'awaitResults': True}, **more})

    def test_a_to_do_prepared_ahead_says_so_for_an_awaited_command_only(self):
        sid = self.t.ahead()['id']
        self.t.app.preparation_step(lambda _: {'status': 'admitted'})
        job_id = self.t.q('SELECT job_id FROM preparations WHERE suggestion_id=?', sid)['job_id']
        self.assertEqual(self.intent(job_id, 'a', awaited=True), {'active': True, 'ahead': True})
        self.assertEqual(self.intent(job_id, 'b'), {'active': True})

    def test_do_it_is_never_ahead(self):
        self.t.accept()
        self.t.app.preparation_step(lambda _: {'status': 'admitted'})
        self.assertEqual(self.intent(self.t.job()['job_id'], 'a', awaited=True), {'active': True})


if __name__ == '__main__':
    unittest.main()

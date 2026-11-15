import tempfile
import unittest
from pathlib import Path
import machine.actions as machine_actions
import machine.main as machine_main
import machine.store.first_look as machine_store_first_look
import timeutil


class FirstTips(unittest.TestCase):
    """First-use tips (Store.first_tips): only for a new person, each gone for good once its button is used or closed."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Body', 'metadata': {}, 'deleted': False}])
        self.n = 0

    def decide(self, choice, source='dashboard'):
        self.n += 1
        sid = self.store.suggest('task', f'Task {self.n}', 'I can draft this.', [1])['id']
        with self.store.connect() as db:
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (f'd{self.n}', sid, choice, '', source, timeutil.now()))

    def test_a_new_person_gets_both_until_each_button_is_used(self):
        self.assertEqual(self.store.first_tips(), ['change', 'send'])
        self.decide('accept')  # Do it is not the tip's button
        self.assertEqual(self.store.first_tips(), ['change', 'send'])
        self.decide('reject', source='telegram')  # Not needed anywhere counts
        self.assertEqual(self.store.first_tips(), ['send'])
        self.decide('send')
        self.assertEqual(self.store.first_tips(), [])

    def test_closed_tips_never_come_back(self):
        self.assertEqual(self.store.tip_done('send')['first_tips'], ['change'])
        self.store.tip_done('send')
        self.assertEqual(self.store.first_tips(), ['change'])
        with self.assertRaises(ValueError):
            self.store.tip_done('tour')

    def test_someone_who_already_decided_to_dos_never_sees_them(self):
        self.decide('complete')
        self.assertEqual(self.store.first_tips(), [])
        with self.store.connect() as db:
            db.execute('DELETE FROM decisions')
        self.assertEqual(self.store.first_tips(), [], 'decided once, for good')

    def test_tips_stop_after_the_first_to_dos(self):
        self.store.first_tips()
        for _ in range(machine_store_first_look.FIRST_TIPS_UNTIL - 1):
            self.decide('snooze')
        self.assertEqual(self.store.first_tips(), ['change', 'send'])
        self.decide('complete')
        self.assertEqual(self.store.first_tips(), [])

    def test_only_the_owner_closes_a_tip_on_the_dashboard(self):
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, {'accounts': []}
        self.assertIn('tip_done', machine_actions.DASHBOARD_ACTIONS)
        self.assertIn('tip_done', machine_actions.OWNER_ACTIONS)
        with self.assertRaises(ValueError):
            app.action('tip_done', {'tip': 'change'})
        self.assertEqual(app.action('tip_done', {'tip': 'change'}, owner_dashboard=True)['first_tips'], ['send'])


if __name__ == '__main__':
    unittest.main()

"""A to-do only about the Machine itself (a gateway that keeps restarting: its one account is the Machine's own,
owner:system) is neither Work nor Personal. It used to count as Personal, so the To-dos filter listed such alerts under
Personal (Waiting, Later and Done too). Now its scope is None: the filter shows it under All only, and the Done counts
per area leave it out. A pin wins, and a to-do with any Work or Personal account keeps its area. Made-up data; offline."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('machine_own_scope_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import todo_areas  # noqa: E402

ACCOUNTS = [{'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'},
            {'id': 'work-mail', 'service': 'gmail', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
            {'id': 'home-chat', 'service': 'whatsapp', 'boundary': 'personal:whatsapp'}]


class MachineOwnScope(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.store.config = {'accounts': ACCOUNTS}

    def add(self, sid, accounts, status='pending', area=None):
        with self.store.connect() as db:
            db.execute('INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,area) VALUES (?,?,?,?,?,?,?,?,?)',
                       (sid, 'k-' + sid, 'A to-do', 'Its body.', '[]', a.json.dumps(accounts), status, '2026-11-10T09:00:00+00:00', area))

    def scope(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row.get('scope')

    def test_machine_own(self):
        self.assertTrue(todo_areas.machine_own('["gateway"]', ACCOUNTS))
        self.assertFalse(todo_areas.machine_own('["gateway","home-chat"]', ACCOUNTS))
        self.assertFalse(todo_areas.machine_own('["gateway"]', ACCOUNTS, 'personal'))
        self.assertFalse(todo_areas.machine_own('[]', ACCOUNTS))
        self.assertFalse(todo_areas.machine_own('["gone"]', ACCOUNTS))
        # what sharing and the rest go by is unchanged
        self.assertEqual(a.suggestion_scope('["gateway"]', ACCOUNTS), 'personal')

    def test_the_filter_shows_a_machine_alert_under_all_only(self):
        self.add('alert', ['gateway'])
        self.add('work', ['work-mail'])
        self.add('home', ['home-chat'])
        self.add('pinned', ['gateway'], area='personal')
        self.assertEqual([self.scope(x) for x in ('alert', 'work', 'home', 'pinned')], [None, 'work', 'personal', 'personal'])

    def test_done_leaves_a_machine_alert_out_of_work_and_personal(self):
        self.add('alert', ['gateway'], 'completed')
        self.add('work', ['work-mail'], 'completed')
        self.add('home', ['home-chat'], 'completed')
        with self.store.connect() as db:
            self.assertEqual(self.store.done_counts(db), {'all': 3, 'work': 1, 'personal': 1})
        self.assertEqual([c['id'] for c in self.store.done_page(scope='personal')['cards']], ['home'])
        self.assertEqual({c['id'] for c in self.store.done_page()['cards']}, {'alert', 'work', 'home'})
        self.assertIsNone(next(c for c in self.store.done_page()['cards'] if c['id'] == 'alert').get('scope'))


if __name__ == '__main__':
    unittest.main()

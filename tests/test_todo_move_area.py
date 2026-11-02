"""Moving a to-do to another area (todo_areas.py): Personal to Work at the owner's company and back, from the to-do's
More menu. Its accounts become that area's, so what it may send from follows; the move is an event line and has an
Undo. Its run can ask for a move (preparation_blocked move_to) but never makes one: the owner's tap does, and a to-do
stuck on exactly that carries on by itself. Offline: nothing is sent and no site is contacted."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('move_area_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import next_actions  # noqa: E402
import todo_areas  # noqa: E402

ACCOUNTS = [
    {'id': 'home-chat', 'service': 'whatsapp', 'boundary': 'personal:whatsapp'},
    {'id': 'home-phone', 'service': 'android', 'boundary': 'personal:phone'},
    {'id': 'acme-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
    {'id': 'acme-chat', 'service': 'slack', 'boundary': 'work:Acme'},
    {'id': 'side-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@side.example', 'boundary': 'work:Side', 'scope': 'personal'},
    {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'},
]


def chat(source_id, when):
    return {'account_id': 'home-chat', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': when, 'title': 'Invoices',
            'body': 'Why do I still get invoices?', 'metadata': {'from': 'Kai Rivera', 'chat_id': 'c1'}, 'deleted': False}


def email(account='acme-mail'):
    return {'kind': 'email', 'account_id': account, 'to': ['billing@vendor.example'], 'subject': 'Zero invoices', 'body': 'Hi, could you check this?'}


class Areas(unittest.TestCase):
    def test_the_owners_areas_and_where_a_to_do_is(self):
        self.assertEqual(todo_areas.areas(ACCOUNTS), [{'id': 'personal', 'label': 'Personal'}, {'id': 'work:Acme', 'label': 'Work'}])
        self.assertEqual(todo_areas.areas(ACCOUNTS + [{'id': 'b', 'boundary': 'work:Beta'}])[1:],
                         [{'id': 'work:Acme', 'label': 'Work at Acme'}, {'id': 'work:Beta', 'label': 'Work at Beta'}])
        self.assertEqual(todo_areas.current('["home-chat"]', ACCOUNTS), 'personal')
        self.assertEqual(todo_areas.current(['home-chat', 'acme-chat'], ACCOUNTS), 'work:Acme')  # any Work account makes it Work
        self.assertIsNone(todo_areas.current(['acme-chat', 'b'], ACCOUNTS + [{'id': 'b', 'boundary': 'work:Beta'}]))  # two companies
        self.assertEqual(todo_areas.accounts_in('work:Acme', ACCOUNTS), ['acme-mail', 'acme-chat'])
        self.assertEqual(todo_areas.accounts_in('personal', ACCOUNTS), ['home-chat', 'home-phone'])  # a work mailbox labeled personal is in neither
        with self.assertRaisesRegex(ValueError, 'Pick one of your areas'):
            todo_areas.check('work:Side', ['home-chat'], ACCOUNTS)
        with self.assertRaisesRegex(ValueError, 'in that area already'):
            todo_areas.check('personal', ['home-chat'], ACCOUNTS)


class MoveCard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        self.store.commit_page('home-chat', {}, [chat('m1', '2026-10-30T09:00:00+00:00'), chat('m2', '2026-11-02T09:00:00+00:00')])
        self.sid = self.store.suggest('home-chat:c1', 'Find out why the zero invoices keep coming', 'Kai still gets them.', [1])['id']

    def move(self, area=None, undo=None, owner=True):
        return self.app.action('card_move', {'suggestion_id': self.sid, 'area': area, 'undo': undo, 'decision_id': a.uuid.uuid4().hex},
                               owner_dashboard=owner)

    def row(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def card(self):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (self.sid,)).fetchone())
            self.store.card_views(db, [row])
        return row

    def lines(self):
        with self.store.connect() as db:
            owner, _ = self.app.card_chat_service(db, self.sid)
        return [i['text'] for i in owner if i.get('kind') == 'event']

    def allowed(self):
        return json.loads(self.row()['account_ids'])

    def test_a_personal_to_do_moves_to_work_and_sends_from_the_company_mailbox(self):
        with self.assertRaisesRegex(ValueError, 'company'):
            next_actions.validate(email(), self.app.config, self.allowed())
        self.assertEqual((self.card()['scope'], self.card()['area']), ('personal', 'personal'))
        moved = self.move('work:Acme')
        self.assertEqual((moved['area'], moved['line'], moved['resumed']), ('work:Acme', 'Moved to Work', False))
        self.assertEqual(self.allowed(), ['acme-mail', 'acme-chat'])
        self.assertEqual((self.card()['scope'], self.card()['area']), ('work', 'work:Acme'))
        self.assertTrue(self.app.is_work(self.row()['account_ids']))  # Work timing, sharing and handoffs follow
        self.assertEqual(next_actions.validate(email(), self.app.config, self.allowed())['from'], 'robin@acme.example')
        self.assertEqual(self.lines(), ['Moved to Work'])  # no "You"
        # The messages it came from stay where they were
        with self.store.connect() as db:
            self.assertEqual({r['account_id'] for r in db.execute('SELECT account_id FROM events')}, {'home-chat'})

    def test_undo_puts_it_back_and_takes_the_line_away(self):
        moved = self.move('work:Acme')
        self.move(undo=moved['decision_id'])
        self.assertEqual((self.allowed(), self.row()['area'], self.card()['scope']), (['home-chat'], None, 'personal'))
        self.assertEqual(self.lines(), [])
        with self.assertRaisesRegex(ValueError, 'can’t be undone'):
            self.move(undo=moved['decision_id'])
        # Only the latest move can be undone
        first = self.move('work:Acme'); self.move('personal')
        with self.assertRaisesRegex(ValueError, 'can’t be undone'):
            self.move(undo=first['decision_id'])
        self.assertEqual(self.lines(), ['Moved to Work', 'Moved to Personal'])

    def test_a_new_message_on_the_old_side_does_not_pull_it_back(self):
        self.move('work:Acme')
        self.store.suggest('home-chat:c1', 'Kai asked again about the invoices', 'Kai wrote again.', [2])
        self.assertEqual(self.allowed(), ['acme-mail', 'acme-chat'])
        self.assertEqual(self.card()['scope'], 'work')

    def test_only_the_owner_moves_it_and_only_to_their_own_areas(self):
        with self.assertRaisesRegex(ValueError, 'owner'):
            self.move('work:Acme', owner=False)
        for area in ('work:Side', 'work:Other', 'personal', '', None):
            with self.assertRaises(ValueError):
                self.move(area)
        with self.assertRaisesRegex(ValueError, 'owner’s controls'):
            self.app.action('card_move', {'suggestion_id': self.sid, 'area': 'work:Acme', 'decision_id': 'bad id!'}, owner_dashboard=True)
        self.store.decide(self.sid, 'complete', '', 'done-1', 'dashboard')
        with self.assertRaisesRegex(ValueError, 'Reopen it first'):
            self.move('work:Acme')
        self.assertEqual(self.allowed(), ['home-chat'])

    def test_a_run_asks_for_the_move_and_carries_on_after_the_owners_tap(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()['job_id']
        with self.assertRaisesRegex(ValueError, "move_to: .*work:Acme"):
            self.store.preparation_blocked(self.sid, job, 'This needs to go from the Acme mailbox.', move_to='work:Nope')
        self.store.preparation_blocked(self.sid, job, 'The email to the vendor has to come from your Acme address.', move_to='work:Acme')
        card = self.card()
        self.assertEqual((card['preparation_status'], card['preparation_move_to']), ('blocked', 'work:Acme'))
        self.assertEqual(self.allowed(), ['home-chat'])  # asking moved nothing
        moved = self.move('work:Acme')
        self.assertTrue(moved['resumed'])
        card = self.card()
        self.assertEqual((card['preparation_status'], card['preparation_move_to']), ('queued', None))
        self.assertEqual(self.lines(), ['Do it', 'Moved to Work'])  # it carried on by itself: no Try again of theirs

    def test_a_to_do_stuck_on_something_else_keeps_try_again(self):
        self.store.decide(self.sid, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            job = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (self.sid,)).fetchone()['job_id']
        self.store.preparation_blocked(self.sid, job, 'The vendor portal is down.')
        self.assertFalse(self.move('work:Acme')['resumed'])
        self.assertEqual(self.card()['preparation_status'], 'blocked')

    def test_the_run_is_told_its_area_and_how_to_ask(self):
        line = a.area_prompt(self.app.config, '["home-chat"]')
        self.assertIn('this to-do is in Personal', line)
        self.assertIn('move_to=<work:Acme (Work)>', line)
        self.assertIn('never move it yourself', line)
        self.assertEqual(a.area_prompt({'accounts': ACCOUNTS[:2]}, '["home-chat"]'), '')  # only one area: nothing to say
        self.assertIn('Area: this to-do is in', (ROOT / 'PREPARATION.md').read_text() + line)


if __name__ == '__main__':
    unittest.main()

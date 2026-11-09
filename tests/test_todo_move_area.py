"""Moving a to-do to another area (todo_areas.py): Personal to Work at the owner's company and back, from the to-do's
More menu. Its accounts become that area's, so what it may send from follows; the move is an event line and has an
Undo. Its run can ask for a move (preparation_blocked move_to): the owner's tap makes it, and a to-do stuck on exactly that
carries on by itself. When the messages it came from are all in that area, it moves there by itself. Offline: nothing is
sent and no site is contacted."""
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
        self.assertEqual(todo_areas.areas(ACCOUNTS), [{'id': 'personal', 'label': 'Personal'}, {'id': 'work:Acme', 'label': 'Work', 'name': 'acme.example'}])
        self.assertEqual(todo_areas.areas(ACCOUNTS + [{'id': 'b', 'boundary': 'work:Beta'}])[1:],
                         [{'id': 'work:Acme', 'label': 'Work at acme.example', 'name': 'acme.example'}, {'id': 'work:Beta', 'label': 'Work at Beta', 'name': 'Beta'}])
        # A company only made from a domain (work:Acme for robin@acme.example) reads as that domain, never capitalized;
        # one with a name of its own keeps it
        self.assertEqual(todo_areas.areas([{'id': 'm', 'email': 'jo@moreaudesign.io', 'boundary': 'work:Moreaudesign'},
                                           {'id': 'n', 'email': 'pat@initech.dev', 'boundary': 'work:Initech Corp'}])[0:2],
                         [{'id': 'work:Initech Corp', 'label': 'Work at Initech Corp', 'name': 'Initech Corp'},
                          {'id': 'work:Moreaudesign', 'label': 'Work at moreaudesign.io', 'name': 'moreaudesign.io'}])
        self.assertEqual(todo_areas.current('["home-chat"]', ACCOUNTS), 'personal')
        self.assertEqual(todo_areas.current(['home-chat', 'acme-chat'], ACCOUNTS), 'work:Acme')  # any Work account makes it Work
        self.assertIsNone(todo_areas.current(['acme-chat', 'b'], ACCOUNTS + [{'id': 'b', 'boundary': 'work:Beta'}]))  # two companies
        self.assertEqual(todo_areas.accounts_in('work:Acme', ACCOUNTS), ['acme-mail', 'acme-chat'])
        self.assertEqual(todo_areas.accounts_in('personal', ACCOUNTS), ['home-chat', 'home-phone', 'side-mail'])  # a work mailbox labeled personal is Personal
        self.assertEqual(todo_areas.current(['side-mail'], ACCOUNTS), 'personal')
        self.assertIsNone(todo_areas.area_of_account({'id': 'p', 'boundary': 'personal:me', 'scope': 'work'}))  # labeled work: no company, in neither
        with self.assertRaisesRegex(ValueError, 'Pick one of your areas'):
            todo_areas.check('work:Side', ['home-chat'], ACCOUNTS)
        with self.assertRaisesRegex(ValueError, 'in that area already'):
            todo_areas.check('personal', ['home-chat'], ACCOUNTS)

    def test_a_profile_named_after_its_own_source_is_no_company(self):
        # An owner's own LinkedIn and X profiles, set up as work:linkedin and work:x before the setup asked for a company
        mine = ACCOUNTS + [{'id': 'me-li', 'service': 'linkedin', 'transport': 'linkedin-inbox', 'boundary': 'work:linkedin'},
                           {'id': 'me-x', 'service': 'x', 'transport': 'x-inbox', 'boundary': 'work:x'},
                           {'id': 'beta-x', 'service': 'x', 'transport': 'x-inbox', 'boundary': 'work:Beta Labs'}]
        self.assertEqual(todo_areas.areas(mine), [{'id': 'personal', 'label': 'Personal'},
                                                  {'id': 'work:Acme', 'label': 'Work at acme.example', 'name': 'acme.example'},
                                                  {'id': 'work:Beta Labs', 'label': 'Work at Beta Labs', 'name': 'Beta Labs'}])
        self.assertEqual(todo_areas.current(['me-li'], mine), 'work')  # still Work, in no company
        self.assertEqual(todo_areas.current(['me-x', 'acme-chat'], mine), 'work:Acme')
        self.assertEqual(todo_areas.check('work:Acme', ['me-li'], mine), 'work:Acme')  # it can move to a company
        for area in ('work:linkedin', 'work:x', 'work'):
            with self.assertRaisesRegex(ValueError, 'Pick one of your areas'):
                todo_areas.check(area, ['home-chat'], mine)
        # Only a profile: one company, so plain Work
        self.assertEqual([x['label'] for x in todo_areas.areas(ACCOUNTS + mine[-3:-1])], ['Personal', 'Work'])

    def test_where_its_people_point(self):
        mine = ACCOUNTS + [{'id': 'beta-mail', 'service': 'gmail', 'email': 'robin@beta.example', 'boundary': 'work:Beta'},
                           {'id': 'me-li', 'service': 'linkedin', 'boundary': 'work:linkedin'}]
        domain = lambda value: str(value or '').rpartition('@')[2] if '@' in str(value or '')[1:] else ''
        point = lambda people, here='personal': todo_areas.pointed(people, mine, here, domain)
        self.assertEqual(point([{'side': 'work', 'accounts': ['home-chat', 'beta-mail']}]), 'work:Beta')  # heard on Beta's mailbox
        self.assertEqual(point([{'side': None, 'accounts': ['home-chat'], 'org_domain': 'acme.example'}]), 'work:Acme')  # works at Acme
        self.assertEqual(point([{'side': 'personal', 'accounts': ['acme-chat']}], 'work:Acme'), 'personal')
        self.assertIsNone(point([{'side': 'work', 'accounts': ['home-chat']}]))  # Work, but no company to go by
        self.assertIsNone(point([{'side': 'work', 'accounts': ['me-li']}]))  # a profile is no company
        self.assertIsNone(point([{'accounts': ['acme-chat']}, {'accounts': ['beta-mail']}]))  # two companies: no guess
        self.assertIsNone(point([{'accounts': ['acme-chat']}], 'work:Acme'))  # where it is already
        self.assertIsNone(point([]))

    def test_the_card_carries_the_hint_only_with_a_picker(self):
        import sqlite3
        db = sqlite3.connect(':memory:'); db.row_factory = sqlite3.Row
        db.executescript("CREATE TABLE graph_nodes(id TEXT,kind TEXT,info TEXT);CREATE TABLE graph_events(event_id INTEGER,node_id TEXT,direct INTEGER);"
                         "INSERT INTO graph_events VALUES(7,'p1',1);")
        db.execute("INSERT INTO graph_nodes VALUES('p1','person',?),('org:beta.example','org',?)",
                   (json.dumps({'side': 'work', 'accounts': ['home-chat'], 'org': 'org:beta.example'}), json.dumps({'domain': 'beta.example'})))
        mine = ACCOUNTS + [{'id': 'beta-mail', 'service': 'gmail', 'email': 'robin@beta.example', 'boundary': 'work:Beta'}]
        card = {'event_ids': '[7]', 'account_ids': '["home-chat"]'}
        self.assertEqual(a.area_hint(db, card, mine, 'personal'), 'work:Beta')
        self.assertIsNone(a.area_hint(db, card, ACCOUNTS, 'personal'))  # one other area: no picker, no hint


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
        self.assertIn('this to-do is in Personal (its accounts: whatsapp, android, gmail)', line)  # gmail: Side's, labeled personal
        self.assertIn('move_to=<work:Acme (Work: gmail, slack)>', line)  # what a move would get it
        self.assertIn('never for what the to-do is about', line)
        self.assertIn('never move it yourself', line)
        self.assertEqual(a.area_prompt({'accounts': ACCOUNTS[:2]}, '["home-chat"]'), '')  # only one area: nothing to say
        self.assertIn('Area: this to-do is in', (ROOT / 'PREPARATION.md').read_text() + line)



BETA = [{'id': 'beta-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@beta.example', 'boundary': 'work:Beta'}]


class MovesByItself(unittest.TestCase):
    """A run's move to the area all its sources are in happens with no tap; anything less clear keeps the button."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.accounts = ACCOUNTS + BETA
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = self.accounts
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': self.accounts, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        self.store.commit_page('acme-chat', {}, [{'account_id': 'acme-chat', 'source_id': 's1', 'kind': 'slack.message',
                                                  'occurred_at': '2026-11-04T13:00:00+00:00', 'title': 'Bug report', 'body': 'The report did not show up.',
                                                  'metadata': {'channel_name': 'DM Sam Lee', 'conversation_type': 'dm'}, 'deleted': False}])
        self.store.commit_page('home-chat', {}, [chat('m1', '2026-11-04T09:00:00+00:00')])

    def card(self, event_ids, **placed):
        sid = self.store.suggest('k' + ''.join(map(str, event_ids)) + str(placed), 'Look into the missing report', 'Sam asked about it.', event_ids, **placed)['id']
        self.store.decide(sid, 'accept', '', 'click-' + sid, 'dashboard')
        self.app.preparation_step(lambda req: {'status': 'admitted'})
        with self.store.connect() as db:
            return sid, db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()['job_id']

    def view(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
            owner, _ = self.app.card_chat_service(db, sid)
        return row, [i['text'] for i in owner if i.get('kind') == 'event']

    def test_a_to_do_asking_for_the_area_its_sources_are_in_moves_there_and_carries_on(self):
        sid, job = self.card([1], company='work:Beta')  # the review placed it with another company
        self.assertEqual(self.view(sid)[0]['area'], 'work:Beta')
        out = self.store.preparation_blocked(sid, job, 'The reply has to go from the Acme Slack.', move_to='work:Acme')
        self.assertEqual((out['status'], out['area'], out['resumed']), ('moved', 'work:Acme', True))
        card, lines = self.view(sid)
        self.assertEqual((json.loads(card['account_ids']), card['preparation_status']), (['acme-mail', 'acme-chat'], 'queued'))
        self.assertEqual(lines, ['Do it', 'Moved to Work at acme.example'])  # work:Acme is only its domain; a quiet line, no "You"; the area chip can move it back
        undo = self.app.action('card_move', {'suggestion_id': sid, 'area': 'work:Beta', 'decision_id': 'back-1'}, owner_dashboard=True)
        self.assertEqual(undo['area'], 'work:Beta')

    def test_anything_less_clear_keeps_the_button(self):
        cases = {'sources in another area': ([1], {}, 'work:Beta'),
                 'sources in two areas': ([1, 2], {'company': 'work:Beta'}, 'work:Acme'),
                 'pinned Personal (its own life)': ([1], {'personal': True}, 'work:Acme')}
        for case, (events, placed, to) in cases.items():
            with self.subTest(case):
                sid, job = self.card(events, **placed)
                before = self.view(sid)[0]['account_ids']
                self.assertEqual(self.store.preparation_blocked(sid, job, 'It needs the other area.', move_to=to)['status'], 'blocked')
                card = self.view(sid)[0]
                self.assertEqual((card['account_ids'], card['preparation_move_to']), (before, to))

    def test_after_a_move_the_next_one_is_the_owners(self):
        sid, job = self.card([1], company='work:Beta')
        self.app.action('card_move', {'suggestion_id': sid, 'area': 'personal', 'decision_id': 'mine-1'}, owner_dashboard=True)
        self.assertEqual(self.store.preparation_blocked(sid, job, 'It needs the Acme Slack.', move_to='work:Acme')['status'], 'blocked')


HOME_MAIL = {'id': 'home-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@mail.example', 'boundary': 'personal:mail'}


class PersonalReplyFromWorkMailbox(unittest.TestCase):
    """A matter of the owner's own life that came in on a mailbox labeled Work is Personal (its accounts are the
    Personal area's), but its reply goes from the mailbox its thread came in on: not refused, not rerouted to the
    Personal mailbox. Only the sender changes; the to-do stays Personal for sharing."""
    config = {'accounts': [*ACCOUNTS, HOME_MAIL]}
    replied = {'<family@school.example>': {'to': ['robin@acme.example'], 'from': 'teacher@school.example', 'sent': False,
                                           'account_id': 'acme-mail', 'thread_id': 'abc123', 'homes': {}}}

    def draft(self, **extra):
        return {'kind': 'email', 'account_id': 'acme-mail', 'to': ['teacher@school.example'], 'subject': 'Re: Field trip',
                'body': 'Yes, Kai can come.\n\nRobin', 'in_reply_to': '<family@school.example>', **extra}

    def test_the_reply_goes_from_the_work_mailbox_it_came_in_on(self):
        action = next_actions.validate(self.draft(), self.config, ['home-mail', 'home-chat'], replied=self.replied)
        self.assertEqual((action['account_id'], action['from'], action.get('thread_id')), ('acme-mail', 'robin@acme.example', 'abc123'))
        self.assertNotIn('reply_elsewhere', action)
        self.assertEqual(todo_areas.current(['home-mail', 'home-chat'], self.config['accounts']), 'personal')  # still Personal

    def test_only_its_own_thread_and_only_for_a_personal_to_do(self):
        new = self.draft(subject='Hello', in_reply_to=None)
        new.pop('in_reply_to')
        with self.assertRaises(ValueError):  # a new email from the Work mailbox: not its thread
            next_actions.validate(new, self.config, ['home-mail'], replied=self.replied)
        with self.assertRaises(ValueError):  # a thread in another mailbox
            next_actions.validate(self.draft(account_id='side-mail'), self.config, ['home-mail'], replied=self.replied)
        beta = {'accounts': [*self.config['accounts'], *BETA]}
        with self.assertRaises(ValueError):  # a Work to-do at another company keeps its company's mailboxes
            next_actions.validate(self.draft(), beta, ['beta-mail'], replied=self.replied)

    def test_the_run_is_told_to_reply_from_there_and_not_to_ask_for_a_move(self):
        line = a.area_prompt(self.config, '["home-mail", "home-chat"]', [(1, 'acme-mail')])
        self.assertIn('goes from the mailbox that thread came in on (robin@acme.example), also one labeled Work', line)
        self.assertIn('never ask to move this to-do to Work for it', line)
        self.assertNotIn('goes from the mailbox that thread', a.area_prompt(self.config, '["home-mail"]', [(1, 'home-mail')]))
        self.assertNotIn('goes from the mailbox that thread', a.area_prompt(self.config, '["acme-mail"]', [(1, 'acme-mail')]))


if __name__ == '__main__':
    unittest.main()

"""Intercom to-dos follow who the conversation is assigned to. Made-up data, no live calls.

A to-do comes only from a conversation assigned to the owner's own Intercom admin, to nobody, or only to a team inbox.
One a teammate was assigned is context for the review, not a to-do, and an open to-do made only from Intercom closes by
itself once a teammate takes the conversation: Done, with an event line and Undo, once per teammate."""
import importlib.util
import json
import tempfile
import types
import unittest
from pathlib import Path

from connectors import intercom

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('assignee_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

OWN = {'id': 'ic', 'service': 'intercom', 'transport': 'api', 'workspace_id': 'ws1', 'admin_id': '42', 'region': 'us',
       'email': 'owner@example.com'}
SHARED = {'id': 'ic', 'service': 'intercom', 'transport': 'api', 'workspace_id': 'ws1', 'admin_id': '42', 'region': 'us',
          'shared': {'fleet': 'f1', 'service': 'intercom', 'grant': 'g1'}}  # a teammate's token: admin 42 is theirs
MAIL = {'id': 'mail', 'service': 'gmail', 'email': 'owner@example.com'}


def conversation(assignee=None, team=None, parts=()):
    return {'id': '7', 'updated_at': 100, 'created_at': 50, 'title': 'Export question', 'state': 'open', 'open': True,
            'admin_assignee_id': assignee, 'team_assignee_id': team,
            'source': {'body': '<p>Can I export?</p>', 'author': {'type': 'user', 'email': 'customer@example.com', 'name': 'Casey'}},
            'conversation_parts': {'conversation_parts': list(parts), 'total_count': len(parts)}}


def said(admin, name, email, at=90):
    return {'id': 'p' + admin, 'created_at': at, 'part_type': 'comment', 'body': '<p>On it</p>',
            'author': {'type': 'admin', 'id': admin, 'name': name, 'email': email}}


HELPERS = types.SimpleNamespace(SourceError=a.SourceError, iso=a.CONNECTOR_HELPERS.iso)


class Connector(unittest.TestCase):
    def test_it_keeps_the_assignee_and_who_the_admins_are(self):
        m = intercom.event(OWN, conversation('51', parts=[said('51', 'Sam  Lee', 'Sam@Example.com')]), HELPERS)['metadata']
        self.assertEqual((m['admin_assignee_id'], m['assignee_name'], m['assignee_email']), ('51', 'Sam Lee', 'sam@example.com'))
        self.assertEqual(m['admin_emails'], {'51': 'sam@example.com'})
        for nobody in (None, 0, '0', 'x'):
            m = intercom.event(OWN, conversation(nobody, team=nobody), HELPERS)['metadata']
            self.assertEqual((m['admin_assignee_id'], m['team_assignee_id'], m['assignee_name']), (None, None, None))
        self.assertEqual(intercom.event(OWN, conversation(None, team=9), HELPERS)['metadata']['team_assignee_id'], '9')


class Assignment(unittest.TestCase):
    def test_owner_nobody_team_or_a_teammate(self):
        mine = ({'42'}, {'owner@example.com'})
        self.assertEqual(a.intercom_assignment({'admin_assignee_id': '42'}, *mine), 'owner')
        self.assertEqual(a.intercom_assignment({}, *mine), 'nobody')
        self.assertEqual(a.intercom_assignment({'team_assignee_id': '9'}, *mine), 'team')
        self.assertEqual(a.intercom_assignment({'admin_assignee_id': '51', 'team_assignee_id': '9', 'assignee_name': 'Sam'}, *mine), ('teammate', 'Sam'))
        self.assertEqual(a.intercom_assignment({'admin_assignee_id': '51'}, *mine), ('teammate', ''))
        # The owner's own address on the assignee: theirs, whatever the id
        self.assertEqual(a.intercom_assignment({'admin_assignee_id': '77', 'assignee_email': 'owner@example.com'}, *mine), 'owner')
        # Who the owner is in Intercom unknown, and the assignee unnamed: left as it was, never closed on a guess
        self.assertEqual(a.intercom_assignment({'admin_assignee_id': '51'}, set(), {'owner@example.com'}), 'unknown')


class Store(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.accounts = [OWN, MAIL]
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'database': str(Path(self.temp.name) / 'events.sqlite'),
                           'openclaw_config': str(Path(self.temp.name) / 'openclaw.json')}

    def sync(self, *raws, account=OWN):
        self.store.commit_page(account['id'], {}, [intercom.event(account, r, HELPERS) for r in raws])

    def card(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def test_no_to_do_from_a_conversation_a_teammate_was_assigned(self):
        self.sync(conversation('51', parts=[said('51', 'Sam', 'sam@example.com')]))
        with self.assertRaisesRegex(ValueError, 'assigned to Sam, not the owner'):
            self.store.suggest('c7', 'Answer Casey about export', 'Casey asks whether they can export.', [1])
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM events WHERE id=1').fetchone())
            view = a.review_view(row, assigned=self.store.intercom_assignments(db, [row])[1])
        self.assertIn('Assigned in Intercom to Sam, not the owner', view['assigned'])
        self.assertFalse({'admin_assignee_id', 'assignee_email', 'admin_emails', 'assignee_name'} & set(view.get('metadata', {})))

    def test_the_owners_unassigned_and_team_inbox_conversations_make_to_dos(self):
        for n, raw in enumerate((conversation('42'), conversation(None), conversation(None, team='9'))):
            raw['id'] = str(10 + n)
            self.sync(raw)
            self.assertIn('id', self.store.suggest(f'c{n}', 'Answer Casey about export', 'Casey asks whether they can export.', [n + 1]))

    def test_an_open_to_do_closes_quietly_once_a_teammate_takes_it_with_undo_once(self):
        self.sync(conversation(None))
        sid = self.store.suggest('c7', 'Answer Casey about export', 'Casey asks whether they can export.', [1])['id']
        self.assertEqual(self.store.close_taken_intercom(), [])
        self.sync(conversation('42'))  # the owner's own: stays
        self.assertEqual(self.store.close_taken_intercom(), [])
        self.sync(conversation('51', parts=[said('51', 'Sam', 'sam@example.com')]))
        self.assertEqual(self.store.close_taken_intercom(), [sid])
        self.assertEqual(self.store.close_taken_intercom(), [])
        card = self.card(sid)
        self.assertEqual((card['status'], card['closed_from']), ('completed', 'pending'))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT status FROM deliveries WHERE suggestion_id=?", (sid,)).fetchone()[0], 'cancelled')
            lines = [i for i in self.app.card_chat_service(db, sid)[0] if i['kind'] == 'event']
        self.assertEqual([i['text'] for i in lines], ['Closed by itself: Sam took it in Intercom'])
        # Undo brings it back and it stays, for this teammate
        self.assertEqual(self.store.decide(sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertEqual(self.store.close_taken_intercom(), [])
        self.assertEqual(self.card(sid)['status'], 'pending')

    def test_a_to_do_with_other_evidence_too_stays(self):
        self.sync(conversation(None))
        self.store.commit_page('mail', {}, [{'account_id': 'mail', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Export', 'body': 'Also by mail', 'deleted': False, 'metadata': {'from': 'customer@example.com'}}])
        sid = self.store.suggest('c7', 'Answer Casey about export', 'Casey asks whether they can export.', [1, 2])['id']
        self.sync(conversation('51'))
        self.assertEqual(self.store.close_taken_intercom(), [])
        self.assertEqual(self.card(sid)['status'], 'pending')

    def test_a_shared_intercom_finds_its_owner_by_address_never_by_the_sharers_admin(self):
        self.store.accounts = [SHARED, MAIL]
        # Admin 42 is the teammate whose token it is: assigned to them, it's not the owner's
        self.sync(conversation('42', parts=[said('42', 'Robin', 'robin@example.com')]), account=SHARED)
        with self.store.connect() as db:
            self.assertEqual(self.store.intercom_owner(db, 'ic')[0], set())
        with self.assertRaisesRegex(ValueError, 'assigned to Robin'):
            self.store.suggest('c7', 'Answer Casey about export', 'Casey asks whether they can export.', [1])
        # The owner wrote in another conversation as admin 63: that one is theirs from then on
        other = conversation('63', parts=[said('63', 'Owner', 'owner@example.com')])
        other['id'] = '8'
        self.sync(other, account=SHARED)
        with self.store.connect() as db:
            self.assertEqual(self.store.intercom_owner(db, 'ic')[0], {'63'})
        self.assertIn('id', self.store.suggest('c8', 'Answer Casey about import', 'Casey asks about import.', [2]))

    def test_the_line_is_in_every_language(self):
        for lang in ('nl', 'fr', 'de', 'es', 'it', 'pt-BR'):
            catalog = json.loads((ROOT / 'i18n' / f'{lang}.json').read_text())
            self.assertIn('Closed by itself: {} took it in Intercom', catalog)
            self.assertIn('Closed by itself: a teammate took it in Intercom', catalog)


if __name__ == '__main__':
    unittest.main()

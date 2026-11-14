"""A contact detail the owner states for someone goes on that person's record, not into Facts (contact_facts.py): the
record that has the number already, merged with the one other record of the same name; the one record the words name;
and when it is not certain who, or it is no contact detail, a fact as before. Undo puts it all back, and stays undone."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

spec = importlib.util.spec_from_file_location('contact_facts_assistant', Path(__file__).parent.parent / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
import contact_facts  # noqa: E402
import fact_links  # noqa: E402
import fact_ties  # noqa: E402
import learning_loop  # noqa: E402

NOW = dt.datetime(2026, 11, 9, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}, {'id': 'chat', 'service': 'whatsapp', 'email': 'Personal WhatsApp'}]}
ROBIN_MAIL, ROBIN_WA, KIM = 'email:robin@vale.example', 'wa:15550100', 'email:kim@north.example'
NUMBER = '+1 555 0100'


def at(days_ago):
    return (NOW - dt.timedelta(days=days_ago)).isoformat()


def mail(n, sender):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at(n), 'title': f'Mail {n}', 'body': 'Hello',
            'deleted': False, 'metadata': {'from': sender, 'to': 'sam@acme.example', 'cc': '', 'labels': ['INBOX'], 'message-id': f'<{n}@x>', 'thread_id': f't{n}'}}


def chat(n, phone, name):
    return {'account_id': 'chat', 'source_id': f'w{n}', 'kind': 'whatsapp.message', 'occurred_at': at(n), 'title': name, 'body': 'Hi',
            'deleted': False, 'metadata': {'chat_id': phone + '@s.whatsapp.net', 'chat_name': name, 'from_me': False, 'from': name,
                                           'sender_id': phone + '@s.whatsapp.net'}}


class ContactFacts(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.store.config = CONFIG
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)
        for e in (mail(1, 'Robin Vale <robin@vale.example>'), chat(2, '15550100', 'Robin Vale'), mail(3, 'Kim North <kim@north.example>')):
            self.store.commit_page(e['account_id'], {}, [e])
        self.build()
        self.todo = self.store.suggest('t1', 'Send the deck', 'Body', [1])['id']
        self.store.decide(self.todo, 'other', 'a note', 'owner-note', 'dashboard')

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def people(self):
        with self.store.connect() as db:
            return {r['id']: (r['name'], sorted(json.loads(r['info'])['identifiers'])) for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='person'")}

    def phones(self, node_id):
        with self.store.connect() as db:
            row = graph.resolve(db, node_id)
            return [p['value'] for p in json.loads(row['info']).get('phones') or []]

    def current_facts(self):
        return [f['text'] for f in self.store.facts()]

    def save(self, text, kind='contact', **more):
        return self.store.remember_fact(text, 'owner-note', kind, **more, quote='a note')

    def test_the_two_records_of_one_name_are_merged_when_the_number_is_on_one(self):
        self.assertEqual(sorted(i for i, (n, _) in self.people().items() if n == 'Robin Vale'), [ROBIN_MAIL, ROBIN_WA])  # never joined by name
        done = self.save(f"Robin Vale's WhatsApp number is {NUMBER}.")
        self.assertEqual((done['record'], done['name'], done['merged']), (ROBIN_WA, 'Robin Vale', True))
        self.assertEqual(self.current_facts(), [])  # not a fact
        self.build()
        robin = [ids for n, ids in self.people().values() if n == 'Robin Vale']
        self.assertEqual(robin, [sorted([ROBIN_MAIL, ROBIN_WA])])  # one person now
        self.assertEqual(self.phones(ROBIN_MAIL), ['+15550100'])
        with self.store.connect() as db:  # the to-do's chat says where it went, with Undo
            line = a.App.card_chat_learned(db, self.todo)
        self.assertEqual([(i['state'], i['record'], i['name']) for i in line], [('record', ROBIN_WA, 'Robin Vale')])
        self.assertEqual(self.save(f"Robin Vale's WhatsApp number is {NUMBER}.").get('duplicate'), True)  # said again: nothing new

    def test_a_number_for_the_one_record_its_words_name_is_added_as_the_owners(self):
        done = self.save('Kim North can be reached on +1 555 0199.')
        self.assertEqual((done['record'], done['merged'], done['added']), (KIM, False, True))
        self.build()
        self.assertEqual(self.phones(KIM), ['+1 555 0199'])
        with self.store.connect() as db:
            self.assertEqual(graph.people_by_phone(db, ['+15550199']), [(KIM, '+15550199')])
        self.assertEqual(self.current_facts(), [])

    def test_unknown_person_and_a_commitment_with_a_number_stay_facts(self):
        self.assertNotIn('record', self.save('Alex Unknown has the number +1 555 0142.'))
        self.assertNotIn('record', self.save('Call the plumber on 0476 11 22 33 before Friday.', 'commitment'))
        self.assertNotIn('record', self.save('Kim North and Robin Vale share +1 555 0177.'))  # two people named: never a guess
        self.assertEqual(len(self.current_facts()), 3)
        self.assertEqual(self.phones(KIM), [])

    def test_undo_puts_it_back_and_it_stays_undone(self):
        done = self.save(f"Robin Vale's WhatsApp number is {NUMBER}.")
        self.store.undo_learning(next(c['id'] for c in self.store_changes() if c['kind'] == 'contact'))
        self.build()
        self.assertEqual(sorted(i for i, (n, _) in self.people().items() if n == 'Robin Vale'), [ROBIN_MAIL, ROBIN_WA])
        self.assertEqual(self.current_facts(), [f"Robin Vale's WhatsApp number is {NUMBER}."])
        again = self.save(f"Robin Vale's WhatsApp number is {NUMBER}.")
        self.assertEqual((again['id'], again.get('duplicate'), 'record' in again), (done['id'], True, False))
        with self.store.connect() as db:
            self.assertEqual(contact_facts.movable(db, fact_links.index(db, CONFIG)), [])  # a fact the owner brought back

    def test_what_the_owner_said_on_the_record_holds(self):
        with self.store.connect() as db:  # they took the number off Robin, and said the two Robins are not the same
            graph.person_edit(db, ROBIN_WA, {'phones': []}, NOW.isoformat())
        self.assertNotIn('record', self.save(f"Robin Vale's WhatsApp number is {NUMBER}."))
        with self.store.connect() as db:
            graph.person_edit(db, ROBIN_WA, {'phones': ['+15550100']}, NOW.isoformat())
            graph.merge(db, ROBIN_MAIL, ROBIN_WA, False, NOW.isoformat(), 'owner')
        self.assertNotIn('record', self.save(f"Robin Vale's number is {NUMBER}."))
        self.assertEqual(len(self.current_facts()), 2)

    def test_the_facts_saved_before_move_once_only_when_they_say_nothing_else(self):
        with self.store.connect() as db:
            for text in (f"Robin Vale's WhatsApp number is {NUMBER}.", 'Kim North moved to Lisbon; her number is +1 555 0199 since 2025.',
                         'Kim North prefers calls.'):
                db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind,fact_kind) VALUES(?,'owner-note',?,?,'fact','fact')",
                           (text, self.todo, NOW.isoformat()))
        self.assertEqual(self.store.contacts_once(), [[1, ROBIN_WA]])
        self.assertIsNone(self.store.contacts_once())  # one time
        self.assertEqual(len(self.current_facts()), 2)
        self.assertEqual([c['kind'] for c in self.store_changes()], ['contact'])
        with self.store.connect() as db:  # it runs before fact_ties' pass, which then leaves the moved one alone
            self.assertNotIn(1, [r['id'] for r in fact_ties.loose(db)])

    def test_a_detail_is_one_number_or_one_address(self):
        self.assertEqual(contact_facts.detail('Her number is +32 470 12 34 56.'), ('phones', '+32 470 12 34 56'))
        self.assertEqual(contact_facts.detail('Mail her at robin@vale.example.'), ('emails', 'robin@vale.example'))
        self.assertIsNone(contact_facts.detail('The launch is on 2026-11-12.'))
        self.assertIsNone(contact_facts.detail('Call +1 555 0100 or +1 555 0101.'))
        self.assertIsNone(contact_facts.detail('Room 12 is free.'))

    def test_the_action_rebuilds_the_graph_after_a_move(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, CONFIG
        with patch.object(a.App, 'graph_later') as later:
            app.action('remember_fact', {'text': 'Kim North can be reached on +1 555 0199.', 'decision_id': 'owner-note', 'kind': 'contact', 'quote': 'a note'})
            later.assert_called_once()

    def store_changes(self):
        with self.store.connect() as db:
            return learning_loop.recent(db)


if __name__ == '__main__':
    unittest.main()

"""Facebook friends nobody in the Graph has, added as people (birthdays_facebook.add and remove, the Import birthdays from
Facebook to-do's Add button, docs/help/routines.md "Templates"): only on the owner's tap, each a Personal person
with their name and birthday (source facebook), never shared with a Work Fleet. Matched again at that moment: a name a
person in the Graph has now, or two people have, is skipped. One transaction, one Graph build after it, and nothing
looked up for them. Undo takes exactly those people away. Made-up people only."""
import datetime as dt
import importlib.util
import json
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('facebook_people_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import birthdays  # noqa: E402
import birthdays_facebook as fb  # noqa: E402
import enrichment  # noqa: E402
import graph  # noqa: E402
import person_birthday  # noqa: E402
import shared_graph  # noqa: E402

NOW = '2026-11-10T09:00:00+00:00'
FIRST = 'Ada Bram Cleo Dov Esme Finn Gia Hugo Ines Jules Kai Lena Milo Nora Otto Pia Quin Rhea Sami Tove Uma Vito Wren Xavi Yara'.split()
LAST = 'Arden Brook Calloway Dunmore Ellery Fairbank Garrow Hollis Ivers Jessup Kestrel Lowell Marsh Northam Orrin Pell Quarry Rook Stroud Thorne'.split()


class AddPeople(unittest.TestCase):
    ITEMS = [{'name': 'Sam Rivera', 'month': 11, 'day': 14}, {'name': 'Pat Quinn', 'month': 12, 'day': 9},
             {'name': 'Mira Holt', 'month': 1, 'day': 5, 'year': 1990}, {'name': 'Theo Brandt', 'month': 2, 'day': 7},
             {'name': 'Cher', 'month': 3, 'day': 3}, {'name': '', 'month': 4, 'day': 4}]

    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'email': 'owner@mail.example', 'service': 'gmail', 'boundary': 'personal'}],
                           'timezone': 'Europe/Brussels', 'browser_cdp_url': 'http://127.0.0.1:9'}
        self.store.accounts = self.app.config['accounts']
        self.app.birthdays_facebook_inline = True
        self.answer, self.builds = {'items': self.ITEMS}, []
        for name, value in (('birthdays_facebook_base', lambda s: 'http://127.0.0.1:9'), ('graph_later', lambda s: self.builds.append(1))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        p = patch.object(fb, 'read', lambda base, url=fb.PAGE, limits=None: self.answer); p.start(); self.addCleanup(p.stop)
        p = patch('subprocess.run', lambda *x, **k: subprocess.CompletedProcess(x, 0, '', '')); p.start(); self.addCleanup(p.stop)  # the lease
        with self.store.connect() as db:
            graph.ensure(db)
            for node, name in (('email:sam@mail.example', 'Sam Rivera'), ('email:pat@one.example', 'Pat Quinn'), ('email:pat@two.example', 'Pat Quinn')):
                db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,info) VALUES(?,'person',?,1,?,5,?)",
                           (node, name, '2026-11-01', json.dumps({'identifiers': [node], 'wrote': 3})))

    def step(self, sid, step):
        return self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': step}, owner_dashboard=True)

    def read(self):
        sid = self.app.birthdays_facebook_offer({'routine_id': 'r1'})
        self.step(sid, 'read')
        return sid

    def card(self, sid):
        with self.store.connect() as db:
            return fb.view(db, sid)

    def people(self):
        with self.store.connect() as db:
            return {r['name']: (r['id'], json.loads(r['info'])) for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='person'")}

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {'accounts': self.app.config['accounts'], 'embeddings': {'enabled': False}}, NOW)

    def test_the_preview_names_the_others_and_nothing_is_added_before_the_tap(self):
        sid = self.read()
        view = self.card(sid)
        self.assertEqual((view['matched'], view['ambiguous'], view['others'], view['others_shown'], view['added']),
                         (1, ['Pat Quinn'], 2, ['Mira Holt', 'Theo Brandt'], 0))  # no one-word or empty name
        self.assertEqual(set(self.people()), {'Sam Rivera', 'Pat Quinn'})
        with self.assertRaises(ValueError):
            self.app.action('birthdays_facebook', {'suggestion_id': sid, 'step': 'add'}, owner_dashboard=False)

    def test_add_makes_personal_people_with_their_birthday_never_shared(self):
        sid = self.read()
        self.assertEqual(self.step(sid, 'add'), {'state': 'preview', 'added': 2})
        self.assertEqual(self.builds, [1])  # one build for all of them, in the worker
        people = self.people()
        node, info = people['Mira Holt']
        self.assertTrue(node.startswith('manual:'))
        self.assertEqual((info['side'], info['side_by'], info['manual']), ('personal', 'owner', True))  # on their page at once
        with self.store.connect() as db:
            self.assertEqual(person_birthday.get(db, node)['value'], '1990-01-05')
            self.assertEqual(person_birthday.get(db, node)['source'], 'facebook')
            self.assertEqual(person_birthday.get(db, people['Theo Brandt'][0])['value'], '--02-07')
        self.assertEqual(self.card(sid)['added'], 2)
        with self.assertRaises(ValueError):
            self.step(sid, 'add')  # once
        self.build()
        people = self.people()
        self.assertTrue(graph.own_life(people['Mira Holt'][1]))  # Personal by the owner's word, after a build too
        with self.store.connect() as db:
            shared_graph.ensure(db)
            private = shared_graph.Scope(db, ['home'], set(), {'owner@mail.example'}).private
        self.assertTrue({people['Mira Holt'][0], people['Theo Brandt'][0]} <= private)
        self.assertNotIn('email:sam@mail.example', private)

    def test_a_name_the_graph_has_by_now_is_skipped(self):
        sid = self.read()
        with self.store.connect() as db:  # added by hand between the read and the tap
            db.execute('BEGIN IMMEDIATE')
            graph.create_record(db, 'person', {'name': 'Theo  Brandt'}, NOW)
            db.execute('COMMIT')
        self.build()
        self.assertEqual(self.step(sid, 'add')['added'], 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM manual_nodes WHERE name LIKE 'Theo%'").fetchone()[0], 1)

    def test_undo_takes_exactly_those_people_away(self):
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            mine = graph.create_record(db, 'person', {'name': 'Lou Garrow'}, NOW)['node_id']  # the owner's own, before
            db.execute('COMMIT')
        sid = self.read()
        self.step(sid, 'add')
        self.build()
        added = [i for n, (i, _) in self.people().items() if n in ('Mira Holt', 'Theo Brandt')]
        self.assertEqual(len(added), 2)
        self.assertEqual(self.step(sid, 'undo_add'), {'state': 'preview', 'undone': 2})
        self.assertEqual(set(self.people()) & {'Mira Holt', 'Theo Brandt', 'Lou Garrow'}, {'Lou Garrow'})  # gone at once
        with self.store.connect() as db:
            for table, column in (('manual_nodes', 'identifier'), ('graph_names', 'node_id'), ('person_edits', 'identifier'), ('person_facts', 'identifier')):
                self.assertEqual(db.execute(f'SELECT count(*) FROM {table} WHERE {column} IN (?,?)', added).fetchone()[0], 0, table)
            self.assertTrue(db.execute('SELECT 1 FROM manual_nodes WHERE identifier=?', (mine,)).fetchone())
        self.build()
        self.assertEqual(set(self.people()) & {'Mira Holt', 'Theo Brandt', 'Lou Garrow'}, {'Lou Garrow'})
        self.assertEqual((self.card(sid)['others'], self.card(sid)['added']), (2, 0))  # can be added again
        with self.assertRaises(ValueError):
            self.step(sid, 'undo_add')
        self.assertEqual(self.step(sid, 'add')['added'], 2)

    def test_add_after_save_on_the_done_todo(self):
        sid = self.read()
        self.assertEqual(self.step(sid, 'save')['saved'], 1)
        view = self.card(sid)
        self.assertEqual((view['state'], view['others'], view['others_shown']), ('saved', 2, ['Mira Holt', 'Theo Brandt']))
        self.assertEqual(self.step(sid, 'add'), {'state': 'saved', 'added': 2})
        self.assertEqual(self.card(sid)['added'], 2)
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 2)

    def test_five_thousand_at_once_are_quick_and_nothing_is_looked_up_for_them(self):
        names = [f'{f} {m} {l}' for f in FIRST for m in FIRST[:10] for l in LAST][:5000]
        self.answer = {'items': [{'name': n, 'month': 1 + i % 12, 'day': 1 + i % 28} for i, n in enumerate(names)]}
        sid = self.read()
        self.assertEqual(self.card(sid)['others'], 5000)
        start = time.monotonic()
        self.assertEqual(self.step(sid, 'add')['added'], 5000)
        took = time.monotonic() - start
        self.assertLess(took, 20, f'adding 5,000 took {took:.1f} s')
        self.assertEqual(self.builds, [1])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM graph_nodes WHERE kind='person' AND id LIKE 'manual:%'").fetchone()[0], 5000)
            due = {p['identifier'] for p in enrichment.people_due(db, NOW, 6000)}
            self.assertFalse({i for i in due if i.startswith('manual:')})
            self.assertEqual(len(due), 3)  # only the people with an address: none of them is looked up
            self.assertFalse([i for i in birthdays.close_people(db) if i.startswith('manual:')])  # no messages: no birthday to-dos for them
        start = time.monotonic()
        self.assertEqual(self.step(sid, 'undo_add')['undone'], 5000)
        self.assertLess(time.monotonic() - start, 20)


if __name__ == '__main__':
    unittest.main()

"""What The Machine updated today (graph_updates.py): the people, organizations and projects it changed or learned
something about since the owner's midnight, for the quiet line on top of each Graph list and the mark on its rows. The
owner's own edits and older changes stay out; each record counts once, with its newest change."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('graph_updates_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import graph_updates  # noqa: E402

NOW = dt.datetime(2026, 11, 4, 15, 0, tzinfo=dt.timezone.utc)
SAM, KIM, LEE = 'email:sam@client.example', 'email:kim@client.example', 'email:lee@client.example'


class GraphUpdates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        zone = patch('timeutil.local_tz', lambda: dt.timezone.utc); zone.start(); self.addCleanup(zone.stop)
        with self.store.connect() as db:
            for node, kind, name in ((SAM, 'person', 'Sam Lee'), (KIM, 'person', 'Kim Park'), (LEE, 'person', 'Lee Ray'),
                                     ('org:client.example', 'org', 'Client Co'), ('project:1', 'project', 'Client renewal')):
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,1,?)',
                           (node, kind, name, json.dumps({'identifiers': [node]} if kind == 'person' else {})))

    def today(self, at=NOW):
        with self.store.connect() as db:
            return graph_updates.today(db, at)

    def test_the_machines_changes_today_count_once_per_record_newest_first(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES(?,'head of ops','review','2026-11-04T09:00:00+00:00')", (SAM,))
            db.execute("INSERT INTO person_orgs(identifier,org,source,created_at) VALUES(?,'Client Co','review','2026-11-04T11:00:00+00:00')", (SAM,))
            db.execute("INSERT INTO graph_relations(a,b,relation,source,created_at) VALUES(?,?,'colleague of','review','2026-11-04T10:00:00+00:00')", (KIM, LEE))
            db.execute("INSERT INTO project_moves(project_id,stage,source,at,created_at) VALUES(1,'In review','review','2026-11-04T08:00:00+00:00','2026-11-04T08:00:00+00:00')")
        found = self.today()
        self.assertEqual(found['since'], '2026-11-04T00:00:00+00:00')
        people = found['people']
        self.assertEqual(people['count'], 3)
        self.assertEqual([x['name'] for x in people['items']], ['Sam Lee', 'Kim Park', 'Lee Ray'])
        self.assertEqual(people['items'][0]['change'], {'kind': 'org', 'org': 'Client Co'})  # Sam's newest of two
        self.assertEqual(people['items'][1]['change'], {'kind': 'relation', 'a_name': 'Kim Park', 'b_name': 'Lee Ray', 'relation': 'colleague of'})
        self.assertEqual(found['projects'], {'count': 1, 'ids': ['project:1'], 'items': [
            {'id': 'project:1', 'name': 'Client renewal', 'at': '2026-11-04T08:00:00+00:00', 'change': {'kind': 'move', 'stage': 'In review'}}]})
        self.assertEqual(found['orgs'], {'count': 0, 'items': []})

    def test_the_owners_own_edits_and_yesterdays_changes_stay_out(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES(?,'friend','owner','2026-11-04T09:00:00+00:00')", (SAM,))
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES(?,'investor','review','2026-11-03T23:30:00+00:00')", (KIM,))
            db.execute("INSERT INTO project_moves(project_id,stage,source,at,created_at) VALUES(1,'Won','owner','2026-11-04T08:00:00+00:00','2026-11-04T08:00:00+00:00')")
        found = self.today()
        self.assertEqual((found['people']['count'], found['projects']['count']), (0, 0))
        self.assertEqual(self.today(NOW - dt.timedelta(days=1))['people']['count'], 1)  # yesterday Kim's role was news

    def test_a_fact_about_a_record_counts_and_a_removed_one_does_not(self):
        with self.store.connect() as db:
            for fact, text, removed in ((1, 'Prefers calls in the morning', None), (2, 'Old news', '2026-11-04T12:00:00+00:00')):
                db.execute("INSERT INTO facts(id,text,decision_id,created_at,removed_at) VALUES(?,?,'d','2026-11-04T10:00:00+00:00',?)", (fact, text, removed))
                db.execute("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'agent','2026-11-04T10:00:00+00:00')", (fact, 'org:client.example' if fact == 1 else KIM))
        found = self.today()
        self.assertEqual([(x['name'], x['change']) for x in found['orgs']['items']], [('Client Co', {'kind': 'fact', 'text': 'Prefers calls in the morning'})])
        self.assertEqual(found['people']['count'], 0)

    def test_an_identifier_finds_the_person_it_now_belongs_to(self):
        with self.store.connect() as db:  # Sam's second address, joined to Sam's record
            db.execute('UPDATE graph_nodes SET info=? WHERE id=?', (json.dumps({'identifiers': [SAM, 'email:sam@home.example']}), SAM))
            db.execute("INSERT OR IGNORE INTO graph_identifiers(identifier,node_id) VALUES('email:sam@home.example',?)", (SAM,))
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES('email:sam@home.example','neighbor','review','2026-11-04T09:00:00+00:00')")
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES('email:gone@client.example','vendor','review','2026-11-04T09:00:00+00:00')")
        self.assertEqual([x['id'] for x in self.today()['people']['items']], [SAM])  # and one no longer in the graph is left out

    def test_a_list_marks_the_rows_updated_today(self):
        app = object.__new__(a.App); app.store = self.store; app.config = {'accounts': []}
        at = dt.datetime.now(dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at) VALUES(?,'head of ops','review',?)", (SAM, at))
        rows = {x['id']: x for x in app.graph_list('people', 'name')['items']}
        self.assertEqual(rows[SAM]['updated_at'], at)
        self.assertNotIn('updated_at', rows[KIM])


if __name__ == '__main__':
    unittest.main()

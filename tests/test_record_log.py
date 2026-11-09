"""Recent changes on a record (record_log.py): what The Machine changed or learned about a person, organization or
project, newest first, each with its source and the page's own correction. The owner's own edits stay out, and a
project's Undo shows only while the move it would take back still stands."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('record_log_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import record_log  # noqa: E402

SAM, KIM = 'email:sam@client.example', 'email:kim@client.example'


class RecordLog(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('w', {}, [{'account_id': 'w', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-11-02T09:00:00+00:00',
                                          'title': 'Renewal', 'body': 'Kim and I run ops here.', 'metadata': {'from': 'Sam Lee <sam@client.example>'},
                                          'deleted': False}])
        with self.store.connect() as db:
            self.mail = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
            for node, kind, name in ((SAM, 'person', 'Sam Lee'), (KIM, 'person', 'Kim Park'), ('org:client.example', 'org', 'Client Co'),
                                     ('project:1', 'project', 'Client renewal')):
                db.execute('INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES(?,?,?,1,1,?)',
                           (node, kind, name, json.dumps({'identifiers': [node]} if kind == 'person' else {})))

    def log(self, node):
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM graph_nodes WHERE id=?', (node,)).fetchone()
            return record_log.recent(db, row)

    def test_a_persons_page_lists_what_was_learned_with_its_message(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO person_roles(identifier,role,source,created_at,event_id,quote) VALUES(?,'head of ops','review','2026-11-03T10:00:00+00:00',?,'I run ops')",
                       (SAM, self.mail))
            db.execute("INSERT INTO person_orgs(identifier,org,org_id,source,via,event_id,created_at) VALUES(?,'Client Co','org:client.example','review',"
                       "'signature',?,'2026-11-02T10:00:00+00:00')", (SAM, self.mail))
            db.execute("INSERT INTO graph_relations(a,b,relation,source,event_id,created_at) VALUES(?,?,'colleague of','review',?,'2026-11-04T10:00:00+00:00')",
                       (SAM, KIM, self.mail))
            db.execute("INSERT INTO person_orgs(identifier,org,source,created_at) VALUES(?,'Elsewhere','owner','2026-11-05T10:00:00+00:00')", (KIM,))
        lines = self.log(SAM)
        self.assertEqual([x['kind'] for x in lines], ['relation', 'role', 'org'])
        relation = lines[0]
        self.assertEqual((relation['a_name'], relation['relation'], relation['b_name']), ('Sam Lee', 'colleague of', 'Kim Park'))
        self.assertEqual(relation['act'], {'unrelate': [SAM, KIM]})
        self.assertEqual(relation['source'], {'type': 'event', 'id': self.mail, 'via': 'email', 'at': '2026-11-02T09:00:00+00:00', 'from': 'Sam'})
        self.assertEqual(lines[1]['act'], {'edit': True})
        self.assertNotIn('quote', lines[1])  # the message is at hand, so the source is the message
        self.assertEqual(self.log(KIM)[0]['kind'], 'relation')  # the owner's own org for Kim is no news to them
        self.assertEqual(len(self.log(KIM)), 1)

    def test_an_organizations_page_lists_who_was_placed_there(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO person_orgs(identifier,org,source,via,event_id,created_at) VALUES(?,'client co','review','signature',?,"
                       "'2026-11-02T10:00:00+00:00')", (SAM, self.mail))
        lines = self.log('org:client.example')
        self.assertEqual([(x['kind'], x['name'], x['person']) for x in lines], [('member', 'Sam Lee', SAM)])
        self.assertEqual(lines[0]['source']['from'], 'Sam')

    def test_a_projects_latest_move_by_a_review_can_be_undone_while_it_stands(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO projects(id,name,created_at,board_id,stage,stage_by) VALUES(1,'Client renewal','2026-10-01T00:00:00+00:00',1,'Agreed','review')")
            db.executemany("INSERT INTO project_moves(project_id,board_id,stage,event_id,source,at,created_at) VALUES(1,1,?,?,?,?,'2026-11-09T00:00:00+00:00')",
                           [('Contacted', None, 'owner', '2026-10-20T10:00:00+00:00'), ('Agreed', self.mail, 'review', '2026-11-02T10:00:00+00:00')])
        lines = self.log('project:1')
        self.assertEqual([(x['kind'], x['stage'], x['at'][:10]) for x in lines], [('move', 'Agreed', '2026-11-02')])  # when it moved; the owner's own move stays out
        self.assertEqual(lines[0]['act'], {'stage': 'Contacted'})
        with self.store.connect() as db:
            db.execute("UPDATE projects SET stage='Won',stage_by='owner'")
        self.assertNotIn('act', self.log('project:1')[0])

    def test_an_updated_fact_says_what_it_was(self):
        with self.store.connect() as db:
            old = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,removed_at) VALUES('Sam wants 40 seats.','d1','2026-11-01T00:00:00+00:00','fact',"
                             "'2026-11-06T00:00:00+00:00')").lastrowid
            new = db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES('Sam wants 8 seats.','d2','2026-11-06T00:00:00+00:00','fact')").lastrowid
            db.execute('UPDATE facts SET merged_into=? WHERE id=?', (f'fact:{new}', old))
            db.executemany("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'review','2026-11-06T00:00:00+00:00')", [(old, SAM), (new, SAM)])
        [line] = self.log(SAM)
        self.assertEqual((line['kind'], line['text'], line['was'], line['fact']), ('fact', 'Sam wants 8 seats.', 'Sam wants 40 seats.', new))
        with self.store.connect() as db:
            db.execute("UPDATE fact_about SET removed_at='2026-11-07T00:00:00+00:00' WHERE fact_id=?", (new,))
        self.assertEqual(self.log(SAM), [])  # Not about Sam takes it off this page and out of the log

    def test_anything_else_has_no_log(self):
        self.assertEqual(record_log.recent(None, None), [])


if __name__ == '__main__':
    unittest.main()

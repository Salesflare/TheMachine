"""graph_identifiers: who has an identifier, derived from graph_nodes. Its triggers keep it in step with every graph
write, ensure() is safe to run again and makes it whole, dropping it loses nothing, and what the to-do list shows (the
status, Slack names, a person's emails) is the same with the table as without it."""
import datetime as dt
import gc
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('identifiers_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
from machine import stamps  # noqa: E402
from machine.store import graph_identifiers, views  # noqa: E402
import bounces  # noqa: E402

NOW = dt.datetime(2026, 11, 8, 9, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'work', 'email': 'sam@acme.example'}]
PEOPLE = [  # (id, kind, name, info)
    ('p1', 'person', 'Robin Example', {'identifiers': ['slack:U0ROBIN001', 'email:robin@client.example']}),
    ('p2', 'person', 'Ann Example', {'identifiers': ['email:ann@client.example', 'email:ann.b@client.example'],
                                     'emails': ['ann@client.example']}),
    ('p3', 'person', 'Lee Example', {'identifiers': ['email:lee@client.example'], 'note': 'knows "slack:U0ROBIN002"'}),
    ('p4', 'person', 'Robin Later', {'identifiers': ['slack:U0ROBIN001']}),  # a second match: the later one wins, as before
    ('o1', 'organization', 'Client', {'identifiers': ['slack:U0ROBIN002', 'email:ann@client.example']}),
    ('p5', 'person', 'Odd', 'not json'),
    ('p6', 'person', 'Odd list', {'identifiers': 'slack:U0ROBIN002'}),
]


def index(db):
    return sorted(tuple(r) for r in db.execute('SELECT identifier,node_id FROM graph_identifiers'))


def scanned(db):
    """What the table should hold: worked out in Python from graph_nodes."""
    out = []
    for node, info in db.execute("SELECT id,info FROM graph_nodes WHERE kind='person'"):
        try:
            ids = json.loads(info).get('identifiers')
        except (ValueError, AttributeError):
            continue
        ids = ids if isinstance(ids, list) else list(ids.values()) if isinstance(ids, dict) else [ids]
        out += [(i, node) for i in ids if isinstance(i, str)]
    return sorted(set(out))


class GraphIdentifiers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.owner_user_ids = set()
        self.store.accounts = ACCOUNTS
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start(); self.addCleanup(clock.stop)
        with self.store.connect() as db:
            for node, kind, name, info in PEOPLE:
                self.add(db, node, kind, name, info)

    def add(self, db, node, kind, name, info):
        columns = {'id': node, 'kind': kind, 'name': name, 'info': info if isinstance(info, str) else json.dumps(info)}
        for _, col, typ, notnull, default, pk in db.execute('PRAGMA table_info(graph_nodes)').fetchall():
            if notnull and default is None and not pk and col not in columns:
                columns[col] = 0 if 'INT' in (typ or '').upper() else ''
        db.execute(f'INSERT INTO graph_nodes({",".join(columns)}) VALUES({",".join("?" * len(columns))})', list(columns.values()))

    def test_triggers_keep_it_in_step(self):
        with self.store.connect() as db:
            self.assertEqual(index(db), scanned(db))
            self.assertIn(('slack:U0ROBIN001', 'p1'), index(db))
            self.assertNotIn('o1', {n for _, n in index(db)})  # people only
            db.execute("UPDATE graph_nodes SET info=? WHERE id='p1'", (json.dumps({'identifiers': ['slack:U0ROBIN009']}),))
            db.execute("UPDATE graph_nodes SET kind='person' WHERE id='o1'")
            db.execute("UPDATE graph_nodes SET kind='organization' WHERE id='p2'")
            db.execute("UPDATE graph_nodes SET id='p3b' WHERE id='p3'")
            db.execute("DELETE FROM graph_nodes WHERE id='p4'")
            db.execute("UPDATE graph_nodes SET name='Renamed' WHERE id='p5'")
            self.assertEqual(index(db), scanned(db))
            self.assertIn(('slack:U0ROBIN009', 'p1'), index(db))
            self.assertNotIn(('slack:U0ROBIN001', 'p1'), index(db))

    def test_ensure_is_safe_again_and_dropping_loses_nothing(self):
        with self.store.connect() as db:
            before = index(db)
            nodes = db.execute('SELECT * FROM graph_nodes ORDER BY rowid').fetchall()
            graph_identifiers.ensure(db); graph_identifiers.ensure(db)
            self.assertEqual(index(db), before)
            graph_identifiers.drop(db)
            self.add(db, 'p7', 'person', 'New', {'identifiers': ['email:new@client.example']})  # a graph write without it
            self.assertEqual([tuple(r) for r in db.execute('SELECT * FROM graph_nodes ORDER BY rowid')][:len(nodes)],
                             [tuple(r) for r in nodes])
            graph.ensure(db)  # the next start makes it again, whole
            self.assertEqual(index(db), scanned(db))
            self.assertIn(('email:new@client.example', 'p7'), index(db))
            db.execute("DROP TRIGGER graph_identifiers_update")  # a write it missed: rebuilt when a trigger is back
            db.execute("UPDATE graph_nodes SET info=? WHERE id='p7'", (json.dumps({'identifiers': ['email:newer@client.example']}),))
            graph_identifiers.ensure(db)
            self.assertEqual(index(db), scanned(db))

    def readers(self):
        for kept in [o for o in gc.get_objects() if isinstance(o, stamps.Kept)]:
            kept.clear()
        with self.store.connect() as db:
            ids = ['U0ROBIN001', 'U0ROBIN002', 'U0NOBODY01']
            out = {'slack_names': graph.slack_names(db, ids), 'slack_people': views._slack_people_names(db, ids),
                   'emails': [bounces.person_emails(db, e) for e in ('ann.b@client.example', 'lee@client.example', 'x@y.example')],
                   'resolve': [dict(graph.resolve(db, i) or {}) for i in ('email:ann.b@client.example', 'slack:U0ROBIN001',
                                                                         'slack:U0ROBIN002', 'p3')]}
        out['status'] = json.loads(json.dumps(self.store.snapshot([]), sort_keys=True, default=str))
        return out

    def test_what_is_shown_is_the_same_without_it(self):
        events = [{'account_id': 'work', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': NOW.isoformat(), 'title': 'Hi',
                   'body': 'Hello', 'deleted': False, 'metadata': {'from': 'Ann <ann.b@client.example>', 'to': 'sam@acme.example'}}]
        self.store.commit_page('work', {}, events)
        with self.store.connect() as db:
            db.execute("DELETE FROM graph_nodes WHERE id='p5'")  # the scan without the table fails on an info that is not JSON
            event_id = db.execute("SELECT id FROM events WHERE source_id='m1'").fetchone()[0]
            db.execute("INSERT OR IGNORE INTO identity_names(identifier,name) VALUES('slack:U0ROBIN002','Robin Slack')")
        card = self.store.suggest('k1', 'Answer U0ROBIN001', 'Robin asked.', [event_id])['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET source_line='Slack from U0ROBIN001' WHERE id=?", (card,))
        with_it = self.readers()
        self.assertEqual(with_it['slack_people']['U0ROBIN001'], 'Robin Later')
        self.assertEqual(with_it['emails'][0], ['ann@client.example', 'ann.b@client.example'])
        self.assertEqual(with_it['resolve'][0]['id'], 'p2')
        self.assertIn('Slack from Robin Later', json.dumps(with_it['status']))  # the card's source line, by the Graph's name
        with self.store.connect() as db:
            graph_identifiers.drop(db)
            seen = []
            db.set_trace_callback(seen.append)
            self.assertEqual(graph.slack_names(db, ['U0ROBIN001'])['U0ROBIN001'], 'Robin Later')
        self.assertTrue(any('info LIKE' in s for s in seen), 'without the table, the graph is read as before')
        self.assertEqual(self.readers(), with_it)


if __name__ == '__main__':
    unittest.main()

"""A graph build only when something it reads changed (graph.unchanged, App.graph_build keep), and a setup that writes,
and takes the write lock, only for what changed: the graph comes out the same as a full build's, row for row."""
import re
import sqlite3
import time
import unittest
from unittest.mock import patch

import graph
import graph_golden
import machine.app.graph_actions as graph_actions
import machine.main as machine_main
import test_graph as tg
from test_graph import CONFIG, NOW, chat, mail

SETTINGS = {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}
# What a build may read without a counter of its own: SQLite's and JSON's own, the counters themselves, and events,
# counted by events_shared (what a message shows, not the review's bookkeeping on it)
UNCOUNTED = {'sqlite_master', 'json_each', 'json_tree', 'pragma_table_info', 'data_stamps', 'graph_edits', 'events'}


def meeting(days_ago, *emails):
    n = next(tg.counter)
    return {'account_id': 'work', 'source_id': f'c{n}', 'kind': 'calendar.event', 'occurred_at': tg.at(days_ago), 'title': 'Planning',
            'body': '', 'deleted': False, 'metadata': {'attendees': [{'email': 'sam@acme.com', 'self': True},
                                                                    *({'email': e, 'displayName': e.split('@')[0].title()} for e in emails)]}}


class Skip(unittest.TestCase):
    setUp, add, build = tg.Graph.setUp, tg.Graph.add, tg.Graph.build

    def fixture(self):
        self.add(mail(30, 'Kim Lee (Initech) <kim@initech.example>', 'sam@acme.com', thread='deal'),
                 mail(29, 'Sam <sam@acme.com>', 'Kim Lee <kim@initech.example>, Bo Park <bo@initech.example>', ('SENT',), thread='deal'),
                 mail(12, 'Ann Bell <ann@client.example>', 'Sam <sam@acme.com>', cc='Kim Lee <kim@initech.example>'),
                 mail(11, 'Sam Owner <sam@home.example>', 'ann@client.example', ('SENT',)),  # an alias the owner sends from
                 mail(5, 'News <newsletter@shop.example>', 'sam@acme.com', ('CATEGORY_PROMOTIONS', 'INBOX')),
                 chat(4, '00000000002', 'Pat Moss'), chat(3, '00000000002', 'Pat Moss', mine=True),
                 meeting(2, 'kim@initech.example', 'ann@client.example'))

    def traced(self, db, run):
        """run() with every statement on db: (its result, the statements)."""
        sql = []
        db.set_trace_callback(sql.append)
        try:
            return run(), sql
        finally:
            db.set_trace_callback(None)

    def copy(self):
        """The database as it is now, in a second file (a full build runs there)."""
        path = self.store.path.with_name('full.sqlite')
        with self.store.connect() as db, sqlite3.connect(path) as out:
            db.backup(out)
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path

    def rows(self, path):
        with sqlite3.connect(path) as db:
            found = graph_golden.rows(db)
            found['own_addresses'] = sorted(db.execute('SELECT address,sources,state,reason FROM own_addresses').fetchall())
            found['graph_state'] = [r[:1] for r in db.execute('SELECT built_at FROM graph_state')]
        return found

    def full_and_incremental(self):
        """The same database built both ways: a full build (the setup's checks and writes under the write lock throughout,
        as every build once was) in a copy, and the build as the worker runs it here. Their rows."""
        full = self.copy()
        with machine_main.Store(full).connect() as db:
            db.isolation_level = None
            graph._build(db, SETTINGS, NOW.isoformat(), locked=True)
        summary = self.build()
        self.assertEqual(self.rows(full), self.rows(self.store.path))
        return summary

    def test_a_full_build_and_the_incremental_path_make_the_same_graph(self):
        self.fixture()
        self.build()
        self.full_and_incremental()  # nothing changed
        # new mail, a new address the owner sends from (their addresses change), a name the owner gave someone
        self.add(mail(1, 'Sam Lee <sam@side.example>', 'bo@initech.example', ('SENT',)), mail(0, 'Bo Park <bo@initech.example>', 'sam@acme.com'))
        with self.store.connect() as db:
            graph.rename(db, 'email:ann@client.example', 'Ann Bell-Moss', NOW.isoformat())
        self.full_and_incremental()

    def test_a_build_with_nothing_to_set_up_takes_the_write_lock_only_to_publish(self):
        self.fixture()
        self.build()
        with self.store.connect() as db:
            db.isolation_level = None
            _, sql = self.traced(db, lambda: graph.build(db, SETTINGS, NOW.isoformat()))
        self.assertEqual([s for s in sql if s.startswith('BEGIN IMMEDIATE')], ['BEGIN IMMEDIATE'])
        self.assertFalse([s for s in sql[:sql.index('BEGIN IMMEDIATE')] if re.match(r'\s*(INSERT|UPDATE|DELETE|REPLACE|CREATE TRIGGER)', s, re.I)])

    def test_a_build_reads_only_what_its_mark_counts(self):
        self.fixture()
        self.build()
        with self.store.connect() as db:
            db.isolation_level = None
            _, sql = self.traced(db, lambda: graph.build(db, SETTINGS, NOW.isoformat()))
        read = {t.lower() for s in sql for t in re.findall(r'\b(?:FROM|JOIN)\s+([A-Za-z_]\w*)', s)}
        self.assertEqual(read - set(graph.GRAPH_INPUTS) - UNCOUNTED, set(), 'add these to graph.GRAPH_INPUTS')

    def test_unchanged_until_something_a_build_reads_changes(self):
        self.fixture()
        mark = self.build()['mark']
        with self.store.connect() as db:
            self.assertTrue(graph.unchanged(db, mark))
            db.execute('UPDATE events SET ingested_at=ingested_at')  # the review's bookkeeping on a message: not read by a build
            db.commit()
            self.assertTrue(graph.unchanged(db, mark))
            self.assertFalse(graph.unchanged(db, None))
        self.add(mail(0, 'Kim Lee <kim@initech.example>', 'sam@acme.com'))  # a new message
        with self.store.connect() as db:
            self.assertFalse(graph.unchanged(db, mark))
        mark = self.build()['mark']
        with self.store.connect() as db:
            self.assertTrue(graph.unchanged(db, mark))
            graph.rename(db, 'email:kim@initech.example', 'Kimberly Lee', NOW.isoformat())  # the owner's edit
            db.commit()
            self.assertFalse(graph.unchanged(db, mark))

    def test_the_worker_skips_a_timed_build_only_while_nothing_changed(self):
        self.fixture()
        self.app.config = SETTINGS
        built = self.app.graph_build()
        self.assertIn('people', built)
        self.assertEqual(self.app.graph_build(keep=True), {'skipped': True})
        self.assertIn('people', self.app.graph_build())  # an edit's build (no keep) always builds
        self.add(mail(0, 'Kim Lee <kim@initech.example>', 'sam@acme.com'))
        self.assertIn('people', self.app.graph_build(keep=True))  # new mail
        self.assertEqual(self.app.graph_build(keep=True), {'skipped': True})
        self.app.config = {**SETTINGS, 'owner_name': 'Sam Owner'}  # a setting
        self.assertIn('people', self.app.graph_build(keep=True))
        later = time.monotonic() + graph_actions.GRAPH_KEEP_SECONDS + 1
        with patch.object(graph_actions.time, 'monotonic', return_value=later):  # an hour on: time alone changes a graph
            self.assertIn('people', self.app.graph_build(keep=True))


if __name__ == '__main__':
    unittest.main()

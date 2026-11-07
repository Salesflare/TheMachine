"""The people graph's rebuild holds no write lock while it computes (graph.build): syncs, the review, delivery and the
dashboard write on meanwhile. Only a short prepare and the publish take the lock. An edit to the graph committed
while it computed is never overwritten by the older graph: it is computed again, and after BUILD_TRIES the last try
holds the lock throughout, as every build did before."""
import sqlite3
import unittest
from unittest.mock import patch

import crm
import graph_publish
import test_graph as tg
from test_graph import NOW, graph, mail

KIM = 'email:kim@initech.example'


class Lock(unittest.TestCase):
    setUp_graph, add, build, node = tg.Graph.setUp, tg.Graph.add, tg.Graph.build, tg.Graph.node  # test_graph's helpers

    def setUp(self):
        self.setUp_graph()
        self.add(mail(3, 'Kim Lee <kim@initech.example>', 'sam@acme.com'), mail(2, 'Sam <sam@acme.com>', 'kim@initech.example', ('SENT',)))
        with self.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS probe(at TEXT)')  # what a sync or the review writes meanwhile
        self.path = self.store.path

    def during(self, act):
        """Runs act(other connection) while the build computes (crm.decorate is called near its end)."""
        real = crm.decorate
        calls = []

        def decorate(db, nodes, links):
            calls.append(db.in_transaction)
            other = sqlite3.connect(self.path, timeout=0.3)  # a writer that gives up quickly
            try:
                act(other, len(calls))
                other.commit()
            finally:
                other.close()
            return real(db, nodes, links)
        return patch.object(crm, 'decorate', decorate), calls

    def test_a_write_during_the_rebuild_goes_through_at_once(self):
        written = []

        def write(other, n):
            other.execute('INSERT INTO probe(at) VALUES(?)', (NOW.isoformat(),))
            written.append(n)
        hook, calls = self.during(write)
        with hook:
            self.build()
        self.assertEqual(written, [1])  # not "database is locked": the rebuild held no write lock while it computed
        self.assertEqual(self.node(KIM)['name'], 'Kim Lee')

        # as every build did before: one write transaction throughout, so the same write waits and gives up
        def blocked(other, n):
            with self.assertRaisesRegex(sqlite3.OperationalError, 'locked'):
                other.execute('INSERT INTO probe(at) VALUES(?)', (NOW.isoformat(),))
        hook, calls = self.during(blocked)
        with hook, self.store.connect() as db:
            db.isolation_level = None
            graph._build(db, {**tg.CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat(), locked=True)
        self.assertEqual(len(calls), 1)

    def test_an_edit_meanwhile_is_never_overwritten_by_the_older_graph(self):
        self.build()

        def rename(other, n):
            if n == 1:  # the owner renames Kim while the rebuild computes
                other.execute("INSERT OR REPLACE INTO graph_names(node_id,name,created_at) VALUES(?,?,?)", (KIM, 'Kimberly Lee', NOW.isoformat()))
                other.execute('UPDATE graph_nodes SET name=? WHERE id=?', ('Kimberly Lee', KIM))
        hook, calls = self.during(rename)
        with hook:
            self.build()
        self.assertEqual(len(calls), 2)  # computed again from a snapshot with the edit
        self.assertEqual(self.node(KIM)['name'], 'Kimberly Lee')

    def test_edits_every_time_end_in_one_build_under_the_lock(self):
        tries = []

        def edit(other, n):
            tries.append(n)
            try:
                other.execute("INSERT OR REPLACE INTO graph_names(node_id,name,created_at) VALUES(?,?,?)", (KIM, f'Kim {n}', NOW.isoformat()))
            except sqlite3.OperationalError:
                pass  # the last try holds the lock: this edit waits for it
        hook, calls = self.during(edit)
        with hook:
            found = self.build()
        self.assertEqual(len(calls), graph.BUILD_TRIES + 1)
        self.assertEqual(found['people'], 1)
        self.assertEqual(self.node(KIM)['name'], f'Kim {graph.BUILD_TRIES}')  # the last edit that got in

    def test_the_worker_tries_again_later_instead_of_holding_the_lock(self):
        def edit(other, n):
            other.execute("INSERT OR REPLACE INTO graph_names(node_id,name,created_at) VALUES(?,?,?)", (KIM, f'Kim {n}', NOW.isoformat()))
        hook, calls = self.during(edit)
        with hook, self.store.connect() as db:
            db.isolation_level = None
            with self.assertRaises(graph.Outdated):  # lock_last=False: the graph worker builds again in a few seconds
                graph.build(db, {**tg.CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat(), lock_last=False)
        self.assertEqual(len(calls), graph.BUILD_TRIES)  # never a try under the lock throughout
        self.assertEqual(len([c for c in calls if c]), len(calls))  # each computed from a read snapshot

    def test_a_build_writes_only_what_changed(self):
        self.build()
        with self.store.connect() as db:
            db.isolation_level = None
            before = {t: sorted(map(tuple, db.execute(f'SELECT * FROM {t}'))) for t in graph_publish.TABLES}
            edits = graph._edits(db)
            self.build()
            self.assertEqual(graph._edits(db), edits)  # nothing in the graph changed: no row written again
            self.assertEqual({t: sorted(map(tuple, db.execute(f'SELECT * FROM {t}'))) for t in graph_publish.TABLES}, before)
            db.execute("INSERT OR REPLACE INTO graph_names(node_id,name,created_at) VALUES(?,?,?)", (KIM, 'Kimberly Lee', NOW.isoformat()))
            edits = graph._edits(db)
            self.build()
            self.assertEqual(self.node(KIM)['name'], 'Kimberly Lee')
            self.assertLessEqual(graph._edits(db) - edits, 3)  # her row, not every row again

    def test_a_signal_on_a_node_twice_keeps_the_confirmed_label(self):
        rows = [('project:1', 7, '2026-01-02', 1, 0), ('project:1', 7, '2026-01-03', 0, 0), ('project:1', 7, '2026-01-04', 1, 1)]
        self.assertEqual(graph_publish._events(rows), {('project:1', 7): ('project:1', 7, '2026-01-02', 0, 1)})

    def test_only_edits_to_the_graph_are_counted(self):
        with self.store.connect() as db:  # the triggers exist once a build ran: a sync's or the review's write is no edit
            db.isolation_level = None
            self.build()
            before = graph._edits(db)
            db.execute('INSERT INTO probe(at) VALUES(?)', (NOW.isoformat(),))
            self.assertEqual(graph._edits(db), before)
            db.execute('UPDATE graph_nodes SET strength=strength WHERE id=?', (KIM,))
            self.assertEqual(graph._edits(db), before + 1)


if __name__ == '__main__':
    unittest.main()

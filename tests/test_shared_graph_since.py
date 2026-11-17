"""A Team Graph publish reads again only what could have changed (shared_graph_since.py, docs/shared-graph.md): a round
with nothing new reads and sends nothing, one where only scores moved puts the new scores on the records it has, and
after any change the team ends up with exactly what a round that reads everything gives, deletes and take-backs too.
The made-up Fleet and its fake Network are tests/test_shared_graph.py's."""
import json
import unittest
from unittest.mock import patch

from machine import stamps
import shared_graph as sg
import shared_graph_apart as apart
import shared_graph_since as since
import test_shared_graph as base  # by module: its test classes run in its own file, not again here
from test_shared_graph import BODY, FLEET, mail
import timeutil


class Since(base.SharedGraph):
    def setUp(self):
        super().setUp()
        self.children = []  # one per collect that read the database
        stores = {box.graph_secret(): box.store for box in self.boxes}

        def child(store, scope_args, keys, secret, kept, grants, reads=False):
            """The child process's work on a connection of its own, as apart.run's child does (the made-up Machines'
            connect has no Store behind it, so the real one would collect in-process)."""
            self.children.append(secret)
            st = stores[secret]
            request = apart._loads(apart._dumps({'scope': [sorted(a) if isinstance(a, (set, frozenset)) else a for a in scope_args],
                                                 'keys': list(keys), 'secret': secret, 'kept': set(kept),
                                                 'grants': [list(map(sorted, g)) for g in grants]}))
            db = apart._connect(str(st.path), st._seal_key, bool(getattr(st, 'protected', False)))
            try:
                with db:
                    db.execute('BEGIN')
                    found, read, looked = apart.reading(db, request)
            finally:
                db.close()
            return apart._loads(apart._dumps((found, sorted(read), looked) if reads else found))
        patcher = patch.object(apart, 'run', side_effect=child); patcher.start(); self.addCleanup(patcher.stop)

    def reads(self, box=None):
        """How many collects read the database since the last call (box: only its own)."""
        secret = (box or self.own).graph_secret()
        n = sum(1 for s in self.children if s == secret)
        self.children.clear()
        return n

    def puts(self, since_call):
        return [c[3]['blob']['header']['kind'] for c in self.net.calls[since_call:]
                if c[0] == 'own1' and c[2] == '/graph' and c[1] == 'POST' and (c[3] or {}).get('op') == 'put']

    def team_has(self):
        """What each teammate holds of the owner's Machine: its records and threads, as they read them."""
        return {box.member_id: (sorted(sg.canon(json.loads(r['body'])).decode() for r in self.team(box)),
                                sorted(sg.canon(json.loads(r['body'])).decode() for r in self.team(box, 'team_mail')))
                for box in (self.adm, self.mem)}

    def same_as_reading_everything(self):
        """A round that reads everything again (what was kept forgotten) sends nothing new, and the team has what it had."""
        had = self.team_has()
        state = self.own.meta('graph_out:' + FLEET, {}) or {}
        state.pop('inputs', None)
        self.own.set_meta('graph_out:' + FLEET, state)
        self.own.__dict__.pop('_graph_last', None)
        calls = len(self.net.calls)
        self.rounds()
        self.assertEqual(self.puts(calls), [], 'a round that read everything found something the last rounds missed')
        self.assertEqual(self.team_has(), had)

    def test_a_round_with_nothing_new_reads_and_sends_nothing(self):
        self.olive_mail()
        self.rounds()
        self.assertIn(BODY, json.dumps(self.team(self.mem, 'team_mail')))
        self.reads()
        calls = len(self.net.calls)
        for _ in range(3):
            self.own.graph_round(force=True)
        self.assertEqual(self.reads(), 0)
        self.assertEqual(self.puts(calls), [])
        self.add(self.own, mail('work', 40, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Renewal quote', 'Make it fifty seats.', 1, 't-renewal'))
        self.rounds()
        self.assertGreaterEqual(self.reads(), 1)
        self.assertIn('Make it fifty seats.', json.dumps(self.team(self.mem, 'team_mail')))
        self.same_as_reading_everything()

    def test_what_a_graph_build_rewrites_and_a_publish_never_reads_reads_nothing_again(self):
        self.olive_mail()
        self.rounds()
        self.reads()
        with self.own.store.connect() as db:
            db.execute("UPDATE graph_nodes SET info=json_set(info,'$.live',json('{\"at\":\"x\"}')),signals=coalesce(signals,0)+1")
            db.execute('UPDATE graph_links SET strength=strength+0.0001,last_at=last_at')
            db.execute('UPDATE events SET analyzed_version=coalesce(analyzed_version,0)+1')
        self.own.graph_round(force=True)
        self.assertEqual(self.reads(), 0)

    def test_only_scores_moved_the_records_get_the_new_scores_without_reading_again(self):
        self.olive_mail()
        self.rounds()
        self.reads()
        with self.own.store.connect() as db:
            db.execute("UPDATE graph_nodes SET strength=strength/3 WHERE kind IN ('person','org')")
            want = {r[0]: round(r[1], 3) for r in db.execute("SELECT name,strength FROM graph_nodes WHERE kind IN ('person','org')")}
        calls = len(self.net.calls)
        self.rounds()
        self.assertEqual(self.reads(), 0)
        self.assertEqual(self.puts(calls), ['delta'])
        got = {json.loads(r['body'])['name']: json.loads(r['body'])['score'] for r in self.team(self.mem)}
        self.assertEqual(got, {name: want[name] for name in got})
        self.same_as_reading_everything()

    def test_after_each_change_the_team_has_what_reading_everything_gives(self):
        self.olive_mail()
        self.add(self.own, mail('work', 41, 'Kim Lo <kim@buyer.example>', 'own1@acme.example', 'Pilot', 'Can we start the pilot in March?', 2, 't-pilot'),
                 mail('work', 42, 'Kim Lo <kim@buyer.example>', 'own1@acme.example', 'Re: Pilot', 'Also, the invoice address changed.', 1, 't-pilot'))
        self.judge(self.own, ('work-41', 'client', 'Kim asked about the pilot'), ('work-42', 'client', 'Kim sent a new address'))
        self.rounds()
        self.same_as_reading_everything()
        self.assertIn('invoice address', json.dumps(self.team(self.mem, 'team_mail')))
        with self.own.store.connect() as db:  # a message deleted in the mailbox
            db.execute("UPDATE events SET deleted=1 WHERE source_id='work-42'")
        self.rounds()
        self.assertNotIn('invoice address', json.dumps(self.team(self.mem, 'team_mail')))
        self.same_as_reading_everything()
        self.judge(self.own, ('work-41', 'personal', 'Kim wrote'))  # sorted again: no longer shared
        self.rounds()
        self.assertNotIn('pilot in March', json.dumps(self.team(self.mem, 'team_mail')))
        self.same_as_reading_everything()
        with self.own.store.connect() as db:  # an organization kept private
            sg.keep_private(db, 'org:client.example')
        self.rounds()
        self.assertEqual(self.team(self.mem, 'team_mail'), [])
        self.same_as_reading_everything()
        with self.own.store.connect() as db:  # a person gone from the graph
            db.execute("DELETE FROM graph_nodes WHERE kind='person' AND name='Kim Lo'")
        self.rounds()
        self.same_as_reading_everything()

    def test_the_list_of_blobs_to_pass_on_is_read_again_only_when_a_blob_came_or_went(self):
        self.olive_mail()
        self.rounds()
        def listed():
            with self.mem.store.connect() as db:
                return [dict(r) for r in db.execute(sg.BLOB_LIST, (FLEET,))]
        first = since.blob_list(self.mem, FLEET)
        self.assertTrue(first)
        self.assertEqual(first, listed())
        self.assertIs(since.blob_list(self.mem, FLEET), first)  # nothing changed: not read again
        self.add(self.own, mail('work', 43, 'Lee Park <lee@client.example>', 'own1@acme.example', 'Re: Renewal quote', 'Signed copy attached.', 0, 't-renewal'))
        self.rounds()
        self.assertEqual(since.blob_list(self.mem, FLEET), listed())
        self.assertGreater(len(listed()), len(first))

    def test_the_hour_and_a_thread_leaving_the_hold_read_again(self):
        self.olive_mail()
        self.rounds()
        reads = self.own.meta('graph_reads:' + FLEET)
        parts = {'scope': [['work']]}
        with self.own.store.connect() as db:
            timeutil.pin('2026-05-04T10:10:00+00:00'); self.addCleanup(timeutil.pin, None)
            first = since.inputs(db, reads, parts)
            timeutil.pin('2026-05-04T10:50:00+00:00')
            self.assertEqual(since.inputs(db, reads, parts), first)
            timeutil.pin('2026-05-04T11:01:00+00:00')
            self.assertNotEqual(since.inputs(db, reads, parts)[0], first[0])
            with patch.object(sg, 'HOLD', 7200):  # a thread sorted in the hour before: still in the hold
                db.execute("UPDATE share_threads SET sorted_at='2026-05-04T10:30:00+00:00', hand=NULL")
                db.commit()
                held = since.inputs(db, reads, parts)
            self.assertNotEqual(held[0], since.inputs(db, reads, parts)[0])
            self.assertIsNone(since.inputs(db, reads + ['no_counter_here'], parts)[0])  # an uncounted table: read every round


class Counters(unittest.TestCase):
    def test_a_build_rewriting_strength_and_live_counts_only_scores(self):
        import sqlite3
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE graph_nodes(id TEXT PRIMARY KEY,kind TEXT,name TEXT,strength REAL,last_at TEXT,signals INT,info TEXT)')
        db.execute('CREATE TABLE graph_links(a TEXT,b TEXT,kind TEXT,strength REAL,last_at TEXT,PRIMARY KEY(a,b))')
        stamps.watch_graph_shared(db)
        n = lambda: dict(db.execute("SELECT name,n FROM data_stamps"))
        db.execute("INSERT INTO graph_nodes VALUES('email:a@x.example','person','A',1.0,'2026-01-01',1,'{\"live\":1}')")
        db.execute("INSERT INTO graph_links VALUES('email:a@x.example','org:x.example','org',1.0,'2026-01-01')")
        start = n()
        db.execute("UPDATE graph_nodes SET strength=1.0001,signals=5,info='{\"live\":2}'")  # under a thousandth, live, signals
        db.execute("UPDATE graph_links SET strength=2,last_at='2026-02-01'")
        self.assertEqual(n(), start)
        db.execute('UPDATE graph_nodes SET strength=0.9')
        self.assertEqual((n()['graph_scores'], n()['graph_shared']), (start['graph_scores'] + 1, start['graph_shared']))
        db.execute("UPDATE graph_nodes SET info='{\"live\":2,\"role\":\"CFO\"}'")
        db.execute("UPDATE graph_links SET kind='project'")
        self.assertEqual((n()['graph_shared'], n()['links_shared']), (start['graph_shared'] + 1, start['links_shared'] + 1))

    def test_records_that_went_are_written_only_where_they_changed(self):
        import sqlite3
        db = sqlite3.connect(':memory:')
        sg.ensure(db)
        sg.went_records(db, FLEET, {'a': '1', 'b': '2'})
        db.execute("UPDATE share_out SET at='then'")
        sg.went_records(db, FLEET, {'a': '1', 'c': '3'})
        self.assertEqual(sorted(db.execute("SELECT key,hash,at='then' FROM share_out WHERE kind='record'")), [('a', '1', 1), ('c', '3', 0)])


def load_tests(loader, tests, pattern):
    """This file's own tests only: the ones Since inherits run in tests/test_shared_graph.py."""
    return unittest.TestSuite([*(Since(name) for name in loader.getTestCaseNames(Since) if name in vars(Since)),
                               loader.loadTestsFromTestCase(Counters)])


if __name__ == '__main__':
    unittest.main()

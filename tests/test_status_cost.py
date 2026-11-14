"""What the status poll costs: one database connection per request however often it connects (it opened some 40 and the
Fleet tab over 400), each closed when the request ends; the lookups it makes per connection and per to-do served by an
index or asked once; and `openclaw models status` never run while a request waits (it took 20 s on a busy Machine).
Measured on a copy of a busy Machine's database: status 20 s -> under 1 s, 41 connections -> 4."""
import http.client
import json
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
import crm
import models
from machine import timing as request_timing
from seams import patch_everywhere  # noqa: E402
import served  # noqa: E402

NOW = '2026-11-07T12:00:00+00:00'


def event(i):
    return {'account_id': 'work', 'source_id': f'm{i}', 'kind': 'gmail.message', 'occurred_at': NOW, 'title': f'Subject {i}',
            'body': 'Hello', 'metadata': {'from': f'person{i}@client.example', 'thread_id': f't{i}'}, 'deleted': False}


class Opened:
    """Every connection sqlite3.connect opens while it is on, with the statements each ran."""

    def __init__(self, test):
        self.connections, self.statements, real = [], [], sqlite3.connect

        def connect(*args, **kwargs):
            db = real(*args, **kwargs)
            db.set_trace_callback(self.statements.append)
            self.connections.append(db)
            return db
        patcher = patch.object(sqlite3, 'connect', side_effect=connect)
        patcher.start(); test.addCleanup(patcher.stop)

    def closed(self):
        out = []
        for db in self.connections:
            try:
                db.execute('SELECT 1')
                out.append(False)
            except sqlite3.ProgrammingError:  # closed
                out.append(True)
        return out

    def asked(self, text):
        return sum(text in s for s in self.statements)


class StatusCost(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.accounts = [{'id': 'work', 'email': 'owner@example.com', 'boundary': 'work:Example', 'service': 'gmail'}]
        self.addCleanup(setattr, a._REQUEST_TIMING, 'value', None)

    def todos(self, count, start=0):
        self.store.commit_page('work', {}, [event(i) for i in range(start, start + count)])
        with self.store.connect() as db:
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
        for i, event_id in ((i, ids[f'm{i}']) for i in range(start, start + count)):
            self.store.suggest(f'todo-{i}', f'Reply to person {i}', 'Body', [event_id])

    def status(self):
        """store.snapshot as a request answers it: (db_connections, statements, the connections closed at its end)."""
        opened = Opened(self)
        a._REQUEST_TIMING.value = spent = {'db_wait': 0.0, 'db_held': 0.0, 'db_connections': 0}
        with patch_everywhere(a, 'now', return_value=NOW):
            self.store.snapshot(self.accounts)
        a._REQUEST_TIMING.value = None
        request_timing.close_kept(spent)
        return spent['db_connections'], opened

    def test_a_status_request_opens_few_connections_and_closes_them_all_when_it_ends(self):
        self.todos(4)
        connections, opened = self.status()
        self.assertLessEqual(connections, 2)  # was a new connection for nearly every helper: 40 per poll
        self.assertEqual(len(opened.connections), connections)
        self.assertTrue(opened.connections and all(opened.closed()), 'every connection closes when the request ends')

    def test_what_status_asks_per_to_do_does_not_grow_with_lookups_that_find_nothing(self):
        """Each to-do asked for its Change request with none to ask about (request_id=NULL, 254 per poll on a busy
        Machine) and twice whether the bounces table exists (150): never, and once per connection."""
        self.todos(3)
        _, few = self.status()
        self.todos(9, start=3)
        _, many = self.status()
        self.assertEqual(many.asked('FROM feedback_prompts WHERE request_id'), 0)
        self.assertLessEqual(many.asked("name='email_bounces'"), 1)
        self.assertLessEqual(many.asked('PRAGMA secure_delete'), 2)  # the connection setup, not once per helper
        self.assertLessEqual(len(many.statements) - len(few.statements), 30 * 9)  # a bound per to-do; was over 20

    def busy(self, start, count):
        """count more to-dos, each with what the status looks up for it: a cleanup's and a digest's items, a decision
        with its annotation, a preparation, a paused step and a handoff to a teammate (half of them snoozed)."""
        self.todos(count, start)
        with self.store.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS fleet_out(id TEXT PRIMARY KEY,fleet TEXT NOT NULL,member_id TEXT NOT NULL,name TEXT NOT NULL,kind TEXT NOT NULL,"
                       "question TEXT NOT NULL,context TEXT,status TEXT NOT NULL,answer TEXT,at TEXT NOT NULL,answered_at TEXT)")
            db.execute('CREATE TABLE IF NOT EXISTS fleet_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
            for n, (card,) in enumerate(db.execute("SELECT id FROM suggestions WHERE dedupe_key IN (SELECT value FROM json_each(?))",
                                                   (json.dumps([f'todo-{i}' for i in range(start, start + count)]),)).fetchall()):
                db.execute("INSERT INTO mail_cleanup_items(suggestion_id,item,kind,account_id,address,updated_at) VALUES(?,0,'unsubscribe','work','news@list.example',?)", (card, NOW))
                db.execute("INSERT INTO digest_items(suggestion_id,item,event_id,account_id,address,updated_at) VALUES(?,0,NULL,'work','news@list.example',?)", (card, NOW))
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other','Shorter','dashboard',?)", ('d' + card, card, NOW))
                db.execute("INSERT INTO decision_annotations(decision_id,status,reason) VALUES(?,'superseded','newer')", ('d' + card,))
                db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,reason,created_at,updated_at) VALUES(?,?,?,'done','',?,?)",
                           (card, 'd' + card, 'j' + card, NOW, NOW))
                db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,status,payload,approval_id,source,rfc_message_id,created_at,updated_at) "
                           "VALUES(?,?,'r1','paused',?,?,'dashboard','',?,?)", ('a' + card, card, json.dumps({'kind': 'finish', 'label': 'Send it'}), 'ap' + card, NOW, NOW))
                db.execute("INSERT INTO fleet_out(id,fleet,member_id,name,kind,question,context,status,at) VALUES(?,'f','m','Robin Vale','handoff','Book it',?,'asked',?)",
                           ('q' + card, 'handoff:' + card, NOW))
                if n % 2:
                    db.execute("UPDATE suggestions SET status='snoozed' WHERE id=?", (card,))

    def test_what_status_looks_up_per_to_do_is_read_once_for_the_list(self):
        """A cleanup's and a digest's items, decision annotations, a to-do's preparation and stopped step, its handoff,
        and each module's table check (stamps.once) were read once per to-do or decision: 52, 52, 43, 22, 22, 22 and over
        200 reads in a 1,270-statement build. Now once per build, however many to-dos there are."""
        self.busy(0, 3)
        self.status()  # a new database's first: its tables made
        _, few = self.status()
        self.busy(3, 9)
        _, many = self.status()
        for read in ('FROM mail_cleanup_items', 'FROM digest_items', 'FROM decision_annotations WHERE', 'FROM preparations',
                     "FROM action_jobs WHERE suggestion_id=? AND status IN ('paused'", 'FROM fleet_out', 'PRAGMA database_list', 'FROM sqlite_master WHERE name=?'):
            self.assertLessEqual(many.asked(read), few.asked(read), read)
        self.assertGreater(few.asked('FROM fleet_out'), 0)
        self.assertLessEqual(many.asked('PRAGMA schema_version'), few.asked('PRAGMA schema_version') + 9 * 4)  # one a check, not three

    def test_the_lists_reads_show_what_each_to_do_read_on_its_own(self):
        self.busy(0, 4)
        with self.store.connect() as db:
            cards = [dict(r) for r in db.execute("SELECT * FROM suggestions")]
            listed, alone = [dict(c) for c in cards], [dict(c) for c in cards]
            pre = self.store.card_reads(db, listed)
            for one, two in zip(listed, alone):
                with patch_everywhere(a, 'now', return_value=NOW):
                    self.assertEqual(self.store.suggestion_result(one, db, pre), self.store.suggestion_result(two, db))
        self.assertTrue(any(c.get('status') == 'snoozed' for c in cards))

    def test_the_failed_reads_and_signal_counts_come_from_an_index(self):
        """Status asks each connection for its last failed read and its failures today; most never fail, so this walked
        every read of the connection (167,000 for a phone feed, half a second a poll) to find none."""
        with self.store.connect() as db:
            plans = {sql: ' '.join(r[3] for r in db.execute('EXPLAIN QUERY PLAN ' + sql, args)) for sql, args in [
                ("SELECT at,error FROM sync_activity WHERE account_id=? AND status='failed' ORDER BY at DESC,rowid DESC LIMIT 1", ('work',)),
                ("SELECT count(*) FROM sync_activity WHERE account_id=? AND status='failed' AND at>=?", ('work', NOW)),
                ('SELECT count(*) total,sum(analyzed_version<version) pending,sum(ingested_at>=?) signals_24h FROM events WHERE account_id=? AND history=0', (NOW, 'work')),
                ('SELECT count(*) total,sum(analyzed_version<version) pending,sum(analyzed_version=0) first_review,'
                 'coalesce(sum(analyzed_version<version AND deferrals>=?),0) set_aside FROM events WHERE history=0', (3,))]}
        for sql, plan in plans.items():
            self.assertIn('sync_activity_failed' if 'sync_activity' in sql else 'COVERING INDEX events_signal_counts', plan, sql)

    def test_an_organization_named_on_a_to_do_is_found_by_index(self):
        """Each to-do that names its organization looks it up by name (todo_org.card_org): a scan of every Graph node per
        to-do, 10 to 20 ms each on a Graph of 20,000 nodes. An index on the name, not on the kind: one on the kind
        sent queries that join Graph events through it, and the many that read all of one kind, the slow way."""
        with self.store.connect() as db:
            plan = lambda sql, *args: ' '.join(r[3] for r in db.execute('EXPLAIN QUERY PLAN ' + sql, args))
            self.assertIn('INDEX graph_nodes_name', plan("SELECT id FROM graph_nodes WHERE kind='org' AND name=? COLLATE NOCASE LIMIT 2", 'Acme'))
            self.assertNotIn('graph_nodes_name', plan("SELECT id,name,info FROM graph_nodes WHERE kind='org'"))

    def test_status_stays_fast_with_a_long_read_history(self):
        """A timing guard: 200,000 successful reads of one connection (a phone feed's months) and 60 to-dos."""
        self.todos(60)
        with self.store.connect() as db:
            db.executemany("INSERT INTO sync_activity VALUES(?,?,?,'success',1,NULL,NULL)",
                           ((f'r{i}', 'work', f'2026-{1 + i % 10:02d}-01T00:00:{i % 60:02d}+00:00') for i in range(200000)))
        started = time.perf_counter()
        connections, _ = self.status()
        self.assertLess(time.perf_counter() - started, 3.0)  # about 0.2 s here; the failed-read scans alone took 0.5 s on 340,000 reads
        self.assertLessEqual(connections, 2)

    def test_a_connection_inside_another_ones_block_is_its_own_and_both_go_back(self):
        a._REQUEST_TIMING.value = spent = {'db_wait': 0.0, 'db_held': 0.0, 'db_connections': 0}
        with self.store.connect() as outer:
            outer.execute('CREATE TABLE IF NOT EXISTS t(x)')
            outer.execute('INSERT INTO t VALUES(1)')
            with self.store.connect() as inner:
                self.assertIsNot(inner, outer)
        for _ in range(20):
            with self.store.connect() as db:
                self.assertEqual(db.execute('SELECT count(*) FROM t').fetchone()[0], 1)  # committed when the block ended
        with self.assertRaises(ValueError):
            with self.store.connect() as db:
                db.execute('INSERT INTO t VALUES(2)')
                raise ValueError('rolled back')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM t').fetchone()[0], 1)
            db.isolation_level = None  # as graph_build sets it: the next connect gets the usual one back
        with self.store.connect() as db:
            self.assertEqual(db.isolation_level, '')
        self.assertEqual(spent['db_connections'], 2)
        kept = [db for dbs in spent['kept'].values() for db in dbs]
        request_timing.close_kept(spent)
        self.assertEqual(len(kept), 2)
        for db in kept:
            with self.assertRaises(sqlite3.ProgrammingError):
                db.execute('SELECT 1')

    def test_org_aliases_are_read_once_per_connection_until_it_changes_them(self):
        with self.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS org_aliases(alias TEXT PRIMARY KEY,target TEXT NOT NULL,undo TEXT,created_at TEXT)')
            seen = []
            db.set_trace_callback(seen.append)
            for _ in range(50):
                self.assertEqual(crm.canonical(db, 'org:a.example'), 'org:a.example')
            db.execute("INSERT INTO org_aliases VALUES('org:a.example','org:b.example','{}',?)", (NOW,))
            self.assertEqual(crm.canonical(db, 'org:a.example'), 'org:b.example')
            db.set_trace_callback(None)
        self.assertEqual(sum('FROM org_aliases' in s for s in seen), 2)


class RequestsCloseTheirConnections(unittest.TestCase):
    """Through the dashboard server: a request that connects many times opens one connection and closes it at its end."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = a.Store(Path(self.temp.name) / 's.sqlite'), 'test-token', threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}

    def serve(self):
        return served.serve(self, a)

    def test_one_connection_per_request_closed_at_its_end(self):
        port = self.serve()
        opened = Opened(self)
        mine = []

        def many(*_args, **_kwargs):
            before = len(opened.connections)
            for _ in range(25):
                with self.app.store.connect() as db:
                    db.execute('SELECT 1').fetchone()
            mine.extend(opened.connections[before:])
            return {'ok': True}
        with patch_everywhere(a, 'SLOW_REQUEST_SECONDS', 0.0), patch.object(a.App, 'action', side_effect=many), \
                self.assertLogs(a.LOG, 'WARNING') as logged:
            for _ in range(2):
                conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
                conn.request('POST', '/api/action', body=json.dumps({'action': 'status', 'args': {}}),
                             headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test-token'})
                response = conn.getresponse(); response.read(); conn.close()
                self.assertEqual(response.status, 200)
            deadline = time.monotonic() + 5
            while len([l for l in logged.output if 'slow request' in l]) < 2 and time.monotonic() < deadline:
                time.sleep(0.01)
        lines = [l for l in logged.output if 'slow request' in l]
        self.assertEqual([int(l.split('db_connections=')[1]) for l in lines], [1, 1])  # was 25 each
        self.assertEqual(len(mine), 2)
        for db in mine:
            with self.assertRaises(sqlite3.ProgrammingError, msg='no connection outlives its request'):
                db.execute('SELECT 1')


class ModelReadyNeverWaits(unittest.TestCase):
    """`openclaw models status` starts a node process (20 s or more on a busy Machine): the status poll used to run it
    in the request every time its reading expired, so a status answer took 20 s every ten minutes."""

    def setUp(self):
        models._model_ready.clear(); self.addCleanup(models._model_ready.clear)
        patcher = patch.object(models, 'main_model', return_value='openai/gpt-6-astra')
        patcher.start(); self.addCleanup(patcher.stop)

    def test_the_poll_gets_the_last_reading_while_one_background_read_runs(self):
        release, calls = threading.Event(), []
        out = json.dumps({'fallbacks': [], 'auth': {'missingProvidersInUse': []}})

        def run(args, **kwargs):
            calls.append(args)
            release.wait(5)
            return type('R', (), {'stdout': out, 'returncode': 0})()
        started = time.perf_counter()
        self.assertIsNone(models.model_ready({}, run, wait=False))  # nothing read yet: unknown, never a wait
        self.assertIsNone(models.model_ready({}, run, wait=False))
        self.assertLess(time.perf_counter() - started, 1)
        release.set()
        deadline = time.monotonic() + 5
        while not models._model_ready and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertEqual(len(calls), 1)  # one read at a time
        self.assertTrue(models.model_ready({}, run, wait=False))
        # expired: the last reading at once, and a fresh read behind it
        models._model_ready['openai/gpt-6-astra'] = (time.monotonic() - 1, True)
        release.clear()
        self.assertTrue(models.model_ready({}, run, wait=False))
        release.set()
        deadline = time.monotonic() + 5
        while models._model_reading and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertEqual(len(calls), 2)

    def test_needs_you_asks_without_waiting(self):
        with patch_everywhere(a, 'model_ready', return_value=None) as ready, patch_everywhere(a, 'main_model', return_value='openai/gpt-6-astra'):
            a.needs_you({'accounts': []})
        self.assertIs(ready.call_args.kwargs.get('wait'), False)


if __name__ == '__main__':
    unittest.main()

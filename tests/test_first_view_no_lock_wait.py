"""A dashboard's first view never waits for the write lock. On a new Machine the first import takes in page after page
and the Machine joins its Network meanwhile: the page stayed blank for half a minute, as its first calls each made
tables, counted the visit, marked the first view and made a new table's guards, every one a write that queued behind
the import. Measured on a sealed sandbox install with another connection holding the write lock for 8 s: the first
view complete after 8.7 s -> 0.3 s."""
import http.client
import secrets
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
from machine import timing as request_timing

OWNER = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com'}
FIRST_VIEW = ('/', '/api/status', '/api/session', '/api/reviews/live', '/api/browser-now')  # what a page asks for at once
BOUND = 3.0  # seconds: far under the 20 a write waits for the lock, far over what a read takes


def event(i):
    return {'account_id': 'work', 'source_id': f'm{i}', 'kind': 'gmail.message', 'occurred_at': a.now(), 'title': f'Subject {i}',
            'body': 'Hello', 'metadata': {'from': f'Sam Person <sam{i}@client.example>', 'thread_id': f't{i}'}, 'deleted': False}


class FirstViewNoLockWait(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        credentials = {}
        for name in ('api-token', 'owner-token'):
            (Path(self.temp.name) / name).write_text(secrets.token_hex(24))
            credentials[name] = str(Path(self.temp.name) / name)
        config = {'database': str(self.path), 'accounts': [{'id': 'work', 'email': 'owner@example.com', 'boundary': 'work:Example', 'service': 'gmail'}],
                  'owner_name': 'Alex Example', 'timezone': 'Europe/Brussels', 'telegram_owner': '', 'tailscale_owner': 'owner@example.com',
                  'dashboard_host': 'machine.example:8443', 'dashboard_path': '/', 'dashboard_aliases': [], 'port': 0, 'http_timeout': 1,
                  'app_dir': str(Path(a.__file__).parent), 'openclaw': '/nonexistent/openclaw', 'node': '/nonexistent/node',
                  'gog': '/nonexistent/gog', 'wacli': '/nonexistent/wacli', 'openclaw_state': str(Path(self.temp.name) / 'openclaw.sqlite'),
                  'agent_db': str(Path(self.temp.name) / 'agent.sqlite'), 'delivery_enabled': False, 'digest_at': '08:30', 'bootstrap_days': 7,
                  'poll_seconds': 300, 'credentials': credentials, 'embeddings': {'enabled': False}, 'enrichment': {'enabled': False},
                  'browser_cdp_url': 'http://127.0.0.1:9'}
        self.app = a.App(config)
        self.assertTrue(self.app.store.protected)  # as every Machine: message contents sealed
        self.app.store.commit_page('work', {}, [event(i) for i in range(3)])
        with self.app.store.connect() as db:
            ids = [r['id'] for r in db.execute('SELECT id FROM events ORDER BY id')]
        self.app.store.suggest('todo-1', 'Reply to Sam', 'Body', ids[:1])  # a to-do to show, greet with and count
        self.assertTrue(request_timing.aside_settled())
        self.addCleanup(request_timing.aside_settled)

    def serve(self):
        servers, real = [], a.http.server.ThreadingHTTPServer
        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs)); return servers[-1]
        workers = [name for name in dir(a.App) if name.endswith('_worker') or name in ('collector', 'ability_checker', 'gbrain_start', 'meeting_write_resume')]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture), patch.object(a.signal, 'signal'),
                        *(patch.object(a.App, name) for name in workers)):
            patcher.start(); self.addCleanup(patcher.stop)
        thread = threading.Thread(target=self.app.serve, daemon=True); thread.start()
        while not servers:
            time.sleep(0.01)
        self.addCleanup(lambda: (self.app.stop.set(), thread.join(5)))
        port = servers[0].server_address[1]
        self.view(port, ('/healthz',))  # answered once the start's own writes are done and it serves
        return port

    def hold(self, seconds=30):
        """Another connection takes the write lock, as an import's page does, and keeps it until the test ends."""
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None, check_same_thread=False)
        db.execute('BEGIN IMMEDIATE')
        db.execute("INSERT OR REPLACE INTO checkpoints(account_id,state) VALUES('held','{}')")
        release = threading.Timer(seconds, db.rollback); release.start()  # never left held, whatever the test does
        self.addCleanup(lambda: (release.cancel(), db.rollback(), db.close()))
        return db

    def view(self, port, paths=FIRST_VIEW):
        """{path: (status, seconds)} of the first view's calls, asked at once as a page does."""
        out = {}
        def get(path):
            started = time.monotonic()
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=60)
            conn.request('GET', path, headers=OWNER)
            response = conn.getresponse(); response.read(); conn.close()
            out[path] = (response.status, time.monotonic() - started)
        threads = [threading.Thread(target=get, args=(path,)) for path in paths]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return out

    def assert_answered(self, answers):
        for path, (status, seconds) in answers.items():
            self.assertEqual(status, 200, path)
            self.assertLess(seconds, BOUND, f'{path} waited {seconds:.1f}s for the write lock')

    def schema(self):
        with sqlite3.connect(self.path) as db:
            return db.execute('PRAGMA schema_version').fetchone()[0]

    def test_a_new_machines_first_view_answers_while_a_writer_holds_the_database(self):
        port, before = self.serve(), self.schema()
        held = self.hold()
        self.assert_answered(self.view(port))
        self.assertEqual(self.schema(), before, 'the first view made a table: make it when the Store opens (StoreCore.__init__)')
        held.rollback()  # the import's page is in: what the view left for later is written now
        self.assertTrue(request_timing.aside_settled())
        with self.app.store.connect() as db:
            marks = {r['name'] for r in db.execute('SELECT name FROM milestones')}
            counted = {r['kind'] for r in db.execute('SELECT kind FROM activity_seen')}
        self.assertLessEqual({'greeting', 'tips', 'first_card_shown'}, marks)
        self.assertLessEqual({'visits', 'shown', 'active_hours'}, counted)

    def test_a_first_views_mark_is_the_one_it_answered_with(self):
        port = self.serve()
        held = self.hold()
        first = self.view(port, ('/api/status',))
        self.assert_answered(first)
        held.rollback()
        self.assertTrue(request_timing.aside_settled())
        with self.app.store.connect() as db:
            at = db.execute("SELECT at FROM milestones WHERE name='greeting'").fetchone()['at']
        self.view(port, ('/api/status',))  # a later view finds the mark and makes no second one
        self.assertTrue(request_timing.aside_settled())
        with self.app.store.connect() as db:
            self.assertEqual([r['at'] for r in db.execute("SELECT at FROM milestones WHERE name='greeting'")], [at])

    def test_a_sealed_table_made_meanwhile_gets_its_guards_without_holding_a_page(self):
        port = self.serve()
        with sqlite3.connect(self.path) as db:  # as joining the Network does while the first import runs (network.py)
            db.execute('CREATE TABLE network_replies(ask_id TEXT PRIMARY KEY,body TEXT NOT NULL,at TEXT NOT NULL)')
        held = self.hold()
        self.assert_answered(self.view(port))  # each waited here to make the guards, and all but one then failed
        held.rollback()
        self.assertTrue(request_timing.aside_settled())
        with self.app.store.connect() as db:
            guards = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name='network_replies'")}
        self.assertEqual(guards, {'mc_network_replies_body_insert', 'mc_network_replies_body_update'})

    def test_threads_that_make_the_same_guard_at_once_all_go_on(self):
        with sqlite3.connect(self.path) as db:
            db.execute('CREATE TABLE network_replies(ask_id TEXT PRIMARY KEY,body TEXT NOT NULL,at TEXT NOT NULL)')
        held, failed = self.hold(), []
        def connect():
            try:
                with self.app.store.connect() as db:
                    db.execute('SELECT 1').fetchone()
            except sqlite3.Error as error:
                failed.append(error)
        threads = [threading.Thread(target=connect) for _ in range(4)]
        for thread in threads:
            thread.start()
        time.sleep(0.3)  # all four wait for the write lock to make the guard
        held.rollback()
        for thread in threads:
            thread.join(30)
        self.assertEqual(failed, [])

    def test_outside_a_request_the_writes_are_made_at_once(self):
        self.assertIsNone(getattr(request_timing._REQUEST_TIMING, 'value', None))
        self.app.store.greeting('Alex Example')
        self.app.store.note_activity('visit')
        with self.app.store.connect() as db:
            self.assertTrue(db.execute("SELECT 1 FROM milestones WHERE name='greeting'").fetchone())
            self.assertTrue(db.execute("SELECT 1 FROM activity_seen WHERE kind='visits'").fetchone())

    def test_a_failing_write_on_the_side_is_logged_and_the_next_one_is_made(self):
        made = []
        request_timing._REQUEST_TIMING.value = {'db_wait': 0.0, 'db_held': 0.0, 'db_connections': 0}
        self.addCleanup(setattr, request_timing._REQUEST_TIMING, 'value', None)
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            request_timing.aside(lambda: 1 / 0, 'a count')
            request_timing.aside(lambda: made.append(threading.current_thread().name), 'a mark')
            self.assertTrue(request_timing.aside_settled())
        self.assertEqual(made, ['aside-writes'])
        self.assertTrue(any('what=a count error=ZeroDivisionError' in line for line in logged.output))


if __name__ == '__main__':
    unittest.main()

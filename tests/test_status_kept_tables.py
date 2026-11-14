"""The kept status is kept by the change counters of the tables it reads (StatusApp.status_mark), not by every commit:
meaning search, graph runs and the Network write all day, and each of their commits threw it away. It never stays as it
was: a change to any table a build reads builds it again, a sync round makes the connections' cards again (and only
those), and what it reads outside the database (preparations held back, USER.md, the disconnect receipts) is part of it."""
import contextlib
import gc
import json
import re
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

import assistant as a
from machine import stamps
from machine.store import views
from test_status_kept import NOW, WORK, mail

LATER = '2099-01-01T00:00:00+00:00'


def touch(path, table):
    """The table's last row written again by another connection (a worker), or in an empty table a row with its required
    columns made up added and removed again in one commit (its counters change, its rows don't). False when neither
    could be done."""
    with contextlib.closing(sqlite3.connect(path)) as db, db:
        columns = db.execute(f'PRAGMA table_info({table})').fetchall()
        try:
            if db.execute(f'UPDATE {table} SET {columns[0][1]}={columns[0][1]} WHERE rowid=(SELECT max(rowid) FROM {table})').rowcount > 0:
                return True
        except sqlite3.Error:
            pass
        values = {name: ((1 if pk else uuid.uuid4().int % 10**9) if 'INT' in (kind or '').upper() or 'REAL' in (kind or '').upper() else uuid.uuid4().hex)
                  for _, name, kind, notnull, default, pk in columns if (notnull and default is None) or pk}
        try:
            added = db.execute(f'INSERT INTO {table}({",".join(values)}) VALUES({",".join("?" * len(values))})' if values else
                               f'INSERT INTO {table} DEFAULT VALUES', list(values.values())).lastrowid
            db.execute(f'DELETE FROM {table} WHERE ' + ' AND '.join(f'{k}=?' for k in values), list(values.values())) if values else \
                db.execute(f'DELETE FROM {table} WHERE rowid=?', (added,))
            return True
        except sqlite3.Error:
            return False


def write(path, *statements):
    """Statements committed by another connection (a worker, a sync round)."""
    with contextlib.closing(sqlite3.connect(path)) as db, db:
        for sql, args in statements:
            db.execute(sql, args)


class StatusKeptByTable(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.config_path, self.app.config = self.store, None, {'accounts': [WORK]}
        self.builds, built = [], self.app.status_built

        def counted(done):
            self.builds.append(done)
            return built(done)
        self.app.status_built = counted
        self.addCleanup(lambda: (self.app.__dict__.get('_status_kept') or {}).get('watch') and self.app._status_kept['watch'].close())
        # some to-dos with their messages and a decision: more of what the status reads
        self.store.commit_page('work', {}, [mail(1), mail(2)])
        with self.store.connect() as db:
            ids = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id')]
        card = self.store.suggest('k1', 'Answer Sam', 'Sam asked.', ids[:1])['id']
        self.store.suggest('k2', 'Book the room', 'A room.', ids[1:])
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1',?,'other','Shorter','dashboard',?)",
                       (card, NOW.isoformat()))
        self.status(); self.status(); self.builds.clear()  # a new database's first build makes its tables: one more build

    def status(self):
        return self.app.action('status', {'full': True, 'done': 25})

    def cards_made(self):
        made, real = [], self.app.status_connectors

        def counted():
            made.append(1)
            return real()
        self.app.status_connectors = counted
        return made

    def read_by_a_build(self, **patches):
        """The tables a full build reads, with what the status keeps inside it (stamps.Kept) emptied first."""
        for kept in [o for o in gc.get_objects() if isinstance(o, stamps.Kept)]:
            kept.clear()
        read, real = set(), sqlite3.connect

        def connect(*args, **kwargs):
            db = real(*args, **kwargs)
            db.set_trace_callback(lambda sql: read.update(t.lower() for t in re.findall(r'\b(?:FROM|JOIN)\s+([A-Za-z_]\w*)', sql)))
            return db
        with patch.object(sqlite3, 'connect', side_effect=connect), patch.multiple(self.app, **patches) if patches else contextlib.nullcontext():
            self.app.status_built(25)
        return read - {'sqlite_master', 'data_stamps', 'json_each', 'json_tree', 'pragma_table_info'}

    def test_it_reads_no_quiet_table_and_only_the_cards_read_what_a_sync_round_writes(self):
        read = self.read_by_a_build()
        with contextlib.closing(sqlite3.connect(self.store.path)) as db:
            counted = set(views.status_tables(db))
        self.assertIn('suggestions', read)
        self.assertEqual(read - counted, set(), 'a table the status reads without its counter: the status would stay as it was')
        self.assertEqual(read & set(views.STATUS_QUIET), set())
        self.assertTrue(read & set(views.SYNC_TABLES))  # the cards
        rest = self.read_by_a_build(status_connectors=lambda: [])
        self.assertEqual(rest & set(views.SYNC_TABLES), set(), 'kept by the rest of the status while a sync round changes it')

    def test_a_change_to_any_table_it_reads_builds_it_again(self):
        """Each table a build reads, changed by another process (a worker): what the status is kept by changes, so it is
        built again, or for those a sync round writes, the connections' cards are made again, never kept as they were."""
        read, missed = sorted(self.read_by_a_build()), []
        self.status()
        kept = self.app._status_kept
        with patch('machine.app.status.now', return_value=NOW.isoformat()), kept['lock']:  # the minute stands still
            for table in read:
                rest, cards = self.app.status_mark(25, kept)
                changed = touch(self.store.path, table)
                after_rest, after_cards = self.app.status_mark(25, kept)
                if not changed:
                    missed.append(f'{table}: could not write a row to check it')
                elif table in views.SYNC_TABLES and (after_cards == cards or after_rest != rest):
                    missed.append(f'{table}: the cards were kept, or the rest built again')
                elif table not in views.SYNC_TABLES and after_rest == rest:
                    missed.append(f'{table}: kept')
        self.assertEqual(missed, [])
        self.status(); self.builds.clear()  # end to end: one of them changed, the status is built again
        touch(self.store.path, 'suggestions')
        self.status(); self.assertEqual(len(self.builds), 1)

    def test_a_sync_round_makes_only_the_connection_cards_again(self):
        made = self.cards_made()
        first = self.status()
        write(self.store.path, ("INSERT INTO sync_activity VALUES('r1','work',?,'success',0,NULL,NULL)", (LATER,)),  # a sync round with
              ("UPDATE checkpoints SET last_success=? WHERE account_id='work'", (LATER,)))  # nothing new, as Store.commit_page writes it
        after = self.status()
        self.assertEqual((self.builds, len(made)), ([], 1))
        self.assertEqual(after['suggestions'], first['suggestions'])
        self.assertEqual((after['connectors'][0]['sync_activity'][0]['at'], after['connectors'][0]['last_success']), (LATER, LATER))
        self.assertNotEqual(first['connectors'][0]['last_success'], LATER)
        self.assertEqual(self.status(), after)
        self.assertEqual((self.builds, len(made)), ([], 1))

    def test_a_write_it_never_reads_keeps_it(self):
        made = self.cards_made()
        with self.store.connect() as db:
            event = db.execute('SELECT id FROM events LIMIT 1').fetchone()[0]
        write(self.store.path, ("INSERT INTO event_vectors VALUES(?,1,'m',4,?,NULL)", (event, b'\0' * 16)))  # meaning search, in the background
        self.status()
        self.assertEqual((self.builds, made), ([], []))

    def test_a_page_load_keeps_it_and_opening_a_to_do_builds_it_again(self):
        """activity_seen: the page's own load (a visit) and the list's poll (to-dos shown, the active hour) are never read
        by the status and keep it; an open of a to-do is (Still needed?) and builds it again."""
        self.store.note_activity('visit')  # activity_seen is made: the status is kept by its opens from here on
        with patch('machine.app.status.now', return_value=NOW.isoformat()):  # the minute stands still
            self.status(); self.status(); self.builds.clear()
            self.store.note_activity('visit')
            self.store._activity_at = 0
            self.store.note_activity('dashboard')
            self.status()
            self.assertEqual(self.builds, [])
            with self.store.connect() as db:
                card = db.execute('SELECT id FROM suggestions LIMIT 1').fetchone()[0]
            self.store.note_activity('opened', card)
            self.status()
            self.assertEqual(len(self.builds), 1)
            self.store.note_activity('opened', card)  # the same open again that day: nothing new
            self.status()
            self.assertEqual(len(self.builds), 1)

    def test_what_it_reads_outside_the_database_builds_it_again(self):
        """Preparations held back in memory, USER.md (Learning's "You corrected …") and the disconnect receipts."""
        self.app.config['openclaw_workspace'] = self.temp.name
        self.app.config['database'] = str(self.store.path)
        self.store.config = self.app.config  # one config, as main.py sets it
        self.status(); self.builds.clear()
        self.store.preparation_holds = {'reason': 'limit'}
        self.status(); self.assertEqual(len(self.builds), 1)
        user_md = self.app.user_md()
        user_md.parent.mkdir(parents=True, exist_ok=True)
        user_md.write_text('# USER.md\n- Name: Pat Doe\n')
        self.status(); self.assertEqual(len(self.builds), 2)
        import mail_grants
        mail_grants._receipts_path(self.app.config).write_text(json.dumps([{'provider': 'google', 'email': 'old@acme.example',
                                                                              'at': NOW.isoformat(), 'state': 'removed'}]))
        out = self.status()
        self.assertEqual(len(self.builds), 3)
        self.assertEqual([r['card_title'] for r in out['disconnected']], ['old@acme.example'])
        self.status(); self.assertEqual(len(self.builds), 3)

    def test_without_the_counters_it_is_kept_by_any_commit_as_before(self):
        with patch.object(self.app, 'watch_status_tables'):
            write(self.store.path, ('DROP TRIGGER stamp_suggestions_delete', ()))
            self.status(); self.builds.clear()
            write(self.store.path, ("INSERT INTO sync_activity VALUES('r2','work',?,'success',0,NULL,NULL)", (NOW.isoformat(),)))
            self.status(); self.assertEqual(len(self.builds), 1)
            self.status(); self.assertEqual(len(self.builds), 1)


if __name__ == '__main__':
    unittest.main()

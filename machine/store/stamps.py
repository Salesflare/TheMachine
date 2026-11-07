"""Change counters per table, so what a request works out from a few tables can be kept between requests and worked out
again only once one of them changed (Kept, below).

data_stamps holds one counter per watched table; triggers add one on each insert, update and delete, in the same
transaction as the change, so a kept answer is never older than a committed change. The triggers are made by an
ensure (watch, from Store, graph.ensure or shared_graph.ensure), never on a request's read path; a table without its
triggers has no stamp, and what reads it is worked out each time, as before."""
import collections
import os
import re
import sqlite3
import threading

IDENTIFIER = re.compile(r'[a-z][a-z0-9_]{0,62}')


def watch(db, tables):
    """The triggers for these tables (those that exist), once."""
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'stamp\\_%' ESCAPE '\\'")}
    for table in tables:
        if table not in have:
            continue
        db.execute('INSERT OR IGNORE INTO data_stamps(name,n) VALUES(?,0)', (table,))
        for op in ('insert', 'update', 'delete'):
            if f'stamp_{table}_{op}' not in made:
                db.execute(_trigger_sql(table, op))


def _trigger_sql(table, op):
    """The counter trigger for one of the module's own table names (a plain identifier that exists, checked: never a
    value from a request)."""
    if not IDENTIFIER.fullmatch(table) or op not in ('insert', 'update', 'delete'):
        raise ValueError('not a table name')
    return (f"CREATE TRIGGER stamp_{table}_{op} AFTER {op.upper()} ON {table} BEGIN "
            f"UPDATE data_stamps SET n=n+1 WHERE name='{table}'; END")


def stamp(db, tables):
    """A value that changes with every committed change to any of these tables, or None when one of them is not watched
    or the connection is in a transaction (then nothing is kept). The database file is part of it, so two databases
    never share a kept answer."""
    tables = tuple(sorted(set(tables)))
    if db.in_transaction:  # its own changes not committed yet (they could still roll back): nothing kept from them
        return None
    try:
        rows = dict(db.execute('SELECT name,n FROM data_stamps WHERE name IN (SELECT value FROM json_each(?))',
                               ('[' + ','.join('"' + t + '"' for t in tables) + ']',)).fetchall())
        made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'stamp\\_%\\_delete' ESCAPE '\\'")}
        path = next((r[2] for r in db.execute('PRAGMA database_list') if r[1] == 'main'), '')
    except sqlite3.Error:
        return None
    if not path or any(t not in rows or f'stamp_{t}_delete' not in made for t in tables):
        return None
    return (path, tuple(rows[t] for t in tables))


class Kept:
    """A few answers kept by key, each with the stamp it was worked out at: get() gives it back while the stamp is the
    same. The newest `size` keys are kept. Shared by threads; a value is handed out as is, so callers must not change it."""

    def __init__(self, size=8):
        self.size, self.lock, self.items = size, threading.Lock(), collections.OrderedDict()

    def get(self, key, at, make):
        """The value kept for key at stamp `at`, else make() (kept when `at` is not None)."""
        if at is None:
            return make()
        with self.lock:
            hit = self.items.get(key)
            if hit and hit[0] == at:
                self.items.move_to_end(key)
                return hit[1]
        value = make()
        with self.lock:
            self.items[key] = (at, value)
            self.items.move_to_end(key)
            while len(self.items) > self.size:
                self.items.popitem(last=False)
        return value

    def clear(self):
        with self.lock:
            self.items.clear()


_MADE = set()  # (name, database file, its inode, schema version) that once() made current


def _schema_key(db):
    try:
        path = next((r[2] for r in db.execute('PRAGMA database_list') if r[1] == 'main'), '')
        if not path:
            return None
        return (path, os.stat(path).st_ino, db.execute('PRAGMA schema_version').fetchone()[0])
    except (sqlite3.Error, OSError):
        return None


def once(db, name, make, sentinel):
    """make(db) (a module's CREATE ... IF NOT EXISTS and its column checks) once per database and schema version, not on
    each of the dozens of calls a request makes: again when the schema changed since or the sentinel (a table make
    creates) is missing, as in a new database at the same path."""
    key = _schema_key(db)
    if key is not None and (name, *key) in _MADE and db.execute(
            "SELECT 1 FROM sqlite_master WHERE name=?", (sentinel,)).fetchone():
        return
    make(db)
    key = _schema_key(db)  # its tables and triggers changed the schema version
    if key is not None:
        _MADE.add((name, *key))

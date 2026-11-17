"""Change counters per table, so what a request works out from a few tables can be kept between requests and worked out
again only once one of them changed (Kept, below).

data_stamps holds one counter per watched table; triggers add one on each insert, update and delete, in the same
transaction as the change, so a kept answer is never older than a committed change. The triggers are made by an
ensure (watch, from Store, graph.ensure or shared_graph.ensure), never on a request's read path; a table without its
triggers has no stamp, and what reads it is worked out each time, as before."""
import collections
import datetime
import os
import re
import sqlite3
import threading
import timeutil

LAYER = 0  # change counters per table, so a request's answer is kept until its tables change

IDENTIFIER = re.compile(r'[a-z][a-z0-9_]{0,62}')


def watch(db, tables):
    """The triggers for these tables (those that exist), once."""
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'stamp\\_%' ESCAPE '\\'")}
    for table in dict.fromkeys(tables):  # each once, also when two modules' lists share one
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
        raise ValueError(table)  # one of the module's own names, never shown
    return (f"CREATE TRIGGER stamp_{table}_{op} AFTER {op.upper()} ON {table} BEGIN "
            f"UPDATE data_stamps SET n=n+1 WHERE name='{table}'; END")


# graph_who: graph_nodes as the sharing rules read it, who each person and organization is (id, kind, name and info
# without 'profile' and 'live'). A graph build rewrites those two and every person's strength each few minutes (some 30k
# changes an hour on a big graph), so what is kept by graph_nodes' own stamp (a person page's sharing rules and team
# graph: a second's work) was worked out again on nearly every request. Read by stamp(db, ('graph_who',)), like a table.
GRAPH_WHO = (
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_who_insert AFTER INSERT ON graph_nodes BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_who'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_who_update AFTER UPDATE ON graph_nodes WHEN old.id IS NOT new.id "
    "OR old.kind IS NOT new.kind OR old.name IS NOT new.name "
    "OR (CASE WHEN json_valid(old.info) THEN json_remove(old.info,'$.profile','$.live') ELSE old.info END) IS NOT "
    "(CASE WHEN json_valid(new.info) THEN json_remove(new.info,'$.profile','$.live') ELSE new.info END) BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_who'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_who_delete AFTER DELETE ON graph_nodes BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_who'; END",
)


def watch_graph_who(db):
    """graph_who's counter and triggers (when graph_nodes exists), once."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='graph_nodes'").fetchone():
        return
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    db.execute("INSERT OR IGNORE INTO data_stamps(name,n) VALUES('graph_who',0)")
    for sql in GRAPH_WHO:
        db.execute(sql)


# graph_shared: graph_nodes as the Team Graph's publish reads it (shared_graph.collect), but for the score: who each
# person, organization and project is (id, kind, name, info without 'live') and its last contact (last_at). A graph build
# rewrites every person's strength, signals and live each few minutes, so graph_nodes' own counter moved every round and
# the publish read everything again. Read by stamp(db, ('graph_shared',)).
GRAPH_SHARED = (
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_shared_insert AFTER INSERT ON graph_nodes BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_shared_update AFTER UPDATE ON graph_nodes WHEN old.id IS NOT new.id "
    "OR old.kind IS NOT new.kind OR old.name IS NOT new.name OR old.last_at IS NOT new.last_at "
    "OR (CASE WHEN json_valid(old.info) THEN json_remove(old.info,'$.live') ELSE old.info END) IS NOT "
    "(CASE WHEN json_valid(new.info) THEN json_remove(new.info,'$.live') ELSE new.info END) BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_shared_delete AFTER DELETE ON graph_nodes BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_shared'; END",
)
# graph_scores: the same rows' strength to three decimals alone, the score a shared record carries. It fades with time,
# so some move on every build: the publish then puts the new scores on the records it has (shared_graph.rescored).
GRAPH_SCORES = (
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_scores_update AFTER UPDATE ON graph_nodes WHEN "
    "round(old.strength,3) IS NOT round(new.strength,3) BEGIN UPDATE data_stamps SET n=n+1 WHERE name='graph_scores'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_graph_scores_delete AFTER DELETE ON graph_nodes BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='graph_scores'; END",
)


# links_shared: graph_links as that publish reads it, which links there are (a, b, kind), not their strength or last
# contact, which a graph build rewrites on thousands of links an hour (graph_publish changes them in place, so the
# trigger can compare).
LINKS_SHARED = (
    "CREATE TRIGGER IF NOT EXISTS stamp_links_shared_insert AFTER INSERT ON graph_links BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='links_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_links_shared_update AFTER UPDATE ON graph_links WHEN old.a IS NOT new.a "
    "OR old.b IS NOT new.b OR old.kind IS NOT new.kind BEGIN UPDATE data_stamps SET n=n+1 WHERE name='links_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_links_shared_delete AFTER DELETE ON graph_links BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='links_shared'; END",
)


def watch_graph_shared(db):
    """graph_shared's, graph_scores' and links_shared's counters and triggers (for the tables there are), once."""
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    # only on tables with every column a trigger compares (a test's or an old database's smaller graph_nodes has none:
    # then stamp() gives None, and the publish reads every round)
    needs = {'graph_nodes': {'id', 'kind', 'name', 'last_at', 'info', 'strength'}, 'graph_links': {'a', 'b', 'kind'}}
    have = {t for t in needs if needs[t] <= {r[1] for r in db.execute(f'PRAGMA table_info({t})')}}
    for table, name, triggers in (('graph_nodes', 'graph_shared', GRAPH_SHARED), ('graph_nodes', 'graph_scores', GRAPH_SCORES),
                                  ('graph_links', 'links_shared', LINKS_SHARED)):
        if table in have:
            db.execute('INSERT OR IGNORE INTO data_stamps(name,n) VALUES(?,0)', (name,))
            for sql in triggers:
                db.execute(sql)


# events_shared: events as the Shared Graph's What's shared reads them (shared_graph_kept.overview): a message in, out, or
# changed in what it shows (its account, kind, time, title, body, metadata, or deleted or history). Not counted: the
# review's own bookkeeping on each message (analyzed_version, deferrals), which changes all the time and is never read there.
EVENTS_SHARED = (
    "CREATE TRIGGER IF NOT EXISTS stamp_events_shared_insert AFTER INSERT ON events BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='events_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_events_shared_update AFTER UPDATE OF id,account_id,kind,occurred_at,title,body,metadata,"
    "deleted,history ON events BEGIN UPDATE data_stamps SET n=n+1 WHERE name='events_shared'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_events_shared_delete AFTER DELETE ON events BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='events_shared'; END",
)


def watch_events_shared(db):
    """events_shared's counter and triggers (when events exists), once."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='events'").fetchone():
        return
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    db.execute("INSERT OR IGNORE INTO data_stamps(name,n) VALUES('events_shared',0)")
    for sql in EVENTS_SHARED:
        db.execute(sql)


# activity_opened: activity_seen as the status reads it, the owner's opens of a to-do (still_needed.last_touch). The
# rest of activity_seen (a page visit, the to-dos shown, the active hour) is written by the page's own load and poll and
# never read by the status, so each load made the next status build again in full.
ACTIVITY_OPENED = (
    "CREATE TRIGGER IF NOT EXISTS stamp_activity_opened_insert AFTER INSERT ON activity_seen WHEN new.kind='opened' BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='activity_opened'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_activity_opened_update AFTER UPDATE ON activity_seen WHEN old.kind='opened' "
    "OR new.kind='opened' BEGIN UPDATE data_stamps SET n=n+1 WHERE name='activity_opened'; END",
    "CREATE TRIGGER IF NOT EXISTS stamp_activity_opened_delete AFTER DELETE ON activity_seen WHEN old.kind='opened' BEGIN "
    "UPDATE data_stamps SET n=n+1 WHERE name='activity_opened'; END",
)


def watch_activity_opened(db):
    """activity_opened's counter and triggers (when activity_seen exists), once."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='activity_seen'").fetchone():
        return
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    db.execute("INSERT OR IGNORE INTO data_stamps(name,n) VALUES('activity_opened',0)")
    for sql in ACTIVITY_OPENED:
        db.execute(sql)


# fleet_view: one counter for what the Fleet's view (fleet.Fleet.view, shared_view: api/fleet) reads, the fleet_ and
# network_ tables. The dashboard fetches api/fleet for the Fleet's to-dos only once the status says this changed, not every
# 20 seconds. Not counted: fleet_claims (the to-dos' claims, which the status itself carries), and fleet_meta's Team Graph
# round bookkeeping (graph_*) and answer receipts, which change every few minutes and are never shown.
FLEET_VIEW_QUIET_META = "NOT (new.key LIKE 'graph\\_%' ESCAPE '\\' OR new.key LIKE 'answer\\_receipt:%' ESCAPE '\\')"


def watch_fleet_view(db):
    """fleet_view's counter and its triggers on the fleet_ and network_ tables there are, once each."""
    db.execute('CREATE TABLE IF NOT EXISTS data_stamps(name TEXT PRIMARY KEY,n INTEGER NOT NULL)')
    db.execute("INSERT OR IGNORE INTO data_stamps(name,n) VALUES('fleet_view',0)")
    made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'stamp\\_fleetview\\_%' ESCAPE '\\'")}
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE 'fleet\\_%' ESCAPE '\\' "
                                       "OR name LIKE 'network\\_%' ESCAPE '\\') AND name<>'fleet_claims'")]
    for table in tables:
        if not IDENTIFIER.fullmatch(table):
            continue
        for op in ('insert', 'update', 'delete'):
            name = f'stamp_fleetview_{table}_{op}'
            if name in made:
                continue
            row = 'old' if op == 'delete' else 'new'
            when = (' WHEN ' + FLEET_VIEW_QUIET_META.replace('new.', row + '.')) if table == 'fleet_meta' else ''
            db.execute(f"CREATE TRIGGER {name} AFTER {op.upper()} ON {table}{when} BEGIN "
                       "UPDATE data_stamps SET n=n+1 WHERE name='fleet_view'; END")


def counter(db, name):
    """One counter of data_stamps (fleet_view, graph_who), or None when it isn't kept here."""
    try:
        row = db.execute('SELECT n FROM data_stamps WHERE name=?', (name,)).fetchone()
    except sqlite3.Error:
        return None
    return row[0] if row else None


def fleet_view_stamp(db):
    """A small marker that changes whenever the Fleet's view (api/fleet) could: the fleet_view counter and the hour, for
    what only time changes (a free question's "no answer", a split's last day). The dashboard fetches api/fleet for the
    Fleet's to-dos when it changes. None when the counter isn't kept: the dashboard then fetches as before."""
    n = counter(db, 'fleet_view')
    return None if n is None else f"{n}.{timeutil.clock():%Y%m%d%H}"


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
    creates) is missing, as in a new database at the same path. On a connection that made it current already at this
    schema version, one read: no schema change since means its tables are all still there (a status build asked 70 times,
    three reads each)."""
    current = getattr(db, '__dict__', {}).get('_once_made')
    if current and name in current:
        try:
            if db.execute('PRAGMA schema_version').fetchone()[0] == current[name]:
                return
        except sqlite3.Error:
            pass
    key = _schema_key(db)
    if key is not None and (name, *key) in _MADE and db.execute(
            "SELECT 1 FROM sqlite_master WHERE name=?", (sentinel,)).fetchone():
        _made_on(db, name, key[2])
        return
    make(db)
    key = _schema_key(db)  # its tables and triggers changed the schema version
    if key is not None:
        _MADE.add((name, *key))
        _made_on(db, name, key[2])


def _made_on(db, name, version):
    """Noted on the connection itself (the Store's, message_seal.Connection); a plain sqlite3 one keeps nothing. Only
    outside a transaction: one rolled back takes its tables with it and its schema version back."""
    if db.in_transaction:
        return
    try:
        db.__dict__.setdefault('_once_made', {})[name] = version
    except AttributeError:
        pass

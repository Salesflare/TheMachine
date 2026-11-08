"""Which person in the graph has an identifier ("email:ann@client.com", "slack:U0123ABCDE"): a lookup table derived from
graph_nodes.info's identifiers, so a lookup by identifier reads an index instead of every person's info (the to-do list
looked up Slack names and bounced addresses that way: three passes over some 5 MB on each status after a graph change).

Derived only: triggers on graph_nodes keep it in step on every write, and ensure() rebuilds it whole when it is new, empty
or its triggers were missing. Dropping it loses nothing (drop() takes its triggers too; the next start makes it again),
and a reader that finds it missing reads graph_nodes as before (rows).

Only a person's identifiers are indexed, the strings json_each reads from them (as the scan did); the readers keep checking
each row's own identifiers, so a row the index finds is still the row the scan found."""
import json
import sqlite3

TRIGGERS = ('graph_identifiers_insert', 'graph_identifiers_update', 'graph_identifiers_delete')
# A node's identifiers: the strings json_each reads from them, as the scan it replaces did; an info that is not JSON is
# read as none (it never fails the graph's own write).
CREATE = (
    'CREATE TABLE IF NOT EXISTS graph_identifiers(identifier TEXT NOT NULL,node_id TEXT NOT NULL,PRIMARY KEY(identifier,node_id)) WITHOUT ROWID',
    'CREATE INDEX IF NOT EXISTS graph_identifiers_node ON graph_identifiers(node_id)',
    "CREATE TRIGGER IF NOT EXISTS graph_identifiers_insert AFTER INSERT ON graph_nodes WHEN new.kind='person' BEGIN "
    "INSERT OR IGNORE INTO graph_identifiers(identifier,node_id) SELECT j.value,new.id "
    "FROM json_each(CASE WHEN json_valid(new.info) THEN new.info ELSE '{}' END,'$.identifiers') j WHERE j.type='text'; END",
    'CREATE TRIGGER IF NOT EXISTS graph_identifiers_update AFTER UPDATE OF id,kind,info ON graph_nodes BEGIN '
    'DELETE FROM graph_identifiers WHERE node_id=old.id; '
    "INSERT OR IGNORE INTO graph_identifiers(identifier,node_id) SELECT j.value,new.id "
    "FROM json_each(CASE WHEN json_valid(new.info) THEN new.info ELSE '{}' END,'$.identifiers') j WHERE j.type='text' AND new.kind='person'; END",
    'CREATE TRIGGER IF NOT EXISTS graph_identifiers_delete AFTER DELETE ON graph_nodes BEGIN '
    'DELETE FROM graph_identifiers WHERE node_id=old.id; END',
)
REBUILD = ("INSERT OR IGNORE INTO graph_identifiers(identifier,node_id) SELECT j.value,n.id "
           "FROM graph_nodes n, json_each(CASE WHEN json_valid(n.info) THEN n.info ELSE '{}' END,'$.identifiers') j "
           "WHERE j.type='text' AND n.kind='person'")
DROP = ('DROP TRIGGER IF EXISTS graph_identifiers_insert', 'DROP TRIGGER IF EXISTS graph_identifiers_update',
        'DROP TRIGGER IF EXISTS graph_identifiers_delete', 'DROP TABLE IF EXISTS graph_identifiers')
_WHO = (" FROM graph_nodes n WHERE n.kind='person' AND n.id IN "
        '(SELECT node_id FROM graph_identifiers WHERE identifier IN (SELECT value FROM json_each(?))) ORDER BY n.rowid')
READS = {'n.name,n.info': 'SELECT n.name,n.info' + _WHO, 'n.*': 'SELECT n.*' + _WHO}  # the columns a reader asks for


def ensure(db):
    """Make the table, its index and its triggers (each only when missing, so it is safe to run again), and fill it
    whole when it was just made, is empty while there are people, or a trigger was missing (writes it did not see)."""
    made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'graph_identifiers_%'")}
    for sql in CREATE:
        db.execute(sql)
    if set(TRIGGERS) - made or (not db.execute('SELECT 1 FROM graph_identifiers LIMIT 1').fetchone()
                                and db.execute("SELECT 1 FROM graph_nodes WHERE kind='person' LIMIT 1").fetchone()):
        rebuild(db)


def rebuild(db):
    """The whole table again from graph_nodes."""
    db.execute('DELETE FROM graph_identifiers')
    db.execute(REBUILD)


def drop(db):
    """Take it away with its triggers (a graph write would fail on triggers left without their table)."""
    for sql in DROP:
        db.execute(sql)


def rows(db, columns, identifiers, scan, scan_args=()):
    """graph_nodes rows (`columns`, of `n`: one of READS) for the people with any of these identifiers, in the order a
    pass over graph_nodes reads them (rowid). `scan` with `scan_args`: that pass, for a database without the table (an
    old one, or dropped)."""
    identifiers = [str(i) for i in identifiers]
    if not identifiers:
        return []
    try:
        return db.execute(READS[columns], (json.dumps(identifiers),)).fetchall()
    except sqlite3.OperationalError as error:
        if 'graph_identifiers' not in str(error):
            raise
        return db.execute(scan, list(scan_args)).fetchall()

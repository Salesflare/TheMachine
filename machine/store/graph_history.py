"""History in the Graph (docs/help/history.md): older mail and meetings count toward closeness, last talked, who knows
whom and the people and organizations, by counting only. Never toward projects, to-dos, promises, "new" or reviews.

How a build (graph.build with history=True) takes it in: history rows from `since` on (graph_history), newest first.
`since` starts empty, so a new Machine's builds read no history at all; a graph pass after the first look (and only
while nothing of setup runs, machine/app/history.py history_hold) moves it back by at most STEP rows, so each pass
adds a bounded slice and the first pass over a year of history is spread over several builds.

What history adds to a person or organization node: its contact days in strength, wrote/heard/met, last_at and the
links between people. info.history counts its history rows, and info.live is the node's closeness from signals alone:
what the reviews, summaries, lookups and the Network pick people by (live()), so history never makes one of those. A
history row goes to graph_history_events, never to graph_events, so nothing that reads a node's signals (reviews,
preparations, to-dos, the Team Graph) reads history; only Fleet's "who knows someone" reads both
(fleet._work_last), under the same work-account and Team Graph rules as signals, and the owner's own page Timeline
(graph.timeline history=True) shows them, as its last contact counts them."""
import hashlib
import threading

STEP = 5000  # history rows a graph pass may add to the ones the Graph has (a history of 27k: six passes, an hour)


def live(alias=''):
    """SQL for a node's closeness from signals alone (info.live, else strength: a node without history)."""
    prefix = alias + '.' if alias else ''
    return f"coalesce(json_extract({prefix}info,'$.live'),{prefix}strength)"


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS graph_history(id INTEGER PRIMARY KEY CHECK(id=1),since TEXT,at TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS graph_history_events(node_id TEXT NOT NULL,event_id INTEGER NOT NULL,at TEXT NOT NULL,'
               'PRIMARY KEY(node_id,event_id))')


def since(db):
    """The oldest moment of history the Graph takes in, None before the first pass."""
    row = db.execute('SELECT since FROM graph_history WHERE id=1').fetchone()
    return row[0] if row else None


_opened, _opened_lock = {}, threading.Lock()  # database file -> {event id: (fingerprint, opened row)}, in this process
COLUMNS = 'SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE history=1 AND deleted=0 AND '


def rows(db, horizon):
    """The history rows a build counts, from max(horizon, since) on, as (id, account_id, kind, occurred_at, metadata)
    with the metadata opened. [] before the first pass. A history row is sealed, and opening all of them on each build
    (an owner edit rebuilds the Graph) doubled a build's cost, so this process keeps them opened, as text, and opens
    only rows that are new or changed: a row is told by its account, kind, time and its stored, still sealed metadata,
    so one rewritten in place opens again, and one deleted or no longer history drops out."""
    start = since(db)
    if not start:
        return []
    path = next((r[2] for r in db.execute('PRAGMA database_list') if r[1] == 'main'), '')
    raw = db.cursor()
    raw.row_factory = None  # as stored: nothing is opened to tell whether a row changed
    current = raw.execute(COLUMNS + 'occurred_at>=? ORDER BY occurred_at', (max(start, horizon),)).fetchall()
    with _opened_lock:
        kept = _opened.get(path, {}) if path else {}
    out, marks = {}, {}
    for event_id, *row in current:
        mark = hashlib.blake2b(repr(row).encode(), digest_size=16).digest()
        hit = kept.get(event_id)
        if hit and hit[0] == mark:
            out[event_id] = hit
        else:
            marks[event_id] = mark
    for r in _open(db, list(marks)):
        out[r[0]] = (marks[r[0]], r)
    if path:
        with _opened_lock:
            _opened.clear()  # one database per process: never a second copy kept
            _opened[path] = out
    return [out[r[0]][1] for r in current if r[0] in out]


def _open(db, ids):
    """These history rows, opened the usual way: the connection's own rows."""
    opened = []
    for begin in range(0, len(ids), 500):
        chunk = ids[begin:begin + 500]
        opened += [tuple(r) for r in db.execute(COLUMNS + f"id IN ({','.join('?' * len(chunk))})", chunk)]
    return opened


def advance(db, horizon, at, step=STEP):
    """One pass: `since` moves back so the next build takes in at most `step` more history rows. False when all history
    within the horizon is in already."""
    start = since(db)
    if start and start <= horizon:
        return False  # in up to the horizon: what the backfill adds from now on is in its next build
    row = db.execute('SELECT occurred_at FROM events WHERE history=1 AND deleted=0 AND occurred_at>=? AND occurred_at<? '
                     'ORDER BY occurred_at DESC LIMIT 1 OFFSET ?', (horizon, start or '9999', step - 1)).fetchone()
    if not row and not db.execute('SELECT 1 FROM events WHERE history=1 AND deleted=0 AND occurred_at<? LIMIT 1', (start or '9999',)).fetchone():
        return False  # no history (yet): nothing to take in
    db.execute('INSERT INTO graph_history(id,since,at) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET since=excluded.since,at=excluded.at',
               (row[0] if row else horizon, at))
    return True


def publish(db, history_rows):
    """The node -> history row links of a build, in place of the last build's: only what changed is written, as most
    builds (an owner edit) change few of them."""
    wanted = {}
    for node_id, event_id, at in history_rows:
        wanted.setdefault((node_id, event_id), at)
    had = {(r[0], r[1]): r[2] for r in db.execute('SELECT node_id,event_id,at FROM graph_history_events')}
    db.executemany('DELETE FROM graph_history_events WHERE node_id=? AND event_id=?', [k for k in had if k not in wanted])
    db.executemany('INSERT OR REPLACE INTO graph_history_events(node_id,event_id,at) VALUES(?,?,?)',
                   [(*k, at) for k, at in wanted.items() if had.get(k) != at])

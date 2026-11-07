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
(fleet._work_last), under the same work-account and Team Graph rules as signals."""
STEP = 5000  # history rows a graph pass may add to the ones the Graph has (Jeroen's 27k: six passes, an hour)


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


def rows(db, horizon):
    """The history rows a build counts: from max(horizon, since) on. [] before the first pass."""
    start = since(db)
    if not start:
        return []
    return db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE history=1 AND deleted=0 AND occurred_at>=? '
                      'ORDER BY occurred_at', (max(start, horizon),)).fetchall()


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
    """The node -> history row links of a build, in place of the last build's."""
    db.execute('DELETE FROM graph_history_events')
    db.executemany('INSERT OR IGNORE INTO graph_history_events(node_id,event_id,at) VALUES(?,?,?)', history_rows)

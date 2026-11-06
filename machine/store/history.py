"""History: older messages and meetings kept to search and read, never as signals (docs/help/history.md).

The line between history and signal is one column, events.history. A history row (1) is stored reviewed
(analyzed_version=version) and stays reviewed through later edits (assistant.Store.commit_page), so no review, first
look, to-do, promise or "new" count ever sees it. What reads signals by time instead of by review (the Graph, local
embeddings, bounces, Possibly slipped, the setup hints) reads only rows that match SIGNAL. Search, a thread, a message
and the Calendar read both. No model reads history: bringing it in is a plain read of the source.

The backfill's own place is history_backfill: one row per connection, with where its walk back in time is (`state`,
the source's cursor), how many rows it kept, the oldest one so far, and when it reached its depth (done_at). Each step
is small and repeatable: a row already here is never touched again, so a step replayed after a restart keeps nothing
twice."""
import datetime as dt
import json

SIGNAL = 'history=0'  # in SQL on events: a signal, never history
DEFAULT_DAYS = 365  # how far back, per connection (config history_days); 0 turns the backfill off
MAX_DAYS = 730


def ensure(db):
    """The events.history column (0: a signal, 1: history), the backfill's table and the indexes."""
    if 'history' not in {r[1] for r in db.execute('PRAGMA table_info(events)')}:
        db.execute('ALTER TABLE events ADD COLUMN history INTEGER NOT NULL DEFAULT 0')
    db.execute('CREATE TABLE IF NOT EXISTS history_backfill(account_id TEXT PRIMARY KEY,state TEXT NOT NULL,'
               'kept INTEGER NOT NULL DEFAULT 0,oldest TEXT,done_at TEXT,depth_days INTEGER,updated_at TEXT NOT NULL)')
    indexes(db)


def indexes(db):
    """Signals by account and time without the history next to them, and the reviewable ones, so what setup,
    Connected and reviews read stays as fast with a year of history (tests/history_measure.py)."""
    db.execute('CREATE INDEX IF NOT EXISTS events_signal_time ON events(account_id,occurred_at) WHERE history=0')
    db.execute('CREATE INDEX IF NOT EXISTS events_pending_time ON events(account_id,occurred_at) WHERE analyzed_version<version')


def depth(config):
    """How many days back history goes: config history_days (0 to MAX_DAYS), DEFAULT_DAYS when unset or not a number."""
    try:
        value = int((config or {}).get('history_days', DEFAULT_DAYS))
    except (TypeError, ValueError):
        return DEFAULT_DAYS
    return max(0, min(value, MAX_DAYS))


def get(db, account_id):
    """{'state', 'kept', 'oldest', 'done_at', 'depth_days'} of a connection's backfill, None before its first step."""
    row = db.execute('SELECT state,kept,oldest,done_at,depth_days FROM history_backfill WHERE account_id=?', (account_id,)).fetchone()
    if not row:
        return None
    return {'state': json.loads(row[0]), 'kept': row[1], 'oldest': row[2], 'done_at': row[3], 'depth_days': row[4]}


def save(db, account_id, state, at, kept=0, oldest=None, done=False, depth_days=None):
    """One step's end: the cursor, the rows it kept and the oldest one, and done_at once the walk reached its depth."""
    db.execute('INSERT INTO history_backfill(account_id,state,kept,oldest,done_at,depth_days,updated_at) VALUES(?,?,?,?,?,?,?) '
               'ON CONFLICT(account_id) DO UPDATE SET state=excluded.state,kept=kept+excluded.kept,'
               'oldest=CASE WHEN excluded.oldest IS NOT NULL AND (oldest IS NULL OR excluded.oldest<oldest) THEN excluded.oldest ELSE oldest END,'
               'done_at=excluded.done_at,depth_days=coalesce(excluded.depth_days,depth_days),updated_at=excluded.updated_at',
               (account_id, json.dumps(state, sort_keys=True), int(kept), oldest, at if done else None, depth_days, at))


def progress(db, account_ids):
    """{account id: {'back_to': 'YYYY-MM' (the oldest month it reaches), 'done': bool, 'kept': n}} for the cards, only
    for connections whose backfill started."""
    if not account_ids:
        return {}
    return {r[0]: {'back_to': str(r[2])[:7] if r[2] else None, 'done': bool(r[3]), 'kept': r[1]} for r in db.execute(
        'SELECT account_id,kept,oldest,done_at FROM history_backfill WHERE account_id IN (' + ','.join('?' * len(account_ids)) + ')',
        list(account_ids))}


def calendar_start(db, account_ids):
    """The first day calendar history reaches, as an ISO date, once every one of these calendars finished its backfill;
    else None (the Calendar keeps its first-read start)."""
    if not account_ids:
        return None
    rows = db.execute('SELECT done_at,state FROM history_backfill WHERE account_id IN (' + ','.join('?' * len(account_ids)) + ')',
                      list(account_ids)).fetchall()
    if len(rows) < len(set(account_ids)) or any(not r[0] for r in rows):
        return None
    targets = [json.loads(r[1]).get('target') for r in rows]
    return max(t for t in targets if t)[:10] if all(targets) else None


def calendar_coming(db, account_ids):
    """True while one of these calendars' backfill started and hasn't reached its depth."""
    if not account_ids:
        return False
    return bool(db.execute('SELECT 1 FROM history_backfill WHERE done_at IS NULL AND account_id IN (' + ','.join('?' * len(account_ids)) + ')',
                           list(account_ids)).fetchone())


def before(text, days):
    """An ISO time `days` before another one."""
    return (dt.datetime.fromisoformat(text) - dt.timedelta(days=days)).isoformat()

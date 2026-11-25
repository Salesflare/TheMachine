"""Drafts a review asks for ahead that wait while reviews are far behind (a usage limit, a long pause, a big import):
the AI plan's window goes to reading what came in first. The to-do itself is saved and sent as any to-do without a draft
ahead (pending, with Do it), so it is never late; only its draft waits, as a row here, and is started later as the
review would have started it (App.ahead_hold_step). No other state: a restart carries on from the rows.

- Behind: review_catch_up's own definition, more than two whole reviews' worth. Once a draft waits, the Machine counts
  as behind until what waits fits EASE_RUNS review, so a backlog around the line doesn't hold and let go by turns.
- Ends, whichever comes first: the to-do turns pressing or its moment comes near, the owner opens it, the Machine is
  caught up (every row is let go then, and a newer backlog doesn't take that back), or HOLD_HOURS passed. A draft the
  owner uses is mostly used within hours of its to-do, and a to-do that closes without it mostly closes as soon: past
  HOLD_HOURS a longer hold saves little and only makes the rest later. So a Machine that is always behind still gets
  every draft, and a pause of the reviews leaves none behind.
- Dropped, never made: its to-do was closed (for good: not while Undo still brings it back), snoozed, merged or handed
  off, or is worked on already (Do it, a chat, a coding agent).
- One that ever had a run is never held (may_wait)."""
import datetime as dt

from machine import todo_states
from machine.night_pause import NEW_INSTALL_HOURS

HOLD_HOURS = 6       # at most this long, about one 5-hour window of an AI plan
EASE_RUNS = 1        # once drafts wait: caught up when what waits fits this many whole reviews
SOON_DAYS = 2        # a to-do that closes by itself within this many days doesn't wait (as PRESSING_DAYS for a due date)
DECISION = 'ahead-held:'  # its prepare_ahead decision's id: its result comes quietly (quiet), its to-do was sent already


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS ahead_holds(suggestion_id TEXT PRIMARY KEY,created_at TEXT NOT NULL,released_at TEXT)')


def kept(db):
    """How many drafts wait: each took its place in the day's prepared-ahead room when its to-do was saved."""
    return db.execute('SELECT count(*) FROM ahead_holds').fetchone()[0]


def under_way(db):
    """Whether drafts wait for the Machine to catch up (none let go yet): the lower line counts then."""
    return bool(db.execute('SELECT 1 FROM ahead_holds WHERE released_at IS NULL LIMIT 1').fetchone())


def may_wait(db, suggestion_id):
    """A new to-do's first draft: never one that had a run or a draft before."""
    return not db.execute('SELECT 1 FROM preparations WHERE suggestion_id=?', (suggestion_id,)).fetchone()


def keep(db, suggestion_id, at):
    db.execute('INSERT OR IGNORE INTO ahead_holds(suggestion_id,created_at) VALUES(?,?)', (suggestion_id, at))


def gone(db, suggestion_id):
    db.execute('DELETE FROM ahead_holds WHERE suggestion_id=?', (suggestion_id,))


def clear(db):
    return db.execute('DELETE FROM ahead_holds').rowcount


def let_go(db, at):
    """The Machine is caught up: every waiting draft may start in its turn. How many that were."""
    return db.execute('UPDATE ahead_holds SET released_at=? WHERE released_at IS NULL', (at,)).rowcount


def soon(expires_at, current):
    """Its to-do closes by itself within SOON_DAYS: it doesn't wait."""
    try:
        at = dt.datetime.fromisoformat(str(expires_at).replace('Z', '+00:00'))
    except ValueError:
        return False
    return (at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)) <= current + dt.timedelta(days=SOON_DAYS)


def new_owner(db, current):
    """Its first draft isn't started yet or it is a new install's first day: nothing is held then."""
    since = (db.execute("SELECT at FROM milestones WHERE name='tracking_since'").fetchone() or [''])[0]
    return (not db.execute("SELECT 1 FROM milestones WHERE name='first_ahead_started'").fetchone()
            or since > (current - dt.timedelta(hours=NEW_INSTALL_HOURS)).isoformat())


def from_review(db, event_ids):
    """The to-do comes from a regular review's claim under way: never a preview, the first look or its next batches, and
    never what a chat or another turn saves."""
    marks = ','.join('?' * len(event_ids))
    return bool(event_ids) and bool(db.execute(
        "SELECT 1 FROM analyses a JOIN review_runs r ON r.run_id=a.owner_run, json_each(a.items) j "
        "WHERE a.status='running' AND r.preview=0 AND coalesce(r.window_hours,0)=0 AND r.promising=0 "
        f"AND json_extract(j.value,'$.id') IN ({marks}) LIMIT 1", list(event_ids)).fetchone())


def _table(db, name):
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()


def stale(db, current):
    """The waiting drafts whose to-do no longer wants one: {suggestion id: why}."""
    out = {}
    agent = '(SELECT 1 FROM agent_jobs j WHERE j.suggestion_id=s.id)' if _table(db, 'agent_jobs') else 'NULL'
    for r in db.execute('SELECT h.suggestion_id sid,s.status,s.undo_until,(SELECT 1 FROM preparations p WHERE p.suggestion_id=s.id) run,'
                        f'{agent} agent FROM ahead_holds h LEFT JOIN suggestions s ON s.id=h.suggestion_id').fetchall():
        if r['status'] in todo_states.CLOSED and (r['undo_until'] or '') > current.isoformat():
            continue  # Undo still brings it back as it was
        why = ('closed' if r['status'] is None or r['status'] in todo_states.CLOSED else 'snoozed' if r['status'] == todo_states.SNOOZED
               else 'worked on' if r['status'] != todo_states.PENDING or r['run'] or r['agent'] else None)
        if why:
            out[r['sid']] = why
    return out


def ready(db, current, pressing):
    """The waiting drafts that may start now, in order, as (suggestion id, why). pressing(urgent, due) and those the owner
    opened first; then, once let go, the newest to-do first; then those that waited HOLD_HOURS, the
    longest first."""
    first, caught_up, waited = [], [], []
    longest = (current - dt.timedelta(hours=HOLD_HOURS)).isoformat()
    opens = _table(db, 'activity_seen')
    for r in db.execute('SELECT h.*,s.urgent,s.due,s.expires_at FROM ahead_holds h JOIN suggestions s ON s.id=h.suggestion_id '
                        f"WHERE s.status IN {todo_states.sql((todo_states.PENDING,))} AND s.handled_hint IS NULL ORDER BY h.created_at,h.rowid").fetchall():
        sid = r['suggestion_id']
        if pressing(r['urgent'], r['due']) or r['expires_at'] and soon(r['expires_at'], current):
            first.append((sid, 'pressing'))
        elif opens and db.execute("SELECT 1 FROM activity_seen WHERE kind='opened' AND ref=? LIMIT 1", (sid,)).fetchone():
            first.append((sid, 'opened'))
        elif r['released_at']:
            caught_up.append((sid, 'caught up'))
        elif r['created_at'] <= longest:
            waited.append((sid, 'waited'))
    return first + caught_up[::-1] + waited


def one_going(db):
    """A draft ahead is already starting or under way: the next one waits its turn (automated follow-ups go apart)."""
    return bool(db.execute("SELECT 1 FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id WHERE s.early=1 "
                           f"AND s.status IN {todo_states.sql(todo_states.PREPARING)} AND p.status IN ('queued','starting','running') "
                           'AND s.id NOT IN (SELECT suggestion_id FROM follow_up_cards) LIMIT 1').fetchone())


def quiet(db, row):
    """A draft that waited is ready on a to-do the owner was told of when it was saved: the message is edited, no ping."""
    return bool(row.get('message_id') and row.get('early') and row.get('status') == todo_states.PREPARED and db.execute(
        'SELECT 1 FROM preparations WHERE suggestion_id=? AND substr(decision_id,1,?)=?', (row['id'], len(DECISION), DECISION)).fetchone())

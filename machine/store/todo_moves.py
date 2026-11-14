"""A to-do's moves from one status to another: transition() checks each against machine/todo_states.MOVES and keeps it
in the to-do's history (todo_moves). Writers move a to-do through transition(), one area at a time, instead of their
own UPDATE of suggestions.status.

A writer that sets more columns with the move does so in its own UPDATE in the same transaction, just before the
move: there an expression that reads status (closed_from=status) still reads the status before the move.

The history holds the statuses, when, and a short reason in code words (such as 'do_it' or 'wake'), never text from
the to-do. Removing a source's work removes its rows with the to-do (work_removal: the suggestion_id column)."""
from machine import todo_states
from timeutil import now


class MoveNotAllowed(ValueError):
    """A move machine/todo_states.MOVES doesn't declare: a bug in the caller, not something for the owner."""


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS todo_moves(id INTEGER PRIMARY KEY,suggestion_id TEXT NOT NULL,at TEXT NOT NULL,'
               'from_status TEXT NOT NULL,to_status TEXT NOT NULL,reason TEXT NOT NULL)')
    db.execute('CREATE INDEX IF NOT EXISTS todo_moves_card ON todo_moves(suggestion_id,id)')


def transition(db, suggestion_id, to, reason, *, only=None, at=None):
    """Move to-do suggestion_id to status `to`, for `reason` (a short code word), and keep the move in its history.
    only: the statuses it may move from (a group or one status), as an UPDATE's AND status IN (...) did; from any other
    it stays as it is.

    Returns how many rows moved, 0 or 1, as that UPDATE's rowcount would: 0 when the to-do is gone or its status isn't
    in `only`. A move MOVES doesn't declare raises MoveNotAllowed and changes nothing. Staying in the same status counts
    as 1 and writes no history."""
    if to not in todo_states.ALL:
        raise MoveNotAllowed(f'not a to-do status: {to!r}')
    row = db.execute('SELECT status FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if row is None:
        return 0
    before = row[0]
    if only is not None and before not in ((only,) if isinstance(only, str) else only):
        return 0
    if not todo_states.allowed(before, to):
        raise MoveNotAllowed(f'to-do move not declared in todo_states.MOVES: {before} -> {to} ({reason})')
    if before == to:
        return 1
    moved = db.execute('UPDATE suggestions SET status=? WHERE id=? AND status=?', (to, suggestion_id, before)).rowcount
    if moved:
        db.execute('INSERT INTO todo_moves(suggestion_id,at,from_status,to_status,reason) VALUES(?,?,?,?,?)',
                   (suggestion_id, at or now(), before, to, str(reason)[:60]))
    return moved


def history(db, suggestion_id):
    """A to-do's moves, oldest first: [{'at', 'from', 'to', 'reason'}]."""
    return [{'at': r[0], 'from': r[1], 'to': r[2], 'reason': r[3]} for r in db.execute(
        'SELECT at,from_status,to_status,reason FROM todo_moves WHERE suggestion_id=? ORDER BY id', (suggestion_id,))]

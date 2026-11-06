"""Still needed? (docs/help/cards.md): an open to-do nobody touched for a week is asked about once, on the to-do itself.

To-dos pile up when nobody says no to them: a draft is ready, the moment passed, and the to-do just sits. Looks done
needs a sign it was handled and a time-bound to-do closes by itself (Store.expire_passed); the rest waits for the owner.
So once a to-do has sat untouched for DAYS, the to-do asks "Still needed?" with the weekly recap's own Drop and Keep:

- touched: opened (its chat read on the dashboard or by Talk: the 'opened' marks activity.py keeps a few days), a decision by the owner (a chat message, a
  change, a snooze, a rename...), an edit of its draft, or a new message on it (an event it is about);
- asked once: the question is a row in the weekly recap's choices table (recap_items, kind KIND), never added twice
  for a to-do, so Keep (status 'kept') means never again. Drop is the dashboard's own Not needed (a reject decision),
  answered there; a to-do that closes any way ends its question (Store.still_needed_ask);
- no answer: once the question has waited DAYS more without a touch, the dashboard folds the to-do into Coming back
  later, under its own heading, instead of deleting it (annotate: folded). A touch brings it back; the question stays.

Asked only of to-dos waiting on the owner (OPEN): not snoozed, closed or still preparing, and not of one that looks done,
waits on others (the caller's skip), has a date still ahead, closes by itself at a set time or repeats (recurring.py)."""
from __future__ import annotations

import datetime as dt
import json

DAYS = 7
KIND = 'still_needed'
OPEN = ('pending', 'prepared')
# Decisions that aren't the owner's own touch: the Machine's own, automated follow-ups, a coding agent
NOT_TOUCHES = ('assistant', 'auto_follow_up', 'agent')

def _at(value):
    """An ISO time (with Z, an offset or none: UTC) as an aware datetime, or None."""
    try:
        d = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def _tables(db):
    return {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def last_touch(db, cards, tz=dt.timezone.utc):
    """{card id: when it was last touched (datetime)}: made, opened, decided on by the owner, its draft edited, or a new
    message on it. cards are rows with id, created_at and event_ids. An open is marked by its local day (tz), so it
    counts as the end of that day."""
    ids = [c['id'] for c in cards]
    out = {c['id']: _at(c['created_at']) for c in cards}
    opens = 'activity_seen' in _tables(db)

    def later(sid, value):
        d = _at(value)
        if d and (out.get(sid) is None or d > out[sid]):
            out[sid] = d
    for n in range(0, len(ids), 400):
        chunk = ids[n:n + 400]
        marks = ','.join('?' * len(chunk))
        for r in db.execute(f"SELECT ref,max(day) FROM activity_seen WHERE kind='opened' AND ref IN ({marks}) GROUP BY ref", chunk) if opens else []:
            try:
                later(r[0], dt.datetime.combine(dt.date.fromisoformat(r[1]) + dt.timedelta(days=1), dt.time(), tz).isoformat())
            except (TypeError, ValueError):
                pass
        for r in db.execute(f"SELECT suggestion_id,max(created_at) FROM decisions WHERE suggestion_id IN ({marks}) "
                            f"AND source NOT IN ({','.join('?' * len(NOT_TOUCHES))}) GROUP BY suggestion_id", [*chunk, *NOT_TOUCHES]):
            later(r[0], r[1])
        for r in db.execute(f"SELECT suggestion_id,max(created_at) FROM draft_edits WHERE suggestion_id IN ({marks}) AND source!='agent' "
                            'GROUP BY suggestion_id', chunk):
            later(r[0], r[1])
    on_event = {}
    for c in cards:
        try:
            for e in json.loads(c.get('event_ids') or '[]'):
                on_event.setdefault(int(e), []).append(c['id'])
        except (TypeError, ValueError):
            continue
    events = list(on_event)
    for n in range(0, len(events), 400):
        chunk = events[n:n + 400]
        for r in db.execute(f"SELECT id,occurred_at FROM events WHERE id IN ({','.join('?' * len(chunk))})", chunk):
            for sid in on_event.get(r[0], []):
                later(sid, r[1])
    return out


def _repeating(db):
    try:
        return {r[0] for r in db.execute('SELECT suggestion_id FROM recurring_cards')}
    except Exception:  # noqa: BLE001 - no recurring to-dos on this Machine yet
        return set()


def due(db, stamp, skip=lambda row: False, tz=dt.timezone.utc):
    """The open to-dos to ask now: untouched for DAYS and never asked. skip(row) leaves a to-do out (the caller's looks
    done and waiting on others). Store.still_needed_ask writes the questions (assistant.py owns recap_items)."""
    current = _at(stamp)
    today = current.date().isoformat()
    asked = {r[0] for r in db.execute('SELECT ref FROM recap_items WHERE kind=?', (KIND,))}
    repeating = _repeating(db)
    rows = [dict(r) for r in db.execute(f"SELECT * FROM suggestions WHERE status IN ({','.join('?' * len(OPEN))})", OPEN)]
    rows = [r for r in rows if r['id'] not in asked and r['id'] not in repeating and not r.get('expires_at')
            and not (r.get('due') and str(r['due'])[:10] >= today) and not skip(r)]
    touched = last_touch(db, rows, tz)
    return [r for r in rows if touched.get(r['id']) and current - touched[r['id']] >= dt.timedelta(days=DAYS)]


def annotate(db, cards, stamp, tz=dt.timezone.utc):
    """Each open to-do with an open question gets still_needed: {'id', 'since' (its last touch), 'folded'}. Folded:
    the question waited DAYS without an answer or a touch, so the dashboard puts it out of the way."""
    live = [c for c in cards if c.get('status') not in ('completed', 'rejected', 'snoozed')]
    if not live:
        return
    ids = [c['id'] for c in live]
    open_rows = {}
    for n in range(0, len(ids), 400):
        chunk = ids[n:n + 400]
        for r in db.execute(f"SELECT id,ref,data FROM recap_items WHERE kind=? AND status='open' AND ref IN ({','.join('?' * len(chunk))})", [KIND, *chunk]):
            open_rows[r['ref']] = r
    if not open_rows:
        return
    current = _at(stamp)
    asking = [c for c in live if c['id'] in open_rows]
    touched = last_touch(db, asking, tz)
    for c in asking:
        row = open_rows[c['id']]
        try:
            asked = _at(json.loads(row['data']).get('asked_at')) or current
        except (TypeError, ValueError, AttributeError):
            asked = current
        since = touched.get(c['id']) or asked
        c['still_needed'] = {'id': row['id'], 'since': since.isoformat(), 'folded': current - max(asked, since) >= dt.timedelta(days=DAYS)}

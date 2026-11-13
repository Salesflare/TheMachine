"""One more look for messages the review set aside (SET_ASIDE_AFTER). A message the review put off twice at the same
version is no longer offered, and until this it stayed that way unless its thread changed: never judged, never in the
missed-work audit. Now a set-aside message that may need the owner gets ONE more look, LAST_LOOK_DAYS after it came in,
in a regular review that runs anyway (begin_analysis), at most LAST_LOOK_CAP per review: no model call of its own.

Who may need the owner is read without a model, from who wrote to whom, never the words: not automated or bulk
(review_wait.can_wait), and a person writing to the owner directly (need_rank 0), a person the Graph knows, or a
customer's conversation no teammate has taken. Anything the owner already decided stays decided: a message on any
to-do (open, done, snoozed or dismissed), a thread with a dismissed or snoozed to-do, a snoozed mail thread, Spam or
Trash.

The last look ends it either way. Reviewed: the review's usual path (a to-do through suggest, with its dedupe, or
no to-do with its no_todo line). Put off again: finish_analysis counts one more deferral, past SET_ASIDE_AFTER, and
it is closed for good (CLOSED_AFTER); nothing offers it again. A new version of the message starts over, as before.

The count and a short list show under Checks of new messages (listing, review_health)."""
import datetime as dt
import json
import sqlite3

from machine.store import review_wait
from machine.store.events import SET_ASIDE_AFTER
from timeutil import now

LAST_LOOK_DAYS = 3        # the one more look: this long after the message came in
LAST_LOOK_MAX_DAYS = 30   # older set-aside messages stay as they are
LAST_LOOK_CAP = 5         # per review: the rest wait for the next one
CLOSED_AFTER = SET_ASIDE_AFTER + 1  # deferrals: put off at its last look too, closed for good
LISTED = 10               # rows in the list under the count

# The review is told (review_view last_look): this is its last look
RULE = ('Last look: set aside twice before. Judge it now on what is here; left out of reviewed_ids it is closed for good.')

CUSTOMER_KINDS = frozenset({'intercom.conversation', 'fleet.intercom'})
DECIDED = ('rejected', 'snoozed')  # the owner's Not needed, dismissed or snoozed to-dos
THREAD_KEYS = ('thread_id', 'conversation_id', 'chat_id', 'channel_id')


def meta(row):
    try:
        value = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
    except (TypeError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def thread(metadata):
    for key in THREAD_KEYS:
        if metadata.get(key):
            return key, str(metadata[key])
    return None


def worth(store, db, row, own, people):
    """Whether a set-aside message may need the owner, read from who wrote to whom (never the words)."""
    m = meta(row)
    if row['deleted'] or row.get('history') or {'SPAM', 'TRASH'} & set(m.get('labels') or ()):
        return False
    if review_wait.can_wait(row, people):  # automated or bulk: a newsletter, a receipt, an app's notification
        return False
    if row['kind'] in CUSTOMER_KINDS:
        assigned = store.intercom_assignments(db, [row]).get(row['id']) if row['kind'] == 'intercom.conversation' else None
        return not isinstance(assigned, tuple)  # a teammate took it: theirs
    if store.need_rank(row, own) == 0:
        return True
    address = review_wait.sender(m) if row['kind'] == 'gmail.message' else ''
    return bool(address) and address not in own and people.person(address)


def decided(db, row):
    """The owner decided on this message or its thread already: it's on a to-do, its thread has a dismissed or snoozed
    to-do, or its mail thread is snoozed."""
    if db.execute('SELECT 1 FROM suggestions s, json_each(s.event_ids) j WHERE j.value=? LIMIT 1', (row['id'],)).fetchone():
        return True
    key = thread(meta(row))
    if not key:
        return False
    field, value = key
    if db.execute(f"SELECT 1 FROM suggestions s, json_each(s.event_ids) j JOIN events e ON e.id=j.value WHERE s.status IN ({','.join('?' * len(DECIDED))}) "
                  f"AND e.account_id=? AND json_extract(e.metadata,'$.{field}')=? LIMIT 1", (*DECIDED, row['account_id'], value)).fetchone():
        return True
    if field == 'thread_id':
        try:
            return bool(db.execute("SELECT 1 FROM thread_snoozes WHERE account_id=? AND thread_id=? AND status IN ('queued','snoozed') AND until>? LIMIT 1",
                                   (row['account_id'], value, now())).fetchone())
        except sqlite3.OperationalError:  # a database without snoozed threads yet
            return False
    return False


def set_aside_rows(db, accounts=None, closed=False):
    """The set-aside messages (pending, put off SET_ASIDE_AFTER times), with closed ones too when asked; newest first."""
    marks = ','.join('?' * len(accounts)) if accounts else ''
    where = f' AND account_id IN ({marks})' if accounts else ''
    deferrals = 'deferrals>=?' if closed else 'deferrals=?'
    return [dict(r) for r in db.execute(f'SELECT * FROM events WHERE history=0 AND analyzed_version<version AND {deferrals}{where} '
                                        'ORDER BY ingested_at DESC,id DESC LIMIT 500', (SET_ASIDE_AFTER, *(accounts or ())))]


def due(store, db, accounts, cap=LAST_LOOK_CAP, current=None):
    """Set-aside messages for one more look now, oldest first, at most cap."""
    if cap <= 0:
        return []
    current = current or dt.datetime.fromisoformat(now())
    ready, oldest = (current - dt.timedelta(days=LAST_LOOK_DAYS)).isoformat(), (current - dt.timedelta(days=LAST_LOOK_MAX_DAYS)).isoformat()
    own, people = store.review_own_addresses(db), review_wait.People(db)
    found = []
    for row in reversed(set_aside_rows(db, accounts)):
        if not oldest <= row['ingested_at'] <= ready:
            continue
        if worth(store, db, row, own, people) and not decided(db, row):
            found.append(row)
            if len(found) >= cap:
                break
    return found


def listing(store, db, limit=LISTED):
    """The set-aside messages for the list under the count: {id, kind, title, at, state, look_at}. state: 'look' (one
    more look on look_at, or with the next check once that passed), 'closed' (put off at its last look too) or 'left'
    (no sign it needs the owner, or the owner decided already)."""
    own, people = store.review_own_addresses(db), review_wait.People(db)
    out = []
    for row in set_aside_rows(db, closed=True)[:limit]:
        if row['deferrals'] >= CLOSED_AFTER:
            state = 'closed'
        else:
            state = 'look' if worth(store, db, row, own, people) and not decided(db, row) else 'left'
        look_at = (dt.datetime.fromisoformat(row['ingested_at']) + dt.timedelta(days=LAST_LOOK_DAYS)).isoformat() if state == 'look' else None
        out.append({'id': row['id'], 'kind': row['kind'], 'title': (row['title'] or '')[:200], 'at': row['occurred_at'], 'state': state, 'look_at': look_at})
    return out

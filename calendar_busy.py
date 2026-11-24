"""When the owner is busy, and which times their Machine doesn't know: plain code over the synced calendars, no table.

One rule for what takes time (blocks), used by free/busy (friends.free_busy: a friend's question, a Family's "When are
we all free?", scheduling between Machines) and calendar clashes (calendar_clashes.py).

Free/busy is only as good as what was read. A time is known when the owner has a calendar of their own connected, it
was read within the last STALE, and the time is inside the days that were read in full (a calendar's checkpoint:
read_from, read_until; machine/sources/calendar.py). Every other time is unknown: never free and never busy. With two
calendars, a time is known when both are. One failed read changes nothing until STALE passed."""
from __future__ import annotations

import datetime as dt
import json
import sqlite3

import own_addresses
from machine import names

STALE = dt.timedelta(hours=24)         # a calendar not read for this long: what is on it now isn't known
OLD_DAYS = 30                          # how far ahead a Machine from before `unknown` reads its calendars
LONGEST = dt.timedelta(days=366)       # an event that began this long ago may still run


def moment(value):
    """An aware datetime, or None."""
    try:
        at = dt.datetime.fromisoformat(str(value or '').replace('Z', '+00:00'))
    except ValueError:
        return None
    return at if at.tzinfo else None


def blocks(metadata):
    """Whether an event takes its time: Busy in its calendar. A timed event does unless it is marked Free; an all-day
    one only when its calendar says Busy ('opaque'), since birthdays, holidays and the like are Free by default."""
    shown = metadata.get('transparency')
    return shown == 'opaque' if metadata.get('all_day') else shown != 'transparent'


def mine(metadata):
    """On the owner's own calendar, live and not declined."""
    if metadata.get('status') == 'cancelled' or metadata.get('access') == 'shared_read_only':
        return False
    return not any(isinstance(a, dict) and a.get('self') and a.get('responseStatus') == 'declined' for a in metadata.get('attendees') or [])


def merge(spans):
    out = []
    for a, b in sorted(s for s in spans if s[0] < s[1]):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def calendars(config):
    """The ids of the owner's own calendars that sync: never one shared with them, or one that only does actions."""
    return [a['id'] for a in own_addresses.own_accounts(config) if own_addresses.own_calendar(a) and a.get('signals') is not False]


def known(db, account_id, current):
    """The span (from, until) of one calendar that is known now, or None."""
    try:
        row = db.execute('SELECT state,last_success FROM checkpoints WHERE account_id=?', (account_id,)).fetchone()
    except sqlite3.OperationalError:  # nothing was ever read
        return None
    read = moment(row['last_success']) if row else None
    if not read or current - read > STALE:
        return None
    try:
        state = json.loads(row['state'] or '{}')
    except ValueError:
        return None
    done = state.get('mode') == 'incremental'  # a window read in full before read_from and read_until were kept
    since = moment(state.get('read_from') or (state.get('time_min') if done else None))
    until = moment(state.get('read_until') or (state.get('time_max') if done else None))
    return (since, until) if since and until and since < until else None


def unread(db, config, current):
    """The owner's own calendars nothing is known of now (never read, or not for STALE), by their names on Connections.
    For the owner only: on their own dashboard, never in an answer."""
    accounts, out = config.get('accounts') or [], []
    for account_id in calendars(config):
        if not known(db, account_id, current):
            account = next(a for a in accounts if a.get('id') == account_id)
            try:
                row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account_id,)).fetchone()
                state = json.loads(row['state'] or '{}') if row else {}
            except (sqlite3.OperationalError, ValueError):
                state = {}
            out.append(names.card_title(account, accounts, state))
    return list(dict.fromkeys(out))


def read(db, config, start, end, current):
    """(busy, unknown) between start and end: merged (from, until) spans. Unknown wins where the two overlap."""
    own = calendars(config)
    if not own:
        return [], [(start, end)]
    busy, unknown, spans = [], [], {}
    for account_id in own:
        span = spans[account_id] = known(db, account_id, current)
        unknown += [(start, end)] if not span else [(start, min(end, span[0])), (max(start, span[1]), end)]
    # end_at is a plain key (message_seal.ROUTING_KEYS); a row sealed before it was one has none here and is read too
    rows = db.execute("SELECT account_id,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                      'AND +account_id IN (SELECT value FROM json_each(?)) AND occurred_at<? AND occurred_at>=? '
                      "AND (json_extract(metadata,'$.end_at') IS NULL OR CAST(json_extract(metadata,'$.end_at') AS TEXT)>?)",
                      (json.dumps(own), end.isoformat(), (start - LONGEST).isoformat(), (start - dt.timedelta(days=1)).isoformat()))
    for row in rows:
        if not spans[row['account_id']]:
            continue  # what that calendar says now isn't known
        meta = json.loads(row['metadata'] or '{}')
        a, b = moment(row['occurred_at']), moment(meta.get('end_at'))
        if a and b and mine(meta) and blocks(meta) and a < b and b > start and a < end:
            busy.append((max(a, start), min(b, end)))
    return merge(busy), merge(unknown)

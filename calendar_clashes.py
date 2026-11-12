"""Calendar clashes: a work meeting that overlaps something in a personal calendar, or the other way around.

Plain code, no model: every pass (App.clash_step) reads the timed events of the calendars the Machine already has
(Google and Outlook, each connection Work or Personal by graph.account_side) for the next AHEAD_DAYS days and pairs each
work event with each personal one it overlaps. Only a found clash becomes a to-do, and only that to-do's preparation
(prepared ahead, like any to-do) uses the model: a short note to move the meeting, or a way to decline or move it.
Nothing goes out until the owner approves it on the to-do.

What counts: both events timed (never all day), busy (not free/transparent), on a calendar of the owner's or one they
are on (calendar_owned), not canceled or declined, and firm: an event marked tentative, or one the owner answered
Maybe, never clashes. An invite still waiting for an answer counts, since that is the moment to say no. The same
meeting on both calendars (one iCalUID, or the same title and times) is one meeting, not a clash. Two blocks with
nobody else on either (a focus block over a gym slot) aren't one either: the owner put both there, and there is no one
to move it with.

Which side the to-do is about: the event that came in or changed last (its `updated`), since that is the one that
made the clash; Work when they tie. The to-do sits in that event's area and holds only that event as evidence.

Sharing: what a to-do stores (title, body, evidence) names only its own event; the other side is "a personal event" or
"a work meeting". So a Work to-do, its preparation, a handoff or anything a Fleet sees never carries the personal
event's details, only that there is a conflict. The owner's own dashboard shows the other side in full (annotate),
read at view time from calendar_clashes and never written into the to-do.

Once: calendar_clashes keeps every clash raised, by the pair's series (a recurring meeting clashing with a recurring
one is one clash, not one a week), so a clash comes up once, also after the to-do is done or dismissed. At most
PER_DAY new clash to-dos a day."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sqlite3

SCHEMA = ('CREATE TABLE IF NOT EXISTS calendar_clashes(dedupe_key TEXT PRIMARY KEY,suggestion_id TEXT,event_id INTEGER NOT NULL,'
          'other_id INTEGER NOT NULL,side TEXT NOT NULL,starts_at TEXT NOT NULL,created_at TEXT NOT NULL)')
CALENDARS = ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')
AHEAD_DAYS = 14  # how far ahead a clash is looked for
PER_DAY = 3      # new clash to-dos a day, at most
SIDES = ('work', 'personal')


def ensure(db):
    db.execute(SCHEMA)


def calendar_sides(accounts, side_of):
    """{account_id: 'work' or 'personal'} for each connected calendar; side_of is graph.account_side."""
    out = {}
    for a in accounts or ():
        if a.get('service') in CALENDARS and side_of(a) in SIDES:
            out[a['id']] = side_of(a)
    return out


def _at(value):
    try:
        at = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None
    return at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)


def _own_response(metadata):
    """The owner's own answer on the invite ('accepted', 'tentative', 'declined', 'needsAction'), None when they are
    not listed (their own event)."""
    for a in metadata.get('attendees') or ():
        if isinstance(a, dict) and a.get('self'):
            return a.get('responseStatus')
    return None


def firm(metadata, owned):
    """Whether an event blocks the owner's time for sure: timed, busy, live, theirs and not tentative."""
    if metadata.get('all_day') or metadata.get('transparency') == 'transparent':
        return False
    if metadata.get('status') in ('tentative', 'cancelled'):
        return False
    if _own_response(metadata) in ('declined', 'tentative'):
        return False
    return bool(owned(metadata))


def _series(row):
    """The meeting or series an event is part of: its iCalUID (one for every occurrence, and the same on every calendar
    it is on), else its own series or id on its calendar (Outlook has no iCalUID here)."""
    m = row['meta']
    return m.get('ical_uid') or f"{row['account_id']}:{m.get('recurring_event_id') or row['source_id']}"


def with_others(row):
    """Whether someone besides the owner is on it (a booked room doesn't count)."""
    return any(isinstance(a, dict) and not a.get('self') and not a.get('resource') and a.get('email')
               for a in row['meta'].get('attendees') or ())


def clash_key(a, b):
    """One key per pair of series (or single events), the same whichever side comes first."""
    pair = '|'.join(sorted((_series(a), _series(b))))
    return 'clash:' + hashlib.sha256(pair.encode()).hexdigest()[:32]


def same_meeting(a, b):
    ua, ub = a['meta'].get('ical_uid'), b['meta'].get('ical_uid')
    if ua and ua == ub:
        return True
    return (a['title'].strip().casefold(), a['start'], a['end']) == (b['title'].strip().casefold(), b['start'], b['end'])


def events(db, sides, start, end, owned):
    """The firm, timed events on these calendars that start within (start, end): dicts with id, account_id, source_id,
    title, start, end (aware datetimes), side and meta. Times are read from the opened metadata, never in SQL: on a
    Machine with message protection (the default) end_at is sealed, so json_extract can't see it."""
    if not sides:
        return []
    marks = ','.join('?' * len(sides))
    rows = db.execute(f"SELECT id,account_id,source_id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                      f"AND account_id IN ({marks}) AND occurred_at<? AND occurred_at>?",
                      [*sides, end.isoformat(), start.isoformat()]).fetchall()
    out = []
    for r in rows:
        try:
            meta = json.loads(r['metadata'] or '{}')
        except ValueError:
            continue
        begins, ends = _at(r['occurred_at']), _at(meta.get('end_at'))
        if not begins or not ends or ends <= begins or not firm(meta, owned):
            continue
        out.append({'id': r['id'], 'account_id': r['account_id'], 'source_id': r['source_id'], 'title': r['title'] or '',
                    'start': begins, 'end': ends, 'side': sides[r['account_id']], 'meta': meta})
    return out


def find(db, sides, current, owned, days=AHEAD_DAYS):
    """Every clash ahead: [{'key', 'work', 'personal', 'start', 'end'}], each pair of series once, soonest first.
    Only clashes that have not started yet (both events still ahead)."""
    found = events(db, sides, current, current + dt.timedelta(days=days), owned)
    work = sorted((e for e in found if e['side'] == 'work' and e['start'] > current), key=lambda e: e['start'])
    personal = sorted((e for e in found if e['side'] == 'personal' and e['start'] > current), key=lambda e: e['start'])
    out, seen = [], set()
    for w in work:
        for p in personal:
            if p['start'] >= w['end']:
                break
            if p['end'] <= w['start'] or same_meeting(w, p) or not (with_others(w) or with_others(p)):
                continue  # apart, one meeting on two calendars, or two blocks the owner made alone
            key = clash_key(w, p)
            if key in seen:
                continue
            seen.add(key)
            out.append({'key': key, 'work': w, 'personal': p, 'start': max(w['start'], p['start']), 'end': min(w['end'], p['end'])})
    return sorted(out, key=lambda c: c['start'])


def newer_side(clash):
    """The side whose event came in or changed last: the one that made the clash. Work on a tie."""
    w, p = (str(clash[s]['meta'].get('updated') or '') for s in SIDES)
    return 'personal' if p > w else 'work'


def raised(db, keys):
    ensure(db)
    keys = list(keys)
    found = set()
    for n in range(0, len(keys), 400):
        chunk = keys[n:n + 400]
        found |= {r[0] for r in db.execute(f"SELECT dedupe_key FROM calendar_clashes WHERE dedupe_key IN ({','.join('?' * len(chunk))})", chunk)}
    return found


def raised_today(db, since):
    ensure(db)
    return db.execute('SELECT count(*) FROM calendar_clashes WHERE created_at>=? AND suggestion_id IS NOT NULL', (since,)).fetchone()[0]


def keep(db, clash, side, suggestion_id, stamp):
    ensure(db)
    other = 'personal' if side == 'work' else 'work'
    db.execute('INSERT OR IGNORE INTO calendar_clashes(dedupe_key,suggestion_id,event_id,other_id,side,starts_at,created_at) VALUES(?,?,?,?,?,?,?)',
               (clash['key'], suggestion_id, clash[side]['id'], clash[other]['id'], side, clash['start'].isoformat(), stamp))


def annotate(db, cards):
    """card['clash'] on each open clash to-do, for the owner's own dashboard: the other side in full
    {'title', 'start', 'end', 'side'}. Read here, never stored on the to-do, so nothing that reads the to-do
    (a Fleet, a handoff, its preparation) sees it."""
    live = {c['id']: c for c in cards if c.get('status') not in ('completed', 'rejected') and str(c.get('dedupe_key') or '').startswith('clash:')}
    if not live:
        return
    try:
        rows = db.execute(f"SELECT c.suggestion_id,c.side,e.title,e.occurred_at,e.metadata FROM calendar_clashes c JOIN events e ON e.id=c.other_id "
                          f"WHERE e.deleted=0 AND c.suggestion_id IN ({','.join('?' * len(live))})", list(live)).fetchall()
    except sqlite3.OperationalError:  # no clash raised on this Machine yet
        return
    for r in rows:
        try:
            end = json.loads(r['metadata'] or '{}').get('end_at')
        except ValueError:
            end = None
        live[r['suggestion_id']]['clash'] = {'title': r['title'], 'start': r['occurred_at'], 'end': end,
                                             'side': 'personal' if r['side'] == 'work' else 'work'}

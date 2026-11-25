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
to move it with. Google's own working location, focus time and out of office never clash, whatever is over them.

A frame around the day is no meeting: a block nobody else is on that holds meetings of its own side (an office day,
working from home, a conference day), or that does on other days of its series (frame). It never clashes by itself,
the meetings in it do. It is told by what is inside it, never by its title. A block nobody else is on with no meeting
inside (a flight on the work calendar, a dentist on the personal one) is a commitment of its own and still clashes with
an event that has others on it: nothing in the calendar tells a flight from a quiet afternoon.

One to-do per event: an event that overlaps several on the other side is one to-do, about that event (grouped). It is
judged on its whole overlap: events after the window's end are read too (AFTER), so what starts a little later is in it
from the start. Two events that only overlap each other: the to-do is about the one that came in or changed last (its
`updated`), since that is the one that made the clash; Work when they tie. The to-do sits in its event's area and holds
only that event as evidence.

Later (plan): a new overlap with an event that has an open clash to-do joins it. When the event the overlaps share is
only the other side of an open to-do the owner did nothing on, one to-do about that event takes its place, and a to-do
whose every overlap is on others, or turned out to be with a frame, closes by itself; never one the owner acted on. On an
event whose to-do is closed (done, dismissed or expired), only an event that was made or changed after that to-do
comes up again; one that was there all along stays quiet.

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

import calendar_busy
from machine import todo_states

SCHEMA = ('CREATE TABLE IF NOT EXISTS calendar_clashes(dedupe_key TEXT PRIMARY KEY,suggestion_id TEXT,event_id INTEGER NOT NULL,'
          'other_id INTEGER NOT NULL,side TEXT NOT NULL,starts_at TEXT NOT NULL,created_at TEXT NOT NULL)')
CALENDARS = ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')
AHEAD_DAYS = 14  # how far ahead a clash is looked for
AFTER = dt.timedelta(days=7)    # read past the window, so what enters it is judged with everything it overlaps
BEFORE = dt.timedelta(days=14)  # and back, for what a recurring block holds on its other days
PER_DAY = 3      # new clash to-dos a day, at most
SIDES = ('work', 'personal')
OWN_BLOCKS = ('workingLocation', 'focusTime', 'outOfOffice')  # Google's eventType: where or how the owner works, or that they are away
GONE = 'clash-gone:'  # the decision that closed a to-do whose clash is gone (Store.clash_gone)


def ensure(db):
    db.execute(SCHEMA)


def calendar_sides(accounts, side_of):
    """{account_id: 'work' or 'personal'} for each connected calendar; side_of is graph.account_side."""
    out = {}
    for a in accounts or ():
        if a.get('service') in CALENDARS and side_of(a) in SIDES:
            out[a['id']] = side_of(a)
    return out


def other_side(side):
    return 'personal' if side == 'work' else 'work'


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
    if metadata.get('all_day') or not calendar_busy.blocks(metadata):  # one rule for what is Busy
        return False
    if metadata.get('status') in ('tentative', 'cancelled') or metadata.get('event_type') in OWN_BLOCKS:
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


def meetings(found, side):
    """One side's events with the same meeting on several of its calendars as one: the event (a copy someone else is on
    first), its 'copies', all their 'ids' and 'others' (whether anyone else is on it), soonest first."""
    by, out = {}, []
    for e in sorted((e for e in found if e['side'] == side), key=lambda e: (not with_others(e), e['id'])):
        keys = [('title', e['title'].strip().casefold(), e['start'], e['end'])]
        if e['meta'].get('ical_uid'):
            keys.append(('uid', e['meta']['ical_uid'], e['start']))
        kept = next((by[k] for k in keys if k in by), None)
        if kept is None:
            kept = {**e, 'copies': [], 'ids': set(), 'others': with_others(e)}
            out.append(kept)
        kept['copies'].append(e)
        kept['ids'].add(e['id'])
        for k in keys:
            by.setdefault(k, kept)
    return sorted(out, key=lambda e: e['start'])


def _own_block(event):
    """One the owner put there for themselves, of at most a day: nobody else on it and not someone else's invite whose
    guests don't show. A longer one is a trip, and a trip is a commitment."""
    return not event['others'] and event['end'] - event['start'] <= dt.timedelta(days=1) and not any(
        _own_response(c['meta']) and not (c['meta'].get('organizer') or {}).get('self') for c in event['copies'])


def mark_frames(side):
    """'frame' on each of one side's meetings: an own block that holds meetings with others of the same side, or that
    does on two days of its series (an office day with no meeting in it is still one)."""
    days = {}
    for e in side:
        e['frame'] = _own_block(e) and any(m['others'] and e['start'] <= m['start'] and m['end'] <= e['end'] for m in side)
        if e['frame']:
            days[_series(e)] = days.get(_series(e), 0) + 1
    for e in side:
        e['frame'] = e['frame'] or days.get(_series(e), 0) >= 2 and _own_block(e)


def pairs(db, sides, current, owned, days=AHEAD_DAYS):
    """Every work event and personal event that overlap, neither started yet, soonest first: {'key', 'keys' (its copies'
    too), 'work', 'personal', 'start', 'end' (of the overlap), 'frame' (one is a frame, so no clash)}. Read AFTER past the
    window too: `due` says which are in it."""
    until = current + dt.timedelta(days=days)
    found = events(db, sides, current - BEFORE, until + AFTER, owned)
    both = {side: meetings(found, side) for side in SIDES}
    out = []
    for side in SIDES:
        mark_frames(both[side])
    personal = [e for e in both['personal'] if e['start'] > current]
    for w in both['work']:
        if w['start'] <= current:
            continue
        for p in personal:
            if p['start'] >= w['end']:
                break
            if p['end'] <= w['start'] or not (w['others'] or p['others']) or any(same_meeting(a, b) for a in w['copies'] for b in p['copies']):
                continue  # apart, two blocks the owner made alone, or one meeting on two calendars
            start = max(w['start'], p['start'])
            out.append({'key': clash_key(w, p), 'keys': {clash_key(a, b) for a in w['copies'] for b in p['copies']}, 'work': w, 'personal': p,
                        'start': start, 'end': min(w['end'], p['end']), 'frame': w['frame'] or p['frame'], 'due': start < until})
    return sorted(out, key=lambda c: c['start'])


def newer_side(clash):
    """The side whose event came in or changed last: the one that made the clash. Work on a tie."""
    w, p = (str(clash[s]['meta'].get('updated') or '') for s in SIDES)
    return 'personal' if p > w else 'work'


def grouped(clashes):
    """One group per to-do: {'about': the event, 'side': its side, 'others': what it overlaps, 'pairs', 'start'}, soonest
    first. The event that overlaps most goes first and takes all its overlaps, so an event is never on two lists for the
    same overlap; a pair on its own goes to its newer side."""
    left, out = list(clashes), []
    while left:
        count = {}
        for c in left:
            for side in SIDES:
                count.setdefault((side, c[side]['id']), []).append(c)
        (side, at), most = max(count.items(), key=lambda kv: (len(kv[1]), str(kv[1][0][kv[0][0]]['meta'].get('updated') or ''),
                                                              kv[0][0] == 'work', -kv[0][1]))
        if len(most) == 1:
            side, most = newer_side(left[0]), [left[0]]
        out.append({'about': most[0][side], 'side': side, 'others': [c[other_side(side)] for c in most], 'pairs': most,
                    'start': min(c['start'] for c in most)})
        taken = {id(c) for c in most}
        left = [c for c in left if id(c) not in taken]
    return sorted(out, key=lambda g: g['start'])


def due(group):
    return any(c['due'] for c in group['pairs'])


def once(clashes):
    """Each pair of series once, its soonest overlap; never one with a frame."""
    seen, out = set(), []
    for c in clashes:
        if not c['frame'] and not c['keys'] & seen:
            seen |= c['keys']
            out.append(c)
    return out


def find(db, sides, current, owned, days=AHEAD_DAYS):
    """Every clash ahead as it would be raised on a Machine that raised none yet: groups (grouped), soonest first. Only
    clashes that have not started yet (both events still ahead)."""
    return [g for g in grouped(once(pairs(db, sides, current, owned, days))) if due(g)]


def raised_today(db, since):
    """The clash to-dos made since then (an overlap that joined an older one is no new to-do)."""
    ensure(db)
    return db.execute('SELECT count(*) FROM (SELECT min(created_at) AS first FROM calendar_clashes WHERE suggestion_id IS NOT NULL '
                      'GROUP BY suggestion_id) WHERE first>=?', (since,)).fetchone()[0]


def keep(db, clash, side, suggestion_id, stamp):
    """This overlap is on that to-do, which is about its `side` event (None: no to-do, and never one). One already kept
    moves there."""
    ensure(db)
    db.execute('INSERT INTO calendar_clashes(dedupe_key,suggestion_id,event_id,other_id,side,starts_at,created_at) VALUES(?,?,?,?,?,?,?) '
               'ON CONFLICT(dedupe_key) DO UPDATE SET suggestion_id=excluded.suggestion_id,event_id=excluded.event_id,'
               'other_id=excluded.other_id,side=excluded.side',
               (clash['row']['dedupe_key'] if clash.get('row') else clash['key'], suggestion_id, clash[side]['id'], clash[other_side(side)]['id'],
                side, clash['start'].isoformat(), stamp))


def drop(db, clash):
    """This overlap is on no to-do any more: it turned out to be with a frame."""
    db.execute('UPDATE calendar_clashes SET suggestion_id=NULL WHERE dedupe_key=?', (clash['row']['dedupe_key'],))


def kept(db):
    """Every clash kept, with where its to-do is: 'open', 'closed' (done, dismissed or expired), or None (it has none, or
    it closed because its clash was gone)."""
    ensure(db)
    out = {}
    for r in db.execute('SELECT c.*,s.status,s.closed_decision_id FROM calendar_clashes c LEFT JOIN suggestions s ON s.id=c.suggestion_id ORDER BY c.created_at'):
        state = ('open' if r['status'] in todo_states.OPEN else
                 'closed' if r['status'] and not str(r['closed_decision_id'] or '').startswith(GONE) else None)
        out[r['dedupe_key']] = {**dict(r), 'state': state}
    return out


def really_new(event, since):
    """Whether an event was made or changed after `since` (the to-do it would come up next to)."""
    since = _at(since)
    return any((at := _at(c['meta'].get(k))) and since and at > since for c in event['copies'] for k in ('created', 'updated'))


def plan(db, found, untouched):
    """What a pass does with the overlaps now (pairs), given the to-dos there are: {'join': [(clash, side, to-do)],
    'quiet': [clash], 'drop': [clash], 'gone': [(to-do, why)], 'raise': [group]}, each group with the to-dos it replaces
    ('gone'). untouched(id) says the owner did nothing on a to-do yet: only such a one is taken over or closed. Reads
    only; the App does it (raise_clashes)."""
    rows = kept(db)
    known, fresh = [], []
    told = set(rows)
    for c in found:
        row = next((rows[k] for k in c['keys'] if k in rows), None)
        if row and {row['event_id'], row['other_id']} & c['work']['ids'] and {row['event_id'], row['other_id']} & c['personal']['ids']:
            known.append({**c, 'row': row})
        elif not row and not c['frame'] and not c['keys'] & told:
            told |= c['keys']  # its soonest overlap; a later one of the same two series is the same clash
            fresh.append(c)
    out = {'join': [], 'quiet': [], 'drop': [], 'gone': [], 'raise': []}
    about = {r['event_id']: r['suggestion_id'] for r in rows.values() if r['state'] == 'open'}
    closed = {}
    for r in rows.values():
        if r['state'] == 'closed':
            for i in (r['event_id'], r['other_id']):
                closed[i] = max(closed.get(i, ''), r['created_at'])

    def on(event, ids):
        return next((ids[i] for i in sorted(event['ids']) if i in ids), None)

    rest = []
    for c in fresh:
        side = next((s for s in SIDES if on(c[s], about)), None)
        if side:
            out['join'].append((c, side, on(c[side], about)))
        elif any(on(c[s], closed) and not really_new(c[other_side(s)], on(c[s], closed)) for s in SIDES):
            out['quiet'].append(c)
        else:
            rest.append(c)
    joined = {t for _, _, t in out['join']}
    free = {}  # the open to-dos the owner did nothing on: what each has now
    for c in known:
        if c['row']['state'] == 'open':
            free.setdefault(c['row']['suggestion_id'], []).append(c)
    free = {t: cs for t, cs in free.items() if untouched(t)}
    whole = {t: len(cs) == sum(r['suggestion_id'] == t for r in rows.values()) for t, cs in free.items()}
    for t, cs in list(free.items()):  # with a frame: no clash
        if whole[t] and t not in joined and all(c['frame'] for c in cs):
            out['gone'].append((t, 'frame'))
            about = {i: s for i, s in about.items() if s != t}
            del free[t]
        else:
            out['drop'] += [c for c in cs if c['frame']]
            free[t] = [c for c in cs if not c['frame']]
    for t, cs in list(free.items()):  # its one overlap is with an event that has a to-do of its own
        if len(cs) != 1 or not whole[t] or t in joined:
            continue
        side = other_side(cs[0]['row']['side'])
        to = on(cs[0][side], about)
        if to:
            out['join'].append((cs[0], side, to))
            out['gone'].append((t, 'moved'))
            about = {i: s for i, s in about.items() if s != t}
            joined.add(to)
            del free[t]
    open_now = [c for t, cs in free.items() if t not in joined and whole[t] for c in cs]
    for g in grouped(rest + open_now):
        if due(g) and not all(c.get('row') for c in g['pairs']):
            took = [id(c) for c in g['pairs']]
            out['raise'].append({**g, 'gone': [t for t, cs in free.items() if cs and all(id(c) in took for c in cs)]})
    return out


def annotate(db, cards):
    """card['clash'] on each open clash to-do, for the owner's own dashboard: the other side in full
    {'title', 'start', 'end', 'side'}, the rest of them in its 'more', soonest first. Read here, never stored on the
    to-do, so nothing that reads the to-do (a Fleet, a handoff, its preparation) sees it."""
    live = {c['id']: c for c in cards if c.get('status') not in todo_states.CLOSED and str(c.get('dedupe_key') or '').startswith('clash:')}
    if not live:
        return
    try:
        rows = db.execute(f"SELECT c.suggestion_id,c.side,e.title,e.occurred_at,e.metadata FROM calendar_clashes c JOIN events e ON e.id=c.other_id "
                          f"WHERE e.deleted=0 AND c.suggestion_id IN ({','.join('?' * len(live))}) ORDER BY e.occurred_at,e.id", list(live)).fetchall()
    except sqlite3.OperationalError:  # no clash raised on this Machine yet
        return
    for r in rows:
        try:
            end = json.loads(r['metadata'] or '{}').get('end_at')
        except ValueError:
            end = None
        if not end:
            continue
        card = live[r['suggestion_id']]
        other = {'title': r['title'], 'start': r['occurred_at'], 'end': end, 'side': other_side(r['side'])}
        if card.get('clash'):
            card['clash'].setdefault('more', []).append(other)
        else:
            card['clash'] = other

"""The desktop robot (desktop/) as a place a notification goes: while it is there on a computer, it shows a to-do's
notification in a small bubble instead of that computer's browser or installed app, never next to it.

It has no channel of its own: the robot asks api/status every half minute anyway (look=1), says which desk it is and
whether it may speak (desk=, up=1), and gets what waits for it with the answer. Whether something notifies at all is
decided before this (deliver.py, notify.py, push_send): hours, the day's cap, calm, a dashboard in use, the kinds the
owner turned off. Here only where it shows: a notification that would buzz, of one to-do, goes to the desks that are up
and not to the browsers of those computers. Phones and other computers get theirs as ever.

Which browser is on the robot's computer: the robot opens the dashboard with ?desk=<its random id>, and the page says
it with its own push subscription (push_desk; none is fine: nothing to stand in for). A robot whose computer isn't
known yet stays quiet while a browser that may be on it has notifications on: better one notification than two. A phone
or a browser on another system isn't. The app without its robot asks the person about the rest (none=): those on until
then are not on its computer.

What it got it names in its next look (got=); until then it gets it again, as an answer can be lost on the way. A
notification it doesn't name in LATE seconds (the computer slept, the robot went quiet or away) goes to that computer's
browser after all (late). On a computer whose browser has no notifications on it waits KEEP seconds for the robot. What waits for a desk is in memory only, ids and no text: the robot asks api/notice for the
words, as the phone app does, so hidden text stays hidden and what no longer waits shows nothing."""
import datetime as dt
import re
import secrets
import sqlite3
import threading

import meet
import meeting_prep
import notify
import security_levels

ID = re.compile(r'[a-f0-9]{32}')
TODO = re.compile(r'[a-f0-9]{16}')
LEASE = 75  # seconds after its last look a robot counts as there (it looks every 30)
LATE = 90   # seconds a notification waits for its robot to have it before that computer's browser gets it
KEEP = 15 * 60  # seconds it waits when there is no browser to get it instead
DESKS = 8   # robots at once; a longer-gone one gives way
LINKS = 40  # known pairs of a robot and a browser
SOON = 10 * 60  # seconds before a meeting the robot says so
COMPUTERS = ('mac', 'windows', 'linux', 'other')  # what a browser with notifications on runs on (other: a phone)
SCHEMA = ('CREATE TABLE IF NOT EXISTS notify_desks(desk TEXT NOT NULL,endpoint TEXT NOT NULL,at TEXT NOT NULL,'
          'PRIMARY KEY(desk,endpoint))')
_lock = threading.Lock()
_desks = {}  # id -> {'at', 'up', 'on', 'none', 'waiting': [{'key', 'id', 'kind', 'at', 'payload', 'instead'}]}


def reset():
    with _lock:
        _desks.clear()


def computer(agent):
    """The system a browser runs on, of COMPUTERS, by its User-Agent. An iPad can say it is a Mac."""
    agent = str(agent or '')
    if re.search(r'Android|iPhone|iPad|iPod|Mobi|CrOS', agent):
        return 'other'
    return next((name for name, word in (('mac', 'Macintosh'), ('windows', 'Windows'), ('linux', 'Linux')) if word in agent), None)


def look(desk, up, got=(), clock=notify.wall, on='', none=''):
    """The robot asked for the status: it is there, whether it may speak now (up), and the keys of what it got before.
    What else waits for it: [{'key', 'id', 'kind'}]. on: its computer's system, of COMPUTERS; none: the person said the
    browsers `maybe` asked about then are not on it."""
    if not ID.fullmatch(str(desk or '')):
        return []
    at = clock()
    with _lock:
        row = _desks.pop(desk, None) or {'waiting': []}
        for gone in list(_desks)[:max(0, len(_desks) - DESKS + 1)]:  # the longest unseen first
            del _desks[gone]
        _desks[desk] = row
        row['at'], row['up'] = at, bool(up)
        row['on'] = on if on in COMPUTERS else ''
        row['none'] = int(none) if re.fullmatch(r'[0-9]{1,12}', str(none)) else 0
        row['waiting'] = [w for w in row['waiting'] if w['key'] not in got]
        there = [w for w in row['waiting'] if up and not _over(w, at)]  # later ones are the browser's now (late)
    return [{k: w[k] for k in ('key', 'id', 'kind')} for w in there]


def had(desk, got):
    """The to-dos of the notifications this robot says it got (look's got)."""
    with _lock:
        return [w['id'] for w in (_desks.get(desk) or {'waiting': ()})['waiting'] if w['key'] in got]


def link(db, desk, endpoint, at):
    """A page the robot opened says which push subscription its browser has ('' for none)."""
    if not ID.fullmatch(str(desk or '')):
        raise ValueError('Invalid push subscription')
    db.execute(SCHEMA)
    if endpoint:  # it has one now: no longer a browser without
        db.execute("DELETE FROM notify_desks WHERE desk=? AND endpoint=''", (desk,))
    db.execute('INSERT INTO notify_desks(desk,endpoint,at) VALUES(?,?,?) ON CONFLICT(desk,endpoint) DO UPDATE SET at=excluded.at', (desk, endpoint, at))
    db.execute('DELETE FROM notify_desks WHERE rowid NOT IN (SELECT rowid FROM notify_desks ORDER BY at DESC LIMIT ?)', (LINKS,))


def up(clock=notify.wall):
    """The robots there now that may speak."""
    at = clock()
    with _lock:
        return [d for d, row in _desks.items() if row['up'] and at - row['at'] < LEASE]


def here(db, clock=notify.wall):
    """The robots that may stand in now: {id: {its computer's push endpoints}}. One whose computer isn't known counts
    only while no browser that may be on it has notifications on."""
    there = up(clock)
    if not there:
        return {}
    found = _known(db, there)
    return found | {d: set() for d in there if d not in found and not maybe(db, d)}


def _known(db, desks):
    try:
        rows = db.execute(f"SELECT desk,endpoint FROM notify_desks WHERE desk IN ({','.join('?' * len(desks))})", desks).fetchall()
    except sqlite3.OperationalError:  # no robot ever opened the dashboard
        rows = []
    found = {}
    for desk, endpoint in rows:
        found.setdefault(desk, set()).update({endpoint} if endpoint else ())
    return found


def maybe(db, desk):
    """Whether a browser with notifications on may be on this robot's computer, which isn't known: 0, or the second the
    newest was turned on (for none=). Not one on another system, nor one of another robot's computer that is there."""
    with _lock:
        row, others = _desks.get(desk) or {}, [d for d in _desks if d != desk]
    if _known(db, [desk]):
        return 0
    theirs = set().union(*_known(db, others).values())
    newest = 0
    for endpoint, created, runs in db.execute('SELECT endpoint,created_at,computer FROM push_subscriptions').fetchall():
        at = int(dt.datetime.fromisoformat(created).timestamp())
        if endpoint not in theirs and at > row.get('none', 0) and (not runs or not row.get('on') or runs == row['on']):
            newest = max(newest, at)
    return newest


def speaks(payload, kind):
    """Whether a push is one the robot shows: one to-do's, with a buzz. The digest, the Fleet and a batch's quiet ones
    stay where they are."""
    return bool(kind) and not payload.get('silent') and bool(TODO.fullmatch(str(payload.get('tag') or '')))


def stand_in(db, subscriptions, payload, kind, clock=notify.wall):
    """The browsers this push still goes to, and how many robots show it instead of theirs."""
    desks = here(db, clock) if speaks(payload, kind) else {}
    at, count, taken = clock(), 0, set()
    for desk, endpoints in desks.items():
        with _lock:
            row = _desks.get(desk)
            if not row:
                continue
            row['waiting'] = [w for w in row['waiting'] if w['id'] != payload['tag']]  # a newer one replaces it, as a push does
            row['waiting'].append({'key': secrets.token_hex(4), 'id': payload['tag'], 'kind': kind, 'at': at, 'payload': payload,
                                   'instead': [s for s in subscriptions if s['endpoint'] in endpoints]})
        count += 1
        taken |= endpoints
    return [s for s in subscriptions if s['endpoint'] not in taken], count


def _over(waits, at):
    return at - waits['at'] >= (LATE if waits['instead'] else KEEP)


def late(clock=notify.wall):
    """What no robot had in time, or whose robot went quiet: [(subscriptions, payload)] to push after all."""
    at, out = clock(), []
    with _lock:
        for row in _desks.values():
            old = [w for w in row['waiting'] if _over(w, at) or w['instead'] and not row['up']]
            row['waiting'] = [w for w in row['waiting'] if w not in old]
            out += [(w['instead'], w['payload']) for w in old if w['instead']]
    return out


def meeting(db, current, owner, gone):
    """The next meeting The Machine wrote a briefing for (meeting_prep.py) that starts within SOON, for the robot to
    say: {'id': its briefing to-do, 'event', 'at', 'who', 'others', 'title', 'join'}, or None. Off with push for
    reminders. who: the first guest from outside by first name, with how many others; title: the meeting's own name. Both
    '' when there is none, and with notification text off. join: a known video service's
    own link in the event (meet.video_link). owner: the owner's emails and domains, called only when there is one; gone:
    to-do states whose briefing the owner didn't want."""
    if not notify.allowed(db, 'reminder', 'push'):
        return None
    try:
        rows = db.execute("SELECT m.suggestion_id,e.id,e.title,e.body,e.occurred_at,e.metadata,s.status FROM meeting_preps m "
                          "JOIN events e ON e.id=m.event_id JOIN suggestions s ON s.id=m.suggestion_id WHERE m.verdict='made' "
                          'AND e.deleted=0 AND e.occurred_at>? AND e.occurred_at<=? ORDER BY e.occurred_at,e.id',
                          (current.isoformat(), (current + dt.timedelta(seconds=SOON)).isoformat())).fetchall()
    except sqlite3.OperationalError:  # no meeting prepared yet
        return None
    for row in rows:
        start, meta = meeting_prep.start_if_on(row['occurred_at'], row['metadata'])
        if not start or row['status'] in gone:
            continue
        who, others, title = '', 0, ''
        if security_levels.notify_text(db, True):
            guests = meeting_prep.outside_guests(meta, *owner())
            named = [g['name'].split()[0] for g in guests if g['name'] and '@' not in g['name']]
            who, others = (named[0], len(guests) - 1) if named else ('', 0)
            title = ' '.join(str(row['title'] or '').split())[:60]
        return {'id': row['suggestion_id'], 'event': row['id'], 'at': start.isoformat(), 'who': who, 'others': others, 'title': title,
                'join': meet.video_link(' '.join(str(x or '') for x in (meta.get('location'), meta.get('video'), row['body'])))}
    return None

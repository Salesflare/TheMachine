"""Scheduling between Machines: two people who each have a Machine, and are not in the same Fleet, find a meeting time
over The Machine Network (docs/scheduling-between-machines.md).

The proposer's Machine looks the other person up by a hash of their address (the cloud's `meet` route), asks their
Machine for free times in a window, picks a slot that fits both and sends it. Each owner gets one to-do with Book it,
Other time and Not needed. The proposer's Machine books (its owner's calendar, an invite for the other person) only
once both owners tapped Book it. Anything that doesn't work out (no Machine, no answer within ANSWER_WAIT, a refusal,
too many rounds) leaves the proposer's to-do as it was: today's email draft with times.

What leaves this Machine, and when:
- Answering: free times only, within the asked window (at most MAX_DAYS), inside the owner's work hours, busy times
  widened by their buffer and to the GRID. Never what, where or with whom; private events are busy like any other.
  Only when the owner's setting allows it (security_levels 'meet_asks'), the asker is a Machine the cloud verified, and
  the owner's own mail shows an exchange both ways with one of the asker's verified addresses. Rate-limited.
- Proposing: one slot. At the Careful level only after the owner's own Book it.
- Booking: only after both taps, through the app's own calendar write (meet_book), which sends the invite.

Every message is sealed for the other Machine (network_crypto), bound to who sends what to whom and the message id;
the cloud only routes. A peer's keys are pinned the first time they're seen. Every exchange is a line in Activity
(Calendar), without event details. What a peer sends is data in a fixed shape, never read by a model.

The app wires it (meet_on, meet_card, meet_book, meet_close, meet_thread); unwired, this Machine neither asks nor
tells the cloud it can be asked."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import re
import secrets

import activity_log
import network_crypto as nc
import security_levels
from i18n import t

LOG = logging.getLogger('personal-assistant')
KIND = 'meet'
ALLOW = ('freebusy', 'off')
MAX_DAYS = 14            # the widest window anyone may ask about
AHEAD_DAYS = 60          # a window starts within this many days
GRID = 15                # minutes: every time that leaves this Machine is on this grid
LEAD = 60                # minutes from now before the first free time offered
LATEST = '18:00'         # meetings end by then, also when work hours run later (they are the notification hours too)
ANSWER_WAIT = 180        # seconds the proposer waits for free times before it keeps the email draft
ROUNDS = 3               # Other time this often, then the email draft
MAX_SLOTS = 200          # free times in one answer
PEER_PER_DAY = 6         # asks answered from one person a day
ALL_PER_DAY = 40         # asks answered a day
STARTS_PER_DAY = 20      # times this Machine asks others a day
INBOX_EVERY = 120        # seconds between inbox looks when the Fleet inbox gave no hint
KEEP_DAYS = 30
LENGTHS = (15, 30, 45, 60, 90)
BUFFERS = (0, 5, 10, 15, 30)
PREFER = ('any', 'morning', 'afternoon')
DEFAULTS = {'minutes': 30, 'buffer': 10, 'prefer': 'any'}
VIDEO = {'zoom': 'Zoom', 'meet': 'Google Meet', 'teams': 'Teams'}
VIDEO_LINKS = {'zoom': ('zoom.us/',), 'meet': ('meet.google.com/',), 'teams': ('teams.microsoft.com/', 'teams.live.com/')}
TYPES = {'asker': ('free', 'no', 'ok', 'other', 'cancel'), 'answerer': ('propose', 'booked', 'cancel')}
SESSION = re.compile(r'[a-f0-9]{32}')
PEER = re.compile(r'mt_[A-Za-z0-9_-]{8,40}')
SLOT = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z')
DAY = re.compile(r'\d{4}-\d{2}-\d{2}')
SCHEMA = '''
CREATE TABLE IF NOT EXISTS meet_sessions(id TEXT NOT NULL,peer TEXT NOT NULL,role TEXT NOT NULL,keys TEXT,email TEXT,name TEXT,
  card_id TEXT,state TEXT NOT NULL,start TEXT NOT NULL,days INTEGER NOT NULL,minutes INTEGER NOT NULL,free TEXT,prefer TEXT,
  slot TEXT,video TEXT,round INTEGER NOT NULL DEFAULT 0,rejected TEXT NOT NULL DEFAULT '[]',mine_ok INTEGER NOT NULL DEFAULT 0,
  their_ok INTEGER NOT NULL DEFAULT 0,sent INTEGER NOT NULL DEFAULT 0,note TEXT,deadline TEXT,created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,PRIMARY KEY(id,peer));
CREATE INDEX IF NOT EXISTS meet_sessions_card ON meet_sessions(card_id);
CREATE TABLE IF NOT EXISTS meet_seen(msg TEXT PRIMARY KEY,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS meet_pins(peer TEXT PRIMARY KEY,fingerprint TEXT NOT NULL,first_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS meet_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS meet_log(id INTEGER PRIMARY KEY,at TEXT NOT NULL,direction TEXT NOT NULL,peer TEXT,name TEXT,
  what TEXT NOT NULL,args TEXT NOT NULL,outcome TEXT NOT NULL,card_id TEXT);
'''


def ensure(db):
    db.executescript(SCHEMA)


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp(moment=None):
    return (moment or now()).isoformat(timespec='seconds')


def email_hash(address):
    """What the cloud is asked about: never the address itself."""
    return hashlib.sha256(b'tm-meet/1\n' + str(address or '').strip().lower().encode()).hexdigest()


# -- times, plain code

def slot_text(moment):
    return moment.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def parse_slot(value):
    if not isinstance(value, str) or not SLOT.fullmatch(value):
        return None
    try:
        moment = dt.datetime.strptime(value, '%Y-%m-%dT%H:%MZ').replace(tzinfo=dt.timezone.utc)
    except ValueError:
        return None
    return moment if moment.minute % GRID == 0 else None


def floor_grid(moment):
    moment = moment.astimezone(dt.timezone.utc).replace(second=0, microsecond=0)
    return moment - dt.timedelta(minutes=moment.minute % GRID)


def ceil_grid(moment):
    down = floor_grid(moment)
    return down if down == moment.astimezone(dt.timezone.utc) else down + dt.timedelta(minutes=GRID)


def parse_window(start, days, today=None):
    """A window in its fixed form ({start: a day, days: 1 to MAX_DAYS}, starting from today up to AHEAD_DAYS ahead),
    else None."""
    today = today or now().date()
    if not isinstance(start, str) or not DAY.fullmatch(start) or not isinstance(days, int) or isinstance(days, bool):
        return None
    try:
        first = dt.date.fromisoformat(start)
    except ValueError:
        return None
    if not 1 <= days <= MAX_DAYS or not today - dt.timedelta(days=1) <= first <= today + dt.timedelta(days=AHEAD_DAYS):
        return None
    return {'start': start, 'days': days}


def _clock(value, default):
    try:
        hour, minute = (int(x) for x in str(value or default).split(':'))
        return dt.time(hour, minute) if (hour, minute) <= (23, 59) else dt.time(23, 59)
    except ValueError:
        return dt.time(*map(int, default.split(':')))


def busy_blocks(busy, buffer=0):
    """Busy blocks ([[start, end]] UTC slots, as friends.free_busy gives them) widened by the buffer and outward to
    the grid, merged: [(start, end)] as datetimes."""
    out = []
    for pair in busy or []:
        try:
            a = dt.datetime.strptime(pair[0], '%Y-%m-%dT%H:%MZ').replace(tzinfo=dt.timezone.utc)
            b = dt.datetime.strptime(pair[1], '%Y-%m-%dT%H:%MZ').replace(tzinfo=dt.timezone.utc)
        except (TypeError, ValueError, IndexError):
            continue
        out.append((floor_grid(a - dt.timedelta(minutes=buffer)), ceil_grid(b + dt.timedelta(minutes=buffer))))
    out.sort()
    merged = []
    for a, b in out:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


def free_times(busy, window, hours, tz, buffer=0, prefer='any', current=None):
    """(free, preferred): the owner's free times in the window, as [[start, end]] UTC slots on the grid. Only on their
    work days, within their work hours and by LATEST, after busy blocks widened by the buffer, from LEAD minutes after
    now. preferred is the part of those in the owner's preferred part of the day."""
    blocks = busy_blocks(busy, buffer)
    earliest = ceil_grid((current or now()) + dt.timedelta(minutes=LEAD))
    days = hours.get('days') or [1, 2, 3, 4, 5]
    opens, closes = _clock(hours.get('start'), '09:00'), min(_clock(hours.get('end'), LATEST), _clock(LATEST, LATEST))
    free, liked = [], []
    first = dt.date.fromisoformat(window['start'])
    for n in range(window['days']):
        day = first + dt.timedelta(days=n)
        if day.isoweekday() not in days:
            continue
        cursor = max(dt.datetime.combine(day, opens, tz).astimezone(dt.timezone.utc), earliest)
        close = dt.datetime.combine(day, closes, tz).astimezone(dt.timezone.utc)
        noon = dt.datetime.combine(day, dt.time(12), tz).astimezone(dt.timezone.utc)
        spans = []
        for a, b in blocks:
            if b <= cursor or a >= close:
                continue
            if a > cursor:
                spans.append((cursor, a))
            cursor = max(cursor, b)
        if close > cursor:
            spans.append((cursor, close))
        for a, b in spans:
            a, b = ceil_grid(a), floor_grid(b)
            if (b - a).total_seconds() < GRID * 60:
                continue
            free.append([slot_text(a), slot_text(b)])
            part = (a, min(b, noon)) if prefer == 'morning' else (max(a, noon), b) if prefer == 'afternoon' else (a, b)
            if (part[1] - part[0]).total_seconds() >= GRID * 60:
                liked.append([slot_text(part[0]), slot_text(part[1])])
    return free[:MAX_SLOTS], liked[:MAX_SLOTS]


def clean_times(value, window):
    """A peer's free times: [[start, end]] UTC slots on the grid, inside the window asked, at most MAX_SLOTS. Anything
    else is dropped."""
    if not isinstance(value, list):
        return []
    first = dt.datetime.combine(dt.date.fromisoformat(window['start']), dt.time(), dt.timezone.utc) - dt.timedelta(hours=14)
    last = first + dt.timedelta(days=window['days'], hours=28)
    out = []
    for pair in value[:MAX_SLOTS]:
        if not isinstance(pair, list) or len(pair) != 2:
            continue
        a, b = parse_slot(pair[0]), parse_slot(pair[1])
        if a and b and first <= a < b <= last:
            out.append([slot_text(a), slot_text(b)])
    return sorted(out)


def _spans(times):
    return [(parse_slot(a), parse_slot(b)) for a, b in times or [] if parse_slot(a) and parse_slot(b)]


def _inside(spans, a, b):
    return any(x <= a and b <= y for x, y in spans)


def pick(mine, theirs, minutes, liked_mine=(), liked_theirs=(), rejected=()):
    """The first start, on the grid, where both are free for `minutes`: one both prefer first, then one either prefers,
    then the earliest. Never a rejected one. [start, end] or None."""
    length = dt.timedelta(minutes=minutes)
    mine_s, theirs_s = _spans(mine), _spans(theirs)
    like_a, like_b = _spans(liked_mine), _spans(liked_theirs)
    best = None
    for a, b in mine_s:
        for c, d in theirs_s:
            start, end = max(a, c), min(b, d)
            cursor = ceil_grid(start)
            while cursor + length <= end:
                if slot_text(cursor) not in rejected:
                    score = 2 - _inside(like_a, cursor, cursor + length) - _inside(like_b, cursor, cursor + length)
                    if best is None or (score, cursor) < best[:2]:
                        best = (score, cursor)
                cursor += dt.timedelta(minutes=GRID)
    return [slot_text(best[1]), slot_text(best[1] + length)] if best else None


def video_habit(db, owner=(), days=90):
    """The video link the owner's own recent meetings use most (zoom, meet, teams), else None. Read from the links in
    their calendar events; nothing leaves."""
    since = stamp(now() - dt.timedelta(days=days))
    counts = dict.fromkeys(VIDEO, 0)
    try:
        rows = db.execute("SELECT metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND occurred_at>=? ORDER BY occurred_at DESC LIMIT 400",
                          (since,)).fetchall()
    except Exception:  # noqa: BLE001 - no events table yet
        return None
    for row in rows:
        text = (row[0] or '').lower()
        for kind, marks in VIDEO_LINKS.items():
            if any(m in text for m in marks):
                counts[kind] += 1
                break
    kind = max(counts, key=counts.get)
    return kind if counts[kind] else None


def when_text(moment, tz):
    import locale_prefs
    local = moment.astimezone(tz)
    if (local.date() - now().astimezone(tz).date()).days < 6:
        return locale_prefs.short_text(local)
    return locale_prefs.day_text(local) + ' ' + locale_prefs.clock_text(local)


def window_text(window):
    import locale_prefs
    first = dt.date.fromisoformat(window['start'])
    last = first + dt.timedelta(days=window['days'] - 1)
    return locale_prefs.day_text(first, weekday=False) if window['days'] == 1 else locale_prefs.span_text(first, last)


def todo_title(name):
    """'Meet Alex Example': what the to-do says on both sides. The time, length and video link are its line below."""
    return t('Meet {}', ' '.join(str(name or '').split())[:80] or t('someone'))


# -- the Activity lines, in the owner's language when read (no event details: a window, a slot, a name)
LINES = {
    'asked': ('out', 'Free times asked from {}: {}'),
    'asked_in': ('in', 'Free times asked by {}: {}'),
    'proposed': ('out', 'Time proposed to {}: {}'),
    'proposed_in': ('in', 'Time proposed by {}: {}'),
    'booked': ('out', 'Meeting booked with {}: {}'),
    'booked_in': ('in', 'Meeting booked by {}: {}'),
    'other': ('out', 'Another time asked from {}: {}'),
    'other_in': ('in', 'Another time asked by {}: {}'),
    'canceled': ('out', 'Meeting not needed with {}: {}'),
    'canceled_in': ('in', 'Meeting not needed for {}: {}'),
    'fallback': ('out', 'Email draft kept for {}: {}'),
}
OUTCOMES = {  # code -> (Activity outcome, status, detail)
    'answered': ('done', 'Answered', None),
    'sent': ('done', 'Sent', None),
    'booked': ('done', 'Booked', None),
    'waiting': ('pending', 'Waiting for them', None),
    'off': ('refused', 'Refused', 'Off in your settings'),
    'thread': ('refused', 'Refused', 'No email exchange with them'),
    'limit': ('refused', 'Refused', 'Too many asks today'),
    'window': ('refused', 'Refused', 'Window too wide'),
    'keys': ('refused', 'Refused', 'Their Machine’s keys changed'),
    'no_machine': ('refused', 'No Machine', 'No Machine found for them'),
    'no_answer': ('refused', 'No answer', 'Their Machine didn’t answer in time'),
    'declined': ('refused', 'Declined', None),
    'no_slot': ('refused', 'No time found', 'No time fits you both'),
    'rounds': ('refused', 'No time found', 'Too many other times'),
    'passed': ('refused', 'Time passed', None),
    'failed': ('failed', 'Failed', None),
    'canceled': ('undone', 'Canceled', None),
}


def activity_lines(db, limit):
    """Activity, Calendar: each exchange, newest first."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='meet_log'").fetchone():
        return []
    out = []
    titled = db.execute("SELECT 1 FROM sqlite_master WHERE name='suggestions'").fetchone()  # the to-do's title, for its link
    query = ('SELECT l.*,s.title AS todo_title FROM meet_log l LEFT JOIN suggestions s ON s.id=l.card_id' if titled
             else 'SELECT l.*,NULL AS todo_title FROM meet_log l')
    for r in db.execute(query + ' ORDER BY l.id DESC LIMIT ?', (limit,)):
        line = LINES.get(r['what'])
        outcome, status, detail = OUTCOMES.get(r['outcome'], OUTCOMES['failed'])
        if not line:
            continue
        args = json.loads(r['args'] or '[]')
        out.append({'id': f"meet:{r['id']}", 'kind': 'calendar', 'at': r['at'], 'what': t(line[1], r['name'] or t('someone'), *args[:1]),
                    'where': t('The Machine Network'), 'outcome': outcome, 'status': t(status), 'by': None,
                    'todo': {'id': r['card_id'], 'title': ' '.join(str(r['todo_title']).split())[:120]} if r['card_id'] and r['todo_title'] is not None else None, 'detail': t(detail) if detail else None})
    return out


activity_log.register('calendar', activity_lines)


class Meet:
    """Mixed into fleet.Fleet: scheduling with Machines outside the owner's Fleets. Set by the app:

    - meet_on: True once the app wires the rest; until then nothing is asked or answered.
    - meet_card(session) -> card id: a new to-do for a time another Machine proposed (the other side's to-do).
    - meet_book(session) -> {'status': 'done'|'failed'|...}: the calendar write with the invite, after both taps.
    - meet_close(card_id, why): closes a to-do this flow made or settled.
    - meet_thread(addresses) -> bool: the owner's mail shows an exchange both ways with one of them (default: the Graph).
    - meet_hours() -> {'days', 'start', 'end'} and meet_tz() -> tzinfo: the owner's work hours and time zone.
    """
    meet_on = False
    meet_card = meet_book = meet_close = meet_thread = meet_hours = meet_tz = None
    meet_clock = None  # tests: () -> aware datetime

    # -- state
    def _meet_now(self):
        return self.meet_clock() if self.meet_clock else now()

    def _meet_db(self):
        db = self.connect()
        return db

    def meet_setting(self):
        with self.connect() as db:
            ensure(db)
            allow = security_levels.pref(db, 'meet_asks')
            prefs = {r['key']: r['value'] for r in db.execute('SELECT key,value FROM meet_prefs')}
        out = dict(DEFAULTS)
        for key, choices in (('minutes', LENGTHS), ('buffer', BUFFERS)):
            try:
                out[key] = int(prefs[key]) if int(prefs.get(key, -1)) in choices else out[key]
            except ValueError:
                pass
        out['prefer'] = prefs.get('prefer') if prefs.get('prefer') in PREFER else out['prefer']
        return {'allow': allow, **out}

    def meet_set(self, allow=None, minutes=None, buffer=None, prefer=None):
        """The owner's setting: who may ask (free/busy or off) and their meeting preferences."""
        with self.connect() as db:
            ensure(db)
            if allow is not None:
                if allow not in ALLOW:
                    raise ValueError('Pick Free/busy for scheduling or Off')
                security_levels.set_pref(db, 'meet_asks', allow)
            for key, value, choices in (('minutes', minutes, LENGTHS), ('buffer', buffer, BUFFERS), ('prefer', prefer, PREFER)):
                if value is None:
                    continue
                if value not in choices:
                    raise ValueError('Pick one of the choices shown')
                db.execute('INSERT INTO meet_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, str(value)))
        if allow is not None:
            self.set_meta('meet_told', None)  # the cloud hears it on the next round
            try:
                self.meet_tell()
            except Exception as error:  # noqa: BLE001 - away: told on the next round
                LOG.info('meet setting not told yet error=%s', type(error).__name__)
        return self.meet_setting()

    def _meet_log(self, db, what, name, args, outcome, peer=None, card_id=None):
        db.execute('INSERT INTO meet_log(at,direction,peer,name,what,args,outcome,card_id) VALUES(?,?,?,?,?,?,?,?)',
                   (stamp(self._meet_now()), LINES[what][0], peer, ' '.join(str(name or '').split())[:80], what, json.dumps(list(args)), outcome, card_id))
        db.execute('DELETE FROM meet_log WHERE id NOT IN (SELECT id FROM meet_log ORDER BY id DESC LIMIT 1000)')

    def _meet_tz(self):
        if self.meet_tz:
            return self.meet_tz()
        local = (self.hours or {}).get('local_now')
        return local().tzinfo if local else dt.timezone.utc

    def _meet_hours(self):
        if self.meet_hours:
            return self.meet_hours()
        return {**{'days': [1, 2, 3, 4, 5], 'start': '09:00', 'end': LATEST}, **(self.config.get('work_hours') or {})}

    def _sealing(self):
        relay = self.relay
        return relay if getattr(relay, 'private', None) and hasattr(relay, 'send_or_keep') else None

    def _careful(self, db):
        return security_levels.label(db) == 'careful' or bool(security_levels.careful_fleets(db))

    # -- the cloud
    def meet_tell(self):
        """Tells the cloud what the owner allows (and gets this Machine's scheduling id). Once a day, or after a change."""
        if not self.meet_on or not self._sealing():
            return None
        allow = self.meet_setting()['allow']
        told = self.meta('meet_told') or {}
        if told.get('allow') == allow and told.get('at', '') > stamp(self._meet_now() - dt.timedelta(days=1)) and self.meta('meet_id'):
            return self.meta('meet_id')
        found = self.relay.call('POST', '/meet', {'op': 'allow', 'allow': allow}, timeout=20)
        if isinstance(found, dict) and PEER.fullmatch(str(found.get('id') or '')):
            self.set_meta('meet_id', found['id'])
        self.set_meta('meet_told', {'allow': allow, 'at': stamp(self._meet_now())})
        return self.meta('meet_id')

    def _meet_send(self, row, payload):
        """One sealed message to the peer's Machine, through the outbox (sent again while the Network is away)."""
        sealing = self._sealing()
        me = self.meta('meet_id') or self.meet_tell()
        if not sealing or not me:
            raise ValueError('This Machine is not on The Machine Network')
        msg = secrets.token_hex(16)
        body = {**payload, 's': row['id']}
        env = nc.seal(body, sealing.private, json.loads(row['keys']), {'p': 'meet', 'k': KIND, 'f': me, 't': row['peer'], 'r': msg})
        return sealing.send_or_keep('POST', '/meet', {'op': 'send', 'to': row['peer'], 'id': msg, 'sealed': env}, 'meet:' + msg, 20)

    # -- the proposer
    def meet_start(self, card_id, email, name='', minutes=None, start=None, days=None):
        """A meeting request on a to-do: ask the other person's Machine, if they have one. Returns the state: asked, or
        fallback (the to-do keeps its email draft)."""
        if not self.meet_on or not self._sealing():
            return 'fallback'
        email = str(email or '').strip().lower()
        current = self._meet_now()
        tz = self._meet_tz()
        setting = self.meet_setting()
        minutes = minutes if minutes in LENGTHS else setting['minutes']
        today = current.astimezone(tz).date()
        window = parse_window(start or (today + dt.timedelta(days=1)).isoformat(), days if isinstance(days, int) else 7, today) \
            or {'start': (today + dt.timedelta(days=1)).isoformat(), 'days': 7}
        with self.connect() as db:
            ensure(db)
            open_ = db.execute("SELECT state FROM meet_sessions WHERE card_id=? AND role='asker' ORDER BY created_at DESC LIMIT 1", (str(card_id),)).fetchone()
            if open_:
                return open_['state']
            started = db.execute("SELECT COUNT(*) FROM meet_sessions WHERE role='asker' AND created_at>?", (stamp(current - dt.timedelta(days=1)),)).fetchone()[0]
        session = {'id': secrets.token_hex(16), 'peer': '-', 'keys': None, 'email': email, 'name': name, 'card_id': str(card_id)}
        found = None
        if started < STARTS_PER_DAY and '@' in email:
            try:
                found = self.relay.call('POST', '/meet', {'op': 'find', 'hash': email_hash(email)}, timeout=20)
            except Exception as error:  # noqa: BLE001 - the Network away, too many lookups, an older cloud: the email draft
                LOG.info('meet find error=%s', type(error).__name__)
        found = (found or {}).get('found') if isinstance(found, dict) else None
        keys = found.get('keys') if isinstance(found, dict) else None
        checked = nc.check_keys(keys) if keys else None
        if not (isinstance(found, dict) and PEER.fullmatch(str(found.get('id') or '')) and checked):
            self._meet_save(session, 'fallback', window, minutes, note='no_machine')
            return 'fallback'
        session.update(peer=found['id'], keys=json.dumps(keys), name=name or ' '.join(str(found.get('name') or '').split())[:80])
        if not self._meet_pin(found['id'], checked['fingerprint']):
            self._meet_save(session, 'fallback', window, minutes, note='keys')
            return 'fallback'
        self._meet_save(session, 'asked', window, minutes, deadline=stamp(current + dt.timedelta(seconds=ANSWER_WAIT)))
        try:
            self._meet_send(session, {'t': 'ask', 'start': window['start'], 'days': window['days'], 'minutes': minutes})
        except Exception as error:  # noqa: BLE001
            LOG.info('meet ask not sent error=%s', type(error).__name__)
            self._meet_state(session['id'], session['peer'], 'fallback', note='failed')
            return 'fallback'
        with self.connect() as db:
            self._meet_log(db, 'asked', session['name'], [window_text(window)], 'waiting', session['peer'], session['card_id'])
        return 'asked'

    def _meet_save(self, s, state, window, minutes, note=None, deadline=None):
        at = stamp(self._meet_now())
        with self.connect() as db:
            ensure(db)
            db.execute('INSERT INTO meet_sessions(id,peer,role,keys,email,name,card_id,state,start,days,minutes,note,deadline,created_at,updated_at) '
                       "VALUES(?,?,'asker',?,?,?,?,?,?,?,?,?,?,?,?)",
                       (s['id'], s['peer'], s['keys'], s['email'], s['name'], s['card_id'], state, window['start'], window['days'], minutes,
                        note, deadline, at, at))
            if state == 'fallback':
                self._meet_log(db, 'fallback', s['name'] or s['email'], [window_text(window)], note or 'failed', None, s['card_id'])

    def _meet_state(self, sid, peer, state, **fields):
        with self.connect() as db:
            sets = ', '.join(f'{k}=?' for k in fields)
            db.execute(f'UPDATE meet_sessions SET state=?,updated_at=?{", " + sets if sets else ""} WHERE id=? AND peer=?',
                       (state, stamp(self._meet_now()), *fields.values(), sid, peer))
            row = db.execute('SELECT * FROM meet_sessions WHERE id=? AND peer=?', (sid, peer)).fetchone()
            if state == 'fallback' and row:
                self._meet_log(db, 'fallback', row['name'] or row['email'], [window_text(row)], fields.get('note') or 'failed', row['peer'], row['card_id'])
        return row

    def _meet_pin(self, peer, fingerprint):
        """Trust on first use: a peer's keys are pinned the first time; a change is refused (that conversation falls back)."""
        with self.connect() as db:
            ensure(db)
            row = db.execute('SELECT fingerprint FROM meet_pins WHERE peer=?', (peer,)).fetchone()
            if not row:
                db.execute('INSERT INTO meet_pins(peer,fingerprint,first_at) VALUES(?,?,?)', (peer, fingerprint, stamp(self._meet_now())))
                return True
            return row['fingerprint'] == fingerprint

    def _meet_mine(self, db, window):
        """This owner's free times and preferred ones in the window: from their own calendars, busy blocks only."""
        import friends
        setting = self.meet_setting()
        tz = self._meet_tz()
        first = dt.date.fromisoformat(window['start'])
        busy = friends.free_busy(db, self.config, {'start': (first - dt.timedelta(days=1)).isoformat(), 'days': min(window['days'] + 2, MAX_DAYS + 2)})['busy']
        return free_times(busy, window, self._meet_hours(), tz, setting['buffer'], setting['prefer'], self._meet_now())

    def _meet_propose(self, row, rejected=None):
        """Picks the next slot that fits both and, unless the owner must tap first (Careful), sends it."""
        rejected = list(rejected if rejected is not None else json.loads(row['rejected'] or '[]'))
        window = {'start': row['start'], 'days': row['days']}
        with self.connect() as db:
            mine, liked = self._meet_mine(db, window)
            careful = self._careful(db)
            video = video_habit(db)
        slot = pick(mine, json.loads(row['free'] or '[]'), row['minutes'], liked, json.loads(row['prefer'] or '[]'), rejected)
        if not slot:
            self._meet_send_quietly(row, {'t': 'cancel'})
            return self._meet_state(row['id'], row['peer'], 'fallback', note='no_slot', rejected=json.dumps(rejected))
        row = self._meet_state(row['id'], row['peer'], 'proposed', slot=json.dumps(slot), video=video, rejected=json.dumps(rejected),
                               mine_ok=0, their_ok=0, sent=0)
        if not careful:
            row = self._meet_send_proposal(row)
        return row

    def _meet_send_proposal(self, row):
        slot = json.loads(row['slot'])
        self._meet_send(row, {'t': 'propose', 'start': slot[0], 'end': slot[1], 'video': row['video'], 'round': row['round']})
        with self.connect() as db:
            db.execute('UPDATE meet_sessions SET sent=1 WHERE id=? AND peer=?', (row['id'], row['peer']))
            self._meet_log(db, 'proposed', row['name'], [when_text(parse_slot(slot[0]), self._meet_tz())], 'sent', row['peer'], row['card_id'])
            return db.execute('SELECT * FROM meet_sessions WHERE id=? AND peer=?', (row['id'], row['peer'])).fetchone()

    def _meet_send_quietly(self, row, payload):
        try:
            self._meet_send(row, payload)
        except Exception as error:  # noqa: BLE001 - its own to-do settles at its time; nothing more to do here
            LOG.info('meet message not sent error=%s', type(error).__name__)

    def _meet_book(self, row):
        """Both tapped Book it: the proposer's calendar write with the invite (the app's meet_book), then the other
        Machine is told. A failed write leaves both to-dos open, with the owner's tap still needed to try again."""
        slot = json.loads(row['slot'])
        result = {'status': 'failed'}
        if self.meet_book:
            try:
                result = self.meet_book(dict(row)) or result
            except Exception as error:  # noqa: BLE001 - said on the to-do; tapping Book it again tries again
                LOG.warning('meet book error=%s', type(error).__name__)
                result = {'status': 'failed', 'error': str(error)[:200]}
        when = when_text(parse_slot(slot[0]), self._meet_tz())
        if result.get('status') != 'done':
            with self.connect() as db:
                db.execute("UPDATE meet_sessions SET mine_ok=0,note='failed',updated_at=? WHERE id=? AND peer=?", (stamp(self._meet_now()), row['id'], row['peer']))
                self._meet_log(db, 'booked', row['name'], [when], 'failed', row['peer'], row['card_id'])
            return 'failed'
        row = self._meet_state(row['id'], row['peer'], 'booked', note=None)
        with self.connect() as db:
            self._meet_log(db, 'booked', row['name'], [when], 'booked', row['peer'], row['card_id'])
        self._meet_send_quietly(row, {'t': 'booked', 'start': slot[0], 'end': slot[1]})
        if self.meet_close and row['card_id']:
            self.meet_close(row['card_id'], t('Booked with {}', row['name'] or row['email']))
        return 'booked'

    # -- the owner's taps (both sides)
    def meet_decide(self, card_id, choice):
        """Book it, Other time or Not needed on a scheduling to-do."""
        if choice not in ('book', 'other', 'skip'):
            raise ValueError('Book it, Other time or Not needed')
        with self.connect() as db:
            ensure(db)
            row = db.execute("SELECT * FROM meet_sessions WHERE card_id=? AND state IN ('proposed','answered','waiting') ORDER BY updated_at DESC LIMIT 1",
                             (str(card_id),)).fetchone()
        if not row or row['state'] != 'proposed':
            raise ValueError('That time is no longer open')
        slot = json.loads(row['slot'])
        when = when_text(parse_slot(slot[0]), self._meet_tz())
        if choice == 'skip':
            self._meet_send_quietly(row, {'t': 'cancel'})
            self._meet_state(row['id'], row['peer'], 'canceled')
            with self.connect() as db:
                self._meet_log(db, 'canceled', row['name'], [when], 'canceled', row['peer'], row['card_id'])
            if self.meet_close and row['card_id']:
                self.meet_close(row['card_id'], t('Not needed'))
            return {'state': 'canceled'}
        if choice == 'other':
            with self.connect() as db:
                self._meet_log(db, 'other', row['name'], [when], 'sent', row['peer'], row['card_id'])
            if row['role'] == 'answerer':
                self._meet_send(row, {'t': 'other', 'start': slot[0]})
                self._meet_state(row['id'], row['peer'], 'waiting', mine_ok=0, their_ok=0)
                return {'state': 'waiting'}
            return {'state': self._meet_again(row)['state']}
        # Book it
        if row['role'] == 'answerer':
            self._meet_send(row, {'t': 'ok', 'start': slot[0]})
            self._meet_state(row['id'], row['peer'], 'proposed', mine_ok=1)
            return {'state': 'proposed', 'waiting': True}
        row = self._meet_state(row['id'], row['peer'], 'proposed', mine_ok=1)
        if not row['sent']:  # Careful: the slot goes only now
            self._meet_send_proposal(row)
            return {'state': 'proposed', 'waiting': True}
        if row['their_ok']:
            return {'state': self._meet_book(row)}
        return {'state': 'proposed', 'waiting': True}

    def _meet_again(self, row):
        """Other time: the next slot, or the email draft after ROUNDS."""
        slot = json.loads(row['slot'] or 'null')
        rejected = json.loads(row['rejected'] or '[]') + ([slot[0]] if slot else [])
        if row['round'] + 1 >= ROUNDS:
            self._meet_send_quietly(row, {'t': 'cancel'})
            return self._meet_state(row['id'], row['peer'], 'fallback', note='rounds', rejected=json.dumps(rejected))
        with self.connect() as db:
            db.execute('UPDATE meet_sessions SET round=round+1 WHERE id=? AND peer=?', (row['id'], row['peer']))
            row = db.execute('SELECT * FROM meet_sessions WHERE id=? AND peer=?', (row['id'], row['peer'])).fetchone()
        return self._meet_propose(row, rejected)

    # -- receiving
    def meet_round(self, hinted=False):
        """Fetches and takes what other Machines sent, settles timeouts, and tells the cloud the setting when due."""
        if not self.meet_on or not self._sealing():
            return 0
        import time
        stamp_now = time.monotonic()
        try:
            self.meet_tell()
        except Exception as error:  # noqa: BLE001
            LOG.info('meet allow not told error=%s', type(error).__name__)
        taken = 0
        if hinted or stamp_now - getattr(self, '_meet_looked', 0.0) > INBOX_EVERY:
            self._meet_looked = stamp_now
            try:
                found = self.relay.call('POST', '/meet', {'op': 'inbox'}, timeout=20)
            except Exception as error:  # noqa: BLE001 - away or an older cloud: next round
                LOG.info('meet inbox error=%s', type(error).__name__)
                found = {}
            done = []
            for msg in (found or {}).get('messages', [])[:50] if isinstance(found, dict) else []:
                try:
                    self.meet_take(msg)
                    taken += 1
                except Exception as error:  # noqa: BLE001 - one bad message never stops the others
                    LOG.warning('meet message dropped error=%s', type(error).__name__)
                if isinstance(msg, dict) and msg.get('id'):
                    done.append(str(msg['id']))
            if done:
                try:
                    self.relay.call('POST', '/meet', {'op': 'ack', 'ids': done}, timeout=20)
                except Exception as error:  # noqa: BLE001 - sent again and taken once (meet_seen)
                    LOG.info('meet ack error=%s', type(error).__name__)
        self.meet_timeouts()
        return taken

    def meet_timeouts(self):
        current = self._meet_now()
        with self.connect() as db:
            ensure(db)
            late = db.execute("SELECT * FROM meet_sessions WHERE role='asker' AND state='asked' AND deadline<?", (stamp(current),)).fetchall()
            passed = db.execute("SELECT * FROM meet_sessions WHERE state IN ('proposed','waiting') AND slot IS NOT NULL").fetchall()
            db.execute('DELETE FROM meet_seen WHERE at<?', (stamp(current - dt.timedelta(days=KEEP_DAYS)),))
        for row in late:
            self._meet_state(row['id'], row['peer'], 'fallback', note='no_answer')
        for row in passed:
            start = parse_slot(json.loads(row['slot'])[0])
            if start and start <= current + dt.timedelta(minutes=30):
                if row['role'] == 'asker':
                    self._meet_state(row['id'], row['peer'], 'fallback', note='passed')
                else:
                    self._meet_state(row['id'], row['peer'], 'canceled', note='passed')
                    if self.meet_close and row['card_id']:
                        self.meet_close(row['card_id'], t('Time passed'))

    def meet_take(self, msg):
        """One message from another Machine: checked (the cloud's routing, pinned keys, the seal bound to it), then
        taken once."""
        sealing = self._sealing()
        me = self.meta('meet_id')
        if not isinstance(msg, dict) or not sealing or not me:
            return None
        peer, mid, keys = str(msg.get('from') or ''), str(msg.get('id') or ''), msg.get('keys')
        checked = nc.check_keys(keys) if isinstance(keys, dict) else None
        if not PEER.fullmatch(peer) or not re.fullmatch(r'[a-f0-9]{32}', mid) or not checked:
            return None
        with self.connect() as db:
            ensure(db)
            if db.execute('SELECT 1 FROM meet_seen WHERE msg=?', (mid,)).fetchone():
                return None
            db.execute('INSERT INTO meet_seen(msg,at) VALUES(?,?)', (mid, stamp(self._meet_now())))
        name = ' '.join(str(msg.get('name') or '').split())[:80]
        if not self._meet_pin(peer, checked['fingerprint']):
            with self.connect() as db:
                self._meet_log(db, 'asked_in', name, [''], 'keys', peer)
            return None
        try:
            body = nc.open_sealed(msg.get('sealed'), sealing.private, keys, {'p': 'meet', 'k': KIND, 'f': peer, 't': me, 'r': mid})
        except nc.SealError as error:
            LOG.warning('meet message did not open reason=%s', error)
            return None
        if not isinstance(body, dict) or not SESSION.fullmatch(str(body.get('s') or '')):
            return None
        kind = body.get('t')
        if kind == 'ask':
            emails = [str(e).strip().lower() for e in (msg.get('emails') or [])[:20] if isinstance(e, str) and '@' in e]
            return self._meet_answer(peer, keys, name, emails, body)
        with self.connect() as db:
            row = db.execute('SELECT * FROM meet_sessions WHERE id=? AND peer=?', (body['s'], peer)).fetchone()
        if not row or kind not in TYPES.get(row['role'], ()):
            return None
        return getattr(self, '_meet_' + ('asker' if row['role'] == 'asker' else 'answerer'))(row, kind, body)

    def _meet_answer(self, peer, keys, name, emails, body):
        """Another Machine asks for free times: answered by plain code, or refused (with no reason told)."""
        current = self._meet_now()
        window = parse_window(body.get('start'), body.get('days'), current.astimezone(self._meet_tz()).date())
        minutes = body.get('minutes') if body.get('minutes') in LENGTHS else 30
        sid = body['s']
        with self.connect() as db:
            ensure(db)
            if db.execute('SELECT 1 FROM meet_sessions WHERE id=? AND peer=?', (sid, peer)).fetchone():
                return None  # the same conversation asked twice: answered once
            day = stamp(current - dt.timedelta(days=1))
            mine = db.execute("SELECT COUNT(*) FROM meet_log WHERE what='asked_in' AND at>?", (day,)).fetchone()[0]
            theirs = db.execute("SELECT COUNT(*) FROM meet_log WHERE what='asked_in' AND peer=? AND at>?", (peer, day)).fetchone()[0]
            shown = window_text(window) if window else ''
            reason = None
            if self.meet_setting()['allow'] != 'freebusy':
                reason = 'off'
            elif not window:
                reason = 'window'
            elif theirs >= PEER_PER_DAY or mine >= ALL_PER_DAY:
                reason = 'limit'
            elif not emails or not self._meet_thread(db, emails):
                reason = 'thread'
            who = name or (emails[0] if emails else '')
            self._meet_log(db, 'asked_in', who, [shown], reason or 'answered', peer)
            if reason:
                free = liked = None
            else:
                free, liked = self._meet_mine(db, window)
                at = stamp(current)
                db.execute('INSERT INTO meet_sessions(id,peer,role,keys,email,name,state,start,days,minutes,free,prefer,created_at,updated_at) '
                           "VALUES(?,?,'answerer',?,?,?,'answered',?,?,?,?,?,?,?)",
                           (sid, peer, json.dumps(keys), emails[0], who, window['start'], window['days'], minutes, json.dumps(free), json.dumps(liked), at, at))
        row = {'id': sid, 'peer': peer, 'keys': json.dumps(keys)}
        if reason:
            self._meet_send_quietly(row, {'t': 'no'})
            return 'refused'
        self._meet_send_quietly(row, {'t': 'free', 'free': free, 'prefer': liked, 'book': bool(self.meet_card)})
        return 'answered'

    def _meet_thread(self, db, emails):
        """An exchange both ways with one of these addresses, in the owner's own mail: they wrote, and the owner wrote."""
        if self.meet_thread:
            return bool(self.meet_thread(emails))
        import fleet
        for address in emails:
            node = fleet._person(db, address)
            if not node:
                continue
            try:
                info = json.loads(node['info'] or '{}')
            except ValueError:
                continue
            if (info.get('wrote') or 0) >= 1 and (info.get('heard') or 0) >= 1 and str(info.get('role') or '').lower() != 'automated sender':
                return True
        return False

    def _meet_asker(self, row, kind, body):
        if kind == 'free' and row['state'] == 'asked':
            window = {'start': row['start'], 'days': row['days']}
            if body.get('book') is not True:
                return self._meet_state(row['id'], row['peer'], 'fallback', note='declined')
            self._meet_state(row['id'], row['peer'], 'asked', free=json.dumps(clean_times(body.get('free'), window)),
                             prefer=json.dumps(clean_times(body.get('prefer'), window)))
            with self.connect() as db:
                db.execute("UPDATE meet_log SET outcome='answered' WHERE id=(SELECT MAX(id) FROM meet_log WHERE what='asked' AND peer=?)", (row['peer'],))
                row = db.execute('SELECT * FROM meet_sessions WHERE id=? AND peer=?', (row['id'], row['peer'])).fetchone()
            return self._meet_propose(row)
        if kind == 'no' and row['state'] == 'asked':
            return self._meet_state(row['id'], row['peer'], 'fallback', note='declined')
        slot = json.loads(row['slot'] or 'null')
        if row['state'] != 'proposed' or not slot:
            return None
        when = when_text(parse_slot(slot[0]), self._meet_tz())
        if kind == 'ok' and body.get('start') == slot[0] and row['sent']:
            row = self._meet_state(row['id'], row['peer'], 'proposed', their_ok=1)
            return self._meet_book(row) if row['mine_ok'] else 'waiting'
        if kind == 'other':
            with self.connect() as db:
                self._meet_log(db, 'other_in', row['name'], [when], 'answered', row['peer'], row['card_id'])
            return self._meet_again(row)
        if kind == 'cancel':
            with self.connect() as db:
                self._meet_log(db, 'canceled_in', row['name'], [when], 'canceled', row['peer'], row['card_id'])
            return self._meet_state(row['id'], row['peer'], 'fallback', note='declined')
        return None

    def _meet_answerer(self, row, kind, body):
        tz = self._meet_tz()
        if kind == 'propose' and row['state'] in ('answered', 'waiting', 'proposed'):
            a, b = parse_slot(body.get('start')), parse_slot(body.get('end'))
            window = {'start': row['start'], 'days': row['days']}
            fits = a and b and (b - a) == dt.timedelta(minutes=row['minutes']) and _inside(_spans(json.loads(row['free'] or '[]')), a, b)
            if fits:  # still free now, from the owner's calendars as they are
                with self.connect() as db:
                    fits = _inside(_spans(self._meet_mine(db, window)[0]), a, b)
            if not fits:
                self._meet_send_quietly(row, {'t': 'other', 'start': body.get('start') if isinstance(body.get('start'), str) else ''})
                return 'other'
            video = body.get('video') if body.get('video') in VIDEO else None
            row = self._meet_state(row['id'], row['peer'], 'proposed', slot=json.dumps([slot_text(a), slot_text(b)]), video=video, mine_ok=0, their_ok=0, sent=1)
            with self.connect() as db:
                self._meet_log(db, 'proposed_in', row['name'], [when_text(a, tz)], 'waiting', row['peer'], row['card_id'])
            if not row['card_id'] and self.meet_card:
                card_id = self.meet_card({**dict(row), 'title': todo_title(row['name'] or row['email'])})
                with self.connect() as db:
                    db.execute('UPDATE meet_sessions SET card_id=? WHERE id=? AND peer=?', (str(card_id), row['id'], row['peer']))
            return 'proposed'
        slot = json.loads(row['slot'] or 'null')
        when = when_text(parse_slot(slot[0]), tz) if slot else ''
        if kind == 'booked' and row['state'] == 'proposed' and slot and body.get('start') == slot[0] and row['mine_ok']:
            self._meet_state(row['id'], row['peer'], 'booked')
            with self.connect() as db:
                self._meet_log(db, 'booked_in', row['name'], [when], 'booked', row['peer'], row['card_id'])
            if self.meet_close and row['card_id']:
                self.meet_close(row['card_id'], t('Booked by {}', row['name'] or row['email']))
            return 'booked'
        if kind == 'cancel' and row['state'] in ('answered', 'proposed', 'waiting'):
            self._meet_state(row['id'], row['peer'], 'canceled')
            with self.connect() as db:
                self._meet_log(db, 'canceled_in', row['name'], [when or window_text(row)], 'canceled', row['peer'], row['card_id'])
            if self.meet_close and row['card_id']:
                self.meet_close(row['card_id'], t('Not needed'))
            return 'canceled'
        return None

    # -- what the to-dos show
    def annotate_meet(self, db, suggestions):
        """A scheduling to-do's state: the proposed time and the taps, for the dashboard."""
        ids = [s['id'] for s in suggestions if s.get('id')]
        if not ids or not db.execute("SELECT 1 FROM sqlite_master WHERE name='meet_sessions'").fetchone():
            return
        tz = self._meet_tz()
        rows = {}
        for r in db.execute('SELECT * FROM meet_sessions WHERE card_id IN (SELECT value FROM json_each(?)) ORDER BY updated_at', (json.dumps(ids),)):
            rows[r['card_id']] = r
        for s in suggestions:
            r = rows.get(s.get('id'))
            if not r:
                continue
            slot = json.loads(r['slot'] or 'null')
            start = parse_slot(slot[0]) if slot else None
            view = {'state': r['state'], 'role': r['role'], 'name': r['name'] or r['email'], 'minutes': r['minutes'],
                    'video': VIDEO.get(r['video']), 'mine_ok': bool(r['mine_ok']), 'their_ok': bool(r['their_ok']), 'note': r['note']}
            if start and r['state'] in ('proposed', 'waiting', 'booked'):
                view.update(title=todo_title(r['name'] or r['email']), when=when_text(start, tz), start=slot[0])
                if r['state'] == 'proposed':
                    s['title'] = view['title']
            s['meet'] = view

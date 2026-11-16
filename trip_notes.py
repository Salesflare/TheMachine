"""Trips (docs/help/calendar.md, "Trips and events"): one trip per journey, a band in Calendar, built from booking mail.

The mail source reads a confirmation's structured data (bookings.py) into the message's sealed metadata. collect()
copies each mail's bookings into trip_bookings (sealed at rest, message_seal.DERIVED), from a cursor over events, so a
round reads only new mail. A mail without structured data that looks like a booking (bookings.looks_booked) waits in
trip_pending instead, for TripsApp.trip_extract_step to read with a small model call (bookings.extract_prompt), a few
mails per call; what it finds goes into trip_bookings the same way (answered). Event tickets are kept there too, for
event_notes.py. drafts() then builds the trips from all of them, and NotesApp.trip_notes_step hands those to
note_pages.sync, which keeps the owner's own edits, moves and deletes on top.

How bookings become trips, in plain code:
- One booking (a flight leg, a stay, a train ride, a rental car, a taxi, a parking) is known by its type and code (a
  ride: and its number). A later mail about it (a changed time or day, a seat, a reminder) updates it, keeping what
  the earlier mail said that the later one leaves out; a cancellation takes it out.
- Bookings that overlap or follow within a day are one journey, and so are bookings under the same booking code.
  After a ride away, what follows within RETURN_DAYS joins the journey until a ride back to where it started, when it
  connects (it leaves from where the journey is) or follows within a few days. A ticket for any train that day (no
  time, like a commute) joins only a journey it connects to on that day, and makes no trip on its own; nor does a
  booking for someone else (a colleague's flight forwarded).
- The trip is named after where it goes: the town of its longest stay, else where its rides wait the longest.
- A trip keeps its note: bookings that are on a trip note already stay on that note (drafts), whatever order their
  mail is read in.
- Each booking is a line at its own time, in the owner's language, with its code, seat, address and arrival time, and
  the mail it came from. A stay, a rental car and a parking also get a line when they end. A ticket for something
  during the trip goes on it too (event_notes.py leaves it out of Events).
- Gaps, while the trip is still ahead or under way, and only when real (gaps): a night between the stays of a trip
  that has stays, and no ride, transfer, car or taxi between a flight and the stay, or the stay and the flight home.
- A trip whose bookings were all canceled goes. One whose mail aged out of the mailbox stays.

Tables (this module owns them): trip_bookings (one row per mail with bookings: the account it came in on, when, and its
rows), trip_pending (mail waiting for the model, with the text the history walk read when the stored one was a stub)
and trip_state (the cursor)."""
import datetime as dt
import hashlib
import json
import re
import unicodedata

from i18n import t
import bookings as bookings_mail
import mail_cleanup
import timeutil
import todo_areas

SCHEMA = '''
CREATE TABLE IF NOT EXISTS trip_bookings(event_id INTEGER PRIMARY KEY,account_id TEXT NOT NULL,occurred_at TEXT NOT NULL,rows TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS trip_state(id INTEGER PRIMARY KEY CHECK(id=1),cursor INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS trip_pending(event_id INTEGER PRIMARY KEY,account_id TEXT NOT NULL,occurred_at TEXT NOT NULL,text TEXT,
  tries INTEGER NOT NULL DEFAULT 0,done_at TEXT);
'''
BATCH = 5000  # mails read per round: a Machine with a year of mail is through it in a few rounds, not a day
# Mail the Machine held before it read bookings (or before it read them as it does now) carries none in its metadata:
# the history worker reads the mailbox's held mail again once per WALK_VERSION, slowly, after its own history walk
# (HistoryApp.history_bookings). Raise it when bookings.py reads more than before.
WALK_VERSION = 2  # 2: booking-like mail without structured data is read by the model too
NEAR = dt.timedelta(days=1, hours=12)  # bookings this close after each other are one journey
RETURN_DAYS = 31  # a ride back home this long after the way out still belongs to it
FOLLOWS = dt.timedelta(days=3)  # while away, a booking this close after the last one joins the journey
RIDES = ('flight', 'train', 'bus', 'boat')
GROUND = ('car', 'taxi', 'train', 'bus')  # what gets someone from an airport to a stay
STAYS = ('hotel',)
TRAVEL = ('hotel', 'car', 'taxi', 'parking', *RIDES)
PENDING_TRIES = 3  # a mail whose reading failed this often is passed


def ensure(db):
    db.executescript(SCHEMA)


def _meta(value):
    if isinstance(value, dict):
        return value
    try:
        found = json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def keep(db, event_id, account_id, occurred_at, found):
    """One mail's bookings kept for the trips and events; 1 when it had some, else 0."""
    found = [x for x in found if isinstance(x, dict)][:12] if isinstance(found, list) else []
    if not found:
        return 0
    db.execute('INSERT OR REPLACE INTO trip_bookings(event_id,account_id,occurred_at,rows) VALUES(?,?,?,?)',
               (event_id, account_id, occurred_at, json.dumps(found)))
    return 1


def queue(db, event_id, account_id, occurred_at, text=None):
    """A mail that looks like a booking without structured data, for the model to read (text: what the history walk
    read, when the stored text is a stub); once, unless the walk reads it in full where the stored text was a stub
    ("this mail is in HTML"): then it is read again with that."""
    if text:
        row = db.execute('SELECT p.text,e.body FROM trip_pending p JOIN events e ON e.id=p.event_id WHERE p.event_id=?', (event_id,)).fetchone()
        if row:
            if row['text'] is None and len(str(row['body'] or '')) * 2 < len(text):
                db.execute('UPDATE trip_pending SET text=?,tries=0,done_at=NULL WHERE event_id=?', (text[:bookings_mail.MAIL_CHARS * 2], event_id))
            return
    db.execute('INSERT OR IGNORE INTO trip_pending(event_id,account_id,occurred_at,text) VALUES(?,?,?,?)',
               (event_id, account_id, occurred_at, (text or '')[:bookings_mail.MAIL_CHARS * 2] or None))


def collect(db, limit=BATCH):
    """New mail since the cursor: each one with bookings is kept, one that looks like a booking without them waits for
    the model (trip_pending). Returns how many mails had some."""
    cursor = (db.execute('SELECT cursor FROM trip_state WHERE id=1').fetchone() or [0])[0]
    rows = db.execute(f"SELECT id,account_id,occurred_at,title,body,metadata FROM events WHERE id>? AND kind IN ({','.join('?' * len(mail_cleanup.MAIL_KINDS))}) "
                      'ORDER BY id LIMIT ?', (cursor, *mail_cleanup.MAIL_KINDS, limit)).fetchall()
    kept = 0
    for r in rows:
        meta = _meta(r['metadata'])
        if meta.get('bookings'):
            kept += keep(db, r['id'], r['account_id'], r['occurred_at'], meta['bookings'])
        elif bookings_mail.looks_booked(r['title'], meta.get('from'), r['body']):
            queue(db, r['id'], r['account_id'], r['occurred_at'])
    if rows:
        db.execute('INSERT INTO trip_state(id,cursor) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET cursor=excluded.cursor', (rows[-1]['id'],))
    return kept


def _subject(title):
    return ' '.join(bookings_mail.FORWARD.sub('', re.sub(r'^\s*(re|aw|sv)\s*:\s*', '', str(title or ''), flags=re.I)).casefold().split())


def pending(db, limit):
    """The mails waiting for the model, newest first (a trip ahead matters more than one in last year's history):
    [{id, account_id, occurred_at, title, sender, text}]. A copy of one already read or waiting (the same sender and
    subject the same day, like a boarding pass per passenger) is passed, without a call."""
    out, seen = [], set()
    rows = db.execute('SELECT p.event_id,p.account_id,p.occurred_at,p.text,e.title,e.body,e.metadata FROM trip_pending p '
                      'JOIN events e ON e.id=p.event_id WHERE p.done_at IS NULL ORDER BY p.occurred_at DESC LIMIT ?', (limit * 4,)).fetchall()
    for r in rows:
        sender = str(_meta(r['metadata']).get('from') or '')
        same = (sender.casefold(), _subject(r['title']), r['occurred_at'][:10])
        if same in seen:
            db.execute('UPDATE trip_pending SET done_at=? WHERE event_id=?', ('same', r['event_id']))
            continue
        seen.add(same)
        if len(out) < limit:
            out.append({'id': r['event_id'], 'account_id': r['account_id'], 'occurred_at': r['occurred_at'], 'title': str(r['title'] or ''),
                        'sender': sender, 'text': r['text'] or str(r['body'] or '')})
    return out


def answered(db, mails, found, at):
    """The model's reading of these mails ({mail id: rows}, bookings.parse) kept; a mail it gave nothing for is done
    too. None (no answer): each is tried again later, up to PENDING_TRIES. Returns how many had bookings."""
    kept = 0
    for m in mails:
        if found is None:
            db.execute('UPDATE trip_pending SET tries=tries+1,done_at=CASE WHEN tries+1>=? THEN ? END WHERE event_id=?',
                       (PENDING_TRIES, at, m['id']))
            continue
        kept += keep(db, m['id'], m['account_id'], m['occurred_at'], found.get(str(m['id'])) or [])
        db.execute('UPDATE trip_pending SET done_at=? WHERE event_id=?', (at, m['id']))
    return kept


def waiting(db):
    return db.execute('SELECT count(*) FROM trip_pending WHERE done_at IS NULL').fetchone()[0]


def _at(value):
    """A booking's time as a datetime (a day alone: its start)."""
    try:
        return dt.datetime.fromisoformat(value if 'T' in value else value + 'T00:00')
    except (TypeError, ValueError):
        return None


def _ident(b):
    """A booking's line key: its type, code, number or name (a ride without a number: where it goes), and day."""
    what = b.get('number', '') or b.get('name', '') or (_leg(b) if b['type'] in LEGS else '')
    return '|'.join((b['type'], b.get('code', ''), what, b['start'][:10]))


LEGS = ('train', 'bus', 'boat', 'taxi')  # often one ticket for the way out and back, without a number


def _leg(b):
    return '>'.join(sorted(_spot(b.get('from')))) + '>' + '>'.join(sorted(_spot(b.get('to'))))


def _same(b):
    """What makes two mails about one booking: its type and code, and a ride's number; without a code, as _ident."""
    if not b.get('code'):
        return _ident(b)
    number = re.sub(r'\W', '', str(b.get('number') or '')).upper()
    if b['type'] in LEGS and not number:  # legs on one ticket: its way out and back
        number = _leg(b)
    return '|'.join(('same', b['type'], b['code'].upper(), number if b['type'] in (*RIDES, 'taxi') else ''))


def bookings_now(db):
    """Every travel booking as the latest mail about it says, canceled ones out: [{..., event_id, account_id, seen}], by
    start. Also the line keys that were canceled. A cancellation that names only a code takes out every booking of
    that type under it."""
    latest, canceled = {}, set()
    for r in db.execute('SELECT event_id,account_id,occurred_at,rows FROM trip_bookings ORDER BY occurred_at,event_id'):
        try:
            rows = json.loads(r['rows'])
        except (TypeError, ValueError):
            continue
        for b in rows if isinstance(rows, list) else ():
            if not isinstance(b, dict) or b.get('type') not in TRAVEL:
                continue
            if b.get('status') == 'canceled' and b.get('code') and not _at(b.get('start')):
                for key in [k for k, x in latest.items() if x['type'] == b['type'] and x.get('code', '').upper() == b['code'].upper()]:
                    canceled.add(_ident(latest.pop(key)))
                continue
            if not _at(b.get('start')):
                continue
            key = _same(b)
            if b.get('status') == 'canceled':
                old = latest.pop(key, None)
                canceled.add(_ident(old or b))
                continue
            old = latest.get(key) or {}
            if b.get('others') and old and not old.get('others'):
                continue  # a fellow traveler's copy of the owner's booking (their boarding pass): the owner's stays
            if old.get('others') and not b.get('others'):
                old = {}
            if old and old['start'][:10] != b['start'][:10]:
                old = {}  # moved to another day: what the earlier mail said of times and seats no longer holds
            canceled.discard(_ident(b))
            latest[key] = {**{k: v for k, v in old.items() if k not in ('status', 'read')}, **b,
                           'event_id': r['event_id'], 'account_id': r['account_id'], 'seen': r['occurred_at']}
    merged, index = {}, {}
    for n, b in enumerate(sorted(latest.values(), key=lambda b: b['seen'])):  # one booking from several mails: one line
        keys = _alike(b)
        at = next((index[k] for k in keys if k in index), None)
        if at is None:
            at = n
            merged[at] = b
        elif not (b.get('others') and not merged[at].get('others')):
            merged[at] = b if merged[at].get('others') else _merge(merged[at], b)
        index.update((k, at) for k in keys + _alike(merged[at]))
    return sorted(merged.values(), key=lambda b: (b['start'], b['type'])), canceled


def _alike(b):
    """What two mails about one booking share even when only one gives its code: its type, a ride's number or a
    stay's name, and its day; a ride with a code, its departure time too (a mail that leaves out the number)."""
    keys = [(b['type'], 'code', b['code'].upper(), b['start'])] if b['type'] in RIDES and b.get('code') and 'T' in b['start'] else []
    name = re.sub(r'\W', '', str((b.get('number') if b['type'] in RIDES else b.get('name')) or '')).casefold()
    name = re.sub(r'(?<=[a-z])0+(?=\d)', '', name)  # "EX 0645" is EX645
    return keys + ([(b['type'], name, b['start'][:10])] if name else [])


def _merge(old, new):
    """The later mail over the earlier one, keeping a time of day and a code the later one leaves out."""
    out = {**old, **{k: v for k, v in new.items() if v}}
    for key in ('start', 'end'):
        if old.get(key) and new.get(key) and 'T' in old[key] and 'T' not in new[key] and old[key][:10] == new[key]:
            out[key] = old[key]
    return out


def _end(b):
    """When a booking ends: its end, else its start; a day alone runs to that day's end."""
    value = b.get('end') or b['start']
    found = _at(value)
    return found + dt.timedelta(hours=23, minutes=59) if 'T' not in value else found


STOP = {'airport', 'arpt', 'intl', 'international', 'luchthaven', 'aeroport', 'aeropuerto', 'aeroporto', 'flughafen', 'station',
        'gare', 'bahnhof', 'stazione', 'estacion', 'centraal', 'central', 'centrale', 'terminal', 'port', 'harbour', 'harbor',
        'city', 'saint', 'sankt', 'santa', 'north', 'south', 'east', 'west', 'nord', 'noord', 'zuid', 'main'}


AIRPORT_WORDS = {'airport', 'arpt', 'intl', 'international', 'luchthaven', 'aeroport', 'aéroport', 'aeropuerto', 'aeroporto',
                 'flughafen', 'lufthavn', 'flygplats', 'lotnisko'}


def _words(place):
    plain = unicodedata.normalize('NFKD', str(place or '')).encode('ascii', 'ignore').decode()
    codes = {w.casefold() for w in re.findall(r'\b[A-Z]{3}\b', plain)} - {'the', 'and', 'int', 'apt'}  # an airport's code: BRU
    return {w for w in re.split(r'[^a-z]+', plain.casefold()) if len(w) >= 4 and w not in STOP} | codes


def same_place(a, b):
    """Whether two place names are one place, as bookings write them: "Paris (Beauvais)" and "Parijs", "Nice
    Arpt" and "Nice", "LYON-PART-DIEU" and "Lyon"."""
    x, y = _words(a), _words(b)
    return any(p == q or (len(p) >= 5 and len(q) >= 5 and p[:5] == q[:5]) for p in x for q in y)


def _where(b):
    """Where a booking is, for connecting: a stay's town, a parking's place, else where a ride or car arrives."""
    return b.get('where') or b.get('to') or b.get('from') or b.get('name') or ''


def _open_ticket(b):
    """A train or bus ticket for any time that day, like a commute."""
    return b['type'] in ('train', 'bus') and 'T' not in b['start']


def _connects(a, b):
    """b picks up where a leaves off: a ride's arrival is b's departure, or a stay's town."""
    return any(same_place(x, y) for x in (a.get('to'), a.get('where'), a.get('from') if a['type'] in STAYS else None) if x
               for y in (b.get('from'), b.get('where'), b.get('to') if b['type'] in STAYS else None) if y)


def journeys(found):
    """Bookings grouped into journeys: [[booking, ...]] in time order. Bookings for someone else, and open tickets that
    connect to nothing, make none on their own; a booking for someone else (a colleague's flight sent on) is no part
    of the owner's journey."""
    found = [x for x in found if not x.get('others')]
    regular = _regular(found)
    groups = []
    for b in found:
        start = _at(b['start'])
        last = groups[-1] if groups else None
        same_code = last and b.get('code') and any(x.get('code') == b['code'] for x in last)
        near = last and start <= max(_end(x) for x in last) + NEAR
        if near and (_open_ticket(b) or all(_open_ticket(x) for x in last)):  # a commute ticket next to a trip isn't part of it
            near = any(x['start'][:10] == b['start'][:10] and (_connects(x, b) or _connects(b, x)) for x in last)
        if last and (same_code or near):
            last.append(b)
        else:
            groups.append([b])
    out = []
    for g in (g for g in groups if not _commute(g, regular)):  # while away: what follows joins, up to the ride back home
        prev = out[-1] if out else None
        rides = [x for x in prev or () if x['type'] in RIDES and not x.get('others')]
        origin = rides[0].get('from') if rides else None
        away = rides and not any(same_place(r.get('to'), origin) for r in rides[1:])  # not back where it started
        gap = _at(g[0]['start']) - max(_end(x) for x in prev) if prev else None
        leaves_home = g[0]['type'] in RIDES and same_place(g[0].get('from'), origin)
        if (away and gap <= dt.timedelta(days=RETURN_DAYS) and not leaves_home
                and (gap <= FOLLOWS or _connects(prev[-1], g[0]) or any(x['type'] in RIDES and same_place(x.get('to'), origin) for x in g))):
            prev.extend(g)
        else:
            out.append(g)
    return [g for g in out if _a_trip(g, regular)]


def _spot(place):
    return frozenset(w[:5] for w in _words(place))


def _route(b):
    return frozenset((_spot(b.get('from')), _spot(b.get('to'))))


def _regular(found):
    """Train and bus routes ridden on more than one day, like a commute."""
    days = {}
    for b in found:
        if b['type'] in ('train', 'bus'):
            days.setdefault(_route(b), set()).add(b['start'][:10])
    return {route for route, seen in days.items() if len(seen) > 1}


def _commute(group, regular):
    """Trains and buses alone, on a route ridden on other days too: a commute, never a trip nor part of one."""
    return all(b['type'] in ('train', 'bus') for b in group) and any(_route(b) in regular for b in group)


def _a_trip(group, regular=frozenset()):
    """Whether bookings make a trip: anything with more than trains and buses; those alone when one is for a set time
    off the routes ridden on other days, or they go somewhere and come back (a day out on open tickets)."""
    ground = [b for b in group if b['type'] in ('train', 'bus')]
    if len(ground) < len(group):
        return True
    far = [b for b in ground if _route(b) not in regular]
    return any(not _open_ticket(b) for b in far) or (len(far) > 1 and same_place(ground[-1].get('to'), ground[0].get('from')))


def _town(place):
    """A place as a trip names it: "Porto-Francisco Sa Carneiro Airport (OPO)" is Porto, "NATAL INTL" Natal."""
    text = re.split(r'\s*[,(]|\s+-\s+|(?<=[a-z])-(?=[A-Z])', str(place or ''))[0]
    text = ' '.join(w for w in text.split() if w.casefold().strip('.') not in AIRPORT_WORDS)
    text = text.title() if text.isupper() else text
    return text or str(place or '')


def _nights(b):
    start, end = _at(b['start']), _at(b.get('end') or '')
    return (end.date() - start.date()).days if end else 0


def _title(group):
    """Where the trip goes: the town of its longest stay, else where its rides wait the longest before the next one."""
    stays = sorted((b for b in group if b['type'] in STAYS and not b.get('others') and (b.get('where') or b.get('name'))),
                   key=lambda b: -_nights(b))
    if stays:
        return stays[0].get('where') or stays[0]['name']
    rides = [b for b in group if b['type'] in RIDES and b.get('to')]
    if rides:
        home = rides[0].get('from')
        waits = [((_at(n['start']) - _end(r)) if n else dt.timedelta(0), -i, r['to'])
                 for i, (r, n) in enumerate(zip(rides, rides[1:] + [None])) if not (i and same_place(r['to'], home))]
        return _town(max(waits)[2])
    other = next((b for b in group if b.get('from') or b.get('where') or b.get('name')), None)
    return (other.get('where') or other.get('from') or other.get('name')) if other else t('Trip')


def _code(b, lang=None):
    more = [t('booking {}', b['code'], lang=lang)] if b.get('code') else []
    if b.get('seat'):
        more.append(t('seat {}', b['seat'], lang=lang))
    if b.get('ticket'):
        more.append(t('ticket {}', b['ticket'], lang=lang))
    return ''.join(', ' + x for x in more)


def _arrives(b, lang=None):
    """', arrives 19:50' (or the next day), from a ride's own arrival time."""
    end = b.get('end') or ''
    if 'T' not in end or end == b['start']:
        return ''
    days = (_at(end).date() - _at(b['start']).date()).days
    when = end[11:16]
    return ', ' + (t('arrives {} the next day', when, lang=lang) if days == 1 else t('arrives {}', when, lang=lang) if days == 0 else
                   t('arrives {} on {}', when, end[:10], lang=lang))


def _within(part, whole):
    """Whether every word of one place is in the other already (a pick-up desk and its address, an event's town)."""
    words = set(re.findall(r'\w+', str(part or '').casefold()))
    return bool(words) and words <= set(re.findall(r'\w+', str(whole or '').casefold()))


def lines(b, lang=None):
    """The lines one booking gives: (key, at, text)."""
    key = hashlib.sha256(_ident(b).encode()).hexdigest()[:16]
    route = t('{} to {}', b['from'], b['to'], lang=lang) if b.get('from') and b.get('to') else b.get('to') or b.get('from') or ''
    address = ', ' + b['address'] if b.get('address') else ''
    if b['type'] == 'hotel':
        nights = _nights(b)
        text = b['name'] + (', ' + t('{} nights', nights, lang=lang) if nights > 0 else '') + address + _code(b, lang)
        out = [(key, b['start'], text)]
        if b.get('end'):
            out.append((key + '-out', b['end'], t('Check out of {}', b['name'], lang=lang)))
        return out
    if b['type'] == 'car':
        what = ', '.join(x for x in (b.get('by'), b.get('name')) if x)
        address = '' if _within(b.get('address'), b.get('from')) else address
        text = t('Rental car', lang=lang) + (' ' + what if what else '') + (', ' + t('pick up in {}', b['from'], lang=lang) if b.get('from') else '') + address + _code(b, lang)
        out = [(key, b['start'], text)]
        if b.get('end'):
            out.append((key + '-back', b['end'], t('Return the rental car in {}', b.get('to') or b.get('from'), lang=lang) if (b.get('to') or b.get('from')) else t('Return the rental car', lang=lang)))
        return out
    if b['type'] == 'parking':
        place = b.get('name') or b.get('where') or b.get('address')
        text = t('Parking at {}', place, lang=lang) + (address if b.get('address') != place else '') + _code(b, lang)
        out = [(key, b['start'], text)]
        if b.get('end'):
            out.append((key + '-back', b['end'], t('Pick up the car at {}', place, lang=lang)))
        return out
    if b['type'] == 'event':
        where = b.get('address') if _within(b.get('where'), b.get('address')) else ', '.join(x for x in (b.get('where'), b.get('address')) if x)
        return [(key, b['start'], t('Tickets for {}', b['name'], lang=lang) + (', ' + where if where else '') + _code(b, lang))]
    word = {'flight': t('Flight', lang=lang), 'train': t('Train', lang=lang), 'bus': t('Bus', lang=lang), 'boat': t('Ferry', lang=lang),
            'taxi': t('Taxi', lang=lang)}[b['type']]
    name = ' '.join(x for x in (word, b.get('number') or (b.get('by') if b['type'] != 'flight' else '')) if x)
    return [(key, b['start'], name + (' ' + route if route else '') + _arrives(b, lang) + _code(b, lang))]


def _in(stay):
    """A stay's check-in; a day alone: the afternoon."""
    return _at(stay['start']) + (dt.timedelta(hours=15) if 'T' not in stay['start'] else dt.timedelta(0))


def _out(stay):
    """A stay's check-out; a day alone: the late morning."""
    return _at(stay['end']) + (dt.timedelta(hours=11) if 'T' not in stay['end'] else dt.timedelta(0))


def _overlaps(b, start, end):
    return _at(b['start']) <= end and _end(b) >= start


def gaps(group, lang=None):
    """What is missing from a trip, only where it is real: (key, at, text, until).
    - A night with no place to stay, between the first and the last night away, on a trip that has stays (one with
      none is a stay with family or friends, or at home), unless a ride runs through it.
    - Nothing booked between a flight's arrival and the stay it goes to, or the stay and the flight out: no car, taxi,
      train or bus in between, and no rental car at hand."""
    mine = [b for b in group if not b.get('others')]
    stays = [b for b in mine if b['type'] in STAYS and b.get('end')]
    out = []
    if not stays:
        return out
    rides = [b for b in mine if b['type'] in RIDES]
    first = min([_at(stays[0]['start']).date()] + [_end(r).date() for r in rides[:1]])
    last = max([_at(s['end']).date() for s in stays] + [_at(r['start']).date() for r in rides[-1:]])
    covered = set()
    for b in stays + [r for r in rides if _end(r).date() > _at(r['start']).date()]:
        day = _at(b['start']).date()
        while day < (_at(b['end']).date() if b.get('end') else day):
            covered.add(day)
            day += dt.timedelta(days=1)
    night, run = first, []
    while night <= last:
        if night < last and night not in covered:
            run.append(night)
        elif run:
            text = t('No place to stay booked for {} nights', len(run), lang=lang)
            out.append(('gap-night-' + run[0].isoformat(), run[0].isoformat(), text, run[-1].isoformat() if len(run) > 1 else None))
            run = []
        night += dt.timedelta(days=1)
    ground = [b for b in mine if b['type'] in GROUND]
    for flight in (r for r in rides if r['type'] == 'flight'):
        key = hashlib.sha256(_ident(flight).encode()).hexdigest()[:16]
        arrival = _end(flight)
        stay = next((s for s in stays if dt.timedelta(hours=-6) <= _in(s) - arrival <= dt.timedelta(hours=30)), None)
        if stay and flight.get('to') and not any(_overlaps(g, arrival - dt.timedelta(hours=1), max(arrival, _in(stay)) + dt.timedelta(hours=3)) for g in ground):
            out.append(('gap-to-' + key, flight.get('end') or flight['start'], t('Nothing booked from {} airport to {}', _town(flight['to']), stay['name'], lang=lang), None))
        leaves = _at(flight['start'])
        stay = next((s for s in stays if dt.timedelta(hours=-3) <= leaves - _out(s) <= dt.timedelta(hours=30)), None)
        if stay and flight.get('from') and not any(_overlaps(g, _out(stay) - dt.timedelta(hours=12), leaves) for g in ground):
            out.append(('gap-from-' + key, _out(stay).isoformat()[:16], t('Nothing booked from {} to {} airport', stay['name'], _town(flight['from']), lang=lang), None))
    return out


def _area(accounts, account_id):
    account = next((a for a in accounts or () if a.get('id') == account_id), None)
    return (todo_areas.area_of_account(account) if account else None) or todo_areas.PERSONAL


def _kept(db):
    """The trip notes already made, by the bookings on them: {booking line key: {note key}}, and each note's rank (one
    the owner deleted or merged away after the ones still there, then the oldest first). A line the owner moved to
    another note stays out."""
    held, rank = {}, {}
    try:
        rows = db.execute("SELECT p.id,p.key AS note,l.key AS line,(p.removed_at IS NOT NULL OR p.merged_into IS NOT NULL) AS gone "
                          "FROM note_pages p JOIN note_page_lines l ON l.note_id=p.id "
                          "WHERE p.kind='trip' AND l.by='machine' AND l.moved_from IS NULL AND l.key IS NOT NULL").fetchall()
    except Exception:  # noqa: BLE001 - a database before notes
        return held, rank
    for r in rows:
        if str(r['note'] or '').startswith('trip:'):
            held.setdefault(r['line'], set()).add(r['note'][5:])
            rank[r['note'][5:]] = (r['gone'], r['id'])
    return held, rank


def _spare(db, key):
    """A trip note no booking needs any more that nothing of the owner's is on: their title, dates, place, words or
    lines. It goes (keep says no); one with anything of theirs stays, for them to merge or delete."""
    row = db.execute("SELECT id FROM note_pages WHERE key=? AND by='machine' AND owner_title IS NULL AND owner_dates=0 AND owner_parent=0 "
                     'AND removed_at IS NULL AND merged_into IS NULL', ('trip:' + key,)).fetchone()
    return bool(row) and not db.execute("SELECT 1 FROM note_page_lines WHERE note_id=? AND (by!='machine' OR owner_text IS NOT NULL OR moved_from IS NOT NULL) "
                                        'UNION SELECT 1 FROM note_pages WHERE parent_id=? OR merged_into=?', (row['id'], row['id'], row['id'])).fetchone()


def _tickets(db):
    try:
        import event_notes
        return event_notes.tickets(db)[0]
    except Exception:  # noqa: BLE001 - tickets are extra on a trip; the trip comes without them
        return []


def spans(groups):
    """Each journey's first and last moment, for the tickets that fall in it."""
    return [(min(_at(b['start']) for b in g), max(_end(b) for b in g)) for g in groups]


def on_a_trip(ticket, found_spans):
    start = _at(ticket['start'])
    return bool(start) and any(a <= start <= z for a, z in found_spans)


def _order(line):
    """A line's place in the day: a day without a time sits where it usually falls, a check-out in the morning, a
    check-in in the afternoon, parking around the rest, and the rest at noon."""
    at, key, item = line['at'], line['key'], line.get('item')
    if 'T' in at:
        return at
    if key.endswith('-out'):
        return at + 'T10:59'
    if item == 'parking':
        return at + ('T23:00' if key.endswith('-back') else 'T06:00')
    return at + ('T15:00' if item == 'hotel' else 'T12:00')


def _today():
    return timeutil.today().isoformat()


def drafts(db, accounts, lang=None, today=None):
    """The trips as note_pages.sync drafts, and keep(key) for the trips no booking holds any more.

    A trip keeps the key of the note already made for it: the oldest trip note holding any of its bookings. Mail is
    read in the order it arrived on the Machine, not the order it was sent, so a journey's first booking can show up
    after its note was made (an older confirmation the history walk brings in later); a key from the bookings alone
    would then start a second note for the same journey. A machine-made trip note whose bookings all went to another
    trip's note goes, unless the owner put something of theirs on it."""
    found, canceled = bookings_now(db)
    today = today or _today()
    (held, rank), taken, superseded = _kept(db), set(), set()
    groups = journeys(found)
    tickets = _tickets(db)
    out = []
    for group, (first_at, last_at) in zip(groups, spans(groups)):
        first = min((b for b in group if not b.get('others')), key=lambda b: (b['seen'], b['start']))  # a new trip's key
        key = hashlib.sha256(_ident(first).encode()).hexdigest()[:20]
        mine = {hashlib.sha256(_ident(b).encode()).hexdigest()[:16] for b in group}
        before = {k for lkey in mine for k in held.get(lkey, ()) if k not in taken}
        if before:
            key = min(before, key=rank.__getitem__)
            superseded |= {k for k in before - {key} if all(lkey in mine for lkey, notes in held.items() if k in notes)}
        taken.add(key)
        during = [x for x in tickets if first_at <= _at(x['start']) <= last_at]
        made = []
        for b in group + during:
            made += [{'key': k, 'at': at, 'text': text, 'event_id': b['event_id'], 'item': b['type']} for k, at, text in lines(b, lang)]
        ends = max((b.get('end') or b['start']) for b in group)[:10]
        if ends >= today:
            made += [{'key': k, 'at': at, 'text': text, 'item': 'gap', 'data': {'gap': 1, **({'until': until} if until else {})}}
                     for k, at, text, until in gaps(group, lang)]
        made.sort(key=_order)
        out.append({'key': key, 'title': _title(group), 'area': _area(accounts, first['account_id']), 'under': ['Trips'],
                    'starts': min(b['start'] for b in group)[:10], 'ends': ends, 'lines': made})
    gone = {hashlib.sha256(k.encode()).hexdigest()[:20] for k in canceled}
    gone |= {k for k in superseded - taken if _spare(db, k)}
    return out, (lambda key: key not in gone)


def trip_spans(db):
    """The journeys' spans, for event_notes.drafts: a ticket during a trip goes on the trip, not under Events."""
    return spans(journeys(bookings_now(db)[0]))

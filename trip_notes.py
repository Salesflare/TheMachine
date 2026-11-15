"""Trip notes (docs/help/notes.md, "Trips"): one note per journey under Trips, filled in from booking mail by plain code.

The mail source reads a confirmation's structured data (bookings.py) into the message's sealed metadata. collect()
copies each mail's bookings into trip_bookings (sealed at rest, message_seal.DERIVED), from a cursor over events, so a
round reads only new mail. Event tickets are kept there too, for event_notes.py; a trip leaves them out. drafts() then builds the trips from all of them, and NotesApp.trip_notes_step hands those
to note_pages.sync, which keeps the owner's own edits, moves and deletes on top.

How bookings become trips, without a model:
- One booking (a flight leg, a hotel stay, a train ride, a rental car) is known by its type, code, number and day. A
  later mail about the same one (a changed time, a seat) replaces it; a cancellation takes it out.
- Bookings that overlap or follow within a day are one journey, and so are bookings under the same booking code. A
  ride back to where the journey started, from where it went, within RETURN_DAYS joins it too, with no hotel between.
- The trip is named after where it goes: the first ride's destination, or the first hotel's town when there is no
  ride. Its days run from the first start to the last end.
- A trip keeps its note: bookings that are on a trip note already stay on that note (drafts), whatever order their
  mail is read in.
- Each booking is a line at its own time, in the owner's language, with its code and seat, and the mail it came from.
  A hotel and a rental car also get a line when they end (check-out, return the car).
- A trip whose bookings were all canceled goes. One whose mail aged out of the mailbox stays.

Tables (this module owns them): trip_bookings (one row per mail with bookings: the account it came in on, when, and its
rows) and trip_state (the cursor)."""
import datetime as dt
import hashlib
import json

from i18n import t
import mail_cleanup
import todo_areas

SCHEMA = '''
CREATE TABLE IF NOT EXISTS trip_bookings(event_id INTEGER PRIMARY KEY,account_id TEXT NOT NULL,occurred_at TEXT NOT NULL,rows TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS trip_state(id INTEGER PRIMARY KEY CHECK(id=1),cursor INTEGER NOT NULL DEFAULT 0);
'''
BATCH = 5000  # mails read per round: a Machine with a year of mail is through it in a few rounds, not a day
# Mail the Machine held before it read bookings (or before it read them as it does now) carries none in its metadata:
# the history worker reads the mailbox's held mail again once per WALK_VERSION, slowly, after its own history walk
# (HistoryApp.history_bookings). Raise it when bookings.py reads more than before.
WALK_VERSION = 1
NEAR = dt.timedelta(days=1, hours=12)  # bookings this close after each other are one journey
RETURN_DAYS = 31  # a ride back home this long after the way out still belongs to it
RIDES = ('flight', 'train', 'bus', 'boat')


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


def collect(db, limit=BATCH):
    """New mail since the cursor: each one with bookings is kept. Returns how many mails had some."""
    cursor = (db.execute('SELECT cursor FROM trip_state WHERE id=1').fetchone() or [0])[0]
    rows = db.execute(f"SELECT id,account_id,occurred_at,metadata FROM events WHERE id>? AND kind IN ({','.join('?' * len(mail_cleanup.MAIL_KINDS))}) "
                      'ORDER BY id LIMIT ?', (cursor, *mail_cleanup.MAIL_KINDS, limit)).fetchall()
    kept = 0
    for r in rows:
        kept += keep(db, r['id'], r['account_id'], r['occurred_at'], _meta(r['metadata']).get('bookings'))
    if rows:
        db.execute('INSERT INTO trip_state(id,cursor) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET cursor=excluded.cursor', (rows[-1]['id'],))
    return kept


def _at(value):
    """A booking's time as a datetime (a day alone: its start)."""
    try:
        return dt.datetime.fromisoformat(value if 'T' in value else value + 'T00:00')
    except (TypeError, ValueError):
        return None


def _ident(b):
    return '|'.join((b['type'], b.get('code', ''), b.get('number', '') or b.get('name', ''), b['start'][:10]))


def bookings_now(db):
    """Every booking as the latest mail about it says, canceled ones out: [{..., event_id, account_id}], by start.
    Also the identities that were canceled."""
    latest, canceled = {}, set()
    for r in db.execute('SELECT event_id,account_id,occurred_at,rows FROM trip_bookings ORDER BY occurred_at,event_id'):
        try:
            rows = json.loads(r['rows'])
        except (TypeError, ValueError):
            continue
        for b in rows if isinstance(rows, list) else ():
            if not isinstance(b, dict) or b.get('type') not in ('hotel', 'car', *RIDES) or not _at(b.get('start')):
                continue
            key = _ident(b)
            if b.get('status') == 'canceled':
                latest.pop(key, None)
                canceled.add(key)
                continue
            canceled.discard(key)
            latest[key] = {**b, 'event_id': r['event_id'], 'account_id': r['account_id'], 'seen': r['occurred_at']}
    return sorted(latest.values(), key=lambda b: (b['start'], b['type'])), canceled


def _end(b):
    return _at(b.get('end')) or _at(b['start'])


def journeys(found):
    """Bookings grouped into journeys: [[booking, ...]] in time order."""
    groups = []
    for b in found:
        start = _at(b['start'])
        last = groups[-1] if groups else None
        same_code = last and b.get('code') and any(x.get('code') == b['code'] for x in last)
        if last and (same_code or start <= max(_end(x) for x in last) + NEAR):
            last.append(b)
        else:
            groups.append([b])
    out = []
    for g in groups:  # a ride back home after days with no booking between joins the way out
        prev = out[-1] if out else None
        rides = [x for x in prev or () if x['type'] in RIDES]
        back = [x for x in g if x['type'] in RIDES]
        if (rides and back and back[0].get('from') and back[0]['from'] == rides[-1].get('to') and back[-1].get('to') == rides[0].get('from')
                and _at(back[0]['start']) - max(_end(x) for x in prev) <= dt.timedelta(days=RETURN_DAYS)):
            prev.extend(g)
        else:
            out.append(g)
    return out


def _title(group):
    ride = next((x for x in group if x['type'] in RIDES and x.get('to')), None)
    if ride:
        return ride['to']
    hotel = next((x for x in group if x['type'] == 'hotel' and x.get('where')), None)
    if hotel:
        return hotel['where']
    car = next((x for x in group if x['type'] == 'car' and x.get('from')), None)
    return car['from'] if car else t('Trip')


def _code(b, lang=None):
    more = [t('booking {}', b['code'], lang=lang)] if b.get('code') else []
    if b.get('seat'):
        more.append(t('seat {}', b['seat'], lang=lang))
    if b.get('ticket'):
        more.append(t('ticket {}', b['ticket'], lang=lang))
    return ''.join(', ' + x for x in more)


def _nights(b):
    start, end = _at(b['start']), _at(b.get('end') or '')
    return (end.date() - start.date()).days if end else 0


def lines(b, lang=None):
    """The lines one booking gives: (key, at, text)."""
    key = hashlib.sha256(_ident(b).encode()).hexdigest()[:16]
    route = t('{} to {}', b['from'], b['to'], lang=lang) if b.get('from') and b.get('to') else b.get('to') or b.get('from') or ''
    if b['type'] == 'hotel':
        nights = _nights(b)
        text = b['name'] + (', ' + t('{} nights', nights, lang=lang) if nights > 0 else '') + _code(b, lang)
        out = [(key, b['start'], text)]
        if b.get('end'):
            out.append((key + '-out', b['end'], t('Check out of {}', b['name'], lang=lang)))
        return out
    if b['type'] == 'car':
        what = ', '.join(x for x in (b.get('by'), b.get('name')) if x)
        text = t('Rental car', lang=lang) + (' ' + what if what else '') + (', ' + t('pick up in {}', b['from'], lang=lang) if b.get('from') else '') + _code(b, lang)
        out = [(key, b['start'], text)]
        if b.get('end'):
            out.append((key + '-back', b['end'], t('Return the rental car in {}', b.get('to') or b.get('from'), lang=lang) if (b.get('to') or b.get('from')) else t('Return the rental car', lang=lang)))
        return out
    word = {'flight': t('Flight', lang=lang), 'train': t('Train', lang=lang), 'bus': t('Bus', lang=lang), 'boat': t('Ferry', lang=lang)}[b['type']]
    name = ' '.join(x for x in (word, b.get('number') or (b.get('by') if b['type'] != 'flight' else '')) if x)
    return [(key, b['start'], name + (' ' + route if route else '') + _code(b, lang))]


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


def drafts(db, accounts, lang=None):
    """The trips as note_pages.sync drafts, and keep(key) for the trips no booking holds any more.

    A trip keeps the key of the note already made for it: the oldest trip note holding any of its bookings. Mail is
    read in the order it arrived on the Machine, not the order it was sent, so a journey's first booking can show up
    after its note was made (an older confirmation the history walk brings in later); a key from the bookings alone
    would then start a second note for the same journey. A machine-made trip note whose bookings all went to another
    trip's note goes, unless the owner put something of theirs on it."""
    found, canceled = bookings_now(db)
    (held, rank), taken, superseded = _kept(db), set(), set()
    out = []
    for group in journeys(found):
        first = min(group, key=lambda b: (b['seen'], b['start']))  # a new trip's key
        key = hashlib.sha256(_ident(first).encode()).hexdigest()[:20]
        mine = {hashlib.sha256(_ident(b).encode()).hexdigest()[:16] for b in group}
        before = {k for lkey in mine for k in held.get(lkey, ()) if k not in taken}
        if before:
            key = min(before, key=rank.__getitem__)
            superseded |= {k for k in before - {key} if all(lkey in mine for lkey, notes in held.items() if k in notes)}
        taken.add(key)
        made = []
        for b in group:
            made += [{'key': k, 'at': at, 'text': text, 'event_id': b['event_id'], 'item': b['type']} for k, at, text in lines(b, lang)]
        made.sort(key=lambda x: x['at'])
        out.append({'key': key, 'title': _title(group), 'area': _area(accounts, first['account_id']), 'under': ['Trips'],
                    'starts': min(b['start'] for b in group)[:10], 'ends': max((b.get('end') or b['start']) for b in group)[:10], 'lines': made})
    gone = {hashlib.sha256(k.encode()).hexdigest()[:20] for k in canceled}
    gone |= {k for k in superseded - taken if _spare(db, k)}
    return out, (lambda key: key not in gone)

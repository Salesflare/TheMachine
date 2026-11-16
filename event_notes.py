"""Event notes (docs/help/calendar.md, "Trips and events"): one dated note per event the owner has tickets for, under Events, filled in
from ticket mail by plain code.

Ticket sellers put a schema.org EventReservation in their confirmation mail, as airlines do with a flight: bookings.py
reads it into the message's sealed metadata and trip_notes.collect keeps it with the travel bookings (trip_bookings,
one cursor over mail for both). drafts() builds the events from those rows, and NotesApp.trip_notes_step hands them to
note_pages.sync, which keeps the owner's own edits, moves and deletes on top.

How tickets become events, without a model:
- One event is known by its name and first day. Every booking for it (a second order, a mail about more seats) is a
  line on that note. A later mail about the same booking replaces it, and a cancellation takes it out.
- A line says where, with the booking code, seat and ticket, at the event's time; one that runs into another day keeps
  its end too (data.until), so its date reads from start to end. The note's dates run from the first day to the last:
  a band in Calendar, like a trip.
- A to-do made from the ticket mail (pay, pick up the tickets) opens from its line.
- An event whose tickets were all canceled goes. One whose mail aged out of the mailbox stays.
- A ticket for something during a trip (a tour, a museum, a match while away) goes on that trip instead
  (trip_notes.drafts), so the journey is one band; an event note made before stays.
Its area is the mailbox's: a conference booked on the work address is Work. Tickets read from mail without structured
data (bookings.looks_booked, read by the model) come in the same way."""
import hashlib
import json

from i18n import t
import trip_notes


def tickets(db):
    """Every event booking as the latest mail about it says, canceled ones out: [{..., event_id, account_id, seen}] by
    start, and the canceled ones (their last rows)."""
    latest, canceled = {}, {}
    for r in db.execute('SELECT event_id,account_id,occurred_at,rows FROM trip_bookings ORDER BY occurred_at,event_id'):
        try:
            rows = json.loads(r['rows'])
        except (TypeError, ValueError):
            continue
        for b in rows if isinstance(rows, list) else ():
            if not isinstance(b, dict) or b.get('type') != 'event' or not b.get('name') or not trip_notes._at(b.get('start')):
                continue
            key = trip_notes._ident(b)
            if b.get('status') == 'canceled':
                latest.pop(key, None)
                canceled[key] = b
                continue
            canceled.pop(key, None)
            latest[key] = {**b, 'event_id': r['event_id'], 'account_id': r['account_id'], 'seen': r['occurred_at']}
    return sorted(latest.values(), key=lambda b: b['start']), list(canceled.values())


def _key(b):
    """The event's own key: its name and first day, the same for every booking for it."""
    return hashlib.sha256(('event|' + ' '.join(b['name'].casefold().split()) + '|' + b['start'][:10]).encode()).hexdigest()[:20]


def line(b, lang=None):
    """The line one booking gives: (key, at, text, until), until being its end when it runs into another day (the
    line's date reads "Fri 18 Dec 09:00 to Sat 19 Dec 17:30"), else None."""
    key = hashlib.sha256(trip_notes._ident(b).encode()).hexdigest()[:16]
    seats = int(b['guests']) if str(b.get('guests') or '').isdigit() else 0
    text = (t('At {}', b['where'], lang=lang) if b.get('where') else t('Tickets', lang=lang)) + (', ' + t('{} tickets (to an event)', seats, lang=lang) if seats > 1 else '')
    end = b.get('end') or ''
    return key, b['start'], text + trip_notes._code(b, lang), end if end[:10] > b['start'][:10] else None


def _todos(db, event_ids):
    """The to-do made from each mail, newest first: {event_id: suggestion id}."""
    if not event_ids:
        return {}
    found = {}
    for r in db.execute(f"SELECT s.id,j.value FROM suggestions s, json_each(s.event_ids) j WHERE j.value IN ({','.join('?' * len(event_ids))}) "
                        'ORDER BY s.created_at', sorted(event_ids)):
        found[r[1]] = r[0]
    return found


def drafts(db, accounts, lang=None):
    """The events as note_pages.sync drafts, and keep(key) for the events no booking holds any more."""
    found, canceled = tickets(db)
    during = trip_notes.trip_spans(db)
    found = [b for b in found if not trip_notes.on_a_trip(b, during)]  # a ticket during a trip is on the trip (trip_notes.drafts)
    todos = _todos(db, {b['event_id'] for b in found})
    groups = {}
    for b in found:
        groups.setdefault(_key(b), []).append(b)
    out = []
    for key, group in groups.items():
        first = min(group, key=lambda b: (b['seen'], b['start']))
        made = []
        for b in group:
            k, at, text, until = line(b, lang)
            data = {**({'until': until} if until else {}), **({'todo': todos[b['event_id']]} if b['event_id'] in todos else {})}
            made.append({'key': k, 'at': at, 'text': text, 'event_id': b['event_id'], 'item': 'event', **({'data': data} if data else {})})
        made.sort(key=lambda x: x['at'])
        out.append({'key': key, 'title': first['name'], 'area': trip_notes._area(accounts, first['account_id']), 'under': ['Events'],
                    'starts': min(b['start'] for b in group)[:10], 'ends': max((b.get('end') or b['start']) for b in group)[:10], 'lines': made})
    gone = {_key(b) for b in canceled} - set(groups)
    return out, (lambda key: key not in gone)

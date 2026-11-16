"""Trips and events, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

Trips (trip_notes.py) and events (event_notes.py) come in from booking and ticket mail in plain code and show in
Calendar as bands (calendar_notes); a band opens its page (note_page, read through /api/graph), each line with the
message it came from. They are kept in note_pages.py's tables. The Notes feature that used those tables too is gone:
its notes stay in the database untouched (note_pages, note_page_lines, note_page_links and the tables listed under
"Notes in the Graph" in machine/export/coverage.py), and no code reads or writes them."""
import json
import logging
from datetime import date, timedelta
from email.utils import parseaddr
from time import monotonic

import event_notes
import note_pages
import todo_areas
import trip_notes
from timeutil import now

LOG = logging.getLogger('personal-assistant')
EVENTS_EVERY = 3600  # seconds: the events brought up to date without new ticket mail (a to-do made later)


def _sender(metadata, mine):
    """The name a message came from (its From's name, else its address), or '' when it has none or the owner sent it.
    metadata: as Store.events gives it (read already), or its JSON."""
    try:
        meta = metadata if isinstance(metadata, dict) else json.loads(metadata or '{}')
    except (TypeError, ValueError):
        return ''
    name, address = parseaddr(str(meta.get('from') or '') if isinstance(meta, dict) else '')
    if not address or address.casefold() in mine:
        return ''
    return ' '.join(name.strip('"\' ').split())[:80] or address[:80]


class NotesApp:
    ACTIONS = {}

    def trip_notes_step(self):
        """Every ten minutes, plain code: new booking mail kept (trip_notes.collect), then the trips and events
        (event_notes.py) brought up to date when there was any. The events also once an hour without new mail, so a
        to-do made from a ticket mail later on opens from its line. Bookings the history worker found in mail held from
        before (HistoryApp.history_bookings) count as new mail, and so does the first round after a start. Returns the
        trips and events it changed."""
        try:
            accounts, clock = self.config.get('accounts') or [], monotonic()
            added = self.__dict__.pop('trip_bookings_added', False) or not getattr(self, 'trip_notes_built', False)
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                kept = trip_notes.collect(db) or added
                touched = []
                if kept:
                    found, keep = trip_notes.drafts(db, accounts)
                    touched = note_pages.sync(db, 'trip', found, now(), keep)
                if kept or clock - getattr(self, 'event_notes_at', -EVENTS_EVERY) >= EVENTS_EVERY:
                    self.event_notes_at = clock
                    found, keep = event_notes.drafts(db, accounts)
                    touched += note_pages.sync(db, 'event', found, now(), keep)
            self.trip_notes_built = True
            return touched
        except Exception as error:  # the next round tries again from the same mail
            LOG.warning('trip notes error=%s', type(error).__name__)
            if added:
                self.trip_bookings_added = True
            return []

    def calendar_notes(self, start, end):
        """The trips and events that touch the Calendar's window, as bands: a day either side, since the window's edges
        are instants and their dates are local days (the Calendar keeps what touches each week)."""
        try:
            first = (date.fromisoformat(start[:10]) - timedelta(days=1)).isoformat()
            last = (date.fromisoformat(end[:10]) + timedelta(days=1)).isoformat()
        except ValueError:
            return []
        with self.store.connect() as db:
            return [{k: x[k] for k in ('id', 'kind', 'name', 'starts', 'ends')} for x in note_pages.dated(db, first, last)]

    def note_page(self, node):
        """A trip's or an event's page, opened from its band in Calendar: each line with the message it came from (what
        and when), so it opens from there. Any other kind is not found (ValueError, a 404)."""
        with self.store.connect() as db:
            found = note_pages.page(db, node)
        todos = sorted({str(x['data']['todo']) for x in found['lines'] if isinstance(x.get('data'), dict) and x['data'].get('todo')})
        if todos:  # a ticket's line opens its to-do, while it is there
            with self.store.connect() as db:
                there = {r['id'] for r in db.execute(f"SELECT id FROM suggestions WHERE id IN ({','.join('?' * len(todos))})", todos)}
            for x in found['lines']:
                todo = str((x.get('data') or {}).get('todo') or '')
                if todo in there:
                    x['todo'] = todo
        ids = sorted({x['event_id'] for x in found['lines'] if x.get('event_id')})
        if ids:
            rows = {r['id']: r for r in self.store.events([a['id'] for a in self.config['accounts']], event_ids=ids)}
            mine = {str(a.get('email') or '').casefold() for a in self.config['accounts']} - {''}
            for x in found['lines']:
                r = rows.get(x.get('event_id'))
                if r:
                    x['source'] = {'id': r['id'], 'kind': r['kind'], 'title': r['title'][:200], 'occurred_at': r['occurred_at']}
                    who = _sender(r['metadata'], mine)
                    if who:  # a message says who it is from ("From Example Energy"), not its subject
                        x['source']['from'] = who
                elif x.get('event_id'):
                    x['source'] = {'gone': True}
        found['areas'] = todo_areas.areas(self.config.get('accounts') or [])
        return found

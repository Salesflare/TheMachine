"""Notes in the Graph, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

The Notes list and a note's page (read through /api/graph, like the Graph's other records) and the owner's edits
(NOTE_ACTIONS, from their dashboard only). The notes themselves, their kinds, the tree, links and how The Machine keeps
its own notes current: note_pages.py. A line that came from a fact is that fact: editing it edits the fact under What
I've learned first (Store.edit_fact), so there is one truth."""
import json
import logging
import threading
from datetime import date, timedelta
from email.utils import parseaddr
from time import monotonic

import event_notes
import health_notes
import help_chat
import home_notes
import kids_notes
import note_pages
import section_notes
import todo_areas
import trip_notes
from models import background_model
from timeutil import now, today

LOG = logging.getLogger('personal-assistant')
SECTION_KINDS = (home_notes.KIND, health_notes.KIND, kids_notes.KIND)  # the kinds kept in sections (section_notes.py)
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
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys((
        'note_delete',
        'note_edit',
        'note_line_add',
        'note_line_edit',
        'note_line_remove',
        'note_line_reset',
        'note_line_restore',
        'note_merge',
        'note_new',
        'note_restore',
        'note_unmerge',
    ), 'note_action')

    def note_areas(self):
        return [a['id'] for a in todo_areas.areas(self.config.get('accounts') or [])]

    def trip_notes_step(self):
        """Every ten minutes, plain code: new booking mail kept (trip_notes.collect), then the trips and events
        (event_notes.py) brought up to date when there was any. The events also once an hour without new mail, so a
        to-do made from a ticket mail later on opens from its line. Returns the notes it changed."""
        try:
            accounts, clock = self.config.get('accounts') or [], monotonic()
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                kept = trip_notes.collect(db)
                touched = []
                if kept:
                    found, keep = trip_notes.drafts(db, accounts)
                    touched = note_pages.sync(db, 'trip', found, now(), keep)
                if kept or clock - getattr(self, 'event_notes_at', -EVENTS_EVERY) >= EVENTS_EVERY:
                    self.event_notes_at = clock
                    found, keep = event_notes.drafts(db, accounts)
                    touched += note_pages.sync(db, 'event', found, now(), keep)
                return touched
        except Exception as error:  # the next round tries again from the same mail
            LOG.warning('trip notes error=%s', type(error).__name__)
            return []

    def section_notes_step(self):
        """About every six hours (section_notes.EVERY) for each kind in sections (Home, Health): its notes from plain
        code, with one small model call per kind over the candidates no call placed yet, in a thread of its own once
        the budget allows. Nothing new to place: no model, the notes still brought up to date. True when a round
        started."""
        running = getattr(self, 'section_notes_thread', None)
        if running and running.is_alive():
            return False
        at, accounts = now(), self.config.get('accounts') or []
        with self.store.connect() as db:
            section_notes.ensure(db)
            kinds = [k for k in SECTION_KINDS if section_notes.due(db, k, at)]
            ask = any(section_notes.unasked(db, k, k.candidates(db, accounts, today())) for k in kinds)
        if not kinds or ask and (self.background_pause(job='section-notes') or not self.background_spaced()):
            return False
        if ask:
            self.background_started()
        self.section_notes_thread = threading.Thread(target=lambda: [self.section_notes_run(k) for k in kinds], daemon=True, name='section-notes')
        self.section_notes_thread.start()
        return True

    def section_notes_ask(self, prompt):
        ask = getattr(self, 'section_notes_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                return ask(prompt)
            model = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=section_notes.TIMEOUT)
        except help_chat.Unavailable:
            return None

    def section_notes_run(self, kind):
        """One round of one kind: what is new placed by the model (kept, so it is asked once), then its notes synced.
        Returns the notes it changed."""
        accounts, at = self.config.get('accounts') or [], now()
        try:
            with self.store.connect() as db:
                section_notes.ensure(db)
                items = section_notes.unasked(db, kind, kind.candidates(db, accounts, today()))
                under = section_notes.notes_under(db, kind)
            placed = section_notes.reply(kind, self.section_notes_ask(section_notes.prompt(kind, items, under)), items, under) if items else {}
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                section_notes.remember(db, kind, placed or {}, at)
                section_notes.ran(db, kind, at)
                found, keep = section_notes.drafts(db, kind, kind.candidates(db, accounts, today()))
                touched = note_pages.sync(db, kind.kind, found, at, keep)
        except Exception as error:  # noqa: BLE001 - the next round tries again
            LOG.warning('section notes kind=%s error=%s', kind.kind, type(error).__name__)
            return []
        LOG.info('section notes kind=%s asked=%s placed=%s notes=%s', kind.kind, len(items), len(placed or {}), len(touched))
        return touched

    def calendar_notes(self, start, end):
        """The dated notes (trips, events) that touch the Calendar's window, as bands: a day either side, since the window's
        edges are instants and a note's dates are local days (the Calendar keeps what touches each week)."""
        try:
            first = (date.fromisoformat(start[:10]) - timedelta(days=1)).isoformat()
            last = (date.fromisoformat(end[:10]) + timedelta(days=1)).isoformat()
        except ValueError:
            return []
        with self.store.connect() as db:
            return [{k: x[k] for k in ('id', 'kind', 'name', 'starts', 'ends')} for x in note_pages.dated(db, first, last)]

    def notes_list(self, db):
        """The Notes list, light: what each row shows, in tree order."""
        return note_pages.listing(db, today().isoformat())

    def note_page(self, node):
        """One note's page (with the whole tree, light), each line with the message it came from (what and when), so it opens from there."""
        with self.store.connect() as db:
            found = note_pages.page(db, node)
            found['tree'] = note_pages.listing(db, today().isoformat())  # for Under and Merge into, and @ links
        todos = sorted({str(x['data']['todo']) for x in found['lines'] if isinstance(x.get('data'), dict) and x['data'].get('todo')})
        if todos:  # a bill's or a subscription's line opens its to-do, while it is there
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

    def note_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Notes are changed from the owner’s dashboard')
        at = now()
        if name == 'note_line_edit':  # one truth: a line from a fact edits that fact first (What I've learned says it too)
            with self.store.connect() as db:
                row = db.execute('SELECT fact_id FROM note_page_lines WHERE id=? AND removed_at IS NULL', (int(args.get('line') or 0),)).fetchone()
            if row and row['fact_id']:
                self.store.edit_fact(row['fact_id'], args.get('text'))
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if name == 'note_new':
                lines = args.get('lines') or []
                return note_pages.create(db, args.get('title'), args.get('area'), at, self.note_areas(),
                                         lines if isinstance(lines, list) else str(lines).splitlines(), args.get('starts'), args.get('ends'),
                                         parent=args.get('parent'))
            if name == 'note_edit':
                fields = {k: args[k] for k in ('title', 'area', 'starts', 'ends', 'parent') if k in args}
                return note_pages.edit(db, args.get('id'), at, self.note_areas(), **fields)
            if name in ('note_delete', 'note_restore', 'note_unmerge'):
                return {'note_delete': note_pages.remove, 'note_restore': note_pages.restore, 'note_unmerge': note_pages.unmerge}[name](db, args.get('id'), at)
            if name == 'note_merge':
                return note_pages.merge(db, args.get('id'), args.get('into'), at)
            if name == 'note_line_add':
                return note_pages.line_add(db, args.get('id'), args.get('text'), at, args.get('at'), args.get('links'))
            if name == 'note_line_edit':
                return note_pages.line_edit(db, args.get('line'), args.get('text'), at, args.get('links'))
            return {'note_line_reset': note_pages.line_reset, 'note_line_remove': note_pages.line_remove,
                    'note_line_restore': note_pages.line_restore}[name](db, args.get('line'), at)

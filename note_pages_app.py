"""Notes in the Graph, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

The Notes list and a note's page (read through /api/graph, like the Graph's other records) and the owner's edits
(NOTE_ACTIONS, from their dashboard only). The notes themselves, their kinds, the tree, links and how The Machine keeps
its own notes current: note_pages.py. A line that came from a fact is that fact: editing it edits the fact under What
I've learned first (Store.edit_fact), so there is one truth."""
import logging
import threading
from datetime import date, timedelta

import help_chat
import home_notes
import note_pages
import todo_areas
import trip_notes
from models import background_model
from timeutil import now, today

LOG = logging.getLogger('personal-assistant')


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
        """Every ten minutes, plain code: new booking mail kept (trip_notes.collect), then the trips brought up to date
        when there was any. Returns the notes it changed."""
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                if not trip_notes.collect(db):
                    return []
                found, keep = trip_notes.drafts(db, self.config.get('accounts') or [])
                return note_pages.sync(db, 'trip', found, now(), keep)
        except Exception as error:  # the next round tries again from the same mail
            LOG.warning('trip notes error=%s', type(error).__name__)
            return []

    def home_notes_step(self):
        """About every six hours (home_notes.EVERY): the Home notes from plain code, with one small model call over the
        candidates no call placed yet, in a thread of its own once the budget allows. Nothing new to place: no model,
        the notes still brought up to date. True when a round started."""
        running = getattr(self, 'home_notes_thread', None)
        if running and running.is_alive():
            return False
        at = now()
        with self.store.connect() as db:
            home_notes.ensure(db)
            if not home_notes.due(db, at):
                return False
            ask = home_notes.unasked(db, home_notes.candidates(db, self.config.get('accounts') or [], today()))
        if ask and (self.background_pause(job='home-notes') or not self.background_spaced()):
            return False
        if ask:
            self.background_started()
        self.home_notes_thread = threading.Thread(target=self.home_notes_run, daemon=True, name='home-notes')
        self.home_notes_thread.start()
        return True

    def home_notes_ask(self, prompt):
        ask = getattr(self, 'home_notes_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                return ask(prompt)
            model = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=home_notes.TIMEOUT)
        except help_chat.Unavailable:
            return None

    def home_notes_run(self):
        """One round: what is new placed by the model (kept, so it is asked once), then the notes synced. Returns the
        notes it changed."""
        accounts, at = self.config.get('accounts') or [], now()
        try:
            with self.store.connect() as db:
                items = home_notes.unasked(db, home_notes.candidates(db, accounts, today()))
            placed = home_notes.reply(self.home_notes_ask(home_notes.prompt(items)), items) if items else {}
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                home_notes.remember(db, placed or {}, at)
                home_notes.ran(db, at)
                found, keep = home_notes.drafts(db, home_notes.candidates(db, accounts, today()))
                touched = note_pages.sync(db, 'home', found, at, keep)
        except Exception as error:  # noqa: BLE001 - the next round tries again
            LOG.warning('home notes error=%s', type(error).__name__)
            return []
        LOG.info('home notes asked=%s placed=%s notes=%s', len(items), len(placed or {}), len(touched))
        return touched

    def calendar_notes(self, start, end):
        """The dated notes (trips) that touch the Calendar's window, as bands: a day either side, since the window's
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
            for x in found['lines']:
                r = rows.get(x.get('event_id'))
                if r:
                    x['source'] = {'id': r['id'], 'kind': r['kind'], 'title': r['title'][:200], 'occurred_at': r['occurred_at']}
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

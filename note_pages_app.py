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
import topic_notes
import trip_notes
from models import background_model
from timeutil import clock, local_tz, now, quiet_hours, today

LOG = logging.getLogger('personal-assistant')
SECTION_KINDS = (home_notes.KIND, health_notes.KIND, kids_notes.KIND)  # the kinds kept in sections (section_notes.py)
EVENTS_EVERY = 3600  # seconds: the events brought up to date without new ticket mail (a to-do made later)
SPACED_WAIT_SECONDS = 3600  # a due section round waits at most this long for the space between background turns


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
        to-do made from a ticket mail later on opens from its line. Bookings the history worker found in mail held from
        before (HistoryApp.history_bookings) count as new mail, and so does the first round after a start. Returns the
        notes it changed."""
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

    def section_notes_step(self):
        """About every six hours (section_notes.EVERY) for each kind in sections (Home, Health, Kids): its notes from
        plain code, with one small model call per kind over the candidates no call placed yet, in a thread of its own
        once the budget allows and there is space after the last background turn, or it waited SPACED_WAIT_SECONDS for
        that. Nothing new to place: no model, the notes still brought up to date. Conversations come in through
        topic_notes_step. True when a round started."""
        running = getattr(self, 'section_notes_thread', None)
        if running and running.is_alive():
            return False
        at, accounts = now(), self.config.get('accounts') or []
        with self.store.connect() as db:
            section_notes.ensure(db)
            kinds = [k for k in SECTION_KINDS if section_notes.due(db, k, at)]
            ask = kinds and any(section_notes.unasked(db, k, k.candidates(db, accounts, today())) for k in kinds)
        if not kinds:
            return False
        if ask and not self.notes_turn_free('section-notes'):
            return False
        self.section_notes_thread = threading.Thread(target=lambda: [self.section_notes_run(k) for k in kinds], daemon=True, name='section-notes')
        self.section_notes_thread.start()
        return True

    def notes_turn_free(self, job):
        """Whether a notes round that calls the model may start now: within the budget, and after the space since the
        last background turn, or once it waited SPACED_WAIT_SECONDS for that. Marks the turn started when it may."""
        if self.background_pause(job=job):
            return False
        # This step comes round once every ten minutes, and the space after the last background turn is ten minutes
        # too: work that runs more often (reviews, drafts ahead) took that space every time, and a round never came.
        # After SPACED_WAIT_SECONDS of waiting it goes anyway (still within the budget, background_pause above).
        waiting = self.__dict__.setdefault(job + '-waiting', monotonic())
        if not self.background_spaced() and monotonic() - waiting < SPACED_WAIT_SECONDS:
            return False
        self.__dict__.pop(job + '-waiting', None)
        self.background_started()
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
        """One round of one kind: what is new placed by the model (kept, so it is asked once), then its notes synced
        (section_notes_sync). Returns the notes it changed."""
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
        except Exception as error:  # noqa: BLE001 - the next round tries again
            LOG.warning('section notes kind=%s error=%s', kind.kind, type(error).__name__)
            return []
        touched = self.section_notes_sync(kind)
        LOG.info('section notes kind=%s asked=%s placed=%s notes=%s', kind.kind, len(items), len(placed or {}), len(touched))
        return touched

    def section_notes_sync(self, kind):
        """One kind's notes brought up to date in plain code: its candidates and the conversations placed in its parts
        (topic_notes.part_candidates). Returns the notes it changed."""
        accounts, at = self.config.get('accounts') or [], now()
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                section_notes.ensure(db)
                topic_notes.ensure(db)
                found, keep = section_notes.drafts(db, kind, [*kind.candidates(db, accounts, today()), *topic_notes.part_candidates(db, kind)])
                touched = note_pages.sync(db, kind.kind, found, at, keep)
                gone = note_pages.drop_empty_folder(db, [kind.folder])  # the kind has nothing left to show: no empty Health
                if gone:
                    touched.append(gone)
            return touched
        except Exception as error:  # noqa: BLE001 - the next round tries again
            LOG.warning('section notes sync kind=%s error=%s', kind.kind, type(error).__name__)
            return []

    def owner_slack_ids(self):
        accounts = self.config.get('accounts') or []
        return {a['user_id'] for a in accounts if a.get('service') == 'slack' and a.get('user_id')} | set(getattr(self.store, 'owner_user_ids', None) or ())

    def topic_notes_step(self):
        """Every topic_notes.EVERY (every FIRST_EVERY in the first fill, outside the quiet hours, topic_notes.filling):
        the owner's conversations no call placed yet sorted into notes, in a thread of its own once the budget allows
        (notes_turn_free). Nothing new to place, or too little to be worth a call yet (topic_notes.worth): no model,
        the notes still brought up to date. True when a round started."""
        running = getattr(self, 'topic_notes_thread', None)
        if running and running.is_alive():
            return False
        at = now()
        with self.store.connect() as db:
            topic_notes.ensure(db)
            if not topic_notes.due(db, at, topic_notes.FIRST_EVERY if not topic_notes.filled(db) else topic_notes.EVERY):
                return False  # after the first fill, conversations aren't even read between rounds
            pending = topic_notes.unasked(db, topic_notes.conversations(db, self.config.get('accounts') or [], today(), self.owner_slack_ids()))
            fast = (not topic_notes.quiet(clock(local_tz()), quiet_hours())) and topic_notes.filling(db, at, lambda: bool(pending))
            if not fast and not topic_notes.due(db, at, topic_notes.EVERY):
                return False
        waiting = bool(pending) and (fast or topic_notes.worth(pending, at))
        if waiting and not self.notes_turn_free('topic-notes'):
            return False
        calls = (topic_notes.FIRST_CALLS if fast else topic_notes.CALLS) if waiting else 0
        self.topic_notes_thread = threading.Thread(target=self.topic_notes_run, args=(calls,), daemon=True, name='topic-notes')
        self.topic_notes_thread.start()
        return True

    def topic_notes_ask(self, prompt):
        ask = getattr(self, 'topic_notes_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                return ask(prompt)
            model = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=topic_notes.TIMEOUT)
        except help_chat.Unavailable:
            return None

    def topic_notes_run(self, calls=topic_notes.CALLS):
        """One round: the conversations that went on keep their place (plain code); the ones no call placed yet go to
        the model ASK_MAX at a time, up to `calls` calls (each after the first waits for the budget and stops the round
        when it holds; a reply that isn't one keeps nothing and stops it too); then the notes started here and the
        kinds in sections are brought up to date. Returns how many conversations it placed."""
        accounts, done, slack = self.config.get('accounts') or [], 0, self.owner_slack_ids()
        try:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                topic_notes.ensure(db)
                section_notes.ensure(db)
                convs = topic_notes.conversations(db, accounts, today(), slack)
                topic_notes.refresh(db, convs)
                topic_notes.ran(db, now())
            for n in range(calls):
                if n and self.background_pause(job='topic-notes'):
                    break
                with self.store.connect() as db:
                    items = topic_notes.texts(db, topic_notes.unasked(db, convs), slack)
                    where, linked = topic_notes.places(db, SECTION_KINDS), topic_notes.records(db, items)
                if not items:
                    break
                text, refs = topic_notes.prompt(items, where, linked)
                placed = topic_notes.reply(self.topic_notes_ask(text), items, where, refs)
                if placed is None:
                    break
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    topic_notes.remember(db, items, placed, now(), SECTION_KINDS)
                done += len(items)
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                touched = note_pages.sync(db, 'topic', topic_notes.drafts(db), now())
        except Exception as error:  # noqa: BLE001 - the next round tries again
            LOG.warning('topic notes error=%s', type(error).__name__)
            return done
        for kind in SECTION_KINDS:
            touched += self.section_notes_sync(kind)
        LOG.info('topic notes placed=%s notes=%s', done, len(touched))
        return done

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

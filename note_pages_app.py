"""Notes in the Graph, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

The Notes list and a note's page (read through /api/graph, like the Graph's other records) and the owner's edits
(NOTE_ACTIONS, from their dashboard only). The notes themselves, their kinds, the tree, links and how The Machine keeps
its own notes current: note_pages.py. A line that came from a fact is that fact: editing it edits the fact under What
I've learned first (Store.edit_fact), so there is one truth."""
import logging

import note_pages
import todo_areas
import trip_notes
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

    def notes_list(self, db):
        """The Notes list, light: what each row shows, in tree order."""
        return note_pages.listing(db, today().isoformat())

    def note_page(self, node):
        """One note's page (with the whole tree, light), each line with the message it came from (what and when), so it opens from there."""
        with self.store.connect() as db:
            found = note_pages.page(db, node)
            found['tree'] = note_pages.listing(db, today().isoformat())  # for Under and Merge into, and @ links
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

"""Trips and events, kept as pages of lines: a band across their days in Calendar that opens their page.

trip_notes.py (booking mail) and event_notes.py (ticket mail) turn their sources into drafts and hand them to
sync(db, kind, drafts); calendar_notes and note_page (note_pages_app.py) read them. Each line says where it came from
(the message, event_id). The tables are note_pages, note_page_lines and note_page_links; a page's id is 'note:<id>'.
Not to be mixed up with the owner's notes on a to-do (decisions) or a meeting's notes (meeting_notes.py).

One truth, nothing that drifts: a page is built again from its sources (sync, one kind at a time, by a stable key per
page and per line). What an owner changed on one before stays on top: a renamed title (owner_title), changed dates
(owner_dates), a page moved (owner_parent), a line in their words (owner_text), a line or page removed (removed_at, so
a later sync never brings it back), a page merged into another (merged_into: its lines go on there).

The Notes feature (2026-11) kept its notes in these tables too, of other kinds ('note', 'topic', 'home', 'health',
'kids', 'memory', 'archived'), and in the tables of KEPT_SCHEMA. It is gone; its notes stay in the database as they
were, and no code reads or writes them. Only the folders trips and events go under ('Trips', 'Events', kind 'note')
are still found and made here.

Sharing: trips and events stay on the owner's Machine. None goes to a Fleet or the Team Graph."""
import datetime as dt
import json
import re

from i18n import t
from machine.owner_error import OwnerError

SCHEMA = '''
CREATE TABLE IF NOT EXISTS note_pages(id INTEGER PRIMARY KEY,kind TEXT NOT NULL,key TEXT UNIQUE,title TEXT NOT NULL,owner_title TEXT,
  area TEXT NOT NULL,starts TEXT,ends TEXT,owner_dates INTEGER NOT NULL DEFAULT 0,parent_id INTEGER,owner_parent INTEGER NOT NULL DEFAULT 0,
  merged_into INTEGER,moved_from INTEGER,by TEXT NOT NULL,data TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,removed_at TEXT);
CREATE INDEX IF NOT EXISTS note_pages_parent ON note_pages(parent_id);
CREATE TABLE IF NOT EXISTS note_page_lines(id INTEGER PRIMARY KEY,note_id INTEGER NOT NULL,key TEXT,pos REAL NOT NULL,at TEXT,item TEXT,
  text TEXT NOT NULL,owner_text TEXT,links TEXT,moved_from INTEGER,event_id INTEGER,fact_id INTEGER,data TEXT,by TEXT NOT NULL,created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,removed_at TEXT,UNIQUE(note_id,key));
CREATE INDEX IF NOT EXISTS note_page_lines_note ON note_page_lines(note_id,pos);
CREATE TABLE IF NOT EXISTS note_page_links(line_id INTEGER NOT NULL,note_id INTEGER NOT NULL,target TEXT NOT NULL,PRIMARY KEY(line_id,target));
CREATE INDEX IF NOT EXISTS note_page_links_target ON note_page_links(target);
'''
# The gone Notes feature's own tables, kept as they are (no drop, no flush; machine/export/coverage.py says where the
# export puts them): made empty on a Machine that never had them, so every Machine has the same tables. Nothing reads
# or writes them.
KEPT_SCHEMA = '''
CREATE TABLE IF NOT EXISTS section_topics(kind TEXT NOT NULL,key TEXT NOT NULL,section TEXT NOT NULL,note TEXT NOT NULL DEFAULT '',at TEXT NOT NULL,
  PRIMARY KEY(kind,key));
CREATE TABLE IF NOT EXISTS section_state(kind TEXT PRIMARY KEY,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS topic_routes(conv TEXT PRIMARY KEY,place TEXT NOT NULL,note TEXT,under TEXT,ongoing INTEGER NOT NULL DEFAULT 0,
  title TEXT,kind TEXT,event_id INTEGER,last_at TEXT,area TEXT,replied INTEGER NOT NULL DEFAULT 0,at TEXT NOT NULL,events TEXT,left TEXT);
CREATE TABLE IF NOT EXISTS topic_state(name TEXT PRIMARY KEY,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS topic_aliases(key TEXT PRIMARY KEY,target TEXT NOT NULL,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS note_writeups(note_id INTEGER PRIMARY KEY,page TEXT,basis TEXT,written_at TEXT,tried_at TEXT);
CREATE TABLE IF NOT EXISTS folder_overviews(note_id INTEGER PRIMARY KEY,page TEXT,basis TEXT,written_at TEXT,tried_at TEXT);
CREATE TABLE IF NOT EXISTS memory_seed_pages(page TEXT PRIMARY KEY,hash TEXT NOT NULL,tries INTEGER NOT NULL DEFAULT 0,lines INTEGER NOT NULL DEFAULT 0,
  read_at TEXT);
CREATE TABLE IF NOT EXISTS memory_seed_state(key TEXT PRIMARY KEY,value TEXT NOT NULL);
'''

# What each kind is. dated: its pages have a start and an end day (a band across those days in Calendar); personal:
# always the Personal area, never shared to a Fleet. 'note': the folders trips and events go under.
KINDS = {
    'note': {'label': 'Note', 'dated': False, 'personal': False},
    'trip': {'label': 'Trip', 'dated': True, 'personal': False},  # trip_notes.py: one trip, from its bookings, under Trips
    'event': {'label': 'Event', 'dated': True, 'personal': False},  # event_notes.py: one event the owner has tickets for, under Events
}
SHOWN = ('trip', 'event')  # the kinds Calendar shows and a page opens for
PERSONAL = 'personal'
TITLE_MAX, LINE_MAX, LINKS_MAX, DEPTH_MAX = 120, 1000, 20, 6
DAY = re.compile(r'\d{4}-\d{2}-\d{2}')
WHEN = re.compile(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?)?')


def ensure(db):
    for statement in (SCHEMA + KEPT_SCHEMA).split(';'):  # one at a time: executescript would commit an open transaction
        if statement.strip():
            db.execute(statement)


def node_id(note_id):
    return 'note:' + str(int(note_id))


def parse_id(value):
    """'note:12' or 12 -> 12."""
    text = str(value or '')
    text = text[5:] if text.startswith('note:') else text
    if not text.isdigit():
        raise ValueError('Not a note')
    return int(text)


def _title(value):
    title = ' '.join(str(value or '').split())
    if not title:
        raise OwnerError('Give the note a title')
    if len(title) > TITLE_MAX:
        raise OwnerError('Keep the title short')
    return title


def _text(value):
    text = '\n'.join(' '.join(part.split()) for part in str(value or '').strip().splitlines()).strip()
    if not text:
        raise OwnerError('A line needs some words')
    if len(text) > LINE_MAX:
        raise OwnerError('Keep a line shorter: split it in two')
    return text


def _day(value):
    value = str(value or '').strip()
    if not value:
        return None
    if not DAY.fullmatch(value):
        raise OwnerError('Pick a date')
    dt.date.fromisoformat(value)
    return value


def _when(value):
    value = str(value or '').strip()
    if not value:
        return None
    if not WHEN.fullmatch(value):
        raise ValueError('at is a date or a date and time')
    return value


def _dates(starts, ends):
    starts, ends = _day(starts), _day(ends)
    if ends and not starts:
        starts = ends
    if starts and not ends:
        ends = starts
    if starts and ends < starts:
        raise OwnerError('It ends before it starts.')
    return starts, ends


def _row(db, note_id):
    row = db.execute('SELECT * FROM note_pages WHERE id=? AND removed_at IS NULL', (note_id,)).fetchone()
    if not row:
        raise OwnerError('That note is gone')
    return row


def _touch(db, note_id, at):
    db.execute('UPDATE note_pages SET updated_at=? WHERE id=?', (at, note_id))


def _links(db, text, links, own=None):
    """The links of a line: [{id, name}] whose name is still in its words and whose record is there. own: the page
    the line is on (it doesn't link to itself)."""
    if not isinstance(links, list):
        return []
    folded, kept, seen = text.casefold(), [], set()
    for link in links[:LINKS_MAX * 2]:
        if not isinstance(link, dict):
            continue
        target, name = str(link.get('id') or ''), ' '.join(str(link.get('name') or '').split())
        if not target or not name or target in seen or name.casefold() not in folded or target == (own and node_id(own)):
            continue
        if target.startswith('note:'):
            ok = target[5:].isdigit() and db.execute('SELECT 1 FROM note_pages WHERE id=? AND removed_at IS NULL', (int(target[5:]),)).fetchone()
        else:
            ok = db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind IN ('person','org','project')", (target,)).fetchone()
        if ok:
            kept.append({'id': target, 'name': name[:TITLE_MAX]})
            seen.add(target)
        if len(kept) >= LINKS_MAX:
            break
    return kept


def _index(db, line_id, note_id, links):
    db.execute('DELETE FROM note_page_links WHERE line_id=?', (line_id,))
    for link in links or ():
        db.execute('INSERT OR IGNORE INTO note_page_links(line_id,note_id,target) VALUES(?,?,?)', (line_id, note_id, link['id']))


def _item(row, lines):
    title = row['owner_title'] or row['title']
    return {'id': node_id(row['id']), 'kind': row['kind'], 'name': title, 'area': row['area'], 'starts': row['starts'],
            'ends': row['ends'], 'by': row['by'], 'updated_at': row['updated_at'], 'lines': lines}


def dated(db, start, end):
    """The trips and events that touch the days start..end (ISO dates, end included): the Calendar's bands."""
    rows = db.execute(f"SELECT * FROM note_pages WHERE kind IN ({','.join('?' * len(SHOWN))}) AND removed_at IS NULL AND starts IS NOT NULL "
                      'AND starts<=? AND ends>=? ORDER BY starts,id', (*SHOWN, end, start)).fetchall()
    return [_item(r, None) for r in rows]


def _line(r):
    return {'id': r['id'], 'text': r['owner_text'] or r['text'], 'at': r['at'], 'item': r['item'] or '', 'by': r['by'],
            'edited': bool(r['owner_text']), 'event_id': r['event_id'], 'fact_id': r['fact_id'],
            'links': json.loads(r['links']) if r['links'] else [], **({'data': json.loads(r['data'])} if r['data'] else {})}


def page(db, note_id):
    """A trip or an event as its page shows it: its lines in time order (the ones without a time after them, a day
    without an hour after that day's hours)."""
    row = _row(db, parse_id(note_id))
    if row['kind'] not in SHOWN:
        raise ValueError('Not a note')
    lines = [_line(r) for r in db.execute("SELECT * FROM note_page_lines WHERE note_id=? AND removed_at IS NULL ORDER BY pos,by='owner',id", (row['id'],))]
    lines.sort(key=lambda x: (x['at'] is None, (x['at'] or '') + ('' if len(x['at'] or '') > 10 else 'T99')))
    return {**_item(row, len(lines)), 'created_at': row['created_at'], 'renamed': bool(row['owner_title']),
            'owner_dates': bool(row['owner_dates']), 'dated': True, 'lines': lines,
            **({'data': json.loads(row['data'])} if row['data'] else {})}


def _next_pos(db, note_id):
    return (db.execute('SELECT max(pos) FROM note_page_lines WHERE note_id=?', (note_id,)).fetchone()[0] or 0) + 1


def _merged_end(db, note_id):
    """The live page a merged page's lines go to now (merges can chain), or None."""
    seen = set()
    while note_id and note_id not in seen:
        seen.add(note_id)
        row = db.execute('SELECT id,merged_into,removed_at FROM note_pages WHERE id=?', (note_id,)).fetchone()
        if not row:
            return None
        if not row['merged_into']:
            return None if row['removed_at'] else row['id']
        note_id = row['merged_into']
    return None


def _sync_lines(db, note_id, drafts, at, merged=False):
    """One page's lines from its draft. merged: they go on a page an owner merged theirs into, beside its own lines
    (none of those goes, and theirs keep their place). Whether anything changed."""
    lines = {r['key']: r for r in db.execute('SELECT * FROM note_page_lines WHERE note_id=? AND key IS NOT NULL', (note_id,))}
    wanted, changed, base = set(), False, _next_pos(db, note_id) if merged else 1
    for n, line in enumerate(drafts):
        lkey, text = str(line['key']), _text(line['text'])
        wanted.add(lkey)
        links = _links(db, text, line.get('links'), note_id)
        old = lines.get(lkey)
        pos = old['pos'] if merged and old else base + n
        values = (pos, _when(line.get('at')), str(line.get('item') or ''), text, line.get('event_id'), line.get('fact_id'),
                  json.dumps(line['data'], sort_keys=True) if line.get('data') else None)
        stored = json.dumps(links) if links else None
        if not old:
            line_id = db.execute("INSERT INTO note_page_lines(note_id,key,pos,at,item,text,event_id,fact_id,data,links,by,created_at,updated_at) "
                                 "VALUES(?,?,?,?,?,?,?,?,?,?,'machine',?,?)", (note_id, lkey, *values, stored, at, at)).lastrowid
            _index(db, line_id, note_id, links)
            changed = True
        elif (old['pos'], old['at'], old['item'], old['text'], old['event_id'], old['fact_id'], old['data']) != values or (
                not old['owner_text'] and old['links'] != stored):
            db.execute('UPDATE note_page_lines SET pos=?,at=?,item=?,text=?,event_id=?,fact_id=?,data=?,updated_at=? WHERE id=?', (*values, at, old['id']))
            if not old['owner_text']:  # the owner's words keep the links they gave
                db.execute('UPDATE note_page_lines SET links=? WHERE id=?', (stored, old['id']))
                _index(db, old['id'], note_id, links)
            changed = True
    if not merged:
        for lkey, old in lines.items():
            if lkey not in wanted and old['by'] == 'machine' and not old['removed_at'] and not old['moved_from']:
                db.execute('DELETE FROM note_page_links WHERE line_id=?', (old['id'],))
                db.execute('DELETE FROM note_page_lines WHERE id=?', (old['id'],))
                changed = True
    if changed and merged:
        _touch(db, note_id, at)
    return changed


def _same(db, title, parent):
    """A page an owner started with this name in this place (no key yet), to fill in instead of starting a second one."""
    for row in db.execute('SELECT * FROM note_pages WHERE key IS NULL AND removed_at IS NULL AND merged_into IS NULL AND parent_id IS ? '
                          'ORDER BY id', (parent,)):
        if (row['owner_title'] or row['title']).casefold() == title.casefold():
            return row
    return None


def _folder(db, path, at):
    """The page a kind's pages go under (['Trips'], in English: its key), made once when it isn't there, titled in the
    owner's language. One an owner renamed or moved keeps its key, so it is still found there; one they merged leads to
    the page they merged it into; one they deleted stays deleted, and what would go in it goes where it was instead."""
    parent = None
    for depth in range(1, min(len(path), DEPTH_MAX) + 1):
        key = 'folder:' + '/'.join(p.casefold() for p in path[:depth])
        row = db.execute('SELECT id,removed_at,merged_into FROM note_pages WHERE key=?', (key,)).fetchone()
        if row and row['merged_into']:
            parent = _merged_end(db, row['id']) or parent
            continue
        if row and row['removed_at']:
            return parent
        if row:
            parent = row['id']
            continue
        own = _same(db, _title(t(path[depth - 1])), parent)
        if own:  # an owner's own Trips: it becomes the folder
            db.execute('UPDATE note_pages SET key=? WHERE id=?', (key, own['id']))
            parent = own['id']
            continue
        parent = db.execute("INSERT INTO note_pages(kind,key,title,area,parent_id,by,created_at,updated_at) VALUES('note',?,?,?,?,'machine',?,?)",
                            (key, _title(t(path[depth - 1])), PERSONAL, parent, at, at)).lastrowid
    return parent


def sync(db, kind, drafts, at, keep=None):
    """The trips or the events, from their sources. drafts: [{key, title, area, starts, ends, under, data, lines: [{key,
    text, at, item, event_id, fact_id, links, data}]}], the whole current set for that kind. under: the folder they go
    in (['Trips']); or inside: the key of a page of this kind earlier in drafts that it goes in (skipped while that one
    isn't there). A page or line not there yet is added; one that is changes to what its draft says (an owner's title,
    place, dates and words stay on top); a line its draft no longer has goes (not an owner's own lines). A page no draft
    has any more stays as it is unless keep says otherwise (keep(key) False: the source is gone, so is the page), so
    mail that ages out of the mailbox never takes a trip with it. A page or line removed stays removed. Returns the
    page ids it touched."""
    if kind not in SHOWN:
        raise ValueError('Not a kind The Machine keeps')
    touched, seen = [], set()
    for d in drafts:
        key = kind + ':' + str(d['key'])
        seen.add(key)
        starts, ends = _dates(d.get('starts'), d.get('ends')) if KINDS[kind]['dated'] else (None, None)
        title = ' '.join(str(d.get('title') or '').split())[:TITLE_MAX] or KINDS[kind]['label']
        area = PERSONAL if KINDS[kind]['personal'] else str(d.get('area') or PERSONAL)
        data = json.dumps(d['data'], sort_keys=True) if d.get('data') else None
        row = db.execute('SELECT * FROM note_pages WHERE key=?', (key,)).fetchone()
        if row and row['merged_into']:  # an owner merged it into another page: its lines go on there
            into = _merged_end(db, row['id'])
            if into:
                _sync_lines(db, into, d.get('lines') or (), at, merged=True)
            continue
        if row and row['removed_at']:
            continue
        if d.get('inside'):  # in another page of this kind, synced before it
            up = db.execute('SELECT id FROM note_pages WHERE key=? AND removed_at IS NULL AND merged_into IS NULL',
                            (kind + ':' + str(d['inside']),)).fetchone()
            if not up:
                continue
            parent = up['id']
        else:
            parent = _folder(db, [str(p) for p in d['under']], at) if d.get('under') else None
        own = None if row else _same(db, title, parent)
        if own:  # an owner's page of that name there: filled in beside their own lines, which stay theirs; their name stands
            shown = own['owner_title'] or own['title']
            db.execute('UPDATE note_pages SET key=?,kind=?,by=?,title=?,owner_title=? WHERE id=?',
                       (key, kind, 'machine', title, None if shown == title else shown, own['id']))
            row = db.execute('SELECT * FROM note_pages WHERE id=?', (own['id'],)).fetchone()
        if not row:
            note_id = db.execute('INSERT INTO note_pages(kind,key,title,area,starts,ends,parent_id,by,data,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                                 (kind, key, title, area, starts, ends, parent, 'machine', data, at, at)).lastrowid
            changed = True
        else:
            note_id = row['id']
            dates = (row['starts'], row['ends']) if row['owner_dates'] else (starts, ends)
            place = row['parent_id'] if row['owner_parent'] else parent
            changed = (row['title'], row['starts'], row['ends'], row['data'], row['area'], row['parent_id']) != (title, *dates, data, area, place)
            if changed:
                db.execute('UPDATE note_pages SET title=?,starts=?,ends=?,data=?,area=?,parent_id=? WHERE id=?', (title, *dates, data, area, place, note_id))
        changed = _sync_lines(db, note_id, d.get('lines') or (), at) or changed
        if changed:
            _touch(db, note_id, at)
            touched.append(node_id(note_id))
    if keep:
        for row in db.execute("SELECT id,key FROM note_pages WHERE kind=? AND by='machine' AND removed_at IS NULL", (kind,)).fetchall():
            if row['key'] not in seen and not keep(row['key'][len(kind) + 1:]):
                db.execute('DELETE FROM note_page_links WHERE note_id=?', (row['id'],))
                db.execute('DELETE FROM note_page_lines WHERE note_id=?', (row['id'],))
                db.execute('UPDATE note_pages SET parent_id=NULL WHERE parent_id=?', (row['id'],))
                db.execute('DELETE FROM note_pages WHERE id=?', (row['id'],))
                touched.append(node_id(row['id']))
    return touched

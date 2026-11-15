"""Notes in the Graph (2026-11-14): the readable overview of one subject, next to People, Organizations and Projects.

A note is a page of lines: a trip, a guide (the house, the car, how invoices are done), later health history. Each
line says where it came from: the owner wrote it, or The Machine wrote it from a message (event_id) or from what it
learned (fact_id). Not to be mixed up with the owner's notes on a to-do (decisions) or a meeting's notes
(meeting_notes.py): the tables here are note_pages, note_page_lines and note_page_links; a note's Graph id is
'note:<id>'.

Simple wiki, nothing more:
- A note can sit under another note (parent_id): Home > Appliances. The Notes list shows the tree. A note whose parent
  is deleted shows at the top until that parent comes back (Undo), so nothing is lost and nothing moves.
- A line can link to other notes and to people, organizations and projects. The text stays plain words: links holds
  which words are which record ([{id, name}], each name in the text), so no markup is ever shown. note_page_links
  indexes them for Linked from, on a note's page and on each record's page.

One truth, nothing that drifts:
- An owner's note is their own words, kept here.
- A note The Machine fills in by itself is built again from its sources (sync, one kind at a time, by a stable key per
  note and per line). The owner's edits stay on top: a renamed title (owner_title), changed dates (owner_dates), a
  note moved elsewhere in the tree (owner_parent), a line in their words (owner_text), a line or note removed
  (removed_at, so a later sync never brings it back).
- A line from a fact is that fact: editing it edits the fact (Store.edit_fact, under What I've learned), and the next
  sync shows the fact's words. note_pages_app.py does that part.

A kind is mostly a template: KINDS says whether its notes have dates (a trip: a band in Calendar) and whether they
are always Personal (health: never to a Fleet). An extractor elsewhere turns sources into drafts and hands them to
sync(db, kind, drafts), with where in the tree they go (under: ['Trips'], ['Home', 'Appliances']); everything else
(the page, edits, Undo, the tree, links, the Graph row) is shared by every kind.

Sharing: notes stay on the owner's Machine. None goes to a Fleet or the Team Graph yet."""
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

# What each kind is. dated: its notes have a start and an end day (a band across those days in Calendar); personal:
# always the Personal area, never shared to a Fleet. A new kind is a line here, its words in i18n/en.json, and an
# extractor that calls sync().
KINDS = {
    'note': {'label': 'Note', 'dated': False, 'personal': False},
    'trip': {'label': 'Trip', 'dated': True, 'personal': False},
    'home': {'label': 'Home', 'dated': False, 'personal': True},  # home_notes.py: a part of the home, under Home
}
OWNER_KINDS = ('note',)        # what the owner can start by hand (New note)
# The guidance The Machine builds the tree by. The starting tree: the top notes its own notes go under, each made only
# when a first real note lands in it (never an empty one). PLACING: the rules any code or model turn that adds notes
# follows; the owner's own moves, renames, merges and deletes always stand (owner_title, owner_parent, merged_into,
# removed_at) and teach where that subject goes: a folder keeps its key wherever the owner puts it, so later notes of
# that subject follow it there.
STARTING_TREE = ('Trips', 'Home', 'Health', 'Kids', 'Events', 'Car', 'Taxes', 'Pets')
PLACING = (
    'A subject earns its own note only with several facts or sources about it, never from one message.',
    'It goes under the starting tree note it belongs to (a trip under Trips, a fridge under Home > Appliances).',
    'A new top note outside the starting tree only for a subject that clearly comes back.',
    'Add to the note that already covers the subject instead of starting a second one.',
    'Where the owner moved, renamed, merged or deleted a note, that stands, and the same subject goes where they put it.',
)
PERSONAL = 'personal'
TITLE_MAX, LINE_MAX, LINES_MAX, ADD_MAX, LINKS_MAX, DEPTH_MAX = 120, 1000, 400, 50, 20, 6
DAY = re.compile(r'\d{4}-\d{2}-\d{2}')
WHEN = re.compile(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})?)?')
TARGET = re.compile(r'(?:note:\d+|(?:person|org|project):.+|[a-z]+:.+)')


def ensure(db):
    for statement in SCHEMA.split(';'):  # one at a time: executescript would commit an open transaction
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


def _area(kind, area, areas):
    """The note's area: Personal for a personal kind, else one of the owner's areas (Personal when it has none)."""
    if KINDS[kind]['personal']:
        return PERSONAL
    area = str(area or '').strip() or (areas[0] if areas else PERSONAL)
    if areas and area not in areas:
        raise ValueError('Not one of your areas')
    return area


def _row(db, note_id, removed=False):
    row = db.execute('SELECT * FROM note_pages WHERE id=?' + ('' if removed else ' AND removed_at IS NULL'), (note_id,)).fetchone()
    if not row:
        raise OwnerError('That note is gone')
    return row


def _touch(db, note_id, at):
    db.execute('UPDATE note_pages SET updated_at=? WHERE id=?', (at, note_id))


def _parent(db, note_id, parent):
    """The note a note goes under: a live note, never itself or one under it, and not too deep."""
    if parent in (None, ''):
        return None
    pid = parse_id(parent)
    _row(db, pid)
    seen, at = set(), pid
    while at is not None:
        if at == note_id:
            raise OwnerError('A note can’t go under itself')
        if at in seen or len(seen) >= DEPTH_MAX:
            raise OwnerError('That is too deep: pick a note higher up')
        seen.add(at)
        up = db.execute('SELECT parent_id FROM note_pages WHERE id=?', (at,)).fetchone()
        at = up['parent_id'] if up else None
    return pid


def _links(db, text, links, own=None):
    """The links of a line: [{id, name}] whose name is still in its words and whose record is there. own: the note
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


def count(db):
    return db.execute('SELECT count(*) FROM note_pages WHERE removed_at IS NULL').fetchone()[0]


def _item(row, lines):
    title = row['owner_title'] or row['title']
    return {'id': node_id(row['id']), 'kind': row['kind'], 'name': title, 'area': row['area'], 'starts': row['starts'],
            'ends': row['ends'], 'by': row['by'], 'updated_at': row['updated_at'], 'lines': lines,
            'parent': node_id(row['parent_id']) if row['parent_id'] else None}


def _order(items, today):
    """Dated notes that are on or still to come first (soonest first), then the rest by when they last changed, then
    dated ones that are over (latest first)."""
    ahead = sorted((x for x in items if x['ends'] and x['ends'] >= today), key=lambda x: (x['starts'], x['name'].casefold()))
    past = sorted((x for x in items if x['ends'] and x['ends'] < today), key=lambda x: x['starts'], reverse=True)
    rest = sorted((x for x in items if not x['ends']), key=lambda x: x['updated_at'], reverse=True)
    return ahead + rest + past


def listing(db, today):
    """Every note for the Notes list, in tree order: each note followed by the ones under it (depth says how far in).
    One under a deleted note shows at the top."""
    rows = db.execute('SELECT p.*,(SELECT count(*) FROM note_page_lines l WHERE l.note_id=p.id AND l.removed_at IS NULL) n '
                      'FROM note_pages p WHERE p.removed_at IS NULL').fetchall()
    items = {node_id(r['id']): _item(r, r['n']) for r in rows}
    under = {}
    for x in items.values():
        if x['parent'] not in items:
            x['parent'] = None
        under.setdefault(x['parent'], []).append(x)
    out = []

    def walk(parent, depth):
        for x in _order(under.get(parent, []), today):
            kids = under.get(x['id'], [])
            out.append({**x, 'depth': depth, 'children': len(kids)})
            if depth < DEPTH_MAX:
                walk(x['id'], depth + 1)
    walk(None, 0)
    return out


def dated(db, start, end):
    """Notes with dates that touch the days start..end (ISO dates, end included): the Calendar's bands."""
    rows = db.execute('SELECT * FROM note_pages WHERE removed_at IS NULL AND starts IS NOT NULL AND starts<=? AND ends>=? ORDER BY starts,id',
                      (end, start)).fetchall()
    return [_item(r, None) for r in rows]


def linked_from(db, target):
    """The notes with a line that links to target (a note's or a record's id), newest first: Linked from."""
    return [{'id': node_id(r['id']), 'name': r['owner_title'] or r['title'], 'kind': r['kind']} for r in db.execute(
        'SELECT DISTINCT p.id,p.title,p.owner_title,p.kind,p.updated_at FROM note_page_links k JOIN note_page_lines l ON l.id=k.line_id '
        'JOIN note_pages p ON p.id=k.note_id WHERE k.target=? AND l.removed_at IS NULL AND p.removed_at IS NULL ORDER BY p.updated_at DESC LIMIT 50',
        (str(target),))]


def find(db, text, limit=8):
    """Notes whose title holds every word asked: the Graph's search and the link picker."""
    words = [w for w in re.findall(r'\w+', str(text or '').casefold()) if w]
    if not words:
        return []
    rows = db.execute('SELECT * FROM note_pages WHERE removed_at IS NULL ORDER BY updated_at DESC').fetchall()
    return [_item(r, None) for r in rows if all(w in (r['owner_title'] or r['title']).casefold() for w in words)][:limit]


def _line(r):
    return {'id': r['id'], 'text': r['owner_text'] or r['text'], 'at': r['at'], 'item': r['item'] or '', 'by': r['by'],
            'edited': bool(r['owner_text']), 'event_id': r['event_id'], 'fact_id': r['fact_id'],
            'links': json.loads(r['links']) if r['links'] else [], **({'data': json.loads(r['data'])} if r['data'] else {})}


def page(db, note_id):
    """One note as its page shows it: where it sits (path), its lines in order, the notes under it and Linked from."""
    row = _row(db, parse_id(note_id))
    # in their place (an owner's line after The Machine's at the same place); a dated note's lines in time order, the
    # ones without a time after them, a day without an hour after that day's hours
    lines = [_line(r) for r in db.execute("SELECT * FROM note_page_lines WHERE note_id=? AND removed_at IS NULL ORDER BY pos,by='owner',id", (row['id'],))]
    if KINDS.get(row['kind'], KINDS['note'])['dated']:
        lines.sort(key=lambda x: (x['at'] is None, (x['at'] or '') + ('' if len(x['at'] or '') > 10 else 'T99')))
    path, at = [], row['parent_id']
    while at is not None and len(path) < DEPTH_MAX:
        up = db.execute('SELECT id,title,owner_title,parent_id,removed_at FROM note_pages WHERE id=?', (at,)).fetchone()
        if not up or up['removed_at']:
            break
        path.insert(0, {'id': node_id(up['id']), 'name': up['owner_title'] or up['title']})
        at = up['parent_id']
    children = [_item(r, None) for r in db.execute('SELECT * FROM note_pages WHERE parent_id=? AND removed_at IS NULL', (row['id'],))]
    return {**_item(row, len(lines)), 'parent': path[-1]['id'] if path else None, 'path': path, 'created_at': row['created_at'],
            'renamed': bool(row['owner_title']), 'owner_dates': bool(row['owner_dates']), 'dated': KINDS.get(row['kind'], KINDS['note'])['dated'],
            'lines': lines, 'children': _order(children, ''), 'linked_from': linked_from(db, node_id(row['id'])),
            **({'data': json.loads(row['data'])} if row['data'] else {})}


def _next_pos(db, note_id):
    return (db.execute('SELECT max(pos) FROM note_page_lines WHERE note_id=?', (note_id,)).fetchone()[0] or 0) + 1


def create(db, title, area, at, areas=(), lines=(), starts=None, ends=None, kind='note', parent=None):
    """The owner's own note: New note, optionally under another one. lines: its first lines, one per entry."""
    if kind not in OWNER_KINDS:
        raise ValueError('Not a kind of note the owner starts')
    starts, ends = _dates(starts, ends)
    pid = _parent(db, None, parent)
    note_id = db.execute('INSERT INTO note_pages(kind,title,area,starts,ends,owner_dates,parent_id,owner_parent,by,created_at,updated_at) '
                         'VALUES(?,?,?,?,?,?,?,1,?,?,?)', (kind, _title(title), _area(kind, area, list(areas)), starts, ends, int(bool(starts)),
                                                         pid, 'owner', at, at)).lastrowid
    for n, text in enumerate([t for t in lines if str(t or '').strip()][:ADD_MAX]):
        db.execute("INSERT INTO note_page_lines(note_id,pos,text,by,created_at,updated_at) VALUES(?,?,?,'owner',?,?)", (note_id, n + 1, _text(text), at, at))
    return {'id': node_id(note_id)}


def edit(db, note_id, at, areas=(), **fields):
    """Rename, move to another area or under another note (parent: a note's id, or empty for the top), set or clear
    the dates. On a note The Machine keeps, the owner's title, place and dates stay over what a later sync finds."""
    row = _row(db, parse_id(note_id))
    sets = {}
    if 'title' in fields:
        title = _title(fields['title'])
        if row['by'] == 'owner':
            sets['title'] = title
        else:
            sets['owner_title'] = None if title == row['title'] else title
    if 'area' in fields:
        sets['area'] = _area(row['kind'], fields['area'], list(areas))
    if 'parent' in fields:
        sets['parent_id'], sets['owner_parent'] = _parent(db, row['id'], fields['parent']), 1
    if 'starts' in fields or 'ends' in fields:
        sets['starts'], sets['ends'] = _dates(fields.get('starts'), fields.get('ends'))
        if KINDS.get(row['kind'], KINDS['note'])['dated'] and not sets['starts']:
            raise OwnerError('A trip has dates')
        sets['owner_dates'] = 1
    if not sets:
        return {'id': node_id(row['id']), 'unchanged': True}
    db.execute('UPDATE note_pages SET ' + ','.join(k + '=?' for k in sets) + ',updated_at=? WHERE id=?', (*sets.values(), at, row['id']))
    return {'id': node_id(row['id'])}


def remove(db, note_id, at):
    """Delete a note (Undo: restore). The notes under it show at the top meanwhile. A note The Machine keeps stays
    gone: its next sync doesn't make it again."""
    row = _row(db, parse_id(note_id))
    db.execute('UPDATE note_pages SET removed_at=? WHERE id=?', (at, row['id']))
    return {'id': node_id(row['id']), 'removed': True}


def restore(db, note_id, at):
    row = _row(db, parse_id(note_id), removed=True)
    db.execute('UPDATE note_pages SET removed_at=NULL,updated_at=? WHERE id=?', (at, row['id']))
    return {'id': node_id(row['id'])}


def line_add(db, note_id, text, at, when=None, links=None):
    """The owner adds lines at the end: each line of text becomes one, each with the links its words still hold."""
    row = _row(db, parse_id(note_id))
    parts = [p for p in str(text or '').splitlines() if p.strip()]
    if not parts:
        raise OwnerError('A line needs some words')
    if len(parts) > ADD_MAX or db.execute('SELECT count(*) FROM note_page_lines WHERE note_id=?', (row['id'],)).fetchone()[0] + len(parts) > LINES_MAX:
        raise OwnerError('That is too much for one note: start another one')
    pos, ids = _next_pos(db, row['id']), []
    for n, part in enumerate(parts):
        part = _text(part)
        kept = _links(db, part, links, row['id'])
        line_id = db.execute("INSERT INTO note_page_lines(note_id,pos,at,text,links,by,created_at,updated_at) VALUES(?,?,?,?,?,'owner',?,?)",
                             (row['id'], pos + n, _when(when), part, json.dumps(kept) if kept else None, at, at)).lastrowid
        _index(db, line_id, row['id'], kept)
        ids.append(line_id)
    _touch(db, row['id'], at)
    return {'id': node_id(row['id']), 'lines': ids}


def _line_row(db, line_id, removed=False):
    row = db.execute('SELECT l.* FROM note_page_lines l JOIN note_pages p ON p.id=l.note_id WHERE l.id=? AND p.removed_at IS NULL'
                     + ('' if removed else ' AND l.removed_at IS NULL'), (int(line_id),)).fetchone()
    if not row:
        raise OwnerError('That line is gone')
    return row


def line_edit(db, line_id, text, at, links=None):
    """The owner's words for a line. Their own line changes; a line The Machine wrote keeps its source and shows the
    owner's words over it (a later sync never writes over them); a line from a fact is that fact's words (the caller
    edits the fact). links: the records its words name (else the ones it had, where their names are still in it)."""
    row, text = _line_row(db, line_id), _text(text)
    kept = _links(db, text, links if links is not None else json.loads(row['links'] or '[]'), row['note_id'])
    stored = json.dumps(kept) if kept else None
    if row['by'] == 'owner':
        db.execute('UPDATE note_page_lines SET text=?,links=?,updated_at=? WHERE id=?', (text, stored, at, row['id']))
    elif row['fact_id']:
        db.execute('UPDATE note_page_lines SET text=?,owner_text=NULL,links=?,updated_at=? WHERE id=?', (text, stored, at, row['id']))
    else:
        db.execute('UPDATE note_page_lines SET owner_text=?,links=?,updated_at=? WHERE id=?', (None if text == row['text'] else text, stored, at, row['id']))
    _index(db, row['id'], row['note_id'], kept)
    _touch(db, row['note_id'], at)
    return {'id': row['id'], 'note': node_id(row['note_id']), **({'fact_id': row['fact_id']} if row['fact_id'] else {})}


def line_reset(db, line_id, at):
    """Back to what The Machine wrote: the owner's words on one of its lines go."""
    row = _line_row(db, line_id)
    db.execute('UPDATE note_page_lines SET owner_text=NULL,updated_at=? WHERE id=?', (at, row['id']))
    return {'id': row['id'], 'note': node_id(row['note_id'])}


def line_remove(db, line_id, at):
    row = _line_row(db, line_id)
    db.execute('UPDATE note_page_lines SET removed_at=? WHERE id=?', (at, row['id']))
    _touch(db, row['note_id'], at)
    return {'id': row['id'], 'note': node_id(row['note_id']), 'removed': True}


def line_restore(db, line_id, at):
    row = _line_row(db, line_id, removed=True)
    db.execute('UPDATE note_page_lines SET removed_at=NULL,updated_at=? WHERE id=?', (at, row['id']))
    _touch(db, row['note_id'], at)
    return {'id': row['id'], 'note': node_id(row['note_id'])}


def _merged_end(db, note_id):
    """The live note a merged note's lines go to now (merges can chain), or None."""
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
    """One note's lines from its draft. merged: they go on a note the owner merged theirs into, beside its own lines
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


def merge(db, note_id, into, at):
    """The owner merges a note into another: its lines go to the end of that one, the notes under it go under that
    one, and it is gone. A later sync of its subject adds to that one too. Undo: unmerge."""
    row, target = _row(db, parse_id(note_id)), _row(db, parse_id(into))
    if row['id'] == target['id']:
        raise OwnerError('Pick another note')
    at_ = target['parent_id']
    while at_ is not None:  # merging a note into one under it: that one takes its place in the tree
        if at_ == row['id']:
            db.execute('UPDATE note_pages SET parent_id=?,moved_from=? WHERE id=?', (row['parent_id'], row['id'], target['id']))
            break
        up = db.execute('SELECT parent_id FROM note_pages WHERE id=?', (at_,)).fetchone()
        at_ = up['parent_id'] if up else None
    base = _next_pos(db, target['id'])
    for n, line in enumerate(db.execute('SELECT id,key FROM note_page_lines WHERE note_id=? ORDER BY pos,id', (row['id'],)).fetchall()):
        key = line['key']
        if key and db.execute('SELECT 1 FROM note_page_lines WHERE note_id=? AND key=?', (target['id'], key)).fetchone():
            key = None  # the same line is there already: this one stays the owner's to remove
        db.execute('UPDATE note_page_lines SET note_id=?,pos=?,key=?,moved_from=? WHERE id=?', (target['id'], base + n, key, row['id'], line['id']))
    db.execute('UPDATE note_page_links SET note_id=? WHERE note_id=?', (target['id'], row['id']))
    db.execute('UPDATE note_pages SET parent_id=?,moved_from=? WHERE parent_id=? AND removed_at IS NULL', (target['id'], row['id'], row['id']))
    db.execute('UPDATE note_page_links SET target=? WHERE target=?', (node_id(target['id']), node_id(row['id'])))
    db.execute('UPDATE note_pages SET merged_into=?,removed_at=? WHERE id=?', (target['id'], at, row['id']))
    _touch(db, target['id'], at)
    return {'id': node_id(target['id']), 'merged': node_id(row['id'])}


def unmerge(db, note_id, at):
    """Undo a merge: the note is back with its own lines and the notes that were under it."""
    row = _row(db, parse_id(note_id), removed=True)
    if not row['merged_into']:
        raise OwnerError('That note wasn’t merged')
    lines = db.execute('SELECT id,note_id FROM note_page_lines WHERE moved_from=?', (row['id'],)).fetchall()
    for line in lines:
        db.execute('UPDATE note_page_lines SET note_id=?,moved_from=NULL WHERE id=?', (row['id'], line['id']))
        db.execute('UPDATE note_page_links SET note_id=? WHERE line_id=?', (row['id'], line['id']))
    db.execute('UPDATE note_pages SET parent_id=?,moved_from=NULL WHERE moved_from=? AND parent_id=?', (row['id'], row['id'], row['merged_into']))
    # the note it was merged into, when that sat under it: back under it
    db.execute('UPDATE note_pages SET parent_id=?,moved_from=NULL WHERE moved_from=?', (row['id'], row['id']))
    db.execute('UPDATE note_pages SET merged_into=NULL,removed_at=NULL,updated_at=? WHERE id=?', (at, row['id']))
    return {'id': node_id(row['id'])}


def _same(db, title, parent):
    """A note the owner started with this name in this place (no key yet), to fill in instead of starting a second one."""
    for row in db.execute('SELECT * FROM note_pages WHERE key IS NULL AND removed_at IS NULL AND merged_into IS NULL AND parent_id IS ? '
                          'ORDER BY id', (parent,)):
        if (row['owner_title'] or row['title']).casefold() == title.casefold():
            return row
    return None


def _folder(db, path, at):
    """The note a kind's notes go under (['Home', 'Appliances'], in English: its key), made once by The Machine when it
    isn't there, titled in the owner's language. A folder the owner renamed or moved keeps its key, so it is still
    found there; one they merged leads to the note they merged it into; one they deleted stays deleted, and what would
    go in it goes where it was instead."""
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
        if own:  # the owner's own Home: it becomes the folder, wherever they move it later
            db.execute('UPDATE note_pages SET key=? WHERE id=?', (key, own['id']))
            parent = own['id']
            continue
        parent = db.execute("INSERT INTO note_pages(kind,key,title,area,parent_id,by,created_at,updated_at) VALUES('note',?,?,?,?,'machine',?,?)",
                            (key, _title(t(path[depth - 1])), PERSONAL, parent, at, at)).lastrowid
    return parent


def sync(db, kind, drafts, at, keep=None):
    """The notes of one kind The Machine keeps, from its sources. drafts: [{key, title, area, starts, ends, under,
    data, lines: [{key, text, at, item, event_id, fact_id, links, data}]}], the whole current set for that kind. under:
    the folder notes it goes in (['Trips']); or inside: the key of a note of this kind earlier in drafts that it goes in
    (skipped while that one isn't there). A note or line not there yet is added; one that is changes to what its
    draft says (the owner's title, place, dates and words stay on top); a line its draft no longer has goes (not the
    owner's own lines). A note no draft has any more stays as it is unless keep says otherwise (keep(key) False: the
    source is gone, so is the note), so mail that ages out of the mailbox never takes a trip with it. A note or line
    the owner removed stays removed. Returns the note ids it touched."""
    if kind not in KINDS or kind in OWNER_KINDS:
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
        if row and row['merged_into']:  # the owner merged it into another note: its lines go on there
            into = _merged_end(db, row['id'])
            if into:
                _sync_lines(db, into, d.get('lines') or (), at, merged=True)
            continue
        if row and row['removed_at']:
            continue
        if d.get('inside'):  # in another note of this kind, synced before it (an owner's Dishwasher in Appliances)
            up = db.execute('SELECT id FROM note_pages WHERE key=? AND removed_at IS NULL AND merged_into IS NULL',
                            (kind + ':' + str(d['inside']),)).fetchone()
            if not up:
                continue
            parent = up['id']
        else:
            parent = _folder(db, [str(p) for p in d['under']], at) if d.get('under') else None
        own = None if row else _same(db, title, parent)
        if own:  # the owner's note of that name there: filled in beside their own lines, which stay theirs; their name stands
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

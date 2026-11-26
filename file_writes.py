"""Owner-approved edits to a Google Sheet or Slides file linked in a to-do: a doc_write edit (doc_writes.py) whose file
is one of these two kinds ({file_kind: sheets | slides}). Everything else is the doc edit's own: drafted against the
file as it is, pinned to that version, shown in the to-do before and after, written only after the owner's Save (or
their own word in the chat, do_now), once, and checked by reading back when the outcome is unclear.

Scopes: spreadsheets and presentations, from Google Docs' own sign-in with Allow edits to Sheets and Slides (a hosted
Machine's account page, docs_files_write_consent), or drive where a Docs connection already holds it. Reading with
them only reads; nothing here asks for a scope. A gog sign-in edits no Sheet or Slides file.

Sheets, at most MAX_CELLS cells in one write:
- {tab, cells, values}: values into cells of a tab ("B2", or "B2:C3" the size of values), the cells' values only.
- {tab, append}: rows after the tab's last row with anything in it.
- {add_tab, values?}: a new tab, its first rows from A1.
Values go in as they are (RAW): text stays text. formulas:true on a change enters its values as typed (USER_ENTERED),
only for a change with a formula ("=..."); the to-do says so. Google Sheets has no version to write against, so the
version is a digest of what the write depends on: the tabs, the cells it changes, and each appended tab's last row.
They are read again right before the write; if any differs, nothing is written.

Slides, pinned to Google's revisionId in the write itself (requiredRevisionId), in one batchUpdate:
- {slide, find, replace}: text replaced in the shapes and tables of one slide (every place it is on that slide).
- {add_slide, body, at?}: a new slide with a title and body text (Google's Title and body layout), at that number or
  last."""
from __future__ import annotations

import hashlib
import json
import re
import uuid

import google_files
from google_files import A1, SHEETS, SLIDES, letters, number

KINDS = (SHEETS, SLIDES)
EDIT_SCOPE = {SHEETS: 'https://www.googleapis.com/auth/spreadsheets',
              SLIDES: 'https://www.googleapis.com/auth/presentations'}
WHERE = {SHEETS: 'Google Sheets', SLIDES: 'Google Slides'}
MAX_CHANGES = 20
MAX_CELLS = 200      # cells one write sets, over all its changes
MAX_ROWS, MAX_COLS = 50, 26
MAX_VALUE = 2000     # characters of one cell
MAX_TAB = 100        # characters of a tab's name
MAX_FIND, MAX_REPLACE = 2000, 5000
MAX_TITLE, MAX_BODY = 200, 5000
MAX_SLIDES = 300
TEXT = 'text(textElements(textRun(content)))'
SHAPES = f'objectId,shape({TEXT}),table(tableRows(tableCells({TEXT})))'
SLIDE_FIELDS = f'title,revisionId,slides(objectId,pageElements({SHAPES},elementGroup(children({SHAPES}))))'
CONTROL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f￾￿]')


# ------------------------------------------------------------------------------------------- what the owner approves

def short(text, size=60):
    text = ' '.join(str(text).split())
    return text if len(text) <= size else text[:size - 1] + '…'


def _line(value, field, limit, newlines=False):
    if not isinstance(value, str) or len(value) > limit:
        raise ValueError(f'{field} is text of at most {limit:,} characters')
    if CONTROL.search(value):
        raise ValueError(f'{field} has control characters')
    value = value.replace('\r\n', '\n').replace('\r', '\n')
    if not newlines and '\n' in value:
        raise ValueError(f'{field} stays on one line')
    return value


def shown(value):
    """A cell's value as the owner reads it."""
    if isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return '' if value is None else str(value)


def _rows(value, field):
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_ROWS:
        raise ValueError(f'{field} is a list of 1 to {MAX_ROWS} rows, each a list of values')
    out = []
    for row in value:
        if not isinstance(row, list) or not 1 <= len(row) <= MAX_COLS:
            raise ValueError(f'Each row of {field} is a list of 1 to {MAX_COLS} values')
        kept = []
        for cell in row:
            if isinstance(cell, bool) or isinstance(cell, (int, float)) and cell == cell and abs(cell) < 1e15:
                kept.append(cell)
            else:
                kept.append(_line(cell, 'A value', MAX_VALUE, newlines=True))
        out.append(kept)
    return out


def _formulas(change, rows):
    """Whether this change's values go in as typed (formulas:true): only for one with a formula, and every formula
    needs it, so text that starts with "=" is never a formula by accident."""
    on = change.get('formulas', False)
    if on not in (True, False):
        raise ValueError('formulas is true or left out')
    has = [v for row in rows for v in row if isinstance(v, str) and v.lstrip().startswith('=')]
    if has and not on:
        raise ValueError(f'“{short(has[0])}” starts with "=": add formulas:true to the change to enter it as a formula, '
                         'or leave out the "=" for text')
    if on and not has:
        raise ValueError('formulas:true is only for a change with a formula (a value starting with "="): leave it out')
    return on


def _tab(value, field='tab'):
    name = ' '.join(_line(value, field, MAX_TAB).split())
    if not name:
        raise ValueError(f'{field} is the name of a tab')
    return name


def span(cells, rows):
    """The A1 range "B2:C3" that rows of values fill from cells ("B2", or "B2:C3" of that size), or ValueError."""
    found = A1.fullmatch(str(cells or '').strip().upper().replace('$', ''))
    if not found or not found[2] or found[3] and not found[4]:
        raise ValueError(f'cells is a cell like "B2", or a range like "B2:C3" ({cells!r} is not)')
    c1, r1 = number(found[1]), int(found[2])
    width, height = max(len(r) for r in rows), len(rows)
    if found[3]:
        c2, r2 = number(found[3]), int(found[4])
        if (c2 - c1 + 1, r2 - r1 + 1) != (width, height):
            raise ValueError(f'{cells} is {r2 - r1 + 1} by {c2 - c1 + 1} cells, but values has {height} rows of up to {width}: make them the same size')
    if r1 < 1 or c1 < 1:
        raise ValueError(f'{cells} is not a cell')
    return f'{letters(c1)}{r1}:{letters(c1 + width - 1)}{r1 + height - 1}'


def parse(kind, value):
    """The changes as given, checked for shape: [{tab, cells, values, formulas?} | {tab, append, formulas?} |
    {add_tab, values?, formulas?}] for a sheet, [{slide, find, replace} | {add_slide, body, at?}] for slides."""
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_CHANGES:
        raise ValueError(f'changes is a list of 1 to {MAX_CHANGES} changes')
    out, total = [], 0
    for change in value:
        keys = set(change) if isinstance(change, dict) else set()
        if kind == SHEETS:
            if keys - {'formulas'} == {'tab', 'cells', 'values'}:
                rows = _rows(change['values'], 'values')
                one = {'tab': _tab(change['tab']), 'cells': span(change['cells'], rows), 'values': rows}
            elif keys - {'formulas'} == {'tab', 'append'}:
                rows = _rows(change['append'], 'append')
                one = {'tab': _tab(change['tab']), 'append': rows}
            elif keys - {'formulas', 'values'} == {'add_tab'}:
                rows = _rows(change['values'], 'values') if 'values' in change else []
                one = {'add_tab': _tab(change['add_tab'], 'add_tab'), **({'values': rows} if rows else {})}
            else:
                raise ValueError('A change to a sheet is {tab, cells, values}, {tab, append} or {add_tab}, with formulas:true '
                                 'only for formulas')
            if _formulas(change, rows):
                one['formulas'] = True
            total += sum(len(r) for r in rows)
        elif keys == {'slide', 'find', 'replace'}:
            if not isinstance(change['slide'], int) or isinstance(change['slide'], bool) or not 1 <= change['slide'] <= MAX_SLIDES:
                raise ValueError('slide is the number of the slide, 1 for the first')
            find = _line(change['find'], 'find', MAX_FIND)
            if not find.strip():
                raise ValueError('find is the text to change')
            replace = _line(change['replace'], 'replace', MAX_REPLACE)
            if replace == find:
                raise ValueError(f'“{short(find)}” is replaced by the same text')
            one = {'slide': change['slide'], 'find': find, 'replace': replace}
        elif keys - {'at'} == {'add_slide', 'body'}:
            title = ' '.join(_line(change['add_slide'], 'add_slide', MAX_TITLE).split())
            body = '\n'.join(line.strip() for line in _line(change['body'], 'body', MAX_BODY, newlines=True).split('\n') if line.strip())
            if not title or not body:
                raise ValueError('A new slide has a title (add_slide) and body text')
            at = change.get('at')
            if at is not None and (not isinstance(at, int) or isinstance(at, bool) or not 1 <= at <= MAX_SLIDES):
                raise ValueError('at is the new slide\'s number, or left out for the end')
            one = {'add_slide': title, 'body': body, **({'at': at} if at else {})}
        else:
            raise ValueError('A change to slides is {slide, find, replace} or {add_slide, body, at}')
        out.append(one)
    if total > MAX_CELLS:
        raise ValueError(f'One write changes at most {MAX_CELLS} cells; this has {total}. Split it, or give the rest as text')
    return out


def tab_named(tabs, name):
    return next((t for t in tabs if t['title'].lower() == str(name).lower()), None)


def quoted(title, cells=''):
    return "'" + title.replace("'", "''") + "'" + ('!' + cells if cells else '')


def bounds(cells):
    found = A1.fullmatch(cells)
    return number(found[1]), int(found[2]), number(found[3]), int(found[4])


def cells_of(cells, rows):
    """[(A1 name, row index, column index)] of each cell rows fill from the top left of cells."""
    c1, r1, _, _ = bounds(cells)
    return [(f'{letters(c1 + j)}{r1 + i}', i, j) for i, row in enumerate(rows) for j in range(len(row))]


def resolve(kind, snapshot, changes):
    """The changes as the owner sees them, checked against the file as read: each with what it shows (shown: each cell
    before and after, or each shape's text). Raises ValueError with what to fix."""
    return (resolve_sheet if kind == SHEETS else resolve_slides)(snapshot, changes)


def resolve_sheet(snapshot, changes):
    tabs, out, taken = snapshot['tabs'], [], {}
    for change in changes:
        if 'add_tab' in change:
            if tab_named(tabs, change['add_tab']) or any(c.get('add_tab', '').lower() == change['add_tab'].lower() for c in out):
                raise ValueError(f'A tab named “{change["add_tab"]}” is there already. Pick another name, or change its cells')
            out.append({**change, 'shown': [{'cell': name, 'after': shown(change['values'][i][j])}
                                            for name, i, j in cells_of(f'A1:{letters(MAX_COLS)}{MAX_ROWS}', change.get('values') or [])]})
            continue
        tab = tab_named(tabs, change['tab'])
        if not tab or tab.get('kind', 'GRID') != 'GRID':
            raise ValueError(f'“{change["tab"]}” is not a tab with cells in this sheet. Its tabs: '
                             + ', '.join(f'“{t["title"]}”' for t in tabs if t.get('kind', 'GRID') == 'GRID'))
        change = {**change, 'tab': tab['title']}
        if 'append' in change:
            width = max(len(r) for r in change['append'])
            if width > tab['cols']:
                raise ValueError(f'“{tab["title"]}” has {tab["cols"]} columns; a new row has {width} values')
            last, row = (snapshot.get('last') or {}).get(tab['title'], (None, None))
            if last is None:
                raise ValueError('The sheet could not be read for this change just now. Nothing was saved; try again')
            out.append({**change, 'row': last + 1, 'last': [shown(v) for v in row or []][:MAX_COLS],
                        'shown': [{'cell': name, 'after': shown(change['append'][i][j])}
                                  for name, i, j in cells_of(f'A{last + 1}:A{last + 1}', change['append'])]})
            continue
        c1, r1, c2, r2 = bounds(change['cells'])
        if c2 > tab['cols'] or r2 > tab['rows']:
            raise ValueError(f'{change["cells"]} is outside “{tab["title"]}” ({tab["rows"]} rows, {tab["cols"]} columns)')
        for c, r1x, c2x, r2x in taken.get(tab['title'], ()):
            if c1 <= c2x and c <= c2 and r1 <= r2x and r1x <= r2:
                raise ValueError(f'Two changes touch the same cells in “{tab["title"]}”. Make them one')
        taken.setdefault(tab['title'], []).append((c1, r1, c2, r2))
        read = (snapshot.get('cells') or {}).get(quoted(tab['title'], change['cells']))
        if read is None:
            raise ValueError('The sheet could not be read for this change just now. Nothing was saved; try again')
        cells = [{'cell': name, 'before': read['shown'][i][j], 'after': shown(change['values'][i][j])}
                 for name, i, j in cells_of(change['cells'], change['values'])]
        if all(c['before'] == c['after'] for c in cells):
            raise ValueError(f'{change["cells"]} in “{tab["title"]}” holds these values already')
        out.append({**change, 'shown': cells})
    return out


def resolve_slides(snapshot, changes):
    slides, out, count = snapshot['slides'], [], len(snapshot['slides'])
    for change in changes:
        if 'add_slide' in change:
            count += 1
            at = change.get('at') or count
            if at > count:
                raise ValueError(f'at is at most {count}: the slides number 1 to {count - 1} now')
            out.append({**change, 'at': at})
            continue
        n = change['slide']
        if n > len(slides):
            raise ValueError(f'There is no slide {n}: these slides number 1 to {len(slides)}')
        texts = [text for _, text in slides[n - 1]['texts']]
        if not any(change['find'] in text for text in texts):
            raise ValueError(f'“{short(change["find"])}” is not on slide {n}. Copy it exactly from its text (assistant doc-draft prints it)')
        for earlier in out:
            if earlier.get('slide') == n and (change['find'] in earlier['find'] or earlier['find'] in change['find']
                                              or change['find'] in earlier['replace']):
                raise ValueError(f'Two changes touch “{short(change["find"])}” on slide {n}. Make them one')
        out.append({**change, 'slide_id': slides[n - 1]['id'],
                    'shown': [{'before': text, 'after': text.replace(change['find'], change['replace'])}
                              for text in texts if change['find'] in text]})
    return out


def validate(value, known, account, snapshot, result):
    """An edit to a linked Sheet or Slides file (doc_writes.validate's edit, for these kinds): result with its changes
    resolved and its version, or ValueError."""
    kind = known['kind']
    if set(value) - {'kind', 'op', 'label', 'file_id', 'changes', 'account_id', 'last', 'then'}:
        raise ValueError('An edit has file_id and changes only')
    if not account or kind not in (account.get('writes') or ()):
        raise ValueError(f'Editing {WHERE[kind]} is not allowed for this Google Docs connection yet (Allow edits to Sheets and '
                         'Slides on its connection). Give the changes as text in the to-do instead')
    changes = parse(kind, value.get('changes'))
    if not isinstance(snapshot, dict):
        raise ValueError(str(snapshot or 'The file could not be read just now') + '. Nothing was saved; try again')
    result.update(account_id=known['account_id'], provider='google', file_id=snapshot['file_id'], file_kind=kind,
                  doc_title=str(snapshot.get('title') or 'the file')[:200], version=snapshot['version'], url=snapshot['url'],
                  changes=resolve(kind, snapshot, changes))
    return result


def done(action):
    n = len(action['changes'])
    return f'Saved {n} change{"s" if n > 1 else ""} to “{action["doc_title"]}”'


def change_lines(change):
    if 'find' in change:
        return [f'Slide {change["slide"]}:'] + [x for c in change['shown'] for x in ('Before: ' + c['before'], 'After: ' + c['after'])]
    if 'add_slide' in change:
        return [f'New slide {change["at"]}: {change["add_slide"]}', change['body']]
    how = ' (entered as formulas)' if change.get('formulas') else ''
    if 'add_tab' in change:
        head = f'New tab “{change["add_tab"]}”{how}' + (':' if change['shown'] else '')
    elif 'append' in change:
        head = f'Add {len(change["append"])} row{"s" if len(change["append"]) > 1 else ""} to “{change["tab"]}” after row {change["row"] - 1}{how}:'
    else:
        head = f'Cells {change["cells"]} in “{change["tab"]}”{how}:'
    return [head] + [f'{c["cell"]}: ' + (f'“{c["before"]}” becomes ' if c.get('before') else '') + f'“{c["after"]}”'
                     for c in change['shown']]


def preview(action):
    n = len(action['changes'])
    blocks = [f'Edit “{action["doc_title"]}” in {WHERE[action["file_kind"]]}: {n} change{"s" if n > 1 else ""}']
    for i, change in enumerate(action['changes'], 1):
        blocks.append((f'{i}. ' if n > 1 else '') + '\n'.join(change_lines(change)))
    return '\n\n'.join(blocks)


def new_text(action):
    """Every value and text this edit puts in, for the checks on what goes out (next_actions.check)."""
    out = []
    for c in action.get('changes') or ():
        out += [shown(v) for row in c.get('values') or c.get('append') or () for v in row]
        out += [c[k] for k in ('replace', 'add_tab', 'add_slide', 'body') if isinstance(c.get(k), str)]
    return '\n'.join(out)


def failed(action, status, reason=None):
    """The to-do's line when Google refused the write: what was refused, and that nothing changed."""
    import doc_writes  # noqa: PLC0415 - Google's labels, one list
    where = WHERE[action['file_kind']]
    if status in (409, 412):
        return 'The file changed since this was drafted. Nothing was changed; ask for a new draft.'
    if reason in doc_writes.TURNED_OFF:
        return f'{where} is turned off for this Google sign-in, so it can’t change the file. Nothing was changed.'
    if reason in doc_writes.NO_SCOPE:
        return 'This sign-in may read Sheets and Slides but not change them. Nothing was changed.'
    if reason in doc_writes.BUSY:
        return f'{where} is too busy for this account right now. Nothing was changed; try again in a few minutes.'
    if reason in doc_writes.POLICY:
        return 'Your organization’s Google settings don’t allow this. Nothing was changed.'
    if status == 403:
        return 'This account can view the file but not edit it. Nothing was changed; ask the file’s owner for edit access.'
    return f'{where} refused the changes (error {status}). Nothing was changed; try again or ask for a new draft.'


def link(kind, file_id):
    return (f'https://docs.google.com/spreadsheets/d/{file_id}/edit' if kind == SHEETS
            else f'https://docs.google.com/presentation/d/{file_id}/edit')


# ------------------------------------------------------------------------------------------- the file as it is

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:32]


def padded(rows, height, width):
    rows = [list(r) if isinstance(r, list) else [] for r in (rows or [])][:height]
    return [(r + [''] * width)[:width] for r in rows + [[]] * (height - len(rows))]


def snapshot(writer, file_id, kind, changes=()):
    """The file as it is now, for an edit: its title, link and version; a sheet's tabs and the cells these changes
    touch, a deck's slides with each shape's text. `changes` parsed or resolved (parse, resolve)."""
    return (sheet_snapshot if kind == SHEETS else slides_snapshot)(writer, file_id, changes)


def sheet_snapshot(writer, file_id, changes):
    about = writer.file_call(SHEETS, 'sheets.spreadsheets.get', {'spreadsheetId': file_id, 'fields': google_files.SHEET_FIELDS})
    tabs = [{'id': int(p.get('sheetId') or 0), 'title': str(p.get('title') or ''), 'kind': p.get('sheetType', 'GRID'),
             'rows': google_files.grid(p)[0], 'cols': google_files.grid(p)[1], 'hidden': bool(p.get('hidden'))}
            for p in (s.get('properties') or {} for s in about.get('sheets') or [] if isinstance(s, dict)) if p.get('title')]
    sets, wholes = [], []
    for change in changes or ():
        tab = tab_named(tabs, change.get('tab') or '')
        if not tab or tab['kind'] != 'GRID':
            continue
        if 'cells' in change:
            c1, r1, c2, r2 = bounds(change['cells'])
            if c2 <= tab['cols'] and r2 <= tab['rows'] and quoted(tab['title'], change['cells']) not in sets:
                sets.append(quoted(tab['title'], change['cells']))
        elif 'append' in change and quoted(tab['title']) not in wholes:
            wholes.append(quoted(tab['title']))
    raw = shown_rows = []
    if sets or wholes:
        raw = writer.file_call(SHEETS, 'sheets.spreadsheets.values.batchGet', {
            'spreadsheetId': file_id, 'ranges': sets + wholes, 'valueRenderOption': 'FORMULA'}).get('valueRanges') or []
    if sets:
        shown_rows = writer.file_call(SHEETS, 'sheets.spreadsheets.values.batchGet', {
            'spreadsheetId': file_id, 'ranges': sets, 'valueRenderOption': 'FORMATTED_VALUE'}).get('valueRanges') or []
    cells, last = {}, {}
    for i, name in enumerate(sets):
        c1, r1, c2, r2 = bounds(name.rpartition('!')[2])
        values = padded((raw[i] if i < len(raw) else {}).get('values'), r2 - r1 + 1, c2 - c1 + 1)
        looks = padded((shown_rows[i] if i < len(shown_rows) else {}).get('values'), r2 - r1 + 1, c2 - c1 + 1)
        cells[name] = {'raw': values, 'shown': [[shown(f) if isinstance(f, str) and f.startswith('=') else shown(s)
                                                for f, s in zip(fr, sr)] for fr, sr in zip(values, looks)]}
    for k, name in enumerate(wholes):
        rows = (raw[len(sets) + k] if len(sets) + k < len(raw) else {}).get('values') or []
        while rows and not any(shown(v).strip() for v in rows[-1] or []):
            rows = rows[:-1]
        last[name[1:-1].replace("''", "'")] = (len(rows), list(rows[-1]) if rows else [])
    version = digest({'tabs': [[t['id'], t['title']] for t in tabs], 'cells': {k: v['raw'] for k, v in cells.items()},
                      'last': {k: [n, [shown(x) for x in row]] for k, (n, row) in last.items()}})
    return {'file_id': file_id, 'kind': SHEETS, 'version': version, 'title': str((about.get('properties') or {}).get('title') or ''),
            'url': link(SHEETS, file_id), 'tabs': tabs, 'cells': cells, 'last': last}


def raw_text(text):
    """A shape's text as Google holds it (what replaceAllText matches), without its last newline."""
    runs = ((e.get('textRun') or {}).get('content') for e in (text or {}).get('textElements') or [] if isinstance(e, dict))
    return ''.join(str(r or '') for r in runs).rstrip('\n')


def shape_texts(element, depth=0):
    """[(objectId, text)] of one thing on a slide: a shape, each cell of a table, and what a group holds."""
    if not isinstance(element, dict):
        return []
    out = []
    if isinstance(element.get('shape'), dict):
        out.append((element.get('objectId'), raw_text(element['shape'].get('text'))))
    for row in (element.get('table') or {}).get('tableRows') or []:
        out += [(element.get('objectId'), raw_text(c.get('text'))) for c in row.get('tableCells') or []]
    if depth < 2:
        for child in (element.get('elementGroup') or {}).get('children') or []:
            out += shape_texts(child, depth + 1)
    return [(i, t) for i, t in out if t]


def slides_snapshot(writer, file_id, changes=()):
    about = writer.file_call(SLIDES, 'slides.presentations.get', {'presentationId': file_id, 'fields': SLIDE_FIELDS})
    slides = [{'id': str(s.get('objectId') or ''), 'texts': [x for e in s.get('pageElements') or [] for x in shape_texts(e)]}
              for s in about.get('slides') or [] if isinstance(s, dict)]
    return {'file_id': file_id, 'kind': SLIDES, 'version': str(about.get('revisionId') or ''), 'title': str(about.get('title') or ''),
            'url': link(SLIDES, file_id), 'slides': slides}


def outline(found):
    """What doc-draft prints of a file before its changes are drafted: a sheet's tabs, or each slide's text."""
    if found['kind'] == SHEETS:
        return {'tabs': [{'title': t['title'], 'rows': t['rows'], 'columns': t['cols']} for t in found['tabs'] if t['kind'] == 'GRID'],
                'read': 'Read its cells with assistant doc --file <id> --range "Tab!A1:H50"'}
    return {'slides': [{'n': i + 1, 'text': [t for _, t in s['texts']]} for i, s in enumerate(found['slides'])]}


# ------------------------------------------------------------------------------------------- the one write

def preflight(writer, action):
    if action['file_kind'] == SLIDES:  # set once, before the write: a new slide's id, what reconcile looks for
        action.setdefault('proof', {}).setdefault('token', uuid.uuid4().hex)
    current = snapshot(writer, action['file_id'], action['file_kind'], action['changes'])
    if current['version'] != action['version']:
        from machine.owner_error import OwnerError  # noqa: PLC0415
        raise OwnerError('The file changed since this was drafted. Nothing was changed; ask for a new draft.')
    resolve(action['file_kind'], current, [{k: v for k, v in c.items() if k in ('tab', 'cells', 'values', 'append', 'add_tab', 'formulas',
                                                                             'slide', 'find', 'replace', 'add_slide', 'body', 'at')}
                                           for c in action['changes']])


def object_ids(action, i):
    token = re.sub(r'[^0-9a-f]', '', str((action.get('proof') or {}).get('token') or ''))[:20]
    base = f'tm{token}s{i}'
    return base, base + 't', base + 'b'


def edit(writer, action, error_type):
    """The write itself, against the version the owner approved; {'rejected': 409} when the file moved on. A refusal after
    a first write went through is an unclear outcome ({}): reconcile reads the file, nothing is written twice."""
    kind, file_id = action['file_kind'], action['file_id']
    current = snapshot(writer, file_id, kind, action['changes'])
    if current['version'] != action['version']:
        return {'rejected': 409}
    if kind == SLIDES:
        if any('add_slide' in c for c in action['changes']) and not (action.get('proof') or {}).get('token'):
            return {'rejected': 409}  # a new slide's id comes from preflight's token; never one a retry could not find
        writer.file_call(SLIDES, 'slides.presentations.batchUpdate', {'presentationId': file_id}, write=True,
                         body={'requests': slide_requests(action), 'writeControl': {'requiredRevisionId': action['version']}})
        return {'message_id': 'docwrite:' + file_id}
    structure, data = [], {False: [], True: []}
    for change in action['changes']:
        rows = change.get('values') or change.get('append') or []
        if 'add_tab' in change:
            structure.append({'addSheet': {'properties': {'title': change['add_tab']}}})
            if rows:
                data[bool(change.get('formulas'))].append({'range': quoted(change['add_tab'], f'A1:{letters(max(map(len, rows)))}{len(rows)}'),
                                                           'majorDimension': 'ROWS', 'values': rows})
            continue
        tab = tab_named(current['tabs'], change['tab'])
        if 'append' in change:
            need = change['row'] + len(rows) - 1
            if need > tab['rows']:
                structure.append({'appendDimension': {'sheetId': tab['id'], 'dimension': 'ROWS', 'length': need - tab['rows']}})
            where = f'A{change["row"]}:{letters(max(map(len, rows)))}{need}'
        else:
            where = change['cells']
        data[bool(change.get('formulas'))].append({'range': quoted(tab['title'], where), 'majorDimension': 'ROWS', 'values': rows})
    wrote = False
    try:
        if structure:
            writer.file_call(SHEETS, 'sheets.spreadsheets.batchUpdate', {'spreadsheetId': file_id}, write=True, body={'requests': structure})
            wrote = True
        for formulas in (False, True):
            if data[formulas]:
                writer.file_call(SHEETS, 'sheets.spreadsheets.values.batchUpdate', {'spreadsheetId': file_id}, write=True,
                                 body={'valueInputOption': 'USER_ENTERED' if formulas else 'RAW', 'data': data[formulas]})
                wrote = True
    except error_type:
        if wrote:
            return {}
        raise
    return {'message_id': 'docwrite:' + file_id}


def slide_requests(action):
    """The batchUpdate requests: each find replaced on its slide only, then each new slide with its title and body."""
    out = [{'replaceAllText': {'containsText': {'text': c['find'], 'matchCase': True}, 'replaceText': c['replace'],
                               'pageObjectIds': [c['slide_id']]}} for c in action['changes'] if 'find' in c]
    for i, c in enumerate(action['changes']):
        if 'add_slide' not in c:
            continue
        slide, title, body = object_ids(action, i)
        out += [{'createSlide': {'objectId': slide, 'insertionIndex': c['at'] - 1, 'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'},
                                 'placeholderIdMappings': [{'layoutPlaceholder': {'type': 'TITLE', 'index': 0}, 'objectId': title},
                                                           {'layoutPlaceholder': {'type': 'BODY', 'index': 0}, 'objectId': body}]}},
                {'insertText': {'objectId': title, 'text': c['add_slide']}},
                {'insertText': {'objectId': body, 'text': c['body']}}]
    return out


def landed(writer, action):
    """Whether this approved edit is in the file read back: every cell holds its new value (as entered, or as it shows),
    each new tab is there; each shape shows its text after, each new slide is there."""
    kind, file_id = action['file_kind'], action['file_id']
    if kind == SLIDES:
        about = writer.file_call(SLIDES, 'slides.presentations.get', {'presentationId': file_id, 'fields': SLIDE_FIELDS})
        if str(about.get('revisionId') or '') == action['version']:
            return False
        slides = {str(s.get('objectId') or ''): [t for e in s.get('pageElements') or [] for _, t in shape_texts(e)]
                  for s in about.get('slides') or [] if isinstance(s, dict)}
        for i, c in enumerate(action['changes']):
            if 'add_slide' in c and object_ids(action, i)[0] not in slides:
                return False
            if 'find' in c and any(x['after'] not in slides.get(c['slide_id'], ()) for x in c['shown']):
                return False
        return True
    about = writer.file_call(SHEETS, 'sheets.spreadsheets.get', {'spreadsheetId': file_id, 'fields': google_files.SHEET_FIELDS})
    titles = {str((s.get('properties') or {}).get('title') or '').lower() for s in about.get('sheets') or [] if isinstance(s, dict)}
    ranges, wanted = [], []
    for c in action['changes']:
        rows = c.get('values') or c.get('append') or []
        if 'add_tab' in c and c['add_tab'].lower() not in titles:
            return False
        if rows:
            tab = c.get('add_tab') or c['tab']
            start = 'A1' if 'add_tab' in c else f'A{c["row"]}' if 'append' in c else c['cells'].split(':')[0]
            col, row = re.fullmatch(r'([A-Z]+)(\d+)', start).groups()
            ranges.append(quoted(tab, f'{start}:{letters(number(col) + max(map(len, rows)) - 1)}{int(row) + len(rows) - 1}'))
            wanted.append(rows)
    if not ranges:
        return True
    reads = [writer.file_call(SHEETS, 'sheets.spreadsheets.values.batchGet', {'spreadsheetId': file_id, 'ranges': ranges,
                                                                              'valueRenderOption': option}).get('valueRanges') or []
             for option in ('FORMULA', 'FORMATTED_VALUE')]
    for i, rows in enumerate(wanted):
        width = max(map(len, rows))
        got = [padded((r[i] if i < len(r) else {}).get('values'), len(rows), width) for r in reads]
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                if shown(value) not in (shown(got[0][y][x]), shown(got[1][y][x])):
                    return False
    return True


def reconcile(writer, action):
    return {'message_id': 'docwrite:' + action['file_id']} if landed(writer, action) else {}

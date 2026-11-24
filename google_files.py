"""A Google Sheet or Slides file linked in a to-do, read for one run (connectors/docs.py): read-only, small.

A sheet: its tabs with their sizes, then the cells as they show (a formula's value, never the formula), the linked tab or
range first, at most MAX_CELLS of them. Slides: each slide's text and speaker notes, in order. The rest is read with a
range: cells of one tab, or slide numbers.

Scopes: spreadsheets.readonly and presentations.readonly (both sensitive, not restricted), from Google Docs' own sign-in
with Allow Sheets and Slides; or a wider one a sign-in already holds. Nothing here asks for a scope."""
import csv
import io
import json
import re

import google_links
from google_links import SHEETS, SLIDES

TYPES = {SHEETS: 'Google Sheet', SLIDES: 'Google Slides'}
SCOPE = {SHEETS: 'https://www.googleapis.com/auth/spreadsheets.readonly',
         SLIDES: 'https://www.googleapis.com/auth/presentations.readonly'}
# The scopes that read each kind, narrowest first
READS = {kind: (SCOPE[kind], 'https://www.googleapis.com/auth/' + wide, 'https://www.googleapis.com/auth/drive.readonly',
                'https://www.googleapis.com/auth/drive') for kind, wide in ((SHEETS, 'spreadsheets'), (SLIDES, 'presentations'))}
GID = re.compile(r'\bgid=(\d{1,12})')
RANGE = re.compile(r'\brange=([A-Za-z]{1,3}\d{0,7}(?:(?::|%3A)[A-Za-z]{1,3}\d{0,7})?)', re.I)
A1 = re.compile(r'([A-Z]{1,3})(\d{0,7})(?::([A-Z]{1,3})(\d{0,7}))?')
PAGES = re.compile(r'(\d{1,4})(?:\s*-\s*(\d{1,4}))?')
MAX_SPOTS = 3        # linked tabs or ranges of one sheet
MAX_CELLS = 2000     # cells of a sheet handed to a run, over all its tabs
MAX_ROWS, MAX_COLS = 500, 50  # asked of one tab
MAX_TABS = 6         # tabs whose cells are read in one go
MAX_CELL = 500       # characters of one cell
MAX_SLIDES = 60
MAX_TEXT = 30_000    # characters of one file handed to a run
MAX_ANSWER = 8_000_000  # bytes of one answer from Google
SHEET_FIELDS = 'properties(title),sheets(properties(sheetId,title,sheetType,hidden,gridProperties(rowCount,columnCount)))'
_TEXT = 'text(textElements(textRun(content)))'
_SHAPES = f'shape({_TEXT}),table(tableRows(tableCells({_TEXT}))),wordArt(renderedText)'
SLIDE_FIELDS = (f'title,slides(slideProperties(isSkipped,notesPage(notesProperties(speakerNotesObjectId),pageElements(objectId,shape({_TEXT})))),'
                f'pageElements({_SHAPES},elementGroup(children({_SHAPES},elementGroup(children({_SHAPES}))))))')


def links(text):
    """{file id: {kind, spots}} of the Sheets and Slides files linked in a text, in order; spots: the (tab, range) pairs a
    sheet's links point at, each as Google writes it in the link, or None."""
    found = {}
    for kind, file_id, tail in google_links.find(text):
        if kind not in (SHEETS, SLIDES):
            continue
        file = found.setdefault(file_id, {'kind': kind, 'spots': []})
        gid, cells = GID.search(tail), RANGE.search(tail)
        spot = (int(gid[1]) if gid else None, cells[1].upper().replace('%3A', ':') if cells else None)
        if file['kind'] == SHEETS and spot != (None, None) and spot not in file['spots'] and len(file['spots']) < MAX_SPOTS:
            file['spots'].append(spot)
    return found


def scope_for(kind, granted):
    """The narrowest granted scope that reads this kind, or None."""
    return next((s for s in READS[kind] if s in granted), None)


def reads(granted):
    """The kinds these scopes read, sorted."""
    return sorted(kind for kind in READS if scope_for(kind, granted))


class Reader:
    """One file read through a Google sign-in: `source` is connectors/docs.py's Google or GogGoogle."""

    def __init__(self, source, kind, scope):
        self.source, self.kind, self.scope = source, kind, scope
        self.helpers = source.helpers

    def call(self, method, params):
        try:
            data = self.source.call(method, params, scope=self.scope, raw=True, limit=MAX_ANSWER)
            return data if isinstance(data, dict) else json.loads(data)
        except ValueError:
            raise self.helpers.SourceError('docs_file_too_large') from None
        except self.helpers.SourceError as error:
            category = {'docs_response_too_large': 'docs_file_too_large', 'docs_not_connected': 'docs_files_not_granted'}.get(error.category)
            reason = str(getattr(error, 'reason', None) or '')
            if not category and error.status == 403 and reason not in ('SERVICE_DISABLED', 'accessNotConfigured'):
                category = 'docs_files_not_granted' if 'SCOPE' in reason else 'docs_no_access'
            category = category or {400: 'docs_file_kind', 404: 'docs_gone', 410: 'docs_gone'}.get(error.status)
            if not category:
                raise
            raise self.helpers.SourceError(category, error.status) from None

    def read(self, file_id, spots=(), asked=None):
        return (self.sheet if self.kind == SHEETS else self.slides)(file_id, list(spots or ()), str(asked or '').strip())

    # ---- sheets

    def sheet(self, file_id, spots, asked):
        about = self.call('sheets.spreadsheets.get', {'spreadsheetId': file_id, 'fields': SHEET_FIELDS})
        tabs = [s.get('properties') or {} for s in about.get('sheets') or [] if isinstance(s, dict)]
        grids = [t for t in tabs if t.get('sheetType', 'GRID') == 'GRID' and t.get('title')]
        todo = [(tab, cells) for tab, cells in ((linked(grids, gid), cells) for gid, cells in spots) if tab]
        if asked:
            todo = [self.asked(asked, todo, grids)]
        else:  # the linked tabs first, then the visible others; a hidden one only when it is linked or asked for
            todo += [(t, None) for t in grids if not t.get('hidden') and not any(t is x for x, _ in todo)]
        out, left, done = [], MAX_CELLS, set()
        cut = any(cells for _, cells in todo)
        for tab, cells in todo:
            if len(done) >= MAX_TABS or left <= 0:
                cut = True
                break
            done.add(tab['title'])
            got = self.cells(file_id, tab, cells, left)
            left, cut = left - got['cells'], cut or got['cut']
            out.append(got['text'])
        listed = '; '.join(size(t) for t in tabs)
        text = 'Tabs: ' + listed + '\n\n' + '\n\n'.join(out)
        note = ('Not all of it was read. Read another part with --range and a tab and cells from the list above, '
                "like \"Tab name!A1:H200\".") if cut or len(text) > MAX_TEXT else ''
        return {'title': (about.get('properties') or {}).get('title'), 'type': TYPES[SHEETS],
                'url': f'https://docs.google.com/spreadsheets/d/{file_id}/edit', 'text': text[:MAX_TEXT],
                'truncated': bool(note), **({'note': note} if note else {})}

    def asked(self, asked, linked, grids):
        """The tab and cells a run asked for: "Tab!A1:C9", "A1:C9" (the linked tab, else the first) or "Tab"."""
        name, _, cells = asked.rpartition('!')
        if not name and (titled(grids, cells) or not A1.fullmatch(cells.upper())):
            name, cells = cells, ''
        name = name.strip().strip("'").replace("''", "'")
        tab = titled(grids, name) if name else linked[0][0] if linked else grids[0] if grids else None
        if not tab or cells and not A1.fullmatch(cells.upper()):
            raise self.helpers.SourceError('docs_range_unknown')
        return tab, cells.upper() or None

    def cells(self, file_id, tab, cells, left):
        rows, cols = grid(tab)
        c1, r1, c2, r2 = bounds(cells, rows, cols)
        wide = min(c2, c1 + MAX_COLS - 1)
        tall = min(r2, r1 + MAX_ROWS - 1)
        where = f"{letters(c1)}{r1}:{letters(wide)}{tall}"
        title = tab['title'].replace("'", "''")
        got = self.call('sheets.spreadsheets.values.get', {'spreadsheetId': file_id, 'range': f"'{title}'!{where}",
                                                           'valueRenderOption': 'FORMATTED_VALUE'})
        kept, count, cut = [], 0, wide < c2 or tall < r2
        for row in got.get('values') or []:
            row = [' '.join(str('' if v is None else v).split()) for v in (row if isinstance(row, list) else [])]
            if count + len(row) > left:
                cut = True
                break
            count += len(row)
            kept.append([v if len(v) <= MAX_CELL else v[:MAX_CELL] + '...' for v in row])
        last = r1 + len(kept) - 1
        width = max((len(r) for r in kept), default=0)
        name = ' '.join(tab['title'].split())
        if not count:
            return {'text': f"# {name}, {where}: {'not read' if got.get('values') else 'empty'}", 'cells': 0, 'cut': cut}
        answer = io.StringIO()
        csv.writer(answer, lineterminator='\n').writerows(kept)
        return {'text': f'# {name}, {letters(c1)}{r1}:{letters(c1 + width - 1)}{last}\n' + answer.getvalue().rstrip('\n'),
                'cells': count, 'cut': cut}

    # ---- slides

    def slides(self, file_id, spots, asked):
        about = self.call('slides.presentations.get', {'presentationId': file_id, 'fields': SLIDE_FIELDS})
        slides = [s for s in about.get('slides') or [] if isinstance(s, dict)]
        first, last = 1, len(slides)
        if asked:
            found = PAGES.fullmatch(asked)
            first = int(found[1]) if found else 0
            last = min(int(found[2] or found[1]), last) if found else 0
            if not 1 <= first <= last:
                raise self.helpers.SourceError('docs_range_unknown')
        out, used, stop = [], 0, first - 1
        for n in range(first, min(last, first + MAX_SLIDES - 1) + 1):
            said = slide_text(slides[n - 1], n)
            if out and used + len(said) > MAX_TEXT:
                break
            out.append(said[:MAX_TEXT])
            used, stop = used + len(said), n
        note = f'Slides {first} to {stop} of {len(slides)}. Read more with --range and slide numbers, like "{stop + 1}-{len(slides)}".' \
            if stop < last else ''
        return {'title': about.get('title'), 'type': TYPES[SLIDES],
                'url': f'https://docs.google.com/presentation/d/{file_id}/edit',
                'text': (f'{len(slides)} slides' if len(slides) != 1 else '1 slide') + '\n\n' + '\n\n'.join(out), 'truncated': bool(note),
                **({'note': note} if note else {})}


def linked(grids, gid):
    """The tab a link points at: its gid, or the first one without a gid."""
    return next((t for t in grids if int(t.get('sheetId') or 0) == gid), None) if gid is not None else grids[0] if grids else None


def titled(grids, name):
    return next((t for t in grids if t['title'].strip().lower() == name.strip().lower()), None)


def grid(tab):
    found = tab.get('gridProperties') or {}
    return int(found.get('rowCount') or 1), int(found.get('columnCount') or 1)


def size(tab):
    name = ' '.join(str(tab.get('title') or 'Untitled').split())
    if tab.get('sheetType', 'GRID') != 'GRID':
        return f'{name} (no cells)'  # a chart, or a connected data source
    rows, cols = grid(tab)
    return f"{name} ({rows} rows, {cols} columns{', hidden' if tab.get('hidden') else ''})"


def number(column):
    value = 0
    for letter in column:
        value = value * 26 + ord(letter) - 64
    return value


def letters(column):
    found = ''
    while column > 0:
        column, rest = divmod(column - 1, 26)
        found = chr(65 + rest) + found
    return found


def bounds(cells, rows, cols):
    """(first column, first row, last column, last row) of an A1 range, inside the tab; all of it without one."""
    found = A1.fullmatch(cells or '')
    if not found:
        return 1, 1, cols, rows
    c1, r1 = min(number(found[1]), cols), min(int(found[2] or 1) or 1, rows)
    c2 = min(number(found[3]), cols) if found[3] else c1
    r2 = min(int(found[4]) or 1, rows) if found[4] else rows if found[3] or not found[2] else r1
    return min(c1, c2), min(r1, r2), max(c1, c2), max(r1, r2)


def words(text):
    runs = ((e.get('textRun') or {}).get('content') for e in (text or {}).get('textElements') or [] if isinstance(e, dict))
    return '\n'.join(line for line in (' '.join(x.split()) for x in ''.join(str(r or '') for r in runs).splitlines()) if line)


def element_text(element, depth=0):
    """The text of one thing on a slide: a shape, a table (a line a row), word art, or what a group holds."""
    if not isinstance(element, dict):
        return ''
    out = [words((element.get('shape') or {}).get('text')), ' '.join(str((element.get('wordArt') or {}).get('renderedText') or '').split())]
    for row in (element.get('table') or {}).get('tableRows') or []:
        out.append(' | '.join(words(c.get('text')).replace('\n', ' ') for c in row.get('tableCells') or []))
    if depth < 3:
        out += [element_text(e, depth + 1) for e in (element.get('elementGroup') or {}).get('children') or []]
    return '\n'.join(x for x in out if x.strip(' |'))


def slide_text(slide, n):
    about = slide.get('slideProperties') or {}
    body = '\n'.join(x for x in (element_text(e) for e in slide.get('pageElements') or []) if x)
    page = about.get('notesPage') or {}
    speaker = (page.get('notesProperties') or {}).get('speakerNotesObjectId')
    notes = '\n'.join(x for x in (element_text(e) for e in page.get('pageElements') or [] if speaker and isinstance(e, dict) and e.get('objectId') == speaker) if x)
    return (f"# Slide {n}{' (skipped)' if about.get('isSkipped') else ''}\n" + (body or '(no text)')
            + (f'\nSpeaker notes: {notes}' if notes else ''))

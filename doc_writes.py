"""Owner-approved writes to documents: a new doc, or an edit to a doc of the task's own doc events. Google Docs, and Word
on OneDrive and SharePoint. connectors/docs.py (Writer) does the reading and writing; this module decides what is
written and checks it.

Nothing is written without the owner seeing it. A preparation offers {kind: doc_write} as a next action; the to-do shows
the whole new doc, or each change as before and after, and the write runs only after the owner's Create or Save and its
confirm. Never with send_now, so a chat turn never drafts and writes at once; by voice the whole change is read aloud
first and needs a clear yes (talk_live.py).

- create {op: create, account_id, title, body}: a new doc from plain text. A line starting with "# ", "## " or "### "
  is a heading, every other line a paragraph. Google: a Google Doc in the owner's My Drive (the drive.file scope, or
  drive). Word: a .docx in the root of their OneDrive (Files.ReadWrite.All).
- edit {op: edit, file_id, changes}: at most 20 changes to one doc of the task's own doc events:
  {find, replace} text within one paragraph that is in the doc exactly once (an empty replace deletes it);
  {after, insert} new paragraphs after the paragraph that holds `after`; {append} new paragraphs at the end.
  Text in tables, paragraphs with suggestions, tracked changes, fields or text boxes, and images stay as they are.
  The text around a change keeps its formatting; new paragraphs are plain (or headings).

Pinned: an edit carries the doc's version when it was drafted (Google's revisionId, Word's cTag), read live when the
draft was saved; the to-do shows the changes against that version. If the doc changed since, nothing is written and
the owner is asked for a new draft. Google checks the revision in the write itself (requiredRevisionId); Word uploads
with If-Match on the eTag read right before, after checking the cTag.

Once: a write whose outcome is unclear is checked by reading the doc back, never by writing again."""
from __future__ import annotations

import bisect
import html
import io
import json
import re
import zipfile

KIND = 'doc_write'
OPS = ('create', 'edit')
KEYS = {'kind', 'op', 'label', 'account_id', 'title', 'body', 'file_id', 'changes'}
MAX_CHANGES = 20
MAX_FIND = 2000
MAX_REPLACE = 5000
MAX_INSERT = 20_000
MAX_BODY = 100_000
MAX_TITLE = 200
MAX_LINES = 400
LABELS = re.compile(r'(?:Create|Save|Update|Add|Edit)\b')
WHERE = {'google': 'Google Docs', 'microsoft': 'Word'}
HEADING = re.compile(r'(#{1,3}) +(.*)')
FIXED = '\t\u000b￼'  # a tab, a line break or an object (an image) in a paragraph: never part of a change
DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


# ------------------------------------------------------------------------------------------- what the owner approves

def lines(text):
    """[(style, text)] of a new doc's or an insert's plain text: h1, h2, h3 for "# ", "## ", "### " lines, else p.
    Blank lines only separate."""
    out = []
    for line in str(text).split('\n'):
        line = line.strip()
        if not line:
            continue
        found = HEADING.fullmatch(line)
        out.append(('h' + str(len(found[1])), found[2].strip()) if found and found[2].strip() else ('p', line))
    return out


def _text(value, field, limit, newlines):
    if not isinstance(value, str) or '\x00' in value or len(value) > limit:
        raise ValueError(f'{field} is text of at most {limit:,} characters')
    if re.search(r'[\x01-\x08\x0b\x0c\x0e-\x1f￾￿]', value):
        raise ValueError(f'{field} has control characters')
    value = value.replace('\r\n', '\n').replace('\r', '\n')
    if not newlines and '\n' in value:
        raise ValueError(f'{field} stays within one paragraph: no line breaks (use insert for new paragraphs)')
    return value


def _new_text(value, field):
    value = _text(value, field, MAX_INSERT if field != 'body' else MAX_BODY, True)
    found = lines(value)
    if not found:
        raise ValueError(f'{field} has no text')
    if len(found) > MAX_LINES:
        raise ValueError(f'{field} has at most {MAX_LINES} paragraphs')
    return '\n'.join(('#' * int(style[1]) + ' ' if style != 'p' else '') + text for style, text in found)


def short(text, size=60):
    text = ' '.join(str(text).split())
    return text if len(text) <= size else text[:size - 1] + '…'


def paragraph_text(text):
    """A paragraph as the owner reads it: a tab or line break as a space, an image as [image]."""
    return text.replace('\t', ' ').replace('\u000b', ' ').replace('￼', '[image]')


def resolve(snapshot, changes):
    """The changes as the owner sees them, checked against the doc's paragraphs: each find and anchor is in the doc
    exactly once, within one paragraph; replacements never overlap. Raises ValueError with what to fix."""
    paras = snapshot['paragraphs']
    joined = '\n'.join(p['text'] for p in paras)
    starts, at = [], 0
    for p in paras:
        starts.append(at)
        at += len(p['text']) + 1

    def locate(needle, field):
        if '\n' in needle:
            raise ValueError(f'“{short(needle)}” ({field}) runs across paragraphs. Make one change per paragraph')
        first = joined.find(needle)
        if first < 0:
            raise ValueError(f'“{short(needle)}” ({field}) is not in the doc. Copy it exactly from its current text '
                             '(assistant doc-draft prints it)')
        if joined.find(needle, first + 1) >= 0:
            raise ValueError(f'“{short(needle)}” ({field}) is in the doc more than once. Give a longer piece, so it is there once')
        k = bisect.bisect_right(starts, first) - 1
        return k, first - starts[k]

    out, spans = [], []
    for change in changes:
        if 'find' in change:
            k, s = locate(change['find'], 'find')
            e = s + len(change['find'])
            para = paras[k]
            if not para.get('editable', True):
                raise ValueError(f'“{short(change["find"])}” is in a paragraph with suggestions, tracked changes or fields. '
                                 'Change it in the doc itself')
            if any(c in FIXED for c in change['find']):
                raise ValueError(f'“{short(change["find"])}” runs across a tab, line break or image. Pick text within it')
            if any(k == k2 and s < e2 and s2 < e for k2, s2, e2 in spans):
                raise ValueError(f'Two changes touch “{short(change["find"])}”. Make them one')
            spans.append((k, s, e))
            after = para['text'][:s] + change['replace'] + para['text'][e:]
            out.append({'find': change['find'], 'replace': change['replace'], 'before': paragraph_text(para['text']),
                        'after': paragraph_text(after)})
        elif 'after' in change:
            k, _ = locate(change['after'], 'after')
            out.append({'after': change['after'], 'insert': change['insert'], 'before': paragraph_text(paras[k]['text'])})
        else:
            out.append({'append': change['append']})
    return out


def _changes(value):
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_CHANGES:
        raise ValueError(f'changes is a list of 1 to {MAX_CHANGES} changes')
    out = []
    for change in value:
        keys = set(change) if isinstance(change, dict) else None
        if keys == {'find', 'replace'}:
            find = _text(change['find'], 'find', MAX_FIND, False)
            if not find.strip():
                raise ValueError('find is the text to change')
            replace = _text(change['replace'], 'replace', MAX_REPLACE, False)
            if replace == find:
                raise ValueError(f'“{short(find)}” is replaced by the same text')
            out.append({'find': find, 'replace': replace})
        elif keys == {'after', 'insert'}:
            after = _text(change['after'], 'after', MAX_FIND, False)
            if not after.strip():
                raise ValueError('after is text from the paragraph the new text goes under')
            out.append({'after': after, 'insert': _new_text(change['insert'], 'insert')})
        elif keys == {'append'}:
            out.append({'append': _new_text(change['append'], 'append')})
        else:
            raise ValueError('A change is {find, replace}, {after, insert} or {append}')
    return out


def validate(value, context):
    """A doc write as the owner will see it, without its revision. context (assistant.doc_write_context):
    accounts {id: {name, provider, writes}}: the owner's Docs connections and what each may write;
    files {file_id: {account_id, doc_title, provider}}: the docs of this task's own doc events;
    snapshots {file_id: snapshot, or the reason it couldn't be read}: each doc an edit names, read just now."""
    context = context or {}
    if set(value) - KEYS:
        raise ValueError('A doc write has op, account_id and title and body (create), or file_id and changes (edit)')
    op = value.get('op')
    if op not in OPS:
        raise ValueError('op is create (a new doc) or edit (a doc of this task)')
    result = {'kind': KIND, 'op': op}
    if value.get('label') is not None:
        if not LABELS.match(value['label']):
            raise ValueError('Doc write button labels say Create, Save, Update, Add or Edit, such as Create doc')
        result['label'] = value['label']
    accounts = context.get('accounts') or {}
    if op == 'create':
        if set(value) - {'kind', 'op', 'label', 'account_id', 'title', 'body'}:
            raise ValueError('A new doc has account_id, title and body only')
        account = accounts.get(value.get('account_id'))
        if not account:
            raise ValueError('account_id is one of your Docs connections: ' + (', '.join(sorted(accounts)) or 'none connected'))
        if 'create' not in account.get('writes', ()):
            raise ValueError('Creating docs is not allowed for this Docs connection yet (Allow edits on its connection). '
                             'Give the text in the to-do instead')
        title = ' '.join(_text(value.get('title'), 'title', MAX_TITLE, False).split())
        if not title:
            raise ValueError('A new doc needs a title')
        result.update(account_id=value['account_id'], provider=account['provider'], account_name=account.get('name', ''),
                      title=title, body=_new_text(value.get('body'), 'body'))
        return result
    if set(value) - {'kind', 'op', 'label', 'file_id', 'changes', 'account_id'}:
        raise ValueError('An edit has file_id and changes only')
    file_id = str(value.get('file_id') or '')
    known = (context.get('files') or {}).get(file_id)
    if not known:
        raise ValueError('Edit only a doc of this task’s own doc events (file_id is its metadata.file_id)')
    if value.get('account_id') not in (None, known['account_id']):
        raise ValueError('That doc belongs to another Docs connection')
    account = accounts.get(known['account_id'])
    if not account or 'edit' not in account.get('writes', ()):
        raise ValueError('Editing docs is not allowed for this Docs connection yet (Allow edits on its connection; Google '
                         'needs the same permission as posting replies). Give the changes as text in the to-do instead')
    changes = _changes(value.get('changes'))
    snapshot = (context.get('snapshots') or {}).get(file_id)
    if not isinstance(snapshot, dict):
        raise ValueError(str(snapshot or 'The doc could not be read just now') + '. Nothing was saved; try again')
    result.update(account_id=known['account_id'], provider=account['provider'], file_id=file_id,
                  doc_title=str(snapshot.get('title') or known.get('doc_title') or 'the doc')[:200], version=snapshot['version'],
                  changes=resolve(snapshot, changes))
    if snapshot.get('url'):
        result['url'] = snapshot['url']
    return result


def label(action):
    return action.get('label') or ('Create doc' if action['op'] == 'create' else 'Save changes')


def where(action):
    return WHERE.get(action.get('provider'), 'Docs')


def done(action):
    """What happened, once written: "Created “Plan” in Google Docs" or "Saved 2 changes to “Plan”"."""
    if action['op'] == 'create':
        return f'Created “{action["title"]}” in {where(action)}'
    n = len(action['changes'])
    return f'Saved {n} change{"s" if n > 1 else ""} to “{action["doc_title"]}”'


def change_lines(change):
    if 'find' in change:
        return ['Before: ' + change['before'], 'After: ' + change['after']]
    if 'after' in change:
        return ['Add after “' + short(change['before'], 80) + '”:', change['insert']]
    return ['Add at the end:', change['append']]


def preview(action):
    """The whole write as plain text: the new doc in full, or every change as before and after."""
    if action['op'] == 'create':
        return f'New doc in {where(action)}: “{action["title"]}”\n\n{action["body"]}'
    n = len(action['changes'])
    blocks = [f'Edit “{action["doc_title"]}” in {where(action)}: {n} change{"s" if n > 1 else ""}']
    for i, change in enumerate(action['changes'], 1):
        blocks.append((f'{i}. ' if n > 1 else '') + '\n'.join(change_lines(change)))
    return '\n\n'.join(blocks)


def spoken(action):
    """What voice reads aloud before asking for a yes: the same as the preview, every change in full."""
    return preview(action)


def landed(snapshot, action):
    """Whether this approved edit is in the doc read back: every changed paragraph and every new one is there."""
    have = {paragraph_text(p['text']) for p in snapshot['paragraphs']}
    for change in action['changes']:
        if 'find' in change:
            if change['after'] not in have:
                return False
        else:
            if any(text not in have for _, text in lines(change.get('insert') or change.get('append'))):
                return False
    return True


def failed(action, status):
    """The to-do's line when the doc refused the write: nothing changed."""
    if status in (409, 412):
        return 'The doc changed since this was drafted. Nothing was changed; ask for a new draft.'
    if status == 423:
        return 'The doc is locked (open with a lock somewhere). Nothing was changed; try again later.'
    return f'{where(action)} refused it (error {status}). Nothing was changed; try again or ask for a new draft.'


UNCLEAR = 'I couldn’t confirm the doc change. I’m checking the doc; I won’t make it twice.'


# ------------------------------------------------------------------------------------------- Google Docs

def utf16(text):
    return len(text.encode('utf-16-le')) // 2


def google_paragraphs(doc):
    """A Docs API document's body paragraphs (tables skipped): [{text, editable, at}], `at` the document index of each
    character and, last, of the paragraph's own newline. A non-text element (an image, a person chip) is a FIXED
    character per index it takes; a paragraph with suggestions is not editable."""
    out = []
    for block in ((doc.get('body') or {}).get('content') or []):
        para = block.get('paragraph') if isinstance(block, dict) else None
        if not isinstance(para, dict):
            continue
        text, at, editable = '', [], not (para.get('suggestedParagraphStyleChanges') or para.get('suggestedPositionedObjectIds'))
        index = None
        for element in para.get('elements') or []:
            start, end = element.get('startIndex'), element.get('endIndex')
            if not isinstance(start, int) or not isinstance(end, int):
                editable = False
                continue
            index = start
            run = element.get('textRun')
            if isinstance(run, dict):
                if run.get('suggestedInsertionIds') or run.get('suggestedDeletionIds'):
                    editable = False
                content = str(run.get('content') or '')
                if utf16(content) != end - start:
                    editable = False
                for ch in content:
                    text += ch
                    at.append(index)
                    index += utf16(ch)
            else:
                for _ in range(end - start):
                    text += '￼'
                    at.append(index)
                    index += 1
        if not at:
            continue
        if text.endswith('\n'):
            text, at = text[:-1], at  # the newline's index stays last
        else:
            at.append(index)
            editable = False
        out.append({'text': text, 'editable': editable, 'at': at})
    return out


def google_snapshot(doc, file_id):
    return {'version': str(doc.get('revisionId') or ''), 'title': str(doc.get('title') or ''),
            'url': f'https://docs.google.com/document/d/{file_id}/edit', 'paragraphs': google_paragraphs(doc)}


STYLE = {'h1': 'HEADING_1', 'h2': 'HEADING_2', 'h3': 'HEADING_3', 'p': 'NORMAL_TEXT'}


def _positions(paras, changes):
    """[(where, rank, order, change, paragraph index, start, end)] for each change, in the doc's own text."""
    joined = '\n'.join(p['text'] for p in paras)
    starts, at = [], 0
    for p in paras:
        starts.append(at)
        at += len(p['text']) + 1
    out = []
    for order, change in enumerate(changes):
        needle = change.get('find', change.get('after'))
        if needle is not None:
            first = joined.find(needle)
            if first < 0 or joined.find(needle, first + 1) >= 0:
                raise ValueError('changed')
            k = bisect.bisect_right(starts, first) - 1
            s = first - starts[k]
            out.append((k, s, s + len(needle), order, change))
        else:
            out.append((len(paras) - 1, None, None, order, change))
    return out


def google_requests(doc, changes):
    """The batchUpdate requests for these changes, last in the doc first so earlier indexes stay put."""
    paras = google_paragraphs(doc)
    if not paras:
        raise ValueError('changed')
    steps = []
    for k, s, e, order, change in _positions(paras, changes):
        para = paras[k]
        if 'find' in change:
            if not para['editable']:
                raise ValueError('changed')
            a, b = para['at'][s], para['at'][e]
            ops = ([{'deleteContentRange': {'range': {'startIndex': a, 'endIndex': b}}}] if b > a else [])
            if change['replace']:
                ops.append({'insertText': {'location': {'index': a}, 'text': change['replace']}})
            steps.append(((a, 0, order), ops))
        else:
            new = lines(change.get('insert') or change.get('append'))
            at = para['at'][-1]  # before this paragraph's newline: its text ends, the new paragraphs follow
            ops = [{'insertText': {'location': {'index': at}, 'text': ''.join('\n' + text for _, text in new)}}]
            start = at + 1
            for style, text in new:
                ops.append({'updateParagraphStyle': {'range': {'startIndex': start, 'endIndex': start + utf16(text) + 1},
                                                     'paragraphStyle': {'namedStyleType': STYLE[style]}, 'fields': 'namedStyleType'}})
                start += utf16(text) + 1
            steps.append(((at, 2 if 'append' in change else 1, order), ops))
    return [op for _, ops in sorted(steps, key=lambda step: step[0], reverse=True) for op in ops]


def google_html(title, body):
    """A new Google Doc's content: Drive converts this HTML (headings and paragraphs) to a doc."""
    tags = {'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'p': 'p'}
    parts = ''.join(f'<{tags[s]}>{html.escape(t, quote=False)}</{tags[s]}>' for s, t in lines(body))
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{html.escape(title, quote=False)}</title></head>'
            f'<body>{parts}</body></html>')


def google_upload(file_id, title, body, boundary='tm-doc-write-boundary'):
    """(bytes, content type) of a multipart upload that creates the doc under the id generated before the write."""
    meta = json.dumps({'id': file_id, 'name': title, 'mimeType': 'application/vnd.google-apps.document'}, ensure_ascii=False)
    data = (f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n'
            f'--{boundary}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n{google_html(title, body)}\r\n--{boundary}--\r\n')
    return data.encode('utf-8'), f'multipart/related; boundary={boundary}'


# ------------------------------------------------------------------------------------------- Word (.docx)

TAG = re.compile(r'<(/?)([A-Za-z][\w.-]*:[A-Za-z][\w.-]*|[A-Za-z][\w.-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')
ENTITY = re.compile(r'&(#x[0-9A-Fa-f]+|#[0-9]+|amp|lt|gt|quot|apos);')
NAMED = {'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'"}
# a paragraph with any of these is left alone: tracked changes, fields, nested paragraphs (a text box)
BLOCKERS = {'w:ins', 'w:del', 'w:moveFrom', 'w:moveTo', 'w:fldChar', 'w:fldSimple', 'w:instrText', 'w:delText',
            'w:txbxContent', 'mc:AlternateContent'}
OBJECTS = {'w:drawing', 'w:object', 'w:pict'}


def _unescape(raw):
    """(text, map): the text of a w:t's raw XML, and for each character (and the end) its offset in the raw XML."""
    text, pos, i = [], [], 0
    for m in ENTITY.finditer(raw):
        for j in range(i, m.start()):
            text.append(raw[j])
            pos.append(j)
        name = m.group(1)
        char = NAMED.get(name) or chr(int(name[2:], 16) if name.startswith('#x') else int(name[1:]))
        text.append(char)
        pos.append(m.start())
        i = m.end()
    for j in range(i, len(raw)):
        text.append(raw[j])
        pos.append(j)
    pos.append(len(raw))
    return ''.join(text), pos


def escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class DocxError(ValueError):
    pass


def docx_xml(data):
    """document.xml of a .docx as text, after the same safety check as reading it (no DTD, no entities)."""
    from connectors import docs  # noqa: PLC0415 - the connector's safe parser
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as package:
            info = package.getinfo('word/document.xml')
            if info.file_size > 20_000_000:
                raise DocxError('docs_file_too_large')
            raw = package.read(info)
    except (zipfile.BadZipFile, KeyError, OSError):
        raise DocxError('docs_edit_unsupported') from None
    try:
        docs.parse_xml(raw)
        xml = raw.decode('utf-8')
    except Exception:  # noqa: BLE001 - not plain UTF-8 XML without a DTD: not edited
        raise DocxError('docs_edit_unsupported') from None
    if f'xmlns:w="{W_NS}"' not in xml[:5000]:
        raise DocxError('docs_edit_unsupported')
    return xml


def docx_paragraphs(xml):
    """(paragraphs, body end): the body's paragraphs outside tables, each {text, editable, start, end, segments}, with
    segments [(text start, text end, raw start, map, open tag start, open tag end)] for each w:t. A tab, a line break or
    an image is a FIXED character in the text."""
    body = re.search(r'<w:body\b[^>]*>', xml)
    close = xml.rfind('</w:body>')
    if not body or close < body.end():
        raise DocxError('docs_edit_unsupported')
    paras, depth, tables, runs, cur, skip_to = [], 0, 0, 0, None, -1
    for m in TAG.finditer(xml, body.end(), close):
        if m.start() < skip_to:
            continue
        closing, name, attrs = m.group(1) == '/', m.group(2), m.group(3)
        empty = attrs.rstrip().endswith('/')
        if name.startswith('?') or name.startswith('!'):
            continue
        if name == 'w:tbl' and not empty:
            tables += -1 if closing else 1
            continue
        if name == 'w:p':
            if empty:
                if depth == 0 and tables == 0:
                    paras.append({'text': '', 'editable': True, 'start': m.start(), 'end': m.end(), 'segments': [], 'empty_tag': True})
                elif cur:
                    cur['editable'] = False
                continue
            if not closing:
                depth += 1
                if depth == 1:
                    cur = {'text': '', 'editable': True, 'start': m.start(), 'segments': [], 'table': tables > 0}
                elif cur:
                    cur['editable'] = False
            else:
                depth -= 1
                if depth == 0 and cur is not None:
                    cur['end'] = m.end()
                    if not cur.pop('table'):
                        paras.append(cur)
                    cur, runs = None, 0
            continue
        if cur is None or depth != 1:
            continue
        if name in BLOCKERS:
            cur['editable'] = False
        if name == 'w:r' and not empty:
            runs += -1 if closing else 1
        elif runs > 0 and not closing and name == 'w:t' and not empty:
            end = xml.find('</w:t>', m.end(), close)
            if end < 0:
                raise DocxError('docs_edit_unsupported')
            text, pos = _unescape(xml[m.end():end])
            if '<' in xml[m.end():end]:
                raise DocxError('docs_edit_unsupported')
            cur['segments'].append((len(cur['text']), len(cur['text']) + len(text), m.end(), pos, m.start(), m.end()))
            cur['text'] += text
            skip_to = end
        elif runs > 0 and not closing and name == 'w:tab':
            cur['text'] += '\t'
        elif runs > 0 and not closing and name in ('w:br', 'w:cr'):
            cur['text'] += '\u000b'
        elif runs > 0 and not closing and name in OBJECTS:
            cur['text'] += '￼'
            if not empty:
                stop = xml.find('</' + name + '>', m.end(), close)
                if stop < 0:
                    raise DocxError('docs_edit_unsupported')
                if '<w:p' in xml[m.end():stop]:
                    cur['editable'] = False
                skip_to = stop
    return paras, close


def docx_snapshot(item, data, file_id):
    paras, _ = docx_paragraphs(docx_xml(data))
    return {'version': str(item.get('cTag') or ''), 'title': re.sub(r'\.doc[xm]$', '', str(item.get('name') or ''), flags=re.I),
            'url': str(item.get('webUrl') or ''), 'paragraphs': paras}


def word_paragraph(style, text):
    pstyle = {'h1': 'Heading1', 'h2': 'Heading2', 'h3': 'Heading3'}.get(style)
    head = f'<w:pPr><w:pStyle w:val="{pstyle}"/></w:pPr>' if pstyle else ''
    return f'<w:p>{head}<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def _preserve(tag):
    """A w:t opening tag that keeps leading and trailing spaces."""
    if 'xml:space=' in tag:
        return tag
    return tag[:-1].rstrip('/') + ' xml:space="preserve">' if not tag.endswith('/>') else tag


def docx_edit(data, changes):
    """The .docx with these changes, every other byte of document.xml and every other part as it was."""
    xml = docx_xml(data)
    paras, close = docx_paragraphs(xml)
    if not paras:
        raise ValueError('changed')
    splices, tags = [], {}
    for k, s, e, order, change in _positions(paras, changes):
        para = paras[k]
        if 'find' in change:
            if not para['editable']:
                raise ValueError('changed')
            touched = [g for g in para['segments'] if g[0] < e and g[1] > s]
            if sum(min(e, g[1]) - max(s, g[0]) for g in touched) != e - s:
                raise ValueError('changed')
            for n, (t0, _t1, raw, pos, open_start, open_end) in enumerate(touched):
                a, b = max(s, t0) - t0, min(e, _t1) - t0
                splices.append((raw + pos[a], raw + pos[b], escape(change['replace']) if n == 0 else '', (0, order)))
                tags[open_start] = open_end
        else:
            new = ''.join(word_paragraph(style, text) for style, text in lines(change.get('insert') or change.get('append')))
            if 'append' in change:
                at = _body_end(xml, paras[-1]['end'], close)
                splices.append((at, at, new, (2, order)))
            else:
                splices.append((para['end'], para['end'], new, (1, order)))
    for start, end in tags.items():
        splices.append((start, end, _preserve(xml[start:end]), (-1, 0)))
    for start, end, text, _ in sorted(splices, key=lambda x: (x[0], x[3]), reverse=True):
        xml = xml[:start] + text + xml[end:]
    return _repack(data, {'word/document.xml': xml.encode('utf-8')})


def _body_end(xml, last, close):
    """Where appended paragraphs go: before the body's own section properties, else at the end of the body."""
    sect = xml.rfind('<w:sectPr', last, close)
    return sect if sect >= 0 else close


def _repack(data, replace):
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(data)) as source, zipfile.ZipFile(out, 'w') as target:
        for info in source.infolist():
            target.writestr(info, replace.get(info.filename, source.read(info)), compress_type=info.compress_type)
    return out.getvalue()


PACKAGE = {
    '[Content_Types].xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>',
    '_rels/.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>',
    'word/_rels/document.xml.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
    'word/styles.xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:styles xmlns:w="' + W_NS + '">'
    '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>'
    '<w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
    + ''.join(f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}"/><w:basedOn w:val="Normal"/>'
              f'<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="{n - 1}"/></w:pPr>'
              f'<w:rPr><w:b/><w:sz w:val="{size}"/></w:rPr></w:style>' for n, size in ((1, 32), (2, 26), (3, 24)))
    + '</w:styles>',
}


def docx_new(body):
    """A new .docx with these headings and paragraphs: the same bytes every time, so a lost upload can be recognized."""
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document xmlns:w="' + W_NS + '"><w:body>'
                + ''.join(word_paragraph(style, text) for style, text in lines(body))
                + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
                  'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>')
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as package:
        for name, text in [*PACKAGE.items(), ('word/document.xml', document)]:
            package.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)), text.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    return out.getvalue()


def word_name(title, n=1):
    """A OneDrive file name for a new doc: the title without characters OneDrive refuses, then (2), (3)… when taken."""
    base = re.sub(r'[\\/:*?"<>|#%\x00-\x1f]+', ' ', title)
    base = ' '.join(base.split()).strip(' .')[:120] or 'Untitled document'
    return base + (f' ({n})' if n > 1 else '') + '.docx'


# ------------------------------------------------------------------------------------------- the one write

class DocWriteTransport:
    """Runs one approved doc write: checks first (the connection, its permission, the doc's version), then one write.
    An unclear outcome is checked by reading the doc back, never by writing again."""

    def __init__(self, config, connector, helpers):
        self.config, self.connector, self.helpers = config, connector, helpers

    def writer(self, action):
        if action.get('kind') != KIND:
            raise ValueError('Only an approved doc write uses the doc transport')
        account = next((a for a in self.config.get('accounts', []) if a.get('id') == action['account_id'] and a.get('service') == 'docs'), None)
        if not account:
            raise ValueError('That Docs connection is no longer here. Nothing was changed.')
        if action['op'] not in self.connector.writes_on(self.config, account, self.helpers):
            raise ValueError('Writing docs is not allowed for this connection anymore. Nothing was changed.')
        return self.connector.Writer(self.config, account, self.helpers)

    def snapshot(self, writer, file_id):
        return snapshot(writer, file_id)

    def preflight(self, action):
        writer = self.writer(action)
        try:
            if action['op'] == 'edit':
                current = self.snapshot(writer, action['file_id'])
                if current['version'] != action['version']:
                    raise ValueError('The doc changed since this was drafted. Nothing was changed; ask for a new draft.')
                resolve(current, action['changes'])
                return
            proof = action.setdefault('proof', {})
            if writer.provider == 'google':
                proof.setdefault('file_id', writer.new_id())
            elif not proof.get('name'):
                proof['name'] = next((name for name in (word_name(action['title'], n) for n in range(1, 10))
                                      if writer.lookup(name) is None), None)
                if not proof['name']:
                    raise ValueError('Files with that name are in your OneDrive already. Nothing was created; give it another title.')
        except self.helpers.SourceError:
            raise ValueError('I couldn’t reach the doc. Nothing was changed; tap it again.') from None

    def send(self, action, job):
        writer = self.writer(action)
        try:
            if action['op'] == 'create':
                return self.create(writer, action, job)
            return self.edit(writer, action)
        except self.helpers.SourceError as error:
            if error.status == 429:
                return {'not_sent': True}
            if error.status == 409 and action['op'] == 'create':
                return self.reconcile(action, job)  # this approval's doc is there already: the earlier try went through
            if error.status in (400, 401, 403, 404, 409, 412, 423):
                return {'rejected': error.status}
            return {}  # unknown: never written again; reconcile reads the doc

    def create(self, writer, action, job):
        proof = action.get('proof') or {}
        if writer.provider == 'google':
            data, kind = google_upload(proof['file_id'], action['title'], action['body'])
            made = writer.upload(data, kind)
            return {'message_id': 'docwrite:' + str(made.get('id') or proof['file_id'])}
        made = writer.create(proof['name'], docx_new(action['body']))
        drive = ((made.get('parentReference') or {}).get('driveId') or '')
        return {'message_id': 'docwrite:' + drive + '!' + str(made.get('id') or '')}

    def edit(self, writer, action):
        if writer.provider == 'google':
            doc = writer.document(action['file_id'])
            if str(doc.get('revisionId') or '') != action['version']:
                return {'rejected': 409}
            try:
                requests = google_requests(doc, action['changes'])
            except ValueError:
                return {'rejected': 409}
            writer.update(action['file_id'], requests, action['version'])
            return {'message_id': 'docwrite:' + action['file_id']}
        item, data = writer.item_and_bytes(action['file_id'])
        if str(item.get('cTag') or '') != action['version']:
            return {'rejected': 409}
        try:
            edited = docx_edit(data, action['changes'])
        except ValueError:
            return {'rejected': 409}
        writer.put(action['file_id'], edited, item.get('eTag'))
        return {'message_id': 'docwrite:' + action['file_id']}

    def reconcile(self, action, job):
        try:
            writer = self.writer(action)
            if action['op'] == 'create':
                proof = action.get('proof') or {}
                if writer.provider == 'google':
                    found = writer.find(proof.get('file_id'))
                    return {'message_id': 'docwrite:' + proof['file_id']} if found and not found.get('trashed') else {}
                found = writer.lookup(proof.get('name'))
                if found and int(found.get('size') or -1) == len(docx_new(action['body'])):
                    return {'message_id': 'docwrite:' + ((found.get('parentReference') or {}).get('driveId') or '') + '!' + str(found.get('id'))}
                return {}
            current = self.snapshot(writer, action['file_id'])
            if current['version'] != action['version'] and landed(current, action):
                return {'message_id': 'docwrite:' + action['file_id']}
        except (ValueError, KeyError, self.helpers.SourceError):
            pass
        return {}


def snapshot(writer, file_id):
    """The doc as it is now, for an edit: its version, title, link and paragraphs."""
    if writer.provider == 'google':
        return google_snapshot(writer.document(file_id), file_id)
    item, data = writer.item_and_bytes(file_id)
    try:
        return docx_snapshot(item, data, file_id)
    except DocxError as error:
        raise writer.helpers.SourceError(str(error)) from None


def context(config, connector, helpers, files, value):
    """What validate needs, read only when the next actions hold a doc write: the owner's Docs connections and what
    each may write, and each doc an edit names, read now (its version is the one the owner approves)."""
    items = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
    wanted = [a for a in items if isinstance(a, dict) and a.get('kind') == KIND]
    if not wanted or not connector:
        return None
    accounts = {}
    for a in config.get('accounts', []):
        if a.get('service') == 'docs' and not a.get('shared'):
            accounts[a['id']] = {'name': str(a.get('display_name') or a.get('email') or a['id']),
                                 'provider': connector.provider(config, a), 'writes': sorted(connector.writes_on(config, a, helpers))}
    snapshots = {}
    for w in wanted:
        file_id = str(w.get('file_id') or '')
        known = files.get(file_id)
        if w.get('op') != 'edit' or not known or file_id in snapshots or 'edit' not in (accounts.get(known['account_id']) or {}).get('writes', ()):
            continue
        account = next(a for a in config['accounts'] if a['id'] == known['account_id'])
        try:
            snapshots[file_id] = snapshot(connector.Writer(config, account, helpers), file_id)
        except helpers.SourceError as error:
            snapshots[file_id] = {'docs_edit_unsupported': 'That file can’t be edited here (only Google Docs and .docx Word files)',
                                  'docs_file_too_large': 'That file is too large to edit here',
                                  'docs_not_connected': 'Reading docs is not allowed for this connection'}.get(
                                      error.category, f'The doc could not be read ({error.category})')
    return {'accounts': accounts, 'files': files, 'snapshots': snapshots}

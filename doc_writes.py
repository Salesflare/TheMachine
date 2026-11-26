"""Writes to documents: a new doc, or an owner-approved edit to a doc of the task's own doc events. Google Docs, Word
on OneDrive and SharePoint, and Notion pages. connectors/docs.py (Writer) does the reading and writing (a Notion page
through connectors/notion.py); this module decides what is written and checks it.

Notion differs in three ways: a new page waits for the owner's OK like an edit (Store.make_new_docs leaves it), and goes
in their Private section or under a Notion page of the to-do (file_id); an edit's version is a digest of the page's
blocks; and done {op: done, file_id} marks a task assigned to the owner done, after their OK.

A preparation offers {kind: doc_write} as a next action. A new doc is made right away (Store.make_new_docs): a private
doc in the owner's own Drive or OneDrive, shared with nobody, so nothing goes to anyone and it needs no OK; the to-do
shows its link (2026-11-03). Sharing it is a step after it, drafted for the owner's OK. An edit to an existing doc
shows each change as before and after and runs only after the owner's Save and its confirm, or at once when the owner's
own chat message asked for that change (do_now, 2026-11-06). Never with send_now; by voice the whole change is read aloud first and needs a clear yes
(talk_live.py). If making the new doc fails, it waits as Review and create, like before.

- create {op: create, account_id, title, body}: a new doc from plain text. A line starting with "# ", "## " or "### "
  is a heading, every other line a paragraph. Google: a Google Doc in the owner's My Drive (the drive.file scope, or
  drive), through a Docs connection or the owner's own gog sign-in for Gmail when it already has that scope. Word: a
  .docx in the root of their OneDrive (Files.ReadWrite.All). Only into a connection of the to-do's own area (Work at
  that company, or Personal), and the conversation's own address when that one can: never another area's account.
- edit {op: edit, file_id, changes}: at most 20 changes to one doc of the task's own doc events:
  {find, replace} text within one paragraph that is in the doc exactly once (an empty replace deletes it);
  {after, insert} new paragraphs after the paragraph that holds `after`; {append} new paragraphs at the end.
  Text in tables, paragraphs with suggestions, tracked changes, fields or text boxes, and images stay as they are.
  The text around a change keeps its formatting; new paragraphs are plain (or headings).
- Google Docs only (2026-11-26, a to-do's doc stayed plain text and its chat said formatting was blocked): {format,
  style} formats text that is in the doc once: bold, italic, underline or plain (that text), h1 to h3 or p, bullet,
  number or no_list (its paragraph, through the one holding `through`), page_break (a page break before its paragraph);
  {format, link} links that text. New text (insert, append, a new doc's body) may hold "- " or "1. " list lines,
  **bold**, *italic* and [text](https://link); its other text is plain. All of it goes in the same documents.batchUpdate
  under the scope edits already use. Word and Notion take the text as it is written; tables are not made.

Pinned: an edit carries the doc's version when it was drafted (Google's revisionId, Word's cTag), read live when the
draft was saved; the to-do shows the changes against that version. If the doc changed since, nothing is written and
the owner is asked for a new draft. Google checks the revision in the write itself (requiredRevisionId); Word uploads
with If-Match on the eTag read right before, after checking the cTag.

Once: a write whose outcome is unclear is checked by reading the doc back, never by writing again.

After: a doc is rarely the whole to-do. {last: true} says it is, and the to-do is done once it is written; otherwise
{then: <the step after it>} (a reply with its link, sharing it) and the to-do carries on with that step, drafted for the
owner's OK again (assistant.settle_doc_write)."""
from __future__ import annotations

import bisect
import datetime as dt
import html
import io
import json
import logging
import re
import uuid
import zipfile
from machine.owner_error import OwnerError
import google_links
import timeutil

LOG = logging.getLogger('assistant')

KIND = 'doc_write'
NEW_DOC = 'new-doc:'  # the approval id of a new doc made while its to-do was prepared, without an OK (Store.make_new_docs)
WRITE_KEY = 'themachine_write'  # a new Google Doc's appProperties key (connectors/docs.py WRITE_KEY): this write's token
DOC_SERVICES = ('docs', 'notion')  # the connections a doc write goes through (abilities.DOC_SERVICES), besides a gog sign-in
OPS = ('create', 'edit', 'done')  # done: a Notion task assigned to the owner, marked done (connectors/notion.py)
KEYS = {'kind', 'op', 'label', 'account_id', 'title', 'body', 'file_id', 'changes', 'last', 'then'}
MAX_THEN = 300
MAX_CHANGES = 20
MAX_FIND = 2000
MAX_REPLACE = 5000
MAX_INSERT = 20_000
MAX_BODY = 100_000
MAX_TITLE = 200
MAX_LINES = 400
LABELS = re.compile(r'(?:Create|Save|Update|Add|Edit|Mark)\b')
WHERE = {'google': 'Google Docs', 'microsoft': 'Word', 'notion': 'Notion'}
HEADING = re.compile(r'(#{1,3}) +(.*)')
# {format, style}: what the owner reads for each style (the dashboard translates it); link's slot is the link
FORMATS = {'bold': 'Bold', 'italic': 'Italic', 'underline': 'Underline', 'plain': 'Plain text', 'h1': 'Heading 1',
           'h2': 'Heading 2', 'h3': 'Heading 3', 'p': 'Normal text', 'bullet': 'Bulleted list', 'number': 'Numbered list',
           'no_list': 'No list', 'page_break': 'Page break before', 'link': 'Link to {}'}
TEXT_FORMATS = ('bold', 'italic', 'underline', 'plain', 'link')  # the text itself; the others style its paragraph
RANGE_FORMATS = ('h1', 'h2', 'h3', 'p', 'bullet', 'number', 'no_list')  # these may run on through a later paragraph
# a link is https:// or http://, as next_actions.check wants a draft's [text](link)
LINK = re.compile(r'https?://[^\s<>"\\]{1,2000}')
LIST_LINE = re.compile(r'(?:([-*•])|\d{1,3}[.)]) +(.*)')
MARKS = re.compile(r'\*\*(?=\S)(.+?)(?<=\S)\*\*|(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])'
                   r'|\[([^\]\n]{1,500})\]\((https?://[^\s<>"\\)]{1,2000})\)')
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


def rich(text):
    """(the text, [(start, end, mark, link)]) of one line of new text for Google Docs: **bold**, *italic* and
    [text](https://link) become marks on their text, every other character stays as written."""
    out, marks, at = '', [], 0
    for found in MARKS.finditer(text):
        out += text[at:found.start()]
        inner = found[1] or found[2] or found[3]
        marks.append((len(out), len(out) + len(inner), 'bold' if found[1] else 'italic' if found[2] else 'link', found[4]))
        out, at = out + inner, found.end()
    return out + text[at:], marks


def google_lines(text):
    """[(style, list, text, marks)] of new text as Google Docs gets it: lines(), a "- ", "* " or "• " paragraph a
    bulleted list item and a "1. " one a numbered one (list None otherwise), and rich()'s marks."""
    out = []
    for style, line in lines(text):
        kind, found = None, LIST_LINE.fullmatch(line) if style == 'p' else None
        if found and found[2].strip():
            kind, line = 'bullet' if found[1] else 'number', found[2].strip()
        out.append((style, kind, *rich(line)))
    return out


def new_texts(change, provider):
    """The paragraphs an insert or append adds, as the doc will hold their text."""
    text = change.get('insert') or change.get('append')
    return [t for _, _, t, _ in google_lines(text)] if provider == 'google' else [t for _, t in lines(text)]


def _text(value, field, limit, newlines):
    if not isinstance(value, str) or '\x00' in value or len(value) > limit:
        raise OwnerError(f'{field} is text of at most {limit:,} characters')
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

    out, spans, marked = [], [], []
    for change in changes:
        if 'format' in change:
            k, s = locate(change['format'], 'format')
            para, style = paras[k], change.get('style', 'link')
            if not para.get('editable', True):
                raise ValueError(f'“{short(change["format"])}” is in a paragraph with suggestions, tracked changes or fields. '
                                 'Format it in the doc itself')
            last = locate(change['through'], 'through')[0] if 'through' in change else k
            if last < k:
                raise ValueError(f'“{short(change["through"])}” (through) comes before “{short(change["format"])}”. Give the first paragraph in format')
            if style in ('bullet', 'number') and any(paras[i]['text'].startswith('\t') for i in range(k, last + 1)):
                raise ValueError('A paragraph that starts with a tab can’t become a list item here. Change it in the doc itself')
            if style in TEXT_FORMATS:
                if any(c in FIXED for c in change['format']):
                    raise ValueError(f'“{short(change["format"])}” runs across a tab, line break or image. Pick text within it')
                marked.append((k, s, s + len(change['format']), change['format']))
            # the paragraph it is in, through the last one it styles
            out.append({**change, 'before': paragraph_text(para['text']) + (' … ' + paragraph_text(paras[last]['text']) if last > k else ''),
                        'how': FORMATS[style]})
        elif 'find' in change:
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
            # the paragraph it goes under, as its label says it (here and on the dashboard)
            out.append({'after': change['after'], 'insert': change['insert'], 'before': short(paragraph_text(paras[k]['text']), 80)})
        else:
            out.append({'append': change['append']})
    for k, s, e, text in marked:  # formatting text a change replaces: one of them would miss
        if any(k == k2 and s < e2 and s2 < e for k2, s2, e2 in spans):
            raise ValueError(f'“{short(text)}” is formatted and changed. Format the new text in a later edit, once it is in the doc')
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
        elif keys in ({'format', 'style'}, {'format', 'link'}, {'format', 'style', 'through'}):
            found = _text(change['format'], 'format', MAX_FIND, False)
            if not found.strip():
                raise ValueError('format is the text to format, from the doc')
            item = {'format': found}
            if 'link' in change:
                if not isinstance(change['link'], str) or not LINK.fullmatch(change['link']):
                    raise ValueError('link is a whole https:// link')
                item['link'] = change['link']
            elif not isinstance(change['style'], str) or change['style'] not in FORMATS or change['style'] == 'link':
                raise ValueError('style is one of ' + ', '.join(k for k in FORMATS if k != 'link') + ' (or give link)')
            else:
                item['style'] = change['style']
            if 'through' in change:
                if item['style'] not in RANGE_FORMATS:
                    raise ValueError('through goes with a heading, normal text or list style only')
                item['through'] = _text(change['through'], 'through', MAX_FIND, False)
            out.append(item)
        else:
            raise ValueError('A change is {find, replace}, {after, insert}, {append}, or (Google Docs) {format, style} or {format, link}')
    return out


def kind_of(boundary):
    """work, personal or '' (unknown) of an account's boundary: work:Acme, work, personal:me, personal:phone."""
    head = str(boundary or '').split(':', 1)[0].lower()
    return head if head in ('work', 'personal') else ''


def fits(boundary, area):
    """Whether an account with this boundary is in the to-do's area {boundaries, emails}: the same Work boundary (a bare
    "work" fits any company, and any company fits it), or Personal for a personal to-do. No area known: any fits."""
    boundaries = [b for b in ((area or {}).get('boundaries') or ()) if kind_of(b)]
    if not boundaries:
        return True
    mine = str(boundary or '')
    for b in boundaries:
        if kind_of(b) != kind_of(mine):
            continue
        if kind_of(b) == 'personal' or b == mine or 'work' in (b, mine):
            return True
    return False


def area_of(area):
    return next((b for b in ((area or {}).get('boundaries') or ()) if kind_of(b) == 'work'),
                next((b for b in ((area or {}).get('boundaries') or ()) if kind_of(b)), ''))


def area_name(boundary):
    """Work (at Acme), Personal: an area as the owner reads it."""
    kind, _, org = str(boundary or '').partition(':')
    if kind_of(kind) == 'work':
        return 'Work' + (f' at {org}' if org else '')
    return 'Personal' if kind_of(kind) == 'personal' else 'another area'


def google_offered(accounts, config=None):
    """Whether the owner can add a Google place for docs on this setup: when Google already takes docs here (their own
    Google sign-in with Drive on their own computer, or a Google Docs connection), or a hosted Machine's account page
    offers Connect Google Docs (docs_consent lists google). A hosted Machine's mail sign-in has no Drive scope."""
    consent = (config or {}).get('docs_consent')
    return (any((a or {}).get('provider') == 'google' for a in (accounts or {}).values())
            or bool((config or {}).get('manage_url') and isinstance(consent, list) and 'google' in consent))


def connect_line(area, google=False):
    """What the owner does when no doc connection fits the to-do's area: only what they can connect on this setup."""
    where = 'Google Docs or Microsoft OneDrive' if google else 'Microsoft OneDrive'
    return f'Connect {where} for {"Work" if kind_of(area_of(area)) == "work" else "Personal"}'


def none_fits(area, google=False):
    return (f'No Docs connection is in this to-do’s area ({area_name(area_of(area))}). Don’t draft a doc: give its text in the '
            f'to-do and say needs: "{connect_line(area, google)}"')


WHERE_WORDS = {'microsoft': re.compile(r'\bGoogle (?:Docs?|Drive)\b', re.I),
               'google': re.compile(r'\b(?:Microsoft Word|Word (?:docs?|documents?|files?)|OneDrive)\b|\bin Word\b', re.I)}


def wording(actions, texts):
    """Problems where the to-do names another place than the doc write's own (Google Docs vs Word)."""
    out = []
    for action in actions:
        if action.get('kind') != KIND:
            continue
        other = WHERE_WORDS.get(action.get('provider'))
        said = [m.group(0) for text in texts for m in ([other.search(str(text or ''))] if other else []) if m]
        if said:
            out.append(f'the doc goes to {where(action)}, but the to-do says “{said[0]}”: name {where(action)}')
    return out


def validate(value, context):
    """A doc write as the owner will see it, without its revision. context (assistant.doc_write_context):
    accounts {id: {name, provider, writes}}: the owner's Docs connections and what each may write;
    files {file_id: {account_id, doc_title, provider}}: the docs of this task's own doc events;
    snapshots {file_id: snapshot, or the reason it couldn't be read}: each doc an edit names, read just now."""
    context = context or {}
    if set(value) - KEYS:
        raise ValueError('A doc write has op, account_id and title and body (create), or file_id and changes (edit), and last or then; '
                         'leave out ' + ', '.join(sorted(map(str, set(value) - KEYS))))
    op = value.get('op')
    if op not in OPS:
        raise ValueError('op is create (a new doc), edit (a doc of this task) or done (a Notion task of this task)')
    result = {'kind': KIND, 'op': op}
    if value.get('label') is not None:
        if not LABELS.match(value['label']):
            raise ValueError('Doc write button labels say Create, Save, Update, Add, Edit or Mark, such as Create doc')
        result['label'] = value['label']
    if value.get('last') not in (None, True, False):
        raise ValueError('last is true when this doc finishes the to-do (nothing to send or share after it)')
    if value.get('last') is True:
        result['last'] = True
    elif value.get('then') is not None:
        then = ' '.join(_text(value['then'], 'then', MAX_THEN, False).split())
        if then:
            result['then'] = then
    accounts = context.get('accounts') or {}
    if op == 'done':
        if set(value) - {'kind', 'op', 'label', 'file_id', 'account_id', 'last', 'then'}:
            raise ValueError('Marking a task done has file_id only')
        file_id = file_id_of(value.get('file_id'))
        known = (context.get('files') or {}).get(file_id)
        if not known or not known.get('task'):
            raise ValueError('That file_id is not a Notion task of this to-do (the metadata.file_id of its notion.task event)')
        account = accounts.get(known['account_id'])
        if not account or 'done' not in (account.get('writes') or ()):
            raise ValueError('Marking tasks done is not allowed for this Notion connection. Say it in the to-do instead')
        result.update(account_id=known['account_id'], provider=account['provider'], file_id=file_id,
                      doc_title=str(known.get('doc_title') or 'the task')[:200])
        return result
    if op == 'create':
        parent = None
        if value.get('file_id') is not None:
            parent = file_id_of(value['file_id'])
            under = (context.get('files') or {}).get(parent)
            if not under or under.get('provider') != 'notion' or under.get('account_id') != value.get('account_id'):
                raise ValueError('file_id on a new doc is the Notion page of this to-do it goes under; leave it out for a private page')
        if set(value) - {'kind', 'op', 'label', 'account_id', 'title', 'body', 'last', 'then', 'file_id'}:
            raise ValueError('A new doc has account_id, title and body only (and last or then)')
        area = context.get('area')
        fitting = {k: a for k, a in accounts.items() if fits(a.get('boundary'), area)}
        account = accounts.get(value.get('account_id'))
        if not account:
            raise ValueError('account_id is one of your Docs connections: ' + (', '.join(sorted(fitting)) or none_fits(area, context.get('google', google_offered(accounts)))))
        if not fits(account.get('boundary'), area):
            raise ValueError(f'{account.get("name") or value["account_id"]} is {area_name(account.get("boundary"))}, not this '
                             f'to-do’s area ({area_name(area_of(area))}). Never put its doc there. '
                             + ('Use ' + ' or '.join(sorted(fitting)) + ' instead' if fitting else none_fits(area, context.get('google', google_offered(accounts)))))
        own = (area or {}).get('emails') or ()
        better = sorted(k for k, a in fitting.items() if str(a.get('email') or '').lower() in own and 'create' in a.get('writes', ()))
        if better and str(account.get('email') or '').lower() not in own:
            raise ValueError(f'This to-do’s conversation is in {", ".join(sorted(own))}: put the doc in {" or ".join(better)} '
                             'instead')
        if 'create' not in account.get('writes', ()):
            raise ValueError('Creating docs is not allowed for this Docs connection yet (Allow edits on its connection). '
                             'Give the text in the to-do instead')
        title = ' '.join(_text(value.get('title'), 'title', MAX_TITLE, False).split())
        if not title:
            raise ValueError('A new doc needs a title')
        result.update(account_id=value['account_id'], provider=account['provider'], account_name=account.get('name', ''),
                      title=title, body=_new_text(value.get('body'), 'body'), **({'parent': parent} if parent else {}))
        return result
    if set(value) - {'kind', 'op', 'label', 'file_id', 'changes', 'account_id', 'last', 'then'}:
        raise ValueError('An edit has file_id and changes only')
    file_id = file_id_of(value.get('file_id'))
    files = context.get('files') or {}
    known = files.get(file_id)
    if not known:
        made = sorted(k for k, f in files.items() if f.get('made'))
        raise ValueError('That file_id is not one of this to-do’s docs. Its docs: '
                         + (', '.join(f'{k} ({files[k].get("doc_title") or "made for this to-do"})' for k in made) + ', made for it; ' if made else '')
                         + 'the metadata.file_id of its doc events; the id in a Google Doc link in its messages. Use one of these '
                         'ids. Never ask the owner to paste a link to a doc made for this to-do')
    if value.get('account_id') not in (None, known['account_id']):
        raise ValueError('That doc belongs to another Docs connection')
    account = accounts.get(known['account_id'])
    if not account or not can_edit(account, known):
        if known.get('made'):
            raise ValueError(f'This doc was made for this to-do with {(account or {}).get("name") or known["account_id"]}, which '
                             + ('can make docs but not edit them (Allow edits on its connection)' if account else
                                'can’t write docs anymore (it was removed, or its Can do things or Drive access is off)')
                             + '. Give the changes as text in the to-do instead')
        raise ValueError('Editing docs is not allowed for this Docs connection yet (Allow edits on its connection; Google '
                         'needs the same permission as posting replies). Give the changes as text in the to-do instead')
    changes = _changes(value.get('changes'))
    if account['provider'] != 'google' and any('format' in c for c in changes):
        raise ValueError(f'Formatting changes are for Google Docs; {where(account)} takes text changes only. Leave the '
                         'formatting out, and say in the to-do what to format by hand')
    snapshot = (context.get('snapshots') or {}).get(file_id)
    if not isinstance(snapshot, dict):
        raise ValueError(str(snapshot or 'The doc could not be read just now') + '. Nothing was saved; try again')
    if known.get('made') and 'edit' not in account.get('writes', ()):
        result['made'] = True  # its own doc, through the sign-in that made it (can_edit): the transport checks this again
    result.update(account_id=known['account_id'], provider=account['provider'], file_id=file_id,
                  doc_title=str(snapshot.get('title') or known.get('doc_title') or 'the doc')[:200], version=snapshot['version'],
                  changes=resolve(snapshot, changes))
    if snapshot.get('url'):
        result['url'] = snapshot['url']
    return result


def file_id_of(value):
    """The doc id an edit names: the id itself, or the id in a Google Docs or Notion link to it (with /edit or any suffix)."""
    text = str(value or '').strip()
    found = re.search(r'docs\.google\.com/document/(?:u/\d+/)?d/([A-Za-z0-9_-]{1,200})', text)
    linked = google_links.ids(text, google_links.DOC)  # any other form of the link
    if found or linked:
        return linked[0] if linked else found[1]
    page = re.search(r'notion\.(?:so|site)/[^\s?#]*?([0-9a-f]{32})(?:[?#]|$)', text)  # a Notion page by its link
    if page:
        return page[1]
    plain = text.replace('-', '').lower()
    return plain if re.fullmatch(r'[0-9a-f]{32}', plain) and len(text) == 36 else text  # a dashed Notion id


def can_edit(account, known):
    """Whether this connection may edit this doc after the owner's OK: one with edits allowed, or the owner's own gog
    Google sign-in for a doc it made for this to-do itself (known['made']), with the same Drive access that made it.
    A gog sign-in edits no other doc."""
    writes = account.get('writes') or ()
    return 'edit' in writes or bool(known.get('made') and account.get('gog') and 'create' in writes)


def label(action):
    return action.get('label') or {'create': 'Create page' if action.get('provider') == 'notion' else 'Create doc',
                                   'done': 'Mark done'}.get(action['op'], 'Save changes')


def where(action):
    return WHERE.get(action.get('provider'), 'Docs')


def done(action):
    """What happened, once written: "Created “Plan” in Google Docs" or "Saved 2 changes to “Plan”"."""
    if action['op'] == 'create':
        return f'Created “{action["title"]}” in {where(action)}'
    if action['op'] == 'done':
        return f'Marked “{action["doc_title"]}” done in {where(action)}'
    n = len(action['changes'])
    return f'Saved {n} change{"s" if n > 1 else ""} to “{action["doc_title"]}”'


def change_lines(change):
    if 'format' in change:
        return [change['how'].replace('{}', change.get('link', '')) + ': “' + change['format'] + '”', 'In: ' + change['before']]
    if 'find' in change:
        return ['Before: ' + change['before'], 'After: ' + change['after']]
    if 'after' in change:
        return ['Add after “' + short(change['before'], 80) + '”:', change['insert']]  # short already, but for older drafts
    return ['Add at the end:', change['append']]


def untitled(action):
    """A new doc's body under its title: a first heading that only repeats the title is said once, not twice."""
    rows = [line for line in str(action.get('body') or '').split('\n') if line.strip()]
    found = HEADING.fullmatch(rows[0].strip()) if rows else None
    same = found and ' '.join(found[2].split()).lower() == ' '.join(str(action.get('title') or '').split()).lower()
    return '\n'.join(rows[1:]) if same else str(action.get('body') or '')


def preview(action):
    """The whole write as plain text: the new doc in full, or every change as before and after."""
    if action['op'] == 'create':
        return f'New {"page" if action.get("provider") == "notion" else "doc"} in {where(action)}: “{action["title"]}”\n\n{untitled(action)}'
    if action['op'] == 'done':
        return f'Mark “{action["doc_title"]}” done in {where(action)}'
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
        if 'format' in change:  # formatting leaves the text as it was: it is still there
            if not any(change['format'] in text for text in have):
                return False
        elif 'find' in change:
            if change['after'] not in have:
                return False
        else:
            if any(text not in have for text in new_texts(change, action.get('provider'))):
                return False
    return True


# Google's label for a refusal (google_api.error_reason) -> what was refused, in plain words. Each says nothing changed.
TURNED_OFF = ('SERVICE_DISABLED', 'accessNotConfigured', 'API_DISABLED')
NO_SCOPE = ('ACCESS_TOKEN_SCOPE_INSUFFICIENT', 'insufficientPermissions', 'insufficientScopes')
NO_EDIT = ('insufficientFilePermissions', 'appNotAuthorizedToFile', 'cannotModifyViewersCanCopyContent', 'fileWriterTeamDriveMoveInDisabled')
FULL = ('storageQuotaExceeded', 'teamDriveFileLimitExceeded', 'numChildrenInNonRootLimitExceeded')
BUSY = ('userRateLimitExceeded', 'rateLimitExceeded', 'dailyLimitExceeded', 'quotaExceeded', 'RATE_LIMIT_EXCEEDED',
        'RESOURCE_EXHAUSTED', 'sharingRateLimitExceeded')
POLICY = ('domainPolicy', 'ORG_POLICY_VIOLATION', 'cannotCreateFile')


def failed(action, status, reason=None):
    """The to-do's line when the doc refused the write: what was refused, in plain words, and that nothing changed.
    `reason` is Google's label from its error body; the error number stays at the end for support."""
    if status in (409, 412):
        return 'The doc changed since this was drafted. Nothing was changed; ask for a new draft.'
    if status == 423:
        return 'The doc is locked (open with a lock somewhere). Nothing was changed; try again later.'
    create = action.get('op') == 'create'
    if reason in TURNED_OFF:
        return 'Google Docs is turned off for this Google sign-in, so it can’t write docs. Nothing was changed.'
    if reason in NO_SCOPE:
        return ('This sign-in may read docs but not create them. Nothing was changed.' if create else
                'This sign-in may read docs but not change them. Nothing was changed.')
    if reason in FULL:
        return 'Your Google Drive is full, so the new doc didn’t fit. Nothing was changed; free up space and try again.'
    if reason in BUSY:
        return 'Google Docs is too busy for this account right now. Nothing was changed; try again in a few minutes.'
    if reason in POLICY:
        return 'Your organization’s Google settings don’t allow this. Nothing was changed.'
    if reason in NO_EDIT or (not create and status == 403):
        return 'This account can view the doc but not edit it. Nothing was changed; ask the doc’s owner for edit access.'
    if create and status == 403:
        return f'{where(action)} didn’t let this account create the doc (error 403). Nothing was changed; try again or ask for a new draft.'
    return (f'{where(action)} refused to create the doc (error {status}). Nothing was changed; try again or ask for a new draft.'
            if create else f'{where(action)} refused the changes (error {status}). Nothing was changed; try again or ask for a new draft.')


def made_by_itself(job):
    """Whether this write is a new doc made while its to-do was prepared (no OK needed), from its job's approval id."""
    return bool(job) and str(job['approval_id'] or '').startswith(NEW_DOC)


def link_of(message_id, provider=None):
    """A made Google Doc's link from its write's message id (docwrite:<file id>), or a Notion page's; None for Word or
    anything else."""
    found = re.fullmatch(r'docwrite:([\w-]{1,200})', str(message_id or ''))
    if found and provider == 'notion':
        return f'https://www.notion.so/{found[1]}' if re.fullmatch(r'[0-9a-f]{32}', found[1]) else None
    return google_link(found[1]) if found else None


def google_link(file_id):
    return f'https://docs.google.com/document/d/{file_id}/edit'


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
        named = str((para.get('paragraphStyle') or {}).get('namedStyleType') or 'NORMAL_TEXT')
        out.append({'text': text, 'editable': editable, 'at': at, 'style': STYLE_OF.get(named, named.lower()),
                    'list': bool(para.get('bullet'))})
    return out


def google_snapshot(doc, file_id):
    return {'version': str(doc.get('revisionId') or ''), 'title': str(doc.get('title') or ''),
            'url': f'https://docs.google.com/document/d/{file_id}/edit', 'paragraphs': google_paragraphs(doc)}


STYLE = {'h1': 'HEADING_1', 'h2': 'HEADING_2', 'h3': 'HEADING_3', 'p': 'NORMAL_TEXT'}
STYLE_OF = {v: k for k, v in STYLE.items()}  # a paragraph's named style as the run reads it (h1, p; else Google's, lowercased)
PRESET = {'bullet': 'BULLET_DISC_CIRCLE_SQUARE', 'number': 'NUMBERED_DECIMAL_ALPHA_ROMAN'}


def _positions(paras, changes):
    """[(where, rank, order, change, paragraph index, start, end)] for each change, in the doc's own text."""
    joined = '\n'.join(p['text'] for p in paras)
    starts, at = [], 0
    for p in paras:
        starts.append(at)
        at += len(p['text']) + 1
    out = []
    for order, change in enumerate(changes):
        needle = change.get('find', change.get('after', change.get('format')))
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


def _span(start, end):
    return {'startIndex': start, 'endIndex': end}


def styled(start, new, listed=False):
    """The requests that give new paragraphs (google_lines), their text from document index `start` on, their own look:
    each one's heading or normal style, its list, plain text but for its marks. Inserted text takes the look of the text
    it follows (a list item's bullet, a bold end), so the rest is set back: bullets go only after a list item (listed)."""
    ops, marks, runs, at = [], [], [], start
    for style, kind, text, found in new:
        end = at + utf16(text) + 1
        ops.append({'updateParagraphStyle': {'range': _span(at, end), 'paragraphStyle': {'namedStyleType': STYLE[style]},
                                             'fields': 'namedStyleType'}})
        if runs and runs[-1][0] == kind:
            runs[-1][2] = end
        else:
            runs.append([kind, at, end])
        for s, e, mark, link in found:
            marks.append({'updateTextStyle': {'range': _span(at + utf16(text[:s]), at + utf16(text[:e])),
                                              'textStyle': {'link': {'url': link}} if mark == 'link' else {mark: True}, 'fields': mark}})
        at = end
    # without the last newline, which may end the doc: a range in a paragraph styles all of it
    ops.append({'updateTextStyle': {'range': _span(start, at - 1), 'textStyle': {}, 'fields': 'bold,italic,underline,link'}})
    for kind, a, b in runs:
        if kind:
            ops.append({'createParagraphBullets': {'range': _span(a, b - 1), 'bulletPreset': PRESET[kind]}})
        elif listed:
            ops.append({'deleteParagraphBullets': {'range': _span(a, b - 1)}})
    return ops + marks


def google_format(paras, k, s, e, change, last):
    """The requests for a {format} change: its text's look, or its paragraphs' (k through last). None moves any index."""
    style, para = change.get('style', 'link'), paras[k]
    if style in TEXT_FORMATS:
        look = ({'link': {'url': change['link']}}, 'link') if style == 'link' else ({}, 'bold,italic,underline') \
            if style == 'plain' else ({style: True}, style)
        return [{'updateTextStyle': {'range': _span(para['at'][s], para['at'][e]), 'textStyle': look[0], 'fields': look[1]}}]
    span = _span(para['at'][0], paras[last]['at'][0] + 1)  # a paragraph's style is set by any range in it
    if style == 'page_break':
        return [{'updateParagraphStyle': {'range': span, 'paragraphStyle': {'pageBreakBefore': True}, 'fields': 'pageBreakBefore'}}]
    if style in PRESET:
        return [{'createParagraphBullets': {'range': span, 'bulletPreset': PRESET[style]}}]
    if style == 'no_list':
        return [{'deleteParagraphBullets': {'range': span}}]
    return [{'updateParagraphStyle': {'range': span, 'paragraphStyle': {'namedStyleType': STYLE[style]}, 'fields': 'namedStyleType'}}]


def google_requests(doc, changes):
    """The batchUpdate requests for these changes: formatting first (it moves no index), then the text, last in the doc
    first so earlier indexes stay put."""
    paras = google_paragraphs(doc)
    if not paras:
        raise ValueError('changed')
    steps, looks, listed = [], [], [p['list'] for p in paras]
    found = _positions(paras, changes)
    for k, s, e, order, change in found:
        if 'format' in change:
            if not paras[k]['editable']:
                raise ValueError('changed')
            last = _positions(paras, [{'find': change['through']}])[0][0] if 'through' in change else k
            looks += google_format(paras, k, s, e, change, last)
            if change.get('style') in ('bullet', 'number', 'no_list'):
                listed[k:last + 1] = [change['style'] != 'no_list'] * (last + 1 - k)
    for k, s, e, order, change in found:
        para = paras[k]
        if 'format' in change:
            continue
        if 'find' in change:
            if not para['editable']:
                raise ValueError('changed')
            a, b = para['at'][s], para['at'][e]
            ops = ([{'deleteContentRange': {'range': {'startIndex': a, 'endIndex': b}}}] if b > a else [])
            if change['replace']:
                ops.append({'insertText': {'location': {'index': a}, 'text': change['replace']}})
            steps.append(((a, 0, order), ops))
        else:
            new = google_lines(change.get('insert') or change.get('append'))
            at = para['at'][-1]  # before this paragraph's newline: its text ends, the new paragraphs follow
            ops = [{'insertText': {'location': {'index': at}, 'text': ''.join('\n' + text for _, _, text, _ in new)}}]
            steps.append(((at, 2 if 'append' in change else 1, order), ops + styled(at + 1, new, listed[k])))
    return looks + [op for _, ops in sorted(steps, key=lambda step: step[0], reverse=True) for op in ops]


def google_html(title, body):
    """A new Google Doc's content: Drive converts this HTML (headings, paragraphs, lists, bold, italic, links) to a doc."""
    tags = {'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'p': 'p'}
    parts, open_list = [], None
    for style, kind, text, marks in google_lines(body):
        wanted = {'bullet': 'ul', 'number': 'ol'}.get(kind)
        if open_list != wanted:
            parts.append((f'</{open_list}>' if open_list else '') + (f'<{wanted}>' if wanted else ''))
            open_list = wanted
        inner, at = '', 0
        for s, e, mark, link in marks:
            piece = html.escape(text[s:e], quote=False)
            inner += html.escape(text[at:s], quote=False) + (f'<a href="{html.escape(link)}">{piece}</a>' if mark == 'link' else
                                                             f'<b>{piece}</b>' if mark == 'bold' else f'<i>{piece}</i>')
            at = e
        inner += html.escape(text[at:], quote=False)
        parts.append(f'<li>{inner}</li>' if wanted else f'<{tags[style]}>{inner}</{tags[style]}>')
    parts.append(f'</{open_list}>' if open_list else '')
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>{html.escape(title, quote=False)}</title></head>'
            f'<body>{"".join(parts)}</body></html>')


def google_fill(body):
    """The batchUpdate requests that write a new doc's text into an empty Google Doc: its paragraphs, then their look
    (styled: headings, lists, marks)."""
    found = google_lines(body)
    return [{'insertText': {'location': {'index': 1}, 'text': '\n'.join(text for _, _, text, _ in found)}}] + styled(1, found)


def google_upload(token, title, body, boundary='tm-doc-write-boundary'):
    """(bytes, content type) of a multipart upload that creates the doc, tagged with this write's token (appProperties)
    so an unclear outcome finds it again. Drive picks the id: it takes no pre-generated one for a Google Doc."""
    meta = json.dumps({'name': title, 'mimeType': 'application/vnd.google-apps.document', 'appProperties': {WRITE_KEY: token}},
                      ensure_ascii=False)
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
        gog = getattr(self.connector, 'gog_google', lambda a: False)
        account = next((a for a in self.config.get('accounts', []) if a.get('id') == action['account_id']
                        and (a.get('service') in DOC_SERVICES or (action['op'] == 'create' or action.get('made')) and gog(a))), None)
        if not account:
            raise OwnerError('That Docs connection is no longer here. Nothing was changed.')
        writes = self.connector.writes_on(self.config, account, self.helpers)
        # a gog sign-in edits only a doc it made for this to-do (validate's made), with the Drive access that made it
        if action['op'] not in writes and not (action['op'] == 'edit' and action.get('made') and gog(account) and 'create' in writes):
            raise OwnerError('Writing docs is not allowed for this connection anymore. Nothing was changed.')
        return self.connector.Writer(self.config, account, self.helpers)

    def snapshot(self, writer, file_id):
        return snapshot(writer, file_id)

    def preflight(self, action):
        writer = self.writer(action)
        try:
            if action['op'] == 'done':
                return  # marking a task done twice leaves it done
            if action['op'] == 'edit':
                current = self.snapshot(writer, action['file_id'])
                if current['version'] != action['version']:
                    raise OwnerError('The doc changed since this was drafted. Nothing was changed; ask for a new draft.')
                resolve(current, action['changes'])
                return
            proof = action.setdefault('proof', {})
            if writer.provider == 'notion':
                proof.setdefault('since', timeutil.clock().replace(second=0, microsecond=0).isoformat())  # Notion stamps to the minute
            elif writer.provider == 'google':
                proof.setdefault('token', uuid.uuid4().hex)  # set once, before the write: what reconcile looks for
            elif not proof.get('name'):
                proof['name'] = next((name for name in (word_name(action['title'], n) for n in range(1, 10))
                                      if writer.lookup(name) is None), None)
                if not proof['name']:
                    raise OwnerError('Files with that name are in your OneDrive already. Nothing was created; give it another title.')
        except self.helpers.SourceError:
            raise OwnerError('I couldn’t reach the doc. Nothing was changed; tap it again.') from None

    def send(self, action, job):
        writer = self.writer(action)
        try:
            if action['op'] == 'done':
                return writer.mark_done(action['file_id'])
            if action['op'] == 'create':
                return self.create(writer, action, job)
            return self.edit(writer, action)
        except self.helpers.SourceError as error:
            if error.status == 429:
                return {'not_sent': True}
            if error.status == 409 and action['op'] == 'create':
                return self.reconcile(action, job)  # this approval's doc is there already: the earlier try went through
            if error.status in (400, 401, 403, 404, 409, 412, 423):
                reason = getattr(error, 'reason', None)
                LOG.warning('doc write refused op=%s provider=%s status=%s reason=%s', action['op'], action.get('provider'),
                            error.status, reason or '-')  # labels only: never the doc's text or a token
                return {'rejected': error.status, **({'reason': reason} if reason else {})}
            return {}  # unknown: never written again; reconcile reads the doc

    def create(self, writer, action, job):
        proof = action.get('proof') or {}
        if writer.provider == 'notion':
            if not proof.get('since'):
                return {}  # never made without its start: reconcile looks for it from then
            made = writer.create(action['title'], action['body'], action.get('parent'))
            return {'message_id': 'docwrite:' + made['id'], **({'url': made['url']} if str(made.get('url') or '').startswith('https://') else {})} \
                if re.fullmatch(r'[0-9a-f]{32}', str(made.get('id') or '')) else {}
        if writer.provider == 'google':
            if not proof.get('token'):
                return {}  # never made without its token: reconcile checks the older kind
            made = writer.make(proof['token'], action['title'], action['body'],
                               google_upload(proof['token'], action['title'], action['body']), google_fill(action['body']))
            found = str((made or {}).get('id') or '')
            if not re.fullmatch(r'[\w-]{1,200}', found):
                return {}  # unclear: reconcile finds it by its token, never makes it again
            return {'message_id': 'docwrite:' + found, 'url': google_link(found)}
        made = writer.create(proof['name'], docx_new(action['body']))
        drive = ((made.get('parentReference') or {}).get('driveId') or '')
        return {'message_id': 'docwrite:' + drive + '!' + str(made.get('id') or ''),
                **({'url': made['webUrl']} if str(made.get('webUrl') or '').startswith('https://') else {})}

    def edit(self, writer, action):
        if writer.provider == 'notion':  # read again right before, pinned to the version the owner approved
            return writer.edit(action['file_id'], action['changes'], action['version'])
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
            if action['op'] == 'done':
                return {'message_id': 'docwrite:' + action['file_id']} if writer.task(action['file_id'])[2] is None else {}
            if action['op'] == 'create':
                proof = action.get('proof') or {}
                if writer.provider == 'notion':
                    since = dt.datetime.fromisoformat(proof['since']) if proof.get('since') else None
                    found = writer.written(action['title'], since) if since else None
                    return {'message_id': 'docwrite:' + found['id'], **({'url': found['url']} if str(found.get('url') or '').startswith('https://') else {})} \
                        if found else {}
                if writer.provider == 'google':
                    # an older write's generated id (proof file_id, before 2026-11-03) is still looked up by that id
                    found = (writer.written(proof['token']) if proof.get('token') else None) or (
                        writer.find(proof['file_id']) if proof.get('file_id') else None)
                    if not found or found.get('trashed') or not found.get('id'):
                        return {}
                    file_id = str(found['id'])
                    if getattr(writer, 'gog', False):
                        writer.fill(file_id, google_fill(action['body']))  # only while it is still empty
                    return {'message_id': 'docwrite:' + file_id, 'url': google_link(file_id)}
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
    if writer.provider == 'notion':
        return writer.snapshot(file_id)
    if writer.provider == 'google':
        return google_snapshot(writer.document(file_id), file_id)
    item, data = writer.item_and_bytes(file_id)
    try:
        return docx_snapshot(item, data, file_id)
    except DocxError as error:
        raise writer.helpers.SourceError(str(error)) from None


def targets(config, connector, helpers, check=True):
    """{account id: {name, email, provider, boundary, writes}}: where a doc may be written. The owner's Docs connections,
    and their own gog Google sign-ins that can already make a doc (drive or drive.file), never one a Fleet shares.
    check=False leaves a Docs connection's writes unread (None: the prompt lists it, validate checks)."""
    out = {}
    gog = getattr(connector, 'gog_google', lambda a: False)
    for a in config.get('accounts', []):
        own = a.get('service') in DOC_SERVICES
        if a.get('shared') or not (own or gog(a)) or a.get('actions') is False:
            continue  # a Fleet's share only reads; Can do things off (abilities.py) writes nothing
        writes = sorted(connector.writes_on(config, a, helpers)) if check or not own else None
        if not own and not writes:
            continue
        out[a['id']] = {'name': str(a.get('display_name') or a.get('workspace_name') or a.get('email') or a['id']),
                        'email': str(a.get('email') or a.get('member_email') or '').lower(),
                        'provider': connector.provider(config, a) if own else 'google',
                        'boundary': a.get('boundary') or '', 'writes': writes,
                        **({'gog': True} if not own else {})}
    return out


def area(config, account_ids):
    """The to-do's area: the boundaries and addresses of its own accounts."""
    mine = [a for a in config.get('accounts', []) if a.get('id') in set(account_ids or ())]
    return {'boundaries': sorted({a['boundary'] for a in mine if kind_of(a.get('boundary'))}),
            'emails': sorted({str(a['email']).lower() for a in mine if '@' in str(a.get('email') or '')})}


def context(config, connector, helpers, files, value, area=None):
    """What validate needs, read only when the next actions hold a doc write: where docs may be written (targets), the
    to-do's area, and each doc an edit names, read now (its version is the one the owner approves)."""
    items = value if isinstance(value, list) else [value] if isinstance(value, dict) else []
    wanted = [a for a in items if isinstance(a, dict) and a.get('kind') == KIND]
    if not wanted or not connector:
        return None
    accounts = targets(config, connector, helpers)
    snapshots = {}
    for w in wanted:
        file_id = file_id_of(w.get('file_id'))
        known = files.get(file_id)
        if w.get('op') != 'edit' or not known or file_id in snapshots or not can_edit(accounts.get(known['account_id']) or {}, known):
            continue
        account = next(a for a in config['accounts'] if a['id'] == known['account_id'])
        try:
            snapshots[file_id] = snapshot(connector.Writer(config, account, helpers), file_id)
        except helpers.SourceError as error:
            snapshots[file_id] = {'docs_edit_unsupported': 'That file can’t be edited here (only Google Docs and .docx Word files)',
                                  'docs_file_too_large': 'That file is too large to edit here',
                                  'docs_not_connected': 'Reading docs is not allowed for this connection'}.get(
                                      error.category, f'The doc could not be read ({error.category})')
    return {'accounts': accounts, 'files': files, 'snapshots': snapshots, 'area': area, 'google': google_offered(accounts, config)}

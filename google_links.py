"""The Google files linked in a text: a Doc, Sheet or Slides file, or a Drive link that doesn't say which. No network.

A link is read in the forms people and mail programs send it: with /u/0/ or a domain in it, as docs.google.com/open?id=,
drive.google.com/open?id= or /file/d/, behind a link checker or a click counter (Outlook's Safe Links, Proofpoint,
google.com/url), and with its id cut by a line end in a quoted mail. A published page (/d/e/...) and a folder are no file.

An HTML message's link behind other words is kept in its text (keep_links): without it, "see the plan" says nothing.
"""
import html
import re
import urllib.parse

DOC, SHEETS, SLIDES, ANY = 'doc', 'sheets', 'slides', 'any'
KINDS = {'document': DOC, 'spreadsheets': SHEETS, 'presentation': SLIDES}
ID = '[A-Za-z0-9_-]{20,100}'
ID_LENGTH = 44  # a Google file's id as Google makes it now: what an id cut by a line end is completed to
HOST = re.compile(r'(?:https?(?::|%3A|%253A|-3A)(?://|%2F%2F|%252F%252F|__)|(?<![A-Za-z0-9.-]))(docs|drive)\.google\.com(?=[/%_])', re.I)
PATH = re.compile(r'/(?:a/[^/\s]{1,100}/)?(?:'
                  rf'(?P<kind>document|spreadsheets|presentation)/(?:u/\d+/)?(?:d/(?P<id>{ID})|open\?(?:[^\s#]{{0,80}}[&;])?id=(?P<open>{ID}))'
                  rf'|(?:file/(?:u/\d+/)?d/(?P<file>{ID})|(?:open|uc)\?(?:[^\s#]{{0,80}}[&;])?id=(?P<any>{ID})))(?P<tail>[^\s<>"\\)\]]*)')
TAIL = re.compile(r'[^\s<>"\\)\]]{0,600}')
CUT = re.compile(r'[ \t]*\r?\n(?:[ \t]*>)*[ \t]*([A-Za-z0-9_-]{1,24})(?![A-Za-z0-9_-])')
TAG = re.compile(r'<a\b([^>]{1,4000})>', re.I)
HREF = re.compile(r'''\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))''', re.I)
CLOSE = re.compile('</a', re.I)
ADDED = re.compile(r' \(https://(?:docs|drive)\.google\.com/[^\s()]{20,200}\)')  # what keep_links adds
SHOWN = {DOC: 'document/d/{}/edit', SHEETS: 'spreadsheets/d/{}/edit', SLIDES: 'presentation/d/{}/edit'}


def _tail(text, at):
    """What follows the host in a link, decoded when the link is inside another one's address."""
    tail = TAIL.match(text, at)[0]
    if tail[:1] == '_':  # Proofpoint's urldefense v2: "/" as "_", any other sign as "-" and its code
        tail = urllib.parse.unquote(tail.split('&')[0].replace('%', '').replace('-', '%').replace('_', '/'))
    elif tail[:1] == '%':
        tail = tail.split('&')[0]
        for _ in range(2):  # a link checker around a click counter
            if tail[:1] == '%':
                tail = urllib.parse.unquote(tail)
    return tail


def find(text):
    """[(kind, file id, the rest of the link)] of the Google files linked in a text, in order, as often as they are linked.
    kind: doc, sheets, slides, or any for a Drive link, which doesn't say which."""
    text = str(text or '')
    if 'google' not in text.lower():
        return []
    out = []
    for host in HOST.finditer(text):
        tail = _tail(text, host.end())
        m = PATH.match(tail)
        if not m or m['kind'] and host[1].lower() != 'docs':
            continue
        found, rest = m['id'] or m['open'] or m['file'] or m['any'], html.unescape(m['tail'])
        if len(found) < ID_LENGTH and not rest and text.startswith(tail, host.end()):
            more = CUT.match(text, host.end() + m.end('tail'))
            if more and len(found) + len(more[1]) == ID_LENGTH:
                found += more[1]
        out.append((KINDS.get(m['kind'] or '', ANY), found, rest))
    whole = {f for _, f, _ in out if len(f) >= ID_LENGTH}
    # an id cut short, whole elsewhere in the text, is that file
    return [(k, f, rest) for k, f, rest in out if len(f) >= ID_LENGTH or not any(w.startswith(f) for w in whole)]


def ids(text, kind):
    """The ids of the linked files of this kind, in order, once each. any: those no other link in the text says more of."""
    found = find(text)
    known = {f for k, f, _ in found if k != ANY}
    return list(dict.fromkeys(f for k, f, _ in found if k == kind and (kind != ANY or f not in known)))


def keep_links(value):
    """An HTML message where a link to a Google file behind other words has its address after them, once each, so its
    text still has it. Any other HTML comes back as it is."""
    value = str(value or '')
    if 'google' not in value.lower():
        return value
    out, at, said = [], 0, set()
    for tag in TAG.finditer(value):
        if tag.start() < at:
            continue
        href = HREF.search(tag[1])
        found = find(html.unescape(next((g for g in href.groups() if g), ''))) if href else []
        if not found:
            continue
        kind, file_id, rest = found[0]
        close = CLOSE.search(value, tag.end()) if len(said) < 50 and file_id not in said else None
        if not close:
            continue
        end = close.start()
        said.add(file_id)
        if file_id in value[tag.end():end]:  # its words are the address itself
            continue
        gid = re.search(r'[#?&](gid=\d{1,12})', rest) if kind == SHEETS else None
        url = ('https://docs.google.com/' + SHOWN[kind].format(file_id) + (f'#{gid[1]}' if gid else '') if kind in SHOWN
               else f'https://drive.google.com/file/d/{file_id}/view')
        out += [value[at:end], f' ({url})']
        at = end
    return ''.join(out) + value[at:]

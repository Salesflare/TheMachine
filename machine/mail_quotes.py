"""Which lines of an email its sender wrote and which they quote, told by structure, in any language: lines with ">", the
attribution above them, a header block (From, Sent, To, Subject by its shape), and in HTML the containers mail programs
put a quote in. Used for a mail's text (machine/text.py), the owner's signature (signatures.py) and what a mail asks
(machine/store/promises.py)."""
from html.parser import HTMLParser
import re

LAYER = 0  # message parsing

TAGS = r'\s*(?:\[[^\]\n]{1,24}\]\s*)*'  # "[EXT] " before a subject
FORWARD_SUBJECT = re.compile(rf'(?i)^{TAGS}(?:fwd?|tr|wg|doorst)\s*:')

# A top-level reply header whose quote may have no ">" under it: "On Thu, 8 Oct 2026, Ann <a@b.c> wrote:" (often wrapped
# over two or three lines), and Outlook's "Original Message" and "From: … Sent:". Everything else is told by structure.
REPLY_HEADER = re.compile(
    r'^(?:On|Le|Op|Am|El|Il|Den|Em)\b[^\n]{0,250}(?:\r?\n(?!>)[^\n]{0,250}){0,2}?'
    r'\s(?:wrote|a\s+écrit|schreef|schrieb|escribió|ha\s+scritto|skrev|escreveu)\b[^\n]{0,200}?(?:\r?\n(?!>)[^\n]{0,200}?)?:[ \t]*\r?$'
    r'|^-{2,}\s*Original Message\s*-{2,}[ \t]*\r?$'
    r'|^From:[ \t]\S[^\n]*\r?\nSent:[ \t]', re.M | re.I)

ADDRESS = re.compile(r'[^\s<>()\[\]"\',;:]+@[^\s<>()\[\]"\',;:]+\.[^\W\d_]{2,}')
YEAR = re.compile(r'(?<!\d)(?:(?:19|20)\d\d(?!\d)|\d{1,2}[./-]\d{1,2}[./-]\d{2}(?!\d))')
TIME = re.compile(r'(?<!\d)\d{1,2}[:.h]\d{2}(?!\d)')
ORIGINAL = re.compile(r'(?i)^\s*-{2,}\s*Original Message\s*-{2,}\s*$')
DASHED = re.compile(r'^\s*-{4,7}\s*[^-\s][^\n]{2,60}?\s*-{4,7}\s*$')  # "-----Ursprüngliche Nachricht-----"
FORWARDED = re.compile(r'^\s*-{8,}\s*[^-\s][^\n]{2,60}?\s*-{4,}\s*$')  # "---------- Forwarded message ---------"
RULE = re.compile(r'^\s*[_\-=—–]{5,}\s*$')
LABEL = re.compile(r'^\s*[*_]{0,2}([^\W\d_][^\n:：*<@]{0,24}?)\s*[*_]{0,2}\s*(?::\s*[*_]{0,2}\s+|：\s*[*_]{0,2}\s*)(\S.*)$')
FOOTER = re.compile(r'^(?:--\s?|[-_=]{10,})$')  # a signature or a mailing list's footer under the quote
PREFIX = re.compile(rf'^{TAGS}(?:[^\W\d_]{{1,6}}(?:\[\d+\])?\s*[:：]\s*)+')  # "Re: ", "AW: ", "Re: Fwd: "
REPLY = re.compile(rf'(?i)^{TAGS}re\s*[:：]')


def _mark(line):
    return line.lstrip().startswith('>')


def _next(lines, i):
    """The index of the next line that says something, from i on, or len(lines)."""
    while i < len(lines) and not lines[i].strip():
        i += 1
    return i


def _run_end(lines, i):
    """The end of a run of ">" lines from i, with the blank lines inside it and what a mail program wrapped without its
    mark: right between two marked lines, after one that was full and stopped in the middle of a sentence, or of a link."""
    end = i
    while i < len(lines):
        if _mark(lines[i]):
            i = end = i + 1
        elif not lines[i].strip():
            i = _next(lines, i)
            if i >= len(lines) or not _mark(lines[i]):
                break
        else:
            above, after = lines[i - 1].rstrip(), i
            while after < len(lines) and lines[after].strip() and not _mark(lines[after]):
                after += 1
            if after >= len(lines) or not _mark(lines[after]) or not _mark(above):
                break
            full = len(above) >= 60 and above[-1] not in '.?!:;)…' and (after == i + 1 or lines[i].lstrip()[0].islower())
            if not full and above[-1] not in '([<':
                break
            i = after
    return end


def _attribution(lines, i, quoted):
    """Where the line that says whose quote starts at i begins ("Ann <a@b.c> napisał(a):", over up to three lines), or
    None: it ends in a colon and names an address or a date with its time, in whatever language."""
    k = i - 1
    while k >= 0 and i - k <= 8 and not lines[k].strip():
        k -= 1
    if k < 0 or i - k > 8 or quoted[k] or _mark(lines[k]):
        return None
    colon = lines[k].rstrip().rstrip('*_').endswith((':', '：'))
    found = None
    for start in range(k, max(k - 3, -1), -1):
        if not lines[start].strip() or quoted[start] or _mark(lines[start]) or (start < k and lines[start].rstrip().endswith(('.', '!', '?', ':'))
                                                                              and not re.search(r'\d\.$|\b\w{1,4}\.$', lines[start].rstrip())):
            break
        said = ' '.join(x.strip() for x in lines[start:k + 1])
        if len(said) > 400:
            break
        dated, named = bool(YEAR.search(said) and TIME.search(said)), bool(ADDRESS.search(said))
        match = REPLY_HEADER.match('\n'.join(x.strip() for x in lines[start:k + 1]))
        if match or dated and (colon or named):
            return start
        if named and colon and found is None:
            found = start
    return found


def _bare(subject):
    """A subject without its "Re:", "AW:" and the like, for comparing."""
    return ' '.join(PREFIX.sub('', str(subject or '')).casefold().split())


def _shape(lines, i):
    """The values of a mail's header block at line i, by its shape: lines "label: value", who it is from first, its date
    second and at least three in all; None when it isn't one."""
    first = LABEL.match(lines[i]) if i < len(lines) else None
    if not first or '-' in first[1]:  # "Delivered-To:": a mail's raw headers
        return None
    values = [first[2]]
    for line in lines[i + 1:i + 14]:
        found = LABEL.match(line)
        if found:
            values.append(found[2])
        elif not line.strip():
            break
        elif len(values) == 1:  # a sender that wraps before the date
            values[0] += ' ' + line.strip()
        if len(values) == 6:
            break
    if len(values) < 3 or not YEAR.search(values[1]) or not re.search(r'\d\D+\d', values[1]):
        return None
    return values


def _header(lines, i, subject, people):
    """Who a quoted mail's header block at line i says it is from, or None: its shape, and either the sender's address, a
    sender this mail also has, or this mail's own subject."""
    values = _shape(lines, i)
    if not values:
        return None
    own, sender = _bare(subject), values[0].strip(' *_')
    same = len(own) >= 3 and any(_bare(v.strip(' *_')) == own for v in values[2:])
    named = len(sender) >= 3 and people and re.sub(r'\s*<.*', '', sender).strip(' "\'').casefold() in people
    return sender if ADDRESS.search(sender) or same or named else None


def _forward(sender, subject, people):
    """Whether a mail that has another mail under this header sends it on: an answer goes to who it quotes (or comes
    from them). people: everyone on the mail, '' when not known."""
    return bool(people) and not REPLY.match(subject or '') and not _with(sender, people)


def _with(sender, people):
    """Whether who a header names is on the mail: by address, or by name (who writes from a second address)."""
    addresses = [a.casefold() for a in ADDRESS.findall(sender)]
    name = ' '.join(re.split(r'[<(\[]|\S+@', sender, maxsplit=1)[0].strip(' "\'*').casefold().split())
    if any(a in people for a in addresses) or len(name) >= 5 and ' ' in name and name in people:
        return True
    words, called = re.findall(r'[^\W\d_]{3,}', name), re.findall(r'[^\W\d_]+', re.sub(r'@\S+', ' ', people))
    return words[0] in called and len(words[0]) > 3 if addresses and words else any(w in called for w in words)


def _sent_on(lines, subject, people):
    """Whether a quote holds a forwarded mail: it starts with that mail's own header ("From", "Subject", "Date", "To" in
    any order, as Apple Mail's forward has it), from someone this mail isn't with."""
    lines = [x.strip().lstrip('> ') for x in lines[:12]]
    for i in range(min(4, len(lines))):
        found = [m[2] for x in lines[i:i + 4] if (m := LABEL.match(x))]
        if LABEL.match(lines[i]) and len(found) >= 3 and (sender := next((v for v in found if ADDRESS.search(v)), None)):
            return _forward(sender, subject, people)
    return False


def sent_on(lines):
    """The index of the first line of a mail sent on in these lines, which is someone else's: a forward's dashed line or
    the mail's own header, marked or not; None when there is none."""
    first = _next(lines, 0)
    for i, line in enumerate(lines):
        if FORWARDED.match(line):
            after = _next(lines, i + 1)
            if i == first or _shape([x.lstrip('> ') for x in lines[after:after + 14]], 0):
                return i
        elif _mark(line) and (i == 0 or not _mark(lines[i - 1])):
            if _sent_on(lines[i:i + 12], '', '-'):
                return i
        elif (values := _shape(lines, i)) and ADDRESS.search(values[0]):
            while i and (not lines[i - 1].strip() or RULE.match(lines[i - 1]) or DASHED.match(lines[i - 1])):
                i -= 1
            return i
    return None


def _wrote(lines, i):
    """Whether lines[i] starts a reply header with nothing marked under it ("On …, Ann <a@b.c> wrote:")."""
    if not re.match(r'(?i)(?:On|Le|Op|Am|El|Il|Den|Em)\b', lines[i]) or not any(x.rstrip().endswith(':') for x in lines[i:i + 4]):
        return False
    match = REPLY_HEADER.match('\n'.join(lines[i:i + 4]))
    if not match:
        return False
    said, size = match[0], match[0].count('\n') + 1
    if not (ADDRESS.search(said) or (year := YEAR.search(said)) and (TIME.search(said) or size == 1 and (i == 0 or not lines[i - 1].strip())
                                                                  and len(said[year.end():].split()) <= 6)):
        return False  # "On Monday I met the client and as they wrote:"
    after = _next(lines, i + size)
    return after >= len(lines) or not _mark(lines[after])  # marked lines are a run of their own, with its attribution


def _said(lines, i, subject, people):
    """Whether an answer's lines[i] says whose quote follows, with nothing marked under it, in any language: a paragraph
    of its own, of one line or two, that names an address, a date and its time, and ends in a colon."""
    if not PREFIX.match(subject or '') or i and lines[i - 1].strip():
        return False
    for size in (1, 2):
        said = ' '.join(x.strip() for x in lines[i:i + size])
        if said.endswith((':', '：')) and (size == 1 or ADDRESS.search(lines[i]) or YEAR.search(lines[i])):
            break
    else:
        return False
    short = len(re.findall(r'[^\W\d_]{2,}', ADDRESS.sub('', said))) <= 14 and len(said) <= 200
    after = _next(lines, i + size)
    return bool(short and ADDRESS.search(said) and YEAR.search(said) and TIME.search(said) and after < len(lines) and not _mark(lines[after])
                and not LABEL.match(said) and (REPLY.match(subject) or not people or _with(said, people)))


def quoted(lines, subject='', people=''):
    """For each line whether it is quoted. A forward's lines are what it sends: none is. people: the mail's From, To and
    Cc in lower case when known, which tells a forward without its prefix from an answer."""
    out, sure = [False] * len(lines), bool(PREFIX.match(subject or ''))
    if FORWARD_SUBJECT.match(subject or ''):
        return out
    i = entries = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if _mark(line):
            start, end = i, _run_end(lines, i)
            above = _attribution(lines, i, out)
            if above is None and _sent_on(lines[start:end], subject, people):
                i = end
                continue
            if above is not None:
                start, sure = above, True
            elif end - i > 1:
                sure = True
            out[start:end] = [True] * (end - start)
            i = end
            after = _next(lines, i)
            if after < len(lines) and FOOTER.match(lines[after].rstrip()):
                out[after:] = [True] * (len(lines) - after)
                break
            continue
        rest = bool(ORIGINAL.match(line)) or _wrote(lines, i) or _said(lines, i, subject, people)
        if not rest and FORWARDED.match(line):
            sender = _header(lines, _next(lines, i + 1), subject, people)
            own = ADDRESS.search(people)
            if not (sender and people and _with(sender, people)) or not PREFIX.match(subject or '') and own and own[0] in sender.casefold():
                break
            rest = True  # an answer to who it quotes, from a program that dashes its answers so
        if not rest and DASHED.match(line):
            rest = _shape(lines, _next(lines, i + 1)) is not None
        if not rest and RULE.match(line) and people and PREFIX.match(subject or ''):
            # a help desk's "Ann, 18 Jun 2026 17:26" under a line: its newest is the mail itself, the next ones are quoted
            said = lines[k].strip() if (k := _next(lines, i + 1)) < len(lines) else ''
            if len(said) <= 80 and YEAR.search(said) and TIME.search(said) and not LABEL.match(said):
                entries += 1
                name = re.split(r'\d|,', said, maxsplit=1)[0]
                rest = entries > 1 and _with(name, people) and not _with(name, people[:own.end()] if (own := ADDRESS.search(people)) else '')
        if not rest:
            sender = _header(lines, i, subject, people)
            if sender is None and re.match(r'(?i)From:[ \t]\S', line) and i + 1 < len(lines) and re.match(r'(?i)Sent:[ \t]', lines[i + 1]):
                sender = LABEL.match(line)[2] if LABEL.match(line) else line
            if sender is not None:
                if _forward(sender, subject, people):
                    break
                rest = True
        if rest:
            start, sure = i, True
            while start and (not lines[start - 1].strip() or RULE.match(lines[start - 1])) and not out[start - 1]:
                start -= 1
            out[start:] = [True] * (len(lines) - start)
            break
        i += 1
    if not sure:  # one line that starts with ">" is no quote by itself
        return [False] * len(lines)
    return out


# -------------------------------------------------------------------------------------------------------------- HTML

VOID = {'br', 'img', 'hr', 'meta', 'link', 'input', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr', 'param'}
BREAKS = {'p', 'div', 'br', 'li'}
REST_IDS = {'divrplyfwdmsg', 'appendonsend', 'mail-editor-reference-message-container'}  # all that follows is the quoted mail
QUOTE_CLASSES = {'gmail_quote', 'yahoo_quoted', 'protonmail_quote', 'tutanota_quote', 'moz-cite', 'mail-quote'}


NESTED, CONTAINERS = 40, 2000  # quote containers followed in each other, and in one mail: what is deeper has the outer ones' place
LINE = re.compile('\r\n|[\n\r\x0b\x0c\x1c-\x1e\x85\u2028\u2029]')  # as str.splitlines


class _Lines(HTMLParser):
    """An HTML mail's lines as plain_html gives them, each with the quote containers it is in and where it starts."""

    def __init__(self):
        super().__init__()
        self.lines = [{'text': '', 'in': (), 'at': None, 'soft': False}]
        self.open, self.inside, self.tags, self.hidden, self.ids, self.at = [], (), {}, 0, 0, None
        self.kinds, self.starts, self.offsets = {}, {}, [0]

    def read(self, value):
        self.offsets = [0] + [m.end() for m in re.finditer('\n', value)]
        self.feed(value)
        self.close()
        return self.lines

    def _offset(self):
        row, column = self.getpos()
        return self.offsets[min(row, len(self.offsets)) - 1] + column

    def _break(self, soft=False):
        """A new line; soft: only where a container starts or ends, a line of its own when that container is a quote."""
        self.lines.append({'text': '', 'in': self.inside, 'at': None, 'soft': soft})

    def _container(self, tag, attrs):
        attrs = {k: str(v or '') for k, v in attrs}
        name = re.sub(r'^(?:x_)+', '', attrs.get('id', '').casefold())
        classes = {re.sub(r'^(?:x_)+', '', c) for c in attrs.get('class', '').casefold().split()}
        kind = None
        if name in REST_IDS:
            kind = 'rest'
        elif tag == 'blockquote':
            kind = 'cite' if attrs.get('type', '').casefold() == 'cite' or 'cite' in attrs or classes & QUOTE_CLASSES else 'plain'
        elif 'yahoo_quoted' in classes:
            kind = 'cite'
        elif 'gmail_quote' in classes:
            kind = 'around'  # holds the attribution, the quote and any answers between; a forward too
        if kind is None or len(self.inside) >= NESTED or self.ids >= CONTAINERS:
            return None
        self.ids += 1
        self.kinds[self.ids], self.starts[self.ids] = kind, self._offset()
        return self.ids

    def handle_starttag(self, tag, attrs):
        if self.at is None and tag != 'img':
            self.at = self._offset()
        if tag in ('script', 'style'):
            self.hidden += 1
            return
        found = self._container(tag, attrs)
        if tag not in VOID:
            self.open.append((tag, found))
            self.tags[tag] = self.tags.get(tag, 0) + 1
            self.inside += (found,) if found else ()
        if tag == 'img':
            self.at = None
        if not self.hidden and (tag in BREAKS or found):
            self._break(soft=tag not in BREAKS)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
            return
        for i in range(len(self.open) - 1, -1, -1) if self.tags.get(tag) else ():
            if self.open[i][0] == tag:
                for name, _ in self.open[i:]:
                    self.tags[name] -= 1
                closed = [q for _, q in self.open[i:] if q]
                rest = [q for q in closed if self.kinds[q] == 'rest']
                del self.open[i:]
                for q in rest:  # no end tag closes it
                    self.open.append(('#rest', q))
                    self.tags['#rest'] = self.tags.get('#rest', 0) + 1
                if closed:
                    self.inside = tuple(q for _, q in self.open if q)
                if closed and not self.hidden:
                    self._break(soft=True)
                break
        self.at = None

    def handle_data(self, data):
        if self.hidden:
            return
        at = self._offset()
        for n, part in enumerate(LINE.split(data)):
            if n:
                self._break()
            line = self.lines[-1]
            if part.strip() and line['at'] is None:
                line['at'] = at if self.at is None else self.at
            if part.strip():
                self.at = None
            line['text'] += part
            at += len(part) + 1


def _read_html(value, subject='', people=''):
    """(lines as text, which are quoted, where each starts in the HTML, how many quote containers each is in) of an
    HTML mail."""
    reader = _Lines()
    every = reader.read(str(value or ''))
    rows = [x for x in every if x['text'].strip()]
    text = [x['text'].strip() for x in rows]
    counts, held = set(), {}
    for n, x in enumerate(rows):
        for q in x['in']:
            held.setdefault(q, []).append(n)
    for q, kind in () if FORWARD_SUBJECT.match(subject or '') else reader.kinds.items():
        inside = held.get(q)
        if not inside:
            continue
        before = inside[0] - 1
        if kind == 'rest':
            at = inside[0]
            if FORWARDED.match(text[at]):
                continue
            sender = next((s for k in range(at, min(at + 3, len(text))) if (s := _header(text, k, subject, people))), None)
            if sender and _forward(sender, subject, people):
                continue
            counts.add(q)
        elif kind == 'cite':
            # Gmail's forward has no blockquote; another program's puts the forwarded mail in one, under its dashed line
            if not any(FORWARDED.match(text[k]) for k in range(max(0, before - 6), inside[0])) \
                    and not _sent_on(text[inside[0]:inside[-1] + 1], subject, people):
                counts.add(q)
        elif kind == 'plain' and before >= 0 and _attribution([*text[:before + 1], '>'], before + 1, [False] * (before + 2)) is not None:
            counts.add(q)
    seen = set()
    for x in rows:  # a quote starts where its container does
        x['at'] = min([reader.starts[q] for q in x['in'] if q not in seen and reader.kinds[q] != 'plain']
                      + ([] if x['at'] is None else [x['at']]), default=None)
        seen.update(x['in'])
    merged = []
    for x in every:
        x['depth'] = sum(q in counts for q in x['in'])
        if x['soft'] and merged and x['depth'] == merged[-1]['depth']:
            merged[-1]['text'] += x['text']
            merged[-1]['at'] = x['at'] if merged[-1]['at'] is None else merged[-1]['at']
        else:
            merged.append(x)
    rows = [x for x in merged if x['text'].strip()]
    text, depth = [x['text'].strip() for x in rows], [x['depth'] for x in rows]
    marks = quoted([('> ' if d else '') + t for t, d in zip(text, depth)], subject, people)
    return text, [bool(m or d) for m, d in zip(marks, depth)], [x['at'] for x in rows], depth


def mail_html(value, subject='', people=''):
    """An HTML mail as text, as plain_html gives it, with what it has in a quote container marked ">", as a plain mail
    marks it. A forward is whole."""
    text, _, _, depth = _read_html(value, subject, people)
    out = []
    for n, line in enumerate(text):
        if n and bool(depth[n]) != bool(depth[n - 1]) and depth[n - 1]:
            out.append('')  # what is written under a quote starts a paragraph
        out.append('>' * depth[n] + (' ' if depth[n] else '') + line)
    return '\n'.join(out)


def new_html(value):
    """An HTML mail up to the conversation it quotes."""
    value = str(value or '')
    _, marks, starts, _ = _read_html(value)
    first = next((s for s, m in zip(starts, marks) if m and s is not None), None)
    return value if first is None else re.sub(r'(?i)<hr\b[^>]*>(?:\s|<div\b[^>]*>)*$', '', value[:first])

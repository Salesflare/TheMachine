"""Message text: a mail's own words without the quoted history under them, its body from the plain and HTML parts
(plain_html), its attachments and inline images, invisible characters, the compact JSON the app stores (encoded), a
value cut to size (clamp), the address in a header (_address), and an encrypted copy of a database (seal_copy,
open_copy). Moved out of assistant.py as is. Also whether a quote is in a message (quoted_in)."""
import base64
import contextlib
import hashlib
import hmac
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sqlite3
import unicodedata

import google_links
from mail_senders import header_address as _address, recipients  # noqa: F401 (imported from here)
import message_seal
import portable
from machine.mail_quotes import FORWARD_SUBJECT, PREFIX, REPLY_HEADER, mail_html, quoted, sent_on  # noqa: F401 - REPLY_HEADER: importable from here

LAYER = 0  # message parsing


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def clamp(value, chars=300, items=10):
    if isinstance(value, str):
        return value if len(value) <= chars else value[:chars] + '…'
    if isinstance(value, list):
        return [clamp(v, chars, items) for v in value[:items]] + ([f'… {len(value) - items} more'] if len(value) > items else [])
    if isinstance(value, dict):
        return {k: clamp(v, chars, items) for k, v in value.items()}
    return value


class PlainHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        elif tag in ('p', 'div', 'br', 'li') and not self.hidden:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_html(value):
    parser = PlainHTML()
    parser.feed(str(value or ''))
    return '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())


QUOTED_HISTORY_KEPT = 3000
BODY_KEPT = 40000  # characters of a mail's text a source keeps


# Text parts that only tell the reader to open the HTML version.
PLAIN_PLACEHOLDER = re.compile(r'(?i)plain[- ]text version (?:is )?not available|requires an? html|'
                               r'view (?:this|the) (?:email|message) in (?:a|your) (?:web )?browser|use an html[- ]capable|'
                               r'(?:does not|doesn\'t|cannot|can\'t) (?:support|display|show) html|in html-opmaak|'
                               r'online versie van (?:deze|dit) (?:e-?mail|bericht)')


def mail_people(meta):
    """Everyone on a mail, in lower case, from its metadata (from, to, cc, reply-to): what tells a forward without its
    prefix from an answer (mail_quotes.quoted). '' when it names no one it went to."""
    meta = meta or {}
    if not (meta.get('to') or meta.get('cc')):
        return ''
    return ' '.join(', '.join(recipients(meta.get(k))) for k in ('from', 'to', 'cc', 'reply-to')).casefold().strip()


def split_quoted_history(text, subject='', people=''):
    """Return (new text, quoted history): the history under the sender's last own line, so answers written between
    quoted lines stay in the new text with what they answer. Forwarded messages are kept whole: they are the content."""
    lines = text.splitlines(keepends=True)
    marks = quoted([x.rstrip('\r\n') for x in lines], subject, people)
    own = [n for n, line in enumerate(lines) if line.strip() and not marks[n]]
    last = own[-1] + 1 if own else len(lines)
    if not re.search(r'\w', ''.join(x for x, m in zip(lines[last:], marks[last:]) if m)):
        return text, ''
    return ''.join(lines[:last]).rstrip(), ''.join(lines[last:]).lstrip('\r\n')


def _fit(text, subject, people):
    """A mail too long to keep whole, with what it quotes above the sender's own words cut short, so those stay."""
    lines = text.split('\n')
    marks = quoted([x.rstrip('\r') for x in lines], subject, people)
    room, out = max(0, BODY_KEPT - QUOTED_HISTORY_KEPT - sum(len(x) + 1 for x, m in zip(lines, marks) if not m)), []
    for line, mark in zip(lines, marks):
        room -= (len(line) + 1) * mark
        if not mark or room >= 0:
            out.append(line)
        elif out[-1:] != ['> […]']:
            out.append('> […]')
    return '\n'.join(out)


def _runs_cut(text, subject, people):
    """A mail's text with each long quote above the sender's last words cut to its start, as the history below them is."""
    if len(text) <= QUOTED_HISTORY_KEPT:
        return text
    lines = text.split('\n')
    marks, out, room = quoted([x.rstrip('\r') for x in lines], subject, people), [], 0
    if not any(x.strip() and not m for x, m in zip(lines, marks)):  # nothing of their own: kept as it came
        return text
    for n, (line, mark) in enumerate(zip(lines, marks)):
        room = (room if n and marks[n - 1] else QUOTED_HISTORY_KEPT) - len(line) - 1
        if not mark or room >= 0:
            out.append(line)
        elif out[-1:] != ['> […]']:
            out.append('> […]')
    return '\n'.join(out)


def trim_quoted_history(text, subject='', people=''):
    """Each reply quotes the whole thread below it, and the earlier messages are their own
    signals. Keep the new text whole and only the start of the quoted history."""
    new, history = split_quoted_history(text, subject, people)
    new = _runs_cut(new, subject, people)
    if len(new) > BODY_KEPT - QUOTED_HISTORY_KEPT:
        new = _fit(new, subject, people)
    if not history:
        return new if len(new) < len(text) else text, 0
    kept = history[:QUOTED_HISTORY_KEPT]
    return (new + f'\n\n[Quoted earlier messages: first {len(kept):,} of {len(history):,} characters kept. '
            'Earlier messages in this thread are separate signals.]\n' + kept), len(history)


# The line trim_quoted_history puts between a reply and its quoted history. It tells the model the earlier messages are
# separate signals; people never see it (shown_body).
QUOTED_MARK = re.compile(r'(?<!\n)\n*\[Quoted earlier messages(?::[^\]\n]*)?\]\n?')


# What a review and the checks that close read of a mail whose text can't be read (its body is stored empty, with why in
# `unreadable`): it says something, and nobody here knows what. Never stored and never shown: people see one line
# (message_view.shape_email), and it is no one's own words.
UNREADABLE = {reason: f"[The text of this mail couldn't be read: {why}. It may say anything: conclude nothing from it.]" for reason, why in (
    ('encrypted', 'it is encrypted'), ('signed', 'it is signed in a form that has to be opened first'),
    ('winmail', 'Outlook put it in a file, winmail.dat'))}


def shown_body(text):
    """A stored body as people read it: (text, clipped). The quoted-history marker is left out, the history under it
    kept; clipped when the marker says part of that history was cut."""
    text = str(text or '')
    match = QUOTED_MARK.search(text)
    if not match:
        return text, False
    counts = re.search(r'first ([\d,]+) of ([\d,]+)', match[0])
    clipped = bool(counts) and int(counts[1].replace(',', '')) < int(counts[2].replace(',', ''))
    before, after = text[:match.start()].rstrip(), text[match.end():].lstrip('\n')
    return (before + '\n\n' + after if before and after else before or after), clipped


def same_text(one, other):
    """Whether two stored bodies are the same mail's text, only split differently into new words and kept history: the
    same characters (a quote's marks and white space aside), up to where one's history was cut, out of about as many."""
    def read(text):
        shown, clipped = shown_body(str(text or '').replace('\r', ''))
        found = QUOTED_MARK.search(str(text or ''))
        count = re.search(r'of ([\d,]+) characters', found[0]) if found else None
        total = len(str(text)[:found.start()].rstrip()) + int(count[1].replace(',', '')) if count else len(str(text or '').strip())
        return re.sub(r'[\s>]+', '', shown), clipped, total
    (a, a_cut, a_all), (b, b_cut, b_all) = read(one), read(other)
    if a == b and not a_cut and not b_cut:
        return True
    return (a_cut and b.startswith(a) or b_cut and a.startswith(b)) and abs(a_all - b_all) <= max(a_all, b_all) // 4


def _marked(text, subject='', people=''):
    """A mail's lines, as collected or as stored, and which are quoted. Under the stored marker all is, except what the
    sender wrote between marked lines (mail stored before those answers stayed above it)."""
    found = QUOTED_MARK.search(text)
    above = text[:found.start()].rstrip().split('\n') if found else text.split('\n')
    under = ['', *text[found.end():].lstrip('\n').split('\n')] if found else []
    lines = [x.rstrip() for x in (above if any(x.strip() for x in above) else []) + under]
    marks, cut = quoted(lines, subject, people), len(lines) - len(under)
    if under and not marks[cut + 1]:
        marks[cut:] = [True] * len(under)
    return lines, marks


def unquoted(text, subject='', people=''):
    """What someone wrote themselves in an email, stored or as it came: its lines that quote no one, also the answers
    between quoted lines. A forward keeps its lines: they are what it sends."""
    lines, marks = _marked(str(text or '').replace('\r', ''), subject, people)
    own = [x for x, m in zip(lines, marks) if not m]
    if not any(own) and not PREFIX.match(subject or ''):  # nothing of its own, and no answer: what isn't marked as quoted
        own = [x for x in lines if not x.lstrip().startswith('>')]
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(own)).strip()


def without_forward(text):
    """What someone wrote themselves above a mail they send on: in a forward that mail's text is its own sender's."""
    lines = text.split('\n')
    return '\n'.join(lines[:sent_on(lines)]).strip()


def quoted_history(text, subject='', people=''):
    """A stored mail from its first quoted line on, for its fold under the sender's own words; '' when it quotes none."""
    lines, marks = _marked(str(text or '').replace('\r', ''), subject, people)
    if True not in marks or not any(x and not m for x, m in zip(lines, marks)):
        return ''
    return '\n'.join(lines[marks.index(True):]).strip()


def own_part(text, subject='', people=''):
    """unquoted(), without the signature under "-- "."""
    text = unquoted(text, subject, people)
    return text if FORWARD_SUBJECT.match(subject or '') else re.split(r'\n--\n', text, maxsplit=1)[0].strip()


# Zero-width and filler characters newsletters use to pad preview text.
INVISIBLE = re.compile('[\u200b-\u200f\u2060\u034f\u00ad\ufeff\u2007\u180e]')


def visible_text(text):
    text = INVISIBLE.sub('', text)
    return re.sub(r'[ \t]+\n', '\n', re.sub(r'[ \t]{2,}', ' ', re.sub(r'\n{3,}', '\n\n', text)))


# A quote from a message, compared the way a person reads it (quoted_in): Unicode compatibility forms folded (NFKC:
# full-width letters, ligatures, no-break spaces), case ignored, every quote mark and apostrophe read as ' and every
# dash as -, zero-width characters dropped and a run of whitespace as one space. Words are never translated: a quote
# from a message in Dutch is Dutch.
QUOTE_FOLD = {**dict.fromkeys('"‘’‚‛“”„‟′″‵´`ʹʺʻ'
                              'ʼʽ‹›«»〝〞〟', "'"),
              **dict.fromkeys('‐‑‒–—―⁃−⸺⸻﹘', '-')}
QUOTE_SKIP = set('​‌‍‎‏⁠­﻿͏')
QUOTE_EDGE = " '.,;:!?"  # a quote's own marks and end punctuation, around the words that count
QUOTE_MIN = 8  # characters a quote has at least, unless it is the whole message
QUOTE_MAX = 300


def _quote_folded(text):
    """(text in NFC, [(folded character, its index in that text)])."""
    base, out = unicodedata.normalize('NFC', str(text or '')), []
    for i, c in enumerate(base):
        if c in QUOTE_SKIP:
            continue
        for d in unicodedata.normalize('NFKC', unicodedata.normalize('NFKC', c).casefold()):
            d = QUOTE_FOLD.get(d, d)
            if d.isspace():
                if out and out[-1][0] != ' ':
                    out.append((' ', i))
            else:
                out.append((d, i))
    return base, out


def quoted_in(quote, message):
    """The stretch of message that quote is (folded as above, its own quote marks and end punctuation left out), in the
    message's own characters with whitespace as single spaces; None when the message doesn't say it, or the quote is
    too short (QUOTE_MIN, unless it is the whole message) or too long (QUOTE_MAX)."""
    if not isinstance(quote, str) or not isinstance(message, str):
        return None
    folded = _quote_folded(quote)[1]
    start, end = 0, len(folded)
    while start < end and folded[start][0] in QUOTE_EDGE:
        start += 1
    while end > start and folded[end - 1][0] in QUOTE_EDGE:
        end -= 1
    key = ''.join(c for c, _ in folded[start:end])
    if not key or len(key) > QUOTE_MAX:
        return None
    base, said = _quote_folded(message)
    words = ''.join(c for c, _ in said)
    at = words.find(key)
    if at < 0 or (len(key) < QUOTE_MIN and words.strip(QUOTE_EDGE) != key):
        return None
    return ' '.join(base[said[at][1]:said[at + len(key) - 1][1] + 1].split())


def email_body(plain, html_parts, subject='', people=''):
    """Prefer the text part, unless it is empty, only points to the HTML version, or is a
    token stub (like "empty") while the HTML has the real message."""
    plain = visible_text(plain)
    rendered = visible_text('\n'.join(x for x in (mail_html(v, subject, people) for v in html_parts) if x))
    stub = len(plain.strip()) < 40 and len(rendered.strip()) > 200
    if not stub and len(plain.strip()) < 500 and len(rendered) > 3 * len(plain):  # "Your program can't show this mail"
        said = set(_words(plain).split())
        stub = len(said - set(_words(rendered).split())) * 2 > len(said)
    placeholder = len(plain.strip()) < 500 and PLAIN_PLACEHOLDER.search(plain)  # a booking's "sent in HTML" note runs a few lines
    # a program whose text part leaves out where a link to a Google file goes (Apple Mail): the HTML has it
    lost = {f for v in html_parts[:10] for _, f, _ in google_links.find(v)} if rendered.strip() else ()
    if lost:
        said = {f for _, f, _ in google_links.find(plain)}
        shown = {f for _, f, _ in google_links.find(rendered)}
        lost = [f for f in lost if f in shown and not any(f.startswith(s) for s in said)]
    if plain.strip() and not stub and not placeholder and not lost:
        return plain
    return rendered if rendered.strip() else plain


def _part_text(part):
    """(kind, text) of a message's own text part, or None: files and attached messages are not its body."""
    kind = str(part.get('mimeType') or '').lower()
    data = (part.get('body') or {}).get('data')
    if kind not in ('text/plain', 'text/html') or part.get('filename') or not data:
        return None
    disposition = next((str(h.get('value', '')) for h in part.get('headers') or () if isinstance(h, dict)
                        and str(h.get('name', '')).lower() == 'content-disposition'), '')
    if disposition.strip().lower().startswith('attachment'):
        return None
    return kind, base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)).decode('utf-8', errors='replace')


def _attached(part):
    """A message attached to this one (a forwarded .eml): its text is its own. A bounce's delivery status is part of it."""
    return str(part.get('mimeType') or '').lower() in ('message/rfc822', 'message/global')


def _attached_messages(part):
    """The messages attached to one, not those inside them."""
    if _attached(part):
        return [part]
    return [x for child in part.get('parts') or () for x in _attached_messages(child)]


def _header_value(part, name):
    return next((' '.join(str(h.get('value') or '').split()) for h in part.get('headers') or () if isinstance(h, dict)
                 and str(h.get('name') or '').lower() == name.lower()), '')


def body_parts(payload):
    """A message's own text as [(plain, [html])], in order: the versions of one text (multipart/alternative) together,
    every other part by itself, so a mailing list's plain footer never stands in for an HTML mail."""
    out = []

    def leaves(part):
        if _attached(part):
            return
        found = _part_text(part)
        if found:
            yield found
        for child in part.get('parts') or ():
            yield from leaves(child)

    def one(found):
        found = list(found)
        if found:
            out.append(('\n'.join(t for k, t in found if k == 'text/plain'), [t for k, t in found if k == 'text/html']))

    def walk(part):
        if _attached(part):
            return
        kind, children = str(part.get('mimeType') or '').lower(), part.get('parts') or ()
        if kind == 'multipart/alternative' or children and not kind:
            one(leaves(part))
        elif children:
            for child in children:
                walk(child)
        else:
            one(leaves(part))

    walk(payload or {})
    return out


def message_body(payload, subject='', people=''):
    """A message's own text: each part's plain version or its HTML (email_body). A part that repeats another one's words
    (a sender that puts both versions side by side) is left out. With no text of its own, the messages attached to it
    are what it sends, each under its own header, as a forward in the text has them."""
    parts = [(p, h, email_body(p, h, subject, people)) for p, h in body_parts(payload)]
    said = [_words(google_links.ADDED.sub('', text)) for _, _, text in parts]
    kept = []
    for n, (_, html_parts, text) in enumerate(parts):
        others = [s for k, s in enumerate(said) if k != n and bool(parts[k][1]) != bool(html_parts) and len(s) > 40]
        if html_parts:  # its plain version is there too, with most of it
            twice = any(said[n] and said[n] in s or s in said[n] and len(s) * 2 >= len(said[n]) for s in others)
        else:
            twice = len(said[n]) > 40 and any(said[n] in s and len(said[n]) * 2 < len(s) for s in others)
        if said[n] and not twice:
            kept.append(text)
    if not kept:
        for part in _attached_messages(payload or {}):
            inner = (part.get('parts') or [part])[0]
            text = message_body(inner, _header_value(inner, 'subject'))
            if text.strip():
                names = [f'{name}: {value}' for name in ('From', 'Date', 'Subject', 'To') if (value := _header_value(inner, name))]
                kept.append('\n'.join(['---------- Forwarded message ---------', *names, '', text]))
    return '\n'.join(kept)


ATTACHMENT_INLINE = {'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/webp'}


def message_attachments(payload):
    """Real attachments of a Gmail message, without embedded signature/logo images. A message attached to it too, named
    by its subject when it has no name, and the files in it."""
    found = []
    def walk(part):
        body, name = part.get('body') or {}, part.get('filename')
        if not name and _attached(part) and part.get('parts'):
            name = (_header_value(part['parts'][0], 'subject') or 'message') + '.eml'
        if name and (body.get('attachmentId') or body.get('data')):
            headers = {h['name'].lower(): h.get('value', '') for h in part.get('headers', [])}
            embedded = (headers.get('content-id') and part.get('mimeType', '').startswith('image/')
                        and not headers.get('content-disposition', '').lower().startswith('attachment'))
            if not embedded:
                found.append({'part': str(part.get('partId', '')), 'name': name[:200],
                              'mime': part.get('mimeType', 'application/octet-stream')[:100], 'size': int(body.get('size') or 0)})
        for child in part.get('parts', []):
            walk(child)
    walk(payload or {})
    return found[:20]


def message_images(payload):
    """Embedded images by Content-ID, so an HTML email can show them: {cid: partId}."""
    found = {}
    def walk(part):
        body = part.get('body') or {}
        headers = {h['name'].lower(): h.get('value', '') for h in part.get('headers', [])}
        cid = headers.get('content-id', '').strip().strip('<>')
        if cid and part.get('mimeType') in ATTACHMENT_INLINE - {'application/pdf'} and (body.get('attachmentId') or body.get('data')):
            found[cid[:300]] = str(part.get('partId', ''))
        for child in part.get('parts', []):
            walk(child)
    walk(payload or {})
    return dict(list(found.items())[:50])


def message_html(payload):
    """The message's own HTML body (not an attached .html file), or ''."""
    def walk(part):
        if _attached(part):
            return ''
        if part.get('mimeType') == 'text/html' and not part.get('filename') and (part.get('body') or {}).get('data'):
            data = part['body']['data']
            return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)).decode('utf-8', errors='replace')
        for child in part.get('parts', []):
            found = walk(child)
            if found:
                return found
        return ''
    return walk(payload or {})[:1_000_000]


COPY_MAGIC = b'MC1COPY\x00'


COPY_CHUNK = 1 << 20


def _copy_keys(key):
    derive = lambda name: hashlib.blake2b(key=key, person=name, digest_size=32).digest()
    return derive(b'mc1-copy-seal'), derive(b'mc1-copy-mac')


def _copy_tag(mac, index, nonce, sealed):
    return hashlib.blake2b(index.to_bytes(8, 'big') + len(sealed).to_bytes(4, 'big') + nonce + sealed, key=mac, digest_size=16).digest()


def _xor(data, stream):
    return (int.from_bytes(data, 'little') ^ int.from_bytes(stream, 'little')).to_bytes(len(data), 'little')


def seal_copy(database, target, key):
    """An encrypted copy of a SQLite database, as message_seal seals a value (SHAKE256 keystream, BLAKE2b MAC) in
    chunks of 1 MB, with keys derived from the message key. The consistent copy SQLite's backup makes on the way only
    exists in the same private folder as the target, and is overwritten before it is removed."""
    target = Path(target)
    plain = target.with_name(target.name + '.tmp')
    enc, mac = _copy_keys(key)
    try:
        with contextlib.closing(sqlite3.connect(database, timeout=60)) as source, contextlib.closing(sqlite3.connect(plain)) as copy:
            source.backup(copy)
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with open(plain, 'rb') as source, os.fdopen(fd, 'wb') as out:
            out.write(COPY_MAGIC)
            index = 0
            while chunk := source.read(COPY_CHUNK):
                nonce = os.urandom(16)
                sealed = _xor(chunk, hashlib.shake_256(enc + nonce).digest(len(chunk)))
                out.write(len(chunk).to_bytes(4, 'big') + nonce + sealed + _copy_tag(mac, index, nonce, sealed))
                index += 1
            out.write((0).to_bytes(4, 'big') + _copy_tag(mac, index, b'', b''))  # the end: a cut-off copy does not open
            out.flush()
            os.fsync(out.fileno())
    finally:
        portable.shred(plain)


def open_copy(source, target, key):
    """The database back from seal_copy, written to target (600); SealError when the key or the copy is wrong."""
    enc, mac = _copy_keys(key)
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with open(source, 'rb') as copy, os.fdopen(fd, 'wb') as out:
        if copy.read(len(COPY_MAGIC)) != COPY_MAGIC:
            raise message_seal.SealError(f'{source} is not an encrypted database copy')
        index = 0
        while True:
            size = int.from_bytes(copy.read(4) or b'\xff' * 4, 'big')
            if size == 0:
                if not hmac.compare_digest(copy.read(16), _copy_tag(mac, index, b'', b'')):
                    raise message_seal.SealError(f'{source} did not open: wrong key or a damaged copy')
                break
            if size > COPY_CHUNK:
                raise message_seal.SealError(f'{source} is cut off or damaged')
            nonce, sealed, tag = copy.read(16), copy.read(size), copy.read(16)
            if len(sealed) != size or not hmac.compare_digest(tag, _copy_tag(mac, index, nonce, sealed)):
                raise message_seal.SealError(f'{source} did not open: wrong key or a damaged copy')
            out.write(_xor(sealed, hashlib.shake_256(enc + nonce).digest(size)))
            index += 1
        out.flush()
        os.fsync(out.fileno())


def first_sentence(text):
    """The first sentence of a card's body, plain: an already_done result leads with what shows it."""
    text = ' '.join(re.sub(r'[*_`\[\]]|\(https?://[^)]*\)', '', str(text or '')).split())
    return re.split(r'(?<=[.!?])\s', text, maxsplit=1)[0][:200]


def no_you(reason):
    """A review's reason, as a line under the to-do shows it: never with "You" as its subject ("Explained that…", not
    "You explained that…"). A leading "You " goes and the next word takes the capital; "You and Sam…" stays as it is."""
    found = re.match(r'you\s+(?!and\b)(\w)(.*)', str(reason or ''), re.I | re.S)
    return found.group(1).upper() + found.group(2) if found else reason


def body_after_title(title, body):
    """What a to-do's body says beyond its title: '' when it only repeats the title (New to-do's own words), the rest
    when its first line or sentence is the title (Talk's title, then a note), else all of it. Case, spacing and
    punctuation don't count; a title cut short (…) keeps the whole body, which says it in full. The dashboard reads
    bodies by the same rule (todos-cards.js bodyAfterTitle), so ones stored before it show clean too."""
    head, text = str(title or '').strip(), str(body or '')
    t, b = list(re.finditer(r'[^\W_]+', head)), list(re.finditer(r'[^\W_]+', text))
    n = len(t)
    if not n or len(b) < n or any(x.group().lower() != y.group().lower() for x, y in zip(t, b)):
        return text
    if len(b) == n:
        return ''
    end = b[n - 1].end()
    if head.endswith('…') or not re.search(r'[\n.!?:;…]', head[-1] + text[end:b[n].start()]):
        return text
    return re.sub(r'^[\s.!?:;,…–—-]+', '', text[end:])


def _words(text):
    return ' '.join(re.findall(r'[^\W_]+', str(text or '').casefold()))


def fold_previews(rows):
    """Search results without the phone's previews of what is there in full: a notification whose text a message in
    the results already has (the chat or mail it previews), or that repeats an earlier preview word for word, goes.
    A preview of something the Machine has nothing else of stays where it ranked."""
    full = [_words(f"{r.get('title') or ''} {r.get('body') or ''}") for r in rows if r.get('kind') != 'android.notification']
    seen, out = set(), []
    for r in rows:
        if r.get('kind') == 'android.notification':
            said = _words(r.get('body') or r.get('title'))
            if said and (said in seen or (len(said) >= 12 and any(said in text for text in full))):
                continue
            seen.add(said)
        out.append(r)
    return out


def intercom_note(part_type):
    """Whether a part is an internal note the customer never sees (note, note_and_reopen, note_and_unsnooze, …_note)."""
    return bool(re.search(r'(?:^|_)note(?:_|$)', part_type))

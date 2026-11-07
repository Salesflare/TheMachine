"""Message text: a mail's own words without the quoted history under them, its body from the plain and HTML parts
(plain_html), its attachments and inline images, invisible characters, the compact JSON the app stores (encoded), a
value cut to size (clamp), the first address in a header (_address), and an encrypted copy of a database (seal_copy,
open_copy). Moved out of assistant.py as is."""
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

import message_seal
import portable


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


def _address(value):
    found = re.findall(r'[^\s<>"\',;]+@[^\s<>"\',;]+', str(value or ''))
    return found[0].lower() if found else ''


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


# Where an email reply's quoted history starts: a top-level reply header such as
# "On Thu, 8 Oct 2026, Ann <a@b.c> wrote:" (often wrapped over two or three lines,
# in several languages) or an Outlook "Original Message"/"From: … Sent:" block.
REPLY_HEADER = re.compile(
    r'^(?:On|Le|Op|Am|El|Il|Den|Em)\b[^\n]{0,250}(?:\r?\n(?!>)[^\n]{0,250}){0,2}?'
    r'\s(?:wrote|a\s+écrit|schreef|schrieb|escribió|ha\s+scritto|skrev|escreveu)\b[^\n]{0,200}?(?:\r?\n(?!>)[^\n]{0,200}?)?:[ \t]*\r?$'
    r'|^-{2,}\s*Original Message\s*-{2,}[ \t]*\r?$'
    r'|^From:[ \t]\S[^\n]*\r?\nSent:[ \t]', re.M | re.I)


FORWARD_SUBJECT = re.compile(r'(?i)^\s*(?:fwd?|tr|wg|doorst)\s*:')


QUOTED_HISTORY_KEPT = 3000


# Text parts that only tell the reader to open the HTML version.
PLAIN_PLACEHOLDER = re.compile(r'(?i)plain[- ]text version (?:is )?not available|requires an? html|'
                               r'view (?:this|the) (?:email|message) in (?:a|your) (?:web )?browser|use an html[- ]capable')


def split_quoted_history(text, subject=''):
    """Return (new text, quoted history). Forwarded messages are kept whole: they are the content."""
    if FORWARD_SUBJECT.match(subject or ''):
        return text, ''
    match = REPLY_HEADER.search(text)
    if not match or not text[:match.start()].strip():
        return text, ''
    return text[:match.start()].rstrip(), text[match.start():]


def trim_quoted_history(text, subject=''):
    """Each reply quotes the whole thread below it, and the earlier messages are their own
    signals. Keep the new text whole and only the start of the quoted history."""
    new, quoted = split_quoted_history(text, subject)
    if not quoted:
        return text, 0
    kept = quoted[:QUOTED_HISTORY_KEPT]
    return (new + f'\n\n[Quoted earlier messages: first {len(kept):,} of {len(quoted):,} characters kept. '
            'Earlier messages in this thread are separate signals.]\n' + kept), len(quoted)


# The line trim_quoted_history puts between a reply and its quoted history. It tells the model the earlier messages are
# separate signals; people never see it (shown_body).
QUOTED_MARK = re.compile(r'\n*\[Quoted earlier messages(?::[^\]\n]*)?\]\n?')


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


# Zero-width and filler characters newsletters use to pad preview text.
INVISIBLE = re.compile('[\u200b-\u200f\u2060\u034f\u00ad\ufeff\u2007\u180e]')


def visible_text(text):
    text = INVISIBLE.sub('', text)
    return re.sub(r'[ \t]+\n', '\n', re.sub(r'[ \t]{2,}', ' ', re.sub(r'\n{3,}', '\n\n', text)))


def email_body(plain, html_parts):
    """Prefer the text part, unless it is empty, only points to the HTML version, or is a
    token stub (like "empty") while the HTML has the real message."""
    plain = visible_text(plain)
    rendered = visible_text(plain_html('\n'.join(html_parts))) if html_parts else ''
    stub = len(plain.strip()) < 40 and len(rendered.strip()) > 200
    placeholder = len(plain.strip()) < 300 and PLAIN_PLACEHOLDER.search(plain)
    if plain.strip() and not stub and not placeholder:
        return plain
    return rendered if rendered.strip() else plain


ATTACHMENT_INLINE = {'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/webp'}


def message_attachments(payload):
    """Real attachments of a Gmail message, without embedded signature/logo images."""
    found = []
    def walk(part):
        body = part.get('body') or {}
        if part.get('filename') and (body.get('attachmentId') or body.get('data')):
            headers = {h['name'].lower(): h.get('value', '') for h in part.get('headers', [])}
            embedded = (headers.get('content-id') and part.get('mimeType', '').startswith('image/')
                        and not headers.get('content-disposition', '').lower().startswith('attachment'))
            if not embedded:
                found.append({'part': str(part.get('partId', '')), 'name': part['filename'][:200],
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

"""Email signatures per mail account, as HTML: imported from the mailbox (Gmail's sendAs signature; for Outlook, which has
no signature API, found in the owner's own sent mail) or set on the dashboard (Settings, Signatures). For Gmail a set
one overrides the sendAs signature, which is read fresh at every send; empty means Gmail's own.

Kept in signatures.json next to the database (state, not a secret):
    {"<account id>": {"html": "<div>Alex Smith<br>Acme</div>", "source": "imported" | "detected" | "owner", "updated_at": "..."}}
An owner's own entry is never replaced by an imported or detected one. Every signature is cleaned to a small set of tags and
attributes before it is stored, shown or sent: no scripts, event handlers, frames, forms or remote styles."""
from __future__ import annotations

import datetime as dt
import portable
import html
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

MAX_HTML = 20000
MAX_PASTED = 60000  # what the owner may send to be cleaned (the dashboard's own check is the same)
TAGS = {'a', 'b', 'strong', 'i', 'em', 'u', 'br', 'p', 'div', 'span', 'font', 'small', 'big', 'sub', 'sup', 'hr', 'img',
        'table', 'thead', 'tbody', 'tr', 'td', 'th', 'ul', 'ol', 'li', 'blockquote', 'center', 'h1', 'h2', 'h3', 'h4'}
VOID = {'br', 'hr', 'img', 'meta', 'link', 'base', 'input', 'embed'}
DROP = {'script', 'style', 'iframe', 'object', 'embed', 'form', 'input', 'button', 'textarea', 'select', 'svg', 'math',
        'template', 'noscript', 'head', 'title', 'meta', 'link', 'base'}  # removed with everything inside them
ATTRS = {'href', 'src', 'alt', 'title', 'width', 'height', 'style', 'color', 'face', 'size', 'align', 'valign', 'border',
         'cellpadding', 'cellspacing', 'colspan', 'rowspan', 'bgcolor', 'dir'}
STYLE_BAD = re.compile(r'expression|url\s*\(|@import|behavio(u)?r|javascript:|-moz-binding', re.I)


class _Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.open, self.dropping = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP:
            self.dropping += tag not in VOID
            return
        if self.dropping or tag not in TAGS:
            return
        kept = []
        for name, value in attrs:
            value = value or ''
            if name not in ATTRS:
                continue  # on* handlers, class, id and the rest
            if name == 'href' and not re.match(r'(https?:|mailto:|tel:)', value.strip(), re.I):
                continue
            if name == 'src' and not re.match(r'(https:|cid:|data:image/(png|gif|jpe?g|webp);base64,)', value.strip(), re.I):
                continue
            if name == 'style' and STYLE_BAD.search(value):
                continue
            kept.append(f' {name}="{html.escape(value, quote=True)}"')
        self.out.append(f'<{tag}{"".join(kept)}>')
        if tag not in VOID:
            self.open.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in DROP and tag not in VOID:
            self.handle_endtag(tag)
        elif tag not in VOID and self.open and self.open[-1] == tag:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in DROP:
            if tag not in VOID:
                self.dropping = max(0, self.dropping - 1)
            return
        if self.dropping or tag not in self.open:
            return
        while self.open:
            last = self.open.pop()
            self.out.append(f'</{last}>')
            if last == tag:
                break

    def handle_data(self, data):
        if not self.dropping:
            self.out.append(html.escape(data, quote=False))


def clean(value, read=MAX_HTML * 2, keep=MAX_HTML):
    """Only harmless formatting, links (http, https, mailto, tel) and images (https, cid or inline data); `read`: how
    much of the value is read at most, `keep`: how much of what is left is kept (None: all, to measure it)."""
    parser = _Cleaner()
    parser.feed(str(value or '')[:read])
    parser.close()
    out = ''.join(parser.out) + ''.join(f'</{t}>' for t in reversed(parser.open))
    return out.strip()[:keep]


def text(value):
    """What a signature says, for comparing and for "is there anything in it"."""
    plain = re.sub(r'<(br|/p|/div|/tr|/li)[^>]*>', '\n', str(value or ''), flags=re.I)
    plain = html.unescape(re.sub(r'<[^>]+>', ' ', plain))
    return '\n'.join(' '.join(line.split()) for line in plain.split('\n') if line.strip())


# ------------------------------------------------------------------------------------------- detection

QUOTE_MARKS = re.compile(r'<div[^>]*id="?(appendonsend|divRplyFwdMsg|mail-editor-reference-message-container)"?|<div[^>]*class="?gmail_quote'
                         r'|<blockquote|<hr[^>]*>\s*(<div[^>]*>\s*)*<font[^>]*>\s*<b>\s*(From|Van|De|Von|Da)\s*:', re.I)
BLOCK = re.compile(r'(?=<(?:div|p|table|tr|hr)\b)|(?<=<br>)|(?<=<br/>)|(?<=<br />)', re.I)


def new_part(body):
    """A sent message without the conversation it quotes."""
    found = QUOTE_MARKS.search(body or '')
    return (body or '')[:found.start()] if found else (body or '')


def _body(body):
    found = re.search(r'<body[^>]*>(.*)</body>', body or '', re.I | re.S)
    return found.group(1) if found else (body or '')


def _blocks(body):
    return [b for b in BLOCK.split(clean(_body(new_part(body)))) if b.strip()]


MARKED = re.compile(r'<div[^>]*\bid="?(x_)?Signature"?[^>]*>', re.I)


def _marked(body):
    """What Outlook itself put in its signature container (<div id="Signature">), or None."""
    found = MARKED.search(body or '')
    if not found:
        return None
    depth, at = 1, found.end()
    for tag in re.finditer(r'<(/?)div\b[^>]*>', body[at:], re.I):
        depth += -1 if tag.group(1) else 1
        if not depth:
            return body[at:at + tag.start()]
    return None


def detect(bodies, names=(), least=3):
    """The signature the owner's sent messages end with, kept only when at least `least` of them share it word for
    word: Outlook's own signature container when it has one, else the longest shared trailing run of blocks, without
    a closing line ("Cheers,") or the owner's first name before it (the draft already ends with those). '' when
    nothing repeats: better no signature than a wrong one."""
    if isinstance(names, str):
        names = (names,)
    names = {n.strip().lower() for n in names if n and n.strip()}
    bodies = [b for b in bodies if b]
    marked = {}
    for body in bodies:
        inner = _marked(_body(new_part(body)))
        if inner is not None and text(clean(inner)).strip():
            marked.setdefault(text(clean(inner)), []).append(clean(inner))
    common = max(marked.values(), key=len, default=[])
    if len(common) >= least:
        return common[0]
    found = [_blocks(b) for b in bodies]
    best = ''
    for size in range(1, 41):
        counts = {}
        for blocks in found:
            if len(blocks) < size:
                continue
            tail = blocks[-size:]
            key = '\n'.join(text(b) for b in tail)
            if key.strip():
                counts.setdefault(key, []).append(tail)
        shared = [tails for tails in counts.values() if len(tails) >= least]
        if not shared:
            break
        tail = max(shared, key=len)[0]
        while tail and _lead(text(tail[0]), names):
            tail = tail[1:]
        if tail and len(text(''.join(tail))) <= 1500:
            best = ''.join(tail)
    return clean(best)


def _lead(line, names):
    """Space, a closing line ending in a comma, or the owner's first name: what comes before a signature."""
    line = line.strip()
    return not line or line.strip(' .-').lower() in names or (len(line) <= 30 and line.endswith(',') and '\n' not in line)


# ------------------------------------------------------------------------------------------- storage

def path(config):
    database = config.get('database')
    return Path(database).expanduser().parent / 'signatures.json' if database else None


def load(config):
    where = path(config)
    try:
        value = json.loads(where.read_text()) if where else {}
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def get(config, account_id):
    """The stored entry for this account ({'html', 'source', 'updated_at'}), or None."""
    entry = load(config).get(account_id)
    return entry if isinstance(entry, dict) and isinstance(entry.get('html'), str) else None


def save(config, account_id, value, source):
    """Store a cleaned signature; one read from the mailbox (imported or detected) never replaces the owner's own.
    Returns the stored entry."""
    where = path(config)
    if not where:
        raise ValueError('Signatures can only be saved with a database path in config.json')
    where.parent.mkdir(parents=True, exist_ok=True)
    with open(where.with_name(where.name + '.lock'), 'w') as lock:
        portable.lock(lock)
        current = load(config)
        if source != 'owner' and (current.get(account_id) or {}).get('source') == 'owner':
            return current[account_id]
        current[account_id] = {'html': clean(value, MAX_PASTED if source == 'owner' else MAX_HTML * 2), 'source': source,
                               'updated_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}
        temp = where.with_name(where.name + '.tmp')
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as handle:
            json.dump(current, handle, indent=2)
        os.replace(temp, where)
        return current[account_id]


def remove(config, account_id):
    """Forget the signature kept for this account (the owner's own included): the mailbox's own applies again."""
    where = path(config)
    if not where or not where.exists():
        return
    with open(where.with_name(where.name + '.lock'), 'w') as lock:
        portable.lock(lock)
        current = load(config)
        if current.pop(account_id, None) is None:
            return
        temp = where.with_name(where.name + '.tmp')
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as handle:
            json.dump(current, handle, indent=2)
        os.replace(temp, where)

"""What the checks that close to-dos and promises by themselves (handled_check.py, promise_checks.py) read of each later
message: the sender's own words, whole up to WORDS characters, else their start and their end with a mark between that
says it is cut, and the files it came with, by name."""
import json

from machine import kinds
from machine.sources.slack import slack_ids_named
from machine.store import message_view
from machine.text import own_part

# Mail the owner writes fits almost always, chats always; the longest are conversations whose newest part is at the end
WORDS = 1500
# What the judge is told about a page of these
RULE = ('A message marked cut shows only its start and its end: when what you see does not itself settle it, it is open. '
        '"files" names the files that came with a message, "no files" says none did (a picture inside the text is not '
        'counted): saying something is attached without a file delivers nothing, and a file that is the thing asked for '
        'delivers it, however little the message says. With neither, files are not recorded there: go by its words.')


def cut(text, limit=WORDS):
    """The text on one line; past the limit its start and its end, with how much is left out between."""
    text = ' '.join(str(text or '').split())
    if len(text) <= limit:
        return text
    half = limit // 2
    return f'{text[:half]} […cut: {len(text) - 2 * half:,} characters left out…] {text[-half:]}'


def words(kind, meta, title, body):
    """A message's own words: an email's subject and its new part, any other message's text (a Slack title's
    repeat of its first line is left out: graph.slack_title)."""
    title, body = str(title or ''), str(body or '')
    if kinds.KINDS.get(kind, {}).get('family') == kinds.MAIL:
        return f'{title} — {own_part(body, title)}'
    body = message_view.intercom_body(kind, meta, body)
    if kind == 'slack.message' and body.strip():
        title = title.split(': ', 1)[0]
    return f'{title} — {body}'


def files(kind, meta, body=''):
    """The files a message came with, by name (a chat that keeps no names: what it sent, like "document"); [] when it
    had none; None when its source doesn't keep them, so nobody can tell."""
    if kind == 'gmail.message':
        kept = meta.get('attachments')
        return [str(a.get('name') or 'file') for a in kept if isinstance(a, dict)] if isinstance(kept, list) else None
    if kind in message_view.MEDIA_KINDS and 'media_type' in meta:
        sent = str(meta['media_type'] or '').replace('_', ' ')
        return None if sent == 'other' else [sent] if sent else []  # other: Telegram's link previews, mostly
    if kind == 'teams.message':
        found = [line[len('[file] '):] for line in str(body or '').split('\n') if line.startswith('[file] ')]
        return found or (None if meta.get('truncated') else [])
    return None


def judged(db, ids):
    """{event id: its words, and its files when known} for a page the model judges, message text as data."""
    out = {}
    for r in db.execute(f"SELECT id,title,body,kind,metadata FROM events WHERE id IN ({','.join('?' * len(ids))})", list(ids)):
        meta = json.loads(r['metadata'] or '{}')
        found = files(r['kind'], meta, r['body'])
        named = '' if found is None else ', no files' if not found else f", files: <<<{', '.join(' '.join(n.split())[:120] for n in found[:10])}>>>"
        out[r['id']] = f"<<<{cut(slack_ids_named(db, words(r['kind'], meta, r['title'], r['body'])))}>>>{named}"
    return out

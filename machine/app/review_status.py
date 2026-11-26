"""A signal review's status, lighter and read once (the review prompt's LIGHT_STATUS_RULE says how to read it).

A review reads status first, to judge every signal against the open and done to-dos. compact_status gives each open
to-do its first 400 characters, and a long list ran past OpenClaw's tool-result cut, while the review resent that
status with each of its model steps. For a signal review (the plugin passes its session as _review_session) status
now gives:
- light: every open to-do by its title and the start of its body (body_start), every done one as a line with its id,
  title and day closed; kept under REVIEW_PAGE_CHARS (fit), the done lines first to go.
- here: the open to-dos that share a mail thread, a chat or a sender with the batch, with their first 400 characters,
  in the claim's reply (open_todos_here), where the review needs them whole.
- read_once: a second status in the same review gives only the to-dos new or changed since the review read it, as
  RunReads does for a to-do's own run (prep_reads.py); again:true reads it whole.
The CLI, the dashboard, chats and a to-do's run keep compact_status."""
import hashlib
import json
import re

from machine.store.review import REVIEW_PAGE_CHARS, REVIEW_SESSION_PREFIX
from machine.text import clamp, encoded

BODY_START = 120   # characters of an open to-do's body in the light status
HERE_MAX, HERE_CHARS = 10, 7000  # open_todos_here: to-dos and characters at most
HERE_EVIDENCE = 20  # of a to-do's evidence, the messages its thread, chat and sender are read from
CHAT_KEYS = {'slack.message': 'channel_id', 'whatsapp.message': 'chat_id', 'teams.message': 'chat_id', 'telegram.message': 'chat_id',
             'signal.message': 'chat_id', 'linkedin.message': 'conversation_id'}

NOTE = ('suggestions: the open to-dos, body_start is only the beginning; done: id, title (day closed). status with suggestion_id '
        'gives one in full; events and related read signals.')
AGAIN = ('Read earlier in this review, so left out: {n} to-dos as you read them. Shown: only the ones new or changed since. '
         'Only when the list is no longer in front of you, read it whole with again:true.')
LEFT = 'Left out to stay whole: {done} done to-dos (the oldest) and the body_start of {short} open ones (the oldest).'


def is_review(args):
    """A status call from a signal review: the session the plugin passes (host-owned), never a model's word."""
    return str(args.get('_review_session') or '').startswith(REVIEW_SESSION_PREFIX)


def light(compact):
    """compact_status's reply made lighter: every open to-do in short, every done one as a line."""
    open_, done = [], []
    for card in compact['suggestions']:
        card = dict(card)
        if 'body' in card:
            body = re.sub(r'\s+', ' ', card.pop('body') or '').strip()
            if body:
                card['body_start'] = clamp(body, BODY_START)
            for key in ('deliver_after', 'created_at'):
                card.pop(key, None)
            if card.get('latest_feedback'):
                card['latest_feedback'] = clamp(str(card['latest_feedback']), 160)
            open_.append(card)
        else:
            extra = {k: v for k, v in card.items() if k not in ('id', 'status', 'title', 'dedupe_key', 'closed_at')}
            done.append(f"{card['id']} {card.get('title') or ''}" + (f" ({str(card['closed_at'])[:10]})" if card.get('closed_at') else '')
                        + (' [dismissed]' if card.get('status') == 'rejected' else '') + (' ' + encoded(extra) if extra else ''))
    return fit({'review_health': compact['review_health'], 'suggestion_counts': compact['suggestion_counts'],
                'connectors': [{k: c[k] for k in ('id', 'service', 'display_name', 'error', 'pending') if c.get(k)} for c in compact['connectors']],
                'suggestions': open_, 'done': done,
                'decisions': [{k: d[k] for k in ('suggestion_id', 'choice', 'feedback') if d.get(k)} for d in compact['decisions']
                              if str(d.get('feedback') or '').strip()][:15],
                'note': NOTE})


def fit(result, limit=REVIEW_PAGE_CHARS):
    """Under the cut of a review's replies: the oldest done lines go first, then the oldest open to-dos' body_start.
    Every open to-do stays listed by its id and title, and what was left out is said."""
    done = short = 0
    cards = iter(reversed(result['suggestions']))
    while len(encoded(result)) > limit:
        if result['done']:
            result['done'].pop()
            done += 1
        elif (card := next(cards, None)) is None:
            break
        elif card.pop('body_start', None) is not None:
            short += 1
        result['left_out'] = LEFT.format(done=done, short=short)  # said in the reply it is measured with
    return result


def read_once(reads, session, result, again=False):
    """A second status in the same review: only the to-dos new or changed since it read them (each keyed by its
    content, so one a save changed shows again). again:true reads it whole."""
    def key(kind, item):
        return 'status', kind, hashlib.sha256(encoded(item).encode()).hexdigest()[:16]
    keys = [key('todo', c) for c in result['suggestions']] + [key('done', d) for d in result['done']]
    known = reads.before(session, keys)
    if again or not known:
        return result
    kept = [c for c in result['suggestions'] if key('todo', c) not in known]
    done = [d for d in result['done'] if key('done', d) not in known]
    left = len(result['suggestions']) - len(kept) + len(result['done']) - len(done)
    return {**result, 'suggestions': kept, 'done': done, 'already_read': AGAIN.format(n=left)}


def keys_of(kind, metadata):
    """A message's thread, chat and sender, as here() matches them."""
    out = set()
    if kind == 'gmail.message' and metadata.get('thread_id'):
        out.add(('thread', str(metadata['thread_id'])))
    chat = CHAT_KEYS.get(kind)
    if chat and metadata.get(chat) and not (kind == 'slack.message' and metadata.get('conversation_type') == 'channel'):
        out.add(('chat', str(metadata[chat])))
    sender = re.search(r'[\w.+-]+@[\w.-]+', str(metadata.get('from') or ''))
    if kind == 'gmail.message' and sender and not metadata.get('list_unsubscribe') and 'SENT' not in (metadata.get('labels') or ()):
        out.add(('sender', sender[0].lower()))
    return out


def here(db, event_ids, open_states):
    """The open to-dos that share a mail thread, a chat or a sender with these signals, newest first, with their first
    400 characters and the signals they share it with: at most HERE_MAX, within HERE_CHARS. A Slack channel is too
    wide to count as one conversation, its threads count by mail only."""
    def meta(row):
        try:
            found = json.loads(row['metadata'] or '{}') if not isinstance(row['metadata'], dict) else row['metadata']
        except (TypeError, ValueError):
            return {}
        return found if isinstance(found, dict) else {}
    if not event_ids:
        return []
    batch = {}
    for row in db.execute('SELECT id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(event_ids)) + ')', list(event_ids)):
        for k in keys_of(row['kind'], meta(row)):
            batch.setdefault(k, []).append(row['id'])
    if not batch:
        return []
    found, size = [], 0
    for card in db.execute('SELECT id,title,body,event_ids FROM suggestions WHERE status IN (' + ','.join('?' * len(open_states)) + ') '
                           'ORDER BY created_at DESC', list(open_states)).fetchall():
        try:
            ids = [i for i in json.loads(card['event_ids'] or '[]') if isinstance(i, int)][:HERE_EVIDENCE]
        except (TypeError, ValueError):
            continue
        if not ids:
            continue
        mine = set()
        for row in db.execute('SELECT kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids):
            mine |= keys_of(row['kind'], meta(row))
        shared = sorted({i for k in mine & set(batch) for i in batch[k]})
        if not shared:
            continue
        one = {'id': card['id'], 'title': card['title'], 'body': clamp(card['body'] or '', 400), 'shares_with_signals': shared[:6]}
        size += len(encoded(one))
        if size > HERE_CHARS:
            break
        found.append(one)
        if len(found) >= HERE_MAX:
            break
    return found

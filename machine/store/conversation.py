"""The conversation around a to-do's source message, for reading it on the dashboard (events-email.js): the messages
before it in the same chat, channel, Slack thread or email thread and the replies after it, from what the Machine
already stored. A mixin of Store, through ViewsStore.

A reply in a Slack thread often answers what was said in the channel before the thread started ("1. yes 2. no" to a
list of questions): its thread then comes with the channel's run before the thread's first message, so the reply
reads with what it answers. A Teams channel thread is its own conversation (its chat_id), read the same way as a chat.

Only messages of the same connection (account) and kind as the source are read, so a Work to-do never shows a
Personal message and the other way around; a teammate's shared message (fleet.*) and an Intercom conversation (one
stored event that already holds all its turns) get nothing added. Read-only."""
import datetime as dt
import json

from timeutil import local_tz
from machine.owner_error import OwnerError

# kind -> the plain (unsealed, message_seal.PLAIN_METADATA) metadata key its conversation is matched on in SQL
CONTEXT_KEYS = {'slack.message': 'channel_id', 'whatsapp.message': 'chat_id', 'telegram.message': 'chat_id',
                'signal.message': 'chat_id', 'teams.message': 'chat_id',
                'linkedin.message': 'conversation_id', 'x.dm': 'conversation_id', 'gmail.message': 'thread_id'}
BEFORE_MAX, BEFORE_MIN, AFTER_MAX, EARLIER_PAGE = 10, 3, 20, 20
THREAD_MAX = 20  # a Slack thread reply: its thread's earlier messages shown at once (more come with Show earlier)
SCAN = 400  # candidate rows read on each side; a busy channel's threads are filtered out in Python
# One fixed query per side; the metadata key goes in as a bound JSON path, never into the SQL text
_SIDE_SQL = {
    'before': 'SELECT id,occurred_at,metadata FROM events WHERE account_id=? AND kind=? AND deleted=0 AND json_extract(metadata,?)=? '
              'AND (occurred_at < ? OR (occurred_at=? AND id < ?)) ORDER BY occurred_at DESC,id DESC LIMIT ?',
    'after': 'SELECT id,occurred_at,metadata FROM events WHERE account_id=? AND kind=? AND deleted=0 AND json_extract(metadata,?)=? '
             'AND (occurred_at > ? OR (occurred_at=? AND id > ?)) ORDER BY occurred_at ASC,id ASC LIMIT ?',
}


def _meta(row):
    m = row['metadata']
    return m if isinstance(m, dict) else json.loads(m or '{}')


def _at(row):
    return dt.datetime.fromisoformat(str(row['occurred_at']).replace('Z', '+00:00'))


def slack_member(anchor, m):
    """Whether a Slack message belongs with the anchor: a reply sees its thread (the parent and the other replies); a
    top-level message sees the channel's other top-level messages and its own replies, not other threads' replies."""
    ts = str(anchor.get('message_ts') or '')
    thread = str(anchor.get('thread_ts') or ts)
    own_ts = str(m.get('message_ts') or '')
    own_thread = str(m.get('thread_ts') or own_ts)
    if ts and thread != ts:
        return own_thread == thread
    return own_thread == own_ts or bool(ts) and own_thread == ts


def thread_reply(anchor):
    """Whether the anchor is a reply in a Slack thread (not the thread's first message)."""
    if anchor['kind'] != 'slack.message':
        return False
    m = _meta(anchor)
    ts = str(m.get('message_ts') or '')
    return bool(ts) and str(m.get('thread_ts') or ts) != ts


def thread_start(anchor, older):
    """For a Slack thread reply, its thread's first message among `older` (its thread before it, oldest first), else None."""
    if not thread_reply(anchor) or not older:
        return None
    first = older[0]
    if str(_meta(first).get('message_ts') or '') != str(_meta(anchor).get('thread_ts') or ''):
        return None  # its first message isn't stored (older than the first import)
    return {**dict(first), 'account_id': anchor['account_id'], 'kind': anchor['kind']}


def in_thread(views, ids):
    """The views of a Slack thread's messages marked thread: true, so the viewer shows where the thread begins after
    the channel's messages before it."""
    return [{**v, 'thread': True} if v.get('event_id') in ids else v for v in views]


def same_day_run(before, anchor_at):
    """At most BEFORE_MAX messages (newest last), cut at the anchor's own day but never below BEFORE_MIN."""
    before = before[-BEFORE_MAX:]
    day = anchor_at.astimezone(local_tz()).date()
    today = [r for r in before if _at(r).astimezone(local_tz()).date() == day]
    return before[-max(len(today), BEFORE_MIN):]


def context_anchor(db, suggestion_id):
    """The to-do's main message that has a conversation to show (its first such source), or None."""
    row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        raise ValueError('Unknown suggestion')
    ids = [i for i in json.loads(row['event_ids'] or '[]') if isinstance(i, int)][:20]
    if not ids:
        return None
    found = {r['id']: r for r in db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE deleted=0 AND id IN ('
                                            + ','.join('?' * len(ids)) + ')', ids)}
    return next((found[i] for i in ids if i in found and found[i]['kind'] in CONTEXT_KEYS and _meta(found[i]).get(CONTEXT_KEYS[found[i]['kind']])), None)


def conversation_ids(db, anchor, side, cursor=None):
    """Event ids of the anchor's conversation on one side ('before': newest first; 'after': oldest first), up to SCAN
    read. cursor: an event of that conversation to page from instead of the anchor."""
    kind, key = anchor['kind'], CONTEXT_KEYS[anchor['kind']]
    start = cursor or anchor
    rows = db.execute(
        _SIDE_SQL['before' if side == 'before' else 'after'],
        (anchor['account_id'], kind, '$.' + key, str(_meta(anchor)[key]), start['occurred_at'], start['occurred_at'], start['id'], SCAN)).fetchall()
    if kind == 'slack.message':
        m = _meta(anchor)
        rows = [r for r in rows if slack_member(m, _meta(r))]
    return rows


class ConversationStore:
    """Store methods for a source message's conversation."""

    def context_anchor(self, db, suggestion_id):
        return context_anchor(db, suggestion_id)

    def conversation_ids(self, db, anchor, side, cursor=None):
        return conversation_ids(db, anchor, side, cursor)

    def message_context(self, suggestion_id, before=None):
        """{'event_id', 'before', 'after', 'earlier'} for a to-do's source message: the messages before it (at most
        BEFORE_MAX, the same day's run for a chat, never fewer than BEFORE_MIN when there are any; a whole email thread
        up to BEFORE_MAX) and the replies after it (AFTER_MAX), as event_views shows them; earlier: more before these.
        before: an event id of that conversation, for its next EARLIER_PAGE older messages (Show earlier). None when the
        to-do's source has no conversation stored around it.

        A Slack thread reply: its thread before it (up to THREAD_MAX) and, when that reaches the thread's first message,
        the channel's run before that message (the same rule as for a channel message), so the reply reads with what it
        answers. Show earlier pages the thread, then the channel before it."""
        with self.connect() as db:
            anchor = self.context_anchor(db, suggestion_id)
            if not anchor:
                return None
            older = list(reversed(self.conversation_ids(db, anchor, 'before')))
            start = thread_start(anchor, older)
            if before is not None:
                cursor = db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id=? AND deleted=0', (int(before),)).fetchone()
                key = CONTEXT_KEYS[anchor['kind']]
                # Only a message of this same conversation pages it: never a way to read another chat
                if not cursor or cursor['account_id'] != anchor['account_id'] or cursor['kind'] != anchor['kind'] \
                        or _meta(cursor).get(key) != _meta(anchor).get(key) \
                        or anchor['kind'] == 'slack.message' and cursor['id'] != anchor['id'] and not slack_member(_meta(anchor), _meta(cursor)) \
                        and not (start and slack_member(_meta(start), _meta(cursor))):
                    raise OwnerError('Original not available')  # only a message of this same conversation pages it
                thread = set()
                if start and (cursor['id'] == start['id'] or not thread_reply(cursor)):  # past the thread: the channel before it
                    rows = self.conversation_ids(db, start, 'before', cursor)
                    page, earlier = list(reversed(rows[:EARLIER_PAGE])), len(rows) > EARLIER_PAGE
                else:
                    rows = self.conversation_ids(db, anchor, 'before', cursor)
                    page, earlier = list(reversed(rows[:EARLIER_PAGE])), len(rows) > EARLIER_PAGE
                    if start:
                        thread = {r['id'] for r in page}
                    if start and not earlier:
                        lead, earlier = self.channel_lead(db, start)
                        page = lead + page
                return {'event_id': anchor['id'], 'before': in_thread(self.event_views([r['id'] for r in page]), thread), 'after': [], 'earlier': earlier}
            later = self.conversation_ids(db, anchor, 'after')[:AFTER_MAX]
            thread = set()
            if start:
                shown, earlier = older[-THREAD_MAX:], len(older) > THREAD_MAX
                thread = {r['id'] for r in shown}
                if not earlier:
                    lead, earlier = self.channel_lead(db, start)
                    shown = lead + shown
            else:
                shown = older[-BEFORE_MAX:] if anchor['kind'] == 'gmail.message' else same_day_run(older, _at(anchor))
                earlier = len(older) > len(shown)
        return {'event_id': anchor['id'], 'before': in_thread(self.event_views([r['id'] for r in shown]), thread),
                'after': self.event_views([r['id'] for r in later]), 'earlier': earlier}

    def channel_lead(self, db, start):
        """The channel's messages before a thread's first message (oldest first), as a channel message shows them
        (same_day_run), and whether there are more before those."""
        channel = list(reversed(self.conversation_ids(db, start, 'before')))
        lead = same_day_run(channel, _at(start))
        return lead, len(channel) > len(lead)

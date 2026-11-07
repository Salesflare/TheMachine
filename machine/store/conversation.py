"""The conversation around a to-do's source message, for reading it on the dashboard (events-email.js): the messages
before it in the same chat, channel, Slack thread or email thread and the replies after it, from what the Machine
already stored. A mixin of Store, through ViewsStore.

Only messages of the same connection (account) and kind as the source are read, so a Work to-do never shows a
Personal message and the other way around; a teammate's shared message (fleet.*) and an Intercom conversation (one
stored event that already holds all its turns) get nothing added. Read-only."""
import datetime as dt
import json

from timeutil import local_tz

# kind -> the plain (unsealed, message_seal.PLAIN_METADATA) metadata key its conversation is matched on in SQL
CONTEXT_KEYS = {'slack.message': 'channel_id', 'whatsapp.message': 'chat_id', 'telegram.message': 'chat_id',
                'linkedin.message': 'conversation_id', 'x.dm': 'conversation_id', 'gmail.message': 'thread_id'}
BEFORE_MAX, BEFORE_MIN, AFTER_MAX, EARLIER_PAGE = 10, 3, 20, 20
SCAN = 400  # candidate rows read on each side; a busy channel's threads are filtered out in Python


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


def same_day_run(before, anchor_at):
    """At most BEFORE_MAX messages (newest last), cut at the anchor's own day but never below BEFORE_MIN."""
    before = before[-BEFORE_MAX:]
    day = anchor_at.astimezone(local_tz()).date()
    today = [r for r in before if _at(r).astimezone(local_tz()).date() == day]
    return before[-max(len(today), BEFORE_MIN):]


class ConversationStore:
    """Store methods for a source message's conversation."""

    def context_anchor(self, db, suggestion_id):
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

    def conversation_ids(self, db, anchor, side, cursor=None):
        """Event ids of the anchor's conversation on one side ('before': newest first; 'after': oldest first), up to SCAN
        read. cursor: an event of that conversation to page from instead of the anchor."""
        kind, key = anchor['kind'], CONTEXT_KEYS[anchor['kind']]
        start = cursor or anchor
        op, order = ('<', 'DESC') if side == 'before' else ('>', 'ASC')
        rows = db.execute(
            f"SELECT id,occurred_at,metadata FROM events WHERE account_id=? AND kind=? AND deleted=0 AND json_extract(metadata,'$.{key}')=? "
            f'AND (occurred_at {op} ? OR (occurred_at=? AND id {op} ?)) ORDER BY occurred_at {order},id {order} LIMIT ?',
            (anchor['account_id'], kind, str(_meta(anchor)[key]), start['occurred_at'], start['occurred_at'], start['id'], SCAN)).fetchall()
        if kind == 'slack.message':
            m = _meta(anchor)
            rows = [r for r in rows if slack_member(m, _meta(r))]
        return rows

    def message_context(self, suggestion_id, before=None):
        """{'event_id', 'before', 'after', 'earlier'} for a to-do's source message: the messages before it (at most
        BEFORE_MAX, the same day's run for a chat, never fewer than BEFORE_MIN when there are any; a whole email thread
        up to BEFORE_MAX) and the replies after it (AFTER_MAX), as event_views shows them; earlier: more before these.
        before: an event id of that conversation, for its next EARLIER_PAGE older messages (Show earlier). None when the
        to-do's source has no conversation stored around it."""
        with self.connect() as db:
            anchor = self.context_anchor(db, suggestion_id)
            if not anchor:
                return None
            if before is not None:
                cursor = db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id=? AND deleted=0', (int(before),)).fetchone()
                key = CONTEXT_KEYS[anchor['kind']]
                # Only a message of this same conversation pages it: never a way to read another chat
                if not cursor or cursor['account_id'] != anchor['account_id'] or cursor['kind'] != anchor['kind'] \
                        or _meta(cursor).get(key) != _meta(anchor).get(key) \
                        or anchor['kind'] == 'slack.message' and not slack_member(_meta(anchor), _meta(cursor)) and cursor['id'] != anchor['id']:
                    raise ValueError('Original not available')  # only a message of this same conversation pages it
                older = self.conversation_ids(db, anchor, 'before', cursor)
            else:
                older = list(reversed(self.conversation_ids(db, anchor, 'before')))
                later = self.conversation_ids(db, anchor, 'after')[:AFTER_MAX]
        if before is not None:
            page = list(reversed(older[:EARLIER_PAGE]))
            return {'event_id': anchor['id'], 'before': self.event_views([r['id'] for r in page]), 'after': [],
                    'earlier': len(older) > EARLIER_PAGE}
        shown = older[-BEFORE_MAX:] if anchor['kind'] == 'gmail.message' else same_day_run(older, _at(anchor))
        return {'event_id': anchor['id'], 'before': self.event_views([r['id'] for r in shown]),
                'after': self.event_views([r['id'] for r in later]), 'earlier': len(older) > len(shown)}

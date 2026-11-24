"""From when on something counts as news on a to-do or a promise: a moment per conversation its evidence is in (what came
after the mail from thread A is judged from that mail on, whatever came in thread B since), and one for everywhere else.
A calendar event is no message: it takes place later than it says anything, so it counts by when it was made or changed,
and only where no message is evidence. Never later than now, and never before the owner added the to-do themselves: it
was open then."""
import datetime as dt
import json

from machine.kinds import KINDS, MEETING
from timeutil import now

# What takes place at its time instead of being said then (a meeting's notes and transcript are said)
TAKES_PLACE = frozenset(k for k, row in KINDS.items() if row['family'] == MEETING and k.endswith(('.event', '.meeting')))


def conversation_of(kind, m):
    """The conversation a message belongs to: an email thread, a Slack channel or DM, a chat."""
    key = m.get('thread_id') if kind == 'gmail.message' else m.get('channel_id') if kind == 'slack.message' else m.get('chat_id') or m.get('conversation_id')
    return str(key) if key else None


def conversation(account_id, kind, m):
    """A message's conversation, as (account, kind, its key, its Slack thread); None when it is in none. m: its metadata."""
    key = conversation_of(kind, m)
    return (account_id, kind, key, str(m.get('thread_ts') or '') if kind == 'slack.message' else '') if key else None


def made_or_changed(db, row, m):
    """When a calendar event was last made or changed, else when its latest version reached the Machine."""
    try:
        at = dt.datetime.fromisoformat(str(m.get('updated') or '').replace('Z', '+00:00'))
        return (at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)).astimezone(dt.timezone.utc).isoformat()
    except ValueError:
        return db.execute('SELECT ingested_at FROM events WHERE id=?', (row['id'],)).fetchone()[0]


class Moments:
    """rows: the evidence (id, account_id, kind, occurred_at, metadata). everywhere: the moment for what is in none of its
    conversations, None without evidence."""

    def __init__(self, db, event_ids):
        self.ids = [i for i in event_ids or () if isinstance(i, int)]
        self.rows = [(r, json.loads(r['metadata'] or '{}')) for r in db.execute(
            'SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id IN (SELECT value FROM json_each(?))',
            (json.dumps(self.ids),))]
        current = now()
        self.threads, self.channels, said = {}, {}, []
        added = max((r['occurred_at'] for r, _ in self.rows if r['kind'] == 'owner.card'), default='')
        for r, m in self.rows:
            if r['kind'] in TAKES_PLACE:
                continue
            at = min(max(r['occurred_at'], added), current)
            said.append(at)
            found = conversation(r['account_id'], r['kind'], m)
            if found:
                self.threads[found] = max(self.threads.get(found, ''), at)
                self.channels[found[:3]] = max(self.channels.get(found[:3], ''), at)
        self.everywhere = max(said or [min(made_or_changed(db, r, m), current) for r, m in self.rows], default=None)

    def of(self, account_id, kind, m):
        """The moment for a message: its own conversation's when evidence is in it, else the one for everywhere."""
        return self.threads.get(conversation(account_id, kind, m)) or self.everywhere

    def channel(self, account_id, kind, key):
        """The moment for a whole chat (a DM, a group DM), its threads included."""
        return self.channels.get((account_id, kind, str(key))) or self.everywhere

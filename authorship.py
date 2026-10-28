"""Who wrote a message the owner sent: the owner themselves, or The Machine (docs/intelligence.md#how-you-write).

A message the owner sent from a to-do (Send on a draft) comes back in their Sent mail or chat like any message of
theirs, with their name on it. It is still an agent's draft, even when they approved it, so it says how the drafts
write, not how the owner does. Voice and style learn only from what the owner wrote themselves: the profile, the voice
study, the examples a draft matches and the "answered it themselves" lessons all skip messages The Machine sent.
A draft the owner changed before sending teaches through that change instead (draft_edits: what they cut and added),
weighed by what they changed, never as if all of it were theirs.

How a sent message is recognized, from the send jobs (action_jobs with status sent):
- by its id: the Gmail Message-ID the send set (rfc_message_id) or the message id the channel returned (Gmail id,
  Slack ts, WhatsApp, Telegram, LinkedIn or X id), against the collected message's own ids;
- by its text, for a send whose id never came back: the collected message starts with the text that was sent (a
  signature or quoted history may follow). Only texts long enough to say something are matched, so a "Thanks!" the
  owner typed themselves still counts as theirs.
"""
from __future__ import annotations

import json

MIN_TEXT = 20     # shorter sent texts are matched by id only: a short reply is too common to tell apart
TEXT_PREFIX = 200  # this much of the sent text is compared, after spacing and case are evened out
ID_FIELDS = ('message-id', 'message_id', 'message_ts', 'ts', 'id')
SKIP_PREFIXES = ('merge:', 'undo:')  # a merged code fix is no message


def norm(text):
    return ' '.join(str(text or '').split()).casefold()


def _ids(value):
    value = str(value or '').strip()
    if not value or value.startswith(SKIP_PREFIXES):
        return set()
    out = {value, value.strip('<>')}
    if ':' in value and not value.startswith('urn:'):
        out.add(value.rsplit(':', 1)[-1])  # slack:<channel>:<ts>, whatsapp:<id>, x:<id>
    return {v for v in out if v}


class MachineSent:
    """The messages The Machine sent for the owner, to tell them apart from what the owner wrote themselves."""

    def __init__(self, jobs=()):
        self.ids, self.texts, self.edited = set(), [], set()
        for job in jobs:
            job = dict(job)
            try:
                action = json.loads(job.get('payload') or '{}')
            except ValueError:
                action = {}
            if action.get('kind') in ('merge', 'calendar'):
                continue
            self.ids |= _ids(job.get('rfc_message_id')) | _ids(job.get('message_id'))
            body = action.get('body') if action.get('kind') != 'finish' else action.get('message')
            text = norm(body)
            if len(text) >= MIN_TEXT:
                self.texts.append(text[:TEXT_PREFIX])

    @classmethod
    def load(cls, db):
        try:
            rows = db.execute("SELECT payload,rfc_message_id,message_id FROM action_jobs WHERE status='sent'").fetchall()
        except Exception:
            rows = []  # no send jobs yet
        return cls(rows)

    def __bool__(self):
        return bool(self.ids or self.texts)

    def wrote(self, event, text=None):
        """Whether The Machine wrote this collected message (an event row or dict). `text` is what the owner's part
        of it says (without quoted history), when the caller has it already."""
        if not self:
            return False
        m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
        keys = set()
        try:
            keys |= _ids(event['source_id'])
        except (KeyError, IndexError):
            pass
        for field in ID_FIELDS:
            keys |= _ids(m.get(field))
        if keys & self.ids:
            return True
        if text is None:
            text = str(event['body'] or '').split('[Quoted earlier messages', 1)[0]
        mine = norm(text)
        return any(mine.startswith(sent)
                   for sent in self.texts)


def own_only(rows, sent, text_of=None):
    """The rows the owner wrote themselves, in order."""
    return [r for r in rows if not sent.wrote(r, text_of(r) if text_of else None)]


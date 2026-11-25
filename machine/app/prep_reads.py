"""A to-do's run reads less: it starts from what its review found, and reads each message once.

- review_brief: the job message's "What the review found" block. The to-do as saved (title, summary, organization,
  project, due day) and a header line per message it came from (who wrote it, to whom, its subject, thread and time),
  read from the database, no model call. With it, the run looks up only what is missing (READ_BUDGET) instead of
  finding the same messages, people and threads again. A token study of the owner's runs found about half their
  message reads were the to-do's own messages, read once more, or reads of something already read in that run.
- RunReads: within one run (its OpenClaw run id, which the plugin passes as _prep_run, host-owned), a message the run
  already got whole from events or related comes back as its id under already_read with a short note, not its text
  again. Every tool call resends the whole session, so each repeat costs the full context again. again:true reads it
  anew (the text may have left the context). Kept in memory for a few hours: a restart only means a full read once more.
- history_once: the same for preparation_history (a page this run already got comes back as unchanged), and
  SyncApp.slack_read lists only the messages new since the run's last read of that conversation. A study of the
  owner's runs found most of their status, slack_read and preparation_history calls were repeats."""
import hashlib
import json
import threading
import time

from mail_senders import recipients, to_people
from machine.store.review import local_when
from machine.text import clamp

SOURCES = 12          # source messages listed in the brief at most
BRIEF_CHARS = 3000    # the whole block at most
RUNS = 200            # runs remembered at once
RUN_SECONDS = 4 * 3600

READ_BUDGET = ('Start from this and from the blocks below: look up only what is still missing. Read the to-do\'s own messages '
               'once, all in one events call, for their exact words; search further only for a specific gap (an earlier '
               'thread, a fact the draft needs). No status check before saving: a save that newer feedback replaced is '
               'refused. A message read again in this run comes back as "already read above".')
ALREADY_READ = ('Already read above in this run, so left out here: work from the text you have. Only when it is no longer '
                'in front of you, read those ids again with again:true.')


def _who(people):
    return ', '.join(people[:4]) + (f' and {len(people) - 4} more' if len(people) > 4 else '')


def source_line(row, threads=None):
    """One message the to-do came from as a header line: id, kind, when, account, from, to, subject, thread. No body.
    The thread is whole, since a reply names it (a LinkedIn conversation's id is over 140 characters), and once: a later
    message in it points to the first (threads: {thread: event id}). Tool results leave it out (compact_metadata)."""
    try:
        meta = json.loads(row['metadata'] or '{}')
    except (TypeError, ValueError):
        meta = {}
    meta = meta if isinstance(meta, dict) else {}
    when = local_when(row['occurred_at'])
    parts = [f"event {row['id']} ({row['kind']}, " + (f'{when} local time)' if when else f"{str(row['occurred_at'])[:16]} UTC)")]
    parts.append(f"on {row['account_id']}")
    if meta.get('from'):
        parts.append('from ' + clamp(_who(recipients(meta['from'])), 160))
    if to := to_people(meta):
        parts.append('to ' + clamp(_who(to), 200))
    if row['title']:
        parts.append('"' + clamp(' '.join(str(row['title']).split()), 140) + '"')
    thread = meta.get('thread_id') or meta.get('conversation_id') or meta.get('chat_id') or meta.get('channel_id')
    if thread:
        first = row['id'] if threads is None else threads.setdefault(str(thread), row['id'])
        parts.append(f'same thread as event {first}' if first != row['id'] else 'thread ' + str(thread)[:400])
    return '- ' + ', '.join(parts)


def review_brief(db, suggestion_id):
    """The block for a to-do's preparation: what its review found, so the run doesn't find it again. '' when none."""
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        return ''
    row = dict(row)
    try:
        ids = [int(i) for i in json.loads(row.get('event_ids') or '[]')][:SOURCES]
    except (TypeError, ValueError):
        ids = []
    found = {r['id']: r for r in db.execute(
        f"SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE id IN ({','.join('?' * len(ids))}) AND deleted=0", ids)} if ids else {}
    lines = ['- To-do: ' + clamp(' '.join(str(row.get('title') or '').split()), 160)]
    if row.get('body'):
        lines.append('- Its summary now: ' + clamp(' '.join(str(row['body']).split()), 700))
    for label, key in (('Organization', 'org'), ('Project', 'project'), ('Due', 'due'), ('Its moment', 'expires_what')):
        if row.get(key):
            lines.append(f'- {label}: ' + clamp(str(row[key]), 160))
    if row.get('based_on'):
        lines.append(f"- Follows event {row['based_on']} (someone else's input)")
    threads = {}
    heads = [source_line(found[i], threads) for i in ids if i in found]
    if heads:
        lines.append('- The messages it came from, which the review read whole:')
        lines += heads
    text = '\n'.join(lines)
    if len(text) > BRIEF_CHARS:
        text = text[:BRIEF_CHARS].rsplit('\n', 1)[0]
    return '\n\nWhat the review found when it made this to-do (no need to look it up again):\n' + text + '\n' + READ_BUDGET


class RunReads:
    """Which messages each run got whole from events or related, in memory, so a repeat read gets a note instead."""

    def __init__(self, runs=RUNS, seconds=RUN_SECONDS, clock=time.monotonic):
        self.runs, self.seconds, self.clock = runs, seconds, clock
        self.lock = threading.Lock()
        self.seen = {}  # run: (last use, {event id})

    def _ids(self, run):
        now = self.clock()
        for old in [r for r, (at, _) in self.seen.items() if now - at > self.seconds]:
            del self.seen[old]
        if run not in self.seen and len(self.seen) >= self.runs:
            del self.seen[min(self.seen, key=lambda r: self.seen[r][0])]
        ids = self.seen.get(run, (now, set()))[1]
        self.seen[run] = (now, ids)
        return ids

    @staticmethod
    def _read(row):
        """A message as read: its id and version, so one edited in place since (a new version) reads whole again."""
        return 'event', row['id'], row.get('version') if hasattr(row, 'get') else None

    def split(self, run, rows):
        """(rows not read whole yet in this run, ids of the ones that were, at the version read)."""
        if not run:
            return rows, []
        with self.lock:
            ids = set(self._ids(run))
        return [r for r in rows if self._read(r) not in ids], [r['id'] for r in rows if self._read(r) in ids]

    def mark(self, run, views):
        """The events a result showed from the start of their body (not a later part, not a passage a search matched)."""
        if not run:
            return
        with self.lock:
            self._ids(run).update(self._read(v) for v in views if not v.get('body_offset') and not v.get('body_matched'))

    def before(self, run, keys):
        """Of these keys (tuples: a history page, a Slack message listed), the ones this run got before; all are marked
        now. Empty without a run."""
        if not run:
            return set()
        keys = set(keys)
        with self.lock:
            ids = self._ids(str(run))
            known = keys & ids
            ids.update(keys)
        return known


HISTORY_UNCHANGED = ('Unchanged since you read this page earlier in this run: earlier runs\' calls do not change while '
                     'this one goes on, so work from what you read. Only when it is no longer in front of you, ask again '
                     'with again:true.')


def history_once(reads, run, args, result):
    """A preparation_history page this run already got, word for word: a short note instead of the page again (it
    lists only earlier runs' calls, so within a run it stays the same). again:true reads it anew, and one call's exact
    details (call_ref) always read whole: they are read on purpose, to reconcile a step."""
    if not run or args.get('again') is True or args.get('call_ref') is not None:
        return result
    digest = hashlib.sha256(json.dumps(result, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    key = ('history', int(args.get('offset') or 0), digest)
    if not reads.before(run, [key]):
        return result
    return {'unchanged': True, 'next_offset': result.get('next_offset'), 'note': HISTORY_UNCHANGED}


def read_once(reads, args, rows):
    """For an events or related call: (rows to show, ids left out as already read). Only a run's first page of bodies
    is checked: a later body part (body_offset), metadata, a later row page or again:true reads as asked."""
    run = args.get('_prep_run')
    if (not run or args.get('again') is True or args.get('full') or args.get('metadata_offset') is not None
            or int(args.get('body_offset') or 0) or int(args.get('row_offset') or 0)):
        return rows, []
    return reads.split(str(run), rows)

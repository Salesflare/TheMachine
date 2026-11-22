"""A to-do's run reads less: it starts from what its review found, and reads each message once.

- review_brief: the job message's "What the review found" block. The to-do as saved (title, summary, organization,
  project, due day) and a header line per message it came from (who wrote it, to whom, its subject, thread and time),
  read from the database, no model call. With it, the run looks up only what is missing (READ_BUDGET) instead of
  finding the same messages, people and threads again. A token study of the owner's runs found about half their
  message reads were the to-do's own messages, read once more, or reads of something already read in that run.
- RunReads: within one run (its OpenClaw run id, which the plugin passes as _prep_run, host-owned), a message the run
  already got whole from events or related comes back as its id under already_read with a short note, not its text
  again. Every tool call resends the whole session, so each repeat costs the full context again. again:true reads it
  anew (the text may have left the context). Kept in memory for a few hours: a restart only means a full read once more."""
import json
import threading
import time

from machine.store.review import local_when
from machine.text import clamp

SOURCES = 12          # source messages listed in the brief at most
BRIEF_CHARS = 3000    # the whole block at most
RUNS = 200            # runs remembered at once
RUN_SECONDS = 4 * 3600

READ_BUDGET = ('Start from this and from the blocks below: look up only what is still missing. Read the to-do\'s own messages '
               'once, all in one events call, for their exact words; search further only for a specific gap (an earlier '
               'thread, a fact the draft needs). Re-check status only before saving. A message read again in this run '
               'comes back as "already read above".')
ALREADY_READ = ('Already read above in this run, so left out here: work from the text you have. Only when it is no longer '
                'in front of you, read those ids again with again:true.')


def _who(value):
    if isinstance(value, list):
        return ', '.join(_who(v) for v in value[:4]) + (f' and {len(value) - 4} more' if len(value) > 4 else '')
    if isinstance(value, dict):
        name, address = value.get('name') or '', value.get('email') or value.get('address') or ''
        return f'{name} <{address}>' if name and address else str(name or address)
    return str(value or '')


def source_line(row):
    """One message the to-do came from as a header line: id, kind, when, from, to, subject, thread. No body."""
    try:
        meta = json.loads(row['metadata'] or '{}')
    except (TypeError, ValueError):
        meta = {}
    meta = meta if isinstance(meta, dict) else {}
    when = local_when(row['occurred_at'])
    parts = [f"event {row['id']} ({row['kind']}, " + (f'{when} local time)' if when else f"{str(row['occurred_at'])[:16]} UTC)")]
    if meta.get('from'):
        parts.append('from ' + clamp(_who(meta['from']), 160))
    if meta.get('to'):
        parts.append('to ' + clamp(_who(meta['to']), 200))
    if row['title']:
        parts.append('"' + clamp(' '.join(str(row['title']).split()), 140) + '"')
    thread = meta.get('thread_id') or meta.get('conversation_id') or meta.get('chat_id') or meta.get('channel_id')
    if thread:
        parts.append('thread ' + clamp(str(thread), 80))
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
        f"SELECT id,kind,occurred_at,title,metadata FROM events WHERE id IN ({','.join('?' * len(ids))}) AND deleted=0", ids)} if ids else {}
    lines = ['- To-do: ' + clamp(' '.join(str(row.get('title') or '').split()), 160)]
    if row.get('body'):
        lines.append('- Its summary now: ' + clamp(' '.join(str(row['body']).split()), 700))
    for label, key in (('Organization', 'org'), ('Project', 'project'), ('Due', 'due'), ('Its moment', 'expires_what')):
        if row.get(key):
            lines.append(f'- {label}: ' + clamp(str(row[key]), 160))
    if row.get('based_on'):
        lines.append(f"- Follows event {row['based_on']} (someone else's input)")
    heads = [source_line(found[i]) for i in ids if i in found]
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

    def split(self, run, rows):
        """(rows not read whole yet in this run, ids of the ones that were)."""
        if not run:
            return rows, []
        with self.lock:
            ids = set(self._ids(run))
        return [r for r in rows if r['id'] not in ids], [r['id'] for r in rows if r['id'] in ids]

    def mark(self, run, views):
        """The events a result showed from the start of their body (not a later part, not a passage a search matched)."""
        if not run:
            return
        with self.lock:
            self._ids(run).update(v['id'] for v in views if not v.get('body_offset') and not v.get('body_matched'))


def read_once(reads, args, rows):
    """For an events or related call: (rows to show, ids left out as already read). Only a run's first page of bodies
    is checked: a later body part (body_offset), metadata, a later row page or again:true reads as asked."""
    run = args.get('_prep_run')
    if (not run or args.get('again') is True or args.get('full') or args.get('metadata_offset') is not None
            or int(args.get('body_offset') or 0) or int(args.get('row_offset') or 0)):
        return rows, []
    return reads.split(str(run), rows)

"""What memory went into a prompt: one shape for a piece of memory, and a log of what was read.

A prompt reads several kinds of memory: facts and draft rules, open promises, what the owner did with recent to-dos,
the people and projects on a to-do, related signals, the owner's skills and team learnings. Each has its own picker
(Store.facts_for, Store.promises_text, App.graph_lines and the rest). This module gives them one shape (Item) and
one log (the memory_use table), so "what did this prompt read" and "was this ever read" have one answer.

How it fits together:
- A prompt builder asks machine/app/recall.py for a Recalled: the pickers of its purpose, under block names.
- Recalled.text(block) runs a picker. While it runs, the picker's note() calls say what it put in its text: one Item
  per row. Outside a Recalled, note() does nothing, so a picker called on its own behaves as before.
- Recalled.rows() is what goes in the log: ids and numbers, never text. The builder puts it on its request (_memory)
  and calls record() once the run is admitted, so a retry that resends its first start logs that start's rows.
- record() is one insert for the whole prompt, and stamps facts.used_at for the facts picked for their to-do. It
  never raises: a prompt is never lost over its log.

The table stays on this Machine: it is in the owner's full export and goes with a delete (work_removal.purge by its
suggestion_id, forget_person for a deleted person's records), and nothing shares it. Rows older than KEEP_DAYS go in
the nightly retention pass (retention.run).

outcomes() and summary() join the log with what the owner then did with the to-do (sent as written, edited,
dismissed, snoozed): numbers only, for the learning loop to read later. Nothing reads them yet."""
from __future__ import annotations

import contextvars
import dataclasses
import datetime as dt
import logging

from timeutil import now

LOG = logging.getLogger('personal-assistant')

KEEP_DAYS = 60   # a use older than this is gone (fewer at the Careful level, as for a run's tool calls)
PURPOSES = ('review', 'preparation', 'ask', 'routine', 'talk', 'chat', 'todo_chat')
# What a piece of memory is, by the table its row id is in:
# fact, rule: facts (kind fact, draft); promise: promises; history: suggestions (the owner's recent to-dos, 30 days);
# record: graph_nodes (a person or project); signal: events; skill: skills (by slug); team_learning: by fingerprint;
# voice: voices (by channel).
KINDS = ('fact', 'rule', 'promise', 'history', 'record', 'signal', 'skill', 'team_learning', 'voice')
# How it was picked: always (all of them, while they fit), own (learned on this to-do), closeness (by meaning, with a
# score), weight (what counts most, when meaning can't be ranked), recency (a window of days), match (by name or
# words), about (it is on the to-do's signals, or in the question's scope), search (the search's best matches),
# rotation (its turn: the one a review saw longest ago, review_facts.py).
HOWS = ('always', 'own', 'closeness', 'weight', 'recency', 'match', 'about', 'search', 'rotation')
OUTCOMES = ('sent_unchanged', 'sent_edited', 'dismissed', 'snoozed', 'open')

SCHEMA = '''
CREATE TABLE IF NOT EXISTS memory_use(
  id INTEGER PRIMARY KEY,at TEXT NOT NULL,purpose TEXT NOT NULL,run_id TEXT NOT NULL DEFAULT '',
  suggestion_id TEXT NOT NULL DEFAULT '',kind TEXT NOT NULL,row_id TEXT NOT NULL,how TEXT NOT NULL,
  score REAL,chars INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS memory_use_todo ON memory_use(suggestion_id);
CREATE INDEX IF NOT EXISTS memory_use_item ON memory_use(kind,row_id);
CREATE INDEX IF NOT EXISTS memory_use_seen ON memory_use(kind,purpose,row_id,at);
'''


def ensure(db):
    db.executescript(SCHEMA)


@dataclasses.dataclass(frozen=True)
class Item:
    """One piece of memory as a prompt got it."""
    kind: str             # one of KINDS
    row_id: str           # its row in that kind's table
    text: str             # what went in the prompt for it
    how: str              # one of HOWS
    about: tuple = ()     # the records (graph node ids) it is about, where the picker knows them
    source: str = ''      # where it came from: signal, note, promise, owner, ai, team
    at: str = ''          # when it was learned or said
    score: float | None = None  # how close, for closeness
    used: bool = False    # picked for this to-do, not just listed: counts as a use of the fact (facts.used_at)


_OPEN = contextvars.ContextVar('memory_use_open', default=None)


def collecting():
    """Whether a Recalled is reading a picker right now (in this thread)."""
    return _OPEN.get() is not None


def note(kind, row_id, text, how, about=(), source='', at='', score=None, used=False):
    """A picker says what it put in its text. Does nothing outside a Recalled, and never raises."""
    bag = _OPEN.get()
    if bag is None:
        return
    try:
        bag.append(Item(str(kind), str(row_id), str(text or ''), str(how), tuple(about or ()), str(source or ''), str(at or ''),
                        None if score is None else float(score), bool(used)))
    except Exception as error:  # the log never costs a prompt its memory
        LOG.error('memory note error=%s', type(error).__name__)


def note_lines(kind, lines, shown, limit, how, source=''):
    """For a text that is lines joined and then cut at limit characters: notes the rows whose whole line is inside
    the cut. shown: [(index in lines, row id)]."""
    if not collecting():
        return
    ends, size = [], -1
    for line in lines:
        size += len(line) + 1
        ends.append(size)
    for index, row_id in shown:
        if index < len(ends) and ends[index] <= limit:
            note(kind, row_id, lines[index], how, source=source)


class Recalled:
    """The memory one prompt reads: its purpose's pickers by block name, run when the builder asks for their text."""

    def __init__(self, purpose, about=None, budget=0):
        if purpose not in PURPOSES:
            raise ValueError('unknown_purpose')
        self.purpose, self.about, self.budget = purpose, dict(about or {}), int(budget or 0)
        self.pickers, self.blocks = {}, {}

    def add(self, block, picker):
        self.pickers[block] = picker
        return self

    def read(self, block, *args, **kwargs):
        """Runs the block's picker and returns what it returns, keeping what it noted. A picker that raises does so
        here, as it did for the builder before, and leaves nothing behind."""
        bag = []
        token = _OPEN.set(bag)
        try:
            out = self.pickers[block](*args, **kwargs)
        finally:
            _OPEN.reset(token)
        self.blocks[block] = bag
        return out

    text = read  # most pickers return the prompt's text for their block

    def fit(self, block, used, reserve=0, *args, **kwargs):
        """The block's text when it fits the budget next to `used` characters with `reserve` to spare, else '' (and
        then nothing of it counts as read)."""
        text = self.read(block, *args, **kwargs)
        if used + len(text) < self.budget - reserve:
            return text
        self.drop(block)
        return ''

    def drop(self, block):
        """The builder left this block out after all."""
        self.blocks.pop(block, None)

    def items(self):
        return [item for block in self.blocks.values() for item in block]

    def picked(self):
        """{kind: [Item]} of what the prompt got."""
        out = {}
        for item in self.items():
            out.setdefault(item.kind, []).append(item)
        return out

    def rows(self):
        """What the log keeps of each item: [kind, row id, how, score, characters, used]. No text."""
        return [[i.kind, i.row_id, i.how, i.score, len(i.text), 1 if i.used else 0] for i in self.items()]


def record(store, purpose, rows, run_id='', suggestion_id='', at=None):
    """Logs one prompt's rows (Recalled.rows) in one insert, and stamps the facts picked for their to-do as used.
    Returns how many were logged; 0, never an error, when it can't."""
    try:
        rows = [r for r in rows or () if isinstance(r, (list, tuple)) and len(r) >= 6]
        if not rows:
            return 0
        at = at or now()
        with store.connect() as db:
            db.executemany('INSERT INTO memory_use(at,purpose,run_id,suggestion_id,kind,row_id,how,score,chars) VALUES(?,?,?,?,?,?,?,?,?)',
                           [(at, str(purpose), str(run_id or ''), str(suggestion_id or ''), str(r[0]), str(r[1]), str(r[2]),
                             None if r[3] is None else float(r[3]), int(r[4] or 0)) for r in rows])
        used = [r[1] for r in rows if r[5] and r[0] in ('fact', 'rule') and str(r[1]).isdigit()]
        if used:
            store.mark_used(used)
        return len(rows)
    except Exception as error:  # a busy or broken log never fails the prompt it is about
        LOG.error('memory use log error=%s', type(error).__name__)
        return 0


def prune(connect, when, days=KEEP_DAYS):
    """Rows older than `days` before `when` (a datetime) go. Returns how many."""
    cutoff = (when.astimezone(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()
    with connect() as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='memory_use'").fetchone():
            return 0  # a database from before the log
        return db.execute('DELETE FROM memory_use WHERE at<?', (cutoff,)).rowcount


def forget_person(db, needles):
    """A person was deleted for good: the uses of their record go (a record's row id holds an address), and those of
    any record that is no longer there. Returns how many."""
    gone = db.execute("DELETE FROM memory_use WHERE kind='record' AND row_id NOT IN (SELECT id FROM graph_nodes)").rowcount
    for needle in {str(n).lower() for n in needles or () if str(n).strip()}:
        gone += db.execute("DELETE FROM memory_use WHERE kind='record' AND instr(lower(row_id),?)>0", (needle,)).rowcount
    return gone


def last_used(db, kind, row_ids=None):
    """{row id: when a prompt last read it} for a kind, from the log (so within KEEP_DAYS)."""
    sql, args = 'SELECT row_id,max(at) FROM memory_use WHERE kind=?', [kind]
    if row_ids is not None:
        ids = [str(i) for i in row_ids]
        if not ids:
            return {}
        sql += ' AND row_id IN (' + ','.join('?' for _ in ids) + ')'
        args += ids
    return {r[0]: r[1] for r in db.execute(sql + ' GROUP BY row_id', args)}


def counts(db):
    """Numbers only, for a status or support view: rows per purpose and per kind."""
    return {'purposes': {r[0]: r[1] for r in db.execute('SELECT purpose,count(*) FROM memory_use GROUP BY purpose')},
            'kinds': {r[0]: r[1] for r in db.execute('SELECT kind,count(*) FROM memory_use GROUP BY kind')}}


# What the owner did with a to-do, as one word. Sent wins over a later dismissal; an edit is the owner's own change
# to a draft (not an agent's rewrite), as Store.behaviour counts it.
_OUTCOME = '''CASE
  WHEN EXISTS(SELECT 1 FROM action_jobs j WHERE j.suggestion_id=s.id AND j.status='sent') THEN
    CASE WHEN EXISTS(SELECT 1 FROM draft_edits e WHERE e.suggestion_id=s.id AND e.source!='agent') THEN 'sent_edited' ELSE 'sent_unchanged' END
  WHEN EXISTS(SELECT 1 FROM decisions d WHERE d.suggestion_id=s.id AND d.choice='reject') THEN 'dismissed'
  WHEN EXISTS(SELECT 1 FROM decisions d WHERE d.suggestion_id=s.id AND d.choice='snooze') THEN 'snoozed'
  ELSE 'open' END'''


def outcomes(db, suggestion_id):
    """For one to-do: what memory was in its prompts, and what the owner then did. {'todo', 'outcome', 'edits',
    'decisions': {choice: count}, 'prompts', 'memory': [{'at', 'purpose', 'run', 'kind', 'row_id', 'how', 'score',
    'chars'}]}; None for a to-do that isn't there."""
    row = db.execute(f'SELECT {_OUTCOME} FROM suggestions s WHERE s.id=?', (suggestion_id,)).fetchone()
    if not row:
        return None
    memory = [{'at': r[0], 'purpose': r[1], 'run': r[2], 'kind': r[3], 'row_id': r[4], 'how': r[5], 'score': r[6], 'chars': r[7]}
              for r in db.execute('SELECT at,purpose,run_id,kind,row_id,how,score,chars FROM memory_use WHERE suggestion_id=? ORDER BY id', (suggestion_id,))]
    return {'todo': suggestion_id, 'outcome': row[0],
            'edits': db.execute("SELECT count(*) FROM draft_edits WHERE suggestion_id=? AND source!='agent'", (suggestion_id,)).fetchone()[0],
            'decisions': {r[0]: r[1] for r in db.execute('SELECT choice,count(*) FROM decisions WHERE suggestion_id=? GROUP BY choice', (suggestion_id,))},
            'prompts': len({(m['purpose'], m['run']) for m in memory}), 'memory': memory}


def summary(db):
    """Counts only: per kind of memory and per item, in how many prompts of a to-do it was, and how those to-dos
    went. {'kinds': {kind: {'prompts', <each of OUTCOMES>}}, 'items': {(kind, row id): the same}}. A to-do with
    several prompts counts once per prompt."""
    def table(key):
        out = {}
        sql = (f'SELECT {key},o.outcome,count(DISTINCT m.run_id) FROM memory_use m JOIN '
               f'(SELECT s.id,{_OUTCOME} outcome FROM suggestions s WHERE s.id IN (SELECT suggestion_id FROM memory_use)) o '
               f"ON o.id=m.suggestion_id WHERE m.suggestion_id!='' GROUP BY {key},o.outcome")
        for *name, outcome, n in db.execute(sql):
            entry = out.setdefault(name[0] if len(name) == 1 else tuple(name), {'prompts': 0, **{o: 0 for o in OUTCOMES}})
            entry['prompts'] += n
            entry[outcome] += n
        return out
    return {'kinds': table('m.kind'), 'items': table('m.kind,m.row_id')}

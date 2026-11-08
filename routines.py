"""Routines (docs/help/routines.md): work The Machine does on its own, on a rhythm, with its result on the Routines page.

A routine is not a recurring to-do. A recurring to-do (recurring.py) reminds the owner to do something; a routine is
The Machine doing something by itself, like "every Monday at 9, sum up last week's open deals". Only the rhythm math is
shared: a routine's `rule` and `anchor` are recurring.py's (clean_rule, occurrence, next_after, parse), plus a time of
day, `at` ('HH:MM' on the owner's clock).

Each routine runs once per period: a run's key is (routine, period), so a restart, a retry or a second worker never
makes a second result. A scheduled period is its date; Run now is 'now:<stamp>'. Periods missed while the Machine was
off don't stack: only the newest missed one runs. A run reads with the review's read-only tools and ends with one
routine_result (routines_app.py): Ready (a result), Nothing new, or Didn't work. A run that ends without one didn't work.

A routine can also come from an old OpenClaw job (routine_imports.py, origin 'openclaw:<job id>'). Such a row starts as
'sorting': one run reads the job, says whether it fits (a routine, a recurring to-do or neither) and, when it is a
routine, runs it once for real. That run is the preview of a 'suggested' routine, which the owner adds with one tap
('on') or turns down ('stopped'). A sorted job never comes back: its row stays, 'skipped' when it didn't fit. A week
after it was added, a routine from an OpenClaw job that ran well offers to turn the old job off (old_job).

Tables (this module owns them): routines, routine_runs."""
import datetime as dt
import json
import re
import uuid

import recurring

STATES = ('on', 'paused', 'stopped')
LIVE = ('on', 'paused')  # the owner's routines; 'sorting', 'suggested' and 'skipped' come from OpenClaw jobs
SHORT_MAX = 18  # a suggested routine's name: it fits a phone's row next to its status
MAX_SUGGESTED = 3  # open suggestions at a time: the next job is sorted once one is answered
OLD_JOB_AFTER = 7  # days a routine from an OpenClaw job runs before it offers to turn the old job off
RUN_STATES = ('running', 'ready', 'nothing', 'failed')
DEFAULT_AT = '08:00'
NAME_MAX = 80
INSTRUCTIONS_MAX = 2000
RESULT_MAX = 4000
WHY_MAX = 200
HISTORY = 5  # runs a routine shows
KEEP_RUNS = 60  # runs a routine keeps; older ones go
MAX_ROUTINES = 20  # a short list on purpose: each one costs model time


def ensure(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS routines(
        id TEXT PRIMARY KEY,name TEXT NOT NULL,instructions TEXT NOT NULL,rule TEXT NOT NULL,anchor TEXT NOT NULL,
        at TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'on',work INTEGER NOT NULL DEFAULT 0,version INTEGER NOT NULL DEFAULT 1,
        next_due TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS routine_runs(
        id TEXT PRIMARY KEY,routine_id TEXT NOT NULL,period TEXT NOT NULL,version INTEGER NOT NULL,state TEXT NOT NULL,
        result TEXT,why TEXT,error TEXT,started_at TEXT NOT NULL,admitted_at TEXT,finished_at TEXT,UNIQUE(routine_id,period));
      CREATE INDEX IF NOT EXISTS routine_runs_routine ON routine_runs(routine_id,started_at);
    ''')
    have = {r[1] for r in db.execute('PRAGMA table_info(routines)')}
    for column in ('origin', 'accepted_at', 'old_job', 'name_check'):  # added after the first release (#916; name_check: Edit)
        if column not in have:
            db.execute(f'ALTER TABLE routines ADD COLUMN {column} TEXT')


# --- words -------------------------------------------------------------------------------------------------------------

_AT = re.compile(r'\b(?:at|om|à|um|a las|alle|às)\s+(\d{1,2})(?:[:.h](\d{2}))?\s*(am|pm|a\.m\.|p\.m\.|h|uur|uhr)?\b'
                 r'|\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b', re.I)
_PARTS = {'morning': '08:00', 'noon': '12:00', 'afternoon': '14:00', 'evening': '18:00', 'night': '21:00'}
_PART = re.compile(r'\b(?:in the |every |each )?(morning|noon|afternoon|evening|night)\b', re.I)


def clean_at(value):
    """'HH:MM' on a 24-hour clock, or ValueError."""
    m = re.fullmatch(r'(\d{1,2}):(\d{2})', str(value or '').strip())
    if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
        raise ValueError('Pick a time like 9:00')
    return f'{int(m.group(1)):02d}:{m.group(2)}'


def read_at(text):
    """(the time of day in the words as 'HH:MM' or None, the words without it)."""
    s = str(text or '')
    m = _AT.search(s)
    if m:
        hour = int(m.group(1) or m.group(4))
        minute = int(m.group(2) or m.group(5) or 0)
        half = (m.group(3) or m.group(6) or '').lower().replace('.', '')
        if half == 'pm' and hour < 12:
            hour += 12
        elif half == 'am' and hour == 12:
            hour = 0
        if hour <= 23 and minute <= 59:
            return f'{hour:02d}:{minute:02d}', ' '.join((s[:m.start()] + ' ' + s[m.end():]).split())
    m = _PART.search(s)  # "every morning" also says daily: the words stay for the rhythm (read drops what's left)
    return (_PARTS[m.group(1).lower()] if m else None), s


def read(text, today):
    """A routine in the owner's words ("every Monday at 9 sum up last week's open deals"): {'rule', 'anchor', 'at',
    'instructions'}, or ValueError saying what is missing."""
    words = ' '.join(str(text or '').split())
    if not words:
        raise ValueError('Say what it should do and when, like every Monday at 9, sum up my open deals')
    at, rest = read_at(words)
    got = recurring.parse(rest, today)
    if not got:
        raise ValueError('Say when it should run, like every Monday at 9 or every weekday morning')
    instructions = re.sub(r'^(?:(?:in the|on|at) )?(?:morning|noon|afternoon|evening|night)\b|\b(?:in the |at )?(?:morning|noon|afternoon|evening|night)$',
                          '', got['rest'].strip(' ,.;:-'), flags=re.I).strip(' ,.;:-')
    instructions = instructions[:1].upper() + instructions[1:]
    if len(instructions) < 4:
        raise ValueError('Say what it should do, like sum up my open deals')
    return {'rule': got['rule'], 'anchor': got['anchor'], 'at': at or DEFAULT_AT, 'instructions': instructions[:INSTRUCTIONS_MAX]}


def name_of(instructions):
    """A short name from the instructions: their first sentence, at most NAME_MAX characters."""
    first = re.split(r'(?<=[.!?])\s', ' '.join(str(instructions or '').split()), maxsplit=1)[0].rstrip('.!?')
    if len(first) > NAME_MAX:
        first = first[:NAME_MAX - 1].rsplit(' ', 1)[0] + '…'
    return first[:1].upper() + first[1:]


# --- dates -------------------------------------------------------------------------------------------------------------

def first_due(rule, anchor, at, now_local):
    """The routine's first date: its anchor, or the next date of its rhythm when the anchor's time already passed."""
    today = now_local.date()
    if anchor > today or (anchor == today and not _past(now_local, at)):
        return anchor
    day = recurring.next_after(rule, anchor, today - dt.timedelta(days=1))  # its first date from today on
    return recurring.next_after(rule, anchor, today) if day == today and _past(now_local, at) else day


def _past(now_local, at):
    return now_local.strftime('%H:%M') >= at


def due_period(row, now_local):
    """The period a routine runs for now (a date, as 'YYYY-MM-DD'), or None. Missed dates don't stack: the newest one
    that is due runs, once."""
    if row['state'] != 'on' or not row['next_due']:
        return None
    rule, anchor, due = json.loads(row['rule']), dt.date.fromisoformat(row['anchor']), dt.date.fromisoformat(row['next_due'])
    today = now_local.date()
    if due > today or (due == today and not _past(now_local, row['at'])):
        return None
    newest = due
    while True:
        later = recurring.next_after(rule, anchor, newest)
        if later > today or (later == today and not _past(now_local, row['at'])):
            return newest.isoformat()
        newest = later


# --- routines ----------------------------------------------------------------------------------------------------------

def _full(db):
    if db.execute("SELECT count(*) FROM routines WHERE state IN ('on','paused')").fetchone()[0] >= MAX_ROUTINES:
        raise ValueError('You have 20 routines. Stop one before you add another.')


def short_name(text):
    """A name that fits a phone's row: at most SHORT_MAX characters, cut at a word."""
    words = ' '.join(str(text or '').split()).strip(' .,:;-')
    if len(words) > SHORT_MAX:
        words = words[:SHORT_MAX + 1].rsplit(' ', 1)[0] if ' ' in words[:SHORT_MAX + 1] else words[:SHORT_MAX]
    words = words.strip(' .,:;-&')
    return words[:1].upper() + words[1:]


def create(db, instructions, rule, anchor, at, now_local, stamp, name=None, work=False, origin=None, state='on'):
    if state == 'on':
        _full(db)
    rule, at = recurring.clean_rule(rule), clean_at(at)
    anchor = recurring.anchor_for(rule, anchor)  # a weekdays routine never starts on a weekend
    instructions = ' '.join(str(instructions or '').split())[:INSTRUCTIONS_MAX]
    if len(instructions) < 4:
        raise ValueError('Say what it should do, like sum up my open deals')
    rid = uuid.uuid4().hex
    db.execute('INSERT INTO routines(id,name,instructions,rule,anchor,at,state,work,next_due,origin,accepted_at,created_at,updated_at) '
               'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
               (rid, (name or name_of(instructions))[:NAME_MAX], instructions, json.dumps(rule), anchor.isoformat(), at, state,
                int(bool(work)), first_due(rule, anchor, at, now_local).isoformat() if state == 'on' else None, origin,
                stamp if state == 'on' else None, stamp, stamp))
    return rid


def get(db, routine_id, states=LIVE):
    row = db.execute('SELECT * FROM routines WHERE id=?', (str(routine_id or ''),)).fetchone()
    if not row or row['state'] not in states:
        raise ValueError('That routine is gone')
    return row


def change_when(db, routine_id, rule, anchor, at, now_local, stamp):
    row = get(db, routine_id)
    rule, at = recurring.clean_rule(rule), clean_at(at)
    anchor = recurring.anchor_for(rule, anchor)
    db.execute('UPDATE routines SET rule=?,anchor=?,at=?,next_due=?,updated_at=? WHERE id=?',
               (json.dumps(rule), anchor.isoformat(), at, first_due(rule, anchor, at, now_local).isoformat(), stamp, row['id']))


def change_instructions(db, routine_id, instructions, stamp):
    """Edit: what the routine does, in new words. Its rhythm and its runs stay; a name made from the old words follows."""
    row = get(db, routine_id)
    instructions = ' '.join(str(instructions or '').split())[:INSTRUCTIONS_MAX]
    if len(instructions) < 4:
        raise ValueError('Say what it should do, like sum up my open deals')
    placeholder = row['name'] == name_of(row['instructions'])
    name = name_of(instructions) if placeholder else row['name']
    db.execute('UPDATE routines SET name=?,instructions=?,version=version+1,name_check=?,updated_at=? WHERE id=?',
               (name[:NAME_MAX], instructions, None if placeholder else '1', stamp, row['id']))


def needs_name(row):
    """A routine the owner made has the start of its words as a placeholder name until its first run gives it a short
    one (no model call of its own); after Edit, the next run keeps its name unless it no longer fits."""
    return row['name_check'] == '1' or row['name'] == name_of(row['instructions'])


def named(db, routine_id, name, stamp):
    """A run's short name for its routine (routine_result name), taken only when the routine asked for one."""
    row = db.execute('SELECT * FROM routines WHERE id=?', (routine_id,)).fetchone()
    name = short_name(name)
    if row and needs_name(row) and len(name) >= 2:
        db.execute('UPDATE routines SET name=?,name_check=NULL,updated_at=? WHERE id=?', (name, stamp, routine_id))


def set_state(db, routine_id, state, now_local, stamp):
    """Pause, resume ('on') or stop. Resuming starts from the next date, never with what was missed while paused."""
    if state not in STATES:
        raise ValueError('Unknown state')
    row = get(db, routine_id, LIVE + ('suggested',) if state == 'stopped' else LIVE)  # No thanks on a suggestion stops it
    due = row['next_due']
    if state == 'on' and row['state'] != 'on':
        due = first_due(json.loads(row['rule']), dt.date.fromisoformat(row['anchor']), row['at'], now_local).isoformat()
    db.execute('UPDATE routines SET state=?,next_due=?,updated_at=? WHERE id=?', (state, due, stamp, row['id']))


# --- runs --------------------------------------------------------------------------------------------------------------

def running(db):
    """Runs not over yet, oldest first: admitted ones (admitted_at, the Gateway runs their turn) and waiting ones."""
    return db.execute("SELECT r.*,t.name,t.instructions,t.name_check FROM routine_runs r JOIN routines t ON t.id=r.routine_id "
                      "WHERE r.state='running' ORDER BY r.started_at").fetchall()


def begin(db, routine_id, period, stamp, now_local=None):
    """A run for (routine, period), or None when that period has one already (it never runs twice). A scheduled period
    moves the routine's next date past it in the same transaction, never back."""
    row = get(db, routine_id, LIVE + ('sorting',))
    run_id = uuid.uuid4().hex
    made = db.execute('INSERT OR IGNORE INTO routine_runs(id,routine_id,period,version,state,started_at) VALUES(?,?,?,?,?,?)',
                      (run_id, row['id'], period, row['version'], 'running', stamp)).rowcount
    if not period.startswith(('now:', 'sort:')):
        after = dt.date.fromisoformat(period)
        nxt = recurring.next_after(json.loads(row['rule']), dt.date.fromisoformat(row['anchor']), after)
        db.execute('UPDATE routines SET next_due=? WHERE id=? AND (next_due IS NULL OR next_due<?)', (nxt.isoformat(), row['id'], nxt.isoformat()))
    return run_id if made else None


def run_now(db, routine_id, stamp):
    """Run now: one at a time per routine."""
    row = get(db, routine_id)
    if db.execute("SELECT 1 FROM routine_runs WHERE routine_id=? AND state='running'", (row['id'],)).fetchone():
        raise ValueError('It’s running already')
    return begin(db, row['id'], 'now:' + stamp, stamp)


def admitted(db, run_id, stamp):
    db.execute("UPDATE routine_runs SET admitted_at=? WHERE id=? AND state='running'", (stamp, str(run_id)))


def finish(db, run_id, state, stamp, result=None, why=None, error=None):
    """A run's end. Only a running run finishes, once; False when it wasn't running."""
    if state not in RUN_STATES[1:]:
        raise ValueError('Unknown run state')
    done = db.execute("UPDATE routine_runs SET state=?,result=?,why=?,error=?,finished_at=? WHERE id=? AND state='running'",
                      (state, (result or '')[:RESULT_MAX] or None, (why or '')[:WHY_MAX] or None, error, stamp, str(run_id))).rowcount
    if done:
        rid = db.execute('SELECT routine_id FROM routine_runs WHERE id=?', (str(run_id),)).fetchone()[0]
        db.execute('DELETE FROM routine_runs WHERE routine_id=? AND id NOT IN (SELECT id FROM routine_runs WHERE routine_id=? '
                   'ORDER BY started_at DESC LIMIT ?)', (rid, rid, KEEP_RUNS))
    return bool(done)


def report(db, run_id, text=None, nothing=False, why=None, stamp=None):
    """The run's own result (routine_result): its text, or nothing new with why. ValueError when it isn't one."""
    text = str(text or '').strip()
    if not nothing and not text:
        raise ValueError('routine_result needs text (the result), or nothing: true with why')
    if not finish(db, run_id, 'nothing' if nothing else 'ready', stamp, result=None if nothing else text,
                  why=' '.join(str(why or '').split()) if nothing else None):
        raise ValueError('This routine run is over: end the turn')


def last_result(db, routine_id):
    """The newest result of a routine, for its next run to build on."""
    row = db.execute("SELECT result,started_at FROM routine_runs WHERE routine_id=? AND state='ready' ORDER BY started_at DESC LIMIT 1",
                     (routine_id,)).fetchone()
    return dict(row) if row else None


def view(db, states=LIVE):
    """The Routines page: the owner's routines (or the suggestions), with their rhythm and last runs, newest first."""
    out = []
    marks = ','.join('?' * len(states))
    for r in db.execute(f'SELECT * FROM routines WHERE state IN ({marks}) ORDER BY created_at', states).fetchall():
        runs = [dict(x) for x in db.execute('SELECT id,period,state,result,why,error,started_at,finished_at FROM routine_runs '
                                            'WHERE routine_id=? ORDER BY started_at DESC LIMIT ?', (r['id'], HISTORY))]
        out.append({'id': r['id'], 'name': r['name'], 'instructions': r['instructions'], 'rule': json.loads(r['rule']),
                    'anchor': r['anchor'], 'at': r['at'], 'state': r['state'], 'next_due': r['next_due'] if r['state'] == 'on' else None,
                    'origin': r['origin'], 'accepted_at': r['accepted_at'], 'old_job': r['old_job'], 'runs': runs})
    return out


# --- from OpenClaw jobs ------------------------------------------------------------------------------------------------

def sorted_origins(db):
    """Every origin a row was made for, in any state: a job is sorted once."""
    return {r[0] for r in db.execute('SELECT origin FROM routines WHERE origin IS NOT NULL')}


def sorting(db):
    """The row being sorted now, or None (one at a time)."""
    return db.execute("SELECT * FROM routines WHERE state='sorting' ORDER BY created_at LIMIT 1").fetchone()


def open_suggestions(db):
    return db.execute("SELECT count(*) FROM routines WHERE state='suggested'").fetchone()[0]


def start_sorting(db, job, now_local, stamp):
    """A 'sorting' row for an OpenClaw job and its one run: (routine id, run id)."""
    rid = create(db, 'Sort the OpenClaw job ' + job['name'], job['rule'], job['anchor'], job['at'], now_local, stamp,
                 name=short_name(job['name']) or 'OpenClaw job', origin='openclaw:' + job['id'], state='sorting')
    return rid, begin(db, rid, 'sort:' + stamp, stamp)


def sort_again(db, row, stamp):
    """The sorting row's run didn't work: once more, then the job is skipped (its failed runs kept). The new run id or None."""
    failed = db.execute("SELECT count(*) FROM routine_runs WHERE routine_id=? AND state='failed'", (row['id'],)).fetchone()[0]
    if failed >= 2:
        db.execute("UPDATE routines SET state='skipped',updated_at=? WHERE id=?", (stamp, row['id']))
        return None
    return begin(db, row['id'], 'sort:' + stamp, stamp)


def sorted_as(db, run_id, kind, stamp, name=None, instructions=None, text=None, nothing=False, why=None):
    """A sorting run's answer: 'routine' (a suggestion; its result is the preview), 'todo' or 'skip'. The routine's row."""
    run = db.execute("SELECT r.routine_id FROM routine_runs r JOIN routines t ON t.id=r.routine_id WHERE r.id=? AND r.state='running' "
                     "AND t.state='sorting'", (str(run_id),)).fetchone()
    if not run:
        raise ValueError('This routine run is over: end the turn')
    rid = run['routine_id']
    if kind == 'routine':
        name, instructions = short_name(name), ' '.join(str(instructions or '').split())[:INSTRUCTIONS_MAX]
        if len(name) < 2 or len(instructions) < 4:
            raise ValueError('A routine needs name (at most 18 characters) and instructions')
        report(db, run_id, text=text, nothing=nothing, why=why, stamp=stamp)
        db.execute("UPDATE routines SET state='suggested',name=?,instructions=?,updated_at=? WHERE id=?", (name, instructions, stamp, rid))
    else:
        finish(db, run_id, 'nothing', stamp, why=' '.join(str(why or kind).split()))
        db.execute("UPDATE routines SET state='skipped',updated_at=? WHERE id=?", (stamp, rid))
    return db.execute('SELECT * FROM routines WHERE id=?', (rid,)).fetchone()


def accept(db, routine_id, now_local, stamp):
    """Add a suggested routine: it runs on its rhythm from its next date; its preview stays its first result."""
    row = get(db, routine_id, ('suggested',))
    _full(db)
    due = first_due(json.loads(row['rule']), dt.date.fromisoformat(row['anchor']), row['at'], now_local).isoformat()
    db.execute("UPDATE routines SET state='on',next_due=?,accepted_at=?,updated_at=? WHERE id=?", (due, stamp, stamp, row['id']))


def old_job_due(db, row, now_utc):
    """Whether a routine from an OpenClaw job offers to turn the old job off: added a week ago or more, not answered, and
    its last three runs since then all worked (Ready or Nothing new)."""
    if row['state'] != 'on' or not str(row['origin'] or '').startswith('openclaw:') or row['old_job'] or not row['accepted_at']:
        return False
    if now_utc - dt.datetime.fromisoformat(row['accepted_at']) < dt.timedelta(days=OLD_JOB_AFTER):
        return False
    last = [r[0] for r in db.execute("SELECT state FROM routine_runs WHERE routine_id=? AND started_at>=? AND state!='running' "
                                     'ORDER BY started_at DESC LIMIT 3', (row['id'], row['accepted_at']))]
    return len(last) == 3 and all(s in ('ready', 'nothing') for s in last)


def answer_old_job(db, routine_id, choice, stamp):
    """'off' (the caller turned the job off) or 'kept': asked once either way."""
    if choice not in ('off', 'kept'):
        raise ValueError('Unknown choice')
    row = get(db, routine_id)
    db.execute('UPDATE routines SET old_job=?,updated_at=? WHERE id=?', (choice, stamp, row['id']))

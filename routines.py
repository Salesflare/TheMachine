"""Routines (docs/help/routines.md): work The Machine does on its own, on a rhythm, with its result on the Routines page.

A routine is not a recurring to-do. A recurring to-do (recurring.py) reminds the owner to do something; a routine is
The Machine doing something by itself, like "every Monday at 9, sum up last week's open deals". Only the rhythm math is
shared: a routine's `rule` and `anchor` are recurring.py's (clean_rule, occurrence, next_after, parse), plus a time of
day, `at` ('HH:MM' on the owner's clock).

Each routine runs once per period: a run's key is (routine, period), so a restart, a retry or a second worker never
makes a second result. A scheduled period is its date; Run now is 'now:<stamp>'. Periods missed while the Machine was
off don't stack: only the newest missed one runs. A run reads with the review's read-only tools and ends with one
routine_result (routines_app.py): Ready (a result), Nothing new, or Didn't work. A run that ends without one didn't work.
A run may follow the owner's skills that are on (instructions only, skills.py); its result names them (used).

Script steps (the owner's, `steps`): Get data runs a command on the owner's Machine first, and its output (capped,
token-like strings removed) goes to the run as evidence; with no words, that output is the result and no model runs.
Check gets the result on stdin: a nonzero exit means the run didn't work, with what it said. Each run keeps the steps
it ran with. A routine still never sends: a step's output is read, never acted on.

A routine can also come from an old OpenClaw job (routine_imports.py, origin 'openclaw:<job id>'). Such a row starts as
'sorting': one run reads the job, says whether it fits (a routine, a recurring to-do or neither) and, when it is a
routine, runs it once for real. That run is the preview of a 'suggested' routine, which the owner adds with one tap
('on') or turns down ('stopped'). A sorted job never comes back: its row stays, 'skipped' when it didn't fit. A week
after it was added, a routine from an OpenClaw job that ran well offers to turn the old job off (old_job).

A test run (period 'test:<stamp>') shows what a routine would give before it is kept: a new one waits as 'trying'
until Add (accept), and Edit's Try it runs new words (the run's `trial`) without changing the routine. A test run is
dry: it reads like any run, but it is never a routine's result, its next run's "last time" or a reason to rename it,
until Add or Save keeps it.

A suggestion can also come from what the owner does on a rhythm (routine_patterns.py, origin 'pattern:<kind>:<key>'): it
is sorted the same way, with `why` (JSON numbers, like {"kind": "ask", "n": 4}) for the line that says what it saw.

Tables (this module owns them): routines, routine_runs."""
import datetime as dt
import json
import re
import shlex
import uuid

import recurring

STATES = ('on', 'paused', 'stopped')
LIVE = ('on', 'paused')  # the owner's routines; 'sorting', 'suggested' and 'skipped' are suggestions (OpenClaw jobs, patterns); 'trying': a new one on trial
SHORT_MAX = 18  # a suggested routine's name: it fits a phone's row next to its status
MAX_SUGGESTED = 3  # open suggestions at a time: the next job or pattern is sorted once one is answered
OLD_JOB_AFTER = 7  # days a routine from an OpenClaw job runs before it offers to turn the old job off
RUN_STATES = ('running', 'ready', 'nothing', 'failed')
DEFAULT_AT = '08:00'
NAME_MAX = 80
PLACEHOLDER_MAX = 28  # a name made from the words until the first run names it: a card's title line on a phone
INSTRUCTIONS_MAX = 2000
RESULT_MAX = 4000
WHY_MAX = 200
HISTORY = 5  # runs a routine shows
KEEP_RUNS = 60  # runs a routine keeps; older ones go
MAX_ROUTINES = 20  # a short list on purpose: each one costs model time
DATA_MAX = 8000  # characters of Get data's output a run sees
STEP_TIMEOUT = {'get': 60, 'check': 30}  # seconds a step may take unless the owner says, at most STEP_TIMEOUT_MAX
STEP_TIMEOUT_MAX = 600
COMMAND_MAX = 1000


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
    for column in ('origin', 'accepted_at', 'old_job', 'name_check', 'steps', 'why'):  # added after the first release (#916; name_check: Edit; why: patterns)
        if column not in have:
            db.execute(f'ALTER TABLE routines ADD COLUMN {column} TEXT')
    have = {r[1] for r in db.execute('PRAGMA table_info(routine_runs)')}
    for column in ('trial', 'used', 'steps', 'data'):  # trial: Try it's words; used: skills it followed; steps it ran with, data: Get data's output
        if column not in have:
            db.execute(f'ALTER TABLE routine_runs ADD COLUMN {column} TEXT')
    for r in db.execute("SELECT id,name,instructions FROM routines WHERE state!='stopped'").fetchall():  # a long placeholder made before gets short
        short = name_of(r[2])
        if short and r[1] != short and r[1] == _long_name_of(r[2]):
            db.execute('UPDATE routines SET name=? WHERE id=?', (short, r[0]))


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


def _first(instructions):
    return re.split(r'(?<=[.!?])\s', ' '.join(str(instructions or '').split()), maxsplit=1)[0].rstrip('.!?')


def name_of(instructions):
    """A routine's name until its first run gives it one: the start of its first sentence, short enough for a phone's
    row (short_name). The run that names it recognizes it as this placeholder (needs_name)."""
    return short_name(_first(instructions), PLACEHOLDER_MAX)


def _long_name_of(instructions):
    """The placeholder before it was short: the first sentence, at most NAME_MAX characters (names made before)."""
    first = _first(instructions)
    if len(first) > NAME_MAX:
        first = first[:NAME_MAX - 1].rsplit(' ', 1)[0] + '…'
    return first[:1].upper() + first[1:]


def placeholder(row):
    """Its name is still the one made from its words, never one a run or the owner gave it."""
    return row['name'] in (name_of(row['instructions']), _long_name_of(row['instructions']))


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


def short_name(text, most=SHORT_MAX):
    """A name that fits a phone's row: at most SHORT_MAX characters (most), cut at a word."""
    words = ' '.join(str(text or '').split()).strip(' .,:;-')
    if len(words) > most:
        words = words[:most + 1].rsplit(' ', 1)[0] if ' ' in words[:most + 1] else words[:most]
    words = words.strip(' .,:;-&')
    return words[:1].upper() + words[1:]


def clean_steps(steps):
    """The owner's script steps as kept: {'get': {command, cwd, timeout}, 'check': {command, timeout}}, each only when
    it has a command; None for none. A command is one line, split like a shell would (no pipes or variables)."""
    out = {}
    for kind in ('get', 'check'):
        step = (steps or {}).get(kind) if isinstance(steps, dict) else None
        command = ' '.join(str((step or {}).get('command') or '').split())[:COMMAND_MAX] if isinstance(step, dict) else ''
        if not command:
            continue
        try:
            if not shlex.split(command):
                continue
        except ValueError:
            raise ValueError('That command has an open quote') from None
        timeout = step.get('timeout') or STEP_TIMEOUT[kind]
        try:
            timeout = int(timeout)
        except (TypeError, ValueError):
            raise ValueError('Say how long it may take in seconds, like 60') from None
        if not 1 <= timeout <= STEP_TIMEOUT_MAX:
            raise ValueError('A step may take 1 to 600 seconds')
        out[kind] = {'command': command, 'timeout': timeout}
        cwd = ' '.join(str(step.get('cwd') or '').split())[:500]
        if kind == 'get' and cwd:
            out[kind]['cwd'] = cwd
    return out or None


def steps_of(row):
    """A routine's or a run's steps (clean_steps), or {}."""
    try:
        return json.loads(row['steps'] or 'null') or {}
    except (KeyError, IndexError, ValueError):
        return {}


def create(db, instructions, rule, anchor, at, now_local, stamp, name=None, work=False, origin=None, state='on', steps=None, why=None):
    if state in ('on', 'trying'):
        _full(db)
    rule, at = recurring.clean_rule(rule), clean_at(at)
    anchor = recurring.anchor_for(rule, anchor)  # a weekdays routine never starts on a weekend
    steps = clean_steps(steps)
    instructions = _words(instructions, steps)
    rid = uuid.uuid4().hex
    db.execute('INSERT INTO routines(id,name,instructions,rule,anchor,at,state,work,next_due,origin,accepted_at,steps,why,created_at,updated_at) '
               'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
               (rid, (name or name_of(instructions) or 'Get data')[:NAME_MAX], instructions, json.dumps(rule), anchor.isoformat(), at, state,
                int(bool(work)), first_due(rule, anchor, at, now_local).isoformat() if state == 'on' else None, origin,
                stamp if state == 'on' else None, json.dumps(steps) if steps else None,
                json.dumps(why) if why else None, stamp, stamp))
    return rid


def _words(instructions, steps=None):
    """What a routine does, in one line; none only when Get data's output is the result."""
    instructions = ' '.join(str(instructions or '').split())[:INSTRUCTIONS_MAX]
    if len(instructions) < 4 and not (not instructions and (steps or {}).get('get')):
        raise ValueError('Say what it should do, like sum up my open deals')
    return instructions


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


def change_instructions(db, routine_id, instructions, stamp, steps=False):
    """Edit: what the routine does, in new words, and its script steps (False: as they are). Its rhythm and its runs
    stay; a name made from the old words follows."""
    row = get(db, routine_id)
    steps = steps_of(row) if steps is False else clean_steps(steps)
    instructions = _words(instructions, steps)
    made = placeholder(row)
    name = (name_of(instructions) or row['name']) if made else row['name']
    db.execute('UPDATE routines SET name=?,instructions=?,steps=?,version=version+1,name_check=?,updated_at=? WHERE id=?',
               (name[:NAME_MAX], instructions, json.dumps(steps) if steps else None, None if made else '1', stamp, row['id']))


def needs_name(row):
    """A routine the owner made has the start of its words as a placeholder name until its first run gives it a short
    one (no model call of its own); after Edit, the next run keeps its name unless it no longer fits."""
    return row['name_check'] == '1' or placeholder(row)


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
    trying = db.execute("SELECT id FROM routines WHERE id=? AND state='trying'", (str(routine_id or ''),)).fetchone()
    if trying and state == 'stopped':  # Cancel on a new one's test run: it was never kept
        return _drop(db, trying['id'])
    row = get(db, routine_id, LIVE + ('suggested',) if state == 'stopped' else LIVE)  # No thanks on a suggestion stops it
    due = row['next_due']
    if state == 'on' and row['state'] != 'on':
        due = first_due(json.loads(row['rule']), dt.date.fromisoformat(row['anchor']), row['at'], now_local).isoformat()
    db.execute('UPDATE routines SET state=?,next_due=?,updated_at=? WHERE id=?', (state, due, stamp, row['id']))


# --- runs --------------------------------------------------------------------------------------------------------------

def running(db):
    """Runs not over yet, oldest first: admitted ones (admitted_at, the Gateway runs their turn) and waiting ones."""
    return db.execute("SELECT r.*,t.name,t.instructions,t.name_check,t.state AS routine_state FROM routine_runs r "
                      "JOIN routines t ON t.id=r.routine_id WHERE r.state='running' ORDER BY r.started_at").fetchall()


def begin(db, routine_id, period, stamp, now_local=None):
    """A run for (routine, period), or None when that period has one already (it never runs twice). A scheduled period
    moves the routine's next date past it in the same transaction, never back."""
    row = get(db, routine_id, LIVE + ('sorting', 'trying'))
    run_id = uuid.uuid4().hex
    made = db.execute('INSERT OR IGNORE INTO routine_runs(id,routine_id,period,version,state,started_at,steps) VALUES(?,?,?,?,?,?,?)',
                      (run_id, row['id'], period, row['version'], 'running', stamp, row['steps'])).rowcount
    if not period.startswith(('now:', 'sort:', 'test:')):
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


# --- test runs (dry: shown, never kept until Add or Save) ----------------------------------------------------------------

def is_test(run):
    return str(run['period']).startswith('test:')


def _drop(db, routine_id):
    db.execute('DELETE FROM routine_runs WHERE routine_id=?', (routine_id,))
    db.execute("DELETE FROM routines WHERE id=? AND state='trying'", (routine_id,))


def try_new(db, instructions, rule, anchor, at, now_local, stamp, steps=None):
    """Add on the page: a new routine's test run first. It waits as 'trying' (one at a time) until Add or Cancel."""
    for old in db.execute("SELECT id FROM routines WHERE state='trying'").fetchall():
        _drop(db, old['id'])
    rid = create(db, instructions, rule, anchor, at, now_local, stamp, state='trying', steps=steps)
    return rid, begin(db, rid, 'test:' + stamp, stamp)


def try_words(db, routine_id, instructions, stamp, steps=False):
    """Try it: a test run of new words (and script steps; False: as they are), one per press. A new one's ('trying')
    change with it; a kept routine's stay as they are, the words and steps go with the run (trial) until Save."""
    row = get(db, routine_id, LIVE + ('trying',))
    steps = steps_of(row) if steps is False else clean_steps(steps)
    instructions = _words(instructions, steps)
    kept = json.dumps(steps) if steps else None
    if db.execute("SELECT 1 FROM routine_runs WHERE routine_id=? AND state='running'", (row['id'],)).fetchone():
        raise ValueError('It’s running already')
    db.execute("DELETE FROM routine_runs WHERE routine_id=? AND period LIKE 'test:%'", (row['id'],))  # only the newest try shows
    if row['state'] == 'trying':
        db.execute('UPDATE routines SET name=?,instructions=?,steps=?,updated_at=? WHERE id=?',
                   ((name_of(instructions) or row['name'])[:NAME_MAX], instructions, kept, stamp, row['id']))
        return begin(db, row['id'], 'test:' + stamp, stamp)
    run_id = uuid.uuid4().hex
    db.execute("INSERT INTO routine_runs(id,routine_id,period,version,state,started_at,trial,steps) VALUES(?,?,?,?,'running',?,?,?)",
               (run_id, row['id'], 'test:' + stamp, row['version'], stamp, instructions, kept))
    return run_id


def keep_test(db, routine_id, saved=None):
    """Add or Save: a test run of what is kept (saved: the routine's row after Save) becomes its newest result; any
    other test run goes."""
    for run in db.execute("SELECT id,trial,steps FROM routine_runs WHERE routine_id=? AND period LIKE 'test:%'", (routine_id,)).fetchall():
        if saved is None or (run['trial'] == saved['instructions'] and steps_of(run) == steps_of(saved)):
            db.execute("UPDATE routine_runs SET period='now:'||substr(period,6),trial=NULL WHERE id=?", (run['id'],))
        else:
            db.execute('DELETE FROM routine_runs WHERE id=?', (run['id'],))


def admitted(db, run_id, stamp):
    db.execute("UPDATE routine_runs SET admitted_at=? WHERE id=? AND state='running'", (stamp, str(run_id)))


def got_data(db, run_id, data):
    """Get data's output for a run that is still running: what its turn reads."""
    db.execute("UPDATE routine_runs SET data=? WHERE id=? AND state='running'", (str(data)[:DATA_MAX], str(run_id)))


def hold(db, run_id, text=None, nothing=False, why=None, used=None):
    """A result waiting for its Check: kept on the run, which stays running until the check finishes it."""
    text = str(text or '').strip()
    if not nothing and not text:
        raise ValueError('routine_result needs text (the result), or nothing: true with why')
    done = db.execute("UPDATE routine_runs SET result=?,why=?,used=? WHERE id=? AND state='running' AND result IS NULL AND why IS NULL",
                      (None if nothing else text[:RESULT_MAX], ' '.join(str(why or '').split())[:WHY_MAX] if nothing else None,
                       json.dumps(list(used)) if used else None, str(run_id))).rowcount
    if not done:
        raise ValueError('This routine run is over: end the turn')


def finish(db, run_id, state, stamp, result=None, why=None, error=None, used=None):
    """A run's end. Only a running run finishes, once; False when it wasn't running."""
    if state not in RUN_STATES[1:]:
        raise ValueError('Unknown run state')
    done = db.execute("UPDATE routine_runs SET state=?,result=?,why=?,error=?,used=?,finished_at=? WHERE id=? AND state='running'",
                      (state, (result or '')[:RESULT_MAX] or None, (why or '')[:WHY_MAX] or None, error,
                       json.dumps(list(used)) if used else None, stamp, str(run_id))).rowcount
    if done:
        rid = db.execute('SELECT routine_id FROM routine_runs WHERE id=?', (str(run_id),)).fetchone()[0]
        db.execute('DELETE FROM routine_runs WHERE routine_id=? AND id NOT IN (SELECT id FROM routine_runs WHERE routine_id=? '
                   'ORDER BY started_at DESC LIMIT ?)', (rid, rid, KEEP_RUNS))
    return bool(done)


def report(db, run_id, text=None, nothing=False, why=None, stamp=None, used=None):
    """The run's own result (routine_result): its text, or nothing new with why, and the skills it followed (used,
    names). ValueError when it isn't one."""
    text = str(text or '').strip()
    if not nothing and not text:
        raise ValueError('routine_result needs text (the result), or nothing: true with why')
    if not finish(db, run_id, 'nothing' if nothing else 'ready', stamp, result=None if nothing else text,
                  why=' '.join(str(why or '').split()) if nothing else None, used=used):
        raise ValueError('This routine run is over: end the turn')


def held(db, run_id):
    """A run whose result waits for its Check (hold), or None."""
    return db.execute("SELECT * FROM routine_runs WHERE id=? AND state='running' AND (result IS NOT NULL OR why IS NOT NULL)",
                      (str(run_id),)).fetchone()


def last_result(db, routine_id):
    """The newest result of a routine, for its next run to build on."""
    row = db.execute("SELECT result,started_at FROM routine_runs WHERE routine_id=? AND state='ready' AND period NOT LIKE 'test:%' "
                     'ORDER BY started_at DESC LIMIT 1',
                     (routine_id,)).fetchone()
    return dict(row) if row else None


def view(db, states=LIVE):
    """The Routines page: the owner's routines (or the suggestions), with their rhythm and last runs, newest first."""
    out = []
    marks = ','.join('?' * len(states))
    for r in db.execute(f'SELECT * FROM routines WHERE state IN ({marks}) ORDER BY created_at', states).fetchall():
        runs = [dict(x) for x in db.execute('SELECT id,period,state,result,why,error,started_at,finished_at,trial,used,steps FROM routine_runs '
                                            'WHERE routine_id=? ORDER BY started_at DESC LIMIT ?', (r['id'], HISTORY + 1))]
        for x in runs:
            x['used'] = json.loads(x['used']) if x['used'] else []
            x['got'] = bool(steps_of(x).get('get'))  # Get data ran (or runs) for it
            x['steps'] = steps_of(x) if x['trial'] is not None else None
            if x['state'] == 'running':  # a result waiting for its Check shows when the check is done
                x['result'] = x['why'] = None
        test = next((x for x in runs if is_test(x)), None)  # a test run is shown on its own, never as a result
        runs = [x for x in runs if not is_test(x)][:HISTORY]
        out.append({'id': r['id'], 'name': r['name'], 'instructions': r['instructions'], 'rule': json.loads(r['rule']),
                    'anchor': r['anchor'], 'at': r['at'], 'state': r['state'], 'next_due': r['next_due'] if r['state'] == 'on' else None,
                    'origin': r['origin'], 'accepted_at': r['accepted_at'], 'old_job': r['old_job'], 'runs': runs, 'test': test,
                    'why': json.loads(r['why']) if r['why'] else None,
                    'steps': steps_of(r)})
    return out


# --- suggestions: from OpenClaw jobs and from patterns -----------------------------------------------------------------

def sorted_origins(db):
    """Every origin a row was made for, in any state: a job is sorted once."""
    return {r[0] for r in db.execute('SELECT origin FROM routines WHERE origin IS NOT NULL')}


def sorting(db):
    """The row being sorted now, or None (one at a time)."""
    return db.execute("SELECT * FROM routines WHERE state='sorting' ORDER BY created_at LIMIT 1").fetchone()


def open_suggestions(db):
    return db.execute("SELECT count(*) FROM routines WHERE state='suggested'").fetchone()[0]


def start_sorting(db, job, now_local, stamp):
    """A 'sorting' row for an OpenClaw job (with its script as Get data, when it has one) and its one run: (routine
    id, run id)."""
    rid = create(db, 'Sort the OpenClaw job ' + job['name'], job['rule'], job['anchor'], job['at'], now_local, stamp,
                 name=short_name(job['name']) or 'OpenClaw job', origin='openclaw:' + job['id'], state='sorting', steps=job.get('steps'))
    return rid, begin(db, rid, 'sort:' + stamp, stamp)


def start_pattern(db, found, now_local, stamp):
    """A 'sorting' row for a pattern in the owner's activity (routine_patterns.candidates) and its one run."""
    rid = create(db, 'Sort a pattern: ' + found['name'], found['rule'], found['anchor'], found['at'], now_local, stamp,
                 name=short_name(found['name']) or 'Pattern', origin=found['key'], state='sorting', why=found['why'])
    return rid, begin(db, rid, 'sort:' + stamp, stamp)


def last_pattern_at(db):
    """When the last pattern was handed to a sorting run (its row's created_at), or None."""
    return db.execute("SELECT max(created_at) FROM routines WHERE origin LIKE 'pattern:%'").fetchone()[0]


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
        scripted = not instructions and steps_of(db.execute('SELECT steps FROM routines WHERE id=?', (rid,)).fetchone()).get('get')
        if len(name) < 2 or (len(instructions) < 4 and not scripted):
            raise ValueError('A routine needs name (at most 18 characters) and instructions')
        report(db, run_id, text=text, nothing=nothing, why=why, stamp=stamp)
        db.execute("UPDATE routines SET state='suggested',name=?,instructions=?,updated_at=? WHERE id=?", (name, instructions, stamp, rid))
    else:
        finish(db, run_id, 'nothing', stamp, why=' '.join(str(why or kind).split()))
        db.execute("UPDATE routines SET state='skipped',updated_at=? WHERE id=?", (stamp, rid))
    return db.execute('SELECT * FROM routines WHERE id=?', (rid,)).fetchone()


def accept(db, routine_id, now_local, stamp):
    """Add a suggested routine, or a new one after its test run: it runs on its rhythm from its next date; its preview
    (or test run) stays its first result."""
    row = get(db, routine_id, ('suggested', 'trying'))
    _full(db)
    keep_test(db, row['id'])
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

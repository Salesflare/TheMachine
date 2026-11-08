"""OpenClaw jobs as routine suggestions (docs/help/routines.md): read-only.

Someone who used OpenClaw's own scheduled jobs before The Machine has work on a rhythm there already. This reads those
jobs from OpenClaw's state database (opened read-only, never written) so each one that fits can come back as a routine
suggestion with a real preview run (routines_app.py). Only jobs that are on, that run a model turn and that run at most
once a day qualify; OpenClaw's own upkeep (jobs a plugin manages, the heartbeat) never does. What a job's prompt says,
including corrections added to it later, is the run's to read and fold into one definition.

A job that runs a script comes with it as the routine's Get data step (routines.py steps): one whose prompt says to run
exactly a command ("Run exactly: python3 …"), or one that reads what a separate command job collected before it (a
collector and model pair: its prompt names the command job by id or name). A command with a token-like argument never
comes along.

Nothing here changes OpenClaw. Turning an old job off happens only on the owner's tap (openclaw-cron-off.mjs)."""
import contextlib
import datetime as dt
import json
import os
import re
import shlex
import sqlite3
from pathlib import Path

import recurring

PROMPT_MAX = 12000  # what a run sees of a job's prompt: its start and its end, where later corrections go
# Token-like strings never reach a run: keys, bearer tokens, long opaque strings
TOKEN = re.compile(r'\b(?:sk|pk|rk|ghp|gho|github_pat|xox[a-z])[-_][A-Za-z0-9_-]{8,}|Bearer\s+\S+|\b[A-Za-z0-9_\-+/=]{40,}', re.I)
DAY_MS = 86_400_000
# "Run exactly: python3 /path/x.py", "Run exactly once: …", "Run exactly this command from `/dir` using exec: …", "Run via exec: `…`"
RUN_EXACTLY = re.compile(r'\bRun (?:exactly|via exec)\b[^:\n]{0,120}:\s*`?((?:python3?|node|bash|sh)\s+[^\s`]+(?:\s+-{1,2}[\w-]+(?:[= ](?!-)[^\s`]+)?)*)`?')
WORKDIR = re.compile(r'(?:Working directory:\s*|\bfrom\s+)`?(/[^\s`]+|~[^\s`]*)`?')


def state_path(config):
    """OpenClaw's state database: the config's openclaw_state, else under OPENCLAW_STATE_DIR or ~/.openclaw."""
    if config.get('openclaw_state'):
        return Path(config['openclaw_state']).expanduser()
    root = os.environ.get('OPENCLAW_STATE_DIR', '').strip()
    return (Path(root).expanduser() if root else Path.home() / '.openclaw') / 'state/openclaw.sqlite'


def scrub(text):
    return TOKEN.sub('[removed]', str(text or ''))


def prompt_of(job):
    """A job's prompt for the run, token-like strings removed; a long one keeps its start and its end."""
    payload = job.get('payload') or {}
    text = scrub(' '.join(str(payload.get('message') or payload.get('text') or payload.get('prompt') or '').split()))
    if len(text) > PROMPT_MAX:
        text = text[:PROMPT_MAX // 3] + ' […] ' + text[-(PROMPT_MAX * 2 // 3):]
    return text


def safe_command(argv):
    """An OpenClaw command as one line for Get data, or None when an argument looks like a key or token (a path is fine)."""
    argv = [str(a) for a in argv or []]
    if not argv or any(not re.fullmatch(r'[\w./~:=@,+-]+', a) and TOKEN.search(a) or
                       '/' not in a and TOKEN.search(a) for a in argv):
        return None
    return shlex.join(argv)[:1000]


def script_of(message):
    """Get data from a job's raw prompt that says to run exactly a command, else None."""
    m = RUN_EXACTLY.search(str(message or ''))
    if not m:
        return None
    try:
        command = safe_command(shlex.split(m.group(1)))
    except ValueError:
        return None
    if not command:
        return None
    where = WORKDIR.search(str(message))
    return {'command': command, **({'cwd': where.group(1)} if where else {}), 'timeout': 300}


def _collector(message, commands):
    """The command job a model job reads the output of (named by its id's start or its name), as Get data."""
    text = str(message or '')
    for c in commands:
        if c['id'][:8] in text or (len(c['name']) >= 6 and c['name'] in text):
            command = safe_command(c['argv'])
            if command:
                return {'command': command, **({'cwd': c['cwd']} if c['cwd'] else {}), 'timeout': c['timeout']}
    return None


def _dow(field):
    """Cron's days of the week as Python weekdays (Monday 0), or None when it isn't a plain list or range."""
    days = set()
    for part in field.split(','):
        m = re.fullmatch(r'(\d)(?:-(\d))?', part)
        if not m:
            return None
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        if a > b or b > 7:
            return None
        days |= {(d - 1) % 7 for d in range(a, b + 1)}
    return days


def rhythm(schedule, today, tz=None):
    """A job's schedule as a routine's rhythm: (rule, anchor, at), or None when it runs more than once a day or in a
    way a routine can't. Two days a week becomes weekly on the first; three or more weekdays become weekdays."""
    schedule = schedule or {}
    if schedule.get('kind') == 'cron':
        fields = str(schedule.get('expr') or '').split()
        if len(fields) != 5 or not fields[0].isdigit() or not fields[1].isdigit() or fields[3] != '*':
            return None
        minute, hour, dom, dow = int(fields[0]), int(fields[1]), fields[2], fields[4]
        if minute > 59 or hour > 23:
            return None
        at = f'{hour:02d}:{minute:02d}'
        if dom == '*' and dow == '*':
            rule = {'unit': 'day', 'n': 1}
            return rule, recurring.anchor_for(rule, today), at
        if dom == '*':
            days = _dow(dow)
            if not days:
                return None
            if len(days) == 7:
                rule = {'unit': 'day', 'n': 1}
                return rule, recurring.anchor_for(rule, today), at
            if len(days) >= 3 and days <= {0, 1, 2, 3, 4}:
                rule = {'unit': 'weekday', 'n': 1}
                return rule, recurring.anchor_for(rule, today), at
            if len(days) >= 3:
                return None
            rule = {'unit': 'week', 'n': 1}
            return rule, recurring.anchor_for(rule, today, weekday=min(days)), at
        if dow == '*' and dom.isdigit() and 1 <= int(dom) <= 31:
            rule = {'unit': 'month', 'n': 1}
            return rule, recurring.anchor_for(rule, today, monthday=int(dom)), at
        return None
    if schedule.get('kind') == 'every':
        every, anchor_ms = schedule.get('everyMs'), schedule.get('anchorMs') or 0
        if not isinstance(every, int) or every < DAY_MS or every % DAY_MS:
            return None
        days = every // DAY_MS
        if days % 7 == 0 and days // 7 <= recurring.N_MAX:
            rule = {'unit': 'week', 'n': days // 7}
        elif days <= recurring.N_MAX:
            rule = {'unit': 'day', 'n': days}
        elif round(days / 30.44) <= recurring.N_MAX:
            rule = {'unit': 'month', 'n': max(1, round(days / 30.44))}
        else:
            return None
        start = dt.datetime.fromtimestamp(anchor_ms / 1000, tz or dt.timezone.utc)
        step = dt.timedelta(milliseconds=every)
        now = dt.datetime.combine(today, dt.time(), start.tzinfo)
        if start < now:
            start += step * -(-(now - start) // step)  # its next time from today on
        if rule['unit'] == 'month':
            anchor = recurring.anchor_for(rule, start.date(), monthday=start.day)
        else:
            anchor = start.date()
        return rule, anchor, start.strftime('%H:%M')
    return None


def jobs(config, today, tz=None):
    """The OpenClaw jobs that could be routines, in OpenClaw's own order: [{'id', 'name', 'prompt', 'rule', 'anchor',
    'at'}]. Empty when there is no OpenClaw state to read."""
    path = state_path(config)
    if not path.is_file():
        return []
    try:
        with contextlib.closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=2)) as db:
            rows = db.execute("SELECT job_id,name,description,job_json FROM cron_jobs WHERE enabled=1 AND payload_kind='agentTurn' "
                              'ORDER BY sort_order').fetchall()
            commands = db.execute("SELECT job_id,name,job_json FROM cron_jobs WHERE enabled=1 AND payload_kind='command'").fetchall()
    except sqlite3.Error:
        return []
    collectors = []
    for job_id, name, job_json in commands:
        try:
            payload = json.loads(job_json or '{}').get('payload') or {}
        except ValueError:
            continue
        if isinstance(payload.get('argv'), list) and len(str(job_id or '')) >= 8:
            timeout = payload.get('timeoutSeconds')
            collectors.append({'id': str(job_id), 'name': str(name or ''), 'argv': payload['argv'], 'cwd': str(payload.get('cwd') or ''),
                               'timeout': min(int(timeout), 600) if isinstance(timeout, int) and timeout > 0 else 300})
    out = []
    for job_id, name, description, job_json in rows:
        about = str(description or '')
        if about.startswith('[managed-by=') or re.search(r'\bINACTIVE\b', about):
            continue  # a plugin's own upkeep, or a job its owner marked as no longer in use
        try:
            job = json.loads(job_json or '{}')
        except ValueError:
            continue
        got = rhythm(job.get('schedule'), today, tz)
        prompt = prompt_of(job)
        if not got or len(prompt) < 20 or not re.fullmatch(r'[A-Za-z0-9-]{8,64}', str(job_id or '')):
            continue
        rule, anchor, at = got
        raw = (job.get('payload') or {}).get('message') or ''
        get = script_of(raw) or _collector(raw, collectors)
        out.append({'id': job_id, 'name': scrub(' '.join(str(name or '').split()))[:120], 'prompt': prompt,
                    'rule': rule, 'anchor': anchor, 'at': at, **({'steps': {'get': get}} if get else {})})
    return out


def still_on(config, job_id):
    """Whether an OpenClaw job is still there and on (read-only)."""
    path = state_path(config)
    try:
        with contextlib.closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=2)) as db:
            row = db.execute('SELECT enabled FROM cron_jobs WHERE job_id=?', (str(job_id),)).fetchone()
    except sqlite3.Error:
        return False
    return bool(row and row[0])

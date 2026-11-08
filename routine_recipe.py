"""A routine's recipe (docs/help/routines.md): the reading part of a routine that is the same every run, written by
The Machine itself, never by the owner. A run's turn passes `recipe` with its routine_result when what it read could
be read the same way next time (routines_app.py); from then on the Machine reads it before the turn, in plain code,
and the turn only judges and writes. Fewer tool calls, fewer tokens, the same reads every time.

A recipe only reads, under the same rules as a routine's own turn (openclaw-plugin/review-recovery.ts, routineRead):
- events: the Machine's own signals (mail, calendar, chats), as assistant_signals events reads them: a query, kinds,
  how far back (since_days, or since the last run) and, for what is coming, how far ahead (until_days).
- command: one gh or git command that only reads (the same list as routineShellRead), run without a shell. Dates in
  it are filled in by the Machine at each run: {since} (the last run, else a day ago), {today}, {days_ago:N},
  {days_ahead:N}, all as YYYY-MM-DD.
Every run checks the recipe again (clean) before it runs a step. A step that fails, or a recipe that no longer passes,
hands the reading back to the turn, which repairs the recipe; after REPAIR_TRIES runs without a repair it goes.
"""
import datetime as dt
import json
import re

STEPS_MAX = 4
QUERY_MAX = 200
ARG_MAX = 300
ARGS_MAX = 40
DAYS_MAX = 90
LIMIT_MAX = 40
TIMEOUT = 60  # seconds a command step may take
DATA_MAX = 12000  # characters of what a recipe read that a run sees
REPAIR_TRIES = 3  # runs in a row a recipe may fail before it goes
KIND = re.compile(r'^[a-z_]+\.[a-z_]+$')
PLACEHOLDER = re.compile(r'\{(since|today|days_ago:\d{1,2}|days_ahead:\d{1,2})\}')

# The same reads as routineShellRead (openclaw-plugin/review-recovery.ts), a little narrower: no ls-remote (its
# --upload-pack runs a program) and no option that names a program, a config or an output file.
GH_READS = re.compile(r'^(?:pr (?:list|view|diff|checks|status)|issue (?:list|view|status)|release (?:list|view)|run (?:list|view)|repo view|search \S+|api)$')
GIT_READS = {'log', 'show', 'diff', 'status', 'shortlog', 'rev-parse', 'describe'}
NEVER = re.compile(r'^(?:--output\b|--web$|-w$|--ext-diff$|--textconv$|--upload-pack|--receive-pack|--exec|--config|-c$|--git-dir|--work-tree|-o$)')


def shell_read(argv):
    """True when argv is one gh or git command that only reads."""
    if not argv or any(not isinstance(a, str) for a in argv):
        return False
    tool, args = argv[0], argv[1:]
    if any(re.fullmatch(r'[<>|;&]+', a) or '\n' in a or '`' in a or '$(' in a or NEVER.match(a) for a in args):
        return False
    if tool == 'git':
        rest = args[2:] if args[:1] == ['-C'] else args
        return bool(rest) and rest[0] in GIT_READS
    if tool != 'gh':
        return False
    verb = 'api' if args[:1] == ['api'] else ' '.join(args[:2])
    if not GH_READS.match(verb):
        return False
    if verb != 'api':
        return True
    for i, a in enumerate(args[1:], 1):
        if re.match(r'^(?:-f|-F|--field|--raw-field|--input)(?:=|$)', a) or re.match(r'^-[fF].', a):
            return False
        method = re.match(r'^(?:-X|--method)(?:=(.*))?$', a) or re.match(r'^-X(.+)$', a)
        if method and str(method.group(1) if method.group(1) is not None else (args[i + 1] if i + 1 < len(args) else '')).upper() != 'GET':
            return False
    return not any(a.lower() == 'graphql' for a in args[1:])


def _days(value, name):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= DAYS_MAX:
        raise ValueError(f'{name} is a whole number of days, 0 to {DAYS_MAX}')
    return value


def clean(recipe):
    """The recipe as kept: {'steps': [...]}, each step checked; ValueError says what doesn't pass."""
    steps = recipe.get('steps') if isinstance(recipe, dict) else recipe
    if not isinstance(steps, list) or not 1 <= len(steps) <= STEPS_MAX:
        raise ValueError(f'A recipe is 1 to {STEPS_MAX} steps')
    out = []
    for step in steps:
        if not isinstance(step, dict):
            raise ValueError('Each step is an object')
        if step.get('events') is not None or step.get('kind') == 'events':
            e = step.get('events') if isinstance(step.get('events'), dict) else step
            kinds = e.get('kinds') or []
            if not isinstance(kinds, list) or not all(isinstance(k, str) and KIND.match(k) for k in kinds):
                raise ValueError('kinds is a list of event kinds, like gmail.message or calendar.event')
            query = ' '.join(str(e.get('query') or '').split())[:QUERY_MAX]
            limit = e.get('limit', 20)
            if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= LIMIT_MAX:
                raise ValueError(f'limit is 1 to {LIMIT_MAX}')
            clean_step = {'events': {'query': query, 'kinds': kinds[:8], 'limit': limit}}
            for key in ('since_days', 'until_days'):
                if _days(e.get(key), key) is not None:
                    clean_step['events'][key] = e[key]
            out.append(clean_step)
        elif step.get('command') is not None:
            argv = step['command']
            if not isinstance(argv, list) or not 1 <= len(argv) <= ARGS_MAX or any(not isinstance(a, str) or len(a) > ARG_MAX for a in argv):
                raise ValueError(f'command is a list of words (argv), at most {ARGS_MAX}')
            if '{' in ' '.join(PLACEHOLDER.sub('', a) for a in argv):
                raise ValueError('Only {since}, {today}, {days_ago:N} and {days_ahead:N} are filled in')
            if not shell_read(argv):
                raise ValueError('A command step is one gh or git command that only reads')
            out.append({'command': list(argv)})
        else:
            raise ValueError('Each step is events or command')
    return {'steps': out}


def of(row):
    """A routine's recipe (clean), or None when it has none or it no longer passes."""
    try:
        return clean(json.loads(row['recipe'])) if row['recipe'] else None
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def dates(now, since):
    """The dates a command's placeholders take: since is the last good run's start (aware), else a day ago."""
    start = since or now - dt.timedelta(days=1)
    return {'since': start.date().isoformat(), 'today': now.date().isoformat()}


def fill(argv, now, since):
    known = dates(now, since)

    def one(m):
        key = m.group(1)
        if ':' in key:
            kind, n = key.split(':')
            return (now + dt.timedelta(days=int(n) * (1 if kind == 'days_ahead' else -1))).date().isoformat()
        return known[key]
    return [PLACEHOLDER.sub(one, a) for a in argv]


def window(step, now, since):
    """(since, until) of an events step as UTC ISO stamps: since_days back (else the last run, else a day ago);
    until_days ahead, or None."""
    e = step['events']
    start = now - dt.timedelta(days=e['since_days']) if 'since_days' in e else since or now - dt.timedelta(days=1)
    if 'since_days' in e and e['since_days'] == 0:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    until = None
    if 'until_days' in e:
        until = (now + dt.timedelta(days=e['until_days'])).replace(hour=23, minute=59, second=59, microsecond=0)
    utc = dt.timezone.utc
    return start.astimezone(utc).isoformat(), until.astimezone(utc).isoformat() if until else None


def describe(step):
    """One line a person can read for a step (the Advanced view shows the recipe as it runs)."""
    if 'command' in step:
        return ' '.join(step['command'])
    e = step['events']
    parts = [f'query={json.dumps(e["query"], ensure_ascii=False)}'] if e['query'] else []
    parts += [f'kinds={",".join(e["kinds"])}'] if e['kinds'] else []
    parts += [f'{k}={e[k]}' for k in ('since_days', 'until_days') if k in e] + [f'limit={e["limit"]}']
    return 'events ' + ' '.join(parts)


PROMPT = ('If the reading part of this routine is the same every run, also pass recipe: {steps: [...]} so the Machine '
          'reads it itself next time, before the run, and you only judge and write. Each step is either {events: {query '
          '(words every match contains; empty for all of those kinds), kinds (like ["gmail.message"] or ["calendar.event"]), '
          'limit (1-40), since_days (0: from the start of today; left out: since the last run), until_days (for what is '
          'coming; 0: the end of today)}} or {command: ["gh", ...] or ["git", ...]} that only reads, as an argv list. Dates '
          'in a command are filled in each run: {since}, {today}, {days_ago:N}, {days_ahead:N}. Only the reads this run '
          'needed and would make the same way again, as few steps as do it; leave recipe out when they differ each time.')

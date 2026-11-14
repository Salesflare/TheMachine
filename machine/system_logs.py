"""The computer's own logs: journald and systemd-coredump, read so The Machine can explain and fix problems on the
computer it runs on.

Read-only and local. It reads `journalctl --user` for the owner's own user session and units (their own journal, never
the system one, never with sudo), and `coredumpctl` only when that journal has no crash records. Only structured
fields are read: which unit, how it ended, how often it restarted, and for a crash the program's name, its signal and
whether it was a browser's helper process. Never message text, so no log line is kept, shown or sent. Volume and time
are capped (MAX_ENTRIES over WINDOW, short timeouts) and the service reads at most every EVERY.

Owner decision (October 10, 2026), kept here as for the Gateway source: routine restarts and noise stay silent. Only
real problems surface (detect): a unit that keeps restarting (LOOP_RESTARTS within an hour), one systemd gave up on
(start-limit-hit), one that ran out of memory, one that failed REPEAT_FAILURES times in a day and has not run well since
(a unit whose failed runs were followed by a run that finished well is fine again: recovered), one that stays failed,
and a program that crashed: all its crash dumps over WINDOW make one finding with their count and time span. A
browser's helper processes and browsers a program drives (headless, Playwright, Puppeteer, CI, remote debugging with a
throwaway profile) are not the owner's programs and stay quiet (automated), and so do developer, test and coding-agent
runs: what an agent's service ran, a test runner, a program run from a temporary or cache folder (dev_run). So does
anything that ended while a service it belongs to was being stopped or restarted (stopping): the service took it down,
as a deliberate restart of the OpenClaw Gateway does with its browser. A script's crash is named by the script, not
its interpreter (script_of). On Omarchy it also reads Hyprland (its crashes and the errors it reports in its
settings) and the bar, with fixes in Omarchy's own commands.

Each finding has a plain cause and a suggested fix (card). The service turns new ones into to-dos through the Machine
health source (Store.system_log_cards): one per problem, deduped and rate-limited, and nothing on the computer changes
unless the owner asks in the to-do and approves the step (Do it). `assistant doctor` lists them too (doctor_lines),
scrubbed the way learnings are, since a bug report carries the doctor's output.

macOS, Windows, WSL without systemd and other computers without journald: supported() says why not and nothing is read."""
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import i18n
import locale_prefs
from timeutil import local_tz
import timeutil

WINDOW = dt.timedelta(hours=24)
EVERY = dt.timedelta(minutes=30)  # the service reads at most this often
MAX_ENTRIES = 3000  # newest records over WINDOW; enough for a day of a busy desktop
TIMEOUT = 20
LOOP_RESTARTS = 5  # restarts within LOOP_WINDOW that make a crash loop; fewer are routine and stay silent
LOOP_WINDOW = dt.timedelta(hours=1)
REPEAT_FAILURES = 3  # failed runs within WINDOW
FAILED_FOR = dt.timedelta(hours=1)  # a unit still failed this long after it last failed "stays failed"
QUIET = dt.timedelta(days=14)  # the same problem brings a to-do at most once in this time
PER_DAY = 2  # new to-dos a day at most

# systemd's catalog ids (sd-messages.h): a restart was scheduled, a unit ended with a result, a process dumped core
RESTARTED = '5eb03494b6584870a536b337290809b3'
RESULT = 'd9b373ed55a64feb8242e02dbe79a49c'
COREDUMP = 'fc2e22bc6ee647b6b90729ab34a250b1'
STOPPING = 'de5b426a63be47a7b6ac3eaac82e2f6f'  # a unit is being stopped (a stop or the first half of a restart)
STOPPED = '9d1aaa27d60140bd96365438aad20286'
# A start job that ended: done (JOB_RESULT=done: a oneshot's run finished well, a service is up) or failed. A user
# session logs no other record of a run that ended well. Read only for units that failed (read_journal).
STARTED = '39f53479d3a045ac8e11786248231fbf'
START_FAILED = 'be02cf6855d2428ba40df7e9d022f03d'
MAX_UNITS = 40  # units whose starts are read at most
FIELDS = ('MESSAGE_ID', 'USER_UNIT', 'UNIT_RESULT', 'JOB_RESULT', 'COREDUMP_COMM', 'COREDUMP_EXE', 'COREDUMP_SIGNAL', 'COREDUMP_SIGNAL_NAME',
          'COREDUMP_PID', 'COREDUMP_UID', 'COREDUMP_CMDLINE', 'COREDUMP_USER_UNIT', 'COREDUMP_TIMESTAMP', 'COREDUMP_CGROUP', 'COREDUMP_CWD')
STOP_SETTLE = dt.timedelta(minutes=2)  # a crash dump is written a little after the stop that caused it
STOP_LONGEST = dt.timedelta(minutes=15)  # a stop with no end on record counts this long
# Browsers a program drives rather than the owner: by their path, their flags or the unit they run in
DRIVEN_PATH = re.compile(r'(ms-playwright|puppeteer|chrome-headless-shell|headless[_-]shell|/selenium/|chromedriver)', re.I)
DRIVEN_FLAG = re.compile(r'(^|\s)--(headless|enable-automation|remote-debugging-pipe|test-type)(=|\s|$)')
THROWAWAY_PROFILE = re.compile(r'--user-data-dir=(/tmp/|/var/tmp/|/dev/shm/|\S*(playwright|puppeteer|selenium|\.org\.chromium\.Chromium\.))', re.I)
CI_UNIT = re.compile(r'(actions\.runner|gitlab-runner|buildkite|jenkins|woodpecker|act[_-]runner|forgejo-runner)', re.I)
# Runs a developer, a test or a coding agent started rather than programs the owner uses (dev_run): anything a coding
# agent's service or session ran (by its unit or cgroup, unless it is the agent itself), a test runner or a test file,
# and a program or working folder in a temporary or cache folder (a throwaway checkout, a sandbox; not an AppImage,
# which runs from /tmp/.mount_*)
CODING_AGENT = re.compile(r'(claude|codex|aider|gemini-cli|opencode|goose|openhands|cursor-agent|devin)', re.I)
TEST_RUNNER = re.compile(r'(pytest|py\.test|unittest|nose2?|tox|nox|jest|vitest|mocha|ava|ctest|karma|cypress)$', re.I)
TEST_FILE = re.compile(r'(^|/)(tests?|__tests__|spec)/|(^|/)(tests?|test_[\w.-]+|[\w.-]+[._-]test|[\w.-]+\.spec)\.(py|[cm]?[jt]s)$', re.I)
THROWAWAY_DIR = re.compile(r'^(/tmp/(?!\.mount_)|/var/tmp/|/dev/shm/|/run/user/\d+/|/home/[^/]+/\.cache/|/root/\.cache/)')
# Interpreters, named in a to-do by the script they ran ('backup.py crashed', not 'python3 crashed'), and their
# options that take a value of their own
INTERPRETER = re.compile(r'(python[\d.]*|pypy[\d.]*|node(js)?|bun|deno|ruby[\d.]*|perl[\d.]*|php[\d.]*|lua[\d.]*|luajit|'
                         r'bash|sh|dash|zsh|fish|ksh|tclsh[\d.]*|Rscript)$')
VALUE_FLAGS = {'-W', '-X', '-r', '--require', '--import', '--loader', '--experimental-loader', '-o', '-O', '--title'}
INLINE_FLAGS = {'-c', '-e', '--eval', '-p', '--print'}  # the code is on the command line: no script to name
FAILURES = {'exit-code', 'signal', 'core-dump', 'timeout', 'watchdog', 'oom-kill', 'start-limit-hit', 'resources', 'protocol'}
SIGNALS = {4: 'SIGILL', 5: 'SIGTRAP', 6: 'SIGABRT', 7: 'SIGBUS', 8: 'SIGFPE', 11: 'SIGSEGV', 31: 'SIGSYS'}
# One to-do per unit: the clearest kind wins.
RANK = ('out_of_memory', 'gave_up', 'crash_loop', 'repeated_failures', 'stays_failed')
# Omarchy's desktop pieces, by the crashed program's name
TRANSIENT = re.compile(r'run-[\w-]+\.service$')  # one-off commands started with systemd-run (a restart later, a test)
OMARCHY_PIECES = {'hyprland': 'hyprland', 'quickshell': 'bar', 'qs': 'bar', 'waybar': 'bar'}
# Do it: the one safe, known fix a finding may offer, and only after the owner's OK. A failed unit of the owner's own is
# started again, never The Machine's own units and never the OpenClaw Gateway; the bar is brought back with Omarchy's
# own command. Nothing else ever runs from here.
RESTARTABLE = ('gave_up', 'repeated_failures', 'stays_failed')
PROTECTED = re.compile(r'(openclaw|personal-assistant|the-machine)', re.I)
SAFE_UNIT = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.@:-]{0,200}\.service')
FIX_TIMEOUT = 60


def run_quiet(args, timeout=TIMEOUT, env=None):
    """(returncode, stdout) of a read-only command; (None, '') when it can't run."""
    try:
        done = subprocess.run(args, capture_output=True, text=True, timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return None, ''
    return done.returncode, done.stdout


def supported(platform=None, which=shutil.which, systemd_dir='/run/systemd/system'):
    """(True, '') when this computer keeps a systemd journal for its user session, else (False, why)."""
    platform = platform or sys.platform
    if platform == 'darwin':
        return False, 'macOS keeps no systemd journal'
    if platform.startswith('win') or platform == 'cygwin':
        return False, 'Windows keeps no systemd journal'
    if not platform.startswith('linux'):
        return False, 'no systemd journal here'
    if not which('journalctl'):
        return False, 'no journalctl here (no systemd journal)'
    if not Path(systemd_dir).is_dir():  # WSL without systemd, a container, another init system
        return False, 'systemd is not running here'
    return True, ''


def omarchy(which=shutil.which, home=None):
    """Whether this is an Omarchy desktop (its command, or its files where a package or an older install puts them)."""
    home = Path(home or Path.home())
    return bool(which('omarchy') or Path('/usr/share/omarchy/bin').is_dir() or (home / '.local/share/omarchy/bin').is_dir())


def unit_name(unit):
    """A unit as the owner knows it: 'waybar' for app-Hyprland-waybar-1a2b3c4d.scope, 'backup' for backup.service."""
    unit = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), str(unit or ''))
    app = re.fullmatch(r'app-(?:[^-]+-)?(.+?)(?:-[0-9a-f]{8}|@[0-9a-f]{16,32})?\.(?:scope|service)', unit)
    if app and unit.count('-') >= 2:
        return app.group(1)
    return re.sub(r'\.service$', '', unit)


def _text(value):
    if isinstance(value, list):  # journald writes non-UTF-8 values as bytes
        return bytes(value).decode('utf-8', 'replace')
    return str(value or '')


def read_journal(hours=WINDOW, run=run_quiet, limit=MAX_ENTRIES):
    """The records detect needs from the owner's own journal, oldest first: [{...FIELDS, 'at': datetime}]. None when it
    can't be read. Only these records (systemd's own, by catalog id) and only these fields: never a message."""
    code, out = run(['journalctl', '--user', '--no-pager', '-q', '-o', 'json', f'--since=-{int(hours.total_seconds() // 60)}min',
                     '-n', str(limit), '--output-fields=' + ','.join(FIELDS),
                     f'MESSAGE_ID={RESTARTED}', f'MESSAGE_ID={RESULT}', f'MESSAGE_ID={COREDUMP}', f'MESSAGE_ID={STOPPING}',
                     f'MESSAGE_ID={STOPPED}'])
    if code != 0:
        return None
    rows = _rows(out)
    # how the starts of the units that failed ended, so one that ran well since is told apart (recovered): only theirs
    count = {}
    for row in rows:
        if row.get('MESSAGE_ID') == RESULT and row.get('UNIT_RESULT') in FAILURES and row.get('USER_UNIT', '').endswith('.service'):
            count[row['USER_UNIT']] = count.get(row['USER_UNIT'], 0) + 1
    units = sorted(unit for unit, n in count.items() if n >= REPEAT_FAILURES and not TRANSIENT.match(unit))[:MAX_UNITS]
    if units:
        code, out = run(['journalctl', '--user', '--no-pager', '-q', '-o', 'json', f'--since=-{int(hours.total_seconds() // 60)}min',
                         '-n', str(limit), '--output-fields=' + ','.join(FIELDS), f'MESSAGE_ID={STARTED}', f'MESSAGE_ID={START_FAILED}',
                         *(f'USER_UNIT={unit}' for unit in units)])
        if code == 0:
            rows += [row for row in _rows(out) if row.get('MESSAGE_ID') in (STARTED, START_FAILED)]
    return rows


def _rows(out):
    rows = []
    for line in out.splitlines():
        try:
            raw = json.loads(line)
            row = {k: _text(raw.get(k)) for k in FIELDS if raw.get(k) is not None}
            row['at'] = dt.datetime.fromtimestamp(int(raw['__REALTIME_TIMESTAMP']) / 1e6, dt.timezone.utc)
        except (ValueError, KeyError, TypeError):
            continue
        rows.append(row)
    return rows


def read_coredumps(hours=WINDOW, run=run_quiet):
    """Crash records from coredumpctl, for when the owner's journal holds none (they went to the system journal):
    [{COREDUMP_*, 'at'}] without a command line, so detect asks for two crashes before it speaks. [] when none."""
    code, out = run(['coredumpctl', 'list', '--json=short', '--no-pager', f'--since=-{int(hours.total_seconds() // 60)}min'])
    if code != 0 or not out.strip():
        return []
    try:
        listed = json.loads(out)
    except ValueError:
        return []
    rows = []
    for item in listed if isinstance(listed, list) else []:
        try:
            rows.append({'MESSAGE_ID': COREDUMP, 'COREDUMP_EXE': str(item.get('exe') or ''), 'COREDUMP_SIGNAL': str(item.get('sig') or ''),
                         'COREDUMP_PID': str(item.get('pid') or ''), 'COREDUMP_UID': str(item.get('uid', '')),
                         'at': dt.datetime.fromtimestamp(int(item['time']) / 1e6, dt.timezone.utc)})
        except (ValueError, KeyError, TypeError):
            continue
    return rows


def failed_units(run=run_quiet):
    """The owner's units systemd lists as failed right now."""
    code, out = run(['systemctl', '--user', 'list-units', '--state=failed', '--no-legend', '--plain', '--no-pager'])
    if code != 0:
        return set()
    return {line.split()[0] for line in out.splitlines() if line.split() and line.split()[0].endswith('.service')}


def hyprland_config_errors(run=run_quiet, runtime=None):
    """How many errors Hyprland reports in its settings (hyprctl configerrors), or 0 when it can't tell."""
    env = dict(os.environ)
    if not env.get('HYPRLAND_INSTANCE_SIGNATURE'):  # the service starts outside the desktop: find its newest Hyprland
        base = Path(runtime or env.get('XDG_RUNTIME_DIR') or f'/run/user/{os.getuid()}') / 'hypr'
        try:
            newest = max((p for p in base.iterdir() if p.is_dir()), key=lambda p: p.stat().st_mtime, default=None)
        except OSError:
            newest = None
        if not newest:
            return 0
        env['HYPRLAND_INSTANCE_SIGNATURE'] = newest.name
    code, out = run(['hyprctl', 'configerrors', '-j'], timeout=5, env=env)
    try:
        found = json.loads(out) if code == 0 else []
    except ValueError:
        return 0
    return sum(1 for item in found if isinstance(item, str) and item.strip()) if isinstance(found, list) else 0


def automated(cmdline, exe='', unit=''):
    """Whether a crashed process isn't one of the owner's programs: a browser's renderer or GPU helper (it says --type=),
    or a browser a test, an agent or CI drove (headless, Playwright's or Puppeteer's own browsers, automation flags,
    remote debugging with a throwaway profile, a CI runner's unit). cmdline is None when it wasn't recorded."""
    if DRIVEN_PATH.search(exe or '') or CI_UNIT.search(unit or ''):
        return True
    if cmdline is None:
        return False
    if '--type=' in cmdline or DRIVEN_FLAG.search(cmdline) or DRIVEN_PATH.search(cmdline):
        return True
    return '--remote-debugging-port' in cmdline and bool(THROWAWAY_PROFILE.search(cmdline))


def _args(cmdline):
    try:
        return shlex.split(cmdline or '')
    except ValueError:
        return (cmdline or '').split()


def script_of(cmdline, exe=''):
    """(script, test_flag) an interpreter ran: the script's path or `-m` module, or None when the program isn't an
    interpreter or ran code from its own command line; test_flag when it ran as a test runner (node --test)."""
    args = _args(cmdline)
    program = os.path.basename(exe or (args[0] if args else ''))
    if not args or not INTERPRETER.match(program):
        return None, False
    rest, test = iter(args[1:]), False
    for arg in rest:
        if arg == '-m':
            return next(rest, None), test
        if arg in INLINE_FLAGS:
            return None, test
        if arg in VALUE_FLAGS:
            next(rest, None)
        elif arg == '--test':
            test = True
        elif arg == 'run' and program in ('bun', 'deno'):
            continue
        elif not arg.startswith('-'):
            return arg, test
    return None, test


def dev_run(row):
    """Whether a crashed process was a developer's, a test's or a coding agent's run, not a program the owner uses
    (see CODING_AGENT): under a coding agent's unit or cgroup (the agent itself crashing still counts), a test runner
    or test file, or run from a temporary or cache folder. Reads only the unit, cgroup, paths and command line."""
    cmdline, exe = row.get('COREDUMP_CMDLINE') or '', row.get('COREDUMP_EXE') or ''
    args = _args(cmdline)
    itself = f"{os.path.basename(exe)} {row.get('COREDUMP_COMM') or ''} {os.path.basename(args[0]) if args else ''}"
    if CODING_AGENT.search(f"{row.get('COREDUMP_USER_UNIT') or ''} {row.get('COREDUMP_CGROUP') or ''}") and not CODING_AGENT.search(itself):
        return True
    script, test = script_of(cmdline, exe)
    if test or (script and (TEST_FILE.search(script) or TEST_RUNNER.match(os.path.splitext(os.path.basename(script))[0])
                            or TEST_RUNNER.match(script.split('.')[0]))):
        return True
    if TEST_RUNNER.match(os.path.basename(exe)):
        return True
    return any(THROWAWAY_DIR.match(path) for path in (exe, row.get('COREDUMP_CWD') or '', script or '') if path.startswith('/'))


def stop_windows(rows):
    """{unit: [(start, end)]}: when each unit was being stopped or restarted, from systemd's Stopping record to its
    Stopped or result record (STOP_LONGEST without one)."""
    windows = {}
    open_ = {}
    for row in sorted(rows, key=lambda r: r['at']):
        unit, mid = row.get('USER_UNIT') or '', row.get('MESSAGE_ID')
        if not unit:
            continue
        if mid == STOPPING:
            open_.setdefault(unit, row['at'])
        elif mid in (STOPPED, RESULT) and unit in open_:
            windows.setdefault(unit, []).append((open_.pop(unit), row['at']))
    for unit, start in open_.items():
        windows.setdefault(unit, []).append((start, start + STOP_LONGEST))
    return windows


def _belongs(unit, crashed_unit, cmdline, exe):
    """Whether a crashed process belongs to a service: it ran in it, or its command line names the service's own files
    (OpenClaw's browser keeps its profile in ~/.openclaw and runs in a scope of its own)."""
    if crashed_unit and crashed_unit == unit:
        return True
    name = unit_name(unit).lower()
    stems = {name, name.split('-')[0]}
    text = f'{exe} {cmdline or ""}'.lower()
    return any(len(stem) >= 4 and re.search(r'[/.]' + re.escape(stem) + r'(?=[/.-])', text) for stem in stems)


def stopping(row, windows):
    """Whether a crash happened while a service it belongs to was being stopped or restarted (or just after, STOP_SETTLE):
    expected, not a problem."""
    at = _crash_time(row)
    return any(start <= at <= end + STOP_SETTLE and _belongs(unit, row.get('COREDUMP_USER_UNIT'), row.get('COREDUMP_CMDLINE'), row.get('COREDUMP_EXE'))
               for unit, spans in windows.items() for start, end in spans)


def _crash_time(row):
    """When the program crashed (systemd-coredump's own time), not when the dump was written."""
    try:
        return dt.datetime.fromtimestamp(int(row['COREDUMP_TIMESTAMP']) / 1e6, dt.timezone.utc)
    except (KeyError, ValueError, TypeError):
        return row['at']


def recovered(failures, started, start_failed):
    """Whether a unit that failed is fine again: its last failure was a start that failed (a oneshot's run that ended
    in an error, a service that didn't come up) and a later start ended well. A service that started and failed later
    proves nothing by starting again, so it never counts."""
    last = max(failures, default=None)
    if last is None or not any(at >= last for at in start_failed):
        return False
    return any(at > max(start_failed) for at in started)


def detect(rows, failed=(), now=None, on_omarchy=False, config_errors=0, uid=None):
    """The real problems in these records, as findings: [{key, kind, name, unit, count, last_at, ...}], clearest first.
    Pure: everything it reads is passed in."""
    now = now or timeutil.clock()
    uid = str(os.getuid() if uid is None else uid)
    units = {}
    crashes = {}
    starts = {}  # {unit: ([started well], [start failed])}
    windows = stop_windows(rows)
    for row in rows:
        mid = row.get('MESSAGE_ID')
        if mid == COREDUMP:
            if row.get('COREDUMP_UID', uid) != uid:
                continue
            cmdline = row.get('COREDUMP_CMDLINE')
            exe = row.get('COREDUMP_EXE') or ''
            if automated(cmdline, exe, row.get('COREDUMP_USER_UNIT')) or dev_run(row) or stopping(row, windows):
                continue
            if not exe and not row.get('COREDUMP_COMM'):
                continue
            script = os.path.basename(script_of(cmdline, exe)[0] or '')
            name = script or row.get('COREDUMP_COMM') or os.path.basename(exe)
            item = crashes.setdefault(script or os.path.basename(exe) or name, {'name': name, 'times': [], 'known': True})
            item['times'].append(_crash_time(row))
            item['pid'] = row.get('COREDUMP_PID') or item.get('pid')
            item['signal'] = row.get('COREDUMP_SIGNAL_NAME') or SIGNALS.get(int(row.get('COREDUMP_SIGNAL') or 0) if (row.get('COREDUMP_SIGNAL') or '').isdigit() else 0) or ''
            item['known'] = item['known'] and cmdline is not None
            continue
        unit = row.get('USER_UNIT') or ''
        if not unit or TRANSIENT.match(unit):
            continue
        if mid in (STARTED, START_FAILED):
            if mid == START_FAILED or row.get('JOB_RESULT') == 'done':
                starts.setdefault(unit, ([], []))[mid == START_FAILED].append(row['at'])
            continue
        entry = units.setdefault(unit, {'restarts': [], 'failures': [], 'results': set()})
        if mid == RESTARTED:
            entry['restarts'].append(row['at'])
        elif mid == RESULT and row.get('UNIT_RESULT') in FAILURES:
            if any(start <= row['at'] <= end for start, end in windows.get(unit, ())):
                continue  # it ended while being stopped or restarted: the stop, not a failure
            entry['failures'].append(row['at'])
            entry['results'].add(row['UNIT_RESULT'])
    found = {}
    for unit, entry in units.items():
        scope = unit.endswith('.scope')
        kinds = {}
        if 'oom-kill' in entry['results']:
            kinds['out_of_memory'] = len(entry['failures'])
        if not scope:
            if 'start-limit-hit' in entry['results']:
                kinds['gave_up'] = len(entry['failures'])
            times = sorted(entry['restarts'])
            burst = max((sum(1 for t in times[i:] if t - start <= LOOP_WINDOW) for i, start in enumerate(times)), default=0)
            if burst >= LOOP_RESTARTS:
                kinds['crash_loop'] = burst
            if len(entry['failures']) >= REPEAT_FAILURES and not recovered(entry['failures'], *starts.get(unit, ((), ()))):
                kinds['repeated_failures'] = len(entry['failures'])
            last = max(entry['failures'], default=None)
            if unit in failed and last and now - last >= FAILED_FOR:
                kinds['stays_failed'] = 1
        if kinds:
            kind = next(k for k in RANK if k in kinds)
            found[unit] = {'kind': kind, 'unit': unit, 'name': unit_name(unit), 'count': int(kinds[kind] or 1),
                           'last_at': max(entry['failures'] + entry['restarts']).isoformat()}
            if kind in RESTARTABLE and unit in failed and restartable(unit):
                found[unit]['fix'] = 'restart_unit'
    for unit in failed:  # failed before the window: it has stayed failed at least that long
        if unit not in units and not TRANSIENT.match(unit):
            found[unit] = {'kind': 'stays_failed', 'unit': unit, 'name': unit_name(unit), 'count': 1, 'last_at': None,
                           **({'fix': 'restart_unit'} if restartable(unit) else {})}
    findings = [dict(f, key=f"{f['kind']}:{f['name']}") for f in found.values()]
    for exe, item in crashes.items():
        if not item['known'] and len(item['times']) < 2:  # no command line to tell a helper apart: two crashes or quiet
            continue
        piece = OMARCHY_PIECES.get(exe.lower()) if on_omarchy else None
        findings.append({'key': f'crashed:{exe}', 'kind': 'crashed', 'name': item['name'], 'program': exe, 'count': len(item['times']),
                         'pid': item.get('pid'), 'signal': item['signal'], 'piece': piece, 'first_at': min(item['times']).isoformat(),
                         'last_at': max(item['times']).isoformat(),
                         **({'fix': 'restart_bar'} if piece == 'bar' else {})})
    if on_omarchy and config_errors:
        findings.append({'key': 'hyprland_config:hyprland', 'kind': 'hyprland_config', 'name': 'Hyprland', 'count': int(config_errors),
                         'piece': 'hyprland', 'last_at': now.isoformat()})
    order = ('crashed', 'out_of_memory', 'gave_up', 'crash_loop', 'hyprland_config', 'repeated_failures', 'stays_failed')
    return sorted(findings, key=lambda f: (order.index(f['kind']), f['name']))


def scan(window=WINDOW, run=run_quiet, now=None, which=shutil.which):
    """{'supported', 'reason', 'omarchy', 'findings'} for this computer, read as described above."""
    ok, why = supported(which=which)
    if not ok:
        return {'supported': False, 'reason': why, 'omarchy': False, 'findings': []}
    rows = read_journal(window, run)
    if rows is None:
        return {'supported': False, 'reason': 'the journal of this user session could not be read', 'omarchy': False, 'findings': []}
    if not any(r.get('MESSAGE_ID') == COREDUMP for r in rows) and which('coredumpctl'):
        rows += read_coredumps(window, run)
    on_omarchy = omarchy(which)
    errors = hyprland_config_errors(run) if on_omarchy and which('hyprctl') else 0
    return {'supported': True, 'reason': '', 'omarchy': on_omarchy,
            'findings': detect(rows, failed_units(run), now, on_omarchy, errors)}


def _bar_command(which=shutil.which):
    return 'omarchy-restart-waybar' if which('omarchy-restart-waybar') and not which('omarchy-restart-shell') else 'omarchy-restart-shell'


def restartable(unit):
    """Whether Do it may start this unit again: an owner's own service, never The Machine's or the OpenClaw Gateway."""
    return bool(SAFE_UNIT.fullmatch(str(unit or ''))) and not PROTECTED.search(str(unit))


def fix_command(finding, which=shutil.which):
    """The exact command Do it runs for a finding (or a to-do's metadata), checked again here: [argv] or None."""
    if finding.get('fix') == 'restart_unit' and restartable(finding.get('unit')) and which('systemctl'):
        return ['systemctl', '--user', 'restart', finding['unit']]
    if finding.get('fix') == 'restart_bar' and which(_bar_command(which)):
        return [_bar_command(which)]
    return None


def run_fix(finding, run=subprocess.run, which=shutil.which):
    """Do it on a to-do from the computer's logs: runs only its exact fix_command, once, and says how it went in plain
    words. (ok, text). Its output is never read: no log text reaches the to-do."""
    argv = fix_command(finding, which)
    if not argv:
        return False, i18n.t('There is no safe fix to run for this here. To see why, ask in this to-do’s chat.')
    shown = ' '.join(argv)
    try:
        code = run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=FIX_TIMEOUT,
                   start_new_session=True).returncode
    except subprocess.TimeoutExpired:
        code = 'timeout'
    except OSError:
        code = None
    if code == 0 and argv[0] == 'systemctl':
        try:
            active = run(['systemctl', '--user', 'is-active', '--quiet', finding['unit']], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, timeout=TIMEOUT).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            active = False
        if active:
            return True, i18n.t('Ran {}. {} is running again.', shown, finding['name'])
        return False, i18n.t('Ran {}, but {} stopped again. Ask in this to-do’s chat and The Machine looks into why.', shown, finding['name'])
    if code == 0:
        return True, i18n.t('Ran {}. The bar is back.', shown)
    if code is None:
        return False, i18n.t('Couldn’t run {} on this computer.', shown)
    if code == 'timeout':
        return False, i18n.t('{} didn’t finish within a minute.', shown)
    return False, i18n.t('{} didn’t work (exit code {}).', shown, code)


def _journal(unit):
    return f'journalctl --user -u {unit} -n 50'


def explain(finding, which=shutil.which):
    """(title, cause, detail) in the owner's language: what happened, why it matters, and the technical detail (the
    commands that show why), which the to-do keeps under Show more and the doctor prints as its fix."""
    kind, name, unit, count = finding['kind'], finding['name'], finding.get('unit', ''), finding['count']
    if kind == 'crash_loop':
        return (i18n.t('{} keeps restarting', name),
                i18n.t('It stopped and started again {} times within an hour, so something keeps making it fail.', count),
                i18n.t('In a terminal, {} shows why.', _journal(unit)))
    if kind == 'gave_up':
        return (i18n.t('{} stopped after failing to start', name),
                i18n.t('It failed several times in a row, so this computer stopped trying. It stays off until it is started again.'),
                i18n.t('In a terminal, {0} shows why, and {1} starts it again once fixed.', _journal(unit), f'systemctl --user restart {unit}'))
    if kind == 'out_of_memory':
        return (i18n.t('{} ran out of memory', name),
                i18n.t('It used more memory than it is allowed, so the system stopped it.'),
                i18n.t('In a terminal, {} shows when. A higher MemoryMax gives it more room.', _journal(unit)))
    if kind == 'repeated_failures':
        return (i18n.t('{} failed {} times in a day', name, count),
                i18n.t('Each run ended in an error, so what it does is not getting done.'),
                i18n.t('In a terminal, {} shows why.', _journal(unit)))
    if kind == 'stays_failed':
        return (i18n.t('{} is down after a failure', name),
                i18n.t('It failed and has not started again since, so what it does is not running.'),
                i18n.t('In a terminal, {0} shows why, and {1} clears it if it is no longer needed.', f'systemctl --user status {unit}',
                       f'systemctl --user reset-failed {unit}'))
    if kind == 'hyprland_config':
        return (i18n.t('Hyprland reports {} errors in its settings', count) if count > 1 else i18n.t('Hyprland reports an error in its settings'),
                i18n.t('Some lines in your Hyprland settings could not be read, so those settings are not applied.'),
                i18n.t('In a terminal, hyprctl configerrors shows them. The settings are in ~/.config/hypr.'))
    where = f"coredumpctl info {finding.get('pid') or ''}".strip()
    crashed = i18n.t('{} crashed {} times in a day', name, count) if count > 1 else i18n.t('{} crashed', name)
    if finding.get('piece') == 'bar':
        return (i18n.t('The bar crashed {} times in a day', count) if count > 1 else i18n.t('The bar crashed'),
                i18n.t('The bar at the top of the screen stopped unexpectedly and left a crash report.'),
                i18n.t('In a terminal, {0} brings it back and {1} shows where it crashed.', _bar_command(which), where))
    if finding.get('piece') == 'hyprland':
        return (crashed,
                i18n.t('Hyprland, the window manager, stopped unexpectedly and left a crash report. Open apps close with it.'),
                i18n.t('In a terminal, {} shows where it crashed.', where))
    signal = finding.get('signal') or i18n.t('no signal recorded')
    span = _span(finding) if count > 1 else None
    return (crashed,
            i18n.t('It stopped unexpectedly {0} times between {1} and {2} ({3}) and left crash reports.', count, *span, signal) if span
            else i18n.t('The program stopped unexpectedly ({}) and left a crash report.', signal),
            i18n.t('In a terminal, {} shows where it crashed.', where))


def _span(finding):
    """(first, last) crash as the owner reads times ('Mon 9:27 AM'), or None without both."""
    try:
        first, last = (dt.datetime.fromisoformat(finding[k]).astimezone(local_tz()) for k in ('first_at', 'last_at'))
    except (KeyError, TypeError, ValueError):
        return None
    return locale_prefs.short_text(first), locale_prefs.short_text(last)


def next_step(finding):
    """What the owner can do about a finding without a terminal, in plain words, or '' (the to-do's chat is offered too)."""
    if finding['kind'] == 'out_of_memory':
        return i18n.t('Closing other heavy apps gives it more room.')
    if finding['kind'] == 'crashed' and finding.get('piece') == 'hyprland':
        return i18n.t('Updating Omarchy brings the latest fixes.')
    if finding['kind'] == 'crashed' and finding.get('piece') != 'bar':
        return i18n.t('If it keeps crashing after an update, report it to its makers.')
    return ''


def see_why(finding, which=shutil.which):
    """The command that shows why, for a to-do whose fix Do it runs."""
    if finding.get('fix') == 'restart_bar':
        return i18n.t('In a terminal, {} shows where it crashed.', f"coredumpctl info {finding.get('pid') or ''}".strip())
    if finding['kind'] == 'stays_failed':
        return i18n.t('In a terminal, {} shows why.', f"systemctl --user status {finding['unit']}")
    return i18n.t('In a terminal, {} shows why.', _journal(finding['unit']))


def card(finding, which=shutil.which):
    """(title, body, signal) of the to-do for one finding. No log text: only names and counts. Plain words first: what
    happened, what Do it does (with a safe fix, fix_command) or what the owner can do and that the chat looks into it;
    the commands come last, so the to-do keeps them under Show more."""
    title, cause, detail = explain(finding, which)
    argv = fix_command(finding, which)
    if argv:
        does = i18n.t('Do it restarts the bar.') if finding.get('fix') == 'restart_bar' else i18n.t('Do it restarts {}.', finding['name'])
        body = '\n\n'.join((cause, does, i18n.t('Do it runs {}.', ' '.join(argv)) + ' ' + see_why(finding, which)))
    else:
        body = '\n\n'.join(filter(None, (cause, next_step(finding),
                                         i18n.t('Ask in this to-do’s chat and The Machine looks into it. Anything it changes on this computer waits for your OK.'),
                                         detail)))
    # what was seen is the signal, what it means and what to do is the to-do: the open to-do shows each once
    facts = [f'Unit: {finding["unit"]}'] if finding.get('unit') else []
    facts += [f'Program: {finding["program"]}'] if finding.get('program') else []
    facts += [i18n.t('Crashed ({})', finding['signal'])] if finding.get('signal') else []
    facts += [f"Seen: {finding['count']}× in the last {int(WINDOW.total_seconds() // 3600)} hours"]
    signal = i18n.t('Seen in this computer’s own logs.') + '\n\n' + '\n'.join(facts)
    return title[:90], body[:699], signal


def doctor(config, scan_logs=None):
    """`assistant doctor`'s lines for the computer's own logs; none when they are off ("computer_logs": false)."""
    if config.get('computer_logs', True) is False:
        return []
    return doctor_lines((scan_logs or scan)())


def doctor_lines(result, names=()):
    """`assistant doctor` lines (mark, text, fix) for a scan, scrubbed the way learnings are (team_learnings.scrub_log):
    the doctor's output goes into bug reports."""
    import team_learnings
    clean = lambda text: team_learnings.scrub_log(text, names)
    if not result['supported']:
        return [('✓', f"computer logs: not read here ({result['reason']})", '')]
    if not result['findings']:
        return [('✓', 'computer logs: no problems in the last day' + (' (Omarchy: Hyprland and the bar too)' if result['omarchy'] else ''), '')]
    lines = []
    for finding in result['findings']:
        title, cause, fix = explain(finding)
        lines.append(('!', clean(f'computer logs: {title}. {cause}'), clean(fix)))
    return lines

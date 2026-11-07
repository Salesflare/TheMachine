"""The computer's own logs: journald and systemd-coredump, read so The Machine can explain and fix problems on the
computer it runs on.

Read-only and local. It reads `journalctl --user` for the owner's own user session and units (their own journal, never
the system one, never with sudo), and `coredumpctl` only when that journal has no crash records. Only structured
fields are read: which unit, how it ended, how often it restarted, and for a crash the program's name, its signal and
whether it was a browser's helper process. Never message text, so no log line is kept, shown or sent. Volume and time
are capped (MAX_ENTRIES over WINDOW, short timeouts) and the service reads at most every EVERY.

Owner decision (October 10, 2026), kept here as for the Gateway source: routine restarts and noise stay silent. Only
real problems surface (detect): a unit that keeps restarting (LOOP_RESTARTS within an hour), one systemd gave up on
(start-limit-hit), one that ran out of memory, one that failed REPEAT_FAILURES times in a day, one that stays failed,
and a crash dump of a program (not a browser's renderer or a headless test browser). On Omarchy it also reads Hyprland
(its crashes and the errors it reports in its settings) and the bar, with fixes in Omarchy's own commands.

Each finding has a plain cause and a suggested fix (card). The service turns new ones into to-dos through the Machine
health source (Store.system_log_cards): one per problem, deduped and rate-limited, and nothing on the computer changes
unless the owner asks in the to-do and approves the step (Do it). `assistant doctor` lists them too (doctor_lines),
scrubbed the way learnings are, since a bug report carries the doctor's output.

macOS, Windows, WSL without systemd and other computers without journald: supported() says why not and nothing is read."""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import i18n

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
FIELDS = ('MESSAGE_ID', 'USER_UNIT', 'UNIT_RESULT', 'COREDUMP_COMM', 'COREDUMP_EXE', 'COREDUMP_SIGNAL', 'COREDUMP_SIGNAL_NAME',
          'COREDUMP_PID', 'COREDUMP_UID', 'COREDUMP_CMDLINE')
FAILURES = {'exit-code', 'signal', 'core-dump', 'timeout', 'watchdog', 'oom-kill', 'start-limit-hit', 'resources', 'protocol'}
SIGNALS = {4: 'SIGILL', 5: 'SIGTRAP', 6: 'SIGABRT', 7: 'SIGBUS', 8: 'SIGFPE', 11: 'SIGSEGV', 31: 'SIGSYS'}
# One to-do per unit: the clearest kind wins.
RANK = ('out_of_memory', 'gave_up', 'crash_loop', 'repeated_failures', 'stays_failed')
# Omarchy's desktop pieces, by the crashed program's name
TRANSIENT = re.compile(r'run-[\w-]+\.service$')  # one-off commands started with systemd-run (a restart later, a test)
OMARCHY_PIECES = {'hyprland': 'hyprland', 'quickshell': 'bar', 'qs': 'bar', 'waybar': 'bar'}


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
                     f'MESSAGE_ID={RESTARTED}', f'MESSAGE_ID={RESULT}', f'MESSAGE_ID={COREDUMP}'])
    if code != 0:
        return None
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


def _helper(cmdline):
    """A process that isn't a program of its own: a browser's renderer or GPU helper (it says --type=), or a headless
    browser a test or an agent drove."""
    return '--type=' in cmdline or '--headless' in cmdline


def detect(rows, failed=(), now=None, on_omarchy=False, config_errors=0, uid=None):
    """The real problems in these records, as findings: [{key, kind, name, unit, count, last_at, ...}], clearest first.
    Pure: everything it reads is passed in."""
    now = now or dt.datetime.now(dt.timezone.utc)
    uid = str(os.getuid() if uid is None else uid)
    units = {}
    crashes = {}
    for row in rows:
        mid = row.get('MESSAGE_ID')
        if mid == COREDUMP:
            if row.get('COREDUMP_UID', uid) != uid:
                continue
            cmdline = row.get('COREDUMP_CMDLINE')
            if cmdline is not None and _helper(cmdline):
                continue
            exe = row.get('COREDUMP_EXE') or ''
            name = row.get('COREDUMP_COMM') or os.path.basename(exe) or 'a program'
            if not exe and not row.get('COREDUMP_COMM'):
                continue
            item = crashes.setdefault(os.path.basename(exe) or name, {'name': name, 'times': [], 'known': True})
            item['times'].append(row['at'])
            item['pid'] = row.get('COREDUMP_PID') or item.get('pid')
            item['signal'] = row.get('COREDUMP_SIGNAL_NAME') or SIGNALS.get(int(row.get('COREDUMP_SIGNAL') or 0) if (row.get('COREDUMP_SIGNAL') or '').isdigit() else 0) or ''
            item['known'] = item['known'] and cmdline is not None
            continue
        unit = row.get('USER_UNIT') or ''
        if not unit or TRANSIENT.match(unit):
            continue
        entry = units.setdefault(unit, {'restarts': [], 'failures': [], 'results': set()})
        if mid == RESTARTED:
            entry['restarts'].append(row['at'])
        elif mid == RESULT and row.get('UNIT_RESULT') in FAILURES:
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
            if len(entry['failures']) >= REPEAT_FAILURES:
                kinds['repeated_failures'] = len(entry['failures'])
            last = max(entry['failures'], default=None)
            if unit in failed and last and now - last >= FAILED_FOR:
                kinds['stays_failed'] = 1
        if kinds:
            kind = next(k for k in RANK if k in kinds)
            found[unit] = {'kind': kind, 'unit': unit, 'name': unit_name(unit), 'count': int(kinds[kind] or 1),
                           'last_at': max(entry['failures'] + entry['restarts']).isoformat()}
    for unit in failed:  # failed before the window: it has stayed failed at least that long
        if unit not in units and not TRANSIENT.match(unit):
            found[unit] = {'kind': 'stays_failed', 'unit': unit, 'name': unit_name(unit), 'count': 1, 'last_at': None}
    findings = [dict(f, key=f"{f['kind']}:{f['name']}") for f in found.values()]
    for exe, item in crashes.items():
        if not item['known'] and len(item['times']) < 2:  # no command line to tell a helper apart: two crashes or quiet
            continue
        piece = OMARCHY_PIECES.get(exe.lower()) if on_omarchy else None
        findings.append({'key': f'crashed:{exe}', 'kind': 'crashed', 'name': item['name'], 'program': exe, 'count': len(item['times']),
                         'pid': item.get('pid'), 'signal': item['signal'], 'piece': piece, 'last_at': max(item['times']).isoformat()})
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


def explain(finding, which=shutil.which):
    """(title, cause, fix) in the owner's language: what happened, why it matters, and what fixes it."""
    kind, name, unit, count = finding['kind'], finding['name'], finding.get('unit', ''), finding['count']
    if kind == 'crash_loop':
        return (i18n.t('{} keeps restarting', name),
                i18n.t('It stopped and started again {} times within an hour, so something keeps making it fail.', count),
                i18n.t('To see why: journalctl --user -u {} -n 50', unit))
    if kind == 'gave_up':
        return (i18n.t('{} stopped after failing to start', name),
                i18n.t('It failed several times in a row, so systemd stopped trying. It stays off until it is started again.'),
                i18n.t('To see why: journalctl --user -u {0} -n 50. Once fixed: systemctl --user restart {0}', unit))
    if kind == 'out_of_memory':
        return (i18n.t('{} ran out of memory', name),
                i18n.t('It used more memory than it is allowed, so the system stopped it.'),
                i18n.t('Close other heavy apps, or raise its MemoryMax. To see when: journalctl --user -u {} -n 50', unit))
    if kind == 'repeated_failures':
        return (i18n.t('{} failed {} times in a day', name, count),
                i18n.t('Each run ended in an error, so what it does is not getting done.'),
                i18n.t('To see why: journalctl --user -u {} -n 50', unit))
    if kind == 'stays_failed':
        return (i18n.t('{} is down after a failure', name),
                i18n.t('It failed and has not started again since, so what it does is not running.'),
                i18n.t('To see why: systemctl --user status {0}. If it is no longer needed: systemctl --user reset-failed {0}', unit))
    if kind == 'hyprland_config':
        return (i18n.t('Hyprland reports {} errors in its settings', count) if count > 1 else i18n.t('Hyprland reports an error in its settings'),
                i18n.t('Some lines in your Hyprland settings could not be read, so those settings are not applied.'),
                i18n.t('To see them: hyprctl configerrors. Then fix those lines in ~/.config/hypr.'))
    pid = finding.get('pid') or ''
    crashed = i18n.t('{} crashed {} times in a day', name, count) if count > 1 else i18n.t('{} crashed', name)
    if finding.get('piece') == 'bar':
        return (i18n.t('The bar crashed {} times in a day', count) if count > 1 else i18n.t('The bar crashed'),
                i18n.t('The bar at the top of the screen stopped unexpectedly and left a crash report.'),
                i18n.t('To bring it back: {}. To see where it crashed: coredumpctl info {}', _bar_command(which), pid))
    if finding.get('piece') == 'hyprland':
        return (crashed,
                i18n.t('Hyprland, the window manager, stopped unexpectedly and left a crash report. Open apps close with it.'),
                i18n.t('To see where it crashed: coredumpctl info {}. omarchy-update brings the latest fixes.', pid))
    return (crashed,
            i18n.t('The program stopped unexpectedly ({}) and left a crash report.', finding.get('signal') or i18n.t('no signal recorded')),
            i18n.t('To see where it crashed: coredumpctl info {}. If it keeps crashing after an update, report it to its makers.', pid))


def card(finding, which=shutil.which):
    """(title, body, signal) of the to-do for one finding. No log text: only names, counts and the commands to run."""
    title, cause, fix = explain(finding, which)
    body = '\n\n'.join((cause, fix, i18n.t('Ask in this to-do’s chat and The Machine looks into it. Anything it changes on this computer waits for your OK.')))
    # what was seen is the signal, what it means and what to do is the to-do: the open to-do shows each once
    facts = [f'Unit: {finding["unit"]}'] if finding.get('unit') else []
    facts += [f'Program: {finding["program"]}'] if finding.get('program') else []
    facts += [f'Signal: {finding["signal"]}'] if finding.get('signal') else []
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

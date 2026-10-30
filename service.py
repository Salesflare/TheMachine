"""How The Machine runs in the background, per operating system.

Linux: systemd user units; journald keeps their logs. macOS: launchd agents in ~/Library/LaunchAgents, logging
to ~/Library/Logs/TheMachine. Windows: The Machine runs inside WSL2, which is Linux (see install.ps1).
ASSISTANT_SERVICE_MANAGER=systemd|launchd|none overrides the choice.

Every command here takes the caller's `run`, so the caller's own tests see the exact commands."""
import os
import plistlib
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

UNIT_NAME = 'personal-assistant.service'
LABEL_PREFIX = 'computer.themachine.'
LABEL = LABEL_PREFIX + 'assistant'
LOG_LIMIT = 20 * 1024 * 1024  # a launchd log is trimmed to its last part at start beyond this


def default_run(args, timeout=60, **kwargs):
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    try:
        return subprocess.run(args, timeout=timeout, **kwargs)
    except (OSError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(args, 127, '', str(error))


def manager():
    forced = os.environ.get('ASSISTANT_SERVICE_MANAGER', '').strip().lower()
    if forced in ('systemd', 'launchd', 'none'):
        return forced
    if sys.platform == 'darwin':
        return 'launchd'
    if sys.platform.startswith('linux'):
        return 'systemd'
    return 'none'


def available():
    """A service manager this account can use is here."""
    return {'systemd': lambda: bool(shutil.which('systemctl')), 'launchd': lambda: bool(shutil.which('launchctl'))}.get(
        manager(), lambda: False)()


def wsl():
    """Running inside Windows Subsystem for Linux."""
    try:
        return 'microsoft' in Path('/proc/sys/kernel/osrelease').read_text().lower()
    except OSError:
        return False


def label(unit=UNIT_NAME):
    """The launchd label for a unit name: personal-assistant.service is computer.themachine.assistant,
    the-machine-wacli-x.service is computer.themachine.wacli-x."""
    if unit == UNIT_NAME:
        return LABEL
    return LABEL_PREFIX + re.sub(r'^the-machine-', '', unit.removesuffix('.service'))


def home():
    return Path(os.environ.get('HOME') or Path.home())


def definition_path(unit=UNIT_NAME, base=None):
    """Where the unit (Linux) or agent plist (macOS) lives."""
    base = Path(base or home())
    if manager() == 'launchd':
        return base / 'Library/LaunchAgents' / f'{label(unit)}.plist'
    return base / '.config/systemd/user' / unit


def log_path(unit=UNIT_NAME, base=None):
    """The log file of a launchd agent (systemd units log to the journal instead)."""
    return Path(base or home()) / 'Library/Logs/TheMachine' / f"{label(unit).removeprefix(LABEL_PREFIX)}.log"


def plist_text(program, workdir=None, env=None, unit=UNIT_NAME, base=None, throttle=10):
    """A launchd agent that starts at login, restarts when it ends and logs to log_path()."""
    log = str(log_path(unit, base))
    agent = {'Label': label(unit), 'ProgramArguments': [str(p) for p in program], 'RunAtLoad': True, 'KeepAlive': True,
             'ThrottleInterval': throttle, 'ProcessType': 'Background', 'Umask': 0o077,
             'StandardOutPath': log, 'StandardErrorPath': log}
    if workdir:
        agent['WorkingDirectory'] = str(workdir)
    if env:
        agent['EnvironmentVariables'] = {k: str(v) for k, v in env.items()}
    return plistlib.dumps(agent, sort_keys=False).decode()


def _domain():
    return f'gui/{os.getuid()}'


def _target(unit):
    return f'{_domain()}/{label(unit)}'


def _ok(args):
    return subprocess.CompletedProcess(args, 0, '', '')


def reload(run=default_run):
    """systemd reads changed unit files; launchd reads a plist when it is bootstrapped, so nothing to do there."""
    if manager() == 'launchd':
        return _ok(['launchctl'])
    return run(['systemctl', '--user', 'daemon-reload'], timeout=30)


def loaded(unit=UNIT_NAME, run=default_run):
    if manager() == 'launchd':
        return run(['launchctl', 'print', _target(unit)], timeout=15).returncode == 0
    return run(['systemctl', '--user', 'is-enabled', unit], timeout=15).returncode == 0


def enable(unit=UNIT_NAME, run=default_run):
    """Start at login from now on (launchd: load the agent; it starts right away)."""
    if manager() == 'launchd':
        path = definition_path(unit)
        log_path(unit).parent.mkdir(parents=True, exist_ok=True)
        run(['launchctl', 'bootout', _target(unit)], timeout=30)  # a changed plist is only read when loaded again
        enabled = run(['launchctl', 'enable', _target(unit)], timeout=15)
        if enabled.returncode:
            return enabled
        return run(['launchctl', 'bootstrap', _domain(), str(path)], timeout=60)
    return run(['systemctl', '--user', 'enable', unit], timeout=60)


def enable_now(unit=UNIT_NAME, run=default_run):
    if manager() == 'launchd':
        return enable(unit, run)
    return run(['systemctl', '--user', 'enable', '--now', unit], timeout=60)


def restart(unit=UNIT_NAME, run=default_run, timeout=60):
    if manager() == 'launchd':
        result = run(['launchctl', 'kickstart', '-k', _target(unit)], timeout=timeout)
        if result.returncode and definition_path(unit).exists():  # not loaded (stopped, or never started): load it
            result = run(['launchctl', 'bootstrap', _domain(), str(definition_path(unit))], timeout=timeout)
        return result
    return run(['systemctl', '--user', 'restart', unit], timeout=timeout)


def try_restart(unit=UNIT_NAME, run=default_run):
    """Restart only when it runs."""
    if manager() == 'launchd':
        result = run(['launchctl', 'print', _target(unit)], timeout=15)
        if result.returncode or not re.search(r'^\s*state = running\s*$', result.stdout or '', re.M):
            return _ok(result.args)
        return run(['launchctl', 'kickstart', '-k', _target(unit)], timeout=60)
    return run(['systemctl', '--user', 'try-restart', unit], timeout=60)


def start(unit=UNIT_NAME, run=default_run):
    if manager() == 'launchd':
        if loaded(unit, run):
            return run(['launchctl', 'kickstart', _target(unit)], timeout=60)
        return run(['launchctl', 'bootstrap', _domain(), str(definition_path(unit))], timeout=60)
    return run(['systemctl', '--user', 'start', unit], timeout=60)


def stop(unit=UNIT_NAME, run=default_run):
    """Stop it until the next start or login (launchd: unload the agent; KeepAlive would restart a plain kill)."""
    if manager() == 'launchd':
        result = run(['launchctl', 'bootout', _target(unit)], timeout=60)
        return _ok(result.args) if result.returncode and not loaded(unit, run) else result
    return run(['systemctl', '--user', 'stop', unit], timeout=60)


def disable_now(unit=UNIT_NAME, run=default_run):
    if manager() == 'launchd':
        disabled = run(['launchctl', 'disable', _target(unit)], timeout=15)
        if disabled.returncode:
            return disabled
        return stop(unit, run)
    return run(['systemctl', '--user', 'disable', '--now', unit], timeout=60)


def active(unit=UNIT_NAME, run=default_run):
    if not available():
        return False
    if manager() == 'launchd':
        return bool(re.search(r'^\s*state = running\s*$', run(['launchctl', 'print', _target(unit)], timeout=15).stdout or '', re.M))
    return run(['systemctl', '--user', 'is-active', unit], timeout=15).stdout.strip() == 'active'


def status_text(unit=UNIT_NAME, run=default_run):
    if manager() == 'launchd':
        result = run(['launchctl', 'print', _target(unit)], timeout=15)
        if result.returncode:
            return f'{label(unit)}: not loaded ({definition_path(unit)})'
        keep = [line.strip() for line in result.stdout.splitlines()
                if re.match(r'\s*(state|pid|last exit code|runs|program|path) =', line)]
        return f'{label(unit)}\n  ' + '\n  '.join(keep) + f'\n  log = {log_path(unit)}'
    result = run(['systemctl', '--user', 'status', unit, '--no-pager', '-n', '0'], timeout=15)
    return (result.stdout or result.stderr).rstrip()


def environment(unit=UNIT_NAME, run=default_run):
    """The environment the service is configured with, as a dict."""
    if manager() == 'launchd':
        try:
            return dict(plistlib.loads(definition_path(unit).read_bytes()).get('EnvironmentVariables') or {})
        except (OSError, ValueError, plistlib.InvalidFileException):
            return {}
    text = run(['systemctl', '--user', 'show', unit, '-p', 'Environment', '--value'], timeout=15).stdout or ''
    try:
        parts = shlex.split(text)
    except ValueError:
        parts = text.split()
    return dict(part.split('=', 1) for part in parts if '=' in part)


def logs(unit=UNIT_NAME, lines=50, follow=False, run=default_run):
    """The service's recent log lines (follow: keep printing, in the terminal)."""
    if manager() == 'launchd':
        path = log_path(unit)
        if follow:
            return subprocess.call(['tail', '-n', str(lines), '-F', str(path)])
        try:
            with path.open('rb') as handle:
                handle.seek(0, 2)
                handle.seek(max(0, handle.tell() - 400 * lines))
                return '\n'.join(handle.read().decode(errors='replace').splitlines()[-lines:])
        except OSError:
            return f'(no log yet at {path})'
    args = ['journalctl', '--user', '-u', unit, '-n', str(lines), '--no-pager']
    if follow:
        return subprocess.call(args[:-1] + ['-f'])
    result = run(args, timeout=30)
    return (result.stdout or result.stderr).rstrip()


def hint(action, unit=UNIT_NAME):
    """The command to tell the owner, for restart, start, stop, status or logs."""
    if manager() == 'launchd':
        if unit == UNIT_NAME:
            return 'assistant service ' + {'enable': 'start'}.get(action, action)
        return {'restart': f'launchctl kickstart -k gui/$(id -u)/{label(unit)}', 'start': f'launchctl kickstart gui/$(id -u)/{label(unit)}',
                'enable': f'launchctl bootstrap gui/$(id -u) {definition_path(unit)}',
                'stop': f'launchctl bootout gui/$(id -u)/{label(unit)}', 'status': f'launchctl print gui/$(id -u)/{label(unit)}',
                'logs': f'tail -n 50 {log_path(unit)}'}[action]
    if action == 'logs':
        return f'journalctl --user -u {unit} -n 50'
    if action == 'enable':
        return f'systemctl --user enable --now {unit}'
    return f'systemctl --user {action} {unit}'


def running_as_service():
    """This process is the service, started by systemd or launchd."""
    if manager() == 'launchd':
        return os.environ.get('XPC_SERVICE_NAME', '').startswith(LABEL_PREFIX)
    return bool(os.environ.get('INVOCATION_ID'))


def restart_later(unit=UNIT_NAME, delay=5):
    """Restart the service a few seconds from now, from outside its own process. Returns whether it was scheduled."""
    if manager() == 'launchd':
        command = f'sleep {int(delay)}; exec launchctl kickstart -k "$0"'
        target = _target(unit)
    else:
        if shutil.which('systemd-run') and not default_run(['systemd-run', '--user', '--quiet', '--collect', f'--on-active={delay}',
                                                            # on time: a user manager's timers default to a minute's accuracy,
                                                            # which put a new connection's restart 7 to 13 s out instead of 3
                                                            '--timer-property=AccuracySec=100ms', 'systemctl', '--user', 'restart', unit], timeout=20).returncode:
            return True
        command = f'sleep {int(delay)}; exec systemctl --user restart "$0"'
        target = unit
    try:
        subprocess.Popen(['sh', '-c', command, target], start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False


def trim_log(unit=UNIT_NAME, keep=1024 * 1024):
    """launchd never rotates a log: at start, a log past LOG_LIMIT keeps only its last `keep` bytes."""
    if manager() != 'launchd' or not running_as_service():
        return
    path = log_path(unit)
    try:
        if path.stat().st_size <= LOG_LIMIT:
            return
        with path.open('rb') as handle:
            handle.seek(-keep, 2)
            tail = handle.read()
        with path.open('r+b') as handle:  # in place: launchd keeps appending to the same open file
            handle.write(tail)
            handle.truncate()
    except OSError:
        pass

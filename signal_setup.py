"""Signal's setup (onboarding.STEPS['signal']): the pinned signal-cli, a link as a device of the owner's phone (a QR code
to scan in Signal, Settings, Linked devices), then the mirror (signal_mirror.py) as a user service. Disconnect stops the
mirror and deletes the store with the linked device's keys; the phone lists the device until it is unlinked there.

Kept apart from onboarding.py, which it uses for the shared setup helpers (loaded when a step runs)."""
import json
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINK_WAIT = 900  # seconds a link waits for the owner to scan the code


def _ob():
    import onboarding
    return onboarding


def base(config):
    ob = _ob()
    return ob.data_dir(config) if config.get('database') else ob.home() / '.local/share/personal-assistant'


def command(config, account, what):
    """The mirror's command line for this account: signal-cli from config `signal_cli` (a hosted Machine's own), else the
    pinned build under <data>/signal-cli."""
    parts = [sys.executable, str(ROOT / 'signal_mirror.py'), '--store', str(account['store']), '--base', str(base(config) / 'signal-cli')]
    if config.get('signal_cli'):
        parts += ['--cli', str(config['signal_cli'])]
    if config.get('database'):
        parts += ['--database', str(Path(config['database']).expanduser())]
    return parts + [what]


def state(account):
    """The mirror's state for this account's store, {} when it has none yet."""
    import sqlite3
    import signal_store
    try:
        with closing(signal_store.connect(account['store'], readonly=True)) as db:
            return signal_store.get_state(db)
    except (sqlite3.Error, OSError):
        return {}


def unit(account):
    """the-machine-personal-signal.service: the account id already says Signal."""
    return f"the-machine-{re.sub(r'[^A-Za-z0-9_-]', '-', account['id'])}.service"


def install(config):
    import signal_release
    if config.get('signal_cli') and Path(config['signal_cli']).exists():
        return config['signal_cli']
    try:
        return str(signal_release.install(base(config) / 'signal-cli'))
    except (OSError, RuntimeError) as error:
        text = str(error)
        raise _ob().SetupError(text[:1].upper() + text[1:200] if 'Java' in text else f'Could not install Signal here ({text[:200]})',
                               'install Java 25 or later, then add Signal again' if 'Java' in text else 'check the connection and add Signal again')


def step_signal(config, account, ui):
    import timeutil
    ob = _ob()
    import signal_store
    account['store'] = str(Path(account.get('store') or base(config) / 'signal' / ob.slug(account['id'])).expanduser())
    install(config)
    signal_store.private_dir(account['store'])
    now = state(account)
    if not now.get('identity') or now.get('error') or not (Path(account['store']) / signal_store.CLI_DIR).exists():
        now = link(config, account, ui)
    account['identity_sha256'] = now['identity']
    account['connected_at'] = timeutil.clock().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    if follow(config, account, ui):
        ui.say('  Linked. Signal gives a new linked device no older messages, so it reads from now on.')


def link(config, account, ui):
    """One link through the mirror, which speaks JSON lines: each QR code goes to the dashboard (or the terminal)."""
    ob = _ob()
    name = unit(account)
    if ob.service.available() and ob.service.definition_path(name, ob.home()).exists():
        ob.service.stop(name, run=ob.run)  # the store has one writer: the link, until the mirror starts again
    try:
        process = subprocess.Popen(command(config, account, 'link'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    except OSError as error:
        raise ob.SetupError(f'Could not start the Signal link ({error.strerror})')
    events, done = [], threading.Event()

    def reader():
        for line in process.stdout:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if isinstance(event, dict):
                events.append(event)
        done.set()
    threading.Thread(target=reader, daemon=True).start()
    web = getattr(ui, 'web', False)
    until, connected, failed, shown = time.monotonic() + LINK_WAIT, None, [], False
    try:
        while not (done.is_set() and not events):
            if getattr(ui, 'cancelled', False) or time.monotonic() > until:
                raise ob.SetupError('Stopped' if getattr(ui, 'cancelled', False) else 'The Signal link took too long', 'add Signal again')
            if not events:
                time.sleep(0.5)
                continue
            event = events.pop(0)
            if event.get('event') == 'qr' and isinstance(event.get('matrix'), list):
                if web:
                    ui.show_code({'kind': 'qr', 'app': 'signal', 'matrix': [str(r)[:200] for r in event['matrix'][:200]],
                                  'expires': str(event.get('expires') or '')})
                else:
                    ui.say(ob.telegram_qr_text(event['matrix']))
                    if not shown:
                        ui.say('  In Signal on your phone: Settings, Linked devices, Link new device, then scan this code.')
                shown = True
            elif event.get('event') == 'connected':
                connected = event
            elif event.get('event') == 'error':
                failed.append(event)
        process.wait(30)
    finally:
        if web:
            ui.show_code(None)
        if process.poll() is None:
            process.terminate()
            process.wait(10)
    if not connected or not connected.get('identity'):
        why = str((failed[-1] if failed else {}).get('code') or '')
        if why == 'qr_expired':
            raise ob.SetupError('The QR code was not scanned in time', 'add Signal again')
        raise ob.SetupError('Signal was not linked' + (f' ({why})' if why else ''), 'add Signal again')
    return {**state(account), 'identity': connected['identity']}


def follow(config, account, ui):
    """The mirror only reads while it runs: one per account as a user service (systemd on Linux, launchd on macOS), the
    store's single writer, which also sends what the owner approved. It stays stopped once Signal unlinks it. True once
    it runs."""
    ob = _ob()
    name = unit(account)
    path = ob.service.definition_path(name, ob.home())
    parts = command(config, account, 'follow')
    if not ob.service.available():
        ui.say('  Signal: keep it running yourself: ' + ' '.join(shlex.quote(p) for p in parts))
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    if ob.service.manager() == 'launchd':
        path.write_text(ob.service.plist_text(parts, unit=name, base=ob.home(), throttle=120))
        started = ob.service.enable(name, run=ob.run)
        if started.returncode:
            ui.say(f'  Signal: start it with {ob.service.hint("enable", name)}')
        return not started.returncode
    line = ' '.join(shlex.quote(str(part)) for part in parts)
    path.write_text('[Unit]\nDescription=The Machine: Signal chats\nAfter=network-online.target\n\n'
                    f'[Service]\nExecStart={line}\nRestart=on-failure\nRestartSec=120\nMemoryMax=768M\n\n[Install]\nWantedBy=default.target\n')
    ob.run(['systemctl', '--user', 'daemon-reload'], timeout=30)
    started = ob.run(['systemctl', '--user', 'enable', '--now', path.name], timeout=60)
    if not started.returncode:
        ob.service.restart(path.name, run=ob.run)  # a new link: a mirror still running would hold the old one
    else:
        ui.say(f'  Signal: start it with systemctl --user enable --now {path.name}')
    return not started.returncode


def signal_remove(config, account):
    """Disconnect: stop the mirror and delete its store (messages, chats and the linked device's keys)."""
    ob = _ob()
    name = unit(account)
    path = ob.service.definition_path(name, ob.home())
    if path.exists():
        if ob.service.available():
            ob.service.disable_now(name, run=ob.run)
        path.unlink(missing_ok=True)
        if ob.service.available():
            ob.service.reload(run=ob.run)
    store = account.get('store')
    if not store or not Path(store).exists():
        return
    ob.run(command(config, account, 'logout'), timeout=120)
    if not any(a.get('store') == store for a in config.get('accounts', []) if a.get('id') != account.get('id')):
        shutil.rmtree(store, ignore_errors=True)

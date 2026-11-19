"""WhatsApp's sync as a user service (onboarding.STEPS['whatsapp']): the store's single writer, kept by The Machine's own
service or by one the owner set up themselves, which pauses while the dashboard links WhatsApp again.

Kept apart from onboarding.py, which it uses for the shared setup helpers (loaded when a step runs)."""
import re
import shlex
from contextlib import contextmanager
from pathlib import Path

import portable
import service
import wacli_release


def _ob():
    import onboarding
    return onboarding


def store_busy(store):
    """Whether another wacli (such as your own sync) holds the store: then that one keeps it synced."""
    try:
        with open(Path(store) / 'LOCK', 'a') as lock:
            portable.lock(lock, blocking=False)
            portable.unlock(lock)
        return False
    except BlockingIOError:
        return True
    except OSError:
        return False


def store_units(store):
    """The user services whose definition names this wacli store: The Machine's own sync, or one the owner set up
    themselves (a mirror of their own). systemd only; none elsewhere."""
    if service.manager() != 'systemd':
        return []
    folder, named = service.definition_path('x.service', _ob().home()).parent, re.compile(re.escape(str(store).rstrip('/')) + r'(?![^/\s"\'])')
    found = []
    for path in sorted(folder.glob('*.service')) if folder.is_dir() else ():
        try:
            if named.search(path.read_text()):
                found.append(path.name)
        except OSError:
            continue
    return found


@contextmanager
def store_paused(store):
    """Linking takes the store's lock, which a running sync holds (and one that restarts takes back every few seconds):
    the services syncing this store stop while it links, and the ones that ran start again after, logged in or not."""
    stopped = [unit for unit in store_units(store)
               if _ob().run(['systemctl', '--user', 'is-active', unit], timeout=15).stdout.strip() in ('active', 'activating', 'reloading')]
    for unit in stopped:
        service.stop(unit, run=_ob().run)
    try:
        yield
    finally:
        for unit in stopped:
            service.start(unit, run=_ob().run)


def whatsapp_sync(wacli, account, ui):
    """wacli only receives messages while its sync runs: keep one running as a user service (systemd on Linux,
    launchd on macOS), the store's single writer. Sends hand off to it. Skipped when something else already syncs this
    store; a service of the owner's own for it (one that stopped when WhatsApp logged it out) is started again instead."""
    name = f"the-machine-wacli-{re.sub(r'[^A-Za-z0-9_-]', '-', account['id'])}.service"
    unit = service.definition_path(name, _ob().home())
    if not unit.exists() and store_busy(account['store']):
        ui.say('  WhatsApp: already kept in sync on this Machine')
        return
    own = [u for u in store_units(account['store']) if u != name]
    if not unit.exists() and own:
        started = service.start(own[0], run=_ob().run)
        ui.say('  WhatsApp: synced by its own service again' if not started.returncode and getattr(ui, 'web', False) else
               f'  WhatsApp: synced by {own[0]}' if not started.returncode else f'  WhatsApp: start it with systemctl --user start {own[0]}')
        return
    if not service.available():
        ui.say(f'  WhatsApp: keep it synced yourself: {wacli} --store {account["store"]} sync --follow')
        return
    if not unit.exists() and not ui.yes('Keep WhatsApp synced in the background?', True):
        return
    parts = (wacli, '--store', account['store'], 'sync', '--follow', '--presence-mode', 'quiet',
             '--max-messages', '0', '--max-db-size', '2GB', '--max-reconnect', '10m')
    if wacli_release.supports_pictures(_ob().run([wacli, 'sync', '--help'], timeout=30).stdout):
        # People's profile pictures for the graph, asked read-only through this sync, at most 50 a day.
        parts += (wacli_release.PICTURE_FLAG, str(wacli_release.PICTURES_PER_DAY))
    unit.parent.mkdir(parents=True, exist_ok=True)
    if service.manager() == 'launchd':
        unit.write_text(service.plist_text(parts, unit=name, base=_ob().home(), throttle=30))
        started = service.enable(name, run=_ob().run)
        ui.say(f'  WhatsApp: synced by {service.label(name)}' if not started.returncode else
               f'  WhatsApp: start it with {service.hint("enable", name)}')
        return
    command = ' '.join(shlex.quote(str(part)) for part in parts)
    unit.write_text('[Unit]\nDescription=The Machine: keep WhatsApp (wacli) synced\nAfter=network-online.target\n\n'
                    f'[Service]\nExecStart={command}\nRestart=always\nRestartSec=30\nMemoryMax=512M\n\n[Install]\nWantedBy=default.target\n')
    _ob().run(['systemctl', '--user', 'daemon-reload'], timeout=30)
    started = _ob().run(['systemctl', '--user', 'enable', '--now', unit.name], timeout=60)
    ui.say(f'  WhatsApp: synced by {unit.name}' if not started.returncode else f'  WhatsApp: start it with systemctl --user enable --now {unit.name}')

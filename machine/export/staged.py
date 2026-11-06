"""The owner's "Import now" (or "Replace with this export") on an export staged in Settings, Export (moving.stage).

confirm() flags the staged summary `"confirmed": true`. A hosted Machine's server then applies it (moving.apply_staged)
with the service stopped. A self-hosted Machine restarts its own service (restart(), systemd or launchd, never the
Gateway), and the new process applies it at its start, before it serves (apply_confirmed). What happened is kept in
imported.json next to the export folder, so Settings says Imported, or why not, after the restart. The commands
(`assistant import --staged`) stay for a Machine that runs without a service manager."""
import datetime as dt
import json
import logging
import os
import sqlite3
from contextlib import closing
from pathlib import Path

import moving
import portable
import service

LOG = logging.getLogger('personal-assistant')
RESULT = 'imported.json'


def _now(now=None):
    return now or dt.datetime.now(dt.timezone.utc)


def _write(path, value):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as handle:
        handle.write(json.dumps(value))
    os.replace(temp, path)


def _summary_path(config_path):
    return moving._staged_dir(config_path) / 'staged.json'


def result_path(config_path):
    """imported.json in the private export folder next to the data folder (machine/app/export.py)."""
    data = Path(config_path).expanduser().parent
    return data.parent / f'.{data.name}.export' / RESULT


def confirm(config_path, now=None):
    """Mark the staged export as confirmed by the owner and return its summary; MoveError when there is none."""
    summary = moving.staged(config_path, now)
    if not summary:
        raise moving.MoveError('There is no export waiting to be imported; upload it again')
    summary['confirmed'] = True
    summary['confirmed_at'] = _now(now).isoformat(timespec='seconds')
    _write(_summary_path(config_path), summary)
    forget(config_path)
    return summary


def unconfirm(config_path):
    """Back to staged: the restart didn't happen, or the import at the start didn't go through."""
    summary = moving.staged(config_path)
    if summary and summary.pop('confirmed', None):
        summary.pop('confirmed_at', None)
        _write(_summary_path(config_path), summary)


def result(config_path, now=None):
    """What the last import at the start did, for a day: {'state': 'imported' | 'failed', ...} or None."""
    path = result_path(config_path)
    try:
        found = json.loads(path.read_text())
        at = dt.datetime.fromisoformat(found['at'])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if _now(now) - at > dt.timedelta(hours=moving.STAGED_HOURS):
        portable.shred(path)
        return None
    return found


def forget(config_path):
    portable.shred(result_path(config_path))


def restart(delay=3):
    """Restart this service from outside its own process (service.restart_later), as assistant.restart_self does: only
    when it runs under systemd or launchd. Returns whether a restart was scheduled."""
    if not can_restart():
        return False
    unit = None
    if service.manager() == 'systemd':
        try:
            unit = next((part for part in Path('/proc/self/cgroup').read_text().strip().split('/')[::-1] if part.endswith('.service')), None)
        except OSError:
            unit = None
    return service.restart_later(unit or service.UNIT_NAME, delay)


def can_restart():
    return service.running_as_service() and service.available()


def _settle(data):
    """A stopped service can leave SQLite's WAL files behind. Opening and closing each database folds them back in (the
    last connection to close removes them); a database another program still has open keeps its WAL, and the import
    then says so. Never deletes a WAL file itself."""
    for wal in sorted(Path(data).rglob('*-wal')):
        db = wal.with_name(wal.name[:-4])
        if not db.is_file():
            continue
        try:
            with closing(sqlite3.connect(db, timeout=5)) as conn:
                conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        except sqlite3.Error as error:
            LOG.warning('import at start: %s kept its WAL error=%s', db.name, type(error).__name__)


def apply_confirmed(config_path, config, now=None, apply=None):
    """At the service's start, before it takes its lock and serves: a self-hosted Machine puts a confirmed staged
    import in place (moving.apply_staged, force: the current data folder is kept as a copy first). Returns the
    result it saved in imported.json, or None when there was nothing to do. Never raises: a failed import puts the
    export back to staged with the reason, and the service starts as it was."""
    if (config or {}).get('manage_url'):
        return None  # hosted: the server applies it
    summary = moving.staged(config_path, now)
    if not summary or not summary.get('confirmed'):
        return None
    apply = apply or moving.apply_staged
    at = _now(now).isoformat(timespec='seconds')
    try:
        _settle(Path(config_path).expanduser().parent)
        done = apply(config_path, force=True)
        held = done.get('held') or {}
        found = {'state': 'imported', 'at': at, 'created_at': summary.get('created_at'), 'source': summary.get('source'),
                 'sends': int(held.get('sends', 0)) + int(held.get('sends_unsure', 0)) + int(held.get('telegram', 0)),
                 'boards': int(held.get('follow_up_boards', 0)), 'reconnect': len(done.get('reconnect') or [])}
        LOG.info('import at start: done files=%d', len(done.get('restored') or []))
    except moving.MoveError as error:
        unconfirm(config_path)
        found = {'state': 'failed', 'at': at, 'error': str(error)}
        LOG.warning('import at start: refused')
    except Exception as error:  # noqa: BLE001 - the service still starts; Settings says the import didn't go through
        unconfirm(config_path)
        found = {'state': 'failed', 'at': at, 'error': 'The import didn’t go through. The export is still here to try again.'}
        LOG.error('import at start failed error=%s', type(error).__name__)
    _write(result_path(config_path), found)
    return found

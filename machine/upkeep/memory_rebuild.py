"""OpenClaw's memory index rebuild that never ends by itself, and the quiet night that lets it finish.

OpenClaw rebuilds its memory index in full when the saved one no longer fits. One case: from 2026.11.2 the local
embeddinggemma model wants its task prefixes ("embedding input format" 1), and an index saved before has format 0.
On local embeddings a full rebuild of a big index runs for hours, into a copy next to the agent database
(<db>.memory-reindex-<uuid>). It gives up as soon as the agent runs a turn (MemoryBackgroundRebuildInterruptedError in
OpenClaw's log), and the next try starts from the beginning. The embedding cache it could reuse holds 50,000 entries,
fewer than a big index has chunks, so the tries don't add up. On a Machine with turns every few minutes (chat,
OpenClaw's jobs and heartbeat, The Machine's own reviews) it never ends, burns CPU on every try, and the installer's
bridge swap waits for it on every update.

stuck() says when that is so. The installer then stops waiting for the rebuild (installer.gateway_idle), and the
service opens one quiet window a night (step): from `start` local time until `end`, The Machine's background turns wait
(App.background_pause) and the OpenClaw jobs that run agent turns (the heartbeat among them) are turned off. OpenClaw's
own rebuild then runs to the end. The window closes once the saved index has the format its model wants, or at `end`,
and every job it turned off is turned on again. The owner's own turns (chat, Do it, Review now) still go; one only
makes that night's try start again.

Nothing here restarts the Gateway or reloads a plugin, and OpenClaw's own reindex command is not used: it runs a second
index manager beside the Gateway's, and OpenClaw coordinates rebuilds only inside one process ("foreign writers must
stop the Gateway"). Reads only file times, OpenClaw's log and the index's saved settings (read-only)."""
from __future__ import annotations

import datetime as dt
import json
import logging
import os
from pathlib import Path
import sqlite3
import subprocess
import time

LOG = logging.getLogger('personal-assistant')

INTERRUPTED = 'MemoryBackgroundRebuildInterruptedError'  # OpenClaw's log line for a try cut off by a turn
STUCK_INTERRUPTS = 3  # tries cut off in the last day that make a rebuild count as one that does not end by itself
LOG_DIR = Path('/tmp/openclaw')  # OpenClaw's file log, one a day (openclaw-YYYY-MM-DD.log), unless logging.file says
META_KEY = 'memory_index_meta_v1'  # the index's saved settings in the agent database (memory_index_meta)
REINDEX_FRESH = 120  # seconds since the last write to a rebuild's copy within which it counts as running
WINDOW = (23, 7)  # local hours: the quiet window opens in the hour from `start` and always closes at `end`
TURN_KINDS = ('agentTurn', 'heartbeat')  # OpenClaw jobs that run an agent turn; scripts and commands keep running
STATE = 'memory-rebuild.json'  # in the data folder: the window that is open or was last open, and the jobs it turned off


def local_search(settings):
    """Whether OpenClaw embeds its memory on this computer (memory.search.provider "local", or the same under
    agents.defaults.memorySearch). Only there does a rebuild take hours."""
    def provider(*keys):
        value = settings
        for key in keys:
            value = value.get(key) if isinstance(value, dict) else None
        return value
    return 'local' in (provider('memory', 'search', 'provider'), provider('agents', 'defaults', 'memorySearch', 'provider'))


def agent_dirs(settings, state_dir):
    """The folders OpenClaw keeps its agents' databases in: <state dir>/agents/<agent>/agent, and any agentDir
    openclaw.json sets (agents.list[].agentDir)."""
    found = []
    try:
        found = sorted((Path(state_dir) / 'agents').glob('*/agent'))
    except OSError:
        pass
    agents = settings.get('agents')
    for entry in (agents.get('list') if isinstance(agents, dict) else None) or []:
        value = entry.get('agentDir') if isinstance(entry, dict) else None
        if isinstance(value, str) and value.strip():
            found.append(Path(value.strip()).expanduser())
    return list(dict.fromkeys(found))


def wanted_format(model):
    """The embedding input format OpenClaw wants for this model: 1 for embeddinggemma (task prefixes), else 0."""
    return 1 if 'embeddinggemma' in str(model or '').lower() else 0


def index_meta(folder):
    """The saved settings of the memory index in an agent folder ({} when there is none), read-only."""
    try:
        paths = sorted(p for p in Path(folder).glob('*.sqlite') if '.sqlite.' not in p.name)
    except OSError:
        return {}
    for path in paths:
        try:
            with sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=5) as db:
                row = db.execute('SELECT value FROM memory_index_meta WHERE key=?', (META_KEY,)).fetchone()
        except sqlite3.Error:
            continue
        try:
            meta = json.loads(row[0]) if row else None
        except ValueError:
            meta = None
        if isinstance(meta, dict):
            return meta
    return {}


def format_behind(meta):
    """A saved local index whose embedding input format is older than its model wants: OpenClaw rebuilds it in full."""
    if not meta or meta.get('provider') != 'local':
        return False
    try:
        saved = int(meta.get('embeddingInputFormatVersion') or 0)
    except (TypeError, ValueError):
        saved = 0
    return wanted_format(meta.get('model')) > saved


def rebuild_running(folders, now):
    """A rebuild's copy written in the last REINDEX_FRESH seconds in any agent folder."""
    newest = 0.0
    for folder in folders:
        try:
            for path in Path(folder).glob('*.memory-reindex-*'):
                try:
                    newest = max(newest, path.stat().st_mtime)
                except OSError:
                    pass
        except OSError:
            continue
    return bool(newest) and now - newest < REINDEX_FRESH


def log_files(settings, today, days=1):
    """OpenClaw's log files for today and the `days` before: logging.file when openclaw.json sets one."""
    file = (settings.get('logging') or {}).get('file') if isinstance(settings.get('logging'), dict) else None
    if isinstance(file, str) and file.strip():
        return [Path(file.strip()).expanduser()]
    folder = Path(os.environ.get('ASSISTANT_OPENCLAW_LOG_DIR') or LOG_DIR)
    return [folder / f'openclaw-{(today - dt.timedelta(days=n)).isoformat()}.log' for n in range(days + 1)]


def line_time(line):
    """When an OpenClaw log line was written (its JSON `time`), as epoch seconds; None when it doesn't say."""
    try:
        found = json.loads(line).get('time')
        return dt.datetime.fromisoformat(found).timestamp() if isinstance(found, str) else None
    except (ValueError, AttributeError, TypeError):
        return None


def interruptions(paths, since):
    """Rebuild tries a turn cut off since `since` (epoch seconds), from OpenClaw's log."""
    count = 0
    for path in paths:
        try:
            with open(path, encoding='utf-8', errors='replace') as lines:
                for line in lines:
                    if INTERRUPTED in line and (line_time(line) or 0) >= since:
                        count += 1
        except OSError:
            continue
    return count


def stuck(settings, folders, now=None, today=None):
    """None, or why OpenClaw's memory rebuild does not end by itself: on local embeddings, a saved index in an older
    input format than its model wants, or at least STUCK_INTERRUPTS tries cut off in the last day.
    {'format_behind': bool, 'interrupted': n}."""
    if not local_search(settings):
        return None
    now = time.time() if now is None else now
    today = today or dt.date.fromtimestamp(now)
    behind = any(format_behind(index_meta(folder)) for folder in folders)
    cut = interruptions(log_files(settings, today), now - 86400)
    if behind or cut >= STUCK_INTERRUPTS:
        return {'format_behind': behind, 'interrupted': cut}
    return None


def read_state(folder):
    try:
        found = json.loads((Path(folder) / STATE).read_text())
    except (OSError, ValueError):
        return None
    return found if isinstance(found, dict) else None


def write_state(folder, state):
    path = Path(folder) / STATE
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(state, sort_keys=True))
    os.replace(temporary, path)


def holding(folder, now=None):
    """The open quiet window ({'until', ...}), or None. The Machine's background turns wait while one is open."""
    state = read_state(folder)
    now = time.time() if now is None else now
    if state and not state.get('closed') and float(state.get('until') or 0) > now:
        return state
    return None


def turn_jobs(openclaw, run=subprocess.run):
    """The enabled OpenClaw jobs that run an agent turn (TURN_KINDS), by id; None when the Gateway can't say."""
    try:
        result = run([openclaw, 'cron', 'list', '--json'], capture_output=True, text=True, timeout=60)
        jobs = json.loads(result.stdout or 'null').get('jobs') if result.returncode == 0 else None
    except (OSError, ValueError, AttributeError, subprocess.SubprocessError):
        return None
    if not isinstance(jobs, list):
        return None
    return [job['id'] for job in jobs if isinstance(job, dict) and job.get('enabled') and isinstance(job.get('id'), str)
            and ((job.get('payload') or {}).get('kind') in TURN_KINDS)]


def switch_jobs(openclaw, ids, on, run=subprocess.run):
    """Turn these OpenClaw jobs off or on again; the ids that did not change."""
    failed = []
    for job in ids:
        try:
            result = run([openclaw, 'cron', 'enable' if on else 'disable', job], capture_output=True, text=True, timeout=60)
            ok = result.returncode == 0
        except (OSError, subprocess.SubprocessError):
            ok = False
        if not ok:
            failed.append(job)
    return failed


def window_bounds(local_now, hours=WINDOW):
    """(opens, closes) of tonight's window as aware datetimes, when `local_now` is in its first hour; else None."""
    start, end = hours
    if local_now.hour != start:
        return None
    opens = local_now.replace(minute=0, second=0, microsecond=0)
    closes = opens.replace(hour=end)
    if closes <= opens:
        closes += dt.timedelta(days=1)
    return opens, closes


def finished(state, folders, now):
    """The rebuild the window was opened for is done: no rebuild runs, the saved index is in the format its model
    wants, and it was saved again since the window opened."""
    if rebuild_running(folders, now):
        return False
    metas = [index_meta(folder) for folder in folders]
    return not any(format_behind(meta) for meta in metas) and json.dumps(metas, sort_keys=True) != state.get('meta')


def close(folder, openclaw, state, why, now, run=subprocess.run):
    """Turn the window's jobs on again; the window stays closing (and holds nothing) until all of them are."""
    left = switch_jobs(openclaw, state.get('jobs') or [], True, run)
    write_state(folder, {**state, 'jobs': left, 'closed': now, 'outcome': why})
    if left:
        LOG.warning('memory rebuild window closing jobs_left=%s', len(left))
    else:
        LOG.info('memory rebuild window closed outcome=%s minutes=%s', why, int((now - float(state.get('opened') or now)) / 60))


def step(folder, openclaw, settings, state_dir, now, local_now, hours=WINDOW, run=subprocess.run):
    """One look (the service's retention worker, every ten minutes). An open window closes when its rebuild is done or
    its time is up; a closing one turns its jobs on again; in the first hour of tonight's window, a stuck rebuild opens
    one (once a night). `hours` None: never opens one, and closes any that is open. Returns what it did, for the log."""
    folders = agent_dirs(settings, state_dir)
    state = read_state(folder)
    if state and state.get('closed'):
        if state.get('jobs'):
            close(folder, openclaw, state, state.get('outcome') or 'ended', now, run)
            return 'closing'
    elif state:
        if hours is None or now >= float(state.get('until') or 0):
            close(folder, openclaw, state, 'ended', now, run)
            return 'ended'
        if finished(state, folders, now):
            close(folder, openclaw, state, 'done', now, run)
            return 'done'
        return 'open'
    if hours is None:
        return None
    bounds = window_bounds(local_now, hours)
    if not bounds or (state and state.get('night') == bounds[0].date().isoformat()):
        return None
    why = stuck(settings, folders, now, local_now.date())
    if not why:
        return None
    jobs = turn_jobs(openclaw, run)
    if jobs is None:
        return None  # the Gateway doesn't answer: no rebuild runs either
    metas = [index_meta(folder) for folder in folders]
    opened = {'opened': now, 'until': bounds[1].timestamp(), 'night': bounds[0].date().isoformat(), 'jobs': jobs,
              'meta': json.dumps(metas, sort_keys=True), 'why': why}
    write_state(folder, opened)  # first: a crash in between still turns every one of them on again
    left = switch_jobs(openclaw, jobs, False, run)
    LOG.info('memory rebuild window opened jobs=%s not_off=%s format_behind=%s interrupted=%s',
             len(jobs), len(left), why['format_behind'], why['interrupted'])
    return 'opened'

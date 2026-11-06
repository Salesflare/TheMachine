"""Claude Code and Codex job folders (agent_jobs.py: <database folder>/agent-jobs/<job>/work) give their room back
once nothing needs them. A job can fill its folder with gigabytes (a cloned site, an npm cache), and every handoff
makes a new one.

A finished job's work folder stays while:
- the job still runs, or was handed to this computer by the owner's hosted Machine and that side hasn't heard back;
- its to-do is still open (not done or dismissed): Try again and Ask for changes carry on in that folder, and the
  to-do's chat and preparations read and run what the job prepared there;
- it ended (or its to-do closed) less than GRACE_DAYS ago, and it is one of the KEEP_FINISHED newest such folders.

Then everything in it goes except what the job's answers list as its files (what the to-do links to stays where it
was, so its links keep working), BRIEF.md and the folder's Claude Code settings. The job's git history goes too. Its
turn transcripts stay next to the work folder, so its answers still show. Should the owner pick the job up again
later, it carries on in the same folder. A marker file notes what went; a job that ran again since counts afresh.
Folders without a job in the database are left alone. Runs in the nightly retention pass (retention.py)."""
from __future__ import annotations

import contextlib
import datetime as dt
import json
import logging
import os
from pathlib import Path
import re
import shutil
import sqlite3

import agent_jobs

LOG = logging.getLogger('personal-assistant')

GRACE_DAYS = 7
KEEP_FINISHED = 3
FINISHED = ('result', 'failed', 'cancelled')
CLOSED_CARDS = ('completed', 'rejected')
MARKER = 'work-removed.json'
KEEP_IN_WORK = {'BRIEF.md', '.claude'}
JOB = re.compile(r'aj_[0-9a-f]{16}')


def _when(value):
    try:
        found = dt.datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None
    return found if found.tzinfo else found.replace(tzinfo=dt.timezone.utc)


def _tables(db):
    return {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def why_kept(row, card_status, waiting_relayed):
    """Why a job's work folder must stay whatever its age, or None."""
    if row['status'] not in FINISHED:
        return 'running'
    if str(row['suggestion_id']).startswith(agent_jobs.RELAYED):
        return 'not reported back' if row['id'] in waiting_relayed else None
    if card_status is not None and card_status not in CLOSED_CARDS:
        return 'to-do open'
    return None


def linked_files(row, folder):
    """The work folder's files the job's answers list (the latest result's `files` and each turn's answer)."""
    job = dict(row)
    found = set()
    with contextlib.suppress(ValueError, TypeError):
        found |= {str(f.get('path')) for f in json.loads(job.get('files') or '[]') if isinstance(f, dict) and f.get('path')}
    for answer in agent_jobs.turn_answers(job, folder):
        found |= {str(f) for f in answer.get('files') or ()}
    return {Path(f).as_posix() for f in found if f and not Path(f).is_absolute() and '..' not in Path(f).parts}


def _size(path):
    with contextlib.suppress(OSError):
        return path.lstat().st_size
    return 0


def clear_work(folder, keep, dry_run=False):
    """Removes all of `folder`/work except `keep` (relative paths of regular files inside it) and KEEP_IN_WORK, and
    the job's own git history next to it. Never follows a link. Returns (bytes freed, files kept)."""
    work = folder / 'work'
    real = work.resolve()
    kept, freed = [], 0
    for top, dirs, files in os.walk(work, topdown=False, followlinks=False):
        here = Path(top)
        rel_dir = here.relative_to(work)
        if rel_dir.parts and rel_dir.parts[0] in KEEP_IN_WORK:
            continue
        for name in files + [d for d in dirs if (here / d).is_symlink()]:
            path, rel = here / name, (rel_dir / name).as_posix()
            if not rel_dir.parts and name in KEEP_IN_WORK and not path.is_symlink():
                continue
            if rel in keep and path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(real):
                kept.append(rel)
                continue
            freed += _size(path)
            if not dry_run:
                with contextlib.suppress(OSError):
                    path.unlink()
        if rel_dir.parts and not dry_run:
            with contextlib.suppress(OSError):
                here.rmdir()  # only when nothing in it was kept
    history = folder / 'git'
    if history.is_dir() and not history.is_symlink():
        for top, _dirs, files in os.walk(history):
            freed += sum(_size(Path(top) / f) for f in files)
        if not dry_run:
            shutil.rmtree(history, ignore_errors=True)
    return freed, sorted(kept)


def _marked(folder):
    with contextlib.suppress(OSError, ValueError):
        return json.loads((folder / MARKER).read_text())
    return None


def prune(connect, root, now=None, grace_days=GRACE_DAYS, keep=KEEP_FINISHED, dry_run=False):
    """Clears the work folders nothing needs any more (see the module's docstring). Returns a report without names
    or paths other than the job ids."""
    now = now or dt.datetime.now(dt.timezone.utc)
    root = Path(root)
    report = {'cleared': [], 'kept': {}, 'freed_bytes': 0, 'dry_run': dry_run}
    if not root.is_dir():
        return report
    with connect() as db:
        tables = _tables(db)
        if 'agent_jobs' not in tables:
            return report
        cards = 'suggestions' in tables
        rows = {r['id']: r for r in db.execute('SELECT j.*, ' + ('s.status' if cards else 'NULL') + ' AS card_status FROM agent_jobs j '
                                               + ('LEFT JOIN suggestions s ON s.id=j.suggestion_id' if cards else ''))}
        waiting = {r[0] for r in db.execute('SELECT job_id FROM agent_relayed WHERE reported=0')} if 'agent_relayed' in tables else set()
    finished = []
    for folder in sorted(root.iterdir()):
        row = rows.get(folder.name)
        if not JOB.fullmatch(folder.name) or folder.is_symlink() or not (folder / 'work').is_dir() or row is None:
            continue
        marked = _marked(folder)
        if marked and marked.get('job_updated_at') == row['updated_at']:
            continue  # cleared already, and the job hasn't run since
        reason = why_kept(row, row['card_status'], waiting)
        if reason:
            report['kept'][folder.name] = reason
            continue
        finished.append((_when(row['updated_at']) or now, folder, row))
    finished.sort(key=lambda item: item[0], reverse=True)
    for n, (ended, folder, row) in enumerate(finished):
        if n < keep and now - ended < dt.timedelta(days=grace_days):
            report['kept'][folder.name] = 'recent'
            continue
        with connect() as db:  # the owner may have picked it up again meanwhile
            current = db.execute('SELECT status,updated_at FROM agent_jobs WHERE id=?', (row['id'],)).fetchone()
        if not current or current['status'] not in FINISHED or current['updated_at'] != row['updated_at']:
            report['kept'][folder.name] = 'changed'
            continue
        try:
            freed, kept = clear_work(folder, linked_files(row, folder), dry_run=dry_run)
            if not dry_run:
                (folder / MARKER).write_text(json.dumps({'at': now.isoformat(), 'job_updated_at': row['updated_at'],
                                                         'freed_bytes': freed, 'kept': kept}) + '\n')
        except (OSError, sqlite3.Error) as error:  # tried again tomorrow
            LOG.warning('agent workspace prune error=%s', type(error).__name__)
            continue
        report['cleared'].append(folder.name)
        report['freed_bytes'] += freed
    return report

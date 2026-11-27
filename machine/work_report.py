"""What the background work did in the last 24 hours, per job, for the hosted health report (activity_report's `work`,
read by the cloud's daily check): counts only, never content or an error's words.

    {'reviews': {'ok': 12, 'failed': 1, 'auth': 0}, 'trip_extract': {'no_model': 3}, ...}

- ok, failed, auth: from the table each job keeps its runs in (JOBS), finished in the window; `auth` counts the
  failures whose error is about the sign-in or a missing model (AUTH), as on 2026-11-27, when every Gateway turn was
  "Not logged in" and nothing said so.
- no_model: the jobs that log "<job>: no model now" and keep no runs (trip extract, meeting prep, the handled and promise
  checks), counted from the log since the app started (Counter, on the app's LOG)."""
from __future__ import annotations

import collections
import datetime as dt
import logging
import re
import threading
import time

from machine.config import LOG

LAYER = 1  # counts of the background jobs' runs, for the hosted health report
WINDOW = 24 * 3600
# job -> (table, its status column, when it finished)
JOBS = {'reviews': ('review_runs', 'status', 'finished_at'), 'profiles': ('profile_runs', 'status', 'finished_at'),
        'preparations': ('preparations', 'status', 'updated_at'), 'routines': ('routine_runs', 'state', 'finished_at')}
OK = ('ok', 'done')
FAILED = ('error', 'failed', 'timed_out', 'lost', 'aborted')
AUTH = re.compile(r'(?i)not logged in|/login|signed[ _-]?out|unauthori[sz]ed|\b40[13]\b|api key|no model|invalid (?:token|key)|\bauth\b')
NO_MODEL = re.compile(r'([a-z][a-z ]{1,38}): no model now')

_seen = collections.defaultdict(collections.deque)
_lock = threading.Lock()


class Counter(logging.Filter):
    """Counts each "<job>: no model now" line the app logs (its time only); lets every line through."""

    def filter(self, record):
        found = NO_MODEL.fullmatch(str(record.msg))
        if found:
            with _lock:
                _seen[found.group(1).replace(' ', '_')].append(time.time())
        return True


if not any(isinstance(f, Counter) for f in LOG.filters):
    LOG.addFilter(Counter())


def report(db, current, now_s=None):
    """{job: counts} for the WINDOW before `current` (ISO time); jobs whose table is missing are left out.
    `db`: a plain sqlite3 connection to the events database."""
    since = (dt.datetime.fromisoformat(current) - dt.timedelta(seconds=WINDOW)).isoformat()
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    out = {}
    for job, (table, status, at) in JOBS.items():
        if table not in tables:
            continue
        rows = db.execute(f'SELECT {status},error FROM {table} WHERE {at}>=?', (since,)).fetchall()
        failed = [r for r in rows if r[0] in FAILED]
        out[job] = {'ok': sum(r[0] in OK for r in rows), 'failed': len(failed),
                    'auth': sum(bool(AUTH.search(str(r[1] or ''))) for r in failed)}
    now_s = time.time() if now_s is None else now_s
    with _lock:
        for job, times in _seen.items():
            while times and times[0] < now_s - WINDOW:
                times.popleft()
            if times:
                out.setdefault(job, {})['no_model'] = len(times)
    return out

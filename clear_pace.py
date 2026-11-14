"""Time to clear: how long the to-dos waiting for the owner take them, from their own pace on the dashboard.

The pace is the median time between two of the owner's decisions on the dashboard (Send, Do it, Snooze, Ask for
changes...: the decisions table, source 'dashboard') in the last PACE_DAYS. Only gaps of one sitting count (MIN_GAP to
MAX_GAP seconds): a gap of an hour is a break, not a slow decision. With fewer than MIN_SAMPLES such gaps the pace is
DEFAULT. The morning digest says "4 ready · about 2 min"; the dashboard's Ready header, under its count, "about 2 min".

A leaf module: only the standard library and i18n."""
from __future__ import annotations

import datetime as dt
import math
import statistics

from i18n import t

PACE_DAYS = 30
MIN_GAP, MAX_GAP = 2, 600
MIN_SAMPLES = 5
DEFAULT = 30
FLOOR, CEILING = 5, 300


def pace(stamps):
    """Seconds per action from decision times (ISO strings, any order): the median gap within a sitting, else DEFAULT."""
    times = sorted(at for at in (_when(s) for s in stamps) if at is not None)
    gaps = [b - a for a, b in zip(times, times[1:]) if MIN_GAP <= b - a <= MAX_GAP]
    if len(gaps) < MIN_SAMPLES:
        return DEFAULT
    return int(min(CEILING, max(FLOOR, round(statistics.median(gaps)))))


def seconds(db, current=None):
    """The owner's pace (seconds per action) from their dashboard decisions of the last PACE_DAYS."""
    import timeutil
    current = current or timeutil.clock()
    since = (current - dt.timedelta(days=PACE_DAYS)).isoformat()
    rows = db.execute("SELECT created_at FROM decisions WHERE source='dashboard' AND created_at>=? ORDER BY created_at DESC LIMIT 2000",
                      (since,)).fetchall()
    return pace(r[0] for r in rows)


def minutes(count, per):
    """Whole minutes for `count` actions at `per` seconds each, at least one."""
    return max(1, math.ceil(count * per / 60))


def line(count, per, lang=None):
    """"4 ready · about 2 min", or '' when nothing waits."""
    return t('{} ready · about {} min', count, minutes(count, per), lang=lang) if count else ''


def _when(value):
    try:
        at = dt.datetime.fromisoformat(str(value))
    except ValueError:
        return None
    return (at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)).timestamp()

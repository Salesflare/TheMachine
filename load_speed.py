"""How fast the dashboard opens for its owner: a small daily summary for the hosted health report.

The dashboard (dashboard/shell-speed.js) sends, a few page loads at a time, two times per load in milliseconds from the
start of the page: when the first drawing of To-dos was on screen (drawn), and when the whole page was drawn and answers
taps (tap). With each: whether that first drawing came from the device's kept copy (warm) or waited for the Machine
(cold), and the device kind, phone or desktop, the installed app or a browser. Nothing else: no address, no count of
to-dos, no user agent.

Per local day and kind (device, app or browser, warm or cold, and the Machine's version) the Machine keeps only a
histogram of each time in STEP-sized steps (5%), for KEEP_DAYS days. report() turns it into the count, median and p90.
A hosted Machine's agent passes that on with the activity counts (activity_report); a self-hosted one keeps it to
itself."""
from __future__ import annotations

import datetime as dt
import json
import math
import re

DAYS = 7
KEEP_DAYS = 8
STEP = 1.05
MOST_MS = 60_000  # a load slower than a minute is a page left in the background, not a measure
MOST_LOADS = 20  # per request: the page sends a few at a time
METRICS = ('drawn', 'tap')
VERSION = re.compile(r'release-\d{8}-\d{4}|[0-9a-f]{7,12}')


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS load_speed(day TEXT NOT NULL,kind TEXT NOT NULL,version TEXT NOT NULL,'
               'metric TEXT NOT NULL,bins TEXT NOT NULL,PRIMARY KEY(day,kind,version,metric))')


def kind_of(load):
    """'phone-app-warm' and the like, or None for a load that isn't what the page sends."""
    if not isinstance(load, dict) or not all(type(load.get(k)) is bool for k in ('phone', 'app', 'warm')):
        return None
    return '-'.join(('phone' if load['phone'] else 'desktop', 'app' if load['app'] else 'browser',
                     'warm' if load['warm'] else 'cold'))


def times(load):
    """(drawn, tap) in whole ms, or None when either is not a plain number in range or tap comes before drawn."""
    values = [load.get(k) for k in METRICS]
    if not all(type(v) in (int, float) and 0 < v <= MOST_MS for v in values) or values[1] < values[0]:
        return None
    return tuple(round(v) for v in values)


def step_of(ms):
    return round(math.log(max(ms, 1)) / math.log(STEP))


def ms_of(step):
    return round(STEP ** step)


def note(db, loads, day, version):
    """Add the page's loads (a list of dicts) to `day`'s histograms. Returns how many were kept; the rest are dropped."""
    version = version if isinstance(version, str) and VERSION.fullmatch(version) else 'unknown'
    kept = 0
    for load in (loads if isinstance(loads, list) else [])[:MOST_LOADS]:
        kind, found = kind_of(load), times(load) if isinstance(load, dict) else None
        if not kind or not found:
            continue
        for metric, ms in zip(METRICS, found):
            row = db.execute('SELECT bins FROM load_speed WHERE day=? AND kind=? AND version=? AND metric=?',
                             (day, kind, version, metric)).fetchone()
            bins = json.loads(row[0]) if row else {}
            bins[str(step_of(ms))] = bins.get(str(step_of(ms)), 0) + 1
            db.execute('INSERT INTO load_speed(day,kind,version,metric,bins) VALUES(?,?,?,?,?) ON CONFLICT(day,kind,version,metric) '
                       'DO UPDATE SET bins=excluded.bins', (day, kind, version, metric, json.dumps(bins, sort_keys=True)))
        kept += 1
    oldest = (dt.date.fromisoformat(day) - dt.timedelta(days=KEEP_DAYS)).isoformat()
    db.execute('DELETE FROM load_speed WHERE day<?', (oldest,))
    return kept


def percentile(bins, share):
    """The time (ms) at `share` of the loads in a histogram, nearest rank."""
    steps = sorted((int(k), n) for k, n in bins.items())
    rank, seen = max(1, math.ceil(share * sum(n for _, n in steps))), 0
    for step, n in steps:
        seen += n
        if seen >= rank:
            return ms_of(step)
    return ms_of(steps[-1][0])


def report(db, today):
    """[{'day', 'device', 'app', 'warm', 'version', 'count', 'drawn_median', 'drawn_p90', 'tap_median', 'tap_p90'}]
    for the last DAYS local days up to `today` (YYYY-MM-DD), oldest first. Numbers and those labels only."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='load_speed'").fetchone():
        return []
    since = (dt.date.fromisoformat(today) - dt.timedelta(days=DAYS - 1)).isoformat()
    found = {}
    for day, kind, version, metric, bins in db.execute(
            'SELECT day,kind,version,metric,bins FROM load_speed WHERE day>=? AND day<=? ORDER BY day,kind,version', (since, today)):
        if metric not in METRICS:
            continue
        device, app, warm = kind.split('-')
        entry = found.setdefault((day, kind, version), {'day': day, 'device': device, 'app': app == 'app', 'warm': warm == 'warm',
                                                         'version': version})
        bins = json.loads(bins)
        entry['count'] = sum(bins.values())
        entry[metric + '_median'], entry[metric + '_p90'] = percentile(bins, 0.5), percentile(bins, 0.9)
    return [e for e in found.values() if all(m + '_median' in e for m in METRICS)]

"""Whether the reviews of new signals wait by design right now, in the review worker's own words (App.review_step), for
whoever watches a hosted Machine from outside: the AI plan's usage window ('5h' or 'week'), a usage limit reached
('limit'), the quiet night for OpenClaw's memory rebuild ('memory') or the night pause ('night'), since when and until
when. The hosting agent reports it (report) so a stall alert doesn't have to guess the app's rules from outside: the
usage windows of a Claude plan are only known here (machine/model_usage.py). The kind and times only, never content.

Kept in the database, since the agent is another process: in milestones, at = when the worker last looked."""
import datetime as dt
import json

from timeutil import now

NAME = 'review_pause'
KEEP_SECONDS = 600   # an unchanged answer is written again this often, so a worker that stopped looking shows
SAME_PAUSE = 3600    # a reset time read a little different is the same pause; further off, a new one


def _read(db):
    row = db.execute('SELECT at,detail FROM milestones WHERE name=?', (NAME,)).fetchone()
    try:
        found = json.loads(row[1]) if row else None
        return (row[0], found) if isinstance(found, dict) else (None, {})
    except (TypeError, ValueError):
        return None, {}


def note(db, found):
    """The worker just looked: `found` is why a review may not start now ({'window', 'until'} with `until` an epoch
    second or None), None when one may. Written when it changed, and every KEEP_SECONDS."""
    at, kept = _read(db)
    stamp = now()
    until = int(found['until']) if found and found.get('until') else None
    new = {'window': found['window'], 'until': until, 'since': stamp} if found else {'window': None}
    old = kept.get('until')
    if found and kept.get('window') == found['window'] and kept.get('since') \
            and (until == old or (until and old and abs(until - old) < SAME_PAUSE)):
        new['since'] = kept['since']
    if at and new == kept and (dt.datetime.fromisoformat(stamp) - dt.datetime.fromisoformat(at)).total_seconds() < KEEP_SECONDS:
        return
    db.execute('INSERT OR REPLACE INTO milestones(name,at,detail) VALUES(?,?,?)', (NAME, stamp, json.dumps(new, sort_keys=True)))


def report(db):
    """{'window' (None: they don't wait), 'until' (epoch seconds), 'since', 'checked_at'}, or None before the first look.
    `db`: a plain connection to the events database."""
    at, kept = _read(db)
    return {'window': kept.get('window'), 'until': kept.get('until'), 'since': kept.get('since'), 'checked_at': at} if at else None

"""How often background work has to pace (model_budget.py), for The Machine team (docs/help/error-reports.md#pacing).

Background work waits when the sign-in's 5-hour window is past SHORT_PAUSE (FIRST_PAUSE for the first look) or the
weekly window is past its share for the day. That keeps room for the owner's own chats, but waiting work is a worse
experience, so the team counts how often it happens. Kept here, per pacing stretch: when it started, which window and
threshold, how long it lasted, and how many jobs waited (distinct ones, by an id that never leaves this Machine).

Once a day the finished days go to the control plane, with the error reports and under the same Settings switch
(Send error reports), over the Network: POST /errors {"action": "pacing", "day", "starts": [{"hour", "window",
"threshold", "minutes", "jobs"}]}. Only counts and durations: no content, no names, no job ids. Off: nothing is
recorded or sent, and what waited is deleted. Nothing new is shown to the owner. Kept KEEP_DAYS here."""
from __future__ import annotations

import contextlib
import datetime as dt
import time

import error_feed

SCHEMA = '''
CREATE TABLE IF NOT EXISTS pacing_starts(id INTEGER PRIMARY KEY,started_at TEXT NOT NULL,ended_at TEXT,win TEXT NOT NULL,
  threshold INTEGER NOT NULL,jobs INTEGER NOT NULL DEFAULT 0,until TEXT);
CREATE TABLE IF NOT EXISTS pacing_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL);
'''
KEEP_DAYS = 30
BACK_DAYS = 7           # a finished day is sent at most this late
STARTS_MAX = 48         # pacing starts one day carries at most
LONGEST = {'5h': 5 * 3600, 'week': 86400}  # a stretch nobody saw end (the service was down) counts this long at most
SEND_EVERY = 6 * 3600


def ensure(db):
    for statement in SCHEMA.split(';'):
        if statement.strip():
            db.execute(statement)


def iso(seconds):
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).isoformat(timespec='seconds')


def epoch(text):
    return dt.datetime.fromisoformat(text).timestamp()


def threshold(found):
    """The percent a pause began at (model_budget.pause): 65 or 85 for the 5-hour window, the day's share of the week."""
    return int(found.get('threshold') or 0)


class Tracker:
    """The open pacing stretch, in memory, written only when one starts, a new job waits in it, or it ends. Fed by every
    budget check (assistant.background_pause): `found` is model_budget.pause's answer, None when work may go."""

    def __init__(self, connect):
        self.connect, self.open, self.jobs = connect, None, set()

    def _db(self, db):
        return contextlib.nullcontext(db) if db is not None else self.connect()

    def note(self, found, job=None, first=False, now_s=None, db=None):
        """One budget check. A stretch is one window pacing (5h or week); its threshold is the highest it reached (85:
        even the first look waited). A check for the first look that may go doesn't end it: the others still wait.
        `db`: the caller's connection when it is in a write transaction, which a connection of our own would wait on."""
        now_s = time.time() if now_s is None else now_s
        try:
            if self.open is None:
                self._resume(db)
            if not found:
                return None if first else self._close(now_s, db)
            window, limit = found.get('window') or '5h', threshold(found)
            if self.open and (self.open['window'] != window or (self.open.get('until') and now_s > self.open['until'])):
                self._close(now_s, db)  # another window, or the same one again after it reset: a new stretch
            if not self.open:
                with self._db(db) as conn:
                    ensure(conn)
                    if not error_feed.on(conn):
                        return None  # Send error reports off: nothing is counted
                    until = iso(found['until']) if found.get('until') else None
                    row_id = conn.execute('INSERT INTO pacing_starts(started_at,win,threshold,jobs,until) VALUES(?,?,?,0,?)',
                                        (iso(now_s), window, limit, until)).lastrowid
                self.open, self.jobs = {'id': row_id, 'window': window, 'threshold': limit, 'started': now_s, 'jobs': 0,
                                        'until': found.get('until')}, set()
            changed = False
            if window == '5h' and limit > self.open['threshold']:
                self.open['threshold'], changed = limit, True
            if job and job not in self.jobs and len(self.jobs) < 1000:
                self.jobs.add(job)
                self.open['jobs'] += 1
                changed = True
            if changed:
                with self._db(db) as conn:
                    conn.execute('UPDATE pacing_starts SET jobs=?,threshold=? WHERE id=?', (self.open['jobs'], self.open['threshold'], self.open['id']))
            return self.open['id']
        except Exception:
            return None  # counting never holds up the work itself

    def _resume(self, db=None):
        """A stretch the service was in when it stopped: carried on (its jobs counted again from here), or ended."""
        with self._db(db) as db:
            ensure(db)
            row = db.execute('SELECT id,started_at,win,threshold,jobs,until FROM pacing_starts WHERE ended_at IS NULL ORDER BY id DESC LIMIT 1').fetchone()
        self.open = {'id': row[0], 'started': epoch(row[1]), 'window': row[2], 'threshold': row[3], 'jobs': row[4],
                     'until': epoch(row[5]) if row[5] else None} if row else False

    def _close(self, now_s, db=None):
        if not self.open:
            self.open = False
            return None
        o, end = self.open, now_s
        if o.get('until'):
            end = min(end, max(o['until'], o['started']))  # it ended when the window reset, at the latest
        end = min(end, o['started'] + LONGEST.get(o['window'], LONGEST['5h']))
        with self._db(db) as db:
            db.execute('UPDATE pacing_starts SET ended_at=?,jobs=? WHERE id=? AND ended_at IS NULL', (iso(max(end, o['started'])), o['jobs'], o['id']))
        self.open, self.jobs = False, set()
        return None


def day_payload(db, day):
    """One finished day's pacing starts, as they go: hour, window, threshold, minutes, jobs. None when it had none."""
    rows = db.execute('SELECT started_at,ended_at,win,threshold,jobs FROM pacing_starts WHERE ended_at IS NOT NULL AND substr(started_at,1,10)=? '
                      'ORDER BY started_at LIMIT ?', (day, STARTS_MAX)).fetchall()
    starts = [{'hour': int(r[0][11:13]), 'window': r[2], 'threshold': int(r[3]),
               'minutes': max(0, round((epoch(r[1]) - epoch(r[0])) / 60)), 'jobs': int(r[4])} for r in rows]
    return {'action': 'pacing', 'day': day, 'starts': starts} if starts else None


def send(connect, call, current=None):
    """The finished days not sent yet (the last BACK_DAYS), one call each, at most every SEND_EVERY. Returns days sent."""
    current = current or dt.datetime.now(dt.timezone.utc)
    with connect() as db:
        ensure(db)
        if not error_feed.on(db):
            db.execute('DELETE FROM pacing_starts')
            return 0
        db.execute('DELETE FROM pacing_starts WHERE started_at<?', ((current - dt.timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds'),))
        row = db.execute("SELECT value FROM pacing_prefs WHERE key='tried_at'").fetchone()
        if row and row[0] > (current - dt.timedelta(seconds=SEND_EVERY)).isoformat(timespec='seconds'):
            return 0
        db.execute("INSERT INTO pacing_prefs(key,value) VALUES('tried_at',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                   (current.isoformat(timespec='seconds'),))
        last = (db.execute("SELECT value FROM pacing_prefs WHERE key='sent_day'").fetchone() or [''])[0]
        today = current.date()
        days = [(today - dt.timedelta(days=k)).isoformat() for k in range(BACK_DAYS, 0, -1)]
        payloads = [p for p in (day_payload(db, d) for d in days if d > last) if p]
    sent = 0
    for payload in payloads:
        answer = call('POST', '/errors', payload)
        if not (isinstance(answer, dict) and answer.get('ok') is True):
            break
        with connect() as db:
            db.execute("INSERT INTO pacing_prefs(key,value) VALUES('sent_day',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (payload['day'],))
        sent += 1
    else:
        with connect() as db:  # nothing left before today: the days with no pacing count as sent too
            db.execute("INSERT INTO pacing_prefs(key,value) VALUES('sent_day',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       ((today - dt.timedelta(days=1)).isoformat(),))
    return sent

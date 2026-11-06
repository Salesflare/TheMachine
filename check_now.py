"""Check now (docs/help/cards.md#check-now): every source is read and a review of what came in starts right away,
outside the usual rhythm. Usually each source is read every few minutes (poll_seconds) and a review of what came in
starts once enough new messages wait or the oldest one waited 15 minutes (review_worker min_signals, max_wait_minutes). Nothing gates either
by the time of day: there are no quiet hours for reading, and a hosted Machine never pauses while it is paid for.

From the To-dos page head (the dashboard and the phone app, which loads the same dashboard) and from chat, where the
agent runs `assistant check`. One check at a time: a press while one runs, or within REST_SECONDS after it ended,
joins it instead of starting another, so repeated taps never stack reads or reviews.

A check: 'reading' while each source that waits for its next read reads now (the collector's own read, woken early:
its pacing, locks and error handling stay as they are), then 'reviewing' while the review it asked for runs, then done
with how many new to-dos it brought. Slow sources (SLOW_SERVICES, or read every SLOW_POLL seconds or less often) and
one waiting out an error keep their own pace. Kept in memory only: a restart forgets a check, which then just ends."""
from __future__ import annotations

import datetime as dt
import threading
import time

import abilities

REST_SECONDS = 60             # after a check ends, a new press within this long shows it instead of starting another
READ_WAIT = 180               # the sources' reads, at most this long
REVIEW_WAIT = 30 * 60         # the review it asked for, at most this long
REVIEW_START_WAIT = 90        # a review asked for that doesn't start within this long (nothing to review after all)
SLOW_POLL = 600
SLOW_SERVICES = ('linkedin', 'x', 'salesflare')  # read in the Machine's browser, a paid API, a CRM's long rounds
ACTIVE = ('starting', 'running', 'recovering')


def fast(config, account):
    """A source Check now reads: it brings in signals and is read every few minutes by nature."""
    poll = account.get('poll_seconds', config.get('poll_seconds', 300))
    return abilities.signals_on(account) and account.get('service') not in SLOW_SERVICES and poll < SLOW_POLL


def reviews(db, queue, min_signals):
    """The status the owner cares about: when messages were last reviewed into to-dos and when the next review is due.
    reviewing and reading: a review runs, or a mailbox's first import comes in, whoever started it (the first look, the
    usual rhythm or a check), so Check now shows busy then too. `queue` is the service's review_queue (how many wait and when the next review starts: at min_signals waiting, or
    once the oldest waited max_wait_minutes); soon: the batch is (nearly) full, so it starts within minutes."""
    row = db.execute("SELECT max(finished_at) FROM review_runs WHERE status='ok'").fetchone()
    waiting = (queue or {}).get('waiting') or 0
    return {'reviewed': row[0] if row else None, 'reviewing': reviewing(db), 'waiting': waiting,
            'reading': (queue or {}).get('why') == 'mail',  # a mailbox's first import still coming in
            'next_review': (queue or {}).get('starts_at') if waiting else None,
            'soon': bool(waiting) and waiting >= min_signals * 3 / 4}


def epoch(text):
    return dt.datetime.fromisoformat(text).timestamp()


def iso(seconds):
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).isoformat(timespec='seconds') if seconds else None


def waiting(db):
    """New messages a review still has to look at."""
    return db.execute('SELECT count(*) FROM events WHERE analyzed_version<version').fetchone()[0]


def reviewing(db):
    return bool(db.execute('SELECT 1 FROM review_runs WHERE status IN (%s) LIMIT 1' % ','.join('?' * len(ACTIVE)), ACTIVE).fetchone())


def new_todos(db, since):
    return db.execute('SELECT count(*) FROM suggestions WHERE created_at>=?', (iso(since),)).fetchone()[0]


class Check:
    """The one check, in memory: started, read (the sources' reads ended), ended, and how many new to-dos it brought."""

    def __init__(self):
        self.lock = threading.Lock()
        self.started = self.read = self.ended = 0.0
        self.found = None

    def start(self, now_s):
        """True when a new check starts; False when one runs, or one ended under REST_SECONDS ago."""
        with self.lock:
            if self.phase() or (self.ended and now_s - self.ended < REST_SECONDS):
                return False
            self.started, self.read, self.ended, self.found = now_s, 0.0, 0.0, None
            return True

    def phase(self):
        if not self.started or self.ended:
            return None
        return 'reviewing' if self.read else 'reading'

    def view(self, status):
        """For the dashboard (state.check): phase ('reading', 'reviewing' or None), the last check's start, end and
        new to-dos, and `status` (reviews(): the last review, the next one and how many messages wait)."""
        return {**status, 'phase': self.phase(), 'started': iso(self.started), 'ended': iso(self.ended), 'found': self.found,
                'rest_until': iso(self.ended + REST_SECONDS) if self.ended else None}


def run(check, app):
    """The check itself, on its own thread: wake the resting sources, wait for their reads, ask for a review, wait for
    it, end. `app` is the service (assistant.App): its collectors, review worker, store and stop."""
    try:
        started = check.started
        woken = app.wake_collectors(lambda account: fast(app.config, account))
        deadline = time.monotonic() + READ_WAIT
        while woken and not app.stop.is_set() and time.monotonic() < deadline:
            if all(app.collector_reads.get(account_id, 0) >= started for account_id in woken):
                break
            app.stop.wait(1)
        check.read = time.time()
        if not (app.config.get('review_worker') or {}).get('enabled'):
            return
        with app.store.connect() as db:
            new = waiting(db)
        if not new:
            return
        asked = time.time()
        app.review_asked, app.review_paused = asked, None
        deadline = time.monotonic() + REVIEW_WAIT
        while not app.stop.is_set() and time.monotonic() < deadline:
            app.stop.wait(2)
            if getattr(app, 'review_paused', None):
                break  # a usage limit holds it (the dashboard's banner says so)
            with app.store.connect() as db:
                running = reviewing(db)
            pending = getattr(app, 'review_asked', 0) == asked
            if not running and not pending:
                break  # it ran and ended
            if pending and not running and time.time() - asked > REVIEW_START_WAIT:
                break  # nothing it could review after all
    finally:
        try:
            with app.store.connect() as db:
                check.found = new_todos(db, check.started)
        except Exception:  # noqa: BLE001 - the check still ends
            check.found = None
        check.ended = time.time()

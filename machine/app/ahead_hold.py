"""Drafts ahead while reviews are far behind (machine/store/ahead_hold.py): whether a draft a review asks for waits, and the
step that starts the ones that waited. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import time
import uuid

from machine.config import LOG
from machine.store import ahead_hold, review_catch_up
from machine.store.cards import pressing
from machine.store.review import signal_weight
from timeutil import now

CHECK_SECONDS = 60  # how often the step asks again whether the Machine is still behind


class AheadHoldApp:
    ACTIONS = {}  # no actions: suggest asks, the preparation worker runs the step

    def plan_windows(self):
        """Whether the AI sign-in reports usage windows that count now. An API key, Azure or a local model has none, and
        neither has a Machine whose fallback billed apart carries the work: nothing to keep for reviews, no hold. None:
        not read yet (a restart)."""
        if getattr(self, 'model_usage', None) is None and not self.fallback_covers():
            return None
        return any(isinstance(w.get('used'), (int, float)) for p in self.paced_usage() or [] for w in p.get('windows') or [])

    def reviews_behind(self, db):
        """Reviews are on, on a plan, and far behind (review_catch_up.waits); while drafts already wait, until caught up."""
        if not (self.config.get('review_worker') or {}).get('enabled') or not self.plan_windows():
            return False
        runs = ahead_hold.EASE_RUNS if ahead_hold.under_way(db) else review_catch_up.BEHIND_RUNS
        return review_catch_up.waits(db, [a['id'] for a in self.config['accounts']], signal_weight, dt.datetime.fromisoformat(now()), runs)

    def ahead_waits(self, args):
        """Whether the draft a review asked for with this to-do waits: never pressing work, one that closes soon, a new
        owner's first ones or a to-do another turn saves."""
        current = dt.datetime.fromisoformat(now())
        if pressing(args.get('urgent') is True, args.get('due')) or args.get('expires_at') and ahead_hold.soon(args['expires_at'], current):
            return False
        with self.store.connect() as db:
            return (ahead_hold.from_review(db, args['event_ids']) and self.store.first_magic_done(db) and not ahead_hold.new_owner(db, current)
                    and self.reviews_behind(db))

    def ahead_hold_step(self):
        """Every few seconds: the drafts that waited, dropped or started (ahead_hold.ready), inside the usage budget and
        the day's room, as many as can run. Pressing ones and those the owner opened first, the others one after
        another. Returns the to-dos started."""
        current = dt.datetime.fromisoformat(now())
        per_day = int(self.config.get('prepare_ahead_per_day', 10))
        with self.store.connect() as db:
            if ahead_hold.empty(db):
                return []
            ended = False
            if time.monotonic() - getattr(self, 'ahead_behind_at', -CHECK_SECONDS) >= CHECK_SECONDS:
                self.ahead_behind_at = time.monotonic()
                ended = self.plan_windows() is not None and ahead_hold.under_way(db) and not self.reviews_behind(db)
            if ended:
                LOG.info('drafts ahead let go why=caught_up count=%s', ahead_hold.let_go(db, now()))
            if self.config.get('prepare_ahead', True) is False or per_day <= 0:
                LOG.info('drafts ahead dropped why=off count=%s', ahead_hold.clear(db))
                return []
            stale, ready = ahead_hold.stale(db, current), ahead_hold.ready(db, current, pressing)
        # What holds a draft ahead once it is queued (preparation_step): held back there, its to-do would only show as
        # waiting, so until one can start it stays as it is
        if ready and self.background_pause(job='ahead:' + ready[0][0]):
            ready = []
        if not stale and not ready:
            return []
        started = []
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for sid, why in ahead_hold.stale(db, current).items():
                ahead_hold.gone(db, sid)
                LOG.info('draft ahead dropped why=%s', why)
            for sid, why in ahead_hold.ready(db, current, pressing) if ready else []:
                free, going = ahead_hold.slots(db, current, int(self.config.get('preparation_concurrency', 3)))
                if why != 'pressing' and (not free or why != 'opened' and going):
                    continue
                if not self.store.ahead_started_room(db, per_day):  # all of it: its place was taken when its to-do was saved
                    break
                ahead_hold.gone(db, sid)
                self.store.start_ahead(db, sid, ahead_hold.DECISION + uuid.uuid4().hex, told=True)
                LOG.info('draft ahead started why=%s', why)
                started.append(sid)
        return started

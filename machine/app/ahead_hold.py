"""Drafts ahead while reviews are far behind (machine/store/ahead_hold.py): whether a draft a review asks for waits, and the
step that starts the ones that waited. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import time
import uuid

import model_budget
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
        the day's room. Pressing ones and those the owner opened at once, the others one after another. Returns the
        to-dos started."""
        current = dt.datetime.fromisoformat(now())
        with self.store.connect() as db:
            if not ahead_hold.kept(db):
                return []
            ended = False
            if time.monotonic() - getattr(self, 'ahead_behind_at', -CHECK_SECONDS) >= CHECK_SECONDS:
                self.ahead_behind_at = time.monotonic()
                ended = self.plan_windows() is not None and ahead_hold.under_way(db) and not self.reviews_behind(db)
        if self.config.get('prepare_ahead', True) is False:
            with self.store.connect() as db:
                LOG.info('drafts ahead dropped why=off count=%s', ahead_hold.clear(db))
            return []
        # Held back now, a draft would only show as waiting: its to-do stays as it is until one can start
        paused = self.background_pause(owner=True) or model_budget.pause(self.paced_usage())
        per_day, started = int(self.config.get('prepare_ahead_per_day', 10)), []
        with self.store.connect() as db:
            if not ended and not ahead_hold.stale(db, current) and (paused or not ahead_hold.ready(db, current, pressing)):
                return []
            db.execute('BEGIN IMMEDIATE')
            if ended:
                LOG.info('drafts ahead let go why=caught_up count=%s', ahead_hold.let_go(db, now()))
            for sid, why in ahead_hold.stale(db, current).items():
                ahead_hold.gone(db, sid)
                LOG.info('draft ahead dropped why=%s', why)
            for sid, why in [] if paused else ahead_hold.ready(db, current, pressing):
                # The whole day's room: its place in it was taken when its to-do was saved (Store.ahead_room)
                if not self.store.ahead_started_room(db, per_day) or why not in ('pressing', 'opened') and ahead_hold.one_going(db):
                    continue
                ahead_hold.gone(db, sid)
                self.store.start_ahead(db, sid, ahead_hold.DECISION + uuid.uuid4().hex)
                LOG.info('draft ahead started why=%s', why)
                started.append(sid)
        return started

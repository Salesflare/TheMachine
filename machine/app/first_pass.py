"""The first pass's small model call (machine/store/first_pass.py), from the review worker: before a review reads new
signals, the automated ones are sorted in batches by the main sign-in's small model (models.small_model), and what
clearly needs nothing is set aside, so the big model reads less. A call goes only within the usage budget like every
background turn (model_budget, `signals`: new signals), in a thread of its own so the worker never waits on it, at most
one at a time and one every GAP_SECONDS. Off with review_worker first_pass false, without a small model on the
sign-in, and before the first review finished: then every signal goes to the review as before. A call that fails sorts
nothing (FAIL_SECONDS before the next); what it didn't sort goes to the review as before."""
import threading
import time

import help_chat
from machine.config import LOG
from machine.store import first_pass
from models import small_model

GAP_SECONDS = 60
FAIL_SECONDS = 900
TIMEOUT = 120


class FirstPassApp:
    ACTIONS = {}  # no actions: the review worker runs it

    def first_pass_on(self):
        settings = self.config.get('review_worker') or {}
        return bool(settings.get('enabled')) and settings.get('first_pass', True) is not False

    def first_pass_step(self):
        """Start one batch of the first pass when one is due: the thread it runs in, else None."""
        if not self.first_pass_on() or self.__dict__.get('_first_pass_busy') or time.monotonic() < self.__dict__.get('_first_pass_next', 0):
            return None
        model = small_model(self.config)
        if not model:
            return None
        with self.store.connect() as db:
            if not db.execute("SELECT 1 FROM review_runs WHERE status='ok' LIMIT 1").fetchone():
                return None  # the first look reads its week as it is
        self._first_pass_next = time.monotonic() + GAP_SECONDS
        rows = self.store.first_pass_due()
        if not rows or self.background_pause(job='first_pass', signals=True):
            return None
        with self.store.connect() as db:
            own = self.store.review_own_addresses(db)
        self._first_pass_busy = True
        thread = threading.Thread(target=self.first_pass_run, args=(rows, model, own), name='first-pass', daemon=True)
        thread.start()
        return thread

    def first_pass_run(self, rows, model, own=()):
        """One small model call over rows, and its sort kept (Store.first_pass_keep)."""
        try:
            ask = self.__dict__.get('first_pass_model')  # tests: (prompt) -> reply
            text = first_pass.prompt(rows, own)
            reply = ask(text) if ask else help_chat.openclaw_model_run(self.config, text, model[0], model[1], timeout=TIMEOUT)
            found = first_pass.aside(reply, [r['id'] for r in rows])
            if found is None:
                raise ValueError('no_result')
            kept = self.store.first_pass_keep(rows, found, model[0])
            LOG.info('first pass sorted=%s aside=%s', len(rows), kept)
        except Exception as error:  # nothing sorted: the review reads them as before
            self._first_pass_next = time.monotonic() + FAIL_SECONDS
            LOG.warning('first pass error=%s', type(error).__name__)
        finally:
            self._first_pass_busy = False

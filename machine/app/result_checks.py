"""Result checks, the turn (machine/store/result_checks.py has the rows): what came for a waiting to-do (its page, the
message that brought the result) read against what was agreed, in one small background turn, before it closes. A
mixin of assistant.App (APP_MIXINS), stepped by the preparation worker.

One check per step, at most every EVERY seconds, in its own thread like the handled check: claimed in one short write,
asked outside any transaction, kept in another short write that holds only for that claim. No model, or a turn that
fails twice: it comes back for a look, never a close. Tests and the sandbox stand in with result_check_model(config,
prompt)."""
import threading
import time

from machine import model_reply
from machine.config import LOG
from machine.prompts.result_check import result_check_prompt
from machine.store import result_checks
from machine.store.review import own_message
from models import background_model, openclaw_model
from timeutil import now

EVERY = 20  # seconds between steps
SECONDS = 90  # one turn at most


class ResultChecksApp:
    ACTIONS = {}

    def result_check_step(self):
        if time.monotonic() - self.__dict__.get('result_checked', -EVERY) < EVERY:
            return None
        self.result_checked = time.monotonic()
        thread = self.__dict__.get('_result_check_thread')
        if thread and thread.is_alive():
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            result_checks.given_up(db, now())
            own = self.store.review_own_addresses(db)
            jobs = result_checks.claim(db, now(), mine=lambda e: own_message(e, self.store.owner_user_ids, own))
        if not jobs:
            return None
        if getattr(self, 'result_check_model', None):
            return self.result_check_run(jobs[0])
        self._result_check_thread = threading.Thread(target=self.result_check_run, args=(jobs[0],), name='result-check', daemon=True)
        self._result_check_thread.start()
        return None

    def result_check_run(self, job):
        """One turn for one check; its answer kept. None when the turn failed (asked again by a later step, then back)."""
        import help_chat
        stand_in = getattr(self, 'result_check_model', None)

        def turn(text):
            if stand_in:
                return stand_in(self.config, text)
            if not openclaw_model(self.config):
                raise help_chat.Unavailable
            swap = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, text, '/'.join(swap) if swap else None, timeout=SECONDS)
        answer = None
        try:
            answer = model_reply.ask(turn, result_check_prompt(job), model_reply.read)
        except help_chat.Unavailable:
            pass  # no model: no answer, it comes back for a look
        except Exception as error:  # noqa: BLE001 - a turn that fails is no verdict: never a close
            LOG.warning('result check turn error=%s', type(error).__name__)
            return None  # asked again after the lease, then given up (result_checks.given_up): it comes back for a look
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            kept = result_checks.settle(db, job, answer, now())
        LOG.info('result check kept=%s', kept)
        return kept

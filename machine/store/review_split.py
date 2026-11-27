"""A review batch that fails every run, split up until the signal behind it is found (Store.begin_analysis,
App.review_step). A failed run's claim goes back as it was, and the next run resumes exactly that batch: one message
that makes every run fail (too large for the model, or one it keeps calling a tool wrongly on) held every later
signal back for good, while the dashboard said it retries.

A run that failed on the batch itself (batch_failure: a generic runtime error, an idle model, a timeout; never the
sign-in, billing, a provider outage or the Gateway's limits, which fail every batch alike), while the AI answered
its last real check (model_check.answering; a failure is checked again at once, model_check.ask_recheck), counts on
its claim (analyses.failures). From SPLIT_AFTER such failures on, each resume takes only the first half of what is left; the
rest goes back to waiting and is claimed again as usual. A claim down to one signal that failed alone is set aside
(SET_ASIDE_AFTER, as a message the review put off twice: listed under Set aside, one more look later; if it fails
then too, closed: review_last_look.CLOSED_AFTER) only once the AI answered its real check after that failure
(model_check.answered_since): with the sign-in gone or the AI down, nothing is ever set aside; the claim just waits.

Bounded: a batch of RUN_SIGNAL_BUDGET signals is down to one after about log2(budget) more failed runs; a set-aside
signal leaves every claim; a new version of the message starts over, as before."""
import json
import math

from machine.store.events import SET_ASIDE_AFTER
from machine.store.review_last_look import CLOSED_AFTER
from preparation_state import ACCOUNT_REASONS

SPLIT_AFTER = 2  # failed runs on one batch before it is split: a single failure is often the AI's moment, not the batch
BATCH_ERRORS = ('runtime_error', 'model_idle_timeout', 'runtime_timeout')


def batch_failure(error, reason=None):
    """Whether a failed review run may have failed on its batch: its error code and reason (preparation-run.mjs)."""
    return error in BATCH_ERRORS and reason not in ACCOUNT_REASONS


def ran_alone(claim):
    """The claim's last run had one signal to review."""
    items = [i for i in json.loads(claim['items'] or '[]') if not i.get('excluded')]
    return len(items) == 1


def splitting(claim):
    """This claim failed on its batch often enough to be split on its next resume."""
    return bool(claim) and (claim['failures'] or 0) >= SPLIT_AFTER


def resume(db, claim, rows):
    """What a resumed claim reviews now: (rows, None) with `rows` its signals still waiting in their order, or their
    first half once it is splitting; or ([], row) when its one signal is to be set aside (aside) and the claim closed,
    which the Store does (begin_analysis). Reads only."""
    import model_check
    if not splitting(claim) or not rows:
        return rows, None
    if len(rows) > 1:
        return rows[:math.ceil(len(rows) / 2)], None
    if not ran_alone(claim) or not model_check.answered_since(db, claim['error_at']):
        return rows, None
    return [], rows[0]


def aside(deferrals):
    """The deferrals a signal set aside here gets: set aside, or closed when it was set aside before (its last look)."""
    return CLOSED_AFTER if (deferrals or 0) >= SET_ASIDE_AFTER else SET_ASIDE_AFTER


def retry_soon(db):
    """A claim is being split while the AI answers its check: the next run goes after the first retry gap, not after a
    gap that doubled with every failure (each split is one smaller run, at most about log2 of the batch)."""
    import model_check
    claim = db.execute("SELECT * FROM analyses WHERE status='retryable' ORDER BY started_at LIMIT 1").fetchone()
    return splitting(claim) and model_check.answered_since(db, claim['error_at'])

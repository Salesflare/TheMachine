"""The first look in the service (refactor PR 26c): the quick first review on a new install, the dig after it and its
ending on the dashboard, with their timing constants. Moved out of assistant.App as is. A mixin of assistant.App
(APP_MIXINS)."""
import collections
import datetime as dt
import json
import threading
import time

import activity
import chat_model
import graph
from machine.config import LOG
from machine.delivery.push import mailing_sources
from machine.sources.suggest import suggestions
from machine.store.events import RUN_SIGNAL_BUDGET, SET_ASIDE_AFTER
from machine.store.first_look import FIRST_ACTIONS, TIP_SOURCES, note_model_check
from machine.store.review import FIRST_LOOK_READ, PREVIEW_DAYS
from machine.text import encoded
import model_check
from models import has_model, main_model, model_ready
from sources import CALENDAR_SERVICES, MAIL_SERVICES
from timeutil import now


# The first look (App.first_look): starts once no new signal came in for this long, tried at most this often, a failed
# try again at most this far apart (minutes, not half an hour: a new owner is waiting for their first to-do)
FIRST_LOOK_SETTLE_SECONDS, FIRST_LOOK_TRIES, FIRST_LOOK_RETRY_SECONDS = 180, 3, 300
FIRST_LOOK_LIMIT_SECONDS = 1800  # after a rate or usage limit: the limit holds that long anyway
FIRST_LOOK_MOVED = ('aborted', 'lost')  # a first look's run stopped from outside (a Gateway restart): not the model's failure
# Before it, a quick first look: as soon as the first page of mail is in, the QUICK_LOOK_SIGNALS of the week that most
# likely need the owner (Store.most_promising: newest first, whatever their age within the week), so the first cards
# come within minutes. A failed try is retried after this long, doubling per failure up to FIRST_LOOK_RETRY_SECONDS.
QUICK_LOOK_HOURS, QUICK_LOOK_SIGNALS, FIRST_LOOK_RETRY_MIN_SECONDS = PREVIEW_DAYS * 24, 20, 120
# The first review keeps digging, a batch of QUICK_LOOK_SIGNALS at a time (most promising first, each to-do shown as it is
# saved), until one of these: FIRST_DIG_CARDS to-dos; nothing of the week left to review; or it used FIRST_DIG_USAGE
# percent of the 5-hour window (a sign-in without usage windows, like an API key: FIRST_DIG_SIGNALS signals reviewed,
# about the same work).
FIRST_DIG_CARDS, FIRST_DIG_USAGE, FIRST_DIG_SIGNALS = 3, 60, 300
# The dashboard's bar while it digs (App.first_dig_live): one count over the whole week. The count is what its batches
# saved; between two saves only the bar moves, a signal's width at a time at the pace this install's first batches took
# (this many seconds per signal before one finished)
FIRST_DIG_PACE_SECONDS = 6
FIRST_DIG_HOURS = 24  # a first review that started longer ago than this digs no more (an install from before it dug)
# The first look's ending on the dashboard (App.first_look_done): shown this long after it stopped digging. What its
# reviewer sorted each signal into, by meaning (finish_analysis read), for a summary in counts only.
FIRST_LOOK_DONE_HOURS = 24


# While the first review digs (App.first_dig), each next review takes this many of the most promising signals of the
# week (twice the quick look: fewer turns, each with its fixed cost, and fewer pauses between them); the backlog after
# it goes in the regular reviews, spread out under the usage budget.
FIRST_LOOK_NEXT_SIGNALS = 2 * QUICK_LOOK_SIGNALS


# What is left of the week up to this many more goes in that same batch: a batch of a few signals still costs a whole
# turn and its start (2026-11-04: 106 signals went as 20, 40, 40 and 6; the 6 took 51 s)
FIRST_LOOK_TAIL_SIGNALS = FIRST_LOOK_NEXT_SIGNALS // 2


# The longest a new message waits for a review when fewer than min_signals (40) wait: 15 minutes since 2026-11-06,
# 60 before. Shorter batches cost a little more per message; the 10-minute gap between runs stays (gap_seconds).
REVIEW_MAX_WAIT_MINUTES = 15


def review_max_wait(settings):
    """review_worker max_wait_minutes, in minutes. 60 was the shipped default every install copied into its config.json
    (config.example.json), not an owner's choice, so it now means the new default too; any other value is kept."""
    value = (settings or {}).get('max_wait_minutes')
    return REVIEW_MAX_WAIT_MINUTES if value in (None, 60) else value


SYSTEM_SERVICES = {'gateway'}  # The Machine's own logs: not a source of the owner's


def first_look_batch(left):
    """How many signals the first look's next batch takes: FIRST_LOOK_NEXT_SIGNALS, or all that is left of the week
    when that is at most FIRST_LOOK_TAIL_SIGNALS more, so no batch of a few comes after it."""
    return max(FIRST_LOOK_NEXT_SIGNALS, left) if left <= FIRST_LOOK_NEXT_SIGNALS + FIRST_LOOK_TAIL_SIGNALS else FIRST_LOOK_NEXT_SIGNALS


def first_look_spent(runs):
    """Tried enough: FIRST_LOOK_TRIES tries; a run stopped from outside (a Gateway restart) is not a try, up to twice as many runs in all."""
    return sum(r['status'] not in ('aborted', 'lost') for r in runs) >= FIRST_LOOK_TRIES or len(runs) >= 2 * FIRST_LOOK_TRIES


def first_look_retry_at(runs, current):
    """When a first look that failed last may be tried again (None: now). A few minutes after the first failure, doubling
    per failure in a row up to FIRST_LOOK_RETRY_SECONDS; a rate limit waits FIRST_LOOK_LIMIT_SECONDS at once."""
    if not runs or runs[-1]['status'] == 'ok' or not runs[-1]['finished_at']:
        return None
    failed = 0
    for run in reversed(runs):
        if run['status'] == 'ok':
            break
        failed += 1
    wait = FIRST_LOOK_LIMIT_SECONDS if runs[-1].get('error') in ('rate_limited', 'usage_limited') else min(
        FIRST_LOOK_RETRY_MIN_SECONDS * 2 ** (failed - 1), FIRST_LOOK_RETRY_SECONDS)
    at = dt.datetime.fromisoformat(runs[-1]['finished_at']) + dt.timedelta(seconds=wait)
    return at.isoformat() if at > current else None


def signal_family(kind):
    """What a signal kind is to the owner, for a count in words: email, meeting (calendar events, meeting notes and
    transcripts), message (chats) or other (notifications, a CRM or payment update)."""
    kind = str(kind or '')
    if kind in ('gmail.message', 'outlook.message', 'ms_graph.message'):
        return 'email'
    if kind.endswith(('.event', '.meeting', '.transcript')) and kind not in ('stripe.event',):
        return 'meeting'
    if kind.endswith('.message'):
        return 'message'
    return 'other'


class FirstLookApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def mail_backfill(self, db):
        """The first import of a newly connected mailbox, for when the first review of its mail starts.
        'filling': mailboxes whose first import is still going (paging through the last days); one that failed
        is not waited for. 'fresh': mailboxes whose first import is in and that no review has
        finished since. Mailboxes imported before this was recorded count as reviewed."""
        filling, fresh = [], []
        last_ok = db.execute("SELECT max(started_at) FROM review_runs WHERE status='ok'").fetchone()[0] or ''
        for account in self.config.get('accounts', []):
            if account.get('service', 'gmail') not in MAIL_SERVICES:
                continue
            row = db.execute('SELECT state,error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
            try:
                state = json.loads(row['state'] or '{}') if row else {}
            except (TypeError, ValueError):
                state = {}
            if not row or row['error']:
                continue
            if state.get('mode') == 'bootstrap':
                filling.append(account['id'])
            elif state.get('backfilled_at') and state['backfilled_at'] > last_ok:
                fresh.append(account['id'])
        return {'filling': filling, 'fresh': fresh}

    def first_look(self, db, current=None):
        """The first look: on a new install with reviews still off, previews start by itself once a model and a source
        are connected. First a quick one: the QUICK_LOOK_SIGNALS of the week that most likely need the owner, as soon
        as the first page of mail is in, so the first cards come within minutes. Then it digs on, a batch at a time, until
        first_dig stops it; what one batch reviewed is not reviewed again, so no card comes twice. A failed try comes back
        within FIRST_LOOK_RETRY_SECONDS, however often it failed.
        Read-only like any preview: its cards show on the dashboard, nothing is sent, nothing is prepared while reviews
        are off (Store.prepare_first_look, after), nothing is done in any account; turning reviews on stays the owner's choice. None when it is not (or no longer) for this
        install, else its state: 'due' (with `quick` for the quick one), or 'waiting' with why (model, sources,
        settling, mail, retry; a retry with `failing`: Store.reviews_failing)."""
        settings = self.config.get('review_worker') or {}
        if settings.get('enabled') or settings.get('first_look') is False:
            return None
        runs = [dict(r) for r in db.execute('SELECT status,auto,finished_at,error,window_hours FROM review_runs ORDER BY started_at')]
        quick_runs = [r for r in runs if r['window_hours']]
        if any(not r['auto'] for r in runs):
            return None  # the owner ran their own preview
        if any(r['status'] in ('starting', 'running', 'recovering') for r in runs):
            return None
        current = current or dt.datetime.fromisoformat(now())
        dig = self.first_dig(db, current)
        if (dig and 'done' in dig) or (not dig and any(r['status'] == 'ok' for r in runs)):
            return None  # the first look found enough, looked through the week or used its share; or reviewed before
        digging = bool(dig)
        quick_done = any(r['status'] == 'ok' for r in quick_runs) or first_look_spent(quick_runs)
        sources = [a['id'] for a in self.config.get('accounts', []) if a.get('service') not in SYSTEM_SERVICES]
        since = (current - dt.timedelta(days=PREVIEW_DAYS)).isoformat()
        marks = ','.join('?' for _ in sources)
        waiting, newest = db.execute(f'SELECT count(*),max(ingested_at) FROM events WHERE analyzed_version<version AND deferrals<? AND occurred_at>=? '
                                     f'AND account_id IN ({marks})', (SET_ASIDE_AFTER, since, *sources)).fetchone() if sources else (0, None)
        out = {'waiting': min(waiting, RUN_SIGNAL_BUDGET), 'days': PREVIEW_DAYS}
        mail = self.mail_backfill(db)
        if not has_model(self.config):
            return {**out, 'state': 'waiting', 'why': 'model'}
        if not has_model(self.config, answered=db):
            # Signed in, but the AI hasn't answered its real check yet (model_check.py): still checking, or it failed,
            # with the provider's own error for Details
            found = model_check.last(db) or {}
            failed = found.get('model') == main_model() and found.get('ok') is False
            return {**out, 'state': 'waiting', 'why': 'model_check',
                    **({'error': found.get('error') or '', 'checked_at': found.get('at')} if failed else {})}
        if not quick_done and sources:
            recent = db.execute(f'SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<? AND occurred_at>=? AND account_id IN ({marks})',
                                (SET_ASIDE_AFTER, (current - dt.timedelta(hours=QUICK_LOOK_HOURS)).isoformat(), *sources)).fetchone()[0]
            # A mailbox still on its first page: its newest mail is what the quick look is for, wait for it
            first_page = mail['filling'] and not db.execute('SELECT 1 FROM events WHERE account_id IN (' + ','.join('?' for _ in mail['filling'])
                                                             + ') LIMIT 1', mail['filling']).fetchone()
            if recent and not first_page:
                quick = {**out, 'waiting': min(recent, QUICK_LOOK_SIGNALS), 'quick': True, 'hours': QUICK_LOOK_HOURS}
                retry = first_look_retry_at(runs, current)
                return {**quick, 'state': 'waiting', 'why': 'retry', 'retry_at': retry, 'failing': self.store.reviews_failing(db)} if retry else {**quick, 'state': 'due'}
            if first_page:
                return {**out, 'state': 'waiting', 'why': 'mail'}
        if mail['filling'] and (not waiting or newest > (current - dt.timedelta(minutes=review_max_wait(settings))).isoformat()) \
                and not (digging and waiting):
            return {**out, 'state': 'waiting', 'why': 'mail'}
        if not waiting:
            # After a quick look that left nothing of the week to review, the first look is done
            return None if any(r['status'] == 'ok' for r in quick_runs) else {**out, 'state': 'waiting', 'why': 'sources'}
        if (waiting < RUN_SIGNAL_BUDGET and not mail['fresh'] and not digging and
                newest > (current - dt.timedelta(seconds=FIRST_LOOK_SETTLE_SECONDS)).isoformat()):
            return {**out, 'state': 'waiting', 'why': 'settling'}
        retry = first_look_retry_at(runs, current)  # also after a failed quick look: a rate limit holds for both
        if retry:
            return {**out, 'state': 'waiting', 'why': 'retry', 'retry_at': retry, 'failing': self.store.reviews_failing(db)}
        return {**out, 'state': 'due'}

    def first_look_over(self, db):
        """The first look ended (first_dig_done), or this install reviewed before it had one."""
        return bool(db.execute("SELECT 1 FROM milestones WHERE name='first_dig_done'").fetchone() or (
            db.execute("SELECT 1 FROM review_runs WHERE status='ok' LIMIT 1").fetchone()
            and not db.execute("SELECT 1 FROM milestones WHERE name='first_dig'").fetchone()))

    def first_look_failing(self, db):
        """The first look's last pass failed (not one a restart cut off), so its next may go to another model."""
        row = db.execute("SELECT status FROM review_runs WHERE ((preview=1 AND auto=1) OR window_hours IS NOT NULL OR promising=1) "
                         "AND finished_at IS NOT NULL ORDER BY finished_at DESC LIMIT 1").fetchone()
        return bool(row) and row['status'] not in ('ok', *FIRST_LOOK_MOVED)

    def first_look_model(self, run_id, db):
        """The model a first look's run goes to: None (the main model), or another AI the owner signed in that answered
        its check (model_check.fallback), while the main model fails its check or failed the first look's last pass."""
        if not self.store.first_look_run(run_id, db):
            return None
        model = main_model()
        fallback = model_check.fallback(db, model)
        if not fallback or not chat_model.REF.fullmatch(fallback):
            return None
        return fallback if not model_check.passed(db, model) or self.first_look_failing(db) else None

    def model_check_kick(self):
        """From the review worker, never blocking it: the AI's real check (model_check.py) in a thread of its own when
        one is due (an AI connected, or a failed check comes round again), and while the first look is still ahead and
        the main model fails it or the first look's last pass failed, a look for another AI to fall back to. Nothing
        while no sign-in or key exists yet (has_model): there is nothing to check."""
        thread = getattr(self, '_model_check_thread', None)
        if thread and thread.is_alive():
            return None
        model = main_model()
        if not model or model_ready(self.config, wait=False) is False:
            return None
        current = dt.datetime.fromisoformat(now())
        with self.store.connect() as db:
            found = model_check.last(db)
            main = model_check.due(found, model, model_check.sign_in_stamp(self.config), current)
            other = not main and bool(found) and found.get('model') == model and not self.first_look_over(db) and (
                not found.get('ok') or self.first_look_failing(db)) and model_check.due_fallback(found, current)
        if not (main or other):
            return None
        self._model_check_thread = threading.Thread(target=self.model_check_run, args=(model, main), name='model-check', daemon=True)
        self._model_check_thread.start()
        return self._model_check_thread

    def model_check_run(self, model, main=True, run=None):
        """The check itself (model_check_kick's thread): the main model's when `main`, then, when it failed or the first
        look's last pass did, the other AIs the owner signed in, the first that answers kept as the fallback."""
        try:
            with self.store.connect() as db:
                found = model_check.last(db)
            if main:
                found = model_check.check(found, self.config, model, now(), run)
                with self.store.connect() as db:
                    note_model_check(db, found)
                LOG.info('model check ok=%s failed=%s', found['ok'], found['failed'])
            with self.store.connect() as db:
                look = not self.first_look_over(db) and (not found['ok'] or self.first_look_failing(db))
            if not look:
                return found
            catalog = getattr(self, 'chat_catalog', None)
            models = catalog.refresh(self.config) if catalog else chat_model.read_catalog(self.config)
            other = model_check.look_for_fallback(found, self.config, model, models, now(), dt.datetime.fromisoformat(now()), run)
            if other is not None:
                with self.store.connect() as db:
                    note_model_check(db, other)
                LOG.info('model check fallback=%s', bool(other.get('fallback')))
                found = other
            return found
        except Exception as error:  # noqa: BLE001 - checked again on a later round
            LOG.error('model check error=%s', type(error).__name__)
            return None

    def quick_first_review(self, db):
        """How many signals the first review after reviews turned on looks at, quickly: the week's most promising (the
        last QUICK_LOOK_HOURS, at most QUICK_LOOK_SIGNALS). 0 once any review or look finished well, or after
        FIRST_LOOK_TRIES tries (first_dig carries on from there), so an install that has reviewed before never gets one."""
        if db.execute("SELECT 1 FROM review_runs WHERE status='ok'").fetchone():
            return 0
        tries = [dict(r) for r in db.execute('SELECT status FROM review_runs WHERE preview=0 AND window_hours IS NOT NULL')]
        if tries and first_look_spent(tries):
            return 0
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(hours=QUICK_LOOK_HOURS)).isoformat()
        recent = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<? AND occurred_at>=?',
                            (SET_ASIDE_AFTER, since)).fetchone()[0]
        return min(recent, QUICK_LOOK_SIGNALS)

    def first_dig(self, db, current=None):
        """The first review digging on until it has something to show (FIRST_DIG_CARDS etc.). None when this install
        had no quick first review (it reviewed before); {'done': why} once it stopped, for good: 'cards' (FIRST_DIG_CARDS
        to-dos since it started), 'covered' (nothing of the last PREVIEW_DAYS left to review), 'usage' (first_dig_spent) or
        'expired' (it started more than FIRST_DIG_HOURS ago); else {'cards', 'left'}: it digs on, next with the most promising of the `left` signals of the week."""
        done = db.execute("SELECT detail FROM milestones WHERE name='first_dig_done'").fetchone()
        if done:
            return {'done': done[0]}
        start = db.execute('SELECT min(started_at) FROM review_runs WHERE window_hours IS NOT NULL').fetchone()[0]
        if not start:
            return None
        current = current or dt.datetime.fromisoformat(now())
        cards = db.execute('SELECT count(*) FROM suggestions WHERE created_at>=?', (start,)).fetchone()[0]
        sources = [a['id'] for a in self.config.get('accounts', []) if a.get('service') not in SYSTEM_SERVICES]
        left = db.execute(f"SELECT count(*) FROM events WHERE analyzed_version<version AND deferrals<? AND occurred_at>=? "
                          f"AND account_id IN ({','.join('?' for _ in sources)})",
                          (SET_ASIDE_AFTER, (current - dt.timedelta(days=PREVIEW_DAYS)).isoformat(), *sources)).fetchone()[0] if sources else 0
        why = 'cards' if cards >= FIRST_DIG_CARDS else 'usage' if self.first_dig_spent(db, start) else \
            'expired' if start < (current - dt.timedelta(hours=FIRST_DIG_HOURS)).isoformat() else None
        if not why and not left and not self.mail_backfill(db)['filling']:  # a mailbox still importing may bring more
            why = 'covered'
        if why:
            db.execute("INSERT OR IGNORE INTO milestones(name,at,detail) VALUES('first_dig_done',?,?)", (now(), why))
            LOG.info('first review done why=%s cards=%s', why, cards)
            return {'done': why}
        return {'cards': cards, 'left': left}

    def first_dig_live(self, db, current=None):
        """While the first look digs (first_dig, from its quick first review on, also between its batches): how far it got
        over the week, so the dashboard shows one bar that keeps moving until it has its to-dos or has read the week,
        instead of All clear between batches. {'read': signals its batches saved so far, 'total': read plus the week's
        signals left (at most FIRST_DIG_SIGNALS in all while more are left), 'todos', 'goal': FIRST_DIG_CARDS, 'days',
        'pace': seconds per signal of the batch that runs now, at the time its last finished batch took (FIRST_DIG_PACE_SECONDS before one finished), 'unit': 'email' when
        every source is a mailbox, else 'message', 'names': who it reads about (Store.first_look_names), 'first': the first
        to-do it found, {'id', 'title'}, or None}. None once it stopped, or on an install that had no first look. Counts,
        names and a to-do title only, never a message's text. 'failing': Store.reviews_failing."""
        dig = self.first_dig(db, current)
        if not dig or 'left' not in dig:
            return None
        # What a batch saved counts at once, also while its run is still ending: its signals have left `left` by then, so
        # counting them only after the run ended made the total dip by a batch for a moment (2026-11-04: 82, then 102)
        # A batch takes about as long whatever its size (its turn's steps, not its signals: 2026-11-04, 20 signals took
        # 135 s, 40 took 91 s), so the pace is the last batch's time spread over the batch that runs now
        read, last, size, runs = 0, None, None, []
        for run in db.execute("SELECT run_id,status,started_at,finished_at,planned FROM review_runs WHERE (preview=1 AND auto=1) OR window_hours IS NOT NULL OR promising=1 "
                              "ORDER BY started_at"):
            runs.append(run['run_id'])
            items = sum(len(json.loads(row[0] or '[]')) for row in db.execute(
                "SELECT items FROM analyses WHERE owner_run=? AND status='complete'", (run['run_id'],)))
            read += items
            if items and run['finished_at']:
                last = max(0.0, (dt.datetime.fromisoformat(run['finished_at']) - dt.datetime.fromisoformat(run['started_at'])).total_seconds())
            if run['status'] in ('starting', 'running', 'recovering'):
                size = run['planned']
        size = size or min(dig['left'], first_look_batch(dig['left']))
        pace = min(30, max(1, round(last / size))) if last and size else FIRST_DIG_PACE_SECONDS
        total = read + dig['left']
        if dig['left'] and total > FIRST_DIG_SIGNALS:
            total = max(FIRST_DIG_SIGNALS, read + min(dig['left'], FIRST_LOOK_NEXT_SIGNALS))
        # The live first look: who it reads about, the first to-do's title the moment it is saved, and whether all it
        # reads is mail ('email') or also other messages; from what its batches already wrote, no model call
        start = db.execute('SELECT min(started_at) FROM review_runs WHERE window_hours IS NOT NULL').fetchone()[0]
        first = db.execute('SELECT id,title FROM suggestions WHERE created_at>=? AND ' + activity.SHOWN + ' ORDER BY created_at LIMIT 1',
                           (start, now())).fetchone() if dig['cards'] else None
        services = {a.get('service') for a in self.config.get('accounts', []) if a.get('service') not in SYSTEM_SERVICES}
        return {'read': read, 'total': total, 'todos': dig['cards'], 'goal': FIRST_DIG_CARDS, 'days': PREVIEW_DAYS, 'pace': pace,
                'unit': 'email' if services and services <= set(MAIL_SERVICES) else 'message', 'names': self.store.first_look_names(db, runs, self.config.get('owner_name')),
                'first': {'id': first['id'], 'title': first['title']} if first else None, 'failing': self.store.reviews_failing(db)}

    def first_look_done(self, current=None):
        """The first look's ending, for the dashboard: what it read and what came of it, so an empty list says what the
        Machine did instead of only "Nothing to report". Shown for FIRST_LOOK_DONE_HOURS after it stopped digging
        (first_dig: found its to-dos, looked through the week, or used its share; not after one that expired). Counts
        and codes only, never a message's text: {'at', 'days', 'kinds': {email, meeting, message, other}, 'read': the
        groups its reviewer sorted them into (FIRST_LOOK_READ, finish_analysis read; empty when it gave none), 'todos',
        'acted' (the owner decided a to-do since), 'next': the setup steps that would help most ('calendar': no calendar
        connected; 'inbox': one mailbox only), 'connect': with no to-dos, sources that mail the owner often and aren't
        connected (first_look_connect)}. None before, after, or on an install that had no first look."""
        current = current or dt.datetime.fromisoformat(now())
        with self.store.connect() as db:
            done = db.execute("SELECT at,detail FROM milestones WHERE name='first_dig_done'").fetchone()
            if not done or done['detail'] == 'expired' or done['at'] < (current - dt.timedelta(hours=FIRST_LOOK_DONE_HOURS)).isoformat():
                return None
            runs = [r[0] for r in db.execute('SELECT run_id FROM review_runs WHERE ((preview=1 AND auto=1) OR window_hours IS NOT NULL OR promising=1) '
                                             'AND started_at<=?', (done['at'],))]
            if not runs:
                return None
            start = db.execute(f"SELECT min(started_at) FROM review_runs WHERE run_id IN ({','.join('?' * len(runs))})", runs).fetchone()[0]
            seen = {}
            for row in db.execute(f"SELECT items FROM analyses WHERE status='complete' AND owner_run IN ({','.join('?' * len(runs))})", runs):
                for item in json.loads(row['items'] or '[]'):
                    if not item.get('deferred'):
                        seen[int(item['id'])] = item.get('read') or seen.get(int(item['id']))
            kinds, read = collections.Counter(), collections.Counter(g for g in seen.values() if g in FIRST_LOOK_READ)
            ids = sorted(seen)
            for n in range(0, len(ids), 500):
                chunk = ids[n:n + 500]
                kinds.update(signal_family(r[0]) for r in db.execute(f"SELECT kind FROM events WHERE id IN ({','.join('?' * len(chunk))})", chunk))
            # Its to-dos up to when its last batch ended: a batch still running as it stopped digging saves its to-dos
            # after that, and its reads already count above (2026-11-09: "found 3 to-dos" over a list of 4)
            last = db.execute(f"SELECT max(CASE WHEN status IN ('starting','running','recovering') THEN ? ELSE coalesce(finished_at,?) END) "
                              f"FROM review_runs WHERE run_id IN ({','.join('?' * len(runs))})", (current.isoformat(), done['at'], *runs)).fetchone()[0]
            todos = db.execute('SELECT count(*) FROM suggestions WHERE created_at>=? AND created_at<=?', (start, max(done['at'], last or ''))).fetchone()[0]
            acted = bool(db.execute('SELECT 1 FROM decisions WHERE source IN (' + ','.join('?' * len(TIP_SOURCES)) + ') AND choice IN ('
                                    + ','.join('?' * len(FIRST_ACTIONS)) + ') AND created_at>=? LIMIT 1', (*TIP_SOURCES, *FIRST_ACTIONS, start)).fetchone())
        services = [a.get('service') for a in self.config.get('accounts', []) if a.get('service') not in SYSTEM_SERVICES]
        nxt = [step for step, missing in (('calendar', not any(s in CALENDAR_SERVICES for s in services)),
                                          ('inbox', sum(s in MAIL_SERVICES for s in services) == 1)) if missing]
        connect = self.first_look_connect(services) if not todos else []
        return {'at': done['at'], 'days': PREVIEW_DAYS, 'kinds': dict(kinds), 'read': dict(read), 'todos': todos, 'acted': acted, 'next': nxt,
                'connect': connect}

    def first_look_connect(self, services):
        """For an ending with no to-dos: the services that mail the owner often and aren't connected (mailing_sources), at
        most two as [{service, label}], so it offers "Connect Slack" rather than an empty ask. Worked out at most every 10
        minutes (the dashboard asks every few seconds); connecting one drops it at once."""
        key = tuple(sorted(str(s) for s in services))
        cached = getattr(self, '_first_look_connect', None)
        if cached and cached[1] == key and time.monotonic() - cached[0] < 600:
            return cached[2]
        with self.store.connect() as db:
            found = [{'service': s, 'label': label} for s, label in mailing_sources(db, self.config)][:2]
        self._first_look_connect = (time.monotonic(), key, found)
        return found

    def connect_suggested(self, sources, unfinished=()):
        """Connections, + Add: Suggested for you (machine/sources/suggest.py), [] when nothing has a signal. Worked out at
        most every 10 minutes for the same tiles; connecting one, or a setup failing, works it out again at once."""
        if getattr(self, 'store', None) is None:
            return []
        key = (tuple(sorted(str(s.get('name')) for s in sources if not s.get('connected'))), tuple(sorted(set(unfinished))))
        cached = getattr(self, '_connect_suggested', None)
        if cached and cached[1] == key and time.monotonic() - cached[0] < 600:
            return cached[2]
        try:
            with self.store.connect() as db:
                found = suggestions(db, sources, unfinished)
        except Exception as error:  # noqa: BLE001 - + Add shows its list without them
            LOG.warning('connect suggestions error=%s', type(error).__name__)
            return []
        self._connect_suggested = (time.monotonic(), key, found)
        return found

    def note_dig_start(self, db):
        """Where the 5-hour window stood when the first review started, so first_dig_spent counts only its own share."""
        db.execute("INSERT OR IGNORE INTO milestones(name,at,detail) VALUES('first_dig',?,?)", (now(), encoded(self.short_window() or {})))

    def first_dig_spent(self, db, start):
        """The first review used its share: FIRST_DIG_USAGE percent of the 5-hour window since it started (all of the
        window's use when it reset since), or FIRST_DIG_SIGNALS signals on a sign-in without usage windows."""
        window = self.short_window()
        if window:
            row = db.execute("SELECT detail FROM milestones WHERE name='first_dig'").fetchone()
            try:
                before = json.loads(row[0] or '{}') if row else {}
            except ValueError:
                before = {}
            same = before.get('used') is not None and (before.get('reset') == window['reset'] or (
                isinstance(before.get('reset'), (int, float)) and isinstance(window['reset'], (int, float)) and abs(before['reset'] - window['reset']) < 600))
            return window['used'] - (before['used'] if same else 0) >= FIRST_DIG_USAGE
        planned = db.execute('SELECT coalesce(sum(planned),0) FROM review_runs WHERE started_at>=?', (start,)).fetchone()[0]
        return planned >= FIRST_DIG_SIGNALS

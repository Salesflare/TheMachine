"""How much model use the background work may take (model_budget.py, pacing.py): usage limits, the fallback model,
the pauses of background turns, reviews and a board's look through the history, and that look's ranking
(backfill_scores, backfill_text). Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import logging
import math
import sqlite3
import threading
import time

import embeddings
import graph
import graph_board_reviews
from machine.model_usage import model_resets, model_status, model_usage, usage_status
import model_budget
import model_fallback
from models import claude_plan_route, openclaw_model
import pacing
from timeutil import now

LOG = logging.getLogger('personal-assistant')


class ModelPacingApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def note_usage_limit(self, receipt):
        """A run ended on the sign-in's usage limit: everything the service starts waits until it resets (the time the
        provider named, else the window's), instead of trying again every few minutes."""
        if not isinstance(receipt, dict) or receipt.get('error') != 'usage_limited':
            return None
        model = openclaw_model(self.config)
        until = model_budget.limit_until(receipt.get('retry_at'), model_budget.for_model(getattr(self, 'model_usage', None), model))
        known = getattr(self, 'usage_limit', None)
        if not known or known['until'] < until:
            LOG.warning('usage limit reached until=%s', dt.datetime.fromtimestamp(until, dt.timezone.utc).isoformat(timespec='minutes'))
        self.usage_limit = {'until': until, 'at': int(time.time()), 'provider': model_budget.provider_of(model)}
        self.fallback_health().doubt()  # the fallback didn't carry this run: the usage rules hold until a check passes
        getattr(self, 'model_usage_wake', threading.Event()).set()
        return until

    def fallback_health(self):
        health = getattr(self, '_fallback_health', None)
        if health is None:
            health = self._fallback_health = model_fallback.Health()
        return health

    def fallback_models(self):
        """OpenClaw's fallbacks billed apart from the main model (model_fallback.separate)."""
        primary, fallbacks = model_fallback.configured(self.config)
        return model_fallback.separate(primary or openclaw_model(self.config), fallbacks)

    def fallback_covers(self):
        """The fallback that carries work past the main model's usage limits, when one is known to work
        (model_fallback.py); None: the usage rules apply."""
        try:
            return self.fallback_health().working(self.fallback_models())
        except Exception as error:  # noqa: BLE001 - the usage rules apply
            LOG.error('fallback check error=%s', type(error).__name__)
            return None

    def paced_usage(self):
        """The main model's usage windows the usage rules go by (model_budget.for_model); None (no rules) while a
        working fallback carries work past them."""
        if self.fallback_covers():
            return None
        return model_budget.for_model(getattr(self, 'model_usage', None), openclaw_model(self.config))

    def check_fallback(self):
        """From the usage worker: checks the fallback (model_fallback.Health.refresh) only while the main model's
        limits would hold work back (the earliest rule: follow-ups) or a usage limit holds it."""
        models = self.fallback_models()
        if not models:
            return None
        now_s = time.time()
        usage = model_budget.for_model(getattr(self, 'model_usage', None), openclaw_model(self.config))
        limit = getattr(self, 'usage_limit', None)
        if not (model_budget.follow_up_pause(usage, now_s) or (limit and limit['until'] > now_s)):
            return None
        found = self.fallback_health().refresh(self.config, models, now_s)
        LOG.info('fallback check working=%s', bool(found))
        return found

    def background_pause(self, first=False, owner=False, job=None, db=None, signals=False):
        """None when a turn the service starts may go now; else why it waits ({'window', 'until', 'limited'...}). A
        usage limit holds everything; the budget (model_budget.pause) holds background work only, `first` for the
        first look and its first draft, `signals` for a review of new signals (the week holds it only at WEEK_CAP). A sign-in that reports no usage windows (an API key) is never paused here,
        nor one with a working fallback billed apart (fallback_covers): OpenClaw moves to it once the limit is reached.
        Each budget check is counted (pacing.py): how often background work paces, how long, how many jobs (`job`,
        an id that stays here) waited."""
        model = openclaw_model(self.config)
        covered = self.fallback_covers()  # a working fallback billed apart carries work past the limits: no rules
        now_s, usage = time.time(), None if covered else model_budget.for_model(getattr(self, 'model_usage', None), model)
        limit = None if covered else getattr(self, 'usage_limit', None)
        if limit and limit['until'] > now_s and limit.get('provider') in (None, model_budget.provider_of(model)):
            return {'window': 'limit', 'until': limit['until'], 'limited': True}
        full = [{'window': '5h' if model_budget.window_kind(w['label']) == 'short' else 'week', 'until': w.get('reset'), 'limited': True}
                for p in usage or [] for w in p.get('windows') or [] if w.get('used', 0) >= 100 and (w.get('reset') or now_s + 1) > now_s]
        if full:
            return max(full, key=lambda f: f['until'] or 0)
        if owner:
            return None
        found = model_budget.pause(usage, now_s, first=first, signals=signals)
        tracker = getattr(self, 'pacing', None)
        if tracker is None and getattr(self, 'store', None) is not None:
            tracker = self.pacing = pacing.Tracker(self.store.connect)
        # A review of new signals that goes while the day's share holds heavier work doesn't end that work's stretch
        if tracker and not (signals and not found and model_budget.pause(usage, now_s, first=first)):
            tracker.note(found, job, first=first, now_s=now_s, db=db)  # db: a caller's write transaction (preparation_step)
        return {**found, 'limited': False} if found else None

    def background_started(self):
        self.background_at = time.time()

    def model_pause(self):
        """What the dashboard's limit banner shows: a usage limit reached (which one, when it resets), else None. The
        budget's own pauses are not shown: nothing is wrong then."""
        found = self.background_pause(owner=True)
        if found:
            return {'window': found['window'], 'until': found.get('until'), 'name': self.model_name()}
        if not self.fallback_covers():
            return None
        status = getattr(self, 'model_status', None) or {}
        limit = getattr(self, 'usage_limit', None)
        if status.get('limit_reached') or (limit and limit['until'] > time.time()):  # the fallback answers meanwhile
            return {'window': 'limit', 'until': status.get('limit_resets_at') or (limit or {}).get('until'),
                    'name': self.model_name(), 'fallback': True}
        return None

    def model_name(self):
        """The sign-in's name for the owner: Claude, ChatGPT, or None when it is neither."""
        model = openclaw_model(self.config) or ''
        return 'Claude' if model.startswith(('claude-cli/', 'anthropic/')) or claude_plan_route(self.config) else 'ChatGPT' if model.startswith(('openai', 'codex')) else None

    def review_pause(self):
        """What the dashboard says while reviews of new signals wait for the budget (review_step), with its Review now:
        which window, until when, the sign-in's name. None when they don't wait, or a usage limit holds them (model_pause
        says that)."""
        found = getattr(self, 'review_paused', None)
        if not found or found.get('limited') or not (self.config.get('review_worker') or {}).get('enabled') or self.fallback_covers():
            return None
        if found.get('until') and found['until'] <= time.time():
            return None
        return {'window': found['window'], 'until': found.get('until'), 'name': self.model_name()}

    def history_paced(self):
        """A board's look through the history keeps the daily share of the week (model_budget.pause without `signals`),
        also when it rides along with a review of new signals. Not counted in pacing.py: the review's own check is."""
        return bool(model_budget.pause(self.paced_usage()))

    def model_room(self, most=80):
        """The model's limits have room for extra work (a board's look through the history): no window the sign-in reports
        is past `most` percent used. Unknown usage counts as room."""
        return all(w['used'] < most for p in self.paced_usage() or [] for w in p.get('windows') or [])

    def backfill_scores(self, board, text):
        """How likely each counterpart belongs on the board by meaning, from local embeddings: its messages against the
        board's description and the messages of projects on it. None without embeddings."""
        settings = embeddings.settings(self.config)
        if not settings:
            return None
        model, dims = settings.get('model', ''), int(settings.get('dims', 256))
        asked = embeddings.embed(settings, [embeddings.QUERY_PREFIX + text[:embeddings.BODY_CHARS]], 30)[0]
        with self.store.connect() as db:
            found = graph_board_reviews.backfill_counterparts(db)
            vector = lambda ids: [embeddings.unpack(r[0]) for r in db.execute(
                f"SELECT v.vector FROM event_vectors v JOIN events e ON e.id=v.event_id WHERE e.deleted=0 AND v.version=e.version AND v.model=? AND v.dims=? "
                f"AND e.id IN ({','.join('?' * len(ids))})", (model, dims, *ids))] if ids else []
            probes = vector([r[0] for r in db.execute('SELECT ep.event_id FROM event_projects ep JOIN projects p ON p.id=ep.project_id WHERE p.board_id=? '
                                                      'ORDER BY ep.event_id DESC LIMIT 300', (board['id'],))])
            centre = [sum(x) / len(probes) for x in zip(*probes)] if probes else None
            if centre:
                norm = math.sqrt(sum(x * x for x in centre)) or 1
                centre = [x / norm for x in centre]
            floor, query_floor = float(settings.get('floor', embeddings.FLOOR)), float(settings.get('query_floor', embeddings.QUERY_FLOOR))
            scores = {}
            for key, c in found.items():
                best = None
                for v in vector(c['event_ids'][:8]):
                    score = max(embeddings.cosine(asked, v) - query_floor, (embeddings.cosine(centre, v) - floor) if centre else -9)
                    best = score if best is None else max(best, score)
                if best is not None:
                    scores[key] = best
        return scores

    def backfill_text(self, run_id):
        """The next round of a new board's look through the history for this review (graph_board_reviews.backfill_brief), ranked by
        meaning first when there are local embeddings. Empty while the model's limits are nearly used."""
        try:
            if not self.model_room() or self.history_paced():
                return ''
            with self.store.connect() as db:
                pending = graph_board_reviews.backfill_pending(db)
            for board, text in pending:
                try:
                    scores = self.backfill_scores(board, text)
                except (embeddings.EmbeddingError, OSError, ValueError) as error:
                    LOG.info('backfill ranking without embeddings error=%s', type(error).__name__)
                    scores = None
                with self.store.connect() as db:
                    graph_board_reviews.rank_backfill(db, board['id'], scores)
            with self.store.connect() as db:
                return graph_board_reviews.backfill_brief(db, run_id, now(), self.graph_event_lines)
        except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
            LOG.error('backfill brief error=%s', type(error).__name__)
            return ''

    def model_usage_worker(self):
        """Reads the AI sign-in's usage limits every five minutes, and a minute after a run ends (OpenClaw makes the
        model calls, so its usage reading is the one to ask; that reading never costs model usage). A failed read
        keeps the last one. The resets come from the Codex CLI's own sign-in when it is the same account."""
        self.model_usage_wake = getattr(self, 'model_usage_wake', None) or threading.Event()
        while not self.stop.is_set():
            self.refresh_model_usage()
            try:  # a fallback billed apart: checked while the main model's limits would hold work back (model_fallback.py)
                self.check_fallback()
            except Exception as error:  # noqa: BLE001 - never stops the worker
                LOG.error('fallback check error=%s', type(error).__name__)
            try:  # the models a chat can pick (chat_model.py): read again every ten minutes
                self.chat_models()
            except Exception as error:  # noqa: BLE001 - never stops the worker
                LOG.error('model list error=%s', type(error).__name__)
            self.model_usage_wake.clear()
            if self.stop.wait(60):
                break
            for _ in range(240):  # the rest of five minutes, or sooner when a run ended
                if self.stop.is_set() or self.model_usage_wake.is_set():
                    break
                self.stop.wait(1)

    def refresh_model_usage(self):
        reply = usage_status(self.config)
        if reply is None:
            return
        self.model_usage = model_usage(self.config, reply=reply) or getattr(self, 'model_usage', None)
        self.model_usage_reply = reply
        try:
            resets = model_resets(self.config, reply) if self.config.get('codex') is not False else None
        except (OSError, ValueError):
            resets = None
        self.model_status = model_status(self.config, reply, self.model_usage, resets)

    def pacing_send(self):
        """Once a day, with error reports on: the finished days' pacing counts and minutes to the control plane."""
        try:
            return pacing.send(self.store.connect, self.fleet.relay.call)
        except Exception as error:  # the Network or the control plane is away: next time
            LOG.warning('pacing report error=%s', type(error).__name__)
            return 0

    def short_window(self):
        """The main model's 5-hour usage window as last read (model_usage): {'used', 'reset'}, or None (an API key, a
        sign-in that reports no windows, or nothing read yet)."""
        usage = self.paced_usage()  # None while a working fallback carries work: the first review counts signals then
        found = [w for p in usage or [] for w in p.get('windows') or []
                 if model_budget.window_kind(w.get('label')) == 'short' and isinstance(w.get('used'), (int, float))]
        if not found:
            return None
        window = max(found, key=lambda w: w['used'])
        return {'used': window['used'], 'reset': window.get('reset')}

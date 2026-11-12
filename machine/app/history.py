"""History backfill in the service: older WhatsApp, Slack and Teams messages, email and meetings brought in slowly in
the background, as history only (machine/store/history.py has the line between history and signal). A mixin of
assistant.App (APP_MIXINS); the source readers come from App.HISTORY_SOURCES (Gmail, Calendar and WhatsApp stay in
assistant.py; Slack reads through its collector's own client, Teams through connectors/teams.py history_page).

When it runs: only after the first look ended, never while a review, a first import or a sync read runs, with room on
the disk and in memory, at the lowest CPU and disk priority, one small step at a time (STEP_GAP_SECONDS apart), so
setup, Connected and the first to-dos never wait for it. Every Machine starts it by itself after an update; each step
saves where it got, so a restart goes on from there. No model reads what it brings in."""
import contextlib
import datetime as dt
import json
import logging
import os
from pathlib import Path
import platform
import random
import re
import shutil
import sqlite3
import threading
import time

import abilities
import check_now
import embeddings
import graph
from machine.store import graph_history
from machine.store import history
from machine.store.facts import FACT_VECTOR_BATCH
from sources import SourceError, rate_limited, upstream_busy
from timeutil import local_tz, now

LOG = logging.getLogger('personal-assistant')

STEP_GAP_SECONDS = 20  # between two steps; a step is one small page from one source
WAIT_SECONDS = 300  # after a step found a reason to wait
SHORT_WAITS = {'review', 'first_import', 'sync'}  # over soon: tried again after STEP_GAP_SECONDS, so steps slot in between them
MAIL_PAGE = 20  # messages per mail step: one list call and at most this many reads, far inside Gmail's and Graph's limits
CALENDAR_PAGE = 100
WHATSAPP_DAYS = 7  # one local read of the WhatsApp store per step covers this many days
WHATSAPP_LIMIT = 1000  # wacli's most rows per read: a fuller window is split
# Room on the data disk (free_disk): never under FREE_DISK_BYTES; a tenth of the disk on a small one, but never more
# than FREE_DISK_ENOUGH (a tenth of a big disk is far more than history ever writes); and DATABASE_HEADROOM times the
# database, so the database can still double while SQLite rewrites it (a VACUUM or a table rebuild needs a full copy).
FREE_DISK_BYTES = 2 * 1024 ** 3
FREE_DISK_SHARE = 0.10
FREE_DISK_ENOUGH = 5 * 1024 ** 3
DATABASE_HEADROOM = 2
FREE_MEMORY_BYTES = 500 * 1024 ** 2  # pauses with less memory available (a hosted Machine has 3.8 GB)
ERROR_WAIT_DAYS = 1 / 24  # a connection whose step failed waits an hour, the others go on
FIRST_LOOK_GRACE = dt.timedelta(days=1)  # a Machine from before the first look: history waits this long after its first read
RATE_LIMIT_REST = 1800  # seconds all history work rests after a 429 or quota answer to it
LIVE_LIMIT_WINDOW = dt.timedelta(minutes=30)  # a live sync's 429 this recent holds history back too
EMBED_BATCH = 8  # history events per embedding request: small, so a live one never waits long behind it
EMBED_GAP_SECONDS = 30  # between two history embedding batches
# Passages of long meetings and conversations (embeddings.passage_pass, a few per pass): the next pass waits at least
# PASSAGE_GAP_SECONDS and PASSAGE_REST times as long as this one took, so the local model works a tenth of the time
# at most, on a small or busy server too (a passage took 0.3 s on an idle desktop, 1 to 2 s on a loaded one,
# November 2026). A pass that only looked (nothing long) is followed sooner.
PASSAGE_GAP_SECONDS, PASSAGE_REST, PASSAGE_LOOK_GAP_SECONDS = 20, 10, 5
# Slack's slow lane (history_slack). Slack allows a non-Marketplace app about one history or replies read a minute per
# workspace, and the collector spends one every few minutes (machine/sources/slack.py). History shares the collector's
# client and reads only while the collector rests with room for its own next read after it: at most one page (Slack's
# own page size for the connection, slack_limits) every SLACK_GAP_SECONDS, never in a minute the collector wants.
SLACK_GAP_SECONDS = 180
SLACK_WAIT_MAX = 60  # seconds a step may wait for the connection's minute of the round; longer: another step tries
SLACK_THREADS_KEEP = 5000  # threads with replies queued for the walk's second pass
MAIL, CALENDAR, WHATSAPP = ('gmail', 'outlook', 'imap'), ('calendar', 'outlook_calendar'), ('whatsapp',)
CONNECTOR_HISTORY = ('teams', 'linkedin', 'x')  # a connector with its own history_page (connectors/teams.py, ...)
PACED_STOP_DAYS = 1  # a paced connector (HISTORY_PACE) stops its history this long after any failed or odd read


def connector_pace(account):
    """A connector's HISTORY_PACE (LinkedIn and X: read through the owner's own browser, where bulk reads could get the
    account restricted), else None: {'steps_per_day', 'pause_minutes': (least, most), 'hours': (start, end)}."""
    if account.get('service') not in CONNECTOR_HISTORY:
        return None
    from machine.sources.connectors import load_connector
    pace = getattr(load_connector(account.get('service')), 'HISTORY_PACE', None)
    return pace if isinstance(pace, dict) else None


def pace_wait(pace, account, state, current, default_hours=None):
    """Why a paced connector's history step waits now (a short code), or None: stopped for a day after a failed or odd
    read, its jittered pause since the last step not over, outside waking hours, or its steps for today used up.
    `current` is an aware datetime; waking hours are local (the account's active_hours narrowed to the pace's)."""
    stamp = current.isoformat()
    if state.get('stopped_until', '') > stamp:
        return 'stopped'
    if state.get('next_at', '') > stamp:
        return 'pause'
    local = current.astimezone(local_tz())
    start, end = pace['hours']
    own = account.get('active_hours') or default_hours
    if own:
        start, end = max(start, own[0]), min(end, own[1])
    if not start <= local.hour < end:
        return 'hours'
    if state.get('day') == local.date().isoformat() and int(state.get('steps') or 0) >= pace['steps_per_day']:
        return 'cap'
    return None


def pace_after(pace, state, current, failed=None):
    """After a paced step at `current`: count it for today and pause a random few minutes (pace_minutes), so the reads
    never come at a fixed beat. A failed read (`failed`, its error code) stops for PACED_STOP_DAYS, unless only the
    browser was busy with another job (local, not the site): then just the pause."""
    day = current.astimezone(local_tz()).date().isoformat()
    if state.get('day') != day:
        state.update(day=day, steps=0)
    state['steps'] = int(state.get('steps') or 0) + 1
    least, most = pace['pause_minutes']
    state['next_at'] = (current + dt.timedelta(minutes=random.uniform(least, most))).isoformat()
    if failed and not str(failed).endswith('_browser_busy'):
        state['stopped_until'] = (current + dt.timedelta(days=PACED_STOP_DAYS)).isoformat()


def kind(account):
    service = account.get('service', 'gmail')
    return ('mail' if service in MAIL else 'calendar' if service in CALENDAR else 'whatsapp' if service in WHATSAPP
            else 'slack' if service == 'slack' else 'connector' if service in CONNECTOR_HISTORY else None)


def free_disk(database):
    """Room on the disk that holds the database file (see FREE_DISK_BYTES). Can't tell: no reason to wait."""
    database = Path(database)
    try:
        usage = shutil.disk_usage(database.parent)
    except OSError:
        return True
    size = 0
    for part in (database, database.with_name(database.name + '-wal')):
        with contextlib.suppress(OSError):
            size += part.stat().st_size
    return usage.free >= max(FREE_DISK_BYTES, min(usage.total * FREE_DISK_SHARE, FREE_DISK_ENOUGH), DATABASE_HEADROOM * size)


def free_memory(path='/proc/meminfo'):
    try:
        with open(path) as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    return int(line.split()[1]) * 1024 >= FREE_MEMORY_BYTES
    except (OSError, ValueError, IndexError):
        pass
    return True  # not Linux, or no figure: no reason to wait


IOPRIO_SYSCALL = {'x86_64': 251, 'aarch64': 30, 'arm64': 30}


def lowest_priority():
    """This thread at nice 19 and idle disk priority (Linux: both are per thread, and wacli started from it inherits
    them). Best effort: elsewhere, or refused, it runs as it is."""
    with contextlib.suppress(Exception):
        os.setpriority(os.PRIO_PROCESS, threading.get_native_id(), 19)
    number = IOPRIO_SYSCALL.get(platform.machine())
    if number and platform.system() == 'Linux':
        with contextlib.suppress(Exception):  # ioprio_set(IOPRIO_WHO_PROCESS, this thread, IOPRIO_CLASS_IDLE)
            import ctypes  # here: a Python whose ctypes doesn't load still runs everything else
            ctypes.CDLL(None, use_errno=True).syscall(number, 1, threading.get_native_id(), 3 << 13)


class HistoryApp:
    ACTIONS = {}

    def history_worker(self):
        lowest_priority()
        wait = STEP_GAP_SECONDS
        while not self.stop.wait(wait):
            try:
                wait = STEP_GAP_SECONDS if self.history_step() or self.history_why in SHORT_WAITS else WAIT_SECONDS
            except sqlite3.OperationalError as error:
                LOG.info('history waits error=%s', type(error).__name__); wait = WAIT_SECONDS
            except Exception as error:  # noqa: BLE001 - tried again later, never stops the service
                LOG.error('history error=%s', type(error).__name__); wait = WAIT_SECONDS

    def history_accounts(self):
        # Own connections only: a shared one is read by its owner's Machine, and WhatsApp needs its local store
        return [a for a in self.config.get('accounts') or [] if kind(a) and abilities.signals_on(a) and not a.get('shared')
                and (kind(a) != 'whatsapp' or a.get('store'))]

    history_why = None  # why the last step waited (a code from history_wait, or 'sync'), None when it went
    history_rested = 0.0  # time.monotonic() until which history rests after a source or the embedding server said slow down

    def history_wait(self, current=None):
        """Why history waits now (a short code), or None when a step may go: it is off, the first look hasn't ended,
        a review or a first import runs, a source asked to slow down, or the disk or memory is short. A connection's
        own sync read, or its own first import not being in yet, only holds back that connection (history_step), so on
        a Machine with many sources there's always a gap to step in."""
        if not any(history.depth(self.config, a) for a in self.history_accounts()):
            return 'off'
        return self.history_hold(current)

    def history_rest(self, error):
        """A 429 or quota answer to a history read: all history work (backfill, Graph passes, embeddings) rests for
        RATE_LIMIT_REST (or longer when the source says so), so the budget stays for live sync. True when it was one."""
        if not (rate_limited(error) or upstream_busy(error)):
            return False
        self.history_rested = time.monotonic() + max(RATE_LIMIT_REST, int(getattr(error, 'retry_after', None) or 0))
        return True

    def history_hold(self, current=None):
        """What holds back every kind of history work (the backfill, a Graph pass over history, history embeddings),
        or None: the first look hasn't ended, a review or a first import runs, a source asked to slow down (a history
        read's own 429, or a live sync's), or the disk or memory is short."""
        if time.monotonic() < self.history_rested:
            return 'rate_limit'
        current = current or dt.datetime.fromisoformat(now())
        with self.store.connect() as db:
            if not db.execute("SELECT 1 FROM milestones WHERE name='first_dig_done'").fetchone():
                first = db.execute("SELECT min(at) FROM sync_activity WHERE status='success'").fetchone()[0]
                if (not first or db.execute('SELECT 1 FROM review_runs WHERE preview=1 AND auto=1 AND status IN '
                                            "('starting','running','recovering') LIMIT 1").fetchone()
                        or dt.datetime.fromisoformat(first) > current - FIRST_LOOK_GRACE):
                    return 'first_look'
            if check_now.reviewing(db):
                return 'review'
            for (state,) in db.execute('SELECT state FROM checkpoints'):
                with contextlib.suppress(ValueError, TypeError, AttributeError):
                    state = json.loads(state)
                    if state.get('mode') in ('bootstrap', 'resync') or state.get('page_token'):
                        return 'first_import'
            # a live sync the service asked to slow down: history spends none of what it has left
            for error, at in db.execute('SELECT error,error_at FROM checkpoints WHERE error IS NOT NULL AND error_at>?',
                                        ((current - LIVE_LIMIT_WINDOW).isoformat(),)):
                if 'HTTP_429' in str(error) or re.search(r'rate_?limit|quota', str(error), re.I):
                    return 'rate_limit'
        if not free_disk(self.store.path):
            return 'disk'
        if not free_memory():
            return 'memory'
        return None

    def history_step(self, current=None):
        """One small step for the first connection whose history isn't in yet. True when it did one (the next follows
        soon), False when there is nothing to do or a reason to wait."""
        why = self.history_wait(current)
        if why:
            return self.history_waits(why)
        stamp = now()
        resting, reading = self.__dict__.get('collector_resting'), False
        for account in self.history_accounts():
            days = history.depth(self.config, account)
            if not days:
                continue  # its kind of history is off (history_days, or social_history_days for LinkedIn and X)
            with self.store.connect() as db:
                found = history.get(db, account['id'])
                imported = history.first_import_done(db, account['id'])
                live = db.execute('SELECT error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
            # Teams from before channel history (only Teams: LinkedIn's and X's walks have no channels)
            reopen = bool(found and found['done_at'] and account.get('service') == 'teams' and 'channels' not in found['state'])
            if found and found['done_at'] and (found['depth_days'] or 0) >= days and not reopen:
                continue
            if not imported:
                reading = reading or 'first_import'
                continue  # its own first week isn't in yet (a connection added later too): never before that
            state = dict(found['state']) if found else {}
            if state.get('error_at', '') > history.before(stamp, ERROR_WAIT_DAYS):
                continue  # failed a while ago: the others first
            if resting is not None and account['id'] not in resting:
                reading = 'sync'
                continue  # its own sync reads it now: another one, or this one once that read is done
            pace = connector_pace(account)
            if pace:  # LinkedIn and X: never while its own sync fails, and only at its own slow, waking-hours pace
                if live and live[0]:
                    reading = reading or 'live_error'
                    continue
                from machine.sources.connectors import load_connector
                held = pace_wait(pace, account, state, dt.datetime.fromisoformat(stamp),
                                 getattr(load_connector(account.get('service')), 'READ_HOURS', None))
                if held:
                    reading = reading or 'pace'
                    continue
            if reopen:  # Teams from before channel history: its chats are in, its channels' walk follows
                state['chats'] = []
            elif found and found['done_at']:  # a deeper setting since: walk on from where it stopped
                state.update(upper=state.get('target'), target=None, cursor=None, token=None)
                for key in ('chats', 'channels', 'threads', 'link', 'page'):
                    state.pop(key, None)  # a connector's, Slack's, LinkedIn's or X's walk lists its conversations again
            state['upper'] = state.get('upper') or self.history_upper(account, stamp)
            state['target'] = state.get('target') or history.before(stamp, days)  # fixed for the walk: a page token holds its query
            state.pop('error_at', None)
            try:
                stepped = getattr(self, 'history_' + kind(account))(account, state)
                if stepped is None:  # not its turn yet (Slack's slow lane): the others go
                    reading = reading or 'sync'
                    continue
                kept, oldest, done = stepped
            except SourceError as error:  # tried again later; the connection's own sync reports its errors
                LOG.info('history account=%s waits error=%s', account['id'], error)
                if pace:  # any failed or odd answer: a day off for this one, the others go on
                    pace_after(pace, state, dt.datetime.fromisoformat(stamp), failed=error.category)
                with self.store.connect() as db:
                    history.save(db, account['id'], {**state, 'error_at': stamp}, stamp)
                if pace:
                    return self.history_waits('error')
                return self.history_waits('rate_limit' if self.history_rest(error) else 'error')
            if pace:
                pace_after(pace, state, dt.datetime.fromisoformat(stamp))
            with self.store.connect() as db:
                history.save(db, account['id'], state, now(), kept, oldest, done, days)
            self.history_waits(None)
            if kept or done:
                LOG.info('history account=%s kept=%d done=%s', account['id'], kept, done)
            return True
        return self.history_waits(reading or 'done')

    def history_waits(self, why):
        """Note why it waits (None: it goes), logged once per change rather than every step. Always False."""
        if why != self.history_why:
            LOG.info('history %s', f'waits reason={why}' if why else 'goes')
            self.history_why = why
        return False

    def history_graph_step(self):
        """After a graph build (graph_worker): the Graph takes in one more slice of history (graph_history.advance),
        only while nothing holds history back. True when it did, so the next build counts it soon."""
        if self.history_hold():
            return False
        stamp = now()
        horizon = (dt.datetime.fromisoformat(stamp) - dt.timedelta(days=graph.HORIZON_DAYS)).isoformat()
        with self.store.connect() as db:
            graph_history.ensure(db)
            return graph_history.advance(db, horizon, stamp)

    def embed_pass(self, settings):
        """One pass of embedding_worker: vectors for facts just learned, edited or brought back (Store.embed_new_facts,
        a few), for new and changed signals, newest first, then history's at a slower pace once none waits. Seconds
        until the next pass."""
        facts = self.store.embed_new_facts(settings)
        done = embeddings.embed_pending(self.store.connect, settings, 16)
        if done == 16 or facts == FACT_VECTOR_BATCH:
            return 5
        return 60 if done else min(60, self.passage_step(settings), self.history_embed_step(settings))

    def passage_step(self, settings):
        """A few more passages for long signals (embedding_worker calls it only when no signal waits for its first
        vector), held back by all that holds history back: never during the first look, a review or a first import.
        Seconds until the next one."""
        if not settings or self.history_hold():
            return WAIT_SECONDS
        started = time.monotonic()
        done, more = embeddings.passage_pass(self.store.connect, settings)
        if not more:
            return WAIT_SECONDS
        return max(PASSAGE_GAP_SECONDS, PASSAGE_REST * (time.monotonic() - started)) if done else PASSAGE_LOOK_GAP_SECONDS

    def history_embed_step(self, settings):
        """One small batch of history vectors for Search by meaning (embedding_worker calls it only when no signal waits
        for one), newest first. Seconds until the next one: longer while held back, after a 429 or when all are in."""
        if not settings or self.history_hold():
            return WAIT_SECONDS
        try:
            done = embeddings.embed_pending(self.store.connect, settings, EMBED_BATCH, history=True)
        except embeddings.EmbeddingError as error:
            status = str(error)[5:] if str(error).startswith('http_') else ''
            if status.isdigit() and self.history_rest(SourceError('embeddings', int(status))):
                LOG.info('history embeddings rest error=%s', error)
            return WAIT_SECONDS
        return EMBED_GAP_SECONDS if done else WAIT_SECONDS

    def history_upper(self, account, stamp):
        """Where a connection's history ends: where its own import starts (a mailbox's first import, the week a
        calendar or WhatsApp rereads), a day earlier for WhatsApp and the Calendar so the two never meet."""
        state = self.store.checkpoint(account['id']) or {}
        if kind(account) == 'mail' and str(state.get('after') or '').isdigit():
            return dt.datetime.fromtimestamp(int(state['after']), dt.timezone.utc).isoformat()
        if kind(account) == 'slack' and re.fullmatch(r'\d+(\.\d+)?', str(state.get('after') or '')):
            return dt.datetime.fromtimestamp(float(state['after']), dt.timezone.utc).isoformat()  # its first import's window
        return history.before(stamp, int(self.config.get('bootstrap_days', 7)) + 1)

    def history_keep(self, account, events):
        """Kept as history (Store.commit_page history=True): new rows only, reviewed from the start. (kept, oldest)."""
        if not events:
            return 0, None
        kept = self.store.commit_page(account['id'], None, events, record_sync=False, history=True)
        return kept, min(e['occurred_at'] for e in events)

    def history_whatsapp(self, account, state):
        """One local read of the WhatsApp store (wacli, read-only): WHATSAPP_DAYS further back. A full window splits."""
        reader, event = self.HISTORY_SOURCES['whatsapp']
        source = reader(self.config, account)
        end = dt.datetime.fromisoformat(state.get('cursor') or state['upper'])
        target = dt.datetime.fromisoformat(state['target'])
        if end <= target:
            return 0, None, True
        start = max(target, end - dt.timedelta(days=WHATSAPP_DAYS))

        def read(a, b):
            rows = source.read(['messages', 'list', '--after', a.isoformat(), '--before', b.isoformat(), '--limit', str(WHATSAPP_LIMIT)]).get('messages')
            if not isinstance(rows, list):
                raise SourceError('whatsapp_invalid_page')
            if len(rows) < WHATSAPP_LIMIT or b - a <= dt.timedelta(hours=1):
                return rows  # a saturated hour keeps what it has: history needs no proof of completeness
            middle = a + (b - a) / 2
            return read(a, middle) + read(middle, b)

        events = {}
        for raw in read(start, end):
            try:
                e = event(account, raw if isinstance(raw, dict) else {})
            except SourceError:
                continue  # a row it can't take (a Channel post, an odd timestamp): skipped, as the sync does
            if not e['deleted']:
                events[e['source_id']] = e
        kept, oldest = self.history_keep(account, list(events.values()))
        state['cursor'] = start.isoformat()
        return kept, oldest, start <= target

    def history_connector(self, account, state):
        """One step of a connector's older messages (its history_page: Teams chats, LinkedIn and X messages), newest
        first, back to the target. Only what happened before `upper` is kept: the live sync owns the rest."""
        from machine.sources.connectors import CONNECTOR_HELPERS, load_connector
        module = load_connector(account.get('service'))
        if not module or not hasattr(module, 'history_page'):
            return 0, None, True
        events, done = module.history_page(self.config, account, CONNECTOR_HELPERS, state, state['upper'], state['target'])
        kept, oldest = self.history_keep(account, [e for e in events if not e.get('deleted') and e['occurred_at'] < state['upper']])
        return kept, oldest, done

    def history_slack(self, account, state):
        """One page of a Slack connection's older messages, newest first. The conversations are the collector's own
        list (users.conversations: the channels, private channels, direct and group messages the owner is in, never one
        more), most recently active first, each back to the target; then the replies of the threads found on the way.
        Reads only in Slack's slow lane (SLACK_GAP_SECONDS): None when it isn't its turn, so the others go."""
        from machine.sources.slack import slack_activity, slack_error, slack_limits, slack_page_names, slack_refused
        event = self.HISTORY_SOURCES['slack'][1]
        live = self.store.checkpoint(account['id']) or {}
        known = {c['id']: c for c in live.get('channels') or [] if isinstance(c, dict) and c.get('id') and not c.get('error')}
        if 'chats' not in state:  # no Slack call: the collector's list as it is now
            state.update(chats=[c['id'] for c in sorted(known.values(), key=slack_activity, reverse=True)], threads=[], cursor=None)
            return 0, None, not state['chats']
        while state['chats'] and state['chats'][0] not in known:
            state.update(chats=state['chats'][1:], cursor=None)  # left it since, or Slack refused it: never read here
        state['threads'] = [t for t in state.get('threads') or [] if t[0] in known]
        if not state['chats'] and not state['threads']:
            return 0, None, True
        if time.time() < float(state.get('next_at') or 0):
            return None
        source = self.slack_source(account)
        left = (self.__dict__.get('collector_rest_until') or {}).get(account['id'], 0) - time.monotonic()
        wait = source.limited_wait()
        if wait > SLACK_WAIT_MAX or left < wait + source.limited_gap():
            return None  # the collector reads now or soon: its read comes first, history takes a later minute
        state['next_at'] = time.time() + SLACK_GAP_SECONDS
        oldest = f"{dt.datetime.fromisoformat(state['target']).timestamp():.6f}"
        latest = f"{dt.datetime.fromisoformat(state['upper']).timestamp():.6f}"
        thread = None if state['chats'] else state['threads'][0]
        channel = known[thread[0] if thread else state['chats'][0]]
        params = {'channel': channel['id'], 'oldest': oldest, 'latest': latest, 'limit': slack_limits(account)['page']}
        if thread:
            params['ts'] = thread[1]
        if state.get('cursor'):
            params['cursor'] = state['cursor']
        try:
            page = source.get('conversations.replies' if thread else 'conversations.history', params)
        except SourceError as error:
            if slack_error(error) == 'slack_invalid_cursor':
                state['cursor'] = None
            elif slack_error(error) != 'slack_thread_not_found' and not slack_refused(error):
                raise
            else:  # gone, no longer the owner's, or refused for this one conversation: on to the next one
                state.update(cursor=None, **({'threads': state['threads'][1:]} if thread else {'chats': state['chats'][1:]}))
            return 0, None, False
        messages = [m for m in page.get('messages') or [] if isinstance(m, dict)]
        names = slack_page_names(self.store, channel, messages)
        events = []
        for raw in messages:
            if raw.get('subtype') == 'message_deleted' or (thread and raw.get('ts') == thread[1]):
                continue  # a deletion, or the thread's own first message (its conversation's walk has it)
            try:
                found = event(account, channel, raw, names)
            except SourceError:
                continue  # a message it can't take, as the sync skips it
            events.append(found)
            if not thread and raw.get('reply_count') and len(state['threads']) < SLACK_THREADS_KEEP:
                state['threads'].append([channel['id'], found['metadata']['message_ts']])
        kept, found_oldest = self.history_keep(account, events)
        state['cursor'] = (page.get('response_metadata') or {}).get('next_cursor') or None
        if not state['cursor']:
            state.update(**({'threads': state['threads'][1:]} if thread else {'chats': state['chats'][1:]}))
        return kept, found_oldest, not state['chats'] and not state['threads']

    def history_mail(self, account, state):
        """One page of the mailbox's older mail (Gmail or Outlook, the read-only sign-in it has), newest first."""
        reader, event = self.HISTORY_SOURCES['mail']
        source = reader(self.config, account)
        source.profile()  # the right mailbox, as every sync checks
        after = int(dt.datetime.fromisoformat(state['target']).timestamp())
        before = int(dt.datetime.fromisoformat(state['upper']).timestamp())
        if before <= after:
            return 0, None, True
        params = {'q': f'after:{after} before:{before}', 'maxResults': MAIL_PAGE}
        if state.get('token'):
            params['pageToken'] = state['token']
        page = source.get('messages', params)
        refs = [r['id'] for r in page.get('messages') or [] if isinstance(r, dict) and r.get('id')]
        with self.store.connect() as db:
            have = {r[0] for r in db.execute('SELECT source_id FROM events WHERE account_id=? AND source_id IN (' + ','.join('?' * len(refs)) + ')',
                                             (account['id'], *refs))} if refs else set()
        events = []
        for ref in refs:
            if ref in have:
                continue  # here already (a signal, or an earlier try of this page): not read again
            try:
                found = event(account, source.get('messages/' + ref, {'format': 'full'}), self.config)
            except SourceError as error:
                if error.status != 404:
                    raise
                continue
            if found:
                events.append(found)
        kept, oldest = self.history_keep(account, events)
        state['token'] = page.get('nextPageToken')
        return kept, oldest, not state['token']

    def history_calendar(self, account, state):
        """One page of the calendar's earlier meetings (the read-only sign-in it has), over the whole history window."""
        reader, event, excluded = self.HISTORY_SOURCES['calendar']
        source = reader(self.config, account)
        timezone = source.profile().get('timeZone') or 'UTC'
        if state['upper'] <= state['target']:
            return 0, None, True
        params = {'singleEvents': True, 'showDeleted': False, 'maxResults': CALENDAR_PAGE,
                  'timeMin': state['target'], 'timeMax': state['upper']}
        if state.get('token'):
            params['pageToken'] = state['token']
        page = source.get('events.list', params)
        events = []
        for raw in page.get('items') or []:
            if raw.get('status') == 'cancelled' or excluded(account, raw.get('summary')):
                continue
            e = event(account, raw, timezone)
            if e['occurred_at'] < state['upper']:
                events.append(e)
        kept, oldest = self.history_keep(account, events)
        state['token'] = page.get('nextPageToken')
        return kept, oldest, not state['token']

    def history_view(self, db, account_ids):
        """For the Connected cards: {account id: {'back_to': 'YYYY-MM', 'done', 'kept'}} (history.progress)."""
        return history.progress(db, account_ids)

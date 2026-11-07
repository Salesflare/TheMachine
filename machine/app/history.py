"""History backfill in the service: older WhatsApp messages, email and meetings brought in slowly in the background,
as history only (machine/store/history.py has the line between history and signal). A mixin of assistant.App
(APP_MIXINS); the source readers come from App.HISTORY_SOURCES (Gmail, Calendar and WhatsApp stay in assistant.py).

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
import re
import shutil
import sqlite3
import threading
import time

import abilities
import check_now
import embeddings
import graph
from machine import graph_history
from machine.store import history
from sources import SourceError, rate_limited, upstream_busy
from timeutil import now

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
MAIL, CALENDAR, WHATSAPP = ('gmail', 'outlook'), ('calendar', 'outlook_calendar'), ('whatsapp',)


def kind(account):
    service = account.get('service', 'gmail')
    return 'mail' if service in MAIL else 'calendar' if service in CALENDAR else 'whatsapp' if service in WHATSAPP else None


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
        if not history.depth(self.config) or not self.history_accounts():
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
        days, stamp = history.depth(self.config), now()
        resting, reading = self.__dict__.get('collector_resting'), False
        for account in self.history_accounts():
            with self.store.connect() as db:
                found = history.get(db, account['id'])
                imported = history.first_import_done(db, account['id'])
            if found and found['done_at'] and (found['depth_days'] or 0) >= days:
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
            if found and found['done_at']:  # a deeper setting since: walk on from where it stopped
                state.update(upper=state.get('target'), target=None, cursor=None, token=None)
            state['upper'] = state.get('upper') or self.history_upper(account, stamp)
            state['target'] = state.get('target') or history.before(stamp, days)  # fixed for the walk: a page token holds its query
            state.pop('error_at', None)
            try:
                kept, oldest, done = getattr(self, 'history_' + kind(account))(account, state)
            except SourceError as error:  # tried again later; the connection's own sync reports its errors
                LOG.info('history account=%s waits error=%s', account['id'], error)
                with self.store.connect() as db:
                    history.save(db, account['id'], {**state, 'error_at': stamp}, stamp)
                return self.history_waits('rate_limit' if self.history_rest(error) else 'error')
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

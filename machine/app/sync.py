"""Reading the owner's accounts: each account's collector with its lock and waits, a connector's sync, and what an
action-only connection may do. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import re
import secrets
import sqlite3
import threading
import time

from machine.config import LOG, SIGNIN_ERROR
from machine.faults import db_busy, DB_BUSY_RETRY
from machine.sources.connectors import ABILITY_CHECK_SECONDS, BUILT_IN_SERVICES, CONNECTOR_HELPERS, load_connector
from machine.sources.salesflare import salesflare_progress
from machine.sources.slack import Slack
from sources import gog_signed_in_since, SourceError
from timeutil import now


SALESFLARE_RESTART_SPREAD = 180  # seconds: team Machines restarted together start their Salesflare rounds apart


SALESFLARE_ROUND_SPREAD = 60  # seconds: and a fresh spread each round, so two whose starts landed close drift apart again


SYNC_LOCKS, SYNC_LOCKS_LOCK = {}, threading.Lock()


class SyncApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def started_at(self):
        """When this Machine started: `started_at` in the config (a hosted machine's signup), else its first own activity."""
        given = str(self.config.get('started_at') or '')
        if given:
            return given
        if getattr(self, '_started_at', None):  # found once, it stays: the poll asked each time, two passes over big tables
            return self._started_at
        with self.store.connect() as db:
            row = db.execute("SELECT MIN(t) FROM (SELECT MIN(started_at) t FROM analyses UNION ALL SELECT MIN(created_at) FROM suggestions"
                             " UNION ALL SELECT MIN(at) FROM sync_activity UNION ALL SELECT MIN(day) FROM sync_daily)").fetchone()
        self._started_at = row[0] if row and row[0] else None
        return self._started_at

    def resume_wait(self, account):
        """Seconds until a slow source (polled every 10 minutes or less often: LinkedIn, X, CRM) is due
        again after a restart. A restart alone must not cost an extra read; catch-up and new accounts go now.
        Salesflare too, whatever its poll: a round starts with its account lists ordered by activity, which run close
        to Salesflare's 2-minute gateway limit on a large team. A release restarts a team's Machines together, and
        each one starting that list at the same second answered 504 (HTTP gateway timeout), so after a finished
        round it waits out its gap plus a random spread. One mid-round goes now: its list is already read."""
        delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
        crm = account.get('service') == 'salesflare'
        if delay < 600 and not crm:
            return 0
        state = self.store.checkpoint(account['id']) or {}
        with self.store.connect() as db:
            row = db.execute('SELECT last_success FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
        unfinished = state.get('page_token') or state.get('catchup') or state.get('coverage_complete') is False
        if not row or not row['last_success'] or not state or state.get('mode') != 'incremental' or (unfinished and account.get('service') != 'x') \
                or (crm and state.get('window')):
            return 0
        since = (dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(row['last_success'])).total_seconds()
        return max(0, min(delay, delay - since)) + (secrets.randbelow(SALESFLARE_RESTART_SPREAD + 1) if crm else 0)

    def wait_for_retry(self, account, row):
        """Wait until the checkpoint's retry time; True when stopping. An expired Google sign-in
        is retried as soon as the owner signs in again, instead of after the full hour."""
        expired = bool(re.search(SIGNIN_ERROR, row['error'] or ''))
        while True:
            seconds = (dt.datetime.fromisoformat(row['retry_at']) - dt.datetime.fromisoformat(now())).total_seconds()
            if seconds <= 0:
                return False
            if expired and gog_signed_in_since(self.config, account, row['error_at']):
                LOG.info('sync account=%s signed in again, retrying now', account['id'])
                with self.store.connect() as db:
                    db.execute('UPDATE checkpoints SET retry_at=NULL WHERE account_id=?', (account['id'],))
                return False
            if self.stop.wait(min(seconds, 15) if expired else seconds):
                return True

    def sync_lock(self, account_id):
        """One sync of an account at a time: its collector, and a read right after a calendar change (sync_soon)."""
        with SYNC_LOCKS_LOCK:
            return SYNC_LOCKS.setdefault(account_id, threading.Lock())

    def ability_checker(self, account):
        """An action-only connection (Brings in signals off): nothing is read, but what it may do (a Docs connection's
        reads and writes, from its consent) is checked now and every ABILITY_CHECK_SECONDS, for its card."""
        plugin = load_connector(account.get('service', '')) if account.get('service') not in BUILT_IN_SERVICES else None
        refresh = getattr(plugin, 'refresh', None)
        while refresh and not self.stop.is_set():
            try:
                refresh(self.store, self.config, account, CONNECTOR_HELPERS)
            except Exception as error:  # noqa: BLE001 - the card keeps what it knew
                LOG.warning('ability check account=%s error=%s', account['id'], type(error).__name__)
            if self.stop.wait(ABILITY_CHECK_SECONDS):
                break

    def collector(self, account):
        source = Slack(self.config, account, self.stop) if account.get('service') == 'slack' else None
        try:
            wait = self.resume_wait(account)
        except Exception as error:  # never keep a source from starting
            LOG.warning('resume_wait account=%s error=%s', account['id'], type(error).__name__)
            wait = 0
        if wait:
            LOG.info('sync account=%s resumes in %ds (last read before the restart)', account['id'], wait)
            if self.stop.wait(wait):
                return
        while not self.stop.is_set():
            try:
                with self.store.connect() as db:
                    row = db.execute('SELECT retry_at,error,error_at FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                local_android_feed = account.get('service') == 'android' and account.get('transport') == 'openclaw-feed'
                if row and row['retry_at'] and not local_android_feed:
                    if self.wait_for_retry(account, row):
                        break
                delay = account.get('poll_seconds', self.config.get('poll_seconds', 300))
                try:
                    result = self.sync_retrying(account, source)
                    LOG.info('sync account=%s mode=%s read=%d filtered=%d skipped=%d', account['id'], result['mode'], result['events'], result.get('filtered', 0), result.get('skipped', 0))
                    state = self.store.checkpoint(account['id'])
                    if not result.get('stopped') and (result.get('more') or state.get('mode', result['mode']) != 'incremental' or state.get('page_token')):  # a plugin's checkpoint may not keep a mode
                        delay = account.get('poll_seconds', 3600) if account.get('service') == 'x' else 30 if account.get('service') == 'linkedin' else 0 if source else 5
                    elif account.get('service') == 'salesflare':
                        # A finished round: the next one opens with the slow account lists. Rounds of teammates' Machines
                        # take about as long, so two that started close stay together for hours (both answered 504 in a
                        # regular round, 41 minutes after a shared restart). A fresh spread each round breaks that up.
                        delay += secrets.randbelow(SALESFLARE_ROUND_SPREAD + 1)
                except SourceError as error:
                    if self.stop.is_set():
                        break
                    delay = error.retry_after or delay
                    error.retry_after = delay
                    if local_android_feed:
                        # Local queue reads may resume immediately when the bridge
                        # returns. Phone fallback attempts keep their own durable cap.
                        delay = account.get('poll_seconds', 15)
                    self.store.failed(account['id'], error)
                    LOG.warning('sync account=%s error=%s', account['id'], error)
                    # Enter the checkpoint wait directly so renewed sign-ins are watched.
                    # Ordinary failures and rate limits retain their normal backoff.
                    if re.search(SIGNIN_ERROR, str(error)):
                        continue
                except sqlite3.OperationalError as error:
                    if not db_busy(error):
                        safe = SourceError(type(error).__name__, retry_after=delay)
                        self.store.failed(account['id'], safe)
                        LOG.error('sync account=%s error=%s', account['id'], safe)
                    else:  # another writer held the database past the busy timeout: transient, read again soon
                        LOG.info('sync account=%s waits: database busy', account['id'])
                        delay = DB_BUSY_RETRY
                except Exception as error:
                    safe = SourceError(type(error).__name__, retry_after=delay)
                    self.store.failed(account['id'], safe)
                    LOG.error('sync account=%s error=%s', account['id'], safe)
            except Exception as error:
                # A database error here (locked, disk full) must never end this
                # account's thread silently while /health stays green.
                LOG.error('collector account=%s internal_error=%s', account['id'], type(error).__name__)
                delay = 60
            self.__dict__.setdefault('collector_reads', {})[account['id']] = time.time()  # a read ended (Check now waits for it)
            self.collector_rest(account['id'], delay)

    def connector_sync(self, args):
        """Stop, Start or Restart on a Salesflare card. Stop: nothing is read until Start, which goes on where it was.
        Restart: the round of accounts it was on is dropped, with its errors and wait, and a new one reads the last
        week again now (a round stuck on slow or failing accounts). What it brought in stays either way."""
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account')), None)
        if not account or account.get('service') != 'salesflare':
            raise ValueError('Only a Salesflare connection can be stopped or restarted here')
        do = args.get('do')
        if do not in ('stop', 'start', 'restart'):
            raise ValueError('Choose stop, start or restart')
        lock = self.sync_lock(account['id'])
        if not lock.acquire(timeout=20):
            raise ValueError('It is reading a batch of accounts. Try again in a minute')
        try:
            with self.store.connect() as db:
                row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
                state = json.loads(row['state'] or '{}') if row else {}
                if do == 'stop':
                    state['stopped'] = now()
                else:
                    state.pop('stopped', None)
                if do == 'restart':
                    state.pop('window', None)
                    state['next_full'] = 0
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?) ON CONFLICT(account_id) DO UPDATE SET state=excluded.state'
                           + ('' if do == 'stop' else ',error=NULL,retry_at=NULL,failures=0'), (account['id'], json.dumps(state)))
        finally:
            lock.release()
        LOG.info('connector_sync account=%s do=%s', account['id'], do)
        if do != 'stop':
            self.sync_soon(account['id'])
        return {'ok': True, 'do': do, 'salesflare': salesflare_progress(account, state)}

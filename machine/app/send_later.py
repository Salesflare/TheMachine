"""Send later in the service (machine/store/send_later.py has the rows): the owner's Change time, Cancel and Send now, the
step that takes a message back when someone wrote first or hands it to the outbox at its time, and the fresh read the
outbox asks for right before it goes. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json

import abilities
from machine.app.sync import sync_source
from machine.config import LOG
from machine.store import send_later
from machine import services, todo_states
from machine.owner_error import OwnerError
import next_actions
from sources import credential, MAIL_SERVICES
from timeutil import now

READABLE = services.of(flag='read_now')  # whose messages a read of the account brings in, right now
MIRRORS = ('telegram', 'signal')      # read by a mirror of ours that notes when it last reached the service
MIRROR_FRESH = dt.timedelta(minutes=15)
CATCH_UP = 5                          # reads of one account before it counts as not caught up
LOCK_SECONDS = 20                     # a longer read of that account is going on


class Unread(Exception):
    """The conversation couldn't be read to its end just now; why is for the log."""

    def __init__(self, why):
        super().__init__(why)


class SendLaterApp:
    ACTIONS = {'send_later_move': 'send_later_action', 'send_later_cancel': 'send_later_action', 'send_later_now': 'send_later_action'}

    def send_later_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise OwnerError('Scheduled messages are changed in the dashboard')
        sid, at = str(args.get('suggestion_id') or ''), now()
        send_at = send_later.pick_time(args.get('later')) if name == 'send_later_move' else None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if name == 'send_later_move':
                return send_later.move(db, sid, send_at, at)
            return send_later.cancel(db, sid, at) if name == 'send_later_cancel' else send_later.send_now(db, sid, at)

    def send_later_step(self):
        """Each round of the action worker: messages whose other side wrote first are taken back as soon as that is
        collected; the ones whose time came become outbox jobs, or ask when that was over an hour ago. Nothing here
        reads or sends anything outside."""
        with self.store.connect() as db:
            if not db.execute("SELECT 1 FROM scheduled_sends WHERE state='waiting'").fetchone():
                return
            db.execute('BEGIN IMMEDIATE')
            at, mine, own = now(), self.follow_up_mine(), self.follow_up_own(db)['emails']
            for row in db.execute("SELECT w.*,s.status,s.next_action FROM scheduled_sends w JOIN suggestions s ON s.id=w.suggestion_id "
                                  "WHERE w.state='waiting'").fetchall():
                if row['status'] in (todo_states.SNOOZED, todo_states.PREPARED) and next_actions.selected(row['next_action'], row['revision']):
                    news = send_later.replied(db, row, mine, own)
                    if news:
                        send_later.take_back(db, row, news, at)
            send_later.sweep(db, at)
            due = db.execute("SELECT * FROM scheduled_sends WHERE state='waiting' AND send_at<=? ORDER BY send_at,approved_at", (at,)).fetchall()
            for sid in dict.fromkeys(r['suggestion_id'] for r in due):
                rows = [r for r in due if r['suggestion_id'] == sid]
                off = next((x for r in rows if (x := abilities.refuse(self.config, json.loads(r['payload']).get('account_id')))), None)
                late = send_later.is_late(rows[0], at)
                if not off and not late:
                    send_later.release(db, rows, at)
                    continue
                for row in rows:
                    if off:
                        send_later.ask(db, row, 'stopped', off, at)
                    else:
                        send_later.ask_late(db, row, at)

    # -------------------------------------------------------------- right before it goes (action_step)

    def send_later_due(self, job):
        """Before anything else is done for this outbox job: the scheduled send it is, or None for any other send;
        'asked' when it is too late for it to go."""
        with self.store.connect() as db:
            row = send_later.of_job(db, job['id'])
            if row is None or job['status'] != 'queued':
                return None
            if not send_later.is_late(row, now()):
                return dict(row)
            db.execute('BEGIN IMMEDIATE')
            send_later.ask_late(db, row, now())
            return 'asked'

    def send_later_check(self, row):
        """The conversation read now, outside any transaction: who wrote first ([] nobody). Unread when it can't be read
        to its end."""
        action = json.loads(row['payload'])
        if action['kind'] == 'email_demo':
            return []
        with self.store.connect() as db:
            watch = send_later.watched(db, row['suggestion_id'], action)
        accounts = {a['id']: a for a in self.config.get('accounts') or () if isinstance(a, dict) and a.get('id')}
        sending = accounts.get(action.get('account_id'))
        if sending is None:
            raise Unread(why='account gone')
        news = []
        for account_id in sorted(watch['accounts'] & set(accounts)):
            account = accounts[account_id]
            if account.get('service') == 'slack':
                news += self.send_later_slack(account, action, watch, row)
            elif account.get('service', 'gmail') in READABLE:
                self.send_later_read(account, row['approved_at'])
            elif account is sending:
                raise Unread(why='service ' + str(account.get('service')))
        if action['kind'] == 'email':  # they may write to another mailbox of the owner's: read too, when it can be
            for account in accounts.values():
                if account.get('service', 'gmail') in MAIL_SERVICES and account['id'] not in watch['accounts']:
                    try:
                        self.send_later_read(account, row['approved_at'])
                    except Unread as error:
                        LOG.info('send later: other mailbox not read account=%s why=%s', account['id'], error)
        return news

    def send_later_read(self, account, since):
        """Collect this account's new messages now, until nothing new since the approval is left to read (Outlook: a
        message that couldn't be read waits in its checkpoint; one from long before is no news)."""
        lock = self.sync_lock(account['id'])
        if not lock.acquire(timeout=LOCK_SECONDS):
            raise Unread(why='a longer read is going on')
        try:
            for _ in range(CATCH_UP):
                result = sync_source(self.store, self.config, account) or {}
                state = self.store.checkpoint(account['id']) or {}
                left = any(str(w.get('since') or '') >= since for w in (state['waiting'] if isinstance(state.get('waiting'), dict) else {}).values())
                if result.get('mode', 'incremental') == 'incremental' and not (state.get('page_token') or result.get('more') or left):
                    break
            else:
                raise Unread(why='not caught up')
        except Unread:
            raise
        except Exception as error:  # noqa: BLE001 - offline, signed out, rate limited: it isn't read
            raise Unread(why=type(error).__name__) from None
        finally:
            lock.release()
        if account.get('service') in MIRRORS:
            seen = state.get('mirror_last_ok')
            try:
                fresh = dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(str(seen)) <= MIRROR_FRESH
            except (TypeError, ValueError):
                fresh = False
            if not fresh:
                raise Unread(why='mirror offline')

    def send_later_slack(self, account, action, watch, row):
        """Slack's own conversations, read directly: a whole workspace's sync takes too long right before a send."""
        transport = self.slack_reader()
        since = f"{dt.datetime.fromisoformat(row['approved_at']).timestamp():.6f}"
        mine = {str(account.get('user_id') or '')} | {str(u) for u in self.store.owner_user_ids}
        at = {**action, 'account_id': account['id']}
        places = {(k[1], None if k[2] == 'dm' else k[2]) for k in watch['keys'] if k[0] == account['id'] and len(k) == 3}
        news = []
        try:
            if action.get('kind') == 'slack' and action.get('account_id') == account['id'] and not action.get('thread'):
                places.add((transport.channel(at, transport.person(at)), None))
            for channel, thread in sorted(places, key=str):
                reply = (transport.call(at, 'conversations.replies', {'channel': channel, 'ts': thread, 'oldest': since, 'limit': 100}) if thread
                         else transport.call(at, 'conversations.history', {'channel': channel, 'oldest': since, 'limit': 100}))
                if not reply.get('ok'):
                    raise Unread(why='slack ' + str(reply.get('error') or ''))
                found = [m for m in reply.get('messages') or () if float(m.get('ts') or 0) > float(since)
                         and m.get('user') and m['user'] not in mine and not m.get('bot_id') and m.get('subtype') in (None, '', 'file_share', 'thread_broadcast')]
                if not found and reply.get('has_more'):
                    raise Unread(why='slack more')
                news += [{'id': m['ts'], 'mine': False, 'from': (action.get('to_name') or '') if m['user'] == action.get('user_id') else '',
                          'at': dt.datetime.fromtimestamp(float(m['ts']), dt.timezone.utc).isoformat()} for m in found]
        except Unread:
            raise
        except Exception as error:  # noqa: BLE001 - offline, signed out, rate limited: it isn't read
            raise Unread(why=type(error).__name__) from None
        return news

    def slack_reader(self):
        return next_actions.SlackTransport(self.config, credential)

    def send_later_recheck(self, row):
        """Right before it goes, after the outbox's own checks: True to go on, False when it was stopped or waits."""
        try:
            news = self.send_later_check(row)
        except Unread as error:
            LOG.info('send later: not read send=%s why=%s', row['id'], error)
            with self.store.connect() as db:
                send_later.wait_unread(db, row, now())
            return False
        if not news:
            return True
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            send_later.take_back(db, row, news, now())
        return False

    def send_later_admit(self, db, job):
        """In the outbox's own transaction, just before the one write: what the fresh read collected, and the time once
        more. False when it was stopped (or Cancel came first)."""
        row = send_later.of_job(db, job['id'])
        if row is None:  # Send now meanwhile, or Cancel (the job says so)
            return True
        if send_later.is_late(row, now()):
            send_later.ask_late(db, row, now())
            return False
        news = send_later.replied(db, row, self.follow_up_mine(), self.follow_up_own(db)['emails'])
        if news:
            send_later.take_back(db, row, news, now())
            return False
        send_later.read_again(db, row)
        return True

"""Settings, Notifications (App.action): what reaches the owner and when, a page saying it is in use, a test
notification, and the phone's and browser's push subscriptions. Moved out of assistant.App's action as is. A mixin of
assistant.App (APP_MIXINS)."""
import datetime as dt
import re
import sqlite3
import subprocess

import clear_pace
import i18n
import locale_prefs
from machine.app.recap import recap_escape, recap_meetings
from machine.cards import looks_done, NOT_FOR_OWNER_SQL, waits_on_others
from machine.config import LOG
from machine.delivery.push import (app_wake, cloud_target, mail_ready, phone_app, push_reach, push_send, quick_web,
                                   reply_waits, waiting_count)
from machine.delivery.telegram import DeliveryNotSent, telegram_request
from machine.model_usage import telegram_account, telegram_on
from machine.store.facts import suggestion_scope
from machine.store.promises import promise_text
import notify
import security_levels
import still_needed
import todo_areas
from timeutil import clock, in_hours, is_work_day, local_tz, next_work_day, now, WORK_HOURS


def done_today(db, start, current):
    """The to-dos closed as done between start and current (UTC ISO), by the owner or by The Machine (its closing
    decision, the one Undo takes back), not one that lapsed or was merged into another; the ones that matter first
    (urgent, then something went out for it, then the latest)."""
    rows = [dict(r) for r in db.execute(
        "SELECT s.id,s.title,s.urgent,s.account_ids,s.area,c.choice closed_by,coalesce(c.created_at,(SELECT max(d.created_at) FROM decisions d WHERE d.suggestion_id=s.id)) done_at,"
        "EXISTS(SELECT 1 FROM action_jobs j WHERE j.suggestion_id=s.id AND j.status IN ('sent','done')) went "
        "FROM suggestions s LEFT JOIN decisions c ON c.id=s.closed_decision_id WHERE s.status='completed' AND s.expired_at IS NULL "
        "AND s.id IN (SELECT suggestion_id FROM decisions WHERE created_at>=?)", (start,))]
    return sorted((r for r in rows if start <= str(r['done_at'] or '') <= current and r['closed_by'] != 'merge'),
                  key=lambda r: (int(r['urgent'] or 0), int(r['went'] or 0), str(r['done_at'])), reverse=True)


def to_read(db):
    """The ids of the to-dos that are something to read or sort, not to do: a Daily digest's (reading_digest.py) and a
    cleanup's (mail_cleanup.py). An area's digest leaves them out."""
    ids = set()
    for table in ('digest_items', 'mail_cleanup_items'):
        try:
            ids |= {r[0] for r in db.execute(f'SELECT DISTINCT suggestion_id FROM {table}')}
        except sqlite3.OperationalError:  # a database before that table
            pass
    return ids


class NotificationsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'notify_set': 'notify_action', 'notify_active': 'notify_action', 'notify_preview': 'notify_action',
               'push_test': 'push_test_action', 'app_push_register': 'app_push_action_handler',
               'app_push_unregister': 'app_push_action_handler', 'push_subscribe': 'push_subscribe_action',
               'push_unsubscribe': 'push_subscribe_action', 'area_digest': 'area_digest_action',
               'digest_sent': 'digest_sent_action', 'digest_row_hide': 'digest_row_hide_action'}

    def digest_row_hide_action(self, name, args, owner_dashboard=False):
        # To-dos, the Digest row's ×: hidden on every device until the next digest goes out or the next day
        # (notify.digest_row_hidden, the status's digest_row_hidden). The owner's own dashboard only
        if not owner_dashboard:
            raise ValueError('The digest is read in the dashboard')
        with self.store.connect() as db:
            notify.digest_row_hide(db, now())
        return {'digest_row_hidden': True}

    def digest_row_view(self):
        """Whether To-dos' Digest row stays set aside (notify.digest_row_hidden): the status's digest_row_hidden."""
        with self.store.connect() as db:
            return notify.digest_row_hidden(db, dt.datetime.fromisoformat(now()), local_tz())

    def digest_sent_action(self, name, args, owner_dashboard=False):
        # A tapped digest notification, or its email's link: the last morning or evening digest as it went
        # (notify.digest_shown), {} when none is kept or the kind is neither. The owner's own dashboard only, as the
        # area digest
        if not owner_dashboard:
            raise ValueError('The digest is read in the dashboard')
        with self.store.connect() as db:
            return notify.digest_shown(db, str(args.get('kind') or ''))

    def area_digest_action(self, name, args, owner_dashboard=False):
        # To-dos, Digest: each area's digest to read and copy (area_digests). The owner's own dashboard only: Personal
        # never reaches anyone else
        if not owner_dashboard:
            raise ValueError('The digest is read in the dashboard')
        return self.area_digests()

    def notify_action(self, name, args, owner_dashboard=False):
        # Settings, Notifications (notify.py)
        if not owner_dashboard:
            raise ValueError('Notifications are set in the dashboard')
        if name == 'notify_active':  # a page says whether it is in use (visible, in focus, touched lately) or not
            client = str(args.get('client') or 'page')
            if not re.fullmatch(r'[a-z0-9]{1,16}', client):
                raise ValueError('Invalid page')
            on = args.get('active', True) is not False
            try:
                idle = max(0, min(int(args.get('idle') or 0), 86400))
            except (TypeError, ValueError):
                idle = 0
            notify.mark_active(client=client, on=on, idle=idle)
            if on:
                with self.store.connect() as db:
                    notify.visited(db)  # kept: a few days without a visit and only the morning summary goes (notify.away)
            return {'active': notify.active()}
        if name == 'notify_preview':  # shown on the page only: nothing is sent
            digest = self.digest()
            return {'empty': not digest, 'text': digest['text'] if digest else '', 'push': digest['push'] if digest else None}
        with self.store.connect() as db:
            notify.set_pref(db, str(args.get('kind') or ''), str(args.get('channel') or ''), bool(args.get('on')))
        return self.notify_view()

    def push_test_action(self, name, args, owner_dashboard=False):
        # Settings or the nudge: one test notification to this device's own subscription
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        if 'app_device' in args:  # the mobile app: a test wakeup to that phone only
            device = str(args.get('app_device') or '')
            with self.store.connect() as db:
                known = notify.APP_ID.fullmatch(device) and any(d['id'] == device for d in notify.app_devices(db))
            if not known:
                raise ValueError('Notifications are off on this device. Turn them on first.')
            if not app_wake(self.store, self.config, 'test', 'push-test', device):
                raise ValueError('The test didn’t go through. Turn notifications off and on again.')
            return {'sent': True}
        with self.store.connect() as db:
            row = db.execute('SELECT endpoint,p256dh,auth FROM push_subscriptions WHERE endpoint=?', (str(args.get('endpoint') or ''),)).fetchone()
        if not row:
            raise ValueError('Notifications are off on this device. Turn them on first.')
        results = push_send(self.store, self.config, [dict(row)], {'title': i18n.t('Notifications are on'), 'body': i18n.t('This is how a new to-do shows up.'), 'url': '.', 'tag': 'push-test'}, 'test')
        if not any(200 <= r.get('status', 0) < 300 for r in results):
            raise ValueError('The test didn’t go through. Turn notifications off and on again.')
        return {'sent': True}

    def app_push_action_handler(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        return self.app_push_action(name, args)

    def push_subscribe_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        endpoint = str(args.get('endpoint') or '')
        if not re.fullmatch(r'https://[^\s]{1,2000}', endpoint):
            raise ValueError('Invalid push subscription')
        with self.store.connect() as db:
            if name == 'push_unsubscribe':
                db.execute('DELETE FROM push_subscriptions WHERE endpoint=?', (endpoint,))
                return {'subscribed': False}
            keys = args.get('keys') or {}
            if not all(re.fullmatch(r'[A-Za-z0-9_-]{16,200}=*', str(keys.get(k) or '')) for k in ('p256dh', 'auth')):
                raise ValueError('Invalid push subscription')
            db.execute('''INSERT INTO push_subscriptions(endpoint,p256dh,auth,created_at) VALUES(?,?,?,?)
                    ON CONFLICT(endpoint) DO UPDATE SET p256dh=excluded.p256dh,auth=excluded.auth''',
                       (endpoint, keys['p256dh'].rstrip('='), keys['auth'].rstrip('='), now()))
        return {'subscribed': True}

    def digest(self, current=None):
        """The morning digest as of `current` (notify.compose), or None when there is nothing to say."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        start = local.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + dt.timedelta(days=1)
        # Overnight: since the end of the last work day's hours (or a day back)
        hour, minute = clock(WORK_HOURS['end'])
        since = (local - dt.timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        if since > local:
            since -= dt.timedelta(days=1)
        utc = lambda t: t.astimezone(dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            meetings = recap_meetings(db, utc(start), utc(end), {})
            meetings = [m for m in meetings if m['at'] >= utc(local)] or []
            open_states = "('pending','accepted','prepared','instructions')"
            due = [dict(r) for r in db.execute(
                f"SELECT id,title FROM suggestions WHERE (status IN {open_states} AND due=? AND NOT {NOT_FOR_OWNER_SQL}) OR (status='snoozed' AND snoozed_until>=? AND snoozed_until<?) "
                "ORDER BY created_at LIMIT 20", (local.date().isoformat(), utc(local), utc(end)))]
            overnight = [dict(r) for r in db.execute(
                "SELECT id,title FROM suggestions WHERE status='pending' AND handled_hint IS NULL AND created_at>=? AND (due IS NULL OR due!=?) "
                "AND (deliver_after IS NULL OR deliver_after<=?) ORDER BY urgent DESC,created_at DESC LIMIT 20", (utc(since), local.date().isoformat(), utc(current)))]
            # What waits for the owner (waiting_count, the app's badge), in the dashboard's order (notify.open_order): the
            # ready ones (prepared, the dashboard's Ready) lead the digest; the rest is its "Waiting for you", without
            # what an earlier part already listed (notify.compose), so a pile still gets one
            later = still_needed.folded(db, utc(current), local_tz())  # a Still needed? left unanswered waits in Later
            top = notify.open_order([dict(r) for r in db.execute(
                "SELECT id,title,status,due,due_at,created_at,event_ids,next_action,outcome FROM suggestions WHERE status IN ('pending','prepared') AND NOT " + NOT_FOR_OWNER_SQL + " "
                "AND (deliver_after IS NULL OR deliver_after<=?) LIMIT 2000", (utc(current),)) if r['id'] not in later], local)
            ready = [r for r in top if r['status'] == 'prepared']
            # The ones that wait on the owner's answer (a run that stopped to ask, a result that asks): in the count, not
            # in the time to clear, as in the dashboard's header (crKind)
            stuck = {r[0] for r in db.execute("SELECT suggestion_id FROM preparations WHERE status='blocked'")}
            asking = [r['id'] for r in top if r['id'] in stuck or notify.asks(r.get('outcome'))]
            total = waiting_count(db)
            per = clear_pace.seconds(db, current)  # the owner's pace: "12 more can wait, about 5 min to clear."
            show = security_levels.notify_text(db, False)
            show_work = security_levels.notify_text(db, True)  # a Careful Work Fleet keeps Work titles out of email
        promised = notify.promised_today(self.store.promises(), top, local.date().isoformat(), lambda p: promise_text(p)[0])
        root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/') if self.config.get('dashboard_host') else ''
        when = lambda iso: locale_prefs.clock_text(dt.datetime.fromisoformat(iso).astimezone(local_tz()))
        # Each area's digest after the rest: the email goes to the owner's own address only, so Personal goes along;
        # Work as Work's own rules allow (a Careful Fleet: no Work titles in notifications)
        rows = self.area_rows(current) if show else {}
        if not show_work:
            rows.pop('work', None)
        areas = {a: notify.area_digest(*r) for a, r in rows.items()}
        digest = notify.compose(meetings, due, overnight, root, show, when, total=total, top=top, ready=ready, promised=promised,
                                per=per, name=notify.first_name(self.config.get('owner_name')), replies=[r['id'] for r in ready if reply_waits(r)], asking=asking,
                                areas=[(a, areas.get(a, '')) for a in notify.AREAS], area_rows=rows)
        if digest:  # the to-dos it speaks of, listed or counted: their held email lines go with it (digest_step)
            digest['covers'] = sorted({r['id'] for r in due + overnight + top if r.get('id')} |
                                      {p['covers'] for p in promised if p.get('covers')})
        return digest

    def area_digests(self, current=None):
        """Each area's digest as of `current` (notify.area_digest): {'work': text, 'personal': text}, '' for an area with
        nothing worth listing."""
        return {a: notify.area_digest(*r) for a, r in self.area_rows(current).items()}

    def area_rows(self, current=None):
        """What each area's digest is made from: {area: (done, open, today)}. An area as the To-dos filter places a to-do
        (suggestion_scope); one only about the Machine itself is in neither. Done: the to-dos closed as done today
        (done_today). Open: the ones still open in the dashboard's order, without what waits on others or looks done, one
        set aside by Still needed?, and a Daily digest or cleanup to-do (to read, not to do)."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        start = local.replace(hour=0, minute=0, second=0, microsecond=0)
        utc = lambda t: t.astimezone(dt.timezone.utc).isoformat()
        accounts = self.config.get('accounts', [])
        with self.store.connect() as db:
            skip = to_read(db) | still_needed.folded(db, utc(current), local_tz())
            done = [r for r in done_today(db, utc(start), utc(current)) if r['id'] not in skip]
            open_rows = notify.open_order([dict(r) for r in db.execute(
                "SELECT id,title,status,due,due_at,created_at,account_ids,area FROM suggestions WHERE status IN ('pending','accepted','prepared','instructions') "
                "AND NOT " + NOT_FOR_OWNER_SQL + " AND (deliver_after IS NULL OR deliver_after<=?) LIMIT 2000", (utc(current),)) if r['id'] not in skip], local)

        def area(r):
            if not accounts or r.get('account_ids') is None or todo_areas.machine_own(r['account_ids'], accounts, r.get('area')):
                return None
            return suggestion_scope(r['account_ids'], accounts, r.get('area'))
        today = local.date().isoformat()
        return {a: ([r for r in done if area(r) == a], [r for r in open_rows if area(r) == a], today) for a in notify.AREAS}

    def digest_step(self, current=None, push=None, telegram_send=None, mail=None):
        """Send the morning digest once on a work day, at its time, on the channels the owner picked."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        day = local.date().isoformat()
        with self.store.connect() as db:
            notify.ensure(db)
            prefs = notify.prefs(db)['digest']
            if not any(prefs.values()):
                return None
            sent = notify.digest_sent(db, day)
        if not notify.digest_due(local, self.config.get('digest_at', '08:30'), WORK_HOURS['start'], WORK_HOURS['end'], is_work_day, sent, WORK_HOURS['morning']):
            return None
        with self.store.connect() as db:
            if not notify.digest_claim(db, day, now()):
                return None
        digest = self.digest(current)
        went = self.digest_send(digest, prefs, 'digest', push, telegram_send, mail) if digest else []
        with self.store.connect() as db:
            notify.digest_done(db, day, 'sent' if went else 'empty' if not digest else 'not_sent', went, digest)
        LOG.info('digest day=%s channels=%s', day, ','.join(went) or '-')
        return went

    def digest_send(self, digest, prefs, label, push=None, telegram_send=None, mail=None):
        """One digest (the morning's or the evening's) on the channels the owner picked for the digest (prefs). Returns
        the channels it went on."""
        went = []
        if prefs.get('push'):
            subscriptions, phones = push_reach(self.store, self.config)
            if subscriptions or phones:
                payload = {**digest['push'], **({'silent': True} if notify.active() else {}),  # at the dashboard: no buzz
                           '_line': digest['push']['title'], '_body': digest['push']['body'].replace('\n', ' · '),  # the mobile app asks for these
                           'actions': quick_web('view')}
                if push_send(self.store, self.config, subscriptions, payload, label, push, wake='digest'):
                    went.append('push')
        if prefs.get('telegram') and telegram_on(self.config):
            try:
                (telegram_send or (lambda text: telegram_request(self.config, {'action': 'send', 'channel': 'telegram', 'accountId': telegram_account(self.config),
                                                                              'target': self.config.get('telegram_owner'), 'message': recap_escape(text),
                                                                              'presentation': {'blocks': [{'type': 'buttons', 'buttons': []}]}})))(notify.LINKS.sub('', digest['text']))
                went.append('telegram')
            except (DeliveryNotSent, subprocess.TimeoutExpired, ValueError) as error:
                LOG.warning('%s telegram error=%s', label, type(error).__name__)
        target = prefs.get('email') and self.notify_mail_target()
        if prefs.get('email') and not target:
            LOG.info('%s email skipped reason=not_paired', label)
        if target and (mail or notify.mail)(target[0], target[1], digest['subject'], digest['text']):
            went.append('email')
            if digest.get('covers'):
                with self.store.connect() as db:  # the hourly waiting-for-you email doesn't list them again
                    dropped = notify.drop_covered(db, ['suggestion:' + i for i in digest['covers']], notify.wall())
                if dropped:
                    LOG.info('notify email dropped digest=%d', dropped)
        return went

    def evening_digest(self, current=None, day=None):
        """The evening digest of the work day `day` (a date, default today) as of `current` (notify.evening_compose),
        or None when the day had nothing. Done: the to-dos closed as done today, by the owner or by The Machine (its
        closing decision, the one Undo takes back, made today), not one that lapsed or was merged into another; the ones
        that matter first (urgent, then something went out for it, then the latest). Meetings: today's with other people
        until now, the routine ones counted but not named. Open: the next work day's first meetings, what is due then
        (to-dos and the owner's own promises), and how many to-dos still need the owner."""
        current = current or dt.datetime.fromisoformat(now())
        tz = local_tz()
        day = day or current.astimezone(tz).date()
        start = dt.datetime.combine(day, dt.time(), tz)
        following = next_work_day(start + dt.timedelta(days=1))
        ahead_end = following + dt.timedelta(days=1)
        utc = lambda t: t.astimezone(dt.timezone.utc).isoformat()
        with self.store.connect() as db:
            done = done_today(db, utc(start), utc(current))
            named = {(m['at'], m['title']) for m in recap_meetings(db, utc(start), utc(current), {})}
            held = [{**m, 'named': (m['at'], m['title']) in named} for m in recap_meetings(db, utc(start), utc(current), {}, routine=True)]
            ahead = recap_meetings(db, utc(following), utc(ahead_end), {})[:2]
            due = [dict(r) for r in db.execute(
                "SELECT id,title,account_ids,area FROM suggestions WHERE status IN ('pending','accepted','prepared','instructions') AND due=? AND NOT " + NOT_FOR_OWNER_SQL + " "
                "ORDER BY urgent DESC,created_at LIMIT 20", (following.date().isoformat(),))]
            waiting = waiting_count(db)
            show = security_levels.notify_text(db, False)
        listed = {r['id'] for r in due}
        due += [{'id': p.get('suggestion_id'), 'title': promise_text(p)[0], 'account_ids': [p.get('account_id')]} for p in self.store.promises()
                if p['direction'] == 'mine' and p.get('due') == following.date().isoformat() and p['state'] in ('open', 'card')
                and p.get('suggestion_id') not in listed]
        # Work or Personal, the way the to-do's own label says (todo_areas.current); a meeting by its calendar's account
        accounts = self.config.get('accounts', [])
        unsure = 'work' if any(todo_areas.area_of_account(a) not in (None, todo_areas.PERSONAL) for a in accounts) else 'personal'
        side = lambda area: 'personal' if area == todo_areas.PERSONAL else 'work' if area else unsure
        by_id = {a.get('id'): a for a in accounts}
        for r in done + due:
            r['area'] = side(todo_areas.current(r.get('account_ids'), accounts, r.get('area')))
        for m in held + ahead:
            m['area'] = side(todo_areas.area_of_account(by_id[m['account']]) if m.get('account') in by_id else None)
        root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/') if self.config.get('dashboard_host') else ''
        when = lambda iso: locale_prefs.clock_text(dt.datetime.fromisoformat(iso).astimezone(tz))
        tomorrow = following.date() == day + dt.timedelta(days=1)
        return notify.evening_compose(done, held, waiting, due, ahead, root, show, when, name=notify.first_name(self.config.get('owner_name')),
                                      next_day=None if tomorrow else locale_prefs.day_text(following), tomorrow=tomorrow)

    def evening_step(self, current=None, push=None, telegram_send=None, mail=None):
        """Send the evening digest once on a work day at its time (notify.evening_time: evening_at, or 15 minutes before
        the end of the hours), on the channels the owner picked for it (Settings, Notifications, Evening digest), unless
        the day had nothing. Its row in notify_digests (evening:<day>) is taken before it is made, so a restart never
        sends it twice."""
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        with self.store.connect() as db:
            notify.ensure(db)
            prefs = notify.prefs(db)['evening']
            if not any(prefs.values()):
                return None
            at = notify.evening_time(self.config.get('evening_at'), WORK_HOURS['start'], WORK_HOURS['end'])
            day = notify.evening_due(local, at, WORK_HOURS['start'], WORK_HOURS['end'], is_work_day,
                                     lambda d: notify.digest_sent(db, notify.evening_key(d)))
        if not day:
            return None
        key = notify.evening_key(day)
        with self.store.connect() as db:
            if not notify.digest_claim(db, key, now()):
                return None
        digest = self.evening_digest(current, day)
        went = self.digest_send(digest, prefs, 'evening', push, telegram_send, mail) if digest else []
        with self.store.connect() as db:
            notify.digest_done(db, key, 'sent' if went else 'empty' if not digest else 'not_sent', went, digest)
        LOG.info('evening digest day=%s channels=%s', day, ','.join(went) or '-')
        return went

    def notify_step(self, current=None, push=None, mail=None):
        """Held notifications (notify.take_due): a push a minute after the owner left the dashboard, and one email for
        what is still unseen and waiting a while later. Within work hours only; a held push outside them is dropped."""
        local = (current or dt.datetime.now(dt.timezone.utc)).astimezone(local_tz())
        with self.store.connect() as db:
            notify.ensure(db)
            if not in_hours(local):
                notify.drop_pushes(db)
                return None
            pushes, lines = notify.take_due(db, self.notify_open)
            handoffs = notify.take_handoffs(db)
        subscriptions, phones = push_reach(self.store, self.config) if pushes else ([], 0)
        went = []
        if pushes and not subscriptions and not phones:
            with self.store.connect() as db:
                notify.delivered(db, pushes)  # nowhere to push to: dropped, not kept to go off later
            pushes = []
        for item in pushes:
            if push_send(self.store, self.config, subscriptions, item['payload'], 'held', push, kind=item['kind'], held=True):
                with self.store.connect() as db:
                    notify.delivered(db, [item])
                went.append('push')
        target = (lines or handoffs) and self.notify_mail_target()
        if target:
            root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/') if self.config.get('dashboard_host') else ''
            for item in handoffs:  # each its own email, once
                message = notify.handoff_mail(item, root)
                if (mail(*target, message['subject'], message['text']) if mail else notify.mail(*target, message['subject'], message['text'], delivery=item['delivery'])):
                    with self.store.connect() as db:
                        notify.delivered(db, [item])
                    went.append('email')
            message = notify.waiting_mail(lines, root) if lines else None
            if message and (mail(*target, message['subject'], message['text']) if mail else notify.mail(*target, message['subject'], message['text'], delivery=lines[0]['batch'])):
                with self.store.connect() as db:
                    notify.delivered(db, lines)
                    notify.mailed(db)
                went.append('email')
        if went:
            LOG.info('notify held channels=%s', ','.join(went))
        return went

    def app_push_action(self, name, args):
        """The mobile app's phones (app_push_register, app_push_unregister): the control plane keeps the push token and
        sends the wakeups (app_wake); this Machine keeps the phone's id, platform and name for Settings, never the token."""
        if name == 'app_push_unregister':
            device = str(args.get('id') or '')
            if not notify.APP_ID.fullmatch(device):
                raise ValueError('Invalid phone')
            target = cloud_target(self.config)
            answer = notify.app_push(*target, {'action': 'unregister', 'id': device}) if target else {'missing': True}
            if not answer:
                raise ValueError('Couldn’t remove this phone. Try again.')
            with self.store.connect() as db:
                notify.app_device_remove(db, [device])
            return {'removed': True}
        platform, token = args.get('platform'), args.get('token')
        if platform not in ('fcm', 'apns') or not isinstance(token, str) or not re.fullmatch(r'[A-Za-z0-9_:.-]{16,4096}', token):
            raise ValueError('Invalid phone')
        label = ' '.join(re.sub(r'[\x00-\x1f\x7f<>]', ' ', str(args.get('label') or '')).split())[:60]
        label = label or ('iPhone' if platform == 'apns' else 'Android')
        target = cloud_target(self.config)
        if not target:  # self-hosted off The Machine Network: the relay doesn't know it. The app works without them.
            return {'registered': False, 'reason': 'network'}
        # fetch: the app shows the notification itself, with what it asks this Machine for (GET /api/notice): the Android
        # app, and the iPhone's Notification Service extension
        answer = notify.app_push(*target, {'action': 'register', 'platform': platform, 'token': token, 'label': label,
                                           'sandbox': args.get('sandbox') is True, 'fetch': args.get('fetch') is True})
        device = str((answer or {}).get('id') or '')
        if not notify.APP_ID.fullmatch(device):
            raise ValueError('Couldn’t turn on notifications for this phone. Try again.')
        with self.store.connect() as db:
            notify.app_device_add(db, device, platform, label, now())
        LOG.info('app push registered platform=%s', platform)
        return {'registered': True, 'id': device, 'platform': platform, 'label': label}

    # -- notifications (notify.py): Settings, Notifications and the morning digest
    def notify_on(self, kind, channel):
        with self.store.connect() as db:
            return notify.allowed(db, kind, channel)

    def notify_mail_target(self):
        """(url, token) for the digest email through the control plane, or None (not hosted or paired)."""
        return cloud_target(self.config)

    def notify_open(self, ref):
        """Whether a held notification's to-do or Fleet question still waits for the owner."""
        what, _, key = ref.partition(':')
        with self.store.connect() as db:
            if what == 'suggestion':
                row = db.execute('SELECT s.status,s.handled_hint,s.outcome,p.status prep FROM suggestions s LEFT JOIN preparations p ON p.suggestion_id=s.id '
                                 'WHERE s.id=?', (key,)).fetchone()
                return bool(row) and not looks_done(dict(row)) and not waits_on_others(dict(row)) and (row['status'] in ('pending', 'prepared', 'instructions')
                                                                  or (row['status'] == 'accepted' and row['prep'] == 'blocked'))
            if what == 'fleet':
                try:
                    return bool(db.execute("SELECT 1 FROM fleet_in WHERE id=? AND status='waiting'", (key,)).fetchone())
                except sqlite3.OperationalError:
                    return False
        return True

    def notify_view(self):
        with self.store.connect() as db:
            prefs = notify.prefs(db)
            devices = db.execute('SELECT count(*) FROM push_subscriptions').fetchone()[0]
            phones = notify.app_devices(db)  # the mobile app's phones count as devices too, and are listed to remove
        return {'prefs': prefs, 'telegram': telegram_on(self.config), 'email': mail_ready(self.config),
                'push_devices': devices + len(phones), 'app_devices': phones,
                'app_push_ready': bool(cloud_target(self.config)), 'phone_app': phone_app(self.config),
                'push_ready': bool(self.config.get('dashboard_host')), 'digest_at': self.config.get('digest_at', '08:30'),
                'weekly_recap': self.recap_switch_view()}

    def waiting_handoffs_text(self):
        """Teammates' handoffs waiting for the owner, for the review (silent acceptance); nothing when off the Network."""
        try:
            return self.fleet.waiting_handoffs_text() if getattr(self, 'fleet', None) else ''
        except Exception as error:  # the review goes on without them
            LOG.warning('waiting handoffs error=%s', type(error).__name__)
            return ''

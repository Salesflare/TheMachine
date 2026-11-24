"""The waiting email goes only for what no push or Telegram message reached the owner about (notify.reached): shown on
their phone or browser, or taken by Telegram; accepted by a push service is not enough. Each case that is not reached
keeps the email. A busy day, before and after, at the end. Made-up to-dos only; every send here is a fake."""
import datetime as dt
import functools
import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a
import notify
import served
from machine.delivery import desk, push
from machine.delivery.telegram import DeliveryNotSent
from seams import patch_everywhere

UTC = dt.timezone.utc
REAL = dt.datetime
KEYS = {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}
PHONE, LAPTOP = 'https://fcm.googleapis.com/fcm/send/phone', 'https://fcm.googleapis.com/fcm/send/laptop'
ANDROID, IPHONE = 'Dalvik/2.1.0 (Linux; U; Android 15; Pixel 8)', 'TheMachine/12 CFNetwork/1568.1 Darwin/24.0.0'
ROBOT, DESKTOP = 'a' * 32, 'TheMachineRobot/1 (macos)'


class Clock(dt.datetime):
    at = REAL(2026, 10, 12, 10, 0, tzinfo=UTC)  # a Monday, within hours

    @classmethod
    def now(cls, tz=None):
        return cls.fromtimestamp(cls.at.timestamp(), tz or UTC)


class Base(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); desk.reset()
        self.addCleanup(notify.reset_active); self.addCleanup(desk.reset)
        Clock.at = REAL(2026, 10, 12, 10, 0, tzinfo=UTC)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        for patcher in (patch.object(dt, 'datetime', Clock), patch.object(notify.time, 'time', lambda: Clock.at.timestamp()),
                        patch_everywhere(a, 'telegram', side_effect=lambda config, row, action, message_id=None: self.telegram(row)),
                        patch_everywhere(a, 'cloud_target', return_value=('https://cp.example', 'tok')),
                        patch.object(notify, 'app_push', side_effect=self.cloud),
                        patch_everywhere(push, 'push_node', side_effect=lambda config, request: self.push_service(request))):
            patcher.start(); self.addCleanup(patcher.stop)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/',
                                         'telegram_owner': '42', 'credentials': {'fleet': 'fleet'}, 'fleet': {'url': 'https://cp.example/api/fleet'}}
        self.telegram = self.no_telegram
        self.statuses, self.pushed, self.woken, self.mails = {}, [], [], []
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': f'Quote {n}', 'body': 'Could you send the quote?', 'metadata': {}, 'deleted': False} for n in range(20)])

    # -- the fakes
    def no_telegram(self, row):
        return {'messageId': 'web-0123456789ab'}  # Telegram off: the dashboard has it

    def cloud(self, url, token, body):
        if body['action'] == 'register':
            return {'id': 'dev_1'}
        if body['action'] == 'wake':
            self.woken.append(body)
            return {'sent': 1, 'removed': 0}
        return {}

    def push_service(self, request):
        self.pushed.append(request)
        return {'results': [{'endpoint': s['endpoint'], 'status': self.statuses.get(s['endpoint'], 201)} for s in request['subscriptions']]}

    # -- what the owner has
    def browser(self, endpoint, computer):
        self.app.action('push_subscribe', {'endpoint': endpoint, 'keys': KEYS, 'computer': computer}, owner_dashboard=True)

    def phone_app(self):
        self.app.action('app_push_register', {'platform': 'fcm', 'token': 'fcm-token:' + 'A' * 140, 'label': 'Pixel 8', 'fetch': True}, owner_dashboard=True)

    # -- what happens
    def todo(self, n=1, deliver=True, **more):
        sid = self.store.suggest(f'quote {n}', f'Send quote {n}', 'They ask for the quote.', [n], urgent=more.pop('urgent', False), **more)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL WHERE id=?', (sid,))
        if deliver:
            self.deliver()
        return sid

    def deliver(self, why='reminder'):
        """why: what it can't wait for; a reminder neither urgent nor due, unless the test says otherwise."""
        with patch('machine.delivery.deliver.why_now', return_value=why):
            return a.deliver_one(self.store, self.config, edit_cards=False)

    def later(self, minutes):
        Clock.at += dt.timedelta(minutes=minutes)

    def step(self):
        return self.app.notify_step(Clock.at, mail=lambda url, token, subject, text: self.mails.append(text) or True)

    def browsers_show(self, *endpoints):
        """What sw.js says back, with the key its own push carried."""
        for request in self.pushed:
            for s in request['subscriptions']:
                if s['endpoint'] in endpoints:
                    push.shown(self.store, request['payload']['tag'], s['shown'])

    def phone_asks(self, agent=ANDROID):
        for wake in self.woken:
            push.shown(self.store, wake['tag'], agent=agent)

    def emailed(self):
        self.later(16)
        self.step()
        return len(self.mails)


class Reached(Base):
    def test_the_phone_app_showed_it(self):
        for agent in (ANDROID, IPHONE):
            with self.subTest(agent=agent):
                self.phone_app()
                self.todo(1 if agent == ANDROID else 2)
                self.assertEqual(len(self.woken), 1)
                self.phone_asks(agent)
                self.assertEqual(self.emailed(), 0)
                self.woken.clear()

    def test_a_phones_browser_showed_it(self):
        self.browser(PHONE, 'other')
        self.todo()
        self.browsers_show(PHONE)
        self.assertEqual(self.emailed(), 0)

    def test_a_phone_is_enough_for_what_is_urgent(self):
        self.browser(PHONE, 'other'); self.browser(LAPTOP, 'mac')
        self.todo(deliver=False); self.deliver('urgent')
        self.browsers_show(LAPTOP)
        self.browsers_show(PHONE)
        self.assertEqual(self.emailed(), 0)

    def test_a_computer_showed_what_is_not_urgent(self):
        self.browser(LAPTOP, 'linux')
        self.todo()
        self.browsers_show(LAPTOP)
        self.assertEqual(self.emailed(), 0)

    def test_telegram_took_it(self):
        self.telegram = lambda row: {'messageId': '77'}
        self.todo()
        self.assertEqual(self.emailed(), 0)

    def test_telegram_found_afterwards(self):
        """An unknown outcome whose message turns up in the chat (reconcile_uncertain)."""
        def timeout(row): raise ValueError('timeout')
        self.telegram = timeout
        sid = self.todo()
        self.later(3)
        with patch_everywhere(a, 'cached_card_ids', return_value=[78]):
            a.reconcile_uncertain(self.store, self.config)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0], 'sent')
        self.assertEqual(self.emailed(), 0)

    def test_the_robot_got_it(self):
        self.app.desk_look(ROBOT, True)
        self.todo()
        found = self.app.desk_look(ROBOT, True)['notices']
        self.assertEqual(len(found), 1)
        self.app.desk_look(ROBOT, True, [found[0]['key']])
        self.assertEqual(self.emailed(), 0)

    def test_a_newer_notification_replaces_the_line_and_one_reach_drops_it(self):
        self.browser(PHONE, 'other')
        sid = self.todo()
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='queued',reminder=1,last_notified_at=NULL WHERE suggestion_id=?", (sid,))
        notify.reset_active()
        self.deliver()
        self.browsers_show(PHONE)
        self.assertEqual(self.emailed(), 0)


class NotReached(Base):
    """Every one of these keeps its email."""
    def test_nothing_set_up(self):
        self.todo()
        self.assertEqual((self.pushed, self.woken), ([], []))
        self.assertEqual(self.emailed(), 1)
        self.assertIn('Send quote 1', self.mails[0])
        self.assertIn('no notification about it reached you', self.mails[0])

    def test_the_push_service_took_it_and_nothing_showed(self):
        """Permission off, the device off or offline, signed out: accepted (201), never shown."""
        self.browser(PHONE, 'other'); self.phone_app()
        self.todo()
        self.assertEqual((len(self.pushed), len(self.woken)), (1, 1))
        self.assertEqual(self.emailed(), 1)

    def test_an_expired_subscription(self):
        self.browser(PHONE, 'other')
        self.statuses[PHONE] = 410
        self.todo()
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM push_subscriptions').fetchone()[0], 0)
        self.assertEqual(self.emailed(), 1)

    def test_the_push_service_unreachable_or_refusing(self):
        for n, status in enumerate((0, 403, 500), 1):
            with self.subTest(status=status):
                self.browser(PHONE, 'other')
                self.statuses[PHONE] = status
                self.todo(n)
                self.assertEqual(self.emailed(), n)
                self.later(60)

    def test_the_cloud_did_not_take_the_wakeup(self):
        self.phone_app()
        notify.app_push.side_effect = None
        notify.app_push.return_value = None
        self.todo()
        self.assertEqual(self.emailed(), 1)

    def test_a_batchs_later_to_do_never_wakes_the_phone(self):
        self.phone_app()
        self.todo(1)
        self.phone_asks()
        self.later(1)
        self.todo(2)  # within three minutes of the first: silent, so no wakeup
        self.assertEqual(len(self.woken), 1)
        self.assertEqual(self.emailed(), 1)
        self.assertNotIn('Send quote 1', self.mails[0])
        self.assertIn('Send quote 2', self.mails[0])

    def test_push_turned_off_for_this_kind(self):
        self.browser(PHONE, 'other'); self.phone_app()
        with patch.object(notify, 'allowed', side_effect=lambda db, kind, channel: channel != 'push'):
            self.todo()
        self.assertEqual((self.pushed, self.woken), ([], []))
        self.assertEqual(self.emailed(), 1)

    def test_quiet_hours_held_the_push_and_dropped_it(self):
        """The push was held for the owner just leaving a dashboard, and the day ended: the next work hours email it."""
        self.browser(PHONE, 'other')
        with patch.object(notify, 'push_now', return_value=False):
            self.todo()
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='push'").fetchone()[0], 1)
        with patch('machine.app.notifications.in_hours', return_value=False):
            self.step()
        self.assertEqual((self.pushed, self.mails), ([], []))
        self.assertEqual(self.emailed(), 1)

    def test_telegram_refused_it(self):
        def refuse(row): raise DeliveryNotSent('blocked')
        self.telegram = refuse
        self.todo()
        self.assertEqual(self.emailed(), 1)
        for _ in range(6):  # tried again every minute, for hours: no second email
            self.later(30); self.deliver(); self.step()
        self.assertEqual(len(self.mails), 1)

    def test_telegram_did_not_answer(self):
        def timeout(row): raise ValueError('timeout')
        self.telegram = timeout
        self.todo()
        self.assertEqual(self.emailed(), 1)

    def test_telegram_refused_first_and_took_it_in_time(self):
        def refuse(row): raise DeliveryNotSent('blocked')
        self.telegram = refuse
        self.todo()
        self.later(2)
        self.telegram = lambda row: {'messageId': '79'}
        self.deliver()
        self.assertEqual(self.emailed(), 0)

    def test_telegram_without_a_buzz_while_a_dashboard_was_open(self):
        self.telegram = lambda row: {'messageId': '80'}
        with patch('machine.delivery.deliver.notify.active', return_value=True):
            self.todo()
        self.assertEqual(self.emailed(), 1)

    def test_what_is_urgent_or_due_shown_on_a_computer_only(self):
        for n, (why, computer) in enumerate((('urgent', 'mac'), ('due', 'windows'), ('urgent', None)), 1):
            with self.subTest(why=why, computer=computer):
                self.browser(LAPTOP, computer)
                self.todo(n, deliver=False); self.deliver(why)
                self.browsers_show(LAPTOP)
                self.assertEqual(self.emailed(), n)
                self.later(60)

    def test_what_is_urgent_got_by_the_robot_only(self):
        self.app.desk_look(ROBOT, True)
        self.todo(deliver=False); self.deliver('urgent')
        found = self.app.desk_look(ROBOT, True)['notices']
        self.app.desk_look(ROBOT, True, [n['key'] for n in found])
        self.assertEqual(self.emailed(), 1)

    def test_the_robot_never_named_it(self):
        self.app.desk_look(ROBOT, True)
        self.todo()
        self.app.desk_look(ROBOT, True)
        self.app.desk_look(ROBOT, True, ['deadbeef'])
        self.assertEqual(self.emailed(), 1)

    def test_only_a_known_device_counts(self):
        self.todo()
        with self.store.connect() as db:
            sid = db.execute("SELECT ref FROM notify_queue WHERE channel='email'").fetchone()[0].partition(':')[2]
        for key, agent in (('0' * 32, ANDROID), ('', ANDROID), ('', DESKTOP), ('', None)):  # no phone app here, no such browser
            push.shown(self.store, sid, key, agent)
        self.phone_app()
        push.shown(self.store, sid, agent=DESKTOP)
        push.shown(self.store, 'other', agent=ANDROID)
        push.shown(self.store, '', agent=ANDROID)
        self.assertEqual(self.emailed(), 1)

    def test_a_line_held_before_the_update_has_no_tag(self):
        with self.store.connect() as db:
            notify.hold(db, 'email', 'todo', 'Send quote 1', Clock.at.timestamp() + 900, ref='suggestion:x')
            self.assertEqual(notify.reached(db, 'x', 'phone'), 0)


class Fleet(Base):
    ROWS = [{'id': 'q1', 'kind': 'ask', 'text': 'one'}, {'id': 'q2', 'kind': 'ask', 'text': 'two'}]

    def ask(self, message_id=None):
        with patch_everywhere(a, 'fleet_push', side_effect=lambda store, config, rows: self.assertEqual(self.lines(), 2)), \
                patch('machine.app.fleet.fleet.asks_line', return_value='A question'), \
                patch('machine.app.fleet.fleet.telegram_message', return_value={}), \
                patch('machine.app.fleet.telegram_on', return_value=bool(message_id)), \
                patch('machine.app.fleet.fleet_telegram', return_value={'messageId': message_id}):
            return self.app.fleet_notify(self.ROWS)

    def lines(self):
        with self.store.connect() as db:
            notify.ensure(db)
            return db.execute("SELECT count(*) FROM notify_queue WHERE channel='email'").fetchone()[0]

    def test_nothing_reached_them(self):
        self.ask()
        self.assertEqual(self.lines(), 2)
        self.ask('not-a-message')
        self.assertEqual(self.lines(), 2)

    def test_telegram_took_them(self):
        self.assertEqual(self.ask('91'), '91')
        self.assertEqual(self.lines(), 0)

    def test_their_one_notification_showed(self):
        self.ask()
        with self.store.connect() as db:
            notify.reached(db, 'fleet-q1', 'phone')
        self.assertEqual(self.lines(), 0)


class Endpoint(Base):
    """GET api/notice, as the phone app and the dashboard's service worker ask it."""
    def test_what_counts_as_shown(self):
        self.browser(PHONE, 'other'); self.phone_app()
        self.app.token, self.app.stop, self.app.graph_dirty, self.app.owner_token = 'test-token', threading.Event(), threading.Event(), 'owner-key'
        self.config.update(tailscale_owner='owner@example.com', dashboard_host='machine.example:8443', port=0, http_timeout=1)
        port = served.serve(self)

        def get(path, agent, login='owner@example.com'):
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
            conn.request('GET', path, headers={'Host': 'machine.example:8443', 'Tailscale-User-Login': login, 'User-Agent': agent})
            r = conn.getresponse()
            body = json.loads(r.read())
            conn.close()
            return r.status, body

        def line():
            with self.store.connect() as db:
                notify.ensure(db)
                db.execute('DELETE FROM notify_queue')
                notify.hold(db, 'email', 'todo', 'Send quote 1', 0, ref='suggestion:card_1', payload={'tag': 'card_1', 'why': 'urgent'})

        def left():
            with self.store.connect() as db:
                return db.execute('SELECT count(*) FROM notify_queue').fetchone()[0]

        key = push.shown_key(PHONE)
        for path, agent, after in (('/api/notice?tag=card_1&v=2&kind=todo', ANDROID, 0), ('/api/notice?tag=card_1&v=2&kind=todo', IPHONE, 0),
                                   ('/api/notice?tag=card_1&shown=' + key, 'Mozilla/5.0 (iPhone)', 0),
                                   ('/api/notice?tag=card_1&v=2', ANDROID, 1),                # a button's title, nothing shown
                                   ('/api/notice?tag=card_1&v=2&kind=todo', DESKTOP, 1),      # the desktop app
                                   ('/api/notice?tag=card_1&shown=' + '0' * 32, ANDROID, 1),  # no such browser
                                   ('/api/notice?tag=card_2&shown=' + key, ANDROID, 1)):
            with self.subTest(path=path, agent=agent):
                line()
                self.assertEqual(get(path, agent)[0], 200)
                self.assertEqual(left(), after)
        line()
        with patch('sys.stderr'):
            self.assertEqual(get('/api/notice?tag=card_1&shown=' + key, ANDROID, login='someone@example.com')[0], 403)
        self.assertEqual(left(), 1)


class BusyDay(Base):
    """A made-up busy day: twelve to-dos that can't wait from 9:30 to 16:30, one of them shown on no phone (in a batch).
    Emails with the rule before (nothing counts as reached) and now."""
    MINUTES = (0, 31, 90, 92, 160, 161, 215, 270, 300, 340, 380, 420)

    def day(self, has, before=False):
        self.setUp()
        Clock.at = REAL(2026, 10, 12, 9, 30, tzinfo=UTC)
        {'app': self.phone_app, 'nothing': lambda: None, 'telegram': lambda: setattr(self, 'telegram', lambda row: {'messageId': '90'}),
         'laptop': functools.partial(self.browser, LAPTOP, 'mac'), 'phone off': self.phone_app}[has]()
        start, old = Clock.at, patch.object(notify, 'reached', return_value=0) if before else None
        if old:
            old.start()
        try:
            for minute in range(0, 450, 5):
                Clock.at = start + dt.timedelta(minutes=minute)
                for n, at in enumerate(self.MINUTES, 1):
                    if minute <= at < minute + 5:
                        Clock.at = start + dt.timedelta(minutes=at)
                        self.todo(n, deliver=False)
                        self.deliver('urgent' if n % 4 == 0 else 'reminder')
                        if before and has == 'telegram':  # it was held whatever Telegram said
                            push.hold_mail(self.store, self.config, 'todo', f'Send quote {n}', f'suggestion:{n}')
                        if has == 'app':
                            self.phone_asks()
                        self.browsers_show(LAPTOP)
                        self.woken.clear(); self.pushed.clear()
                Clock.at = start + dt.timedelta(minutes=minute + 4)
                with patch.object(self.app, 'notify_open', return_value=True, create=True):
                    self.step()
        finally:
            if old:
                old.stop()
        return len(self.mails)

    def test_emails_before_and_after(self):
        seen = {}
        for has in ('app', 'telegram', 'laptop', 'phone off', 'nothing'):
            seen[has] = (self.day(has, before=True), self.day(has))
        # the app's two: to-dos in a batch, which never woke it; the laptop's two: urgent. Without push the day's cap on
        # pushes (notify.PUSH_CAP) quiets nothing, so eight
        self.assertEqual(seen, {'app': (7, 2), 'telegram': (8, 0), 'laptop': (7, 2), 'phone off': (7, 7), 'nothing': (8, 8)})


if __name__ == '__main__':
    unittest.main()

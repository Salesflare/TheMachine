"""Notifications (notify.py): per kind and channel, quiet while the owner is at the dashboard, and the morning digest.
Every send here is a fake: no push service, Telegram or mail server is reached."""
import io, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import assistant as a
import notify
import timeutil
from seams import patch_everywhere  # noqa: E402

SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}
UTC = a.dt.timezone.utc


class Daytime(a.dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 12, 10, 0, tzinfo=tz or UTC)  # a Monday, within hours


class Notifications(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        self.sent = []
        self.sender = lambda request: self.sent.append(request) or {'results': [{'endpoint': SUB['endpoint'], 'status': 201}]}

    def card(self, key='one', title='Reply to the landlord', **extra):
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': key, 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        sid = self.store.suggest(key, title, 'Body', [1], **extra)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        return sid

    def test_defaults_have_email_for_every_kind_and_each_cell_saves(self):
        view = self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(view['prefs']['todo'], {'push': False, 'telegram': True, 'email': True})
        self.assertEqual(view['prefs']['digest'], {'push': True, 'telegram': False, 'email': True})
        self.assertEqual(view['prefs']['result'], {'push': True, 'telegram': True, 'email': True})
        self.assertEqual(view['prefs']['reminder'], {'push': True, 'telegram': True, 'email': True})
        self.assertFalse(self.app.action('notify_set', {'kind': 'todo', 'channel': 'email', 'on': False}, owner_dashboard=True)['prefs']['todo']['email'])
        for bad in ({'kind': 'todo', 'channel': 'sms'}, {'kind': 'spam', 'channel': 'push'}):
            with self.assertRaises(ValueError):
                self.app.action('notify_set', {**bad, 'on': True}, owner_dashboard=True)
        with self.assertRaises(ValueError):  # only the owner, on the dashboard
            self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': True})

    def test_presence_like_slack_in_use_idle_or_in_the_background(self):
        clock = [1000.0]
        at = lambda: clock[0]
        notify.mark_active(at, client='desk', on=True)
        self.assertTrue(notify.active(at))
        self.assertFalse(notify.push_now(at))  # in use: held, they may see it there
        clock[0] += 30
        notify.mark_active(at, client='desk', on=False, idle=2)  # the window went to the background
        self.assertFalse(notify.active(at))
        self.assertEqual(notify.last_seen(at), 1028)
        self.assertFalse(notify.push_now(at))
        clock[0] = 1028 + notify.AWAY_GRACE
        self.assertTrue(notify.push_now(at))  # a minute after they left
        # Focused but untouched: still in use for ten minutes, last seen when they stopped touching it
        clock[0] = 5000.0
        notify.mark_active(at, client='desk', on=True)
        clock[0] += 300
        notify.mark_active(at, client='desk', on=True, idle=300)
        self.assertTrue(notify.active(at))
        self.assertEqual(notify.last_seen(at), 5000)
        clock[0] += 300
        notify.mark_active(at, client='desk', on=False, idle=600)  # idle: away, a push may go
        self.assertFalse(notify.active(at))
        self.assertTrue(notify.push_now(at))
        self.assertEqual(notify.last_seen(at), 5000)
        # Another page in use (the phone) keeps them here; a page that stops beating (closed) lets go
        notify.mark_active(at, client='phone', on=True)
        self.assertTrue(notify.active(at))
        clock[0] += notify.ACTIVE_FOR + 1
        self.assertFalse(notify.active(at))
        # A page open in the background that was never in use changes nothing
        before = notify.last_seen(at)
        notify.mark_active(at, client='other', on=False)
        self.assertEqual(notify.last_seen(at), before)

    def test_the_page_says_in_use_or_not(self):
        self.app.action('notify_active', {'client': 'abc123', 'active': True}, owner_dashboard=True)
        self.assertTrue(notify.active())
        self.assertEqual(self.app.action('notify_active', {'client': 'abc123', 'active': False, 'idle': 'x'}, owner_dashboard=True), {'active': False})
        with self.assertRaises(ValueError):
            self.app.action('notify_active', {'client': '../x', 'active': True}, owner_dashboard=True)

    def held(self, mails=None):
        """A paired Machine with one phone: pushes into self.sent, emails into mails."""
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.config.update(credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        self.mails = [] if mails is None else mails
        self.mail = lambda url, token, subject, text: self.mails.append((subject, text)) or True

    def step(self, clock):
        with patch.object(notify.time, 'time', return_value=clock), patch_everywhere(a, 'local_tz', return_value=UTC), \
                patch_everywhere(a, 'credential', return_value='token'):
            return self.app.notify_step(current=a.dt.datetime.fromtimestamp(clock, UTC), push=self.sender, mail=self.mail)

    def deliver(self, sid, clock, row=None):
        with patch.object(notify.time, 'time', return_value=clock):
            a.push_notify(self.store, self.config, row or {'id': sid, 'title': 'Reply to the landlord', 'body': 'B', 'status': 'pending'}, self.sender)
            a.hold_mail(self.store, self.config, 'todo', 'Reply to the landlord', 'suggestion:' + sid)

    def test_just_left_the_dashboard_the_push_waits_a_minute_and_coming_back_cancels_it(self):
        self.held()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        notify.mark_active(lambda: t0, client='desk', on=True)
        notify.mark_active(lambda: t0 + 5, client='desk', on=False)  # switched to another app
        sid = self.card()
        self.deliver(sid, t0 + 10)
        self.assertEqual(self.sent, [])  # held
        self.assertEqual(self.step(t0 + 30), [])
        self.assertEqual(self.step(t0 + 5 + notify.AWAY_GRACE), ['push'])
        self.assertEqual(self.sent[0]['payload']['title'], 'Reply to the landlord')
        self.assertEqual(self.sent[0]['payload']['badge'], 1)
        # Next one: they come back before the minute is up, and see it there. No push, no email.
        sid2 = self.card('two', 'Pay the invoice')
        notify.mark_active(lambda: t0 + 100, client='desk', on=True)
        notify.mark_active(lambda: t0 + 101, client='desk', on=False)
        self.deliver(sid2, t0 + 102, {'id': sid2, 'title': 'Pay the invoice', 'body': 'B', 'status': 'pending'})
        notify.mark_active(lambda: t0 + 120, client='desk', on=True)
        notify.mark_active(lambda: t0 + 125, client='desk', on=False)
        self.assertEqual(self.step(t0 + 3000), [])
        self.assertEqual(len(self.sent), 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE ref='suggestion:'||?", (sid2,)).fetchone()[0], 0)

    def test_in_use_nothing_buzzes_and_nothing_is_emailed(self):
        self.held()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        notify.mark_active(lambda: t0, client='desk', on=True)
        sid = self.card()
        self.deliver(sid, t0 + 1)
        notify.mark_active(lambda: t0 + 60, client='desk', on=True)
        with self.assertLogs(a.LOG, 'INFO') as logs:
            self.assertEqual(self.step(t0 + 60 + notify.EMAIL_AFTER), [])
        self.assertEqual((self.sent, self.mails), ([], []))
        # the log says why no email went: it was seen on a dashboard while it waited
        self.assertIn('notify email dropped seen=1 stale=0 handled=0', '\n'.join(logs.output))

    def test_still_unseen_after_a_while_one_email_bundles_what_waits_at_most_hourly(self):
        self.held()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()  # away since the start: pushes go at once
        one, two, done = self.card(), self.card('two', 'Pay the invoice'), self.card('three', 'Book the venue')
        self.deliver(one, t0)
        with patch.object(notify.time, 'time', return_value=t0 + 60):
            a.hold_mail(self.store, self.config, 'result', 'Ready: Pay the invoice', 'suggestion:' + two)
            a.hold_mail(self.store, self.config, 'todo', 'Book the venue', 'suggestion:' + done)
        self.assertEqual(len(self.sent), 1)
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='dismissed' WHERE id=?", (done,))  # handled on Telegram meanwhile
        with self.assertLogs(a.LOG, 'INFO') as logs:
            self.assertEqual(self.step(t0 + notify.EMAIL_AFTER - 1), [])
        self.assertIn('notify email dropped seen=0 stale=0 handled=1', '\n'.join(logs.output))
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER), ['email'])
        subject, text = self.mails[0]
        self.assertEqual(subject, '2 things wait for you')
        self.assertIn('• Reply to the landlord', text)
        self.assertIn('• Ready: Pay the invoice', text)
        self.assertNotIn('Book the venue', text)
        self.assertIn('Open The Machine: https://the-machine.example/assistant/', text)
        # More comes in: it waits for the hour to be up, then goes alone
        four = self.card('four', 'Answer the school')
        with patch.object(notify.time, 'time', return_value=t0 + 1000):
            a.hold_mail(self.store, self.config, 'todo', 'Answer the school', 'suggestion:' + four)
        self.assertEqual(self.step(t0 + 1000 + notify.EMAIL_AFTER), [])
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER + notify.EMAIL_EVERY), ['email'])
        self.assertEqual(self.mails[1][0], 'Waiting for you: Answer the school')

    def test_email_follows_its_switch_the_security_level_and_the_hours(self):
        self.held()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        sid = self.card()
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'email', 'on': False}, owner_dashboard=True)
        with patch.object(notify.time, 'time', return_value=t0):
            self.assertFalse(a.hold_mail(self.store, self.config, 'todo', 'Reply to the landlord', 'suggestion:' + sid))
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'email', 'on': True}, owner_dashboard=True)
        with patch.object(a.security_levels, 'notify_text', return_value=False), patch.object(notify.time, 'time', return_value=t0):
            self.assertTrue(a.hold_mail(self.store, self.config, 'todo', 'Reply to the landlord', 'suggestion:' + sid))
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER), ['email'])
        self.assertEqual(self.mails[0][0], '1 thing waits for you')
        self.assertNotIn('landlord', self.mails[0][1])
        # Not hosted or paired: nothing to send it with, so nothing is held
        self.assertFalse(a.hold_mail(self.store, {'accounts': []}, 'todo', 'T', 'suggestion:' + sid))
        # Outside work hours a held push is dropped (the digest has it)
        with self.store.connect() as db:
            notify.hold(db, 'push', 'todo', 'T', t0, payload={'title': 'T'})
        night = a.dt.datetime(2026, 10, 12, 23, 30, tzinfo=UTC).timestamp()
        with patch.dict(timeutil.WORK_HOURS, dict(timeutil.WORK_HOURS_DEFAULT, end='18:00')):
            self.assertIsNone(self.step(night))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='push'").fetchone()[0], 0)

    def handoff(self, key='q_' + 'a' * 16, title='Fix the tag leaks', kind='handoff'):
        """A teammate's handoff waiting for the owner, as fleet_in has it."""
        question = {'title': title, 'summary': 'Customer data in the export, see the thread', 'contact': ''} if kind == 'handoff' else {'about': 'Acme'}
        row = {'id': key, 'fleet': 'fl_x', 'member_id': 'k', 'name': 'Kim Lee', 'kind': kind, 'question': json.dumps(question),
               'status': 'waiting', 'at': a.now()}
        with self.store.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS fleet_in(id TEXT PRIMARY KEY,fleet TEXT NOT NULL,member_id TEXT NOT NULL,name TEXT NOT NULL,'
                       'kind TEXT NOT NULL,question TEXT NOT NULL,status TEXT NOT NULL,at TEXT NOT NULL,decided_at TEXT)')
            db.execute('INSERT INTO fleet_in(id,fleet,member_id,name,kind,question,status,at) VALUES(?,?,?,?,?,?,?,?)', tuple(row.values()))
        return row

    def paired(self):
        """Hosted or paired, so email can go, but no phone and no Telegram."""
        self.config.update(credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        self.mails = []
        self.mail = lambda url, token, subject, text: self.mails.append((subject, text)) or True

    def test_a_handoff_to_an_owner_nothing_else_reaches_is_emailed_once_with_its_title_and_a_link(self):
        self.paired()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        row = self.handoff()
        with patch.object(notify.time, 'time', return_value=t0):
            self.app.fleet_notify([row])
            self.app.fleet_notify([row])  # told twice: still one email
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER - 1), [])
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER), ['email'])
        self.assertEqual(len(self.mails), 1)
        subject, text = self.mails[0]
        self.assertEqual(subject, 'Kim Lee handed you a to-do: Fix the tag leaks')
        self.assertIn('[Accept or decline it on The Machine](https://the-machine.example/assistant/#fleet=' + row['id'] + ')', text)
        self.assertIn('Turn it off in Settings, Notifications.', text)
        self.assertNotIn('Customer data', text)  # the title only, never their summary
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER + notify.EMAIL_EVERY), [])
        self.assertEqual(len(self.mails), 1)

    def test_a_handoff_email_that_keeps_failing_is_retried_for_a_day_not_forever(self):
        self.paired()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        row = self.handoff()
        with patch.object(notify.time, 'time', return_value=t0):
            self.app.fleet_notify([row])
        self.mail = lambda *args: False  # the control plane doesn't take it
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER), [])
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER + 61), [])  # kept and tried again
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='handoff'").fetchone()[0], 1)
        self.step(t0 + notify.HANDOFF_STALE + 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='handoff'").fetchone()[0], 0)

    def test_a_held_push_with_no_phone_left_is_dropped_not_kept_for_later(self):
        self.held()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        notify.mark_active(lambda: t0, client='desk', on=True)
        notify.mark_active(lambda: t0 + 5, client='desk', on=False)
        self.deliver(self.card(), t0 + 10)
        with self.store.connect() as db:
            db.execute('DELETE FROM push_subscriptions')  # the phone unsubscribed meanwhile
        self.assertEqual(self.step(t0 + 5 + notify.AWAY_GRACE), [])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel='push'").fetchone()[0], 0)

    def test_no_handoff_email_with_a_phone_or_telegram_once_seen_or_handled_or_switched_off(self):
        self.paired()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        later = t0 + notify.EMAIL_AFTER + 60
        # Seen on the dashboard in the meantime
        seen = self.handoff('q_' + 'b' * 16)
        with patch.object(notify.time, 'time', return_value=t0):
            self.app.fleet_notify([seen])
        notify.mark_active(lambda: t0 + 30, client='desk', on=True)
        notify.mark_active(lambda: t0 + 40, client='desk', on=False)
        # Accepted on another device before it was due
        taken = self.handoff('q_' + 'c' * 16)
        with patch.object(notify.time, 'time', return_value=t0 + 50):
            self.app.fleet_notify([taken])
        with self.store.connect() as db:
            db.execute("UPDATE fleet_in SET status='accepted' WHERE id=?", (taken['id'],))
        self.assertEqual(self.step(later), [])
        # Email off for results: nothing held
        self.app.action('notify_set', {'kind': 'result', 'channel': 'email', 'on': False}, owner_dashboard=True)
        self.assertFalse(a.hold_handoff(self.store, self.config, self.handoff('q_' + 'd' * 16)))
        self.app.action('notify_set', {'kind': 'result', 'channel': 'email', 'on': True}, owner_dashboard=True)
        # Telegram reaches them: no email for a handoff
        self.config['telegram_owner'] = '42'
        with patch_everywhere(a, 'fleet_telegram', return_value={}), patch.object(a.fleet, 'telegram_message', return_value={}), \
                patch.object(notify.time, 'time', return_value=later):
            self.app.fleet_notify([self.handoff('q_' + 'e' * 16)])
        del self.config['telegram_owner']
        # A phone reaches them: no email either
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        with patch_everywhere(a, 'push_send', return_value=[]), patch.object(notify.time, 'time', return_value=later):
            self.app.fleet_notify([self.handoff('q_' + 'f' * 16)])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notify_queue WHERE channel IN ('handoff','email')").fetchone()[0], 0)
        self.assertEqual(self.step(later + notify.EMAIL_AFTER), [])
        self.assertEqual(self.mails, [])

    def test_a_handoff_email_in_careful_has_no_title_and_other_fleet_questions_keep_the_bundle(self):
        self.paired()
        t0 = a.dt.datetime(2026, 10, 12, 10, 0, tzinfo=UTC).timestamp()
        with patch.object(a.security_levels, 'notify_text', return_value=False), patch.object(notify.time, 'time', return_value=t0):
            self.app.fleet_notify([self.handoff()])
        with patch.object(notify.time, 'time', return_value=t0), patch.object(a.fleet, 'question_text', return_value='Who knows Acme?'):
            self.app.fleet_notify([self.handoff('q_' + 'g' * 16, kind='relationships')])
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER), ['email', 'email'])
        (careful, body), (bundle, _) = self.mails
        self.assertEqual(careful, 'Kim Lee handed you a to-do')
        self.assertNotIn('tag leaks', careful + body)
        self.assertEqual(bundle, "Waiting for you: Kim Lee's Machine asks: Who knows Acme?")

    def test_handoff_mail_reads_in_the_owners_language(self):
        item = {'name': 'Kim Lee', 'title': 'Fix the tag leaks', 'show': True, 'id': 'q_1'}
        self.addCleanup(a.locale_prefs.configure, {})
        for lang, words in (('nl', 'gaf je een to-do door: Fix'), ('fr', 'vous a transféré')):
            a.locale_prefs.configure({'language': lang})
            self.assertIn(words, notify.handoff_mail(item, 'https://m.example/')['subject'])
            self.assertIn('https://m.example/#fleet=q_1', notify.handoff_mail(item, 'https://m.example/')['text'])
        a.locale_prefs.configure({})
        message = notify.handoff_mail(item, 'https://m.example/')
        self.assertEqual(message['subject'], 'Kim Lee handed you a to-do: Fix the tag leaks')
        self.assertTrue(message['text'].startswith('[Accept or decline it on The Machine](https://m.example/#fleet=q_1)\n\n'))
        self.assertEqual(notify.handoff_mail(dict(item, name=''), '')['subject'], 'Your teammate handed you a to-do: Fix the tag leaks')

    def test_kinds_of_a_card_delivery(self):
        self.assertEqual(notify.kind_of({'status': 'pending'}), 'todo')
        self.assertEqual(notify.kind_of({'status': 'pending', 'reminder': 1}), 'reminder')
        self.assertEqual(notify.kind_of({'status': 'prepared', 'reminder': 1}), 'result')
        self.assertEqual(notify.kind_of({'status': 'accepted', 'reminder': 1, 'preparation_status': 'blocked'}), 'result')
        self.assertEqual(notify.kind_of({'status': 'prepared', '_result_notice': True}), 'result')

    def test_push_follows_the_setting_carries_the_badge_and_waits_while_the_owner_is_here(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.card()
        row = {'id': 'x' * 16, 'title': 'T', 'body': 'B', 'status': 'pending'}
        a.push_notify(self.store, self.config, row, self.sender)
        self.assertEqual(self.sent[-1]['payload']['badge'], 1)
        self.app.action('notify_active', {}, owner_dashboard=True)
        self.assertEqual(a.push_notify(self.store, self.config, row, self.sender), [])
        self.assertEqual(a.fleet_notice_push(self.store, self.config, {'id': 'n1', 'kind': 'joined', 'text': 'Someone joined', 'url': 'x', 'title': 'Joined'}, self.sender), [])
        self.assertEqual(len(self.sent), 1)
        notify.reset_active()
        self.app.action('notify_set', {'kind': 'reminder', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(a.push_notify(self.store, self.config, dict(row, reminder=1), self.sender), [])
        a.push_notify(self.store, self.config, row, self.sender)  # a new to-do still goes
        self.assertEqual(len(self.sent), 2)
        # A test notification has no kind: it always goes, as the owner asked for it.
        self.assertTrue(a.push_send(self.store, self.config, [SUB | {'p256dh': 'p', 'auth': 'a'}], {'title': 't'}, 'test', self.sender))

    def test_active_is_a_recent_heartbeat(self):
        clock = [1000.0]
        notify.mark_active(lambda: clock[0])
        self.assertTrue(notify.active(lambda: clock[0] + 60))
        self.assertFalse(notify.active(lambda: clock[0] + notify.ACTIVE_FOR + 1))

    def test_telegram_off_for_to_dos_keeps_the_card_off_telegram_and_on_the_phone(self):
        sid = self.card()
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'telegram', 'on': False}, owner_dashboard=True)
        config = dict(self.config, telegram_owner='42')
        with patch.object(a.dt, 'datetime', Daytime), patch_everywhere(a, 'telegram', side_effect=AssertionError('no Telegram')), \
                patch_everywhere(a, 'push_notify') as push:
            self.assertTrue(a.deliver_one(self.store, config, edit_cards=False))
        self.assertEqual([c.args[2]['id'] for c in push.call_args_list], [sid])
        with self.store.connect() as db:
            message = db.execute('SELECT message_id FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0]
        self.assertTrue(message.startswith('web-'))
        # Its later edits and result notices never go to Telegram for a card that isn't there.
        with patch.object(a.subprocess, 'run', side_effect=AssertionError('no Telegram helper')):
            self.assertEqual(a.telegram_request(config, {'action': 'edit', 'messageId': message}), {'messageId': message})
        with patch_everywhere(a, 'telegram_request', side_effect=lambda config, args: args) as request:
            args = a.telegram(dict(config), {'id': sid, 'title': 'T', 'status': 'prepared', 'message_id': message, '_result_notice': True}, 'send')
        self.assertNotIn('replyTo', args)

    def test_at_the_dashboard_telegram_arrives_silently(self):
        self.card()
        self.app.action('notify_active', {}, owner_dashboard=True)
        seen = []
        with patch.object(a.dt, 'datetime', Daytime), patch_everywhere(a, 'telegram', side_effect=lambda c, row, action: seen.append(row) or {'messageId': '7'}), \
                patch_everywhere(a, 'push_notify'):
            a.deliver_one(self.store, dict(self.config, telegram_owner='42'), edit_cards=False)
        self.assertTrue(seen[0]['_silent'])

    def test_the_snooze_promise_follows_the_reminders_row(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        config = dict(self.config, telegram_owner='42')
        say = lambda: a.reminder_line(a.reminder_channels(self.store, config))
        self.assertEqual(say(), 'I’ll remind you on Telegram and as a notification.')
        self.app.action('notify_set', {'kind': 'reminder', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(say(), 'I’ll remind you on Telegram.')
        self.app.action('notify_set', {'kind': 'reminder', 'channel': 'telegram', 'on': False}, owner_dashboard=True)
        self.assertEqual(say(), 'It’ll be back on the dashboard then.')

    def test_a_held_to_do_names_the_channels_of_the_to_dos_row(self):
        # The chip on a to-do held for later ("Telegram Mon 2 Nov · 08:30") follows New to-dos, not Reminders.
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        config = self.app.config = dict(self.config, telegram_owner='42')
        channels = lambda: a.reminder_channels(self.store, config, 'todo')
        self.assertEqual(channels(), {'telegram': True, 'push': 1})
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'telegram', 'on': False}, owner_dashboard=True)
        self.assertEqual(channels(), {'telegram': False, 'push': 1})
        self.assertEqual(a.reminder_channels(self.store, config), {'telegram': True, 'push': 1})  # Reminders keep their own row
        self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(channels(), {'telegram': False, 'push': 0})

    def test_digest_time(self):
        work_day = lambda local: local.isoweekday() <= 5
        at = lambda h, m=0, d=12: a.dt.datetime(2026, 10, d, h, m, tzinfo=UTC)
        due = lambda local, digest='08:30', start='08:00', end='18:00', sent=False: notify.digest_due(local, digest, start, end, work_day, sent)
        self.assertFalse(due(at(8, 29)))
        self.assertTrue(due(at(8, 30)))
        self.assertFalse(due(at(8, 30), sent=True))
        self.assertFalse(due(at(12, 0)))  # more than three hours late: the next work day
        self.assertFalse(due(at(9, 0, d=17)))  # a Saturday
        self.assertFalse(due(at(7, 0), digest='07:00'))  # before the hours: it waits for their start
        self.assertTrue(due(at(8, 0), digest='07:00'))

    def test_compose_says_nothing_when_empty_and_only_counts_when_careful(self):
        self.assertIsNone(notify.compose([], [], []))
        meetings = [{'at': '2026-10-12T09:30:00+00:00', 'title': 'Planning with the agency'}]
        overnight = [{'title': f'To-do {n}'} for n in range(5)]
        full = notify.compose(meetings, [{'title': 'Pay the invoice'}], overnight, 'https://m.example/')
        self.assertEqual(full['push']['title'], 'Your morning')
        self.assertEqual(full['push']['body'], '6 to-dos: Pay the invoice, To-do 0, … · First meeting 09:30')
        self.assertIn('• Pay the invoice', full['text'])
        self.assertIn('• +2 more', full['text'])
        self.assertTrue(full['text'].endswith('Open The Machine: https://m.example/'))
        careful = notify.compose(meetings, [], overnight, '', show_text=False)
        self.assertEqual(careful['push']['body'], '5 to-dos waiting · First meeting 09:30')
        self.assertNotIn('agency', careful['text'] + careful['subject'])

    def test_the_morning_push_says_what_waits_and_when_the_first_meeting_is(self):
        # Its body was empty on the phone ("Your morning" only): it says how many to-dos wait, the first two, and the
        # first meeting's time, never the meeting's title; Careful keeps the count and the time; nothing waiting: calm.
        meeting = [{'at': '2026-10-12T10:00:00+00:00', 'title': 'Board call about the merger'}]
        line = lambda *args, **kw: notify.compose(*args, **kw)['push']['body']
        waiting = [{'title': 'Reply to Sam about Tuesday'}, {'title': 'Pay the invoice'}]
        self.assertEqual(line(meeting, [], [{'title': 'x'}], waiting=waiting, total=3), '3 to-dos: Reply to Sam about Tuesday, Pay the invoice, … · First meeting 10:00')
        self.assertEqual(line([], [], [{'title': 'x'}], waiting=waiting[:1], total=1), '1 to-do: Reply to Sam about Tuesday')
        self.assertEqual(line(meeting, [], [], waiting=[], total=0), 'Nothing waiting · First meeting 10:00')
        self.assertEqual(line([], [{'title': 'x'}], [], waiting=[], total=0), 'Nothing waiting. A calm start.')
        careful = line(meeting, [], [], show_text=False, waiting=waiting, total=2)
        self.assertEqual(careful, '2 to-dos waiting · First meeting 10:00')
        long = line(meeting, [], [], waiting=[{'title': 'Reply ' * 30}, {'title': 'Pay ' * 30}], total=9)
        self.assertLessEqual(len(long), notify.APP_BODY)
        self.assertNotIn('merger', line(meeting, [], [], waiting=waiting, total=2))
        self.assertNotIn('—', long)

    def test_a_waiting_pile_gets_its_digest_in_the_dashboards_order(self):
        # It was skipped every morning while 17-19 to-dos waited: no meetings, nothing due or new overnight. A pile that
        # waits now gets a digest with the first ones as the to-do list shows them (three, then "+N more"); truly
        # nothing stays quiet. Made-up data.
        top = [{'title': 'Reply to the landlord'}, {'title': 'Send the quote'}, {'title': 'Book the venue'}]
        pile = notify.compose([], [], [], 'https://m.example/', waiting=top[:2], total=18, top=top)
        self.assertEqual(pile['subject'], 'Your morning: 18 waiting')
        self.assertIn('Waiting for you\n• Reply to the landlord\n• Send the quote\n• Book the venue\n• +15 more', pile['text'])
        self.assertTrue(pile['push']['body'].startswith('18 to-dos: Reply to the landlord, Send the quote'))
        careful = notify.compose([], [], [], '', show_text=False, waiting=top[:2], total=18, top=top)
        self.assertNotIn('landlord', careful['text'] + careful['subject'] + careful['push']['body'])
        self.assertIn('18 waiting', careful['text'])
        self.assertIsNone(notify.compose([], [], [], waiting=[], total=0, top=[]))
        # the whole way: the order of tests/test_open_order_dashboard.mjs (overdue or due by tomorrow first, then newest
        # first; a deadline months away goes by its time)
        current = a.dt.datetime(2026, 11, 5, 10, 0, tzinfo=UTC)
        h = lambda n: (current - a.dt.timedelta(hours=n)).isoformat()
        day = lambda n: (current + a.dt.timedelta(days=n)).date().isoformat()
        cards = [('a', 'Send the venue the final count', h(24 * 13), day(-13)), ('b', 'Book the train for the offsite', h(24 * 9), None),
                 ('c', 'Reply to Sam about the pilot', h(2), None), ('d', 'Answer the supplier about pallets', h(24 * 3), day(90)),
                 ('e', 'Confirm the dentist', h(26), day(1)), ('h', 'Pick a date for the board call', h(24 * 6), None)]
        for key, title, created, due in cards:
            sid = self.card(key=key, title=title)
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET created_at=?,due=?,urgent=0 WHERE id=?', (created, due, sid))
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch_everywhere(a, 'recap_meetings', return_value=[]):
            digest = self.app.digest(current + a.dt.timedelta(days=2, hours=-1))  # two days on: nothing new overnight, nothing due today
        self.assertIn('Waiting for you\n• Confirm the dentist\n• Send the venue the final count\n• Reply to Sam about the pilot\n• +3 more', digest['text'])
        self.assertEqual(digest['subject'], 'Your morning: 6 waiting')
        self.assertIn('• +3 more\n\n6 ready · about 3 min\n', digest['text'])  # the To-dos header's line, at the default pace
        order = notify.open_order([{'id': k, 'title': t, 'created_at': c, 'due': d} for k, t, c, d in cards], current)
        self.assertEqual([r['id'] for r in order], ['e', 'a', 'c', 'd', 'h', 'b'])
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed'")
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch_everywhere(a, 'recap_meetings', return_value=[]):
            self.assertIsNone(self.app.digest(current))

    def test_ready_and_promises_due_today_lead_and_no_to_do_is_listed_twice(self):
        # The preview listed the same three to-dos under Overnight and Waiting for you, and the ready drafts and the
        # promises due today weren't among its first lines. Ready leads, then the promises due today; Overnight and
        # Waiting never repeat what came before, and "+N more" counts only the rest. The push says the same first.
        ready = [{'id': 'r1', 'title': 'Reply to Sam about the pilot'}, {'id': 'r2', 'title': 'Answer the supplier'}]
        new = [{'id': 'n1', 'title': 'Book the venue'}, {'id': 'r1', 'title': 'Reply to Sam about the pilot'}]
        top = ready + [{'id': 'n1', 'title': 'Book the venue'}, {'id': 'w1', 'title': 'Pay the invoice'}]
        out = notify.compose([], [], new, 'https://m.example/', total=5, top=top, ready=ready,
                             promised=[{'id': 'promise:1', 'title': 'Send the recap for Wren'}])
        self.assertTrue(out['text'].startswith('Ready for you\n• Reply to Sam about the pilot\n• Answer the supplier\n\n'
                                               'Promises due today\n• Send the recap for Wren\n\nOvernight\n• Book the venue\n\n'
                                               'Waiting for you\n• Pay the invoice\n• +1 more\n\n'), out['text'])
        self.assertEqual(out['subject'], 'Your morning: 2 ready · 1 promise due today · 1 new · 5 waiting')
        self.assertEqual(out['push']['body'], '2 ready · 1 promise due today · 5 to-dos: Reply to Sam about the pilot, Answer the supplier, …')
        # all of what waits is listed above: no Waiting part at all
        self.assertNotIn('Waiting for you', notify.compose([], [], new, total=3, top=top[:3], ready=ready)['text'])
        # a promise alone (its to-do not made yet) still gets a digest, without "Nothing waiting" after it
        alone = notify.compose([], [], [], total=0, top=[], promised=[{'title': 'Send the recap for Wren'}])
        self.assertEqual(alone['push']['body'], '1 promise due today')
        careful = notify.compose([], [], new, show_text=False, total=5, top=top, ready=ready)
        self.assertNotIn('Sam', careful['text'] + careful['subject'] + careful['push']['body'])
        self.assertTrue(careful['push']['body'].startswith('2 ready · '))

    def test_the_digest_finds_the_ready_ones_and_the_owners_promises_due_today(self):
        current = a.dt.datetime(2026, 11, 5, 8, 30, tzinfo=UTC)
        ready = self.card(key='a', title='Reply to Sam about the pilot')
        self.card(key='b', title='Book the venue')
        recap = self.card(key='c', title='Send Wren the pilot recap')
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (ready,))
            db.execute("UPDATE suggestions SET event_ids='[3]' WHERE id=?", (recap,))  # made from the promise's message
            for who, what, direction, due, event in (('Wren', 'send the pilot recap', 'mine', '2026-11-05', 3), ('Jonah', 'send the rate limits', 'mine', '2026-11-06', 1),
                                                     ('Mila', 'send the contract', 'theirs', '2026-11-05', 1)):
                db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) VALUES(?,?,?,?,?,?,'home','open',?,?)",
                           (direction, who, what, due, current.isoformat(), event, current.isoformat(), current.isoformat()))
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch_everywhere(a, 'recap_meetings', return_value=[]):
            digest = self.app.digest(current)
        self.assertTrue(digest['text'].startswith('Ready for you\n• Reply to Sam about the pilot\n\nPromises due today\n• Send the pilot recap for Wren\n\n'), digest['text'])
        self.assertEqual(digest['text'].count('Reply to Sam about the pilot'), 1)
        self.assertEqual(digest['text'].count('Book the venue'), 1)
        self.assertNotIn('Send Wren the pilot recap', digest['text'])  # the promise's own to-do: listed as the promise
        self.assertNotIn('rate limits', digest['text'])  # tomorrow's
        self.assertNotIn('contract', digest['text'])  # someone else's
        self.assertTrue(digest['push']['body'].startswith('1 ready · 1 promise due today · 3 to-dos: Reply to Sam about the pilot, Book the venue'), digest['push']['body'])

    def test_the_digest_goes_once_on_the_chosen_channels_and_the_preview_sends_nothing(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.card(title='Answer the school')
        self.config.update(telegram_owner='42', credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'telegram', 'on': True}, owner_dashboard=True)
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'email', 'on': True}, owner_dashboard=True)
        with patch_everywhere(a, 'push_node', side_effect=AssertionError('no push')), patch_everywhere(a, 'telegram_request', side_effect=AssertionError('no Telegram')):
            preview = self.app.action('notify_preview', {}, owner_dashboard=True)
        self.assertIn('Answer the school', preview['text'])
        morning = a.dt.datetime(2026, 10, 12, 8, 40, tzinfo=UTC)
        told, mailed = [], []
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch_everywhere(a, 'credential', return_value='token'), patch.object(self.app, 'digest', return_value=notify.compose([], [], [{'title': 'Answer the school'}])):
            went = self.app.digest_step(current=morning, push=self.sender, telegram_send=told.append,
                                        mail=lambda url, token, subject, text: mailed.append((url, token, subject)) or True)
            self.assertEqual(went, ['push', 'telegram', 'email'])
            self.assertIsNone(self.app.digest_step(current=morning + a.dt.timedelta(minutes=5), push=self.sender, telegram_send=told.append,
                                                   mail=lambda *x: self.fail('twice')))
        self.assertEqual(self.sent[0]['payload']['title'], 'Your morning')
        self.assertEqual(mailed, [('https://cp.example/api/fleet', 'token', 'Your morning: 1 new')])
        self.assertIn('Answer the school', told[0])

    def test_no_digest_when_there_is_nothing_or_it_is_turned_off(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        monday = a.dt.datetime(2026, 10, 12, 8, 40, tzinfo=UTC)
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch.object(self.app, 'digest', return_value=None):
            self.assertEqual(self.app.digest_step(current=monday, push=self.sender), [])
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'email', 'on': False}, owner_dashboard=True)
        with patch_everywhere(a, 'local_tz', return_value=UTC):
            self.assertIsNone(self.app.digest_step(current=monday + a.dt.timedelta(days=1), push=self.sender))
        self.assertEqual(self.sent, [])

    def test_mail_goes_to_the_control_plane_with_the_network_token(self):
        seen = []
        class Answer(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *x): return False
        def opener(request, timeout):
            seen.append(request)
            return Answer(b'{"sent": true}')
        self.assertTrue(notify.mail('https://cp.example/api/fleet', 'tok', 'S' * 500, 'Body', opener))
        self.assertEqual(seen[0].full_url, 'https://cp.example/api/fleet/notify-mail')
        self.assertEqual(seen[0].get_header('Authorization'), 'Bearer tok')
        self.assertEqual(len(json.loads(seen[0].data)['subject']), notify.MAIL_SUBJECT)
        self.assertFalse(notify.mail('', 'tok', 'S', 'B', opener))
        def broken(request, timeout): raise OSError('down')
        def refused(request, timeout): raise notify.urllib.error.HTTPError(request.full_url, 429, 'enough email for today', {}, None)
        with self.assertLogs(a.LOG, 'WARNING') as logs:
            self.assertFalse(notify.mail('https://cp.example/api/fleet', 'tok', 'S', 'B', broken))
            self.assertFalse(notify.mail('https://cp.example/api/fleet', 'tok', 'S', 'B', refused))
            self.assertFalse(notify.mail('https://cp.example/api/fleet', 'tok', 'S', 'B', lambda request, timeout: Answer(b'{}')))
        # a failed send is in the log with its reason, never the token or the text
        self.assertEqual([line.split(':', 2)[2] for line in logs.output], ['notify mail error=OSError', 'notify mail status=429', 'notify mail not taken'])


class DurableQueue(Notifications):
    def test_failed_delivery_survives_restart_and_keeps_its_batch(self):
        clock = [10000.0]
        at = lambda: clock[0]
        with self.store.connect() as db:
            notify.hold(db, 'email', 'todo', 'Original', 1, clock=at)
            _, first = notify.take_due(db, clock=at)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM notify_queue').fetchone()[0], 1)
            self.assertEqual(notify.take_due(db, clock=at)[1], [])  # claimed, not lost
        clock[0] += 61
        with self.store.connect() as db:
            notify.hold(db, 'email', 'todo', 'New', 1, clock=at)
            _, retry = notify.take_due(db, clock=at)
            self.assertEqual(retry, first)  # new mail cannot change the retry's body or key
            notify.delivered(db, retry)
            self.assertEqual(db.execute('SELECT title FROM notify_queue').fetchone()[0], 'New')


class OwnTables(unittest.TestCase):
    """notify.py writes its own tables (the digest of each day, the held pushes); assistant.py calls it."""
    def test_digest_once_a_day_and_held_pushes_dropped(self):
        import sqlite3
        db = sqlite3.connect(':memory:', isolation_level=None)
        notify.ensure(db)
        self.assertFalse(notify.digest_sent(db, '2026-11-02'))
        self.assertTrue(notify.digest_claim(db, '2026-11-02', 'at'))
        db.execute('COMMIT')
        self.assertTrue(notify.digest_sent(db, '2026-11-02'))
        self.assertFalse(notify.digest_claim(db, '2026-11-02', 'later'))
        db.execute('ROLLBACK')
        notify.digest_done(db, '2026-11-02', 'sent', ['push', 'email'])
        self.assertEqual(db.execute('SELECT status,channels,created_at FROM notify_digests').fetchall(), [('sent', '["push","email"]', 'at')])
        notify.hold(db, 'push', 'todo', 'A', 0, clock=lambda: 0)
        notify.hold(db, 'email', 'todo', 'A', 0, clock=lambda: 0)
        notify.drop_pushes(db)
        self.assertEqual(db.execute('SELECT channel FROM notify_queue').fetchall(), [('email',)])


if __name__ == '__main__':
    unittest.main()

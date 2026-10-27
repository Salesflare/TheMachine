"""Notifications (notify.py): per kind and channel, quiet while the owner is at the dashboard, and the morning digest.
Every send here is a fake: no push service, Telegram or mail server is reached."""
import io, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import assistant as a
import notify

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
        with patch.object(notify.time, 'time', return_value=clock), patch.object(a, 'local_tz', return_value=UTC), \
                patch.object(a, 'credential', return_value='token'):
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
        self.assertEqual(self.step(t0 + 60 + notify.EMAIL_AFTER), [])
        self.assertEqual((self.sent, self.mails), ([], []))

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
        self.assertEqual(self.step(t0 + notify.EMAIL_AFTER - 1), [])
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
        with patch.object(a, 'WORK_HOURS', dict(a.WORK_HOURS_DEFAULT, end='18:00')):
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
        with patch.object(a, 'fleet_telegram', return_value={}), patch.object(a.fleet, 'telegram_message', return_value={}), \
                patch.object(notify.time, 'time', return_value=later):
            self.app.fleet_notify([self.handoff('q_' + 'e' * 16)])
        del self.config['telegram_owner']
        # A phone reaches them: no email either
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        with patch.object(a, 'push_send', return_value=[]), patch.object(notify.time, 'time', return_value=later):
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
        with patch.object(a.dt, 'datetime', Daytime), patch.object(a, 'telegram', side_effect=AssertionError('no Telegram')), \
                patch.object(a, 'push_notify') as push:
            self.assertTrue(a.deliver_one(self.store, config, edit_cards=False))
        self.assertEqual([c.args[2]['id'] for c in push.call_args_list], [sid])
        with self.store.connect() as db:
            message = db.execute('SELECT message_id FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0]
        self.assertTrue(message.startswith('web-'))
        # Its later edits and result notices never go to Telegram for a card that isn't there.
        with patch.object(a.subprocess, 'run', side_effect=AssertionError('no Telegram helper')):
            self.assertEqual(a.telegram_request(config, {'action': 'edit', 'messageId': message}), {'messageId': message})
        with patch.object(a, 'telegram_request', side_effect=lambda config, args: args) as request:
            args = a.telegram(dict(config), {'id': sid, 'title': 'T', 'status': 'prepared', 'message_id': message, '_result_notice': True}, 'send')
        self.assertNotIn('replyTo', args)

    def test_at_the_dashboard_telegram_arrives_silently(self):
        self.card()
        self.app.action('notify_active', {}, owner_dashboard=True)
        seen = []
        with patch.object(a.dt, 'datetime', Daytime), patch.object(a, 'telegram', side_effect=lambda c, row, action: seen.append(row) or {'messageId': '7'}), \
                patch.object(a, 'push_notify'):
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
        self.assertEqual(full['push']['body'], 'First: 09:30 Planning with the agency. 1 meeting · 1 due · 5 new')
        self.assertIn('• Pay the invoice', full['text'])
        self.assertIn('• +2 more', full['text'])
        self.assertTrue(full['text'].endswith('Open The Machine: https://m.example/'))
        careful = notify.compose(meetings, [], overnight, '', show_text=False)
        self.assertEqual(careful['push']['body'], '1 meeting · 5 new')
        self.assertNotIn('agency', careful['text'] + careful['subject'])

    def test_the_digest_goes_once_on_the_chosen_channels_and_the_preview_sends_nothing(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.card(title='Answer the school')
        self.config.update(telegram_owner='42', credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'telegram', 'on': True}, owner_dashboard=True)
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'email', 'on': True}, owner_dashboard=True)
        with patch.object(a, 'push_node', side_effect=AssertionError('no push')), patch.object(a, 'telegram_request', side_effect=AssertionError('no Telegram')):
            preview = self.app.action('notify_preview', {}, owner_dashboard=True)
        self.assertIn('Answer the school', preview['text'])
        morning = a.dt.datetime(2026, 10, 12, 8, 40, tzinfo=UTC)
        told, mailed = [], []
        with patch.object(a, 'local_tz', return_value=UTC), patch.object(a, 'credential', return_value='token'), patch.object(self.app, 'digest', return_value=notify.compose([], [], [{'title': 'Answer the school'}])):
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
        with patch.object(a, 'local_tz', return_value=UTC), patch.object(self.app, 'digest', return_value=None):
            self.assertEqual(self.app.digest_step(current=monday, push=self.sender), [])
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.app.action('notify_set', {'kind': 'digest', 'channel': 'email', 'on': False}, owner_dashboard=True)
        with patch.object(a, 'local_tz', return_value=UTC):
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
        self.assertFalse(notify.mail('https://cp.example/api/fleet', 'tok', 'S', 'B', broken))


if __name__ == '__main__':
    unittest.main()

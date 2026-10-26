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

    def test_defaults_keep_todays_behavior_and_each_cell_saves(self):
        view = self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': False}, owner_dashboard=True)
        self.assertEqual(view['prefs']['todo'], {'push': False, 'telegram': True})
        self.assertEqual(view['prefs']['digest'], {'push': True, 'telegram': False, 'email': False})
        self.assertEqual(view['prefs']['result'], {'push': True, 'telegram': True})
        for bad in ({'kind': 'todo', 'channel': 'email'}, {'kind': 'spam', 'channel': 'push'}):
            with self.assertRaises(ValueError):
                self.app.action('notify_set', {**bad, 'on': True}, owner_dashboard=True)
        with self.assertRaises(ValueError):  # only the owner, on the dashboard
            self.app.action('notify_set', {'kind': 'todo', 'channel': 'push', 'on': True})

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

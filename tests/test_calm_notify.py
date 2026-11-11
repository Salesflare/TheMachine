"""Calm notifications: only what can't wait buzzes (due today, a reply someone waits for, a sign-in, urgent, a snooze
coming back); the rest waits for the morning summary. No buzz on days off unless urgent, at most PUSH_CAP pushes a
day, and summary only after AWAY_DAYS without a visit. Made-up data; every send here is a fake."""
import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import assistant as a
import locale_prefs
import notify
from machine.delivery import deliver
from seams import patch_everywhere  # noqa: E402

UTC = a.dt.timezone.utc
DAY = '2026-10-12'


class Daytime(a.dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 12, 10, 0, tzinfo=tz or UTC)  # a Monday, within hours


class Sunday(a.dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 11, 10, 0, tzinfo=tz or UTC)


class Calm(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        self.clock = [1_800_000_000.0]

    def card(self, key='one', title='Book the venue', **extra):
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': key, 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        sid = self.store.suggest(key, title, 'Body', [1], **extra)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        return sid

    def reason(self, why, work_day=True):
        with self.store.connect() as db:
            return notify.calm_reason(db, why, work_day, DAY, lambda: self.clock[0])

    def test_what_cannot_wait(self):
        today = DAY
        self.assertEqual(deliver.why_now({'urgent': 1}, today), 'urgent')
        self.assertEqual(deliver.why_now({'due': '2026-10-12'}, today), 'due')
        self.assertEqual(deliver.why_now({'due': '2026-10-01T09:00'}, today), 'due')  # overdue too
        self.assertEqual(deliver.why_now({'due': '2026-10-13'}, today), '')  # tomorrow can wait
        self.assertEqual(deliver.why_now({'preparation_browser': {'signin_url': 'https://shop.example/login'}}, today), 'signin')
        self.assertEqual(deliver.why_now({'id': 'x', 'status': 'pending', 'reminder': 1}, today), 'reminder')
        self.assertEqual(deliver.why_now({'id': 'x', 'status': 'pending'}, today), '')

    def test_quiet_reasons_in_order(self):
        self.assertEqual(self.reason(''), 'later')
        self.assertEqual(self.reason('reply', work_day=False), 'day_off')
        self.assertEqual(self.reason('urgent', work_day=False), '')  # urgent buzzes on a day off
        self.assertEqual(self.reason('reply'), '')
        with self.store.connect() as db:
            for _ in range(notify.PUSH_CAP):
                notify.count_push(db, DAY)
            self.assertEqual(notify.pushed_today(db, DAY), notify.PUSH_CAP)
            self.assertEqual(notify.pushed_today(db, '2026-10-13'), 0)  # a new day starts at zero
        self.assertEqual(self.reason('urgent'), 'cap')

    def test_away_starts_counting_when_it_arrives_and_a_visit_or_decision_resets_it(self):
        self.assertEqual(self.reason('urgent'), '')  # no visit kept yet: the count starts now, nobody goes quiet today
        self.clock[0] += notify.AWAY_DAYS * 86400 + 60
        self.assertEqual(self.reason('urgent'), 'away')
        with self.store.connect() as db:
            notify.visited(db, lambda: self.clock[0])
        self.assertEqual(self.reason('urgent'), '')
        self.clock[0] += notify.AWAY_DAYS * 86400 + 60
        sid = self.card()
        at = a.dt.datetime.fromtimestamp(self.clock[0] - 3600, UTC).isoformat()
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1',?,'accept','','telegram',?)", (sid, at))
        self.assertEqual(self.reason('urgent'), '')  # a Telegram answer counts as being here

    def deliver(self, now=Daytime, config=None):
        fake = patch_everywhere(a, 'telegram', side_effect=lambda c, row, action: self.told.append(row) or {'messageId': '7'}) if config is None \
            else patch.object(a.subprocess, 'run', side_effect=AssertionError('no Telegram helper'))
        with patch.object(a.dt, 'datetime', now), fake, patch_everywhere(a, 'push_notify') as push, patch_everywhere(a, 'hold_mail') as mail:
            self.assertTrue(a.deliver_one(self.store, config or dict(self.config, telegram_owner='42'), edit_cards=False))
        return push, mail

    def test_a_to_do_that_can_wait_arrives_quietly_and_writes_its_line(self):
        self.told = []
        sid = self.card()
        with self.assertLogs(a.LOG, 'INFO') as logs:
            push, mail = self.deliver()
        self.assertEqual((push.call_count, mail.call_count), (0, 0))
        self.assertTrue(self.told[0]['_silent'])
        self.assertTrue(any('quiet=later' in line for line in logs.output), logs.output)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0], 'sent')

    def test_due_today_buzzes_also_on_a_day_off_and_what_can_wait_stays_quiet_then(self):
        self.told = []
        self.card(due=DAY)
        push, mail = self.deliver()
        self.assertEqual((push.call_count, mail.call_count), (1, 1))
        self.assertFalse(self.told[0]['_silent'])
        self.told = []
        self.card(key='two', title='Pay the invoice', due='2026-10-11')
        push, mail = self.deliver(Sunday)
        self.assertEqual((push.call_count, mail.call_count), (1, 1))
        self.told = []
        self.card(key='three', title='Book the train')
        push, mail = self.deliver(Sunday)
        self.assertEqual((push.call_count, mail.call_count), (0, 0))
        self.assertEqual(self.told[0]['_calm'], 'later')

    def prepared_before_its_first_delivery(self, **extra):
        sid = self.card(**extra)
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',early=1 WHERE id=?", (sid,))  # prepared ahead, by itself
            db.execute("UPDATE deliveries SET status='queued',reminder=1,message_id=NULL WHERE suggestion_id=?", (sid,))
        return sid

    def test_a_work_to_do_prepared_before_its_first_delivery_waits_for_a_work_day(self):
        # The reminder flag a preparation sets let a never-delivered to-do skip the day-off hold: a weekend ping.
        # (A to-do the owner accepted themselves keeps going at once: tests/test_preparation.py.)
        sid = self.prepared_before_its_first_delivery()
        config = dict(self.config, telegram_owner='42', accounts=[{'id': 'home', 'boundary': 'work:example'}])
        with patch.object(a.dt, 'datetime', Sunday), patch_everywhere(a, 'telegram', side_effect=AssertionError('no Telegram on a day off')), \
                patch_everywhere(a, 'push_notify', side_effect=AssertionError('no push')):
            self.assertFalse(a.deliver_one(self.store, config, edit_cards=False))
        with self.store.connect() as db:
            self.assertTrue(db.execute('SELECT deliver_after FROM suggestions WHERE id=?', (sid,)).fetchone()[0].startswith('2026-10-12'))

    def test_a_to_do_prepared_before_its_first_delivery_keeps_its_send_time(self):
        later = self.prepared_before_its_first_delivery()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET deliver_after='2026-10-12T15:00:00+00:00' WHERE id=?", (later,))
        with patch.object(a.dt, 'datetime', Daytime), patch_everywhere(a, 'now', return_value='2026-10-12T10:00:00+00:00'), \
                patch_everywhere(a, 'telegram', side_effect=AssertionError('not yet')):
            self.assertFalse(a.deliver_one(self.store, dict(self.config, telegram_owner='42'), edit_cards=False))

    def test_a_quiet_delivery_never_silences_the_next_one_that_cannot_wait(self):
        self.told = []
        self.card()
        self.deliver()
        self.card(key='two', title='Pay the invoice', urgent=True)
        push, _ = self.deliver()
        self.assertEqual(push.call_count, 1)
        self.assertFalse(self.told[1]['_silent'])

    def test_without_telegram_a_calm_to_do_still_reaches_the_dashboard(self):
        self.told = []
        sid = self.card()
        push, _ = self.deliver(config=dict(self.config, telegram_owner=''))
        self.assertEqual(push.call_count, 0)
        with self.store.connect() as db:
            self.assertTrue(db.execute('SELECT message_id FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone()[0].startswith('web-'))

    def test_a_buzzing_push_counts_toward_the_cap_and_a_silent_one_does_not(self):
        sent = []
        sender = lambda request: sent.append(request) or {'results': []}
        sub = [{'endpoint': 'https://push.example/abc', 'p256dh': 'p', 'auth': 'x'}]
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch.object(a.dt, 'datetime', Daytime):
            a.push_send(self.store, self.config, sub, {'title': 'T'}, 'todo', sender, kind='todo')
            a.push_send(self.store, self.config, sub, {'title': 'T', 'silent': True}, 'todo', sender, kind='todo')
        with self.store.connect() as db:
            self.assertEqual(notify.pushed_today(db, DAY), 1)


class Summary(unittest.TestCase):
    def tearDown(self):
        locale_prefs.configure({})

    def test_a_pile_names_itself_and_the_time_to_clear_it(self):
        top = [{'title': f'Answer the supplier {n}'} for n in range(12)]
        out = notify.compose([], [], [], 'https://m.example/', total=12, top=top, per=25, name='Robin')
        self.assertEqual(out['subject'], 'Morning Robin, 12 waiting, about 5 min to clear')
        self.assertEqual(out['text'].count('\n• '), 3)
        self.assertIn('\n\n9 more can wait, about 4 min to clear.\n\n', out['text'])

    def test_the_example_reads_short_in_english_and_dutch(self):
        ready = [{'id': 'a1b2c3d4e5f60718', 'title': 'Send the reply to Robin'}, {'id': 'b1b2c3d4e5f60718', 'title': 'Send the reply to Kai'}]
        meeting = [{'at': '2026-10-12T10:00:00+00:00', 'title': 'Planning'}]
        top = ready + [{'title': f'To-do {n}'} for n in range(12)]
        args = dict(total=14, top=top, ready=ready, replies=[r['id'] for r in ready], per=25, name='Sam')
        en = notify.compose(meeting, [], [], 'https://m.example/', **args)
        self.assertEqual(en['text'].split('\n')[:9], ['Morning Sam, 2 replies are ready to send', '',
                                                     '• Send the reply to Robin · [Open](https://m.example/#chat=a1b2c3d4e5f60718)',
                                                     '• Send the reply to Kai · [Open](https://m.example/#chat=b1b2c3d4e5f60718)',
                                                     '• 10:00 Planning', '', '12 more can wait, about 5 min to clear.', '',
                                                     '1 meeting today, at 10:00.'])
        locale_prefs.configure({'language': 'nl'})
        nl = notify.compose(meeting, [], [], 'https://m.example/', **args)
        self.assertEqual(nl['push']['title'], 'Goeiemorgen Sam, 2 antwoorden staan klaar om te versturen')
        self.assertEqual(nl['push']['body'], 'Send the reply to Robin\nSend the reply to Kai\nEerste afspraak om 10:00\n12 andere kunnen wachten, ongeveer 5 min werk.')


if __name__ == '__main__':
    unittest.main()

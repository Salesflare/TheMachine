"""The evening digest (notify.evening_time, notify.evening_due, notify.evening_compose, App.evening_digest and
App.evening_step): at its time (by default 15 minutes before the end of the work hours) on a work day, in the owner's
time zone, at most once a day and never twice after a restart, on the channels picked for it; what got done today and
what's open for the next work day; nothing on a day without anything done or held.
Every send here is a fake: no push service, Telegram or mail server is reached."""
import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import assistant as a
import locale_prefs
import notify
from seams import patch_everywhere  # noqa: E402

UTC = a.dt.timezone.utc
BXL = ZoneInfo('Europe/Brussels')
SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}
work_day = lambda day: day.isoweekday() <= 5


def at(day, h, m=0, tz=BXL):
    return a.dt.datetime(2026, 11, day, h, m, tzinfo=tz)  # 2026-11-12 is a Thursday, the 13th a Friday


class When(unittest.TestCase):
    def due(self, local, start='08:00', end='18:00', sent=(), own=None):
        return notify.evening_due(local, notify.evening_time(own, start, end), start, end, work_day, lambda day: day in sent)

    def test_its_time_15_minutes_before_until_unless_set(self):
        self.assertEqual(notify.evening_time(None, '08:00', '18:00'), '17:45')
        self.assertEqual(notify.evening_time(None, '20:00', '00:10'), '23:55')
        self.assertEqual(notify.evening_time('16:30', '08:00', '18:00'), '16:30')

    def test_a_quarter_of_an_hour_before_the_end_of_the_hours_on_a_work_day(self):
        self.assertIsNone(self.due(at(12, 17, 44)))
        self.assertEqual(self.due(at(12, 17, 45)), a.dt.date(2026, 11, 12))
        self.assertEqual(self.due(at(12, 17, 59)), a.dt.date(2026, 11, 12))
        self.assertIsNone(self.due(at(12, 18, 0)))  # the hours ended: nothing goes outside them
        self.assertIsNone(self.due(at(14, 17, 50)))  # a Saturday
        self.assertIsNone(self.due(at(12, 17, 50), sent={'2026-11-12'}))  # once a day
        self.assertEqual(self.due(at(13, 17, 50), sent={'2026-11-12'}), a.dt.date(2026, 11, 13))  # the next day is its own

    def test_a_time_of_its_own(self):
        self.assertIsNone(self.due(at(12, 16, 29), own='16:30'))
        self.assertEqual(self.due(at(12, 16, 30), own='16:30'), a.dt.date(2026, 11, 12))
        self.assertEqual(self.due(at(12, 17, 50), own='16:30'), a.dt.date(2026, 11, 12))  # the Machine was off: later that day
        self.assertIsNone(self.due(at(12, 18, 30), own='16:30'))  # never outside the hours
        self.assertIsNone(self.due(at(12, 7, 0), own='06:00'))  # a time before the hours waits for them: none that day

    def test_in_the_owners_time_zone(self):
        # 17:50 in Brussels is 16:50 UTC: the same moment read in UTC is before its time, in Brussels it is due
        moment = at(12, 16, 50, UTC)
        self.assertIsNone(self.due(moment))
        self.assertEqual(self.due(moment.astimezone(BXL)), a.dt.date(2026, 11, 12))
        # New York's 17:45 is 23:45 in Brussels
        self.assertEqual(self.due(at(12, 17, 45, ZoneInfo('America/New_York'))), a.dt.date(2026, 11, 12))

    def test_hours_past_midnight_and_round_the_clock(self):
        # Thursday 20:00 to 02:00: its evening is Friday 01:45, still Thursday's work day
        self.assertEqual(self.due(at(13, 1, 50), start='20:00', end='02:00'), a.dt.date(2026, 11, 12))
        self.assertIsNone(self.due(at(15, 1, 50), start='20:00', end='02:00'))  # Saturday night's belongs to the Saturday
        self.assertEqual(self.due(at(12, 7, 50), start='08:00', end='08:00'), a.dt.date(2026, 11, 12))  # round the clock


class Compose(unittest.TestCase):
    DONE = [{'id': 'a1b2c3d4e5f60718', 'title': 'Send the order form', 'area': 'work'},
            {'id': 'b1b2c3d4e5f60718', 'title': 'Reply to the supplier', 'area': 'work'},
            {'id': 'c1b2c3d4e5f60718', 'title': 'Book the dentist', 'area': 'personal'},
            {'id': 'd1b2c3d4e5f60718', 'title': 'Pay the invoice', 'area': 'work'},
            {'id': 'f1b2c3d4e5f60718', 'title': 'File the expenses', 'area': 'work'}]
    HELD = [{'at': '2026-11-12T09:00:00+00:00', 'title': 'Standup', 'named': False, 'area': 'work'},
            {'at': '2026-11-12T14:00:00+00:00', 'title': 'Pricing call', 'named': True, 'area': 'work'}]
    AHEAD = [{'at': '2026-11-13T10:00:00+00:00', 'title': 'Roadmap review', 'area': 'work'}]
    DUE = [{'id': 'e1b2c3d4e5f60718', 'title': 'Send the signed contract', 'area': 'work'},
           {'id': None, 'title': 'Pick up the parcel', 'area': 'personal'}]

    def test_a_day_without_anything_says_nothing(self):
        self.assertIsNone(notify.evening_compose([], [], 5, self.DUE, self.AHEAD, 'https://m.example/'))

    def test_work_and_personal_each_with_done_and_open_for_tomorrow(self):
        out = notify.evening_compose(self.DONE, self.HELD, 6, self.DUE, self.AHEAD, 'https://m.example/', name='Robin')
        self.assertEqual(out['subject'], 'Evening Robin, 5 to-dos done today')
        self.assertEqual(out['text'],
                         'Evening Robin, 5 to-dos done today\n\n'
                         'Work\nDone today\n• Send the order form\n• Reply to the supplier\n• Pay the invoice\n1 more done.\n'
                         '2 meetings: Pricing call and 1 more.\n'
                         'Open for tomorrow\n• 10:00 Roadmap review\n'
                         '• Due: Send the signed contract · [Open](https://m.example/#card=e1b2c3d4e5f60718&or=chat)\n\n'
                         'Personal\nDone today\n• Book the dentist\nOpen for tomorrow\n• Due: Pick up the parcel\n\n'
                         '6 to-dos still need you.\n\n'
                         'Open The Machine: https://m.example/')
        # each part copies on its own, as plain text: every to-do done, no links
        self.assertEqual(out['sections'], [
            {'area': 'work', 'copy': 'Done today\n• Send the order form\n• Reply to the supplier\n• Pay the invoice\n• File the expenses\n'
                                     '2 meetings: Pricing call and 1 more.\nOpen for tomorrow\n• 10:00 Roadmap review\n• Due: Send the signed contract'},
            {'area': 'personal', 'copy': 'Done today\n• Book the dentist\nOpen for tomorrow\n• Due: Pick up the parcel'}])
        self.assertEqual(out['push'], {'title': 'Evening Robin, 5 to-dos done today',
                                       'body': 'Done: Send the order form, Reply to the supplier and 3 more\nTomorrow, first meeting at 10:00',
                                       'url': 'https://m.example/#todos', 'tag': 'evening'})
        self.assertLessEqual(len(out['push']['body']), notify.APP_BODY)
        self.assertNotIn('—', out['text'])
        self.assertFalse(any(line.startswith('You') for line in out['text'].split('\n')))

    def test_an_empty_part_is_left_out(self):
        work = notify.evening_compose(self.DONE[:1], [], 0, [], [])
        self.assertEqual(work['text'], 'Good evening, 1 to-do done today\n\nWork\nDone today\n• Send the order form')
        self.assertEqual([s['area'] for s in work['sections']], ['work'])
        personal = notify.evening_compose([{'id': 'x', 'title': 'Call the plumber', 'area': 'personal'}], [], 0, [], [])
        self.assertNotIn('Work', personal['text'])
        self.assertEqual(personal['sections'], [{'area': 'personal', 'copy': 'Done today\n• Call the plumber'}])

    def test_a_long_title_keeps_the_count_in_the_push(self):
        long = [{'id': 'x', 'title': 'Send the signed contract to the new supplier', 'area': 'work'},
                {'id': 'y', 'title': 'Answer the pricing question from the reseller', 'area': 'work'}, *self.DONE[:3]]
        body = notify.evening_compose(long, [], 0, [], self.AHEAD)['push']['body']
        self.assertTrue(body.split('\n')[0].endswith('and 4 more'), body)

    def test_meetings_alone_a_friday_and_careful(self):
        friday = notify.evening_compose([], self.HELD, 0, self.DUE[:1], [], tomorrow=False, next_day='Mon, Nov 16')
        self.assertEqual(friday['subject'], 'Good evening, 2 meetings today')
        self.assertIn('\nOpen for Mon, Nov 16\n', friday['text'])
        self.assertEqual(friday['push']['body'], '2 meetings.\n1 due on Mon, Nov 16')
        careful = notify.evening_compose(self.DONE, self.HELD, 3, self.DUE, self.AHEAD, '', show_text=False)
        for title in ('order form', 'dentist', 'Pricing call', 'Roadmap', 'contract', 'parcel'):
            self.assertNotIn(title, careful['text'] + careful['push']['body'] + str(careful['sections']))
        self.assertIn('Work\nDone today\n4 to-dos done.\n2 meetings.\nOpen for tomorrow\nTomorrow, first meeting at 10:00.\n1 due tomorrow.',
                      careful['text'])
        self.assertIn('Personal\nDone today\n1 to-do done.\nOpen for tomorrow\n1 due tomorrow.\n\n3 to-dos still need you.', careful['text'])

    def test_in_the_owners_language(self):
        with patch.object(locale_prefs, 'language', return_value='nl'):
            out = notify.evening_compose(self.DONE[:1], [], 0, [], [], name='Robin')
        self.assertEqual(out['subject'], 'Goeienavond Robin, vandaag 1 to-do gedaan')
        self.assertIn('\nWerk\n', out['text'])


class Step(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [{'id': 'home', 'boundary': 'personal:me'}, {'id': 'office', 'boundary': 'work:Acme'}], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        a.set_work_hours({'start': '08:00', 'end': '18:00'}); self.addCleanup(a.set_work_hours, None)
        self.sent = []
        self.sender = lambda request: self.sent.append(request) or {'results': [{'endpoint': SUB['endpoint'], 'status': 201}]}
        self.n = 0

    def card(self, title, account='office', **extra):
        self.n += 1
        self.store.commit_page(account, {}, [{'account_id': account, 'source_id': f'm{self.n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        sid = self.store.suggest(f'k{self.n}', title, 'Body', [self.n], **extra)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        return sid

    def done(self, sid, when, choice='complete', source='dashboard'):
        with self.store.connect() as db:
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       ('d-' + sid, sid, choice, '', source, when.astimezone(UTC).isoformat()))
            db.execute("UPDATE suggestions SET status='completed',closed_decision_id=? WHERE id=?", ('d-' + sid, sid))

    def meetings(self, db, start, end, cards, routine=False):
        found = [{'at': at(12, 9, 0).astimezone(UTC).isoformat(), 'title': 'Standup', 'guests': 4, 'card': None, 'routine': True, 'account': 'office'},
                 {'at': at(12, 14, 0).astimezone(UTC).isoformat(), 'title': 'Pricing call', 'guests': 2, 'card': None, 'account': 'office'},
                 {'at': at(13, 10, 0).astimezone(UTC).isoformat(), 'title': 'Roadmap review', 'guests': 3, 'card': None, 'account': 'office'}]
        return [m for m in found if start <= m['at'] < end and (routine or not m.get('routine'))]

    def test_done_today_by_the_owner_or_the_machine_and_whats_due_tomorrow(self):
        evening = at(12, 17, 45)
        self.done(self.card('Send the order form'), at(12, 10, 0))
        self.done(self.card('Close the follow-up'), at(12, 11, 0), source='assistant')  # by The Machine
        self.done(self.card('Book the venue'), at(11, 16, 0))  # yesterday
        self.done(self.card('Merged away'), at(12, 12, 0), choice='merge')
        self.card('Send the signed contract', due='2026-11-13')
        self.done(self.card('Book the dentist', account='home'), at(12, 13, 0))
        self.card('Answer the school', account='home')
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', side_effect=self.meetings):
            out = self.app.evening_digest(evening.astimezone(UTC))
        self.assertTrue(out['text'].startswith('Good evening, 3 to-dos done today\n\nWork\nDone today\n'), out['text'])
        self.assertIn('\n\nPersonal\nDone today\n• Book the dentist\n', out['text'])  # a to-do on a personal account
        self.assertEqual([x['area'] for x in out['sections']], ['work', 'personal'])
        self.assertIn('• Send the order form', out['text'])
        self.assertIn('• Close the follow-up', out['text'])
        self.assertNotIn('Book the venue', out['text'])
        self.assertNotIn('Merged away', out['text'])
        self.assertIn('2 meetings: Pricing call and 1 more.', out['text'])  # the standup counted, not named
        self.assertIn('Open for tomorrow\n• 10:00 Roadmap review\n• Due: Send the signed contract', out['text'])
        self.assertIn('2 to-dos still need you.', out['text'])

    def test_once_a_day_on_its_channels_and_never_twice_after_a_restart(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        mailed = []
        mail = lambda url, token, subject, text: mailed.append(subject) or True
        self.config.update(credentials={'fleet': 'fleet'}, fleet={'url': 'https://cp.example/api/fleet'})
        self.done(self.card('Send the order form'), at(12, 10, 0))
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'credential', return_value='token'), \
                patch_everywhere(a, 'recap_meetings', return_value=[]):
            self.assertIsNone(self.app.evening_step(at(12, 17, 30).astimezone(UTC), push=self.sender, mail=mail))  # not yet
            self.assertEqual(self.app.evening_step(at(12, 17, 46).astimezone(UTC), push=self.sender, mail=mail), ['push', 'email'])
            # a restart: a new App on the same database finds the day taken
            again = object.__new__(a.App); again.store = a.Store(self.store.path); again.config = self.config
            self.assertIsNone(again.evening_step(at(12, 17, 50).astimezone(UTC), push=self.sender, mail=lambda *x: self.fail('twice')))
        self.assertEqual(self.sent[0]['payload']['title'], 'Good evening, 1 to-do done today')
        self.assertEqual(self.sent[0]['payload']['tag'], 'evening')
        self.assertEqual(mailed, ['Good evening, 1 to-do done today'])
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT day,status FROM notify_digests')], [('evening:2026-11-12', 'sent')])

    def test_a_day_with_nothing_a_day_off_and_every_channel_off_send_nothing(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.card('Answer the school')  # waiting, but nothing done today
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', return_value=[]):
            self.assertEqual(self.app.evening_step(at(12, 17, 50).astimezone(UTC), push=self.sender), [])
            self.assertIsNone(self.app.evening_step(at(14, 17, 50).astimezone(UTC), push=self.sender))  # Saturday
            self.done(self.card('Send the order form'), at(13, 10, 0))
            with self.store.connect() as db:  # its own row in Notifications, apart from the morning's
                for channel in ('push', 'email'):
                    notify.set_pref(db, 'evening', channel, False)
                self.assertTrue(notify.prefs(db)['digest']['push'])
            self.assertIsNone(self.app.evening_step(at(13, 17, 50).astimezone(UTC), push=self.sender))
        self.assertEqual(self.sent, [])
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT day,status FROM notify_digests')], [('evening:2026-11-12', 'empty')])

    def test_at_a_time_of_its_own(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.config['evening_at'] = '16:00'
        self.done(self.card('Send the order form'), at(12, 10, 0))
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', return_value=[]):
            self.assertIsNone(self.app.evening_step(at(12, 15, 59).astimezone(UTC), push=self.sender))
            self.assertEqual(self.app.evening_step(at(12, 16, 0).astimezone(UTC), push=self.sender), ['push'])


if __name__ == '__main__':
    unittest.main()

"""A digest opens again from its notification and its email's link (notify.DIGEST_VIEW, EVENING_VIEW): a sent morning or
evening digest keeps what it said (notify.digest_done, digest_kept) for DIGEST_KEEP, and the digest_sent action gives the
last one of a kind to the owner's own dashboard (tests/test_push_links_dashboard.mjs opens it there).
Every send here is a fake: no push service or mail server is reached."""
import tempfile, unittest
from pathlib import Path
from zoneinfo import ZoneInfo
import assistant as a
import notify
from seams import patch_everywhere  # noqa: E402

UTC = a.dt.timezone.utc
BXL = ZoneInfo('Europe/Brussels')
SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}


class Reopen(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'home', 'boundary': 'personal:me'}, {'id': 'office', 'boundary': 'work:Acme'}],
                           'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        a.set_work_hours({'start': '08:00', 'end': '18:00'}); self.addCleanup(a.set_work_hours, None)
        self.sent = []
        self.sender = lambda request: self.sent.append(request) or {'results': [{'endpoint': SUB['endpoint'], 'status': 201}]}

    def done_card(self, title, account, when):
        self.store.commit_page(account, {}, [{'account_id': account, 'source_id': 'm-' + title, 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        with self.store.connect() as db:
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
        sid = self.store.suggest('k-' + title, title, 'Body', [event])['id']
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'complete','','dashboard',?)",
                       ('d-' + sid, sid, when.astimezone(UTC).isoformat()))
            db.execute("UPDATE suggestions SET status='completed',closed_decision_id=?,deliver_after=NULL WHERE id=?", ('d-' + sid, sid))

    def shown(self, kind):
        return self.app.action('digest_sent', {'kind': kind}, owner_dashboard=True)

    def test_the_evening_push_and_email_open_that_digest_as_it_went(self):
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.done_card('Send the order form', 'office', a.dt.datetime(2026, 11, 12, 10, tzinfo=BXL))
        self.done_card('Book the dentist', 'home', a.dt.datetime(2026, 11, 12, 12, tzinfo=BXL))
        self.assertEqual(self.shown('evening'), {})  # none sent yet: the dashboard shows today's digest instead
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', return_value=[]):
            self.assertEqual(self.app.evening_step(a.dt.datetime(2026, 11, 12, 17, 46, tzinfo=BXL).astimezone(UTC), push=self.sender), ['push'])
        self.assertEqual(self.sent[0]['payload']['url'], 'https://the-machine.example/assistant/#digest=evening')
        got = self.shown('evening')
        self.assertEqual(got['title'], 'Good evening, 2 to-dos done today')
        self.assertTrue(got['text'].startswith('Work\nDone today\n• Send the order form'), got['text'])
        self.assertIn('Personal\nDone today\n• Book the dentist', got['text'])
        self.assertNotIn('Open The Machine', got['text'])  # it is open already
        self.assertNotIn('](', got['text'])
        self.assertEqual([s['area'] for s in got['sections']], ['work', 'personal'])
        # drawn as it reads: the areas headings, Done today a subhead, the to-dos a list
        self.assertEqual(got['blocks'][:3], [['h', 'Work'], ['sub', 'Done today'], ['li', 'Send the order form']])
        self.assertIn(['h', 'Personal'], got['blocks'])
        self.assertEqual(self.shown('morning'), {})  # the evening's never stands in for the morning's

    def test_the_morning_keeps_its_text_and_the_email_links_back_to_it(self):
        out = notify.compose([], [{'id': 'a1b2c3d4e5f60718', 'title': 'Pay the invoice'}], [], 'https://m.example/')
        self.assertEqual(out['push']['url'], 'https://m.example/#digest=morning')
        self.assertTrue(out['text'].endswith('Open The Machine: https://m.example/#digest=morning'), out['text'])
        with self.store.connect() as db:
            notify.ensure(db)
        with self.store.connect() as db:
            notify.digest_claim(db, '2026-11-12', '2026-11-12T07:30:00+00:00')
        with self.store.connect() as db:
            notify.digest_done(db, '2026-11-12', 'sent', ['push', 'email'], out)
        got = self.shown('morning')
        self.assertEqual((got['title'], got['text']), ('Good morning, 1 due today', '• Pay the invoice'))  # without its Open link
        self.assertEqual(got['blocks'], [['li', 'Pay the invoice']])

    def test_only_a_sent_one_keeps_its_text_and_not_past_a_week(self):
        out = notify.compose([], [{'title': 'Pay the invoice'}], [])
        old = (a.dt.datetime.now(UTC) - notify.DIGEST_KEEP - a.dt.timedelta(hours=1)).isoformat()
        with self.store.connect() as db:
            notify.ensure(db)
        for day, at, status in (('2026-10-01', old, 'sent'), ('2026-11-11', a.now(), 'not_sent')):
            with self.store.connect() as db:
                notify.digest_claim(db, day, at)
            with self.store.connect() as db:
                notify.digest_done(db, day, status, [], out)
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT day,body IS NULL FROM notify_digests ORDER BY day')],
                             [('2026-10-01', 1), ('2026-11-11', 1)])
        self.assertEqual(self.shown('morning'), {})

    def test_the_owners_dashboard_only(self):
        with self.assertRaises(ValueError):
            self.app.action('digest_sent', {'kind': 'evening'}, owner_dashboard=False)
        self.assertEqual(self.shown('weekly'), {})

    def test_the_digest_row_hides_until_the_next_digest_or_day(self):
        # To-dos' Digest row: its × keeps it hidden on the Machine (every device), until a digest goes out or the next day
        at = lambda d, h, m=0: a.dt.datetime(2026, 11, d, h, m, tzinfo=BXL).astimezone(UTC)

        def hidden(current):
            with self.store.connect() as db:
                return notify.digest_row_hidden(db, current, BXL)
        self.assertFalse(hidden(at(13, 7)))  # never hidden
        with self.assertRaises(ValueError):
            self.app.action('digest_row_hide', {}, owner_dashboard=False)
        self.assertIn('digest_row_hide', a.DASHBOARD_ACTIONS)
        self.assertIn('digest_row_hide', a.OWNER_ACTIONS)  # never the CLI the agent runs
        with self.store.connect() as db:
            notify.digest_row_hide(db, at(13, 6, 45).isoformat())
        self.assertTrue(hidden(at(13, 7)))
        self.assertTrue(hidden(at(13, 23, 59)))
        self.assertFalse(hidden(at(14, 0, 1)))  # the next day: back
        with self.store.connect() as db:  # a digest that didn't go out changes nothing
            notify.digest_claim(db, 'evening:2026-11-13', at(13, 17, 45).isoformat())
        with self.store.connect() as db:
            notify.digest_done(db, 'evening:2026-11-13', 'empty', [])
        self.assertTrue(hidden(at(13, 18)))
        with self.store.connect() as db:  # one sent before it was hidden neither
            notify.digest_claim(db, '2026-11-13', at(13, 6, 30).isoformat())
        with self.store.connect() as db:
            notify.digest_done(db, '2026-11-13', 'sent', ['push'], notify.compose([], [{'title': 'Pay the invoice'}], []))
        self.assertTrue(hidden(at(13, 18)))
        with self.store.connect() as db:  # the evening digest sent after: back for it
            db.execute("UPDATE notify_digests SET status='sent',created_at=? WHERE day='evening:2026-11-13'", (at(13, 17, 46).isoformat(),))
        self.assertFalse(hidden(at(13, 18)))
        # the action stamps now and the status says so
        with self.store.connect() as db:
            db.execute('DELETE FROM notify_digests')
        self.assertEqual(self.app.action('digest_row_hide', {}, owner_dashboard=True), {'digest_row_hidden': True})
        with patch_everywhere(a, 'local_tz', return_value=BXL):
            self.assertTrue(self.app.digest_row_view())


if __name__ == '__main__':
    unittest.main()

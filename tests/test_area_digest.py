"""An area's digest (notify.area_digest, App.area_digests, the area_digest action): what got done today and what is
still open, per area (Work, Personal), as plain text the owner copies from To-dos. Nothing for an area with nothing
worth listing; only on the owner's own dashboard. The morning digest doesn't carry it (no evening-style recap there). Made-up to-dos only; nothing is sent."""
import tempfile, unittest
from pathlib import Path
from zoneinfo import ZoneInfo
import assistant as a
import notify
import reading_digest
from seams import patch_everywhere  # noqa: E402

UTC = a.dt.timezone.utc
BXL = ZoneInfo('Europe/Brussels')


def at(day, h, m=0):
    return a.dt.datetime(2026, 11, day, h, m, tzinfo=BXL)  # 2026-11-12 is a Thursday


class Text(unittest.TestCase):
    def test_done_then_still_open_with_what_is_due_today_and_a_count_for_the_rest(self):
        done = [{'title': 'Send the order form'}, {'title': 'Reply to the supplier'}]
        still = [{'title': 'Send the signed contract', 'due': '2026-11-12'}, {'title': 'Plan the offsite', 'due': '2026-11-20'}]
        self.assertEqual(notify.area_digest(done, still, '2026-11-12'),
                         'Done today\n• Send the order form\n• Reply to the supplier\n'
                         'Still open\n• Due today: Send the signed contract\n• Plan the offsite')
        many = [{'title': f'To-do {n}'} for n in range(notify.AREA_LISTED + 3)]
        text = notify.area_digest([], many)
        self.assertTrue(text.startswith('Still open\n• To-do 0\n'), text)
        self.assertTrue(text.endswith(f'• To-do {notify.AREA_LISTED - 1}\n• +3 more'), text)
        self.assertEqual(notify.area_digest(many, []).splitlines()[-1], '• +3 more')

    def test_nothing_worth_listing_says_nothing(self):
        self.assertEqual(notify.area_digest([], []), '')
        self.assertEqual(notify.area_digest([{'title': ' '}], [{'title': ''}]), '')

    def test_the_morning_digest_has_no_area_part(self):
        # what got done is the evening digest's; what is open is the morning's own list and its count
        due = [{'id': 'a1b2c3d4e5f60718', 'title': 'Reply to the supplier'}]
        out = notify.compose([], due, [], 'https://m.example/', total=2)
        for word in ('Work', 'Personal', 'Done today', 'Still open'):
            self.assertNotIn(word, out['text'])
            self.assertNotIn(word, out['read'])
        self.assertEqual(out['sections'], [])
        self.assertFalse([b for b in out['blocks'] if b[0] in ('h', 'sub')], out['blocks'])


class FromTheMachine(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [{'id': 'home', 'boundary': 'personal:me'}, {'id': 'office', 'boundary': 'work:Acme'},
                                                      {'id': 'machine', 'boundary': 'owner:system'}],
                                         'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        a.set_work_hours({'start': '08:00', 'end': '18:00'}); self.addCleanup(a.set_work_hours, None)
        self.n = 0

    def card(self, title, account='office', **extra):
        self.n += 1
        self.store.commit_page(account, {}, [{'account_id': account, 'source_id': f'm{self.n}', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        sid = self.store.suggest(f'k{self.n}', title, 'Body', [self.n], **extra)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        return sid

    def done(self, sid, when):
        with self.store.connect() as db:
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'complete','','dashboard',?)",
                       ('d-' + sid, sid, when.astimezone(UTC).isoformat()))
            db.execute("UPDATE suggestions SET status='completed',closed_decision_id=? WHERE id=?", ('d-' + sid, sid))

    def digests(self, when):
        with patch_everywhere(a, 'local_tz', return_value=BXL):
            return self.app.area_digests(when.astimezone(UTC))

    def test_each_area_as_the_to_dos_filter_places_it(self):
        self.done(self.card('Send the order form'), at(12, 10))
        self.done(self.card('Book the venue'), at(11, 16))  # yesterday
        self.card('Send the signed contract', due='2026-11-12')
        self.card('Answer the school', account='home')
        self.card('Gateway keeps restarting', account='machine')  # about the Machine itself: neither area
        snoozed = self.card('Renew the passport', account='home')
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='snoozed' WHERE id=?", (snoozed,))
        out = self.digests(at(12, 15))
        self.assertEqual(out['work'], 'Done today\n• Send the order form\nStill open\n• Due today: Send the signed contract')
        self.assertEqual(out['personal'], 'Still open\n• Answer the school')
        self.assertNotIn('Gateway', out['work'] + out['personal'])

    def test_an_area_with_nothing_is_empty_and_something_to_read_is_left_out(self):
        reading = self.card('Daily digest')
        with self.store.connect() as db:
            reading_digest.ensure(db)
            db.execute("INSERT INTO digest_items(suggestion_id,item,account_id,address,updated_at) VALUES(?,1,'office','news@example.com',?)", (reading, a.now()))
        self.assertEqual(self.digests(at(12, 9)), {'work': '', 'personal': ''})

    def test_only_on_the_owners_own_dashboard(self):
        self.card('Answer the school', account='home')
        with patch_everywhere(a, 'local_tz', return_value=BXL):
            with self.assertRaises(ValueError):
                self.app.action('area_digest', {}, owner_dashboard=False)
            self.assertEqual(self.app.action('area_digest', {}, owner_dashboard=True)['personal'], 'Still open\n• Answer the school')

    def test_the_morning_digest_email_has_no_area_part_and_counts_nothing_done(self):
        work = ['Send the signed contract', 'Plan the offsite', 'Review the budget', 'Call the bank']
        home = ['Answer the school', 'Book the dentist', 'Renew the passport']
        self.done(self.card('Send the order form'), at(12, 8, 30))  # done this morning: the evening digest says it
        for title in home:
            self.card(title, account='home')
        for title in work:
            self.card(title)
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', return_value=[]):
            digest = self.app.digest(at(12, 9).astimezone(UTC))
        text = digest['text']
        for word in ('\nWork\n', '\nPersonal\n', 'Done today', 'Still open', 'Send the order form'):
            self.assertNotIn(word, text)
        self.assertEqual(digest['sections'], [])
        # To-dos' Digest row: how many each area has open, nothing done
        self.assertEqual(digest['counts'], {'work': {'done': 0, 'open': 4}, 'personal': {'done': 0, 'open': 3}})
        # every waiting to-do is listed or counted, once: 3 lines up top, "4 more can wait"
        self.assertEqual(sum(text.count(x) for x in work + home), 3, text)
        self.assertIn('4 more can wait', text)

if __name__ == '__main__':
    unittest.main()

"""An area's digest (notify.area_digest, App.area_digests, the area_digest action and its part of the morning digest):
what got done today and what is still open, per area (Work, Personal), as plain text the owner copies from To-dos and
finds again in the morning digest's email. Nothing for an area with nothing worth listing; only on the owner's own
dashboard; never titles in the email when notifications hide to-do text. Made-up to-dos only; nothing is sent."""
import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import assistant as a
import notify
import reading_digest
import security_levels
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

    def test_the_morning_digest_carries_each_area_after_the_rest_only_with_titles(self):
        areas = [('work', 'Still open\n• Plan the offsite'), ('personal', '')]
        text = notify.compose([], [], [{'title': 'Answer the school'}], 'https://m.example/', total=1, areas=areas)['text']
        self.assertTrue(text.endswith('\n\nWork\nStill open\n• Plan the offsite\n\nOpen The Machine: https://m.example/#digest=morning'), text)
        self.assertNotIn('Personal', text)
        careful = notify.compose([], [], [{'title': 'Answer the school'}], '', show_text=False, total=1, areas=areas)
        self.assertNotIn('Plan the offsite', careful['text'])
        self.assertNotIn('Plan the offsite', notify.compose([], [], [{'title': 'Answer the school'}], '', total=1, areas=areas)['push']['body'])

    def test_the_morning_digest_lists_a_to_do_once(self):
        due = [{'id': 'a1b2c3d4e5f60718', 'title': 'Reply to the supplier'}]
        still = [{'id': 'a1b2c3d4e5f60718', 'title': 'Reply to the supplier', 'due': '2026-11-13'},
                 {'id': 'b1b2c3d4e5f60718', 'title': 'Send the quarterly numbers'}]
        rows = {'work': ([], still, '2026-11-13'), 'personal': ([], [{'id': 'c1b2c3d4e5f60718', 'title': 'Book the dentist'}], '')}
        areas = [(a, notify.area_digest(*rows[a])) for a in notify.AREAS]
        out = notify.compose([], due, [], 'https://m.example/', total=3, top=still, areas=areas, area_rows=rows)
        # the three lines above the areas carry the due one with its Open link; Work lists the rest
        self.assertEqual(out['text'].count('Reply to the supplier'), 1, out['text'])
        self.assertIn('• Reply to the supplier · [Open]', out['text'])
        self.assertEqual(out['text'].count('Send the quarterly numbers'), 1, out['text'])
        self.assertEqual(out['text'].count('Book the dentist'), 1, out['text'])
        self.assertEqual(out['read'].count('Reply to the supplier'), 1, out['read'])
        self.assertEqual([b for b in out['blocks'] if 'Reply to the supplier' in b[1]], [['li', 'Reply to the supplier']])
        # Copy Work stays the whole area, as the To-dos digest copies it
        self.assertEqual(out['sections'][0], {'area': 'work', 'copy': 'Still open\n• Due today: Reply to the supplier\n• Send the quarterly numbers'})

    def test_an_area_with_only_what_the_top_lists_is_left_out(self):
        due = [{'id': 'a1b2c3d4e5f60718', 'title': 'Reply to the supplier'}]
        rows = {'work': ([], [dict(due[0], due='2026-11-13')], '2026-11-13')}
        out = notify.compose([], due, [], '', total=1, top=rows['work'][1], areas=[('work', notify.area_digest(*rows['work']))], area_rows=rows)
        self.assertNotIn('Work', out['text'])
        self.assertEqual(out['sections'], [{'area': 'work', 'copy': 'Still open\n• Due today: Reply to the supplier'}])


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

    def test_the_morning_digest_email_has_both_areas_unless_text_is_hidden(self):
        work = ['Send the signed contract', 'Plan the offsite', 'Review the budget', 'Call the bank']
        home = ['Answer the school', 'Book the dentist', 'Renew the passport']
        for title in home:  # the newest lead: three Work ones up top, Work's fourth and all of Personal below
            self.card(title, account='home')
        for title in work:
            self.card(title)
        with patch_everywhere(a, 'local_tz', return_value=BXL), patch_everywhere(a, 'recap_meetings', return_value=[]):
            digest = self.app.digest(at(12, 9).astimezone(UTC))
            text = digest['text']
            self.assertIn('\n\nWork\nStill open\n• ', text)
            self.assertIn('\n\nPersonal\nStill open\n• ', text)
            # each to-do once: the three lines up top, the rest under its area; Copy Work and Copy Personal stay whole
            for title in work + home:
                self.assertEqual(text.count(title), 1, (title, text))
            copied = {s['area']: s['copy'] for s in digest['sections']}
            self.assertTrue(all(x in copied['work'] for x in work) and all(x in copied['personal'] for x in home), copied)
            # a Careful Work Fleet keeps Work titles out of notifications: the Work part goes, the owner's Personal stays
            with patch.object(security_levels, 'careful_fleets', return_value=[{'id': 'f1'}]):
                fleet = self.app.digest(at(12, 9).astimezone(UTC))['text']
            self.assertNotIn('\nWork\n', fleet)
            self.assertIn('\n\nPersonal\nStill open\n• ', fleet)
            with self.store.connect() as db:  # to-do text off in notifications: no part at all
                security_levels.set_pref(db, 'notify_text', 'off')
            careful = self.app.digest(at(12, 9).astimezone(UTC))['text']
        for title in work + home:
            self.assertNotIn(title, careful)


if __name__ == '__main__':
    unittest.main()

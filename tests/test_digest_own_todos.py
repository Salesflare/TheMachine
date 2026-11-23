"""The morning digest names the owner's own to-dos (New to-do, "Added by you") that wait on them, also when its headline
counts something else (a to-do ready for their OK), and its "N more can wait" counts only what waits: a snoozed to-do
coming back later today shows as due today but isn't one of the waiting (notify.compose own, counts).
Fake fixture data only; nothing is sent."""
import tempfile, unittest
from pathlib import Path
from zoneinfo import ZoneInfo
import datetime as dt
import notify
from seams import patch_everywhere  # noqa: E402
import machine.app.recap as machine_app_recap
import machine.main as machine_main
import timeutil

UTC = dt.timezone.utc
BXL = ZoneInfo('Europe/Brussels')


class OwnTodos(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App); self.app.store = self.store
        self.app.config = {'openclaw_workspace': self.temp.name, 'accounts': [{'id': 'home', 'boundary': 'personal:me'}],
                           'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/'}
        timeutil.set_work_hours({'start': '08:00', 'end': '18:00'}); self.addCleanup(timeutil.set_work_hours, None)

    def card(self, title):
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': 'm-' + title, 'kind': 'gmail.message', 'occurred_at': timeutil.now(),
                                             'title': 'Evidence', 'body': 'Evidence', 'metadata': {}, 'deleted': False}])
        with self.store.connect() as db:
            event = db.execute('SELECT max(id) FROM events').fetchone()[0]
        sid = self.store.suggest('k-' + title, title, 'Body', [event])['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL WHERE id=?', (sid,))
        return sid

    def test_the_owners_own_to_dos_are_named_beside_a_ready_one(self):
        ready = self.store.owner_card('Reseal the bathtub', 'home')['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (ready,))
        self.store.owner_card('Lower the kitchen step', 'home')
        self.store.owner_card('Get new bike pedals', 'home')
        back = self.card('Send the sample deal')  # snoozed, back later today, due yesterday: a "Due today" line
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='snoozed',due='2026-11-15',snoozed_until=? WHERE id=?",
                       (dt.datetime(2026, 11, 16, 10, 41, tzinfo=BXL).astimezone(UTC).isoformat(), back))
        with patch_everywhere(timeutil, 'local_tz', return_value=BXL), patch_everywhere(machine_app_recap, 'recap_meetings', return_value=[]):
            digest = self.app.digest(dt.datetime(2026, 11, 16, 9, 5, tzinfo=BXL).astimezone(UTC))
        self.assertEqual(digest['subject'], 'Good morning, ready for your OK: Reseal the bathtub')
        text = digest['text']
        self.assertIn('• Reseal the bathtub', text)
        self.assertIn('• Due today: Send the sample deal', text)
        self.assertIn('• Lower the kitchen step', text)  # was only counted, as "1 more can wait"
        self.assertIn('• Get new bike pedals', text)
        self.assertNotIn('more can wait', text)  # all three waiting are named: none left to count

    def test_a_snoozed_due_line_is_not_taken_from_what_waits(self):
        ready = [{'id': 'a1b2c3d4e5f60718', 'title': 'Send the quote', 'status': 'prepared'}]
        due = [{'id': 'b1b2c3d4e5f60718', 'title': 'Send the sample deal', 'status': 'snoozed'}]
        top = ready + [{'id': 'c1b2c3d4e5f60718', 'title': 'Answer the supplier'}, {'id': 'd1b2c3d4e5f60718', 'title': 'Book the venue'}]
        out = notify.compose([], due, [], total=3, top=top, ready=ready)
        self.assertIn('2 more can wait', out['text'])

    def test_own_to_dos_beyond_the_limit_are_counted(self):
        top = [{'id': '%016x' % n, 'title': f'Own to-do {n}'} for n in range(notify.OWN_LISTED + 3)]
        out = notify.compose([], [], [], total=len(top), top=top, own=[i['id'] for i in top])
        self.assertEqual(out['text'].count('• Own to-do'), notify.OWN_LISTED)
        self.assertIn('3 more can wait', out['text'])
        quiet = notify.compose([], [], [], show_text=False, total=len(top), top=top, own=[i['id'] for i in top])
        self.assertNotIn('Own to-do', quiet['text'] + quiet['push']['body'])


if __name__ == '__main__':
    unittest.main()

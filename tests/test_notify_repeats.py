"""Fewer repeat notifications for the same to-do (notify.py, machine/delivery/): a to-do prepared before its first
notification says "Ready:", never "Reminder:"; a rerun's newer result while the earlier notification is still unseen
updates the to-do silently; and the morning digest email takes the held waiting-for-you lines it covered with it.
Every send here is a fake: no push service, Telegram or mail server is reached."""
import json, tempfile, unittest, uuid
from pathlib import Path
from unittest.mock import patch
import assistant as a
import notify
from seams import patch_everywhere  # noqa: E402

SUB = {'endpoint': 'https://fcm.googleapis.com/fcm/send/abc', 'keys': {'p256dh': 'B' + 'x' * 86, 'auth': 'y' * 22}}
UTC = a.dt.timezone.utc


class Daytime(a.dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 12, 10, 0, tzinfo=tz or UTC)  # a Monday, within hours


class Repeats(unittest.TestCase):
    def setUp(self):
        notify.reset_active(); self.addCleanup(notify.reset_active)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.config = self.app.config = {'accounts': [], 'dashboard_host': 'the-machine.example', 'dashboard_path': '/assistant/',
                                         'telegram_owner': '42', 'credentials': {'fleet': 'fleet'}, 'fleet': {'url': 'https://cp.example/api/fleet'}}
        self.app.action('push_subscribe', SUB, owner_dashboard=True)
        self.pushed, self.told = [], []
        self.store.commit_page('home', {}, [{'account_id': 'home', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': a.now(),
                                             'title': 'Quote', 'body': 'Could you send the quote?', 'metadata': {}, 'deleted': False}])
        # urgent: it buzzes (only what can't wait does, tests/test_calm_notify.py)
        self.sid = self.store.suggest('quote', 'Send the quote to the bakery', 'They ask for the quote.', [1], urgent=True)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')

    def run_ahead(self, body):
        """A run The Machine started by itself (prepared ahead) saves its result, as Store.prepare does for any run."""
        job = uuid.uuid4().hex
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted',early=1 WHERE id=?", (self.sid,))
            db.execute('DELETE FROM preparations WHERE suggestion_id=?', (self.sid,))
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,?,?,'running',?,?)",
                       (self.sid, 'ahead:' + job, job, a.now(), a.now()))
        self.store.prepare(self.sid, body, job_id=job, outcome={'state': 'needs_you', 'needs': 'check the reply'})

    def deliver(self):
        def push_send(store, config, subs, payload, label, sender=None, kind=None, **extra):
            self.pushed.append(payload)
            return [{'status': 201}]
        with patch.object(a.dt, 'datetime', Daytime), patch_everywhere(a, 'push_send', push_send), \
                patch_everywhere(a, 'telegram', side_effect=lambda config, row, action, message_id=None: self.told.append(dict(row)) or {'messageId': str(len(self.told) + 100)}):
            return a.deliver_one(self.store, self.config, edit_cards=False)

    def held_titles(self):
        with self.store.connect() as db:
            notify.ensure(db)
            return [r[0] for r in db.execute("SELECT title FROM notify_queue WHERE channel='email' ORDER BY id")]

    def delivery(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT status,reminder,needs_edit,message_id,last_notified_at FROM deliveries WHERE suggestion_id=?', (self.sid,)).fetchone())

    # -- A: the first notification of a to-do prepared before it ever went out
    def test_a_to_do_prepared_before_its_first_notification_says_ready_not_reminder(self):
        self.run_ahead('Here is the quote reply, ready to send.')
        self.assertEqual((self.delivery()['status'], self.delivery()['reminder'], self.delivery()['message_id']), ('queued', 1, None))
        self.assertTrue(self.deliver())
        self.assertEqual(self.pushed[0]['title'], 'Ready: Send the quote to the bakery')
        self.assertEqual(self.pushed[0]['body'], 'Here is the quote reply, ready to send.')
        self.assertEqual(self.held_titles(), ['Ready: Send the quote to the bakery'])
        self.assertNotIn('Reminder', json.dumps(self.pushed))
        self.assertEqual(self.delivery()['reminder'], 0)

    def test_a_to_do_still_preparing_at_its_first_notification_is_new_not_a_reminder(self):
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (self.sid,))
            db.execute("UPDATE deliveries SET reminder=1 WHERE suggestion_id=?", (self.sid,))
        self.assertTrue(self.deliver())
        self.assertEqual(self.pushed[0]['title'], 'Send the quote to the bakery')
        self.assertEqual(self.held_titles(), ['Send the quote to the bakery'])
        self.assertEqual(notify.kind_of({'status': 'accepted', 'reminder': 1, '_first': True}), 'todo')
        self.assertEqual(notify.kind_of({'status': 'pending', 'reminder': 1}), 'reminder')

    def test_a_snooze_coming_back_still_says_reminder(self):
        self.assertTrue(self.deliver())  # its first notification
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='queued',reminder=1 WHERE suggestion_id=?", (self.sid,))
        self.assertTrue(self.deliver())
        self.assertEqual(self.pushed[-1]['title'], 'Reminder: Send the quote to the bakery')

    # -- B: a rerun's newer result while the earlier notification is still unseen
    def test_a_newer_result_while_the_earlier_notification_is_unseen_updates_it_silently(self):
        self.run_ahead('First draft of the quote reply.')
        self.assertTrue(self.deliver())
        self.assertEqual(len(self.pushed), 1)
        self.run_ahead('Second draft of the quote reply.')  # a new signal reran it; the owner hasn't looked yet
        self.assertEqual(self.delivery()['status'], 'queued')
        with self.assertLogs(a.LOG, 'INFO') as logs:
            self.assertTrue(self.deliver())
        self.assertIn('quiet=unseen', '\n'.join(logs.output))
        self.assertEqual((len(self.pushed), len(self.told)), (1, 1))  # no second ping, no second message
        self.assertEqual(len(self.held_titles()), 1)
        row = self.delivery()
        self.assertEqual((row['status'], row['reminder'], row['needs_edit']), ('sent', 0, 1))  # the card is edited in place
        self.assertFalse(self.deliver())  # nothing left queued

    def test_a_newer_result_pings_again_once_the_owner_saw_the_earlier_one(self):
        self.run_ahead('First draft of the quote reply.')
        self.assertTrue(self.deliver())
        pinged = a.dt.datetime.fromisoformat(self.delivery()['last_notified_at']).timestamp()
        notify.mark_active(lambda: pinged + 30, client='desk', on=True)  # they opened the dashboard after it
        notify.mark_active(lambda: pinged + 60, client='desk', on=False)
        self.run_ahead('Second draft of the quote reply.')
        self.assertTrue(self.deliver())
        self.assertEqual(len(self.pushed), 2)

    def test_a_newer_result_pings_again_after_the_owners_own_step_on_it(self):
        self.run_ahead('First draft of the quote reply.')
        self.assertTrue(self.deliver())
        with self.store.connect() as db:  # they answered on Telegram: a step of theirs after the ping
            later = (a.dt.datetime.fromisoformat(self.delivery()['last_notified_at']) + a.dt.timedelta(minutes=10)).isoformat()
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES('d1',?,'revise','Shorter please','telegram',?)", (self.sid, later))
        self.run_ahead('Second, shorter draft of the quote reply.')
        self.assertTrue(self.deliver())
        self.assertEqual(len(self.pushed), 2)

    # -- C: the morning digest email covers what it lists
    def test_the_digest_email_clears_the_held_lines_it_covered(self):
        mails = []
        t0 = a.dt.datetime(2026, 10, 12, 9, 5, tzinfo=UTC)
        other = self.store.suggest('venue', 'Book the venue', 'The venue asks for a date.', [1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='prepared',deliver_after=NULL")
        with patch.object(notify.time, 'time', return_value=t0.timestamp() - 60):
            a.hold_mail(self.store, self.config, 'result', 'Ready: Send the quote to the bakery', 'suggestion:' + self.sid)
            a.hold_mail(self.store, self.config, 'result', 'Ready: Book the venue', 'suggestion:' + other)
        with patch_everywhere(a, 'local_tz', return_value=UTC), patch_everywhere(a, 'credential', return_value='token'), \
                patch_everywhere(a, 'recap_meetings', return_value=[]), patch.object(notify.time, 'time', return_value=t0.timestamp()):
            digest = self.app.digest(t0)
            self.assertIn('Send the quote to the bakery', digest['text'])  # a ready pile alone gets its digest
            self.assertEqual(set(digest['covers']), {self.sid, other})
            went = self.app.digest_step(current=t0, push=lambda request: {'results': [{'endpoint': SUB['endpoint'], 'status': 201}]},
                                        mail=lambda url, token, subject, text: mails.append(subject) or True)
        self.assertIn('email', went)
        self.assertEqual(self.held_titles(), [])
        # What comes in after the digest still gets its line
        with patch.object(notify.time, 'time', return_value=t0.timestamp() + 120):
            a.hold_mail(self.store, self.config, 'result', 'Ready: Book the venue', 'suggestion:' + other)
        self.assertEqual(self.held_titles(), ['Ready: Book the venue'])

    def test_drop_covered_keeps_other_to_dos_and_later_lines(self):
        with self.store.connect() as db:
            notify.hold(db, 'email', 'result', 'One', 1000.0, ref='suggestion:' + 'a' * 16, clock=lambda: 100.0)
            notify.hold(db, 'email', 'result', 'Two', 1000.0, ref='suggestion:' + 'b' * 16, clock=lambda: 100.0)
            notify.hold(db, 'email', 'result', 'Three', 1000.0, ref='suggestion:' + 'a' * 16, clock=lambda: 300.0)
            self.assertEqual(notify.drop_covered(db, ['suggestion:' + 'a' * 16], 200.0), 1)
        self.assertEqual(self.held_titles(), ['Two', 'Three'])


if __name__ == '__main__':
    unittest.main()

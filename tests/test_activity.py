"""The daily activity counts for the hosted health report (activity.py): plain integers per local day, the last 7 days,
counted from the owner's presses, the outbox and the dashboard's own moments. Never a title, name, address or id."""
import datetime as dt, importlib.util, json, sqlite3, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

spec = importlib.util.spec_from_file_location('activity_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import activity

TZ = ZoneInfo('America/New_York')
NOW = '2026-10-29T15:00:00+00:00'  # 11:00 in New York


class Activity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        with self.store.connect() as db:
            for n, status in enumerate(('pending', 'prepared', 'completed', 'snoozed')):
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                           (f'{n:016x}', f'k{n}', 'Reply to Sam Example', 'Private body', '[]', '[]', status, NOW))

    def decide(self, db, choice, at, source='dashboard'):
        db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   (a.uuid.uuid4().hex, '0' * 16, choice, 'secret words', source, at))

    def job(self, db, kind, status, at):
        db.execute('INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) '
                   'VALUES(?,?,?,?,?,?,?,?,?,?)', (a.uuid.uuid4().hex, '0' * 16, a.uuid.uuid4().hex,
                                                   json.dumps({'kind': kind, 'to': ['sam@example.com'], 'subject': 'Hi'}), status, at, at, 'x', 'dashboard', ''))

    def test_presses_and_outbox_count_per_local_day(self):
        with self.store.connect() as db:
            self.decide(db, 'accept', '2026-10-29T14:00:00+00:00')
            self.decide(db, 'accept', '2026-10-29T03:00:00+00:00')  # 23:00 on the 28th in New York
            self.decide(db, 'prepare_next', '2026-10-29T14:01:00+00:00')
            self.decide(db, 'send', '2026-10-29T14:02:00+00:00')
            self.decide(db, 'complete', '2026-10-29T14:03:00+00:00', source='telegram')
            self.decide(db, 'reject', '2026-10-29T14:04:00+00:00')
            self.decide(db, 'snooze', '2026-10-29T14:05:00+00:00')
            self.decide(db, 'other', '2026-10-29T14:06:00+00:00')
            self.decide(db, 'other', '2026-10-29T14:06:00+00:00', source='fleet')  # not the owner's press
            self.decide(db, 'accept', '2026-10-10T14:00:00+00:00')  # older than the week
            self.job(db, 'email', 'sent', '2026-10-29T14:10:00+00:00')
            self.job(db, 'whatsapp', 'sent', '2026-10-27T14:10:00+00:00')
            self.job(db, 'email', 'queued', '2026-10-29T14:10:00+00:00')  # not delivered
            self.job(db, 'merge', 'sent', '2026-10-29T14:10:00+00:00')  # not a message
            report = activity.report(db, TZ, NOW)
        days = {d['day']: d for d in report['days']}
        self.assertEqual(list(days), [f'2026-10-{n}' for n in range(23, 30)])
        today = days['2026-10-29']
        self.assertEqual({k: today[k] for k in ('do_it', 'send', 'sent', 'done', 'dismissed', 'snoozed', 'chat')},
                         {'do_it': 2, 'send': 1, 'sent': 1, 'done': 1, 'dismissed': 1, 'snoozed': 1, 'chat': 1})
        self.assertEqual((days['2026-10-28']['do_it'], days['2026-10-27']['sent']), (1, 1))
        # Counts only: every value a plain integer, no content anywhere
        for day in report['days']:
            self.assertEqual(set(day), {'day', *activity.KINDS})
            self.assertTrue(all(type(v) is int for k, v in day.items() if k != 'day'))
        text = json.dumps(report)
        for secret in ('Sam', 'example.com', 'secret', 'Private', 'Hi', '0000000000000000'):
            self.assertNotIn(secret, text)

    def test_dashboard_moments_count_distinct(self):
        with patch.object(a, 'now', return_value=NOW), patch.object(a, 'local_tz', return_value=TZ):
            self.store.note_activity('dashboard')
            self.store.note_activity('dashboard')  # within the minute: no second write
            self.store._activity_at = 0
            self.store.note_activity('dashboard')  # the same to-dos and hour again: still distinct
            self.store.note_activity('visit')
            self.store.note_activity('visit')
            self.store.note_activity('opened', '0' * 16)
            self.store.note_activity('opened', '0' * 16)
            self.store.note_activity('opened', '../etc')  # not an id: ignored
        with self.store.connect() as db:
            today = activity.report(db, TZ, NOW)['days'][-1]
        # pending and prepared are on the list; completed and snoozed are not
        self.assertEqual({k: today[k] for k in ('shown', 'opened', 'visits', 'active_hours')},
                         {'shown': 2, 'opened': 1, 'visits': 2, 'active_hours': 1})

    def test_old_marks_are_dropped(self):
        with self.store.connect() as db:
            activity.note(db, 'opened', ['a'], '2026-10-01T12:00:00+00:00', TZ)
            activity.note(db, 'opened', ['b'], NOW, TZ)
            self.assertEqual([r[0] for r in db.execute('SELECT ref FROM activity_seen')], ['b'])

    def test_report_for_the_health_report(self):
        db = sqlite3.connect(self.store.path)
        try:
            report = a.activity_report(db, 'America/New_York', NOW)
            self.assertEqual(len(report['days']), 7)
            self.assertEqual(report['days'][-1]['day'], '2026-10-29')
            self.assertEqual(a.activity_report(db, 'Not/AZone', NOW)['days'][-1]['day'][:4], '2026')
        finally:
            db.close()

    def test_card_chat_counts_an_open_only_from_the_dashboard(self):
        app = object.__new__(a.App); app.store = self.store; app.config = {'accounts': []}
        with patch.object(a.App, 'card_chat', return_value={'items': []}), patch.object(a, 'now', return_value=NOW), patch.object(a, 'local_tz', return_value=TZ):
            app.action('card_chat', {'suggestion_id': '1' * 16}, owner_dashboard=True)
            app.action('card_chat', {'suggestion_id': '2' * 16, 'cursor': 'c'}, owner_dashboard=True)  # a poll of an open chat
            app.action('card_chat', {'suggestion_id': '3' * 16})  # not the owner's dashboard
        with self.store.connect() as db:
            self.assertEqual([r[0] for r in db.execute("SELECT ref FROM activity_seen WHERE kind='opened'")], ['1' * 16])


if __name__ == '__main__':
    unittest.main()

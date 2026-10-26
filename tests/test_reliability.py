import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def event(account='work', source='one'):
    return {'account_id': account, 'source_id': source, 'kind': 'gmail.message',
            'occurred_at': '2026-10-09T10:00:00+00:00', 'title': 'A real subject',
            'body': 'Body', 'metadata': {}, 'deleted': False}


class Daytime(a.dt.datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 10, 10, 10, 0, tzinfo=tz or a.dt.timezone.utc)


class Reliability(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def delivery(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM deliveries WHERE suggestion_id=?', (sid,)).fetchone())

    # Collector

    def test_a_plugin_checkpoint_without_a_mode_is_not_a_failure(self):
        # The RSS connector keeps only etag/last_modified in its checkpoint; a good sync must stay good.
        class Stop:
            calls = 0
            def is_set(self): return self.calls >= 1
            def wait(self, seconds): self.calls += 1; self.waited = seconds; return self.is_set()
        account = {'id': 'feed', 'service': 'rss', 'poll_seconds': 1800}
        app = object.__new__(a.App)
        app.config, app.store, app.stop = {'accounts': [account]}, self.store, Stop()
        def sync(store, config, acct):
            store.commit_page(acct['id'], {'etag': 'x'}, [])
            return {'mode': 'incremental', 'events': 0}
        with patch.object(a, 'sync_source', side_effect=sync):
            app.collector(account)
        with self.store.connect() as db:
            row = db.execute('SELECT failures, error FROM checkpoints WHERE account_id=?', ('feed',)).fetchone()
        self.assertEqual((row['failures'], row['error']), (0, None))
        self.assertEqual(app.stop.waited, 1800)

    def test_database_error_outside_sync_does_not_end_collector_thread(self):
        class Stop:
            calls = 0
            def is_set(self): return self.calls >= 2
            def wait(self, _): self.calls += 1; return self.is_set()
        class BrokenStore:
            def connect(self): raise sqlite3.OperationalError('database is locked')
        app = object.__new__(a.App)
        app.config, app.store, app.stop = {}, BrokenStore(), Stop()
        app.collector({'id': 'work', 'service': 'gmail'})  # must return normally, not raise
        self.assertEqual(app.stop.calls, 2)

    def test_a_restart_does_not_cost_slow_sources_an_extra_read(self):
        app = object.__new__(a.App)
        app.config, app.store = {}, self.store
        linkedin = {'id': 'li', 'service': 'linkedin', 'poll_seconds': 3600}
        self.assertEqual(app.resume_wait(linkedin), 0)  # never read: go now
        self.store.commit_page('li', {'mode': 'incremental'}, [])
        self.assertGreater(app.resume_wait(linkedin), 3500)  # just read: wait out the hour
        self.assertEqual(app.resume_wait({'id': 'li', 'service': 'gmail', 'poll_seconds': 60}), 0)  # fast sources go now
        with self.store.connect() as db:
            db.execute("UPDATE checkpoints SET last_success=?", ((a.dt.datetime.now(a.dt.timezone.utc) - a.dt.timedelta(hours=2)).isoformat(),))
        self.assertEqual(app.resume_wait(linkedin), 0)  # overdue: go now
        self.store.commit_page('li', {'mode': 'incremental', 'page_token': 'next'}, [])
        self.assertEqual(app.resume_wait(linkedin), 0)  # catching up: go now

    def test_restart_resumes_catchup_without_ignoring_x_budget_or_retry_deadline(self):
        app = object.__new__(a.App)
        app.config, app.store = {}, self.store
        for service in ('github', 'stripe', 'linkedin'):
            account = {'id': service, 'service': service, 'poll_seconds': 900}
            self.store.commit_page(service, {'mode': 'incremental', 'catchup': {'page': 6}, 'coverage_complete': False}, [])
            self.assertEqual(app.resume_wait(account), 0)
            self.store.commit_page(service, {'mode': 'incremental', 'coverage_complete': True}, [])
            self.assertGreater(app.resume_wait(account), 890)
        self.store.commit_page('x', {'mode': 'incremental', 'page': {'mention_catchup': {'cursor': 'next'}}, 'coverage_complete': False}, [])
        self.assertGreater(app.resume_wait({'id': 'x', 'service': 'x', 'poll_seconds': 3600}), 3590)
        deadline = (a.dt.datetime.now(a.dt.timezone.utc) + a.dt.timedelta(minutes=20)).isoformat()
        with self.store.connect() as db:
            db.execute('UPDATE checkpoints SET retry_at=? WHERE account_id=?', (deadline, 'github'))
        app.resume_wait({'id': 'github', 'service': 'github', 'poll_seconds': 900})
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT retry_at FROM checkpoints WHERE account_id='github'").fetchone()[0], deadline)

    def test_status_lists_sources_without_an_email(self):
        accounts = [{'id': 'openclaw-gateway', 'service': 'gateway', 'boundary': 'owner:system'},
                    {'id': 'feed', 'service': 'rss', 'boundary': 'work:Acme', 'display_name': 'Feed'}]
        names = {c['id']: c['display_name'] for c in self.store.snapshot(accounts)['connectors']}
        self.assertEqual(names, {'openclaw-gateway': 'openclaw-gateway', 'feed': 'Feed'})

    # Rolling replay windows

    def test_expired_gmail_history_replays_retained_window_not_since_install(self):
        install = int(time.time()) - 90 * 86400
        self.store.commit_page('work', {'mode': 'incremental', 'history_id': '1', 'after': install}, [])
        class Gmail:
            def __init__(self, *_): pass
            def profile(self): return {'historyId': '9'}
            def get(self, *_): raise a.SourceError('gmail', 404)
        with patch.object(a, 'Gmail', Gmail):
            a.sync_gmail(self.store, {}, {'id': 'work'})
        state = self.store.checkpoint('work')
        self.assertEqual(state['mode'], 'resync')
        self.assertGreater(state['after'], int(time.time()) - 8 * 86400)

    def test_slack_full_scan_uses_rolling_window_and_prunes_old_threads(self):
        recent, old = f'{time.time() - 86400:.6f}', f'{time.time() - 60 * 86400:.6f}'
        channel = {'id': 'C1', 'name': 'team', 'type': 'channel', 'threads': [old, recent]}
        self.store.commit_page('slack', {'mode': 'incremental', 'phase': 'scan', 'index': 0, 'channels': [channel],
                                         'after': f'{time.time() - 90 * 86400:.6f}',
                                         'next_discovery': time.time() + 86400}, [])
        calls = []
        class Source:
            def profile(self): pass
            def get(self, method, params): calls.append(params.copy()); return {'messages': []}
        a.sync_slack(self.store, {}, {'id': 'slack', 'slack_host': 'example.slack.com'}, Source())
        self.assertGreater(float(calls[0]['oldest']), time.time() - 8 * 86400)
        self.assertEqual(self.store.checkpoint('slack')['scan']['threads'], [recent])

    def test_saturated_whatsapp_window_is_split_instead_of_failing(self):
        calls = []
        class Source:
            def profile(self): pass
            def read(self, command):
                calls.append(command)
                return {'messages': [{}] * 1000 if len(calls) == 1 else []}
        result = a.sync_whatsapp(self.store, {}, {'id': 'personal-whatsapp'}, Source())
        self.assertEqual(result['events'], 0)
        self.assertEqual(len(calls), 3)  # whole week, then each half

    # Telegram delivery

    def test_missing_helper_binary_is_definitely_not_sent(self):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('one', 'One', 'Prepare', [1])['id']
        with patch.object(a.dt, 'datetime', Daytime), \
                patch.object(a.subprocess, 'run', side_effect=FileNotFoundError('node')):
            a.deliver(self.store, {'openclaw': '/missing/openclaw', 'telegram_owner': 'owner'})
        self.assertEqual(self.delivery(sid)['status'], 'queued')

    def test_failing_card_edit_backs_off(self):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('one', 'One', 'Prepare', [1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='123',needs_edit=1 WHERE suggestion_id=?", (sid,))
        with patch.object(a, 'telegram', side_effect=ValueError('OpenClaw delivery unconfirmed')) as send:
            a.deliver(self.store, {'telegram_owner': 'owner'})
            a.deliver(self.store, {'telegram_owner': 'owner'})
        self.assertEqual(send.call_count, 1)
        row = self.delivery(sid)
        self.assertEqual((row['needs_edit'], row['edit_failures']), (1, 1))
        self.assertIsNotNone(row['edit_retry_at'])

    def test_decision_during_first_send_queues_edit_of_new_card(self):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('one', 'One', 'Prepare', [1])['id']
        def owner_rejects_while_sending(*_):
            self.store.decide(sid, 'reject', '', 'owner-click', 'dashboard')
            return {'messageId': '777'}
        with patch.object(a.dt, 'datetime', Daytime), \
                patch.object(a, 'telegram', side_effect=owner_rejects_while_sending):
            a.deliver_one(self.store, {'telegram_owner': 'owner'}, edit_cards=False)
        row = self.delivery(sid)
        self.assertEqual((row['status'], row['message_id'], row['needs_edit']), ('sent', '777', 1))

    def test_result_still_notifies_after_an_uncertain_first_send(self):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('one', 'One', 'Prepare', [1])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='uncertain' WHERE suggestion_id=?", (sid,))
        self.store.decide(sid, 'accept', '', 'owner-click', 'dashboard')
        self.store.prepare(sid, 'A short draft')
        row = self.delivery(sid)
        self.assertEqual((row['status'], row['reminder']), ('queued', 1))

    # Uncertain sends

    def cache(self, cards):
        path = Path(self.temp.name) / 'openclaw.sqlite'
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS plugin_state_entries(plugin_id,namespace,entry_key,value_json)')
            for message_id, sid, date in cards:
                db.execute('INSERT INTO plugin_state_entries VALUES(?,?,?,?)', ('telegram', 'telegram.message-cache', f'x:{message_id}',
                    a.json.dumps({'sourceMessage': {'message_id': message_id, 'date': date, 'chat': {'id': 808},
                                                    'from': {'is_bot': True}, 'rich_message': {'cb': f'assistant:{sid}:accept'}}})))
        return {'telegram_owner': '808', 'openclaw_state': str(path)}

    def uncertain(self, minutes_ago, status='accepted'):
        self.store.commit_page('work', {}, [event()])
        sid = self.store.suggest('one', 'One', 'Prepare', [1])['id']
        when = (a.dt.datetime.now(a.dt.timezone.utc) - a.dt.timedelta(minutes=minutes_ago)).isoformat()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status=? WHERE id=?", (status, sid))
            db.execute("UPDATE deliveries SET status='uncertain',message_id='100',error='delivery_outcome_unknown',updated_at=? WHERE suggestion_id=?", (when, sid))
        return sid, a.dt.datetime.fromisoformat(when).timestamp()

    def test_uncertain_send_found_in_chat_is_marked_sent(self):
        sid, at = self.uncertain(5)
        config = self.cache([(100, sid, at - 7200), (205, sid, at - 30)])  # old original card + the reminder
        a.reconcile_uncertain(self.store, config)
        row = self.delivery(sid)
        self.assertEqual((row['status'], row['message_id']), ('sent', '205'))
        self.assertIn('100', row['previous_message_ids'])

    def test_uncertain_send_missing_from_chat_is_requeued_after_grace(self):
        sid, at = self.uncertain(5)
        config = self.cache([(100, sid, at - 7200)])  # only the original card, not the reminder
        a.reconcile_uncertain(self.store, config)
        self.assertEqual(self.delivery(sid)['status'], 'uncertain')  # still within grace: keep holding
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET updated_at=? WHERE suggestion_id=?",
                       ((a.dt.datetime.now(a.dt.timezone.utc) - a.dt.timedelta(minutes=45)).isoformat(), sid))
        a.reconcile_uncertain(self.store, config)
        row = self.delivery(sid)
        self.assertEqual((row['status'], row['reminder']), ('queued', 1))

    def test_uncertain_send_for_finished_item_is_cancelled_not_resent(self):
        sid, _ = self.uncertain(45, status='completed')
        a.reconcile_uncertain(self.store, self.cache([]))
        self.assertEqual(self.delivery(sid)['status'], 'cancelled')

    def test_unreadable_cache_keeps_holding(self):
        sid, _ = self.uncertain(45)
        a.reconcile_uncertain(self.store, {'telegram_owner': '808', 'openclaw_state': '/nonexistent/openclaw.sqlite'})
        self.assertEqual(self.delivery(sid)['status'], 'uncertain')

    def test_tomorrow_respects_a_day_that_starts_at_3am(self):
        local_tz = a.ZoneInfo('Europe/Amsterdam')
        def due(local):
            class Fixed(a.dt.datetime):
                @classmethod
                def now(cls, tz=None): return local.astimezone(tz or a.dt.timezone.utc)
            with patch.object(a.dt, 'datetime', Fixed):
                return a.dt.datetime.fromisoformat(a.snooze_time('tomorrow')).astimezone(local_tz)
        late_night = due(a.dt.datetime(2026, 10, 14, 1, 30, tzinfo=local_tz))
        self.assertEqual((late_night.day, late_night.hour), (14, 9))
        early = due(a.dt.datetime(2026, 10, 14, 3, 5, tzinfo=local_tz))
        self.assertEqual((early.day, early.hour), (15, 9))
        evening = due(a.dt.datetime(2026, 10, 14, 22, 0, tzinfo=local_tz))
        self.assertEqual((evening.day, evening.hour), (15, 9))

    # Review claims

    def test_pending_backlog_uses_partial_index(self):
        with self.store.connect() as db:
            plan = ' '.join(r[3] for r in db.execute(
                'EXPLAIN QUERY PLAN SELECT count(*) FROM events WHERE account_id=? AND analyzed_version<version', ('work',)))
        self.assertIn('events_pending_account', plan)


if __name__ == '__main__':
    unittest.main()

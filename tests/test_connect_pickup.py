"""A sign-in started on a paired self-hosted Machine's dashboard lands a moment after consent: the Machine asks the control
plane for it itself while it waits (fleet.py connects_watch), apart from the Fleet's loop, which a Shared Graph round
after a restart kept busy for over a minute. One pickup at a time. The dashboard's reads write nothing
that did not change (fleet.Fleet.keep_meta), so a database another writer holds is no crash there, and no sync error
(assistant.db_busy). No live calls."""
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant
import fleet
import network_crypto as nc
import service
from test_device_connect import context, fleet_with


def sealed(f, cid, body):
    return {'id': cid, 'sealed': nc.seal_box(body, nc.unb64(nc.public_keys(f.private)['box'], 32), context('dev_1', cid))}


BODY = {'command': 'connect', 'args': {'source': 'microsoft_docs', 'grant': {'provider': 'microsoft', 'email': 'dee@acme.example',
                                                                             'refresh_token': 'fixture-refresh'}}}


class Watch(unittest.TestCase):
    def test_a_waiting_sign_in_is_picked_up_without_the_inbox_hint_then_the_watch_ends(self):
        f = fleet_with(self, [])
        f.connect_start('microsoft_docs')  # no watch_connects here: nothing runs by itself
        self.assertFalse(f.connects_due)
        waits = []

        def wait(seconds):  # the grant lands at the control plane after the second ask
            waits.append(seconds)
            if len(waits) == 2:
                f.relay.items = [sealed(f, 'dc_1', BODY)]
        f.connects_watch(wait=wait)
        self.assertEqual(f.got, [BODY])
        self.assertEqual(waits, [fleet.CONNECTS_WATCH_EVERY] * 3)  # ended once it was done
        self.assertEqual([c[1] for c in f.relay.calls].count('/connects'), 4)  # three asks and the result
        self.assertEqual(f.signin_state('microsoft_docs')['state'], 'done')

    def test_nothing_is_asked_when_no_sign_in_waits_or_after_the_watch_time(self):
        f = fleet_with(self, [])
        f.connects_watch(wait=lambda s: self.fail('no wait'))
        self.assertEqual(f.relay.calls, [])
        f.connect_start('intercom')
        calls = len(f.relay.calls)
        clock = iter([0, 1, fleet.CONNECTS_WATCH_FOR + 1])
        f.connects_watch(wait=lambda s: None, clock=lambda: next(clock))
        self.assertEqual(len(f.relay.calls), calls + 1)  # one ask, then the time was up: the inbox hint covers the rest
        self.assertFalse(f.signin_waiting(clock=lambda: time.time() + fleet.CONNECTS_WATCH_FOR + 1))

    def test_connect_start_watches_in_its_own_thread_on_a_machine_that_asks_for_it(self):
        f = fleet_with(self, [])
        f.watch_connects = True
        delivered = threading.Event()
        f.connect_delivered = lambda body: delivered.set() or {'ok': True, 'name': 'dee@acme.example'}
        with patch.object(fleet, 'CONNECTS_WATCH_EVERY', 0.02):
            f.connect_start('microsoft_docs')
            self.assertFalse(f.connects_watch_start())  # one watch at a time
            f.relay.items = [sealed(f, 'dc_1', BODY)]  # consent given: sealed for this Machine
            started = time.monotonic()
            self.assertTrue(delivered.wait(5))
            self.assertLess(time.monotonic() - started, 2)
            # the watch ends once nothing waits. Still at the short interval: outside it, the watch's last wait is the
            # real one (2 s), and on a busy machine it outlives a short poll and then finds its database gone.
            until = time.monotonic() + 10
            while f.connects_watch_lock.locked() and time.monotonic() < until:
                time.sleep(0.02)
        self.assertFalse(f.connects_watch_lock.locked())

    def test_the_app_asks_for_the_watch_where_it_takes_connects(self):
        source = Path(assistant.__file__).read_text()
        self.assertIn('self.fleet.connect_delivered = self.fleet_connect_delivered', source)
        self.assertIn('self.fleet.watch_connects = True', source)

    def test_one_pickup_at_a_time_and_a_hint_stays_due(self):
        f = fleet_with(self, [])
        f.relay.items = [sealed(f, 'dc_1', BODY)]
        f.connects_due = True
        f.connects_lock = threading.Lock()
        with f.connects_lock:  # the watch is picking up right now
            self.assertEqual(f.connects_round(), [])
        self.assertTrue(f.connects_due)
        self.assertEqual(f.relay.calls, [])
        self.assertEqual(f.connects_round(), ['dc_1'])
        self.assertEqual(f.got, [BODY])


class Restart(unittest.TestCase):
    def test_the_restart_after_a_new_connection_fires_on_time(self):
        ran = []
        with patch.object(service, 'manager', return_value='systemd'), patch('shutil.which', return_value='/usr/bin/systemd-run'), \
                patch.object(service, 'default_run', side_effect=lambda command, timeout: ran.append(command) or type('R', (), {'returncode': 0})()):
            self.assertTrue(service.restart_later('personal-assistant.service', 3))
        [command] = ran
        self.assertIn('--on-active=3', command)
        self.assertIn('--timer-property=AccuracySec=100ms', command)  # a user manager's default is a minute


class Busy(unittest.TestCase):
    def test_a_statement_kept_already_is_not_written_again(self):
        box = fleet_with(self, [])
        writes = []
        box.set_meta = lambda key, value: writes.append((key, value))
        statement = {'t': 'pause', 'fleet': 'f1', 'on': False, 'at': '2026-10-30T10:00:00+00:00'}
        box.keep_meta('graph_pause:f1', dict(statement), statement)
        box.keep_meta('trust:f1', {'a1': ['k', 1]}, {'a1': ('k', 1)})  # as JSON gives it back
        self.assertEqual(writes, [])  # the dashboard's read writes nothing when nothing changed
        box.keep_meta('graph_pause:f1', None, statement)
        self.assertEqual(writes, [('graph_pause:f1', statement)])

        def locked(key, value):
            raise sqlite3.OperationalError('database is locked')
        box.set_meta = locked
        with self.assertRaises(sqlite3.OperationalError):  # a change that cannot be kept is never dropped quietly
            box.keep_meta('graph_pause:f1', None, statement)

    def test_a_locked_database_is_transient_for_a_sync_no_error_and_soon_again(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        store = assistant.Store(Path(temp.name) / 'events.sqlite')
        account = {'id': 'work-outlook', 'email': 'owner@example.com', 'service': 'outlook', 'transport': 'broker'}
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {}, store, threading.Event()
        waits = []
        app.stop.wait = lambda seconds: waits.append(seconds) or app.stop.set() or True
        with patch.object(app, 'resume_wait', return_value=0), \
                patch.object(assistant, 'sync_source', side_effect=sqlite3.OperationalError('database is locked')):
            app.collector(account)
        self.assertEqual(waits, [assistant.DB_BUSY_RETRY])
        with store.connect() as db:
            self.assertIsNone(db.execute('SELECT error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone())
            self.assertEqual(db.execute("SELECT COUNT(*) FROM error_feed WHERE source='sync'").fetchone()[0], 0)
        self.assertTrue(assistant.db_busy(sqlite3.OperationalError('database is locked')))
        self.assertFalse(assistant.db_busy(sqlite3.OperationalError('no such column: x')))


if __name__ == '__main__':
    unittest.main()

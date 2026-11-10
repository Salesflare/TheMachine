"""The status is built once and kept until the database or config changes (StatusApp.status_kept): the dashboard asks
on every load, poll and action, from each open tab, and each one was built in full (half a second quiet, up to half a
minute on a busy Machine). What changes without them (the model's state, reviews running, the heartbeat) is fresh on
every ask, and what only Settings shows comes from api/settings, not the status."""
import datetime as dt
import sqlite3
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant as a

NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
WORK = {'id': 'work', 'email': 'owner@acme.example', 'service': 'gmail', 'boundary': 'work:Acme'}
SETTINGS_ONLY = ('agents_settings', 'signatures', 'lookups', 'own_addresses')


def mail(n):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=n)).isoformat(),
            'title': f'Mail {n}', 'body': 'Hello', 'deleted': False,
            'metadata': {'from': f'Sam Lee <sam{n}@client.example>', 'to': 'owner@acme.example', 'labels': ['INBOX'], 'thread_id': f't{n}'}}


class StatusKept(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.config_path, self.app.config = self.store, None, {'accounts': [WORK]}
        self.builds, built = [], self.app.status_built

        def counted(done):
            self.builds.append(done)
            return built(done)
        self.app.status_built = counted
        self.status(); self.status(); self.builds.clear()  # a new database's first build makes its tables: one more build
        self.addCleanup(lambda: (self.app.__dict__.get('_status_kept') or {}).get('watch') and self.app._status_kept['watch'].close())

    def status(self):
        return self.app.action('status', {'full': True, 'done': 25})

    def test_asked_again_without_a_change_it_is_built_once(self):
        first = self.status()
        for _ in range(4):
            self.assertEqual(self.status(), first)
        self.assertEqual(self.builds, [])
        self.app.action('status', {'full': True})  # another Done page (the CLI): its own build
        self.assertEqual(self.builds, [None])

    def test_a_change_in_the_database_builds_it_again(self):
        self.status()
        self.store.commit_page('work', {}, [mail(1)])  # this process
        self.status(); self.assertEqual(len(self.builds), 1)
        self.status(); self.assertEqual(len(self.builds), 1)
        with sqlite3.connect(self.store.path) as db:  # another process (a worker)
            db.execute("UPDATE events SET title='Mail one' WHERE source_id='m1'")
        self.status(); self.assertEqual(len(self.builds), 2)

    def test_a_config_change_or_the_next_minute_builds_it_again(self):
        self.status()
        self.app.config['owner_name'] = 'Pat'
        self.status(); self.assertEqual(len(self.builds), 1)
        with patch('machine.app.status.now', return_value='2099-01-01T00:00:00+00:00'):
            self.status(); self.assertEqual(len(self.builds), 2)

    def test_what_changes_in_memory_is_fresh_without_a_build(self):
        self.status()
        self.app.model_usage = {'used': 42}
        out = self.status()
        self.assertEqual(out['model_usage'], {'used': 42})
        self.assertEqual(self.builds, [])
        out['review_health']['marked'] = True  # a caller changing its copy leaves the kept one alone
        self.assertNotIn('marked', self.status()['review_health'])

    def test_requests_at_once_share_one_build(self):
        built = self.app.status_built

        def slow(done):
            time.sleep(0.3)
            return built(done)
        self.app.status_built = slow
        self.store.commit_page('work', {}, [mail(1)])  # something new: one build is due
        start, out = threading.Barrier(6), []

        def ask():
            start.wait(); out.append(self.status())
        threads = [threading.Thread(target=ask) for _ in range(6)]
        for t in threads: t.start()
        for t in threads: t.join(10)
        self.assertEqual(len(out), 6)
        self.assertEqual(len(self.builds), 1, 'six tabs asking at once: one build')

    def test_settings_only_parts_come_from_settings_views(self):
        status = self.status()
        for key in SETTINGS_ONLY:
            self.assertNotIn(key, status)
        self.assertEqual(set(self.app.settings_views()), set(SETTINGS_ONLY))

    def test_without_a_database_file_nothing_is_kept(self):
        self.builds.clear()
        self.app.store = type('Bare', (), {'path': None, '__getattr__': lambda s, n: getattr(self.store, n)})()
        self.status(); self.status()
        self.assertEqual(len(self.builds), 2)


if __name__ == '__main__':
    unittest.main()

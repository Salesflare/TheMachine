"""A service's own 5xx or 429 on a sync (assistant.App.sync_retrying, Store.failed): one quick retry, then the normal
wait; no error report unless it keeps happening (TRANSIENT_REPORT_AFTER). A 401 or 403 is reported at once."""
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant


class ServiceBusy(unittest.TestCase):
    """A service's own 5xx or 429 is its hiccup: one quick retry, no error report unless it keeps happening."""

    def app(self, effects):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop = {}, assistant.Store(Path(temp.name) / 'events.sqlite'), threading.Event()
        self.waits, self.calls = [], []
        effects = list(effects)

        def wait(seconds):
            self.waits.append(seconds)
            if len(self.waits) > 1 and not effects:
                app.stop.set()
            return app.stop.is_set()
        app.stop.wait = wait

        def sync(store, config, account):
            self.calls.append(account['id'])
            effect = effects.pop(0) if effects else None
            if effect is None:
                app.stop.set()  # the round after: done
                raise assistant.SourceError('network:URLError:stop')
            if isinstance(effect, Exception):
                raise effect
            return effect
        return app, sync

    def feed(self, app):
        with app.store.connect() as db:
            return db.execute("SELECT COUNT(*) FROM error_feed WHERE source='sync'").fetchone()[0]

    def test_a_single_503_is_retried_shortly_and_records_no_error(self):
        account = {'id': 'salesflare-google-meet', 'service': 'google_meet'}
        app, sync = self.app([assistant.SourceError('google_meet_http', 503), {'mode': 'incremental', 'events': 0}])
        with patch.object(app, 'resume_wait', return_value=0), patch.object(assistant, 'sync_source', side_effect=sync):
            result = app.sync_retrying(account)
        self.assertEqual(result['mode'], 'incremental')
        self.assertEqual(self.calls, [account['id']] * 2)
        self.assertEqual(self.waits, [assistant.QUICK_RETRY_SECONDS])
        self.assertEqual(self.feed(app), 0)

    def test_a_short_retry_after_is_honored(self):
        account = {'id': 'work-trello', 'service': 'trello'}
        app, sync = self.app([assistant.SourceError('trello_http', 429, retry_after=30), {'mode': 'incremental', 'events': 0}])
        with patch.object(assistant, 'sync_source', side_effect=sync):
            app.sync_retrying(account)
        self.assertEqual(self.waits, [30])

    def test_a_long_retry_after_waits_in_the_checkpoint_instead(self):
        account = {'id': 'work-trello', 'service': 'trello'}
        app, sync = self.app([assistant.SourceError('trello_http', 429, retry_after=900)])
        with patch.object(assistant, 'sync_source', side_effect=sync), self.assertRaises(assistant.SourceError):
            app.sync_retrying(account)
        self.assertEqual((self.calls, self.waits), ([account['id']], []))

    def test_a_second_503_waits_for_the_next_round_unreported(self):
        account = {'id': 'salesflare-google-meet', 'service': 'google_meet', 'poll_seconds': 300}
        app, sync = self.app([assistant.SourceError('google_meet_http', 503), assistant.SourceError('google_meet_http', 503)])
        with patch.object(app, 'resume_wait', return_value=0), patch.object(assistant, 'sync_source', side_effect=sync):
            app.collector(account)
        self.assertEqual(self.waits[:2], [assistant.QUICK_RETRY_SECONDS, 300])
        self.assertEqual(self.feed(app), 0)
        with app.store.connect() as db:
            self.assertEqual(db.execute('SELECT error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()[0],
                             'google_meet_http:HTTP_503')  # the connection says the service had a problem, retrying

    def test_a_permission_error_is_not_retried_and_is_reported(self):
        for status in (401, 403):
            account = {'id': 'work-trello', 'service': 'trello'}
            app, sync = self.app([assistant.SourceError('trello_http', status)])
            with patch.object(app, 'resume_wait', return_value=0), patch.object(assistant, 'sync_source', side_effect=sync):
                app.collector(account)
            self.assertEqual(self.calls, [account['id']])  # no quick retry: it waits for the next round
            self.assertNotIn(assistant.QUICK_RETRY_SECONDS, self.waits)
            self.assertEqual(self.feed(app), 1, status)


if __name__ == '__main__':
    unittest.main()

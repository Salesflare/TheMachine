"""Store.keep_found: mail a run's search finds is context (reviewed), unless it came in after the account's last sync.
A test persona's accountant asked for receipts a minute after the first look; a run's mailbox search found that mail
before the next sync did, kept it as reviewed, and the sync then skipped it as already collected: no to-do, ever."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402,F401

spec = importlib.util.spec_from_file_location('keep_found_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def mail(source_id, when):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'title': 'Missing receipts for the quarter',
            'occurred_at': when.isoformat(), 'body': 'Please send the three receipts by Wednesday.', 'deleted': False,
            'metadata': {'from': 'Accountant <books@example.com>', 'thread_id': source_id, 'labels': ['INBOX']}}


class KeepFoundNews(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)

    def state(self, source_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT analyzed_version,version FROM events WHERE source_id=?', (source_id,)).fetchone())

    def test_mail_after_the_last_sync_stays_for_the_review(self):
        self.store.commit_page('work', {'cursor': 1}, [mail('old', self.now - dt.timedelta(days=3))])
        [new] = self.store.keep_found('work', [mail('new', self.now + dt.timedelta(minutes=2))])
        self.assertEqual(self.state('new'), {'analyzed_version': 0, 'version': 1})
        # the sync reaches it later and skips it as collected: it is still waiting for the review
        self.store.commit_page('work', {'cursor': 2}, [mail('new', self.now + dt.timedelta(minutes=2))])
        self.assertEqual(self.state('new')['analyzed_version'], 0)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT id FROM events WHERE source_id=?', ('new',)).fetchone()[0], new)

    def test_old_mail_a_run_looks_up_is_context(self):
        self.store.commit_page('work', {'cursor': 1}, [])
        self.store.keep_found('work', [mail('weeks', self.now - dt.timedelta(days=30))])
        self.assertEqual(self.state('weeks'), {'analyzed_version': 1, 'version': 1})

    def test_before_any_sync_what_is_found_is_context(self):
        self.store.keep_found('work', [mail('first', self.now)])
        self.assertEqual(self.state('first'), {'analyzed_version': 1, 'version': 1})


if __name__ == '__main__':
    unittest.main()

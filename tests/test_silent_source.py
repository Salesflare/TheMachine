import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest
import uuid
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_silent', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

PHONE = {'id': 'phone', 'service': 'android', 'boundary': 'personal', 'node_id': 'node', 'poll_seconds': 15}
NOW = dt.datetime(2026, 11, 6, 12, 0, tzinfo=dt.timezone.utc)
iso = lambda d: d.isoformat()


class ConnectedButSilent(unittest.TestCase):
    """The notification feed answers (every poll "succeeds") while the phone itself is offline: the direct read keeps
    failing and nothing new comes in. The card must say the phone is disconnected, not stay green, and clear by itself."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        patcher = patch_everywhere(a, 'now', side_effect=lambda: iso(NOW))
        patcher.start()
        self.addCleanup(patcher.stop)

    def notifications(self, account, start, end, every=dt.timedelta(minutes=20)):
        events, at = [], start
        while at <= end:
            ms = int(at.timestamp() * 1000)
            events.append(a.android_event(account, {'key': f'k{ms}', 'packageName': 'com.example.app', 'postTimeMs': ms, 'title': 'Hi'}))
            at += every
        self.store.commit_page(account['id'], {}, events)

    def log(self, account, at, status, error=None):
        with self.store.connect() as db:
            db.execute('INSERT INTO sync_activity VALUES(?,?,?,?,?,?,?)', (uuid.uuid4().hex, account['id'], iso(at), status, 0, error, None))

    def offline_reads(self, account, hours=5, error='android_offline', end=NOW):
        for minutes in range(0, hours * 60, 10):  # the direct read every 10 minutes, the feed polls in between
            self.log(account, end - dt.timedelta(minutes=minutes), 'failed', error)
            self.log(account, end - dt.timedelta(minutes=minutes, seconds=15), 'success')

    def card(self, account=PHONE):
        return next(c for c in self.store.snapshot([account])['connectors'] if c['id'] == account['id'])

    def test_the_phone_goes_offline_and_its_card_says_so(self):
        self.notifications(PHONE, NOW - dt.timedelta(days=7), NOW - dt.timedelta(hours=5))
        self.offline_reads(PHONE)
        card = self.card()
        self.assertEqual(card['error'], 'android_offline')
        self.assertEqual(card['silent_since'][:16], iso(NOW - dt.timedelta(hours=5))[:16])
        self.assertEqual(a.compact_status({**self.store.snapshot([PHONE]), 'suggestions': [], 'decisions': [], 'analyses': []})['connectors'][0]['error'],
                         'android_offline')  # the agent sees it too

    def test_it_recovers_once_notifications_arrive_again(self):
        self.notifications(PHONE, NOW - dt.timedelta(days=7), NOW - dt.timedelta(hours=5))
        self.offline_reads(PHONE)
        self.notifications(PHONE, NOW - dt.timedelta(minutes=5), NOW - dt.timedelta(minutes=5))
        self.assertNotIn('silent_since', self.card())
        self.assertIsNone(self.card()['error'])

    def test_it_recovers_once_the_reads_stop_failing(self):
        self.notifications(PHONE, NOW - dt.timedelta(days=7), NOW - dt.timedelta(hours=5))
        self.offline_reads(PHONE)
        with self.store.connect() as db:
            db.execute("DELETE FROM sync_activity WHERE status='failed' AND at>?", (iso(NOW - dt.timedelta(hours=1, minutes=5)),))
        self.assertNotIn('silent_since', self.card())

    def test_failing_reads_while_notifications_still_arrive_stay_green(self):
        self.notifications(PHONE, NOW - dt.timedelta(days=7), NOW)
        self.offline_reads(PHONE)
        self.assertNotIn('silent_since', self.card())

    def test_a_quiet_stretch_like_its_usual_nights_is_not_an_outage(self):
        # notifications every 20 minutes by day, none from 22:00 to 06:00: an 8 hour quiet night is normal for it
        for day in range(7, 0, -1):
            start = (NOW - dt.timedelta(days=day)).replace(hour=6, minute=0)
            self.notifications(PHONE, start, start.replace(hour=22))
        at = (NOW - dt.timedelta(days=1)).replace(hour=22, minute=0)
        self.offline_reads(PHONE, hours=14)
        with self.store.connect() as db:
            self.assertIsNone(a.silent_failure(db, PHONE, {'error': None}, iso(at + dt.timedelta(hours=5))))
            # past its usual night it shows
            self.assertTrue(a.silent_failure(db, PHONE, {'error': None}, iso(NOW)))

    def test_sources_quiet_by_nature_are_left_alone(self):
        github = {'id': 'gh', 'service': 'github', 'boundary': 'work'}
        x = {'id': 'x', 'service': 'x', 'boundary': 'work', 'active_hours': [13, 14]}
        for account in (github, x):
            self.store.commit_page(account['id'], {}, [])
            self.offline_reads(account, error='timeout')
        # GitHub: a few notifications a week
        self.store.commit_page('gh', {}, [{'account_id': 'gh', 'source_id': f'g{i}', 'kind': 'github.notification',
                                           'occurred_at': iso(NOW - dt.timedelta(days=i + 1)), 'title': 'PR', 'body': '',
                                           'deleted': False, 'metadata': {}} for i in range(5)])
        self.assertNotIn('silent_since', self.card(github))
        self.assertNotIn('silent_since', self.card(x))  # reads only in set hours

    def test_an_error_already_showing_stays_as_it_is(self):
        self.notifications(PHONE, NOW - dt.timedelta(days=7), NOW - dt.timedelta(hours=5))
        self.offline_reads(PHONE)
        with self.store.connect() as db:
            db.execute("UPDATE checkpoints SET error='android_feed_unavailable' WHERE account_id=?", (PHONE['id'],))
        card = self.card()
        self.assertEqual(card['error'], 'android_feed_unavailable')
        self.assertNotIn('silent_since', card)


if __name__ == '__main__':
    unittest.main()

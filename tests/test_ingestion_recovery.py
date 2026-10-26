"""Provider catch-up and X lease regression cases. Disposable DBs/leases; no live calls."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
import urllib.parse
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


a = load('recovery_assistant', ROOT / 'assistant.py')
x = load('recovery_x', ROOT / 'integrations/x_inbox.py')
GITHUB = {'id': 'github', 'service': 'github', 'login': 'owner', 'boundary': 'work'}
STRIPE = {'id': 'stripe', 'service': 'stripe', 'boundary': 'work'}
NOW = '2026-10-16T12:00:00+00:00'


def github_sync(store, source):
    if hasattr(a, 'sync_github'):
        return a.sync_github(store, {}, GITHUB, source)
    return a.load_connector('github').sync(store, {}, GITHUB, a.CONNECTOR_HELPERS, source)


def stripe_sync(store, source):
    if hasattr(a, 'sync_stripe'):
        return a.sync_stripe(store, {}, STRIPE, source)
    return a.load_connector('stripe').sync(store, {}, STRIPE, a.CONNECTOR_HELPERS, source)


class GitHubPages:
    def __init__(self, count):
        end = dt.datetime.fromisoformat(NOW) - dt.timedelta(seconds=1)
        self.items = [{'id': str(i), 'reason': 'mention',
                      'updated_at': (end - dt.timedelta(seconds=i)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                      'repository': {'full_name': 'example/app'}, 'subject': {'title': f'Mention {i}', 'type': 'Issue'}}
                     for i in range(count)]
        self.calls, self.fail_page = [], None

    def verify(self):
        pass

    def get(self, path):
        self.calls.append(path)
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(path).query)
        page = int(q['page'][0])
        if page == self.fail_page:
            raise a.SourceError('network')
        rows = sorted((n for n in self.items if q['since'][0] <= n['updated_at'] <= q['before'][0]),
                      key=lambda n: n['updated_at'], reverse=True)
        return rows[(page - 1) * 50:page * 50]


class StripePages:
    def __init__(self, count):
        self.items = [{'id': f'evt_{i}', 'type': 'invoice.payment_failed', 'created': 1792151999 - i,
                       'data': {'object': {'id': f'in_{i}', 'customer_name': 'Synthetic Customer',
                                          'amount_due': 1000, 'currency': 'eur'}}} for i in range(count)]
        self.calls, self.fail_cursor = [], None

    def verify(self):
        pass

    def customer(self, _):
        return {}

    def get(self, path, params):
        self.calls.append(dict(params))
        if self.fail_cursor and params.get('starting_after') == self.fail_cursor:
            raise a.SourceError('network')
        rows = sorted((n for n in self.items if params['created[gte]'] <= n['created'] <= params['created[lte]']),
                      key=lambda n: n['created'], reverse=True)
        start = next((i + 1 for i, n in enumerate(rows) if n['id'] == params.get('starting_after')), 0)
        return {'data': rows[start:start + 100], 'has_more': len(rows) > start + 100}


class CatchUp(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'events.sqlite'
        self.store = a.Store(self.path)
        self.store.commit_page('github', {'since': '2026-10-16T11:00:00Z'}, [])
        self.store.commit_page('stripe', {'since': 1792140000}, [])
        clock = patch.object(a, 'now', return_value=NOW)
        clock.start(); self.addCleanup(clock.stop)

    def reopen(self):
        self.store = a.Store(self.path)

    def count(self, account):
        with self.store.connect() as db:
            return db.execute('SELECT count(*) FROM events WHERE account_id=?', (account,)).fetchone()[0]

    def test_github_backlog_resumes_after_restart_and_freezes_the_window(self):
        source = GitHubPages(300)
        self.assertTrue(github_sync(self.store, source)['more'])
        saved = self.store.checkpoint('github')
        self.assertEqual((self.count('github'), saved['since'], saved['catchup']['page']),
                         (250, '2026-10-16T11:00:00Z', 6))
        self.assertFalse(saved['coverage_complete'])
        source.items.insert(0, {**source.items[0], 'id': 'newer', 'updated_at': '2026-10-16T12:01:00Z'})
        self.reopen()
        self.assertFalse(github_sync(self.store, source)['more'])
        self.assertEqual(self.count('github'), 300)
        self.assertNotIn('catchup', self.store.checkpoint('github'))
        self.assertTrue(self.store.checkpoint('github')['coverage_complete'])
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(next(path for path in source.calls if urllib.parse.parse_qs(urllib.parse.urlsplit(path).query)['page'] == ['6'])).query)
        self.assertEqual((q['page'], q['before']), (['6'], ['2026-10-16T12:00:00Z']))
        with patch.object(a, 'now', return_value='2026-10-16T12:02:00+00:00'):
            github_sync(self.store, source)
        self.assertEqual(self.count('github'), 301)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT max(version) FROM events').fetchone()[0], 1)

    def test_github_shifted_pages_replay_without_losing_older_notifications(self):
        for during_read in (False, True):
            with self.subTest(during_read=during_read):
                self.path = Path(self.tmp.name) / ('during' if during_read else 'before')
                self.store = a.Store(self.path)
                self.store.commit_page('github', {'since': '2026-10-16T11:00:00Z'}, [])
                source = GitHubPages(300)
                self.assertTrue(github_sync(self.store, source)['more'])
                original_get = source.get
                moved = False
                def move_earlier():
                    nonlocal moved
                    for item in source.items[:5]:
                        item['updated_at'] = '2026-10-16T12:01:00Z'
                    moved = True
                def get(path):
                    if during_read and 'page=6&' in path and not moved:
                        move_earlier()
                    return original_get(path)
                source.get = get
                if not during_read:
                    move_earlier()
                self.reopen()
                for _ in range(10):
                    if not github_sync(self.store, source)['more']:
                        break
                else:
                    self.fail('stable window did not drain')
                self.assertEqual(self.count('github'), 300)
                self.assertNotIn('catchup', self.store.checkpoint('github'))

    def test_github_failed_later_page_preserves_committed_page(self):
        source = GitHubPages(90); source.fail_page = 2
        with self.assertRaises(a.SourceError):
            github_sync(self.store, source)
        self.assertEqual((self.count('github'), self.store.checkpoint('github')['catchup']['page']), (50, 2))
        self.reopen(); source.fail_page = None
        github_sync(self.store, source)
        self.assertEqual(self.count('github'), 90)

    def test_stripe_backlog_resumes_after_restart(self):
        source = StripePages(1100)
        self.assertTrue(stripe_sync(self.store, source)['more'])
        state = self.store.checkpoint('stripe')
        self.assertEqual((self.count('stripe'), state['since'], state['catchup']['cursor']), (1000, 1792140000, 'evt_999'))
        self.assertFalse(state['coverage_complete'])
        self.reopen()
        self.assertFalse(stripe_sync(self.store, source)['more'])
        self.assertTrue(self.store.checkpoint('stripe')['coverage_complete'])
        self.assertEqual(self.count('stripe'), 1100)
        self.assertEqual(source.calls[10]['starting_after'], 'evt_999')
        self.assertEqual(source.calls[10]['created[lte]'], source.calls[0]['created[lte]'])

    def test_stripe_later_same_second_is_collected_without_duplicates(self):
        source = StripePages(1)
        stripe_sync(self.store, source)
        source.items.append({**source.items[0], 'id': 'evt_same_second'})
        self.reopen()
        stripe_sync(self.store, source)
        stripe_sync(self.store, source)
        self.assertEqual(self.count('stripe'), 2)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT max(version) FROM events').fetchone()[0], 1)

    def test_stripe_failed_later_page_keeps_receipts_and_cursor(self):
        source = StripePages(150); source.fail_cursor = 'evt_99'
        with self.assertRaises(a.SourceError):
            stripe_sync(self.store, source)
        self.assertEqual((self.count('stripe'), self.store.checkpoint('stripe')['catchup']['cursor']), (100, 'evt_99'))
        self.reopen(); source.fail_cursor = None
        stripe_sync(self.store, source)
        self.assertEqual(self.count('stripe'), 150)

    def test_checkpoint_does_not_advance_if_event_commit_fails(self):
        commit = self.store.commit_page
        def fail(account, state, events, **kwargs):
            if events:
                raise RuntimeError('synthetic disk failure')
            return commit(account, state, events, **kwargs)
        for account, sync, source in [('github', github_sync, GitHubPages(70)), ('stripe', stripe_sync, StripePages(150))]:
            before = self.store.checkpoint(account)
            with patch.object(self.store, 'commit_page', side_effect=fail), self.assertRaises(RuntimeError):
                sync(self.store, source)
            self.assertEqual(self.store.checkpoint(account), before)
            self.assertEqual(self.count(account), 0)

    def test_x_partial_coverage_is_visible_until_the_cursor_is_drained(self):
        account = {'id': 'x', 'service': 'x', 'handle': 'Owner', 'transport': 'x-inbox', 'boundary': 'personal'}
        pending = {'cursor': 'bottom', 'since_id': '1', 'top': '5', 'since_ms': 0}
        data = {'account': {'screen_name': 'Owner'}, 'mentions': [], 'dms': [], 'state': {'mention_catchup': pending}}
        source = types.SimpleNamespace(page=lambda since, state: data)
        def sync():
            if hasattr(a, 'sync_x'):
                return a.sync_x(self.store, {}, account, source)
            return a.load_connector('x').sync(self.store, {}, account, a.CONNECTOR_HELPERS, source)
        self.assertTrue(sync()['more'])
        saved = self.store.checkpoint('x')
        self.assertFalse(saved['coverage_complete'])
        self.assertEqual(saved['page']['mention_catchup'], pending)
        self.reopen(); data['state'] = {'mention_since_id': '5'}
        self.assertFalse(sync()['more'])
        self.assertTrue(self.store.checkpoint('x')['coverage_complete'])


class XLease(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.api = load('disposable_x_lease', x.LEASE)
        self.api.STATE = Path(self.tmp.name) / 'lease.json'
        self.api.LOCK = Path(self.tmp.name) / 'lease.lock'
        lease = patch.object(x, 'LEASE_API', self.api); lease.start(); self.addCleanup(lease.stop)
        # The tab list and its lock would otherwise be the real ones, shared with a live inbox run on this computer.
        for name, value in (('OPEN_TABS', Path(self.tmp.name) / 'x-inbox-tabs'), ('CDP', '')):
            patcher = patch.object(x, name, value); patcher.start(); self.addCleanup(patcher.stop)
        cli = patch.object(x.subprocess, 'run', side_effect=self.cli); cli.start(); self.addCleanup(cli.stop)
        self.browser_calls = []

    def cli(self, args, **kwargs):
        action = args[2]
        if action == 'release':
            state = self.api.read(); state['holders'].pop(x.OWNER, None); self.api.save(state)
            return subprocess.CompletedProcess(args, 0, '', '')
        if action == 'status':
            return subprocess.CompletedProcess(args, 0, self.api.describe(self.api.read()) or 'free', '')
        granted, state = self.api.claim(x.OWNER, 10, exclusive=False)
        return subprocess.CompletedProcess(args, 0 if granted else 3, self.api.describe(state), '')

    def browser(self, *args, **kwargs):
        self.browser_calls.append(args)
        if args[0] == 'open':
            self.assertFalse(self.api.try_claim('another-browser-job', 10, False)[0])
            self.assertTrue(self.api.read()['holders'][x.OWNER]['exclusive'])
            return 'id: own-tab'
        return ''

    def test_account_switch_holds_atomic_custody_through_cleanup(self):
        def work(_):
            self.assertFalse(self.api.try_claim('another-browser-job', 10, False)[0])
            return 'done'
        with patch.object(x, 'oc', side_effect=self.browser):
            self.assertEqual(x.with_tab(x.NEUTRAL_URL, work, switching=True), 'done')
        self.assertEqual(self.browser_calls[-1], ('close', 'own-tab'))
        self.assertFalse(self.api.read()['holders'])
        self.assertTrue(self.api.try_claim('another-browser-job', 10, False)[0])

    def test_existing_shared_owner_prevents_switch_without_opening_tab(self):
        self.api.try_claim('existing-job', 10, False)
        with patch.object(x, 'oc') as browser, self.assertRaises(x.Fail):
            x.with_tab(x.NEUTRAL_URL, lambda _: self.fail('must not run'), switching=True)
        browser.assert_not_called()
        self.assertEqual(set(self.api.read()['holders']), {'existing-job'})

    def test_exception_still_closes_own_tab_and_releases_custody(self):
        with patch.object(x, 'oc', side_effect=self.browser), self.assertRaises(ValueError):
            x.with_tab(x.NEUTRAL_URL, lambda _: (_ for _ in ()).throw(ValueError('synthetic')), switching=True)
        self.assertEqual(self.browser_calls[-1], ('close', 'own-tab'))
        self.assertFalse(self.api.read()['holders'])

    def test_primary_read_also_reserves_account_restoration(self):
        lock = types.SimpleNamespace(close=lambda: None)
        with patch.object(x, 'one_at_a_time', return_value=lock), patch.object(x, 'with_tab', return_value={}) as tabs:
            x.run('sync', handle='Owner', primary='Owner')
        self.assertTrue(tabs.call_args.args[2])
        with patch.object(x, 'one_at_a_time', return_value=lock), patch.object(x, 'with_tab', return_value={}) as tabs:
            x.run('accounts')
        self.assertFalse(tabs.call_args.args[2])


if __name__ == '__main__':
    unittest.main()

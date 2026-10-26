"""GitHub and Stripe connector plugins: read-only, relevant events only, replays add nothing. No live calls."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant_gh_stripe', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
stripe, github = a.load_connector('stripe'), a.load_connector('github')
H = a.CONNECTOR_HELPERS

STRIPE = {'id': 'test-stripe', 'service': 'stripe', 'transport': 'maton', 'credential': 'maton', 'credential_variable': 'KEY',
          'connection_id': 'conn-1', 'stripe_account': 'acct_1', 'boundary': 'work'}
GITHUB = {'id': 'test-github', 'service': 'github', 'transport': 'gh', 'login': 'Owner', 'boundary': 'work'}


def sub(sub_id, amount, interval='month', **extra):
    return {'id': sub_id, 'customer': 'cus_1', 'currency': 'eur', 'status': 'active',
            'items': {'data': [{'quantity': 2, 'price': {'unit_amount': amount, 'currency': 'eur', 'recurring': {'interval': interval}}}]}, **extra}


STRIPE_EVENTS = [  # newest first, as Stripe returns them
    {'id': 'evt_5', 'type': 'customer.subscription.created', 'created': 1792000500, 'livemode': True, 'data': {'object': sub('sub_big', 30000)}},
    {'id': 'evt_4', 'type': 'customer.subscription.created', 'created': 1792000400, 'livemode': True, 'data': {'object': sub('sub_small', 2000)}},
    {'id': 'evt_3', 'type': 'customer.subscription.updated', 'created': 1792000300, 'livemode': True,
     'data': {'object': sub('sub_a', 120000, 'year', cancel_at_period_end=True, cancel_at=1794600000), 'previous_attributes': {'cancel_at_period_end': False}}},
    {'id': 'evt_2', 'type': 'customer.subscription.updated', 'created': 1792000200, 'livemode': True,
     'data': {'object': sub('sub_a', 120000, 'year'), 'previous_attributes': {'items': {}}}},
    {'id': 'evt_1', 'type': 'invoice.payment_failed', 'created': 1792000100, 'livemode': True,
     'data': {'object': {'id': 'in_1', 'customer': 'cus_1', 'customer_name': 'Acme BV', 'customer_email': 'billing@acme.example',
                         'amount_due': 3900, 'currency': 'eur', 'attempt_count': 2, 'next_payment_attempt': 1792300000, 'billing_reason': 'subscription_cycle'}}},
]


class FakeStripe(stripe.Source):
    def __init__(self, events, account_id='acct_1'):
        super().__init__({}, STRIPE, H)
        self.events, self.account_id, self.calls = events, account_id, []

    def get(self, path, params=None):
        self.calls.append((path, dict(params or {})))
        if path == 'v1/account':
            return {'id': self.account_id}
        if path == 'v1/events':
            return {'data': [e for e in self.events if params['created[gte]'] <= e['created'] <= params['created[lte]']], 'has_more': False}
        if path.startswith('v1/customers/'):
            return {'name': 'Acme BV', 'email': 'billing@acme.example'}
        raise AssertionError(path)


def notification(n_id, reason, title, updated, number=7, repo='org/app', kind='Issue', comment=True):
    base = f'https://api.github.com/repos/{repo}/{"issues" if kind == "Issue" else "pulls"}/{number}'
    return {'id': n_id, 'reason': reason, 'updated_at': updated, 'repository': {'full_name': repo},
            'subject': {'title': title, 'type': kind, 'url': base,
                        'latest_comment_url': f'https://api.github.com/repos/{repo}/issues/comments/9{n_id}' if comment else base}}


class FakeGitHub(github.Source):
    def __init__(self, notifications, runs=(), account=GITHUB):
        super().__init__({}, account, H)
        self.notifications, self.runs, self.calls = notifications, list(runs), []

    def get(self, path):
        self.calls.append(path)
        if path == 'user':
            return {'login': 'owner'}
        if path.startswith('notifications?'):
            return self.notifications if 'page=1&' in path else []
        if '/issues/comments/' in path:
            return {'user': {'login': 'colleague'}, 'body': 'Can you take a look?', 'html_url': 'https://github.com/org/app/issues/7#issuecomment-1'}
        if '/actions/runs' in path:
            return {'workflow_runs': self.runs}
        if path.startswith('repos/'):
            return {'number': 7, 'state': 'open', 'body': 'The <b>bug</b> report', 'user': {'login': 'reporter'}, 'html_url': 'https://github.com/org/app/issues/7'}
        raise AssertionError(path)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'test.sqlite3')

    def stored(self):
        with self.store.connect() as db:
            return [{**dict(r), 'metadata': json.loads(r['metadata'])} for r in
                    db.execute('SELECT source_id,kind,title,body,metadata,occurred_at,version FROM events ORDER BY occurred_at')]


class Stripe(Base):
    def test_only_relevant_events_become_signals_with_dashboard_links(self):
        source = FakeStripe(STRIPE_EVENTS)
        result = stripe.sync(self.store, {'bootstrap_days': 30000}, STRIPE, H, source)
        self.assertEqual((result['read'], result['events']), (5, 3))
        rows = self.stored()
        self.assertEqual([r['source_id'] for r in rows], ['evt_1', 'evt_3', 'evt_5'])
        failed, cancel, big = rows
        self.assertEqual(failed['title'], 'Payment failed: Acme BV, 39 EUR')
        self.assertIn('Attempt 2; Stripe retries 2026-10-18.', failed['body'])
        self.assertEqual(failed['metadata']['source_url'], 'https://dashboard.stripe.com/invoices/in_1')
        self.assertEqual(failed['metadata']['from'], 'billing@acme.example')
        self.assertEqual(cancel['title'], 'Cancellation scheduled: Acme BV, 200 EUR/month')  # 2 × 1200/year
        self.assertIn('Ends 2026-11-13.', cancel['body'])
        self.assertEqual(big['title'], 'New subscription: Acme BV, 600 EUR/month')
        self.assertEqual(self.store.checkpoint('test-stripe')['since'], 1792000500)
        # Names come from the event when it has one; otherwise one cached lookup, only for relevant events.
        self.assertEqual(sum(1 for path, _ in source.calls if path.startswith('v1/customers/')), 1)

    def test_replay_adds_nothing_and_reads_from_the_checkpoint(self):
        stripe.sync(self.store, {'bootstrap_days': 30000}, STRIPE, H, FakeStripe(STRIPE_EVENTS))
        source = FakeStripe(STRIPE_EVENTS)
        self.assertEqual(stripe.sync(self.store, {}, STRIPE, H, source)['read'], 1)
        self.assertEqual([p['created[gte]'] for path, p in source.calls if path == 'v1/events'], [1792000499])
        self.assertEqual(len(self.stored()), 3)

    def test_wrong_stripe_account_is_refused_before_reading(self):
        source = FakeStripe(STRIPE_EVENTS, account_id='acct_other')
        with self.assertRaises(a.SourceError) as caught:
            stripe.sync(self.store, {}, STRIPE, H, source)
        self.assertEqual(str(caught.exception), 'account_identity_mismatch')
        self.assertEqual([path for path, _ in source.calls], ['v1/account'])

    def test_the_client_only_reads_and_checks_the_connection(self):
        source = stripe.Source({}, STRIPE, H)
        for path in ['v1/refunds', 'v1/subscriptions/sub_1', 'v1/invoices/in_1/pay']:
            with self.subTest(path), self.assertRaises(a.SourceError) as caught:
                source.get(path)
            self.assertEqual(str(caught.exception), 'stripe_path_not_allowed')

        class Response(io.BytesIO):
            def __init__(self, connection):
                super().__init__(b'{"id":"acct_1"}')
                self.headers = {'Maton-Connection': connection}
            def __enter__(self): return self
            def __exit__(self, *_): self.close()

        seen = []
        def opener(connection):
            def urlopen(request, timeout):
                seen.append(request)
                return Response(connection)
            return urlopen
        with patch.object(a, 'credential', return_value='OTHER=x\nKEY=secret\n'), patch('urllib.request.urlopen', opener('conn-1')):
            self.assertEqual(source.get('v1/account'), {'id': 'acct_1'})
        self.assertEqual(seen[0].get_method(), 'GET')
        self.assertEqual(seen[0].get_header('Authorization'), 'Bearer secret')
        self.assertEqual(seen[0].get_header('Maton-connection'), 'conn-1')
        with patch.object(a, 'credential', return_value='KEY=secret'), patch('urllib.request.urlopen', opener('conn-2')):
            with self.assertRaises(a.SourceError) as caught:
                source.get('v1/account')
        self.assertEqual(str(caught.exception), 'connection_identity_mismatch')
        # A restricted key straight to Stripe: same reads, no Maton header to check.
        direct = stripe.Source({}, {**STRIPE, 'transport': 'api', 'credential_variable': None}, H)
        with patch.object(a, 'credential', return_value='restricted-key'), patch('urllib.request.urlopen', opener(None)):
            self.assertEqual(direct.get('v1/account'), {'id': 'acct_1'})
        self.assertEqual(seen[-1].full_url, 'https://api.stripe.com/v1/account')
        self.assertEqual(seen[-1].get_header('Authorization'), 'Bearer restricted-key')
        self.assertIsNone(seen[-1].get_header('Maton-connection'))


class GitHub(Base):
    NOTES = [notification(1, 'comment', 'Login fails on Safari', '2026-10-15T09:00:00Z'),
             notification(2, 'subscribed', 'Watched repo noise', '2026-10-15T10:00:00Z'),
             notification(3, 'review_requested', 'Add export', '2026-10-15T11:00:00Z', number=8, kind='PullRequest', comment=False)]

    def setUp(self):
        super().setUp()
        # The notifications are dated; a fixed clock keeps them inside the 7-day first read on any day.
        clock = patch.object(H, 'now', return_value='2026-10-16T12:00:00+00:00')
        clock.start()
        self.addCleanup(clock.stop)

    def test_participating_notifications_with_thread_detail_and_links(self):
        source = FakeGitHub(self.NOTES)
        self.assertEqual(github.sync(self.store, {}, GITHUB, H, source)['events'], 2)
        issue, pr = self.stored()
        self.assertEqual((issue['source_id'], issue['kind'], issue['title']), ('n:1', 'github.notification', '[app] Login fails on Safari'))
        self.assertIn('Issue in org/app (open); why you got it: comment.', issue['body'])
        self.assertIn('Latest comment by colleague:\nCan you take a look?', issue['body'])
        self.assertEqual(issue['metadata']['source_url'], 'https://github.com/org/app/issues/7#issuecomment-1')
        self.assertEqual((issue['metadata']['from'], issue['metadata']['from_me']), ('colleague', False))
        self.assertIn('why you got it: review requested.', pr['body'])
        self.assertNotIn('Latest comment', pr['body'])
        self.assertEqual(issue['occurred_at'], '2026-10-15T09:00:00+00:00')
        self.assertEqual(self.store.checkpoint('test-github')['since'], '2026-10-15T11:00:00Z')
        self.assertTrue(all(c == 'user' or c.startswith(('notifications?', 'repos/')) for c in source.calls))
        self.assertIn('participating=true', next(c for c in source.calls if c.startswith('notifications?')))

    def test_replay_adds_nothing_and_repo_filter_applies(self):
        github.sync(self.store, {}, GITHUB, H, FakeGitHub(self.NOTES))
        github.sync(self.store, {}, GITHUB, H, FakeGitHub(self.NOTES))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*),max(version) FROM events').fetchone()[:], (2, 1))
        self.store = a.Store(Path(self.tmp.name) / 'filtered.sqlite3')
        self.assertEqual(github.sync(self.store, {}, {**GITHUB, 'repos': ['org/elsewhere']}, H, FakeGitHub(self.NOTES))['events'], 0)

    def test_failed_ci_runs_on_watched_repos(self):
        run = {'id': 55, 'name': 'Tests', 'updated_at': '2026-10-15T12:00:00Z', 'html_url': 'https://github.com/org/app/actions/runs/55',
               'head_commit': {'message': 'Fix export'}, 'actor': {'login': 'colleague'}}
        source = FakeGitHub([], [run])
        github.sync(self.store, {}, {**GITHUB, 'ci_repos': ['org/app']}, H, source)
        [row] = self.stored()
        self.assertEqual((row['source_id'], row['kind'], row['title']), ('ci:55', 'github.ci', '[app] Tests failed on main'))
        self.assertIn('status=failure', next(c for c in source.calls if 'actions/runs' in c))

    def test_wrong_login_and_unsafe_paths_are_refused(self):
        with self.assertRaises(a.SourceError) as caught:
            wrong = {**GITHUB, 'login': 'someone-else'}
            github.sync(self.store, {}, wrong, H, FakeGitHub(self.NOTES, account=wrong))
        self.assertEqual(str(caught.exception), 'account_identity_mismatch')
        source = github.Source({'gh': '/bin/false'}, GITHUB, H)
        for path in ['/user', 'graphql', 'user; rm -rf x', 'repos/a b']:
            with self.subTest(path), self.assertRaises(a.SourceError) as caught:
                source.get(path)
            self.assertEqual(str(caught.exception), 'github_path_not_allowed')
        with patch('subprocess.run', return_value=subprocess.CompletedProcess([], 1, '', 'gh: Not Found (HTTP 404)')) as run:
            with self.assertRaises(a.SourceError) as caught:
                source.get('notifications')
        self.assertEqual(caught.exception.status, 404)
        self.assertEqual(run.call_args[0][0][1:4], ['api', '--method', 'GET'])

    def test_kind_labels_and_plugin_loading(self):
        self.assertEqual(a.source_kind('github.notification'), 'GitHub')
        self.assertEqual(a.source_kind('github.ci'), 'GitHub CI')
        self.assertEqual(a.source_kind('stripe.event'), 'Stripe')
        self.assertTrue({'github', 'stripe'} <= set(a.connector_services()))


if __name__ == '__main__':
    unittest.main()

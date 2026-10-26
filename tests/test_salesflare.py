import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('salesflare_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

ACCOUNT = {'id': 'work-crm', 'service': 'salesflare', 'email': 'owner@example.com', 'user_id': 1, 'team_id': 1,
           'boundary': 'work:Example', 'api_base': 'https://crm.example', 'app_base': 'https://app.example',
           'accounts_per_batch': 1}
NOW = a.dt.datetime.now(a.dt.timezone.utc)


def iso(hours_ago):
    return (NOW - a.dt.timedelta(hours=hours_ago)).isoformat().replace('+00:00', 'Z')


class FakeCRM:
    def __init__(self, forbidden=(), opportunities=()):
        self.calls, self.forbidden, self.joined = [], set(forbidden), []
        self.opportunities = set(opportunities)  # (crm_id, pipeline)
        self.accounts = {
            10: {'id': 10, 'name': 'Acme', 'domain': 'acme.com', 'last_email_date': iso(2), 'last_meeting_date': None,
                 'customers': [{'id': 100, 'name': 'Ann Acme', 'email': 'ann@acme.example', 'role': 'CEO'},
                               {'id': 101, 'name': 'Bob Acme', 'email': 'bob@acme.example', 'role': 'CTO'}]},
            20: {'id': 20, 'name': 'Globex', 'domain': 'globex.com', 'last_email_date': iso(500), 'last_meeting_date': iso(5),
                 'customers': [{'id': 200, 'name': 'Gail Globex', 'email': 'gail@globex.example', 'role': 'Buyer'}]},
            30: {'id': 30, 'name': 'Old', 'domain': 'old.com', 'last_email_date': iso(900), 'last_meeting_date': iso(900), 'customers': []},
        }
        self.feeds = {
            (10, 'email'): [
                {'id': 'e1', 'time': iso(2), 'email': {'user_id': 7, 'date': iso(2), 'subject': 'Pricing question',
                    'body': [{'type': 'text/html', 'content': '<p>Can you send a quote?</p>'}],
                    'addresses': {'from': {'name': 'Ann Acme', 'email': 'ann@acme.example'},
                                  'to': [{'name': 'Rep', 'email': 'rep@example.com'}]}}},
                {'id': 'e2', 'time': iso(3), 'email': {'user_id': 7, 'date': iso(3), 'subject': 'Cc owner',
                    'body': [], 'addresses': {'from': {'email': 'bob@acme.example'}, 'to': [{'email': 'rep@example.com'}],
                                              'cc': [{'email': 'OWNER@example.com'}]}}},
                {'id': 'e3', 'time': iso(4), 'email': {'user_id': 1, 'date': iso(4), 'subject': 'Owner mailbox',
                    'body': [], 'addresses': {'from': {'email': 'ann@acme.example'}, 'to': [{'email': 'other@example.com'}]}}},
            ],
            (20, 'meeting-live'): [
                {'id': 7, 'time': iso(5), 'type': 'meeting-live', 'subject': 'Demo', 'notes': '<p>They want SSO by Q1.</p>',
                 'person': {'email': 'rep@example.com'},
                 'participants': [{'id': 200, 'name': 'Gail Globex', 'email': 'gail@globex.example', 'type': 'contact'},
                                  {'id': 3, 'name': 'Rep', 'type': 'user'}]},
                {'id': 8, 'time': iso(6), 'type': 'meeting-live', 'subject': 'No notes', 'notes': '  ', 'participants': []},
            ],
        }

    def profile(self):
        return {'id': 1}

    def get(self, path, params=None):
        self.calls.append((path, dict(params or {})))
        if path == '/accounts':
            field = params['order_by'].split()[0]
            rows = sorted((r for r in self.accounts.values() if r.get(field)), key=lambda r: r[field], reverse=True)
            return rows[params['offset']:params['offset'] + params['limit']]
        if path == '/opportunities':
            return [{'id': 1}] if (params['account'], params['pipeline']) in self.opportunities else []
        crm_id = int(path.split('/')[2])
        if crm_id in self.forbidden and path.endswith('/feed'):
            raise a.SourceError('salesflare', 403)
        if path.endswith('/feed'):
            return self.feeds.get((crm_id, params['types']), [])
        return {**self.accounts[crm_id], 'part_of': crm_id not in self.forbidden}

    def join_account(self, crm_id):
        self.joined.append(crm_id)
        self.forbidden.discard(crm_id)


class SalesflareConnector(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')

    def run_to_completion(self, crm):
        for _ in range(10):
            if not a.sync_salesflare(self.store, {}, ACCOUNT, crm)['more']:
                return
        self.fail('sync did not finish')

    def test_imports_recent_accounts_only_other_peoples_email_and_noted_meetings(self):
        crm = FakeCRM()
        self.run_to_completion(crm)
        rows = {r['source_id']: r for r in self.store.events(['work-crm'])}
        self.assertEqual(set(rows), {'email:e1', 'meeting:7'})  # cc'd owner, owner mailbox, empty notes all skipped
        self.assertNotIn(30, {int(p.split('/')[2]) for p, _ in crm.calls if p != '/accounts'})  # out-of-window account
        email = rows['email:e1']
        self.assertEqual(email['metadata']['crm_account'], {'id': 10, 'name': 'Acme', 'domain': 'acme.com'})
        self.assertEqual(email['metadata']['contacts'], [{'id': 100, 'name': 'Ann Acme', 'email': 'ann@acme.example', 'role': 'CEO'}])
        self.assertIn('Can you send a quote?', email['body'])
        self.assertEqual(email['metadata']['source_url'], 'https://app.example/#/accounts/10/info/view')
        meeting = rows['meeting:7']
        self.assertIn('They want SSO by Q1.', meeting['body'])
        self.assertEqual(meeting['metadata']['contacts'], [{'id': 200, 'name': 'Gail Globex', 'email': 'gail@globex.example', 'role': 'Buyer'}])
        state = self.store.checkpoint('work-crm')
        self.assertEqual(state['mode'], 'incremental')
        self.assertNotIn('window', state)

    def test_each_batch_commits_with_its_progress_and_replay_is_idempotent(self):
        crm = FakeCRM()
        first = a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertTrue(first['more'])
        self.assertEqual(len(self.store.checkpoint('work-crm')['window']['pending']), 1)
        self.run_to_completion(crm)
        self.store.commit_page('work-crm', self.store.checkpoint('work-crm'), [])
        before = len(self.store.events(['work-crm']))
        self.run_to_completion(FakeCRM())  # next window rereads with overlap
        self.assertEqual(len(self.store.events(['work-crm'])), before)

    def test_inaccessible_account_is_recorded_not_fatal(self):
        crm = FakeCRM(forbidden={10})
        self.run_to_completion(crm)
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'meeting:7'})
        self.assertEqual(self.store.checkpoint('work-crm')['inaccessible_accounts'], [10])

    def test_failed_feed_keeps_the_batch_pending(self):
        crm = FakeCRM()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)  # first account committed
        pending = self.store.checkpoint('work-crm')['window']['pending']
        with patch.object(crm, 'get', side_effect=a.SourceError('network:TimeoutError:salesflare_read')):
            with self.assertRaises(a.SourceError):
                a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(self.store.checkpoint('work-crm')['window']['pending'], pending)

    def test_only_read_routes_and_exact_identity(self):
        client = a.Salesflare({}, ACCOUNT)
        for path in ['/accounts/10/contacts', '/accounts/10/users', '/me/settings']:
            with self.assertRaises(a.SourceError):
                client.get(path)
        for me in [{'id': 2, 'email': 'owner@example.com', 'team': {'id': 1}},
                   {'id': 1, 'email': 'other@example.com', 'team': {'id': 1}},
                   {'id': 1, 'email': 'owner@example.com', 'team': {'id': 9}}]:
            with patch.object(client, 'get', return_value=me), self.assertRaises(a.SourceError):
                client.profile()

    def test_unbounded_account_listing_fails_visibly(self):
        crm = FakeCRM()
        with patch.object(a, 'salesflare_time', return_value=NOW):
            with self.assertRaises(a.SourceError):
                a.salesflare_recent_accounts(crm, 'last_email_date', NOW, page=1, max_pages=2)

    def test_joins_only_pipeline_linked_accounts_then_reads_their_timeline(self):
        joining = {**ACCOUNT, 'join_pipelines': [1, 318]}
        crm = FakeCRM(forbidden={10, 20}, opportunities={(10, 318)})
        for _ in range(10):
            if not a.sync_salesflare(self.store, {}, joining, crm)['more']:
                break
        self.assertEqual(crm.joined, [10])  # Globex has no Customers/Larger prospects opportunity
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1'})
        state = self.store.checkpoint('work-crm')
        self.assertEqual([j['id'] for j in state['joined_accounts']], [10])
        self.assertEqual(state['inaccessible_accounts'], [20])

    def test_join_is_off_without_explicit_pipelines(self):
        crm = FakeCRM(forbidden={10}, opportunities={(10, 1)})
        self.run_to_completion(crm)
        self.assertEqual(crm.joined, [])
        with self.assertRaises(a.SourceError):
            a.Salesflare({}, ACCOUNT).join_account(10)

    def test_join_posts_only_the_owner_to_one_account(self):
        client = a.Salesflare({}, {**ACCOUNT, 'join_pipelines': [1]})
        with patch.object(client, 'send') as send:
            client.join_account(10)
        send.assert_called_once_with('/accounts/10/users', None, [{'id': 1}])

    def test_meetings_are_reread_over_a_week_while_email_stays_incremental(self):
        crm = FakeCRM()
        self.run_to_completion(crm)  # first window
        crm.feeds[(20, 'meeting-live')][1]['notes'] = '<p>Notes added days later</p>'
        crm.feeds[(20, 'meeting-live')][1]['time'] = iso(70)  # meeting three days ago
        crm.accounts[20]['last_meeting_date'] = iso(70)
        crm.calls.clear()
        self.run_to_completion(crm)  # next incremental poll
        self.assertIn('meeting:8', {r['source_id'] for r in self.store.events(['work-crm'])})
        feeds = [(p, q) for p, q in crm.calls if p.endswith('/feed')]
        self.assertFalse([1 for p, q in feeds if p == '/accounts/20/feed' and q['types'] == 'email'])  # meeting-only account
        meeting_after = a.dt.datetime.fromisoformat(next(q['after'] for p, q in feeds if q['types'] == 'meeting-live'))
        self.assertLess(meeting_after, NOW - a.dt.timedelta(days=6))

    def test_noise_subjects_are_excluded_in_every_language_and_purged(self):
        for subject in ["Accepted: Demo @ Tue", "Geaccepteerd: Call",
                        "Accepté : Réunion", "Angenommen: Termin", "Aceptado: Llamada", "ACCEPTED: sync"]:
            self.assertTrue(a.email_subject_excluded({}, subject), subject)
        for subject in ["Re: Pricing", "Your offer was accepted: next steps", "Not accepted yet", "Dana's notes"]:
            self.assertFalse(a.email_subject_excluded({}, subject), subject)
        crm = FakeCRM()
        crm.feeds[(10, 'email')][0]['email']['subject'] = 'Accepted: Demo'
        self.run_to_completion(crm)
        self.assertNotIn('email:e1', {r['source_id'] for r in self.store.events(['work-crm'])})
        self.store.commit_page('work-gmail', {}, [{'account_id': 'work-gmail', 'source_id': 'g1', 'kind': 'gmail.message',
            'occurred_at': a.now(), 'title': "Accepted: Weekly sync", 'body': 'x', 'metadata': {}, 'deleted': False},
            {'account_id': 'work-gmail', 'source_id': 'g2', 'kind': 'gmail.message', 'occurred_at': a.now(),
             'title': 'Real customer question', 'body': 'x', 'metadata': {}, 'deleted': False}])
        self.assertEqual(self.store.purge_email_subject_exclusions({}), {'work-gmail': 1})
        self.assertEqual([r['source_id'] for r in self.store.events(['work-gmail'])], ['g2'])

    def test_account_that_keeps_timing_out_is_set_aside_after_three_tries(self):
        crm = FakeCRM()
        original = crm.get
        def slow_acme(path, params=None):
            if path == '/accounts/10/feed':
                raise a.SourceError('network:TimeoutError:salesflare_read')
            return original(path, params)
        crm.get = slow_acme
        for _ in range(2):
            with self.assertRaises(a.SourceError):
                a.sync_salesflare(self.store, {}, {**ACCOUNT, 'accounts_per_batch': 5}, crm)
        self.run_to_completion(crm)  # third failure: set aside, Globex still imported
        state = self.store.checkpoint('work-crm')
        self.assertEqual(state['skipped_accounts'], [10])
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'meeting:7'})


class SalesflareStopAndRestart(unittest.TestCase):
    """The Salesflare card: Stop, Start and Restart (App.connector_sync), and what the card shows of a round."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.soon = []
        import threading
        lock = threading.Lock()
        self.app = type('App', (), {'config': {'accounts': [ACCOUNT, {'id': 'work-mail', 'service': 'gmail'}]}, 'store': self.store,
                                    'sync_lock': lambda _, account: lock, 'sync_soon': lambda _, account: self.soon.append(account),
                                    'connector_sync': a.App.connector_sync})()

    def test_the_card_shows_the_round_and_a_round_running_too_long_as_stuck(self):
        a.sync_salesflare(self.store, {}, ACCOUNT, FakeCRM())
        view = a.salesflare_progress(ACCOUNT, self.store.checkpoint('work-crm'))
        self.assertEqual((view['round']['accounts'], view['round']['done'], view['round']['stuck'], view['stopped']), (2, 1, False, None))
        self.assertEqual(view['keys_url'], 'https://app.example/#/settings/apikeys')
        state = self.store.checkpoint('work-crm')
        state['window']['until'] = (NOW - a.dt.timedelta(hours=3)).isoformat()
        self.assertTrue(a.salesflare_progress(ACCOUNT, state)['round']['stuck'])
        self.assertEqual(a.salesflare_progress({}, {})['keys_url'], 'https://app.salesflare.com/#/settings/apikeys')

    def test_stop_reads_nothing_until_start_which_goes_on_where_it_was(self):
        crm = FakeCRM()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        pending = self.store.checkpoint('work-crm')['window']['pending']
        self.app.connector_sync({'account': 'work-crm', 'do': 'stop'})
        calls = len(crm.calls)
        self.assertEqual(a.sync_salesflare(self.store, {}, ACCOUNT, crm), {'mode': 'bootstrap', 'events': 0, 'stopped': True})
        self.assertEqual(len(crm.calls), calls)  # not even a profile read
        self.assertEqual(self.soon, [])
        self.app.connector_sync({'account': 'work-crm', 'do': 'start'})
        self.assertEqual((self.store.checkpoint('work-crm')['window']['pending'], self.soon), (pending, ['work-crm']))
        self.assertFalse(a.sync_salesflare(self.store, {}, ACCOUNT, crm).get('stopped'))

    def test_restart_drops_a_stuck_round_its_errors_and_wait_and_rereads_the_week(self):
        crm = FakeCRM()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.store.failed('work-crm', a.SourceError('network:TimeoutError:salesflare_read', retry_after=3600))
        result = self.app.connector_sync({'account': 'work-crm', 'do': 'restart'})
        self.assertIsNone(result['salesflare']['round'])
        with self.store.connect() as db:
            row = db.execute('SELECT error,retry_at,failures FROM checkpoints WHERE account_id=?', ('work-crm',)).fetchone()
        self.assertEqual(tuple(row), (None, None, 0))
        self.assertEqual(self.store.checkpoint('work-crm')['next_full'], 0)
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(len(self.store.checkpoint('work-crm')['window']['pending']), 1)  # a new round of the same accounts

    def test_only_a_salesflare_connection_and_only_these_three(self):
        for args in ({'account': 'work-mail', 'do': 'stop'}, {'account': 'nope', 'do': 'stop'}, {'account': 'work-crm', 'do': 'wipe'}):
            with self.assertRaises(ValueError):
                self.app.connector_sync(args)
        self.assertIn('connector_sync', a.DASHBOARD_ACTIONS)
        self.assertIn('connector_sync', a.OWNER_ACTIONS)


if __name__ == '__main__':
    unittest.main()

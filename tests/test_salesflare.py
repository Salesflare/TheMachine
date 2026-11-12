import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('salesflare_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

ACCOUNT = {'id': 'work-crm', 'service': 'salesflare', 'email': 'owner@example.com', 'user_id': 1, 'team_id': 1,
           'boundary': 'work:Example', 'api_base': 'https://crm.example', 'app_base': 'https://app.example',
           'accounts_per_batch': 1}
NOW = a.dt.datetime.now(a.dt.timezone.utc)


def iso(hours_ago):
    return (NOW - a.dt.timedelta(hours=hours_ago)).isoformat().replace('+00:00', 'Z')


def listed(crm):
    """(field, offset) of each account list page asked."""
    return [(a.json.loads(q['q'])['rules'][0]['id'].removeprefix('account.'), q['offset'])
            for p, q in crm.calls if p == '/accounts']


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
            # Filtered by one date rule and ordered by ID, as the sync asks; never sorted by the date (heavy on Salesflare).
            assert params['order_by'] == 'id', params
            [rule] = a.json.loads(params['q'])['rules']
            field, lowest = rule['id'].removeprefix('account.'), a.salesflare_time(rule['value'][0])
            assert rule['operator'] == 'greater_or_equal', rule
            rows = sorted((r for r in self.accounts.values() if r.get(field)
                           and (a.salesflare_time_or_none(r[field]) or lowest) >= lowest), key=lambda r: r['id'])
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
        for _ in range(40):
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

    def test_a_contacts_picture_on_salesflares_own_host_is_kept_for_people_in_what_was_read(self):
        """A contact's picture from the account read anyway: only links on Salesflare's own image host, only for people
        in a kept message or meeting, kept as a contact's photo link (not chosen by them), never fetched here."""
        crm = FakeCRM()
        crm.accounts[10]['customers'][0]['picture'] = 'https://lib.salesflare.com/pictures/ann.png'
        crm.accounts[10]['customers'][1]['picture'] = 'https://lib.salesflare.com/pictures/bob.png'  # only in skipped mail
        crm.accounts[20]['customers'][0]['picture'] = 'https://img.enrich.example/gail.png'  # another service's host
        self.run_to_completion(crm)
        with self.store.connect() as db:
            rows = db.execute('SELECT identifier,url,chosen,source FROM contact_photo_links').fetchall()
        self.assertEqual([tuple(r) for r in rows], [('email:ann@acme.example', 'https://lib.salesflare.com/pictures/ann.png', 0, 'salesflare')])
        rows = {r['source_id']: r for r in self.store.events(['work-crm'])}
        self.assertNotIn('picture', rows['email:e1']['metadata']['contacts'][0])  # the link stays out of the message
        from machine.sources.salesflare import salesflare_picture
        self.assertEqual(salesflare_picture('https://staginglib.salesflare.com/p/x.jpg'), 'https://staginglib.salesflare.com/p/x.jpg')
        for other in ('http://lib.salesflare.com/p.png', 'https://lib.salesflare.com.evil.example/p.png', None, 5):
            self.assertIsNone(salesflare_picture(other))

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
            self.assertTrue(a.sync_salesflare(self.store, {}, ACCOUNT, crm)['more'])  # one hiccup: back of the round
            self.assertEqual(self.store.checkpoint('work-crm')['window']['pending'], pending)
            with self.assertRaises(a.SourceError):  # two in a row: Salesflare is down, the sync fails and backs off
                a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(self.store.checkpoint('work-crm')['window']['pending'], pending)

    def test_dates_as_epoch_milliseconds_or_text_parse(self):
        expected = a.dt.datetime(2026, 11, 1, 3, 49, 11, tzinfo=a.dt.timezone.utc)
        for value in (1793504951000, 1793504951000.0, '1793504951000', 1793504951, '2026-11-01T03:49:11.000Z',
                      '2026-11-01T04:49:11+01:00'):
            self.assertEqual(a.salesflare_time(value), expected, value)
        for value in (None, '', 'yesterday', True):
            with self.assertRaises(a.SourceError):
                a.salesflare_time(value)
        with self.assertRaises(a.SourceError):
            a.salesflare_time('2026-11-01T03:49:11')  # no timezone

    def test_an_email_dated_in_epoch_milliseconds_is_imported(self):
        crm = FakeCRM()
        email = crm.feeds[(10, 'email')][0]['email']
        email['date'] = int(a.dt.datetime.fromisoformat(email['date'].replace('Z', '+00:00')).timestamp() * 1000)
        self.run_to_completion(crm)
        rows = {r['source_id']: r for r in self.store.events(['work-crm'])}
        self.assertEqual(set(rows), {'email:e1', 'meeting:7'})
        self.assertNotIn('window', self.store.checkpoint('work-crm'))

    def test_one_unreadable_record_is_skipped_and_logged_not_the_round(self):
        crm = FakeCRM()
        crm.feeds[(10, 'email')].insert(0, {'id': 'bad', 'time': 'not a date', 'email': {
            'user_id': 7, 'date': None, 'subject': 'Broken', 'body': [],
            'addresses': {'from': {'email': 'ann@acme.example'}, 'to': [{'email': 'rep@example.com'}]}}})
        crm.feeds[(20, 'meeting-live')].append({'id': 9, 'time': None, 'subject': 'Broken', 'notes': 'Has notes', 'participants': []})
        with self.assertLogs('personal-assistant', 'WARNING') as logs:
            self.run_to_completion(crm)
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1', 'meeting:7'})
        state = self.store.checkpoint('work-crm')
        self.assertNotIn('window', state)  # the round finished and the watermark moved on
        self.assertIsNotNone(state['watermark'])
        joined = '\n'.join(logs.output)
        self.assertIn('item=email:bad error=salesflare_invalid_timestamp', joined)
        self.assertIn('item=meeting:9 error=salesflare_invalid_timestamp', joined)
        self.assertNotIn('Broken', joined)  # no subjects or bodies in the log

    def test_an_unreadable_account_date_still_lists_the_account(self):
        crm = FakeCRM()
        crm.accounts[10]['last_email_date'] = 'garbage'
        self.assertIn(10, a.salesflare_recent_accounts(crm, 'last_email_date', NOW - a.dt.timedelta(days=1)))

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
        with patch_everywhere(a, 'salesflare_time', return_value=NOW):
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

    def due_now(self, *meetings):
        """Time passes until the next notes check of these watched meetings."""
        state = self.store.checkpoint('work-crm')
        for key in meetings:
            state['notes_watch'][key]['next'] = iso(0.01)
        self.store.commit_page('work-crm', state, [], record_sync=False)

    def test_late_notes_are_picked_up_by_rechecking_only_meetings_without_them(self):
        crm = FakeCRM()
        self.run_to_completion(crm)  # first window
        watch = self.store.checkpoint('work-crm')['notes_watch']
        # No notes yet (8), and notes on a meeting less than a day old (7): both watched, from 2 hours, a day, ... after
        self.assertEqual(set(watch), {'7', '8'})
        self.assertEqual(a.dt.datetime.fromisoformat(watch['8']['next']),
                         a.dt.datetime.fromisoformat(iso(6).replace('Z', '+00:00')) + a.dt.timedelta(days=1))
        crm.feeds[(20, 'meeting-live')][1]['notes'] = '<p>Notes added later</p>'  # the meeting's date stays the same
        crm.calls.clear()
        self.run_to_completion(crm)  # nothing due, nothing changed: two short list pages and no account read
        self.assertEqual([p for p, _ in crm.calls], ['/accounts', '/accounts'])
        self.assertNotIn('meeting:8', {r['source_id'] for r in self.store.events(['work-crm'])})
        self.due_now('8')
        crm.calls.clear()
        self.run_to_completion(crm)
        self.assertIn('meeting:8', {r['source_id'] for r in self.store.events(['work-crm'])})
        feeds = [(p, q['types']) for p, q in crm.calls if p.endswith('/feed')]
        self.assertEqual(feeds, [('/accounts/20/feed', 'meeting-live'), ('/accounts/20/feed', 'meeting-phone')])  # no email
        self.assertIn('8', self.store.checkpoint('work-crm')['notes_watch'])  # under a day old: its notes may still grow

    def test_a_meeting_is_checked_for_notes_at_most_a_week(self):
        state, stamp = {}, NOW
        old = {'id': 1, 'time': iso(24 * 6), 'notes': ''}
        settled = {'id': 2, 'time': iso(30), 'notes': '<p>Done</p>'}
        fresh = {'id': 3, 'time': iso(1), 'notes': '<p>Draft</p>'}
        planned = {'id': 4, 'time': iso(-48), 'notes': ''}
        from machine.sources.salesflare import salesflare_notes_due, salesflare_watch_notes
        salesflare_watch_notes(state, 20, [old, settled, fresh, planned], stamp)
        watch = state['notes_watch']
        self.assertEqual(set(watch), {'1', '3', '4'})
        at = a.dt.datetime.fromisoformat(watch['1']['at'])
        self.assertEqual(a.dt.datetime.fromisoformat(watch['1']['next']), at + a.dt.timedelta(days=7))  # its last check
        due = salesflare_notes_due(state, stamp + a.dt.timedelta(days=1, hours=1))
        self.assertEqual({entry['at'] for entry in due}, {watch['1']['at'], watch['3']['at']})
        self.assertNotIn('1', state['notes_watch'])  # the week is over: no more checks, read or not
        self.assertEqual(a.dt.datetime.fromisoformat(state['notes_watch']['3']['next']),
                         a.dt.datetime.fromisoformat(watch['3']['at']) + a.dt.timedelta(days=3))
        salesflare_watch_notes(state, 20, [], stamp)  # read again and gone from the feed: not watched any more
        self.assertNotIn('notes_watch', state)

    def test_a_quiet_round_lists_one_page_per_field_and_reads_no_account(self):
        crm = FakeCRM()
        for n in range(25):  # more than two pages of accounts with email today
            crm.accounts[1000 + n] = {'id': 1000 + n, 'name': f'Co {n}', 'domain': f'co{n}.example',
                                      'last_email_date': iso(1 + n / 10), 'last_meeting_date': None, 'customers': []}
        self.run_to_completion(crm)
        self.assertEqual(listed(crm), [('last_email_date', 0), ('last_meeting_date', 0)])  # one filtered page each
        crm.calls.clear()
        self.store.commit_page('work-crm', {**self.store.checkpoint('work-crm'), 'notes_watch': {}}, [], record_sync=False)
        last_round = self.store.checkpoint('work-crm')['last_round']
        self.run_to_completion(crm)
        self.assertEqual([p for p, _ in crm.calls], ['/accounts', '/accounts'])
        self.assertEqual(listed(crm), [('last_email_date', 0), ('last_meeting_date', 0)])
        state = self.store.checkpoint('work-crm')
        self.assertEqual(state['last_round'], last_round)  # the card keeps the last round that read accounts
        self.assertGreater(state['watermark'], last_round['at'])
        crm.accounts[1020]['last_email_date'] = iso(0)  # one new email, on an account well down the list
        crm.calls.clear()
        self.run_to_completion(crm)
        self.assertEqual([p for p, _ in crm.calls if p != '/accounts'], ['/accounts/1020', '/accounts/1020/feed',
                                                                         '/accounts/1020/feed', '/accounts/1020/feed'])
        self.assertEqual(len([p for p, _ in crm.calls if p == '/accounts']), 2)

    def test_the_list_pages_on_until_it_reaches_the_last_rounds_mark(self):
        crm = FakeCRM()
        self.run_to_completion(crm)
        mark = self.store.checkpoint('work-crm')['marks']['last_email_date']
        self.assertEqual(mark['id'], 10)
        for n in range(15):  # more new activity than one page holds
            crm.accounts[2000 + n] = {'id': 2000 + n, 'name': f'New {n}', 'domain': f'new{n}.example',
                                      'last_email_date': iso(0.5 + n / 100), 'last_meeting_date': None, 'customers': []}
        crm.calls.clear()
        self.run_to_completion(crm)
        [query] = [q for p, q in crm.calls if p == '/accounts' and 'last_email_date' in q['q']]
        lowest = a.salesflare_time(a.json.loads(query['q'])['rules'][0]['value'][0])
        self.assertEqual(lowest, a.salesflare_time(mark['at']).replace(microsecond=0) - a.dt.timedelta(minutes=1))
        read = {int(p.split('/')[2]) for p, _ in crm.calls if p.startswith('/accounts/') and not p.endswith('/feed')}
        self.assertEqual(read, set(range(2000, 2015)))  # Acme, at the mark, is not read again
        self.assertEqual(self.store.checkpoint('work-crm')['marks']['last_email_date']['id'], 2000)

    def test_the_filtered_list_pages_by_id_and_answers_newest_first(self):
        from machine.sources.salesflare import salesflare_recent_stamps
        crm = FakeCRM()
        for n in range(15):  # more than one page; IDs in the opposite order of their dates
            crm.accounts[3000 - n] = {'id': 3000 - n, 'name': f'New {n}', 'domain': f'new{n}.example',
                                      'last_email_date': iso(0.5 + n / 100), 'last_meeting_date': None, 'customers': []}
        crm.accounts[3001] = {'id': 3001, 'name': 'Just below', 'domain': 'below.example',
                              'last_email_date': iso(48.01), 'last_meeting_date': None, 'customers': []}  # in the margin
        mark = {'at': iso(2), 'id': 10}  # Acme, read last round
        found = salesflare_recent_stamps(crm, 'last_email_date', NOW - a.dt.timedelta(hours=48), mark, page=10)
        self.assertEqual(listed(crm), [('last_email_date', 0), ('last_email_date', 10)])
        self.assertEqual(list(found), list(range(3000, 2985, -1)))  # newest first; not Acme at the mark, nor Globex
        found = salesflare_recent_stamps(crm, 'last_email_date', NOW - a.dt.timedelta(hours=48), page=100)
        self.assertNotIn(3001, found)  # older than the window, though within the filter's margin
        self.assertEqual(list(found)[-1], 10)

    def test_a_weekly_full_round_rereads_the_week_whatever_the_dates_say(self):
        crm = FakeCRM()
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertAlmostEqual(state['next_full'] - a.time.time(), 7 * 86400, delta=600)
        crm.feeds[(10, 'email')].append({'id': 'late', 'time': iso(30), 'email': {
            'user_id': 7, 'date': iso(30), 'subject': 'Taken in late', 'body': [],
            'addresses': {'from': {'email': 'ann@acme.example'}, 'to': [{'email': 'rep@example.com'}]}}})
        self.run_to_completion(crm)
        self.assertNotIn('email:late', {r['source_id'] for r in self.store.events(['work-crm'])})  # Acme's date didn't move
        self.store.commit_page('work-crm', {**self.store.checkpoint('work-crm'), 'next_full': 0}, [], record_sync=False)
        self.run_to_completion(crm)
        self.assertIn('email:late', {r['source_id'] for r in self.store.events(['work-crm'])})

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

    def run_through_hiccups(self, crm, account):
        for _ in range(12):
            try:
                if not a.sync_salesflare(self.store, {}, account, crm)['more']:
                    return
            except a.SourceError:
                pass
        self.fail('sync did not finish')

    def test_account_that_keeps_timing_out_is_set_aside_after_three_tries(self):
        crm = FakeCRM()
        original = crm.get
        def slow_acme(path, params=None):
            if path == '/accounts/10/feed':
                crm.calls.append((path, dict(params or {})))
                raise a.SourceError('network:TimeoutError:salesflare_read')
            return original(path, params)
        crm.get = slow_acme
        self.run_through_hiccups(crm, {**ACCOUNT, 'accounts_per_batch': 5})  # third failure: set aside, Globex still imported
        state = self.store.checkpoint('work-crm')
        self.assertEqual(state['skipped_accounts'], [10])
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'meeting:7'})
        self.assertEqual(sum(p == '/accounts/10/feed' for p, _ in crm.calls), 3)

    def test_a_gateway_timeout_moves_the_account_to_the_back_and_the_batch_goes_on(self):
        # Salesflare's feed now and then hangs until its gateway answers 504 after two minutes, and the same read a
        # minute later answers at once (report s_f0d5d0200384ed92). The accounts before it stay read, the ones after
        # it are read in the same sync, and the slow one is asked again only at the back of the round.
        crm = FakeCRM()
        crm.accounts[40] = {'id': 40, 'name': 'Initech', 'domain': 'initech.com', 'last_email_date': iso(1),
                            'last_meeting_date': None, 'customers': []}
        original = crm.get
        hangs = {'/accounts/10/feed': 1}
        def gateway(path, params=None):
            if hangs.get(path):
                hangs[path] -= 1
                crm.calls.append((path, dict(params or {})))
                raise a.SourceError('salesflare', 504, route='/accounts/{id}/feed')
            return original(path, params)
        crm.get = gateway
        batch = {**ACCOUNT, 'accounts_per_batch': 2}
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            self.assertTrue(a.sync_salesflare(self.store, {}, batch, crm)['more'])  # no failed sync, no quick refire
        self.assertIn('salesflare slow account error=salesflare:HTTP_504 route=/accounts/{id}/feed try=1 in_a_row=1', logged.output[0])
        window = self.store.checkpoint('work-crm')['window']
        self.assertEqual(window['pending'], [20, 10])  # Initech (40) read, Acme (10) at the back
        self.assertEqual(sum(p == '/accounts/10/feed' for p, _ in crm.calls), 1)
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1', 'meeting:7'})
        self.assertEqual((state['skipped_accounts'], state['last_round']['read'], state['last_round']['set_aside']), ([], 3, 0))

    def test_a_repeat_offender_is_set_aside_and_two_in_a_row_back_off(self):
        crm = FakeCRM()
        original = crm.get
        def gateway(path, params=None):
            if path == '/accounts/20':
                raise a.SourceError('salesflare', 504)
            return original(path, params)
        crm.get = gateway
        batch = {**ACCOUNT, 'accounts_per_batch': 5}
        self.assertTrue(a.sync_salesflare(self.store, {}, batch, crm)['more'])  # Acme read, Globex to the back
        self.assertEqual(self.store.checkpoint('work-crm')['window']['pending'], [20])
        with self.assertRaises(a.SourceError):  # Globex again, with no answer in between: back off
            a.sync_salesflare(self.store, {}, batch, crm)
        self.assertEqual(self.store.checkpoint('work-crm')['window']['pending'], [20])
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1'})
        self.run_through_hiccups(crm, batch)  # third time: set aside, the round ends
        state = self.store.checkpoint('work-crm')
        self.assertEqual((state['skipped_accounts'], state['last_round']['read'], state['last_round']['set_aside']), ([20], 1, 1))
        view = a.salesflare_progress(ACCOUNT, state)
        self.assertEqual((view['slow_accounts'], view['no_access'], view['no_access_all']), (1, 0, False))

    def test_without_access_counts_one_round_never_more_than_its_accounts(self):
        state = {'watermark': iso(1), 'inaccessible_accounts': list(range(136)),
                 'window': {'accounts': 128, 'pending': list(range(123)), 'until': iso(0)}}
        # An older Machine's list only grew: its running round counts its own, and the list is replaced when it ends
        self.assertEqual(a.salesflare_progress(ACCOUNT, state)['no_access'], 0)
        self.assertEqual(a.salesflare_progress(ACCOUNT, {**state, 'window': {**state['window'], 'no_access': [5]}})['no_access'], 1)
        self.assertEqual(a.salesflare_progress(ACCOUNT, {**state, 'window': None})['no_access'], 136)  # no round to go by
        crm = FakeCRM(forbidden={10})
        self.store.commit_page('work-crm', {'inaccessible_accounts': list(range(500, 636))}, [], record_sync=False)
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertEqual(state['inaccessible_accounts'], [10])
        self.assertEqual(state['last_round'] | {'at': None}, {'at': None, 'accounts': 2, 'read': 1, 'no_access': 1, 'refused': 1, 'set_aside': 0})
        view = a.salesflare_progress(ACCOUNT, state)
        self.assertEqual((view['no_access'], view['no_access_all'], view['last_round']['read']), (1, False, 1))

    def test_an_account_that_becomes_readable_drops_out(self):
        crm = FakeCRM(forbidden={10, 20})
        self.run_to_completion(crm)
        self.assertEqual(self.store.checkpoint('work-crm')['inaccessible_accounts'], [10, 20])
        crm.forbidden = {20}  # the owner was added to Acme
        self.store.commit_page('work-crm', {**self.store.checkpoint('work-crm'), 'next_full': 0}, [], record_sync=False)
        with self.assertLogs(a.LOG, 'INFO') as logged:
            self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertEqual((state['inaccessible_accounts'], state['last_round']['no_access']), ([20], 1))
        self.assertEqual(a.salesflare_progress(ACCOUNT, state)['no_access'], 1)
        batches = [line.split('salesflare ')[1] for line in logged.output if 'salesflare batch' in line]
        self.assertEqual(sorted(batches), ['batch read=0 no_access=1 left=0', 'batch read=1 no_access=0 left=1'])

    def test_without_access_during_a_round_adds_new_ones_to_the_last_round(self):
        last = {'at': iso(2), 'accounts': 128, 'read': 120, 'no_access': 8, 'refused': 8, 'set_aside': 0}
        state = {'watermark': iso(1), 'inaccessible_accounts': list(range(8)), 'last_round': last,
                 'window': {'accounts': 128, 'pending': list(range(100)), 'until': iso(0), 'read': 20, 'no_access': [3, 50]}}
        self.assertEqual(a.salesflare_progress(ACCOUNT, state)['no_access'], 9)  # 3 was already counted
        self.assertEqual(a.salesflare_progress(ACCOUNT, {**state, 'window': None})['no_access'], 8)
        state['inaccessible_accounts'] = list(range(500, 636))
        self.assertEqual(a.salesflare_progress(ACCOUNT, state)['no_access'], 128)  # never more than the round has

    def test_a_key_that_opens_no_account_says_so(self):
        crm = FakeCRM(forbidden={10, 20})
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            self.run_to_completion(crm)
        self.assertIn('salesflare round opened no account account=work-crm accounts=2 refused=2 missing=0', logged.output[-1])
        view = a.salesflare_progress(ACCOUNT, self.store.checkpoint('work-crm'))
        self.assertTrue(view['no_access_all'])
        self.assertEqual((view['no_access'], view['last_round']['read']), (2, 0))
        # During a first round: after 10 accounts, all refused
        window = {'accounts': 128, 'pending': list(range(118)), 'until': iso(0), 'no_access': list(range(10)), 'refused': 10}
        self.assertTrue(a.salesflare_progress(ACCOUNT, {'window': window})['no_access_all'])
        self.assertFalse(a.salesflare_progress(ACCOUNT, {'window': {**window, 'read': 1}})['no_access_all'])
        self.assertFalse(a.salesflare_progress(ACCOUNT, {'window': {**window, 'pending': list(range(123)), 'no_access': list(range(5))}})['no_access_all'])

    def test_a_refused_round_logs_part_of_route_and_message_as_counts(self):
        class Refusing(FakeCRM):
            def get(self, path, params=None):
                try:
                    answer = super().get(path, params)
                except a.SourceError as error:
                    error.route, error.reason = '/accounts/{id}/feed', 'Forbidden'
                    raise
                if path == '/accounts/20':
                    answer['part_of'] = True  # a member, refused all the same
                return answer
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            self.run_to_completion(Refusing(forbidden={10, 20}))
        refused = sorted(line.split('salesflare ')[1] for line in logged.output if 'salesflare refused ' in line)
        self.assertEqual(refused, ['refused account=work-crm count=1 part_of=false route=/accounts/{id}/feed message=Forbidden',
                                   'refused account=work-crm count=1 part_of=true route=/accounts/{id}/feed message=Forbidden'])
        self.assertNotRegex(' '.join(refused), r'\b(10|20)\b')
        self.assertIn('salesflare round opened no account', logged.output[-1])
        self.assertNotIn('refused_detail', str(self.store.checkpoint('work-crm')))  # gone with the round

    def team_off(self, **more):
        """A CRM whose team has the feed off: every feed read answers 403, though the key's user is part of each account."""
        class TeamOff(FakeCRM):
            off, outsider = True, ()

            def get(self, path, params=None):
                self.calls.append((path, dict(params or {})))
                if path.endswith('/feed') and (self.off or int(path.split('/')[2]) in self.outsider):
                    error = a.SourceError('salesflare', 403, route='/accounts/{id}/feed')
                    error.reason = 'API key access to account feed is not enabled for this team'
                    raise error
                self.calls.pop()
                answer = super().get(path, params)
                if isinstance(answer, dict):
                    answer['part_of'] = answer['id'] not in self.outsider
                return answer
        crm = TeamOff()
        for key, value in more.items():
            setattr(crm, key, value)
        return crm

    def feeds_asked(self, crm):
        return [path for path, _ in crm.calls if path.endswith('/feed')]

    def later(self, **passed):
        """Time passes while the feed is off: every stamp it keeps moves that far back."""
        state = self.store.checkpoint('work-crm')
        for key, value in state['feed_off'].items():
            state['feed_off'][key] = (a.dt.datetime.fromisoformat(value) - a.dt.timedelta(**passed)).isoformat()
        self.store.commit_page('work-crm', state, [], record_sync=False)

    def an_hour_later(self):
        self.later(minutes=61)

    def recheck(self, crm):
        """One sync round while the feed is off: how many accounts it asked, and the level it logged the re-check at."""
        crm.calls.clear()
        with self.assertLogs(a.LOG, 'INFO') as logged:
            a.LOG.info('round')  # so a silent round passes assertLogs
            result = a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual((result['feed_off'], result['more']), (True, False))
        levels = [record.levelname for record in logged.records if 'recheck=1' in record.getMessage()]
        return len(self.feeds_asked(crm)), levels

    def test_a_feed_refused_for_the_whole_team_goes_slow_and_says_so(self):
        crm = self.team_off()
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            self.run_to_completion(crm)
        self.assertIn('salesflare feed off for team account=work-crm accounts=2: one account is re-checked every 10 min for a day, then every 60 min', logged.output[-1])
        view = a.salesflare_progress(ACCOUNT, self.store.checkpoint('work-crm'))
        self.assertEqual((view['feed_off'], view['no_access_all']), (True, False))  # not the key's fault: another key changes nothing
        # The next rounds ask no account at all, log nothing, and still count as a sync that worked
        crm.calls.clear()
        with self.assertNoLogs(a.LOG, 'WARNING'):
            for _ in range(5):
                self.assertEqual(a.sync_salesflare(self.store, {}, ACCOUNT, crm), {'mode': 'incremental', 'events': 0, 'feed_off': True, 'more': False})
        self.assertEqual(crm.calls, [])
        with self.store.connect() as db:
            row = db.execute('SELECT last_success,error FROM checkpoints WHERE account_id=?', ('work-crm',)).fetchone()
        self.assertTrue(row['last_success'] and not row['error'])
        # About an hour later: one account is asked, one line is logged, and it waits again
        self.an_hour_later()
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            result = a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual((result['feed_off'], result['more']), (True, False))
        self.assertEqual(len(self.feeds_asked(crm)), 1)
        self.assertEqual(len(logged.output), 1)
        self.assertRegex(logged.output[0], r'salesflare feed off for team account=work-crm since=\S+ recheck=1 route=/accounts/\{id\}/feed '
                                           r'message=API key access to account feed is not enabled for this team$')
        self.assertNotIn('window', self.store.checkpoint('work-crm'))
        crm.calls.clear()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(crm.calls, [])

    def test_on_the_first_day_one_account_is_asked_every_ten_minutes_and_the_warning_stays_hourly(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        self.later(minutes=9)
        self.assertEqual(self.recheck(crm), (0, []))  # not yet
        self.later(minutes=2)
        self.assertEqual(self.recheck(crm), (1, ['INFO']))  # one account, and no warning so soon after the first one
        self.assertEqual(self.recheck(crm), (0, []))
        levels = []
        for _ in range(12):  # every 11 minutes for over two hours
            self.later(minutes=11)
            asked, logged = self.recheck(crm)
            self.assertEqual(asked, 1)
            levels += logged
        self.assertEqual(len(levels), 12)
        self.assertEqual(levels.count('WARNING'), 2)
        self.assertNotIn('window', self.store.checkpoint('work-crm'))

    def test_after_a_day_one_account_is_asked_hourly(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        self.later(days=1, minutes=1)
        self.assertEqual(self.recheck(crm), (1, ['WARNING']))
        self.later(minutes=11)
        self.assertEqual(self.recheck(crm), (0, []))  # ten minutes no longer does it
        self.later(minutes=48)
        self.assertEqual(self.recheck(crm), (0, []))
        self.later(minutes=2)
        self.assertEqual(self.recheck(crm), (1, ['WARNING']))

    def test_a_feed_off_from_before_the_warning_was_timed_still_warns(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        state['feed_off'].pop('warned')
        self.store.commit_page('work-crm', state, [], record_sync=False)
        self.later(minutes=11)
        self.assertEqual(self.recheck(crm), (1, ['WARNING']))
        self.later(minutes=11)
        self.assertEqual(self.recheck(crm), (1, ['INFO']))

    def test_a_quick_recheck_that_reads_clears_it(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        crm.off = False  # Salesflare support switched it on
        self.later(minutes=11)
        with self.assertLogs(a.LOG, 'INFO') as logged:
            self.run_to_completion(crm)
        self.assertIn('salesflare feed on again account=work-crm', ' '.join(logged.output))
        self.assertNotIn('feed_off', self.store.checkpoint('work-crm'))
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1', 'meeting:7'})

    def test_it_goes_by_route_status_and_part_of_not_by_the_message(self):
        class Reworded(FakeCRM):
            def get(self, path, params=None):
                if path.endswith('/feed'):
                    error = a.SourceError('salesflare', 403, route='/accounts/{id}/feed')
                    error.reason = 'other'
                    raise error
                answer = super().get(path, params)
                return {**answer, 'part_of': True} if isinstance(answer, dict) else answer
        self.run_to_completion(Reworded())
        self.assertTrue(a.salesflare_progress(ACCOUNT, self.store.checkpoint('work-crm'))['feed_off'])

    def test_a_round_with_some_refused_and_some_read_goes_on_as_before(self):
        crm = self.team_off(off=False)  # 20 says the key's user is part of it, and its feed is refused all the same
        refusing = crm.get

        def get(path, params=None):
            if path == '/accounts/20/feed':
                crm.calls.append((path, dict(params or {})))
                raise a.SourceError('salesflare', 403, route='/accounts/{id}/feed')
            return refusing(path, params)
        crm.get = get
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertNotIn('feed_off', state)
        self.assertEqual((state['last_round']['read'], state['last_round']['no_access']), (1, 1))
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1'})
        view = a.salesflare_progress(ACCOUNT, state)
        self.assertEqual((view['feed_off'], view['no_access_all'], view['no_access']), (False, False, 1))
        crm.calls.clear()
        self.run_to_completion(crm)  # the next round asks the refused account again, not the one it read
        self.assertEqual(set(self.feeds_asked(crm)), {'/accounts/20/feed'})

    def test_accounts_the_key_is_not_part_of_stay_a_per_account_refusal(self):
        crm = self.team_off(off=False, outsider={10, 20})
        with self.assertLogs(a.LOG, 'WARNING') as logged:
            self.run_to_completion(crm)
        self.assertIn('salesflare round opened no account', logged.output[-1])
        self.assertNotIn('feed off for team', ' '.join(logged.output))
        state = self.store.checkpoint('work-crm')
        self.assertNotIn('feed_off', state)
        view = a.salesflare_progress(ACCOUNT, state)
        self.assertEqual((view['feed_off'], view['no_access_all']), (False, True))  # the card asks for another key, as before
        crm.calls.clear()
        self.run_to_completion(crm)
        self.assertEqual({path for path in self.feeds_asked(crm)}, {'/accounts/10/feed', '/accounts/20/feed'})
        # One the key is part of and one it isn't, both refused: not every account says "team", so nothing changes
        mixed = self.team_off(off=True, outsider={20})
        self.run_to_completion(mixed)
        self.assertNotIn('feed_off', self.store.checkpoint('work-crm'))

    def test_one_read_after_a_team_refusal_clears_it_and_the_round_goes_on(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        self.assertTrue(self.store.checkpoint('work-crm')['feed_off'])
        crm.off = False  # Salesflare support switched it on
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(self.store.events(['work-crm']), [])  # not asked before the next re-check
        self.an_hour_later()
        with self.assertLogs(a.LOG, 'INFO') as logged:
            self.run_to_completion(crm)
        self.assertIn('salesflare feed on again account=work-crm', ' '.join(logged.output))
        self.assertNotIn('feed off for team', ' '.join(logged.output))
        state = self.store.checkpoint('work-crm')
        self.assertNotIn('feed_off', state)
        self.assertEqual({r['source_id'] for r in self.store.events(['work-crm'])}, {'email:e1', 'meeting:7'})
        view = a.salesflare_progress(ACCOUNT, state)
        self.assertEqual((view['feed_off'], view['no_access_all'], view['no_access'], view['last_round']['read']), (False, False, 0, 2))
        asked = len(self.feeds_asked(crm))
        crm.accounts[10]['last_email_date'] = iso(0)  # a new email
        self.run_to_completion(crm)  # and the next round reads as usual, without waiting an hour
        self.assertGreater(len(self.feeds_asked(crm)), asked)

    def test_a_recheck_reads_the_whole_week_so_nothing_from_the_gap_is_missed(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        self.assertTrue(state['watermark'])  # an incremental round would start six hours before this
        crm.off = False
        self.an_hour_later()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        window = self.store.checkpoint('work-crm')['window']
        self.assertTrue(window['full'])
        self.assertLess(a.dt.datetime.fromisoformat(window['since']), NOW - a.dt.timedelta(days=6))

    def test_restart_sync_rechecks_a_team_refusal_right_away_once(self):
        crm = self.team_off()
        self.run_to_completion(crm)
        state = self.store.checkpoint('work-crm')
        state['next_full'] = 0  # what Restart sync on the card leaves (connector_sync)
        self.store.commit_page('work-crm', state, [], record_sync=False)
        crm.calls.clear()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(len(self.feeds_asked(crm)), 1)
        crm.calls.clear()
        a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        self.assertEqual(crm.calls, [])  # still off: back to the slow pace

    def test_a_403_body_message_is_kept_only_as_plain_words(self):
        from machine.sources import salesflare as sf
        import io

        def refused(body):
            return sf.refusal_message(sf.urllib.error.HTTPError('https://crm.example/x', 403, 'Forbidden', {}, io.BytesIO(body)))
        self.assertEqual(refused(b'{"statusCode":403,"error":"Forbidden","message":"Forbidden"}'), 'Forbidden')
        self.assertEqual(refused(b'{"message":"User 42 is not part of account"}'), 'other')
        self.assertEqual(refused(b'{"message":"kris@example.com"}'), 'other')
        self.assertEqual(refused(b'{}'), 'none')
        self.assertEqual(refused(b'<html>'), 'unreadable')
        source = sf.Salesflare({}, {**ACCOUNT, 'credential': 'salesflare', 'credential_variable': 'K'})
        error = sf.urllib.error.HTTPError('https://crm.example/accounts/7/feed', 403, 'Forbidden', {},
                                          io.BytesIO(b'{"message":"Forbidden"}'))
        with patch('machine.sources.salesflare.credential', return_value='K=secret'), \
                patch('machine.sources.salesflare.urllib.request.urlopen', side_effect=error), \
                self.assertRaises(sf.SourceError) as raised:
            source.get('/accounts/7/feed', {'types': 'email'})
        self.assertEqual((raised.exception.status, raised.exception.route, raised.exception.reason),
                         (403, '/accounts/{id}/feed', 'Forbidden'))

    def test_a_5xx_logs_its_route_with_ids_masked(self):
        from machine.sources import salesflare as sf
        self.assertEqual(sf.route_of('/accounts/123/feed'), '/accounts/{id}/feed')
        self.assertEqual(sf.route_of('/accounts/123'), '/accounts/{id}')
        self.assertEqual(sf.route_of('/accounts'), '/accounts')
        source = sf.Salesflare({}, {**ACCOUNT, 'credential': 'salesflare', 'credential_variable': 'K'})
        error = sf.urllib.error.HTTPError('https://crm.example/accounts/7/feed', 504, 'Gateway Timeout', {}, None)
        with patch('machine.sources.salesflare.credential', return_value='K=secret'), \
                patch('machine.sources.salesflare.urllib.request.urlopen', side_effect=error), \
                self.assertLogs(sf.LOG, 'WARNING') as logged, self.assertRaises(sf.SourceError) as raised:
            source.get('/accounts/7/feed', {'types': 'email'})
        self.assertEqual((raised.exception.status, raised.exception.route, str(raised.exception)),
                         (504, '/accounts/{id}/feed', 'salesflare:HTTP_504'))
        self.assertRegex(logged.output[0], r'salesflare answered route=/accounts/\{id\}/feed status=504 after=\d+s$')
        self.assertNotIn('7', logged.output[0].split('route=')[1].split()[0])
        # The sync's own failure line names the route too, not only salesflare:HTTP_504
        from machine.app.sync import error_route
        self.assertEqual(error_route(raised.exception), ' route=/accounts/{id}/feed')
        self.assertEqual(error_route(a.SourceError('salesflare', 504)), '')

    def test_a_feed_read_waits_a_minute_not_three(self):
        # A feed answers in about a second; a hang lasts until the gateway's 504 at 120 s. Account lists keep 180 s.
        import urllib.parse
        from machine.sources import salesflare as sf
        source = sf.Salesflare({}, {**ACCOUNT, 'credential': 'salesflare', 'credential_variable': 'K'})
        waits = []
        def urlopen(request, timeout):
            waits.append((sf.route_of(urllib.parse.urlsplit(request.full_url).path), timeout))
            raise TimeoutError()
        with patch('machine.sources.salesflare.credential', return_value='K=secret'), \
                patch('machine.sources.salesflare.urllib.request.urlopen', side_effect=urlopen):
            for path in ('/accounts/7/feed', '/accounts', '/accounts/7', '/me'):
                with self.assertRaises(sf.SourceError) as raised:
                    source.get(path, {'limit': 1})
                self.assertEqual(raised.exception.route, sf.route_of(path))
        self.assertEqual(waits, [('/accounts/{id}/feed', 60), ('/accounts', 180), ('/accounts/{id}', 180), ('/me', 60)])

    def test_a_profile_hiccup_after_a_recent_confirmation_does_not_fail_the_sync(self):
        # On a large team /me hangs now and then until Salesflare's gateway answers 504, like the other reads. A key
        # confirmed minutes before goes on; a first check, a refusal, another user or a changed key still fail.
        from machine.sources import salesflare as sf
        self.addCleanup(sf.SALESFLARE_CONFIRMED.clear)
        crm = FakeCRM()
        crm.key_fingerprint = lambda: 'key-1'
        hang = sf.SourceError('salesflare', 504, route='/me')
        with patch.object(crm, 'profile', side_effect=hang), self.assertRaises(sf.SourceError):
            a.sync_salesflare(self.store, {}, ACCOUNT, crm)  # never confirmed: fails as before
        self.assertTrue(a.sync_salesflare(self.store, {}, ACCOUNT, crm)['more'])  # confirmed
        with patch.object(crm, 'profile', side_effect=hang), self.assertLogs(sf.LOG, 'WARNING') as logged:
            self.assertFalse(a.sync_salesflare(self.store, {}, ACCOUNT, crm)['more'])  # the round goes on and ends
        self.assertRegex(logged.output[0], r'salesflare profile check skipped account=work-crm error=salesflare:HTTP_504 route=/me confirmed=\d+s ago')
        with patch.object(crm, 'profile', side_effect=sf.SourceError('network:TimeoutError:salesflare_read', route='/me')):
            a.sync_salesflare(self.store, {}, ACCOUNT, crm)  # a timeout is a hiccup too
        for error in (sf.SourceError('salesflare', 401, route='/me'), sf.SourceError('account_identity_mismatch')):
            with patch.object(crm, 'profile', side_effect=error), self.assertRaises(sf.SourceError):
                a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        crm.key_fingerprint = lambda: 'key-2'  # the owner pasted another key
        with patch.object(crm, 'profile', side_effect=hang), self.assertRaises(sf.SourceError):
            a.sync_salesflare(self.store, {}, ACCOUNT, crm)
        crm.key_fingerprint = lambda: 'key-1'
        sf.SALESFLARE_CONFIRMED['work-crm'] = ('key-1', sf.time.monotonic() - sf.SALESFLARE_PROFILE_TRUSTED - 1)
        with patch.object(crm, 'profile', side_effect=hang), self.assertRaises(sf.SourceError):
            a.sync_salesflare(self.store, {}, ACCOUNT, crm)  # confirmed too long ago

    def test_the_key_fingerprint_is_the_keys_and_never_the_key(self):
        from machine.sources import salesflare as sf
        source = sf.Salesflare({}, {**ACCOUNT, 'credential': 'salesflare', 'credential_variable': 'K'})
        with patch('machine.sources.salesflare.credential', return_value='K=secret'):
            first = source.key_fingerprint()
        with patch('machine.sources.salesflare.credential', return_value='K=other'):
            self.assertNotEqual(source.key_fingerprint(), first)
        self.assertNotIn('secret', first)


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

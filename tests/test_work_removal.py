import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)
import work_removal  # noqa: E402

NOW = '2026-10-21T10:00:00+00:00'
ACCOUNTS = [
    {'id': 'acme-gmail', 'service': 'gmail', 'email': 'alex@acme.com', 'boundary': 'work:Acme'},
    {'id': 'acme-calendar', 'service': 'calendar', 'email': 'alex@eu.acme.com', 'boundary': 'work:Acme'},
    {'id': 'acme-intercom', 'service': 'intercom', 'credential': 'intercom-acme', 'boundary': 'work:Acme'},
    {'id': 'side-gmail', 'service': 'gmail', 'email': 'alex@gmail.com', 'boundary': 'work:Acme'},
    {'id': 'personal-gmail', 'service': 'gmail', 'email': 'alex@gmail.com', 'boundary': 'personal:me'},
    {'id': 'other-slack', 'service': 'slack', 'email': 'alex@othercorp.com', 'boundary': 'work:Othercorp'},
]


def event(account, source, text):
    return {'account_id': account, 'source_id': source, 'kind': 'gmail.message', 'occurred_at': NOW, 'title': text,
            'body': text, 'metadata': {}, 'deleted': False}


class Matching(unittest.TestCase):
    def test_company_address_and_its_boundary_go_personal_and_other_companies_stay(self):
        found = {a['id']: why for a, why in work_removal.matching({'accounts': ACCOUNTS}, ['acme.com'], ['Acme'])}
        self.assertEqual(found, {'acme-gmail': 'address', 'acme-calendar': 'address', 'acme-intercom': 'boundary'})

    def test_boundary_alone_from_the_fleet_name_and_nothing_without_a_match(self):
        found = {a['id'] for a, _ in work_removal.matching({'accounts': ACCOUNTS}, [], ['ACME'])}
        self.assertEqual(found, {'acme-intercom'})  # without the domain an address in the boundary is not known to be theirs
        self.assertEqual(work_removal.matching({'accounts': ACCOUNTS}, ['example.org'], ['Nobody']), [])
        self.assertEqual(work_removal.matching({'accounts': ACCOUNTS}, ['not a domain', '@'], []), [])

    def test_the_owners_own_marking_comes_first(self):
        accounts = [dict(a) for a in ACCOUNTS] + [
            {'id': 'acme-personal', 'service': 'gmail', 'email': 'alex.home@acme.com', 'boundary': 'personal:me', 'boundary_by': 'owner'},
            {'id': 'marked-work', 'service': 'gmail', 'email': 'alex.acme@gmail.com', 'boundary': 'work:Acme', 'boundary_by': 'owner'},
            {'id': 'marked-other', 'service': 'gmail', 'email': 'alex@acme.com', 'boundary': 'work:Othercorp', 'boundary_by': 'owner'}]
        found = {a['id']: why for a, why in work_removal.matching({'accounts': accounts}, ['acme.com'], ['Acme'])}
        self.assertEqual(found, {'acme-gmail': 'address', 'acme-calendar': 'address', 'acme-intercom': 'boundary', 'marked-work': 'marked'})
        # A company named otherwise on the Machine: marked Work at its domain is enough
        renamed = [{'id': 'hq', 'service': 'gmail', 'email': 'alex@acme.com', 'boundary': 'work:Acme HQ', 'boundary_by': 'owner'},
                   {'id': 'hq-slack', 'service': 'slack', 'boundary': 'work:Acme HQ', 'boundary_by': 'owner'}]
        self.assertEqual({a['id'] for a, _ in work_removal.matching({'accounts': renamed}, ['acme.com'], ['Acme Inc'])}, {'hq', 'hq-slack'})


class Removal(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.db = self.dir / 'events.sqlite'
        secret = self.dir / 'intercom.env'
        secret.write_text('INTERCOM_TOKEN=x\n')
        self.config = {'database': str(self.db), 'accounts': [dict(a) for a in ACCOUNTS],
                       'credentials': {'intercom-acme': str(secret), 'api-token': str(self.dir / 'api-token')}}
        self.path = self.dir / 'config.json'
        self.path.write_text(json.dumps(self.config))
        self.store = assistant.Store(self.db)
        for account in ('acme-gmail', 'acme-intercom', 'personal-gmail'):
            self.store.commit_page(account, {'cursor': account}, [event(account, f'{account}-1', f'word{account.replace("-", "")} hello'),
                                                                  event(account, f'{account}-2', 'second')])
        with self.store.connect() as db:
            ids = {r['source_id']: r['id'] for r in db.execute('SELECT id,source_id FROM events')}
            cards = [('work', [ids['acme-gmail-1'], ids['acme-intercom-1']], ['acme-gmail', 'acme-intercom']),
                     ('mixed', [ids['acme-gmail-2'], ids['personal-gmail-1']], ['acme-gmail', 'personal-gmail']),
                     ('home', [ids['personal-gmail-2']], ['personal-gmail'])]
            for card, events, accounts in cards:
                db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at) VALUES(?,?,?,?,?,?,'pending',?)",
                           (card, card, card, card, json.dumps(events), json.dumps(accounts), NOW))
                db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'approve','','dashboard',?)",
                           ('d-' + card, card, NOW))
                db.execute("INSERT INTO decision_annotations(decision_id,status,reason) VALUES(?,'ok','')", ('d-' + card,))
                db.execute("INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_body,after_body,source,created_at) "
                           "VALUES(?,?,'a','b','edit','x','y','dashboard',?)", ('e-' + card, card, NOW))
                db.execute("INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,'sent',?)", (card, NOW))
            self.ids = ids

    def rows(self, sql, *args):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute(sql, args)]

    def test_removes_work_accounts_and_only_what_came_from_them(self):
        restarted = []
        result = work_removal.remove(self.path, ['acme.com'], ['Acme'], restart=lambda: restarted.append(1), store=self.store)
        self.assertEqual(sorted(a['id'] for a in result['accounts']), ['acme-calendar', 'acme-gmail', 'acme-intercom'])
        self.assertEqual((result['events'], result['cards'], result['drafts'], result['secrets']), (4, 1, 1, 1))
        self.assertEqual(restarted, [1])
        saved = json.loads(self.path.read_text())
        self.assertEqual([a['id'] for a in saved['accounts']], ['side-gmail', 'personal-gmail', 'other-slack'])
        self.assertNotIn('intercom-acme', saved['credentials'])
        self.assertIn('api-token', saved['credentials'])
        self.assertFalse((self.dir / 'intercom.env').exists())
        self.assertFalse(self.path.with_name('config.json.bak').exists())  # it still listed them
        self.assertEqual(self.rows('SELECT DISTINCT account_id FROM events'), [('personal-gmail',)])
        self.assertEqual(self.rows('SELECT id FROM suggestions ORDER BY id'), [('home',), ('mixed',)])
        self.assertEqual(self.rows('SELECT id FROM decisions ORDER BY id'), [('d-home',), ('d-mixed',)])
        self.assertEqual(self.rows('SELECT suggestion_id FROM draft_edits ORDER BY 1'), [('home',), ('mixed',)])
        self.assertEqual(self.rows('SELECT account_id FROM checkpoints'), [('personal-gmail',)])
        self.assertEqual(self.store.events(['acme-gmail', 'acme-intercom'], query='wordacmegmail'), [])
        self.assertEqual(len(self.store.events(['personal-gmail'], query='wordpersonalgmail')), 1)
        with self.store.connect() as db:
            db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")
        # The safety copy holds everything as it was, privately, until it is pruned
        folder = self.dir / 'work-removal-backups' / result['backup']
        self.assertEqual(len(json.loads((folder / 'config.json').read_text())['accounts']), len(ACCOUNTS))
        self.assertTrue((folder / 'events.sqlite').is_file())
        self.assertEqual(os.stat(folder).st_mode & 0o777, 0o700)
        self.assertEqual(os.stat(folder / 'events.sqlite').st_mode & 0o777, 0o600)
        old = time.time() - 8 * 86400
        os.utime(folder, (old, old))
        self.assertEqual(work_removal.prune(self.config), 1)
        self.assertFalse(folder.exists())

    def test_restart_after_config_save_finishes_the_removal(self):
        with mock.patch.object(work_removal, '_forget_google', side_effect=RuntimeError('interrupted')):
            with self.assertRaises(RuntimeError):
                work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store)
        saved = json.loads(self.path.read_text())
        self.assertNotIn('acme-gmail', [a['id'] for a in saved['accounts']])
        self.assertTrue((self.dir / work_removal.PENDING).is_file())
        result = work_removal.settle(saved, self.store)
        self.assertEqual(result['events'], 4)
        self.assertEqual(self.rows('SELECT DISTINCT account_id FROM events'), [('personal-gmail',)])

    def test_failed_recovery_note_flush_does_not_change_accounts_or_credentials(self):
        with mock.patch.object(work_removal.os, 'fsync', side_effect=OSError('flush failed')):
            with self.assertRaises(OSError):
                work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store)
        self.assertTrue((self.dir / 'intercom.env').is_file())
        self.assertIn('acme-gmail', [a['id'] for a in json.loads(self.path.read_text())['accounts']])

    def test_failed_config_save_does_not_delete_credentials(self):
        import onboarding
        with mock.patch.object(onboarding, 'save', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store)
        self.assertTrue((self.dir / 'intercom.env').is_file())
        self.assertIn('acme-gmail', [a['id'] for a in json.loads(self.path.read_text())['accounts']])

    def test_twice_finds_nothing_and_settle_removes_what_a_late_sync_stored(self):
        work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store)
        self.store.commit_page('acme-gmail', {'cursor': 'late'}, [event('acme-gmail', 'late', 'late one')])
        again = work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store)
        self.assertEqual((again['accounts'], again['events']), ([], 0))
        settled = work_removal.settle(json.loads(self.path.read_text()), self.store)
        self.assertEqual(settled['events'], 1)
        self.assertEqual(self.rows("SELECT COUNT(*) FROM events WHERE account_id='acme-gmail'"), [(0,)])
        self.assertIsNone(work_removal.settle(json.loads(self.path.read_text()), self.store))  # once

    def test_work_sign_ins_go_personal_ones_stay(self):
        token = self.dir / 'microsoft-alex-acme-com'
        token.write_text('{}')
        Path(str(token) + '.lock').write_text('')
        keyring = self.dir / 'keyring'
        keyring.mkdir()
        config = json.loads(self.path.read_text())
        config['gog_keyring_dir'] = str(keyring)
        config['credentials'].update({'microsoft-alex-acme-com': str(token), 'gog-password': str(self.dir / 'gog-password')})
        (self.dir / 'gog-password').write_text('pw')
        for a in config['accounts']:
            if a['id'] in ('acme-gmail', 'personal-gmail', 'side-gmail'):
                a.update(transport='gog', client='mine')
        config['accounts'].append({'id': 'acme-outlook', 'service': 'outlook', 'transport': 'graph', 'email': 'alex@acme.com',
                                   'credential': 'microsoft-alex-acme-com', 'boundary': 'work:Acme'})
        self.path.write_text(json.dumps(config))
        for email in ('alex@acme.com', 'alex@gmail.com'):
            assistant.gog_token_path(config, {'email': email, 'client': 'mine'}).write_text('token')
        calls = []
        def run(command, **kwargs):
            calls.append(command)
            self.assertEqual(kwargs['env']['GOG_KEYRING_PASSWORD'], 'pw')
            return type('Done', (), {'returncode': 0})()
        result = work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store, run=run)
        self.assertEqual(result['signins'], 2)
        self.assertEqual(calls, [['gog', 'auth', 'remove', 'alex@acme.com', '--client', 'mine', '--force', '--no-input']])
        self.assertFalse(assistant.gog_token_path(config, {'email': 'alex@acme.com', 'client': 'mine'}).exists())
        self.assertTrue(assistant.gog_token_path(config, {'email': 'alex@gmail.com', 'client': 'mine'}).exists())
        self.assertFalse(token.exists())
        self.assertFalse(Path(str(token) + '.lock').exists())
        self.assertNotIn('microsoft-alex-acme-com', json.loads(self.path.read_text())['credentials'])

    def test_marked_personal_at_the_company_domain_stays_with_its_sign_in(self):
        config = json.loads(self.path.read_text())
        for a in config['accounts']:
            if a['id'] == 'acme-gmail':
                a.update(transport='gog', client='mine', boundary='personal:me', boundary_by='owner')
        self.path.write_text(json.dumps(config))
        result = work_removal.remove(self.path, ['acme.com'], ['Acme'], store=self.store, run=lambda *a, **k: self.fail('kept'))
        self.assertNotIn('acme-gmail', [a['id'] for a in result['accounts']])
        self.assertEqual(result['signins'], 0)
        self.assertIn('acme-gmail', [a['id'] for a in json.loads(self.path.read_text())['accounts']])

    def test_no_match_changes_nothing(self):
        before = self.path.read_text()
        result = work_removal.remove(self.path, ['example.org'], ['Nobody'], store=self.store)
        self.assertEqual(result['accounts'], [])
        self.assertEqual(self.path.read_text(), before)
        self.assertFalse((self.dir / 'work-removal-backups').exists())


class Relay:
    """The control plane through the Network, faked: one waiting request, and what this Machine reports."""
    def __init__(self, error=None):
        self.calls, self.error = [], error

    def call(self, method, path, body=None, timeout=40):
        self.calls.append((method, path, body))
        if self.error:
            raise self.error
        if (method, path) == ('GET', '/removals'):
            return {'removals': [{'id': 'wr_1', 'fleet': 'Acme', 'domains': ['acme.com'], 'companies': ['Acme']}]}
        return {'ok': True}


class FleetRound(unittest.TestCase):
    def make(self, relay):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        store = assistant.Store(Path(temp.name) / 'events.sqlite')
        config = {'accounts': [], 'fleet': {'url': 'https://cp.example/api/fleet'}, 'credentials': {}}
        return assistant.fleet.Fleet(store.connect, config, lambda: 'token', relay=relay)

    def test_does_each_request_and_reports_counts_also_outside_any_fleet(self):
        relay, asked = Relay(), []
        machine = self.make(relay)
        self.assertEqual(machine.removals_round(clock=lambda: 0), [])  # nothing set up to remove with: not even asked
        self.assertEqual(relay.calls, [])
        machine.remove_work = lambda item: asked.append(item) or {'accounts': [{'id': 'acme-gmail'}], 'events': 3}
        self.assertEqual(machine.removals_round(clock=lambda: 0), ['wr_1'])
        self.assertEqual(asked[0]['domains'], ['acme.com'])
        self.assertEqual(relay.calls[-1], ('POST', '/removals', {'id': 'wr_1', 'result': {'ok': True, 'accounts': [{'id': 'acme-gmail'}], 'events': 3}}))
        self.assertEqual(machine.removals_round(clock=lambda: 60), [])  # not again within REMOVALS_EVERY
        machine.remove_work = lambda item: 1 / 0
        self.assertEqual(machine.removals_round(clock=lambda: 10_000), ['wr_1'])
        self.assertEqual(relay.calls[-1][2]['result'], {'ok': False, 'error': 'ZeroDivisionError'})

    def test_an_older_network_or_no_fleet_is_quiet(self):
        machine = self.make(Relay(error=assistant.fleet.Off()))
        machine.remove_work = lambda item: self.fail('nothing to do')
        self.assertEqual(machine.removals_round(clock=lambda: 0), [])

    def test_tells_the_network_it_can(self):
        relay = Relay()
        relay.call = lambda method, path, body=None, timeout=40: relay.calls.append((method, path, body)) or {'fleets': []}
        self.make(relay).directory(refresh=True)
        self.assertTrue(next(body for _, path, body in relay.calls if path == '/me')['remove_work'])


if __name__ == '__main__':
    unittest.main()

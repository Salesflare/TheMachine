"""A connection's two abilities (abilities.py): Brings in signals and Can do things. Made-up accounts, nothing reaches
Google, Microsoft or a broker: which connections get which switches, how they are saved (a connection from before keeps
both on), that Can do things off stops every action and read on demand, and Docs as an action-only connection."""
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import abilities
import assistant
from connectors import docs
import doc_writes
import mail_grants
import onboarding
from test_connectors import a
from test_connector_docs import ACCOUNT, GMAIL, OWNER, GoogleFake, helpers_for
from seams import patch_everywhere  # noqa: E402

SLACK = {'id': 'acme-slack', 'service': 'slack', 'transport': 'maton', 'boundary': 'work:Acme'}
RSS = {'id': 'news', 'service': 'rss', 'url': 'https://news.example/feed'}


class Kinds(unittest.TestCase):
    def test_which_connections_get_which_switches(self):
        self.assertEqual(abilities.view(GMAIL), {'abilities': ['signals', 'actions'], 'signals': True, 'actions': True,
                                                 'ability_switches': ['signals', 'actions']})
        self.assertEqual(abilities.view(ACCOUNT)['ability_switches'], ['signals', 'actions'])
        self.assertEqual(abilities.view(SLACK)['ability_switches'], ['actions'])  # its replies answer what it brings in
        self.assertEqual(abilities.view(RSS), {'abilities': ['signals'], 'signals': True, 'actions': False, 'ability_switches': []})
        shared = {**GMAIL, 'shared': {'fleet': 'f1'}}
        self.assertEqual(abilities.view(shared)['abilities'], ['signals'])  # a Fleet's share only reads

    def test_a_connection_from_before_has_both_on_and_off_is_only_an_explicit_false(self):
        self.assertTrue(abilities.actions_on(GMAIL) and abilities.signals_on(GMAIL))
        self.assertFalse(abilities.actions_on({**GMAIL, 'actions': False}))
        self.assertFalse(abilities.signals_on({**ACCOUNT, 'signals': False}))
        self.assertTrue(abilities.actions_on({**GMAIL, 'actions': None}))

    def test_switches_are_checked(self):
        both = {'signals': True, 'actions': False}
        self.assertEqual(abilities.check(GMAIL, both), {'signals': None, 'actions': False})
        for account, values, says in ((RSS, both, 'one ability'), (GMAIL, {'signals': False, 'actions': False}, 'Keep one on'),
                                      (GMAIL, {'signals': 'no', 'actions': True}, 'each on or off'),
                                      (GMAIL, {'signals': True}, 'each on or off'),
                                      (SLACK, {'signals': False, 'actions': True}, 'stays on')):
            with self.assertRaisesRegex(ValueError, says):
                abilities.check(account, values)

    def test_the_refusal_names_the_connection(self):
        config = {'accounts': [{**GMAIL, 'actions': False, 'display_name': 'Acme mail'}, SLACK, RSS]}
        self.assertIn('Acme mail', abilities.refuse(config, 'acme-gmail'))
        self.assertIsNone(abilities.refuse(config, 'acme-slack'))
        self.assertIsNone(abilities.refuse(config, 'news'))  # can't act anyway: nothing to refuse
        self.assertIsNone(abilities.refuse(config, 'gone'))


class Saved(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / 'config.json'
        owner = {'id': 'machine', 'service': 'rss', 'boundary': 'owner:system'}
        self.path.write_text(json.dumps({'accounts': [GMAIL, ACCOUNT, SLACK, owner], 'database': str(Path(tmp.name) / 'e.sqlite')}))
        self.app = object.__new__(assistant.App)
        self.app.config, self.app.config_path = json.loads(self.path.read_text()), self.path

    def saved(self, account_id):
        return next(x for x in json.loads(self.path.read_text())['accounts'] if x['id'] == account_id)

    def test_off_is_saved_as_false_and_on_drops_the_key(self):
        view = onboarding.set_abilities(self.path, 'acme-docs', {'signals': False, 'actions': True})
        self.assertEqual((view['signals'], view['actions']), (False, True))
        self.assertIs(self.saved('acme-docs')['signals'], False)
        onboarding.set_abilities(self.path, 'acme-docs', {'signals': True, 'actions': True})
        self.assertEqual(self.saved('acme-docs'), ACCOUNT)  # as it was before: nothing to migrate
        with self.assertRaisesRegex(onboarding.SetupError, 'Machine itself'):
            onboarding.set_abilities(self.path, 'machine', {'signals': True, 'actions': True})
        with self.assertRaisesRegex(onboarding.SetupError, 'stays on'):
            onboarding.set_abilities(self.path, 'acme-slack', {'signals': False, 'actions': True})

    def test_only_from_the_dashboard_and_it_restarts(self):
        with self.assertRaises(ValueError):
            self.app.action('connect_abilities', {'account': 'acme-gmail', 'signals': True, 'actions': False})
        with patch_everywhere(assistant, 'restart_self', return_value=True):
            view = self.app.action('connect_abilities', {'account': 'acme-gmail', 'signals': True, 'actions': False},
                                   owner_dashboard=True)
        self.assertEqual((view['actions'], view['restarting']), (False, True))
        self.assertIs(self.saved('acme-gmail')['actions'], False)
        with self.assertRaisesRegex(ValueError, 'not connected'):
            self.app.action('connect_abilities', {'account': 'gone', 'signals': True, 'actions': True}, owner_dashboard=True)


class Off(unittest.TestCase):
    """Can do things off: nothing offered, nothing confirmed, no doc written there; Brings in signals off: no sync."""

    def test_the_card_line_and_doc_targets(self):
        self.assertEqual(assistant.connector_says(GMAIL, 'gmail').get('acts'), 'send')
        self.assertNotIn('acts', assistant.connector_says({**GMAIL, 'actions': False}, 'gmail'))
        plugin = types.SimpleNamespace(writes_on=lambda config, account, helpers: {'create'}, provider=lambda config, account: 'google')
        config = {'accounts': [{**ACCOUNT, 'actions': False}, {**ACCOUNT, 'id': 'other-docs'}]}
        self.assertEqual(list(doc_writes.targets(config, plugin, None)), ['other-docs'])

    def test_with_signals_off_no_sync_runs_only_the_check_of_what_it_may_do(self):
        source = Path(assistant.__file__).read_text(encoding='utf-8')
        self.assertIn('target=self.collector if abilities.signals_on(account) else self.ability_checker', source)
        app, checked = object.__new__(assistant.App), []
        app.stop, app.store, app.config = assistant.threading.Event(), None, {'accounts': [ACCOUNT]}
        plugin = types.SimpleNamespace(refresh=lambda store, config, account, helpers: checked.append(account['id']) or app.stop.set())
        with patch_everywhere(assistant, 'load_connector', lambda name: plugin):
            app.ability_checker(ACCOUNT)
        self.assertEqual(checked, ['acme-docs'])

    def test_a_draft_for_it_is_refused_on_validate_and_on_confirm(self):
        import next_actions
        validate = Path(next_actions.__file__).read_text(encoding='utf-8').split('\ndef validate(', 1)[1].split('\ndef ', 1)[0]
        self.assertIn("abilities.refuse(config, result.get('account_id'))", validate)
        confirm = Path(assistant.__file__).read_text(encoding='utf-8').split('def confirm_action', 1)[1].split('\n    def ', 1)[0]
        self.assertIn('abilities.refuse(', confirm)


class DocsActionOnly(unittest.TestCase):
    """A Docs connection that only does things: finds and reads the docs a run needs, through the connection that can."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.account = {**ACCOUNT, 'signals': False}
        self.app = object.__new__(assistant.App)
        self.app.store = self.store
        self.app.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'accounts': [self.account],
                           'google_broker': {'url': 'https://cp.example/api/google/token'}}
        self.reads = []
        plugin = types.SimpleNamespace(
            provider=lambda config, account: 'google',
            find=lambda config, account, words, helpers: [{'file_id': 'found-doc-1', 'title': 'Q4 plan', 'url': None, 'at': None}],
            read_text=lambda config, account, file_id, helpers: self.reads.append(file_id) or {'title': 'Q4 plan', 'text': 'Week 2.'})
        patch_everywhere(assistant, 'load_connector', lambda name: plugin if name == 'docs' else None).start()
        patch.object(assistant.App, 'doc_run', lambda app, args: ('job-1', {'event_ids': '[]'}, {'linked-doc-1': 1}, doc_writes.area(app.config, ['acme-docs']))).start()
        self.addCleanup(patch.stopall)

    def test_finds_then_reads_only_what_it_found_or_the_task_links(self):
        with self.assertRaisesRegex(ValueError, 'doc-find'):
            self.app.doc_text({'job_id': 'job-1', 'file_id': 'never-seen-doc'})
        self.assertEqual(self.app.doc_find({'job_id': 'job-1', 'words': 'Q4 plan'})['docs'][0]['account_id'], 'acme-docs')
        self.assertEqual(self.app.doc_text({'job_id': 'job-1', 'file_id': 'found-doc-1'})['text'], 'Week 2.')
        self.app.doc_text({'job_id': 'job-1', 'file_id': 'linked-doc-1'})
        self.assertEqual(self.reads, ['found-doc-1', 'linked-doc-1'])

    def test_with_can_do_things_off_it_neither_finds_nor_reads(self):
        self.app.doc_find({'job_id': 'job-1', 'words': 'Q4'})
        self.account['actions'] = False
        with self.assertRaisesRegex(ValueError, 'can do things'):
            self.app.doc_find({'job_id': 'job-1', 'words': 'Q4'})
        with self.assertRaisesRegex(ValueError, 'Can do things is off'):
            self.app.doc_text({'job_id': 'job-1', 'file_id': 'found-doc-1'})
        with self.assertRaisesRegex(ValueError, 'can do things'):
            self.app.doc_text({'job_id': 'job-1', 'file_id': 'linked-doc-1'})
        self.assertEqual(self.reads, [])


class GoogleNarrow(unittest.TestCase):
    """Google without drive.readonly (a restricted scope): a doc by its id with documents.readonly, a search among the docs
    this app made with drive.file, and an hourly check of what it may do that counts as no sync."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'events.sqlite')
        self.config = {'database': str(Path(tmp.name) / 'events.sqlite'), 'google_broker': {'url': 'https://cp.example/api/google/token'},
                       'accounts': [{**ACCOUNT, 'signals': False}]}
        mail_grants.put(self.config, 'google', OWNER, 'refresh-1')
        import google_api
        google_api._tokens.clear()
        self.fake = GoogleFake(self)
        self.fake.granted = {docs.DOCS_READ_SCOPE, docs.FILE_SCOPE}
        patch('urllib.request.OpenerDirector.open', side_effect=self.fake.respond).start()
        self.addCleanup(patch.stopall)

    def scopes(self):
        return {r[1] for r in self.fake.requests if r[0] == 'BROKER' and r[1]}

    def test_reads_a_doc_by_its_id_and_finds_by_name(self):
        self.fake.suggestions = {}
        read = docs.read_text(self.config, self.config['accounts'][0], 'doc1', helpers_for())
        self.assertEqual(read['url'], 'https://docs.google.com/document/d/doc1/edit')
        found = docs.find(self.config, self.config['accounts'][0], "Q4 'plan", helpers_for())
        self.assertEqual([d['file_id'] for d in found], ['doc1', 'doc2'])
        query = next(r[2]['q'] for r in self.fake.requests if r[1] == '/drive/v3/files')
        self.assertIn("name contains 'Q4 \\'plan'", query)
        self.assertNotIn(docs.READ_SCOPE, self.scopes())  # never asks for the restricted scope it doesn't have
        self.assertEqual(docs.doc_links('see https://docs.google.com/document/d/abcdefghij1234567890/edit and again '
                                        'https://docs.google.com/document/d/abcdefghij1234567890'), ['abcdefghij1234567890'])

    def test_refresh_keeps_what_it_may_do_without_a_sync(self):
        docs.refresh(self.store, self.config, self.config['accounts'][0], helpers_for())
        state = self.store.checkpoint('acme-docs')
        self.assertEqual(state['provider'], 'google')
        self.assertIn('create', state['writes'])
        self.assertFalse([r for r in self.fake.requests if r[0] == 'GET' and 'comments' in r[1]])  # nothing read


if __name__ == '__main__':
    unittest.main()

"""A source nobody signed in to yet, or whose program isn't on this computer, says so on its card and never as a raw
FileNotFoundError. A new install starts the service before its first sign-in, so it read Gmail with no keyring password
saved yet: "FileNotFoundError" on Connections, twice in the error reports, five minutes apart."""
import os
import tempfile
import threading
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import assistant
import installer
import onboarding
import sources
from machine.app import ask_connections, status as machine_app_status
from machine.sources.android import Android
from machine.sources.connectors import CONNECTOR_HELPERS, load_connector
from machine.sources.gateway import GatewayJournal
from machine.sources.whatsapp import WhatsApp
from seams import patch_everywhere

GONE = '/nonexistent/program'


class Base(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        env = {k: v for k, v in os.environ.items() if k not in ('CREDENTIALS_DIRECTORY', 'GOG_KEYRING_PASSWORD')}
        for patcher in (patch.dict(os.environ, {**env, 'HOME': temp.name}, clear=True),):
            patcher.start()
            self.addCleanup(patcher.stop)

    def new_install(self, **facts):
        """config.json as the installer writes it, before the first sign-in."""
        paths = types.SimpleNamespace(home=self.home, data=self.home / 'data', workspace=self.home / 'ws')
        paths.data.mkdir(exist_ok=True)
        facts = {'gog': '/bin/false', 'openclaw': '/bin/false', 'node': '/bin/false', **facts}
        values = dict(owner_name='Sam', telegram_owner='', tailscale_owner='sam@acme.example', dashboard_host='desk.tailnet.example',
                      timezone='UTC', locale='', connectors='gmail,calendar', email='sam@acme.example', gog_client='default',
                      boundary='work:Acme', android_node_id='', whatsapp_store='')
        config = installer.refresh_install_paths(installer.new_config(values, facts, paths), facts, paths)
        config['database'] = str(paths.data / 'events.sqlite')
        return config

    def read(self, config, account, rounds=1):
        """The service's own collector for some rounds: (its checkpoint's row, its waits, the error reports, its failed syncs)."""
        app = object.__new__(assistant.App)
        app.config, app.store, app.stop, waits = config, assistant.Store(config['database']), threading.Event(), []

        def wait(seconds):
            waits.append(seconds)
            if len(waits) >= rounds:
                app.stop.set()
            return app.stop.is_set()
        app.stop.wait = wait
        app.collector(account)
        with app.store.connect() as db:
            row = dict(db.execute('SELECT error,failures,retry_at FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone())
            return (row, waits, [r['message'] for r in db.execute("SELECT message FROM error_feed WHERE source='sync'")],
                    db.execute("SELECT COUNT(*) FROM sync_activity WHERE status='failed'").fetchone()[0])


class NewInstall(Base):
    def test_before_the_first_sign_in_the_card_says_not_set_up_and_nothing_is_reported(self):
        config = self.new_install()
        for account in config['accounts']:
            row, waits, reported, failed = self.read(config, account, rounds=2)
            self.assertEqual(row, {'error': account['service'] + ':not_set_up', 'failures': 0, 'retry_at': None})
            self.assertEqual(waits, [30, 30])  # read soon after the sign-in, not a whole poll later
            self.assertEqual((reported, failed), ([], 0))

    def test_signed_in_but_the_program_is_gone(self):
        config = self.new_install()
        config['gog'] = GONE
        Path(config['credentials']['gog-password']).expanduser().parent.mkdir(parents=True, exist_ok=True)
        Path(config['credentials']['gog-password']).expanduser().write_text('fixture\n')
        account = config['accounts'][0]
        row, waits, reported, failed = self.read(config, account)
        self.assertEqual((row['error'], row['failures'], failed), ('gmail:not_installed', 1, 1))
        self.assertTrue(row['retry_at'])
        self.assertEqual(reported, ['gmail: not_installed'])

    def test_any_source_whose_key_file_is_not_there_yet(self):
        config = self.new_install()
        config['credentials']['notes'] = str(self.home / 'notes.key')
        account = {'id': 'notes', 'service': 'granola', 'credential': 'notes', 'boundary': 'work:Acme'}

        def reads(store, config, account):
            return sources.credential(config, 'notes')
        with patch_everywhere(assistant, 'sync_source', side_effect=reads):
            self.assertEqual(self.read(config, account)[0]['error'], 'granola:not_set_up')

    def test_another_missing_file_of_a_source_that_is_set_up_stays_an_error(self):
        config = self.new_install()
        (self.home / 'notes.key').write_text('fixture')
        config['credentials']['notes'] = str(self.home / 'notes.key')
        account = {'id': 'notes', 'service': 'granola', 'credential': 'notes', 'boundary': 'work:Acme'}
        with patch_everywhere(assistant, 'sync_source', side_effect=FileNotFoundError(2, 'no such file')), \
                patch.object(onboarding, 'missing', return_value=''):
            row, _, reported, failed = self.read(config, account)
        self.assertEqual((row['error'], reported, failed), ('FileNotFoundError', ['FileNotFoundError'], 1))


class Programs(Base):
    """Every source that runs a program says it isn't there, the same way."""

    def test_each_one(self):
        (self.home / 'pw').write_text('fixture')
        config = {'credentials': {'gog-password': str(self.home / 'pw')}, 'gog': GONE, 'gh': GONE, 'wacli': GONE, 'node': GONE,
                  'linkedin_inbox': GONE, 'x_inbox': GONE}
        google = {'id': 'g', 'email': 'sam@acme.example', 'client': 'default', 'transport': 'gog', 'node_id': 'n', 'store': str(self.home),
                  'handle': 'sam', 'login': 'sam'}
        docs, github, linkedin = (load_connector(s) for s in ('docs', 'github', 'linkedin'))
        reads = {
            'gmail': lambda: sources.gog_call(config, google, 'gmail', 'v1', 'gmail.users.getProfile', {}, 's'),
            'calendar': lambda: sources.gog_call(config, google, 'calendar', 'v3', 'calendars.get', {}, 's'),
            'github': lambda: github.Source(config, google, CONNECTOR_HELPERS).get('notifications'),
            'linkedin': lambda: linkedin.Source(config, google, CONNECTOR_HELPERS).run(['verify']),
            'whatsapp': lambda: WhatsApp(config, google).read(['auth', 'status']),
            'android': lambda: Android(config, google).snapshot(),
        }
        for service, read in reads.items():
            with self.subTest(service), self.assertRaises(sources.SourceError) as caught:
                read()
            self.assertEqual(str(caught.exception), service + ':not_installed')
        with patch('subprocess.run', side_effect=FileNotFoundError(2, 'x')), self.assertRaises(sources.SourceError) as caught:
            GatewayJournal({}).read(since='now')
        self.assertEqual(str(caught.exception), 'gateway:not_installed')
        with self.assertRaises(sources.SourceError) as caught:  # and the file of a WhatsApp message
            WhatsApp(config, google).download('123@s.whatsapp.net', 'ABC', self.home / 'f')
        self.assertEqual(str(caught.exception), 'whatsapp:not_installed')
        self.assertIn("SourceError('docs:not_installed')", Path(docs.__file__).read_text(encoding='utf-8'))
        self.assertNotIn('type(error).__name__', Path(load_connector('x').__file__).read_text(encoding='utf-8'))


class WhatToDo(Base):
    def test_the_command_and_the_hint(self):
        config = self.new_install()
        gmail = config['accounts'][0]
        self.assertEqual(onboarding.fix_command(config, gmail, 'gmail:not_set_up'), 'assistant connect gmail')
        self.assertEqual(onboarding.fix_command(config, gmail, 'gmail:not_installed'), 'assistant connect gmail')
        self.assertEqual(onboarding.fix_command(config, {'id': 'd', 'service': 'docs'}, 'docs:not_installed'), 'assistant connect gmail')
        self.assertTrue(onboarding.fix_command(config, {'id': 'p', 'service': 'android'}, 'android:not_installed').strip("'").endswith('/install.sh'))
        self.assertEqual(onboarding.fix_command(config, gmail, 'gmail:HTTP_403'), '')
        self.assertIn('assistant connect', onboarding.hint('gmail:not_set_up'))
        self.assertIn('gog (gogcli)', onboarding.hint('calendar:not_installed'))
        self.assertIn('gh', onboarding.hint('github:not_installed'))
        self.assertIn('wacli', onboarding.hint('whatsapp:not_installed'))
        self.assertIn('./install.sh', onboarding.hint('android:not_installed'))
        self.assertIn('./install.sh', onboarding.hint('gateway:not_installed'))
        self.assertIn('Gmail API', onboarding.hint('gmail:HTTP_403'))
        self.assertEqual(onboarding.missing(config, gmail), 'not signed in to Google yet')  # no file name on the dashboard

    def test_its_card_has_the_command_but_never_on_a_hosted_machine(self):
        config = self.new_install()
        app = object.__new__(assistant.App)
        app.config, app.store, app.config_path = config, assistant.Store(config['database']), None
        app.store.failed(config['accounts'][0]['id'], sources.SourceError('gmail:not_set_up'), 'gmail')
        card = next(c for c in app.status_connectors() if c['id'] == config['accounts'][0]['id'])
        self.assertEqual((card['error'], card['sign_in_command']), ('gmail:not_set_up', 'assistant connect gmail'))
        config['manage_url'] = 'https://app.example.com/setup'
        card = next(c for c in app.status_connectors() if c['id'] == config['accounts'][0]['id'])
        self.assertNotIn('sign_in_command', card)

    def test_ask_says_it_as_connections_does(self):
        def health(error):
            return ask_connections.health({'error': error}, {'service': 'gmail'}, lambda text, *args: text, None)[0]
        self.assertEqual(health('gmail:not_set_up'), 'Not set up yet')
        self.assertEqual(health('gmail:not_installed'), 'Needs your help')

    def test_the_line_on_top_names_no_file_and_is_the_only_one(self):
        items = {i['id']: i['text'] for i in machine_app_status.needs_you(self.new_install())}
        self.assertIn('is not fully set up yet (not signed in to Google yet)', items['setup-work-gmail'])
        self.assertNotIn('gog', ' '.join(items.values()))
        needs = (Path(onboarding.__file__).parent / 'dashboard' / 'shell-needs-you.js').read_text(encoding='utf-8')
        self.assertIn("!items.some(i=>i.id==='setup-'+c.id)", needs)  # no second line for the same connection


class InReach(Base):
    """The service's PATH isn't the terminal's."""

    def program(self, folder, name):
        path = self.home / folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('#!/bin/sh\n')
        path.chmod(0o755)
        return str(path)

    def test_connecting_keeps_where_it_is_and_finds_one_that_moved(self):
        gh = self.program('brew', 'gh')
        with patch.dict(os.environ, {'PATH': str(Path(gh).parent)}):
            for had in ({}, {'gh': 'gh'}, {'gh': GONE}):
                config = dict(had)
                self.assertEqual(onboarding.settle(config, 'gh'), gh)
                self.assertEqual(config['gh'], gh)
            own = self.program('own', 'gh')
            config = {'gh': own}  # one the owner chose and that is there stays
            self.assertEqual((onboarding.settle(config, 'gh'), config['gh']), (own, own))
        with patch.dict(os.environ, {'PATH': '/nonexistent'}):
            config = {}
            self.assertEqual((onboarding.settle(config, 'gh'), config), (None, {}))

    def test_an_install_run_again_finds_one_that_moved(self):
        here, own = self.program('new', 'gog'), self.program('own', 'gog')
        paths = types.SimpleNamespace(home=self.home, data=self.home, workspace=self.home)
        for had, kept in ((None, here), ('gog', here), (GONE, here), (own, own)):
            with patch.dict(os.environ, {'PATH': '/nonexistent'}):
                config = installer.refresh_install_paths({'gog': had} if had else {}, {'gog': here}, paths)
            self.assertEqual(config['gog'], kept)

    def test_the_services_path_has_gh_and_the_usual_places(self):
        for path in (installer.unit_path({'gh': '/opt/tools/gh'}), installer.service_path({'gh': '/opt/tools/gh'})):
            folders = path.split(':')
            self.assertEqual(folders[0], '/opt/tools')
            self.assertTrue(any(f.endswith('/go/bin') for f in folders))
        folders = installer.unit_path({}).split(':')
        self.assertIn('/home/linuxbrew/.linuxbrew/bin', folders)
        self.assertLess(folders.index('/usr/bin'), folders.index('/home/linuxbrew/.linuxbrew/bin'))  # nothing of the system's changes


if __name__ == '__main__':
    unittest.main()

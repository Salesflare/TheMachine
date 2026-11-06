"""Settings, Export (machine/app/export.py): export everything in the background, download it, delete it; upload an
export, open it with its passphrase, discard it or confirm it; a self-hosted Machine restarts itself and puts it in
place at its start (Replace with this export). Made-up data in a temporary home folder only."""
import io
import json
import os
import shutil
import sqlite3
import tempfile
import time
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import moving
from machine.app import export as export_app
from machine.export import staged as staged_import

HAS_OPENSSL = shutil.which('openssl') is not None


class FakeHandler:
    """What the mixin uses of assistant's Handler: headers, rfile, wfile, output and the raw response calls."""

    def __init__(self, body=b'', headers=None):
        self.headers = {'Content-Length': str(len(body)), **(headers or {})}
        self.rfile, self.wfile = io.BytesIO(body), io.BytesIO()
        self.status, self.sent, self.json, self.close_connection = None, {}, None, False

    def output(self, status, value, *_):
        self.status, self.json = status, value

    def send_response(self, status):
        self.status = status

    def send_header(self, name, value):
        self.sent[name] = value

    def end_headers(self):
        pass


class Machine(export_app.ExportApp):
    def __init__(self, config, config_path, paths):
        self.config, self.config_path, self.export_paths = config, config_path, paths


def wait(app, what, until):
    for _ in range(300):
        view = app.export_status()[what]
        if until(view):
            return view
        time.sleep(0.05)
    raise AssertionError(f'{what} never got there: {view}')


@unittest.skipUnless(HAS_OPENSSL, 'openssl is needed for an export')
class ExportSettings(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        env = patch.dict(os.environ, {'HOME': str(self.tmp / 'home')})
        env.start()
        self.addCleanup(env.stop)
        for target in ('own_connectors',):
            p = patch.object(moving, target, return_value=[])
            p.start()
            self.addCleanup(p.stop)
        self.data = self.tmp / 'home/.local/share/personal-assistant'
        self.data.mkdir(parents=True)
        with closing(sqlite3.connect(self.data / 'events.sqlite')) as db, db:
            db.execute('CREATE TABLE events(id TEXT, title TEXT)')
            db.executemany('INSERT INTO events VALUES (?, ?)', [('e1', 'Example subject'), ('e2', 'Another example')])
            db.execute('CREATE TABLE suggestions(id TEXT)')
            db.execute("INSERT INTO suggestions VALUES ('s1')")
        self.config_path = self.data / 'config.json'
        self.config = {'database': str(self.data / 'events.sqlite'), 'accounts': [{'id': 'mail', 'service': 'gmail'}]}
        self.config_path.write_text(json.dumps(self.config))
        space, claw = self.tmp / 'home/workspace', self.tmp / 'home/.openclaw'
        space.mkdir(parents=True)
        claw.mkdir(parents=True)
        (space / 'USER.md').write_text('About the owner\n')
        self.paths = {'workspace': space, 'openclaw_home': claw, 'home': self.tmp / 'home'}
        self.app = Machine(self.config, self.config_path, self.paths)

    def export(self, **args):
        started = self.app.export_start_action('export_start', args, True)
        self.assertTrue(started['started'])
        return wait(self.app, 'export', lambda v: v and v['state'] != 'running')

    def test_export_with_a_code_download_and_delete(self):
        view = self.export()
        self.assertEqual(view['state'], 'ready', view)
        self.assertRegex(view['code'], r'^[A-Z0-9]{4}(-[A-Z0-9]{4}){4}$')
        labels = {p['key']: p for p in view['parts']}
        self.assertEqual(labels['messages']['rows'], 2)
        self.assertEqual(labels['todos']['rows'], 1)
        self.assertTrue(any(n['what'].startswith('Telegram, Slack') for n in view['not_exported']))
        self.assertFalse(any(n['what'].startswith('~/') for n in view['not_exported']))
        # outside the data folder, private, and never in the next export
        out = self.data.parent / '.personal-assistant.export' / 'out'
        self.assertEqual(os.stat(out.parent).st_mode & 0o777, 0o700)
        self.assertNotIn(str(self.data), str(out))
        self.assertFalse((out / 'export.json').read_text().count(view['code']))  # the code stays in memory only
        # Download: the owner's own, by its id, streamed as a file
        wrong = FakeHandler()
        self.app.export_download(wrong, 'id=nope')
        self.assertEqual(wrong.status, 404)
        got = FakeHandler()
        self.app.export_download(got, 'id=' + view['id'])
        self.assertEqual(got.status, 200)
        self.assertEqual(got.sent['Content-Type'], 'application/octet-stream')
        self.assertIn('attachment', got.sent['Content-Disposition'])
        self.assertEqual(got.wfile.getvalue(), (out / view['name']).read_bytes())
        archive = self.tmp / 'moved.tar.gz.enc'
        archive.write_bytes(got.wfile.getvalue())
        # Delete: gone at once
        after = self.app.export_delete_action('export_delete', {}, True)
        self.assertIsNone(after['export'])
        self.assertFalse(out.exists())
        # Import that file on another (fresh) Machine: upload, a wrong code, the right one, the summary, confirm
        other_data = self.tmp / 'other/data'
        other_data.mkdir(parents=True)
        (other_data / 'config.json').write_text('{}')
        other = Machine({'manage_url': 'https://manage.example.test'}, other_data / 'config.json', self.paths)
        body = archive.read_bytes()
        up = FakeHandler(body, {'X-File-Name': 'the-machine-export.tar.gz.enc'})
        other.import_upload(up, True)
        self.assertEqual(up.status, 200, up.json)
        self.assertEqual(up.json['import']['state'], 'uploaded')
        self.assertTrue(up.json['hosted'])
        self.assertIsNone(up.json['export'])
        self.assertNotIn('commands', up.json)
        other.import_stage_action('import_stage', {'passphrase': 'AAAA-AAAA-AAAA-AAAA-AAAA'}, True)
        tried = wait(other, 'import', lambda v: v['state'] != 'checking')
        self.assertEqual(tried['state'], 'uploaded')
        self.assertTrue(tried['error'])
        other.import_stage_action('import_stage', {'passphrase': view['code'].lower()}, True)
        staged = wait(other, 'import', lambda v: v['state'] != 'checking')
        self.assertEqual(staged['state'], 'staged', staged)
        self.assertEqual({p['key']: p['rows'] for p in staged['parts']}['messages'], 2)
        self.assertFalse(staged['replaces'])
        self.assertFalse(other._upload_path().exists())  # only the checked, unpacked copy stays
        confirmed = other.import_confirm_action('import_confirm', {}, True)['import']
        self.assertEqual(confirmed['state'], 'confirmed')
        self.assertTrue(moving.staged(other.config_path)['confirmed'])  # what the hosted server's agent waits for
        other.import_discard_action('import_discard', {}, True)
        self.assertIsNone(moving.staged(other.config_path))

    def other_machine(self, archive, code):
        """A self-hosted Machine with a source of its own, the export uploaded and checked: (app, staged view)."""
        other_data = self.tmp / 'home/.local/share/other'
        other_data.mkdir(parents=True)
        with closing(sqlite3.connect(other_data / 'events.sqlite')) as db, db:
            db.execute('CREATE TABLE events(id TEXT, title TEXT)')
            db.execute("INSERT INTO events VALUES ('old', 'What this Machine had')")
        config = {'database': str(other_data / 'events.sqlite'), 'accounts': [{'id': 'old-mail', 'service': 'gmail'}]}
        (other_data / 'config.json').write_text(json.dumps(config))
        other = Machine(config, other_data / 'config.json', self.paths)
        up = FakeHandler(archive.read_bytes(), {'X-File-Name': 'the-machine-export.tar.gz.enc'})
        other.import_upload(up, True)
        other.import_stage_action('import_stage', {'passphrase': code}, True)
        return other, wait(other, 'import', lambda v: v['state'] != 'checking')

    def exported(self):
        view = self.export()
        got = FakeHandler()
        self.app.export_download(got, 'id=' + view['id'])
        archive = self.tmp / 'moved.tar.gz.enc'
        archive.write_bytes(got.wfile.getvalue())
        return archive, view['code']

    def test_self_hosted_replaces_itself_after_a_restart(self):
        archive, code = self.exported()
        other, staged = self.other_machine(archive, code)
        self.assertEqual(staged['state'], 'staged', staged)
        self.assertTrue(staged['replaces'])
        # Without systemd or launchd there is no button: the commands, and Import now refuses
        with patch.object(staged_import, 'can_restart', return_value=False):
            self.assertFalse(other.export_status()['restart'])
            with self.assertRaisesRegex(ValueError, 'commands'):
                other.import_confirm_action('import_confirm', {}, True)
        self.assertFalse(moving.staged(other.config_path).get('confirmed'))
        # Under a service manager: confirmed, and a restart of this service only (never the Gateway)
        restarts = []
        with patch.object(staged_import, 'can_restart', return_value=True), \
                patch.object(staged_import.service, 'manager', return_value='systemd'), \
                patch.object(staged_import.service, 'restart_later', side_effect=lambda unit, delay: restarts.append((unit, delay)) or True):
            self.assertTrue(other.export_status()['restart'])
            done = other.import_confirm_action('import_confirm', {}, True)
        self.assertTrue(done['restarting'])
        self.assertEqual(done['import']['state'], 'confirmed')
        self.assertEqual(len(restarts), 1)
        self.assertNotIn('gateway', restarts[0][0].lower())
        # The new process, before it serves: the export goes in place, a copy of what was there is kept
        self.assertIsNone(staged_import.apply_confirmed(other.config_path, {'manage_url': 'https://manage.example.test'}))
        result = staged_import.apply_confirmed(other.config_path, other.config)
        self.assertEqual(result['state'], 'imported', result)
        with closing(sqlite3.connect(other.config_path.parent / 'events.sqlite')) as db:
            self.assertEqual(sorted(r[0] for r in db.execute('SELECT id FROM events')), ['e1', 'e2'])
        self.assertTrue([p for p in other.config_path.parent.parent.iterdir() if p.name.startswith('other') and p.name != 'other'])
        self.assertIsNone(moving.staged(other.config_path))
        self.assertIsNone(staged_import.apply_confirmed(other.config_path, other.config))  # once only
        view = other.export_status()['import']
        self.assertEqual(view['state'], 'imported')
        self.assertTrue(view['reconnect'])
        self.assertEqual(os.stat(staged_import.result_path(other.config_path)).st_mode & 0o777, 0o600)
        other.import_discard_action('import_discard', {}, True)  # Done
        self.assertIsNone(other.export_status()['import'])

    def test_a_restart_that_cant_be_scheduled_or_an_import_refused_stays_staged(self):
        archive, code = self.exported()
        other, _ = self.other_machine(archive, code)
        with patch.object(staged_import, 'can_restart', return_value=True), patch.object(staged_import, 'restart', return_value=False):
            with self.assertRaisesRegex(ValueError, 'restart'):
                other.import_confirm_action('import_confirm', {}, True)
        self.assertFalse(moving.staged(other.config_path).get('confirmed'))
        staged_import.confirm(other.config_path)
        refused = staged_import.apply_confirmed(other.config_path, other.config,
                                                apply=lambda *_a, **_k: (_ for _ in ()).throw(moving.MoveError('The export is damaged')))
        self.assertEqual(refused['state'], 'failed')
        view = other.export_status()['import']
        self.assertEqual((view['state'], view['error']), ('staged', 'The export is damaged'))
        with closing(sqlite3.connect(other.config_path.parent / 'events.sqlite')) as db:
            self.assertEqual([r[0] for r in db.execute('SELECT id FROM events')], ['old'])

    def test_keys_need_a_passphrase_and_only_the_owner_exports(self):
        with self.assertRaises(ValueError):
            self.app.export_start_action('export_start', {'keys': True}, True)
        with self.assertRaises(ValueError):
            self.app.export_start_action('export_start', {'passphrase': 'short'}, True)
        for action in ('export_start', 'export_status', 'export_delete', 'import_stage', 'import_discard', 'import_confirm'):
            with self.assertRaises(ValueError):
                getattr(self.app, export_app.ExportApp.ACTIONS[action])(action, {}, False)
        refused = FakeHandler(b'x')
        self.app.import_upload(refused, False)
        self.assertEqual(refused.status, 403)
        view = self.export(passphrase='a long example passphrase', keys=True)
        self.assertEqual(view['state'], 'ready')
        self.assertNotIn('code', view)
        self.assertTrue(view['includes_keys'])
        # A self-hosted owner gets the commands, with --force where this Machine has sources already
        self.assertEqual(self.app.export_status()['commands'],
                         ['assistant service stop', 'assistant import --staged --force', 'assistant service start'])

    def test_hosted_exports_from_the_account_page(self):
        hosted = Machine({'manage_url': 'https://manage.example.test'}, self.config_path, self.paths)
        with self.assertRaises(ValueError):
            hosted.export_start_action('export_start', {}, True)
        self.assertTrue(hosted.export_status()['hosted'])

    def test_upload_checks_free_disk_and_a_cut_off_upload_leaves_nothing(self):
        small = FakeHandler(b'x' * 10)
        with patch.object(export_app.shutil, 'disk_usage', return_value=type('U', (), {'free': 1024})()):
            self.app.import_upload(small, True)
        self.assertEqual(small.status, 400)
        self.assertIn('free disk space', small.json['error'])
        cut = FakeHandler(b'x' * 10, {'Content-Length': '100'})
        self.app.import_upload(cut, True)
        self.assertEqual(cut.status, 400)
        self.assertIsNone(self.app.export_status()['import'])
        self.assertEqual(list(self.app._upload_path().parent.iterdir()), [])

    def test_an_export_older_than_a_day_is_shredded(self):
        view = self.export()
        path = self.data.parent / '.personal-assistant.export' / 'out' / view['name']
        old = time.time() - export_app.KEEP_HOURS * 3600 - 10
        os.utime(path, (old, old))
        self.assertIsNone(self.app.export_status()['export'])
        self.assertFalse(path.exists())


if __name__ == '__main__':
    unittest.main()

"""The sandbox (sandbox/): its fixture holds nothing real, its seal holds, and every state loads."""
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'sandbox'))
import check_fixture  # noqa: E402


class FixtureTest(unittest.TestCase):
    def test_fixture_is_current_and_clean(self):
        built = subprocess.run([sys.executable, str(ROOT / 'sandbox' / 'fixture.py')], capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(built), json.loads((ROOT / 'sandbox' / 'fixture.json').read_text()), 'run sandbox/fixture.py > sandbox/fixture.json')
        self.assertEqual(check_fixture.static_problems(built), [])

    def test_static_rules_catch_real_looking_values(self):
        self.assertTrue(check_fixture.static_problems('{"from": "Someone <someone@realcompany.com>"}'))
        self.assertTrue(check_fixture.static_problems('see https://realcompany.com/pricing'))
        self.assertTrue(check_fixture.static_problems('call me on +32 470 12 34 56'))
        self.assertEqual(check_fixture.static_problems('mail mila@northwind.example, https://mail.example/x'), [])

    def test_database_check_finds_real_names(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'real.sqlite'
            db = sqlite3.connect(path)
            db.execute('CREATE TABLE checkpoints(account_id TEXT)')
            db.execute('CREATE TABLE events(metadata TEXT)')
            db.execute('CREATE TABLE graph_nodes(kind TEXT, name TEXT)')
            db.execute("INSERT INTO checkpoints VALUES('acme-mail')")
            db.execute("INSERT INTO graph_nodes VALUES('person','Quentin Realperson'),('org','Acmeworks')")
            db.execute('INSERT INTO events VALUES(?)', (json.dumps({'from': 'Quentin Realperson <q@acmeworks.io>'}),))
            db.commit()
            db.close()
            found = check_fixture.real_identifiers(path)
            self.assertEqual(check_fixture.matches('Hi Quentin Realperson from Acmeworks', found), {'name': 1, 'company': 1})
            self.assertEqual(check_fixture.matches('q@acmeworks.io via acme-mail', found), {'email': 1, 'domain': 1, 'company': 1, 'account': 1})
            self.assertEqual(check_fixture.matches((ROOT / 'sandbox' / 'fixture.json').read_text(), found), {})


class SealTest(unittest.TestCase):
    def test_guard_refuses_the_world_and_programs(self):
        code = ('import sys,socket,subprocess;sys.path.insert(0,"sandbox");import guard;guard.install()\n'
                'for f in (lambda: socket.create_connection(("192.0.2.1",443),timeout=1), lambda: socket.getaddrinfo("example.com",443),'
                ' lambda: subprocess.run(["true"])):\n'
                '  try: f(); print("open")\n'
                '  except PermissionError: print("refused")\n')
        out = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True, timeout=30).stdout.split()
        self.assertEqual(out, ['refused'] * 3)


class StatesTest(unittest.TestCase):
    def test_every_state_loads(self):
        for state in ('fresh', 'reviews-off', 'busy', 'all,expired'):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as folder:
                code = f'import sys;sys.path.insert(0,"sandbox");import load;load.load({folder!r}, load.parse_states({state!r}))'
                subprocess.run([sys.executable, '-c', code], cwd=ROOT, check=True, capture_output=True, timeout=120)
                config = json.loads((Path(folder) / 'config.json').read_text())
                db = sqlite3.connect(Path(folder) / 'events.sqlite')
                cards = db.execute("SELECT count(*) FROM suggestions").fetchone()[0]
                errors = db.execute("SELECT count(*) FROM checkpoints WHERE error IS NOT NULL").fetchone()[0]
                self.assertEqual(config['review_worker']['enabled'], state != 'reviews-off')
                self.assertEqual(config['telegram_owner'], '')
                self.assertEqual(bool(config.get('fleet')), 'all' in state)
                self.assertEqual(cards == 0, state == 'fresh')
                self.assertEqual(errors, 2 if 'expired' in state else 0)
                self.assertTrue(config['fleet']['url'].startswith('http://127.0.0.1:') if config.get('fleet') else True)


class DemoMachineTest(unittest.TestCase):
    """sandbox/demo_machine.py: the made-up day in a real Machine's database, sealed, with no accounts added."""

    def test_loads_sealed_without_accounts_and_only_once(self):
        with tempfile.TemporaryDirectory() as folder:
            config = {'database': str(Path(folder) / 'events.sqlite'), 'accounts': [], 'owner_name': 'App review'}
            path = Path(folder) / 'config.json'
            path.write_text(json.dumps(config))
            code = (f'import os,sys;os.environ["HOME"]={folder!r};sys.path.insert(0,".");import assistant,message_seal;'
                    f'message_seal.load_key({config["database"]!r}, create=True);assistant.Store({config["database"]!r}, protect=True)')
            subprocess.run([sys.executable, '-c', code], cwd=ROOT, check=True, capture_output=True, timeout=60)
            run = lambda: subprocess.run([sys.executable, 'sandbox/demo_machine.py', '--config', str(path)], cwd=ROOT,
                                         capture_output=True, text=True, timeout=120, env={'HOME': folder, 'PATH': '/usr/bin:/bin'})
            done = run()
            self.assertEqual(done.returncode, 0, done.stderr[-2000:])
            counts = json.loads(done.stdout.strip().splitlines()[-1])
            self.assertGreater(counts['todos'], 10)
            self.assertGreater(counts['promises'], 3)
            self.assertEqual(json.loads(path.read_text()), config)  # no accounts, nothing else changed
            db = sqlite3.connect(config['database'])
            self.assertEqual(db.execute('SELECT count(*) FROM checkpoints').fetchone()[0], 0)  # nothing to sync
            titles = [r[0] for r in db.execute('SELECT title FROM events LIMIT 5')]
            self.assertFalse(any(isinstance(t, str) and 'Demo' in t for t in titles))  # sealed at rest, as on any Machine
            again = run()
            self.assertNotEqual(again.returncode, 0)
            self.assertIn('already has signals', again.stderr)


if __name__ == '__main__':
    unittest.main()

"""The parts that differ per operating system: file locks, the service manager (systemd, launchd) and the
support bundle. Runs on Linux, macOS and Windows."""
import json, os, plistlib, subprocess, sys, tarfile, tempfile, unittest
from pathlib import Path
from unittest import mock

import portable
import service
import support


def done(code=0, out='', err=''):
    return lambda args, **kw: subprocess.CompletedProcess(args, code, out, err)


class Recorder:
    def __init__(self, answers=None):
        self.calls, self.answers = [], answers or {}

    def __call__(self, args, **kwargs):
        self.calls.append(list(args))
        for prefix, (code, out) in self.answers.items():
            if ' '.join(args).startswith(prefix):
                return subprocess.CompletedProcess(args, code, out, '')
        return subprocess.CompletedProcess(args, 0, '', '')


class LockTest(unittest.TestCase):
    def test_a_held_lock_refuses_a_second_holder_until_released(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'x.lock'
            child = ('import sys, portable\n'
                     'h = open(sys.argv[1], "a")\n'
                     'try:\n    portable.lock(h, blocking=False)\nexcept BlockingIOError:\n    sys.exit(3)\n')
            with path.open('a') as held:
                portable.lock(held)
                again = subprocess.run([sys.executable, '-c', child, str(path)], cwd=Path(__file__).parent.parent)
                self.assertEqual(again.returncode, 3)
                portable.unlock(held)
            free = subprocess.run([sys.executable, '-c', child, str(path)], cwd=Path(__file__).parent.parent)
            self.assertEqual(free.returncode, 0)

    def test_a_group_ends_with_its_children(self):
        proc = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'], **portable.new_group())
        portable.end_group(proc)
        self.assertIsNotNone(proc.poll())


class SystemdTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {'ASSISTANT_SERVICE_MANAGER': 'systemd'})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_commands_are_the_systemd_user_ones(self):
        run = Recorder({'systemctl --user is-active': (0, 'active\n')})
        service.restart(run=run)
        service.stop(run=run)
        service.enable_now('the-machine-wacli-x.service', run=run)
        self.assertEqual(run.calls, [['systemctl', '--user', 'restart', 'personal-assistant.service'],
                                     ['systemctl', '--user', 'stop', 'personal-assistant.service'],
                                     ['systemctl', '--user', 'enable', '--now', 'the-machine-wacli-x.service']])
        self.assertEqual(service.hint('restart'), 'systemctl --user restart personal-assistant.service')
        self.assertEqual(service.hint('logs'), 'journalctl --user -u personal-assistant.service -n 50')
        self.assertTrue(str(service.definition_path(base='/h')).endswith(os.path.join('.config', 'systemd', 'user', 'personal-assistant.service')))

    def test_environment_reads_quoted_values(self):
        run = done(out='PATH=/a:/b "ASSISTANT_CONFIG=/x y/config.json" HOME=/h\n')
        self.assertEqual(service.environment(run=run), {'PATH': '/a:/b', 'ASSISTANT_CONFIG': '/x y/config.json', 'HOME': '/h'})


@unittest.skipIf(os.name != 'posix', 'launchd exists on macOS only; the plist and commands are checked on Linux and macOS')
class LaunchdTest(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp(prefix='machine-launchd-'))
        patcher = mock.patch.dict(os.environ, {'ASSISTANT_SERVICE_MANAGER': 'launchd', 'HOME': str(self.home)})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_agent_starts_at_login_restarts_and_logs_to_a_file(self):
        agent = plistlib.loads(service.plist_text(['/usr/bin/python3', '/app/assistant.py', 'serve'], workdir='/app',
                                                  env={'ASSISTANT_CONFIG': '/c.json'}).encode())
        self.assertEqual(agent['Label'], 'computer.themachine.assistant')
        self.assertTrue(agent['RunAtLoad'] and agent['KeepAlive'])
        self.assertEqual(agent['ProgramArguments'][-1], 'serve')
        self.assertEqual(agent['Umask'], 0o077)
        self.assertEqual(agent['StandardOutPath'], str(self.home / 'Library/Logs/TheMachine/assistant.log'))
        self.assertEqual(agent['EnvironmentVariables'], {'ASSISTANT_CONFIG': '/c.json'})
        self.assertEqual(service.definition_path(), self.home / 'Library/LaunchAgents/computer.themachine.assistant.plist')
        self.assertEqual(service.label('the-machine-wacli-personal-whatsapp.service'), 'computer.themachine.wacli-personal-whatsapp')

    def test_disable_survives_next_login_and_enable_clears_the_override_first(self):
        target = f'gui/{os.getuid()}/computer.themachine.assistant'
        run = Recorder()
        service.disable_now(run=run)
        self.assertIn(['launchctl', 'disable', target], run.calls)
        run = Recorder()
        service.enable(run=run)
        self.assertLess(run.calls.index(['launchctl', 'enable', target]),
                        run.calls.index(['launchctl', 'bootstrap', f'gui/{os.getuid()}', str(service.definition_path())]))

    def test_try_restart_does_not_start_a_stopped_loaded_agent(self):
        run = Recorder({'launchctl print': (0, 'state = not running\n')})
        service.try_restart(run=run)
        self.assertFalse(any(c[:2] == ['launchctl', 'kickstart'] for c in run.calls))

    def test_restart_stop_and_status_use_launchctl_in_the_gui_domain(self):
        target = f'gui/{os.getuid()}/computer.themachine.assistant'
        run = Recorder({'launchctl print': (0, 'state = running\n\tpid = 42\n')})
        service.restart(run=run)
        self.assertEqual(run.calls[-1], ['launchctl', 'kickstart', '-k', target])
        service.stop(run=run)
        self.assertEqual(run.calls[-1], ['launchctl', 'bootout', target])
        with mock.patch.object(service.shutil, 'which', return_value='/bin/launchctl'):
            self.assertTrue(service.active(run=run))
        self.assertIn('pid = 42', service.status_text(run=run))
        self.assertEqual(service.hint('restart'), 'assistant service restart')

    def test_a_stopped_agent_is_loaded_again_on_restart(self):
        service.definition_path().parent.mkdir(parents=True)
        service.definition_path().write_text('x')
        run = Recorder({'launchctl kickstart': (113, '')})
        service.restart(run=run)
        self.assertEqual(run.calls[-1], ['launchctl', 'bootstrap', f'gui/{os.getuid()}', str(service.definition_path())])

    def test_logs_come_from_the_agent_log_and_a_big_log_is_trimmed(self):
        log = service.log_path()
        log.parent.mkdir(parents=True)
        log.write_text(''.join(f'line {i}\n' for i in range(200)))
        self.assertEqual(service.logs(lines=2), 'line 198\nline 199')
        with mock.patch.object(service, 'LOG_LIMIT', 100), mock.patch.dict(os.environ, {'XPC_SERVICE_NAME': service.LABEL}):
            service.trim_log(keep=18)
        self.assertEqual(log.read_text(), 'line 198\nline 199\n')

    def test_the_installer_writes_an_agent_with_the_same_program_and_environment(self):
        import installer
        paths = installer.Paths(self.home)
        text = installer.agent_text({}, {'python': '/usr/bin/python3', 'node': '/opt/homebrew/bin/node'}, paths.config, paths)
        agent = plistlib.loads(text.encode())
        self.assertEqual(agent['ProgramArguments'], ['/usr/bin/python3', str(installer.ROOT / 'assistant.py'), 'serve'])
        self.assertEqual(agent['EnvironmentVariables']['ASSISTANT_CONFIG'], str(paths.config))
        self.assertTrue(agent['EnvironmentVariables']['PATH'].startswith('/opt/homebrew/bin:'))
        self.assertEqual(paths.unit, self.home / 'Library/LaunchAgents/computer.themachine.assistant.plist')


class DryRunTest(unittest.TestCase):
    def test_the_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as home:
            env = {k: v for k, v in os.environ.items() if not k.startswith(('ASSISTANT_', 'OPENCLAW_'))}
            env.update(HOME=home, USERPROFILE=home)
            result = subprocess.run([sys.executable, str(Path(__file__).parent.parent / 'installer.py'), '--dry-run'], env=env,
                                    capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(Path(home).iterdir()), [])
            self.assertIn('WSL2' if os.name == 'nt' else 'Dry run: nothing written', result.stdout)


class SupportBundleTest(unittest.TestCase):
    def test_secrets_and_addresses_stay_out(self):
        text = ('Authorization: Bearer abcdefghijklmnop1234 token=s3cr3t-value 123456789:AAEhBOweik6ad9r_QXMENQjcrGbqCr4K-ab '
                'alex@example.com sk-proj-abcdefghijklmnopqrstuv https://x.test/t/1#k=SECRETKEY /home/alex/.local/share/file.json')
        clean = support.scrub(text)
        for secret in ('abcdefghijklmnop1234', 's3cr3t-value', 'AAEhBOweik6ad9r', 'alex@example.com', 'sk-proj', 'SECRETKEY'):
            self.assertNotIn(secret, clean)
        self.assertIn('/home/alex/.local/share/file.json', clean)
        config = support.scrub_config({'port': 8787, 'telegram_owner': '1000001', 'credentials': {'api-token': '/p/api-token'},
                                       'accounts': [{'id': 'work-gmail', 'email': 'a@b.test', 'owner_emails': ['a@b.test']}]})
        self.assertEqual(config['port'], 8787)
        self.assertEqual(config['telegram_owner'], '<redacted>')
        self.assertEqual(config['accounts'][0], {'id': 'work-gmail', 'email': '<redacted>', 'owner_emails': ['<redacted>']})

    def test_the_bundle_is_one_private_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'config.json'
            config.write_text(json.dumps({'telegram_owner': '1000001', 'openclaw': ''}))
            with mock.patch.dict(os.environ, {'ASSISTANT_SERVICE_MANAGER': 'none'}), mock.patch.object(support.shutil, 'which', return_value=None):
                path = support.bundle(config, out=tmp, doctor=lambda _: [('✓', 'config ok', '')])
            with tarfile.open(path) as archive:
                names = {Path(n).name for n in archive.getnames()}
                body = b''.join(archive.extractfile(m).read() for m in archive.getmembers())
            self.assertTrue({'versions.txt', 'doctor.txt', 'config.json'} <= names)
            self.assertNotIn(b'1000001', body)
            if os.name == 'posix':
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)


if __name__ == '__main__':
    unittest.main()

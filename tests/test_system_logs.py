"""The computer's own logs (machine/system_logs.py): read only and local, only real problems become to-dos (routine
restarts stay silent, per the owner's decision of October 10, 2026), quietly, and no log text is ever kept. All records
here are synthetic."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from machine import system_logs as s

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('syslog_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
GATEWAY = {'id': 'openclaw-gateway', 'service': 'gateway'}
NOW = dt.datetime(2026, 11, 7, 12, 0, tzinfo=dt.timezone.utc)
UID = '1000'


def ago(minutes):
    return NOW - dt.timedelta(minutes=minutes)


def restart(unit, minutes):
    return {'MESSAGE_ID': s.RESTARTED, 'USER_UNIT': unit, 'at': ago(minutes)}


def result(unit, minutes, how='exit-code'):
    return {'MESSAGE_ID': s.RESULT, 'USER_UNIT': unit, 'UNIT_RESULT': how, 'at': ago(minutes)}


def crash(exe, minutes, cmdline=None, uid=UID, signal='11'):
    row = {'MESSAGE_ID': s.COREDUMP, 'COREDUMP_EXE': exe, 'COREDUMP_COMM': exe.rsplit('/', 1)[-1], 'COREDUMP_SIGNAL': signal,
           'COREDUMP_PID': '4242', 'COREDUMP_UID': uid, 'at': ago(minutes)}
    if cmdline is not None:
        row['COREDUMP_CMDLINE'] = cmdline
    return row


def detect(rows, failed=(), **kw):
    return s.detect(rows, failed, NOW, uid=UID, **kw)


class Detection(unittest.TestCase):
    def test_routine_restarts_and_single_failures_stay_silent(self):
        rows = [restart('sync-notes.service', 50), restart('sync-notes.service', 20), result('sync-notes.service', 21),
                result('backup.service', 300), result('backup.service', 30, 'success')]
        self.assertEqual(detect(rows), [])
        # five restarts spread over a day are routine too
        self.assertEqual(detect([restart('sync-notes.service', m) for m in (60, 300, 600, 900, 1200)]), [])

    def test_a_crash_loop_a_unit_systemd_gave_up_on_and_out_of_memory(self):
        loop = [restart('sync-notes.service', m) for m in (55, 45, 30, 20, 10)]
        [found] = detect(loop)
        self.assertEqual((found['kind'], found['name'], found['count'], found['key']), ('crash_loop', 'sync-notes', 5, 'crash_loop:sync-notes'))
        [found] = detect(loop + [result('sync-notes.service', 5, 'start-limit-hit')])
        self.assertEqual(found['kind'], 'gave_up')  # one to-do per unit: the clearest kind
        [found] = detect([result('indexer.service', 40, 'oom-kill')])
        self.assertEqual(found['kind'], 'out_of_memory')

    def test_repeated_failures_and_a_unit_that_stays_failed(self):
        self.assertEqual(detect([result('backup.service', m) for m in (600, 300)]), [])
        [found] = detect([result('backup.service', m) for m in (600, 300, 60)])
        self.assertEqual((found['kind'], found['count']), ('repeated_failures', 3))
        self.assertEqual(detect([result('backup.service', 10)], failed={'backup.service'}), [])  # just failed: may still come back
        [found] = detect([result('backup.service', 90)], failed={'backup.service'})
        self.assertEqual(found['kind'], 'stays_failed')
        [found] = detect([], failed={'backup.service'})  # failed before the window
        self.assertEqual((found['kind'], found['last_at']), ('stays_failed', None))

    def test_one_off_commands_and_app_scopes_that_exit_are_not_problems(self):
        rows = [result('run-u42.service', m) for m in (50, 40, 30)] + [result('app-Hyprland-editor-1a2b3c4d.scope', m) for m in (50, 40, 30)]
        self.assertEqual(detect(rows, failed={'run-u42.service'}), [])
        [found] = detect([result('app-Hyprland-editor-1a2b3c4d.scope', 30, 'oom-kill')])
        self.assertEqual((found['kind'], found['name']), ('out_of_memory', 'editor'))

    def test_a_crash_dump_counts_but_a_browsers_helpers_and_headless_test_browsers_do_not(self):
        rows = [crash('/usr/bin/examplebrowser', 30, '/usr/bin/examplebrowser --type=renderer'),
                crash('/usr/bin/examplebrowser', 20, '/usr/bin/examplebrowser --headless --remote-debugging-port=0'),
                crash('/usr/bin/notes-app', 600, '/usr/bin/notes-app'), crash('/usr/bin/notes-app', 10, '/usr/bin/notes-app'),
                crash('/usr/bin/other-users-app', 10, '/usr/bin/other-users-app', uid='1001')]
        [found] = detect(rows)
        self.assertEqual((found['kind'], found['name'], found['count'], found['signal'], found['pid']), ('crashed', 'notes-app', 2, 'SIGSEGV', '4242'))

    def test_without_a_command_line_one_crash_stays_quiet(self):
        # coredumpctl's own list has no command line, so a browser helper can't be told apart: two crashes or nothing
        self.assertEqual(detect([crash('/usr/bin/notes-app', 10)]), [])
        self.assertEqual(len(detect([crash('/usr/bin/notes-app', 10), crash('/usr/bin/notes-app', 5)])), 1)

    def test_omarchy_pieces_only_on_omarchy(self):
        rows = [crash('/usr/bin/quickshell', 10, 'quickshell -p /usr/share/omarchy/shell')]
        self.assertEqual(detect(rows, on_omarchy=True)[0]['piece'], 'bar')
        self.assertIsNone(detect(rows)[0]['piece'])
        found = detect([], on_omarchy=True, config_errors=2)
        self.assertEqual([(f['kind'], f['count']) for f in found], [('hyprland_config', 2)])
        self.assertEqual(detect([], config_errors=2), [])

    def test_unit_names_read_the_way_the_owner_knows_them(self):
        self.assertEqual(s.unit_name('app-Hyprland-gtk\\x2dlaunch-16f504ee.scope'), 'gtk-launch')
        self.assertEqual(s.unit_name('backup.service'), 'backup')
        self.assertEqual(s.unit_name('wayland-wm@hyprland.desktop.service'), 'wayland-wm@hyprland.desktop')


class Reading(unittest.TestCase):
    def test_it_asks_only_for_systemds_own_records_and_never_a_message(self):
        calls = []

        def run(args, timeout=None, env=None):
            calls.append(args)
            line = {'__REALTIME_TIMESTAMP': str(int(NOW.timestamp() * 1e6)), 'MESSAGE_ID': s.RESULT, 'USER_UNIT': 'backup.service',
                    'UNIT_RESULT': 'exit-code', 'MESSAGE': 'synthetic text that must not be kept'}
            return 0, json.dumps(line) + '\nnot json\n'
        [row] = s.read_journal(run=run)
        args = calls[0]
        self.assertEqual(args[:2], ['journalctl', '--user'])
        self.assertNotIn('sudo', args)
        self.assertIn('-n', args)
        fields = next(a for a in args if a.startswith('--output-fields='))
        self.assertNotIn('MESSAGE,', fields + ',')
        self.assertEqual(sorted(a for a in args if a.startswith('MESSAGE_ID=')), sorted(f'MESSAGE_ID={i}' for i in (s.RESTARTED, s.RESULT, s.COREDUMP)))
        self.assertNotIn('MESSAGE', row)
        self.assertIsNone(s.read_journal(run=lambda *a, **k: (1, '')))

    def test_coredumpctl_list_is_read_when_the_journal_has_no_crashes(self):
        listed = [{'pid': 7, 'uid': 1000, 'sig': 6, 'exe': '/usr/bin/notes-app', 'time': int(NOW.timestamp() * 1e6)}]
        rows = s.read_coredumps(run=lambda *a, **k: (0, json.dumps(listed)))
        self.assertEqual((rows[0]['COREDUMP_EXE'], rows[0]['COREDUMP_SIGNAL'], 'COREDUMP_CMDLINE' in rows[0]), ('/usr/bin/notes-app', '6', False))
        self.assertEqual(s.read_coredumps(run=lambda *a, **k: (1, '')), [])

    def test_other_systems_degrade_cleanly_and_nothing_runs(self):
        self.assertEqual(s.supported('darwin')[0], False)
        self.assertEqual(s.supported('win32')[0], False)
        self.assertEqual(s.supported('linux', which=lambda name: None)[0], False)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(s.supported('linux', which=lambda name: '/usr/bin/' + name, systemd_dir=Path(tmp) / 'none'),
                             (False, 'systemd is not running here'))  # WSL without systemd, a container
            self.assertEqual(s.supported('linux', which=lambda name: '/usr/bin/' + name, systemd_dir=tmp), (True, ''))
        with mock.patch.object(s, 'supported', return_value=(False, 'macOS keeps no systemd journal')):
            ran = []
            self.assertEqual(s.scan(run=lambda *a, **k: ran.append(a) or (0, ''))['findings'], [])
            self.assertEqual(ran, [])


class ToDos(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = a.Store(Path(tmp.name) / 'a.sqlite')
        self.config = {'accounts': [GATEWAY]}

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT id, title, body, status, origin FROM suggestions ORDER BY created_at, rowid')]

    def finding(self, kind='repeated_failures', name='backup', **extra):
        return dict({'key': f'{kind}:{name}', 'kind': kind, 'name': name, 'unit': name + '.service', 'count': 3,
                     'last_at': NOW.isoformat()}, **extra)

    def test_a_finding_reads_in_plain_words_with_its_fix_and_no_log_text(self):
        title, body, signal = s.card(self.finding())
        self.assertEqual(title, 'backup failed 3 times in a day')
        self.assertIn('journalctl --user -u backup.service -n 50', body)
        self.assertIn('waits for your OK', body)
        self.assertIn('Unit: backup.service', signal)
        title, body, _ = s.card(self.finding('crashed', 'quickshell', unit=None, program='quickshell', piece='bar', pid='4242', count=1),
                                which=lambda name: '/usr/bin/' + name)
        self.assertEqual(title, 'The bar crashed')
        self.assertIn('omarchy-restart-shell', body)
        self.assertIn('coredumpctl info 4242', body)

    def test_each_problem_comes_once_and_quietly(self):
        self.assertEqual(self.store.system_log_cards(GATEWAY['id'], [self.finding()]), 1)
        self.assertEqual(self.store.system_log_cards(GATEWAY['id'], [self.finding()]), 0)  # the same problem again: still open
        [todo] = self.todos()
        self.assertEqual((todo['title'], todo['origin']), ('backup failed 3 times in a day', 'machine'))
        with self.store.connect() as db:
            event = db.execute("SELECT kind, analyzed_version FROM events WHERE kind='machine.system_log'").fetchone()
        self.assertEqual(tuple(event), ('machine.system_log', 1))  # read already: no review makes another to-do
        self.assertEqual(a.todo_source('machine.system_log'), 'The Machine itself')
        # at most PER_DAY new ones a day, however many problems there are
        more = [self.finding('crashed', f'app{i}', unit=None, program=f'app{i}', pid='1', count=1) for i in range(4)]
        self.assertEqual(self.store.system_log_cards(GATEWAY['id'], more), s.PER_DAY - 1)

    def test_closed_comes_back_only_after_the_quiet_time(self):
        self.store.system_log_cards(GATEWAY['id'], [self.finding()])
        [todo] = self.todos()
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (todo['id'],))
        self.assertEqual(self.store.system_log_cards(GATEWAY['id'], [self.finding()], per_day=10), 0)
        with self.store.connect() as db:
            db.execute("UPDATE events SET ingested_at=?, source_id='syslog:repeated_failures:backup:2026-01-01' WHERE kind='machine.system_log'",
                       ((NOW - s.QUIET - dt.timedelta(days=300)).isoformat(),))
        self.assertEqual(self.store.system_log_cards(GATEWAY['id'], [self.finding()], per_day=10), 1)

    def test_the_gateway_source_reads_them_at_most_every_half_hour_and_can_be_off(self):
        class NoJournal:
            def read(self, cursor=None, since=None):
                return []
        scans = []
        scan = lambda: scans.append(1) or {'findings': [self.finding()]}
        with mock.patch('machine.sources.gateway.GatewayJournal', return_value=NoJournal()):
            a.sync_gateway(self.store, {**self.config, 'computer_logs': False}, GATEWAY, scan_logs=scan)
            self.assertEqual(scans, [])
            a.sync_gateway(self.store, self.config, GATEWAY, scan_logs=scan)
            a.sync_gateway(self.store, self.config, GATEWAY, scan_logs=scan)
            self.assertEqual(len(scans), 1)
            self.assertEqual(len(self.todos()), 1)
            a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())  # a test's own source: never the real logs
        self.assertEqual(len(scans), 1)

    def test_doctor_lines_are_scrubbed_like_learnings(self):
        lines = s.doctor_lines({'supported': True, 'omarchy': False, 'findings': [self.finding(name='mail-sam@example.com', unit='mail-sam@example.com.service')]})
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0][0], '!')
        self.assertNotIn('sam@example.com', ' '.join(lines[0]))
        self.assertEqual(s.doctor_lines({'supported': False, 'reason': 'macOS keeps no systemd journal', 'omarchy': False, 'findings': []})[0][0], '✓')
        self.assertEqual(s.doctor({'computer_logs': False}, scan_logs=lambda: self.fail('read while off')), [])


if __name__ == '__main__':
    unittest.main()

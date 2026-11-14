"""machine/upkeep/memory_rebuild.py: OpenClaw's memory rebuild that never ends by itself, and the quiet night for it.
Everything against a temporary OpenClaw folder, log and a fake `openclaw cron`; nothing touches this computer's."""
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile
import time
import unittest
from unittest import mock
from zoneinfo import ZoneInfo

from machine.app.model_pacing import ModelPacingApp
from machine.app.workers import WorkersApp
from machine.upkeep import memory_rebuild

TZ = ZoneInfo('Europe/Brussels')
GEMMA = '/models/hf_ggml-org_embeddinggemma-300M-Q8_0.gguf'


def at(hour, day=14, minute=5):
    return dt.datetime(2026, 11, day, hour, minute, tzinfo=TZ)


class FakeCron:
    """`openclaw cron list|enable|disable` over a few jobs; `down` makes the Gateway not answer."""

    def __init__(self, jobs):
        self.jobs = {job['id']: job for job in jobs}
        self.calls, self.down = [], False

    def __call__(self, command, **kwargs):
        self.calls.append(command[1:])
        if self.down:
            return subprocess.CompletedProcess(command, 1, '', 'gateway closed')
        if command[1:3] == ['cron', 'list']:
            listed = [job for job in self.jobs.values() if job['enabled']]
            return subprocess.CompletedProcess(command, 0, json.dumps({'jobs': listed, 'total': len(listed)}), '')
        if command[1:3] in (['cron', 'enable'], ['cron', 'disable']):
            self.jobs[command[3]]['enabled'] = command[2] == 'enable'
            return subprocess.CompletedProcess(command, 0, '{}', '')
        return subprocess.CompletedProcess(command, 1, '', 'unknown')

    def enabled(self):
        return sorted(job_id for job_id, job in self.jobs.items() if job['enabled'])


def job(job_id, kind, enabled=True):
    return {'id': job_id, 'enabled': enabled, 'payload': {'kind': kind}}


class MemoryRebuildTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='machine-memory-rebuild-'))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.state = self.tmp / 'openclaw'
        self.agent = self.state / 'agents' / 'main' / 'agent'
        self.agent.mkdir(parents=True)
        self.data = self.tmp / 'data'
        self.data.mkdir()
        self.logs = self.tmp / 'logs'
        self.logs.mkdir()
        env = mock.patch.dict(os.environ, {'ASSISTANT_OPENCLAW_LOG_DIR': str(self.logs)})
        env.start()
        self.addCleanup(env.stop)
        self.settings = {'memory': {'search': {'provider': 'local'}}}
        self.save_meta(0)
        self.cron = FakeCron([job('beat', 'heartbeat'), job('brief', 'agentTurn'), job('backup', 'command'),
                              job('sync', 'script'), job('old', 'agentTurn', enabled=False)])

    def save_meta(self, version, model=GEMMA, provider='local'):
        with sqlite3.connect(self.agent / 'openclaw-agent.sqlite') as db:
            db.execute('CREATE TABLE IF NOT EXISTS memory_index_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
            db.execute('INSERT OR REPLACE INTO memory_index_meta VALUES (?, ?)', ('memory_index_meta_v1', json.dumps(
                {'provider': provider, 'model': model, 'embeddingInputFormatVersion': version, 'chunkingVersion': 6})))
            db.execute('INSERT OR REPLACE INTO memory_index_meta VALUES (?, ?)', ('memory_vector_rebuild_v1', 'clean'))

    def log(self, day, *times):
        lines = [json.dumps({'0': '{"subsystem":"memory"}', '1': 'memory sync failed (watch): MemoryBackgroundRebuildInterruptedError: '
                             'Memory background rebuild interrupted by foreground activity', 'time': t}) for t in times]
        lines.append(json.dumps({'0': '{"subsystem":"gateway"}', '1': 'ready', 'time': times[0] if times else f'{day}T00:00:00.000+01:00'}))
        with open(self.logs / f'openclaw-{day}.log', 'a') as out:
            out.write('\n'.join(lines) + '\n')

    def step(self, local_now, hours=memory_rebuild.WINDOW):
        return memory_rebuild.step(self.data, 'openclaw', self.settings, self.state, local_now.timestamp(), local_now, hours, self.cron)

    def test_stuck_on_an_older_input_format_or_on_tries_cut_off(self):
        now = at(8).timestamp()
        self.assertEqual(memory_rebuild.stuck(self.settings, [self.agent], now), {'format_behind': True, 'interrupted': 0})
        self.save_meta(1)
        self.assertIsNone(memory_rebuild.stuck(self.settings, [self.agent], now))
        self.log('2026-11-13', '2026-11-13T04:15:58.249+01:00', '2026-11-13T09:33:32.282+01:00', '2026-11-13T22:45:45.599+01:00')
        self.log('2026-11-14', '2026-11-14T03:51:46.001+01:00', '2026-11-14T07:58:13.608+01:00')
        found = memory_rebuild.stuck(self.settings, [self.agent], now)
        self.assertEqual(found, {'format_behind': False, 'interrupted': 4})  # the day before: only the last 24 hours count
        self.assertIsNone(memory_rebuild.stuck(self.settings, [self.agent], at(8, day=16).timestamp()))
        self.assertIsNone(memory_rebuild.stuck({'memory': {'search': {'provider': 'openai'}}}, [self.agent], now))  # remote: not hours
        self.save_meta(0, model='nomic-embed-text')  # a model whose format did not change
        self.assertIsNone(memory_rebuild.stuck(self.settings, [self.agent], at(8, day=16).timestamp()))
        self.assertEqual(memory_rebuild.agent_dirs({'agents': {'list': [{'agentDir': str(self.tmp / 'x')}]}}, self.state),
                         [self.agent, self.tmp / 'x'])

    def test_a_log_file_openclaw_json_names_is_read(self):
        path = self.tmp / 'gateway.log'
        path.write_text(json.dumps({'1': 'MemoryBackgroundRebuildInterruptedError', 'time': '2026-11-14T07:00:00+01:00'}) + '\nnot json MemoryBackgroundRebuildInterruptedError\n')
        settings = {**self.settings, 'logging': {'file': str(path)}}
        self.assertEqual(memory_rebuild.log_files(settings, dt.date(2026, 11, 14)), [path])
        self.assertEqual(memory_rebuild.interruptions([path], at(0).timestamp()), 1)  # a line without its time is not counted

    def test_a_stuck_rebuild_gets_one_quiet_night(self):
        self.assertIsNone(self.step(at(22, minute=50)))  # not yet
        self.assertEqual(self.step(at(23, minute=0)), 'opened')
        self.assertEqual(self.cron.enabled(), ['backup', 'sync'])  # the heartbeat and the job's turns are off; scripts and commands run
        held = memory_rebuild.holding(self.data, at(23, minute=30).timestamp())
        self.assertEqual(held['until'], at(7, day=15, minute=0).timestamp())
        self.assertEqual(self.step(at(23, minute=10)), 'open')
        # a rebuild that runs: still open, also once the saved index is past the format
        shadow = self.agent / 'openclaw-agent.sqlite.memory-reindex-8762fa68-b86f-4bd0-a19b-7e1a4dae71d1'
        shadow.write_text('')
        os.utime(shadow, (at(3, day=15).timestamp(),) * 2)
        self.save_meta(1)
        self.assertEqual(self.step(at(3, day=15, minute=1)), 'open')
        shadow.unlink()  # OpenClaw published the rebuilt index and removed its copy
        self.assertEqual(self.step(at(3, day=15, minute=11)), 'done')
        self.assertEqual(self.cron.enabled(), ['backup', 'beat', 'brief', 'sync'])  # every job it turned off is on again
        self.assertFalse(self.cron.jobs['old']['enabled'])  # one the owner had off stays off
        self.assertIsNone(memory_rebuild.holding(self.data, at(3, day=15, minute=12).timestamp()))
        self.assertIsNone(self.step(at(23, day=15)))  # done: not stuck any more, no window the next night

    def test_the_window_ends_at_its_hour_and_opens_once_a_night(self):
        self.assertEqual(self.step(at(23)), 'opened')
        self.assertEqual(self.step(at(6, day=15, minute=55)), 'open')  # still in the old format, nothing published
        self.assertEqual(self.step(at(7, day=15, minute=0)), 'ended')
        self.assertEqual(self.cron.enabled(), ['backup', 'beat', 'brief', 'sync'])
        self.assertIsNone(memory_rebuild.holding(self.data, at(7, day=15, minute=1).timestamp()))
        self.assertEqual(memory_rebuild.read_state(self.data)['outcome'], 'ended')
        self.assertEqual(self.step(at(23, day=15, minute=0)), 'opened')  # the next night tries again
        self.assertEqual(memory_rebuild.read_state(self.data)['night'], '2026-11-15')
        self.assertEqual(self.step(at(23, day=15, minute=20), hours=None), 'ended')  # ended early
        self.assertIsNone(self.step(at(23, day=15, minute=30)))  # once a night

    def test_jobs_that_did_not_turn_on_again_are_retried_and_nothing_opens_without_the_gateway(self):
        self.assertEqual(self.step(at(23)), 'opened')
        self.cron.down = True
        self.assertEqual(self.step(at(7, day=15)), 'ended')
        self.assertEqual(sorted(memory_rebuild.read_state(self.data)['jobs']), ['beat', 'brief'])
        self.assertIsNone(memory_rebuild.holding(self.data, at(7, day=15, minute=1).timestamp()))  # holds nothing meanwhile
        self.cron.down = False
        self.assertEqual(self.step(at(7, day=15, minute=10)), 'closing')
        self.assertEqual(self.cron.enabled(), ['backup', 'beat', 'brief', 'sync'])
        self.assertEqual(memory_rebuild.read_state(self.data)['jobs'], [])
        (self.data / memory_rebuild.STATE).unlink()
        self.cron.down = True
        self.assertIsNone(self.step(at(23, day=15)))
        self.assertFalse((self.data / memory_rebuild.STATE).exists())

    def test_turned_off_it_closes_an_open_window_and_never_opens_one(self):
        self.assertEqual(self.step(at(23)), 'opened')
        self.assertEqual(self.step(at(23, minute=30), hours=None), 'ended')
        self.assertEqual(self.cron.enabled(), ['backup', 'beat', 'brief', 'sync'])
        (self.data / memory_rebuild.STATE).unlink()
        self.assertIsNone(self.step(at(23, day=15), hours=None))
        self.assertEqual(memory_rebuild.window_bounds(at(1), (1, 6))[1], at(6, minute=0))

    def test_only_background_turns_wait_while_it_is_open(self):
        class App(ModelPacingApp, WorkersApp):
            pass
        app = App.__new__(App)
        app.config = {'review_worker': {'enabled': True}}
        app.store = mock.Mock(path=str(self.data / 'assistant.sqlite'))
        app.model_usage, app.usage_limit, app.pacing = None, None, None
        with mock.patch.object(App, 'fallback_covers', return_value=None):
            self.assertIsNone(app.background_pause(job='review'))
            memory_rebuild.write_state(self.data, {'opened': time.time(), 'until': time.time() + 3600, 'jobs': []})
            held = app.background_pause(job='review', signals=True)
            self.assertEqual((held['window'], held['limited']), ('memory', False))
            self.assertIsNone(app.background_pause(owner=True))  # the owner's own turns go
            app.review_paused = held
            self.assertIsNone(app.review_pause())  # no budget banner for it
        self.assertEqual(App.memory_rebuild_hours(app), (23, 7))
        app.config['memory_rebuild_hours'] = False
        self.assertIsNone(App.memory_rebuild_hours(app))
        app.config['memory_rebuild_hours'] = [1, 6]
        self.assertEqual(App.memory_rebuild_hours(app), (1, 6))


if __name__ == '__main__':
    unittest.main()

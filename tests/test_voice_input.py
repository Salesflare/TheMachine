"""Voice input (voice_input.py): the clip checks, Settings, the first-use preparation, the local worker, the OpenAI path
and the API. Whisper itself never runs here: the worker, pip and the downloads are stubbed."""
import base64
import hashlib
import http.client
import importlib.util
import io
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import threading
import time
import unittest
import wave
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('voice_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
v = a.voice_input


def wav(seconds=1.0, rate=16000, channels=1, width=2):
    out = io.BytesIO()
    with wave.open(out, 'wb') as clip:
        clip.setnchannels(channels)
        clip.setsampwidth(width)
        clip.setframerate(rate)
        clip.writeframes(b'\x01\x00' * int(seconds * rate) * channels * (width // 2))
    return out.getvalue()


class Clip(unittest.TestCase):
    def test_a_dashboard_clip_is_read(self):
        frames, seconds = v.pcm(wav(1.5))
        self.assertEqual(len(frames), 1.5 * 16000 * 2)
        self.assertAlmostEqual(seconds, 1.5)

    def test_anything_else_is_refused_with_what_to_do(self):
        for data in (b'', b'not a wav', wav(1, rate=48000), wav(1, channels=2), wav(1, width=1)):
            with self.assertRaisesRegex(ValueError, 'couldn’t be read'):
                v.pcm(data)
        with self.assertRaisesRegex(ValueError, 'too short'):
            v.pcm(wav(0.1))
        with self.assertRaisesRegex(ValueError, 'up to 2 minutes'):
            v.pcm(wav(v.MAX_SECONDS + 6))
        v.pcm(wav(v.MAX_SECONDS + 1))   # the browser stops at 2:00, give or take its rounding

    def test_the_request_limit_fits_a_whole_clip(self):
        body = json.dumps({'action': 'voice_transcribe', 'args': {'data': base64.b64encode(wav(v.MAX_SECONDS + 1)).decode()}})
        self.assertLess(len(body), v.REQUEST_BYTES)

    def test_what_lands_in_the_box_is_plain_text(self):
        self.assertEqual(v.clean('  Hello\x00  there\t\tagain \x1b[31m '), 'Hello there again [31m')
        self.assertEqual(v.clean(None), '')


class Prefs(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')

    def test_defaults_and_choices(self):
        with self.store.connect() as db:
            self.assertEqual(v.prefs(db), {'engine': 'auto', 'model': 'small', 'language': ''})
            self.assertEqual(v.set_prefs(db, {'model': 'base', 'language': 'nl'}, False),
                             {'engine': 'auto', 'model': 'base', 'language': 'nl'})
            self.assertEqual(v.set_prefs(db, {'engine': 'local'}, False)['engine'], 'local')
            self.assertEqual(v.set_prefs(db, {'language': ''}, False)['language'], '')
            for args in ({'engine': 'google'}, {'model': 'large'}, {'language': 'xx'}):
                with self.assertRaises(ValueError):
                    v.set_prefs(db, args, True)
            with self.assertRaisesRegex(ValueError, 'OpenAI set up in OpenClaw'):
                v.set_prefs(db, {'engine': 'openai'}, False)
            self.assertEqual(v.set_prefs(db, {'engine': 'openai'}, True)['engine'], 'openai')
            db.execute("UPDATE voice_prefs SET value='gone' WHERE key='engine'")
            self.assertEqual(v.prefs(db)['engine'], 'auto')

    def test_automatic_uses_openai_when_there_is_one(self):
        auto, local, openai = ({'engine': e} for e in ('auto', 'local', 'openai'))
        self.assertEqual(v.engine_for(auto, True), 'openai')
        self.assertEqual(v.engine_for(auto, False), 'local')
        self.assertEqual(v.engine_for(auto, None), 'local')
        self.assertEqual(v.engine_for(local, True), 'local')   # the owner picked privacy
        self.assertEqual(v.engine_for(openai, True), 'openai')

    def test_the_local_model_is_only_ever_fetched_when_it_will_be_used(self):
        missing, ready, failed = {'state': 'missing'}, {'state': 'ready'}, {'state': 'failed'}
        self.assertFalse(v.warm_due({'engine': 'auto'}, True, missing, True))    # OpenAI here: never, not even later
        self.assertFalse(v.warm_due({'engine': 'openai'}, False, missing, True))
        self.assertTrue(v.warm_due({'engine': 'auto'}, False, missing, True))
        self.assertTrue(v.warm_due({'engine': 'local'}, True, failed, True))     # On this Machine picked
        self.assertFalse(v.warm_due({'engine': 'local'}, True, ready, True))
        self.assertFalse(v.warm_due({'engine': 'local'}, True, missing, False))  # no room on disk
        self.assertTrue(v.idle(0.5, 2))
        self.assertFalse(v.idle(1.5, 2))
        self.assertFalse(v.idle(3.0, 4))


TINY = {'tiny': {'repo': 'example/tiny', 'revision': 'abc', 'files': {
    'config.json': (5, hashlib.sha256(b'{"a"}').hexdigest()),
    'model.bin': (6, hashlib.sha256(b'MODEL!').hexdigest())}}}
FILES = {'config.json': b'{"a"}', 'model.bin': b'MODEL!'}


class Preparation(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / 'voice'
        self.commands, self.urls, self.served = [], [], dict(FILES)
        patcher = patch.object(v, 'MODELS', TINY)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_stub(self, command, **kwargs):
        self.commands.append(command)
        if command[1:3] == ['-m', 'venv']:
            python = v.python_in(Path(command[3]))
            python.parent.mkdir(parents=True)
            python.write_text('')
        return subprocess.CompletedProcess(command, 0, '', '')

    def open_stub(self, request, timeout):
        self.urls.append(request.full_url)
        return io.BytesIO(self.served[request.full_url.rsplit('/', 1)[1]])

    def voice(self, **kwargs):
        return v.Voice(self.root, {}, runner=kwargs.get('runner', self.run_stub), opener=self.open_stub)

    def wait(self, voice, model='tiny'):
        for _ in range(200):
            status = voice.status(model)
            if status['state'] != 'preparing':
                return status
            time.sleep(0.02)
        self.fail('still preparing')

    def test_first_use_installs_pinned_wheels_and_a_checked_model(self):
        voice = self.voice()
        self.assertEqual(voice.status('tiny'), {'state': 'missing'})
        self.assertEqual(voice.prepare('tiny')['state'], 'preparing')
        self.assertEqual(self.wait(voice), {'state': 'ready'})
        pip = next(c for c in self.commands if 'pip' in c)
        for flag in ('--require-hashes', '--only-binary=:all:', '--no-cache-dir'):
            self.assertIn(flag, pip)
        self.assertEqual(pip[-1], str(v.REQUIREMENTS))
        self.assertEqual(self.urls, ['https://huggingface.co/example/tiny/resolve/abc/config.json',
                                     'https://huggingface.co/example/tiny/resolve/abc/model.bin'])
        self.assertEqual((self.root / 'models/tiny/model.bin').read_bytes(), b'MODEL!')
        # Prepared stays prepared: no second install, no second download
        self.commands.clear(), self.urls.clear()
        self.assertEqual(self.voice().prepare('tiny'), {'state': 'ready'})
        self.assertEqual((self.commands, self.urls), ([], []))

    def test_new_requirements_prepare_again(self):
        voice = self.voice()
        voice.prepare('tiny'), self.wait(voice)
        with patch.object(v, 'requirements_key', return_value='newer'):
            self.assertEqual(voice.status('tiny'), {'state': 'missing'})

    def test_a_changed_download_is_refused_and_not_kept(self):
        self.served['model.bin'] = b'EVIL!!'
        voice = self.voice()
        voice.prepare('tiny')
        self.assertEqual(self.wait(voice), {'state': 'failed', 'error': 'The voice model didn’t download correctly. Try again.'})
        self.assertFalse((self.root / 'models/tiny/model.bin').exists())
        self.assertFalse((self.root / 'models/tiny/model.bin.part').exists())
        self.served['model.bin'] = b'MODEL!'   # the next tap tries again
        voice.prepare('tiny')
        self.assertEqual(self.wait(voice), {'state': 'ready'})

    def test_failures_say_what_to_do(self):
        def no_venv(command, **kwargs):
            return subprocess.CompletedProcess(command, 1, '', 'ensurepip is not available')
        voice = self.voice(runner=no_venv)
        voice.prepare('tiny')
        self.assertIn('python3-venv', self.wait(voice)['error'])

        def no_pip(command, **kwargs):
            return self.run_stub(command) if 'venv' in command else subprocess.CompletedProcess(command, 1, '', 'offline')
        voice = self.voice(runner=no_pip)
        voice.prepare('tiny')
        self.assertIn('internet connection', self.wait(voice)['error'])
        self.assertFalse(voice.env.exists())

    def test_too_little_disk_says_so_before_anything_downloads(self):
        self.commands.clear()
        with patch.object(v.shutil, 'disk_usage', return_value=v.shutil._ntuple_diskusage(10 ** 10, 9 * 10 ** 9, 10 ** 9)):
            voice = self.voice()
            self.assertEqual(voice.prepare('tiny'), {'state': 'failed', 'error': 'There isn’t enough free disk space for voice (it needs about 2 GB).'})
        self.assertEqual((self.commands, self.urls), ([], []))
        self.assertEqual(voice.prepare('tiny')['state'], 'preparing')   # room again: the next tap prepares
        self.assertEqual(self.wait(voice), {'state': 'ready'})

    def test_installs_run_at_a_lower_priority(self):
        voice = self.voice()
        voice.prepare('tiny'), self.wait(voice)
        pip = next(c for c in self.commands if 'pip' in c)
        if os.name != 'nt' and shutil.which('nice'):
            self.assertEqual(pip[1:3], ['-n', str(v.NICE)])


class DefaultModel(unittest.TestCase):
    def test_small_servers_get_base_and_the_rest_small(self):
        for memory, model in ((4 * 1024 ** 3, 'base'), (8 * 1024 ** 3, 'small'), (32 * 1024 ** 3, 'small'), (0, 'small')):
            with patch.object(v, 'memory_bytes', return_value=memory):
                self.assertEqual(v.default_model(), model, memory)

    def test_the_default_follows_the_server_until_the_owner_picks(self):
        db = sqlite3.connect(':memory:')
        v.initialize(db)
        with patch.object(v, 'memory_bytes', return_value=4 * 1024 ** 3):
            self.assertEqual(v.prefs(db)['model'], 'base')
            self.assertEqual(v.set_prefs(db, {'model': 'small'}, False)['model'], 'small')


class FakeWorker:
    """voice_worker.py's side of the pipe: says it's ready, then answers each clip."""

    def __init__(self, answer):
        self.answer, self.requests = answer, []
        self.stdin = self
        self.stdout = self
        self.lines = [json.dumps({'ready': True}).encode() + b'\n']
        self.buffer, self.closed = b'', False

    def write(self, data):
        self.buffer += data

    def flush(self):
        head, _, frames = self.buffer.partition(b'\n')
        request = json.loads(head)
        if len(frames) == request['bytes']:
            self.requests.append((request, frames))
            self.buffer = b''
            self.lines.append(json.dumps(self.answer).encode() + b'\n')

    def readline(self):
        return self.lines.pop(0) if self.lines else b''

    def poll(self):
        return 0 if self.closed else None

    def close(self):
        self.closed = True

    def wait(self, timeout=None):
        return 0


class Worker(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.voice = v.Voice(Path(temp.name) / 'voice', {}, popen=self.popen)
        self.started, self.worker = [], FakeWorker({'text': ' Hallo daar ', 'language': 'nl'})
        self.addCleanup(self.voice.stop)

    def popen(self, command, **kwargs):
        self.started.append(command)
        return self.worker

    def test_not_prepared_is_not_ready(self):
        with self.assertRaises(v.NotReady):
            self.voice.transcribe(b'\0\0' * 16000, 'small', '', 60)
        self.assertEqual(self.started, [])

    def test_clips_go_to_one_worker_in_memory(self):
        frames = b'\x02\x00' * 16000
        with patch.object(v.Voice, 'ready', return_value=True):
            self.assertEqual(self.voice.transcribe(frames, 'small', '', 60), {'text': 'Hallo daar', 'language': 'nl'})
            self.voice.transcribe(frames, 'small', 'de', 60)
        self.assertEqual(len(self.started), 1)
        command = self.started[0]
        self.assertTrue(command[-3].endswith('voice_worker.py'))
        if os.name != 'nt' and shutil.which('nice'):
            self.assertEqual(command[1:3], ['-n', str(v.NICE)])   # yields to reviews
        (first, sent), (second, _) = self.worker.requests
        self.assertEqual(sent, frames)
        self.assertEqual(first, {'bytes': len(frames), 'language': None, 'languages': list(v.LANGUAGES)})
        self.assertEqual(second['language'], 'de')
        self.assertEqual(list(Path(self.voice.root).glob('**/*')), [])   # nothing written to disk

    def test_a_worker_error_says_try_again(self):
        self.worker.answer = {'error': 'RuntimeError'}
        with patch.object(v.Voice, 'ready', return_value=True), self.assertRaisesRegex(ValueError, 'turned into text'):
            self.voice.transcribe(b'\0\0' * 16000, 'small', '', 60)

    def test_a_worker_that_wont_start(self):
        self.worker.lines = []
        with patch.object(v.Voice, 'ready', return_value=True), self.assertRaisesRegex(ValueError, 'couldn’t start'):
            self.voice.transcribe(b'\0\0' * 16000, 'small', '', 60)


class OpenAI(unittest.TestCase):
    def test_the_clip_is_a_private_file_only_during_the_call(self):
        seen = {}

        def run(command, **kwargs):
            clip = Path(command[command.index('--file') + 1])
            seen.update(command=command, clip=clip, bytes=clip.read_bytes(), mode=clip.parent.stat().st_mode & 0o777)
            return subprocess.CompletedProcess(command, 0, json.dumps({'ok': True, 'outputs': [{'text': ' Bonjour '}]}), '')
        with tempfile.TemporaryDirectory() as temp:
            frames = b'\x03\x00' * 16000
            heard = v.openai_transcribe({'openclaw': 'oc'}, Path(temp) / 'clips', frames, 'fr', run=run)
            self.assertEqual(heard, {'text': 'Bonjour', 'language': 'fr'})
            self.assertEqual(seen['command'][:4], ['oc', 'infer', 'audio', 'transcribe'])
            self.assertIn(v.OPENAI_MODEL, seen['command'])
            self.assertEqual(seen['command'][-2:], ['--language', 'fr'])
            self.assertEqual(v.pcm(seen['bytes'])[0], frames)
            self.assertEqual(seen['mode'], 0o700)
            self.assertFalse(seen['clip'].exists())
            self.assertEqual(list((Path(temp) / 'clips').iterdir()), [])

    def test_no_answer_says_what_to_do_and_removes_the_clip(self):
        def run(command, **kwargs):
            raise subprocess.TimeoutExpired(command, 120)
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, 'use this Machine'):
                v.openai_transcribe({}, Path(temp), b'\0\0' * 16000, '', run=run)
            self.assertEqual([p for p in Path(temp).iterdir()], [])

    def test_only_an_api_key_counts(self):
        def providers(listing):
            return lambda command, **kwargs: subprocess.CompletedProcess(command, 0, json.dumps(listing), '')
        self.assertTrue(v.openai_ready({}, providers([{'id': 'openai', 'configured': True}])))
        self.assertFalse(v.openai_ready({}, providers([{'id': 'openai', 'configured': False}, {'id': 'groq'}])))
        self.assertFalse(v.openai_ready({}, lambda *x, **y: (_ for _ in ()).throw(OSError())))


TOKEN = 'test-token'


class Api(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.token, self.app.stop = self.store, TOKEN, threading.Event()
        self.app.graph_dirty = threading.Event()
        self.app.owner_token = 'owner-key'
        self.app.config = {'accounts': [], 'tailscale_owner': 'owner@example.com', 'database': str(Path(temp.name) / 'events.sqlite'),
                           'dashboard_host': 'machine.example:8443', 'port': 0, 'http_timeout': 1}
        self.app._voice_openai = (time.monotonic() + 600, False)

    def clip(self, seconds=1.0):
        return {'data': base64.b64encode(wav(seconds)).decode()}

    def test_only_the_owner_on_the_dashboard(self):
        for name in sorted(a.VOICE_ACTIONS):
            with self.assertRaisesRegex(ValueError, 'Only the owner'):
                self.app.action(name, {})
        self.assertLessEqual(a.VOICE_ACTIONS, a.DASHBOARD_ACTIONS)
        self.assertLessEqual(a.VOICE_ACTIONS, a.OWNER_ACTIONS)

    def test_status_and_settings(self):
        view = self.app.action('voice_status', {}, owner_dashboard=True)
        self.assertEqual({k: view[k] for k in ('engine', 'model', 'language', 'max_seconds')},
                         {'engine': 'auto', 'model': 'small', 'language': '', 'max_seconds': 120})
        self.assertEqual(view['local'], {'state': 'missing'})
        self.assertEqual(view['models'], ['small', 'base'])
        self.assertEqual((view['in_use'], view['use']), ('local', 'browser'))   # not ready: the browser's own until then
        view = self.app.action('voice_prefs', {'language': 'it'}, owner_dashboard=True)
        self.assertEqual(view['language'], 'it')
        with self.assertRaisesRegex(ValueError, 'OpenAI set up in OpenClaw'):
            self.app.action('voice_prefs', {'engine': 'openai'}, owner_dashboard=True)
        view = self.app.action('voice_prefs', {'engine': 'local'}, owner_dashboard=True)
        self.assertEqual((view['in_use'], view['use']), ('local', 'wait'))      # On this Machine never goes elsewhere
        self.app._voice_openai = (time.monotonic() + 600, True)
        view = self.app.action('voice_prefs', {'engine': 'auto'}, owner_dashboard=True)
        self.assertEqual((view['in_use'], view['use']), ('openai', 'openai'))

    def test_automatic_with_openai_never_touches_the_local_model(self):
        self.app._voice_openai = (time.monotonic() + 600, True)
        with patch.object(v, 'openai_transcribe', return_value={'text': 'Hi', 'language': 'en'}), \
                patch.object(v.Voice, 'transcribe') as local, patch.object(v.Voice, 'prepare') as prepare:
            self.assertEqual(self.app.action('voice_transcribe', self.clip(), owner_dashboard=True)['text'], 'Hi')
        local.assert_not_called()
        prepare.assert_not_called()

    def test_automatic_falls_back_when_openai_refuses(self):
        self.app._voice_openai = (time.monotonic() + 600, True)
        with patch.object(v, 'openai_transcribe', side_effect=ValueError('OpenAI didn’t answer.')), \
                patch.object(v.Voice, 'ready', return_value=True), \
                patch.object(v.Voice, 'transcribe', return_value={'text': 'Lokaal', 'language': 'nl'}):
            self.assertEqual(self.app.action('voice_transcribe', self.clip(), owner_dashboard=True)['text'], 'Lokaal')
        self.assertFalse(self.app.voice_openai())   # not offered again for a while

    def test_a_clip_becomes_text_and_is_never_kept_or_logged(self):
        heard = []

        def transcribe(voice, frames, model, language, timeout):
            heard.append((len(frames), model, language, timeout))
            return {'text': 'Zeg hem dat het\x07 goed is', 'language': 'nl'}
        with patch.object(v.Voice, 'transcribe', transcribe), self.assertLogs(a.LOG, 'INFO') as logs:
            answer = self.app.action('voice_transcribe', self.clip(2), owner_dashboard=True)
        self.assertEqual(answer, {'text': 'Zeg hem dat het goed is', 'language': 'nl'})
        self.assertEqual(heard, [(64000, 'small', '', v.timeout_for(2))])
        self.assertEqual(logs.output, [f'INFO:{a.LOG.name}:voice clip seconds=2 engine=local'])
        self.assertFalse(any((self.app.dictation.root).glob('**/*.wav')) if self.app.dictation.root.exists() else False)
        with self.store.connect() as db:   # no clip, and no text, in the database
            tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            for table in tables:
                for row in db.execute(f'SELECT * FROM "{table}"'):
                    self.assertNotIn('goed is', json.dumps(row, default=str))

    def test_first_use_waits_for_the_preparation(self):
        with patch.object(v.Voice, 'prepare', return_value={'state': 'preparing'}) as prepare:
            answer = self.app.action('voice_transcribe', self.clip(), owner_dashboard=True)
        self.assertTrue(answer['pending'])
        self.assertEqual(answer['voice']['local'], {'state': 'missing'})
        prepare.assert_called_once_with('small')

    def test_openai_when_the_owner_picked_it(self):
        self.app._voice_openai = (time.monotonic() + 600, True)
        self.app.action('voice_prefs', {'engine': 'openai', 'language': 'es'}, owner_dashboard=True)
        with patch.object(v, 'openai_transcribe', return_value={'text': 'Hola', 'language': 'es'}) as call, \
                patch.object(v.Voice, 'transcribe') as local:
            self.assertEqual(self.app.action('voice_transcribe', self.clip(), owner_dashboard=True)['text'], 'Hola')
        local.assert_not_called()
        self.assertEqual(call.call_args.args[3], 'es')

    def warm(self, checks, openai=False, live=True, busy=False, load=0.0):
        """voice_warm_worker for a number of 5-minute checks; what it prepared."""
        with self.store.connect() as db:
            db.execute('DELETE FROM review_runs')
            if live:
                db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r1','ok','t','t')")
            if busy:
                db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r2','running','t','t')")
        waits = iter([False] * checks + [True])
        self.app.stop = type('Stop', (), {'wait': lambda self, seconds: next(waits)})()
        with patch.object(a.App, 'voice_openai', return_value=openai), patch.object(v.Voice, 'prepare') as prepare, \
                patch.object(v.Voice, 'room', return_value=True), patch.object(v, 'idle', return_value=load < 1):
            self.app.voice_warm_worker()
        return prepare.call_args_list

    def test_the_local_model_gets_ready_only_on_a_live_quiet_machine_without_openai(self):
        self.assertEqual(len(self.warm(a.VOICE_WARM_QUIET)), 1)

    def test_never_while_setting_up_busy_or_with_openai(self):
        self.assertEqual(self.warm(a.VOICE_WARM_QUIET - 1), [])      # not quiet long enough yet
        self.assertEqual(self.warm(10, live=False), [])               # setup: no full review done yet
        self.assertEqual(self.warm(10, busy=True), [])                # a review is running
        self.assertEqual(self.warm(10, load=2.0), [])                 # the server is busy
        self.assertEqual(self.warm(10, openai=True), [])              # GPT Live/OpenAI does dictation here

    def test_settings_never_wait_on_the_openai_check(self):
        slow = threading.Event()

        def ready(config):
            slow.wait(5)
            return True
        del self.app._voice_openai
        self.app._talk = a.talk_live.Talk({}, runner=lambda *x, **y: (slow.wait(5), subprocess.CompletedProcess(x[0], 0, '{"ready": true}', ''))[1])
        with patch.object(v, 'openai_ready', ready):
            began = time.monotonic()
            view = self.app.action('voice_status', {'settings': True}, owner_dashboard=True)
            self.assertLess(time.monotonic() - began, 0.5)   # OpenClaw takes 10 to 20 seconds on a busy Machine
            self.assertIsNone(view['openai'])                 # filled in afterwards: the dashboard asks again
            self.assertIsNone(view['talk']['ready'])
            slow.set()
            for _ in range(100):
                if self.app.voice_openai() is not None:
                    break
                time.sleep(0.02)
        self.assertTrue(self.app.voice_openai())

    def test_a_bad_clip_says_try_again(self):
        for args in ({}, {'data': 'not base64!'}, {'data': base64.b64encode(b'RIFF....').decode()}):
            with self.assertRaisesRegex(ValueError, 'couldn’t be read'):
                self.app.action('voice_transcribe', args, owner_dashboard=True)

    # Over HTTP: the larger body is only for voice_transcribe, and only up to a 2-minute clip

    def serve(self):
        servers = []
        real = a.http.server.ThreadingHTTPServer

        def capture(*args, **kwargs):
            servers.append(real(*args, **kwargs))
            return servers[-1]
        for patcher in (patch.object(a.http.server, 'ThreadingHTTPServer', side_effect=capture),
                        patch.object(a.signal, 'signal'), patch.object(a.App, 'preparation_worker'),
                        patch.object(a.App, 'delivery_worker')):
            patcher.start()
            self.addCleanup(patcher.stop)
        thread = threading.Thread(target=self.app.serve, daemon=True)
        thread.start()
        while not servers:
            time.sleep(0.01)
        self.addCleanup(lambda: (self.app.stop.set(), thread.join(5)))
        return servers[0].server_address[1]

    def post(self, port, body, upload, length=None):
        """Status and answer; with length, only the headers go (the size check comes before the body is read)."""
        csrf = a.hmac.new(TOKEN.encode(), b'owner@example.com', a.hashlib.sha256).hexdigest()
        headers = {'Host': 'machine.example:8443', 'Tailscale-User-Login': 'owner@example.com', 'X-Upload': upload,
                   'Origin': 'https://machine.example:8443', 'X-CSRF-Token': csrf, 'Content-Type': 'application/json',
                   'Content-Length': str(length or len(body))}
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=10)
        try:
            conn.putrequest('POST', '/api/action', skip_host=True)
            for key, value in headers.items():
                conn.putheader(key, value)
            conn.endheaders(None if length else body.encode())
            response = conn.getresponse()
            return response.status, json.loads(response.read() or b'{}')
        finally:
            conn.close()

    def test_the_upload_route(self):
        port = self.serve()
        long = json.dumps({'action': 'voice_transcribe', 'args': self.clip(60)})
        self.assertGreater(len(long), 65536)
        with patch.object(v.Voice, 'transcribe', return_value={'text': 'Long one', 'language': 'en'}):
            self.assertEqual(self.post(port, long, 'voice'), (200, {'text': 'Long one', 'language': 'en'}))
        self.assertEqual(self.post(port, '', '', length=len(long))[0], 400)   # without the header, the usual limit
        status, body = self.post(port, json.dumps({'action': 'set_locale', 'args': {'locale': 'nl'}}), 'voice')
        self.assertEqual(status, 400)   # the header is only for voice_transcribe
        self.assertEqual(self.post(port, '', 'voice', length=v.REQUEST_BYTES + 1),
                         (400, {'error': 'Recordings can be up to 2 minutes.'}))


class Dashboard(unittest.TestCase):
    def test_every_message_box_has_the_mic(self):
        html = (ROOT / 'dashboard.html').read_text()
        self.assertGreaterEqual(html.count('micBtn()}'), 4)   # to-do chat, New to-do, Help, change a draft
        # The browser's own speech recognition only as the stopgap on Automatic (voice_view's use 'browser'), never otherwise
        self.assertEqual(html.count('window.SpeechRecognition'), 1)
        self.assertIn("micUse==='browser'", html)


if __name__ == '__main__':
    unittest.main()

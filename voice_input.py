"""Voice input: the owner talks, and The Machine writes what they said into the box they were typing in. It never
sends it: the owner reads it, edits it and sends it themselves.

The dashboard records with the browser's MediaRecorder (at most MAX_SECONDS), turns the clip into 16 kHz mono 16-bit
WAV in the browser, and posts it (voice_transcribe). Engines (Settings, Voice input; `engine_for`):

- **auto** (the default): OpenAI when this Machine has OpenAI in OpenClaw, otherwise this Machine. With OpenAI here the
  local model is never downloaded.
- **openai**: the owner's own OpenAI access, through OpenClaw (model OPENAI_MODEL): an API key, or a ChatGPT sign-in
  where the account allows audio (OpenClaw's audio providers list says which). The clip goes to OpenAI. OpenClaw runs
  loaded in voice-openai-run.mjs (OpenAIVoice), started on the tap and kept IDLE_SECONDS, with the
  `openclaw infer audio transcribe` CLI as the fallback. OpenClaw reads a file, so the clip is written to a private
  folder and removed as soon as it returns.
- **local**: faster-whisper with a Whisper model, on this Machine. Nothing leaves it. It is not part of the install or
  the prebuilt images, so setup stays as fast as it was. It gets ready in the background once the Machine is live and
  quiet (the service's voice_warm_worker; `prepare`): its own virtualenv next to the database (voice/env), the exact
  packages in voice-requirements.txt (every one pinned by hash, wheels only, installed at a lower priority), and the
  model from Hugging Face at a pinned revision, each file checked against its SHA-256. The model runs in
  voice_worker.py, started when the owner taps the mic and stopped after IDLE_SECONDS without a clip. Clips go to it
  one at a time over a pipe.

While the owner talks, the dashboard sends what they said so far at each pause (a part), so most of it is written
down before they tap Done and only the last few seconds are left to wait for.

Until the local engine is ready, a tap on Automatic uses the browser's own speech recognition where the browser has it
(the dashboard says so); with On this Machine picked, the clip waits for it instead and goes nowhere else.

A clip is never kept: it is only in memory (and, for the openai engine, in that file for the seconds the call takes),
and nothing about it is logged but its length. The language is the one the owner picked in Settings, or detected
among the app's languages."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / 'voice-requirements.txt'
MAX_SECONDS = 120          # the dashboard stops recording here; a little more is allowed for the browser's rounding
RATE = 16000
REQUEST_BYTES = (MAX_SECONDS + 5) * RATE * 2 * 4 // 3 + 64 * 1024   # the WAV, base64 in JSON
IDLE_SECONDS = 300
FREE_BYTES = 2 * 1024 ** 3   # room the preparation needs: packages about 0.5 GB, the small model 0.5 GB, and slack
LANGUAGES = ('de', 'en', 'es', 'fr', 'it', 'nl', 'pt')   # the app's languages (i18n/*.json), as Whisper names them
# Talk live's voices (OpenAI Realtime, gpt-realtime). ChatGPT's Cove isn't one of them (only GPT-Live through a
# ChatGPT sign-in has it); Cedar, calm and low, is the closest, so it's the default. Samples: brand/voices/<name>.mp3.
TALK_VOICES = ('cedar', 'marin', 'ash', 'ballad', 'coral', 'echo', 'sage', 'shimmer', 'verse', 'alloy')
ENGINES = ('auto', 'local', 'openai')   # auto: OpenAI when this Machine has OpenAI, else this Machine
OPENAI_MODEL = 'openai/gpt-4o-transcribe'
HF = 'https://huggingface.co/{repo}/resolve/{revision}/{name}'
# The models, at a fixed revision, each file with its size and SHA-256. "small" gets Dutch, German and the rest right
# where "base" garbles them more often; "base" is about three times faster and needs half the memory (docs/voice.md).
MODELS = {
    'small': {'repo': 'Systran/faster-whisper-small', 'revision': '536b0662742c02347bc0e980a01041f333bce120', 'files': {
        'config.json': (2370, 'b55496ac7940a7ae47d2c01eab40edfd8701feec1229d9cce3b40014383fb828'),
        'tokenizer.json': (2203239, 'fb7b63191e9bb045082c79fd742a3106a12c99513ab30df4a0d47fa6cb6fd0ab'),
        'vocabulary.txt': (459861, '34ce3fe1c5041027b3f8d42912270993f986dbc4bb34cf27f951e34a1e453913'),
        'model.bin': (483546902, '3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671')}},
    'base': {'repo': 'Systran/faster-whisper-base', 'revision': 'ebe41f70d5b6dfa9166e2c581c45c9c0cfc57b66', 'files': {
        'config.json': (2309, '56a6d8110d311f19c8f0471e562832c7527f146b567275bfca59fcf7c184da9a'),
        'tokenizer.json': (2203239, 'fb7b63191e9bb045082c79fd742a3106a12c99513ab30df4a0d47fa6cb6fd0ab'),
        'vocabulary.txt': (459861, '34ce3fe1c5041027b3f8d42912270993f986dbc4bb34cf27f951e34a1e453913'),
        'model.bin': (145217532, 'd01c3014881c9c6f3133c182f3d2887eb6ca1c789a7538c5c007196857a0a6a9')}},
}
SMALL_SERVER = 6 * 1024 ** 3   # below this much memory, "base" is the default: a Standard server has 4 GB and 2 cores
NICE = 10                      # transcription and its preparation yield to reviews and the rest of the Machine


def memory_bytes():
    try:
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    except (AttributeError, ValueError, OSError):
        return 0


def default_model():
    """"small" where there's room (desktops, Bigger servers), "base" on small servers, where "small" pushes into swap."""
    memory = memory_bytes()
    return 'base' if 0 < memory < SMALL_SERVER else 'small'


def lowered(command):
    """The command and its keyword arguments, so it runs at a lower priority than the Machine's own work."""
    if os.name == 'nt':
        return command, {'creationflags': subprocess.BELOW_NORMAL_PRIORITY_CLASS}
    nice = shutil.which('nice')
    return ([nice, '-n', str(NICE), *command] if nice else command), {}


class NotReady(Exception):
    """The local engine isn't prepared yet; the dashboard shows the preparation and sends the clip when it's done."""


def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS voice_prefs(key TEXT PRIMARY KEY, value TEXT NOT NULL)')


def prefs(db):
    """The owner's choices in Settings, Voice input: engine, model, language ('' detects it) and Talk live's voice."""
    kept = dict(db.execute('SELECT key,value FROM voice_prefs').fetchall())
    engine = kept.get('engine') if kept.get('engine') in ENGINES else 'auto'
    model = kept.get('model') if kept.get('model') in MODELS else default_model()
    language = kept.get('language') if kept.get('language') in LANGUAGES else ''
    talk_voice = kept.get('talk_voice') if kept.get('talk_voice') in TALK_VOICES else TALK_VOICES[0]
    return {'engine': engine, 'model': model, 'language': language, 'talk_voice': talk_voice}


def set_prefs(db, args, openai_ok):
    changes = {}
    if 'engine' in args:
        if args['engine'] not in ENGINES:
            raise ValueError('Pick Automatic, this Machine or OpenAI')
        if args['engine'] == 'openai' and not openai_ok:
            raise ValueError('Voice through OpenAI needs OpenAI set up in OpenClaw')
        changes['engine'] = args['engine']
    if 'model' in args:
        if args['model'] not in MODELS:
            raise ValueError('Pick Faster or More accurate')
        changes['model'] = args['model']
    if 'language' in args:
        if args['language'] not in ('', *LANGUAGES):
            raise ValueError('Pick a language, or Detect')
        changes['language'] = args['language']
    if 'talk_voice' in args:
        if args['talk_voice'] not in TALK_VOICES:
            raise ValueError('Pick one of the voices')
        changes['talk_voice'] = args['talk_voice']
    for key, value in changes.items():
        db.execute('INSERT INTO voice_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',
                   (key, value))
    return prefs(db)


def engine_for(prefs, openai_ok):
    """The engine in use: OpenAI when picked, or on Automatic when this Machine has OpenAI; otherwise this Machine."""
    return 'openai' if prefs['engine'] == 'openai' or (prefs['engine'] == 'auto' and openai_ok) else 'local'


def idle(load=None, cpus=None):
    """Whether a small server has nothing much going on: a load under half its cores."""
    try:
        load = os.getloadavg()[0] if load is None else load
    except (AttributeError, OSError):
        return True
    return load < max(1, cpus or os.cpu_count() or 1) / 2


def warm_due(prefs, openai_ok, status, room):
    """Whether to get the local engine ready in the background: only when this Machine will use it and there's room."""
    return engine_for(prefs, openai_ok) == 'local' and status['state'] in ('missing', 'failed') and room


def pcm(data):
    """The 16 kHz mono 16-bit PCM in a WAV the dashboard made, and its length in seconds. Anything else is refused."""
    try:
        with wave.open(io.BytesIO(data)) as clip:
            if clip.getnchannels() != 1 or clip.getsampwidth() != 2 or clip.getframerate() != RATE:
                raise ValueError('That recording couldn’t be read. Try again.')
            frames = clip.readframes(clip.getnframes())
    except (wave.Error, EOFError) as error:
        raise ValueError('That recording couldn’t be read. Try again.') from error
    seconds = len(frames) / (RATE * 2)
    if seconds < 0.3:
        raise ValueError('That was too short. Talk a little longer.')
    if seconds > MAX_SECONDS + 5:
        raise ValueError(f'Recordings can be up to {MAX_SECONDS // 60} minutes.')
    return frames, seconds


def python_in(env):
    return env / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def requirements_key():
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()[:16]


class Voice:
    """The local engine on this Machine: its preparation, its worker and the clips it turns into text."""

    def __init__(self, root, config=None, runner=subprocess.run, opener=urllib.request.urlopen, popen=subprocess.Popen):
        self.root, self.config = Path(root), config or {}
        self.run, self.open, self.popen = runner, opener, popen
        self.lock, self.work = threading.Lock(), threading.Lock()   # state; one clip at a time through the worker
        self.preparing = None   # {'model', 'step', 'done', 'total'} while a preparation runs
        self.failed = None      # what went wrong in the last preparation, for the dashboard
        self.worker = None      # (process, model) while it runs
        self.used = 0.0
        self.timer = None

    @property
    def env(self):
        return self.root / 'env'

    def model_dir(self, model):
        return self.root / 'models' / model

    def ready_file(self):
        return self.root / 'ready.json'

    def ready(self, model):
        """Prepared for this model with today's packages (a release that changes voice-requirements.txt prepares again)."""
        try:
            done = json.loads(self.ready_file().read_text())
        except (OSError, ValueError):
            return False
        return (done.get('packages') == requirements_key() and model in (done.get('models') or [])
                and python_in(self.env).exists() and (self.model_dir(model) / 'model.bin').exists())

    def status(self, model):
        with self.lock:
            if self.preparing:
                return {'state': 'preparing', **self.preparing}
            if self.ready(model):
                return {'state': 'ready'}
            if self.failed:
                return {'state': 'failed', 'error': self.failed}
            return {'state': 'missing'}

    def prepare(self, model):
        """Start preparing in the background (once at a time); returns the status."""
        with self.lock:
            if self.preparing or self.ready(model):
                pass
            elif not self.room():   # said before anything downloads
                self.failed = 'There isn’t enough free disk space for voice (it needs about 2 GB).'
            else:
                self.failed = None
                self.preparing = {'model': model, 'step': 'packages', 'done': 0, 'total': 0}
                threading.Thread(target=self._prepare, args=(model,), name='voice-prepare', daemon=True).start()
        return self.status(model)

    def room(self):
        """Free disk space for the packages and a model, measured where they go (or the nearest folder that exists)."""
        place = self.root
        while not place.exists() and place != place.parent:
            place = place.parent
        try:
            return shutil.disk_usage(place).free >= FREE_BYTES
        except OSError:
            return True   # can't tell: the download says it if it runs out

    def _prepare(self, model):
        try:
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            key = requirements_key()
            try:
                done = json.loads(self.ready_file().read_text())
            except (OSError, ValueError):
                done = {}
            if done.get('packages') != key or not python_in(self.env).exists():
                self._packages()
                done = {'packages': key, 'models': []}
                self._write_ready(done)
            with self.lock:
                self.preparing.update(step='model')
            self._model(model)
            done['models'] = sorted({*(done.get('models') or []), model})
            self._write_ready(done)
        except Exception as error:  # the dashboard says it, and the next tap tries again
            with self.lock:
                self.failed = str(error) if isinstance(error, RuntimeError) else 'Getting voice ready failed. Try again later.'
        finally:
            with self.lock:
                self.preparing = None

    def _write_ready(self, done):
        part = self.ready_file().with_suffix('.part')
        part.write_text(json.dumps(done))
        part.replace(self.ready_file())

    def _packages(self):
        if self.env.exists():
            shutil.rmtree(self.env)
        made = self.run([self.config.get('voice_python') or sys.executable, '-m', 'venv', str(self.env)],
                        capture_output=True, text=True, timeout=300)
        if made.returncode:
            raise RuntimeError('Python can’t make a virtual environment here. Install python3-venv, then try again.')
        command, low = lowered([str(python_in(self.env)), '-m', 'pip', 'install', '--disable-pip-version-check', '--no-input',
                                '--no-cache-dir', '--only-binary=:all:', '--require-hashes', '-r', str(REQUIREMENTS)])
        got = self.run(command, capture_output=True, text=True, timeout=1800, **low)
        if got.returncode:
            shutil.rmtree(self.env, ignore_errors=True)
            raise RuntimeError('The voice packages couldn’t be installed. Check the internet connection, then try again.')

    def _model(self, model):
        spec, folder = MODELS[model], self.model_dir(model)
        folder.mkdir(parents=True, exist_ok=True)
        total = sum(size for size, _ in spec['files'].values())
        with self.lock:
            self.preparing.update(total=total, done=0)
        for name, (size, digest) in spec['files'].items():
            target = folder / name
            if target.exists() and target.stat().st_size == size:
                with self.lock:
                    self.preparing['done'] += size
                continue
            part, sha = target.with_name(name + '.part'), hashlib.sha256()
            url = HF.format(repo=spec['repo'], revision=spec['revision'], name=name)
            with self.open(urllib.request.Request(url, headers={'User-Agent': 'TheMachine'}), timeout=60) as response, \
                    open(part, 'wb') as out:
                while chunk := response.read(1 << 20):
                    sha.update(chunk)
                    out.write(chunk)
                    with self.lock:
                        self.preparing['done'] += len(chunk)
            if sha.hexdigest() != digest:
                part.unlink(missing_ok=True)
                raise RuntimeError('The voice model didn’t download correctly. Try again.')
            part.replace(target)

    def warm(self, model):
        """Starts the worker in the background (the mic was tapped), so the model is loaded by the time a clip comes."""
        if not self.ready(model) or self.worker and self.worker[1] == model and self.worker[0].poll() is None:
            return

        def start():
            with contextlib.suppress(ValueError), self.work:
                self._worker(model)
                self.used = time.monotonic()
                self._idle()
        threading.Thread(target=start, daemon=True, name='voice-warm-worker').start()

    def transcribe(self, frames, model, language, timeout):
        """Text for the PCM, through the worker (started when needed)."""
        if not self.ready(model):
            raise NotReady()
        with self.work:
            process = self._worker(model)
            try:
                process.stdin.write(json.dumps({'bytes': len(frames), 'language': language or None,
                                                'languages': list(LANGUAGES)}).encode() + b'\n')
                process.stdin.write(frames)
                process.stdin.flush()
                answer = self._line(process, timeout)
            except (OSError, ValueError, TimeoutError, EOFError):
                self.stop()
                raise ValueError('Voice didn’t answer. Try again.')
            finally:
                self.used = time.monotonic()
                self._idle()
        if answer.get('error'):
            raise ValueError('That recording couldn’t be turned into text. Try again.')
        return {'text': str(answer.get('text') or '').strip(), 'language': answer.get('language')}

    def _worker(self, model):
        if self.worker and self.worker[1] == model and self.worker[0].poll() is None:
            return self.worker[0]
        self.stop()
        threads = max(1, min(4, (os.cpu_count() or 2)))
        # At the normal priority, unlike the preparation: the owner is waiting on it
        command = [str(python_in(self.env)), str(ROOT / 'voice_worker.py'), str(self.model_dir(model)), str(threads)]
        process = self.popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                             cwd=str(self.root))
        self.worker = (process, model)
        try:
            if not self._line(process, 120).get('ready'):
                raise EOFError()
        except (OSError, ValueError, TimeoutError, EOFError):
            self.stop()
            raise ValueError('Voice couldn’t start on this Machine. Try again.')
        return process

    @staticmethod
    def _line(process, timeout):
        got = {}
        reader = threading.Thread(target=lambda: got.update(line=process.stdout.readline()), daemon=True)
        reader.start()
        reader.join(timeout)
        if reader.is_alive():
            raise TimeoutError()
        if not got.get('line'):
            raise EOFError()
        return json.loads(got['line'])

    def _idle(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(IDLE_SECONDS, self._maybe_stop)
        self.timer.daemon = True
        self.timer.start()

    def _maybe_stop(self):
        if time.monotonic() - self.used >= IDLE_SECONDS - 1 and self.work.acquire(blocking=False):
            try:
                self.stop()
            finally:
                self.work.release()

    def stop(self):
        if self.worker:
            process = self.worker[0]
            self.worker = None
            with contextlib.suppress(OSError, ValueError):
                process.stdin.close()
            try:
                process.wait(5)
            except subprocess.TimeoutExpired:
                process.kill()


def openai_ready(config, run=subprocess.run):
    """Whether OpenClaw can transcribe with OpenAI (an API key, or a ChatGPT sign-in where the account allows it): its
    audio providers list."""
    try:
        result = run([str(config.get('openclaw') or 'openclaw'), 'infer', 'audio', 'providers', '--json'],
                     capture_output=True, text=True, timeout=90)
        providers = json.loads(result.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    return any(isinstance(p, dict) and p.get('id') == 'openai' and p.get('configured') for p in providers or [])


def wav_bytes(frames):
    out = io.BytesIO()
    with wave.open(out, 'wb') as clip:
        clip.setnchannels(1)
        clip.setsampwidth(2)
        clip.setframerate(RATE)
        clip.writeframes(frames)
    return out.getvalue()


def openai_transcribe(config, root, frames, language, run=subprocess.run):
    """Text for the PCM through the owner's OpenAI access in OpenClaw. The clip is in a private file only for the call."""
    Path(root).mkdir(parents=True, exist_ok=True, mode=0o700)
    folder = Path(tempfile.mkdtemp(prefix='clip-', dir=root))
    clip = folder / (secrets.token_hex(8) + '.wav')
    try:
        clip.write_bytes(wav_bytes(frames))
        command = [str(config.get('openclaw') or 'openclaw'), 'infer', 'audio', 'transcribe', '--file', str(clip),
                   '--model', OPENAI_MODEL, '--json']
        if language:
            command += ['--language', language]
        try:
            result = run(command, capture_output=True, text=True, timeout=120)
            answer = json.loads(result.stdout)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            raise ValueError('OpenAI didn’t answer. Try again, or use this Machine for voice in Settings.') from error
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    outputs = answer.get('outputs') if isinstance(answer, dict) and answer.get('ok') else None
    if not outputs:
        raise ValueError('OpenAI didn’t answer. Try again, or use this Machine for voice in Settings.')
    return {'text': ' '.join(str(o.get('text') or '').strip() for o in outputs if isinstance(o, dict)).strip(),
            'language': language or None}


class OpenAIVoice:
    """The openai engine with OpenClaw loaded once (voice-openai-run.mjs): a clip then takes a second or two, where the
    `openclaw infer audio transcribe` CLI needs 8 to 10 seconds just to start. Started when the owner taps the mic (so
    it is ready by the time they stop talking) and stopped after IDLE_SECONDS without a clip. When it can't start or
    answer, the CLI (openai_transcribe) does the clip instead."""

    def __init__(self, root, command, popen=subprocess.Popen):
        self.root, self.command, self.popen = Path(root), command, popen   # command(): (argv, env)
        self.lock, self.work = threading.Lock(), threading.Lock()
        self.worker = None
        self.used = 0.0
        self.timer = None
        self.broken = 0.0   # when it last failed to start: the CLI does clips for a while after that

    def warm(self):
        """Starts it in the background (the mic was tapped)."""
        if self.worker and self.worker.poll() is None or time.monotonic() - self.broken < 600:
            return
        threading.Thread(target=self._warm, daemon=True, name='voice-openai-warm').start()

    def _warm(self):
        with contextlib.suppress(ValueError), self.work:
            self._worker()
            self.used = time.monotonic()
            self._idle()

    def _worker(self):
        if self.worker and self.worker.poll() is None:
            return self.worker
        if time.monotonic() - self.broken < 600:
            raise ValueError('unavailable')
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        argv, env = self.command()
        try:
            process = self.popen([*argv, str(self.root)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, cwd=str(self.root), env=env)
        except OSError as error:
            self.broken = time.monotonic()
            raise ValueError('unavailable') from error
        self.worker = process
        try:
            if not Voice._line(process, 60).get('ready'):
                raise EOFError()
        except (OSError, ValueError, TimeoutError, EOFError) as error:
            self.stop()
            self.broken = time.monotonic()
            raise ValueError('unavailable') from error
        return process

    def transcribe(self, frames, language, timeout=60):
        """Text for the PCM, or ValueError (then the CLI tries). The clip is in a private file only for the call."""
        with self.work:
            folder = Path(tempfile.mkdtemp(prefix='clip-', dir=self._root()))
            clip = folder / (secrets.token_hex(8) + '.wav')
            try:
                process = self._worker()
                clip.write_bytes(wav_bytes(frames))
                process.stdin.write(json.dumps({'file': str(clip), 'language': language or None}).encode() + b'\n')
                process.stdin.flush()
                answer = Voice._line(process, timeout)
            except (OSError, TimeoutError, EOFError) as error:
                self.stop()
                raise ValueError('unavailable') from error
            finally:
                shutil.rmtree(folder, ignore_errors=True)
                self.used = time.monotonic()
                self._idle()
        if not isinstance(answer, dict) or answer.get('error') or 'text' not in answer:
            raise ValueError('unavailable')
        return {'text': str(answer['text']).strip(), 'language': language or None}

    def _root(self):
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        return self.root

    def _idle(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(IDLE_SECONDS, self._maybe_stop)
        self.timer.daemon = True
        self.timer.start()

    def _maybe_stop(self):
        if time.monotonic() - self.used >= IDLE_SECONDS - 1 and self.work.acquire(blocking=False):
            try:
                self.stop()
            finally:
                self.work.release()

    def stop(self):
        process, self.worker = self.worker, None
        if process:
            with contextlib.suppress(OSError, ValueError):
                process.stdin.close()
            try:
                process.wait(5)
            except subprocess.TimeoutExpired:
                process.kill()


def timeout_for(seconds):
    """How long a clip may take: generous on a small server, where the small model runs at about real time."""
    return 60 + 3 * seconds


def clean(text):
    """What lands in the box: plain text, no control characters or doubled spaces."""
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', str(text or ''))
    return re.sub(r'[ \t]+', ' ', text).strip()[:8000]

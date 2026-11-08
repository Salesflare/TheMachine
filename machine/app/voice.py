"""Voice input in the service (voice_input.py and voice_worker.py do the work): dictation, the OpenAI voice key, the
view Settings shows and the voice actions. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import base64
import logging
from pathlib import Path
import threading
import time

from machine.actions import VOICE_ACTIONS
import voice_input

LOG = logging.getLogger('personal-assistant')


VOICE_WARM_QUIET = 3   # 5-minute checks in a row that a live Machine is quiet before voice gets ready in the background


class VoiceApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {**dict.fromkeys(VOICE_ACTIONS, 'voice_actions_action')}

    @property
    def dictation(self):
        """Voice input's local engine (voice_input.py), next to the database."""
        if getattr(self, '_voice', None) is None:
            self._voice = voice_input.Voice(Path(self.config['database']).expanduser().parent / 'voice', self.config)
        return self._voice

    def voice_openai(self, check=False, wait=False):
        """Whether OpenClaw has OpenAI access that can transcribe (an API key, or a ChatGPT sign-in where the account allows
        it), kept 10 minutes; None until known. Asking OpenClaw takes it 10 to 20 seconds on a busy Machine, so with check
        a stale answer is refreshed in the background and what is known now comes back at once (Settings never waits on
        it); only wait=True (the background worker, a clip when nothing is known yet) waits for the answer."""
        kept = getattr(self, '_voice_openai', None)
        if check and (not kept or kept[0] < time.monotonic()):
            if wait:
                kept = self._voice_openai = (time.monotonic() + 600, voice_input.openai_ready(self.config))
            else:
                lock = self.__dict__.setdefault('_voice_openai_lock', threading.Lock())
                if lock.acquire(blocking=False):
                    def refresh():
                        try:
                            self._voice_openai = (time.monotonic() + 600, voice_input.openai_ready(self.config))
                        finally:
                            lock.release()
                    threading.Thread(target=refresh, daemon=True, name='voice-openai').start()
        return kept[1] if kept else None

    def voice_view(self, prefs, check=False):
        openai, local = self.voice_openai(check), self.dictation.status(prefs['model'])
        engine = voice_input.engine_for(prefs, openai)
        # What a tap does now: the engine in use; on Automatic without OpenAI while this Machine's own isn't ready yet,
        # 'browser' (the dashboard uses the browser's own speech recognition where it has one, else waits); with On this
        # Machine picked, 'wait': the recording waits for it, never going anywhere else.
        use = engine if engine == 'openai' or local['state'] == 'ready' else 'browser' if prefs['engine'] == 'auto' else 'wait'
        return {**prefs, 'local': local, 'openai': openai, 'in_use': engine, 'use': use,
                'max_seconds': voice_input.MAX_SECONDS, 'languages': list(voice_input.LANGUAGES),
                'models': list(voice_input.MODELS)}

    def voice_action(self, name, args):
        """Settings, Voice input, and the mic in the dashboard's message boxes. A clip is only ever in memory here, and the
        log has only its length (voice_input.py)."""
        with self.store.connect() as db:
            prefs = (voice_input.set_prefs(db, args, (self.voice_openai() or self.voice_openai(True, wait=True)) if args.get('engine') == 'openai' else False)
                     if name == 'voice_prefs' else voice_input.prefs(db))
        if name in ('voice_status', 'voice_prefs'):
            view = self.voice_view(prefs, check=bool(args.get('settings')) or name == 'voice_prefs')
            if args.get('warm'):   # the mic was tapped: the engine in use loads while the owner talks
                if view['use'] == 'openai':
                    self.dictation_openai.warm()
                elif view['use'] == 'local':
                    self.dictation.warm(prefs['model'])
            # Settings (its own status, and a change saved there) shows Talk live's rows from this too
            return {**view, 'talk': self.talk_view(check=bool(args.get('settings')))} if args.get('settings') or name == 'voice_prefs' else view
        if name == 'voice_prepare':
            if voice_input.engine_for(prefs, self.voice_openai()) == 'local':
                self.dictation.prepare(prefs['model'])
            return self.voice_view(prefs)
        try:
            data = base64.b64decode(str(args.get('data') or ''), validate=True)
        except (ValueError, TypeError) as error:
            raise ValueError('That recording couldn’t be read. Try again.') from error
        began = time.monotonic()
        frames, seconds = voice_input.pcm(data)
        if not prefs['language'] and args.get('language') in voice_input.LANGUAGES:   # a later part: the language heard first
            prefs = {**prefs, 'language': args['language']}
        openai = self.voice_openai(True, wait=self.voice_openai() is None) if prefs['engine'] == 'auto' else self.voice_openai()
        engine = voice_input.engine_for(prefs, openai)
        local_ready = self.dictation.ready(prefs['model'])
        if engine == 'openai':
            try:
                try:
                    heard = self.dictation_openai.transcribe(frames, prefs['language'], timeout=30 + seconds)
                except ValueError:   # it couldn't start or answer: the CLI, which also says why
                    heard = voice_input.openai_transcribe(self.config, self.dictation.root / 'clips', frames, prefs['language'])
                engine = 'openai'
            except ValueError:
                if prefs['engine'] == 'auto':   # OpenAI refused (a sign-in without audio access): Automatic leaves it for an hour
                    self._voice_openai = (time.monotonic() + 3600, False)
                if not local_ready:
                    raise
                heard, engine = None, 'local'
        else:
            heard = None
        if heard is None:
            try:
                heard, engine = self.dictation.transcribe(frames, prefs['model'], prefs['language'], voice_input.timeout_for(seconds)), 'local'
            except voice_input.NotReady:
                self.dictation.prepare(prefs['model'])
                return {'pending': True, 'voice': self.voice_view(prefs)}
        LOG.info('voice clip seconds=%.0f engine=%s part=%s took=%.1f', seconds, engine, bool(args.get('part')), time.monotonic() - began)
        return {'text': voice_input.clean(heard['text']), 'language': heard.get('language')}

    def voice_actions_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner uses voice input, on the dashboard')
        return self.voice_action(name, args)

    def voice_warm_worker(self):
        """Gets this Machine's own voice engine ready in the background, so a tap on the mic never waits on a download.
        Never during setup: only once this Machine is live (its first full review is done) and has been quiet for a while
        (VOICE_WARM_QUIET checks in a row: no review or preparation running, load under half the cores). Only when it
        will use it (no OpenAI here, or On this Machine picked) and there's room on disk. The same after an update that
        changes its packages. The install runs at a lower priority (voice_input.lowered). Until then a tap uses OpenAI or
        the browser's own speech recognition (voice_view's `use`)."""
        tried, quiet = 0.0, 0
        try:
            self.voice_openai(True, wait=True)   # known before the first tap: whether Automatic means OpenAI here
        except Exception as error:
            LOG.error('voice openai check error=%s', type(error).__name__)
        while not self.stop.wait(300):
            try:
                with self.store.connect() as db:
                    prefs = voice_input.prefs(db)
                    live = db.execute("SELECT 1 FROM review_runs WHERE status='ok' AND NOT COALESCE(window_hours,0) LIMIT 1").fetchone()
                    busy = db.execute("SELECT (SELECT count(*) FROM preparations WHERE status IN ('starting','running'))"
                                      "+(SELECT count(*) FROM review_runs WHERE status IN ('starting','running','recovering'))").fetchone()[0]
                openai = self.voice_openai(True, wait=True)   # kept 10 minutes: OpenAI connected later switches Automatic to it
                quiet = quiet + 1 if live and not busy and voice_input.idle() else 0
                status = self.dictation.status(prefs['model'])
                if quiet < VOICE_WARM_QUIET or (status['state'] == 'failed' and time.monotonic() - tried < 6 * 3600):
                    continue
                if voice_input.warm_due(prefs, openai, status, self.dictation.room()):
                    tried = time.monotonic()
                    LOG.info('voice warm start model=%s', prefs['model'])
                    self.dictation.prepare(prefs['model'])
            except Exception as error:
                LOG.error('voice warm error=%s', type(error).__name__)

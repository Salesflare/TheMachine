"""Model turns someone waits on (a search answer, Help) through one long-running helper (model-run-service.mjs), not a
new `openclaw infer model run` process per turn: that CLI loads OpenClaw each time, seconds before the turn starts.

The helper makes the same Gateway call as the CLI, with the same client and scopes. It starts on first use (or warm(),
when the search opens) and exits after ten idle minutes, so it holds no memory while nobody asks. When it can't start
or stops mid-turn, the turn runs through the CLI as before (help_chat.openclaw_model_run)."""
from __future__ import annotations

import json
import subprocess
import threading
import uuid
from pathlib import Path

import help_chat
from machine.model_usage import node_bin, node_env

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / 'model-run-service.mjs'
START_SECONDS = 30  # loading OpenClaw once: about 2 s, more on a busy computer


class Down(Exception):
    """The helper isn't running or stopped: the turn goes through the CLI."""


class Service:
    def __init__(self, command, env):
        self.command, self.env = command, env
        self.lock = threading.Lock()
        self.proc = None
        self.ready = threading.Event()
        self.waiting = {}  # id: [Event, reply]

    def start(self):
        """The running helper, started when it isn't (or exited when idle)."""
        with self.lock:
            if self.proc and self.proc.poll() is None:
                return self.proc
            try:
                proc = subprocess.Popen(self.command, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL, text=True, bufsize=1)
            except OSError:
                raise Down() from None
            self.proc, self.ready = proc, threading.Event()
            threading.Thread(target=self.read, args=(proc, self.ready), daemon=True, name='model-run-service').start()
            return proc

    def read(self, proc, ready):
        for line in proc.stdout:
            try:
                reply = json.loads(line)
            except ValueError:
                continue
            if reply.get('ready'):
                ready.set()
                continue
            slot = self.waiting.get(reply.get('id'))
            if slot:
                slot[1] = reply
                slot[0].set()
        with self.lock:  # it exited (idle, or failed): wake everyone still waiting on it
            for slot in self.waiting.values():
                if slot[1] is None:
                    slot[1] = {'down': True}
                    slot[0].set()
        ready.set()

    def warm(self):
        """Start it now (when the search opens), so the first question doesn't wait for OpenClaw to load."""
        try:
            self.start()
        except Down:
            pass

    def run(self, text, model=None, thinking=None, timeout=60):
        """The reply's text. Raises Down when the helper can't take the turn, help_chat.Unavailable when the model
        didn't answer."""
        proc = self.start()
        if not self.ready.wait(START_SECONDS) or proc.poll() is not None:
            raise Down()
        rid, slot = uuid.uuid4().hex, [threading.Event(), None]
        self.waiting[rid] = slot
        try:
            line = {'id': rid, 'prompt': text, 'timeout_ms': int(timeout * 1000)}
            line.update({k: v for k, v in (('model', model), ('thinking', thinking)) if v})
            try:
                with self.lock:
                    proc.stdin.write(json.dumps(line) + '\n')
                    proc.stdin.flush()
            except (OSError, ValueError):
                raise Down() from None
            if not slot[0].wait(timeout + 5):
                raise help_chat.Unavailable(help_chat.t('Help took too long to answer. Try again.'))
            reply = slot[1]
        finally:
            self.waiting.pop(rid, None)
        if reply.get('down'):
            raise Down()
        if reply.get('ok') and reply.get('text'):
            return reply['text']
        if reply.get('error') == 'timeout':
            raise help_chat.Unavailable(help_chat.t('Help took too long to answer. Try again.'))
        raise help_chat.Unavailable(help_chat.t('Help can’t reach your model right now.'))


_services = {}
_services_lock = threading.Lock()


def service(config):
    """The helper for this config's Node and OpenClaw (one per process)."""
    command = (node_bin(config or {}), str(SCRIPT))
    with _services_lock:
        if command not in _services:
            _services[command] = Service(list(command), node_env(config or {}))
        return _services[command]


def warm(config):
    service(config).warm()


def run(config, text, model=None, thinking=None, timeout=help_chat.TIMEOUT):
    """One model turn, as help_chat.openclaw_model_run (same arguments, same reply and errors), through the helper;
    through the CLI when the helper can't take it."""
    try:
        return service(config).run(text, model, thinking, timeout)
    except Down:
        return help_chat.openclaw_model_run(config, text, model, thinking, timeout=timeout)

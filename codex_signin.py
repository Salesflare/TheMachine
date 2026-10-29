"""Codex in Connections (+ Add, Codex): whether Codex is signed in here, and its own device sign-in from the dashboard.

Codex signs in with a code: `codex login --device-auth` prints OpenAI's device page and a one-time code, the owner
enters the code there on any device, and the CLI keeps its sign-in in ~/.codex as it always does. The dashboard shows
that code and link, so nobody types a command. Nothing is read, copied or stored here but whether Codex is signed in
(`codex login status`, which prints no secrets). On a hosted Machine the control plane starts the same sign-in on the
server (POST /_machine/connect, like GitHub's) and the dashboard follows it there; this module runs it on a self-hosted
Machine, and reports the status on both.
"""
from __future__ import annotations

import os
import re
import subprocess
import threading
import time

import agent_jobs

DEVICE_PAGE = re.compile(r'https://auth\.openai\.com/codex/device[\w/.-]*')
CODE = re.compile(r'\b[A-Z0-9]{4}-[A-Z0-9]{4,6}\b')
ANSI = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]')
WAIT = 900          # seconds a code stays good (Codex's own: 15 minutes)
STATUS_TTL = 5      # seconds a `codex login status` answer is used again
_status = {'at': 0.0, 'key': None, 'value': None}
_lock = threading.Lock()


def binary(config):
    """The Codex CLI this Machine's jobs use: as configured, on PATH or in ~/.local/bin, else the Codex app's own."""
    own = (agent_jobs.settings(config) or {}).get('codex')
    command = own.get('command') if isinstance(own, dict) else None
    return agent_jobs.find('codex', command) or agent_jobs.desktop_codex()


def status(config):
    """'connected', 'signed_out', or None when Codex isn't on this Machine."""
    codex = binary(config)
    if not codex:
        return None
    with _lock:
        if _status['key'] == codex and time.monotonic() - _status['at'] < STATUS_TTL:
            return _status['value']
    try:
        result = subprocess.run([codex, 'login', 'status'], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=20)
        said = (result.stdout or '') + (result.stderr or '')
        value = ('connected' if result.returncode == 0 and re.search(r'logged in', said, re.I) and not re.search(r'not logged in', said, re.I)
                 else 'signed_out')
    except (OSError, subprocess.SubprocessError):
        value = 'signed_out'
    with _lock:
        _status.update(at=time.monotonic(), key=codex, value=value)
    return value


def forget():
    with _lock:
        _status.update(at=0.0, key=None, value=None)


class Signin:
    """One device sign-in at a time on this Machine. view(): {state, code?, url?, error?}, the state one of starting,
    code (enter it at url), done, failed, missing (no Codex here) or none."""

    def __init__(self):
        self.lock = threading.Lock()
        self.state = {'state': 'none'}
        self.process = None

    def view(self):
        with self.lock:
            return dict(self.state)

    def start(self, config):
        with self.lock:
            if self.state['state'] in ('starting', 'code') and self.process and self.process.poll() is None:
                return dict(self.state)  # pressed again: the same sign-in
        codex = binary(config)
        if not codex:
            return self._set({'state': 'missing'})
        forget()
        if status(config) == 'connected':
            return self._set({'state': 'done'})
        try:
            process = subprocess.Popen([codex, 'login', '--device-auth'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True, env={**os.environ, 'BROWSER': 'true'})
        except OSError:
            return self._set({'state': 'failed', 'error': 'Codex did not start its sign-in. Try again.'})
        with self.lock:
            self.process = process
            self.state = {'state': 'starting'}
        threading.Thread(target=self._follow, args=(config, process), name='codex-signin', daemon=True).start()
        return self.view()

    def _set(self, state):
        with self.lock:
            self.state = state
            return dict(state)

    def _follow(self, config, process):
        timer = threading.Timer(WAIT, process.kill)
        timer.start()
        seen, shown = '', False
        try:
            for line in process.stdout:
                seen = (seen + ANSI.sub('', line))[-4000:]
                page, code = DEVICE_PAGE.search(seen), CODE.search(seen)
                if not shown and page and code:
                    shown = True
                    self._set({'state': 'code', 'code': code.group(0), 'url': page.group(0)})
            process.wait()
        finally:
            timer.cancel()
            process.stdout.close()
        forget()
        if process.returncode == 0 and status(config) == 'connected':
            self._set({'state': 'done'})
        else:
            self._set({'state': 'failed', 'error': 'The sign-in code expired or was not approved.' if shown
                       else 'Codex did not start its sign-in. Try again.'})

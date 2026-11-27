"""Claude Code's own sign-in, which a main model on the Claude CLI route runs on (models.claude_plan_route): whether it
holds one, the plan's kind and when it ends, from `claude auth status --json` (it prints no secrets; only loggedIn,
subscriptionType and loginExpiresAt are kept).

A Claude sign-in ends on a fixed day: Claude Code keeps the end its sign-in got, a token refresh never moves it later,
and after it Claude Code asks for /login again. Until its next refresh fails it still says loggedIn, so a reading past
its end counts as signed out. Two hosted Machines lost theirs about four weeks after signing in, and every review
failed for hours with nothing on the dashboard (2026-11): Needs you says it now (machine/app/status.py needs_you), three
days ahead too, and a lapse is told once on the phone and in Telegram (machine/app/ai_signin.py).

read() runs the command at most once per SOON and keeps a reading HOLD seconds (shorter while signed out). It reads
again sooner when Claude Code's credentials file changed (a sign-in: its time only, never what it holds) or the AI failed
its check since (stale, from model_check_run). wait=False never runs it on the caller's thread (the status poll): the last
reading, or None before the first, while one background thread reads it again."""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

LAYER = 0  # what Claude Code says of its own sign-in (a leaf)

HOLD = {True: 3600, False: 300}  # seconds a reading holds, by whether it was signed in
SOON = 60  # never two readings closer than this
ENDS_SOON = 3 * 86400  # Claude Code itself warns this long before its sign-in ends
TIMEOUT = 30
_lock = threading.Lock()
_cache = {'at': float('-inf'), 'found': None, 'stamp': None, 'reading': False, 'stale': False}


def binary(config):
    """Claude Code's executable: config `claude`, else the one on PATH, else Anthropic's installer's place; None."""
    found = (config or {}).get('claude') or shutil.which('claude')
    local = Path.home() / '.local' / 'bin' / 'claude'
    return str(found) if found else str(local) if local.exists() else None


def stamp():
    """When Claude Code's credentials last changed (the file's time, never its contents), or None."""
    try:
        return int((Path.home() / '.claude' / '.credentials.json').stat().st_mtime)
    except OSError:
        return None


def plan_kind(plan):
    words = re.findall(r'[a-z]+', re.sub(r'^self_serve_', '', str(plan or '').strip().lower()))
    return words[0] if words else None


def parse(text, now):
    """{'signed_in', 'plan', 'expires_at'} from what `claude auth status --json` printed; None when it isn't that.
    signed_in is False once expires_at (ISO, UTC) passed, whatever loggedIn says."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get('loggedIn'), bool):
        return None
    ends = _when(data.get('loginExpiresAt')) if data['loggedIn'] else None
    signed = data['loggedIn'] and not (ends and ends.timestamp() <= now)
    return {'signed_in': signed, 'plan': plan_kind(data.get('subscriptionType')) if signed else None,
            'expires_at': ends.isoformat() if ends else None}


def _when(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)', value):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(dt.timezone.utc).replace(microsecond=0)
    except ValueError:
        return None


def stale():
    """The AI failed its check: read the sign-in again at the next chance (still at most once per SOON)."""
    with _lock:
        _cache['stale'] = True


def reset():
    with _lock:
        _cache.update(at=float('-inf'), found=None, stamp=None, reading=False, stale=False)


def _due(clock):
    found, age = _cache['found'], clock() - _cache['at']
    if age < SOON:
        return False
    if _cache['stale'] or _cache['stamp'] != stamp():
        return True
    hold = HOLD[bool(found and found['signed_in'])]
    if found and found.get('expires_at'):  # held past its end, never: it is read again right after
        hold = min(hold, max(SOON, dt.datetime.fromisoformat(found['expires_at']).timestamp() - time.time() + SOON))
    return age >= hold


def _read(config, run, clock):
    path = binary(config)
    found = None
    if path:
        try:
            found = parse(run([path, 'auth', 'status', '--json'], capture_output=True, text=True, timeout=TIMEOUT).stdout, time.time())
        except (OSError, subprocess.TimeoutExpired):
            found = None
    with _lock:
        _cache.update(at=clock(), found=found, stamp=stamp(), reading=False, stale=False)
    return found


def read(config, run=subprocess.run, clock=time.monotonic, wait=True):
    """The last reading of Claude Code's sign-in ({'signed_in', 'plan', 'expires_at'}), read again when due; None when
    there is no Claude Code or it can't tell. wait=False: never on this thread (see the module's text)."""
    with _lock:
        due = _due(clock)
        found = _cache['found']
        start = due and not wait and not _cache['reading']
        if start:
            _cache['reading'] = True
    if due and wait:
        return _read(config, run, clock)
    if start:
        def background():
            try:
                _read(config, run, clock)
            finally:
                with _lock:
                    _cache['reading'] = False
        threading.Thread(target=background, name='claude-signin', daemon=True).start()
    return found


def days_left(found, now):
    """Whole days until a sign-in that ends within ENDS_SOON ends (0: today), else None."""
    ends = (found or {}).get('expires_at') if (found or {}).get('signed_in') else None
    if not ends:
        return None
    left = dt.datetime.fromisoformat(ends).timestamp() - now
    return int(left // 86400) if 0 < left <= ENDS_SOON else None

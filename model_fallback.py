"""A fallback model that carries work past the sign-in's usage limits (model_budget.py, docs/help/model.md, "With a fallback").

The usage rules (model_budget.py: pacing at 65/85% of the 5-hour window and the day's share of the week, holding
everything once a limit is reached) protect a sign-in whose limits are shared with the owner's own chats. When
OpenClaw has a fallback in `agents.defaults.model.fallbacks` that is billed apart from the main model (another
provider: a custom provider, an API key, another plan), it takes over once the main model reaches its limit (OpenClaw
treats a usage limit as a rate limit and moves to the next model), so holding work back only makes it wait.

So the rules are set aside while such a fallback is known to work: its last check answered within OK_SECONDS and
nothing failed since. The check is one tiny one-shot turn on that model alone (`openclaw infer model run --model`,
strict: no other model answers for it), made only while the main model's limits would hold work back, at most every
CHECK_GAP. A failed check, or a run that still ended on a usage limit, brings the rules back until a check passes.
No content goes out: the prompt is fixed."""
from __future__ import annotations

import json
import subprocess
import threading
import time
from pathlib import Path

import model_budget

OK_SECONDS = 3600       # a check that passed counts this long
REFRESH_SECONDS = 2700  # checked again this old, while it matters, so it doesn't lapse
CHECK_GAP = 900         # never checked more often than this
TIMEOUT = 90
PROMPT = 'Reply with OK.'


def configured(config):
    """(primary, [fallbacks]) from openclaw.json (`agents.defaults.model`); ('', []) when unreadable."""
    path = Path((config or {}).get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        model = json.loads(path.read_text()).get('agents', {}).get('defaults', {}).get('model')
    except (OSError, ValueError, AttributeError):
        return '', []
    if isinstance(model, str):
        return model.strip(), []
    if not isinstance(model, dict):
        return '', []
    primary = model.get('primary') if isinstance(model.get('primary'), str) else ''
    fallbacks = [m.strip() for m in model.get('fallbacks') or [] if isinstance(m, str) and '/' in m.strip()]
    return primary.strip(), fallbacks[:8]


def separate(primary, fallbacks):
    """The fallbacks billed apart from the primary: another provider (model_budget.provider_of, so `openai-codex` is the
    same ChatGPT sign-in as `openai`). Same provider counts as the same limits, to be safe."""
    own = model_budget.provider_of(primary)
    return [m for m in fallbacks if model_budget.provider_of(m) and model_budget.provider_of(m) != own]


def probe(config, model, run=subprocess.run):
    """One tiny turn on `model` alone through the Gateway. True when it answered."""
    args = [str((config or {}).get('openclaw') or 'openclaw'), 'infer', 'model', 'run', '--gateway', '--json',
            '--model', model, '--prompt', PROMPT]
    try:
        result = run(args, capture_output=True, text=True, timeout=TIMEOUT)
        data = json.loads(result.stdout or '{}')
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False
    texts = [o.get('text') for o in data.get('outputs') or [] if isinstance(o, dict) and isinstance(o.get('text'), str)]
    return result.returncode == 0 and data.get('ok') is True and any(t.strip() for t in texts)


class Health:
    """What the checks found, per fallback model, in memory: a restart checks again when it matters."""

    def __init__(self, check=probe):
        self.check, self.seen, self.lock = check, {}, threading.Lock()

    def working(self, models, now_s=None):
        """The first of `models` known to work now, or None."""
        now_s = time.time() if now_s is None else now_s
        for model in models:
            seen = self.seen.get(model) or {}
            ok = seen.get('ok', 0)
            if ok > now_s - OK_SECONDS and ok >= seen.get('failed', 0):
                return model
        return None

    def doubt(self, now_s=None):
        """A run ended on a usage limit after all: no fallback counts as working until a check passes again."""
        now_s = time.time() if now_s is None else now_s
        with self.lock:
            for seen in self.seen.values():
                seen['failed'] = max(seen.get('failed', 0), now_s)

    def refresh(self, config, models, now_s=None):
        """Checks the fallbacks in order until one works, skipping those checked within CHECK_GAP or found working
        within REFRESH_SECONDS. Returns the working one, or None. Blocks for the checks: call it from a worker."""
        now_s = time.time() if now_s is None else now_s
        for model in models:
            seen = self.seen.setdefault(model, {})
            if seen.get('ok', 0) > now_s - REFRESH_SECONDS and seen.get('ok', 0) >= seen.get('failed', 0):
                return model
            if seen.get('tried', 0) > now_s - CHECK_GAP:
                continue
            seen['tried'] = now_s
            passed = self.check(config, model)
            with self.lock:
                seen['ok' if passed else 'failed'] = time.time()
            if passed:
                return model
        return self.working(models, now_s)

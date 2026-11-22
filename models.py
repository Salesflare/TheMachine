"""Which model OpenClaw runs, whether it can run, and what background work uses: plain functions any module may import
(they read OpenClaw's own config and `openclaw models status`; nothing of the app's).

`config` is The Machine's config.json (its `openclaw_config` and `openclaw` say where OpenClaw's config and command
are; both default to the usual places)."""
import json
from pathlib import Path
import subprocess
import threading
import time

# Background work never runs on these models (several times the cost for the same result): a cheaper one instead, the
# first the owner's model allowlist names. With an allowlist that allows any, the last: one every OpenClaw we support
# knows (OpenClaw 2026.11.2 runs GPT-6.2 Sol only with its own entry in openclaw.json, docs/models.md).
BACKGROUND_SWAP = {'gpt-6-astra': ('gpt-6.2-sol', 'gpt-6.1-sol')}
# For now (since 2026-11-22), background work on the ChatGPT sign-in (CHATGPT_PROVIDERS) runs on GPT-6.1 Sol, not
# GPT-6.2 Sol: on that route (OpenClaw's native Codex responses) GPT-6.2 Sol never takes the system prompt
# (`instructions`) from the prompt cache, so every call after a session's first pays about 27k fresh input tokens
# again (fresh input per call tripled). Once a probe shows GPT-6.2 Sol caching it, set this to False: background work
# then follows BACKGROUND_SWAP and the main model again. The owner's chat model and a model they picked stay as they are.
GPT_62_UNCACHED = True
CHATGPT_PROVIDERS = ('openai', 'openai-codex')


def openclaw_model(config):
    """The model OpenClaw answers with by default (`agents.defaults.model` in openclaw.json); None when unknown."""
    path = Path(config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        model = json.loads(path.read_text()).get('agents', {}).get('defaults', {}).get('model')
    except (OSError, ValueError, AttributeError):
        return None
    model = model.get('primary') if isinstance(model, dict) else model
    return model.strip()[:80] if isinstance(model, str) and model.strip() else None


def claude_plan_route(config):
    """Whether OpenClaw runs the default model through the installed Claude Code (its Claude CLI route), so usage
    counts against the Claude plan Claude Code is signed in to. Read from openclaw.json; Claude Code's own sign-in is
    never read."""
    path = Path(config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        defaults = json.loads(path.read_text()).get('agents', {}).get('defaults', {})
        model, models = defaults.get('model'), defaults.get('models') or {}
    except (OSError, ValueError, AttributeError):
        return False
    model = model.get('primary') if isinstance(model, dict) else model
    if not isinstance(model, str) or not isinstance(models, dict):
        return False
    if model.startswith('claude-cli/'):
        return True

    def runtime(key):
        entry = models.get(key)
        found = entry.get('agentRuntime') if isinstance(entry, dict) else None
        return found.get('id') if isinstance(found, dict) and found.get('id') not in (None, 'default') else None
    return (runtime(model) or (runtime('anthropic/*') if model.startswith('anthropic/') else None)) == 'claude-cli'


def main_model():
    """OpenClaw's main model (agents.defaults.model), or ''."""
    import onboarding
    model = ((onboarding.openclaw_settings().get('agents') or {}).get('defaults') or {}).get('model')
    model = model.get('primary') if isinstance(model, dict) else model
    return model.strip() if isinstance(model, str) else ''


MODEL_READY_SECONDS = {True: 600, False: 60}  # how long one reading of `models status` holds, by its answer
_model_ready = {}
_model_reading = set()  # models whose `models status` is being read in the background now
_model_lock = threading.Lock()


def model_ready(config=None, run=subprocess.run, wait=True):
    """Whether the main model can run, as `openclaw models status` says (no model call; the same reading a hosted
    Machine's health report uses): its provider has a sign-in or key, and any provider in use without one is only a
    fallback's. None when that can't be read. Cached a short while; a not-ready answer for less long.

    wait=False never runs the command on the caller's thread (a request answering the status poll: one `openclaw`
    process takes 20 s or more on a busy Machine): the last reading, even an expired one, or None before the first,
    while one background thread reads it again."""
    model = main_model()
    if not model:
        return False
    hit = _model_ready.get(model)
    if hit and hit[0] > time.monotonic():
        return hit[1]
    if wait:
        return _read_model_ready(model, config, run)
    with _model_lock:
        start = model not in _model_reading
        _model_reading.add(model)
    if start:
        def read():
            try:
                _read_model_ready(model, config, run)
            finally:
                with _model_lock:
                    _model_reading.discard(model)
        threading.Thread(target=read, name='model-ready', daemon=True).start()
    return hit[1] if hit else None


def _read_model_ready(model, config, run):
    try:
        result = run([str((config or {}).get('openclaw') or 'openclaw'), 'models', 'status', '--json'],
                     capture_output=True, text=True, timeout=90)
        data = json.loads(result.stdout)
        missing = {p for p in (data.get('auth') or {}).get('missingProvidersInUse') or [] if isinstance(p, str)}
        fallbacks = {m.split('/')[0] for m in data.get('fallbacks') or [] if isinstance(m, str)}
    except (OSError, ValueError, AttributeError, subprocess.TimeoutExpired):
        return None
    ready = model.split('/')[0] not in missing and missing <= fallbacks
    _model_ready[model] = (time.monotonic() + MODEL_READY_SECONDS[ready], ready)
    return ready


def background_model(config):
    """(provider, model) for The Machine's background turns when the main model is one background work never uses
    (BACKGROUND_SWAP, and GPT-6.2 Sol on the ChatGPT sign-in while GPT_62_UNCACHED): the first cheaper one the owner's
    model allowlist (`agents.defaults.models`) names, else the last when it allows any (empty, or `provider/*`).
    None: the main model."""
    main = openclaw_model(config) or ''
    provider, _, name = main.partition('/')
    cheaper = BACKGROUND_SWAP.get(name)
    if GPT_62_UNCACHED and provider in CHATGPT_PROVIDERS:
        cheaper = ('gpt-6.1-sol',) if name == 'gpt-6.2-sol' else tuple(m for m in cheaper or () if m != 'gpt-6.2-sol')
    if not cheaper:
        return None
    path = Path(config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        allowed = json.loads(path.read_text()).get('agents', {}).get('defaults', {}).get('models') or {}
    except (OSError, ValueError, AttributeError):
        allowed = {}
    allowed = set(allowed) if isinstance(allowed, dict) else set()
    named = next((m for m in cheaper if f'{provider}/{m}' in allowed), None)
    if named:
        return provider, named
    return (provider, cheaper[-1]) if not allowed or f'{provider}/*' in allowed else None


def has_model(config=None, wait=True, answered=None, unknown=True):
    """Whether OpenClaw has a main model to review with that can run (model_ready). When that can't be read,
    a main model set in its config is taken as one (`unknown`). wait=False: a turn the owner waits on never waits for
    `models status` too (model_ready's last reading). answered: the app's database; then also that the main model
    answered its real check (model_check.py), or another model the first look can fall back to did."""
    model = main_model()
    ready = model_ready(config, wait=wait) if model else False
    if ready is False or (ready is None and not unknown):
        return False
    if answered is None:
        return True
    import model_check
    return model_check.passed(answered, model) or bool(model_check.fallback(answered, model))

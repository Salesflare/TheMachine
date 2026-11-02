"""Which model OpenClaw runs, whether it can run, and what background work uses: plain functions any module may import
(they read OpenClaw's own config and `openclaw models status`; nothing of the app's).

`config` is The Machine's config.json (its `openclaw_config` and `openclaw` say where OpenClaw's config and command
are; both default to the usual places)."""
import json
from pathlib import Path
import subprocess
import time

# Background work never runs on these models (several times the cost for the same result): the cheaper one instead.
BACKGROUND_SWAP = {'gpt-6-astra': 'gpt-6.1-sol'}


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


def model_ready(config=None, run=subprocess.run):
    """Whether the main model can run, as `openclaw models status` says (no model call; the same reading a hosted
    Machine's health report uses): its provider has a sign-in or key, and any provider in use without one is only a
    fallback's. None when that can't be read. Cached a short while; a not-ready answer for less long."""
    model = main_model()
    if not model:
        return False
    hit = _model_ready.get(model)
    if hit and hit[0] > time.monotonic():
        return hit[1]
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
    (BACKGROUND_SWAP), and the owner's model allowlist (`agents.defaults.models`, empty allows any) allows the other.
    None: the main model."""
    main = openclaw_model(config) or ''
    provider, _, name = main.partition('/')
    cheaper = BACKGROUND_SWAP.get(name)
    if not cheaper:
        return None
    path = Path(config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        allowed = json.loads(path.read_text()).get('agents', {}).get('defaults', {}).get('models') or {}
    except (OSError, ValueError, AttributeError):
        allowed = {}
    if isinstance(allowed, dict) and allowed and not ({f'{provider}/{cheaper}', f'{provider}/*'} & set(allowed)):
        return None
    return provider, cheaper


def has_model(config=None):
    """Whether OpenClaw has a main model to review with that can run (model_ready). When that can't be read,
    a main model set in its config is taken as one."""
    return bool(main_model()) and model_ready(config) is not False

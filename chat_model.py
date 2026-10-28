"""Which model and thinking level answer in a chat: the default for chats (Settings, Model) and one chat's own choice
(the small pill under a to-do chat's or Help's message box).

The choices are what OpenClaw's running Gateway lists (`models.list`, its "configured" view: the configured models and
those of every provider with a sign-in, each with the thinking levels it supports for that model). Only models whose
provider is signed in (`available`) and that the owner's model allowlist allows are offered, so a Machine signed in with
ChatGPT only offers ChatGPT's models, and Claude's only show once Claude is connected.

A choice goes with each turn (the Gateway's `agent` call takes provider, model and thinking; Help's `infer model run`
takes --model and --thinking), so nothing in OpenClaw's own config changes and the Gateway never reloads or restarts.
Without any choice, turns run exactly as before: OpenClaw's main model and thinking level. The default for chats is
`chat_model` in config.json ({"model": "provider/id", "thinking": "high"}, either may be missing: then OpenClaw's); a
to-do's own choice is in the chat_models table, and Help's lives in the dashboard for that Help conversation. Background
work (reviews, drafts prepared ahead, the profile) keeps its own model (assistant.background_model)."""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

# Every thinking level OpenClaw knows, from none to most; a model supports some of them.
LEVELS = ('off', 'minimal', 'low', 'medium', 'high', 'xhigh', 'adaptive', 'max', 'ultra')
REF = re.compile(r'[a-z0-9-]{1,40}/[A-Za-z0-9._:/-]{1,120}')
CATALOG_SECONDS = 600  # how long one reading of the Gateway's model list holds
MAX_MODELS = 80


def initialize(db):
    db.execute('CREATE TABLE IF NOT EXISTS chat_models(suggestion_id TEXT PRIMARY KEY,model TEXT,thinking TEXT,updated_at TEXT NOT NULL)')


def openclaw_settings(config):
    path = Path((config or {}).get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json')
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    defaults = (data.get('agents') or {}).get('defaults') if isinstance(data, dict) else None
    return defaults if isinstance(defaults, dict) else {}


def main(config):
    """(model, thinking) OpenClaw answers with when nothing is chosen: agents.defaults.model.primary and
    agents.defaults.thinkingDefault; None for what it doesn't set."""
    defaults = openclaw_settings(config)
    model = defaults.get('model')
    model = model.get('primary') if isinstance(model, dict) else model
    thinking = defaults.get('thinkingDefault')
    return (model.strip() if isinstance(model, str) and REF.fullmatch(model.strip()) else None,
            thinking if thinking in LEVELS else None)


def allowed(config, ref):
    """Whether the owner's model allowlist (agents.defaults.models, or agents.defaults.modelPolicy.allow) lets a turn use
    this model. No allowlist allows every model."""
    defaults = openclaw_settings(config)
    keys = set()
    if isinstance(defaults.get('models'), dict):
        keys |= set(defaults['models'])
    policy = defaults.get('modelPolicy')
    if isinstance(policy, dict) and isinstance(policy.get('allow'), list):
        keys |= {k for k in policy['allow'] if isinstance(k, str)}
    return not keys or ref in keys or ref.split('/')[0] + '/*' in keys or '*' in keys


def parse_catalog(reply, config=None):
    """The models a chat can pick, from a `models.list` reply: [{'ref', 'name', 'levels', 'default'}], signed-in and
    allowed ones only, in the Gateway's order (each provider's recommended ones first)."""
    out, seen = [], set()
    for row in (reply or {}).get('models') or []:
        if not isinstance(row, dict) or row.get('available') is not True:
            continue
        ref = f"{row.get('provider')}/{row.get('id')}"
        if not REF.fullmatch(ref) or ref in seen or not allowed(config, ref):
            continue
        levels = [x.get('id') for x in row.get('thinkingLevels') or [] if isinstance(x, dict)]
        levels = [x for x in LEVELS if x in levels]  # in order, only the ones OpenClaw knows
        seen.add(ref)
        out.append({'ref': ref, 'name': str(row.get('name') or row.get('id'))[:80], 'levels': levels,
                    'default': row.get('thinkingDefault') if row.get('thinkingDefault') in levels else (levels[0] if levels else None)})
        if len(out) >= MAX_MODELS:
            break
    return out


def gateway_call(config, method, params, run=subprocess.run):
    """One read-only Gateway RPC (a short client, no model call); its JSON reply, or None."""
    try:
        result = run([str((config or {}).get('openclaw') or 'openclaw'), 'gateway', 'call', method, '--json',
                      '--timeout', '30000', '--params', json.dumps(params)],
                     capture_output=True, text=True, timeout=60)
        reply = json.loads(result.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    return reply if result.returncode == 0 and isinstance(reply, dict) else None


def session_levels(reply):
    """(model ref, levels, default) of the latest session in a `sessions.list` reply, or None without levels."""
    sessions = (reply or {}).get('sessions')
    session = sessions[0] if isinstance(sessions, list) and sessions and isinstance(sessions[0], dict) else {}
    ref = f"{session.get('modelProvider') or ''}/{session.get('model') or ''}"
    levels = {x.get('id') for x in session.get('thinkingLevels') or [] if isinstance(x, dict)}
    levels = [x for x in LEVELS if x in levels]
    if not REF.fullmatch(ref) or len(levels) < 2:
        return None
    return ref, levels, session.get('thinkingDefault') if session.get('thinkingDefault') in levels else levels[0]


def fill_levels(models, config, session):
    """The model list with the main model's thinking levels filled in from its session when the list has none for it.
    Some Gateways list a model without its levels (or not at all, while it is the one every turn runs on), though a
    session on it has them: without this a chat showed the model but no thinking picker."""
    if not session:
        return models
    ref, levels, default = session
    if ref != main(config)[0] and ref not in {m['ref'] for m in models}:
        return models
    for entry in models:
        if entry['ref'] == ref:
            if len(entry['levels']) < 2:
                entry.update(levels=levels, default=default)
            return models
    if allowed(config, ref):
        models.insert(0, {'ref': ref, 'name': ref.split('/', 1)[1][:80], 'levels': levels, 'default': default})
    return models


def read_catalog(config, run=subprocess.run):
    """The Gateway's model list, parsed; None when it can't be read. When the main model is missing or comes without
    its thinking levels, the latest session says them (fill_levels)."""
    reply = gateway_call(config, 'models.list', {'view': 'configured'}, run)
    if not reply or not isinstance(reply.get('models'), list):
        return None
    models = parse_catalog(reply, config)
    main_model = main(config)[0]
    if main_model and not any(m['ref'] == main_model and len(m['levels']) > 1 for m in models):
        models = fill_levels(models, config, session_levels(gateway_call(config, 'sessions.list', {'limit': 1}, run)))
    return models


class Catalog:
    """The last good reading of the model list, read again when CATALOG_SECONDS old (from the model usage worker)."""

    def __init__(self, reader=read_catalog):
        self.reader, self.models, self.read_at = reader, None, 0.0

    def refresh(self, config, force=False):
        if not force and self.models is not None and time.monotonic() - self.read_at < CATALOG_SECONDS:
            return self.models
        found = self.reader(config)
        if found is not None:
            self.models, self.read_at = found, time.monotonic()
        return self.models


def nearest(level, levels):
    """The supported level closest to the one asked for (OpenClaw maps the same way); None without levels."""
    if not levels:
        return None
    if level in levels:
        return level
    at = LEVELS.index(level) if level in LEVELS else LEVELS.index('low')
    return min(levels, key=lambda x: (abs(LEVELS.index(x) - at), -LEVELS.index(x)))


def clean(choice):
    """{'model', 'thinking'} with what isn't a model ref or a known level left out."""
    choice = choice if isinstance(choice, dict) else {}
    model, thinking = choice.get('model'), choice.get('thinking')
    out = {}
    if isinstance(model, str) and REF.fullmatch(model):
        out['model'] = model
    if thinking in LEVELS:
        out['thinking'] = thinking
    return out


def saved_default(config):
    return clean((config or {}).get('chat_model'))


def resolve(config, models, own=None):
    """{'model', 'thinking'} a chat runs with: its own choice, else the default for chats, else OpenClaw's; a model the
    sign-in no longer offers falls back to OpenClaw's main model, and the level to the nearest that model supports."""
    main_model, main_thinking = main(config)
    picked = {**saved_default(config), **clean(own)}
    by_ref = {m['ref']: m for m in models or []}
    model = picked.get('model') or main_model
    if models is not None and model not in by_ref:
        model = main_model
    entry = by_ref.get(model)
    levels = entry['levels'] if entry else []
    thinking = picked.get('thinking') or main_thinking or (entry or {}).get('default')
    if levels:
        thinking = nearest(thinking, levels)
    return {'model': model, 'thinking': thinking}


def chosen(config, own=None):
    """Whether anything was picked for this chat or as the default; without that, turns go exactly as before."""
    return bool(saved_default(config) or clean(own))


def turn_args(config, models, own=None):
    """What the Gateway's `agent` call gets for an owner's chat turn: {} when nothing was picked, else the provider,
    model and thinking level (resolve)."""
    if not chosen(config, own):
        return {}
    found = resolve(config, models, own)
    out = {}
    if found['model']:
        provider, _, name = found['model'].partition('/')
        out.update(provider=provider, model=name)
    if found['thinking']:
        out['thinking'] = found['thinking']
    return out


def check(choice, models, config=None):
    """A choice from the dashboard, checked against what the sign-in offers. Raises ValueError otherwise."""
    if models is None:
        raise ValueError('The model list isn’t loaded yet. Try again in a minute.')
    choice = choice if isinstance(choice, dict) else {}
    out = {}
    by_ref = {m['ref']: m for m in models}
    model = choice.get('model')
    if model not in (None, ''):
        if not isinstance(model, str) or model not in by_ref:
            raise ValueError('That model isn’t available with your sign-in.')
        out['model'] = model
    thinking = choice.get('thinking')
    if thinking not in (None, ''):
        target = by_ref.get(resolve(config, models, out)['model'])
        if not target or thinking not in target['levels']:
            raise ValueError('That model has no such thinking level.')
        out['thinking'] = thinking
    return out


def card_choice(db, suggestion_id):
    row = db.execute('SELECT model,thinking FROM chat_models WHERE suggestion_id=?', (suggestion_id,)).fetchone()
    return clean({'model': row[0], 'thinking': row[1]}) if row else {}


def set_card(db, suggestion_id, choice, at):
    """Keeps a to-do chat's own choice; one that is the same as the default for chats is not kept (it then follows the
    default when that changes)."""
    if not choice:
        db.execute('DELETE FROM chat_models WHERE suggestion_id=?', (suggestion_id,))
        return
    db.execute('INSERT INTO chat_models(suggestion_id,model,thinking,updated_at) VALUES(?,?,?,?) ON CONFLICT(suggestion_id) '
               'DO UPDATE SET model=excluded.model,thinking=excluded.thinking,updated_at=excluded.updated_at',
               (suggestion_id, choice.get('model'), choice.get('thinking'), at))


def minimal(config, models, choice, base=None):
    """The part of a choice that differs from what it would get anyway (`base`, else the default for chats)."""
    base = resolve(config, models, base) if base is not None else resolve(config, models)
    found = resolve(config, models, choice)
    return {k: found[k] for k in ('model', 'thinking') if found[k] and found[k] != base[k]}


def view(config, models):
    """What the dashboard shows: the models to pick from, OpenClaw's own, and the default for chats as it resolves."""
    main_model, main_thinking = main(config)
    return {'models': models or [], 'known': models is not None, 'main': {'model': main_model, 'thinking': main_thinking},
            'default': resolve(config, models), 'saved': saved_default(config)}

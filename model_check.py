"""Whether the AI really answers: one tiny model call with no content of the owner's (model_fallback.PROMPT), made when an
AI connects (a sign-in or a key: the main model changed, or nothing was checked yet), before the first look starts.

A sign-in that exists is not enough (models.model_ready reads only that): a first look once started while the Claude
sign-in was still finishing, and the owner then waited hours for a first to-do (2026-10-27). So the first look waits
for a check that passed (models.has_model(answered=db)). A failed check keeps the owner on the AI step with the
provider's own error (short, behind Details), and is made again a minute later, then 2, then every 5 minutes, and at
once when a sign-in changes (a reconnect: file times only, never what the files hold).

When the main model fails its check, or the first look's last pass failed, another AI the owner has signed in (a
fallback in OpenClaw's config, or a model of another provider the Gateway lists) is checked the same way; the first
look then runs on the first one that answers (App.first_look_model).

The check is stored as the milestone `model_check`: {model, ok, at, error, stamp, failed (failures in a row), fallback,
fallback_at}. Read by the hosted agent for the setup page (health `model.check`)."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import subprocess

import model_budget
import model_fallback

NAME = 'model_check'
PROMPT = model_fallback.PROMPT  # fixed: nothing of the owner's goes out
RETRY_SECONDS = (60, 120, 300)  # a failed check is made again this long after its 1st, 2nd, 3rd and later failure in a row
SOON_SECONDS = 20  # never two checks closer than this, also when a sign-in changed in between
FALLBACK_SECONDS = 300  # a fallback is looked for again at most this often
TIMEOUT = 90
ERROR_CHARS = 300
FALLBACKS = 3  # at most this many other models checked per round

# What never shows from a provider's error: anything like a key or token, an address
SECRET = re.compile(r'(?i)\b(?:sk|rk|pk|key)-[A-Za-z0-9_-]{6,}|\bBearer\s+\S+|\b[A-Za-z0-9_\-]{32,}\b|[\w.+-]+@[\w-]+\.[\w.-]+')
ANSI = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')


def sign_in_stamp(config):
    """When the sign-ins last changed, from the times of the files that hold them, never their contents: OpenClaw's
    config (a key, a ChatGPT sign-in, the model) and Claude Code's credentials."""
    paths = (Path((config or {}).get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json'),
             Path.home() / '.claude' / '.credentials.json')
    stamps = []
    for path in paths:
        try:
            stamps.append(str(int(path.stat().st_mtime)))
        except OSError:
            stamps.append('-')
    return ','.join(stamps)


def short_error(text):
    """A provider's error for Details: its first lines, at most ERROR_CHARS, with anything like a key taken out."""
    text = ANSI.sub('', str(text or ''))
    text = ' '.join(line.strip() for line in text.splitlines() if line.strip())
    text = SECRET.sub('…', text)
    return text[:ERROR_CHARS].rstrip() or None


def _error(data, stderr):
    """The provider's message from `openclaw infer model run --json`: its error, else the last lines it wrote."""
    for value in (data.get('error'), data.get('message'), data.get('errorMessage')):
        if isinstance(value, dict):
            value = value.get('message') or value.get('error')
        if isinstance(value, str) and value.strip():
            return short_error(value)
    lines = [line for line in str(stderr or '').splitlines() if line.strip()]
    return short_error('\n'.join(lines[-3:]))


def probe(config, model=None, run=subprocess.run):
    """(ok, error): one tiny turn through the Gateway, on `model` alone when given, else on the main model. `error` is
    the provider's own message, short (short_error), or why there was none."""
    args = [str((config or {}).get('openclaw') or 'openclaw'), 'infer', 'model', 'run', '--gateway', '--json', '--prompt', PROMPT]
    if model:
        args += ['--model', model]
    try:
        result = run(args, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, f'No answer within {TIMEOUT} seconds.'
    except OSError:
        return False, 'OpenClaw could not be started.'
    try:
        data = json.loads(result.stdout or '{}')
    except ValueError:
        data = {}
    data = data if isinstance(data, dict) else {}
    texts = [o.get('text') for o in data.get('outputs') or [] if isinstance(o, dict) and isinstance(o.get('text'), str)]
    if result.returncode == 0 and data.get('ok') is True and any(t.strip() for t in texts):
        return True, None
    return False, _error(data, result.stderr) or 'The model gave an empty answer.'


def last(db):
    """The last check ({model, ok, at, error, ...}), or None before the first."""
    row = db.execute('SELECT detail FROM milestones WHERE name=?', (NAME,)).fetchone()
    try:
        found = json.loads(row[0] or 'null') if row else None
    except ValueError:
        return None
    return found if isinstance(found, dict) else None


def passed(db, model):
    """The main model `model` answered its last check."""
    found = last(db)
    return bool(found and found.get('model') == model and found.get('ok'))


def fallback(db, model):
    """The other model the first look runs on while `model` fails its check (or failed the first look's last pass),
    when one answered: its ref, or None."""
    found = last(db)
    return found.get('fallback') if found and found.get('model') == model and isinstance(found.get('fallback'), str) else None


def _seconds(found, key, current):
    try:
        return (current - dt.datetime.fromisoformat(found[key])).total_seconds()
    except (KeyError, TypeError, ValueError):
        return float('inf')


def due(found, model, stamp, current):
    """Whether to check `model` now: not checked yet (a new install, a new sign-in, another main model), or its last check
    failed and either a sign-in changed since (a reconnect: at once) or RETRY_SECONDS passed."""
    if not model:
        return False
    if not found or found.get('model') != model:
        return True
    if found.get('ok'):
        return False
    since = _seconds(found, 'at', current)
    if since < SOON_SECONDS:
        return False
    if found.get('stamp') != stamp:
        return True
    return since >= RETRY_SECONDS[min(max(int(found.get('failed') or 1), 1), len(RETRY_SECONDS)) - 1]


def candidates(config, model, catalog=None):
    """Other AIs the owner has signed in, to fall back to: OpenClaw's fallbacks billed apart from `model`
    (model_fallback.separate), then the first model of each other provider the Gateway lists (chat_model.Catalog rows,
    signed-in ones only, each provider's recommended first). At most FALLBACKS."""
    primary, fallbacks = model_fallback.configured(config)
    found = model_fallback.separate(primary or model, fallbacks)
    own = model_budget.provider_of(primary or model)
    seen = {own, *(model_budget.provider_of(m) for m in found)}
    for row in catalog or []:
        ref = row.get('ref') if isinstance(row, dict) else None
        provider = model_budget.provider_of(ref)
        if provider and provider not in seen:
            found.append(ref)
            seen.add(provider)
    return found[:FALLBACKS]


def check(found, config, model, now_text, run=None):
    """The main model's check, made now: the new state to save."""
    ok, error = (run or probe)(config, None)
    failed = 0 if ok else (int(found.get('failed') or 0) + 1 if found and found.get('model') == model and not found.get('ok') else 1)
    out = {'model': model, 'ok': ok, 'at': now_text, 'stamp': sign_in_stamp(config), 'failed': failed}
    if error:
        out['error'] = error
    if found and found.get('model') == model and not ok:  # a fallback that answered stays until it is looked for again
        out.update({k: found[k] for k in ('fallback', 'fallback_at') if k in found})
    return out


def due_fallback(found, current):
    """Whether to look for a fallback now: never looked, or FALLBACK_SECONDS since the last look."""
    return _seconds(found or {}, 'fallback_at', current) >= FALLBACK_SECONDS


def look_for_fallback(found, config, model, catalog, now_text, current, run=None):
    """While the main model fails (its check, or the first look's last pass): the first other model that answers its
    check, at most every FALLBACK_SECONDS. The new state to save, or None when nothing was looked at."""
    if not due_fallback(found, current):
        return None
    out = {**found, 'fallback_at': now_text}
    out.pop('fallback', None)
    for ref in candidates(config, model, catalog):
        ok, _ = (run or probe)(config, ref)
        if ok:
            out['fallback'] = ref
            break
    return out

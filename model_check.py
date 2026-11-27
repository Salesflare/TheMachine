"""Whether the AI really answers: one tiny model call with no content of the owner's (model_fallback.PROMPT; on a Claude
sign-in Claude Code's own print mode, the executable and sign-in reviews run on: model_fallback.turn), made when an
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
fallback_at}. Read by the hosted agent for the setup page (health `model.check`).

Once a check passed and before any review ran, the Gateway's agent runtime is readied for the first look (warm_up):
Gateway RPCs only, no model call."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import time

import model_budget
import model_fallback
from machine import ai_training

NAME = 'model_check'
PROMPT = model_fallback.PROMPT  # fixed: nothing of the owner's goes out
RETRY_SECONDS = (60, 120, 300)  # a failed check is made again this long after its 1st, 2nd, 3rd and later failure in a row
SOON_SECONDS = 20  # never two checks closer than this, also when a sign-in changed in between
FALLBACK_SECONDS = 300  # a fallback is looked for again at most this often
TIMEOUT = model_fallback.TIMEOUT
ERROR_CHARS = 300
FALLBACKS = 3  # at most this many other models checked per round
# A check that never reached the AI, in our own words (the cloud's ai_plan.py knows them too)
NOT_REACHED = (f'No answer within {TIMEOUT} seconds.', 'OpenClaw could not be started.')

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
    """The provider's message from `openclaw infer model run --json` or `openclaw agent --json`: its error, else the
    last lines it wrote."""
    for value in (data.get('error'), data.get('message'), data.get('errorMessage')):
        if isinstance(value, dict):
            value = value.get('message') or value.get('error')
        if isinstance(value, str) and value.strip():
            return short_error(value)
    lines = [line for line in str(stderr or '').splitlines() if line.strip()]
    return short_error('\n'.join(lines[-3:]))


def probe(config, model=None, run=subprocess.run):
    """(ok, error): one tiny turn through the Gateway, on `model` alone when given, else on the main model. `error` is
    the provider's own message, short (short_error), or why there was none. The turn goes the way the model's work does
    (model_fallback.turn): a raw model call for keys and the ChatGPT sign-in, Claude Code's own print mode for a Claude
    sign-in (its Claude CLI route), which `infer model run` never takes."""
    try:
        ok, data, stderr = model_fallback.turn(config, model, run)
    except subprocess.TimeoutExpired:
        return False, NOT_REACHED[0]
    except OSError:
        return False, NOT_REACHED[1]
    if ok:
        return True, None
    return False, _error(data, stderr) or 'The model gave an empty answer.'


def plan_note(found, status):
    """{'plan': 'chatgpt' or 'claude', 'plan_free': True when its provider says the account is free} for the line about
    the plan under a failed check, else {}. Claude needs a paid plan: also when its plan is unknown. Codex comes with
    ChatGPT's free plan too: only when ChatGPT says the account is free. `status` is what Settings shows
    (model_usage.model_status): nothing is read for this. Not for a check that never reached the AI, a limit reached, an
    API key or another provider, nor a plan its provider says is paid."""
    status = status or {}
    if found.get('error') in NOT_REACHED or status.get('limit_reached') or status.get('model') != found.get('model'):
        return {}
    plan = 'chatgpt' if status.get('chatgpt') else 'claude' if status.get('claude_plan') else None
    kind = ai_training.plan_kind(status.get('plan'))
    if not plan or kind not in (('free',) if plan == 'chatgpt' else (None, 'free')):
        return {}
    return {'plan': plan, **({'plan_free': True} if kind else {})}


WARM_KEY = 'agent:main:assistant-warm-up'


def warm_up(config, run=subprocess.run, clock=None):
    """(ok, seconds): readies the Gateway's agent runtime for the first look, with no model call. A new Gateway's first
    agent run loads and builds its tools (the bridge's included) before it reaches the model, about 3.5 of 8 seconds
    on a quiet desktop and more on a busy one. The same work done ahead through the Gateway's own RPCs (a throwaway
    session and its tools.effective, then the session deleted) leaves the first review only the rest. Nothing of the
    owner's is read or sent, and no tokens are spent."""
    clock = clock or time.monotonic
    binary = str((config or {}).get('openclaw') or 'openclaw')

    def call(method, params):
        try:
            result = run([binary, 'gateway', 'call', method, '--json', '--timeout', '60000', '--params', json.dumps(params)],
                         capture_output=True, text=True, timeout=TIMEOUT)
            return result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False
    start = clock()
    call('sessions.create', {'key': WARM_KEY})  # already there (a warm-up cut off before its delete) is fine too
    ok = call('tools.effective', {'sessionKey': WARM_KEY})
    call('sessions.delete', {'key': WARM_KEY, 'deleteTranscript': True})
    return ok, clock() - start


def last(db):
    """The last check ({model, ok, at, error, ...}), or None before the first."""
    row = db.execute('SELECT detail FROM milestones WHERE name=?', (NAME,)).fetchone()
    try:
        found = json.loads(row[0] or 'null') if row else None
    except ValueError:
        return None
    return found if isinstance(found, dict) else None


def ask_recheck(db):
    """A review failed while the last check passed: check the AI again soon (due), so a sign-in that lapsed since shows
    as a failed check with the provider's own words (ModelCheckFailed in the error reports), and its comeback
    (recovered_at) lets the reviews go again at once. Nothing before a first check, nor when one failed already: those
    are checked again by themselves. A check is of the main model of its time; another main model is checked anew (due)."""
    from machine.store.first_look import note_model_check
    found = last(db)
    if found and found.get('ok') and not found.get('recheck') and found.get('at'):
        note_model_check(db, {**found, 'recheck': True})


def answering(db):
    """The AI answered its last check and nothing failed since that asks for another (ask_recheck)."""
    found = last(db)
    return bool(found and found.get('ok') and not found.get('recheck'))


def answered_since(db, at):
    """The AI answered a check made at or after `at` (ISO text): it works, whatever failed before it."""
    found = last(db)
    return bool(found and found.get('ok') and not found.get('recheck') and str(found.get('at') or '') >= str(at or ''))


def recovered_since(db, at):
    """The AI failed its check and answered again after `at` (ISO text): a sign-in or an outage came back."""
    found = last(db)
    return bool(found and found.get('ok') and str(found.get('recovered_at') or '') > str(at or ''))


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
    if found.get('ok') and not found.get('recheck'):
        return False
    since = _seconds(found, 'at', current)
    if found.get('ok'):  # a review failed after it passed (ask_recheck): once, after SOON_SECONDS
        return since >= SOON_SECONDS
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
    if ok and found and found.get('model') == model and not found.get('ok'):
        out['recovered_at'] = now_text  # it failed, now it answers: reviews that failed meanwhile go again at once
    elif ok and found and found.get('model') == model and found.get('recovered_at'):
        out['recovered_at'] = found['recovered_at']
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

"""How much of the AI sign-in's usage limits The Machine's own background work may use (reviews, the profile, voices,
roles and organizations turns, drafts prepared ahead). One check before every such turn, so the owner's own chats and
the cards they asked for keep room:

- the 5-hour window: background work pauses at SHORT_PAUSE percent (the first look and its first draft at FIRST_PAUSE:
  that is the first magic), until the window resets;
- the weekly window: paced at a seventh a day (what a quiet day leaves over carries to the next), never past WEEK_CAP;
  reviews of new signals (`signals`) are not paced per day: they go on until WEEK_CAP, so what came in today is looked
  at today, while heavier work (a board's look through the history, drafts prepared ahead, the profile) keeps the
  daily share;
- automated follow-ups (follow_ups.py) pause first: at FOLLOW_UP_PAUSE in the 5-hour window and FOLLOW_UP_ROOM
  percent before the day's weekly share, so the owner's to-dos and the other background work keep room. A follow-up
  that reached its longest wait goes ahead like other background work (`late`);
- a usage limit a run hit (the provider said so): everything the service starts waits until the reset it named, or
  the window's own reset, instead of trying again every few minutes.

A sign-in that reports no windows (an API key, a local model) is never paused here. No model call; only labels,
percentages and reset times from `usage.status` (assistant.model_usage)."""
from __future__ import annotations

import math
import re
import time

SHORT_PAUSE = 65
FIRST_PAUSE = 85
WEEK_CAP = 90
FOLLOW_UP_PAUSE = 50
FOLLOW_UP_ROOM = 10
DAY, WEEK = 86400, 7 * 86400
LIMIT_WAIT = 1800  # a usage limit without any reset time known: look again after this long
LIMIT_WAIT_MAX = 8 * DAY  # a reset further out than a week is not believed


def provider_of(model):
    provider = str(model or '').split('/', 1)[0].lower()
    if provider in ('claude-cli', 'anthropic'):
        return 'anthropic'
    if provider in ('openai', 'openai-codex', 'codex'):
        return 'openai'
    return provider if '/' in str(model or '') else None


def for_model(usage, model):
    """Only the selected runtime's quota. An unknown selection, or one whose provider reports no usage under a name
    we recognize, keeps all of it: pacing on the wrong quota only waits, no pacing at all could use up the plan."""
    provider = provider_of(model)
    if not provider:
        return usage
    return [p for p in usage or [] if provider_of(str(p.get('provider') or '') + '/') == provider] or usage


def window_kind(label):
    """'short' for the 5-hour window, 'week' for the weekly one (OpenClaw labels them 5h and Week; 168h and 7d too)."""
    text = re.sub(r'[\s_-]+', '', str(label or '').lower())
    if text in ('week', 'weekly', '7d', '168h', '1w') or text.endswith('week'):
        return 'week'
    return 'short'


def pause(usage, now_s=None, first=False, signals=False):
    """None when a background turn may start now; else why not: {'window': '5h'|'week', 'provider', 'used', 'until',
    'threshold'} (`until` an epoch second, None when unknown; `threshold` the percent it paused at). Counted by pacing.py.
    `signals`: a review of new signals, which the weekly window holds only at WEEK_CAP (the 5-hour one as usual)."""
    now_s = time.time() if now_s is None else now_s
    for entry in usage or []:
        for w in entry.get('windows') or []:
            used, reset = w.get('used'), w.get('reset')
            if not isinstance(used, (int, float)) or (reset and reset <= now_s):
                continue  # an old reading of a window that has reset since
            found = {'provider': entry.get('provider'), 'name': entry.get('name'), 'label': w.get('label'), 'used': used}
            if window_kind(w.get('label')) == 'short':
                if used >= (FIRST_PAUSE if first else SHORT_PAUSE):
                    return {**found, 'window': '5h', 'until': reset, 'threshold': FIRST_PAUSE if first else SHORT_PAUSE}
                continue
            allowed = WEEK_CAP if first or signals else allowed_this_week(reset, now_s)
            if used >= allowed:
                day_end = None
                if reset and used < WEEK_CAP and not first and not signals:
                    start = reset - WEEK
                    day_end = start + math.ceil(max(now_s - start, 1) / DAY) * DAY
                return {**found, 'window': 'week', 'until': min(day_end or reset, reset) if reset else None, 'threshold': int(round(allowed))}
    return None


def follow_up_pause(usage, now_s=None, late=False):
    """None when an automated follow-up may be drafted now; else why not, like pause. They wait first: at
    FOLLOW_UP_PAUSE in the 5-hour window and FOLLOW_UP_ROOM percent below the day's weekly share. `late`: it reached
    its longest wait, so it only waits where any background work would."""
    found = pause(usage, now_s)
    if found or late:
        return found
    now_s = time.time() if now_s is None else now_s
    for entry in usage or []:
        for w in entry.get('windows') or []:
            used, reset = w.get('used'), w.get('reset')
            if not isinstance(used, (int, float)) or (reset and reset <= now_s):
                continue
            base = {'provider': entry.get('provider'), 'name': entry.get('name'), 'label': w.get('label'), 'used': used}
            if window_kind(w.get('label')) == 'short':
                if used >= FOLLOW_UP_PAUSE:
                    return {**base, 'window': '5h', 'until': reset, 'threshold': FOLLOW_UP_PAUSE}
            elif used >= allowed_this_week(reset, now_s) - FOLLOW_UP_ROOM:
                return {**base, 'window': 'week', 'until': reset, 'threshold': int(round(allowed_this_week(reset, now_s) - FOLLOW_UP_ROOM))}
    return None


def allowed_this_week(reset, now_s):
    """How many percent of the weekly window background work may have used by now: a seventh for each day of the week
    begun so far, at most WEEK_CAP. Without a reset time, WEEK_CAP."""
    if not reset:
        return WEEK_CAP
    days = min(7, max(1, math.ceil((now_s - (reset - WEEK)) / DAY)))
    return min(WEEK_CAP, days * 100 / 7)


def limit_until(retry_at, usage, now_s=None):
    """Until when a usage limit a run hit holds: the reset the provider named, else the latest reset of a full window
    (or of any window when none reads full yet), else LIMIT_WAIT from now."""
    now_s = time.time() if now_s is None else now_s
    if isinstance(retry_at, (int, float)) and now_s < retry_at < now_s + LIMIT_WAIT_MAX:
        return int(retry_at)
    windows = [w for p in usage or [] for w in p.get('windows') or [] if (w.get('reset') or 0) > now_s]
    full = [w['reset'] for w in windows if (w.get('used') or 0) >= 100]
    if full:
        return int(max(full))
    if windows:
        return int(min(w['reset'] for w in windows))
    return int(now_s + LIMIT_WAIT)

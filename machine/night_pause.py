"""The night pause: no review of new signals while the owner sleeps (docs/help/cards.md#check-now).

Reviews between midnight and 07:00 took about a fifth of one Machine's review tokens over a week, mostly the fixed
start each review pays (instructions, status, context) for a handful of signals, and nobody reads those to-dos before
morning: the dashboard is quiet and nothing is delivered outside the owner's hours (deliver.py, notify_step).

So in the quiet hours (timeutil.quiet_hours, 00:00 to 07:00 by default) signals keep coming in and are stored, but no
review starts (App.night_hold, App.review_step). CATCH_UP_LEAD minutes before the quiet hours end the pause ends, and
the held signals go in one review, so the to-dos are there before the morning summary (SUMMARY_LEAD before it when
it comes earlier). The review reads a chat's messages together: an earlier message that a newer one in the same batch
already shows in full is offered as a line pointing at it (Store.review_claim), so a chat that went on all night
costs little more than its last message.

It holds only the reviews of new signals. Never the first look and its first batches, a new install's first day, a
review that is running or recovering, the owner's Check now, anything the owner asked for (chat, Do it, routines at
their time), or outward safety flows: those run outside the reviews. And never while the owner uses The Machine: a
dashboard or the app in use, a message in their chat or on Telegram, a tap on a to-do. After that, reviews run as
usual until IDLE_SECONDS passed without use, and what waited is reviewed right away. The owner's own hours
(work_hours) are never night, so a Machine whose hours run through the night never pauses.

A time-sensitive title (review_wait.TIME_SENSITIVE: "urgent", "security alert", "starts in 10 min") waits too: its
to-do could not reach the owner before their hours start anyway, and the catch-up comes before that. Pure functions
here; App.night_hold reads the database."""
from __future__ import annotations

import datetime as dt

import timeutil

CATCH_UP_LEAD = 30       # minutes before the quiet hours end: the held signals are reviewed then
SUMMARY_LEAD = 60        # minutes before the morning summary, when it comes before that
IDLE_SECONDS = 3600      # after the owner last used The Machine at night, reviews run as usual this long
NEW_INSTALL_HOURS = 24   # a new install's first day never pauses: setup and the first look go on


def _minute(value):
    hour, minute = timeutil.hour_minute(value)
    return hour * 60 + minute


def window(quiet=None, summary=None, hours=None):
    """The pause as (start, length) in minutes of the local day, or None when there is none: from the start of the quiet
    hours until CATCH_UP_LEAD before they end, or SUMMARY_LEAD before the morning summary ('HH:MM') or the start of the
    owner's hours, whichever comes first."""
    start, end = quiet or timeutil.quiet_hours()
    start *= 60
    length = (end * 60 - start) % 1440 - CATCH_UP_LEAD
    for at, lead in ((summary, SUMMARY_LEAD), ((hours or {}).get('start') if hours and hours.get('start') != hours.get('end') else None, 0)):
        if at:
            offset = (_minute(at) - start) % 1440
            if offset < length + lead:
                length = offset - lead
    return (start, length) if length > 0 else None


def held_until(local, quiet=None, summary=None, hours=None):
    """When the pause `local` (an aware local time) falls in ends: the catch-up, as an aware local time. None outside
    the pause and within the owner's hours."""
    found = window(quiet, summary, hours)
    if not found or timeutil.in_hours(local, hours):
        return None
    start, length = found
    into = (local.hour * 60 + local.minute - start) % 1440
    if into >= length:
        return None
    return local.replace(second=0, microsecond=0) + dt.timedelta(minutes=length - into)


def used_lately(last_use, current):
    """The owner used The Machine within IDLE_SECONDS before `current` (both epoch seconds)."""
    return bool(last_use) and current - last_use < IDLE_SECONDS

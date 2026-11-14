"""The owner's time zone and hours, and the clock: plain functions any module may import (it imports nothing of the
app's own).

The zone and hours are the owner's (`timezone` and `work_hours` in config.json, applied by App with set_timezone and
set_work_hours; the dashboard's Work hours; `assistant hours`). The functions that read the hours take them as
`hours` and default to the owner's."""
import datetime as dt
import os
import re
from zoneinfo import ZoneInfo
from machine.owner_error import OwnerError

# Local time for quiet hours, snoozes, weekly recaps and file-name dates. Set `timezone` in
# config.json (applied by App) or ASSISTANT_TIMEZONE.
LOCAL_TZ = ZoneInfo(os.environ.get('ASSISTANT_TIMEZONE') or 'Europe/Amsterdam')


def local_tz():
    return LOCAL_TZ


def set_timezone(name):
    global LOCAL_TZ
    if name:
        LOCAL_TZ = ZoneInfo(name)


# The clock: clock() is the one place the app reads the current time, so a test (tests/pinned.py) or a run at a
# chosen moment can fix it with pin(). An architecture test keeps datetime.now() and date.today() out of other code.
PINNED = None  # the moment pin() fixed (an aware datetime), or None for the real clock
PIN_NEEDS_A_ZONE = 'pin() takes a datetime with a time zone, so the moment is not ambiguous'  # for developers, not shown


def clock(tz=dt.timezone.utc):
    """The current time, aware in `tz` (UTC by default); `tz=None` gives naive local time, as datetime.now() does."""
    if PINNED is None:
        return dt.datetime.now(tz)
    return PINNED.astimezone(tz).replace(tzinfo=None) if tz is None else PINNED.astimezone(tz)


def today():
    """The current local date, as date.today() gives it."""
    return dt.date.today() if PINNED is None else clock(None).date()


def pin(when):
    """Fix the clock at `when` (an aware datetime, or ISO text with an offset); None lets it run again."""
    global PINNED
    if isinstance(when, str):
        when = dt.datetime.fromisoformat(when.replace('Z', '+00:00'))
    if when is not None and (not isinstance(when, dt.datetime) or when.utcoffset() is None):
        raise ValueError(PIN_NEEDS_A_ZONE)
    PINNED = when


def now():
    """The current time in UTC, as ISO text (what the database stores)."""
    return clock().isoformat()


# The owner's hours (`work_hours` in config.json, the dashboard's Work hours, `assistant hours`):
# `days` are ISO weekdays (1 = Monday) when work cards go out and snoozed work and returning
# threads come back; nothing is sent outside `start`–`end` (it may wrap past midnight); `morning`
# is when "Tomorrow", "3 days" and "1 week" land, as the hours start; the morning digest (digest_at, 08:30) comes after
# it (digest_floor). Missing keys keep these defaults.
# WORK_HOURS is one dict for the whole run, changed in place by set_work_hours, so a module that imported it sees the
# owner's current hours.
WORK_HOURS_DEFAULT = {'days': [1, 2, 3, 4, 5], 'start': '08:00', 'end': '23:00', 'morning': '08:00'}
WORK_HOURS = dict(WORK_HOURS_DEFAULT)
DAY_NAMES = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def hour_minute(value, what='time'):
    """'8:30' or '08:30' as (8, 30); anything else is a ValueError naming `what`."""
    match = re.fullmatch(r'\s*([01]?\d|2[0-3]):([0-5]\d)\s*', str(value or ''))
    if not match:
        raise OwnerError(f'{what} must be a time like 09:00')
    return int(match[1]), int(match[2])


def work_hours(value=None):
    """`work_hours` checked and completed with the defaults; a ValueError says what is wrong."""
    if value is None:
        value = {}
    if not isinstance(value, dict):
        raise ValueError('work_hours must be an object with days, start, end and morning')
    days = value.get('days', WORK_HOURS_DEFAULT['days'])
    if isinstance(days, str):  # 'mon-fri', 'sun-thu' or 'mon,wed,fri'
        listed = []
        for part in (p for p in re.split(r'[\s,]+', days.lower()) if p):
            first, _, last = part.partition('-')
            if last and first[:3] in DAY_NAMES and last[:3] in DAY_NAMES:
                start, stop = DAY_NAMES.index(first[:3]), DAY_NAMES.index(last[:3])
                listed += [DAY_NAMES[(start + i) % 7] for i in range((stop - start) % 7 + 1)]
            else:
                listed.append(part)
        days = listed
    picked = set()
    for day in days if isinstance(days, list) else [None]:
        name = str(day).strip().lower()[:3]
        if isinstance(day, int) and not isinstance(day, bool) and 1 <= day <= 7:
            picked.add(day)
        elif name in DAY_NAMES:
            picked.add(DAY_NAMES.index(name) + 1)
        else:
            raise ValueError('work days are weekday numbers 1 (Monday) to 7 (Sunday) or names like mon')
    if not picked:
        raise OwnerError('Pick at least one work day')
    hours = {'days': sorted(picked)}
    for key, what in (('start', 'The start'), ('end', 'The end'), ('morning', 'The morning time')):
        hours[key] = '%02d:%02d' % hour_minute(value.get(key, WORK_HOURS_DEFAULT[key]), what)
    return hours


def set_work_hours(value):
    checked = work_hours(value)
    WORK_HOURS.clear()
    WORK_HOURS.update(checked)


DIGEST_AFTER_SNOOZES = 5  # minutes: the morning digest comes at least this long after the morning's snoozes


def digest_floor(digest_at, hours=None):
    """The morning digest time ('HH:MM') that follows the snooze time (`morning`): never before DIGEST_AFTER_SNOOZES
    minutes after it, so the to-dos back that morning are in the digest. A later digest keeps its time. When that
    minimum falls past midnight or outside the hours, the digest keeps its own time. The dashboard's Work hours do the
    same (settings-general.js, digestFloor)."""
    hours = hours or WORK_HOURS
    digest = '%02d:%02d' % hour_minute(digest_at)
    hour, minute = hour_minute(hours['morning'])
    after = hour * 60 + minute + DIGEST_AFTER_SNOOZES
    if after >= 24 * 60:
        return digest
    floor = '%02d:%02d' % divmod(after, 60)
    if floor <= digest or not in_hours(dt.datetime(2000, 1, 1, *divmod(after, 60)), hours):
        return digest
    return floor


def is_work_day(day, hours=None):
    """A date or datetime (in local time) on one of the owner's work days."""
    return day.isoweekday() in (hours or WORK_HOURS)['days']


def next_work_day(local, hours=None):
    """`local` itself when it is on a work day, else the same time on the next one."""
    for _ in range(7):
        if is_work_day(local, hours):
            return local
        local += dt.timedelta(days=1)
    return local


def in_hours(local, hours=None):
    """Within the owner's hours (start–end, local time), when cards and reminders may go out."""
    hours = hours or WORK_HOURS
    start, end, minute = hour_minute(hours['start']), hour_minute(hours['end']), (local.hour, local.minute)
    if start == end:
        return True
    return start <= minute < end if start < end else minute >= start or minute < end


# The quiet hours: the local hours ("from-to" in ASSISTANT_QUIET_HOURS, 00:00 to 07:00 by default) when the owner's
# chats and to-dos rest. The nightly update puts a changed bridge in only then (installer.quiet_hours reads the same
# setting: the installer runs before a time zone is checked, so it keeps its own copy), and the reviews of new signals
# pause in them (machine/night_pause.py).
QUIET_HOURS = (0, 7)


def quiet_hours():
    """The quiet hours as (start, end) local hours; end may be past midnight (22-6)."""
    try:
        start, end = (int(part) % 24 for part in os.environ.get('ASSISTANT_QUIET_HOURS', '').split('-'))
    except ValueError:
        return QUIET_HOURS
    return start, end


def morning_label(hours=None):
    hour, minute = hour_minute((hours or WORK_HOURS)['morning'])
    return f'{hour}:{minute:02d}'


def local_day(value, metadata=None, tz=None):
    """The owner's calendar day (a date) of a stored time: ISO text (UTC in the database) or a datetime, in their time
    zone (`tz`, default theirs), so 00:30 in Brussels is that day, not the one before in UTC. An all-day calendar event
    (metadata with all_day and start.date, as connectors store it) is on its own date whatever the zone: its stored
    start is midnight in the calendar's zone, which is the day before in UTC east of it. A bare date stays that date.
    None when there is no time."""
    if isinstance(metadata, dict) and metadata.get('all_day'):
        day = (metadata.get('start') or {}).get('date') if isinstance(metadata.get('start'), dict) else None
        if isinstance(day, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
            return dt.date.fromisoformat(day)
    if isinstance(value, dt.datetime):
        stamp = value
    elif isinstance(value, dt.date):
        return value
    else:
        text = str(value or '').strip()
        if not text:
            return None
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', text):
            return dt.date.fromisoformat(text)
        try:
            stamp = dt.datetime.fromisoformat(text.replace('Z', '+00:00'))
        except ValueError:
            return dt.date.fromisoformat(text[:10])
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=dt.timezone.utc)
    return stamp.astimezone(tz or LOCAL_TZ).date()


def local_day_text(value, metadata=None, tz=None):
    """local_day as ISO text ('2026-12-05'), or '' without a time."""
    day = local_day(value, metadata, tz)
    return day.isoformat() if day else ''

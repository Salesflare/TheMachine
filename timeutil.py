"""The owner's time zone and hours, and the clock: plain functions any module may import (it imports nothing of the
app's own).

The zone and hours are the owner's (`timezone` and `work_hours` in config.json, applied by App with set_timezone and
set_work_hours; the dashboard's Work hours; `assistant hours`). The functions that read the hours take them as
`hours` and default to the owner's."""
import datetime as dt
import os
import re
from zoneinfo import ZoneInfo

# Local time for quiet hours, snoozes, weekly recaps and file-name dates. Set `timezone` in
# config.json (applied by App) or ASSISTANT_TIMEZONE.
LOCAL_TZ = ZoneInfo(os.environ.get('ASSISTANT_TIMEZONE') or 'Europe/Amsterdam')


def local_tz():
    return LOCAL_TZ


def set_timezone(name):
    global LOCAL_TZ
    if name:
        LOCAL_TZ = ZoneInfo(name)


def now():
    """The current time in UTC, as ISO text (what the database stores)."""
    return dt.datetime.now(dt.timezone.utc).isoformat()


# The owner's hours (`work_hours` in config.json, the dashboard's Work hours, `assistant hours`):
# `days` are ISO weekdays (1 = Monday) when work cards go out and snoozed work and returning
# threads come back; nothing is sent outside `start`–`end` (it may wrap past midnight); `morning`
# is when "Tomorrow", "3 days" and "1 week" land. Missing keys keep these defaults.
# WORK_HOURS is one dict for the whole run, changed in place by set_work_hours, so a module that imported it sees the
# owner's current hours.
WORK_HOURS_DEFAULT = {'days': [1, 2, 3, 4, 5], 'start': '08:00', 'end': '23:00', 'morning': '09:00'}
WORK_HOURS = dict(WORK_HOURS_DEFAULT)
DAY_NAMES = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def clock(value, what='time'):
    """'8:30' or '08:30' as (8, 30); anything else is a ValueError naming `what`."""
    match = re.fullmatch(r'\s*([01]?\d|2[0-3]):([0-5]\d)\s*', str(value or ''))
    if not match:
        raise ValueError(f'{what} must be a time like 09:00')
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
        raise ValueError('Pick at least one work day')
    hours = {'days': sorted(picked)}
    for key, what in (('start', 'The start'), ('end', 'The end'), ('morning', 'The morning time')):
        hours[key] = '%02d:%02d' % clock(value.get(key, WORK_HOURS_DEFAULT[key]), what)
    return hours


def set_work_hours(value):
    checked = work_hours(value)
    WORK_HOURS.clear()
    WORK_HOURS.update(checked)


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
    start, end, minute = clock(hours['start']), clock(hours['end']), (local.hour, local.minute)
    if start == end:
        return True
    return start <= minute < end if start < end else minute >= start or minute < end


def morning_label(hours=None):
    hour, minute = clock((hours or WORK_HOURS)['morning'])
    return f'{hour}:{minute:02d}'

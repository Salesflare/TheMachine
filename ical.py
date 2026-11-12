"""iCalendar (RFC 5545) events as Google Calendar ones, for the calendars that hand out .ics data: CalDAV servers
(caldav_calendar.py: iCloud, Fastmail, Nextcloud, Zoho) and calendar links (ics_feed.py: Proton Calendar, published
Outlook and iCloud calendars, school and sports feeds).

Python only, nothing to install. It reads VEVENTs with their time zones (an IANA name, a Windows one, or the feed's own
VTIMEZONE offset), and expands a recurring event into its occurrences in a window, as Google's singleEvents does:
RRULE (DAILY, WEEKLY, MONTHLY, YEARLY with INTERVAL, COUNT, UNTIL, BYDAY, BYMONTHDAY, BYMONTH, BYSETPOS), RDATE,
EXDATE, and an occurrence changed or cancelled on its own (RECURRENCE-ID). A rule it can't follow (by hour, by week
number) gives its first occurrence only. Each event comes out in the shape machine/sources/calendar.calendar_event reads.

The text comes from the network: it is only ever parsed as lines, nothing in it is fetched or run, and every loop has
a cap (MAX_EVENTS, MAX_OCCURRENCES, MAX_PERIODS)."""
import datetime as dt
import hashlib
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

MAX_EVENTS = 20000       # VEVENTs read from one text
MAX_OCCURRENCES = 5000   # occurrences one series gives in a window
MAX_PERIODS = 40000      # days, weeks, months or years a rule steps through
MAX_ITEMS = 10000        # events one window gives
DAYS = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')
PARTSTAT = {'ACCEPTED': 'accepted', 'DECLINED': 'declined', 'TENTATIVE': 'tentative', 'NEEDS-ACTION': 'needsAction',
            'DELEGATED': 'needsAction'}
# Windows time zone names some servers (Exchange, Outlook's published calendars) put in TZID: the usual ones
WINDOWS_ZONES = {
    'UTC': 'UTC', 'GMT Standard Time': 'Europe/London', 'Greenwich Standard Time': 'Atlantic/Reykjavik',
    'W. Europe Standard Time': 'Europe/Berlin', 'Romance Standard Time': 'Europe/Paris',
    'Central Europe Standard Time': 'Europe/Budapest', 'Central European Standard Time': 'Europe/Warsaw',
    'E. Europe Standard Time': 'Europe/Chisinau', 'FLE Standard Time': 'Europe/Kiev', 'GTB Standard Time': 'Europe/Bucharest',
    'Russian Standard Time': 'Europe/Moscow', 'Turkey Standard Time': 'Europe/Istanbul', 'Israel Standard Time': 'Asia/Jerusalem',
    'South Africa Standard Time': 'Africa/Johannesburg', 'Arabian Standard Time': 'Asia/Dubai', 'India Standard Time': 'Asia/Kolkata',
    'China Standard Time': 'Asia/Shanghai', 'Singapore Standard Time': 'Asia/Singapore', 'Tokyo Standard Time': 'Asia/Tokyo',
    'Korea Standard Time': 'Asia/Seoul', 'AUS Eastern Standard Time': 'Australia/Sydney', 'New Zealand Standard Time': 'Pacific/Auckland',
    'Eastern Standard Time': 'America/New_York', 'Central Standard Time': 'America/Chicago',
    'Mountain Standard Time': 'America/Denver', 'US Mountain Standard Time': 'America/Phoenix',
    'Pacific Standard Time': 'America/Los_Angeles', 'Alaskan Standard Time': 'America/Anchorage',
    'Hawaiian Standard Time': 'Pacific/Honolulu', 'Atlantic Standard Time': 'America/Halifax',
    'E. South America Standard Time': 'America/Sao_Paulo', 'Argentina Standard Time': 'America/Argentina/Buenos_Aires',
    'SA Pacific Standard Time': 'America/Bogota', 'Central Standard Time (Mexico)': 'America/Mexico_City',
}


# ------------------------------------------------------------------------------------------------- reading the text

def _unescape(value):
    return re.sub(r'\\([\\;,nN])', lambda m: '\n' if m[1] in 'nN' else m[1], value)


def _params(text):
    """'TZID=Europe/Brussels;VALUE=DATE' (quotes kept apart) -> {'TZID': ..., 'VALUE': ...}."""
    out = {}
    for match in re.finditer(r';([A-Za-z0-9-]+)=("[^"]*"|[^;:]*)', text):
        out[match[1].upper()] = match[2].strip('"')
    return out


def _line(line):
    """(NAME, {params}, value) of one unfolded content line; None for one that isn't."""
    match = re.match(r'([A-Za-z0-9-]+)((?:;[A-Za-z0-9-]+=(?:"[^"]*"|[^;:"]*))*):(.*)', line)
    if not match:
        return None
    return match[1].upper(), _params(match[2]), match[3]


def components(text):
    """The text's components as nested dicts: {'name', 'props': [(NAME, params, value)], 'children': [...]}."""
    text = str(text or '').replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n[ \t]', '', text)  # unfold
    root = {'name': 'ROOT', 'props': [], 'children': []}
    stack, events = [root], 0
    for raw in text.split('\n'):
        parsed = _line(raw.strip('﻿'))
        if not parsed:
            continue
        name, params, value = parsed
        if name == 'BEGIN':
            if value.upper() == 'VEVENT':
                events += 1
                if events > MAX_EVENTS:
                    break
            node = {'name': value.strip().upper(), 'props': [], 'children': []}
            stack[-1]['children'].append(node)
            if len(stack) < 8:
                stack.append(node)
        elif name == 'END':
            if len(stack) > 1 and stack[-1]['name'] == value.strip().upper():
                stack.pop()
        else:
            stack[-1]['props'].append((name, params, value))
    return root


def walk(node, name):
    for child in node['children']:
        if child['name'] == name:
            yield child
        yield from walk(child, name)


def prop(component, name):
    return next(((params, value) for n, params, value in component['props'] if n == name), (None, None))


def props(component, name):
    return [(params, value) for n, params, value in component['props'] if n == name]


def text_of(component, name):
    value = prop(component, name)[1]
    return _unescape(value).strip() if value is not None else ''


# ------------------------------------------------------------------------------------------------- time zones

class _Fixed(dt.tzinfo):
    """A feed's own VTIMEZONE that names no known zone: its standard offset."""
    def __init__(self, minutes, name):
        self._offset, self._name = dt.timedelta(minutes=minutes), name

    def utcoffset(self, _when):
        return self._offset

    def dst(self, _when):
        return dt.timedelta(0)

    def tzname(self, _when):
        return self._name


def _offset_minutes(text):
    match = re.fullmatch(r'([+-])(\d\d)(\d\d)(\d\d)?', str(text or '').strip())
    if not match:
        return None
    minutes = int(match[2]) * 60 + int(match[3])
    return -minutes if match[1] == '-' else minutes


def zone_named(name, own=None):
    """A tzinfo for a TZID: an IANA name (also behind a /mozilla.org/... style prefix), a Windows name, or the text's
    own VTIMEZONE (own: {tzid: tzinfo}); None when nothing fits."""
    name = str(name or '').strip().strip('"')
    if not name:
        return None
    tail = re.search(r'[A-Z][A-Za-z]+/[A-Za-z_+-]+(?:/[A-Za-z_+-]+)?$', name)  # /mozilla.org/20050126_1/Europe/Brussels
    for candidate in (name, WINDOWS_ZONES.get(name), tail[0] if tail else None):
        if candidate and re.fullmatch(r'[A-Za-z0-9_+./-]+', candidate) and '..' not in candidate:
            try:
                return ZoneInfo(candidate)
            except (ZoneInfoNotFoundError, ValueError):
                continue
    return (own or {}).get(name)


def own_zones(root):
    """{tzid: tzinfo} for the text's VTIMEZONEs: a known zone by its name or X-LIC-LOCATION, else its standard offset."""
    found = {}
    for tz in walk(root, 'VTIMEZONE'):
        tzid = text_of(tz, 'TZID')
        if not tzid:
            continue
        zone = zone_named(tzid) or zone_named(text_of(tz, 'X-LIC-LOCATION'))
        if zone is None:
            standard = next(walk(tz, 'STANDARD'), None) or next(iter(tz['children']), None)
            minutes = _offset_minutes(text_of(standard, 'TZOFFSETTO')) if standard else None
            zone = _Fixed(minutes, tzid[:40]) if minutes is not None else None
        if zone is not None:
            found[tzid] = zone
    return found


def parse_when(params, value, zones, default):
    """A DTSTART-like value: a date (all day) or an aware datetime. Floating times are in the calendar's own zone."""
    value = str(value or '').strip()
    params = params or {}
    if params.get('VALUE', '').upper() == 'DATE' or re.fullmatch(r'\d{8}', value):
        return dt.date(int(value[:4]), int(value[4:6]), int(value[6:8]))
    match = re.fullmatch(r'(\d{4})(\d\d)(\d\d)T(\d\d)(\d\d)(\d\d)?(Z?)', value)
    if not match:
        raise ValueError('ical_time')
    stamp = dt.datetime(*(int(match[i] or 0) for i in range(1, 7)))
    if match[7]:
        return stamp.replace(tzinfo=dt.timezone.utc)
    return stamp.replace(tzinfo=zone_named(params.get('TZID'), zones) or default)


def parse_duration(text):
    match = re.fullmatch(r'([+-])?P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?', str(text or '').strip())
    if not match or str(text).strip() in ('P', 'PT', '+P', '-P'):
        return None
    weeks, days, hours, minutes, seconds = (int(match[i] or 0) for i in range(2, 7))
    span = dt.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return -span if match[1] == '-' else span


# ------------------------------------------------------------------------------------------------- recurrence

def parse_rule(text):
    rule = {}
    for part in str(text or '').split(';'):
        key, _, value = part.partition('=')
        if key and value:
            rule[key.strip().upper()] = value.strip().upper()
    return rule


def _ints(text):
    out = []
    for part in str(text or '').split(','):
        if re.fullmatch(r'[+-]?\d{1,3}', part.strip()):
            out.append(int(part))
    return out


def _bydays(text):
    """[(ordinal or None, weekday 0-6)] of a BYDAY list."""
    out = []
    for part in str(text or '').split(','):
        match = re.fullmatch(r'([+-]?\d{1,2})?(MO|TU|WE|TH|FR|SA|SU)', part.strip())
        if match:
            out.append((int(match[1]) if match[1] else None, DAYS.index(match[2])))
    return out


def _month_days(year, month):
    first = dt.date(year, month, 1)
    nxt = dt.date(year + (month == 12), month % 12 + 1, 1)
    return [first + dt.timedelta(days=i) for i in range((nxt - first).days)]


def _weekday_pick(days, bydays):
    """The days among `days` (one month or year, in order) that a BYDAY list picks, ordinals counted within them."""
    out = set()
    for ordinal, weekday in bydays:
        matching = [d for d in days if d.weekday() == weekday]
        if ordinal is None:
            out.update(matching)
        elif 0 < ordinal <= len(matching):
            out.add(matching[ordinal - 1])
        elif 0 < -ordinal <= len(matching):
            out.add(matching[ordinal])
    return out


def _monthday_pick(days, monthdays):
    out = set()
    for n in monthdays:
        if 0 < n <= len(days):
            out.add(days[n - 1])
        elif 0 < -n <= len(days):
            out.add(days[n])
    return out


def _add_months(year, month, count):
    total = year * 12 + month - 1 + count
    return total // 12, total % 12 + 1


def rule_dates(start, rule, until_day):
    """The dates a rule gives, in order, from the start date's period on (each a date), never past until_day.
    None when the rule is one this doesn't follow."""
    freq = rule.get('FREQ')
    if freq not in ('DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY') or any(k in rule for k in ('BYWEEKNO', 'BYYEARDAY', 'BYHOUR', 'BYMINUTE', 'BYSECOND')):
        return None
    try:
        interval = max(1, int(rule.get('INTERVAL') or 1))
    except ValueError:
        interval = 1
    bydays, monthdays, months = _bydays(rule.get('BYDAY')), _ints(rule.get('BYMONTHDAY')), _ints(rule.get('BYMONTH'))
    setpos = _ints(rule.get('BYSETPOS'))
    for step in range(MAX_PERIODS):
        if freq == 'DAILY':
            day = start + dt.timedelta(days=step * interval)
            if day > until_day:
                return
            candidates = [day]
            if bydays:
                candidates = [d for d in candidates if d.weekday() in {w for _, w in bydays}]
            if monthdays:
                candidates = [d for d in candidates if d in _monthday_pick(_month_days(d.year, d.month), monthdays)]
        elif freq == 'WEEKLY':
            monday = start - dt.timedelta(days=start.weekday()) + dt.timedelta(weeks=step * interval)
            if monday > until_day:
                return
            weekdays = sorted({w for _, w in bydays}) or [start.weekday()]
            candidates = [monday + dt.timedelta(days=w) for w in weekdays]
        elif freq == 'MONTHLY':
            year, month = _add_months(start.year, start.month, step * interval)
            if dt.date(year, month, 1) > until_day:
                return
            days = _month_days(year, month)
            if bydays:
                picked = _weekday_pick(days, bydays)
                candidates = sorted(picked & _monthday_pick(days, monthdays) if monthdays else picked)
            else:
                candidates = sorted(_monthday_pick(days, monthdays or [start.day]))
        else:
            year = start.year + step * interval
            if dt.date(year, 1, 1) > until_day or year > 9000:
                return
            candidates = []
            for month in months or [start.month]:
                if not 1 <= month <= 12:
                    continue
                days = _month_days(year, month)
                if bydays and (months or monthdays):
                    picked = _weekday_pick(days, bydays)
                    candidates += sorted(picked & _monthday_pick(days, monthdays) if monthdays else picked)
                elif monthdays:
                    candidates += sorted(_monthday_pick(days, monthdays))
                elif bydays:
                    continue
                elif start.day <= len(days):
                    candidates.append(days[start.day - 1])
            if bydays and not (months or monthdays):
                year_days = [d for m in range(1, 13) for d in _month_days(year, m)]
                candidates = sorted(_weekday_pick(year_days, bydays))
        if months and freq != 'YEARLY':
            candidates = [d for d in candidates if d.month in months]
        candidates = sorted(set(candidates))
        if setpos:
            candidates = sorted({candidates[p - 1] if p > 0 else candidates[p] for p in setpos
                                 if candidates and (0 < p <= len(candidates) or 0 < -p <= len(candidates))})
        yield from candidates


def occurrences(start, rule_text, window_end, exdates=(), rdates=()):
    """The starts of a series (date or aware datetime, like start), in order, up to window_end (UTC datetime):
    the rule's, RDATEs added, EXDATEs taken out. Each start keeps the series' wall-clock time in its zone."""
    all_day = not isinstance(start, dt.datetime)
    rule = parse_rule(rule_text) if rule_text else None
    zone = None if all_day else start.tzinfo
    end_day = (window_end.astimezone(zone).date() if zone else window_end.date()) + dt.timedelta(days=1)
    until, count = None, None
    if rule:
        if rule.get('UNTIL'):
            try:
                until = parse_when({}, rule['UNTIL'], {}, zone or dt.timezone.utc)
            except ValueError:
                until = None
        try:
            count = int(rule['COUNT']) if rule.get('COUNT') else None
        except ValueError:
            count = None
    excluded = {_key(x) for x in exdates}
    found = []
    first_day = start if all_day else start.replace(tzinfo=None).date()
    dates = rule_dates(first_day, rule, end_day) if rule else None
    if dates is None:
        dates = iter([first_day])
    given = 0
    for day in dates:
        moment = day if all_day else dt.datetime.combine(day, start.timetz().replace(tzinfo=None)).replace(tzinfo=zone)
        if (moment < start) if not all_day else (day < start):
            continue
        if until is not None and _past(moment, until):
            break
        given += 1
        if count is not None and given > count:
            break
        if _key(moment) not in excluded:
            found.append(moment)
        if len(found) >= MAX_OCCURRENCES or _utc(moment) > window_end:
            break
    for extra in rdates:
        if type(extra) is type(start) and _key(extra) not in excluded and _key(extra) not in {_key(f) for f in found}:
            found.append(extra)
    return sorted(found, key=_utc)


def _utc(when):
    if isinstance(when, dt.datetime):
        return when.astimezone(dt.timezone.utc)
    return dt.datetime.combine(when, dt.time(), dt.timezone.utc)


def _key(when):
    """What makes two starts the same occurrence: the moment (UTC) or the date."""
    return _utc(when).strftime('%Y%m%dT%H%M%SZ') if isinstance(when, dt.datetime) else when.strftime('%Y%m%d')


def _past(moment, until):
    if isinstance(until, dt.datetime):
        return _utc(moment) > until.astimezone(dt.timezone.utc) if isinstance(moment, dt.datetime) else moment > until.date()
    return (moment.date() if isinstance(moment, dt.datetime) else moment) > until


# ------------------------------------------------------------------------------------------------- Google's shape

def _address(value):
    value = str(value or '').strip()
    return value[7:].strip().lower() if value.lower().startswith('mailto:') else (value.lower() if '@' in value else '')


def _when(value):
    if isinstance(value, dt.datetime):
        return {'dateTime': value.astimezone(dt.timezone.utc).isoformat()}
    return {'date': value.isoformat()}


def event_id(uid, scope=''):
    """A short id from the event's UID (and the calendar it is in): no text from the event itself."""
    return 'ical' + hashlib.sha256(f'{scope}\x00{uid}'.encode()).hexdigest()[:24]


def _base(event, zones, default, owner):
    """What every occurrence of a VEVENT shares, in Google's shape."""
    params, value = prop(event, 'ORGANIZER')
    organizer = {'email': _address(value), 'displayName': _unescape((params or {}).get('CN', '')).strip()} if value else {}
    if organizer.get('email') and organizer['email'] in owner:
        organizer['self'] = True
    attendees = []
    for params, value in props(event, 'ATTENDEE')[:500]:
        email = _address(value)
        if not email:
            continue
        person = {'email': email, 'displayName': _unescape(params.get('CN', '')).strip(),
                  'responseStatus': PARTSTAT.get(params.get('PARTSTAT', '').upper(), 'needsAction')}
        if email in owner:
            person['self'] = True
        if params.get('CUTYPE', '').upper() in ('ROOM', 'RESOURCE'):
            person['resource'] = True
        attendees.append(person)
    updated = None
    for name in ('LAST-MODIFIED', 'DTSTAMP'):
        try:
            stamp = parse_when({}, prop(event, name)[1], zones, dt.timezone.utc) if prop(event, name)[1] else None
        except ValueError:
            stamp = None
        if isinstance(stamp, dt.datetime):
            updated = stamp.astimezone(dt.timezone.utc).isoformat()
            break
    item = {'summary': text_of(event, 'SUMMARY') or '(untitled event)', 'description': text_of(event, 'DESCRIPTION')[:40000],
            'location': text_of(event, 'LOCATION') or None, 'organizer': organizer, 'attendees': attendees,
            'status': 'cancelled' if text_of(event, 'STATUS').upper() == 'CANCELLED' else 'confirmed', 'updated': updated,
            'iCalUID': text_of(event, 'UID')[:500] or None}
    if text_of(event, 'TRANSP').upper() == 'TRANSPARENT':
        item['transparency'] = 'transparent'
    return item


def _times(event, zones, default):
    """(start, end) of a VEVENT: DTEND, else DTSTART plus DURATION, else a day (all day) or nothing (a moment)."""
    params, value = prop(event, 'DTSTART')
    start = parse_when(params, value, zones, default)
    params, value = prop(event, 'DTEND')
    end = parse_when(params, value, zones, default) if value else None
    if end is None:
        span = parse_duration(text_of(event, 'DURATION'))
        end = start + span if span is not None else (start + dt.timedelta(days=1) if not isinstance(start, dt.datetime) else start)
    if type(end) is not type(start):
        end = end.date() if isinstance(end, dt.datetime) else dt.datetime.combine(end, dt.time(), start.tzinfo)
    return start, max(end, start)


def _date_list(entries, zones, default):
    out = []
    for params, value in entries:
        for part in str(value or '').split(','):
            try:
                out.append(parse_when(params, part.split('/')[0], zones, default))
            except ValueError:
                continue
    return out


def window_items(texts, time_min, time_max, owner=(), default_zone=None, scope=''):
    """Every event (each occurrence of a recurring one) in the texts that overlaps [time_min, time_max), in Google's
    shape, plus how many it couldn't read. texts: iCalendar documents (one per CalDAV object, or one whole feed).
    time_min, time_max: aware datetimes. owner: the owner's addresses, for 'self'. scope: what tells calendars apart
    in the ids (the CalDAV collection)."""
    owner = {str(e).lower() for e in owner if e}
    default = default_zone or dt.timezone.utc
    series, overrides, skipped = {}, {}, 0
    for text in texts:
        root = components(text)
        zones = own_zones(root)
        calendar_zone = zone_named(text_of(next(walk(root, 'VCALENDAR'), root), 'X-WR-TIMEZONE'), zones) or default
        for event in walk(root, 'VEVENT'):
            uid = text_of(event, 'UID') or hashlib.sha256(repr(event['props'][:6]).encode()).hexdigest()
            try:
                recurrence = prop(event, 'RECURRENCE-ID')
                if recurrence[1]:
                    when = parse_when(recurrence[0], recurrence[1], zones, calendar_zone)
                    overrides.setdefault(uid, {})[_key(when)] = (event, zones, calendar_zone, when)
                else:
                    series[uid] = (event, zones, calendar_zone)
            except (ValueError, OverflowError):
                skipped += 1
    items = []
    for uid, (event, zones, zone) in series.items():
        try:
            items += _expand(uid, event, zones, zone, overrides.pop(uid, {}), time_min, time_max, owner, scope)
        except (ValueError, OverflowError, TypeError):
            skipped += 1
        if len(items) >= MAX_ITEMS:
            break
    for uid, changed in overrides.items():  # an occurrence whose series isn't here (a CalDAV object with only it)
        for key, (event, zones, zone, when) in changed.items():
            try:
                items += _expand(uid, None, zones, zone, {key: (event, zones, zone, when)}, time_min, time_max, owner, scope)
            except (ValueError, OverflowError, TypeError):
                skipped += 1
    return items[:MAX_ITEMS], skipped


def _overlaps(start, end, time_min, time_max):
    s, e = _utc(start), _utc(end)
    return s < time_max and (e > time_min or (e == s and s >= time_min))


def _expand(uid, event, zones, zone, changed, time_min, time_max, owner, scope):
    master = event_id(uid, scope)
    out = []
    if event is not None:
        base = _base(event, zones, zone, owner)
        start, end = _times(event, zones, zone)
        rule = text_of(event, 'RRULE')
        rdates, exdates = _date_list(props(event, 'RDATE'), zones, zone), _date_list(props(event, 'EXDATE'), zones, zone)
        if not rule and not rdates and not changed:  # a single event
            return [{**base, 'id': master, 'start': _when(start), 'end': _when(end)}] if _overlaps(start, end, time_min, time_max) else []
        span = end - start
        for moment in occurrences(start, rule, time_max, exdates, rdates):
            key = _key(moment)
            if key not in changed and _overlaps(moment, moment + span, time_min, time_max):
                out.append({**base, 'id': f'{master}_{key}', 'start': _when(moment), 'end': _when(moment + span),
                            'recurringEventId': master, 'originalStartTime': _when(moment)})
    for key, (one, one_zones, one_zone, when) in changed.items():  # an occurrence changed on its own: where it is now
        base = _base(one, one_zones, one_zone, owner)
        try:
            start, end = _times(one, one_zones, one_zone)
        except ValueError:
            start, end = when, when
        if _overlaps(start, end, time_min, time_max):
            out.append({**base, 'id': f'{master}_{key}', 'start': _when(start), 'end': _when(end),
                        'recurringEventId': master, 'originalStartTime': _when(when)})
    return out

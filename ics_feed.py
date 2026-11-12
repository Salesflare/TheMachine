"""A calendar link (an .ics feed) as a calendar source: Proton Calendar's share link (it has no CalDAV or API), an
iCloud public calendar, an Outlook published calendar, a school's or a sports club's. Like caldav_calendar.py, it answers
the Google Calendar reads the app makes (calendar_call), so its events flow through the same sync, meeting prep and
Calendar view. Read-only by nature: a link can't change anything.

The link is a secret (anyone with it reads the calendar): it is kept in a credential file like a password, and never
in the config, a log, an error or the dashboard. Only https (webcal:// is https), verified TLS.

Polite polling: at most once per POLL_SECONDS, with If-None-Match and If-Modified-Since, so an unchanged feed costs a
304. A changed one answers 410, Google's word for an expired sync token, so the sync reads its window again whole
(machine/sources/calendar.sync_calendar). Recurring events are expanded here (ical.py)."""
import hashlib
import time

import caldav_calendar
from caldav_calendar import CalendarError
import ical
from timeutil import local_tz

POLL_SECONDS = 900  # a feed is asked at most this often; Proton says its links take hours to update anyway
_seen = {}  # account id -> {'at': monotonic time of the last ask, 'etag', 'modified', 'text'} (this process only)


def link_of(config, credential, account):
    try:
        link = credential(config, account['credential'])
    except (OSError, KeyError):
        raise CalendarError('ics_link_missing', retry_after=3600) from None
    return caldav_calendar.https_url(link)


def fetch(link, known=None):
    """(changed, text, etag, modified) of the feed. known: the etag and modified time from the last answer."""
    known = known or {}
    headers = {'Accept': 'text/calendar, */*;q=0.5'}
    if known.get('etag'):
        headers['If-None-Match'] = known['etag']
    if known.get('modified'):
        headers['If-Modified-Since'] = known['modified']
    try:
        status, answer, data = caldav_calendar.request(link, 'GET', None, headers, prefix='ics')
    except CalendarError as error:
        raise CalendarError(error.category.replace('caldav', 'ics'), error.status, error.retry_after) from None
    if status == 304:
        return False, None, known.get('etag'), known.get('modified')
    if status in (404, 410):
        raise CalendarError('ics_gone', status, retry_after=3600)  # the link was removed or changed
    if status != 200:
        raise caldav_calendar.status_error(status, 'ics')
    text = data.decode('utf-8', 'replace')
    if 'BEGIN:VCALENDAR' not in text[:4096].upper():
        raise CalendarError('ics_not_a_calendar', retry_after=3600)
    return True, text, answer.get('etag'), answer.get('last-modified')


def _marker(text):
    return 'ics:' + hashlib.sha256(text.encode()).hexdigest()


def calendar_call(config, credential, account, method, params):
    """Google Calendar's calendars.get and events.list answered from the feed."""
    seen = _seen.setdefault(account['id'], {})
    if method == 'calendars.get':
        return {'id': str(account.get('email') or '').lower(), 'timeZone': 'UTC'}
    if method != 'events.list':
        raise CalendarError('unsupported_calendar_method')
    link = link_of(config, credential, account)
    if params.get('syncToken'):
        if time.monotonic() - seen.get('at', -POLL_SECONDS) < POLL_SECONDS:
            return {'items': [], 'nextSyncToken': params['syncToken']}  # asked a moment ago
        changed, text, etag, modified = fetch(link, seen)
        seen.update(at=time.monotonic(), etag=etag, modified=modified)
        if changed:
            seen['text'] = text
            if _marker(text) != params['syncToken']:
                raise CalendarError('ics', 410)  # changed: the window is read again whole
        return {'items': [], 'nextSyncToken': params['syncToken']}
    text = seen.get('text') if params.get('pageToken') or time.monotonic() - seen.get('at', -POLL_SECONDS) < 60 else None
    if text is None:
        _changed, text, etag, modified = fetch(link)
        seen.update(at=time.monotonic(), etag=etag, modified=modified, text=text)
    owner = caldav_calendar.owner_addresses(account)

    def read_slice(start, end, _first):
        return ical.window_items([text], start, end, owner, local_tz())
    return caldav_calendar.page_of(params, read_slice, lambda: _marker(text))


def check(link):
    """The feed answers and is a calendar, before anything is saved: how many events it has."""
    _changed, text, _etag, _modified = fetch(caldav_calendar.https_url(link))
    return text.upper().count('BEGIN:VEVENT')

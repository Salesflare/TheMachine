"""Any CalDAV calendar (iCloud, Fastmail, Nextcloud, Zoho, Yahoo, a company's own server) as a calendar source. Like
ms_graph.py does for Outlook, it answers the Google Calendar reads the app makes (calendar_call: calendars.get and
events.list), so its meetings flow through the same sync, history, meeting prep and Calendar view.

Python only, nothing to install. Reads only: PROPFIND and REPORT, never a PUT or DELETE. Every calendar of the account
that holds events is read, or only the one named in Server settings (calendar_name). Recurring events are expanded
here (ical.py), within the window asked for.

Incremental: each calendar's sync-token (RFC 6578), else its ctag, else its objects' etags, make one change marker. An
unchanged marker answers "nothing new" with one PROPFIND; a changed one answers 410, Google's word for an expired sync
token, so the sync reads its window again whole and removes what is gone (machine/sources/calendar.sync_calendar).

The password comes from the account's credential file (sources.credential) and is only ever sent to the server, over
verified TLS (https only, also after a redirect, which may only stay within the server's own domain). Errors are fixed,
content-free labels (CalendarError): what the server said is matched, never kept or logged."""
import base64
import datetime as dt
import hashlib
import http.client
import re
import socket
import ssl
import time
import urllib.parse
import xml.etree.ElementTree as ET

import ical
from timeutil import local_tz

TIMEOUT = 30
MAX_ANSWER = 20_000_000  # bytes read from one answer
SLICE_DAYS = 92          # a window is read in slices this long, one page each
CACHE_SECONDS = 90       # the calendars read for calendars.get serve the events.list right after it
DAV, CAL, CS = 'DAV:', 'urn:ietf:params:xml:ns:caldav', 'http://calendarserver.org/ns/'
ICLOUD = 'https://caldav.icloud.com/'
# Known servers, by the address's domain: where discovery starts. Others start at the domain's /.well-known/caldav.
SERVERS = {('icloud.com', 'me.com', 'mac.com'): ICLOUD,
           ('fastmail.com', 'fastmail.fm', 'fastmail.net', 'fastmail.org', 'fastmail.to', 'fastmail.us', 'sent.com',
            'messagingengine.com'): 'https://caldav.fastmail.com/dav/',
           ('yahoo.com', 'ymail.com', 'rocketmail.com'): 'https://caldav.calendar.yahoo.com/',
           ('zoho.com', 'zohomail.com'): 'https://calendar.zoho.com/caldav/',
           ('zoho.eu', 'zohomail.eu'): 'https://calendar.zoho.eu/caldav/'}
_cache = {}  # account id -> (monotonic time, [calendar]) read for calendars.get


class CalendarError(Exception):
    """A content-free label, as sources.SourceError takes it: never what the server said, never a password or link."""
    def __init__(self, category, status=None, retry_after=None):
        self.category, self.status, self.retry_after = category, status, retry_after
        super().__init__(category + (f':HTTP_{status}' if status else ''))


# ------------------------------------------------------------------------------------------------- HTTP over TLS

def https_url(text):
    """A server as typed (caldav.example.com, https://example.com/dav) as an https URL; plain http is refused."""
    text = str(text or '').strip()
    if not text:
        return ''
    if text.lower().startswith('webcal://'):
        text = 'https://' + text[9:]
    if '://' not in text:
        text = 'https://' + text
    parts = urllib.parse.urlsplit(text)
    if parts.scheme.lower() != 'https' or not parts.hostname:
        raise CalendarError('calendar_plaintext_refused')
    return urllib.parse.urlunsplit(('https', parts.netloc, parts.path or '/', parts.query, ''))


def tls_context():
    """Verified TLS, as a browser does, for every server: no exception, also not on this computer."""
    return ssl.create_default_context()


def _site(host):
    return '.'.join(str(host or '').lower().split('.')[-2:])


def failure(error, prefix):
    """A CalendarError for what went wrong on the connection itself."""
    if isinstance(error, CalendarError):
        return error
    if isinstance(error, (socket.timeout, TimeoutError)):
        return CalendarError('timeout')
    if isinstance(error, (ssl.SSLError, ssl.CertificateError)):
        return CalendarError(prefix + '_tls_failed', retry_after=3600)
    if isinstance(error, (socket.gaierror, ConnectionError, OSError, http.client.HTTPException)):
        return CalendarError(prefix + '_unreachable')
    return CalendarError(prefix + '_failed')


def status_error(status, prefix, retry_after=None):
    if status in (401, 403):
        # an hour before trying again: repeated wrong passwords can lock the account at the provider
        return CalendarError(prefix + '_auth_failed', status, retry_after=3600)
    if status == 404:
        return CalendarError(prefix + '_not_found', 404, retry_after=3600)
    if status in (429, 503):
        return CalendarError(prefix + '_rate_limited', status, retry_after=retry_after or 600)
    return CalendarError(prefix, status)


def request(url, method='GET', body=None, headers=None, prefix='caldav', redirects=5):
    """(status, headers, body) of one https request, verified TLS. A redirect is followed only to https on the same
    domain (pNN-caldav.icloud.com from caldav.icloud.com), so the password never goes anywhere else."""
    headers = dict(headers or {})
    for _ in range(redirects + 1):
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != 'https' or not parts.hostname:
            raise CalendarError(prefix + '_plaintext_refused')
        try:
            connection = http.client.HTTPSConnection(parts.hostname, parts.port or 443, timeout=TIMEOUT,
                                                     context=tls_context())
            try:
                connection.request(method, (parts.path or '/') + ('?' + parts.query if parts.query else ''),
                                   body=body, headers={'User-Agent': 'TheMachine-calendar', **headers})
                reply = connection.getresponse()
                data = reply.read(MAX_ANSWER + 1)
                answer = {k.lower(): v for k, v in reply.getheaders()}
            finally:
                connection.close()
        except Exception as error:  # noqa: BLE001 - every failure becomes a label, its text never kept
            raise failure(error, prefix) from None
        if reply.status in (301, 302, 307, 308) and answer.get('location'):
            target = urllib.parse.urljoin(url, answer['location'])
            if urllib.parse.urlsplit(target).scheme != 'https' or _site(urllib.parse.urlsplit(target).hostname) != _site(parts.hostname):
                raise CalendarError(prefix + '_redirect_refused')
            url = target
            continue
        if len(data) > MAX_ANSWER:
            raise CalendarError(prefix + '_too_big')
        return reply.status, {**answer, 'url': url}, data
    raise CalendarError(prefix + '_redirect_refused')


def parse_xml(data, prefix='caldav'):
    """An XML answer from the network, read by the parser that refuses any DTD (connectors/docs.parse_xml: no entity
    expansion, no external entities)."""
    from connectors.docs import parse_xml as hardened  # noqa: PLC0415 - the one hardened XML reader
    text = data.decode('utf-8', 'replace') if isinstance(data, bytes) else str(data or '')
    if re.search(r'<!(DOCTYPE|ENTITY)', text, re.I):
        raise CalendarError(prefix + '_bad_answer')
    try:
        return hardened(text.encode('utf-8'))
    except ET.ParseError:
        raise CalendarError(prefix + '_bad_answer') from None


# ------------------------------------------------------------------------------------------------- CalDAV

def _auth(username, password):
    return 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()


def _q(ns, name):
    return '{%s}%s' % (ns, name)


def _dav(url, method, body, auth, depth='0'):
    status, headers, data = request(url, method, body.encode(), {
        'Authorization': auth, 'Depth': depth, 'Content-Type': 'application/xml; charset=utf-8', 'Accept': 'application/xml'})
    if status != 207:
        raise status_error(status, 'caldav', _retry(headers))
    return headers['url'], parse_xml(data)


def _retry(headers):
    value = str(headers.get('retry-after') or '')
    return min(int(value), 3600) if value.isdigit() else None


def _responses(tree):
    """[(href, {prop tag: element})] of a multistatus, only the props answered 200."""
    out = []
    for response in tree.iter(_q(DAV, 'response')):
        href = (response.findtext(_q(DAV, 'href')) or '').strip()
        found = {}
        for propstat in response.findall(_q(DAV, 'propstat')):
            if ' 200 ' not in ' ' + (propstat.findtext(_q(DAV, 'status')) or '') + ' ':
                continue
            for prop in propstat.findall(_q(DAV, 'prop')):
                for child in prop:
                    found[child.tag] = child
        out.append((href, found))
    return out


def _href(found, tag):
    element = found.get(tag)
    return (element.findtext(_q(DAV, 'href')) or '').strip() if element is not None else ''


PROPFIND = ('<?xml version="1.0" encoding="utf-8"?><d:propfind xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav" '
            'xmlns:cs="http://calendarserver.org/ns/"><d:prop>{}</d:prop></d:propfind>')
LIST_PROPS = '<d:resourcetype/><d:displayname/><c:supported-calendar-component-set/><cs:getctag/><d:sync-token/>'


def start_url(account):
    """Where discovery starts: the server in Server settings, else iCloud's for iCloud, a known provider's, or the
    address's own domain."""
    if account.get('caldav_url'):
        return https_url(account['caldav_url'])
    if account.get('service') == 'icloud_calendar':
        return ICLOUD
    domain = str(account.get('email') or '').rpartition('@')[2].lower()
    for domains, url in SERVERS.items():
        if domain in domains:
            return url
    return https_url(domain) if domain else ''


def discover(account, password):
    """The account's calendar home (where its calendars are), from its server: the principal, then its home.
    A server address that is a calendar home or calendar itself is taken as it is."""
    auth = _auth(account.get('username') or account.get('email') or '', password)
    start = start_url(account)
    if not start:
        raise CalendarError('caldav_not_configured')
    tries = [start]
    if urllib.parse.urlsplit(start).path in ('', '/'):
        tries.insert(0, urllib.parse.urljoin(start, '/.well-known/caldav'))
    principal, last = None, None
    for url in tries:
        try:
            at, tree = _dav(url, 'PROPFIND', PROPFIND.format('<d:current-user-principal/><c:calendar-home-set/><d:resourcetype/>'), auth)
        except CalendarError as error:
            if error.category in ('caldav_auth_failed', 'caldav_tls_failed') or url == tries[-1]:
                raise
            last = error
            continue
        for href, found in _responses(tree):
            home = _href(found, _q(CAL, 'calendar-home-set'))
            if home:
                return urllib.parse.urljoin(at, home)
            kind = found.get(_q(DAV, 'resourcetype'))
            if kind is not None and kind.find(_q(CAL, 'calendar')) is not None:
                return urllib.parse.urljoin(at, href or at)  # a calendar itself
            principal = principal or (urllib.parse.urljoin(at, _href(found, _q(DAV, 'current-user-principal'))) if _href(found, _q(DAV, 'current-user-principal')) else None)
        if principal:
            break
    if not principal:
        raise last or CalendarError('caldav_not_found', 404)
    at, tree = _dav(principal, 'PROPFIND', PROPFIND.format('<c:calendar-home-set/>'), auth)
    for _href_, found in _responses(tree):
        home = _href(found, _q(CAL, 'calendar-home-set'))
        if home:
            return urllib.parse.urljoin(at, home)
    raise CalendarError('caldav_not_found', 404)


def calendars(account, password, home=None):
    """[{href, name, marker}] of the event calendars in the home (or the one calendar the home is), with what tells a
    change: the sync-token, else the ctag, else ''. Only the one named calendar_name when it is set."""
    auth = _auth(account.get('username') or account.get('email') or '', password)
    home = home or account.get('caldav_home') or discover(account, password)
    at, tree = _dav(home, 'PROPFIND', PROPFIND.format(LIST_PROPS), auth, depth='1')
    found = []
    for href, props in _responses(tree):
        kind = props.get(_q(DAV, 'resourcetype'))
        if kind is None or kind.find(_q(CAL, 'calendar')) is None:
            continue
        comps = props.get(_q(CAL, 'supported-calendar-component-set'))
        if comps is not None and len(comps) and not any(c.get('name', '').upper() == 'VEVENT' for c in comps):
            continue  # reminders or tasks only
        marker = ''.join((props.get(t).text or '').strip() for t in (_q(DAV, 'sync-token'), _q(CS, 'getctag')) if props.get(t) is not None)[:300]
        name = ' '.join(str((props.get(_q(DAV, 'displayname')).text if props.get(_q(DAV, 'displayname')) is not None else '') or '').split())
        found.append({'href': urllib.parse.urljoin(at, href), 'name': name[:80], 'marker': marker})
    wanted = ' '.join(str(account.get('calendar_name') or '').split()).casefold()
    if wanted:
        found = [c for c in found if c['name'].casefold() == wanted]
    if not found:
        raise CalendarError('caldav_no_calendar', 404, retry_after=3600)
    return found


def _etags(account, password, href):
    """A calendar without sync-token or ctag: its objects' etags, as its change marker."""
    _at, tree = _dav(href, 'PROPFIND', PROPFIND.format('<d:getetag/>'), _auth(account.get('username') or account.get('email') or '', password), depth='1')
    return hashlib.sha256('\n'.join(sorted(f'{h} {(p.get(_q(DAV, "getetag")).text if p.get(_q(DAV, "getetag")) is not None else "")}'
                                          for h, p in _responses(tree))).encode()).hexdigest()


def marker(account, password, found):
    parts = [f"{c['href']} {c['marker'] or _etags(account, password, c['href'])}" for c in found]
    return 'caldav:' + hashlib.sha256('\n'.join(sorted(parts)).encode()).hexdigest()


def _stamp(value):
    return value.astimezone(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def window_texts(account, password, href, start, end):
    """The iCalendar objects of one calendar with an event in [start, end) (the server's time-range filter)."""
    body = ('<?xml version="1.0" encoding="utf-8"?><c:calendar-query xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">'
            '<d:prop><d:getetag/><c:calendar-data/></d:prop><c:filter><c:comp-filter name="VCALENDAR"><c:comp-filter name="VEVENT">'
            f'<c:time-range start="{_stamp(start)}" end="{_stamp(end)}"/></c:comp-filter></c:comp-filter></c:filter></c:calendar-query>')
    _at, tree = _dav(href, 'REPORT', body, _auth(account.get('username') or account.get('email') or '', password), depth='1')
    return [found[_q(CAL, 'calendar-data')].text or '' for _h, found in _responses(tree) if found.get(_q(CAL, 'calendar-data')) is not None]


def owner_addresses(account):
    return {str(v).strip().lower() for v in (account.get('email'), account.get('username')) if v and '@' in str(v)}


def _when(text):
    stamp = dt.datetime.fromisoformat(str(text).replace('Z', '+00:00'))
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=dt.timezone.utc)


def page_of(params, read_slice, marker_now, days=SLICE_DAYS):
    """One page of a window read, as Google's events.list gives it: a slice of SLICE_DAYS from the page token on, the
    next slice's start (and the marker taken on the first page) as the next page token, the marker as the sync token
    after the last. read_slice(start, end, first) -> (items, skipped)."""
    time_min, time_max = _when(params['timeMin']), _when(params['timeMax'])
    token = str(params.get('pageToken') or '')
    at, _, mark = token.partition('|')
    start = max(time_min, _when(at)) if at else time_min
    mark = mark or marker_now()
    end = min(time_max, start + dt.timedelta(days=days))
    items, skipped = read_slice(start, end, start == time_min)
    items = [i for i in items if start == time_min or _starts(i) >= start]  # one spanning two slices: given once
    out = {'items': items + [{'id': '', 'unreadable': 'calendar_invalid_event'}] * min(skipped, 50)}
    if end < time_max:
        out['nextPageToken'] = f'{end.isoformat()}|{mark}'
    else:
        out['nextSyncToken'] = mark
    return out


def _starts(item):
    when = item.get('start') or {}
    if when.get('dateTime'):
        return _when(when['dateTime'])
    return dt.datetime.combine(dt.date.fromisoformat(when['date']), dt.time(), local_tz())


def calendar_call(config, credential, account, method, params):
    """Google Calendar's calendars.get and events.list (singleEvents, sync tokens) answered over CalDAV."""
    try:
        password = credential(config, account['credential'])
    except (OSError, KeyError):
        raise CalendarError('caldav_password_missing', retry_after=3600) from None
    if method == 'calendars.get':
        _cache[account['id']] = (time.monotonic(), calendars(account, password))
        return {'id': str(account.get('email') or '').lower(), 'timeZone': 'UTC'}
    if method != 'events.list':
        raise CalendarError('unsupported_calendar_method')
    at, found = _cache.pop(account['id'], (0, None))
    if found is None or time.monotonic() - at > CACHE_SECONDS:
        found = calendars(account, password)
    if params.get('syncToken'):
        if marker(account, password, found) != params['syncToken']:
            raise CalendarError('caldav', 410)  # changed: the window is read again whole (sync_calendar)
        return {'items': [], 'nextSyncToken': params['syncToken']}
    owner = owner_addresses(account)

    def read_slice(start, end, _first):
        items, skipped = [], 0
        for one in found:
            got, missed = ical.window_items(window_texts(account, password, one['href'], start, end), start, end, owner,
                                            local_tz(), scope=urllib.parse.urlsplit(one['href']).path)
            items += got
            skipped += missed
        return items, skipped
    return page_of(params, read_slice, lambda: marker(account, password, found))


def check(account, password):
    """Sign in and find the calendars before anything is saved: (calendar home, [calendar names])."""
    home = discover(account, password)
    return home, [c['name'] for c in calendars(account, password, home)]


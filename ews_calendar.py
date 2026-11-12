"""A calendar on an on-premises Microsoft Exchange Server (2013, 2016, 2019, Subscription Edition) as a calendar
source, over Exchange Web Services (EWS). Like ms_graph.py does for Outlook, it answers the Google Calendar reads the app
makes (calendar_call), so its meetings flow through the same sync, history, meeting prep and Calendar view.

Exchange Online (Microsoft 365) is not read here: Microsoft is retiring EWS there and has turned basic sign-in off, so
such an account connects as Outlook (ms_graph.py). Autodiscover pointing to outlook.office365.com says so (exchange_online).

Python only, nothing to install: SOAP over https with Basic or NTLM (NTLMv2, with a small MD4 since OpenSSL 3 often
leaves it out). Reads only: GetFolder, FindItem (a calendar view, which expands recurring meetings), GetItem and
SyncFolderItems; never CreateItem, UpdateItem or DeleteItem.

Incremental: SyncFolderItems' state is the sync token. No change answers "nothing new"; a change answers 410, Google's
word for an expired sync token, so the sync reads its window again whole and removes what is gone
(machine/sources/calendar.sync_calendar).

The password comes from the account's credential file and only goes to the server, over verified TLS. Errors are fixed,
content-free labels (CalendarError): what the server said is matched, never kept or logged."""
import base64
import datetime as dt
import hmac
import http.client
import json
import os
import re
import struct
import time
import urllib.parse
from xml.sax.saxutils import escape

import caldav_calendar
from caldav_calendar import CalendarError
import ical

TIMEOUT = 60
MAX_ANSWER = 30_000_000
SLICE_DAYS = 31        # a calendar view this long per page (Exchange caps how many it returns at once)
VIEW_MAX = 1000
GET_BATCH = 50         # meetings read per GetItem
SYNC_PAGES = 200       # SyncFolderItems rounds to reach the end of a big calendar
ONLINE_HOSTS = ('outlook.office365.com', 'outlook.office.com', 'outlook.live.com')
T = 'http://schemas.microsoft.com/exchange/services/2006/types'
M = 'http://schemas.microsoft.com/exchange/services/2006/messages'
RESPONSES = {'Accept': 'accepted', 'Tentative': 'tentative', 'Decline': 'declined', 'Organizer': 'accepted',
             'NoResponseReceived': 'needsAction', 'Unknown': 'needsAction'}
_advanced = {}  # account id -> the sync state a change was found at, for the window read it starts (this process only)
_cache = {}     # account id -> (monotonic time, calendar folder answered) for calendars.get then events.list


# ------------------------------------------------------------------------------------------------- NTLM

def md4(data):
    """MD4 (RFC 1320), for NTLM's password hash: OpenSSL 3 builds often leave it out of hashlib."""
    mask = 0xFFFFFFFF
    rot = lambda x, n: ((x << n) | (x >> (32 - n))) & mask  # noqa: E731
    msg = bytearray(data) + b'\x80'
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += struct.pack('<Q', len(data) * 8)
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
    rounds = (
        (lambda x, y, z: (x & y) | (~x & z), 0, list(range(16)), (3, 7, 11, 19)),
        (lambda x, y, z: (x & y) | (x & z) | (y & z), 0x5A827999, [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15], (3, 5, 9, 13)),
        (lambda x, y, z: x ^ y ^ z, 0x6ED9EBA1, [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15], (3, 9, 11, 15)),
    )
    for offset in range(0, len(msg), 64):
        x = struct.unpack('<16I', bytes(msg[offset:offset + 64]))
        a, b, c, d = h
        for f, const, order, shifts in rounds:
            for i, k in enumerate(order):
                a, b, c, d = d, rot((a + (f(b, c, d) & mask) + x[k] + const) & mask, shifts[i % 4]), b, c
        h = [(v + w) & mask for v, w in zip(h, (a, b, c, d))]
    return struct.pack('<4I', *h)


FLAGS = 0xA0888205  # unicode, request target, NTLM, always sign, extended session security, target info, 128, 56


def ntlm_negotiate():
    return b'NTLMSSP\x00' + struct.pack('<II', 1, FLAGS) + b'\x00' * 16


def _user_domain(username):
    """'DOMAIN\\user' -> (user, DOMAIN); 'user@example.com' (a UPN) stays whole with no domain."""
    if '\\' in username:
        domain, _, user = username.partition('\\')
        return user, domain
    return username, ''


def ntlm_authenticate(challenge, username, password, client=None, stamp=None):
    """The NTLMv2 answer to a server's challenge message."""
    if len(challenge) < 32 or challenge[:8] != b'NTLMSSP\x00' or struct.unpack('<I', challenge[8:12])[0] != 2:
        raise CalendarError('ews_auth_failed', 401, retry_after=3600)
    server = challenge[24:32]
    info = b''
    if len(challenge) >= 48:
        length, _max, offset = struct.unpack('<HHI', challenge[40:48])
        info = challenge[offset:offset + length]
    user, domain = _user_domain(username)
    key = hmac.new(md4(password.encode('utf-16-le')), (user.upper() + domain).encode('utf-16-le'), 'md5').digest()
    client = client or os.urandom(8)
    found = _av(info, 7)  # MsvAvTimestamp: the server's clock
    stamp = found or stamp or struct.pack('<Q', int((time.time() + 11644473600) * 10_000_000))
    blob = b'\x01\x01' + b'\x00' * 6 + stamp + client + b'\x00' * 4 + info + b'\x00' * 4
    nt = hmac.new(key, server + blob, 'md5').digest() + blob
    lm = b'\x00' * 24 if found else hmac.new(key, server + client, 'md5').digest() + client
    fields = [lm, nt, domain.encode('utf-16-le'), user.encode('utf-16-le'), b'', b'']
    offset, header, payload = 64, b'', b''
    for value in fields:
        header += struct.pack('<HHI', len(value), len(value), offset + len(payload))
        payload += value
    return b'NTLMSSP\x00' + struct.pack('<I', 3) + header + struct.pack('<I', FLAGS) + payload


def _av(info, wanted):
    i = 0
    while i + 4 <= len(info):
        kind, length = struct.unpack('<HH', info[i:i + 4])
        if kind == 0:
            return None
        if kind == wanted:
            return info[i + 4:i + 4 + length]
        i += 4 + length
    return None


# ------------------------------------------------------------------------------------------------- HTTP

def post(url, body, username, password, scheme=None, content_type='text/xml; charset=utf-8'):
    """(status, data, scheme used) of one POST, signed in with NTLM (also inside Negotiate) or Basic: scheme 'ntlm',
    'basic', or None to take what the server offers, NTLM first so the password itself never travels."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != 'https' or not parts.hostname:
        raise CalendarError('ews_plaintext_refused')
    path = (parts.path or '/') + ('?' + parts.query if parts.query else '')
    basic = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
    try:
        connection = http.client.HTTPSConnection(parts.hostname, parts.port or 443, timeout=TIMEOUT, context=caldav_calendar.tls_context())
        try:
            def send(auth):
                connection.request('POST', path, body=body, headers={'Content-Type': content_type, 'User-Agent': 'TheMachine-calendar',
                                                                     **({'Authorization': auth} if auth else {})})
                reply = connection.getresponse()
                data = reply.read(MAX_ANSWER + 1)
                return reply, data
            if scheme == 'basic':
                reply, data = send(basic)
            else:
                word, used = 'NTLM', 'ntlm'
                reply, data = send('NTLM ' + base64.b64encode(ntlm_negotiate()).decode())
                offers = reply.headers.get_all('WWW-Authenticate') or [] if reply.status == 401 else []
                if reply.status == 401 and not _token(offers) and any(o.lower().startswith('negotiate') for o in offers):
                    word = 'Negotiate'  # NTLM inside Negotiate (IIS with Windows authentication)
                    reply, data = send('Negotiate ' + base64.b64encode(ntlm_negotiate()).decode())
                    offers = reply.headers.get_all('WWW-Authenticate') or [] if reply.status == 401 else []
                token = _token(offers)
                if reply.status == 401 and token:
                    reply, data = send(word + ' ' + base64.b64encode(ntlm_authenticate(token, username, password)).decode())
                elif reply.status == 401 and scheme is None and any(o.lower().startswith('basic') for o in offers):
                    reply, data = send(basic)
                    used = 'basic'
                scheme = used
        finally:
            connection.close()
    except CalendarError:
        raise
    except Exception as error:  # noqa: BLE001 - every failure becomes a label, its text never kept
        raise caldav_calendar.failure(error, 'ews') from None
    if len(data) > MAX_ANSWER:
        raise CalendarError('ews_too_big')
    return reply.status, data, scheme


def _token(offers):
    for offer in offers:
        match = re.match(r'\s*(?:NTLM|Negotiate)\s+([A-Za-z0-9+/=]+)\s*$', offer, re.I)
        if match:
            try:
                return base64.b64decode(match[1])
            except ValueError:
                return None
    return None


# ------------------------------------------------------------------------------------------------- autodiscover

def online(url):
    host = (urllib.parse.urlsplit(str(url or '')).hostname or '').lower()
    return host in ONLINE_HOSTS or host.endswith('.office365.com')


def server_url(text):
    """A server as typed (mail.example.com, or its whole EWS address) as the EWS address."""
    url = caldav_calendar.https_url(text)
    if urllib.parse.urlsplit(url).path in ('', '/'):
        url = url.rstrip('/') + '/EWS/Exchange.asmx'
    return url


def _json_url(url):
    try:
        status, _headers, data = caldav_calendar.request(url, 'GET', None, {'Accept': 'application/json'}, prefix='ews', redirects=2)
        found = json.loads(data.decode('utf-8', 'replace')) if status == 200 else {}
    except (CalendarError, ValueError):
        return None
    value = found.get('Url') if isinstance(found, dict) else None
    return value if isinstance(value, str) and value.lower().startswith('https://') else None


def microsoft_365(email):
    """True when Microsoft's own autodiscover sends the address to Exchange Online (Microsoft 365)."""
    found = _json_url('https://autodiscover-s.outlook.com/autodiscover/autodiscover.json/v1.0/'
                      + urllib.parse.quote(email) + '?Protocol=EWS')
    return bool(found and online(found))


POX = ('<?xml version="1.0" encoding="utf-8"?><Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">'
       '<Request><EMailAddress>{}</EMailAddress><AcceptableResponseSchema>'
       'http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema></Request></Autodiscover>')


def autodiscover(email, username, password):
    """(EWS address, scheme) for an address: the domain's autodiscover (JSON, then the signed-in XML one). Raises
    exchange_online for a Microsoft 365 mailbox, and ews_not_found when nothing answers."""
    domain = email.rpartition('@')[2].lower()
    if not re.fullmatch(r'[a-z0-9.-]+\.[a-z]{2,}', domain):
        raise CalendarError('ews_not_configured')
    for host in (f'autodiscover.{domain}', domain):
        found = _json_url(f'https://{host}/autodiscover/autodiscover.json?' + urllib.parse.urlencode({'Email': email, 'Protocol': 'EWS', 'RedirectCount': 1}))
        if found:
            if online(found):
                raise CalendarError('exchange_online', retry_after=86400)
            return found, None
    for host in (domain, f'autodiscover.{domain}'):
        try:
            status, data, scheme = post(f'https://{host}/autodiscover/autodiscover.xml', POX.format(escape(email)).encode(), username, password)
        except CalendarError:
            continue  # not there, or no trusted certificate: the next one
        if status in (401, 403):
            raise CalendarError('ews_auth_failed', status, retry_after=3600)
        text = data.decode('utf-8', 'replace')
        if status != 200 or re.search(r'<!(DOCTYPE|ENTITY)', text, re.I):
            continue
        urls = re.findall(r'<EwsUrl>\s*(https://[^<\s]+)\s*</EwsUrl>', text)
        if urls:
            if online(urls[0]):
                raise CalendarError('exchange_online', retry_after=86400)
            return urls[0], scheme
    raise CalendarError('ews_not_found', 404, retry_after=3600)


# ------------------------------------------------------------------------------------------------- SOAP

ENVELOPE = ('<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
            f'xmlns:t="{T}" xmlns:m="{M}"><soap:Header><t:RequestServerVersion Version="Exchange2013"/></soap:Header>'
            '<soap:Body>{}</soap:Body></soap:Envelope>')
CALENDAR = '<t:DistinguishedFolderId Id="calendar"/>'


def _q(ns, name):
    return '{%s}%s' % (ns, name)


def soap(account, password, body):
    """The answer's first response message, checked: a fault or an error code becomes a label."""
    url = account.get('ews_url') or ''
    if not url:
        raise CalendarError('ews_not_configured')
    if online(url):
        raise CalendarError('exchange_online', retry_after=86400)
    status, data, scheme = post(url, ENVELOPE.format(body).encode(), account.get('username') or account.get('email') or '',
                                password, account.get('ews_auth'))
    if status in (401, 403):
        raise CalendarError('ews_auth_failed', status, retry_after=3600)
    if status not in (200, 500):
        raise caldav_calendar.status_error(status, 'ews')
    tree = caldav_calendar.parse_xml(data, 'ews')
    message = next((e for e in tree.iter() if e.tag.startswith('{%s}' % M) and e.tag.endswith('ResponseMessage')), None)
    if message is None:
        raise CalendarError('ews', status)
    code = message.findtext(_q(M, 'ResponseCode')) or ''
    if code in ('ErrorInvalidSyncStateData', 'ErrorInvalidSyncStateObject'):
        raise CalendarError('ews', 410)
    if code in ('ErrorServerBusy', 'ErrorTooManyObjectsOpened'):
        raise CalendarError('ews_rate_limited', 503, retry_after=600)
    if code in ('ErrorAccessDenied', 'ErrorNonExistentMailbox'):
        raise CalendarError('ews_auth_failed', 403, retry_after=3600)
    if code != 'NoError' and message.get('ResponseClass') == 'Error':
        raise CalendarError('ews_refused')
    return tree, scheme


def _stamp(value):
    return value.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def view_ids(account, password, start, end):
    body = ('<m:FindItem Traversal="Shallow"><m:ItemShape><t:BaseShape>IdOnly</t:BaseShape></m:ItemShape>'
            f'<m:CalendarView MaxEntriesReturned="{VIEW_MAX}" StartDate="{_stamp(start)}" EndDate="{_stamp(end)}"/>'
            f'<m:ParentFolderIds>{CALENDAR}</m:ParentFolderIds></m:FindItem>')
    tree, _scheme = soap(account, password, body)
    return [e.get('Id') for e in tree.iter(_q(T, 'ItemId')) if e.get('Id')]


FIELDS = ('item:Subject', 'item:Body', 'item:LastModifiedTime', 'calendar:Start', 'calendar:End', 'calendar:IsAllDayEvent',
          'calendar:Location', 'calendar:Organizer', 'calendar:RequiredAttendees', 'calendar:OptionalAttendees',
          'calendar:Resources', 'calendar:IsCancelled', 'calendar:LegacyFreeBusyStatus', 'calendar:UID',
          'calendar:CalendarItemType', 'calendar:RecurrenceId', 'calendar:MyResponseType')


def get_items(account, password, ids):
    out = []
    for i in range(0, len(ids), GET_BATCH):
        body = ('<m:GetItem><m:ItemShape><t:BaseShape>IdOnly</t:BaseShape><t:BodyType>Text</t:BodyType><t:AdditionalProperties>'
                + ''.join(f'<t:FieldURI FieldURI="{f}"/>' for f in FIELDS) + '</t:AdditionalProperties></m:ItemShape><m:ItemIds>'
                + ''.join(f'<t:ItemId Id="{escape(x, {chr(34): "&quot;"})}"/>' for x in ids[i:i + GET_BATCH]) + '</m:ItemIds></m:GetItem>')
        tree, _scheme = soap(account, password, body)
        out += list(tree.iter(_q(T, 'CalendarItem')))
    return out


def _utc(text):
    return dt.datetime.fromisoformat(str(text).strip().replace('Z', '+00:00')).astimezone(dt.timezone.utc)


def _all_day(stamp):
    """An all-day meeting's date: Exchange gives local midnight as UTC; the owner's zone, else the nearest midnight."""
    local = stamp.astimezone(caldav_calendar.local_tz())
    if (local.hour, local.minute) == (0, 0):
        return local.date()
    return (stamp + dt.timedelta(hours=12)).date()


def _person(mailbox):
    if mailbox is None:
        return {}
    email = (mailbox.findtext(_q(T, 'EmailAddress')) or '').strip()
    routing = (mailbox.findtext(_q(T, 'RoutingType')) or 'SMTP').upper()
    return {'email': email.lower() if routing == 'SMTP' and '@' in email else '', 'displayName': (mailbox.findtext(_q(T, 'Name')) or '').strip()}


def item_of(element, owner):
    """A CalendarItem as a Google Calendar event (the fields calendar_event reads)."""
    text = lambda name, ns=T: (element.findtext(_q(ns, name)) or '').strip()  # noqa: E731
    uid = text('UID') or text('Subject')
    kind = text('CalendarItemType')
    all_day = text('IsAllDayEvent').lower() == 'true'
    start, end = _utc(text('Start')), _utc(text('End'))
    master = ical.event_id(uid, 'ews')
    recurrence = text('RecurrenceId')
    item = {'id': master, 'summary': text('Subject') or '(untitled event)',
            'start': {'date': _all_day(start).isoformat()} if all_day else {'dateTime': start.isoformat()},
            'end': {'date': max(_all_day(end), _all_day(start) + dt.timedelta(days=1)).isoformat()} if all_day else {'dateTime': end.isoformat()},
            'status': 'cancelled' if text('IsCancelled').lower() == 'true' else 'confirmed',
            'updated': _utc(text('LastModifiedTime')).isoformat() if text('LastModifiedTime') else None,
            'location': text('Location') or None, 'description': text('Body')[:40000], 'iCalUID': uid[:500] or None}
    organizer = _person(element.find(_q(T, 'Organizer') + '/' + _q(T, 'Mailbox')))
    if organizer.get('email') in owner or text('MyResponseType') == 'Organizer':
        organizer['self'] = True
    item['organizer'] = organizer
    attendees = []
    for group in ('RequiredAttendees', 'OptionalAttendees', 'Resources'):
        for attendee in element.findall(_q(T, group) + '/' + _q(T, 'Attendee'))[:500]:
            person = _person(attendee.find(_q(T, 'Mailbox')))
            if not person.get('email'):
                continue
            person['responseStatus'] = RESPONSES.get((attendee.findtext(_q(T, 'ResponseType')) or '').strip(), 'needsAction')
            if person['email'] in owner:
                person['self'] = True
                person['responseStatus'] = RESPONSES.get(text('MyResponseType'), person['responseStatus'])
            if group == 'Resources':
                person['resource'] = True
            attendees.append(person)
    item['attendees'] = attendees
    if text('LegacyFreeBusyStatus') == 'Free':
        item['transparency'] = 'transparent'
    if kind in ('Occurrence', 'Exception') and recurrence:
        moment = _utc(recurrence)
        item.update(id=f'{master}_{moment.strftime("%Y%m%dT%H%M%SZ")}', recurringEventId=master,
                    originalStartTime={'date': _all_day(moment).isoformat()} if all_day else {'dateTime': moment.isoformat()})
    return item


def sync_state(account, password, state=''):
    """(new state, whether anything changed) after SyncFolderItems from `state` ('' from the start) to the end."""
    changed = False
    for _ in range(SYNC_PAGES):
        body = ('<m:SyncFolderItems><m:ItemShape><t:BaseShape>IdOnly</t:BaseShape></m:ItemShape>'
                f'<m:SyncFolderId>{CALENDAR}</m:SyncFolderId>' + (f'<m:SyncState>{escape(state)}</m:SyncState>' if state else '')
                + '<m:MaxChangesReturned>512</m:MaxChangesReturned></m:SyncFolderItems>')
        tree, _scheme = soap(account, password, body)
        state = next((e.text or '' for e in tree.iter(_q(M, 'SyncState'))), state)
        changes = next(tree.iter(_q(M, 'Changes')), None)
        changed = changed or (changes is not None and any(not c.tag.endswith('ReadFlagChange') for c in changes))
        if (next((e.text for e in tree.iter(_q(M, 'IncludesLastItemInRange'))), 'true') or 'true').lower() == 'true':
            return state, changed
    return state, changed


def calendar_call(config, credential, account, method, params):
    """Google Calendar's calendars.get and events.list (singleEvents, sync tokens) answered over EWS."""
    try:
        password = credential(config, account['credential'])
    except (OSError, KeyError):
        raise CalendarError('ews_password_missing', retry_after=3600) from None
    if method == 'calendars.get':
        soap(account, password, f'<m:GetFolder><m:FolderShape><t:BaseShape>IdOnly</t:BaseShape></m:FolderShape><m:FolderIds>{CALENDAR}</m:FolderIds></m:GetFolder>')
        return {'id': str(account.get('email') or '').lower(), 'timeZone': 'UTC'}
    if method != 'events.list':
        raise CalendarError('unsupported_calendar_method')
    if params.get('syncToken'):
        state, changed = sync_state(account, password, params['syncToken'])
        if changed:
            _advanced[account['id']] = state
            raise CalendarError('ews', 410)  # changed: the window is read again whole (sync_calendar)
        return {'items': [], 'nextSyncToken': state}
    owner = caldav_calendar.owner_addresses(account)

    def read_slice(start, end, _first):
        items, skipped = [], 0
        for element in get_items(account, password, view_ids(account, password, start, end)):
            try:
                items.append(item_of(element, owner))
            except (ValueError, TypeError, AttributeError):
                skipped += 1
        return items, skipped

    def marker():
        return _advanced.pop(account['id'], None) or sync_state(account, password)[0]
    return caldav_calendar.page_of(params, read_slice, marker, SLICE_DAYS)


def check(account, password):
    """Sign in and open the calendar before anything is saved: (EWS address, scheme used)."""
    if not account.get('ews_url'):
        account['ews_url'], account['ews_auth'] = autodiscover(account['email'], account.get('username') or account['email'], password)
    _tree, account['ews_auth'] = soap(account, password, f'<m:GetFolder><m:FolderShape><t:BaseShape>IdOnly</t:BaseShape></m:FolderShape><m:FolderIds>{CALENDAR}</m:FolderIds></m:GetFolder>')
    return account['ews_url'], account['ews_auth']


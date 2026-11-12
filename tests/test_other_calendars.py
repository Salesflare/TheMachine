"""Calendars beyond Google and Outlook (caldav_calendar.py, ics_feed.py, ews_calendar.py, ical.py,
machine/sources/calendar_setup.py): read-only, in Google Calendar's shapes, through the same sync. Fake servers on this
computer (https with a throwaway certificate, trusted only inside these tests) hold made-up meetings: a CalDAV server,
a calendar link and an Exchange Server with NTLM. Every other address is refused, so no real server is reached. The
password and the link never show in a log, an error, the config or the database."""
import base64
import datetime as dt
import hmac
import http.server
import json
import logging
import os
import re
import shutil
import socket
import ssl
import struct
import subprocess
import tempfile
import threading
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

import caldav_calendar
import ews_calendar
import ical
import ics_feed
import onboarding
import sources
from caldav_calendar import CalendarError
from machine.sources import calendar_setup
from test_ux import a

PASSWORD = 'pw-Fake-5521-cal'  # made up; the tests look for it everywhere it must not be
LINK_KEY = 'k-Fake-9931-share'  # the secret part of a made-up calendar link
USER, APPLE_ID = 'alex@acme.test', 'alex@icloud.com'
FAKE_HOSTS = {'caldav.acme.test', 'caldav.icloud.com', 'feeds.acme.test', 'mail.acme.test', 'basic.acme.test',
              'autodiscover.acme.test', 'acme.test', 'autodiscover-s.outlook.com', 'autodiscover.cloudco.test', 'cloudco.test'}
REAL_CONNECT = socket.create_connection
T, M = ews_calendar.T, ews_calendar.M
BRUSSELS, NEW_YORK = ZoneInfo('Europe/Brussels'), ZoneInfo('America/New_York')


def local(when):
    return when.strftime('%Y%m%dT%H%M%S')


def utc(when):
    return when.astimezone(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def vcal(*events):
    return 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fake//Test//EN\r\n' + ''.join(events) + 'END:VCALENDAR\r\n'


def vevent(uid, summary, lines):
    return f'BEGIN:VEVENT\r\nUID:{uid}\r\nDTSTAMP:20260101T000000Z\r\nSUMMARY:{summary}\r\n' + ''.join(l + '\r\n' for l in lines) + 'END:VEVENT\r\n'


def certificate(folder):
    key, cert = Path(folder) / 'key.pem', Path(folder) / 'cert.pem'
    names = ','.join('DNS:' + h for h in sorted(FAKE_HOSTS | {'localhost'}))
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', str(key), '-out', str(cert),
                    '-days', '1', '-subj', '/CN=localhost', '-addext', 'subjectAltName=' + names,
                    '-addext', 'keyUsage=critical,digitalSignature,keyEncipherment,keyCertSign',
                    '-addext', 'extendedKeyUsage=serverAuth'], check=True, capture_output=True)
    return str(cert), str(key)


# ------------------------------------------------------------------------------------------------- the fake servers

def multistatus(responses):
    return ('<?xml version="1.0" encoding="utf-8"?><d:multistatus xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav" '
            'xmlns:cs="http://calendarserver.org/ns/">' + ''.join(
                f'<d:response><d:href>{href}</d:href><d:propstat><d:prop>{props}</d:prop>'
                '<d:status>HTTP/1.1 200 OK</d:status></d:propstat></d:response>' for href, props in responses) + '</d:multistatus>')


def ews_answer(op, inner='', code='NoError'):
    kind = 'Success' if code == 'NoError' else 'Error'
    return (f'<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body>'
            f'<m:{op}Response xmlns:m="{M}" xmlns:t="{T}"><m:ResponseMessages><m:{op}ResponseMessage ResponseClass="{kind}">'
            f'<m:ResponseCode>{code}</m:ResponseCode>{inner}</m:{op}ResponseMessage></m:ResponseMessages></m:{op}Response>'
            '</s:Body></s:Envelope>')


def mailbox(name, email):
    return f'<t:Mailbox><t:Name>{name}</t:Name><t:EmailAddress>{email}</t:EmailAddress><t:RoutingType>SMTP</t:RoutingType></t:Mailbox>'


def ntlm_challenge(nonce):
    info = (struct.pack('<HH', 2, 8) + 'ACME'.encode('utf-16-le') + struct.pack('<HH', 7, 8)
            + struct.pack('<Q', 133_000_000_000_000_000) + struct.pack('<HH', 0, 0))
    return (b'NTLMSSP\x00' + struct.pack('<I', 2) + struct.pack('<HHI', 0, 0, 48) + struct.pack('<I', 0xA2898205)
            + nonce + b'\x00' * 8 + struct.pack('<HHI', len(info), len(info), 48) + info)


def ntlm_valid(message, nonce, password):
    """The server's side of NTLMv2: the client's proof matches the password, for ACME\\alex."""
    fields = []
    for i in range(4):
        length, _max, offset = struct.unpack('<HHI', message[12 + 8 * i:20 + 8 * i])
        fields.append(message[offset:offset + length])
    _lm, nt, domain, user = fields
    domain, user = domain.decode('utf-16-le'), user.decode('utf-16-le')
    key = hmac.new(ews_calendar.md4(password.encode('utf-16-le')), (user.upper() + domain).encode('utf-16-le'), 'md5').digest()
    return (domain, user) == ('ACME', 'alex') and hmac.new(key, nonce + nt[16:], 'md5').digest() == nt[:16]


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    nonce = None  # this connection's NTLM challenge

    def log_message(self, *args):
        pass

    def reply(self, status, body='', headers=()):
        body = body.encode() if isinstance(body, str) else body
        self.send_response(status)
        for key, value in headers:
            self.send_header(key, value)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def any(self):
        size = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(size).decode() if size else ''
        host = (self.headers.get('Host') or '').rpartition(':')[0] or self.headers.get('Host')
        fake = self.server.fake
        fake.requests.append((host, self.command, self.path, dict(self.headers), body))
        if host in ('caldav.acme.test', 'caldav.icloud.com'):
            return fake.caldav(self, host, body)
        if host == 'feeds.acme.test':
            return fake.feed(self)
        if host in ('mail.acme.test', 'basic.acme.test'):
            return fake.ews(self, host, body)
        return fake.autodiscover(self, host)

    do_GET = do_POST = do_PROPFIND = do_REPORT = any


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True


class Fake:
    """The made-up servers' data, and every request they got."""

    def __init__(self, cert):
        self.requests = []
        now = dt.datetime.now(BRUSSELS).replace(second=0, microsecond=0)
        self.now = now
        standup = (now - dt.timedelta(days=2)).replace(hour=10, minute=0)
        self.standup = standup
        lunch = (now + dt.timedelta(days=1)).replace(hour=12, minute=0)
        daily = vevent('standup@acme.test', 'Daily standup', [
            f'DTSTART;TZID=Europe/Brussels:{local(standup)}', f'DTEND;TZID=Europe/Brussels:{local(standup + dt.timedelta(minutes=15))}',
            'RRULE:FREQ=DAILY;COUNT=5', f'EXDATE;TZID=Europe/Brussels:{local(standup + dt.timedelta(days=2))}',
            'ORGANIZER;CN=Alex:mailto:alex@acme.test', 'ATTENDEE;CN=Bo;PARTSTAT=ACCEPTED:mailto:bo@client.test',
            'ATTENDEE;CUTYPE=ROOM;CN=Room 4:mailto:room4@acme.test'])
        meal = vevent('lunch@acme.test', 'Lunch with Bo', [f'DTSTART:{utc(lunch)}', f'DTEND:{utc(lunch + dt.timedelta(hours=1))}',
                                                          'ATTENDEE;CN=Bo:mailto:bo@client.test'])
        day = (now + dt.timedelta(days=3)).date()
        dentist = vevent('dentist@acme.test', 'Dentist', [f'DTSTART;VALUE=DATE:{day:%Y%m%d}',
                                                          f'DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}'])
        todo = 'BEGIN:VTODO\r\nUID:todo@acme.test\r\nSUMMARY:Buy milk\r\nEND:VTODO\r\n'
        self.calendars = {
            'work': {'name': 'Work', 'token': 'https://caldav.acme.test/sync/1', 'parts': 'VEVENT',
                     'objects': {'standup.ics': ('"e1"', vcal(daily)), 'lunch.ics': ('"e2"', vcal(meal))}},
            'family': {'name': 'Family', 'token': None, 'parts': 'VEVENT', 'objects': {'dentist.ics': ('"e3"', vcal(dentist))}},
            'reminders': {'name': 'Reminders', 'token': 'r1', 'parts': 'VTODO', 'objects': {'todo.ics': ('"e4"', vcal(todo))}}}
        # a calendar link: a weekly meeting in New York's time, one occurrence moved
        team = (now.astimezone(NEW_YORK) - dt.timedelta(days=3)).replace(hour=9, minute=0, second=0)
        self.team = team
        self.feed_events = [
            vevent('team@feed.test', 'Team sync', [f'DTSTART;TZID=America/New_York:{local(team)}',
                                                   f'DTEND;TZID=America/New_York:{local(team + dt.timedelta(hours=1))}',
                                                   'RRULE:FREQ=WEEKLY;COUNT=6']),
            vevent('team@feed.test', 'Team sync (moved)', [
                f'RECURRENCE-ID;TZID=America/New_York:{local(team + dt.timedelta(days=7))}',
                f'DTSTART;TZID=America/New_York:{local((team + dt.timedelta(days=7)).replace(hour=11))}',
                f'DTEND;TZID=America/New_York:{local((team + dt.timedelta(days=7)).replace(hour=12))}'])]
        self.feed_etag, self.feed_status = '"v1"', 200
        # an Exchange Server's calendar
        at = lambda days, hour: (now + dt.timedelta(days=days)).astimezone(dt.timezone.utc).replace(hour=hour, minute=0)  # noqa: E731
        self.items = {
            'AAMk-plan': dict(subject='Quarterly plan', start=at(2, 14), end=at(2, 15), uid='plan@acme.test', kind='Single',
                              organizer=('Bo', 'bo@client.test'), required=[('Alex', USER, 'Unknown'), ('Cy', 'cy@client.test', 'Accept')],
                              resources=[('Room 4', 'room4@acme.test')], my='Accept'),
            'AAMk-one-1': dict(subject='Weekly 1:1', start=at(1, 9), end=at(1, 10), uid='oneone@acme.test', kind='Occurrence',
                               organizer=('Alex', USER), required=[('Bo', 'bo@client.test', 'Tentative')], my='Organizer'),
            'AAMk-one-2': dict(subject='Weekly 1:1', start=at(8, 9), end=at(8, 10), uid='oneone@acme.test', kind='Occurrence',
                               organizer=('Alex', USER), required=[('Bo', 'bo@client.test', 'Decline')], my='Organizer'),
            'AAMk-offsite': dict(subject='Offsite', start=at(27, 8), end=at(27, 17), uid='offsite@acme.test', kind='Single',
                                 organizer=('Alex', USER), required=[], my='Organizer')}
        self.version, self.known_states = 1, {'state-1'}
        self.basic_used = False
        self.server = Server(('127.0.0.1', 0), Handler)
        self.server.fake = self
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(*cert)
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def connect(self, address, *args, **kwargs):
        """Every connection the code makes: a fake host goes to the fake server, anything else is refused."""
        if address[0] in FAKE_HOSTS:
            return REAL_CONNECT(('127.0.0.1', self.port), *args, **kwargs)
        raise OSError('no network in tests')

    def made(self, host=None, method=None):
        return [r for r in self.requests if (host is None or r[0] == host) and (method is None or r[1] == method)]

    # -- CalDAV
    def caldav(self, handler, host, body):
        wanted = base64.b64encode(f'{APPLE_ID if host == "caldav.icloud.com" else USER}:{PASSWORD}'.encode()).decode()
        if handler.headers.get('Authorization') != 'Basic ' + wanted:
            return handler.reply(401, '', [('WWW-Authenticate', 'Basic realm="fake"')])
        path, depth = handler.path, handler.headers.get('Depth')
        if path == '/.well-known/caldav':
            return handler.reply(301, '', [('Location', '/dav/')])
        if path == '/dav/':
            return handler.reply(207, multistatus([('/dav/', '<d:current-user-principal><d:href>/dav/principals/alex/</d:href></d:current-user-principal>')]))
        if path == '/dav/principals/alex/':
            return handler.reply(207, multistatus([(path, '<c:calendar-home-set><d:href>/dav/calendars/alex/</d:href></c:calendar-home-set>')]))
        if path == '/dav/calendars/alex/' and depth == '1':
            listing = [(path, '<d:resourcetype><d:collection/></d:resourcetype><d:displayname>Alex</d:displayname>')]
            for key, c in self.calendars.items():
                listing.append((f'{path}{key}/', '<d:resourcetype><d:collection/><c:calendar/></d:resourcetype>'
                                f'<d:displayname>{c["name"]}</d:displayname><c:supported-calendar-component-set>'
                                f'<c:comp name="{c["parts"]}"/></c:supported-calendar-component-set>'
                                + (f'<d:sync-token>{c["token"]}</d:sync-token>' if c['token'] else '')))
            return handler.reply(207, multistatus(listing))
        match = re.fullmatch(r'/dav/calendars/alex/(\w+)/', path)
        if not match or match[1] not in self.calendars:
            return handler.reply(404)
        objects = self.calendars[match[1]]['objects']
        if handler.command == 'PROPFIND':  # the etags of a calendar without a sync-token
            return handler.reply(207, multistatus([(path + name, f'<d:getetag>{tag}</d:getetag>') for name, (tag, _t) in objects.items()]))
        assert 'time-range' in body
        return handler.reply(207, multistatus([(path + name, f'<d:getetag>{tag}</d:getetag><c:calendar-data>{escape(text)}</c:calendar-data>')
                                               for name, (tag, text) in objects.items()]))

    # -- a calendar link
    def feed(self, handler):
        if handler.path == '/cal/away.ics':
            return handler.reply(302, '', [('Location', 'https://elsewhere.test/cal.ics')])
        if handler.path == '/cal/plain.ics':
            return handler.reply(302, '', [('Location', 'http://feeds.acme.test/cal/' + LINK_KEY + '.ics')])
        if handler.path == '/cal/page.ics':
            return handler.reply(200, '<html>Sign in</html>', [('Content-Type', 'text/html')])
        if handler.path != f'/cal/{LINK_KEY}.ics' or self.feed_status != 200:
            return handler.reply(404 if self.feed_status == 200 else self.feed_status)
        if handler.headers.get('If-None-Match') == self.feed_etag:
            return handler.reply(304, '', [('ETag', self.feed_etag)])
        return handler.reply(200, vcal(*self.feed_events), [('Content-Type', 'text/calendar'), ('ETag', self.feed_etag),
                                                             ('Last-Modified', 'Mon, 02 Nov 2026 08:00:00 GMT')])

    # -- Autodiscover
    def autodiscover(self, handler, host):
        if host == 'autodiscover-s.outlook.com':
            if 'cloudco.test' in urllib.parse.unquote(handler.path):
                return handler.reply(200, json.dumps({'Protocol': 'EWS', 'Url': 'https://outlook.office365.com/EWS/Exchange.asmx'}))
            return handler.reply(404)
        if host == 'autodiscover.acme.test' and handler.path.startswith('/autodiscover/autodiscover.json'):
            return handler.reply(200, json.dumps({'Protocol': 'EWS', 'Url': 'https://mail.acme.test/EWS/Exchange.asmx'}))
        if host == 'autodiscover.cloudco.test' and handler.path.startswith('/autodiscover/autodiscover.json'):
            return handler.reply(200, json.dumps({'Protocol': 'EWS', 'Url': 'https://outlook.office365.com/EWS/Exchange.asmx'}))
        return handler.reply(404)

    # -- Exchange Web Services
    def ews(self, handler, host, body):
        auth = handler.headers.get('Authorization') or ''
        offers = [('WWW-Authenticate', 'Basic realm="mail"')] if host == 'basic.acme.test' else [
            ('WWW-Authenticate', 'Negotiate'), ('WWW-Authenticate', 'NTLM')]
        word, _, token = auth.partition(' ')
        signed_in = False
        if word in ('NTLM', 'Negotiate') and host != 'basic.acme.test':
            message = base64.b64decode(token)
            kind = struct.unpack('<I', message[8:12])[0]
            if kind == 1:
                handler.nonce = os.urandom(8)
                return handler.reply(401, '', [('WWW-Authenticate', f'{word} ' + base64.b64encode(ntlm_challenge(handler.nonce)).decode())])
            signed_in = kind == 3 and handler.nonce is not None and ntlm_valid(message, handler.nonce, PASSWORD)
        elif word == 'Basic':
            self.basic_used = True
            signed_in = host == 'basic.acme.test' and token == base64.b64encode(f'ACME\\alex:{PASSWORD}'.encode()).decode()
        if not signed_in:
            return handler.reply(401, '', offers)
        if '<m:GetFolder>' in body:
            return handler.reply(200, ews_answer('GetFolder', '<m:Folders><t:CalendarFolder><t:FolderId Id="cal"/></t:CalendarFolder></m:Folders>'))
        if '<m:FindItem' in body:
            low, high = (dt.datetime.fromisoformat(v.replace('Z', '+00:00')) for v in re.findall(r'(?:StartDate|EndDate)="([^"]+)"', body))
            ids = ''.join(f'<t:CalendarItem><t:ItemId Id="{i}"/></t:CalendarItem>' for i, x in self.items.items()
                          if x['start'] < high and x['end'] > low)
            return handler.reply(200, ews_answer('FindItem', f'<m:RootFolder><t:Items>{ids}</t:Items></m:RootFolder>'))
        if '<m:GetItem>' in body:
            return handler.reply(200, ews_answer('GetItem', '<m:Items>' + ''.join(
                self.item_xml(i) for i in re.findall(r'ItemId Id="([^"]+)"', body) if i in self.items) + '</m:Items>'))
        if '<m:SyncFolderItems>' in body:
            given = re.search(r'<m:SyncState>(.*?)</m:SyncState>', body)
            current = f'state-{self.version}'
            if given and given[1] not in self.known_states:
                return handler.reply(200, ews_answer('SyncFolderItems', code='ErrorInvalidSyncStateData'))
            changes = '' if given and given[1] == current else ''.join(
                f'<t:Create><t:CalendarItem><t:ItemId Id="{i}"/></t:CalendarItem></t:Create>' for i in self.items)
            return handler.reply(200, ews_answer('SyncFolderItems', f'<m:SyncState>{current}</m:SyncState>'
                                                 f'<m:IncludesLastItemInRange>true</m:IncludesLastItemInRange><m:Changes>{changes}</m:Changes>'))
        return handler.reply(500, ews_answer('Unknown', code='ErrorInvalidRequest'))

    def item_xml(self, key):
        x = self.items[key]
        stamp = lambda v: v.strftime('%Y-%m-%dT%H:%M:%SZ')  # noqa: E731
        people = ''.join(f'<t:Attendee>{mailbox(n, e)}<t:ResponseType>{r}</t:ResponseType></t:Attendee>' for n, e, r in x['required'])
        rooms = ''.join(f'<t:Attendee>{mailbox(n, e)}<t:ResponseType>Accept</t:ResponseType></t:Attendee>' for n, e in x.get('resources', []))
        return (f'<t:CalendarItem><t:ItemId Id="{key}"/><t:Subject>{x["subject"]}</t:Subject><t:Body BodyType="Text">Agenda</t:Body>'
                f'<t:LastModifiedTime>2026-11-01T08:00:00Z</t:LastModifiedTime><t:Start>{stamp(x["start"])}</t:Start>'
                f'<t:End>{stamp(x["end"])}</t:End><t:IsAllDayEvent>false</t:IsAllDayEvent><t:Location>Room 4</t:Location>'
                f'<t:Organizer>{mailbox(*x["organizer"])}</t:Organizer><t:RequiredAttendees>{people}</t:RequiredAttendees>'
                f'<t:Resources>{rooms}</t:Resources><t:IsCancelled>false</t:IsCancelled><t:LegacyFreeBusyStatus>Busy</t:LegacyFreeBusyStatus>'
                f'<t:UID>{x["uid"]}</t:UID><t:CalendarItemType>{x["kind"]}</t:CalendarItemType>'
                + (f'<t:RecurrenceId>{stamp(x["start"])}</t:RecurrenceId>' if x['kind'] == 'Occurrence' else '')
                + f'<t:MyResponseType>{x["my"]}</t:MyResponseType></t:CalendarItem>')


class FakeUI:
    """The setup's questions answered from a table; the password (or link) as typed."""
    interactive, web, reconnect = True, True, False

    def __init__(self, answers, secret):
        self.answers, self.password, self.lines = answers, secret, []

    def ask(self, prompt, default=''):
        return self.answers.get(prompt, default)

    def secret(self, prompt):
        return self.password

    def say(self, text=''):
        self.lines.append(text)


# ------------------------------------------------------------------------------------------------- tests

@unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
class Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certs = tempfile.TemporaryDirectory()
        cls.cert = certificate(cls.certs.name)

    @classmethod
    def tearDownClass(cls):
        cls.certs.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fake = Fake(self.cert)
        self.addCleanup(self.fake.close)
        for patch in (mock.patch.object(socket, 'create_connection', side_effect=self.fake.connect),
                      mock.patch.object(caldav_calendar, 'tls_context', lambda: ssl.create_default_context(cafile=self.cert[0]))):
            patch.start()
            self.addCleanup(patch.stop)
        for memory in (caldav_calendar._cache, ics_feed._seen, ews_calendar._advanced, ews_calendar._cache):
            memory.clear()
        self.config = {'credentials': {}, 'accounts': [], 'database': str(Path(self.temp.name) / 'events.sqlite'),
                       'data_dir': self.temp.name}
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.logs = []
        handler = logging.Handler(logging.DEBUG)
        handler.emit = lambda record: self.logs.append(record.getMessage())
        root = logging.getLogger()
        old = root.level
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        self.addCleanup(root.setLevel, old)
        self.addCleanup(root.removeHandler, handler)

    def account(self, account_id, service, secret, **more):
        transport = calendar_setup.TRANSPORTS[service]
        name = f'{transport}-{account_id}'
        path = Path(self.temp.name) / name
        path.write_text(secret + '\n')
        self.config['credentials'][name] = str(path)
        account = {'id': account_id, 'service': service, 'transport': transport, 'calendar_id': 'primary',
                   'boundary': 'work:Acme', 'credential': name, 'email': USER if transport != 'ics' else '', **more}
        self.config['accounts'].append(account)
        return account

    def events(self, account, deleted=0):
        with self.store.connect() as db:
            return [{**dict(r), 'metadata': json.loads(r['metadata'])} for r in db.execute(
                "SELECT * FROM events WHERE account_id=? AND kind='calendar.event' AND deleted=? ORDER BY occurred_at",
                (account['id'], deleted))]

    def titles(self, account, deleted=0):
        found = {}
        for row in self.events(account, deleted):
            found[row['title']] = found.get(row['title'], 0) + 1
        return found

    def assert_secret_kept(self, *texts):
        for text in [*texts, *self.logs]:
            self.assertNotIn(PASSWORD, str(text))
            self.assertNotIn(LINK_KEY, str(text))
        stored = Path(self.config['database']).read_bytes() if Path(self.config['database']).exists() else b''
        self.assertNotIn(PASSWORD.encode(), stored)
        self.assertNotIn(LINK_KEY.encode(), stored)


class CalDAV(Base):
    def test_window_then_nothing_new_then_a_removal(self):
        account = self.account('acme-caldav', 'caldav', PASSWORD, caldav_url='https://caldav.acme.test/')
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account), {'Daily standup': 4, 'Lunch with Bo': 1, 'Dentist': 1})  # 5 days, one left out
        standups = [r for r in self.events(account) if r['title'] == 'Daily standup']
        first = self.fake.standup.astimezone(dt.timezone.utc).isoformat()
        self.assertEqual(standups[0]['occurred_at'], first)  # 10:00 in Brussels
        meta = standups[0]['metadata']
        self.assertEqual(meta['attendees'][0], {'email': 'bo@client.test', 'displayName': 'Bo', 'responseStatus': 'accepted'})
        self.assertTrue(meta['attendees'][1]['resource'])  # the room is never a person
        self.assertEqual(len({r['metadata']['recurring_event_id'] for r in standups}), 1)
        self.assertNotIn('Buy milk', json.dumps(self.events(account)))  # a reminders list isn't read
        dentist = next(r for r in self.events(account) if r['title'] == 'Dentist')
        self.assertEqual(dentist['metadata']['start'], {'date': str((self.fake.now + dt.timedelta(days=3)).date())})
        self.assertEqual(self.store.checkpoint(account['id'])['mode'], 'incremental')
        # nothing changed: one listing, no calendar read
        before = len(self.fake.made(method='REPORT'))
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['events'], 0)
        self.assertEqual(len(self.fake.made(method='REPORT')), before)
        # the lunch is removed on the server: the window is read again, and it is gone here too
        del self.fake.calendars['work']['objects']['lunch.ics']
        self.fake.calendars['work']['token'] = 'https://caldav.acme.test/sync/2'
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['mode'], 'resync')
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account, deleted=1), {'Lunch with Bo': 1})
        # a calendar without a sync-token or ctag: its etags tell the change
        self.fake.calendars['family']['objects']['dentist.ics'] = ('"e3b"', self.fake.calendars['family']['objects']['dentist.ics'][1])
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['mode'], 'resync')
        self.assert_secret_kept(json.dumps(self.config))
        self.assertFalse([r for r in self.fake.requests if r[1] not in ('PROPFIND', 'REPORT')])  # reads only

    def test_icloud_setup_signs_in_and_saves_only_then(self):
        account = {'id': 'acme-icloud', 'service': 'icloud_calendar', 'boundary': 'work:Acme'}
        ui = FakeUI({'Apple ID': APPLE_ID}, 'pw-Wrong-0000')
        with self.assertRaises(onboarding.SetupError) as caught:
            calendar_setup.step(self.config, account, ui)
        self.assertEqual(caught.exception.message, 'The server refused the username or password')
        self.assertIn('appleid.apple.com', caught.exception.fix)
        self.assertFalse(Path(self.config['credentials'][account['credential']]).exists())
        ui = FakeUI({'Apple ID': APPLE_ID}, PASSWORD)
        calendar_setup.step(self.config, account, ui)
        self.assertEqual((account['transport'], account['email']), ('caldav', APPLE_ID))
        self.assertEqual(account['caldav_home'], 'https://caldav.icloud.com/dav/calendars/alex/')
        self.assertEqual(ui.lines, ['  2 calendars found', '  signed in'])
        saved = Path(self.config['credentials'][account['credential']])
        self.assertEqual((saved.read_text().strip(), saved.stat().st_mode & 0o777), (PASSWORD, 0o600))
        self.assertEqual(self.fake.made()[0][2], '/.well-known/caldav')
        self.assert_secret_kept(json.dumps(account), json.dumps(self.config), ui.lines)

    def test_other_calendar_with_its_server_and_one_calendar(self):
        account = {'id': 'acme-caldav', 'service': 'caldav', 'boundary': 'work:Acme'}
        ui = FakeUI({'Email address': USER, 'CalDAV server': 'caldav.acme.test', 'Only this calendar': 'family'}, PASSWORD)
        calendar_setup.step(self.config, account, ui)
        self.assertEqual((account['caldav_url'], account['calendar_name']), ('https://caldav.acme.test/', 'family'))
        self.assertEqual(ui.lines[0], '  Family found')
        self.config['accounts'] = [account]
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account), {'Dentist': 1})
        with self.assertRaises(onboarding.SetupError) as caught:
            calendar_setup.step(self.config, {'id': 'x', 'service': 'caldav'},
                                FakeUI({'Email address': USER, 'CalDAV server': 'caldav.acme.test', 'Only this calendar': 'Gym'}, PASSWORD))
        self.assertEqual(caught.exception.message, 'Couldn’t find a calendar with that name')

    def test_tls_is_always_verified(self):
        account = {'id': 'x', 'service': 'caldav', 'email': USER, 'caldav_url': 'https://caldav.acme.test/'}
        with mock.patch.object(caldav_calendar, 'tls_context', ssl.create_default_context):  # the fake certificate isn't trusted
            with self.assertRaises(CalendarError) as caught:
                caldav_calendar.check(account, PASSWORD)
        self.assertEqual(caught.exception.category, 'caldav_tls_failed')
        self.assertEqual(caldav_calendar.tls_context().verify_mode, ssl.CERT_REQUIRED)
        with self.assertRaises(CalendarError) as caught:
            caldav_calendar.https_url('http://caldav.acme.test/')
        self.assertEqual(caught.exception.category, 'calendar_plaintext_refused')
        self.assertFalse(self.fake.made())


class CalendarLink(Base):
    def link(self, name=LINK_KEY):
        return f'webcal://feeds.acme.test/cal/{name}.ics'

    def test_window_then_a_polite_poll_then_a_change(self):
        account = self.account('acme-proton', 'proton_calendar', self.link())
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account), {'Team sync': 4, 'Team sync (moved)': 1})
        moved = next(r for r in self.events(account) if r['title'] == 'Team sync (moved)')
        self.assertEqual(moved['occurred_at'], (self.fake.team + dt.timedelta(days=7)).replace(hour=11).astimezone(dt.timezone.utc).isoformat())
        self.assertEqual(len(self.fake.made('feeds.acme.test')), 1)
        # asked a moment ago: not asked again
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(len(self.fake.made('feeds.acme.test')), 1)
        # later: asked with its ETag, and unchanged costs a 304
        ics_feed._seen[account['id']]['at'] -= ics_feed.POLL_SECONDS + 1
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['mode'], 'incremental')
        last = self.fake.made('feeds.acme.test')[-1]
        self.assertEqual((last[3].get('If-None-Match'), last[3].get('If-Modified-Since')), ('"v1"', 'Mon, 02 Nov 2026 08:00:00 GMT'))
        # the series is cut short: read again, the later meetings gone
        self.fake.feed_events[0] = self.fake.feed_events[0].replace('COUNT=6', 'COUNT=2')
        self.fake.feed_etag = '"v2"'
        ics_feed._seen[account['id']]['at'] -= ics_feed.POLL_SECONDS + 1
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['mode'], 'resync')
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account), {'Team sync': 1, 'Team sync (moved)': 1})
        self.assertEqual(self.titles(account, deleted=1), {'Team sync': 3})
        # the link stops working: a fixed label, without the link
        self.fake.feed_status = 404
        ics_feed._seen[account['id']]['at'] -= ics_feed.POLL_SECONDS + 1
        with self.assertRaises(sources.SourceError) as caught:
            a.sync_calendar(self.store, self.config, account)
        self.assertIn('ics_gone', str(caught.exception))
        self.assert_secret_kept(caught.exception, repr(caught.exception), json.dumps(self.config))

    def test_setup_checks_the_link_and_keeps_it_as_a_secret(self):
        account = {'id': 'acme-ics', 'service': 'ics', 'boundary': 'work:Acme'}
        ui = FakeUI({}, self.link())
        calendar_setup.step(self.config, account, ui)
        saved = Path(self.config['credentials'][account['credential']])
        self.assertEqual(saved.read_text().strip(), f'https://feeds.acme.test/cal/{LINK_KEY}.ics')
        self.assertEqual(saved.stat().st_mode & 0o777, 0o600)
        self.assertEqual(ui.lines, ['  calendar found', '  saved the link'])
        for name, message in (('page', 'That link doesn’t open a calendar'), ('nothing', 'That link doesn’t open a calendar'),
                              ('away', 'The server sent the sign-in somewhere else'), ('plain', 'The server sent the sign-in somewhere else')):
            with self.subTest(name), self.assertRaises(onboarding.SetupError) as caught:
                calendar_setup.step(self.config, {'id': 'acme-' + name, 'service': 'ics'}, FakeUI({}, self.link(name)))
            self.assertEqual(caught.exception.message, message)
        self.assertFalse([r for r in self.fake.requests if r[0] != 'feeds.acme.test'])  # never followed elsewhere
        self.assert_secret_kept(json.dumps(account), json.dumps(self.config), ui.lines)

    def test_tls_is_always_verified(self):
        with mock.patch.object(caldav_calendar, 'tls_context', ssl.create_default_context):
            with self.assertRaises(CalendarError) as caught:
                ics_feed.check(self.link())
        self.assertEqual(caught.exception.category, 'ics_tls_failed')
        self.assert_secret_kept(caught.exception, repr(caught.exception))


class Exchange(Base):
    def test_window_in_pages_then_nothing_new_then_a_removal(self):
        account = self.account('acme-ews', 'exchange', PASSWORD, username='ACME\\alex', ews_url='https://mail.acme.test/EWS/Exchange.asmx')
        a.sync_calendar(self.store, self.config, account)  # the first month
        self.assertEqual(self.titles(account), {'Weekly 1:1': 2, 'Quarterly plan': 1})
        self.assertEqual(self.store.checkpoint(account['id'])['mode'], 'bootstrap')
        a.sync_calendar(self.store, self.config, account)  # the rest
        self.assertEqual(self.titles(account), {'Weekly 1:1': 2, 'Quarterly plan': 1, 'Offsite': 1})
        state = self.store.checkpoint(account['id'])
        self.assertEqual((state['mode'], state['sync_token']), ('incremental', 'state-1'))
        plan = next(r for r in self.events(account) if r['title'] == 'Quarterly plan')['metadata']
        people = {p['email']: p for p in plan['attendees']}
        self.assertEqual(people[USER]['responseStatus'], 'accepted')  # what the owner answered
        self.assertTrue(people[USER]['self'])
        self.assertEqual(people['cy@client.test']['responseStatus'], 'accepted')
        self.assertTrue(people['room4@acme.test']['resource'])
        ones = [r for r in self.events(account) if r['title'] == 'Weekly 1:1']
        self.assertEqual(len({r['source_id'] for r in ones}), 2)
        self.assertEqual({r['metadata']['recurring_event_id'] for r in ones}, {ical.event_id('oneone@acme.test', 'ews')})
        # nothing changed
        finds = len([r for r in self.fake.requests if '<m:FindItem' in r[4]])
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['events'], 0)
        self.assertEqual(len([r for r in self.fake.requests if '<m:FindItem' in r[4]]), finds)
        # the plan is removed: read again, gone here too
        del self.fake.items['AAMk-plan']
        self.fake.version += 1
        self.fake.known_states.add('state-2')
        self.assertEqual(a.sync_calendar(self.store, self.config, account)['mode'], 'resync')
        a.sync_calendar(self.store, self.config, account)
        a.sync_calendar(self.store, self.config, account)
        self.assertEqual(self.titles(account, deleted=1), {'Quarterly plan': 1})
        self.assertEqual(self.store.checkpoint(account['id'])['sync_token'], 'state-2')
        self.assertFalse(self.fake.basic_used)  # NTLM: the password itself never went over the wire
        bodies = ' '.join(r[4] for r in self.fake.requests)
        for write in ('CreateItem', 'UpdateItem', 'DeleteItem', 'SendItem'):
            self.assertNotIn(write, bodies)
        self.assert_secret_kept(json.dumps(self.config))

    def test_a_lost_sync_state_reads_the_window_again(self):
        account = self.account('acme-ews', 'exchange', PASSWORD, username='ACME\\alex', ews_url='https://mail.acme.test/EWS/Exchange.asmx')
        with self.assertRaises(CalendarError) as caught:
            ews_calendar.calendar_call(self.config, sources.credential, account, 'events.list', {'syncToken': 'state-lost'})
        self.assertEqual(caught.exception.status, 410)

    def test_setup_finds_the_server_and_signs_in_with_ntlm(self):
        account = {'id': 'acme-ews', 'service': 'exchange', 'boundary': 'work:Acme'}
        ui = FakeUI({'Email address': USER, 'Username (DOMAIN\\name)': 'ACME\\alex'}, PASSWORD)
        calendar_setup.step(self.config, account, ui)
        self.assertEqual((account['ews_url'], account['ews_auth'], account['username']),
                         ('https://mail.acme.test/EWS/Exchange.asmx', 'ntlm', 'ACME\\alex'))
        self.assertEqual(ui.lines, ['  calendar found', '  signed in'])
        with self.assertRaises(onboarding.SetupError) as caught:
            calendar_setup.step(self.config, {'id': 'x', 'service': 'exchange'},
                                FakeUI({'Email address': USER, 'Username (DOMAIN\\name)': 'ACME\\alex'}, 'pw-Wrong-0000'))
        self.assertEqual(caught.exception.message, 'The server refused the username or password')
        self.assertIn('DOMAIN', caught.exception.fix)
        self.assertFalse(self.fake.basic_used)
        self.assert_secret_kept(json.dumps(account), json.dumps(self.config), ui.lines)

    def test_a_server_with_only_basic_sign_in(self):
        account = {'email': USER, 'username': 'ACME\\alex', 'ews_url': ews_calendar.server_url('basic.acme.test')}
        self.assertEqual(ews_calendar.check(account, PASSWORD), ('https://basic.acme.test/EWS/Exchange.asmx', 'basic'))

    def test_microsoft_365_goes_to_outlook_calendar(self):
        account = {'id': 'x', 'service': 'exchange', 'boundary': 'work:Acme'}
        with self.assertRaises(onboarding.SetupError) as caught:
            calendar_setup.step(self.config, account, FakeUI({'Email address': 'alex@cloudco.test'}, PASSWORD))
        self.assertEqual(caught.exception.message, 'This is a Microsoft 365 mailbox')
        self.assertIn('Outlook Calendar', caught.exception.fix)
        self.assertNotIn(account.get('credential'), self.config['credentials'])  # asked nothing, saved nothing
        with self.assertRaises(CalendarError) as caught:  # its own autodiscover points there too
            ews_calendar.autodiscover('alex@cloudco.test', 'alex@cloudco.test', PASSWORD)
        self.assertEqual(caught.exception.category, 'exchange_online')
        self.assertFalse([r for r in self.fake.requests if r[1] == 'POST'])  # the password went nowhere

    def test_tls_is_always_verified(self):
        account = {'email': USER, 'username': 'ACME\\alex', 'ews_url': 'https://mail.acme.test/EWS/Exchange.asmx'}
        with mock.patch.object(caldav_calendar, 'tls_context', ssl.create_default_context):
            with self.assertRaises(CalendarError) as caught:
                ews_calendar.check(account, PASSWORD)
        self.assertEqual(caught.exception.category, 'ews_tls_failed')


class Pieces(unittest.TestCase):
    def test_md4(self):
        self.assertEqual(ews_calendar.md4(b'').hex(), '31d6cfe0d16ae931b73c59d7e0c089c0')
        self.assertEqual(ews_calendar.md4(b'abc').hex(), 'a448017aaf21d8525fc10ae87aa6729d')
        self.assertEqual(ews_calendar.md4(b'1234567890' * 8).hex(), 'e33b4ddc9c38f2199c3e7b164fcc0536')

    def test_recurrence_zones_and_changed_occurrences(self):
        text = vcal(
            'BEGIN:VTIMEZONE\r\nTZID:Custom Zone\r\nBEGIN:STANDARD\r\nTZOFFSETFROM:+0200\r\nTZOFFSETTO:+0100\r\n'
            'DTSTART:19701025T030000\r\nEND:STANDARD\r\nEND:VTIMEZONE\r\n',
            vevent('w@x.test', 'Stand-up', ['DTSTART;TZID=Europe/Brussels:20261019T100000', 'DTEND;TZID=Europe/Brussels:20261019T103000',
                                            'RRULE:FREQ=WEEKLY;BYDAY=MO,WE;COUNT=6', 'EXDATE;TZID=Europe/Brussels:20261021T100000']),
            vevent('w@x.test', 'Stand-up (moved)', ['RECURRENCE-ID;TZID=Europe/Brussels:20261026T100000',
                                                    'DTSTART;TZID=Europe/Brussels:20261026T140000', 'DTEND;TZID=Europe/Brussels:20261026T143000']),
            vevent('m@x.test', 'Last Friday', ['DTSTART;TZID=Custom Zone:20261001T090000', 'DURATION:PT1H',
                                               'RRULE:FREQ=MONTHLY;BYDAY=-1FR;UNTIL=20261231T000000Z']),
            vevent('z@x.test', 'Windows zone', ['DTSTART;TZID=W. Europe Standard Time:20261102T100000', 'DURATION:PT1H']),
            vevent('d@x.test', 'Holiday', ['DTSTART;VALUE=DATE:20261101', 'DTEND;VALUE=DATE:20261102']))
        items, skipped = ical.window_items([text], dt.datetime(2026, 10, 18, tzinfo=dt.timezone.utc),
                                           dt.datetime(2027, 1, 30, tzinfo=dt.timezone.utc))
        starts = sorted((i['summary'], i['start'].get('dateTime') or i['start']['date']) for i in items)
        utc_of = lambda s: dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc).strftime('%m-%d %H:%M')  # noqa: E731
        self.assertEqual([(n, utc_of(s)) for n, s in starts if n.startswith('Stand-up')],
                         [('Stand-up', '10-19 08:00'), ('Stand-up', '10-28 09:00'), ('Stand-up', '11-02 09:00'),
                          ('Stand-up', '11-04 09:00'), ('Stand-up (moved)', '10-26 13:00')])  # summer, then winter time
        self.assertEqual([utc_of(s) for n, s in starts if n == 'Last Friday'], ['10-30 08:00', '11-27 08:00', '12-25 08:00'])
        self.assertEqual([utc_of(s) for n, s in starts if n == 'Windows zone'], ['11-02 09:00'])
        self.assertIn(('Holiday', '2026-11-01'), starts)
        self.assertEqual(skipped, 0)
        moved = next(i for i in items if i['summary'] == 'Stand-up (moved)')
        self.assertEqual(moved['recurringEventId'], ical.event_id('w@x.test'))

    def test_every_one_says_read_only(self):
        for service in calendar_setup.SERVICES:
            self.assertTrue(calendar_setup.WHAT[service].endswith('Read-only.'), service)
            self.assertLessEqual(len(calendar_setup.WHAT[service]), 80)

    def test_xml_with_entities_is_never_read(self):
        with self.assertRaises(CalendarError):
            caldav_calendar.parse_xml('<!DOCTYPE x [<!ENTITY a "aaaa">]><d:multistatus xmlns:d="DAV:">&a;</d:multistatus>')


if __name__ == '__main__':
    unittest.main()

"""Any mailbox over IMAP (imap_mail.py, imap_presets.py, machine/sources/imap_setup.py): read-only, in Gmail's shapes, through the
same sync. A fake IMAP server on this computer (TLS with a throwaway certificate, or STARTTLS) holds made-up mail; no
other server is reached and nothing is ever sent. The password never shows in a log, an error, the config or the lines
the dashboard shows."""
import base64
import datetime as dt
import email
import email.policy
import json
import logging
import re
import shutil
import socket
import socketserver
import ssl
import subprocess
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import imap_mail
import imap_presets
import onboarding
import smtp_mail
import sources
from machine import config as machine_config
from machine.sources import imap_setup
from test_ux import a

PASSWORD = 'pw-Fake-7731-xyz'  # made up; the tests look for it everywhere it must not be
USER = 'alex@acme.test'
TELENET_USER = 'bo@telenet.be'


def when(days_ago=1, hour=8):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_ago)).replace(hour=hour, minute=0, second=0, microsecond=0)


def mime(subject, sender, to, body, message_id, at, reply_to=None):
    head = (f'From: {sender}\r\nTo: {to}\r\nSubject: {subject}\r\nMessage-ID: {message_id}\r\n'
            f'Date: {email.utils.format_datetime(at)}\r\n')
    if reply_to:
        head += f'In-Reply-To: {reply_to}\r\nReferences: {reply_to}\r\n'
    return (head + f'Content-Type: text/plain; charset=utf-8\r\n\r\n{body}\r\n').encode()


class Folder:
    def __init__(self, validity, flags=''):
        self.validity, self.flags, self.messages, self.next = validity, flags, {}, 1

    def add(self, data, at, flags=()):
        uid = self.next
        self.messages[uid] = {'mime': data, 'at': at, 'flags': list(flags)}
        self.next += 1
        return uid


TOKEN = re.compile(rb'\(|\)|"(?:[^"\\]|\\.)*"|\[[^\]]*\](?:<[\d.]+>)?|[^\s()\[]+(?:\[[^\]]*\](?:<[\d.]+>)?)?')


def tokens(line):
    return [t[1:-1].replace(b'\\"', b'"').replace(b'\\\\', b'\\') if t.startswith(b'"') else t for t in TOKEN.findall(line)]


def imap_day(text):
    return dt.datetime.strptime(text.decode(), '%d-%b-%Y').replace(tzinfo=dt.timezone.utc)


class FakeImap(socketserver.ThreadingTCPServer):
    """A small IMAP4rev1 server: LOGIN / AUTHENTICATE PLAIN, LIST, EXAMINE, UID SEARCH, UID FETCH, APPEND, NOOP, LOGOUT.
    mode: 'ssl' (TLS from the first byte), 'starttls', 'plain' (no STARTTLS on offer) or 'silent' (never greets)."""
    daemon_threads = allow_reuse_address = True

    def __init__(self, mode, cert, users):
        super().__init__(('127.0.0.1', 0), Handler)
        self.mode, self.users, self.commands, self.refuse = mode, users, [], None
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(*cert)
        self.folders = {'INBOX': Folder(1700000000), 'Sent': Folder(1700000001, '\\Sent')}
        self.logins = 0
        threading.Thread(target=self.serve_forever, daemon=True).start()

    @property
    def port(self):
        return self.server_address[1]


class Handler(socketserver.StreamRequestHandler):
    def setup(self):
        if self.server.mode == 'ssl':
            self.request = self.server.context.wrap_socket(self.request, server_side=True)
        super().setup()
        self.tls, self.user, self.folder = self.server.mode == 'ssl', None, None

    def finish(self):
        try:
            super().finish()
        finally:
            self.request.close()

    def send(self, data):
        self.wfile.write(data if isinstance(data, bytes) else data.encode())
        self.wfile.flush()

    def capabilities(self):
        caps = ['IMAP4rev1', 'AUTH=PLAIN', 'SPECIAL-USE']
        if self.server.mode == 'starttls' and not self.tls:
            caps.append('STARTTLS')
        return ' '.join(caps)

    def handle(self):
        if self.server.mode == 'silent':
            time.sleep(3)
            return
        self.send(f'* OK [CAPABILITY {self.capabilities()}] fake ready\r\n')
        while True:
            line = self.rfile.readline()
            if not line:
                return
            literal = re.search(rb'\{(\d+)\}\r\n$', line)
            if literal and line.split(b' ')[1:2] == [b'APPEND']:  # a message: kept as it came
                self.send('+ go on\r\n')
                data = self.rfile.read(int(literal[1]))
                self.rfile.readline()
                self.server.commands.append(('APPEND', self.tls))
                self.do_APPEND(line.split(b' ')[0].decode(), line[:literal.start()], data)
                continue
            if literal:  # a literal argument: say go on, then read it and the rest of the line
                self.send('+ go on\r\n')
                line = line[:literal.start()] + b' "' + self.rfile.read(int(literal[1])) + b'"' + self.rfile.readline()
            parts = line.rstrip(b'\r\n').split(b' ', 2)
            tag, verb, rest = parts[0].decode(), parts[1].upper().decode() if len(parts) > 1 else '', parts[2] if len(parts) > 2 else b''
            self.server.commands.append((verb, self.tls))
            if verb == 'UID':
                sub, _, rest = rest.partition(b' ')
                verb = 'UID ' + sub.upper().decode()
            try:
                if getattr(self, 'do_' + verb.replace(' ', '_'), None) is None:
                    self.send(f'{tag} BAD unknown command\r\n')
                elif getattr(self, 'do_' + verb.replace(' ', '_'))(tag, rest) == 'bye':
                    return
            except (ssl.SSLError, OSError):
                return

    def do_CAPABILITY(self, tag, rest):
        self.send(f'* CAPABILITY {self.capabilities()}\r\n{tag} OK done\r\n')

    def do_NOOP(self, tag, rest):
        self.send(f'{tag} OK done\r\n')

    def do_LOGOUT(self, tag, rest):
        self.send(f'* BYE bye\r\n{tag} OK done\r\n')
        return 'bye'

    def do_STARTTLS(self, tag, rest):
        if self.server.mode != 'starttls':
            self.send(f'{tag} BAD no TLS here\r\n')
            return
        self.send(f'{tag} OK begin TLS\r\n')
        self.request = self.server.context.wrap_socket(self.request, server_side=True)
        self.rfile, self.wfile = self.request.makefile('rb'), self.request.makefile('wb')
        self.tls = True

    def signed_in(self, tag, user, password):
        self.server.logins += 1
        if self.server.refuse == 'throttle':
            self.send(f'{tag} NO [LIMIT] too many logins, slow down\r\n')
        elif self.server.refuse == 'unavailable':
            self.send(f'{tag} NO [UNAVAILABLE] try again later\r\n')
        elif self.server.users.get(user) == password:
            self.user = user
            self.send(f'{tag} OK signed in\r\n')
        else:
            self.send(f'{tag} NO [AUTHENTICATIONFAILED] invalid credentials\r\n')

    def do_LOGIN(self, tag, rest):
        user, password = [t.decode() for t in tokens(rest)[:2]]
        self.signed_in(tag, user, password)

    def do_AUTHENTICATE(self, tag, rest):
        self.send('+ \r\n')
        _, user, password = base64.b64decode(self.rfile.readline().strip()).split(b'\0')
        self.signed_in(tag, user.decode(), password.decode())

    def do_LIST(self, tag, rest):
        for name, folder in self.server.folders.items():
            self.send(f'* LIST (\\HasNoChildren{" " + folder.flags if folder.flags else ""}) "/" "{name}"\r\n')
        self.send(f'{tag} OK done\r\n')

    def do_APPEND(self, tag, head, data):
        folder = self.server.folders.get(tokens(head)[2].decode())
        if not self.user or folder is None:
            self.send(f'{tag} NO no such folder\r\n')
            return
        uid = folder.add(data, dt.datetime.now(dt.timezone.utc), ['\\Seen'])
        self.send(f'{tag} OK [APPENDUID {folder.validity} {uid}] appended\r\n')

    def do_SELECT(self, tag, rest):
        self.send(f'{tag} NO read-only, please\r\n')  # the Machine only ever EXAMINEs

    def do_EXAMINE(self, tag, rest):
        name = tokens(rest)[0].decode()
        folder = self.server.folders.get(name)
        if not self.user or folder is None:
            self.folder = None
            self.send(f'{tag} NO no such folder\r\n')
            return
        self.folder = folder
        self.send(f'* FLAGS (\\Seen \\Draft)\r\n* {len(folder.messages)} EXISTS\r\n* OK [UIDVALIDITY {folder.validity}] ok\r\n'
                  f'* OK [UIDNEXT {folder.next}] ok\r\n{tag} OK [READ-ONLY] examined\r\n')

    def uid_set(self, text):
        top = max(self.folder.messages, default=0)
        found = set()
        for part in text.decode().split(','):
            low, _, high = part.partition(':')
            low = top if low == '*' else int(low)
            high = low if not high else (top if high == '*' else int(high))
            low, high = min(low, high), max(low, high)
            found |= {u for u in self.folder.messages if low <= u <= high}
            if high == top and low > top and top:  # n:* with n past the newest: the newest, as RFC 3501 says
                found.add(top)
        return sorted(found)

    def do_UID_SEARCH(self, tag, rest):
        parts, uids = tokens(rest), set(self.folder.messages)
        i = 0
        while i < len(parts):
            word = parts[i].upper()
            if word == b'CHARSET':
                i += 2
                continue
            if word == b'UID':
                uids &= set(self.uid_set(parts[i + 1]))
                i += 2
                continue
            if word in (b'SINCE', b'BEFORE'):
                day = imap_day(parts[i + 1])
                keep = {u for u in uids if (self.folder.messages[u]['at'].date() >= day.date()) == (word == b'SINCE')}
                uids &= keep
                i += 2
                continue
            if word == b'HEADER':
                name, value = parts[i + 1].decode(), parts[i + 2].decode().lower()
                uids &= {u for u in uids if value in (email.message_from_bytes(self.folder.messages[u]['mime']).get(name) or '').lower()}
                i += 3
                continue
            if word in (b'FROM', b'TO', b'SUBJECT', b'CC', b'TEXT'):
                value = parts[i + 1].decode().lower()
                def has(u):
                    message = email.message_from_bytes(self.folder.messages[u]['mime'], policy=email.policy.default)
                    if word == b'TEXT':
                        return value in self.folder.messages[u]['mime'].decode('utf-8', 'replace').lower()
                    return value in str(message.get(word.decode()) or '').lower()
                uids &= {u for u in uids if has(u)}
                i += 2
                continue
            i += 1
        self.send(f'* SEARCH {" ".join(map(str, sorted(uids)))}\r\n{tag} OK done\r\n'.replace('SEARCH \r\n', 'SEARCH\r\n'))

    def do_UID_FETCH(self, tag, rest):
        which, _, items = rest.partition(b' ')
        items = items.decode()
        for seq, uid in enumerate(self.uid_set(which), 1):
            message = self.folder.messages[uid]
            out = [f'UID {uid}'.encode()]
            if 'FLAGS' in items.replace('HEADER.FIELDS', ''):
                out.append(f'FLAGS ({" ".join(message["flags"])})'.encode())
            if 'INTERNALDATE' in items:
                out.append(b'INTERNALDATE "' + message['at'].strftime('%d-%b-%Y %H:%M:%S +0000').encode() + b'"')
            if 'RFC822.SIZE' in items:
                out.append(f'RFC822.SIZE {len(message["mime"])}'.encode())
            for section in re.findall(r'BODY\.PEEK\[([^\]]*)\](?:<[\d.]+>)?', items):
                head, _, body = message['mime'].partition(b'\r\n\r\n')
                if section == '':
                    data = message['mime']
                elif section == 'HEADER':
                    data = head + b'\r\n\r\n'
                elif section == 'TEXT':
                    data = body
                else:
                    wanted = re.findall(r'[\w-]+', section.split('(', 1)[1].upper())
                    data = b''.join(line + b'\r\n' for line in head.split(b'\r\n')
                                    if line.split(b':')[0].decode().upper() in wanted) + b'\r\n'
                out.append(f'BODY[{section}] {{{len(data)}}}\r\n'.encode() + data)
            self.send(f'* {seq} FETCH ('.encode() + b' '.join(out) + b')\r\n')
        self.send(f'{tag} OK done\r\n')


def certificate(folder):
    key, cert = Path(folder) / 'key.pem', Path(folder) / 'cert.pem'
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', str(key), '-out', str(cert),
                    '-days', '1', '-subj', '/CN=localhost'], check=True, capture_output=True)
    return str(cert), str(key)


@unittest.skipUnless(shutil.which('openssl'), 'needs openssl')
class Base(unittest.TestCase):
    mode = 'ssl'

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
        self.server = FakeImap(self.mode, self.cert, {USER: PASSWORD, TELENET_USER: PASSWORD})
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.addCleanup(lambda: [imap_mail.forget({'id': key[0]}) for key in list(imap_mail._sessions)])
        secret = Path(self.temp.name) / 'imap-acme-imap'
        secret.write_text(PASSWORD + '\n')
        self.account = {'id': 'acme-imap', 'service': 'imap', 'transport': 'imap', 'email': USER, 'boundary': 'work:Acme',
                        'imap_host': '127.0.0.1', 'imap_port': self.server.port, 'imap_security': self.mode,
                        'username': USER, 'credential': 'imap-acme-imap'}
        self.config = {'credentials': {'imap-acme-imap': str(secret)}, 'accounts': [self.account], 'bootstrap_days': 7,
                       'database': str(Path(self.temp.name) / 'events.sqlite'), 'data_dir': self.temp.name}
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

    def rows(self):
        with self.store.connect() as db:
            return {r['source_id']: r for r in db.execute("SELECT * FROM events WHERE kind='gmail.message'")}

    def assert_no_password(self, *texts):
        for text in [*texts, *self.logs]:
            self.assertNotIn(PASSWORD, str(text))
        if Path(self.config['database']).exists():
            self.assertNotIn(PASSWORD.encode(), Path(self.config['database']).read_bytes())


class Sync(Base):
    def test_bootstrap_then_new_mail_in_both_folders_read_only(self):
        inbox, sent = self.server.folders['INBOX'], self.server.folders['Sent']
        inbox.add(mime('Quote', 'Bo <bo@client.test>', USER, 'Café at 10?', '<q1@client.test>', when(2)), when(2))
        inbox.add(mime('Old', 'Cy <cy@client.test>', USER, 'From long ago', '<o1@client.test>', when(40)), when(40), ['\\Seen'])
        a.sync_gmail(self.store, self.config, self.account)  # bootstrap: the last 7 days
        rows = self.rows()
        self.assertEqual(list(rows), ['i1700000000-1'])
        first = json.loads(rows['i1700000000-1']['metadata'])
        self.assertIn('Café at 10?', rows['i1700000000-1']['body'])
        self.assertEqual(first['labels'], ['INBOX', 'UNREAD'])
        self.assertEqual(first['message-id'], '<q1@client.test>')
        self.assertIsNone(first.get('source_url'))
        self.assertEqual(self.store.checkpoint('acme-imap')['mode'], 'incremental')
        # A reply sent from another mail app and a new message: the next sync reads just those
        sent.add(mime('Re: Quote', USER, 'bo@client.test', 'Yes, 10 works', '<r1@acme.test>', when(0), reply_to='<q1@client.test>'), when(0), ['\\Seen'])
        inbox.add(mime('Lunch', 'Di <di@client.test>', USER, 'Lunch Friday?', '<l1@client.test>', when(0)), when(0), ['\\Seen'])
        a.sync_gmail(self.store, self.config, self.account)
        rows = self.rows()
        self.assertEqual(set(rows), {'i1700000000-1', 'i1700000000-3', 's1700000001-1'})
        reply = json.loads(rows['s1700000001-1']['metadata'])
        self.assertEqual(reply['labels'], ['SENT'])
        self.assertEqual(reply['thread_id'], first['thread_id'])  # a reply joins its conversation
        self.assertEqual(json.loads(rows['i1700000000-3']['metadata'])['labels'], ['INBOX'])
        cursor = self.store.checkpoint('acme-imap')['history_id']
        self.assertEqual(cursor, 'imap1:i1700000000.4:s1700000001.2')
        # Nothing new: nothing read again, the cursor stays
        a.sync_gmail(self.store, self.config, self.account)
        self.assertEqual(self.store.checkpoint('acme-imap')['history_id'], cursor)
        verbs = {v for v, _ in self.server.commands}
        self.assertNotIn('SELECT', verbs)  # read-only: EXAMINE, never SELECT
        self.assertFalse(verbs & {'STORE', 'APPEND', 'EXPUNGE', 'COPY', 'MOVE', 'UID STORE'})
        self.assertTrue(all(tls for _, tls in self.server.commands))
        self.assertEqual(self.server.logins, 1)  # one connection, kept between reads
        self.assert_no_password()

    def test_a_renumbered_folder_reads_the_window_again(self):
        inbox = self.server.folders['INBOX']
        inbox.add(mime('Quote', 'Bo <bo@client.test>', USER, 'Hi', '<q1@client.test>', when(1)), when(1))
        a.sync_gmail(self.store, self.config, self.account)
        self.assertEqual(set(self.rows()), {'i1700000000-1'})
        inbox.validity = 1800000000  # UIDVALIDITY changed: every UID it had is gone
        self.assertEqual(a.sync_gmail(self.store, self.config, self.account)['mode'], 'resync')
        self.assertEqual(self.store.checkpoint('acme-imap')['resync_reason'], 'expired_history')
        a.sync_gmail(self.store, self.config, self.account)
        self.assertIn('i1800000000-1', self.rows())
        self.assertEqual(self.store.checkpoint('acme-imap')['mode'], 'incremental')

    def test_more_new_mail_than_a_page_comes_in_pages(self):
        inbox = self.server.folders['INBOX']
        a.sync_gmail(self.store, self.config, self.account)  # an empty mailbox
        for n in range(5):
            inbox.add(mime(f'N{n}', 'Bo <bo@client.test>', USER, 'x', f'<n{n}@client.test>', when(0)), when(0))
        session = imap_mail._Use(self.config, sources.credential, self.account)
        with session as live:
            start = 'imap1:i1700000000.1:s1700000001.1'
            page, more = imap_mail.history(live, self.account, start, 2)
            self.assertTrue(more)
            self.assertEqual([h['messagesAdded'][0]['message']['id'] for h in page['history']], ['i1700000000-1', 'i1700000000-2'])
            page, more = imap_mail.history(live, self.account, page['historyId'], 10)
            self.assertFalse(more)
            self.assertEqual(len(page['history']), 3)
            self.assertEqual(page['historyId'], 'imap1:i1700000000.6:s1700000001.1')
            # n:* past the newest UID still answers the newest one (RFC 3501): never read twice
            page, _ = imap_mail.history(live, self.account, page['historyId'], 10)
            self.assertEqual(page['history'], [])

    def test_history_import_searches_by_date_and_words(self):
        inbox, sent = self.server.folders['INBOX'], self.server.folders['Sent']
        inbox.add(mime('Quote', 'Bo <bo@client.test>', USER, 'pricing', '<q1@client.test>', when(20)), when(20))
        inbox.add(mime('Other', 'Cy <cy@client.test>', USER, 'hello', '<o1@client.test>', when(3)), when(3))
        sent.add(mime('Re: Quote', USER, 'bo@client.test', 'pricing ok', '<r1@acme.test>', when(19)), when(19))
        call = lambda q, **more: sources.gog_read(self.config, self.account, 'gmail', 'v1', 'gmail.users.messages.list',
                                                  {'q': q, **more}, '')
        after = int(when(30).timestamp())
        found = call(f'after:{after}')
        self.assertEqual([m['id'] for m in found['messages']], ['i1700000000-2', 's1700000001-1', 'i1700000000-1'])  # newest first
        self.assertEqual([m['id'] for m in call(f'after:{after}', maxResults=2)['messages']], ['i1700000000-2', 's1700000001-1'])
        self.assertEqual(call(f'after:{after}', maxResults=2)['nextPageToken'], '2')
        self.assertEqual([m['id'] for m in call('in:sent pricing')['messages']], ['s1700000001-1'])
        self.assertEqual([m['id'] for m in call('rfc822msgid:<o1@client.test>')['messages']], ['i1700000000-2'])
        self.assertEqual([m['id'] for m in call(f'before:{int(when(10).timestamp())} after:{after}')['messages']],
                         ['s1700000001-1', 'i1700000000-1'])
        thread_id = sources.gog_read(self.config, self.account, 'gmail', 'v1', 'gmail.users.messages.get',
                                     {'id': 'i1700000000-1', 'format': 'minimal'}, '')['threadId']
        thread = sources.gog_read(self.config, self.account, 'gmail', 'v1', 'gmail.users.threads.get', {'id': thread_id}, '')
        self.assertEqual([m['id'] for m in thread['messages']], ['i1700000000-1'])

    def test_a_message_gone_or_from_another_numbering_is_404(self):
        for message_id in ('i1700000000-9', 'i1600000000-1', 'nonsense'):
            with self.assertRaises(sources.SourceError) as caught:
                sources.gog_read(self.config, self.account, 'gmail', 'v1', 'gmail.users.messages.get', {'id': message_id}, '')
            self.assertEqual(caught.exception.status, 404)


class StartTls(Base):
    mode = 'starttls'

    def test_starttls_before_the_password(self):
        self.server.folders['INBOX'].add(mime('Hi', 'Bo <bo@client.test>', USER, 'x', '<h1@client.test>', when(1)), when(1))
        self.assertEqual(imap_mail.check(self.config, sources.credential, self.account), 'Sent')
        login = next(tls for verb, tls in self.server.commands if verb == 'LOGIN')
        self.assertTrue(login)  # the password only ever went over TLS


class Plain(Base):
    mode = 'plain'

    def test_a_server_without_tls_is_never_sent_the_password(self):
        self.account['imap_security'] = 'starttls'
        with self.assertRaises(imap_mail.ImapError) as caught:
            imap_mail.check(self.config, sources.credential, self.account)
        self.assertEqual(caught.exception.category, 'imap_tls_failed')
        self.assertNotIn('LOGIN', [v for v, _ in self.server.commands])
        self.assertEqual(self.server.logins, 0)
        self.account['imap_security'] = 'ssl'  # TLS expected, plain text answered
        with self.assertRaises(imap_mail.ImapError) as caught:
            imap_mail.check(self.config, sources.credential, self.account)
        self.assertEqual(caught.exception.category, 'imap_tls_failed')
        for plaintext in ('none', 'plain', ''):
            self.account['imap_security'] = plaintext or 'plaintext'
            with self.assertRaises(imap_mail.ImapError) as caught:
                imap_mail.settings(self.account)
            self.assertEqual(caught.exception.category, 'imap_plaintext_refused')


class Errors(Base):
    def check(self, **change):
        account = {**self.account, **change}
        with self.assertRaises(sources.SourceError) as caught:
            sources.gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.getProfile', {}, '')
        self.assert_no_password(caught.exception, repr(caught.exception), caught.exception.args)
        return caught.exception

    def test_each_failure_is_a_fixed_label(self):
        Path(self.config['credentials']['imap-acme-imap']).write_text('pw-Wrong-0000\n')
        error = self.check()
        self.assertEqual((error.category, error.status), ('imap_auth_failed', 401))
        self.assertRegex(str(error), machine_config.SIGNIN_ERROR)  # shown as "sign in again", not as a broken source
        Path(self.config['credentials']['imap-acme-imap']).write_text(PASSWORD + '\n')
        self.server.refuse = 'throttle'
        self.assertEqual(self.check().category, 'imap_rate_limited')
        self.server.refuse = 'unavailable'
        self.assertEqual(self.check().category, 'imap_unavailable')
        self.server.refuse = None
        free = socket.socket()
        free.bind(('127.0.0.1', 0))
        port = free.getsockname()[1]
        free.close()
        self.assertEqual(self.check(imap_port=port).category, 'imap_unreachable')
        self.assertEqual(self.check(credential='imap-missing').category, 'imap_password_missing')
        self.assertEqual(self.check(imap_host='').category, 'imap_not_configured')
        self.assertEqual(self.check(imap_security='plain').category, 'imap_plaintext_refused')

    def test_a_server_that_never_answers_times_out(self):
        silent = FakeImap('silent', self.cert, {})
        self.addCleanup(silent.server_close)
        self.addCleanup(silent.shutdown)
        with mock.patch.object(imap_mail, 'TIMEOUT', 0.5):
            self.assertEqual(self.check(imap_port=silent.port).category, 'timeout')

    def test_only_a_server_on_this_computer_skips_certificate_checks(self):
        self.assertEqual(imap_mail.tls_context('imap.example.test').verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(imap_mail.tls_context('imap.example.test').check_hostname)
        self.assertEqual(imap_mail.tls_context('127.0.0.1').verify_mode, ssl.CERT_NONE)

    def test_only_reads_are_answered(self):
        for method in ('gmail.users.messages.send', 'gmail.users.messages.modify', 'gmail.users.drafts.create'):
            with self.assertRaises(sources.SourceError) as caught:
                sources.gog_read(self.config, self.account, 'gmail', 'v1', method, {}, '')
            self.assertEqual(caught.exception.category, 'unsupported_gmail_method')
        self.assertEqual(self.server.logins, 0)


class Folders(unittest.TestCase):
    def test_the_sent_folder_by_flag_then_by_name(self):
        rows = [b'(\\HasNoChildren) "/" "INBOX"', b'(\\HasNoChildren \\Sent) "/" "Elsewhere"', b'(\\HasNoChildren) "/" "Sent"']
        self.assertEqual(imap_mail.sent_folder(rows), 'Elsewhere')
        self.assertEqual(imap_mail.sent_folder(rows, 'Sent'), 'Sent')  # the one saved at setup, while it is there
        self.assertEqual(imap_mail.sent_folder([b'(\\HasChildren) "." "INBOX"', b'(\\HasNoChildren) "." "INBOX.Verzonden items"']),
                         'INBOX.Verzonden items')
        self.assertEqual(imap_mail.sent_folder([b'(\\HasNoChildren) "/" "Envoy&AOk-s"']), 'Envoy&AOk-s')
        self.assertEqual(imap_mail.decode_folder('Envoy&AOk-s'), 'Envoyés')
        self.assertIsNone(imap_mail.sent_folder([b'(\\HasNoChildren) "/" "INBOX"', b'(\\Noselect) "/" "Sent"']))

    def test_dates_in_any_language_of_the_computer(self):
        self.assertEqual(imap_mail.internal_date('07-Mar-2026 09:15:00 +0100'),
                         dt.datetime(2026, 3, 7, 8, 15, tzinfo=dt.timezone.utc))
        self.assertEqual(imap_mail.imap_date(dt.datetime(2026, 3, 7)), '07-Mar-2026')

    def test_non_ascii_search_goes_as_a_utf8_literal(self):
        keys, criteria, literal, after, before = imap_mail.parse_query('in:inbox from:"Zoë" after:1800000000')
        self.assertEqual((keys, literal, after), (['i'], ('FROM', 'Zoë'), 1800000000))
        self.assertIn('SINCE', criteria)


class Presets(unittest.TestCase):
    def test_telenet_out_of_the_box(self):
        found = imap_presets.lookup('bo@Telenet.be', network=False)
        self.assertEqual((found['imap_host'], found['imap_port'], found['imap_security']), ('imap.telenet.be', 993, 'ssl'))
        self.assertEqual((found['smtp_host'], found['smtp_port'], found['smtp_security']), ('smtp.telenet.be', 587, 'starttls'))
        self.assertEqual(found['username'], 'bo@telenet.be')

    def test_google_and_microsoft_are_steered_to_their_own_connection(self):
        self.assertEqual(imap_presets.lookup('a@gmail.com', network=False)['oauth'], 'gmail')
        self.assertEqual(imap_presets.lookup('a@hotmail.com', network=False)['oauth'], 'outlook')
        mx = lambda url: json.dumps({'Answer': [{'type': 15, 'data': '1 aspmx.l.google.com.'}]}) if 'dns' in url else None
        self.assertEqual(imap_presets.lookup('a@acme.test', fetch=mx)['oauth'], 'gmail')

    def test_autoconfig_then_mx_as_a_best_effort(self):
        xml = ('<clientConfig><emailProvider id="acme.test"><incomingServer type="imap"><hostname>mail.acme.test</hostname>'
               '<port>993</port><socketType>SSL</socketType><username>%EMAILADDRESS%</username></incomingServer>'
               '<incomingServer type="imap"><hostname>plain.acme.test</hostname><port>143</port><socketType>plain</socketType>'
               '</incomingServer><outgoingServer type="smtp"><hostname>smtp.acme.test</hostname><port>587</port>'
               '<socketType>STARTTLS</socketType><username>%EMAILLOCALPART%</username></outgoingServer></emailProvider></clientConfig>')
        found = imap_presets.lookup('alex@acme.test', fetch=lambda url: xml if 'autoconfig.acme.test' in url else None)
        self.assertEqual((found['imap_host'], found['imap_security'], found['smtp_host'], found['smtp_security']),
                         ('mail.acme.test', 'ssl', 'smtp.acme.test', 'starttls'))
        self.assertEqual(found['username'], 'alex@acme.test')
        plain = xml.replace('<socketType>SSL</socketType>', '<socketType>plain</socketType>')
        self.assertNotEqual((imap_presets.parse_autoconfig(plain, 'alex@acme.test') or {}).get('imap_security'), 'plain')
        # entities never expand: a document with a DOCTYPE is not read at all
        hostile = '<!DOCTYPE x [<!ENTITY a "aaaa">]>' + xml.replace('mail.acme.test', '&a;.acme.test')
        self.assertIsNone(imap_presets.parse_autoconfig(hostile, 'alex@acme.test'))
        mx = lambda url: json.dumps({'Answer': [{'type': 15, 'data': '10 mx1.mail.ovh.net.'}]}) if 'dns' in url else None
        self.assertEqual(imap_presets.lookup('alex@shop.test', fetch=mx)['imap_host'], 'ssl0.ovh.net')
        self.assertEqual(imap_presets.lookup('alex@nowhere.test', fetch=lambda url: None), {})  # nothing found: typed by hand

    def test_lookups_are_https_only(self):
        with mock.patch.object(imap_presets.urllib.request, 'urlopen') as opened:
            self.assertIsNone(imap_presets._fetch('http://autoconfig.acme.test/mail/config-v1.1.xml'))
            opened.assert_not_called()


class FakeUI:
    """step_imap's questions answered from a table; an unanswered one takes its default."""
    interactive, web, reconnect = True, True, False

    def __init__(self, answers, password):
        self.answers, self.password, self.lines, self.asked = answers, password, [], []

    def given(self, prompt):
        return self.answers.get(prompt) or None

    def ask(self, prompt, default=''):
        self.asked.append(prompt)
        return self.answers.get(prompt, default)

    def secret(self, prompt):
        return self.password

    def say(self, text=''):
        self.lines.append(text)


class Setup(Base):
    def step(self, email_address, answers=None, password=PASSWORD, found=None):
        account = {'id': 'acme-imap', 'service': 'imap', 'transport': 'imap', 'boundary': 'work:Acme'}
        ui = FakeUI({'Email address': email_address, **(answers or {})}, password)
        lookup = mock.patch.object(imap_presets, 'lookup', return_value=found if found is not None else {})
        with lookup, mock.patch.object(smtp_mail, 'check'):  # no SMTP server is reached (test_smtp.py has a fake one)
            imap_setup.step(self.config, account, ui)
        return account, ui

    def test_telenet_style_settings_sign_in_on_the_fake_server(self):
        # Telenet's own settings (IMAP over SSL/TLS, SMTP with STARTTLS on 587, the full address as username, the
        # normal mail password), pointed at the fake server on this computer
        telenet = imap_presets.lookup(TELENET_USER, network=False)
        found = {**telenet, 'imap_host': '127.0.0.1', 'imap_port': self.server.port}
        self.server.folders = {'INBOX': self.server.folders['INBOX'], 'INBOX.Verzonden items': self.server.folders['Sent']}
        self.server.folders['INBOX.Verzonden items'].flags = ''  # no \Sent flag: found by its usual name
        account, ui = self.step(TELENET_USER, found=found)
        self.assertEqual((account['imap_host'], account['imap_port'], account['imap_security']), ('127.0.0.1', self.server.port, 'ssl'))
        self.assertEqual((account['smtp_host'], account['smtp_port'], account['smtp_security']), ('smtp.telenet.be', 587, 'starttls'))
        self.assertEqual((account['username'], account['sent_folder']), (TELENET_USER, 'INBOX.Verzonden items'))
        self.assertIn('  Telenet settings found', ui.lines)
        saved = Path(self.config['credentials'][account['credential']])
        self.assertEqual(saved.read_text().strip(), PASSWORD)
        self.assertEqual(saved.stat().st_mode & 0o777, 0o600)
        self.assert_no_password(json.dumps(account), json.dumps(self.config), ui.lines)
        # and it reads from there
        self.server.folders['INBOX'].add(mime('Hallo', 'Bo <bo@client.test>', TELENET_USER, 'x', '<t1@client.test>', when(1)), when(1))
        self.config['accounts'] = [account]
        a.sync_gmail(self.store, self.config, account)
        self.assertEqual(list(self.rows()), ['i1700000000-1'])
        # A wrong password says what to use for Telenet, and saves nothing
        Path(saved).unlink()
        with self.assertRaises(onboarding.SetupError) as caught:
            self.step(TELENET_USER, password='pw-Wrong-0000', found=found)
        self.assertIn('Telenet mail password', caught.exception.fix)
        self.assertFalse(saved.exists())

    def test_any_server_typed_by_hand(self):
        answers = {'IMAP server': '127.0.0.1', 'IMAP port': str(self.server.port), 'IMAP security': 'SSL/TLS',
                   'Username': USER, 'SMTP server': 'smtp.acme.test', 'SMTP port': '465', 'SMTP security': 'SSL/TLS'}
        with mock.patch.object(imap_presets, 'lookup') as lookup:
            account, _ = self.step(USER, answers)
            lookup.assert_not_called()  # typed server settings are taken as they are
        self.assertEqual((account['imap_port'], account['smtp_port'], account['smtp_security'], account['sent_folder']),
                         (self.server.port, 465, 'ssl', 'Sent'))

    def test_wrong_password_and_plaintext_are_refused_before_saving(self):
        answers = {'IMAP server': '127.0.0.1', 'IMAP port': str(self.server.port)}
        with self.assertRaises(onboarding.SetupError) as caught:
            self.step(USER, answers, password='pw-Wrong-0000')
        self.assertEqual(caught.exception.message, imap_setup.REFUSED['imap_auth_failed'])
        self.assertNotIn('pw-Wrong-0000', str(caught.exception))
        with self.assertRaises(onboarding.SetupError):
            self.step(USER, {**answers, 'IMAP security': 'None'})
        self.assertFalse(any(p.name.startswith('imap-') for p in Path(self.temp.name).iterdir() if p.name != 'imap-acme-imap'))

    def test_gmail_and_microsoft_addresses_are_steered(self):
        with self.assertRaises(onboarding.SetupError) as caught:
            self.step('alex@gmail.com', found={'oauth': 'gmail'})
        self.assertIn('Gmail', caught.exception.fix)
        self.assertEqual(self.server.logins, 0)

    def test_the_dashboard_form_with_its_server_settings(self):
        form = onboarding.web_form(self.config, 'imap')
        self.assertEqual(form['ask'], [['email', 'Email address']])
        self.assertEqual(form['secret'], 'Password')
        self.assertEqual([f[1] for f in form['advanced']], ['Username', 'IMAP server', 'IMAP port', 'IMAP security',
                                                           'SMTP server', 'SMTP port', 'SMTP security'])  # by role
        ui = onboarding.WebUI(wait=1)
        ui.prefill({'Email address': USER, 'IMAP server': '127.0.0.1', 'IMAP port': str(self.server.port)},
                   {'Password': PASSWORD})
        account = {'id': 'acme-imap', 'service': 'imap', 'transport': 'imap', 'boundary': 'work:Acme'}
        with mock.patch.object(imap_presets, 'lookup', return_value={}):
            imap_setup.step(self.config, account, ui)
        self.assertEqual((account['imap_host'], account['imap_security'], account['sent_folder']), ('127.0.0.1', 'ssl', 'Sent'))
        self.assert_no_password(ui.view(), json.dumps(account))


if __name__ == '__main__':
    unittest.main()

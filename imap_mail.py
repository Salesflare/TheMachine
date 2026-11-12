"""Any IMAP mailbox (Fastmail, iCloud, Yahoo, an internet provider's or hosting company's mail, a company's own server)
as a mail source. Like ms_graph.py does for Outlook, it answers the Gmail reads the app makes (gmail_call), so its mail
flows through the same sync, history import, review, threads and cards, stored as 'gmail.message' ("an email").

Python's own imaplib, nothing to install. Reads only: every folder is opened read-only (EXAMINE) and bodies are fetched
with BODY.PEEK, so nothing is marked read. INBOX and the Sent folder (RFC 6154 \\Sent, else a usual name) are read.

A message's id is <folder key><UIDVALIDITY>-<UID> (i1700000000-42 in INBOX, s…-7 in Sent): no message text, and it
says where to fetch it. The history cursor is each folder's UIDVALIDITY and next UID. A folder whose UIDVALIDITY changed
(the server renumbered it) answers 404, so the sync reads its usual window again, as for an expired Gmail history.

The password comes from the account's credential file (sources.credential) and is only ever sent to the server, over
TLS: implicit TLS (993) or STARTTLS, never plaintext. Errors are fixed, content-free labels (ImapError): what the server
said is matched, never kept."""
import base64
import datetime as dt
import email
import email.policy
import hashlib
import imaplib
import re
import socket
import ssl
import threading
import time

import ms_graph

SECURITY = ('ssl', 'starttls')  # implicit TLS, or STARTTLS: a plaintext connection is refused
TIMEOUT = 30  # seconds per server answer
IDLE_CHECK = 60  # a kept connection unused this long is checked (NOOP) before it is used again
IDLE_CLOSE = 900  # and one unused this long is closed and opened again
FULL_FETCH = 8_000_000  # bytes: a bigger message is read as its headers and the first part of its text
PART_FETCH = 2_000_000
LIST_CAP = 5000  # newest messages per folder a search looks at
THREAD_DAYS = 60  # how far back a thread's other messages are looked for (threads.get)
LOOPBACK = ('127.0.0.1', '::1', 'localhost')
FOLDERS = {'i': 'INBOX', 's': 'SENT'}  # folder key -> its Gmail label
# Usual names of the Sent folder when the server doesn't mark it \Sent (casefolded, the last part of the path)
SENT_NAMES = {'sent', 'sent items', 'sent messages', 'sent mail', 'sent-mail', 'verzonden', 'verzonden items',
              'verzonden berichten', 'gesendet', 'gesendete elemente', 'gesendete objekte', 'envoyés', 'éléments envoyés',
              'messages envoyés', 'enviados', 'elementos enviados', 'mensajes enviados', 'posta inviata', 'inviata',
              'inviati', 'itens enviados', 'enviadas'}
MONTHS = {m: i for i, m in enumerate(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'), 1)}
MESSAGE_ID = re.compile(r'^([is])(\d+)-(\d+)$')


class ImapError(Exception):
    """A content-free label, as sources.SourceError takes it: never what the server said, and never the password."""
    def __init__(self, category, status=None, retry_after=None):
        self.category, self.status, self.retry_after = category, status, retry_after
        super().__init__(category + (f':HTTP_{status}' if status else ''))


def settings(account):
    """(host, port, security, username) of the account's IMAP server; a plaintext one is refused."""
    security = str(account.get('imap_security') or 'ssl').lower()
    if security not in SECURITY:
        raise ImapError('imap_plaintext_refused')
    host = str(account.get('imap_host') or '').strip().lower()
    if not host or not re.fullmatch(r'[a-z0-9.:\[\]-]+', host):
        raise ImapError('imap_not_configured')
    try:
        port = int(account.get('imap_port') or (993 if security == 'ssl' else 143))
    except (TypeError, ValueError):
        raise ImapError('imap_not_configured') from None
    if not 0 < port < 65536:
        raise ImapError('imap_not_configured')
    return host, port, security, str(account.get('username') or account.get('email') or '')


def tls_context(host):
    """Verified TLS, as a browser does. Only a server on this computer itself (Proton Mail Bridge) may have its own
    self-signed certificate: nothing in between can read a connection that never leaves the computer."""
    context = ssl.create_default_context()
    if host in LOOPBACK:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context


def failure(error, login=False):
    """An ImapError for what went wrong. The server's words are only matched here, never kept or logged."""
    if isinstance(error, ImapError):
        return error
    text = str(error)
    if isinstance(error, (socket.timeout, TimeoutError)):
        return ImapError('timeout')
    if isinstance(error, ssl.SSLError):  # a certificate that doesn't match or isn't trusted, or no common TLS version
        return ImapError('imap_tls_failed', retry_after=3600)
    if isinstance(error, imaplib.IMAP4.error):
        if re.search(r'TLS not supported|STARTTLS', text, re.I):
            return ImapError('imap_tls_failed', retry_after=3600)
        if re.search(r'THROTTL|\[LIMIT\]|too many|rate.?limit|slow down', text, re.I):
            return ImapError('imap_rate_limited', 429, retry_after=600)
        if re.search(r'\[UNAVAILABLE\]|try again later|temporar|server busy|maintenance', text, re.I):
            return ImapError('imap_unavailable', 503, retry_after=300)
        if login or re.search(r'AUTHENTICATIONFAILED|AUTHORIZATIONFAILED|EXPIRED|invalid credentials|LOGIN failed|'
                              r'authentication failed|not authenticated', text, re.I):
            # an hour before trying again: repeated wrong passwords can lock the account at the provider
            return ImapError('imap_auth_failed', 401, retry_after=3600)
        if isinstance(error, imaplib.IMAP4.abort):
            return ImapError('imap_network')
        return ImapError('imap_refused')
    if isinstance(error, (socket.gaierror, ConnectionError, OSError)):
        return ImapError('imap_unreachable')
    return ImapError('imap_failed')


def _quote(name):
    """A folder name as a command argument: as is when it is a plain atom, else quoted."""
    if re.fullmatch(r'[A-Za-z0-9_.&/+-]+', name):
        return name
    return '"' + name.replace('\\', '\\\\').replace('"', '\\"') + '"'


def decode_folder(name):
    """IMAP's modified UTF-7 folder name (RFC 3501 5.1.3) as text: "Envoy&AOk-s" -> "Envoyés"."""
    def part(match):
        text = match.group(1)
        if not text:
            return '&'
        try:
            data = text.replace(',', '/')
            return base64.b64decode(data + '=' * (-len(data) % 4)).decode('utf-16-be')
        except (ValueError, UnicodeDecodeError):
            return match.group(0)
    return re.sub(r'&([A-Za-z0-9+,]*)-', part, name)


def parse_list(rows):
    """LIST answers as [(flags, name)], the name as the server spells it (modified UTF-7 kept)."""
    found = []
    for row in rows or ():
        if isinstance(row, tuple):  # the name came as a literal
            head, name = row[0].decode('utf-8', 'replace'), row[1].decode('utf-8', 'replace')
            match = re.match(r'\(([^)]*)\)', head)
            found.append((match[1] if match else '', name))
            continue
        if not isinstance(row, bytes):
            continue
        match = re.match(r'\(([^)]*)\) (?:"(?:[^"\\]|\\.)*"|NIL) (.+)$', row.decode('utf-8', 'replace'))
        if not match:
            continue
        name = match[2].strip()
        if name.startswith('"') and name.endswith('"'):
            name = re.sub(r'\\(.)', r'\1', name[1:-1])
        found.append((match[1], name))
    return found


def sent_folder(rows, wanted=None):
    """The Sent folder among LIST rows: the one saved at setup while it is there, else the one marked \\Sent, else one
    with a usual name (Sent, Sent Items, Verzonden items, Gesendet…), the shortest path first. None when there is none."""
    folders = parse_list(rows)
    names = [name for _, name in folders]
    if wanted and wanted in names:
        return wanted
    marked = [name for flags, name in folders if '\\sent' in flags.lower().split()]
    if marked:
        return marked[0]
    usual = [name for flags, name in folders if '\\noselect' not in flags.lower()
             and re.split(r'[./]', decode_folder(name))[-1].strip().casefold() in SENT_NAMES]
    return min(usual, key=len) if usual else None


def internal_date(text):
    """INTERNALDATE ("17-Jul-2026 02:44:25 -0700") as an aware datetime, whatever the computer's language."""
    match = re.match(r'\s*(\d{1,2})-([A-Za-z]{3})-(\d{4}) (\d\d):(\d\d):(\d\d) ([+-])(\d\d)(\d\d)', text or '')
    if not match or match[2].title() not in MONTHS:
        return None
    zone = dt.timezone((1 if match[7] == '+' else -1) * dt.timedelta(hours=int(match[8]), minutes=int(match[9])))
    return dt.datetime(int(match[3]), MONTHS[match[2].title()], int(match[1]), int(match[4]), int(match[5]), int(match[6]), tzinfo=zone)


def imap_date(stamp):
    """A date as SEARCH takes it (12-Nov-2026), in English whatever the computer's language."""
    return f'{stamp.day:02d}-{list(MONTHS)[stamp.month - 1]}-{stamp.year}'


def parse_fetch(data):
    """FETCH answers as {uid: {'flags': [...], 'date': datetime|None, 'size': int, 'bytes': [literal, ...]}}."""
    found, current = {}, None
    for item in data or ():
        head, literal = (item[0], item[1]) if isinstance(item, tuple) else (item, None)
        if not isinstance(head, bytes):
            continue
        text = head.decode('utf-8', 'replace')
        uid = re.search(r'\bUID (\d+)', text)
        if uid:
            current = found.setdefault(int(uid[1]), {'flags': [], 'date': None, 'size': 0, 'bytes': []})
        elif re.match(r'\d+ \(', text):
            current = None  # a message without its UID: not one we can name
        if current is None:
            continue
        flags = re.search(r'FLAGS \(([^)]*)\)', text)
        if flags:
            current['flags'] = flags[1].split()
        when = re.search(r'INTERNALDATE "([^"]+)"', text)
        if when:
            current['date'] = internal_date(when[1])
        size = re.search(r'RFC822\.SIZE (\d+)', text)
        if size:
            current['size'] = int(size[1])
        if literal is not None:
            current['bytes'].append(literal)
    return found


# ------------------------------------------------------------------------------------------- connections

class Session:
    """One logged-in connection, kept per account between reads (a sync reads dozens of messages)."""
    def __init__(self, conn):
        self.conn, self.used, self.folders, self.selected, self.lock = conn, time.monotonic(), None, None, threading.RLock()


_lock = threading.Lock()
_sessions = {}


def _key(account):
    host, port, security, username = settings(account)
    return (account.get('id'), host, port, security, username.lower())


def open_connection(account, password):
    """A new connection, over TLS, logged in. Raises ImapError."""
    host, port, security, username = settings(account)
    if not password:
        raise ImapError('imap_password_missing')
    conn = None
    try:
        if security == 'ssl':
            conn = imaplib.IMAP4_SSL(host, port, ssl_context=tls_context(host), timeout=TIMEOUT)
        else:
            conn = imaplib.IMAP4(host, port, timeout=TIMEOUT)
            conn.starttls(ssl_context=tls_context(host))  # no STARTTLS on offer: refused, never read in plaintext
    except Exception as error:  # noqa: BLE001 - every way it fails is mapped
        _close(conn)
        raise failure(error) from None
    try:
        if password.isascii() and username.isascii() and 'LOGINDISABLED' not in conn.capabilities:
            conn.login(username, password)
        else:  # a password or name with other characters: SASL PLAIN carries UTF-8
            secret = b'\0' + username.encode() + b'\0' + password.encode()
            conn.authenticate('PLAIN', lambda _: secret)
    except Exception as error:  # noqa: BLE001
        _close(conn)
        raise failure(error, login=True) from None
    return conn


def _close(conn):
    if conn is None:
        return
    try:
        conn.logout()
    except Exception:  # noqa: BLE001 - it is going away anyway
        try:
            conn.shutdown()
        except Exception:  # noqa: BLE001
            pass


def forget(account):
    """Close this account's kept connection (a new password, a removed account)."""
    with _lock:
        stale = [k for k in _sessions if k[0] == account.get('id')]
        sessions = [_sessions.pop(k) for k in stale]
    for session in sessions:
        _close(session.conn)


class _Use:
    """with _Use(config, credential, account) as session: the account's kept connection, checked and locked; dropped
    when something goes wrong in it, so the next read opens a fresh one."""
    def __init__(self, config, credential, account):
        self.config, self.credential, self.account = config, credential, account

    def __enter__(self):
        key = _key(self.account)
        with _lock:
            session = _sessions.get(key)
        if session is not None:
            session.lock.acquire()
            idle = time.monotonic() - session.used
            ok = idle < IDLE_CLOSE
            if ok and idle > IDLE_CHECK:
                try:
                    ok = session.conn.noop()[0] == 'OK'
                except Exception:  # noqa: BLE001 - the server closed it: open a new one
                    ok = False
            if ok:
                self.session = session
                return session
            session.lock.release()
            self._drop(key, session)
        try:
            password = self.credential(self.config, self.account['credential']) if self.account.get('credential') else ''
        except (OSError, KeyError):
            raise ImapError('imap_password_missing') from None
        session = Session(open_connection(self.account, password))
        session.lock.acquire()
        with _lock:
            old = _sessions.get(key)
            _sessions[key] = session
        if old is not None and old is not session:
            _close(old.conn)
        self.session = session
        return session

    def _drop(self, key, session):
        with _lock:
            if _sessions.get(key) is session:
                _sessions.pop(key)
        _close(session.conn)

    def __exit__(self, kind, error, trace):
        session = self.session
        session.used = time.monotonic()
        session.lock.release()
        if error is not None and not (isinstance(error, ImapError) and error.status == 404):
            self._drop(_key(self.account), session)
        return False


def _ok(answer, what='imap_refused'):
    kind, data = answer
    if kind != 'OK':
        raise failure(imaplib.IMAP4.error(b' '.join(d for d in data if isinstance(d, bytes)).decode('utf-8', 'replace') or what))
    return data


def _uids(answer):
    """A SEARCH answer's UIDs, sorted."""
    return sorted({int(u) for d in _ok(answer) if isinstance(d, bytes) for u in d.split() if u.isdigit()})


def folders(session, account):
    """{'i': INBOX, 's': the Sent folder or None}, looked up once per connection."""
    if session.folders is None:
        try:
            rows = _ok(session.conn.list('""', '*'))
        except ImapError:
            rows = []
        session.folders = {'i': 'INBOX', 's': sent_folder(rows, account.get('sent_folder'))}
    return session.folders


def examine(session, account, key):
    """Open a folder read-only: (uidvalidity, uidnext). A missing folder raises imap_no_folder."""
    name = folders(session, account).get(key)
    if not name:
        raise ImapError('imap_no_folder', 404)
    conn = session.conn
    kind, data = conn.select(_quote(name), readonly=True)
    if kind != 'OK':
        session.selected = None
        raise ImapError('imap_no_inbox' if key == 'i' else 'imap_no_folder', 404 if key != 'i' else None)
    session.selected = key
    validity = conn.response('UIDVALIDITY')[1]
    upcoming = conn.response('UIDNEXT')[1]
    try:
        validity = int((validity[-1] or b'0').split()[0]) if validity and validity[-1] else 0
    except (ValueError, IndexError):
        validity = 0
    try:
        upcoming = int((upcoming[-1] or b'0').split()[0]) if upcoming and upcoming[-1] else 0
    except (ValueError, IndexError):
        upcoming = 0
    if not upcoming:  # a server that doesn't say: one past the newest message
        if int((data or [b'0'])[0] or 0):
            found = parse_fetch(_ok(conn.uid('fetch', '*', '(UID)')))
            upcoming = max(found) + 1 if found else 1
        else:
            upcoming = 1
    return validity, upcoming


# ------------------------------------------------------------------------------------------- Gmail shapes

def thread_of(headers):
    """A conversation id from the headers: the first message it refers to (References' first id, else In-Reply-To),
    else its own Message-ID. Hashed, so no address shows."""
    references = re.findall(r'<[^<>\s]+>', headers.get('references') or '')
    root = (references[0] if references else None) or next(iter(re.findall(r'<[^<>\s]+>', headers.get('in-reply-to') or '')), None) \
        or (headers.get('message-id') or '').strip()
    return 't' + hashlib.sha256(root.lower().encode()).hexdigest()[:24] if root else None


def labels(key, flags):
    found = [FOLDERS[key]]
    lowered = [f.lower() for f in flags]
    if '\\draft' in lowered:
        found.append('DRAFT')
    if key == 'i' and '\\seen' not in lowered:
        found.append('UNREAD')
    return found


def _headers(mime):
    message = email.message_from_bytes(mime, policy=email.policy.compat32)
    return {k.lower(): ms_graph._header(k, v) for k, v in message.items()}


def get_message(session, account, message_id, form='full'):
    match = MESSAGE_ID.match(str(message_id or ''))
    if not match:
        raise ImapError('imap_message_gone', 404)
    key, validity, uid = match[1], int(match[2]), int(match[3])
    current, _ = examine(session, account, key)
    if current != validity:
        raise ImapError('imap_message_gone', 404)
    conn = session.conn
    meta = parse_fetch(_ok(conn.uid('fetch', str(uid), '(UID FLAGS INTERNALDATE RFC822.SIZE)'))).get(uid)
    if not meta:
        raise ImapError('imap_message_gone', 404)
    when = meta['date'] or dt.datetime.now(dt.timezone.utc)
    out = {'id': message_id, 'labelIds': labels(key, meta['flags']), 'internalDate': str(int(when.timestamp() * 1000)),
           'snippet': '', 'webLink': None}
    if form == 'minimal':
        heads = parse_fetch(_ok(conn.uid('fetch', str(uid), '(UID BODY.PEEK[HEADER.FIELDS (MESSAGE-ID REFERENCES IN-REPLY-TO)])'))).get(uid)
        out['threadId'] = thread_of(_headers(b''.join(heads['bytes']) if heads else b'')) or 't' + message_id
        return out
    if meta['size'] and meta['size'] > FULL_FETCH:  # its headers and the start of its text, never a huge download
        parts = parse_fetch(_ok(conn.uid('fetch', str(uid), f'(UID BODY.PEEK[HEADER] BODY.PEEK[TEXT]<0.{PART_FETCH}>)'))).get(uid)
    else:
        parts = parse_fetch(_ok(conn.uid('fetch', str(uid), '(UID BODY.PEEK[])'))).get(uid)
    mime = b''.join(parts['bytes']) if parts else b''
    if not mime:
        raise ImapError('imap_message_gone', 404)
    out['payload'] = ms_graph.payload(mime)
    out['threadId'] = thread_of(_headers(mime)) or 't' + message_id
    return out


def cursor(session, account):
    """The history cursor now: imap1:i<uidvalidity>.<uidnext>[:s<uidvalidity>.<uidnext>]."""
    parts = []
    for key in ('i', 's'):
        if key == 's' and not folders(session, account).get('s'):
            continue
        validity, upcoming = examine(session, account, key)
        parts.append(f'{key}{validity}.{upcoming}')
    return 'imap1:' + ':'.join(parts)


def parse_cursor(text):
    match = re.fullmatch(r'imap1((?::[is]\d+\.\d+)+)', str(text or ''))
    if not match:
        return None
    return {part[0]: (int(part[1:].split('.')[0]), int(part.split('.')[1])) for part in match[1].split(':')[1:]}


def history(session, account, start, limit):
    """Messages added since the cursor, oldest first, at most `limit`: ({'history', 'historyId'}, more?)."""
    known = parse_cursor(start)
    if known is None or 'i' not in known:
        raise ImapError('imap_cursor_unknown', 404)  # not a cursor of ours: read the window again
    added, latest, more = [], {}, False
    for key in ('i', 's'):
        if key == 's' and not folders(session, account).get('s'):
            continue
        validity, upcoming = examine(session, account, key)
        if key in known and known[key][0] != validity:
            raise ImapError('imap_uidvalidity_reset', 404)  # the server renumbered the folder: read the window again
        first = known[key][1] if key in known else upcoming  # a Sent folder found later: from now on
        latest[key] = (validity, upcoming)
        if first >= upcoming:
            latest[key] = (validity, max(first, upcoming))
            continue
        uids = [u for u in _uids(session.conn.uid('search', 'UID', f'{first}:*')) if u >= first]
        room = max(0, limit - len(added))
        taken = uids[:room]
        added += [f'{key}{validity}-{uid}' for uid in taken]
        if len(taken) < len(uids):
            more = True
            latest[key] = (validity, taken[-1] + 1 if taken else first)
    out = 'imap1:' + ':'.join(f'{k}{v}.{n}' for k, (v, n) in latest.items())
    return {'history': [{'messagesAdded': [{'message': {'id': i}}]} for i in added], 'historyId': out}, more


def _search_words(text):
    """A quoted SEARCH string (ASCII only: the caller sends other text as a literal)."""
    return '"' + text.replace('\\', '\\\\').replace('"', '\\"') + '"'


def parse_query(query):
    """Gmail's search words as IMAP SEARCH: (folder keys, [criteria], literal text or None, after, before)."""
    after = before = None
    keys = ['i', 's']
    criteria, words, literal = [], [], None
    for token in re.findall(r'(\w+):"([^"]*)"|(\w+):(\S+)|"([^"]*)"|(\S+)', str(query or '')):
        name, value = (token[0], token[1]) if token[0] else (token[2], token[3]) if token[2] else ('', token[4] or token[5])
        name = name.lower()
        if name == 'after' and value.isdigit():
            after = int(value)
        elif name == 'before' and value.isdigit():
            before = int(value)
        elif name == 'in' and value.lower() in ('sent', 'inbox'):
            keys = ['s'] if value.lower() == 'sent' else ['i']
        elif name == 'rfc822msgid' and value:
            criteria += ['HEADER', 'Message-ID', _search_words(value.strip())] if value.isascii() else []
        elif name in ('from', 'to', 'subject', 'cc') and value:
            if value.isascii():
                criteria += [name.upper(), _search_words(value)]
            elif literal is None:
                literal = (name.upper(), value)
        elif name in ('is', 'label', 'older_than', 'newer_than', 'has', 'category'):
            continue  # Gmail's own filters: not something IMAP can ask
        elif value:
            words.append(value)
    if words:
        text = ' '.join(words)[:200]
        if text.isascii():
            criteria += ['TEXT', _search_words(text)]
        elif literal is None:
            literal = ('TEXT', text)
    if after is not None:
        criteria += ['SINCE', imap_date(dt.datetime.fromtimestamp(after - 86400, dt.timezone.utc))]
    if before is not None:
        criteria += ['BEFORE', imap_date(dt.datetime.fromtimestamp(before + 86400, dt.timezone.utc))]
    return keys, criteria, literal, after, before


def search(session, account, query, limit, offset=0):
    """Messages matching Gmail-style search words, newest first: ([ids], more?)."""
    keys, criteria, literal, after, before = parse_query(query)
    if not criteria and not literal:
        raise ImapError('unsupported_gmail_query')
    conn, found = session.conn, []
    for key in keys:
        if key == 's' and not folders(session, account).get('s'):
            continue
        validity, _ = examine(session, account, key)
        if literal:
            conn.literal = literal[1].encode()
            answer = conn.uid('search', 'CHARSET', 'UTF-8', *criteria, literal[0])
        else:
            answer = conn.uid('search', *criteria)
        try:
            uids = _uids(answer)[-LIST_CAP:]
        except ImapError as error:
            if literal and error.category == 'imap_refused':
                continue  # a server that can't search that text: nothing found there
            raise
        if not uids:
            continue
        dates = parse_fetch(_ok(conn.uid('fetch', ','.join(map(str, uids)), '(UID INTERNALDATE)')))
        for uid in uids:
            when = (dates.get(uid) or {}).get('date')
            stamp = when.timestamp() if when else None
            if stamp is not None and ((after is not None and stamp < after) or (before is not None and stamp >= before)):
                continue
            found.append((stamp or 0, key, f'{key}{validity}-{uid}'))
    found.sort(key=lambda x: (-x[0], x[1]))
    page = found[offset:offset + limit]
    return [x[2] for x in page], len(found) > offset + limit


def thread(session, account, thread_id):
    """The messages of one conversation from the last THREAD_DAYS days, in both folders, with who sent each and when."""
    since = imap_date(dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=THREAD_DAYS))
    out = []
    for key in ('i', 's'):
        if key == 's' and not folders(session, account).get('s'):
            continue
        validity, _ = examine(session, account, key)
        uids = _uids(session.conn.uid('search', 'SINCE', since))[-2000:]
        if not uids:
            continue
        rows = parse_fetch(_ok(session.conn.uid('fetch', ','.join(map(str, uids)),
                                                '(UID FLAGS INTERNALDATE BODY.PEEK[HEADER.FIELDS (MESSAGE-ID REFERENCES IN-REPLY-TO FROM)])')))
        for uid, row in rows.items():
            headers = _headers(b''.join(row['bytes']))
            if thread_of(headers) != thread_id:
                continue
            when = row['date'] or dt.datetime.now(dt.timezone.utc)
            out.append({'id': f'{key}{validity}-{uid}', 'threadId': thread_id, 'labelIds': labels(key, row['flags']),
                        'internalDate': str(int(when.timestamp() * 1000)),
                        'payload': {'headers': [{'name': 'From', 'value': headers.get('from', '')}]}})
    out.sort(key=lambda m: int(m['internalDate']))
    return {'id': thread_id, 'messages': out}


def gmail_call(config, credential, account, method, params):
    """The Gmail reads the app makes, answered from the IMAP server (see the module's notes)."""
    params = dict(params or {})
    email_address = str(account.get('email') or '').lower()
    if method == 'gmail.users.settings.sendAs.get':
        return {'sendAsEmail': params.get('sendAsEmail') or email_address, 'signature': ''}
    if method == 'gmail.users.settings.sendAs.list':
        return {'sendAs': [{'sendAsEmail': email_address, 'isPrimary': True, 'treatAsAlias': True, 'verificationStatus': 'accepted'}]}
    if method == 'gmail.users.messages.attachments.get':
        raise ImapError('imap', 404)  # every part's data is already in the message's payload
    if method not in ('gmail.users.getProfile', 'gmail.users.messages.get', 'gmail.users.threads.get',
                      'gmail.users.messages.list', 'gmail.users.history.list'):
        raise ImapError('unsupported_gmail_method')
    try:
        with _Use(config, credential, account) as session:
            if method == 'gmail.users.getProfile':
                return {'emailAddress': email_address, 'historyId': cursor(session, account)}
            if method == 'gmail.users.messages.get':
                return get_message(session, account, params.get('id'), params.get('format', 'full'))
            if method == 'gmail.users.threads.get':
                return thread(session, account, str(params.get('id') or ''))
            if method == 'gmail.users.messages.list':
                offset = int(params['pageToken']) if str(params.get('pageToken') or '').isdigit() else 0
                limit = max(1, min(int(params.get('maxResults') or 40), 100))
                ids, more = search(session, account, params.get('q'), limit, offset)
                out = {'messages': [{'id': i, 'threadId': None} for i in ids]}
                if more:
                    out['nextPageToken'] = str(offset + limit)
                return out
            start = params.get('pageToken') or params.get('startHistoryId')
            out, more = history(session, account, start, max(1, min(int(params.get('maxResults') or 100), 500)))
            if more:
                out['nextPageToken'] = out['historyId']
            return out
    except ImapError:
        raise
    except Exception as error:  # noqa: BLE001 - imaplib, the socket, TLS: all as content-free labels
        raise failure(error) from None


def check(config, credential, account):
    """Log in and look for INBOX and the Sent folder: the Sent folder's name, or None. Raises ImapError."""
    forget(account)  # a new password or server: never a connection from before
    try:
        with _Use(config, credential, account) as session:
            examine(session, account, 'i')
            return folders(session, account).get('s')
    except ImapError:
        raise
    except Exception as error:  # noqa: BLE001
        raise failure(error) from None

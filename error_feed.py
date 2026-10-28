"""Error reports for The Machine team (docs/help/error-reports.md): a signature of each error, never what caused it.

So the team sees a bug before anyone has to report it, a Machine on The Machine Network sends the errors it hits, as
signatures only:

- what: the error's type, and its message normalized (normalize): numbers, ids, quoted text, addresses, links, paths
  and anything token-like taken out, then held to a strict allowed shape, so a word that could be a name goes too;
- where: file:function:line in The Machine's own code (never a path on this computer), and the app version;
- how often: a count, first and last seen.

Never: message content, names, addresses, tokens or values. Errors come from the service's own code (assistant.FaultLog:
logged errors and threads that die of one), the dashboard (window errors and unhandled rejections, posted by the page),
failed reviews and coding-agent jobs (their error codes) and syncs that fail (the source's service and the error type).

Locally deduplicated by signature (a repeat only counts), at most MAX_SIGNATURES kept, at most BATCH sent at a time and
SEND_EVERY apart, DAY_CAP a day; what was sent goes again only when its count grew. Kept 30 days. Sent over the Network
(POST /errors, the control plane's /api/fleet/errors); without the Network nothing is sent.

On by default; the owner turns it off in Settings, The Machine team ("Send error reports"). Off: nothing is recorded
or sent, and what waited is deleted."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import uuid

SOURCES = ('service', 'dashboard', 'job', 'review', 'sync')
MAX_SIGNATURES = 300
BATCH = 50
SEND_EVERY = 600       # seconds between batches
DAY_CAP = 500          # signatures sent a day at most
KEEP_DAYS = 30
MESSAGE_MAX = 160
CLIENT_MAX = 10        # errors one dashboard post may carry
CLIENT_FILES = ('dashboard.html', 'sw.js')  # the dashboard's own code; an extension's or another page's errors are not ours

SCHEMA = '''
CREATE TABLE IF NOT EXISTS error_feed(id TEXT PRIMARY KEY,source TEXT NOT NULL,kind TEXT NOT NULL,message TEXT NOT NULL,
  location TEXT NOT NULL,version TEXT,count INTEGER NOT NULL,sent INTEGER NOT NULL DEFAULT 0,first_at TEXT NOT NULL,last_at TEXT NOT NULL,sent_at TEXT);
CREATE TABLE IF NOT EXISTS error_feed_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL);
'''


def ensure(db):
    for statement in SCHEMA.split(';'):
        if statement.strip():
            db.execute(statement)
    if not db.execute("SELECT 1 FROM error_feed_prefs WHERE key='lexical_v2'").fetchone():
        for sid, message in db.execute('SELECT id,message FROM error_feed').fetchall():
            db.execute('UPDATE error_feed SET message=? WHERE id=?', (normalize(message), sid))
        db.execute("INSERT INTO error_feed_prefs VALUES('lexical_v2','on')")


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def pref(db, key, default=None):
    ensure(db)
    row = db.execute('SELECT value FROM error_feed_prefs WHERE key=?', (key,)).fetchone()
    return row[0] if row else default


def set_pref(db, key, value):
    ensure(db)
    db.execute('INSERT INTO error_feed_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, str(value)))


def on(db):
    """Settings, Send error reports: on unless the owner turned it off."""
    return pref(db, 'on', 'on') != 'off'


def set_on(db, value):
    """Turn reports on or off. Off deletes what waited: nothing recorded is ever sent later."""
    set_pref(db, 'on', 'on' if value else 'off')
    if not value:
        db.execute('DELETE FROM error_feed')


# ---------------------------------------------------------------- what a message may say

# Capitalized words an error message is written in. Any other capitalized word could be a name, so it goes (<word>).
WORDS = set('''A An The No Not Cannot Could Failed Failure Invalid Unexpected Unknown Missing Expected Bad Too Unable
Internal Bearer Error Errors Exception Timeout Timed Connection Network Request Response Object Value Key Index Type Attribute
Name Module Import Syntax Reference Range Abort Aborted Permission Denied Access Refused Reset Closed Broken Pipe File
Directory Database Table Column Row Query Operation Unsupported Undefined Null None True False NaN Infinity Uncaught
Promise Load Loading Script Network Fetch JSON HTTP HTTPS API URL SQL TLS SSL EOF UTF ASCII CSRF CORS DOM OK Is Was
Got Has Have Must Should Only Already Empty Out Of In On At For To From With Without And Or If Then Else Unhandled
Rejection Maximum Minimum Call Stack Size Exceeded Assertion Decode Encode Unicode Recursion Overflow Memory Zero
Division Lookup Stop Iteration Generator Runtime Not Implemented Gateway Machine Machines OpenClaw Telegram Gmail Google
Microsoft Outlook Slack WhatsApp Telegram Zoom Calendar Drive Network Fleet Graph Card Cards Chat Review Preparation Sync Token Tokens
Expired Authentication Auth Rate Limit Quota Service Unavailable Forbidden Unauthorized Server Client Found Read Write Socket'''.split())
TYPES = {'str', 'int', 'float', 'bool', 'bytes', 'dict', 'list', 'tuple', 'set', 'frozenset', 'NoneType', 'object', 'type',
         'function', 'method', 'module', 'datetime', 'date', 'Path', 'Row', 'Connection', 'Cursor', 'undefined', 'null',
         'number', 'string', 'boolean', 'symbol', 'bigint', 'Array', 'Object', 'Promise', 'Response', 'Element', 'HTMLElement',
         'Node', 'Window', 'Document'}
TYPE_NAME = re.compile(r'[A-Z][A-Za-z0-9]*(?:Error|Exception|Warning|Interrupt|Exit|Iteration|Type)')
SAFE_WORDS = {w.lower() for w in WORDS | TYPES} | set('''such attribute properties reading after s person email lookup delivery status android feed jwt parse reply draft rejected open cannot send see role has no name known next failed down gone error unavailable request response local at remote retry code result received returned does did not exist is was are been have network reach body text get set null sent timeout connection refused deprecation validation sync unknown outcome exceeded exception quota limit read write pending range invalid empty function expected dict list index key and or of the a an to from for in on with without by it its this that too many client server call file os errno'''.split())
SAFE_CODES = {'android_feed_unavailable', 'delivery_outcome_unknown', 'conversations.history', 'HTTP_'}
SAFE_TYPES = set('''Error Exception Warning BaseException RuntimeError ValueError TypeError KeyError IndexError AttributeError NameError ImportError ModuleNotFoundError SyntaxError ReferenceError RangeError AbortError TimeoutError ConnectionError ConnectionResetError ConnectionRefusedError BrokenPipeError FileNotFoundError PermissionError OSError IOError EOFError UnicodeError UnicodeDecodeError UnicodeEncodeError RecursionError OverflowError MemoryError ZeroDivisionError AssertionError LookupError StopIteration SystemExit KeyboardInterrupt NotImplementedError OperationalError DatabaseError IntegrityError HttpError SourceError BrokerError'''.split())


def safe_word(word):
    return word.lower() in SAFE_WORDS or word in SAFE_CODES or word in SAFE_TYPES

SECRETISH = (
    (re.compile(r'(?i)\b(bearer|basic)\s+\S+'), r'\1 <secret>'),
    (re.compile(r'(?i)\b(token|secret|password|passwd|passphrase|api[_-]?key|authorization|cookie|session|code|sig|signature)'
                r'(["\']?\s*[:=]\s*)\S+'), r'\1\2<secret>'),
)
EMAIL = re.compile(r'[\w.+%-]+@[\w-]+(?:\.[\w-]+)+')
URL = re.compile(r'(?i)\b[a-z][a-z0-9+.-]*://\S*|\bwww\.\S+')
DOMAIN = re.compile(r'(?i)\b[\w-]+(?:\.[\w-]+)*\.(?:com|org|net|io|ai|be|nl|de|fr|uk|eu|co|app|dev|computer|me|info|biz|us|ca|es|it|ch|at|se|no|dk|fi|pl|pt|br|au|in|jp|cloud|tech|so|ly|xyz)\b(?![\w(])')
QUOTED = re.compile(r'"([^"]*)"|\'([^\']*)\'|“([^”]*)”|‘([^’]*)’|`([^`]*)`')
# A path: anything with a slash in it, or a Windows one; a home folder often carries a person's name
PATH = re.compile(r'(?:[A-Za-z]:\\|\\\\)[^\s,;)]+|(?<![\w<])~?(?:/[^\s/,;:)]+)+/?|(?<![\w<])[\w.-]+(?:/[\w.-]+)+')
UUID = re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I)
HEX = re.compile(r'\b(?:0x)?[0-9a-f]*\d[0-9a-f]*[a-f][0-9a-f]*\b|\b(?:0x)?[0-9a-f]*[a-f][0-9a-f]*\d[0-9a-f]*\b', re.I)
LONG = re.compile(r'[A-Za-z0-9_\-+/=]{24,}')
# A plain code made of lowercase words (android_feed_unavailable, error=delivery_outcome_unknown) is not a secret:
# a token has digits, capitals or one long run of letters. Each word at most 20 letters.
PLAIN_CODE = re.compile(r'[a-z]{1,20}(?:[_=-][a-z]{1,20})+')
NUMBER = re.compile(r'[-+]?\d[\d.,:_]*')
TOKEN = re.compile(r'<[a-z]{1,8}>|…|[^\W\d_][\w$]*(?:\.[^\W\d_][\w$]*)*|\S')
PUNCT = set('.,:;()[]{}=<>!?+-*/#&|%"…')
PLACEHOLDERS = {'<n>', '<id>', '<secret>', '<email>', '<url>', '<path>', '<word>', '<name>', '<text>', '<link>', '<number>'}
# What a sent message may look like, checked last (and again by the control plane): placeholders, plain ASCII words and
# a little punctuation, nothing else
SHAPE = re.compile(r'(?:<[a-z]{1,8}>|…|[A-Za-z_][A-Za-z0-9_$.]{0,39}|[.,:;()\[\]{}=<>!?+*/#&|%"\-]| )*')


def _word(token, names):
    if token in PLACEHOLDERS or token == '…':
        return token
    if not token.isascii() or not re.fullmatch(r'[A-Za-z_][\w$.]*', token) or len(token) > 40:
        return '<word>'
    if names and any(part in names for part in token.lower().split('.')):
        return '<name>'
    if safe_word(token):
        return token
    return '<word>'


def normalize(message, names=()):
    """The message as a signature may carry it, or '' when nothing safe is left. `names`: words to take out besides
    (the people, organizations and accounts this Machine knows, lowercased)."""
    text = ' '.join(str(message or '').split())[:2000]
    if not text:
        return ''
    import support  # the support bundle's redaction first: tokens, keys, long hex, addresses
    text = support.scrub(text)
    for pattern, replace in SECRETISH:
        text = pattern.sub(replace, text)
    text = URL.sub('<url>', text)
    text = EMAIL.sub('<email>', text)
    text = DOMAIN.sub('<url>', text)
    text = QUOTED.sub(lambda m: f'"{q}"' if (q := next(g for g in m.groups() if g is not None)) in TYPES else '"…"', text)
    text = PATH.sub('<path>', text)
    text = support.HOME.sub('<path>', text)
    text = UUID.sub('<id>', text)
    text = re.sub(r'<(?:jwt|bot-token|api-key|token|hex|secret|redacted)>|\[(?:redacted|email|number)\]', '<secret>', text)
    text = LONG.sub(lambda m: m.group(0) if PLAIN_CODE.fullmatch(m.group(0)) else '<secret>', text)
    text = HEX.sub('<id>', text)
    text = NUMBER.sub('<n>', text)
    lowered = {str(n).lower() for n in names if n}
    out = []
    for token in TOKEN.findall(text):
        if len(token) == 1 and not token.isalnum() and token != '_':
            if token in PUNCT:
                out.append(token)
            continue
        word = _word(token, lowered)
        if not (out and out[-1] == word and word.startswith('<')):  # <n> <n> <n> says no more than <n>
            out.append(word)
    text = re.sub(r'\s+([.,:;)\]}!?])', r'\1', ' '.join(out))
    text = re.sub(r'([(\[{])\s+', r'\1', text)
    text = re.sub(r'"\s*([^"]*?)\s*"', r'"\1"', text)
    text = text.strip()[:MESSAGE_MAX].strip()
    return text if allowed(text) else ''


def allowed(message):
    return (isinstance(message, str) and len(message) <= MESSAGE_MAX and bool(SHAPE.fullmatch(message))
            and all(safe_word(w) for w in re.findall(r'[A-Za-z_][A-Za-z0-9_$.]*', re.sub(r'<[a-z]{1,8}>', ' ', message))))


KIND = re.compile(r'[A-Za-z][A-Za-z0-9_.]{0,59}')
FILE = re.compile(r'(?!/)(?!.*\.\.)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+){0,3}')
FUNCTION = re.compile(r'[A-Za-z_$<][A-Za-z0-9_$.<>-]{0,59}')
VERSION = re.compile(r'[A-Za-z0-9._-]{1,40}')


def where(file, function, line=None):
    """file:function[:line] when it is a place in The Machine's own code, else None."""
    file, function = str(file or ''), str(function or '') or '<module>'
    if not FILE.fullmatch(file) or not FUNCTION.fullmatch(function):
        return None
    if line not in (None, '', 0):
        try:
            line = int(line)
        except (TypeError, ValueError):
            return None
        return f'{file}:{function}:{line}' if 0 < line < 10 ** 6 else None
    return f'{file}:{function}'


def signature_id(source, kind, location, message):
    """Stable across releases: the line number is left out, so a moved line is the same error."""
    place = ':'.join(location.split(':')[:2])
    return hashlib.sha256(f'{source}|{kind}|{place}|{message}'.encode()).hexdigest()[:16]


def record(db, source, kind, message, file, function, line=None, version=None, at=None):
    """Count one error. Returns its signature id, or None when reports are off or it isn't one to keep."""
    ensure(db)
    if source not in SOURCES or not on(db):
        return None
    kind = str(kind or '') if KIND.fullmatch(str(kind or '')) else 'Error'
    location = where(file, function, line)
    if not location:
        return None
    text = normalize(message)
    version = str(version) if version and VERSION.fullmatch(str(version)) else None
    sid = signature_id(source, kind, location, text)
    stamp = at or now()
    if not db.execute('SELECT 1 FROM error_feed WHERE id=?', (sid,)).fetchone():
        if db.execute('SELECT count(*) FROM error_feed').fetchone()[0] >= MAX_SIGNATURES:
            return None  # a flood of different errors: the first ones already tell
        db.execute('INSERT INTO error_feed(id,source,kind,message,location,version,count,first_at,last_at) VALUES(?,?,?,?,?,?,1,?,?)',
                   (sid, source, kind, text, location, version, stamp, stamp))
    else:
        db.execute('UPDATE error_feed SET count=count+1,last_at=?,location=?,version=coalesce(?,version) WHERE id=?', (stamp, location, version, sid))
    return sid


def record_client(db, errors, version=None):
    """What the dashboard posted: [{kind, message, file, function, line}], at most CLIENT_MAX, each normalized here
    again (the page is never trusted). Returns how many were counted."""
    counted = 0
    for item in (errors if isinstance(errors, list) else [])[:CLIENT_MAX]:
        if not isinstance(item, dict) or str(item.get('file') or '') not in CLIENT_FILES:
            continue
        if record(db, 'dashboard', str(item.get('kind') or '')[:60], str(item.get('message') or '')[:1000], item.get('file'),
                  str(item.get('function') or '')[:60] or '<anonymous>', item.get('line'), version):
            counted += 1
    return counted


def prune(db, current=None):
    ensure(db)
    cutoff = ((current or dt.datetime.now(dt.timezone.utc)) - dt.timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds')
    return db.execute('DELETE FROM error_feed WHERE last_at<?', (cutoff,)).rowcount


# ---------------------------------------------------------------- sending

def batch(db, current=None, names=()):
    """The next batch to send, or None: reports on, SEND_EVERY since the last, under DAY_CAP today, and only signatures
    that are new or counted more since they were last sent. Each is checked again before it may go, with `names` (or
    what it returns, when it is a function: read only when something is to go) taken out besides."""
    ensure(db)
    if not on(db):
        return None
    current = current or dt.datetime.now(dt.timezone.utc)
    prune(db, current)
    last = pref(db, 'sent_at')
    if last and dt.datetime.fromisoformat(last) > current - dt.timedelta(seconds=SEND_EVERY):
        return None
    day = current.date().isoformat()
    used = int(pref(db, 'day_count', '0') or 0) if pref(db, 'day') == day else 0
    room = min(BATCH, DAY_CAP - used)
    if room <= 0:
        return None
    rows = db.execute('SELECT id,source,kind,message,location,version,count,sent,first_at,last_at FROM error_feed WHERE count>sent '
                      'ORDER BY sent=0 DESC,count-sent DESC,last_at DESC LIMIT ?', (room,)).fetchall()
    if not rows:
        return None
    lowered = {str(n).lower() for n in (names() if callable(names) else names) if n}
    out = []
    for sid, source, kind, message, location, version, count, done, first_at, last_at in rows:
        scrubbed = normalize(message, lowered)
        if scrubbed != message:
            db.execute('UPDATE error_feed SET message=? WHERE id=?', (scrubbed, sid))
        message = scrubbed
        if not allowed(message) or not where(*(location.split(':') + [None])[:3]) or not KIND.fullmatch(kind):
            db.execute('UPDATE error_feed SET sent=count WHERE id=?', (sid,))  # never goes: not offered again
            continue
        out.append({'id': sid, 'source': source, 'kind': kind, 'message': message, 'where': location, 'version': version,
                    'count': count - done, 'total': count, 'first_seen': first_at, 'last_seen': last_at})
    return {'batch': 'eb_' + uuid.uuid4().hex[:20], 'signatures': out} if out else None


def sent(db, payload, current=None):
    """After the control plane took a batch: each signature counts as sent up to what went."""
    current = current or dt.datetime.now(dt.timezone.utc)
    stamp = current.isoformat(timespec='seconds')
    for item in payload.get('signatures') or []:
        db.execute('UPDATE error_feed SET sent=?,sent_at=? WHERE id=?', (item['total'], stamp, item['id']))
    day = current.date().isoformat()
    used = int(pref(db, 'day_count', '0') or 0) if pref(db, 'day') == day else 0
    set_pref(db, 'day', day)
    set_pref(db, 'day_count', used + len(payload.get('signatures') or []))
    set_pref(db, 'sent_at', stamp)


def send(connect, call, names=(), current=None):
    """One round: build a batch, POST it over the Network, mark it sent. Returns how many signatures went."""
    with connect() as db:
        payload = batch(db, current, names)
    if not payload:
        return 0
    answer = call('POST', '/errors', payload)
    if not isinstance(answer, dict) or answer.get('ok') is not True:
        raise ValueError('no receipt')
    with connect() as db:
        if on(db):  # turned off while it went: it is deleted, not marked
            sent(db, payload, current)
    return len(payload['signatures'])


def view(db):
    ensure(db)
    waiting = db.execute('SELECT count(*) FROM error_feed WHERE count>sent').fetchone()[0]
    return {'on': on(db), 'waiting': waiting, 'sent_at': pref(db, 'sent_at')}


def example(db, limit=3):
    """What the last batch would look like, for `assistant error-reports` and the help page."""
    ensure(db)
    rows = db.execute('SELECT source,kind,message,location,version,count,first_at,last_at FROM error_feed ORDER BY last_at DESC LIMIT ?', (limit,))
    return [dict(zip(('source', 'kind', 'message', 'where', 'version', 'count', 'first_seen', 'last_seen'), r)) for r in rows]


def to_json(value):
    return json.dumps(value, indent=2, ensure_ascii=False)

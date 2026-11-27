"""Error reports for The Machine team (docs/help/error-reports.md): a signature of each error, never what caused it.

So the team sees a bug before anyone has to report it, a Machine on The Machine Network sends the errors it hits, as
signatures only:

- what: the error's type, and its message normalized (normalize): numbers, ids, quoted text, addresses, links, paths
  and anything token-like taken out, then held to a strict allowed shape, so a word that could be a name goes too;
- where: file:function:line in The Machine's own code (never a path on this computer), and the app version;
- how often: a count, first and last seen.

Never: message content, names, addresses, tokens or values. Errors come from the service's own code (assistant.FaultLog:
logged errors and threads that die of one, and a ValueError a dashboard action hit that isn't an OwnerError:
machine/web/handler.py), the dashboard (window errors, unhandled rejections and bugs in its code a
try caught and showed, posted by the page), its service worker (source sw: its own errors and a failed shell update,
passed on by the page), failed API calls the dashboard saw (source api: the endpoint and an action's name, a 5xx or a
timeout, never the query or what was sent), failed reviews, preparations and coding-agent jobs (their error codes), syncs that
fail (the source's service and the error type; an owner's own connector as sync:own:<service> with its error's label,
own_message) and the AI's check when it fails (ModelCheckFailed, machine/app/first_look.py). Not the owner's own states:
a usage limit, or a sign-in to the AI that lapsed (preparation_state.SIGNIN_REASONS, claude_signin.said_signed_out).

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
import timeutil
import uuid

# what a message may say: its words, types and services (shared with the control plane)
from error_words import (DOMAIN, SAFE_CODES, SAFE_TYPES, SAFE_WORDS, SERVICES, SHAPE, TYPE_NAME, TYPES, WORDS,  # noqa: F401
                         safe_word)

SOURCES = ('service', 'dashboard', 'sw', 'api', 'job', 'review', 'sync')
MAX_SIGNATURES = 300
BATCH = 50
SEND_EVERY = 600       # seconds between batches
DAY_CAP = 500          # signatures sent a day at most
KEEP_DAYS = 30
MESSAGE_MAX = 160
CLIENT_MAX = 10        # errors one dashboard post may carry
CLIENT_FILES = {'dashboard.html': 'dashboard', 'sw.js': 'sw'}  # the dashboard's own code; an extension's or another page's errors are not ours
SEGMENT = re.compile(r'[a-z][a-z_-]{0,30}')  # an endpoint's part as the code names it; anything else (an id) is <id>

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
    return timeutil.stamp()


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

# The words, types and services a message may have: error_words.py.
# An HTTP status said in words, as the control plane takes no 3-digit numbers: 401 and 429 stay told apart
HTTP_STATUS = re.compile(r'(?i)(?<![A-Za-z])HTTP(?:[ _]?Error)?[ _:]*([1-5]\d\d)\b')
REASONS = {400: 'bad request', 401: 'unauthorized', 402: 'payment required', 403: 'forbidden', 404: 'not found',
           405: 'method not allowed', 408: 'request timeout', 409: 'conflict', 410: 'gone', 413: 'payload too large',
           415: 'unsupported media type', 422: 'unprocessable entity', 423: 'locked', 429: 'rate limited',
           500: 'internal server error', 501: 'not implemented', 502: 'bad gateway', 503: 'service unavailable',
           504: 'gateway timeout'}


def http_reason(code):
    code = int(code)
    return REASONS.get(code) or {3: 'redirect', 4: 'client error', 5: 'server error'}.get(code // 100, 'status')


SECRETISH = (
    (re.compile(r'(?i)\b(bearer|basic)\s+\S+'), r'\1 <secret>'),
    (re.compile(r'(?i)\b(token|secret|password|passwd|passphrase|api[_-]?key|authorization|cookie|session|code|sig|signature)'
                r'(["\']?\s*[:=]\s*)\S+'), r'\1\2<secret>'),
)
EMAIL = re.compile(r'[\w.+%-]+@[\w-]+(?:\.[\w-]+)+')
URL = re.compile(r'(?i)\b[a-z][a-z0-9+.-]*://\S*|\bwww\.\S+')
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
    text = HTTP_STATUS.sub(lambda m: 'HTTP ' + http_reason(m.group(1)), text)
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
            # a sentence's full stop is not part of its last word ("Failed to fetch resource." was refused whole)
            and all(safe_word(w.rstrip('.')) for w in re.findall(r'[A-Za-z_][A-Za-z0-9_$.]*', re.sub(r'<[a-z]{1,8}>', ' ', message))))


KIND = re.compile(r'[A-Za-z][A-Za-z0-9_.]{0,59}')
FILE = re.compile(r'(?!/)(?!.*\.\.)[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+){0,3}')
FUNCTION = re.compile(r'[A-Za-z_$<][A-Za-z0-9_$.<>-]{0,59}')
VERSION = re.compile(r'[A-Za-z0-9._-]{1,40}')
# An owner's own connector (connectors/<service>.py without a services row): its service id and the label its
# SourceError names (notes_http), so the team can see whose connector fails and help. Nothing else of its code.
OWN = 'sync:own'
OWN_SERVICE = re.compile(r'[a-z0-9_]{1,40}')
OWN_LABEL = re.compile(r'[a-z][a-z0-9_]{0,39}')
OWN_MESSAGE = re.compile(r'(?:[a-z][a-z0-9_]{0,39}|<word>)(?:: HTTP ((?:[a-z]+ ){0,2}[a-z]+))?')


def own(location):
    return location == OWN or str(location).startswith(OWN + ':')


def own_message(error):
    """An own connector's failure as a report says it: its SourceError's label when it is a plain one, and the HTTP
    status in words (notes_http: HTTP unauthorized). Any other label goes through normalize like every message."""
    label = getattr(error, 'category', None)
    if not isinstance(label, str) or not OWN_LABEL.fullmatch(label):
        return normalize(str(error))
    status = getattr(error, 'status', None)
    return f'{label}: HTTP {http_reason(status)}' if isinstance(status, int) and 100 <= status <= 599 else label


def own_allowed(message):
    match = OWN_MESSAGE.fullmatch(str(message or ''))
    return bool(match) and (not match.group(1) or match.group(1) in set(REASONS.values()) | {'redirect', 'client error', 'server error', 'status'})


def where(file, function, line=None):
    """file:function[:line] when it is a place in The Machine's own code, else None. An owner's own connector's sync is
    sync:own:<service> (its service id, when it is a plain one) or sync:own."""
    file, function = str(file or ''), str(function or '') or '<module>'
    if (file, function) == ('sync', 'own') and line not in (None, ''):
        return f'sync:own:{line}' if OWN_SERVICE.fullmatch(str(line)) else None
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
    place = location if own(location) else ':'.join(location.split(':')[:2])  # each own connector its own signature
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
    text = message if own(location) and own_allowed(message) else normalize(message)
    version = str(version) if version and VERSION.fullmatch(str(version)) else None
    sid = signature_id(source, kind, location, text)
    stamp = at or now()
    if not db.execute('SELECT 1 FROM error_feed WHERE id=?', (sid,)).fetchone():
        if db.execute('SELECT count(*) FROM error_feed').fetchone()[0] >= MAX_SIGNATURES:
            return None  # a flood of different errors: the first ones already tell
        db.execute('INSERT INTO error_feed(id,source,kind,message,location,version,count,first_at,last_at) VALUES(?,?,?,?,?,?,1,?,?)',
                   (sid, source, kind, text, location, version, stamp, stamp))
    else:
        # The message as this release words it: a batch scrubbed under an older, shorter word list rewrote the kept one,
        # and a repeat must not send that forever (whatsapp_source_unavailable went on arriving as "<word>", 2026-11-09)
        db.execute('UPDATE error_feed SET count=count+1,last_at=?,location=?,message=?,version=coalesce(?,version) WHERE id=?',
                   (stamp, location, text, version, sid))
    return sid


def endpoint(api, action='', actions=()):
    """A failed call's place: api/graph/node/4f2c?q=… is graph.node.<id>, api/action with the action's name (one of
    `actions`, the dashboard's own, else other) is action.<name>. None when it isn't one of ours."""
    parts = [p for p in str(api or '').split('?')[0].split('#')[0].split('/') if p][:4]
    if not parts or not SEGMENT.fullmatch(parts[0]):
        return None
    out = '.'.join(p if SEGMENT.fullmatch(p) else '<id>' for p in parts)
    if out == 'action':
        out += '.' + (action if action in actions else 'other')
    return out[:60]


def record_client(db, errors, version=None, actions=()):
    """What the dashboard posted, at most CLIENT_MAX: its own errors and its service worker's as {kind, message, file,
    function, line}, each normalized here again (the page is never trusted), and failed API calls as {api, action,
    status}: a 5xx or 'timeout', kept as the endpoint and HTTP5xx or Timeout, no message. Returns how many were counted."""
    counted = 0
    for item in (errors if isinstance(errors, list) else [])[:CLIENT_MAX]:
        if not isinstance(item, dict):
            continue
        if 'api' in item:
            status, place = item.get('status'), endpoint(item.get('api'), str(item.get('action') or ''), actions)
            kind = 'Timeout' if status == 'timeout' else f'HTTP{status}' if isinstance(status, int) and 500 <= status <= 599 else None
            if kind and place and record(db, 'api', kind, '', 'api', place, None, version):
                counted += 1
            continue
        source = CLIENT_FILES.get(str(item.get('file') or ''))
        if source and record(db, source, str(item.get('kind') or '')[:60], str(item.get('message') or '')[:1000], item.get('file'),
                             str(item.get('function') or '')[:60] or '<anonymous>', item.get('line'), version):
            counted += 1
    return counted


def prune(db, current=None):
    ensure(db)
    cutoff = ((current or timeutil.clock()) - dt.timedelta(days=KEEP_DAYS)).isoformat(timespec='seconds')
    return db.execute('DELETE FROM error_feed WHERE last_at<?', (cutoff,)).rowcount


# ---------------------------------------------------------------- sending

def batch(db, current=None, names=()):
    """The next batch to send, or None: reports on, SEND_EVERY since the last, under DAY_CAP today, and only signatures
    that are new or counted more since they were last sent. Each is checked again before it may go, with `names` (or
    what it returns, when it is a function: read only when something is to go) taken out besides."""
    ensure(db)
    if not on(db):
        return None
    current = current or timeutil.clock()
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
        kept = own(location) and own_allowed(message)  # an own connector's label, as own_message made it
        scrubbed = message if kept else normalize(message, lowered)
        if scrubbed != message:
            db.execute('UPDATE error_feed SET message=? WHERE id=?', (scrubbed, sid))
        message = scrubbed
        if not (kept or allowed(message)) or not where(*(location.split(':') + [None])[:3]) or not KIND.fullmatch(kind):
            db.execute('UPDATE error_feed SET sent=count WHERE id=?', (sid,))  # never goes: not offered again
            continue
        out.append({'id': sid, 'source': source, 'kind': kind, 'message': message, 'where': location, 'version': version,
                    'count': count - done, 'total': count, 'first_seen': first_at, 'last_seen': last_at})
    return {'batch': 'eb_' + uuid.uuid4().hex[:20], 'signatures': out} if out else None


def sent(db, payload, current=None):
    """After the control plane took a batch: each signature counts as sent up to what went."""
    current = current or timeutil.clock()
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

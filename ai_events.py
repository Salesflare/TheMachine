"""Events for connected AIs: MCP Events with webhook delivery (docs/ai-connections.md, Events).

An AI that speaks MCP Events (ChatGPT today; any MCP client that subscribes with a webhook) can ask to be told when
something happens on this Machine, and start work on it. Nothing in here is about one AI: a connection is a connection.

- What it can watch (EVENTS): a new to-do for the owner, a meeting in the next day with its briefing ready, and a
  promise coming due. The payload is ids and short text only, the same text the read tools give that connection; the AI
  reads the rest through those tools, under the connection's access, area and Messages, as always.
- Off until the owner turns an event on for that connection (Settings, Apps, Connected AIs: ai_connections.events,
  ai_access.change). events/list names them all; events/subscribe to one that is off is refused, and logged.
- Never an echo (loops): a to-do an AI added (dedupe key ai:) is never a new to-do event, and no tool makes a meeting
  briefing or a promise. Changes an AI makes stay marked as its own, with Undo, as before.
- Subscriptions (ai_event_subs) are durable, kept per connection, url, name and arguments (canonical JSON), with a
  deterministic id. A grant lasts DEFAULT_TTL (an asked ttlMs between MIN_TTL and MAX_TTL), never past the connection's
  own end. They go when it is turned off, removed, expires, or the owner turns that event off; at most
  SUBS_PER_CONNECTION each.
- The callback: https only, no credentials or fragment. Before the first delivery to a url, a signed verification
  challenge it must echo (cached VERIFY_HOURS per connection and url). Every connection resolves the name, refuses
  anything that isn't a public address (private, loopback, link-local, shared, reserved, documentation, 6to4, Teredo,
  NAT64), connects to that address with TLS checked against the name, and never follows a redirect (Transport).
- Delivery: one event per request, at most BODY_MAX bytes, signed per Standard Webhooks (webhook-id, -timestamp,
  -signature; X-MCP-Subscription-Id), from the outbox (ai_event_outbox, sealed at rest). Retries on a network error,
  408, 429 and 5xx with doubling backoff, ATTEMPTS at most, the same event id each time; 410 ends the subscription,
  other answers end that event. PER_HOUR per connection (under ChatGPT's 30 task runs an hour): more waits its turn.
  An event older than STALE is dropped, never sent late.
- Every subscribe, refusal, stop and delivery is a line in the connection's Activity (ai_access.log)."""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import hmac
import http.client
import ipaddress
import json
import secrets
import socket
import ssl
import urllib.parse

import timeutil

DEFAULT_TTL = dt.timedelta(hours=24)
MIN_TTL = dt.timedelta(hours=1)        # a shorter ask is raised to this (refresh traffic)
MAX_TTL = dt.timedelta(days=7)
SUBS_PER_CONNECTION = 20
PER_HOUR = 20                          # deliveries per connection
ATTEMPTS = 6                           # per event: 1, 2, 4, 8, 16 minutes between them
BACKOFF = 60                           # seconds before the first retry
STALE = dt.timedelta(hours=24)         # an event this old is dropped instead of sent
PENDING_MOST = 50                      # events waiting per subscription; more wait in the source until there is room
ROUND_MOST = 50                        # deliveries per round of the worker
KEEP_DAYS = 7                          # sent and ended events, then they go
VERIFY_HOURS = 24
TIMEOUT = 10                           # seconds for each connect, send and answer
BODY_MAX = 256 * 1024
ANSWER_MAX = 64 * 1024
URL_MAX = 2048
WHY_CHARS = 280
ROTATION = dt.timedelta(minutes=10)    # a replaced signing secret still signs this long, next to the new one
# JSON-RPC errors, as ChatGPT's MCP Events integration numbers them
NOT_FOUND, FORBIDDEN, EXHAUSTED, UNSUPPORTED, CALLBACK = -32011, -32012, -32013, -32014, -32015

_AREA = {'type': 'string', 'enum': ['work', 'personal'], 'description': 'Only Work or only Personal; left out: whatever this connection may see.'}
_ARGS = {'type': 'object', 'properties': {'area': _AREA}, 'additionalProperties': False}
_OFF = ' Off until the owner turns it on for this connection in The Machine (Settings, Apps, Connected AIs).'


def _payload(properties, required):
    return {'type': 'object', 'properties': properties, 'required': list(required), 'additionalProperties': False}


_S, _N = {'type': 'string'}, {'type': ['string', 'null']}
# name -> (the owner's words for it, its description, its payload schema)
EVENTS = {
    'todo.created': ('New to-dos', 'A new to-do for the owner: one The Machine found in their messages and prepared, or '
                     'one they added. Not the ones a connected AI adds. Read it with get_todo.' + _OFF,
                     _payload({'todo_id': _S, 'title': _S, 'area': {'type': 'string', 'enum': ['work', 'personal']}, 'why': _S,
                               'link': _N}, ('todo_id', 'title', 'area', 'why', 'link'))),
    'meeting.briefing_ready': ('Meeting briefings', "A meeting in the next day has its briefing ready, as a to-do. Read it with "
                               'get_todo.' + _OFF,
                               _payload({'todo_id': _S, 'title': _S, 'area': {'type': 'string', 'enum': ['work', 'personal']},
                                         'starts_at': _S, 'link': _N}, ('todo_id', 'title', 'area', 'starts_at', 'link'))),
    'promise.due': ('Promises due', 'A promise the owner made, or one made to them, is due tomorrow. list_promises has the '
                    'rest.' + _OFF,
                    _payload({'promise_id': {'type': 'integer'}, 'direction': {'type': 'string', 'enum': ['mine', 'theirs']},
                              'who': _S, 'what': _S, 'due': _S, 'todo_id': _N},
                             ('promise_id', 'direction', 'who', 'what', 'due', 'todo_id'))),
}
NAMES = tuple(EVENTS)

SCHEMA = """
CREATE TABLE IF NOT EXISTS ai_event_subs(id TEXT PRIMARY KEY,connection_id TEXT NOT NULL,name TEXT NOT NULL,args TEXT NOT NULL,
  url TEXT NOT NULL,secret TEXT NOT NULL,old_secret TEXT,old_until TEXT,since TEXT NOT NULL,expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL,refreshed_at TEXT,UNIQUE(connection_id,url,name,args));
CREATE TABLE IF NOT EXISTS ai_event_seen(sub_id TEXT NOT NULL,item TEXT NOT NULL,at TEXT NOT NULL,PRIMARY KEY(sub_id,item));
CREATE TABLE IF NOT EXISTS ai_event_outbox(id TEXT NOT NULL,sub_id TEXT NOT NULL,at TEXT NOT NULL,body TEXT NOT NULL,
  todo_id TEXT,attempts INTEGER NOT NULL DEFAULT 0,next_at TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'wait',done_at TEXT,
  PRIMARY KEY(sub_id,id));
CREATE INDEX IF NOT EXISTS ai_event_outbox_next ON ai_event_outbox(state,next_at);
CREATE TABLE IF NOT EXISTS ai_event_verified(connection_id TEXT NOT NULL,url TEXT NOT NULL,at TEXT NOT NULL,PRIMARY KEY(connection_id,url));
"""
# ai_event_subs.since: what happened before it never fires; secret (and old_secret while rotating): the AI's signing
# key, sealed at rest (message_seal.DERIVED). ai_event_seen: what a subscription has queued, so nothing goes twice.
# ai_event_outbox.state: wait, sent, failed (gave up or refused) or dropped (stale); body: the exact event JSON.


class Failed(Exception):
    """A callback that could not take a request: reason is one of the spec's categories (connection_refused, timeout,
    tls_error, http_4xx, http_5xx, challenge_failed), never what the endpoint said."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def ensure(db):
    db.executescript(SCHEMA)


def _now():
    return timeutil.clock()


def _stamp(at=None):
    return (at or _now()).isoformat(timespec='seconds')


def _when(text):
    """An aware datetime from stored ISO text (naive is UTC), or None."""
    try:
        at = dt.datetime.fromisoformat(str(text).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)


def _zulu(at):
    return at.astimezone(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def enabled(connection):
    """The events the owner turned on for this connection (ai_connections.events: names, comma separated)."""
    try:
        value = connection['events'] if connection else ''
    except (KeyError, IndexError):  # a row from before the column
        value = ''
    return [n for n in str(value or '').split(',') if n in EVENTS]


def catalog():
    """events/list: every event, with its arguments and payload."""
    return [{'name': name, 'description': description, 'delivery': ['webhook'], 'inputSchema': _ARGS, 'payloadSchema': payload}
            for name, (_, description, payload) in EVENTS.items()]


def canonical(args):
    return json.dumps(args or {}, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def sub_id(connection_id, url, name, args):
    """Deterministic from the principal (the connection), the callback, the event and its arguments."""
    return 'sub_' + hashlib.sha256('\n'.join((connection_id, url, name, canonical(args))).encode()).hexdigest()[:32]


def event_id(sid, item):
    return 'evt_' + hashlib.sha256(f'{sid}\n{item}'.encode()).hexdigest()[:32]


def check_url(url):
    """The callback as given, or a ValueError: absolute https, a host, no credentials or fragment."""
    url = str(url or '')
    parts = urllib.parse.urlsplit(url)
    if len(url) > URL_MAX or parts.scheme != 'https' or not parts.hostname:
        raise ValueError('delivery.url must be an absolute https URL')
    if parts.username is not None or parts.password is not None or parts.fragment or any(c in url for c in ' \r\n\t'):
        raise ValueError('delivery.url must not carry credentials, a fragment or spaces')
    try:
        parts.port  # noqa: B018 - a bad port raises here
    except ValueError:
        raise ValueError('delivery.url has a bad port') from None
    return url


def check_secret(secret):
    """A whsec_ secret whose base64 is 24-64 bytes, or a ValueError."""
    text = str(secret or '')
    if not text.startswith('whsec_'):
        raise ValueError('delivery.secret must be a whsec_ signing secret')
    try:
        key = base64.b64decode(text[6:], validate=True)
    except ValueError:
        raise ValueError('delivery.secret is not base64') from None
    if not 24 <= len(key) <= 64:
        raise ValueError('delivery.secret must be 24 to 64 bytes')
    return text


def signature(secrets_, msg_id, timestamp, body):
    """The webhook-signature header: v1,<base64 HMAC-SHA256 of id.timestamp.body> for each secret, space separated."""
    signed = f'{msg_id}.{timestamp}.'.encode() + body
    return ' '.join('v1,' + base64.b64encode(hmac.new(base64.b64decode(s[6:]), signed, hashlib.sha256).digest()).decode()
                    for s in secrets_)


def check_args(name, args):
    if name not in EVENTS:
        raise LookupError('Unknown event')
    if args is None:
        args = {}
    if not isinstance(args, dict) or set(args) - {'area'}:
        raise ValueError('arguments can only be area')
    if 'area' in args and args['area'] not in ('work', 'personal'):
        raise ValueError('area is work or personal')
    return args


# ------------------------------------------------------------------ the callback: public addresses only

BLOCKED = tuple(ipaddress.ip_network(n) for n in (
    '0.0.0.0/8', '100.64.0.0/10', '192.0.0.0/24', '192.0.2.0/24', '192.88.99.0/24', '198.18.0.0/15', '198.51.100.0/24',
    '203.0.113.0/24', '240.0.0.0/4', '255.255.255.255/32', '2001::/23', '2001:db8::/32', '2002::/16', '3fff::/20',
    '64:ff9b::/96', '64:ff9b:1::/48', '100::/64', 'fc00::/7', 'fe80::/10', 'fec0::/10'))
GLOBAL_V6 = ipaddress.ip_network('2000::/3')


def public(address):
    """Whether a resolved address is one the callback may reach: a public unicast address, nothing else."""
    try:
        ip = ipaddress.ip_address(str(address).split('%', 1)[0])
    except ValueError:
        return False
    if ip.version == 6 and ip.ipv4_mapped:
        ip = ip.ipv4_mapped
    if (not ip.is_global or ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved
            or ip.is_unspecified):
        return False
    if any(ip in net for net in BLOCKED if net.version == ip.version):
        return False
    return ip.version == 4 or ip in GLOBAL_V6


class _Pinned(http.client.HTTPSConnection):
    """HTTPS to one checked address, TLS verified against the URL's own name (no second lookup: DNS rebinding)."""

    def __init__(self, host, address, port, context):
        super().__init__(host, port, timeout=TIMEOUT, context=context)
        self.address = address

    def connect(self):
        raw = socket.create_connection((self.address, self.port), TIMEOUT)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except BaseException:
            raw.close()
            raise


class Transport:
    """POSTs to a callback. resolve and allow are for tests (a fake subscriber on loopback); the Machine uses the real
    resolver and public(). No proxy, no redirect, a bounded answer."""

    def __init__(self, resolve=None, allow=public, context=None):
        self.resolve = resolve or (lambda host, port: [i[4][0] for i in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)])
        self.allow, self.context = allow, context or ssl.create_default_context()

    def post(self, url, body, headers):
        """(status, the answer's first ANSWER_MAX bytes), or Failed."""
        parts = urllib.parse.urlsplit(check_url(url))
        host, port = parts.hostname, parts.port or 443
        try:
            found = list(dict.fromkeys(self.resolve(host, port)))
        except OSError:
            raise Failed('connection_refused') from None
        if not found or not all(self.allow(a) for a in found):
            raise Failed('connection_refused')  # every address must be public, so a mixed answer can't slip one in
        path = (parts.path or '/') + ('?' + parts.query if parts.query else '')
        last = 'connection_refused'
        for address in found:
            conn = _Pinned(host, address, port, self.context)
            try:
                conn.request('POST', path, body=body, headers={**headers, 'Content-Length': str(len(body)), 'User-Agent': 'TheMachine-Events/1'})
                answer = conn.getresponse()
                return answer.status, answer.read(ANSWER_MAX)
            except (socket.timeout, TimeoutError):
                last = 'timeout'
            except ssl.SSLError:
                last = 'tls_error'
            except (OSError, http.client.HTTPException):
                last = 'connection_refused'
            finally:
                conn.close()
        raise Failed(last)


def verify(transport, sid, url, secret):
    """The handshake: a signed, single-use challenge the callback must echo in a 2xx. Failed otherwise."""
    challenge = secrets.token_urlsafe(32)
    body = json.dumps({'type': 'verification', 'challenge': challenge}, separators=(',', ':')).encode()
    msg_id = 'msg_verification_' + secrets.token_hex(12)
    status, answer = transport.post(url, body, _headers(sid, msg_id, body, [secret]))
    if not 200 <= status < 300:  # a redirect is never followed: it fails like any other answer
        raise Failed('http_5xx' if status >= 500 else 'http_4xx')
    try:
        echoed = json.loads(answer or b'null')
    except ValueError:
        echoed = None
    given = echoed.get('challenge') if isinstance(echoed, dict) else None
    if not isinstance(given, str) or not hmac.compare_digest(given.encode(), challenge.encode()):
        raise Failed('challenge_failed')


def _headers(sid, msg_id, body, secrets_):
    stamp = str(int(_now().timestamp()))
    return {'Content-Type': 'application/json', 'webhook-id': msg_id, 'webhook-timestamp': stamp,
            'webhook-signature': signature(secrets_, msg_id, stamp, body), 'X-MCP-Subscription-Id': sid}


# ------------------------------------------------------------------ subscriptions

def _granted(ttl_ms, connection_ends, at):
    """When a subscription ends: DEFAULT_TTL, or the asked ttlMs within MIN_TTL..MAX_TTL; never after the connection."""
    if isinstance(ttl_ms, bool) or not isinstance(ttl_ms, (int, float)) or ttl_ms <= 0:
        length = DEFAULT_TTL  # omitted, or null (no expiry is never granted: a finite grant, as the spec allows)
    else:
        length = min(max(dt.timedelta(milliseconds=ttl_ms), MIN_TTL), MAX_TTL)
    ends = _when(connection_ends)
    return min(at + length, ends) if ends else at + length


def subscribe(db, connection, params, transport):
    """events/subscribe: (its result, whether it is new) or Refused(code, message, data). The caller logs it. A
    refresh (the same connection, url, name and arguments) gets a new end and, when it brings one, the new secret."""
    name, args = params.get('name'), params.get('arguments')
    try:
        args = check_args(name, args)
    except LookupError:
        raise Refused(NOT_FOUND, 'Unknown event', {'kind': 'event'}) from None
    except ValueError as error:
        raise Refused(-32602, str(error)) from None
    if name not in enabled(connection):
        raise Refused(FORBIDDEN, 'This event is off for this connection. The owner can turn it on in The Machine: Settings, '
                                 'Apps, Connected AIs.', {'reason': 'event_off'})
    if args.get('area') and connection['area'] not in ('both', args['area']):
        raise Refused(FORBIDDEN, f"This connection can only see {connection['area'].capitalize()}")
    delivery = params.get('delivery') if isinstance(params.get('delivery'), dict) else {}
    if delivery.get('mode') != 'webhook':
        raise Refused(UNSUPPORTED, 'Only webhook delivery', {'feature': 'deliveryMode', 'value': delivery.get('mode')})
    try:
        url, secret = check_url(delivery.get('url')), check_secret(delivery.get('secret'))
    except ValueError as error:
        raise Refused(-32602, str(error)) from None
    at, key = _now(), canonical(args)
    row = db.execute('SELECT * FROM ai_event_subs WHERE connection_id=? AND url=? AND name=? AND args=?',
                     (connection['id'], url, name, key)).fetchone()
    if not row and db.execute('SELECT count(*) FROM ai_event_subs WHERE connection_id=?', (connection['id'],)).fetchone()[0] >= SUBS_PER_CONNECTION:
        raise Refused(EXHAUSTED, f'At most {SUBS_PER_CONNECTION} subscriptions per connection', {'limit': 'subscriptions', 'max': SUBS_PER_CONNECTION})
    sid = row['id'] if row else sub_id(connection['id'], url, name, args)
    if not db.execute('SELECT 1 FROM ai_event_verified WHERE connection_id=? AND url=? AND at>?',
                      (connection['id'], url, _stamp(at - dt.timedelta(hours=VERIFY_HOURS)))).fetchone():
        try:
            verify(transport, sid, url, secret)
        except Failed as error:
            raise Refused(CALLBACK, 'The callback did not pass verification', {'reason': error.reason}) from None
        db.execute('INSERT OR REPLACE INTO ai_event_verified(connection_id,url,at) VALUES(?,?,?)', (connection['id'], url, _stamp(at)))
    ends = _granted(params.get('ttlMs'), connection['expires_at'], at)
    if row:
        rotate = row['secret'] != secret
        db.execute('UPDATE ai_event_subs SET secret=?,old_secret=?,old_until=?,expires_at=?,refreshed_at=? WHERE id=?',
                   (secret, row['secret'] if rotate else row['old_secret'], _stamp(at + ROTATION) if rotate else row['old_until'],
                    _stamp(ends), _stamp(at), sid))
    else:
        db.execute('INSERT INTO ai_event_subs(id,connection_id,name,args,url,secret,since,expires_at,created_at) VALUES(?,?,?,?,?,?,?,?,?)',
                   (sid, connection['id'], name, key, url, secret, at.isoformat(), _stamp(ends), _stamp(at)))  # since: to the microsecond
    return {'id': sid, 'refreshBefore': _zulu(ends), 'cursor': None, 'truncated': False}, not row


def unsubscribe(db, connection, params):
    """events/unsubscribe: the matching subscription goes; none is fine (idempotent). Whether one went."""
    name, delivery = params.get('name'), params.get('delivery') if isinstance(params.get('delivery'), dict) else {}
    try:
        args = check_args(name, params.get('arguments'))
    except (LookupError, ValueError):
        return False
    row = db.execute('SELECT id FROM ai_event_subs WHERE connection_id=? AND url=? AND name=? AND args=?',
                     (connection['id'], str(delivery.get('url') or ''), name, canonical(args))).fetchone()
    if row:
        _drop(db, [row['id']])
    return bool(row)


class Refused(Exception):
    def __init__(self, code, message, data=None):
        super().__init__(message)
        self.code, self.message, self.data = code, message, data


def _drop(db, ids):
    for sid in ids:
        for sql in ('DELETE FROM ai_event_outbox WHERE sub_id=?', 'DELETE FROM ai_event_seen WHERE sub_id=?', 'DELETE FROM ai_event_subs WHERE id=?'):
            db.execute(sql, (sid,))


def end(db, connection_id, keep=None):
    """A connection's subscriptions end: all of them (turned off, removed), or those of events no longer in keep (the
    owner turned one off). Their waiting events go with them."""
    rows = db.execute('SELECT id,name FROM ai_event_subs WHERE connection_id=?', (connection_id,)).fetchall()
    _drop(db, [r['id'] for r in rows if keep is None or r['name'] not in keep])
    if keep is None:
        db.execute('DELETE FROM ai_event_verified WHERE connection_id=?', (connection_id,))


def moved(db, from_id, into_id):
    """A connection folded into another (ai_access.fold): its subscriptions go with its sign-ins."""
    for table in ('ai_event_subs', 'ai_event_verified'):
        db.execute(f'UPDATE OR IGNORE {table} SET connection_id=? WHERE connection_id=?', (into_id, from_id))
    end(db, from_id)


def watching(db, connection_id):
    """The events this connection has a live subscription to, for Settings."""
    rows = db.execute('SELECT DISTINCT name FROM ai_event_subs WHERE connection_id=? AND expires_at>?', (connection_id, _stamp())).fetchall()
    return sorted(r['name'] for r in rows)


def prune(db):
    at = _now()
    _drop(db, [r['id'] for r in db.execute('SELECT id FROM ai_event_subs WHERE expires_at<=?', (_stamp(at),))])
    db.execute("DELETE FROM ai_event_outbox WHERE state!='wait' AND done_at<?", (_stamp(at - dt.timedelta(days=KEEP_DAYS)),))
    db.execute('DELETE FROM ai_event_seen WHERE at<?', (_stamp(at - STALE * 2),))
    db.execute('DELETE FROM ai_event_verified WHERE at<?', (_stamp(at - dt.timedelta(hours=VERIFY_HOURS)),))


# ------------------------------------------------------------------ what happened (the App's data, each connection's view)

def _visible_at(row):
    made, held = _when(row['created_at']), _when(row['deliver_after'])
    return max(made, held) if made and held else made


def todos_created(app, db, connection, args, since, at):
    """(item, moment, data, todo id) of to-dos that came on the owner's screen since: open, not snoozed, in the area,
    never one an AI added (loops). Text as get_todo gives it (marked when it came from others)."""
    from machine import todo_states
    ids, want = app.ai_accounts(connection, args.get('area'))
    rows = db.execute(f"SELECT * FROM suggestions WHERE status IN ({','.join('?' * len(todo_states.OPEN_NOT_SNOOZED))}) "
                      "AND (created_at>=? OR deliver_after>=?) AND coalesce(dedupe_key,'') NOT LIKE 'ai:%' ORDER BY created_at LIMIT 500",
                      (*todo_states.OPEN_NOT_SNOOZED, _stamp(since - dt.timedelta(days=1)), _stamp(since))).fetchall()
    for r in rows:
        moment = _visible_at(r)
        if not moment or moment < since or moment > at or not app.ai_visible(r['account_ids'], ids, want, r['area']):
            continue
        item, source = app.ai_todo(r), app.ai_todo_source(r)
        why = _short(r['body'])  # shortened before it is marked, so the mark stays whole
        yield f"todo:{r['id']}", moment, {'todo_id': r['id'], 'title': item['title'], 'area': item['area'],
                                          'why': _untrusted(why, source) if source else why, 'link': item['link']}, r['id']


def briefings_ready(app, db, connection, args, since, at):
    """A meeting starting within the next day whose briefing (meeting_prep.py: a to-do) is open and in the area: once
    the briefing is on the screen and the meeting is a day away."""
    from machine import todo_states
    ids, want = app.ai_accounts(connection, args.get('area'))
    try:
        rows = db.execute(f"SELECT s.*,m.starts_at meeting_at FROM meeting_preps m JOIN suggestions s ON s.id=m.suggestion_id "
                          f"WHERE m.verdict='made' AND m.starts_at>? AND m.starts_at<? AND s.status IN ({','.join('?' * len(todo_states.OPEN_NOT_SNOOZED))})",
                          (_stamp(at), _stamp(at + dt.timedelta(days=2)), *todo_states.OPEN_NOT_SNOOZED)).fetchall()
    except Exception:  # noqa: BLE001 - no meeting briefings on this Machine yet
        return
    for r in rows:
        starts = _when(r['meeting_at'])
        shown = _visible_at(r)
        if not starts or not shown or starts <= at:
            continue
        moment = max(shown, starts - dt.timedelta(days=1))
        if moment < since or moment > at or not app.ai_visible(r['account_ids'], ids, want, r['area']):
            continue
        item = app.ai_todo(r)
        yield f"meeting:{r['id']}:{r['meeting_at']}", moment, {'todo_id': r['id'], 'title': item['title'], 'area': item['area'],
                                                               'starts_at': _zulu(starts), 'link': item['link']}, r['id']


def promises_due(app, db, connection, args, since, at):
    """An open promise due tomorrow, in the area, from the owner's morning the day before (or when it was noted, if
    later). Again when its date moves."""
    ids, want = app.ai_accounts(connection, args.get('area'))
    hour, minute = timeutil.hour_minute(timeutil.WORK_HOURS.get('morning') or '08:00')
    for p in app.store.promises():
        if p['state'] not in ('open', 'card') or not p.get('due') or (want is not None and p['account_id'] not in ids):
            continue
        try:
            due = dt.date.fromisoformat(p['due'])
        except ValueError:
            continue
        morning = dt.datetime.combine(due - dt.timedelta(days=1), dt.time(hour, minute), timeutil.local_tz())
        noted = _when(p.get('created_at'))
        moment = max(morning, noted) if noted else morning
        if moment < since or moment > at or due < at.astimezone(timeutil.local_tz()).date():
            continue
        yield f"promise:{p['id']}:{p['due']}", moment, {'promise_id': p['id'], 'direction': p['direction'], 'who': str(p['who'] or '')[:120],
                                                        'what': _untrusted(_short(p['what']), 'messages'), 'due': p['due'],
                                                        'todo_id': p.get('suggestion_id')}, p.get('suggestion_id')


SOURCES = {'todo.created': todos_created, 'meeting.briefing_ready': briefings_ready, 'promise.due': promises_due}


def _untrusted(text, source):
    """Text from other people, marked for the AI as the read tools mark it (ai_access.untrusted: the one marker)."""
    import ai_access  # it imports this module, so only when an event is made
    return ai_access.untrusted(text, source)


def _short(text):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= WHY_CHARS else text[:WHY_CHARS - 1].rstrip() + '…'


def usable(connection, at):
    return bool(connection) and connection['level'] != 'off' and connection['expires_at'] > _stamp(at)


def collect(app, db, connections, at=None):
    """Each live subscription's new events into the outbox (at most PENDING_MOST waiting each). Returns how many."""
    at, made = at or _now(), 0
    for sub in db.execute('SELECT * FROM ai_event_subs WHERE expires_at>? ORDER BY created_at', (_stamp(at),)).fetchall():
        connection = connections.get(sub['connection_id'])
        if not usable(connection, at) or sub['name'] not in enabled(connection):
            continue
        room = PENDING_MOST - db.execute("SELECT count(*) FROM ai_event_outbox WHERE sub_id=? AND state='wait'", (sub['id'],)).fetchone()[0]
        since = max(_when(sub['since']), at - STALE)
        for item, moment, data, todo in SOURCES[sub['name']](app, db, connection, json.loads(sub['args']), since, at):
            if room <= 0:
                break
            if db.execute('SELECT 1 FROM ai_event_seen WHERE sub_id=? AND item=?', (sub['id'], item)).fetchone():
                continue
            eid = event_id(sub['id'], item)
            body = json.dumps({'eventId': eid, 'name': sub['name'], 'timestamp': _zulu(moment), 'data': data, 'cursor': None},
                              ensure_ascii=False, separators=(',', ':'), allow_nan=False)
            db.execute('INSERT INTO ai_event_seen(sub_id,item,at) VALUES(?,?,?)', (sub['id'], item, _stamp(at)))
            if len(body.encode()) > BODY_MAX:
                continue
            db.execute('INSERT OR IGNORE INTO ai_event_outbox(id,sub_id,at,body,todo_id,next_at) VALUES(?,?,?,?,?,?)',
                       (eid, sub['id'], _stamp(moment), body, todo, _stamp(at)))
            room, made = room - 1, made + 1
    return made


def _sent_last_hour(db, connection_id, at):
    return db.execute("SELECT count(*) FROM ai_event_outbox o JOIN ai_event_subs s ON s.id=o.sub_id WHERE s.connection_id=? "
                      "AND o.state='sent' AND o.done_at>?", (connection_id, _stamp(at - dt.timedelta(hours=1)))).fetchone()[0]


def due(db, at):
    return db.execute("SELECT o.*,s.connection_id,s.name,s.url,s.secret,s.old_secret,s.old_until FROM ai_event_outbox o "
                      "JOIN ai_event_subs s ON s.id=o.sub_id WHERE o.state='wait' AND o.next_at<=? ORDER BY o.next_at,o.at LIMIT ?",
                      (_stamp(at), ROUND_MOST)).fetchall()


def deliver(db_open, transport, connections, log, at=None):
    """One round of the outbox. log(db, connection_id, outcome, row) writes its Activity line. Returns {state: n}."""
    at, counts = at or _now(), {}
    with db_open() as db:
        rows = [dict(r) for r in due(db, at)]
        sent = {}
    for row in rows:
        connection = connections.get(row['connection_id'])
        with db_open() as db:
            if not db.execute("SELECT 1 FROM ai_event_outbox WHERE sub_id=? AND id=? AND state='wait'", (row['sub_id'], row['id'])).fetchone():
                continue
            if not usable(connection, at) or row['name'] not in enabled(connection):
                end(db, row['connection_id'], keep=enabled(connection) if usable(connection, at) else None)
                counts['ended'] = counts.get('ended', 0) + 1
                continue
            if (_when(row['at']) or at) < at - STALE:
                db.execute("UPDATE ai_event_outbox SET state='dropped',done_at=? WHERE sub_id=? AND id=?", (_stamp(at), row['sub_id'], row['id']))
                counts['dropped'] = counts.get('dropped', 0) + 1
                continue
            if row['connection_id'] not in sent:
                sent[row['connection_id']] = _sent_last_hour(db, row['connection_id'], at)
            if sent[row['connection_id']] >= PER_HOUR:
                db.execute('UPDATE ai_event_outbox SET next_at=? WHERE sub_id=? AND id=?', (_stamp(at + dt.timedelta(minutes=5)), row['sub_id'], row['id']))
                counts['held'] = counts.get('held', 0) + 1
                continue
        keys = [row['secret']] + ([row['old_secret']] if row['old_secret'] and (row['old_until'] or '') > _stamp(at) else [])
        body = row['body'].encode()
        try:
            status, _ = transport.post(row['url'], body, _headers(row['sub_id'], row['id'], body, keys))
            reason = None
        except Failed as error:
            status, reason = None, error.reason
        with db_open() as db:
            if status is not None and 200 <= status < 300:
                db.execute("UPDATE ai_event_outbox SET state='sent',attempts=attempts+1,done_at=? WHERE sub_id=? AND id=?", (_stamp(at), row['sub_id'], row['id']))
                sent[row['connection_id']] += 1
                state = 'sent'
            elif status == 410:  # the subscriber is gone: so is the subscription
                _drop(db, [row['sub_id']])
                state = 'gone'
            elif status is None or status in (408, 429) or status >= 500:
                tries = row['attempts'] + 1
                state = 'failed' if tries >= ATTEMPTS else 'retry'
                db.execute('UPDATE ai_event_outbox SET attempts=?,next_at=?,state=?,done_at=? WHERE sub_id=? AND id=?',
                           (tries, _stamp(at + dt.timedelta(seconds=BACKOFF * 2 ** (tries - 1))), 'failed' if state == 'failed' else 'wait',
                            _stamp(at) if state == 'failed' else None, row['sub_id'], row['id']))
            else:  # 413, another 4xx, a redirect: never again
                db.execute("UPDATE ai_event_outbox SET state='failed',attempts=attempts+1,done_at=? WHERE sub_id=? AND id=?", (_stamp(at), row['sub_id'], row['id']))
                state = 'failed'
            if state != 'retry':
                log(db, row['connection_id'], state, row, reason or (f'HTTP {status}' if status else ''))
        counts[state] = counts.get(state, 0) + 1
    return counts

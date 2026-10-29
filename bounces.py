"""Email addresses that bounce, recorded per address so the rest of the app can use it (docs/help/graph.md, "Bounced").

Detection reads the structure of a delivery report, never its wording:

- a multipart/report (report-type=delivery-status) or any message/delivery-status part: per recipient its
  Final-Recipient (or Original-Recipient), Action and Status (RFC 3464). Gmail's "Delivery Status Notification",
  Outlook and Exchange's "Undeliverable:" reports and other mail servers' reports all have it;
- the X-Failed-Recipients header (Exim, Gmail), which only names recipients that failed for good;
- the original message's Message-ID from the attached message/rfc822 or text/rfc822-headers part, else the report's
  own In-Reply-To or References (Gmail threads the report with what bounced).

Only when a report has no recipient field is its text read, and then only for the failed address and its status code.
Messages collected before this existed keep only their text: a one-time pass (backfill) reads those from mail-system
senders (mailer-daemon, postmaster, Exchange's own sender) the same way, the report fields as they show in the text.

Kinds: a 5.x.x status (or Action: failed with no status) is a hard bounce, except a full mailbox (x.2.2) or a message
too large (x.3.4). 4.x.x and Action: delayed are soft: they count only when the same address soft-bounces three times
over seven days or more (SOFT_TIMES, SOFT_DAYS).

email_bounces holds the flag per address: when, which kind, the report's event and the original message. It clears by
itself (cleared_at) when a later message comes from that address, or a later send to it is not followed by a bounce
within 48 hours (CLEAR_HOURS). The owner's own addresses are never flagged.

Tables (CREATE TABLE IF NOT EXISTS only, beside the old ones)."""
from __future__ import annotations

import base64
import datetime as dt
import email.parser
import email.policy
import email.utils
import json
import re

SCHEMA = '''
CREATE TABLE IF NOT EXISTS email_bounce_events(event_id INTEGER NOT NULL,address TEXT NOT NULL,kind TEXT NOT NULL,status TEXT,
  original_id TEXT,thread_id TEXT,account_id TEXT,at TEXT NOT NULL,via TEXT NOT NULL,PRIMARY KEY(event_id,address));
CREATE INDEX IF NOT EXISTS email_bounce_events_address ON email_bounce_events(address,at);
CREATE TABLE IF NOT EXISTS email_bounces(address TEXT PRIMARY KEY,kind TEXT NOT NULL,status TEXT,bounced_at TEXT NOT NULL,event_id INTEGER,
  original_id TEXT,thread_id TEXT,account_id TEXT,cleared_at TEXT,cleared_by TEXT,cleared_event INTEGER,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS email_bounce_scan(id INTEGER PRIMARY KEY CHECK(id=1),last_event INTEGER NOT NULL,backfilled_at TEXT);
'''
SOFT_TIMES = 3           # soft bounces of one address that make it count
SOFT_DAYS = 7            # ...spread over at least this many days
CLEAR_HOURS = 48         # a send this long ago with no bounce since: the address works again
PER_PASS = 2000          # new messages read per pass
MAIL_KINDS = ('gmail.message',)
SOFT_PERMANENT = ('2.2', '3.4')  # x.2.2 mailbox full, x.3.4 message too large: about this message, not the address
SYSTEM = re.compile(r'^(?:mailer-daemon|mail-daemon|postmaster|microsoftexchange[0-9a-f]{32})@', re.I)
STATUS = re.compile(r'^([245])\.(\d{1,3})\.(\d{1,3})$')
ADDRESS = re.compile(r'[A-Za-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
CODE = re.compile(r'\b([245]\.\d{1,3}\.\d{1,3})\b')
FIELD = re.compile(r'^(final-recipient|original-recipient|action|status|diagnostic-code)\s*:\s*(.*)$', re.I)


def ensure(db):
    for statement in SCHEMA.split(';'):
        if statement.strip():
            db.execute(statement)


def _table(db):
    return bool(db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='email_bounces'").fetchone())


def parse_time(value):
    when = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    return when if when.tzinfo else when.replace(tzinfo=dt.timezone.utc)


def address_of(value):
    found = [a.strip().lower() for _, a in email.utils.getaddresses([str(value or '')]) if ADDRESS.fullmatch(a.strip())]
    return found[0] if found else ''


def addresses_in(value):
    if isinstance(value, list):
        value = ', '.join(map(str, value))
    return [a.strip().lower() for _, a in email.utils.getaddresses([str(value or '')]) if ADDRESS.fullmatch(a.strip())]


def system_sender(value):
    """A mail system's own sender (mailer-daemon, postmaster, Exchange's): who sends delivery reports."""
    return bool(SYSTEM.match(address_of(value)))


def kind_of(status, action=''):
    """'hard', 'soft' or None from a report's Status (x.y.z) and Action."""
    action = str(action or '').strip().lower()
    found = STATUS.match(str(status or '').strip())
    if action in ('delivered', 'relayed', 'expanded'):
        return None
    if action == 'delayed':
        return 'soft'
    if not found:
        return 'hard' if action == 'failed' else None
    if found[1] == '2':
        return None
    if found[1] == '4' or f'{found[2]}.{found[3]}' in SOFT_PERMANENT:
        return 'soft'
    return 'hard'


def _recipient(value):
    """An address from a Final-Recipient or Original-Recipient field ("rfc822; sam@example.com")."""
    value = str(value or '').split(';', 1)[-1].strip().strip('<>')
    return value.lower() if ADDRESS.fullmatch(value) else ''


def report_fields(text):
    """[{'address', 'action', 'status'}] from a delivery-status body: header blocks, one per recipient."""
    out, block = [], {}

    def flush():
        address = _recipient(block.get('final-recipient')) or _recipient(block.get('original-recipient'))
        if address:
            out.append({'address': address, 'action': (block.get('action') or '').strip().lower(), 'status': (block.get('status') or '').split()[0] if block.get('status') else ''})

    for line in str(text or '').replace('\r', '').split('\n'):
        if not line.strip():
            flush()
            block = {}
            continue
        found = FIELD.match(line.strip())
        if found:
            name = found[1].lower()
            if name in ('final-recipient', 'original-recipient') and block.get(name):
                flush()  # a new recipient without a blank line in between (a report's text as shown)
                block = {}
            block[name] = found[2]
    flush()
    seen, unique = set(), []
    for item in out:
        if item['address'] not in seen:
            seen.add(item['address'])
            unique.append(item)
    return unique


def _data(part):
    data = (part.get('body') or {}).get('data') or ''
    try:
        return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)).decode('utf-8', errors='replace')
    except ValueError:
        return ''


def _headers(part):
    return {h.get('name', '').lower(): str(h.get('value', '')) for h in part.get('headers') or ()}


def read_report(payload):
    """What a delivery report says, from Gmail's "full" payload (Outlook's comes in the same shape, ms_graph.payload):
    {'recipients': [{'address', 'kind', 'status'}], 'original_id', 'via'} or None when the message is no report."""
    payload = payload or {}
    top = _headers(payload)
    report = 'multipart/report' in top.get('content-type', '').lower() and 'delivery-status' in top.get('content-type', '').lower()
    fields, original, texts = [], '', []

    def walk(part):
        nonlocal report, original
        mime = str(part.get('mimeType') or '').lower()
        if mime in ('message/delivery-status', 'message/global-delivery-status'):
            report = True
            if part.get('parts'):  # parsed into header blocks (Outlook's MIME, ms_graph.payload)
                fields.extend(report_fields('\n\n'.join('\n'.join(f"{h.get('name')}: {h.get('value')}" for h in p.get('headers') or ()) for p in part['parts'])))
            fields.extend(report_fields(_data(part)))
        elif mime in ('message/rfc822', 'text/rfc822-headers', 'message/global', 'message/global-headers') and not original:
            inner = _headers(part.get('parts', [{}])[0]) if part.get('parts') else {}
            if not inner.get('message-id') and _data(part):
                inner = {k.lower(): str(v) for k, v in email.parser.HeaderParser(policy=email.policy.compat32).parsestr(_data(part)).items()}
            original = (inner.get('message-id') or '').strip()
        elif mime == 'text/plain' and not part.get('filename'):
            texts.append(_data(part))
        for child in part.get('parts') or ():
            walk(child)

    walk(payload)
    failed = addresses_in(top.get('x-failed-recipients', ''))
    if not report and not failed:
        return None
    recipients = []
    for f in fields:
        kind = kind_of(f['status'], f['action'])
        if kind:
            recipients.append({'address': f['address'], 'kind': kind, 'status': f['status'] or None})
    for address in failed:  # only permanent failures are named here
        if not any(r['address'] == address for r in recipients):
            recipients.append({'address': address, 'kind': 'hard', 'status': None})
    via = 'report' if fields else 'header' if failed else 'text'
    if not recipients and not fields:
        recipients = from_text('\n'.join(texts), loose=True)  # a report with no recipient fields: its text, for the address only
    if not original:
        original = (top.get('in-reply-to') or '').strip() or next(reversed((top.get('references') or '').split()), '')
    return {'recipients': recipients, 'original_id': original or None, 'via': via} if recipients else None


def from_text(text, loose=False):
    """The fallback when a report's structure can't be read: its fields as the text shows them. loose (only for a
    message whose structure says it is a report): else the addresses the text names, with the first status code in it."""
    found = report_fields(text)
    if found:
        return [{'address': f['address'], 'kind': k, 'status': f['status'] or None} for f in found for k in [kind_of(f['status'], f['action'])] if k]
    if not loose:
        return []
    codes = CODE.findall(str(text or ''))
    kind = kind_of(codes[0]) if codes else None
    if not kind:
        return []
    return [{'address': a.lower(), 'kind': kind, 'status': codes[0]} for a in dict.fromkeys(ADDRESS.findall(str(text or '')))][:3]


def from_event(event):
    """A collected message as a report: its own reading (metadata 'bounce', from the structure at collection), or for
    one collected before that, its text when it comes from a mail system's sender. None for anything else."""
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
    if event['kind'] not in MAIL_KINDS or 'SENT' in (m.get('labels') or ()):
        return None
    if isinstance(m.get('bounce'), dict):
        return m['bounce']
    if not system_sender(m.get('from')):
        return None
    recipients = from_text(event['body'] or '')
    if not recipients:
        return None
    return {'recipients': recipients, 'original_id': (m.get('in-reply-to') or '').strip() or None, 'via': 'text'}


# ------------------------------------------------------------------ recording

def record(db, event, found, own=()):
    """Keeps one report's recipients (email_bounce_events) and updates each address's flag. Returns the addresses that
    are flagged now ([(address, kind)]), the newly flagged ones first."""
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
    own = {str(o).lower() for o in own}
    flagged = []
    for r in found.get('recipients') or ():
        address = str(r.get('address') or '').lower()
        if not address or address in own or r.get('kind') not in ('hard', 'soft'):
            continue
        db.execute('INSERT OR IGNORE INTO email_bounce_events(event_id,address,kind,status,original_id,thread_id,account_id,at,via) VALUES(?,?,?,?,?,?,?,?,?)',
                   (event['id'], address, r['kind'], r.get('status'), found.get('original_id'), m.get('thread_id'), event['account_id'],
                    event['occurred_at'], found.get('via') or 'report'))
        kind = r['kind']
        if kind == 'soft':
            kind = 'soft' if repeated_soft(db, address) else None
        if not kind:
            continue
        row = db.execute('SELECT bounced_at,cleared_at FROM email_bounces WHERE address=?', (address,)).fetchone()
        if row and row['cleared_at'] is None and row['bounced_at'] >= event['occurred_at']:
            continue  # flagged already by this or a newer report
        if row and row['cleared_at'] and row['cleared_at'] > event['occurred_at']:
            continue  # cleared after this report: it's older news
        db.execute('INSERT INTO email_bounces(address,kind,status,bounced_at,event_id,original_id,thread_id,account_id,updated_at) VALUES(?,?,?,?,?,?,?,?,?) '
                   'ON CONFLICT(address) DO UPDATE SET kind=excluded.kind,status=excluded.status,bounced_at=excluded.bounced_at,event_id=excluded.event_id,'
                   'original_id=excluded.original_id,thread_id=excluded.thread_id,account_id=excluded.account_id,cleared_at=NULL,cleared_by=NULL,'
                   'cleared_event=NULL,updated_at=excluded.updated_at',
                   (address, kind, r.get('status'), event['occurred_at'], event['id'], found.get('original_id'), m.get('thread_id'), event['account_id'],
                    event['occurred_at']))
        flagged.append((address, kind, not row or row['cleared_at'] is not None))
    return [(a, k) for a, k, new in sorted(flagged, key=lambda x: not x[2])]


def repeated_soft(db, address):
    """Three soft bounces or more of one address since it last worked, spread over seven days or more."""
    row = db.execute('SELECT cleared_at FROM email_bounces WHERE address=?', (address,)).fetchone()
    since = row['cleared_at'] if row and row['cleared_at'] else ''
    times = [r[0] for r in db.execute("SELECT at FROM email_bounce_events WHERE address=? AND kind='soft' AND at>? ORDER BY at", (address, since))]
    return len(times) >= SOFT_TIMES and (parse_time(times[-1]) - parse_time(times[0])) >= dt.timedelta(days=SOFT_DAYS)


def scan(db, own=(), limit=PER_PASS):
    """Reads the messages collected since the last pass for reports and records them. The first pass is the one-time
    backfill: every message collected before, from mail systems' senders. Returns [(event_id, address, kind)] flagged."""
    ensure(db)
    state = db.execute('SELECT last_event,backfilled_at FROM email_bounce_scan WHERE id=1').fetchone()
    out = []
    if state is None:
        top = db.execute('SELECT coalesce(max(id),0) FROM events').fetchone()[0]
        rows = db.execute("SELECT * FROM events WHERE kind='gmail.message' AND deleted=0 AND id<=? AND ("
                          "lower(json_extract(metadata,'$.from')) LIKE '%mailer-daemon@%' OR lower(json_extract(metadata,'$.from')) LIKE '%mail-daemon@%' "
                          "OR lower(json_extract(metadata,'$.from')) LIKE '%postmaster@%' OR lower(json_extract(metadata,'$.from')) LIKE '%microsoftexchange%') "
                          'ORDER BY occurred_at,id', (top,)).fetchall()
        for row in rows:
            out += _one(db, row, own)
        db.execute("INSERT INTO email_bounce_scan(id,last_event,backfilled_at) VALUES(1,?,strftime('%Y-%m-%dT%H:%M:%SZ','now'))", (top,))
        return out
    rows = db.execute("SELECT * FROM events WHERE id>? AND kind='gmail.message' AND deleted=0 ORDER BY id LIMIT ?", (state['last_event'], limit)).fetchall()
    for row in rows:
        out += _one(db, row, own)
    if rows:
        db.execute('UPDATE email_bounce_scan SET last_event=? WHERE id=1', (rows[-1]['id'],))
    return out


def _one(db, row, own):
    try:
        found = from_event(row)
    except (ValueError, TypeError):
        return []
    if not found:
        return []
    return [(row['id'], address, kind) for address, kind in record(db, dict(row), found, own)]


def clear(db, now, own=()):
    """Clears a flag when the address works again: a later message from it, or a later send to it with no bounce of it
    within CLEAR_HOURS. Returns [(address, how)]."""
    if not _table(db):
        return []
    cleared = []
    settled = (parse_time(now) - dt.timedelta(hours=CLEAR_HOURS)).isoformat()
    for b in db.execute('SELECT * FROM email_bounces WHERE cleared_at IS NULL').fetchall():
        address = b['address']
        bounce_ids = {r[0] for r in db.execute('SELECT event_id FROM email_bounce_events WHERE address=?', (address,))}
        how = None
        for r in db.execute("SELECT id,occurred_at,metadata FROM events WHERE kind='gmail.message' AND deleted=0 AND occurred_at>? "
                            "AND (instr(lower(json_extract(metadata,'$.from')),?)>0 OR instr(lower(json_extract(metadata,'$.to')),?)>0 "
                            "OR instr(lower(json_extract(metadata,'$.cc')),?)>0) ORDER BY occurred_at", (b['bounced_at'], address, address, address)):
            if r['id'] in bounce_ids:
                continue
            m = json.loads(r['metadata']) if isinstance(r['metadata'], str) else r['metadata']
            sent = 'SENT' in (m.get('labels') or ()) or address_of(m.get('from')) in own
            if not sent and address_of(m.get('from')) == address:
                how = ('reply', r['id'], r['occurred_at'])
                break
            if sent and address in addresses_in(m.get('to')) + addresses_in(m.get('cc')) and r['occurred_at'] <= settled:
                later = db.execute('SELECT 1 FROM email_bounce_events WHERE address=? AND at>? AND at<=?',
                                   (address, r['occurred_at'], (parse_time(r['occurred_at']) + dt.timedelta(hours=CLEAR_HOURS)).isoformat())).fetchone()
                if not later:
                    how = ('delivered', r['id'], r['occurred_at'])
                    break
        if how:
            db.execute('UPDATE email_bounces SET cleared_at=?,cleared_by=?,cleared_event=?,updated_at=? WHERE address=?', (how[2], how[0], how[1], now, address))
            cleared.append((address, how[0]))
    return cleared


# ------------------------------------------------------------------ reading

def flags(db, addresses):
    """{address: {'at', 'kind', 'status', 'event_id'}} for the ones flagged now."""
    wanted = sorted({str(a).lower() for a in addresses if a})
    if not wanted or not _table(db):
        return {}
    marks = ','.join('?' for _ in wanted)
    return {r['address']: {'at': r['bounced_at'], 'kind': r['kind'], 'status': r['status'], 'event_id': r['event_id']}
            for r in db.execute(f'SELECT * FROM email_bounces WHERE cleared_at IS NULL AND address IN ({marks})', wanted)}


def bounce_event_ids(db, ids):
    """The ids among these that are delivery reports."""
    ids = [int(i) for i in ids]
    if not ids or not _table(db):
        return set()
    return {r[0] for r in db.execute(f"SELECT DISTINCT event_id FROM email_bounce_events WHERE event_id IN ({','.join('?' * len(ids))})", ids)}


def person_emails(db, address):
    """The emails of the person this address is theirs: the shown ones (the messages', the owner's own), in order."""
    import graph
    try:
        row = graph.resolve(db, 'email:' + str(address).lower())
    except Exception:  # noqa: BLE001 - no graph yet
        row = None
    if not row:
        return [str(address).lower()]
    info = json.loads(row['info'] or '{}')
    found = [str(e.get('value') if isinstance(e, dict) else e).lower() for e in info.get('emails') or ()]
    found += [i.split(':', 1)[1].lower() for i in info.get('identifiers') or () if str(i).startswith('email:')]
    return list(dict.fromkeys([a for a in found if ADDRESS.fullmatch(a)] or [str(address).lower()]))


def working(db, address):
    """Another address of the same person that hasn't bounced, or None."""
    others = [a for a in person_emails(db, address) if a != str(address).lower()]
    bad = flags(db, others)
    return next((a for a in others if a not in bad), None)


def steer(db, raw, options):
    """A draft's recipients before it is checked (next_actions.validate): a bounced To becomes the same person's working
    address when they have one; the thread's addresses to pick from list working ones first. Returns (raw, options)."""
    if not _table(db):
        return raw, options
    options = list(options or [])
    bad = flags(db, options)
    if bad:
        swapped = []
        for o in options:
            swapped.append(working(db, o) or o if o in bad else o)
        options = sorted(dict.fromkeys(swapped), key=lambda o: o in bad)

    def one(action):
        if not isinstance(action, dict) or action.get('kind') != 'email' or not isinstance(action.get('to'), list):
            return action
        to = [str(a) for a in action['to']]
        bad_to = flags(db, to)
        if not bad_to:
            return action
        taken = {a.lower() for a in to + list(action.get('cc') or []) + list(action.get('bcc') or []) if isinstance(a, str)}
        out = []
        for a in to:
            alt = working(db, a) if a.lower() in bad_to else None
            if alt and alt not in taken:
                out.append(alt)
                taken.add(alt)
            elif alt:
                continue  # the working one is on it already
            else:
                out.append(a)
        return {**action, 'to': out}

    if isinstance(raw, list):
        raw = [one(a) for a in raw]
    elif isinstance(raw, dict) and isinstance(raw.get('choices'), list):
        raw = {**raw, 'choices': [one(a) for a in raw['choices']]}
    else:
        raw = one(raw)
    return raw, options


def moved(db, to):
    """{address: the bounced one it stands in for}: a draft's To that is a working address of someone whose other address
    bounced ("Bounced, now to <address>")."""
    to = addresses_in(to)
    if not to or not _table(db):
        return {}
    out = {}
    # From each bounced address to its person's other ones (an address the owner added is no identifier to look up by)
    for r in db.execute('SELECT address FROM email_bounces WHERE cleared_at IS NULL ORDER BY bounced_at'):
        for other in person_emails(db, r['address']):
            if other in to and other != r['address']:
                out[other] = r['address']
    bad = flags(db, list(out))
    return {a: b for a, b in out.items() if a not in bad}


def mark_draft(db, action):
    """A draft as the send sheet shows it: 'bounced' {address: when} for its recipients that bounced, 'moved' {address:
    the bounced one} when it goes to someone's working address instead of one that bounced."""
    if not isinstance(action, dict) or action.get('kind') != 'email':
        return action
    found = flags(db, list(action.get('to') or []) + list(action.get('to_options') or []))
    instead = moved(db, action.get('to') or [])
    if found:
        action = {**action, 'bounced': {a: f['at'] for a, f in found.items()}}
    if instead:
        action = {**action, 'moved': instead}
    return action


def retarget(db, action):
    """A ready email draft whose To bounced, sent to the same person's working address instead: the draft under a new
    revision (so it waits for the owner's Send again), or None when there is no working address to move to."""
    if not isinstance(action, dict) or action.get('kind') != 'email':
        return None
    new = steer(db, action, [])[0]
    if [str(a).lower() for a in new.get('to') or ()] == [str(a).lower() for a in action.get('to') or ()]:
        return None
    import hashlib
    import next_actions
    new = {k: v for k, v in new.items() if k != 'revision'}
    new['revision'] = hashlib.sha256(next_actions.canonical(new).encode()).hexdigest()[:12]
    return new


def requeue_lookup(db, address):
    """A bounced person is looked up again by people enrichment (person_profiles): their work contact is due now."""
    try:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='person_profiles'").fetchone():
            return 0
        ids = ['email:' + a for a in person_emails(db, address)]
        marks = ','.join('?' for _ in ids)
        return db.execute(f"UPDATE person_profiles SET fetched_at='1970-01-01T00:00:00+00:00' WHERE identifier IN ({marks}) AND status<>'error'", ids).rowcount
    except Exception:  # noqa: BLE001 - a lookup is a bonus, never a reason to fail
        return 0


def matters(db, event_id, address):
    """Why a bounce on this report matters, for the review: {'projects': [open projects on its thread], 'awaited':
    a to-do's email that waits for their reply} or {}."""
    row = db.execute('SELECT thread_id,original_id,account_id FROM email_bounce_events WHERE event_id=? AND address=?', (event_id, address)).fetchone()
    if not row:
        return {}
    out = {}
    if row['thread_id']:
        names = [r[0] for r in db.execute(
            "SELECT DISTINCT p.name FROM events e JOIN event_projects ep ON ep.event_id=e.id JOIN projects p ON p.id=ep.project_id "
            "WHERE e.kind='gmail.message' AND e.account_id=? AND json_extract(e.metadata,'$.thread_id')=? AND p.closed_at IS NULL "
            "AND (p.outcome IS NULL OR p.outcome='')", (row['account_id'], row['thread_id']))]
        if names:
            out['projects'] = names[:3]
    try:  # an email sent from a to-do, in that thread: its reply is awaited (the payload is read in Python: it may be sealed)
        jobs = db.execute("SELECT j.suggestion_id,j.rfc_message_id,j.payload,s.title FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id "
                          "WHERE j.status='sent' ORDER BY j.updated_at DESC LIMIT 500").fetchall()
    except Exception:  # noqa: BLE001 - no outbox: the projects are enough
        jobs = []
    for j in jobs:
        try:
            payload = json.loads(j['payload'] or '{}')
        except (TypeError, ValueError):
            continue
        if payload.get('kind') != 'email':
            continue
        if (row['original_id'] and j['rfc_message_id'] == row['original_id']) or (
                row['thread_id'] and payload.get('thread_id') == row['thread_id'] and payload.get('account_id') == row['account_id']):
            out['awaited'] = {'suggestion_id': j['suggestion_id'], 'title': j['title']}
            break
    return out


def hint(db, event_id):
    """What a review sees on a delivery report: who it bounced for, whether it matters, and their other address."""
    rows = db.execute('SELECT address,kind,status FROM email_bounce_events WHERE event_id=?', (int(event_id),)).fetchall() if _table(db) else []
    out = []
    for r in rows:
        import graph
        person = graph.resolve(db, 'email:' + r['address'])
        item = {'address': r['address'], 'kind': r['kind'], 'person': person['name'] if person else None,
                'person_id': person['id'] if person else None, 'other_address': working(db, r['address'])}
        item.update(matters(db, event_id, r['address']))
        out.append(item)
    return out

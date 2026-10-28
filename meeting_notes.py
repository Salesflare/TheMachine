"""Meeting notes and the calendar meeting they belong to: a Zoom AI Companion summary (connectors/zoom.py), or notes
added to the meeting itself (ADDED: pasted or uploaded by the owner on the meeting in the Calendar, or saved by a Do it
run, for example a transcript someone sent).

Added notes are a signal of their own (kind meeting.notes) on the meeting's own calendar account, so they are Work or
Personal as the meeting is, are reviewed like other notes, and go to the team only as the meeting does
(shared_graph.py). They carry the meeting's guests, so sharing judges them by the same people. One per meeting
(source_id notes:<the meeting's event id>): saving again replaces them, or adds below them.

Zoom notes are matched by plain code, never by a model: the Zoom meeting ID in the calendar event (its join link or "Meeting ID" in the
location or description) at about the same time; else the time alone (start within a few minutes, or mostly
overlapping), preferring the event the notes' host was in. Two events that fit equally well match neither: no notes is
better than another meeting's notes. What the notes say is read by the review, which judges it by meaning."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re

ADDED = 'meeting.notes'
KINDS = ('zoom.summary', ADDED)
SOURCE = {'zoom.summary': 'Zoom', ADDED: 'Meeting'}
MAX_CHARS = 400_000  # a long meeting's full transcript fits
READ_CHARS = 20_000  # one read of the notes for a tool result; the rest with offset
SAME_ID_HOURS = 3  # a recurring Zoom meeting keeps its ID: the same ID only counts at about the same time
NEAR_MINUTES = 20
LINK = re.compile(r'zoom\.us/(?:j|w|s|wc/join)/(\d{9,12})\b', re.I)
SPOKEN = re.compile(r'Meeting\s+ID\s*:?\s*(\d{3}[\s-]?\d{3,4}[\s-]?\d{3,5})\b', re.I)


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def zoom_ids(*texts):
    """The Zoom meeting IDs a calendar event names, as digits."""
    found = set()
    for text in texts:
        text = str(text or '')
        found |= set(LINK.findall(text))
        found |= {re.sub(r'\D', '', m) for m in SPOKEN.findall(text)}
    return found


def _span(event):
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
    start = stamp(event['occurred_at'])
    end = stamp(m.get('end_at')) or (start + dt.timedelta(hours=1) if start else None)
    return start, end, m


def _people(m):
    emails = {str((m.get('organizer') or {}).get('email') or '').lower()}
    emails |= {str(a.get('email') or '').lower() for a in m.get('attendees') or [] if isinstance(a, dict)}
    return emails - {''}


def candidates(db, start):
    """Calendar events around the notes' start (a day either side; times are compared parsed, not as text)."""
    rows = db.execute("SELECT id,source_id,title,body,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                      'AND occurred_at>=? AND occurred_at<=?',
                      ((start - dt.timedelta(days=1)).isoformat(), (start + dt.timedelta(days=1)).isoformat())).fetchall()
    return [dict(r) for r in rows]


def match(db, notes):
    """The calendar event (a dict with id, title, occurred_at, metadata) these notes are of, or None."""
    if notes.get('kind') == ADDED:  # added to the meeting itself: that meeting, while it is there
        found = meeting(db, _meeting_id(notes.get('source_id')))
        return dict(found) if found else None
    m = notes['metadata'] if isinstance(notes['metadata'], dict) else json.loads(notes['metadata'] or '{}')
    start = stamp(m.get('start_at')) or stamp(notes['occurred_at'])
    if not start:
        return None
    end = stamp(m.get('end_at')) or start + dt.timedelta(hours=1)
    meeting_id = re.sub(r'\D', '', str(m.get('meeting_id') or ''))
    host = str(m.get('host_email') or '').lower()
    by_id, by_time = [], []
    for event in candidates(db, start):
        begun, ended, em = _span(event)
        if not begun or em.get('all_day') or em.get('status') == 'cancelled':
            continue
        if meeting_id and meeting_id in zoom_ids(em.get('location'), event.get('body')) and abs(begun - start) <= dt.timedelta(hours=SAME_ID_HOURS):
            by_id.append((abs(begun - start), event))
            continue
        overlap = (min(end, ended) - max(start, begun)).total_seconds()
        if abs(begun - start) <= dt.timedelta(minutes=NEAR_MINUTES) or overlap >= 0.5 * max(60, (end - start).total_seconds()):
            by_time.append((host in _people(em), event))
    if by_id:
        by_id.sort(key=lambda x: x[0])
        return by_id[0][1] if len(by_id) == 1 or by_id[0][0] < by_id[1][0] else None
    if host and any(hosted for hosted, _ in by_time):
        by_time = [x for x in by_time if x[0]]
    return by_time[0][1] if len(by_time) == 1 else None


def for_event(db, event_id, day):
    """The newest notes that match calendar event `event_id` (its day as YYYY-MM-DD), or None."""
    start = dt.date.fromisoformat(day)
    rows = db.execute(f"SELECT id,kind,source_id,title,occurred_at,metadata FROM events WHERE kind IN ({','.join('?' * len(KINDS))}) AND deleted=0 "
                      f"AND occurred_at>=? AND occurred_at<? ORDER BY kind='{ADDED}' DESC,occurred_at DESC",
                      (*KINDS, (start - dt.timedelta(days=1)).isoformat(), (start + dt.timedelta(days=2)).isoformat())).fetchall()
    for notes in rows:
        found = match(db, dict(notes))
        if found and found['id'] == event_id:
            return dict(notes)
    return None


# ------------------------------------------------------------------ notes added to a meeting
def _meeting_id(source_id):
    m = re.fullmatch(r'notes:(\d+)', str(source_id or ''))
    return int(m[1]) if m else None


def meeting(db, event_id):
    """The calendar meeting with this events id, or None."""
    try:
        event_id = int(event_id)
    except (TypeError, ValueError):
        return None
    return db.execute("SELECT id,account_id,source_id,title,body,occurred_at,metadata FROM events WHERE id=? AND kind='calendar.event' AND deleted=0",
                      (event_id,)).fetchone()


def added(db, event):
    """The notes added to this meeting (a row of `meeting`), or None."""
    return db.execute('SELECT id,title,body,occurred_at,metadata,ingested_at FROM events WHERE account_id=? AND source_id=? AND kind=? AND deleted=0',
                      (event['account_id'], f"notes:{event['id']}", ADDED)).fetchone()


def added_for(db, event_ids):
    """{meeting event id: {by, at, chars}} for those of these meetings that have notes added: the Calendar's marker."""
    ids = sorted({int(i) for i in event_ids})
    if not ids:
        return {}
    out = {}
    for r in db.execute('SELECT source_id,body,metadata FROM events WHERE kind=? AND deleted=0 AND source_id IN (SELECT ? || value FROM json_each(?))',
                        (ADDED, 'notes:', json.dumps(ids))):
        m = json.loads(r['metadata'] or '{}')
        out[_meeting_id(r['source_id'])] = {'by': m.get('added_by') or 'owner', 'at': m.get('added_at'), 'chars': len(r['body'] or '')}
    return out


def clean(text):
    """The notes as given: line endings made plain and the ends trimmed; Markdown stays as it is."""
    text = str(text or '').replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '')
    return text.strip('\n').rstrip()


def plan(db, event_id, text, by, at, append=False):
    """What saving notes on a meeting changes: (result, write). Adds them, or replaces the ones it has (append: below
    them); empty text removes them. by: 'owner' or 'machine'. write is None (nothing changes), ('remove', notes id),
    ('update', notes id, row) or ('insert', row): Store.save_meeting_notes makes it, as only assistant.py writes
    events (sealed). The notes become a new version of their signal, so the next review reads them."""
    event = meeting(db, event_id)
    if not event:
        raise ValueError('No meeting with that event_id. Find it with day (and query) first')
    text = clean(text)
    old = added(db, event)
    if append and old and text:
        text = old['body'].rstrip() + '\n\n' + text
    if len(text) > MAX_CHARS:
        raise ValueError(f'Notes can be up to {MAX_CHARS:,} characters')
    source_id = f"notes:{event['id']}"
    if not text:
        return {'event_id': event['id'], 'title': event['title'], 'removed': bool(old)}, ('remove', old['id']) if old else None
    em = json.loads(event['metadata'] or '{}')
    people = lambda a: {k: a[k] for k in ('email', 'displayName', 'self', 'resource', 'responseStatus') if k in a}
    meta = {'event_id': event['id'], 'start_at': event['occurred_at'], 'end_at': em.get('end_at'), 'format': 'markdown',
            'added_by': 'owner' if by == 'owner' else 'machine', 'added_at': at,
            # the meeting's people, so sharing judges the notes by the same people as the meeting
            **({'organizer': people(em['organizer'])} if isinstance(em.get('organizer'), dict) else {}),
            'attendees': [people(a) for a in em.get('attendees') or [] if isinstance(a, dict)][:200]}
    digest = hashlib.sha256(text.encode()).hexdigest()
    row = db.execute('SELECT id,content_hash,deleted FROM events WHERE account_id=? AND source_id=?', (event['account_id'], source_id)).fetchone()
    result = {'event_id': event['id'], 'title': event['title'], 'chars': len(text)}
    if row and row['content_hash'] == digest and not row['deleted']:
        return {**result, 'notes_id': row['id'], 'unchanged': True}, None
    record = {'account_id': event['account_id'], 'source_id': source_id, 'kind': ADDED, 'occurred_at': event['occurred_at'], 'title': event['title'],
              'body': text, 'metadata': json.dumps(meta), 'content_hash': digest, 'ingested_at': at}
    return ({**result, **({'replaced': True} if old and not append else {}), **({'appended': True} if old and append else {})},
            ('update', row['id'], record) if row else ('insert', record))


def read(db, event_id, offset=0, limit=READ_CHARS):
    """A meeting and its notes: the ones added to it ({text, by, at, chars, next_offset}) and the Zoom summary that
    matches it ({title, text, url}), each None when there is none."""
    event = meeting(db, event_id)
    if not event:
        raise ValueError('No meeting with that event_id')
    out = {'event_id': event['id'], 'title': event['title'], 'start': event['occurred_at'], 'notes': None, 'zoom': None}
    row = added(db, event)
    if row:
        m, body = json.loads(row['metadata'] or '{}'), row['body'] or ''
        offset = max(0, int(offset or 0))
        end = offset + max(1, int(limit))
        out['notes'] = {'id': row['id'], 'text': body[offset:end], 'by': m.get('added_by') or 'owner', 'at': m.get('added_at') or row['ingested_at'],
                        'chars': len(body), 'next_offset': end if end < len(body) else None}
    start = stamp(event['occurred_at'])
    if start:
        day = start.date().isoformat()
        zoom = next((n for n in [for_zoom(db, event['id'], day)] if n), None)
        if zoom:
            zm = json.loads(zoom['metadata'] or '{}') if not isinstance(zoom['metadata'], dict) else zoom['metadata']
            url = zm.get('source_url')
            out['zoom'] = {'id': zoom['id'], 'title': zoom['title'], 'text': str(zoom.get('body') or '')[:READ_CHARS],
                           'url': url if isinstance(url, str) and url.startswith('https://') else None}
    return out


def for_zoom(db, event_id, day):
    """The newest Zoom summary that matches this meeting (for_event, Zoom only), with its body."""
    start = dt.date.fromisoformat(day)
    for notes in db.execute("SELECT id,kind,source_id,title,body,occurred_at,metadata FROM events WHERE kind='zoom.summary' AND deleted=0 "
                            'AND occurred_at>=? AND occurred_at<? ORDER BY occurred_at DESC',
                            ((start - dt.timedelta(days=1)).isoformat(), (start + dt.timedelta(days=2)).isoformat())).fetchall():
        found = match(db, dict(notes))
        if found and found['id'] == event_id:
            return dict(notes)
    return None


def meetings_on(db, account_ids, day, tz, query=''):
    """The meetings on one day (YYYY-MM-DD, in the owner's time zone tz), for finding the one notes belong to:
    [{event_id, title, start, end, has_notes}], optionally only those whose title has `query`."""
    first = dt.datetime.combine(dt.date.fromisoformat(str(day)), dt.time(), tz)
    last = first + dt.timedelta(days=1)
    if not account_ids:
        return []
    rows = db.execute("SELECT id,account_id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 "
                      'AND account_id IN (SELECT value FROM json_each(?)) AND occurred_at>=? AND occurred_at<? ORDER BY occurred_at,id LIMIT 200',
                      (json.dumps(sorted(account_ids)), (first - dt.timedelta(days=1)).astimezone(dt.timezone.utc).isoformat(),
                       last.astimezone(dt.timezone.utc).isoformat())).fetchall()
    words = str(query or '').casefold().split()
    out = []
    for r in rows:
        start = stamp(r['occurred_at'])
        m = json.loads(r['metadata'] or '{}')
        end = stamp(m.get('end_at')) or start
        if not start or not (start < last and end >= first) or m.get('status') == 'cancelled':
            continue
        if words and not all(w in str(r['title'] or '').casefold() for w in words):
            continue
        out.append({'event_id': r['id'], 'title': r['title'], 'start': r['occurred_at'], 'end': m.get('end_at') or r['occurred_at']})
    have = added_for(db, [o['event_id'] for o in out])
    for o in out:
        o['has_notes'] = o['event_id'] in have
    return out

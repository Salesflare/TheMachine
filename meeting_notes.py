"""A meeting's two records, kept apart: its Notes (a summary, decisions, action items; written by a person or an AI) and
its Transcript (the verbatim record of what was said). Each comes from the meeting app (connectors/zoom.py: the AI
Companion summary is Notes, the transcript is Transcript; connectors/google_meet.py: Gemini's notes are Notes, the
transcript is Transcript) or is added to the meeting itself (pasted or uploaded by the owner on the meeting in the
Calendar, or saved by a Do it run). The owner's and the app's never replace each other: when both are there, both
show, each with its source.

Added ones are a signal each (kind meeting.notes, meeting.transcript) on the meeting's own calendar account, so they
are Work or Personal as the meeting is, are reviewed like other notes, and go to the team only as the meeting does
(shared_graph.py). They carry the meeting's guests, so sharing judges them by the same people. One of each per meeting
(source_id notes:<the meeting's event id>, transcript:<the meeting's event id>): saving again replaces it, or adds
below it. Text is never moved from one to the other on its own, except once for notes saved before the two were apart
(transcript_moves, at the start).

The app's are matched by plain code, never by a model: the Zoom meeting ID in the calendar event (its join link or "Meeting ID" in the
location or description) at about the same time; else the time alone, all Google Meet gives (start within a few minutes, or mostly
overlapping), preferring the event the notes' host was in. Two events that fit equally well match neither: no notes is
better than another meeting's notes. What the notes say is read by the review, which judges it by meaning."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re

NOTES, TRANSCRIPT = 'meeting.notes', 'meeting.transcript'
ADDED = NOTES
FIELDS = {'notes': NOTES, 'transcript': TRANSCRIPT}  # the field's name in the API, and its kind
PREFIX = {NOTES: 'notes:', TRANSCRIPT: 'transcript:'}
ZOOM = {'notes': 'zoom.summary', 'transcript': 'zoom.transcript'}
GOOGLE_MEET = {'notes': 'google_meet.notes', 'transcript': 'google_meet.transcript'}
SOURCES = {'zoom': ZOOM, 'google_meet': GOOGLE_MEET}  # a meeting app's records of each field, by its key in read()
KINDS = (NOTES, TRANSCRIPT, 'zoom.summary', 'google_meet.notes')  # a meeting's record for its follow-ups, in this order (for_event)
SOURCE = {'zoom.summary': 'Zoom', 'zoom.transcript': 'Zoom', 'google_meet.notes': 'Google Meet', 'google_meet.transcript': 'Google Meet',
          NOTES: 'Meeting', TRANSCRIPT: 'Meeting'}
MAX_CHARS = 400_000  # a long meeting's full transcript fits
READ_CHARS = 20_000  # one read of a field for a tool result; the rest with offset
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
    if notes.get('kind') in PREFIX:  # added to the meeting itself: that meeting, while it is there
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


def for_event(db, event_id, day, kinds=KINDS):
    """The record of calendar event `event_id` (its day as YYYY-MM-DD) for its follow-ups, or None: its added Notes,
    else its added Transcript, else the newest Zoom summary that matches it (kinds narrows that, in its own order)."""
    start = dt.date.fromisoformat(day)
    order = ','.join(f'kind=? DESC' for _ in kinds)
    rows = db.execute(f"SELECT id,kind,source_id,title,body,occurred_at,metadata FROM events WHERE kind IN ({','.join('?' * len(kinds))}) AND deleted=0 "
                      f'AND occurred_at>=? AND occurred_at<? ORDER BY {order},occurred_at DESC',
                      (*kinds, (start - dt.timedelta(days=1)).isoformat(), (start + dt.timedelta(days=2)).isoformat(), *kinds)).fetchall()
    for notes in rows:
        found = match(db, dict(notes))
        if found and found['id'] == event_id:
            return dict(notes)
    return None


# ------------------------------------------------------------------ notes and transcripts added to a meeting
def _meeting_id(source_id):
    m = re.fullmatch(r'(?:notes|transcript):(\d+)', str(source_id or ''))
    return int(m[1]) if m else None


def field_kind(field):
    """The kind of a field named in the API ('notes' or 'transcript'; notes when left out)."""
    kind = FIELDS.get(str(field or 'notes'))
    if not kind:
        raise ValueError('field is notes (a summary, decisions, action items) or transcript (what was said, word for word)')
    return kind


def meeting(db, event_id):
    """The calendar meeting with this events id, or None."""
    try:
        event_id = int(event_id)
    except (TypeError, ValueError):
        return None
    return db.execute("SELECT id,account_id,source_id,title,body,occurred_at,metadata FROM events WHERE id=? AND kind='calendar.event' AND deleted=0",
                      (event_id,)).fetchone()


def added(db, event, kind=NOTES):
    """The notes (or, with kind TRANSCRIPT, the transcript) added to this meeting (a row of `meeting`), or None."""
    return db.execute('SELECT id,title,body,occurred_at,metadata,ingested_at FROM events WHERE account_id=? AND source_id=? AND kind=? AND deleted=0',
                      (event['account_id'], PREFIX[kind] + str(event['id']), kind)).fetchone()


def added_for(db, event_ids):
    """{meeting event id: {'notes': {by, at, chars}, 'transcript': {...}}} for those of these meetings that have notes
    or a transcript added (each key only when it has that): the Calendar's marker."""
    ids = sorted({int(i) for i in event_ids})
    if not ids:
        return {}
    out = {}
    for kind, field in ((NOTES, 'notes'), (TRANSCRIPT, 'transcript')):
        for r in db.execute('SELECT source_id,body,metadata FROM events WHERE kind=? AND deleted=0 AND source_id IN (SELECT ? || value FROM json_each(?))',
                            (kind, PREFIX[kind], json.dumps(ids))):
            m = json.loads(r['metadata'] or '{}')
            out.setdefault(_meeting_id(r['source_id']), {})[field] = {'by': m.get('added_by') or 'owner', 'at': m.get('added_at'),
                                                                       'chars': len(r['body'] or '')}
    return out


def clean(text):
    """The text as given: line endings made plain and the ends trimmed; Markdown stays as it is."""
    text = str(text or '').replace('\r\n', '\n').replace('\r', '\n').replace('\x00', '')
    return text.strip('\n').rstrip()


def _people_meta(em):
    people = lambda a: {k: a[k] for k in ('email', 'displayName', 'self', 'resource', 'responseStatus') if k in a}
    return {**({'organizer': people(em['organizer'])} if isinstance(em.get('organizer'), dict) else {}),
            'attendees': [people(a) for a in em.get('attendees') or [] if isinstance(a, dict)][:200]}


def plan(db, event_id, text, by, at, append=False, field='notes'):
    """What saving a meeting's notes (or its transcript: field) changes: (result, write). Adds it, or replaces the one it
    has (append: below it); empty text removes it. Only that field: the other is never touched, whatever the text
    looks like. by: 'owner' or 'machine'. write is None (nothing changes), ('remove', id), ('update', id, row) or
    ('insert', row): Store.save_meeting_notes makes it, as only assistant.py writes events (sealed). It becomes a new
    version of its signal, so the next review reads it."""
    kind = field_kind(field)
    event = meeting(db, event_id)
    if not event:
        raise ValueError('No meeting with that event_id. Find it with day (and query) first')
    text = clean(text)
    old = added(db, event, kind)
    if append and old and text:
        text = old['body'].rstrip() + '\n\n' + text
    if len(text) > MAX_CHARS:
        if kind == TRANSCRIPT:
            raise ValueError(f'A transcript can be up to {MAX_CHARS:,} characters')
        raise ValueError(f'Notes can be up to {MAX_CHARS:,} characters')
    source_id = PREFIX[kind] + str(event['id'])
    result = {'event_id': event['id'], 'title': event['title'], 'field': 'transcript' if kind == TRANSCRIPT else 'notes'}
    if not text:
        return {**result, 'removed': bool(old)}, ('remove', old['id']) if old else None
    em = json.loads(event['metadata'] or '{}')
    meta = {'event_id': event['id'], 'start_at': event['occurred_at'], 'end_at': em.get('end_at'), 'format': 'markdown', 'field': result['field'],
            'added_by': 'owner' if by == 'owner' else 'machine', 'added_at': at,
            **_people_meta(em)}  # the meeting's people, so sharing judges it by the same people as the meeting
    digest = hashlib.sha256(text.encode()).hexdigest()
    row = db.execute('SELECT id,content_hash,deleted FROM events WHERE account_id=? AND source_id=?', (event['account_id'], source_id)).fetchone()
    result['chars'] = len(text)
    if row and row['content_hash'] == digest and not row['deleted']:
        return {**result, 'notes_id': row['id'], 'unchanged': True}, None
    record = {'account_id': event['account_id'], 'source_id': source_id, 'kind': kind, 'occurred_at': event['occurred_at'], 'title': event['title'],
              'body': text, 'metadata': json.dumps(meta), 'content_hash': digest, 'ingested_at': at}
    return ({**result, **({'replaced': True} if old and not append else {}), **({'appended': True} if old and append else {})},
            ('update', row['id'], record) if row else ('insert', record))


# A transcript line: a timestamp and a speaker, in either order ("[0:01] Speaker 1: ...", "00:01:02 Dana: ...",
# "Dana (00:01): ...", "Dana  0:01" with the words on the next lines), or a WebVTT cue timing. Structure only, never words.
TIME = r'[\[(]?(?:\d{1,2}:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?[\])]?'
TURN = re.compile(r'^\s*(?:[-*]\s+)?(?:' + TIME + r'\s*[-–|]?\s*[^\s:][^:\n]{0,60}:(?:\s|$)'
                  r'|[^\s:\[(][^:\n]{0,60}?[\s,–-]+' + TIME + r'\s*(?::\s|$)'
                  r'|(?:\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}\s+-->\s)')
STAMP = re.compile(r'(?<![\d:])(?:(\d{1,2}):)?(\d{1,2}):(\d{2})(?![\d:])')


def looks_like_transcript(text):
    """Whether timestamped speaker turns are the text's dominant structure: at least 5 turns, holding most of its text
    (a turn's words may follow on the next lines). A summary that quotes a few timestamps is not one."""
    lines = [line for line in clean(text).split('\n')]
    total = sum(len(line.strip()) for line in lines)
    turns = covered = 0
    inside = False
    for line in lines:
        bare = line.strip()
        if not bare:
            inside = False
            continue
        if TURN.match(line):
            turns, inside = turns + 1, True
            covered += len(bare)
        elif inside:
            covered += len(bare)
    return turns >= 5 and total > 0 and covered >= 0.6 * total


def spoken_minutes(text):
    """How long the transcript runs, in minutes, from its last timestamp; None when it has none."""
    for line in reversed(clean(text)[-4000:].split('\n')):
        if TURN.match(line):
            found = STAMP.search(line)
            if found:
                h, m, s = (int(found[1] or 0), int(found[2]), int(found[3]))
                return round(h * 60 + m + s / 60) if found[1] else round(m + s / 60)
    return None


def _minutes(event):
    start, end, _ = _span(event)
    return round((end - start).total_seconds() / 60) if start and end and end > start else None


def _page(body, offset, limit):
    end = offset + max(1, int(limit))
    return {'text': body[offset:end], 'chars': len(body), 'next_offset': end if end < len(body) else None}


def read(db, event_id, offset=0, limit=READ_CHARS, field=None):
    """A meeting and its two records: notes and transcript, each the one added to it ({text, by, at, chars,
    next_offset}; the transcript also with minutes, how long it runs) or None, and the meeting app's that match it
    under zoom and google_meet ({notes, transcript, url}, each item with its own url, or None). field ('notes' or 'transcript') reads only that one, from offset."""
    event = meeting(db, event_id)
    if not event:
        raise ValueError('No meeting with that event_id')
    only = field_kind(field) if field else None
    offset = max(0, int(offset or 0))
    em = json.loads(event['metadata'] or '{}')
    out = {'event_id': event['id'], 'title': event['title'], 'start': event['occurred_at'], 'end': em.get('end_at') or event['occurred_at'],
           'notes': None, 'transcript': None, 'zoom': None, 'google_meet': None}
    meeting_minutes = _minutes(dict(event))
    for kind, key in ((NOTES, 'notes'), (TRANSCRIPT, 'transcript')):
        if only and kind != only:
            continue
        row = added(db, event, kind)
        if row:
            m, body = json.loads(row['metadata'] or '{}'), row['body'] or ''
            out[key] = {'id': row['id'], **_page(body, offset, limit), 'by': m.get('added_by') or 'owner', 'at': m.get('added_at') or row['ingested_at'],
                        **({'minutes': spoken_minutes(body) or meeting_minutes} if kind == TRANSCRIPT else {})}
    start = stamp(event['occurred_at'])
    for name, kinds in SOURCES.items():
        if not start:
            break
        found_any, url = {}, None
        for key, kind in kinds.items():
            if only and FIELDS[key] != only:
                continue
            found = for_event(db, event['id'], start.date().isoformat(), (kind,))
            if not found:
                continue
            sm = found['metadata'] if isinstance(found['metadata'], dict) else json.loads(found['metadata'] or '{}')
            body = str(found.get('body') or '')
            if not body.strip():
                continue
            link = sm.get('source_url')
            link = link if isinstance(link, str) and link.startswith('https://') else None
            url = url or link
            found_any[key] = {'id': found['id'], 'title': found['title'], 'url': link, **_page(body, offset, limit),
                              **({'minutes': spoken_minutes(body) or _span_minutes(sm) or meeting_minutes, 'truncated': bool(sm.get('truncated'))}
                                 if key == 'transcript' else {})}
        if found_any:
            out[name] = {'notes': found_any.get('notes'), 'transcript': found_any.get('transcript'), 'url': url}
    return out


def _span_minutes(m):
    start, end = stamp(m.get('start_at')), stamp(m.get('end_at'))
    return round((end - start).total_seconds() / 60) if start and end and end > start else None


MOVES = ('CREATE TABLE IF NOT EXISTS meeting_moves(event_id INTEGER PRIMARY KEY,old_kind TEXT NOT NULL,old_source_id TEXT NOT NULL,'
         'new_kind TEXT NOT NULL,new_source_id TEXT NOT NULL,moved_at TEXT NOT NULL)')


def transcript_moves(db):
    """Once, for notes saved before Notes and Transcript were apart: each added notes row whose dominant structure is
    timestamped speaker turns (looks_like_transcript) becomes that meeting's transcript, when it has none yet. Only rows
    without a field (saved before) are looked at, so what the owner puts in Notes after this stays there. The row keeps
    its id, text and people; its kind and source_id change (Store.move_meeting_transcripts makes it, keeping what they
    were in meeting_moves). [(notes id, old source_id, new source_id, new metadata)]. Rows it can't read (sealed,
    without the key) are left for a start that can."""
    out = []
    for r in db.execute('SELECT id,account_id,source_id,body,metadata FROM events WHERE kind=? AND deleted=0', (NOTES,)).fetchall():
        body, meta, meeting_id = r['body'], r['metadata'], _meeting_id(r['source_id'])
        if not isinstance(body, str) or not isinstance(meta, str) or meeting_id is None:
            continue
        try:
            m = json.loads(meta or '{}')
        except ValueError:
            continue
        if not isinstance(m, dict) or 'field' in m or not looks_like_transcript(body):
            continue
        target = PREFIX[TRANSCRIPT] + str(meeting_id)
        if db.execute('SELECT 1 FROM events WHERE account_id=? AND source_id=?', (r['account_id'], target)).fetchone():
            continue
        out.append((r['id'], r['source_id'], target, json.dumps({**m, 'field': 'transcript', 'moved_from': 'notes'})))
    return out


def meetings_on(db, account_ids, day, tz, query=''):
    """The meetings on one day (YYYY-MM-DD, in the owner's time zone tz), for finding the one notes belong to:
    [{event_id, title, start, end, has_notes, has_transcript}], optionally only those whose title has `query`."""
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
        o['has_notes'] = 'notes' in have.get(o['event_id'], {})
        o['has_transcript'] = 'transcript' in have.get(o['event_id'], {})
    return out

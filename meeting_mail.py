"""One meeting, one record: its notes reach The Machine up to three ways, and they make one set of to-dos with the
meeting as their source ("Notes from Board meeting Q4 · Wed 28 Oct").

- The meeting app's own record (meeting_notes.py): Zoom's AI Companion summary, Gemini's notes from Google Meet,
  Teams' notes, or notes added to the meeting.
- Its calendar event, edited once it began: notes a person or a notes app put in its description. A changed event is a
  new version of its signal, so the review reads it again after the meeting (calendar_notes).
- The same notes by mail: the meeting app sends its summary to the host (MAIL_FROM, the app's own sending address).

Which meeting a mail or a record is of is plain code, never a model: a record by meeting_notes.match; a mail by the
Zoom meeting ID it names, else by the meeting title it carries, else by when: the owner's meeting that ended just before
it came, when no other one ended near that time. No meeting is better than another meeting's.

The review is told the meeting and the open to-dos already made from it (hint), and a new to-do from one of them is held
until it says whether one of those is the same next step (same_meeting_cards, Store.suggest). The same notes arriving a
second way join that to-do quietly (joins_quietly): no second to-do, no second notification. Whatever came first, the
meeting leads its source line (lead)."""
from __future__ import annotations

import datetime as dt
import json
import re

import meeting_notes
from machine import todo_states

# The meeting apps' own sending address for their notes mail, read from the From address: a sender, never the words
MAIL_FROM = {'no-reply@zoom.us': 'Zoom', 'gemini-notes@google.com': 'Google Meet'}
MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message')
RECORDS = meeting_notes.KINDS + ('zoom.transcript', 'google_meet.transcript', 'teams.transcript')
MAIL_AFTER_HOURS = 6  # a notes mail comes within hours of the meeting's end
MAIL_EARLY_MINUTES = 45  # a call can end before its calendar slot does
CLEAR_MINUTES = 30  # by time alone, the nearest ending meeting only when the next nearest is this much further
OPEN = todo_states.OPEN  # review.CARD_OPEN, without importing the Store

MAIL_RULE = ('This mail is the meeting app\'s notes of a meeting: the same record as that meeting\'s notes on its '
             'calendar event. Make each next step one to-do led by the meeting: event_ids start with notes_event_id when '
             'there is one, else the meeting\'s event_id, then this mail. When an open to-do in todos already has that next '
             'step, suggest with its card_id instead; never a second to-do for it.')
RECORD_RULE = ('These open to-dos were already made from this meeting\'s notes (by mail, or another record of it). For a '
               'next step one of them has, suggest with its card_id and this signal first in event_ids: the meeting becomes '
               'its source. A new to-do only for a next step none of them has.')
CALENDAR_RULE = ('This meeting has ended, and its event was edited once it began. When its description now holds notes '
                 '(a summary, decisions, next steps, written by a person or a notes app), they are this meeting\'s record: '
                 'make its follow-ups from them as from meeting notes, each with this event as evidence. An agenda or the '
                 'invite text alone is no to-do.')


def _meta(row):
    m = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
    return m if isinstance(m, dict) else {}


def _sender(m):
    found = re.findall(r'[^\s<>"\',;]+@[^\s<>"\',;]+', str(m.get('from') or ''))
    return found[0].lower() if found else ''


def notes_mail(row):
    """Whether this signal is a meeting app's notes mail: mail that came from that app's own sending address."""
    if row['kind'] not in MAIL_KINDS:
        return False
    m = _meta(row)
    return _sender(m) in MAIL_FROM and 'SENT' not in (m.get('labels') or [])


def _description(row):
    """The event's description: its body without the location and guest lines calendar_event adds."""
    m = _meta(row)
    lines = str(row.get('body') or '').split('\n')
    if lines and lines[-1].startswith('Participants: '):
        lines = lines[:-1]
    if lines and m.get('location') and lines[-1] == m['location']:
        lines = lines[:-1]
    return '\n'.join(lines).strip()


def calendar_notes(row, at=None):
    """Whether a calendar event may now carry its meeting's notes: it has ended, it was edited once it began, and it
    has a description. What the description says is the review's to judge (CALENDAR_RULE)."""
    import timeutil
    if row['kind'] != 'calendar.event' or row.get('deleted'):
        return False
    m = _meta(row)
    start, end, edited = (meeting_notes.stamp(row['occurred_at']), meeting_notes.stamp(m.get('end_at')),
                          meeting_notes.stamp(m.get('updated')))
    at = at or timeutil.clock()
    return bool(start and end and edited and not m.get('all_day') and m.get('status') != 'cancelled'
                and end <= at and edited >= start and _description(row))


def _owned(m):
    from machine.sources.calendar import calendar_owned  # the Store's sources, loaded when needed (no import cycle)
    return calendar_owned(m)


def _plain(text):
    return ' '.join(re.sub(r'[^\w]+', ' ', str(text or '').lower()).split())


def mail_meeting(db, row):
    """The owner's calendar meeting (a dict) a meeting app's notes mail is of, or None."""
    at = meeting_notes.stamp(row['occurred_at'])
    if not at:
        return None
    found = []
    for event in db.execute("SELECT id,account_id,source_id,title,body,occurred_at,metadata FROM events WHERE kind='calendar.event' "
                            'AND deleted=0 AND occurred_at>=? AND occurred_at<=?',
                            ((at - dt.timedelta(days=1)).isoformat(), at.isoformat())):
        event = dict(event)
        start, end, m = meeting_notes._span(event)
        if (not start or m.get('all_day') or m.get('status') == 'cancelled' or not _owned(m) or start > at
                or not at - dt.timedelta(hours=MAIL_AFTER_HOURS) <= end <= at + dt.timedelta(minutes=MAIL_EARLY_MINUTES)):
            continue
        found.append((abs((at - end).total_seconds()), event, m))
    if not found:
        return None
    ids = meeting_notes.zoom_ids(row.get('title'), row.get('body'))
    named = [e for _, e, m in found if ids & meeting_notes.zoom_ids(m.get('location'), e.get('body'))]
    if len(named) == 1:
        return named[0]
    subject = _plain(row.get('title'))
    titled = [e for _, e, _ in found if len(_plain(e['title'])) >= 4 and _plain(e['title']) in subject]
    if len(titled) == 1:
        return titled[0]
    found.sort(key=lambda x: x[0])
    if len(found) == 1 or found[1][0] - found[0][0] >= CLEAR_MINUTES * 60:
        return found[0][1]
    return None


def _full(db, event_id):
    row = db.execute('SELECT id,account_id,source_id,kind,title,body,occurred_at,metadata,deleted FROM events WHERE id=?', (event_id,)).fetchone()
    return dict(row) if row else None


def meeting_of(db, event_id, at=None):
    """(the meeting's calendar event as a dict, how this signal is of it: 'record', 'event' or 'mail'), or (None, None)."""
    row = _full(db, event_id)
    if not row or row.get('deleted'):
        return None, None
    if row['kind'] in RECORDS:
        found = meeting_notes.match(db, row)
        return (dict(found), 'record') if found else (None, None)
    if row['kind'] == 'calendar.event':
        return (row, 'event') if calendar_notes(row, at) else (None, None)
    if notes_mail(row):
        found = mail_meeting(db, row)
        return (found, 'mail') if found else (None, None)
    return None, None


def _meetings(db, event_ids, at=None, events=False):
    """{event id: (meeting id, how)} for those of these signals that are of a meeting. events: a calendar event counts
    as its own meeting even with no notes in it."""
    out = {}
    for i in event_ids:
        if isinstance(i, int) and not isinstance(i, bool):
            found, how = meeting_of(db, i, at)
            if not found and events:
                row = _full(db, i)
                found, how = (row, 'plain') if row and row['kind'] == 'calendar.event' and not row['deleted'] else (None, None)
            if found:
                out[i] = (found['id'], how)
    return out


def _candidates(db, ids):
    """Of these event ids, those that may be of a meeting, by kind (a cheap pass before matching each)."""
    ids = sorted({i for i in ids if isinstance(i, int) and not isinstance(i, bool)})
    if not ids:
        return set()
    kinds = (*RECORDS, 'calendar.event', *MAIL_KINDS)
    return {r[0] for r in db.execute(f"SELECT id FROM events WHERE deleted=0 AND kind IN ({','.join('?' * len(kinds))}) "
                                     f"AND id IN ({','.join('?' * len(ids))})", (*kinds, *ids))}


def same_meeting_cards(db, event_ids, limit=4, at=None):
    """Open to-dos already made from the same meeting as these signals, by another of its records: a to-do from its
    notes mail for its Zoom summary, and the other way round. [{'id', 'title', 'status'}]."""
    mine = _meetings(db, _candidates(db, event_ids), at)
    if not mine:
        return []
    meetings = {meeting for meeting, _ in mine.values()}
    cards = db.execute(f"SELECT id,title,status,event_ids FROM suggestions WHERE status IN ({','.join('?' * len(OPEN))}) "
                       'ORDER BY created_at DESC LIMIT 200', OPEN).fetchall()
    held = {c['id']: [i for i in json.loads(c['event_ids'] or '[]') if i not in mine] for c in cards}
    maybe = _candidates(db, {i for ids in held.values() for i in ids})
    theirs = _meetings(db, maybe, at)
    found = []
    for card in cards:
        if any(i in theirs and theirs[i][0] in meetings for i in held[card['id']]) and not set(event_ids) <= set(json.loads(card['event_ids'] or '[]')):
            found.append({'id': card['id'], 'title': card['title'], 'status': card['status']})
        if len(found) >= limit:
            break
    return found


def joins_quietly(db, old_ids, added_ids, at=None):
    """Whether the signals added to a to-do are only the same meeting's notes again, by another way (its record, its
    event or its notes mail), for a meeting the to-do is already from: they join it without bringing it back."""
    if not added_ids:
        return False
    new = _meetings(db, added_ids, at, events=True)
    if len(new) != len(set(added_ids)) or all(how == 'plain' for _, how in new.values()):
        return False  # something else, or only the meeting's event: news the review judged as such
    old = {m for m, _ in _meetings(db, _candidates(db, old_ids), at).values()}
    return all(m in old for m, _ in new.values())


def lead(db, rows, at=None):
    """The source line's rows, the meeting first when a notes mail would lead it, and the meeting's title when the line
    names the meeting's notes ("notes from <title>"), else None."""
    if not rows or db is None:
        return rows, None
    first = rows[0]
    if first['kind'] in MAIL_KINDS and notes_mail(_full(db, first['id']) or first):
        mail = _meetings(db, [first['id']], at).get(first['id'])
        if mail:
            # its own record of that meeting first (Zoom's notes), else the meeting's event
            same = [(0 if how == 'record' else 1, n, r) for n, r in enumerate(rows[1:])
                    for found, how in [meeting_of(db, r['id'], at)] if found and found['id'] == mail[0]]
            if not same:
                same = [(1, n, r) for n, r in enumerate(rows[1:]) if r['id'] == mail[0]]
            if same:
                _, _, chosen = min(same, key=lambda x: x[:2])
                rows = [chosen, *[r for r in rows if r['id'] != chosen['id']]]
                if chosen['id'] == mail[0]:  # the meeting's own event, notes in it or not: the mail's notes are of it
                    return rows, ' '.join(str((_full(db, mail[0]) or {}).get('title') or '').split()) or None
    first = rows[0]
    if first['kind'] in RECORDS or first['kind'] == 'calendar.event':
        found, _ = meeting_of(db, first['id'], at)
        if found:
            return rows, ' '.join(str(found['title'] or '').split()) or None
    return rows, None


def hint(db, row, at=None):
    """What a review is told on a signal that is of a meeting: the meeting, its record, and the open to-dos already
    made from it, with the rule. None for other signals."""
    import timeutil
    if row['kind'] not in RECORDS and row['kind'] != 'calendar.event' and not notes_mail(row):
        return None
    found, how = meeting_of(db, row['id'], at)
    if not found:
        return None
    todos = same_meeting_cards(db, [row['id']], at=at)
    out = {'event_id': found['id'], 'title': found['title']}
    if how == 'mail':
        day = (meeting_notes.stamp(found['occurred_at']) or timeutil.clock()).date().isoformat()
        record = meeting_notes.for_event(db, found['id'], day)
        return {**out, **({'notes_event_id': record['id']} if record else {}), **({'todos': todos} if todos else {}), 'rule': MAIL_RULE}
    rules = [CALENDAR_RULE] if how == 'event' else []
    if todos:
        rules.append(RECORD_RULE)
    return {**out, **({'todos': todos} if todos else {}), 'rule': ' '.join(rules)} if rules else None

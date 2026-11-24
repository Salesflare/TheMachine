"""What a meeting briefing (meeting_prep.py) reads of the notes of earlier meetings with the same people.

Which earlier meetings (meetings): on this Machine's own calendars, in the upcoming meeting's area (work or personal, by
the calendar's account and the notes' account), the owner's, over, at most DAYS old, and with one of the upcoming
meeting's outside guests on it. The guests are matched as people, through the Graph (graph_events: every address of one
person counts), never by the meeting's title. The Graph has no one on a meeting of more than 25 and nobody who declined,
so neither brings anything in. Someone from the owner's own team never brings a meeting in; a shared colleague only adds
a little to its rank. The more of its people are in the upcoming meeting and the newer it is, the higher it ranks; a
weekly call with them gives its newest ones.

What is read of a meeting (record): its notes (added to it, or its meeting app's), else the notes mail its app sent, else
its transcript's start and end, else its calendar description when that was edited once it began (which may be only the
agenda: the turn is told so). At most MEETINGS of them, newest first, within CHARS characters in all.

What came after (since): an old open point may be settled by now, so next to the notes the turn reads what happened since
the oldest of them: later messages with these people (bounded), promises closed since and to-dos done since.

Only this Machine's own signals are read: never history (docs/help/history.md: no model reads it), the Team Graph or what
a Fleet shares. And the notes are never the
to-do's sources: what others can see follows those. Notes are other people's words: they reach the turn quoted, as
evidence, never instructions."""
from __future__ import annotations

import datetime as dt
import json
import math
import re

import meeting_mail
import meeting_notes
import timeutil
from machine import todo_states
from machine.store import graph_promises

DAYS = 365           # how far back an earlier meeting counts
HALF_LIFE = 90       # days after which an earlier meeting counts half
LOOKED = 24          # meetings looked at for a record, best first
MEETINGS = 4         # read, at most
PER_SERIES = 2       # of one recurring series, at most
CHARS = 10_000       # of notes in a turn, at most (about 2,500 tokens)
FIRST, REST = 4_500, 2_600  # of the newest meeting's notes, and of each other's
MAIL_MIN = 600       # a notes mail shorter than this holds no notes (someone joined, a reminder)
TEXT_MIN = 120       # a calendar description shorter than this is a line about the meeting, not notes
SPOKEN_HEAD, SPOKEN_TAIL = 600, 3_000  # of a transcript: how it began, and its end, where next steps are said
SMALLEST = .3       # shared people by the root of its size: one of twelve or more doesn't bring a meeting in
TEAM_SHARE = .1      # what a shared colleague adds to a meeting's rank, next to 1 for an outside guest
SINCE = 25           # later messages, at most, newest first
SINCE_CHARS = 4_000  # of them in all, and of each
SINCE_EACH = 500
SPOKEN = tuple(k for k in meeting_mail.RECORDS if k not in meeting_notes.KINDS) + (meeting_notes.TRANSCRIPT,)
ORDER = {k: n for n, k in enumerate((*meeting_notes.KINDS, *SPOKEN)) if k not in SPOKEN}


def _marks(values):
    return ','.join('?' * len(values))


def _has(db, table):
    return db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone() is not None


def _meta(row):
    try:
        found = json.loads(row['metadata'] or '{}')
    except ValueError:
        return {}
    return found if isinstance(found, dict) else {}


def _emails(meta):
    return {str(a.get('email') or '').lower() for a in (*(meta.get('attendees') or ()), meta.get('organizer') or {})
            if isinstance(a, dict) and not a.get('self') and not a.get('resource')} - {''}


def names(meta, limit=8):
    """Who was on it, for the turn: names, or addresses without one."""
    out = []
    for a in meta.get('attendees') or ():
        if isinstance(a, dict) and not a.get('self') and not a.get('resource') and a.get('responseStatus') != 'declined':
            name = ' '.join(str(a.get('displayName') or a.get('email') or '').split())[:60]
            if name and name not in out:
                out.append(name)
    return out[:limit]


def meetings(db, meeting, nodes, same_side, owned, domains, current):
    """The earlier meetings to look at for notes, best first: [{'ids' (its copies on several calendars), 'id', 'title',
    'start', 'end', 'meta', 'row', 'series'}]. nodes: the outside guests' Graph ids; owned: calendar_owned; domains: the
    owner's own company's."""
    if not nodes:
        return []
    end = min(current, meeting['start'])
    rows = db.execute('SELECT e.id,e.account_id,e.source_id,e.kind,e.title,e.body,e.occurred_at,e.metadata,e.deleted,group_concat(DISTINCT g.node_id) AS who '
                      "FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id IN (SELECT value FROM json_each(?)) AND e.kind='calendar.event' "
                      'AND e.deleted=0 AND e.history=0 AND e.id!=? AND e.occurred_at>=? AND e.occurred_at<? GROUP BY e.id',
                      (json.dumps(sorted(nodes)), meeting['id'], (end - dt.timedelta(days=DAYS)).isoformat(), end.isoformat())).fetchall()
    team = {e for e in _emails(meeting['meta']) if e.rpartition('@')[2] in domains}
    found = {}
    for r in rows:
        meta, start = _meta(r), meeting_notes.stamp(r['occurred_at'])
        ends = meeting_notes.stamp(meta.get('end_at')) or (start + dt.timedelta(hours=1) if start else None)
        if not start or meta.get('all_day') or meta.get('status') == 'cancelled' or not owned(meta) or not same_side(r['account_id']) or ends > current:
            continue
        me = next((a for a in meta.get('attendees') or () if isinstance(a, dict) and a.get('self')), {})
        if me.get('responseStatus') == 'declined':  # the owner wasn't there
            continue
        people = _emails(meta)
        shared = len(set(str(r['who']).split(','))) + TEAM_SHARE * len(team & people)
        close = shared / math.sqrt(max(1, len(people)))
        if close < SMALLEST and not (meta.get('recurring_event_id') and meta['recurring_event_id'] == meeting['meta'].get('recurring_event_id')):
            continue
        rank = close * .5 ** (max(0, (end - start).days) / HALF_LIFE)
        key = (meta.get('ical_uid') or r['source_id'], start)
        if key in found:
            found[key]['ids'].add(r['id'])
            continue
        found[key] = {'ids': {r['id']}, 'id': r['id'], 'title': ' '.join(str(r['title'] or '').split())[:120], 'start': start, 'end': ends, 'meta': meta,
                      'row': dict(r), 'series': meta.get('recurring_event_id'), 'rank': rank}
    return sorted(found.values(), key=lambda m: (-m['rank'], -m['start'].timestamp()))[:LOOKED]


def clip(text, n, head=.55):
    """The text within n characters: its start and its end (where next steps stand), cut between words."""
    text = re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', str(text or ''))).strip()
    if len(text) <= n:
        return text
    first = int(n * head)
    start, rest = text[:first], text[len(text) - (n - first - 3):]
    return start[:start.rfind(' ')].rstrip() + ' … ' + rest[rest.find(' ') + 1:].lstrip()


def records(db, found, same_side):
    """{meeting id: [its notes and transcripts as signals]} of these meetings, by plain code (meeting_notes.match)."""
    if not found:
        return {}
    first, last = min(m['start'] for m in found), max(m['start'] for m in found)
    by_id = {i: m['id'] for m in found for i in m['ids']}
    out = {}
    rows = db.execute(f'SELECT id,account_id,occurred_at FROM events WHERE kind IN ({_marks(meeting_mail.RECORDS)}) AND deleted=0 AND history=0 AND occurred_at>=? AND occurred_at<=?',
                      (*meeting_mail.RECORDS, (first - dt.timedelta(days=1)).isoformat(), (last + dt.timedelta(days=1)).isoformat())).fetchall()
    for r in rows:
        at = meeting_notes.stamp(r['occurred_at'])
        if not same_side(r['account_id']) or not at or not any(abs(at - m['start']) <= dt.timedelta(days=1) for m in found):
            continue
        row = dict(db.execute('SELECT id,account_id,source_id,kind,title,body,occurred_at,metadata FROM events WHERE id=?', (r['id'],)).fetchone())
        match = meeting_notes.match(db, row)
        if match and match['id'] in by_id and str(row['body'] or '').strip():
            out.setdefault(by_id[match['id']], []).append(row)
    return out


def mails(db, meeting, accounts):
    """The notes mails of one meeting, the longest first (meeting_mail.mail_meeting)."""
    after, before = meeting['end'] - dt.timedelta(minutes=meeting_mail.MAIL_EARLY_MINUTES), meeting['end'] + dt.timedelta(hours=meeting_mail.MAIL_AFTER_HOURS)
    out = []
    for r in db.execute(f'SELECT id,kind,metadata FROM events WHERE account_id IN ({_marks(accounts)}) AND occurred_at>=? AND occurred_at<=? AND deleted=0 '
                        f'AND history=0 AND kind IN ({_marks(meeting_mail.MAIL_KINDS)})', (*accounts, after.isoformat(), before.isoformat(), *meeting_mail.MAIL_KINDS)).fetchall():
        if not meeting_mail.notes_mail(r):
            continue
        row = dict(db.execute('SELECT id,account_id,kind,title,body,occurred_at,metadata FROM events WHERE id=?', (r['id'],)).fetchone())
        match = meeting_mail.mail_meeting(db, row) if len(str(row['body'] or '')) >= MAIL_MIN else None
        if match and match['id'] in meeting['ids']:
            out.append(row)
    return sorted(out, key=lambda r: -len(r['body']))


def record(db, meeting, held, accounts, current, room, agenda=''):
    """What is read of one meeting: {'as', 'text', 'ids', 'url'}, or None when nothing is there. agenda: the upcoming
    meeting's own description, which the same text on an earlier one only repeats."""
    notes = sorted((r for r in held if r['kind'] in ORDER), key=lambda r: ORDER[r['kind']])
    spoken = [r for r in held if r['kind'] in SPOKEN]
    if notes:
        chosen = notes[:1]
        for r in notes[1:]:  # the owner's own notes and the app's: both, when they fit
            if chosen[0]['kind'] == meeting_notes.NOTES and len(chosen[0]['body']) + len(r['body']) <= room and len(chosen) == 1:
                chosen.append(r)
        return {'as': 'notes', 'text': clip('\n'.join(str(r['body']) for r in chosen), room), 'ids': [r['id'] for r in chosen], 'url': _url(chosen)}
    sent = mails(db, meeting, accounts) if accounts else []
    if sent:
        return {'as': 'notes the meeting app mailed (may also be an automatic notice without notes)', 'text': clip(sent[0]['body'], room), 'ids': [sent[0]['id']], 'url': ''}
    if spoken:
        row = max(spoken, key=lambda r: len(r['body']))
        size = min(room, SPOKEN_HEAD + SPOKEN_TAIL)
        return {'as': 'the start and end of its transcript', 'text': clip(row['body'], size, SPOKEN_HEAD / (SPOKEN_HEAD + SPOKEN_TAIL)), 'ids': [row['id']], 'url': _url([row])}
    row = meeting['row']
    said = meeting_mail._description(row) if meeting_mail.calendar_notes(row, current) else ''
    if len(said) >= TEXT_MIN and said != agenda:
        return {'as': 'its calendar description: notes, or only the agenda (then it says what was planned, never what was agreed)',
                'text': clip(said, room), 'ids': [row['id']], 'url': ''}
    return None


def _url(rows):
    for r in rows:
        link = _meta(r).get('source_url')
        if isinstance(link, str) and re.fullmatch(r'https://[^\s()<>\[\]]{1,2000}', link):
            return link
    return ''


def read(db, meeting, nodes, same_side, sides, owned, domains, current):
    """The notes of earlier meetings with these people, newest first: [{'id': 'N1', 'meeting', 'date', 'start', 'with',
    'as', 'text', 'ids', 'url', 'of' (the meeting's event ids)}]."""
    found = meetings(db, meeting, nodes, same_side, owned, domains, current)
    if not found:
        return []
    held, accounts = records(db, found, same_side), sorted(a for a in sides if same_side(a))
    agenda = meeting_mail._description({'body': meeting['body'], 'metadata': meeting['meta']})
    chosen, series = [], {}
    for m in found:
        if len(chosen) >= MEETINGS:
            break
        if m['series'] and series.get(m['series'], 0) >= PER_SERIES:
            continue
        got = record(db, m, held.get(m['id'], []), accounts, current, FIRST, agenda)
        if got and got['text']:
            chosen.append((m, got))
            series[m['series']] = series.get(m['series'], 0) + 1
    out, left = [], CHARS
    for m, got in sorted(chosen, key=lambda x: x[0]['start'], reverse=True):
        text = clip(got['text'], min(left, FIRST if not out else REST))
        left -= len(text)
        out.append({'id': f'N{len(out) + 1}', 'meeting': m['title'], 'date': timeutil.local_day_text(m['row']['occurred_at'], m['meta']), 'start': m['start'],
                    'with': names(m['meta']), **got, 'text': text, 'of': sorted(m['ids'])})
        if left < 400:
            break
    return out


def since(db, notes, nodes, same_side, shown, sent, calendar):
    """What happened after the oldest of these notes: ({event id: row}, {'messages', 'promises_closed', 'todos_done',
    'open': promises read from the notes that are still open}). shown: messages the turn reads already; sent(meta): whether
    the owner wrote it; calendar: the kinds that are meetings."""
    oldest = min(n['start'] for n in notes).isoformat()
    ids = json.dumps(sorted(nodes))
    rows = [r for r in db.execute('SELECT DISTINCT e.id,e.account_id,e.kind,e.occurred_at,e.title,e.body,e.metadata FROM graph_events g JOIN events e ON e.id=g.event_id '
                                  'WHERE g.node_id IN (SELECT value FROM json_each(?)) AND g.direct=1 AND e.deleted=0 AND e.occurred_at>? '
                                  f"AND e.history=0 AND e.kind NOT IN ({_marks(calendar)}) ORDER BY e.occurred_at DESC LIMIT 60", (ids, oldest, *calendar)).fetchall()
            if same_side(r['account_id']) and r['id'] not in shown]
    later, texts, left = {}, {}, SINCE_CHARS
    for r in rows[:SINCE]:
        text = clip(r['body'], min(SINCE_EACH, left))
        if not text:
            continue
        left -= len(text)
        later[r['id']], texts[r['id']] = r, text
        if left < 80:
            break
    out = {}
    if later:
        out['messages'] = [{'id': f"E{r['id']}", 'date': timeutil.local_day_text(r['occurred_at'], _meta(r)), 'from': 'the owner' if sent(_meta(r)) else sender(r),
                            'subject': str(r['title'] or '')[:80], 'text': texts[r['id']]}
                           for r in sorted(later.values(), key=lambda r: r['occurred_at'])]
    mine = json.dumps(sorted({i for n in notes for i in (*n['ids'], *n['of'])}))
    touching = 'SELECT event_id FROM graph_events WHERE node_id IN (SELECT value FROM json_each(?)) UNION SELECT value FROM json_each(?)'
    open_ = {}
    if _has(db, 'promises'):
        elses = {i for n in nodes for i in graph_promises.of_others(db, n)}
        closed = [p for p in db.execute("SELECT id,direction,who,what,account_id,status,updated_at FROM promises WHERE status IN ('kept','dropped') AND updated_at>? "
                                        f'AND event_id IN ({touching}) ORDER BY updated_at DESC LIMIT 20', (oldest, ids, mine)).fetchall()
                  if same_side(p['account_id']) and p['id'] not in elses]
        if closed:
            out['promises_closed'] = [{'promised_by': promised_by(p), 'what': str(p['what'])[:120], 'now': 'done' if p['status'] == 'kept' else 'no longer needed',
                                       'date': str(p['updated_at'])[:10]} for p in closed[:8]]
        for p in db.execute("SELECT id,direction,who,what,due,account_id FROM promises p WHERE (status='open' OR (status='carded' AND NOT EXISTS "
                            f"(SELECT 1 FROM suggestions s WHERE s.id=p.suggestion_id AND s.status IN {todo_states.sql(todo_states.CLOSED)}))) "
                            'AND event_id IN (SELECT value FROM json_each(?)) ORDER BY coalesce(due,check_at) LIMIT 8', (mine,)).fetchall():
            if same_side(p['account_id']):
                open_[p['id']] = p
    done = db.execute("SELECT s.title,max(d.created_at) AS at,e.account_id FROM suggestions s JOIN decisions d ON d.suggestion_id=s.id AND d.choice='complete' AND d.source!='expiry' "
                      "JOIN json_each(s.event_ids) j JOIN events e ON e.id=j.value WHERE s.status='completed' AND d.created_at>? AND s.dedupe_key NOT LIKE 'meetprep:%' "
                      f'AND j.value IN ({touching}) GROUP BY s.id ORDER BY at DESC LIMIT 12', (oldest, ids, mine)).fetchall()
    done = [t for t in done if same_side(t['account_id'])][:6]
    if done:
        out['todos_done'] = [{'todo': str(t['title'])[:120], 'date': str(t['at'])[:10]} for t in done]
    return later, open_, out


def promised_by(p):
    return 'the owner' if p['direction'] == 'mine' else str(p['who'] or '').removeprefix('wa:')[:60] or 'them'


def sender(row):
    found = re.sub(r'\s*<[^>]*>', '', str(_meta(row).get('from') or '')).strip(' "')
    return found[:60] or 'them'

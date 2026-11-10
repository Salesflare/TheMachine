"""Birthdays (docs/help/routines.md, "Templates"): whose birthday it is today among the people the owner is close to,
for the Birthdays template's morning to-dos (birthdays_app.py). Plain code, no model, no table.

Where a birthday comes from, with the reads each Machine already has (never a wider scope):
- the owner's calendars: Google's birthday events (eventType birthday, a contact's birthday on the main calendar, or the
  Birthdays calendar when it is connected) and an all-day event named like one ("Sam Lee's birthday");
- Outlook's Birthdays calendar, read by the app at run time with Calendars.Read (birthdays_app.py), its titles here;
- a person's facts: the birthday on their Google contact (self-hosted sign-ins that read contacts, enrichment.py);
- a date field the owner named Birthday on a person in the Graph (crm_fields.py).

Each comes down to a person in the Graph, once, however many sources name them. A name alone counts only when it is one
close person's full name. Only people the owner is close to count (CLOSE): someone they wrote to themselves, and who is
a regular contact or family or a friend. Strangers, newsletters and big lists never are. The owner's own birthday is not
someone else's.

Each person's to-do goes on the channel the owner usually writes to them on, one to one (usual_channel): its latest
message there is the to-do's evidence, so the draft is written in that conversation, in its language and the owner's
voice, and only sent when the owner says so."""
from __future__ import annotations

import datetime as dt
import json
import re
import unicodedata

import graph
from mail_senders import addresses

CLOSE = 1.0  # graph.closeness: regular or close
OWN_LIFE_CLOSE = 0.3  # family or a friend: occasional is enough
MAX_A_DAY = 5
CHANNEL_DAYS = 365

# What a birthday calendar is called, in the languages the app speaks (Outlook names its own after the owner's language)
CALENDAR_NAMES = {'birthdays', 'birthday calendar', 'verjaardagen', 'geburtstage', 'anniversaires', 'cumpleaños', 'compleanni',
                  'aniversários', 'aniversarios'}
GOOGLE_BIRTHDAYS = '#contacts@group.v.calendar.google.com'
# "Sam Lee's birthday", "Birthday of Sam Lee", "Verjaardag van Sam Lee", "Geburtstag von Sam Lee", "Sam Lee hat Geburtstag",
# "Anniversaire de Sam Lee", "Cumpleaños de Sam Lee", "Compleanno di Sam Lee", "Aniversário de Sam Lee"
TITLE = [re.compile(p, re.I) for p in (
    r"^(?P<name>.+?)[’']s?\s+birthday$", r'^birthday(?:\s+of|:)\s+(?P<name>.+)$', r'^(?P<name>.+?)\s*:\s*birthday$',
    r'^verjaardag(?:\s+van|:)\s+(?P<name>.+)$', r'^(?P<name>.+?)\s+(?:is\s+)?jarig$',
    r'^geburtstag(?:\s+von|:)\s+(?P<name>.+)$', r'^(?P<name>.+?)\s+hat\s+geburtstag$', r'^(?P<name>.+?)s\s+geburtstag$',
    r"^anniversaire(?:\s+de|\s+d[’']|:)\s*(?P<name>.+)$", r'^cumpleaños(?:\s+de|:)\s+(?P<name>.+)$',
    r"^compleanno(?:\s+di|\s+d[’']|:)\s*(?P<name>.+)$", r'^aniversário(?:\s+de|\s+do|\s+da|:)\s+(?P<name>.+)$')]
SELF = re.compile(r'^\W*happy birthday\W*$', re.I)  # Google's own event for the owner's birthday
# A date field on a person the owner named like this is a birthday
FIELD_NAMES = {'birthday', 'birthdate', 'birth date', 'date of birth', 'dob', 'verjaardag', 'geboortedatum', 'geburtstag',
               'geburtsdatum', 'anniversaire', 'date de naissance', 'cumpleaños', 'fecha de nacimiento', 'compleanno',
               'data di nascita', 'aniversário', 'data de nascimento'}
# One-to-one conversations the owner writes in, and how a message there is theirs (graph.person_evidence reads it so too)
CHANNELS = ('whatsapp.message', 'telegram.message', 'gmail.message', 'slack.message', 'linkedin.message', 'teams.message')


def fold(text):
    return ' '.join(unicodedata.normalize('NFKC', str(text or '')).casefold().split())


def name_in_title(title, birthday_event=False):
    """The person a birthday event is about, from its title; None when it isn't one. On an event that is a birthday by
    itself (Google's birthday type, a Birthdays calendar) a bare name is the name."""
    text = ' '.join(str(title or '').replace('🎂', ' ').replace('🎉', ' ').split()).strip(' -–:!.')
    if not text or SELF.match(text):
        return None
    for pattern in TITLE:
        found = pattern.match(text)
        if found:
            return found.group('name').strip(' -–:!.') or None
    return text if birthday_event and not re.search(r'\bbirthday\b', text, re.I) else None


def birthday_value(text):
    """(month, day) from a birthday kept as YYYY-MM-DD or MM-DD (--MM-DD too), or None."""
    found = re.fullmatch(r'(?:\d{4}-|--)?(\d{2})-(\d{2})', str(text or '').strip())
    if not found:
        return None
    month, day = int(found.group(1)), int(found.group(2))
    try:
        dt.date(2000, month, day)  # a leap year: 02-29 is a day
    except ValueError:
        return None
    return month, day


def on(day, value):
    """Whether a birthday (month, day) falls on this day; 29 February is on 28 February in other years."""
    if not value:
        return False
    if value == (2, 29) and not (day.year % 4 == 0 and (day.year % 100 or day.year % 400 == 0)):
        return (day.month, day.day) == (2, 28)
    return (day.month, day.day) == value


def window(day, tz, days=1):
    """The day's start and end in UTC as stored (occurred_at); with days, the end of that many days from it."""
    start = dt.datetime.combine(day, dt.time(), tz).astimezone(dt.timezone.utc)
    return start.isoformat(), (start + dt.timedelta(days=days)).isoformat()


# --- the people who count ----------------------------------------------------------------------------------------------

def close_people(db):
    """{node id: row} of the people the owner is close to: they wrote to them, and they are a regular contact or closer,
    or family or a friend."""
    out = {}
    for row in db.execute("SELECT id,name,strength,info FROM graph_nodes WHERE kind='person' AND strength>=?", (OWN_LIFE_CLOSE,)):
        info = json.loads(row['info'] or '{}')
        if not info.get('wrote') or info.get('seen_only'):
            continue
        if row['strength'] >= CLOSE or graph.own_life(info):
            out[row['id']] = {'id': row['id'], 'name': row['name'], 'info': info}
    return out


def by_name(people, name):
    """The one close person with this full name, or None (no one, a first name only, or two of them)."""
    words = graph.name_words(name)
    if len(words) < 2:
        return None
    found = [p for p in people.values() if graph.name_match(words, graph.name_words(p['name'])) == 'same']
    return found[0]['id'] if len(found) == 1 else None


def by_identifier(people, identifiers):
    """{identifier: node id} for the close people these identifiers are theirs."""
    out = {}
    for node_id, info in ((p['id'], p['info']) for p in people.values()):
        for identifier in set(info.get('identifiers') or ()) | {node_id}:
            if identifier in identifiers:
                out[identifier] = node_id
    return out


# --- the sources -------------------------------------------------------------------------------------------------------

def calendar_names(db, day, tz):
    """[(name, source)] from the owner's calendars for this day: birthday events and all-day events named like one."""
    start, end = window(day, tz)
    out = []
    for row in db.execute("SELECT title,metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND occurred_at>=? AND occurred_at<?",
                          (start, end)):
        try:
            meta = json.loads(row['metadata'] or '{}')
        except ValueError:
            continue
        if meta.get('status') == 'cancelled' or not meta.get('all_day'):
            continue
        kind = (meta.get('birthday') or {}).get('type') if isinstance(meta.get('birthday'), dict) else None
        if kind and kind != 'birthday':
            continue  # the owner's own ("self"), an anniversary or another special day
        birthday = meta.get('event_type') == 'birthday' or GOOGLE_BIRTHDAYS in str(meta.get('calendar_id') or '')
        name = name_in_title(row['title'], birthday)
        if name:
            out.append((name, 'calendar'))
    return out


def outlook_names(subjects):
    """[(name, source)] from the events on an Outlook Birthdays calendar today (birthdays_app reads them)."""
    return [(name, 'outlook') for name in (name_in_title(s, True) for s in subjects) if name]


def known(db):
    """Whether any source on this Machine holds a birthday at all, on any day: a contact's kept birthday, a Birthday
    field with a date, or a birthday event on a calendar. A quiet day without one says so (birthdays_app)."""
    try:
        if db.execute("SELECT 1 FROM person_facts WHERE field='birthday' LIMIT 1").fetchone():
            return True
    except Exception:  # noqa: BLE001 - no facts yet
        pass
    try:
        fields = [r['id'] for r in db.execute("SELECT id,name FROM crm_fields WHERE kind='person' AND type='date'") if fold(r['name']) in FIELD_NAMES]
        if fields and db.execute("SELECT 1 FROM crm_values WHERE field_id IN (SELECT value FROM json_each(?)) AND value<>'' LIMIT 1",
                                 (json.dumps(fields),)).fetchone():
            return True
    except Exception:  # noqa: BLE001 - no fields yet
        pass
    for row in db.execute("SELECT title,metadata FROM events WHERE kind='calendar.event' AND deleted=0"):
        try:
            meta = json.loads(row['metadata'] or '{}')
        except ValueError:
            continue
        if not meta.get('all_day'):
            continue
        birthday = meta.get('event_type') == 'birthday' or GOOGLE_BIRTHDAYS in str(meta.get('calendar_id') or '')
        if (birthday and (meta.get('birthday') or {}).get('type', 'birthday') == 'birthday') or name_in_title(row['title']):
            return True
    return False


def fact_ids(db, day):
    """[(identifier, source)] whose kept birthday (person_facts, from a Google contact) is today."""
    try:
        rows = db.execute("SELECT identifier,value FROM person_facts WHERE field='birthday'").fetchall()
    except Exception:  # noqa: BLE001 - no facts yet
        return []
    return [(r['identifier'], 'contacts') for r in rows if on(day, birthday_value(r['value']))]


def field_ids(db, day):
    """[(id, source)] of people whose date field named Birthday (crm_fields) is today."""
    try:
        fields = [r['id'] for r in db.execute("SELECT id,name FROM crm_fields WHERE kind='person' AND type='date'") if fold(r['name']) in FIELD_NAMES]
        if not fields:
            return []
        rows = db.execute('SELECT node_id,value FROM crm_values WHERE field_id IN (SELECT value FROM json_each(?))', (json.dumps(fields),)).fetchall()
    except Exception:  # noqa: BLE001 - no fields yet
        return []
    return [(r['node_id'], 'graph') for r in rows if on(day, birthday_value(str(r['value'] or '')[:10]))]


def today(db, day, tz, outlook=()):
    """[{id, name, sources}] whose birthday it is on this day among the close people, once each, at most MAX_A_DAY (the
    closest first). outlook: the titles on Outlook Birthdays calendars today."""
    people = close_people(db)
    if not people:
        return []
    found = {}
    for name, source in calendar_names(db, day, tz) + outlook_names(outlook):
        node = by_name(people, name)
        if node:
            found.setdefault(node, set()).add(source)
    ids = fact_ids(db, day) + field_ids(db, day)
    nodes = by_identifier(people, {i for i, _ in ids})
    for identifier, source in ids:
        if identifier in nodes:
            found.setdefault(nodes[identifier], set()).add(source)
    rows = {r['id']: r['strength'] for r in db.execute('SELECT id,strength FROM graph_nodes WHERE id IN (SELECT value FROM json_each(?))',
                                                       (json.dumps(sorted(found)),))}
    picked = sorted(found, key=lambda n: -rows.get(n, 0))[:MAX_A_DAY]
    return [{'id': n, 'name': graph.person_name(people[n]['name']), 'sources': sorted(found[n])} for n in picked]


# --- where to wish them ------------------------------------------------------------------------------------------------

def _one_to_one(kind, meta, owner_slack):
    if kind == 'whatsapp.message':
        return not str(meta.get('chat_id') or '').endswith('@g.us') and not meta.get('group')
    if kind == 'telegram.message':
        return meta.get('chat_kind') != 'group'
    if kind == 'slack.message':
        return str(meta.get('channel_id') or '').startswith('D')
    if kind == 'linkedin.message':
        return not meta.get('group')
    if kind == 'teams.message':
        return meta.get('chat_type') == 'oneOnOne'
    if kind == 'gmail.message':  # the owner and one other person, nobody in copy
        people = {a for _, a in addresses(meta.get('from')) + addresses(meta.get('to')) + addresses(meta.get('cc'))}
        return len(people) == 2
    return False


def _mine(kind, meta, owner_slack):
    if kind == 'gmail.message':
        return 'SENT' in (meta.get('labels') or ())
    if kind == 'slack.message':
        return meta.get('user_id') in owner_slack
    return bool(meta.get('from_me'))


def usual_channel(db, node_id, now, owner_slack=()):
    """(kind, event id) where the owner usually writes to this person one to one: the channel with most of their own
    messages in the past year, and its latest message (theirs or the owner's). None when the owner never wrote to them
    one to one."""
    since = (now - dt.timedelta(days=CHANNEL_DAYS)).isoformat()
    marks = ','.join('?' * len(CHANNELS))
    rows = db.execute(f'SELECT e.id,e.kind,e.occurred_at,e.metadata FROM graph_events g JOIN events e ON e.id=g.event_id '
                      f'WHERE g.node_id=? AND g.direct=1 AND e.deleted=0 AND e.occurred_at>=? AND e.kind IN ({marks}) ORDER BY e.occurred_at',
                      (node_id, since, *CHANNELS)).fetchall()
    sent, latest = {}, {}
    for row in rows:
        try:
            meta = json.loads(row['metadata'] or '{}')
        except ValueError:
            continue
        if not _one_to_one(row['kind'], meta, owner_slack):
            continue
        latest[row['kind']] = row['id']
        if _mine(row['kind'], meta, owner_slack):
            sent[row['kind']] = sent.get(row['kind'], 0) + 1
    if not sent:
        return None
    kind = max(sent, key=lambda k: (sent[k], latest[k]))
    return kind, latest[kind]

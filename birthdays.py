"""Birthdays (docs/help/routines.md, "Templates"): whose birthday it is today among the people the owner is close to,
for the Birthdays template's morning to-dos (birthdays_app.py). Plain code, no model, no table.

Where a birthday comes from, with the reads each Machine already has (never a wider scope):
- the owner's calendars: Google's birthday events (eventType birthday, a contact's birthday on the main calendar, or the
  Birthdays calendar when it is connected) and an all-day event named like one ("Sam Lee's birthday");
- Google's birthday events and its contacts' Birthdays calendar, read by the app each run with calendar.readonly
  (birthdays_app.py), also when the calendar's sync leaves them out (google_birthdays here); one that is a close
  person's (google_people) is saved as their Birthday (person_birthday.offer, source google_calendar), so their page
  shows it, and never over the owner's;
- Outlook's Birthdays calendar, read by the app at run time with Calendars.Read (birthdays_app.py), its titles here;
- the Birthday on a person's page (person_birthday.py): their Google contact's, an import's, or the one the owner set
  there, which wins. The routine reads exactly what the page shows.

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

import crm_fixes
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
CONTACTS_CALENDAR = 'addressbook' + GOOGLE_BIRTHDAYS  # Google's Birthdays calendar, made from the contacts
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


def same_form(identifier):
    """An identifier the way a kept birthday has it: an email address in lower case, a number as 'wa:' and its E.164
    digits."""
    kind, _, value = str(identifier or '').partition(':')
    if kind == 'email':
        return 'email:' + value.strip().lower()
    if kind == 'wa':
        digits = re.sub(r'\D', '', value.split('@')[0])
        return 'wa:' + digits if 7 <= len(digits) <= 15 else identifier
    return identifier


def person_ids(node_id, info, code=None):
    """Every identifier a person in the Graph goes by: their own, every email address on them (aliases and ones the
    owner added, not only the first) and every phone number in E.164, read in the owner's region (code) when it has no
    country code."""
    ids = {same_form(i) for i in set(info.get('identifiers') or ()) | {node_id}}
    for item in info.get('emails') or ():
        value = str((item.get('value') if isinstance(item, dict) else item) or '').strip()
        if '@' in value:
            ids.add(same_form('email:' + value))
    for item in info.get('phones') or ():
        value = str((item.get('value') if isinstance(item, dict) else item) or '').strip()
        found = crm_fixes.phone(value, code) if value else None
        if found and re.fullmatch(r'\+[1-9]\d{6,14}', found):
            ids.add('wa:' + found[1:])
    return ids


def by_identifier(db, people, identifiers, code=None):
    """{identifier: node id} for the close people these identifiers are theirs. An identifier more than one person in
    the Graph goes by (a shared number, a team address) is nobody's: never a guess."""
    wanted = {same_form(i): i for i in identifiers}
    if not wanted:
        return {}
    owners = {}
    for row in db.execute("SELECT id,info FROM graph_nodes WHERE kind='person'"):
        info = people[row['id']]['info'] if row['id'] in people else json.loads(row['info'] or '{}')
        for identifier in person_ids(row['id'], info, code) & set(wanted):
            owners.setdefault(identifier, set()).add(row['id'])
    return {wanted[i]: next(iter(nodes)) for i, nodes in owners.items() if len(nodes) == 1 and next(iter(nodes)) in people}


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


def google_birthdays(items, day=None, contacts=False):
    """[{name, emails, date}] from events Google's calendar API returned: its birthday events on the main calendar
    (eventType birthday), or with contacts the contacts' Birthdays calendar (it names the contact and their address).
    The owner's own, anniversaries and other special days are left out; with day, so is any event not on that date."""
    out = []
    for item in items or ():
        if not isinstance(item, dict) or item.get('status') == 'cancelled':
            continue
        date = (item.get('start') or {}).get('date')
        if not date or (day and date != day.isoformat()):
            continue
        if contacts:
            prefs = (item.get('gadget') or {}).get('preferences') or {}
            kind = str(prefs.get('goo.contactsEventType') or '').upper()
            if kind and kind != 'BIRTHDAY':
                continue
            name = ' '.join(str(prefs.get('goo.contactsFullName') or '').split()) or name_in_title(item.get('summary'), kind == 'BIRTHDAY')
            emails = [e for e in re.split(r'[\s,;]+', str(prefs.get('goo.contactsEmail') or '')) if '@' in e]
        else:
            if item.get('eventType') != 'birthday' or (item.get('birthdayProperties') or {}).get('type', 'birthday') != 'birthday':
                continue
            name, emails = name_in_title(item.get('summary'), True), []
        if name or emails:
            out.append({'name': name, 'emails': emails, 'date': str(date)})
    return out


def google_people(db, people, google, code=None):
    """{node id: month and day as kept (--MM-DD)} for the close people (close_people) these Google birthdays are: by the
    contact's address first (by_identifier: never one more than one person goes by), else by their full name (by_name)."""
    google = list(google)
    mails = [['email:' + e.strip().lower() for e in g.get('emails') or ()] for g in google]
    nodes = by_identifier(db, people, {m for found in mails for m in found}, code)
    out = {}
    for entry, found in zip(google, mails):
        node = next((nodes[m] for m in found if m in nodes), None) or by_name(people, entry.get('name'))
        value = birthday_value(str(entry.get('date') or '')[:10])
        if node and value:
            out[node] = f'--{value[0]:02d}-{value[1]:02d}'
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


def today(db, day, tz, outlook=(), code=None):
    """[{id, name, sources}] whose birthday it is on this day among the close people, once each, at most MAX_A_DAY (the
    closest first). outlook: the titles on Outlook Birthdays calendars today; code: the owner's calling code, for a
    number kept without its own."""
    people = close_people(db)
    if not people:
        return []
    found = {}
    for name, source in calendar_names(db, day, tz) + outlook_names(outlook):
        node = by_name(people, name)
        if node:
            found.setdefault(node, set()).add(source)
    import person_birthday  # the one birthday each person's page shows (a contact's, an import's or the owner's)
    for node, born in person_birthday.known(db, people, code).items():
        if on(day, (born['month'], born['day'])):
            found.setdefault(node, set()).add('contacts' if born['source'] != person_birthday.SOURCE else 'graph')
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

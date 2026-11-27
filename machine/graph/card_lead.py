"""Who a to-do is for: the sender of its main source (its first event, the message the review says the matter is
about), so a colleague of theirs on copy, or a teammate closer to the owner from a meeting on it, never leads its
person chip over who asked (graph.card_people). A to-do about a meeting of the owner's own team (several colleagues,
nobody else) names none of them on its chip, and on a meeting with people from outside a colleague comes after them."""
import json
import sqlite3

from graph import addresses, relayed, resolve
from machine import kinds

MEETINGS = kinds.of(family=kinds.MEETING)


def lead_identifiers(kind, m):
    """Who a message is from, as graph identifiers: whoever wrote it to the owner, or for the owner's own message whoever
    it went to. Others on it (cc, the rest of a thread or meeting) are not its sender."""
    m = relayed(kind, m)
    if kind == 'gmail.message' or (m.get('from') and '@' in str(m.get('from'))):
        own = 'SENT' in (m.get('labels') or ()) or m.get('from_me') is True
        return ['email:' + a for _, a in addresses(m.get('to'))] if own else ['email:' + a for _, a in addresses(m.get('from'))[:1]]
    if kind == 'slack.message' and m.get('user_id'):
        return ['slack:' + str(m['user_id'])]
    if kind == 'teams.message' and m.get('from_email') and m.get('from_me') is not True:
        return ['email:' + str(m['from_email']).lower()]
    prefix = 'wa:' if kind == 'whatsapp.message' else 'tg:' if kind == 'telegram.message' else None
    if prefix:
        sender = str(m.get('sender_id') or '') if m.get('from_me') is not True else ''
        chat = str(m.get('chat_id') or '')
        who = sender or (chat if not chat.endswith('@g.us') else '')
        return [prefix + who.split('@')[0]] if who else []
    return []


def card_lead(db, event_id, first=None):
    """The person a to-do's main source is from (lead_identifiers), as a graph node id, or None. first: that event's
    kind and metadata when the caller read them already (the to-do list reads all at once)."""
    row = first or db.execute('SELECT kind,metadata FROM events WHERE id=?', (event_id,)).fetchone()
    if not row:
        return None
    try:
        m = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
    except ValueError:
        return None
    for identifier in lead_identifiers(row['kind'], m if isinstance(m, dict) else {}):
        node = resolve(db, identifier)
        if node and node['kind'] == 'person':
            return node['id']
    return None


def is_meeting(db, event_id, first=None):
    """Whether an event is a meeting (its calendar event or its notes). first: its row when the caller read it."""
    try:
        row = first or db.execute('SELECT kind FROM events WHERE id=?', (event_id,)).fetchone()
    except sqlite3.OperationalError:
        return False  # a bare graph without the events table
    return bool(row) and row['kind'] in MEETINGS


def colleague(row):
    """Whether a person row is one of the owner's colleagues (the graph's colleague mark)."""
    try:
        info = json.loads(row['info'] or '{}')
    except ValueError:
        return False
    return isinstance(info, dict) and info.get('colleague') in (True, 1)


def ordered(db, ids, found, first=None, unlinked=False):
    """A to-do's people (graph.card_people's rows, each person once): the sender of its first event first, then the
    people of each message in the review's order of its evidence, closest first within one. The owner's own post first
    names nobody, so the next message's people lead, not a teammate closer to the owner from an internal meeting.
    first: the first event's kind and metadata when the caller read them ({} when it is gone). unlinked: the sender
    leads also before the graph links their message to them (the to-do's chip; a same-matter check keeps to links)."""
    try:
        lead = None if first == {} else card_lead(db, ids[0], first)
    except sqlite3.OperationalError:
        lead = None  # a bare graph without the events table
    apart = set()  # colleagues on the meeting it is about: after anyone from outside on it, and none when only they are
    if not lead and unlinked and first != {} and is_meeting(db, ids[0], first):
        on = {r['id']: colleague(r) for r in found if r['event_id'] == ids[0]}
        if len(on) > 1 and all(on.values()):
            found = [r for r in found if r['event_id'] != ids[0]]  # a meeting of the owner's own team: the chip names no one
        apart = {i for i, mark in on.items() if mark}
    if lead and unlinked and not any(r['id'] == lead for r in found):
        found = db.execute("SELECT n.id,n.name,n.strength,n.info,o.id org_id,o.name org_name,o.info org_info,? event_id FROM graph_nodes n "
                           "LEFT JOIN graph_nodes o ON o.id=json_extract(n.info,'$.org') WHERE n.id=?", (ids[0], lead)).fetchall() + list(found)
    order = {e: n for n, e in reversed(list(enumerate(ids)))}
    return list({r['id']: r for r in sorted(found, key=lambda r: (r['id'] != lead, order.get(r['event_id'], len(ids)), r['id'] in apart))}.values())

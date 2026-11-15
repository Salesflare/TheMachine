"""Who a to-do is for: the sender of its main source (its first event, the message the review says the matter is
about), so a colleague of theirs on copy, or a teammate closer to the owner from a meeting on it, never leads its
person chip over who asked (graph.card_people)."""
import json
import sqlite3

from graph import addresses, relayed, resolve


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
    if lead and unlinked and not any(r['id'] == lead for r in found):
        found = db.execute("SELECT n.id,n.name,n.strength,n.info,o.id org_id,o.name org_name,o.info org_info,? event_id FROM graph_nodes n "
                           "LEFT JOIN graph_nodes o ON o.id=json_extract(n.info,'$.org') WHERE n.id=?", (ids[0], lead)).fetchall() + list(found)
    order = {e: n for n, e in reversed(list(enumerate(ids)))}
    return list({r['id']: r for r in sorted(found, key=lambda r: (r['id'] != lead, order.get(r['event_id'], len(ids))))}.values())

"""What we don't know about the people on a to-do: a gap note from The Machine's own synced data, no model call.

A preparation (Do it, a meeting prep, a to-do prepared ahead) reads the evidence and writes as if it knew how things
stand with the person. It doesn't always: the last word may be twelve days old, the owner may have written last with no
answer since, or the person may use a channel this Machine doesn't sync. Facts like these come from the stored signals
alone, so they are computed here, plainly, and handed to the preparation (assistant.preparation_prompt) so the result
can say what isn't known ("Last contact 12 days ago by email; nothing since.") instead of guessing past it.

Per person on the to-do (graph.card_people: who it is directly about, closest first):
- last contact: the newest message with them in any synced channel, when, on which channel and who wrote it;
- nothing since: by construction nothing newer is synced; when the owner wrote last, their last message is named too;
- open promises both ways (graph.open_between);
- channels they may have answered on that aren't synced: a WhatsApp number, a LinkedIn, Telegram, X or Slack identity
  for a service with no connected account here.

The to-do itself shows one short line (card_gap) only where it helps: their last message is STALE_DAYS old, or the
owner wrote last, nothing came back for WAITING_DAYS and they may have answered on a channel that isn't synced (the
waiting alone is often what the to-do says already). Fresh conversations get no line."""
from __future__ import annotations

import datetime as dt
import json
import sqlite3

import graph

# Message signals that count as contact, and the channel each is on (the words the card and the prompt use).
CHANNELS = {'gmail.message': 'email', 'ms_graph.message': 'email', 'outlook.message': 'email', 'salesflare.email': 'email',
            'slack.message': 'Slack', 'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram',
            'linkedin.message': 'LinkedIn', 'x.dm': 'X', 'intercom.conversation': 'Intercom'}
# Channels the person may use that this Machine may not sync: (channel, services that sync it, identifier prefixes and
# person_facts fields that show they use it).
ELSEWHERE = (('WhatsApp', ('whatsapp',), ('wa:',), ('phone',)),
             ('LinkedIn', ('linkedin',), ('li:',), ('linkedin_url',)),
             ('Telegram', ('telegram',), ('tg:',), ()),
             ('Slack', ('slack',), ('slack:',), ()),
             ('X', ('x',), ('x:',), ('x',)))
WAITING_DAYS = 3  # the owner wrote last: the card says so after this many days without an answer
STALE_DAYS = 14  # the last contact either way: the card says so after this many days
OPEN_STATUSES = ('pending', 'accepted', 'prepared', 'instructions')


def _time(value):
    at = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    return at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)


def _days(at, now):
    return max(0, (_time(now) - _time(at)).days)


def _identifiers(db, node_id):
    row = db.execute('SELECT info FROM graph_nodes WHERE id=?', (node_id,)).fetchone()
    info = json.loads(row['info'] or '{}') if row else {}
    return list(dict.fromkeys([node_id, *(info.get('identifiers') or info.get('ids') or [])])), info


def unsynced(db, node_id, services, identifiers=None, info=None):
    """The channels this person shows up on (or has a number or profile for) that no connected account here syncs."""
    if identifiers is None:
        identifiers, info = _identifiers(db, node_id)
    info = info or {}
    services = {str(s) for s in services}
    fields = set()
    try:
        marks = ','.join('?' for _ in identifiers)
        fields = {r[0] for r in db.execute(f'SELECT DISTINCT field FROM person_facts WHERE identifier IN ({marks})', identifiers)}
    except sqlite3.OperationalError:
        pass  # no enrichment yet
    if info.get('phones'):
        fields.add('phone')
    out = []
    for channel, synced_by, prefixes, facts in ELSEWHERE:
        if services & set(synced_by):
            continue
        if any(str(i).startswith(prefixes) for i in identifiers) or fields & set(facts):
            out.append(channel)
    return out


def person(db, node_id, name, services, mine, now, skip_card=None):
    """What is known and what isn't about one person, from synced signals only. mine(event) tells the owner's own
    message (assistant.own_message)."""
    identifiers, info = _identifiers(db, node_id)
    marks = ','.join('?' for _ in CHANNELS)
    rows = db.execute(f'SELECT e.id,e.kind,e.occurred_at,e.metadata FROM graph_events g JOIN events e ON e.id=g.event_id '
                      f'WHERE g.node_id=? AND g.direct=1 AND e.deleted=0 AND e.kind IN ({marks}) AND e.occurred_at<=? '
                      'ORDER BY e.occurred_at DESC,e.id DESC LIMIT 40', (node_id, *CHANNELS, now)).fetchall()
    out = {'id': node_id, 'name': name, 'last': None, 'theirs': None}
    for r in rows:
        own = bool(mine(dict(r)))
        if out['last'] is None:
            out['last'] = {'at': r['occurred_at'], 'channel': CHANNELS[r['kind']], 'mine': own, 'days': _days(r['occurred_at'], now)}
        if not own:
            out['theirs'] = {'at': r['occurred_at'], 'channel': CHANNELS[r['kind']], 'days': _days(r['occurred_at'], now)}
            break
    opened = graph.open_between(db, node_id, 2, skip_card)
    out['you_promised'], out['they_promised'] = opened.get('you_promised', []), opened.get('they_promised', [])
    out['unsynced'] = unsynced(db, node_id, services, identifiers, info)
    return out


def for_card(db, event_ids, services, mine, now, skip_card=None, limit=2):
    """The gap facts for the people a to-do is directly about (at most `limit`, closest first)."""
    try:
        people = graph.card_people(db, event_ids, limit=limit)[0]
    except (sqlite3.Error, ValueError, TypeError):
        return []
    return [person(db, p['id'], p['name'], services, mine, now, skip_card) for p in people if p.get('id') and p.get('name')]


def _ago(days):
    return 'today' if days == 0 else 'yesterday' if days == 1 else f'{days} days ago'


def prompt_lines(found):
    """The gap note for a preparation: one line per person, plain facts, and how to use them."""
    lines = []
    for p in found:
        last, theirs = p['last'], p['theirs']
        if not last:
            bits = ['no messages with them are synced']
        elif last['mine']:
            bits = [f"last contact {graph.short_date(last['at'])} ({_ago(last['days'])}) by {last['channel']}, from the owner; no reply synced since"
                    + (f" (their last message: {graph.short_date(theirs['at'])} by {theirs['channel']})" if theirs else ' (no message from them synced at all)')]
        else:
            bits = [f"last contact {graph.short_date(last['at'])} ({_ago(last['days'])}) by {last['channel']}, from them; nothing synced since"]
        for side, who in (('you_promised', 'the owner promised'), ('they_promised', 'they promised')):
            for x in p[side][:2]:
                bits.append(f"open: {who} to {x['what']}" + (f" by {graph.short_date(x['due'])}" if x.get('due') else ''))
        if p['unsynced']:
            bits.append(f"not synced here: {', '.join(p['unsynced'])} (they may have answered there)")
        lines.append(f"- {p['name']}: " + '; '.join(bits))
    if not lines:
        return ''
    return ('\n\nWhat we don\'t know (computed from synced signals only, nothing guessed). When it bears on the result, say it plainly '
            'in one short line instead of guessing past it, e.g. "Last contact 12 days ago by email; nothing since." Never say they '
            'replied, agreed or are waiting unless a synced message shows it:\n' + '\n'.join(lines))


def card_gap(found):
    """The one short line's facts for the to-do, or None when there is nothing worth a line (see the module docstring)."""
    for p in found:
        last = p.get('last')
        if not last:
            continue
        # The owner waiting on them is often what the to-do itself says ("no reply in 6 days"): a line only when it adds
        # where an answer may be that this Machine can't see. An old last word from them is worth a line on its own.
        if last['mine'] and last['days'] >= WAITING_DAYS and p['unsynced'] or not last['mine'] and last['days'] >= STALE_DAYS:
            return {'name': p['name'], 'days': last['days'], 'channel': last['channel'], 'wrote_last': bool(last['mine']),
                    'unsynced': p['unsynced'][:2]}
    return None

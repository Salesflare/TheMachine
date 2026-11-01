"""Inviting family at the right moment: a quiet line on a to-do (docs/family.md, Invite suggestions).

When the review judges that a to-do is the owner coordinating family life with one specific person (who picks up the
kids, a plan, a back-and-forth about the weekend) and that person is family as the Graph or the owner's own words say,
it passes `family_with` (their Graph node) with the to-do. This module decides whether the to-do then says
"Invite Sasha? Your Machines can sort this out without you asking each other.", by plain checks:

- the owner can invite to a Family Fleet: theirs (as its owner or an admin, with room left) or a new one from their
  account page; a Machine without the Network has no Family Fleet feature and never gets one;
- the person is no Work contact (a Work to-do, the Graph's Work side, a Work Fleet member), is not in the Family
  already and has no open invite to it (the directory lists open ones for its managers), and has an email address;
- at most once per person: one to-do carries it; Not now hides it for HIDE_DAYS; Invite never brings it back;
- the owner's switch (Settings, Fleet: Suggest inviting family) is on.

Invite opens the account page's existing invite form, prefilled with that one address, where the owner sees the email
before anything goes out. Nothing is sent from here. Every step is a line in Activity (Fleet)."""
from __future__ import annotations

import datetime as dt
import json
import re
import urllib.parse

import activity_log
from i18n import t

HIDE_DAYS = 90  # Not now
MAX_FAMILY = 6  # people in a Family Fleet, open invites included (the control plane's own limit)
SETTING = 'family_invite_suggest'  # fleet_meta: the owner's switch, on unless turned off
EMAIL = re.compile(r'[^@\s<>,;"]+@[^@\s<>,;"]+\.[^@\s<>,;"]+')
SCHEMA = ('CREATE TABLE IF NOT EXISTS family_invite_offers(person TEXT PRIMARY KEY,node_id TEXT,name TEXT NOT NULL,card_id TEXT,'
          'state TEXT NOT NULL,at TEXT NOT NULL,until TEXT)',
          'CREATE TABLE IF NOT EXISTS family_invite_log(id INTEGER PRIMARY KEY,at TEXT NOT NULL,person TEXT NOT NULL,name TEXT NOT NULL,'
          'what TEXT NOT NULL,card_id TEXT)')
CLOSED = ('completed', 'rejected', 'expired')


def ensure(db):
    for statement in SCHEMA:
        db.execute(statement)


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def person(db, node_id):
    """{'node_id', 'name', 'first', 'email', 'emails', 'side'} for a person in the Graph, else None. The address used is
    the first one the Graph lists for them."""
    if not isinstance(node_id, str) or not node_id or len(node_id) > 300:
        return None
    try:
        row = db.execute("SELECT id,name,info FROM graph_nodes WHERE id=? AND kind='person'", (node_id,)).fetchone()
    except Exception:  # no Graph yet
        return None
    if not row:
        return None
    info = json.loads(row['info'] or '{}')
    emails = []
    for value in [*(info.get('emails') or []), *(i[6:] for i in info.get('identifiers') or [] if str(i).startswith('email:')),
                  *([node_id[6:]] if node_id.startswith('email:') else [])]:
        value = str(value or '').strip().lower()
        if EMAIL.fullmatch(value) and value not in emails:
            emails.append(value)
    name = ' '.join(str(row['name'] or '').split())[:80]
    if not name or EMAIL.fullmatch(name):
        name = ''
    return {'node_id': row['id'], 'name': name, 'first': name.split(' ')[0] if name else '', 'email': emails[0] if emails else '',
            'emails': emails, 'side': info.get('side')}


def family_entry(fleets):
    return next((f for f in (fleets or {}).values() if (f or {}).get('kind') == 'family'), None)


def can_invite(fleets, account_url):
    """(True, family entry or None) when the owner can invite someone to a Family Fleet from their account page: as the
    owner or an admin of theirs while it has room, or by starting one. No account page: no Family Fleet feature."""
    if not account_url:
        return False, None
    family = family_entry(fleets)
    if not family:
        return True, None
    me = family.get('me') if isinstance(family.get('me'), dict) else next((m for m in family.get('members') or [] if m.get('me')), {})
    if (me or {}).get('role') not in ('owner', 'admin'):
        return False, family
    people = len(family.get('members') or []) + len(family.get('invited') or [])
    return people < MAX_FAMILY, family


def excluded(found, fleets, work_card=False, own_domains=()):
    """Why this person gets no suggestion, or None: a Work contact, in the Family or invited to it, or no address."""
    if not found or not found['email']:
        return 'no address'
    if work_card or found.get('side') == 'work':
        return 'work'
    mine = set(found['emails'])
    if any(e.rsplit('@', 1)[1] in own_domains for e in mine):
        return 'work'
    for f in (fleets or {}).values():
        kind = (f or {}).get('kind')
        for m in (f or {}).get('members') or []:
            if isinstance(m, dict) and not m.get('me') and mine & {str(e).strip().lower() for e in (m.get('emails') or []) + [m.get('account_email') or '']}:
                if kind in ('work', 'family'):
                    return 'work' if kind == 'work' else 'member'
        if kind == 'family' and mine & {str(e).strip().lower() for e in f.get('invited') or []}:
            return 'invited'
    return None


def invite_url(account_url, found, family=None):
    """The account page's invite form for the Family, prefilled with this one person (cloud: fleet.account_html)."""
    query = urllib.parse.urlencode({'tab': 'fleet', 'invite': 'family', 'to': found['email'], 'name': found['name']})
    anchor = f"invites-{family['id']}" if family and re.fullmatch(r'fl_[0-9a-f]{16}', str(family.get('id') or '')) else 'fleet'
    return f'{account_url}?{query}#{anchor}'


def log(db, key, name, what, card_id=None):
    db.execute('INSERT INTO family_invite_log(at,person,name,what,card_id) VALUES(?,?,?,?,?)', (_now(), key, name, what, card_id))


def offer(db, card_id, node_id, fleets, account_url, on=True, work_card=False, own_domains=(), now=None):
    """Put the suggestion on this to-do when every check passes: 'offered', else why not (for the review's reply)."""
    if not on:
        return 'off'
    able, family = can_invite(fleets, account_url)
    if not able:
        return 'no family invites'
    found = person(db, node_id)
    why = excluded(found, fleets, work_card, own_domains)
    if why:
        return why
    ensure(db)
    now = now or _now()
    rows = [db.execute('SELECT * FROM family_invite_offers WHERE person=?', (e,)).fetchone() for e in found['emails']]
    row = next((r for r in rows if r), None)
    if row and not (row['state'] == 'later' and (row['until'] or '') <= now):
        return 'once'  # one to-do carries it; after Not now only once HIDE_DAYS passed; never after Invite
    db.execute('INSERT OR REPLACE INTO family_invite_offers(person,node_id,name,card_id,state,at,until) VALUES(?,?,?,?,?,?,NULL)',
               (row['person'] if row else found['email'], found['node_id'], found['name'] or found['email'], str(card_id), 'offered', now))
    log(db, row['person'] if row else found['email'], found['name'] or found['email'], 'offered', str(card_id))
    return 'offered'


def annotate(db, suggestions, fleets, account_url, on=True, own_domains=()):
    """`family_invite` on the open to-do that carries one, while every check still passes (someone may have joined, been
    invited or moved to Work since): {'name', 'first', 'line', 'url'}."""
    if not on or not suggestions:
        return
    able, family = can_invite(fleets, account_url)
    if not able:
        return
    try:
        rows = {r['card_id']: r for r in db.execute("SELECT * FROM family_invite_offers WHERE state='offered'")}
    except Exception:  # no table yet: nothing offered
        return
    for s in suggestions:
        r = rows.get(str(s.get('id')))
        if not r or s.get('status') in CLOSED:
            continue
        found = person(db, r['node_id'])
        if not found or r['person'] not in found['emails']:
            found = found and {**found, 'email': r['person'], 'emails': [r['person'], *found['emails']]}
        if excluded(found, fleets, s.get('scope') == 'work', own_domains):
            continue
        first = found['first'] or found['email']
        s['family_invite'] = {'name': found['name'] or found['email'], 'first': first, 'email': found['email'],
                              'question': t('Invite {}?', first),
                              'line': t('Your Machines can sort this out without you asking each other.'),
                              'url': invite_url(account_url, found, family)}


def act(db, card_id, do, account_url, fleets, now=None):
    """The owner's tap: 'open' (Invite: the account page's form, prefilled; never suggested again) or 'later' (Not now:
    hidden for HIDE_DAYS). Nothing is sent from here."""
    if do not in ('open', 'later'):
        raise ValueError('Invite or Not now')
    ensure(db)
    row = db.execute("SELECT * FROM family_invite_offers WHERE card_id=? AND state='offered'", (str(card_id),)).fetchone()
    if not row:
        raise ValueError('That suggestion is gone')
    now = now or _now()
    if do == 'later':
        until = (dt.datetime.fromisoformat(now) + dt.timedelta(days=HIDE_DAYS)).isoformat(timespec='seconds')
        db.execute("UPDATE family_invite_offers SET state='later',at=?,until=? WHERE person=?", (now, until, row['person']))
        log(db, row['person'], row['name'], 'later', row['card_id'])
        return {'state': 'later', 'until': until}
    found = person(db, row['node_id']) or {'node_id': row['node_id'], 'name': row['name'], 'email': row['person'], 'emails': [row['person']]}
    found = {**found, 'email': row['person'], 'name': found.get('name') or row['name']}
    db.execute("UPDATE family_invite_offers SET state='invited',at=? WHERE person=?", (now, row['person']))
    log(db, row['person'], row['name'], 'opened', row['card_id'])
    return {'state': 'invited', 'url': invite_url(account_url, found, family_entry(fleets))}


LINES = {'offered': ('Suggested inviting {} to the Family', 'Suggested'),
         'opened': ('Opened the Family invite for {}', 'Opened'),
         'later': ('Not now: inviting {} to the Family', 'Hidden for 90 days')}


def activity_lines(db, limit):
    """Activity, Fleet: each suggestion, and what the owner did with it."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='family_invite_log'").fetchone():
        return []
    out = []
    for r in db.execute('SELECT * FROM family_invite_log ORDER BY id DESC LIMIT ?', (limit,)):
        what, status = LINES.get(r['what'], LINES['offered'])
        out.append({'id': f"family-invite:{r['id']}", 'kind': 'fleet', 'at': r['at'], 'what': t(what, r['name']), 'where': t('Family'),
                    'outcome': 'done', 'status': t(status), 'by': None,
                    'todo': {'id': r['card_id'], 'title': ''} if r['card_id'] else None, 'detail': None})
    return out


activity_log.register('fleet', activity_lines)

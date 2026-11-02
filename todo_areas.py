"""A to-do's area: Personal, or Work at one company, and moving a to-do from one to the other.

A to-do's area comes from its accounts (assistant.suggestion_scope): what it may read and send from, and whether it
counts as Work for timing, sharing and handoffs, all follow them. The owner can move a to-do to another of their areas
(More, Move to Work): its accounts become that area's, so everything that follows the accounts follows the move. The
messages it came from stay where they are; only the to-do moves. Nothing moves a to-do by itself: its run can ask for a
move (preparation_blocked move_to), which the to-do shows as a button for the owner's tap.

An area is 'personal' (every account with a personal boundary) or a company: a work boundary ('work:Acme', the accounts
with it). An account whose own `scope` says the other side (a work boundary labeled personal) is in neither. A work
boundary named after its own source ('work:linkedin' on a LinkedIn account, 'work:x' on an X account: an owner's own
profile, from before the setup asked for a company) is Work but no company: such a to-do can move to any company, and
nothing moves to it."""
from __future__ import annotations

import json

PERSONAL = 'personal'


def _side(account):
    kind = str(account.get('boundary') or '').partition(':')[0].lower()
    if kind not in ('work', 'personal'):
        return None  # the Machine itself (owner:system), or never placed
    scope = account.get('scope')
    return kind if scope in (None, kind) else None


def area_of_account(account):
    """The area one account is in, or None."""
    side = _side(account)
    return PERSONAL if side == 'personal' else str(account['boundary']) if side == 'work' else None


def _sources(account):
    return {str(account.get(k) or '').partition('-')[0].casefold() for k in ('service', 'transport')} - {''}


def companies(accounts):
    """The owner's companies: each work boundary with its accounts, unless it is only named after its own source (the
    service of every account in it: 'work:linkedin' holding just a LinkedIn profile)."""
    found = {}
    for a in accounts or ():
        area = area_of_account(a)
        if area and area != PERSONAL:
            found.setdefault(area, []).append(a)
    return [x for x in found if not all(name(x).casefold() in _sources(a) for a in found[x])]


def name(area):
    """A company's name as the owner gave it, the way Connections shows it (Work · Acme)."""
    return str(area).partition(':')[2].strip()


def areas(accounts):
    """The owner's areas, Personal first then each company: [{'id', 'label', 'name'}]. A company is named only when
    there are several ("Work at Acme"); with one it is just Work."""
    personal = any(area_of_account(a) == PERSONAL for a in accounts or ())
    work = sorted(companies(accounts), key=str.lower)
    return ([{'id': PERSONAL, 'label': label(PERSONAL)}] if personal else []) + [{'id': x, 'label': label(x, len(work)), 'name': name(x)} for x in work]


def label(area, companies=1):
    """Personal, Work, or Work at Acme when the owner has more than one company."""
    if area == PERSONAL:
        return 'Personal'
    org = name(area)
    return f'Work at {org}' if companies > 1 and org else 'Work'


def moved_line(area, companies=1):
    """The to-do's event line after a move: a whole sentence per case (i18n)."""
    if area == PERSONAL:
        return 'Moved to Personal'
    org = name(area)
    return ('Moved to Work at {}', org) if companies > 1 and org else 'Moved to Work'


WORK = 'work'  # a to-do whose Work accounts are in no company (a 'work:linkedin' profile's): Work, and any company is another area


def current(account_ids, accounts):
    """The one area a to-do is in now, from its accounts: a company when its Work accounts are all that company's,
    Personal when it has no Work account, Work (no company) when its Work accounts are in none. None when it spans
    several companies (a merged one) or none is known."""
    ids = json.loads(account_ids or '[]') if isinstance(account_ids, str) else list(account_ids or ())
    mine = {area_of_account(a) for a in accounts or () if a.get('id') in ids} - {None}
    work = {x for x in mine if x != PERSONAL}
    if work:
        firms = work & set(companies(accounts))
        return (next(iter(firms)) if len(firms) == 1 else None) if firms else WORK
    # suggestion_scope reads a to-do with no Work account as Personal
    return PERSONAL if mine or ids else None


def accounts_in(area, accounts):
    """The ids of the accounts in an area, in config order."""
    return [a['id'] for a in accounts or () if area_of_account(a) == area]


def check(area, account_ids, accounts):
    """The area to move a to-do to, checked: one of the owner's, with accounts, and not the one it is in."""
    if not isinstance(area, str) or area not in {x['id'] for x in areas(accounts)}:
        raise ValueError('Pick one of your areas')
    if area == current(account_ids, accounts):
        raise ValueError('It is in that area already')
    return area


def pointed(people, accounts, here=None, domain=lambda value: ''):
    """The area a to-do's people point to, for the picker to start on: Personal when they are Personal, a company when
    they are heard on its accounts or work at one of its domains. None when they point nowhere, or to several, or to
    where it is already. people: [{'side', 'accounts', 'org_domain'}] (graph person nodes); domain(email): its domain."""
    firms = set(companies(accounts))
    owned = {}
    for a in accounts or ():
        area = area_of_account(a)
        if area in firms and domain(a.get('email')):
            owned.setdefault(domain(a.get('email')), set()).add(area)
    where = {a.get('id'): area_of_account(a) for a in accounts or ()}
    ids = {x['id'] for x in areas(accounts)}
    votes = set()
    for p in people or ():
        if p.get('side') == 'personal':
            votes.add(PERSONAL)
            continue
        found = ({where.get(i) for i in p.get('accounts') or ()} & firms) | owned.get(str(p.get('org_domain') or '').lower(), set())
        if len(found) == 1:
            votes |= found
    return next(iter(votes)) if len(votes) == 1 and votes <= ids and votes != {here} else None

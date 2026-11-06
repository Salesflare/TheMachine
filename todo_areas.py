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
nothing moves to it. Mail in one company's mailbox for another company of the owner's goes to that company from the
start (owner_companies, the review's suggest company), also one whose accounts are labeled personal.

A matter of the owner's own life (family, friends, home) that came in on a work mailbox is Personal from the start
(personal_accounts: the review's personal or family_with, or only people from the owner's own life on it). With a
Personal area it gets that area's accounts, as a move does. Without one (only work accounts connected) it keeps the
mailbox it came in on and is pinned Personal (the to-do's area column): its label, sharing and handoffs follow the pin,
so a family matter is never offered to a Work Fleet. A move to Work takes the pin off."""
from __future__ import annotations

import json
import re

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


def current(account_ids, accounts, pinned=None):
    """The one area a to-do is in now, from its accounts: a company when its Work accounts are all that company's,
    Personal when it has no Work account, Work (no company) when its Work accounts are in none. None when it spans
    several companies (a merged one) or none is known. pinned: the to-do's area column; Personal there is Personal,
    whatever its accounts (a family matter on a work mailbox, when there is no Personal area)."""
    if pinned == PERSONAL:
        return PERSONAL
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


def check(area, account_ids, accounts, pinned=None):
    """The area to move a to-do to, checked: one of the owner's, with accounts, and not the one it is in."""
    if not isinstance(area, str) or area not in {x['id'] for x in areas(accounts)}:
        raise ValueError('Pick one of your areas')
    if area == current(account_ids, accounts, pinned):
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


def owner_companies(accounts):
    """Every company of the owner's, also one whose accounts they labeled Personal (a work boundary with scope:
    personal, which is in neither area): [{'id', 'name', 'domains', 'personal'}]. A to-do about one of them lands in it
    (company_accounts): its Work, or Personal when its accounts are labeled personal."""
    found = {}
    for a in accounts or ():
        boundary = str(a.get('boundary') or '')
        if boundary.partition(':')[0].lower() != 'work' or not name(boundary):
            continue
        found.setdefault(boundary, []).append(a)
    out = []
    for boundary, held in found.items():
        if all(name(boundary).casefold() in _sources(a) for a in held):
            continue  # an own profile named after its source ('work:linkedin'): no company
        domains = sorted({str(a.get('email') or '').rpartition('@')[2].lower() for a in held if '@' in str(a.get('email') or '')[1:]})
        out.append({'id': boundary, 'name': name(boundary), 'domains': domains,
                    'personal': all(a.get('scope') == PERSONAL for a in held)})
    return sorted(out, key=lambda c: c['name'].lower())


def company_accounts(company, accounts):
    """The accounts a to-do about one of the owner's companies gets: that company's own, checked."""
    if company not in {c['id'] for c in owner_companies(accounts)}:
        raise ValueError('company: one of the owner\'s companies: ' + ', '.join(c['id'] for c in owner_companies(accounts)))
    return [a['id'] for a in accounts if a.get('boundary') == company]


def personal_accounts(accounts):
    """The accounts a to-do of the owner's own life gets (Store.suggest personal): the Personal area's, or None when
    there is none, and it keeps its own accounts, pinned Personal."""
    return accounts_in(PERSONAL, accounts) or None


ADDRESS = re.compile(r'[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)')


def addresses(text):
    """The email addresses a to-do's words mention, lowercased, at most ten."""
    return list(dict.fromkeys(m.group(0).lower().rstrip('.') for m in ADDRESS.finditer(str(text or ''))))[:10]


def mentioned(text, accounts, domain=lambda value: ''):
    """The area a new to-do's words point to: a company they name ("the Acme inbox") or an address of one of its
    mailboxes or domains, Personal for an address of a Personal mailbox. None when they point nowhere or to several.
    domain(email): its domain, '' for a free mail one (a gmail.com address points to no company)."""
    words = str(text or '')
    ids = {x['id'] for x in areas(accounts)}
    votes = set()
    for company in companies(accounts):
        org = name(company)
        if len(org) >= 3 and re.search(r'(?<![\w@.])' + re.escape(org) + r'(?![\w])', words, re.IGNORECASE):
            votes.add(company)
    found = addresses(words)
    for a in accounts or ():
        area, own = area_of_account(a), str(a.get('email') or '').lower()
        if area not in ids or '@' not in own:
            continue
        firm = domain(own)
        if own in found or (area != PERSONAL and firm and any(domain(x) == firm for x in found)):
            votes.add(area)
    return next(iter(votes)) if len(votes) == 1 else None


def most_used(rows, accounts):
    """The area most of the owner's recent to-dos are in, for a new one nothing places: rows are (account_ids, area
    column). None on a tie or when none is in one of their areas."""
    ids = {x['id'] for x in areas(accounts)}
    counts = {}
    for account_ids, pinned in rows:
        x = current(account_ids, accounts, pinned)
        if x in ids:
            counts[x] = counts.get(x, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
        return None
    return ranked[0][0]

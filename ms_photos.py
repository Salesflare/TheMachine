"""People's photos from Microsoft 365 and Outlook.com, through Microsoft Graph (ms_graph.py), with the two optional
scopes Outlook's consent asks for:

- colleagues (User.ReadBasic.All): GET /users/{address}/photos/96x96/$value (48x48 when there is no 96), only for
  people already in the graph who show no photo, by a work address on one of the owner's organization's verified
  domains (GET /organization). A personal account (Outlook.com) has no colleagues: nothing is asked, and it is never
  asked to reconnect for them.
- Outlook contacts (Contacts.Read): once a day per account, the owner's contacts (their addresses, job title and
  company), then the photo of each contact who is in the graph and shows none (GET /me/contacts/{id}/photo/$value).
  Their job title and company go to the person's facts (enrichment.offer_facts), as a contact's record.

Only the owner's own Outlook accounts, never one shared from a Fleet. A photo is downloaded with the account's token
(these links need it, so no link is kept), checked to be a small JPEG, PNG or WebP by its own bytes (at most
enrichment.PHOTO_BYTES) and saved once here as the person's (enrichment.keep_photo). Someone with none is asked again
after 30 days (enrichment.PHOTO_RETRY_DAYS), after an error the next day; at most PER_DAY asks a day for all accounts.

Without a scope nothing of that kind is asked: the grant is read once a day (ms_graph.grant). An account connected
before these scopes, whose broker offers them now, asks to connect again (machine/app/reconnect_asks.py, through
the ask the worker passes); one whose organization refused them is not offered them, and says nothing."""
from __future__ import annotations

import datetime as dt
import json
import logging

import enrichment
import ms_graph

LOG = logging.getLogger('personal-assistant')
PER_DAY = 200
PER_PASS = 40
CHECK_HOURS = 24  # the grant and the organization's domains
ASKING_MINUTES = 15  # sooner while it asks to reconnect: its row goes soon after the owner did
CONTACT_PAGES = 10
COLLEAGUE, CONTACT = 'User.ReadBasic.All', 'Contacts.Read'
SCOPES = (COLLEAGUE, CONTACT)
SIZES = ('96x96', '48x48')
SCHEMA = ('CREATE TABLE IF NOT EXISTS ms_photo_asks(identifier TEXT PRIMARY KEY,asked_at TEXT NOT NULL,outcome TEXT NOT NULL)',
          'CREATE TABLE IF NOT EXISTS ms_photo_accounts(email TEXT PRIMARY KEY,scopes TEXT NOT NULL,domains TEXT NOT NULL,'
          "offered TEXT NOT NULL DEFAULT '[]',checked_at TEXT NOT NULL)")


class _NotGranted(Exception):
    pass


def tables(db):
    for statement in SCHEMA:
        db.execute(statement)


def accounts(config):
    """The owner's own Outlook mail accounts, once per address (never one shared from a Fleet)."""
    seen = {}
    for account in config.get('accounts', []):
        if (account.get('service') == 'outlook' and account.get('transport') in ('broker', 'graph') and account.get('email')
                and not account.get('shared')):
            seen.setdefault(account['email'].lower(), account)
    return list(seen.values())


def check(connect, config, credential, account, now, read=None, ask=None):
    """The account's photo scopes and organization domains, read again once a day (every ASKING_MINUTES while its
    broker offers more): (scopes, domains). Tells ask(db, account id, missing, now) whether to ask the owner to
    reconnect (machine/app/reconnect_asks.py): only for what its broker offers, so never where the organization
    refused them. Nothing on a failed read (kept as it was, tried again later)."""
    email = account['email'].lower()
    with connect() as db:
        tables(db)
        row = db.execute('SELECT scopes,domains,checked_at,offered FROM ms_photo_accounts WHERE email=?', (email,)).fetchone()
    wait = dt.timedelta(minutes=ASKING_MINUTES) if row and json.loads(row[3]) else dt.timedelta(hours=CHECK_HOURS)
    if row and row[2] > (dt.datetime.fromisoformat(now) - wait).isoformat():
        return set(json.loads(row[0])), set(json.loads(row[1]))
    scopes, domains = (set(json.loads(row[0])), set(json.loads(row[1]))) if row else (set(), set())
    offered = None
    try:
        granted, offered = ms_graph.grant(config, credential, account)
        if ms_graph.personal(account):  # an Outlook.com account has no colleagues: reconnecting for them brings nothing
            offered = set(offered) - {COLLEAGUE}
        scopes ={s for s in SCOPES if ms_graph.ANSWERS[s] & granted}
        domains = _domains(config, credential, account, read) if COLLEAGUE in scopes else set()
    except ms_graph.GraphError:
        pass
    with connect() as db:
        tables(db)
        missing = sorted(set(offered or ()) & (set(SCOPES) - scopes))
        db.execute('INSERT INTO ms_photo_accounts(email,scopes,domains,offered,checked_at) VALUES(?,?,?,?,?) ON CONFLICT(email) DO UPDATE SET '
                   'scopes=excluded.scopes,domains=excluded.domains,offered=excluded.offered,checked_at=excluded.checked_at',
                   (email, json.dumps(sorted(scopes)), json.dumps(sorted(domains)), json.dumps(missing), now))
        if offered is not None and ask:
            ask(db, account['id'], missing, now)  # gone once granted, or no longer offered (refused)
    return scopes, domains


def _domains(config, credential, account, read=None):
    """The verified domains of the account's organization, without free-mail ones; none for a personal account."""
    read = read or (lambda method, params, raw=False: ms_graph.call(config, credential, account, method, params, raw=raw, timeout=20))
    try:
        answer = read('organization', {'$select': 'verifiedDomains'})
    except ms_graph.GraphError:
        return set()
    found = {str(d.get('name') or '').strip().lower() for o in answer.get('value') or [] if isinstance(o, dict)
             for d in o.get('verifiedDomains') or [] if isinstance(d, dict)}
    return {d for d in found if '.' in d and not enrichment.FREEMAIL.match(d) and not d.endswith('.onmicrosoft.com')}


def _due(db, now):
    """(asks left today, {identifier: when it may be asked again})"""
    stamp = dt.datetime.fromisoformat(now)
    today = stamp.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT00:00:00')
    left = PER_DAY - db.execute('SELECT count(*) FROM ms_photo_asks WHERE asked_at>=?', (today,)).fetchone()[0]
    again = {}
    for identifier, at, outcome in db.execute('SELECT identifier,asked_at,outcome FROM ms_photo_asks'):
        wait = dt.timedelta(days=1 if outcome == 'error' else enrichment.PHOTO_RETRY_DAYS)
        again[identifier] = (dt.datetime.fromisoformat(at) + wait).isoformat()
    return left, again


def wanted(db, now):
    """[(node id, [work addresses])] of the people in the graph who show no photo, strongest first, with the
    addresses not asked lately."""
    _, again = _due(db, now)
    rows = db.execute("SELECT id,info FROM graph_nodes WHERE kind='person' ORDER BY strength DESC").fetchall()
    bare = enrichment.without_photo(db, [{'id': r[0], 'info': r[1]} for r in rows])
    out = []
    for node, info in rows:
        if node not in bare:
            continue
        ids = [i for i in (json.loads(info or '{}').get('identifiers') or []) if str(i).startswith('email:') and '@' in str(i)]
        ids = [i for i in ids if again.get(i, '') <= now]
        if ids:
            out.append((node, ids))
    return out


def _photo(config, credential, account, method, params, fetch=None):
    """(bytes, type), 'none' when they have none (or it isn't a small image), None after an error. _NotGranted when
    the account lacks the scope."""
    fetch = fetch or (lambda m, p: ms_graph.call(config, credential, account, m, p, raw=True, timeout=15))
    try:
        data = fetch(method, params)
    except ms_graph.GraphError as error:
        if error.category == 'microsoft_scope_not_granted' or error.status == 403:
            raise _NotGranted() from None
        return 'none' if error.status == 404 else None
    kind = enrichment.image_type(data or b'')
    return (data, kind) if kind and len(data) <= enrichment.PHOTO_BYTES else 'none'


def _keep(connect, node, identifier, got, now):
    with connect() as db:
        tables(db)
        saved = got not in (None, 'none') and enrichment.keep_photo(db, node, got, now)
        outcome = 'saved' if saved else 'error' if got is None else 'none'
        db.execute('INSERT INTO ms_photo_asks(identifier,asked_at,outcome) VALUES(?,?,?) ON CONFLICT(identifier) DO UPDATE SET '
                   'asked_at=excluded.asked_at,outcome=excluded.outcome', (identifier, now, outcome))
    return bool(saved)


def colleague_photos(connect, config, credential, account, domains, now, limit, fetch=None):
    """Colleagues' photos by address, for people without one. Returns (saved, asked)."""
    with connect() as db:
        tables(db)
        people = wanted(db, now)
    saved = asked = 0
    for node, ids in people:
        identifier = next((i for i in ids if i.rsplit('@', 1)[1] in domains), None)
        if not identifier:
            continue
        if asked >= limit:
            break
        asked += 1
        got = 'none'
        try:
            for size in SIZES:
                got = _photo(config, credential, account, 'users.photo', {'user': identifier.split(':', 1)[1], 'size': size}, fetch)
                if got != 'none':
                    break
        except _NotGranted:
            break
        saved += _keep(connect, node, identifier, got, now)
    return saved, asked


def contacts(config, credential, account, read=None):
    """[(contact id, [identifiers], {'title', 'company'})] of the owner's Outlook contacts with an address."""
    read = read or (lambda method, params: ms_graph.call(config, credential, account, method, params, timeout=30))
    out, link = [], None
    for _ in range(CONTACT_PAGES):
        try:
            page = read('contacts.list', {'$link': link} if link else {'$select': 'emailAddresses,jobTitle,companyName', '$top': 500})
        except ms_graph.GraphError:
            break
        for contact in page.get('value') or []:
            if not isinstance(contact, dict) or not contact.get('id'):
                continue
            ids = list(dict.fromkeys('email:' + str(e.get('address')).strip().lower() for e in contact.get('emailAddresses') or []
                                     if isinstance(e, dict) and '@' in str(e.get('address') or '')))
            if ids:
                out.append((str(contact['id']), ids, {'title': contact.get('jobTitle') or '', 'company': contact.get('companyName') or ''}))
        link = page.get('@odata.nextLink')
        if not link:
            break
    return out


def contact_photos(connect, config, credential, account, now, limit, read=None, fetch=None):
    """Once a day: the account's contacts' facts, and photos for those in the graph without one. Returns (saved, asked,
    facts changed)."""
    source = 'outlook:' + account['email'].lower()
    with connect() as db:
        if not enrichment.contact_run_due(db, source, now):
            return 0, 0, 0
    found = contacts(config, credential, account, read)
    with connect() as db:
        tables(db)
        known = enrichment.graph_people(db)
        facts = enrichment.offer_facts(db, [(ids, fields, enrichment.RECORD) for _, ids, fields in found
                                            if any(i in known for i in ids) and (fields['title'] or fields['company'])], 'outlook', now)
        people = dict((i, node) for node, ids in wanted(db, now) for i in ids)
        enrichment.contact_run_done(db, source, now)
    saved = asked = 0
    for contact_id, ids, _ in found:
        identifier = next((i for i in ids if i in people), None)
        if not identifier:
            continue
        if asked >= limit:
            break
        asked += 1
        try:
            got = _photo(config, credential, account, 'contacts.photo', {'id': contact_id}, fetch)
        except _NotGranted:
            break
        saved += _keep(connect, people.pop(identifier), identifier, got, now)
        for other in ids:
            people.pop(other, None)
    return saved, asked, facts


def step(connect, config, credential, now, stop=lambda: False, ask=None):
    """One pass for every own Outlook account: the grant once a day, then contacts' and colleagues' photos within the
    day's budget. Returns (photos saved, facts changed)."""
    saved = facts = 0
    for account in accounts(config):
        if stop():
            break
        try:  # one account's trouble never stops the others, nor the other photo sources after this
            scopes, domains = check(connect, config, credential, account, now, ask=ask)
            with connect() as db:
                tables(db)
                left = min(PER_PASS, _due(db, now)[0])
            if CONTACT in scopes and left > 0:
                got, asked, changed = contact_photos(connect, config, credential, account, now, left)
                saved, facts, left = saved + got, facts + changed, left - asked
            if COLLEAGUE in scopes and domains and left > 0:
                saved += colleague_photos(connect, config, credential, account, domains, now, left)[0]
        except Exception as error:  # noqa: BLE001 - logged by kind only, tried again next pass
            LOG.warning('outlook photos error=%s', type(error).__name__)
    return saved, facts

"""A question in Search about one of the owner's own mailboxes or chat accounts (search_ask.py): which one, and what the
Machine itself knows of it.

The first turn gets a short list of the connections of the area in view (listed) and picks from it by number. What it
picks is checked here against that list and the config (resolve), so a question never reads a connection the model made
up, and an address of the owner's own is always a mailbox of theirs, never the person a question is about. An address
or name it gives back has to be in the question as typed. Only the owner's own connections count, never one shared
with them from a Fleet.

What messages can't tell goes to the answer as facts: how the connection is doing in Connections' own words (health, the
same as connectorHealth in dashboard/connections-shared.js), when it was last read in full, or that it isn't connected.
Never an error code or an id."""
import datetime as dt
import re

import abilities
import graph
import i18n
import own_addresses
import search_ask
from machine import names
from machine.kinds import KINDS
from machine.services import SERVICES
from timeutil import now

LISTED = 12        # connections the first turn can pick from, mailboxes first
NAME_CHARS = 60    # of each one's name there
TOLD = 4           # connections whose state goes to the answer: more than that, only what doesn't read well
ADDRESS = re.compile(r'[^\s<>"\'(),;:]+@[^\s<>"\'(),;:]+\.[^\s<>"\'(),;:.?!]+')
MESSAGE_SERVICES = frozenset(own_addresses.MAIL_SERVICES) | {KINDS[k]['service'] for k in graph.MESSAGE_KINDS if KINDS.get(k, {}).get('service')}
HELP = re.compile(r'(auth|unauthor|forbidden|permission|invalid_grant|signin_expired|HTTP_40[13])')
# what a chat app's own stop says (dashboard/todos-cards.js TELEGRAM_STOP)
STOPS = {'telegram_logged_out': lambda t: t('Logged out of Telegram'), 'telegram_app_blocked': lambda t: t('Telegram stopped accepting the app ID'),
         'signal_unlinked': lambda t: t('Signal unlinked this Machine'), 'whatsapp_unlinked': lambda t: t('WhatsApp unlinked this Machine'),
         'signal_outdated': lambda t: t('Update The Machine for Signal')}
FLAKY_FAILURES, FLAKY_HOURS = 6, 3
UNREAD = 'so anything newer is not known'


def _clean(text):
    return ' '.join(str(text or '').replace('<<<', '').replace('>>>', '').split())


def own(config):
    """The owner's own connections that bring in messages Ask can read."""
    return [a for a in own_addresses.own_accounts(config) if a.get('id') and names.account_service(a) in MESSAGE_SERVICES]


def name(account, accounts=()):
    """'Gmail sam@acme.example': its kind and its name on Connections, with its address when that doesn't say it."""
    as_is = lambda text, *args: i18n.fill(text, args)
    title, detail = names.card_title(account, accounts, t=as_is), names.card_detail(account)
    kind = names.service_name(names.account_service(account)) or ''
    said = title if kind.casefold() in title.casefold() else f'{kind} {title}'
    return _clean(said + (f' ({detail})' if detail and detail.casefold() not in title.casefold() else ''))[:NAME_CHARS]


def listed(app, area):
    """[{'id', 'name', 'side', 'mail'}] of the owner's own connections in the area in view, mailboxes first, each kind in the
    order of Connections: what the first turn may pick from."""
    ids, accounts = set(app.search_ask_accounts(area)), own_addresses.own_accounts(app.config)
    found = sorted((a for a in own(app.config) if a['id'] in ids), key=lambda a: names.account_service(a) not in own_addresses.MAIL_SERVICES)
    return [{'id': a['id'], 'name': name(a, accounts), 'side': graph.account_side(a) or '',
             'mail': names.account_service(a) in own_addresses.MAIL_SERVICES} for a in found[:LISTED]]


def by_address(db, config, address):
    """The owner's own connections (any kind) that are this address: its account's own, else the mailbox that also
    sends as it."""
    accounts = own_addresses.own_accounts(config)
    found = [a for a in accounts if own_addresses.clean(a.get('email')) == address or address in {own_addresses.clean(e) for e in a.get('owner_emails') or ()}]
    if not found:
        also = {i for i, entries in own_addresses.fetched(db, config).items()
                if any(own_addresses.clean(e.get('address')) == address and not e.get('other_server') for e in entries)}
        found = [a for a in accounts if a.get('id') in also]
    return found


def _known(config, words):
    """Whether some connection of any area, kind or owner could be what these words name: then nothing is said to be
    missing."""
    said = words.casefold()
    for a in config.get('accounts', []):
        kind, title = (names.service_name(names.account_service(a)) or '').casefold(), name(a).casefold()
        if said in title or (kind and kind in said):
            return True
    return False


def resolve(app, db, plan, found, area, question):
    """What a plan's picks come to, checked: {'ids', 'names', 'missing', 'elsewhere', 'other', 'outside'} (the picked
    connections of the list, addresses connected nowhere, ones of the other area, ones that are only a calendar or
    another kind, words for one that isn't in view), or None for a question about no connection of theirs. Takes an own
    address out of plan['person']."""
    config, said = app.config, question.casefold()
    in_view = set(app.search_ask_accounts(area))
    can_read = {a['id'] for a in own(config)}
    ids, missing, elsewhere, other, outside = [], [], [], [], []
    addresses, words = [], []
    for pick in plan.get('connections') or ():
        if isinstance(pick, int):
            if 1 <= pick <= len(found):
                ids.append(found[pick - 1]['id'])
            continue
        address = ADDRESS.search(pick)
        if address:
            addresses.append(address[0].casefold())
        elif pick.casefold() in said:
            words.append(pick)
    mine = graph.Owner(config, db).emails
    person = ADDRESS.search(plan.get('person') or '')
    if person and (person[0].casefold() in mine or by_address(db, config, person[0].casefold())):
        addresses.append(person[0].casefold())
        plan['person'] = ''
    for address in dict.fromkeys(a for a in addresses if a in said):
        accounts = by_address(db, config, address)
        readable = [a for a in accounts if a['id'] in can_read]
        if any(a['id'] in in_view for a in readable):
            ids += [a['id'] for a in readable if a['id'] in in_view]
        elif readable:
            elsewhere.append((address, graph.account_side(readable[0]) or ''))
        elif accounts:
            other.append((address, ', '.join(dict.fromkeys(names.service_name(names.account_service(a)) or '' for a in accounts))))
        elif any(own_addresses.clean(a.get('email')) == address for a in config.get('accounts', [])):
            continue  # one shared with them: read as any other, and neither missing nor theirs
        elif address not in mine and app.search_ask_people(db, address):  # someone else's, with mail of theirs: the person it is about
            plan['person'] = plan.get('person') or address
        else:
            missing.append(address)
    for w in words if not ids else ():
        same = [c['id'] for c in found if c['name'].casefold() == w.casefold()]
        if same:
            ids += same
        elif area and any(a['id'] not in in_view for a in own(config)):
            outside.append(w)
        elif len(found) < LISTED and not _known(config, w):
            missing.append(w)
    ids = list(dict.fromkeys(ids))
    if not (ids or missing or elsewhere or other or outside):
        return None
    by_id = {c['id']: c['name'] for c in found}
    accounts = own_addresses.own_accounts(config)
    called = {a['id']: by_id.get(a['id']) or name(a, accounts) for a in accounts if a.get('id') in ids}
    return {'ids': ids, 'names': [called[i] for i in ids if i in called], 'missing': missing, 'elsewhere': elsewhere, 'other': other, 'outside': outside}


def _at(value):
    try:
        at = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return None
    return at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)


def health(view, account, t, tz):
    """(Connections' words for how this connection is doing, what that means for an answer or ''), from its row
    (Store.connector_views): connectorHealth of dashboard/connections-shared.js, which tests/test_search_ask.py holds
    this against."""
    error, window, at = view.get('error') or '', view.get('read_window') or {}, _at(now())
    again = _at(window.get('reads_again_at'))
    again = again if again and again > at else None
    service = SERVICES.get(names.account_service(account)) or {}
    short = service.get('short') or service.get('name') or ''
    resting = (t('Reads again at {}', again.astimezone(tz).strftime('%H:%M')), 'it only reads in set hours') if again else None
    fix = f'it can not be read until they fix it on that page, {UNREAD}'
    crm = view.get('salesflare') or {}
    if crm.get('stopped'):
        return t('Stopped'), f'they stopped it, {UNREAD}'
    if error.endswith('_signed_out'):
        return f'{t("Signed out of")} {short}', fix
    if error in STOPS:
        return STOPS[error](t), fix
    if error and HELP.search(error):
        return t('Needs your help'), fix
    if error:
        return resting if resting and view.get('last_success') else (t('Reconnecting automatically'), f'reading it fails now and it tries again by itself, {UNREAD}')
    if crm.get('no_access_all') or crm.get('feed_off'):
        return t('Needs your help'), fix
    if not abilities.signals_on(account):
        return t('Connected'), f'“{t("Brings in signals")}” is off for it, so it is not read, {UNREAD}'
    if not view.get('last_success'):
        return t('Waiting for first sync'), 'it was not read yet'
    if resting:
        return resting
    since = max(filter(None, (_at(view['last_success']), _at(window.get('reads_again_at') or window.get('opened_at')))))
    if (at - since).total_seconds() > max(900, (view.get('poll_seconds') or 300) * 3):
        return t('Waiting for a fresh sync'), f'it was not read for a while, {UNREAD}'
    if view.get('service') == 'slack' and (view.get('conversation_errors') or view.get('deferred_threads')):
        return t('Connected · some conversations waiting'), 'some conversations were not read yet'
    failed = view.get('last_failure') or {}
    if (view.get('failures_24h') or 0) >= FLAKY_FAILURES and failed and (at - (_at(failed.get('at')) or at)).total_seconds() < FLAKY_HOURS * 3600:
        slow = re.search(r'HTTP_(429|5\d\d)|network|timeout', failed.get('error') or '', re.I)
        return (t('Connected · {} is slow at times', short) if slow else t('Connected · some syncs fail')), ''
    return t('Connected'), ''


def facts(app, db, got, area, lang, tz):
    """The lines an answer gets about the connections a question is about (resolve)."""
    t = lambda text, *args: i18n.t(text, *args, lang=lang)
    page, out = t('Connections'), []
    by_id = {a['id']: a for a in own(app.config)}
    told = []
    for view in app.store.connector_views(db, [by_id[i] for i in got['ids'] if i in by_id]):
        account = by_id[view['id']]
        words, meaning = health(view, account, t, tz)
        read = f', last read in full {search_ask.local_at(view["last_success"], tz)}' if view.get('last_success') else ''
        side = {'work': t('Work'), 'personal': t('Personal')}.get(graph.account_side(account))
        told.append((not meaning, f'{got["names"][got["ids"].index(view["id"])]}{f" ({side})" if side else ""} is connected, on the page “{page}” it says “{words}”{read}'
                     + (f': {meaning}.' if meaning else '.')))
    told.sort(key=lambda x: x[0])  # what doesn't read well first
    out += [line for _, line in told[:TOLD]]
    for address in got['missing']:
        out.append(f'“{_clean(address)[:80]}” is not connected: none of their connections is it. They can add it on the page “{page}”.')
    for address, kind in got['other']:
        out.append(f'{address} is connected as {kind} only, so its mail is not read. They can add it as a mailbox on the page “{page}”.')
    here = {'work': t('Work'), 'personal': t('Personal')}
    for address, side in got['elsewhere']:
        out.append(f'{address} is connected, and is {here.get(side) or "not in this area"}; only {here.get(area) or page} is in view here. '
                   f'They can ask this with “{here.get(side) or t("All")}” or “{t("All")}” picked.')
    for words in got['outside']:
        out.append(f'“{_clean(words)[:80]}” is none of their {here.get(area, "")} connections, and only those are in view here. '
                   f'They can ask this with “{t("All")}” picked.')
    return out

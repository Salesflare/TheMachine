"""Mail cleanup (docs/help/routines.md, "Templates"): what the Newsletter cleanup and Spam cleanup routines find, the
one to-do each run makes with a choice per item, and what is remembered of the owner's choices.

A run finds the items (newsletters: plain code, from the List-Unsubscribe and List-Id headers, as review_wait.mail_wait
tells them apart; spam: the run's turn picks them from mail by unknown senders) and makes one to-do with them, quietly
(no buzz or push: it waits in the list and the morning summary). No items, no to-do. Spam cleanup runs hourly: while
its to-do for an area still has an item open, a run adds to that to-do instead of making another (open_todo). A receipt, an order or a
payment the review sorted as a notification is no newsletter (notifications). Mail a list relayed (a Google Group like
info@) counts under its original sender and is never unsubscribed through the list (relay_ways).

Nothing changes until the owner picks Keep or Unsubscribe (Not spam or Spam) per item and confirms on the to-do. Then
each item is done with what this Machine may already do, never with more permission (mail_cleanup_app.py):
unsubscribe by the list's one-click link (RFC 8058, an HTTPS POST to a public address) or by its mailto address from
the owner's mailbox when sending is on, else the to-do offers the list's page to open; spam is moved to Junk (Outlook,
Mail.ReadWrite) or labeled spam (Gmail, only with gmail.modify), else the to-do offers to open the mail. A send whose
outcome is unknown is never sent again.

A sender the owner kept (or unsubscribed from, or marked as spam) is never asked about again: mail_cleanup_senders.

Tables (this module owns them): mail_cleanup_items (one row per item of a to-do: its pick and how it went; the
unsubscribe page's link, sealed, while the owner still has to open it) and mail_cleanup_senders."""
import datetime as dt
import json
import re
import urllib.parse

import graph
from machine.store.review_wait import People, mail_wait

KINDS = ('newsletters', 'spam')
MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message')
MAX_ITEMS = 25  # items on one to-do: a phone's screen or two
SPAM_LOOK = 40  # mails by unknown senders a spam run's turn reads, newest first
SYNC_LAG = dt.timedelta(minutes=30)  # mail dated before a run that only synced after it: the next run still reads it
SNIPPET = 160
# An item's state: open (no pick yet), working (being done now), done, kept, yours (the owner finishes it: open the
# list's unsubscribe page), failed (with why), unknown (a send that may have gone out: never sent again)
STATES = ('open', 'working', 'done', 'kept', 'yours', 'failed', 'unknown')
SETTLED = ('done', 'kept', 'yours', 'failed', 'unknown')


def ensure(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS mail_cleanup_items(
        suggestion_id TEXT NOT NULL,item INTEGER NOT NULL,kind TEXT NOT NULL,account_id TEXT NOT NULL,address TEXT NOT NULL,
        choice TEXT,state TEXT NOT NULL DEFAULT 'open',how TEXT,link TEXT,updated_at TEXT NOT NULL,PRIMARY KEY(suggestion_id,item));
      CREATE TABLE IF NOT EXISTS mail_cleanup_senders(
        kind TEXT NOT NULL,address TEXT NOT NULL,choice TEXT NOT NULL,at TEXT NOT NULL,PRIMARY KEY(kind,address));
    ''')


def _rows(db, accounts, since, lag=False):
    """The owner's incoming mail since then, newest first, as (row, metadata). lag: also mail dated up to SYNC_LAG
    before then that first came in after it (the run before could not have seen it), never mail that only changed."""
    if not accounts:
        return []
    marks = ','.join('?' * len(accounts))
    start = (dt.datetime.fromisoformat(since) - SYNC_LAG).isoformat() if lag else since
    out = []
    for r in db.execute(f"SELECT id,account_id,source_id,kind,title,body,metadata,occurred_at,ingested_at,version FROM events WHERE kind IN ({','.join('?' * len(MAIL_KINDS))}) "
                        f"AND account_id IN ({marks}) AND deleted=0 AND occurred_at>=? ORDER BY occurred_at DESC LIMIT 2000",
                        (*MAIL_KINDS, *accounts, start)):
        if r['occurred_at'] < since and not (r['version'] == 1 and str(r['ingested_at'] or '') >= since):
            continue
        m = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        labels = set(m.get('labels') or ())
        if m.get('from_me') or labels & {'SENT', 'DRAFT', 'SPAM', 'TRASH'}:
            continue
        out.append((r, m))
    return out


def sender(m):
    """(display name, address) of a mail's sender, address lowercased; ('', '') when none."""
    found = graph.addresses(m.get('from'))[:1]
    if not found:
        return '', ''
    name, address = found[0]
    return ' '.join(str(name or '').split())[:80], str(address or '').lower()


# --- mail a mailing list relayed (a Google Group like info@, Mailman) ---------------------------------------------------
# A list that relays mail rewrites From to its own address ("'Ann' via info@acme.example readers" <info@acme.example>)
# and adds its own List-Id and List-Unsubscribe. That unsubscribe leaves the list (the owner's, or the team's, info@),
# never the original sender's mailing: it is never used. The original sender is in X-Original-From or
# X-Original-Sender, else in Reply-To.

def _address_of(value):
    found = graph.addresses(value)[:1]
    return (' '.join(str(found[0][0] or '').split())[:80], found[0][1]) if found else ('', '')


def _domain(address):
    return str(address or '').rpartition('@')[2].lower().strip('.')


def relay_of(m):
    """The list address that relayed this mail (its From is the list's own), or ''. m: a mail's metadata, or
    header_meta of its headers."""
    name, address = _address_of(m.get('from'))
    if not address:
        return ''
    _, original = _address_of(m.get('original_from'))
    if original and original != address:
        return address
    # "'Ann' via info@acme.example readers", or "Ann via Info" from the list whose id is its address with a dot (RFC
    # 2919: <info.acme.example>). A list that sends its own mail (an announcement list) has no "via": its unsubscribe is right.
    local, _, domain = address.partition('@')
    own_id = str(m.get('list_id') or '').strip().strip('<>').strip().lower() == f'{local}.{domain}'
    if ' via ' in name.lower() and (f' via {address}' in name.lower() or own_id):
        return address
    return ''


def original_sender(m):
    """(name, address) of who wrote a relayed mail: X-Original-From (or -Sender), else Reply-To when it is someone
    else; the address is '' when the relay kept none."""
    relay = relay_of(m)
    for key in ('original_from', 'reply-to'):
        name, address = _address_of(m.get(key))
        if address and address != relay:
            return name or address, address
    name = _address_of(m.get('from'))[0]
    via = name.lower().find(' via ')
    return (name[:via].strip(' \'"') if via > 0 else name), ''


def header_meta(headers):
    """The keys relay_of and original_sender read, from a mail's headers (lowercased names)."""
    return {'from': headers.get('from', ''), 'reply-to': headers.get('reply-to', ''), 'list_id': headers.get('list-id', ''),
            'original_from': headers.get('x-original-from') or headers.get('x-original-sender') or ''}


def _site(domain):
    """A domain's site: its last two labels, three under a country's second level (shop.example.co.uk: example.co.uk)."""
    labels = [x for x in str(domain or '').lower().split('.') if x]
    keep = 3 if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in ('co', 'com', 'org', 'net', 'ac', 'gov', 'edu') else 2
    return '.'.join(labels[-keep:]) if len(labels) >= 2 else ''


def _under(domain, site):
    return bool(site) and (domain == site or domain.endswith('.' + site))


def relay_ways(ways, original, relay):
    """Of a relayed mail's unsubscribe ways, only those of its original sender: at the original sender's site and not at
    the relay's. With no original address, none: the list's own unsubscribe is never used."""
    theirs, list_site = _site(_domain(original)), _site(_domain(relay))
    out = {}
    for key, way in ways.items():
        target = _domain(way['to']) if key == 'mailto' else (urllib.parse.urlsplit(way).hostname or '').lower()
        if _under(target, theirs) and not _under(target, list_site):
            out[key] = way
    return out


def unsubscribe_ways_of(headers, via=''):
    """unsubscribe_ways from a mail's headers (lowercased names). Mail a list relayed (or an item that came through
    one: via) keeps only its original sender's ways (relay_ways)."""
    ways = unsubscribe_ways(headers.get('list-unsubscribe'), headers.get('list-unsubscribe-post'))
    m = header_meta(headers)
    relay = relay_of(m) or via
    return relay_ways(ways, original_sender(m)[1], relay) if relay else ways


def asked(db, kind):
    """Senders not to ask about: the owner's earlier picks, and those on an item still open on another to-do."""
    out = {r[0] for r in db.execute('SELECT address FROM mail_cleanup_senders WHERE kind=?', (kind,))}
    out |= {r[0] for r in db.execute("SELECT i.address FROM mail_cleanup_items i JOIN suggestions s ON s.id=i.suggestion_id "
                                     "WHERE i.kind=? AND i.state='open' AND s.status NOT IN ('completed','rejected')", (kind,))}
    return out


def _item(r, m, name, address, count=1, via=''):
    return {'account': r['account_id'], 'event': r['id'], 'message': r['source_id'], 'thread': m.get('thread_id') or '',
            'mail': r['kind'], 'from': name or address, 'address': address, 'title': ' '.join(str(r['title'] or '').split())[:120],
            'count': count, **({'via': via} if via else {})}


def notifications(db, since):
    """Event ids the review sorted as notifications since then (finish_analysis read): a receipt, an order summary, an
    invoice, a payment notice, a service's status, judged by what the mail is. Not a newsletter, even with an
    unsubscribe header."""
    found = set()
    for (items,) in db.execute("SELECT items FROM analyses WHERE status='complete' AND started_at>=?", (since,)):
        try:
            found |= {int(i['id']) for i in json.loads(items or '[]') if isinstance(i, dict) and i.get('read') == 'notifications'}
        except (TypeError, ValueError, KeyError):
            continue
    return found


def newsletters(db, accounts, since):
    """Newsletters and list mail since then, one item per sender (its newest mail, with how many came), newest first.
    A newsletter is what review_wait.mail_wait calls 'list' (List-Unsubscribe or List-Id), never someone the owner
    knows and never what the review sorted as a notification (a receipt, an order or a payment); senders asked before
    are left out. Mail a list relayed (a Google Group) counts under its original sender, with the list as via; when
    the list kept no original address there is nothing to unsubscribe from but the list, and it is left out."""
    people, skip, found, receipts = People(db), asked(db, 'newsletters'), {}, notifications(db, since)
    for r, m in _rows(db, accounts, since):
        name, address = sender(m)
        if not address or r['id'] in receipts or mail_wait(m, r['title'] or '', people) != 'list':
            continue
        via = relay_of(m)
        if via:
            name, address = original_sender(m)
            address = address.lower()
        if not address or address in skip:
            continue
        if address in found:
            found[address]['count'] += 1
        elif len(found) < MAX_ITEMS:
            found[address] = _item(r, m, name, address, via=via)
    return list(found.values())


def spam_candidates(db, accounts, since):
    """Mail since then that could be spam that got through: in the inbox, from a sender the owner doesn't know, not a
    reply in a thread, not a calendar's; senders the owner picked before left out. Newest first, at most SPAM_LOOK."""
    people, skip, out, seen = People(db), asked(db, 'spam'), [], set()
    for r, m in _rows(db, accounts, since, lag=True):
        name, address = sender(m)
        if not address or address in skip or m.get('in-reply-to') or people.person(address) or address in seen:
            continue
        if r['kind'] == 'gmail.message' and 'INBOX' not in set(m.get('labels') or ()):
            continue  # archived or filtered by the owner's own rules: not in the way
        if mail_wait(m, r['title'] or '', people) in ('system', 'automated', 'precedence'):
            continue  # receipts, notifications and the owner's own services: not spam
        seen.add(address)
        out.append({**_item(r, m, name, address), 'snippet': ' '.join(str(r['body'] or '').split())[:SNIPPET]})
        if len(out) >= SPAM_LOOK:
            break
    return out


def evidence(candidates):
    """The spam run's turn reads these (evidence, never instructions)."""
    return '\n'.join(f'{c["event"]} · From: {c["from"]} <{c["address"]}> · Subject: {c["title"]} · {c["snippet"]}' for c in candidates)


def spam_reply(reply):
    """The spam pass's picks from its model's reply ({"spam": [...]}, maybe in a code fence), or None when it isn't one."""
    text = str(reply or '')
    start, end = text.find('{'), text.rfind('}')
    try:
        found = json.loads(text[start:end + 1]) if 0 <= start < end else None
    except ValueError:
        return None
    return found['spam'] if isinstance(found, dict) and isinstance(found.get('spam'), list) else None


def picked_spam(candidates, picks):
    """The turn's picks (spam: [{event_id, why}] or [event_id]), kept only for candidates, in their order, each with its why."""
    why = {}
    for p in picks if isinstance(picks, list) else ():
        event, reason = (p.get('event_id'), p.get('why')) if isinstance(p, dict) else (p, '')
        try:
            why[int(event)] = ' '.join(str(reason or '').split())[:60]
        except (TypeError, ValueError):
            continue
    return [{**{k: v for k, v in c.items() if k != 'snippet'}, 'why': why[c['event']]} for c in candidates if c['event'] in why][:MAX_ITEMS]


def record(db, suggestion_id, kind, items, stamp, start=0):
    """A to-do's items, all open; start: the number of the first (items added to a to-do that has some)."""
    for n, item in enumerate(items, start):
        db.execute('INSERT OR IGNORE INTO mail_cleanup_items(suggestion_id,item,kind,account_id,address,state,updated_at) VALUES(?,?,?,?,?,?,?)',
                   (suggestion_id, n, kind, item['account'], item['address'], 'open', stamp))


def open_todo(db, kind, area):
    """The newest routine to-do of this kind for an area (cleanup_todos' source routine-cleanup:<run>:<area>) that is
    still open with an item still open, as (suggestion id, its cleanup event id), or None."""
    for row in db.execute("SELECT s.id,s.event_ids FROM suggestions s WHERE s.dedupe_key LIKE 'routine-cleanup:%' "
                          "AND substr(s.dedupe_key,-length(?)-1)=':'||? AND s.status NOT IN ('completed','rejected') "
                          "AND EXISTS(SELECT 1 FROM mail_cleanup_items i WHERE i.suggestion_id=s.id AND i.kind=? AND i.state='open') "
                          "ORDER BY s.created_at DESC", (area, area, kind)):
        for event in json.loads(row['event_ids'] or '[]'):
            meta = db.execute("SELECT metadata FROM events WHERE id=? AND kind='routine.cleanup'", (event,)).fetchone()
            if meta and json.loads(meta[0] or '{}').get('cleanup') == kind:
                return row['id'], event
    return None


def items_of(db, suggestion_id):
    """{item: row} of a to-do's items; {} for any other to-do."""
    try:
        return {r['item']: dict(r) for r in db.execute('SELECT * FROM mail_cleanup_items WHERE suggestion_id=?', (suggestion_id,))}
    except Exception:  # a database before this table
        return {}


def is_cleanup(db, suggestion_id):
    return bool(items_of(db, suggestion_id))


def pick(db, suggestion_id, picks, stamp):
    """The owner's confirmed picks ({item: 'keep' or 'go'}): kept ones are settled and their sender remembered; the
    ones to do turn 'working'. Only open items change. Returns the item numbers to do."""
    have, todo = items_of(db, suggestion_id), []
    if not have:
        raise ValueError('That to-do is gone')
    for key, choice in (picks or {}).items():
        try:
            n = int(key)
        except (TypeError, ValueError):
            continue
        row = have.get(n)
        if not row or row['state'] != 'open' or choice not in ('keep', 'go'):
            continue
        if choice == 'keep':
            db.execute("UPDATE mail_cleanup_items SET choice='keep',state='kept',updated_at=? WHERE suggestion_id=? AND item=?", (stamp, suggestion_id, n))
            remember(db, row['kind'], row['address'], 'keep', stamp)
        else:
            db.execute("UPDATE mail_cleanup_items SET choice='go',state='working',updated_at=? WHERE suggestion_id=? AND item=?", (stamp, suggestion_id, n))
            todo.append(n)
    return todo


def settle(db, suggestion_id, n, state, stamp, how=None, link=None):
    """How one item went: done (how: one_click, mailto, junk, spam), yours (link: the unsubscribe page to open), failed,
    unknown. A done or yours item's sender is not asked about again."""
    state = state if state in SETTLED else 'failed'
    db.execute("UPDATE mail_cleanup_items SET state=?,how=?,link=?,updated_at=? WHERE suggestion_id=? AND item=? AND state='working'",
               (state, how, link, stamp, suggestion_id, n))
    row = db.execute('SELECT kind,address FROM mail_cleanup_items WHERE suggestion_id=? AND item=?', (suggestion_id, n)).fetchone()
    if row and state in ('done', 'yours', 'unknown'):
        remember(db, row['kind'], row['address'], 'gone', stamp)


def remember(db, kind, address, choice, stamp):
    db.execute('INSERT OR REPLACE INTO mail_cleanup_senders(kind,address,choice,at) VALUES(?,?,?,?)', (kind, address, choice, stamp))


def all_settled(db, suggestion_id):
    """Every item is settled and none waits for the owner's own step (yours)."""
    states = {r['state'] for r in items_of(db, suggestion_id).values()}
    return bool(states) and states <= {'done', 'kept', 'failed', 'unknown'}


def view(db, suggestion_id, metas):
    """What a to-do shows of its items, or None: {'kind', 'items': [{n, from, address, title, count, why, state, how,
    link}]}. metas: the to-do's evidence metadata, as stored (the items' details are sealed with it)."""
    have = items_of(db, suggestion_id)
    if not have:
        return None
    for meta in metas:
        try:
            m = meta if isinstance(meta, dict) else json.loads(meta or '{}')
        except (TypeError, ValueError):
            continue
        if not isinstance(m, dict) or m.get('cleanup') not in KINDS:
            continue
        items = []
        for n, item in enumerate(m.get('items') or ()):
            row = have.get(n)
            if not row:
                continue
            items.append({'n': n, 'from': item.get('from') or '', 'address': item.get('address') or '', 'title': item.get('title') or '',
                          'count': item.get('count') or 1, 'why': item.get('why') or '', 'state': row['state'], 'how': row['how'],
                          'plan': item.get('how'),  # what the pick will do, read when the run made it (mail_cleanup_app.py)
                          'link': row['link'] if row['state'] == 'yours' else None})
        return {'kind': m['cleanup'], 'items': items}
    return None


def details(metas, n):
    """One item's details from the to-do's evidence (account, message, thread, mail kind, url), or None."""
    for meta in metas:
        m = meta if isinstance(meta, dict) else json.loads(meta or '{}')
        if isinstance(m, dict) and m.get('cleanup') in KINDS:
            items = m.get('items') or []
            return items[n] if 0 <= n < len(items) else None
    return None


# --- the List-Unsubscribe header (RFC 2369, RFC 8058) -------------------------------------------------------------------

_TARGET = re.compile(r'<([^<>\s]+)>')


def unsubscribe_ways(header, post=''):
    """{'one_click': https URL (only with List-Unsubscribe-Post: List-Unsubscribe=One-Click), 'mailto': {to, subject,
    body}, 'link': an https page} from a List-Unsubscribe header, each only when it is there and well formed."""
    out = {}
    one_click = 'list-unsubscribe=one-click' in ' '.join(str(post or '').lower().split())
    for target in _TARGET.findall(str(header or ''))[:4]:
        parts = urllib.parse.urlsplit(target)
        if parts.scheme == 'https' and parts.hostname and not parts.username and not parts.password and len(target) <= 2000:
            out.setdefault('link', target)
            if one_click:
                out.setdefault('one_click', target)
        elif parts.scheme == 'mailto' and 'mailto' not in out:
            address = urllib.parse.unquote(parts.path)
            if re.fullmatch(r'[^@\s,;<>]+@[^@\s,;<>]+\.[^@\s,;<>]+', address):
                q = urllib.parse.parse_qs(parts.query)
                out['mailto'] = {'to': address[:200], 'subject': ' '.join((q.get('subject') or ['unsubscribe'])[0].split())[:120] or 'unsubscribe',
                                 'body': (q.get('body') or ['unsubscribe'])[0][:500] or 'unsubscribe'}
    return out

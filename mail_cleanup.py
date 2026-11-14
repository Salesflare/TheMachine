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
the owner's mailbox when sending is on, else on the list's page in this Machine's own browser (unsubscribe_page.py),
else the to-do offers that page to open, with why; spam is moved to Junk (Outlook,
Mail.ReadWrite) or labeled spam (Gmail, only with gmail.modify), else the to-do offers to open the mail. A send whose
outcome is unknown is never sent again.

A sender the owner kept (or unsubscribed from) is never asked about again: mail_cleanup_senders. Spam is the other way
round. Who the owner never wrote to is unknown, even when the Graph has them from mail they sent (known_senders), and a
reply counts as a conversation only in a thread the owner wrote in: a made-up "Re:" from a stranger is still read. A
sender the owner said Spam about, on the to-do or by moving their mail to spam themselves (learn_marks: mail that went
to spam after it came in), is remembered as such: their next mail that gets through is on the to-do without a model, and
the owner's newest own marks go with the spam pass as examples of what they call spam (marked_examples). Not spam on a
later to-do wins.

Tables (this module owns them): mail_cleanup_items (one row per item of a to-do: its pick and how it went; the
unsubscribe page's link, sealed, while the owner still has to open it) and mail_cleanup_senders."""
import datetime as dt
import html
import json
import re
import urllib.parse

import graph
import i18n
from machine.cards import group_sender
from machine.sources.gmail import phone_link
from machine.store.review_wait import People, mail_wait

KINDS = ('newsletters', 'spam')
MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message')
MAX_ITEMS = 25  # items on one to-do: a phone's screen or two
SPAM_LOOK = 40  # mails by unknown senders a spam run's turn reads, newest first
SYNC_LAG = dt.timedelta(minutes=30)  # mail dated before a run that only synced after it: the next run still reads it
SNIPPET = 120  # the start of a mail's text the spam pass reads: enough to tell a pitch, short enough to stay cheap
MARKS_DAYS = 30  # how far back the owner's own spam marks are read
EXAMPLES = 6  # the owner's newest own spam marks the spam pass sees as examples
EXAMPLE_TITLE = 70
SPAM_SENDERS = ('gone', 'marked')  # mail_cleanup_senders choices that say spam: Spam on a to-do, or the owner's own mark
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
# X-Original-Sender, else in Reply-To. A list often keeps the sender's From (when the sender's domain lets it): then
# only its headers tell: its List-Id is the address it came to (<info.acme.example> on mail to info@acme.example), a
# Google Group's X-Google-Group-Id or Mailing-list, Mailman's X-Mailman-Version, or a Sender that is the list.
# Whatever a mail says, an unsubscribe at a group service (GROUP_HOSTS) or at the owner's own domains is never used.

# Where a group's or a team list's own unsubscribe lives (Google Groups, Microsoft 365 groups, groups.io): never a
# newsletter's own
GROUP_HOSTS = ('googlegroups.com', 'groups.google.com', 'groups.io', 'outlook.office365.com', 'outlook.office.com')


def _address_of(value):
    found = graph.addresses(value)[:1]
    return (' '.join(str(found[0][0] or '').split())[:80], found[0][1]) if found else ('', '')


def _domain(address):
    return str(address or '').rpartition('@')[2].lower().strip('.')


def _list_id(m):
    """A List-Id's id, lowercased, without its phrase and brackets: 'Info <info.acme.example>' reads info.acme.example."""
    text = str(m.get('list_id') or '')
    found = re.search(r'<([^<>]+)>', text)
    return (found.group(1) if found else text).strip().lower()


def relay_of(m, own=()):
    """The list address that relayed this mail, or ''. m: a mail's metadata, or header_meta of its headers. own: the
    owner's own sites (own_sites): a list there is their team's."""
    name, address = _address_of(m.get('from'))
    if not address:
        return ''
    _, original = _address_of(m.get('original_from'))
    if original and original != address:
        return address
    # "'Ann' via info@acme.example readers", or "Ann via Info" from the list whose id is its address with a dot (RFC
    # 2919: <info.acme.example>). A list that sends its own mail (an announcement list) has no "via": its unsubscribe is right.
    local, _, domain = address.partition('@')
    list_id = _list_id(m)
    if ' via ' in name.lower() and (f' via {address}' in name.lower() or list_id == f'{local}.{domain}'):
        return address
    # the sender's From kept: the list it came through, from its headers
    recipients = [a for _, a in graph.addresses(', '.join(str(m.get(k) or '') for k in ('to', 'cc')))]
    for to in recipients:
        to_local, _, to_domain = to.partition('@')
        if to != address and list_id == f'{to_local}.{to_domain}':
            return to
    _, sender = _address_of(m.get('sender'))
    if sender and sender != address and (m.get('list_id') or m.get('list_unsubscribe')) and \
            (sender in recipients or any(_under(_domain(sender), site) for site in own)):
        return sender
    _, listed = _address_of(str(m.get('mailing_list') or '').partition(';')[0].removeprefix('list '))
    marked = m.get('google_group') or m.get('mailing_list') or m.get('mailman') or \
        any(_under(list_id, site) for site in GROUP_HOSTS) or any(_under(list_id, site) for site in own)
    if marked:
        return (listed if listed and listed != address else '') or (sender if sender and sender != address else '') or \
            (list_id if list_id and not _under(list_id, _site(domain)) else '') or 'list.invalid'
    return ''


def original_sender(m, own=()):
    """(name, address) of who wrote a relayed mail: X-Original-From (or -Sender), else Reply-To when it is someone
    else, else From when the list kept it; the address is '' when the relay kept none."""
    relay = relay_of(m, own)
    name, address = _address_of(m.get('from'))
    if address and address != relay:  # the list kept the sender's From
        return name or address, address
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
            'original_from': headers.get('x-original-from') or headers.get('x-original-sender') or '',
            'to': headers.get('to', ''), 'cc': headers.get('cc', ''), 'sender': headers.get('sender', ''),
            'list_unsubscribe': bool(str(headers.get('list-unsubscribe') or '').strip()),
            'google_group': str(headers.get('x-google-group-id') or '').strip(),
            'mailing_list': ' '.join(str(headers.get('mailing-list') or '').split())[:200],
            'mailman': str(headers.get('x-mailman-version') or '').strip()}


def own_sites(db, config):
    """The sites of the owner's own domains (their mailboxes' and the company domains they added): mail a list there
    relayed is their team's, and nothing there is ever unsubscribed from."""
    import own_addresses
    domains = set()
    try:
        domains = own_addresses.detected_domains(db, config) | own_addresses.domains(db)
    except Exception:  # a read-only or locked database: at least the mailboxes' own
        domains = {own_addresses.email_domain(a.get('email')) for a in own_addresses.own_accounts(config)} - {''} - graph.FREEMAIL
    return {_site(d) for d in domains} - {''}


def _site(domain):
    """A domain's site: its last two labels, three under a country's second level (shop.example.co.uk: example.co.uk)."""
    labels = [x for x in str(domain or '').lower().split('.') if x]
    keep = 3 if len(labels) >= 3 and len(labels[-1]) == 2 and labels[-2] in ('co', 'com', 'org', 'net', 'ac', 'gov', 'edu') else 2
    return '.'.join(labels[-keep:]) if len(labels) >= 2 else ''


def _under(domain, site):
    return bool(site) and (domain == site or domain.endswith('.' + site))


def _target(key, way):
    return _domain(way['to']) if key == 'mailto' else (urllib.parse.urlsplit(way).hostname or '').lower()


def safe_ways(ways, own=()):
    """Never a group service's unsubscribe (GROUP_HOSTS), and never one at the owner's own sites: that would take the
    owner, or the team, off their own list."""
    return {key: way for key, way in ways.items()
            if not any(_under(_target(key, way), site) for site in (*GROUP_HOSTS, *own))}


def relay_ways(ways, original, relay, own=()):
    """Of a relayed mail's unsubscribe ways, only those of its original sender: at the original sender's site and not at
    the relay's. With no original address, none: the list's own unsubscribe is never used."""
    theirs, list_site = _site(_domain(original)), _site(_domain(relay))
    out = {}
    for key, way in safe_ways(ways, own).items():
        target = _target(key, way)
        if _under(target, theirs) and not _under(target, list_site):
            out[key] = way
    return out


# An unsubscribe link in a mail's text, in the languages the app speaks: its words or its address say so
_UNSUB_WORDS = re.compile(r'unsub|opt[\s_-]?out|afmeld|uitschrijv|d[ée]sinscri|d[ée]sabonn|abmeld|abbestell|darse de baja|'
                          r'disiscri|cancelar (?:a )?(?:subscri|inscri)|descadastr', re.I)
_LINK = re.compile(r'<a\b[^>]*?\bhref\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)


def body_link(text, original, relay, own=()):
    """The original sender's own unsubscribe page from a relayed mail's HTML: an https link that says unsubscribe, at the
    original sender's site and never at the relay's, a group service's or the owner's own (a list's footer has its own
    leave link). '' when there is none."""
    theirs, list_site = _site(_domain(original)), _site(_domain(relay))
    for href, label in _LINK.findall(str(text or '')[:500_000]):
        href = html.unescape(href).strip()
        parts = urllib.parse.urlsplit(href)
        host = (parts.hostname or '').lower()
        words = re.sub(r'<[^>]+>', ' ', html.unescape(label)) + ' ' + parts.path + ' ' + parts.query
        if (parts.scheme == 'https' and host and not parts.username and not parts.password and len(href) <= 2000
                and _UNSUB_WORDS.search(words) and _under(host, theirs) and not _under(host, list_site)
                and not any(_under(host, site) for site in (*GROUP_HOSTS, *own))):
            return href
    return ''


def unsubscribe_ways_of(headers, via='', own=()):
    """unsubscribe_ways from a mail's headers (lowercased names), never a group's or one at the owner's own sites
    (safe_ways). Mail a list relayed (or an item that came through one: via) keeps only its original sender's ways
    (relay_ways)."""
    ways = safe_ways(unsubscribe_ways(headers.get('list-unsubscribe'), headers.get('list-unsubscribe-post')), own)
    m = header_meta(headers)
    relay = relay_of(m, own) or via
    return relay_ways(ways, original_sender(m, own)[1], relay, own) if relay else ways


def asked(db, kind):
    """Senders not to ask about: the owner's earlier picks (spam: only Not spam), and those on an item still open on
    another to-do."""
    out = {r[0] for r in db.execute('SELECT address FROM mail_cleanup_senders WHERE kind=?' + (" AND choice='keep'" if kind == 'spam' else ''), (kind,))}
    out |= {r[0] for r in db.execute("SELECT i.address FROM mail_cleanup_items i JOIN suggestions s ON s.id=i.suggestion_id "
                                     "WHERE i.kind=? AND i.state='open' AND s.status NOT IN ('completed','rejected')", (kind,))}
    return out


def _item(r, m, name, address, count=1, via=''):
    # a Google Group's "'Ann' via Sales" as people say it: Ann via Sales
    return {'account': r['account_id'], 'event': r['id'], 'message': r['source_id'], 'thread': m.get('thread_id') or '',
            'mail': r['kind'], 'from': group_sender(name) or address, 'address': address, 'title': ' '.join(str(r['title'] or '').split())[:120],
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


def newsletters(db, accounts, since, own=()):
    """Newsletters and list mail since then, one item per sender (its newest mail, with how many came), newest first.
    A newsletter is what review_wait.mail_wait calls 'list' (List-Unsubscribe or List-Id), never someone the owner
    knows and never what the review sorted as a notification (a receipt, an order or a payment); senders asked before
    are left out. Mail a list relayed (a Google Group) counts under its original sender, with the list as via; when
    the list kept no original address there is nothing to unsubscribe from but the list, and it is left out. own: the
    owner's own sites (own_sites)."""
    found = {}
    for r, m, name, address, via in _newsletter_mail(db, accounts, since, own):
        if address in found:
            found[address]['count'] += 1
        elif len(found) < MAX_ITEMS:
            found[address] = _item(r, m, name, address, via=via)
    return list(found.values())


def _newsletter_mail(db, accounts, since, own=()):
    """Each newsletter mail since then, newest first, as (row, metadata, name, address, via): newsletters' own test."""
    people, skip, receipts = People(db), asked(db, 'newsletters'), notifications(db, since)
    for r, m in _rows(db, accounts, since):
        name, address = sender(m)
        if not address or r['id'] in receipts or mail_wait(m, r['title'] or '', people) != 'list':
            continue
        via = relay_of(m, own)
        if via:
            name, address = original_sender(m, own)
            address = address.lower()
        if address and address not in skip:
            yield r, m, name, address, via


def newsletter_count(db, accounts, since):
    """How many newsletters came since then, and from how many senders: what Newsletter cleanup would list, counted
    (routine_offers.py). Plain code, no model."""
    senders, n = set(), 0
    for _, _, _, address, _ in _newsletter_mail(db, accounts, since):
        senders.add(address)
        n += 1
    return n, len(senders)


_BY_OWNER = "(json_extract({0}.metadata,'$.from_me') IN (1,'true') OR instr(json_extract({0}.metadata,'$.labels'),'\"SENT\"')>0)"


class Known:
    """Who the owner wrote to and the threads they wrote in, read once per run. Getting mail from someone, or the Graph
    having them from it, is not knowing them: only a message the owner sent to them (any channel, on their person in the
    Graph), or the owner saying the sender is a person (mail_shown)."""

    def __init__(self, db):
        self.db, self.cache = db, {}

    def _one(self, key, sql, args):
        if key not in self.cache:
            try:
                self.cache[key] = bool(self.db.execute(sql, args).fetchone())
            except Exception:  # a table this database doesn't have yet
                self.cache[key] = False
        return self.cache[key]

    def wrote_to(self, address):
        identifier = 'email:' + address
        return self._one(('to', address), 'SELECT 1 FROM graph_identifiers i JOIN graph_events g ON g.node_id=i.node_id JOIN events e '
                         f'ON e.id=g.event_id WHERE i.identifier=? AND e.deleted=0 AND {_BY_OWNER.format("e")} LIMIT 1', (identifier,)) \
            or self._one(('shown', address), 'SELECT 1 FROM mail_shown WHERE identifier=? LIMIT 1', (identifier,))

    def wrote_in(self, account, thread):
        """The owner sent mail in this thread: a reply in it is a conversation."""
        return bool(thread) and self._one(('in', account, thread), f"SELECT 1 FROM events e WHERE e.account_id=? AND e.kind IN ({','.join('?' * len(MAIL_KINDS))}) "
                                          f"AND e.deleted=0 AND json_extract(e.metadata,'$.thread_id')=? AND {_BY_OWNER.format('e')} LIMIT 1",
                                          (account, *MAIL_KINDS, thread))


def known_senders(db, addresses):
    """Of these addresses, the ones the owner wrote to (Known.wrote_to)."""
    known = Known(db)
    return {a for a in addresses if known.wrote_to(a)}


def _marked_rows(db, accounts, days=MARKS_DAYS):
    """The owner's own spam marks of the past days: their mail that went to spam after it came in (labels SPAM,
    changed since its first sync), newest first."""
    if not accounts:
        return []
    start = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()
    rows = db.execute(f"SELECT id,account_id,kind,title,metadata,ingested_at FROM events WHERE kind IN ({','.join('?' * len(MAIL_KINDS))}) "
                      f"AND account_id IN ({','.join('?' * len(accounts))}) AND deleted=0 AND occurred_at>=? AND version>1 "
                      "AND instr(json_extract(metadata,'$.labels'),'\"SPAM\"')>0 ORDER BY ingested_at DESC LIMIT 500",
                      (*MAIL_KINDS, *accounts, start))
    out = []
    for r in rows:
        m = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        if not m.get('from_me') and 'SENT' not in set(m.get('labels') or ()):
            out.append((r, m))
    return out


def learn_marks(db, accounts, stamp):
    """Remember the senders of the owner's own spam marks (mail_cleanup_senders 'marked'), never someone the owner wrote
    to. A newer pick wins either way: Not spam on a later to-do, or a mark after an earlier Not spam. Plain code, each
    run; returns how many were new."""
    rows = _marked_rows(db, accounts)
    known, n = Known(db), 0
    for r, m in reversed(rows):  # oldest first: the newest mark is the one kept
        _, address = sender(m)
        if not address or known.wrote_to(address):
            continue
        n += db.execute("INSERT INTO mail_cleanup_senders(kind,address,choice,at) VALUES('spam',?,'marked',?) "
                        "ON CONFLICT(kind,address) DO UPDATE SET choice='marked',at=excluded.at WHERE excluded.at>mail_cleanup_senders.at "
                        "AND mail_cleanup_senders.choice!='marked'", (address, r['ingested_at'] or stamp)).rowcount
    return n


def marks_count(db, accounts, days):
    """How many mails the owner moved to spam themselves in the past days (_marked_rows), never counting mail from
    someone they wrote to (routine_offers.py). Plain code, no model."""
    known = Known(db)
    return sum(1 for _, m in _marked_rows(db, accounts, days) if (address := sender(m)[1]) and not known.wrote_to(address))


def marked_examples(db, accounts):
    """The owner's newest own spam marks, as examples for the spam pass: subject and the sender's domain only, never
    mail from someone the owner wrote to."""
    out, known = [], Known(db)
    for r, m in _marked_rows(db, accounts):
        _, address = sender(m)
        if not address or known.wrote_to(address):
            continue
        line = f'{" ".join(str(r["title"] or "").split())[:EXAMPLE_TITLE]} · {address.rpartition("@")[2]}'
        if line not in out:
            out.append(line)
        if len(out) >= EXAMPLES:
            break
    return out


def spam_candidates(db, accounts, since):
    """Mail since then that could be spam that got through: in the inbox, from a sender the owner never wrote to, not a
    reply in a thread the owner wrote in, not a calendar's; senders the owner said Not spam about left out. A sender the
    owner said Spam about before is marked (spammed): it goes on the to-do without the model. Newest first, at most
    SPAM_LOOK."""
    known, skip, out, seen = Known(db), asked(db, 'spam'), [], set()
    spammed = {r[0] for r in db.execute(f"SELECT address FROM mail_cleanup_senders WHERE kind='spam' AND choice IN ({','.join('?' * len(SPAM_SENDERS))})", SPAM_SENDERS)}
    for r, m in _rows(db, accounts, since, lag=True):
        name, address = sender(m)
        if not address or address in skip or address in seen:
            continue
        reply = bool(m.get('in-reply-to'))
        if (reply and known.wrote_in(r['account_id'], m.get('thread_id'))) or known.wrote_to(address):
            continue  # a conversation the owner is in, or someone they wrote to
        if r['kind'] == 'gmail.message' and 'INBOX' not in set(m.get('labels') or ()):
            continue  # archived or filtered by the owner's own rules: not in the way
        if mail_wait({k: v for k, v in m.items() if k != 'in-reply-to'}, r['title'] or '', None) in ('system', 'automated', 'precedence'):
            continue  # receipts, notifications and the owner's own services: not spam
        seen.add(address)
        out.append({**_item(r, m, name, address), 'snippet': ' '.join(str(r['body'] or '').split())[:SNIPPET],
                    **({'reply': True} if reply else {}), **({'spammed': True} if address in spammed else {})})
        if len(out) >= SPAM_LOOK:
            break
    return out


def for_model(candidates):
    """The candidates the spam pass's model reads: all but senders the owner said Spam about before."""
    return [c for c in candidates if not c.get('spammed')]


def evidence(candidates, examples=()):
    """The spam pass reads these (evidence, never instructions): the mail it may pick from, and the owner's own newest
    marks as examples."""
    lines = [f'{c["event"]} · {c["from"]} <{c["address"]}> · {c["title"]} · {c["snippet"]}' + (' · Re: without the owner' if c.get('reply') else '')
             for c in for_model(candidates)]
    if examples:
        lines += ['', 'Examples the owner moved to spam lately (subject · domain):', *examples]
    return '\n'.join(lines)


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
    """The turn's picks (spam: [{event_id, why}] or [event_id]), kept only for candidates, in their order, each with its
    why; a sender the owner said Spam about before is on it without a pick."""
    why = {c['event']: i18n.t('Marked as spam before') for c in candidates if c.get('spammed')}
    for p in picks if isinstance(picks, list) else ():
        event, reason = (p.get('event_id'), p.get('why')) if isinstance(p, dict) else (p, '')
        try:
            why.setdefault(int(event), ' '.join(str(reason or '').split())[:60])
        except (TypeError, ValueError):
            continue
    return [{**{k: v for k, v in c.items() if k != 'snippet'}, 'why': why[c['event']]} for c in candidates if c['event'] in why][:MAX_ITEMS]


def record(db, suggestion_id, kind, items, stamp, start=0):
    """A to-do's items, open; start: the number of the first (items added to a to-do that has some). A newsletter that
    came through a group with no way of its sender's own (how: hand) is the owner's from the start: its row says so,
    with no pick (yours, how: group), and its sender is not asked about again."""
    for n, item in enumerate(items, start):
        hand = item.get('how') == 'hand'
        db.execute('INSERT OR IGNORE INTO mail_cleanup_items(suggestion_id,item,kind,account_id,address,state,how,updated_at) VALUES(?,?,?,?,?,?,?,?)',
                   (suggestion_id, n, kind, item['account'], item['address'], 'yours' if hand else 'open', 'group' if hand else None, stamp))
        if hand:
            remember(db, kind, item['address'], 'gone', stamp)


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
    """How one item went: done (how: one_click, mailto, page, junk, spam), yours (link: the unsubscribe page to open;
    how: why the Machine left it, unsubscribe_page.REASONS, or page from before), failed, unknown. A done or yours item's sender is not asked about again."""
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


def view(db, suggestion_id, metas, have=None):
    """What a to-do shows of its items, or None: {'kind', 'items': [{n, from, address, title, event, count, why, state,
    how, link}]}; event: its mail's id while that mail is kept, else None. metas: the to-do's evidence metadata, as stored (the items' details are sealed with it).
    have: its items_of, read once for a list of to-dos (views.card_reads)."""
    have = items_of(db, suggestion_id) if have is None else have
    if not have:
        return None
    for meta in metas:
        try:
            m = meta if isinstance(meta, dict) else json.loads(meta or '{}')
        except (TypeError, ValueError):
            continue
        if not isinstance(m, dict) or m.get('cleanup') not in KINDS:
            continue
        items, kept = [], _kept(db, [i.get('event') for i in m.get('items') or () if isinstance(i, dict)])
        for n, item in enumerate(m.get('items') or ()):
            row = have.get(n)
            if not row:
                continue
            items.append({'n': n, 'from': item.get('from') or '', 'address': item.get('address') or '', 'title': item.get('title') or '',
                          'event': item.get('event') if item.get('event') in kept else None,  # its mail, to read in the viewer while still kept
                          'count': item.get('count') or 1, 'why': item.get('why') or '', 'state': row['state'], 'how': row['how'],
                          'plan': item.get('how'),  # what the pick will do, read when the run made it (mail_cleanup_app.py)
                          'link': row['link'] if row['state'] == 'yours' else None,
                          **({'phone_link': phone} if row['state'] == 'yours' and (phone := phone_link(row['link'], item.get('thread'))) else {})})
        return {'kind': m['cleanup'], 'items': items}
    return None


def _kept(db, events):
    """The ones of these event ids still kept (not deleted): an item's mail opens only while it is."""
    ids = [e for e in events if isinstance(e, int) and not isinstance(e, bool)]
    if not ids:
        return set()
    return {r[0] for r in db.execute(f"SELECT id FROM events WHERE id IN ({','.join('?' * len(ids))}) AND deleted=0", ids)}


def details(metas, n):
    """One item's details from the to-do's evidence (account, message, thread, mail kind, url), or None."""
    for meta in metas:
        m = meta if isinstance(meta, dict) else json.loads(meta or '{}')
        if isinstance(m, dict) and m.get('cleanup') in KINDS:
            items = m.get('items') or []
            return items[n] if 0 <= n < len(items) else None
    return None


_MESSAGE_ID = re.compile(r'[A-Za-z0-9_-]{1,64}')


def mail_link(account, item):
    """A Gmail item's mail in Gmail on the web, in the account it came to (Spam where this Machine may not move mail to
    spam: the owner marks it there), or None (Outlook, or no message id of Gmail's shape)."""
    message = str(item.get('message') or '')
    if item.get('mail') != 'gmail.message' or (account.get('service') or 'gmail') != 'gmail' or not account.get('email') \
            or not _MESSAGE_ID.fullmatch(message):
        return None
    return 'https://mail.google.com/mail/u/?authuser=' + urllib.parse.quote(account['email']) + '#all/' + message


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

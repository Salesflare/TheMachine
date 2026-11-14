"""Lookalike senders: an address whose domain imitates one the owner already deals with (docs/intelligence.md,
Lookalike senders).

Two domains are confusable when, beyond the ending (.com, .co.uk), their names read the same once hyphens and the
letters people mix up are folded (kestrel-bikes for kestrelbikes, larkspurstudlo for larkspurstudio), when a long
name is one letter apart (fjordlinefreigth), or when one is the other's whole name plus a word (quillpress-payments,
larkspurstudio-mail). The same name at another ending (example.nl for example.com) is the organization's other domain,
never a lookalike. Free mail domains never count: everyone there is someone else.

Of a confusable pair, the lookalike is the one that showed up later; the owner's own domains always come first. The
Graph build marks each person at a lookalike domain (`lookalike` on their node: the domain it imitates, and the
person on record there with the same name, when there is one). What follows from it:

- a review never gives them a role (graph.set_role), and a role a review gave them before is not shown;
- "Same person?" never pairs two people whose domains are confusable, and a shared name never joins them;
- a prepared email to a lookalike address is checked before it is saved: it goes to the address on record instead
  (problems, from the Do it prepare step);
- a to-do about their message says that it isn't who it seems (graph.card_people, the dashboard).

The owner's own word is never overruled: they can still set a role, merge two people or send to any address."""
from __future__ import annotations

import collections
import datetime as dt
import json
import re

# Letters and pairs people read as one another, folded before names are compared
GLYPHS = (('rn', 'm'), ('vv', 'w'), ('0', 'o'), ('1', 'l'), ('i', 'l'), ('|', 'l'), ('5', 's'), ('3', 'e'))
EDIT_MIN = 6  # one letter apart counts from this length: shorter names that close are often just other companies
WORD_MIN = 5  # the whole name inside another's, plus a word, counts from this length (acme-corp is no lookalike of acme)
SECOND_LEVEL = {'co', 'com', 'org', 'net', 'ac', 'gov', 'edu'}  # example.co.uk keeps three parts (as enrichment.registrable)


def registrable(domain):
    """The organization's own domain of an address's domain: mail.example.com is example.com."""
    labels = str(domain or '').strip().strip('.').lower().rsplit('@', 1)[-1].split('.')
    keep = 3 if len(labels) >= 3 and labels[-2] in SECOND_LEVEL and len(labels[-1]) == 2 else 2
    return '.'.join(labels[-keep:]) if len(labels) >= 2 and all(labels[-keep:]) else ''


def name_of(domain):
    """The name part of a domain, without its ending: kestrel-bikes for mail.kestrel-bikes.example."""
    return registrable(domain).split('.', 1)[0]


def fold(name):
    """A name as it reads: lowercase, the letters people mix up made one, no hyphens or dots."""
    text = str(name or '').lower()
    for seen, read in GLYPHS:
        text = text.replace(seen, read)
    return re.sub(r'[-_.]', '', text)


def one_apart(a, b):
    """Whether a and b differ by one letter: one changed, added or left out."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) > len(b):
        a, b = b, a
    i = next((n for n, (x, y) in enumerate(zip(a, b)) if x != y), len(a))
    return a[i + 1:] == b[i + 1:] if len(a) == len(b) else a[i:] == b[i + 1:]


def _runs(name):
    """The folded runs of words a hyphenated name starts or ends with: larkspurstudio-mail gives larkspurstudio and mail."""
    words = [w for w in re.split(r'[-_]', name) if w]
    return {fold(''.join(words[:i])) for i in range(1, len(words))} | {fold(''.join(words[i:])) for i in range(1, len(words))}


def confusable(a, b):
    """Whether two domains imitate one another (either way round)."""
    a, b = registrable(a), registrable(b)
    if not a or not b or a == b:
        return False
    na, nb = name_of(a), name_of(b)
    if na == nb:  # the same name at another ending: the organization's other domain
        return False
    fa, fb = fold(na), fold(nb)
    if min(len(fa), len(fb)) < 4:
        return False
    if fa == fb:
        return True
    if min(len(fa), len(fb)) >= EDIT_MIN and one_apart(fa, fb):
        return True
    return len(fb) >= WORD_MIN and fb in _runs(na) or len(fa) >= WORD_MIN and fa in _runs(nb)


def _keys(domain):
    """What two confusable domains always share at least one of, so a build compares only those (not every pair)."""
    name = name_of(domain)
    folded = fold(name)
    keys = {folded} | {r for r in _runs(name) if len(r) >= WORD_MIN}
    if len(folded) >= EDIT_MIN - 1:
        keys |= {folded[:i] + folded[i + 1:] for i in range(len(folded))}
    return keys


def imitations(first_seen, own=()):
    """{lookalike domain: the domain it imitates} among the domains in first_seen ({domain: when it first showed up,
    any comparable value}). own: the owner's own domains, always first."""
    order = {d: (0, '') for d in own}
    order.update({d: (1, at) for d, at in first_seen.items() if d not in order})
    by_key = collections.defaultdict(set)
    for domain in order:
        for key in _keys(domain):
            by_key[key].add(domain)
    out = {}
    for domain in sorted(order, key=order.get):
        if domain in own:
            continue
        earlier = sorted({d for key in _keys(domain) for d in by_key[key]
                          if d != domain and order[d] < order[domain] and confusable(d, domain)}, key=order.get)
        if earlier:
            out[domain] = earlier[0]
    return out


def apart(domains, others):
    """True when any of one person's domains imitates any of another's: never one person, whatever the name."""
    return any(confusable(a, b) for a in domains for b in others)


def first_seen(nodes, *events):
    """{node: when it first showed up, in UTC} from the build's node -> [(at, event_id)] maps."""
    return {node: min(at for found in events for at, _ in found.get(node, ())).astimezone(dt.timezone.utc)
            for node in nodes if any(found.get(node) for found in events)}


def mark(nodes, times, own, skip=frozenset()):
    """The Graph build's pass: marks each person node at a lookalike domain with what it imitates ({'from', 'domain',
    'name', 'node', 'address'}: the person on record there with the same name, when there is one), and drops a role a
    review gave them (only the owner's own word stays). nodes: the build's rows, info a dict; times: node -> when it was
    first seen (comparable values); own: the owner's domains; skip: free mail domains. Returns {node: mark}."""
    first, people = {}, collections.defaultdict(list)
    for n in nodes:
        if n[1] != 'person' or not isinstance(n[9], dict):
            continue
        for identifier in n[9].get('identifiers') or (n[0],):
            if not identifier.startswith('email:') or '@' not in identifier:
                continue
            domain = registrable(identifier.rsplit('@', 1)[1])
            if not domain or domain in skip:
                continue
            people[domain].append((n, identifier[6:]))
            if n[0] in times and (domain not in first or times[n[0]] < first[domain]):
                first[domain] = times[n[0]]
    own = {registrable(d) for d in own} - {''}
    found = imitations(first, own)
    marked = {}
    for domain, real in found.items():
        for n, sender in people[domain]:
            if n[0] in marked:
                continue  # one mark per person: their first address at the lookalike domain
            name = ' '.join(str(n[2] or '').casefold().split())
            twin = next(((m, address) for m, address in people.get(real, ()) if ' '.join(str(m[2] or '').casefold().split()) == name), None)
            info = n[9]
            info['lookalike'] = marked[n[0]] = {'from': domain, 'domain': real, 'name': twin[0][2] if twin else None,
                                                'node': twin[0][0] if twin else None, 'address': twin[1] if twin else None,
                                                'sender': sender}  # their own address: what the to-do shows for them
            if info.get('role_by') == 'review':
                info.update(role=None, role_by=None)
    return marked


def of_node(db, row):
    """A person's or organization's lookalike mark from the last build, else None. An organization carries its
    people's: everyone there writes from the lookalike domain."""
    info = json.loads(row['info'] or '{}') if isinstance(row['info'], str) else (row['info'] or {})
    if row['kind'] == 'person':
        return info.get('lookalike')
    if row['kind'] == 'org':
        found = db.execute("SELECT json_extract(n.info,'$.lookalike') FROM graph_links l JOIN graph_nodes n ON n.id=l.a WHERE l.b=? AND l.kind='member' "
                           "AND json_extract(n.info,'$.lookalike') IS NOT NULL LIMIT 1", (row['id'],)).fetchone()
        return json.loads(found[0]) if found else None
    return None


def refuse_role(db, row, source):
    """graph.set_role's check: a lookalike's own words can't make them anyone, so only the owner gives them a role."""
    like = source != 'owner' and of_node(db, row)
    if like:
        raise ValueError(f"No role for a lookalike: {like['from']} only looks like {like['domain']}"
                         + (f", where {like['name']} is on record ({like['address']})" if like.get('address') else '')
                         + '. Say on the to-do that it is not who it seems.')


def prep_bit(like):
    """What the preparation prompt says in place of a lookalike's role, with what to do about it (PREPARATION.md stays
    within its size: this shows only when one is on the to-do)."""
    return f"LOOKALIKE: {like['from']} only imitates {like['domain']}, so not " + (
        f"{like['name']}; any check goes to {like['address']}, never back to them" if like.get('address')
        else f"anyone there; any check goes to someone on record at {like['domain']}") + "; say plainly the message wasn't from who it claims"


def for_addresses(db, addresses):
    """{address: its mark} for the addresses whose person the last build marked as a lookalike."""
    wanted = sorted({str(a or '').strip().lower() for a in addresses if a and '@' in str(a)})
    if not wanted:
        return {}
    try:
        rows = db.execute("SELECT j.value,json_extract(n.info,'$.lookalike') FROM graph_nodes n, json_each(n.info,'$.identifiers') j "
                          "WHERE n.kind='person' AND json_extract(n.info,'$.lookalike') IS NOT NULL AND j.value IN (SELECT 'email:'||value FROM json_each(?))",
                          (json.dumps(wanted),)).fetchall()
    except Exception:  # noqa: BLE001 - no graph yet (a new install), or one from before: nothing is marked
        return {}
    return {r[0][6:]: json.loads(r[1]) for r in rows}


SOURCE_FROM = re.compile(r'^((?:Source: )?\S+ from )(.+?)((?: · [^·]+?)?(?: \(\+\d+ more\))?)$')


def source_line(line, people):
    """A to-do's source line ("email from Sam Lee · Wed 11 Nov") when its lead person (graph.card_people) is a lookalike:
    their own address in place of the name they borrowed, so the line never says it came from the known contact."""
    like = ((people or [{}])[0].get('lookalike') or {}).get('sender')
    found = like and line and SOURCE_FROM.match(str(line))
    return found[1] + like + found[3] if found else line


def recipients(actions):
    """Every to, cc and bcc address of the email actions in a Do it result."""
    return [x for a in actions if a.get('kind') == 'email' for x in [*a.get('to', []), *a.get('cc', []), *a.get('bcc', [])]]


def problems(actions, marks):
    """A soft "Check before saving" problem per email recipient at a lookalike domain (marks from for_addresses): a check
    on a lookalike's claim goes to the address on record, never back to the one that asked. The run can still override it."""
    out = []
    for address in dict.fromkeys(recipients(actions)):
        if like := marks.get(str(address).strip().lower()):
            out.append(f"{address} only looks like {like['domain']}: " + (
                f"write to {like['name']} at the address on record, {like['address']}, instead" if like.get('address')
                else f"don't write to it; use an address on record at {like['domain']}") + ", and say on the to-do that the message wasn't from them")
    return out


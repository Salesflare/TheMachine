"""Which record a fact names, read from its own words: no model.

A fact is tied to who it is about in fact_about (machine/store/facts.py). A review can say so with node ids, but a note
on a to-do or a learning pass mostly doesn't, and then the fact shows on no record's page and no preparation can pick
it by record. named() finds the one person, organization or project a fact's text clearly names:

- the record's own name, whole words, same capitals ("Acme" is not "acme");
- a person by their full name only: a first name alone names no one;
- one record: a name two records share links nothing, unless exactly one of them is on the fact's own to-do; a text
  that names two different records links nothing;
- a one-word name that starts a sentence names nothing: every sentence starts with a capital ("Close the deal");
- a one-word name is weak by itself (many organizations are called like a common word): it links only when that
  record is on the fact's own to-do. Elsewhere it links nothing, and it still counts as a second record named;
- a name the Machine itself works with is the tool, not the company: what its sources, connectors and channels are
  called (tools(), read from the product's own lists), so "not on Slack after 8" is about the owner;
- never the owner: their own person record, and their own organization (their mail domain's, or their
  colleagues'), are not what a fact is "about". Facts about them are the owner's own memory.

A wrong link costs more than a missing one: a linked fact leaves the general facts every review reads.

This module only reads. machine/store/facts.py writes the links (by 'name'): link_named when a fact is saved, and
link_named_all one time for the facts already there, which leaves one entry under Learning, Changes, with Undo
(learning_loop.name_links). A link the owner removed stays removed (fact_about keeps it with removed_at), also for a
later save of the same fact."""
import functools
import json

BY = 'name'            # fact_about.by for a link read from the fact's words
EDGE = '.,;:!?()[]{}"“”‘’\'«»'
MAX_WORDS = 6


def words(text):
    """[(word, starts a sentence)] of a text or a name: punctuation around a word and a possessive go."""
    out, start = [], True
    for raw in str(text or '').split():
        word = raw.strip(EDGE)
        for tail in ("'s", '’s'):
            if word.endswith(tail):
                word = word[:-2]
        if word:
            out.append((word, start))
        start = raw[-1] in '.!?:'
    return out


def name_key(kind, name):
    """A record's name as named() looks for it, or None when it can't clearly name the record: a person needs two
    words, anything else at least three characters, and every name a capital."""
    parts = [w for w, _ in words(name)]
    if not parts or len(parts) > MAX_WORDS or not any(c.isupper() for w in parts for c in w):
        return None
    if kind == 'person' and len(parts) < 2:
        return None
    key = ' '.join(parts)
    return key if len(key) >= 3 else None


@functools.lru_cache(maxsize=1)
def tools():
    """What the Machine's own sources, connectors and channels are called, lowercase: each label whole and each of
    its capitalized words ("Salesflare CRM": salesflare crm, salesflare, crm). Read from the product's own lists
    (onboarding's labels and every connector's, and the channels a voice can have), never written out here."""
    import onboarding
    from machine.store import voices
    labels = {*onboarding.LABELS.values(), *voices.VOICE_CHANNELS, *voices.OWN_KINDS.values()}
    for service in onboarding.sources():
        try:
            labels.add(str(onboarding.label(onboarding.SERVICES.get(service, service)) or ''))
        except Exception:  # a connector that doesn't load names nothing
            continue
    out = set()
    for label in labels:
        parts = [w for w, _ in words(label)]
        out.add(' '.join(parts).casefold())
        out.update(w.casefold() for w in parts if w[:1].isupper())
    return frozenset(out - {''})


def own(db, config, rows):
    """The ids among rows (graph_nodes) that are the owner's own: a person record at one of their addresses or under
    their name, and their own organization (their mail domain's, the one their colleagues are at, and an
    organization or project called like their own domain: "Acme" for acme.example, whatever id it has)."""
    import graph
    owner = graph.Owner(config or {}, db)
    name = graph.plain_name((config or {}).get('owner_name'))
    orgs, identifiers = graph.colleagues(db)  # as graph.own_domain tells the owner's own company
    theirs = {str(o) for o in orgs if o} | {'org:' + d for d in owner.domains} | {'org:' + i.rsplit('@', 1)[1].lower() for i in identifiers if '@' in i}
    labels = {d.split('.')[0].casefold() for d in owner.domains} - {''}
    out = set()
    for r in rows:
        if r['kind'] == 'person':
            try:
                ids = [r['id'], *(str(i) for i in json.loads(r['info'] or '{}').get('identifiers') or ())]
            except (ValueError, AttributeError):
                ids = [r['id']]
            if any(owner.has(i) for i in ids) or (name and graph.plain_name(r['name']) == name):
                out.add(r['id'])
        elif r['id'] in theirs or ' '.join(str(r['name'] or '').split()).casefold() in labels:
            out.add(r['id'])
    return out


def index(db, config=None):
    """{name: {record id: kind}} of the people, organizations and projects a text can name. A record known under
    several ids (info.identifiers) is one record. config (the service's, with its accounts): then only what a fact's
    own words may name, so without the owner's own records and without the names of the Machine's tools; without it,
    every record, for an about= that says who by name."""
    rows = db.execute("SELECT id,kind,name,info FROM graph_nodes WHERE kind IN ('person','org','project')").fetchall()
    alias = {}
    for r in rows:
        try:
            for other in json.loads(r['info'] or '{}').get('identifiers') or ():
                alias.setdefault(str(other), r['id'])
        except (ValueError, AttributeError):
            continue
    skip, tool = (own(db, config, rows), tools()) if config is not None else (set(), frozenset())
    names = {}
    for r in rows:
        key = name_key(r['kind'], r['name'])
        if key and r['id'] not in skip and key.casefold() not in tool:
            names.setdefault(key, {})[alias.get(r['id'], r['id'])] = r['kind']
    return names


def named(names, text, near=()):
    """(record id or None, why): the one record text names. why: 'one', 'none' (it names no record), 'shared' (a
    name several records have) or 'several' (it names more than one record). near: the records on the fact's own
    to-do, which settle a shared name when exactly one of them has it, and which a one-word name needs."""
    parts = words(text)
    found, shared, loose, taken = {}, False, False, set()
    for size in range(min(MAX_WORDS, len(parts)), 0, -1):  # the longest name first: "Acme Labs" before "Acme"
        for at in range(len(parts) - size + 1):
            span = range(at, at + size)
            if taken.intersection(span) or (size == 1 and parts[at][1]):  # one word at a sentence's start: no name
                continue
            have = names.get(' '.join(parts[i][0] for i in span))
            if not have:
                continue
            taken.update(span)
            ids = list(have)
            if size == 1 and len([i for i in ids if i in near]) != 1:
                loose = True  # one word, and nothing on the to-do says it is that record
                continue
            if len(ids) > 1:
                close = [i for i in ids if i in near]
                if len(close) != 1:
                    shared = True
                    continue
                ids = close
            found[ids[0]] = have[ids[0]]
    if shared:
        return None, 'shared'
    if len(found) != 1 or loose:
        return None, 'several' if found else 'none'
    return next(iter(found)), 'one'


def known(db, names, value):
    """The record a prompt named by something else than its node id: an address, an organization's domain or its
    exact name (one record only). None when that is no record."""
    value = ' '.join(str(value or '').split())
    for node in ('email:' + value.lower(), 'org:' + value.lower()):
        if db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind IN ('person','org','project')", (node,)).fetchone():
            return node
    have = names.get(' '.join(w for w, _ in words(value))) or {}
    return next(iter(have)) if len(have) == 1 else None


def records(db, node_ids):
    """{node id: {'name', 'kind', 'side'}} for the records facts are about. side: a person's, work or personal."""
    ids, out = sorted(node_ids), {}
    for at in range(0, len(ids), 500):
        part = ids[at:at + 500]
        for r in db.execute('SELECT id,kind,name,info FROM graph_nodes WHERE id IN (' + ','.join('?' for _ in part) + ')', part):
            try:
                side = json.loads(r['info'] or '{}').get('side')
            except (ValueError, AttributeError):
                side = None
            out[r['id']] = {'name': ' '.join(str(r['name'] or '').replace('<<<', '').replace('>>>', '').split()), 'kind': r['kind'], 'side': side}
    return out


def on_side(about, who, area):
    """Whether a fact may go in a prompt of this area (work or personal): one about people who are all on the other
    side stays out. A fact about no person, or about someone whose side isn't known, goes anywhere."""
    sides = {who[n]['side'] for n in about if n in who and who[n]['kind'] == 'person'} & {'work', 'personal'}
    return not sides or area in sides


def unnamed(text, about, who):
    """The names of the records a fact is about that its own words don't say, for its line in a prompt ('' if none)."""
    low = str(text or '').casefold()
    missing = [who[n]['name'] for n in about if n in who and who[n]['name'] and who[n]['name'].casefold() not in low]
    return ', '.join(dict.fromkeys(missing))[:80]


def todo_records(db, suggestion_id):
    """The ids of the records on a to-do's signals, each with the other ids it is known under and, for a person,
    their organization."""
    row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone() if suggestion_id else None
    try:
        ids = [int(i) for i in json.loads(row['event_ids'] or '[]')] if row else []
    except (ValueError, TypeError):
        ids = []
    if not ids:
        return set()
    out = set()
    for r in db.execute('SELECT DISTINCT n.id,n.info FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id WHERE g.event_id IN ('
                        + ','.join('?' for _ in ids) + ')', ids):
        out.add(r['id'])
        try:
            info = json.loads(r['info'] or '{}')
            out.update(str(i) for i in info.get('identifiers') or ())
            out.update([str(info['org'])] if info.get('org') else [])
        except (ValueError, AttributeError):
            continue
    return out

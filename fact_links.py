"""Which record a fact names, read from its own words: no model.

A fact is tied to who it is about in fact_about (machine/store/facts.py). A review can say so with node ids, but a note
on a to-do or a learning pass mostly doesn't, and then the fact shows on no record's page and no preparation can pick
it by record. named() finds the one person, organization or project a fact's text clearly names:

- the record's own name, whole words, same capitals ("Acme" is not "acme");
- a person by their full name only: a first name alone names no one;
- one record: a name two records share links nothing, unless exactly one of them is on the fact's own to-do; a text
  that names two different records links nothing.

This module only reads. machine/store/facts.py writes the links (by 'name'): link_named when a fact is saved, and
link_named_all one time for the facts already there, which leaves one entry under Learning, Changes, with Undo
(learning_loop.name_links). A link the owner removed stays removed (fact_about keeps it with removed_at), also for a
later save of the same fact."""
import json
import re

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


def index(db):
    """{name: {record id: kind}} of the people, organizations and projects a text can name. A record known under
    several ids (info.identifiers) is one record."""
    rows = db.execute("SELECT id,kind,name,info FROM graph_nodes WHERE kind IN ('person','org','project')").fetchall()
    alias = {}
    for r in rows:
        try:
            for other in json.loads(r['info'] or '{}').get('identifiers') or ():
                alias.setdefault(str(other), r['id'])
        except (ValueError, AttributeError):
            continue
    names = {}
    for r in rows:
        key = name_key(r['kind'], r['name'])
        if key:
            names.setdefault(key, {})[alias.get(r['id'], r['id'])] = r['kind']
    return names


def named(names, text, near=()):
    """(record id or None, why): the one record text names. why: 'one', 'none' (it names no record), 'shared' (a
    name several records have) or 'several' (it names more than one record). near: the records on the fact's own
    to-do, which settle a shared name when exactly one of them has it."""
    parts = words(text)
    found, shared, taken = {}, False, set()
    for size in range(min(MAX_WORDS, len(parts)), 0, -1):  # the longest name first: "Acme Labs" before "Acme"
        for at in range(len(parts) - size + 1):
            span = range(at, at + size)
            if taken.intersection(span):
                continue
            have = names.get(' '.join(parts[i][0] for i in span))
            if not have:
                continue
            taken.update(span)
            ids = list(have)
            if len(ids) > 1:
                close = [i for i in ids if i in near]
                if len(close) != 1:
                    shared = True
                    continue
                ids = close
            found[ids[0]] = have[ids[0]]
    if shared:
        return None, 'shared'
    if len(found) != 1:
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
    """The ids of the records on a to-do's signals, each with the other ids it is known under."""
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
            out.update(str(i) for i in json.loads(r['info'] or '{}').get('identifiers') or ())
        except (ValueError, AttributeError):
            continue
    return out

"""A contact detail the owner states for someone goes on that person's record in the Graph, not into Facts.

"Ann Example's WhatsApp number is +32 470 00 00 00" in a note on a to-do is the owner telling The Machine how to reach
Ann. Kept as a fact it hangs loose under Learning, Facts; on Ann's record it is a phone the owner added (the same as
Edit on her page), and it proves which records are Ann.

Whether a fact is a contact detail is judged by meaning, by the review or preparation that saves it (remember_fact
kind=contact, machine/prompts/review.py FACT_KIND_HINT): "Call the plumber on 0476... before Friday" is a commitment
that holds a number, not a contact detail. Then plain code checks it (no model):

- the text holds exactly one phone number or email address (detail);
- the person is certain (resolve): the one person record that has that number or address already, when the fact's
  words name them and no other record; else the one person its words name (fact_links.named, its rules). When the
  number is on one record and exactly one other person record has the same name, the owner just said they are one
  person: the two are merged (graph.merge, as the owner's word). Anything less certain stays a fact, as before.
- a number or address the owner took off that person, and a pair the owner said are not the same, stay as they said:
  then it is a fact.

The fact is kept, set aside as moved (facts.merged_into 'record:<node id>'), so the to-do's chat says where it went.
The move is one change under Learning, Changes (learning_changes kind 'contact', its before and after sealed like the
rest of that table) with Undo: the merge and the added detail go, and the fact is back as a fact. The facts saved
before this existed are moved once (FactsStore.contacts_once), only the ones that say nothing else: a plain fact (not
an event, commitment or preference, no end day) of a few words besides the name and the detail, with no other number."""
from __future__ import annotations

import json
import re

import fact_links
import graph
import learning_loop
from machine.owner_error import OwnerError

KIND = 'contact'           # learning_changes.kind of a move
MOVED = 'record:'          # facts.merged_into of a moved fact, then the record's id
ONCE = 'contacts_moved'    # learning_state: the one-time pass over the facts already saved ran
REST_WORDS = 6             # the one-time pass: at most this many words besides the name and the detail
PHONE_IN = re.compile(r'(?<![\w+])\+?\d[\d\s().-]{5,38}\d(?!\w)')
EMAIL_IN = re.compile(r'[^@\s<>()"“”,;]+@[^@\s<>()"“”,;]+\.[A-Za-z]{2,}')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}|\d{1,2}[./-]\d{1,2}[./-]\d{2,4}')


def detail(text):
    """('phones' or 'emails', the value as written) for the one phone number or email address in text, else None."""
    text = str(text or '')
    emails = [m.group().rstrip('.') for m in EMAIL_IN.finditer(text)]
    rest = EMAIL_IN.sub(' ', text)
    phones = [' '.join(m.group().split()) for m in PHONE_IN.finditer(rest)
              if len(re.sub(r'\D', '', m.group())) >= 7 and not DATE.fullmatch(m.group().strip())]
    if len(emails) + len(phones) != 1:
        return None
    if emails:
        return ('emails', emails[0]) if graph.EMAIL.fullmatch(emails[0]) else None
    return ('phones', phones[0]) if graph.PHONE.fullmatch(phones[0]) else None


def plain(text, name, value):
    """Whether text says only how to reach name, for the one-time pass: few other words, no other number."""
    rest = str(text).replace(value, ' ')
    for word, _ in fact_links.words(name):
        rest = re.sub(r'(?<!\w)' + re.escape(word) + r'(?:[’\']s)?(?!\w)', ' ', rest)
    words = [w for w, _ in fact_links.words(rest)]
    return len(words) <= REST_WORDS and not any(c.isdigit() for w in words for c in w)


def _contacts_now(db, node_id, kind):
    """(what a person's page shows for phones or emails, the keys of those the owner took off), as person_edit sees them."""
    row = db.execute("SELECT info FROM graph_nodes WHERE id=? AND kind='person'", (str(node_id),)).fetchone()
    if not row or kind not in graph.PERSON_LISTS:
        return None, None
    info = json.loads(row['info'] or '{}')
    group = set(info.get('identifiers') or ()) | {str(node_id)}
    kept = graph.person_edits_for(db, group).get(kind) or {}
    found = graph.found_contacts(group)[kind]
    stated = ' '.join(str((info.get('profile') or {}).get('phone') or '').split())
    if kind == 'phones' and graph.PHONE.fullmatch(stated):
        found.append(stated)
    gone = {graph.contact_key(kind, v) for v in kept.get('removed', ())}
    return [v for v in found if graph.contact_key(kind, v) not in gone] + list(kept.get('added', ())), gone


def taken_off(db, node_id, kind, value):
    """Whether the owner took this phone or email off the person's page."""
    return graph.contact_key(kind, value) in (_contacts_now(db, node_id, kind)[1] or ())


def add(db, node_id, kind, value, now):
    """Add one phone or email to a person as the owner's own, the way Edit on their page saves it (person_edit with
    the list as shown, plus this one). False when it is on their page already, or the owner took it off before."""
    shown, gone = _contacts_now(db, node_id, kind)
    if shown is None or graph.contact_key(kind, value) in gone | {graph.contact_key(kind, v) for v in shown}:
        return False
    graph.person_edit(db, node_id, {kind: shown + [value]}, now)
    return True


def _person(db, node_id):
    return db.execute("SELECT id,name FROM graph_nodes WHERE id=? AND kind='person'", (str(node_id),)).fetchone()


def resolve(db, names, text, kind, value, near=(), about=()):
    """(the person's node id, the other record to merge it with or None) when it is certain who text gives this
    detail for; None otherwise. names: fact_links.index with the owner's config (never the owner's own record). about:
    the node ids the saver said it is about."""
    holders = sorted({n for n, _ in (graph.people_by_phone if kind == 'phones' else graph.people_by_email)(db, [value])})
    said = [n for n in about if _person(db, n)]
    if len(holders) > 1 or len(said) > 1 or len(said) != len(about):
        return None
    if not holders:
        node, why = fact_links.named(names, text, near)
        node = said[0] if said and (why == 'none' or node == said[0]) else node if why == 'one' and not said else None
        return (node, None) if node and _person(db, node) and not taken_off(db, node, kind, value) else None
    holder = _person(db, holders[0])
    key = fact_links.name_key('person', holder['name']) if holder else None
    same = names.get(key) or {}
    if holder['id'] not in same or any(k != 'person' for k in same.values()) or (said and said[0] != holder['id']):
        return None  # the owner's own record, or a name that can't name them clearly
    if fact_links.named({key: {holder['id']: 'person'}}, text)[0] != holder['id']:
        return None  # its words don't name them
    rest = re.sub(r'(?<!\w)' + r'\s+'.join(re.escape(w) for w in key.split()) + r'(?!\w)', ' . ', text)
    if fact_links.named(names, rest, near)[1] != 'none':
        return None  # it names someone else too
    if taken_off(db, holder['id'], kind, value):
        return None  # the owner took it off their page
    others = [i for i in same if i != holder['id']]
    if not others:
        return holder['id'], None
    if len(others) > 1:
        return None
    a, b = sorted((holder['id'], others[0]))
    if db.execute('SELECT 1 FROM graph_merges WHERE a=? AND b=? AND same=0', (a, b)).fetchone() or not graph.PERSON_ID.fullmatch(others[0]):
        return None  # the owner said they are not the same
    return holder['id'], others[0]


def _ids(db, *nodes):
    out = set()
    for n in nodes:
        row = db.execute('SELECT info FROM graph_nodes WHERE id=?', (n,)).fetchone()
        out |= {n, *(json.loads(row['info'] or '{}').get('identifiers') or ())} if row else {n}
    return sorted(out)


def _edits(db, ids):
    return {r['identifier']: [r['fields'], r['updated_at']] for r in db.execute(
        f"SELECT identifier,fields,updated_at FROM person_edits WHERE identifier IN ({','.join('?' for _ in ids)})", ids)}


def move(db, fact_id, text, kind, value, node, other, run_id, at):
    """Put the detail on the record (merging other into it first), kept as one change with Undo; the Store sets the
    fact aside as moved (MOVED). {'record': node id, 'name', 'merged': bool, 'added': bool}."""
    ids = _ids(db, node, *([other] if other else []))
    before = _edits(db, ids)
    if other:
        graph.merge(db, node, other, True, at, 'owner', keep=node)  # the detail's record stays the one shown
    added = add(db, node, kind, value, at)
    name = _person(db, node)['name']
    learning_loop.record(db, run_id, KIND, str(fact_id), json.dumps({'node': node, 'name': name, 'other': other, 'merged_at': at if other else None,
                                                                    'ids': ids, 'edits': before, 'edits_after': _edits(db, ids)}), text, '')
    return {'record': node, 'name': name, 'merged': bool(other), 'added': added}


def undo(db, row):
    """Put a move back (learning_loop.undo, kind 'contact', which makes the fact a fact again): the merge and the added
    detail go. Refused when the owner changed that person's details or the fact since."""
    before = json.loads(row['before'])
    fact = db.execute('SELECT merged_into FROM facts WHERE id=?', (int(row['target']),)).fetchone()
    if not fact or fact['merged_into'] != MOVED + before['node'] or _edits(db, before['ids']) != before['edits_after']:
        raise OwnerError('That changed since. Change it where it is now')
    graph.edits_restore(db, {'kind': 'person', 'ids': before['ids'], 'rows': before['edits']})
    if before.get('other'):
        graph.unmerge(db, before['node'], before['other'], before['merged_at'])
    return {'graph': True, 'fact': int(row['target'])}


def moved_to(db, fact_id):
    """The applied move of this fact: {'change': its id, 'record', 'name'}, or None."""
    row = db.execute("SELECT id,before FROM learning_changes WHERE kind=? AND target=? AND status='applied' ORDER BY id DESC LIMIT 1",
                     (KIND, str(fact_id))).fetchone()
    if not row:
        return None
    before = json.loads(row['before'])
    return {'change': row['id'], 'record': before['node'], 'name': before['name']}


def movable(db, names):
    """The one-time pass: the facts already saved that only say how to reach one certain person, as [(fact id, text,
    (kind, value), (node, other))]; None while there is no graph yet. The Store moves them (contacts_once)."""
    if not db.execute('SELECT 1 FROM graph_nodes LIMIT 1').fetchone():
        return None
    out = []
    for f in db.execute("SELECT id,text,suggestion_id FROM facts WHERE removed_at IS NULL AND kind='fact' AND source IS NULL AND valid_until IS NULL "
                        "AND coalesce(fact_kind,'fact')='fact' AND kept_at IS NULL AND CAST(id AS TEXT) NOT IN "
                        "(SELECT target FROM learning_changes WHERE kind=?) ORDER BY id", (KIND,)).fetchall():  # one moved back stays
        found = detail(f['text'])
        about = [r[0] for r in db.execute("SELECT node_id FROM fact_about WHERE fact_id=? AND removed_at IS NULL AND by!=?", (f['id'], fact_links.BY))]
        who = found and resolve(db, names, f['text'], *found, fact_links.todo_records(db, f['suggestion_id']), about)
        if who and plain(f['text'], _person(db, who[0])['name'], found[1]):
            out.append((f['id'], f['text'], found, who))
    return out

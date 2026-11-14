"""Who is one person: identities joined on strong evidence only (merges, the directory, one message or
conversation, a LinkedIn profile, a number in a signature, the same full name), and people the owner
added by hand."""

import collections
import json

from graph import Union, linkedin_key, person_name, signature_pairs


def join_identities(db, per_event, gone, names, keys, senders):
    merges = db.execute('SELECT a,b,same,source FROM graph_merges ORDER BY created_at').fetchall()
    union = Union(frozenset((r['a'], r['b'])) for r in merges if not r['same'])  # Not the same, and an undone merge
    known = {identifier for (_, _, _, _, found) in per_event.values() for identifier, _, _, _ in found}
    for identifier in sorted(known):
        union.find(identifier)
    for r in merges:
        if r['same'] and not gone(r['a']) and not gone(r['b']):
            union.join(r['a'], r['b'], 'owner' if r['source'] == 'owner' else 'agent')
    for r in db.execute('SELECT identifier,name,email FROM identity_names'):
        if gone(r['identifier']) or (r['email'] and gone('email:' + r['email'].lower())):
            continue
        if r['name']:
            names[r['identifier']][person_name(r['name'])] += 3
        if r['email'] and r['identifier'] in known:
            union.join('email:' + r['email'].lower(), r['identifier'], 'directory')

    # People the owner added by hand (an address, or none yet): in the graph from the start, as known identities.
    manual = db.execute('SELECT identifier,kind,name FROM manual_nodes').fetchall()
    manual_people = [r['identifier'] for r in manual if r['kind'] == 'person' and not gone(r['identifier'])]
    for r in manual:
        if r['kind'] == 'person' and not gone(r['identifier']):
            known.add(r['identifier'])
            union.find(r['identifier'])
            names[r['identifier']][person_name(r['name']) or r['name']] += 5

    def best(identifier):
        top = names[identifier].most_common(1)
        return top[0][0] if top else None
    # Strong evidence, never a name alone: the same full name on two identities in one message (someone writing from
    # work with their own address in CC) or one conversation (never through a shared address: graph_joins.py), ...
    for one, other, where in keys.together():
        union.join(one, other, where)
    # ... the same LinkedIn profile, found for both by a lookup, and their WhatsApp number in mail they wrote themselves.
    by_profile = collections.defaultdict(set)
    for r in db.execute("SELECT identifier,profile FROM person_profiles WHERE status='found' AND profile IS NOT NULL"):
        try:
            url = linkedin_key(json.loads(r['profile']).get('linkedin_url')) if r['identifier'] in known else None
        except (ValueError, AttributeError):
            url = None
        if url:
            by_profile[url].add(r['identifier'])
    for url, group in sorted(by_profile.items()):
        group = sorted(group, key=lambda i: (not i.startswith('email:'), i))
        for other in group[1:]:
            union.join(group[0], other, 'profile')
    for address, number in signature_pairs(db, senders, best, known):
        union.join(address, number, 'signature')
    # The same full name on different channels is one person, unless two people carry it on one channel, someone said
    # they differ, or it is a work contact and a personal chat with nothing but the name in common: then it is a question.
    keys.join_names(db, union, known, best)
    joined = collections.defaultdict(list)
    for a, b, why in union.edges:
        joined[union.find(a)].append((a, b, why))
    return (union, manual, manual_people, joined)

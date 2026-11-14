"""The links between people: seen together, and relations a review or the owner read in the messages."""

import collections
import json

from graph import FLOOR, HALF_LIFE, fade


def relation_links(pair_day, age, related, union, kept, links, nodes):
    pairs = collections.defaultdict(float)
    pair_last = {}
    for (a, b, day), weight in pair_day.items():
        pairs[(a, b)] += fade(weight, age(day), HALF_LIFE['pair'])
        pair_last[(a, b)] = max(pair_last.get((a, b), day), day)
    # Relations a review or the owner read in the messages ("assistant of", "sister of", "introduced by").
    relations = {}
    for r in related:
        a, b = union.find(r['a']), union.find(r['b'])
        if a != b and a in kept and b in kept:
            relations[tuple(sorted((a, b)))] = (a, b, r['relation'], 'owner' if r['source'] == 'owner' else 'review')
    for (a, b), value in pairs.items():
        if value >= FLOOR and a in kept and b in kept and (a, b) not in relations:
            links.append((a, b, 'together', round(value, 4), pair_last[(a, b)].isoformat()))
    by_node = {n[0]: i for i, n in enumerate(nodes)}
    for pair, (a, b, relation, by) in relations.items():
        if not relation:
            continue  # a deliberate removal stays removed, including after identity merges
        links.append((*pair, 'relation', round(max(0.5, pairs.get(pair, 0)), 4), pair_last[pair].isoformat() if pair in pair_last else None))
        for node in (a, b):
            row = list(nodes[by_node[node]])
            info = json.loads(row[9])
            info.setdefault('relations', []).append({'a': a, 'a_name': nodes[by_node[a]][2], 'relation': relation, 'b': b, 'b_name': nodes[by_node[b]][2], 'by': by})
            row[9] = json.dumps(info)
            nodes[by_node[node]] = tuple(row)

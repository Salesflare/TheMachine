"""Same person? Likely pairs for the owner to Merge or keep apart."""

import collections
import json

import lookalike
from graph import FLOOR, likely_same, name_match, name_words, shown_id


def find_same_people(event_people, node_events, project_people, alike, union, infos, x_names, nodes, owner_names=()):
    # Same person? Likely pairs for the owner to Merge or keep apart, on both pages and in People. Never with a person
    # the lookalikes pass marked, nor anyone carrying the owner's own name (owner_names: the configured one and the ones
    # they send under).
    marked = {n[0] for n in nodes if isinstance(n[9], dict) and n[9].get('lookalike')}
    owner_words = [w for w in (name_words(n) for n in dict.fromkeys(owner_names) if n) if len(w) >= 2]

    def never(a, b):
        """A name is what anyone can type: never asked with a lookalike, with anyone using the owner's own name (their
        other addresses go under Your addresses), or across domains that imitate one another or swap the ending."""
        pa, pb = alike[a], alike[b]
        if a in marked or b in marked or any(name_match(p['words'], w) == 'same' for w in owner_words for p in (pa, pb)):
            return True
        ma, mb = pa.get('mail') or set(), pb.get('mail') or set()
        return bool(ma and mb and not ma & mb and lookalike.apart_same_person(ma, mb))
    seen_with = {}

    def together(node):
        if node not in seen_with:
            seen_with[node] = {p for _, e in node_events[node] for p in event_people.get(e, ())} - {node}
        return seen_with[node]
    on_projects = collections.defaultdict(set)
    for (node, pid), value in project_people.items():
        if value >= FLOOR:
            on_projects[node].add(pid)
    same_rows = likely_same(alike, union, together, on_projects, never)
    for a, b, why, _ in same_rows:
        for one, other in ((a, b), (b, a)):
            asks = infos[one].setdefault('same', [])
            if len(asks) < 3:
                asks.append({'id': other, 'why': why, 'from': shown_id(other, x_names)})  # where the other one is from: their address or number
    names_now = {n[0]: n[2] for n in nodes}
    for info in infos.values():
        for ask in info.get('same', ()):
            ask['name'] = names_now.get(ask['id'])
    nodes = [n[:9] + (json.dumps(n[9]),) if isinstance(n[9], dict) else n for n in nodes]
    kept = {n[0] for n in nodes}
    return (same_rows, nodes, kept)

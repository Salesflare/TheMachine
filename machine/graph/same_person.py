"""Same person? Likely pairs for the owner to Merge or keep apart."""

import collections
import json
import re

import lookalike
from graph import FLOOR, FREEMAIL, name_match, name_words, shown_id

SAME_BUCKET = 60         # more people than this with one first name: too common to compare
SMALL_PROJECT = 8        # people on a project before being on it together starts to say less
PROJECT_EVIDENCE = 0.3   # what a project's weight must reach before "on the same project" counts at all


def project_weight(people, orgs):
    """How much two people on one project says they may be one: 1 for a small project at one organization, falling with
    its people (8 / people) and divided by the organizations (company domains) on it. A catch-all project (testers from
    many companies) says nothing. Both "Same person?" (project_weights) and a name join (graph_joins.Keys.agree) use it."""
    return min(1.0, SMALL_PROJECT / max(1, people)) / max(1, orgs)


def project_weights(on_projects, people):
    """project_weight per project, for people as machine/graph/people.py stores them."""
    members = collections.defaultdict(set)
    for node, pids in on_projects.items():
        for pid in pids:
            members[pid].add(node)
    return {pid: project_weight(len(nodes), len({d for n in nodes for d in people.get(n, {}).get('domains', ())}))
            for pid, nodes in members.items()}


def phone_key(value):
    """A phone number as two records compare it: its last nine digits (+32 470 and 0470 are one number), else None."""
    digits = re.sub(r'\D', '', str(value or ''))
    return digits[-9:] if len(digits) >= 9 else None


def first_name_only(a, b):
    """Whether two similar names agree on no more than a first name: "Gary" and "Gary Wilson", "Frank" and "Frank".
    "Alex Lee" and "Alexander Lee" share a surname too."""
    return not (len(a) >= 2 and len(b) >= 2 and a[-1] == b[-1] and len(a[-1]) >= 2)


def likely_same(people, union, together, projects, never=lambda a, b: False, weights=None):
    """Pairs of people who may be one, for the owner to Merge or keep apart: [(a, b, why, score)]. The same full name at a
    domain in common (or no address on one side) is enough to ask; a similar name, or one across domains, needs something
    shared: people seen with both, a small project (weights: project_weights), the same role. Only a first name in common
    ("Gary" and "Gary Wilson") needs strong evidence instead: the same company domain, phone number or LinkedIn profile,
    unless both write from a company domain in common (the owner's own); and a full name that several such first-name-only
    people at other domains match is none of theirs. A name read from an address (jane.doe@) is only ever similar;
    never(a, b): pairs never asked (machine/graph/same_person.py)."""
    weights = weights or {}
    company = lambda p: (p.get('mail') or set()) - FREEMAIL  # a free-mail domain in common says nothing
    buckets = collections.defaultdict(list)
    for node, p in people.items():
        if p['words']:
            buckets[p['words'][0]].append(node)
            if len(p['words'][0]) >= 3:
                buckets[p['words'][0][:3]].append(node)  # "Alex" and "Alexander"
    seen, out, first_only = set(), [], collections.defaultdict(list)
    for members in buckets.values():
        if len(members) > SAME_BUCKET:
            continue
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                pair = tuple(sorted((a, b)))
                if pair in seen or a == b:
                    continue
                seen.add(pair)
                pa, pb = people[pair[0]], people[pair[1]]
                match = name_match(pa['words'], pb['words'])
                if match == 'same' and (pa.get('derived') or pb.get('derived')):
                    match = 'similar'
                if not match or union.kept_apart(union.find(pair[0]), union.find(pair[1])) or lookalike.apart(pa['domains'], pb['domains']) or never(*pair):
                    continue  # nor when one's domain imitates the other's (lookalike.py), a lookalike or the owner's name
                shared = []
                if pa['domains'] & pb['domains']:
                    shared.append(f"both at {sorted(pa['domains'] & pb['domains'])[0]}")
                if pa.get('phones', set()) & pb.get('phones', set()):
                    shared.append('the same phone number')
                if pa.get('linkedin', set()) & pb.get('linkedin', set()):
                    shared.append('the same LinkedIn profile')
                first = match == 'similar' and first_name_only(pa['words'], pb['words'])
                on_both = max((weights.get(pid, 1.0) for pid in projects.get(pair[0], set()) & projects.get(pair[1], set())), default=0)
                if first and not shared and not company(pa) & company(pb) and (on_both < 1 or pa.get('mail') and pb.get('mail')):
                    continue  # only a first name in common, and no company domain: a role, people around them or a project are no
                    # evidence, unless one has no address at all and both are on a small project at one organization
                weight = len(shared)
                if pa['role'] and pa['role'] == pb['role']:
                    shared.append('the same role')
                    weight += 1
                if together(pair[0]) & together(pair[1]):
                    shared.append('with the same people')
                    weight += 1
                if on_both >= PROJECT_EVIDENCE:
                    shared.append('on the same project')
                    weight += on_both
                if match == 'same' and len(pa['words']) >= 2 and (not (pa.get('mail') and pb.get('mail')) or pa['mail'] & pb['mail']) or shared:
                    why = ', '.join([('Same name' if match == 'same' else 'Similar name')] + shared)
                    out.append((*pair, why, round(weight + (2 if match == 'same' else 0) + min(pa['strength'], pb['strength']), 4)))
                    if first and not (pa.get('phones', set()) & pb.get('phones', set()) or pa.get('linkedin', set()) & pb.get('linkedin', set())):
                        fuller = max(pair, key=lambda n: len(people[n]['words']))
                        first_only[fuller].append((pair, frozenset(company(people[pair[0] if fuller == pair[1] else pair[1]]))))
    # One full name that first-name-only people at several companies all match ("Scott" at five domains and one "Scott
    # Lee"): none of them is a credible guess, unless a number or a profile says so
    crowd = {frozenset(pair) for asks in first_only.values() if len({at for _, at in asks}) >= 2 for pair, _ in asks}
    return sorted((s for s in out if frozenset(s[:2]) not in crowd), key=lambda s: -s[3])[:300]


def find_same_people(event_people, node_events, project_people, alike, union, infos, x_names, nodes, owner_names=(), asked=()):
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
    same_rows = likely_same(alike, union, together, on_projects, never, project_weights(on_projects, alike))
    paired = {frozenset(row[:2]) for row in same_rows}
    for (one, other), why in (asked or {}).items():  # what a chat shows about an address, not enough to join by itself (chat_proof.py)
        a, b = sorted((union.find(one), union.find(other)))
        if a != b and frozenset((a, b)) not in paired and a in alike and b in alike and not union.kept_apart(a, b) and not never(a, b):
            paired.add(frozenset((a, b)))
            same_rows.append((a, b, why, round(3 + min(alike[a]['strength'], alike[b]['strength']), 4)))
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

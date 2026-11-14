"""The owner's decisions on to-dos: once per to-do, for the people it was directly about and its project."""

import collections
import json

from graph import DECISION_WEIGHT, FLOOR, HALF_LIFE, fade, parse_time


def weigh_decisions(db, current, projects, direct_people, age, heat_day, strength, live, manual_people, union):
    # The owner's decisions on cards: once per card, for the people it was directly about.
    decided = collections.defaultdict(float)
    cards = {}
    for r in db.execute('SELECT d.suggestion_id,d.choice,d.feedback,d.created_at,s.event_ids,s.project FROM decisions d '
                        'JOIN suggestions s ON s.id=d.suggestion_id '
                        'WHERE NOT EXISTS (SELECT 1 FROM decision_annotations a WHERE a.decision_id=d.id) ORDER BY d.created_at'):
        weight = DECISION_WEIGHT.get(r['choice'])
        if weight is None or (r['choice'] == 'reject' and (r['feedback'] or '').strip() not in ('', 'Not relevant', 'Wrong facts')):
            continue  # "Already handled" says nothing against the people
        at = parse_time(r['created_at'])
        if at > current:
            continue
        card = cards.setdefault(r['suggestion_id'], {'weight': weight, 'at': at, 'event_ids': r['event_ids'], 'project': r['project']})
        if weight > card['weight'] or (weight < 0 < card['weight']):
            card.update(weight=weight, at=at)  # the strongest yes; a later Not relevant overrides it
    projects_by_name = {p['name'].casefold(): pid for pid, p in projects.items()}
    for card in cards.values():
        try:
            evidence = [int(i) for i in json.loads(card['event_ids'] or '[]')]
        except (ValueError, TypeError):
            evidence = []
        for node in {n for e in evidence for n in direct_people.get(e, ())}:
            decided[node] += fade(card['weight'], age(card['at'].date()), HALF_LIFE['person'])
        project_id = projects_by_name.get(str(card['project'] or '').casefold())
        if project_id and card['weight'] > 0:
            heat_day[(project_id, card['at'].date())] += card['weight']
    for node, weight in decided.items():
        strength[node] = max(0.0, strength[node] + weight)
        live[node] = max(0.0, live[node] + weight)
    for identifier in manual_people:  # added by hand: shown even before the first message
        node = union.find(identifier)
        strength[node] = max(strength[node], FLOOR)
        live[node] = max(live[node], FLOOR)

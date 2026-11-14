"""How strong: contact per person per day, capped, faded by age; and who was on each signal."""

import collections
import datetime as dt

from graph import DAY_CAP, HALF_LIFE, UNDATED, fade


def weigh_contact(per_event, union, current, tz, past):
    # How strong: per day, capped; faded by age.
    day_weight = collections.defaultdict(float)
    roles = collections.defaultdict(lambda: collections.defaultdict(set))
    live_roles = collections.defaultdict(lambda: collections.defaultdict(set))  # wrote, heard, met: what reviews read
    pair_day = collections.defaultdict(float)
    node_events = collections.defaultdict(list)
    event_people, direct_people = {}, {}
    next_meeting, accounts = {}, collections.defaultdict(set)
    live_weight, history_events = collections.defaultdict(float), collections.defaultdict(list)
    last_day = {}
    for event_id, (kind, at, account_id, m, found) in per_event.items():
        people = {}
        for identifier, _, weight, role in found:
            node = union.find(identifier)
            people[node] = max(people.get(node, 0), weight)
            if at > current:
                if role == 'met' and (node not in next_meeting or at < next_meeting[node]):
                    next_meeting[node] = at
                continue
            day = at.astimezone(tz).date()  # the owner's day: a message at 00:17 on Sunday is Sunday
            day_weight[(node, day)] += weight
            if kind not in UNDATED:  # last contact: what happened with them, never when a record about them was made
                last_day[node] = max(last_day.get(node, day), day)
            if event_id not in past:
                live_weight[(node, day)] += weight
                live_roles[node][role].add(day)
            roles[node][role].add(day)
            accounts[node].add(account_id)
        event_people[event_id] = list(people)
        direct_people[event_id] = [union.find(i) for i, _, weight, role in found if role != 'seen']
        for node in people:
            (history_events if event_id in past else node_events)[node].append((at, event_id))
        if at <= current and 2 <= len(people) <= 8:
            ordered = sorted(people)
            for i, a in enumerate(ordered):
                for b in ordered[i + 1:]:
                    pair_day[(a, b, at.date())] = min(0.5, pair_day[(a, b, at.date())] + 0.2 / (len(people) - 1))

    def age(day):
        return (current - dt.datetime.combine(day, dt.time(12), dt.timezone.utc)).total_seconds() / 86400

    strength, live = collections.defaultdict(float), collections.defaultdict(float)
    for (node, day), weight in day_weight.items():
        strength[node] += fade(min(DAY_CAP, weight), age(day), HALF_LIFE['person'])
    for (node, day), weight in live_weight.items():
        live[node] += fade(min(DAY_CAP, weight), age(day), HALF_LIFE['person'])
    signal_events = {e: v for e, v in per_event.items() if e not in past}  # projects and unnamed work: signals only
    return (roles, live_roles, pair_day, node_events, event_people, direct_people, next_meeting, accounts,
            history_events, last_day, age, strength, live, signal_events)

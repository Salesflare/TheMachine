"""The organization and project nodes, their member and project links."""

import collections
import datetime as dt
import json

import enrichment
from graph import FLOOR, HALF_LIFE, fade


def org_and_project_nodes(heat_day, history_events, live, named_orgs, said, manual, nodes, named, last_day, edits,
                          links, members, inboxes, profiles, site_logos, org_name, paying_names, wrong, current,
                          projects, project_events, tz, kept, project_people, project_people_last):
    heat_days = collections.defaultdict(list)
    for (pid, day), weight in heat_day.items():
        heat_days[pid].append((dt.datetime.combine(day, dt.time(12), dt.timezone.utc), min(2.0, weight)))

    def heat(pid, then):
        return sum(fade(w, (then - at).total_seconds() / 86400, HALF_LIFE['project']) for at, w in heat_days[pid] if at <= then)
    def org_live(people):  # an organization's closeness from signals alone, when history counts in it
        return {'live': round(sum(live[p] for p in people), 4)} if any(history_events.get(p) for p in people) else {}
    for org_id, people in named_orgs.items():
        role, role_by = said.get(org_id, (None, None))
        made = next((r['name'] for r in manual if r['identifier'] == org_id), None)
        nodes.append((org_id, 'org', (named.get(org_id) or (collections.Counter(p[2] for p in people).most_common(1)[0][0] if people else made) or org_id)[:200],
                      round(sum(v for _, v, _ in people), 4), max((last_day[p].isoformat() for p, _, _ in people if p in last_day), default=None),
                      len(people), None, 0, None, json.dumps({'domain': None, 'role': role, 'role_by': role_by, 'paying': False, 'profile': edits.get(org_id) or None,
                                                              'edited': sorted(edits.get(org_id, {})), 'wrong': False, 'stated': True,
                                                              'manual': made is not None, **org_live([p for p, _, _ in people])})))
        for node, value, _ in people:
            links.append((node, org_id, 'member', round(value, 4), None))
    for domain, people in members.items():
        total = sum(v for _, v in people + inboxes.get(domain, []))
        role, role_by = said.get('org:' + domain, (None, None))
        # What the owner wrote wins; the email domain is the website when nothing else says one.
        profile = {'website': enrichment.website(domain), **(profiles.get(domain) or {}), **edits.get(domain, {})}
        if domain in site_logos and 'logo' not in edits.get(domain, {}):  # its own site's icon: the logo when the lookup has none, else for small sizes
            profile['icon' if 'logo' in profile else 'logo'] = 'api/person-photo?p=' + site_logos[domain]
        nodes.append(('org:' + domain, 'org', org_name(domain)[:200], round(total, 4),
                      max((last_day[p].isoformat() for p, _ in people + inboxes.get(domain, []) if p in last_day), default=None), len(people), None, 0, None,
                      json.dumps({'domain': domain, 'role': role, 'role_by': role_by, 'paying': domain in paying_names, 'profile': profile,
                                  'edited': sorted(edits.get(domain, {})), 'wrong': domain in wrong,
                                  'manual': any(r['identifier'] == 'org:' + domain for r in manual), **org_live([p for p, _ in people])})))
        for node, value in people:
            links.append((node, 'org:' + domain, 'member', round(value, 4), None))
    two_weeks = current - dt.timedelta(days=14)
    for pid, project in projects.items():
        value, before = heat(pid, current), heat(pid, two_weeks)
        if value < FLOOR and not project_events.get(pid) and not project['board_id'] and not project['made_by']:  # on a board or made by the owner it stays
            continue
        events_ = sorted(project_events.get(pid, ()))
        # Last signal is what already happened; a meeting still to come is the next one, never the last.
        past = [e for e in events_ if e[0] <= current]
        coming = [e for e in events_ if e[0] > current]
        nodes.append(('project:' + str(pid), 'project', project['name'], round(value, 4), past[-1][0].astimezone(tz).date().isoformat() if past else None,
                      len(past), None, 0, round(value / before, 2) if before > FLOOR else None,
                      json.dumps({'closed_at': project['closed_at'], 'created_at': project['created_at'], 'probable': sum(1 for e in past if e[2]),
                                  'board_id': project['board_id'], 'stage': project['stage'],
                                  'next_meeting': coming[0][0].isoformat() if coming else None})))
        kept.add('project:' + str(pid))
    for (node, pid), value in project_people.items():
        if value >= FLOOR and node in kept:
            links.append((node, 'project:' + str(pid), 'project', round(value, 4), project_people_last[(node, pid)].date().isoformat()))

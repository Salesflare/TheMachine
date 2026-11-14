"""Projects: labels spread to the rest of their threads, probable ones, their heat and who is on them; and
unnamed work."""

import collections

from graph import HALF_LIFE, fade, load_vectors, probable_projects, thread_key, unnamed_work


def place_on_projects(db, signals, config, signal_events, event_people, current, age, owner_events):
    # Projects: labels, spread to the rest of their threads.
    projects = {r['id']: dict(r) for r in db.execute('SELECT id,name,created_at,closed_at,board_id,stage,made_by FROM projects')}
    labelled = collections.defaultdict(set)
    for r in db.execute('SELECT event_id,project_id FROM event_projects'):
        if r['project_id'] in projects:
            labelled[r['event_id']].add(r['project_id'])
    threads = collections.defaultdict(list)
    for event_id, account_id, kind, at, m in signals:
        key, exact = thread_key(kind, m)
        if key:
            threads[(account_id, key)].append((at, event_id, exact))
    spread = {e: set(p) for e, p in labelled.items()}
    for members in threads.values():
        tagged = [(at, labelled[e]) for at, e, _ in members if e in labelled]
        if not tagged:
            continue
        for at, event_id, exact in members:
            for tagged_at, ids in tagged:
                if exact or abs((at - tagged_at).total_seconds()) <= 2 * 86400:
                    spread.setdefault(event_id, set()).update(ids)
    times = {event_id: at for event_id, _, _, at, _ in signals}
    vectors = load_vectors(db, set(signal_events), config['embeddings']) if isinstance(config.get('embeddings'), dict) and config['embeddings'].get('enabled') is not False else {}
    probable = probable_projects(spread, event_people, vectors, times, current, {pid for pid, p in projects.items() if not p['closed_at']},
                                 {e: v[0] for e, v in signal_events.items()})
    heat_day = collections.defaultdict(float)
    project_events = collections.defaultdict(list)
    project_people = collections.defaultdict(float)
    project_people_last = {}
    for event_id, ids, guess in [(e, ids, 0) for e, ids in spread.items()] + [(e, ids, 1) for e, ids in probable.items()]:
        at = times.get(event_id)
        if at is None:
            continue
        for pid in ids:
            project_events[pid].append((at, event_id, guess))
            if at <= current:
                # A probable one counts half until a review confirms it.
                heat_day[(pid, at.date())] += 0.1 if guess else 0.2
                for node in event_people.get(event_id, ()):
                    key = (node, pid)
                    project_people[key] += fade(0.15 if guess else 0.3, age(at.date()), HALF_LIFE['project_person'])
                    project_people_last[key] = max(project_people_last.get(key, at), at)
    for r in db.execute('SELECT project_id,node_id FROM project_people'):  # people the owner put on a project themselves
        if r['project_id'] in projects:
            key = (r['node_id'], r['project_id'])
            project_people[key] = max(project_people[key], 0.5)
            project_people_last.setdefault(key, current)
    unnamed = unnamed_work(signal_events, event_people, owner_events, set(spread) | set(probable), vectors, current)
    return (projects, spread, probable, heat_day, project_events, project_people, project_people_last, unnamed)

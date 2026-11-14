"""What a build publishes besides nodes and links: organizations folded into their parent (crm.decorate), each
node's signals and history, and unnamed work."""

import json
import re


def event_and_unnamed_rows(db, nodes, links, kept, node_events, project_events, direct_people, history_events, unnamed):
    from crm import decorate  # organizations folded into the one they are part of, and who owns each record
    nodes, links = decorate(db, nodes, links)
    kept |= {n[0] for n in nodes}
    event_rows = []
    for node, items in [(n, [(at, e, 0) for at, e in v]) for n, v in node_events.items()] + [('project:' + str(p), v) for p, v in project_events.items()]:
        if node in kept:
            # Complete membership for old task evidence; only readers cap display lists.
            # direct: the person was in contact with the owner on it, not merely on it.
            event_rows += [(node, e, at.isoformat(), guess, int(node in direct_people.get(e, ()))) for at, e, guess in sorted(items)]
    history_rows = [(node, e, at.isoformat()) for node, items in history_events.items() if node in kept for at, e in items]
    names_of = {n[0]: n[2] for n in nodes}
    unnamed_rows = []
    for group, people, last in unnamed:
        marks = ','.join('?' for _ in group)
        titles = list(dict.fromkeys(re.sub(r'^(?:(?:re|fwd?|aw|tr)\s*:\s*)+', '', r[0], flags=re.I)[:80]
                                    for r in db.execute(f'SELECT title FROM events WHERE id IN ({marks}) ORDER BY occurred_at DESC', group)))
        unnamed_rows.append((min(group), json.dumps(sorted(group)), json.dumps([names_of[p] for p in people if p in names_of][:4]),
                             json.dumps(titles[:4]), len(group), last.isoformat()))
    return (nodes, links, kept, event_rows, history_rows, unnamed_rows)

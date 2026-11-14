"""What says a person is Work or Personal (auto_side): the sides of the accounts their conversations came
from, the sharing review's calls on their threads, and the projects they're on."""

import collections

from graph import WORK_VERDICTS, account_side, thread_key


def read_sides(config, db, spread, per_event, projects, direct_people):
    # What says a person is work or personal (auto_side): the sides of the accounts their conversations came from, the
    # sharing review's calls on their threads, and the projects they're on.
    side_of_account = {a.get('id'): account_side(a) for a in config.get('accounts', []) if a.get('id')}
    calls = {}
    if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='share_threads'").fetchone():
        calls = {r[0]: (r[1], r[2]) for r in db.execute('SELECT thread,verdict,hand FROM share_threads')}
    came_from = collections.defaultdict(set)  # project -> the sides of the accounts its messages came from
    for event_id, ids in spread.items():
        if event_id in per_event:
            for pid in ids:
                came_from[pid].add(side_of_account.get(per_event[event_id][2]))
    project_side = {}
    for pid, p in projects.items():
        found = came_from[pid] - {None}
        # a board is a pipeline the owner keeps like a CRM: work; another project is the side its messages came from
        project_side[pid] = 'work' if p['board_id'] is not None else found.pop() if len(found) == 1 else None
    thread_sides = collections.defaultdict(dict)  # person node -> thread -> work or personal
    on_projects = collections.defaultdict(set)
    for event_id, (kind, _, _, m, _) in per_event.items():
        thread = thread_key(kind, m)[0] or f'ev:{event_id}'  # shared_graph.thread_of
        verdict, hand = calls.get(thread, (None, None))
        side = 'personal' if verdict == 'personal' else 'work' if verdict in WORK_VERDICTS or hand == 'team' else None
        for node in direct_people.get(event_id, ()):
            if side:
                thread_sides[node][thread] = side
            on_projects[node] |= spread.get(event_id, set())
    for r in db.execute('SELECT project_id,node_id FROM project_people'):
        if r['project_id'] in projects:
            on_projects[r['node_id']].add(r['project_id'])
    return (side_of_account, project_side, thread_sides, on_projects)

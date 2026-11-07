"""The Projects board view (graph.boards): every board with its stages and projects, read in a few queries.

It used to ask per project for its open to-dos, its messages (how long the other side hasn't answered), its owner
and its moves: some 2,400 queries for 600 projects on each Graph tab open. Those come in one query each now, for
all projects at once; what a tile says is the same."""
import json

import graph

_ASCII_LOWER = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')


def _nocase(text):
    """SQLite's COLLATE NOCASE: only A to Z fold."""
    return str(text).translate(_ASCII_LOWER)


def _todos(db, projects):
    """{project node: [(id, title)], newest first}: the open to-dos on each project, by its name or (none named or
    picked by hand) one of its signals on it (graph._project_cards_where, for all projects at once)."""
    statuses, by = json.dumps(list(graph.OPEN_CARD)), graph._has_column(db, 'suggestions', 'project_by')
    rows = db.execute('SELECT id,title,project FROM suggestions WHERE status IN (SELECT value FROM json_each(?)) ORDER BY created_at DESC',
                      (statuses,)).fetchall()
    linked = {}
    for r in db.execute("SELECT DISTINCT s.id,g.node_id FROM suggestions s, json_each(s.event_ids) j JOIN graph_events g ON g.event_id=j.value "
                        "WHERE s.status IN (SELECT value FROM json_each(?)) AND (s.project IS NULL OR s.project='') AND g.probable=0 "
                        "AND g.node_id IN (SELECT value FROM json_each(?))" + (' AND s.project_by IS NULL' if by else ''),
                        (statuses, json.dumps(list(projects)))):
        linked.setdefault(r['node_id'], set()).add(r['id'])
    named, place = {}, {r['id']: (i, r['title']) for i, r in enumerate(rows)}
    for r in rows:
        if r['project'] is not None:
            named.setdefault(_nocase(r['project']), set()).add(r['id'])
    return {node: [(i, place[i][1]) for i in sorted((named.get(_nocase(name), set()) | linked.get(node, set())) & place.keys(), key=lambda i: place[i][0])]
            for node, name in projects.items()}


def _waiting_since(db, nodes):
    """{project node: when the owner first wrote since the other side last did} (graph._waiting_since, for all)."""
    out = {}
    for r in db.execute("SELECT g.node_id,e.occurred_at,(json_extract(e.metadata,'$.from_me') IS 1 OR EXISTS(SELECT 1 FROM json_each(e.metadata,'$.labels') "
                        "WHERE value='SENT')) mine FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id IN (SELECT value FROM json_each(?)) "
                        "AND g.probable=0 AND e.deleted=0 AND e.kind IN (SELECT value FROM json_each(?)) ORDER BY g.node_id,e.occurred_at",
                        (json.dumps(nodes), json.dumps(list(graph.MESSAGE_KINDS)))):
        out[r['node_id']] = (out.get(r['node_id']) or r['occurred_at']) if r['mine'] else None
    return out


def _owners(db, nodes):
    """{node: {'owner', 'owner_name'}} for the records someone in the owner's Work Fleet owns (graph.owner_of)."""
    return {r['id']: {'owner': r['owner'], 'owner_name': r['name']} for r in db.execute(
        "SELECT id,json_extract(info,'$.owner') owner,json_extract(info,'$.owner_name') name FROM graph_nodes "
        "WHERE id IN (SELECT value FROM json_each(?))", (json.dumps(nodes),)) if r['owner']}


def boards(db, now):
    """graph.boards: every board with its stages and projects, for the Projects board view."""
    out, org_cache, orgs = [], {}, {}
    today = graph.parse_time(now)
    boards_rows = db.execute('SELECT * FROM boards ORDER BY is_default DESC,id').fetchall()
    projects = {b['id']: db.execute('SELECT * FROM projects WHERE board_id=? AND closed_at IS NULL ORDER BY coalesce(stage_at,created_at) DESC',
                                    (b['id'],)).fetchall() for b in boards_rows}
    every = {'project:' + str(p['id']): p for rows in projects.values() for p in rows}
    nodes = list(every)
    todos, waiting, owners = _todos(db, {n: p['name'] for n, p in every.items()}), _waiting_since(db, nodes), _owners(db, nodes)
    moved = {r[0] for r in db.execute('SELECT project_id FROM project_moves WHERE project_id IN (SELECT value FROM json_each(?)) '
                                      'GROUP BY project_id HAVING count(*)>1', (json.dumps([p['id'] for p in every.values()]),))}

    def org_of(key):
        if key not in orgs:
            orgs[key] = graph.project_org(db, key)
        return orgs[key]
    for b in boards_rows:
        names, items = graph.stage_names(b), []
        for p in projects[b['id']]:
            node = 'project:' + str(p['id'])
            org = org_of(p['org'] or (graph.infer_org(db, p['id'], org_cache) if not p['org_by'] else None))  # set, or what fill_orgs will set
            mine_since = waiting.get(node)
            since = graph.parse_time(p['stage_at'] or p['created_at'])
            last = None if p['stage_by'] else next(iter(graph.project_events(db, p['id'], 1, now)), None)  # an unplaced tile: its latest message
            found = todos[node]
            card = found[0] if found else None
            items.append({'id': node, 'name': p['name'], 'stage': p['stage'] if p['stage'] in names else names[0], 'reason': p['stage_reason'],
                          'by': p['stage_by'], **graph.sort_view(db, p), 'at': p['stage_at'], 'event_id': p['stage_event_id'], 'next': p['next_step'],
                          'first': p['id'] not in moved, 'days': max(0, (today - since).days), 'closed': bool(p['closed_at']),
                          'visibility': p['visibility'], 'no_reply_days': max(0, (today - graph.parse_time(mine_since)).days) if mine_since else None,
                          'org': {**org, 'node_id': org['id']} if org else None, 'card': {'id': card[0], 'title': card[1]} if card else None,
                          'todos': len(found),
                          **({'last_at': last['occurred_at'], 'last_event_id': last['id']} if last else {}),
                          **({'value': p['value']} if p['value'] is not None else {}), **({'close_date': p['close_date']} if p['close_date'] else {}),
                          **({'outcome': p['outcome']} if p['outcome'] else {}), **owners.get(node, {})})
        out.append({'id': b['id'], 'name': b['name'], 'about': b['about'], 'side': bool(b['side']), 'visibility': b['visibility'] or 'team',
                    'stages': json.loads(b['stages']) + ([{'name': graph.STALLED, 'side': True}] if b['side'] else []), 'projects': items,
                    'stuck': sum(1 for i in items if (i['no_reply_days'] or 0) >= graph.STUCK_DAYS and i['stage'] != graph.STALLED),
                    'sorting': sum(1 for i in items if i['sorting']), 'default': bool(b['is_default']), 'maybes': graph.board_maybes(db, b['id'])})
        out[-1]['backfill'] = graph.backfill_view(db, b['id'], now, out[-1]['maybes'])
    return out

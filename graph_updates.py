"""What The Machine updated today: the people, organizations and projects it changed or learned something about since
the owner's midnight, so the Graph's lists can show that it does things, calmly. One quiet line on top of each list
("Updated 4 people today", which opens what changed) and a small mark on each row it touched.

Read only, from the same rows as a page's Recent changes (record_log.py), so a marked row's page says what changed:
a review's role (person_roles), where someone works (person_orgs), how two people are related (graph_relations),
two identities joined (graph_merges), Work or Personal from a new rule (side_changes), a project moved by a review
(project_moves), a project on no board its proof marked done (project_success) and a fact about them (fact_about). The owner's own edits are no news to them and stay out.
No table of its own, no model call."""
from __future__ import annotations

import datetime as dt
import json
import sqlite3

import timeutil

KINDS = {'person': 'people', 'org': 'orgs', 'project': 'projects'}
LISTED = 20   # changed records listed per kind, newest first; the line counts them all
SCAN = 2000   # rows read per source and day at most: a day of a big first look stays a quick read


def since(now=None):
    """The owner's midnight today, in UTC ISO (what the database stores)."""
    current = (now or dt.datetime.now(dt.timezone.utc)).astimezone(timeutil.local_tz())
    return current.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(dt.timezone.utc).isoformat()


def _at(text):
    try:
        found = dt.datetime.fromisoformat(str(text).replace('Z', '+00:00'))
    except ValueError:
        return None
    return found if found.tzinfo else found.replace(tzinfo=dt.timezone.utc)


def _rows(db, sql, args):
    try:
        return db.execute(sql, args).fetchall()
    except sqlite3.OperationalError:
        return []  # a graph without that table (tests, an older database): what can be read still counts


def _changes(db, start):
    """[(identifier, at, change)] from each source since start, the Machine's own only. start is compared as text first
    (a day earlier, for stored offsets other than UTC), then as a time."""
    loose = (_at(start) - dt.timedelta(days=1)).isoformat()
    out = []
    for r in _rows(db, "SELECT identifier,role,created_at FROM person_roles WHERE source!='owner' AND role!='' AND created_at>=? "
                       'ORDER BY created_at DESC LIMIT ?', (loose, SCAN)):
        out.append((r[0], r[2], {'kind': 'role', 'role': r[1]}))
    for r in _rows(db, "SELECT identifier,org,created_at FROM person_orgs WHERE source!='owner' AND org!='' AND created_at>=? "
                       'ORDER BY created_at DESC LIMIT ?', (loose, SCAN)):
        out.append((r[0], r[2], {'kind': 'org', 'org': r[1]}))
    for r in _rows(db, "SELECT g.a,g.b,g.relation,g.created_at,x.name,y.name FROM graph_relations g LEFT JOIN graph_nodes x ON x.id=g.a "
                       "LEFT JOIN graph_nodes y ON y.id=g.b WHERE g.source!='owner' AND g.relation!='' AND g.created_at>=? "
                       'ORDER BY g.created_at DESC LIMIT ?', (loose, SCAN)):
        if r[4] and r[5]:
            change = {'kind': 'relation', 'a_name': r[4], 'b_name': r[5], 'relation': r[2]}
            out += [(r[0], r[3], change), (r[1], r[3], change)]
    for r in _rows(db, "SELECT a,b,created_at FROM graph_merges WHERE same=1 AND coalesce(source,'agent')!='owner' AND created_at>=? "
                       'ORDER BY created_at DESC LIMIT ?', (loose, SCAN)):
        import graph
        out += [(r[0], r[2], {'kind': 'joined', 'shown': graph.shown_id(r[1], {})}), (r[1], r[2], {'kind': 'joined', 'shown': graph.shown_id(r[0], {})})]
    for r in _rows(db, "SELECT c.node_id,c.after,c.at FROM side_changes c JOIN graph_nodes n ON n.id=c.node_id WHERE c.at>=? AND c.after IN ('work','personal') "
                       "AND json_extract(n.info,'$.side')=c.after AND coalesce(json_extract(n.info,'$.side_by'),'')!='owner' ORDER BY c.at DESC LIMIT ?", (loose, SCAN)):
        out.append((r[0], r[2], {'kind': 'side', 'side': r[1]}))
    for r in _rows(db, "SELECT project_id,stage,at FROM project_moves WHERE source!='owner' AND at>=? ORDER BY at DESC LIMIT ?", (loose, SCAN)):
        out.append(('project:' + str(r[0]), r[2], {'kind': 'move', 'stage': r[1]}))
    for r in _rows(db, "SELECT s.project_id,s.marked_at,(p.value IS NOT NULL OR p.close_date IS NOT NULL) deal FROM project_success s JOIN projects p ON p.id=s.project_id "
                       "WHERE s.marked_by='evidence' AND s.marked_at>=? ORDER BY s.marked_at DESC LIMIT ?", (loose, SCAN)):
        out.append(('project:' + str(r[0]), r[1], {'kind': 'done', 'deal': bool(r[2])}))  # its proof marked a project on no board done
    for r in _rows(db, "SELECT a.node_id,f.text,f.created_at FROM fact_about a JOIN facts f ON f.id=a.fact_id WHERE a.removed_at IS NULL AND f.removed_at IS NULL "
                       "AND f.kind='fact' AND a.by!='owner' AND f.created_at>=? ORDER BY f.created_at DESC LIMIT ?", (loose, SCAN)):
        out.append((r[0], r[2], {'kind': 'fact', 'text': r[1]}))
    first = _at(start)
    return [(str(i), str(at), change) for i, at, change in out if i and _at(at) and _at(at) >= first]


def _nodes(db, identifiers):
    """{identifier: graph_nodes row (id, kind, name)} for the ones still in the graph: a node's own id, else the person
    whose identifiers have it (graph_identifiers), else a role's id (info.role_id)."""
    wanted = json.dumps(sorted(set(identifiers)))
    found = {r[0]: r for r in _rows(db, 'SELECT id,kind,name FROM graph_nodes WHERE id IN (SELECT value FROM json_each(?))', (wanted,))}
    left = json.dumps(sorted(set(identifiers) - set(found)))
    if left != '[]':
        for r in _rows(db, "SELECT g.identifier,n.id,n.kind,n.name FROM graph_identifiers g JOIN graph_nodes n ON n.id=g.node_id "
                           'WHERE g.identifier IN (SELECT value FROM json_each(?))', (left,)):
            found.setdefault(r[0], r[1:])
        left = json.dumps(sorted(set(identifiers) - set(found)))
    if left != '[]':
        for r in _rows(db, "SELECT json_extract(info,'$.role_id'),id,kind,name FROM graph_nodes WHERE json_extract(info,'$.role_id') IN (SELECT value FROM json_each(?))", (left,)):
            found.setdefault(r[0], r[1:])
    return found


def updated(db, now=None):
    """{node id: {'id', 'kind', 'name', 'at', 'change'}}: every person, organization and project The Machine updated
    since the owner's midnight, with its newest change (a Recent changes line: role, org, relation, joined, side,
    move or fact)."""
    changes = _changes(db, since(now))
    nodes = _nodes(db, [i for i, _, _ in changes]) if changes else {}
    newest = {}
    for identifier, at, change in changes:
        row = nodes.get(identifier)
        if row and row[1] in KINDS and (row[0] not in newest or at > newest[row[0]]['at']):
            newest[row[0]] = {'id': row[0], 'kind': row[1], 'name': row[2], 'at': at, 'change': change}
    return newest


def today(db, now=None, found=None):
    """{'since', 'people', 'orgs', 'projects'}: for each kind, how many records The Machine updated today ('count') and
    the newest LISTED of them ('items': id, name, at, change), newest first. For the line on top of each Graph list.
    Projects also give every id ('ids'): the board's tiles carry the mark too, and a day has a handful of them."""
    found = updated(db, now) if found is None else found
    out = {'since': since(now)}
    for kind, key in KINDS.items():
        items = sorted((x for x in found.values() if x['kind'] == kind), key=lambda x: x['at'], reverse=True)
        out[key] = {'count': len(items), 'items': [{k: x[k] for k in ('id', 'name', 'at', 'change')} for x in items[:LISTED]]}
        if kind == 'project':
            out[key]['ids'] = [x['id'] for x in items]
    return out

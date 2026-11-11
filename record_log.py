"""Recent changes on a record: a short, dated log under a person's, organization's or project's page of what The
Machine changed or learned about it, when, and from where, so a wrong conclusion is easy to spot and to take back
right there (each line names the existing correction: Edit, Forget, Remove, Undo).

Read only, from what the Machine already keeps; no table of its own and no model call:
- a review's role for them (person_roles, with the message it read it in) and the owner's corrections of one (role_corrections);
- where someone works, as a source stated it (person_orgs); on an organization's page, who was placed there that way;
- how two people are related (graph_relations);
- two identities a review joined as one person (graph_merges, source not the owner's);
- Work or Personal set by a new rule (side_changes);
- a project moved by a review (project_moves), with Undo back to the stage before while it still stands there;
- a project on no board its proof marked done (project_success), with Undo (Reopen) while it stays done;
- facts about them (facts, fact_about), "updated" when a newer note condensed older ones (merged_into);
- a connected AI's change to the record (ai_writes), with its Undo while nothing changed it since.

The owner's own edits are no news to them and stay out, apart from a corrected role (what they fixed, and from what).
Each source is a message (its id, so the page opens it), the owner's note on a to-do, or a connected AI by name."""
from __future__ import annotations

import json
import re
import sqlite3

LIMIT = 20   # lines per record, newest first; the page shows a few and the rest under Show more
SLACK_ID = re.compile(r'\b[UW][A-Z0-9]{8,}\b')
SERVICES = {'gmail.message': 'email', 'salesflare.email': 'email', 'calendar.event': 'meeting', 'salesflare.meeting': 'meeting',
            'zoom.summary': 'meeting', 'meeting.notes': 'meeting', 'meeting.transcript': 'meeting', 'whatsapp.message': 'WhatsApp',
            'slack.message': 'Slack', 'teams.message': 'Teams', 'linkedin.message': 'LinkedIn', 'telegram.message': 'Telegram',
            'x.dm': 'X', 'x.mention': 'X', 'intercom.conversation': 'Intercom', 'github.notification': 'GitHub'}


def _json(text, default):
    try:
        found = json.loads(text or '')
    except (TypeError, ValueError):
        return default
    return found if isinstance(found, type(default)) else default


def _sender(meta):
    """Who sent a message, as its first name, or '' (an address, a number, a raw id is never shown)."""
    try:
        from machine.store.views import sender_first_name
        who = sender_first_name(meta)
    except (ImportError, TypeError, ValueError, AttributeError):
        who = ''
    return '' if not who or SLACK_ID.search(who) else who[:60]


def _events(db, ids):
    """{event id: source} for the messages lines came from: its kind as a word, who sent it, if the owner did."""
    ids = sorted({int(i) for i in ids if str(i or '').isdigit()})
    if not ids:
        return {}
    out = {}
    for r in db.execute("SELECT id,kind,metadata,occurred_at FROM events WHERE deleted=0 AND id IN (SELECT value FROM json_each(?))", (json.dumps(ids),)):
        meta = _json(r['metadata'], {})
        mine = meta.get('from_me') is True or 'SENT' in (meta.get('labels') or ())
        out[r['id']] = {'type': 'event', 'id': r['id'], 'via': SERVICES.get(r['kind'], 'message'), 'at': r['occurred_at'],
                        **({'mine': True} if mine else {'from': _sender(meta)})}
    return out


def _source(events, event_id, via=None):
    found = events.get(event_id) if event_id is not None else None
    if found:
        return found
    return {'type': 'line', 'via': via} if via else None  # the message is gone; say where it was read, if known


def _roles(db, ids, out, wanted):
    """What a review read they are to the owner, with its message or the line it was read in; the owner's corrections."""
    r = db.execute("SELECT role,created_at,event_id,quote FROM person_roles WHERE identifier IN (SELECT value FROM json_each(?)) AND source!='owner' AND role!='' "
                   'ORDER BY created_at DESC LIMIT 1', (ids,)).fetchone()
    if r:
        out.append({'kind': 'role', 'at': r['created_at'], 'role': r['role'], 'event': r['event_id'], 'act': {'edit': True},
                    **({'quote': r['quote']} if r['quote'] else {})})
        wanted.add(r['event_id'])
    for r in db.execute('SELECT old_role,new_role,created_at FROM role_corrections WHERE identifier IN (SELECT value FROM json_each(?)) ORDER BY created_at DESC LIMIT 3', (ids,)):
        out.append({'kind': 'role_fix', 'at': r['created_at'], 'role': r['new_role'], 'was': r['old_role']})


def _person(db, row, ids, out, wanted):
    node_id = row['id']
    _roles(db, ids, out, wanted)
    r = db.execute("SELECT org,org_id,source,via,event_id,created_at FROM person_orgs WHERE identifier IN (SELECT value FROM json_each(?)) AND source!='owner' AND org!='' "
                   'ORDER BY created_at DESC LIMIT 1', (ids,)).fetchone()
    if r:
        out.append({'kind': 'org', 'at': r['created_at'], 'org': r['org'], 'org_id': r['org_id'], 'event': r['event_id'], 'via': r['via'],
                    'act': {'edit': True}})
        wanted.add(r['event_id'])
    for r in db.execute("SELECT g.a,g.b,g.relation,g.event_id,g.created_at,x.name AS a_name,y.name AS b_name FROM graph_relations g "
                        "LEFT JOIN graph_nodes x ON x.id=g.a LEFT JOIN graph_nodes y ON y.id=g.b "
                        "WHERE g.source!='owner' AND g.relation!='' AND (g.a IN (SELECT value FROM json_each(?)) OR g.b IN (SELECT value FROM json_each(?))) ORDER BY g.created_at DESC LIMIT 5", (ids, ids)):
        if r['a_name'] and r['b_name']:
            out.append({'kind': 'relation', 'at': r['created_at'], 'a_name': r['a_name'], 'b_name': r['b_name'], 'relation': r['relation'],
                        'event': r['event_id'], 'act': {'unrelate': [r['a'], r['b']]}})
            wanted.add(r['event_id'])
    try:
        import graph
        for r in db.execute("SELECT a,b,created_at FROM graph_merges WHERE same=1 AND coalesce(source,'agent')!='owner' "
                            'AND a IN (SELECT value FROM json_each(?)) AND b IN (SELECT value FROM json_each(?)) ORDER BY created_at DESC LIMIT 5', (ids, ids)):
            other = r['b'] if r['a'] == node_id else r['a']
            out.append({'kind': 'joined', 'at': r['created_at'], 'shown': graph.shown_id(other, {}), 'act': {'split': [r['a'], r['b']]}})
    except sqlite3.OperationalError:
        pass  # an older graph_merges without its source column
    r = db.execute('SELECT after,at FROM side_changes WHERE node_id=? ORDER BY at DESC LIMIT 1', (node_id,)).fetchone()
    info = _json(row['info'], {})
    if r and r['after'] in ('work', 'personal') and info.get('side') == r['after'] and info.get('side_by') != 'owner':
        out.append({'kind': 'side', 'at': r['at'], 'side': r['after'], 'act': {'edit': True}})


def _org(db, row, ids, out, wanted):
    _roles(db, ids, out, wanted)
    for r in db.execute("SELECT p.identifier,p.via,p.event_id,p.created_at,n.id AS person,n.name FROM person_orgs p JOIN graph_nodes n "
                        "ON n.kind='person' AND (n.id=p.identifier OR EXISTS (SELECT 1 FROM json_each(n.info,'$.identifiers') j WHERE j.value=p.identifier)) "
                        "WHERE p.source!='owner' AND (p.org_id=? OR (p.org_id IS NULL AND p.org=? COLLATE NOCASE)) ORDER BY p.created_at DESC LIMIT 5",
                        (row['id'], row['name'])):
        out.append({'kind': 'member', 'at': r['created_at'], 'person': r['person'], 'name': r['name'], 'event': r['event_id'], 'via': r['via']})
        wanted.add(r['event_id'])


def _project(db, row, out, wanted):
    project_id = str(row['id']).split(':', 1)[1]
    now = db.execute('SELECT stage,stage_by FROM projects WHERE id=?', (project_id,)).fetchone()
    moves = db.execute('SELECT id,board_id,stage,reason,event_id,source,at FROM project_moves WHERE project_id=? ORDER BY at,id',
                       (project_id,)).fetchall()
    for i, m in enumerate(moves):
        if m['source'] == 'owner':
            continue
        item = {'kind': 'move', 'at': m['at'], 'stage': m['stage'], 'event': m['event_id']}
        before = next((p for p in reversed(moves[:i]) if p['board_id'] == m['board_id']), None)
        latest = i == len(moves) - 1
        if latest and before and now and now['stage'] == m['stage'] and now['stage_by'] != 'owner' and before['stage'] != m['stage']:
            item['act'] = {'stage': before['stage']}  # Undo: back where it was, as the owner's own move
        out.append(item)
        wanted.add(m['event_id'])
    try:
        done = db.execute("SELECT marked_at,evidence_event_id FROM project_success WHERE project_id=? AND marked_by='evidence'", (project_id,)).fetchone()
    except sqlite3.OperationalError:
        done = None  # no project_success yet
    if done and done['marked_at']:
        import graph
        project = db.execute('SELECT * FROM projects WHERE id=?', (project_id,)).fetchone()
        item = {'kind': 'done', 'at': done['marked_at'], 'event': done['evidence_event_id'], 'deal': __import__('project_success').is_deal(db, project)}
        if project['outcome'] == 'won':
            item['act'] = {'reopen': row['id']}  # Undo: open again, as the owner's own Reopen
        out.append(item)
        wanted.add(done['evidence_event_id'])


def _facts(db, ids, out):
    rows = db.execute("SELECT f.id,f.text,f.created_at,f.source,f.suggestion_id,s.title FROM facts f LEFT JOIN suggestions s ON s.id=f.suggestion_id "
                      "WHERE f.removed_at IS NULL AND f.kind='fact' "
                      'AND EXISTS (SELECT 1 FROM fact_about a WHERE a.fact_id=f.id AND a.removed_at IS NULL AND a.node_id IN (SELECT value FROM json_each(?))) '
                      'AND NOT EXISTS (SELECT 1 FROM fact_about a WHERE a.fact_id=f.id AND a.removed_at IS NOT NULL AND a.node_id IN (SELECT value FROM json_each(?))) '
                      'ORDER BY f.created_at DESC LIMIT ?', (ids, ids, LIMIT)).fetchall()
    for r in rows:
        was = db.execute("SELECT text FROM facts WHERE merged_into=? AND kind='fact' ORDER BY created_at DESC LIMIT 1", ('fact:' + str(r['id']),)).fetchone()
        source = str(r['source'] or '')
        src = {'type': 'ai', 'name': source[3:][:60]} if source.startswith('ai:') else \
            {'type': 'note', 'card': r['suggestion_id'], 'title': str(r['title'] or '')[:120]} if r['suggestion_id'] else {'type': 'note'}
        out.append({'kind': 'fact', 'at': r['created_at'], 'text': r['text'], 'fact': r['id'], 'source': src,
                    **({'was': was['text']} if was and was['text'] != r['text'] else {})})


def _ai(db, node_id, out):
    """A connected AI's changes to the record itself (its facts are under facts), with Undo while it still applies."""
    for r in db.execute("SELECT w.id,w.tool,w.at,w.undone_at,w.changes,c.name FROM ai_writes w LEFT JOIN ai_connections c ON c.id=w.connection_id "
                        "WHERE w.node_id=? AND w.waiting=0 AND w.tool IN ('update_record','add_summary_line') ORDER BY w.at DESC LIMIT 5", (node_id,)):
        parts = sorted({c.get('part') for c in _json(r['changes'], []) if isinstance(c, dict) and c.get('part') in ('details', 'crm', 'summary')})
        if parts:
            out.append({'kind': 'ai', 'at': r['at'], 'parts': parts, 'source': {'type': 'ai', 'name': str(r['name'] or '')[:60]},
                        **({'undone': True} if r['undone_at'] else {'act': {'ai_undo': r['id']}})})


def recent(db, row, limit=LIMIT):
    """[{'kind', 'at', …, 'source', 'act'}] for a person's, organization's or project's page, newest first. kind:
    role, role_fix, org, member, relation, joined, side, move, done, fact, ai. source: {'type': 'event', 'id', 'via',
    'from' or 'mine'}, {'type': 'note', 'card', 'title'}, {'type': 'ai', 'name'}, {'type': 'quote', 'text'} (the line a role was
    read in, when its message isn't at hand) or {'type': 'line', 'via'}. act: what
    the page's own correction for it needs (edit, unrelate, split, stage, reopen, ai_undo); none when there is nothing to undo."""
    if not row or row['kind'] not in ('person', 'org', 'project'):
        return []
    info = _json(row['info'], {})
    # its ids as one JSON list, bound to each json_each(?): every query stays a fixed string
    ids = json.dumps(list(dict.fromkeys([row['id'], *(info.get('identifiers') or [])])))
    out, wanted = [], set()
    steps = [lambda: _facts(db, ids, out), lambda: _ai(db, row['id'], out)]
    if row['kind'] == 'person':
        steps.insert(0, lambda: _person(db, row, ids, out, wanted))
    elif row['kind'] == 'org':
        steps.insert(0, lambda: _org(db, row, ids, out, wanted))
    else:
        steps.insert(0, lambda: _project(db, row, out, wanted))
    for step in steps:
        try:
            step()
        except sqlite3.OperationalError:
            continue  # a bare graph without the assistant's tables (tests, an older database): what can be read still shows
    events = _events(db, wanted)
    for item in out:
        if 'event' in item or 'via' in item:
            src = _source(events, item.pop('event', None), item.pop('via', None))
            if src:
                item['source'] = src
        if 'quote' in item:  # the line it was read in, when its message isn't at hand
            quote = item.pop('quote')
            item.setdefault('source', {'type': 'quote', 'text': quote})
    out = [x for x in out if x.get('at')]
    out.sort(key=lambda x: str(x['at']), reverse=True)
    return out[:limit]

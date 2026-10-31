"""Fix it where it came from (docs/intelligence.md#fixed-at-the-source): when the owner corrects something in a to-do's
chat ("she's not the CEO", "we don't use that template anymore", "he left the company"), the chat turn looks up where
The Machine got the wrong thing from (sources) and fixes it there (fix), instead of only adding a rule on top of it.

Where it can come from, and how it is fixed, as the owner's own word (so a later review can't put it back):
- fact: a fact or draft rule under What I've learned, reworded or removed;
- role: what someone (or an organization) is to the owner, from a review (graph.set_role; the correction is kept in
  role_corrections, so later reviews learn from it);
- org: where someone works, from a signature, a headline or a look-up (graph.set_org; empty: they're not there anymore);
- title, location: a person's job title or place from a connector or a look-up (graph.person_edit, the owner's edit wins);
- stage: where a project stands on its board (graph.set_stage);
- project: which project the to-do is for (graph.set_card_project).
A GBrain page's section The Machine writes follows the Graph and What I've learned, so it changes with the next sync;
what the owner wrote on that page stays as they wrote it. A skill changes through a skill update the owner approves.

Every fix is kept in learning_changes (kind 'source') with what it replaced, so it shows in the to-do's chat as a quiet
line ("Fixed: Ana's role is Head of Sales, from her email signature") and under What I've learned, Recent changes, with
Undo. An undo puts back exactly what was there, unless that changed again since (the owner's later edit wins). A note
fixed at the source is no signal for the learning loop any more: it adds no rule on top."""
from __future__ import annotations

import json

import graph
import learning_loop

# The rule a to-do's preparation and chat turns get (assistant.preparation_prompt, chat_prompt).
PROMPT = ('When the owner\'s note says something The Machine has is wrong ("she\'s not the CEO", "he left the company", "we don\'t use that '
          'template anymore", "that\'s not part of the Acme deal"), fix it where it came from first: assistant_signals correction_sources args '
          'suggestion_id, words=<the wrong claim\'s key words> (node_ids=[...] for someone not on this to-do) lists the people, organizations and '
          'projects on it with their role, organization, title, place and stage and where each came from, the facts and rules that mention it, '
          'The Machine\'s GBrain pages and the skills that mention it. Then fix the one it came from: assistant_signals fix_source args '
          'suggestion_id, decision_id=<that note\'s id>, kind and target as that item\'s fix says, value=<what is right, from their note; empty '
          'removes a fact or rule, a role, an organization or the to-do\'s project>, came_from=<where the wrong one came from, a few words in '
          'their language, like "her email signature">. The chat shows each fix with Undo by itself: don\'t also save a fact or rule that says '
          'the same, and the reply says in one line what was wrong and that it is fixed. The Machine\'s part of a GBrain page follows by itself; '
          'what the owner wrote on a GBrain page stays theirs, so name that page in the reply. A wrong skill gets an update they approve '
          '(assistant skills-propose --update <skill> --job <job id>). Only when no source says it, save a fact or rule as usual.')
KINDS = ('fact', 'role', 'org', 'title', 'location', 'stage', 'project')
GRAPH_KINDS = ('role', 'org', 'title', 'location', 'stage', 'project')
FROM_CHARS, VALUE_CHARS = 80, 120
PER_NOTE = 5          # fixes from one note
SOURCES_MAX = 12      # facts, skills and GBrain notes listed by sources


def _clip(text, n):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= n else text[:n - 1] + '…'


def _rows(db, sql, args=()):
    try:
        return [dict(r) for r in db.execute(sql, args)]
    except Exception:
        return []


def _note(db, suggestion_id, decision_id):
    """The owner's own written note on this to-do: a fix needs one, like a learned fact."""
    row = db.execute("SELECT d.id,s.title,s.event_ids FROM decisions d JOIN suggestions s ON s.id=d.suggestion_id WHERE d.id=? AND d.suggestion_id=? "
                     "AND d.source IN ('telegram','dashboard') AND d.feedback!='' AND d.id NOT IN (SELECT decision_id FROM decision_annotations)",
                     (str(decision_id or ''), str(suggestion_id or ''))).fetchone()
    if not row:
        raise ValueError("A fix comes from the owner's own note on this to-do: give its suggestion_id and decision_id")
    return row


def _node(db, node_id, kinds):
    row = db.execute(f"SELECT id,kind,name,info FROM graph_nodes WHERE id=? AND kind IN ({','.join('?' for _ in kinds)})",
                     (str(node_id or ''), *kinds)).fetchone()
    if not row:
        raise ValueError(f"target is a {' or '.join(kinds)} node_id from sources or graph")
    return row, json.loads(row['info'] or '{}')


def _snap(db, table, where, args):
    return sorted(_rows(db, f'SELECT * FROM {table} WHERE {where}', args), key=lambda r: json.dumps(r, sort_keys=True, default=str))


def _ids(row, info):
    return list(dict.fromkeys([row['id'], *(info.get('identifiers') or [])]))


def _where_ids(ids):
    return f"identifier IN ({','.join('?' for _ in ids)})"


# What a fix says, as whole sentences the dashboard translates (window.t), slots filled in order.
def _line(key, *args):
    return [key, *[str(a) for a in args]]


def _english(line, plain=''):
    if not line:
        return plain
    text = line[0]
    for value in line[1:]:
        text = text.replace('{}', value, 1)
    return text


def _event_via(db, event_id):
    found = db.execute('SELECT kind,occurred_at FROM events WHERE id=?', (event_id,)).fetchone() if event_id else None
    return f"{graph.VIA.get(found['kind'], found['kind'].split('.')[0])} on {str(found['occurred_at'])[:10]}" if found else None


# ------------------------------------------------------------------------------------------------ where it came from

def sources(db, suggestion_id, words='', node_ids=None):
    """Where what The Machine knows about this to-do comes from: the people, organizations and projects on it (or the
    node_ids given) with their role, organization, title and place and where each came from, the to-do's project and
    its stage, the facts and rules that mention words or are about them, The Machine's GBrain pages for them, and skills
    that mention words. Each item that can be fixed says how (fix: kind and target)."""
    card = db.execute('SELECT id,title,event_ids,project,project_by FROM suggestions WHERE id=?', (str(suggestion_id or ''),)).fetchone()
    if not card:
        raise ValueError('Unknown to-do')
    words = [w for w in (_clip(words, 200).casefold().split()) if len(w) > 2][:8]
    if node_ids:
        ids = [str(n) for n in (node_ids if isinstance(node_ids, list) else [node_ids])][:8]
        rows = [r for r in (db.execute('SELECT * FROM graph_nodes WHERE id=?', (i,)).fetchone() for i in ids) if r]
    else:
        try:
            rows = list(graph.for_events(db, json.loads(card['event_ids'] or '[]')))[:8]
        except (ValueError, TypeError):
            rows = []
    people, projects = [], [i for i in (ids if node_ids else []) if i.startswith('project:')]
    for row in rows:
        info = json.loads(row['info'] or '{}')
        if row['kind'] in ('person', 'org'):
            item = {'node_id': row['id'], 'kind': row['kind'], 'name': row['name']}
            role = db.execute('SELECT * FROM person_roles WHERE identifier=?', (info.get('role_id') or row['id'],)).fetchone()
            if info.get('role'):
                said = ('the owner' if info.get('role_by') == 'owner' else 'a review') + (
                    f" from {_event_via(db, role['event_id'])}" if role and role['event_id'] else '') + (f': "{role["quote"]}"' if role and role['quote'] else '')
                item['role'] = {'value': info['role'], 'came_from': said, 'fix': {'kind': 'role', 'target': row['id']}}
            if row['kind'] == 'person':
                if info.get('org'):
                    org = db.execute('SELECT name FROM graph_nodes WHERE id=?', (info['org'],)).fetchone()
                    item['org'] = {'value': org['name'] if org else info['org'], 'came_from': ('the owner' if info.get('org_by') == 'owner' else
                                   info.get('org_via') or 'their email address'), 'fix': {'kind': 'org', 'target': row['id']}}
                profile = info.get('profile') or {}
                for field in ('title', 'location'):
                    if profile.get(field):
                        by = ((profile.get('sources') or {}).get(field) or {}).get('from') or 'a look-up'
                        item[field] = {'value': profile[field], 'came_from': by, 'fix': {'kind': field, 'target': row['id']}}
            people.append(item)
        elif row['kind'] == 'project':
            projects.append(row['id'])
    if card['project']:
        found = db.execute('SELECT id FROM projects WHERE name=? COLLATE NOCASE', (card['project'],)).fetchone()
        if found:
            projects.insert(0, 'project:' + str(found['id']))
    out_projects = []
    for node_id in dict.fromkeys(projects):
        p = db.execute('SELECT p.*,b.name board FROM projects p LEFT JOIN boards b ON b.id=p.board_id WHERE p.id=?', (node_id.split(':', 1)[1],)).fetchone()
        if p:
            item = {'node_id': node_id, 'name': p['name']}
            if p['stage']:
                item['stage'] = {'value': p['stage'], 'board': p['board'], 'came_from': 'the owner' if p['stage_by'] == 'owner' else
                                 'a review' + (f": {p['stage_reason']}" if p['stage_reason'] else ''), 'fix': {'kind': 'stage', 'target': node_id}}
            out_projects.append(item)
    about = [p['node_id'] for p in people] + [p['node_id'] for p in out_projects]
    facts = []
    for f in _rows(db, 'SELECT f.id,f.kind,f.text,s.title FROM facts f LEFT JOIN suggestions s ON s.id=f.suggestion_id WHERE f.removed_at IS NULL '
                       'ORDER BY f.created_at DESC LIMIT 300'):
        if any(w in f['text'].casefold() for w in words) or f['id'] in _about(db, about):
            facts.append({'id': f['id'], 'what': 'rule' if f['kind'] == 'draft' else f['kind'], 'text': f['text'],
                          'came_from': f'a note on "{_clip(f["title"], 80)}"' if f['title'] else 'a note', 'fix': {'kind': 'fact', 'target': f['id']}})
    out = {'to_do': {'title': card['title'], 'project': card['project'], 'project_by': card['project_by'] or None,
                     'fix': {'kind': 'project', 'target': card['id']}},
           'people': people, 'projects': out_projects, 'facts': facts[:SOURCES_MAX]}
    pages = _rows(db, f"SELECT p.node_id,p.slug,p.state,n.text FROM gbrain_pages p LEFT JOIN gbrain_notes n ON n.node_id=p.node_id "
                      f"WHERE p.node_id IN ({','.join('?' for _ in about) or 'NULL'}) OR p.node_id='the-machine:learnings'", about)
    if pages:
        out['gbrain'] = [{'slug': p['slug'], 'the_machine_section': 'follows the Graph and What I\'ve learned: fix those' if p['state'] == 'synced'
                          else 'the owner changed or removed it: theirs now', **({'owner_text': p['text']} if p['text'] else {})} for p in pages][:SOURCES_MAX]
    skills = [s for s in _rows(db, "SELECT id,name,origin,description,body FROM skills WHERE status='on'")
              if words and any(w in f"{s['name']} {s['description']} {s['body']}".casefold() for w in words)]
    if skills:
        out['skills'] = [{'skill': s['id'], 'name': s['name'], 'written_by_owner': s['origin'] == 'mine'} for s in skills][:SOURCES_MAX]
    return out


def _about(db, node_ids):
    if not node_ids:
        return set()
    return {r[0] for r in db.execute(f"SELECT fact_id FROM fact_about WHERE removed_at IS NULL AND node_id IN ({','.join('?' for _ in node_ids)})", node_ids)} \
        if db.execute("SELECT 1 FROM sqlite_master WHERE name='fact_about'").fetchone() else set()


# ------------------------------------------------------------------------------------------------ the fix

def _state(db, kind, target):
    """What a fix compares and puts back: the rows behind the value, never more."""
    if kind == 'fact':
        row = db.execute('SELECT text,removed_at IS NOT NULL removed FROM facts WHERE id=?', (int(target['id']),)).fetchone()
        return {'text': row['text'], 'removed': bool(row['removed'])} if row else None
    if kind == 'role':
        return {'rows': _snap(db, 'person_roles', _where_ids(target['ids']), target['ids'])}
    if kind == 'org':
        return {'rows': _snap(db, 'person_orgs', 'identifier=?', (target['id'],))}
    if kind in ('title', 'location'):
        return {'rows': _snap(db, 'person_edits', 'identifier=?', (target['id'],))}
    if kind == 'stage':
        row = db.execute('SELECT board_id,stage,stage_reason,stage_event_id,stage_by,stage_at,outcome,outcome_reason FROM projects WHERE id=?',
                         (int(target['id'].split(':', 1)[1]),)).fetchone()
        return dict(row) if row else None
    if kind == 'project':
        row = db.execute('SELECT project,project_by FROM suggestions WHERE id=?', (target['id'],)).fetchone()
        return dict(row) if row else None
    return None


def _same(kind, a, b):
    """Is it still what the fix left? Compared on what says the value (a review's later re-read of the same role is fine)."""
    if kind in ('role', 'org'):
        keys = ('identifier', 'role', 'org', 'source')
        pick = lambda s: [{k: r.get(k) for k in keys} for r in (s or {}).get('rows', [])]
        return pick(a) == pick(b)
    if kind == 'stage':
        pick = lambda s: {k: (s or {}).get(k) for k in ('board_id', 'stage', 'stage_by')}
        return pick(a) == pick(b)
    return a == b


def fix(db, suggestion_id, decision_id, kind, target, value, came_from, now):
    """Fix one wrong thing where it lives, from the owner's note (decision_id) on this to-do. value is what is right
    ('' takes it away, for a fact, a role, an organization or the to-do's project). came_from: where the wrong one came
    from, in a few words in the owner's language ("her email signature"). Returns the change id and its line."""
    learning_loop.ensure(db)
    if not db.in_transaction:
        db.execute('BEGIN IMMEDIATE')
    _note(db, suggestion_id, decision_id)
    if kind not in KINDS:
        raise ValueError('kind is where the wrong thing lives: ' + ', '.join(KINDS))
    if db.execute("SELECT count(*) FROM learning_changes WHERE kind='source' AND run_id=?", ('fix:' + str(decision_id),)).fetchone()[0] >= PER_NOTE:
        raise ValueError(f'At most {PER_NOTE} fixes from one note')
    value = ' '.join(str(value if value is not None else '').split())
    came_from = _clip(came_from, FROM_CHARS) or None
    if kind == 'fact':
        if not str(target or '').isdigit():
            raise ValueError('target is the fact or rule id from sources')
        row = db.execute('SELECT id,kind,text FROM facts WHERE id=? AND removed_at IS NULL', (int(target),)).fetchone()
        if not row:
            raise ValueError('That fact or rule is not current: see sources')
        if value and not 5 <= len(value) <= 240:
            raise ValueError('A fact is one short sentence (5-240 characters), or empty to remove it')
        if value == row['text']:
            return {'unchanged': True}
        if value and db.execute('SELECT 1 FROM facts WHERE removed_at IS NULL AND kind=? AND lower(text)=lower(?) AND id!=?', (row['kind'], value, row['id'])).fetchone():
            raise ValueError('That is already in what I’ve learned: remove this one instead (value empty)')
        where, old = {'id': row['id']}, row['text']
        before = _state(db, kind, where)
        learning_loop.set_fact(db, row['id'], value or old, None if value else now, str(row['id']))
        line = None if value else _line('Removed “{}” from what I’ve learned', _clip(old, 120))  # a reworded fact says it itself
    elif kind == 'project':
        if str(target or '') != str(suggestion_id):
            raise ValueError("target is this to-do's suggestion_id")
        where = {'id': str(suggestion_id)}
        before = _state(db, kind, where)
        old = before['project']
        name = (graph.set_card_project(db, suggestion_id, value) or {}).get('name')
        if (name or '') == (old or '') and before['project_by'] == 'owner':
            return {'unchanged': True}
        line = _line('Moved this to-do to {}', name) if name else _line('Took this to-do off {}', old) if old else _line('This to-do has no project')
    elif kind == 'stage':
        if not str(target or '').startswith('project:') or not value:
            raise ValueError('target is a project node_id (project:…) and value its right stage')
        where = {'id': str(target)}
        before = _state(db, kind, where)
        if before is None:
            raise ValueError('Unknown project')
        moves = db.execute('SELECT coalesce(max(id),0) FROM project_moves').fetchone()[0]
        said = graph.set_stage(db, str(target), value, 'owner', now)
        if said.get('stage') == before['stage'] and before['stage_by'] == 'owner':
            return {'unchanged': True}
        where['moves'], old = moves, before['stage']
        line = _line('{} moved to {}', said['project'], said['stage'])
    else:
        row, info = _node(db, target, ('person', 'org') if kind == 'role' else ('person',))
        where, name = {'id': row['id'], 'ids': _ids(row, info)}, row['name']
        before = _state(db, kind, where)
        if kind == 'role':
            old = info.get('role')
            corrections = db.execute('SELECT coalesce(max(id),0) FROM role_corrections').fetchone()[0]
            if len(value) > 60:
                raise ValueError('A role is a few words (up to 60 characters)')
            if not value and not old:
                return {'unchanged': True}
            if value and old and value.casefold() == old.casefold() and info.get('role_by') == 'owner':
                return {'unchanged': True}
            graph.set_role(db, row['id'], value, 'owner', now)
            where['corrections'] = corrections
            line = _line('{}’s role is {}', name, value) if value else _line('Removed {}’s role', name)
        elif kind == 'org':
            org = db.execute('SELECT name FROM graph_nodes WHERE id=?', (info.get('org'),)).fetchone() if info.get('org') else None
            old = org['name'] if org else None
            if not value and not old:
                return {'unchanged': True}
            graph.set_org(db, row['id'], value, 'owner', now)
            shown = db.execute('SELECT org FROM person_orgs WHERE identifier=?', (row['id'],)).fetchone()
            line = _line('{} works at {}', name, shown['org']) if value else _line('{} no longer works at {}', name, old)
        else:  # title, location: the owner's own detail, over what a connector or a look-up said
            old = (info.get('profile') or {}).get(kind)
            if not value or len(value) > VALUE_CHARS:
                raise ValueError(f'value is their right {kind}, up to {VALUE_CHARS} characters')
            if old and value.casefold() == old.casefold():
                return {'unchanged': True}
            graph.person_edit(db, row['id'], {kind: value}, now)
            line = _line('{}’s title is {}', name, value) if kind == 'title' else _line('{} is based in {}', name, value)
    after = _state(db, kind, where)
    change = learning_loop.record(db, 'fix:' + str(decision_id), 'source',
                                  json.dumps({'type': kind, 'where': where, 'line': line, 'after': after, 'suggestion_id': str(suggestion_id)}),
                                  json.dumps({'text': old, 'state': before}), _english(line, value), came_from or '')
    return {'id': change, 'fixed': _english(line, value), **({'came_from': came_from} if came_from else {}), 'graph': kind in GRAPH_KINDS}


def undo(db, row):
    """Put back what one fix replaced (learning_loop.undo calls this for kind 'source'). Refused when it changed since."""
    target, before = json.loads(row['target']), json.loads(row['before'] or '{}')
    kind, where = target['type'], target['where']
    if not _same(kind, _state(db, kind, where), target['after']):
        raise ValueError('That changed since. Change it where it is now')
    old = before.get('state')
    if kind == 'fact':
        learning_loop.set_fact(db, where['id'], old['text'], row['at'] if old['removed'] else None, 'undo:' + str(row['id']))
    elif kind == 'role':
        graph.put_back_person_rows(db, 'person_roles', where['ids'], old['rows'])
        graph.drop_role_corrections(db, where['id'], where['corrections'])
    elif kind == 'org':
        graph.put_back_person_rows(db, 'person_orgs', [where['id']], old['rows'])
    elif kind in ('title', 'location'):
        graph.put_back_person_rows(db, 'person_edits', [where['id']], old['rows'])
    elif kind == 'stage':
        graph.put_back_stage(db, where['id'].split(':', 1)[1], old, where['moves'])
    elif kind == 'project':
        graph.put_back_card_project(db, where['id'], old['project'], old['project_by'])
    return {'graph': kind in GRAPH_KINDS}


def fixed_decisions(db):
    """Notes fixed at the source: the learning loop adds no rule on top of them."""
    return {r[0][4:] for r in db.execute("SELECT DISTINCT run_id FROM learning_changes WHERE kind='source' AND status='applied'")}


def chat_items(db, suggestion_id):
    """This to-do's fixes, for its chat: a quiet line each, with Undo while it holds (from the database, never a reply)."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='learning_changes'").fetchone():
        return []
    out = []
    for r in db.execute("SELECT c.* FROM learning_changes c JOIN decisions d ON 'fix:'||d.id=c.run_id WHERE c.kind='source' AND d.suggestion_id=? "
                        'ORDER BY c.at,c.id', (str(suggestion_id),)):
        target = json.loads(r['target'])
        out.append({'kind': 'fixed', 'id': r['id'], 'line': target.get('line'), 'text': r['after'], 'from': r['why'] or None,
                    'undone': r['status'] == 'undone', 'at': r['at']})
    return out

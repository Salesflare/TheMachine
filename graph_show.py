"""What the owner changes on a record shows on its page at once, in the transaction of the change, written as a Graph
build writes it: so the answer needs no whole build first (on a big Graph that is some 16-22 s). The rest of the Graph
follows in the graph worker's next build (App.graph_later)."""
from __future__ import annotations

import json

import enrichment
import graph


def show_person_edit(db, node_id, changed):
    """Put a Save from a person's page on their page at once, in the transaction of the save: their name, details,
    contacts, Type and organization as a build writes them, so the answer needs no whole build first (on a big Graph
    that held a Save some 16 s). The rest of the Graph (lists, Same person?, an organization's own page) follows in
    the graph worker's next build. changed: the fields the owner saved."""
    row = db.execute("SELECT id,strength,info FROM graph_nodes WHERE id=? AND kind='person'", (str(node_id or ''),)).fetchone()
    if not row:
        return
    info = json.loads(row['info'] or '{}')
    group = sorted(set(info.get('identifiers') or ()) | {row['id']})
    marks = ','.join('?' for _ in group)
    looked_up = {r[0]: r[1] for r in db.execute(
        f"SELECT identifier,profile FROM person_profiles WHERE status='found' AND profile IS NOT NULL AND identifier IN ({marks})", group)}
    photos = {r[0]: r[1] for r in db.execute(f'SELECT identifier,key FROM person_photos WHERE identifier IN ({marks})', group)}
    edited = graph.person_edits_for(db, group)
    profile, contacts = graph.person_shown(group, edited, looked_up, enrichment.people_facts(db, ids=group), photos)
    info.update(profile=profile, edited=sorted(edited), notes=edited.get('notes'), **contacts)
    if edited.get('side'):
        info.update(side=edited['side'], side_by='owner', side_why='owner')
    elif 'side' in changed:
        info['side_by'] = None  # back to what The Machine knows of them: the next build works that out
    if 'org' in changed:
        said = db.execute('SELECT org,org_id,said_at FROM person_orgs WHERE identifier=?', (row['id'],)).fetchone()
        org = said['org'] if said else ''
        db.execute("DELETE FROM graph_links WHERE a=? AND kind='member'", (row['id'],))
        org_id = None
        if org:
            org_id = said['org_id'] if said['org_id'] and db.execute('SELECT 1 FROM graph_nodes WHERE id=?', (said['org_id'],)).fetchone() else None
            folded = graph.folded_words(org)
            org_id = org_id or next((r[0] for r in db.execute("SELECT id,name FROM graph_nodes WHERE kind='org' ORDER BY strength DESC")
                                     if graph.folded_words(r[1]) == folded), None)
            if org_id:
                db.execute('INSERT OR REPLACE INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,?,?,NULL)', (row['id'], org_id, 'member', row['strength']))
            else:  # a new organization stands once the build makes it; its name shows on their page meanwhile
                org_id = 'org:named:' + '-'.join(folded.split())[:80]
        info.update(org=org_id, org_by='owner' if org_id else None, org_name=org or None, org_via=None, org_event_id=None,
                    org_at=said['said_at'] if org else None)
    db.execute('UPDATE graph_nodes SET info=? WHERE id=?', (json.dumps(info), row['id']))
    if 'name' in changed:
        named = db.execute('SELECT name FROM graph_names WHERE node_id=?', (row['id'],)).fetchone()
        if named:  # an empty name gives back the one from their messages: the next build reads it
            db.execute('UPDATE graph_nodes SET name=? WHERE id=?', (named['name'][:200], row['id']))


def show_org_edit(db, node_id):
    """An organization's page after the owner's details, name, picture or "wrong company", as a build writes it."""
    row = db.execute("SELECT id,info FROM graph_nodes WHERE id=? AND kind='org'", (str(node_id or ''),)).fetchone()
    if not row:
        return
    info = json.loads(row['info'] or '{}')
    domain = info.get('domain')
    got = db.execute('SELECT fields FROM org_edits WHERE domain=?', (domain or row['id'],)).fetchone()
    edits = json.loads(got['fields']) if got else {}
    if domain:
        found = db.execute('SELECT profile,status FROM org_profiles WHERE domain=?', (domain,)).fetchone()
        wrong = bool(found and found['status'] == 'wrong')
        looked = enrichment.usable(domain, json.loads(found['profile'])) if found and found['profile'] and not wrong else None
        profile = {'website': enrichment.website(domain), **(looked or {}), **edits}
        logo = db.execute('SELECT key FROM person_photos WHERE identifier=?', ('logo:' + domain,)).fetchone()
        if 'logo' not in profile and logo:  # no logo from the lookup or the owner: the one from its own site
            profile['logo'] = 'api/person-photo?p=' + logo[0]
        info.update(profile=profile, wrong=wrong)
    else:
        info['profile'] = edits or None
    info['edited'] = sorted(edits)
    db.execute('UPDATE graph_nodes SET info=? WHERE id=?', (json.dumps(info), row['id']))
    show_name(db, row['id'])


def show_name(db, node_id):
    """A name the owner gave a person, organization or project, on its node. An emptied one (back to the name from
    their messages) waits for the build that works it out."""
    node_id = str(node_id or '')
    if node_id.startswith('project:'):
        named = db.execute('SELECT name FROM projects WHERE id=?', (node_id.split(':', 1)[1],)).fetchone()
    else:
        named = db.execute('SELECT name FROM graph_names WHERE node_id=?', (node_id,)).fetchone()
    if named:
        db.execute('UPDATE graph_nodes SET name=? WHERE id=?', (named[0][:200], node_id))


def show_rename(db, node_id, done):
    """After graph.rename: the new name on its node; a project renamed into another one is that one from now on (its
    people and links go along)."""
    if done.get('merged'):
        old, new = str(node_id), done['node_id']
        db.execute('UPDATE OR IGNORE graph_links SET b=? WHERE b=?', (new, old))
        db.execute('UPDATE OR IGNORE graph_links SET a=? WHERE a=?', (new, old))
        db.execute('DELETE FROM graph_links WHERE a=? OR b=?', (old, old))
        db.execute('DELETE FROM graph_nodes WHERE id=?', (old,))
        return
    if db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind='person'", (str(node_id),)).fetchone():
        show_person_edit(db, node_id, {'name'})
    else:
        show_name(db, node_id)


def show_new_record(db, done, kind):
    """A person or organization the owner just added (graph.create_record) on its own page at once, as a build adds
    one with no messages yet: their name, address and organization, or its website."""
    if not done.get('created'):
        return
    node_id, name = done['node_id'], done['name']
    if kind == 'org':
        domain = None if node_id.startswith('org:named:') else node_id[4:]
        info = {'domain': domain, 'role': None, 'role_by': None, 'paying': False, 'edited': [], 'wrong': False, 'manual': True,
                'profile': {'website': enrichment.website(domain)} if domain else None, **({} if domain else {'stated': True})}
        db.execute('INSERT OR REPLACE INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,?,?,?,NULL,0,NULL,0,NULL,?)',
                   (node_id, 'org', name[:200], 0, json.dumps(info)))
        show_org_edit(db, node_id)
        return
    info = {'ids': [] if node_id.startswith('manual:') else [graph.shown_id(node_id, {})], 'org': None, 'org_by': None, 'has_headline': False,
            'wrote': 0, 'heard': 0, 'met': 0, 'accounts': [], 'next_meeting': None, 'colleague': False, 'role': None, 'role_by': None,
            'role_id': None, 'identifiers': [node_id], 'hints': [], 'seen_only': True, 'profile': None, 'edited': [], 'side': None,
            'side_by': None, 'side_why': None, 'manual': True, 'notes': None, 'emails': [], 'phones': []}
    db.execute('INSERT OR REPLACE INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,?,?,?,NULL,0,NULL,0,NULL,?)',
               (node_id, 'person', name[:200], graph.FLOOR, json.dumps(info)))
    if db.execute('SELECT 1 FROM person_orgs WHERE identifier=?', (node_id,)).fetchone():
        show_person_edit(db, node_id, {'org'})
    else:
        show_person_edit(db, node_id, set())
        domain = node_id.rsplit('@', 1)[1] if node_id.startswith('email:') else None
        if domain and db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind='org'", ('org:' + domain,)).fetchone():  # their work address says it
            db.execute("INSERT OR REPLACE INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,'member',?,NULL)", (node_id, 'org:' + domain, graph.FLOOR))
            db.execute("UPDATE graph_nodes SET info=json_set(info,'$.org',?,'$.org_by','email') WHERE id=?", ('org:' + domain, node_id))


def show_relation(db, a, b):
    """A relation the owner took off (graph.relate with no relation), off both their pages."""
    for node in (str(a), str(b)):
        row = db.execute('SELECT info FROM graph_nodes WHERE id=?', (node,)).fetchone()
        if row:
            info = json.loads(row['info'] or '{}')
            info['relations'] = [r for r in info.get('relations') or () if {r.get('a'), r.get('b')} != {str(a), str(b)}]
            db.execute('UPDATE graph_nodes SET info=? WHERE id=?', (json.dumps(info), node))
    db.execute("DELETE FROM graph_links WHERE kind='relation' AND ((a=? AND b=?) OR (a=? AND b=?))", (str(a), str(b), str(b), str(a)))


def show_project_save(db, done, args):
    """A project the owner saved (graph.save_project) on its page and its board at once: a new one gets its node, a
    renamed one its name, and the people on it are linked to it."""
    node, pid = done['node_id'], int(done['node_id'].split(':', 1)[1])
    project = db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    if not db.execute('SELECT 1 FROM graph_nodes WHERE id=?', (node,)).fetchone():
        info = {'closed_at': project['closed_at'], 'created_at': project['created_at'], 'probable': 0, 'board_id': project['board_id'],
                'stage': project['stage'], 'next_meeting': None}
        db.execute('INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES(?,?,?,0,NULL,0,NULL,0,NULL,?)',
                   (node, 'project', project['name'], json.dumps(info)))
    else:
        db.execute("UPDATE graph_nodes SET name=?,info=json_set(info,'$.board_id',?,'$.stage',?) WHERE id=?",
                   (project['name'], project['board_id'], project['stage'], node))
    if 'people' in args:
        for person in [str(x) for x in args.get('people') or [] if str(x).strip()]:
            db.execute("INSERT OR IGNORE INTO graph_links(a,b,kind,strength,last_at) VALUES(?,?,'project',?,NULL)", (person, node, graph.FLOOR))

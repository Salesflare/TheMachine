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

"""The organization a to-do is about (2026-11-10), for its chip: the one the review named on suggest (org), else its
project's organization when the owner or a review set it. Never one that only comes from where someone on it works:
their employer, or a project organization the Machine filled in from its people (graph.fill_orgs). No table: the
review's word is suggestions.org (machine/store/cards.py)."""
import re

import crm
import enrichment
import graph


def card_org(db, value):
    """The organization a to-do is about, from the review's word on suggest (org): its graph node id ("org:acme.com"),
    its web domain or its exact name in the Graph. '' when the review named none, or one the Graph doesn't know. Who is
    on the to-do never decides it: a person's employer is no reason to show their organization."""
    text = ' '.join(str(value or '').split())
    if not text:
        return ''
    if text.lower().startswith('org:'):
        ids = ['org:' + text[4:].lower()]
    else:
        domain = re.sub(r'^(?:https?://)?(?:www\.)?', '', text.lower()).split('/')[0]
        ids = ['org:' + domain] if graph.ORG_DOMAIN.fullmatch(domain) else []
        named = [r[0] for r in db.execute("SELECT id FROM graph_nodes WHERE kind='org' AND name=? COLLATE NOCASE LIMIT 2", (text,))]
        ids += named if len(named) == 1 else []
    for node in ids:
        node = crm.canonical(db, node)
        if db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind='org'", (node,)).fetchone():
            return node
    return ''


def card_org_view(db, node_id):
    """{'id', 'name'} of the organization a to-do is about (card_org), for its chip; None when it is gone since."""
    if not node_id:
        return None
    row = db.execute("SELECT id,name,info FROM graph_nodes WHERE id=? AND kind='org'", (crm.canonical(db, node_id),)).fetchone()
    return with_logo({'id': row['id'], 'name': row['name']}, row['info']) if row and row['name'] else None


def with_logo(org, info):
    """The organization's chip with its logo, when its Graph node shows one (enrichment.node_picture)."""
    logo = enrichment.node_picture(info, 'logo')
    return {**org, 'logo': logo} if logo else org


def project_org_view(db, project_node):
    """{'id', 'name'} of a to-do's project's organization (graph.card_project_view's node) when the owner or a review set
    it; None for one the Machine filled in from the project's people (that is only where they work) or none."""
    node = str((project_node or {}).get('node_id') or '')
    if not node.startswith('project:') or not node[8:].isdigit():
        return None
    row = db.execute('SELECT org,org_by FROM projects WHERE id=?', (int(node[8:]),)).fetchone()
    if not row or not row['org'] or row['org_by'] not in ('owner', 'review'):
        return None
    org = graph.project_org(db, row['org'])
    if not org or not org.get('id') or not org.get('name'):
        return None
    node = db.execute("SELECT info FROM graph_nodes WHERE id=? AND kind='org'", (org['id'],)).fetchone()
    return with_logo({'id': org['id'], 'name': org['name']}, node['info'] if node else None)

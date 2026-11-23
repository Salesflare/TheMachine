"""Whose a promise is, when its message has several people on it: a promise has a message and a name, no link to a person."""
import json
import re
import unicodedata


def of_others(db, node_id):
    """Ids of the promises on this person's messages that are someone else's: who is exactly another person on that
    message (their name or an address) and can't be this one. Anything less sure (a first name, a role, two people, a
    name nobody on the message has, an older name) stays with everyone on the message."""
    row = db.execute("SELECT name,info FROM graph_nodes WHERE id=? AND kind='person'", (node_id,)).fetchone()
    if not row:
        return set()  # a project or an organization has the promises of all its messages
    plain = lambda text: ' '.join(re.findall(r'\w+', unicodedata.normalize('NFKC', str(text or '')).casefold()))
    names = lambda key, name, info: {plain(name)} | {plain(str(i).partition(':')[2] or i) for i in (key, *(json.loads(info or '{}').get('identifiers') or ()))}
    mine, others = names(node_id, *row), {}
    for r in db.execute("SELECT p.id,p.who,n.id AS node,n.name,n.info FROM promises p JOIN graph_events g ON g.event_id=p.event_id JOIN graph_nodes n ON n.id=g.node_id "
                        "WHERE n.kind='person' AND n.id<>? AND p.event_id IN (SELECT event_id FROM graph_events WHERE node_id=?)", (node_id, node_id)):
        others.setdefault((r['id'], plain(str(r['who']).removeprefix('wa:'))), set()).update(names(r['node'], r['name'], r['info']))
    words = {w for name in mine for w in name.split()}
    own = lambda who: any(set(name.split()) <= set(who.split()) for name in mine if name) or set(who.split()) <= words
    return {pid for (pid, who), found in others.items() if who and who in found and not own(who)}

"""What the dashboard's requests work out from the sharing tables, kept between requests until one of those tables
changes (machine/stamps.py): the Fleet marks, the hash index and the sharing rules (shared_graph.Scope)."""
import copy
import datetime as dt
import json

import graph
from machine import stamps


# What sharing works out from on a person's page and the to-do list, kept between requests (machine/stamps.py):
# its tables carry change counters, so a kept answer is worked out again after any change to them
WATCHED = ('share_private', 'share_rules', 'share_threads', 'graph_nodes', 'projects', 'boards', 'board_suggestions', 'event_projects',
           'graph_events', 'slack_members', 'identity_names', 'team_records', 'team_sources')

# What a Scope is made from (besides the time and the Slack checkpoints, read again for each request: renewed). graph_who:
# graph_nodes without what each graph build rewrites (strength, profile, live: stamps.GRAPH_WHO), which a Scope never reads
SCOPE_TABLES = ('share_private', 'share_rules', 'share_threads', 'graph_who', 'projects', 'boards', 'board_suggestions',
                'event_projects', 'graph_events', 'slack_members', 'identity_names')
KEPT = stamps.Kept(16)  # what the dashboard's requests work out from the sharing tables (WATCHED), by stamp


def fleet_marks(db, fleets):
    """graph.fleet_marks: the Fleet members kept until the graph's people or the directory change (a pass over every
    person's addresses, asked on each person's page and graph list), the people found on the Network read each time (a
    setting and a table of their own; who in the graph has their addresses kept with the people). Its marks are shared
    by every caller: copy them before changing them."""
    at = stamps.stamp(db, ('graph_who',))
    members = KEPT.get(('marks', json.dumps(fleets, sort_keys=True, default=str)), at, lambda: graph.fleet_marks(db, fleets, network=False))
    # who in the graph has the addresses and numbers found on the Network: two passes over every person (some 90 ms on
    # a big graph, on each person's page, the Graph tab and its search), kept until the graph's people change
    return graph.network_marks(db, members, fleets, people=lambda addresses, numbers: KEPT.get(
        ('network people', tuple(addresses), tuple(numbers)), at, lambda: graph.people_by_email(db, addresses) + graph.people_by_phone(db, numbers)))


# The hashes of the last index made, {keys: {address or domain: its hash per key}}: an address hashes the same each time,
# so the next index (after any change to the graph's people, every few minutes) hashes only the new ones, not every
# address again (some 60k HMACs on a big graph: most of a person page's first open after a change)
_HASHED = {}


def hash_index(db, keys, keyed):
    """{hash: local node id} for these graph keys (SharedGraph.hash_index; keyed: shared_graph.keyed)."""
    keys = tuple(keys)
    index, before, hashed = {}, _HASHED.get(keys) or {}, {}
    for row in db.execute("SELECT id,kind,info FROM graph_nodes WHERE kind IN ('person','org')"):
        info = json.loads(row['info'] or '{}')
        values = (['email:' + i[6:].lower() for i in [row['id'], *info.get('identifiers', [])] if str(i).startswith('email:')]
                  if row['kind'] == 'person' else (['domain:' + info['domain']] if info.get('domain') else []))
        for v in values:
            if v not in hashed:
                hashed[v] = before.get(v) or tuple(keyed(key, v) for key in keys)
        for i in range(len(keys)):
            for v in values:
                index.setdefault(hashed[v][i], row['id'])
    _HASHED.clear()  # only the latest keys: a key changed or dropped takes its hashes along
    _HASHED[keys] = hashed
    return index


def renewed(scope, db, memo, hold, private=None):
    """A copy of this shared_graph.Scope for another request on its connection: what depends on the time (the hold on threads the
    review just called) and the Slack conversations (from the sync checkpoints, which change all the time) read again,
    and the parts worked out on demand left to work out again. memo: {thread: automated} shared by the scopes of
    one read-only request (automated_only); private: {unit: its answers}, the same for private_among."""
    out = copy.copy(scope)
    out._db, out._automated, out._team_items, out._private_events = db, None, None, None
    out._automated_memo = memo
    out._private_found, out._private_memo = {}, private  # read from the messages, which change all the time
    out.hold = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=hold)).isoformat(timespec='seconds')
    out.fresh = {r[0] for r in db.execute('SELECT thread FROM share_threads WHERE hand IS NULL AND sorted_at>?', (out.hold,))}
    out._slack_load(db)
    return out

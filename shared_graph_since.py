"""What a Team Graph publish reads again, and when it doesn't (shared_graph.graph_publish, docs/shared-graph.md).

A publish read the same rows every five minutes (every shared thread, the people, organizations and projects: tens of
megabytes and seconds a round on a big mailbox) to find that little or nothing had changed. Now:

- Nothing it reads changed since a round that sent everything: the same records and threads would go, so it reads
  nothing and sends nothing. What it reads is what its last collect read (shared_graph_apart.reading), by the change
  counters of those tables (machine/stamps.py); events, graph_nodes and graph_links by narrower ones that count only
  what a publish reads of them (not the review's bookkeeping on each message, nor a graph build's rewrite of every
  person's and link's strength). The digest also holds what the round hands the collect (accounts, keys, grants, what
  went before), the threads still in the hold, the Slack conversations shared with another company (from checkpoints)
  and the hour (what only time changes, such as this week's counts).
- Only the records' scores moved (a person's strength fades with time, so some move on every graph build): the records
  of the last round that read, with the new scores, are what reading again would give (rescored). Kept in memory only.
- Anything else, the daily snapshot, a round that could not send everything, a restart: it reads everything, as before.
- And it runs every half hour (PUBLISH_EVERY), not every round: sooner only when the round is forced or the owner's
  choices or a take-back ask for it (publish, choices).

Who gets what is decided by the same collect as before; this only skips reading when its answer can't have changed."""
import datetime as dt
import hashlib
import json
import sqlite3
import time

from machine import stamps
import shared_graph_apart as apart
import timeutil

PUBLISH_EVERY = 1800  # seconds: the read-and-publish part of a round (publish), unless forced or choices() moved
READ_AS = {'events': ('events_shared',), 'graph_nodes': ('graph_shared', 'graph_scores'), 'graph_links': ('links_shared',)}
NOT_COUNTED = frozenset({'sqlite_master', 'sqlite_schema', 'sqlite_temp_master', 'data_stamps', 'json_each', 'json_tree', 'checkpoints'})
SCORES = 'graph_scores'  # only the records' scores moved: rescored, not read again


def counted(read):
    """The change counters of the tables a collect read."""
    return sorted({c for t in read for c in READ_AS.get(t, (t,))} - NOT_COUNTED)


class _Slack:
    """Scope._slack_load on its own: the Slack conversations shared with another company, for inputs()."""

    def __init__(self, db, accounts):
        import shared_graph
        self.accounts = set(accounts)
        shared_graph.Scope._slack_load(self, db)


def inputs(db, counters, parts):
    """Digests of all a collect works from: the counters of the tables it read, what the round hands it (parts), the
    threads still in the hold, the Slack conversations shared with another company, and the hour. (all of it, all but
    the records' scores), or (None, None) when one of the tables has no counter here (then it reads every round)."""
    import shared_graph as sg
    at = stamps.stamp(db, counters) if counters else None
    if at is None:
        return None, None
    hold = (timeutil.clock() - dt.timedelta(seconds=sg.HOLD)).isoformat(timespec='seconds')
    fresh = sorted(r[0] for r in db.execute('SELECT thread FROM share_threads WHERE hand IS NULL AND sorted_at>?', (hold,)))
    slack = sorted(_Slack(db, parts['scope'][0]).slack_connect)
    rest = [parts, fresh, slack, timeutil.clock().strftime('%Y-%m-%dT%H')]
    n = dict(zip(sorted(set(counters)), at[1]))
    digest = lambda names: hashlib.sha256(sg.canon([[[c, n[c]] for c in names], rest])).hexdigest()
    return digest(sorted(n)), digest([c for c in sorted(n) if c != SCORES])


def rescored(db, found, top, secret):
    """found (a collect's) with each record's score as the graph has it now, when nothing else it read changed: the same
    as collecting again. None when who the records are could have changed: the people with the most strength
    (MAX_RECORDS) are not the same ones (top: those that collect looked at), or a record's node is gone. secret: what
    record ids are keyed with (a record's id is its node's, keyed)."""
    import shared_graph as sg
    now = [r[0] for r in db.execute("SELECT id FROM graph_nodes WHERE kind='person' ORDER BY strength DESC LIMIT ?", (sg.MAX_RECORDS,))]
    if sorted(now) != sorted(top):
        return None
    score = {sg.keyed(secret, 'record|' + r[0]): round(r[1], 3) for r in db.execute("SELECT id,strength FROM graph_nodes WHERE kind IN ('person','org','project')")}
    out = []
    for records, *rest in found:
        if any(rid not in score for rid in records):
            return None
        out.append(({rid: {**record, 'score': score[rid]} for rid, record in records.items()}, *rest))
    return out


def watch_reads(db, counters):
    """Counters for the tables a collect read that have none yet (stamps.watch), never on a virtual table (no triggers
    there: it stays uncounted, and the publish reads every round)."""
    plain = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND sql NOT LIKE 'CREATE VIRTUAL%'")}
    stamps.watch(db, [t for t in counters if t in plain])
    stamps.watch_graph_shared(db)


def collect(box, fleet, request, round_, state, due):
    """(the collect's answer as graph_publish uses it, what to keep once the round sent everything (kept()) or None), or
    (None, None) when nothing it reads changed since a round that did: then there is nothing to send. request: the
    collect's arguments (shared_graph_apart.collect); round_: what else of the round goes into what is sent (order: the
    grants and who has each, to, kv, learned: the team learnings); state: graph_out's; due: the daily snapshot goes this
    round (read in full)."""
    import shared_graph as sg
    digest = lambda value: hashlib.sha256(sg.canon(value)).hexdigest()
    parts = {'scope': [sorted(a) for a in request['scope']], 'keys': digest([*request['keys'], request['secret']]),
             'went': sorted(request['kept']), 'grants': [[[sorted(map(str, g[0])), sorted(map(str, g[1]))], m] for g, m in round_['order']],
             'to': round_['to'], 'kv': round_['kv'], 'learned': digest(round_['learned'])}
    reads = box.meta('graph_reads:' + fleet) or []
    with box.connect() as db:
        now, steady = inputs(db, reads, parts)
    if now and state.get('inputs') == now and not due:
        return None, None
    if state.get('inputs'):
        state['inputs'] = None  # it reads again now; until a round sends everything, every round does
        box.set_meta('graph_out:' + fleet, state)
    last = box.__dict__.setdefault('_graph_last', {}).pop(fleet, None)
    found = None
    if now and last and last['steady'] == steady and not due:
        with box.connect() as db:
            found = rescored(db, last['found'], last['top'], request['secret'])
        top = last['top']
    if found is None:
        # The reads themselves in a process of their own (shared_graph_apart.py): page requests don't wait on them
        found = apart.run(getattr(box.connect, '__self__', None), request['scope'], request['keys'], request['secret'], request['kept'],
                          request['grants'], reads=True)
        if found is None:  # where a child can't run: here, as before, and then read every round (apart.reading)
            with box.connect() as db:
                return apart.collect(db, request), None
        found, read, looked = found
        top = looked.get('top') or []
        if set(counted(read)) - set(reads):  # a table it hadn't read before: counted from now on, this round's not kept
            with box.connect() as db:
                watch_reads(db, counted(read))
            box.set_meta('graph_reads:' + fleet, sorted(set(reads) | set(counted(read))))
            now = None
    # as read, before graph_publish adds the team learnings to the records
    return found, ({'inputs': now, 'steady': steady, 'found': [(dict(r), *rest) for r, *rest in found], 'top': top} if now else None)


def choices(box, db, fleet):
    """What decides whether something that went must come back, read without a single message: the owner's choices (a
    thread's Team or Only you, Keep private, the sharing rules, who a board or thread is shared with, Only-you boards and
    projects and their messages, the connections that feed the Fleet), who is the owner's own life (Personal, Family,
    Friends), the company's and the owner's addresses, and the threads that went and are now kept back (the owner's Only
    you, or the review's call no longer client). (a digest of all of it, the tags of those threads)."""
    import graph
    import shared_graph as sg
    secret = box.graph_secret()
    went = {r[0] for r in db.execute("SELECT key FROM share_out WHERE fleet=? AND kind='thread'", (fleet,))}
    named = {r[0] for r in db.execute("SELECT key FROM share_people WHERE kind='thread' AND fleet=?", (fleet,))}
    back = sorted(tag for (thread,) in db.execute("SELECT thread FROM share_threads WHERE hand='private' OR verdict='personal' OR "
                                                  "(hand IS NULL AND verdict IN ('sensitive','internal','unsure','other'))")
                  if thread not in named and (tag := sg.keyed(secret, 'thread|' + thread)) in went)
    rows = lambda sql, *args: [list(r) for r in db.execute(sql, args)]
    state = [sorted(box.graph_accounts(fleet)), sorted(box.internal(fleet)), sorted(box.my_emails()), sorted(box._personal_people(db)),
             sorted([m, sorted(map(str, p)), sorted(map(str, t))] for m, (p, t) in sg.grants(db, fleet).items()),
             sorted(graph.hidden_project_ids(db)), sorted(graph.hidden_event_ids(db)),
             rows('SELECT thread,hand FROM share_threads WHERE hand IS NOT NULL ORDER BY thread'),
             rows('SELECT node_id FROM share_private ORDER BY node_id'), rows('SELECT key,choice FROM share_rules ORDER BY key'),
             rows('SELECT kind,key,fleet,member FROM share_people ORDER BY kind,key,fleet,member'),
             rows("SELECT id FROM graph_nodes WHERE kind='person' AND json_extract(info,'$.side')='personal' "
                  "AND json_extract(info,'$.side_why') IN (SELECT value FROM json_each(?)) ORDER BY id", json.dumps(graph.OWN_LIFE))]
    return hashlib.sha256(sg.canon(state)).hexdigest(), back


def publish(box, group, me, found, force):
    """graph_publish, the part of a round that reads every shared thread (most of its work): every PUBLISH_EVERY, as a
    new client thread waits out HOLD anyway. Every round still when it is forced (a member OK, Share now, an admin's
    remove) or choices() moved: the owner chose something, or a thread that went is now kept back, so what is taken back
    goes within a round, as before. The rest of a round (the directory, keys, an admin's remove or pause, take-backs
    while paused or off, fetching what teammates sent) runs every round. Whether it published."""
    fleet = group['id']
    last = box.__dict__.setdefault('_graph_published', {}).get(fleet)
    try:
        with box.connect() as db:
            digest, back = choices(box, db, fleet)
    except (sqlite3.Error, ValueError, TypeError, KeyError, AttributeError):
        digest, back = None, ()  # can't tell: publish, as before
    at = time.monotonic()
    if not force and digest and last and at - last[0] < PUBLISH_EVERY and digest == last[1] and set(back) <= last[2]:
        return False
    box.graph_publish(group, me, found)
    box._graph_published[fleet] = (at, digest, set(back))  # as before it: a change meanwhile publishes next round
    return True


def blob_list(box, fleet):
    """What each of this Machine's copies of the team's blobs is (shared_graph.BLOB_LIST), for passing them on to a
    teammate who asked (_graph_serve): kept in memory until team_blobs changes. Listing them read each blob's sealed
    content too (it sits in the same rows), megabytes every round while anyone's ask was open. Not to be changed."""
    import shared_graph as sg
    have = box.__dict__.setdefault('_blob_list', {})
    if not have.get(('watched',)):
        with box.connect() as db:
            stamps.watch(db, ['team_blobs'])
        have[('watched',)] = True
    with box.connect() as db:
        at = stamps.stamp(db, ['team_blobs'])
        if at is not None and fleet in have and have[fleet][0] == at:
            return have[fleet][1]
        rows = [dict(r) for r in db.execute(sg.BLOB_LIST, (fleet,))]
    if at is not None:  # counted before it was listed: a change meanwhile lists it again next time
        have[fleet] = (at, rows)
    return rows


def kept(box, fleet, state, keep, records, chains):
    """A round that sent everything: what it read is kept for the next (graph_out's inputs; the rest in memory only).
    Not while an organization's logo or a person's photo waits for room in a later blob (shared_graph_logos): the next
    round sends it. records, chains: what this round published, for the team and for each chain."""
    import shared_graph_logos as logos
    st = box.meta('graph_chains:' + fleet, {}) or {}
    for recs, sent in [(records, state.get('logos')), *((c['records'], (st.get(chain) or {}).get('logos')) for chain, c in chains.items())]:
        if any(logos._h(r) in logos._OUT and (sent or {}).get(rid) != logos._h(r) for rid, r in recs.items()):
            return
    box.set_meta('graph_out:' + fleet, {**state, 'inputs': keep['inputs']})
    box.__dict__.setdefault('_graph_last', {})[fleet] = {k: keep[k] for k in ('steady', 'found', 'top')}

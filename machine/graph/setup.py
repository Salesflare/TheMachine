"""A Graph build's setup, and what it is computed from (its mark).

The setup: the owner's own addresses (own_addresses.py), organization profiles saved before their check, the people the
owner made from their own addresses (About you), and the change counters a build needs. It reads the signals once,
outside the write lock, and writes only what changed, each under the write lock for a moment; with nothing to change
(most builds) it takes no lock at all, so it never waits on a sync's or a request's write.

The mark: the change counters (machine/stamps.py) of every table a build reads, as the build found them, with its own
publish's writes added. While they are all the same, nothing a build reads changed: the graph worker skips its next
timed build (unchanged, App.graph_build keep). tests/test_graph_skip.py traces a build to keep GRAPH_INPUTS whole."""
import json
import sqlite3

import graph
import own_addresses
from machine import stamps

# What a build reads besides events (counted by events_shared: what a message shows, not the review's bookkeeping on it)
GRAPH_INPUTS = tuple(sorted({
    *graph.GRAPH_WATCHED, 'contact_marks', 'crm_tags', 'decision_annotations', 'decisions', 'event_projects', 'event_vectors',
    'forgotten_salt', 'graph_events', 'graph_history', 'graph_history_events', 'graph_links', 'graph_unnamed', 'mail_hidden',
    'mail_shown', 'org_aliases', 'org_profiles', 'own_address_choices', 'own_address_fetched', 'own_addresses', 'own_domains',
    'owner_numbers', 'person_facts', 'person_photos', 'person_profiles', 'project_org_backfill', 'promises', 'share_private',
    'share_threads', 'side_rule', 'suggestions'}))
INPUT_COUNTERS = ('events_shared', *GRAPH_INPUTS)


def learn_sent(owner, sent_by):
    """graph.Owner.learn from what own_addresses.evidence read already: {From address of sent mail: its plain names}."""
    for address, names in sent_by.items():
        if address not in owner.excluded:
            owner.emails.add(address)
            owner.names |= names - {None, ''}


def prepare(db, config, signals, team, now, locked):
    """The setup, in the build's transaction when locked (all of it, as every build once was). Returns graph.Owner."""
    found = own_addresses.evidence(config, signals)
    if locked or unwatched(db) or unusable_profiles(db) or own_addresses.unsaved(
            db, own_addresses.detect(config, own_addresses.fetched(db, config), found, team)):
        if not locked:
            db.execute('BEGIN IMMEDIATE')
        graph._watch(db)
        stamps.watch(db, GRAPH_INPUTS)
        stamps.watch_events_shared(db)
        own_addresses.refresh(db, config, signals, team, now, found)  # the owner's own addresses, before anyone is told apart from them
        graph._drop_unusable_profiles(db)
        if not locked:
            db.execute('COMMIT')
    owner = graph.Owner(config, db)
    if locked:  # reads the signals again, as every build once did (tests/test_graph_skip.py compares the two)
        owner.learn(signals)
    else:
        learn_sent(owner, found['sent_by'])
    if locked or graph.self_records(db, owner):
        if not locked:
            db.execute('BEGIN IMMEDIATE')
        graph.fold_self_records(db, owner, now)  # a person made from the owner's own address goes into About you (2026-10-26)
        if not locked:
            db.execute('COMMIT')
    return owner


def unusable_profiles(db):
    """Organization profiles saved before the check (a shared host's domain, another company): their domains."""
    import enrichment
    return [r['domain'] for r in db.execute("SELECT domain,profile FROM org_profiles WHERE profile IS NOT NULL AND status='found'").fetchall()
            if not enrichment.usable(r['domain'], json.loads(r['profile']))]


def unwatched(db):
    """Whether a counter a build needs is missing (graph_edits' and those of GRAPH_INPUTS): made in the setup's write."""
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    made = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
    if 'graph_edits' not in tables or 'data_stamps' not in tables or not db.execute('SELECT 1 FROM graph_edits WHERE id=1').fetchone():
        return True
    return any(f'graph_edit_{t}_insert' not in made for t in graph.GRAPH_WATCHED if t in tables) \
        or any(f'stamp_{t}_insert' not in made for t in GRAPH_INPUTS if t in tables) \
        or 'stamp_events_shared_insert' not in made


def counters(db):
    """{counter: n} for what a build reads and graph_edits, in the caller's snapshot; None without them."""
    try:
        found = dict(db.execute('SELECT name,n FROM data_stamps WHERE name IN (SELECT value FROM json_each(?))',
                                (json.dumps(INPUT_COUNTERS),)).fetchall())
        found['graph_edits'] = graph._edits(db)
    except sqlite3.Error:
        return None
    return found


def mark(before, pre, post):
    """The counters a build's graph stands for: those it was computed from (before), with what its own publish added
    (post - pre); a change by anyone else since then makes them differ. None when a counter came or went meanwhile."""
    if before is None or pre is None or post is None or set(before) != set(pre) or set(pre) != set(post):
        return None
    return {k: before[k] + post[k] - pre[k] for k in sorted(post)}


def unchanged(db, built):
    """Nothing a build reads changed since the build whose summary's mark this is."""
    return bool(built) and not db.in_transaction and counters(db) == built

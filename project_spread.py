"""Catch-all projects. A project is one piece of work with shared people or one goal. The same kind of outreach to many
separate people (invites, testers, pitches, candidates) is not one project: each counterpart is its own piece of work
once they answer, and a message nobody answered is none yet.

Groups: a project's conversations joined by who they are with, leaving out the owner, their team and colleagues: the
organization, or the person when they have none (graph.touches says who a message is with, graph_identifiers which
person that is). Two conversations with the same organization are one group, and so is a three-way thread with a
partner and a customer. A group is one-way while only the owner wrote in it (no reply, no meeting).

Plain code, no model, in two places:
- admit: what a review labels into a project (finish_analysis projects, graph project with event_ids). A thread that
  shares nobody with the project joins it only while the project is no catch-all, and, when only the owner wrote in it,
  while the project has fewer than ONE_WAY one-way groups. Threads with nobody outside (the owner's own notes, a
  colleague) and threads with someone already on it always join. The owner's own labels never pass here. A thread
  refused while one-way can still join once the other side answers and a review labels the reply (graph.build spreads
  a label over its thread).
- catch_all: CATCH_ALL groups or more, or SOME or more with at least two thirds one-way. The project's page says so and
  offers Split up (project_split.group_items: one project per group that answered, or onto the one it is on already;
  the one-way ones taken off, nothing deleted, Undo) or Keep as one: kept (project_spread_kept) until it has twice the groups it had then.

Bounded: READ labeled messages per project, newest first; a kept row per project, gone with its project."""
from __future__ import annotations

import json

import graph
from machine import stamps

ONE_WAY = 3      # one-way groups a project may hold before a new one is refused
SOME = 6         # groups from which a project two thirds one-way is a catch-all
CATCH_ALL = 25   # groups from which any project is
READ = 3000      # labeled messages read per project, newest first

SCHEMA = 'CREATE TABLE IF NOT EXISTS project_spread_kept(project_id INTEGER PRIMARY KEY,groups INTEGER NOT NULL,kept_at TEXT NOT NULL)'
KEPT = stamps.Kept(16)


def ensure(db):
    db.execute(SCHEMA)


def _meta(raw):
    try:
        found = json.loads(raw or '{}') if str(raw or '').startswith('{') else {}
    except ValueError:
        return {}
    return found if isinstance(found, dict) else {}


class Who:
    """Who a message is with, as group keys: {organization node id, or person node id when they have none}."""

    def __init__(self, db, owner):
        self.db, self.owner, self.cache, self.orgs = db, owner, {}, {}
        self.colleagues = graph.colleagues(db)  # once: own_domain reads every person otherwise

    def org(self, org):
        """The organization key, or None for the owner's own company."""
        if org not in self.orgs:
            self.orgs[org] = None if org[4:] in self.owner.domains or graph.own_domain(self.db, org[4:], self.colleagues) else org
        return self.orgs[org]

    def key(self, identifier):
        if identifier in self.cache:
            return self.cache[identifier]
        row = self.db.execute("SELECT n.id,json_extract(n.info,'$.org') org,json_extract(n.info,'$.colleague') colleague FROM graph_identifiers i "
                              "JOIN graph_nodes n ON n.id=i.node_id AND n.kind='person' WHERE i.identifier=? LIMIT 1", (identifier,)).fetchone()
        if row:
            org = str(row['org'] or '')
            found = None if row['colleague'] == 1 else ((self.org(org) or None) if org.startswith('org:') else row['id'])
        elif identifier.startswith('email:'):  # not in the graph yet (it builds every half hour): their mail domain
            domain = identifier.rsplit('@', 1)[-1]
            found = identifier if domain in graph.FREEMAIL or graph.personal_mail(self.db, domain) else self.org('org:' + domain)
        else:
            found = identifier
        self.cache[identifier] = found
        return found

    def of(self, kind, m):
        """(keys, answered): who a message is with, and whether someone other than the owner wrote it (or met them)."""
        keys, answered = set(), False
        for identifier, _, _, role in graph.touches(kind, m, self.owner, ()):
            key = self.key(identifier)
            if key:
                keys.add(key)
                answered = answered or role != 'owner'
        return keys, answered


def _threads(rows, who):
    """{thread: {'keys', 'answered', 'events', 'at'}} for event rows (id, account_id, kind, occurred_at, metadata)."""
    out = {}
    for r in rows:
        m = _meta(r['metadata'])
        key, _ = graph.thread_key(r['kind'], m)
        thread = out.setdefault((r['account_id'], key) if key else ('event', r['id']), {'keys': set(), 'answered': False, 'events': [], 'at': r['occurred_at']})
        keys, answered = who.of(r['kind'], m)
        thread['keys'] |= keys
        thread['answered'] = thread['answered'] or answered
        thread['events'].append(r['id'])
        thread['at'] = max(thread['at'] or '', r['occurred_at'] or '')
    return out


def _rows(db, sql, args):
    return db.execute('SELECT e.id,e.account_id,e.kind,e.occurred_at,e.metadata FROM events e ' + sql, args).fetchall()


class Shape:
    """A project's groups: threads joined by a shared key."""

    def __init__(self):
        self.parent, self.groups = {}, {}

    def find(self, x):
        while self.parent.setdefault(x, x) != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def add(self, thread):
        keys = sorted(thread['keys'])
        if not keys:
            return
        roots = {self.find(k) for k in keys}
        root = min(roots)
        group = {'keys': set(), 'answered': False, 'events': [], 'at': '', 'threads': 1}
        for r in roots:
            old = self.groups.pop(r, None)
            if old:
                group['keys'] |= old['keys']
                group['answered'] = group['answered'] or old['answered']
                group['events'] += old['events']
                group['at'] = max(group['at'], old['at'])
                group['threads'] += old['threads']
            self.parent[r] = root
        group['keys'] |= thread['keys']
        group['answered'] = group['answered'] or thread['answered']
        group['events'] += thread['events']
        group['at'] = max(group['at'], thread['at'] or '')
        self.groups[root] = group

    def shares(self, thread):
        return any(k in self.parent for k in thread['keys'])

    @property
    def one_way(self):
        return sum(1 for g in self.groups.values() if not g['answered'])

    def catch_all(self):
        n = len(self.groups)
        return n >= CATCH_ALL or (n >= SOME and 3 * self.one_way >= 2 * n)


def shape(db, pid, owner, who=None):
    """(Shape, threads with nobody outside): the groups on a project's labeled messages."""
    who = who or Who(db, owner)
    rows = _rows(db, 'JOIN event_projects ep ON ep.event_id=e.id WHERE ep.project_id=? AND e.deleted=0 ORDER BY e.occurred_at DESC,e.id DESC LIMIT ?', (pid, READ))
    found, alone = Shape(), []
    for thread in _threads(rows, who).values():
        if thread['keys']:
            found.add(thread)
        else:
            alone.append(thread)
    return found, alone


def kept(db, pid):
    """The groups the project had when the owner kept it as one, or None."""
    try:
        row = db.execute('SELECT groups FROM project_spread_kept WHERE project_id=?', (pid,)).fetchone()
    except Exception:  # sqlite3.OperationalError: no table yet
        return None
    return row[0] if row else None


def is_catch_all(db, pid, found):
    held = kept(db, pid)
    return found.catch_all() and not (held and len(found.groups) < 2 * held)


def admit(db, name, event_ids, owner):
    """(admitted ids, refused ids) of a review's label of these messages onto the project by this name (see the module).
    A new project starts empty, so a batch of outreach that names one stops at ONE_WAY one-way groups too."""
    ids = [int(e) for e in event_ids]
    if not ids:
        return [], []
    row = db.execute('SELECT id FROM projects WHERE name=? COLLATE NOCASE', (' '.join(str(name or '').split()),)).fetchone()
    who = Who(db, owner)
    if row:
        found, _ = shape(db, row['id'], owner, who)
        if kept(db, row['id']) and not is_catch_all(db, row['id'], found):
            return ids, []  # the owner kept it as one
    else:
        found = Shape()
    marks = ','.join('?' * len(ids))
    threads = sorted(_threads(_rows(db, f'WHERE e.id IN ({marks})', ids), who).values(), key=lambda t: t['at'] or '')
    admitted, refused = [], []
    for thread in threads:
        if not thread['keys'] or found.shares(thread):
            admitted += thread['events']
        elif (is_catch_all(db, row['id'], found) if row else found.catch_all()) or (not thread['answered'] and found.one_way >= ONE_WAY):
            refused += thread['events']
            continue
        else:
            admitted += thread['events']
        found.add(thread)
    known = set(admitted) | set(refused)
    return admitted + [e for e in ids if e not in known], refused  # an id that is no live message: as graph.label had it


def label(db, projects, owner, now, source='review'):
    """A review's labels ({name: [event ids]}) through admit: {name: refused count} for those it kept off."""
    refused = {}
    for name, ids in projects.items():
        took, kept_off = admit(db, name, ids, owner)
        if took:
            graph.label(db, took, name, source, now)
        if kept_off:
            refused[name] = len(kept_off)
    return refused


def page(db, pid, owner):
    """For a project's page: {'groups', 'one_way'} when it is a catch-all, else None. Kept until its labels, its people or
    the owner's word change."""
    def make():
        if db.execute('SELECT count(*) FROM event_projects WHERE project_id=?', (pid,)).fetchone()[0] < SOME:
            return None
        found, _ = shape(db, pid, owner)
        return {'groups': len(found.groups), 'one_way': found.one_way} if is_catch_all(db, pid, found) else None
    ensure(db)
    at = stamps.stamp(db, ('event_projects', 'graph_identifiers', 'graph_nodes'))
    held = kept(db, pid)
    return KEPT.get(('spread', pid, held), at, make)


def keep(db, pid, owner, now):
    """Keep as one: not a catch-all again until it has twice the groups it has now."""
    ensure(db)
    db.execute('DELETE FROM project_spread_kept WHERE project_id NOT IN (SELECT id FROM projects)')
    found, _ = shape(db, pid, owner)
    db.execute('INSERT OR REPLACE INTO project_spread_kept(project_id,groups,kept_at) VALUES(?,?,?)', (pid, max(1, len(found.groups)), now))
    return {'kept': len(found.groups)}


def groups(db, pid, owner):
    """The project's groups for a split, most messages first: ([group dicts], threads with nobody outside)."""
    found, alone = shape(db, pid, owner)
    return sorted(found.groups.values(), key=lambda g: (-len(g['events']), min(g['keys']))), alone


def name_of(db, keys):
    """A group's name: its organization's, else its person's, as the graph calls them."""
    for key in sorted(keys, key=lambda k: (not k.startswith('org:'), k)):
        row = db.execute('SELECT name FROM graph_nodes WHERE id=?', (key,)).fetchone()
        if row and str(row['name'] or '').strip():
            return graph.one_line(row['name'], 60) or key
    key = sorted(keys)[0]
    return (key[4:] if key.startswith('org:') else key.split(':', 1)[-1])[:60]

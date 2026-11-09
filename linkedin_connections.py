"""LinkedIn connections: each one's current title and company, and their profile link, kept up to date on the people
already in the Graph, with when LinkedIn last showed it.

Read through the owner's own signed-in browser, like the messages (connectors/linkedin.py Source.connections, through
integrations/linkedin_inbox.py `connections`): the My Network, Connections list, one page of 40 per step, newest first,
as that page itself loads it (name and headline). No profile is opened, nothing is written to LinkedIn, no new
permission is asked.

LinkedIn has no API for this and bulk reads could get the account restricted, so very slowly (PACE): one page per
step, a random 8 to 20 minutes apart, at most 24 steps a day, only from 9 to 21 local time (narrowed to the account's
active_hours), never while the connection's own sync fails or before its first import is in, and a day off after any
failed or odd answer (a 429, a security check, a changed answer): never a retry loop. A full pass starts again at most
every REFRESH_DAYS. The same rules as LinkedIn history in PR #1065 (machine/app/history.py HISTORY_PACE, pace_wait,
pace_after): kept self-contained here until that merges; then the two should share one pace and one daily budget.

Matching, never a new person: by profile link first (their vanity link or member id, against the links the Graph
knows), else the same full name and company, and only when exactly one person fits. A connection that matches nobody
is left alone and not kept. What matches is kept as their facts (enrichment.person_facts, source linkedin, their own
words), so their page and the Graph show it with its date. A new title or company is a line on their page (crm
record_changes, field job: "Now Head of Sales at Acme, was Sales Lead at Beta")."""
from __future__ import annotations

import datetime as dt
import json
import random
import re

import abilities
import crm
import enrichment
import graph
from machine.store import history
from timeutil import local_tz, now as now_iso

PACE = {'page': 40, 'steps_per_day': 24, 'pause_minutes': (8, 20), 'hours': (9, 21)}
REFRESH_DAYS = 7  # a new pass starts this long after the last one started
STOP_DAYS = 1     # after any failed or odd read
MAX_START = 30000  # LinkedIn's own limit on connections: a pass never pages past it
PREF = 'linkedin_connections:'  # + account id, in enrich_prefs: the pass and its pace
# "Head of Sales at Acme | Helping teams grow": the part before the first separator, split on "at" (and its own word
# in the other languages people write headlines in). Anything else ("Founder, Acme") gives no title or company.
AT = re.compile(r'\s+(?:at|@|bij|chez|bei|presso|en la|na)\s+|\s*@\s*', re.I)
SEPARATOR = re.compile(r'\s+[|•·–—]\s+|\s+-\s+|\s*\|\s*')


def accounts(config):
    """The owner's own LinkedIn connections that read through the browser, unless "connections": false."""
    return [a for a in config.get('accounts') or [] if a.get('service') == 'linkedin' and a.get('transport', 'linkedin-inbox') == 'linkedin-inbox'
            and abilities.signals_on(a) and not a.get('shared') and a.get('connections') is not False]


def job(headline):
    """(title, company) from a headline that says it ("Head of Sales at Acme"), else (None, None)."""
    first = SEPARATOR.split(' '.join(str(headline or '').split()), maxsplit=1)[0]
    parts = AT.split(first, maxsplit=1)
    if len(parts) != 2:
        return None, None
    title, company = parts[0].strip(' ,.;:'), re.split(r',\s|\s\(', parts[1], maxsplit=1)[0].strip(' ,.;:')  # "Acme, ex-Globex": Acme
    if not (2 <= len(title) <= 120 and 2 <= len(company) <= 120):
        return None, None
    return title, company


def profile_url(raw):
    slug = str(raw.get('slug') or '')
    return 'https://www.linkedin.com/in/' + slug + '/' if re.fullmatch(r'[A-Za-z0-9_%-]{2,100}', slug) else None


def keys(raw):
    """The profile link keys a connection can be known by: their vanity link and their member id (messages link that)."""
    return {k for k in (str(raw.get('slug') or '').casefold(), str(raw.get('member') or '').casefold()) if len(k) >= 2}


# ------------------------------------------------------------------ pace

def get_state(db, account_id):
    try:
        state = json.loads(enrichment.pref(db, PREF + account_id) or '{}')
    except ValueError:
        state = {}
    return state if isinstance(state, dict) else {}


def put_state(db, account_id, state):
    enrichment.set_pref(db, PREF + account_id, json.dumps(state, sort_keys=True))


def wait(state, account, current):
    """Why a step waits now (a short code), or None: stopped for a day, its pause not over, outside waking hours, the
    day's steps used up, or the last pass recent enough. `current` is an aware datetime."""
    stamp = current.isoformat()
    if state.get('stopped_until', '') > stamp:
        return 'stopped'
    if state.get('next_at', '') > stamp:
        return 'pause'
    local = current.astimezone(local_tz())
    start, end = PACE['hours']
    own = account.get('active_hours')
    if isinstance(own, (list, tuple)) and len(own) == 2:
        start, end = max(start, int(own[0])), min(end, int(own[1]))
    if not start <= local.hour < end:
        return 'hours'
    if state.get('day') == local.date().isoformat() and int(state.get('steps') or 0) >= PACE['steps_per_day']:
        return 'cap'
    if not state.get('start') and state.get('pass_at') and state.get('done_at') and \
            dt.datetime.fromisoformat(state['pass_at']) + dt.timedelta(days=REFRESH_DAYS) > current:
        return 'rest'
    return None


def after(state, current, failed=None):
    """After a step at `current`: count it for today and pause a random 8 to 20 minutes, so reads never come at a fixed
    beat. A failed or odd read stops for STOP_DAYS, unless only the browser was busy with another job."""
    day = current.astimezone(local_tz()).date().isoformat()
    if state.get('day') != day:
        state.update(day=day, steps=0)
    state['steps'] = int(state.get('steps') or 0) + 1
    least, most = PACE['pause_minutes']
    state['next_at'] = (current + dt.timedelta(minutes=random.uniform(least, most))).isoformat()
    if failed:
        state['error'] = str(failed)[:80]
        if not str(failed).endswith('_browser_busy'):
            state['stopped_until'] = (current + dt.timedelta(days=STOP_DAYS)).isoformat()
    else:
        state.pop('error', None)


# ------------------------------------------------------------------ matching

def folded(text):
    return graph.folded_words(text)


def same_company(a, b):
    a, b = folded(a), folded(b)
    return bool(a and b) and (a == b or f' {a} ' in f' {b} ' or f' {b} ' in f' {a} ')


def index(db):
    """The Graph's people, to match connections against: {'links': {key: node ids}, 'names': {full name: [(node id,
    companies)]}, 'nodes': {node id: identifiers}}."""
    orgs = {r[0]: r[1] for r in db.execute("SELECT id,name FROM graph_nodes WHERE kind='org'")}
    facts = enrichment.people_facts(db, ('linkedin_url', 'company'))
    links, names, nodes = {}, {}, {}
    for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='person' ORDER BY strength DESC,id"):
        try:
            info = json.loads(r[2] or '{}')
        except ValueError:
            continue
        group = info.get('identifiers') or [r[0]]
        nodes[r[0]] = group
        profile = info.get('profile') or {}
        urls = {profile.get('linkedin_url')} | {(facts.get(i) or {}).get('linkedin_url', (None,))[0] for i in group}
        for url in urls:
            key = graph.linkedin_key(url)
            if key:
                links.setdefault(key, []).append(r[0])
        full = graph.plain_name(r[1])
        if full:
            companies = {profile.get('company'), orgs.get(info.get('org'))} | {(facts.get(i) or {}).get('company', (None,))[0] for i in group}
            names.setdefault(full, []).append((r[0], {c for c in companies if c}))
    return {'links': links, 'names': names, 'nodes': nodes}


def match(found, raw, company):
    """The one Graph person this connection is, or None: by profile link, else by full name and company."""
    for key in keys(raw):
        if found['links'].get(key):
            return found['links'][key][0]  # the strongest, when the Graph has them twice
    full = graph.plain_name(raw.get('name'))
    if not full or not company:
        return None
    fits = [node for node, companies in found['names'].get(full, ()) if any(same_company(company, c) for c in companies)]
    return fits[0] if len(fits) == 1 else None


def apply(db, found, node, raw, title, company, current):
    """Keeps what LinkedIn shows on this person (their own words, STATED) and, when their title or company moved on, a
    line on their page. Returns (facts changed, changes noted)."""
    group = found['nodes'].get(node) or [node]
    had = enrichment.people_facts(db, ('title', 'company'), group)
    mine = {f: v[0] for f, v in (had.get(node) or {}).items() if v[2] == 'linkedin'}
    noted = 0
    if title or company:
        new = {'title': title, 'company': company}
        if mine:  # LinkedIn showed them before: any change of their own title or company
            old = {'title': mine.get('title'), 'company': mine.get('company')}
            moved = folded(old['title']) != folded(title) or folded(old['company']) != folded(company)
        else:  # first seen here: only another company than the Graph has, never a differently worded title
            best = enrichment.best_facts([had[i] for i in group if i in had])
            org = db.execute("SELECT o.name FROM graph_nodes p JOIN graph_nodes o ON o.id=json_extract(p.info,'$.org') WHERE p.id=?", (node,)).fetchone()
            old = {'title': (best.get('title') or (None,))[0], 'company': (best.get('company') or (None,))[0] or (org[0] if org else None)}
            moved = bool(company and old['company'] and not same_company(company, old['company']))
        if moved:
            crm.ensure(db)
            crm.change(db, node, 'job', json.dumps({k: v for k, v in old.items() if v}) if (old['title'] or old['company']) else None,
                       json.dumps({**{k: v for k, v in new.items() if v}, 'via': 'LinkedIn'}), current)
            noted = 1
    offer = {'headline': raw.get('headline') or '', 'title': title or '', 'company': company or '',
             'linkedin_url': profile_url(raw) or ''}
    return enrichment.offer_facts(db, [([node], offer, enrichment.STATED)], 'linkedin', current), noted


# ------------------------------------------------------------------ a step

def reader(config, account):
    from machine.sources.connectors import CONNECTOR_HELPERS, load_connector
    module = load_connector('linkedin')
    return module.Source(config, account, CONNECTOR_HELPERS).connections


def step(connect, config, account, read=None, current=None):
    """One paced step for one account: {'wait': code} when it waits, else what this page did ({'seen', 'matched',
    'changed', 'noted', 'done'}) or {'error': code}."""
    from sources import SourceError
    current = dt.datetime.fromisoformat(current or now_iso())
    stamp = current.isoformat()
    with connect() as db:
        state = get_state(db, account['id'])
        live = db.execute('SELECT error FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
        imported = history.first_import_done(db, account['id'])
    if not imported:
        return {'wait': 'first_import'}
    if live and live[0]:
        return {'wait': 'live_error'}  # its own sync fails (signed out, blocked): don't add reads
    why = wait(state, account, current)
    if why:
        return {'wait': why}
    start = int(state.get('start') or 0)
    if not start:
        state.update(pass_at=stamp, seen=0, matched=0, noted=0)
    try:
        page = (read or reader(config, account))(start, PACE['page'])
    except SourceError as error:
        after(state, current, failed=error.category)
        with connect() as db:
            put_state(db, account['id'], state)
        return {'error': error.category}
    rows = [r for r in page['connections'] if isinstance(r, dict) and r.get('name')]
    if page['more'] and not rows:  # an odd answer: stop for the day rather than page on through nothing
        after(state, current, failed='linkedin_odd_page')
        with connect() as db:
            put_state(db, account['id'], state)
        return {'error': 'linkedin_odd_page'}
    changed = noted = matched = 0
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        found = index(db)
        for raw in rows:
            title, company = job(raw.get('headline'))
            node = match(found, raw, company)
            if not node:
                continue
            matched += 1
            facts, lines = apply(db, found, node, raw, title, company, stamp)
            changed, noted = changed + facts, noted + lines
        done = not page['more'] or start + PACE['page'] >= MAX_START
        state.update(start=0 if done else start + PACE['page'], seen=int(state.get('seen') or 0) + len(rows),
                     matched=int(state.get('matched') or 0) + matched, noted=int(state.get('noted') or 0) + noted)
        if done:
            state['done_at'] = stamp
        after(state, current)
        put_state(db, account['id'], state)
    return {'seen': len(rows), 'matched': matched, 'changed': changed, 'noted': noted, 'done': done}


def status(db, account_id):
    """The pass so far, for the connection's details: {'seen', 'matched', 'noted', 'done_at', 'error'}."""
    state = get_state(db, account_id)
    return {k: state.get(k) for k in ('seen', 'matched', 'noted', 'done_at', 'error', 'stopped_until')}

"""The standing eval for "one brain behind every surface" (knowledge.py): realistic questions with the records that
must come back, asked through every surface's own tool path without a model. The chat's tools (graph, events), Talk's
(search, open_record), a connected AI's (search_graph, get_graph_record, search_messages) and the dashboard's (the
Graph page and its timeline, Ctrl/Cmd K search).

    python3 tests/knowledge_eval.py                      the sandbox (sandbox/load.py, busy) plus the cases below
    python3 tests/knowledge_eval.py --db X --config Y    read-only agreement checks on a copy of a real install's
                                                         database: counts only, never a name or a message
    python3 tests/knowledge_eval.py --llm                also the questions a model answers with Talk's tools
                                                         (optional, weekly; needs OPENAI_API_KEY)

Seeded with the shapes that failed for real: a person found by name whose latest messages are on a second identity,
a record with many meetings ahead, identities merged into one person, a person known only by a WhatsApp number, and
nothing found (said plainly, with what was searched).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# search: Ctrl/Cmd K and the Graph's search box (api/graph?q=); layer: knowledge.py itself, as the owner asks it
SURFACES = ('chat', 'talk', 'mcp', 'page', 'search', 'layer')
MESSAGES = ('gmail.message', 'salesflare.email', 'linkedin.message', 'slack.message', 'whatsapp.message', 'telegram.message',
            'intercom.conversation', 'x.dm', 'ms_graph.message', 'outlook.message')

# Made up, like everything in the sandbox
PIM = {'name': 'Pim Ostrava', 'number': '32470000102', 'spoken': ('+32 470 00 01 02', '0470 00 01 02', '0032470000102')}
JUNO = {'name': 'Juno Calloway', 'email': 'juno@tidepool.example'}
KAI = {'name': 'Kai Brandt', 'email': 'kai@fernhollow.example', 'number': '32470000177'}
RHEA = {'name': 'Rhea Lindqvist', 'email': 'rhea@saltwick.example'}  # Work, one thread judged sensitive
NOBODY = 'Nobody Zebrafinch'


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


# ------------------------------------------------------------------ the install

def app_for(config, assistant):
    """An App over an install's config and database, enough for the read paths (no services started)."""
    app = object.__new__(assistant.App)
    app.config = config
    app.store = assistant.Store(config['database'])
    app.token, app.owner_token, app.stop = 'eval', 'eval-owner', threading.Event()
    app.graph_dirty = threading.Event()
    app.fleet = None
    return app


def sandbox(folder):
    """The sandbox install (busy) with the failure shapes added as ordinary synced signals, then the Graph rebuilt."""
    sys.path.insert(0, str(ROOT / 'sandbox'))
    import load
    home = os.environ.get('HOME')
    try:
        config, _ = load.load(folder, load.parse_states('busy'))
    finally:  # load points HOME at the sandbox for its own run; put it back for whatever runs next in this process
        if home is not None:
            os.environ['HOME'] = home
    import assistant
    import graph
    store = assistant.Store(config['database'])
    base = now()
    at = lambda hours: (base + dt.timedelta(hours=hours)).isoformat()
    ids = {'pim': [], 'juno_mail': [], 'juno_ahead': [], 'kai_mail': [], 'kai_chat': [], 'rhea_open': [], 'rhea_held': []}
    with store.connect() as db:
        def add(account, kind, hours, title, body, meta, key):
            event = db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,'
                               'analyzed_version,ingested_at) VALUES(?,?,?,?,?,?,?,0,?,1,1,?)',
                               (account, 'eval:%s:%s' % (key, hours), kind, at(hours), title, body, json.dumps(meta),
                                hashlib.sha256((title + body).encode()).hexdigest(), at(min(hours, 0)))).lastrowid
            ids[key].append(event)
        wa = lambda number, name, mine, n: {'chat_id': number + '@s.whatsapp.net', 'chat_name': name, 'from_me': mine, 'group': False,
                                            'sender_display': name, 'message_id': 'eval-wa-%s-%d' % (number, n)}
        # Known only by a WhatsApp number: a chat, nothing else
        for n, hours in enumerate((-2, -26, -50)):
            add('home-whatsapp', 'whatsapp.message', hours, PIM['name'], 'See you at the climbing gym', wa(PIM['number'], PIM['name'], n == 1, n), 'pim')
        # Two mails, then many meetings ahead: the latest messages are still the mails
        for n, hours in enumerate((-3, -40)):
            add('work-gmail', 'gmail.message', hours, 'Tidepool rollout plan', 'The rollout plan for the depots',
                {'from': '%s <%s>' % (JUNO['name'], JUNO['email']), 'to': 'alex@lumenlabs.example', 'labels': ['INBOX'],
                 'thread_id': 'eval-juno', 'message-id': '<eval-juno.%d@tidepool.example>' % n}, 'juno_mail')
        for day in range(1, 13):
            start = base + dt.timedelta(days=day)
            add('work-calendar', 'calendar.event', day * 24, 'Tidepool rollout check-in', '',
                {'status': 'confirmed', 'start': {'dateTime': start.isoformat()}, 'end': {'dateTime': (start + dt.timedelta(minutes=30)).isoformat()},
                 'end_at': (start + dt.timedelta(minutes=30)).isoformat(), 'all_day': False, 'organizer': {'email': 'alex@lumenlabs.example'},
                 'attendees': [{'email': 'alex@lumenlabs.example', 'self': True}, {'email': JUNO['email'], 'responseStatus': 'accepted'}]},
                'juno_ahead')
        # One person under two identities, merged by the owner: mail on the personal address, chats on WhatsApp
        for n, hours in enumerate((-5, -30)):
            add('home-gmail', 'gmail.message', hours, 'Cabin weekend', 'Shall we book the cabin weekend',
                {'from': '%s <%s>' % (KAI['name'], KAI['email']), 'to': 'alex.morgan@mail.example', 'labels': ['INBOX'],
                 'thread_id': 'eval-kai', 'message-id': '<eval-kai.%d@fernhollow.example>' % n}, 'kai_mail')
        for n, hours in enumerate((-1, -20, -60)):
            add('home-whatsapp', 'whatsapp.message', hours, KAI['name'], 'Bringing the kayak', wa(KAI['number'], KAI['name'], False, n), 'kai_chat')
        # A Work contact with one ordinary thread and one the review judged sensitive: a connected AI never reads that one
        for key, thread, hours in (('rhea_open', 'eval-rhea-1', -4), ('rhea_held', 'eval-rhea-2', -2)):
            add('work-gmail', 'gmail.message', hours, 'Saltwick contract' if key == 'rhea_open' else 'Saltwick team changes', 'About the contract',
                {'from': '%s <%s>' % (RHEA['name'], RHEA['email']), 'to': 'alex@lumenlabs.example', 'labels': ['INBOX'],
                 'thread_id': thread, 'message-id': '<%s@saltwick.example>' % thread}, key)
        import shared_graph
        shared_graph.ensure(db)
        held = db.execute('SELECT kind,metadata FROM events WHERE id=?', (ids['rhea_held'][0],)).fetchone()
        db.execute("INSERT OR REPLACE INTO share_threads(thread,verdict,event_id,at) VALUES(?,'sensitive',?,?)",
                   (shared_graph.thread_of(held['kind'], json.loads(held['metadata']), ids['rhea_held'][0]), ids['rhea_held'][0], at(0)))
        db.commit()
        graph.build(db, config, base.isoformat())
        graph.merge(db, 'email:' + KAI['email'], 'wa:' + KAI['number'], True, base.isoformat(), 'owner')
        db.commit()
        graph.build(db, config, base.isoformat())
    return config, ids


# ------------------------------------------------------------------ the surfaces' own tool paths

class Surfaces:
    """Each question through each surface's own path: what the model (or the owner's screen) gets back."""

    def __init__(self, app, assistant, area=None):
        self.app, self.a = app, assistant
        self.conn = {'id': 'eval', 'name': 'Eval', 'area': area or 'both', 'messages': True, 'level': 'read'}
        import knowledge
        self.k = knowledge
        self.caller = knowledge.connection(app.config, area) if area else knowledge.owner()

    def accounts(self):
        return [x['id'] for x in self.app.config.get('accounts', [])]

    def mcp(self, name, **args):
        try:
            return self.app.ai_tool(self.conn, name, args)[0]
        except ValueError as error:
            return {'error': str(error)}

    def talk(self, name, **args):
        return self.app.talk_machine_tool(name, args)

    # who is X: the records found, strongest first
    def find(self, surface, words):
        if surface == 'chat':
            return [x['id'] for x in self.app.graph_action({'query': words}).get('found', [])]
        if surface == 'talk':
            return [x['id'] for x in self.talk('search', words=words).get('found', [])]
        if surface == 'mcp':
            return [x['id'] for x in self.mcp('search_graph', query=words).get('found', [])]
        if surface in ('search', 'page'):
            return [x['id'] for x in self.app.graph_find(words)['found'] if x['id'] != 'me']
        if surface == 'layer':
            with self.app.store.connect() as db:
                return [r['id'] for r in self.k.find(db, words, self.caller)]
        raise KeyError(surface)

    def first(self, surface, words):
        found = self.find(surface, words)
        return found[0] if found else None

    # latest messages with X: event ids, newest first
    def latest(self, surface, words, limit=5):
        if surface == 'talk':
            got = self.talk('search', kind='message', person=words)
            return [int(x['id'].split(':')[1]) for x in got.get('found', [])][:limit], got
        node = self.first('search' if surface == 'page' else surface, words)
        if not node:
            return [], {}
        if surface == 'chat':
            lines = self.app.graph_action({'node_id': node}).get('recent', [])
            ids = [int(line.split(' ', 1)[0]) for line in lines]
            kinds = {r['id']: r['kind'] for r in self.app.store.events(self.accounts(), event_ids=ids)} if ids else {}
            return [i for i in ids if kinds.get(i) in MESSAGES][:limit], {}
        if surface == 'mcp':
            got = self.mcp('search_messages', person=node, limit=limit)
            return [m['id'] for m in got.get('messages', [])][:limit], got
        if surface == 'page':
            got = self.app.graph_timeline(node)
            return [i['id'] for i in got['items'] if i['type'] == 'event' and i.get('kind') in MESSAGES][:limit], got
        if surface == 'layer':
            return [r['id'] for r in self.k.latest_messages(self.app.store, self.app.config, node, self.caller, limit)], {}
        raise KeyError(surface)

    # open to-dos and promises with X: ({promise ids}, {to-do ids})
    def open(self, surface, words):
        node = self.first('search' if surface == 'page' else surface, words)
        if not node:
            return set(), set()
        if surface in ('chat', 'page'):
            found = self.app.graph_action({'node_id': node}).get('open') or {}
            return {p['id'] for k in ('you_promised', 'they_promised') for p in found.get(k, [])}, {c['id'] for c in found.get('cards', [])}
        if surface == 'talk':
            got = self.talk('open_record', id=node)
            return ({int(str(p['id']).split(':')[-1]) for p in got.get('promises', [])},
                    {c['id'] for c in got.get('open_todos', [])})
        if surface == 'mcp':
            got = self.mcp('get_graph_record', id=node)
            return {p['id'] for p in got.get('promises', [])}, {t['id'] for t in got.get('todos', [])}
        if surface == 'layer':
            got = self.k.open_with(self.app.store, self.app.config, node, self.caller)
            return {p['id'] for k in ('you_promised', 'they_promised') for p in got[k]}, {t['id'] for t in got['todos']}
        raise KeyError(surface)

    # when did I last talk to X: the moment, as the surface gives it
    def last(self, surface, words):
        node = self.first('search' if surface == 'page' else surface, words)
        if not node:
            return None
        if surface == 'talk':
            return self.talk('open_record', id=node).get('last')
        if surface == 'mcp':
            return self.mcp('get_graph_record', id=node).get('last_at')
        if surface == 'layer':
            with self.app.store.connect() as db:
                return self.k.last_contact(db, node)
        return self.app.graph_action({'node_id': node}).get('last_at')

    # what did we say about Y: message ids found by words
    def about(self, surface, words):
        if surface == 'chat':
            got = self.app.action('events', {'account_ids': self.accounts(), 'query': words, 'limit': 20})
            return [e['id'] for e in got['events']]
        if surface == 'talk':
            return [int(x['id'].split(':')[1]) for x in self.talk('search', words=words, kind='message').get('found', [])]
        if surface == 'mcp':
            return [m['id'] for m in self.mcp('search_messages', query=words, limit=20).get('messages', [])]
        if surface == 'layer':
            return [r['id'] for r in self.k.search_messages(self.app.store, self.app.config, words, self.caller, 20)]
        raise KeyError(surface)


# ------------------------------------------------------------------ the cases

def cases(ids, store):
    """(name, surfaces, check(surfaces, surface) -> (ok, detail)). Expected answers come from how the data was made,
    never from a surface."""
    with store.connect() as db:
        said = {r[0] for r in db.execute("SELECT id FROM events WHERE deleted=0 AND kind IN (%s) AND (title LIKE '%%rate limit%%' "
                                            "OR body LIKE '%%rate limit%%')" % ','.join('?' * len(MESSAGES)), MESSAGES)}
        wren = {r[0] for r in db.execute("SELECT id FROM promises WHERE who='Wren Fairhaven' AND status='open'")}
        juno_last = db.execute('SELECT max(occurred_at) FROM events WHERE id IN (%s)' % ','.join('?' * len(ids['juno_mail'])), ids['juno_mail']).fetchone()[0]
    newest = lambda key, *more: sorted([i for k in (key, *more) for i in ids[k]], key=lambda i: _at(store, i), reverse=True)
    out = []

    def case(name, surfaces, check):
        out.append((name, surfaces, check))

    every = SURFACES
    for words in ('Mila Underhay', 'mila@northwindanalytics.example', 'mila'):
        case('who: %s' % words, every, lambda s, x, w=words: _same(s.first(x, w), 'email:mila@northwindanalytics.example'))
    case('who: by name, known only by a WhatsApp number', every, lambda s, x: _same(s.first(x, PIM['name']), 'wa:' + PIM['number']))
    for spoken in PIM['spoken']:
        case('who: by phone number "%s"' % spoken, every, lambda s, x, w=spoken: _same(s.first(x, w), 'wa:' + PIM['number']))
    case('who: merged identities are one record', every,
         lambda s, x: _same([i for i in s.find(x, KAI['name'])], ['email:' + KAI['email']]))
    case('who: nobody by that name is said plainly', every, lambda s, x: _same(s.find(x, NOBODY), []))

    latest = ('chat', 'talk', 'mcp', 'page', 'layer')
    case('latest: known only by a WhatsApp number', latest, lambda s, x: _same(s.latest(x, PIM['name'])[0], newest('pim')))
    case('latest: many meetings ahead never crowd out the latest messages', latest,
         lambda s, x: _same(s.latest(x, JUNO['name'])[0], newest('juno_mail')))
    case('latest: every merged identity, newest first', latest, lambda s, x: _same(s.latest(x, KAI['name'])[0], newest('kai_chat', 'kai_mail')[:5]))
    case('latest: a thread held back from connected AIs is the owner\'s to read', ('chat', 'talk', 'page', 'layer'),
         lambda s, x: _same(s.latest(x, RHEA['name'])[0], newest('rhea_open', 'rhea_held')))
    case('latest: nobody by that name says what was searched', ('talk',),
         lambda s, x: _check(s.latest(x, NOBODY)[1].get('searched') and not s.latest(x, NOBODY)[0], s.latest(x, NOBODY)[1]))

    opens = ('chat', 'talk', 'mcp', 'page', 'layer')
    case('open: promises both ways with a person', opens, lambda s, x: _same(s.open(x, 'Wren Fairhaven')[0], wren))
    case('open: an organization has its people\'s promises', opens, lambda s, x: _check(wren <= s.open(x, 'Harborline Health')[0], s.open(x, 'Harborline Health')[0]))
    case('last: the latest contact, never a meeting ahead', ('chat', 'mcp', 'page', 'layer'), lambda s, x: _same(str(s.last(x, JUNO['name']))[:10], juno_last[:10]))
    case('last: Talk says the latest contact, never a meeting ahead', ('talk',),
         lambda s, x: _same(s.last(x, JUNO['name']), s.app.talk_when(juno_last)))
    case('about: what was said about rate limits', ('chat', 'talk', 'mcp', 'layer'), lambda s, x: _check(said and said <= set(s.about(x, 'rate limit')), sorted(s.about(x, 'rate limit'))))
    return out


def _at(store, event_id):
    with store.connect() as db:
        return db.execute('SELECT occurred_at FROM events WHERE id=?', (event_id,)).fetchone()[0]


def _same(got, want):
    return got == want, got


def _check(ok, detail):
    return bool(ok), detail


def visibility_cases(ids):
    """A Work-only connection never sees a Personal person or their messages; the owner (Talk) does."""
    return [
        ('work only: a Personal person stays out', lambda s, x: _same(s.find(x, PIM['name']), [])),
        ('work only: a Personal person\'s messages stay out', lambda s, x: _same(s.latest(x, KAI['name'])[0], [])),
        ('work only: Personal promises and to-dos stay out', lambda s, x: _same(s.open(x, KAI['name']), (set(), set()))),
        ('work only: a thread judged sensitive stays out', lambda s, x: _same(s.latest(x, RHEA['name'])[0], ids['rhea_open'])),
    ]


def run(app, assistant, ids):
    """[(case, surface, ok, detail)] over every case and surface."""
    surfaces = Surfaces(app, assistant)
    results = []
    for name, where, check in cases(ids, app.store):
        for surface in where:
            try:
                ok, detail = check(surfaces, surface)
            except Exception as error:  # a surface that breaks on a question fails that question, the rest still run
                ok, detail = False, '%s: %s' % (type(error).__name__, error)
            results.append((name, surface, ok, detail))
    work = Surfaces(app, assistant, area='work')
    for name, check in visibility_cases(ids):
        for surface in ('mcp', 'layer'):
            try:
                ok, detail = check(work, surface)
            except Exception as error:
                ok, detail = False, '%s: %s' % (type(error).__name__, error)
            results.append((name, surface, ok, detail))
    return results


def report(results, out=sys.stdout):
    width = max(len(r[0]) for r in results)
    names = list(dict.fromkeys(r[0] for r in results))
    print('%-*s  %s' % (width, 'question', '  '.join('%-6s' % s for s in SURFACES)), file=out)
    for name in names:
        row = {r[1]: r[2] for r in results if r[0] == name}
        print('%-*s  %s' % (width, name, '  '.join('%-6s' % ({True: 'ok', False: 'FAIL'}.get(row.get(s), '-')) for s in SURFACES)), file=out)
    passed = sum(1 for r in results if r[2])
    print('\n%d of %d passed' % (passed, len(results)), file=out)
    for s in SURFACES:
        mine = [r for r in results if r[1] == s]
        if mine:
            print('  %-6s %d/%d' % (s, sum(1 for r in mine if r[2]), len(mine)), file=out)


# ------------------------------------------------------------------ a real install, read-only: agreement, counts only

def agreement(app, assistant, sample=40):
    """On a real install's database copy: for its strongest people, the ones with meetings ahead, merged identities and
    WhatsApp-only, does every surface agree with the Graph page? {check: [passed, total]} per surface; no names."""
    surfaces = Surfaces(app, assistant)
    current = now().isoformat()
    with app.store.connect() as db:
        rows = db.execute("SELECT id,name,info,last_at FROM graph_nodes WHERE kind='person' AND name NOT LIKE '%@%' ORDER BY strength DESC LIMIT ?", (sample,)).fetchall()
        ahead = db.execute("SELECT n.id,n.name,n.info,n.last_at FROM graph_nodes n WHERE n.kind='person' AND n.name NOT LIKE '%@%' AND "
                           "(SELECT count(*) FROM graph_events g WHERE g.node_id=n.id AND g.at>?)>=3 ORDER BY n.strength DESC LIMIT ?", (current, sample // 2)).fetchall()
        merged = db.execute("SELECT id,name,info,last_at FROM graph_nodes WHERE kind='person' AND name NOT LIKE '%@%' AND "
                            "json_array_length(json_extract(info,'$.identifiers'))>1 ORDER BY strength DESC LIMIT ?", (sample // 2,)).fetchall()
        whatsapp = db.execute("SELECT id,name,info,last_at FROM graph_nodes WHERE kind='person' AND id LIKE 'wa:%' AND length(id)>10 "
                              "ORDER BY strength DESC LIMIT ?", (sample // 2,)).fetchall()
    tally = {}

    def count(check, surface, ok):
        t = tally.setdefault(check, {}).setdefault(surface, [0, 0])
        t[0] += bool(ok)
        t[1] += 1
    groups = (('strongest', rows), ('meetings ahead', ahead), ('merged', merged), ('whatsapp only', whatsapp))
    for group, people in groups:
        for p in people:
            truth = _page_messages(app, p['id'])
            for surface in SURFACES:
                try:
                    found = surfaces.find(surface, p['name'])
                    count('%s: found by name' % group, surface, p['id'] in found)
                except Exception:
                    count('%s: found by name' % group, surface, False)
            for surface in ('chat', 'talk', 'mcp'):
                try:
                    got = _latest_for(surfaces, surface, p['id'], p['name'])
                    count('%s: latest messages as the Graph page' % group, surface, got == truth[:len(got)] and (len(got) >= min(len(truth), 5) or surface == 'chat'))
                except Exception:
                    count('%s: latest messages as the Graph page' % group, surface, False)
            count('%s: last contact not ahead' % group, 'page', not p['last_at'] or p['last_at'] <= current)
            if group == 'whatsapp only':
                number = re.sub(r'\D', '', p['id'])
                spoken = '+%s %s %s' % (number[:2], number[2:5], number[5:])
                for surface in SURFACES:
                    try:
                        count('whatsapp only: found by phone number', surface, p['id'] in surfaces.find(surface, spoken))
                    except Exception:
                        count('whatsapp only: found by phone number', surface, False)
    return tally


def _page_messages(app, node):
    got = app.graph_timeline(node)
    return [i['id'] for i in got['items'] if i['type'] == 'event' and i.get('kind') in MESSAGES][:5]


def _latest_for(surfaces, surface, node, name):
    """Latest messages through a surface for a record already known by id (the step after finding them)."""
    if surface == 'talk':
        return [int(x['id'].split(':')[1]) for x in surfaces.talk('search', kind='message', person=node).get('found', [])][:5]
    if surface == 'mcp':
        return [m['id'] for m in surfaces.mcp('search_messages', person=node, limit=5).get('messages', [])][:5]
    lines = surfaces.app.graph_action({'node_id': node}).get('recent', [])
    ids = [int(line.split(' ', 1)[0]) for line in lines]
    kinds = {r['id']: r['kind'] for r in surfaces.app.store.events(surfaces.accounts(), event_ids=ids)} if ids else {}
    return [i for i in ids if kinds.get(i) in MESSAGES][:5]


def print_agreement(tally, out=sys.stdout):
    for check, per in tally.items():
        print('%-48s %s' % (check, '  '.join('%s %d/%d' % (s, *per[s]) for s in SURFACES if s in per)), file=out)


# ------------------------------------------------------------------ with a model in the loop (optional, weekly)

LLM_CASES = (
    # (what the owner says, what the answer must name)
    ('What did Pim Ostrava send me last?', ('climbing',)),
    ('Any news from Juno Calloway?', ('rollout',)),
    ('What has Kai Brandt been messaging about?', ('kayak',)),
    ('Did Nobody Zebrafinch write to me?', ('no', 'not', "didn't", 'nothing')),
)


def run_llm(app, model=None):
    """Talk's main tools (search, open_record, calendar) with a model choosing the calls; [(question, ok, answer)]."""
    import urllib.request
    import talk_live
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        raise SystemExit('--llm needs OPENAI_API_KEY')
    tools = [{'type': 'function', 'function': {k: t[k] for k in ('name', 'description', 'parameters')}}
             for t in talk_live.MAIN_TOOLS if t.get('name') in talk_live.MACHINE_TOOLS]
    out = []
    for question, words in LLM_CASES:
        messages = [{'role': 'system', 'content': talk_live.main_instructions('en', now().isoformat())}, {'role': 'user', 'content': question}]
        answer = ''
        for _ in range(6):
            body = json.dumps({'model': model or os.environ.get('KNOWLEDGE_EVAL_MODEL', 'gpt-4.1-mini'), 'messages': messages, 'tools': tools}).encode()
            request = urllib.request.Request('https://api.openai.com/v1/chat/completions', body,
                                             {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(request, timeout=60) as response:
                said = json.load(response)['choices'][0]['message']
            messages.append(said)
            if not said.get('tool_calls'):
                answer = said.get('content') or ''
                break
            for call in said['tool_calls']:
                result = app.talk_machine_tool(call['function']['name'], json.loads(call['function']['arguments'] or '{}'))
                messages.append({'role': 'tool', 'tool_call_id': call['id'], 'content': json.dumps(result)})
        out.append((question, any(w in answer.lower() for w in words), answer))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--db', help='a copy of a real install database (read-only agreement checks)')
    parser.add_argument('--config', help="that install's config.json")
    parser.add_argument('--llm', action='store_true', help='also ask a model through Talk\'s tools (needs OPENAI_API_KEY)')
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    if args.db:
        config = json.loads(Path(args.config).read_text())
        config['database'] = args.db
        import assistant
        uri = sqlite3.connect('file:%s?mode=ro' % args.db, uri=True)
        uri.close()
        print_agreement(agreement(app_for(config, assistant), assistant))
        return
    with tempfile.TemporaryDirectory() as folder:
        config, ids = sandbox(folder)
        import assistant
        app = app_for(config, assistant)
        report(run(app, assistant, ids))
        if args.llm:
            for question, ok, answer in run_llm(app):
                print('%-4s %s  ->  %s' % ('ok' if ok else 'FAIL', question, ' '.join(answer.split())[:160]))


if __name__ == '__main__':
    main()

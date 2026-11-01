"""One brain behind every surface: how the chat, Talk, connected AIs (MCP) and the Graph pages find people,
organizations and projects, their latest messages, what is open with them and when the owner last talked to them.

Every surface asks the same questions ("who is X", "what's going on with X", "latest messages with X", "what did we say
about Y", "open to-dos and promises with X", "when did I last talk to X"). Each used to gather the answer its own way,
so one could miss what another showed (Talk missed a person's WhatsApp messages their Graph page had). The answers
come from here now; each surface only formats them. The rules for who may see what come from the Caller:

- the owner (the chat, Talk, the dashboard): every account, nothing held back;
- a connected AI (ai_app.py): its connection's area (Work, Personal or both), never the owner's own record or a
  teammate's, and messages without what the app holds back (an Only you board or project, threads judged sensitive or
  kept private, and with Work only, threads about the owner's own life).

A record's messages are the ones its Graph page's timeline shows (graph.timeline): every address and number merged
into a person, an organization's people, Intercom on their address. What already happened comes first, newest first;
meetings still ahead never crowd out the latest messages.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import json
import re
import sqlite3

import graph
import shared_graph

KINDS = ('person', 'org', 'project')
NAMED = ('person', 'org')  # what has messages "with" it by name
PHONE_DIGITS = 8  # a phone number is matched on at least this many of its last digits


@dataclasses.dataclass(frozen=True)
class Caller:
    """Who is asking. accounts: the account ids they may read (None: every account); area: None (both), 'work' or
    'personal'; held: whether messages the app holds back stay out (connected AIs); me: whether the owner's own record
    and teammates' records may come back."""
    accounts: frozenset | None = None
    area: str | None = None
    held: bool = False
    me: bool = True

    def account_ids(self, config):
        every = [a['id'] for a in (config or {}).get('accounts', [])]
        return every if self.accounts is None else [a for a in every if a in self.accounts]


OWNER = Caller()


def owner():
    """The owner: every account, nothing held back (the chat, Talk, the dashboard)."""
    return OWNER


def connection(config, area):
    """A connected AI whose connection (or call) sees `area`: None for both, else 'work' or 'personal'."""
    ids = frozenset(a['id'] for a in (config or {}).get('accounts', []) if area is None or graph.account_side(a) == area)
    return Caller(accounts=ids, area=area, held=True, me=False)


# ------------------------------------------------------------------ records

def visible(view, caller):
    """Whether this caller may see a record: a connected AI never the owner's own record or a teammate's, and only its
    area (a person by their side; organizations and projects are Work)."""
    if not view:
        return False
    if not caller.me and (view['id'] == graph.ME or str(view['id']).startswith('team:')):
        return False
    if caller.area is None:
        return True
    if view['kind'] == 'person':
        return view.get('side') == caller.area
    return caller.area == 'work'


def digits(text):
    return re.sub(r'\D', '', str(text or ''))


def _phone_hits(db, said, kinds):
    """Records with this phone number, however it is written ("+32 470 00 01 02", "0470 00 01 02", "32470000102"):
    their last digits against the numbers in their ids and identifiers."""
    tail = digits(said)[-9:]
    if len(tail) < PHONE_DIGITS:
        return []
    marks = ','.join('?' for _ in kinds)
    out = []
    for r in db.execute(f'SELECT * FROM graph_nodes WHERE kind IN ({marks}) ORDER BY strength DESC', tuple(kinds)):
        try:
            info = json.loads(r['info'] or '{}')
        except ValueError:
            info = {}
        numbers = [x for x in (r['id'], *(info.get('identifiers') or ())) if str(x).startswith('wa:')] + list(info.get('phones') or ())
        if any(digits(x).endswith(tail) for x in numbers if len(digits(x)) >= PHONE_DIGITS):
            out.append(r)
    return out


def looks_like_phone(text):
    text = str(text or '').strip()
    return bool(re.fullmatch(r'[+\d][\d\s().-]{6,}', text)) and len(digits(text)) >= PHONE_DIGITS


def find(db, words, caller=OWNER, kinds=KINDS, limit=10, also=None):
    """People, organizations and projects for a name, an address, a handle or a phone number, strongest first, that
    this caller may see: graph rows. also: more text per record to match (a Fleet member's name)."""
    kinds = tuple(k for k in kinds if k in KINDS) or KINDS
    try:
        # a number is matched as a number, whatever way it is written; anything else by its words
        hits = _phone_hits(db, words, kinds) if looks_like_phone(words) else graph.find(db, words, max(limit * 3, limit + 10), kinds, also=also)
    except sqlite3.OperationalError:
        return []  # no Graph yet
    return [r for r in hits if visible(graph.node_view(r), caller)][:limit]


def named(db, words, caller=OWNER, kinds=NAMED, also=None):
    """The record these words name: every word in its name (or the phone number it has), strongest first; None. "kim"
    names Kim Vale; "the latest from Kim" doesn't name anyone, so a search by meaning stays a search by meaning."""
    said = [w for w in re.findall(r'\w+', str(words or '').casefold()) if len(w) > 1]
    if looks_like_phone(words):
        hits = find(db, words, caller, kinds, 3, also)
        return hits[0] if hits else None
    if not said or len(said) > 5:
        return None
    for r in find(db, words, caller, kinds, 10, also):
        if set(said) <= set(re.findall(r'\w+', str(r['name'] or '').casefold())):
            return r
    return None


def record(db, ref, caller=OWNER, kinds=KINDS, also=None):
    """One record by its id, by an identifier merged into a person (an old link), or by the name or number that names
    it; None when there is none this caller may see."""
    ref = ' '.join(str(ref or '').split())
    if not ref:
        return None
    if re.fullmatch(r'[a-z]+:\S+', ref):
        try:
            row = graph.resolve(db, ref)
        except sqlite3.OperationalError:
            return None
        row = row if row and row['kind'] in kinds else None
    else:
        row = named(db, ref, caller, tuple(k for k in kinds if k in NAMED) or NAMED, also)
    return row if row and visible(graph.node_view(row), caller) else None


def last_contact(db, node_id):
    """When the owner last had contact with a record (an ISO moment): its latest signal that already happened, never a
    meeting still ahead; for an organization, its people's. None when there was none."""
    row = graph.resolve(db, node_id)
    if not row:
        return None
    nodes = _members(db, row)
    current = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    found = db.execute(f"SELECT max(e.occurred_at) FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id IN "
                       f"({','.join('?' * len(nodes))}) AND e.deleted=0 AND e.occurred_at<=?", (*nodes, current)).fetchone()[0]
    return found or row['last_at']


# ------------------------------------------------------------------ messages

def held(db, rows, area=None):
    """The event ids among rows a connected AI never reads: an Only you board's or project's (graph.hidden_event_ids),
    threads the review judged sensitive or the owner kept private, and with Work only, threads about the owner's own
    life (shared_graph's calls, share_threads)."""
    out = set(graph.hidden_event_ids(db)) & {r['id'] for r in rows}
    try:
        calls = {r[0]: (r[1], r[2]) for r in db.execute('SELECT thread,verdict,hand FROM share_threads')}
    except sqlite3.OperationalError:
        calls = {}  # no Shared Graph here
    for r in rows:
        meta = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        verdict, hand = calls.get(shared_graph.thread_of(r['kind'], meta, r['id']), (None, None))
        if verdict == 'sensitive' or hand == 'private' or (verdict == 'personal' and area == 'work'):
            out.add(r['id'])
    return out


def readable(store, config, caller, rows):
    """rows as this caller may read them: on its accounts, without what is held back for it."""
    allowed = set(caller.account_ids(config))
    rows = [r for r in rows if r['account_id'] in allowed]
    if caller.held and rows:
        with store.connect() as db:
            out = held(db, rows, caller.area)
        rows = [r for r in rows if r['id'] not in out]
    return rows


def latest_messages(store, config, node_id, caller=OWNER, limit=10, query='', kinds=None):
    """A record's latest messages (Store.events rows), newest first, the ones its Graph page's timeline shows: every
    address and number merged into a person, an organization's people. query narrows them to these words; kinds to
    these event kinds. Never a meeting, never anything still ahead."""
    accounts = caller.account_ids(config)
    if not accounts:
        return []
    with store.connect() as db:
        ids = graph.recent_messages(db, node_id, 200)
    if not ids:
        return []
    rows = store.events(accounts, query=query, event_ids=ids, **({'kinds': list(kinds)} if kinds else {}))
    place = {e: i for i, e in enumerate(ids)}
    rows = sorted(readable(store, config, caller, rows), key=lambda r: place.get(r['id'], len(place)))
    return rows[:max(1, int(limit))]


def search_messages(store, config, words, caller=OWNER, limit=10, kinds=None):
    """Messages with these words, newest first, as this caller may read them (Store.events' word search)."""
    accounts = caller.account_ids(config)
    if not accounts:
        return []
    rows = store.events(accounts, query=words, limit=max(1, int(limit)) * 3, kinds=list(kinds or graph.MESSAGE_KINDS))
    return readable(store, config, caller, rows)[:max(1, int(limit))]


# ------------------------------------------------------------------ what is open

def _members(db, row):
    if row['kind'] != 'org':
        return [row['id']]
    return [row['id'], *(r[0] for r in db.execute("SELECT a FROM graph_links WHERE b=? AND kind='member'", (row['id'],)))]


def open_with(store, config, node_id, caller=OWNER, limit=10):
    """What is open between the owner and a record, as its Graph page has it (graph.open_between): promises both ways
    and open to-dos, for an organization also its people's; only those on this caller's accounts and area.
    {'you_promised': [...], 'they_promised': [...], 'todos': [...]}, each item with its id."""
    out = {'you_promised': [], 'they_promised': [], 'todos': []}
    with store.connect() as db:
        row = graph.resolve(db, node_id)
        if not row:
            return out
        seen = {k: set() for k in out}
        for node in _members(db, row):
            found = graph.open_between(db, node, limit)
            for key, src in (('you_promised', 'you_promised'), ('they_promised', 'they_promised'), ('todos', 'cards')):
                for item in found.get(src) or ():
                    if item['id'] not in seen[key]:
                        seen[key].add(item['id'])
                        out[key].append(dict(item))
        if caller.accounts is not None:
            allowed = caller.accounts
            ids = [p['id'] for p in out['you_promised'] + out['they_promised']]
            on = {r[0]: r[1] for r in db.execute(f"SELECT id,account_id FROM promises WHERE id IN ({','.join('?' * len(ids)) or 'NULL'})", ids)}
            for key in ('you_promised', 'they_promised'):
                out[key] = [p for p in out[key] if on.get(p['id']) in allowed]
            cards = [t['id'] for t in out['todos']]
            areas = {r[0]: r[1] for r in db.execute(f"SELECT id,account_ids FROM suggestions WHERE id IN ({','.join('?' * len(cards)) or 'NULL'})", cards)}
            out['todos'] = [t for t in out['todos'] if _card_visible(config, areas.get(t['id']), caller)]
    return {k: v[:limit] for k, v in out.items()}


def card_area(config, account_ids):
    """A to-do's area: Work when any of its accounts is Work, else Personal."""
    ids = json.loads(account_ids or '[]') if isinstance(account_ids, str) else (account_ids or [])
    return 'work' if any(graph.account_side(a) == 'work' for a in (config or {}).get('accounts', []) if a['id'] in ids) else 'personal'


def _card_visible(config, account_ids, caller):
    if caller.area is None:
        return True
    mine = json.loads(account_ids or '[]') if isinstance(account_ids, str) else list(account_ids or [])
    return card_area(config, mine) == caller.area and bool(set(mine) & set(caller.accounts or ()))


# ------------------------------------------------------------------ earlier conversations

RECALL_SECONDS = 8   # the most a recall waits for OpenClaw's memory search (Node, the Gateway, the search): Talk waits on it
RECALL_LIMIT = 5
RECALL_SOURCES = {'sessions': 'an earlier conversation', 'memory': 'the notes'}


def recall_allowed(caller):
    """Whether this caller may recall earlier conversations: only one that sees everything (the owner across Work and
    Personal). Transcripts and memory notes carry no account, area or Only you mark, so they can't be cut to an area:
    a connected AI, or anything asked for one area, gets nothing."""
    return caller.accounts is None and caller.area is None and not caller.held and caller.me


def recall(search, words, caller=OWNER, limit=RECALL_LIMIT):
    """What the owner said or decided in earlier conversations with The Machine, and its notes: OpenClaw's memory
    search (memory files, and past conversation transcripts where that is on), by meaning or by keywords as the Machine
    has it. search(request) runs it (memory-recall-run.mjs) and answers {'results': [...]} or {'error'}.

    [{'source': 'sessions' or 'memory', 'from': in words, 'text', 'at': ISO moment or None, 'origin'}], best first. The
    text can quote anyone (a message pasted in a chat, a review of someone's mail): untrusted, for the surface to mark.
    [] when the caller may not recall (recall_allowed), memory search is off, or it fails or is slow: never an error."""
    words = ' '.join(str(words or '').split())[:300]
    if not words or not recall_allowed(caller):
        return []
    try:
        found = search({'query': words, 'max_results': max(1, min(int(limit), 8)), 'timeout_ms': (RECALL_SECONDS - 1) * 1000})
    except Exception:  # noqa: BLE001 - recall is a nice-to-have: whatever breaks, the answer is nothing
        return []
    rows = found.get('results') if isinstance(found, dict) else None
    out = []
    for r in rows if isinstance(rows, list) else ():
        if not isinstance(r, dict) or not str(r.get('text') or '').strip():
            continue
        source = 'sessions' if r.get('source') == 'sessions' else 'memory'
        at = None
        # When it was said: a transcript's moment. A note's is when it was indexed, not when it was written, so none.
        if source == 'sessions' and isinstance(r.get('at'), (int, float)) and r['at'] > 0:
            try:
                at = dt.datetime.fromtimestamp(r['at'] / 1000, dt.timezone.utc).isoformat(timespec='seconds')
            except (OverflowError, OSError, ValueError):
                at = None
        out.append({'source': source, 'from': RECALL_SOURCES[source], 'text': str(r['text']).strip()[:1200], 'at': at,
                    'origin': r.get('origin') if r.get('origin') in ('owner', 'agent', 'untrusted') else 'unknown'})
    return out[:max(1, int(limit))]

"""What Ask reads besides messages (search_ask.py): the promises the Machine tracks, what it learned, its summary of a
person, organization or project, and meeting notes. Each is a block of the `ask` purpose (machine/app/recall.py), so
it is fitted to the prompt's budget and logged like the rest (memory_use.py).

Only what matches the question goes in, and nothing when nothing matches: the prompt is then the one it was.
- What it is about (subjects): the person the first turn read, and each organization or project the question names.
- promises: open ones and those closed in the last CLOSED_DAYS days whose message is one the search found, or is on
  one of those records. A question about some days gets the ones said or due in those days.
- facts: the ones tied to those records, then the closest in meaning to the question (the stored fact vectors
  against the question's own, as a preparation ranks them: local embeddings, no model turn). Without embeddings (or
  when the embedding server fails) the owner's own facts that share the question's words instead (matching), so a
  fact about no one, like one about the owner themselves, is still found.
- records: the person's summary lines of the area in view, a project's stage and next step, an organization's role.
- meetings: the meeting notes the search found for the question (Ask kept only messages of what it found), or the
  ones the Graph has that person on.

Privacy is Ask's own: only the connections of the area in view (All, Work or Personal), with Work never a thread
judged to be about the owner's own life, a summary's lines only of that area, and a connected AI's fact only of that
area. Nothing from the Fleet or a teammate. Each line has its own tag ([P1] a promise, [F1] something learned, [S1] a
summary, [M1] meeting notes), so the answer cites it as what it is and never as a message."""
import datetime as dt
import functools
import json
import logging
import re
import sqlite3
import unicodedata

import embeddings
import fact_links
import graph
import memory_use
import person_summary
from machine.app import retained_facts
from machine.store.facts import COMMON, ai_fact_by, fact_line, fact_weight, fact_words, key_words, note_facts, with_about, word_match
from machine.store.promises import promise_card, promise_state, who_named
from machine.text import shown_body
from timeutil import now

LOG = logging.getLogger('personal-assistant')

MEMORY_CHARS = 1600   # all four blocks together at most: about 400 tokens, inside the prompt's own limit
PROMISES = 4
PROMISE_HITS = 3          # a promise the question's records don't have: only on one of the search's best messages
FACTS = 3
MEETINGS = 2
CLOSED_DAYS = 30      # a promise closed longer ago is no longer brought up
PROMISE_CHARS = 220
FACT_CHARS = 260
SUMMARY_CHARS = 500
MEETING_CHARS = 450   # of one meeting's notes: the part that matched
FACT_FLOOR = 0.6           # cosine of a fact to the question: under it the fact is not about the question (unrelated ones reach 0.5)
LEARNED = 3           # facts and rules Talk's recall gets for its words (learned)
LEARNED_TIMEOUT = 2   # seconds for the words' vector in Talk's recall; slower, and words only (a voice waits on it)
FACT_TIMEOUT = 4      # seconds for the question's vector; slower, and no fact is ranked
NAMED = 2             # organizations and projects named in one question
NAME_LETTERS = 4      # a name's first word counts alone from this many letters, when no other record has it
MEETING_KINDS = tuple(sorted(embeddings.PASSAGE_KINDS - set(graph.MESSAGE_KINDS)))
ORDER = ('promises', 'facts', 'records', 'meetings')
INTRO = ("Also from The Machine's own memory, matching the question. P: a promise it tracks, F: something it learned, "
         "S: its summary of a person, organization or project, M: meeting notes. They count like the messages. After a "
         "fact from one put its own tag, like [P1], never a message's number.")


class Block(str):
    """A block's text for the prompt, with what each of its lines is (entries: {'tag', 'type', 'id', 'title', 'at'})."""
    entries = ()


def _block(lines, entries):
    out = Block('\n'.join(lines))
    out.entries = list(entries)
    return out


def _data(text):
    return ' '.join(str(text or '').replace('<<<', '').replace('>>>', '').split())


def _fold(text):
    return re.findall(r'[a-z0-9]+', unicodedata.normalize('NFKD', str(text or '')).encode('ascii', 'ignore').decode().casefold())


def _marks(values):
    return ','.join('?' * len(values))


def _on(db, nodes):
    """The records whose signals count for these: each one itself, and for an organization its people."""
    nodes = list(nodes)
    orgs = [n for n in nodes if str(n).startswith('org:')]
    if orgs:
        nodes += [r[0] for r in db.execute(f"SELECT a FROM graph_links WHERE kind='member' AND b IN ({_marks(orgs)})", orgs)]
    return list(dict.fromkeys(nodes))


def _in_area(db, node, accounts):
    """Whether the area's connections have a signal on this record: one known only from the other area stays out."""
    nodes = _on(db, [node])
    return bool(db.execute(f'SELECT 1 FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id IN ({_marks(nodes)}) AND g.probable=0 '
                           f'AND e.deleted=0 AND e.account_id IN ({_marks(accounts)}) LIMIT 1', (*nodes, *accounts)).fetchone())


def named(db, question, accounts):
    """The organizations and projects the question names, strongest first: every word of the name is in it, or the
    name's first word is and no other person, organization or project has that word. Names only, never a guess from
    what the words mean."""
    asked = set(_fold(question))
    if not asked or not accounts:
        return []
    rows = db.execute("SELECT id,kind,name FROM graph_nodes WHERE kind IN ('org','project') ORDER BY strength DESC,rowid").fetchall()
    found, firsts = [], {}
    for r in rows:
        words = _fold(r['name'])
        if not words or len(''.join(words)) < 3:
            continue
        if set(words) <= asked:
            found.append(r)
        elif len(words) > 1 and len(words[0]) >= NAME_LETTERS and words[0] in asked:
            firsts.setdefault(words[0], []).append(r)
    for word, group in firsts.items():
        if len(group) > 1 or any(set(_fold(r['name'])) <= asked for r in found if word in _fold(r['name'])):
            continue
        shared = db.execute("SELECT count(*) FROM graph_nodes WHERE id!=? AND lower(name) LIKE ?", (group[0]['id'], f'%{word}%')).fetchone()[0]
        if not shared:
            found.append(group[0])
    return [{'id': r['id'], 'kind': r['kind'], 'name': r['name']} for r in found if _in_area(db, r['id'], accounts)][:NAMED]


def context(app, question, area, scope=None, hits=(), starts=None, days=None, best=()):
    """What the pickers go on, read once per question: the area's connections, the records it is about, the search's
    own hits (event ids, best first, messages or not) and the days asked about."""
    accounts = app.search_ask_accounts(area)
    subjects = []
    try:
        with app.store.connect() as db:
            node = (scope or {}).get('node')
            if node and accounts:
                subjects.append({'id': node, 'kind': 'person', 'name': scope.get('name') or '', 'scoped': True})
            subjects += named(db, question, accounts)
    except sqlite3.Error as error:  # no Graph yet: the question is then about no record
        LOG.info('ask memory subjects error=%s', type(error).__name__)
    return {'question': question, 'area': area, 'accounts': accounts, 'subjects': subjects, 'hits': [int(i) for i in hits or ()], 'best': [int(i) for i in best or ()][:PROMISE_HITS],
            'starts': dict(starts or {}), 'days': days if days and any(days) else None,
            'keep': lambda rows: app.search_ask_keep(rows, area)}


def _within(value, days):
    if not days:
        return True
    try:
        at = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except ValueError:
        return False
    at = at if at.tzinfo else at.replace(tzinfo=dt.timezone.utc)
    start, until = (dt.datetime.fromisoformat(d) if d else None for d in days)
    return (not start or at >= start) and (not until or at < until)


def _lines(found, room, line_of):
    """(lines, entries) of the found ones that fit in room characters, whole lines only, tagged in order. Only a line
    that goes in is noted for the log."""
    lines, entries, used = [], [], 0
    for item in found:
        note, tag, line, entry = line_of(len(entries) + 1, item)
        if used + len(line) + 1 > room:
            break
        note()
        lines.append(line)
        entries.append({'tag': tag, **entry})
        used += len(line) + 1
    return lines, entries


def promises(app, about, room):
    """Open and lately closed promises on the question's records or on a message the search found for it."""
    accounts, nodes, hits = about['accounts'], [s['id'] for s in about['subjects']], set(about['best'])
    if not accounts or not (nodes or hits):
        return _block([], [])
    since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=CLOSED_DAYS)).isoformat()
    with app.store.connect() as db:
        rows = [dict(r) for r in db.execute(
            'SELECT p.id,p.direction,p.who,p.what,p.due,p.status,p.event_id,p.updated_at,p.together,p.suggestion_id,e.occurred_at made_at,e.kind,e.metadata,'
            's.status card_status FROM promises p JOIN events e ON e.id=p.event_id LEFT JOIN suggestions s ON s.id=p.suggestion_id '
            f"WHERE e.deleted=0 AND p.account_id IN ({_marks(accounts)}) AND (p.status IN ('open','carded') OR p.updated_at>=?) "
            'ORDER BY e.occurred_at DESC,p.id DESC', (*accounts, since))]
        on = set()
        if nodes and rows:
            nodes = _on(db, nodes)
            on = {r[0] for r in db.execute(f'SELECT DISTINCT event_id FROM graph_events WHERE probable=0 AND node_id IN ({_marks(nodes)}) '
                                           f'AND event_id IN ({_marks(rows)})', (*nodes, *(r["event_id"] for r in rows)))}
        rows = [r for r in rows if r['event_id'] in on or r['event_id'] in hits]
        for r in rows:
            r['who'] = who_named(db, r['who'])
            if r['status'] == 'carded':  # the to-do it is now (the one it was merged into), as the promises page reads it
                card = promise_card(db, r['suggestion_id'])
                r['card_status'] = card['status'] if card else None
    kept = {r['id'] for r in about['keep']([{'id': r['event_id'], 'kind': r['kind'], 'metadata': r['metadata']} for r in rows])}
    found = []
    for r in rows:
        r['state'] = promise_state(r)
        day = (r['due'] + 'T12:00:00+00:00') if r['due'] else ''
        if r['event_id'] in kept and (_within(r['made_at'], about['days']) or (day and _within(day, about['days']))):
            found.append(r)
    found.sort(key=lambda r: (r['event_id'] not in on, r['state'] not in ('open', 'card')))  # on the record first, open first, newest first
    states = {'open': 'open', 'card': 'open, a to-do now', 'kept': 'kept', 'dropped': 'dropped', 'answered': 'answered'}

    def line_of(n, p):
        tag = f'P{n}'
        who = f"the owner together with {_data(p['who'])}" if p.get('together') else \
            f"the owner to {_data(p['who'])}" if p['direction'] == 'mine' else f"{_data(p['who'])} to the owner"
        line = (f"[{tag}] Promise by {who}, {states.get(p['state'], p['state'])}, {'due ' + p['due'] if p['due'] else 'no date'}, "
                f"said {str(p['made_at'])[:10]}: <<<{_data(p['what'])[:PROMISE_CHARS]}>>>")
        note = lambda: memory_use.note('promise', p['id'], line, 'about' if p['event_id'] in on else 'search', about=nodes if p['event_id'] in on else (),
                        source='signal', at=p['made_at'])
        return note, tag, line, {'type': 'promise', 'id': p['id'], 'title': _data(p['what'])[:160], 'from': p['who'], 'at': str(p['made_at'] or '')[:32],
                           'state': p['state']}
    return _block(*_lines(found[:PROMISES], room, line_of))


def _closest(app, about, facts):
    """{fact id: cosine} of the facts close in meaning to the question, from their stored vectors and the question's
    own (one local embedding request, with the facts that have no vector yet); None when embeddings don't run here
    or the embedding server is down or slow, so the facts are matched by words instead."""
    settings = embeddings.settings(app.config)
    if not settings:
        return None
    if not facts:
        return {}
    try:
        return {f['id']: score for score, f in app.store.facts_ranked(embeddings.QUERY_PREFIX + about['question'], facts, settings, FACT_TIMEOUT)}
    except Exception as error:  # the embedding server is down or slow: the words instead, the rest of the answer as it was
        LOG.info('ask memory facts error=%s', type(error).__name__)
        return None


def facts(app, about, room):
    """What was learned about the question's records, then what is closest in meaning to the question, or without
    embeddings the owner's own facts that share its words (matching)."""
    area, nodes, at = about['area'], [s['id'] for s in about['subjects']], now()
    known = [f for f in app.store.facts() if f['kind'] == 'fact' and (area is None or f.get('side') in (None, area)) and fact_weight(f, at) > 0]
    if not known or not about['accounts']:
        return _block([], [])
    tied = {}
    if nodes:
        with app.store.connect() as db:
            nodes = _on(db, nodes)  # an organization's facts are also the ones on its people
            for r in db.execute(f'SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL AND node_id IN ({_marks(nodes)})', nodes):
                tied.setdefault(r['fact_id'], []).append(r['node_id'])
    rest = [f for f in known if f['id'] not in tied]
    closest = _closest(app, about, rest)
    how = 'closeness' if closest is not None else 'match'
    if closest is None:  # no meaning here: by words, and only what the owner said, never a connected AI's
        scores = {f['id']: s for s, f in matching([f for f in rest if not ai_fact_by(f)], about['question'])}
    else:
        scores = {i: s for i, s in closest.items() if s >= FACT_FLOOR}
    asked = {s['id'] for s in about['subjects']}
    found = sorted((f for f in known if f['id'] in tied), key=lambda f: (bool(asked & set(tied[f['id']])), f['created_at']), reverse=True) \
        + sorted((f for f in known if f['id'] in scores), key=lambda f: -scores[f['id']])

    def line_of(n, f):
        tag = f'F{n}'
        line = f"[{tag}] Learned {str(f.get('confirmed_at') or f['created_at'])[:10]}: <<<{_data(fact_line(f)[2:])[:FACT_CHARS]}>>>"
        note = lambda: memory_use.note('fact', f['id'], line, 'about' if f['id'] in tied else how, about=tied.get(f['id'], ()),
                        source='ai' if ai_fact_by(f) else 'note' if f.get('suggestion_id') else 'review', at=f.get('created_at'),
                        score=scores.get(f['id']), used=True)
        return note, tag, line, {'type': 'fact', 'id': f['id'], 'title': _data(f['text'])[:160], 'from': '', 'at': str(f.get('created_at') or '')[:32]}
    return _block(*_lines(found[:FACTS], room, line_of))


def _record(db, subject, about):
    """(name, line) for one record; ('', '') when the Machine keeps nothing specific on it in this area."""
    row = db.execute('SELECT * FROM graph_nodes WHERE id=?', (subject['id'],)).fetchone()
    if not row:
        return '', ''
    view = graph.node_view(row)
    name = _data(view['name'] or subject.get('name'))
    if row['kind'] == 'person':
        sides = {about['area']} if about['area'] else {'work', 'personal'}
        try:
            lines = person_summary.prep_lines(db, row['id'], sides)
        except (sqlite3.Error, ValueError, KeyError, TypeError):
            lines = []
        text = ''
        for line in lines:
            if len(text) + len(line) + 1 > SUMMARY_CHARS:
                break
            text += (' ' if text else '') + _data(line)
        org = db.execute('SELECT name FROM graph_nodes WHERE id=?', (view['org'],)).fetchone() if view.get('org') else None
        who = ', '.join(b for b in (_data(view.get('role')), org and 'at ' + _data(org['name'])) if b)
        return (name, f"Summary of {name}{' (' + who + ')' if who else ''}: <<<{text}>>>") if text else ('', '')
    if row['kind'] == 'project':
        try:
            p = graph.project_row(db, row['id'])
        except (sqlite3.OperationalError, ValueError):
            p = None
        if not p or not (p['stage'] or p['next_step']):
            return '', ''
        seen = lambda event: bool(event) and bool(db.execute(  # its reason and next step come from a message: only one of this area
            f'SELECT 1 FROM events WHERE id=? AND deleted=0 AND account_id IN ({_marks(about["accounts"])})', (event, *about['accounts'])).fetchone())
        bits = ([f"stage {_data(p['stage'])}" + (f" ({_data(p['stage_reason'])})" if p['stage_reason'] and seen(p['stage_event_id']) else '')] if p['stage'] else []) \
            + ([f"next step: {_data(p['next_step'])}"] if p['next_step'] and seen(p['next_step_event_id']) else []) \
            + [f"{view['state']}, last signal {str(view['last_at'] or '')[:10] or 'never'}"]
        return name, f"Project {name}: <<<{'; '.join(bits)[:SUMMARY_CHARS]}>>>"
    bits = [b for b in (_data(view.get('role')), _data(view.get('about'))) if b]
    return (name, f"Organization {name}: <<<{'; '.join(bits)[:SUMMARY_CHARS]}>>>") if view.get('role') else ('', '')


def records(app, about, room):
    """The summary of the person the question is about, and the project or organization it names."""
    found = []
    if about['subjects']:
        with app.store.connect() as db:
            for subject in about['subjects']:
                try:
                    name, text = _record(db, subject, about)
                except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
                    LOG.info('ask memory record error=%s', type(error).__name__)
                    name, text = '', ''
                if text:
                    found.append((subject, name, text))

    def line_of(n, item):
        subject, name, text = item
        tag = f'S{n}'
        line = f'[{tag}] {text}'
        note = lambda: memory_use.note('record', subject['id'], line, 'about' if subject.get('scoped') else 'match', about=(subject['id'],), source='signal')
        return note, tag, line, {'type': subject['kind'], 'id': subject['id'], 'title': name[:160], 'from': '', 'at': ''}
    return _block(*_lines(found, room, line_of))


def meetings(app, about, room):
    """The meeting notes the search found for the question, else the newest ones the Graph has its person on."""
    accounts, hits = about['accounts'], about['hits']
    if not accounts:
        return _block([], [])
    how, ids = 'search', hits
    scoped = [s['id'] for s in about['subjects'] if s.get('scoped')]
    if scoped:  # a question about one person: their meetings, in the days asked about
        how = 'about'
        sql = (f'SELECT e.id FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id=? AND g.direct=1 AND g.probable=0 AND e.deleted=0 '
               f'AND e.account_id IN ({_marks(accounts)}) AND e.kind IN ({_marks(MEETING_KINDS)})')
        args = [scoped[0], *accounts, *MEETING_KINDS]
        for bound, mark in zip(about['days'] or (), ('>=', '<')):
            if bound:
                sql += f' AND e.occurred_at{mark}?'
                args.append(bound)
        with app.store.connect() as db:
            ids = [r[0] for r in db.execute(sql + ' ORDER BY e.occurred_at DESC LIMIT ?', (*args, MEETINGS * 2))]
    if not ids:
        return _block([], [])
    rows = app.store.events(accounts, event_ids=ids, kinds=list(MEETING_KINDS))
    place = {e: n for n, e in enumerate(ids)}
    rows = sorted((r for r in about['keep'](rows) if _within(r['occurred_at'], about['days'])), key=lambda r: place.get(r['id'], len(place)))

    def line_of(n, r):
        tag = f'M{n}'
        body = ' '.join(shown_body(r['body'] or '')[0].split())
        text = embeddings.passage_text(body, about['starts'].get(r['id'], 0), MEETING_CHARS) if how == 'search' else body[:MEETING_CHARS]
        title = ' '.join(str(r['title'] or '').split())[:160]
        line = f"[{tag}] Meeting notes, {str(r['occurred_at'])[:10]}: {_data(title)}\n<<<{_data(text)}>>>"
        note = lambda: memory_use.note('signal', r['id'], line, how, source='signal', at=r['occurred_at'])
        return note, tag, line, {'type': 'meeting', 'id': r['id'], 'title': title, 'from': '', 'at': str(r['occurred_at'] or '')[:32], 'kind': r['kind']}
    return _block(*_lines(rows[:MEETINGS], room, line_of))


BLOCKS = {'promises': promises, 'facts': facts, 'records': records, 'meetings': meetings}


def add(memory, app):
    """Puts the four blocks on an `ask` recall (machine/app/recall.py)."""
    for name in ORDER:
        memory.add(name, functools.partial(BLOCKS[name], app))


def read(memory, about, budget):
    """The four blocks for the prompt, each fitted (Recalled.fit) to what is left of MEMORY_CHARS inside the prompt's
    budget: (text, entries by tag). ('', {}) when nothing matched: the prompt is then the one without them."""
    parts, entries, used = [], {}, len(INTRO) + 1
    for name in ORDER:
        try:
            text = memory.fit(name, used, budget - MEMORY_CHARS, about, MEMORY_CHARS - used)
        except (sqlite3.Error, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:  # one block never costs the answer
            LOG.warning('ask memory block=%s error=%s', name, type(error).__name__)
            memory.drop(name)
            continue
        if text:
            parts.append(text)
            used += len(text) + 1
            entries.update({e['tag']: e for e in text.entries})
    return ('\n'.join([INTRO, *parts]), entries) if parts else ('', {})


def _stem(word):
    """A word's plain form, cheaply and the same for both sides of a match: plurals, -ing and -ed off, a doubled last
    letter and a final e dropped ("seats", "seat" > seat; "booking", "booked", "books" > book; "quoting", "quotes" >
    quot). No word list and no model: a word that changes its stem ("flying", "flights") matches by meaning only."""
    w = word
    if len(w) > 4 and w.endswith('ies'):
        w = w[:-3] + 'y'
    elif len(w) > 4 and w.endswith(('ches', 'shes', 'xes', 'zes')):
        w = w[:-2]
    elif len(w) > 3 and w.endswith('s') and not w.endswith(('ss', 'us', 'is')):
        w = w[:-1]
    if len(w) > 5 and w.endswith('ing'):  # after the plural: "meetings" > meet
        w = w[:-3]
    elif len(w) > 4 and w.endswith('ed') and not w.endswith('eed'):
        w = w[:-2]
    if w != word and len(w) > 3 and w[-1] == w[-2] and w[-1] not in 'lsz':  # planned > plan, running > run
        w = w[:-1]
    if len(w) > 3 and w.endswith('e') and not w.endswith('ee'):
        w = w[:-1]
    return w


def _stems(words):
    """fact_words in their plain form (_stem), so "seat" finds "seats" and "booking" finds "booked"."""
    return {_stem(w) for w in words}


def _shared(asked, text):
    """How many of the words' content words (asked, _stems) a text has: 0 under half of them."""
    shared = len(asked & _stems(fact_words(text)))
    return shared if shared and 2 * shared >= len(asked) else 0


# Words of how a question is asked, not what it is about: they never make a fact match (matching).
QUESTION_WORDS = {'who', 'whom', 'whose', 'what', 'when', 'where', 'why', 'how', 'which', 'do', 'does', 'did', 'done', 'doing',
          'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'you', 'your', 'yours', 'was', 'were', 'am', 'been',
          'can', 'shall', 'may', 'might', 'must', 'has', 'had', 'get', 'got', 'any', 'tell', 'know', 'remember', 'again',
          'usually', 'ever', 'there', 'here', 'from', 'up', 'out', 'so', 'if', 'all', 'now', 'go', 'goes', 'going', 'went',
          'come', 'comes', 'take', 'takes', 'put', 'say', 'said', 'see', 'thing', 'things'}


def _distinct(text):
    """The words of a text that say what it is about, short ones too ("gym", "car", "tax"), in their plain form:
    content words without filler, question words or common ones, never a word list's length cut."""
    return _stems(w for w in fact_words(text) if not w.isdigit()) - _stems(QUESTION_WORDS | COMMON)


def matching(facts, words):
    """[(score 0-1, fact)] of the facts that share the words, best first, without embeddings or a model call: at
    least half of what the question is about (_distinct: "when do I go to the gym" is about the gym), or enough
    of the fact's own distinctive words (facts.word_match, as a preparation picks facts without embeddings: for a
    longer question). A question of only question words ("what do I do") finds nothing."""
    asked, keys = _distinct(words), _stems(key_words(words))
    if not asked:
        return []
    out = []
    for f in facts:
        shared = len(asked & _distinct(f['text']))
        half = shared / len(asked) if shared and 2 * shared >= len(asked) else 0
        score = max(half, word_match(f['text'], keys, _stems))
        if score:
            out.append((score, f))
    return sorted(out, key=lambda x: -x[0])


def _meaning(store, words, facts, settings):
    """{fact id: cosine} of the facts with a stored vector close in meaning to the words (at least FACT_FLOOR): the
    vectors a preparation or Ask already stored (fact_vectors), against one local embedding of the words, as
    retained_facts.py reads them. A fact without a stored vector is matched by words only, and none is embedded here.
    {} without embeddings, or when the embedding server is down or slow."""
    if not settings or not facts:
        return {}
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    ids = [f['id'] for f in facts]
    with store.connect() as db:
        stored = {r[0]: embeddings.unpack(r[1]) for r in db.execute(
            f'SELECT fact_id,vector FROM fact_vectors WHERE model=? AND fact_id IN ({_marks(ids)})', (key, *ids))}
    if not stored:
        return {}
    try:
        asked = embeddings.embed(settings, [embeddings.QUERY_PREFIX + words], LEARNED_TIMEOUT)[0]
    except Exception as error:  # words only, the rest of the recall as it was
        LOG.info('talk recall meaning error=%s', type(error).__name__)
        return {}
    close = {i: embeddings.cosine(asked, v) for i, v in stored.items()}
    return {i: c for i, c in close.items() if c >= FACT_FLOOR}


def learned(store, words, settings=None):
    """What was learned that a few words are about, for Talk's recall (the `talk` recall's facts block): the owner's own
    facts and rules, never a connected AI's, that share at least half of the words' content words (in their plain
    form, _stem), most shared first, then those close in meaning to the words (their stored vectors, when the Machine
    has embeddings: settings), at most LEARNED. No model call: words alone work on every Machine. Without it, what the
    owner said in a chat ("remember ...") never came back by voice: it is a fact here, not in OpenClaw's memory files.
    Only current facts: a forgotten, ended or replaced one is not in store.facts()."""
    asked = _stems(fact_words(words))
    if not asked:
        return []
    at = now()
    own = [f for f in store.facts() if not ai_fact_by(f) and fact_weight(f, at) > 0]
    close = _meaning(store, words, own, settings)
    scored = []
    for f in own:
        shared = _shared(asked, f['text'])
        if shared or f['id'] in close:
            scored.append((shared, close.get(f['id'], 0.0), str(f.get('last_use') or ''), f))
    picked = [x[3] for x in sorted(scored, key=lambda x: x[:3], reverse=True)[:LEARNED]]
    said = {f['id'] for s, _, _, f in scored if s}
    note_facts(picked, lambda f: 'match' if f['id'] in said else 'closeness', scores={i: c for i, c in close.items() if i not in said})
    return picked


# The owner's main chat (Telegram, the web chat) reads what was learned on demand: the bridge's assistant_memory tool,
# the `chat` recall's learned block. Nothing goes in its prompt until it asks, so a turn that doesn't ask costs nothing.
CHAT_CHARS = 900          # the whole answer at most: about 225 tokens
CHAT_LEARNED = 5          # current facts and rules
ASKING = frozenset(('what', 'which', 'where', 'when', 'who', 'whom', 'why', 'how', 'do', 'does', 'did', 'i', 'me', 'my',
                    'mine', 'you', 'your', 'we', 'our', 'us', 'know', 'remember', 'said', 'say', 'tell', 'told', 'about',
                    'again', 'there', 'anything', 'something'))
CHAT_HEAD = ('What The Machine learned that matches: the owner\'s own facts and draft rules. A line marked '
             f'"{retained_facts.HISTORY}" no longer holds: never give it as how things are now.')


def _asked(question):
    """The question's words without the ones every question has ("what do you know about my ...") and short ones
    ("go", "is"), numbers kept."""
    return ' '.join(w for w in re.findall(r'\w+', str(question or '')) if w.casefold() not in ASKING and (len(w) > 2 or w.isdigit()))


def _people_named(question, who):
    """Of these records (fact_links.records), the people the question names: their whole name, or their first name
    (three letters or more). A fact about someone else stays out unless the question asks about them."""
    asked = set(_fold(question))
    out = set()
    for node, r in who.items():
        if r['kind'] != 'person':
            continue
        name = _fold(r['name'])
        if name and (set(name) <= asked or (len(name[0]) >= 3 and name[0] in asked)):
            out.add(node)
    return out


def _chat_vector(app, question, settings):
    """The chat question's own vector (one local embedding request, LEARNED_TIMEOUT), only when some fact has a stored
    vector of this model to compare it with; None without embeddings, without stored vectors, or when the embedding
    server is down or slow: the words alone then."""
    if not settings:
        return None
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    with app.store.connect() as db:
        if not db.execute('SELECT 1 FROM fact_vectors WHERE model=? LIMIT 1', (key,)).fetchone():
            return None
    try:
        return embeddings.embed(settings, [embeddings.QUERY_PREFIX + question], LEARNED_TIMEOUT)[0]
    except Exception as error:  # words only, the rest of the answer as it was
        LOG.info('chat recall meaning error=%s', type(error).__name__)
        return None


def _near_current(db, vector, settings):
    """{fact id: cosine} of the current facts and draft rules whose stored vector (fact_vectors) is at least
    FACT_FLOOR from the question's: the newest retained_facts.MEANING_WORK of them, one comparison each. None is
    embedded here: a fact without a stored vector is matched by words only."""
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    out = {}
    for fact_id, blob in db.execute("SELECT v.fact_id,v.vector FROM fact_vectors v JOIN facts f ON f.id=v.fact_id WHERE v.model=? "
                                    "AND f.removed_at IS NULL AND f.kind IN ('fact','draft') ORDER BY f.id DESC LIMIT ?", (key, retained_facts.MEANING_WORK)):
        close = embeddings.cosine(vector, embeddings.unpack(blob))
        if close >= FACT_FLOOR:
            out[fact_id] = close
    return out


def for_chat(app, question, limit=CHAT_CHARS):
    """What was learned that the owner's chat question is about, in at most limit characters ('' when nothing
    matches): their own current facts and draft rules by words (as Talk's learned), then by meaning (their stored
    vectors against one embedding of the question, when the Machine has embeddings), then what was learned earlier and
    is no longer in the current list (retained_facts.py: set aside, or ended or replaced and marked historical), by
    words or meaning too. Never a connected AI's fact, nor one the owner removed. A fact about a person comes only
    when the question names them. Noted for the use log (purpose chat)."""
    words = _asked(question)
    asked = _stems(fact_words(words))
    if not asked:
        return ''
    settings = embeddings.settings(app.config)
    vector = _chat_vector(app, question, settings)
    with app.store.connect() as db:
        near = _near_current(db, vector, settings) if vector else {}
        near_old = retained_facts.near(db, vector, settings, FACT_FLOOR) if vector else {}
    # by words as Talk's recall: half of the asked words (a short noun like "gym" counts), most shared first, then by meaning
    at, rank = now(), lambda f: (_shared(asked, f['text']), near.get(f['id'], 0.0), str(f.get('last_use') or ''))
    current = sorted((f for f in app.store.facts() if (f['id'] in near or _shared(asked, f['text'])) and not ai_fact_by(f) and fact_weight(f, at) > 0),
                     key=rank, reverse=True)
    with app.store.connect() as db:
        with_about(db, current)
        starts = {w[:-1] if w.endswith('y') and len(w) > 1 else w for w in asked}  # "party" is the stem of "parties"
        old = [f for f in retained_facts.candidates(db, retained_facts.starting(db, starts) | set(near_old))  # never one the owner removed
               if f['id'] in near_old or _shared(asked, f['text'])]
        with_about(db, old)
        people = {n for f in current + old for n in f['about']}
        who = fact_links.records(db, people)
    named = _people_named(question, who)
    mine = lambda f: not any(who.get(n, {}).get('kind') == 'person' and n not in named for n in f['about'])
    current = [f for f in current if f['kind'] in ('fact', 'draft') and mine(f)][:CHAT_LEARNED]
    old = sorted((f for f in old if mine(f)), key=lambda f: (f['state'] != 'aside', -_shared(asked, f['text']), -near_old.get(f['id'], 0.0)))[:retained_facts.LINES]
    lines, size = [], len(CHAT_HEAD)
    for f in current + old:
        text = retained_facts.line(f) if 'state' in f else ('- Draft rule: ' + f['text']) if f['kind'] == 'draft' else fact_line(f)
        if size + len(text) + 1 > limit:
            break
        lines.append(text)
        size += len(text) + 1
        said = _shared(asked, f['text'])
        memory_use.note('rule' if f['kind'] == 'draft' else 'fact', f['id'], text, 'match' if said else 'closeness', about=f['about'],
                        source='note' if f.get('suggestion_id') else 'review', at=f.get('created_at'),
                        score=None if said else (near_old if 'state' in f else near).get(f['id']))
    return '\n'.join([CHAT_HEAD, *lines]) if lines else ''

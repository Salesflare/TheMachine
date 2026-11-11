"""What was learned and is no longer in the current list, brought back into a prompt when it bears on the matter: the
`retained` block of recall.py's review, preparation and chat purposes.

The current list is what every prompt picks from (Store.facts_for, review_facts.py). Three kinds of fact leave it
without being wrong or forgotten, and before this nothing but Learning's Bring back could find them:

- set aside: not used in 21 days while the list was full (machine/store/facts.py set_aside, 'aside:<id>'). It still
  holds, so it goes in as the fact it is, like one from the current list.
- ended: past its end day, or a newer message overturned it ('expired:<id>'). Shown only as history: "Historical, not
  current", with the day it ended and, when a review ended it, what it says now (rule_changes 'Ended: … Updated: …').
- replaced: a newer fact took its place in a condense ('fact:<id>'). Shown as history with the day and the fact that
  replaced it. One whose words the newer fact all holds says nothing the newer one doesn't, so it never goes in.

A fact the owner removed (forget_fact: removed with nothing it went into), or one whose replacement they removed, is
never read here. Neither is a connected AI's fact, nor a contact detail moved to a person's record, a voice or a skill
(each is kept where it went).

What bears on the matter, without a model call or an embedding request:
- its records: a fact tied to a person, organization or project on the to-do's signals (or the review's waiting
  ones), or whose words name one of them;
- its words: at least two distinctive words shared with the to-do (title, body, the owner's latest note) or the
  waiting signals' subjects, and at least a third of the fact's own (facts.word_match, as a preparation picks its
  current facts without embeddings);
- its meaning, when embeddings are on: the fact's stored vector against the stored vectors of those signals, at
  least FLOOR. A fact without a stored vector is matched by records and words only.

Every fact outside the current list counts, however many years of them there are: what may bear on the matter is found
through indexes (FactsStore.index_facts), and only those are read and checked as above. Records: fact_about by node_id.
Names and words: the facts' keyword index (fact_search, FTS5): a fact with a record's name, or with two of the words
asked, which finds every fact the checks can pass. Meaning: the stored vectors of the facts outside the list, scanned
like a message search (embeddings.related), within MEANING_WORK comparisons (_closeness).

The block is a small fixed slice (CHARS, LINES), outside the current facts' own cap, and empty when nothing matches:
the prompt is then the one it was. Set-aside facts go first, then history. A pick is not a use: facts.used_at is
neither read nor written, so a set-aside fact stays set aside until the owner brings it back.

A to-do's chat answers in its preparation's session, which read the current list when that preparation started.
since_session is the `new` block of the chat's recall: what changed in the list after the session last read it, as a
small delta (NEW_CHARS, NEW_LINES), and nothing when nothing changed:
- a current fact or rule learned, edited or brought back since then, that the session wasn't given in this state
  (memory_use: the session's runs, by id and time), of the to-do's area. While the list is short every preparation
  gets all of it, so all such ones go; else only those that bear on the to-do, by `matches` above. Never one learned
  on this to-do (the session saw that note), never a connected AI's;
- one the session was given that has since gone: removed by the owner ("no longer use"), or ended (as history). One a
  newer fact replaced, set aside or moved elsewhere still says nothing wrong, so it gets no line."""
import itertools
import json
import math

import embeddings
import fact_links
import memory_use
from machine.app.review_facts import waiting
from machine.config import LOG
from machine.store.facts import FACTS_ALL_UNDER, MATCH_WORDS, ai_fact_by, fact_line, key_words as words, suggestion_scope, word_match
from timeutil import now

CHARS = 600           # about 150 tokens, only when something matches
CHAT_CHARS = 400      # a chat turn's message stays short
LINES = 3
MEANING_WORK = 500_000  # vector comparisons per recall at most (_closeness): one to three seconds
FLOOR = 0.45          # cosine of a fact to a signal: facts unrelated to one mostly score 0.1 to 0.35
SIGNALS = 120         # the review's waiting signals looked at, the newest
HEAD = ('Also learned earlier, outside the current list, matching this {what}. A plain line still holds (set aside only for '
        'room). A line marked "Historical, not current" is history: never use it as how things are now.')
REVIEW_HEAD = HEAD.format(what='batch')
TODO_HEAD = HEAD.format(what='to-do')
HISTORY = 'Historical, not current'
NEW_CHARS = 400       # a chat turn's delta: about 100 tokens, only when the list changed since the session read it
NEW_LINES = 3
NEW_HEAD = ('Changed in what was learned since this session read it. Where a line differs from what you were told earlier '
            'in this session, the line here is current.')
GONE = 'The owner removed this; no longer use it'
# A fact outside the current list that may come back: set aside, ended, or replaced in a condense (never one the owner
# removed: forget_fact leaves merged_into empty). Written out in each query, so every query is fixed text; ids go in as
# one JSON list (json_each).
RETAINED = "kind='fact' AND removed_at IS NOT NULL AND (merged_into='aside:'||id OR merged_into='expired:'||id OR merged_into LIKE 'fact:%')"


def _chain(rows, fact_id, depth=10):
    """The current fact a replaced one went into, following later condenses; None when one on the way was removed
    by the owner or is gone, so nothing of it comes back."""
    seen = 0
    while seen < depth:
        row = rows(fact_id)
        if row is None:
            return None
        if row['removed_at'] is None:
            return row
        into = str(row['merged_into'] or '')
        if not into.startswith('fact:'):  # set aside after it took the place: it still holds; removed or ended: nothing
            return row if into == 'aside:' + str(row['id']) else None
        fact_id, seen = into[5:], seen + 1
    return None


def _ids(items):
    return json.dumps(sorted(items))


def candidates(db, ids, today=None):
    """[fact] of these facts that are outside the current list and may still come back, each with state ('aside' or
    'history'), day (when it left) and now_says (what replaced it, '' for none), the most lately removed first."""
    today = today or now()[:10]
    rows = [dict(r) for r in db.execute(
        'SELECT id,text,kind,fact_kind,valid_until,created_at,confirmed_at,removed_at,merged_into,source,side,suggestion_id FROM facts '
        "WHERE id IN (SELECT value FROM json_each(?)) AND kind='fact' AND removed_at IS NOT NULL AND (merged_into='aside:'||id OR merged_into='expired:'||id OR merged_into LIKE 'fact:%')", (_ids(ids),))]
    if not rows:
        return []
    rows.sort(key=lambda r: (r['removed_at'], r['id']), reverse=True)
    current = {str(r[0]).casefold() for r in db.execute("SELECT text FROM facts WHERE removed_at IS NULL AND kind='fact'")}
    expired = [f"expired:{r['id']}" for r in rows if r['merged_into'] == f"expired:{r['id']}"]
    reasons = {r['ref']: r['text'].split(' Updated: ', 1)[1] for r in db.execute(
        "SELECT ref,text FROM rule_changes WHERE kind='condense' AND ref IN (SELECT value FROM json_each(?)) AND text LIKE 'Ended: %' AND text LIKE '% Updated: %'",
        (_ids(expired),))}
    lookup = lambda i: db.execute('SELECT id,text,removed_at,merged_into FROM facts WHERE id=?', (int(i),)).fetchone()
    out = []
    for f in rows:
        if ai_fact_by(f) or f['text'].casefold() in current:  # a connected AI's, or learned again since
            continue
        into = f['merged_into']
        if into == 'aside:' + str(f['id']):
            ended = bool(f['valid_until']) and f['valid_until'] < today
            f.update(state='history' if ended else 'aside', day=(f['valid_until'] if ended else f['removed_at'][:10]), now_says='')
        elif into == 'expired:' + str(f['id']):
            f.update(state='history', day=(f['valid_until'] or f['removed_at'])[:10], now_says=reasons.get(into, ''))
        else:
            head = _chain(lookup, into[5:])
            if head is None or words(f['text']) <= words(head['text']):  # removed by the owner, or the newer one says it all
                continue
            f.update(state='history', day=f['removed_at'][:10], now_says=head['text'])
        out.append(f)
    return out


def line(f):
    """A retained fact for a prompt: a set-aside one as the fact it is; one from history marked so, with its day and
    what replaced it."""
    if f['state'] == 'aside':
        return fact_line(f)
    then = f"ended {f['day']}" + (f'; now: {f["now_says"][:160]}' if f['now_says'] else '')
    return f"- {HISTORY} ({then}): {f['text']}"


def _names(db, nodes):
    """[(record id, its name as words)] of these records, for a fact whose words name one (fact_links.name_key)."""
    nodes = sorted(nodes)
    out = []
    for at in range(0, len(nodes), 500):
        part = nodes[at:at + 500]
        for r in db.execute("SELECT id,kind,name FROM graph_nodes WHERE kind IN ('person','org','project') AND id IN ("
                            + ','.join('?' for _ in part) + ')', part):
            key = fact_links.name_key(r['kind'], r['name'])
            if key:
                out.append((r['id'], tuple(key.split())))
    return out


def _says(parts, name):
    """parts (a fact's words, fact_links.words) has this name's words in a row."""
    return any(tuple(parts[i:i + len(name)]) == name for i in range(len(parts) - len(name) + 1))


def _probes(db, signals, settings):
    if not settings or not signals:
        return []
    return [embeddings.unpack(r[0]) for r in db.execute(
        'SELECT v.vector FROM events e JOIN event_vectors v ON v.event_id=e.id AND v.version=e.version '
        f"WHERE e.id IN ({','.join('?' for _ in signals)}) AND v.model=? AND v.dims=? ORDER BY e.id DESC",  # newest first (_closeness)
        (*signals, settings.get('model', ''), int(settings.get('dims', 256))))]


def _tied(db, nodes):
    """ids of the facts outside the current list about one of these records (fact_about_node)."""
    return {r[0] for r in db.execute(
        'SELECT a.fact_id FROM fact_about a JOIN facts f ON f.id=a.fact_id WHERE a.removed_at IS NULL AND a.node_id IN (SELECT value FROM json_each(?)) '
        "AND f.kind='fact' AND f.removed_at IS NOT NULL AND (f.merged_into='aside:'||f.id OR f.merged_into='expired:'||f.id OR f.merged_into LIKE 'fact:%')", (_ids(nodes),))}


def _searched(db, term, prefix=False):
    """ids of the facts outside the current list whose text has this word or name (fact_search, FTS5); prefix: a word
    that starts with it. The index folds case and accents, so it finds every fact the exact checks (_says, word_match)
    can pass, and some they don't."""
    if not any(c.isalnum() for c in term):
        return set()
    return {r[0] for r in db.execute(
        "SELECT id FROM facts WHERE id IN (SELECT rowid FROM fact_search WHERE fact_search MATCH ?) AND kind='fact' AND removed_at IS NOT NULL AND (merged_into='aside:'||id OR merged_into='expired:'||id OR merged_into LIKE 'fact:%')",
        ('"' + term.replace('"', '""') + '"' + ('*' if prefix else ''),))}


def starting(db, prefixes):
    """ids of the facts outside the current list with a word that starts with one of these (a chat question's word
    stems, ask_memory.for_chat), for candidates."""
    return {i for p in prefixes for i in _searched(db, p, prefix=True)}


def _worded(db, asked):
    """ids of the facts outside the current list with at least MATCH_WORDS of the words asked: the only ones
    word_match can pass."""
    seen = {}
    for word in asked:
        for fact_id in _searched(db, word):
            seen[fact_id] = seen.get(fact_id, 0) + 1
    return {fact_id for fact_id, n in seen.items() if n >= MATCH_WORDS}


def _closeness(db, probes, settings):
    """{fact id: best cosine} of the facts outside the current list whose stored vector is at least FLOOR from one of
    the probes. Each is compared with every probe while that stays within MEANING_WORK. Past it (thousands of facts
    against a review's waiting signals), the most lately removed get half the work, every probe each, and the rest the
    other half, against the first probes (the newest signals): never fewer than the 500 newest got before."""
    if not probes:
        return {}
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    total = db.execute("SELECT count(*) FROM fact_vectors v JOIN facts f ON f.id=v.fact_id WHERE v.model=? AND f.kind='fact' AND f.removed_at IS NOT NULL AND (f.merged_into='aside:'||f.id OR f.merged_into='expired:'||f.id OR f.merged_into LIKE 'fact:%')",
                       (key,)).fetchone()[0]
    full = total if total * len(probes) <= MEANING_WORK else MEANING_WORK // (2 * len(probes))
    few = probes[:max(1, MEANING_WORK // 2 // max(1, total - full))]
    sizes, out = {len(p) for p in probes}, {}
    for n, (fact_id, blob) in enumerate(db.execute(
            "SELECT v.fact_id,v.vector FROM fact_vectors v JOIN facts f ON f.id=v.fact_id WHERE v.model=? AND f.kind='fact' AND f.removed_at IS NOT NULL AND (f.merged_into='aside:'||f.id OR f.merged_into='expired:'||f.id OR f.merged_into LIKE 'fact:%') "
            'ORDER BY f.removed_at DESC,f.id DESC', (key,))):
        vector, against = embeddings.unpack(blob), probes if n < full else few
        if sizes == {len(vector)}:
            close = max(map(math.sumprod, itertools.repeat(vector), against))  # embeddings.cosine without a call per pair
        else:
            close = max(embeddings.cosine(vector, p) for p in against)
        if close >= FLOOR:
            out[fact_id] = close
    return out


def near(db, vector, settings, floor):
    """{fact id: cosine} of the facts outside the current list at least floor from one vector (a chat question's,
    ask_memory.for_chat), within MEANING_WORK comparisons (_closeness)."""
    return {i: c for i, c in _closeness(db, [vector], settings).items() if c >= floor}


def _close_for(db, found, probes, settings):
    """{fact id: best cosine} of these few facts (since_session's current ones), from their stored vectors."""
    if not probes or not found:
        return {}
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    return {r[0]: max(embeddings.cosine(embeddings.unpack(r[1]), p) for p in probes) for r in db.execute(
        'SELECT fact_id,vector FROM fact_vectors WHERE model=? AND fact_id IN (SELECT value FROM json_each(?))', (key, _ids(f['id'] for f in found)))}


def find(db, nodes, text, signals, settings):
    """What may bear on the matter, through the indexes: (candidates, the records' names, the words asked, {fact id:
    closeness}). matches says which really do."""
    nodes = set(nodes or ())
    names = _names(db, nodes) if nodes else []
    asked = words(text)
    close = _closeness(db, _probes(db, signals, settings), settings)
    ids = _tied(db, nodes) | {i for _, name in names for i in _searched(db, ' '.join(name))} | _worded(db, asked) | set(close)
    return candidates(db, ids), names, asked, close


def matches(db, found, nodes, names, asked, close):
    """[(how, score, fact)] of the found ones that bear on the matter, best first: set aside before history, then by
    records, meaning and words. how: about, closeness or match (memory_use.HOWS)."""
    if not found:
        return []
    nodes = set(nodes or ())
    tied = {}
    if nodes:
        for r in db.execute('SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL AND fact_id IN (SELECT value FROM json_each(?))',
                            (_ids(f['id'] for f in found),)):
            tied.setdefault(r['fact_id'], set()).add(r['node_id'])
    out = []
    for f in found:
        parts = [w for w, _ in fact_links.words(f['text'])] if names else []
        if tied.get(f['id'], set()) & nodes or any(_says(parts, name) for _, name in names):
            out.append(('about', 1.0, f))
            continue
        near = close.get(f['id'], 0.0)
        said = word_match(f['text'], asked)
        if near >= FLOOR or said:
            out.append(('closeness', near, f) if near >= FLOOR else ('match', said, f))
    return sorted(out, key=lambda m: (m[2]['state'] != 'aside', -m[1]))


def block(found, limit, head):
    """The block's text for the matched ones that fit limit characters (LINES at most), noted for the use log; ''
    when none matched."""
    lines, size = [], len(head) + 1
    for how, score, f in found:
        text = line(f)
        if len(lines) >= LINES or size + len(text) + 1 > limit:
            break
        lines.append(text)
        size += len(text) + 1
        memory_use.note('fact', f['id'], text, how, about=f.get('about', ()), source='note' if f.get('suggestion_id') else 'review',
                        at=f.get('created_at'), score=score if how == 'closeness' else None, used=False)
    return head + '\n' + '\n'.join(lines) if lines else ''


def for_todo(app, suggestion_id, limit=None):
    """The retained facts that bear on a to-do (a preparation, or a turn of its chat): by its records, its signals'
    meaning and its words (title, body, the owner's latest note). Only facts of the to-do's area (as Store.facts_for)."""
    try:
        with app.store.connect() as db:
            card = db.execute('SELECT title,body,event_ids,account_ids,area FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not card:
                return ''
            note = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND feedback!='' ORDER BY created_at DESC LIMIT 1", (suggestion_id,)).fetchone()
            try:
                signals = [int(i) for i in json.loads(card['event_ids'] or '[]')][:20]
            except (TypeError, ValueError):
                signals = []
            text = ' '.join(filter(None, (card['title'], card['body'], note['feedback'] if note else '')))
            nodes = fact_links.todo_records(db, suggestion_id)
            found, names, asked, close = find(db, nodes, text, signals, embeddings.settings(app.config))
            if not found:
                return ''
            about = {}
            for r in db.execute('SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL AND fact_id IN (SELECT value FROM json_each(?))',
                                (_ids(f['id'] for f in found),)):
                about.setdefault(r['fact_id'], []).append(r['node_id'])
            for f in found:
                f['about'] = tuple(about.get(f['id'], ()))
            accounts = app.config.get('accounts', [])
            area = suggestion_scope(card['account_ids'] or '[]', accounts, card['area'])
            who = fact_links.records(db, {n for f in found for n in f['about']})
            found = [f for f in found if f.get('side') in (None, area) and fact_links.on_side(f['about'], who, area)]
            found = matches(db, found, nodes, names, asked, close)
    except Exception as error:  # a busy database never costs the prompt the rest of its memory
        LOG.error('retained facts error=%s', type(error).__name__)
        return ''
    return block(found, limit or CHARS, TODO_HEAD)


def for_review(app, limit=None):
    """The retained facts that bear on the signals waiting for a review: by their records, meaning and subjects."""
    try:
        with app.store.connect() as db:
            signals = waiting(db, [a['id'] for a in app.config.get('accounts', [])], SIGNALS)
            if not signals:
                return ''
            marks = ','.join('?' for _ in signals)
            nodes = {r[0] for r in db.execute(f'SELECT DISTINCT node_id FROM graph_events WHERE probable=0 AND event_id IN ({marks})', signals)}
            text = ' '.join(r[0] or '' for r in db.execute(f'SELECT title FROM events WHERE id IN ({marks})', signals))
            found, names, asked, close = find(db, nodes, text, signals, embeddings.settings(app.config))
            found = matches(db, found, nodes, names, asked, close)
    except Exception as error:  # a busy database never costs the review its facts
        LOG.error('retained facts error=%s', type(error).__name__)
        return ''
    return block(found, limit or CHARS, REVIEW_HEAD)


def _session(db, session):
    """(when a preparation session last read the current list, {(kind, row id): when one of its runs was last given
    it}): the later of its first start and its latest preparation's logged read (memory_use)."""
    runs = [r[0] for r in db.execute('SELECT job_id FROM preparation_runs WHERE session_job_id=? OR job_id=?', (session, session))]
    if not runs:
        return None, {}
    marks = ','.join('?' for _ in runs)
    start = db.execute(f'SELECT min(started_at) FROM preparation_runs WHERE job_id IN ({marks})', runs).fetchone()[0]
    read = db.execute(f"SELECT max(at) FROM memory_use WHERE purpose='preparation' AND run_id IN ({marks})", runs).fetchone()[0]
    given = {(r[0], r[1]): r[2] for r in db.execute(
        f"SELECT kind,row_id,max(at) FROM memory_use WHERE kind IN ('fact','rule') AND run_id IN ({marks}) GROUP BY kind,row_id", runs)}
    return max(filter(None, (start, read)), default=None), given


def _kind(f):
    return 'rule' if f['kind'] == 'draft' else 'fact'


def since_session(app, suggestion_id, session, limit=None):
    """The `new` block of a to-do's chat turn: what changed in what was learned since its session last read it (see
    the module's docstring). '' when nothing did."""
    try:
        current = [f for f in app.store.facts() if not ai_fact_by(f)]
        with app.store.connect() as db:
            card = db.execute('SELECT title,body,event_ids,account_ids,area FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            since, given = _session(db, session) if card and session else (None, {})
            if not since:
                return ''
            changed = {r[0]: r[1] for r in db.execute(
                "SELECT id,max(created_at,coalesce(kept_at,'')) FROM facts WHERE removed_at IS NULL AND max(created_at,coalesce(kept_at,''))>?", (since,))}
            ids = [int(i) for k, i in given if str(i).isdigit()]
            gone = [dict(r) for r in db.execute(
                f"SELECT id,text,kind,removed_at,merged_into,valid_until FROM facts WHERE removed_at IS NOT NULL AND id IN ({','.join('?' for _ in ids)}) "
                "AND (merged_into IS NULL OR merged_into='expired:'||id) ORDER BY removed_at DESC", ids)] if ids else []
            gone = [f for f in gone if f['removed_at'] > given.get((_kind(f), str(f['id'])), '')]
            if not changed and not gone:
                return ''
            about = {}
            for r in db.execute('SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL'):
                about.setdefault(r['fact_id'], []).append(r['node_id'])
            for f in current:
                f['about'], f['state'] = tuple(about.get(f['id'], ())), 'aside'  # current: matched and shown as a fact
            area = suggestion_scope(card['account_ids'] or '[]', app.config.get('accounts', []), card['area'])
            who = fact_links.records(db, {n for f in current for n in f['about']})
            current = [f for f in current if f.get('side') in (None, area) and fact_links.on_side(f['about'], who, area)]
            short = {kind for kind in ('fact', 'draft') if sum(len(fact_line(f)) + 1 for f in current if f['kind'] == kind) <= FACTS_ALL_UNDER}
            new = [f for f in current if f['id'] in changed and f['suggestion_id'] != suggestion_id
                   and given.get((_kind(f), str(f['id'])), '') < changed[f['id']]]
            picks = []
            if new:
                note = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND feedback!='' ORDER BY created_at DESC LIMIT 1", (suggestion_id,)).fetchone()
                try:
                    signals = [int(i) for i in json.loads(card['event_ids'] or '[]')][:20]
                except (TypeError, ValueError):
                    signals = []
                text = ' '.join(filter(None, (card['title'], card['body'], note['feedback'] if note else '')))
                nodes, settings = fact_links.todo_records(db, suggestion_id), embeddings.settings(app.config)
                picks = matches(db, new, nodes, _names(db, nodes) if nodes else [], words(text), _close_for(db, new, _probes(db, signals, settings), settings))
                matched = {f['id'] for _, _, f in picks}  # while the list is short a preparation gets all of it: so does this
                picks += [('recency', None, f) for f in sorted(new, key=lambda f: changed[f['id']], reverse=True) if f['kind'] in short and f['id'] not in matched]
    except Exception as error:  # a busy database never costs the chat turn its answer
        LOG.error('session facts error=%s', type(error).__name__)
        return ''
    lines, size = [], len(NEW_HEAD) + 1
    shown = [('recency', None, f, (f"- {GONE}: {f['text'][:80]}" if f['merged_into'] is None
                                   else f"- {HISTORY} (ended {(f['valid_until'] or f['removed_at'])[:10]}): {f['text']}")) for f in gone]
    shown += [(how, score, f, ('- Draft rule: ' + f['text'] if f['kind'] == 'draft' else fact_line(f))) for how, score, f in picks]
    for how, score, f, text in shown:
        if len(lines) >= NEW_LINES or size + len(text) + 1 > (limit or NEW_CHARS):
            continue  # a shorter one after it may still fit
        lines.append(text)
        size += len(text) + 1
        memory_use.note(_kind(f), f['id'], text, how, about=f.get('about', ()), source='note' if f.get('suggestion_id') else 'review',
                        at=f.get('created_at', ''), score=score if how == 'closeness' else None, used=False)
    return NEW_HEAD + '\n' + '\n'.join(lines) if lines else ''

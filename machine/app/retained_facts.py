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

The block is a small fixed slice (CHARS, LINES), outside the current facts' own cap, and empty when nothing matches:
the prompt is then the one it was. Set-aside facts go first, then history. A pick is not a use: facts.used_at is
neither read nor written, so a set-aside fact stays set aside until the owner brings it back."""
import json

import embeddings
import fact_links
import memory_use
from machine.app.review_facts import waiting
from machine.config import LOG
from machine.store.facts import ai_fact_by, fact_line, key_words as words, suggestion_scope, word_match
from timeutil import now

CHARS = 600           # about 150 tokens, only when something matches
CHAT_CHARS = 400      # a chat turn's message stays short
LINES = 3
CANDIDATES = 500      # the most lately removed facts looked at
FLOOR = 0.45          # cosine of a fact to a signal: facts unrelated to one mostly score 0.1 to 0.35
SIGNALS = 120         # the review's waiting signals looked at, the newest
HEAD = ('Also learned earlier, outside the current list, matching this {what}. A plain line still holds (set aside only for '
        'room). A line marked "Historical, not current" is history: never use it as how things are now.')
REVIEW_HEAD = HEAD.format(what='batch')
TODO_HEAD = HEAD.format(what='to-do')
HISTORY = 'Historical, not current'


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


def candidates(db, today=None):
    """[fact] of the facts outside the current list that may still come back, each with state ('aside' or 'history'),
    day (when it left) and now_says (what replaced it, '' for none), the most lately removed first."""
    today = today or now()[:10]
    rows = [dict(r) for r in db.execute(
        "SELECT id,text,kind,fact_kind,valid_until,created_at,confirmed_at,removed_at,merged_into,source,side,suggestion_id FROM facts "
        "WHERE kind='fact' AND removed_at IS NOT NULL AND (merged_into='aside:'||id OR merged_into='expired:'||id OR merged_into LIKE 'fact:%') "
        'ORDER BY removed_at DESC,id DESC LIMIT ?', (CANDIDATES,))]
    current = {str(r[0]).casefold() for r in db.execute("SELECT text FROM facts WHERE removed_at IS NULL AND kind='fact'")}
    reasons = {r['ref']: r['text'].split(' Updated: ', 1)[1] for r in db.execute(
        "SELECT ref,text FROM rule_changes WHERE kind='condense' AND ref LIKE 'expired:%' AND text LIKE 'Ended: %' AND text LIKE '% Updated: %'")}
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


def _says(text, name):
    parts = [w for w, _ in fact_links.words(text)]
    return any(tuple(parts[i:i + len(name)]) == name for i in range(len(parts) - len(name) + 1))


def _probes(db, signals, settings):
    if not settings or not signals:
        return []
    return [embeddings.unpack(r[0]) for r in db.execute(
        'SELECT v.vector FROM events e JOIN event_vectors v ON v.event_id=e.id AND v.version=e.version '
        f"WHERE e.id IN ({','.join('?' for _ in signals)}) AND v.model=? AND v.dims=?",
        (*signals, settings.get('model', ''), int(settings.get('dims', 256))))]


def matches(db, found, nodes, text, signals, settings):
    """[(how, score, fact)] of the found ones that bear on the matter, best first: set aside before history, then by
    records, meaning and words. how: about, closeness or match (memory_use.HOWS)."""
    if not found:
        return []
    ids = [f['id'] for f in found]
    tied = {}
    if nodes:
        for r in db.execute(f"SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL AND fact_id IN ({','.join('?' for _ in ids)})", ids):
            tied.setdefault(r['fact_id'], set()).add(r['node_id'])
    names = _names(db, nodes) if nodes else []
    asked = words(text)
    probes = _probes(db, signals, settings)
    stored = {}
    if probes:
        key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
        stored = {r[0]: embeddings.unpack(r[1]) for r in db.execute(
            f"SELECT fact_id,vector FROM fact_vectors WHERE model=? AND fact_id IN ({','.join('?' for _ in ids)})", (key, *ids))}
    out = []
    for f in found:
        if tied.get(f['id'], set()) & set(nodes) or any(_says(f['text'], name) for _, name in names):
            out.append(('about', 1.0, f))
            continue
        close = max((embeddings.cosine(stored[f['id']], p) for p in probes), default=0.0) if f['id'] in stored else 0.0
        said = word_match(f['text'], asked)
        if close >= FLOOR or said:
            out.append(('closeness', close, f) if close >= FLOOR else ('match', said, f))
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
            found = candidates(db)
            if not found:
                return ''
            about = {}
            for r in db.execute('SELECT fact_id,node_id FROM fact_about WHERE removed_at IS NULL'):
                about.setdefault(r['fact_id'], []).append(r['node_id'])
            for f in found:
                f['about'] = tuple(about.get(f['id'], ()))
            accounts = app.config.get('accounts', [])
            area = suggestion_scope(card['account_ids'] or '[]', accounts, card['area'])
            who = fact_links.records(db, {n for f in found for n in f['about']})
            found = [f for f in found if f.get('side') in (None, area) and fact_links.on_side(f['about'], who, area)]
            note = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND feedback!='' ORDER BY created_at DESC LIMIT 1", (suggestion_id,)).fetchone()
            try:
                signals = [int(i) for i in json.loads(card['event_ids'] or '[]')][:20]
            except (TypeError, ValueError):
                signals = []
            text = ' '.join(filter(None, (card['title'], card['body'], note['feedback'] if note else '')))
            found = matches(db, found, fact_links.todo_records(db, suggestion_id), text, signals, embeddings.settings(app.config))
    except Exception as error:  # a busy database never costs the prompt the rest of its memory
        LOG.error('retained facts error=%s', type(error).__name__)
        return ''
    return block(found, limit or CHARS, TODO_HEAD)


def for_review(app, limit=None):
    """The retained facts that bear on the signals waiting for a review: by their records, meaning and subjects."""
    try:
        with app.store.connect() as db:
            found = candidates(db)
            if not found:
                return ''
            signals = waiting(db, [a['id'] for a in app.config.get('accounts', [])], SIGNALS)
            if not signals:
                return ''
            marks = ','.join('?' for _ in signals)
            nodes = {r[0] for r in db.execute(f'SELECT DISTINCT node_id FROM graph_events WHERE probable=0 AND event_id IN ({marks})', signals)}
            text = ' '.join(r[0] or '' for r in db.execute(f'SELECT title FROM events WHERE id IN ({marks})', signals))
            found = matches(db, found, nodes, text, signals, embeddings.settings(app.config))
    except Exception as error:  # a busy database never costs the review its facts
        LOG.error('retained facts error=%s', type(error).__name__)
        return ''
    return block(found, limit or CHARS, REVIEW_HEAD)

"""Which facts a review gets once they no longer all fit its prompt (the `facts` blocks of recall.py's review).

While everything learned fits the review's fact cap, the review gets all of it, as before (Store.facts_text). Past the
cap the list used to be cut in one order, so the same facts missed every review. Now, inside the same cap:

- Standing facts keep their place, first and in a fixed order: the ones the owner wrote or brought back themselves
  (kept_at) and their own preferences (fact_kind preference, about no one). At most STANDING_SHARE of the cap.
- The rest is picked for the batch: closest in meaning to the signals that wait for this review, from the vectors
  already stored for facts and signals (no embedding call, no model call). Without meaning search, or before any
  vector is there, the ones said or used most lately instead, as before.
- A part of the room (TURN_SHARE) goes by turns: the fact a review saw longest ago goes in, whatever else was
  picked, so none is left out forever. "Saw" is the use log (memory_use, purpose review); a fact no review saw yet
  goes first, so a new one is shown at once.

The picked part is a block of its own that the prompt puts after everything that changes slowly: it differs from
one review to the next, and a cached prompt prefix ends at the first byte that differs (machine/prompts/review.py).
It is listed in id order, so two batches that pick the same facts give the same bytes.

A review's pick is not a use of the fact: facts.used_at (which setting aside after 21 unused days reads) is neither
read nor written here."""
import embeddings
import memory_use
from machine.config import LOG
from machine.prompts.review import FACTS_YOU
from machine.store.events import SET_ASIDE_AFTER
from machine.store.facts import AI_FACTS_HEAD, FACTS_FLOOR, ai_fact_by, fact_line, fact_weight, note_facts
from timeutil import now

LIMIT = 3000          # the review's fact cap in characters, as Store.facts_text has it
STANDING_SHARE = 0.5  # of the cap, at most, for the standing facts
TURN_SHARE = 0.2      # of the picked part's room, for the facts whose turn it is
BATCH_SIGNALS = 120   # waiting signals read from each end (newest, and waiting longest), as a review's batch is made
BATCH_HEAD = ('{more} the owner told you earlier (true unless newer evidence says otherwise; ' + FACTS_YOU
              + '). These fit this batch best; there are others, not shown this time:')


def cost(fact):
    return len(fact_line(fact, True)) + 1


def batch_head(standing):
    return BATCH_HEAD.format(more='More facts' if standing else 'Facts')


def cut_size(store, facts, limit):
    """The characters the list took when it was cut at limit in one order (Store.facts_text): what the two blocks
    together stay within, so the prompt never grows."""
    out, size = [], 0
    lately = sorted(facts, key=lambda f: (f['last_use'], f['created_at'], f['id']), reverse=True)
    for f in sorted(lately, key=lambda f: bool(ai_fact_by(f))):
        size += cost(f)
        if size > limit:
            break
        out.append(f)
    return len(store.facts_block(out, True)) + 2


def pick(facts, limit, standing_ids=(), scores=None, seen=None, floor=FACTS_FLOOR):
    """(standing, picked, how) for a list that doesn't fit limit characters. standing: the standing facts, in id
    order. picked: the rest that fits, in id order. how: {fact id: 'closeness', 'recency' or 'rotation'}.
    scores: {fact id: closeness to the batch}, or None when meaning can't rank (then the most lately said or used
    lead). seen: {fact id as text: when a review last had it}."""
    seen = seen or {}
    standing, size = [], 0
    for f in sorted((f for f in facts if f['id'] in standing_ids and not ai_fact_by(f)), key=lambda f: -f['id']):
        if size + cost(f) <= limit * STANDING_SHARE:  # the newest of them when even they are too many
            standing.append(f); size += cost(f)
    standing.sort(key=lambda f: f['id'])
    rest = [f for f in facts if f not in standing]
    room = limit - size - len(batch_head(standing)) - 1 - (len(AI_FACTS_HEAD) + 9 if any(ai_fact_by(f) for f in rest) else 0)
    turns = sorted(rest, key=lambda f: (seen.get(str(f['id']), ''), -f['id']))  # never seen first, the newest of those first
    reserve = max(int(room * TURN_SHARE), cost(turns[0])) if turns else 0  # its turn always fits
    if scores is None:
        ranked = sorted(rest, key=lambda f: (f['last_use'], f['created_at'], f['id']), reverse=True)
    else:
        ranked = sorted((f for f in rest if scores.get(f['id'], 0) >= floor), key=lambda f: -scores[f['id']])
    picked, how, used = [], {}, 0
    for label, queue, most in (('recency' if scores is None else 'closeness', ranked, room - reserve), ('rotation', turns, room)):
        for f in queue:
            if f['id'] not in how and used + cost(f) <= most:
                picked.append(f); how[f['id']] = label; used += cost(f)
    return standing, sorted(picked, key=lambda f: f['id']), how


def waiting_vectors(db, accounts, settings, each=BATCH_SIGNALS):
    """The stored vectors of the signals that wait for a review: the newest and the ones waiting longest, the two ends
    a batch is made from (Store.begin_analysis). The batch itself is claimed after the prompt is built."""
    if not accounts:
        return []
    marks = ','.join('?' for _ in accounts)
    sql = ('SELECT e.id,v.vector FROM events e JOIN event_vectors v ON v.event_id=e.id AND v.version=e.version '
           f'WHERE e.account_id IN ({marks}) AND e.deleted=0 AND e.analyzed_version<e.version AND e.deferrals<? AND v.model=? AND v.dims=? ')
    args = (*accounts, SET_ASIDE_AFTER, settings.get('model', ''), int(settings.get('dims', 256)), each)
    found = {}
    for order in ('ORDER BY e.id DESC LIMIT ?', 'ORDER BY e.deferrals,e.ingested_at,e.id LIMIT ?'):
        for r in db.execute(sql + order, args):
            found[r[0]] = embeddings.unpack(r[1])
    return list(found.values())


def closeness(db, facts, accounts, settings, at=None):
    """{fact id: how close it is to the waiting signals}: its best cosine against any of them, weighed by how much the
    fact still counts (as a preparation weighs it, Store.facts_for). None when there is nothing to rank by: no
    waiting signal has a vector, or no fact has one. Stored vectors only."""
    probes = waiting_vectors(db, accounts, settings)
    key = f"{settings.get('model', '')}:{int(settings.get('dims', 256))}"
    stored = {r[0]: embeddings.unpack(r[1]) for r in db.execute('SELECT fact_id,vector FROM fact_vectors WHERE model=?', (key,))}
    if not probes or not any(f['id'] in stored for f in facts):
        return None
    at = at or now()
    return {f['id']: max(embeddings.cosine(stored[f['id']], p) for p in probes) * (0.5 + 0.5 * fact_weight(f, at))
            for f in facts if f['id'] in stored}


def last_seen(db):
    """{fact id as text: when a review last had it in its prompt}, from the use log."""
    return {r[0]: r[1] for r in db.execute("SELECT row_id,max(at) FROM memory_use WHERE kind='fact' AND purpose='review' GROUP BY row_id")}


class ReviewFacts:
    """One review's facts: standing() is the block where the facts always were, for_batch() the picked one."""

    def __init__(self, app, limit=LIMIT):
        self.app, self.limit, self.parts = app, limit, None

    def chosen(self):
        if self.parts is None:
            store = self.app.store
            facts = [f for f in store.facts() if f['kind'] == 'fact']
            if sum(cost(f) for f in facts) <= self.limit:
                self.parts = (None, [], {}, {})  # they all fit: the whole list, as before
                return self.parts
            limit = cut_size(store, facts, self.limit)
            scores, seen, standing_ids = None, {}, set()
            settings = embeddings.settings(self.app.config)
            try:
                with store.connect() as db:
                    about = {r[0] for r in db.execute('SELECT fact_id FROM fact_about WHERE removed_at IS NULL')}
                    kept = {r[0] for r in db.execute("SELECT id FROM facts WHERE removed_at IS NULL AND kind='fact' AND kept_at IS NOT NULL")}
                    standing_ids = kept | {f['id'] for f in facts if f.get('fact_kind') == 'preference' and f['id'] not in about}
                    seen = last_seen(db)
                    if settings:
                        scores = closeness(db, facts, [a['id'] for a in self.app.config.get('accounts', [])], settings)
            except Exception as error:  # a busy database or a missing table never costs the review its facts
                LOG.error('review facts error=%s', type(error).__name__)
            standing, picked, how = pick(facts, limit, standing_ids, scores, seen)
            self.parts = (standing, picked, how, scores or {})
        return self.parts

    def standing(self):
        standing = self.chosen()[0]
        if standing is None:
            return self.app.store.facts_text(self.limit, ids=True)
        note_facts(standing, 'always', True)
        return self.app.store.facts_block(standing, True)

    def for_batch(self):
        standing, picked, how, scores = self.chosen()
        if not picked:
            return ''
        note_facts(picked, lambda f: how[f['id']], True, scores={i: s for i, s in scores.items() if how.get(i) == 'closeness'})
        return batch_head(standing) + '\n' + self.app.store.facts_block(picked, True)


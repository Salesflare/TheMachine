"""Related signals by meaning (optional): local embedding vectors next to the FTS5 keyword index.

Off unless config has an `embeddings` block ({"url", "model", "dims"}) without `enabled: false`.
Text goes only to that server: meant to be a local one on 127.0.0.1, such as llama.cpp's
`llama-server --embedding` with an EmbeddingGemma GGUF, or any OpenAI-compatible /v1/embeddings
endpoint. `model` is the name the server reports (llama-server's --alias) and is recorded per
vector, so switching models re-embeds. Vectors are Matryoshka-truncated to `dims`, renormalized
and stored as float32 little-endian per event version; deleting an event deletes its vector.
A long meeting or conversation gets more vectors, one per passage after the part the first one covers
(`event_passages`, with where each starts in the body), so a hit can hand back the part that matched.
Search is brute-force cosine over the caller's explicit accounts only, fused with FTS5
(reciprocal rank) when there is a query.

Every input is cut to fit the server (`max_input_tokens`, counted conservatively: at most one token
per UTF-8 byte, `bytes_per_token`) and requests are split to stay under `max_batch_tokens`. An input
the server still refuses is set aside per event version (`event_vector_skips`, with the error class)
so it never blocks the others."""
from __future__ import annotations

import http.client
import json
import math
import re
import struct
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

import message_seal

SCHEMA = '''CREATE TABLE IF NOT EXISTS event_vectors(event_id INTEGER PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,model TEXT NOT NULL,dims INTEGER NOT NULL,vector BLOB NOT NULL)'''
# An event version the server refused on its own (error class only); a new version or model tries again.
SKIP_SCHEMA = '''CREATE TABLE IF NOT EXISTS event_vector_skips(event_id INTEGER PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,model TEXT NOT NULL,reason TEXT NOT NULL,at REAL NOT NULL)'''
# The rest of a long signal, a passage per row: `start` and `chars` are in the body as it is read (whitespace runs
# as one space, review_view's body_offset). No text here: a passage is read from the event's own (sealed) body.
PASSAGE_SCHEMA = '''CREATE TABLE IF NOT EXISTS event_passages(event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
  seq INTEGER NOT NULL,version INTEGER NOT NULL,model TEXT NOT NULL,dims INTEGER NOT NULL,start INTEGER NOT NULL,chars INTEGER NOT NULL,
  vector BLOB NOT NULL,PRIMARY KEY(event_id,seq))'''
SCHEMAS = (SCHEMA, SKIP_SCHEMA, PASSAGE_SCHEMA)
# Kinds whose late parts are worth finding by meaning: meetings and support conversations. Mail is left out: quoted
# history is cut before embedding, and what is long in its own words is mostly newsletters (keywords still find those).
PASSAGE_KINDS = frozenset({'meeting.notes', 'meeting.transcript', 'zoom.summary', 'zoom.transcript', 'google_meet.notes',
                           'google_meet.transcript', 'teams.notes', 'teams.transcript', 'salesflare.meeting', 'intercom.conversation'})
# A passage: whole lines up to PASSAGE_BYTES, ended early at a new paragraph or speaker's turn once it has
# PASSAGE_SOFT. About 250 to 400 tokens: what a retrieval model matches a short question against best, far inside
# EmbeddingGemma's 2,048-token input with its title, and a quarter of the CPU time of a full input each.
PASSAGE_SOFT, PASSAGE_BYTES, PASSAGE_TITLE = 1000, 1600, 100
PASSAGES_MOST = 200  # per signal (about 250 KB of text); beyond that keywords still find it
# One background pass (passage_pass) embeds at most PASSAGE_BATCH passages and looks at PASSAGE_LOOK signals.
PASSAGE_BATCH, PASSAGE_LOOK = 4, 200
TURN = re.compile(r'(?:\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s+)?[^\s:][^:]{0,40}:(?:\s|$)|#{1,6}\s')  # "Ann Example: ...", "[00:12] Ann: ...", a heading
SKIP_SECONDS = 86400  # a set-aside input is tried once more a day later (a server bug may be fixed by then)
BODY_CHARS = 2000
# Cosine at 256 dims. Signal-to-signal matches that were really related scored 0.6-0.87, a query's
# 0.4-0.5; below these they were mostly unrelated (EmbeddingGemma 300M on a real mailbox, October 2026).
FLOOR, QUERY_FLOOR = 0.6, 0.4
MAX_LIMIT = 20
RRF_K = 60
QUOTED = re.compile(r'\n*\[Quoted earlier messages:.*', re.S)  # the stored marker and the history after it
QUERY_PREFIX = 'task: search result | query: '
# Per input and per request, in tokens. llama-server refuses an input longer than its physical batch
# (-ub, 2048 in deploy/embeddinggemma.service, also EmbeddingGemma's context) with HTTP 500, and
# OpenAI's /v1/embeddings takes 8,191 tokens per input and 300,000 per request.
LIMITS = {'local': (2048, 8192, 64), 'openai': (8191, 300000, 2048)}  # input, request, inputs per request
SPECIAL_TOKENS = 16  # room for BOS/EOS and the like the server adds


def settings(config):
    """The `embeddings` block when the feature is on, else None (absent, empty or `enabled: false`)."""
    block = (config or {}).get('embeddings')
    if not isinstance(block, dict) or block.get('enabled') is False or not block.get('url'):
        return None
    return block


class EmbeddingError(Exception):
    """A redacted failure class (never the text or the server's reply)."""


def document(title, body):
    """EmbeddingGemma's document prompt: title plus the new text of the message."""
    body = invisible(QUOTED.sub('', body or ''))
    body = '\n'.join(line for line in body.splitlines() if not line.lstrip().startswith('>'))
    body = re.sub(r'\s+', ' ', body).strip()[:BODY_CHARS]
    title = re.sub(r'\s+', ' ', invisible(title or '')).strip()[:300] or 'none'
    return f'title: {title} | text: {body}'


def ensure(db):
    """The tables, and what earlier versions lack: event_vectors.passages (NULL: not split yet; else how many
    passages this version has, 0 for a short one). Existing vectors stay as they are."""
    for schema in SCHEMAS:
        db.execute(schema)
    if 'passages' not in {r[1] for r in db.execute('PRAGMA table_info(event_vectors)')}:
        db.execute('ALTER TABLE event_vectors ADD COLUMN passages INTEGER')
    db.execute('CREATE INDEX IF NOT EXISTS event_vectors_unsplit ON event_vectors(event_id) WHERE passages IS NULL')


def lines(body):
    """The message's own lines (no quoted history): (offset in the body as read, text, starts a paragraph or a turn)."""
    quoted = QUOTED.search(body)
    at, out, fresh = 0, [], True
    for line in (body[:quoted.start()] if quoted else body).split('\n'):
        text = ' '.join(line.split())
        if not text:
            fresh = True
            continue
        if text.startswith('>'):
            fresh = True
        else:
            turn, piece = fresh or bool(TURN.match(text)), 0
            most = PASSAGE_SOFT if text.isascii() else PASSAGE_SOFT // 4  # in bytes at worst
            while piece < len(text):  # a line longer than a passage: runs of whole words
                end = len(text) if len(text) - piece <= most else text.rfind(' ', piece + 1, piece + most + 1)
                end = end if end > piece else min(piece + most, len(text))
                out.append((at + piece, text[piece:end], turn and not piece))
                piece = end + (text[end:end + 1] == ' ')
            fresh = False
        at += len(text) + 1
    return out


def passages(title, body, settings=None):
    """[(start, chars, document)] for what the first vector (document) leaves out of a long body, in order; [] when
    that one covers it all. Deterministic for a body, so a pass can stop anywhere and go on later."""
    per_input, _, _, per_token = limits(settings or {})
    covered = len(fit(document(title, body), per_input, per_token)) - len(document(title, ''))
    rest, own = [], 0
    for line in lines(body or ''):
        own += len(line[1]) + 1
        if own - 1 > covered:
            rest.append(line)
    groups, size = [], 0
    for line in rest:
        cost = len(line[1].encode()) + 1
        if not groups or size + cost > PASSAGE_BYTES or (line[2] and size >= PASSAGE_SOFT):
            groups.append([])
            size = 0
        groups[-1].append(line); size += cost
    if len(groups) > 1 and sum(len(t.encode()) + 1 for _, t, _ in groups[-1]) < PASSAGE_SOFT // 4:
        groups[-2:] = [groups[-2] + groups[-1]]  # a few closing words go with what came before
    name = re.sub(r'\s+', ' ', invisible(title or '')).strip()[:PASSAGE_TITLE] or 'none'
    return [(group[0][0], group[-1][0] + len(group[-1][1]) - group[0][0], f'title: {name} | text: ' + invisible(' '.join(t for _, t, _ in group)))
            for group in groups[:PASSAGES_MOST]]


def passage_text(body, start, chars=None):
    """The body as read from `start` (a hit's passage), `chars` long or to its end."""
    return ' '.join((body or '').split())[start:None if chars is None else start + chars]


def invisible(text):
    """Without format characters (zero-width spaces, bidi marks, tag characters): they mean nothing to
    the model but cost tokens, a few per character, and mail can hide thousands of them."""
    return ''.join(c for c in text if unicodedata.category(c) != 'Cf') if not text.isascii() else text


def limits(settings):
    """(tokens per input, tokens per request, inputs per request, UTF-8 bytes per token): config
    overrides, else the provider's. One byte per token is the safe bound for byte-level tokenizers
    (SentencePiece with byte fallback, tiktoken); a provider known to do better can raise it."""
    host = urllib.parse.urlsplit(settings.get('url', '')).hostname or ''
    per_input, per_request, inputs = LIMITS['openai' if host == 'api.openai.com' else 'local']
    per_input = max(int(settings.get('max_input_tokens') or per_input), SPECIAL_TOKENS + 32)
    per_request = max(int(settings.get('max_batch_tokens') or per_request), per_input)
    inputs = max(int(settings.get('max_batch_inputs') or inputs), 1)
    return per_input, per_request, inputs, max(float(settings.get('bytes_per_token') or 1.0), 1.0)


def fit(text, per_input, bytes_per_token=1.0):
    """The text cut (at a character boundary) so its worst-case token count fits one input."""
    budget = int((per_input - SPECIAL_TOKENS) * bytes_per_token)
    data = text.encode()
    return text if len(data) <= budget else data[:budget].decode('utf-8', 'ignore')


def tokens(text, bytes_per_token=1.0):
    """Worst-case tokens for one input."""
    return math.ceil(len(text.encode()) / bytes_per_token) + SPECIAL_TOKENS


def batches(texts, settings):
    """The (fitted) texts in consecutive groups, each within the request limits."""
    per_input, per_request, inputs, per_token = limits(settings)
    group, used = [], 0
    for text in (fit(t, per_input, per_token) for t in texts):
        cost = tokens(text, per_token)
        if group and (used + cost > per_request or len(group) >= inputs):
            yield group
            group, used = [], 0
        group.append(text); used += cost
    if group:
        yield group


def endpoint(settings):
    """The configured server's /v1/embeddings: an http(s) address with a host and no user or password in it,
    so a config value can never make urllib read a local file or another scheme."""
    url = str(settings.get('url') or '').rstrip('/')
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        raise EmbeddingError('bad_url') from None
    if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username is not None or parts.password is not None:
        raise EmbeddingError('bad_url')
    return url if url.endswith('/embeddings') else url + '/v1/embeddings'


SERVED = {}  # url -> (checked at, model ids the server reports)


def request(settings, texts, timeout=120):
    """POST to the embedding server; returns the raw vectors in input order. The server must report
    the configured model in /v1/models (llama-server echoes any requested name), so a swap never
    mixes vectors."""
    body = json.dumps({'model': settings.get('model', ''), 'input': texts}).encode()
    request = urllib.request.Request(endpoint(settings), body, {'Content-Type': 'application/json'})
    try:
        checked, served = SERVED.get(settings['url'], (-1e9, ()))
        if time.monotonic() - checked > 600:
            with urllib.request.urlopen(endpoint(settings).rsplit('/', 1)[0] + '/models', timeout=min(10, timeout)) as response:
                served = {m.get('id') for m in json.load(response).get('data', [])}
            SERVED[settings['url']] = (time.monotonic(), served)
        if settings.get('model') not in served:
            raise EmbeddingError('model_mismatch')
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.load(response)['data']
    except urllib.error.HTTPError as error:
        raise EmbeddingError(f'http_{error.code}') from None
    except (urllib.error.URLError, OSError, http.client.HTTPException) as error:
        raise EmbeddingError('timeout' if 'timed out' in str(error) else 'unreachable') from None
    except (ValueError, KeyError, TypeError):
        raise EmbeddingError('bad_response') from None
    if len(data) != len(texts):
        raise EmbeddingError('bad_response')
    return [item['embedding'] for item in sorted(data, key=lambda d: d.get('index', 0))]


def embed(settings, texts, timeout=120):
    """Normalized vectors at the configured Matryoshka size; long texts are cut to fit the server and
    big lists go in several requests."""
    dims = int(settings.get('dims', 256))
    raw = []
    for group in batches(texts, settings):
        raw += request(settings, group, timeout)
    result = []
    for vector in raw:
        if len(vector) < dims:
            raise EmbeddingError('bad_response')
        vector = vector[:dims]
        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        result.append([x / norm for x in vector])
    return result


def pack(vector):
    return struct.pack('<%df' % len(vector), *vector)


def unpack(blob):
    return struct.unpack('<%df' % (len(blob) // 4), blob)


def pending(db, settings, limit, newest=True, history=False):
    """Live signals without a vector for their current version, model and size. history: history rows instead
    (machine/store/history.py), newest first, which the service embeds only once no signal waits, at a slower pace
    (machine/app/history.py history_embed_step)."""
    order = ('e.occurred_at DESC' if newest else 'e.occurred_at ASC') if history else 'e.id ' + ('DESC' if newest else 'ASC')
    return [dict(r) for r in db.execute(
        'SELECT e.id,e.version,e.title,e.body FROM events e LEFT JOIN event_vectors v ON v.event_id=e.id '
        'LEFT JOIN event_vector_skips s ON s.event_id=e.id AND s.version=e.version AND s.model=? AND s.at>? '
        f'WHERE e.deleted=0 AND e.history={int(bool(history))} AND (v.event_id IS NULL OR v.version<>e.version OR v.model<>? OR v.dims<>?) AND s.event_id IS NULL '
        'ORDER BY ' + order + ' LIMIT ?',
        (settings.get('model', ''), time.time() - SKIP_SECONDS, settings.get('model', ''), int(settings.get('dims', 256)), limit))]


def save(db, settings, rows, vectors):
    # A slow older request must not overwrite a newer version's vector. Passages of what the signal said before go
    # with it; the new version's follow in the background (passage_pass).
    db.executemany('DELETE FROM event_passages WHERE event_id=? AND EXISTS(SELECT 1 FROM events WHERE id=? AND version=? AND deleted=0)',
                   [(r['id'], r['id'], r['version']) for r in rows])
    db.executemany('INSERT OR REPLACE INTO event_vectors(event_id,version,model,dims,vector) '
                   'SELECT ?,?,?,?,? WHERE EXISTS(SELECT 1 FROM events WHERE id=? AND version=? AND deleted=0)',
                   [(r['id'], r['version'], settings.get('model', ''), len(v), pack(v), r['id'], r['version']) for r, v in zip(rows, vectors)])


def refused(error):
    """An HTTP error that may be about one input (llama-server answers 500 to one too long), not
    about the server or the account (auth, missing route, rate limit)."""
    code = str(error)[5:] if str(error).startswith('http_') else ''
    return code.isdigit() and code not in {'401', '403', '404', '405', '408', '429'}


def embed_isolating(settings, rows, texts, timeout=120):
    """([(row, vector)], [(row, error class)]): a refused request is split in halves until each
    refused input stands alone, so one bad input never holds back the rest."""
    try:
        return list(zip(rows, embed(settings, texts, timeout))), []
    except EmbeddingError as error:
        if not refused(error):
            raise
        if len(rows) == 1:
            return [], [(rows[0], str(error))]
    half = len(rows) // 2
    done, failed = embed_isolating(settings, rows[:half], texts[:half], timeout)
    more, failed_more = embed_isolating(settings, rows[half:], texts[half:], timeout)
    return done + more, failed + failed_more


def skip(db, settings, failed):
    db.executemany('INSERT OR REPLACE INTO event_vector_skips(event_id,version,model,reason,at) '
                   'SELECT ?,?,?,?,? WHERE EXISTS(SELECT 1 FROM events WHERE id=? AND version=? AND deleted=0)',
                   [(r['id'], r['version'], settings.get('model', ''), reason, time.time(), r['id'], r['version']) for r, reason in failed])


def embed_pending(connect, settings, limit=16, newest=True, history=False):
    """One small pass: read, embed outside any transaction, write. Returns the number of events done
    (embedded, or set aside because the server refused that one input while it took the others)."""
    with connect() as db:
        rows = pending(db, settings, limit, newest, history)
    if not rows:
        return 0
    done, failed = embed_isolating(settings, rows, [document(r['title'], r['body']) for r in rows])
    blame(settings, done, failed)
    with connect() as db:
        save(db, settings, [r for r, _ in done], [v for _, v in done])
        skip(db, settings, failed)
    return len(rows)


def blame(settings, done, failed):
    """Nothing went through: an input, or the server? A tiny probe tells; the server's failure is raised."""
    if failed and not done:
        try:
            embed(settings, [document('none', 'ok')])
        except EmbeddingError:
            raise EmbeddingError(failed[0][1]) from None


def passage_pass(connect, settings, budget=PASSAGE_BATCH, look=PASSAGE_LOOK):
    """One small pass over signals whose current vector has no passages yet, live ones before history, newest
    first: short ones and other kinds are marked done, a long one gets its next passages, at most `budget` of them
    in all (one request, outside any transaction). A long transcript takes several passes and is found by what it
    has so far. (passages embedded, whether more wait)."""
    model, dims = settings.get('model', ''), int(settings.get('dims', 256))
    marked, work, left = [], [], budget  # (passages, event_id, version); (event, version, seq, start, chars, text)
    with connect() as db:
        rows = db.execute('SELECT v.event_id id,v.version,v.model,v.dims,e.version now,e.deleted,e.kind,length(e.body) size FROM event_vectors v '
                          'CROSS JOIN events e ON e.id=v.event_id WHERE v.passages IS NULL ORDER BY e.history,e.id DESC LIMIT ?', (look,)).fetchall()
        for r in rows:
            if (r['version'], r['model'], r['dims'], r['deleted']) != (r['now'], model, dims, 0) or r['kind'] not in PASSAGE_KINDS or r['size'] <= BODY_CHARS:
                marked.append((0, r['id'], r['version']))  # not current (its new vector starts over), or nothing to split
                continue
            if left <= 0:
                break
            event = db.execute('SELECT title,body FROM events WHERE id=?', (r['id'],)).fetchone()
            parts = passages(event['title'], event['body'], settings)
            have = db.execute('SELECT count(*) FROM event_passages WHERE event_id=? AND version=? AND model=? AND dims=?', (r['id'], r['version'], model, dims)).fetchone()[0]
            take = parts[have:have + left]
            left -= len(take)
            work += [(r['id'], r['version'], have + n, *part) for n, part in enumerate(take)]
            if have + len(take) >= len(parts):
                marked.append((len(parts), r['id'], r['version']))
    done, failed = embed_isolating(settings, work, [w[5] for w in work]) if work else ([], [])
    blame(settings, done, failed)
    with connect() as db:
        db.executemany('INSERT OR REPLACE INTO event_passages(event_id,seq,version,model,dims,start,chars,vector) SELECT ?,?,?,?,?,?,?,? '
                       'WHERE EXISTS(SELECT 1 FROM events e JOIN event_vectors v ON v.event_id=e.id WHERE e.id=? AND e.version=? AND e.deleted=0 AND v.version=e.version)',
                       [(w[0], w[2], w[1], model, len(v), w[3], w[4], pack(v), w[0], w[1]) for w, v in done])
        # A passage the server refused on its own ends that signal's split where it is: the others go on.
        marked = [(w[2], w[0], w[1]) for w, _ in failed] + marked
        db.executemany('UPDATE event_vectors SET passages=? WHERE event_id=? AND version=? AND passages IS NULL', marked)
        return len(done), bool(db.execute('SELECT 1 FROM event_vectors WHERE passages IS NULL LIMIT 1').fetchone())


def backfill(connect, settings, batch=16, out=print):
    """Embed every pending event, oldest first (the service works newest first), with progress."""
    with connect() as db:
        total = len(pending(db, settings, 10 ** 9))
    done, started = 0, time.monotonic()
    out(f'{total} events to embed with {settings.get("model")} at {settings.get("dims", 256)} dims')
    failures = 0
    while True:
        try:
            count = embed_pending(connect, settings, batch, newest=False)
        except EmbeddingError as error:  # e.g. the server restarting: wait, then go on
            failures += 1
            if failures > 5:
                raise
            out(f'local model unavailable ({error}); retrying in {30 * failures} s')
            time.sleep(30 * failures)
            continue
        failures = 0
        if not count:
            break
        done += count
        rate = done / max(time.monotonic() - started, 0.001)
        out(f'{done}/{total} embedded, {rate:.1f}/s, about {max(total - done, 0) / rate / 60:.0f} min left')
    return done


class Hit(tuple):
    """(event_id, similarity), as `related` always answered, with where the match is: `start` is the offset of the
    passage that matched best in the body as read (review_view's body_offset) and `chars` its length; None and 0
    when it was the signal's start (or its words only)."""
    def __new__(cls, event_id, similarity, start=None, chars=0):
        self = super().__new__(cls, (event_id, similarity))
        self.start, self.chars = start, chars
        return self


def starts(found):
    """{event_id: offset} of the hits whose best match is a later passage of their body."""
    return {hit[0]: hit.start for hit in found if getattr(hit, 'start', None)}


def cosine(a, b):
    """Dot product of two normalized vectors. math.sumprod runs in C: a search scores every stored vector against the
    query (20k and more), some 4x quicker than a Python sum. Unequal lengths compare their shared part, as zip did."""
    if len(a) != len(b):
        n = min(len(a), len(b))
        a, b = a[:n], b[:n]
    return math.sumprod(a, b)


# Words that only shape a question ("what's the", "wat is de", "c'est quoi le"), in the dashboard's languages: the word
# match leaves them out while other words remain, so a question matches on what it asks about, not on every message
# with "what" and "the" in it.
QUESTION_WORDS = frozenset((
    'a an the is are was were be do does did can could will would should of for to in on at by with from about and or '
    'what whats which who whom whose where when why how it its this that these those my our your me we you there any some '
    'de het een is zijn was waren wat wie welk welke waar wanneer waarom hoe van voor op aan met bij in en of om dat die '
    'dit deze mijn ons onze je jouw we er ook nog nu '
    'der die das ein eine ist sind war was wer wo wann warum wie welche mein unser und oder für mit von zu im '
    'le la les un une des du est sont quel quelle quels quelles qui où quand pourquoi comment mon ma mes notre et ou pour '
    'el los las una es son qué que cuál cuáles quién dónde cuándo por cómo mi nuestro para con del '
    'il lo gli le uno di che chi dove quando perché come qual quale è sono mio nostro per '
    'o os as um uma é são quem onde porque como meu nosso com da do'
).split())


def search_words(query):
    """The words a keyword search matches on: without the question's own words while any other word is left."""
    words = [w for w in re.findall(r'\w+', query) if len(w) > 1]
    asked = [w for w in words if w.casefold() not in QUESTION_WORDS]
    return asked or words


def best_word_hits(db, accounts, query, n, pool=30):
    """The n keyword matches with the most of the words asked, then by bm25: a long mail with the place and the code
    asked comes before a short line that only names the place."""
    words, ids = {w.casefold() for w in search_words(query)}, fts_ids(db, accounts, query, pool)
    if len(words) < 2 or len(ids) <= 1:
        return ids[:n]
    has = {r[0]: words & set(re.findall(r'\w+', f'{r[1]} {r[2]}'.casefold()))
           for r in db.execute('SELECT id,title,body FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)}
    return sorted(ids, key=lambda i: -len(has.get(i, ())))[:n]


def words_lead(order, word_hits, room):
    """order (best first) with each of word_hits (the best keyword matches, best first) in its first `room` places: a
    message with the rare words asked (a name, a place) is never buried under ones that only mean something alike."""
    lead = [i for i in word_hits if i not in order[:room]][:room]
    if not lead:
        return list(order)
    cut = room - len(lead)
    return order[:cut] + lead + [i for i in order[cut:] if i not in lead]


def fts_ids(db, accounts, query, limit, signals_only=False):
    """Keyword ranking (bm25) within the accounts; any word may match, rarer words weigh more. A question's own words
    (search_words) are left out."""
    words = search_words(query)
    if not words:
        return []
    marks = ','.join('?' for _ in accounts)
    return [r[0] for r in db.execute(
        'SELECT e.id FROM event_search JOIN events e ON e.id=event_search.rowid WHERE event_search MATCH ? '
        'AND e.account_id IN (' + marks + ') AND e.deleted=0' + (' AND e.history=0' if signals_only else '') + ' ORDER BY event_search.rank LIMIT ?',
        (message_seal.match(db, words, ' OR '), *accounts, limit))]


def related(connect, settings, accounts, event_ids=(), query='', limit=8, floor=None, exclude=(), timeout=30, query_floor=None,
            signals_only=False):
    """[Hit: (event_id, similarity or None)] best first, only from `accounts`, never the given/excluded ids. A long
    signal scores by its best part (its start or a later passage, Hit.start) and shows once. signals_only:
    never history (what a preparation reads: no model reads history).
    Probes are the given events' own vectors (each candidate scores its best match, against `floor`)
    and the query (against the lower `query_floor`). With a query the meaning and keyword rankings
    are fused (reciprocal rank)."""
    if not accounts:
        raise ValueError('Explicit account_ids are required')
    limit = min(max(int(limit), 1), 40)
    floor = float(settings.get('floor', FLOOR) if floor is None else floor)
    query_floor = float(settings.get('query_floor', QUERY_FLOOR) if query_floor is None else query_floor)
    model, dims = settings.get('model', ''), int(settings.get('dims', 256))
    marks = ','.join('?' for _ in accounts)
    seeds = [int(i) for i in event_ids or ()]
    skip = set(seeds) | {int(i) for i in exclude or ()}
    with connect() as db:
        rows = [dict(r) for r in db.execute(
            'SELECT e.id,e.version,e.title,e.body,v.version vector_version,v.vector,v.model,v.dims FROM events e LEFT JOIN event_vectors v ON v.event_id=e.id '
            'WHERE e.deleted=0 AND e.account_id IN (' + marks + ') AND e.id IN (' + ','.join('?' for _ in seeds) + ')', (*accounts, *seeds))] if seeds else []
    current = lambda r: r['vector'] and r['vector_version'] == r['version'] and r['model'] == model and r['dims'] == dims
    probes = [(r['id'], r['version'], unpack(r['vector'])) for r in rows if current(r)]
    missing = [r for r in rows if not current(r)]
    texts = [document(r['title'], r['body']) for r in missing] + ([QUERY_PREFIX + query.strip()[:BODY_CHARS]] if query.strip() else [])
    if texts:
        vectors = embed(settings, texts, timeout)
        if missing:  # just arrived: embed now, and keep the vector
            with connect() as db:
                save(db, settings, missing, vectors[:len(missing)])
        probes += [(r['id'], r['version'], v) for r, v in zip(missing, vectors)]
    asked = vectors[len(missing)] if query.strip() else None
    scored, part = [], {}  # (margin over its floor, similarity, event_id); event_id -> (margin, similarity, start, chars) of its best later passage
    if probes or asked:
        with connect() as db:
            # A seed may have changed/deleted while its embedding request was running.
            versions = {r[0]: r[1] for r in db.execute('SELECT id,version FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in seeds) + ')', seeds)} if seeds else {}
            live_probes = [vector for event_id, version, vector in probes if versions.get(event_id) == version]
            # CROSS JOIN: each vector, then its event by id. A plain join walked every event of the accounts (most have no
            # vector) by events_account_time and looked each vector up: a search took twice as long.
            for event_id, blob in db.execute(
                    'SELECT v.event_id,v.vector FROM event_vectors v CROSS JOIN events e ON e.id=v.event_id '
                    'WHERE e.account_id IN (' + marks + ') AND e.deleted=0 AND v.version=e.version AND v.model=? AND v.dims=?'
                    + (' AND e.history=0' if signals_only else ''), (*accounts, model, dims)):
                if event_id in skip:
                    continue
                vector = unpack(blob)
                comparisons = [(c - floor, c) for c in (cosine(p, vector) for p in live_probes)] + [(c - query_floor, c) for c in ([cosine(asked, vector)] if asked else [])]
                if not comparisons:
                    continue
                best = max(comparisons)
                if best[0] >= 0:
                    scored.append((*best, event_id))
            for event_id, start, chars, blob in db.execute(
                    'SELECT p.event_id,p.start,p.chars,p.vector FROM event_passages p CROSS JOIN events e ON e.id=p.event_id '
                    'WHERE e.account_id IN (' + marks + ') AND e.deleted=0 AND p.version=e.version AND p.model=? AND p.dims=?'
                    + (' AND e.history=0' if signals_only else ''), (*accounts, model, dims)):
                if event_id in skip:
                    continue
                vector = unpack(blob)
                comparisons = [(c - floor, c) for c in (cosine(p, vector) for p in live_probes)] + [(c - query_floor, c) for c in ([cosine(asked, vector)] if asked else [])]
                best = max(comparisons, default=(-1, 0))
                if best[0] >= 0 and best > part.get(event_id, (-1, 0))[:2]:
                    part[event_id] = (*best, start, chars)
    if part:  # one line per signal: its best part
        whole = {i: (m, s) for m, s, i in scored}
        part = {i: p for i, p in part.items() if p[:2] > whole.get(i, (-1, 0))}
        scored = [(m, s, i) for m, s, i in scored if i not in part] + [(p[0], p[1], i) for i, p in part.items()]
    scored.sort(reverse=True)
    similarity = {i: s for _, s, i in scored}
    hit = lambda i: Hit(i, round(similarity[i], 3) if i in similarity else None, *part.get(i, (0, 0, None, 0))[2:])
    semantic = [i for _, _, i in scored[:max(limit * 3, 30)]]
    if not query.strip():
        return [hit(i) for i in semantic[:limit]]
    with connect() as db:
        keyword = [i for i in fts_ids(db, accounts, query, max(limit * 3, 30), signals_only) if i not in skip]
    fused = {}
    for ranking in (semantic, keyword):
        for rank, event_id in enumerate(ranking):
            fused[event_id] = fused.get(event_id, 0) + 1 / (RRF_K + rank + 1)
    best = sorted(fused, key=lambda i: (-fused[i], -similarity.get(i, 0)))[:limit]
    return [hit(i) for i in best]

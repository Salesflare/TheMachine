"""Related signals by meaning (optional): local embedding vectors next to the FTS5 keyword index.

Off unless config has an `embeddings` block ({"url", "model", "dims"}) without `enabled: false`.
Text goes only to that server: meant to be a local one on 127.0.0.1, such as llama.cpp's
`llama-server --embedding` with an EmbeddingGemma GGUF, or any OpenAI-compatible /v1/embeddings
endpoint. `model` is the name the server reports (llama-server's --alias) and is recorded per
vector, so switching models re-embeds. Vectors are Matryoshka-truncated to `dims`, renormalized
and stored as float32 little-endian per event version; deleting an event deletes its vector.
A long meeting or conversation gets more vectors, one per passage after the part the first one covers
(`event_passages`, with where each starts in the body), so a hit can hand back the part that matched.
Search is cosine over the caller's explicit accounts only, fused with FTS5
(reciprocal rank) when there is a query. It scores every vector first from an in-memory copy at 8 bits (Index, about
27 MB per 100k vectors at 256 dims, kept current from event_vector_changes), then reads only the vectors that could
rank and scores those exactly as before, so the result is the same as comparing each stored vector.

Every input is cut to fit the server (`max_input_tokens`, counted conservatively: at most one token
per UTF-8 byte, `bytes_per_token`) and requests are split to stay under `max_batch_tokens`. An input
the server still refuses is set aside per event version (`event_vector_skips`, with the error class)
so it never blocks the others."""
from __future__ import annotations

import array
import contextlib
import heapq
import http.client
import itertools
import json
import math
import os
import re
import struct
import sys
import threading
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
# Which signals' vectors or passages changed (written by triggers, whoever writes them), so the in-memory index (Index)
# reads only those again. Ids only; the oldest rows go once CHANGES_KEPT are newer (an index that far behind reloads).
CHANGES_SCHEMA = 'CREATE TABLE IF NOT EXISTS event_vector_changes(seq INTEGER PRIMARY KEY AUTOINCREMENT,event_id INTEGER NOT NULL)'
CHANGE_TRIGGERS = tuple(
    f'CREATE TRIGGER IF NOT EXISTS {table}_changed_{op} AFTER {op.upper()}{columns} ON {table} BEGIN '
    f'INSERT INTO event_vector_changes(event_id) {ids}; END'
    for table, watched in (('event_vectors', 'event_id,version,model,dims,vector'), ('event_passages', 'event_id,seq,version,model,dims,vector'))
    for op, columns, ids in (('insert', '', 'VALUES(new.event_id)'), ('update', ' OF ' + watched, 'SELECT old.event_id UNION SELECT new.event_id'),
                             ('delete', '', 'VALUES(old.event_id)')))
CHANGES_KEPT = 50000
# Kinds whose late parts are worth finding by meaning: meetings and support conversations. Mail is left out: quoted
# history is cut before embedding, and what is long in its own words is mostly newsletters (keywords still find those).
PASSAGE_KINDS = frozenset({'meeting.notes', 'meeting.transcript', 'zoom.summary', 'zoom.transcript', 'google_meet.notes',
                           'google_meet.transcript', 'teams.notes', 'teams.transcript', 'granola.notes', 'granola.transcript', 'salesflare.meeting', 'intercom.conversation'})
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
    db.execute(CHANGES_SCHEMA)
    for trigger in CHANGE_TRIGGERS:
        db.execute(trigger)
    trim_changes(db)


def trim_changes(db):
    """The change log without what is CHANGES_KEPT behind its newest row."""
    db.execute('DELETE FROM event_vector_changes WHERE seq<=(SELECT max(seq) FROM event_vector_changes)-?', (CHANGES_KEPT,))


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


def floats(blob):
    """A blob's vector as one float32 array where floats are stored little-endian, as pack writes them, else unpack. For
    a vector compared once: a copy of its bytes, not a tuple of floats, about 20% quicker to read and score."""
    return array.array('f', blob) if sys.byteorder == 'little' and len(blob) % 4 == 0 else unpack(blob)


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
        trim_changes(db)
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
        trim_changes(db)
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


class Unindexed(Exception):
    """What the in-memory index can't hold (a vector of another length, a passage number past KEY): search reads every
    stored vector, as before."""


SHIFT = 12  # Index keys: event_id << SHIFT, plus seq + 1 for a passage
INDEXES, INDEX_LOCK, INDEXES_KEPT = {}, threading.Lock(), 2  # (database file, model, dims) -> Index, the newest used last
RELOAD_AT = 5000  # more changed signals than this (or a quarter of the index) since the last search: read it all again
# Reading every vector into the index takes some 40 us each in plain Python: up to INLINE vectors a search does it on
# the spot, more are read by a thread of their own while searches read every vector, as before, until it is done.
INLINE, BUILDING, FAILED, RETRY_S = 20000, set(), {}, 600  # FAILED: key -> when an index couldn't be read (Unindexed)
AMONG = ' AND {}.event_id IN (SELECT value FROM json_each(?))'  # a search's read narrowed to some signals, by the vector's key
SLACK = 1e-6  # on each error bound, for float rounding in the estimate (far below what a ranking shows)
DISTANCE = bytes(abs(b - 128) for b in range(256))  # a stored byte's |value| (bytes.translate)


class Index:
    """One model and size's stored vectors (signals' and their passages') in memory, for search to score them all at
    once instead of reading each from the database: 8 bits per value (each vector in steps of its largest value / 127,
    stored + 128), one vector after another. Per vector D bytes plus 16: 27 MB per 100k vectors at 256 dims.

    lanes scores a probe against every vector in one pass of big-integer arithmetic (a lane of a few bytes per vector, a
    multiply-add per dimension), and each score has a bound on its error, so search reads and scores exactly only the
    vectors that could still rank (close)."""

    def __init__(self, ident, dims):
        self.ident, self.dims, self.seq = ident, dims, -1
        self.keys, self.free = array.array('q'), []  # per slot: its key, or -1 when free
        self.scales, self.sizes = array.array('f'), array.array('f')  # per slot: its step, and step * sum of |stored values|
        self.rows, self.most = bytearray(), (0.0, 0.0)  # the largest step and size kept (bounds only grow until a reload)

    def refresh(self, db, model, whole=True):
        """Up to date with the database as this transaction sees it: the changed signals read again, or all of it
        (False instead when not `whole`)."""
        low, top = db.execute('SELECT min(seq),max(seq) FROM event_vector_changes').fetchone()
        top = top or 0
        if 0 <= self.seq <= top and (low is None or low <= self.seq + 1):
            changed = [r[0] for r in db.execute('SELECT DISTINCT event_id FROM event_vector_changes WHERE seq>?', (self.seq,))]
            if len(changed) <= max(RELOAD_AT, len(self.keys) // 4):
                self.read(db, model, changed)
                self.seq = top
                return True
        if not whole:
            return False
        self.__init__(self.ident, self.dims)
        self.read(db, model, None)
        self.seq = top
        return True

    def read(self, db, model, changed):
        """Every vector of the model and size (changed None), or the changed signals' again."""
        if changed is not None:
            if not changed:
                return
            gone = set(changed)
            for slot, key in enumerate(self.keys):
                if key >> SHIFT in gone:
                    self.keys[slot] = -1
                    self.free.append(slot)
        within = '' if changed is None else ' AND event_id IN (SELECT value FROM json_each(?))'
        args = (model, self.dims) + (() if changed is None else (json.dumps(changed),))
        for event_id, blob in db.execute('SELECT event_id,vector FROM event_vectors WHERE model=? AND dims=?' + within, args):
            self.put(event_id << SHIFT, blob)
        for event_id, seq, blob in db.execute('SELECT event_id,seq,vector FROM event_passages WHERE model=? AND dims=?' + within, args):
            if not 0 <= seq < (1 << SHIFT) - 1:
                raise Unindexed('seq')
            self.put((event_id << SHIFT) + seq + 1, blob)

    def put(self, key, blob):
        if len(blob) != 4 * self.dims:
            raise Unindexed('dims')
        vector = floats(blob)
        top = max(map(abs, vector))
        step = array.array('f', [top / 127 * (1 + 1e-6)])[0]  # as kept: every |value| / step stays under 127
        # value / step + 128, rounded to the nearest (all positive, so int() of it + 0.5), without a Python loop
        row = bytes(map(int, map((128.5).__add__, map((1 / step).__mul__, vector)))) if step else bytes([128]) * self.dims
        size = step * sum(row.translate(DISTANCE)) * (1 + 1e-6)  # rounded up as kept
        self.most = (max(self.most[0], step), max(self.most[1], size))
        if self.free:
            slot = self.free.pop()
            self.keys[slot], self.scales[slot], self.sizes[slot] = key, step, size
            self.rows[slot * self.dims:(slot + 1) * self.dims] = row
        else:
            self.keys.append(key); self.scales.append(step); self.sizes.append(size)
            self.rows += row

    def lanes(self, probe):
        """(per slot: sum(q * stored) + off, off, step, |probe|_1 / 2) for the probe in steps of its own, q = probe / step
        rounded. A score is then step * scale * (lane - off), within scale * |probe|_1 / 2 + step / 2 * size: each value's
        rounding times the other's. All slots at once: per dimension, every slot's stored value spread to a lane of
        `width` bytes in one integer, times q, summed; a lane holds |sum| <= 127 * 255 * D with its sign."""
        dims, n = self.dims, len(self.keys)
        step = max(map(abs, probe), default=0.0) / 127
        if not step or not n:
            return None
        q = [round(x / step) for x in probe]
        width = ((127 * 255 * dims).bit_length() + 8) // 8
        buf, total, rows = bytearray(width * n), 0, self.rows
        for j, w in enumerate(q):
            if w:
                buf[::width] = rows[j::dims]
                total += w * int.from_bytes(buf, 'little')
        half = 1 << (8 * width - 1)
        raw = (total + int.from_bytes((bytes(width - 1) + b'\x80') * n, 'little')).to_bytes(width * n, 'little')  # each lane + half
        wide = 4 if width <= 4 else 8
        out = bytearray(wide * n)
        for b in range(width):
            out[b::wide] = raw[b::width]
        return memoryview(out).cast('I' if wide == 4 else 'Q'), half + 128 * sum(q), step, math.fsum(map(abs, probe)) / 2

    def close(self, db, vectors_sql, passages_sql, args, skip, probes, keep):
        """The signals whose best (margin over its floor) could be among the `keep` best at or over 0: every one whose
        upper bound reaches the keep-th best lower bound (0 when fewer). First the slots that could reach a floor with
        the largest scale and size (a compare per slot in C), then only their signals' bounds and whether the search may
        see them (the same SQL as the exact read). None when a probe has another length. probes: [(vector, floor)]."""
        if any(len(vector) != self.dims for vector, _ in probes):
            return None
        n, keys, (scale, size) = len(self.keys), self.keys, self.most
        scored, flat, near = [], [], set()
        for vector, floor in probes:
            lanes = self.lanes(vector)
            if lanes is None:  # a probe of zeros: every cosine is 0
                flat.append(floor)
                if floor <= SLACK:
                    near.update(range(n))
                continue
            values, off, step, spread = lanes
            scored.append((*lanes, floor))
            room = floor - scale * spread - step / 2 * size - SLACK  # what (lane - off) * step * scale must reach
            if room <= 0:
                near.update(range(n))
            elif scale:
                least = off + math.floor(room / (step * scale)) - 1
                near.update(itertools.compress(range(n), map(least.__le__, values)))
        events = sorted({keys[slot] >> SHIFT for slot in near if keys[slot] >= 0} - set(skip))
        if not events:
            return set()
        within = (*args, json.dumps(events))
        seen = {r[0] << SHIFT for r in db.execute(vectors_sql + AMONG.format('v'), within)}
        seen.update((r[0] << SHIFT) + r[1] + 1 for r in db.execute(passages_sql + AMONG.format('p'), within))
        best_low, best_high = {}, {}
        for slot in near:
            key = keys[slot]
            if key not in seen:
                continue
            scale_, size_, low, high = self.scales[slot], self.sizes[slot], -math.inf, -math.inf
            for values, off, step, spread, floor in scored:
                estimate, error = (values[slot] - off) * step * scale_, scale_ * spread + step / 2 * size_ + SLACK
                low, high = max(low, estimate - error - floor), max(high, estimate + error - floor)
            for floor in flat:
                low, high = max(low, -SLACK - floor), max(high, SLACK - floor)
            if high >= 0:
                event_id = key >> SHIFT
                best_low[event_id] = max(best_low.get(event_id, -math.inf), low)
                best_high[event_id] = max(best_high.get(event_id, -math.inf), high)
        top = heapq.nlargest(keep, best_low.values())
        bar = max(top[-1], 0) if len(top) == keep else 0
        return {event_id for event_id, high in best_high.items() if high >= bar}


def keep_index(key, index):
    """The index kept as the newest used (INDEX_LOCK held), the oldest let go past INDEXES_KEPT."""
    INDEXES.pop(key, None)
    INDEXES[key] = index
    while len(INDEXES) > INDEXES_KEPT:
        INDEXES.pop(next(iter(INDEXES)))


def build_index(connect, key, ident, model, dims):
    """A thread's: every vector into a new index, in a snapshot of its own; searches use it from then on."""
    index = Index(ident, dims)
    try:
        with connect() as db:
            if not db.in_transaction:
                db.execute('BEGIN')
            index.refresh(db, model)
    except Exception:  # Unindexed, or the database busy or gone: searches go on reading every vector, and try later
        index = None
    with INDEX_LOCK:
        BUILDING.discard(key)
        if index is None:
            FAILED[key] = time.monotonic()
        else:
            keep_index(key, index)


@contextlib.contextmanager
def held_index(db, connect, model, dims):
    """The in-memory index of this database file, model and size, up to date and held (one search at a time) in a read
    transaction begun under the hold, so the index, the vectors search reads and their signals are one snapshot. None
    (search reads every vector) while a big one is being read (build_index), for a database without a file or the change
    log, or on a big-endian machine."""
    path = next((r[2] for r in db.execute('PRAGMA database_list') if r[1] == 'main'), '')
    if not path or sys.byteorder != 'little' or not db.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='event_vector_changes'").fetchone():
        yield None
        return
    try:
        stat = os.stat(path)
    except OSError:
        yield None
        return
    key, ident = (path, model, dims), (stat.st_dev, stat.st_ino)
    with INDEX_LOCK:
        began = not db.in_transaction
        if began:
            db.execute('BEGIN')
        try:
            index = INDEXES.pop(key, None)
            try:
                if index is not None and (index.ident != ident or not index.refresh(db, model, whole=False)):
                    index = None
                if index is None and key not in BUILDING and time.monotonic() - FAILED.get(key, -RETRY_S) >= RETRY_S:
                    size = db.execute('SELECT (SELECT count(*) FROM event_vectors WHERE model=?1 AND dims=?2)'
                                      '+(SELECT count(*) FROM event_passages WHERE model=?1 AND dims=?2)', (model, dims)).fetchone()[0]
                    if size > INLINE:
                        BUILDING.add(key)
                        threading.Thread(target=build_index, args=(connect, key, ident, model, dims), name='meaning-index', daemon=True).start()
                    else:
                        index = Index(ident, dims)
                        index.refresh(db, model)
            except Unindexed:
                FAILED[key], index = time.monotonic(), None
            if index is not None:
                keep_index(key, index)
            yield index
        finally:
            if began and db.in_transaction:
                db.commit()


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
    keyword, keep = None, max(limit * 3, 30)
    if probes or asked:
        with connect() as db, held_index(db, connect, model, dims) as index:
            # A seed may have changed/deleted while its embedding request was running.
            versions = {r[0]: r[1] for r in db.execute('SELECT id,version FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in seeds) + ')', seeds)} if seeds else {}
            live_probes = [vector for event_id, version, vector in probes if versions.get(event_id) == version]
            # CROSS JOIN: each vector, then its event by id. A plain join walked every event of the accounts (most have no
            # vector) by events_account_time and looked each vector up: a search took twice as long.
            alone, size = bool(asked) and not live_probes, len(asked) if asked else 0
            history = ' AND e.history=0' if signals_only else ''
            vectors_from = ('FROM event_vectors v CROSS JOIN events e ON e.id=v.event_id WHERE e.account_id IN (' + marks + ') '
                            'AND e.deleted=0 AND v.version=e.version AND v.model=? AND v.dims=?' + history)
            passages_from = ('FROM event_passages p CROSS JOIN events e ON e.id=p.event_id WHERE e.account_id IN (' + marks + ') '
                             'AND e.deleted=0 AND p.version=e.version AND p.model=? AND p.dims=?' + history)
            args = (*accounts, model, dims)
            if query.strip():
                keyword = [i for i in fts_ids(db, accounts, query, keep, signals_only) if i not in skip]
            # The in-memory index's estimates leave out what can't rank; those that can (and the keyword matches, whose
            # similarity is shown) are read and scored exactly below. Without an index every vector is.
            within = index and index.close(db, 'SELECT v.event_id ' + vectors_from, 'SELECT p.event_id,p.seq ' + passages_from, args, skip,
                                           [(vector, floor) for vector in live_probes] + ([(asked, query_floor)] if asked else []), keep)
            narrow = ('', '') if within is None else (AMONG.format('v'), AMONG.format('p'))
            if within is not None:
                args = (*args, json.dumps(sorted(within | set(keyword or ()))))

            def compare(blob):
                """(margin over its floor, similarity) of the vector's best comparison, None without any. A search by its
                query alone (Messages, the palette) compares each vector once: read as an array (floats), one sumprod, no
                lists."""
                if alone:
                    vector = floats(blob)
                    c = math.sumprod(asked, vector) if len(vector) == size else cosine(asked, vector)
                    return c - query_floor, c
                vector = unpack(blob)
                return max([(c - floor, c) for c in (cosine(p, vector) for p in live_probes)] + [(c - query_floor, c) for c in ([cosine(asked, vector)] if asked else [])], default=None)
            for event_id, blob in db.execute('SELECT v.event_id,v.vector ' + vectors_from + narrow[0], args):
                if event_id in skip:
                    continue
                best = compare(blob)
                if best and best[0] >= 0:
                    scored.append((*best, event_id))
            # In stored order either way: of a signal's equally close passages (the same words twice) the first stays.
            for event_id, start, chars, blob in db.execute('SELECT p.event_id,p.start,p.chars,p.vector ' + passages_from + narrow[1] + ' ORDER BY p.rowid', args):
                if event_id in skip:
                    continue
                best = compare(blob)
                if best and best[0] >= 0 and best > part.get(event_id, (-1, 0))[:2]:
                    part[event_id] = (*best, start, chars)
    if part:  # one line per signal: its best part
        whole = {i: (m, s) for m, s, i in scored}
        part = {i: p for i, p in part.items() if p[:2] > whole.get(i, (-1, 0))}
        scored = [(m, s, i) for m, s, i in scored if i not in part] + [(p[0], p[1], i) for i, p in part.items()]
    scored.sort(reverse=True)
    similarity = {i: s for _, s, i in scored}
    hit = lambda i: Hit(i, round(similarity[i], 3) if i in similarity else None, *part.get(i, (0, 0, None, 0))[2:])
    semantic = [i for _, _, i in scored[:keep]]
    if not query.strip():
        return [hit(i) for i in semantic[:limit]]
    if keyword is None:
        with connect() as db:
            keyword = [i for i in fts_ids(db, accounts, query, keep, signals_only) if i not in skip]
    fused = {}
    for ranking in (semantic, keyword):
        for rank, event_id in enumerate(ranking):
            fused[event_id] = fused.get(event_id, 0) + 1 / (RRF_K + rank + 1)
    best = sorted(fused, key=lambda i: (-fused[i], -similarity.get(i, 0)))[:limit]
    return [hit(i) for i in best]

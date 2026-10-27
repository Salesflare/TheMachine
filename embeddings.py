"""Related signals by meaning (optional): local embedding vectors next to the FTS5 keyword index.

Off unless config has an `embeddings` block ({"url", "model", "dims"}) without `enabled: false`.
Text goes only to that server: meant to be a local one on 127.0.0.1, such as llama.cpp's
`llama-server --embedding` with an EmbeddingGemma GGUF, or any OpenAI-compatible /v1/embeddings
endpoint. `model` is the name the server reports (llama-server's --alias) and is recorded per
vector, so switching models re-embeds. Vectors are Matryoshka-truncated to `dims`, renormalized
and stored as float32 little-endian per event version; deleting an event deletes its vector.
Search is brute-force cosine over the caller's explicit accounts only, fused with FTS5
(reciprocal rank) when there is a query."""
from __future__ import annotations

import json
import math
import re
import struct
import time
import urllib.error
import urllib.request

import message_seal

SCHEMA = '''CREATE TABLE IF NOT EXISTS event_vectors(event_id INTEGER PRIMARY KEY REFERENCES events(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,model TEXT NOT NULL,dims INTEGER NOT NULL,vector BLOB NOT NULL)'''
BODY_CHARS = 2000
# Cosine at 256 dims. Signal-to-signal matches that were really related scored 0.6-0.87, a query's
# 0.4-0.5; below these they were mostly unrelated (EmbeddingGemma 300M on a real mailbox, October 2026).
FLOOR, QUERY_FLOOR = 0.6, 0.4
MAX_LIMIT = 20
RRF_K = 60
QUOTED = re.compile(r'\n*\[Quoted earlier messages:.*', re.S)  # the stored marker and the history after it
QUERY_PREFIX = 'task: search result | query: '


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
    body = QUOTED.sub('', body or '')
    body = '\n'.join(line for line in body.splitlines() if not line.lstrip().startswith('>'))
    body = re.sub(r'\s+', ' ', body).strip()[:BODY_CHARS]
    title = re.sub(r'\s+', ' ', title or '').strip()[:300] or 'none'
    return f'title: {title} | text: {body}'


def endpoint(settings):
    url = settings['url'].rstrip('/')
    return url if url.endswith('/embeddings') else url + '/v1/embeddings'


SERVED = {}  # url -> (checked at, model ids the server reports)


def request(settings, texts, timeout=120):
    """POST to the embedding server; returns the raw vectors in input order. The server must report
    the configured model in /v1/models (llama-server echoes any requested name), so a swap never
    mixes vectors."""
    body = json.dumps({'model': settings.get('model', ''), 'input': texts}).encode()
    http = urllib.request.Request(endpoint(settings), body, {'Content-Type': 'application/json'})
    try:
        checked, served = SERVED.get(settings['url'], (-1e9, ()))
        if time.monotonic() - checked > 600:
            with urllib.request.urlopen(endpoint(settings).rsplit('/', 1)[0] + '/models', timeout=min(10, timeout)) as response:
                served = {m.get('id') for m in json.load(response).get('data', [])}
            SERVED[settings['url']] = (time.monotonic(), served)
        if settings.get('model') not in served:
            raise EmbeddingError('model_mismatch')
        with urllib.request.urlopen(http, timeout=timeout) as response:
            data = json.load(response)['data']
    except urllib.error.HTTPError as error:
        raise EmbeddingError(f'http_{error.code}') from None
    except (urllib.error.URLError, OSError) as error:
        raise EmbeddingError('timeout' if 'timed out' in str(error) else 'unreachable') from None
    except (ValueError, KeyError, TypeError):
        raise EmbeddingError('bad_response') from None
    if len(data) != len(texts):
        raise EmbeddingError('bad_response')
    return [item['embedding'] for item in sorted(data, key=lambda d: d.get('index', 0))]


def embed(settings, texts, timeout=120):
    """Normalized vectors at the configured Matryoshka size."""
    dims = int(settings.get('dims', 256))
    result = []
    for vector in request(settings, texts, timeout):
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


def pending(db, settings, limit, newest=True):
    """Live events without a vector for their current version, model and size."""
    return [dict(r) for r in db.execute(
        'SELECT e.id,e.version,e.title,e.body FROM events e LEFT JOIN event_vectors v ON v.event_id=e.id '
        'WHERE e.deleted=0 AND (v.event_id IS NULL OR v.version<>e.version OR v.model<>? OR v.dims<>?) '
        'ORDER BY e.id ' + ('DESC' if newest else 'ASC') + ' LIMIT ?',
        (settings.get('model', ''), int(settings.get('dims', 256)), limit))]


def save(db, settings, rows, vectors):
    # A slow older request must not overwrite a newer version's vector.
    db.executemany('INSERT OR REPLACE INTO event_vectors(event_id,version,model,dims,vector) '
                   'SELECT ?,?,?,?,? WHERE EXISTS(SELECT 1 FROM events WHERE id=? AND version=? AND deleted=0)',
                   [(r['id'], r['version'], settings.get('model', ''), len(v), pack(v), r['id'], r['version']) for r, v in zip(rows, vectors)])


def embed_pending(connect, settings, limit=16, newest=True):
    """One small pass: read, embed outside any transaction, write. Returns the number embedded."""
    with connect() as db:
        rows = pending(db, settings, limit, newest)
    if not rows:
        return 0
    vectors = embed(settings, [document(r['title'], r['body']) for r in rows])
    with connect() as db:
        save(db, settings, rows, vectors)
    return len(rows)


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


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


def fts_ids(db, accounts, query, limit):
    """Keyword ranking (bm25) within the accounts; any word may match, rarer words weigh more."""
    words = [w for w in re.findall(r'\w+', query) if len(w) > 1]
    if not words:
        return []
    marks = ','.join('?' for _ in accounts)
    return [r[0] for r in db.execute(
        'SELECT e.id FROM event_search JOIN events e ON e.id=event_search.rowid WHERE event_search MATCH ? '
        'AND e.account_id IN (' + marks + ') AND e.deleted=0 ORDER BY event_search.rank LIMIT ?',
        (message_seal.match(db, words, ' OR '), *accounts, limit))]


def related(connect, settings, accounts, event_ids=(), query='', limit=8, floor=None, exclude=(), timeout=30, query_floor=None):
    """[(event_id, similarity or None)] best first, only from `accounts`, never the given/excluded ids.
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
    scored = []  # (margin over its floor, similarity, event_id)
    if probes or asked:
        with connect() as db:
            # A seed may have changed/deleted while its embedding request was running.
            versions = {r[0]: r[1] for r in db.execute('SELECT id,version FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in seeds) + ')', seeds)} if seeds else {}
            live_probes = [vector for event_id, version, vector in probes if versions.get(event_id) == version]
            for event_id, blob in db.execute(
                    'SELECT v.event_id,v.vector FROM event_vectors v JOIN events e ON e.id=v.event_id '
                    'WHERE e.account_id IN (' + marks + ') AND e.deleted=0 AND v.version=e.version AND v.model=? AND v.dims=?', (*accounts, model, dims)):
                if event_id in skip:
                    continue
                vector = unpack(blob)
                comparisons = [(c - floor, c) for c in (cosine(p, vector) for p in live_probes)] + [(c - query_floor, c) for c in ([cosine(asked, vector)] if asked else [])]
                if not comparisons:
                    continue
                best = max(comparisons)
                if best[0] >= 0:
                    scored.append((*best, event_id))
    scored.sort(reverse=True)
    similarity = {i: s for _, s, i in scored}
    semantic = [i for _, _, i in scored[:max(limit * 3, 30)]]
    if not query.strip():
        return [(i, round(similarity[i], 3)) for i in semantic[:limit]]
    with connect() as db:
        keyword = [i for i in fts_ids(db, accounts, query, max(limit * 3, 30)) if i not in skip]
    fused = {}
    for ranking in (semantic, keyword):
        for rank, event_id in enumerate(ranking):
            fused[event_id] = fused.get(event_id, 0) + 1 / (RRF_K + rank + 1)
    best = sorted(fused, key=lambda i: (-fused[i], -similarity.get(i, 0)))[:limit]
    return [(i, round(similarity[i], 3) if i in similarity else None) for i in best]

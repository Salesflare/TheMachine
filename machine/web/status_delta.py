"""api/status as a change list: what changed since the answer a page already holds.

The dashboard polls api/status (some 900 KB on a busy Machine) every few seconds, and nearly all of it is the same
from one poll to the next. Each answer gets a token; a page that sends it back (?since=) gets only the parts that
changed: a top-level part that is the same is left out, and in a list of rows with ids (the to-dos, promises,
deliveries) a row that is the same comes as {"=": id}. The page puts its copy together again (shell-tabs.js
statusMerge). Kept here per token: a short digest per part and per row, never the answer itself. An unknown token (a
restart, an old page) gets the whole answer, as does a request without one (the CLI, the apps)."""
import collections
import hashlib
import json
import secrets
import threading

KEEP = 32  # tokens kept: a few pages on a few devices, each asking again with its last one

_SEEN = collections.OrderedDict()  # token -> {part: digest | (digest, {row id: digest})}
_LOCK = threading.Lock()


def _digest(value):
    return hashlib.blake2b(json.dumps(value, sort_keys=True, separators=(',', ':'), default=str).encode(),
                           digest_size=8).digest()


def _rows(value):
    """A list whose every row is a dict with an id (unique), so rows can be matched by id; else None."""
    if not isinstance(value, list) or not value or not all(isinstance(r, dict) and 'id' in r for r in value):
        return None
    ids = [json.dumps(r['id']) for r in value]
    return ids if len(set(ids)) == len(ids) else None


def digests(status):
    """{part: digest} for each top-level part, with a digest per row for the lists of rows with ids."""
    out = {}
    for key, value in status.items():
        ids = _rows(value)
        if ids is None:
            out[key] = _digest(value)
        else:
            rows = {i: _digest(r) for i, r in zip(ids, value)}
            out[key] = (_digest([[i, rows[i]] for i in ids]), rows)
    return out


def changes(status, since=None):
    """The answer for a page holding the answer of token `since`: all of it with a new `_token` when `since` is
    unknown, else `_since` and only what changed (`_gone`: parts no longer there)."""
    now = digests(status)
    token = secrets.token_urlsafe(9)
    with _LOCK:
        before = _SEEN.get(since) if since else None
        _SEEN[token] = now
        while len(_SEEN) > KEEP:
            _SEEN.popitem(last=False)
    if before is None:
        return {**status, '_token': token}
    out = {'_token': token, '_since': since}
    for key, value in status.items():
        was, digest = before.get(key), now[key]
        if isinstance(digest, tuple):
            if isinstance(was, tuple) and was[0] == digest[0]:
                continue
            kept = was[1] if isinstance(was, tuple) else {}
            out[key] = [{'=': row['id']} if kept.get(i) == digest[1][i] else row
                        for i, row in zip(_rows(value), value)]
        elif was != digest:
            out[key] = value
    gone = sorted(set(before) - set(now))
    if gone:
        out['_gone'] = gone
    return out

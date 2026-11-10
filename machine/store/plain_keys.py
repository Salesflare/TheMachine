"""Once, after the update: the routing keys that joined the plain metadata keys (message_seal.ROUTING_KEYS: end_at,
status, recurring_event_id, chat_kind) become readable to SQLite in the messages kept before.

A message stored from this version on keeps them in the clear by itself. One sealed before has them inside its sealed
member, where SQL sees NULL. This goes over the `events` rows once, oldest first, and seals each one's metadata again
with today's plain keys. Only metadata is rewritten: the title, the body and every other key stay sealed as they were.

- In batches (BATCH rows): a batch is read and sealed again without the write lock, then written in one short
  transaction that first looks whether each row is still what was read (one a sync changed meanwhile was already
  written with today's keys and is left alone). A pause between batches lets the service write.
- Resumable: `plain_key_pass` keeps the last row done. Stopped halfway, the next start goes on from there; a row done
  twice is left as it is (nothing of it is hidden any more), so nothing is sealed twice or lost.
- A row that does not open (damaged, or sealed with another key) is left untouched and counted.
- Without the message key (kept by the hosting or the keyring and not there yet), or with one that opens none of the
  newest sealed rows, nothing is read or written: it waits and the worker tries again.
- A copy of the database comes first (Store.copy_before, as for the other one-time fixes), once, and only when there
  is something to change. store_fixes marks the pass done.

Until it is done nothing reads wrong: the SQL that filters on these keys also takes the rows where it cannot see the
key and decides those from the opened row, as before (Store.calendar, the Connections count, enrichment).

One writer used one of these names for something else: Salesforce kept a task's Status, a word the organization's
admin chose, as `status`. It is `task_status` now (connectors/salesforce.py) and stays sealed; RENAMED moves it in
the rows kept before, with the row's content hash when that still matches, so the next sync sees no change."""
import contextlib
import hashlib
import json
import time

import message_seal
from machine.text import encoded
from timeutil import now

NAME = 'plain-routing-keys'
BATCH = 500
PAUSE = 0.05  # seconds between batches: the service's own writes go first
KEY_SAMPLE = 50  # newest rows looked at to see whether the key opens what is sealed
RENAMED = {'salesforce.activity': (('status', 'task_status'),)}
TABLE = ('CREATE TABLE IF NOT EXISTS plain_key_pass(id INTEGER PRIMARY KEY CHECK(id=1),last_id INTEGER NOT NULL,top_id INTEGER NOT NULL,'
         'copied INTEGER NOT NULL DEFAULT 0,changed INTEGER NOT NULL DEFAULT 0,unread INTEGER NOT NULL DEFAULT 0,started_at TEXT NOT NULL)')


@contextlib.contextmanager
def _raw(store):
    """The store's connection with rows as SQLite has them (sealed values stay sealed): this reads what is stored."""
    with store.connect() as db:
        kept, db.row_factory = db.row_factory, None
        try:
            yield db
        finally:
            db.row_factory = kept


def renamed(kind, metadata):
    """The metadata with this kind's RENAMED keys moved, or None when there is nothing to move."""
    moves = [(old, new) for old, new in RENAMED.get(kind, ()) if old in metadata and new not in metadata]
    if not moves:
        return None
    out = dict(metadata)
    for old, new in moves:
        out[new] = out.pop(old)
    return out


def resealed(sealer, kind, stored):
    """(new stored text, metadata before, metadata after) for a row's metadata as stored, or None when it is as it
    should be. Raises ValueError (message_seal.SealError) for a sealed one that does not open."""
    if type(stored) is not str or not stored.lstrip().startswith('{'):
        return None  # nothing, or not an object (sealed whole): no keys to keep in the clear
    sealed = message_seal.is_sealed_json(stored)
    if sealed and not sealer:
        raise message_seal.SealError('No message key')
    try:
        seen = json.loads(stored)
        before = json.loads(sealer.open_json(stored)) if sealed else seen
    except message_seal.SealError:
        raise
    except ValueError:
        return None  # not JSON: left as it is
    if not isinstance(before, dict) or not isinstance(seen, dict):
        return None
    after = renamed(kind, before)
    hidden = sealed and any(key in message_seal.PLAIN_METADATA and key not in seen for key in before)
    if after is None and not hidden:
        return None
    text = encoded(after if after is not None else before)
    return (sealer.seal_json(text) if sealed else text), before, (after if after is not None else before)


def _hashes(db, sealer, row_id, before, after):
    """(content hash now, content hash with the renamed keys) when the row's hash is the one commit_page gave this
    event, else None: the next sync then finds the same event and nothing looks edited."""
    row = db.execute('SELECT account_id,source_id,kind,occurred_at,title,body,deleted,content_hash FROM events WHERE id=?', (row_id,)).fetchone()
    try:
        title, body = (sealer.open(v) if sealer and type(v) is bytes else v for v in (row[4], row[5]))
    except ValueError:
        return None
    event = {'account_id': row[0], 'source_id': row[1], 'kind': row[2], 'occurred_at': row[3], 'title': title, 'body': body, 'deleted': bool(row[6])}
    digest = lambda metadata: hashlib.sha256(encoded({**event, 'metadata': metadata}).encode()).hexdigest()
    return (row[7], digest(after)) if digest(before) == row[7] else None


def key_fits(store):
    """Whether the store's key opens what is sealed: the newest sealed metadata. True when nothing is sealed."""
    with _raw(store) as db:
        rows = [m for (m,) in db.execute('SELECT metadata FROM events ORDER BY id DESC LIMIT ?', (KEY_SAMPLE,)) if message_seal.is_sealed_json(m)]
    if not rows:
        return True
    if not store.sealer:
        return False
    for stored in rows:
        try:
            store.sealer.open_json(stored)
            return True
        except ValueError:
            continue
    return False


def progress(db):
    """{last_id, top_id, copied, changed, unread, done} of the pass, or None before it began."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='plain_key_pass'").fetchone():
        return None
    row = db.execute('SELECT last_id,top_id,copied,changed,unread FROM plain_key_pass WHERE id=1').fetchone()
    if not row:
        return None
    done = bool(db.execute('SELECT 1 FROM store_fixes WHERE name=?', (NAME,)).fetchone())
    return {**dict(zip(('last_id', 'top_id', 'copied', 'changed', 'unread'), tuple(row))), 'done': done}


def _begin(store):
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        db.execute(TABLE)
        # rows after the newest one now are stored by this version: their keys are in the clear already
        db.execute('INSERT OR IGNORE INTO plain_key_pass(id,last_id,top_id,started_at) VALUES(1,0,(SELECT coalesce(max(id),0) FROM events),?)', (now(),))
        return progress(db)


def _copy(store):
    """The copy of the database before the first change, once. A copy that did not finish is removed."""
    try:
        store.copy_before(NAME)
    except Exception:
        for left in store.path.parent.glob(f'{store.path.name}.before-{NAME}-*'):
            left.unlink(missing_ok=True)
        raise
    with store.connect() as db:
        db.execute('UPDATE plain_key_pass SET copied=1 WHERE id=1')


def step(store, batch=BATCH):
    """One batch. Returns (rows read, rows changed, rows that did not open); rows read is 0 once the pass is over."""
    with _raw(store) as db:
        state = progress(db)
        rows = db.execute('SELECT id,kind,metadata FROM events WHERE id>? AND id<=? ORDER BY id LIMIT ?', (state['last_id'], state['top_id'], batch)).fetchall()
        if not rows:
            return 0, 0, 0
        changes, unread = [], 0
        for row_id, kind, stored in rows:
            try:
                new = resealed(store.sealer, kind, stored)
            except ValueError:
                unread += 1  # left untouched
                continue
            if new:
                moved = new[1] is not new[2]
                changes.append((row_id, stored, new[0], _hashes(db, store.sealer, row_id, new[1], new[2]) if moved else None))
    if changes and not state['copied']:
        _copy(store)
    changed = 0
    with _raw(store) as db:
        db.execute('BEGIN IMMEDIATE')
        if progress(db)['last_id'] != state['last_id']:
            return len(rows), 0, 0  # another run of the pass did this batch
        current = dict(db.execute('SELECT id,metadata FROM events WHERE id>=? AND id<=?', (changes[0][0], changes[-1][0]))) if changes else {}
        for row_id, stored, new, hashes in changes:
            if current.get(row_id) != stored:
                continue  # changed since it was read: written with today's keys already
            store.restore_metadata(db, row_id, new, hashes)
            changed += 1
        db.execute('UPDATE plain_key_pass SET last_id=?,changed=changed+?,unread=unread+? WHERE id=1', (rows[-1][0], changed, unread))
    return len(rows), changed, unread


def run(store, stop=None, batch=BATCH, pause=None, batches=None):
    """The pass, from where it was. Returns {'state', 'changed', 'unread'}: state is 'done' (now or before),
    'waiting' (the message key is not there or does not open the messages: nothing was touched) or 'stopped' (the
    service is stopping, or `batches` ran). None when it had been done before this call."""
    if store.fix_done(NAME):
        return None
    pause = PAUSE if pause is None else pause
    with store.connect() as db:
        sealed = message_seal.is_protected(db)
    if (sealed and not store.sealer) or not key_fits(store):
        return {'state': 'waiting', 'changed': 0, 'unread': 0}
    _begin(store)
    ran = 0
    while True:
        if (stop is not None and stop.is_set()) or (batches is not None and ran >= batches):
            state = 'stopped'
            break
        read, _, _ = step(store, batch)
        ran += 1
        if not read:
            store.mark_fix_done(NAME)
            state = 'done'
            break
        if pause:
            stop.wait(pause) if stop is not None else time.sleep(pause)
    with store.connect() as db:
        found = progress(db)
    return {'state': state, 'changed': found['changed'], 'unread': found['unread']}

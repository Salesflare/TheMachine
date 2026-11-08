"""Once, after the update: messages whose to-do save failed before a failed save kept them for the next review
(review_saves.py, release-20261107-1942) were marked reviewed or set aside with no to-do. A review that left out
dedupe_key got "That didn't go through" on every save, so its messages never came back and their to-dos were missed.

This finds them in the agent's own transcripts (read-only): suggest calls whose exec failed, from WINDOW_START on and
at most MAX_AGE_DAYS back, whose messages are in no to-do now. Each goes back to the review once (pending, no
deferrals); the review dedupes against existing to-dos as for any message, so nothing is made twice. Messages a failed
save since the fix keeps (review_save_failures) are that fix's to hold. A plain scan, no model calls. A copy of the
database comes first (Store.copy_before), and store_fixes marks it done, so it runs once."""
import base64
import contextlib
import datetime as dt
import json
import logging
import re
import sqlite3
import subprocess

from machine.store.events import SET_ASIDE_AFTER
from machine.store import review_saves

LOG = logging.getLogger('personal-assistant')

NAME = 'failed-saves-requeue'
WINDOW_START = dt.datetime(2026, 11, 6, tzinfo=dt.timezone.utc)  # before the release that lost the saves
MAX_AGE_DAYS = 14  # an older message is no to-do any more: it stays as it is

SUGGEST = re.compile(r"""["']?action["']?\s*:\s*["']suggest["']""")
NEXT_ACTION = re.compile(r"""["']?action["']?\s*:""")
EVENT_IDS = re.compile(r"""["']?event_ids["']?\s*:\s*\[([\d\s,]*)\]""")

# zstd (OpenClaw keeps older transcript events packed) for Pythons before 3.14: Node 22.15+ has it built in
NODE_UNZSTD = ("const z=require('zlib');let s='';process.stdin.on('data',d=>s+=d).on('end',()=>process.stdout.write("
               "JSON.stringify(JSON.parse(s).map(b=>z.zstdDecompressSync(Buffer.from(b,'base64')).toString()))))")


def unpack(blobs, node='node'):
    """The texts of these zstd blobs."""
    try:
        from compression import zstd
        return [zstd.decompress(b).decode() for b in blobs]
    except ImportError:
        pass
    texts = []
    for start in range(0, len(blobs), 500):
        chunk = [base64.b64encode(b).decode() for b in blobs[start:start + 500]]
        done = subprocess.run([node, '-e', NODE_UNZSTD], input=json.dumps(chunk), capture_output=True, text=True, timeout=120, check=True)
        texts += json.loads(done.stdout)
    return texts


def suggested_ids(arguments):
    """The event_ids of each suggest call in a tool call's arguments (an exec's code, or the call itself)."""
    if not isinstance(arguments, dict):
        return []
    text = arguments['code'] if isinstance(arguments.get('code'), str) else json.dumps(arguments)
    ids = []
    for found in SUGGEST.finditer(text):
        rest = text[found.end():]
        following = NEXT_ACTION.search(rest)
        listed = EVENT_IDS.search(rest[:following.start()] if following else rest)
        if listed:
            ids += [int(i) for i in re.findall(r'\d+', listed.group(1))]
    return ids


def failed(message):
    """A tool result that says its call failed: the exec's status, or an error result. "Read what came after first" is a
    step of the review, not a failed save."""
    content = message.get('content')
    text = ' '.join(str(c.get('text', '')) for c in content if isinstance(c, dict)) if isinstance(content, list) else str(content or '')
    if review_saves.GUIDANCE in text:
        return False
    details = message.get('details') if isinstance(message.get('details'), dict) else {}
    if message.get('isError') is True or details.get('status') == 'failed':
        return True
    try:
        result = json.loads(text)
    except ValueError:
        return False
    return isinstance(result, dict) and result.get('status') == 'failed'


def failed_saves(agent_db, since, node='node'):
    """{event_id} in suggest calls that failed in the agent's transcripts since then."""
    with contextlib.closing(sqlite3.connect(f'file:{agent_db}?mode=ro', uri=True, timeout=30)) as db:
        rows = db.execute('SELECT event_json,event_zstd FROM transcript_events WHERE created_at>=? ORDER BY session_id,seq',
                          (int(since.timestamp() * 1000),)).fetchall()
    packed = [i for i, (text, blob) in enumerate(rows) if text is None and blob is not None]
    texts = [text for text, _ in rows]
    for i, text in zip(packed, unpack([rows[i][1] for i in packed], node)):
        texts[i] = text
    calls, ids = {}, set()
    for text in texts:
        try:
            message = (json.loads(text) if text else {}).get('message') or {}
        except (ValueError, AttributeError):
            continue
        content = message.get('content')
        for part in content if isinstance(content, list) else []:
            if isinstance(part, dict) and part.get('type') == 'toolCall':
                found = suggested_ids(part.get('arguments'))
                if found:
                    calls[part.get('id')] = found
        if message.get('role') == 'toolResult' and message.get('toolCallId') in calls and failed(message):
            ids.update(calls[message['toolCallId']])
    return ids


def requeue(store, agent_db, node='node', now=None):
    """Once: the messages of failed saves that ended in no to-do go back to the review. Returns how many."""
    now = now or dt.datetime.now(dt.timezone.utc)
    with store.connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS store_fixes(name TEXT PRIMARY KEY,at TEXT NOT NULL)')
        if db.execute('SELECT 1 FROM store_fixes WHERE name=?', (NAME,)).fetchone():
            return 0
    oldest = max(WINDOW_START, now - dt.timedelta(days=MAX_AGE_DAYS))
    ids = failed_saves(agent_db, oldest, node) if agent_db and agent_db.exists() else set()
    lost = sorted(lost_ids(store, ids, oldest))
    if lost:
        store.copy_before(NAME)
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM store_fixes WHERE name=?', (NAME,)).fetchone():
            return 0
        lost = lost_ids(store, lost, oldest, db)  # as they are now, in the same transaction
        db.executemany('UPDATE events SET analyzed_version=min(analyzed_version,version-1),deferrals=0 WHERE id=?', [(i,) for i in lost])
        db.execute('INSERT INTO store_fixes(name,at) VALUES(?,?)', (NAME, now.isoformat()))
    return len(lost)


def lost_ids(store, ids, oldest, db=None):
    """Of these, the messages marked reviewed or set aside, from oldest on, in no to-do and not held by a later failure."""
    if not ids:
        return set()
    if db is None:
        with store.connect() as db:
            return lost_ids(store, ids, oldest, db)
    review_saves.ensure(db)
    in_todo = set()
    for (event_ids,) in db.execute('SELECT event_ids FROM suggestions'):
        try:
            in_todo.update(int(i) for i in json.loads(event_ids or '[]'))
        except (ValueError, TypeError):
            continue
    marks = ','.join('?' * len(ids))
    rows = db.execute(f'SELECT id FROM events WHERE id IN ({marks}) AND deleted=0 AND occurred_at>=? '
                      'AND (analyzed_version>=version OR deferrals>=?) '
                      'AND id NOT IN (SELECT event_id FROM review_save_failures)', (*ids, oldest.isoformat(), SET_ASIDE_AFTER))
    return {r[0] for r in rows} - in_todo

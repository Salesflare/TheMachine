"""A review's to-do saves (suggest): a dedupe_key it left out is made from the to-do's source message, arguments it got
wrong are told back in words it can act on, and a save that failed keeps its messages out of reviewed, so the next
review tries them again (finish_analysis) instead of marking them done with no to-do."""
import json
import re

from timeutil import now


# A failed save older than this no longer holds its messages back: the review that hit it is long over.
FAILED_HOURS = 6

# How suggest's "read what came after the evidence first" starts (assistant.py): a step of the review, not a failed save.
GUIDANCE = 'Something happened after this to-do'


def ensure(db):
    db.execute('CREATE TABLE IF NOT EXISTS review_save_failures(event_id INTEGER PRIMARY KEY, failed_at TEXT NOT NULL, error TEXT NOT NULL)')


def slug(text, words=6):
    return '-'.join(re.findall(r'[a-z0-9]+', str(text).lower())[:words]) or 'todo'


def derived_key(db, event_ids, title):
    """account:thread:title-words, from the first message of the to-do's evidence: the same matter in the same thread
    gets the same key, so a later review updates its to-do instead of making a second one."""
    row = db.execute(f"SELECT account_id,source_id,metadata FROM events WHERE id IN ({','.join('?' * len(event_ids))}) ORDER BY id LIMIT 1",
                     event_ids).fetchone()
    if not row:
        return None
    try:
        thread = (json.loads(row['metadata'] or '{}') or {}).get('thread_id')
    except (ValueError, AttributeError):
        thread = None
    return f"{row['account_id']}:{thread or row['source_id']}:{slug(title)}"


def ready(db, args):
    """The suggest args with a dedupe_key; a ValueError that says what to change when they can't make a to-do."""
    if not isinstance(args, dict):
        raise ValueError('suggest takes args {"title", "body", "event_ids", "dedupe_key"}')
    ids = args.get('event_ids')
    if not isinstance(ids, list) or not ids or not all(isinstance(i, int) and not isinstance(i, bool) for i in ids):
        raise ValueError('suggest needs event_ids: the ids of the messages this to-do comes from, as a list of numbers')
    missing = [k for k in ('title', 'body') if not isinstance(args.get(k), str) or not args[k].strip()]
    if missing:
        hint = ' Put the to-do in title and body, not in suggestion.' if 'suggestion' in args else ''
        raise ValueError(f"suggest needs {' and '.join(missing)}: a short title and a body of about three sentences.{hint}")
    known = {r[0] for r in db.execute(f"SELECT id FROM events WHERE id IN ({','.join('?' * len(ids))})", ids)}
    if set(ids) - known:
        raise ValueError(f'Unknown event_ids {sorted(set(ids) - known)}: use the ids begin_analysis or events gave you')
    if isinstance(args.get('dedupe_key'), str) and args['dedupe_key'].strip():
        return args
    return {**args, 'dedupe_key': derived_key(db, ids, args['title'])}


def failed(db, event_ids, error):
    """A save for these messages didn't go through: they stay out of reviewed until one does."""
    ids = [i for i in event_ids if isinstance(i, int) and not isinstance(i, bool)] if isinstance(event_ids, list) else []
    if ids:
        ensure(db)
        db.executemany('INSERT OR REPLACE INTO review_save_failures(event_id,failed_at,error) VALUES(?,?,?)',
                       [(i, now(), str(error)[:200]) for i in ids])


def saved(db, event_ids):
    ensure(db)
    db.executemany('DELETE FROM review_save_failures WHERE event_id=?', [(i,) for i in event_ids])


def take(db, event_ids, since):
    """{event_id} of these whose last save failed since then; their records go, so each failure holds them back once."""
    ensure(db)
    marks = ','.join('?' * len(event_ids))
    held = {r[0] for r in db.execute(f'SELECT event_id FROM review_save_failures WHERE event_id IN ({marks}) AND failed_at>=?', (*event_ids, since))} if event_ids else set()
    if event_ids:
        db.execute(f'DELETE FROM review_save_failures WHERE event_id IN ({marks})', event_ids)
    return held

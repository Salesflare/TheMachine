"""Why a finished review made no to-do of a message (finish_analysis no_todo and replies), kept apart from the review's
items (analyses.items: ids, versions and flags, which SQL reads): the words come from the messages, so analyses.whys is
sealed (message_seal.DERIVED). {"<event id>": {"no_todo": "…", "no_reply": "…"}}; an item keeps no_reply as a flag."""
from __future__ import annotations

import json

WORDS = ('no_todo', 'no_reply')


def read(value):
    """{event id: {'no_todo', 'no_reply'}} of an analyses.whys value."""
    try:
        found = json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}
    return {int(k): v for k, v in found.items() if str(k).isdigit() and isinstance(v, dict)} if isinstance(found, dict) else {}


def text(whys):
    return json.dumps({str(k): v for k, v in whys.items()}, ensure_ascii=False) if whys else ''


def said(whys, event_id):
    """The line on why one message got no to-do, '' when there is none."""
    found = whys.get(int(event_id)) or {}
    return next((found[k] for k in WORDS if isinstance(found.get(k), str) and found[k].strip()), '')


def drop(db, analysis_id, event_ids):
    """The words about messages the owner excluded or deleted go with them."""
    row = db.execute('SELECT whys FROM analyses WHERE id=?', (analysis_id,)).fetchone()
    whys = read(row[0]) if row else {}
    kept = {k: v for k, v in whys.items() if k not in event_ids}
    if kept != whys:
        db.execute('UPDATE analyses SET whys=? WHERE id=?', (text(kept), analysis_id))


def move(db):
    """Finished reviews from before whys (or by an older release since): their words move out of items. Returns how many."""
    if not db.execute("SELECT 1 FROM analyses WHERE whys IS NULL AND status='complete' LIMIT 1").fetchone():
        return 0
    rows = db.execute("SELECT id,items FROM analyses WHERE whys IS NULL AND (instr(items,'\"no_todo\"')>0 OR instr(items,'\"no_reply\"')>0)").fetchall()
    moved = 0
    for analysis_id, stored in rows:
        try:
            items = json.loads(stored)
        except (TypeError, ValueError):
            continue
        whys = {}
        for item in items if isinstance(items, list) else ():
            if not isinstance(item, dict):
                continue
            words = {k: item[k] for k in WORDS if isinstance(item.get(k), str)}
            item.pop('no_todo', None)
            if 'no_reply' in item:
                item['no_reply'] = bool(item['no_reply'])
            if words and not item.get('excluded') and str(item.get('id') or '').isdigit():
                whys[int(item['id'])] = words
        db.execute('UPDATE analyses SET items=?,whys=? WHERE id=?', (json.dumps(items), text(whys), analysis_id))
        moved += 1
    db.execute("UPDATE analyses SET whys='' WHERE whys IS NULL AND status='complete'")  # looked at, once
    return moved

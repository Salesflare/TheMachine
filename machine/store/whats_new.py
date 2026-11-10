"""What's new: one small notice on the dashboard when a bigger feature or improvement shipped (dashboard/
shell-whats-new.js). The entries ship here, with the code: nothing is fetched. A person only sees entries dated after
they finished getting started on this Machine (no backlog), at most once a day, at most SHOWN at a time, newest first.
What they saw is kept on their Machine (the `whats_new` milestone), so it never shows again on another device.

Adding an entry (CONTRIBUTING.md, What's new): only for something a person would want to be told about. Add it at the
top with a new id and the day it merges, then add its strings to the catalogs (scripts/i18n_extract.py --add).
- id: never changes and is never reused.
- date: the day it shipped (YYYY-MM-DD).
- title: a few words. text: one or two short sentences: what changed and what the person can do now.
- action (optional): {'label': the button, 'run': a command id of the dashboard's palette (dashboard/shell-keys.js
  ACTIONS, like 'go-routines'), or 'search' for Search}. tests/test_whats_new.py checks it exists."""
import datetime as dt
import json

import i18n
from timeutil import local_day, now

ENTRIES = [
    {'id': 'routines', 'date': '2026-11-09', 'title': 'Routines run work for you',
     'text': 'Tell The Machine what to do and how often, and it does it by itself. Or start from a template, like '
             'Newsletter cleanup or Birthdays.',
     'action': {'label': 'Open Routines', 'run': 'go-routines'}},
    {'id': 'ask-from-search', 'date': '2026-11-07', 'title': 'Search answers questions',
     'text': 'Type a question into Search and get a short answer from your own messages, with a link to each message '
             'it used.',
     'action': {'label': 'Open Search', 'run': 'search'}},
    {'id': 'export', 'date': '2026-11-06', 'title': 'Take everything with you',
     'text': 'Export everything your Machine keeps, or what it learned as files any AI can read. It’s in Settings, '
             'under General.',
     'action': {'label': 'Open Settings', 'run': 'go-settings-general'}},
]

SHOWN = 3  # entries in one notice; older new ones just count as seen

SETTLE_HOURS = 24  # nothing this long after getting started: the first look's own ending shows then

MARK = 'whats_new'  # milestones: at = when a notice was last closed, detail = {"seen": [ids]}


def onboarded(db):
    """When this person finished getting started on this Machine (ISO text), or None while they still are: when the
    first look stopped digging; on an install that never had one (it reviewed before first looks existed), when its
    first review finished."""
    row = db.execute("SELECT at FROM milestones WHERE name='first_dig_done'").fetchone()
    if row:
        return row[0]
    if db.execute('SELECT 1 FROM review_runs WHERE window_hours IS NOT NULL LIMIT 1').fetchone():
        return None  # its first look is still going
    return db.execute("SELECT min(finished_at) FROM review_runs WHERE status='ok'").fetchone()[0]


def seen(db):
    """(when a notice was last closed, the ids seen so far)."""
    row = db.execute('SELECT at,detail FROM milestones WHERE name=?', (MARK,)).fetchone()
    if not row:
        return None, set()
    try:
        ids = json.loads(row[1] or '{}').get('seen') or []
    except (ValueError, AttributeError):
        ids = []
    return row[0], {str(i) for i in ids}


def due(db, current=None, entries=None):
    """The entries to tell this person about now, newest first: dated after the day they finished getting started, not
    seen yet. None of them while they are getting started (and SETTLE_HOURS after), or when a notice was closed today."""
    current = current or dt.datetime.fromisoformat(now())
    start = onboarded(db)
    if not start or dt.datetime.fromisoformat(start) + dt.timedelta(hours=SETTLE_HOURS) > current:
        return []
    last, known = seen(db)
    today = local_day(current)
    if last and local_day(last) == today:
        return []
    first = local_day(start).isoformat()
    new = [e for e in (ENTRIES if entries is None else entries)
           if first < e['date'] <= today.isoformat() and e['id'] not in known]
    return sorted(new, key=lambda e: e['date'], reverse=True)


def view(db, current=None, entries=None):
    """The notice for the dashboard's status, in the person's language: {'entries': [{'id', 'title', 'text',
    'action': {'label', 'run'} or None}]}, SHOWN at most (older new ones are left out), or None."""
    new = due(db, current, entries)
    if not new:
        return None
    return {'entries': [{'id': e['id'], 'title': i18n.t(e['title']), 'text': i18n.t(e['text']),
                         'action': {'label': i18n.t(e['action']['label']), 'run': e['action']['run']} if e.get('action') else None}
                        for e in new[:SHOWN]]}


def mark_seen(db, current=None, entries=None):
    """The notice was closed (Close or its button): everything that was due counts as seen, the ones it left out
    too, and nothing more shows today. Nothing is written when nothing was due."""
    new = due(db, current, entries)
    if not new:
        return False
    current = current or dt.datetime.fromisoformat(now())
    known = seen(db)[1] | {e['id'] for e in new}
    db.execute('INSERT OR REPLACE INTO milestones(name,at,detail) VALUES(?,?,?)',
               (MARK, current.isoformat(), json.dumps({'seen': sorted(known)})))
    return True


class WhatsNewStore:
    """Store methods for the dashboard's What's new notice."""

    def whats_new(self, current=None, entries=None):
        with self.connect() as db:
            return view(db, current, entries)

    def whats_new_seen(self, current=None, entries=None):
        with self.connect() as db:
            mark_seen(db, current, entries)
        return {'whats_new': None}

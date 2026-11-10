"""What's new: one small notice on the dashboard about bigger features and improvements (dashboard/
shell-whats-new.js). ENTRIES is a pool of candidates that ship here, with the code: nothing is fetched. A release adds
to the pool; it never pushes a notice by itself.

Once a day, in the owner's early morning (MORNING, local time), the Machine picks what to tell today (pick_step, run
by the daily worker): the top PICKED unseen candidates by weight, then the newest, from those dated after the day this
person finished getting started (no backlog) and within the last KEEP_DAYS days (older ones expire unseen). Nothing may
qualify: then there is no notice that day. The pick shows the next time the dashboard opens that day; what wasn't picked
stays in the pool for a later morning. What a person saw is kept on their Machine (the `whats_new` milestone), so it
never shows again, on any device.

Adding a candidate (CONTRIBUTING.md, What's new): only for something a person would want to be told about. Add it at the
top with a new id and the day it merges, then add its strings to the catalogs (scripts/i18n_extract.py --add).
`scripts/release.py cut` checks a release's new entries with problems() below.
- id: never changes and is never reused.
- date: the day it shipped (YYYY-MM-DD).
- weight: how much a person would care, 1 to 3 (3: a new thing most people will use; 2: a clear improvement to
  something they use; 1: a small change worth a line). It decides the order, so set it honestly.
- title: a few words. text: one or two short sentences: what changed and what the person can do now.
- who (optional): 'team' for something only someone in a Work Fleet can use.
- action (optional): {'label': the button, 'run': a command id of the dashboard's palette (dashboard/shell-keys.js
  ACTIONS, like 'go-routines'), or 'search' for Search}. tests/test_whats_new.py checks it exists.
- art (optional): the name of its picture in WN_ART (dashboard/shell-whats-new.js): a small drawing of the feature in
  the dashboard's own look, without words (CONTRIBUTING.md says how to draw one). Without one the entry is text only,
  or a plain stand-in when others in the same notice have a picture."""
import datetime as dt
import json
import re

import i18n
from timeutil import local_day, local_tz, now

ENTRIES = [
    {'id': 'project-descriptions', 'date': '2026-11-10', 'weight': 2, 'title': 'Projects describe themselves',
     'text': 'A project’s page says what it is and where it stands, and keeps that up to date. Edit it to make it yours.',
     'action': {'label': 'Open Projects', 'run': 'go-projects'}, 'art': 'project'},
    {'id': 'team-boards-timeline', 'date': '2026-11-10', 'weight': 2, 'who': 'team', 'title': 'More of the team’s work',
     'text': 'A board shared with the team now shares every project on it. What teammates shared is in the Timeline, '
             'under Team.',
     'action': {'label': 'Open Projects', 'run': 'go-projects'}, 'art': 'team'},
    {'id': 'routines', 'date': '2026-11-09', 'weight': 3, 'title': 'Routines run work for you',
     'text': 'Tell The Machine what to do and how often, and it does it by itself. Or start from a template, like '
             'Newsletter cleanup or Birthdays.',
     'action': {'label': 'Open Routines', 'run': 'go-routines'}, 'art': 'routines'},
    {'id': 'ask-from-search', 'date': '2026-11-07', 'weight': 3, 'title': 'Search answers questions',
     'text': 'Type a question into Search and get a short answer from your own messages, with a link to each message '
             'it used.',
     'action': {'label': 'Open Search', 'run': 'search'}, 'art': 'search'},
    {'id': 'export', 'date': '2026-11-06', 'weight': 2, 'title': 'Take everything with you',
     'text': 'Export everything your Machine keeps, or what it learned as files any AI can read. It’s in Settings, '
             'under General.',
     'action': {'label': 'Open Settings', 'run': 'go-settings-general'}, 'art': 'export'},
]

PICKED = 5  # at most this many in one morning's notice; 0 is fine

KEEP_DAYS = 21  # a candidate older than this expires unseen

MORNING = (5, 12)  # local hours: the pick is made from 05:00, or later that morning when the Machine was off at five

SETTLE_HOURS = 24  # nothing this long after getting started: the first look's own ending shows then

MARK = 'whats_new'  # milestones: at = when a notice was last closed, detail = {"seen": [ids]}

PICK = 'whats_new_pick'  # milestones: at = when the morning's pick was made, detail = {"day": local day, "ids": [ids]}

KEYS = {'id', 'date', 'weight', 'title', 'text', 'who', 'action', 'art'}


def problems(entry):
    """What is wrong with one candidate, as short lines (empty when it is fine). The picture's and the button's names
    are checked against the dashboard by tests/test_whats_new.py; this needs nothing but the entry."""
    if not isinstance(entry, dict):
        return ['not a dict']
    found = [f'unknown key {k}' for k in sorted(set(entry) - KEYS)]
    found += [f'no {k}' for k in ('id', 'date', 'weight', 'title', 'text') if entry.get(k) in (None, '')]
    if entry.get('id') and not re.fullmatch(r'[a-z0-9-]+', str(entry['id'])):
        found.append('id: lowercase letters, digits and dashes only')
    try:
        dt.date.fromisoformat(str(entry.get('date')))
    except ValueError:
        found.append('date: YYYY-MM-DD')
    if entry.get('weight') is not None and (type(entry['weight']) is not int or not 1 <= entry['weight'] <= 3):
        found.append('weight: 1, 2 or 3')
    if entry.get('who') not in (None, 'team'):
        found.append("who: 'team' or left out")
    action = entry.get('action')
    if action is not None and not (isinstance(action, dict) and action.get('label') and action.get('run')):
        found.append('action: {label, run}')
    texts = [entry.get('title') or '', entry.get('text') or '', (action or {}).get('label', '') if isinstance(action, dict) else '']
    if any(re.search('[—–!]', str(t)) for t in texts):
        found.append('no em or en dashes and no exclamation marks')
    if len(str(entry.get('title') or '')) > 40:
        found.append('title: 40 characters at most')
    if len(str(entry.get('text') or '')) > 160:
        found.append('text: 160 characters at most')
    return found


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


def _detail(db, name):
    row = db.execute('SELECT at,detail FROM milestones WHERE name=?', (name,)).fetchone()
    if not row:
        return None, {}
    try:
        detail = json.loads(row[1] or '{}')
    except ValueError:
        detail = {}
    return row[0], detail if isinstance(detail, dict) else {}


def seen(db):
    """(when a notice was last closed, the ids seen so far)."""
    at, detail = _detail(db, MARK)
    ids = detail.get('seen')
    return at, {str(i) for i in ids} if isinstance(ids, list) else set()


def candidates(db, current, entries=None, team=False):
    """The candidates this person could be told about today, best first (weight, then the newest): dated after the day
    they finished getting started and at most KEEP_DAYS old, not seen yet, for the team only on a Machine in a Work
    Fleet. None while they are getting started (and SETTLE_HOURS after)."""
    start = onboarded(db)
    if not start or dt.datetime.fromisoformat(start) + dt.timedelta(hours=SETTLE_HOURS) > current:
        return []
    known = seen(db)[1]
    today = local_day(current)
    first, oldest = local_day(start).isoformat(), (today - dt.timedelta(days=KEEP_DAYS)).isoformat()
    pool = [e for e in (ENTRIES if entries is None else entries)
            if first < e['date'] <= today.isoformat() and e['date'] >= oldest and e['id'] not in known
            and (team or e.get('who') != 'team')]
    return sorted(pool, key=lambda e: (e.get('weight') or 1, e['date']), reverse=True)


def pick_step(db, current=None, entries=None, team=False):
    """The morning's pick: once a day, in the owner's MORNING hours, the top PICKED candidates are what today's notice
    shows. Outside those hours, or when today's pick is made, nothing changes. The ids picked, or None."""
    current = current or dt.datetime.fromisoformat(now())
    local = current.astimezone(local_tz())
    if not MORNING[0] <= local.hour < MORNING[1]:
        return None
    day = local.date().isoformat()
    if _detail(db, PICK)[1].get('day') == day:
        return None
    ids = [e['id'] for e in candidates(db, current, entries, team)[:PICKED]]
    db.execute('INSERT OR REPLACE INTO milestones(name,at,detail) VALUES(?,?,?)',
               (PICK, current.isoformat(), json.dumps({'day': day, 'ids': ids})))
    return ids


def due(db, current=None, entries=None):
    """The entries to tell this person about now: this morning's pick, in its order, less what they saw already. None
    before the morning's pick, on a day it picked nothing, or once today's notice was closed."""
    current = current or dt.datetime.fromisoformat(now())
    detail = _detail(db, PICK)[1]
    if detail.get('day') != local_day(current).isoformat():
        return []
    last, known = seen(db)
    if last and local_day(last) == local_day(current):
        return []
    by_id = {e['id']: e for e in (ENTRIES if entries is None else entries)}
    ids = detail.get('ids') if isinstance(detail.get('ids'), list) else []
    return [by_id[i] for i in ids if i in by_id and i not in known]


def view(db, current=None, entries=None):
    """The notice for the dashboard's status, in the person's language: {'entries': [{'id', 'title', 'text',
    'action': {'label', 'run'} or None, 'art': its picture or None}]} (this morning's pick), or None."""
    new = due(db, current, entries)
    if not new:
        return None
    return {'entries': [{'id': e['id'], 'title': i18n.t(e['title']), 'text': i18n.t(e['text']), 'art': e.get('art'),
                         'action': {'label': i18n.t(e['action']['label']), 'run': e['action']['run']} if e.get('action') else None}
                        for e in new[:PICKED]]}


def mark_seen(db, current=None, entries=None):
    """The notice was closed (Close or its button): what it showed counts as seen and never shows again, and nothing
    more shows today. What wasn't picked stays in the pool. Nothing is written when nothing was due."""
    new = due(db, current, entries)
    if not new:
        return False
    current = current or dt.datetime.fromisoformat(now())
    known = seen(db)[1] | {e['id'] for e in new[:PICKED]}
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

    def whats_new_pick(self, current=None, entries=None, team=False):
        with self.connect() as db:
            return pick_step(db, current, entries, team)

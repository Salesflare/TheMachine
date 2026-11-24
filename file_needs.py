"""How often a preparation has a linked file other than a Google Doc, and how often one it needs is missing, for The
Machine team: which kind of file is worth reading next. OPEN: off until the privacy policy, the help and the setting's own
words say these numbers go; until then nothing is asked, counted or sent.

Counted when a preparation saves its result or its blocker, once per job: which kinds of file its messages and the
owner's chat link to (links, by address alone), and the kind the run itself says it needed and couldn't open or find
(file_missing, a word of its save). Kept here as those kinds, the day and the job's id, which never leaves this Machine.

Once a day the finished days go with the error reports and under the same Settings switch (Send error reports), over
the Network: POST /errors {"action": "file_needs", "day", "runs", "linked": {kind: runs}, "missing": {kind: runs}}. Only
numbers: no names, no addresses, no contents, no ids. Off: nothing is counted or sent, and what waited is deleted.
Kept KEEP_DAYS here."""
from __future__ import annotations

import datetime as dt
import json
import re
import urllib.parse

import error_feed
import timeutil

SCHEMA = '''
CREATE TABLE IF NOT EXISTS file_need_runs(job TEXT PRIMARY KEY,day TEXT NOT NULL,linked TEXT NOT NULL,missing TEXT);
CREATE TABLE IF NOT EXISTS file_need_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL);
'''
LINKED = ('sheet', 'slides', 'pdf', 'drive', 'cloud')  # drive: a Word, Excel or other file in Google Drive; cloud: another cloud drive
MISSING = ('doc', 'sheet', 'slides', 'pdf', 'word', 'other')
OPEN = False
KEEP_DAYS = 30
BACK_DAYS = 7           # a finished day is sent at most this late
SEND_EVERY = 6 * 3600
URL = re.compile(r'https?://[^\s<>"\'()\[\]|]+')
GOOGLE = re.compile(r'/(?:a/[^/]+/)?(?:u/\d+/)?(spreadsheets|presentation|document)/(?:u/\d+/)?d/')
DRIVE = re.compile(r'/(?:file/(?:u/\d+/)?d/.|open$|uc$)')
PDF = re.compile(r'\.pdf\b', re.I)
CLOUD = {'dropbox.com': r'/(?:s|scl|sh|l)/', 'onedrive.live.com': r'/.', '1drv.ms': r'/.', 'sharepoint.com': r'/.', 'box.com': r'/(?:s|file)/',
         'icloud.com': r'/iclouddrive/', 'wetransfer.com': r'/downloads/', 'we.tl': r'/.'}


def ensure(db):
    for statement in SCHEMA.split(';'):
        if statement.strip():
            db.execute(statement)


def kind(url, before=''):
    """The kind of linked file an address is, or None (a Google Doc, a page). before: the words in front of it on its line
    (a Drive link doesn't say what the file is; a name in front of it does)."""
    try:
        parts = urllib.parse.urlsplit(url.rstrip('.,;:!?'))
        host = (parts.hostname or '').lower()
    except ValueError:
        return None
    if host == 'docs.google.com':
        found = GOOGLE.match(parts.path)
        if not found:
            return None
        if 'rtpof=true' in parts.query:
            return 'drive'  # an Office file opened in Google's editor
        return {'spreadsheets': 'sheet', 'presentation': 'slides'}.get(found.group(1))
    if host == 'drive.google.com':
        return None if not DRIVE.match(parts.path) else 'pdf' if PDF.search(before[-120:]) else 'drive'
    for name, path in CLOUD.items():
        if (host == name or host.endswith('.' + name)) and re.match(path, parts.path):
            return 'cloud'
    return 'pdf' if parts.path.lower().endswith('.pdf') else None


def links(text):
    """The kinds of linked file in this text."""
    out = set()
    for line in str(text or '').split('\n'):
        start = 0
        for found in URL.finditer(line):
            out.add(kind(found.group(0), line[start:found.start()]))
            start = found.end()
    return out - {None}


def prompt():
    """The preparation prompt's line asking for file_missing, while this counts."""
    return f"\n- When a file the task needs can't be opened or found, add file_missing:<{', '.join(MISSING[:-1])} or {MISSING[-1]}> to that save or blocker (only counted)." if OPEN else ''


def note(db, suggestion_id, job, missing=None):
    """A preparation saved its result or blocker: counted once per job, the last word on a missing file kept. missing: the
    kind the run says it needed and couldn't open or find; anything else it says counts as other. A read failing here never
    holds up the save (the caller's try)."""
    if not OPEN or not job or not error_feed.on(db):
        return
    ensure(db)
    said = (missing if missing in MISSING else 'other') if missing else None
    found = set()
    for body, metadata in db.execute("SELECT e.body,e.metadata FROM suggestions s JOIN json_each(s.event_ids) ids JOIN events e ON e.id=ids.value WHERE s.id=?",
                                     (suggestion_id,)).fetchall():
        found |= links(body) | links(str(metadata or '').replace('\\n', '\n'))
    for (text,) in db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND choice='other' AND source IN ('telegram','dashboard') "
                              "AND feedback LIKE '%://%' ORDER BY created_at DESC LIMIT 50", (suggestion_id,)).fetchall():
        found |= links(text)
    db.execute('INSERT INTO file_need_runs(job,day,linked,missing) VALUES(?,?,?,?) ON CONFLICT(job) DO UPDATE SET linked=excluded.linked,missing=excluded.missing',
               (str(job), timeutil.clock().date().isoformat(), json.dumps(sorted(found)), said))


def day_payload(db, day):
    """One finished day's numbers, as they go; None when nothing was prepared."""
    rows = db.execute('SELECT linked,missing FROM file_need_runs WHERE day=?', (day,)).fetchall()
    if not rows:
        return None
    linked, missing = {}, {}
    for kinds, said in rows:
        for k in json.loads(kinds):
            linked[k] = linked.get(k, 0) + 1
        if said:
            missing[said] = missing.get(said, 0) + 1
    return {'action': 'file_needs', 'day': day, 'runs': len(rows), 'linked': linked, 'missing': missing}


def send(connect, call, current=None):
    """The finished days not sent yet (the last BACK_DAYS), one call each, at most every SEND_EVERY. Returns days sent."""
    current = current or timeutil.clock()
    put = "INSERT INTO file_need_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value"
    with connect() as db:
        ensure(db)
        if not OPEN or not error_feed.on(db):
            db.execute('DELETE FROM file_need_runs')
            return 0
        db.execute('DELETE FROM file_need_runs WHERE day<?', ((current.date() - dt.timedelta(days=KEEP_DAYS)).isoformat(),))
        row = db.execute("SELECT value FROM file_need_prefs WHERE key='tried_at'").fetchone()
        if row and row[0] > (current - dt.timedelta(seconds=SEND_EVERY)).isoformat(timespec='seconds'):
            return 0
        db.execute(put, ('tried_at', current.isoformat(timespec='seconds')))
        last = (db.execute("SELECT value FROM file_need_prefs WHERE key='sent_day'").fetchone() or [''])[0]
        days = [(current.date() - dt.timedelta(days=k)).isoformat() for k in range(BACK_DAYS, 0, -1)]
        payloads = [p for p in (day_payload(db, d) for d in days if d > last) if p]
    sent = 0
    for payload in payloads:
        answer = call('POST', '/errors', payload)
        if not (isinstance(answer, dict) and answer.get('ok') is True):
            return sent
        with connect() as db:
            db.execute(put, ('sent_day', payload['day']))
        sent += 1
    with connect() as db:  # nothing left before today: the days with none count as sent too
        db.execute(put, ('sent_day', days[-1]))
    return sent

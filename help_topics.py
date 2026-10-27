"""What people ask Help (help_chat.py), for The Machine team: a few generic words per question, counted per day.

The Help turn ends with a TOPIC: line ("snooze a to-do"); without one, the topic is the title of the help section
that matched best. The question and the answer never go. Before a topic is kept here it must pass, in order:
- team_learnings.strip with every name this Machine knows (its graph and accounts): nothing may be taken out;
- team_learnings.case_problems: no quoted text, no capitalized word that isn't a product or screen name;
- plain lowercase words only, at most 6, and every word must come from the public help pages (help_chat.vocabulary),
  so a customer's name, a company or a detail from a message can't pass even when nothing above caught it.
One that fails is kept as "other" when no help page matched, and dropped otherwise.

Once a day the finished days go to the control plane over the Network (POST /learnings {"action": "help_topics"}),
only {topic, answered, n}, and are deleted here once it took them. The control plane keeps counts per day and topic,
without the account (cloud/help_topics.py there), for /admin. On by default; Settings, The Machine team, Share what
Help is asked turns it off, and turning it off deletes what waits here."""
from __future__ import annotations

import datetime as dt
import re

import team_learnings

SCHEMA = '''CREATE TABLE IF NOT EXISTS help_topics(day TEXT NOT NULL,topic TEXT NOT NULL,answered INTEGER NOT NULL,n INTEGER NOT NULL,
  PRIMARY KEY(day,topic,answered));'''
WORDS = 6
TOPICS = 40         # a day's topics sent, most asked first (the control plane takes as many)
KEEP_DAYS = 14      # unsent days older than this go (the control plane takes no older)
PLAIN = re.compile(r"[a-z0-9][a-z0-9 '-]*")
GENERIC = {'other', 'setup', 'set', 'up', 'change', 'how', 'turn', 'off', 'on', 'not', 'working', 'error', 'problem', 'to-do'}


def ensure(db):
    team_learnings.ensure(db)
    db.execute(SCHEMA)


def on(db):
    """Settings, Share what Help is asked: on unless the owner turned it off."""
    ensure(db)
    return team_learnings.pref(db, 'help_topics', 'on') != 'off'


def set_on(db, value):
    ensure(db)
    team_learnings.set_pref(db, 'help_topics', 'on' if value else 'off')
    if not value:
        db.execute('DELETE FROM help_topics')


def clean(raw, names=(), vocabulary=None):
    """The topic as it may go, or None."""
    import help_chat
    text = ' '.join(str(raw or '').replace('"', ' ').split()).strip(' .,:;')
    if not text or len(text) > 60:
        return None
    stripped, taken = team_learnings.strip(text, names)
    if taken or team_learnings.case_problems(stripped):
        return None
    text = text.lower()
    if not PLAIN.fullmatch(text) or len(text.split()) > WORDS:
        return None
    known = vocabulary if vocabulary is not None else help_chat.vocabulary()
    if any(w not in known and w not in help_chat.STOP and w not in GENERIC for w in (help_chat.stem(x) for x in help_chat.WORD.findall(text))):
        return None
    return text


def record(db, config, topic, answered, today=None, vocabulary=None):
    """Count one Help question under its topic, when sharing is on. The topic kept, or None."""
    if not on(db):
        return None
    kept = clean(topic, team_learnings.known_names(db, config), vocabulary) or (None if answered else 'other')
    if not kept:
        return None
    day = today or dt.date.today().isoformat()
    db.execute('INSERT INTO help_topics(day,topic,answered,n) VALUES(?,?,?,1) ON CONFLICT(day,topic,answered) DO UPDATE SET n=n+1',
               (day, kept, 1 if answered else 0))
    return kept


def send(db_connect, call, today=None):
    """Send each finished day (before today), one call a day, and delete it here once the control plane took it."""
    today = today or dt.date.today().isoformat()
    oldest = (dt.date.fromisoformat(today) - dt.timedelta(days=KEEP_DAYS)).isoformat()
    with db_connect() as db:
        ensure(db)
        db.execute('DELETE FROM help_topics WHERE day<?', (oldest,))
        if not on(db):
            return 0
        days = [r[0] for r in db.execute('SELECT DISTINCT day FROM help_topics WHERE day<? ORDER BY day', (today,))]
    sent = 0
    for day in days:
        with db_connect() as db:
            rows = db.execute('SELECT topic,answered,n FROM help_topics WHERE day=? ORDER BY n DESC, topic LIMIT ?', (day, TOPICS)).fetchall()
        body = {'action': 'help_topics', 'day': day, 'topics': [{'topic': t, 'answered': bool(a), 'n': n} for t, a, n in rows]}
        try:
            answer = call('POST', '/learnings', body)
        except Exception:
            break  # the Network is away: tomorrow
        if not isinstance(answer, dict) or answer.get('ok') is not True:
            break
        with db_connect() as db:
            db.execute('DELETE FROM help_topics WHERE day=?', (day,))
        sent += 1
    return sent

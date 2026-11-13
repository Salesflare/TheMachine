"""How likely a waiting signal is to bring a to-do, for the order the reviews read them in (2026-11-13). The first look
reads the most likely first (Store.most_promising), so its first to-do comes from the top of the queue; a regular review
reads its claimed batch in the same order (Store.begin_analysis). Only the order changes: what a review claims, and
that every signal gets reviewed, stays as it was.

Read on this Machine from what is already there, with no model call: who wrote to whom (need_rank), whether the owner
answered in the thread since (answered) or is in a live thread with them, a direct question or an ask in the subject or
the first lines of the body (never the quoted part), an ask with a date, a sender the Graph knows against a mailing or a
system (review_wait.mail_wait, graph.bulk), Gmail's own Important mark, and how recent it is. A score, highest first;
nothing leaves the Machine and nothing is kept."""
import datetime as dt
import json
import math
import re

from machine.store import review_wait


# Words read from the top of the body only: a reply quotes the whole thread under it
BODY_CHARS = 1500

# Where a reply's quoted part starts: "On <date>, <name> wrote:", "-----Original Message-----", a "From:" header block
QUOTE_START = re.compile(r'(?im)^(?:on .{0,200}wrote:|-{2,}\s*original message|from:\s.+$|op .{0,200}schreef.*:|le .{0,200}a [ée]crit\s*:|am .{0,200}schrieb.*:)')

# An ask of the owner, in the languages the app speaks
ASK = re.compile(
    r"(?i)\b(?:can you|could you|would you|will you|can we|could we|are you able|please|pls|let me know|lmk|"
    r"what do you think|thoughts\?|your (?:feedback|input|approval|answer|go-ahead)|waiting (?:for|on) you|need (?:you|your)|"
    r"kun je|kan je|kunt u|zou je|wil je|graag|laat (?:me|maar) weten|"
    r"pourriez|pouvez-vous|peux-tu|merci de|"
    r"können sie|kannst du|könnten sie|bitte|"
    r"puedes|podrías|podría|por favor|"
    r"você pode|poderia|pode me|"
    r"puoi|potresti|potrebbe|per favore)\b")

# An ask with a time on it: a deadline, a day, a date
DATED = re.compile(
    r"(?i)\b(?:deadline|due|eod|end of (?:the )?(?:day|week|month)|asap|"
    r"(?:by|before|until|no later than|ahead of)\s+(?:today|tonight|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|"
    r"next week|the \d{1,2}(?:st|nd|rd|th)?|\d{1,2}[/.-]\d{1,2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|noon|\d{1,2}(?::\d{2})?\s*(?:am|pm|h)))\b|"
    r"\b(?:tomorrow|morgen|demain|mañana|amanhã|domani|vóór|voor (?:maandag|dinsdag|woensdag|donderdag|vrijdag)|avant (?:lundi|mardi|mercredi|jeudi|vendredi)|"
    r"bis (?:montag|dienstag|mittwoch|donnerstag|freitag))\b")

# A line that only thanks or passes something on: rarely anything for the owner to do
COURTESY = re.compile(r"(?i)^\W*(?:re:\s*|fwd?:\s*)*(?:thanks?(?: you)?|thx|great|perfect|ok(?:ay)?|got it|noted|fyi|dank je|bedankt|merci|danke|gracias|obrigad[oa]|grazie)\b")

# Base by who wrote to whom (Store.need_rank): a person writing to the owner, their appointments, one of many, automated or their own
BASE = {0: 4.0, 1: 1.5, 2: 1.0, 3: -3.0}

QUESTION, ASKED, WITH_DATE, KNOWN, IMPORTANT, LIVE_THREAD = 1.5, 1.0, 1.0, 1.0, 0.75, 1.0
MAILING, COURTESY_ONLY = -2.0, -1.5
THREAD_CHECKS = 200  # at most this many thread lookups (answered, a live thread) per ordering: a query each
RECENT_HOURS = 48  # recency adds up to 1, halving about every 33 hours; what is coming within this long adds 0.5


def metadata(row):
    value = row.get('metadata') if isinstance(row, dict) else row['metadata']
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}


def top_text(body):
    """The body above its quoted part, at most BODY_CHARS."""
    text = str(body or '')[:BODY_CHARS * 2]
    found = QUOTE_START.search(text)
    if found:
        text = text[:found.start()]
    return '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('>'))[:BODY_CHARS]


def words(row):
    """{question, ask, dated, courtesy} from the subject and the top of the body."""
    title, body = str(row.get('title') or ''), top_text(row.get('body'))
    text = title + '\n' + body
    question = '?' in title or '?' in body
    ask = bool(ASK.search(text))
    return {'question': question, 'ask': ask, 'dated': bool(DATED.search(text) or review_wait.TIME_SENSITIVE.search(title)),
            'courtesy': bool(COURTESY.search(title) or COURTESY.search(body.strip()[:80])) and not question and not ask}


def recency(row, current):
    try:
        at = dt.datetime.fromisoformat(str(row['occurred_at']))
    except (TypeError, ValueError):
        return 0.0
    if at.tzinfo is None:
        at = at.replace(tzinfo=dt.timezone.utc)
    hours = (current - at).total_seconds() / 3600
    if hours < 0:  # coming up
        return 0.5 if -hours <= RECENT_HOURS else 0.0
    return math.exp(-hours / RECENT_HOURS)


def score(row, rank, current, people=None, answered=False, live_thread=False):
    """How likely this signal brings a to-do, higher first. `rank`: Store.need_rank; `answered`: the owner wrote in its
    thread since; `live_thread`: a reply in a thread the owner wrote in; `people`: review_wait.People, or None."""
    m = metadata(row)
    rank = 2 if rank == 0 and answered else rank
    value = BASE.get(rank, 1.0) + recency(row, current)
    if rank == 3 or answered:
        return value  # the owner's own and automated: last, newest first; what they answered since asks nothing more of them
    w = words(row)
    value += QUESTION * w['question'] + ASKED * w['ask'] + WITH_DATE * w['dated'] + COURTESY_ONLY * w['courtesy']
    if row['kind'] == 'gmail.message':
        labels = set(m.get('labels') or ())
        value += IMPORTANT * ('IMPORTANT' in labels) + LIVE_THREAD * bool(live_thread and not answered)
        sender = review_wait.sender(m)
        if sender and people is not None and people.person(sender):
            value += KNOWN
        elif review_wait.mail_wait(m, row.get('title') or '', people):
            value += MAILING
    return value


def order(rows, scores):
    """`rows` by score, highest first; equal scores keep their order."""
    return [rows[i] for i in sorted(range(len(rows)), key=lambda i: (-scores[i], i))]

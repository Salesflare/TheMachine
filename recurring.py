"""Recurring to-dos (docs/help/recurring.md): a to-do that comes back on a rhythm.

A series is one to-do that repeats: daily, on weekdays, weekly, monthly (on a date, or "the first Monday"), yearly, or
every N days, weeks or months. Its rule is small JSON (RULE): {'unit': 'day'|'weekday'|'week'|'month'|'year', 'n': N,
'nth': 1..4 or -1 for a month's first..fourth or last weekday}. The weekday, the day of the month and the date of the
year come from the series' anchor, its first date.

One open occurrence at a time. The next one appears on its date (the owner's own calendar day) once the one before is
done, not needed or skipped (tick). A missed one stays open and counts what it missed (missed); occurrences never stack.
Snoozing moves only that to-do. Each occurrence is an ordinary to-do (Store.owner_card) in the same Work or Personal
account and project, so it is prepared like any other; its preparation gets the previous occurrence's result
(prep_lines).

Offers: when a learned note says the owner does something on a rhythm, or the owner closed the same to-do on a regular
rhythm, the dashboard asks once "Make this a recurring to-do?" (offers). Nothing is created without the owner's tap.

Tables (this module owns them): recurring_series, recurring_cards (each occurrence and its date), recurring_offers."""
import calendar
import datetime as dt
import json
import re
import uuid

UNITS = ('day', 'weekday', 'week', 'month', 'year')
N_MAX = 52
CLOSED = ('completed', 'rejected')  # anything else still open (pending, accepted, prepared, instructions, snoozed)
OFFER_DAYS = 200  # how far back a rhythm in closed to-dos is looked for


def ensure(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS recurring_series(
        id TEXT PRIMARY KEY,rule TEXT NOT NULL,anchor TEXT NOT NULL,text TEXT NOT NULL,account_id TEXT NOT NULL,
        work INTEGER NOT NULL DEFAULT 0,project TEXT,current_id TEXT,due TEXT,next_due TEXT,last_id TEXT,last_done TEXT,
        stopped_at TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS recurring_cards(
        suggestion_id TEXT PRIMARY KEY,series_id TEXT NOT NULL,due TEXT NOT NULL,created_at TEXT NOT NULL);
      CREATE INDEX IF NOT EXISTS recurring_cards_series ON recurring_cards(series_id,due);
      CREATE TABLE IF NOT EXISTS recurring_offers(
        key TEXT PRIMARY KEY,source TEXT NOT NULL,title TEXT NOT NULL,text TEXT NOT NULL,rule TEXT NOT NULL,anchor TEXT NOT NULL,
        card_id TEXT,status TEXT NOT NULL DEFAULT 'open',created_at TEXT NOT NULL,decided_at TEXT);
    ''')


# --- rules and dates -------------------------------------------------------------------------------------------------

def clean_rule(rule):
    """A rule from the dashboard or a parse, checked: {'unit', 'n'[, 'nth']}. ValueError when it isn't one."""
    if isinstance(rule, str):
        rule = PRESETS.get(rule) or (json.loads(rule) if rule.startswith('{') else None)
    if not isinstance(rule, dict) or rule.get('unit') not in UNITS:
        raise ValueError('Pick how often it repeats')
    n = rule.get('n', 1)
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= N_MAX:
        raise ValueError('Repeat every 1 to 52')
    out = {'unit': rule['unit'], 'n': 1 if rule['unit'] in ('weekday', 'year') else n}
    if rule['unit'] == 'month' and rule.get('nth') is not None:
        if rule['nth'] not in (1, 2, 3, 4, -1):
            raise ValueError('Pick the first to fourth, or the last, weekday of the month')
        out['nth'] = rule['nth']
    return out


PRESETS = {'daily': {'unit': 'day', 'n': 1}, 'weekdays': {'unit': 'weekday', 'n': 1}, 'weekly': {'unit': 'week', 'n': 1},
           'monthly': {'unit': 'month', 'n': 1}, 'yearly': {'unit': 'year', 'n': 1}}


def _add_months(day, months, keep):
    y, m = divmod(day.month - 1 + months, 12)
    year, month = day.year + y, m + 1
    return dt.date(year, month, min(keep, calendar.monthrange(year, month)[1]))


def _nth_weekday(year, month, weekday, nth):
    days = [d for d in range(1, calendar.monthrange(year, month)[1] + 1) if dt.date(year, month, d).weekday() == weekday]
    return dt.date(year, month, days[-1] if nth == -1 else days[nth - 1])


def occurrence(rule, anchor, k):
    """The k-th date of a series (k=0 is its anchor's own period)."""
    unit, n = rule['unit'], rule.get('n', 1)
    if unit == 'day':
        return anchor + dt.timedelta(days=k * n)
    if unit == 'week':
        return anchor + dt.timedelta(weeks=k * n)
    if unit == 'year':
        try:
            return anchor.replace(year=anchor.year + k)
        except ValueError:  # Feb 29 in a year without it
            return dt.date(anchor.year + k, 2, 28)
    first = _add_months(anchor.replace(day=1), k * n, 1)
    if rule.get('nth') is not None:
        return _nth_weekday(first.year, first.month, anchor.weekday(), rule['nth'])
    return _add_months(anchor, k * n, anchor.day)


def next_after(rule, anchor, after):
    """The series' first date after `after` (never before its anchor)."""
    if rule['unit'] == 'weekday':
        day = max(after + dt.timedelta(days=1), anchor)
        while day.weekday() > 4:
            day += dt.timedelta(days=1)
        return day
    span = {'day': 1, 'week': 7, 'month': 28, 'year': 365}[rule['unit']] * rule.get('n', 1)
    k = max(0, (after - anchor).days // span - 2)
    while True:
        day = occurrence(rule, anchor, k)
        if day > after and day >= anchor:
            return day
        k += 1


def missed(rule, anchor, due, today, cap=99):
    """How many of the series' dates passed (up to today) while the occurrence due on `due` stayed open."""
    count, day = 0, due
    while count < cap:
        day = next_after(rule, anchor, day)
        if day > today:
            return count
        count += 1
    return count


def anchor_for(rule, today, weekday=None, monthday=None, nth=None):
    """The first date on or after today that fits what the words gave: a weekday, a day of the month, or a month's
    first..last weekday."""
    day = today
    for _ in range(400):
        if weekday is not None and day.weekday() != weekday:
            pass
        elif monthday is not None and day.day != min(monthday, calendar.monthrange(day.year, day.month)[1]):
            pass
        elif nth is not None and _nth_weekday(day.year, day.month, day.weekday(), nth) != day:
            pass
        elif rule['unit'] == 'weekday' and day.weekday() > 4:
            pass
        else:
            return day
        day += dt.timedelta(days=1)
    return today


WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
ORDINALS = {1: 'first', 2: 'second', 3: 'third', 4: 'fourth', -1: 'last'}


def describe(rule, anchor):
    """The rhythm in plain English, for prompts and logs (the dashboard words it in the owner's language itself)."""
    unit, n = rule['unit'], rule.get('n', 1)
    if unit == 'weekday':
        return 'every weekday'
    if unit == 'day':
        return 'daily' if n == 1 else f'every {n} days'
    if unit == 'week':
        return (f'weekly on {WEEKDAYS[anchor.weekday()]}' if n == 1 else f'every {n} weeks on {WEEKDAYS[anchor.weekday()]}')
    if unit == 'year':
        return f'yearly on {anchor.strftime("%B")} {anchor.day}'
    every = 'monthly' if n == 1 else f'every {n} months'
    if rule.get('nth') is not None:
        return f'{every} on the {ORDINALS[rule["nth"]]} {WEEKDAYS[anchor.weekday()]}'
    return f'{every} on day {anchor.day}'


# --- plain words ------------------------------------------------------------------------------------------------------

_DAY = {'monday': 0, 'mon': 0, 'tuesday': 1, 'tue': 1, 'tues': 1, 'wednesday': 2, 'wed': 2, 'thursday': 3, 'thu': 3, 'thurs': 3,
        'friday': 4, 'fri': 4, 'saturday': 5, 'sat': 5, 'sunday': 6, 'sun': 6}
_DAYS = r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tues?|wed|thu(?:rs)?|fri|sat|sun)'
_NUM = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12,
        'other': 2}
_NTH = {'first': 1, '1st': 1, 'second': 2, '2nd': 2, 'third': 3, '3rd': 3, 'fourth': 4, '4th': 4, 'last': -1}
_NTHS = r'(first|1st|second|2nd|third|3rd|fourth|4th|last)'
_UNIT = {'day': 'day', 'week': 'week', 'month': 'month', 'year': 'year'}
# The other languages the app speaks: their "every day/week/month/year" and "every weekday"
_WORLD = [
    (r'\b(?:elke|iedere) werkdag\b|\bchaque jour ouvr[ée]\b|\bjeden werktag\b|\bcada d[íi]a laborable\b|\bogni giorno feriale\b|\btodo dia [úu]til\b', 'weekday'),
    (r'\b(?:elke|iedere) dag\b|\bdagelijks\b|\bchaque jour\b|\btous les jours\b|\bjeden tag\b|\bt[äa]glich\b|\bcada d[íi]a\b|\btodos los d[íi]as\b|\bogni giorno\b|\btutti i giorni\b|\btodos os dias\b|\btodo dia\b|\bdiariamente\b', 'day'),
    (r'\b(?:elke|iedere) week\b|\bwekelijks\b|\bchaque semaine\b|\btoutes les semaines\b|\bjede woche\b|\bw[öo]chentlich\b|\bcada semana\b|\btodas las semanas\b|\bogni settimana\b|\btodas as semanas\b|\btoda semana\b|\bsemanalmente\b', 'week'),
    (r'\b(?:elke|iedere) maand\b|\bmaandelijks\b|\bchaque mois\b|\btous les mois\b|\bjeden monat\b|\bmonatlich\b|\bcada mes\b|\btodos los meses\b|\bogni mese\b|\btodos os meses\b|\btodo m[êe]s\b|\bmensalmente\b|\bmensualmente\b', 'month'),
    (r'\b(?:elk|ieder) jaar\b|\bjaarlijks\b|\bchaque ann[ée]e\b|\btous les ans\b|\bjedes jahr\b|\bj[äa]hrlich\b|\bcada a[ñn]o\b|\btodos los a[ñn]os\b|\bogni anno\b|\btodos os anos\b|\btodo ano\b|\banualmente\b', 'year'),
]


def parse(text, today):
    """A rhythm in the owner's words ("every first Monday of the month do payroll", "Water the plants every 3 days",
    "Board update monthly"), or None. {'rule', 'anchor' (date), 'rest' (the words without the rhythm)}. Only clear
    rhythms count: "every ..." anywhere, or daily/weekly/monthly/yearly at the end (not "the weekly report")."""
    s = str(text or '')
    low = s.lower()
    found = None  # (start, end, rule, anchor hints)
    tries = [
        (r'\b(?:every|each) (?:week ?day|working day|business day)s?\b|\bon weekdays\b', lambda m: ({'unit': 'weekday', 'n': 1}, {})),
        (r'\b(?:on )?(?:every|each|the) ' + _NTHS + ' ' + _DAYS + r'(?:\s+(?:of|in)\s+(?:the|each|every)\s+month)?\b',
         lambda m: ({'unit': 'month', 'n': 1, 'nth': _NTH[m.group(1)]}, {'weekday': _DAY[m.group(2)], 'nth': _NTH[m.group(1)]})
         if m.group(0).strip().startswith(('every', 'each')) or re.search(r'month\b', m.group(0)) else None),
        (r'\bevery (\d{1,2}|' + '|'.join(_NUM) + r') (day|week|month|year)s?\b(?: on ' + _DAYS + r')?',
         lambda m: ({'unit': m.group(2), 'n': int(m.group(1)) if m.group(1).isdigit() else _NUM[m.group(1)]},
                    {'weekday': _DAY[m.group(3)]} if m.group(3) and m.group(2) == 'week' else {})),
        (r'\b(?:every|each) (\d{1,2})(?:st|nd|rd|th)(?: (?:day )?of (?:the|each|every) month)?\b|\bon the (\d{1,2})(?:st|nd|rd|th) of (?:each|every) month\b',
         lambda m: ({'unit': 'month', 'n': 1}, {'monthday': int(m.group(1) or m.group(2))}) if 1 <= int(m.group(1) or m.group(2)) <= 31 else None),
        (r'\b(?:every|each) ' + _DAYS + r's?\b|\bon ' + _DAYS + r's\b',
         lambda m: ({'unit': 'week', 'n': 1}, {'weekday': _DAY[m.group(1) or m.group(2)]})),
        (r'\b(?:every|each) (day|week|month|year)\b', lambda m: ({'unit': _UNIT[m.group(1)], 'n': 1}, {})),
        (r'\bevery (?:morning|evening|night)\b', lambda m: ({'unit': 'day', 'n': 1}, {})),
        (r'\b(?:on a |on an )?(daily|weekly|monthly|yearly|annually|annual) basis\b|[\s,(-]+(daily|weekly|monthly|yearly|annually)\W*$',
         lambda m: ({'unit': {'daily': 'day', 'weekly': 'week', 'monthly': 'month', 'yearly': 'year', 'annually': 'year', 'annual': 'year'}[m.group(1) or m.group(2)], 'n': 1}, {})),
        *[(pattern, (lambda u: lambda m: ({'unit': u, 'n': 1}, {}))(unit)) for pattern, unit in _WORLD],
    ]
    for pattern, read in tries:
        m = re.search(pattern, low)
        if m:
            got = read(m)
            if got:
                found = (m.start(), m.end(), *got)
                break
    if not found:
        return None
    start, end, rule, hints = found
    rule = clean_rule(rule)
    anchor = anchor_for(rule, today, **hints)
    rest = (s[:start] + ' ' + s[end:])
    rest = re.sub(r'\s+([,.;:!?])', r'\1', ' '.join(rest.split())).strip(' ,;:-')
    rest = re.sub(r'^(?:and|to|please|remind me to)\s+', '', rest, flags=re.I)
    rest = rest[:1].upper() + rest[1:]
    return {'rule': rule, 'anchor': anchor, 'rest': rest}


# --- series ------------------------------------------------------------------------------------------------------------

def series_of(db, suggestion_id):
    """The series a to-do belongs to (its occurrence row joined to the series), or None."""
    return db.execute('SELECT s.*,c.due card_due FROM recurring_cards c JOIN recurring_series s ON s.id=c.series_id WHERE c.suggestion_id=?',
                      (str(suggestion_id or ''),)).fetchone()


def start(db, card, rule, anchor, text, stamp, work=False):
    """A to-do starts repeating: a new series with this to-do as its first, open occurrence on `anchor`. A to-do that
    was in a stopped series starts a new one."""
    sid = uuid.uuid4().hex[:16]
    accounts = json.loads(card['account_ids'] or '[]')
    db.execute('INSERT INTO recurring_series(id,rule,anchor,text,account_id,work,project,current_id,due,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
               (sid, json.dumps(rule), anchor.isoformat(), text, accounts[0] if accounts else '', 1 if work else 0, card['project'],
                card['id'], anchor.isoformat(), stamp, stamp))
    db.execute('INSERT OR REPLACE INTO recurring_cards(suggestion_id,series_id,due,created_at) VALUES(?,?,?,?)', (card['id'], sid, anchor.isoformat(), stamp))
    return sid


def change(db, series, rule, stamp, today):
    """A new rhythm for a series, from the open occurrence's date on (or, between occurrences, from today)."""
    rule = clean_rule(rule)
    anchor = dt.date.fromisoformat(series['due'] or today.isoformat())
    if rule['unit'] == 'weekday' or rule.get('nth') is not None:  # the first fitting day from there
        anchor = anchor_for(rule, anchor, nth=rule.get('nth'))
    next_due = None if series['current_id'] else next_after(rule, anchor, max(anchor, today - dt.timedelta(days=1))).isoformat()
    db.execute('UPDATE recurring_series SET rule=?,anchor=?,next_due=?,updated_at=? WHERE id=?',
               (json.dumps(rule), anchor.isoformat(), next_due, stamp, series['id']))


def stop(db, series_id, stamp):
    """Stop repeating: the open occurrence stays an ordinary to-do; no next one comes."""
    db.execute('UPDATE recurring_series SET stopped_at=?,next_due=NULL,updated_at=? WHERE id=? AND stopped_at IS NULL', (stamp, stamp, series_id))


def tick(db, today, stamp):
    """Move every running series on: an occurrence that was closed gives its next date; a date that came gives the
    series' next to-do, to make (returned as the series rows due one now; the caller makes each with make_next)."""
    due_now = []
    for s in db.execute('SELECT * FROM recurring_series WHERE stopped_at IS NULL').fetchall():
        rule, anchor = json.loads(s['rule']), dt.date.fromisoformat(s['anchor'])
        if s['current_id']:
            card = db.execute('SELECT status FROM suggestions WHERE id=?', (s['current_id'],)).fetchone()
            if card and card['status'] not in CLOSED:
                continue
            last_due = dt.date.fromisoformat(s['due'] or s['anchor'])
            # the next date after this one, never one already gone: a late one doesn't bring the dates it missed
            nxt = next_after(rule, anchor, max(last_due, today - dt.timedelta(days=1)))
            db.execute('UPDATE recurring_series SET last_id=current_id,last_done=?,current_id=NULL,next_due=?,updated_at=? WHERE id=?',
                       (stamp, nxt.isoformat(), stamp, s['id']))
            s = db.execute('SELECT * FROM recurring_series WHERE id=?', (s['id'],)).fetchone()
        if s['next_due'] and s['next_due'] <= today.isoformat():
            due_now.append(dict(s))
    return due_now


def made(db, series_id, suggestion_id, due, stamp):
    """The series' next occurrence was made as this to-do."""
    db.execute("UPDATE recurring_series SET current_id=?,due=?,next_due=NULL,updated_at=? WHERE id=?", (suggestion_id, due, stamp, series_id))
    db.execute('INSERT OR REPLACE INTO recurring_cards(suggestion_id,series_id,due,created_at) VALUES(?,?,?,?)', (suggestion_id, series_id, due, stamp))


def annotate(db, cards, today):
    """card['repeats'] on each to-do that is a running series' open occurrence: {'rule', 'anchor', 'due', 'missed',
    'next'} for its one line ("Repeats monthly on the first Monday · missed 1") and More > Repeat."""
    if not cards:
        return
    try:
        rows = {r['current_id']: r for r in db.execute('SELECT * FROM recurring_series WHERE stopped_at IS NULL AND current_id IS NOT NULL')}
    except Exception:  # an older database before ensure ran: no series yet
        return
    for card in cards:
        s = rows.get(card['id'])
        if not s:
            continue
        rule, anchor = json.loads(s['rule']), dt.date.fromisoformat(s['anchor'])
        due = dt.date.fromisoformat(s['due'] or s['anchor'])
        card['repeats'] = {'series': s['id'], 'rule': rule, 'anchor': s['anchor'], 'due': due.isoformat(),
                           'missed': missed(rule, anchor, due, today), 'next': next_after(rule, anchor, max(due, today)).isoformat()}


def prep_lines(db, suggestion_id, limit=2500):
    """For an occurrence's preparation: that it repeats, and how the previous one went (its result and the owner's
    notes on it), so this month's payroll starts from last month's. '' when it isn't in a series or is the first."""
    s = series_of(db, suggestion_id)
    if not s:
        return ''
    rule, anchor = json.loads(s['rule']), dt.date.fromisoformat(s['anchor'])
    line = f"\n\nThis to-do repeats ({describe(rule, anchor)}); this one is for {s['card_due']}."
    prev = db.execute('SELECT c.due,g.* FROM recurring_cards c JOIN suggestions g ON g.id=c.suggestion_id WHERE c.series_id=? AND c.due<? '
                      'ORDER BY c.due DESC LIMIT 1', (s['id'], s['card_due'])).fetchone()
    if not prev:
        return line + ' It is the first one.'
    state = {'completed': 'done', 'rejected': 'not needed or skipped'}.get(prev['status'], 'still open')
    notes = [r['feedback'] for r in db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND trim(feedback)<>'' AND source IN ('dashboard','telegram') "
                                               'ORDER BY created_at DESC LIMIT 5', (prev['id'],))]
    out = (line + f" The previous one ({prev['due']}, {state}) was \"{prev['title']}\". Start from how it went: reuse what worked, "
           'update what changed (dates, amounts, names), and say what differs from last time.\nIts result:\n<<<\n'
           + str(prev['body'] or '').strip()[:limit] + '\n>>>')
    if notes:
        out += '\nThe owner\'s notes on it, newest first:\n' + '\n'.join('- ' + ' '.join(n.split())[:300] for n in notes)
    return out


# --- offers ------------------------------------------------------------------------------------------------------------

_MONTHS = r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\b'


def title_key(title):
    """A to-do's title without its dates and numbers: the same task in different months reads the same."""
    t = re.sub(_MONTHS, ' ', str(title or '').lower())
    t = re.sub(r'\b(?:q[1-4]|week|wk|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', ' ', t)
    t = re.sub(r'[^a-zÀ-ɏ]+', ' ', t)
    return ' '.join(t.split())


def rhythm_of(days):
    """A regular rhythm in these dates (oldest first), or None: weekly or monthly, at least three times."""
    if len(days) < 3:
        return None
    gaps = [(b - a).days for a, b in zip(days, days[1:])]
    if all(6 <= g <= 8 for g in gaps):
        return {'unit': 'week', 'n': 1}
    if all(13 <= g <= 15 for g in gaps):
        return {'unit': 'week', 'n': 2}
    if all(27 <= g <= 33 for g in gaps):
        return {'unit': 'month', 'n': 1}
    return None


def find_offers(db, today, stamp, tz):
    """New "Make this a recurring to-do?" offers, each asked once (recurring_offers keeps every key it asked):
    - a learned note that says the owner does something on a rhythm (facts of kind commitment, else any note);
    - the same to-do closed as done on a weekly or monthly rhythm, three times or more.
    Never for something a running series already covers."""
    asked = {r['key'] for r in db.execute('SELECT key FROM recurring_offers')}
    running = {title_key(r['text']) for r in db.execute('SELECT text FROM recurring_series WHERE stopped_at IS NULL')}
    added = 0
    columns = {r[1] for r in db.execute('PRAGMA table_info(facts)')}
    # Learned notes only (kind fact, not a draft rule), still holding; their sort (fact_kind) says which are commitments
    where = 'removed_at IS NULL' + (' AND merged_into IS NULL' if 'merged_into' in columns else '') + (" AND kind='fact'" if 'kind' in columns else '')
    if 'valid_until' in columns:
        where += f" AND (valid_until IS NULL OR valid_until>='{today.isoformat()}')"
    rows = db.execute(f'SELECT id,text{",fact_kind" if "fact_kind" in columns else ""} FROM facts WHERE {where} ORDER BY id DESC LIMIT 400').fetchall()
    commitments = [r for r in rows if 'fact_kind' in columns and r['fact_kind'] == 'commitment']
    for r in commitments or rows:
        key = 'fact:' + str(r['id'])
        if key in asked:
            continue
        got = parse(r['text'], today)
        if not got or len(got['rest']) < 4 or title_key(got['rest']) in running:
            continue
        db.execute('INSERT OR IGNORE INTO recurring_offers(key,source,title,text,rule,anchor,created_at) VALUES(?,?,?,?,?,?,?)',
                   (key, 'fact', got['rest'][:120], got['rest'], json.dumps(got['rule']), got['anchor'].isoformat(), stamp))
        added += 1
    since = (today - dt.timedelta(days=OFFER_DAYS)).isoformat()
    groups = {}
    for r in db.execute("SELECT id,title,status,created_at FROM suggestions WHERE created_at>=? AND status IN ('completed','pending','accepted','prepared','instructions','snoozed') "
                        'ORDER BY created_at', (since,)):
        groups.setdefault(title_key(r['title']), []).append(r)
    for key_text, cards in groups.items():
        if len(key_text) < 4 or key_text in running or 'title:' + key_text in asked:
            continue
        done = [c for c in cards if c['status'] == 'completed']
        days = sorted({dt.datetime.fromisoformat(c['created_at']).astimezone(tz).date() for c in done})
        rule = rhythm_of(days)
        if not rule:
            continue
        open_card = next((c for c in reversed(cards) if c['status'] != 'completed'), None)
        last = days[-1]
        anchor = next_after(rule, last, max(last, today - dt.timedelta(days=1)))
        if rule['unit'] == 'month' and last.day > 28:
            continue  # "the 31st" may be a month end; better not to guess
        db.execute('INSERT OR IGNORE INTO recurring_offers(key,source,title,text,rule,anchor,card_id,created_at) VALUES(?,?,?,?,?,?,?,?)',
                   ('title:' + key_text, 'rhythm', cards[-1]['title'][:120], cards[-1]['title'], json.dumps(rule), anchor.isoformat(),
                    open_card['id'] if open_card else None, stamp))
        added += 1
    return added


def answer_offer(db, key, yes, stamp):
    """The owner's Yes or No thanks on an open offer (never asked again either way): the offer's row."""
    offer = db.execute("SELECT * FROM recurring_offers WHERE key=? AND status='open'", (key,)).fetchone()
    if not offer:
        raise ValueError('That suggestion is gone')
    db.execute('UPDATE recurring_offers SET status=?,decided_at=? WHERE key=?', ('accepted' if yes else 'declined', stamp, key))
    return offer


def offer_view(db):
    """The one open offer the dashboard shows (oldest first), or None."""
    try:
        r = db.execute("SELECT * FROM recurring_offers WHERE status='open' ORDER BY created_at,key LIMIT 1").fetchone()
    except Exception:
        return None
    if not r:
        return None
    card = r['card_id'] and db.execute('SELECT status FROM suggestions WHERE id=?', (r['card_id'],)).fetchone()
    return {'key': r['key'], 'source': r['source'], 'title': r['title'], 'rule': json.loads(r['rule']), 'anchor': r['anchor'],
            'card_id': r['card_id'] if card and card['status'] not in CLOSED else None}


# "stop repeating", "don't repeat this any more": the to-do chat's way to stop
STOP = re.compile(r"\b(?:stop|no longer|don'?t|do not|never)\b.{0,20}\b(?:repeat|repeating|recur|recurring)\b|\bonly (?:this )?once\b", re.I)

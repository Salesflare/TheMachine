"""Here's what I've learned (docs/help/what-ive-learned.md): at the end of the first look, a short summary of the owner's work
that they can glance at and correct, on the To-dos page next to the first look's ending. Work facts only:

- how they write: two or three lines of their main voice (Email, else Everywhere), as How you write keeps it;
- the people who matter most right now (at most PEOPLE): Work people they write with both ways and only on Work
  accounts, closest first, each with what they're working on together, from the Graph (their strongest open project
  that isn't just their company's name) or else the subject of their newest thread; someone with neither is left out,
  never given a guessed title or role;
- their usual hours: when they send their own work mail, from their own sent messages (HOURS_DAYS back), only with a
  few weeks of it and a clear pattern.

Nothing personal: no Personal people or accounts, no family, home, health or money, and no roles inferred from
messages. It reads only what the first look, the Graph and the voice study already wrote: no model call. Quality or
nothing: a part without enough signal is left out, and with no part left there is no summary.

Each item is correctable in one tap (Not right), and every correction is kept like the learning loop's own changes
(learning_changes), so it shows under Learning, Changes, with Undo:
- a line of how they write, reworded or removed: the voice block changes (the owner's own words from then on);
- what they work on with someone: a fact about that person (Learning, Facts; their Graph page);
- their hours: a fact in their words;
- someone who isn't one of the people who matter, or hours that aren't right at all: left off (kind 'learned').

Names and lines are for the owner alone: nothing of it goes into a report or leaves the Machine."""
from __future__ import annotations

import datetime as dt
import json
import re
import secrets

import learning_loop

SCHEMA = 'CREATE TABLE IF NOT EXISTS learned_fixes(key TEXT PRIMARY KEY,state TEXT NOT NULL,text TEXT,at TEXT NOT NULL)'
PEOPLE = 6            # at most this many people
ACTIVE_DAYS = 30      # someone who matters right now: in touch within this many days
VOICE_SHOWN = 3       # lines of how they write
VOICE_ORDER = ('Email', 'All')  # the main voice: email first, else everywhere, else the first channel there is
HOURS_DAYS = 28       # own sent mail read for their hours, this far back
HOURS_MIN, HOURS_MIN_DAYS, HOURS_MIN_WEEKS = 30, 8, 2  # fewer sent messages, days, or weeks between the first and last, say too little
HOURS_MIN_SPAN, HOURS_MAX_SPAN = 120, 14 * 60  # minutes: narrower is a burst, not a working day; wider is no pattern at all
TOPIC_MAX = 80
WHY = 'Corrected after the first look.'  # in every catalog: Learning, Changes reads it in the owner's language
MAIL_KINDS = ('gmail.message', 'outlook.message', 'ms_graph.message')
SUBJECT_PREFIX = re.compile(r'^(?:\s*(?:re|fwd?|fw|aw|wg|tr|rv|r|sv|vs|antw)\s*(?:\[\d+\])?\s*:\s*)+', re.I)
TAGS = re.compile(r'^\s*(?:\[[^\]]{1,40}\]\s*)+')


def ensure(db):
    db.execute(SCHEMA)
    learning_loop.ensure(db)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def _table(db, name):
    return bool(db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone())


def _info(row):
    try:
        return json.loads(row['info'] or '{}')
    except (TypeError, ValueError):
        return {}


def subject(title):
    """A thread's subject as a topic: Re:, Fwd: and [tags] off, spaces tidied, None when nothing is left."""
    text = ' '.join(TAGS.sub('', SUBJECT_PREFIX.sub('', str(title or ''))).split())
    if len(text) < 3 or not re.search(r'[^\W\d_]{2}', text):
        return None
    return text if len(text) <= TOPIC_MAX else text[:TOPIC_MAX - 1].rstrip() + '…'


def removed(db):
    """The items the owner left off (Not right, Remove): their keys."""
    return {r[0] for r in db.execute("SELECT key FROM learned_fixes WHERE state='removed'")}


def owner_facts(db, prefix):
    """The live facts the owner wrote here, newest first: [(id, text)] (decision_id 'learned:<prefix>...')."""
    return [(r[0], r[1]) for r in db.execute("SELECT id,text FROM facts WHERE removed_at IS NULL AND decision_id LIKE ? ORDER BY created_at DESC,id DESC",
                                             ('learned:' + prefix + '%',))]


def writing(db):
    """How the owner writes: {'channel', 'lines'} from their main voice, or None before the voice study wrote one."""
    if not _table(db, 'voices'):
        return None
    rows = {r['channel']: r for r in db.execute('SELECT channel,text FROM voices')}
    channel = next((c for c in VOICE_ORDER if c in rows), None) or (sorted(rows)[0] if rows else None)
    if not channel:
        return None
    lines = [line.strip() for line in str(rows[channel]['text'] or '').split('\n') if line.strip()][:VOICE_SHOWN]
    return {'channel': channel, 'lines': lines} if lines else None


def _person_topic(db, node_id, ids, name, accounts_side, since, own=()):
    """What the owner and this person are working on: the owner's own correction, else their strongest open project,
    else the subject of their newest email thread on a Work account. (topic, source) or (None, None)."""
    marks = ','.join('?' for _ in ids)
    for fact_id, text in db.execute(f"SELECT f.id,f.text FROM facts f JOIN fact_about a ON a.fact_id=f.id WHERE f.removed_at IS NULL AND a.removed_at IS NULL "
                                    f"AND f.decision_id LIKE 'learned:person:%' AND a.node_id IN ({marks}) ORDER BY f.created_at DESC,f.id DESC LIMIT 1", ids):
        topic = text[len(name) + 2:] if text.startswith(name + ': ') else text
        return topic, 'you'
    companies = [c for c in {_letters(part) for i in ids for part in str(i).partition('@')[2].split('.')[:-1]} | {_letters(o) for o in own} if c]
    for row in db.execute("SELECT p.name FROM graph_links l JOIN graph_nodes p ON p.id=(CASE WHEN l.a=? THEN l.b ELSE l.a END) AND p.kind='project' "
                          "WHERE (l.a=? OR l.b=?) AND l.kind='project' AND json_extract(p.info,'$.closed_at') IS NULL AND p.strength>=0.3 "
                          "ORDER BY l.strength DESC LIMIT 3", (node_id, node_id, node_id)):
        if _says_something(row[0], companies):  # "Willowtick" for someone at willowtick.example says nothing new
            return row[0], 'project'
    for r in db.execute(f"SELECT e.title,e.account_id FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id=? AND g.direct=1 AND e.deleted=0 "
                        f"AND e.kind IN ({','.join('?' for _ in MAIL_KINDS)}) AND e.occurred_at>=? ORDER BY e.occurred_at DESC LIMIT 12",
                        (node_id, *MAIL_KINDS, since)):
        if accounts_side.get(r['account_id']) == 'personal':
            continue
        topic = subject(r['title'])
        if _says_something(topic, companies):  # nor does "Larkfield and Lumen Labs", an introduction
            return topic, 'thread'
    return None, None


def _letters(text):
    return re.sub(r'[\W_]+', '', str(text or '').lower())


def _says_something(topic, companies):
    """Whether a topic has a word of its own beyond the companies' names (theirs and the owner's) and short joining words."""
    words = [_letters(w) for w in str(topic or '').split()]
    return any(len(w) >= 4 and not any(w in c for c in companies) for w in words) or any(any(ch.isdigit() for ch in w) for w in words)


def personal_relation(role):
    import graph
    return bool(role) and graph.personal_relation(role)


def _personal_contact(db, node_id, accounts_side, since):
    """Whether the owner was in touch with this person on a Personal account lately (WhatsApp, a home mailbox)."""
    personal = [a for a, side in accounts_side.items() if side == 'personal']
    if not personal:
        return False
    return bool(db.execute(f"SELECT 1 FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.node_id=? AND e.occurred_at>=? "
                           f"AND e.account_id IN ({','.join('?' for _ in personal)}) LIMIT 1", (node_id, since, *personal)).fetchone())


def people(db, accounts_side, current, limit=PEOPLE, own=()):
    """The people who matter most right now: [{id, name, topic, from}] (from: 'project', 'thread' or 'you'), closest
    first. Work people only (their Type), written with both ways, in touch within ACTIVE_DAYS, never the owner or an
    address; each with what they work on together, or not at all."""
    if not _table(db, 'graph_nodes'):
        return []
    since = (current - dt.timedelta(days=ACTIVE_DAYS)).isoformat()
    gone = removed(db)
    out = []
    for row in db.execute("SELECT id,name,info,last_at FROM graph_nodes WHERE kind='person' AND quiet=0 ORDER BY strength DESC LIMIT 80"):
        info = _info(row)
        name = ' '.join(str(row['name'] or '').split())
        if (info.get('side') != 'work' or info.get('seen_only') or not info.get('wrote') or not info.get('heard') or not name or '@' in name
                or not re.search(r'[^\W\d_]{2}', name) or str(row['last_at'] or '') < since[:10] or 'person:' + row['id'] in gone):
            continue
        if personal_relation(info.get('role')) or _personal_contact(db, row['id'], accounts_side, since):
            continue  # family or a friend, by the owner's own word, or someone they also reach on a Personal account
        ids = list(dict.fromkeys([row['id'], *(info.get('identifiers') or [])]))
        topic, source = _person_topic(db, row['id'], ids, name, accounts_side, since, own)
        if topic:
            out.append({'id': row['id'], 'name': name, 'topic': topic, 'from': source})
        if len(out) >= limit:
            break
    return out


def _round(minutes, up):
    step = 30
    return min(24 * 60 - step, (minutes + (step - 1 if up else 0)) // step * step)


def hours(db, accounts_side, tz, current):
    """Their usual hours, from the times they sent their own work mail: {'days': ISO weekdays, 'start', 'end' (HH:MM,
    their time zone), 'messages'}, or the owner's own words for them ({'text'}), or None with too little to go on."""
    if 'hours' in removed(db):
        return None
    fixed = owner_facts(db, 'hours:')
    if fixed:
        return {'text': fixed[0][1], 'from': 'you'}
    work = [a for a, side in accounts_side.items() if side != 'personal']
    if not work:
        return None
    since = (current - dt.timedelta(days=HOURS_DAYS)).isoformat()
    marks = ','.join('?' for _ in work)
    times = []
    for (at,) in db.execute(f"SELECT occurred_at FROM events WHERE deleted=0 AND account_id IN ({marks}) AND occurred_at>=? AND occurred_at<=? AND ("
                            "(kind='gmail.message' AND EXISTS(SELECT 1 FROM json_each(json_extract(events.metadata,'$.labels')) WHERE value='SENT')) OR "
                            "(kind IN ('outlook.message','ms_graph.message') AND json_extract(metadata,'$.from_me')=1)) ORDER BY occurred_at DESC LIMIT 400",
                            (*work, since, current.isoformat())):
        try:
            local = dt.datetime.fromisoformat(at).astimezone(tz)
        except (TypeError, ValueError):
            continue
        times.append(local)
    days_seen = {t.date() for t in times}
    if len(times) < HOURS_MIN or len(days_seen) < HOURS_MIN_DAYS:
        return None
    weeks = ((max(days_seen) - min(days_seen)).days + 1) / 7
    if weeks < HOURS_MIN_WEEKS:
        return None
    per_day, sent = {}, {}
    for t in times:
        per_day.setdefault(t.isoweekday(), set()).add(t.date())
        sent[t.isoweekday()] = sent.get(t.isoweekday(), 0) + 1
    # A usual day: on at least half of the weeks seen, and with at least a quarter of the busiest day's mail, so a
    # few weekend emails don't make the weekend working days
    days = sorted(d for d, dates in per_day.items() if len(dates) >= max(2, round(weeks / 2)) and sent[d] * 4 >= max(sent.values()))
    minutes = sorted(t.hour * 60 + t.minute for t in times if t.isoweekday() in days)
    if len(minutes) < HOURS_MIN:
        return None
    low, high = minutes[len(minutes) // 10], minutes[min(len(minutes) - 1, (len(minutes) * 9) // 10)]
    start, end = _round(low, False), _round(high, True)
    if not HOURS_MIN_SPAN <= end - start <= HOURS_MAX_SPAN:
        return None
    return {'days': days, 'start': f'{start // 60:02d}:{start % 60:02d}', 'end': f'{end // 60:02d}:{end % 60:02d}', 'messages': len(times)}


def summary(db, accounts_side, tz, current, own=()):
    """{'writing', 'people', 'hours'} for the dashboard, each left out without enough signal; None when nothing is.
    own: the owner's company names (their Work accounts' boundary), never a topic by themselves."""
    ensure(db)
    out = {'writing': writing(db), 'people': people(db, accounts_side, current, own=own), 'hours': hours(db, accounts_side, tz, current)}
    out = {k: v for k, v in out.items() if v}
    return out or None


# Corrections. Each is kept in learning_changes with what it replaced, so Learning, Changes shows it with Undo.

def _token(kind):
    return f'learned:{kind}:{secrets.token_hex(4)}'


def _clean(text, limit):
    text = ' '.join(str(text or '').split())
    if len(text) > limit:
        raise ValueError(f'Keep it short: up to {limit} characters')
    return text


def fix_voice(db, channel, line, text):
    """A line of how they write, reworded (text) or removed (text ''): the voice block changes, as the owner's own
    words (the learning loop never changes it after). line: the line as shown, so a block that changed since is
    never changed in the wrong place."""
    from machine.prompts.profile import VOICE_CHARS
    text = _clean(text, 200)
    row = db.execute('SELECT channel,text,source,ref,updated_at FROM voices WHERE channel=?', (str(channel),)).fetchone()
    lines = [x.strip() for x in str(row['text'] or '').split('\n')] if row else []
    target = ' '.join(str(line or '').split())
    at = next((i for i, x in enumerate(lines) if ' '.join(x.split()) == target), None)
    if at is None:
        raise ValueError('That line changed since. Reload to see how it reads now')
    if text:
        lines[at] = text
    else:
        del lines[at]
    block = '\n'.join(x for x in lines if x)
    if len(block) > VOICE_CHARS:
        raise ValueError('That makes the block too long. Edit it under How you write instead')
    run = _token('voice')
    before = json.dumps(dict(row))
    if block:
        db.execute("UPDATE voices SET text=?,source='owner',ref=?,updated_at=? WHERE channel=?", (block, run, now(), row['channel']))
    else:
        db.execute('DELETE FROM voices WHERE channel=?', (row['channel'],))
    db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'voice',?,?)", (now(), f"{row['channel']} voice: {block}" if block else f"Removed {row['channel']} voice", run))
    return learning_loop.record(db, run, 'voice', row['channel'], before, block, WHY)


def fix_person(db, node_id, topic):
    """What the owner and someone work on together, in the owner's words: a fact about them ("Name: topic")."""
    topic = _clean(topic, 160)
    if len(topic) < 2:
        raise ValueError('Say what you work on together, or tap Remove')
    row = db.execute("SELECT id,name,info FROM graph_nodes WHERE id=? AND kind='person'", (str(node_id),)).fetchone()
    if not row:
        raise ValueError('That person is not in your Graph any more')
    name = ' '.join(str(row['name'] or '').split())
    ids = list(dict.fromkeys([row['id'], *(_info(row).get('identifiers') or [])]))
    run = _token('person')
    marks = ','.join('?' for _ in ids)
    old = db.execute(f"SELECT f.id,f.text FROM facts f JOIN fact_about a ON a.fact_id=f.id WHERE f.removed_at IS NULL AND a.removed_at IS NULL "
                     f"AND f.decision_id LIKE 'learned:person:%' AND a.node_id IN ({marks}) ORDER BY f.created_at DESC LIMIT 1", ids).fetchone()
    text = f'{name}: {topic}'
    fact_id = db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES(?,?,NULL,?,'fact')", (text, run, now())).lastrowid
    db.execute("INSERT OR IGNORE INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'owner',?)", (fact_id, row['id'], now()))
    if old:
        db.execute('UPDATE facts SET removed_at=? WHERE id=?', (now(), old['id']))
    db.execute("DELETE FROM learned_fixes WHERE key=?", ('person:' + row['id'],))
    return learning_loop.record(db, run, 'fact', fact_id, json.dumps({'id': old['id'], 'text': old['text']}) if old else None, text, WHY)


def fix_hours(db, text):
    """Their hours in their own words: a fact."""
    text = _clean(text, 160)
    if len(text) < 5:
        raise ValueError('Say when you usually work, or tap Remove')
    run = _token('hours')
    old = owner_facts(db, 'hours:')
    fact_id = db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES(?,?,NULL,?,'fact')", (text, run, now())).lastrowid
    if old:
        db.execute('UPDATE facts SET removed_at=? WHERE id=?', (now(), old[0][0]))
    db.execute("DELETE FROM learned_fixes WHERE key='hours'")
    return learning_loop.record(db, run, 'fact', fact_id, json.dumps({'id': old[0][0], 'text': old[0][1]}) if old else None, text, WHY)


def leave_off(db, key, shown):
    """Someone who isn't one of the people who matter ('person:<node id>'), or hours that aren't right ('hours'): left
    off the summary for good, until undone. shown: what the summary said, for Changes."""
    if not (key == 'hours' or (key.startswith('person:') and db.execute("SELECT 1 FROM graph_nodes WHERE id=? AND kind='person'", (key[7:],)).fetchone())):
        raise ValueError('Unknown item')
    db.execute('INSERT OR REPLACE INTO learned_fixes(key,state,text,at) VALUES(?,?,?,?)', (key, 'removed', _clean(shown, 200)[:200], now()))
    return learning_loop.record(db, _token('off'), 'learned', key, None, _clean(shown, 200)[:200] or key, WHY)


def undo(db, row):
    """Undo of a 'learned' change (learning_loop.undo): the item is back on the summary."""
    db.execute("DELETE FROM learned_fixes WHERE key=? AND state='removed'", (row['target'],))
    return {}

"""Done checks (2026-11-27): a to-do waiting for a result that a public page shows reads that page itself before it comes
back to the owner (docs/help/cards.md, docs/sources.md).

A to-do's done when (outcomes.py) says what result counts as done. When that result is something a public web page
will show (a partner's article that lists the owner's product, a status page), the review or the to-do's run can add a
check: {"url", "expect"}, the page and one to three short words or names it must show. Kept sealed in
suggestions.done_check, with its state. Only an address its own messages or the owner's words give is kept (in_evidence),
so a check never reads a page someone made up.

First, right after a check is kept, the page is read once as it is (the baseline, also claimed): a page that already
shows the expected words (an old incident on a status page, the owner's name in a blog's sidebar) can't tell the result,
so that check never runs and the to-do comes back as before; one that couldn't be read in MAX_ATTEMPTS reads neither.
Only a check whose baseline didn't show them reads the page again later.

When the to-do's time to chase comes (outcome until, the same time return_waiting brings it back), the check goes
first, once a claim is written (claim): one plain read of the page as a polite reader (the App's step, through
connectors/web_page.read: robots.txt, public addresses only, size and time limits). Then (settle):

- met: the page shows every expected word. Then it is checked against what was agreed (result_checks.py: the price,
  the description, an approval step, the owner's half of an exchange) and closes by itself only when it matches, once
  for that version of the page;
- not met: it comes back as before (return_waiting), with "Checked <page>: not there yet" in its chat. When its deadline
  is still ahead, it reads the page once more the morning after the deadline first;
- unknown (the page couldn't be read): never a close. Read again after RETRY, at most MAX_ATTEMPTS reads; then it comes
  back as before with "Couldn't open <page>".

A check only reads. It never sends, drafts or changes anything outside the Machine; the nudge stays the owner's tap.
A claim older than LEASE is taken again (a crash mid-read), and a result counts only for the claim it was read for, on a
to-do that still waits the same way (settle): a newer message, a snooze, the owner's own step or a close comes first.
return_waiting waits for a check at most HOLD past its time, so a to-do always comes back. A new wait (a newer message,
a send after Undo) starts the check afresh (its until is the check's episode)."""
import datetime as dt
import hashlib
import json
import re
import uuid

import i18n
from connectors import web_page
from machine import todo_states
from machine.text import encoded
from machine.store import outcomes
from timeutil import local_tz

KIND = 'page'
EXPECT_MAX = 3      # words or names a page must show, each EXPECT_LEN characters at most
EXPECT_LEN = 80
MAX_ATTEMPTS = 3    # reads of one page for one wait (a recheck after the deadline adds one)
LEASE = dt.timedelta(minutes=15)  # a claim older than this is taken again
RETRY = dt.timedelta(hours=1)     # a page that couldn't be read is read again after this
HOLD = dt.timedelta(hours=6)      # return_waiting waits for a check at most this long past its time
PREFIX = 'done-check:'            # its chat lines (decisions), shown by card_chat
VERIFIED = outcomes.VERIFIED       # the close a page check made (its decision id)
URLS = re.compile(r'(?i)\b(?:https?://)?(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s"\'<>()\[\]]*)?')


def _load(text):
    try:
        found = json.loads(text or 'null')
    except (TypeError, ValueError):
        return None
    return found if isinstance(found, dict) and found.get('kind') == KIND and found.get('url') else None


def _address(text):
    try:
        return web_page.address(str(text or '').rstrip('.,;:!?'))
    except ValueError:
        return None


def _same(a, b):
    return bool(a and b) and a.rstrip('/') == b.rstrip('/')


def in_evidence(url, texts):
    """The address as one of these texts gives it (with or without https://), never one made up."""
    return any(_same(url, _address(m.group(0))) for text in texts for m in URLS.finditer(text or ''))


def evidence_texts(db, suggestion_id):
    """What the to-do rests on: its messages, the owner's own words and their notes in its chat."""
    row = db.execute('SELECT event_ids,owner_words,body FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        return []
    try:
        ids = [int(i) for i in json.loads(row['event_ids'] or '[]')][:50]
    except (TypeError, ValueError):
        ids = []
    texts = [row['owner_words'] or '']
    texts += [f"{r['title'] or ''}\n{r['body'] or ''}" for r in db.execute(
        'SELECT title,body FROM events WHERE deleted=0 AND id IN (' + ','.join('?' * len(ids)) + ')', ids)] if ids else []
    texts += [r['feedback'] or '' for r in db.execute(
        "SELECT feedback FROM decisions WHERE suggestion_id=? AND choice='other' AND source IN ('dashboard','telegram')", (suggestion_id,))]
    return texts


def clean(check):
    """{"url", "expect"} as kept, or ValueError saying what a check is. None or {} clears it."""
    if check in (None, {}, ''):
        return None
    if not isinstance(check, dict):
        raise ValueError('done_check is {"url", "expect"}: the public page that will show the result, and 1 to 3 short words or names it must show')
    url = _address(check.get('url'))
    words = check.get('expect')
    words = [words] if isinstance(words, str) else words
    words = [' '.join(str(w).split()) for w in words or [] if str(w).strip()] if isinstance(words, list) else []
    if not url:
        raise ValueError('done_check url is the public https page that will show the result, as its message gives it')
    if not 1 <= len(words) <= EXPECT_MAX or any(len(w) < 2 or len(w) > EXPECT_LEN for w in words):
        raise ValueError(f'done_check expect is 1 to {EXPECT_MAX} short words or names (2 to {EXPECT_LEN} characters each) the page must show, like the owner\'s product name or domain')
    return {'url': url, 'expect': words}


def set_check(db, suggestion_id, check, by):
    """Keep a clean check on a to-do with a done when, only when its address is in its evidence. Returns what was kept
    (None: no check, or cleared), or ValueError when the address isn't in its messages."""
    if check is None:
        db.execute('UPDATE suggestions SET done_check=NULL WHERE id=?', (suggestion_id,))
        return None
    row = db.execute('SELECT done_when,done_check FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or not row['done_when']:
        raise ValueError('done_check goes with a done_when: the result the page will show')
    if not in_evidence(check['url'], evidence_texts(db, suggestion_id)):
        raise ValueError('done_check url must be an address this to-do\'s messages or the owner give; none of them names it, so no check was kept')
    old = _load(row['done_check'])
    if old and _same(old['url'], check['url']) and old['expect'] == check['expect']:
        return old
    kept = {'kind': KIND, **check, 'by': by}
    db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded(kept), suggestion_id))
    return kept


def _outcome(row):
    try:
        found = json.loads(row['outcome'] or 'null')
    except (TypeError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def _state(plan, until):
    """The check's state for this wait (its episode is the wait's until): fresh when the to-do waits anew."""
    return plan.get('run') if isinstance(plan.get('run'), dict) and plan['run'].get('episode') == until else {'episode': until}


def _when(run, until):
    return run.get('next_at') or until


def holds(row, stamp):
    """return_waiting leaves this waiting to-do for its check: one still to read for this wait, within HOLD of its time."""
    plan = _load(row['done_check']) if 'done_check' in row.keys() else None
    until = str(_outcome(row).get('until') or '')
    if not plan or not until or not row['done_when']:
        return False
    run = _state(plan, until)
    if (plan.get('baseline') or {}).get('state') != 'clear' or run.get('done') or (run.get('attempts', 0) >= MAX_ATTEMPTS and not _live(run, stamp)):
        return False
    return dt.datetime.fromisoformat(stamp) < dt.datetime.fromisoformat(_when(run, until)) + HOLD


def _live(run, stamp):
    """A claim whose read may still be under way (younger than LEASE)."""
    held = run.get('claim') or {}
    return bool(held) and dt.datetime.fromisoformat(held['at']) + LEASE > dt.datetime.fromisoformat(stamp)


def _baselines(db, stamp, limit):
    """Open to-dos whose check still needs its first read of the page as it is, claimed like a check."""
    out = []
    marks = ','.join('?' * len(todo_states.OPEN))
    for row in db.execute(f'SELECT id,done_check FROM suggestions WHERE status IN ({marks}) AND done_check IS NOT NULL', todo_states.OPEN).fetchall():
        if len(out) >= limit:
            break
        plan = _load(row['done_check'])
        base = (plan or {}).get('baseline') or {}
        if not plan or base.get('state') or (base.get('next_at') or '') > stamp or _live(base, stamp):
            continue
        token = uuid.uuid4().hex
        base = {**base, 'claim': {'token': token, 'at': stamp}, 'attempts': base.get('attempts', 0) + 1}
        db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'baseline': base}), row['id']))
        out.append({'id': row['id'], 'url': plan['url'], 'expect': plan['expect'], 'token': token, 'baseline': True})
    return out


def claim(db, stamp, limit=1):
    """The checks due, claimed (a token, the time, one more attempt) inside the caller's write transaction: a baseline
    first ({..., baseline: True}), else a waiting to-do's ({id, url, expect, token, episode}). A claim older than LEASE
    is taken again."""
    out = _baselines(db, stamp, limit)
    for row in db.execute("SELECT id,status,outcome,done_when,done_check FROM suggestions WHERE status='prepared' AND done_check IS NOT NULL "
                          "AND handled_hint IS NULL AND json_extract(outcome,'$.state')='waiting'").fetchall():
        if len(out) >= limit:
            break
        plan, until = _load(row['done_check']), str(_outcome(row).get('until') or '')
        if not plan or not until or not row['done_when'] or not holds(row, stamp):
            continue
        run = _state(plan, until)
        if _when(run, until) > stamp or _live(run, stamp) or run.get('attempts', 0) >= MAX_ATTEMPTS:
            continue
        token = uuid.uuid4().hex
        run = {**run, 'claim': {'token': token, 'at': stamp}, 'attempts': run.get('attempts', 0) + 1}
        db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
        out.append({'id': row['id'], 'url': plan['url'], 'expect': plan['expect'], 'token': token, 'episode': until})
    return out


def shows(lines, words):
    """Whether a page's text shows every word or name: whole words, any case, spaces as on the page."""
    text = ' '.join(' '.join(lines).split()).lower()
    return all(re.search(r'(?<![\w-])' + re.escape(' '.join(w.split()).lower()) + r'(?![\w-]|\.\w)', text) for w in words)


def judge(lines, words):
    """('met' | 'not_met', fingerprint) of a page that was read."""
    return ('met' if shows(lines, words) else 'not_met'), web_page.fingerprint(lines)


def _line(db, sid, text, stamp, key):
    db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               (PREFIX + hashlib.sha256(f'{sid}:{key}'.encode()).hexdigest()[:32], sid, 'update', text[:200], 'assistant', stamp))


def _deadline_end(row):
    if not row['due']:
        return None
    if row['due_at']:
        at = dt.datetime.fromisoformat(str(row['due_at']))
        return at if at.tzinfo else at.replace(tzinfo=local_tz())
    day = dt.date.fromisoformat(str(row['due'])[:10]) + dt.timedelta(days=1)
    return dt.datetime.combine(day, dt.time(0, 0), local_tz())


def _settle_baseline(db, job, result, stamp):
    row = db.execute('SELECT done_check FROM suggestions WHERE id=?', (job['id'],)).fetchone()
    plan = _load(row['done_check']) if row else None
    base = (plan or {}).get('baseline') or {}
    if not plan or not _same(plan['url'], job['url']) or plan['expect'] != job['expect'] or (base.get('claim') or {}).get('token') != job['token']:
        return None
    base = {k: v for k, v in base.items() if k != 'claim'}
    if result in ('met', 'not_met'):
        base.update(state='shown' if result == 'met' else 'clear', at=stamp)
    elif base.get('attempts', 0) >= MAX_ATTEMPTS:
        base.update(state='unread', at=stamp)
    else:
        base['next_at'] = (dt.datetime.fromisoformat(stamp) + RETRY).isoformat()
    db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'baseline': base}), job['id']))
    return 'baseline:' + base.get('state', 'retry')


def settle(db, job, result, stamp, why=None, fingerprint=None, lines=None):
    """Keep what one read found, inside the caller's write transaction, only for the claim it was read for on a to-do
    that still waits the same way. Returns 'checking' (shown: result_checks.py checks it), 'recheck', 'retry', 'back', 'baseline:<clear|shown|unread|retry>'
    or None (the to-do moved on)."""
    if job.get('baseline'):
        return _settle_baseline(db, job, result, stamp)
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (job['id'],)).fetchone()
    plan = _load(row['done_check']) if row else None
    outcome = _outcome(row) if row else {}
    if not plan or row['status'] != 'prepared' or outcome.get('state') != 'waiting' or str(outcome.get('until') or '') != job['episode'] \
            or row['handled_hint'] or not row['done_when'] or not _same(plan['url'], job['url']) or plan['expect'] != job['expect']:
        return None
    run = _state(plan, job['episode'])
    if (run.get('claim') or {}).get('token') != job['token'] or run.get('done'):
        return None
    since = (run.get('claim') or {}).get('at') or stamp
    if db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND created_at>? AND id NOT LIKE ?", (row['id'], since, PREFIX + '%')).fetchone():
        return None  # the owner or a newer message moved it while the page was read: theirs stands
    page = web_page.page_name(plan['url'])
    run = {**{k: v for k, v in run.items() if k != 'claim'}, 'last': {'at': stamp, 'result': result, **({'why': why} if why else {})}}
    if result == 'met' and db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (row['id'],)).fetchone():
        result = 'unknown'  # a send of it is under way: read again later, never a close beside it
    if result == 'met':
        run['done'] = True
        db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
        decision_id = VERIFIED + hashlib.sha256(f"{row['id']}:{plan['url']}:{fingerprint}".encode()).hexdigest()[:32]
        if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
            return 'back'  # closed for this version of the page before and the owner took it back: theirs stands
        from machine.store import result_checks  # the words are there: checked against what was agreed before it closes
        return result_checks.request(db, row, 'page', i18n.t('{} shows {}', page, ', '.join(plan['expect'])), decision_id, stamp,
                                     url=plan['url'], lines=lines)
    if result == 'not_met':
        end = _deadline_end(row)
        if end and not run.get('rechecked') and end > dt.datetime.fromisoformat(stamp):
            from machine.store.cards import wait_until
            run.update(rechecked=True, next_at=wait_until(row['due'], current=end), attempts=min(run.get('attempts', 0), MAX_ATTEMPTS - 1))
            db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
            return 'recheck'
        run['done'] = True
        db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
        _line(db, row['id'], i18n.t('Checked {}: not there yet', page), stamp, f"{job['episode']}:not_met")
        return 'back'
    if run.get('attempts', 0) < MAX_ATTEMPTS:
        run['next_at'] = (dt.datetime.fromisoformat(stamp) + RETRY).isoformat()
        db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
        return 'retry'
    run['done'] = True
    db.execute('UPDATE suggestions SET done_check=? WHERE id=?', (encoded({**plan, 'run': run}), row['id']))
    _line(db, row['id'], i18n.t('Couldn’t open {}', page), stamp, f"{job['episode']}:unknown")
    return 'back'


def chat_line(row):
    """A done-check line in the to-do's chat (card_chat), or None for another decision."""
    return row['feedback'] if str(row['id']).startswith(PREFIX) and row['feedback'] else None

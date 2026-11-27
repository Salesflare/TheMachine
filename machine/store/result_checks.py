"""Result checks (2026-11-28): a waiting to-do whose result seems to have come (a message shows it, outcomes.result_seen;
its page shows the words, done_checks.py) closes only once that is checked against what was agreed in its thread.

A literal match isn't enough: they may have published before the owner's OK, with the wrong price, an old description
or a wrong link, or done their half of an exchange while the owner's half is still owed. So instead of closing, the
to-do keeps what came (request, in the sealed suggestions.result_check) and the App's step asks one small background
turn (machine/prompts/result_check.py) with what came (bounded) and its thread: what the owner asked for and sent, the
material they supplied, their own open promises. Then (settle):

- matches, and nothing owed in return: it closes by itself (outcomes.close_handled) and says what was checked, with Undo;
- the owner owes their part of an exchange (an open promise of theirs on it first, else the turn's owner_owes): it comes
  back as the owner's next step, "<done when>. Your part: <what>", never Done;
- differs: it comes back with the difference, quoted from both sides, and a nudge one tap away;
- early (an approval step skipped) or unsure, a turn that fails or no model: it comes back for a look. Never a close.

What comes back shows that line as its text while open (outcomes.result_summaries); its chat says "Checked <page>"
under the message that named the page, linked there.

A claim older than LEASE is taken again; a verdict counts only for its claim on a to-do that still waits the same way,
with no newer step of the owner or a newer message. return_waiting waits for a check at most HOLD, so a to-do always
comes back. The check only reads; it never sends or writes outside the Machine."""
import datetime as dt
import hashlib
import json
import uuid

import i18n
from connectors import web_page
from machine import todo_states
from machine.prompts.result_check import verdict as kept_verdict
from machine.store import done_checks, outcomes, todo_moves
from machine.text import encoded

LEASE = dt.timedelta(minutes=15)
HOLD = dt.timedelta(hours=6)
MAX_ATTEMPTS = 2
CAME_CHARS = 4000
PREFIX = 'result-check:'  # its chat lines (decisions)


def _load(text):
    try:
        found = json.loads(text or 'null')
    except (TypeError, ValueError):
        return None
    return found if isinstance(found, dict) and found.get('source') in ('page', 'message') else None


def _episode(row):
    outcome = outcomes._outcome(row)
    return f"{outcome.get('state') or ''}:{outcome.get('until') or ''}"


def request(db, row, source, reason, decision_id, stamp, event_ids=(), url=None, lines=None):
    """Instead of closing: keep what came, to be checked against what was agreed first. Returns 'checking'."""
    came = ' '.join(' '.join(lines or []).split())[:CAME_CHARS] if source == 'page' else None
    check = {'source': source, 'reason': ' '.join(str(reason).split())[:200], 'decision_id': decision_id, 'at': stamp,
             'episode': _episode(row), 'attempts': 0, 'event_ids': [int(i) for i in event_ids][:10], 'url': url, 'came': came}
    db.execute('UPDATE suggestions SET result_check=? WHERE id=?', (encoded(check), row['id']))
    return 'checking'


def _live(check, stamp):
    held = check.get('claim') or {}
    return bool(held) and dt.datetime.fromisoformat(held['at']) + LEASE > dt.datetime.fromisoformat(stamp)


def _open(row, check):
    return bool(check) and not check.get('verdict') and check.get('episode') == _episode(row)


def pending(row, stamp):
    """A check still to settle for this wait, within HOLD: return_waiting leaves the to-do for it."""
    check = _load(row['result_check']) if 'result_check' in row.keys() else None
    return _open(row, check) and dt.datetime.fromisoformat(stamp) < dt.datetime.fromisoformat(check['at']) + HOLD


def owed_promises(db, row):
    """The owner's own open promises on this to-do or its messages (promises.py): their half of an exchange."""
    try:
        ids = [int(i) for i in json.loads(row['event_ids'] or '[]')][:50]
    except (TypeError, ValueError):
        ids = []
    return [r['what'] for r in db.execute(
        "SELECT what FROM promises WHERE direction='mine' AND status IN ('open','carded') AND (suggestion_id=? OR event_id IN "
        '(SELECT value FROM json_each(?))) ORDER BY created_at LIMIT 3', (row['id'], json.dumps(ids)))]


def thread(db, row):
    """What was agreed: its messages, the owner's words and notes, and what the owner sent from it (with file names)."""
    texts = done_checks.evidence_texts(db, row['id'])
    for job in db.execute("SELECT payload FROM action_jobs WHERE suggestion_id=? AND status='sent' ORDER BY created_at", (row['id'],)):
        try:
            action = json.loads(job['payload'] or '{}')
        except ValueError:
            continue
        files = [str(a.get('name') or a.get('filename') or '') for a in action.get('attachments') or [] if isinstance(a, dict)]
        texts.append('The owner sent: ' + ' '.join(str(action.get(k) or '') for k in ('subject', 'body')).strip()
                     + (f" (files: {', '.join(f for f in files if f)})" if any(files) else ''))
    return texts


def claim(db, stamp, limit=1):
    """Checks to ask about, claimed inside the caller's write transaction: [{id, token, done_when, source, url, came,
    thread, promises}]."""
    out = []
    marks = ','.join('?' * len(todo_states.OPEN))
    for row in db.execute(f'SELECT * FROM suggestions WHERE result_check IS NOT NULL AND status IN ({marks})', todo_states.OPEN).fetchall():
        if len(out) >= limit:
            break
        check = _load(row['result_check'])
        if not _open(row, check) or _live(check, stamp) or check.get('attempts', 0) >= MAX_ATTEMPTS:
            continue
        token = uuid.uuid4().hex
        check = {**check, 'claim': {'token': token, 'at': stamp}, 'attempts': check.get('attempts', 0) + 1}
        db.execute('UPDATE suggestions SET result_check=? WHERE id=?', (encoded(check), row['id']))
        came = check.get('came')
        if check['source'] == 'message':
            ids = check.get('event_ids') or []
            came = '\n'.join(f"{r['title'] or ''}\n{r['body'] or ''}" for r in db.execute(
                'SELECT title,body FROM events WHERE deleted=0 AND id IN (SELECT value FROM json_each(?))', (json.dumps(ids),)))[:CAME_CHARS]
        out.append({'id': row['id'], 'token': token, 'done_when': row['done_when'], 'source': check['source'], 'url': check.get('url'),
                    'came': came or '', 'thread': thread(db, row), 'promises': owed_promises(db, row)})
    return out


def _line(db, sid, text, stamp, key):
    db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               (PREFIX + hashlib.sha256(f'{sid}:{key}'.encode()).hexdigest()[:32], sid, 'update', text[:200], 'assistant', stamp))


def _come_back(db, row, line, stamp, owed):
    """Back as an open to-do with its line: the owner's part of an exchange (no longer waiting on them), or a look at what
    came while it still waits on them (a nudge one tap away when something differs)."""
    who = str(outcomes._outcome(row).get('waiting_on') or '')[:200]
    db.execute('UPDATE suggestions SET outcome=?,chat_asks=? WHERE id=?',
               (None if owed else encoded({'state': 'still_waiting', 'waiting_on': who}), None if owed else encoded([outcomes.nudge_ask()]), row['id']))
    todo_moves.transition(db, row['id'], todo_states.PENDING, 'result_check', at=stamp)
    db.execute("INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,'queued',?) ON CONFLICT(suggestion_id) DO UPDATE SET "
               "status=CASE WHEN status IN ('sending') THEN status ELSE 'queued' END,reminder=1,error=NULL,"
               "needs_edit=CASE WHEN message_id IS NULL THEN needs_edit ELSE 1 END,updated_at=excluded.updated_at", (row['id'], stamp))


def settle(db, job, answer, stamp):
    """Keep one turn's answer (None: no answer, the turn failed) inside the caller's write transaction, only for its claim
    on a to-do that still waits the same way. Returns 'closed', 'owed', 'differs', 'early', 'unsure' or None."""
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (job['id'],)).fetchone()
    check = _load(row['result_check']) if row else None
    if not check or row['status'] not in todo_states.OPEN or check.get('verdict') or check.get('episode') != _episode(row) \
            or (check.get('claim') or {}).get('token') != job['token']:
        return None
    since = check['claim']['at']
    if db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND created_at>? AND id NOT LIKE ? AND id NOT LIKE ?",
                  (row['id'], since, PREFIX + '%', done_checks.PREFIX + '%')).fetchone():
        return None  # the owner or a newer message moved it while it was checked: theirs stands
    found = kept_verdict(answer) if answer is not None else {'state': 'unsure', 'checked': '', 'difference': '', 'owed': ''}
    promised = owed_promises(db, row)
    owed = promised[0] if promised else found['owed']
    state = found['state']
    page = web_page.page_name(check['url']) if check.get('url') else ''
    if state == 'matches' and not owed and db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (row['id'],)).fetchone():
        state = 'unsure'  # a send of it is under way: never a close beside it
    check = {k: v for k, v in check.items() if k not in ('claim', 'came')}
    if state == 'matches' and not owed:
        if db.execute('SELECT 1 FROM decisions WHERE id=?', (check['decision_id'],)).fetchone():
            state = 'unsure'  # closed for this before and the owner took it back: theirs stands, it comes back for a look
        else:
            db.execute('UPDATE suggestions SET result_check=? WHERE id=?', (encoded({**check, 'verdict': 'matches', 'checked': found['checked']}), row['id']))
            outcomes.close_handled(db, row, check['decision_id'], ', '.join(x for x in (check['reason'], found['checked']) if x), stamp)
            db.execute('UPDATE suggestions SET handled_hint=NULL WHERE id=?', (row['id'],))
            return 'closed'
    if state == 'differs':
        line = i18n.t('Live, but {}', found['difference']) if page else i18n.t('It came, but {}', found['difference'])
    elif state == 'early':
        line = i18n.t('Published before your OK: {}', page) if page else i18n.t('Done before your OK: have a look')
    elif owed:
        state, line = 'owed', i18n.t('{}. Your part: {}', str(row['done_when']).rstrip('.'), str(owed).rstrip('.'))
    else:
        state, line = 'unsure', i18n.t('Live on {}: have a look', page) if page else i18n.t('Looks done: have a look')
    db.execute('UPDATE suggestions SET result_check=? WHERE id=?', (encoded({**check, 'verdict': state, 'line': line[:200]}), row['id']))
    _come_back(db, row, line, stamp, state == 'owed')
    # its chat says it checked (with the page one tap away); the verdict is the to-do's own text (outcomes.result_summaries)
    _line(db, row['id'], i18n.t('Checked {}', page) if page else i18n.t('Checked it against what was agreed'), stamp, check['decision_id'])
    return state


def given_up(db, stamp):
    """Checks whose turns all failed: settled as unsure, so the to-do comes back for a look. Returns how many."""
    marks = ','.join('?' * len(todo_states.OPEN))
    n = 0
    for row in db.execute(f'SELECT id,result_check FROM suggestions WHERE result_check IS NOT NULL AND status IN ({marks})', todo_states.OPEN).fetchall():
        check = _load(row['result_check'])
        if check and not check.get('verdict') and check.get('attempts', 0) >= MAX_ATTEMPTS and not _live(check, stamp) and check.get('claim'):
            n += bool(settle(db, {'id': row['id'], 'token': check['claim']['token']}, None, stamp))
    return n


def chat_line(row):
    """A result-check line in the to-do's chat (card_chat), or None for another decision. The page it read is linked in
    the message above that named it (a done check reads only a page its messages give)."""
    return row['feedback'] if str(row['id']).startswith(PREFIX) and row['feedback'] else None

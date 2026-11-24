"""Send later: an approved message that waits for the time the owner picked, and what stops it (docs/architecture.md,
Send later). The rows only; the fresh read right before it goes is machine/app/send_later.py.

A scheduled send is a row of scheduled_sends with the action exactly as approved. No outbox job exists until its time,
so nothing else can send it. Meanwhile its to-do sleeps under Later until that same time, and everything that takes the
to-do somewhere else (done, not needed, another Later time, back on the list, a changed or replaced draft) ends the
scheduled send: sweep() lets only a to-do that still sleeps until exactly then, with exactly that draft, go on.

    waiting     its time hasn't come
    queued      its time came: it is an outbox job now, which the outbox checks once more right before it goes
    now         Send now: an outbox job like any other Send
    canceled    Cancel, or the to-do moved on
    changed     the draft isn't what was approved anymore
    taken_back  someone wrote first
    late        more than LATE after its time (off, asleep, paused): it asks instead of going late
    unread      the conversation couldn't be read for LATE: it asks instead of going blind
    stopped     the outbox stopped it (a check, a hold), or The Machine moved to another computer

The last four put the to-do back with its draft, the reason on it (an outbox job that is blocked, like any Send a check
stopped) and the notice a to-do that comes back gets. A new Send is a new approval."""
import datetime as dt
import json
import sqlite3
import uuid

import activity_log
import follow_ups
import graph
import i18n
import locale_prefs
import mail_senders
from machine import kinds, todo_states
from machine.cards import snooze_time
from machine.owner_error import OwnerError
from machine.store import todo_moves
from machine.text import encoded
import next_actions
from timeutil import local_tz

CHANNELS = (*kinds.SEND_LATER, 'email_demo')  # what can wait, and the demo's email, which goes nowhere
LATE = dt.timedelta(hours=1)   # how long after its time it may still go; after that it asks
RETRY = dt.timedelta(minutes=2)  # the conversation couldn't be read: tried again this often
OLDER = dt.timedelta(days=1)   # mail from them dated this long before the approval, collected after it, still counts
RESEND = ('blocked', 'cancelled', 'failed')  # outbox jobs a new approval may queue again (confirm_action)

REPLIED = 'Not sent: {} wrote first.'
LATE_LINE = 'Not sent: it was more than an hour late.'
UNREAD_LINE = 'Not sent: couldn’t check for a new message first.'
ON_ITS_WAY = 'It’s already on its way.'
NOT_WAITING = 'It isn’t scheduled anymore.'

SCHEMA = ('CREATE TABLE IF NOT EXISTS scheduled_sends(id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,revision TEXT NOT NULL,'
          'payload TEXT NOT NULL,send_at TEXT NOT NULL,approved_at TEXT NOT NULL,approval_id TEXT NOT NULL,source TEXT NOT NULL,'
          'basis TEXT,state TEXT NOT NULL,job_id TEXT,from_id INTEGER NOT NULL DEFAULT 0,checked_id INTEGER,hold_state TEXT,updated_at TEXT NOT NULL)')
LOG = ('CREATE TABLE IF NOT EXISTS scheduled_send_log(id INTEGER PRIMARY KEY,send_id TEXT NOT NULL,suggestion_id TEXT NOT NULL,'
       'at TEXT NOT NULL,kind TEXT NOT NULL,send_at TEXT NOT NULL)')


def ensure(db):
    db.execute(SCHEMA)
    db.execute(LOG)
    db.execute('CREATE INDEX IF NOT EXISTS scheduled_sends_card ON scheduled_sends(suggestion_id,state)')
    db.execute('CREATE INDEX IF NOT EXISTS scheduled_sends_job ON scheduled_sends(job_id)')


def _log(db, row, kind, at, send_at=None):
    db.execute('INSERT INTO scheduled_send_log(send_id,suggestion_id,at,kind,send_at) VALUES(?,?,?,?,?)',
               (row['id'], row['suggestion_id'], at, kind, send_at or row['send_at']))


def waiting(db, suggestion_id):
    return db.execute("SELECT * FROM scheduled_sends WHERE suggestion_id=? AND state='waiting' ORDER BY approved_at", (suggestion_id,)).fetchall()


def of_job(db, job_id):
    """The scheduled send an outbox job is (its time came), or None for any other send: also one approved again since."""
    return db.execute("SELECT w.* FROM scheduled_sends w JOIN action_jobs j ON j.id=w.job_id AND j.approval_id=w.approval_id "
                      "WHERE w.job_id=? AND w.state='queued'", (job_id,)).fetchone()


# ------------------------------------------------------------------ the outbox's rows

def insert_job(db, job_id, suggestion_id, revision, action, status, stamp, approval_id, source, basis, retry_at=None, error=None):
    """An approved step's row in the outbox (action_jobs): Store.confirm_action's, and a scheduled send's when its time comes."""
    db.execute('INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id,retry_at,error,basis) '
               'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
               (job_id, suggestion_id, revision, encoded(action), status, stamp, stamp, approval_id, source,
                '<assistant-' + job_id + '@' + action['from'].split('@')[1] + '>' if action['kind'] == 'email' else '', retry_at, error, basis))


def _job(db, row, status, at, error=None):
    """The scheduled send's outbox job in this status: a new one, or the earlier one of this draft that didn't go. None
    when that one is on its way or went: never a second send."""
    action, stamp = json.loads(row['payload']), at
    previous = db.execute('SELECT id,status FROM action_jobs WHERE suggestion_id=? AND revision=?', (row['suggestion_id'], row['revision'])).fetchone()
    if previous is None:
        job_id = uuid.uuid4().hex
        insert_job(db, job_id, row['suggestion_id'], row['revision'], action, status, stamp, row['approval_id'], row['source'], row['basis'], error=error)
        return job_id
    if previous['status'] not in RESEND:
        return None
    db.execute('UPDATE action_jobs SET status=?,retry_at=NULL,error=?,updated_at=?,approval_id=?,source=?,payload=?,basis=? WHERE id=?',
               (status, error, stamp, row['approval_id'], row['source'], encoded(action), row['basis'], previous['id']))
    return previous['id']


def _wake(db, suggestion_id, reason, at):
    db.execute("UPDATE suggestions SET snoozed_until=NULL,resume_status=NULL WHERE id=? AND status='snoozed'", (suggestion_id,))
    todo_moves.transition(db, suggestion_id, todo_states.PREPARED, reason, only=todo_states.SNOOZED, at=at)


def notice(db, suggestion_id):
    """The notice a to-do that comes back from Later gets (wake_snoozed), one per return."""
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (suggestion_id,))
    db.execute("UPDATE deliveries SET status='queued',reminder=1,error=NULL WHERE suggestion_id=? AND status IN ('sent','uncertain')", (suggestion_id,))


# ------------------------------------------------------------------ what the owner does

def pick_time(value):
    """The moment the owner picked, in UTC: within the next year, as a snooze's own time."""
    return snooze_time(explicit=value)


def schedule(db, suggestion, revision, action, approval_id, source, basis, send_at, at):
    """The owner approved this message for send_at (Store.confirm_action checked it as any Send). The to-do sleeps under
    Later until then. {'status': 'scheduled', 'send_at'}."""
    if action['kind'] not in CHANNELS:
        raise OwnerError(i18n.t('This can’t be sent later.'))
    sid = suggestion['id']
    again = db.execute('SELECT state,send_at FROM scheduled_sends WHERE approval_id=?', (approval_id,)).fetchone()
    if again:
        return {'status': 'scheduled' if again['state'] == 'waiting' else again['state'], 'send_at': again['send_at'], 'duplicate': True}
    db.execute("UPDATE action_jobs SET status='cancelled',error=NULL,retry_at=NULL,updated_at=? WHERE suggestion_id=? AND revision=? AND status IN ('blocked','failed')",
               (at, sid, revision))
    for old in waiting(db, sid):
        if old['revision'] == revision:  # approved again: this approval replaces it
            db.execute("UPDATE scheduled_sends SET state='canceled',updated_at=? WHERE id=?", (at, old['id']))
    row = {'id': uuid.uuid4().hex, 'suggestion_id': sid, 'send_at': send_at}
    top = db.execute('SELECT COALESCE(MAX(id),0) FROM events').fetchone()[0]
    db.execute('INSERT INTO scheduled_sends(id,suggestion_id,revision,payload,send_at,approved_at,approval_id,source,basis,state,from_id,updated_at) '
               "VALUES(?,?,?,?,?,?,?,?,?,'waiting',?,?)",
               (row['id'], sid, revision, encoded(action), send_at, at, approval_id, source, basis, top, at))
    db.execute("UPDATE suggestions SET snoozed_until=?,resume_status='prepared',undo_until=NULL,feedback_until=NULL,early=0 WHERE id=?", (send_at, sid))
    todo_moves.transition(db, sid, todo_states.SNOOZED, 'send_later', at=at)
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (sid,))
    _log(db, row, 'scheduled', at)
    return {'status': 'scheduled', 'send_at': send_at}


def _one(db, suggestion_id):
    """The to-do's scheduled sends that still wait, or why there are none to change."""
    rows = waiting(db, suggestion_id)
    if rows:
        return rows
    going = db.execute("SELECT j.status FROM scheduled_sends s JOIN action_jobs j ON j.id=s.job_id WHERE s.suggestion_id=? AND s.state='queued' "
                       "AND j.status IN ('sending','uncertain','sent')", (suggestion_id,)).fetchone()
    raise OwnerError(i18n.t(ON_ITS_WAY if going else NOT_WAITING))


def move(db, suggestion_id, send_at, at):
    """Change time: the approval stands, only the moment changes."""
    rows = _one(db, suggestion_id)
    sweep(db, at)
    rows = _one(db, suggestion_id)
    for row in rows:
        db.execute('UPDATE scheduled_sends SET send_at=?,updated_at=? WHERE id=?', (send_at, at, row['id']))
        _log(db, row, 'moved', at, send_at)
    db.execute("UPDATE suggestions SET snoozed_until=? WHERE id=? AND status='snoozed'", (send_at, suggestion_id))
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (suggestion_id,))
    return {'status': 'scheduled', 'send_at': send_at}


def _queued_jobs(db, suggestion_id):
    """Its scheduled sends whose time came and that still wait in the outbox (a read that failed, a pause)."""
    return db.execute("SELECT s.*,j.status job_status FROM scheduled_sends s JOIN action_jobs j ON j.id=s.job_id WHERE s.suggestion_id=? "
                      "AND s.state='queued' AND j.status='queued' AND j.approval_id=s.approval_id", (suggestion_id,)).fetchall()


def cancel(db, suggestion_id, at):
    """Cancel: nothing goes out, the draft is back on the to-do."""
    out = _queued_jobs(db, suggestion_id)
    if not out:
        for row in _one(db, suggestion_id):
            db.execute("UPDATE scheduled_sends SET state='canceled',updated_at=? WHERE id=?", (at, row['id']))
            _log(db, row, 'canceled', at)
    for row in out:
        if db.execute("UPDATE action_jobs SET status='cancelled',error=NULL,retry_at=NULL,updated_at=? WHERE id=? AND status='queued'", (at, row['job_id'])).rowcount:
            db.execute("UPDATE scheduled_sends SET state='canceled',updated_at=? WHERE id=?", (at, row['id']))
    _wake(db, suggestion_id, 'send_later_canceled', at)
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (suggestion_id,))
    return {'status': 'canceled'}


def send_now(db, suggestion_id, at):
    """Send now: what was approved goes like any other Send, in its turn."""
    sweep(db, at)
    out = _queued_jobs(db, suggestion_id)
    for row in out:
        db.execute("UPDATE scheduled_sends SET state='now',updated_at=? WHERE id=?", (at, row['id']))
        db.execute("UPDATE action_jobs SET retry_at=NULL,updated_at=? WHERE id=? AND status='queued'", (at, row['job_id']))
    if not out:
        release(db, _one(db, suggestion_id), at, 'now')
    return {'status': 'queued'}


# ------------------------------------------------------------------ its time, and what stops it

def release(db, rows, at, state='queued'):
    """Their time came: the to-do's scheduled sends become outbox jobs, each claimed once (two workers, a tap on Send now)."""
    for row in rows:
        if not db.execute("UPDATE scheduled_sends SET state=?,updated_at=? WHERE id=? AND state='waiting'", (state, at, row['id'])).rowcount:
            continue
        _wake(db, row['suggestion_id'], 'send_later_due', at)
        job_id = _job(db, row, 'queued', at)
        db.execute('UPDATE scheduled_sends SET job_id=? WHERE id=?', (job_id, row['id']))
        if job_id is None:
            continue
        db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   (row['approval_id'], row['suggestion_id'], 'send', '', row['source'], at))
        # A follow-up joins its batch's spacing; queued as of its approval, so a pause since then holds it
        follow_ups.queued(db, row['suggestion_id'], job_id, json.loads(row['payload']), row['approved_at'])
        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (row['suggestion_id'],))


def ask(db, row, state, line, at, news=None):
    """It doesn't go: the to-do is back with its draft, the reason on it, and the owner hears of it once. True when this
    call stopped it, False when it already went on or was stopped."""
    if row['state'] == 'queued':
        if not db.execute("UPDATE action_jobs SET status='blocked',error=?,retry_at=NULL,updated_at=? WHERE id=? AND status='queued'",
                          (line, at, row['job_id'])).rowcount:
            return False
        db.execute("UPDATE scheduled_sends SET state=?,updated_at=? WHERE id=? AND state='queued'", (state, at, row['id']))
        job_id = row['job_id']
    else:
        if not db.execute("UPDATE scheduled_sends SET state=?,updated_at=? WHERE id=? AND state='waiting'", (state, at, row['id'])).rowcount:
            return False
        _wake(db, row['suggestion_id'], 'send_later_back', at)
        job_id = _job(db, row, 'blocked', at, line)
    if job_id:
        activity_log.note_block(db, job_id, line, at)
        if news:
            follow_ups.note_hold(db, job_id, row['suggestion_id'], 'changed', news, at)
    notice(db, row['suggestion_id'])
    return True


def held(db, job_id, at):
    """The outbox stopped a scheduled send by itself (a check before it, a follow-up's hold): the owner hears of it, as
    it happened while they weren't looking."""
    row = of_job(db, job_id)
    if row and db.execute("SELECT 1 FROM action_jobs WHERE id=? AND status='blocked'", (job_id,)).fetchone():
        db.execute("UPDATE scheduled_sends SET state='stopped',updated_at=? WHERE id=?", (at, row['id']))
        notice(db, row['suggestion_id'])


def failed(db, job_id, at):
    """It was refused, or it isn't clear it went: the owner hears of it."""
    row = of_job(db, job_id)
    if row:
        notice(db, row['suggestion_id'])


def is_late(row, at):
    return dt.datetime.fromisoformat(at) > dt.datetime.fromisoformat(row['send_at']) + LATE


def ask_late(db, row, at):
    return ask(db, row, *(('unread', UNREAD_LINE) if row['hold_state'] == 'unread' else ('late', LATE_LINE)), at)


def wait_unread(db, row, at):
    """The conversation couldn't be read right before it goes: it waits a little, and the to-do says so."""
    db.execute("UPDATE scheduled_sends SET hold_state='unread',updated_at=? WHERE id=? AND state='queued'", (at, row['id']))
    db.execute("UPDATE action_jobs SET retry_at=?,updated_at=? WHERE id=? AND status='queued'",
               ((dt.datetime.fromisoformat(at) + RETRY).isoformat(), at, row['job_id']))


def read_again(db, row):
    """Its conversation could be read after all."""
    db.execute('UPDATE scheduled_sends SET hold_state=NULL WHERE id=?', (row['id'],))


def sweep(db, at):
    """End the scheduled sends whose to-do moved on, or whose draft isn't the approved one anymore."""
    for row in db.execute("SELECT w.*,s.status,s.snoozed_until,s.next_action FROM scheduled_sends w LEFT JOIN suggestions s ON s.id=w.suggestion_id "
                          "WHERE w.state='waiting'").fetchall():
        asleep = row['status'] == todo_states.SNOOZED and row['snoozed_until'] == row['send_at']
        same = asleep and next_actions.selected(row['next_action'], row['revision'])
        if same:
            continue
        db.execute('UPDATE scheduled_sends SET state=?,updated_at=? WHERE id=?', ('changed' if asleep else 'canceled', at, row['id']))
        _log(db, row, 'canceled', at)
        if asleep:  # another draft took its place: it waits for a new approval
            _wake(db, row['suggestion_id'], 'send_later_changed', at)
            notice(db, row['suggestion_id'])
        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (row['suggestion_id'],))


# ------------------------------------------------------------------ did someone write first

def _keys(kind, account, meta):
    """The conversation a collected message is in, as comparable keys."""
    if kind == 'slack.message':
        channel = meta.get('channel_id')
        if not channel:
            return set()
        ts, thread = str(meta.get('message_ts') or ''), str(meta.get('thread_ts') or '')
        if meta.get('conversation_type') == 'dm' and thread in ('', ts):
            return {(account, str(channel), 'dm')}
        return {(account, str(channel), thread or ts)}
    return {(account, str(meta[k])) for k in ('thread_id', 'conversation_id', 'chat_id') if meta.get(k)}


def watched(db, suggestion_id, action):
    """What is watched for a message before it goes: {'keys': the conversations (the send's own, and those its to-do came
    from: a reply by email to a thread that runs on WhatsApp watches both), 'users': Slack members written to directly,
    'emails': every address known for an email's recipients, 'accounts': where those conversations are}."""
    account, kind = action.get('account_id'), action.get('kind')
    keys, users, emails = set(), set(), set()
    for k in ('thread_id', 'conversation_id', 'chat_id'):
        if action.get(k):
            keys.add((account, str(action[k])))
    thread = action.get('thread') or {}
    if thread.get('channel_id'):
        keys.add((account, str(thread['channel_id']), str(thread['ts'])))
    if kind == 'slack' and action.get('user_id'):
        users.add((account, str(action['user_id'])))
    if kind == 'email':
        emails = {a.casefold() for to in action.get('to') or () for a in follow_ups.ADDRESS.findall(str(to))}
        for node, address in graph.people_by_email(db, emails):
            emails.add(address.casefold())
            info = follow_ups._meta(db.execute('SELECT info FROM graph_nodes WHERE id=?', (node,)).fetchone()[0])
            emails |= {str(i)[6:].casefold() for i in info.get('identifiers') or () if str(i).startswith('email:')}
            emails |= {str(e.get('value') or '').casefold() for e in info.get('emails') or () if isinstance(e, dict)}
    emails.discard('')
    came = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    try:
        ids = [int(i) for i in json.loads(came[0] or '[]')] if came else []
    except (TypeError, ValueError):
        ids = []
    messages = set(_message_kinds())
    for e in db.execute(f"SELECT kind,account_id,metadata FROM events WHERE id IN ({','.join('?' * len(ids))})", ids) if ids else ():
        if e['kind'] in messages:
            keys |= _keys(e['kind'], e['account_id'], follow_ups._meta(e['metadata']))
    return {'keys': keys, 'users': users, 'emails': emails, 'accounts': {k[0] for k in keys | users} | {account}}


def _message_kinds():
    return (*kinds.of(family=kinds.MAIL), *kinds.of(family=kinds.CHAT))


def _program(meta):
    """An automatic reply, or anything else no person wrote. A person's reply a list passed on is theirs."""
    if str(meta.get('precedence') or '').lower() == 'list' and not mail_senders.automatic_answer(meta):
        meta = {**meta, 'precedence': ''}
    return follow_ups.automated(meta)


def _news(event, meta):
    return {'id': event['id'], 'at': event['occurred_at'], 'mine': False,
            'from': str(meta.get('from') or meta.get('sender_display') or meta.get('sender') or '')[:200]}


def replied(db, row, mine, own_emails):
    """Who wrote first, from what was collected: messages from someone else since the approval, in a conversation that is
    watched or by email from one of the recipients in any of the owner's mailboxes. The owner's own messages, history
    and automatic replies don't count; a forward from them does. [] when nobody did."""
    top = db.execute('SELECT COALESCE(MAX(id),0) FROM events').fetchone()[0]
    if row['checked_id'] is not None and row['checked_id'] >= top:
        return []
    action = json.loads(row['payload'])
    own_emails = {str(e).casefold() for e in own_emails}
    # What came between the draft and its approval holds any Send (follow_ups.reply_since): known now, so said now
    news = follow_ups.reply_since(db, {'id': row['id'], 'suggestion_id': row['suggestion_id'], 'revision': row['revision']}, action, mine, own_emails)
    if news:
        return news
    watch = watched(db, row['suggestion_id'], action)
    emails = watch['emails'] - own_emails
    oldest = (dt.datetime.fromisoformat(row['approved_at']) - OLDER).isoformat()
    sources, mail = _message_kinds(), set(kinds.of(family=kinds.MAIL))
    found = []
    for e in db.execute(f"SELECT * FROM events WHERE id>? AND deleted=0 AND history=0 AND kind IN ({','.join('?' * len(sources))}) ORDER BY id",
                        (max(row['from_id'], row['checked_id'] or 0), *sources)):
        meta = follow_ups._meta(e['metadata'])
        address = (follow_ups.ADDRESS.findall(str(meta.get('from') or '')) or [''])[-1].casefold()
        theirs = (_keys(e['kind'], e['account_id'], meta) & watch['keys']
                  or e['kind'] in mail and address in emails and e['occurred_at'] >= oldest
                  or e['kind'] == 'slack.message' and (e['account_id'], str(meta.get('user_id') or '')) in watch['users']
                  and meta.get('conversation_type') == 'dm')
        if theirs and not (mine(dict(e)) or address and address in own_emails) and not _program(meta):
            found.append(_news(e, meta))
    if not found:
        db.execute('UPDATE scheduled_sends SET checked_id=? WHERE id=?', (top, row['id']))
    return found


def replied_line(news):
    """'Not sent: Sam wrote first.', or the line any held reply has when the message has no name on it."""
    who = follow_ups._sender((news[-1] or {}).get('from')) if news else ''
    return REPLIED.format(who[:60]) if who else follow_ups.HELD


def is_replied_line(line):
    head, tail = REPLIED.split('{}')
    return str(line or '').startswith(head) and str(line).endswith(tail)


def take_back(db, row, news, at):
    return ask(db, row, 'taken_back', replied_line(news), at, news)


# ------------------------------------------------------------------ what shows

def view(db, suggestion_id):
    """The to-do's scheduled send, for the dashboard and Telegram: {'send_at', 'n' messages, 'until' (after which it
    asks), 'unread': True while its conversation can't be read}, or None."""
    try:
        rows = waiting(db, suggestion_id) or _queued_jobs(db, suggestion_id)
    except sqlite3.OperationalError:  # a database from before this, read before it opened for writing
        return None
    if not rows:
        return None
    first = rows[0]
    return {'send_at': first['send_at'], 'n': len(rows), 'revisions': [r['revision'] for r in rows],
            'until': (dt.datetime.fromisoformat(first['send_at']) + LATE).isoformat(),
            **({'due': True} if first['state'] == 'queued' else {}), **({'unread': True} if first['hold_state'] == 'unread' else {})}


def hold_moved(db, line, at):
    """After an import on another computer (machine/export/hold.py): every one that waited asks first. How many."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='scheduled_sends'").fetchone():
        return 0
    return sum(ask(db, row, 'stopped', line, at) for row in db.execute("SELECT * FROM scheduled_sends WHERE state='waiting'").fetchall())


def activity_lines(db, limit):
    """Activity: a message scheduled, its time changed, and one canceled before its time. Its send, or the reason it was
    stopped, is the outbox's own line."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='scheduled_send_log'").fetchone():
        return []
    out = []
    for r in db.execute('SELECT l.*,w.payload,s.title FROM scheduled_send_log l JOIN scheduled_sends w ON w.id=l.send_id '
                        'LEFT JOIN suggestions s ON s.id=l.suggestion_id ORDER BY l.at DESC,l.id DESC LIMIT ?', (limit,)):
        outcome, status = {'scheduled': ('pending', i18n.t('Scheduled')), 'moved': ('pending', i18n.t('Time changed')),
                           'canceled': ('undone', i18n.t('Canceled'))}[r['kind']]
        out.append(activity_log._line('messages', f"later:{r['id']}", r['at'], activity_log.message_what(json.loads(r['payload'])), outcome, status,
                                      by=i18n.t('Approved in the to-do') if r['kind'] == 'scheduled' else None,
                                      todo={'id': r['suggestion_id'], 'title': activity_log._clip(r['title'], 120)} if r['title'] is not None else None,
                                      detail=next_time(r['send_at']) if r['kind'] != 'canceled' else None))
    return out


def next_time(send_at):
    """'Sends Tue 24 Nov at 09:00': in the owner's time zone and format."""
    return i18n.t('Sends {}', locale_prefs.at_text(dt.datetime.fromisoformat(send_at).astimezone(local_tz())))


activity_log.register('messages', activity_lines)

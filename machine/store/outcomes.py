"""Outcomes (2026-11-11): what result counts as done for a to-do, and why a send alone isn't it.

A sent ask, a reply or an accepted handoff is the owner's part; the result is often someone else's (the contract signed,
the quote in, the listing live). A to-do can carry that result in one plain line, its done when (suggestions.done_when,
sealed), like a project's success condition (project_success.py):

- who sets it: a review (suggest done_when), the to-do's run (save done_when, also from what the owner said in its chat;
  '' clears it), a promise of someone else's that became a to-do (what they promised), and a project's blocker to-do
  (the project's condition, which it follows when that changes: follow_project). The run's word stands over a review's;
  a review fills one nobody set, or revises its own (or a promise's or project's) when newer messages change the goal
  and it suggests with card_id (status shows each open to-do's done_when).
- after the owner's part went out (settle_sent, a delegated reply in settle_awaiting, a teammate's Machine accepting a
  handoff), a to-do with a done when isn't done: it waits under Waiting on others (outcome 'waiting', as the review's
  waiting_on, machine.cards.waits_on_others) with the time to chase them (until).
- what closes it: a signal that shows the result. The review reads the to-do's done when with the reply
  (answers_your_card) and calls looks_handled; a project's proof does the same for its blocker to-do. A to-do waiting on
  its result then closes by itself, with Undo for a day (result_seen); one the owner hasn't done their part on only
  looks done, as before.
- what brings it back: nothing by the time to chase (return_waiting): an open to-do again, "Still waiting on", with a
  nudge offered as a chat tap. No new model turn: a nudge is drafted only when the owner asks for it.

No table of its own: two columns on suggestions."""
import hashlib
import json
import re
import uuid

import i18n
from machine.text import encoded

MAX = 140  # one short line, like a project's condition
BY = ('review', 'run', 'promise', 'project')  # who set it; the run's (and the owner's through it) word stands


def clean(text):
    """One tidy line of at most MAX characters, '' for none; ValueError when it is longer."""
    text = re.sub(r'\s+', ' ', str(text or '')).strip()
    if len(text) > MAX:
        raise ValueError(f'done_when is one short line (up to {MAX} characters) saying what result counts as done, like "Sam signed the order form"')
    return text


def set_done_when(db, suggestion_id, text, by):
    """Save a to-do's done when. A review (or a promise or project) only fills one that is empty or set the same way
    before; the run's stands until the run changes it. '' from the run clears it. True when it changed."""
    text = clean(text)
    row = db.execute('SELECT done_when,done_when_by FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        return False
    if by != 'run' and (not text or (row['done_when'] and row['done_when_by'] == 'run')):
        return False
    if (row['done_when'] or '') == text:
        return False
    db.execute('UPDATE suggestions SET done_when=?,done_when_by=? WHERE id=?', (text or None, by if text else None, suggestion_id))
    _follow_waiting(db, suggestion_id, row['done_when'], text)
    return True


def _follow_waiting(db, suggestion_id, before, after):
    """A to-do waiting for its result says what it waits on; when that line was its old done when (wait_for_result
    with no one named), it follows the new one. A line someone wrote (a name, the run's or the owner's words) stays."""
    row = db.execute('SELECT outcome FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    found = _outcome(row) if row else {}
    if not before or not after or found.get('state') not in ('waiting', 'still_waiting'):
        return
    if ' '.join(str(found.get('waiting_on') or '').split()) == ' '.join(before.split())[:200]:
        db.execute('UPDATE suggestions SET outcome=? WHERE id=?', (encoded({**found, 'waiting_on': after[:200]}), suggestion_id))


def _outcome(row):
    try:
        found = json.loads(row['outcome'] or 'null')
    except (TypeError, ValueError, KeyError, IndexError):
        return {}
    return found if isinstance(found, dict) else {}


def waits_for_result(row):
    """An open to-do whose owner did their part and that now waits for its result (or came back still waiting)."""
    return bool(row['done_when']) and (
        (row['status'] == 'prepared' and _outcome(row).get('state') == 'waiting')
        or (row['status'] == 'pending' and _outcome(row).get('state') == 'still_waiting'))


def until_for(row, current=None):
    """When a to-do waiting for its result comes back to chase it: the morning before its deadline, else after the usual
    wait (machine.store.cards.wait_until); with a deadline too close for that, the next check-in (handoff_checkin)."""
    from machine.cards import handoff_checkin
    from machine.store.cards import wait_until
    return wait_until(row['due'], current=current) or handoff_checkin(bool(row['urgent']), row['due'], current.isoformat() if current else None)


def wait_for_result(db, row, who, stamp, decision_id=None, source='assistant'):
    """The owner's part went out but the result isn't there yet: the to-do waits on `who` (or on the result itself) under
    Waiting on others, nothing drafted left on it, and comes back to chase them at until. Its chat says what it waits for."""
    waiting_on = ' '.join(str(who or '').split())[:200] or row['done_when'][:200]
    until = until_for(row)
    db.execute("UPDATE suggestions SET status='prepared',outcome=?,next_action=NULL,early=0,snoozed_until=NULL,resume_status=NULL,"
               'undo_until=NULL,deliver_after=NULL,feedback_until=NULL WHERE id=?',
               (encoded({'state': 'waiting', 'waiting_on': waiting_on, 'until': until}), row['id']))
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               (decision_id or 'outcome-wait:' + uuid.uuid4().hex, row['id'], 'update', '', source, stamp))  # its words stay sealed on the to-do
    db.execute("UPDATE deliveries SET status='cancelled',reminder=0 WHERE suggestion_id=? AND status='queued'", (row['id'],))
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))
    return {'waiting_on': waiting_on, 'until': until}


def chat_line(feedback):
    """The to-do's chat line when it started waiting for its result."""
    return i18n.t('Waiting for the result: {}', feedback)


def nudge_ask():
    """The chat tap a to-do that came back still waiting for its result offers: the owner's word drafts the nudge."""
    return i18n.t('Write a short nudge')


def result_seen(db, row, reason, event_ids, stamp, undo_hours=24):
    """A signal shows the result. A to-do that waits for it closes by itself (Done, "Closed by itself: <reason>", Undo
    for a day), once for the same messages; any other open one looks done (handled_hint), for the owner to close.
    Not while a send of it is under way. Returns 'closed', 'hint' or None."""
    if row['status'] in ('completed', 'rejected'):
        return None
    ids = list(event_ids)
    if waits_for_result(row) and not db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')",
                                                (row['id'],)).fetchone():
        decision_id = 'handled:' + hashlib.sha256(f"{row['id']}:{sorted(int(i) for i in ids)}".encode()).hexdigest()[:32]
        if not db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
            close_handled(db, row, decision_id, reason, stamp, undo_hours)
            db.execute('UPDATE suggestions SET handled_hint=NULL WHERE id=?', (row['id'],))
            return 'closed'
    db.execute('UPDATE suggestions SET handled_hint=? WHERE id=?', (encoded({'reason': reason, 'event_ids': ids, 'at': stamp}), row['id']))
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))
    return 'hint'


def close_handled(db, row, decision_id, reason, stamp, undo_hours=24):
    """Close an open to-do that a signal shows done: Done, "Closed by itself: <reason>", with Undo for undo_hours."""
    from machine.store.decisions import close_by_itself
    close_by_itself(db, row, decision_id, ' '.join(str(reason).split())[:200], 'handled', stamp, undo_hours)
    db.execute('UPDATE suggestions SET early=0 WHERE id=?', (row['id'],))


def close_replaced(db, row, decision_id, reason, stamp):
    """A newer one replaced this open to-do (a Daily digest's next one): its hint shows the reason, then it closes by
    itself like close_handled, with Undo."""
    db.execute('UPDATE suggestions SET handled_hint=? WHERE id=?', (json.dumps({'reason': reason, 'at': stamp}), row['id']))
    close_handled(db, row, decision_id, reason, stamp)


def project_proof(db, todo_id, condition, event_id, stamp):
    """A project's proof came in: the to-do made for its blocker has its result (result_seen)."""
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (todo_id,)).fetchone() if todo_id else None
    if row and row['status'] not in ('completed', 'rejected'):
        if not row['done_when']:
            return None
        return result_seen(db, row, condition, [event_id], stamp)
    return None


def follow_project(db, todo_id, before, after):
    """The project's Done when changed: its blocker to-do, which carries it (set by 'project'), tracks the new one while
    open, and its "Done when:" body with it. One a review or the run set since stays theirs. True when it changed."""
    row = db.execute('SELECT status,done_when,done_when_by,body FROM suggestions WHERE id=?', (todo_id,)).fetchone()
    if not row or row['status'] in ('completed', 'rejected') or row['done_when_by'] != 'project':
        return False
    after = clean(after)
    db.execute('UPDATE suggestions SET done_when=?,done_when_by=? WHERE id=?', (after or None, 'project' if after else None, todo_id))
    _follow_waiting(db, todo_id, row['done_when'], after)
    if after and before and row['body'] == i18n.t('Done when: {}', before)[:690]:
        db.execute('UPDATE suggestions SET body=? WHERE id=?', (i18n.t('Done when: {}', after)[:690], todo_id))
    return True


def theirs_line(who, what):
    """A promise of someone else's as the result its to-do waits for."""
    return i18n.t('{} kept the promise to {}', who, what)


def handoff_reply(db, row, watch, answer, stamp):
    """A delegated to-do's person answered (Store.settle_awaiting). With a done when their answer isn't the result:
    it waits for that instead of closing, and the review reads their answer with the to-do's done when."""
    db.execute("UPDATE suggestions SET awaiting=? WHERE id=?",
               (encoded({**watch, 'delegated': False, 'answered': answer['title'][:150]}), row['id']))
    db.execute('INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               ('answered:' + row['id'], row['id'], 'update', f"{watch['name']} replied: {answer['title'][:150]} (signal {answer['id']})", 'assistant', stamp))
    return wait_for_result(db, row, watch.get('name'), stamp)


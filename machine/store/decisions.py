"""The Store's to-dos, part 2 (refactor PR 16): what happens to one. The owner's decisions (_decide, confirm_action,
snooze, handoffs, feedback, not done), preparing it (prepare, revise_draft, the preparation queue and its steps), sends
and merges with their undo. The helpers above the mixin hold the send lock and retry, handoff waits and how a reply
says it's handled. A mixin of Store (assistant.py), like App's mixins. Moved out of assistant.py as is."""
import datetime as dt
import hashlib
import json
import re
import sqlite3
import uuid

import abilities
import agent_jobs
import bug_gate
import chat_files
import doc_writes
import fleet
import follow_ups
import i18n
import locale_prefs
from machine.cards import (
    ask_blocked,
    blocker_questions,
    CHAT_STOPPED,
    current_title,
    handoff_checkin,
    looks_done,
    LOOKS_DONE_SQL,
    looks_done_at,
    outcome_state,
    snooze_time,
    title_kept,
)
from machine.config import LOG
from machine.store.cards import return_waiting, source_line
from machine.text import encoded, first_sentence, no_you
import next_actions
from machine.store import outcomes
from machine.store.review import intercom_handled
import skills
from timeutil import local_tz, now
import todo_areas


LOOKS_DONE_HOURS = 24  # how long a to-do looks done before it closes by itself (Store.close_looks_done)


NOTHING_SENT = re.compile(r'\s*Nothing (?:was |has been )?(?:sent|submitted|posted)(?: or (?:changed|submitted|posted|sent))?(?: yet)?\.?\s*$', re.I)


def settle_sent(store, db, suggestion_id, job_id, label='', note=None):
    """A ready card whose message went out, or whose final step went through, is done: it leaves
    Ready for you with one status, the sent note (2026-10-22). Not while another of its sends or final
    steps still waits, not for a handoff (that card waits for the reply) and not for a merge (it keeps
    Undo merge). The preparation's "Nothing sent." no longer holds and its needs-you outcome is answered. A to-do with
    a done when (outcomes.py) isn't done by the send: it waits for that result under Waiting on others."""
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or row['status'] != 'prepared':
        return False
    finished = {r[0] for r in db.execute("SELECT revision FROM action_jobs WHERE suggestion_id=? AND status IN ('sent','done')", (suggestion_id,))}
    waiting = [a for a in next_actions.visible_actions(row['next_action'])
               if a['kind'] in next_actions.APPROVE_KINDS + next_actions.FINISH_KINDS and a['revision'] not in finished]
    if waiting:
        return False
    body = NOTHING_SENT.sub('', row['body'] or '').strip() or row['body']
    db.execute('UPDATE suggestions SET body=?,outcome=NULL WHERE id=?', (body, suggestion_id))
    if 'done_when' in row.keys() and row['done_when']:
        # The owner's part went out, the result it is for hasn't come yet (outcomes.py): it waits for that, not done
        job = db.execute('SELECT payload FROM action_jobs WHERE id=?', (job_id,)).fetchone()
        try:
            sent = json.loads(job['payload']) if job else {}
        except (TypeError, ValueError):
            sent = {}
        outcomes.wait_for_result(db, row, str(sent.get('to_name') or '') if isinstance(sent, dict) else '', now())
        return True
    if checking_in(db, dict(row)):
        # The owner's check-in nudge went out while the teammate still has it: it waits on them again, under Later
        # until the next check-in, and their answer to the handoff still settles it (handoff_latest)
        until = handoff_checkin(bool(row['urgent']), row['due'])
        store._decide(db, suggestion_id, 'snooze', (note or (i18n.t('Sent: {}', label) if label else i18n.t('Sent')))[:200],
                      CHECKIN_SENT_PREFIX + job_id, 'assistant', snoozed_until=until)
        return True
    store._decide(db, suggestion_id, 'complete', (note or (i18n.t('Sent: {}', label) if label else i18n.t('Sent')))[:200], 'sent:' + job_id, 'assistant')
    return True


# A merged fix to The Machine can be undone this long; one it merged by itself undoes itself when
# its code version records an error within AUTO_UNDO_NEW, or the fault it fixed comes back.
UNDO_MERGE = dt.timedelta(hours=24)


AUTO_UNDO_NEW = dt.timedelta(hours=1)


# A message send whose outcome is unknown keeps its lock while the service checks the conversation
# (it never resends by itself). After this long with no sign of it, the owner may send it again.
SEND_RETRY_AFTER = dt.timedelta(minutes=30)


MESSAGE_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'signal', 'intercom', 'doc_reply')


def own_title(db, suggestion_id, title):
    """A handed-off to-do's title once it is the owner's own again (Do it myself): "Waiting on Sam: send the quote"
    becomes "Send the quote". From what was promised when the to-do came from someone else's promise; else the owner's
    language's own "Waiting on {}: {}", only for the teammate it went to. Anything else stays: None."""
    from machine.store.promises import fit_title, promise_title, promise_who_named, PROMISE_TITLE_MAX
    title = ' '.join(str(title or '').split())
    whos = {r['name'] for r in db.execute("SELECT name FROM fleet_out WHERE context=? AND name IS NOT NULL", ('handoff:' + str(suggestion_id),))}
    try:
        promise = db.execute("SELECT * FROM promises WHERE suggestion_id=? AND direction='theirs' ORDER BY id DESC LIMIT 1", (suggestion_id,)).fetchone()
    except sqlite3.OperationalError:  # no promises yet
        promise = None
    if promise:
        whos |= {promise['who'], promise_who_named(db, dict(promise))['who']}
    whos = {' '.join(str(w).split()) for w in whos} - {''}
    whos |= {w.split()[0] for w in whos}
    own = lambda what: fit_title(what[:1].upper() + what[1:], PROMISE_TITLE_MAX) if what else None
    if promise and promise['what']:
        what = ' '.join(str(promise['what']).split())
        if title in {promise_title(dict(promise), i18n.t('Waiting on {}: {}', w, what)) for w in whos}:
            return own(what)
    head, mid, tail = (i18n.t('Waiting on {}: {}', '\0', '\0').split('\0') + ['', ''])[:3]
    match = re.fullmatch(re.escape(head) + '(.+?)' + re.escape(mid) + '(.+)' + re.escape(tail), title)
    if match and match.group(1).casefold() in {w.casefold() for w in whos}:
        return own(match.group(2).strip())
    return None


def send_retry_ok(job, kind):
    """An unconfirmed message send the owner may retry: it was checked for SEND_RETRY_AFTER without a trace."""
    return (job['status'] == 'uncertain' and kind in MESSAGE_KINDS
            and job['updated_at'] <= (dt.datetime.fromisoformat(now()) - SEND_RETRY_AFTER).isoformat())


def send_lock(db, suggestion_id, revision, kind):
    """Why this draft can't be edited now, in plain words, or None. Only this draft's own attempts
    count: a reply already sent from the same card before it reopened with a new draft never blocks
    the new one. Another draft of the card that is going out right now does, for its short lock."""
    for job in db.execute('SELECT * FROM action_jobs WHERE suggestion_id=? ORDER BY updated_at DESC', (suggestion_id,)).fetchall():
        if job['revision'] == revision:
            if job['status'] == 'sent':
                at = locale_prefs.clock_text(dt.datetime.fromisoformat(job['updated_at']).astimezone(local_tz()))
                return f'Sent at {at}. This draft already went out.'
            if job['status'] == 'sending':
                return 'Sending… This draft is going out now.'
            if job['status'] == 'uncertain' and not send_retry_ok(job, kind):
                at = locale_prefs.clock_text((dt.datetime.fromisoformat(job['updated_at']) + SEND_RETRY_AFTER).astimezone(local_tz()))
                return f'I’m still checking whether the last attempt went out, so I won’t send it twice. If it isn’t there by {at}, you can try again.'
        elif job['status'] == 'sending' and (job['retry_at'] or '') > now():
            return 'Another draft on this to-do is sending right now. Try again in a minute.'
    return None


def skill_update_after(before, addition):
    """An older update from notes (no base_sha): what they taught, under the skill's instructions."""
    return before.rstrip() + '\n\n' + addition.strip()


def skill_update_view(db, cluster):
    """The before and after an Update would make, from the skill as it is now. None when the skill is gone."""
    row = db.execute("SELECT name,description,body,sha FROM skills WHERE id=? AND status IN ('on','off') AND origin!='shared'",
                     (cluster['target_id'],)).fetchone()
    if not row:
        return None
    after = cluster['body'] if cluster['base_sha'] else skill_update_after(row['body'], cluster['body'])
    return skills.update_view(cluster['id'], dict(row), after, cluster['base_sha'])


def note_first(db, name, kind, at=None):
    """A first-time milestone (first_prepared, first_verified_action) with its kind: kept once, never content."""
    db.execute('INSERT OR IGNORE INTO milestones(name,at,detail) VALUES(?,?,?)', (name, at or now(), kind))


NOT_TAKEN = "('failed','blocked','undone','needs_input','not_sent','retryable')"  # an action job that didn't take its step


def owner_area_open(db, suggestion_id):
    """Whether a to-do the owner added without an area is still unplaced (owner_card_area): no review, linked message
    or move put it anywhere. Returns its area ids then, else []."""
    row = db.execute('SELECT area,origin,event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or row['area'] or row['origin'] != 'owner':
        return []
    if db.execute('SELECT 1 FROM card_moves WHERE suggestion_id=? LIMIT 1', (suggestion_id,)).fetchone():
        return []
    for r in db.execute("SELECT e.metadata FROM events e JOIN json_each(?) j ON j.value=e.id WHERE e.kind='owner.card'", (row['event_ids'] or '[]',)):
        found = json.loads(r[0] or '{}').get('area_open')
        if isinstance(found, list) and found:
            return [str(x) for x in found]
    return []


def follows_sources(db, suggestion_id, area, accounts):
    """Whether a run's move to area happens by itself (Store.preparation_blocked): every message the to-do came from
    came in on that area (todo_areas.sources_area), so the move takes it where its sources already are, and nothing on
    it reaches anyone they did not already. Not for a to-do pinned Personal (its own life, never a Work Fleet's), nor
    once it has moved: the owner's own move stands, and after a move it made itself or an Undo the next one is theirs.
    A to-do made only from the Machine's own words (a routine's draft, MACHINE_OWN) has no messages from anyone: it
    goes where the account it needs is, since nothing on it reaches anyone new there."""
    row = db.execute('SELECT area,event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or row['area'] == todo_areas.PERSONAL:
        return False
    if db.execute('SELECT 1 FROM card_moves WHERE suggestion_id=? LIMIT 1', (suggestion_id,)).fetchone():
        return False
    rows = db.execute('SELECT e.account_id,e.kind FROM events e JOIN json_each(?) j ON j.value=e.id', (row['event_ids'] or '[]',)).fetchall()
    found = [r[0] for r in rows if r[1] not in MACHINE_OWN]
    if rows and not found:
        return True
    return bool(found) and todo_areas.sources_area(found, accounts) == area


MACHINE_OWN = ('routine.draft',)  # evidence the Machine wrote itself (routines_app.routine_draft_todo), from no one


def draft_saved(db, suggestion_id, action, at=None):
    """Note when each message draft first showed on the card (draft_saves): an assistant send needs the owner to have
    had it in front of them before they wrote the message that approves it (unseen_draft)."""
    for a in next_actions.actions(action) if action else []:
        if a.get('kind') in MESSAGE_KINDS and a.get('revision'):
            db.execute('INSERT OR IGNORE INTO draft_saves(suggestion_id,revision,saved_at) VALUES(?,?,?)', (suggestion_id, a['revision'], at or now()))


def reply_lead(db, suggestion_id, next_action):
    """The email a ready reply answers leads the to-do's evidence, so its source line and Read email open that one."""
    target = next((a['in_reply_to'] for a in next_actions.actions(next_action) if a.get('kind') == 'email' and a.get('in_reply_to')), None)
    row = target and db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row:
        return
    ids = json.loads(row['event_ids'] or '[]')
    rows = {r['id']: dict(r) for r in db.execute("SELECT e.* FROM events e JOIN json_each(?) ids ON ids.value=e.id", (row['event_ids'],))}
    lead = next((i for i in ids if i in rows and rows[i]['kind'] == 'gmail.message'
                 and str(json.loads(rows[i]['metadata'] or '{}').get('message-id') or '').strip() == target.strip()), None)
    if lead is None or ids[0] == lead:
        return
    ids = [lead] + [i for i in ids if i != lead]
    db.execute('UPDATE suggestions SET event_ids=?,source_line=? WHERE id=?', (encoded(ids), source_line([rows[i] for i in ids if i in rows]), suggestion_id))


ALREADY_HANDLED = re.compile(r"(?i)\balready (?:handled|done|did|sorted|taken care|replied|answered|paid|fixed|signed|reviewed|sent|booked|finished)"
                             r"|\b(?:handled|did|done|sorted|fixed|paid|signed|reviewed) (?:it |this |that )?(?:already|myself)\b"
                             r"|\btook care of (?:it|this|that)\b")


# A negative that applies to the completion itself ("haven't handled it", "didn't do it", "but I haven't"),
# not to the card ("Not needed — I already did it" is still completed work).
NEGATED_COMPLETION = re.compile(r"(?i)\b(?:no\s+longer|not|never|haven't|hadn't|hasn't|didn't|wasn't|isn't|won't|can't|cannot|couldn't|don't|doesn't)\s+"
                                # Up to four words ("think this is already handled"), never across a new statement.
                                r"(?:(?!(?:but|and|so|though|i)\b)\w+\s+){0,4}?(?:already\s+)?(?:handled?|done|did|do|sorted|fix(?:ed)?|finished|taken care|took care|sent|send|paid|pay|signed|sign|booked|reviewed)\b"
                                r"|\bi\s+(?:haven't|have not|didn't|did not|hadn't)\s*$")


def owner_reports_handled(text):
    """Explicit completed-work feedback, not a broad substring guess or an owner decision."""
    text = (text or '').replace('’', "'")
    clauses = [c for c in re.split(r'(?<=[.!?;\n,—–])|\s-\s', text) if c and c.strip()]
    if any(NEGATED_COMPLETION.search(c.strip(' .!;,—–\n')) for c in clauses):
        return False
    for clause in clauses:
        if clause.rstrip().endswith('?'):
            continue  # a question about it is not a report that it was done
        clause = clause.strip(' .!;,—–\n')
        if ALREADY_HANDLED.search(clause) or re.match(
                r"(?i)^\s*i(?: have|'ve)?\s+(?:already\s+)?(?:handled|did|done|sorted|fixed|paid|signed|reviewed|finished|booked|sent)\s+(?:it|this|that)\b(?!\s+(?:badly|poorly|partially|incompletely|yet)\b)",clause):
            return True
    return False


def pause_idle_steps(db, suggestion_id=None, stamp=None):
    """A confirmed step (a finish or a next preparation) is 'local_preparation' only while a preparation of its card is
    queued or running. When that preparation stops without saving a result (it is blocked, it timed out, a snooze or a
    close canceled it), the step is 'paused': still approved, nothing runs, so it never counts as active work. Try
    again, the end of a snooze, Undo or Reopen resume it (queue_preparation, and admission in preparation_step)."""
    return db.execute("""UPDATE action_jobs SET status='paused',updated_at=? WHERE status='local_preparation' AND (? IS NULL OR suggestion_id=?)
        AND NOT EXISTS(SELECT 1 FROM preparations p WHERE p.suggestion_id=action_jobs.suggestion_id AND p.status IN ('queued','starting','running'))""",
        (stamp or now(), suggestion_id, suggestion_id)).rowcount


def close_by_itself(db, row, decision_id, feedback, source, stamp, undo_hours, lapsed=False):
    """Close an open to-do without the owner: Done with Undo for undo_hours, its unfinished work stopped and its message
    redrawn. lapsed: it reads Not needed (expired_at), not done by them. Store.expire_passed, close_taken_intercom and
    plan_changed."""
    sid = row['id']
    prior_job = db.execute('SELECT job_id,status FROM preparations WHERE suggestion_id=?', (sid,)).fetchone()
    resume = row['resume_status'] if row['status'] == 'snoozed' else row['status']
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               (decision_id, sid, 'complete', feedback, source, stamp))
    db.execute("UPDATE suggestions SET status='completed',completed_from=?,closed_from=?,closed_decision_id=?,undo_until=?,closed_state=?,"
               'snoozed_until=NULL,resume_status=NULL,feedback_until=NULL' + (',expired_at=?' if lapsed else '') + ' WHERE id=?',
               (resume if resume in ('pending', 'accepted', 'prepared', 'instructions') else 'pending', row['status'], decision_id,
                (dt.datetime.fromisoformat(stamp) + dt.timedelta(hours=undo_hours)).isoformat(),
                encoded({**{k: row[k] for k in ('snoozed_until', 'resume_status')}, 'preparation': dict(prior_job) if prior_job else None}),
                *((stamp,) if lapsed else ()), sid))
    db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status!='done'", (stamp, sid))
    pause_idle_steps(db, sid)
    db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')", (stamp, sid))
    db.execute("UPDATE deliveries SET status='cancelled',reminder=0 WHERE suggestion_id=? AND status='queued'", (sid,))
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (sid,))


HANDOFFS = ("SELECT context,name,status,answer FROM fleet_out WHERE context IN (SELECT value FROM json_each(?)) AND kind='handoff' "
            "AND 'handoff_withdrawn:'||id NOT IN (SELECT key FROM fleet_meta WHERE key LIKE 'handoff_withdrawn:%') ORDER BY at DESC,rowid DESC")


def handoffs_of(db, ids):
    """{context: the newest handoff not taken back} of these to-dos, read once for a list (views.card_reads)."""
    out = {}
    for row in db.execute(HANDOFFS, (json.dumps(['handoff:' + str(i) for i in ids]),)):
        out.setdefault(row['context'], row)
    return out


def handoff_wait(db, suggestion, awake=False, handoffs=None):
    """A card under Later because it is with a teammate who hasn't answered its handoff yet: {'name': their first name}.
    Its time is when it comes back to check in with them, not a snooze of the owner's. awake: the same for a card that
    is back on the list (the check-in is due, or the owner brought it back) while the teammate still has it.
    handoffs: handoffs_of for a list of cards."""
    if suggestion.get('status') not in (('pending', 'accepted', 'prepared', 'instructions') if awake else ('snoozed',)):
        return None
    try:  # the newest handoff not taken back
        row = handoffs.get('handoff:' + str(suggestion['id'])) if handoffs is not None else \
            next(iter(handoffs_of(db, [suggestion['id']]).values()), None)
    except sqlite3.OperationalError:  # no Fleet on this Machine
        return None
    try:
        stage = (json.loads(row['answer'] or 'null') or {}).get('stage') if row else None
    except (ValueError, AttributeError):
        stage = None
    if not row or (stage or row['status']) not in ('asked', 'waiting'):
        return None
    return {'name': (str(row['name'] or '').split() or ['them'])[0]}


# Check in now on a to-do a teammate still has (machine/app/fleet.py handoff_checkin): the owner's ask for a nudge, and
# the to-do going back to wait on them once that nudge went out (settle_sent)
CHECKIN_PREFIX = 'handoff-checkin:'
CHECKIN_SENT_PREFIX = 'handoff-checkin-sent:'


def checking_in(db, suggestion):
    """A to-do working on, or showing, a check-in nudge to the teammate who still has it: open, not snoozed, and the
    owner's Check in now is newer than its handoff's wait (or the last check-in's send)."""
    if suggestion.get('status') not in ('accepted', 'instructions', 'prepared'):
        return False
    row = db.execute("SELECT id FROM decisions WHERE suggestion_id=? AND (id LIKE 'handoff-checkin%' OR id LIKE 'fleet-handoff-wait-%') "
                     'ORDER BY rowid DESC LIMIT 1', (suggestion['id'],)).fetchone()
    return bool(row and row['id'].startswith(CHECKIN_PREFIX)) and bool(handoff_wait(db, suggestion, awake=True))


def handoff_latest(db, suggestion_id):
    """The to-do's latest decision as a handoff's answer sees it: the owner's check-in (Check in now), the send of its
    nudge (its edits in the chat, its Send) and its wait after are no choice of theirs about the handoff, so the
    teammate's answer still settles it. Closing or reopening it is."""
    rows = db.execute('SELECT id,source,choice FROM decisions WHERE suggestion_id=? ORDER BY rowid DESC LIMIT 200', (suggestion_id,)).fetchall()
    handed = next((n for n, r in enumerate(rows) if r['source'] == 'fleet' and r['id'].startswith('fleet-handoff-')), len(rows))
    checks = [n for n, r in enumerate(rows[:handed]) if r['id'].startswith('handoff-checkin')]
    first = checks[-1] if checks else -1  # the first check-in since it was handed off: from there on, the check-ins' own
    return next((r for n, r in enumerate(rows) if n > first or r['choice'] in ('complete', 'reject', 'reopen', 'undo')), None)


def kept_steps(db, suggestion_id, job_id, action, do_now=False):
    """(action, kept): a run carrying out one step (a Confirm, or do_now) keeps the to-do's other waiting steps
    (next_actions.kept_steps), so it closes only when every step is done or the owner marks it done (2026-11-06)."""
    job = db.execute('SELECT action_id FROM preparations WHERE suggestion_id=? AND job_id=?', (suggestion_id, job_id)).fetchone()
    if not do_now and not (job and db.execute("SELECT 1 FROM action_jobs WHERE id=? AND status='local_preparation'", (job['action_id'],)).fetchone()):
        return action, []
    taken = {r[0] for r in db.execute(f"SELECT revision FROM action_jobs WHERE suggestion_id=? AND status NOT IN {NOT_TAKEN}", (suggestion_id,))}
    return next_actions.kept_steps(db.execute('SELECT next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()[0], action, taken)


def queue_preparation(db, suggestion_id, decision_id, action_id=None, resume_action=False):
    old = db.execute('SELECT * FROM preparations WHERE suggestion_id=?',(suggestion_id,)).fetchone()
    if old and old['status'] in ('queued','starting','running'):
        return
    session_job_id = old['session_job_id'] if old else None
    if resume_action and old:action_id=old['action_id']
    # New work replaces a confirmed final step that never saved its result. It may have
    # gone through already, so a later Confirm checks the source first, never resubmits blindly.
    for left in db.execute("SELECT id,status,payload FROM action_jobs WHERE suggestion_id=? AND status IN ('local_preparation','paused') AND id IS NOT ?",(suggestion_id,action_id)).fetchall():
        payload=json.loads(left['payload'])
        if payload['kind']!='finish':continue
        payload['finish_result']={'state':'uncertain','body':'Replaced by new work before its result was saved.','at':now(),'was':left['status']}
        db.execute("UPDATE action_jobs SET status='finish_uncertain',payload=?,updated_at=? WHERE id=?",(encoded(payload),now(),left['id']))
    db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,created_at,updated_at) VALUES(?,?,?,'queued',?,?) ON CONFLICT(suggestion_id) DO UPDATE SET decision_id=excluded.decision_id,job_id=excluded.job_id,status='queued',created_at=excluded.created_at,updated_at=excluded.updated_at,error=NULL,reason=NULL,details=NULL,questions=NULL,move_to=NULL,use_events=NULL,connect=NULL,started_at=NULL,retry_at=NULL,attempts=0,auto_retries=0",
               (suggestion_id,decision_id,uuid.uuid4().hex,now(),now()))
    db.execute('UPDATE preparations SET session_job_id=coalesce(?,job_id) WHERE suggestion_id=?',(session_job_id,suggestion_id))
    db.execute('UPDATE preparations SET action_id=? WHERE suggestion_id=?',(action_id,suggestion_id))
    if action_id:  # the same approved step carries on (Try again, the end of a snooze, Undo, Reopen)
        db.execute("UPDATE action_jobs SET status='local_preparation',updated_at=? WHERE id=? AND status='paused'",(now(),action_id))


def stop_chat(db, suggestion_id, job_id, text, via=None):
    """The chat's Stop: the card's current run ends now, kept as it was. Its preparation waits (blocked, error
    'stopped', so Try again or a new message carries on), any further tool call of the run is refused
    (preparation_state.tool_intent) and the worker aborts it in its session at once (stop_stale_runs). What it had
    said so far is kept for the chat, and where Stop was pressed (`via`: None the chat, 'browser' the Browser view).
    False when nothing was running any more."""
    db.execute('BEGIN IMMEDIATE')
    stamp = now()
    stopped = db.execute("UPDATE preparations SET status='blocked',reason=?,details=NULL,questions=NULL,error='stopped',retry_at=NULL,updated_at=? "
                         "WHERE suggestion_id=? AND job_id=? AND status IN ('queued','starting','running')",
                         (CHAT_STOPPED, stamp, suggestion_id, job_id)).rowcount
    if not stopped:
        return False
    db.execute('INSERT OR REPLACE INTO chat_stops(job_id,suggestion_id,text,at,via) VALUES(?,?,?,?,?)', (job_id, suggestion_id, text or '', stamp, via))
    pause_idle_steps(db, suggestion_id)
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
    return True


def skill_update_reviewed(db, suggestion_id, source, reviewed):
    """Update <skill> on a card from notes changes the owner's skill: only from the dashboard, after its before and
    after (reviewed names what was shown, skill_review_token). It keeps that version, so nothing else is applied."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='skill_clusters'").fetchone():
        return
    cluster = db.execute("SELECT c.* FROM skill_clusters c JOIN suggestions s ON s.id=c.suggestion_id WHERE c.suggestion_id=? "
                         "AND c.status IN ('pending','declined','failed') AND c.target_id IS NOT NULL AND s.status!='snoozed'", (suggestion_id,)).fetchone()
    if not cluster:
        return
    shown = skill_update_view(db, cluster)
    if not shown:
        raise ValueError('That skill is gone')
    if shown.get('stale'):
        raise ValueError(f"{shown['skill']} changed after this was suggested. Not now, or wait: the next check suggests it on the new version")
    if source != 'dashboard' or not reviewed:
        raise ValueError('Open it on the dashboard to see the before and after first')
    if reviewed != shown['review']:
        raise ValueError(f"{shown['skill']} changed since. Look at the before and after again")
    sha = db.execute('SELECT sha FROM skills WHERE id=?', (cluster['target_id'],)).fetchone()['sha']
    db.execute('UPDATE skill_clusters SET reviewed_sha=? WHERE id=?', (sha, cluster['id']))


def rewait_handoffs(db):
    """A card that came back early from a teammate's handoff, by an older check-in rule (an urgent card after 3 hours),
    while they still haven't answered and nothing else happened on it: back to Later until its check-in now."""
    try:
        rows = db.execute("SELECT s.id,s.urgent,s.due,d.created_at FROM suggestions s JOIN decisions d ON d.rowid="
                          "(SELECT MAX(rowid) FROM decisions WHERE suggestion_id=s.id) WHERE s.status='pending' "
                          "AND d.source='fleet' AND d.choice='snooze' AND d.id LIKE 'fleet-handoff-wait-%'").fetchall()
    except sqlite3.OperationalError:
        return 0
    moved = 0
    for row in rows:
        if not handoff_wait(db, {'id': row['id'], 'status': 'snoozed'}):
            continue  # answered, declined or gone: it is back for a reason
        try:
            until = handoff_checkin(bool(row['urgent']), row['due'], start=row['created_at'])
        except ValueError:
            continue
        if until > now():
            db.execute("UPDATE suggestions SET status='snoozed',snoozed_until=?,resume_status='pending' WHERE id=? AND status='pending'",
                       (until, row['id']))
            moved += 1
    return moved


def waiting_questions(db, row):
    """The questions a to-do waits on the owner's answer to, as its Needs you line asks them: those its stopped run
    named (ask_blocked), else its result's own question (needs_you ending in ?, with nothing to send). [] when it asks
    nothing. Same rule as ask_question() in machine/cards.py, from the stored rows."""
    if row['status'] in ('completed', 'rejected', 'snoozed') or row['handled_hint']:
        return []
    prep = db.execute('SELECT status,reason,error,questions FROM preparations WHERE suggestion_id=?', (row['id'],)).fetchone()
    view = {'preparation_status': prep['status'], 'preparation_reason': prep['reason'], 'preparation_error': prep['error'],
            'preparation_questions': prep['questions']} if prep else {}
    if ask_blocked(view):
        return [q['question'] for q in blocker_questions(view['preparation_questions'])]
    if row['status'] != 'prepared' or view.get('preparation_status') == 'blocked':
        return []
    if any(a.get('kind') != 'open' for a in next_actions.visible_actions(row['next_action'])):
        return []
    try:
        outcome = json.loads(row['outcome'] or '{}')
        question = ' '.join(str(outcome.get('needs') or '').split())
        return [question] if outcome.get('state') == 'needs_you' and question.endswith('?') else []
    except (ValueError, TypeError, AttributeError):
        return []


def bind_feedback_prompt(db, suggestion_id, request_id, message_id):
    db.execute("UPDATE feedback_prompts SET status='sent',message_id=?,error=NULL,updated_at=? WHERE request_id=? AND suggestion_id=?",
               (str(message_id),now(),request_id,suggestion_id))
    db.execute('UPDATE suggestions SET feedback_prompt_message_id=? WHERE id=? AND feedback_request_id=? AND feedback_until>?',
               (str(message_id),suggestion_id,request_id,now()))


def _not_done(db, row, feedback, decision_id, source):
    """Not done on a to-do that looked done (looks_done): it is a normal to-do again, and the decision (with what the
    hint or the run said) is what the next review and the learning pass read. A run's already_done result goes back to
    Needs your decision; nothing starts by itself."""
    if row['status'] in ('completed', 'rejected', 'snoozed') or not looks_done(dict(row)):
        if source == 'telegram':
            return {'status': row['status'], 'duplicate': True, 'skipped': True, 'reason': 'stale_not_done'}
        raise ValueError('This to-do no longer looks done')
    try:
        said = json.loads(row['handled_hint'] or 'null') or {}
    except ValueError:
        said = {}
    why = (said.get('reason') if isinstance(said, dict) else '') or first_sentence(row['body'])
    note = ' '.join(str(feedback or '').split()) or 'Not done yet. It looked done because: ' + why
    db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)', (decision_id, row['id'], 'not_done', note[:5000], source, now()))
    status = 'pending' if row['status'] == 'prepared' and outcome_state(row) == 'already_done' else row['status']
    db.execute("UPDATE suggestions SET handled_hint=NULL,status=?,outcome=CASE WHEN ?='pending' THEN NULL ELSE outcome END,undo_until=NULL WHERE id=?",
               (status, status, row['id']))
    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))
    return {'status': status, 'not_done': True}


class DecisionsStore:
    """Store methods for what the owner decides about a to-do and for preparing it."""

    def card_message_changed(self, suggestion_id):
        """A Claude Code or Codex job on the to-do started or ended: its Telegram message is edited to match
        (agent_jobs.shown_preparation: Working…, not Stuck, while it runs)."""
        with self.connect() as db:
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (str(suggestion_id),))

    def waiting_steps(self, suggestion_id, action, finish_state=None):
        """The steps in a result that still wait for the owner: a send, merge, calendar change, final click or handoff
        they haven't approved yet. One they already approved (an action job for that exact revision that didn't fail)
        or a final step this run carried out (finish_state:completed) is not waiting any more."""
        steps = [a for a in next_actions.actions(action) if a['kind'] in next_actions.WAITING_KINDS
                 and not (a['kind'] in next_actions.FINISH_KINDS and finish_state == 'completed')]
        if not steps:
            return []
        with self.connect() as db:
            taken = {r['revision'] for r in db.execute(f"SELECT revision FROM action_jobs WHERE suggestion_id=? AND status NOT IN {NOT_TAKEN}", (suggestion_id,))}
        return [a for a in steps if a.get('revision') not in taken]

    def kept_steps(self, suggestion_id, job_id, action, do_now=False):
        with self.connect() as db:
            return kept_steps(db, suggestion_id, job_id, action, do_now)

    def looks_handled(self, suggestion_id, reason, event_ids):
        """A later signal suggests an open card is already done. It looks done for a day, with Reopen, then closes by
        itself (close_looks_done). A to-do whose
        owner did their part and that waits for this result (outcomes.py) closes by itself, with Undo for a day."""
        reason = no_you(' '.join(str(reason or '').split()))  # an event line: never "You ..."
        if not 5 <= len(reason) <= 200 or not event_ids:
            raise ValueError('Give a short plain reason (5-200 characters) and the event_ids that show it')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown suggestion')
            if row['status'] in ('completed', 'rejected'):
                return {'skipped': 'already closed'}
            found = db.execute('SELECT count(*) FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in event_ids) + ')', event_ids).fetchone()[0]
            if found != len(set(event_ids)):
                raise ValueError('Every event must exist and be live')
            # The owner said Not done: only a signal that came in after that can say it is handled after all
            said = db.execute("SELECT max(created_at) FROM decisions WHERE suggestion_id=? AND choice='not_done'", (suggestion_id,)).fetchone()[0]
            newest = db.execute('SELECT max(ingested_at) FROM events WHERE id IN (' + ','.join('?' for _ in event_ids) + ')', event_ids).fetchone()[0]
            if said and (newest or '') <= said:
                return {'skipped': 'the owner said it is not done; only a newer signal can show otherwise'}
            if outcomes.result_seen(db, row, reason, event_ids, now()) == 'closed':
                return {'saved': True, 'closed': True, 'note': 'It waited for this result: it closed by itself, with Undo for a day.'}
        return {'saved': True}

    def bill_paid(self, suggestion_id, reason, event_ids, undo_hours=24):
        """A newer message shows an open bill to-do paid (the payee confirms the payment came in, a receipt for it, the
        debit went through): nothing is left to do, so it closes by itself as Done, "Closed by itself: <reason>", with
        Undo for a day (outcomes.close_handled), instead of looking done for a day first. Only on messages that came in
        after the to-do was made and after the owner's own last word on it; once per set of messages. Not while a send
        of it is under way. Anything else it can't say falls back to looks_handled."""
        reason = no_you(' '.join(str(reason or '').split()))  # an event line: never "You ..."
        ids = sorted({int(i) for i in event_ids or []})
        if not 5 <= len(reason) <= 200 or not ids:
            raise ValueError('Give a short plain reason (5-200 characters) and the event_ids that show it paid')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown suggestion')
            if row['status'] not in ('pending', 'accepted', 'instructions', 'prepared', 'snoozed'):
                return {'skipped': 'already closed'}
            marks = ','.join('?' * len(ids))
            found = db.execute(f'SELECT count(*),max(ingested_at) FROM events WHERE deleted=0 AND id IN ({marks})', ids).fetchone()
            if found[0] != len(ids):
                raise ValueError('Every event must exist and be live')
            newest = found[1] or ''
            said = db.execute("SELECT max(created_at) FROM decisions WHERE suggestion_id=? AND source IN ('dashboard','telegram')", (suggestion_id,)).fetchone()[0]
            decision_id = 'paid:' + hashlib.sha256(f'{suggestion_id}:{ids}'.encode()).hexdigest()[:32]
            if (newest > row['created_at'] and not (said and newest <= said)
                    and not db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone()
                    and not db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (suggestion_id,)).fetchone()):
                outcomes.close_handled(db, row, decision_id, reason, now(), undo_hours)
                db.execute('UPDATE suggestions SET handled_hint=NULL WHERE id=?', (suggestion_id,))
                return {'closed': True, 'note': 'Paid: it closed by itself, with Undo for a day.'}
        return self.looks_handled(suggestion_id, reason, ids)

    def plan_changed(self, suggestion_id, reason, event_ids, undo_hours=24):
        """A newer message overturned the plan an open to-do was built on (the party moved to another venue, the booking
        was dropped, they no longer need it): the to-do closes by itself as Not needed, its chat says "Updated: <reason>",
        with Undo for a day. Only on messages that came in after the to-do was made and after the owner's own last word on
        it; once per set of messages, so after the owner takes it back the same messages never close it again. Not while
        a send of theirs is under way."""
        reason = no_you(' '.join(str(reason or '').split()))  # an event line: never "You ..."
        ids = sorted({int(i) for i in event_ids or []})
        if not 5 <= len(reason) <= 200 or not ids:
            raise ValueError('Give a short plain reason (5-200 characters) and the event_ids of the newer messages')
        stamp = now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown suggestion')
            if row['status'] not in ('pending', 'accepted', 'instructions', 'prepared', 'snoozed'):
                return {'skipped': 'already closed'}
            marks = ','.join('?' * len(ids))
            found = db.execute(f'SELECT count(*),max(ingested_at) FROM events WHERE deleted=0 AND id IN ({marks})', ids).fetchone()
            if found[0] != len(ids):
                raise ValueError('Every event must exist and be live')
            newest = found[1] or ''
            if newest <= row['created_at']:
                return {'skipped': 'the to-do was made after these messages: update it with suggest and card_id instead'}
            said = db.execute("SELECT max(created_at) FROM decisions WHERE suggestion_id=? AND source IN ('dashboard','telegram')", (suggestion_id,)).fetchone()[0]
            if said and newest <= said:
                return {'skipped': 'the owner decided on it after these messages; their word stands'}
            decision_id = 'plan-changed:' + hashlib.sha256(f'{suggestion_id}:{ids}'.encode()).hexdigest()[:32]
            if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                return {'skipped': 'the owner took it back after these messages closed it'}
            if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (suggestion_id,)).fetchone():
                return {'skipped': 'a send of this to-do is under way'}
            close_by_itself(db, row, decision_id, reason, 'plan', stamp, undo_hours, lapsed=True)
        return {'closed': True}

    def queue_preparation(self, db, suggestion_id, decision_id, action_id=None, resume_action=False):
        return queue_preparation(db, suggestion_id, decision_id, action_id, resume_action)

    def routine_change_line(self, db, suggestion_id, name):
        """The to-do's chat line once its routine took the change its note taught (routine_changes.save): "Changed the
        routine X" (card_chat)."""
        db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   ('routine-change:' + uuid.uuid4().hex, suggestion_id, 'routine_change', name, 'dashboard', now()))

    def decide(self, suggestion_id, choice, feedback, decision_id, source, snooze_hours=24, snoozed_until=None, snooze_option=None, verified_terminal_job=None, work=False,
               reviewed=None, files=None):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if choice == 'accept':
                self.skill_update_reviewed(db, suggestion_id, source, reviewed)
            # Files added to a chat message go with it, in the same transaction, so its run always has them
            rows = chat_files.check(db, suggestion_id, files, decision_id) if files and choice == 'other' else []
            result = self._decide(db, suggestion_id, choice, feedback, decision_id, source,
                                  snooze_hours, snoozed_until, snooze_option, verified_terminal_job, work)
            if rows and not result.get('duplicate'):
                chat_files.bind(db, decision_id, rows)
            if choice in ('other', 'undo', 'reopen', 'retry', 'accept') and source in ('dashboard', 'telegram') and not result.get('duplicate') and \
                    db.execute("SELECT 1 FROM suggestions WHERE id=? AND status NOT IN ('completed','rejected')", (suggestion_id,)).fetchone():
                # The owner's word ("keep trying", Undo, Reopen) opens a skipped or stopped follow-up again (never one a hard fact closed)
                follow_ups.reopen(db, suggestion_id)
            return result

    def stop_chat(self, suggestion_id, job_id, text, via=None):
        with self.connect() as db:
            return stop_chat(db, suggestion_id, job_id, text, via)

    def skill_update_reviewed(self, db, suggestion_id, source, reviewed):
        return skill_update_reviewed(db, suggestion_id, source, reviewed)

    def wait_handoff(self, suggestion_id, feedback, decision_id, expected_decision):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            latest = db.execute('SELECT id FROM decisions WHERE suggestion_id=? ORDER BY rowid DESC LIMIT 1',
                                (suggestion_id,)).fetchone()
            if (latest['id'] if latest else None) != expected_decision:
                return {'skipped': True, 'reason': 'newer_card_choice'}
            card = db.execute('SELECT urgent,due FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            # Back to check in if they haven't answered: by the card's own deadline, else in 3 work days (handoff_checkin).
            until = handoff_checkin(bool(card['urgent']), card['due']) if card else None
            return self._decide(db, suggestion_id, 'snooze', feedback, decision_id, 'fleet', snoozed_until=until, work=True)

    def decide_handoff(self, suggestion_id, choice, feedback, decision_id, request_id):
        """Apply an answer only while this exact handoff still owns the card. Owner input wins, atomically."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            latest = handoff_latest(db, suggestion_id)  # a check-in the owner asked for meanwhile leaves it theirs to settle
            # Handed off, or taken on and waiting for the to-do's result (handoff_result_wait): their Done closes it
            if not latest or latest['source'] != 'fleet' or latest['id'] not in ('fleet-handoff-wait-' + request_id, 'fleet-handoff-result-' + request_id):
                return {'skipped': True, 'reason': 'newer_card_choice'}
            return self._decide(db, suggestion_id, choice, feedback, decision_id, 'fleet')

    def handoff_result_wait(self, suggestion_id, name, request_id):
        """A teammate's Machine took on a handoff (accepted, adjusted) whose to-do has a done when (outcomes.py): taking it on
        isn't the result, so the to-do waits for that under Waiting on others instead of closing, while this handoff still
        owns it. Their Done, or a signal with the result (looks_handled), closes it. True when it waits."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row or not row['done_when'] or row['status'] in ('completed', 'rejected'):
                return False
            latest = handoff_latest(db, suggestion_id)
            if not latest or latest['source'] != 'fleet' or latest['id'] not in ('fleet-handoff-wait-' + request_id, 'fleet-handoff-result-' + request_id):
                return False
            if latest['id'] == 'fleet-handoff-result-' + request_id:
                return True  # waiting already (an adjusted answer after accepted)
            # The wait's line is the fleet's, so this handoff still owns the to-do for their Done (decide_handoff)
            outcomes.wait_for_result(db, row, name, now(), 'fleet-handoff-result-' + request_id, 'fleet')
            return True

    def handoff_back(self, suggestion_id, decision_id, request_id, handed_at):
        """A teammate declined a handoff: the card comes back to Ready. From Later while this handoff still owns the card,
        or reopened when the owner's own last choice was to close it after handing it off (it was with them then).
        Any other later choice of the owner's wins."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                return {'skipped': True, 'reason': 'already_back'}
            latest = db.execute('SELECT id,source,choice,created_at FROM decisions WHERE suggestion_id=? ORDER BY rowid DESC LIMIT 1',
                                (suggestion_id,)).fetchone()
            card = db.execute('SELECT status FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not latest or not card:
                return {'skipped': True, 'reason': 'no_card'}
            own = handoff_latest(db, suggestion_id)  # waiting again after a check-in nudge went out: still this handoff's
            if card['status'] == 'snoozed' and own and own['source'] == 'fleet' and own['id'] == 'fleet-handoff-wait-' + request_id:
                return self._decide(db, suggestion_id, 'accept', '', decision_id, 'fleet')
            try:
                after = dt.datetime.fromisoformat(latest['created_at']) >= dt.datetime.fromisoformat(str(handed_at))
            except (TypeError, ValueError):
                after = False
            taken = db.execute('SELECT 1 FROM decisions WHERE id=?', ('fleet-handoff-' + request_id,)).fetchone()  # they took it on, it closed
            if card['status'] == 'completed' and latest['choice'] == 'complete' and latest['source'] in ('dashboard', 'telegram') and after and not taken:
                return self._decide(db, suggestion_id, 'reopen', '', decision_id, 'fleet')
            # they had taken it on (it closed with their answer), then said Not mine: back to the owner, while nothing newer came
            if card['status'] == 'completed' and latest['source'] == 'fleet' and latest['id'] == 'fleet-handoff-' + request_id:
                return self._decide(db, suggestion_id, 'reopen', '', decision_id, 'fleet')
            return {'skipped': True, 'reason': 'newer_card_choice'}

    def handoff_mine_card(self, suggestion_id):
        """Do it myself on a handoff that came back: the to-do is the owner's own now. Its prepared result no longer
        waits on the teammate (out of Waiting on others), the handoff step and the text about it go, and its title is its
        own (own_title), so it reads and acts as the owner's own to-do. The handoff's note stays (annotate_requests)."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT status,outcome,next_action,title,title_source FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row or row['status'] != 'prepared':
                return False
            title = own_title(db, suggestion_id, row['title']) if row['title_source'] != 'user' else None
            if title and title != row['title']:
                db.execute('UPDATE suggestions SET title=? WHERE id=?', (title, suggestion_id))
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
            try:
                outcome = json.loads(row['outcome'] or 'null')
            except (TypeError, ValueError):
                outcome = None
            waiting = isinstance(outcome, dict) and outcome.get('state') == 'waiting'
            try:
                current = json.loads(row['next_action'] or 'null')
            except (TypeError, ValueError):
                current = None
            kept = [a for a in next_actions.actions(current) if a.get('kind') != 'handoff'] if current else []
            dropped = bool(current) and len(kept) != len(next_actions.actions(current))
            if not waiting and not dropped:
                return bool(title and title != row['title'])
            action = (current if not dropped else {**current, 'actions': kept} if current.get('kind') == 'menu' and len(kept) > 1
                      else kept[0] if kept else None)
            # The prepared text described the handoff ("Prepared a short handoff to Sam"): it goes. With a draft of its
            # own left, that draft is still ready for the owner; else it is the owner's own step again, under Needs you,
            # with Mark done leading (owner_step) and nothing prepared to read.
            db.execute("UPDATE suggestions SET body='',outcome=?,next_action=?,status=?,owner_step=CASE WHEN ? THEN owner_step ELSE 1 END WHERE id=?",
                       (row['outcome'] if action and not waiting else None, encoded(action) if action else None, 'prepared' if action else 'pending',
                        1 if action else 0, suggestion_id))
            return True

    def _decide(self, db, suggestion_id, choice, feedback, decision_id, source, snooze_hours=24, snoozed_until=None, snooze_option=None, verified_terminal_job=None, work=False):
        # The caller owns one IMMEDIATE transaction, including any prompt validation.
        if choice not in ['accept', 'reject', 'snooze', 'other', 'complete', 'reopen', 'undo', 'retry', 'not_done'] or not decision_id:
            raise ValueError('Invalid decision')
        if choice == 'reopen' and source not in ('dashboard', 'fleet'):  # fleet: a declined handoff (handoff_back), never a request
            raise ValueError('Reopen is available only through the owner dashboard')
        if choice == 'other' and not feedback.strip():
            raise ValueError('Change requires written instructions')
        if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
            current = db.execute('SELECT status,snoozed_until FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
            return {'duplicate': True, **dict(current)}
        row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        if not row:
            raise ValueError('Unknown suggestion')
        if source in ('telegram', 'dashboard') and row['early']:
            db.execute('UPDATE suggestions SET early=0 WHERE id=?', (suggestion_id,))  # the owner's own decision from here on
        if choice == 'reject' and row['status'] in ('pending','accepted','instructions','prepared','snoozed') and owner_reports_handled(feedback):
            # "Not needed — I already did it" is a finished task, not a bad suggestion.
            choice = 'complete'
        if choice in ('undo', 'reopen') and row['done_report']:
            db.execute('UPDATE suggestions SET done_report=NULL WHERE id=?', (suggestion_id,))  # back in the list: nothing to report
        if choice == 'undo':
            if row['status'] not in ('completed','rejected') or not row['undo_until'] or row['undo_until'] <= now():
                # Older running bridges throw validation errors into the
                # ordered Telegram ingress queue, blocking later clicks.
                # A stale owner callback is a no-op, not a new decision.
                if source == 'telegram':
                    return {'status':row['status'],'duplicate':True,'skipped':True,'reason':'stale_undo'}
                raise ValueError('Undo has expired; use Reopen for a completed item')
            if not row['closed_decision_id'] or row['closed_decision_id'] != db.execute(
                    'SELECT id FROM decisions WHERE suggestion_id=? ORDER BY rowid DESC LIMIT 1', (suggestion_id,)).fetchone()[0]:
                if source == 'telegram':
                    return {'status':row['status'],'duplicate':True,'skipped':True,'reason':'stale_undo'}
                raise ValueError('A newer decision replaced this action')
            restored = row['closed_from'] or 'pending'
            db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',(decision_id,suggestion_id,choice,feedback[:5000],source,now()))
            previous=json.loads(row['closed_state'] or '{}')
            db.execute('UPDATE suggestions SET status=?,snoozed_until=?,resume_status=?,undo_until=NULL,feedback_until=NULL WHERE id=?',
                       (restored,previous.get('snoozed_until'),previous.get('resume_status'),suggestion_id))
            db.execute('UPDATE suggestions SET expires_at=NULL,expired_at=NULL WHERE id=? AND expired_at IS NOT NULL',(suggestion_id,))  # theirs now: it stays
            if str(row['closed_decision_id']).startswith(('handled:','looks-done:')):
                # It closed because it looked done: Undo says it isn't, like Not done, so it is a normal to-do again
                previous_state=outcome_state(dict(row))
                if restored=='prepared' and previous_state=='already_done':
                    restored='pending'
                db.execute("UPDATE suggestions SET handled_hint=NULL,status=?,outcome=CASE WHEN ?='pending' AND ?='already_done' THEN NULL ELSE outcome END WHERE id=?",
                           (restored,restored,previous_state or '',suggestion_id))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL',(suggestion_id,))
            prior=previous.get('preparation') or {}
            if restored in ('accepted','instructions') and prior.get('status') == 'blocked' and db.execute(
                    "UPDATE preparations SET status='blocked' WHERE suggestion_id=? AND job_id=? AND status='cancelled'",
                    (suggestion_id,prior.get('job_id'))).rowcount:
                pass  # back exactly as it was, waiting on the owner: Try again restarts it, Undo doesn't
            elif restored in ('accepted','instructions'):
                if prior.get('status') == 'queued':
                    # Resume custody of the same job, not another still-running
                    # preparation canceled only by the reversible owner close.
                    db.execute("UPDATE preparations SET status=? WHERE suggestion_id=? AND job_id=? AND status='cancelled'",
                               (prior['status'],suggestion_id,prior.get('job_id')))
                self.queue_preparation(db,suggestion_id,decision_id,resume_action=True)
            db.execute("UPDATE deliveries SET status='sent',reminder=0 WHERE suggestion_id=? AND status='cancelled' AND message_id IS NOT NULL",(suggestion_id,))
            # Restore a canceled original notification only if no card was ever sent.
            db.execute("UPDATE deliveries SET status='queued',reminder=? WHERE suggestion_id=? AND status='cancelled' AND message_id IS NULL",
                       (int(restored != 'pending'),suggestion_id))
            return {'status':restored,'undone':True}
        if choice == 'not_done':
            return self._not_done(db, row, feedback, decision_id, source)
        if choice == 'retry':
            job=db.execute('SELECT status,error,job_id FROM preparations WHERE suggestion_id=?',(suggestion_id,)).fetchone()
            ahead=row['status']=='pending' and job and job['status']=='blocked'  # a prepared-ahead run stuck on a blocker (settle_ahead)
            if row['status'] not in ('accepted','instructions') and not ahead or not job or job['status']!='blocked':
                if row['status'] in ('accepted','instructions','prepared') and job and job['status'] in ('queued','starting','running','done'):
                    # Already carrying on (its sign-in was seen, another device or a second tap was first) or done:
                    # this tap from a card drawn before that asks for what is already happening, so nothing to do.
                    return {'status':row['status'],'already':'done' if job['status']=='done' else 'running'}
                # Closed, snoozed or never started meanwhile: a stale tap, not an error (and never one in the ordered
                # Telegram ingress queue). The card redraws as it is now.
                return {'status':row['status'],'duplicate':True,'skipped':True,'reason':'stale_retry','already':'closed'}
            db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',(decision_id,suggestion_id,choice,feedback[:5000],source,now()))
            if ahead:  # Try again accepts it first: a run works only on an accepted to-do (preparation_state.tool_intent)
                db.execute("UPDATE suggestions SET status='accepted',undo_until=NULL WHERE id=?",(suggestion_id,))
            self.queue_preparation(db,suggestion_id,decision_id,resume_action=True)
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL',(suggestion_id,))
            return {'status':'accepted' if ahead else row['status'],'retrying':True}
        if row['status'] == 'completed':
            if choice == 'complete':
                return {'status': 'completed', 'duplicate': True}
            if choice != 'reopen':
                raise ValueError('This item is already done')
        if choice == 'reopen':
            if row['status'] != 'completed':
                if row['completed_from'] and row['status'] == row['completed_from']:
                    return {'status': row['status'], 'duplicate': True}
                raise ValueError('Only a completed item can be reopened')
            restored = row['completed_from'] or 'accepted'
            if restored not in ['pending','accepted','prepared','instructions']:
                restored = 'accepted'
            db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',
                       (decision_id,suggestion_id,choice,feedback[:5000],source,now()))
            db.execute('UPDATE suggestions SET status=?,completed_from=?,snoozed_until=NULL,resume_status=NULL,feedback_until=NULL,feedback_request_id=NULL,undo_until=NULL WHERE id=?',
                       (restored,restored,suggestion_id))
            db.execute('UPDATE suggestions SET expires_at=NULL,expired_at=NULL WHERE id=? AND expired_at IS NOT NULL',(suggestion_id,))
            if str(row['closed_decision_id']).startswith(('handled:','looks-done:')):  # it closed as looking done: it isn't
                if restored=='prepared' and outcome_state(dict(row))=='already_done':
                    restored='pending'
                    db.execute("UPDATE suggestions SET status='pending',completed_from='pending',outcome=NULL WHERE id=?",(suggestion_id,))
                db.execute('UPDATE suggestions SET handled_hint=NULL WHERE id=?',(suggestion_id,))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
            if restored in ('accepted','instructions'):
                self.queue_preparation(db,suggestion_id,decision_id,resume_action=True)
            # Reopen edits the existing card; it never sends another notification.
            return {'status':restored, 'note':'Back in Outstanding. Telegram will update too.'}
        # The owner may already have handled it without asking for preparation.
        if choice == 'complete' and row['status'] not in ['pending', 'accepted', 'instructions', 'prepared', 'snoozed']:
            raise ValueError('Mark done only an open item')
        status = {'accept': 'accepted', 'reject': 'rejected', 'snooze': 'snoozed', 'other': 'instructions', 'complete': 'completed'}[choice]
        until = snooze_time(snooze_option, snoozed_until, snooze_hours, work) if choice == 'snooze' else None
        resume = row['resume_status'] if row['status'] == 'snoozed' else row['status']
        if resume not in ['pending','accepted','prepared','instructions']:
            resume = 'pending'
        if choice == 'accept' and row['status'] == 'snoozed':
            status = resume
        # A note while the to-do waits on a question answers it: the question is kept beside the answer (decision_asks),
        # so the chat shows it as its own line and the run reads it as its question, never glued into the owner's words.
        asked = waiting_questions(db, row) if choice == 'other' else []
        db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',
                   (decision_id, suggestion_id, choice, feedback[:5000], source, now()))
        if asked:
            db.execute('INSERT OR IGNORE INTO decision_asks(decision_id,suggestion_id,questions,created_at) VALUES(?,?,?,?)',
                       (decision_id, suggestion_id, encoded(asked), now()))
        if choice == 'complete':
            db.execute('UPDATE suggestions SET completed_from=? WHERE id=?', (resume if row['status']=='snoozed' else row['status'],suggestion_id))
        if choice in ('complete','reject'):
            prior_job=db.execute('SELECT job_id,status FROM preparations WHERE suggestion_id=?',(suggestion_id,)).fetchone()
            db.execute('UPDATE suggestions SET closed_from=?,closed_decision_id=?,undo_until=?,closed_state=? WHERE id=?',
                       (row['status'],decision_id,(dt.datetime.fromisoformat(now())+dt.timedelta(minutes=5)).isoformat(),
                        encoded({**{k:row[k] for k in ('snoozed_until','resume_status')},'preparation':dict(prior_job) if prior_job else None}),suggestion_id))
        else:
            db.execute('UPDATE suggestions SET undo_until=NULL WHERE id=?',(suggestion_id,))
        db.execute('UPDATE suggestions SET status=?,snoozed_until=?,resume_status=?,feedback_until=NULL WHERE id=?', (status, until, resume if choice == 'snooze' else None, suggestion_id))
        db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')",(now(),suggestion_id))
        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
        cluster = db.execute("SELECT id FROM skill_clusters WHERE suggestion_id=? AND status IN ('pending','declined','failed')", (suggestion_id,)).fetchone()
        if cluster and choice in ('accept', 'reject', 'complete') and not (choice == 'accept' and row['status'] == 'snoozed'):  # Unsnooze isn't Create skill
            db.execute('UPDATE skill_clusters SET status=?,updated_at=? WHERE id=?', ('accepting' if choice == 'accept' else 'declined', now(), cluster['id']))
            if choice == 'accept':
                db.execute("UPDATE suggestions SET status='completed',completed_from='pending' WHERE id=?", (suggestion_id,))
                return {'status': 'completed', 'snoozed_until': None, 'note': 'Moving those notes into the skill.'}
        if status in ('accepted','instructions'):
            if choice == 'other':
                db.execute("UPDATE preparations SET status='cancelled' WHERE suggestion_id=?",(suggestion_id,))
            self.queue_preparation(db,suggestion_id,decision_id,resume_action=choice=='accept' and row['status']=='snoozed')
        elif status in ('completed','rejected','snoozed'):
            # Stop unfinished work; a finished preparation stays recorded as done. Its confirmed step waits, paused.
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status!='done'",(now(),suggestion_id))
            pause_idle_steps(db,suggestion_id)
        if choice in ['reject','complete']:
            db.execute("UPDATE deliveries SET status='cancelled',reminder=0 WHERE suggestion_id=? AND status='queued'",(suggestion_id,))
        return {'status': status, 'snoozed_until': until, 'note': 'Preference saved. Acceptance does not execute or authorize an unspecified external action.'}

    @staticmethod
    def move_moment(db, suggestion_id, at):
        """A to-do whose moment moved (its meeting was rescheduled or canceled) now closes by itself at `at`."""
        db.execute('UPDATE suggestions SET expires_at=? WHERE id=? AND expired_at IS NULL', (at, suggestion_id))

    def expire_passed(self, undo_hours=24):
        """To-dos whose whole point was a moment that has passed (a confirmation or reminder before a meeting: the review's
        expires_at) close by themselves: Done, "No longer needed", with Undo for a day. Not while a send of theirs is
        under way. Returns the closed ids."""
        stamp, closed = now(), []
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT * FROM suggestions WHERE expires_at IS NOT NULL AND expires_at<=? AND expired_at IS NULL "
                              "AND status IN ('pending','accepted','instructions','prepared','snoozed')", (stamp,)).fetchall()
            for row in rows:
                sid = row['id']
                if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (sid,)).fetchone():
                    continue  # a send on its way settles first
                close_by_itself(db, row, 'expired:' + uuid.uuid4().hex, 'No longer needed: its moment passed.', 'expiry', stamp, undo_hours, lapsed=True)
                closed.append(sid)
        return closed

    def close_taken_intercom(self, undo_hours=24):
        """Open to-dos made only from Intercom conversations that a teammate has since been assigned close by themselves: Done,
        "{name} took it in Intercom", with Undo for a day. Once per teammate: after an Undo it stays. Not while a send of
        theirs is under way. Returns the closed ids."""
        stamp, closed, owners = now(), [], {}
        with self.connect() as db:
            if not db.execute("SELECT 1 FROM events WHERE kind='intercom.conversation' LIMIT 1").fetchone():
                return closed  # no Intercom here: no write lock taken
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT s.* FROM suggestions s WHERE s.status IN ('pending','accepted','instructions','prepared','snoozed') "
                              "AND EXISTS(SELECT 1 FROM json_each(s.event_ids) j JOIN events e ON e.id=j.value WHERE e.kind='intercom.conversation')").fetchall()
            for row in rows:
                sid, ids = row['id'], json.loads(row['event_ids'] or '[]')
                events = db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids).fetchall() if ids else []
                if not events or any(e['kind'] != 'intercom.conversation' for e in events):
                    continue  # other evidence too (a mail, the owner's own words): theirs to judge
                taken = [a for a in self.intercom_assignments(db, events, owners).values() if isinstance(a, tuple)]
                if len(taken) != len(events):
                    continue
                decision_id = 'intercom-taken:' + hashlib.sha256(f"{sid}:{sorted(set(t[1] for t in taken))}:{sorted(json.loads(e['metadata']).get('admin_assignee_id') or '' for e in events)}".encode()).hexdigest()[:32]
                if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                    continue  # closed for this teammate before and the owner took it back
                if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (sid,)).fetchone():
                    continue  # a send on its way settles first
                close_by_itself(db, row, decision_id, taken[0][1], 'intercom', stamp, undo_hours)
                closed.append(sid)
        return closed

    def intercom_only(self, db, row):
        """The Intercom conversations a to-do was made from, when they are all its evidence (other evidence, a mail or the
        owner's own words, is theirs to judge): [event rows], else []."""
        ids = json.loads(row['event_ids'] or '[]')
        events = db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids).fetchall() if ids else []
        return events if events and all(e['kind'] == 'intercom.conversation' for e in events) else []

    def close_handled_intercom(self, undo_hours=24):
        """Open to-dos made only from Intercom conversations that Intercom shows handled since the to-do was made close by
        themselves: Done, "Closed in Intercom" or "Answered in Intercom" (by whom, when a teammate), with Undo for a day.
        Only for certain (review.intercom_handled): someone on the team closed it, or replied and the customer hasn't
        written since, and a reply is all the to-do asks. Never a note, a snooze, an assignment, a bot or Fin. Once per
        close or reply: after an Undo that one stays, a newer one closes it again. Not while a send of it is under way.
        The first run after an update is the one-time sweep (the sync rereads open to-dos' conversations once). Only
        reads, without a write lock, until one is found. Returns the closed ids."""
        stamp, found, owners = now(), [], {}
        with self.connect() as db:
            if not db.execute("SELECT 1 FROM events WHERE kind='intercom.conversation' LIMIT 1").fetchone():
                return []
            rows = db.execute("SELECT s.* FROM suggestions s WHERE s.status IN ('pending','accepted','instructions','prepared','snoozed') "
                              "AND EXISTS(SELECT 1 FROM json_each(s.event_ids) j JOIN events e ON e.id=j.value WHERE e.kind='intercom.conversation')").fetchall()
            for row in rows:
                events, facts = self.intercom_only(db, row), []
                for e in events:
                    if e['account_id'] not in owners:
                        owners[e['account_id']] = self.intercom_owner(db, e['account_id'])[0]
                    facts.append(intercom_handled(json.loads(e['metadata'] or '{}'), dict(row), owners[e['account_id']]))
                if not facts or not all(facts):
                    continue
                how = 'closed' if all(f[0] == 'closed' for f in facts) else 'answered'
                names = sorted({f[1] for f in facts})
                decision_id = f'intercom-{how}:' + hashlib.sha256(f"{row['id']}:{sorted((e['id'], f[2]) for e, f in zip(events, facts))}".encode()).hexdigest()[:32]
                found.append((row['id'], decision_id, names[0] if len(names) == 1 else ''))
        closed = []
        if not found:
            return closed
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for sid, decision_id, name in found:
                row = db.execute("SELECT * FROM suggestions WHERE id=? AND status IN ('pending','accepted','instructions','prepared','snoozed')", (sid,)).fetchone()
                if not row or db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                    continue  # closed already, or closed for this before and the owner took it back
                if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (sid,)).fetchone():
                    continue  # a send on its way settles first
                close_by_itself(db, row, decision_id, name, 'intercom', stamp, undo_hours)
                db.execute('UPDATE suggestions SET early=0 WHERE id=?', (sid,))
                closed.append(sid)
        if closed:
            LOG.info('intercom handled closed=%s', len(closed))
        return closed

    def intercom_rereads(self, account_id, limit=50):
        """The conversations of open to-dos in an Intercom account synced before handled_facts existed (no customer_at
        yet), newest first: the sync reads them again once (connectors/intercom.py)."""
        with self.connect() as db:
            rows = db.execute("SELECT DISTINCT e.source_id,e.metadata FROM suggestions s JOIN json_each(s.event_ids) j JOIN events e ON e.id=j.value "
                              "WHERE s.status IN ('pending','accepted','instructions','prepared','snoozed') AND e.kind='intercom.conversation' "
                              "AND e.account_id=? ORDER BY e.occurred_at DESC", (account_id,)).fetchall()
        wanted = []
        for r in rows:
            try:
                fresh = 'customer_at' in json.loads(r['metadata'] or '{}')
            except (ValueError, TypeError):
                fresh = False
            if not fresh and r['source_id'] not in wanted:
                wanted.append(r['source_id'])
        return wanted[:limit]

    def close_looks_done(self, hours=LOOKS_DONE_HOURS, undo_hours=24):
        """A to-do that has looked done (looks_done: a later signal showed it handled, or its run found it done) for
        `hours` without the owner taking it back closes by itself: Done, "Closed by itself: <what showed it>", with
        Undo for a day. So the list only holds what is really open, also on a Machine whose owner never goes through
        Looks done. Once per sign: after an Undo, Reopen or Not done that same sign never closes it again. Not while a
        send of it is under way. The first run after an update closes the ones that stood long enough already.
        Returns the closed ids."""
        stamp, closed = now(), []
        cutoff = (dt.datetime.fromisoformat(stamp) - dt.timedelta(hours=hours)).isoformat()
        with self.connect() as db:
            if not db.execute("SELECT 1 FROM suggestions WHERE status IN ('pending','accepted','instructions','prepared') AND "
                              + LOOKS_DONE_SQL + ' LIMIT 1').fetchone():
                return closed  # nothing looks done: no write lock taken
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT * FROM suggestions WHERE status IN ('pending','accepted','instructions','prepared') AND " + LOOKS_DONE_SQL).fetchall()
            for row in rows:
                row = dict(row)
                if not looks_done(row):
                    continue
                since = looks_done_at(db, row) or ''
                if not since or since > cutoff:
                    continue  # still fresh: the owner gets a day to say Not done
                decision_id = 'looks-done:' + hashlib.sha256(f"{row['id']}:{since}".encode()).hexdigest()[:32]
                if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                    continue
                # The owner's own word since that sign stands: theirs to close
                if db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND choice IN ('reopen','undo','not_done') AND created_at>=?",
                              (row['id'], since)).fetchone():
                    continue
                if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (row['id'],)).fetchone():
                    continue  # a send on its way settles first
                try:
                    said = json.loads(row.get('handled_hint') or 'null') or {}
                except ValueError:
                    said = {}
                why = ' '.join(str((said.get('reason') if isinstance(said, dict) else '') or first_sentence(row['body']) or '').split())[:200]
                close_by_itself(db, row, decision_id, why or i18n.t('Looks done'), 'handled', stamp, undo_hours)
                db.execute('UPDATE suggestions SET early=0 WHERE id=?', (row['id'],))
                closed.append(row['id'])
        if closed:
            LOG.info('looks done closed=%s', len(closed))
        return closed

    def close_handled(self, suggestion_id, reason, event_ids, undo_hours=24):
        """An open to-do that newer messages show done already (handled_check.py: someone was already asked or told,
        or answered) closes by itself: Done, "Closed by itself: <reason>", with Undo for a day. Once for the same
        messages: after an Undo it stays. Not while a send of its is under way. True when it closed."""
        stamp = now()
        decision_id = 'handled:' + hashlib.sha256(f"{suggestion_id}:{sorted(int(i) for i in event_ids)}".encode()).hexdigest()[:32]
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute("SELECT * FROM suggestions WHERE id=? AND status IN ('pending','accepted','instructions','prepared','snoozed')",
                             (suggestion_id,)).fetchone()
            if not row or db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                return False
            if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')", (suggestion_id,)).fetchone():
                return False  # a send on its way settles first
            prior_job = db.execute('SELECT job_id,status FROM preparations WHERE suggestion_id=?', (suggestion_id,)).fetchone()
            resume = row['resume_status'] if row['status'] == 'snoozed' else row['status']
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, suggestion_id, 'complete', ' '.join(str(reason or '').split())[:200], 'handled', stamp))
            db.execute("UPDATE suggestions SET status='completed',completed_from=?,closed_from=?,closed_decision_id=?,undo_until=?,closed_state=?,"
                       'snoozed_until=NULL,resume_status=NULL,feedback_until=NULL,early=0 WHERE id=?',
                       (resume if resume in ('pending', 'accepted', 'prepared', 'instructions') else 'pending', row['status'], decision_id,
                        (dt.datetime.fromisoformat(stamp) + dt.timedelta(hours=undo_hours)).isoformat(),
                        encoded({**{k: row[k] for k in ('snoozed_until', 'resume_status')}, 'preparation': dict(prior_job) if prior_job else None}), suggestion_id))
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status NOT IN ('done','cancelled')", (stamp, suggestion_id))
            pause_idle_steps(db, suggestion_id)
            db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')", (stamp, suggestion_id))
            db.execute("UPDATE deliveries SET status='cancelled',reminder=0 WHERE suggestion_id=? AND status='queued'", (suggestion_id,))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
        return True

    def wake_snoozed(self):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE message_id IS NOT NULL AND suggestion_id IN (SELECT id FROM suggestions WHERE undo_until<=?)',(now(),))
            db.execute('UPDATE suggestions SET undo_until=NULL WHERE undo_until<=?',(now(),))
            rows = db.execute("SELECT id,resume_status FROM suggestions WHERE status='snoozed' AND snoozed_until<=?",(now(),)).fetchall()
            for row in rows:
                status = row['resume_status'] if row['resume_status'] in ['pending','accepted','prepared','instructions'] else 'pending'
                db.execute('UPDATE suggestions SET status=?,snoozed_until=NULL,resume_status=NULL WHERE id=?',(status,row['id']))
                if status in ('accepted','instructions'):
                    self.queue_preparation(db,row['id'],'snooze-resumed:'+now(),resume_action=True)
                # Exactly one new outbox intent per elapsed snooze. An unknown
                # previous send must be reconciled, not blindly retried.
                db.execute("UPDATE deliveries SET status='queued',reminder=1,needs_edit=1 WHERE suggestion_id=? AND status IN ('sent','uncertain')",(row['id'],))
            return_waiting(db)  # those the review left waiting on someone else, when it is time to chase
            self.rewait_handoffs(db)
            return len(rows)

    def rewait_handoffs(self, db):
        return rewait_handoffs(db)

    def request_feedback(self, suggestion_id, request_id, after_message_id=None, card_message_id=None, managed=False, kind='change'):
        # kind 'dismiss': the next reply is the reason for dismissing, and dismisses the item.
        if kind not in ('change','dismiss'):
            raise ValueError('Unknown reply request')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT feedback_request_id,feedback_kind,status,feedback_until,feedback_prompt_message_id,feedback_card_message_id FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown suggestion')
            if row['status'] in ('completed','rejected') or (kind=='change' and row['status']=='snoozed'):
                raise ValueError('Change is available only on an outstanding item' if kind=='change' else 'This item is already closed')
            if row['feedback_request_id'] == request_id:
                return {'duplicate': True}
            if (row['feedback_until'] and row['feedback_until']>now() and (row['feedback_prompt_message_id'] or db.execute(
                    "SELECT 1 FROM feedback_prompts WHERE request_id=? AND status NOT IN ('cancelled')",(row['feedback_request_id'],)).fetchone())
                    and str(row['feedback_card_message_id'])==str(card_message_id) and (row['feedback_kind'] or 'change')==kind):
                return {'duplicate':True,'awaiting_feedback':True}  # Reuse an already-open confirmed prompt.
            # One clearly scoped next-reply request, persisted across Gateway restarts.
            db.execute('UPDATE suggestions SET feedback_until=NULL')
            started=now()
            until = (dt.datetime.fromisoformat(started) + dt.timedelta(minutes=10)).isoformat()
            db.execute('UPDATE suggestions SET feedback_until=?,feedback_request_id=?,feedback_requested_at=?,feedback_after_message_id=?,feedback_prompt_message_id=NULL,feedback_card_message_id=?,feedback_kind=? WHERE id=?',
                       (until, request_id, started, str(after_message_id) if after_message_id is not None else None, str(card_message_id) if card_message_id is not None else None, kind, suggestion_id))
            if managed:
                title=db.execute('SELECT title FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()[0]
                db.execute("INSERT OR IGNORE INTO feedback_prompts(request_id,suggestion_id,card_id,title,status,created_at,updated_at,kind) VALUES(?,?,?,?,'queued',?,?,?)",
                    (request_id,suggestion_id,str(card_message_id),title,started,started,kind))
        return {'awaiting_feedback': True}

    def feedback_reply(self, text, message_id, timestamp=None, reply_to_id=None):
        decision_id = 'telegram-reply:' + message_id
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old = db.execute('SELECT suggestion_id FROM decisions WHERE id=?', (decision_id,)).fetchone()
            if old:
                return {'handled': True, 'duplicate': True}
            row = db.execute('SELECT * FROM suggestions WHERE feedback_until>? ORDER BY feedback_until DESC LIMIT 1', (now(),)).fetchone()
            if not row or not text.strip() or text.startswith('/'):
                return {'handled': False}
            # Dispatch may be delayed behind agent work. Only a newer native
            # message can answer this request, never an older queued message.
            boundary=row['feedback_prompt_message_id'] or row['feedback_after_message_id']
            if row['feedback_card_message_id'] and not row['feedback_prompt_message_id']:
                return {'handled': False}  # Prompt send has no confirmed receipt yet.
            if not boundary or not str(message_id).isdigit() or not str(boundary).isdigit() or int(message_id)<=int(boundary):
                return {'handled': False}
            if timestamp is not None:
                received=float(timestamp)
                if received>10**12:received/=1000
                if int(received) < int(dt.datetime.fromisoformat(row['feedback_requested_at']).timestamp()):
                    return {'handled': False}
            if row['feedback_prompt_message_id'] and str(reply_to_id) != str(row['feedback_prompt_message_id']):
                return {'handled': False}  # Only an explicit reply to this Change prompt.
            if not row['feedback_prompt_message_id'] and reply_to_id is not None and str(reply_to_id) != str(row['feedback_card_message_id']):
                return {'handled': False}
            suggestion_id = row['id']
            if text.strip().lower() in ['cancel', 'stop', 'never mind', 'nevermind']:
                db.execute('UPDATE suggestions SET feedback_until=NULL WHERE id=?', (suggestion_id,))
                return {'handled': True, 'cancelled': True}
            if (row['feedback_kind'] or 'change') == 'dismiss':
                # Validate the prompt, save the decision and cancel work atomically.
                # A later owner choice waits for this commit and wins afterwards.
                result = self._decide(db, suggestion_id, 'reject', text, decision_id, 'telegram')
                return {**result, 'handled': True}
            else:
                # Keep selection and feedback commit in the same transaction: an
                # intervening Accept must not turn an unrelated chat into feedback.
                db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',
                           (decision_id, suggestion_id, 'other', text[:5000], 'telegram', now()))
                db.execute("UPDATE suggestions SET status='instructions',snoozed_until=NULL,feedback_until=NULL WHERE id=?", (suggestion_id,))
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
                db.execute("UPDATE preparations SET status='cancelled' WHERE suggestion_id=?",(suggestion_id,))
                self.queue_preparation(db,suggestion_id,decision_id)
                db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')",(now(),suggestion_id))
                # The existing card is the visible receipt. Do not send a second
                # Preparing card; the finished result queues its own notification.
        return {'status': 'instructions', 'handled': True}

    def bind_feedback_prompt(self, suggestion_id, request_id, message_id):
        with self.connect() as db:
            bind_feedback_prompt(db, suggestion_id, request_id, message_id)

    def _not_done(self, db, row, feedback, decision_id, source):
        return _not_done(db, row, feedback, decision_id, source)

    def prepare(self, suggestion_id, body, job_id=None, next_action=None, outcome=None, note_kind=None, require_note=False, finish_state=None, title=None, send_now=False):
        if not body.strip():
            raise ValueError('A concrete local preparation is required')
        if title is not None and title_kept(outcome, finish_state, send_now):
            title = None  # a result that only finishes it keeps the title; the result and status line say how it ended
        if title is not None:
            title = ' '.join(str(title).split())
            if not title or len(title) > 90:
                raise ValueError('title is the card\'s new short title, under 90 characters, or left out to keep the current one')
        if len(body) > 1000:
            raise ValueError('Keep the preparation short: at most 1000 characters. Put longer drafts in a local document, not a wall of Telegram text.')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            job=db.execute('SELECT * FROM preparations WHERE suggestion_id=?',(suggestion_id,)).fetchone()
            row = db.execute('SELECT status,body,next_action,title,title_source FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            action_json=encoded(next_action) if next_action else None
            if job_id and job and job['job_id']==job_id and job['status']=='done' and row and row['status']=='prepared' and row['body']==body and row['next_action']==action_json:
                return {'status':'prepared','replayed':True}
            if job_id and job and job['job_id']==job_id and job['status']=='done' and row and row['status']=='snoozed' and row['body']==body and (outcome or {}).get('state')=='snoozed':
                return {'status':'snoozed','replayed':True}
            if job and job['status'] in ('starting','running') and job_id != job['job_id']:
                raise ValueError('This preparation is owned by its already-running turn')
            if job_id and (not job or job['job_id'] != job_id or job['status'] not in ('starting','running')):
                raise ValueError('Preparation canceled or replaced by newer owner feedback')
            if not row or row['status'] not in ['accepted', 'instructions', 'prepared']:
                raise ValueError('Prepare only an owner-accepted suggestion or written instruction')
            if row['status'] == 'prepared' and row['body'] == body and row['next_action']==action_json:
                return {'status': 'prepared', 'replayed': True}
            if db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')",(suggestion_id,)).fetchone():
                raise ValueError('An earlier send is still being checked. Resolve that outcome before replacing its draft.')
            if job_id and (note_kind or require_note):
                self.tag_note(suggestion_id, note_kind, db)
            db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')",(now(),suggestion_id))
            chosen=db.execute("SELECT * FROM action_jobs WHERE id=? AND status='local_preparation'",(job['action_id'],)).fetchone() if job and job['action_id'] else None
            if chosen and json.loads(chosen['payload'])['kind']=='finish':
                state=finish_state or ('completed' if (outcome or {}).get('state')=='done' else 'uncertain')
                if state not in ('completed','not_performed','uncertain'):raise ValueError('finish_state is completed, not_performed or uncertain')
                payload=json.loads(chosen['payload']);payload['finish_result']={'state':state,'body':body,'at':now()}
                db.execute('UPDATE action_jobs SET status=?,payload=?,updated_at=? WHERE id=?',
                           ({'completed':'done','not_performed':'needs_input','uncertain':'finish_uncertain'}[state],encoded(payload),now(),chosen['id']))
            db.execute("UPDATE action_jobs SET status='done',updated_at=? WHERE suggestion_id=? AND status IN ('local_preparation','paused') AND json_extract(payload,'$.kind')='prepare'",(now(),suggestion_id))
            db.execute("UPDATE suggestions SET body=?,status='prepared',next_action=?,outcome=? WHERE id=?", (body[:5000],action_json,encoded(outcome) if outcome else None,suggestion_id))
            if (outcome or {}).get('state')!='snoozed':  # a result the owner can use (first_cards_report); a draft when there is something to approve
                note_first(db,'first_prepared','draft' if any(a['kind'] in next_actions.APPROVE_KINDS+next_actions.FINISH_KINDS for a in next_actions.visible_actions(action_json)) else 'result')
            if chosen and json.loads(chosen['payload'])['kind']=='finish' and state=='completed':
                note_first(db,'first_verified_action','finish')  # saved only with a verified receipt or changed state (PREPARATION.md)
            if title and current_title(row, title) != row['title']:
                db.execute('UPDATE suggestions SET title=? WHERE id=?', (title, suggestion_id))  # the new notification and the edited message carry it
            elif title and row['title_source'] == 'user':
                db.execute('UPDATE suggestions SET title_suggested=? WHERE id=?', (title[:300], suggestion_id))  # their title stays; Reset gets this one
            draft_saved(db,suggestion_id,next_action)
            reply_lead(db,suggestion_id,next_action)
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
            db.execute("UPDATE preparations SET status='done',updated_at=?,error=NULL,reason=NULL WHERE suggestion_id=?",(now(),suggestion_id))
            if (outcome or {}).get('state')=='snoozed':
                # "Remind me about this on Tuesday": the same snooze as the Snooze button. The card leaves
                # Ready for you and comes back (with its notification) then; nothing is notified now.
                done=self._decide(db,suggestion_id,'snooze','','snooze-ask:'+(job_id or uuid.uuid4().hex),'assistant',snoozed_until=outcome['until'])
                return {'status':'snoozed','snoozed_until':done['snoozed_until'],
                        'note':'Result saved and the card is snoozed until then. Do not also add an automation or reminder for it.'}
            # A new result is worth a notification, not only an invisible edit.
            db.execute("UPDATE deliveries SET status='queued',reminder=1,error=NULL WHERE suggestion_id=? AND status IN ('queued','sent','uncertain')",(suggestion_id,))
            # The confirmed final step went through (a verified receipt): like a sent message, the card is done.
            if chosen and json.loads(chosen['payload'])['kind']=='finish' and state=='completed' and settle_sent(self,db,suggestion_id,chosen['id'],json.loads(chosen['payload']).get('label','')):
                # The owner confirmed it and left it to run ("On it. I'll report back."): it never just leaves the list.
                # Just done shows it with its result until they saw it, and the phone hears of it (App.report_done).
                db.execute('UPDATE suggestions SET done_report=? WHERE id=?',(now(),suggestion_id))
                return {'status':'completed','reported':True,'note':'Result saved; the confirmed step went through, so the card is done.'}
        return {'status': 'prepared', 'note': 'Result saved. The service itself executed nothing.'}

    def review_body(self, suggestion_id, body):
        """An open to-do's text as the owner accepted it from a review (fleet_reviews.py): its plan or result, never a send."""
        with self.connect() as db:
            done = db.execute(f"UPDATE suggestions SET body=? WHERE id=? AND status IN ({','.join('?' * len(fleet.OPEN_CARD))})",
                              (str(body)[:5000], suggestion_id, *fleet.OPEN_CARD)).rowcount
        if not done:
            raise ValueError('This to-do is closed')
        return {'status': 'revised'}

    def revise_draft(self,suggestion_id,revision,source,subject=None,body=None,agent_job=None):
        # The owner edits a ready draft themselves: the edit replaces that draft under a new
        # revision, so Send always sends exactly what they last saw; the before/after teaches later drafts.
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if agent_job is not None:
                job = db.execute('SELECT * FROM agent_jobs WHERE id=?', (agent_job['id'],)).fetchone()
                if (not job or job['suggestion_id'] != suggestion_id or job['status'] not in ((*agent_jobs.ACTIVE, 'result') if job['place'] == 'remote' else agent_jobs.ACTIVE)
                        or job['turns'] != agent_job['turns'] or job['outcome'] is not None
                        or job['draft_revision'] != revision):
                    raise ValueError('This agent job stopped or the draft changed. Its result stays on the card without replacing the draft.')
            row=db.execute('SELECT * FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
            action=next_actions.selected(row['next_action'],revision) if row else None
            if not row or row['status']!='prepared' or not action or action['kind'] not in ('email','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply','finish'):
                raise ValueError('This draft changed or is no longer ready. Use its current buttons.')
            lock=send_lock(db,suggestion_id,revision,action['kind'])
            if lock:raise ValueError(lock)
            # A final step that ran, or whose outcome is still unknown, may already have gone out:
            # its text stays as confirmed, so a retry checks the source instead of posting other text.
            if action['kind']=='finish' and db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND revision=? AND status IN ('local_preparation','paused','finish_uncertain','done')",(suggestion_id,revision)).fetchone():
                raise ValueError('This step already ran or is being checked. Use its current buttons.')
            if action['kind']=='finish':subject=None
            revised=next_actions.revise(action,subject,body)
            if revised['revision']==revision:
                return {'status':'unchanged','revision':revision}
            current=json.loads(row['next_action'])
            if current.get('kind')=='menu':
                current['actions']=[revised if a.get('revision')==revision else a for a in current['actions']]
            else:
                current=revised
            stamp=now()
            db.execute('UPDATE suggestions SET next_action=? WHERE id=?',(encoded(current),suggestion_id))
            if agent_job is not None:
                db.execute('UPDATE agent_jobs SET draft_revision=? WHERE id=? AND turns=?', (revised['revision'], agent_job['id'], agent_job['turns']))
            draft_saved(db,suggestion_id,revised,stamp)
            db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND revision=? AND status IN ('queued','blocked')",(stamp,suggestion_id,revision))
            db.execute('INSERT INTO draft_edits(id,suggestion_id,old_revision,new_revision,kind,before_subject,before_body,after_subject,after_body,source,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                (uuid.uuid4().hex,suggestion_id,revision,revised['revision'],action['kind'],action.get('subject'),next_actions.draft_text(action),revised.get('subject'),next_actions.draft_text(revised),source,stamp))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL',(suggestion_id,))
        # The text as saved (an email gets a blank line before the name): the dashboard shows it before it sends
        return {'status':'revised','revision':revised['revision'],'body':next_actions.draft_text(revised),'subject':revised.get('subject')}

    def confirm_action(self,suggestion_id,revision,approval_id,source,recipients=None,sender=None,hold=None):
        # hold: seconds the send waits before the outbox takes it (a yes by voice: Undo in the chat meanwhile, undo_voice_send)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT * FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
            action=next_actions.selected(row['next_action'],revision) if row else None
            # A card closes once its send or final step went through (settle_sent), or waits for its result (outcomes.py):
            # a repeated tap is that same send.
            done=db.execute("SELECT status FROM action_jobs WHERE suggestion_id=? AND revision=? AND status IN ('sent','done')",(suggestion_id,revision)).fetchone() if row and (row['status']=='completed' or row['done_when']) else None
            if done:
                return {'status':done['status'],'duplicate':True}
            # A review to-do (fleet_reviews.py) never sends or acts for anyone: the review goes back to the one who asked.
            if row and str(row['dedupe_key']).startswith('fleet-review:'):
                raise ValueError('A review to-do never sends anything. Your review goes back to its owner, who sends it themselves.')
            if not row or row['status']!='prepared' or not action or action['kind'] not in ('email','linkedin','slack','x','whatsapp','telegram','signal','intercom','doc_reply','merge','prepare','finish','calendar','doc_write'):
                raise ValueError('This result changed or is no longer ready. Use its current buttons.')
            off=abilities.refuse(self.config,action.get('account_id'))  # its Can do things was turned off since the draft
            if off:raise ValueError(off)
            if action.get('to_options'):
                # The owner picked who gets it, only from the addresses the service found in the thread.
                if not isinstance(recipients,list) or not recipients or len(set(recipients))!=len(recipients) or not set(recipients)<=set(action['to_options']):
                    raise ValueError('Choose who gets this email from the addresses offered.')
                action={**{k:v for k,v in action.items() if k!='to_options'},'to':list(recipients)}
            elif recipients:
                raise ValueError('This draft already has its recipients.')
            if sender is not None:
                # The owner picked the From in the review, only from the addresses the draft offered (own_addresses.senders).
                options=[a.lower() for a in action.get('from_options') or ()] if action['kind']=='email' else []
                if not isinstance(sender,str) or sender.lower() not in options and sender.lower()!=str(action.get('from') or '').lower():
                    raise ValueError(i18n.t('Send it from one of the addresses offered.'))
                action={**action,'from':next((a for a in action.get('from_options') or () if a.lower()==sender.lower()),action['from'])}
            if action['kind'] in ('prepare','finish') and db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('sending','uncertain')",(suggestion_id,)).fetchone():
                raise ValueError('An earlier send is still being checked. Wait for that outcome before changing the result.')
            previous=db.execute('SELECT * FROM action_jobs WHERE suggestion_id=? AND revision=?',(suggestion_id,revision)).fetchone()
            if previous and action['kind'] in ('prepare','finish') and previous['status'] in ('needs_input','finish_uncertain','cancelled','failed','blocked','paused') and previous['approval_id']!=approval_id:
                # The same approved step resumes, not a new operation. An unknown outcome
                # starts with reconciliation of that exact step, never a blind new submission.
                db.execute("UPDATE action_jobs SET status='local_preparation',approval_id=?,source=?,updated_at=? WHERE id=?",(approval_id,source,now(),previous['id']))
                db.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?)',(approval_id,suggestion_id,'prepare_next' if action['kind']=='prepare' else 'send','',source,now()))
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=?",(suggestion_id,))
                self.queue_preparation(db,suggestion_id,approval_id,action_id=previous['id'])
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(suggestion_id,))
                return {'status':'queued'}
            if previous and previous['status']=='done' and action['kind']=='prepare' and previous['approval_id']!=approval_id:
                db.execute('DELETE FROM action_jobs WHERE id=?',(previous['id'],));previous=None
            if previous:
                # Repeated clicks/retries never create a second send, including an
                # unknown outcome. A blocked pre-send permission check may be retried.
                # So may an unconfirmed message send after SEND_RETRY_AFTER without a trace: only on the owner's new tap.
                if (previous['status'] in ('blocked','cancelled','failed') or send_retry_ok(previous,action['kind'])) and previous['approval_id']!=approval_id:
                    db.execute("UPDATE action_jobs SET status='queued',retry_at=?,error=NULL,updated_at=?,approval_id=?,source=?,payload=? WHERE id=?",
                               ((dt.datetime.fromisoformat(now())+dt.timedelta(seconds=hold)).isoformat() if hold else None,now(),approval_id,source,encoded(action),previous['id']))
                    follow_ups.queued(db,suggestion_id,previous['id'],action,now())  # an automated follow-up: spaced with its batch
                    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                        (approval_id,suggestion_id,'send','',source,now()))
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(suggestion_id,))
                return {'status':previous['status'],'duplicate':True}
            job_id=uuid.uuid4().hex;stamp=now()
            db.execute('INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id,retry_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                (job_id,suggestion_id,revision,encoded(action),'local_preparation' if action['kind'] in ('prepare','finish') else 'queued',stamp,stamp,approval_id,source,
                 '<assistant-'+job_id+'@'+action['from'].split('@')[1]+'>' if action['kind']=='email' else '',
                 (dt.datetime.fromisoformat(stamp)+dt.timedelta(seconds=hold)).isoformat() if hold else None))
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                (approval_id,suggestion_id,'prepare_next' if action['kind']=='prepare' else 'send','',source,stamp))
            if action['kind'] not in ('prepare','finish'):follow_ups.queued(db,suggestion_id,job_id,action,stamp)  # an automated follow-up: spaced with its batch
            if source in ('telegram','dashboard'):db.execute('UPDATE suggestions SET early=0 WHERE id=?',(suggestion_id,))
            if action['kind'] in ('prepare','finish'):
                # A local turn: a next preparation, or the final step the owner just confirmed.
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=?",(suggestion_id,))
                db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')",(stamp,suggestion_id))
                self.queue_preparation(db,suggestion_id,approval_id,action_id=job_id)
            db.execute('UPDATE suggestions SET feedback_until=NULL WHERE id=?',(suggestion_id,))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(suggestion_id,))
        return {'status':'queued'}

    def undo_voice_send(self, suggestion_id, approval_id):
        """Undo in the chat on a send approved by voice: it is canceled while it still waits (confirm_action's hold)."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            job=db.execute("SELECT id,status,retry_at FROM action_jobs WHERE suggestion_id=? AND approval_id=? AND source='voice'",(str(suggestion_id or ''),str(approval_id or ''))).fetchone()
            if not job:
                raise ValueError('Nothing to undo.')
            if job['status']=='cancelled':
                return {'status':'cancelled'}
            if job['status']!='queued' or not job['retry_at'] or job['retry_at']<=now():
                raise ValueError('It’s already on its way.')
            db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE id=?",(now(),job['id']))
        return {'status':'cancelled'}

    def make_new_docs(self, suggestion_id):
        """A new doc the result asks for is made right away, while it is prepared: a private doc in the owner's own Google
        Drive or OneDrive that nobody else sees until they share it. Nothing goes to anyone, so it needs no OK, and the
        to-do shows its link (2026-11-03: "need to give approval to create a doc first while the skill says to make one").
        Sharing it and any edit to an existing doc still wait for the owner's OK. One per title: a second doc with the
        same title on this to-do waits for the owner. Returns the revisions queued."""
        with self.connect() as db:
            row = db.execute('SELECT status,next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row or row['status'] != 'prepared' or not row['next_action']:
                return []
            made = set()
            for job in db.execute("SELECT payload FROM action_jobs WHERE suggestion_id=? AND status NOT IN ('failed','blocked','cancelled')",
                                  (suggestion_id,)):
                try:
                    done = json.loads(job['payload'])
                except (TypeError, ValueError):
                    continue
                if done.get('kind') == doc_writes.KIND and done.get('op') == 'create':
                    made.add(str(done.get('title') or '').strip().lower())
            wanted = [a for a in next_actions.visible_actions(row['next_action'])
                      if a['kind'] == doc_writes.KIND and a.get('op') == 'create' and str(a.get('title') or '').strip().lower() not in made]
        queued = []
        for item in wanted:
            try:
                self.confirm_action(suggestion_id, item['revision'], doc_writes.NEW_DOC + uuid.uuid4().hex, 'assistant')
            except ValueError:
                continue
            queued.append(item['revision'])
        return queued

    def auto_merge(self, suggestion_id, config):
        """Queue a fix to The Machine's own error for merging without the owner's tap, when it is small, safe and shown
        to fix a bug (next_actions.unsafe_merge, bug_gate.unsafe) and no other merge happened in the last day; a second bug check runs
        before it merges (bug_gate.second_check). Returns why
        not, or None once queued; Merge now still works if the checks stop it."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT * FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
            merges=[a for a in next_actions.visible_actions(row['next_action']) if a['kind']=='merge'] if row and row['status']=='prepared' else []
            if len(merges)!=1:return 'no single fix to merge'
            action=merges[0]
            fault_info=next((json.loads(e['metadata']) for e in db.execute(
                "SELECT e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='machine.fault'",(row['event_ids'],))),None)
            fault=fault_info.get('fingerprint') if fault_info else None
            if not fault:return 'it does not fix one of The Machine’s recorded errors'
            if fault_info.get('outside'):return 'the error came from an outside service, not The Machine’s code'
            reason=next_actions.unsafe_merge(action,config) or bug_gate.unsafe(action)  # small and safe, and shown to fix a bug
            if reason:return reason
            since=(dt.datetime.fromisoformat(now())-UNDO_MERGE).isoformat()
            if db.execute("SELECT 1 FROM action_jobs WHERE json_extract(payload,'$.kind')='merge' AND (status IN ('queued','sending','uncertain','undoing') OR (status='sent' AND updated_at>=?))",(since,)).fetchone():
                return 'another merge happened in the last day'
            if db.execute('SELECT 1 FROM action_jobs WHERE suggestion_id=? AND revision=?',(suggestion_id,action['revision'])).fetchone():
                return 'this fix was already handled'
            job_id=uuid.uuid4().hex;stamp=now()
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) VALUES(?,?,?,?,'queued',?,?,?,'auto','')",
                       (job_id,suggestion_id,action['revision'],encoded({**action,'auto':True,'problem':row['title'],'fault':fault,'fault_kind':fault_info.get('fault_kind'),'fault_frames':fault_info.get('frames',[])}),stamp,stamp,'auto-merge:'+job_id))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(suggestion_id,))
        return None

    def undo_merge(self, suggestion_id, approval_id, source, reason=None):
        """Queue the undo of a merged fix (the owner's Undo, or The Machine's own when the fix misbehaves)."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            since=(dt.datetime.fromisoformat(now())-UNDO_MERGE).isoformat()
            job=db.execute("SELECT * FROM action_jobs WHERE suggestion_id=? AND json_extract(payload,'$.kind')='merge' AND status IN ('sent','undoing','undone') ORDER BY updated_at DESC LIMIT 1",(suggestion_id,)).fetchone()
            if job and job['status'] in ('undoing','undone'):return {'status':job['status'],'duplicate':True}
            if not job or job['updated_at']<since:raise ValueError('There is no merged fix to undo here (Undo lasts 24 hours).')
            db.execute("UPDATE action_jobs SET status='undoing',error=?,retry_at=NULL WHERE id=?",(reason,job['id']))  # updated_at stays the merge time
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',(approval_id,suggestion_id,'undo_merge',reason or '',source,now()))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(suggestion_id,))
        return {'status':'undoing'}

    def misbehaving_merges(self):
        """Fixes merged by themselves that their own code version contradicts: the fault they fixed came
        back, or a new error within the first hour."""
        found=[]
        with self.connect() as db:
            since=(dt.datetime.fromisoformat(now())-UNDO_MERGE).isoformat()
            # Once per fix: an undo that failed is not retried by itself.
            for job in db.execute("SELECT * FROM action_jobs j WHERE status='sent' AND approval_id LIKE 'auto-merge:%' AND updated_at>=? AND NOT EXISTS("
                                  "SELECT 1 FROM decisions d WHERE d.suggestion_id=j.suggestion_id AND d.choice='undo_merge' AND d.created_at>=j.updated_at)",(since,)).fetchall():
                action=json.loads(job['payload']);version=action['head'][:12]
                early=(dt.datetime.fromisoformat(job['updated_at'])+AUTO_UNDO_NEW).isoformat()
                back=db.execute('SELECT kind FROM fault_versions WHERE version=? AND fingerprint=? AND last_at>=?',(version,action.get('fault'),job['updated_at'])).fetchone()
                new=db.execute('SELECT kind FROM fault_versions WHERE version=? AND first_at>=? AND first_at<=? ORDER BY first_at LIMIT 1',(version,job['updated_at'],early)).fetchone()
                if back:found.append((job['suggestion_id'],f"The error it fixed ({back['kind']}) came back, so I undid the merge."))
                elif new:found.append((job['suggestion_id'],f"A new error ({new['kind']}) showed up right after the merge, so I undid it."))
        return found

    def resume_connected(self):
        """To-dos whose run stopped for a source that wasn't connected (preparation_blocked connect) carry on by themselves
        once it is: no Try again to find. Returns the to-dos it started again."""
        have = {a.get('service', 'gmail') for a in getattr(self, 'accounts', None) or []}
        with self.connect() as db:
            waiting = [dict(r) for r in db.execute("SELECT suggestion_id,job_id,connect FROM preparations "
                                                   "WHERE status='blocked' AND error IS NULL AND connect IS NOT NULL").fetchall()]
        resumed = []
        for job in waiting:
            if job['connect'] not in have:
                continue
            try:
                self.decide(job['suggestion_id'], 'retry', '', 'connected:' + job['job_id'], 'connected')
                resumed.append(job['suggestion_id'])
            except ValueError as error:  # closed, snoozed or already started again in the meantime
                LOG.info('connect resume skipped suggestion=%s error=%s', job['suggestion_id'], error)
        return resumed

    def redraft_intercom_emails(self):
        """An open to-do whose reply was drafted as an email because Intercom couldn't reply here (next_actions
        INTERCOM_FALLBACK: shared to read only, replies off, not connected) is drafted again, once, when its conversation's
        Intercom can reply now (the owner signed in with Intercom themselves). Its text and draft are written anew, so it no
        longer says Intercom can't; the new reply waits for the owner's Send like any draft. Returns the to-dos it started."""
        repliable = {a['id'] for a in getattr(self, 'accounts', None) or [] if a.get('service') == 'intercom' and next_actions.intercom_replies_on(a)}
        if not repliable:
            return []
        started = []
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT s.id,s.next_action,s.account_ids FROM suggestions s JOIN preparations p ON p.suggestion_id=s.id "
                              "WHERE s.status IN ('prepared','accepted') AND p.status='done' AND s.next_action IS NOT NULL "
                              "AND NOT EXISTS(SELECT 1 FROM decisions d WHERE d.id='intercom-replies:'||s.id) "
                              "AND NOT EXISTS(SELECT 1 FROM action_jobs j WHERE j.suggestion_id=s.id AND j.status NOT IN ('cancelled','rejected'))").fetchall()
            for row in rows:
                try:
                    choices, accounts = next_actions.actions(row['next_action']), set(json.loads(row['account_ids'] or '[]'))
                except (ValueError, TypeError):
                    continue
                if not accounts & repliable or not any(a.get('kind') == 'email' and a.get('intercom_fallback') for a in choices):
                    continue
                decision_id = 'intercom-replies:' + row['id']
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision_id, row['id'], 'prepare_ahead', '', 'intercom_replies', now()))
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=?", (row['id'],))
                db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status='done'", (now(), row['id']))
                self.queue_preparation(db, row['id'], decision_id)
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))
                started.append(row['id'])
            db.execute('COMMIT')
        for sid in started:
            LOG.info('intercom replies on: drafting again suggestion=%s', sid)
        return started

    def preparation_blocked(self, suggestion_id, job_id, reason, details=None, note_kind=None, questions=None, move_to=None, use_event_ids=None,
                            connect=None):
        """A run that can't go on. move_to: it needs the to-do in another of the owner's areas (todo_areas.py), such as Work
        to send from the company's mailbox. The to-do offers the move for the owner's tap (move_card), and carries on after
        it; it moves by itself when the owner added it without an area (owner_area_open) or the messages it came from are
        all in that area, or it came from no one's (a routine's draft) (follows_sources). use_event_ids: collected messages from another area it needs (up to 5, not
        its own sources already): the to-do offers "Use this email for this to-do" (use_sources), and carries on after it.
        connect: a source it needs that isn't connected (slack, gmail…): the to-do offers Connect Slack, which opens it in
        Connections, and carries on by itself once it is connected (resume_connected); Try again stays in its menu.
        Refused for one that is connected: the run reads it through that connection."""
        if not reason.strip() or len(reason)>400:
            raise ValueError('Give a short, specific blocker')
        if details is not None and (not isinstance(details,str) or len(details)>2000):
            raise ValueError('Keep blocker details under 2000 characters')
        if connect is not None:
            if move_to is not None or use_event_ids is not None:
                raise ValueError('Give connect, move_to or use_event_ids, one of them')
            if not isinstance(connect,str) or not re.fullmatch(r'[a-z][a-z0-9_]{1,30}',connect) or connect=='gateway':
                raise ValueError("connect: the source to connect, as Connections names it (slack, gmail, outlook, whatsapp…)")
            if any(a.get('service','gmail')==connect for a in getattr(self,'accounts',None) or []):
                raise ValueError(f'connect: {connect} is connected already. Read it through that connection'
                                 +(' (assistant_signals slack_read {channel})' if connect=='slack' else '')+', never the browser.')
        questions = blocker_questions(questions, strict=True)
        with self.connect() as db:
            job=db.execute('SELECT * FROM preparations WHERE suggestion_id=?',(suggestion_id,)).fetchone()
            if not job or job['job_id']!=job_id or job['status'] not in ('starting','running'):
                raise ValueError('Preparation canceled or replaced')
            if use_event_ids is not None:
                if move_to is not None:
                    raise ValueError('Give move_to or use_event_ids, not both')
                ids=use_event_ids
                if not isinstance(ids,list) or not 1<=len(ids)<=5 or not all(isinstance(i,int) and not isinstance(i,bool) for i in ids) or len(set(ids))!=len(ids):
                    raise ValueError('use_event_ids: one to five event ids of collected messages')
                card=db.execute('SELECT event_ids FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
                if set(ids)&set(json.loads(card['event_ids'] or '[]') if card else []):
                    raise ValueError('use_event_ids: its own sources are yours to read already; name only other messages')
                if len(db.execute('SELECT id FROM events WHERE deleted=0 AND id IN ('+','.join('?'*len(ids))+')',ids).fetchall())!=len(ids):
                    raise ValueError('use_event_ids: every one must be a collected, live message')
                use_event_ids=encoded(ids)
            if move_to is not None:
                card=db.execute('SELECT account_ids FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
                try:
                    todo_areas.check(move_to,card['account_ids'] if card else '[]',getattr(self,'accounts',None) or [])
                except ValueError as error:
                    raise ValueError(f"move_to: {error}. The owner's areas: "+', '.join(a['id'] for a in todo_areas.areas(getattr(self,'accounts',None) or [])))
            if note_kind:
                self.tag_note(suggestion_id, note_kind, db)
            # An empty list says the run asks nothing (ask_blocked); NULL is a blocker from before runs named questions.
            db.execute("UPDATE preparations SET status='blocked',reason=?,details=?,questions=?,move_to=?,use_events=?,connect=?,updated_at=? WHERE suggestion_id=?",
                       (reason,(details or '').strip() or None,encoded(questions),move_to,use_event_ids,connect,now(),suggestion_id))
            pause_idle_steps(db,suggestion_id)  # nothing runs now: its confirmed step waits for Try again or an answer
            # It moves itself (no tap) when the owner added it without an area and nothing placed it yet (the run found where
            # it belongs), or when the messages it came from are all in that area or it has none, only the Machine's own
            # words, as a routine's draft (follows_sources)
            unplaced=move_to is not None and move_to in owner_area_open(db,suggestion_id)
            sourced=move_to is not None and not unplaced and follows_sources(db,suggestion_id,move_to,getattr(self,'accounts',None) or [])
            if not (unplaced or sourced):
                db.execute("UPDATE deliveries SET status='queued',reminder=1,needs_edit=1,error=NULL WHERE suggestion_id=? AND status IN ('queued','sent','uncertain')",(suggestion_id,))
        if unplaced or sourced:
            try:
                moved=self.move_card(suggestion_id,move_to,'placed:'+job_id,'placed')
                why='The owner gave this to-do no area' if unplaced else 'What this to-do came from is all in that area or The Machine\'s own'
                return {'status':'moved','area':moved['area'],'resumed':moved['resumed'],
                        'note':why+', so it moved to '+moved['label']+' by itself and carries on in a new run there. Stop here.'}
            except ValueError as error:  # it can't move now (closed meanwhile): the owner gets the one-tap move as usual
                LOG.info('placing move skipped suggestion=%s error=%s',suggestion_id,error)
                with self.connect() as db:
                    db.execute("UPDATE deliveries SET status='queued',reminder=1,needs_edit=1,error=NULL WHERE suggestion_id=? AND status IN ('queued','sent','uncertain')",(suggestion_id,))
        return {'status':'blocked','reason':reason}

    def originals(self, suggestion_id):
        """The source messages behind a card, in the reviewer's order (its main evidence first), for reading on the dashboard."""
        with self.connect() as db:
            row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown suggestion')
        # The reviewer lists the event that matters first; newest-first put side context on top.
        return self.event_views(json.loads(row['event_ids'])[:20])[:5]

"""What allowed each outward step: the tap, the owner's words or the setting behind it (Settings, Activity;
docs/help/activity.md#what-allowed-it).

Record only. Nothing here decides whether a step may run, adds a check or a confirmation, or changes what The Machine
or Do it may do: each path keeps its own rules, and this module only notes which one let the step through, as it
happens, so Activity can say it afterwards.

Where it is kept: an outbox send or step (action_jobs.basis, written with the job by Store.confirm_action and
Store.auto_merge) and a preparation run (preparation_runs.basis, written by preparation_state.tool_intent at the
run's first tool call, from the decision that started it). Rows from before this existed say BEFORE, and Activity
keeps its older wording for them.

A basis is a small JSON object: {'kind': one of KINDS, ...}. Kinds:
- todo, telegram, voice: the owner's tap on the to-do's own button (Send, Confirm, Merge, Try again), in the
  dashboard, in Telegram or by voice. 'approval' is that tap's approval id.
- chat: the owner asked for it in words (a to-do's chat, a Change note, or their own main chat). 'decision' is their
  message (decisions.id, or the main chat's note id) and 'quote' the start of their words. A quote is only shown when
  it is still found in that owner message (quoted), so words never get put in the owner's mouth.
- doit: the owner tapped Do it, which approves what the to-do offers (AGENTS.md).
- follow_up: an automated follow-up the owner's follow-up settings send by themselves.
- self_doc, self_fix: The Machine's own rules: a new private doc in the owner's Drive, a small tested fix to its own
  error.
- ahead: work prepared ahead, by itself.
- none: nothing recorded allowed it. The step still runs as before; it is shown as "No approval recorded" and goes
  to the error feed (missing), so the path that skipped it can be found."""
from __future__ import annotations

import json

import authorship
import doc_writes
import error_feed

KINDS = ('todo', 'telegram', 'voice', 'chat', 'doit', 'follow_up', 'self_doc', 'self_fix', 'ahead', 'none')
BEFORE = json.dumps({'kind': 'before'})  # a row from before bases were recorded
QUOTE_MAX = 80
OWNER_SOURCES = ('dashboard', 'telegram')  # where an owner's own message or tap comes from (decisions.source)
TAPS = {'dashboard': 'todo', 'telegram': 'telegram', 'voice': 'voice'}


def clip(words):
    words = ' '.join(str(words or '').split())
    return words if len(words) <= QUOTE_MAX else words[:QUOTE_MAX - 1].rstrip() + '…'


def chat(decision_id, words=None):
    """The owner asked in words: their message's id and the start of what they wrote (None: words not kept)."""
    basis = {'kind': 'chat', 'decision': str(decision_id or '')}
    if str(words or '').strip():
        basis['quote'] = clip(words)
    return basis


def for_outbox(source, approval_id):
    """The basis of an outbox step from who approved it (action_jobs.source and approval_id), when the caller had none
    of its own to give."""
    if source in TAPS:
        return {'kind': TAPS[source], 'approval': str(approval_id or '')}
    if source == 'auto_follow_up':
        return {'kind': 'follow_up'}
    if source == 'auto':
        return {'kind': 'self_fix'}
    if source == 'assistant' and str(approval_id or '').startswith(doc_writes.NEW_DOC):
        return {'kind': 'self_doc'}
    return {'kind': 'none', 'source': str(source or '')[:40]}


def read(value):
    """A stored basis as a dict, or None (not recorded)."""
    try:
        basis = json.loads(value) if isinstance(value, str) else value
    except ValueError:
        return None
    return basis if isinstance(basis, dict) and isinstance(basis.get('kind'), str) else None


def from_decision(db, decision_id, action_id=None):
    """The basis of a preparation run, from the decision that started it (preparations.decision_id) and the outbox step
    it carries on, if any (preparations.action_id). Reads only."""
    decision_id = str(decision_id or '')
    for job_id, own in ((action_id, True), (decision_id[len('after:'):] if decision_id.startswith('after:') else None, False)):
        if job_id:  # a confirmed step's own run ('job': that step), or the work after one: what allowed that step
            row = db.execute('SELECT basis FROM action_jobs WHERE id=?', (job_id,)).fetchone()
            found = read(row[0]) if row else None
            if found and found['kind'] in KINDS:
                return {**found, 'job': job_id} if own else found
    row = db.execute('SELECT choice,feedback,source FROM decisions WHERE id=?', (decision_id,)).fetchone() if decision_id else None
    if not row:
        return {'kind': 'none', 'source': 'run'}
    choice, feedback, source = row[0], row[1], row[2]
    if choice == 'prepare_ahead':
        return {'kind': 'ahead'}
    if choice == 'other' and source in OWNER_SOURCES:
        return chat(decision_id, feedback)
    if choice == 'accept' and source in TAPS:
        return {'kind': 'doit', 'approval': decision_id}
    if source in TAPS:
        return {'kind': TAPS[source], 'approval': decision_id}
    return {'kind': 'none', 'source': 'run'}


def quoted(db, basis):
    """The basis's quote when it is still in that owner message (authorship.norm: spacing and case evened out), else
    None. A main chat's words are kept nowhere, so its basis has no quote to show."""
    quote = str(basis.get('quote') or '').rstrip('…').strip()
    if not quote:
        return None
    row = db.execute("SELECT feedback FROM decisions WHERE id=? AND choice='other' AND source IN (?,?)",
                     (str(basis.get('decision') or ''), *OWNER_SOURCES)).fetchone()
    return basis['quote'] if row and authorship.norm(quote) in authorship.norm(row[0]) else None


def shown(db, basis):
    """(kind, quote or None) for Activity to say (activity_log), or None for a row from before. An unknown kind is
    none."""
    if not basis or basis.get('kind') == 'before':
        return None
    kind = basis['kind'] if basis.get('kind') in KINDS else 'none'
    return kind, quoted(db, basis) if kind == 'chat' else None


def missing(db, where, version=None):
    """A step went out with nothing recorded that allowed it: one error-feed signature per path ('where', a code
    name like 'confirm_action.assistant'), never what the step was. It still went; this only makes the path findable."""
    try:
        error_feed.record(db, 'service', 'NoApprovalRecorded', 'no approval recorded', 'machine/action_basis.py', where, None, version)
    except Exception:  # the error feed never stops a step
        pass

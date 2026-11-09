"""Durable execution custody, not an approval layer. Uses the existing SQLite connection."""
import datetime
import json
import hashlib
import re

TERMINAL = ('ok', 'error', 'aborted', 'timed_out', 'lost')


def initialize(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS preparation_runs(
        job_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,session_job_id TEXT NOT NULL,
        status TEXT NOT NULL,started_at TEXT NOT NULL,finished_at TEXT,history_read INTEGER NOT NULL DEFAULT 0);
      CREATE TABLE IF NOT EXISTS preparation_calls(
        job_id TEXT NOT NULL,call_id TEXT NOT NULL,tool TEXT NOT NULL,params TEXT NOT NULL,
        result TEXT,error TEXT,started_at TEXT NOT NULL,finished_at TEXT,PRIMARY KEY(job_id,call_id));
      CREATE TABLE IF NOT EXISTS gateway_starts(
        job_id TEXT PRIMARY KEY,request TEXT NOT NULL,created_at TEXT NOT NULL);
    ''')
    columns = {r['name'] for r in db.execute('PRAGMA table_info(preparations)')}
    if 'session_job_id' not in columns:
        db.execute('ALTER TABLE preparations ADD COLUMN session_job_id TEXT')
    if 'retry_at' not in {r['name'] for r in db.execute('PRAGMA table_info(preparation_runs)')}:
        db.execute('ALTER TABLE preparation_runs ADD COLUMN retry_at TEXT')
    db.execute('UPDATE preparations SET session_job_id=job_id WHERE session_job_id IS NULL')
    # Preserve pre-upgrade runtime custody. Closed historical rows aren't proof of a live run.
    db.execute('''INSERT OR IGNORE INTO preparation_runs(job_id,suggestion_id,session_job_id,status,started_at)
                  SELECT job_id,suggestion_id,session_job_id,status,coalesce(started_at,created_at)
                  FROM preparations WHERE status IN ('starting','running')''')


START_KEEP_DAYS = 2


def same_start(db, request, stamp):
    """The start to send for this run id. Its id is the Gateway's idempotency key, and an earlier start under it may have
    reached the Gateway: OpenClaw (2026.11.2) refuses the same key with other content for good ("Pending input
    idempotency key conflicts with the accepted input"), and a retry builds its message again (newer agent work, files),
    so every retry under one id sends exactly the first one it built. Kept until the run is admitted or over."""
    db.execute('DELETE FROM gateway_starts WHERE created_at<?',
               ((datetime.datetime.fromisoformat(stamp) - datetime.timedelta(days=START_KEEP_DAYS)).isoformat(),))
    row = db.execute('SELECT request FROM gateway_starts WHERE job_id=?', (request['job_id'],)).fetchone()
    if row:
        kept = json.loads(row[0])
        if kept.get('kind') == request.get('kind') and kept.get('session_job_id') == request.get('session_job_id'):
            return kept
    db.execute('INSERT OR REPLACE INTO gateway_starts(job_id,request,created_at) VALUES(?,?,?)',
               (request['job_id'], json.dumps(request, ensure_ascii=False), stamp))
    return request


def start_settled(db, job_id):
    db.execute('DELETE FROM gateway_starts WHERE job_id=?', (job_id,))


def tool_intent(db, args, stamp):
    db.execute('BEGIN IMMEDIATE')
    run = db.execute('''SELECT r.*,p.status current_status,p.job_id current_job,s.status owner_status
        FROM preparation_runs r JOIN preparations p USING(suggestion_id) JOIN suggestions s ON s.id=r.suggestion_id
        WHERE r.job_id=?''', (args['job_id'],)).fetchone()
    if not run or run['current_job'] != args['job_id'] or run['current_status'] not in ('starting','running') or run['owner_status'] not in ('accepted','instructions'):
        return {'active': False, 'reason': 'The owner changed or stopped this task. End this run.'}
    earlier = db.execute('SELECT 1 FROM preparation_calls c JOIN preparation_runs r USING(job_id) WHERE r.suggestion_id=? AND c.job_id!=? LIMIT 1',
                         (run['suggestion_id'], args['job_id'])).fetchone()
    if earlier and not run['history_read'] and not args.get('read_only') and not finishing(args):
        return {'active': False, 'reason': 'Read preparation_history first, then reconcile completed or uncertain steps before continuing. Do not repeat the whole task.'}
    db.execute('INSERT OR IGNORE INTO preparation_calls(job_id,call_id,tool,params,started_at) VALUES(?,?,?,?,?)',
               (args['job_id'], args['call_id'], args['tool'], json.dumps(args.get('params',{}),ensure_ascii=False), stamp))
    return {'active': True}


# Saving the result or a blocker is always allowed: a continuation that can't finish would only
# end without a result (2026-10-13 review).
FINISH_ACTIONS = ('prepare', 'preparation_blocked')


def finishing(args):
    params = args.get('params')
    if args.get('tool') != 'assistant_signals':
        return False
    # The hook records the action from the original parameters, before journal clipping.
    if 'tool_action' in args:
        return args['tool_action'] in FINISH_ACTIONS
    if isinstance(params, dict):
        if not clipped(params):
            return params.get('action') in FINISH_ACTIONS
        params = params.get('preview', '')
    return leading_action(params) in FINISH_ACTIONS


def leading_action(text):
    """The action a clipped record's text starts with. Only a leading action counts, never an action mentioned inside
    the draft/text being saved. Also reads an old hook's clipped record."""
    match = re.match(r'^\s*\{\s*"action"\s*:\s*"([^"\\]*)"\s*[,}]', str(text or ''))
    return match[1] if match else None


def call_action(params):
    """The action of a recorded assistant_signals call, also when its record was clipped; None when it has none."""
    if not isinstance(params, dict):
        return None
    action = leading_action(params.get('preview', '')) if clipped(params) else params.get('action')
    return action if isinstance(action, str) else None


def tool_result(db, args, stamp):
    db.execute('UPDATE preparation_calls SET result=?,error=?,finished_at=? WHERE job_id=? AND call_id=?',
               (json.dumps(args.get('result'),ensure_ascii=False), args.get('error'), stamp,args['job_id'],args['call_id']))
    return {'saved': True}


# Reads that change nothing; left out of the history so a continuation reads only what matters.
READ_ACTIONS = {'assistant_signals': {'status', 'events', 'preparation_history'},
                'browser': {'status', 'snapshot', 'screenshot', 'tabs', 'console'}}
PAGE = 24000


def decoded(value):
    try:
        return json.loads(value) if value is not None else None
    except (TypeError, ValueError):
        return value


def clipped(value):
    return isinstance(value, dict) and value.get('clipped') is True and value.get('full') == 'retained session transcript'


def call_ref(call):
    # Stable, bounded identity even when old hooks used entire parameters as a call ID.
    return hashlib.sha256(json.dumps([call['job_id'], call['call_id']], ensure_ascii=False).encode()).hexdigest()


def complete_details(call):
    return not any(clipped(decoded(call[field])) for field in ('params', 'result'))


def short(value, limit):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(',', ':'))
    return text if len(text) <= limit else text[:limit] + '…'


def summary(call):
    """One compact line per earlier call: what it was, on what, and whether it finished."""
    params = decoded(call['params'])
    if isinstance(params, dict) and params.get('action') in READ_ACTIONS.get(call['tool'], set()):
        return None
    if call['error']:
        outcome = 'failed: ' + short(call['error'], 160)
    elif call['finished_at'] is None:
        outcome = 'no result recorded (uncertain: check the app before repeating)'
    else:
        result = decoded(call['result'])
        outcome = 'done' + (': ' + short(result, 160) if result not in (None, '', {}) else '')
    return {'call_ref': call_ref(call), 'at': call['started_at'], 'tool': call['tool'],
            'params': short(params, 300), 'outcome': outcome, 'detail_complete': complete_details(call)}


def history(db, job_id, offset=0, ref=None):
    run = db.execute('SELECT suggestion_id FROM preparation_runs WHERE job_id=?',(job_id,)).fetchone()
    if not run:
        raise ValueError('Unknown execution')
    calls = [dict(r) for r in db.execute('''SELECT c.* FROM preparation_calls c JOIN preparation_runs r USING(job_id)
                WHERE r.suggestion_id=? AND c.job_id!=? ORDER BY c.started_at,c.call_id''',(run['suggestion_id'],job_id))]
    if ref is not None:
        selected = next((c for c in calls if call_ref(c) == ref), None)
        if selected is None:
            raise ValueError('Unknown earlier call on this task')
        detail = dict(selected, params=decoded(selected['params']), result=decoded(selected['result']))
        text = json.dumps(detail, ensure_ascii=False)
        instruction = 'Exact saved call details. Follow next_offset with the same call_ref; join history pages to recover the full JSON. Reconcile completed or uncertain work in the original app before repeating it.'
        if not complete_details(selected):
            instruction += ' This call was clipped by the journal hook: the missing content is in the retained session transcript, not this detail reply. Check that transcript or the original app; never infer failure or repeat from a missing suffix.'
    else:
        text = json.dumps([x for x in map(summary, calls) if x], ensure_ascii=False)
        instruction = 'Earlier calls on this task, oldest first (known reads left out). Summaries are shortened: use preparation_history with a call_ref and offset 0, then its next_offset, for exact parameters and receipts when reconciling a call. "done" calls may have changed an app; "uncertain" ones may or may not have. Check the current state before repeating a write. Continue only unfinished work.'
    offset=max(0,int(offset)); end=offset+PAGE
    # Only the page that actually ends the history counts as having read it.
    if ref is None and end>=len(text) and offset<max(len(text),1):
        db.execute('UPDATE preparation_runs SET history_read=1 WHERE job_id=?',(job_id,))
    return {'history':text[offset:end], 'next_offset':end if end<len(text) else None,
            **({'call_ref': ref, 'detail_complete': complete_details(selected)} if ref is not None else {}),
            'instruction': instruction}

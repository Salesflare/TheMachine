"""Activity: one list of everything The Machine did for its owner (Settings, Activity; docs/activity.md).

Read-only. It changes nothing The Machine may do and adds no step to any action: it reads what each part already keeps
and shows it in one place, newest first. Each source stays the owner of its own table; this module only reads them.
It owns two tables: activity_accounts remembers which connections it saw, so a connection added or removed shows, and
activity_blocks keeps each send a check stopped (note_block, called where the outbox blocks it), so the block stays in
the history as Blocked, with its reason, even when the send is canceled or tried again later.

Every line has one shape, the same for every source (and for sources other modules add with register()):

    {'id': 'messages:<job id>',      # unique and stable: '<kind>:<the source's own id>'
     'kind': 'messages',             # one of KINDS: what the list filters by
     'at': '2026-10-31T09:12:00+00:00',
     'what': 'Email to Sam: Pricing', # one line in the owner's language, never starting with "You"
     'where': 'Gmail · sam@acme.com', # the account or app it happened in, or None
     'outcome': 'done',              # done, refused, failed, undone or pending (OUTCOMES)
     'status': 'Sent',               # the outcome in a word or two, in the owner's language
     'by': 'Approved in the to-do',  # what allowed it (machine/action_basis.py), or who started it, or None
     'actor': None,                  # optional: a stable id of who did it (an AI connection), for its own filtered view
     'todo': {'id': '…', 'title': '…'} or None,
     'detail': None,                 # an optional second line
     'withdraw': None,               # {'id', 'n'} on a learning that can still be withdrawn (Fleet's Withdraw)
     'undo': None}                   # {'action', 'id'}: what still can be taken back, by that owner's dashboard action
                                     # with {'id'} (a connected AI's Graph change: ai_undo; a fact
                                     # forgotten in chat: learning_undo). The source keeps what it was
                                     # before and refuses when it changed since; this module only passes it on.

What it reads:
- messages, docs, calendar, web, fixes: the outbox (action_jobs), every step the owner approved or The Machine ran by
  itself (a self-merged fix, a follow-up sent by itself), with how it went: refused when a check before the send
  stopped it (blocked), undone when Undo took it back or it was canceled. Each says what allowed it, as the step
  recorded it (machine/action_basis.py): the to-do's button, Do it, the owner's words in chat (quoted while they are
  still in that message of theirs), a setting, or No approval recorded (that path also goes to the error feed once).
- web, also: a to-do's run that took a step on a page that can change something (a click, typing, an upload), with
  what allowed the run (preparation_runs.basis).
- agents: work handed to Claude Code or Codex (agent_jobs).
- fleet: questions and requests to and from teammates, both ways, with what the owner's rules answered (fleet_log).
- learnings: learnings sent to The Machine team and withdrawn ones (team_learnings), and votes on team learnings.
- skills: skills added, from the owner or shared by a teammate (skills).
- graph: files imported into the Graph, and undone imports (graph_imports).
- connections: a connection added or removed (activity_accounts, noted when the service starts and on each read).
- access: The Machine team's looks under Support access. They live on the control plane (hosted) or come through the
  Fleet (self-hosted); the dashboard adds them from Settings, Security, as it reads them there.
- ai: other AIs connected over MCP, each call and each refused one. Their module adds them with register('ai', read).
- memory: what the owner asked their main chat to forget (learning_changes kind 'forgot'), with Undo while it holds.

A source that isn't set up on this Machine (no table yet) adds nothing."""
from __future__ import annotations

import datetime as dt
import json
import logging
import re

import i18n
from machine import action_basis, names
import preparation_state
from machine.kinds import SENDS
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
KINDS = ('messages', 'docs', 'calendar', 'web', 'fixes', 'agents', 'fleet', 'learnings', 'skills', 'graph', 'connections',
         'access', 'ai', 'memory')
OUTCOMES = ('done', 'refused', 'failed', 'undone', 'pending')
PAGE = 50
MAX_OFFSET = 2000
SCHEMA = ('CREATE TABLE IF NOT EXISTS activity_accounts(account_id TEXT PRIMARY KEY,service TEXT NOT NULL,label TEXT NOT NULL,'
          'added_at TEXT,removed_at TEXT,seen INTEGER NOT NULL DEFAULT 1)')
BLOCKS = ('CREATE TABLE IF NOT EXISTS activity_blocks(job_id TEXT NOT NULL,at TEXT NOT NULL,reason TEXT,'
          'PRIMARY KEY(job_id,at))')
MESSAGE_KINDS = {**{kind: send['name'] for kind, send in SENDS.items()}, 'email_demo': 'Email'}  # machine/kinds.py, and the demo's
# action_jobs.status -> outcome; anything else (queued, sending, local_preparation, undoing) is still on its way
JOB_OUTCOME = {'sent': 'done', 'done': 'done', 'blocked': 'refused', 'failed': 'failed', 'uncertain': 'failed', 'finish_uncertain': 'failed',
               'cancelled': 'undone', 'undone': 'undone'}

_sources = {}


def register(kind, read):
    """Add a source of lines from another module: read(db, limit) -> lines in the shape above, newest first, at most
    limit of them. kind is one of KINDS (an MCP server's calls are 'ai'). The read runs inside the list's own read
    transaction; one that fails is left out of the list, never the whole list."""
    if kind not in KINDS:
        raise ValueError('Unknown activity kind')
    _sources.setdefault(kind, []).append(read)


def ensure(db):
    db.execute(SCHEMA)
    db.execute(BLOCKS)


def note_block(db, job_id, reason, at):
    """A check stopped an outbox send (action_jobs status blocked): remember it as history. Canceling or retrying the
    send later changes action_jobs, never this, so the line stays Blocked under Refused or blocked. Adds no check."""
    db.execute(BLOCKS)
    db.execute('INSERT OR IGNORE INTO activity_blocks(job_id,at,reason) VALUES(?,?,?)', (job_id, at, reason))


def _tables(db):
    return {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def _clip(text, n=160):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= n else text[:n - 1].rstrip() + '…'


def account_who(account):
    """The address or name an account goes by, or ''."""
    return str(account.get('email') or account.get('label') or account.get('name') or account.get('slack_host') or '')


def account_label(account):
    """'Gmail · sam@acme.com': the service and the address or name it goes by. The service is what the owner calls it
    (machine/names.py), never the tool underneath (an account with only transport 'gog' is Gmail)."""
    name = names.service_name(names.account_service(account)) or i18n.t('Connection')
    who = account_who(account)
    return f'{name} · {who}' if who else name


def _stored_label(service, label):
    """A connection line's label as kept in activity_accounts, named again on read: one kept before names.py could
    say 'Gog · sam@acme.com' (an account with no service, only its transport)."""
    who = label.split(' · ', 1)[1] if ' · ' in (label or '') else ''
    return account_label({'service': service, 'email': who})


def note_accounts(db, accounts, at):
    """Remember the connections there are now; one that is new or gone since the last look is a line under
    Connections. The very first look only remembers (what was there before isn't news)."""
    ensure(db)
    known = {r[0]: r for r in db.execute('SELECT account_id,removed_at FROM activity_accounts')}
    first = not known
    now_ids = set()
    for account in accounts or []:
        if not isinstance(account, dict) or not account.get('id'):
            continue
        aid = str(account['id'])
        now_ids.add(aid)
        if aid not in known:
            db.execute('INSERT INTO activity_accounts(account_id,service,label,added_at) VALUES(?,?,?,?)',
                       (aid, names.account_service(account), account_label(account), None if first else at))
        elif known[aid][1]:  # back after it was removed
            db.execute('UPDATE activity_accounts SET added_at=?,removed_at=NULL,label=? WHERE account_id=?', (at, account_label(account), aid))
        else:
            db.execute('UPDATE activity_accounts SET label=? WHERE account_id=?', (account_label(account), aid))
    for aid, row in known.items():
        if aid not in now_ids and not row[1]:
            db.execute('UPDATE activity_accounts SET removed_at=? WHERE account_id=?', (at, aid))


def _line(kind, ref, at, what, outcome='done', status=None, where=None, by=None, todo=None, detail=None, **more):
    return {'id': f'{kind}:{ref}', 'kind': kind, 'at': at, 'what': what, 'where': where, 'outcome': outcome,
            'status': status, 'by': by, 'todo': todo, 'detail': detail, **more}


def _to(payload):
    to = payload.get('to_name') or payload.get('to')
    if isinstance(to, list):
        to = ', '.join(str(x).split('<')[0].strip(' "') or str(x) for x in to[:3])
    return _clip(to or payload.get('to_email') or payload.get('as_name') or '', 80)


def _job_kind(kind):
    if kind in MESSAGE_KINDS:
        return 'messages'
    return {'doc_write': 'docs', 'calendar': 'calendar', 'finish': 'web', 'merge': 'fixes'}.get(kind)


def _job_status(kind, status):
    outcome = JOB_OUTCOME.get(status, 'pending')
    if status == 'uncertain':
        return outcome, i18n.t('Not sure it went through')
    if outcome == 'done':
        if kind == 'messages':
            return outcome, i18n.t('Sent')
        if kind == 'docs':
            return outcome, i18n.t('Saved')
        return outcome, i18n.t('Merged') if kind == 'fixes' else i18n.t('Done')
    if outcome == 'refused':
        return outcome, i18n.t('Blocked')
    if outcome == 'failed':
        return outcome, i18n.t('Didn’t work')
    if outcome == 'undone':
        return outcome, i18n.t('Undone') if status == 'undone' else i18n.t('Canceled')
    return outcome, i18n.t('On its way')


_unrecorded = set()  # outbox jobs with no basis at all, sent to the error feed once per run of the service


def _by(db, r):
    """What allowed an outbox step (machine/action_basis.py), in the owner's language; None for a job from before bases
    were kept (the older wording stays). A job with none at all came by a path that records nothing: it says so, and
    the path goes to the error feed once."""
    basis = action_basis.read(r['basis'])
    if basis is None:
        if r['id'] not in _unrecorded:
            _unrecorded.add(r['id'])
            action_basis.missing(db, 'activity.outbox')
        basis = {'kind': 'none'}
    return _basis_line(db, basis)


def _basis_line(db, basis):
    """The line for what allowed a step, never starting with "You"; None for one from before bases were kept."""
    shown = action_basis.shown(db, basis)
    if not shown:
        return None
    kind, quote = shown
    if quote:
        return i18n.t('Asked in chat: “{}”', quote)
    return {'todo': i18n.t('Approved in the to-do'), 'telegram': i18n.t('Approved in Telegram'), 'voice': i18n.t('Approved by voice'),
            'chat': i18n.t('Asked in chat'), 'doit': i18n.t('Do it tapped'), 'follow_up': i18n.t('Follow-up, sent by itself'),
            'self_doc': i18n.t('New private doc, made by itself'), 'self_fix': i18n.t('Small fix, merged by itself'),
            'ahead': i18n.t('Prepared ahead, by itself')}.get(kind) or i18n.t('No approval recorded')


def _jobs(db, config, limit, tables, kinds):
    accounts = {a.get('id'): a for a in (config or {}).get('accounts') or [] if isinstance(a, dict)}
    follow_ups = 'follow_up_sends' in tables
    rows = db.execute('SELECT j.id,j.suggestion_id,j.payload,j.status,j.error,j.source,j.created_at,j.updated_at,s.title,j.basis,'
                      + ('(SELECT 1 FROM follow_up_sends f WHERE f.job_id=j.id) fu ' if follow_ups else '0 fu ')
                      + 'FROM action_jobs j LEFT JOIN suggestions s ON s.id=j.suggestion_id '
                      "WHERE json_extract(j.payload,'$.kind') IN (" + ','.join('?' * len(kinds)) + ') '
                      'ORDER BY j.created_at DESC LIMIT ?', (*kinds, limit)).fetchall()
    blocks = {}
    if 'activity_blocks' in tables and rows:
        for b in db.execute('SELECT job_id,at,reason FROM activity_blocks WHERE job_id IN (SELECT value FROM json_each(?)) '
                            'ORDER BY at', (json.dumps([r['id'] for r in rows]),)):
            blocks.setdefault(b['job_id'], []).append(b)
    for r in rows:
        try:
            p = json.loads(r['payload'])
        except (TypeError, ValueError):
            continue
        kind = _job_kind(p.get('kind'))
        if not kind:
            continue
        outcome, status = _job_status(kind, r['status'])
        if kind == 'docs' and outcome == 'done' and p.get('op') == 'create':
            status = i18n.t('Created')
        to, label = _to(p), _clip(p.get('label'), 120)
        if kind == 'messages':
            channel = MESSAGE_KINDS[p['kind']]
            subject = _clip(p.get('subject'), 100)
            if p['kind'] in ('email', 'email_demo'):
                what = i18n.t('Email to {}: {}', to, subject) if to and subject else i18n.t('Email to {}', to) if to else i18n.t('Email')
            elif p['kind'] == 'doc_reply':
                what = i18n.t('Reply in a doc')
            else:
                what = i18n.t('{} message to {}', channel, to) if to else i18n.t('{} message', channel)
        elif kind == 'docs':
            title = _clip(p.get('title') or p.get('label'), 100)
            what = i18n.t('New doc: {}', title) if p.get('op') == 'create' else i18n.t('Doc edited: {}', title)
        else:
            what = label or {'calendar': i18n.t('Calendar change'), 'web': i18n.t('Step on the web'), 'fixes': i18n.t('Fix merged')}[kind]
        account = accounts.get(p.get('account_id'))
        # A message's line names its channel already ("Email to …", "Slack message to …"): its account is only the
        # address or name it went from; other lines name the service too
        where = (account_who(account) or account_label(account) if kind == 'messages' else account_label(account)) if account else ({'calendar': i18n.t('Calendar'), 'fixes': 'The Machine'}.get(kind)
                                                       or (_clip(p.get('from'), 80) or None))
        if kind == 'docs' and not account and p.get('provider'):
            where = {'google': 'Google Docs', 'microsoft': 'Word'}.get(p['provider'])
        by = _by(db, r) or (i18n.t('Follow-up, sent by itself') if r['fu'] else i18n.t('By itself') if r['source'] == 'auto'
                            else i18n.t('Approved by voice') if r['source'] == 'voice' else i18n.t('After your OK'))
        todo = {'id': r['suggestion_id'], 'title': _clip(r['title'], 120)} if r['title'] is not None else None
        # Each time a check stopped it is its own line, at that moment; a send canceled or still held after a block
        # is told by those lines, one sent after it by its own line too
        held = blocks.get(r['id'], [])
        for n, b in enumerate(held, 1):
            yield _line(kind, f"{r['id']}:blocked:{n}", b['at'], what, 'refused', i18n.t('Blocked'), where, by, todo,
                        _clip(b['reason'], 200) or None)
        if held and r['status'] in ('blocked', 'cancelled'):
            continue
        detail = (_clip(r['error'], 200) or None) if r['status'] == 'blocked' else None
        yield _line(kind, r['id'], r['created_at'], what, outcome, status, where, by, todo, detail)


RUN_OUTCOME = {'ok': 'done', 'starting': 'pending', 'running': 'pending'}  # preparation_runs.status; the rest stopped


def _runs(db, limit, tables):
    """A to-do's run (Do it, a message in its chat, a confirmed step) that took a step on a web page that can change
    something (preparation_state.OUTWARD_BROWSER): one line under Steps on the web, with what allowed it. A confirmed
    final step is the outbox's line already. Runs from before bases were kept aren't listed, as before."""
    if not {'preparation_runs', 'preparation_calls'} <= tables:
        return
    rows = db.execute("SELECT r.job_id,r.suggestion_id,r.status,r.started_at,r.basis,s.title FROM preparation_runs r "
                      "LEFT JOIN suggestions s ON s.id=r.suggestion_id WHERE r.basis IS NOT NULL AND json_valid(r.basis) "
                      "AND json_extract(r.basis,'$.kind')!='before' "
                      "AND EXISTS(SELECT 1 FROM preparation_calls c WHERE c.job_id=r.job_id AND c.tool='browser') "
                      "AND NOT EXISTS(SELECT 1 FROM action_jobs j WHERE j.id=json_extract(r.basis,'$.job') "
                      "AND json_extract(j.payload,'$.kind')='finish') ORDER BY r.started_at DESC LIMIT ?", (limit,)).fetchall()
    for r in rows:
        # The calls' parameters are sealed at rest (message_seal.DERIVED): read here, never matched in SQL
        if not any(preparation_state.outward(c['tool'], preparation_state.decoded(c['params'])) for c in db.execute(
                "SELECT tool,params FROM preparation_calls WHERE job_id=? AND tool='browser' LIMIT 200", (r['job_id'],))):
            continue
        outcome = RUN_OUTCOME.get(r['status'], 'failed')
        status = {'done': i18n.t('Done'), 'pending': i18n.t('Working'), 'failed': i18n.t('Stopped')}[outcome]
        todo = {'id': r['suggestion_id'], 'title': _clip(r['title'], 120)} if r['title'] is not None else None
        yield _line('web', 'run:' + r['job_id'], r['started_at'], i18n.t('Steps on the web'), outcome, status, None,
                    _basis_line(db, action_basis.read(r['basis']) or {'kind': 'none'}), todo)


def _agents(db, limit, tables):
    if 'agent_jobs' not in tables:
        return
    for r in db.execute('SELECT j.id,j.suggestion_id,j.tool,j.status,j.created_at,s.title FROM agent_jobs j '
                        'LEFT JOIN suggestions s ON s.id=j.suggestion_id ORDER BY j.created_at DESC LIMIT ?', (limit,)):
        name = names.agent_name(r['tool'])
        outcome = {'failed': 'failed', 'cancelled': 'undone'}.get(r['status'], 'done' if r['status'] in ('done', 'finished', 'ok') else 'pending')
        status = {'failed': i18n.t('Stopped'), 'undone': i18n.t('Canceled'), 'done': i18n.t('Done'), 'pending': i18n.t('Working')}[outcome]
        todo = {'id': r['suggestion_id'], 'title': _clip(r['title'], 120)} if r['title'] is not None else None
        yield _line('agents', r['id'], r['created_at'], i18n.t('Handed to {}', name), outcome, status, name, i18n.t('After your OK'), todo)


def _fleet(db, limit, tables):
    if 'fleet_log' not in tables:
        return
    for r in db.execute('SELECT id,at,direction,name,kind,what,outcome FROM fleet_log ORDER BY id DESC LIMIT ?', (limit,)):
        said = str(r['outcome'] or '')
        low = said.lower()
        outcome = ('refused' if low.startswith(('declined', 'refused', 'never', 'no ')) or 'declined' in low
                   else 'pending' if low.startswith('waiting') else 'done')
        name = _clip(r['name'], 60) or i18n.t('a teammate')
        what = i18n.t('From {}: {}', name, _clip(r['what'], 200)) if r['direction'] == 'in' else i18n.t('To {}: {}', name, _clip(r['what'], 200))
        # the status in a word; what the rule or the Machine said in full under it (as the Fleet's log kept it)
        status = (i18n.t('Declined') if outcome == 'refused' else i18n.t('Waiting for you') if outcome == 'pending'
                  else i18n.t('Asked') if r['direction'] == 'out' else i18n.t('Answered'))
        yield _line('fleet', r['id'], r['at'], what, outcome, status, 'Fleet', None,
                    detail=None if re.fullmatch(r'answered|declined|waiting for you|asked \d*', low.strip()) else _clip(said[:1].upper() + said[1:], 200))


def _learnings(db, limit, tables):
    if 'team_learnings' in tables:
        for batch, at, record in db.execute("SELECT id,decided_at,sent FROM team_learnings WHERE status='sent' ORDER BY decided_at DESC LIMIT ?", (limit,)):
            try:
                record = json.loads(record or '{}')
            except ValueError:
                continue
            gone = record.get('withdrawn') or {}
            for n, item in enumerate(record.get('items') or [], 1):
                if not isinstance(item, dict):
                    continue
                withdrawn = gone.get(str(n))
                yield _line('learnings', f'{batch}:{n}', at, i18n.t('Learning shared: {}', _clip(item.get('text'), 200)),
                            'undone' if withdrawn else 'done', i18n.t('Withdrawn') if withdrawn else i18n.t('Sent'),
                            'The Machine team', i18n.t('By itself') if record.get('auto') else i18n.t('After your OK'),
                            detail=i18n.t('With your email') if record.get('named') else None,
                            withdraw=None if withdrawn else {'id': batch, 'n': n},
                            # exactly what went, as Fleet, Activity showed it before: the example, use cases and error log
                            sent={'example': str(item.get('example') or ''), 'log': str(item.get('log') or ''),
                                  'use_cases': [' · '.join(str(c.get(k) or '') for k in ('given', 'when', 'then') if c.get(k))
                                                for c in item.get('use_cases') or [] if isinstance(c, dict)]})
    if 'team_learning_votes' in tables:
        for r in db.execute("SELECT candidate_id,text,vote,sent_at FROM team_learning_votes WHERE sent_at IS NOT NULL ORDER BY sent_at DESC LIMIT ?", (limit,)):
            yield _line('learnings', 'vote:' + str(r['candidate_id']), r['sent_at'], i18n.t('Vote on a team learning: {}', _clip(r['text'], 200)),
                        'done', i18n.t('Sent'), 'The Machine team', None)


def _skills(db, limit, tables):
    if 'skills' not in tables:
        return
    for r in db.execute("SELECT id,name,origin,author,status,created_at FROM skills WHERE status IN ('on','off') ORDER BY created_at DESC LIMIT ?", (limit,)):
        shared = r['origin'] == 'shared'
        yield _line('skills', r['id'], r['created_at'], i18n.t('Skill added: {}', _clip(r['name'], 100)), 'done',
                    i18n.t('On') if r['status'] == 'on' else i18n.t('Off'), i18n.t('From {}', _clip(r['author'], 60)) if shared and r['author'] else 'Skills', None)


def _graph(db, limit, tables):
    if 'graph_imports' not in tables:
        return
    for r in db.execute('SELECT id,name,at,undone_at FROM graph_imports ORDER BY at DESC LIMIT ?', (limit,)):
        yield _line('graph', r['id'], r['at'], i18n.t('Imported into the Graph: {}', _clip(r['name'], 100)) if r['name'] else i18n.t('Imported into the Graph'),
                    'undone' if r['undone_at'] else 'done', i18n.t('Undone') if r['undone_at'] else i18n.t('Done'), 'Graph', i18n.t('After your OK'))


def _memory(db, limit, tables):
    if 'learning_changes' not in tables:
        return
    for r in db.execute("SELECT id,at,after,status FROM learning_changes WHERE kind='forgot' ORDER BY at DESC,id DESC LIMIT ?", (limit,)):
        undone = r['status'] == 'undone'
        yield _line('memory', r['id'], r['at'], i18n.t('Forgot: {}', _clip(r['after'], 200)), 'undone' if undone else 'done',
                    i18n.t('Undone') if undone else i18n.t('Done'), None, i18n.t('Asked in chat'),
                    undo=None if undone else {'action': 'learning_undo', 'id': r['id']})


def _connections(db, limit, tables):
    if 'activity_accounts' not in tables:
        return
    for r in db.execute('SELECT account_id,service,label,added_at,removed_at FROM activity_accounts WHERE added_at IS NOT NULL OR removed_at IS NOT NULL '
                        "ORDER BY max(coalesce(added_at,''),coalesce(removed_at,'')) DESC LIMIT ?", (limit,)):
        if r['removed_at']:
            yield _line('connections', 'removed:' + r['account_id'], r['removed_at'], i18n.t('Connection removed'), 'done', i18n.t('Removed'), _stored_label(r['service'], r['label']))
        if r['added_at']:
            yield _line('connections', 'added:' + r['account_id'], r['added_at'], i18n.t('Connection added'), 'done', i18n.t('Added'), _stored_label(r['service'], r['label']))


def _stamp(value):
    try:
        moment = dt.datetime.fromisoformat(str(value))
    except ValueError:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    return moment if moment.tzinfo else moment.replace(tzinfo=dt.timezone.utc)


OUTBOX = {'messages': tuple(MESSAGE_KINDS), 'docs': ('doc_write',), 'calendar': ('calendar',), 'web': ('finish',), 'fixes': ('merge',)}


def page(db, config=None, kind='', offset=0, limit=PAGE, outcome='', actor=''):
    """{'items': [...], 'next': offset or None, 'kinds': [kinds this Machine has lines for]}: newest first. kind narrows
    to one or more of KINDS (comma-separated: Fleet, Activity shows fleet,learnings); outcome to one of OUTCOMES
    (refused: what was refused or blocked); actor to the lines of one actor (an AI connection's own activity)."""
    try:
        offset = max(0, min(int(offset or 0), MAX_OFFSET))
        limit = max(1, min(int(limit or PAGE), 200))
    except (TypeError, ValueError):
        raise OwnerError('Not a page') from None
    chosen = {k for k in str(kind or '').split(',') if k}
    if chosen - set(KINDS):
        raise ValueError('Unknown activity kind')
    if outcome and outcome not in OUTCOMES:
        raise ValueError('Unknown outcome')
    tables = _tables(db)
    want = offset + limit + 1
    # A filter reads further back in its own sources, the others only far enough to say they have lines
    deep = MAX_OFFSET + limit if outcome or actor else want
    size = {k: (deep if not chosen or k in chosen else 1) for k in KINDS}
    job_kinds = [j for k, js in OUTBOX.items() if not chosen or k in chosen for j in js]
    readers = {
        'outbox': lambda: _jobs(db, config, deep, tables, job_kinds) if job_kinds else (),
        'runs': lambda: _runs(db, size['web'], tables),
        'agents': lambda: _agents(db, size['agents'], tables),
        'fleet': lambda: _fleet(db, size['fleet'], tables),
        'learnings': lambda: _learnings(db, size['learnings'], tables),
        'skills': lambda: _skills(db, size['skills'], tables),
        'graph': lambda: _graph(db, size['graph'], tables),
        'connections': lambda: _connections(db, size['connections'], tables),
        'memory': lambda: _memory(db, size['memory'], tables),
    }
    for name, reads in _sources.items():
        for n, read in enumerate(reads):
            readers[f'{name}:{n}'] = (lambda r, k: lambda: r(db, size[k]))(read, name)
    lines, kinds, seen = [], set(), set()
    for name, read in readers.items():
        try:
            for line in read():
                if not isinstance(line, dict) or line.get('kind') not in KINDS or line.get('id') in seen:
                    continue
                kinds.add(line['kind'])
                seen.add(line.get('id'))
                if (not chosen or line['kind'] in chosen) and (not outcome or line.get('outcome') == outcome) and (
                        not actor or line.get('actor') == actor):
                    lines.append(line)
        except Exception as error:  # a source that can't be read is left out, never the whole list
            LOG.warning('activity source=%s error=%s', name.split(':')[0], type(error).__name__)
    if chosen:  # which kinds the outbox has, for the filter, without reading its lines
        found = {r[0] for r in db.execute("SELECT DISTINCT json_extract(payload,'$.kind') FROM action_jobs")}
        kinds.update(k for k, js in OUTBOX.items() if found & set(js))
    lines.sort(key=lambda x: _stamp(x.get('at')), reverse=True)
    items = [{**x, 'where': names.place(x['where'])} if x.get('where') else x for x in lines[offset:offset + limit]]
    more = len(lines) > offset + limit and offset + limit < MAX_OFFSET
    return {'items': items, 'next': offset + limit if more else None, 'kinds': [k for k in KINDS if k in kinds]}

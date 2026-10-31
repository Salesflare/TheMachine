"""Activity: one list of everything The Machine did for its owner (Settings, Activity; docs/activity.md).

Read-only. It changes nothing The Machine may do and adds no step to any action: it reads what each part already keeps
and shows it in one place, newest first. Each source stays the owner of its own table; this module only reads them.
The one table it owns, activity_accounts, remembers which connections it saw, so a connection added or removed shows.

Every line has one shape, the same for every source (and for sources other modules add with register()):

    {'id': 'messages:<job id>',      # unique and stable: '<kind>:<the source's own id>'
     'kind': 'messages',             # one of KINDS: what the list filters by
     'at': '2026-10-31T09:12:00+00:00',
     'what': 'Email to Sam: Pricing', # one line in the owner's language, never starting with "You"
     'where': 'Gmail · sam@acme.com', # the account or app it happened in, or None
     'outcome': 'done',              # done, refused, failed, undone or pending (OUTCOMES)
     'status': 'Sent',               # the outcome in a word or two, in the owner's language
     'by': 'After your OK',          # who started it, or None
     'actor': None,                  # optional: a stable id of who did it (an AI connection), for its own filtered view
     'todo': {'id': '…', 'title': '…'} or None,
     'detail': None,                 # an optional second line
     'withdraw': None}               # {'id', 'n'} on a learning that can still be withdrawn (Fleet's Withdraw)

What it reads:
- messages, docs, calendar, web, fixes: the outbox (action_jobs), every step the owner approved or The Machine ran by
  itself (a self-merged fix, a follow-up sent by itself), with how it went: refused when a check before the send
  stopped it (blocked), undone when Undo took it back or it was canceled.
- agents: work handed to Claude Code or Codex (agent_jobs).
- fleet: questions and requests to and from teammates, both ways, with what the owner's rules answered (fleet_log).
- learnings: learnings sent to The Machine team and withdrawn ones (team_learnings), and votes on team learnings.
- skills: skills added, from the owner or shared by a teammate (skills).
- graph: files imported into the Graph, and undone imports (graph_imports).
- connections: a connection added or removed (activity_accounts, noted when the service starts and on each read).
- access: The Machine team's looks under Support access. They live on the control plane (hosted) or come through the
  Fleet (self-hosted); the dashboard adds them from Settings, Security, as it reads them there.
- ai: other AIs connected over MCP, each call and each refused one. Their module adds them with register('ai', read).

A source that isn't set up on this Machine (no table yet) adds nothing."""
from __future__ import annotations

import datetime as dt
import json
import logging
import re

import i18n

LOG = logging.getLogger('personal-assistant')
KINDS = ('messages', 'docs', 'calendar', 'web', 'fixes', 'agents', 'fleet', 'learnings', 'skills', 'graph', 'connections',
         'access', 'ai')
OUTCOMES = ('done', 'refused', 'failed', 'undone', 'pending')
PAGE = 50
MAX_OFFSET = 2000
SCHEMA = ('CREATE TABLE IF NOT EXISTS activity_accounts(account_id TEXT PRIMARY KEY,service TEXT NOT NULL,label TEXT NOT NULL,'
          'added_at TEXT,removed_at TEXT,seen INTEGER NOT NULL DEFAULT 1)')
SERVICES = {'gmail': 'Gmail', 'calendar': 'Google Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar',
            'slack': 'Slack', 'salesflare': 'Salesflare', 'android': 'Android', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
            'linkedin': 'LinkedIn', 'x': 'X', 'intercom': 'Intercom', 'zoom': 'Zoom', 'stripe': 'Stripe', 'github': 'GitHub',
            'trello': 'Trello', 'shortcut': 'Shortcut', 'docs': 'Docs', 'google_meet': 'Google Meet', 'rss': 'RSS',
            'gateway': 'OpenClaw'}
MESSAGE_KINDS = {'email': 'Email', 'email_demo': 'Email', 'linkedin': 'LinkedIn', 'slack': 'Slack', 'x': 'X',
                 'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'intercom': 'Intercom', 'doc_reply': 'Docs'}
# action_jobs.status -> outcome; anything else (queued, sending, local_preparation, undoing) is still on its way
JOB_OUTCOME = {'sent': 'done', 'blocked': 'refused', 'failed': 'failed', 'uncertain': 'failed', 'finish_uncertain': 'failed',
               'cancelled': 'undone', 'undone': 'undone'}
AGENTS = {'claude': 'Claude Code', 'claude_code': 'Claude Code', 'codex': 'Codex'}

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


def _tables(db):
    return {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def _clip(text, n=160):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= n else text[:n - 1].rstrip() + '…'


def account_label(account):
    """'Gmail · sam@acme.com': the service and the address or name it goes by."""
    service = str(account.get('service') or account.get('transport') or '')
    name = SERVICES.get(service) or service.replace('_', ' ').capitalize() or i18n.t('Connection')
    who = account.get('email') or account.get('label') or account.get('name') or account.get('slack_host') or ''
    return f'{name} · {who}' if who else name


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
                       (aid, str(account.get('service') or ''), account_label(account), None if first else at))
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


def _jobs(db, config, limit, tables, kinds):
    accounts = {a.get('id'): a for a in (config or {}).get('accounts') or [] if isinstance(a, dict)}
    follow_ups = 'follow_up_sends' in tables
    rows = db.execute('SELECT j.id,j.suggestion_id,j.payload,j.status,j.source,j.created_at,j.updated_at,s.title,'
                      + ('(SELECT 1 FROM follow_up_sends f WHERE f.job_id=j.id) fu ' if follow_ups else '0 fu ')
                      + 'FROM action_jobs j LEFT JOIN suggestions s ON s.id=j.suggestion_id '
                      "WHERE json_extract(j.payload,'$.kind') IN (" + ','.join('?' * len(kinds)) + ') '
                      'ORDER BY j.created_at DESC LIMIT ?', (*kinds, limit))
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
        where = account_label(account) if account else ({'calendar': i18n.t('Calendar'), 'fixes': 'The Machine'}.get(kind)
                                                       or (_clip(p.get('from'), 80) or None))
        if kind == 'docs' and not account and p.get('provider'):
            where = {'google': 'Google Docs', 'microsoft': 'Word'}.get(p['provider'])
        by = (i18n.t('Follow-up, sent by itself') if r['fu'] else i18n.t('By itself') if r['source'] == 'auto'
              else i18n.t('Approved by voice') if r['source'] == 'voice' else i18n.t('After your OK'))
        todo = {'id': r['suggestion_id'], 'title': _clip(r['title'], 120)} if r['title'] is not None else None
        yield _line(kind, r['id'], r['created_at'], what, outcome, status, where, by, todo)


def _agents(db, limit, tables):
    if 'agent_jobs' not in tables:
        return
    for r in db.execute('SELECT j.id,j.suggestion_id,j.tool,j.status,j.created_at,s.title FROM agent_jobs j '
                        'LEFT JOIN suggestions s ON s.id=j.suggestion_id ORDER BY j.created_at DESC LIMIT ?', (limit,)):
        name = AGENTS.get(r['tool'], str(r['tool'] or '').capitalize())
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


def _connections(db, limit, tables):
    if 'activity_accounts' not in tables:
        return
    for r in db.execute('SELECT account_id,label,added_at,removed_at FROM activity_accounts WHERE added_at IS NOT NULL OR removed_at IS NOT NULL '
                        "ORDER BY max(coalesce(added_at,''),coalesce(removed_at,'')) DESC LIMIT ?", (limit,)):
        if r['removed_at']:
            yield _line('connections', 'removed:' + r['account_id'], r['removed_at'], i18n.t('Connection removed'), 'done', i18n.t('Removed'), r['label'])
        if r['added_at']:
            yield _line('connections', 'added:' + r['account_id'], r['added_at'], i18n.t('Connection added'), 'done', i18n.t('Added'), r['label'])


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
        raise ValueError('Not a page') from None
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
        'agents': lambda: _agents(db, size['agents'], tables),
        'fleet': lambda: _fleet(db, size['fleet'], tables),
        'learnings': lambda: _learnings(db, size['learnings'], tables),
        'skills': lambda: _skills(db, size['skills'], tables),
        'graph': lambda: _graph(db, size['graph'], tables),
        'connections': lambda: _connections(db, size['connections'], tables),
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
    items = lines[offset:offset + limit]
    more = len(lines) > offset + limit and offset + limit < MAX_OFFSET
    return {'items': items, 'next': offset + limit if more else None, 'kinds': [k for k in KINDS if k in kinds]}

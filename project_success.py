"""When a project is done, and what stands in its way (2026-11-02).

One workflow first: a partner listing that goes live (a board like "Partner listings": Contacted, Agreed, In review,
Live). Each project on it can carry a success condition in plain words ("Listing is live at a URL with a link to us"),
which a review suggests and the owner can change in the project dialog. The condition says what proves it:

- 'link': a message from the other side gives the listing's address, and The Machine opens it: it loads (https, a
  public address) and links to one of the owner's own domains;
- 'message': a message from the other side says it happened (the review judges what it means).

A review (finish_analysis stages, or graph placing a project) that moves such a project to its board's last stage
gives that message; without proof the project stays one stage before (gate), so a project is only done with its
evidence linked on it. The owner can still mark it done by hand (Won, or a drag), which always stands.

The same review run keeps an eye on the open ones (monitor, no loop of its own): no reply for NO_REPLY_DAYS, an
overdue promise on it (the owner's, or theirs that they are late with). A blocker with a clear next step gets one
to-do, only when the project has no open to-do already, and never one that sends anything: the owner sees it first.
"""
import datetime as dt
import json
import re
import sqlite3

import graph

PROOFS = ('link', 'message')
NO_REPLY_DAYS = graph.STUCK_DAYS
PAGE_BYTES = 2_000_000
MAX_LINKS = 3           # links opened per review call
MONITOR_LIMIT = 60      # projects with a condition looked at per review run
SCHEMA = '''CREATE TABLE IF NOT EXISTS project_success(project_id INTEGER PRIMARY KEY,condition TEXT,proof TEXT NOT NULL DEFAULT 'message',
  condition_by TEXT,condition_at TEXT,evidence_event_id INTEGER,evidence_url TEXT,evidence_at TEXT,evidence_note TEXT,
  blocker TEXT,blocker_at TEXT,todo_id TEXT,updated_at TEXT)'''
URL = re.compile(r'https://[^\s"\'<>()\[\]]+')


def ensure(db):
    db.execute(SCHEMA)


def forget(db, project_id):
    """A deleted project's condition, proof and blocker go with it."""
    ensure(db)
    db.execute('DELETE FROM project_success WHERE project_id=?', (int(project_id),))


def _row(db, project_id):
    return db.execute('SELECT * FROM project_success WHERE project_id=?', (int(project_id),)).fetchone()


def _put(db, project_id, now, **fields):
    db.execute('INSERT OR IGNORE INTO project_success(project_id,updated_at) VALUES(?,?)', (int(project_id), now))
    if fields:
        db.execute('UPDATE project_success SET ' + ','.join(f'{k}=?' for k in fields) + ',updated_at=? WHERE project_id=?',
                   (*fields.values(), now, int(project_id)))


def clean_condition(text):
    text = graph.one_line(text, 140)
    if text is None:
        raise ValueError('Done when: one short line (up to 140 characters), like "Listing is live with a link to us"')
    return text


def clean_proof(proof):
    proof = str(proof or 'message').strip().lower()
    if proof not in PROOFS:
        raise ValueError('proof is "link" (a page that must be live) or "message" (a message from them that says it)')
    return proof


def set_condition(db, project_id, condition, proof, source, now):
    """The owner's word stays: a review only fills a condition nobody set, or one a review set before."""
    ensure(db)
    row = _row(db, project_id)
    if source != 'owner' and row and row['condition_by'] == 'owner':
        return False
    condition = clean_condition(condition)
    if not condition:
        if source == 'owner':
            _put(db, project_id, now, condition=None, condition_by='owner', condition_at=now)
        return True
    _put(db, project_id, now, condition=condition, proof=clean_proof(proof if proof is not None else (row['proof'] if row else None)),
         condition_by=source, condition_at=now)
    return True


# ------------------------------------------------------------------ the proof

def _text(db, event_id):
    row = db.execute('SELECT title,body FROM events WHERE id=? AND deleted=0', (int(event_id),)).fetchone()
    return ' '.join(str(row[k] or '') for k in ('title', 'body')) if row else None


def _mine(db, event_id):
    row = db.execute("SELECT (json_extract(metadata,'$.from_me') IS 1 OR EXISTS(SELECT 1 FROM json_each(events.metadata,'$.labels') "
                     "WHERE value='SENT')) mine FROM events WHERE id=?", (int(event_id),)).fetchone()
    return bool(row and row['mine'])


def _clean_url(url):
    url = str(url or '').strip().rstrip('.,;:!?')
    if not URL.fullmatch(url):
        return None
    head, _, rest = url[8:].partition('/')
    return 'https://' + head.lower() + '/' + rest


def _in_text(url, text):
    """The address as the message gives it (a review never makes one up)."""
    found = {_clean_url(u) for u in URL.findall(text or '')}
    return url in found or url.rstrip('/') in {(u or '').rstrip('/') for u in found}


def _owner_domains(db, accounts):
    try:
        return graph.Owner({'accounts': accounts or []}, db).domains
    except (sqlite3.Error, KeyError, TypeError, ValueError):
        return set()


def page_links_to(data, domains):
    """A loaded page links to (or names) one of the owner's domains; any page counts when none are known."""
    if not domains:
        return True
    text = data.decode('utf-8', 'replace').lower() if isinstance(data, bytes) else str(data or '').lower()
    return any(re.search(r'(?<![a-z0-9-])' + re.escape(d.lower()) + r'(?![a-z0-9-]|\.[a-z0-9])', text) for d in domains)


def fetch_page(url):
    import enrichment
    got = enrichment._download(url, 'text/html,application/xhtml+xml', PAGE_BYTES, timeout=10, redirects=3)
    return got[0] if got and (got[1] or '').startswith(('text/html', 'application/xhtml')) else None


def check_links(connect, accounts, entries, fetch=None):
    """Open the pages a review gives as proof, before its write transaction: {url: (ok, why)}. Only an https address
    that is in the move's own message is opened, to a public address (enrichment._download), at most MAX_LINKS."""
    fetch = fetch or fetch_page
    wanted = []
    for m in entries or ():
        url = _clean_url(m.get('url')) if isinstance(m, dict) else None
        if url and str(m.get('event_id') or '').isdigit() and url not in [w[0] for w in wanted]:
            wanted.append((url, int(m['event_id'])))
    if not wanted:
        return {}
    out = {}
    with connect() as db:
        domains = _owner_domains(db, accounts)
        said = {url: _in_text(url, _text(db, event_id)) for url, event_id in wanted}
    for url, _ in wanted[:MAX_LINKS]:
        if not said[url]:
            out[url] = (False, 'unsaid')
            continue
        try:
            page = fetch(url)
        except Exception:  # noqa: BLE001 - any failure to load is 'unloaded'
            page = None
        if page is None:
            out[url] = (False, 'unloaded')
        elif not page_links_to(page, domains):
            out[url] = (False, 'unlinked')
        else:
            out[url] = (True, None)
    return out


def _project(db, ref):
    ref = str(ref or '').strip()
    if ref.startswith('project:') and ref[8:].isdigit():
        return db.execute('SELECT * FROM projects WHERE id=?', (int(ref[8:]),)).fetchone()
    return db.execute('SELECT * FROM projects WHERE name=? COLLATE NOCASE', (ref,)).fetchone() if ref else None


def _board(db, m, row):
    if m.get('board'):
        return db.execute('SELECT * FROM boards WHERE name=? COLLATE NOCASE', (str(m['board']).strip(),)).fetchone()
    return db.execute('SELECT * FROM boards WHERE id=?', (row['board_id'],)).fetchone() if row and row['board_id'] else None


def gate(db, m, checked):
    """A review's move (a finish_analysis stages entry, or graph's) before it is made: (move, verdict). A move to the
    board's last stage on a project with a condition needs its proof; without it the move goes one stage before, and
    verdict says why ({'proven': False, 'why'}). verdict is None when there is nothing to prove."""
    ensure(db)
    row = _project(db, m.get('project'))
    board = _board(db, m, row)
    if not board:
        return m, None
    main = [s['name'] for s in json.loads(board['stages'])]
    if str(m.get('stage') or '').strip().casefold() != main[-1].casefold():
        return m, None
    saved = _row(db, row['id']) if row else None
    condition = (saved['condition'] if saved and saved['condition_by'] == 'owner' else None) or graph.one_line(m.get('condition'), 140) or (
        saved['condition'] if saved else None)
    if not condition:
        return m, None  # no condition: as before
    # The proof the condition was saved with stands (a review can't swap a page check for a message); a new one's own
    proof = saved['proof'] if saved and saved['condition'] else (m.get('proof') if m.get('proof') in PROOFS else 'link' if m.get('url') else 'message')
    event_id = int(m['event_id']) if str(m.get('event_id') or '').isdigit() else None
    why = None
    if event_id is None or _text(db, event_id) is None:
        why = 'no_message'
    elif _mine(db, event_id):
        why = 'from_owner'
    elif proof == 'link':
        url = _clean_url(m.get('url'))
        ok, said = checked.get(url, (False, 'no_url' if not url else 'unloaded')) if url else (False, 'no_url')
        why = None if ok else said
    if why is None:
        return m, {'proven': True, 'proof': proof, 'event_id': event_id, 'url': _clean_url(m.get('url')) if proof == 'link' else None}
    before = main[-2] if len(main) > 1 else main[-1]
    at = (row['stage'] or '') if row and row['board_id'] == board['id'] else ''
    hold = at if at and at in main[:-1] and main.index(at) > main.index(before) else before
    if at.casefold() == main[-1].casefold():
        hold = at
    return {**m, 'stage': hold}, {'proven': False, 'why': why}


def after_move(db, m, result, verdict, now):
    """What a review's move says about the condition: a condition it suggests, the proof it gave, or why not."""
    ensure(db)
    row = _project(db, (result or {}).get('node_id') or m.get('project'))
    if not row:
        return
    if graph.one_line(m.get('condition'), 140):
        set_condition(db, row['id'], m['condition'], m.get('proof') if m.get('proof') in PROOFS else None, 'review', now)
    if not verdict or (result or {}).get('kept'):
        return
    if verdict['proven']:
        record_proof(db, row['id'], verdict['event_id'], verdict['url'], now)
        saved = _row(db, row['id'])
        if saved and saved['todo_id'] and saved['condition']:
            from machine.store import outcomes
            try:  # the to-do made for its blocker has its result now: it closes, or looks done (outcomes.result_seen)
                outcomes.project_proof(db, saved['todo_id'], saved['condition'], verdict['event_id'], now)
            except sqlite3.OperationalError:
                pass  # a bare graph without the assistant's tables
    else:
        _put(db, row['id'], now, evidence_note=verdict['why'])


def record_proof(db, project_id, event_id, url, now):
    """The message (and the live page) that met the condition, linked on the project."""
    ensure(db)
    at = db.execute('SELECT occurred_at FROM events WHERE id=?', (int(event_id),)).fetchone()
    _put(db, project_id, now, evidence_event_id=int(event_id), evidence_url=url, evidence_at=at['occurred_at'] if at else now,
         evidence_note=None, blocker=None, blocker_at=None)


# ------------------------------------------------------------------ what stands in its way

def _event_ids(db, pid):
    return [r['id'] for r in graph.project_events(db, pid, 400)]


def _waiting(db, pid):
    """(event id, time) of the owner's first message since the other side last wrote, or None."""
    ids = _event_ids(db, pid)
    if not ids:
        return None
    first = None
    for r in db.execute(f"SELECT id,occurred_at,(json_extract(metadata,'$.from_me') IS 1 OR EXISTS(SELECT 1 FROM json_each(events.metadata,'$.labels') "
                        f"WHERE value='SENT')) mine FROM events WHERE id IN ({','.join('?' * len(ids))}) AND kind IN ({','.join('?' * len(graph.MESSAGE_KINDS))}) "
                        'ORDER BY occurred_at', (*ids, *graph.MESSAGE_KINDS)):
        first = (first or (r['id'], r['occurred_at'])) if r['mine'] else None
    return first


def _promises(db, pid, today):
    ids = _event_ids(db, pid)
    if not ids:
        return []
    try:
        return db.execute(f"SELECT id,direction,who,what,due,status,suggestion_id,event_id FROM promises WHERE event_id IN ({','.join('?' * len(ids))}) "
                          "AND status IN ('open','carded') AND due IS NOT NULL AND substr(due,1,10)<? ORDER BY due", (*ids, today)).fetchall()
    except sqlite3.OperationalError:
        return []  # a bare graph without the assistant's tables


def _open_todos(db, row):
    """The project's open to-dos (as its page lists them), newest first."""
    try:
        return [dict(r) for r in db.execute(f"SELECT s.id,s.title FROM suggestions s WHERE s.status IN ({','.join('?' * len(graph.OPEN_CARD))}) AND "
                                            f"{graph._project_cards_where()} ORDER BY s.created_at DESC LIMIT 5",
                                            (*graph.OPEN_CARD, row['name'], 'project:' + str(row['id'])))]
    except sqlite3.OperationalError:
        return []  # a bare graph without the assistant's tables


def _follow_ups_on(db, row, board):
    try:
        import follow_ups
        settings, _ = follow_ups.effective(db, row)
        return bool(settings and settings.get('on') and follow_ups.stage_rule(settings, board, row['stage'])[0])
    except (sqlite3.Error, ImportError, KeyError, TypeError, ValueError):
        return False


def blocker(db, row, board, now):
    """What stands in the way of an open project, the most pressing first, or None."""
    today = graph.parse_time(now).date().isoformat()
    for p in _promises(db, row['id'], today):
        return {'kind': 'promise_' + ('mine' if p['direction'] == 'mine' else 'theirs'), 'who': p['who'], 'what': p['what'],
                'due': p['due'][:10], 'promise_id': p['id'], 'event_id': p['event_id']}
    waiting = _waiting(db, row['id'])
    if waiting:
        days = (graph.parse_time(now) - graph.parse_time(waiting[1])).days
        if days >= NO_REPLY_DAYS:
            return {'kind': 'no_reply', 'days': days, 'event_id': waiting[0], 'follow_ups': _follow_ups_on(db, row, board)}
    return None


def action(row, found, condition):
    """The one to-do a blocker with a clear next step asks for, or None (follow-ups already chase a quiet one)."""
    import i18n
    kind = found['kind']
    if kind == 'no_reply' and found.get('follow_ups'):
        return None
    if kind == 'no_reply':
        title = i18n.t('Nudge {}: no reply in {} days', row['name'], found['days'])
    elif kind == 'promise_theirs':
        title = i18n.t('Ask {} about: {}', found['who'], found['what'])
    else:
        title = i18n.t('Overdue for {}: {}', found['who'], found['what'])
    return {'project_id': row['id'], 'project': row['name'], 'title': title[:89],
            'body': i18n.t('Done when: {}', condition)[:690], 'event_ids': [found['event_id']], 'condition': condition,
            'dedupe': f"project-success:{row['id']}:{kind}:{found.get('promise_id') or found['event_id']}"}


def monitor(db, now, limit=MONITOR_LIMIT):
    """Run with each review: the blocker on every open project with a condition, kept on it for its page, and the
    to-dos that are needed ([action]): one per project at most, only when it has no open to-do."""
    ensure(db)
    actions = []
    for s in db.execute('SELECT s.*,p.name,p.board_id,p.stage,p.outcome,p.closed_at FROM project_success s JOIN projects p ON p.id=s.project_id '
                        "WHERE s.condition IS NOT NULL AND s.condition<>'' AND p.closed_at IS NULL AND p.board_id IS NOT NULL AND p.outcome IS NULL "
                        'ORDER BY s.updated_at LIMIT ?', (limit,)).fetchall():
        board = db.execute('SELECT * FROM boards WHERE id=?', (s['board_id'],)).fetchone()
        main = [x['name'] for x in json.loads(board['stages'])] if board else []
        row = db.execute('SELECT * FROM projects WHERE id=?', (s['project_id'],)).fetchone()
        if not main or s['stage'] in (main[-1], graph.STALLED):
            found = None  # done, or stalled: nothing to chase
        else:
            found = blocker(db, row, board, now)
        todo_id = s['todo_id']
        if found:
            todos = _open_todos(db, row)
            if todos:
                found['todo'] = todos[0]['id']
            else:
                wanted = action(row, found, s['condition'])
                if wanted:
                    actions.append(wanted)
        old = json.loads(s['blocker']) if s['blocker'] else None
        if (old or None) != (found or None):
            _put(db, s['project_id'], now, blocker=json.dumps(found) if found else None, blocker_at=now if found else None, todo_id=todo_id)
        else:
            db.execute('UPDATE project_success SET updated_at=? WHERE project_id=?', (now, s['project_id']))
    return actions


def linked(db, project_id, todo_id, now):
    """The to-do made for a blocker: shown with it."""
    row = _row(db, project_id)
    found = json.loads(row['blocker']) if row and row['blocker'] else None
    if found is not None:
        found['todo'] = todo_id
    _put(db, project_id, now, todo_id=todo_id, blocker=json.dumps(found) if found else None)


# ------------------------------------------------------------------ the project page

def view(db, project_id, stage=None, stages=None, stage_by=None, outcome=None):
    """{'condition', 'proof', 'by', 'done', 'done_by', 'evidence', 'not_proven', 'blocker'} for a project's page, or None."""
    try:
        ensure(db)
        s = _row(db, project_id)
    except sqlite3.Error:
        return None
    if not s or not (s['condition'] or s['evidence_event_id']):
        return None
    last = (stages or [None])[-1] if stages else None
    done = outcome == 'won' or bool(last and stage == last)
    evidence = {'event_id': s['evidence_event_id'], 'url': s['evidence_url'], 'at': s['evidence_at']} if s['evidence_event_id'] else None
    done_by = None
    if done:
        done_by = 'owner' if outcome == 'won' or stage_by == 'owner' or not evidence else 'evidence'
    found = json.loads(s['blocker']) if s['blocker'] and not done else None
    if found and found.get('todo'):
        todo = db.execute('SELECT id,title FROM suggestions WHERE id=?', (found['todo'],)).fetchone() if graph._has_column(db, 'suggestions', 'title') else None
        found['todo'] = {'id': todo['id'], 'title': todo['title']} if todo else None
    return {'condition': s['condition'], 'proof': s['proof'], 'by': s['condition_by'], 'done': done, 'done_by': done_by,
            'evidence': evidence, 'not_proven': s['evidence_note'] if not done and s['evidence_note'] else None, 'blocker': found}

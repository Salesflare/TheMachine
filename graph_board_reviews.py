"""What a review does for the Projects boards, and the owner's answer to it: sorting projects the owner put on a board
onto a stage (sort_brief, sort_answer and the tile's sort_view), checking projects on no board against the boards
(fit_brief, fit_answer), a new board's look through the history (backfill_*), and Add or Leave out on the maybes they
leave, with Undo (decide_fit, undo_fit). Moved out of graph.py (its line budget); the tables stay graph.py's."""
import collections
import datetime as dt
import json
import secrets
import sqlite3

import graph
import timeutil

SORT_TRIES = 3          # reviews that get an unplaced project before its tile says sorting failed
SORT_BATCH = 12         # projects to sort per review
SORT_MESSAGES = 6       # each one's latest messages shown to the review
FIT_BATCH = 40          # projects on no board a review checks against the boards at a time
FIT_FRESH_MINUTES = 30  # a board saved this recently starts a review for its check at once
# A new board looks through the whole history once (2026-10-24): every organization (or person without one) with
# messages or meetings in no project yet is checked against it, BACKFILL_BATCH at a time in each review, the likeliest
# first (by meaning, when there are local embeddings), at most BACKFILL_MAX per board.
BACKFILL_BATCH = 30
BACKFILL_MAX = 400
BACKFILL_CHARS = 14000  # the block's size in one review
BACKFILL_SHOWN_DAYS = 3  # the board says what it found for this long
BACKFILL_GIVE_UP_DAYS = 7
BACKFILL_KINDS = ('gmail.message', 'salesflare.email', 'linkedin.message', 'slack.message', 'teams.message', 'whatsapp.message', 'telegram.message', 'intercom.conversation', 'x.dm',
                  'ms_graph.message', 'outlook.message', 'calendar.event', 'salesflare.meeting', 'outlook.event', 'ms_graph.event')


def unsorted_projects(db, limit=None):
    """Open projects the owner put on a board that no review or move has placed yet and no review has
    answered for, while reviews still try (fewer than SORT_TRIES got them): what the next review sorts first."""
    return db.execute('SELECT p.*,b.name board FROM projects p JOIN boards b ON b.id=p.board_id WHERE p.closed_at IS NULL AND p.stage_by IS NULL '
                      'AND p.sort_note IS NULL AND p.sort_tries<? ORDER BY p.sort_tries,p.id' + (' LIMIT ?' if limit else ''),
                      (SORT_TRIES, *((limit,) if limit else ()))).fetchall()


def sort_brief(db, run_id, limit=SORT_BATCH, per=SORT_MESSAGES):
    """The "Boards to sort" block for review run_id: each unplaced project with its board, stages and latest
    messages (event_ids to read). Marks them as given to this run, so finish_analysis can hold it to an answer
    (sort_answer) and the tile can tell a failed run. A project with no messages at all gets its note now."""
    lines = []
    for p in unsorted_projects(db, limit):
        node = 'project:' + str(p['id'])
        events = graph.project_events(db, p['id'], per)
        if not events:
            db.execute("UPDATE projects SET sort_note='No messages about it yet',sort_run=? WHERE id=?", (run_id, p['id']))
            continue
        board = db.execute('SELECT * FROM boards WHERE id=?', (p['board_id'],)).fetchone()
        db.execute('UPDATE projects SET sort_run=?,sort_tries=sort_tries+1 WHERE id=?', (run_id, p['id']))
        said = ', '.join(f"{e['id']} ({e['kind']}, {timeutil.local_day_text(e['occurred_at'])})" for e in events)
        lines.append(f"- {p['name']} ({node}) on {p['board']} ({' > '.join(graph.stage_names(board))}); its latest messages, newest first: {said}")
    return '\n'.join(lines)


def sort_answer(db, run_id, answer):
    """A review that got "Boards to sort" answers for each project before it finishes: placed with graph (stage,
    event_id, reason), or in finish_analysis sorted [{"project": node_id, "why"}] when no message shows where it
    stands. Raises while one is left; returns how many it couldn't place."""
    given = db.execute('SELECT id,name FROM projects WHERE sort_run=? AND stage_by IS NULL AND sort_note IS NULL AND board_id IS NOT NULL '
                       'AND closed_at IS NULL', (run_id,)).fetchall()
    if not given:
        return 0
    if answer is not None and not (isinstance(answer, list) and all(isinstance(a, dict) for a in answer)):
        raise ValueError('sorted is [{"project": "project:<id>", "why": "<a few words>"}]')
    why = {}
    for a in answer or []:
        ref, text = str(a.get('project') or ''), graph.one_line(a.get('why'), 120)
        if not text:
            raise ValueError('sorted: each one says why no message shows where it stands, in a few words')
        why[ref.casefold()] = text
    left, done = [], 0
    for r in given:
        text = why.get(('project:' + str(r['id'])).casefold()) or why.get(r['name'].casefold())
        if text:
            db.execute('UPDATE projects SET sort_note=? WHERE id=?', (text, r['id']))
            done += 1
        else:
            left.append(f"{r['name']} (project:{r['id']})")
    if left:
        raise ValueError('Boards to sort: place ' + ', '.join(left) + ' with graph (project, board, stage, event_id, reason), the first stage when '
                         'nothing has moved it further; or add it to finish_analysis sorted [{"project", "why"}] when no message shows where it stands')
    return done


def sort_view(db, p):
    """The tile's sorting fields: sorting (a review is due or at it), sort_note (why a review couldn't place it) or
    sort_failed (what went wrong); all off once the project is placed."""
    if p['stage_by']:
        return {'sorting': False}
    state, text = sort_state(db, p)
    return {'sorting': state == 'sorting', **({'sort_note': text} if state == 'note' else {}), **({'sort_failed': text} if state == 'failed' else {})}


def sort_state(db, p):
    """How an unplaced project's tile reads: ('sorting', None) while a review is due or at it, ('note', why) when a
    review couldn't place it, ('failed', what happened) when the reviews that got it failed or gave up."""
    if p['sort_note']:
        return 'note', p['sort_note']
    run = None
    if p['sort_run']:
        try:
            run = db.execute('SELECT status FROM review_runs WHERE run_id=?', (p['sort_run'],)).fetchone()
        except sqlite3.OperationalError:
            run = None
    if (p['sort_tries'] or 0) >= SORT_TRIES:
        return 'failed', f"Couldn't sort it in {p['sort_tries']} checks"
    if run and run['status'] not in ('starting', 'running', 'recovering', 'ok'):
        return 'failed', 'Sorting failed, trying again'
    return 'sorting', None


def fit_brief(db, run_id, now, limit=FIT_BATCH):
    """The "Projects that may fit a board" block for review run_id: open projects on no board that weren't checked
    against every board with an about yet. Marks them as given to this run (board_fits with fit 'asked')."""
    boards_ = db.execute("SELECT * FROM boards WHERE about IS NOT NULL AND about<>'' ORDER BY id").fetchall()
    if not boards_:
        return ''
    rows = db.execute('SELECT p.id,p.name FROM projects p WHERE p.board_id IS NULL AND p.closed_at IS NULL AND EXISTS(SELECT 1 FROM boards b '
                      "WHERE b.about IS NOT NULL AND b.about<>'' AND NOT EXISTS(SELECT 1 FROM board_fits f WHERE f.board_id=b.id AND f.project_id=p.id "
                      "AND f.fit<>'asked')) ORDER BY p.created_at DESC LIMIT ?", (limit,)).fetchall()
    if not rows:
        return ''
    for r in rows:
        for b in boards_:
            db.execute("INSERT INTO board_fits(board_id,project_id,fit,run_id,created_at) VALUES(?,?,'asked',?,?) ON CONFLICT(board_id,project_id) "
                       "DO UPDATE SET run_id=excluded.run_id WHERE fit='asked'", (b['id'], r['id'], run_id, now))
    lines = [f"Boards: " + '; '.join(f"{b['name']} ({' > '.join(graph.stage_names(b))}): {b['about']}" for b in boards_)]
    for r in rows:
        people = [p['name'] for p in db.execute("SELECT n.name FROM graph_links l JOIN graph_nodes n ON n.id=l.a WHERE l.b=? AND l.kind='project' "
                                                "ORDER BY l.strength DESC LIMIT 2", ('project:' + str(r['id']),))]
        lines.append(f"- {r['name']} (project:{r['id']})" + (f" with {', '.join(people)}" if people else ''))
    return '\n'.join(lines)


def fits_said(db, answer, asked, check):
    """A review's finish_analysis fits, per (reference, board id): (fit, why, split). A fit names its board; one without
    a board counts only for something asked about one board in this run (asked: {reference: {board ids}}), so a maybe
    meant for one board never shows on the others."""
    names = {r['name'].casefold(): r['id'] for r in db.execute('SELECT id,name FROM boards')}
    said = {}
    for a in answer or []:
        fit, why = str(a.get('fit') or '').lower(), graph.one_line(a.get('why'), 160)
        if check and (fit not in ('maybe', 'no') or not why):
            raise ValueError('fits: each one has fit "maybe" or "no" and why, in a few words (placing one that fits is graph project, board, stage)')
        if fit not in ('maybe', 'no') or not why:
            continue
        ref = str(a.get('project') or a.get('who') or '').strip().casefold()
        if a.get('board'):
            boards_ = [names.get(str(a.get('board')).strip().casefold())]
        else:
            boards_ = list(asked.get(ref, ())) if len(asked.get(ref, ())) == 1 else []
        for b in boards_:
            if b:
                said[(ref, b)] = (fit, why, 1 if fit == 'maybe' and a.get('split') is True else None)
    return said


def fit_answer(db, run_id, answer):
    """A review that got "Projects that may fit a board" answers for each before it finishes: placed on a board with
    graph (it fits), or finish_analysis fits [{"project", "board", "fit": "maybe" or "no", "why"}]. A maybe shows on
    the board as one the owner can add. Raises while one is left; returns how many it answered."""
    asked = db.execute("SELECT f.board_id,f.project_id,p.name,p.board_id on_board FROM board_fits f JOIN projects p ON p.id=f.project_id "
                       "WHERE f.run_id=? AND f.fit='asked'", (run_id,)).fetchall()
    if not asked:
        return 0
    if answer is not None and not (isinstance(answer, list) and all(isinstance(a, dict) for a in answer)):
        raise ValueError('fits is [{"project": "project:<id>", "board", "fit": "maybe" or "no", "why"}]')
    refs = collections.defaultdict(set)
    for r in asked:
        refs['project:' + str(r['project_id'])].add(r['board_id'])
        refs[r['name'].casefold()].add(r['board_id'])
    said = fits_said(db, answer, refs, True)
    left = []
    for r in asked:
        if r['on_board']:  # placed with graph (or by the owner meanwhile)
            db.execute("UPDATE board_fits SET fit=?,state='added' WHERE board_id=? AND project_id=?",
                       ('yes' if r['on_board'] == r['board_id'] else 'no', r['board_id'], r['project_id']))
            continue
        got = said.get(('project:' + str(r['project_id']), r['board_id'])) or said.get((r['name'].casefold(), r['board_id']))
        if got:
            db.execute('UPDATE board_fits SET fit=?,why=?,split=? WHERE board_id=? AND project_id=?', (*got, r['board_id'], r['project_id']))
        else:
            left.append(f"{r['name']} (project:{r['project_id']})")
    if left:
        raise ValueError('Projects that may fit a board: place ' + ', '.join(dict.fromkeys(left)) + ' with graph (project, board, stage, event_id, reason) '
                         'when it clearly fits, or add it to finish_analysis fits [{"project", "board", "fit": "maybe" or "no", "why"}], one per board it was '
                         'asked about, each naming its board')
    return len(asked)


def fit_due(db, now):
    """A board saved in the last FIT_FRESH_MINUTES with projects on no board not yet checked against it: start a review now."""
    since = (graph.parse_time(now) - dt.timedelta(minutes=FIT_FRESH_MINUTES)).isoformat()
    return bool(db.execute("SELECT 1 FROM boards b WHERE b.about IS NOT NULL AND b.about<>'' AND coalesce(b.updated_at,b.created_at)>=? AND EXISTS("
                           "SELECT 1 FROM projects p WHERE p.board_id IS NULL AND p.closed_at IS NULL AND NOT EXISTS(SELECT 1 FROM board_fits f "
                           "WHERE f.board_id=b.id AND f.project_id=p.id AND f.fit<>'asked'))", (since,)).fetchone())


def board_maybes(db, board_id):
    """Projects a review thought could belong on this board, for the owner to add or leave out."""
    found = []
    for r in db.execute("SELECT f.project_id,f.why,f.split,p.name FROM board_fits f JOIN projects p ON p.id=f.project_id WHERE f.board_id=? AND f.fit='maybe' "
                        "AND f.state='open' AND p.board_id IS NULL AND p.closed_at IS NULL ORDER BY f.created_at DESC LIMIT 100", (board_id,)):
        found.append({'id': 'project:' + str(r['project_id']), 'name': r['name'], 'why': r['why']})
        parts = len(split_plan(db, r['project_id'])) if r['split'] else 0
        if parts >= 2:  # Add makes one project per counterpart
            found[-1]['split'] = parts
    # and organizations or people from the look through the history with no project yet (Add makes one)
    return found + [{'id': r['key'], 'name': r['name'], 'why': r['why']} for r in db.execute(
        "SELECT a.key,a.name,a.why FROM board_backfill_asks a WHERE a.board_id=? AND a.fit='maybe' AND a.state='open' AND (a.project_id IS NULL OR "
        "EXISTS(SELECT 1 FROM projects p WHERE p.id=a.project_id AND p.board_id IS NULL AND p.closed_at IS NULL)) AND NOT EXISTS(SELECT 1 FROM json_each(a.event_ids) j "
        "JOIN event_projects ep ON ep.event_id=j.value JOIN projects p ON p.id=ep.project_id WHERE p.board_id IS NOT NULL OR p.id IS NOT a.project_id) "
        'ORDER BY a.created_at DESC LIMIT 100', (board_id,))]


UNDO_COLUMNS = ('board_id', 'org', 'org_by', 'stage', 'stage_event_id', 'stage_by', 'stage_at', 'sort_run', 'sort_tries', 'closed_at')  # no message text: steps are stored unsealed


def counterpart_keys(db, event_ids):
    """Who each message is with, outside the owner's team: {event_id: [key]} with the organization's node id as key, or
    the person's when they have none (as the look through the history keys them)."""
    out = collections.defaultdict(list)
    ids = [int(i) for i in event_ids]
    for i in range(0, len(ids), 500):
        part = ids[i:i + 500]
        for r in db.execute("SELECT g.event_id,n.id person,json_extract(n.info,'$.org') org FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id "
                            f"WHERE g.event_id IN ({','.join('?' * len(part))}) AND n.kind='person' AND g.probable=0 "
                            "AND json_extract(n.info,'$.colleague') IS NOT 1 ORDER BY g.event_id,n.id", part):
            key = r['org'] if str(r['org'] or '').startswith('org:') else r['person']
            if key not in out[r['event_id']]:
                out[r['event_id']].append(key)
    return out


def split_plan(db, project_id):
    """How Add splits a project that bundles several counterparts (a review said so): one part per organization (or
    person without one) its messages are with, each going into the open project already with them when there is one
    (no duplicates), else a new one named after the counterpart ("<project>: <counterpart>" when that name is taken).
    [{name, key, event_ids, project_id or None}]; fewer than
    two parts means it is one project after all."""
    row = db.execute('SELECT * FROM projects WHERE id=?', (int(project_id),)).fetchone()
    ids = [r[0] for r in db.execute('SELECT ep.event_id FROM event_projects ep JOIN events e ON e.id=ep.event_id WHERE ep.project_id=? AND e.deleted=0 '
                                    'ORDER BY e.occurred_at,e.id', (row['id'],))]
    keys = counterpart_keys(db, ids)
    count = collections.Counter(k for e in ids for k in keys.get(e, ()))
    parts = {}
    for e in ids:
        if keys.get(e):
            key = max(keys[e], key=lambda k: (count[k], k))  # a message with two counterparts goes with the one most of the project is with
            parts.setdefault(key, []).append(e)
    if len(parts) < 2:
        return []
    names = {r['id']: r['name'] for r in db.execute(f"SELECT id,name FROM graph_nodes WHERE id IN ({','.join('?' * len(parts))})", list(parts))}
    owners = {}  # the open project each counterpart is with already
    for r in db.execute('SELECT id,org,board_id FROM projects WHERE closed_at IS NULL AND org IS NOT NULL AND id<>? ORDER BY board_id IS NULL,id', (row['id'],)):
        owners.setdefault('org:' + r['org'], r['id'])
    for r in db.execute("SELECT l.a,json_extract(n.info,'$.org') org,p.id FROM graph_links l JOIN graph_nodes n ON n.id=l.a JOIN projects p ON 'project:'||p.id=l.b "
                        "WHERE l.kind='project' AND p.closed_at IS NULL AND p.id<>? AND n.kind='person' ORDER BY p.board_id IS NULL,p.id", (row['id'],)):
        owners.setdefault(r['a'], r['id'])
        if str(r['org'] or '').startswith('org:'):
            owners.setdefault(r['org'], r['id'])
    out, used = [], set()
    for key, events in sorted(parts.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        who = graph.one_line(names.get(key), 60) or (key[4:] if key.startswith('org:') else key.split(':', 1)[-1])
        # Named after the counterpart alone: the board it goes on names the rest. The bundle's name in front only when
        # that name is taken already (another project, or a second counterpart by the same name), so two never merge.
        name = who[:60].strip()
        if name.lower() in used or db.execute('SELECT 1 FROM projects WHERE name=? COLLATE NOCASE', (name,)).fetchone():
            name = f"{row['name'][:max(10, 58 - len(who))]}: {who}"[:60].strip()
        used.add(name.lower())
        out.append({'name': name, 'key': key, 'event_ids': events, 'project_id': owners.get(key)})
    return out


def counterpart_org(db, key):
    """The organization key of a look-through-the-history counterpart (an org:… node id), unless it is personal mail."""
    found = graph.org_key(key)
    return found if found and not graph.personal_mail(db, found) and not graph.own_domain(db, found) else None


def _remember(db, steps, project_id):
    if not any(s[0] == 'project' and s[1] == project_id for s in steps):
        row = db.execute(f"SELECT {','.join(UNDO_COLUMNS)} FROM projects WHERE id=?", (project_id,)).fetchone()
        steps.append(('project', project_id, dict(row)))


def _attach(db, target, event_ids, now, steps):
    """Label messages into a project (by id, or by name: made when new); remembers what to take back."""
    if isinstance(target, int):
        pid = target
    else:
        before = db.execute('SELECT id FROM projects WHERE name=? COLLATE NOCASE', (target,)).fetchone()
        if before:
            _remember(db, steps, before['id'])
        pid = graph.project_id(db, target, now)
        if not before:
            steps.append(('made', pid))
    have = {r[0] for r in db.execute('SELECT event_id FROM event_projects WHERE project_id=?', (pid,))}
    new = [int(e) for e in event_ids if int(e) not in have]
    db.executemany('INSERT OR IGNORE INTO event_projects(event_id,project_id,source,created_at) VALUES(?,?,?,?)', [(e, pid, 'owner', now) for e in new])
    if new and not any(s == ('made', pid) for s in steps):
        steps.append(('labels', pid, new))
    return pid


def _place(db, board, pid, steps, strict):
    """Onto the board's first stage, sorted from its messages by the next review. A project on another board stays
    there (strict: refuse)."""
    row = db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
    if row['board_id'] == board['id'] and not row['closed_at']:
        return False
    if row['board_id'] and row['board_id'] != board['id'] and not row['closed_at']:
        if strict:
            raise ValueError('It is on another board already')
        return False
    _remember(db, steps, pid)
    db.execute('UPDATE projects SET board_id=?,stage=?,stage_reason=NULL,stage_event_id=NULL,stage_by=NULL,stage_at=NULL,closed_at=NULL,' + graph.SORT_RESET + ' WHERE id=?',
               (board['id'], graph.stage_names(board)[0], pid))
    return True


def _split(db, board, row, now, steps):
    """Add on a project that bundles several counterparts: one project per counterpart on the board; the bundle closes
    once none of its messages is left over."""
    plan = split_plan(db, row['id'])
    if not plan:
        return None
    moved = {e for part in plan for e in part['event_ids']}
    gone = [tuple(r) for r in db.execute(f"SELECT event_id,project_id,source,created_at FROM event_projects WHERE project_id=? AND event_id IN ({','.join('?' * len(moved))})",
                                         (row['id'], *moved))]
    db.execute(f"DELETE FROM event_projects WHERE project_id=? AND event_id IN ({','.join('?' * len(moved))})", (row['id'], *moved))
    steps.append(('unlabels', gone))
    placed = 0
    for part in plan:
        pid = _attach(db, part['project_id'] or part['name'], part['event_ids'], now, steps)
        if counterpart_org(db, part['key']):
            had = db.execute('SELECT org,org_by FROM projects WHERE id=?', (pid,)).fetchone()
            if not had['org'] and not had['org_by']:
                _remember(db, steps, pid)
                db.execute("UPDATE projects SET org=?,org_by='auto' WHERE id=?", (counterpart_org(db, part['key']), pid))
        placed += _place(db, board, pid, steps, strict=False) or db.execute('SELECT board_id FROM projects WHERE id=?', (pid,)).fetchone()[0] == board['id']
    if not db.execute('SELECT 1 FROM event_projects WHERE project_id=?', (row['id'],)).fetchone():
        _remember(db, steps, row['id'])
        db.execute('UPDATE projects SET closed_at=? WHERE id=?', (now, row['id']))
    return placed


def _decide(db, board, node_id, add, now, steps, strict=True):
    node_id = str(node_id or '')
    if not node_id.startswith('project:'):
        ask = db.execute("SELECT * FROM board_backfill_asks WHERE board_id=? AND key=? AND fit='maybe'", (board['id'], node_id)).fetchone()
        if not ask:
            raise ValueError('That suggestion is gone')
        steps.append(('ask', board['id'], ask['key'], ask['state'], ask['project_id'], ask['decided_at']))
        pid = ask['project_id']
        if add and not pid:
            same = db.execute('SELECT board_id FROM projects WHERE name=? COLLATE NOCASE AND closed_at IS NULL', (ask['name'],)).fetchone()
            if same and same['board_id'] and same['board_id'] != board['id']:
                raise ValueError('A project by that name is on another board already')
            ids = [r[0] for r in db.execute('SELECT e.id FROM events e JOIN json_each(?) j ON j.value=e.id WHERE e.deleted=0', (ask['event_ids'],))]
            pid = _attach(db, ask['name'], ids, now, steps)
            if counterpart_org(db, ask['key']):
                db.execute("UPDATE projects SET org=?,org_by='auto' WHERE id=? AND org IS NULL AND org_by IS NULL", (counterpart_org(db, ask['key']), pid))
        db.execute('UPDATE board_backfill_asks SET state=?,decided_at=?,project_id=? WHERE board_id=? AND key=?',
                   ('added' if add else 'dismissed', now, pid, board['id'], ask['key']))
        if not add:
            return 0, None
        node_id = 'project:' + str(pid)
    row = graph.project_row(db, node_id)
    fit = db.execute('SELECT * FROM board_fits WHERE board_id=? AND project_id=?', (board['id'], row['id'])).fetchone()
    if fit:
        steps.append(('fit', board['id'], row['id'], fit['state'], fit['decided_at']))
    db.execute("UPDATE board_fits SET state=?,decided_at=? WHERE board_id=? AND project_id=?", ('added' if add else 'dismissed', now, board['id'], row['id']))
    if not add:
        return 0, row['id']
    if fit and fit['split'] and not row['board_id']:
        placed = _split(db, board, row, now, steps)
        if placed is not None:
            return placed, row['id']
    return int(_place(db, board, row['id'], steps, strict) or row['board_id'] == board['id']), row['id']


def decide_fit(db, board_id, node_id, add, now):
    """The owner adds maybes to the board (sorted from their messages next) or leaves them out for good: node_id, or
    node_ids for several at once. A maybe from the look through the history (an organization or person, no project
    yet) becomes a project; a project a review said bundles several counterparts becomes one per counterpart. Returns
    how many projects it put on the board and an undo token."""
    board = db.execute('SELECT * FROM boards WHERE id=?', (int(board_id or 0),)).fetchone()
    if not board:
        raise ValueError('That board is gone')
    many = isinstance(node_id, list)
    ids = list(dict.fromkeys(str(n) for n in node_id)) if many else [node_id]
    if not ids or len(ids) > 200:
        raise ValueError('Decide 1 to 200 at once')
    steps, placed, skipped, pid = [], 0, [], None
    for n in ids:
        if not many:
            got, pid = _decide(db, board, n, add, now, steps)
            placed += got
            continue
        db.execute('SAVEPOINT fit_one')
        mark = len(steps)
        try:
            placed += _decide(db, board, n, add, now, steps, strict=False)[0]
            db.execute('RELEASE fit_one')
        except ValueError:
            db.execute('ROLLBACK TO fit_one')
            db.execute('RELEASE fit_one')
            del steps[mark:]
            skipped.append(n)
    token = secrets.token_hex(8)
    db.execute('DELETE FROM board_fit_undo WHERE created_at<?', ((graph.parse_time(now) - dt.timedelta(days=1)).isoformat(),))
    db.execute('INSERT INTO board_fit_undo(token,board_id,steps,created_at) VALUES(?,?,?,?)', (token, board['id'], json.dumps(steps), now))
    out = {'added': bool(add), 'decided': len(ids) - len(skipped), 'projects': placed, 'skipped': len(skipped), 'undo': token}
    if not many:
        out['node_id'] = 'project:' + str(pid) if pid else str(node_id)
    return out


def undo_fit(db, token):
    """Take back one Add or Leave out (one or several at once) while its toast shows: the projects go back where they
    were, made ones go, split messages return to the bundle and the suggestions are open again."""
    row = db.execute('SELECT * FROM board_fit_undo WHERE token=?', (str(token or ''),)).fetchone()
    if not row:
        raise ValueError('Too late to undo that')
    steps = json.loads(row['steps'])
    for step in reversed(steps):
        kind = step[0]
        if kind == 'made':
            if db.execute('SELECT 1 FROM projects WHERE id=?', (step[1],)).fetchone():
                graph.delete_project(db, 'project:' + str(step[1]))
        elif kind == 'labels':
            db.execute(f"DELETE FROM event_projects WHERE project_id=? AND event_id IN ({','.join('?' * len(step[2]))})", (step[1], *step[2]))
        elif kind == 'unlabels':
            db.executemany('INSERT OR IGNORE INTO event_projects(event_id,project_id,source,created_at) VALUES(?,?,?,?)', [tuple(r) for r in step[1]])
        elif kind == 'project':
            cols = [c for c in UNDO_COLUMNS if c in step[2]]
            db.execute(f"UPDATE projects SET {','.join(c + '=?' for c in cols)} WHERE id=?", (*[step[2][c] for c in cols], step[1]))
        elif kind == 'fit':
            db.execute('UPDATE board_fits SET state=?,decided_at=? WHERE board_id=? AND project_id=?', (step[3], step[4], step[1], step[2]))
        elif kind == 'ask':
            db.execute('UPDATE board_backfill_asks SET state=?,project_id=?,decided_at=? WHERE board_id=? AND key=?', (step[3], step[4], step[5], step[1], step[2]))
    db.execute('DELETE FROM board_fit_undo WHERE token=?', (row['token'],))
    return {'undone': len(steps)}


def backfill_counterparts(db):
    """Who a new board's look through the history goes over: each organization (or person without one) the owner has
    messages or meetings with that are in no project yet, leaving out colleagues and anyone an open project is with
    already (no duplicates). {key (its graph node id): {name, people, event_ids newest first, first, last}}."""
    taken = {'org:' + r[0] for r in db.execute('SELECT org FROM projects WHERE closed_at IS NULL AND org IS NOT NULL')}
    for r in db.execute("SELECT l.a,json_extract(n.info,'$.org') org FROM graph_links l JOIN graph_nodes n ON n.id=l.a JOIN projects p ON 'project:'||p.id=l.b "
                        "WHERE l.kind='project' AND p.closed_at IS NULL AND n.kind='person' AND json_extract(n.info,'$.colleague') IS NOT 1"):
        taken.add(r['a'])
        if str(r['org'] or '').startswith('org:'):
            taken.add(r['org'])
    out, seen = {}, set()
    for r in db.execute("SELECT n.id person,n.name pname,json_extract(n.info,'$.org') org,e.id event_id,e.occurred_at,coalesce(json_extract(n.info,'$.wrote'),0) wrote,"
                        "coalesce(json_extract(n.info,'$.heard'),0) heard,coalesce(json_extract(n.info,'$.met'),0) met FROM graph_events g "
                        "JOIN graph_nodes n ON n.id=g.node_id JOIN events e ON e.id=g.event_id "
                        f"WHERE n.kind='person' AND g.probable=0 AND e.deleted=0 AND e.kind IN ({','.join('?' * len(BACKFILL_KINDS))}) "
                        "AND json_extract(n.info,'$.colleague') IS NOT 1 AND NOT EXISTS(SELECT 1 FROM event_projects ep WHERE ep.event_id=e.id) "
                        'ORDER BY e.occurred_at DESC,e.id DESC', BACKFILL_KINDS):
        key = r['org'] if str(r['org'] or '').startswith('org:') else r['person']
        if key in taken or r['person'] in taken:
            continue
        c = out.setdefault(key, {'name': None, 'people': [], 'event_ids': [], 'first': r['occurred_at'], 'last': r['occurred_at'], 'wrote': 0, 'heard': 0, 'met': 0, '_seen': set()})
        if r['person'] not in c['_seen']:  # how the owner and they talk: days the owner wrote, they wrote, they met (from the graph)
            c['_seen'].add(r['person'])
            for k in ('wrote', 'heard', 'met'):
                c[k] += int(r[k] or 0)
        if (key, r['event_id']) not in seen:
            seen.add((key, r['event_id']))
            c['event_ids'].append(r['event_id'])
            c['first'] = r['occurred_at']
        if r['pname'] not in c['people'] and len(c['people']) < 3:
            c['people'].append(r['pname'])
    keys = list(out)
    for i in range(0, len(keys), 500):
        part = keys[i:i + 500]
        for r in db.execute(f"SELECT id,name FROM graph_nodes WHERE id IN ({','.join('?' * len(part))})", part):
            out[r['id']]['name'] = r['name']
    for key, c in out.items():
        c.pop('_seen', None)
        c['name'] = (graph.one_line(c['name'], 60) or '') or (key[4:] if key.startswith('org:') else key.split(':', 1)[-1])[:60]
    return out


def backfill_pending(db):
    """Boards still looking through the history whose candidates aren't ranked yet: [(board row, its text)]."""
    return [(r, f"{r['name']}: {r['about'] or ''}") for r in db.execute(
        "SELECT b.* FROM board_backfills f JOIN boards b ON b.id=f.board_id WHERE f.state='running' AND f.ranked IS NULL ORDER BY b.id")]


def rank_backfill(db, board_id, scores=None):
    """The order a board's look goes through the counterparts: by meaning (scores, key -> higher is likelier) when the
    Machine has local embeddings, else the ones with the most messages first; at most BACKFILL_MAX."""
    found = backfill_counterparts(db)
    order = sorted(found, key=lambda k: ((scores or {}).get(k, -9), len(found[k]['event_ids']), found[k]['last']), reverse=True)
    db.execute("UPDATE board_backfills SET ranked=? WHERE board_id=? AND state='running'", (json.dumps(order[:BACKFILL_MAX]), board_id))
    return len(order[:BACKFILL_MAX])


def backfill_due(db, now=None):
    """A board is still looking through the history (and has something left to ask): reviews come sooner, while the
    model has room."""
    if now:
        backfill_settle(db, now)
    return bool(db.execute("SELECT 1 FROM board_backfills WHERE state='running' LIMIT 1").fetchone())


def backfill_settle(db, now):
    """A look is done once every counterpart it ranked has an answer (or got a project meanwhile) and every project on
    no board was checked against the board; after BACKFILL_GIVE_UP_DAYS it stops anyway."""
    found = None
    give_up = (graph.parse_time(now) - dt.timedelta(days=BACKFILL_GIVE_UP_DAYS)).isoformat()
    for f in db.execute("SELECT f.*,b.about FROM board_backfills f JOIN boards b ON b.id=f.board_id WHERE f.state='running' AND f.ranked IS NOT NULL").fetchall():
        if f['started_at'] >= give_up:
            found = backfill_counterparts(db) if found is None else found
            answered = {r[0] for r in db.execute("SELECT key FROM board_backfill_asks WHERE board_id=? AND fit<>'asked'", (f['board_id'],))}
            if any(k in found and k not in answered for k in json.loads(f['ranked'])):
                continue
            if (f['about'] or '').strip() and db.execute(
                    "SELECT 1 FROM projects p WHERE p.board_id IS NULL AND p.closed_at IS NULL AND NOT EXISTS(SELECT 1 FROM board_fits x "
                    "WHERE x.board_id=? AND x.project_id=p.id AND x.fit<>'asked')", (f['board_id'],)).fetchone():
                continue
        db.execute("UPDATE board_backfills SET state='done',finished_at=? WHERE board_id=?", (now, f['board_id']))


def backfill_brief(db, run_id, now, describe, batch=BACKFILL_BATCH, chars=BACKFILL_CHARS):
    """The "Looking through the history for new boards" block for review run_id: the next counterparts (the likeliest
    first) with a few of their messages, checked against each board still looking. Marks them as given to this run.
    describe(event_ids) gives a line per message."""
    backfill_settle(db, now)
    running = db.execute("SELECT f.board_id,f.ranked,b.* FROM board_backfills f JOIN boards b ON b.id=f.board_id "
                         "WHERE f.state='running' AND f.ranked IS NOT NULL ORDER BY b.id").fetchall()
    if not running:
        return ''
    found = backfill_counterparts(db)
    answered = {(r[0], r[1]) for r in db.execute("SELECT board_id,key FROM board_backfill_asks WHERE fit<>'asked'")}
    rank, wants = {}, collections.defaultdict(list)
    for b in running:
        for i, key in enumerate(json.loads(b['ranked'])):
            if key in found and (b['id'], key) not in answered:
                wants[key].append(b)
                rank[key] = min(rank.get(key, i), i)
    lines, size = [], 0
    for key in sorted(wants, key=rank.get)[:batch]:
        c = found[key]
        head = (f"- {c['name']} ({key}): {len(c['event_ids'])} message{'s' if len(c['event_ids']) != 1 else ''} or meeting"
                f"{'s' if len(c['event_ids']) != 1 else ''}, {c['first'][:10]} to {c['last'][:10]}"
                + (f", with {', '.join(c['people'])}" if c['people'] else '')
                + (f"; the owner wrote on {c['wrote']} day{'s' if c['wrote'] != 1 else ''}, they wrote on {c['heard']}, met {c['met']}"
                   if c['wrote'] or c['met'] else f"; inbound only: they wrote on {c['heard']} day{'s' if c['heard'] != 1 else ''}, the owner never wrote to or met them")
                + (f"; check against {', '.join(b['name'] for b in wants[key])} only" if len(wants[key]) < len(running) else ''))
        block = head + ''.join('\n    ' + line for line in describe(c['event_ids'][:4]))
        if lines and size + len(block) > chars:
            break
        lines.append(block)
        size += len(block)
        for b in wants[key]:
            db.execute("INSERT INTO board_backfill_asks(board_id,key,name,event_ids,fit,run_id,created_at) VALUES(?,?,?,?,'asked',?,?) "
                       "ON CONFLICT(board_id,key) DO UPDATE SET run_id=excluded.run_id,name=excluded.name,event_ids=excluded.event_ids WHERE fit='asked'",
                       (b['id'], key, c['name'], json.dumps(c['event_ids'][:60]), run_id, now))
    if not lines:
        return ''
    boards_line = 'Boards: ' + '; '.join(f"{b['name']} ({' > '.join(graph.stage_names(b))}{', only you' if b['visibility'] == 'only_you' else ', only you and chosen teammates' if b['visibility'] == 'people' else ''}): "
                                         f"{b['about'] or 'no description'}" for b in running)
    return boards_line + '\n' + '\n'.join(lines)


def backfill_answer(db, run_id, answer):
    """A review that got the look through the history answers for each counterpart before it finishes: made into a
    project on the board with graph (it fits), or finish_analysis fits [{"project": its key, "board", "fit": "maybe"
    or "no", "why"}]. A maybe waits on the board for Add or Leave out. Raises while one is left; returns how many."""
    asked = db.execute("SELECT * FROM board_backfill_asks WHERE run_id=? AND fit='asked'", (run_id,)).fetchall()
    if not asked:
        return 0
    if answer is not None and not (isinstance(answer, list) and all(isinstance(a, dict) for a in answer)):
        raise ValueError('fits is [{"project": "<its key>", "board", "fit": "maybe" or "no", "why"}]')
    refs = collections.defaultdict(set)
    for r in asked:
        refs[r['key'].casefold()].add(r['board_id'])
        refs[r['name'].casefold()].add(r['board_id'])
    said = fits_said(db, answer, refs, False)
    left = []
    for r in asked:
        ids = [int(i) for i in json.loads(r['event_ids'])]
        placed = db.execute(f"SELECT p.id,p.board_id FROM event_projects ep JOIN projects p ON p.id=ep.project_id WHERE ep.event_id IN ({','.join('?' * len(ids))}) "
                            'AND p.closed_at IS NULL ORDER BY p.board_id IS ? DESC LIMIT 1', (*ids, r['board_id'])).fetchone() if ids else None
        got = said.get((r['key'].casefold(), r['board_id'])) or said.get((r['name'].casefold(), r['board_id']))
        if placed and placed['board_id'] == r['board_id']:
            fit, why, state = 'yes', None, 'added'
        elif got:
            (fit, why, _), state = got, 'open'
        elif placed:  # made into a project for another board or none: that project gets its own check
            fit, why, state = 'other', None, 'open'
        else:
            left.append(f"{r['name']} ({r['key']})")
            continue
        db.execute('UPDATE board_backfill_asks SET fit=?,why=?,state=?,project_id=? WHERE board_id=? AND key=?',
                   (fit, why, state, placed['id'] if placed else None, r['board_id'], r['key']))
    if left:
        raise ValueError('Looking through the history: make ' + ', '.join(dict.fromkeys(left)) + ' a project on the board with graph (project, event_ids, '
                         'board, stage, event_id, reason) when it clearly fits, or add it to finish_analysis fits [{"project": its key, "board", '
                         '"fit": "maybe" or "no", "why"}], one per board it was asked about, each naming its board')
    return len(asked)


def backfill_view(db, board_id, now, maybes):
    """What the board header says about its look through the history: looking, or (for BACKFILL_SHOWN_DAYS after) how
    many it added and how many wait for the owner."""
    f = db.execute('SELECT * FROM board_backfills WHERE board_id=?', (board_id,)).fetchone()
    if not f:
        return None
    if f['state'] == 'running':
        return {'state': 'running'}
    if not f['finished_at'] or graph.parse_time(f['finished_at']) < graph.parse_time(now) - dt.timedelta(days=BACKFILL_SHOWN_DAYS):
        return None
    added = db.execute("SELECT count(*) FROM projects p WHERE p.board_id=? AND p.closed_at IS NULL AND EXISTS(SELECT 1 FROM project_moves m "
                       "WHERE m.project_id=p.id AND m.board_id=p.board_id AND m.source<>'owner' AND m.created_at>=?) AND NOT EXISTS("
                       "SELECT 1 FROM project_moves m WHERE m.project_id=p.id AND m.board_id=p.board_id AND m.created_at<?)",
                       (board_id, f['started_at'], f['started_at'])).fetchone()[0]
    added += db.execute("SELECT count(*) FROM board_backfill_asks a JOIN projects p ON p.id=a.project_id WHERE a.board_id=? AND a.fit='maybe' "
                        "AND a.state='added' AND p.board_id=? AND p.stage_by IS NULL", (board_id, board_id)).fetchone()[0]
    return {'state': 'done', 'added': added, 'review': len(maybes)}


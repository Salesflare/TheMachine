"""Automated follow-ups on Graph boards and projects (docs/help/follow-ups.md).

The owner turns them on for a whole board or for one project; a project's own setting overrides its board's (on with
its own settings, or off). One setting holds:

- days to max_days: wait at least `days` without a reply before a follow-up (DEFAULT_DAYS), and at most `max_days`
  (DEFAULT_MAX_DAYS): in between, a follow-up waits for room in the model's usage; at its longest wait it goes ahead
  like other background work.
- min to max: follow up at least `min` times (DEFAULT_MIN) when there's no reply, at most `max` times (DEFAULT_MAX).
  Up to the minimum a follow-up is always drafted (unless a stop condition holds); past it, the preparation judges from
  the thread and the project whether another one is still worth it (outcome follow_up:'stop' ends the round). Never
  past the maximum. After the last one (waited `days`, still no reply) it ends: the project gets a quiet "No reply
  after N follow-ups" and, with `stall` (on by default when the board has "Stalled or declined"), moves there.
- stages (boards): which stages get follow-ups. By default every open stage does; the last stage (done, won, live) and
  "Stalled or declined" don't. A stage can have its own minimum wait (Customize).
- channels: which of the owner's connected channels that can send may be used (None: all of them). A follow-up stays
  in the channel of the last message; switch (off by default) moves the next one to the next allowed channel where the
  conversation already is, once a follow-up got no reply.
- auto: Send without asking, an explicit standing approval for that board or project (off by default: every
  follow-up waits for the owner's Send). Careful (the owner's level, or a Careful Work Fleet) always asks.

A project is due (schedule) when the owner wrote last, nobody answered for `days`, it had fewer than `max` follow-ups
since their last reply, its stage is on, and it isn't won, lost, Stalled, archived or owned by a teammate (their own
Machine follows up, so two Machines never both do). A waiting point (the owner's last message) is followed up once at
most: follow_up_cards is UNIQUE on (project, that message); the follow-up the owner sends is the next waiting point.
Waiting points older than STALE_DAYS past their date are left alone: turning follow-ups on never chases old threads,
and a round only ends by itself (note, Stalled) after a follow-up that went out from here.

App.follow_up_step drafts in a low-priority background pass: only while no other preparation waits and the model's
usage has room (model_budget.follow_up_pause, which pauses before every other background work). It makes a to-do
prepared ahead by the normal preparation (the owner's voice, the last exchange, newer messages checked first) and the
draft is checked against earlier follow-ups so the same text never goes twice. A board's follow-ups show as one to-do
("8 follow-ups ready for <board>", reviewed one at a time); a project's own is a normal to-do. Sending goes through the
outbox (confirm_action), so a draft goes out once at most; Send without asking falls back to asking on anything
unusual (an earlier attempt on that to-do, a draft for another channel, no verified recipient, a repeated text).

Several follow-ups in a row (Send all checked, or Send without asking) go out spaced: the outbox (assistant.action_step)
holds the next follow-up from the same mailbox (or the same LinkedIn, WhatsApp... account) for a random SEND_GAP
seconds after the one before. Two mailboxes go side by side; a single follow-up goes at once. The spacing and the batch
are kept here (follow_up_sends, follow_up_pace), so after a restart the rest goes on with the same spacing and nothing
goes twice (a send that was under way is only checked, as for every outbox send). A failed one stays a to-do that asks;
the rest of the batch goes on. The dashboard shows each batch's progress ("Sending 3 of 8...", then "Sent 8").

Open follow-up to-dos close by themselves (settle) when the person replies, someone else answered or the owner wrote
again, the project is won, lost, Stalled, archived or its stage turned off, or follow-ups were turned off. Snoozing
the to-do holds it; Skip ends that round.

Tables (CREATE TABLE IF NOT EXISTS only: added beside the old ones, nothing existing changes, so a backup from before
restores as it was and one made after opens on an older version, which simply doesn't read them)."""
from __future__ import annotations

import datetime as dt
import difflib
import json
import random
import re

SCHEMA = '''
CREATE TABLE IF NOT EXISTS follow_up_rules(scope TEXT NOT NULL,ref INTEGER NOT NULL,settings TEXT NOT NULL,updated_at TEXT NOT NULL,
  PRIMARY KEY(scope,ref));
CREATE TABLE IF NOT EXISTS follow_up_cards(suggestion_id TEXT PRIMARY KEY,project_id INTEGER NOT NULL,board_id INTEGER,grouped INTEGER NOT NULL DEFAULT 0,
  n INTEGER NOT NULL,of_max INTEGER NOT NULL,channel TEXT NOT NULL,after_event INTEGER NOT NULL,after_at TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'open',
  auto INTEGER NOT NULL DEFAULT 0,why TEXT,created_at TEXT NOT NULL,closed_at TEXT,UNIQUE(project_id,after_event));
CREATE INDEX IF NOT EXISTS follow_up_cards_project ON follow_up_cards(project_id,state);
CREATE TABLE IF NOT EXISTS follow_up_ends(project_id INTEGER NOT NULL,after_event INTEGER NOT NULL,n INTEGER NOT NULL,moved INTEGER NOT NULL DEFAULT 0,
  judged INTEGER NOT NULL DEFAULT 0,at TEXT NOT NULL,PRIMARY KEY(project_id,after_event));
CREATE TABLE IF NOT EXISTS follow_up_sends(job_id TEXT PRIMARY KEY,batch TEXT NOT NULL,grp TEXT NOT NULL,sender TEXT NOT NULL,queued_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS follow_up_sends_batch ON follow_up_sends(grp,batch);
CREATE TABLE IF NOT EXISTS follow_up_pace(sender TEXT PRIMARY KEY,next_at TEXT NOT NULL);
'''
SCOPES = ('board', 'project')
# The channels a follow-up can go out on, in the order "switch channel" moves through them
CHANNELS = ('email', 'linkedin', 'whatsapp', 'slack', 'telegram', 'intercom')
CHANNEL_KINDS = {'gmail.message': 'email', 'salesflare.email': 'email', 'ms_graph.message': 'email', 'outlook.message': 'email',
                 'linkedin.message': 'linkedin', 'whatsapp.message': 'whatsapp', 'slack.message': 'slack', 'telegram.message': 'telegram',
                 'intercom.conversation': 'intercom'}
MESSAGE_KINDS = tuple(CHANNEL_KINDS) + ('x.dm',)
DEFAULT_DAYS = 3
DEFAULT_MAX_DAYS = 7
DEFAULT_MIN = 1
DEFAULT_MAX = 3
DAYS = (1, 60)
MIN = (0, 5)
MAX = (1, 5)
STALE_DAYS = 14         # a waiting point this long past its follow-up date is left alone
BATCH = 3               # new follow-up drafts per pass
DRAFTING = 3            # follow-ups being drafted at once, at most
PER_DAY = 30            # new follow-up drafts a day, at most
REPEAT = 0.85           # a draft this close to an earlier follow-up (difflib ratio) is a repeat
SEND_GAP = (30, 45)      # seconds between two follow-ups from one mailbox, random in between
SEND_TICK = 3            # the outbox looks every few seconds (assistant.action_worker): drawn so the send still lands in SEND_GAP
PROGRESS_KEEP = 300      # "Sent 8" stays this long after a batch's last send
GOING = ('queued', 'sending')  # outbox states of a follow-up still on its way
OPEN_STATES = ('open',)
STALLED = 'Stalled or declined'  # graph.STALLED


def ensure(db):
    for statement in SCHEMA.split(';'):
        if statement.strip():
            db.execute(statement)


def parse(value):
    when = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    return when if when.tzinfo else when.replace(tzinfo=dt.timezone.utc)


# ------------------------------------------------------------------ settings

def defaults():
    return {'on': False, 'days': DEFAULT_DAYS, 'max_days': DEFAULT_MAX_DAYS, 'min': DEFAULT_MIN, 'max': DEFAULT_MAX, 'stages': {},
            'channels': None, 'switch': False, 'auto': False, 'stall': None}


def _int(value, bounds, what):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(what) from None
    if not bounds[0] <= number <= bounds[1]:
        raise ValueError(what)
    return number


def clean(raw, stage_names=()):
    """A setting as stored, from what the dashboard sent. stage_names: the board's stages (a board's setting only)."""
    if not isinstance(raw, dict):
        raise ValueError('Follow-up settings are missing')
    out = defaults()
    out['on'] = raw.get('on') is True
    days_error = 'Wait 1 to 60 days'  # DAYS
    out['days'] = _int(raw.get('days', DEFAULT_DAYS), DAYS, days_error)
    out['max_days'] = _int(raw.get('max_days', max(out['days'], DEFAULT_MAX_DAYS)), DAYS, days_error)
    if out['max_days'] < out['days']:
        raise ValueError('The longest wait can’t be shorter than the shortest')
    out['min'] = _int(raw.get('min', DEFAULT_MIN), MIN, 'At least 0 to 5 follow-ups')
    out['max'] = _int(raw.get('max', DEFAULT_MAX), MAX, 'At most 1 to 5 follow-ups')
    if out['max'] < out['min']:
        raise ValueError('At most can’t be less than at least')
    stages = raw.get('stages') or {}
    if not isinstance(stages, dict):
        raise ValueError('Stages: on or off per stage')
    known = {n.casefold(): n for n in stage_names}
    for name, value in stages.items():
        if str(name).casefold() not in known or str(name) == STALLED:
            continue  # a stage the board doesn't have (renamed since): dropped
        value = value if isinstance(value, dict) else {'on': bool(value)}
        days = value.get('days')
        out['stages'][known[str(name).casefold()]] = {'on': value.get('on') is not False,
                                                       **({'days': _int(days, DAYS, days_error)} if days not in (None, '') else {})}
    channels = raw.get('channels')
    if channels is not None:
        if not isinstance(channels, list) or any(c not in CHANNELS for c in channels):
            raise ValueError('Channels: pick from the connected ones')
        out['channels'] = [c for c in CHANNELS if c in channels]
        if not out['channels'] and out['on']:
            raise ValueError('Pick at least one channel')
    out['switch'] = raw.get('switch') is True
    out['auto'] = raw.get('auto') is True
    out['stall'] = raw['stall'] if isinstance(raw.get('stall'), bool) else None
    return out


def stalls(settings, board):
    """The project moves to Stalled or declined after the last follow-up: the setting, by default on when the board has
    that stage."""
    if board is None or not board['side']:
        return False
    return settings.get('stall') is not False


def rule(db, scope, ref):
    row = db.execute('SELECT settings FROM follow_up_rules WHERE scope=? AND ref=?', (scope, int(ref))).fetchone()
    if not row:
        return None
    try:
        return {**defaults(), **json.loads(row[0])}
    except ValueError:
        return None


def save(db, scope, ref, raw, now):
    """The owner's setting for a board or a project. A project's 'inherit' takes its own away: its board's applies."""
    if scope not in SCOPES:
        raise ValueError('Follow-ups are set for a board or a project')
    ref = int(ref or 0)
    table = 'boards' if scope == 'board' else 'projects'
    row = db.execute(f'SELECT * FROM {table} WHERE id=?', (ref,)).fetchone()
    if not row:
        raise ValueError('That board is gone' if scope == 'board' else 'That project is gone')
    if scope == 'project' and isinstance(raw, dict) and raw.get('inherit') is True:
        db.execute("DELETE FROM follow_up_rules WHERE scope='project' AND ref=?", (ref,))
        return None
    names = [s['name'] for s in json.loads(row['stages'])] if scope == 'board' else ()
    settings = clean(raw, names)
    if scope == 'project':
        settings['stages'] = {}
    db.execute('INSERT INTO follow_up_rules(scope,ref,settings,updated_at) VALUES(?,?,?,?) ON CONFLICT(scope,ref) DO UPDATE SET '
               'settings=excluded.settings,updated_at=excluded.updated_at', (scope, ref, json.dumps(settings, sort_keys=True), now))
    return settings


def any_on(db):
    try:
        return any(json.loads(r[0]).get('on') for r in db.execute('SELECT settings FROM follow_up_rules'))
    except Exception:  # noqa: BLE001 - no table yet, or a damaged row: nothing on
        return False


def board_stages(board):
    """[(name, open)] for a board row: its stages, the last one and Stalled not open (no follow-ups by default)."""
    names = [s['name'] for s in json.loads(board['stages'])]
    out = [(n, i < len(names) - 1) for i, n in enumerate(names)]
    if board['side']:
        out.append((STALLED, False))
    return out


def stage_rule(settings, board, stage):
    """(on, days) for a project in this stage under a board's setting: days its shortest wait."""
    stages = dict(board_stages(board)) if board is not None else {}
    if stage == STALLED:
        return False, settings['days']
    own = (settings.get('stages') or {}).get(stage)
    if own is not None:
        return own.get('on') is not False, int(own.get('days') or settings['days'])
    return stages.get(stage, True), settings['days']


def effective(db, project, boards=None):
    """(settings, source) for a project row: its own setting ('project'), else its board's ('board'), else (None, None)."""
    own = rule(db, 'project', project['id'])
    if own is not None:
        return own, 'project'
    if project['board_id']:
        board = rule(db, 'board', project['board_id'])
        if board is not None:
            return board, 'board'
    return None, None


# ------------------------------------------------------------------ the schedule

def schedule(messages, settings, now, days=None):
    """Where a project's follow-ups stand, from its messages (oldest first, each {'id', 'at', 'mine', 'channel'}).

    Returns {'state', 'next_at', 'latest_at', 'end_at', 'n', 'judge', 'late', 'after', 'after_at', 'channel', 'tail'}:
    state 'due' (past its shortest wait), 'waiting' (not yet), 'replied' (they wrote last, or nothing yet: nothing waits
    on them), 'last' (the maximum went out; waiting for a reply to it until end_at), 'ended' (no reply to the last one),
    'stale' (more than STALE_DAYS past its date: left alone). n is the follow-up this would be (1 for the first), judge
    whether it's past the minimum (worth another one is judged), late whether it reached its longest wait, after the
    owner's last message (the waiting point) and tail the channels of the owner's messages since their reply."""
    days = int(days or settings['days'])
    longest = max(days, int(settings.get('max_days') or days))
    now = parse(now)
    last_theirs = max((i for i, m in enumerate(messages) if not m['mine']), default=-1)
    tail = messages[last_theirs + 1:]
    none = {'next_at': None, 'latest_at': None, 'end_at': None, 'judge': False, 'late': False}
    if not tail:
        return {**none, 'state': 'replied', 'n': 0, 'after': None, 'after_at': None, 'channel': None, 'tail': []}
    last = tail[-1]
    n = len(tail)  # the first is the message itself, the rest follow-ups
    base = {**none, 'n': n, 'after': last['id'], 'after_at': last['at'], 'channel': last.get('channel'), 'tail': [m.get('channel') for m in tail]}
    wait_from = parse(last['at'])
    if n - 1 >= int(settings['max']):
        end_at = wait_from + dt.timedelta(days=days)
        if now < end_at:
            return {**base, 'state': 'last', 'end_at': end_at.isoformat()}
        if (now - end_at).days > STALE_DAYS:
            return {**base, 'state': 'stale'}
        return {**base, 'state': 'ended', 'end_at': end_at.isoformat()}
    next_at = wait_from + dt.timedelta(days=days)
    latest_at = wait_from + dt.timedelta(days=longest)
    timing = {'next_at': next_at.isoformat(), 'latest_at': latest_at.isoformat(), 'judge': n > int(settings.get('min') or 0)}
    if now < next_at:
        return {**base, **timing, 'state': 'waiting'}
    if (now - latest_at).days > STALE_DAYS:
        return {**base, 'state': 'stale'}
    return {**base, **timing, 'state': 'due', 'late': now >= latest_at}


def pick_channel(last, tail, settings, sendable, reachable):
    """The channel a follow-up goes on: the last message's, when allowed and connected; with switch on and a follow-up
    already unanswered, the next allowed channel after it where the conversation already is (reachable). None: none
    allowed can send."""
    allowed = settings.get('channels')
    usable = [c for c in CHANNELS if c in sendable and (allowed is None or c in allowed)]
    if not usable:
        return None
    if settings.get('switch') and len(tail) >= 2:
        here = [c for c in usable if c in reachable or c == last]
        if len(here) > 1:
            i = here.index(last) if last in here else -1
            return here[(i + 1) % len(here)]
    if last in usable:
        return last
    return next((c for c in usable if c in reachable), None)


def stop_reason(project, settings, source, board, owned_by_other=False):
    """Why a project gets no follow-ups now, or None: archived, won or lost, Stalled, its stage off, a teammate owns it."""
    if not settings or not settings.get('on'):
        return 'off'
    if project['closed_at']:
        return 'archived'
    if project['outcome']:
        return project['outcome']
    if owned_by_other:
        return 'teammate'
    if project['stage'] == STALLED:
        return 'stalled'
    if source == 'board' and board is not None:
        on, _ = stage_rule(settings, board, project['stage'])
        if not on:
            return 'stage'
    return None


def careful(db):
    """Careful mode: the owner's level is Careful, or a Work Fleet they are in is. Nothing goes without asking then."""
    import security_levels
    try:
        return security_levels.label(db) == 'careful' or bool(security_levels.careful_fleets(db))
    except Exception:  # noqa: BLE001 - unknown counts as careful
        return True


def may_send_alone(settings, is_careful, draft, channel, earlier_attempt, repeated):
    """Send without asking applies to this draft: chosen for its board or project, not Careful, exactly the channel
    planned, a verified recipient, nothing tried on it before and not a repeat of an earlier follow-up. Anything else
    waits for the owner."""
    return bool(settings and settings.get('auto') and not is_careful and draft and draft.get('kind') == channel
                and not draft.get('to_options') and not earlier_attempt and not repeated)


def repeats(text, earlier):
    """The draft says what an earlier follow-up said: the same words, or nearly (REPEAT)."""
    norm = lambda s: re.sub(r'\W+', ' ', str(s or '').casefold()).strip()
    mine = norm(text)
    return bool(mine) and any(mine == norm(e) or difflib.SequenceMatcher(None, mine, norm(e)).ratio() >= REPEAT for e in earlier if norm(e))


# ------------------------------------------------------------------ reading a project

def mine_default(event):
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'] or '{}')
    return bool(m.get('from_me')) or 'SENT' in (m.get('labels') or [])


def messages(db, project_id, mine=mine_default):
    """A project's messages, oldest first: {'id', 'at', 'mine', 'channel'}."""
    marks = ','.join('?' for _ in MESSAGE_KINDS)
    # Labeled into it (event_projects), or the Graph's own link (graph_events: its threads)
    rows = db.execute(f"SELECT e.id,e.kind,e.occurred_at,e.metadata FROM events e WHERE e.deleted=0 AND e.kind IN ({marks}) AND e.id IN ("
                      "SELECT event_id FROM event_projects WHERE project_id=? UNION SELECT event_id FROM graph_events WHERE node_id=? AND probable=0) "
                      'ORDER BY e.occurred_at,e.id', (*MESSAGE_KINDS, int(project_id), 'project:' + str(project_id))).fetchall()
    return [{'id': r['id'], 'at': r['occurred_at'], 'mine': mine(dict(r)), 'channel': CHANNEL_KINDS.get(r['kind'], 'x')} for r in rows]


def owned_by_other(db, project_id):
    """A teammate owns the project (record_owners), so their Machine follows it up, not this one."""
    try:
        row = db.execute('SELECT owner FROM record_owners WHERE node_id=?', ('project:' + str(project_id),)).fetchone()
    except Exception:  # noqa: BLE001 - no owners table: the owner here
        return False
    return bool(row and row[0] and row[0] != 'me')


def open_card(db, project_id):
    return db.execute("SELECT f.*,s.status FROM follow_up_cards f JOIN suggestions s ON s.id=f.suggestion_id WHERE f.project_id=? AND f.state='open' "
                      'ORDER BY f.created_at DESC LIMIT 1', (project_id,)).fetchone()


def plan(db, now, sendable, mine=mine_default):
    """Every project follow-ups are on for, with where it stands: [{'project', 'board', 'settings', 'source', 'state',
    'next_at', 'n', 'after', 'after_at', 'channel', 'reason'}]. state as schedule's, or 'off' with a reason, or 'open'
    when a follow-up to-do is out for it already."""
    if not any_on(db):
        return []
    boards = {b['id']: b for b in db.execute('SELECT * FROM boards').fetchall()}
    on_boards = {r[0] for r in db.execute("SELECT ref FROM follow_up_rules WHERE scope='board'")}
    own = {r[0] for r in db.execute("SELECT ref FROM follow_up_rules WHERE scope='project'")}
    ids = sorted(own | {r[0] for r in db.execute(f"SELECT id FROM projects WHERE board_id IN ({','.join('?' * len(on_boards))})", tuple(on_boards))} if on_boards else own)
    out = []
    for pid in ids:
        p = db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
        if not p:
            continue
        settings, source = effective(db, p)
        board = boards.get(p['board_id'])
        item = {'project': p, 'board': board, 'settings': settings, 'source': source}
        reason = stop_reason(p, settings, source, board, owned_by_other(db, pid))
        if reason:
            out.append({**item, 'state': 'off', 'reason': reason, 'next_at': None})
            continue
        days = stage_rule(settings, board, p['stage'])[1] if source == 'board' and board is not None else settings['days']
        msgs = messages(db, pid, mine)
        found = schedule(msgs, settings, now, days)
        if found['state'] in ('due', 'waiting') and found['after'] is not None:
            done = db.execute('SELECT state FROM follow_up_cards WHERE project_id=? AND after_event=?', (pid, found['after'])).fetchone()
            if done:  # this waiting point was followed up already (or skipped): the next one is the follow-up itself
                found = {**found, 'state': 'open' if done['state'] == 'open' else 'handled', 'next_at': None}
        if found['state'] in ('last', 'ended', 'due', 'waiting', 'open', 'handled') and found['after'] is not None:
            ended = db.execute('SELECT n,moved,judged,at FROM follow_up_ends WHERE project_id=? AND after_event=?', (pid, found['after'])).fetchone()
            if ended:
                found = {**found, 'state': 'stopped', 'next_at': None, 'end': dict(ended)}
        if found['state'] == 'ended':
            # Only a round that went out from here ends by itself: a follow-up sent since their last reply
            theirs = max((m['at'] for m in msgs if not m['mine']), default='')
            ours = db.execute("SELECT 1 FROM follow_up_cards WHERE project_id=? AND state='sent' AND after_at>=?", (pid, theirs)).fetchone()
            found = {**found, 'state': 'end' if ours else 'done'}
        elif found['state'] == 'last':
            found = {**found, 'state': 'done'}
        reachable = {m['channel'] for m in msgs}
        channel = pick_channel(found['channel'], found['tail'], settings, sendable, reachable) if found['state'] == 'due' else found['channel']
        if found['state'] == 'due' and not channel:
            found = {**found, 'state': 'off', 'next_at': None}
            item['reason'] = 'channel'
        out.append({**item, **found, 'channel': channel, 'messages': len(msgs)})
    return out


def end(db, item, now, judged=False):
    """A round ends without a reply: the project gets the quiet note (follow_up_ends, "No reply after N follow-ups")
    and, when the setting says so and the board has the stage, moves to Stalled or declined (unless the owner moved it
    by hand since the waiting point). Once per waiting point. Returns the note's {n, moved}."""
    p, board = item['project'], item['board']
    n = max(0, int(item['n']) - 1)  # the follow-ups that went out: the first message of the round isn't one
    moved = False
    if stalls(item['settings'] or {}, board) and p['stage'] != STALLED and not (
            p['stage_by'] == 'owner' and p['stage_at'] and parse(p['stage_at']) > parse(item['after_at'])):
        reason = f'No reply after {n} follow-ups' if n != 1 else 'No reply after 1 follow-up'
        db.execute('INSERT INTO project_moves(project_id,board_id,stage,reason,event_id,source,at,created_at) VALUES(?,?,?,?,?,?,?,?)',
                   (p['id'], p['board_id'], STALLED, reason, item['after'], 'follow_up', now, now))
        db.execute("UPDATE projects SET stage=?,stage_reason=?,stage_event_id=?,stage_by='review',stage_at=? WHERE id=?",
                   (STALLED, reason, item['after'], now, p['id']))
        moved = True
    db.execute('INSERT OR IGNORE INTO follow_up_ends(project_id,after_event,n,moved,judged,at) VALUES(?,?,?,?,?,?)',
               (p['id'], item['after'], n, int(moved), int(judged), now))
    return {'n': n, 'moved': moved}


def due(db, now, sendable, mine=mine_default):
    return [x for x in plan(db, now, sendable, mine) if x['state'] == 'due']


# ------------------------------------------------------------------ what the dashboard shows

def setting_view(settings, source=None):
    return {**(settings or defaults()), **({'source': source} if source else {})}


def panel(db, scope, ref, sendable, now):
    """The settings panel: the setting, the board's stages (on by default or not), the channels that can send, Careful."""
    ref = int(ref or 0)
    if scope == 'board':
        board = db.execute('SELECT * FROM boards WHERE id=?', (ref,)).fetchone()
        if not board:
            raise ValueError('That board is gone')
        own = rule(db, 'board', ref)
        view = {'scope': 'board', 'id': ref, 'name': board['name'], 'settings': setting_view(own), 'stalled': bool(board['side']),
                'stages': [{'name': n, 'open': o} for n, o in board_stages(board) if n != STALLED]}
    elif scope == 'project':
        p = db.execute('SELECT * FROM projects WHERE id=?', (ref,)).fetchone()
        if not p:
            raise ValueError('That project is gone')
        own = rule(db, 'project', ref)
        board = db.execute('SELECT * FROM boards WHERE id=?', (p['board_id'],)).fetchone() if p['board_id'] else None
        board_rule = rule(db, 'board', board['id']) if board else None
        view = {'scope': 'project', 'id': ref, 'name': p['name'], 'settings': setting_view(own or board_rule), 'own': own is not None,
                'stalled': bool(board and board['side']),
                'board': {'id': board['id'], 'name': board['name'], 'on': bool(board_rule and board_rule.get('on'))} if board else None}
    else:
        raise ValueError('Follow-ups are set for a board or a project')
    view.update(channels=[c for c in CHANNELS if c in sendable], careful=careful(db))
    return view


def views(db, now, sendable, mine=mine_default):
    """{'boards': {board_id: {'on', 'next_at'}}, 'projects': {project_id: {'on', 'state', 'next_at', 'n', 'max', 'own', 'end'}}}:
    next_at the next follow-up's date (due or waiting), end the quiet note when a round ended without a reply."""
    out = {'boards': {}, 'projects': {}}
    try:
        for r in db.execute("SELECT ref,settings FROM follow_up_rules WHERE scope='board'"):
            out['boards'][r[0]] = {'on': bool(json.loads(r[1]).get('on')), 'next_at': None}
        items = plan(db, now, sendable, mine)
    except Exception:  # noqa: BLE001 - the board shows without it
        return out
    for x in items:
        p = x['project']
        state = x['state']
        due_at = x.get('next_at') if state in ('due', 'waiting') else None
        out['projects'][p['id']] = {'on': state != 'off', 'state': state, 'reason': x.get('reason'), 'next_at': due_at, 'n': x.get('n'),
                                    'max': (x['settings'] or {}).get('max'), 'own': x['source'] == 'project', 'end': x.get('end')}
        b = out['boards'].get(p['board_id'])
        if b and b['on'] and x['source'] == 'board' and due_at:
            b['next_at'] = min(filter(None, [b['next_at'], due_at]))
    return out


def activity(db, project_id, limit=6):
    """A project's follow-ups, newest first: what went out (by itself or after the owner's Send), skipped or stopped."""
    rows = db.execute('SELECT n,of_max,channel,state,auto,why,created_at,closed_at FROM follow_up_cards WHERE project_id=? '
                      'ORDER BY created_at DESC LIMIT ?', (int(project_id), limit)).fetchall()
    return [dict(r) for r in rows]


# ------------------------------------------------------------------ open follow-up to-dos

WHY = {
    'replied': 'They replied, so this follow-up isn’t needed.',
    'handled': 'Someone already followed up, so this one isn’t needed.',
    'archived': 'The project was archived, so follow-ups stopped.',
    'won': 'The project was won, so follow-ups stopped.',
    'lost': 'The project was lost, so follow-ups stopped.',
    'stalled': 'The project moved to Stalled or declined, so follow-ups stopped.',
    'stage': 'Follow-ups are off for this stage now.',
    'off': 'Follow-ups were turned off.',
    'teammate': 'A teammate owns this project now; their Machine follows it up.',
    'judged': 'Another follow-up isn’t worth it now, so follow-ups stopped.',
}


def close(db, suggestion_id, why, now, state='stopped'):
    """Close an open follow-up to-do by itself (WHY says why in the to-do's history)."""
    db.execute("UPDATE follow_up_cards SET state=?,why=?,closed_at=? WHERE suggestion_id=? AND state='open'", (state, why, now, suggestion_id))
    if db.execute("UPDATE suggestions SET status='rejected',early=0 WHERE id=? AND status NOT IN ('completed','rejected')", (suggestion_id,)).rowcount:
        db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   ('follow-up-' + why + ':' + suggestion_id, suggestion_id, 'reject', WHY.get(why, why), 'assistant', now))
        db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','starting','running','blocked')",
                   (now, suggestion_id))
        db.execute("UPDATE deliveries SET status='cancelled',reminder=0,needs_edit=CASE WHEN message_id IS NULL THEN needs_edit ELSE 1 END,updated_at=? "
                   'WHERE suggestion_id=?', (now, suggestion_id))


def settle(db, now, mine=mine_default):
    """Open follow-up to-dos: mark the ones the owner closed (sent, skipped), leave the ones a review took over as normal
    to-dos, and close the rest when a stop condition holds. Returns [(suggestion_id, why)] closed by itself."""
    closed = []
    for f in db.execute("SELECT f.*,s.status,s.created_at card_at FROM follow_up_cards f JOIN suggestions s ON s.id=f.suggestion_id "
                        "WHERE f.state='open'").fetchall():
        sid = f['suggestion_id']
        jobs = [r[0] for r in db.execute('SELECT status FROM action_jobs WHERE suggestion_id=?', (sid,))]
        if 'sent' in jobs:
            db.execute("UPDATE follow_up_cards SET state='sent',closed_at=? WHERE suggestion_id=?", (now, sid))
            continue
        if f['status'] in ('completed', 'rejected'):
            db.execute("UPDATE follow_up_cards SET state='skipped',closed_at=? WHERE suggestion_id=?", (now, sid))
            continue
        if any(s in ('queued', 'sending', 'uncertain') for s in jobs):
            continue  # on its way: the outbox settles it
        if db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND choice='update' AND created_at>=?", (sid, f['card_at'])).fetchone():
            # A review brought new news onto it: a normal to-do now, with its own notification
            db.execute("UPDATE follow_up_cards SET state='detached',why='update',closed_at=? WHERE suggestion_id=?", (now, sid))
            db.execute("UPDATE deliveries SET status='queued' WHERE suggestion_id=? AND status='grouped'", (sid,))
            continue
        p = db.execute('SELECT * FROM projects WHERE id=?', (f['project_id'],)).fetchone()
        if not p:
            close(db, sid, 'archived', now)
            closed.append((sid, 'archived'))
            continue
        settings, source = effective(db, p)
        board = db.execute('SELECT * FROM boards WHERE id=?', (p['board_id'],)).fetchone() if p['board_id'] else None
        why = stop_reason(p, settings, source, board, owned_by_other(db, p['id']))
        if not why:
            later = [m for m in messages(db, p['id'], mine) if parse(m['at']) > parse(f['after_at']) and m['id'] != f['after_event']]
            why = 'replied' if any(not m['mine'] for m in later) else 'handled' if later else None
        if not why:
            outcome = db.execute('SELECT outcome FROM suggestions WHERE id=?', (sid,)).fetchone()
            try:
                outcome = json.loads(outcome[0] or '{}') if outcome else {}
            except ValueError:
                outcome = {}
            if outcome.get('state') == 'already_done':
                # The preparation judged another follow-up not worth it (past the minimum only), or found it handled
                if outcome.get('follow_up') == 'stop' and f['n'] > int((settings or {}).get('min') or 0):
                    why = 'judged'
                    end(db, {'project': p, 'board': board, 'settings': settings, 'n': f['n'], 'after': f['after_event'], 'after_at': f['after_at']},
                        now, judged=True)
                else:
                    why = 'handled'
        if why:
            close(db, sid, why, now)
            closed.append((sid, why))
    return closed


def earlier_texts(db, project_id, limit=6):
    """What earlier follow-ups on this project said (sent ones, newest first), so a new one never repeats them."""
    out = []
    for r in db.execute("SELECT j.payload FROM follow_up_cards f JOIN action_jobs j ON j.suggestion_id=f.suggestion_id "
                        "WHERE f.project_id=? AND j.status='sent' ORDER BY j.updated_at DESC LIMIT ?", (int(project_id), limit)):
        try:
            out.append(str(json.loads(r[0]).get('body') or ''))
        except ValueError:
            continue
    return [t for t in out if t]


def cards_view(db, ids):
    """{suggestion_id: {...}} for the to-do list: which follow-up a to-do is, and the board it groups under."""
    if not ids:
        return {}
    marks = ','.join('?' for _ in ids)
    try:
        rows = db.execute(f"SELECT f.*,p.name project,b.name board FROM follow_up_cards f LEFT JOIN projects p ON p.id=f.project_id "
                          f"LEFT JOIN boards b ON b.id=f.board_id WHERE f.suggestion_id IN ({marks}) AND f.state IN ('open','sent','skipped','stopped')",
                          tuple(ids)).fetchall()
    except Exception:  # noqa: BLE001 - no table yet
        return {}
    return {r['suggestion_id']: {'project': r['project'], 'project_id': 'project:' + str(r['project_id']), 'board': r['board'],
                                 'group': ('board:' + str(r['board_id'])) if r['grouped'] and r['board_id'] else None,
                                 'n': r['n'], 'max': r['of_max'], 'channel': r['channel'], 'auto': bool(r['auto']), 'state': r['state']}
            for r in rows}


def drafted_today(db, now):
    since = (parse(now) - dt.timedelta(days=1)).isoformat()
    return db.execute('SELECT count(*) FROM follow_up_cards WHERE created_at>=?', (since,)).fetchone()[0]


def late_ids(db, now):
    """Open follow-ups that reached their longest wait: they go ahead like other background work."""
    out = set()
    for f in db.execute("SELECT f.suggestion_id,f.project_id,f.after_at FROM follow_up_cards f WHERE f.state='open'").fetchall():
        p = db.execute('SELECT * FROM projects WHERE id=?', (f['project_id'],)).fetchone()
        settings = (effective(db, p)[0] if p else None) or defaults()
        if parse(now) >= parse(f['after_at']) + dt.timedelta(days=max(int(settings['days']), int(settings.get('max_days') or 0))):
            out.add(f['suggestion_id'])
    return out


def sendable(accounts):
    """The channels the owner's connected accounts can send on (a Fleet-shared one reads only)."""
    import next_actions
    out = set()
    for a in accounts:
        if a.get('shared') and not (isinstance(a.get('shared'), dict) and a['shared'].get('origin')):
            continue
        service = a.get('service', 'gmail')
        if service in ('gmail', 'outlook') and next_actions.mail_account(a):
            out.add('email')
        elif service == 'intercom' and next_actions.intercom_replies_on(a):
            out.add('intercom')
        elif service in ('linkedin', 'whatsapp', 'slack', 'telegram'):
            out.add(service)
    return out


def covered(db):
    """Event ids on projects that automated follow-ups look after, so "Possibly slipped" doesn't offer a second nudge."""
    if not any_on(db):
        return set()
    out = set()
    for p in db.execute('SELECT * FROM projects WHERE closed_at IS NULL').fetchall():
        settings, _ = effective(db, p)
        if settings and settings.get('on'):
            out |= {m['id'] for m in messages(db, p['id'], lambda e: True)}
    return out


# ------------------------------------------------------------------ sending several in a row

def sender(action):
    """Which account a follow-up goes out from, for the spacing: the email's From address, or the channel's account."""
    if action.get('kind') == 'email':
        return 'email:' + str(action.get('from') or '').strip().lower()
    return str(action.get('kind') or '') + ':' + str(action.get('account_id') or '')


def gap(draw=random.uniform):
    """Seconds until the next follow-up from the same account may go: random in SEND_GAP, less the outbox's tick."""
    return draw(SEND_GAP[0], SEND_GAP[1] - SEND_TICK)


def queued(db, suggestion_id, job_id, action, now):
    """An outbox send of a follow-up was queued (confirm_action): it joins the batch of its board (or of the projects'
    own follow-ups) that is still on its way, or starts a new one. Not a follow-up: nothing."""
    f = db.execute('SELECT board_id,grouped FROM follow_up_cards WHERE suggestion_id=?', (suggestion_id,)).fetchone()
    if not f:
        return None
    grp = 'board:' + str(f['board_id']) if f['grouped'] and f['board_id'] else 'own'
    going = db.execute(f"SELECT s.batch FROM follow_up_sends s JOIN action_jobs j ON j.id=s.job_id WHERE s.grp=? AND s.job_id<>? "
                       f"AND j.status IN ({','.join('?' for _ in GOING)}) ORDER BY s.queued_at DESC LIMIT 1", (grp, job_id, *GOING)).fetchone()
    batch = going[0] if going else grp + '@' + now
    db.execute('INSERT OR REPLACE INTO follow_up_sends(job_id,batch,grp,sender,queued_at) VALUES(?,?,?,?,?)', (job_id, batch, grp, sender(action), now))
    return batch


def held_until(db, job_id, now):
    """When a queued follow-up may go: None now, else the time the one before from the same account asked it to wait."""
    row = db.execute('SELECT p.next_at FROM follow_up_sends s JOIN follow_up_pace p ON p.sender=s.sender WHERE s.job_id=?', (job_id,)).fetchone()
    return row[0] if row and parse(row[0]) > parse(now) else None


def going_out(db, job_id, now, draw=random.uniform):
    """A follow-up is admitted to send (in the outbox's transaction): the next one from its account waits a gap."""
    row = db.execute('SELECT sender FROM follow_up_sends WHERE job_id=?', (job_id,)).fetchone()
    if not row:
        return None
    next_at = (parse(now) + dt.timedelta(seconds=gap(draw))).isoformat()
    db.execute('INSERT INTO follow_up_pace(sender,next_at) VALUES(?,?) ON CONFLICT(sender) DO UPDATE SET next_at=excluded.next_at', (row[0], next_at))
    return next_at


def progress(db, now):
    """The latest batch per board (and of the projects' own follow-ups) while it goes, and PROGRESS_KEEP after: [{group,
    board, total, done, sent, going}]. Batches of one aren't shown: that to-do says how its send went."""
    out = []
    try:
        groups = [r[0] for r in db.execute('SELECT DISTINCT grp FROM follow_up_sends')]
    except Exception:  # noqa: BLE001 - no table yet
        return out
    since = (parse(now) - dt.timedelta(seconds=PROGRESS_KEEP)).isoformat()
    for grp in groups:
        batch = db.execute('SELECT batch FROM follow_up_sends WHERE grp=? ORDER BY queued_at DESC,rowid DESC LIMIT 1', (grp,)).fetchone()[0]
        jobs = db.execute('SELECT j.status,j.updated_at FROM follow_up_sends s JOIN action_jobs j ON j.id=s.job_id WHERE s.batch=?', (batch,)).fetchall()
        if len(jobs) < 2:
            continue
        going = sum(j['status'] in GOING for j in jobs)
        if not going and max(j['updated_at'] for j in jobs) < since:
            continue
        board = db.execute('SELECT name FROM boards WHERE id=?', (int(grp.split(':')[1]),)).fetchone() if grp.startswith('board:') else None
        out.append({'group': grp if grp.startswith('board:') else None, 'board': board[0] if board else None, 'total': len(jobs),
                    'done': len(jobs) - going, 'sent': sum(j['status'] == 'sent' for j in jobs), 'going': going > 0})
    return out

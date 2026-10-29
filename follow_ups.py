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

Nothing new since the draft (basis, recheck): each draft remembers what it was written against, the thread's latest
message per channel (follow_up_basis). Right before a follow-up goes out (one Send, Send all checked, Send without
asking: all through the outbox, assistant.action_step) the thread is read again from its source: the collected messages,
Gmail's thread or Outlook's conversation read fresh, and the WhatsApp chat (LinkedIn has no cheap read: its collected
messages count). When anything was added after the basis, by anyone (the owner from Gmail or another app, the contact,
a teammate's Machine), the draft is held, not sent: "Not sent: new message in the thread" (follow_up_holds). A reply
ends the round as before; the owner's own send counts as that round, and the next follow-up waits from it (settle, plan).
When the thread can't be read (offline, signed out), it isn't sent either: "Couldn’t check the thread, try again".

Change in the review (App.follow_up_change): the owner says what should change, for all checked drafts or one. Each
goes through the same path as a message in its to-do's chat (a Change note, the preparation's next turn in its own
session), at most DRAFTING at once, but as a full preparation turn, never the chat's short one: the owner's current
style, what was learned, the thread and earlier follow-ups again, and the skills on right now with their SKILL.md
(change_note), so "I added a skill, use it now" works minutes after the skill was added. Only the text changes: the rewritten draft keeps its channel, recipients, sending
account and thread (route, checked when it is saved: change_problem), and it is never sent from there (no send_now). It
comes back ready, still checked, for the owner to read and send (follow_up_changes).

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
CREATE TABLE IF NOT EXISTS follow_up_threads(event_id INTEGER PRIMARY KEY,sends TEXT,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS follow_up_basis(suggestion_id TEXT PRIMARY KEY,basis TEXT NOT NULL,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS follow_up_holds(job_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,why TEXT NOT NULL,news TEXT,at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS follow_up_changes(decision_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,revision TEXT NOT NULL,route TEXT NOT NULL,at TEXT NOT NULL);
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

def schedule(messages, settings, now, days=None, prior=0, since=None):
    """Where a project's follow-ups stand, from its messages (oldest first, each {'id', 'at', 'mine', 'channel'}).

    Returns {'state', 'next_at', 'latest_at', 'end_at', 'n', 'judge', 'late', 'after', 'after_at', 'channel', 'tail'}:
    state 'due' (past its shortest wait), 'waiting' (not yet), 'replied' (they wrote last, or nothing yet: nothing waits
    on them), 'last' (the maximum went out; waiting for a reply to it until end_at), 'ended' (no reply to the last one),
    'stale' (more than STALE_DAYS past its date: left alone). n is the follow-up this would be (1 for the first), judge
    whether it's past the minimum (worth another one is judged), late whether it reached its longest wait, after the
    owner's last message (the waiting point) and tail the channels of the owner's messages since their reply.

    prior: the owner's earlier unanswered sends in the thread that weren't collected (sent before The Machine read the
    mailbox, earlier_sends), since the first of them when known: they count as sent in this round, and the round
    starts there (round_at, the first unanswered message)."""
    days = int(days or settings['days'])
    longest = max(days, int(settings.get('max_days') or days))
    now = parse(now)
    last_theirs = max((i for i, m in enumerate(messages) if not m['mine']), default=-1)
    tail = messages[last_theirs + 1:]
    none = {'next_at': None, 'latest_at': None, 'end_at': None, 'judge': False, 'late': False}
    if not tail:
        return {**none, 'state': 'replied', 'n': 0, 'after': None, 'after_at': None, 'round_at': None, 'prior': 0, 'channel': None, 'tail': []}
    last = tail[-1]
    n = len(tail) + max(0, int(prior or 0))  # the first is the message itself, the rest follow-ups
    round_at = min([parse(tail[0]['at'])] + ([parse(since)] if since and prior else []))
    base = {**none, 'n': n, 'after': last['id'], 'after_at': last['at'], 'round_at': round_at.isoformat(), 'prior': max(0, int(prior or 0)),
            'channel': last.get('channel'), 'tail': [m.get('channel') for m in tail]}
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


# ------------------------------------------------------------------ earlier sends in the thread
# A thread the owner started from another app, before The Machine read this mailbox, only shows its earlier messages
# as quoted history in the latest one. They still count: three unanswered emails are three, not one. The real thread
# (Gmail's thread, Outlook's conversation: metadata only, read once per waiting point by the App, follow_up_threads) is
# preferred; otherwise the quoted headers in the owner's latest email are read, newest first, until the first message
# from someone else.

WROTE = re.compile(r'^(?:On|Le|Op|Am|El|Il|Em|Den|Dnia)\b(?P<rest>.{0,400}?)\s(?:wrote|a\s+écrit|schreef|schrieb|escribió|ha\s+scritto|'
                   r'skrev|escreveu|napisał)\s*:\s*$', re.I)
FROM_LINE = re.compile(r'^\*?(?:From|Von|De|Van|Da|Fra|Från|Od)\s*:\*?\s*(?P<who>\S.*)$', re.I)
SENT_LINE = re.compile(r'^\*?(?:Sent|Date|Gesendet|Datum|Envoyé|Verzonden|Enviado|Enviada|Fecha|Inviato|Data|Sendt|Skickat|Wysłano)\s*:\*?\s*(?P<at>\S.*)$', re.I)
FORWARDED = re.compile(r'^-{2,}\s*(?:Forwarded message|Doorgestuurd bericht|Message transféré|Weitergeleitete Nachricht|Mensaje reenviado|'
                       r'Messaggio inoltrato|Mensagem encaminhada|Videresendt melding)', re.I)
ADDRESS = re.compile(r'[\w.+\'-]+@[\w-]+(?:\.[\w-]+)+')
MONTHS = {1: ('jan', 'ene', 'gen'), 2: ('feb', 'fév', 'fev'), 3: ('mar', 'mär', 'maa', 'mrt'), 4: ('apr', 'avr', 'abr'), 5: ('may', 'mai', 'mei', 'mag'),
          6: ('jun', 'juin', 'giu'), 7: ('jul', 'juil', 'lug'), 8: ('aug', 'aoû', 'aou', 'ago'), 9: ('sep', 'set'), 10: ('oct', 'okt', 'out', 'ott'),
          11: ('nov',), 12: ('dec', 'déc', 'dez', 'dic')}
DAY_MONTH_YEAR = re.compile(r'\b(\d{1,2})\.?\s+(?:de\s+)?([^\W\d_]{3,})\.?,?\s+(?:de\s+)?(\d{4})\b')
MONTH_DAY_YEAR = re.compile(r'\b([^\W\d_]{3,})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b')
ISO_DAY = re.compile(r'\b(\d{4})-(\d{2})-(\d{2})\b')
CLOCK = re.compile(r'\b(\d{1,2})[:.h](\d{2})(?::(\d{2}))?\s*([ap]\.?\s?m\.?)?', re.I)
ZONE = re.compile(r'(?:\s|GMT|UTC)([+-])(\d{2}):?(\d{2})\b')


def _month(word):
    word = word.casefold()
    return next((n for n, stems in MONTHS.items() if any(word.startswith(s) for s in stems)), None)


def quoted_date(text):
    """The date in a quoted header ("Mon, 21 Sep 2026 08:24:10 -0500", "Mon, Sep 21, 2026 at 3:24 PM", "lun. 21 sept.
    2026 à 08:24", "Monday, September 21, 2026 3:24 PM"...), ISO, or None when it can't be read. Without a zone: UTC."""
    text = str(text or '')
    day = None
    for found in DAY_MONTH_YEAR.finditer(text):
        if _month(found[2]):
            day, end = (int(found[3]), _month(found[2]), int(found[1])), found.end()
            break
    if day is None:
        for found in MONTH_DAY_YEAR.finditer(text):
            if _month(found[1]):
                day, end = (int(found[3]), _month(found[1]), int(found[2])), found.end()
                break
    if day is None and (found := ISO_DAY.search(text)):
        day, end = (int(found[1]), int(found[2]), int(found[3])), found.end()
    if day is None:
        return None
    hour = minute = second = 0
    clock = CLOCK.search(text, end)
    if clock:
        hour, minute, second = int(clock[1]), int(clock[2]), int(clock[3] or 0)
        half = (clock[4] or '').casefold().replace('.', '').replace(' ', '')
        hour = (hour % 12) + (12 if half == 'pm' else 0) if half else hour
    zone = dt.timezone.utc
    if (z := ZONE.search(text, end)):
        zone = dt.timezone((1 if z[1] == '+' else -1) * dt.timedelta(hours=int(z[2]), minutes=int(z[3])))
    try:
        return dt.datetime(*day, hour % 24, minute % 60, second % 60, tzinfo=zone).astimezone(dt.timezone.utc).isoformat()
    except ValueError:
        return None


def quoted_headers(body):
    """The quoted messages' headers in an email body, newest first: [{'who', 'address', 'at'}]. Reply lines in any of
    the common forms ("On <date>, <name> wrote:", over up to three lines, in several languages; Outlook's "From: ...
    Sent: ..."), at any quote depth. Stops at a forwarded message: what's below it isn't this conversation."""
    lines = [re.sub(r'^(?:\s*>)+\s?', '', line).strip() for line in str(body or '').splitlines()]
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if FORWARDED.match(line):
            break
        found = None
        for width in (1, 2, 3):
            joined = ' '.join(x for x in lines[i:i + width] if x)
            if (match := WROTE.match(joined)):
                found = (match['rest'], width)
                break
        if found:
            rest, width = found
            address = ADDRESS.findall(rest)
            out.append({'who': rest, 'address': address[-1].casefold() if address else None, 'at': quoted_date(rest)})
            i += width
            continue
        match = FROM_LINE.match(line)
        if match:
            sent = next((SENT_LINE.match(x) for x in lines[i + 1:i + 4] if SENT_LINE.match(x)), None)
            if sent:
                address = ADDRESS.findall(match['who'])
                out.append({'who': match['who'], 'address': address[-1].casefold() if address else None, 'at': quoted_date(sent['at'])})
                i += 2
                continue
        i += 1
    return out


def own_header(header, own):
    """A quoted header is the owner's: their address, or, with no address in it, their full name."""
    if header['address']:
        return header['address'] in own['emails']
    who = ' '.join(re.sub(r'[^\w@.\s-]', ' ', header['who']).split()).casefold()
    return any(name and name in who for name in own['names'])


def quoted_sends(body, own):
    """The owner's earlier sends quoted in their email, newest first ([ISO date or None]): consecutive headers that are
    theirs, until the first quoted message from someone else (they replied there: the count starts again)."""
    out = []
    for header in quoted_headers(body):
        if not own_header(header, own):
            break
        out.append(header['at'])
    return out


def thread_sends(thread, message_id, own_emails):
    """The owner's earlier sends in a real thread before message_id, newest first ([ISO date]), until a message from
    someone else. thread: Gmail's threads.get answer (format metadata, the From header; an Outlook conversation is
    answered in the same shape). None when the message isn't in it."""
    items = []
    for m in (thread or {}).get('messages') or ():
        labels = m.get('labelIds') or []
        if 'DRAFT' in labels:
            continue
        sender = next((h.get('value') for h in (m.get('payload') or {}).get('headers') or () if str(h.get('name')).casefold() == 'from'), '')
        address = ADDRESS.findall(str(sender or ''))
        mine = 'SENT' in labels or bool(address and address[-1].casefold() in own_emails)
        try:
            at = dt.datetime.fromtimestamp(int(m.get('internalDate')) / 1000, dt.timezone.utc).isoformat()
        except (TypeError, ValueError):
            at = None
        items.append((at or '', str(m.get('id')), mine))
    items.sort()
    ids = [x[1] for x in items]
    if str(message_id) not in ids:
        return None
    out = []
    for at, _, mine in reversed(items[:ids.index(str(message_id))]):
        if not mine:
            break
        out.append(at or None)
    return out


def owner(own=None):
    """{'emails', 'names'} from what the App knows about the owner (their addresses, their full name)."""
    own = own or {}
    return {'emails': {str(e).strip().casefold() for e in own.get('emails') or () if e},
            'names': {' '.join(str(n).split()).casefold() for n in own.get('names') or () if n and len(str(n).split()) >= 2}}


def latest_email(db, tail):
    """The owner's latest collected email in the round (index in the tail, event row), or (None, None)."""
    for i in range(len(tail) - 1, -1, -1):
        if tail[i]['channel'] == 'email':
            row = db.execute('SELECT id,source_id,account_id,body,metadata FROM events WHERE id=?', (tail[i]['id'],)).fetchone()
            if row:
                return i, row
    return None, None


def earlier_sends(db, msgs, own=None):
    """(prior, since, counted): how many of the owner's unanswered sends in this round weren't collected, the first
    one's date, and whether that could be counted at all. From the real thread when the App read it
    (follow_up_threads), else the quoted history of their latest email (its body as the store opens it: a sealed body
    that can't be opened here is not counted, so no follow-up is drafted on a guess). The collected ones are never
    counted twice: both list the owner's sends before that email, newest first, and the first `index` of those are the
    collected tail before it; prior is only what's beyond. Nothing to count (no email, nothing of theirs): counted."""
    last_theirs = max((i for i, m in enumerate(msgs) if not m['mine']), default=-1)
    tail = msgs[last_theirs + 1:]
    if not tail:
        return 0, None, True
    index, row = latest_email(db, tail)
    if row is None:
        return 0, None, True
    sends, tried = None, False
    try:
        cached = db.execute('SELECT sends FROM follow_up_threads WHERE event_id=?', (row['id'],)).fetchone()
        tried = cached is not None  # read, or tried and it couldn't be: the quoted history then
        sends = json.loads(cached[0]) if cached and cached[0] else None
    except Exception:  # noqa: BLE001 - no table yet, or a damaged row: the quoted history
        sends = None
    if sends is None and not isinstance(row['body'], str):
        return 0, None, tried  # still sealed (no key on this connection): not readable here
    if sends is None:
        who = owner(own)
        try:
            meta = json.loads(row['metadata'] or '{}') if not isinstance(row['metadata'], dict) else row['metadata']
        except ValueError:
            meta = {}
        who['emails'] |= {a.casefold() for a in ADDRESS.findall(str(meta.get('from') or ''))}  # it's theirs: its From is too
        sends = quoted_sends(row['body'], who)
    prior = max(0, len(sends) - index)
    dated = [s for s in sends[index:] if s]
    return prior, (min(dated) if prior and dated else None), True


# ------------------------------------------------------------------ nothing new since the draft

SEEN = 20               # source ids per channel a basis keeps, to tell a fresh read's known messages from new ones
HELD = 'Not sent: new message in the thread.'
UNCHECKED = 'Couldn’t check the thread, try again.'


def _meta(value):
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value or '{}')
    except ValueError:
        return {}


def basis(db, project_id, upto=None):
    """What a draft is written against: the project's latest collected message overall and per channel ({'at', 'id',
    'channels': {channel: {'at', 'id', 'source_id', 'account_id', 'thread_id', 'chat_id', 'seen'}}}). upto: only messages
    until then (a draft from before bases were kept: its waiting point)."""
    marks = ','.join('?' for _ in MESSAGE_KINDS)
    rows = db.execute(f"SELECT e.id,e.kind,e.source_id,e.account_id,e.occurred_at,e.metadata FROM events e WHERE e.deleted=0 AND e.kind IN ({marks}) "
                      "AND e.id IN (SELECT event_id FROM event_projects WHERE project_id=? UNION SELECT event_id FROM graph_events WHERE node_id=? "
                      'AND probable=0) ORDER BY e.occurred_at,e.id', (*MESSAGE_KINDS, int(project_id), 'project:' + str(project_id))).fetchall()
    if upto:
        rows = [r for r in rows if parse(r['occurred_at']) <= parse(upto)]
    out = {'at': None, 'id': None, 'channels': {}}
    for r in rows:
        channel = CHANNEL_KINDS.get(r['kind'], 'x')
        meta = _meta(r['metadata'])
        seen = (out['channels'].get(channel) or {}).get('seen') or []
        out['channels'][channel] = {'at': r['occurred_at'], 'id': r['id'], 'source_id': str(r['source_id'] or ''), 'account_id': r['account_id'],
                                    'thread_id': meta.get('thread_id') or meta.get('threadId') or meta.get('conversation_id'),
                                    'chat_id': meta.get('chat_id') or meta.get('chat'), 'seen': (seen + [str(r['source_id'] or '')])[-SEEN:]}
        out['at'], out['id'] = r['occurred_at'], r['id']
    return out


def remember(db, suggestion_id, found, now):
    """Keep a draft's basis (follow_up_card, when its preparation starts)."""
    db.execute('INSERT OR IGNORE INTO follow_up_basis(suggestion_id,basis,at) VALUES(?,?,?)', (suggestion_id, json.dumps(found), now))


def basis_of(db, suggestion_id):
    """(card, basis) for a follow-up to-do, or (None, None) when it isn't one. A to-do from before bases were kept
    gets its waiting point's."""
    card = db.execute('SELECT * FROM follow_up_cards WHERE suggestion_id=?', (suggestion_id,)).fetchone()
    if not card:
        return None, None
    row = db.execute('SELECT basis FROM follow_up_basis WHERE suggestion_id=?', (suggestion_id,)).fetchone()
    try:
        return card, json.loads(row[0])
    except (TypeError, ValueError):
        return card, basis(db, card['project_id'], card['after_at'])


def collected_since(db, project_id, found, mine=mine_default):
    """The project's collected messages added after the basis, oldest first ({'id', 'at', 'mine', 'channel'})."""
    known = {c.get('id') for c in (found.get('channels') or {}).values()} | {found.get('id')}
    since = parse(found['at']) if found.get('at') else None
    return [m for m in messages(db, project_id, mine) if m['id'] not in known and (since is None or parse(m['at']) > since)]


def thread_since(thread, channel_basis, own_emails):
    """The messages in a freshly read email thread (Gmail's threads.get, format metadata; an Outlook conversation in
    the same shape) added after the basis: [{'id', 'at', 'mine'}]. Drafts don't count."""
    seen = set(channel_basis.get('seen') or ()) | {str(channel_basis.get('source_id') or '')}
    since = parse(channel_basis['at']) if channel_basis.get('at') else None
    out = []
    for m in (thread or {}).get('messages') or ():
        labels = m.get('labelIds') or []
        if 'DRAFT' in labels or str(m.get('id')) in seen:
            continue
        try:
            at = dt.datetime.fromtimestamp(int(m.get('internalDate')) / 1000, dt.timezone.utc)
        except (TypeError, ValueError):
            at = None
        if since is not None and at is not None and at <= since:
            continue
        sender = next((h.get('value') for h in (m.get('payload') or {}).get('headers') or () if str(h.get('name')).casefold() == 'from'), '')
        address = ADDRESS.findall(str(sender or ''))
        out.append({'id': str(m.get('id')), 'at': at.isoformat() if at else None,
                    'mine': 'SENT' in labels or bool(address and address[-1].casefold() in own_emails)})
    return out


def chat_since(rows, channel_basis):
    """The messages in a freshly read chat (wacli messages list: MsgID, Timestamp, FromMe) added after the basis."""
    seen = {str(s) for s in channel_basis.get('seen') or ()} | {str(channel_basis.get('source_id') or '')}
    since = parse(channel_basis['at']) if channel_basis.get('at') else None
    out = []
    for r in rows or ():
        msg_id = str(r.get('MsgID') or '')
        if not msg_id or any(msg_id == s or s.endswith(':' + msg_id) for s in seen if s):
            continue
        try:
            at = parse(r.get('Timestamp'))
        except (TypeError, ValueError):
            continue
        if since is not None and at <= since:
            continue
        out.append({'id': msg_id, 'at': at.isoformat(), 'mine': r.get('FromMe') is True})
    return out


def news_kind(news):
    """'reply' when someone else wrote since the basis, 'own' when only the owner did, None when nothing is new."""
    if not news:
        return None
    return 'reply' if any(not n.get('mine') for n in news) else 'own'


def hold(db, job_id, suggestion_id, why, news, now):
    """A follow-up is held before it goes (nothing sent): why 'changed' (a new message in the thread) or 'unchecked'
    (the thread couldn't be read). The outbox job waits, blocked, with the line the to-do shows; a new Send checks
    again."""
    line = HELD if why == 'changed' else UNCHECKED
    db.execute("UPDATE action_jobs SET status='blocked',error=?,retry_at=NULL,updated_at=? WHERE id=? AND status='queued'", (line, now, job_id))
    db.execute('INSERT OR REPLACE INTO follow_up_holds(job_id,suggestion_id,why,news,at) VALUES(?,?,?,?,?)',
               (job_id, suggestion_id, why, json.dumps(news) if news is not None else None, now))
    return line


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


def plan(db, now, sendable, mine=mine_default, own=None):
    """Every project follow-ups are on for, with where it stands: [{'project', 'board', 'settings', 'source', 'state',
    'next_at', 'n', 'after', 'after_at', 'channel', 'reason'}]. state as schedule's, or 'off' with a reason, or 'open'
    when a follow-up to-do is out for it already. own: the owner's {'emails', 'names'}, to read quoted history
    (earlier_sends)."""
    if not any_on(db):
        return []
    boards = {b['id']: b for b in db.execute('SELECT * FROM boards').fetchall()}
    on_boards = {r[0] for r in db.execute("SELECT ref FROM follow_up_rules WHERE scope='board'")}
    own_rules = {r[0] for r in db.execute("SELECT ref FROM follow_up_rules WHERE scope='project'")}
    ids = sorted(own_rules | {r[0] for r in db.execute(f"SELECT id FROM projects WHERE board_id IN ({','.join('?' * len(on_boards))})", tuple(on_boards))}
                 if on_boards else own_rules)
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
        prior, since, counted = earlier_sends(db, msgs, own)
        found = {**schedule(msgs, settings, now, days, prior, since), 'counted': counted}
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
            # ...or one the thread itself shows: the owner's earlier sends already reached the maximum
            found = {**found, 'state': 'end' if ours or found.get('prior') else 'done'}
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


def due(db, now, sendable, mine=mine_default, own=None):
    return [x for x in plan(db, now, sendable, mine, own) if x['state'] == 'due']


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


def views(db, now, sendable, mine=mine_default, own=None):
    """{'boards': {board_id: {'on', 'next_at'}}, 'projects': {project_id: {'on', 'state', 'next_at', 'n', 'max', 'own', 'end'}}}:
    next_at the next follow-up's date (due or waiting), end the quiet note when a round ended without a reply."""
    out = {'boards': {}, 'projects': {}}
    try:
        for r in db.execute("SELECT ref,settings FROM follow_up_rules WHERE scope='board'"):
            out['boards'][r[0]] = {'on': bool(json.loads(r[1]).get('on')), 'next_at': None}
        items = plan(db, now, sendable, mine, own)
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


def short_name(name, board):
    """A project's name without its board's in front: on the board "Editorial listing exchanges", the project
    "Editorial listing exchanges: Acme" is "Acme", also when that front was cut short to fit ("Editorial listing
    exchang: Acme"). Any other name stays as it is."""
    name, board = str(name or ''), ' '.join(str(board or '').split())
    head, sep, rest = name.partition(': ')
    head = ' '.join(head.split())
    if sep and rest.strip() and board and len(head) >= min(len(board), 8) and board.lower().startswith(head.lower()):
        return rest.strip()
    return name


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
    return {r['suggestion_id']: {'project': r['project'], 'name': short_name(r['project'], r['board']), 'project_id': 'project:' + str(r['project_id']), 'board': r['board'],
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
    board, batch, total, done, sent, going, held, held_new, done_at}] (batch: its id, so a finished one can be dismissed): held the ones not sent because the thread changed
    (held_new) or couldn't be checked; done_at, while it goes, about when the last one goes (done_around). Batches of one
    aren't shown: that to-do says how its send went."""
    out = []
    try:
        groups = [r[0] for r in db.execute('SELECT DISTINCT grp FROM follow_up_sends')]
    except Exception:  # noqa: BLE001 - no table yet
        return out
    since = (parse(now) - dt.timedelta(seconds=PROGRESS_KEEP)).isoformat()
    for grp in groups:
        batch = db.execute('SELECT batch FROM follow_up_sends WHERE grp=? ORDER BY queued_at DESC,rowid DESC LIMIT 1', (grp,)).fetchone()[0]
        jobs = db.execute('SELECT j.status,j.updated_at,s.sender,h.why held FROM follow_up_sends s JOIN action_jobs j ON j.id=s.job_id '
                          "LEFT JOIN follow_up_holds h ON h.job_id=s.job_id AND j.status='blocked' WHERE s.batch=?", (batch,)).fetchall()
        if len(jobs) < 2:
            continue
        going = sum(j['status'] in GOING for j in jobs)
        if not going and max(j['updated_at'] for j in jobs) < since:
            continue
        board = db.execute('SELECT name FROM boards WHERE id=?', (int(grp.split(':')[1]),)).fetchone() if grp.startswith('board:') else None
        out.append({'group': grp if grp.startswith('board:') else None, 'board': board[0] if board else None, 'batch': batch, 'total': len(jobs),
                    'done': len(jobs) - going, 'sent': sum(j['status'] == 'sent' for j in jobs), 'going': going > 0,
                    'held': sum(j['held'] is not None for j in jobs), 'held_new': sum(j['held'] == 'changed' for j in jobs),
                    'done_at': done_around(db, jobs, now) if going else None})
    return out


def done_around(db, jobs, now):
    """About when a batch's last follow-up goes: per account, its first queued one when the spacing lets it (follow_up_pace,
    else now), then one every average gap; the latest of the accounts. ISO."""
    start, out = parse(now), parse(now)
    mean = (SEND_GAP[0] + SEND_GAP[1]) / 2
    for who in {j['sender'] for j in jobs if j['status'] == 'queued'}:
        left = sum(j['sender'] == who and j['status'] == 'queued' for j in jobs)
        row = db.execute('SELECT next_at FROM follow_up_pace WHERE sender=?', (who,)).fetchone()
        first = max(start, parse(row[0])) if row else start
        out = max(out, first + dt.timedelta(seconds=mean * (left - 1)))
    return out.replace(microsecond=0).isoformat()


# ------------------------------------------------------------------ Change in the review

CHANGE_NOTE = ('This message came from the follow-up review\'s Change: rewrite only the text of this to-do\'s follow-up draft as it asks. '
               'Keep the draft\'s kind, recipients, sending account and thread exactly as they are, and save it without send_now: the owner reads it and sends it.')
CHANGE_MAX = 2000  # characters of the owner's instruction


def change_note(skills_on):
    """The rewrite rules for a Change, and the owner's skills that are on right now ({name, description, path}): a skill
    added after this session began isn't in its skill list yet, so the turn names each one with its SKILL.md to read."""
    if not skills_on:
        return CHANGE_NOTE
    listed = '\n'.join(f"- {k['name']}: {' '.join(str(k.get('description') or '').split())[:200]} ({k['path']})" for k in skills_on[:30])
    return (CHANGE_NOTE + ' Write it like a new draft, with the owner\'s style and everything above. The owner\'s skills that are on now '
            '(also ones added since this session began) are below: when the owner\'s words point to one ("use the skill", its name or what '
            'it is for), or one is clearly for this kind of follow-up, read its SKILL.md now and follow it in the rewrite.\n' + listed)
# What a rewrite keeps: the channel, who gets it, from which account, and the thread or chat it goes in
ROUTE = ('kind', 'account_id', 'from', 'to', 'cc', 'bcc', 'to_email', 'thread_id', 'conversation_id', 'chat_id', 'user_id', 'handle', 'profile')


def _route_value(value):
    if isinstance(value, list):
        return sorted(str(v).strip().lower() for v in value)
    return str(value).strip().lower() if isinstance(value, str) else value


def route(action):
    """Where a draft goes (ROUTE), comparable between two drafts."""
    return {k: _route_value(action[k]) for k in ROUTE if isinstance(action, dict) and action.get(k) not in (None, '', [])}


def changing(db, suggestion_id, decision_id, revision, action, now):
    """Remember a Change from the review: the draft it rewrites and where that draft goes."""
    db.execute('INSERT OR REPLACE INTO follow_up_changes(decision_id,suggestion_id,revision,route,at) VALUES(?,?,?,?,?)',
               (decision_id, suggestion_id, revision, json.dumps(route(action)), now))


def change_of(db, suggestion_id, job_id):
    """The review's Change this preparation works on, or None."""
    if not job_id:
        return None
    try:
        return db.execute('SELECT c.* FROM follow_up_changes c JOIN preparations p ON p.decision_id=c.decision_id '
                          'WHERE p.suggestion_id=? AND p.job_id=? AND c.suggestion_id=?', (suggestion_id, job_id, suggestion_id)).fetchone()
    except Exception:  # noqa: BLE001 - no table yet
        return None


def change_problem(change, drafts, send_now):
    """Why a rewrite from the review's Change can't be saved as it is, or None: it is never sent from there, and the
    draft keeps where it goes (ROUTE). drafts: the result's message drafts."""
    if not change:
        return None
    if send_now:
        return 'A Change from the follow-up review is never sent from here: save the draft without send_now, for the owner to read and send'
    before = json.loads(change['route'])
    for draft in drafts:
        after = route(draft)
        moved = [k for k in before if after.get(k) != before[k]]
        if moved:
            return ('Only the text changes in a Change from the follow-up review: keep the draft\'s ' + ', '.join(moved)
                    + ' as it was and save it again')
    return None

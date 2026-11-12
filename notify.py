"""Notifications: which kinds reach the owner on which channel, when they are left out, and the morning and evening
digests (docs/help/notifications.md). The evening digest is set like the morning's: its own row here (kind 'evening')
and its time under Work hours (`evening_at` in config.json, 15 minutes before the end of the hours unless set).

Kinds: a new to-do, a result or question (ready to approve, stuck, a sign-in, a Fleet question), a reminder (a snooze or
a wait coming back) and the morning digest. Channels: push (the dashboard app on a phone or computer, sent by this
Machine and encrypted for each device, push-send.mjs), Telegram, and email (through the control plane's mailer, for
hosted and paired Machines). The mobile app (a shell around the dashboard, which has no Web Push) gets its push as a
wakeup without any text, sent by the control plane to the owner's phones (app_push); this Machine keeps only which
phones have it (notify_app_devices), never their tokens. The Android app then asks this Machine for the to-do's short
line (app_line, GET /api/notice) over its own sign-in and shows that: the line never passes through FCM or the cloud.

Smart, like Slack (help center: "Configure your Slack notifications", "Set your Slack status and availability", "Guide
to email notifications"):
- Presence. A dashboard counts as in use while it is visible, in focus and touched in the last IDLE_AFTER (Slack: away
  after 10 minutes without input). Open in the background, minimized or idle, it does not: the owner gets notified.
- While in use, nothing buzzes: no push to any device, Telegram arrives silently, and what came in counts as seen.
- Push when away: right away when the owner has been away a while, else AWAY_GRACE after they left (Slack: mobile one
  minute after the desktop locks). Left out when they came back and saw it in the meantime.
- Email for what can't wait (calm_reason) and is still unseen and still waiting EMAIL_AFTER later, bundled into one, at
  most once per EMAIL_EVERY (Slack: bundled every 15 minutes or hourly, only while inactive). Morning summary (the
  digest, compose) on work days.
- A teammate's handoff to an owner their Machine can't ping (no phone or Telegram): one email of its own for it, also
  EMAIL_AFTER later and only while still unseen and waiting (take_handoffs, handoff_mail).
- A batch buzzes once (assistant.deliver_one); nothing goes out outside work hours (Slack: notification schedule).

Calm (docs/vision.md, "instant and calm"): only what can't wait buzzes (calm_reason). A new to-do that can wait is on
the dashboard and in the next morning summary, without a push, a Telegram buzz or a waiting email. What can't wait: due
today, someone waiting on the owner's reply, a sign-in a run needs, urgent, or a snooze the owner set coming back. Even
then: on a day off only what is urgent or due, at most PUSH_CAP a day, and none after AWAY_DAYS without a dashboard
visit (the morning summary keeps going). So the one email a day is the morning summary."""
from __future__ import annotations

import datetime as dt
import http.client
import json
import logging
import re
import threading
import time
import uuid
import urllib.error
import urllib.request

import clear_pace
from i18n import t
import timeutil

LOG = logging.getLogger('personal-assistant')

KINDS = ('todo', 'result', 'reminder', 'digest', 'evening')
CHANNELS = ('push', 'telegram', 'email')
# Email is on for every kind: many people never get push working, and it only goes for what is still unseen and
# waiting after EMAIL_AFTER, bundled. The digest is a push and an email; Telegram already has the weekly recap.
DEFAULTS = {'todo': {'push': True, 'telegram': True, 'email': True}, 'result': {'push': True, 'telegram': True, 'email': True},
            'reminder': {'push': True, 'telegram': True, 'email': True}, 'digest': {'push': True, 'telegram': False, 'email': True},
            'evening': {'push': True, 'telegram': False, 'email': True}}  # the evening digest: as the morning's
SCHEMA = 'CREATE TABLE IF NOT EXISTS notify_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL)'
DIGESTS = 'CREATE TABLE IF NOT EXISTS notify_digests(day TEXT PRIMARY KEY,status TEXT NOT NULL,created_at TEXT NOT NULL,channels TEXT)'
ACTIVE_FOR = 120  # seconds: a page's "in use" lasts this long (it says so every minute while it is)
IDLE_AFTER = 600  # seconds without a key, a click, a scroll or a touch: idle (Slack: away after 10 minutes)
AWAY_GRACE = 60  # seconds after the owner left the dashboard before a push goes (Slack: a minute after the screen locks)
EMAIL_AFTER = 15 * 60  # still unseen and waiting this long after it came in: an email
EMAIL_EVERY = 60 * 60  # at most one such email per hour, all that waits in it
EMAIL_STALE = 3 * 60 * 60  # not emailed by then (outside hours, the cap): the dashboard and the digest have it
HANDOFF_STALE = 24 * 60 * 60  # a handoff email still not taken by then (the mailer down, an unsure send): the dashboard has it
# A held push that still couldn't go after EMAIL_AFTER is dropped: the email for what still waits takes over by then
QUEUE = ('CREATE TABLE IF NOT EXISTS notify_queue(id INTEGER PRIMARY KEY,channel TEXT NOT NULL,kind TEXT NOT NULL,ref TEXT,'
         'title TEXT NOT NULL,payload TEXT,show INTEGER NOT NULL DEFAULT 1,created REAL NOT NULL,due REAL NOT NULL)')
DIGEST_VIEW = '#calendar?view=agenda'  # where the morning's notification opens: today's meetings and what's due
DIGEST_LATE = dt.timedelta(hours=3)  # a digest not sent by then (the Machine was off) waits for the next day
# The evening digest: what got done and what's open for the next work day, by default this long before the hours end
EVENING_BEFORE = dt.timedelta(minutes=15)
EVENING_LISTED = 3  # to-dos named per part; the rest is a count
EVENING_VIEW = '#todos'  # where the evening's notification opens: what still needs the owner
MAIL_SUBJECT, MAIL_TEXT = 120, 4000
# Phones with the mobile app: what Settings shows. The control plane holds their push tokens and sends the wakeups.
APP_DEVICES = 'CREATE TABLE IF NOT EXISTS notify_app_devices(id TEXT PRIMARY KEY,platform TEXT NOT NULL,label TEXT NOT NULL,created_at TEXT NOT NULL)'
APP_KINDS = ('todo', 'result', 'reminder', 'digest', 'fleet', 'test', 'clear')  # the control plane's fixed text per kind; clear: none
APP_ID = re.compile(r'[A-Za-z0-9_-]{1,64}')
# The line a woken app shows ("Ready: Reply about the listing"), by the wakeup's tag: the same words as the web push,
# short. Kept APP_LINE_DAYS, at most APP_LINES of them.
# A tag that is no to-do (the morning) can keep a body line under it too ("3 to-dos: ... · First meeting 10:00").
APP_LINES_TABLE = "CREATE TABLE IF NOT EXISTS notify_app_lines(tag TEXT PRIMARY KEY,line TEXT NOT NULL,at REAL NOT NULL,body TEXT NOT NULL DEFAULT '')"
APP_LINE, APP_LINES, APP_LINE_DAYS, APP_BODY = 60, 200, 3, 120
# Calm: what can't wait (calm_reason). A safety net, not a budget: a busy day of real deadlines still gets through.
URGENT_WHY = ('urgent', 'due', 'reminder')  # what still buzzes on a day off
PUSH_CAP = 8  # pushes a day at most
AWAY_DAYS = 3  # no dashboard visit (or decision) in this many days: only the morning summary
VISIT_EVERY = 600  # seconds: the kept visit time moves at most this often
OWNER_SOURCES = ('dashboard', 'telegram', 'owner-chat', 'voice')  # decisions that show the owner is around
PILE = 10  # this many waiting: the morning summary's headline names the pile and the time to clear it
HEAD_TITLE = 50  # the one to-do the morning summary's headline names: at most this long
LINKS = re.compile(r' · \[[^\]\n]+\]\([^)\s]+\)')  # a summary line's Open link: Telegram gets the line without it


def ensure(db):
    db.execute(SCHEMA)
    db.execute(DIGESTS)
    db.execute(QUEUE)
    columns = {r[1] for r in db.execute('PRAGMA table_info(notify_queue)')}
    for name, definition in (('delivery', 'TEXT'), ('batch', 'TEXT'), ('claimed_until', 'REAL NOT NULL DEFAULT 0')):
        if name not in columns:
            db.execute(f'ALTER TABLE notify_queue ADD COLUMN {name} {definition}')
    for row in db.execute('SELECT id FROM notify_queue WHERE delivery IS NULL').fetchall():
        db.execute('UPDATE notify_queue SET delivery=? WHERE id=?', (uuid.uuid4().hex, row[0]))
    db.execute(APP_DEVICES)
    db.execute(APP_LINES_TABLE)
    if 'body' not in {r[1] for r in db.execute('PRAGMA table_info(notify_app_lines)')}:
        db.execute("ALTER TABLE notify_app_lines ADD COLUMN body TEXT NOT NULL DEFAULT ''")


def prefs(db):
    """{kind: {channel: bool}}: only the channels a kind can use."""
    ensure(db)
    stored = {k: v for k, v in db.execute('SELECT key,value FROM notify_prefs')}
    return {kind: {ch: stored.get(f'{kind}.{ch}', 'on' if on else 'off') == 'on' for ch, on in chans.items()}
            for kind, chans in DEFAULTS.items()}


def allowed(db, kind, channel):
    return bool(prefs(db).get(kind, {}).get(channel))


def set_pref(db, kind, channel, on):
    if kind not in DEFAULTS or channel not in DEFAULTS[kind]:
        raise ValueError('That notification can’t go there')
    ensure(db)
    db.execute('INSERT INTO notify_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',
               (f'{kind}.{channel}', 'on' if on else 'off'))
    return prefs(db)


def kind_of(row):
    """The kind of a card delivery, as deliver_one sends it."""
    if row.get('_result_notice'):
        return 'result'
    if row.get('reminder'):
        if row.get('status') in ('prepared', 'instructions') or row.get('preparation_status') == 'blocked':
            return 'result'
        return 'todo' if row.get('_first') else 'reminder'  # never delivered before (deliver_one): new, no reminder
    return 'todo'


def wall():
    return time.time()  # looked up at each call, so a test can move the clock


# -- presence: is the owner using a dashboard right now (kept in memory; a restart forgets it, which only means a
# notification may go out). Each open page (client) says whether it is in use (visible, in focus and touched in the
# last IDLE_AFTER) and how long ago it was last touched. `last` is when the owner last touched one: what came in
# before that counts as seen.
_presence = {'clients': {}, 'last': 0.0}
_lock = threading.Lock()
CLIENTS = 20


def mark_active(clock=wall, client='page', on=True, idle=0):
    """A page's heartbeat: in use (on) or not (in the background, minimized, idle, or closing), last touched `idle`
    seconds ago. A page that was never in use (opened in the background) doesn't move `last`."""
    at = clock()
    with _lock:
        clients = _presence['clients']
        was = clients.get(client)
        if on or (was and was['on']):
            _presence['last'] = max(_presence['last'], at - max(0, idle))
        clients[client] = {'at': at, 'on': bool(on)}
        for old in sorted(clients, key=lambda c: clients[c]['at'])[:max(0, len(clients) - CLIENTS)]:
            clients.pop(old)


def active(clock=wall):
    """A dashboard in use now, on any device (Slack: active). A page that stopped saying so lets go after ACTIVE_FOR."""
    at = clock()
    with _lock:
        return any(c['on'] and at - c['at'] < ACTIVE_FOR for c in _presence['clients'].values())


def last_seen(clock=wall):
    """When the owner last touched a dashboard (epoch seconds, 0 for not since the start)."""
    with _lock:
        return _presence['last']


def reset_active():
    with _lock:
        _presence['clients'].clear()
        _presence['last'] = 0.0


def push_now(clock=wall):
    """A push may go now: no dashboard in use, and AWAY_GRACE since the owner last touched one (Slack: mobile a minute
    after the desktop locks). Otherwise it is held (hold) and goes once that is true, unless they saw it first."""
    return not active(clock) and clock() >= last_seen(clock) + AWAY_GRACE


# -- calm: only what can't wait buzzes
def _stamp(db, key, value):
    db.execute('INSERT INTO notify_prefs(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, str(value)))


def visited(db, clock=wall):
    """A dashboard is in use: kept (at most every VISIT_EVERY), so a restart doesn't forget the owner was here."""
    ensure(db)
    at = clock()
    row = db.execute("SELECT value FROM notify_prefs WHERE key='_visit_last'").fetchone()
    if not row or at - float(row[0] or 0) >= VISIT_EVERY:
        _stamp(db, '_visit_last', at)


def away(db, clock=wall):
    """No dashboard visit and no decision of the owner's (dashboard, Telegram, chat, voice) in AWAY_DAYS. A Machine that
    never kept a visit starts its count now, so nobody goes quiet the day this arrives."""
    ensure(db)
    at = clock()
    row = db.execute("SELECT value FROM notify_prefs WHERE key='_visit_last'").fetchone()
    if not row:
        _stamp(db, '_visit_last', at)
        return False
    last = max(float(row[0] or 0), last_seen(clock))
    if at - last < AWAY_DAYS * 86400:
        return False
    since = dt.datetime.fromtimestamp(at - AWAY_DAYS * 86400, dt.timezone.utc).isoformat()
    try:
        decided = db.execute('SELECT 1 FROM decisions WHERE source IN (' + ','.join('?' * len(OWNER_SOURCES)) + ') AND created_at>=? LIMIT 1',
                             (*OWNER_SOURCES, since)).fetchone()
    except Exception:  # noqa: BLE001 - no decisions table (a bare test database): only the visit counts
        decided = None
    return not decided


def pushed_today(db, day):
    """How many pushes buzzed on `day` (local, ISO)."""
    ensure(db)
    row = db.execute("SELECT value FROM notify_prefs WHERE key='_push_day'").fetchone()
    when, _, count = str(row[0] if row else '').partition(' ')
    return int(count) if when == day and count.isdigit() else 0


def count_push(db, day):
    """One more push buzzed on `day`."""
    _stamp(db, '_push_day', f'{day} {pushed_today(db, day) + 1}')


def calm_reason(db, why, work_day, day, clock=wall):
    """Why a to-do's notification stays quiet now, or '' when it may buzz. why: what makes it unable to wait ('urgent',
    'due', 'reply', 'signin', 'reminder', or '' for nothing, deliver.why_now). 'later' (it can wait: the dashboard and
    the morning summary have it), 'day_off' (a non-work day: only URGENT_WHY), 'away' (no visit in AWAY_DAYS), 'cap'
    (PUSH_CAP pushes today already)."""
    if not why:
        return 'later'
    if not work_day and why not in URGENT_WHY:
        return 'day_off'
    if away(db, clock):
        return 'away'
    if pushed_today(db, day) >= PUSH_CAP:
        return 'cap'
    return ''


def hold(db, channel, kind, title, due, ref=None, payload=None, show=True, clock=wall):
    """Queue a push (channel 'push', its payload) or an email line (channel 'email') to go at `due` unless seen."""
    ensure(db)
    db.execute('INSERT INTO notify_queue(channel,kind,ref,title,payload,show,created,due,delivery) VALUES(?,?,?,?,?,?,?,?,?)',
               (channel, kind, ref, title[:200], json.dumps(payload) if payload is not None else None, 1 if show else 0, clock(), due, uuid.uuid4().hex))


def take_due(db, still_open=lambda ref: True, clock=wall):
    """What goes now: (pushes [{payload, kind}], email lines [{title, show, kind}]). Drops what the owner saw (touched a
    dashboard after it came in), what no longer waits for them (still_open) and email lines past EMAIL_STALE. Pushes go
    when push_now; email lines together once the oldest is due and the last email is EMAIL_EVERY ago, never while a
    dashboard is in use. Selected rows are leased for 60 seconds, not deleted; delivered() removes them only after
    a successful receipt. A failed email keeps the same batch so a lost HTTP response cannot create another send."""
    ensure(db)
    at, seen = clock(), last_seen(clock)
    # Why a waiting email never went, in the log (seen on a dashboard, too old, handled), so "no email" can be checked
    dropped = {'seen': db.execute("SELECT count(*) FROM notify_queue WHERE channel='email' AND created<=?", (seen,)).fetchone()[0]}
    db.execute('DELETE FROM notify_queue WHERE created<=?', (seen,))
    dropped['stale'] = db.execute("DELETE FROM notify_queue WHERE channel='email' AND created<?", (at - EMAIL_STALE,)).rowcount
    # Kept until a receipt, but never retried forever: a push only while it is still news, a handoff for a day
    db.execute("DELETE FROM notify_queue WHERE (channel='push' AND due<?) OR (channel='handoff' AND created<?)",
               (at - EMAIL_AFTER, at - HANDOFF_STALE))
    rows = [dict(r) for r in db.execute('SELECT * FROM notify_queue WHERE claimed_until<=? ORDER BY created,id', (at,))]
    gone = [r['id'] for r in rows if r['ref'] and not still_open(r['ref'])]
    dropped['handled'] = sum(r['channel'] == 'email' for r in rows if r['id'] in gone)
    if any(dropped.values()):
        LOG.info('notify email dropped seen=%d stale=%d handled=%d', dropped['seen'], dropped['stale'], dropped['handled'])
    rows = [r for r in rows if r['id'] not in gone]
    pushes, lines = [], []
    if not active(clock):
        pushes = [r for r in rows if r['channel'] == 'push' and r['due'] <= at] if push_now(clock) else []
        mails = [r for r in rows if r['channel'] == 'email']
        last = float(dict(db.execute("SELECT key,value FROM notify_prefs WHERE key='_mail_last'").fetchall()).get('_mail_last') or 0)
        if mails and mails[0]['due'] <= at and at - last >= EMAIL_EVERY:
            batch = mails[0]['batch'] or uuid.uuid4().hex
            lines = [r for r in mails if r['batch'] == batch] if mails[0]['batch'] else [r for r in mails if not r['batch']]
            for r in lines:
                r['batch'] = batch
                db.execute('UPDATE notify_queue SET batch=? WHERE id=?', (batch, r['id']))
    db.executemany('DELETE FROM notify_queue WHERE id=?', [(i,) for i in gone])
    db.executemany('UPDATE notify_queue SET claimed_until=? WHERE id=?', [(at + 60, r['id']) for r in pushes + lines])
    return ([{'payload': json.loads(r['payload'] or '{}'), 'kind': r['kind'], 'delivery': r['delivery']} for r in pushes],
            [{'title': r['title'], 'show': bool(r['show']), 'kind': r['kind'], 'delivery': r['delivery'], 'batch': r['batch'], 'ref': r['ref']}
             for r in lines])


def delivered(db, items):
    """Remove only the exact queue entries with a successful delivery receipt."""
    db.executemany('DELETE FROM notify_queue WHERE delivery=?', [(r['delivery'],) for r in items])


def take_handoffs(db, clock=wall):
    """Handoff emails that go now (hold_handoff): [{title, show, name, id}]. Each was held once for its handoff, went
    when due and no dashboard is in use, and is gone when the owner saw it or it no longer waits (take_due runs first).
    Outside work hours notify_step doesn't come here, so one held then goes when the hours start."""
    ensure(db)
    at = clock()
    if active(clock):
        return []
    rows = [dict(r) for r in db.execute("SELECT * FROM notify_queue WHERE channel='handoff' AND due<=? AND claimed_until<=? ORDER BY created,id", (at, at))]
    db.executemany('UPDATE notify_queue SET claimed_until=? WHERE id=?', [(at + 60, r['id']) for r in rows])
    return [{'title': r['title'], 'show': bool(r['show']), 'name': json.loads(r['payload'] or '{}').get('name') or '',
             'id': (r['ref'] or '').partition(':')[2], 'delivery': r['delivery']} for r in rows]


def handoff_mail(item, root=''):
    """The one email for a teammate's handoff to an owner their Machine can't ping (no phone or Telegram): who handed
    what, and a link to the dashboard. Only the title, and only where the security level shows it."""
    name = item['name'] or t('Your teammate')
    subject = t('{} handed you a to-do: {}', name, item['title']) if item['show'] else t('{} handed you a to-do', name)
    body = []
    if root:
        # [label](url): the control plane's mailer makes it a link, "label (url)" in the text part (cloud/emails.py)
        body += ['[' + t('Accept or decline it on The Machine') + '](' + root + ('#fleet=' + item['id'] if item.get('id') else '') + ')', '']
    body.append(t('You get this once per handoff, as your Machine can’t ping you on a phone or Telegram. Turn it off in Settings, Notifications.'))
    return {'subject': subject, 'text': '\n'.join(body).strip()}


def mailed(db, clock=wall):
    """Remember when the last waiting-for-you email went (EMAIL_EVERY)."""
    ensure(db)
    db.execute("INSERT INTO notify_prefs(key,value) VALUES('_mail_last',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(clock()),))


def mail_links(ref, root=''):
    """An email line's quick buttons, as links (docs/help/notifications.md): Open and Snooze for a to-do, Open for a
    Fleet question. They only open the dashboard (Snooze at its snooze times): a link in an email never does anything
    by itself, since mail apps and scanners open links on their own."""
    kind, _, ident = str(ref or '').partition(':')
    if not root:
        return ''
    if kind == 'suggestion' and re.fullmatch(r'[a-f0-9]{16}', ident):
        return f" · [{t('Open')}]({root}#chat={ident}) · [{t('Snooze')}]({root}#snooze={ident})"
    if kind == 'fleet' and re.fullmatch(r'q_[a-f0-9]{16}', ident):
        return f" · [{t('Open')}]({root}#fleet={ident})"
    return ''


def waiting_mail(lines, root=''):
    """One email for what still waits: {subject, text}. Titles only where the security level shows them, each with its
    quick links (mail_links)."""
    show = all(line['show'] for line in lines)
    if len(lines) == 1 and show:
        subject = t('Waiting for you: {}', lines[0]['title'])
    else:
        subject = t('{} things wait for you', len(lines))
    body = []
    if show:
        body += ['• ' + line['title'] + mail_links(line.get('ref'), root) for line in lines[:8]]
        if len(lines) > 8:
            body.append(t('• +{} more', len(lines) - 8))
    else:
        body.append(t('{} things wait for you', len(lines)))
    body.append('')
    if root:
        body.append(t('Open The Machine: {}', root))
    body.append(t('You get this when something waits for you and you haven’t seen it on the dashboard. Change it in Settings, Notifications.'))
    return {'subject': subject, 'text': '\n'.join(body).strip()}


# -- the morning digest
def digest_time(digest_at, morning=None, start=None, end=None):
    """When the morning digest goes ('HH:MM'): its own time, but never before 5 minutes after the morning snooze time
    (timeutil.digest_floor; work_hours.morning, where Tomorrow, 3 days and 1 week land), so the to-dos that came back
    that morning are in it. A digest set later keeps its time. When that would fall past midnight or outside the hours,
    its own time stays. Work hours save the digest that way too; this holds for a config.json edited by hand.
    The dashboard shows the same time (settings-device.js, digestTime)."""
    if not morning:
        return digest_at
    return timeutil.digest_floor(digest_at, {'morning': morning, 'start': start or '00:00', 'end': end or '00:00'})


def digest_due(local, digest_at, start, end, work_day, sent_today, morning=None):
    """Whether the digest goes now: a work day, at its time (digest_time: after the morning's snoozes came back; or the
    start of hours when it is set earlier), within hours, at most DIGEST_LATE after, once a day."""
    if sent_today or not work_day(local):
        return False
    digest_at = digest_time(digest_at, morning, start, end)
    at = max(digest_at, start) if start < end else digest_at
    hour, minute = (int(x) for x in at.split(':'))
    target = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if local < target or local - target > DIGEST_LATE:
        return False
    now_hm = local.strftime('%H:%M')
    return start == end or (start <= now_hm < end if start < end else now_hm >= start or now_hm < end)


def digest_sent(db, day):
    """Whether the digest of `day` (local, ISO) went out or is going out."""
    return bool(db.execute('SELECT 1 FROM notify_digests WHERE day=?', (day,)).fetchone())


def digest_claim(db, day, at):
    """Claims the digest of `day` for this run, in its own write transaction: False when one already has it."""
    db.execute('BEGIN IMMEDIATE')
    if digest_sent(db, day):
        return False
    db.execute("INSERT INTO notify_digests(day,status,created_at) VALUES(?,'sending',?)", (day, at))
    return True


def digest_done(db, day, status, channels):
    """The digest of `day` is done: sent (on `channels`), empty or not sent."""
    channels = json.dumps(channels, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    db.execute('UPDATE notify_digests SET status=?,channels=? WHERE day=?', (status, channels, day))


def drop_covered(db, refs, before):
    """The morning digest email went and listed these to-dos (refs, 'suggestion:<id>'): the waiting-for-you email lines
    held for them before it (created up to `before`, epoch seconds) are dropped, so the next hourly email doesn't repeat
    them. What comes in after the digest still gets its line. Returns how many."""
    ensure(db)
    refs = sorted({str(r) for r in refs if r})
    gone = 0
    for n in range(0, len(refs), 400):
        chunk = refs[n:n + 400]
        gone += db.execute(f"DELETE FROM notify_queue WHERE channel='email' AND created<=? AND ref IN ({','.join('?' * len(chunk))})",
                           (before, *chunk)).rowcount
    return gone


def drop_pushes(db):
    """Outside work hours a held push is dropped: the email for what still waits takes over."""
    db.execute("DELETE FROM notify_queue WHERE channel='push'")


def drop_all(db):
    """After an import (machine/export/hold.py): what waited was for the old Machine. Returns how many."""
    return db.execute('DELETE FROM notify_queue').rowcount


def brief_line(titles, show_text=True):
    """The team brief notification's body: how many things it has for the team and the first two, as the brief
    shows them ("3 things for the team: Acme is waiting for a reply, Globex went quiet, …"). Without show_text only
    how many. Nothing: the brief's own calm line."""
    if not titles:
        return t('Nothing that needs the team.')
    if not show_text:
        return t('{} things for the team', len(titles))
    names = ', '.join(clip(x, 50) for x in titles[:2]) + (', …' if len(titles) > 2 else '')
    return clip(t('{} things for the team: {}', len(titles), names), APP_BODY)


def open_order(rows, current):
    """The waiting to-dos [{id, title, due, due_at, created_at}] in the order the dashboard's open lists show them
    (openOrder in dashboard/todos-cards.js): overdue or due by tomorrow first, then newest first by created_at, then
    the id. `current` is the owner's local now (an aware datetime). The dashboard breaks a same-moment tie by the
    people weight first; that needs the Graph, so here the id alone does."""
    tomorrow = (current + dt.timedelta(days=1)).date().isoformat()

    def at(value):
        try:
            when = dt.datetime.fromisoformat(str(value))
            return (when if when.tzinfo else when.replace(tzinfo=current.tzinfo)).timestamp()
        except (TypeError, ValueError):
            return None

    def soon(row):
        if not row.get('due'):
            return False
        due_at = at(row.get('due_at')) if row.get('due_at') else None
        return (due_at is not None and due_at < current.timestamp()) or str(row['due']) <= tomorrow

    return sorted(rows, key=lambda r: (not soon(r), -(at(r.get('created_at')) or 0), str(r.get('id') or '')))


def promised_today(promises, top, today, text):
    """The owner's own promises due today, still open (or their to-do still open), for the digest: [{id, title, covers}].
    A to-do made from the promise's message (or its card) is that promise's work (covers): listed with the promise, not
    again under Overnight or Waiting for you. top: the waiting to-dos with their event_ids; text: a promise's line."""
    by_event = {}
    for r in top:
        try:
            for event in json.loads(r.get('event_ids') or '[]'):
                by_event.setdefault(event, r['id'])
        except (TypeError, ValueError):
            pass
    return [{'id': 'promise:' + str(p['id']), 'title': text(p), 'covers': p.get('suggestion_id') or by_event.get(p['event_id'])}
            for p in promises if p['direction'] == 'mine' and p.get('due') == today and p['state'] in ('open', 'card')]


def first_name(name):
    """The owner's first name for the greeting, or '' when it doesn't look like one."""
    first = (str(name or '').split() or [''])[0]
    return first if re.fullmatch(r"[^\W\d_][\w'’-]*", first) else ''


def asks(outcome):
    """Whether a to-do's result (its outcome JSON) needs the owner and says so with a question: it waits on their answer,
    so it isn't one to clear at a tap (machine/cards.py ask_question, needsAsk() in the dashboard)."""
    try:
        result = json.loads(outcome or '{}')
        return result.get('state') == 'needs_you' and str(result.get('needs') or '').strip().endswith('?')
    except (ValueError, TypeError, AttributeError):
        return False


def headline(name, ready=0, replies=0, due=0, piled=0, minutes=0, first_at='', new=0, title=''):
    """The morning summary's first line (the email's subject, the push's title): a greeting with the owner's first name
    and the one thing that makes today matter, only when it is true ("Morning Sam, 2 replies are ready to send"). With
    nothing worth saying: the greeting alone. In order: drafts ready for their OK, what is due today, a pile of PILE or
    more (and the time to clear it), the first meeting, what is new. Whole sentences per case, for the catalogs.
    title: the one to-do ready for their OK, named so the line says what waits ("Morning Sam, ready for your OK: Send
    the signed order form"); left out (more than one, or no titles shown) the count says what kind ("2 to-dos ready")."""
    if ready and replies >= ready:
        return t('Morning {}, {} replies are ready to send', name, ready) if name else t('Good morning, {} replies are ready to send', ready)
    if ready == 1 and title:
        return t('Morning {}, ready for your OK: {}', name, clip(title, HEAD_TITLE)) if name else t('Good morning, ready for your OK: {}', clip(title, HEAD_TITLE))
    if ready:
        return t('Morning {}, {} to-dos ready for your OK', name, ready) if name else t('Good morning, {} to-dos ready for your OK', ready)
    if due:
        return t('Morning {}, {} due today', name, due) if name else t('Good morning, {} due today', due)
    if piled >= PILE and minutes:
        return (t('Morning {}, {} waiting, about {} min to clear', name, piled, minutes) if name
                else t('Good morning, {} waiting, about {} min to clear', piled, minutes))
    if piled >= PILE:  # none of them clears at a tap: no time said
        return t('Morning {}, {} waiting', name, piled) if name else t('Good morning, {} waiting', piled)
    if first_at:
        return t('Morning {}, first meeting at {}', name, first_at) if name else t('Good morning, first meeting at {}', first_at)
    if new:
        return t('Morning {}, {} new to-dos', name, new) if name else t('Good morning, {} new to-dos', new)
    return t('Morning {}', name) if name else t('Good morning')


def compose(meetings, due, overnight, root='', show_text=True, clock=lambda iso: iso[11:16], waiting=None, total=None,
            top=None, ready=(), promised=(), per=None, name='', replies=(), asking=()):
    """The morning summary from its parts, short and scannable: meetings [{at, title}], due and overnight [{id?, title}].
    Returns None when there is nothing to say, else {push: {title, body, url, tag}, text, subject}.

    It reads: a greeting with what makes today matter (headline, also the subject and the push's title), right under it
    at most three lines that each start with what to do (a to-do's title says that) with one Open link, then how many
    more can wait and the time they take at the owner's own pace ("12 more can wait, about 5 min to clear."; per:
    seconds per action, clear_pace), then the day's meetings in a line when there are any (never between the headline
    and its own list). The time counts only what clears at that pace: not the to-dos that wait on the owner's answer
    (asking: their ids, as the dashboard's header leaves them out); with none left to count, the line says how many
    wait and no time. No news, no tips.

    The three: ready [{id?, title}] (prepared, waiting for the owner's OK; replies: the ids of those that are a reply
    someone waits for) and promised [{id?, title}] (the owner's own promises due today; covers: the id of a to-do made
    from that promise) first, then what is due, the first meeting, what came in overnight, and the waiting to-dos in the
    dashboard's order (top, open_order). A to-do is listed once (by id, else by title). total: how many to-dos wait
    (waiting_count); left out, the ones given here. waiting is kept for callers that pass it and not used.
    Without show_text (Careful, or notify_text off) only counts and the meeting time: no titles anywhere. The push's
    body never names a meeting or a person's words beyond the to-do titles the lock screen already allows."""
    seen = set()
    key = lambda i: i.get('id') or ('title', i['title'])
    waiting_ids = {i['id'] for i in [*ready, *due, *overnight, *(top or [])] if i.get('id')}

    def counts(item):
        """Whether a listed line is one of the waiting to-dos: a promise is when its to-do waits too (covers)."""
        if item is None:
            return False
        ident = str(item.get('id') or '')
        return item.get('covers') in waiting_ids if ident.startswith('promise:') else True

    def once(items):
        fresh = [i for i in items if key(i) not in seen]
        seen.update(key(i) for i in fresh)
        return fresh
    ready = once(list(ready))
    # a promise whose to-do is already listed as ready: that line says it (the same to-do twice read as two things)
    promised = once([p for p in promised if not (p.get('covers') and p['covers'] in seen)])
    seen.update(p['covers'] for p in promised if p.get('covers'))  # a promise's own to-do: listed with the promise
    due, overnight, rest = once(list(due)), once(list(overnight)), once(list(top or []))
    todos = ready + due + overnight + rest
    total = len(todos) if total is None else total
    if not (meetings or todos or promised or total):
        return None
    per = per or 30
    # the three lines: (to-do or None for the first meeting, text)
    picks = [(i, i['title']) for i in ready + promised + due]
    if meetings:
        picks.append((None, clock(meetings[0]['at']) + ' ' + meetings[0]['title']))
    picks += [(i, i['title']) for i in overnight + rest]
    picks = picks[:3] if show_text else []
    listed = sum(1 for i, _ in picks if counts(i))
    more = max(0, total - listed)
    asking = set(asking)

    def about(count, shown):
        """Minutes for `count` waiting to-dos beside the ones in `shown`, without those that ask something (0: none)."""
        quick = count - len(asking - {str(i.get('covers') or i.get('id') or '') for i, _ in shown if i is not None})
        return clear_pace.minutes(quick, per) if quick > 0 else 0

    def waits(count, shown, beside):
        took = about(count, shown)
        if beside:
            return t('{} more can wait, about {} min to clear.', count, took) if took else t('{} more can wait.', count)
        return t('{} waiting, about {} min to clear.', count, took) if took else t('{} waiting.', count)
    first_at = clock(meetings[0]['at']) if meetings else ''
    # one ready for the owner's OK: the headline names it, so it says what waits ("1 ready for your OK" didn't)
    named = ready[0] if len(ready) == 1 and show_text else None
    head = headline(name, len(ready), sum(1 for r in ready if r.get('id') in set(replies)), len(due) + len(promised),
                    total, about(total, []), first_at, len(overnight), title=named['title'] if named else '')
    about_meeting = bool(first_at) and not (ready or due or promised or total >= PILE)  # headline's own order
    opening = t('{} meetings today, the first at {}.', len(meetings), first_at) if meetings else ''
    tail = waits(more, picks, bool(picks)) if more else ''

    def link(item):
        """Open: the to-do in the dashboard's list, in view and highlighted (#card=); one no longer there (done,
        snoozed, another scope) opens its chat instead (&or=chat, openCardLink). A promise opens the to-do made from it
        (covers), else its own page (#promise/<id>, as the Graph links it): every listed to-do or promise has one."""
        if not root or not item:
            return ''
        ident = str(item.get('id') or '')
        if ident.startswith('promise:'):
            ident = str(item.get('covers') or '')
            number = item['id'][len('promise:'):]
            if not re.fullmatch(r'[a-f0-9]{16}', ident) and re.fullmatch(r'\d+', number):
                return f" · [{t('Open')}]({root}#promise/{number})"
        return f" · [{t('Open')}]({root}#card={ident}&or=chat)" if re.fullmatch(r'[a-f0-9]{16}', ident) else ''
    # The headline's own list right under it, then how many more wait, then the day's meetings: a meeting line between
    # "3 due today" and its list read as if the list were the meeting's
    lines = [head, '']
    if picks:
        lines += ['• ' + text + link(item) for item, text in picks] + ['']
    if tail:
        lines += [tail, '']
    if opening and not about_meeting:  # a headline about the first meeting already says it
        lines += [opening, '']
    if root:
        lines.append(t('Open The Machine: {}', root))
    # The push: the same lines, without links; a meeting by its time only. Fewer lines when the phone has no room
    # for them all, and the count then says what was left out. The one the title names isn't said again under it.
    shown = [(item, clip(text, 40) if item is not None else t('First meeting at {}', first_at)) for item, text in picks
             if (item is not None or not about_meeting) and (named is None or item is not named)]
    for keep in range(len(shown), -1, -1):
        counted = sum(1 for i, _ in shown[:keep] if counts(i)) + bool(named)
        left = max(0, total - counted)
        said = shown[:keep] + ([(named, '')] if named else [])
        last = waits(left, said, bool(said)) if left else ''
        parts = [x for x in ([text for _, text in shown[:keep]] + [last] if keep else [last, opening]) if x] or [clip(named['title'], 40) if named else head]
        if len('\n'.join(parts)) <= APP_BODY:
            break
    body = '\n'.join(clip(x, APP_BODY) for x in parts)
    return {'push': {'title': head, 'body': body, 'url': (root or './') + DIGEST_VIEW, 'tag': 'digest'},
            'text': '\n'.join(lines).strip(), 'subject': head}


# -- the evening digest
def evening_time(evening_at, start, end):
    """When the evening digest goes ('HH:MM'): its own time (evening_at), else EVENING_BEFORE before the end of the
    hours (round-the-clock hours too: before their turn of the day). The dashboard shows the same default
    (settings-general.js, eveningAt) and the Machine sends it as evening_time (hours())."""
    if evening_at:
        return evening_at
    hour, minute = (int(x) for x in end.split(':'))
    left = (hour * 60 + minute - int(EVENING_BEFORE.total_seconds() // 60)) % (24 * 60)
    return '%02d:%02d' % divmod(left, 60)


def evening_due(local, at, start, end, work_day, sent):
    """The work day (a date) whose evening digest goes now, or None: from its time (`at`, evening_time) for at most
    DIGEST_LATE, within the hours, on a work day, once (sent(iso day): it went or is going). With hours that wrap past
    midnight a time before their start is on the next calendar day: that evening is the day they started."""
    if not at:
        return None
    now_hm = local.strftime('%H:%M')
    if not (start == end or (start <= now_hm < end if start < end else now_hm >= start or now_hm < end)):
        return None
    hour, minute = (int(x) for x in at.split(':'))
    for back in (0, 1):
        day = (local - dt.timedelta(days=back)).date()
        target = dt.datetime.combine(day + dt.timedelta(days=1 if end < start and at < start else 0), dt.time(hour, minute), local.tzinfo)
        if target <= local < target + DIGEST_LATE and work_day(day) and not sent(day.isoformat()):
            return day
    return None


def evening_key(day):
    """The evening digest's row in notify_digests (the morning's is the bare day)."""
    return 'evening:' + str(day)


def evening_headline(name, done, held):
    """The evening digest's first line (the email's subject, the push's title): a greeting and the day in a count, the
    to-dos done first, else the meetings held."""
    if done:
        return t('Evening {}, {} to-dos done today', name, done) if name else t('Good evening, {} to-dos done today', done)
    return t('Evening {}, {} meetings today', name, held) if name else t('Good evening, {} meetings today', held)


EVENING_AREAS = ('work', 'personal')  # the order of the evening digest's parts
EVENING_COPIED = 30  # at most this many done lines in a part's copy


def evening_compose(done, held, waiting, due, ahead, root='', show_text=True, clock=lambda iso: iso[11:16], name='',
                    next_day=None, tomorrow=True):
    """The evening digest: what the day brought and what is open for the next work day, short, in a Work part and a
    Personal part so each can be copied on its own. None when the day had nothing (no to-do done, no meeting held): then
    nothing is sent, whatever waits.

    done: the to-dos finished today [{id, title, area}], the ones that matter first; held: today's meetings with other
    people [{at, title, named, area}] (named: one worth naming, not a routine one); waiting: how many to-dos still need
    the owner (waiting_count); due: what is due on the next work day [{id?, title, area}] (to-dos and the owner's own
    promises); ahead: that day's first meetings worth naming [{at, title, area}]. area: 'work' or 'personal' (Work when
    left out). A part with nothing in it is left out. next_day: that day ("Mon, Nov 16") when it isn't tomorrow
    (tomorrow False: a Friday's evening speaks of Monday). At most EVENING_LISTED lines of each kind per part, the rest as
    a count. Without show_text (Careful, or notify_text off) only counts and the first meeting's time: no titles anywhere.
    Returns {push: {title, body, url, tag}, text, subject, sections: [{area, copy}]}: copy is that part as plain text
    (every to-do done, no links), to paste somewhere else."""
    if not done and not held:
        return None
    head = evening_headline(name, len(done), len(held))
    side = lambda x: 'personal' if x.get('area') == 'personal' else 'work'
    of = lambda items, area: [x for x in items if side(x) == area]

    def link(item):
        ident = str(item.get('id') or '')
        return f" · [{t('Open')}]({root}#card={ident}&or=chat)" if root and re.fullmatch(r'[a-f0-9]{16}', ident) else ''

    def part(area, short):
        """One part's lines: in the message (short: EVENING_LISTED, links) or its copy (every to-do done, plain)."""
        d, h, u, a = of(done, area), of(held, area), of(due, area), of(ahead, area)
        out = []
        if d or h:
            out.append(t('Done today'))
            if show_text:
                most = EVENING_LISTED if short else EVENING_COPIED
                out += ['• ' + clip(i['title'], 80) for i in d[:most]]
                if len(d) > most:
                    out.append(t('{} more done.', len(d) - most))
            elif d:
                out.append(t('{} to-dos done.', len(d)))
            named = [m['title'] for m in h if m.get('named')][:2 if short else EVENING_COPIED] if show_text else []
            names = ', '.join(clip(x, 40) for x in named)
            if h:  # every meeting counted: the ones not named (routine, or past the first few) as a count
                out.append(t('{} meetings.', len(h)) if not named else t('{} meetings: {}.', len(h), names) if len(named) == len(h)
                           else t('{} meetings: {} and {} more.', len(h), names, len(h) - len(named)))
        if u or a:
            out.append(t('Open for tomorrow') if tomorrow else t('Open for {}', next_day))
            if show_text:
                out += ['• ' + clock(m['at']) + ' ' + clip(m['title'], 60) for m in a[:2]]
                out += ['• ' + t('Due: {}', clip(i['title'], 80)) + (link(i) if short else '') for i in u[:EVENING_LISTED]]
                if len(u) > EVENING_LISTED:
                    out.append(t('{} more due.', len(u) - EVENING_LISTED))
            else:
                if a:
                    out.append(t('Tomorrow, first meeting at {}', clock(a[0]['at'])) + '.' if tomorrow
                               else t('{}, first meeting at {}', next_day, clock(a[0]['at'])) + '.')
                if u:
                    out.append(t('{} due tomorrow', len(u)) + '.' if tomorrow else t('{} due on {}', len(u), next_day) + '.')
        return out
    title = {'work': t('Work'), 'personal': t('Personal')}
    lines, sections = [head], []
    for area in EVENING_AREAS:
        body = part(area, True)
        if body:
            lines += ['', title[area], *body]
            sections.append({'area': area, 'copy': '\n'.join(part(area, False))})
    if waiting:
        lines += ['', t('{} to-dos still need you.', waiting)]
    if root:
        lines += ['', t('Open The Machine: {}', root)]
    # The push: what got done in a line, then the one thing to know for the next work day
    soon = []
    if ahead:
        at = clock(ahead[0]['at'])
        soon.append(t('Tomorrow, first meeting at {}', at) if tomorrow else t('{}, first meeting at {}', next_day, at))
    if due:
        soon.append(t('{} due tomorrow', len(due)) if tomorrow else t('{} due on {}', len(due), next_day))
    after = soon[:1] or ([t('{} to-dos still need you', waiting)] if waiting else [])
    room = APP_BODY - len(after[0]) - 1 if after else APP_BODY
    ordered = of(done, 'work') + of(done, 'personal')
    if show_text and done:
        # Two titles when they fit, else one, so the count of the rest is never clipped away
        options = []
        for n in (2, 1):
            first = ', '.join(clip(i['title'], 40) for i in ordered[:n])
            options.append(t('Done: {} and {} more', first, len(done) - n) if len(done) > n else t('Done: {}', first))
        summary = next((x for x in options if len(x) <= room), options[-1])
    elif done:
        summary = t('{} to-dos done.', len(done))
    else:
        summary = t('{} meetings.', len(held))
    body = '\n'.join([clip(summary, room), *after])
    return {'push': {'title': head, 'body': body, 'url': (root or './') + EVENING_VIEW, 'tag': 'evening'},
            'text': '\n'.join(lines).strip(), 'subject': head, 'sections': sections}


# -- email, through the control plane (hosted and paired Machines)
def mail(url, token, subject, text, opener=urllib.request.urlopen, delivery=None):
    """Hand one email (the digest, or what still waits) to the control plane for the account's own address. True when it took it."""
    if not url or not token:
        return False
    request = urllib.request.Request(url.rstrip('/') + '/notify-mail', method='POST',
                                     data=json.dumps({'subject': subject[:MAIL_SUBJECT], 'text': text[:MAIL_TEXT], **({'delivery': delivery} if delivery else {})}).encode(),
                                     headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    try:
        with opener(request, timeout=30) as response:
            if json.loads(response.read(10_000) or b'{}').get('sent'):
                return True
            LOG.warning('notify mail not taken')
    except urllib.error.HTTPError as error:  # the control plane said no: 401 not paired, 404 no address, 429 enough today, 502/503 its mailer
        LOG.warning('notify mail status=%d', error.code)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as error:
        LOG.warning('notify mail error=%s', type(error).__name__)
    return False


# -- the mobile app's push, through the control plane (hosted and paired Machines)
def app_devices(db):
    """[{id, platform, label, created_at}] of the owner's phones with the app, oldest first."""
    ensure(db)
    return [dict(r) for r in db.execute('SELECT id,platform,label,created_at FROM notify_app_devices ORDER BY created_at,id')]


def app_device_add(db, device_id, platform, label, at):
    ensure(db)
    db.execute('INSERT INTO notify_app_devices(id,platform,label,created_at) VALUES(?,?,?,?) '
               'ON CONFLICT(id) DO UPDATE SET platform=excluded.platform,label=excluded.label', (device_id, platform, label, at))


def app_device_remove(db, ids):
    ensure(db)
    db.executemany('DELETE FROM notify_app_devices WHERE id=?', [(i,) for i in ids])


def clip(text, limit=APP_LINE):
    """One plain line of at most `limit` characters, cut at a word with an ellipsis."""
    text = ' '.join(re.sub(r'[\x00-\x1f\x7f]', ' ', str(text or '')).split())
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    word = cut.rsplit(' ', 1)[0]
    return (word if len(word) >= limit // 2 else cut).rstrip(' ,;:.-') + '…'


def app_line_text(template, title, limit=APP_LINE):
    """A lead and the to-do's title ("Ready: {}") in at most `limit` characters: the title is what gets shorter."""
    room = limit - len(t(template, ''))
    return clip(t(template, clip(title, max(room, 10))), limit)


def app_line_save(db, tag, line, at=None, body=''):
    ensure(db)
    at = wall() if at is None else at
    db.execute('INSERT INTO notify_app_lines(tag,line,at,body) VALUES(?,?,?,?) '
               'ON CONFLICT(tag) DO UPDATE SET line=excluded.line,at=excluded.at,body=excluded.body',
               (tag, clip(line), at, clip(body, APP_BODY)))
    db.execute('DELETE FROM notify_app_lines WHERE at<? OR tag NOT IN (SELECT tag FROM notify_app_lines ORDER BY at DESC LIMIT ?)',
               (at - APP_LINE_DAYS * 86400, APP_LINES))


def app_lines(db):
    """The tags phones were woken for, still kept here: what app_clear_step looks at."""
    ensure(db)
    return [r[0] for r in db.execute('SELECT tag FROM notify_app_lines')]


def app_line_forget(db, tag):
    ensure(db)
    db.execute('DELETE FROM notify_app_lines WHERE tag=?', (tag,))


def app_line(db, tag):
    """The line for a wakeup's tag, or '' (unknown, too old, or a kind that has none)."""
    ensure(db)
    if not APP_ID.fullmatch(str(tag or '')):
        return ''
    row = db.execute('SELECT line FROM notify_app_lines WHERE tag=? AND at>=?', (tag, wall() - APP_LINE_DAYS * 86400)).fetchone()
    return row[0] if row else ''


def app_line_body(db, tag):
    """The body line kept with a wakeup's line (the morning's), or ''."""
    ensure(db)
    if not APP_ID.fullmatch(str(tag or '')):
        return ''
    row = db.execute('SELECT body FROM notify_app_lines WHERE tag=? AND at>=?', (tag, wall() - APP_LINE_DAYS * 86400)).fetchone()
    return row[0] if row else ''


def app_push(url, token, body, opener=None):
    """One request to the control plane's /app-push (register, unregister, list or wake). Returns its answer (a dict),
    {'missing': True} when it doesn't know the device (404), or None when it could not be reached or said no. Only the
    status or the error's type goes to the log, never the token."""
    if not url or not token:
        return None
    request = urllib.request.Request(url.rstrip('/') + '/app-push', method='POST', data=json.dumps(body).encode(),
                                     headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    try:
        with (opener or urllib.request.urlopen)(request, timeout=15) as response:
            answer = json.loads(response.read(100_000) or b'{}')
            return answer if isinstance(answer, dict) else None
    except urllib.error.HTTPError as error:
        LOG.warning('app push %s status=%d', body.get('action'), error.code)
        if error.code == 404:
            return {'missing': True}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, http.client.HTTPException) as error:
        LOG.warning('app push %s error=%s', body.get('action'), type(error).__name__)
    return None

"""Notifications: which kinds reach the owner on which channel, when they are left out, and the morning digest
(docs/help/notifications.md).

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
- Email for what is still unseen and still waiting EMAIL_AFTER later, bundled into one, at most once per EMAIL_EVERY
  (Slack: bundled every 15 minutes or hourly, only while inactive). Morning digest on work days.
- A teammate's handoff to an owner their Machine can't ping (no phone or Telegram): one email of its own for it, also
  EMAIL_AFTER later and only while still unseen and waiting (take_handoffs, handoff_mail).
- A batch buzzes once (assistant.deliver_one); nothing goes out outside work hours (Slack: notification schedule)."""
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

from i18n import t

LOG = logging.getLogger('personal-assistant')

KINDS = ('todo', 'result', 'reminder', 'digest')
CHANNELS = ('push', 'telegram', 'email')
# Email is on for every kind: many people never get push working, and it only goes for what is still unseen and
# waiting after EMAIL_AFTER, bundled. The digest is a push and an email; Telegram already has the weekly recap.
DEFAULTS = {'todo': {'push': True, 'telegram': True, 'email': True}, 'result': {'push': True, 'telegram': True, 'email': True},
            'reminder': {'push': True, 'telegram': True, 'email': True}, 'digest': {'push': True, 'telegram': False, 'email': True}}
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
        return 'reminder'
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
def digest_due(local, digest_at, start, end, work_day, sent_today):
    """Whether the digest goes now: a work day, at its time (or the start of hours when it is set earlier), within
    hours, at most DIGEST_LATE after, once a day."""
    if sent_today or not work_day(local):
        return False
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


def drop_pushes(db):
    """Outside work hours a held push is dropped: the email for what still waits takes over."""
    db.execute("DELETE FROM notify_queue WHERE channel='push'")


def drop_all(db):
    """After an import (machine/export/hold.py): what waited was for the old Machine. Returns how many."""
    return db.execute('DELETE FROM notify_queue').rowcount


def morning_line(meetings, waiting, total, show_text=True, clock=lambda iso: iso[11:16]):
    """The morning notification's body, two lines at most: how many to-dos wait and the first two of them, and when
    the first meeting starts ("3 to-dos: Reply to Sam, Pay the invoice, … · First meeting 10:00"). Without show_text
    only the count and the time. Nothing waiting: a calm line. Meeting titles and people's words never go in it."""
    first = clock(meetings[0]['at']) if meetings else ''
    if total and show_text and waiting:
        names = ', '.join(clip(w['title'], 40) for w in waiting[:2]) + (', …' if total > 2 else '')
        line = t('{} to-dos: {} · First meeting {}', total, names, first) if first else t('{} to-dos: {}', total, names)
    elif total:
        line = t('{} to-dos waiting · First meeting {}', total, first) if first else t('{} to-dos waiting', total)
    else:
        line = t('Nothing waiting · First meeting {}', first) if first else t('Nothing waiting. A calm start.')
    return clip(line, APP_BODY)


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


def compose(meetings, due, overnight, root='', show_text=True, clock=lambda iso: iso[11:16], waiting=None, total=None,
            top=None, ready=''):
    """The digest from its three parts: meetings [{at, title, guests}], due and overnight [{title}].
    Returns None when there is nothing to say, else {push: {title, body, url, tag}, text, subject}.
    Without show_text (Careful, or notify_text off) it carries counts only. waiting [{title}] (the first ones) and
    total (how many) are the to-dos waiting for the owner, for the push's body (morning_line); left out: due and
    overnight. top [{title}] are the first waiting to-dos in the dashboard's order (open_order): with total, a "Waiting
    for you" part, so a pile that waits still gets its digest when nothing is due or new. ready: the time to clear what
    waits, as the dashboard's Ready header says it ("4 ready · about 2 min", clear_pace.line), under that part.
    Nothing at all: None."""
    piled = total if top is not None and total else 0
    if not (meetings or due or overnight or piled):
        return None
    # in the owner's language (i18n.py); English when there is no entry
    counts = [t('{} meetings', len(meetings)) if meetings else '', t('{} due', len(due)) if due else '',
              t('{} new', len(overnight)) if overnight else '', t('{} waiting', piled) if piled else '']
    summary = ' · '.join(c for c in counts if c)
    lines = []
    if show_text:
        def part(head, items, line, count=None):
            if not items:
                return
            count = len(items) if count is None else max(count, len(items[:3]))
            lines.append(head)
            lines.extend('• ' + line(i) for i in items[:3])
            if count > 3:
                lines.append(t('• +{} more', count - 3))
            lines.append('')
        part(t('Today'), meetings, lambda m: clock(m['at']) + ' ' + m['title'])
        part(t('Due'), due, lambda d: d['title'])
        part(t('Overnight'), overnight, lambda o: o['title'])
        if piled:
            part(t('Waiting for you'), top, lambda w: w['title'], piled)
    else:
        lines += [summary, '']
    if piled and ready:
        lines += [ready, '']
    if root:
        lines.append(t('Open The Machine: {}', root))
    if waiting is None:
        waiting = due + [o for o in overnight if o not in due]
    body = morning_line(meetings, waiting, len(waiting) if total is None else total, show_text, clock)
    return {'push': {'title': t('Your morning'), 'body': body[:200], 'url': (root or './') + DIGEST_VIEW, 'tag': 'digest'},
            'text': '\n'.join(lines).strip(), 'subject': t('Your morning: {}', summary)}


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

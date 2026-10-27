"""Notifications: which kinds reach the owner on which channel, when they are left out, and the morning digest
(docs/help/notifications.md).

Kinds: a new to-do, a result or question (ready to approve, stuck, a sign-in, a Fleet question), a reminder (a snooze or
a wait coming back) and the morning digest. Channels: push (the dashboard app on a phone or computer, sent by this
Machine and encrypted for each device, push-send.mjs), Telegram, and email (the digest only, through the control
plane's mailer, so it is off until the owner turns it on).

Smart, like Slack: only kinds that need the owner notify; a batch buzzes once (assistant.deliver_one); nothing goes out
outside work hours; and while a dashboard is open and in focus no push goes to any device and Telegram arrives
silently (active)."""
from __future__ import annotations

import datetime as dt
import json
import threading
import time
import urllib.error
import urllib.request

from i18n import t

KINDS = ('todo', 'result', 'reminder', 'digest')
CHANNELS = ('push', 'telegram', 'email')
# Today's behavior for to-dos; the digest is new: a push only. Email is for the digest only.
DEFAULTS = {'todo': {'push': True, 'telegram': True}, 'result': {'push': True, 'telegram': True},
            'reminder': {'push': True, 'telegram': True}, 'digest': {'push': True, 'telegram': False, 'email': False}}
SCHEMA = 'CREATE TABLE IF NOT EXISTS notify_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL)'
DIGESTS = 'CREATE TABLE IF NOT EXISTS notify_digests(day TEXT PRIMARY KEY,status TEXT NOT NULL,created_at TEXT NOT NULL,channels TEXT)'
ACTIVE_FOR = 120  # seconds: a dashboard in focus this recently counts as the owner being there
DIGEST_LATE = dt.timedelta(hours=3)  # a digest not sent by then (the Machine was off) waits for the next day
MAIL_SUBJECT, MAIL_TEXT = 120, 4000


def ensure(db):
    db.execute(SCHEMA)
    db.execute(DIGESTS)


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


# -- active: a dashboard in focus (kept in memory; a restart forgets it, which only means a push may go out)
_active = {'at': 0.0}
_lock = threading.Lock()


def mark_active(clock=time.monotonic):
    with _lock:
        _active['at'] = clock()


def active(clock=time.monotonic):
    with _lock:
        return bool(_active['at']) and clock() - _active['at'] < ACTIVE_FOR


def reset_active():
    with _lock:
        _active['at'] = 0.0


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


def compose(meetings, due, overnight, root='', show_text=True, clock=lambda iso: iso[11:16]):
    """The digest from its three parts: meetings [{at, title, guests}], due and overnight [{title}].
    Returns None when there is nothing to say, else {push: {title, body, url, tag}, text, subject}.
    Without show_text (Careful, or notify_text off) it carries counts only."""
    if not (meetings or due or overnight):
        return None
    # in the owner's language (i18n.py); English when there is no entry
    counts = [t('{} meetings', len(meetings)) if meetings else '', t('{} due', len(due)) if due else '',
              t('{} new', len(overnight)) if overnight else '']
    summary = ' · '.join(c for c in counts if c)
    lines = []
    if show_text:
        def part(head, items, line):
            if not items:
                return
            lines.append(head)
            lines.extend('• ' + line(i) for i in items[:3])
            if len(items) > 3:
                lines.append(t('• +{} more', len(items) - 3))
            lines.append('')
        part(t('Today'), meetings, lambda m: clock(m['at']) + ' ' + m['title'])
        part(t('Due'), due, lambda d: d['title'])
        part(t('Overnight'), overnight, lambda o: o['title'])
    else:
        lines += [summary, '']
    if root:
        lines.append(t('Open The Machine: {}', root))
    body = summary
    if show_text and meetings:
        body = t('First: {}. {}', clock(meetings[0]['at']) + ' ' + meetings[0]['title'], summary)
    return {'push': {'title': t('Your morning'), 'body': body[:200], 'url': root or '.', 'tag': 'digest'},
            'text': '\n'.join(lines).strip(), 'subject': t('Your morning: {}', summary)}


# -- email, through the control plane (hosted and paired Machines)
def mail(url, token, subject, text, opener=urllib.request.urlopen):
    """Hand one digest email to the control plane for the account's own address. True when it took it."""
    if not url or not token:
        return False
    request = urllib.request.Request(url.rstrip('/') + '/notify-mail', method='POST',
                                     data=json.dumps({'subject': subject[:MAIL_SUBJECT], 'text': text[:MAIL_TEXT]}).encode(),
                                     headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    try:
        with opener(request, timeout=30) as response:
            return bool(json.loads(response.read(10_000) or b'{}').get('sent'))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return False

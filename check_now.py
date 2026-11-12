"""Check now (docs/help/cards.md#check-now): every source is read and a review of what came in starts right away,
outside the usual rhythm. Usually each source is read every few minutes (poll_seconds) and a review of what came in
starts once enough new messages wait or the oldest one waited 15 minutes (review_worker min_signals, max_wait_minutes). Nothing gates either
by the time of day: there are no quiet hours for reading, and a hosted Machine never pauses while it is paid for.

From the To-dos page head (the dashboard and the phone app, which loads the same dashboard) and from chat, where the
agent runs `assistant check`. One check at a time: a press while one runs, or within REST_SECONDS after it ended,
joins it instead of starting another, so repeated taps never stack reads or reviews.

A check: 'reading' while each source that waits for its next read reads now (the collector's own read, woken early:
its pacing, locks and error handling stay as they are), then 'reviewing' while the review it asked for runs, then done
with how many new to-dos it brought. Slow sources (SLOW_SERVICES, or read every SLOW_POLL seconds or less often) and
one waiting out an error keep their own pace. Kept in memory only: a restart forgets a check, which then just ends."""
from __future__ import annotations

import collections
import datetime as dt
import email.utils
import json
import threading
import time

import abilities
import graph
from machine.sources.android import android_app_shown
from machine.sources.gmail import machine_notice
from machine.sources.slack import slack_named, slack_plain

REST_SECONDS = 60             # after a check ends, a new press within this long shows it instead of starting another
READ_WAIT = 180               # the sources' reads, at most this long
REVIEW_WAIT = 30 * 60         # the review it asked for, at most this long
REVIEW_START_WAIT = 90        # a review asked for that doesn't start within this long (nothing to review after all)
SLOW_POLL = 600
SLOW_SERVICES = ('linkedin', 'x', 'salesflare')  # read in the Machine's browser, a paid API, a CRM's long rounds
ACTIVE = ('starting', 'running', 'recovering')


def fast(config, account):
    """A source Check now reads: it brings in signals and is read every few minutes by nature."""
    poll = account.get('poll_seconds', config.get('poll_seconds', 300))
    return abilities.signals_on(account) and account.get('service') not in SLOW_SERVICES and poll < SLOW_POLL


def reviews(db, queue, min_signals):
    """The status the owner cares about: when messages were last reviewed into to-dos and when the next review is due.
    reviewing and reading: a review runs, or a mailbox's first import comes in, whoever started it (the first look, the
    usual rhythm or a check), so Check now shows busy then too. `queue` is the service's review_queue (how many wait and when the next review starts: at min_signals waiting, or
    once the oldest waited max_wait_minutes); soon: the batch is (nearly) full, so it starts within minutes."""
    row = db.execute("SELECT max(finished_at) FROM review_runs WHERE status='ok'").fetchone()
    waiting = (queue or {}).get('waiting') or 0
    return {'reviewed': row[0] if row else None, 'reviewing': reviewing(db), 'waiting': waiting,
            'reading': (queue or {}).get('why') == 'mail',  # a mailbox's first import still coming in
            'next_review': (queue or {}).get('starts_at') if waiting else None,
            'soon': bool(waiting) and waiting >= min_signals * 3 / 4}


MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message')
# What the line counts each new message as: email, chat, notification, or else an update (a calendar change, a comment
# on a doc, a payment, meeting notes)
EMAIL_KINDS = (*MAIL_KINDS, 'salesflare.email', 'fleet.email', 'imap.message', 'email.message')
CHAT_KINDS = ('slack.message', 'whatsapp.message', 'telegram.message', 'teams.message', 'linkedin.message', 'x.dm', 'x.message',
              'intercom.conversation', 'sms.message', 'signal.message', 'fleet.message')
OWN_KINDS = ('machine.', 'gateway.')  # The Machine's own logs and alerts: nothing that came in
MAIL_CHECK_HOURS = 12        # the To-dos page says what the last check of new messages found for this long after it
MAIL_CHECK_THREADS = 120     # its list sends every thread: a review reads at most RUN_SIGNAL_BUDGET (120) messages
SAME_WHY = 3                # one reason given for this many threads of one check is a label, not a reason


def source_group(kind):
    """'email', 'chat', 'notification' or 'update': how the line counts a message of this kind."""
    if kind in EMAIL_KINDS:
        return 'email'
    if kind in CHAT_KINDS:
        return 'chat'
    return 'notification' if kind.endswith('.notification') else 'update'


def mail_check(db, current=None, own=()):
    """What the last check that saw new messages found, from every source it read (email, chats, phone notifications,
    the rest), for the line on To-dos (docs/help/cards.md#last-check): when it ran, how many new messages of each kind
    (`counts`, `read` in all), how many new to-dos it made and how many of those are held until later, and one row per
    thread or chat: its kind and newest message (to open it) and when, who (by name: an app's name, never its package; a
    Slack member's name, never their id), the subject or the message's first words in plain text, how many new messages
    it holds when more than one (`n`: the rows add up to `read`), and either its new to-do or why it needed nothing (the review's finish_analysis no_todo, as stored: no model call here).
    Quality or nothing: a reason under three words, or the same one for SAME_WHY threads, is left out. The owner's own
    chat messages (from_me) and The Machine's own logs (OWN_KINDS) aren't new. `own`: the owner's addresses, so a
    thread shows who wrote to them rather than their own reply. None without such a check in the last MAIL_CHECK_HOURS."""
    current = current or dt.datetime.now(dt.timezone.utc)
    since = (current - dt.timedelta(hours=MAIL_CHECK_HOURS)).isoformat()
    own = {str(a).lower() for a in own if a}
    for review in db.execute("SELECT started_at,finished_at,items FROM analyses WHERE status='complete' AND finished_at>=? "
                             'ORDER BY finished_at DESC LIMIT 12', (since,)).fetchall():
        # new messages only: a later version of one already read (its labels or read state changed) is not new mail
        batch = [i for i in json.loads(review['items'] or '[]') if isinstance(i, dict) and not i.get('excluded')]
        items = {i['id']: i for i in batch if i.get('version', 1) == 1}
        if not items:
            continue
        found = db.execute('SELECT id,account_id,kind,occurred_at,title,body,metadata FROM events WHERE deleted=0 AND id IN '
                           '(SELECT value FROM json_each(?)) ORDER BY occurred_at', (json.dumps(sorted(items)),)).fetchall()
        # The Machine's own notices and logs are never news (nor read: machine_notice, OWN_KINDS). The owner's own sent
        # mail and chat messages are read (the context of the threads they answer, the promises they make) but are
        # nothing new for them: a thread only they wrote in is left out, and only messages to them count
        mail = [r for r in found if not str(r['kind']).startswith(OWN_KINDS) and not machine_notice(r['kind'], _meta(r['metadata']))]
        if any(not _from_owner(_meta(r['metadata']), own) for r in mail):
            # a Slack member by name, never by id (slack_named): the sender, a DM's other person, a mention
            return _mail_view(db, review, items, {i['id'] for i in batch}, slack_named(db, [dict(r) for r in mail]), current, own)
    return None


def _from_owner(meta, own):
    return bool({'SENT', 'DRAFT'} & set(meta.get('labels') or ())) or meta.get('from_me') is True or _sender(meta.get('from'))[1] in own


def _thread_key(account_id, kind, meta, event_id):
    """One row per email thread, chat or channel; a phone notification or an update is a row of its own."""
    group = source_group(kind)
    keyed = (meta.get('thread_id') or meta.get('conversation_id')) if group == 'email' else \
        (meta.get('conversation_id') or meta.get('chat_id') or meta.get('channel_id') or meta.get('thread_id')) if group == 'chat' else None
    return (account_id, group, str(keyed or f'event:{event_id}'))


def _snippet(text, size=160):
    return ' '.join(str(text or '').split())[:size]


def _meta(value):
    if isinstance(value, dict):
        return value
    try:
        found = json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


def _sender(value):
    name, address = email.utils.parseaddr(str(value or ''))
    return (name.strip().strip('"') or address).strip(), address.lower()


def _slack_dm(row, meta):
    return row['kind'] == 'slack.message' and (meta.get('conversation_type') == 'im' or str(meta.get('channel_name') or '').startswith('DM'))


def _no_id(who):
    """A name to show, or '' when all there is is a Slack member id or a stand-in for one: never shown."""
    return '' if graph.SLACK_MEMBER.search(who) or graph.SOMEONE_ON_SLACK in who else who


def _who_and_what(row, meta):
    """A message that isn't email: who it's from and its first words (a chat), the app by name and what it said (a
    phone notification), or who and its title (an update). Slack's link and mention markup reads as plain words, and a
    Slack member is named (slack_named ran) or left out, never shown by id: a DM with no name is '' (a "Slack DM")."""
    group, title, body = source_group(row['kind']), _snippet(row['title'], 1000), _snippet(row['body'])
    if row['kind'] == 'slack.message':
        title, body = _snippet(slack_plain(row['title']), 1000), _snippet(slack_plain(row['body']))
    if group == 'notification':
        app = android_app_shown(meta['package_name'], meta.get('app_name')) if meta.get('package_name') else str(meta.get('app_name') or '')
        # the phone's feed puts the same words in both: say them once
        said = body if title and body.startswith(title[:40]) else f'{title}: {body}' if title and body else title or body
        return app, _snippet(said)
    who = str(meta.get('from') or meta.get('sender_display') or meta.get('sender_name') or meta.get('user_name') or '')
    who = _no_id(_sender(who)[0] if '<' in who or '@' in who else ' '.join(who.split()))  # "Sam <U123>", an address, or a name as is
    if group == 'chat':
        if not who and not _slack_dm(row, meta):
            place = str(meta.get('chat_name') or '') or (('#' + str(meta['channel_name'])) if meta.get('channel_name') else '') or title
            who = _no_id(' '.join(place.split()))
        return who, body or _snippet(title)
    return who, _snippet(title) or body


ECHO_APPS = {  # a phone app whose messages also come in directly: its notification about one is that message again
    'com.linkedin.android': ('linkedin.',), 'com.whatsapp': ('whatsapp.',), 'com.whatsapp.w4b': ('whatsapp.',),
    'org.telegram.messenger': ('telegram.',), 'com.Slack': ('slack.',), 'com.microsoft.teams': ('teams.',),
    'com.google.android.gm': EMAIL_KINDS, 'com.microsoft.office.outlook': EMAIL_KINDS, 'com.twitter.android': ('x.',),
    'org.thoughtcrime.securesms': ('signal.',), 'com.intercom.android': ('intercom.',),
}


def _plain(text):
    return ' '.join(str(text or '').casefold().split())


def _echo(note, threads):
    """A phone notification that only repeats a message this check also read directly (LinkedIn's "1 new message:
    Sam - Hi there" next to Sam's LinkedIn message): its words hold the start of that message, and its sender's name
    when the message is short."""
    kinds = ECHO_APPS.get(note.get('package'))
    if not kinds or 'todo' in note:
        return False
    said = note['said']
    for thread in threads:
        if thread is note or thread['source'] == 'notification' or not str(thread['kind']).startswith(kinds):
            continue
        name = _plain(thread['from'])
        if any(head in said and (len(head) >= 12 or (name and name in said)) for head in thread['heads']):
            return True
    return False


def _mail_view(db, review, items, batch, mail, current, own):
    threads = {}
    for row in mail:
        meta = _meta(row['metadata'])
        group, mine = source_group(row['kind']), _from_owner(meta, own)
        thread = threads.setdefault(_thread_key(row['account_id'], row['kind'], meta, row['id']),
                                    {'ids': [], 'from': '', 'subject': '', 'why': None, 'later': False, 'source': group, 'in': 0, 'heads': set()})
        thread['ids'].append(row['id'])
        thread['in'] += not mine
        thread['last'] = row['occurred_at']  # rows come oldest first
        if not mine or 'open' not in thread:
            thread['open'], thread['kind'] = row['id'], row['kind']  # its newest message to the owner opens
        if group == 'email':
            name, address = _sender(meta.get('from'))
            if name and (address not in own or not thread['from']):
                thread['from'] = name
            thread['subject'] = (row['title'] or '').strip() or thread['subject']
            words = [thread['subject'], row['body']]
        else:
            who, what = _who_and_what(row, meta)
            if not mine or not thread['from']:
                thread['from'], thread['subject'] = who or thread['from'], what or thread['subject']
            words = [what]
            if group == 'notification':
                thread['package'], thread['said'] = meta.get('package_name'), _plain(f"{row['title'] or ''} {row['body'] or ''}")
            if _slack_dm(row, meta):
                thread['dm'] = True
        if not mine:
            thread['heads'].update(h for h in (_plain(w)[:24] for w in words) if len(h) >= 4)
        item = items[row['id']]
        if item.get('no_todo'):
            thread['why'] = item['no_todo']
        thread['later'] = thread['later'] or bool(item.get('deferred'))
    # The to-dos this check made: created while it ran, from a message it read or one in the same thread
    end = (dt.datetime.fromisoformat(review['finished_at']) + dt.timedelta(minutes=1)).isoformat()
    made = db.execute('SELECT id,title,event_ids,deliver_after FROM suggestions WHERE created_at>=? AND created_at<=? ORDER BY created_at',
                      (review['started_at'], end)).fetchall()
    cards = [(card, {int(i) for i in json.loads(card['event_ids'] or '[]') if str(i).isdigit()}) for card in made]
    linked = {i for _, ids in cards for i in ids}
    keys = {r['id']: _thread_key(r['account_id'], r['kind'], _meta(r['metadata']), r['id'])
            for r in db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id IN (SELECT value FROM json_each(?))', (json.dumps(sorted(linked)),))}
    now_iso, todos, held = current.isoformat(), 0, []
    for card, ids in cards:
        hit = [threads[keys[i]] for i in ids if keys.get(i) in threads]
        if not hit and not ids & batch:
            continue  # not from this check (the owner's own, one from chat with the Machine)
        todos += 1
        later = card['deliver_after'] if card['deliver_after'] and card['deliver_after'] > now_iso else None
        if later:
            held.append(later)
        for thread in hit[:1]:
            thread.setdefault('todo', card['title'])
            thread.setdefault('held_until', later)
    # only the owner wrote in it: no new mail for them, unless their own mail made a to-do (a promise they made)
    threads = {key: thread for key, thread in threads.items() if thread['in'] or 'todo' in thread}
    # a phone notification that repeats a message read directly is that message: one row, counted once
    threads = {key: thread for key, thread in threads.items() if not _echo(thread, list(threads.values()))}
    said =collections.Counter(' '.join(t['why'].casefold().split()).rstrip('.') for t in threads.values() if t['why'])
    rows = []
    # to-dos first, then the newest thread first
    for thread in sorted(sorted(threads.values(), key=lambda t: t['last'], reverse=True), key=lambda t: 'todo' in t, reverse=True):
        why = thread['why']
        if why and (len(why.split()) < 3 or said[' '.join(why.casefold().split()).rstrip('.')] >= SAME_WHY):
            why = None
        row = {'from': thread['from'], 'subject': thread['subject'][:160], 'source': thread['source'], 'kind': thread['kind'], 'event': thread['open'],
               'at': thread['last']}
        if thread['in'] > 1:
            row['n'] = thread['in']  # its new messages: the rows add up to the line's total
        if thread.get('dm') and not thread['from']:
            row['dm'] = True  # a Slack DM whose other person has no name yet: "Slack DM", never their id
        if 'todo' in thread:
            row['todo'] = thread['todo']
            if thread.get('held_until'):
                row['held_until'] = thread['held_until']
        elif thread['later']:
            row['later'] = True
        elif why:
            row['why'] = why
        rows.append(row)
    counts = collections.Counter()
    for thread in threads.values():
        counts[thread['source']] += thread['in']
    return {'at': review['finished_at'], 'read': sum(counts.values()), 'counts': {k: n for k, n in counts.items() if n}, 'todos': todos, 'held': len(held),
            'held_until': min(held) if held else None, 'threads': rows[:MAIL_CHECK_THREADS], 'more': max(0, len(rows) - MAIL_CHECK_THREADS)}


def epoch(text):
    return dt.datetime.fromisoformat(text).timestamp()


def iso(seconds):
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).isoformat(timespec='seconds') if seconds else None


def waiting(db):
    """New messages a review still has to look at."""
    return db.execute('SELECT count(*) FROM events WHERE analyzed_version<version').fetchone()[0]


def reviewing(db):
    return bool(db.execute('SELECT 1 FROM review_runs WHERE status IN (%s) LIMIT 1' % ','.join('?' * len(ACTIVE)), ACTIVE).fetchone())


def new_todos(db, since):
    return db.execute('SELECT count(*) FROM suggestions WHERE created_at>=?', (iso(since),)).fetchone()[0]


class Check:
    """The one check, in memory: started, read (the sources' reads ended), ended, and how many new to-dos it brought."""

    def __init__(self):
        self.lock = threading.Lock()
        self.started = self.read = self.ended = 0.0
        self.found = None

    def start(self, now_s):
        """True when a new check starts; False when one runs, or one ended under REST_SECONDS ago."""
        with self.lock:
            if self.phase() or (self.ended and now_s - self.ended < REST_SECONDS):
                return False
            self.started, self.read, self.ended, self.found = now_s, 0.0, 0.0, None
            return True

    def phase(self):
        if not self.started or self.ended:
            return None
        return 'reviewing' if self.read else 'reading'

    def view(self, status):
        """For the dashboard (state.check): phase ('reading', 'reviewing' or None), the last check's start, end and
        new to-dos, and `status` (reviews(): the last review, the next one and how many messages wait)."""
        return {**status, 'phase': self.phase(), 'started': iso(self.started), 'ended': iso(self.ended), 'found': self.found,
                'rest_until': iso(self.ended + REST_SECONDS) if self.ended else None}


def run(check, app):
    """The check itself, on its own thread: wake the resting sources, wait for their reads, ask for a review, wait for
    it, end. `app` is the service (assistant.App): its collectors, review worker, store and stop."""
    try:
        started = check.started
        woken = app.wake_collectors(lambda account: fast(app.config, account))
        deadline = time.monotonic() + READ_WAIT
        while woken and not app.stop.is_set() and time.monotonic() < deadline:
            if all(app.collector_reads.get(account_id, 0) >= started for account_id in woken):
                break
            app.stop.wait(1)
        check.read = time.time()
        if not (app.config.get('review_worker') or {}).get('enabled'):
            return
        with app.store.connect() as db:
            new = waiting(db)
        if not new:
            return
        asked = time.time()
        app.review_asked, app.review_paused = asked, None
        deadline = time.monotonic() + REVIEW_WAIT
        while not app.stop.is_set() and time.monotonic() < deadline:
            app.stop.wait(2)
            if getattr(app, 'review_paused', None):
                break  # a usage limit holds it (the dashboard's banner says so)
            with app.store.connect() as db:
                running = reviewing(db)
            pending = getattr(app, 'review_asked', 0) == asked
            if not running and not pending:
                break  # it ran and ended
            if pending and not running and time.time() - asked > REVIEW_START_WAIT:
                break  # nothing it could review after all
    finally:
        try:
            with app.store.connect() as db:
                check.found = new_todos(db, check.started)
        except Exception:  # noqa: BLE001 - the check still ends
            check.found = None
        check.ended = time.time()

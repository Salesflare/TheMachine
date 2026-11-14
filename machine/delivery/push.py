"""Pushes to the phone app and the browser: push_notify and push_send, the node they go through (push_node), the app's
lines and buttons (app_notice, app_wake), reminders and setup hints, and what the to-do counts say. Moved out of
assistant.py as is."""
import datetime as dt
import functools
import json
import re
import subprocess
import time
import urllib.parse

import agent_jobs
import fleet
import i18n
from machine.cards import NOT_FOR_OWNER_SQL, plain
from machine.config import LOG, ROOT, WORKSPACE
from machine.model_usage import node_bin, node_env, telegram_on
from machine.sources.connectors import HOSTED_SIGNINS
from machine.sources.mail_senders import HINT_MAILS, HINT_SOURCES, mails_from, sender_domain_in  # noqa: F401  (setup hints; assistant.py, tests)
from machine.text import encoded, first_sentence
import next_actions
import notify
import qr
import security_levels
from sources import credential
import still_needed
from timeutil import local_tz, now
from machine import todo_states


@functools.lru_cache(maxsize=4)
def phone_qr(link):
    return tuple(qr.encode(link))


# A sentence the link ended ("The draft is at <path>."): without the link it points at nothing, so it goes too.
DANGLING_POINTER = re.compile(r'(^|[.!?]\s+)[^.!?]*\b(?:at|in|to|under|into|on|see|here)\s*[.:]?\s*$', re.I)


def strip_result_links(text):
    """Drop local result-file links (the card gets one Read result link instead) and the gaps they leave.

    A named link keeps its words ("Your [plan](memory/assistant/x.md) is ready" reads "Your plan is ready"); a line
    of nothing but result links (and separators or a short label) goes, since plain text can't open them."""
    root = '(?:' + re.escape(str(WORKSPACE)) + r'/)?memory/assistant/'
    named = re.compile(r'\[([^\]\n]*)\]\(' + root + r'[^\s\)]+\)')
    bare = re.compile(root + r'[^\s<>"\)]+')
    def strip(line, words):
        was = line
        line = bare.sub('', named.sub(lambda m: m[1].strip() if words else '', line)).replace('  ', ' ').rstrip()
        # "No settings were changed. [](memory/assistant/x.md)." leaves its period behind the one before: drop it
        return re.sub(r'([.!?])\s+[.!?](?=\s|$)', r'\1', line) if line != was.rstrip() else line
    # A line left with only separators or a dangling label ("Draft:") carried nothing but the link.
    empty = lambda s: re.fullmatch(r'[\s·•|,;:()\-–—]*', s) or re.fullmatch(r'\s*[-*•]?\s*[^\s:]+(?: [^\s:]+){0,3}:', s)
    lines=[]
    for line in text.split('\n'):
        linked = named.search(line) or bare.search(line)
        if linked and empty(strip(line, False)):
            continue
        kept = strip(line, True)
        if bare.search(named.sub('', line)):  # a sentence that pointed at a bare path points at nothing now
            kept = DANGLING_POINTER.sub(r'\1', kept).rstrip()
        if linked and empty(kept):
            continue
        lines.append(kept)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


def push_node(config, request, timeout=30):
    """push-send.mjs signs and encrypts Web Push with Node's built-in crypto (Python has no EC here)."""
    result = subprocess.run([node_bin(config), str(ROOT / 'push-send.mjs')], env=node_env(config),
                            input=encoded(request), capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError('push sender failed')
    return json.loads(result.stdout)


def push_key(config):
    return push_node(config, {'action': 'key'})['key']


def result_lead(db, row):
    """How a prepared to-do's notification starts, by what the to-do is: 'Ready' only when The Machine prepared
    something for the owner to review (a draft, a handoff, a result). A to-do that tracks what someone else promised
    the owner ("Waiting on Sam: the quote") or waits on someone else says so in its title, and one back from a snooze
    is a reminder: no "Ready" in front of those. Returns 'Ready', 'Reminder' or None (the title alone)."""
    try:
        state = (json.loads(row.get('outcome') or '{}') or {}).get('state')
    except (TypeError, ValueError, AttributeError):
        state = None
    if state == 'snoozed':
        return 'Reminder'
    if state in ('waiting', 'already_done'):
        return None
    key = str(row.get('dedupe_key') or '')
    if key.startswith('promise:') and key[8:].isdigit() and db.execute(
            "SELECT 1 FROM promises WHERE id=? AND direction='theirs'", (int(key[8:]),)).fetchone():
        return None
    return 'Ready'


def reply_waits(row):
    """A prepared to-do whose next step is a message in an existing conversation (an email in its thread, a chat, a
    reply to a post), drafted and ready to send: someone waits on the owner's reply."""
    if row.get('status') != 'prepared':
        return False
    try:
        steps = next_actions.visible_actions(row.get('next_action'))
    except (TypeError, ValueError, AttributeError):
        return False
    return any(s.get('kind') in next_actions.SEND_KINDS and s.get('kind') != 'email_demo'
               and (s.get('kind') != 'email' or s.get('in_reply_to') or s.get('thread_id')) for s in steps)


NUDGE_KINDS = ('email', 'linkedin', 'slack', 'x', 'whatsapp', 'telegram', 'signal', 'intercom', 'handoff')


def nudge_wait(db, suggestion_id, job_id, outcome, actions):
    """A "Waiting on Sam" to-do (what someone else promised the owner came due) whose run, prepared ahead, only drafted a
    nudge or a handoff: the next step is still theirs, so it waits under Waiting on others with the nudge ready there,
    not in Ready. Asked for by the owner, with a question for them, or with any other step, it stays needs_you."""
    needs = str(outcome.get('needs') or '').strip()
    if not actions or needs.endswith('?') or any(a.get('kind') not in NUDGE_KINDS for a in actions):
        return outcome
    row = db.execute('SELECT dedupe_key FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    key = str(row['dedupe_key'] if row else '')
    if not (key.startswith('promise:') and key[8:].isdigit()):
        return outcome
    promise = db.execute("SELECT who FROM promises WHERE id=? AND direction='theirs' AND NOT together", (int(key[8:]),)).fetchone()
    asked = db.execute('SELECT d.choice FROM preparations p JOIN decisions d ON d.id=p.decision_id WHERE p.suggestion_id=? AND p.job_id=?',
                       (suggestion_id, job_id)).fetchone() if job_id else None
    if not promise or not asked or asked['choice'] != 'prepare_ahead':
        return outcome
    return {'state': 'waiting', 'waiting_on': ' '.join(str(promise['who']).split())[:200]}


def first_result(row):
    """A to-do whose first notification is its result: prepared (or stuck) before it was ever delivered (deliver_one
    sets _first: no earlier message). It reads as a result ("Ready: ..."), never as a reminder of something unseen."""
    return bool(row.get('_first') and (row.get('status') == 'prepared' or row.get('preparation_status') == 'blocked'))


def shown_as_reminder(row):
    """A delivery says "Reminder:" only when an earlier notification for that to-do went out: its reminder flag also
    lets a prepared to-do through deliver_one the first time (Store.prepare), and that one is no reminder."""
    return bool(row.get('reminder') and not row.get('_first'))


def push_notify(store, config, row, sender=None):
    """Phone notification for the installed dashboard app, next to the Telegram one
    . Best effort: never changes the Telegram delivery state."""
    subscriptions, phones = push_reach(store, config)
    if not subscriptions and not phones:
        return []
    root = 'https://' + config['dashboard_host'] + config.get('dashboard_path', '/') if config.get('dashboard_host') else ''
    try:
        ids = json.loads(row.get('account_ids') or '[]')
    except (TypeError, ValueError):
        ids = []
    work = any(a['id'] in ids and str(a.get('boundary') or '').startswith('work:') for a in config.get('accounts', []))
    with store.connect() as db:
        text = security_levels.notify_text(db, work)  # Careful: no card text on a lock screen
    if row.get('_result_notice') or first_result(row):
        ready = row['status'] == 'prepared'
        signin = not ready and (row.get('preparation_browser') or {}).get('signin_url')
        # A run the service stopped (a timeout, two failures) asks nothing: Stuck, as on the card
        lead = row.get('_lead', 'Ready') if ready else 'Needs you to sign in' if signin else 'Stuck' if row.get('preparation_error') else 'Needs your help'
        # one key per lead, so the dashboard never reads a bare "{}: {}" into other text; no lead: the title alone
        payload = {'title': (i18n.t(lead + ': {}', row['title']) if lead else row['title']) if text else i18n.t(lead or 'To-do'),
                   'body': plain(strip_result_links(row['body']) if ready else row.get('preparation_reason') or '') if text else '',
                   'url': signin or notify.todo_link(root, row['id'])}  # the to-do in the list, not its chat
        # The mobile app's own line, short (it asks this Machine for it: notify.app_line), and ready or needs-you
        payload['_line'] = (notify.app_line_text(lead + ': {}', row['title']) if lead else notify.clip(row['title'], notify.APP_LINE)) if text else i18n.t(lead or 'To-do')
        payload['_state'] = 'ready' if ready else 'needs'
    else:
        reminder = shown_as_reminder(row)
        payload = {'title': (i18n.t('Reminder: {}', row['title']) if reminder else row['title']) if text else i18n.t('Reminder') if reminder else i18n.t('New to-do'),
                   'body': plain(row['body']) if text else '', 'url': notify.todo_link(root, row['id'])}
        payload['_line'] = (notify.app_line_text('Reminder: {}' if reminder else 'New to-do: {}', row['title']) if text
                            else i18n.t('Reminder') if reminder else i18n.t('New to-do'))
        if notify.kind_of(row) == 'result':  # a reminder for a prepared or stuck to-do: ready or needs-you, as a result says
            payload['_state'] = 'ready' if row.get('status') == 'prepared' else 'needs'
    payload['tag'] = row['id']  # a newer notification for the same card replaces the older one
    blocked = bool(row.get('_result_notice')) and row['status'] != 'prepared' or row.get('preparation_status') == 'blocked'
    payload['actions'] = quick_web(quick_kind(row, notify.kind_of(row), blocked, (row.get('preparation_browser') or {}).get('signin_url')))
    if row.get('_silent'):
        payload['silent'] = True  # later cards of a batch still reach the phone, without a second buzz
    return push_send(store, config, subscriptions, payload, 'suggestion=' + row['id'], sender, kind=notify.kind_of(row))


REPORT_HOURS = 24  # a to-do its confirmed step closed stays under Just done this long, unless the owner saw it first


def reported(row):
    """A done to-do its confirmed final step closed by itself (Store.prepare: done_report) that the owner hasn't seen yet."""
    at = (row or {}).get('done_report')
    if not at or row.get('status') != 'completed':
        return False
    try:
        return dt.datetime.fromisoformat(at) > dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=REPORT_HOURS)
    except (TypeError, ValueError):
        return False


def report_done(store, config, suggestion_id, sender=None):
    """The report the owner was promised when they confirmed a final step ("On it. I'll report back."): a result
    notification, "Done: <title>" with what happened, on every device and phone, replacing that to-do's earlier one.
    Held while a dashboard is in use, where Just done shows it (push_send). The phone app asks for its line (app_notice)."""
    with store.connect() as db:
        row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        row = dict(row) if row else None
        if not reported(row):
            return []
        try:
            ids = json.loads(row.get('account_ids') or '[]')
        except (TypeError, ValueError):
            ids = []
        work = any(a['id'] in ids and str(a.get('boundary') or '').startswith('work:') for a in config.get('accounts', []))
        text = security_levels.notify_text(db, work)  # Careful: no card text on a lock screen
    subscriptions, phones = push_reach(store, config)
    if not subscriptions and not phones:
        return []
    root = 'https://' + config['dashboard_host'] + config.get('dashboard_path', '/') if config.get('dashboard_host') else ''
    payload = {'title': i18n.t('Done: {}', row['title']) if text else i18n.t('Done'),
               'body': plain(row['body'] or '') if text else '', 'url': notify.todo_link(root, row['id']), 'tag': row['id'],
               '_line': notify.app_line_text('Done: {}', row['title']) if text else i18n.t('Done'), '_state': 'ready',
               'actions': quick_web('done')}
    return push_send(store, config, subscriptions, payload, 'done=' + row['id'], sender, kind='result')


def reminder_channels(store, config, kind='reminder'):
    """Where a reminder (a snooze ending, a result) reaches the owner, as deliver_one sends it: Telegram when it is on,
    and a notification on every subscribed device and phone with the app (push_reach). `push` is the device count.
    kind 'todo': where a new to-do held for later (deliver_after) goes when its time comes."""
    with store.connect() as db:
        push_pref = notify.allowed(db, kind, 'push')  # Settings, Notifications, per kind
        telegram_pref = notify.allowed(db, kind, 'telegram')
    subscriptions, phones = push_reach(store, config) if push_pref else ([], 0)
    push = len(subscriptions) + phones
    return {'telegram': telegram_on(config) and telegram_pref, 'push': push}


def mail_ready(config):
    """Email can go: a hosted or paired Machine hands it to the control plane's mailer (App.notify_mail_target)."""
    return bool(fleet.settings(config) and (config.get('credentials') or {}).get('fleet'))


# A hosted Machine whose owner signed up from this day on: the control plane turns its reviews on by itself once its AI
# and mail are connected (themachine-cloud worker.auto_activate, AUTO_ACTIVATE_SINCE).
HOSTED_REVIEWS_AUTO_SINCE = '2026-10-22'


def reviews_start_by_themselves(config):
    """Whether reviews, still off, turn on by themselves (a new hosted Machine), so the dashboard shows how far setup
    is instead of "Reviews are off" with a button. Not once the owner turned them off (first_look False), nor on a
    Machine set up before, whose owner turns them on themselves."""
    settings = config.get('review_worker') or {}
    return (str(config.get('manage_url') or '').startswith('https://') and not settings.get('enabled')
            and settings.get('first_look') is not False and str(config.get('started_at') or '')[:10] >= HOSTED_REVIEWS_AUTO_SINCE)


def cloud_target(config):
    """(url, token) of the control plane a hosted or paired Machine talks to (its email and the mobile app's push), or
    None (self-hosted and not paired)."""
    found = fleet.settings(config)
    if not found or not (config.get('credentials') or {}).get('fleet'):
        return None
    try:
        return found['url'], credential(config, 'fleet')
    except Exception:  # noqa: BLE001 - no readable token: nothing goes through the control plane
        return None


def app_wake(store, config, kind, tag, device=None, state=None, line=None, detail=None):
    """The mobile app's push: the control plane wakes the owner's phones with a fixed text for `kind`, never a to-do's
    own text, and a tap opens the dashboard. `tag` (a to-do's id) lets a newer one replace the older; `device` sends
    only to that phone (a test). `state` ('ready' or 'needs', a result only) picks the fixed text. `line` is kept here
    under the tag for the Android app, which asks for it (GET /api/notice) and shows it instead, with `detail` as the
    body under it (the morning's to-dos and first meeting): neither goes to the cloud. The number sent, or None when there was nothing to send to or it didn't go."""
    with store.connect() as db:
        if not notify.app_devices(db):
            return None
    target = cloud_target(config)
    if not target or kind not in notify.APP_KINDS:
        return None
    tag = str(tag or '')
    tag = tag if notify.APP_ID.fullmatch(tag) else kind
    if line:
        with store.connect() as db:
            notify.app_line_save(db, tag, line, body=detail or '')
    body = {'action': 'wake', 'kind': kind, 'tag': tag, **({'state': state} if kind == 'result' and state in ('ready', 'needs') else {}),
            **({'id': device} if device else {})}
    answer = notify.app_push(*target, body)
    if not answer or answer.get('missing'):
        return None
    removed = answer.get('removed')
    if removed and isinstance(removed, list):  # phones that uninstalled the app: gone here too
        with store.connect() as db:
            notify.app_device_remove(db, [str(r) for r in removed])
    elif removed:  # only a count: what the control plane still has is what Settings shows
        listed = notify.app_push(*target, {'action': 'list'})
        if listed and isinstance(listed.get('devices'), list):
            keep = {str(d.get('id')) for d in listed['devices'] if isinstance(d, dict)}
            with store.connect() as db:
                notify.app_device_remove(db, [d['id'] for d in notify.app_devices(db) if d['id'] not in keep])
    try:
        sent = max(0, int(answer.get('sent') or 0))
    except (TypeError, ValueError):
        sent = 0
    LOG.info('app push kind=%s sent=%d', kind, sent)
    return sent


# The phone app's notification buttons (app_notice): the dashboard's own decide choices, sent by the app with the
# owner's sign-in. Do it only for a to-do not started yet; sending and every final step open the app instead.
APP_BUTTONS = {'prepare': 'accept', 'snooze': 'snooze', 'done': 'complete'}


# Quick buttons on every notification (docs/help/notifications.md, "Buttons on notifications"), by what the to-do
# needs now. Nothing that sends, publishes, pays or submits ever runs from one: a draft opens in the app, where the
# owner reads it first ('draft', 'open', 'answer' and 'signin' only open). Snooze, Mark done and Do it run from a
# phone's notification after the phone unlocks (iOS authenticationRequired, Android setAuthenticationRequired); a
# browser can't ask for that, so there they open the dashboard, which does it and offers Undo (sw.js, #quick=).
# 'web': the browser's and Telegram's (at most two), 'app': the phone app's (at most three). The first leads.
QUICK = {
    'new': {'web': ('snooze2h', 'open'), 'app': ('prepare', 'snooze2h', 'done')},
    'draft': {'web': ('draft', 'snooze2h'), 'app': ('draft', 'snooze2h', 'done')},
    'ready': {'web': ('open', 'done'), 'app': ('open', 'done', 'snooze2h')},
    'question': {'web': ('answer', 'snooze2h'), 'app': ('answer', 'snooze2h', 'done')},
    'stuck': {'web': ('open', 'snooze2h'), 'app': ('open', 'snooze2h', 'done')},
    'signin': {'web': ('signin', 'snooze2h'), 'app': ('signin', 'snooze2h', 'done')},
    'preparing': {'web': ('open',), 'app': ('snooze2h', 'done')},
    'reminder': {'web': ('done', 'snooze'), 'app': ('done', 'snooze', 'open')},
    'done': {'web': ('open',), 'app': ('open',)},
    'view': {'web': ('open',), 'app': ()},  # the morning, the week, a Fleet update: it only opens (a tap, on a phone)
}
QUICK_OPENS = ('open', 'draft', 'answer', 'signin')
# What a button does: the dashboard's decide choice and its snooze time (Snooze alone is until tomorrow, as on a card)
# A button's decision from the phone app carries this decision id prefix (NotificationActions, MachineNotice.decide).
# From a notification, Do it only starts a to-do not started yet (notice_decision_refused): never a Do it on a draft or
# result, and never the step a Claude Code or Codex job left for the owner (card_chat.owner_do_it), which they see first.
NOTICE_DECISION = 'notify-'
NOTICE_CHOICES = ('accept', 'snooze', 'complete')


def notice_decision_refused(db, suggestion_id, choice):
    """Why a phone notification's button may not make this decision, or None. Only Do it (accept), Snooze and Mark done
    come from a notification; Do it only on a to-do still waiting to start, with no Claude Code or Codex work on it."""
    if choice not in NOTICE_CHOICES:
        return 'Open the to-do to do this.'
    if choice != 'accept':
        return None
    row = db.execute('SELECT status FROM suggestions WHERE id=?', (str(suggestion_id),)).fetchone()
    if not row or row['status'] != 'pending':
        return 'Open the to-do to do this.'
    if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='agent_jobs'").fetchone() and \
            db.execute('SELECT 1 FROM agent_jobs WHERE suggestion_id=? LIMIT 1', (str(suggestion_id),)).fetchone():
        return 'Open the to-do to do this.'
    return None


QUICK_RUNS = {'prepare': ('accept', None), 'snooze2h': ('snooze', '2h'), 'snooze': ('snooze', 'tomorrow'), 'done': ('complete', None)}
QUICK_LABELS = {'open': 'Open', 'draft': 'Open draft', 'answer': 'Answer', 'signin': 'Sign in', 'prepare': 'Do it',
                'snooze2h': 'Snooze', 'snooze': 'Snooze', 'done': 'Mark done'}


def quick_kind(row, kind=None, blocked=None, signin=None):
    """Which notification a to-do's is, for its buttons (QUICK): new, draft, ready, question, stuck, signin,
    preparing, reminder or done. kind (notify.KINDS) says a snooze or a wait came back."""
    if reported(row):
        return 'done'
    blocked = row.get('preparation_status') == 'blocked' if blocked is None else blocked
    if blocked:
        return 'signin' if signin else 'stuck'
    status = row.get('status')
    if status == 'prepared':
        try:
            outcome = json.loads(row.get('outcome') or '{}') or {}
        except (TypeError, ValueError):
            outcome = {}
        try:
            steps = next_actions.visible_actions(row.get('next_action'))
        except (TypeError, ValueError, AttributeError):
            steps = []
        drafted = any(s.get('kind') in next_actions.APPROVE_KINDS for s in steps)
        needs = str(outcome.get('needs') or '').strip()
        if needs and (needs.endswith('?') or not drafted):  # "check the draft and send it" is the draft's: Open draft
            return 'question'
        if outcome.get('state') == 'snoozed' and kind == 'reminder':
            return 'reminder'
        return 'draft' if drafted else 'ready'
    if status in ('accepted', 'instructions', 'local_preparation'):
        return 'preparing'
    return 'reminder' if kind == 'reminder' else 'new'


def quick_web(which, t=None):
    """A web push's buttons, [{action, title}], in the owner's language."""
    t = t or i18n.t
    return [{'action': a, 'title': t(QUICK_LABELS[a])} for a in QUICK[which]['web']]


APP_BODY = 120


APP_GONE = todo_states.CLOSED_OR_SNOOZED  # no longer waiting: its phone notification goes


APP_EMPTY = 'Tap to open.'  # the body when there is nothing to say under the title, or Text in notifications is off


def app_notice(store, config, tag, kind=None, version=1):
    """What the phone app's notification for a wakeup says (GET /api/notice): {line, title, body, actions, labels,
    events}, or {gone: True} for a to-do no longer waiting (done, snoozed, not needed), whose notification goes.
    An app from version 2 on (it asks with v=2 and the wakeup's kind) gets the quick buttons (QUICK); an older app
    the three it knows, Do it, Snooze (until tomorrow) and Mark done.
    title is the to-do's title, with its state in front unless it is ready ("Pick a time with Sam", "Preparing: Pay
    the Monizze invoice"): the phone has little room, and the body says what is ready, the next step ("Send to Sam:
    Tuesday 10:00 works for me."). With Text in notifications off (or a Careful work to-do): only the fixed words.
    A tag that is no to-do (the morning, a Fleet question): the line and body kept for it (notify.app_line)."""
    tag = str(tag or '')
    with store.connect() as db:
        line, detail = notify.app_line(db, tag), notify.app_line_body(db, tag)
        row = db.execute(f'SELECT s.*,{agent_jobs.shown_preparation(db, card="s.id")} preparation_status,p.reason preparation_reason,p.error preparation_error '
                         'FROM suggestions s LEFT JOIN preparations p ON p.suggestion_id=s.id '
                         'WHERE s.id=?', (tag,)).fetchone() if notify.APP_ID.fullmatch(tag) else None
        if not row:
            return {'line': line, 'title': line, 'body': detail or (i18n.t(APP_EMPTY) if line else ''), 'actions': []}
        row = dict(row)
        try:
            ids = json.loads(row.get('account_ids') or '[]')
        except (TypeError, ValueError):
            ids = []
        work = any(a['id'] in ids and str(a.get('boundary') or '').startswith('work:') for a in config.get('accounts', []))
        text = security_levels.notify_text(db, work)
        if reported(row):  # its confirmed step closed it: what happened, nothing left to tap but Open
            title = notify.app_line_text('Done: {}', row['title']) if text else i18n.t('Done')
            body = notify.clip(first_sentence(row.get('body') or ''), APP_BODY) if text else ''
            return {'line': title, 'title': title, 'body': body or i18n.t(APP_EMPTY), 'actions': list(QUICK['done']['app']) if version >= 2 else [],
                    'labels': {'open': i18n.t('Open')}}
        if row['status'] in APP_GONE:
            return {'gone': True}
        blocked = row.get('preparation_status') == 'blocked'
        browser = (store.suggestion_result(row, db).get('preparation_browser') or {}) if blocked else {}
        ready_lead = result_lead(db, row)
    if row.get('preparation_status') == agent_jobs.WORKING:  # a job handed off after a stuck run is on it: not Stuck
        lead, buttons = 'Working', ['snooze', 'done']
    elif row['status'] == 'prepared':
        lead, buttons = ready_lead, ['snooze', 'done']
    elif blocked:
        lead = 'Needs you to sign in' if browser.get('signin_url') else 'Stuck' if row.get('preparation_error') else 'Needs your help'
        buttons = ['snooze', 'done']
    elif row.get('preparation_status') == agent_jobs.HANDED_BACK:  # that job's result is in: nothing runs, so no Preparing
        lead, buttons = None, ['snooze', 'done']
    elif row['status'] in ('accepted', 'instructions', 'local_preparation'):
        lead, buttons = 'Preparing', ['snooze', 'done']
    else:
        lead, buttons = 'New to-do', ['prepare', 'snooze', 'done']
    t = i18n.t
    # one key per lead, as push_notify, written out so the catalogs carry each
    leads = {'Ready': ('Ready: {}', t('Ready')), 'Preparing': ('Preparing: {}', t('Preparing')),
             'New to-do': ('New to-do: {}', t('New to-do')), 'Stuck': ('Stuck: {}', t('Stuck')),
             'Needs your help': ('Needs your help: {}', t('Needs your help')),
             'Needs you to sign in': ('Needs you to sign in: {}', t('Needs you to sign in')),
             'Reminder': ('Reminder: {}', t('Reminder')), 'Working': ('Working: {}', t('Working'))}
    if lead == 'Ready' and text:  # what it is about leads; the line under it says what is ready (a draft, a result)
        title = notify.clip(row['title'], notify.APP_LINE)
    elif lead:
        title = notify.app_line_text(leads[lead][0], row['title']) if text else leads[lead][1]
    else:  # what it is is in its title ("Waiting on Sam: the quote"): nothing in front
        title = notify.clip(row['title'], notify.APP_LINE) if text else t('To-do')
    body = (notify.clip(app_next_step(row, blocked), APP_BODY) if text else '') or t(APP_EMPTY)
    events = {'prepare': t('Preparing it'), 'snooze': t('Snoozed it'), 'done': t('Marked it done'),
              'failed': t('Couldn’t reach your Machine. Open the app to try again.')}
    if version >= 2:
        which = quick_kind(row, kind, blocked, browser.get('signin_url'))
        if which == 'reminder':  # a snooze that came back says so, as its web push does
            title = notify.app_line_text(leads['Reminder'][0], row['title']) if text else leads['Reminder'][1]
        return {'line': title, 'title': title, 'body': body, 'actions': list(QUICK[which]['app']),
                'labels': {a: t(label) for a, label in QUICK_LABELS.items()}, 'events': {**events, 'snooze2h': t('Snoozed it')}}
    return {'line': title, 'title': title, 'body': body, 'actions': buttons,
            'labels': {'prepare': t('Do it'), 'snooze': t('Snooze'), 'done': t('Mark done'), 'open': t('Open')},
            'events': events}


def app_next_step(row, blocked=False):
    """The next step of a to-do in one line: what it needs from the owner, the draft waiting for their OK ("Reply to
    Sam: confirm Tuesday 10:00"), or what it is about."""
    if blocked:
        return plain(row.get('preparation_reason') or '')
    try:
        outcome = json.loads(row.get('outcome') or '{}') or {}
    except (TypeError, ValueError):
        outcome = {}
    if row['status'] == 'prepared':
        try:
            steps = next_actions.visible_actions(row.get('next_action'))
        except (TypeError, ValueError, AttributeError):
            steps = []
        step = next((a for a in steps if a.get('kind') != 'open'), None)
        needs = plain(outcome.get('needs') or '')
        # What the owner does: a question for them leads; for a draft, the draft itself says more than "check the
        # draft and send it" (who it goes to and how it starts)
        if needs and (needs.endswith('?') or not (step and step.get('kind') in next_actions.APPROVE_KINDS)):
            return needs
        if outcome.get('state') == 'waiting' and outcome.get('waiting_on'):
            return i18n.t('Waiting on: {}', plain(outcome['waiting_on']))
        if step:
            label = plain(next_actions.label(step))
            to = step.get('to') if isinstance(step.get('to'), list) else []
            if label == 'Send' and to:  # a reply with no label of its own: who it goes to
                label = i18n.t('Send to {}', str(to[0]).split('<')[0].strip().strip('"') or str(to[0]))
            else:
                label = i18n.t(label) if label in ('Send', 'Continue') else label
            try:
                draft = first_sentence(app_draft_lead(next_actions.draft_text(step))) if step.get('kind') in next_actions.APPROVE_KINDS else ''
            except (TypeError, ValueError, KeyError, AttributeError):
                draft = ''
            return f'{label}: {draft}' if draft else label
        return first_sentence(strip_result_links(row.get('body') or ''))
    return first_sentence(row.get('body') or '')


def app_draft_lead(text):
    """A draft without its greeting line ("Hi Mila,") and lines that are only a link, so the notification starts with
    what it says."""
    lines = [line.strip() for line in str(text or '').splitlines() if line.strip() and not re.fullmatch(r'<?\w+://\S+', line.strip())]
    if len(lines) > 1 and len(lines[0]) <= 40 and lines[0].endswith(','):
        lines = lines[1:]
    return '\n'.join(lines)


def app_clear_step(store, config):
    """A to-do a phone was woken for that no longer waits (done, snoozed, sent or not needed, here or anywhere): one
    clear wakeup without text, so the app takes its notification away (app_wake 'clear'). Each tag once; a tag that
    is no to-do (the morning, a Fleet question) stays until notify.app_line_save's own pruning."""
    with store.connect() as db:
        tags = notify.app_lines(db)
        if not tags:
            return []
        known = {r[0]: r[1] for r in db.execute('SELECT id,status FROM suggestions WHERE id IN ('
                                                + ','.join('?' * len(tags)) + ')', tags)}
        kept = {r[0] for r in db.execute('SELECT id,status,done_report FROM suggestions WHERE id IN (' + ','.join('?' * len(tags)) + ')', tags)
                if reported(dict(r))}  # its Done report stays until the owner saw it
        gone = [tag for tag in tags if known.get(tag) in APP_GONE and tag not in kept]
        for tag in gone:
            notify.app_line_forget(db, tag)
    for tag in gone:
        try:
            app_wake(store, config, 'clear', tag)
        except Exception as error:  # noqa: BLE001 - a clear is best effort
            LOG.warning('app clear error=%s', type(error).__name__)
    return gone


APP_SCHEME = 'computer.themachine.app://connect?u='  # the mobile app's own link: it asks the owner, then opens the address


def phone_app(config):
    """Settings, Phone app: how the mobile app finds this Machine. Hosted, or self-hosted on The Machine Network: it
    signs in with the account, which knows the Machine. Self-hosted and not on the Network: a QR code of the app's
    connect link with this Machine's own https address (its Tailscale name, dashboard_host), and the address to type in.
    Nothing secret: the dashboard's own sign-in still applies when the app opens it."""
    if str(config.get('manage_url') or '').startswith('https://') or cloud_target(config):
        return {'hosted': True}
    if not config.get('dashboard_host'):
        return {'hosted': False}
    url = 'https://' + config['dashboard_host'] + config.get('dashboard_path', '/')
    link = APP_SCHEME + urllib.parse.quote(url, safe='')
    try:
        rows = list(phone_qr(link))
    except ValueError:  # an address too long for a code: typed in instead
        rows = []
    return {'hosted': False, 'url': url, 'link': link, 'qr': rows}


def push_reach(store, config):
    """(web push subscriptions, phones with the app): where a push can go. The web ones need dashboard_host for their
    links; the app's need the control plane."""
    with store.connect() as db:
        subscriptions = [dict(r) for r in db.execute('SELECT endpoint,p256dh,auth FROM push_subscriptions')] if config.get('dashboard_host') else []
        phones = len(notify.app_devices(db))
    return subscriptions, phones if phones and cloud_target(config) else 0


def hold_mail(store, config, kind, title, ref, work=False):
    """Something now waits for the owner: an email EMAIL_AFTER from now if they still haven't seen it then and aren't
    using a dashboard (notify.take_due). Nothing when email is off for this kind or can't go."""
    if not mail_ready(config):
        return False
    with store.connect() as db:
        if not notify.allowed(db, kind, 'email'):
            return False
        notify.hold(db, 'email', kind, title, time.time() + notify.EMAIL_AFTER, ref=ref, show=security_levels.notify_text(db, work))
    LOG.info('notify email held kind=%s ref=%s', kind, ref)
    return True


def hold_handoff(store, config, row):
    """A teammate handed the owner a to-do and their Machine can't ping them: one email for it EMAIL_AFTER from now,
    unless they see it first or it no longer waits (notify.take_handoffs). Once per handoff; nothing when email is off
    for results or can't go."""
    if not mail_ready(config):
        return False
    title = str((json.loads(row['question'] or '{}') or {}).get('title') or '').strip()
    ref = 'fleet:' + row['id']
    with store.connect() as db:
        notify.ensure(db)
        if not title or not notify.allowed(db, 'result', 'email') or \
                db.execute("SELECT 1 FROM notify_queue WHERE channel='handoff' AND ref=?", (ref,)).fetchone():
            return False
        notify.hold(db, 'handoff', 'result', title, time.time() + notify.EMAIL_AFTER, ref=ref, payload={'name': row['name']},
                    show=security_levels.notify_text(db, True))
    return True


# Setup hints: what a hosted owner skipped at setup, suggested in the dashboard's setup to-do (setup_card) once it is
# relevant: a source when its mail keeps coming in, Telegram once a snooze would only come back on the dashboard, Codex
# once GitHub is connected. Each links to that step on the setup page. Who mails the owner: machine/sources/mail_senders.py.
def mailing_sources(db, config, now=None):
    """[(service, label)] of HINT_SOURCES that mailed the owner HINT_MAILS times or more in 30 days and aren't connected:
    worth connecting. From the senders' addresses only (setup_hints, and the first look's ending: first_look_done)."""
    services = {a.get('service') for a in config.get('accounts') or [] if isinstance(a, dict)}
    since = ((now or dt.datetime.now(dt.timezone.utc)) - dt.timedelta(days=30)).isoformat()
    return [(service, label) for service, label, domains in HINT_SOURCES
            if service not in services and mails_from(db, domains, since, HINT_MAILS) >= HINT_MAILS]


def setup_hints(store, config, now=None):
    """[{id, title, text, href, button}] for a hosted Machine (manage_url), most relevant first; [] elsewhere."""
    manage = str(config.get('manage_url') or '')
    if not manage.startswith('https://'):
        return []
    services = {a.get('service') for a in config.get('accounts') or [] if isinstance(a, dict)}
    hints = []
    with store.connect() as db:
        for service, label in mailing_sources(db, config, now):
            # one that signs in from + Add (HOSTED_SIGNINS) opens its form there, any other + Add: on the dashboard itself
            hints.append({'id': 'source-' + service, 'title': f'Connect {label}?',
                          'text': f'{label} mails you often. Connected, I read it directly.',
                          'href': f'#connect={service}' if service in HOSTED_SIGNINS else '#connections=add', 'button': 'Connect'})
        snoozed = db.execute("SELECT 1 FROM decisions WHERE choice='snooze' LIMIT 1").fetchone()
    channels = reminder_channels(store, config)
    if snoozed and not channels['telegram'] and not channels['push']:
        hints.append({'id': 'telegram', 'title': 'Reminders in Telegram?', 'text': 'Snoozed to-dos come back as a Telegram message too.',
                      'href': f'{manage}#telegram', 'button': 'Set up'})
    if 'github' in services and not agent_jobs.coding_relevant({'accounts': [], 'agents': config.get('agents')}):
        hints.append({'id': 'codex', 'title': 'Hand coding to-dos to Codex?', 'text': 'It works on your ChatGPT plan.',
                      'href': f'{manage}#codex', 'button': 'Connect'})
    return hints


def reminder_line(channels):
    """The honest promise for a snooze, from reminder_channels. The dashboard says the same (remindLine)."""
    if channels['telegram'] and channels['push']:
        return i18n.t('I’ll remind you on Telegram and as a notification.')
    if channels['telegram']:
        return i18n.t('I’ll remind you on Telegram.')
    if channels['push']:
        return i18n.t('I’ll send you a notification.')
    return i18n.t('It’ll be back on the dashboard then.')


# Talk's records by kind, as the voice says them, and their one line ("CTO · Acme", "acme.com", "a project, active")
TALK_KINDS = {'person': 'person', 'org': 'organization', 'project': 'project'}


def person_line(title, org):
    """A person's title and organization as one line: "CTO · Acme", "Wife · Umicore", or just the one that's there.
    Never "CTO at Acme": a title can be a relationship ("Wife"), and "at" reads wrong then. The dashboard's jobLine
    is the same format."""
    return ' · '.join(x for x in (' '.join(str(title or '').split()), ' '.join(str(org or '').split())) if x)


def talk_about(node):
    if node.get('kind') == 'person':
        org = node.get('org_name') or (node['org'].split(':', 1)[-1] if isinstance(node.get('org'), str) else '')
        return person_line(node.get('role'), org)
    if node.get('kind') == 'org':
        return ' · '.join(x for x in (str(node.get('role') or ''), str(node.get('domain') or ''), str(node.get('about') or '')) if x)
    return str(node.get('state') or '')


def waiting_count(db):
    """To-dos that need the owner now, for the app icon's badge (not the ones that look done or wait on others, nor a
    Still needed? left unanswered: folded into Coming back later)."""
    current = now()
    rows = db.execute(f"SELECT id FROM suggestions WHERE status IN {todo_states.sql(todo_states.WAITING_ON_OWNER)} AND NOT " + NOT_FOR_OWNER_SQL + " "
                      "AND (deliver_after IS NULL OR deliver_after<=?)", (current,)).fetchall()
    later = still_needed.folded(db, current, local_tz()) if rows else set()
    return sum(1 for r in rows if r[0] not in later)


def push_send(store, config, subscriptions, payload, label, sender=None, kind=None, held=False, wake=None):
    """kind (notify.KINDS): left out when the owner turned that kind off for push; held while a dashboard is in use or
    for a minute after they left one (notify.push_now), then sent by App.notify_step unless they saw it there. It
    carries the badge count. Without kind (a test, the digest) it goes at once.
    The phones with the mobile app get a wakeup of their own at the same moment (app_wake): `wake` is its kind (else
    `kind`; none for a test), its tag the payload's. Not for a silent one (a batch's later to-dos, the digest at the
    dashboard). Best effort: the web push goes the same with or without it. The results: one per web subscription,
    plus {'status': 200, 'app': sent} when the control plane took the wakeup."""
    payload = dict(payload)
    wake = wake or payload.pop('_wake', None) or kind
    # The mobile app's line and a result's state: for its wakeup only, never in the web push
    line, state, detail = payload.pop('_line', None), payload.pop('_state', None), payload.pop('_body', None)
    if wake == 'fleet' and detail is None and payload.get('body'):  # the app's body under the line, as the web push has it
        with store.connect() as db:
            detail = notify.clip(plain(payload['body']), notify.APP_BODY) if security_levels.notify_text(db, True) else ''
    if not str(payload.get('body') or '').strip():  # never a title alone: a plain line that says nothing of the to-do
        payload['body'] = i18n.t(APP_EMPTY)
    if kind:
        with store.connect() as db:
            if not notify.allowed(db, kind, 'push'):
                return []
            if not held and not notify.push_now():  # a dashboard in use, or just left: wait, it may be seen there
                kept = {**payload, **({'_wake': wake} if wake != kind else {}), **({'_line': line} if line else {}), **({'_state': state} if state else {}),
                        **({'_body': detail} if detail else {})}
                notify.hold(db, 'push', kind, str(payload.get('title') or ''), time.time(), payload=kept)
                LOG.info('push %s held', label)
                return []
            payload = {**payload, 'badge': waiting_count(db)}
    results = []
    if subscriptions:
        try:
            results = (sender or (lambda request: push_node(config, request)))({'action': 'send', 'subscriptions': subscriptions, 'payload': payload})['results']
        except (subprocess.TimeoutExpired, ValueError, KeyError) as error:
            LOG.warning('push %s error=%s', label, type(error).__name__)
            results = []
        else:
            with store.connect() as db:
                for result in results:
                    if result['status'] in (404, 410):  # the phone unsubscribed or the app was removed
                        db.execute('DELETE FROM push_subscriptions WHERE endpoint=?', (result['endpoint'],))
                    else:
                        db.execute('UPDATE push_subscriptions SET last_status=?,last_sent_at=? WHERE endpoint=?', (result['status'], now(), result['endpoint']))
            LOG.info('push %s statuses=%s', label, ','.join(str(r['status']) for r in results))
    if kind and not payload.get('silent'):
        with store.connect() as db:  # the day's count for notify.PUSH_CAP
            notify.count_push(db, dt.datetime.now(local_tz()).date().isoformat())
    if wake and not payload.get('silent'):
        try:
            sent = app_wake(store, config, wake, payload.get('tag'), state=state,
                            line=line if line is not None else notify.clip(payload.get('title')) if wake == 'fleet' else None, detail=detail)
        except Exception as error:  # noqa: BLE001 - the app's wakeup never stops the rest
            LOG.warning('app push %s error=%s', label, type(error).__name__)
            sent = None
        if sent is not None:
            results = [*results, {'status': 200, 'app': sent}]
    return results

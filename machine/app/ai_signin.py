"""A Claude sign-in that ended, told once (machine/claude_signin.py has why it ends): nothing new gets checked or
prepared until it is signed in again, and the dashboard's Needs you line only reaches someone who opens it. So the
owner hears it where urgent things reach them: a phone notification, and Telegram with Sign in again when Telegram is
on. Once per lapse (the credentials file's time, or the end it had: a new sign-in is a new one), within work hours,
by the owner's notification choices for to-dos that need them (kind 'result'). Run by the delivery worker.

One email goes too, through the control plane's mailer like the digest (a hosted or paired Machine: notify.mail),
with the one step that signs in again: three days ahead when the end is known, else when it ended. Once per sign-in
(its end, or the lapse's key when the end isn't known), never again when it then ends, and only when the owner gets
email for to-dos that need them."""
import hashlib
import json

import i18n
import notify
from machine import claude_signin
from machine.config import LOG
from machine.dashboard_link import dashboard_link
from machine.delivery.push import push_reach, push_send, quick_web
from machine.delivery.telegram import fleet_telegram
from machine.model_usage import telegram_on
from machine.store.first_look import note_ai_signin_told
from models import claude_plan_route
import timeutil
from timeutil import in_hours, local_tz

TOLD = 'claude_signin_told'  # milestones: the lapse that was told and the sign-in that was emailed (note_ai_signin_told)
TEXT = 'Claude is signed out, so nothing new gets checked or prepared.'
SOON = ('Your Claude sign-in ends today.', 'Your Claude sign-in ends tomorrow.', 'Your Claude sign-in ends in 2 days.')


def lapse(found):
    """The key of a sign-in that ended, or None while it holds (or nothing can tell)."""
    if not found or found['signed_in']:
        return None
    return found.get('expires_at') or str(claude_signin.stamp())


def told(db, field='lapse'):
    row = db.execute('SELECT detail FROM milestones WHERE name=?', (TOLD,)).fetchone()
    try:
        return json.loads(row[0]).get(field) if row else None
    except (TypeError, ValueError, AttributeError):
        return None


def mail_text(found, left, manage, url):
    """(subject, text) of the one email: the sign-in ended, or ends within three days (left). The subject is its
    headline (notify_mail.layout), then what to do, as the phone notification says it."""
    subject = i18n.t('Claude is signed out') if left is None else i18n.t(SOON[min(2, left)])
    lines = [subject, i18n.t('Sign in again to keep things running.')]
    if url:  # its own line: the email's button (the control plane's notify_mail.layout)
        lines.append(i18n.t('Sign in again: {}', url) if manage else i18n.t('Open The Machine: {}', url))
    return subject, '\n\n'.join(lines)


def step(app, current=None, push=push_send, telegram=fleet_telegram, mail=None):
    """Tells a lapse that wasn't told yet, and emails a sign-in that ends soon or ended once. Returns the channels it
    went to ([] when there was nothing to tell)."""
    config = app.config
    if not claude_plan_route(config):
        return []
    found = claude_signin.read(config, wait=False)  # never waits on `claude auth status`
    local = (current or timeutil.clock()).astimezone(local_tz())
    key = lapse(found)
    left = claude_signin.days_left(found, local.timestamp())
    mailed = key or (found['expires_at'] if left is not None else None)  # one email per sign-in: ahead, else at its end
    if not mailed:
        return []
    target = app.notify_mail_target() if app.notify_on('result', 'email') else None
    with app.store.connect() as db:
        if not in_hours(local):
            return []
        tell = key and told(db) != key
        email = target and told(db, 'mailed') != mailed
        if not tell and not email:
            return []
        note_ai_signin_told(db, local.isoformat(), key if tell else told(db), mailed if email else told(db, 'mailed'))
    manage = str(config.get('manage_url') or '')
    url = manage + '#model' if manage.startswith('https://') else dashboard_link(config)
    went = []
    subscriptions, phones = push_reach(app.store, config) if tell else ([], 0)
    if subscriptions or phones:
        body = i18n.t('Sign in again to keep things running.')
        if push(app.store, config, subscriptions, {'title': i18n.t('Claude is signed out'), 'body': body, 'url': url, 'tag': 'ai-signin',
                                                   '_line': i18n.t('Claude is signed out'), '_body': body, '_state': 'needs',
                                                   'actions': quick_web('view')}, 'ai-signin', kind='result', wake='result'):
            went.append('push')
    if tell and telegram_on(config) and app.notify_on('result', 'telegram'):
        try:
            telegram(config, {'text': i18n.t(TEXT), 'buttons': [[{'text': i18n.t('Sign in again' if manage else 'Open'), 'url': url}]] if url else []})
            went.append('telegram')
        except Exception as error:  # noqa: BLE001 - the dashboard still says it
            LOG.warning('ai signin telegram error=%s', type(error).__name__)
    if email:
        subject, text = mail_text(found, None if key else left, manage.startswith('https://'), url)
        # the control plane sends one delivery once, whatever happens to this answer (notify_mail_receipts)
        delivery = hashlib.sha256(('claude-signin\n' + mailed).encode()).hexdigest()[:32]
        if (mail or notify.mail)(*target, subject, text, delivery=delivery):
            went.append('email')
    LOG.info('ai signin %s channels=%s', 'lapse told' if key else 'end told', ','.join(went) or '-')
    return went

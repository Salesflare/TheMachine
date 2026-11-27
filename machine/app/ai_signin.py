"""A Claude sign-in that ended, told once (machine/claude_signin.py has why it ends): nothing new gets checked or
prepared until it is signed in again, and the dashboard's Needs you line only reaches someone who opens it. So the
owner hears it where urgent things reach them: a phone notification, and Telegram with Sign in again when Telegram is
on. Once per lapse (the credentials file's time, or the end it had: a new sign-in is a new one), within work hours,
by the owner's notification choices for to-dos that need them (kind 'result'). Run by the delivery worker."""
import json

import i18n
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

TOLD = 'claude_signin_told'  # milestones: the lapse that was told (note_ai_signin_told)
TEXT = 'Claude is signed out, so nothing new gets checked or prepared.'


def lapse(found):
    """The key of a sign-in that ended, or None while it holds (or nothing can tell)."""
    if not found or found['signed_in']:
        return None
    return found.get('expires_at') or str(claude_signin.stamp())


def told(db):
    row = db.execute('SELECT detail FROM milestones WHERE name=?', (TOLD,)).fetchone()
    try:
        return json.loads(row[0]).get('lapse') if row else None
    except (TypeError, ValueError, AttributeError):
        return None


def step(app, current=None, push=push_send, telegram=fleet_telegram):
    """Tells a lapse that wasn't told yet. Returns the channels it went to ([] when there was nothing to tell)."""
    config = app.config
    if not claude_plan_route(config):
        return []
    key = lapse(claude_signin.read(config, wait=False))  # never waits on `claude auth status`
    if not key:
        return []
    local = (current or timeutil.clock()).astimezone(local_tz())
    with app.store.connect() as db:
        if told(db) == key or not in_hours(local):
            return []
        note_ai_signin_told(db, local.isoformat(), key)
    manage = str(config.get('manage_url') or '')
    url = manage + '#model' if manage.startswith('https://') else dashboard_link(config)
    went = []
    subscriptions, phones = push_reach(app.store, config)
    if subscriptions or phones:
        body = i18n.t('Sign in again to keep things running.')
        if push(app.store, config, subscriptions, {'title': i18n.t('Claude is signed out'), 'body': body, 'url': url, 'tag': 'ai-signin',
                                                   '_line': i18n.t('Claude is signed out'), '_body': body, '_state': 'needs',
                                                   'actions': quick_web('view')}, 'ai-signin', kind='result', wake='result'):
            went.append('push')
    if telegram_on(config) and app.notify_on('result', 'telegram'):
        try:
            telegram(config, {'text': i18n.t(TEXT), 'buttons': [[{'text': i18n.t('Sign in again' if manage else 'Open'), 'url': url}]] if url else []})
            went.append('telegram')
        except Exception as error:  # noqa: BLE001 - the dashboard still says it
            LOG.warning('ai signin telegram error=%s', type(error).__name__)
    LOG.info('ai signin lapse told channels=%s', ','.join(went) or '-')
    return went

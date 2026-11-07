"""Delivering to-dos: deliver and deliver_one (the message for each new or changed to-do, edited in place), the
uncertain sends it settles (reconcile_uncertain), and the Fleet's pushes. Moved out of assistant.py as is."""
import contextlib
import datetime as dt
import json
from pathlib import Path
import sqlite3
import subprocess
import uuid

import fleet
import i18n
from machine.cards import card, controls
from machine.config import LOG
from machine.delivery.push import hold_mail, push_notify, push_reach, push_send, result_lead
from machine.delivery.telegram import DeliveryNotSent, telegram
from machine.text import encoded
import notify
from timeutil import in_hours, is_work_day, local_tz, next_work_day, now


def fleet_push(store, config, rows, sender=None):
    """Phone notification for Fleet questions waiting for the owner: who asks and what, nothing of the owner's."""
    subscriptions, phones = push_reach(store, config)
    if not subscriptions and not phones:
        return []
    return push_send(store, config, subscriptions, fleet.push_payload(rows, fleet.dashboard_root(config)), 'fleet=' + rows[0]['id'], sender, kind='result', wake='fleet')


def fleet_notice_push(store, config, view, sender=None):
    """Phone notification for a Fleet notice (a seat request, someone joined or left, a server started)."""
    subscriptions, phones = push_reach(store, config)
    if not subscriptions and not phones:
        return []
    return push_send(store, config, subscriptions, fleet.notice_push(view, fleet.dashboard_root(config)), 'fleet=' + view['id'], sender, kind='result', wake='fleet')


def cached_card_ids(config, suggestion_id, since):
    """Bot cards for this suggestion in the owner chat, from OpenClaw's own Telegram cache."""
    path = config.get('openclaw_state', str(Path.home() / '.openclaw/state/openclaw.sqlite'))
    callback = f'assistant:{suggestion_id}:'
    found = []
    with contextlib.closing(sqlite3.connect('file:' + path + '?mode=ro', uri=True, timeout=2)) as native:
        for value, in native.execute("SELECT value_json FROM plugin_state_entries WHERE plugin_id='telegram' "
                                     "AND namespace='telegram.message-cache' AND (instr(value_json,?)>0 OR instr(value_json,?)>0 OR instr(value_json,?)>0)",
                                     (callback,'#chat='+suggestion_id,'#result='+suggestion_id)):  # #result= in notices sent before
            message = json.loads(value).get('sourceMessage', {})
            if (str(message.get('chat', {}).get('id')) == config.get('telegram_owner') and message.get('from', {}).get('is_bot')
                    and message.get('message_id') and (message.get('date') or 0) >= since):
                found.append(int(message['message_id']))
    return found


def reconcile_uncertain(store, config, grace_minutes=30):
    """An unknown send outcome (e.g. Telegram network trouble outlasting the helper's
    timeout) must not silence a card forever. Confirm it from the cached bot message
    carrying this suggestion's buttons; if none appears within the grace period, the
    send did not happen, so queue it again."""
    current = dt.datetime.now(dt.timezone.utc)
    with store.connect() as db:
        rows = [dict(r) for r in db.execute("SELECT d.*,s.status suggestion_status FROM deliveries d JOIN suggestions s ON s.id=d.suggestion_id "
                                            "WHERE d.status='uncertain' AND d.updated_at<?", ((current - dt.timedelta(minutes=2)).isoformat(),))]
    for row in rows:
        attempted = dt.datetime.fromisoformat(row['updated_at'])
        notice=row.get('send_kind')=='notice'
        try:
            excluded={str(row['message_id']),str(row.get('notification_message_id')), *map(str,json.loads(row['previous_message_ids']))}
            ids = [i for i in cached_card_ids(config, row['suggestion_id'], (attempted - dt.timedelta(minutes=5)).timestamp())
                   if str(i) not in excluded]
        except (sqlite3.Error, OSError, ValueError):
            continue  # cache unavailable: keep holding rather than risk a duplicate
        with store.connect() as db:
            if ids:
                if notice:
                    db.execute("UPDATE deliveries SET status='sent',notification_message_id=?,error=NULL,reminder=0,updated_at=? WHERE suggestion_id=? AND status='uncertain'",
                               (str(max(ids)),now(),row['suggestion_id']))
                    LOG.info('delivery suggestion=%s reconciled=notice_sent',row['suggestion_id'])
                    continue
                previous = json.loads(row['previous_message_ids'])
                if row['message_id'] and row['message_id'] not in previous:
                    previous.append(row['message_id'])
                db.execute("UPDATE deliveries SET status='sent',message_id=?,previous_message_ids=?,error=NULL,needs_edit=1,updated_at=? "
                           "WHERE suggestion_id=? AND status='uncertain'", (str(max(ids)), encoded(previous), now(), row['suggestion_id']))
                LOG.info('delivery suggestion=%s reconciled=sent', row['suggestion_id'])
            elif current - attempted >= dt.timedelta(minutes=grace_minutes):
                if row['suggestion_status'] in ('pending', 'accepted', 'prepared', 'instructions'):
                    # Not in the chat: it was never delivered. An earlier card exists, so this is a reminder.
                    db.execute("UPDATE deliveries SET status='queued',reminder=?,error=NULL,updated_at=? WHERE suggestion_id=? AND status='uncertain'",
                               (1 if row['message_id'] else 0, now(), row['suggestion_id']))
                    LOG.info('delivery suggestion=%s reconciled=requeued', row['suggestion_id'])
                else:
                    db.execute("UPDATE deliveries SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status='uncertain'",
                               (now(), row['suggestion_id']))


def deliver(store, config):
    # Owner approved grouped delivery. Bounded batches avoid a notification flood.
    for _ in range(max(1, min(10, int(config.get('delivery_batch_size', 5))))):
        if not deliver_one(store, config, edit_cards=(_ == 0)):
            break


def delivery_time(when, digest_at='08:30', current=None, work=False, urgent=False):
    """When a new suggestion's card goes out: now, the next morning digest, or a given day."""
    current = current or dt.datetime.fromisoformat(now())
    local = current.astimezone(local_tz())
    hour, minute = (int(x) for x in digest_at.split(':'))
    def weekend(target):
        # Work waits for a work day (work_hours.days), at the digest.
        local_target=target.astimezone(local_tz())
        if work and not urgent and not is_work_day(local_target):
            return next_work_day(local_target).replace(hour=hour,minute=minute,second=0,microsecond=0).astimezone(dt.timezone.utc).isoformat()
        return None if target<=current else target.astimezone(dt.timezone.utc).isoformat()
    if when == 'now':
        return weekend(current)
    if when and when != 'digest':
        try:
            target = dt.datetime.fromisoformat(str(when))
        except ValueError:
            raise ValueError('when is "now", "digest" or a date/time like 2026-10-12 or 2026-10-12T09:00') from None
        if target.tzinfo is None:
            target = target.replace(tzinfo=local_tz())
            if len(str(when)) <= 10:
                target = target.replace(hour=hour, minute=minute)
        return weekend(max(target,current))
    digest = local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if digest <= local:
        digest += dt.timedelta(days=1)
    return weekend(digest)


FEEDBACK_COLUMN = "(SELECT feedback FROM decisions f WHERE f.suggestion_id=s.id AND f.feedback!='' AND NOT EXISTS (SELECT 1 FROM decision_annotations a WHERE a.decision_id=f.id) ORDER BY f.rowid DESC LIMIT 1) requested_feedback"


EDIT_ROWS = ('SELECT s.*,d.message_id,d.edit_failures,p.status preparation_status,p.reason preparation_reason,p.error preparation_error,p.questions preparation_questions,(SELECT choice FROM decisions WHERE id=p.decision_id) preparation_cause,'+FEEDBACK_COLUMN+' FROM suggestions s '
             'JOIN deliveries d ON s.id=d.suggestion_id LEFT JOIN preparations p ON s.id=p.suggestion_id '
             'WHERE d.needs_edit=1 AND d.message_id IS NOT NULL')


def deliver_one(store, config, edit_cards=True):
    # One existing OpenClaw bot, never a second getUpdates consumer.
    store.wake_snoozed()
    if edit_cards:
        reconcile_uncertain(store, config)
    with store.connect() as db:
        edits = [dict(r) for r in db.execute(EDIT_ROWS + ' AND (d.edit_retry_at IS NULL OR d.edit_retry_at<=?)', (now(),))] if edit_cards else []
    for row in edits:
        try:
            with store.connect() as db:
                row.update(store.suggestion_result(row,db))
            telegram(config,row,'edit',row['message_id'])
            with store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                # Clear only if the card still renders the same: a concurrent change to
                # preparation status/reason or snooze time must get its own edit.
                current = db.execute(EDIT_ROWS + ' AND s.id=?', (row['id'],)).fetchone()
                current=dict(current) if current else None
                if current:current.update(store.suggestion_result(current,db))
                if current and card(current) == card(row) and controls(current) == controls(row) and current['requested_feedback']==row['requested_feedback']:
                    db.execute('UPDATE deliveries SET needs_edit=0,edit_failures=0,edit_retry_at=NULL,updated_at=? WHERE suggestion_id=?',
                               (now(), row['id']))
        except (subprocess.TimeoutExpired,ValueError):
            # e.g. the owner deleted the message. Back off (1 min doubling to 6 h)
            # instead of spawning node every 10 seconds forever.
            failures = row.get('edit_failures', 0) + 1
            retry = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=min(2 ** (failures - 1), 360))
            with store.connect() as db:
                db.execute('UPDATE deliveries SET edit_failures=?,edit_retry_at=? WHERE suggestion_id=?',
                           (failures, retry.isoformat(), row['id']))
    if not in_hours(dt.datetime.now(local_tz())):
        return  # quiet outside the owner's hours (work_hours.start–end)
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        # A crash/timeout after sending may have delivered. Never blindly resend.
        db.execute("UPDATE deliveries SET status='uncertain',error='interrupted_delivery' WHERE status='sending' AND updated_at<?",
                   ((dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=3)).isoformat(),))
        retry_cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()
        store.settle_awaiting(db)
        rows = db.execute("SELECT s.*,d.reminder,d.message_id,d.previous_message_ids,p.status preparation_status,p.reason preparation_reason,p.error preparation_error,p.questions preparation_questions,(SELECT choice FROM decisions WHERE id=p.decision_id) preparation_cause,"+FEEDBACK_COLUMN+" FROM suggestions s JOIN deliveries d ON s.id=d.suggestion_id LEFT JOIN preparations p ON s.id=p.suggestion_id WHERE d.status='queued' AND (d.error IS NULL OR d.updated_at<?) AND ((s.status='pending' AND s.handled_hint IS NULL) OR (d.reminder=1 AND s.status IN ('accepted','prepared','instructions') AND s.handled_hint IS NULL AND coalesce(json_extract(s.outcome,'$.state'),'') NOT IN ('already_done','waiting'))) AND ((d.reminder=1 AND s.early=0) OR s.deliver_after IS NULL OR s.deliver_after<=?) ORDER BY d.reminder DESC,s.created_at LIMIT 1",(retry_cutoff,now())).fetchall()
        if not rows:
            return
        row = dict(rows[0])
        # Enforce at delivery too: the last work day's queued work may catch up on a day off.
        # Owner-selected snoozes/preparations are reminders and keep their timing.
        work=row.get('area')!='personal' and any(a['id'] in json.loads(row['account_ids']) and a.get('boundary','').startswith('work:') for a in config.get('accounts',[]))
        held=delivery_time('now',work=work,urgent=bool(row.get('urgent')))
        if not row['reminder'] and held:
            db.execute('UPDATE suggestions SET deliver_after=? WHERE id=?',(held,row['id']))
            return
        row.update(store.suggestion_result(row,db))
        row['_result_notice']=bool(row['reminder'] and row['message_id'] and (row['status']=='prepared' or row.get('preparation_status')=='blocked') and config.get('dashboard_host'))
        row['_lead']=result_lead(db,row)  # "Ready" only when something waits for the owner's review
        if row['_result_notice'] and edit_cards:
            # Keep one full task card. Do not notify Ready before its edit landed.
            # ...unless the card can't be edited (deleted, too old): after three failed
            # edits, notify anyway rather than hold the result back indefinitely.
            edit=db.execute('SELECT needs_edit,edit_failures FROM deliveries WHERE suggestion_id=?',(row['id'],)).fetchone()
            if edit['needs_edit'] and (edit['edit_failures'] or 0) < 3:return
        # A batch (morning digest, several snoozes coming back at 09:00) buzzes once: only
        # the first card in a three-minute window notifies, the rest arrive silently.
        row['_silent']=bool(db.execute('SELECT 1 FROM deliveries WHERE suggestion_id!=? AND last_notified_at>?',
            (row['id'],(dt.datetime.fromisoformat(now())-dt.timedelta(minutes=3)).isoformat())).fetchone())
        db.execute("UPDATE deliveries SET status='sending',send_kind=?,updated_at=? WHERE suggestion_id=?", ('notice' if row['_result_notice'] else 'card',now(), row['id']))
    status, message_id, error = 'uncertain', None, None
    try:
        with store.connect() as db:
            current = db.execute('SELECT status,snoozed_until FROM suggestions WHERE id=?',(row['id'],)).fetchone()
            if current['status'] != row['status'] or current['snoozed_until']:
                db.execute("UPDATE deliveries SET status='cancelled',reminder=0 WHERE suggestion_id=? AND status='sending'",(row['id'],))
                return
        with store.connect() as db:
            on_telegram = notify.allowed(db, notify.kind_of(row), 'telegram')
        if notify.active():
            row['_silent'] = True  # the owner is at the dashboard: Telegram arrives without a buzz, and no push goes
        # Off for this kind in Settings, Notifications: a local receipt, as when Telegram is off (the dashboard has it).
        receipt = telegram(config,row,'send') if on_telegram else {'messageId': 'web-' + uuid.uuid4().hex[:12]}
        message_id = receipt.get('messageId') or receipt.get('message_id')
        if message_id:
            status = 'sent'
        else:
            error = 'missing_delivery_receipt'
    except DeliveryNotSent as failure:
        status, error = 'queued', str(failure)
    except (subprocess.TimeoutExpired, ValueError):
        error = 'delivery_outcome_unknown'
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if row['_result_notice']:
            current=db.execute(EDIT_ROWS.replace('WHERE d.needs_edit=1 AND','WHERE')+' AND s.id=?',(row['id'],)).fetchone()
            newer_result=bool(current and (current['body']!=row['body'] or current['preparation_reason']!=row['preparation_reason']
                              or current['requested_feedback']!=row['requested_feedback'])
                              and (current['status']=='prepared' or current['preparation_status']=='blocked'))
            db.execute('''UPDATE deliveries SET status=?,notification_message_id=coalesce(?,notification_message_id),error=?,
                updated_at=?,last_notified_at=CASE WHEN ? THEN ? ELSE last_notified_at END,reminder=? WHERE suggestion_id=?''',
                ('queued' if status=='sent' and newer_result else status,str(message_id) if message_id else None,error,
                 now(),status=='sent',now(),1 if newer_result else 0 if status=='sent' else row['reminder'],row['id']))
        else:
            previous = json.loads(row['previous_message_ids'])
            if message_id and row['message_id'] and row['message_id'] not in previous:
                previous.append(row['message_id'])
            db.execute('UPDATE deliveries SET status=?,message_id=?,previous_message_ids=?,error=?,updated_at=?,last_notified_at=CASE WHEN ? THEN ? ELSE last_notified_at END,reminder=? WHERE suggestion_id=?',
                       (status,str(message_id) if message_id else row['message_id'],encoded(previous),error,now(),status != 'queued',now(),row['reminder'] if status == 'queued' else 0,row['id']))
            if message_id:
                # A decision made while this send was in flight could not mark the (not yet
                # known) message for editing; the fresh card would keep stale buttons.
                sent = db.execute(EDIT_ROWS.replace('WHERE d.needs_edit=1 AND', 'WHERE') + ' AND s.id=?', (row['id'],)).fetchone()
                sent=dict(sent) if sent else None
                if sent:sent.update(store.suggestion_result(sent,db))
                if sent and (card(sent) != card(row) or controls(sent) != controls(row) or sent['requested_feedback']!=row['requested_feedback']):
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?', (row['id'],))
                if sent and row['status']=='instructions' and sent['status'] in ('instructions','prepared') and (
                        sent['status']=='prepared' or sent['requested_feedback']!=row['requested_feedback']):
                    # The result/new request arrived during its receipt send. Keep
                    # its distinct notification intent instead of losing it here.
                    db.execute("UPDATE deliveries SET status='queued',reminder=1,error=NULL WHERE suggestion_id=?",(row['id'],))
    # Optional phone delivery must never delay committing a known Telegram receipt. A batch buzzes once (_silent),
    # but every card of it reaches the phone, as it reaches Telegram.
    if status == 'sent':
        try:push_notify(store, config, row)
        except Exception as failure:LOG.warning('push error=%s', type(failure).__name__)
        try:
            work = any(a['id'] in json.loads(row.get('account_ids') or '[]') and str(a.get('boundary') or '').startswith('work:') for a in config.get('accounts', []))
            ready = row['_result_notice'] and row['status'] == 'prepared'
            lead = row.get('_lead', 'Ready')
            title = (i18n.t(lead + ': {}', row['title']) if lead else row['title']) if ready else i18n.t('Reminder: {}', row['title']) if row.get('reminder') and not row['_result_notice'] else row['title']
            hold_mail(store, config, notify.kind_of(row), title, 'suggestion:' + row['id'], work)
        except Exception as failure:LOG.warning('mail hold error=%s', type(failure).__name__)
    if row['_result_notice']:
        LOG.info('delivery suggestion=%s notice=1 status=%s error=%s',row['id'],status,error)
    else:
        LOG.info('delivery suggestion=%s reminder=%d status=%s error=%s', row['id'], row['reminder'] or 0, status, error)
    return status == 'sent'

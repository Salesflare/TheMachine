"""Approved actions carried out in the background: the delivery and action workers, an action's step, a merged fix's
effects and its Undo, and stopping runs that live on after they were canceled, replaced or finished. Moved out of
assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import sqlite3
import threading
import time
import uuid

import activity_log
import agent_jobs
import calendar_writes
import doc_writes
import follow_ups
from machine.cards import ACTION_WORKING, PREPARATION_WORKING, thread_return_time
from machine.config import LOG
from machine.delivery.deliver import deliver
from machine.delivery.push import app_clear_step
from machine.faults import loop_failed, restart_self
from machine.sources.connectors import docs_transport, docs_write_transport, intercom_transport
from machine.store.decisions import note_first, NOTHING_SENT, settle_sent
from machine.store.first_look import VERIFIED_KINDS
from machine.store.machine_cards import parked_redo
from machine.text import encoded
import next_actions
import parked_fixes
import preparation_state
from sources import credential, gog_read, mailbox_name
from timeutil import now


# A run that saved its result or blocker usually still writes its last reply: it gets this long to end by itself
# before it is stopped, so its record says how it ended (ok) instead of a stop's lost/aborted.
PREPARATION_SETTLE_SECONDS = 120


def queue_thread_snooze(db, action, job):
    if action.get('snooze_days') and action.get('thread_id'):
        db.execute("INSERT OR IGNORE INTO thread_snoozes(job_id,account_id,thread_id,until,status,created_at,updated_at) VALUES(?,?,?,?,'queued',?,?)",
                   (job['id'],action['account_id'],action['thread_id'],thread_return_time(action['snooze_days']),now(),now()))


def queue_delegate_wait(db, action, job, result):
    """A task handed to someone: once the message is sent, the card waits for their answer. It
    closes when they reply (settle_awaiting) and comes back after wait_days if not."""
    if not action.get('delegate'):
        return
    row = db.execute('SELECT status FROM suggestions WHERE id=?', (job['suggestion_id'],)).fetchone()
    if not row or row['status'] != 'prepared':
        return
    if action['kind'] == 'slack':
        if not result.get('channel_id') or not result.get('user_id'):
            return
        watch = {'kind': 'slack.message', 'channel_id': result['channel_id'], 'user_id': result['user_id']}
    else:
        watch = {'kind': 'gmail.message', 'from': action['to'][0].lower(), 'thread_id': action.get('thread_id'), 'reply_to': job.get('rfc_message_id') or ''}
    watch.update(account_id=action['account_id'], since=now(), delegated=True, name=action.get('to_name') or action['to'][0])
    db.execute("UPDATE suggestions SET awaiting=?,status='snoozed',snoozed_until=?,resume_status='prepared',undo_until=NULL WHERE id=?",
               (encoded(watch), thread_return_time(action['wait_days']), job['suggestion_id']))


def settle_doc_write(store, db, suggestion_id, job_id, action, url=None):
    """A doc made or changed after the owner's OK. With last:true the doc was the whole to-do: done, like a send.
    Otherwise something is left after it (a reply with its link, sharing it): the to-do stays open and carries on with
    that step (then, or what is left), drafted again for the owner's OK, never sent by itself (2026-10-30)."""
    made_now = doc_writes.made_by_itself(db.execute('SELECT approval_id FROM action_jobs WHERE id=?', (job_id,)).fetchone())
    if action.get('last') is True:
        if made_now:  # made while it was prepared (Store.make_new_docs): it stays open with the doc's link for the owner to look at
            return False
        return settle_sent(store, db, suggestion_id, job_id, next_actions.label(action), doc_writes.done(action))
    row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
    if not row or row['status'] != 'prepared':
        return False
    finished = {r[0] for r in db.execute("SELECT revision FROM action_jobs WHERE suggestion_id=? AND status IN ('sent','done')", (suggestion_id,))}
    if any(a['kind'] in next_actions.APPROVE_KINDS + next_actions.FINISH_KINDS and a['revision'] not in finished
           for a in next_actions.visible_actions(row['next_action'])):
        return False
    note = doc_writes.done(action)
    step = (f"{note}{' (' + url + ')' if url else ''}. Now: {action.get('then') or 'what is left of this to-do after the doc'}. "
            'Draft it for the owner to approve, never send it; save outcome done only when nothing is left.')
    body = NOTHING_SENT.sub('', row['body'] or '').strip() or row['body']
    stamp = now()
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               ('sent:' + job_id, suggestion_id, 'update', note[:200], 'assistant', stamp))
    db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
               ('after:' + job_id, suggestion_id, 'continue', step[:2000], 'assistant', stamp))
    db.execute("UPDATE suggestions SET status='accepted',body=?,outcome=NULL,early=0,undo_until=NULL WHERE id=?", (body, suggestion_id))
    store.queue_preparation(db, suggestion_id, 'after:' + job_id)
    return True


def active_work(db):
    """Work a restart or an update would cut off: agent jobs that run, sends under way, confirmed steps being worked on
    and preparations that started. Paused steps, blocked or queued preparations and finished work are not in it."""
    found = {}
    for name, sql, args in (
            ('agent_jobs', 'SELECT id,suggestion_id,status FROM agent_jobs WHERE status IN (%s)', agent_jobs.ACTIVE),
            ('action_jobs', 'SELECT id,suggestion_id,status FROM action_jobs WHERE status IN (%s)', ACTION_WORKING),
            ('preparations', 'SELECT job_id id,suggestion_id,status FROM preparations WHERE status IN (%s)', PREPARATION_WORKING)):
        try:
            rows = db.execute(sql % ','.join('?' for _ in args), args).fetchall()
        except sqlite3.OperationalError:  # a table this install doesn't have yet
            rows = []
        found[name] = [dict(zip(('id', 'suggestion_id', 'status'), tuple(r))) for r in rows]
    found['agent_jobs'] = agent_jobs.working(db, found['agent_jobs'])  # nor jobs whose worker is gone
    return found


class ActionRunsApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def delivery_worker(self):
        while not self.stop.wait(10):
            if not self.config.get('delivery_enabled', False):
                continue
            try:
                self.feedback_prompt_step()
                deliver(self.store, self.config)
                self.notify_step()
                self.digest_step()
                app_clear_step(self.store, self.config)  # notifications on phones for what no longer waits
            except Exception as error:
                loop_failed(LOG, 'delivery', error)

    def action_step(self,transport=None):
        transport=transport or next_actions.ActionTransport(next_actions.EmailTransport(self.config,credential,gog_read),next_actions.LinkedInTransport(self.config),next_actions.SlackTransport(self.config,credential),next_actions.XTransport(self.config),next_actions.MergeTransport(self.config,restart_self),next_actions.WhatsAppTransport(self.config),intercom_transport(self.config),calendar_writes.CalendarTransport(self.config,credential,gog_read),docs_transport(self.config),next_actions.TelegramTransport(self.config),docs_write_transport(self.config))
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            for candidate in db.execute("SELECT j.id,j.revision,s.status,s.next_action FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id WHERE j.status IN ('queued','blocked')").fetchall():
                if candidate['status']!='prepared' or not next_actions.selected(candidate['next_action'],candidate['revision']):
                    db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE id=?",(now(),candidate['id']))
            job=None
            for found in db.execute("SELECT * FROM action_jobs WHERE status IN ('queued','sending','uncertain') AND (retry_at IS NULL OR retry_at<=?) ORDER BY created_at",(now(),)).fetchall():
                # Automated follow-ups in a row: the next from the same account waits its gap (follow_ups.SEND_GAP); another account's goes
                # A paused board or project: Send without asking and sends queued before the pause wait (follow_ups.paused_send)
                # Only on work days: Send without asking queued for a day off waits for the next work day (follow_ups.off_day_send)
                held=(follow_ups.held_until(db,found['id'],now()) or follow_ups.paused_send(db,found['id'],now()) or follow_ups.off_day_send(db,found['id'],now(),self.follow_up_work())) if found['status']=='queued' else None
                if held:db.execute('UPDATE action_jobs SET retry_at=? WHERE id=?',(held,found['id']));continue
                job=found;break
            if not job:return
            job=dict(job);action=json.loads(job['payload'])
        if job['status'] in ('sending','uncertain'):
            # Read outside a transaction. Positive Sent-mail identity recovers an
            # interrupted send; no-match/ambiguity never permits resending.
            try:result=transport.reconcile(action,job)
            except Exception:result={}
            with self.store.connect() as db:
                if result.get('message_id'):
                    if db.execute("UPDATE action_jobs SET status='sent',message_id=?,error=NULL,updated_at=? WHERE id=? AND status IN ('sending','uncertain')",(result['message_id'],now(),job['id'])).rowcount and action['kind'] in VERIFIED_KINDS:
                        note_first(db,'first_verified_action',action['kind'])  # the provider confirmed it (first_cards_report)
                    queue_thread_snooze(db,action,job);queue_delegate_wait(db,action,job,result);self.handoff_mail.sent(db,action,job,result)
                    if action['kind']=='doc_write':settle_doc_write(self.store,db,job['suggestion_id'],job['id'],action,result.get('url'))
                    elif action['kind']!='merge':settle_sent(self.store,db,job['suggestion_id'],job['id'],next_actions.label(action),calendar_writes.done(action) if action['kind']=='calendar' else doc_writes.done(action) if action['kind']=='doc_write' else None)
                    if action['kind']=='merge' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'merge',encoded(result),'pending',now()))
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                else:
                    # Keep checking Sent mail, every five minutes for a day, then hourly.
                    wait=dt.timedelta(minutes=5 if dt.datetime.fromisoformat(job['created_at'])>dt.datetime.fromisoformat(now())-dt.timedelta(days=1) else 60)
                    db.execute("UPDATE action_jobs SET status='uncertain',error=?,retry_at=? WHERE id=? AND status IN ('sending','uncertain')",('I couldn’t confirm whether the fix was merged. I’m checking the code; I won’t merge it again.' if action['kind']=='merge' else doc_writes.UNCLEAR if action['kind']=='doc_write' else 'I couldn’t confirm the calendar change. I’m checking the calendar; I won’t make it twice.' if action['kind']=='calendar' else 'I couldn’t confirm whether this X '+('reply' if action.get('reply_to') else 'message')+' was sent. I’m checking X; I won’t send it again.' if action['kind']=='x' else 'I couldn’t confirm whether this WhatsApp message was sent. I’m checking the chat; I won’t send it again.' if action['kind']=='whatsapp' else 'I couldn’t confirm whether this Telegram message was sent. I’m checking the chat; I won’t send it again.' if action['kind']=='telegram' else 'I couldn’t confirm whether this Intercom reply was sent. I’m checking the conversation; I won’t send it again.' if action['kind']=='intercom' else 'I couldn’t confirm whether this doc reply was posted. I’m checking the comment; I won’t post it again.' if action['kind']=='doc_reply' else 'I couldn’t confirm whether this '+('LinkedIn' if action['kind']=='linkedin' else 'Slack')+' message was sent. I’m checking the conversation; I won’t send it again.' if action['kind'] in ('linkedin','slack') else 'I couldn’t confirm whether this email was sent. I’m checking Sent mail; I won’t send it again.',(dt.datetime.fromisoformat(now())+wait).isoformat(),job['id']))
            if result.get('message_id') and action['kind']=='merge':
                self.merge_effect(job,action,result,'merge',transport.pick(action) if hasattr(transport,'pick') else transport)
            return
        try:transport.preflight(action)
        except next_actions.LinkedInBusy:
            # The shared browser is in use: wait, nothing was sent and the approval stands.
            with self.store.connect() as db:
                db.execute("UPDATE action_jobs SET retry_at=?,updated_at=? WHERE id=? AND status='queued'",((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=2)).isoformat(),now(),job['id']))
            return 'waiting'
        except Exception as error:
            reason=str(error) if isinstance(error,ValueError) else 'The fix could not be checked. Nothing was merged.' if action['kind']=='merge' else 'The doc could not be checked. Nothing was changed.' if action['kind']=='doc_write' else 'The calendar could not be checked. Nothing was changed.' if action['kind']=='calendar' else ({'linkedin':'LinkedIn','slack':'Slack','x':'X','whatsapp':'WhatsApp','telegram':'Telegram','intercom':'Intercom','doc_reply':'The doc'}.get(action['kind'],mailbox_name(self.config,action))+' could not be checked. Nothing was sent.')
            with self.store.connect() as db:
                stamp=now()
                if db.execute("UPDATE action_jobs SET status='blocked',error=?,updated_at=? WHERE id=? AND status='queued'",(reason,stamp,job['id'])).rowcount:
                    activity_log.note_block(db,job['id'],reason,stamp)  # Activity keeps the block as history (activity_log.py)
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
            return 'blocked'
        # An automated follow-up: the thread read again, right before it goes; anything new since the draft holds it (follow_ups.py)
        recheck=self.follow_up_recheck(job,action)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            current=db.execute("SELECT j.status,s.status suggestion_status,s.next_action FROM action_jobs j JOIN suggestions s ON s.id=j.suggestion_id WHERE j.id=?",(job['id'],)).fetchone()
            if not current or current['status']!='queued':return
            if current['suggestion_status']!='prepared' or not next_actions.selected(current['next_action'],job['revision']):
                db.execute("UPDATE action_jobs SET status='cancelled' WHERE id=?",(job['id'],));return
            if recheck and recheck[0]=='bounced':
                follow_ups.hold_bounced(db,job,current['next_action'],recheck[1],now())
                follow_ups.settle(db,now(),self.follow_up_mine())  # no working address: the draft stops ("Email bounced")
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                return 'held'
            if recheck and recheck[0]:
                follow_ups.hold(db,job['id'],job['suggestion_id'],recheck[0],recheck[1],now())
                follow_ups.settle(db,now(),self.follow_up_mine())  # a reply ends the round; the owner's own send counts as this one
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
                return 'held'
            if recheck:follow_ups.unhold(db,job['id'])
            # Commit admission before the one write. Later cancellation cannot recall
            # an admitted email, and restart/repeated clicks only reconcile it.
            if action['kind'] in ('whatsapp', 'intercom'):
                action.setdefault('proof', {})[action['kind'] + '_dispatched_at'] = now()
            held=follow_ups.held_until(db,job['id'],now())
            if held:
                db.execute('UPDATE action_jobs SET retry_at=? WHERE id=?',(held,job['id']));return 'waiting'
            db.execute("UPDATE action_jobs SET status='sending',updated_at=?,retry_at=? WHERE id=?",(now(),(dt.datetime.fromisoformat(now())+dt.timedelta(seconds=90)).isoformat(),job['id']))
            follow_ups.going_out(db,job['id'],now())  # claimed with the send: the next follow-up from this account waits, also after a restart
            if action.get('proof'):db.execute('UPDATE action_jobs SET payload=? WHERE id=?',(encoded(action),job['id']))
        try:result=transport.send(action,job)
        except Exception:result={}
        if result.get('not_sent'):
            with self.store.connect() as db:
                db.execute("UPDATE action_jobs SET status='queued',retry_at=?,updated_at=? WHERE id=? AND status='sending'",((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=2)).isoformat(),now(),job['id']))
            return 'waiting'
        with self.store.connect() as db:
            status='sent' if result.get('message_id') else 'failed' if result.get('rejected') else 'uncertain'
            what,where={'linkedin':('this LinkedIn message','LinkedIn'),'slack':('this Slack message','Slack'),'x':('this X '+('reply' if action.get('reply_to') else 'message'),'X'),'whatsapp':('this WhatsApp message','WhatsApp'),'telegram':('this Telegram message','Telegram'),'intercom':('this Intercom reply','Intercom'),'doc_reply':('this doc reply','The doc')}.get(action['kind'],('this email',mailbox_name(self.config,action)))
            error={'sent':None,'failed':f"Last attempt failed: {where} refused {what} (error {result.get('rejected')}). Nothing was sent; change it or try again.",
                   'uncertain':f'I couldn’t confirm whether {what} was sent. I won’t resend it.'}[status]
            if action['kind']=='doc_write':
                error={'sent':None,'failed':doc_writes.failed(action,result.get('rejected'),result.get('reason')),'uncertain':doc_writes.UNCLEAR}[status]
            if action['kind']=='calendar':
                error={'sent':None,'failed':f"Last attempt failed: Google Calendar refused it (error {result.get('rejected')}). Nothing was changed; try again or change it.",
                       'uncertain':'I couldn’t confirm the calendar change. I’m checking the calendar; I won’t make it twice.'}[status]
            if action['kind']=='merge':
                error={'sent':' '.join(note for note in ('Pushing it failed; push it yourself.' if result.get('pushed') is False else
                                                           'Kept on this machine, not pushed upstream: push it or open a pull request if you want to share it.' if result.get('held')=='auto' else
                                                           'Not pushed: earlier changes here aren’t upstream yet, so push them together when you’re ready.' if result.get('held')=='unshared' else '',
                                                           '' if result.get('restarted') else 'Restart The Machine to use it.') if note) or None,
                       'failed':'The fix no longer applies to the running code. Nothing was merged; tap Change to redo it.',
                       'uncertain':'I couldn’t confirm whether the fix was merged. I won’t merge it again.'}[status]
            db.execute('UPDATE action_jobs SET status=?,message_id=?,error=?,updated_at=?,retry_at=?,rfc_message_id=COALESCE(?,rfc_message_id) WHERE id=?',
                (status,result.get('message_id'),error,now(),None if status=='failed' else (dt.datetime.fromisoformat(now())+dt.timedelta(minutes=5)).isoformat(),
                 result.get('rfc_message_id') if status=='sent' else None,job['id']))
            if status=='sent':
                if action['kind'] in VERIFIED_KINDS:note_first(db,'first_verified_action',action['kind'])  # the provider accepted it (first_cards_report)
                queue_thread_snooze(db,action,job);queue_delegate_wait(db,action,job,result);self.handoff_mail.sent(db,action,job,result)
                if action['kind']=='doc_write':settle_doc_write(self.store,db,job['suggestion_id'],job['id'],action,result.get('url'))
                elif action['kind']!='merge':settle_sent(self.store,db,job['suggestion_id'],job['id'],next_actions.label(action),calendar_writes.done(action) if action['kind']=='calendar' else doc_writes.done(action) if action['kind']=='doc_write' else None)
            if status=='sent' and action['kind']=='merge' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'merge',encoded(result),'pending',now()))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
        if status=='sent' and action['kind']=='merge':
            self.merge_effect(job,action,result,'merge',transport.pick(action) if hasattr(transport,'pick') else transport)
        return status

    def merge_effect(self,job,action,receipt,operation,merge):
        """Durable receipt precedes optional effects; recovery never repeats a Git mutation."""
        if not hasattr(merge,'complete'):return
        with self.store.connect() as db:
            db.execute('INSERT INTO merge_effects VALUES(?,?,?,?,?) ON CONFLICT(action_id,operation) DO NOTHING',
                       (job['id'],operation,encoded(receipt),'pending',now()))
        with self.store.connect() as db:
            saved=db.execute('SELECT receipt,status FROM merge_effects WHERE action_id=? AND operation=?',(job['id'],operation)).fetchone()
        if saved['status']=='done':return
        receipt=json.loads(saved['receipt'])
        result=merge.complete(action,receipt,operation)
        with self.store.connect() as db:
            db.execute("UPDATE merge_effects SET status='done',receipt=?,updated_at=? WHERE action_id=? AND operation=?",(encoded({**receipt,**result}),now(),job['id'],operation))
            redone=parked_redo(db,job['suggestion_id']) if operation=='merge' else None
        if redone:parked_fixes.drop(next_actions.app_dir(self.config),redone['commit'])  # its redo is in: the set-aside fix goes
        # Both the Git outcome and push bookkeeping are durable BEFORE restart is requested.
        result['restarted']=bool(result.get('activation_ready') and merge.restart and merge.restart())
        notes=[]
        if result.get('pushed') is False:notes.append('Pushing it failed; push it yourself.')
        elif result.get('held')=='auto':notes.append('Kept on this machine, not pushed upstream: push it or open a pull request if you want to share it.')
        elif result.get('held')=='unshared':notes.append('Not pushed: earlier changes here aren’t upstream yet, so push them together when you’re ready.')
        if not result.get('restarted'):notes.append('Restart The Machine to use '+('the previous code.' if operation=='undo' else 'it.'))
        with self.store.connect() as db:
            db.execute("UPDATE merge_effects SET receipt=?,updated_at=? WHERE action_id=? AND operation=?",(encoded({**receipt,**result}),now(),job['id'],operation))
            prior=(job.get('error') or 'Merge undone.') if operation=='undo' else None
            if operation=='undo' and result.get('restarted'):prior+=' The Machine restarts on the previous code.'
            db.execute('UPDATE action_jobs SET error=? WHERE id=?',(' '.join(([prior] if prior else [])+notes) or None,job['id']))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))

    def merge_effect_step(self):
        with self.store.connect() as db:
            row=db.execute("SELECT j.*,e.operation,e.receipt FROM merge_effects e JOIN action_jobs j ON j.id=e.action_id WHERE e.status='pending' LIMIT 1").fetchone()
        if row:
            job=dict(row);self.merge_effect(job,json.loads(job['payload']),json.loads(job['receipt']),job['operation'],next_actions.MergeTransport(self.config,restart_self))

    def action_worker(self):
        promised = styled = followed = handled = 0
        while not self.stop.wait(3):
            if time.monotonic() - promised >= 60:
                promised = time.monotonic()
                try:self.promise_step()
                except Exception as error:loop_failed(LOG,'promise check',error)
            if time.monotonic() - handled >= 300:
                handled = time.monotonic()
                try:self.handled_step()  # open to-dos newer messages show done already (handled_check.py)
                except Exception as error:LOG.error('handled check error=%s',type(error).__name__)
            if time.monotonic() - styled >= 600:
                styled = time.monotonic()
                try:self.style_step()
                except Exception as error:LOG.error('style learning error=%s',type(error).__name__)
            if time.monotonic() - followed >= 300:
                followed = time.monotonic()
                try:self.bounce_step()  # before follow-ups: a bounced address gets none by email
                except Exception as error:LOG.error('bounce check error=%s',type(error).__name__)
                try:self.follow_up_step()
                except Exception as error:LOG.error('follow-up error=%s',type(error).__name__)
            try:self.action_step()
            except Exception as error:loop_failed(LOG,'approved action',error)
            try:self.undo_step()
            except Exception as error:LOG.error('undo merge error=%s',type(error).__name__)
            try:self.merge_effect_step()
            except Exception as error:LOG.error('merge effects error=%s',type(error).__name__)
            try:self.thread_snooze_step()
            except Exception as error:LOG.error('thread snooze error=%s',type(error).__name__)

    def undo_step(self,merge=None):
        """Undo merged fixes: the owner's Undo, or a fix merged by itself that misbehaves."""
        for suggestion_id,reason in self.store.misbehaving_merges():
            self.store.undo_merge(suggestion_id,'auto-undo:'+uuid.uuid4().hex,'assistant',reason)
        with self.store.connect() as db:
            job=db.execute("SELECT * FROM action_jobs WHERE status='undoing' ORDER BY updated_at LIMIT 1").fetchone()
        if not job:return
        merge=merge or next_actions.MergeTransport(self.config,restart_self)
        try:
            result=merge.revert(json.loads(job['payload']))
            note=job['error'] or 'Merge undone.'
            status='undone'
        except ValueError as error:
            note,status=str(error),'sent'
        with self.store.connect() as db:
            # A failed undo leaves the fix merged and says why; the card keeps its Undo.
            db.execute('UPDATE action_jobs SET status=?,error=? WHERE id=?',(status,note,job['id']))
            if status=='undone' and result.get('commit'):db.execute('INSERT OR IGNORE INTO merge_effects VALUES(?,?,?,?,?)',(job['id'],'undo',encoded(result),'pending',now()))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(job['suggestion_id'],))
        if status=='undone':self.merge_effect(dict(job),json.loads(job['payload']),result,'undo',merge)
        return status

    def stop_stale_runs(self, runner, limit=5):
        """Canceled, replaced or finished runs live on in their Gateway session until stopped. Stop and
        confirm each exact old run; only work in that same session or card waits for it. One round at a time: the
        Browser view's Stop starts one at once, beside the worker's."""
        with self.__dict__.setdefault('stale_lock', threading.Lock()):
            self._stop_stale_runs(runner, limit)

    def _stop_stale_runs(self, runner, limit):
        with self.store.connect() as db:
            stale=db.execute("""SELECT r.*,p.status prep_status,p.error prep_error,p.reason prep_reason,p.updated_at prep_updated
                FROM preparation_runs r LEFT JOIN preparations p ON p.job_id=r.job_id
                WHERE r.finished_at IS NULL AND (p.job_id IS NULL OR p.status NOT IN ('starting','running'))
                AND (r.retry_at IS NULL OR r.retry_at<=?) ORDER BY r.started_at LIMIT ?""",(now(),limit)).fetchall()
        for run in stale:
            # Its own result or blocker is saved (not replaced, canceled or timed out): the run normally ends by itself
            # seconds later. Read how it ended; stop it only when it is still going after PREPARATION_SETTLE_SECONDS.
            # Also one whose preparation was canceled after its blocker was saved (reason kept: settle_ahead before it kept
            # the blocker): that run finished by itself too, so it is never stopped and recorded as lost.
            saved=run['prep_status'] in ('done','blocked') or run['prep_status']=='cancelled' and bool((run['prep_reason'] or '').strip())
            if saved and run['prep_error'] not in ('completion_unconfirmed','stopped'):  # stopped: the chat's Stop, at once
                outcome=runner({'action':'status','job_id':run['job_id'],'session_job_id':run['session_job_id']})
                if outcome.get('status') in preparation_state.TERMINAL:
                    with self.store.connect() as db:
                        db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE job_id=? AND finished_at IS NULL',(outcome['status'],now(),run['job_id']))
                    continue
                settled=dt.datetime.fromisoformat(run['prep_updated'] or run['started_at'])
                if (dt.datetime.fromisoformat(now())-settled).total_seconds()<PREPARATION_SETTLE_SECONDS:
                    with self.store.connect() as db:
                        db.execute('UPDATE preparation_runs SET retry_at=? WHERE job_id=?',((dt.datetime.fromisoformat(now())+dt.timedelta(seconds=10)).isoformat(),run['job_id']))
                    continue
            outcome=runner({'action':'stop','job_id':run['job_id'],'session_job_id':run['session_job_id']})
            with self.store.connect() as db:
                if outcome.get('status') not in preparation_state.TERMINAL:
                    db.execute('UPDATE preparation_runs SET retry_at=? WHERE job_id=?',((dt.datetime.fromisoformat(now())+dt.timedelta(minutes=1)).isoformat(),run['job_id']))
                    continue
                db.execute('UPDATE preparation_runs SET status=?,finished_at=? WHERE job_id=?',(outcome['status'],now(),run['job_id']))
                # A run that timed out without confirmation gets its one automatic retry once it has really ended. Not on a
                # to-do waiting for the owner (a prepared-ahead one settle_ahead sent out): their Try again starts it.
                retried=db.execute("""UPDATE preparations SET job_id=?,status='queued',reason=NULL,details=NULL,retry_at=NULL,updated_at=?,
                    auto_retries=auto_retries+1,started_at=NULL WHERE job_id=? AND status='blocked' AND error='completion_unconfirmed' AND auto_retries=0
                    AND suggestion_id IN (SELECT id FROM suggestions WHERE status IN ('accepted','instructions'))""",
                    (uuid.uuid4().hex,now(),run['job_id'])).rowcount
                if retried:
                    db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(run['suggestion_id'],))

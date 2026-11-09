"""Feedback on a to-do through the owner's Telegram chat (App.action): asking for it, binding the prompt to its message,
and the owner's reply, read from the bridge's own cached message identities only. Moved out of assistant.App's action
as is. A mixin of assistant.App (APP_MIXINS)."""
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import threading
import time

import i18n
from machine.config import LOG, ROOT
from machine.delivery.telegram import DeliveryNotSent, telegram_request
from machine.model_usage import node_bin, node_env, telegram_account, telegram_on
from machine.text import encoded
from timeutil import now


def prompt_text(title,plain=False,kind='change'):
    t = i18n.t  # “cancel” stays the word the reply handler takes, in every language
    if kind=='dismiss':
        if plain:return t('Why isn’t this needed? Reply to this message. Send “cancel” to keep it.')
        return t('Not needed: {}', title[:90])+'\n\n'+t('Why isn’t this needed? Reply here, or send “cancel” to keep it.')
    if plain:return t('What would you like instead? Reply to this message. Send “cancel” to stop.')
    return t('Change: {}', title[:90])+'\n\n'+t('What would you like instead? Reply here, or send “cancel”.')


# How long after the owner's message in their own chat a fact can be saved from it: the turn that answers it, not a
# later one that started by itself.
OWNER_SAID_MINUTES = 30


class FeedbackApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'request_feedback': 'request_feedback_action', 'bind_feedback_prompt': 'bind_feedback_prompt_action',
               'feedback_reply': 'feedback_reply_action'}

    def request_feedback_action(self, name, args, owner_dashboard=False):
        # Read only native cached message identities in this exact owner
        # chat. The bot receipt fences delayed/queued dispatch safely.
        boundary=None
        try:
            with sqlite3.connect('file:'+str(Path.home()/'.openclaw/state/openclaw.sqlite')+'?mode=ro',uri=True,timeout=2) as native:
                rows=native.execute("SELECT value_json FROM plugin_state_entries WHERE plugin_id='telegram' AND namespace='telegram.message-cache'").fetchall()
                ids=[]
                for value, in rows:
                    message=json.loads(value).get('sourceMessage',{})
                    if str(message.get('chat',{}).get('id'))==self.config.get('telegram_owner') and message.get('message_id'):
                        ids.append(int(message['message_id']))
                boundary=str(max(ids)) if ids else None
        except (sqlite3.Error,ValueError,TypeError):
            pass
        requested=self.store.request_feedback(args['suggestion_id'],args['request_id'],boundary,args.get('card_message_id'),managed=args.get('managed_prompt') is True,kind=args.get('kind') or 'change')
        if args.get('defer_prompt'):
            return requested
        dispatch=False
        with self.store.connect() as db:
            row=db.execute('SELECT * FROM suggestions WHERE id=?',(args['suggestion_id'],)).fetchone()
            if row and row['feedback_request_id']==args['request_id'] and not row['feedback_prompt_message_id'] and row['feedback_until'] and row['feedback_until']>now():
                # Older bridge generations can ask for a fallback after an unknown
                # native send. Never equate that with permission to send again.
                status='queued' if args.get('managed_prompt') and not requested.get('duplicate') else 'uncertain'
                db.execute('INSERT OR IGNORE INTO feedback_prompts(request_id,suggestion_id,card_id,title,status,created_at,updated_at,error) VALUES(?,?,?,?,?,?,?,?)',
                    (args['request_id'],row['id'],str(args.get('card_message_id') or ''),row['title'],status,now(),now(),None if status=='queued' else 'legacy_prompt_unconfirmed'))
                if status=='queued' and self.config.get('delivery_enabled') and hasattr(self,'stop'):
                    # Send now rather than on the next 10-second delivery tick. The step's
                    # own admission makes a concurrent delivery-worker pass a no-op.
                    dispatch=True
            # A second tap while an earlier prompt is unconfirmed reuses it silently;
            # tell the plugin so Telegram can say so instead of doing nothing.
            earlier=db.execute('SELECT p.status FROM suggestions s JOIN feedback_prompts p ON p.request_id=s.feedback_request_id WHERE s.id=? AND s.feedback_request_id!=?',
                               (args['suggestion_id'],args['request_id'])).fetchone() if row else None
        if dispatch:
            threading.Thread(target=self.feedback_prompt_safe,kwargs={'request_id':args['request_id']},daemon=True).start()
        return {'awaiting_feedback':True,'duplicate':True,'prompt_managed':True,**({'earlier_prompt':earlier['status']} if earlier else {})}

    def bind_feedback_prompt_action(self, name, args, owner_dashboard=False):
        self.store.bind_feedback_prompt(args['suggestion_id'],args['request_id'],args['message_id'])
        return {'bound':True}

    def feedback_reply_action(self, name, args, owner_dashboard=False):
        timestamp=args.get('timestamp');reply_to=args.get('reply_to_id')
        # Older running bridge generations lack these fields. Recover
        # only this exact native owner message, not transcript heuristics.
        if timestamp is None or reply_to is None:
            try:
                with sqlite3.connect('file:'+str(Path.home()/'.openclaw/state/openclaw.sqlite')+'?mode=ro',uri=True,timeout=2) as native:
                    for value, in native.execute("SELECT value_json FROM plugin_state_entries WHERE plugin_id='telegram' AND namespace='telegram.message-cache' AND entry_key LIKE ?",('%:'+self.config.get('telegram_owner')+':'+str(args['message_id']),)):
                        message=json.loads(value).get('sourceMessage',{})
                        if str(message.get('chat',{}).get('id'))==self.config.get('telegram_owner') and str(message.get('from',{}).get('id'))==self.config.get('telegram_owner') and str(message.get('message_id'))==str(args['message_id']):
                            timestamp=timestamp if timestamp is not None else message.get('date')
                            reply_to=reply_to or message.get('reply_to_message',{}).get('message_id')
            except (sqlite3.Error,ValueError,TypeError):
                pass
        result=self.store.feedback_reply(args['text'],args['message_id'],timestamp,reply_to)
        if result.get('handled') and not result.get('cancelled'):
            result.update(duplicate=True,card_confirmation_only=True)
        if not result.get('handled') and str(args.get('text') or '').strip() and not str(args['text']).startswith('/'):
            # Not about a to-do: something the owner wrote in their own chat. Its id and when, in memory only (the words
            # are kept nowhere), so a fact they state there can be saved from it (owner_said, remember_fact_action).
            self.owner_said_last = (str(args['message_id']), time.time())
        return result

    def owner_said(self):
        """The note id of the owner's last message in their own private chat ('telegram-said:<message id>'), while it is
        at most OWNER_SAID_MINUTES old; None otherwise. Only feedback_reply sets it, which takes the owner key."""
        message_id, at = getattr(self, 'owner_said_last', None) or (None, 0)
        return 'telegram-said:' + message_id if message_id and 0 <= time.time() - at <= OWNER_SAID_MINUTES * 60 else None

    def feedback_prompt_step(self, request_id=None, sender=None):
        """Durable prompt admission, receipt recovery and conservative ambiguous-send hold."""
        sender=sender or self.native_change_prompt
        stamp=now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not telegram_on(self.config):
                # No Telegram chat to ask in: the dashboard takes the change request itself.
                db.execute("UPDATE feedback_prompts SET status='cancelled' WHERE status NOT IN ('sent','cancelled')")
                return
            db.execute("UPDATE feedback_prompts SET status='cancelled' WHERE status!='sent' AND NOT EXISTS(SELECT 1 FROM suggestions s WHERE s.id=feedback_prompts.suggestion_id AND s.feedback_request_id=feedback_prompts.request_id AND s.feedback_until>? AND s.status NOT IN ('completed','rejected') AND (feedback_prompts.kind='dismiss' OR s.status!='snoozed'))",(stamp,))
            row=db.execute("SELECT * FROM feedback_prompts WHERE status NOT IN ('sent','cancelled') AND (retry_at IS NULL OR retry_at<=?)"+(' AND request_id=?' if request_id else '')+' ORDER BY created_at LIMIT 1', (stamp,request_id) if request_id else (stamp,)).fetchone()
            if not row:return
            row=dict(row)
            if row['status'] in ('native_sending','plain_sending') and row['updated_at']>(dt.datetime.fromisoformat(stamp)-dt.timedelta(seconds=75)).isoformat() and not self.prompt_receipt_file(row):return
            if row['retry_at'] and row['retry_at']>stamp:return
            if row['status'] in ('uncertain','native_sending','plain_sending'):
                # No receipt is not proof of non-delivery. Only positive evidence binds.
                message_id=self.recovered_prompt_receipt(row)
                if message_id:
                    db.execute("UPDATE feedback_prompts SET status='sent',message_id=?,error=NULL,updated_at=? WHERE request_id=?",(message_id,stamp,row['request_id']))
                    db.execute('UPDATE suggestions SET feedback_prompt_message_id=? WHERE id=? AND feedback_request_id=? AND feedback_until>?',
                        (message_id,row['suggestion_id'],row['request_id'],stamp))
                else:db.execute("UPDATE feedback_prompts SET status='uncertain',error='prompt_outcome_unknown',retry_at=? WHERE request_id=?",
                    ((dt.datetime.fromisoformat(stamp)+dt.timedelta(seconds=30)).isoformat(),row['request_id']))
                return
            if row['status']=='queued' and hasattr(self,'stop') and self.stop.is_set():return
            mode='plain' if row['status']=='plain_queued' else 'native'
            db.execute('UPDATE feedback_prompts SET status=?,updated_at=?,attempted_at=? WHERE request_id=?',
                       (mode+'_sending',stamp,stamp,row['request_id']))
        result=None
        try:
            if mode=='native':result=sender(row)
            else:result=telegram_request(self.config,{'action':'send','channel':'telegram','accountId':telegram_account(self.config),'target':self.config.get('telegram_owner'),
                'message':prompt_text(row['title'],plain=True,kind=row.get('kind') or 'change'),'replyTo':row['card_id']})
        except DeliveryNotSent:
            result={'definitely_not_sent':True}
        except (ValueError,OSError,subprocess.TimeoutExpired):
            result={}
        if result and re.fullmatch(r'\d+',str(result.get('messageId',''))):
            self.save_prompt_receipt(row,str(result['messageId']))
            self.store.bind_feedback_prompt(row['suggestion_id'],row['request_id'],result['messageId'])
            return 'sent'
        with self.store.connect() as db:
            # Plain fallback is safe only when native setup never entered send.
            status='plain_queued' if result and result.get('definitely_not_sent') else 'uncertain'
            db.execute('UPDATE feedback_prompts SET status=?,error=?,retry_at=?,updated_at=? WHERE request_id=? AND status=?',
                (status,'prompt_not_sent' if status=='plain_queued' else 'prompt_outcome_unknown',
                 (dt.datetime.fromisoformat(stamp)+dt.timedelta(seconds=10 if mode=='native' and status=='plain_queued' else 60)).isoformat(),now(),row['request_id'],mode+'_sending'))
        return status

    def recovered_prompt_receipt(self,row):
        message_id=self.prompt_receipt_file(row)
        if message_id:return message_id
        path=self.config.get('openclaw_state',str(Path.home()/'.openclaw/state/openclaw.sqlite'))
        try:
            with contextlib.closing(sqlite3.connect('file:'+path+'?mode=ro',uri=True,timeout=2)) as native:
                found=set()
                for value, in native.execute("SELECT value_json FROM plugin_state_entries WHERE plugin_id='telegram' AND namespace='telegram.message-cache'"):
                    msg=json.loads(value).get('sourceMessage',{})
                    if (str(msg.get('chat',{}).get('id'))!=self.config.get('telegram_owner') or not msg.get('from',{}).get('is_bot')
                        or not msg.get('message_id') or (msg.get('date') or 0)<int(dt.datetime.fromisoformat(row.get('attempted_at') or row['created_at']).timestamp())
                        or str(msg.get('reply_to_message',{}).get('message_id'))!=row['card_id']):continue
                    if msg.get('text') in (prompt_text(row['title'],kind=row.get('kind') or 'change'),prompt_text(row['title'],plain=True,kind=row.get('kind') or 'change')):found.add(str(msg['message_id']))
                if len(found)==1:return found.pop()
        except (sqlite3.Error,OSError,ValueError):pass
        return None

    def native_change_prompt(self,row):
        request={'receipt_key':hashlib.sha256(row['request_id'].encode()).hexdigest(),'card_id':row['card_id'],'text':prompt_text(row['title'],kind=row.get('kind') or 'change'),
                 'target':str(self.config.get('telegram_owner'))}
        try:
            env={**node_env(self.config),'ASSISTANT_PROMPT_RECEIPTS':os.path.abspath(self.prompt_receipt_dir())}  # where receipts go: the service's, never the request's
            result=subprocess.run([node_bin(self.config),str(ROOT/'change-prompt-run.mjs')],env=env,input=encoded(request),capture_output=True,text=True,timeout=60)
            reply=json.loads(result.stdout)
            if reply.get('definitely_not_sent'):
                # e.g. OpenClaw helpers removed or renamed by an update: visible, then the plain prompt.
                LOG.warning('native Change prompt unavailable; using plain prompt')
            return reply
        except OSError:return {'definitely_not_sent':True}
        except (ValueError,subprocess.TimeoutExpired):return {}

    def feedback_prompt_safe(self,request_id=None):
        try:self.feedback_prompt_step(request_id=request_id)
        except Exception as error:LOG.error('Change prompt delivery error=%s',type(error).__name__)

    def prompt_receipt_dir(self):
        return Path(self.config.get('prompt_receipts',str(Path.home()/'.local/share/personal-assistant/prompt-receipts')))

    def save_prompt_receipt(self,row,message_id):
        folder=self.prompt_receipt_dir()
        folder.mkdir(parents=True,exist_ok=True,mode=0o700)
        dest=folder/(hashlib.sha256(row['request_id'].encode()).hexdigest()+'.json')
        temp=dest.with_suffix('.tmp')
        with temp.open('w') as stream:
            os.chmod(temp,0o600);json.dump({'messageId':message_id},stream);stream.flush();os.fsync(stream.fileno())
        temp.replace(dest)

    def prompt_receipt_file(self,row):
        folder=self.prompt_receipt_dir()
        path=folder/(hashlib.sha256(row['request_id'].encode()).hexdigest()+'.json')
        try:
            receipt=json.loads(path.read_text())
            if re.fullmatch(r'\d+',str(receipt.get('messageId',''))):return str(receipt['messageId'])
        except (OSError,ValueError):pass
        return None

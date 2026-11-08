"""Feedback on a to-do through the owner's Telegram chat (App.action): asking for it, binding the prompt to its message,
and the owner's reply, read from the bridge's own cached message identities only. Moved out of assistant.App's action
as is. A mixin of assistant.App (APP_MIXINS)."""
import json
from pathlib import Path
import sqlite3
import threading

from timeutil import now


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
        return result

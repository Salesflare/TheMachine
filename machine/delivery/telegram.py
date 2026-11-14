"""Telegram delivery: a to-do's message and its buttons (telegram), the calls to the Telegram bot (telegram_request),
and the Fleet's messages (fleet_telegram). Moved out of assistant.py as is."""
import json
import re
import subprocess
import uuid

import i18n
from machine.cards import ask_blocked, card, card_draft, controls
from machine.config import ROOT
from machine.delivery.push import QUICK, QUICK_LABELS, QUICK_OPENS, quick_kind, strip_result_links
from machine.model_usage import node_bin, node_env, telegram_account, telegram_on
from machine.text import encoded
import notify
from machine import todo_states


# A result notice's quick buttons as the plugin's callbacks: only these two run from the notice itself
TELEGRAM_QUICK = {'snooze2h': 'snooze_2h', 'done': 'complete'}


class DeliveryNotSent(ValueError):
    """Only the pinned helper's pre-invocation failures are retryable."""


def fleet_telegram(config, message, message_id=None, request=None):
    """The Telegram message for Fleet questions (fleet.telegram_message), sent or brought up to date. Owner chat only."""
    escape = lambda text: re.sub(r'([\\`*_{}\[\]()#+.!>|~-])', r'\\\1', text)
    blocks = [{'type': 'buttons', 'buttons': [{'label': b['text'], 'action': {'type': 'url', 'url': b['url']} if b.get('url') else
                                               {'type': 'callback', 'value': b['value']}} for b in row]} for row in message['buttons']]
    args = {'action': 'edit' if message_id else 'send', 'channel': 'telegram', 'accountId': telegram_account(config),
            'target': config.get('telegram_owner'), 'message': escape(message['text']),
            'presentation': {'blocks': blocks or [{'type': 'buttons', 'buttons': []}]}}
    if message_id:
        args['messageId'] = str(message_id)
    return (request or telegram_request)(config, args)


def telegram(config, row, action, message_id=None):
    if action=='send' and row.get('_result_notice'):
        title=re.sub(r'([\\`*_{}\[\]()#+.!>|~-])',r'\\\1',row['title'])
        ready=row['status']=='prepared'
        root='https://'+config['dashboard_host']+config.get('dashboard_path','/')
        signin=not ready and (row.get('preparation_browser') or {}).get('signin_url')
        lead=row.get('_lead','Ready') if ready else 'Needs you to sign in' if signin else 'Needs your help' if ask_blocked(row) or (row.get('preparation_browser') and not row.get('preparation_error')) else 'Stuck'
        message=i18n.t(lead+': {}', '**'+title+'**') if lead else '**'+title+'**'
        message+='\n\n['+(i18n.t('View result') if ready else i18n.t('View task'))+']('+notify.todo_link(root,row['id'])+')'  # the to-do in the list, not its chat
        # A sign-in blocker opens the dashboard's sign-in for this task; once in, the task carries on by itself.
        # Its quick buttons, as the phone's (push.QUICK): the first opens (the draft, the sign-in), the second is a
        # Snooze (2 hours) or Mark done the plugin takes from this message too (openclaw-plugin/index.ts, notice taps).
        blocks=[{'type':'buttons','buttons':[{'label':i18n.t(QUICK_LABELS[a]),'action':{'type':'url','url':signin or notify.todo_link(root,row['id'])}} if a in QUICK_OPENS
                                             else {'label':i18n.t(QUICK_LABELS[a]),'action':{'type':'callback','value':f"assistant:{row['id']}:{TELEGRAM_QUICK[a]}"}}
                                             for a in QUICK[quick_kind(row,'result',not ready,signin)]['web'] if a in QUICK_OPENS or a in TELEGRAM_QUICK]}]
        return telegram_request(config,{'action':'send','channel':'telegram','accountId':telegram_account(config),
            'target':config.get('telegram_owner'),**({} if str(row['message_id']).startswith('web-') else {'replyTo':str(row['message_id'])}),
            'message':message,'presentation':{'blocks':blocks},**({'silent':True} if row.get('_silent') else {})})
    body=dict(row)
    if row['status']=='prepared' and row.get('requested_feedback'):
        asked=re.sub(r'([\\`*_{}\[\]()#+.!>|~-])',r'\\\1',row['requested_feedback'][:500])
        body['body']=i18n.t('You asked: “{}”', asked)+'\n\n'+body['body']
    if row['status']=='instructions' and row.get('preparation_status')!='blocked':
        asked=row.get('requested_feedback')
        if asked:
            asked=re.sub(r'([\\`*_{}\[\]()#+.!>|~-])',r'\\\1',asked[:500])
            body['body']=i18n.t('You asked: “{}”', asked)+'\n\n'+i18n.t('Got it. I’m preparing your update. I’ll send it here when it’s ready.')
        else:body['body']=i18n.t('Got it. I’m preparing your update. I’ll send it here when it’s ready.')
    root='https://'+config['dashboard_host']+config.get('dashboard_path','/') if config.get('dashboard_host') else ''
    shown=card_draft(row)
    if root:
        body['body']=strip_result_links(body['body'])
        if shown:body['body']+='\n\n'+shown['text']
        if row['status']=='prepared':body['body']+='\n\n['+i18n.t('Read result')+']('+notify.todo_link(root,row['id'])+')'
        elif row.get('original_urls'):body['body']+='\n\n['+i18n.t('Open original')+']('+row['original_urls'][0]+')'
    args = {'action':action,'channel':'telegram','accountId':telegram_account(config),'target':config.get('telegram_owner'),
            'message':(i18n.t('Your update')+'\n\n' if action=='send' and row.get('reminder') and (row['status'] in (todo_states.PREPARED, todo_states.INSTRUCTIONS) or row.get('preparation_status')=='blocked') else i18n.t('Reminder')+'\n\n' if action=='send' and row.get('reminder') else '')+card(body),'presentation':controls(row,root)}
    if message_id:
        args['messageId'] = str(message_id)
    elif row.get('_silent'):
        args['silent'] = True
    return telegram_request(config,args)


def telegram_request(config,args):
    if not telegram_on(config):
        # Telegram is off: nothing is sent, and a local receipt lets delivery, edits and
        # result notices proceed, so the dashboard and its push notifications carry the card.
        return {'messageId': 'web-' + uuid.uuid4().hex[:12]}
    if str(args.get('messageId') or '').startswith('web-'):
        return {'messageId': args['messageId']}  # a card kept off Telegram (Settings, Notifications): nothing there to edit
    try:
        result = subprocess.run([node_bin(config), str(ROOT/'telegram-message.mjs')],env=node_env(config),
                                input=encoded(args),capture_output=True,text=True,timeout=60)
    except OSError as error:
        # The helper never started, so nothing can have been sent.
        raise DeliveryNotSent('helper_unavailable:' + type(error).__name__) from None
    if result.returncode:
        try:
            failure = json.loads(result.stdout)
            if failure.get('definitely_not_sent') is True and failure.get('error') in ('gateway_preflight_failed','delivery_not_admitted'):
                raise DeliveryNotSent(failure['error'])
        except json.JSONDecodeError:
            pass
        raise ValueError('Delivery not confirmed')
    return json.loads(result.stdout)

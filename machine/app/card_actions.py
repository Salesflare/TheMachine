"""A to-do's own actions on the dashboard (App.action): preparing it, deciding on it, revising its draft, confirming an
approval, refreshing its card, files in its chat, and importing a task link, with the helpers only they use. Moved
out of assistant.App's action as is. A mixin of assistant.App (APP_MIXINS)."""
import email.utils
import json
import re
import uuid

import bounces
import chat_files
import crm_fixes
import crm_import
import doc_writes
import fleet
import follow_ups
import graph
import i18n
from machine.browser import FINAL_STEPS
from machine.cards import asked_snooze_time, owner_snooze_until, undated_card
from machine.chat import CHAT_FILES_ONLY, unseen_draft
from machine.config import LOG
from machine.delivery.push import (NOTICE_DECISION, notice_decision_refused, nudge_wait, reminder_channels,
                                   reminder_line, report_done)
from machine.sources.calendar import calendar_write_events, calendar_write_ids
from machine.sources.connectors import CONNECTOR_HELPERS, doc_comments, doc_write_files, load_connector
from machine.sources.signal_chats import owner_signal_chats
from machine.sources.telegram import owner_telegram_chats
from machine.sources.whatsapp import owner_whatsapp_chats, reply_spots
import mail_cleanup
import reading_digest
from models import model_ready
import next_actions
from machine.store import outcomes
import own_addresses
import recurring
import routine_changes
import skills
import task_invites
from timeutil import local_tz, now


# A final step that goes to someone (a message, an invite, sharing) is a send: the owner sees and approves it on the
# card. Every other step of these kinds can run on the owner's own word (do_now).
SENDING_FINISH = ('Send', 'Reply', 'Post', 'Invite', 'Share')


NOT_A_PERSON = re.compile(r'(?i)^(?:no-?reply|do-?not-?reply|mailer-daemon|postmaster|notifications?|bounces?)[@+.-]')


def doable_now(action):
    """Whether a next action can run on the owner's own word in the chat (do_now), without a Confirm: an edit to an
    existing doc, or a final step that reaches nobody (no message, no files, not a send, an invite or sharing)."""
    if action.get('kind') == doc_writes.KIND:
        return action.get('op') == 'edit'
    return (action.get('kind') == 'finish' and not any(action.get(k) for k in ('message', 'to_name', 'attachments'))
            and (str(action.get('label') or '').split() or [''])[0] not in SENDING_FINISH)


def owner_turn(db, suggestion_id, job_id):
    """The owner's own message (card chat or Change note) that started this preparation: its decision row
    (feedback, created_at), or None for a run nobody asked for in words (prepared ahead, a bare Do it, a review)."""
    job = db.execute('SELECT decision_id FROM preparations WHERE suggestion_id=? AND job_id=?', (suggestion_id, job_id)).fetchone() if job_id else None
    turn = db.execute("SELECT feedback,created_at FROM decisions WHERE id=? AND suggestion_id=? AND source IN ('dashboard','telegram') AND choice='other'",
                      (job['decision_id'], suggestion_id)).fetchone() if job else None
    return turn if turn and str(turn['feedback'] or '').strip() else None


def ask_do_now(turn, steps):
    """The question a chat turn answers before its step waits for a Confirm: the owner's message and the step side by
    side. Whether the message asked for exactly this step is the model's judgment, never a word list."""
    said = ' '.join(str(turn['feedback']).split())[:600]
    listed = '; '.join(next_actions.label(a) + ': ' + ' '.join(next_actions.preview(a).split())[:400] for a in steps)
    return ('Decide first: does the owner’s message ask for exactly this step? Their message: <<<' + said + '>>>. The step you saved '
            'for their Confirm: ' + listed + '. If their message asks for it (a fix, change or cleanup they asked for, even in passing '
            'or as a complaint that it is not done yet), their message is the OK: save again with do_now:true and it runs now, without '
            'a Confirm; the body says it is being done. If the step goes further than they asked (more changes, other people, sharing '
            'or permissions, publishing) or they only asked a question, save again with do_now:false and it waits for their Confirm.')


def reply_to_newest(rows, value):
    """A reply drafted to an older email of the thread answers its newest one (what Reply does in a mail app), so
    the draft and the to-do's source are the message it really answers. rows: the to-do's emails, newest first."""
    known = []
    for row in rows:
        try:
            m = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
        except ValueError:
            continue
        if m.get('message-id') and m.get('thread_id'):
            known.append((m['thread_id'], str(m['message-id']).strip()))
    def fix(item):
        if not isinstance(item, dict) or item.get('kind') != 'email' or not isinstance(item.get('in_reply_to'), str):
            return item
        thread = next((t for t, mid in known if mid == item['in_reply_to'].strip()), None)
        newest = next((mid for t, mid in known if t == thread), None) if thread and item.get('thread_id', thread) == thread else None
        if not newest or newest == item['in_reply_to'].strip():
            return item
        refs = str(item.get('references') or item['in_reply_to']).split()
        return {**item, 'in_reply_to': newest, 'references': ' '.join(refs + ([newest] if newest not in refs else []))}
    if isinstance(value, list):
        return [fix(x) for x in value]
    if isinstance(value, dict) and isinstance(value.get('actions'), list):
        return {**value, 'actions': [fix(x) for x in value['actions']]}
    return fix(value)


def replied_to(rows):
    """{Message-ID: {'to', 'from', 'sent', ...}} for the task's emails, newest first: who each was addressed to (To, then
    Cc) and sent from, and whether the owner sent it. A reply's default From comes from the one it answers
    (next_actions.pick_sender). With the rows' account_id, source_id and title also the mailbox it is in, its message
    and thread there, its subject and In-Reply-To: what threads a reply to it (next_actions.fill_reply, reply_origin)."""
    out = {}
    for row in rows:
        has = row.keys() if hasattr(row, 'keys') else ()
        try:
            m = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
        except ValueError:
            continue
        if not isinstance(m, dict) or not m.get('message-id'):
            continue
        get = lambda field: [a.strip().lower() for _, a in email.utils.getaddresses([str(m.get(field) or '')]) if '@' in a]
        home = {'account_id': row['account_id'] if 'account_id' in has else None, 'id': row['source_id'] if 'source_id' in has else None,
                'thread_id': m.get('thread_id')}
        found = out.setdefault(str(m['message-id']).strip(), {'to': get('to') + get('cc'), 'from': (get('from') or [''])[0],
                                                              'sent': 'SENT' in (m.get('labels') or ()), **home, 'homes': {},
                                                              'subject': row['title'] if 'title' in has else None,
                                                              'in_reply_to': m.get('in-reply-to')})
        if home['account_id']:  # the same email in two of the owner's mailboxes (both addressed): each its own thread
            found['homes'].setdefault(home['account_id'], home)
    return out


def thread_recipients(rows, own):
    """Addresses a reply could go to, from the task's own emails: Reply-To, From, To, Cc (newest first).

    A From that a Reply-To rewrites (Google Groups "via") is skipped. The owner's own and robot addresses
    are left out. These are the only addresses offered when a draft has no verified recipient."""
    own = {a.lower() for a in own}
    seen = []
    for row in rows:
        try:
            metadata = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
        except ValueError:
            continue
        fields = ['reply-to', 'to', 'cc'] if metadata.get('reply-to') else ['from', 'to', 'cc']
        for field in fields:
            for _, address in email.utils.getaddresses([str(metadata.get(field) or '')]):
                address = address.strip().lower()
                if (re.fullmatch(r'[^\s<>@,;]+@[^\s<>@,;]+\.[^\s<>@,;]+', address) and len(address) <= 254
                        and address not in own and address not in seen and not NOT_A_PERSON.match(address)):
                    seen.append(address)
    return seen[:6]


class CardActionsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'task_import': 'task_import_action', 'prepare': 'prepare_action', 'revise_draft': 'revise_draft_action',
               'confirm_action': 'confirm_action_action', 'refresh_card': 'refresh_card_action',
               'chat_upload': 'chat_upload_action', 'chat_file_remove': 'chat_upload_action', 'decide': 'decide_action',
               # CARD_ACTIONS less the repeat ones (RecurringApp)
               **dict.fromkeys(('card_new', 'card_project', 'card_rename', 'card_move', 'card_report_seen', 'card_use_sources',
                                'card_merge'), 'card_owner_action')}

    def task_import_action(self, name, args, owner_dashboard=False):
        # a task link someone sent this owner by email (task_invites.py)
        if not owner_dashboard:
            raise ValueError('Add a task link from the dashboard')
        return self.task_import(str(args.get('link') or ''))

    def prepare_action(self, name, args, owner_dashboard=False):
        with self.store.connect() as db:
            row=db.execute('SELECT account_ids,event_ids,body FROM suggestions WHERE id=?',(args['suggestion_id'],)).fetchone()
        if not row:raise ValueError('Unknown suggestion')
        # reply: the chat's answer to the owner's message; body: the card's status. A chat turn that only answered
        # leaves the status as it was, so the card never shows a chat reply as its body.
        if args.get('reply') is not None and (not isinstance(args['reply'],str) or len(args['reply'])>1000):
            raise ValueError('reply is your short answer to their message, at most 1000 characters')
        if not str(args.get('body') or '').strip():
            if not str(args.get('reply') or '').strip():raise ValueError('A concrete local preparation is required')
            args={**args,'body':row['body'] or args['reply']}
        # The card's status and title stay true on later days: "tomorrow" is saved as that day (undated_card)
        (body,title),_=undated_card(str(args['body']),args['title'] if isinstance(args.get('title'),str) else None)
        args={**args,'body':body,**({'title':title} if title is not None else {})}
        if args.get('next_action') and args.get('next_actions'):raise ValueError('Use next_action or next_actions, not both')
        with self.store.connect() as db:
            emails=db.execute("SELECT e.metadata,e.account_id,e.source_id,e.title FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='gmail.message' ORDER BY e.occurred_at DESC",(row['event_ids'],)).fetchall()
        options=thread_recipients(emails,[a.get('email','') for a in self.config['accounts']])
        for key in ('next_actions','next_action'):  # a reply always answers its email, in its thread (next_actions.fill_reply)
            if args.get(key):args={**args,key:reply_to_newest(emails,next_actions.fill_reply(args[key],replied_to(emails)))}
        with self.store.connect() as db:  # never a bounced address as To when the person has a working one (bounces.py)
            for key in ('next_actions','next_action'):
                if args.get(key):
                    steered,options=bounces.steer(db,args[key],options)
                    args={**args,key:steered}
            if not args.get('next_actions') and not args.get('next_action'):options=bounces.steer(db,None,options)[1]
        with self.store.connect() as db:
            senders=own_addresses.senders(db,self.config)
        with self.store.connect() as db:
            threads={m['conversation_id']:m.get('chat_name') or 'LinkedIn conversation' for m in (json.loads(r[0]) for r in db.execute(
                "SELECT e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='linkedin.message' ORDER BY e.occurred_at",(row['event_ids'],)))}
            x_threads={'mentions':{},'dms':{}}
            for kind,account_id,body,m in ((r[0],r[1],r[2],json.loads(r[3])) for r in db.execute(
                "SELECT e.kind,e.account_id,e.body,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind IN ('x.mention','x.dm') ORDER BY e.occurred_at",(row['event_ids'],))):
                if kind=='x.mention' and m.get('tweet_id') and m.get('screen_name'):
                    x_threads['mentions'][m['tweet_id']]={'account_id':account_id,'screen_name':m['screen_name'],'name':str(m.get('from') or '').rsplit(' (@',1)[0],
                                                         'text':re.split(r'\n\n\[(?:Quoting|In reply to)',body or '')[0][:280]}
                elif kind=='x.dm' and m.get('conversation_id'):
                    x_threads['dms'][m['conversation_id']]={'account_id':account_id,'name':m.get('chat_name') or 'X conversation'}
            whatsapp_chats={m['chat_id']:{'account_id':r[0],'name':m.get('chat_name') or 'WhatsApp chat'} for r in db.execute(
                "SELECT e.account_id,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='whatsapp.message' ORDER BY e.occurred_at",(row['event_ids'],))
                for m in (json.loads(r[1]),) if m.get('chat_id')}
            telegram_chats={m['chat_id']:{'account_id':r[0],'name':m.get('chat_name') or 'Telegram chat'} for r in db.execute(
                "SELECT e.account_id,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='telegram.message' ORDER BY e.occurred_at",(row['event_ids'],))
                for m in (json.loads(r[1]),) if m.get('chat_id')}
            signal_chats={m['chat_id']:{'account_id':r[0],'name':m.get('chat_name') or 'Signal chat'} for r in db.execute(
                "SELECT e.account_id,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind='signal.message' ORDER BY e.occurred_at",(row['event_ids'],))
                for m in (json.loads(r[1]),) if m.get('chat_id')}
            # The task's Intercom conversations, with the customer's address: an email to them is checked against
            # replying in Intercom (next_actions.validate). One a handoff carried that this Machine doesn't read
            # (fleet.intercom) can't be replied to here.
            intercom_conversations={m['conversation_id']:{'account_id':r[0] if r[2]=='intercom.conversation' else None,
                                                          'name':m.get('from_name') or m.get('from') or 'Intercom conversation',
                                                          'contact':str(m.get('contact_email') or '').lower()} for r in db.execute(
                "SELECT e.account_id,e.metadata,e.kind FROM events e JOIN json_each(?) ids ON ids.value=e.id WHERE e.kind IN ('intercom.conversation','fleet.intercom') ORDER BY e.kind='intercom.conversation',e.occurred_at",(row['event_ids'],))
                for m in (json.loads(r[1]),) if m.get('conversation_id')}
            docs=doc_comments(self.config,db,row['event_ids'])
            # The owner talks to this person on WhatsApp although the task came in another way: their existing chat.
            whatsapp_chats.update(owner_whatsapp_chats(self.config,db,args.get('next_actions',args.get('next_action')),whatsapp_chats))
            telegram_chats.update(owner_telegram_chats(self.config,db,args.get('next_actions',args.get('next_action')),telegram_chats))
            signal_chats.update(owner_signal_chats(self.config,db,args.get('next_actions',args.get('next_action')),signal_chats))
            calendar_events=calendar_write_events(db,calendar_write_ids(args.get('next_actions',args.get('next_action'))),self.owner_emails())
            spots=reply_spots(self.config,db,row['event_ids'])  # a Slack reply in its message's thread, a WhatsApp one quoting it
            doc_files=doc_write_files(db,row['event_ids'],self.config,doc_writes.area(self.config,json.loads(row['account_ids'] or '[]')))
        # A doc write: the owner's Docs connections, and each doc an edit names read now, its version pinned (doc_writes.py)
        doc_context=doc_writes.context(self.config,load_connector('docs'),CONNECTOR_HELPERS,doc_files,args.get('next_actions',args.get('next_action')),
                                       doc_writes.area(self.config,json.loads(row['account_ids'] or '[]')))
        action=next_actions.validate(args.get('next_actions',args.get('next_action')),self.config,json.loads(row['account_ids']),options,threads,x_threads,whatsapp_chats,intercom_conversations,calendar_events,docs,senders,replied_to(emails),telegram_chats,doc_context,spots,signal_chats)
        for item in next_actions.actions(action):
            if item['kind']=='handoff' and not (getattr(self,'fleet',None) and self.fleet.teammate(item)):
                raise ValueError('Hand off through The Machine only to a teammate in a Work Fleet (their email as listed); use a Slack message or email for anyone else')
        if any(item['kind']=='email_demo' for item in next_actions.actions(action)):
            with self.store.connect() as db:
                evidence=db.execute('SELECT e.kind,e.metadata FROM events e JOIN suggestions s ON s.id=? JOIN json_each(s.event_ids) ids ON ids.value=e.id',(args['suggestion_id'],)).fetchall()
            if not evidence or any(e['kind']!='assistant.test' or json.loads(e['metadata']).get('test') is not True for e in evidence):
                raise ValueError('Demo previews are only available on explicitly labeled assistant test tasks')
        problems=next_actions.check(action,args['body'],[a.get('email','') for a in self.config['accounts']])
        problems+=next_actions.reply_context(next_actions.actions(action),spots)
        # The to-do names the place the doc goes, never the other one (Google Docs vs Word)
        problems+=doc_writes.wording(next_actions.actions(action),[args.get('body'),args.get('needs'),args.get('title')])
        if problems and args.get('checked') is not True:
            # The run fixes these itself; checked:true saves anyway when one is deliberate.
            raise ValueError('Check before saving: '+'; '.join(problems)+'. Fix and save again, or add checked:true if this is intended.')
        outcome=None
        if args.get('outcome') is not None or args.get('job_id'):
            # Every result says plainly whether the job is finished.
            needs=' '.join(str(args.get('needs') or '').split())
            if args.get('outcome')=='done':outcome={'state':'done'}
            elif args.get('outcome')=='needs_you' and 3<=len(needs)<=200:outcome={'state':'needs_you','needs':needs}
            elif args.get('outcome')=='already_done' and args.get('follow_up')=='stop':
                # The Machine never ends follow-ups on its own judgment: the draft comes with its advice, the owner decides
                raise ValueError("follow_up:'stop' never goes without a draft: write the follow-up anyway, with follow_up:'stop' and "
                                 "follow_up_why:<why you would stop, a few words>, and outcome:'needs_you'. The owner decides")
            elif args.get('outcome')=='waiting' or args.get('outcome')=='already_done' and args.get('waiting_on'):
                # Done means nothing is left for anyone: with a step still open (a review, a merge, a deploy, someone's
                # reply) it is an open to-do waiting on that step, never "Looks done". Given both, the open step wins.
                waiting=' '.join(str(args.get('waiting_on') or '').split())
                if not 3<=len(waiting)<=200:raise ValueError("outcome:'waiting' needs waiting_on: the step still open and who it waits on, 3 to 200 characters")
                outcome={'state':'waiting','waiting_on':waiting}
            elif args.get('outcome')=='already_done' and 3<=len(' '.join(str(args.get('needs') or '').split()))<=200:
                outcome={'state':'needs_you','needs':' '.join(str(args['needs']).split())}  # something is still left for the owner: open, not done
            elif args.get('outcome')=='already_done':
                if any(a['kind']!='open' for a in next_actions.actions(action)):
                    raise ValueError("outcome:'already_done' means there is nothing left to approve: leave next_actions empty")
                outcome={'state':'already_done'}
            elif args.get('outcome')=='answered':outcome={'state':'answered'}
            elif args.get('outcome')=='your_step':
                # Everything is ready up to a final click the owner makes themselves (in the Machine's browser):
                # the card says what that click is and links to the page (View in browser).
                if args.get('step') not in FINAL_STEPS:
                    raise ValueError("outcome:'your_step' needs step: "+', '.join(FINAL_STEPS)+" (the final click left to the owner)")
                outcome={'state':'your_step','step':args['step']}
            elif args.get('outcome')=='snoozed':
                # The owner wants this card itself back later: the card's own snooze, not a separate reminder.
                outcome={'state':'snoozed','until':asked_snooze_time(args.get('snooze_until'))}
            else:raise ValueError("Say whether the job is finished: outcome:'done' (the task itself is complete; nothing left for the owner but to check it), outcome:'answered' (you only answered a question, explained or planned; the task itself is still to do), outcome:'already_done' (it turned out to be done already or no longer needed, nothing left for anyone), outcome:'waiting' with waiting_on (a step still open on someone else's side), outcome:'your_step' with step:<submit, pay, book, sign, confirm, order or apply> (all ready, the owner makes that final click), or outcome:'needs_you' with needs:<what they have to do, e.g. approve the send, sign in, pick an option>")
        if outcome and outcome['state']=='needs_you':
            with self.store.connect() as db:outcome=nudge_wait(db,args['suggestion_id'],args.get('job_id'),outcome,next_actions.actions(action))
        if 'do_now' in args and not isinstance(args['do_now'],bool):raise ValueError('do_now is true or false')
        # A step the owner asked for in this message runs on their word (do_now): their instruction is the OK. A new
        # step for their Confirm first gets the question, with their message and the step side by side (ask_do_now).
        with self.store.connect() as db:
            turn=owner_turn(db,args['suggestion_id'],args.get('job_id'))
            before={a.get('revision') for a in next_actions.actions(db.execute('SELECT next_action FROM suggestions WHERE id=?',(args['suggestion_id'],)).fetchone()[0] or 'null')}
            early=db.execute('SELECT early FROM suggestions WHERE id=?',(args['suggestion_id'],)).fetchone()[0]
        doable=[a for a in next_actions.actions(action) if doable_now(a)]
        if args.get('do_now') is True:
            if not doable:raise ValueError('do_now is for a doc edit or a final step that reaches nobody; a message, invite or sharing waits for the owner')
            if early or not turn:raise ValueError('do_now needs the owner’s own message in this turn asking for this step; save without it, for their Confirm')
        elif 'do_now' not in args and turn and not early and [a for a in doable if a.get('revision') not in before]:
            raise ValueError(ask_do_now(turn,[a for a in doable if a.get('revision') not in before]))
        # Carrying out one step never drops the other waiting steps; with one kept it isn't done. After do_now: only its own step runs.
        action,kept=self.store.kept_steps(args['suggestion_id'],args.get('job_id'),action,args.get('do_now') is True)
        if kept and outcome and outcome['state'] in ('done','already_done'):
            outcome=None
        if outcome and outcome['state']=='done' and args.get('send_now') is not True and args.get('do_now') is not True and self.store.waiting_steps(args['suggestion_id'],action,args.get('finish_state')):
            # Prepared is not done: a draft, review or final click still waits for the owner.
            raise ValueError("Not done yet: a step in next_actions still waits for the owner (a draft to send, a change to approve, a final click). "
                             "Save outcome:'needs_you' with needs:<what they do, e.g. check the draft and send it>, or outcome:'your_step' for a final click, "
                             'with a body that says what is ready and what is left, never that it is done, sent or applied.')
        with self.store.connect() as db:  # a rewrite from the follow-up review's Change: only its text changes, never sent from here
            why=follow_ups.change_problem(follow_ups.change_of(db,args['suggestion_id'],args.get('job_id')),
                                          [a for a in next_actions.actions(action) if a['kind'] in ('email',)+next_actions.TEXT_KINDS],args.get('send_now') is True)
        if why:raise ValueError(why+'.')
        why=next_actions.unlinked_reply(action)  # never a reply that would go out as a new thread
        if why:raise ValueError(why)
        if args.get('send_now') is True:
            # Only a draft the owner already had in front of them, approved in a later message of theirs. A draft
            # written or changed in this turn is saved and shown first: the owner reads it and taps Send.
            ready=[a for a in next_actions.actions(action) if a['kind'] in ('email','linkedin','slack','x') and not a.get('to_options')]
            with self.store.connect() as db:
                why=unseen_draft(db,args['suggestion_id'],ready[0]['revision'],args.get('job_id')) if ready else None
            if why:
                raise ValueError('Not sent: '+why+'. The owner sends only a draft they have seen. Save it again without send_now, '
                                 "with outcome:'needs_you' and needs:'check the draft and send it', and a body that says it is ready for them "
                                 '(not that it went out). Do not send it any other way.')
        advice=None
        with self.store.connect() as db:
            following=db.execute("SELECT 1 FROM follow_up_cards WHERE suggestion_id=? AND state='open'",(args['suggestion_id'],)).fetchone()
        if args.get('follow_up')=='stop':
            # An automated follow-up past its minimum that The Machine would stop: the draft is still there, the
            # review says why and leaves it unchecked (follow_ups.advise)
            advice=' '.join(str(args.get('follow_up_why') or '').split())
            if not following:raise ValueError("follow_up:'stop' is only for an automated follow-up")
            if not 3<=len(advice)<=follow_ups.ADVICE_MAX:raise ValueError(f"follow_up:'stop' needs follow_up_why: why you would stop, 3 to {follow_ups.ADVICE_MAX} characters")
            if not any(a['kind'] in ('email',)+next_actions.TEXT_KINDS for a in next_actions.actions(action)):
                raise ValueError("follow_up:'stop' still comes with the draft: write the follow-up, the owner decides")
        if args.get('based_on') is not None:
            with self.store.connect() as db:self.store.based_on_check(db,args['based_on'])
        if args.get('method') is not None:  # a repeating to-do's way of doing it, for the next one (recurring.method_lines)
            method=recurring.clean_method(args['method'])
            with self.store.connect() as db:
                if not recurring.method_series(db,args['suggestion_id']):raise ValueError('method is only for a to-do that repeats; leave it out')
        if args.get('routine_change') is not None:  # a lasting change to the to-do's routine, from the owner's note: offered, not saved
            with self.store.connect() as db:routine_change=routine_changes.check(db,args['suggestion_id'],args.get('job_id'),args['routine_change'])
        if not turn and args.get('send_now') is not True and args.get('do_now') is not True and (outcome or {}).get('state')!='already_done':
            # A message or handoff for someone, not asked for in the owner's own message now: their conversations are read
            # first, and what came after is named once (handled_check.py)
            why=self.handled_gate(args['suggestion_id'],args.get('job_id'),next_actions.actions(action))
            if why:raise ValueError(why)
        done_when=outcomes.clean(args['done_when']) if args.get('done_when') is not None else None  # checked before anything is saved
        saved=self.store.prepare(args['suggestion_id'], args['body'],args.get('job_id'),action,outcome,args.get('note_kind'),require_note=True,finish_state=args.get('finish_state'),title=args.get('title'),send_now=args.get('send_now') is True)
        if done_when is not None and not saved.get('replayed'):
            # The result that counts as done ('' clears it): after the send it waits for that, not done (outcomes.py)
            with self.store.connect() as db:outcomes.set_done_when(db,args['suggestion_id'],done_when,'run')
        if args.get('routine_change') is not None and not saved.get('replayed'):
            with self.store.connect() as db:routine_changes.offer(db,args['suggestion_id'],routine_change)
        if args.get('method') is not None and not saved.get('replayed'):
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                recurring.save_method(db,args['suggestion_id'],method,now())
                skills.drop_task_proposal(db,args['suggestion_id'])  # its way of working is kept here: no Create skill for it as well
            saved={**saved,'method':'saved: the to-do shows it with Edit and Undo, and the next one follows it'}
        if (outcome or {}).get('state')=='already_done' and not saved.get('replayed') and self.handled_close(args['suggestion_id'],args.get('job_id'),args['body']):
            saved={**saved,'status':'completed','note':'Done already, as those messages show: the to-do closed by itself (Undo for a day).'}
        if saved.get('reported'):  # its confirmed step went through while nobody watched: say so on the phone
            try:report_done(self.store,self.config,args['suggestion_id'])
            except Exception as error:LOG.warning('done report error=%s',type(error).__name__)
        if args.get('based_on') is not None and not saved.get('replayed'):
            with self.store.connect() as db:  # the teammate's input the draft follows: shown on the to-do, with its link
                self.store.mark_based_on(db,args['suggestion_id'],args['based_on'])
        if getattr(self,'fleet',None) and not saved.get('replayed') and 'team_learnings' in args:  # the team learnings it followed: shown on the to-do
            try:self.fleet.learnings_used(args['suggestion_id'],args['team_learnings'])
            except Exception as error:LOG.error('team learnings used error=%s',type(error).__name__)
        if following and not saved.get('replayed'):
            with self.store.connect() as db:
                follow_ups.advise(db,args['suggestion_id'],advice,now())
        if saved.get('status')=='snoozed' and not saved.get('replayed'):
            saved['note']+=' Tell them how it comes back, in these words: '+reminder_line(reminder_channels(self.store,self.config))

        if args.get('send_now') is True and not saved.get('replayed'):
            with self.store.connect() as db:
                if db.execute('SELECT early FROM suggestions WHERE id=?',(args['suggestion_id'],)).fetchone()[0]:
                    raise ValueError('Prepared ahead: the draft is saved; the owner sends it themselves')
            # The owner asked for it to be sent: queue the draft exactly as their Send tap would
            # (same sender, signature and attachments), without a second confirmation.
            ready=[a for a in next_actions.actions(action) if a['kind'] in ('email','linkedin','slack','x') and not a.get('to_options')]
            if not ready:raise ValueError('send_now needs an email, LinkedIn, Slack or X draft with its recipients filled in')
            saved['send']=self.store.confirm_action(args['suggestion_id'],ready[0]['revision'],'assistant:'+uuid.uuid4().hex,'assistant')
        if args.get('do_now') is True and not saved.get('replayed'):
            # The owner asked for this step in their message: it runs now as their Confirm would (2026-11-06: "why am I
            # confirming something I asked"). Sends still wait for their Send on a draft they saw.
            saved['done_now']=self.store.confirm_action(args['suggestion_id'],doable[0]['revision'],'asked:'+uuid.uuid4().hex,'assistant')
        if any(a['kind']=='doc_write' and a.get('op')=='create' for a in next_actions.actions(action)) and not saved.get('replayed'):
            # A new private doc in the owner's own Drive: made now, no OK needed (make_new_docs). Sharing it waits.
            saved['doc_created']='being made now in the owner’s own Drive, private to them; the to-do shows its link' if self.store.make_new_docs(args['suggestion_id']) else 'waits for the owner'
        if any(a['kind']=='merge' for a in next_actions.actions(action)) and not saved.get('replayed'):
            # The service decides, never the agent: a small, tested fix to its own error merges by itself.
            why=self.store.auto_merge(args['suggestion_id'],self.config)
            saved['auto_merge']='queued: it merges by itself if the tests pass, the new test fails without the fix and a second check agrees it only fixes a bug' if why is None else 'waits for the owner’s Merge: '+why
        if isinstance(saved, dict) and args.get('skill_hint') and getattr(self, 'skills', None) and not saved.get('replayed'):
            saved['skill_hint'] = self.skills.hint(args['suggestion_id'], args['skill_hint'])  # "There's a skill for this", if it clearly helps
        return saved

    def revise_draft_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:raise ValueError('Drafts are edited in the dashboard')
        return self.store.revise_draft(args['suggestion_id'],args['revision'],'dashboard',args.get('subject'),args.get('body'))

    def confirm_action_action(self, name, args, owner_dashboard=False):
        if owner_dashboard and re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}',str(args.get('approval_id',''))):source='dashboard'
        elif not owner_dashboard and re.fullmatch(r'telegram:[A-Za-z0-9_.:-]{1,200}',str(args.get('approval_id',''))):source='telegram'
        else:raise ValueError('Sending approval must come from the owner’s controls')
        return self.store.confirm_action(args['suggestion_id'],args['revision'],args['approval_id'],source,args.get('recipients'),args.get('sender'))

    def refresh_card_action(self, name, args, owner_dashboard=False):
        with self.store.connect() as db:
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=?',(args['suggestion_id'],))
        return {'queued':True}

    def chat_upload_action(self, name, args, owner_dashboard=False):
        # A New to-do form's files upload before the to-do exists, under the form's own draft key
        sid = 'new:' + str(args['draft']) if args.get('draft') is not None else str(args.get('suggestion_id') or '')
        if not re.fullmatch(r'(?:new:)?[a-f0-9]{16}', sid):
            raise ValueError('Unknown suggestion')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if name == 'chat_file_remove':
                return chat_files.remove(db, self.config, sid, args.get('id'))
            chat_files.sweep(db, self.config, now())
            return chat_files.save(db, self.config, sid, args.get('name'), args.get('data'), now())

    def decide_action(self, name, args, owner_dashboard=False):
        if args.get('choice') == 'reopen' and not owner_dashboard:
            raise ValueError('Use the owner dashboard to reopen a completed item')
        # The source is set here, never taken from the request: an agent must not be
        # able to label its own decision as the owner's Telegram click.
        if owner_dashboard:
            source = 'dashboard'
        elif re.fullmatch(r'(?:telegram|feedback)[:-][A-Za-z0-9_.:-]{1,200}', str(args.get('decision_id', ''))):
            source = 'telegram'  # the bridge's verified callback / owner-only command
        else:
            raise ValueError('Decisions must come from the owner’s Telegram buttons or dashboard')
        args = {**args, 'source': source}
        if str(args.get('decision_id', '')).startswith(NOTICE_DECISION):
            with self.store.connect() as db:
                refused = notice_decision_refused(db, args.get('suggestion_id'), args.get('choice'))
            if refused:
                raise ValueError(i18n.t(refused))
        if args.get('choice') in ('accept','other','retry'):
            with self.store.connect() as db:
                if mail_cleanup.is_cleanup(db, args.get('suggestion_id')):
                    raise ValueError(i18n.t('Pick for each one on the to-do, then confirm.'))
                if reading_digest.is_digest(db, args.get('suggestion_id')):
                    raise ValueError(i18n.t('A digest is only for reading.'))
        terminal_job=None
        files=args.get('files') if owner_dashboard and args.get('choice')=='other' else None  # added in the chat's composer
        feedback=args.get('feedback', '')
        if files and isinstance(feedback,str) and not feedback.strip():
            feedback=CHAT_FILES_ONLY[len(files)>1]
        result=self.store.decide(args['suggestion_id'], args['choice'], feedback,
                                 args['decision_id'], source, args.get('snooze_hours', 24),
                                 owner_snooze_until(args.get('snoozed_until')), args.get('snooze_option'),terminal_job,self.is_work_suggestion(args['suggestion_id']),
                                 reviewed=str(args.get('reviewed') or '')[:64] or None, files=files)
        if args['choice'] == 'complete' and getattr(self, 'agents', None):
            self.agents.card_closed(args['suggestion_id'])  # its Claude Code or Codex result did the job
        if args['choice'] == 'complete':
            self.task_pages.card_closed(args['suggestion_id'])  # its task page shows it done (task_pages.py)
        if args['choice'] in ('complete', 'reject') and getattr(self, 'fleet', None) and not result.get('skipped'):
            try:  # a team brief line on it: Not needed teaches the brief, as its own Not needed does (fleet_brief_todos.py)
                self.fleet.brief_todo_closed(args['suggestion_id'], args['choice'])
            except Exception as error:  # noqa: BLE001 - the decision stands
                LOG.warning('fleet brief todo closed error=%s', type(error).__name__)
        if args['choice'] == 'accept':
            try:self.apply_skill_clusters()
            except Exception as error:LOG.error('skill from notes error=%s',type(error).__name__)
        if args.get('source')=='telegram':
            # Compatibility fence: the old handler interprets duplicate
            # as "skip extra chat acknowledgment", after editing buttons.
            result.update(decision_saved=not result.get('skipped',False),duplicate=True,card_confirmation_only=True)
        return result

    def task_import(self, link):
        """Add a task someone sent by email (task_invites.py) as a card, and say who sent it so the owner can connect
        with them on the Network. Works without being on the Network: the link alone opens it."""
        invite_id, key = task_invites.parse_link(link)
        network = getattr(self, 'fleet', None)
        if network:  # signed in, so the Network can count it as added by this Machine
            found = network.relay.call('POST', '/task-invite', {'action': 'claim', 'id': invite_id})
        else:
            found = task_invites.claim(task_invites.network_url(self.config, fleet), invite_id)
        task = task_invites.unseal(str(found.get('sealed') or ''), key)
        who = found.get('from') or {}
        name = ' '.join(str(who.get('name') or task.get('from_name') or 'Someone').split())[:60]
        body = (task.get('summary') or task['title']) + (f"\n\nThey'd like it by {task['due']}." if task.get('due') else '')
        body += f'\n\n{name} sent this by email. Answer them there.'
        card_id = self.fleet_card('task', 'task:' + invite_id, name, task['title'], body, [], due=task.get('due'), via='by email')
        if network:
            try:
                network.relay.call('POST', '/task-invite', {'action': 'added', 'id': invite_id})
            except (ValueError, OSError):
                LOG.warning('task invite local card saved; remote addition receipt unavailable')
        username = who.get('username') if isinstance(who.get('username'), str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{1,28}[a-z0-9]', who['username']) else None
        connected = False
        if network and username:  # a friend already, or in a Work or Family Fleet together: nothing to connect
            ref = network.friends_ref()
            friends = {str(m.get('username') or '').lower() for m in network.teammates(ref)} if ref else set()
            connected = username in friends or network.in_my_fleet(network.fleet_mates(), username)
        return {'card_id': card_id, 'from': {'name': name, 'username': username}, 'can_connect': bool(network and username and not connected)}

    def handoff_email(self, card_id, email, title, summary, keep=None, take=None, name=''):
        """Hand a Work card to someone who is not on The Machine: an ordinary email draft on the card, from the card's
        Gmail or Outlook account, built from what the owner ticked (handoff_mail.py), for the owner to read and send.
        Nothing about the task leaves this Machine until the owner sends it, or approves a task page for it
        (task_pages.py), which this offers on the card."""
        made = self.handoff_mail.prepare(card_id, email, name, title, summary, keep, take)
        self.task_pages.offer(made['card_id'], made['task'])
        return {'card_id': made['card_id']}

    def import_check_start(self, kind, text):
        """The owner's model looks at a file being imported (crm_import.ai_evidence: headers, a few values, unclear
        cells), when it can run now: signed in, with room in its limits and no other agent pass going. Else the
        rules' guess stands and {'ai': False, 'why'} says why."""
        if kind not in crm_import.FIELDS:
            raise ValueError('Import people, organizations or projects')
        if self.config.get('import_check') is False:
            return {'ai': False, 'why': 'off'}
        if model_ready(self.config) is False or not self.model_room():
            return {'ai': False, 'why': 'model'}
        region = crm_fixes.region_of({'country': self.config.get('country'), 'timezone': self.config.get('timezone') or getattr(local_tz(), 'key', '')})
        with self.store.connect() as db:
            evidence = crm_import.ai_evidence(db, kind, text, region, self.currency())
        run_id, started = uuid.uuid4().hex, now()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute("UPDATE profile_runs SET status='error',error='replaced',finished_at=?,updated_at=? WHERE kind='import' AND status='starting'", (started, started))
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') AND kind!='import'").fetchone():
                return {'ai': False, 'why': 'busy'}  # an agent pass is going: the import doesn't wait for it
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind) VALUES(?,'starting',?,?,?,'import')",
                       (run_id, started, started, json.dumps({'kind': kind, 'digest': crm_import.digest(kind, text), 'import': evidence})))
        return {'ai': True, 'run_id': run_id, 'cells': len(evidence['cells'])}

    def import_check_status(self, run_id):
        with self.store.connect() as db:
            row = db.execute("SELECT status,error,draft FROM profile_runs WHERE run_id=? AND kind='import'", (str(run_id or ''),)).fetchone()
        if not row:
            raise ValueError('Unknown import check')
        draft = json.loads(row['draft']) if row['draft'] else {}
        return {'status': row['status'], 'columns': len(draft.get('mapping') or {}), 'fixes': len(draft.get('fixes') or ())}

    def import_check_draft(self, run_id, kind, text):
        """The model's draft for this very file (the same kind and text), else None."""
        if not run_id:
            return None
        with self.store.connect() as db:
            row = db.execute("SELECT evidence,draft FROM profile_runs WHERE run_id=? AND kind='import' AND draft IS NOT NULL", (str(run_id),)).fetchone()
        if not row or json.loads(row['evidence']).get('digest') != crm_import.digest(kind, text):
            return None
        return json.loads(row['draft'])

    def card_owner_action(self, name, args, owner_dashboard=False):
        # a to-do added, renamed, moved or merged by the owner (CARD_ACTIONS)
        if not owner_dashboard:
            raise ValueError('Cards are added, renamed and merged by the owner, on the dashboard')
        if name == 'card_new':
            return self.card_new_repeating(args)  # recurring_app.py: Repeats, or a rhythm in the words
        if name == 'card_project':  # the to-do's project, by hand ('' for none): graph.set_card_project
            with self.store.connect() as db:
                return {'id': str(args.get('suggestion_id') or ''), 'project': graph.set_card_project(db, args.get('suggestion_id'), args.get('project'))}
        if name == 'card_rename':
            return self.store.rename_card(args.get('suggestion_id'), args.get('title'), args.get('reset') is True, args.get('decision_id'))
        if name == 'card_move':  # More, Move to Work (todo_areas.py); undo: the move its toast's Undo takes back
            return self.store.move_card(args.get('suggestion_id'), args.get('area'), args.get('decision_id'), undo=args.get('undo'))
        if name == 'card_report_seen':  # Just done, Got it: the owner saw what their confirmed steps did
            return self.store.report_seen(args.get('ids'))
        if name == 'card_use_sources':  # "Use this email for this to-do": what its stuck run asked for (use_sources)
            return self.store.use_sources(args.get('suggestion_id'), args.get('decision_id'))
        return self.store.merge_answer(args.get('suggestion_id'), args.get('merge') is True, args.get('decision_id'))

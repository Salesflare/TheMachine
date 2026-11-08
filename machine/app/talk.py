"""Talk in the service (refactor PR 21; talk_live.py and the voice side do the rest): Talk's view and readiness, its
actions and tools, the drafts it makes and sends, what it recalls and records, and the lookups it shows. Moved out of
assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import time
import uuid

import ai_access
import doc_writes
import enrichment
import graph
import knowledge
import locale_prefs
from machine.actions import TALK_ACTIONS
from machine.cards import todo_state
from machine.chat import chat_name, chat_person
from machine.config import LOG, ROOT
from machine.delivery.push import talk_about, TALK_KINDS
from machine.model_usage import node_bin, node_env
from machine.store.cards import source_text
from machine.store.decisions import handoff_wait
from machine.store.promises import promise_state
from machine.text import _address, clamp
import next_actions
import security_levels
import talk_live
from timeutil import local_tz, now
import voice_input


class TalkApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {**dict.fromkeys(TALK_ACTIONS, 'talk_actions_action')}

    @property
    def talk(self):
        """Talk live's open conversations (talk_live.py)."""
        if getattr(self, '_talk', None) is None:
            self._talk = talk_live.Talk({**self.config, '_node': node_bin(self.config)})
        return self._talk

    def talk_env(self):
        return {**node_env(self.config), 'OPENCLAW_CONFIG_PATH': str(Path(self.config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json').expanduser())}

    def talk_view(self, check=False):
        """Whether Talk live can start here. Whether OpenAI charges per use (an API key, which the Gateway uses first) or
        not (a ChatGPT sign-in) shows once a conversation starts (talk_start's `per_use`)."""
        found = self.talk.status(self.talk_env(), check)
        if found is None:
            return {'ready': None}
        return {'ready': found['ready'], 'limit': talk_live.LIMIT_SECONDS, 'warn': talk_live.WARN_SECONDS}

    def talk_ready(self):
        """Whether Talk (the sidebar's) can show: Talk live's readiness as known (kept 10 minutes, refreshed in the
        background), None until known."""
        try:
            found = self.talk.status(self.talk_env(), check=True)
        except Exception:  # never in the way of the page's status
            return None
        return found['ready'] if found else None

    def talk_action(self, name, args):
        """A live conversation in a to-do's chat (talk_live.py). Only what it reads and what both sides said pass here;
        the audio goes directly between the browser and OpenAI."""
        env = self.talk_env()
        if name == 'talk_status':
            return self.talk_view(check=True)
        if name == 'talk_start':
            # A to-do's own conversation, or the main one (Talk in the sidebar: main=True, no to-do)
            main = args.get('main') is True
            sid = str(args.get('suggestion_id') or '')
            with self.store.connect() as db:
                card = db.execute('SELECT title FROM suggestions WHERE id=?', (sid,)).fetchone() if re.fullmatch(r'[a-f0-9]{16}', sid) else None
            if not card and not main:
                raise ValueError('Unknown suggestion')
            with self.store.connect() as db:
                voice_prefs = voice_input.prefs(db)
            voice = voice_prefs['talk_voice']
            # The owner's own clock and time zone (setup and Settings), never the server's: a hosted Machine runs in UTC
            (now, zone), language = talk_live.owner_clock(), locale_prefs.language() or 'en'
            # What the owner speaks: the UI language, Voice input's language, the locale's and the browser's languages
            browser = [str(x)[:20] for x in args.get('languages') or [] if isinstance(x, str)][:8] if isinstance(args.get('languages'), list) else []
            spoken = talk_live.spoken(language, voice_prefs['language'], locale_prefs.view().get('locale'), browser)
            started = self.talk.start(None if main else sid, env, voice, spoken)
            LOG.info('talk live start via=%s main=%s', started.get('via'), main)
            view = self.talk_view()
            return {**started, 'voice': voice, 'speed': talk_live.SPEED, 'turn': talk_live.TURN, 'per_use': started.get('via') == 'key',
                    'noise': talk_live.NOISE, 'transcription': talk_live.transcription(spoken), 'transcription_next': talk_live.transcription_next(spoken), 'languages': spoken,
                    'limit': talk_live.MAIN_LIMIT_SECONDS if main else talk_live.LIMIT_SECONDS,
                    'warn': talk_live.MAIN_WARN_SECONDS if main else talk_live.WARN_SECONDS,
                    'tools': talk_live.MAIN_TOOLS if main else talk_live.TOOLS, 'ask_note': talk_live.ASK_NOTE,
                    'notes': {'queued': talk_live.QUEUED_NOTE, 'done': talk_live.DONE_NOTE, 'stopped': talk_live.STOPPED_NOTE, 'new': talk_live.NEW_NOTE,
                              'ready': talk_live.READY_NOTE, 'again': talk_live.AGAIN_NOTE,
                              'unheard': talk_live.UNHEARD_NOTE, 'sent': talk_live.SENT_NOTE, 'not_sent': talk_live.NOT_SENT_NOTE},
                    'instructions': talk_live.main_instructions(language, now, spoken, zone) if main else talk_live.instructions(card['title'], language, now, spoken, zone),
                    'time_zone': zone,
                    'main': main, 'ready': view.get('ready')}
        if name == 'talk_focus':
            sid = str(args.get('suggestion_id') or '')
            with self.store.connect() as db:
                if not (re.fullmatch(r'[a-f0-9]{16}', sid) and db.execute('SELECT 1 FROM suggestions WHERE id=?', (sid,)).fetchone()):
                    raise ValueError('Unknown suggestion')
            return self.talk.focus(args.get('id'), sid)
        if name == 'talk_offer':
            return self.talk.offer(args.get('id'), args.get('sdp'), env)
        if name == 'talk_end':
            return self.talk.end(args.get('id'), env)
        if name == 'talk_line':
            with self.store.connect() as db:
                return self.talk.line(db, args.get('id'), args.get('role'), args.get('text'), int(time.time() * 1000))
        if name == 'talk_ask_send':
            return self.talk_ask_send(args)
        if name == 'talk_send':
            return self.talk_send(args)
        if name == 'talk_undo':
            return self.store.undo_voice_send(args.get('suggestion_id'), args.get('approval_id'))
        if name == 'draft_seen':
            return self.draft_seen(args)
        found = self.talk.get(args.get('id'))
        tool = str(args.get('name') or '')
        if tool == 'todo_details' and not talk_live.subject(found):
            return {'output': {'error': 'No to-do is open. Call open_todo first.'}}
        return {'output': self.talk_tool(talk_live.subject(found), tool, args.get('args') if isinstance(args.get('args'), dict) else {}, ids=bool(found.get('main')))}

    def talk_draft(self, suggestion_id, revision):
        """The draft Talk live may ask to send: this to-do's current one, ready, going to people the draft names."""
        with self.store.connect() as db:
            row = db.execute('SELECT status,next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        action = next_actions.selected(row['next_action'], revision) if row and row['status'] == 'prepared' and revision else None
        if not action or action.get('kind') not in talk_live.SEND_KINDS or action.get('to_options'):
            return None
        return action

    def talk_drafts(self, suggestion_id):
        """This to-do's drafts Talk live may ask to send, in the order the chat shows them."""
        with self.store.connect() as db:
            row = db.execute('SELECT status,next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        if not row or row['status'] != 'prepared':
            return []
        return [a for a in next_actions.visible_actions(row['next_action'])
                if a.get('kind') in talk_live.SEND_KINDS and not a.get('to_options') and a.get('revision')]

    def draft_seen(self, args):
        """The dashboard showed this draft in full (its to-do, its chat or Talk's card), long enough to read: kept for
        this exact text, so a send by voice needn't read it out again. What the page showed must be the draft as it is."""
        sid, revision = str(args.get('suggestion_id') or ''), str(args.get('revision') or '')
        action = self.talk_draft(sid, revision) if re.fullmatch(r'[a-f0-9]{16}', sid) and revision else None
        shown = {'to': [str(x) for x in args.get('to') or []] if isinstance(args.get('to'), list) else [],
                 'subject': str(args.get('subject') or ''), 'body': str(args.get('body') or '')}
        if not action or shown != {'to': [str(x) for x in action.get('to') or []], 'subject': str(action.get('subject') or ''),
                                   'body': str(action.get('body') or action.get('message') or '')}:
            return {'ok': False}
        with self.store.connect() as db:
            talk_live.saw(db, sid, revision, talk_live.digest(action), int(time.time() * 1000))
        return {'ok': True}

    def talk_seen(self, talk_id, sid, revision, action):
        """Whether the owner has seen this exact draft on screen or heard it read out in this conversation."""
        with self.store.connect() as db:
            if talk_live.seen(db, sid, revision, talk_live.digest(action)):
                return True
            return self.talk.heard(db, talk_id, sid, revision, talk_live.digest(action))

    def talk_who(self, action):
        """Who a draft goes to, as the voice says it: their names, or the addresses."""
        to = [str(x) for x in action.get('to') or []]
        names = {}
        if len(to) == 1 and str(action.get('to_name') or '').strip():
            names[_address(to[0])] = chat_person(str(action['to_name']).strip())
        everyone = [chat_name(x, names, str(action.get('to_name') or '') if len(to) == 1 else '') for x in to]
        name = everyone[0] if everyone else ''
        return everyone, (name if len(to) <= 1 else name + ' and %d more' % (len(to) - 1))

    def talk_spoken(self, action, everyone):
        """A draft as the voice reads it out."""
        return {'to': everyone[:20], 'how': talk_live.CHANNELS.get(action['kind'], ''), **({'subject': action['subject']} if action.get('subject') else {}),
                'text': doc_writes.spoken(action) if action['kind'] == 'doc_write' else clamp(str(action.get('body') or action.get('message') or ''), 4000)}

    def talk_ask_send(self, args):
        """The voice asks to send this to-do's draft: the one the screen shows when it shows one (revision), else its
        only draft, or the one named by its number. The Machine pins that revision. A draft the owner hasn't seen on
        screen or heard in this conversation comes whole, to read out first (read: the owner asked to hear it); one they
        have comes without its text, so it is never read twice. With ids: several to-dos' drafts under one question."""
        if isinstance(args.get('ids'), list):
            return self.talk_ask_send_all(args)
        found = self.talk.get(args.get('id'))
        sid, revision = talk_live.subject(found), str(args.get('revision') or '')
        drafts = self.talk_drafts(sid) if sid else []
        if not revision and len(drafts) > 1 and not args.get('draft'):
            return {'error': 'This to-do has more than one draft. Ask which one, then call ask_to_send with its number.',
                    'drafts': [{'draft': n + 1, 'label': clamp(next_actions.label(a), 80)} for n, a in enumerate(drafts[:5])]}
        if not revision and drafts:
            try:
                revision = drafts[max(0, int(args.get('draft') or 1) - 1)]['revision']
            except (IndexError, TypeError, ValueError):
                return {'error': 'No draft with that number.'}
        action = self.talk_draft(sid, revision) if sid and revision else None
        if not action:
            return {'error': 'No draft ready to send by voice. Ask the chat to draft one first.'}
        if action['kind'] == 'doc_write' and len(doc_writes.spoken(action)) > 4000:  # read in full, or not by voice
            return {'error': 'This doc change is too long to read aloud. The owner reviews it on the screen.'}
        everyone, name = self.talk_who(action)
        at, d = int(time.time() * 1000), talk_live.digest(action)
        draft = self.talk_spoken(action, everyone)
        read = args.get('read') is True or not self.talk_seen(args.get('id'), sid, revision, action)
        if read:
            self.talk.reading(args.get('id'), sid, revision, d, draft['text'], at)
        asked = self.talk.ask(args.get('id'), [{'sid': sid, 'revision': revision, 'digest': d, 'read': read}], talk_live.question(action, name), name, at, sid)
        if not read:
            return {'question': asked, 'revision': revision, 'seen': True, 'draft': {k: v for k, v in draft.items() if k != 'text'},
                    'say': talk_live.SAY['seen'] + talk_live.SAY['ask'] + asked}
        return {'question': asked, 'revision': revision, 'draft': draft, 'say': talk_live.SAY['read'] + talk_live.SAY['ask'] + asked}

    def talk_ask_send_all(self, args):
        """Several ready drafts under one question (the main conversation): each to-do's only draft, pinned; the ones the
        owner hasn't seen or heard come whole, to read out first."""
        found = self.talk.get(args.get('id'))
        if not found.get('main'):
            return {'error': 'Only Talk sends several at once.'}
        ids = list(dict.fromkeys(str(x) for x in args.get('ids') or [] if re.fullmatch(r'[a-f0-9]{16}', str(x))))
        if not ids or len(ids) > 5:
            return {'error': 'Give the to-dos’ ids, at most 5 at once.'}
        at, items, drafts, skipped, names = int(time.time() * 1000), [], [], [], []
        with self.store.connect() as db:
            titles = {r['id']: r['title'] for r in db.execute('SELECT id,title FROM suggestions WHERE id IN (SELECT value FROM json_each(?))', (json.dumps(ids),))}
        for sid in ids:
            mine = self.talk_drafts(sid)
            if len(mine) != 1 or (mine[0]['kind'] == 'doc_write' and len(doc_writes.spoken(mine[0])) > 4000):
                skipped.append({'id': sid, 'title': clamp(titles.get(sid) or '', 120),
                                'why': 'more than one draft' if len(mine) > 1 else 'no draft ready to send by voice'})
                continue
            action = mine[0]
            everyone, name = self.talk_who(action)
            d, draft = talk_live.digest(action), self.talk_spoken(action, everyone)
            read = not self.talk_seen(args.get('id'), sid, action['revision'], action)
            if read:
                self.talk.reading(args.get('id'), sid, action['revision'], d, draft['text'], at)
            items.append({'sid': sid, 'revision': action['revision'], 'digest': d, 'read': read})
            names.append(name)
            drafts.append({'id': sid, 'title': clamp(titles.get(sid) or '', 120), **(draft if read else {k: v for k, v in draft.items() if k != 'text'})})
        if not items:
            return {'error': 'None of these has one draft ready to send by voice.', 'skipped': skipped}
        if len(items) == 1:
            asked = talk_live.question(self.talk_draft(items[0]['sid'], items[0]['revision']), names[0])
        else:
            asked = 'Send all %d, to %s?' % (len(items), ', '.join(names[:-1]) + ' and ' + names[-1])
        self.talk.ask(args.get('id'), items, asked, names[0], at)
        unseen = any(i['read'] for i in items)
        return {'question': asked, 'drafts': drafts, **({'skipped': skipped} if skipped else {}),
                'say': (talk_live.SAY['read_some'] if unseen else talk_live.SAY['seen']) + talk_live.SAY['ask'] + asked}

    def talk_send(self, args):
        """The owner answered the confirm question: the Machine judges their own last words (talk_live.clear_answer), and
        a clear yes for the unchanged drafts goes the normal way (confirm_action, source 'voice', each held for Undo)."""
        talk_id = args.get('id')
        found = self.talk.get(talk_id)
        if not found.get('confirm') and not talk_live.subject(found):
            return {'status': 'not_asked', 'say': talk_live.SAY['not_asked']}
        with self.store.connect() as db:
            status, asked = self.talk.answer(db, talk_id, int(time.time() * 1000), lambda sid, revision: self.talk_draft(sid, revision))
        LOG.info('talk live answer %s', status)
        if status != 'yes':
            return {'status': status, 'say': talk_live.SAY[status].replace('{name}', (asked or {}).get('name') or 'them')}
        sent = []
        for item in asked['items']:
            approval = 'voice:' + uuid.uuid4().hex
            action = self.talk_draft(item['sid'], item['revision']) or {}
            try:
                self.store.confirm_action(item['sid'], item['revision'], approval, 'voice', hold=talk_live.UNDO_SECONDS)
            except ValueError:
                continue
            sent.append({'suggestion_id': item['sid'], 'approval_id': approval, 'to': self.talk_who(action)[1] if action else '',
                         'kind': str(action.get('kind') or '')})   # Talk's Undo bar says who it goes to
        if not sent:
            return {'status': 'changed', 'say': talk_live.SAY['changed']}
        many = len(asked['items']) > 1
        # One count for the voice and the Undo bar: what the outbox still holds (its retry_at), not a number of our own
        with self.store.connect() as db:
            held = [r['retry_at'] for r in db.execute("SELECT retry_at FROM action_jobs WHERE source='voice' AND approval_id IN "
                                                      "(SELECT value FROM json_each(?))", (json.dumps([x['approval_id'] for x in sent]),)) if r['retry_at']]
        left = max(0, min((dt.datetime.fromisoformat(x) - dt.datetime.fromisoformat(now())).total_seconds() for x in held)) if held else talk_live.UNDO_SECONDS
        return {'status': 'queued', 'approval_id': sent[0]['approval_id'], 'sent': sent, 'undo_ms': int(left * 1000), 'undo_seconds': int(left),
                **({'not_sent': len(asked['items']) - len(sent)} if len(sent) < len(asked['items']) else {}),
                'say': talk_live.SAY['queued_all' if many else 'queued'].replace('{n}', str(int(left)))}

    def talk_send_status(self, suggestion_id, approval_id=''):
        """Whether a to-do's send went out, from its outbox row (action_jobs): the one approval_id names, else the latest.
        For the voice (send_status) and the dashboard, which follows a send by voice until it settles. Never a guess."""
        with self.store.connect() as db:
            row = db.execute('SELECT status,retry_at,updated_at,error,payload FROM action_jobs WHERE suggestion_id=? AND (?=\'\' OR approval_id=?) '
                             'ORDER BY created_at DESC LIMIT 1', (suggestion_id, approval_id, approval_id)).fetchone()
        if not row:
            return {'state': 'none', 'say': talk_live.STATUS_SAY['none']}
        try:
            action = json.loads(row['payload'])
        except ValueError:
            action = {}
        to = self.talk_who(action)[1] if isinstance(action, dict) else ''
        status, out = row['status'], {}
        if status == 'queued' and row['retry_at'] and row['retry_at'] > now():
            left = int((dt.datetime.fromisoformat(row['retry_at']) - dt.datetime.fromisoformat(now())).total_seconds())
            out = {'state': 'waiting', 'seconds_left': left, 'undo_ms': left * 1000}
        elif status in ('sent', 'done'):
            moment = dt.datetime.fromisoformat(row['updated_at']).astimezone(local_tz())
            out = {'state': 'sent', 'at': row['updated_at'], 'time': moment.strftime('%H:%M')}
        elif status in ('failed', 'blocked', 'cancelled'):
            out = {'state': {'cancelled': 'canceled'}.get(status, status), 'why': clamp(str(row['error'] or ''), 300)}
        elif status in ('uncertain', 'finish_uncertain'):
            out = {'state': 'unsure'}
        else:   # queued for the outbox, sending, a final step being prepared
            out = {'state': 'sending'}
        say = talk_live.STATUS_SAY[out['state']].replace('{to}', to or 'them').replace('{n}', str(out.get('seconds_left', ''))) \
            .replace('{at}', out.get('time', '')).replace('{why}', out.get('why') or 'no reason was given.')
        return {**out, 'to': to, 'kind': str(action.get('kind') or '') if isinstance(action, dict) else '', 'say': say}

    def talk_tool(self, suggestion_id, name, args, ids=False):
        """Talk live's tools that read (talk_live.TOOLS): this to-do, or finding others. Never anything that sends or
        changes; `ask_chat` is the dashboard's own (the chat's normal decide path)."""
        if name == 'todo_details':
            chat = self.card_chat(suggestion_id)
            with self.store.connect() as db:
                card = db.execute('SELECT s.id,s.title,s.status,p.status preparation_status,s.handled_hint,s.outcome FROM suggestions s '
                                  'LEFT JOIN preparations p ON p.suggestion_id=s.id WHERE s.id=?', (suggestion_id,)).fetchone()
                # Handed off and back on the list while the teammate still has it ("Still with Lieven · check in?")
                still = handoff_wait(db, dict(card), awake=True) if card else None
            said, drafts = [], []
            for i in chat.get('items') or []:
                who = {'source': i.get('from') or 'Message', 'you': 'Owner', 'reply': 'The Machine', 'agent': i.get('name') or 'Agent'}.get(i.get('kind'))
                if who and str(i.get('text') or '').strip():
                    said.append({'from': clamp(str(who), 80), 'text': clamp(str(i['text']), 800)})
                drafts = i.get('drafts') or drafts
            # The draft's text isn't here: read_draft reads it out (and keeps that it was), so it is never told twice
            return {'title': card['title'] if card else '', 'state': todo_state(dict(card)) if card else '', 'messages': said[-25:],
                    'drafts': [{k: d.get(k) for k in ('kind', 'to', 'subject')} for d in drafts[:3]],
                    **({'draft_note': 'To hear a draft, call read_draft.'} if drafts else {}),
                    **({'with': still['name'], 'with_note': 'Handed off to ' + still['name'] + ', who has not answered yet.'} if still else {})}
        if name == 'find_todos':
            words = [w for w in re.findall(r'\w+', str(args.get('words') or '').lower()) if len(w) > 1][:6]
            want = str(args.get('state') or '').strip().lower()
            known = talk_live.STATES + (talk_live.LOOKS_DONE,) + talk_live.CLOSED   # the dashboard's order
            want = want if want in known else ''
            if not words and not want:
                return {'todos': []}
            named = next((st for st in known if set(st.split()) <= set(words)), '') if not want else ''
            match = lambda rows: rows if not words else [r for r in rows if all(w in (r['title'] or '').lower() for w in words)] or \
                [r for r in rows if any(w in (r['title'] or '').lower() for w in words)]
            found = []
            if want not in talk_live.CLOSED:
                with self.store.connect() as db:
                    rows = [dict(r) for r in db.execute(
                        "SELECT s.id,s.title,s.status,p.status preparation_status,s.handled_hint,s.outcome FROM suggestions s "
                        "LEFT JOIN preparations p ON p.suggestion_id=s.id WHERE s.status NOT IN ('completed','rejected') "
                        "ORDER BY s.created_at DESC LIMIT 500")]
                for r in rows:
                    r['state'] = todo_state(r)
                if want:
                    rows = [r for r in rows if r['state'] == want]
                found = match(rows)
                if not found and named and named not in talk_live.CLOSED:  # "anything preparing?": no title has the word, so the state it names
                    found = [r for r in rows if r['state'] == named]
                found.sort(key=lambda r: known.index(r['state']))  # the dashboard's order: what needs the owner first
            if not found and (want in talk_live.CLOSED or named in talk_live.CLOSED or (words and not want)):
                # Done / dismissed, latest closed first (the dashboard's list): asked for, or no open one matches
                with self.store.connect() as db:
                    closed = self.store.done_rows(db, titles=True)[:500]
                    status = {r['id']: r['status'] for r in db.execute(
                        'SELECT id,status FROM suggestions WHERE id IN (SELECT value FROM json_each(?))', (json.dumps([r['id'] for r in closed]),))}
                rows = [{**r, 'state': todo_state({'status': status.get(r['id'], 'completed')})} for r in closed]
                kind = want if want in talk_live.CLOSED else named if named in talk_live.CLOSED else ''
                if kind:
                    rows = [r for r in rows if r['state'] == kind]
                found = (match(rows) if words else rows) or (rows if kind else [])   # "anything dismissed?": that list
            # the main conversation opens one by its id (open_todo)
            return {'todos': [{**({'id': r['id']} if ids else {}), 'title': clamp(r['title'], 200), 'state': r['state']}
                              for r in found[:20]], 'count': len(found)}
        if name == 'send_status':  # the main conversation may ask about any to-do by its id; a to-do's own Talk, that one
            sid = str(args.get('id') or '') if ids and re.fullmatch(r'[a-f0-9]{16}', str(args.get('id') or '')) else suggestion_id
            if not sid:
                return {'error': 'No to-do is open. Call open_todo first.'}
            return self.talk_send_status(sid, str(args.get('approval_id') or ''))
        if name in talk_live.MACHINE_TOOLS and ids:  # the main conversation's own: the rest of the Machine, read only
            return self.talk_machine_tool(name, args)
        raise ValueError('Unknown tool')

    def talk_when(self, value):
        """A moment as the voice says it: 'Thu 29 Oct 14:30', in the owner's time zone (English: the model says it in theirs)."""
        try:
            moment = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone(local_tz())
        except (TypeError, ValueError):
            return ''
        return locale_prefs.day_text(moment, lang='en') + moment.strftime(' %H:%M')

    def talk_machine_tool(self, name, args):
        """Talk's read tools for the rest of the Machine (talk_live.MACHINE_TOOLS), through the stores and views the
        dashboard reads: the Graph's search and pages, Events, the Calendar, Promises. Short, speakable rows with ids for
        open_record; nothing here changes anything."""
        accounts = [a['id'] for a in self.config.get('accounts', [])]
        if name == 'calendar':
            try:
                day = dt.date.fromisoformat(str(args.get('day') or '')) if args.get('day') else dt.datetime.now(local_tz()).date()
            except ValueError:
                return {'error': 'day is YYYY-MM-DD'}
            days = max(1, min(int(args.get('days') or 1), 14))
            start = dt.datetime.combine(day, dt.time(), local_tz())
            rows = self.store.calendar(accounts, start.isoformat(), (start + dt.timedelta(days=days)).isoformat(), self.owner_emails()) if accounts else []
            return {'meetings': [{'id': 'event:%d' % m['id'], 'title': clamp(m['title'], 160), 'when': 'all day' if m['all_day'] else self.talk_when(m['start']),
                                  **({'until': self.talk_when(m['end'])[-5:]} if not m['all_day'] else {}),
                                  **({'where': clamp(m['location'], 100)} if m['location'] else {}), 'with': m['people'][:6]} for m in rows[:25]],
                    'from': day.isoformat(), 'days': days, 'count': len(rows)}
        if name == 'search':
            words, kind = ' '.join(str(args.get('words') or '').split())[:200], str(args.get('kind') or 'anything')
            person = ' '.join(str(args.get('person') or '').split())[:200]
            if not words and not person:
                return {'error': 'Say what to look for.'}
            if kind == 'message' and (person or self.talk_named(words)):  # words that name someone: their messages
                # Messages with someone: their latest, the same ones their Graph page shows, from every address and
                # number merged into them; never a search by meaning that happens to mention their name
                return self.talk_messages_with(person or words, accounts)
            if not words:
                return {'error': 'Say what to look for.'}
            if kind in ('message', 'meeting'):
                rows = self.action('events', {'account_ids': accounts, 'query': words, 'full': True, 'limit': 20,
                                              **({'kinds': ['calendar.event']} if kind == 'meeting' else {'semantic': True})}) if accounts else []
                rows = [r for r in rows if (r['kind'] == 'calendar.event') == (kind == 'meeting')][:8]
                found = [{'id': 'event:%d' % r['id'], 'kind': kind, 'title': clamp(' '.join(str(r['title'] or '').split()), 160),
                          'what': source_text(r)} for r in rows]
                return {'found': found} if found else {'found': [], 'searched': '%ss matching "%s", in every connected account' % (kind, words),
                                                       'note': talk_live.NOTHING_NOTE}
            if kind == 'promise':
                with self.store.connect() as db:   # promises with someone: what is open with them, as on their page
                    hit = knowledge.named(db, words, also=self.talk_marks(db))
                    mine = knowledge.open_with(self.store, self.config, hit['id']) if hit else None
                ids = {p['id'] for k in ('you_promised', 'they_promised') for p in mine[k]} if mine else set()
                found = [x for x in self.store.promises() if x['state'] in ('open', 'card') and (x['id'] in ids if mine else
                         all(w in (str(x['who']) + ' ' + str(x['what'])).lower() for w in words.lower().split()))][:8]
                return {'found': [{'id': 'promise:%d' % x['id'], 'kind': 'promise', 'who': clamp(str(x['who']), 80), 'what': clamp(str(x['what']), 200),
                                   'direction': 'the owner promised' if x['direction'] == 'mine' else 'promised to the owner',
                                   **({'due': x['due']} if x.get('due') else {})} for x in found]}
            want = {'person': 'person', 'organization': 'org', 'project': 'project'}.get(kind)
            with self.store.connect() as db:   # by name, address, handle or phone number, however it is written
                hits = [graph.node_view(r) for r in knowledge.find(db, words, kinds=(want,) if want else knowledge.KINDS, limit=8,
                                                                    also=self.talk_marks(db))]
            if not hits:
                return {'found': [], 'searched': 'the Graph for "%s"' % words, 'note': talk_live.NOTHING_NOTE}
            return {'found': [{'id': h['id'], 'kind': TALK_KINDS[h['kind']], 'name': clamp(h['name'], 120),
                               **({'about': clamp(x, 160)} if (x := talk_about(h)) else {}),
                               **({'last': self.talk_when(h['last_at'])} if h.get('last_at') else {})} for h in hits]}
        if name == 'open_record':
            return self.talk_record(str(args.get('id') or ''), accounts)
        if name == 'recall':
            return self.talk_recall(' '.join(str(args.get('words') or '').split())[:200])
        raise ValueError('Unknown tool')

    def talk_recall(self, words):
        """recall: what the owner said or decided in earlier conversations and the notes (knowledge.recall, OpenClaw's
        memory search). Each excerpt marked <untrusted>, since it can quote anyone; with RECALL_NOTE. Off, failing or
        slow: nothing found, said plainly, never an error."""
        if not words:
            return {'error': 'Say what to look for.'}
        found = knowledge.recall(self.memory_search, words)
        if not found:
            return {'found': [], 'searched': 'earlier conversations and notes for "%s"' % words, 'note': talk_live.NOTHING_NOTE}
        mark = lambda r: ai_access.untrusted(clamp(' '.join(r['text'].split()), 600), 'conversation' if r['source'] == 'sessions' else 'notes')
        return {'found': [{'from': r['from'], **({'when': self.talk_when(r['at'])} if r['at'] else {}), 'text': mark(r)} for r in found],
                'note': talk_live.RECALL_NOTE}

    def memory_search(self, request):
        """OpenClaw's memory search, for knowledge.recall (memory-recall-run.mjs): one Gateway call with a short
        timeout. None when Node or the Gateway is away or slow."""
        try:
            result = subprocess.run([node_bin(self.config), str(ROOT / 'memory-recall-run.mjs')], env=node_env(self.config),
                                    input=json.dumps(request), capture_output=True, text=True, timeout=knowledge.RECALL_SECONDS)
            return json.loads(result.stdout or 'null')
        except (OSError, ValueError, subprocess.TimeoutExpired):
            return None

    def talk_named(self, words):
        """The person or organization in the Graph these words (or this phone number) name; None."""
        with self.store.connect() as db:
            return knowledge.named(db, words, also=self.talk_marks(db))

    def talk_marks(self, db):
        """Fleet members' names to match in the Graph (graph_find's also)."""
        return {k: m['name'] for k, m in self.graph_fleet_marks(db).items() if m['name']}

    def talk_message_rows(self, node, accounts, limit=8):
        """A record's latest messages for the voice, newest first: the ones its Graph page's timeline shows."""
        rows = knowledge.latest_messages(self.store, self.config, node, limit=limit) if accounts else []
        return [{'id': 'event:%d' % r['id'], 'title': clamp(' '.join(str(r['title'] or '').split()), 160), 'what': source_text(r)} for r in rows]

    def talk_messages_with(self, who, accounts):
        """search kind message for a person or organization (a name, a number or an id from search): their latest messages."""
        with self.store.connect() as db:
            hit = knowledge.record(db, who, also=self.talk_marks(db))
        if not hit:
            return {'found': [], 'searched': 'the Graph for someone named "%s"' % who, 'note': talk_live.NOTHING_NOTE}
        found = [{**m, 'kind': 'message'} for m in self.talk_message_rows(hit['id'], accounts)]
        record = {'id': hit['id'], 'kind': TALK_KINDS.get(hit['kind'], hit['kind']), 'name': clamp(hit['name'], 120)}
        if not found:
            return {'with': record, 'found': [], 'searched': 'the messages on the Graph page of %s' % record['name'], 'note': talk_live.NOTHING_NOTE}
        return {'with': record, 'found': found}

    def talk_record(self, rid, accounts):
        """One record for the voice, from what its own page shows: a person, organization or project (the Graph's page),
        a meeting (the Calendar's details), a message (its original) or a promise. card is what Talk's transcript shows."""
        if rid.startswith('event:') and rid[6:].isdigit() and accounts:
            meeting = self.store.meeting(accounts, int(rid[6:]), self.owner_emails())
            if meeting:
                when = 'all day ' + self.talk_when(meeting['start'])[:-6] if meeting['all_day'] else self.talk_when(meeting['start'])
                return {'id': rid, 'kind': 'meeting', 'title': clamp(meeting['title'], 200), 'when': when,
                        **({'where': clamp(meeting['location'], 160)} if meeting.get('location') else {}), 'with': meeting['people'][:12],
                        'card': {'kind': 'meeting', 'title': clamp(meeting['title'], 200), 'line': when, 'event': int(rid[6:])}}
            rows = self.store.events(accounts, event_ids=[int(rid[6:])])
            if rows:
                r = rows[0]
                return {'id': rid, 'kind': 'message', 'title': clamp(' '.join(str(r['title'] or '').split()), 200), 'what': source_text(r),
                        'text': clamp(str(r['body'] or ''), 1500),
                        'card': {'kind': 'message', 'title': clamp(' '.join(str(r['title'] or '').split()), 200), 'line': source_text(r), 'event': r['id']}}
            return {'error': 'That message or meeting is not there anymore.'}
        if rid.startswith('promise:') and rid[8:].isdigit():
            try:
                x = self.store.promise_page(int(rid[8:]))
            except ValueError:
                return {'error': 'No such promise.'}
            return {'id': rid, 'kind': 'promise', 'who': clamp(str(x['who']), 80), 'what': clamp(str(x['what']), 300),
                    'direction': 'the owner promised' if x['direction'] == 'mine' else 'promised to the owner', 'state': promise_state(x),
                    **({'due': x['due']} if x.get('due') else {}), 'made': self.talk_when(x['made_at']),
                    'card': {'kind': 'promise', 'title': clamp(str(x['what']), 200), 'line': clamp(str(x['who']), 80), 'promise': int(rid[8:])}}
        if not rid or rid.startswith(('team:', 'event:', 'promise:')):
            return {'error': 'No record with that id. Use search first.'}
        try:
            n = self.graph_action({'node_id': rid, 'limit': 6, 'events': 8})
        except ValueError:
            return {'error': 'No record with that id. Use search first.'}
        if n.get('kind') not in TALK_KINDS:
            return {'error': 'No record with that id. Use search first.'}
        about = talk_about(n)
        out = {'id': n['id'], 'kind': TALK_KINDS[n['kind']], 'name': clamp(n['name'], 120), **({'about': clamp(about, 200)} if about else {})}
        for key, size in (('headline', 200), ('bio', 400), ('notes', 600), ('from_gbrain', 600), ('closeness', 40), ('state', 60)):
            if n.get(key):
                out[key] = clamp(' '.join(str(n[key]).split()), size)
        with self.store.connect() as db:   # the moment of the latest contact, never a meeting ahead (last_at is a day)
            n = {**n, 'last_at': knowledge.last_contact(db, n['id']) or n.get('last_at')}
        for key in ('last_at', 'next_meeting'):
            moment = n[key].get('at') if isinstance(n.get(key), dict) else n.get(key)
            if moment and (said := self.talk_when(moment)):
                out[{'last_at': 'last', 'next_meeting': 'next_meeting'}[key]] = said + (
                    ' · ' + clamp(n[key]['title'], 120) if isinstance(n.get(key), dict) and n[key].get('title') else '')
        # What is open with them, as their page has it: to-dos and promises both ways (an organization's people's too)
        open_ = knowledge.open_with(self.store, self.config, n['id'], limit=5)
        todos = [c for c in (n.get('todos') or open_['todos']) if isinstance(c, dict)]
        if todos:
            out['open_todos'] = [{'id': c.get('id'), 'title': clamp(str(c.get('title') or ''), 160)} for c in todos[:5]]
        promises = [{'id': 'promise:%d' % p['id'], 'who': clamp(str(p['who']), 80), 'what': clamp(str(p['what']), 200),
                     'direction': 'the owner promised' if k == 'you_promised' else 'promised to the owner', **({'due': p['due']} if p.get('due') else {})}
                    for k in ('you_promised', 'they_promised') for p in open_[k]]
        if promises:
            out['promises'] = promises
        out['recent'] = [clamp(line.split(' ', 2)[-1], 200) for line in (n.get('recent') or [])[:8]]
        # Their latest messages, from every address and number merged into them (the page's timeline), each with an id
        # to read it: meetings ahead never crowd these out
        out['messages'] = self.talk_message_rows(n['id'], accounts, 6)
        around = [x for x in (n.get('around') or []) if isinstance(x, dict) and x.get('name')]
        if around:
            out['around'] = [clamp(x['name'], 80) for x in around[:6]]
        return {**out, 'card': {'kind': out['kind'], 'title': out['name'], 'line': out.get('about') or out.get('headline') or '', 'node': n['id']}}

    def lookups_view(self):
        """Settings, Look up work contacts: whether this Machine can look people up, and whether the owner has it on."""
        available = enrichment.people_available(self.config)
        try:
            with self.store.connect() as db:
                on = enrichment.people_on(db)
        except sqlite3.Error:
            on = True
        try:
            with self.store.connect() as db:
                required = bool(security_levels.careful_fleets(db))
        except sqlite3.Error:
            required = False
        return {'people_available': available, 'people': on, **({'required_off': True} if required else {})}

    def talk_actions_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner talks live, on the dashboard')
        return self.talk_action(name, args)

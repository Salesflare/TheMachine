"""A to-do's chat in the service (refactor PR 26; chat.py and the chat prompt do the rest): a turn of the chat, the
models it can run on and the fast setting, stopping a turn or its browser run, what it learned, and the gateway and
agent work it hands off to. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
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
import urllib.request

import agent_jobs
import browser_login
import chat_files
import chat_model
import contact_facts
import corrections
import fleet_reviews
import i18n
from machine import names as display_names
from machine.browser import run_tab
from machine.cards import CHAT_HANDLE
from machine.delivery.push import NOTICE_DECISION
from machine.chat import (
    AGENT_DO_IT_NOTE,
    AGENT_WORK_NOTE,
    card_chat_handoffs,
    chat_agent_text,
    chat_conversation,
    chat_draft,
    chat_excerpt,
    CHAT_FILES_ONLY,
    CHAT_HISTORY_LIMIT,
    chat_items,
    chat_ms,
    chat_name,
    CHAT_ON,
    CHAT_OWNER_WORDS,
    CHAT_PART,
    chat_person,
    chat_reply,
    chat_result_files,
    CHAT_STEP_FAILED,
    CHAT_STEP_HOW,
    chat_text,
    CHAT_UNDONE,
)
from machine.config import LOG, ROOT
from machine.model_usage import node_bin, node_env
from machine.store.cards import use_line
from machine.store.machine_cards import parked_redo
from machine.text import _address, clamp, encoded, shown_body, split_quoted_history
from models import background_model, claude_plan_route
import talk_live
from timeutil import local_tz, now
import todo_areas


def save_hours(path, values):
    """Write these settings into config.json as it is on disk now (other keys untouched), keeping a .bak."""
    path = Path(path)
    text = path.read_text()
    config = json.loads(text)
    config.update(values)
    backup = path.with_name(path.name + '.bak')
    for target, content in ((backup, text), (path, json.dumps(config, indent=2) + '\n')):
        temp = target.with_name(target.name + '.tmp')
        fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as handle:
            handle.write(content)
        os.replace(temp, target)


class CardChatApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'card_chat': 'card_chat_action', 'chat_stop': 'chat_stop_action',
               'chat_model_default': 'chat_model_action', 'chat_model_set': 'chat_model_action',
               'chat_fast_set': 'chat_model_action'}

    def card_chat(self, suggestion_id, cursor=None):
        """The chat view of one card (chat_items): read-only. While its run is going the dashboard asks about once a
        second with the last `cursor`; `unchanged` then means only the live reply (if any) moved."""
        if not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        if cursor is not None and (not isinstance(cursor, str) or len(cursor) > 4000):
            raise ValueError('Invalid cursor')
        with self.store.connect() as db:
            if not db.execute('SELECT 1 FROM suggestions WHERE id=?', (suggestion_id,)).fetchone():
                raise ValueError('Unknown suggestion')
            job = db.execute('SELECT job_id,session_job_id,status FROM preparations WHERE suggestion_id=?', (suggestion_id,)).fetchone()
            owner, results = self.card_chat_service(db, suggestion_id)
            own = chat_model.card_choice(db, suggestion_id)  # this chat's own model and thinking level (chat_model.py)
            kinds = {r[0] for r in db.execute('SELECT status FROM preparation_runs WHERE session_job_id=?', (job['session_job_id'] or job['job_id'],))} if job else set()
            fix_only = kinds == {'machine_fix'}
        # The cursor also carries a digest of what the service itself adds (sends, taps, results): when that moved
        # ("Sending to Sam…" became "Sent to Sam"), the whole chat comes back even if the conversation didn't.
        digest = hashlib.sha256(json.dumps([owner, results], sort_keys=True, default=str).encode()).hexdigest()[:16]
        gateway_cursor, _, seen = (cursor or '').rpartition('|') if cursor and '|' in cursor else (cursor, '', None)
        if seen is not None and seen != digest:
            gateway_cursor = None
        active = bool(job) and job['status'] in ('queued', 'starting', 'running')
        result = {'session': bool(job), 'active': active, 'status': job['status'] if job else None, 'model': own}
        if not job or fix_only:  # fix_only: Do it ran a computer-log fix (Store.machine_fix), no AI session to read
            return {**result, 'items': chat_items([], owner, results), 'cursor': None}
        found = self.card_chat_gateway({'session_key': 'agent:main:assistant-review-preparation-' + (job['session_job_id'] or job['job_id']),
                                        'cursor': gateway_cursor, 'limit': CHAT_HISTORY_LIMIT})
        if not isinstance(found, dict) or found.get('error') or not isinstance(found.get('messages', []), list):
            # Logged (once a minute at most: the dashboard asks every second during a run) with the helper's fixed word
            # for why, so a chat that shows "couldn't load" can be traced to a slow or signed-out Gateway.
            reason = found.get('reason') if isinstance(found, dict) and found.get('reason') in ('timeout', 'auth', 'offline', 'setup', 'other') else 'other'
            if time.monotonic() - getattr(self, '_chat_unavailable_logged', -1e9) >= 60:
                self._chat_unavailable_logged = time.monotonic()
                LOG.warning('card chat history unavailable suggestion=%s active=%s reason=%s', suggestion_id, active, reason)
            return {**result, 'items': chat_items([], owner, results), 'cursor': None, 'unavailable': True}
        flight = found.get('inFlightRun') if isinstance(found.get('inFlightRun'), dict) else None
        # The reply streams as it is written where the stream holds only the answer (OpenAI's final channel: the Gateway
        # leaves commentary out). Claude Code's stream also carries its notes before a tool call and doesn't say which
        # text is the answer until the run ends, so its chat shows Working… instead.
        result['live'] = ({'text': chat_text(flight.get('text'), chars=8000)}
                          if flight and active and not self.chat_run_notes(own, found.get('messages')) else None)
        result['cursor'] = found['deltaCursor'] + '|' + digest if isinstance(found.get('deltaCursor'), str) else None
        if found.get('kind') == 'delta' and gateway_cursor:
            return {**result, 'unchanged': True}
        return {**result, 'items': chat_items(found.get('messages'), owner, results), 'more': bool(found.get('hasMore'))}

    def chat_models(self, read=True):
        """The models a chat can pick (chat_model.Catalog), read again when old; read=False: the last reading only.
        None when there is none."""
        catalog = getattr(self, 'chat_catalog', None)
        if catalog is None:
            catalog = self.chat_catalog = chat_model.Catalog()
        return catalog.refresh(self.config) if read else catalog.models

    def chat_model_view(self):
        """Settings, Model and the chat pill: the models the sign-in offers, with their thinking levels, and the default
        for chats (chat_model.view). The list is the last reading; none yet reads `known: False`."""
        found = chat_model.view(self.config, self.chat_models(read=False))
        swap = background_model(self.config)
        found['background'] = '/'.join(swap) if swap else found['main']['model']  # what the top of Settings, Model names
        if swap and not chat_model.chosen(self.config):  # Help runs on the lighter model unless a model was picked
            found['help'] = chat_model.resolve(self.config, self.chat_models(read=False), {'model': '/'.join(swap)})
        return found

    def chat_model_default(self, args):
        """The default model and thinking level for chats (Settings, Model): checked against what the sign-in offers and
        saved in config.json, only what differs from OpenClaw's own, so the rest keeps following OpenClaw. In use from
        the next turn; OpenClaw's config and its Gateway are left as they are."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        models = self.chat_models()
        picked = chat_model.check(args, models, {**self.config, 'chat_model': None})
        value = chat_model.minimal({**self.config, 'chat_model': None}, models, picked) or None
        save_hours(self.config_path, {'chat_model': value})
        self.config['chat_model'] = value
        return self.chat_model_view()

    def chat_model_set(self, args):
        """One to-do chat's own model and thinking level (the pill under its message box), for its next turns. What is
        the same as the default for chats is not kept, so it keeps following that default."""
        suggestion_id = str(args.get('suggestion_id') or '')
        if not re.fullmatch(r'[a-f0-9]{16}', suggestion_id):
            raise ValueError('Unknown suggestion')
        models = self.chat_models()
        picked = chat_model.check(args, models, self.config)
        keep = chat_model.minimal(self.config, models, picked)
        with self.store.connect() as db:
            if not db.execute('SELECT 1 FROM suggestions WHERE id=?', (suggestion_id,)).fetchone():
                raise ValueError('Unknown suggestion')
            chat_model.set_card(db, suggestion_id, keep, now())
        return {'model': keep, 'resolved': chat_model.resolve(self.config, models, keep)}

    def chat_fast_set(self, args):
        """The person's Fast choice for to-do chats (the model menu under a chat's message box), kept in config.json
        (`chat_fast`, chat_model.fast_on) for every to-do chat, from the next message. Off removes it."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        if not isinstance(args.get('fast'), bool):
            raise ValueError('Say on or off')
        value = True if args['fast'] else None
        save_hours(self.config_path, {'chat_fast': value})
        self.config['chat_fast'] = value
        return self.chat_model_view()

    def chat_turn_fast(self, job, changing='', do_it_source=None):
        """Whether this to-do's turn runs fast (chat_model.fast_turn): only a turn the person waits on in its chat (a
        message, or a Do it they started there), with Fast on and a model that has a fast option. Background work
        (prepared ahead, reviews, a follow-up review's Change) never is. Logged with what the provider last served."""
        interactive = chat_model.interactive_turn(job.get('decision_id'), job.get('ahead'), bool(changing), do_it_source)
        if not interactive or not chat_model.fast_on(self.config):
            return False
        try:
            with self.store.connect() as db:
                own = chat_model.card_choice(db, job['suggestion_id'])
            fast, entry = chat_model.fast_turn(self.config, self.chat_models(), own, interactive)
        except (sqlite3.Error, OSError, ValueError) as error:
            LOG.error('chat fast error=%s', type(error).__name__)
            return False
        LOG.info('chat turn fast=%s model=%s%s', fast, (entry or {}).get('ref') or 'unknown',
                 ' last_served=' + entry['served'] if entry and entry.get('served') else '')
        return fast

    def chat_turn_args(self, suggestion_id):
        """provider, model and thinking for an owner's turn in this to-do's chat (chat_model.turn_args); {} when
        nothing was picked, so the turn runs as it always did."""
        try:
            with self.store.connect() as db:
                own = chat_model.card_choice(db, suggestion_id)
            if not chat_model.chosen(self.config, own):
                return {}
            return chat_model.turn_args(self.config, self.chat_models(), own)
        except (sqlite3.Error, OSError, ValueError) as error:
            LOG.error('chat model error=%s', type(error).__name__)
            return {}

    def chat_run_notes(self, own, messages=None):
        """Whether this chat's run streams its working notes with its answer: Claude Code (the Claude CLI route: the
        chat's model, or the session's own turns so far), whose live text holds every note it wrote before a tool call."""
        for message in reversed(messages if isinstance(messages, list) else []):
            if isinstance(message, dict) and message.get('role') == 'assistant' and message.get('provider'):
                if message['provider'] == 'claude-cli':
                    return True
                break
        try:
            model = chat_model.resolve(self.config, None, own or {})['model'] or ''
            return model.startswith('claude-cli/') or (model.startswith('anthropic/') and claude_plan_route(self.config))
        except (OSError, ValueError, TypeError, AttributeError):
            return True

    def chat_stop(self, suggestion_id, via=None):
        """The chat's Stop button: ends the card's running reply now and keeps what it said so far (its live text,
        read from the Gateway first). {'stopped': False} when it had already finished. The Browser view's Stop
        (via='browser', for the task on the tab it shows, browser_now) is the same stop, said in the chat as such, and
        it doesn't wait for the worker's next round: the page load in the run's own tab stops and the run is aborted in
        its session right away (stop_browser_run)."""
        if not re.fullmatch(r'[a-f0-9]{16}', str(suggestion_id or '')):
            raise ValueError('Unknown suggestion')
        with self.store.connect() as db:
            job = db.execute('SELECT job_id,session_job_id,status FROM preparations WHERE suggestion_id=?', (suggestion_id,)).fetchone()
        if not job or job['status'] not in ('queued', 'starting', 'running'):
            return {'stopped': False}
        text = ''
        if job['status'] != 'queued':
            found = self.card_chat_gateway({'session_key': 'agent:main:assistant-review-preparation-' + (job['session_job_id'] or job['job_id']),
                                            'cursor': None, 'limit': 1})
            flight = found.get('inFlightRun') if isinstance(found, dict) and isinstance(found.get('inFlightRun'), dict) else None
            with self.store.connect() as db:
                own = chat_model.card_choice(db, suggestion_id)
            # What it said so far stays, unless that can hold its working notes (Claude Code, chat_run_notes): then the
            # reply only says it stopped
            notes = self.chat_run_notes(own, found.get('messages') if isinstance(found, dict) else None)
            text = chat_reply(chat_text(flight.get('text'), chars=8000))[0] if flight and not notes else ''
        stopped = self.store.stop_chat(suggestion_id, job['job_id'], text, via)
        if stopped and via == 'browser':
            self.stop_browser_run(job['job_id'])
        return {'stopped': stopped}

    def stop_browser_run(self, job_id):
        """Right after the Browser view's Stop: the run's own tab stops loading (a navigation or form post on its way
        stops there), then its Gateway run is aborted now, in the background, instead of on the worker's next round.
        Its next tool call is refused already (tool_intent), so nothing more is clicked, typed or sent."""
        try:
            with self.store.connect() as db:
                tab = run_tab(db, job_id)
            base = (browser_login.endpoints(self.config) or [None])[0]
            if tab and base and urllib.parse.urlsplit(base).port == tab[1]:
                with browser_login.browser_cdp.Session(base, tab[0], timeout=3) as session:
                    session.call('Page.stopLoading')
        except (browser_login.browser_cdp.CdpError, OSError, KeyError, TypeError, AttributeError, ValueError, sqlite3.Error):
            pass  # the tab is gone or the browser is busy: the abort below still ends the run
        threading.Thread(target=self.stop_stale_runs, args=(self.preparation_gateway,), daemon=True, name='browser-stop').start()

    def card_chat_service(self, db, suggestion_id):
        """What the service itself knows of a card's chat: the source messages, the owner's notes and taps, what
        went out, and each preparation's saved results (by job ID)."""
        row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        try:
            ids = [int(i) for i in json.loads(row['event_ids'])[:20]]
        except (ValueError, TypeError):
            ids = []
        names, owner, kinds, metas = {}, [], {}, {}
        card = db.execute('SELECT title,owner_step,origin FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        own_files = chat_files.of_cards(db, [suggestion_id])
        # planned: only the owner can do its step; one of The Machine's own (origin machine) has Do it, never Plan it
        title, planned = (card['title'] or '', bool(card['owner_step']) and card['origin'] != 'machine') if card else ('', False)
        redo = bool(card and card['origin'] == 'machine' and parked_redo(db, suggestion_id))  # Redo it on a fix an update set aside
        for r in db.execute('SELECT id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids) if ids else []:
            m = json.loads(r['metadata'])
            kinds[r['id']], metas[r['id']] = r['kind'], m
            name = chat_person(str(m.get('sender_display') or '').strip() or str(m.get('from') or '').split('<')[0])
            if _address(m.get('from')) and name and '@' not in name and not m.get('from_me'):
                names[_address(m.get('from'))] = name
        for v in self.store.event_views(ids) if ids else []:
            v['body'] = shown_body(v['body'])[0]  # the model's quoted-history marker never shows in the chat
            kind = kinds.get(v.get('event_id'), '')
            via = v['kind'] if v['kind'] != 'signal' else kind.split('.')[0]
            who, at, text = chat_person(v['from'].split('<')[0]) or v['from'], chat_ms(v['occurred_at']), None
            parts = [p for p in CHAT_PART.finditer(v['body'] or '') if p[4].strip()]
            if parts:  # a conversation (Intercom, a thread): what was asked, then the note of whom the card names
                found = chat_conversation(v['body'], parts, title, self.config.get('owner_name'), metas.get(v.get('event_id')) or {})
                for n, (who, at, text, note) in enumerate(found):
                    owner.append({'kind': 'source', 'from': clamp(who, 120), 'via': via, 'title': clamp(v['title'], 200), 'text': text,
                                  'mine': False, 'at': at, **({'note': True} if note else {})})
                text = '' if found else None
                if found:
                    continue
            # The new part leads; a reply's quoted history folds under it
            quoted = chat_text(split_quoted_history(v['body'] or '', v['title'])[1], chars=3000) if text is None else ''
            text = chat_excerpt(v['body'], v['title']) if text is None else text
            if text or v['title']:
                # The owner's own words (New to-do) carry the files they made it with
                made = own_files.pop(suggestion_id, None) if kind == 'owner.card' else None
                owner.append({'kind': 'source', 'from': clamp(who, 120), 'via': via, 'title': clamp(v['title'], 200),
                              'text': text, 'mine': v['from'] == 'You', 'at': at, **({'files': made} if made else {}),
                              **({'quoted': quoted} if quoted and text else {})})
        # A chat source has only its channel and handle ("#DM U…"): name it after the person the card's sends go to
        for r in db.execute('SELECT payload FROM action_jobs WHERE suggestion_id=? ORDER BY created_at', (suggestion_id,)):
            try:
                person = (chat_draft(json.loads(r['payload'])) or {}).get('to', [])
            except ValueError:
                continue
            if person:
                break
        else:
            person = []
        for i in owner:
            if i['kind'] == 'source' and CHAT_HANDLE.fullmatch(str(i['from']).strip()):
                i['from'] = person[0] if len(person) == 1 else ''
        runs = [r['started_at'] for r in db.execute('SELECT started_at FROM preparation_runs WHERE suggestion_id=?', (suggestion_id,))]
        about = max(((i['at'], i['from']) for i in owner if i['kind'] == 'source' and not i['mine'] and i['from']), default=(0, ''))[1]  # the latest who wrote
        waiting = False  # with a teammate: Later means back to check in, not a snooze of the owner's
        sent_files = chat_files.listed(db, [r['id'] for r in db.execute("SELECT id FROM decisions WHERE suggestion_id=? AND choice='other' AND source='dashboard'", (suggestion_id,))])
        for r in db.execute("SELECT id,choice,feedback,source,created_at FROM decisions WHERE suggestion_id=? AND source IN ('dashboard','telegram','fleet','expiry','placed','intercom','intercom_replies','handled','plan') "
                            'ORDER BY rowid', (suggestion_id,)):
            at, via = chat_ms(r['created_at']), (' in Telegram' if r['source'] == 'telegram' else '')
            if r['source'] == 'expiry':  # its moment passed (Store.expire_passed); Undo takes this back like a tap
                owner.append({'kind': 'event', 'text': 'Closed by itself: no longer needed', 'choice': 'complete', 'at': at})
                continue
            if r['source'] == 'handled':  # newer messages show it done already (Store.close_handled); Undo takes it back
                owner.append({'kind': 'event', 'text': i18n.t('Closed by itself: {}', clamp(r['feedback'], 200)), 'choice': 'complete', 'at': at})
                continue
            if r['source'] == 'plan':  # a newer message overturned its plan (Store.plan_changed); Undo takes this back like a tap
                owner.append({'kind': 'event', 'text': i18n.t('Updated: {}', clamp(r['feedback'], 200)), 'choice': 'complete', 'at': at})
                continue
            if r['source'] == 'intercom_replies':  # drafted again as a reply in Intercom (Store.redraft_intercom_emails)
                owner.append({'kind': 'event', 'text': i18n.t('Intercom replies are on: writing the reply there'), 'at': at})
                continue
            if r['source'] == 'intercom':  # a teammate was assigned the conversation (Store.close_taken_intercom)
                owner.append({'kind': 'event', 'text': i18n.t('Closed by itself: {} took it in Intercom', r['feedback']) if r['feedback']
                              else i18n.t('Closed by itself: a teammate took it in Intercom'), 'choice': 'complete', 'at': at})
                continue
            if r['source'] == 'fleet' or r['choice'] != 'snooze':
                was, waiting = waiting, r['source'] == 'fleet' and r['id'].startswith('fleet-handoff-wait-')
                if r['source'] == 'fleet':
                    if r['choice'] == 'complete' and ' is on it · ' in (r['feedback'] or ''):  # a teammate took it on (silent acceptance)
                        owner.append({'kind': 'event', 'text': clamp(r['feedback'], 200), 'choice': 'complete', 'at': at})
                    elif r['choice'] == 'reject' and r['id'].startswith('fleet-withdrawn-'):  # the teammate who handed it took it back
                        owner.append({'kind': 'event', 'text': clamp(r['feedback'], 200), 'choice': 'reject', 'handoff': True, 'at': at})
                    continue
                if was and r['choice'] == 'accept':
                    owner.append({'kind': 'event', 'text': 'Brought it back for a check-in' + via, 'choice': 'checkin', 'mine': True, 'at': at})
                    continue
            elif waiting:
                owner.append({'kind': 'event', 'text': 'Moved the check-in' + via, 'choice': 'snooze', 'mine': True, 'at': at})
                continue
            if r['choice'] == 'other' and r['id'].startswith(talk_live.RELAY_PREFIX):
                continue   # Talk live handed this to the chat: the owner's own words are the talk lines
            if r['choice'] == 'other':
                attached = sent_files.get(r['id'], [])
                said = '' if attached and r['feedback'] in CHAT_FILES_ONLY else clamp(r['feedback'], 5000)
                owner.append({'kind': 'you', 'text': said, 'via': r['source'], 'at': at, **({'files': attached} if attached else {})})
            elif r['choice'] == 'use_sources':  # "Use this email for this to-do" (use_sources): "Added the email to this to-do"
                used = db.execute('SELECT event_ids,mail FROM card_uses WHERE decision_id=?', (r['id'],)).fetchone()
                if used:
                    owner.append({'kind': 'event', 'text': i18n.t(use_line(len(json.loads(used['event_ids'])), bool(used['mail']))) + via,
                                  'choice': 'use_sources', 'mine': True, 'at': at})
            elif r['choice'] == 'routine_change':  # Also change the routine, confirmed (routine_changes.save): its name
                owner.append({'kind': 'event', 'text': i18n.t('Changed the routine {}', r['feedback']), 'choice': 'routine_change', 'mine': True, 'at': at})
            elif r['choice'] in ('move', 'move_undo'):  # More, Move to (move_card): "Moved to Work"; its Undo takes the line back
                last = next((i for i in reversed(owner) if i.get('choice') == 'move'), None) if r['choice'] == 'move_undo' else None
                if last:
                    owner.remove(last)
                    continue
                moved = db.execute('SELECT area FROM card_moves WHERE decision_id=?', (r['id'],)).fetchone()
                if moved:
                    areas = todo_areas.areas(self.config.get('accounts', []))
                    line = todo_areas.moved_line(moved['area'], sum(a['id'] != todo_areas.PERSONAL for a in areas), self.config.get('accounts', []))
                    owner.append({'kind': 'event', 'text': (i18n.t(*line) if isinstance(line, tuple) else i18n.t(line)) + via,
                                  'choice': 'move', 'mine': r['source'] != 'placed', 'at': at})  # placed: it moved itself
            elif r['choice'] in CHAT_OWNER_WORDS:  # a send shows as what went out, below
                why = ': ' + clamp(r['feedback'], 300) if r['choice'] == 'reject' and r['feedback'] else ''
                taps = [i for i in owner if i.get('choice')]
                ran = any(0 <= chat_ms(t) - at < 120000 for t in runs)  # Do it on a snoozed card brings it back and starts it
                choice = 'unsnooze' if r['choice'] == 'accept' and taps and taps[-1]['choice'] == 'snooze' and not ran else r['choice']
                if taps and (choice == 'undo' or (taps[-1]['choice'], choice) in CHAT_UNDONE and at - taps[-1]['at'] < 60000):
                    owner.remove(taps[-1])
                    continue
                said = ('Unsnoozed' if choice == 'unsnooze' else 'Plan it' if choice == 'accept' and planned
                        else 'Started redoing the fix' if choice == 'accept' and redo else CHAT_OWNER_WORDS[choice])
                owner.append({'kind': 'event', 'text': said + via + why,
                              'choice': choice, 'mine': True, 'at': at})
        owner.extend(card_chat_handoffs(db, suggestion_id))
        owner.extend({**x, 'at': chat_ms(x['at'])} for x in fleet_reviews.chat_lines(db, suggestion_id))
        owner.extend(self.card_chat_learned(db, suggestion_id))
        owner.extend({**x, 'at': chat_ms(x['at'])} for x in corrections.chat_items(db, suggestion_id))  # fixed where it came from
        for r in db.execute('SELECT payload,status,source,created_at,approval_id,retry_at FROM action_jobs WHERE suggestion_id=? ORDER BY created_at', (suggestion_id,)):
            try:
                payload = json.loads(r['payload'])
            except ValueError:
                continue
            if r['source'] == 'voice':  # a yes to Talk live's confirm question: Undo while the send still waits (talk_live.py)
                wait = r['status'] == 'queued' and r['retry_at'] and r['retry_at'] > now()
                owner.append({'kind': 'event', 'text': 'Approved by voice', 'mine': True, 'at': chat_ms(r['created_at']) - 1,
                              **({'undo_voice': r['approval_id'], 'undo_until': chat_ms(r['retry_at'])} if wait else {})})
            draft = chat_draft(payload)
            if draft:
                if len(draft['to']) == 1 and _address(draft['to'][0]) and str(payload.get('to_name') or '').strip():
                    names.setdefault(_address(draft['to'][0]), chat_person(str(payload['to_name']).strip()))  # "Sent to Sam", not the address
                to = ', '.join(chat_name(t, names, about) for t in draft['to'][:3]) or (about.split() or ['them'])[0]
                to += CHAT_ON.get(draft['kind'], '')
                text = {'sent': f'Sent to {to}', 'cancelled': 'Send canceled', 'failed': f'Didn’t go out to {to}'}.get(r['status'], f'Sending to {to}…')
                if draft['kind'] == 'intercom':  # who it went as: the owner's own Intercom admin
                    who = clamp(' '.join(str(payload.get('as_name') or 'your Intercom admin').split()), 100)
                    text = {'sent': f'Sent as {who} in Intercom', 'cancelled': 'Send canceled', 'failed': 'Didn’t go out in Intercom'}.get(r['status'], f'Sending as {who} in Intercom…')
                owner.append({'kind': 'event', 'text': text, 'sent': draft['body'] if r['status'] == 'sent' else None,
                              'mine': r['source'] != 'auto' and r['status'] != 'failed', 'at': chat_ms(r['created_at'])})
            elif isinstance(payload.get('label'), str) and payload['label'].strip():
                # A step without a draft (a calendar change, a merge, a finish): its label, and how it went unless it went
                label, how = clamp(payload['label'], 120), CHAT_STEP_HOW.get(r['status'], '')
                owner.append({'kind': 'event', 'text': label + how, 'mine': r['status'] not in CHAT_STEP_FAILED, 'at': chat_ms(r['created_at'])})
        # How you write, learned from a note or an edit on this card: one line per channel it changed, with Edit to fix it
        for r in db.execute("SELECT at,text FROM rule_changes WHERE kind='voice' AND ref IN ("
                            "SELECT 'decision:'||id FROM decisions WHERE suggestion_id=? UNION SELECT 'edit:'||id FROM draft_edits WHERE suggestion_id=?) "
                            'ORDER BY id', (suggestion_id, suggestion_id)):
            channel = str(r['text']).split(' voice: ', 1)[0] if ' voice: ' in str(r['text']) else ''
            if channel:
                owner.append({'kind': 'event', 'text': i18n.t('Saved to How you write: {}', i18n.t('Everywhere') if channel == 'All' else channel),
                              'voice': channel, 'at': chat_ms(r['at'])})
        # Each preparation's own saved results: what it said and the drafts it left, in the order it saved them.
        results = {}
        for r in db.execute("SELECT c.job_id,c.params,c.started_at,c.error FROM preparation_calls c JOIN preparation_runs p ON p.job_id=c.job_id "
                            "WHERE p.suggestion_id=? AND c.tool='assistant_signals' ORDER BY c.started_at", (suggestion_id,)):
            try:
                params = json.loads(r['params'])
            except (ValueError, TypeError):
                continue
            args = params.get('args') if isinstance(params, dict) and isinstance(params.get('args'), dict) else {}
            if r['error'] or params.get('action') != 'prepare' or args.get('suggestion_id') != suggestion_id:
                continue
            actions = args.get('next_actions') if isinstance(args.get('next_actions'), list) else [args.get('next_action')]
            body, files = chat_result_files(args.get('reply') if str(args.get('reply') or '').strip() else args.get('body'))
            text = chat_reply(re.sub(r'\[([^\]\n]{1,200})\]\((?!https?:)[^)\s]{1,500}\)', r'\1', chat_text(body)))[0]
            drafts = [d for d in map(chat_draft, actions) if d][:3]
            for d in drafts:
                d['to'] = [chat_name(t, names, about) for t in d['to']]
            results.setdefault(r['job_id'], []).append({'kind': 'reply', 'text': text, 'drafts': drafts, 'files': files,
                                                       'at': chat_ms(r['started_at'])})
        # Do it on a to-do from the computer's logs (Store.machine_fix): how each run of its fix went, as its reply
        try:
            ran = {x.get('job_id'): x.get('text') for x in json.loads(db.execute('SELECT outcome FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()[0] or '{}').get('fix_results', [])}
        except (ValueError, TypeError, AttributeError):
            ran = {}
        for r in db.execute("SELECT job_id,finished_at FROM preparation_runs WHERE suggestion_id=? AND status='machine_fix'", (suggestion_id,)) if ran else []:
            if ran.get(r['job_id']):
                results[r['job_id']] = [{'kind': 'reply', 'text': str(ran[r['job_id']]), 'drafts': [], 'files': [], 'at': chat_ms(r['finished_at'])}]
        # The chat's Stop: what the run had said so far stays (unless it had saved a result), cut off with "…" and
        # marked Stopped on the reply itself (the dashboard's small note under it), also when it had said nothing yet
        # Stop in the Browser view says so as an event line; the reply shows only when the run had said something.
        for r in db.execute('SELECT job_id,text,at,via FROM chat_stops WHERE suggestion_id=? ORDER BY at', (suggestion_id,)):
            if r['via'] == 'browser':
                owner.append({'kind': 'event', 'text': 'Stopped from the browser', 'mine': True, 'at': chat_ms(r['at'])})
                if not (r['text'] or '').strip():
                    results.setdefault(r['job_id'], [])
                    continue
            if r['job_id'] not in results:
                text = (r['text'] or '').rstrip()
                results[r['job_id']] = [{'kind': 'reply', 'text': text + '…' if text and not text.endswith(('…', '...')) else text,
                                         'drafts': [], 'files': [], 'stopped': True, 'at': chat_ms(r['at'])}]
        # Work handed to a coding agent (Hand to Claude Code / Codex): when it went, each change asked of it, and what came back
        jobs = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='agent_jobs'").fetchone()  # only once agents are set up
        for r in db.execute('SELECT * FROM agent_jobs WHERE suggestion_id=? ORDER BY created_at', (suggestion_id,)) if jobs else []:
            name, r = display_names.agent_name(r['tool']), dict(r)
            def listed(key):
                try:
                    found = json.loads(r.get(key) or '[]')
                except ValueError:
                    return []
                return [x for x in found if isinstance(x, dict)] if isinstance(found, list) else []
            asks = [x for x in listed('asks') if str(x.get('text') or '').strip()]
            # The handoff is the first turn (its brief); each change asked of it after is the next one. Every turn's
            # answer follows the message it answers, also for jobs from before each answer was kept (read back from
            # the turn's own transcript in the job folder).
            owner.append({'kind': 'event', 'text': 'Handed to ' + name, 'mine': True, 'at': chat_ms(r['created_at'])})
            for ask in asks:
                owner.append({'kind': 'you', 'text': clamp(str(ask['text']), 5000), 'via': 'agent', 'to': name, 'at': chat_ms(ask.get('at'))})
            for answer in agent_jobs.turn_answers(r, self.agent_folder(r['id'])):
                files = answer['files'][:10]
                text, quiet, full = chat_agent_text(answer['summary'], files, full=True)
                owner.append({'kind': 'agent', 'id': r['id'], 'name': name, 'text': text, 'files': files, 'nothing_sent': quiet,
                              'at': answer['at'], **({'full': full} if full else {})})
            if r['status'] in ('failed', 'cancelled'):
                owner.append({'kind': 'event', 'text': f"{name} {'stopped' if r['status'] == 'failed' else 'cancelled'}", 'at': chat_ms(r['finished_at'] or r['updated_at'])})
        owner.extend(talk_live.lines(db, suggestion_id))  # what was said in a live conversation (Talk live)
        for i in owner:
            i.pop('choice', None)
        return owner, results

    @staticmethod
    def card_chat_learned(db, suggestion_id):
        """What this card's notes taught, from the database itself (never from what a reply says): each fact or rule
        saved from a note here (a channel voice shows as its own 'Saved to How you write' line). The chat shows them as
        quiet lines that open the learning on What I've learned. A fact says where it stands now: saved, removed
        (Undo), or condensed into another (`into`, that fact's id, or 0 when it went into a voice or a skill). One about a
        person, organization or project says which (`about`: id and name): it lives on that record's page. A contact
        detail moved onto someone's record (contact_facts.py) says whose (`record`, `name`), with that move's Undo."""
        out, about = [], {}
        for r in db.execute('SELECT a.fact_id,a.node_id,n.name FROM fact_about a JOIN graph_nodes n ON n.id=a.node_id JOIN facts f ON f.id=a.fact_id '
                            'JOIN decisions d ON d.id=f.decision_id WHERE d.suggestion_id=? AND a.removed_at IS NULL ORDER BY a.created_at,a.node_id', (suggestion_id,)):
            about.setdefault(r['fact_id'], {'id': r['node_id'], 'name': clamp(r['name'], 80)})
        for r in db.execute("SELECT f.id,f.kind,f.text,f.created_at,f.removed_at,f.merged_into FROM facts f JOIN decisions d ON d.id=f.decision_id "
                            "WHERE d.suggestion_id=? AND NOT EXISTS (SELECT 1 FROM facts o WHERE o.merged_into='fact:'||f.id) "
                            "ORDER BY f.created_at,f.id", (suggestion_id,)):
            into = str(r['merged_into'] or '')
            moved = contact_facts.moved_to(db, r['id']) if into.startswith(contact_facts.MOVED) else None
            if moved:
                out.append({'kind': 'learned', 'what': 'fact', 'id': r['id'], 'text': clamp(r['text'], 300), 'state': 'record', **moved, 'at': chat_ms(r['created_at'])})
                continue
            state = 'merged' if into else 'removed' if r['removed_at'] else 'saved'
            out.append({'kind': 'learned', 'what': 'draft' if r['kind'] == 'draft' else 'fact', 'id': r['id'], 'text': clamp(r['text'], 300),
                        'state': state, **({'into': int(into[5:]) if into.startswith('fact:') and into[5:].isdigit() else 0} if into else {}),
                        **({'about': about[r['id']]} if r['id'] in about and state == 'saved' else {}),
                        'at': chat_ms(r['created_at'])})
        return out

    def agent_work(self, suggestion_id, job=None):
        """Work handed to Claude Code or Codex on this card (agent_jobs.card_work), as a block for its chat turn or
        preparation: part of the card's state and the latest truth of what was done. Empty without any. `job`: the
        preparation it goes in; when that is the owner's own Do it after a finished job, the step that job left for them
        (a push, publish or deploy) is theirs to have run now (AGENT_DO_IT_NOTE)."""
        with self.store.connect() as db:
            if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='agent_jobs'").fetchone():
                return ''
            rows = db.execute('SELECT * FROM agent_jobs WHERE suggestion_id=? ORDER BY created_at', (str(suggestion_id),)).fetchall()
            do_it = bool(rows) and self.owner_do_it(db, job, rows[-1])
        def when(value):
            try:
                found = dt.datetime.fromisoformat(str(value))
            except ValueError:
                return ''
            return (found if found.tzinfo else found.replace(tzinfo=dt.timezone.utc)).astimezone(local_tz()).strftime('%a %Y-%m-%d %H:%M')
        lines = agent_jobs.card_work(rows[-3:], self.agent_folder, when)
        if lines and do_it:
            lines.append(AGENT_DO_IT_NOTE)
        return ('\n\n' + AGENT_WORK_NOTE + '\n' + '\n'.join(lines)) if lines else ''

    @staticmethod
    def owner_do_it(db, job, latest):
        """Whether this preparation is the owner's own Do it tap (dashboard or Telegram), made after the card's latest
        Claude Code or Codex job finished with a result they haven't closed or set aside. Not a run prepared ahead (nobody
        tapped), not a confirmed final step (that runs its own step) and not a chat message (that says what it wants).
        Without `job`, the card's preparation starting or running now."""
        if job is None:
            row = db.execute("SELECT p.suggestion_id,p.decision_id,p.action_id,s.early FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                             "WHERE p.suggestion_id=? AND p.status IN ('starting','running')", (latest['suggestion_id'],)).fetchone()
            job = row and {'suggestion_id': row['suggestion_id'], 'decision_id': row['decision_id'], 'ahead': bool(row['early']), 'finish': row['action_id']}
        if not isinstance(job, dict) or job.get('ahead') or job.get('finish') or not job.get('decision_id'):
            return False
        if str(job['decision_id']).startswith(NOTICE_DECISION):
            return False  # a notification's button: the owner hasn't seen the job's result (push.notice_decision_refused)
        if latest['status'] != 'result' or latest['outcome'] in ('done', 'set_aside'):
            return False
        tap = db.execute("SELECT created_at FROM decisions WHERE id=? AND suggestion_id=? AND choice='accept' AND source IN ('dashboard','telegram')",
                         (str(job['decision_id']), str(job.get('suggestion_id') or latest['suggestion_id']))).fetchone()
        return bool(tap) and str(tap['created_at']) >= str(latest['finished_at'] or latest['updated_at'] or '')

    def card_chat_gateway(self, request):
        """chat-history-run.mjs: the Gateway's chat.history for one preparation session; {'error'} when unavailable."""
        env = {**node_env(self.config), 'ASSISTANT_STATE_DIR': str(Path(self.config['database']).expanduser().resolve().parent),
               'OPENCLAW_CONFIG_PATH': os.path.abspath(Path(self.config.get('openclaw_config') or Path.home() / '.openclaw' / 'openclaw.json').expanduser())}
        try:
            result = subprocess.run([node_bin(self.config), str(ROOT / 'chat-history-run.mjs')], env=env,
                                    input=encoded(request), capture_output=True, text=True, timeout=40)
            if result.returncode == 0:
                return json.loads(result.stdout)
            if 'ERR_MODULE_NOT_FOUND' in (result.stderr or ''):  # its pinned Node packages aren't there: put them in
                self.chat_packages_install()
                return {'error': 'unavailable', 'reason': 'setup'}
            return {'error': 'unavailable'}
        except subprocess.TimeoutExpired:
            return {'error': 'unavailable', 'reason': 'timeout'}
        except (ValueError, OSError):
            return {'error': 'unavailable'}

    def chat_packages_install(self):
        """The chat helper's pinned Node packages (package-lock.json) are missing, say because npm ci failed during the
        install: put them in the way the installer does (npm ci, no install scripts), in the background and at most every
        10 minutes, so the chat's next read ("Trying again…") gets the replies instead of failing for good."""
        if time.monotonic() - getattr(self, '_chat_packages_tried', -1e9) < 600:
            return
        self._chat_packages_tried = time.monotonic()

        def install():
            import installer  # setup code, loaded only for this repair
            LOG.warning('card chat node packages missing; installed=%s', installer.install_node_packages(node_bin(self.config), ROOT))
        threading.Thread(target=install, name='chat-packages', daemon=True).start()

    def card_chat_action(self, name, args, owner_dashboard=False):
        if owner_dashboard and not args.get('cursor'):
            self.store.note_activity('opened', args.get('suggestion_id'))  # a to-do opened (its chat's first read)
        return self.card_chat(args.get('suggestion_id'), args.get('cursor'))

    def chat_stop_action(self, name, args, owner_dashboard=False):
        return self.chat_stop(args.get('suggestion_id'), via='browser' if args.get('via') == 'browser' else None)

    def chat_model_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner picks the model, on the dashboard')
        if name == 'chat_fast_set':
            return self.chat_fast_set(args)
        return self.chat_model_default(args) if name == 'chat_model_default' else self.chat_model_set(args)

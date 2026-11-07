"""Follow-ups in the service (follow_ups.py has the follow-ups themselves): the step that finds the owner's threads
waiting for an answer, bounces, the lines a to-do shows, a change from chat and the send. Moved out of assistant.App as
is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import logging
from pathlib import Path
import re
import sqlite3
import time
import uuid

import bounces
import follow_ups
import graph
import i18n
from machine.config import WORKSPACE
from machine.sources.calendar import company_domains
from machine.sources.gmail import Gmail
from machine.store.review import own_message
from machine.store.voices import conversation_of
from machine.text import _address
import model_budget
import next_actions
import own_addresses
import skills
from sources import MICROSOFT_SERVICES, SourceError
from timeutil import WORK_HOURS, in_hours, local_tz, now

LOG = logging.getLogger('personal-assistant')


NEWER_KINDS = ('gmail.message', 'slack.message', 'teams.message', 'whatsapp.message', 'linkedin.message', 'x.dm')


def newer_activity(db, event_ids, owner_slack_ids=(), teammates=(), domains=(), limit=5):
    """Messages already synced into a to-do's own conversations (its email thread, Slack thread or DM, chat) after its
    newest evidence: someone may have answered or handled it since. Only who and when, from what is stored; no model
    call and no message text. Newest last, at most `limit`, each {'id', 'at', 'channel', 'who'}."""
    ids = [i for i in event_ids or [] if isinstance(i, int)]
    if not ids:
        return []
    rows = db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids).fetchall()
    found, seen = [], set(ids)
    teammates = {str(e).lower(): name for e, name in dict(teammates).items()} if teammates else {}
    for row in rows:
        if row['kind'] not in NEWER_KINDS:
            continue
        m = json.loads(row['metadata'] or '{}')
        key = conversation_of(row['kind'], m)
        if not key or row['kind'] == 'slack.message' and not m.get('thread_ts') and not key.startswith('D'):
            continue  # a channel message outside a thread: the channel holds many other matters
        field = 'thread_id' if row['kind'] == 'gmail.message' else 'channel_id' if row['kind'] == 'slack.message' else 'chat_id' if m.get('chat_id') else 'conversation_id'
        latest = max(r['occurred_at'] for r in rows if r['account_id'] == row['account_id'])
        for e in db.execute(f"SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE account_id=? AND kind=? AND deleted=0 AND occurred_at>? "
                            f"AND json_extract(metadata,'$.{field}')=? ORDER BY occurred_at LIMIT 50", (row['account_id'], row['kind'], latest, key)):
            if e['id'] in seen:
                continue
            em = json.loads(e['metadata'] or '{}')
            # A Slack channel holds many matters: only the same thread counts there (a DM is one conversation).
            if row['kind'] == 'slack.message' and m.get('thread_ts') and em.get('thread_ts') != m['thread_ts'] and em.get('ts') != m['thread_ts']:
                continue
            seen.add(e['id'])
            if row['kind'] == 'gmail.message' and bounces.system_sender(em.get('from')):
                continue  # a delivery report answers nothing (bounces.py tells what bounced)
            found.append({'id': e['id'], 'at': e['occurred_at'], 'channel': e['kind'].split('.')[0], 'who': activity_who(e, em, owner_slack_ids, teammates, domains)})
    return sorted(found, key=lambda x: x['at'])[-limit:]


def activity_who(event, m, owner_slack_ids=(), teammates=(), domains=()):
    """Who wrote a newer message, in a few words: the owner, a teammate, someone at the same company, or their address."""
    address = _address(m.get('from'))
    if own_message(dict(event), owner_slack_ids):
        return 'the owner'
    if address and address in teammates:
        return f"{teammates[address] or address} (a teammate)"
    if address and own_addresses.email_domain(address) in domains:
        return f"{address} (same company)"
    return address or str(m.get('sender_name') or m.get('user_name') or m.get('from') or 'someone else')[:80]


class FollowUpsApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    # Automated follow-ups (follow_ups.py): drafted in a low-priority background pass, sent only through the outbox.
    def follow_up_annotate(self, db, boards):
        """The board view's follow-up state: per board on and the next date, per project its next follow-up or the note."""
        try:
            follow_ups.ensure(db)
            found = follow_ups.views(db, now(), self.follow_up_sendable(), self.follow_up_mine(), self.follow_up_own(db),
                                   self.follow_up_work())
        except sqlite3.Error:
            return
        for b in boards:
            b['follow_ups'] = found['boards'].get(b['id']) or {'on': False, 'next_at': None}
            for p in b['projects']:
                view = found['projects'].get(int(p['id'].split(':', 1)[1]))
                if view and (view['on'] or view.get('end') or view.get('reason') == 'bounced'):
                    p['follow_up'] = {k: view[k] for k in ('state', 'next_at', 'n', 'max', 'own', 'end', 'reason', 'pause')}

    def follow_up_project(self, db, node_id):
        """A project page's follow-ups: the setting that applies (its own or its board's), the next one, the note when a
        round ended, and what went out."""
        follow_ups.ensure(db)
        pid = int(str(node_id).split(':', 1)[1])
        p = db.execute('SELECT * FROM projects WHERE id=?', (pid,)).fetchone()
        if not p:
            return None
        settings, source = follow_ups.effective(db, p)
        view = follow_ups.views(db, now(), self.follow_up_sendable(), self.follow_up_mine(), self.follow_up_own(db),
                                   self.follow_up_work())['projects'].get(pid) or {}
        ends = [dict(r) for r in db.execute('SELECT n,moved,judged,at FROM follow_up_ends WHERE project_id=? ORDER BY at DESC LIMIT 4', (pid,))]
        return {'on': bool(settings and settings.get('on')), 'source': source, 'next_at': view.get('next_at'), 'state': view.get('state'),
                'reason': view.get('reason'), 'n': view.get('n'), 'max': (settings or {}).get('max'), 'ends': ends,
                'pause': follow_ups.paused(db, p, now()) if settings and settings.get('on') else None,
                'activity': follow_ups.activity(db, pid)}

    def follow_up_sendable(self):
        return follow_ups.sendable(self.config.get('accounts') or [])

    def follow_up_work(self):
        """The owner's work week for Only on work days (follow_ups.work_week): the work days and start of their Work hours
        in their time zone, and the side of each account (a project on no board is Personal by its accounts)."""
        return follow_ups.work_week(WORK_HOURS.get('days'), WORK_HOURS.get('start'), local_tz(),
                                    {a.get('id'): graph.account_side(a) for a in self.config.get('accounts', []) if a.get('id')})

    def follow_up_own(self, db):
        """The owner's addresses and full name, to tell their quoted earlier emails from someone else's."""
        emails = {str(e).lower() for a in self.config.get('accounts', []) for e in a.get('owner_emails', [a.get('email')]) if e}
        try:
            emails |= own_addresses.yours(db, self.config)
        except sqlite3.Error:
            pass
        return {'emails': emails, 'names': [self.config.get('owner_name') or '']}

    def follow_up_threads(self, mine, sendable, own, limit=follow_ups.BATCH * 2):
        """Read the real thread of due follow-ups once per waiting point (Gmail's thread, Outlook's conversation: who
        sent each message and when, nothing else), so the owner's earlier sends from another app count
        (follow_ups.thread_sends). Outside the drafting transaction; a thread that can't be read falls back to the
        quoted history."""
        with self.store.connect() as db:
            follow_ups.ensure(db)
            wanted = []
            # In the order they're drafted (follow_up_step), so the first ones drafted are the ones read first
            for item in sorted((x for x in follow_ups.plan(db, now(), sendable, mine, own, self.follow_up_work()) if x['state'] == 'due'),
                               key=lambda x: (not x['late'], x['next_at'])):
                msgs = follow_ups.messages(db, item['project']['id'], mine)
                theirs = max((i for i, m in enumerate(msgs) if not m['mine']), default=-1)
                _, row = follow_ups.latest_email(db, msgs[theirs + 1:])
                if row is None or db.execute('SELECT 1 FROM follow_up_threads WHERE event_id=?', (row['id'],)).fetchone():
                    continue
                meta = json.loads(row['metadata'] or '{}') if not isinstance(row['metadata'], dict) else row['metadata']
                wanted.append((row['id'], row['source_id'], row['account_id'], meta.get('thread_id') or meta.get('threadId')))
        accounts = {a.get('id'): a for a in self.config.get('accounts') or [] if isinstance(a, dict)}
        for event_id, message_id, account_id, thread_id in wanted[:limit]:
            account, sends = accounts.get(account_id), None
            if account and thread_id and account.get('service', 'gmail') in ('gmail', *MICROSOFT_SERVICES):
                try:
                    sends = follow_ups.thread_sends(self.follow_up_thread(account, thread_id), message_id, own['emails'] | {str(account.get('email') or '').lower()})
                except (SourceError, OSError, ValueError, KeyError) as error:
                    LOG.info('follow-up thread not read event=%s why=%s', event_id, str(error)[:80])
            with self.store.connect() as db:
                follow_ups.remember_thread(db, event_id, sends, now())

    def follow_up_chat(self, action):
        """A WhatsApp chat's newest messages, read now (read-only)."""
        return next_actions.WhatsAppTransport(self.config).read(action, ['messages', 'list', '--chat', action['chat_id'], '--limit', '20']).get('messages') or []

    def follow_up_pause(self, late=False):
        """None when an automated follow-up may be drafted now (model_budget.follow_up_pause): a usage limit holds it,
        and it waits before any other background work while usage runs high, unless it reached its longest wait."""
        limited = self.background_pause(owner=True)
        if limited:
            return limited
        return model_budget.follow_up_pause(self.paced_usage(), time.time(), late)

    def bounce_step(self):
        """Every five minutes, before follow-ups: reads newly collected mail for delivery reports (the first time, the
        ones collected before too: bounces.scan), clears addresses that work again, marks a follow-up that bounced and
        queues a fresh look-up of a bounced person (people enrichment, when it's on)."""
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            follow_ups.ensure(db)
            own = self.follow_up_own(db)['emails']
            flagged = bounces.scan(db, own)
            cleared = bounces.clear(db, now(), own)
            for event_id, address, _ in flagged:
                bounces.requeue_lookup(db, address)
                follow_ups.bounced(db, event_id, address, now())
        if flagged or cleared:
            LOG.info('bounces flagged=%s cleared=%s', len(flagged), len(cleared))
        return {'flagged': len(flagged), 'cleared': len(cleared)}

    def follow_up_lines(self, suggestion_id):
        """What a follow-up's preparation needs beyond a normal to-do: which follow-up it is, on which channel, what the
        earlier ones said (never the same again), and whether it judges if another one is worth it (past the minimum)."""
        with self.store.connect() as db:
            f = db.execute("SELECT * FROM follow_up_cards WHERE suggestion_id=? AND state='open'", (suggestion_id,)).fetchone()
            if not f:
                return ''
            p = db.execute('SELECT * FROM projects WHERE id=?', (f['project_id'],)).fetchone()
            settings = (follow_ups.effective(db, p)[0] if p else None) or follow_ups.defaults()
            earlier = follow_ups.earlier_texts(db, f['project_id'])
        channel = {'email': 'email', 'linkedin': 'LinkedIn', 'whatsapp': 'WhatsApp', 'slack': 'Slack', 'telegram': 'Telegram', 'intercom': 'Intercom'}[f['channel']]
        lines = [f"\n\nAutomated follow-up {f['n']} (at most {f['of_max']}) on the project {p['name'] if p else ''}: the owner wrote last and nobody answered. "
                 f"Draft one short follow-up as a {channel} draft (kind {f['channel']}), in the same conversation as the last messages listed, "
                 'in the owner\'s voice: refer to the last exchange in a few words, add something useful or one easy question, no guilt and no "just '
                 'checking in". Never repeat what an earlier follow-up said. Leave send_now out: the service decides how it goes.',
                 'If they or someone else answered since, or it is handled, save outcome:\'already_done\' instead.']
        if f['n'] > int(settings.get('min') or 0):
            lines.append(f"The minimum of {settings.get('min')} follow-ups went out. Judge from the thread and the project whether another one is still "
                         "worth it (by what was said, not by keywords). Either way, write the draft: you never end follow-ups yourself. When you would "
                         "stop, also save follow_up:'stop' with follow_up_why:<why, a few plain words, e.g. 9 unanswered emails since August>; the owner "
                         'sees it next to the draft and decides.')
        lines.append("The owner's word beats any judgment: when they ask for one anyway (keep trying, write one), write the draft, without "
                     "follow_up:'stop'. Never answer that nothing was sent or that follow-ups stopped.")
        if earlier:
            lines.append('Earlier follow-ups said (newest first; say something else):\n' + '\n'.join('- ' + ' '.join(t.split())[:300] for t in earlier))
        return '\n'.join(lines)

    def follow_up_change(self, args):
        """Change in the follow-up review: the owner's instruction rewrites the drafts of these follow-up to-dos (all
        checked, or one), each through its chat's path (a Change note, decide 'other', the preparation's next turn),
        at most follow_ups.DRAFTING at once (preparation_step). Nothing is sent; only the text changes (change_problem).
        {'changing': [{'id', 'revision'}], 'skipped': [ids no longer ready]}."""
        text = str(args.get('text') or '').strip()
        if not text:
            raise ValueError('Say what should change')
        if len(text) > follow_ups.CHANGE_MAX:
            raise ValueError(f'Keep it under {follow_ups.CHANGE_MAX} characters')
        ids = args.get('ids')
        if not isinstance(ids, list) or not ids or len(ids) > 100 or not all(isinstance(i, str) and re.fullmatch(r'[a-f0-9]{16}', i) for i in ids):
            raise ValueError('Say which follow-ups')
        changing, skipped = [], []
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            follow_ups.ensure(db)
            for sid in dict.fromkeys(ids):
                row = db.execute("SELECT s.status,s.next_action,p.status job FROM suggestions s JOIN follow_up_cards f ON f.suggestion_id=s.id "
                                 "LEFT JOIN preparations p ON p.suggestion_id=s.id WHERE s.id=? AND f.state='open'", (sid,)).fetchone()
                # Ready, or a rewrite that got stuck (its draft still the one before): Try again
                ready = row and (row['status'] == 'prepared' or row['status'] in ('instructions', 'accepted') and row['job'] == 'blocked')
                draft = next((x for x in next_actions.actions(row['next_action'] or 'null') if x['kind'] in ('email',) + next_actions.TEXT_KINDS),
                             None) if ready else None
                if not draft or db.execute("SELECT 1 FROM action_jobs WHERE suggestion_id=? AND status IN ('queued','sending','local_preparation')", (sid,)).fetchone():
                    skipped.append(sid)
                    continue
                decision = 'chat-' + uuid.uuid4().hex
                self.store._decide(db, sid, 'other', text, decision, 'dashboard')
                follow_ups.changing(db, sid, decision, draft['revision'], draft, now())
                changing.append({'id': sid, 'revision': draft['revision']})
        return {'changing': changing, 'skipped': skipped}

    def follow_up_send(self):
        """Send without asking: an open follow-up that's prepared goes through the outbox when its board or project said
        so, Careful is off, it's within the owner's hours and nothing about it is unusual (follow_ups.may_send_alone).
        Anything else stays a to-do that asks."""
        if not in_hours(dt.datetime.fromisoformat(now()).astimezone(local_tz())):
            return []
        sent, work = [], self.follow_up_work()
        with self.store.connect() as db:
            is_careful = follow_ups.careful(db)
            rows = db.execute("SELECT f.*,s.next_action,s.status FROM follow_up_cards f JOIN suggestions s ON s.id=f.suggestion_id "
                              "WHERE f.state='open' AND s.status='prepared' AND f.auto=0").fetchall()
            todo = []
            for f in rows:
                p = db.execute('SELECT * FROM projects WHERE id=?', (f['project_id'],)).fetchone()
                if p and follow_ups.paused(db, p, now()):
                    continue  # paused: it waits for the owner's Send, or the resume
                settings = follow_ups.effective(db, p)[0] if p else None
                if p and follow_ups.off_day(db, p, settings, now(), work):
                    continue  # Only on work days and today is a day off: it waits for the next work day, or the owner's Send
                drafts = [a for a in next_actions.actions(f['next_action']) if a.get('kind') in follow_ups.CHANNELS] if f['next_action'] else []
                draft = drafts[0] if len(drafts) == 1 else None
                attempt = db.execute('SELECT 1 FROM action_jobs WHERE suggestion_id=?', (f['suggestion_id'],)).fetchone()
                repeated = bool(draft) and follow_ups.repeats(draft.get('body'), follow_ups.earlier_texts(db, f['project_id']))
                if follow_ups.may_send_alone(settings, is_careful, draft, f['channel'], attempt, repeated):
                    todo.append((f['suggestion_id'], draft['revision']))
        for sid, revision in todo:
            try:
                result = self.store.confirm_action(sid, revision, f'auto-follow-up:{sid}:{revision}', 'auto_follow_up')
            except ValueError as error:
                LOG.info('follow-up kept for the owner why=%s', str(error)[:80])
                continue
            with self.store.connect() as db:
                follow_ups.sent_alone(db, sid)
            sent.append((sid, result.get('status')))
        return sent

    def follow_up_mine(self):
        ids = self.store.owner_user_ids
        return lambda e: own_message(e, ids) or follow_ups.mine_default(e)

    def follow_up_thread(self, account, thread_id):
        """An email thread read now from its source, never from a cache: Gmail's thread or Outlook's conversation, who sent
        each message and when, nothing else."""
        return Gmail(self.config, account).get('threads/' + str(thread_id), {'format': 'metadata', 'metadataHeaders': ['From']})

    def follow_up_recheck(self, job, action):
        """Right before a follow-up goes out: is the thread still as it was when the draft was written (follow_ups.basis)?
        None for a send that isn't a follow-up; else (why, news): why None (nothing new: it goes), 'bounced' (its To
        bounced since: news is the addresses; hold_bounced), 'changed' (a message
        was added since, by anyone: collected here, or in Gmail's thread or Outlook's conversation read fresh, or in the
        WhatsApp chat) or 'unchecked' (the fresh read failed: it doesn't go). LinkedIn and other channels: the collected
        messages. Outside any transaction."""
        with self.store.connect() as db:
            card, found = follow_ups.basis_of(db, job['suggestion_id'])
            if card is None:
                return None
            # Its To bounced since the draft (bounces.py): held, and moved to a working address when there is one
            bad = bounces.flags(db, action.get('to') or []) if action.get('kind') == 'email' else {}
            if bad:
                return 'bounced', sorted(bad)
            news = follow_ups.collected_since(db, card['project_id'], found, self.follow_up_mine())
            own = self.follow_up_own(db)
        channels = found.get('channels') or {}
        here = channels.get(action.get('kind')) or {'at': found.get('at')}
        try:
            if action.get('kind') == 'email':
                account_id, thread_id = (action.get('account_id'), action['thread_id']) if action.get('thread_id') else (here.get('account_id'), here.get('thread_id'))
                account = next((x for x in self.config.get('accounts') or () if isinstance(x, dict) and x.get('id') == account_id), None)
                if account and thread_id and account.get('service', 'gmail') in ('gmail', *MICROSOFT_SERVICES):
                    news = news + follow_ups.thread_since(self.follow_up_thread(account, thread_id), here,
                                                          own['emails'] | {str(account.get('email') or '').lower()})
            elif action.get('kind') == 'whatsapp':
                news = news + follow_ups.chat_since(self.follow_up_chat(action), here)
        except Exception as error:  # noqa: BLE001 - offline, signed out, an odd answer: fail closed
            LOG.info('follow-up thread not checked job=%s why=%s', job['id'], type(error).__name__)
            return 'unchecked', None
        if news:  # this to-do's own earlier send (sent, then reopened and drafted again) is no new message for it
            with self.store.connect() as db:
                news = follow_ups.without_own_sends(db, job['suggestion_id'], news)
        return ('changed', news) if news else (None, [])

    def follow_up_step(self, limit=follow_ups.BATCH):
        """Every five minutes: close follow-up to-dos that aren't needed any more, send the ones the owner said to send
        without asking, end rounds that got no reply, then draft the next due ones while nothing else waits."""
        mine, sendable = self.follow_up_mine(), self.follow_up_sendable()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            follow_ups.ensure(db)
            if not follow_ups.any_on(db) and not db.execute("SELECT 1 FROM follow_up_cards WHERE state='open'").fetchone():
                return {'drafted': 0}
            follow_ups.settle(db, now(), mine)
            for sid in follow_ups.rewrite_judged(db, now(), mine):  # closed on judgment by an earlier version: drafted after all
                decision_id = 'ahead:' + sid + ':' + uuid.uuid4().hex[:8]
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision_id, sid, 'prepare_ahead', '', 'assistant', now()))
                self.store.queue_preparation(db, sid, decision_id)
        self.follow_up_send()
        if not (self.config.get('review_worker') or {}).get('enabled'):
            return {'drafted': 0}
        drafted = 0
        with self.store.connect() as db:
            own = self.follow_up_own(db)
        self.follow_up_threads(mine, sendable, own)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            items = follow_ups.plan(db, now(), sendable, mine, own, self.follow_up_work())  # Only on work days: nothing due on a day off
            for item in items:
                if item['state'] == 'end':
                    follow_ups.end(db, item, now())
            # Only once the round could be counted (its thread read or tried, or the quoted history read): never on a guess
            due = sorted((x for x in items if x['state'] == 'due' and x.get('counted', True)), key=lambda x: (not x['late'], x['next_at']))
            due = follow_ups.spaced(db, due, now())  # just resumed from a pause: what was due comes one by one
            if not due:
                return {'drafted': 0}
            # Normal work first: no follow-up while another preparation waits, and only a few drafted at once
            others = db.execute("SELECT count(*) FROM preparations p WHERE p.status IN ('queued','starting','running') "
                                'AND p.suggestion_id NOT IN (SELECT suggestion_id FROM follow_up_cards)').fetchone()[0]
            drafting = db.execute("SELECT count(*) FROM preparations p JOIN follow_up_cards f ON f.suggestion_id=p.suggestion_id "
                                  "WHERE p.status IN ('queued','starting','running')").fetchone()[0]
            room = min(limit, follow_ups.DRAFTING - drafting, follow_ups.PER_DAY - follow_ups.drafted_today(db, now()))
            if others or room <= 0 or self.follow_up_pause(late=due[0]['late']):
                return {'drafted': 0, 'waiting': len(due)}
            for item in due[:room]:
                if item['late'] is False and drafted and self.follow_up_pause():
                    break
                if self.follow_up_card(db, item):
                    drafted += 1
        return {'drafted': drafted}

    def follow_up_card(self, db, item):
        """A follow-up to-do for one due project, prepared ahead (the owner's voice, the last exchange). A board's go
        into its grouped to-do; the first of a batch keeps its notification, the others don't add one each."""
        p, board, settings = item['project'], item['board'], item['settings']
        msgs = follow_ups.messages(db, p['id'], self.follow_up_mine())
        theirs = [m for m in msgs if not m['mine']]
        tail = [m for m in msgs if not theirs or m['at'] > theirs[-1]['at']]
        evidence = [m['id'] for m in reversed(tail[-3:])] + ([theirs[-1]['id']] if theirs else [])
        on_channel = [m['id'] for m in msgs if m['channel'] == item['channel']]
        if on_channel and on_channel[-1] not in evidence:
            evidence.append(on_channel[-1])  # switching channel: the conversation there, so the draft can go on it
        newer = newer_activity(db, evidence, self.store.owner_user_ids, {x['email']: x['name'] for x in self.teammate_addresses()},
                               company_domains(self.config))
        if any(x['id'] not in evidence for x in newer):
            return None  # something newer is still on its way into the project: next pass
        grouped = item['source'] == 'board'
        name = p['name']
        title = i18n.t('Follow up with {}', follow_ups.short_name(name, board['name'] if board else ''))[:90]  # the board names the rest
        # Since the round's first unanswered message (earlier sends from another app count too)
        days = (dt.datetime.fromisoformat(now()) - follow_ups.parse(item.get('round_at') or item['after_at'])).days
        body = i18n.t('No reply for {} days. Follow-up {} of at most {}.', days, item['n'], settings['max'])[:700]
        try:
            saved = self.store.suggest(f"follow-up:{p['id']}:{item['after']}", title, body, evidence, 'now', self.config.get('digest_at', '08:30'),
                                       work=self.is_work(sorted({r[0] for r in db.execute(
                                           f"SELECT account_id FROM events WHERE id IN ({','.join('?' * len(evidence))})", evidence)})),
                                       ahead=True, project=name, _db=db, owner_step=False)
        except ValueError as error:
            LOG.info('follow-up skipped project=%s why=%s', p['id'], str(error)[:80])
            return None
        if saved.get('duplicate') or saved.get('preview'):
            return None
        batch = grouped and db.execute("SELECT 1 FROM follow_up_cards WHERE board_id=? AND grouped=1 AND state='open'", (p['board_id'],)).fetchone()
        follow_ups.add_card(db, saved['id'], p, grouped, item, settings['max'], now())
        follow_ups.remember(db, saved['id'], follow_ups.basis(db, p['id']), now())  # what the draft is written against: checked again before it goes
        if batch:
            db.execute("UPDATE deliveries SET status='grouped',updated_at=? WHERE suggestion_id=? AND status='queued'", (now(), saved['id']))
        return saved['id']

    def follow_up_skill_lines(self, suggestion_id, rules='', room=None):
        """The owner's skills that are on and fit this open follow-up (follow_ups.fitting_skills: by the board's or the
        project's name, or named in the draft rules shown for it), with their instructions, ranked above the follow-up
        defaults (follow_ups.skill_note). '' when none fits or it isn't an open follow-up."""
        with self.store.connect() as db:
            f = db.execute("SELECT project_id,board_id FROM follow_up_cards WHERE suggestion_id=? AND state='open'", (suggestion_id,)).fetchone()
            if not f or not db.execute("SELECT 1 FROM sqlite_master WHERE name='skills'").fetchone():
                return ''
            p = db.execute('SELECT name FROM projects WHERE id=?', (f['project_id'],)).fetchone()
            b = db.execute('SELECT name FROM boards WHERE id=?', (f['board_id'],)).fetchone() if f['board_id'] else None
            on = [dict(r) for r in db.execute("SELECT name,slug,description,body FROM skills WHERE status='on' ORDER BY name")]
        fitting = follow_ups.fitting_skills(on, [b['name'] if b else '', p['name'] if p else ''], rules)
        root = Path(getattr(getattr(self, 'skills', None), 'workspace', None) or self.config.get('openclaw_workspace') or WORKSPACE) / 'skills' / skills.FOLDER
        return follow_ups.skill_note([{**k, 'path': str(root / k['slug'] / 'SKILL.md')} for k in fitting], room)

    def prep_skill_lines(self, suggestion_id, rules='', room=None):
        """The owner's skills for any preparation: an open follow-up's as before (follow_up_skill_lines); for any
        other to-do the skills that fit by its board, project or title or that its draft rules name, in full, and the
        other skills that are on as a short index to judge by meaning (follow_ups.prep_skill_note). '' for none."""
        lines = self.follow_up_skill_lines(suggestion_id, rules, room)
        with self.store.connect() as db:
            if lines or db.execute("SELECT 1 FROM follow_up_cards WHERE suggestion_id=? AND state='open'", (suggestion_id,)).fetchone():
                return lines
            if not db.execute("SELECT 1 FROM sqlite_master WHERE name='skills'").fetchone():
                return ''
            row = db.execute('SELECT title,project,event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                return ''
            names = [row['project'] or '']
            ids = [i for i in json.loads(row['event_ids'] or '[]') if isinstance(i, int)][:200]
            if ids and db.execute("SELECT 1 FROM sqlite_master WHERE name='event_projects'").fetchone():
                marks = ','.join('?' * len(ids))
                for p in db.execute(f'SELECT DISTINCT p.name,b.name AS board FROM event_projects e JOIN projects p ON p.id=e.project_id '
                                    f'LEFT JOIN boards b ON b.id=p.board_id WHERE e.event_id IN ({marks})', ids):
                    names += [p['name'] or '', p['board'] or '']
            on = [dict(r) for r in db.execute("SELECT name,slug,description,body FROM skills WHERE status='on' ORDER BY name")]
        root = Path(getattr(getattr(self, 'skills', None), 'workspace', None) or self.config.get('openclaw_workspace') or WORKSPACE) / 'skills' / skills.FOLDER
        on = [{**k, 'path': str(root / k['slug'] / 'SKILL.md')} for k in on]
        fitting = follow_ups.fitting_skills(on, names, rules, row['title'])
        picked = {k['slug'] for k in fitting}
        return follow_ups.prep_skill_note(fitting, [k for k in on if k['slug'] not in picked], room)

    def follow_up_change_note(self, job):
        """What a rewrite from the follow-up review's Change adds to its turn (follow_ups.change_note), else '': the
        rewrite rules and the skills that are on now, read from the database at the start of the turn, so a skill the
        owner added after the draft (or after the session began) is there with its file to read."""
        try:
            with self.store.connect() as db:
                if not follow_ups.change_of(db, job['suggestion_id'], job['job_id']):
                    return ''
                on = [dict(r) for r in db.execute("SELECT name,slug,description FROM skills WHERE status='on' ORDER BY name")] \
                    if db.execute("SELECT 1 FROM sqlite_master WHERE name='skills'").fetchone() else []
        except sqlite3.Error:
            return ''
        root = Path(getattr(getattr(self, 'skills', None), 'workspace', None) or self.config.get('openclaw_workspace') or WORKSPACE) / 'skills' / skills.FOLDER
        return '\n\n' + follow_ups.change_note([{**k, 'path': str(root / k['slug'] / 'SKILL.md')} for k in on])

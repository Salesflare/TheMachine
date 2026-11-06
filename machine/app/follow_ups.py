"""Follow-ups in the service (follow_ups.py has the follow-ups themselves): the step that finds the owner's threads
waiting for an answer, bounces, the lines a to-do shows, a change from chat and the send. Moved out of assistant.App as
is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import json
import logging
import re
import sqlite3
import time
import uuid

import bounces
import follow_ups
import graph
import model_budget
import next_actions
import own_addresses
from sources import MICROSOFT_SERVICES, SourceError
from timeutil import WORK_HOURS, in_hours, local_tz, now

LOG = logging.getLogger('personal-assistant')


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

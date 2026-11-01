"""Hand off by email (docs/help/handoffs.md): a Work to-do handed to a colleague who isn't on The Machine.

The Hand off sheet's By email shows what can go in the email (parts) and the owner ticks what does: a few lines of
context, the ready draft, the to-do's links and the draft's files. Assistant.handoff_email then puts an ordinary email
on the to-do, from the owner's own mailbox, built only from what was ticked, for the owner to read and send like any
email: nothing goes out unseen, and Careful mode applies to its Send. Plain text: no tracking pixels.

What may go follows the owner's Team Graph sharing (shared_graph.thread_labels): context taken from the to-do's
messages goes only when every one of them is shared with the team (Team), and a link only from such a message. Never
Personal or Only you content: without a Work Fleet's Team Graph, only the task in the owner's own words goes.

"Take this on in your own Machine": one short line at the bottom (Settings, Fleet; on by default, only in handoffs).
Its link's id is picked here, and the link is registered on the Network (cloud task_invites, with join: the Work Fleet
and a hash of their address, never the address) only after the email went out. Someone who signs up through it is
offered joining that Work Fleet; once they are in, the Network says their member id and the to-do moves to their
Machine as a normal Fleet handoff (fleet_requests.hand_off).

After the send the to-do waits under Later ("Handed to <name> by email") and becomes a promise to track ("<name> takes
this on"), made from the sent email once it synced. The review closes it when their reply says it's done, which closes
the to-do; Mark done on the to-do keeps the promise. Activity lists each handoff by email (activity_lines)."""
from __future__ import annotations

import base64
import datetime as dt
import json
import logging
import os
import re
import threading
import urllib.parse
import uuid

import activity_log
import fleet
import next_actions
import task_invites
from fleet_requests import card_reason
from i18n import t

LOG = logging.getLogger('personal-assistant')
SCHEMA = 'CREATE TABLE IF NOT EXISTS handoff_mails(card_id TEXT PRIMARY KEY,state TEXT NOT NULL,record TEXT NOT NULL,updated_at TEXT NOT NULL)'
PREFS = 'CREATE TABLE IF NOT EXISTS handoff_mail_prefs(key TEXT PRIMARY KEY,value TEXT NOT NULL)'
SITE = 'https://themachine.computer'
TAKE_DAYS = 30
LINKS = 3
OPEN = ('pending', 'snoozed', 'accepted', 'instructions')  # a to-do whose text is still its own account, not an outcome
ACTIONS = ('fleet_handoff_email_parts', 'fleet_handoff_take_line')


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def ensure(db):
    db.execute(SCHEMA)
    db.execute(PREFS)


def work_card(account_ids, accounts):
    """Whether a to-do is Work, as its Work or Personal label says (suggestion_scope)."""
    ids = json.loads(account_ids or '[]') if isinstance(account_ids, str) else (account_ids or [])
    return any(a['id'] in ids and a.get('scope', 'work' if str(a.get('boundary') or '').startswith('work:') else 'personal') == 'work'
               for a in accounts)


def take_link(config, take_id):
    """The take line's link: on the site for The Machine's own Network (it sends it on to the account pages), else on
    the Network this Machine uses."""
    base = urllib.parse.urlparse(task_invites.network_url(config, fleet))
    host = base.hostname or ''
    if host == 'themachine.computer' or host.endswith('.themachine.computer'):
        return f'{SITE}/take/{take_id}'
    return f'{base.scheme}://{base.netloc}/take/{take_id}'


def take_id():
    return base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip('=')


class HandoffMail:
    def __init__(self, app, checkin, check_at):
        self.app = app
        self.checkin = checkin  # handoff_checkin: when a handed-off to-do comes back to check in
        self.check_at = check_at  # promise_check_at
        self.soon = lambda fn: threading.Timer(5, fn).start()  # the take link right after the send (tests run it themselves)

    # -- storage (the record is sealed at rest: message_seal.DERIVED)
    def load(self, card_id, db=None):
        def read(db):
            ensure(db)
            row = db.execute('SELECT state,record FROM handoff_mails WHERE card_id=?', (str(card_id),)).fetchone()
            return (row['state'], json.loads(row['record'])) if row else (None, None)
        if db is not None:
            return read(db)
        with self.app.store.connect() as db:
            return read(db)

    def save(self, card_id, state, record, db=None):
        def write(db):
            ensure(db)
            db.execute('INSERT INTO handoff_mails(card_id,state,record,updated_at) VALUES(?,?,?,?) ON CONFLICT(card_id) DO UPDATE SET '
                       'state=excluded.state,record=excluded.record,updated_at=excluded.updated_at',
                       (str(card_id), state, json.dumps(record, ensure_ascii=False), now()))
        if db is not None:
            return write(db)
        with self.app.store.connect() as db:
            write(db)

    # -- the setting: Settings, Fleet
    def take_line(self):
        with self.app.store.connect() as db:
            ensure(db)
            row = db.execute("SELECT value FROM handoff_mail_prefs WHERE key='take_line'").fetchone()
        return not row or row['value'] != 'off'

    def set_take_line(self, on):
        with self.app.store.connect() as db:
            ensure(db)
            db.execute("INSERT OR REPLACE INTO handoff_mail_prefs(key,value) VALUES('take_line',?)", ('on' if on else 'off',))
        return {'take_line': bool(on)}

    # -- what can go
    def card(self, card_id):
        with self.app.store.connect() as db:
            card = db.execute('SELECT * FROM suggestions WHERE id=?', (str(card_id),)).fetchone()
        if not card:
            raise ValueError('No such to-do')
        if not work_card(card['account_ids'], self.app.config.get('accounts', [])):
            raise ValueError('Hand off by email is for Work to-dos')
        return card

    def team_events(self, card):
        """The to-do's messages, and which of them the Team Graph shares with the team: (all of them, the shared ids)."""
        ids = json.loads(card['event_ids'] or '[]')
        with self.app.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT id,account_id,kind,title,metadata FROM events WHERE deleted=0 AND id IN '
                                                '(SELECT value FROM json_each(?))', (json.dumps(ids),))]
            network = getattr(self.app, 'fleet', None)
            labels = network.thread_labels(db, rows) if network and rows else {}
        work = set(fleet.work_accounts(self.app.config))
        team = {r['id'] for r in rows if r['account_id'] in work and (labels.get(r['id']) or {}).get('share') == 'team'}
        return rows, team

    def ready_draft(self, card):
        """The to-do's own email draft, ready to send (not a handoff email made here): the action, else None."""
        if card['status'] != 'prepared' or not card['next_action']:
            return None
        value = json.loads(card['next_action'])
        acts = value.get('actions') if isinstance(value, dict) and value.get('kind') == 'menu' else [value]
        state, record = self.load(card['id'])
        mine = (record or {}).get('to') if state == 'drafted' else None
        return next((a for a in acts or [] if isinstance(a, dict) and a.get('kind') == 'email' and a.get('body')
                     and not a.get('delegate') and [x.lower() for x in a.get('to') or []] != [mine]), None)

    def parts(self, card_id):
        """What the Hand off sheet offers for an email: each part with a key, all ticked by default, and the take line's
        default. Context from the to-do's messages only when every one of them is shared with the team."""
        card = self.card(card_id)
        rows, team = self.team_events(card)
        shared = bool(rows) and len(team) == len(rows) and set(json.loads(card['account_ids'] or '[]')) <= set(fleet.work_accounts(self.app.config))
        lines = []
        if shared and card['status'] in OPEN:
            why = card_reason(card['body'])
            if why:
                lines.append({'key': 'why', 'text': why})
        found = self.app.fleet.handoff_draft(card['id']) if getattr(self.app, 'fleet', None) else {}
        if shared and found.get('contact'):
            lines.append({'key': 'contact', 'text': t('Contact: {}', found['contact'])})
        if card['due']:
            lines.append({'key': 'due', 'text': t('Due {}', str(card['due'])[:10]), 'due': str(card['due'])[:10]})
        links = []
        for r in rows:
            url = str(json.loads(r['metadata'] or '{}').get('source_url') or '').strip()
            if r['id'] in team and url.startswith('https://') and len(url) <= 500 and all(x['url'] != url for x in links):
                links.append({'key': f'link:{len(links)}', 'title': fleet.clean(r['title'], 120), 'url': url})
        draft = self.ready_draft(card) if shared else None
        files = [{'key': f'file:{n}', 'name': f['name'], 'size': f.get('size', 0)} for n, f in enumerate((draft or {}).get('attachments') or [])]
        return {'suggestion_id': card['id'], 'shared': shared, 'lines': lines, 'links': links[:LINKS],
                'draft': {'key': 'draft', 'to': draft.get('to') or [], 'subject': draft.get('subject') or ''} if draft else None,
                'files': files, 'take': self.take_line(), 'task': found.get('task') or card['title']}

    # -- the email
    def body(self, task, me, context, links, draft, take_url):
        """The email, built only from what the owner ticked. Plain text: no pixel, no tracking link."""
        subject = t('Could you take this on: {}', task['title'])[:120]
        out = [t('Hi there,'), t('Could you take this on?'), '\n'.join(x for x in (task['title'], task.get('summary', '')) if x)]
        if context:
            out.append('\n'.join(context))
        if links:
            out.append('\n'.join([t('Links:'), *(f"{x['title']}: {x['url']}" if x['title'] else x['url'] for x in links)]))
        if draft:
            head = [t('To: {}', ', '.join(draft.get('to') or [])), t('Subject: {}', draft.get('subject') or '')]
            out.append('\n'.join([t('The draft is ready to send:'), *head, '', next_actions.draft_text(draft).strip()]))
        out.append(t('Just reply to this email to let me know.'))
        out.append(t('Best,') + '\n' + (task_invites.first_name(me) or me))
        if take_url:
            out.append(t('Take this on in your own Machine: {}', take_url))
        return subject, '\n\n'.join(x for x in out if x)

    def prepare(self, card_id, email, name='', title='', summary='', keep=None, take=None):
        """The handoff email on the to-do, for the owner to read and send. keep: the keys of the parts the owner left
        ticked (all of them when left out); take: the take line (the setting when left out)."""
        email = str(email or '').strip()
        if not task_invites.EMAIL.fullmatch(email) or len(email) > 254:
            raise ValueError('Give their email address')
        offered = self.parts(card_id)
        card = self.card(card_id)
        keys = {x['key'] for x in [*offered['lines'], *offered['links'], *offered['files'], *([offered['draft']] if offered['draft'] else [])]}
        keep = keys if keep is None else {k for k in keep if isinstance(k, str)} & keys
        take = offered['take'] if take is None else take is True
        me = str(self.app.config.get('owner_name') or '').strip()
        task = task_invites.clean({'kind': 'handoff', 'title': str(title or '').strip() or card['title'],
                                   'summary': str(summary or '').strip() or offered['task'], 'due': str(card['due'] or '')[:10], 'from_name': me})
        context = []
        for x in offered['lines']:
            if x['key'] in keep:
                context.append(t('It would be great to have it by {}.', task_invites.spoken_day(x['due'])) if x['key'] == 'due' else x['text'])
        links = [x for x in offered['links'] if x['key'] in keep]
        ready = self.ready_draft(card) if offered['draft'] else None
        draft = ready if ready and 'draft' in keep else None
        files = [f for n, f in enumerate((ready or {}).get('attachments') or []) if f'file:{n}' in keep]
        refs = [ref for ref in self.app.fleet.work_fleets()] if getattr(self.app, 'fleet', None) else []
        ref = next((r for r in refs if set(json.loads(card['account_ids'] or '[]')) & set(self.app.fleet.fleet_accounts(r))), refs[0] if refs else None)
        tid = take_id() if take and ref else None
        url = take_link(self.app.config, tid) if tid else SITE if take else None
        subject, body = self.body(task, me, context, links, draft, url)
        allowed = json.loads(card['account_ids'] or '[]')
        mail = [a for a in self.app.config.get('accounts', []) if next_actions.mail_account(a)]
        order = [a for a in mail if a['id'] in allowed] + [a for a in mail if a['id'] not in allowed]
        action = None
        for account in order:
            try:
                action = next_actions.validate({'kind': 'email', 'label': 'Send', 'account_id': account['id'], 'to': [email],
                                                'subject': subject, 'body': body}, self.app.config, allowed)
                break
            except ValueError as error:
                if 'Outlook account' not in str(error) and 'company' not in str(error):
                    raise
        if not action:
            raise ValueError('This to-do has no Gmail or Outlook account to send from')
        if files:
            action['attachments'] = [dict(f) for f in files]  # the ready draft's own files, as the owner reviewed them there
        self.app.handoff_mail_draft(card['id'], f'An email handing this to {email}. Read it, change it if you like, and send it yourself.',
                                    next_action=action, outcome={'state': 'needs_you', 'needs': 'read and send the handoff email'})
        self.save(card['id'], 'drafted', {'to': email.lower(), 'name': fleet.clean(name, 80) or email, 'title': task['title'],
                                          'summary': task.get('summary', ''), 'fleet': ref if tid else None, 'take_id': tid,
                                          'take_url': url if tid else None, 'at': now()})
        return {'card_id': card['id'], 'task': task}

    # -- after the send (the outbox, inside its transaction)
    def sent(self, db, action, job, result):
        """The handoff email went out: the to-do waits under Later, to check in if nothing comes, and the take link is
        registered right after. False when this send isn't one."""
        state, record = self.load(job['suggestion_id'], db)
        if state != 'drafted' or action.get('kind') != 'email' or [str(a).lower() for a in action.get('to') or []] != [record['to']]:
            return False
        card = db.execute('SELECT status,urgent,due FROM suggestions WHERE id=?', (job['suggestion_id'],)).fetchone()
        if not card or card['status'] != 'prepared':
            return False
        self.app.handoff_mail_wait(db, job['suggestion_id'], self.checkin(bool(card['urgent']), card['due']))
        record.update(sent_at=now(), account_id=action.get('account_id'), rfc=(result or {}).get('rfc_message_id') or job.get('rfc_message_id') or '',
                      take_sent=bool(record.get('take_url')) and record['take_url'] in str(action.get('body') or ''))
        self.save(job['suggestion_id'], 'waiting', record, db)
        if record['take_sent']:
            self.soon(self.register)
        return True

    # -- the Network round (fleet.py calls it with the task pages' round)
    def round(self):
        for step in (self.register, self.track, self.moves):
            try:
                step()
            except (ValueError, OSError, KeyError, TypeError) as error:
                LOG.warning('handoff by email %s error=%s', step.__name__, type(error).__name__)

    def waiting(self):
        with self.app.store.connect() as db:
            ensure(db)
            return [(r['card_id'], json.loads(r['record'])) for r in db.execute("SELECT card_id,record FROM handoff_mails WHERE state='waiting'")]

    def register(self):
        """The take links of sent emails, once each: the Network learns the Work Fleet and a hash of the address."""
        network = getattr(self.app, 'fleet', None)
        for card_id, record in self.waiting():
            if not network or not record.get('take_sent') or record.get('invite_id') or record.get('unsupported'):
                continue
            request = record.get('request_id') or uuid.uuid4().hex
            made = network.relay.call('POST', '/task-invite', {
                'action': 'create', 'kind': 'handoff', 'id': record['take_id'], 'request_id': request, 'days': TAKE_DAYS,
                'sealed': task_invites.seal({'kind': 'handoff', 'title': 'A to-do'})[0],  # the page holds nothing: the key is dropped
                'join': {'fleet': record['fleet'], 'to': task_invites.hashed_email(record['to'])}})
            state, record = self.load(card_id)
            if made.get('id') != record['take_id'] or not made.get('take_url'):  # a Network from before take links
                record['unsupported'] = True
                if made.get('id'):
                    network.relay.call('POST', '/task-invite', {'action': 'revoke', 'id': made['id']})
            else:
                record['invite_id'] = made['id']
            self.save(card_id, state, record)

    def sent_event(self, db, record):
        """The sent email as it synced: by its Message-ID, else to them with this subject."""
        since = (dt.datetime.fromisoformat(record['sent_at']) - dt.timedelta(hours=1)).isoformat()
        for r in db.execute("SELECT id,account_id,occurred_at,title,metadata FROM events WHERE account_id=? AND kind='gmail.message' AND deleted=0 "
                            "AND occurred_at>=? AND instr(metadata,'\"SENT\"')>0 ORDER BY occurred_at LIMIT 200", (record.get('account_id'), since)):
            m = json.loads(r['metadata'] or '{}')
            if record.get('rfc') and str(m.get('message-id') or '').strip() == record['rfc'].strip():
                return r
            if not record.get('rfc') and record['to'] in str(m.get('to') or '').lower() and record['title'] in str(r['title'] or ''):
                return r
        return None

    def track(self):
        """The promise "<name> takes this on", from the sent email once it synced, kept in step with the to-do: closed
        by the review when their reply says it's done (the to-do then closes), kept when the owner marks the to-do done,
        dropped when it is Not needed."""
        store = self.app.store
        for card_id, record in self.waiting():
            with store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                card = db.execute('SELECT status,event_ids,due FROM suggestions WHERE id=?', (card_id,)).fetchone()
                if not card:
                    self.save(card_id, 'dropped', record, db)
                    continue
                if not record.get('promise_id'):
                    event = self.sent_event(db, record)
                    if event:
                        record['promise_id'] = self.app.handoff_mail_promise(
                            db, card_id, json.loads(card['event_ids'] or '[]'), record['name'][:80], ('take this on: ' + record['title'])[:140],
                            card['due'], self.check_at('theirs', card['due'], event['occurred_at']), event)
                        self.save(card_id, 'waiting', record, db)
                promise = db.execute('SELECT status,suggestion_id FROM promises WHERE id=?', (record.get('promise_id'),)).fetchone() if record.get('promise_id') else None
            if card['status'] in ('completed', 'rejected'):
                if promise and promise['status'] == 'open':
                    store.update_promise({'id': record['promise_id'], 'status': 'kept' if card['status'] == 'completed' else 'dropped',
                                          'reason': 'Marked done' if card['status'] == 'completed' else 'Not needed'}, source='dashboard')
                self.save(card_id, 'done', record)
            elif promise and promise['status'] == 'kept':
                store.decide(card_id, 'complete', t('{} says it’s done', task_invites.first_name(record['name']) or record['name']),
                             'handoff-mail-done-' + card_id, 'fleet')
                self.save(card_id, 'done', record)

    def moves(self):
        """They signed up through the take link and are in the Work Fleet now: the to-do moves to their Machine as a normal
        Fleet handoff, and the promise goes with it."""
        network = getattr(self.app, 'fleet', None)
        live = {r['invite_id']: (card_id, r) for card_id, r in self.waiting() if r.get('invite_id')}
        if not network or not live:
            return
        found = network.relay.call('POST', '/task-invite', {'action': 'status', 'ids': list(live)[:50]})
        for invite_id, member in (found.get('members') or {}).items():
            if invite_id not in live or not isinstance(member, dict) or member.get('fleet') != live[invite_id][1].get('fleet'):
                continue
            card_id, record = live[invite_id]
            try:
                network.directory(refresh=True)
                network.hand_off(card_id, member['fleet'], str(member.get('member_id') or ''), record['title'], record.get('summary') or record['title'],
                                 None, sources=False)
            except ValueError as error:  # not in the directory yet, or the to-do changed: next round
                LOG.info('handoff by email move waits error=%s', error)
                continue
            if record.get('promise_id'):
                try:
                    self.app.store.update_promise({'id': record['promise_id'], 'status': 'dropped', 'reason': 'Moved to their Machine'})
                except ValueError:
                    pass
            record['moved_at'] = now()
            self.save(card_id, 'moved', record)

    # -- for the dashboard
    def annotate(self, db, suggestions):
        ensure(db)
        rows = {r['card_id']: r for r in db.execute("SELECT card_id,state,record FROM handoff_mails WHERE state IN ('waiting','done')")}
        if not rows:
            return
        for s in suggestions:
            row = rows.get(str(s.get('id')))
            if not row:
                continue
            record = json.loads(row['record'])
            promise = db.execute('SELECT status FROM promises WHERE id=?', (record['promise_id'],)).fetchone() if record.get('promise_id') else None
            kept = s.get('status') == 'completed' or (promise and promise['status'] == 'kept')
            s['handoff_mail'] = {'name': record['name'], 'state': row['state'],
                                 'promise': 'kept' if kept else 'open' if promise or row['state'] == 'waiting' else None}

    def action(self, name, args):
        if name == 'fleet_handoff_email_parts':
            return self.parts(str(args.get('suggestion_id') or ''))
        if name == 'fleet_handoff_take_line':
            return self.set_take_line(args.get('on') is True)
        raise ValueError('Unknown handoff action')


def status_text(state):
    return {'waiting': t('Handed off by email'), 'done': t('Done'), 'moved': t('Moved to their Machine'), 'dropped': t('Not needed')}[state]


def activity_lines(db, limit):
    """Activity (activity_log.py): each handoff by email once it went out, with how it stands."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='handoff_mails'").fetchone():
        return []
    out = []
    for r in db.execute("SELECT card_id,state,record,updated_at FROM handoff_mails WHERE state IN ('waiting','done','moved','dropped') "
                        'ORDER BY updated_at DESC LIMIT ?', (limit,)):
        record = json.loads(r['record'])
        if not record.get('sent_at'):
            continue
        out.append(activity_log._line('fleet', 'handoff-mail:' + r['card_id'], record['sent_at'],
                                      t('To {}: {}', activity_log._clip(record.get('name'), 60), activity_log._clip(record.get('title'), 200)),
                                      'done', status_text(r['state']), t('Email'), None,
                                      todo={'id': r['card_id'], 'title': record.get('title') or ''}))
    return out


activity_log.register('fleet', activity_lines)

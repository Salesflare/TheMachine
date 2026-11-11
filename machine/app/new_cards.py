"""New to-dos in the service: one the owner adds (new_card) and where it goes, one a connected AI adds (ai_card),
one for a coding agent with its source messages, background and chat (agent_card), and whether a card counts as
Work. Moved out of assistant.App as is. A mixin of assistant.App (APP_MIXINS)."""
import datetime as dt
import hashlib
import json
import sqlite3
import uuid

import agent_jobs
import chat_files
import graph
import i18n
from machine.cards import card_task
from machine.config import WORKSPACE
from machine.store.cards import owner_title
from machine.store.facts import suggestion_scope
from machine.store.views import source_lines_shown
from machine.text import body_after_title
import missed_work
import next_actions
import own_addresses
from sources import mail_account, MAIL_SERVICES
from timeutil import now
import todo_areas


def owner_card_area(db, accounts, node_ids=(), text=''):
    """Where a to-do the owner adds without an area goes: (account id, open: the area ids to place it in later). Its
    only area when they have one; else the area its people and organizations point to (todo_areas.pointed: their side,
    the accounts they were heard on, their organization's domain), the people its words name by address among them;
    else the area its words point to (todo_areas.mentioned: a company or one of its mailboxes). Else, open, the area most
    of their recent to-dos are in (todo_areas.most_used, or their first connection's), until the review places it by
    meaning. Never the Machine's own source (the Gateway log, in no area) while an area exists. A mail account of the
    area first, the one its runs search and send from."""
    found = todo_areas.areas(accounts)
    if not found:
        return accounts[0]['id'], []
    pick = found[0]['id'] if len(found) == 1 else None
    free = lambda value: (lambda d: '' if d in graph.FREEMAIL else d)(own_addresses.email_domain(value))
    if pick is None:
        mails = todo_areas.addresses(text)
        try:
            people, rows = [], []
            select = "SELECT n.kind,n.info,o.info org_info FROM graph_nodes n LEFT JOIN graph_nodes o ON o.id=json_extract(n.info,'$.org') "
            if node_ids:
                rows += db.execute(select + f"WHERE n.id IN ({','.join('?' for _ in node_ids)}) AND n.kind IN ('person','org')", list(node_ids)).fetchall()
            if mails:
                rows += db.execute(select + f"WHERE n.kind='person' AND EXISTS (SELECT 1 FROM json_each(n.info,'$.emails') e WHERE lower(e.value) IN "
                                   f"({','.join('?' for _ in mails)}))", mails).fetchall()
            for r in rows:
                info, org = json.loads(r['info'] or '{}'), json.loads(r['org_info'] or '{}')
                people.append({'side': info.get('side'), 'accounts': info.get('accounts') or [],
                               'org_domain': info.get('domain') if r['kind'] == 'org' else org.get('domain')})
        except (sqlite3.Error, ValueError, TypeError):
            people = []
        pick = (todo_areas.pointed(people, accounts, None, free) if people else None) or todo_areas.mentioned(text, accounts, free)
    open_ = [f['id'] for f in found] if pick is None else []
    if open_:
        try:
            since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).isoformat()
            recent = db.execute('SELECT account_ids,area FROM suggestions WHERE created_at>=? ORDER BY created_at DESC LIMIT 500', (since,)).fetchall()
        except sqlite3.Error:
            recent = []
        pick = todo_areas.most_used([(r['account_ids'], r['area']) for r in recent], accounts) or next(
            x for x in (todo_areas.area_of_account(a) for a in accounts) if x in {f['id'] for f in found})
    ids = todo_areas.accounts_in(pick, accounts)
    services = {a['id']: a.get('service', 'gmail') for a in accounts}
    return next((i for i in ids if services[i] in MAIL_SERVICES), ids[0]), open_


def agent_messages(views):
    """The card's source messages as card/messages.md for a coding agent: who, to whom, when, and the full text, so
    it needs no mailbox of its own. The link goes last, as a reference."""
    out = []
    for v in views:
        head = [f"## {v.get('title') or v.get('kind') or 'Message'}", f"From: {v.get('from') or 'unknown'}"]
        head += [f'{k}: {v[k.lower()]}' for k in ('To', 'Cc') if v.get(k.lower())]
        head.append(f"When: {v.get('occurred_at') or ''}")
        body = str(v.get('body') or '').strip() or '(no text)'
        out.append('\n'.join(head) + '\n\n' + body + ('\n\n(Cut short here: the rest is in the original.)' if v.get('clipped') else '')
                   + (f"\n\nOriginal: {v['url']}" if v.get('url') else ''))
    return '\n\n'.join(out)


def agent_about(card, views):
    """Who and what a card is about, in plain lines: the people who wrote, the source, the due date."""
    people = list(dict.fromkeys(str(v.get('from') or '').strip() for v in views if v.get('from') and v.get('from') != 'You'))[:3]
    lines = [f"With: {', '.join(people)}" + (f" ({views[0]['kind']})" if views and views[0].get('kind') else '')] if people else []
    if card.get('source_line'):
        lines.append(str(card['source_line']).strip())
    if card.get('due'):
        lines.append(f"Due: {card['due']}")
    return lines


def agent_history(owner, results, skip='', keep=6):
    """The card's chat so far, as short background lines, newest last: what the owner asked and what came back. The
    owner's latest note is skipped (it goes in the brief word for word)."""
    turns = [(i['at'], 'I asked', i['text']) for i in owner if i.get('kind') == 'you' and i.get('via') != 'agent']
    turns += [(i['at'], f"{i.get('name') or 'The agent'} answered", i['text']) for i in owner if i.get('kind') == 'agent']
    turns += [(r['at'], 'The Machine answered', r['text']) for replies in results.values() for r in replies if r.get('kind') == 'reply']
    skip = ' '.join(str(skip or '').split())
    lines = [f'{who}: {agent_jobs.gist(text, 400)}' for at, who, text in sorted(turns, key=lambda t: t[0] or 0)
             if str(text or '').strip() and ' '.join(str(text).split()) != skip]
    return lines[-keep:]


# Every message the Machine has, whatever brought it in: what New to-do's Message chip searches (api/events?kind=message).
# Mail, Slack, Teams, WhatsApp, Telegram, LinkedIn, X, Intercom, and copies a teammate's handoff carried.
ATTACH_KINDS = tuple(sorted({*graph.MESSAGE_KINDS, 'outlook.message', 'fleet.email', 'fleet.message', 'x.mention'}))


class NewCardsApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def message_hits(self, account_ids, query, limit=8):
        """New to-do's Message chip: messages of every kind (ATTACH_KINDS) whose words match, and those with a person
        whose name matches, newest first. Keywords and names only, so it answers at once."""
        find = {'account_ids': account_ids, 'kinds': list(ATTACH_KINDS), 'full': True, 'limit': limit * 2}
        rows = self.action('events', {**find, 'query': query})
        with self.store.connect() as db:
            people = [r['id'] for r in graph.find(db, query, limit=3, kinds=('person',))]
            ids = [r[0] for r in db.execute(f"SELECT g.event_id FROM graph_events g JOIN events e ON e.id=g.event_id WHERE g.direct=1 AND e.deleted=0 "
                                            f"AND g.node_id IN ({','.join('?' * len(people))}) AND e.kind IN ({','.join('?' * len(ATTACH_KINDS))}) "
                                            'ORDER BY e.occurred_at DESC LIMIT ?', (*people, *ATTACH_KINDS, limit * 2))] if people else []
        if ids:
            rows += self.action('events', {**find, 'event_ids': ids})
        seen, out = set(), []
        for r in sorted(rows, key=lambda r: (r['occurred_at'], r['id']), reverse=True):
            if r['id'] not in seen:
                seen.add(r['id'])
                out.append(r)
        return out[:limit]

    def agent_card(self, suggestion_id):
        """What a Claude Code or Codex brief is made of: the card, its next step as the task, the owner's note, who it is
        about, its chat so far (background), drafts, links, result files and source messages (agent_jobs.brief_for)."""
        with self.store.connect() as db:
            row = db.execute('SELECT s.*,p.status preparation_status,p.reason preparation_reason,p.error preparation_error,'
                             'p.questions preparation_questions FROM suggestions s LEFT JOIN preparations p ON s.id=p.suggestion_id '
                             'WHERE s.id=?', (str(suggestion_id),)).fetchone()
            if not row:
                return None
            card = dict(row)
            source_lines_shown(db, [card])  # a Slack DM by the person's name, never a raw chat handle
            extra = self.store.suggestion_result(card, db)
            note = db.execute("SELECT feedback FROM decisions WHERE suggestion_id=? AND trim(feedback)<>'' AND source IN ('telegram','dashboard') "
                              'AND id NOT IN (SELECT decision_id FROM decision_annotations) ORDER BY created_at DESC,rowid DESC LIMIT 1',
                              (card['id'],)).fetchone()
            try:
                chat = self.card_chat_service(db, card['id'])
            except (sqlite3.Error, ValueError, TypeError, KeyError):
                chat = ([], {})
        actions = extra.get('next_actions') or []
        drafts = [a for a in actions if a.get('body') or a.get('message')]
        links = [*extra.get('original_urls', []), *[a['url'] for a in actions if a.get('kind') == 'open' and str(a.get('url') or '').startswith('https://')]]
        files = [WORKSPACE / f['path'] for f in extra.get('result_files', [])]
        try:
            views = self.store.originals(card['id'])[:5]
        except (ValueError, sqlite3.Error):
            views = []
        note = note['feedback'].strip() if note else ''
        return {'card': card, 'drafts': drafts, 'links': links, 'files': files, 'messages': agent_messages(views), 'sources': views,
                'task': card_task(card), 'note': note, 'about': agent_about(card, views), 'history': agent_history(*chat, skip=note),
                'message_kinds': [v['kind'] for v in views]}

    def new_card(self, args):
        """New card: what the owner typed, with optional Work or Personal, a due date (YYYY-MM-DD; the dashboard reads
        "Friday" or "in 2 weeks" into one) and, when the owner gave a time ("15:00", "in 2 hours"), due_at, people, organizations or a project from the Graph, and messages to attach (mail, Slack, WhatsApp, any kind: message_hits).
        It is a normal card (Store.owner_card); the next review fills it in."""
        accounts = self.config.get('accounts', [])
        if not accounts:
            raise ValueError('Connect a source first')
        scope = args.get('scope') or None
        if scope not in (None, 'work', 'personal'):
            raise ValueError('scope is work or personal')
        try:
            attach = list(dict.fromkeys(int(i) for i in args.get('attach') or []))
        except (TypeError, ValueError):
            raise ValueError('attach is a list of event ids') from None
        wanted = list(dict.fromkeys(str(i) for i in args.get('about') or []))
        if len(attach) > 5 or len(wanted) > 5:
            raise ValueError('Up to five people and five messages')
        known = {a['id'] for a in accounts}
        with self.store.connect() as db:
            found = {r['id']: r['account_id'] for r in db.execute(
                f"SELECT id,account_id FROM events WHERE deleted=0 AND id IN ({','.join('?' * len(attach)) or 'NULL'})", attach)}
            nodes = {r['id']: dict(r) for r in db.execute(
                f"SELECT id,kind,name FROM graph_nodes WHERE id IN ({','.join('?' * len(wanted)) or 'NULL'})", wanted)}
        if set(found) != set(attach) or not set(found.values()) <= known:
            raise ValueError('That message is no longer there')
        if set(nodes) != set(wanted):
            raise ValueError('That person is no longer in the Graph')
        about = [{'id': n['id'], 'name': n['name'][:120], 'kind': n['kind']} for n in (nodes[i] for i in wanted) if n['kind'] in ('person', 'org')]
        project = next((nodes[i]['name'] for i in wanted if nodes[i]['kind'] == 'project'), None)
        work_ids = [a['id'] for a in accounts if suggestion_scope([a['id']], accounts) == 'work']
        personal_ids = [a['id'] for a in accounts if a['id'] not in work_ids]
        if scope == 'work' and not work_ids:
            raise ValueError('No work account is connected')
        if scope == 'personal' and not personal_ids:
            raise ValueError('No personal account is connected')
        area_open = []
        if scope == 'work':
            account = work_ids[0]
        elif scope == 'personal':
            account = personal_ids[0]
        elif attach:
            account = found[attach[0]]
        else:  # no area given: where it belongs, from its people, organizations and words (owner_card_area)
            with self.store.connect() as db:
                account, area_open = owner_card_area(db, accounts, wanted, args.get('text') or '')
        work = any(a['id'] == account and str(a.get('boundary') or '').startswith('work:') for a in accounts)
        due, due_at = args.get('due') or None, args.get('due_at') or None
        try:  # a day (the owner's own calendar day), and a moment when they gave a time ("15:00", "in 2 hours")
            due = due and dt.date.fromisoformat(str(due)).isoformat()
            when = due_at and dt.datetime.fromisoformat(str(due_at))
        except ValueError:
            raise ValueError('due is YYYY-MM-DD and due_at a time with its offset') from None
        if when and when.tzinfo is None:
            raise ValueError('due_at needs its offset')
        due_at = when and when.astimezone(dt.timezone.utc).isoformat(timespec='minutes')
        if due_at and not due:
            raise ValueError('due_at goes with due, its day')
        files = args.get('files') or []
        if files and not isinstance(files, list):
            raise ValueError('files is a list of file ids')
        draft = 'new:' + str(args.get('draft') or '')
        texts = {}
        if files:  # what the PDFs and text files say, read here for the review (chat_files.texts); nothing leaves the Machine
            with self.store.connect() as db:
                texts = chat_files.texts(db, self.config, draft, files)
        saved = self.store.owner_card(args.get('text'), account, work=work, due=due, about=about, attach=attach, project=project,
                                      files=(draft, files) if files else None, due_at=due_at,
                                      area_open=area_open, file_texts=texts)
        if attach:  # a message a review read and left without a to-do: a miss the learning loop reads (missed_work.passed_over)
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                for event_id in attach:
                    missed_work.passed_over(db, event_id, saved['id'])
        if about and getattr(self, 'graph_dirty', None):
            self.graph_dirty.set()  # the card shows on their Graph page after the next build
        return saved

    def is_work(self, account_ids):
        if isinstance(account_ids, str):
            account_ids = json.loads(account_ids or '[]')
        return any(a['id'] in (account_ids or []) and a.get('boundary', '').startswith('work:') for a in self.config.get('accounts', []))

    def is_work_suggestion(self, suggestion_id):
        with self.store.connect() as db:
            row = db.execute('SELECT account_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        return bool(row) and self.is_work(row['account_ids'])

    def ai_card(self, who, text, area, due=None, draft=None):
        """A to-do a connected AI added (ai_app.py, docs/ai-connections.md), made like a Fleet request's (fleet_card): its
        first evidence is an event on one of the owner's accounts in that area, marked reviewed so no review or
        preparation reads it by itself, and it says which AI it is from. With a draft, an email draft from one of the
        owner's mail accounts in that area, which goes out only with the owner's own Send."""
        accounts = [a for a in self.config.get('accounts', []) if area is None or graph.account_side(a) == area]
        if draft:
            accounts = [a for a in accounts if mail_account(a)]
        elif not accounts:  # nothing placed in that area yet: a to-do sends nothing, so it goes on the Machine's own account
            accounts = self.config.get('accounts', [])[:1]
        if not accounts:
            raise ValueError('No Gmail or Outlook account here to write it from' if draft else 'No account here for this')
        account = accounts[0]['id']
        stamp, key = now(), 'ai:' + uuid.uuid4().hex[:16]
        name = ' '.join(str(who or 'AI').split())[:60]
        title = owner_title(text)
        body = (body_after_title(title, text) or text) if not draft else i18n.t('{} wrote this email for you. Read it, change it if you like, and send it yourself.', name) + (
            '\n\n' + text if text != draft['subject'] else '')
        meta = {'sender_display': i18n.t('{} (connected AI)', name), 'ai_connection': name}
        event_id = self.store.add_ai_request(account, key, stamp, title, text, meta)
        card = self.store.suggest(key, (i18n.t('Email to {}: {}', ', '.join(draft['to'])[:60], draft['subject']) if draft else title)[:90],
                                  body[:700], [event_id], when='now', work=(graph.account_side(accounts[0]) or area) == 'work', due=due)
        if not card.get('duplicate'):  # the owner asked for it, as with New card (owner_card): on their list now, not held for a work day
            with self.store.connect() as db:
                db.execute('UPDATE suggestions SET deliver_after=NULL WHERE id=?', (card['id'],))
        if draft and not card.get('duplicate'):
            action = next_actions.validate({'kind': 'email', 'label': 'Send', 'account_id': account, 'to': draft['to'],
                                            'subject': draft['subject'], 'body': draft['body']}, self.config, [account])
            with self.store.connect() as db:
                db.execute("UPDATE suggestions SET status='accepted' WHERE id=? AND status='pending'", (card['id'],))
            self.store.prepare(card['id'], body[:1000], next_action=action, outcome={'state': 'needs_you', 'needs': 'read and send the email'})
        return card['id']

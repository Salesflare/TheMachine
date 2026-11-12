"""The owner's email in the service: a Gmail message and its source email read live, attachments, mailbox lookups and
own addresses, and handoffs by email with their task pages. Moved out of assistant.App as is. A mixin of
assistant.App (APP_MIXINS)."""
import base64
import collections
import datetime as dt
import functools
import json
from pathlib import Path
import re
import sqlite3
import threading
import time

import abilities
import handoff_mail
from i18n import t
from machine.app.promise_checks import activity_since
from machine.cards import handoff_checkin
from machine.sources.calendar import company_domains
from machine.sources.gmail import Gmail, message_event
from machine.store.promises import promise_check_at
from machine.text import message_attachments, message_html, message_images, shown_body
import mail_attachments
import ms_graph
import next_actions
import own_addresses
from sources import credential, gog_read, MAIL_SERVICES, SourceError
import task_pages
import todo_areas

COMPOSE_ADDRESS = re.compile(r'[^\s<>@,;"]+@[^\s<>@,;"]+\.[^\s<>@,;"]+')


class MailApp:
    # New email's two actions are their own reviewed set (machine.actions.COMPOSE_ACTIONS)
    ACTIONS = {'mail_attachment': 'mail_attachment_action', **dict.fromkeys(task_pages.ACTIONS, 'task_page_action'),
               'compose_from': 'compose_from_action', 'compose_email': 'compose_email_action'}

    @functools.cached_property
    def task_pages(self):
        """Pages for tasks handed off by email (task_pages.py)."""
        return task_pages.TaskPages(self)

    @functools.cached_property
    def handoff_mail(self):
        """Handoffs by email to a colleague who isn't on The Machine (handoff_mail.py)."""
        return handoff_mail.HandoffMail(self, handoff_checkin, promise_check_at)

    def handoff_mail_draft(self, card_id, body, next_action, outcome):
        """The handoff email, ready on the to-do for the owner to read and send (a pending to-do counts as accepted)."""
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='accepted' WHERE id=? AND status='pending'", (card_id,))
        self.store.prepare(card_id, body, next_action=next_action, outcome=outcome)

    def handoff_mail_wait(self, db, card_id, until):
        """A handoff email went out: the to-do waits under Later until its check-in, then comes back as it was."""
        db.execute("UPDATE suggestions SET status='snoozed',snoozed_until=?,resume_status='prepared',outcome=NULL,undo_until=NULL WHERE id=?",
                   (until, card_id))

    def handoff_mail_promise(self, db, card_id, event_ids, who, what, due, check_at, event):
        """Their promise to take on a to-do handed off by email, from the sent email (watch NULL: only the review closes it
        by meaning, or the to-do). The to-do then holds that email, so it is the promise's home. Returns its id."""
        stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
        cursor = db.execute("INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,watch,status,created_at,updated_at) "
                            "VALUES('theirs',?,?,?,?,?,?,NULL,'open',?,?) ON CONFLICT(event_id,direction,who,what) DO NOTHING",
                            (who, what, due, check_at, event['id'], event['account_id'], stamp, stamp))
        if event['id'] not in event_ids:
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([*event_ids, event['id']]), card_id))
        return cursor.lastrowid or None

    def email_handoff_round(self):
        """In the Fleet's round: answers from task pages, then handoffs by email (take links, promises, moves)."""
        try:
            self.task_pages.round()
        finally:
            self.handoff_mail.round()

    def gmail_message(self, account_id, message_id):
        """One source email, read live (read-only). Opening it on the dashboard reads it for its attachments, its
        HTML and each embedded image, and visible cards read it ahead, so a few recent ones stay in memory for
        MESSAGE_TTL; one read at a time per message."""
        account = next(a for a in self.config['accounts'] if a['id'] == account_id)
        cache = self.__dict__.setdefault('_messages', collections.OrderedDict())
        locks = self.__dict__.setdefault('_message_locks', collections.defaultdict(threading.Lock))
        key = (account_id, message_id)
        with locks[key]:
            hit = cache.get(key)
            if hit and time.monotonic() - hit[0] < self.MESSAGE_TTL:
                cache.move_to_end(key)
                return account, hit[1]
            message = gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.get',
                               {'userId': 'me', 'id': message_id, 'format': 'full'}, 'https://www.googleapis.com/auth/gmail.readonly')
            cache[key] = (time.monotonic(), message)
            cache.move_to_end(key)
            while len(cache) > self.MESSAGE_CACHE:
                cache.popitem(last=False)
        if len(locks) > 4 * self.MESSAGE_CACHE:
            locks.clear()  # at worst one message is read twice
        return account, message

    def mailbox_lookup(self, account_ids, query, limit=5):
        """Search the owner's own mailboxes themselves (Gmail's search, Outlook's), read-only, for mail older than what
        is collected: a mail they sent weeks ago that a to-do follows up on. What it finds is kept as collected signals
        (Store.keep_found: reviewed, so it is context, not news, unless it came after the last sync) for the run to read and link. Only the mail accounts
        among account_ids, never one shared from a Fleet. Returns (event ids, {account id: error category})."""
        query = ' '.join(str(query or '').split())[:200]
        if not query:
            raise ValueError('mailbox_search needs a query: Gmail search words, such as from:sam subject:pricing in:sent')
        limit = max(1, min(int(limit or 5), self.MAILBOX_LOOKUP_MAX))
        found, failed = [], {}
        for account in self.config.get('accounts', []):
            if account['id'] not in account_ids or account.get('service', 'gmail') not in MAIL_SERVICES or account.get('shared'):
                continue
            source = Gmail(self.config, account)
            try:
                source.profile()  # fail closed on account routing, as a sync does
                refs = source.get('messages', {'q': query, 'maxResults': limit}).get('messages') or []
                events = [e for e in (message_event(account, source.get('messages/' + r['id'], {'format': 'full'}), self.config)
                                      for r in refs[:limit]) if e]
            except SourceError as error:
                failed[account['id']] = error.category
                continue
            found += self.store.keep_found(account['id'], events)
        return found, failed

    def newer_unchecked(self, event_ids, checked=None):
        """Before a new to-do: what happened after its evidence (activity_since) that the review hasn't said it read
        (newer_checked). [] when nothing came after, so most to-dos save at once and the check costs no extra step."""
        ids = [int(i) for i in event_ids or [] if isinstance(i, int) or str(i).isdigit()]
        with self.store.connect() as db:
            found = activity_since(db, ids, self.store.owner_user_ids, {x['email']: x['name'] for x in self.teammate_addresses()},
                                   company_domains(self.config))
        read = {int(i) for i in (checked if isinstance(checked, list) else []) if isinstance(i, int) or str(i).isdigit()}
        return [x for x in found if x['id'] not in read]

    def teammate_addresses(self):
        """The members of the owner's Work Fleets, each address with their name: who Hand off by email suggests first."""
        out = []
        try:
            for found in (self.fleet.fleets().values() if getattr(self, 'fleet', None) else ()):
                if found.get('kind') != 'work':
                    continue
                for member in found.get('members', []):
                    if member.get('me'):
                        continue
                    for email in dict.fromkeys(str(e).lower() for e in [member.get('account_email'), *(member.get('emails') or [])] if e and '@' in str(e)):
                        out.append({'name': ' '.join(str(member.get('name') or '').split())[:80], 'email': email})
        except Exception:  # noqa: BLE001 - suggestions only: the Graph and the domains still help
            return out
        return out

    def owner_emails(self):
        """The owner's addresses: each account's (its owner_emails, else its own) and the ones found as theirs
        (own_addresses.py: aliases, their calendar, their profiles; never a shared one or one they removed)."""
        found = {str(e).lower() for a in self.config.get('accounts', []) for e in a.get('owner_emails', [a.get('email')]) if e}
        try:
            with self.store.connect() as db:
                return found | own_addresses.yours(db, self.config)
        except sqlite3.Error:
            return found

    def originals(self, suggestion_id, event_id='', event_ids=None):
        """Source messages for the dashboard, with Gmail attachments looked up live (read-only):
        a card's, one collected event opened from the Events or People tab, or a conversation's messages in order."""
        items = self.store.originals(suggestion_id) if suggestion_id else self.store.event_views(event_ids or [event_id])
        cache = self.__dict__.setdefault('_attachments', {})
        for item in items:
            body, cut = shown_body(item['body'])  # read by people: never the model's quoted-history marker
            item.update(body=body, clipped=item['clipped'] or cut)
            source = item.pop('gmail')
            item['attachments'] = []
            if not source:
                continue
            key = (source['account_id'], source['message_id'])
            if key not in cache or cache[key][0] < time.monotonic() - 600:
                try:
                    cache[key] = (time.monotonic(), message_attachments(self.gmail_message(*key)[1].get('payload')))
                except Exception:
                    continue  # Attachments are a convenience; the email itself still shows.
            item['attachments'] = cache[key][1]
        return items

    def email_view(self, suggestion_id, event_id):
        """The HTML of one source email, read live (read-only), with its embedded images."""
        source = self.gmail_source(suggestion_id, event_id)
        if not source:
            raise ValueError('Email not available')
        payload = self.gmail_message(source['account_id'], source['message_id'])[1].get('payload')
        return {'html': message_html(payload), 'images': message_images(payload)}

    def gmail_source(self, suggestion_id, event_id):
        items = self.store.originals(suggestion_id) if suggestion_id else self.store.event_views([event_id])
        return next((item['gmail'] for item in items if str(item['event_id']) == str(event_id) and item['gmail']), None)

    def draft_attachment(self, suggestion_id, sha256):
        """A file attached to this card's own email draft, served from the service's store by checksum."""
        with self.store.connect() as db:
            row = db.execute('SELECT next_action FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        record = next((r for action in next_actions.actions(row['next_action'] if row else None)
                       for r in action.get('attachments', []) if r['sha256'] == sha256), None)
        if not record:
            raise ValueError('Attachment not available')
        return next_actions.attachment_bytes(record, self.config), record['type'], record['name']

    def attachment(self, suggestion_id, event_id, part):
        source = self.gmail_source(suggestion_id, event_id)
        if not source:
            raise ValueError('Attachment not available')
        account, message = self.gmail_message(source['account_id'], source['message_id'])
        payload = message.get('payload') or {}
        # Only this message's real attachments and its embedded images are served.
        if part not in [a['part'] for a in message_attachments(payload)] + list(message_images(payload).values()):
            raise ValueError('Attachment not available')
        found = []
        def walk(node):
            if str(node.get('partId', '')) == part:
                found.append(node)
            for child in node.get('parts', []):
                walk(child)
        walk(payload)
        if not found:
            raise ValueError('Attachment not available')
        node = found[0];body = node.get('body') or {}
        data = body.get('data') or gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.attachments.get',
                                            {'userId': 'me', 'messageId': source['message_id'], 'id': body['attachmentId']},
                                            'https://www.googleapis.com/auth/gmail.readonly').get('data', '')
        return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4)), node.get('mimeType', 'application/octet-stream'), node.get('filename') or 'image'

    def mail_attachment(self, args):
        """An email's attachments for a preparation, read-only (Gmail and Outlook): a list, or one saved in the job's
        attachments folder, at most 18 MB. With message protection on it is kept there sealed with the message key and
        the run reads a copy in a private folder that goes after the run (mail_attachments.py); `open` gives such a copy
        of an attachment saved earlier."""
        folder = Path(args.get('_folder') or mail_attachments.root(self.config))
        if args.get('open'):
            return mail_attachments.open_copy(self.config | {'attachment_root': str(folder)}, args['open'], args.get('job_id'))
        account = next((a for a in self.config['accounts'] if a['id'] == args.get('account_id')), None)
        message_id = str(args.get('message_id') or '')
        if args.get('event_id') is not None:
            with self.store.connect() as db:
                row = db.execute("SELECT account_id,source_id FROM events WHERE id=? AND kind IN ('gmail.message','ms_graph.message','outlook.message')",
                                 (int(args['event_id']),)).fetchone()
            if not row:
                raise ValueError('No collected email with that event_id')
            account = next((a for a in self.config['accounts'] if a['id'] == row['account_id']), None)
            message_id = row['source_id']
        if not account or not next_actions.mail_account(account):
            raise ValueError('Give the account_id of a Gmail or Outlook mailbox')
        if not message_id:
            raise ValueError('Give the message_id or event_id of the email')
        fetch = MailApp.outlook_attachments if next_actions.outlook(account) else MailApp.gmail_attachments
        found, data = fetch(self, account, message_id, args.get('save'))
        if not args.get('save'):
            return {'attachments': found}
        if len(data) > next_actions.MAX_ATTACHMENT_BYTES:
            raise ValueError('That attachment is larger than 18 MB')
        job = str(args.get('job_id') or '')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        name = re.sub(r'[^\w. -]+', '_', found['name']).strip(' .') or 'attachment'
        saved = mail_attachments.save(self.config, folder / job, name, data)
        return saved | {'name': name, 'mime': found['mime'], 'size': len(data)}

    def gmail_attachments(self, account, message_id, save=None):
        """A Gmail message's real attachments, read live with gmail.readonly: the list, or (`save`: its part id or
        name) that one and its bytes."""
        try:
            message = self.gmail_message(account['id'], message_id)[1]
        except Exception as error:
            raise ValueError(f'Gmail could not give the message ({type(error).__name__})') from None
        payload = message.get('payload') or {}
        found = [{'id': a['part'], 'name': a['name'], 'mime': a['mime'], 'size': a['size'], 'inline': False, 'kind': 'file'}
                 for a in message_attachments(payload)]
        if not save:
            return found, None
        chosen = next((a for a in found if save in (a['id'], a['name'])), None)
        if not chosen:
            raise ValueError('No attachment with that id or name')
        if chosen['size'] > next_actions.MAX_ATTACHMENT_BYTES:
            raise ValueError('That attachment is larger than 18 MB')
        nodes = []
        def walk(node):
            if str(node.get('partId', '')) == chosen['id']:
                nodes.append(node)
            for child in node.get('parts', []):
                walk(child)
        walk(payload)
        body = nodes[0].get('body') or {}
        data = body.get('data') or gog_read(self.config, account, 'gmail', 'v1', 'gmail.users.messages.attachments.get',
                                            {'userId': 'me', 'messageId': message_id, 'id': body['attachmentId']},
                                            'https://www.googleapis.com/auth/gmail.readonly').get('data', '')
        return chosen, base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))

    def outlook_attachments(self, account, message_id, save=None):
        """An Outlook message's attachments through Microsoft Graph, read-only: the list, or that one and its bytes."""
        try:
            found = ms_graph.attachments(self.config, credential, account, message_id)
            if not save:
                return [{k: a[k] for k in ('id', 'name', 'mime', 'size', 'inline', 'kind')}
                        | ({'note': 'a link to a cloud file: open it in the browser'} if a['kind'] == 'link' else
                           {'note': 'an attached email or event: not saved; read the message itself'} if a['kind'] == 'item' else {})
                        for a in found], None
            chosen = next((a for a in found if save in (a['id'], a['name'])), None)
            if not chosen:
                raise ValueError('No attachment with that id or name')
            if chosen['kind'] != 'file':
                raise ValueError('Only file attachments can be saved; ' + ('open this cloud link in the browser' if chosen['kind'] == 'link' else 'this is an attached email or event'))
            if chosen['size'] > next_actions.MAX_ATTACHMENT_BYTES:
                raise ValueError('That attachment is larger than 18 MB')
            return chosen, ms_graph.attachment(self.config, credential, account, message_id, chosen['id'])
        except ms_graph.GraphError as error:
            raise ValueError(f'Outlook could not give the attachment ({error})') from None

    def share_files(self, event_id, part=None):
        """A Work email's attachments for the Shared Graph, read-only (Gmail and Outlook): the list, or (part) one file's
        bytes. Only files: cloud links and attached emails stay where they are."""
        with self.store.connect() as db:
            row = db.execute('SELECT account_id,source_id,kind FROM events WHERE id=?', (int(event_id),)).fetchone()
        account = row and next((a for a in self.config['accounts'] if a['id'] == row['account_id']), None)
        if not account or not next_actions.mail_account(account) or row['kind'] not in ('gmail.message', 'ms_graph.message') or not row['source_id']:
            return [] if part is None else None
        fetch = MailApp.outlook_attachments if next_actions.outlook(account) else MailApp.gmail_attachments
        if part is None:
            return [a for a in fetch(self, account, row['source_id'])[0] if a.get('kind', 'file') == 'file' and not a.get('inline')]
        return fetch(self, account, row['source_id'], part)[1]

    def mail_attachment_action(self, name, args, owner_dashboard=False):
        return self.mail_attachment({k: v for k, v in args.items() if k != '_folder'})

    # -- New email: a click on an email address in the dashboard (docs/help/email-composer.md). The composer is the send
    # dialog every draft uses; Send makes the email an ordinary draft on a to-do of its own (Store.owner_card, accepted,
    # so no review or run reads it) and sends it with Store.confirm_action, the one way a draft goes out.
    def compose_mailboxes(self):
        """The owner's mailboxes a new email can go from: each one that sends what the owner approves, with Can do
        things on, never one a Fleet shares (an Other email account too, once it can send)."""
        return [a for a in self.config.get('accounts', []) if next_actions.mail_account(a) and a.get('email')
                and not a.get('shared') and not abilities.refuse(self.config, a['id'])]

    @staticmethod
    def compose_address(value):
        address = str(value or '').strip()
        if len(address) > 254 or not COMPOSE_ADDRESS.fullmatch(address):
            raise ValueError(t('Give their email address'))
        return address

    @staticmethod
    def compose_person(db, address):
        """The person in the Graph with this address: (node id, name), else (None, '')."""
        row = db.execute("SELECT id,name FROM graph_nodes n WHERE kind='person' AND EXISTS (SELECT 1 FROM json_each(n.info,'$.emails') e "
                         'WHERE lower(e.value)=?) ORDER BY id LIMIT 1', (address.lower(),)).fetchone()
        return (row['id'], row['name'] or '') if row else (None, '')

    def compose_from_action(self, name, args, owner_dashboard=False):
        """What the composer offers for an address: the From choices (each mailbox and the aliases Gmail confirms it
        sends as, own_addresses.senders), grouped by area, the one for the person's area first picked (owner_card_area:
        Work for a work contact, Personal for a personal one), and their name from the Graph. No mailbox: no choices,
        and the dashboard opens the mail app instead."""
        if not owner_dashboard:
            raise ValueError(t('Only the owner writes an email, from the dashboard'))
        address = self.compose_address(args.get('to'))
        able = self.compose_mailboxes()
        accounts = self.config.get('accounts', [])
        with self.store.connect() as db:
            node, person = self.compose_person(db, address)
            if not able:
                return {'from': [], 'to_name': person, 'node_id': node}
            senders = own_addresses.senders(db, self.config)
            from machine.app.new_cards import owner_card_area  # noqa: PLC0415 - a sibling mixin
            area, _ = owner_card_area(db, accounts, [node] if node else [], address)
        home = next((a for a in accounts if a['id'] == area), None)
        side = home and todo_areas.area_of_account(home)
        pick = next((a for a in able if a['id'] == area), None) or next((a for a in able if side and todo_areas.area_of_account(a) == side), able[0])
        found = todo_areas.areas(accounts)
        firms = sum(x['id'] != todo_areas.PERSONAL for x in found)
        label = lambda area: '' if not area else t('Personal') if area == todo_areas.PERSONAL else (
            t('Work at {}', todo_areas.name(area, accounts)) if firms > 1 and todo_areas.name(area, accounts) else t('Work'))
        choices, seen = [], set()
        for a in sorted(able, key=lambda a: a['id'] != pick['id']):
            for sender in [a['email'], *(x for x in senders.get(a['id']) or () if a.get('service', 'gmail') == 'gmail')]:
                if sender and sender.lower() not in seen:
                    seen.add(sender.lower())
                    choices.append({'account_id': a['id'], 'from': sender, 'area': label(todo_areas.area_of_account(a))})
        return {'from': choices, 'default': pick['email'], 'to_name': person, 'node_id': node}

    def compose_email_action(self, name, args, owner_dashboard=False):
        """Send in the composer: the email as a draft on a new to-do about the person (on their Graph page), checked like
        any draft (next_actions.validate). Nothing is sent here: the dashboard then confirms exactly this revision
        (confirm_action), with the alias picked as its sender."""
        if not owner_dashboard:
            raise ValueError(t('Only the owner writes an email, from the dashboard'))
        address = self.compose_address(args.get('to'))
        account = next((a for a in self.compose_mailboxes() if a['id'] == args.get('account_id')), None)
        if not account:
            raise ValueError(t('Pick a mailbox to send it from.'))
        subject, body = ' '.join(str(args.get('subject') or '').split()), str(args.get('body') or '').strip()
        if not subject:
            raise ValueError(t('Add a subject first.'))
        if not body:
            raise ValueError(t('Write the message first.'))
        with self.store.connect() as db:
            node, person = self.compose_person(db, address)
            senders = own_addresses.senders(db, self.config)
        draft = next_actions.validate({'kind': 'email', 'label': 'Send', 'account_id': account['id'], 'to': [address],
                                       'subject': subject, 'body': body}, self.config, [account['id']], senders=senders)
        title = t('Email to {}: {}', person or address, subject)
        work = str(account.get('boundary') or '').startswith('work:')
        about = [{'id': node, 'name': person[:120], 'kind': 'person'}] if node else []
        card = self.store.owner_card(title, account['id'], work=work, about=about, accepted=True)
        self.store.prepare(card['id'], t('An email you wrote.'), next_action=draft, outcome={'state': 'needs_you', 'needs': 'send the email'})
        if about and getattr(self, 'graph_dirty', None):
            self.graph_dirty.set()  # the to-do shows on their page after the next build
        return {'suggestion_id': card['id'], 'revision': draft['revision'], 'from_options': draft.get('from_options') or []}

    def task_page_action(self, name, args, owner_dashboard=False):
        # a task page for an email handoff: add, skip, stop sharing, mark done (task_pages.py)
        if not owner_dashboard:
            raise ValueError('Task pages are shared from the dashboard')
        return self.task_pages.action(name, args)

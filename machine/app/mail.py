"""The owner's email in the service: a Gmail message and its source email read live, attachments, mailbox lookups and
own addresses, and handoffs by email with their task pages. Moved out of assistant.App as is. A mixin of
assistant.App (APP_MIXINS)."""
import base64
import collections
import datetime as dt
import functools
import json
import sqlite3
import threading
import time

import handoff_mail
from machine.app.promise_checks import activity_since
from machine.cards import handoff_checkin
from machine.sources.calendar import company_domains
from machine.sources.gmail import Gmail, message_event
from machine.store.promises import promise_check_at
from machine.text import message_attachments, message_html, message_images, shown_body
import next_actions
import own_addresses
from sources import gog_read, MAIL_SERVICES, SourceError
import task_pages


class MailApp:
    ACTIONS = {}  # its actions are still App.action's own branches

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
        (Store.keep_found: reviewed, so it is context, not news) for the run to read and link. Only the mail accounts
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

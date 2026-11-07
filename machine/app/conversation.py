"""The conversation around a to-do's source message on the dashboard (machine/store/conversation.py reads what is
stored). An email thread whose earlier messages came in before the mailbox's first import is read live from Gmail on
Show earlier, read-only (gmail.readonly, the scope the Machine already reads mail with), with the same exclusions a
sync applies, and never stored. A mixin of assistant.App (APP_MIXINS)."""
import json
import sqlite3
import time

import graph
import own_addresses
from machine.config import LOG
from machine.sources.exclusions import excluded_by_rules, routine_rules
from machine.sources.gmail import Gmail, message_event
from machine.store.conversation import BEFORE_MAX
from machine.text import _address, shown_body

LIVE_TTL = 600  # a thread read live is kept this long (seconds), so paging back and forth reads Gmail once


def readable(items):
    """Bodies as people read them (shown_body), like App.originals."""
    for item in items:
        item.pop('gmail', None)
        body, cut = shown_body(item['body'])
        item.update(body=body, clipped=item['clipped'] or cut, attachments=[])
    return items


class ConversationApp:
    ACTIONS = {}

    def message_context(self, suggestion_id, before=None):
        """The to-do's source message with what was said around it (Store.message_context), or None. An email thread
        with nothing older stored offers Show earlier (earlier) while its oldest message answers another one; Show
        earlier then reads the rest of that thread live."""
        found = self.store.message_context(suggestion_id, before)
        if not found:
            return None
        readable(found['before'])
        readable(found['after'])
        account = self.mail_account_of(found)
        if not account or found['earlier']:
            return found
        if before is None:
            found['earlier'] = self.thread_has_more(found)
            return found
        found['before'] = self.live_thread(account, found, before) + found['before']
        return found

    def message_context_quiet(self, suggestion_id):
        """message_context for the to-do's originals: None when it can't be read, so the source message still shows."""
        try:
            return self.message_context(suggestion_id)
        except (ValueError, sqlite3.Error) as error:
            LOG.info('message context suggestion=%s error=%s', suggestion_id, type(error).__name__)
            return None

    def mail_account_of(self, found):
        """The Gmail account of an email to-do's thread, when its thread can be read live; else None."""
        with self.store.connect() as db:
            anchor = db.execute('SELECT account_id,kind FROM events WHERE id=?', (found['event_id'],)).fetchone()
        if not anchor or anchor['kind'] != 'gmail.message':
            return None
        account = next((a for a in self.config.get('accounts', []) if a.get('id') == anchor['account_id']), None)
        return account if account and account.get('service', 'gmail') == 'gmail' else None

    def thread_has_more(self, found):
        """Whether the oldest stored message of the thread answers an earlier one (In-Reply-To): one the Machine may
        not have, because it came in before the mailbox's first import."""
        oldest = (found['before'] or [None])[0]
        event_id = oldest['event_id'] if oldest else found['event_id']
        with self.store.connect() as db:
            row = db.execute('SELECT metadata FROM events WHERE id=?', (event_id,)).fetchone()
        m = row['metadata'] if row else {}
        m = m if isinstance(m, dict) else json.loads(m or '{}')
        return bool(str(m.get('in-reply-to') or '').strip())

    def live_thread(self, account, found, before):
        """The thread's messages older than `before` that the Machine never stored, read live (newest BEFORE_MAX), as
        event_views shows a message. Nothing on any error: Show earlier then simply has nothing more."""
        with self.store.connect() as db:
            row = db.execute('SELECT occurred_at,metadata FROM events WHERE id=?', (int(before),)).fetchone()
            anchor = db.execute('SELECT metadata FROM events WHERE id=?', (found['event_id'],)).fetchone()
            if not row or not anchor:
                return []
            thread = (anchor['metadata'] if isinstance(anchor['metadata'], dict) else json.loads(anchor['metadata'])).get('thread_id')
            if not thread:
                return []
            stored = {r[0] for r in db.execute("SELECT source_id FROM events WHERE account_id=? AND kind='gmail.message' "
                                               "AND json_extract(metadata,'$.thread_id')=?", (account['id'], str(thread)))}
            gone = graph.forgotten(db) if graph.anyone_forgotten(db) else None
            own = own_addresses.yours(db, self.config)
        own |= {str(a.get('email') or '').lower() for a in self.config.get('accounts', []) if '@' in str(a.get('email') or '')}
        cache = self.__dict__.setdefault('_live_threads', {})
        key = (account['id'], str(thread))
        if key not in cache or cache[key][0] < time.monotonic() - LIVE_TTL:
            try:
                raw = Gmail(self.config, account).get('threads/' + str(thread), {'format': 'full'})
            except Exception as error:  # noqa: BLE001 - earlier mail is a convenience; the to-do's own message still shows
                LOG.info('live thread account=%s error=%s', account['id'], type(error).__name__)
                return []
            cache[key] = (time.monotonic(), raw.get('messages') or [])
        dropping, _ = routine_rules(self.store.exclusions.get(account['id']) or [])
        owner = graph.Owner({}) if gone else None
        out = []
        for message in cache[key][1]:
            if message.get('id') in stored:
                continue
            try:
                event = message_event(account, message, self.config)
            except Exception:  # noqa: BLE001 - one message it can't read is left out, as a sync would
                continue
            if not event or event['occurred_at'] >= row['occurred_at'] or excluded_by_rules(dropping, event) \
                    or gone and graph.from_forgotten(event['kind'], event['metadata'], owner, gone):
                continue
            m = event['metadata']
            sender = str(m.get('from') or '')
            mine = _address(sender) in own
            body, cut = shown_body(event['body'])
            out.append({'kind': 'email', 'from': ('You' if mine else sender)[:300], 'to': str(m.get('to') or '')[:500],
                        'cc': str(m.get('cc') or '')[:500], 'title': event['title'][:500], 'occurred_at': event['occurred_at'],
                        'body': body[:20000], 'clipped': cut or len(body) > 20000, 'url': m.get('source_url'),
                        'event_id': None, 'live': True, 'attachments': []})
        return sorted(out, key=lambda o: o['occurred_at'])[-BEFORE_MAX:]


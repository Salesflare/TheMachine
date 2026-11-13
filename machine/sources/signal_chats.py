"""Signal as a source: the owner's own Signal chats, read from the store the Signal mirror keeps (signal_store.py), a
message as an event (signal_event), the chats that are the owner's (owner_signal_chats), and its sync (sync_signal).
Named signal_chats so it never stands in for Python's own signal module. Like WhatsApp in what it reads and sends; like
Telegram chats in how (a mirror that alone runs the client, and an outbox for sends the owner approved)."""
import contextlib
import datetime as dt
import hashlib
from pathlib import Path
import re
import sqlite3

from machine.sources.rows import Skips
from machine.text import encoded
from sources import SourceError
from timeutil import now


class Signal:
    """The owner's own Signal chats, read-only from the mirror's store. Nothing here talks to Signal."""

    def __init__(self, config, account):
        self.config, self.account = config, account

    def open(self):
        import signal_store
        store = self.account.get('store')
        if not store or not (Path(store).expanduser() / signal_store.DB_NAME).exists():
            raise SourceError('signal_source_unavailable')
        try:
            db = signal_store.connect(Path(store).expanduser(), readonly=True)
            seal = signal_store.sealer(Path(store).expanduser(), self.config.get('database'), create=False)
        except (sqlite3.Error, OSError, ValueError):
            raise SourceError('signal_source_unavailable') from None
        if seal is None:
            db.close()
            raise SourceError('signal_source_unavailable')
        return signal_store, db, seal

    def profile(self):
        """The mirror's state, when it is linked to this account and nothing stopped it. A stop says why: unlinked on the
        phone (signal_unlinked: link again), or a signal-cli Signal no longer accepts (signal_outdated)."""
        ss, db, _ = self.open()
        with contextlib.closing(db):
            state = ss.get_state(db)
        error = state.get('error')
        if error == 'outdated':
            raise SourceError('signal_outdated')
        if error in ('unlinked', 'logged_out', 'store_unreadable'):
            raise SourceError('signal_unlinked')
        if state.get('identity') != self.account.get('identity_sha256'):
            raise SourceError('account_identity_mismatch')
        return state

    def chats(self, query=None, limit=10):
        """The chats the mirror knows ({id, kind, name}), optionally those whose name holds `query`."""
        ss, db, seal = self.open()
        with contextlib.closing(db):
            rows = db.execute('SELECT id, kind, name FROM signal_chats ORDER BY updated_at DESC').fetchall()
        found = [{'id': r['id'], 'kind': r['kind'], 'name': seal.open(r['name']) or ''} for r in rows]
        found = [c for c in found if c['name']]  # a chat without a name is never guessed at
        if query:
            words = query.casefold().split()
            found = [c for c in found if all(w in c['name'].casefold() for w in words)]
        return found[:limit]

    def messages(self, after):
        ss, db, seal = self.open()
        with contextlib.closing(db):
            rows = db.execute('SELECT m.*, c.name chat_name, c.kind chat_kind FROM signal_messages m LEFT JOIN signal_chats c ON c.id=m.chat_id '
                              # older rows too once deleted (for everyone, or a disappearing message's timer): their text goes here as well
                              'WHERE m.occurred_at>=? OR m.deleted=1 ORDER BY m.occurred_at LIMIT 20000', (after,)).fetchall()
        return [{**dict(r), 'text': seal.open(r['text']) if r['text'] is not None else None,
                 'sender_name': seal.open(r['sender_name']), 'chat_name': seal.open(r['chat_name']) if r['chat_name'] is not None else None}
                for r in rows]


SIGNAL_CHAT = re.compile(r'(?:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|g:[A-Za-z0-9+/=_-]{8,100})')
SECURITY_CODE = re.compile(r'(?i)verification code|security code|login code|one.time (?:code|password)|\bOTP\b|verificatiecode')


def signal_event(account, raw):
    """One message from the Signal store as an event (kind signal.message), like a WhatsApp one."""
    chat, author, sent = str(raw.get('chat_id') or ''), str(raw.get('author') or ''), raw.get('sent_at')
    if not SIGNAL_CHAT.fullmatch(chat) or not author or not isinstance(sent, int) or not isinstance(raw.get('occurred_at'), str):
        raise SourceError('signal_invalid_message')
    try:
        stamp = dt.datetime.fromisoformat(raw['occurred_at'])
    except ValueError:
        raise SourceError('signal_invalid_timestamp') from None
    if stamp.tzinfo is None:
        raise SourceError('signal_missing_timezone')
    from_me = bool(raw.get('from_me'))
    body = raw.get('text') or ''
    if not body.strip() and raw.get('media_type'):  # a photo or file without a caption: say what it is
        media = str(raw['media_type'])
        body = 'Sent ' + ('' if media in ('view-once media', 'audio') else 'a ') + media
    sensitive = bool(SECURITY_CODE.search(body))
    if sensitive:
        body = '[One-time security code omitted]'
    group = chat.startswith('g:')
    chat_name = raw.get('chat_name') or ('Signal group' if group else (raw.get('sender_name') if not from_me else '') or 'Signal chat')
    sender = 'You' if from_me else (raw.get('sender_name') or ('Unknown sender' if group else chat_name))
    deleted = bool(raw.get('deleted')) or not body.strip()
    metadata = {'chat_name': chat_name, 'chat_id': chat, 'chat_kind': 'group' if group else 'dm', 'message_id': f'{author}:{sent}',
                'sent_at': sent, 'from_me': from_me, 'sender_id': None if from_me else author,
                'sender_identity': 'authenticated_account_owner' if from_me else 'source_label_unverified',
                'from': sender, 'sender_display': sender,
                'sender_display_source': 'authenticated_account_owner' if from_me else 'source_label_unverified',
                'edited': bool(raw.get('edited')), 'revoked': bool(raw.get('deleted')), 'no_content': not body.strip(),
                'disappearing': bool(raw.get('expires_at')),
                'media_type': raw.get('media_type') or '', 'media_collected': False,
                'security_code_omitted': sensitive, 'truncated': len(body) > 40000,
                'transport': 'signal_mirror_store',
                'coverage': 'Messages since this Machine was linked. Signal gives a new linked device no older messages.'}
    identity = hashlib.sha256(encoded([chat, author, sent]).encode()).hexdigest()
    return {'account_id': account['id'], 'source_id': identity, 'kind': 'signal.message',
            'occurred_at': stamp.astimezone(dt.timezone.utc).isoformat(),
            'title': chat_name[:1000], 'body': body[:40000], 'metadata': metadata, 'deleted': deleted}


def sync_signal(store, config, account, source=None):
    source = source or Signal(config, account)
    state_ = source.profile()
    stamp = dt.datetime.fromisoformat(now())
    after = (stamp - dt.timedelta(days=config.get('bootstrap_days', 7))).isoformat()
    rows = source.messages(after)
    skipped = Skips('signal_invalid_message')  # a row it can't take is counted, never failing the poll
    events = list({e['source_id']: e for e, _ in skipped.every(rows, signal_event, account)}.values())
    checkpoint = store.checkpoint(account['id']) or {}
    skipped.check().note(checkpoint)
    checkpoint.update(mode='incremental', after=after, before=stamp.isoformat(), retained_days=config.get('bootstrap_days', 7),
                      available_messages=len(rows), source_latest_message=max((e['occurred_at'] for e in events), default=None),
                      mirror_last_ok=state_.get('last_ok'), linked_at=state_.get('linked_at'),
                      account_name=state_.get('name'),  # the linked account's own name, for its card (machine/names.py)
                      coverage='Seven-day reread of the Signal mirror store, from the moment of linking. Nothing here talks to Signal.')
    store.commit_page(account['id'], checkpoint, events)
    return {'mode': 'incremental', 'events': len(events), 'skipped': sum(skipped.values())}


def owner_signal_chats(config, db, raw, task_chats, source=None):
    """As owner_whatsapp_chats, for Signal: the person's existing chat in the owner's own Signal, for a card that
    switches to Signal. A chat_id must be one the mirror knows; a to_name must match one chat (a person first). Never a
    new chat. Returns {chat_id: {account_id, name, switched}} and fills in the chat_id it found."""
    found = {}
    for item in raw if isinstance(raw, list) else [raw]:
        if not isinstance(item, dict) or item.get('kind') != 'signal' or str(item.get('chat_id') or '') in task_chats:
            continue
        account = next((a for a in config['accounts'] if a['id'] == item.get('account_id') and a.get('service') == 'signal' and not a.get('shared')), None)
        if not account:
            continue
        excluded = {c for r in account.get('exclude') or [] if set(r) == {'chats'} for c in r['chats']}
        reader = source(config, account) if source else Signal(config, account)
        try:
            chats = reader.chats(limit=100000) if item.get('chat_id') else reader.chats(str(item.get('to_name') or '').strip() or None)
        except SourceError:
            raise ValueError('Signal can’t be read right now, so I can’t find the chat. Put the message in the body and say '
                             'in one line that they can send it on Signal themselves.') from None
        chats = [c for c in chats if c['id'] not in excluded]
        if item.get('chat_id'):
            chat = next((c for c in chats if c['id'] == str(item['chat_id'])), None)
            if not chat:
                continue
        elif isinstance(item.get('to_name'), str) and 2 <= len(item['to_name'].strip()) <= 100:
            people = [c for c in chats if c['kind'] == 'dm'] or chats
            if len(people) != 1:
                raise ValueError(('More than one Signal chat matches: ' + '; '.join(f"{c['name']} (chat_id {c['id']})" for c in people[:5])
                                  + '. Give the right chat_id.') if people else
                                 'No Signal chat with ' + item['to_name'].strip() + ' in this account. Never start a new one: put the message '
                                 'in the body and say in one line that they can send it on Signal themselves.')
            chat = people[0]
            item['chat_id'] = chat['id']
        else:
            continue
        found[chat['id']] = {'account_id': account['id'], 'name': chat['name'], 'switched': True}
    return found

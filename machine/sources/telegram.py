"""Telegram as a source: the client of the owner's own Telegram session (Telegram), a message as an event
(telegram_event), the chats that are the owner's, and its sync (sync_telegram). Moved out of assistant.py as is."""
import contextlib
import datetime as dt
import hashlib
from pathlib import Path
import re
import sqlite3

import enrichment
from machine.sources.rows import Skips
from machine.text import encoded
import message_seal
from sources import SourceError
from timeutil import now
from machine.owner_error import OwnerError


class Telegram:
    """The owner's own Telegram chats, read from the store the Telegram mirror keeps (telegram_store.py), read-only.
    The mirror alone holds the Telegram session; nothing here talks to Telegram."""

    def __init__(self, config, account):
        self.config, self.account = config, account

    def open(self):
        import telegram_store
        store = self.account.get('store')
        if not store or not (Path(store).expanduser() / telegram_store.DB_NAME).exists():
            raise SourceError('telegram_source_unavailable')
        try:
            db = telegram_store.connect(Path(store).expanduser(), readonly=True)
            seal = telegram_store.sealer(Path(store).expanduser(), self.config.get('database'), create=False)
        except (sqlite3.Error, OSError, ValueError):
            raise SourceError('telegram_source_unavailable') from None
        if seal is None:
            db.close()
            raise SourceError('telegram_source_unavailable')
        return telegram_store, db, seal

    def profile(self):
        """The mirror's state, when it is logged in to this account and nothing stopped it. A stop says why: logged out
        (log in again), Telegram refused this Machine's app ID (telegram_app_blocked: said plainly on Connections, never a
        silent gap), or a flood wait it is sitting out."""
        ts, db, _ = self.open()
        with contextlib.closing(db):
            state = ts.get_state(db)
        error = state.get('error')
        if error == 'app_blocked':
            raise SourceError('telegram_app_blocked')
        if error in ('signed_out', 'logged_out', 'session_unreadable'):
            raise SourceError('telegram_logged_out')
        if state.get('identity') != self.account.get('identity_sha256'):
            raise SourceError('account_identity_mismatch')
        return state

    def chats(self, query=None, limit=10):
        """The chats the mirror reads ({id, kind, name}), optionally those whose name holds `query`."""
        ts, db, seal = self.open()
        with contextlib.closing(db):
            rows = db.execute("SELECT id, kind, name FROM chats WHERE skipped='' ORDER BY updated_at DESC").fetchall()
        found = [{'id': r['id'], 'kind': r['kind'], 'name': seal.open(r['name']) or 'Telegram chat'} for r in rows]
        if query:
            words = query.casefold().split()
            found = [c for c in found if all(w in c['name'].casefold() for w in words)]
        return found[:limit]

    def messages(self, after):
        ts, db, seal = self.open()
        with contextlib.closing(db):
            rows = db.execute("SELECT m.*, c.name chat_name, c.kind chat_kind FROM messages m JOIN chats c ON c.id=m.chat_id "
                              "WHERE m.occurred_at>=? AND c.skipped='' ORDER BY m.occurred_at LIMIT 20000", (after,)).fetchall()
        return [{**dict(r), 'text': seal.open(r['text']) if r['text'] is not None else None,
                 'sender_name': seal.open(r['sender_name']), 'chat_name': seal.open(r['chat_name'])} for r in rows]

    def picture(self, user_id):
        """A person's small profile photo, asked through the mirror, which holds the session (telegram_store.ask_photo):
        {'id', 'data': (bytes, type)}, {} when they have none the owner can see, {'id'} when it didn't download, or
        {'pending': True} while the mirror hasn't answered. SourceError when the mirror can't answer."""
        if not re.fullmatch(r'[0-9]{1,20}', str(user_id)):
            raise SourceError('telegram_invalid_person')
        self.profile()
        import telegram_store
        store = Path(self.account['store']).expanduser()
        try:
            seal = telegram_store.sealer(store, self.config.get('database'), create=False)
            if seal is None:
                raise SourceError('telegram_source_unavailable')
            with contextlib.closing(telegram_store.connect(store)) as db:
                answer = telegram_store.ask_photo(db, seal, str(user_id))
        except (sqlite3.Error, OSError, ValueError, message_seal.SealError):
            raise SourceError('telegram_source_unavailable') from None
        data = answer.pop('data', None)
        kind = enrichment.image_type(data) if data else None
        if kind and len(data) <= enrichment.PHOTO_BYTES:
            answer['data'] = (data, kind)
        return answer


def telegram_photo_asker(config):
    """ask(account id, user id) for enrichment.telegram_photos_step: the owner's own Telegram accounts only (never one
    shared from a Fleet); None when the mirror can't answer."""
    accounts = {a['id']: a for a in config.get('accounts', []) if a.get('service') == 'telegram' and a.get('store') and not a.get('shared')}
    def ask(account_id, user_id):
        try:
            return Telegram(config, accounts[account_id]).picture(user_id)
        except (SourceError, KeyError):
            return None
    return list(accounts), ask


TELEGRAM_CHAT = re.compile(r'-?[0-9]{1,20}')


def telegram_event(account, raw):
    """One message from the Telegram store as an event (kind telegram.message), like a WhatsApp one."""
    chat, mid = str(raw.get('chat_id') or ''), raw.get('msg_id')
    if not TELEGRAM_CHAT.fullmatch(chat) or not isinstance(mid, int) or not isinstance(raw.get('occurred_at'), str):
        raise SourceError('telegram_invalid_message')
    try:
        stamp = dt.datetime.fromisoformat(raw['occurred_at'])
    except ValueError:
        raise SourceError('telegram_invalid_timestamp') from None
    if stamp.tzinfo is None:
        raise SourceError('telegram_missing_timezone')
    from_me = bool(raw.get('from_me'))
    body = raw.get('text') or ''
    if not body.strip() and raw.get('media_type'):
        body = 'Sent a ' + str(raw['media_type'])
    sensitive = bool(re.search(r'(?i)verification code|security code|login code|one.time (?:code|password)|\bOTP\b|verificatiecode', body))
    if sensitive:
        body = '[One-time security code omitted]'
    group = raw.get('chat_kind') == 'group'
    chat_name = raw.get('chat_name') or ('Telegram group' if group else 'Telegram chat')
    sender = 'You' if from_me else (raw.get('sender_name') or ('Unknown sender' if group else chat_name))
    deleted = bool(raw.get('deleted')) or not body.strip()
    metadata = {'chat_name': chat_name, 'chat_id': chat, 'chat_kind': 'group' if group else 'dm', 'message_id': mid,
                'from_me': from_me, 'sender_id': None if from_me else (str(raw.get('sender_id') or '') or None),
                'sender_identity': 'authenticated_account_owner' if from_me else 'source_label_unverified',
                'from': sender, 'sender_display': sender,
                'sender_display_source': 'authenticated_account_owner' if from_me else 'source_label_unverified',
                'edited': bool(raw.get('edited')), 'revoked': bool(raw.get('deleted')), 'no_content': not body.strip(),
                'media_type': raw.get('media_type') or '', 'media_collected': False, 'reply_to': raw.get('reply_to'),
                'security_code_omitted': sensitive, 'truncated': len(body) > 40000,
                'transport': 'telegram_mirror_store',
                'coverage': 'Private chats and small groups the mirror reads; channels, bots, muted and archived chats are skipped.'}
    identity = hashlib.sha256(encoded([chat, mid, from_me]).encode()).hexdigest()
    return {'account_id': account['id'], 'source_id': identity, 'kind': 'telegram.message',
            'occurred_at': stamp.astimezone(dt.timezone.utc).isoformat(),
            'title': chat_name[:1000], 'body': body[:40000], 'metadata': metadata, 'deleted': deleted}


def sync_telegram(store, config, account, source=None):
    source = source or Telegram(config, account)
    state_ = source.profile()
    stamp = dt.datetime.fromisoformat(now())
    after = (stamp - dt.timedelta(days=config.get('bootstrap_days', 7))).isoformat()
    rows = source.messages(after)
    skipped = Skips('telegram_invalid_message')  # a row it can't take is counted, never failing the poll
    events = list({e['source_id']: e for e, _ in skipped.every(rows, telegram_event, account)}.values())
    checkpoint = store.checkpoint(account['id']) or {}
    skipped.check().note(checkpoint)
    checkpoint.update(mode='incremental', after=after, before=stamp.isoformat(), retained_days=config.get('bootstrap_days', 7),
                      available_messages=len(rows), source_latest_message=max((e['occurred_at'] for e in events), default=None),
                      mirror_last_ok=state_.get('last_ok'), flood_until=state_.get('flood_until'),
                      coverage='Seven-day reread of the Telegram mirror store. Nothing here talks to Telegram.')
    store.commit_page(account['id'], checkpoint, events)
    return {'mode': 'incremental', 'events': len(events), 'skipped': sum(skipped.values())}


def owner_telegram_chats(config, db, raw, task_chats, source=None):
    """As owner_whatsapp_chats, for Telegram: the person's existing chat in the owner's own Telegram account, for a
    card that switches to Telegram. A chat_id must be one the mirror reads; a to_name must match one chat (a private
    chat first). Never a new chat. Returns {chat_id: {account_id, name, switched}} and fills in the chat_id it found."""
    found = {}
    for item in raw if isinstance(raw, list) else [raw]:
        if not isinstance(item, dict) or item.get('kind') != 'telegram' or str(item.get('chat_id') or '') in task_chats:
            continue
        account = next((a for a in config['accounts'] if a['id'] == item.get('account_id') and a.get('service') == 'telegram' and not a.get('shared')), None)
        if not account:
            continue
        excluded = {c for r in account.get('exclude') or [] if set(r) == {'chats'} for c in r['chats']}
        reader = source(config, account) if source else Telegram(config, account)
        try:
            chats = reader.chats(limit=100000) if item.get('chat_id') else reader.chats(str(item.get('to_name') or '').strip() or None)
        except SourceError:
            raise OwnerError('Telegram can’t be read right now, so I can’t find the chat. Put the message in the body and say '
                             'in one line that they can send it on Telegram themselves.') from None
        chats = [c for c in chats if c['id'] not in excluded]
        if item.get('chat_id'):
            chat = next((c for c in chats if c['id'] == str(item['chat_id'])), None)
            if not chat:
                continue
        elif isinstance(item.get('to_name'), str) and 2 <= len(item['to_name'].strip()) <= 100:
            people = [c for c in chats if c['kind'] == 'dm'] or chats
            if len(people) != 1:
                raise ValueError(('More than one Telegram chat matches: ' + '; '.join(f"{c['name']} (chat_id {c['id']})" for c in people[:5])
                                  + '. Give the right chat_id.') if people else
                                 'No Telegram chat with ' + item['to_name'].strip() + ' in this account. Never start a new one: put the message '
                                 'in the body and say in one line that they can send it on Telegram themselves.')
            chat = people[0]
            item['chat_id'] = chat['id']
        else:
            continue
        found[chat['id']] = {'account_id': account['id'], 'name': chat['name'], 'switched': True}
    return found

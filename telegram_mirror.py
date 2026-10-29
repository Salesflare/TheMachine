#!/usr/bin/env python3
"""The Telegram chats mirror: the one process that holds the owner's Telegram session (Telethon, from the pinned
libraries telegram_release.py unpacks), as a logged-in device of their own account, like Telegram Desktop.

    telegram_mirror.py --store DIR --app FILE --lib DIR login [--phone +32...]   log in (QR code, or a code by phone)
    telegram_mirror.py --store DIR --app FILE --lib DIR follow                  keep the store in step (a user service)
    telegram_mirror.py --store DIR --app FILE --lib DIR logout                  log this device out at Telegram
    telegram_mirror.py --lib DIR version                                         the Telethon version, to check the libraries

`login` speaks JSON lines: it prints {"event": "qr", "url", "matrix", "expires"} (again each time Telegram renews the
code), {"event": "code_sent"}, {"event": "password", "hint"} and {"event": "connected", "identity", "name"}, and reads
{"code": "..."} or {"password": "..."} lines on stdin. The cloud password only passes through memory: it is never
written, logged or printed.

How it treats the account (Telegram's terms, and the owner's account kept safe):
- One fixed device profile ("The Machine"), so Telegram sees one device that stays; it never logs in by itself again.
  Signed out, it stops and says so (state `error`), and the owner logs in again from Connections.
- Reads private chats and small groups only (telegram_store.readable): never channels, bots, Telegram's service
  notifications or Saved Messages, and muted or archived chats only when the owner opts them in.
- At the first start, the last 7 days of those chats, paged slowly; then only what arrives. No full history pulls.
- Never marks anything read, never sends typing, and tells Telegram it is offline: the owner's own apps show their
  read and online status as they are.
- Telegram's flood waits are kept: short ones inside Telethon, longer ones stop the run until they are over.
- Sends only what the outbox holds, which the app writes for a message the owner approved with Send; one at a time,
  at least SEND_GAP seconds apart. A send that may have gone out is never sent again (status `sending` stays).
- `logout` (and a logout row from Disconnect) ends this device at Telegram and deletes the session."""
import argparse
import asyncio
import datetime as dt
import json
import platform
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import portable  # noqa: E402
import telegram_store as ts  # noqa: E402

DEVICE = 'The Machine'
APP_VERSION = '1.0'
SEND_GAP = 20          # seconds between two sends, at least
CHAT_PAUSE = (1.0, 2.5)  # seconds between two chats while reading the last week
BACKFILL_CHATS = 100   # chats read back at the first start, the most recent first
REFRESH_CHATS = 6 * 3600  # how often the chat list (muted, archived, names) is read again
FLOOD_LIMIT = 900      # a longer flood wait stops the run; the service starts again after it
QR_WAIT = 600          # seconds a login waits for the code to be scanned
TEMPORARY = 75         # exit code: try again later (the service restarts it)
SIGNED_OUT = ('AuthKeyUnregisteredError', 'SessionRevokedError', 'SessionExpiredError', 'UserDeactivatedError',
              'UserDeactivatedBanError', 'AuthKeyDuplicatedError', 'AuthKeyInvalidError')
APP_BLOCKED = ('ApiIdInvalidError', 'ApiIdPublishedFloodError')


def emit(event, **data):
    print(json.dumps({'event': event, **data}), flush=True)


def error_name(error):
    return type(error).__name__


def stop_reason(error):
    """'signed_out' or 'app_blocked' for an error that ends this session or this app ID, else None."""
    name = error_name(error)
    return 'signed_out' if name in SIGNED_OUT else 'app_blocked' if name in APP_BLOCKED else None


def flood_seconds(error):
    return int(getattr(error, 'seconds', 0) or 0) if error_name(error) in ('FloodWaitError', 'FloodPremiumWaitError', 'SlowModeWaitError') else 0


def qr_matrix(url):
    """The QR code for a login link as rows of 0 and 1, which the dashboard draws."""
    import qrcode
    code = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    code.add_data(url)
    code.make(fit=True)
    return [''.join('1' if cell else '0' for cell in row) for row in code.get_matrix()]


def classify(entity, dialog=None):
    """{'id', 'kind', 'name', 'members', 'muted', 'archived'} of a Telegram user, group or channel."""
    kind = type(entity).__name__
    if kind == 'User':
        chat = 'self' if getattr(entity, 'is_self', False) else 'bot' if getattr(entity, 'bot', False) else 'dm'
        name = ' '.join(p for p in (getattr(entity, 'first_name', None), getattr(entity, 'last_name', None)) if p) or (getattr(entity, 'username', None) or 'Telegram chat')
        members = 2
    elif kind in ('Chat', 'ChatForbidden'):
        chat, name, members = 'group', getattr(entity, 'title', '') or 'Telegram group', getattr(entity, 'participants_count', None)
    elif kind in ('Channel', 'ChannelForbidden'):
        chat = 'group' if getattr(entity, 'megagroup', False) else 'channel'
        name, members = getattr(entity, 'title', '') or 'Telegram group', getattr(entity, 'participants_count', None)
    else:
        chat, name, members = 'other', 'Telegram chat', None
    muted = archived = False
    if dialog is not None:
        settings = getattr(getattr(dialog, 'dialog', None), 'notify_settings', None)
        until = getattr(settings, 'mute_until', None)
        if isinstance(until, dt.datetime):
            muted = until > dt.datetime.now(dt.timezone.utc)
        elif isinstance(until, int):
            muted = until > time.time()
        archived = bool(getattr(dialog, 'archived', False) or getattr(dialog, 'folder_id', None) == 1)
    return {'id': str(peer_id(entity, dialog)), 'kind': 'channel' if chat == 'other' else chat, 'name': name[:200],
            'members': members if isinstance(members, int) else None, 'muted': muted, 'archived': archived}


def peer_id(entity, dialog=None):
    if dialog is not None and getattr(dialog, 'id', None) is not None:
        return dialog.id
    kind, raw = type(entity).__name__, getattr(entity, 'id', 0)
    if kind in ('Chat', 'ChatForbidden'):
        return -raw
    if kind in ('Channel', 'ChannelForbidden'):
        return -(10 ** 12) - raw
    return raw


def save_chat(db, seal, chat, include=()):
    skipped = ts.readable(chat, include)
    db.execute('INSERT INTO chats(id, kind, name, members, muted, archived, skipped, updated_at) VALUES (?,?,?,?,?,?,?,?) '
               'ON CONFLICT(id) DO UPDATE SET kind=excluded.kind, name=excluded.name, members=excluded.members, muted=excluded.muted, '
               'archived=excluded.archived, skipped=excluded.skipped, updated_at=excluded.updated_at',
               (chat['id'], chat['kind'], seal.seal(chat['name']), chat['members'], int(chat['muted']), int(chat['archived']), skipped, ts.now()))
    return skipped


def media_kind(message):
    for attribute, name in (('photo', 'photo'), ('video', 'video'), ('voice', 'voice note'), ('audio', 'audio'), ('sticker', 'sticker'),
                            ('gif', 'GIF'), ('document', 'file'), ('geo', 'location'), ('contact', 'contact'), ('poll', 'poll')):
        if getattr(message, attribute, None):
            return name
    return 'other' if getattr(message, 'media', None) else ''


def sender_name(message, chat_name):
    sender = getattr(message, 'sender', None)
    if sender is None:
        return chat_name
    if type(sender).__name__ == 'User':
        return ' '.join(p for p in (getattr(sender, 'first_name', None), getattr(sender, 'last_name', None)) if p) or getattr(sender, 'username', None) or chat_name
    return getattr(sender, 'title', None) or chat_name


def save_message(db, seal, chat_id, message, chat_name):
    """One message into the store (again after an edit). Service messages (joined, changed the title) are not kept."""
    if getattr(message, 'action', None) is not None:
        return False
    date = message.date if message.date.tzinfo else message.date.replace(tzinfo=dt.timezone.utc)
    out = bool(getattr(message, 'out', False))
    name = 'You' if out else sender_name(message, chat_name)
    db.execute('INSERT INTO messages(chat_id, msg_id, from_me, sender_id, sender_name, text, media_type, occurred_at, edited, deleted, reply_to) '
               'VALUES (?,?,?,?,?,?,?,?,?,0,?) ON CONFLICT(chat_id, msg_id) DO UPDATE SET text=excluded.text, media_type=excluded.media_type, '
               'edited=excluded.edited, sender_name=excluded.sender_name',
               (str(chat_id), int(message.id), int(out), None if out else str(getattr(message, 'sender_id', '') or ''),
                seal.seal(name[:200]), seal.seal((getattr(message, 'message', None) or '')[:40000]), media_kind(message),
                date.astimezone(dt.timezone.utc).isoformat(), int(getattr(message, 'edit_date', None) is not None),
                getattr(message, 'reply_to_msg_id', None)))
    return True


class Mirror:
    """The follow loop's state, apart from Telethon so it is tested with a stand-in client."""

    def __init__(self, client, store, seal, include=(), sleep=asyncio.sleep, clock=time.monotonic):
        self.client, self.store, self.seal, self.include = client, Path(store), seal, {str(i) for i in include}
        self.db = ts.connect(store)
        self.sleep, self.clock = sleep, clock
        self.names = {}
        self.last_send = -SEND_GAP
        self.me = None

    def chat_row(self, chat_id):
        return self.db.execute('SELECT * FROM chats WHERE id=?', (str(chat_id),)).fetchone()

    async def refresh_chats(self):
        """The chat list once: which chats are read, and their names. One page of dialogs per 100 chats."""
        seen = []
        async for dialog in self.client.iter_dialogs(limit=None, ignore_migrated=True):
            chat = classify(dialog.entity, dialog)
            skipped = save_chat(self.db, self.seal, chat, self.include)
            self.names[chat['id']] = chat['name']
            seen.append((chat['id'], skipped, getattr(dialog, 'date', None)))
        self.db.commit()
        ts.set_state(self.db, chats_at=ts.now())
        return seen

    async def backfill(self, seen, days=ts.BACKFILL_DAYS):
        """The last `days` days of the chats it reads, once, newest chats first, slowly."""
        since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
        recent = [(cid, date) for cid, skipped, date in seen if not skipped and isinstance(date, dt.datetime)
                  and (date if date.tzinfo else date.replace(tzinfo=dt.timezone.utc)) >= since]
        for cid, _ in recent[:BACKFILL_CHATS]:
            async for message in self.client.iter_messages(int(cid), limit=300):
                date = message.date if message.date.tzinfo else message.date.replace(tzinfo=dt.timezone.utc)
                if date < since:
                    break
                save_message(self.db, self.seal, cid, message, self.names.get(cid, 'Telegram chat'))
            self.db.commit()
            await self.sleep(random.uniform(*CHAT_PAUSE))
        ts.set_state(self.db, backfilled_at=ts.now(), backfill_days=days)

    async def on_message(self, chat_id, message, chat=None):
        """A new or edited message, kept when its chat is one it reads."""
        row = self.chat_row(chat_id)
        if row is None:
            entity = chat or await message.get_chat()
            info = classify(entity)
            info['id'] = str(chat_id)
            save_chat(self.db, self.seal, info, self.include)
            self.names[info['id']] = info['name']
            row = self.chat_row(chat_id)
        if row['skipped']:
            return False
        kept = save_message(self.db, self.seal, chat_id, message, self.names.get(str(chat_id)) or self.seal.open(row['name']) or 'Telegram chat')
        self.db.commit()
        return kept

    def on_deleted(self, chat_id, ids):
        """Deleted messages stay as deleted rows (their text gone). Without a chat (a private chat or a small group,
        where message IDs are the account's own), every chat that is not a channel."""
        for mid in ids:
            if chat_id is None:
                self.db.execute("UPDATE messages SET deleted=1, text=NULL WHERE msg_id=? AND chat_id NOT LIKE '-100%'", (int(mid),))
            else:
                self.db.execute('UPDATE messages SET deleted=1, text=NULL WHERE chat_id=? AND msg_id=?', (str(chat_id), int(mid)))
        self.db.commit()

    async def outbox(self):
        """The next queued row: a send the owner approved, or a logout. Returns 'logout' after logging out."""
        row = self.db.execute("SELECT * FROM outbox WHERE status='queued' ORDER BY created_at, rowid LIMIT 1").fetchone()
        if not row:
            return None
        done = lambda status, **values: (self.db.execute(
            'UPDATE outbox SET status=?, msg_id=?, error=?, done_at=? WHERE id=?',
            (status, values.get('msg_id'), values.get('error'), ts.now(), row['id'])), self.db.commit())
        if row['op'] == 'logout':
            try:
                await self.client.log_out()
            finally:
                ts.forget_session(self.store)
                done('done')
                ts.set_state(self.db, error='logged_out')
            return 'logout'
        if row['op'] != 'send' or not row['approval'] or not row['chat_id']:
            done('failed', error='not_approved')
            return 'failed'
        chat = self.chat_row(row['chat_id'])
        if chat is None or chat['skipped']:
            done('failed', error='chat_not_read')
            return 'failed'
        wait = SEND_GAP - (self.clock() - self.last_send)
        if wait > 0:
            await self.sleep(wait)
        await self.sleep(random.uniform(1.0, 3.0))
        self.db.execute("UPDATE outbox SET status='sending' WHERE id=? AND status='queued'", (row['id'],))
        self.db.commit()
        text = self.seal.open(row['text'])
        self.last_send = self.clock()
        try:
            sent = await self.client.send_message(int(row['chat_id']), text, link_preview=False)
        except Exception as error:  # noqa: BLE001 - every refusal is said on the to-do, and nothing is retried
            if stop_reason(error):
                raise
            seconds = flood_seconds(error)
            done('failed', error='flood_wait:%d' % seconds if seconds else error_name(error)[:80])
            return 'failed'
        save_message(self.db, self.seal, row['chat_id'], sent, self.names.get(row['chat_id'], 'Telegram chat'))
        done('sent', msg_id=int(sent.id))
        return 'sent'


def lock(store):
    handle = open(Path(ts.private_dir(store)) / ts.LOCK_NAME, 'a')
    try:
        portable.lock(handle, blocking=False)
    except BlockingIOError:
        handle.close()
        return None
    return handle


def app_of(path):
    app = ts.read_app(path)
    if not app:
        emit('error', code='no_app', message='No Telegram app ID: add your own, or the one this Machine gets from its hosting.')
        raise SystemExit(2)
    return app


def client_for(args, session_text, receive=False):
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    api_id, api_hash = app_of(args.app)
    return TelegramClient(StringSession(session_text or ''), api_id, api_hash, device_model=DEVICE,
                          system_version=f'{platform.system()} {platform.machine()}'.strip(), app_version=APP_VERSION,
                          lang_code='en', system_lang_code='en', flood_sleep_threshold=60, request_retries=3,
                          connection_retries=5, retry_delay=5, auto_reconnect=True, catch_up=receive, receive_updates=receive)


RESEND = '\x00resend'  # the owner asked for the login code again
# Where Telegram sent a login code (auth.SentCode's type), as the dashboard says it
SENT_VIA = {'SentCodeTypeApp': 'app', 'SentCodeTypeSms': 'sms', 'SentCodeTypeSmsWord': 'sms', 'SentCodeTypeSmsPhrase': 'sms',
            'SentCodeTypeFirebaseSms': 'sms', 'SentCodeTypeCall': 'call', 'SentCodeTypeFlashCall': 'call',
            'SentCodeTypeMissedCall': 'call', 'SentCodeTypeFragmentSms': 'fragment', 'SentCodeTypeEmailCode': 'email',
            'SentCodeTypeSetUpEmailRequired': 'email_setup'}


def read_answer(field, stream=None):
    """One JSON line from the dashboard (through onboarding): {"code": ...}, {"password": ...} or {"resend": true}."""
    line = (stream or sys.stdin).readline()
    if not line:
        raise SystemExit(TEMPORARY)
    try:
        data = json.loads(line)
        value = RESEND if data.get('resend') is True else data.get(field)
    except (ValueError, AttributeError):
        value = None
    return str(value or '')


def sent_event(sent):
    """What the owner is told about a login code: where it went, and how it can come next. Never the code."""
    kind = type(getattr(sent, 'type', None)).__name__
    via = SENT_VIA.get(kind, 'other')
    data = {'via': via, 'kind': kind[:60]}
    pattern = getattr(sent.type, 'email_pattern', None) or getattr(sent.type, 'prefix', None)
    if isinstance(pattern, str) and via in ('email', 'call'):
        data['to'] = pattern[:80]  # Telegram's own masked form, such as j***@example.com
    if getattr(sent, 'next_type', None) is not None:
        data['next'] = SENT_VIA.get(type(sent.next_type).__name__, 'other')
    if isinstance(getattr(sent, 'timeout', None), int):
        data['wait'] = sent.timeout
    return data


async def login(client, store, seal, phone=None, ask=read_answer, wait=QR_WAIT):
    """Logs this device in: a QR code to scan in Telegram (Settings, Devices, Link Desktop Device), or a code Telegram
    sends to the owner's own Telegram app for their phone number. Then the cloud password, if the account has one."""
    from telethon import errors
    from telethon.tl.functions.account import GetPasswordRequest
    db = ts.connect(store)
    await client.connect()

    async def password():
        try:
            hint = (await client(GetPasswordRequest())).hint or ''
        except Exception:  # noqa: BLE001 - the hint is only a help
            hint = ''
        for _ in range(3):
            emit('password', hint=hint[:100])
            try:
                await client.sign_in(password=ask('password'))
                return
            except errors.PasswordHashInvalidError:
                emit('password_wrong')
        raise RuntimeError('password_wrong')

    if phone:
        from telethon.tl.functions.auth import ResendCodeRequest
        sent = await client.send_code_request(phone)
        info = sent_event(sent)
        if info['via'] == 'email_setup':  # Telegram sends no code until the account has a login email: the QR code works
            raise RuntimeError('email_setup_required')
        emit('code_sent', **info)
        wrong = resent = 0
        while True:
            code = ask('code')
            if code == RESEND:
                resent += 1
                if resent > 3:
                    emit('code_resend_failed', reason='too_many')
                    continue
                try:
                    sent = await client(ResendCodeRequest(phone, sent.phone_code_hash))
                    emit('code_sent', again=True, **sent_event(sent))
                except Exception as error:  # noqa: BLE001 - no other way left, or a wait: said, and the old code still works
                    wait = flood_seconds(error)
                    emit('code_resend_failed', reason=error_name(error)[:60], **({'wait': wait} if wait else {}))
                continue
            try:
                await client.sign_in(phone=phone, code=code, phone_code_hash=sent.phone_code_hash)
                break
            except errors.SessionPasswordNeededError:
                await password()
                break
            except errors.PhoneCodeExpiredError:
                emit('code_expired')
            except (errors.PhoneCodeInvalidError, errors.PhoneCodeEmptyError):
                wrong += 1
                if wrong >= 3:
                    raise RuntimeError('code_wrong') from None
                emit('code_wrong')
    else:
        qr = await client.qr_login()
        until = time.monotonic() + wait
        while True:
            emit('qr', url=qr.url, matrix=qr_matrix(qr.url), expires=qr.expires.isoformat())
            left = min(until - time.monotonic(), max(5.0, (qr.expires - dt.datetime.now(dt.timezone.utc)).total_seconds()))
            if left <= 0:
                raise RuntimeError('qr_expired')
            try:
                await qr.wait(timeout=left)
                break
            except asyncio.TimeoutError:
                if time.monotonic() >= until:
                    raise RuntimeError('qr_expired') from None
                await qr.recreate()
            except errors.SessionPasswordNeededError:
                await password()
                break
    me = await client.get_me()
    ts.save_session(store, seal, client.session.save())
    ts.set_state(db, identity=ts.identity(me.id), linked_at=ts.now(), error=None, backfilled_at=None)
    name = ' '.join(p for p in (getattr(me, 'first_name', None), getattr(me, 'last_name', None)) if p)
    emit('connected', identity=ts.identity(me.id), name=name[:100])
    await client.disconnect()


async def follow(client, mirror, refresh=REFRESH_CHATS):
    """Keeps the store in step until Telegram ends the session or a long flood wait stops it."""
    from telethon import events
    from telethon.tl.functions.account import UpdateStatusRequest
    db = mirror.db
    await client.connect()
    if not await client.is_user_authorized():
        raise_signed_out()
    me = await client.get_me()
    if ts.get_state(db).get('identity') not in (None, ts.identity(me.id)):
        ts.set_state(db, error='signed_out')
        return 0
    await client(UpdateStatusRequest(offline=True))  # the owner's own apps say whether they are online
    async def arrived(event):
        await mirror.on_message(event.chat_id, event.message)

    async def deleted(event):
        mirror.on_deleted(event.chat_id, event.deleted_ids)
    client.add_event_handler(arrived, events.NewMessage())
    client.add_event_handler(arrived, events.MessageEdited())
    client.add_event_handler(deleted, events.MessageDeleted())
    seen = await mirror.refresh_chats()
    if not ts.get_state(db).get('backfilled_at'):
        await mirror.backfill(seen)
    ts.set_state(db, error=None, flood_until=None, last_ok=ts.now())
    refreshed, beat = time.monotonic(), time.monotonic()
    while client.is_connected():
        if await mirror.outbox() == 'logout':
            return 0
        if time.monotonic() - refreshed > refresh:
            await mirror.refresh_chats()
            refreshed = time.monotonic()
        if time.monotonic() - beat > 60:
            ts.save_session(mirror.store, mirror.seal, client.session.save())  # a moved data center changes it
            ts.set_state(db, last_ok=ts.now())
            beat = time.monotonic()
        await asyncio.sleep(2)
    return TEMPORARY


def raise_signed_out():
    raise type('AuthKeyUnregisteredError', (Exception,), {})()


async def logout(client):
    await client.connect()
    if await client.is_user_authorized():
        await client.log_out()


def run(args):
    if args.command == 'version':
        import telethon
        print(json.dumps({'telethon': telethon.__version__}))
        return 0
    store = Path(args.store).expanduser()
    held = lock(store)
    if held is None:
        emit('error', code='busy', message='Another Telegram mirror holds this store.')
        return TEMPORARY if args.command == 'follow' else 3
    seal = ts.sealer(store, args.database)
    db = ts.connect(store)
    try:
        session = ts.load_session(store, seal)
    except Exception:  # noqa: BLE001 - sealed with another key
        ts.set_state(db, error='session_unreadable')
        return 0
    if args.command == 'login':
        if session:
            emit('error', code='already', message='This store is logged in already.')
            return 3
        client = client_for(args, None)
        try:
            asyncio.run(login(client, store, seal, phone=args.phone))
        except SystemExit:
            raise
        except Exception as error:  # noqa: BLE001 - said to the dashboard as one short code
            code = stop_reason(error) or (str(error) if isinstance(error, RuntimeError) else error_name(error))
            wait = flood_seconds(error)
            emit('error', code=code[:60], **({'wait': wait} if wait else {}))
            if stop_reason(error) == 'app_blocked':
                ts.set_state(db, error='app_blocked')
            return 1
        return 0
    if args.command == 'logout':
        if session:
            try:
                asyncio.run(logout(client_for(args, session)))
            except Exception as error:  # noqa: BLE001 - the session goes from this Machine either way
                emit('error', code=stop_reason(error) or error_name(error)[:60])
        ts.forget_session(store)
        ts.set_state(db, error='logged_out')
        emit('logged_out')
        return 0
    if not session:
        ts.set_state(db, error=ts.get_state(db).get('error') or 'signed_out')
        return 0  # nothing to follow: Connections asks to log in again
    if ts.get_state(db).get('error') in ts.ERRORS or ts.get_state(db).get('error') == 'logged_out':
        return 0  # stopped for a reason only the owner can fix (log in again, an app ID): never retried by itself
    include = [c for c in (args.include or '').split(',') if c]
    client = client_for(args, session, receive=True)
    mirror = Mirror(client, store, seal, include)
    try:
        return asyncio.run(follow(client, mirror))
    except Exception as error:  # noqa: BLE001 - every stop leaves its reason in the store for the app
        reason, seconds = stop_reason(error), flood_seconds(error)
        if reason:
            if reason == 'signed_out':
                ts.forget_session(store)
            ts.set_state(db, error=reason)
            return 0
        if seconds:
            ts.set_state(db, flood_until=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat(timespec='seconds'))
            time.sleep(min(seconds, FLOOD_LIMIT))
        print('telegram mirror stopped:', error_name(error), file=sys.stderr, flush=True)
        return TEMPORARY


def main(argv=None):
    parser = argparse.ArgumentParser(description='The Telegram chats mirror of The Machine')
    parser.add_argument('--store')
    parser.add_argument('--app', help='file with TELEGRAM_API_ID= and TELEGRAM_API_HASH= lines')
    parser.add_argument('--lib', required=True, help='where the pinned libraries are unpacked (telegram_release.install)')
    parser.add_argument('--database', help="The Machine's database, whose message key seals the store")
    parser.add_argument('--include', help='chat IDs to read although muted, archived or big, comma separated')
    parser.add_argument('command', choices=('login', 'follow', 'logout', 'version'))
    parser.add_argument('--phone')
    args = parser.parse_args(argv)
    import telegram_release
    try:  # this pin's libraries, unpacked once (an update with a new pin unpacks the new one here)
        lib = telegram_release.installed(Path(args.lib).expanduser()) or telegram_release.install(Path(args.lib).expanduser())
    except (OSError, RuntimeError) as error:
        emit('error', code='libraries', message=str(error)[:200])
        return TEMPORARY
    sys.path.insert(0, str(lib))
    if args.command != 'version' and not (args.store and args.app):
        parser.error('--store and --app are needed')
    return run(args)


if __name__ == '__main__':
    sys.exit(main())

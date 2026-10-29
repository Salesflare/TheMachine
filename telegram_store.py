"""The Telegram chats store: what the mirror (telegram_mirror.py, the only process that holds the Telegram session)
writes and the app reads. Standard library only, so the app never imports Telethon.

One folder per account (`store`), mode 700:
- `session.sealed`: the Telegram session (Telethon's StringSession), sealed. Never logged, never in config.json.
- `telegram.sqlite`: `state` (who is signed in, the last good contact, why it stopped), `chats` (the private chats and
  small groups it reads, and why others are skipped), `messages` (their text sealed), `outbox` (sends the owner
  approved, and a log-out) and `photo_asks` (people's small profile photos the app asked for, sealed until the app
  takes them). WAL, so the app reads while the mirror writes.

Sealing: with the Machine's message key when its database has one (message_seal.py, which a host can keep off the
disk), else with a key of the store's own (`store.key`, mode 600). Either way a derived key, never the message key
itself, and the session is unreadable from a copy of the folder without that key."""
import datetime as dt
import hashlib
import json
import os
import sqlite3
from pathlib import Path

import message_seal

DB_NAME = 'telegram.sqlite'
SESSION_NAME = 'session.sealed'
OWN_KEY = 'store.key'
LOCK_NAME = 'LOCK'
# Chats read by default: private chats with people and groups up to this many members. Channels, bots, Telegram's
# own service notifications (777000: login codes) and Saved Messages are never read; muted and archived chats only
# when the owner opts them in (account `telegram_include`).
GROUP_LIMIT = 50
SERVICE_IDS = {'777000', '42777'}
BACKFILL_DAYS = 7
SCHEMA = '''
CREATE TABLE IF NOT EXISTS state(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS chats(id TEXT PRIMARY KEY, kind TEXT NOT NULL, name BLOB, members INTEGER, muted INTEGER NOT NULL DEFAULT 0,
  archived INTEGER NOT NULL DEFAULT 0, skipped TEXT NOT NULL DEFAULT '', updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS messages(chat_id TEXT NOT NULL, msg_id INTEGER NOT NULL, from_me INTEGER NOT NULL, sender_id TEXT,
  sender_name BLOB, text BLOB, media_type TEXT NOT NULL DEFAULT '', occurred_at TEXT NOT NULL, edited INTEGER NOT NULL DEFAULT 0,
  deleted INTEGER NOT NULL DEFAULT 0, reply_to INTEGER, PRIMARY KEY(chat_id, msg_id));
CREATE INDEX IF NOT EXISTS messages_at ON messages(occurred_at);
CREATE TABLE IF NOT EXISTS outbox(id TEXT PRIMARY KEY, op TEXT NOT NULL, chat_id TEXT, text BLOB, approval TEXT, created_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'queued', msg_id INTEGER, error TEXT, done_at TEXT);
CREATE TABLE IF NOT EXISTS photo_asks(user_id TEXT PRIMARY KEY, asked_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'queued',
  photo_id TEXT, type TEXT, data BLOB, done_at TEXT);
'''
# Profile photos: the small one (160 px) only, at most this big, like every other photo the Machine keeps
# (enrichment.PHOTO_BYTES). The mirror answers at most PHOTOS_PER_DAY asks a day.
PHOTO_BYTES = 200_000
PHOTOS_PER_DAY = 50
# Why the mirror stopped, as the app shows it (state `error`)
ERRORS = {
    'signed_out': 'Telegram signed this Machine out. Log in again to keep reading.',
    'app_blocked': 'Telegram stopped accepting this Machine’s app ID. Nothing is read or sent. Add your own app ID, or wait for an update.',
    'session_unreadable': 'The saved Telegram login can’t be opened with this Machine’s key. Log in again.',
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def private_dir(path):
    path = Path(path).expanduser()
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def store_key(store, database=None, create=True):
    """The 32-byte key this store seals with, derived from the Machine's message key or the store's own."""
    key = None
    if database:
        try:
            key = message_seal.load_key(database)
        except (message_seal.SealError, OSError):
            key = None
    if key is None:
        own = Path(store) / OWN_KEY
        if own.exists():
            key = bytes.fromhex(own.read_text().strip())
        elif create:
            private_dir(store)
            key = os.urandom(32)
            fd = os.open(own, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w') as out:
                out.write(key.hex() + '\n')
        else:
            return None
    return hashlib.blake2b(key=key, person=b'tm-telegram', digest_size=32).digest()


def sealer(store, database=None, create=True):
    key = store_key(store, database, create)
    return message_seal.Sealer(key) if key else None


def connect(store, readonly=False):
    path = Path(store) / DB_NAME
    if readonly:
        db = sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=10)
    else:
        private_dir(store)
        db = sqlite3.connect(path, timeout=30)
        db.execute('PRAGMA journal_mode=WAL')
        db.executescript(SCHEMA)
        try:
            path.chmod(0o600)
        except OSError:
            pass
    db.row_factory = sqlite3.Row
    return db


def get_state(db):
    return {r['key']: json.loads(r['value']) for r in db.execute('SELECT key, value FROM state')}


def set_state(db, **values):
    for key, value in values.items():
        if value is None:
            db.execute('DELETE FROM state WHERE key=?', (key,))
        else:
            db.execute('INSERT INTO state(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, json.dumps(value)))
    db.commit()


def save_session(store, seal, text):
    """The session string, sealed, written atomically with mode 600."""
    path = private_dir(store) / SESSION_NAME
    temporary = path.with_name(path.name + '.new')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'wb') as out:
        out.write(seal.seal(text))
        out.flush()
        os.fsync(out.fileno())
    os.replace(temporary, path)


def load_session(store, seal):
    """The session string, or None when there is none. Raises message_seal.SealError when it does not open."""
    path = Path(store) / SESSION_NAME
    if not path.exists():
        return None
    return seal.open(path.read_bytes())


def forget_session(store):
    for name in (SESSION_NAME, SESSION_NAME + '.new'):
        try:
            (Path(store) / name).unlink()
        except FileNotFoundError:
            pass


def identity(user_id):
    """What config.json keeps of the signed-in account: a hash of its user ID, never the ID itself."""
    return hashlib.sha256(('telegram:' + str(user_id)).encode()).hexdigest()


def readable(chat, include=()):
    """Whether a chat is read: '' when it is, else why not. `chat` has kind, members, muted, archived, id."""
    cid = str(chat.get('id'))
    if cid in SERVICE_IDS or chat.get('kind') in ('channel', 'bot', 'self'):
        return chat.get('kind') if chat.get('kind') in ('channel', 'bot', 'self') else 'service'
    if cid in {str(i) for i in include}:
        return ''
    if chat.get('kind') == 'group' and (chat.get('members') or 0) > GROUP_LIMIT:
        return 'big_group'
    if chat.get('muted'):
        return 'muted'
    if chat.get('archived'):
        return 'archived'
    return ''


def ask_photo(db, seal, user_id):
    """The app's ask for a person's profile photo (enrichment.telegram_photos_step), on a writable connection: the
    mirror's answer once it has one, taken out of the store, else the ask is left (or kept) for the mirror.
    {'id', 'data': bytes} for a photo, {} when they have none the owner can see (or it is not someone in a chat the
    mirror reads), {'id'} when it couldn't be fetched (asked again the next day), {'pending': True} while it waits."""
    row = db.execute('SELECT * FROM photo_asks WHERE user_id=?', (str(user_id),)).fetchone()
    if row is None:
        db.execute('INSERT INTO photo_asks(user_id, asked_at) VALUES (?, ?)', (str(user_id), now()))
        db.commit()
        return {'pending': True}
    if row['status'] == 'queued':
        return {'pending': True}
    db.execute('DELETE FROM photo_asks WHERE user_id=?', (str(user_id),))
    db.commit()
    if row['status'] == 'done' and row['data'] is not None:
        return {'id': row['photo_id'] or 'photo', 'data': seal.open_bytes(bytes(row['data']))}
    return {'id': 'failed'} if row['status'] == 'failed' else {}


def answer_photo(db, seal, user_id, status, photo_id=None, data=None):
    """The mirror's answer to one ask: 'done' with the photo's bytes (sealed here), 'none' or 'failed'. A photo bigger
    than PHOTO_BYTES counts as failed. Returns the answer kept."""
    keep = data if status == 'done' and data and len(data) <= PHOTO_BYTES else None
    status = 'done' if keep else ('failed' if status == 'done' else status)
    db.execute('UPDATE photo_asks SET status=?, photo_id=?, type=?, data=?, done_at=? WHERE user_id=?',
               (status, photo_id, 'image/jpeg' if keep else None, seal.seal_bytes(keep) if keep else None, now(), str(user_id)))
    db.commit()
    return status


def read_app(path):
    """(api_id, api_hash) from an app credential file of KEY=value lines, or None."""
    try:
        lines = Path(path).expanduser().read_text().splitlines()
    except (OSError, TypeError):
        return None
    values = dict(line.split('=', 1) for line in lines if '=' in line and not line.lstrip().startswith('#'))
    api_id, api_hash = values.get('TELEGRAM_API_ID', '').strip(), values.get('TELEGRAM_API_HASH', '').strip()
    if api_id.isdigit() and len(api_hash) == 32 and all(c in '0123456789abcdef' for c in api_hash.lower()):
        return int(api_id), api_hash.lower()
    return None

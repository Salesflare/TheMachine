"""The Signal store: what the mirror (signal_mirror.py, the only process that runs signal-cli for the account) writes
and the app reads. Standard library only. Every write goes through a function here, so sealing stays in one place.

One folder per account (`store`), mode 700:
- `signal-keys/`: signal-cli's own data for this linked device (its keys and the account's identity). It stays on this
  Machine; nothing here copies or logs it, and an export takes it only with the keys (moving.SECRET_DIRS).
- `signal.sqlite`: `signal_state` (who is linked, the last good contact, why it stopped), `signal_chats` (people and
  groups, their names sealed), `signal_messages` (their text and the sender's name sealed) and `signal_outbox` (sends the
  owner approved, and an unlink). WAL, so the app reads while the mirror writes.

Sealing: with the Machine's message key when its database has one (message_seal.py), else with a key of the store's own
(`store.key`, mode 600). Either way a key derived for this store, never the message key itself.

Signal gives a newly linked device no older messages: the store starts at the moment of linking."""
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
from pathlib import Path

import message_seal

DB_NAME = 'signal.sqlite'
CLI_DIR = 'signal-keys'
OWN_KEY = 'store.key'
LOCK_NAME = 'LOCK'
DEVICE = 'The Machine'  # the name the phone shows under Signal, Settings, Linked devices
SCHEMA = '''
CREATE TABLE IF NOT EXISTS signal_state(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS signal_chats(id TEXT PRIMARY KEY, kind TEXT NOT NULL, name BLOB, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS signal_messages(chat_id TEXT NOT NULL, author TEXT NOT NULL, sent_at INTEGER NOT NULL, from_me INTEGER NOT NULL,
  sender_name BLOB, text BLOB, media_type TEXT NOT NULL DEFAULT '', occurred_at TEXT NOT NULL, edited INTEGER NOT NULL DEFAULT 0,
  deleted INTEGER NOT NULL DEFAULT 0, expires_at TEXT, quote_author TEXT, quote_sent_at INTEGER,
  PRIMARY KEY(chat_id, author, sent_at));
CREATE INDEX IF NOT EXISTS signal_messages_at ON signal_messages(occurred_at);
CREATE TABLE IF NOT EXISTS signal_outbox(id TEXT PRIMARY KEY, op TEXT NOT NULL, chat_id TEXT, text BLOB, approval TEXT, created_at TEXT NOT NULL,
  quote_author TEXT, quote_sent_at INTEGER, status TEXT NOT NULL DEFAULT 'queued', sent_at INTEGER, error TEXT, done_at TEXT);
'''
# Why the mirror stopped, as the app shows it (state `error`)
ERRORS = {
    'unlinked': 'Signal unlinked this Machine. Link it again to keep reading.',
    'outdated': 'Signal no longer accepts this Machine’s Signal client. Update The Machine.',
    'store_unreadable': 'The Signal store can’t be opened with this Machine’s key. Link it again.',
}
# A Signal chat: a person's account ID (a UUID), or a group as g: and its base64 group ID
PERSON = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
GROUP = r'g:[A-Za-z0-9+/=_-]{8,100}'
CHAT = rf'(?:{PERSON}|{GROUP})'


def re_person(value):
    return bool(re.fullmatch(PERSON, str(value or '')))


def re_chat(value):
    return bool(re.fullmatch(CHAT, str(value or '')))


def touches(m, weights):
    """A Signal message's person for the Graph (graph.touches), as Telegram's: the chat's account ID in a one-to-one,
    the sender's in a group (seen), never the owner."""
    chat, mine, sender = str(m.get('chat_id') or ''), m.get('from_me') is True, str(m.get('sender_id') or '')
    if m.get('chat_kind') == 'group':
        return [] if mine or not re_person(sender) else [('sig:' + sender, m.get('from'), 0.1, 'seen')]
    return [('sig:' + chat, m.get('chat_name'), weights['owner' if mine else 'them'], 'owner' if mine else 'them')] if re_person(chat) else []


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
    return hashlib.blake2b(key=key, person=b'tm-signal', digest_size=32).digest()


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
    return {r['key']: json.loads(r['value']) for r in db.execute('SELECT key, value FROM signal_state')}


def set_state(db, **values):
    for key, value in values.items():
        if value is None:
            db.execute('DELETE FROM signal_state WHERE key=?', (key,))
        else:
            db.execute('INSERT INTO signal_state(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, json.dumps(value)))
    db.commit()


def cli_dir(store):
    return private_dir(Path(store) / CLI_DIR)


def forget_link(store):
    """The linked device's keys go from this Machine (an unlink, a new link)."""
    shutil.rmtree(Path(store) / CLI_DIR, ignore_errors=True)


def identity(number):
    """What config.json keeps of the linked account: a hash of its number (or account ID), never the number itself."""
    return hashlib.sha256(('signal:' + str(number)).encode()).hexdigest()


def save_chat(db, seal, chat_id, kind, name):
    """A person's or a group's chat, with its name sealed. A chat already known keeps its name when none is given."""
    if not name and db.execute('SELECT 1 FROM signal_chats WHERE id=?', (chat_id,)).fetchone():
        return
    db.execute('INSERT INTO signal_chats(id, kind, name, updated_at) VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET '
               'kind=excluded.kind, name=excluded.name, updated_at=excluded.updated_at', (chat_id, kind, seal.seal(name or ''), now()))


def known_chat(db, chat_id):
    return bool(db.execute('SELECT 1 FROM signal_chats WHERE id=?', (chat_id,)).fetchone()
                or db.execute('SELECT 1 FROM signal_messages WHERE chat_id=? LIMIT 1', (chat_id,)).fetchone())


def keep_message(db, seal, m):
    """One message (again after an edit), its text and sender's name sealed. `m`: chat_id, author ('me' for the owner),
    sent_at (Signal's own timestamp in ms, which names a message), from_me, sender, text, media, edited, expires_at,
    quote_author, quote_sent_at."""
    db.execute('INSERT INTO signal_messages(chat_id, author, sent_at, from_me, sender_name, text, media_type, occurred_at, edited, expires_at, '
               'quote_author, quote_sent_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(chat_id, author, sent_at) DO UPDATE SET '
               'text=excluded.text, media_type=excluded.media_type, edited=max(edited, excluded.edited), sender_name=excluded.sender_name',
               (m['chat_id'], m['author'], int(m['sent_at']), int(m['from_me']), seal.seal(m['sender'][:200]), seal.seal(m['text'][:40000]),
                m.get('media') or '', dt.datetime.fromtimestamp(int(m['sent_at']) / 1000, dt.timezone.utc).isoformat(), int(bool(m.get('edited'))),
                m.get('expires_at'), m.get('quote_author'), m.get('quote_sent_at')))
    db.commit()


def remove_message(db, author, sent_at):
    """Deleted for everyone: the row stays, its text goes."""
    db.execute('UPDATE signal_messages SET deleted=1, text=NULL WHERE author=? AND sent_at=?', (author, int(sent_at)))
    db.commit()


def purge_expired(db, at=None):
    """Disappearing messages: their text goes once their timer is up, as on the owner's phone."""
    count = db.execute('UPDATE signal_messages SET deleted=1, text=NULL WHERE expires_at IS NOT NULL AND expires_at<=? AND text IS NOT NULL',
                       (at or now(),)).rowcount
    db.commit()
    return count


def queue_send(db, seal, job, chat_id, text, quote=None):
    """The app's side of a send the owner approved: one outbox row, keyed by its action job, so it is queued once."""
    db.execute("INSERT OR IGNORE INTO signal_outbox(id, op, chat_id, text, approval, created_at, quote_author, quote_sent_at) "
               "VALUES (?, 'send', ?, ?, ?, ?, ?, ?)", (job, chat_id, seal.seal(text), job, now(), (quote or {}).get('author'), (quote or {}).get('sent_at')))
    db.commit()


def next_outbox(db):
    return db.execute("SELECT * FROM signal_outbox WHERE status='queued' ORDER BY created_at, rowid LIMIT 1").fetchone()


def mark_outbox(db, row_id, status, sent_at=None, error=None):
    """'sending' only from 'queued' (a send that may have gone out is never sent again); 'sent', 'failed' or 'done' after."""
    if status == 'sending':
        db.execute("UPDATE signal_outbox SET status='sending' WHERE id=? AND status='queued'", (row_id,))
    else:
        db.execute('UPDATE signal_outbox SET status=?, sent_at=?, error=?, done_at=? WHERE id=?', (status, sent_at, error, now(), row_id))
    db.commit()


def hold_outbox(db, reason, at):
    """After an import (machine/export/hold.py): what waited to go out stops with `reason`, never sent by itself."""
    return db.execute("UPDATE signal_outbox SET status='held',error=?,done_at=? WHERE status='queued'", (reason, at)).rowcount

"""Files the owner adds to a chat message (the card chat's composer: attach, paste, drag and drop).

Each file is uploaded on its own as soon as it is added (`save`), kept in the app's data folder (chat-files/ next to the
database, mode 700, one file per upload named by its ID), and bound to the message when it is sent (`bind`, in the
same transaction as the message). With message protection on (message_seal.py) a file is kept sealed with the message
key, as one sealed file (message_seal.FILE_MAGIC), and its name is sealed in the database (message_seal.DERIVED), like
an email attachment (mail_attachments.py). A file is opened only for a preview (`read`) and for its run.

The message's run gets them (`for_run`): images go to the model as images (the Gateway's `agent` attachments); every
file also gets a readable copy in the runs' private folder (mail_attachments.open_root, in memory when there is one),
so the agent can read a document with its own tools or attach a file to a draft. That copy goes once the run has ended
(mail_attachments.sweep). Files never sent go after a day, and a deleted card's go with it (`sweep`).

Only types the agent can use are taken, checked by extension and, for images and PDFs, by their first bytes, so a file
is never served as something it is not. Images are at most IMAGE_BYTES (the Gateway takes up to 6 MB per image),
other files at most FILE_BYTES, and a message has at most MAX_FILES files with at most IMAGES_BYTES of images (so the
run's request stays within the Gateway's 25 MB frame)."""
from __future__ import annotations

import base64
import binascii
import datetime as dt
import os
import re
import secrets
from pathlib import Path

import mail_attachments
import message_seal

IMAGE_BYTES = 5 * 1024 * 1024
FILE_BYTES = 10 * 1024 * 1024
IMAGES_BYTES = 15 * 1024 * 1024
MAX_FILES = 5
# The upload request: one file, base64 in JSON, with room for its name and the request around it.
REQUEST_BYTES = FILE_BYTES * 4 // 3 + 64 * 1024
UNSENT_HOURS = 24

IMAGES = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp'}
FILES = {'.pdf': 'application/pdf', '.txt': 'text/plain', '.md': 'text/markdown', '.csv': 'text/csv', '.tsv': 'text/tab-separated-values',
         '.json': 'application/json', '.log': 'text/plain', '.rtf': 'application/rtf', '.eml': 'message/rfc822', '.ics': 'text/calendar',
         '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
         '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
         '.odt': 'application/vnd.oasis.opendocument.text', '.ods': 'application/vnd.oasis.opendocument.spreadsheet'}
TYPES = {**IMAGES, **FILES}
MAGIC = {'image/png': (b'\x89PNG\r\n\x1a\n',), 'image/jpeg': (b'\xff\xd8\xff',), 'image/gif': (b'GIF87a', b'GIF89a'),
         'application/pdf': (b'%PDF-',)}
ZIPPED = ('.docx', '.xlsx', '.pptx', '.odt', '.ods')
ID = re.compile(r'cf_[0-9a-f]{20}')


def initialize(db):
    db.execute('''CREATE TABLE IF NOT EXISTS chat_files(
        id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,decision_id TEXT,name TEXT NOT NULL,mime TEXT NOT NULL,
        size INTEGER NOT NULL,created_at TEXT NOT NULL)''')
    db.execute('CREATE INDEX IF NOT EXISTS chat_files_decision ON chat_files(decision_id)')


def folder(config):
    return Path(config['database']).expanduser().parent / 'chat-files'


def _sealer(db):
    """The message key's Sealer when this database is protected, else None."""
    seal = getattr(db, 'sealer', None)
    return seal if seal and message_seal.is_protected(db) else None


def _open(db, data):
    """A stored file's bytes, opened when sealed."""
    if not message_seal.is_sealed_bytes(data):
        return data
    if not getattr(db, 'sealer', None):
        raise message_seal.SealError(f'This file is encrypted and {message_seal.KEY_NAME} is missing')
    return db.sealer.open_bytes(data)


def human(size):
    return f'{size / 1048576:.1f} MB' if size >= 1048576 else f'{max(1, round(size / 1024))} KB'


def plain_name(name):
    """The file's own name, without folders, control characters or anything a path could use; at most 120 characters."""
    name = re.sub(r'[\x00-\x1f\x7f/\\:*?"<>|]+', ' ', str(name or '').rsplit('/', 1)[-1].rsplit('\\', 1)[-1])
    name = ' '.join(name.split()).strip(' .')
    stem, dot, ext = name.rpartition('.')
    if len(name) > 120:
        name = (stem[:120 - len(ext) - 1] + '.' + ext) if dot and len(ext) <= 10 else name[:120]
    return name


def kind(name, data):
    """The type of an upload from its name, checked against its first bytes: None when it isn't one this takes."""
    ext = Path(name).suffix.lower()
    mime = TYPES.get(ext)
    if not mime:
        return None
    if mime in MAGIC and not data.startswith(MAGIC[mime]):
        return None
    if mime == 'image/webp' and not (data[:4] == b'RIFF' and data[8:12] == b'WEBP'):
        return None
    if ext in ZIPPED and not data.startswith(b'PK\x03\x04'):
        return None
    return mime


def too_big(mime, size):
    """Why a file is too big, in the owner's words, or None."""
    limit = IMAGE_BYTES if mime.startswith('image/') else FILE_BYTES
    if size > limit:
        return f"That file is too big ({human(size)}). {'Images' if mime.startswith('image/') else 'Files'} can be up to {human(limit)}."
    return None


def save(db, config, suggestion_id, name, data_b64, stamp):
    """Keep one upload for a card's next message: {id, name, type, size}. ValueError in the owner's words."""
    if not db.execute('SELECT 1 FROM suggestions WHERE id=?', (suggestion_id,)).fetchone():
        raise ValueError('Unknown suggestion')
    name = plain_name(name)
    if not name or not isinstance(data_b64, str):
        raise ValueError('That file has no name')
    if len(data_b64) > REQUEST_BYTES:
        raise ValueError(f'That file is too big. Files can be up to {human(FILE_BYTES)}.')
    try:
        data = base64.b64decode(data_b64, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError('That file didn’t upload. Try again.') from None
    if not data:
        raise ValueError('That file is empty')
    mime = kind(name, data)
    if not mime:
        raise ValueError('I can’t read that type of file. Add an image, a PDF, a text or an Office file.')
    if (why := too_big(mime, len(data))):
        raise ValueError(why)
    if db.execute('SELECT count(*) FROM chat_files WHERE suggestion_id=? AND decision_id IS NULL', (suggestion_id,)).fetchone()[0] >= MAX_FILES * 4:
        raise ValueError('Too many files waiting. Send or remove some first.')
    root = folder(config)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    file_id = 'cf_' + secrets.token_hex(10)
    path = root / file_id
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    seal = _sealer(db)
    with os.fdopen(fd, 'wb') as out:
        out.write(seal.seal_bytes(data) if seal else data)
    db.execute('INSERT INTO chat_files(id,suggestion_id,decision_id,name,mime,size,created_at) VALUES(?,?,NULL,?,?,?,?)',
               (file_id, suggestion_id, name, mime, len(data), stamp))
    return {'id': file_id, 'name': name, 'type': mime, 'size': len(data)}


def check(db, suggestion_id, ids, decision_id=None):
    """The uploads a message carries, checked before it is saved: [rows]. ValueError when one isn't this card's and
    waiting (or already with this same message, sent again)."""
    if not ids:
        return []
    if not isinstance(ids, list) or len(ids) > MAX_FILES or len(set(map(str, ids))) != len(ids):
        raise ValueError(f'A message can carry up to {MAX_FILES} files')
    rows = []
    for file_id in ids:
        row = db.execute('SELECT * FROM chat_files WHERE id=? AND suggestion_id=? AND (decision_id IS NULL OR decision_id=?)',
                         (str(file_id), suggestion_id, decision_id)).fetchone() \
            if ID.fullmatch(str(file_id)) else None
        if not row:
            raise ValueError('A file is gone. Add it again.')
        rows.append(row)
    if sum(r['size'] for r in rows if r['mime'].startswith('image/')) > IMAGES_BYTES:
        raise ValueError(f'The images are too big together. A message can carry up to {human(IMAGES_BYTES)} of images.')
    return rows


def bind(db, decision_id, rows):
    for r in rows:
        db.execute('UPDATE chat_files SET decision_id=? WHERE id=? AND decision_id IS NULL', (decision_id, r['id']))


def remove(db, config, suggestion_id, file_id):
    """Take back an upload that wasn't sent yet."""
    if not ID.fullmatch(str(file_id or '')):
        raise ValueError('Unknown file')
    if db.execute('DELETE FROM chat_files WHERE id=? AND suggestion_id=? AND decision_id IS NULL', (file_id, suggestion_id)).rowcount:
        (folder(config) / file_id).unlink(missing_ok=True)
    return {'removed': True}


def listed(db, decision_ids):
    """{decision id: [{id, name, type, size}]} for the chat."""
    out = {}
    ids = list(decision_ids)
    for start in range(0, len(ids), 500):
        part = ids[start:start + 500]
        for r in db.execute('SELECT id,decision_id,name,mime,size FROM chat_files WHERE decision_id IN (' + ','.join('?' * len(part)) + ') ORDER BY rowid', part):
            out.setdefault(r['decision_id'], []).append({'id': r['id'], 'name': r['name'], 'type': r['mime'], 'size': r['size']})
    return out


def read(db, config, file_id):
    """(bytes, type, name) of one file, for the dashboard."""
    row = db.execute('SELECT * FROM chat_files WHERE id=?', (str(file_id),)).fetchone() if ID.fullmatch(str(file_id or '')) else None
    if not row:
        raise ValueError('Unknown file')
    return _open(db, (folder(config) / row['id']).read_bytes()), row['mime'], row['name']


def for_run(db, config, decision_id, job_id):
    """What a run gets of its message's files: (Gateway attachments for the images, the prompt's lines about all of
    them). Each file gets a readable copy by its own name in the run's private folder, removed once the run has ended."""
    rows = db.execute('SELECT * FROM chat_files WHERE decision_id=? ORDER BY rowid', (decision_id,)).fetchall() if decision_id else []
    if not rows:
        return [], ''
    base = mail_attachments.open_root(config, create=True)
    if not base:
        raise OSError('No private folder for the run')
    target = base / re.sub(r'[^A-Za-z0-9_-]', '', job_id)[:80]
    target.mkdir(exist_ok=True, mode=0o700)
    images, lines, names = [], [], set()
    for r in rows:
        source = folder(config) / r['id']
        try:
            data = _open(db, source.read_bytes())
        except (OSError, message_seal.SealError):
            lines.append(f"- {r['name']}: this file is missing on this computer")
            continue
        name, n = r['name'], 1
        while name.lower() in names:  # two files of the same name keep both
            n += 1
            stem, ext = os.path.splitext(r['name'])
            name = f'{stem} ({n}){ext}'
        names.add(name.lower())
        path = target / name
        if path.is_symlink():
            path.unlink()
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
        if r['mime'].startswith('image/'):
            images.append({'type': 'image', 'mimeType': r['mime'], 'fileName': name, 'content': base64.b64encode(data).decode()})
        lines.append(f"- {path} ({r['mime']}, {human(r['size'])}){' (also in this message as an image)' if r['mime'].startswith('image/') else ''}")
    note = ('\n\nThe owner attached these files to their message. They are part of what they ask: read each one before you '
            'answer (images are in this message; read documents with your tools). You can attach them to a draft from these paths.\n' + '\n'.join(lines))
    return images, note


def sweep(db, config, stamp):
    """Uploads never sent (older than a day) and the files of cards that are gone. Kept files follow message
    protection: sealed in place once it is on, opened again once it is off."""
    cutoff = (dt.datetime.fromisoformat(stamp) - dt.timedelta(hours=UNSENT_HOURS)).isoformat()
    gone = [r['id'] for r in db.execute('SELECT id FROM chat_files WHERE (decision_id IS NULL AND created_at<?) '
                                        'OR NOT EXISTS(SELECT 1 FROM suggestions s WHERE s.id=chat_files.suggestion_id)', (cutoff,))]
    for file_id in gone:
        db.execute('DELETE FROM chat_files WHERE id=?', (file_id,))
        (folder(config) / file_id).unlink(missing_ok=True)
    seal, key = _sealer(db), getattr(db, 'sealer', None)
    if key:
        for r in db.execute('SELECT id FROM chat_files').fetchall():
            path = folder(config) / r['id']
            try:
                sealed = message_seal.is_sealed_file(path)
                if seal and not sealed:
                    mail_attachments._write(path, seal.seal_bytes(path.read_bytes()), scrub=True)
                elif sealed and not seal:
                    mail_attachments._write(path, key.open_bytes(path.read_bytes()))
            except (OSError, message_seal.SealError):
                pass
    return len(gone)


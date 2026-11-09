"""Moving The Machine: everything it knows and how it is set up, in one archive, and back again on another computer.

An export holds everything The Machine knows and has done (machine/export/inventory.py lists it by part): the
databases (messages from every source, to-dos with their history, drafts and sends, decisions, promises, the Graph,
memories, learned preferences, skills, agent jobs), the data folder's files (attachments, photos, job folders),
config.json, connectors you built yourself, your OpenClaw workspace (AGENTS.md, USER.md, memory notes), OpenClaw's
conversations and their photos (machine/export/home.py), the agent jobs' own transcripts and who may talk to your
Telegram bot. Its manifest.json lists every part with counts and checksums, and what could not come along and why.

It is always encrypted as a whole (AES-256, stretched with PBKDF2, through openssl, so only `assistant import` or
openssl opens it), with a passphrase you pick or, without one, an export code made for it and shown once (CODE).
Keys and tokens come along only when asked (`keys=True`), and then only with a passphrase you pick; without them the
import lists what to connect again. The archive is packed straight into openssl, so no unencrypted archive is
written; the database copies it needs on the way sit in a private folder (700) next to the archive and are
overwritten before they are removed, as is what an import unpacks.

An import puts it all back on a fresh install and holds what was waiting (machine/export/hold.py): nothing is sent
by itself, and nothing old comes back as a new to-do.
"""
import datetime as dt
import hashlib
import io
import secrets
import json
import os
import re
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import zipfile
from contextlib import closing
from contextlib import contextmanager
from pathlib import Path

import message_seal
import portable
from machine.export import hold as moved
from machine.export import home as elsewhere
from machine.export import inventory

FORMAT = 2  # 2: parts with counts and checksums, what was not exported, OpenClaw's conversations
APP = Path(__file__).resolve().parent
PASSPHRASE_ENV = 'THE_MACHINE_EXPORT_PASSPHRASE'
MIN_PASSPHRASE = 10
# An export code: 20 characters that can't be mistaken for one another (no 0/O, 1/I/L), about 99 bits, in groups of 4
CODE = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'
# openssl is on every Linux and macOS; the passphrase reaches it through its environment, never its arguments
OPENSSL = ['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '600000', '-md', 'sha256']
# Workspace parts that are not yours to move: the app itself (git's bookkeeping is in REBUILDABLE)
WORKSPACE_SKIP = {'tools'}
SKIP_SUFFIXES = ('.bak', '.lock', '.tmp', '-wal', '-shm', '-journal')
# Files in the data folder that are keys even when config.json does not point at them
SECRET_NAMES = {'network-keys.json', 'learnings-keys.json', 'owner-token', 'api-token', 'vapid.json', 'gog-password', 'browser-logins.sealed', 'browser-logins.enc',
                'browser-logins.key', 'session.sealed', 'fleet-token'}
SECRET_SUFFIXES = ('.key', '.pem', '.sealed', '.p12')  # a Telegram session, a store's own key, a private key
# Folders that only hold keys (a copied gog keyring, OpenClaw's credentials), and copies of OpenClaw's own settings
SECRET_DIRS = {'keyring', 'credentials', '.ssh', '.gnupg'}
SECRET_FILE = re.compile(r'^openclaw.*\.json$')
# A small text file that spells out a token, key or password is a key too, whatever its name (a saved API answer, say)
TOKEN_LIKE = re.compile(rb'(?i)(?:token|api[_-]?key|secret|password|bearer)["\']?\s*[:=]\s*["\']?[A-Za-z0-9_\-./+]{20,}')
SCAN_SUFFIXES = ('.json', '.txt', '.md', '.env', '.yaml', '.yml', '.log', '.ini', '.conf', '.toml', '.sh', '.py', '')
SCAN_LIMIT = 1_000_000
# Older copies of a database or a folder kept by hand (events.sqlite.bak-20261020): not needed to move
COPY_NAME = re.compile(r'\.(?:bak|backup)[-.]|\.before-|\.pre-[^.]*\d{8}')
COPIES = 'older copies (.bak, .before-, dated .pre-)'
# Folders any computer rebuilds by itself (installed packages, caches, git's own history): left out wherever they sit
REBUILDABLE = {'.git', 'node_modules', '.venv', '.venvs', 'venv', '__pycache__', '.cache', '.pytest_cache', '.mypy_cache',
               '.ruff_cache', '.tox'}
# Tokens that only work for a hosted server; they are never exported
HOSTED_ONLY = {'google-broker', 'microsoft-broker', 'zoom-broker', 'google_meet-broker', 'google_docs-broker'}
# Settings a hosted server added that mean nothing elsewhere
HOSTED_KEYS = ('google_broker', 'microsoft_broker', 'zoom_broker', 'google_meet_broker', 'google_docs_broker', 'salesforce_broker', 'manage_url', 'needs_you_file')


class MoveError(Exception):
    pass


def _workspace(path=None):
    return Path(path or os.environ.get('OPENCLAW_WORKSPACE') or Path.home() / '.openclaw/workspace').expanduser()


def home_root(openclaw_home=None, home=None):
    """The home folder an export reads (and an import writes) the send logs and agent transcripts in: given, else the
    folder OpenClaw's sits in (the home folder, or a test's own folder)."""
    return Path(home).expanduser() if home else _openclaw_home(openclaw_home).parent


def _openclaw_home(path=None):
    return Path(path or os.environ.get('OPENCLAW_HOME') or Path.home() / '.openclaw').expanduser()


def _size(root):
    total = 0
    for base, _, names in os.walk(root):
        for name in names:
            try:
                total += os.lstat(os.path.join(base, name)).st_size
            except OSError:
                pass
    return total


def _files(root, skip_top=(), left_out=None):
    """The files under root worth moving. Folders any computer rebuilds (REBUILDABLE) and hand-made copies stay out;
    left_out, when given, counts their bytes by name so the export can say what it skipped."""
    found = []
    for base, dirs, names in os.walk(root):
        here = Path(base)
        for name in list(dirs):
            path = here / name
            if (here == root and name in skip_top) or path.is_symlink():
                dirs.remove(name)
            elif name in REBUILDABLE:
                dirs.remove(name)
                if left_out is not None:
                    left_out[name] = left_out.get(name, 0) + _size(path)
        for name in names:
            path = here / name
            if path.is_symlink() or not path.is_file() or name.endswith(SKIP_SUFFIXES):
                continue
            if COPY_NAME.search(name):
                if left_out is not None:
                    left_out[COPIES] = left_out.get(COPIES, 0) + path.stat().st_size
                continue
            found.append((path, path.relative_to(root)))
    return sorted(found)


def _secretish(path, relative):
    """A key by where it sits, its name, or what it says, even when config.json does not point at it."""
    if path.name in SECRET_NAMES or path.suffix in ('.env', *SECRET_SUFFIXES) or SECRET_FILE.match(path.name):
        return True
    if SECRET_DIRS & set(relative.parts[:-1]):
        return True
    if path.suffix.lower() not in SCAN_SUFFIXES:
        return False
    try:
        if path.stat().st_size > SCAN_LIMIT:
            return False
        return bool(TOKEN_LIKE.search(path.read_bytes()))
    except OSError:
        return False


def plan(config_path, workspace=None, openclaw_home=None, left_out=None, home=None):
    """What an export holds: [(kind, source path, name in the archive)]. kind is db, file, secret or openclaw-db (an
    OpenClaw database, its sign-in tables emptied without keys). left_out, when given, collects the bytes of what was
    skipped as rebuildable (see _files)."""
    config_path = Path(config_path).expanduser()
    config = json.loads(config_path.read_text())
    data = config_path.parent
    keys = {Path(p).expanduser().resolve() for name, p in (config.get('credentials') or {}).items() if name not in HOSTED_ONLY}
    from network import keys_path
    network_key = keys_path(config)
    if network_key:
        keys.add(network_key.resolve())
    hosted = {Path(p).expanduser().resolve() for name, p in (config.get('credentials') or {}).items() if name in HOSTED_ONLY}
    items = [('file', config_path, 'config/config.json')]
    for path, relative in _files(data, left_out=left_out):
        resolved = path.resolve()
        if path == config_path or resolved in hosted or path.name in ('machine-token', message_seal.KEY_NAME, message_seal.KEYRING_NAME, message_seal.KEY_NAME + '.moving'):
            continue
        if path.suffix in ('.sqlite', '.db'):
            items.append(('db', path, f'data/{relative}'))
        elif resolved in keys or _secretish(path, relative):
            items.append(('secret', path, f'secrets/data/{relative}'))
        else:
            items.append(('file', path, f'data/{relative}'))
    for path in keys - {p.resolve() for _, p, _ in items}:  # keys kept outside the data folder
        if path.is_file():
            # the Network keys get their own place, so they can't clash with a credential of the same name
            items.append(('secret', path, f'secrets/network/{path.name}' if network_key and path == network_key.resolve()
                          else f'secrets/elsewhere/{path.name}'))
    space = _workspace(workspace)
    if space.is_dir():
        for path, relative in _files(space, WORKSPACE_SKIP, left_out):
            if path.resolve() in hosted or path.name == 'machine-token':
                continue
            secret = path.resolve() in keys or _secretish(path, relative)
            items.append(('secret' if secret else 'file', path,
                          f'{"secrets/" if secret else ""}workspace/{relative}'))
    items += [('file', path, f'connectors/{path.relative_to(APP)}') for path in own_connectors()]
    home, home_dir = _openclaw_home(openclaw_home), home_root(openclaw_home, home)
    if (home / 'openclaw.json').is_file():
        items.append(('secret', home / 'openclaw.json', 'secrets/openclaw/openclaw.json'))
    if (home / 'credentials').is_dir():
        items += [('secret', path, f'secrets/openclaw/credentials/{relative}') for path, relative in _files(home / 'credentials')]
    main = Path(config.get('database') or data / 'events.sqlite').expanduser()
    items += elsewhere.items(home, home_dir, main, config, left_out)
    # A configured credential can be reached through more than one root. Prefer the workspace's
    # restorable location, but never downgrade a known secret to an ordinary file.
    unique = {}
    for kind, path, name in items:
        previous = unique.get(path.resolve())
        if previous is None or kind == 'secret' or name.startswith(('workspace/', 'secrets/workspace/')):
            unique[path.resolve()] = (kind, path, name)
    return list(unique.values())


def own_connectors():
    """Connectors built here that the app's own repository doesn't have."""
    try:
        listed = subprocess.run(['git', '-C', str(APP), 'ls-files', '--others', '--exclude-standard', '--', 'connectors',
                                 'tests/test_connector_*.py', 'test_connector_*.py'], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    return [APP / line for line in listed.stdout.splitlines()
            if line.endswith('.py') and '__pycache__' not in line and (APP / line).is_file()]


def telegram(openclaw_home=None):
    """Who may talk to the bot, without the bot's token: enough to recognize you again after a move."""
    try:
        config = json.loads((_openclaw_home(openclaw_home) / 'openclaw.json').read_text())
    except (OSError, ValueError):
        return None
    allowed = (config.get('commands') or {}).get('ownerAllowFrom') or []
    channel = (config.get('channels') or {}).get('telegram') or {}
    return {'enabled': bool(channel.get('enabled')), 'owner_allow_from': allowed} if channel or allowed else None


def network_identity(config):
    """Whether this Machine has keys on The Machine Network (network-keys.json): they are its identity there."""
    from network import keys_path
    found = keys_path(config)
    return bool(found and found.is_file())


def reconnect(config, secrets):
    """What has to be connected again after an import, in plain words."""
    out = []
    for account in config.get('accounts') or []:
        service = account.get('service', 'gmail')
        if account.get('transport') == 'broker' and service in ('outlook', 'outlook_calendar'):
            out.append(f'{account["id"]}: sign in to Microsoft again (hosted Microsoft access does not move along): assistant connect '
                       + service)
        elif account.get('transport') == 'broker':
            out.append(f'{account["id"]}: sign in to Google again (hosted Google access does not move along)')
        elif not secrets and account.get('credential'):
            out.append(f'{account["id"]}: its {service} key or token')
    out.append('your model: sign in to ChatGPT or your Claude plan again, or paste your API key')
    if not secrets:
        out.append('Telegram: your bot token (the people allowed to talk to it are kept)')
    if not secrets and network_identity(config):
        out.append('The Machine Network: a new Network identity will be made; your teammates and friends see a '
                   'key-change notice once')
    return out


def estimate(config_path, secrets=False, workspace=None, openclaw_home=None, home=None):
    left_out = {}
    items = [i for i in plan(config_path, workspace, openclaw_home, left_out, home) if secrets or i[0] != 'secret']
    return {'files': len(items), 'bytes': sum(path.stat().st_size for _, path, _ in items), 'left_out': left_out}


class _Hashing:
    """A file read into the archive, hashed on the way: one pass over it."""

    def __init__(self, handle):
        self.handle, self.sha = handle, hashlib.sha256()

    def read(self, size=-1):
        data = self.handle.read(size)
        self.sha.update(data)
        return data


def _add_file(archive, path, entry):
    """Add one file and return its sha256."""
    info = archive.gettarinfo(str(path), entry)
    with open(path, 'rb') as handle:
        reader = _Hashing(handle)
        archive.addfile(info, reader)
    return reader.sha.hexdigest()


def _tables(path, name):
    """{'<db>/<table>': {'part', 'rows', 'sha256'}} of an (opened) database copy."""
    out = {}
    with closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as db:
        for table, virtual in inventory.tables(db):
            if virtual:
                continue
            rows, sha = inventory.digest(db, table)
            out[f'{name}/{table}'] = {'part': inventory.part_of(table), 'rows': rows, 'sha256': sha}
    return out


def parts(files, tables):
    """The manifest's parts: {part: {'label', 'files', 'bytes', 'tables', 'rows'}}."""
    out = {key: {'label': label, 'files': 0, 'bytes': 0, 'tables': 0, 'rows': 0} for key, label in inventory.PARTS.items()}
    out['other'] = {'label': 'Other', 'files': 0, 'bytes': 0, 'tables': 0, 'rows': 0}
    for entry, found in files.items():
        part = 'settings' if entry.startswith('secrets/') else inventory.file_part(entry)
        out[part]['files'] += 1
        out[part]['bytes'] += found['bytes']
    for found in tables.values():
        out[found['part']]['tables'] += 1
        out[found['part']]['rows'] += found['rows']
    return {k: v for k, v in out.items() if v['files'] or v['tables']}


def not_exported(config, keys, emptied):
    """What this export could not take, and why: inventory.NOT_EXPORTED as true for this install."""
    services = {a.get('service') for a in config.get('accounts') or []}
    brokered = any(a.get('transport') == 'broker' for a in config.get('accounts') or [])
    out = []
    for item in inventory.NOT_EXPORTED:
        what = item['what']
        if what.startswith('Sign-ins to Google') and not brokered:
            continue
        if what.startswith("WhatsApp") and 'whatsapp' not in services:
            continue
        if keys and (what.startswith('Telegram, Slack') or what.startswith('The Machine Network')):
            continue
        out.append(dict(item))
    if emptied:
        out.append({'what': "Your AI's own sign-ins", 'why': 'kept out without keys: ' + ', '.join(sorted(set(emptied))),
                    'after': "The new install's own sign-ins are kept"})
    out += [{'what': f'~/{path}', 'why': why, 'after': ''} for path, why in inventory.NOT_EXPORTED_HOME
            if not (keys and path == '.openclaw/credentials')]
    return out


def _add_bytes(archive, name, data):
    info = tarfile.TarInfo(name)
    info.size, info.mode, info.mtime = len(data), 0o600, int(dt.datetime.now().timestamp())
    archive.addfile(info, io.BytesIO(data))


def new_code():
    """A fresh export code, like ABCD-EFGH-JKMN-PQRS-TUVW."""
    raw = ''.join(secrets.choice(CODE) for _ in range(20))
    return '-'.join(raw[i:i + 4] for i in range(0, 20, 4))


def _code_form(text):
    """What was typed, as an export code is written (upper case, groups of 4), or None when it can't be one."""
    raw = re.sub(r'[\s-]', '', text or '').upper()
    if len(raw) != 20 or any(c not in CODE for c in raw):
        return None
    return '-'.join(raw[i:i + 4] for i in range(0, 20, 4))


def export(config_path, out_dir, passphrase=None, workspace=None, openclaw_home=None, source='local', now=None, keys=False,
           home=None):
    """Write the encrypted archive (name ends in .tar.gz.enc) into out_dir and return (path, manifest). Without a
    passphrase an export code is made and returned as manifest['code'] (never written into the archive): show it,
    the import needs it. Keys and tokens come along only when `keys` is true, and then only with a passphrase."""
    if passphrase is not None and len(passphrase) < MIN_PASSPHRASE:
        raise MoveError(f'Pick a passphrase of at least {MIN_PASSPHRASE} characters')
    if keys and passphrase is None:
        raise MoveError('Keys and tokens come along only with a passphrase you pick')
    config_path = Path(config_path).expanduser()
    config = json.loads(config_path.read_text())
    secrets_too = bool(keys)
    code = None if passphrase is not None else new_code()
    left_out = {}
    items = [i for i in plan(config_path, workspace, openclaw_home, left_out, home) if secrets_too or i[0] != 'secret']
    now = now or dt.datetime.now(dt.timezone.utc)
    manifest = {'format': FORMAT, 'created_at': now.isoformat(timespec='seconds'), 'source': source,
                'data_dir': str(config_path.parent), 'workspace_dir': str(_workspace(workspace)), 'includes_keys': secrets_too,
                'telegram': telegram(openclaw_home), 'reconnect': reconnect(config, secrets_too), 'left_out': left_out,
                'network_identity': ('kept' if secrets_too else 'new') if network_identity(config) else None}
    out_dir = Path(out_dir)
    out_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    name = f'the-machine-export-{now:%Y-%m-%d}.tar.gz.enc'
    work = Path(portable.private_dir(out_dir, '.the-machine-export-'))
    files, tables, emptied = {}, {}, []
    try:
        sealed = work / name
        env = {**os.environ, PASSPHRASE_ENV: passphrase or code}
        try:
            proc = subprocess.Popen(OPENSSL + ['-salt', '-out', str(sealed), '-pass', f'env:{PASSPHRASE_ENV}'], env=env,
                                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            raise MoveError('openssl is needed for an export; install it and try again') from None
        try:
            with tarfile.open(fileobj=proc.stdin, mode='w|gz') as archive:
                _add_bytes(archive, 'README.txt', readme(manifest).encode())
                for kind, path, entry in items:
                    if kind not in ('db', 'openclaw-db') and message_seal.is_sealed_file(path):  # an email attachment kept sealed (mail_attachments.py)
                        data = _open_file(path, config)
                        _add_bytes(archive, entry, data)
                        files[entry] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                        continue
                    if kind not in ('db', 'openclaw-db'):
                        size = path.stat().st_size
                        files[entry] = {'bytes': size, 'sha256': _add_file(archive, path, entry)}
                        continue
                    copy = work / 'copy.sqlite'
                    try:
                        if kind == 'openclaw-db':
                            emptied += elsewhere.copy_db(path, copy, secrets_too)
                        else:
                            with closing(sqlite3.connect(path, timeout=30)) as source_db, closing(sqlite3.connect(copy)) as target:
                                source_db.backup(target)  # a consistent copy while the service keeps writing
                            _open_messages(copy, path)
                            tables.update(_tables(copy, str(Path(entry).relative_to('data'))))
                        files[entry] = {'bytes': copy.stat().st_size, 'sha256': _add_file(archive, copy, entry)}
                    finally:
                        portable.shred(copy)
                manifest.update(files=files, tables=tables, parts=parts(files, tables),
                                not_exported=not_exported(config, secrets_too, emptied))
                _add_bytes(archive, 'manifest.json', json.dumps(manifest, indent=2).encode())  # last: it has the checksums
            proc.stdin.close()
            if proc.wait(timeout=600):
                raise MoveError('Could not encrypt the export')
        except BaseException:
            proc.kill()
            proc.wait()
            try:
                proc.stdin.close()
            except OSError:  # openssl is gone: what was still buffered for it is dropped
                pass
            raise
        os.chmod(sealed, 0o600)
        target = out_dir / name
        os.replace(sealed, target)
    finally:
        portable.shred_tree(work)
    return target, ({**manifest, 'code': code} if code else manifest)


def _open_messages(copy, original):
    """An export holds message contents in the clear (it is the owner's), so it opens anywhere without their key."""
    key = message_seal.load_key(original)
    with closing(sqlite3.connect(copy, factory=message_seal.Connection)) as db:
        if not message_seal.is_protected(db):
            return
        if not key:
            raise MoveError('The messages in this database are sealed and their key is missing; nothing was exported.')
        message_seal.attach(db, message_seal.Sealer(key))
        with db:
            message_seal.unprotect(db)
        db.execute('VACUUM')


def _open_file(path, config):
    """A sealed email attachment goes into the export opened, like the messages."""
    key = message_seal.load_key(Path(config['database']).expanduser()) if config.get('database') else None
    if not key:
        raise MoveError(f'{path.name} is encrypted and the message key is missing; nothing was exported.')
    return message_seal.Sealer(key).open_bytes(path.read_bytes())


DECRYPTED_NAME = 'export.tar.gz'


def _decrypt(archive_path, folder, passphrase):
    """Opens an encrypted export with the passphrase as typed, then as an export code is written, into `folder` (the
    import's private temp folder) under a fixed name; returns that path. The cipher has no integrity check, so a wrong
    passphrase sometimes (about 1 in 256) "decrypts" to noise: only a result that starts like an archive counts, the
    rest is a wrong passphrase, not a damaged export."""
    folder = Path(folder).resolve()
    plain = folder / DECRYPTED_NAME  # never a name from the archive or the caller, so it can't point elsewhere
    for attempt in dict.fromkeys(p for p in (passphrase, _code_form(passphrase)) if p):
        try:
            _openssl(['-in', str(archive_path), '-out', str(plain)], attempt, decrypt=True)
        except MoveError:
            continue
        head = _head(plain, folder)
        if head[:2] == b'\x1f\x8b' or head == b'PK\x03\x04':  # gzip or zip
            return plain
    raise MoveError('Wrong export code or passphrase, or the file is damaged')


def _head(path, folder, size=4):
    """The first bytes of a file directly in `folder`, never through a symlink."""
    path = Path(path)
    if path.parent.resolve() != Path(folder).resolve() or path.name in ('', '.', '..'):
        raise MoveError('The decrypted export is not in the import folder')
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    except OSError:
        raise MoveError('The decrypted export could not be read') from None
    with os.fdopen(fd, 'rb') as file:
        return file.read(size)


def _openssl(args, passphrase, decrypt=False):
    env = {**os.environ, PASSPHRASE_ENV: passphrase}
    try:
        result = subprocess.run(OPENSSL + (['-d'] if decrypt else []) + args + ['-pass', f'env:{PASSPHRASE_ENV}'],
                                env=env, capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        raise MoveError('openssl is needed to open an export; install it and try again') from None
    if result.returncode:
        raise MoveError('Wrong export code or passphrase, or the file is damaged' if decrypt else 'Could not encrypt the export')


def readme(manifest):
    lines = ['The Machine: your export', '', f'Made {manifest["created_at"]}.',
             'This holds what The Machine knows and how it was set up. It is yours: keep it somewhere safe.', '',
             'To run it on your own computer:',
             '  1. Install The Machine: https://themachine.computer/help/self-hosted-setup',
             '     Stop its service before importing: assistant service stop',
             '  2. Put it back:  assistant import <this file>',
             '  3. Connect what the import lists, then check with:  assistant doctor', '']
    lines.append('Keys and tokens are included.' if manifest['includes_keys'] else
                 'Keys and tokens are not included; the import lists what to connect again.')
    lines += ['', 'Connect again after the import:'] + [f'  - {line}' for line in manifest['reconnect']]
    if manifest.get('left_out'):
        lines += ['', 'Left out, because a computer rebuilds them (installed packages, caches, git history, older copies):',
                  '  ' + left_out_text(manifest['left_out'])]
    return '\n'.join(lines) + '\n'


def left_out_text(left_out):
    """'node_modules 1.2 GB, .venvs 640 MB' for what an export skipped, biggest first."""
    def size(n):
        return f'{n / 1e9:.1f} GB' if n >= 1e9 else f'{n / 1e6:.0f} MB' if n >= 1e6 else f'{n / 1e3:.0f} KB'
    return ', '.join(f'{name} {size(n)}' for name, n in sorted(left_out.items(), key=lambda kv: -kv[1]))


def _outside(name, zipped=False):
    path = Path(name)
    # a zip may come from Windows: a backslash or a drive letter there points outside as well
    return path.is_absolute() or '..' in path.parts or (zipped and ('\\' in name or name[1:2] == ':'))


def _safe_extract(archive, target):
    if isinstance(archive, zipfile.ZipFile):
        for member in archive.infolist():
            kind = (member.external_attr >> 16) & 0o170000
            if _outside(member.filename, zipped=True) or kind not in (0, 0o100000, 0o040000):  # files and folders only, no links
                raise MoveError('This archive has entries outside its own folder; not importing it')
        archive.extractall(target)
        return
    for member in archive.getmembers():
        if _outside(member.name) or not (member.isfile() or member.isdir()):
            raise MoveError('This archive has entries outside its own folder; not importing it')
    archive.extractall(target, filter='data') if hasattr(tarfile, 'data_filter') else archive.extractall(target)


def _rebase(value, old, new):
    if isinstance(value, dict):
        return {k: _rebase(v, old, new) for k, v in value.items()}
    if isinstance(value, list):
        return [_rebase(v, old, new) for v in value]
    if isinstance(value, str) and old and (value == old or value.startswith(old.rstrip('/') + '/')):
        return new + value[len(old.rstrip('/')):]
    return value


def _atomic_copy(source, target, mode=0o600):
    """Replace a file through a unique sibling, never a shared or symlinked temporary name."""
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=target.name + '.import-', dir=target.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, 'wb') as handle, source.open('rb') as original:
            shutil.copyfileobj(original, handle)
            if hasattr(os, 'fchmod'):
                os.fchmod(handle.fileno(), mode)
            else:  # Windows: no POSIX modes; the folder's own access rules apply
                os.chmod(name, mode)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def _place(source, target, notes, mode=0o600):
    """Copy one file into place. A different file already there is kept, and the imported one sits next to it."""
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != source.read_bytes():
        target = target.with_name(target.name + '.from-export')
        notes.append(f'kept your {target.name[:-len(".from-export")]}; the exported one is {target}')
    _atomic_copy(source, target, mode)


@contextmanager
def offline_target(config_path):
    """Share the service's lock before touching any imported files. Never overlay an existing WAL."""
    data = Path(config_path).expanduser().parent
    data.mkdir(mode=0o700, parents=True, exist_ok=True)
    with (data / 'service.lock').open('a') as lock:
        try:
            portable.lock(lock, blocking=False)
        except BlockingIOError:
            raise MoveError('Stop personal-assistant first: assistant service stop. Then import again.') from None
        try:
            if any(data.rglob('*-wal')) or any(data.rglob('*-shm')):
                raise MoveError('The target database is still open (SQLite WAL files exist). Close its readers and stop '
                                'personal-assistant before importing; do not delete its WAL files.')
            yield
        finally:
            portable.unlock(lock)


def import_(archive_path, config_path, passphrase=None, workspace=None, openclaw_home=None, force=False, now=None, home=None,
            keep_hosted=False):
    with offline_target(config_path):
        return _import(archive_path, config_path, passphrase, workspace, openclaw_home, force, now, home, keep_hosted)


def finish(openclaw_home=None, now=None):
    """`assistant import --finish`: OpenClaw's conversations an import left waiting because OpenClaw ran."""
    now = now or dt.datetime.now(dt.timezone.utc)
    notes = []
    return {'restored': elsewhere.finish(_openclaw_home(openclaw_home), notes, f'{now:%Y%m%d-%H%M%S}'), 'notes': notes}


STAGED_HOURS = 24  # an export uploaded to be imported waits this long for the import, then it is shredded


def _staged_dir(config_path):
    data = Path(config_path).expanduser().parent
    return data.parent / f'.{data.name}.import-staged'


def stage(archive_path, config_path, passphrase=None, now=None):
    """Open and check an export now (a wrong passphrase or a damaged file says so at once) and keep it unpacked in a
    private folder until apply_staged() puts it in place with the service stopped (a hosted Machine's server does
    that: the dashboard can't stop itself). Returns its summary: {'created_at', 'source', 'parts', 'not_exported',
    'includes_keys', 'staged_at'}. A newer upload replaces an older one."""
    discard_staged(config_path)
    folder = _staged_dir(config_path)
    os.makedirs(folder.parent, mode=0o700, exist_ok=True)
    folder.mkdir(mode=0o700)
    try:
        _, manifest, _ = _unpack(Path(archive_path).expanduser(), folder, passphrase)
        summary = {'created_at': manifest.get('created_at'), 'source': manifest.get('source'), 'parts': manifest.get('parts') or {},
                   'not_exported': manifest.get('not_exported') or [], 'includes_keys': bool(manifest.get('includes_keys')),
                   'staged_at': (now or dt.datetime.now(dt.timezone.utc)).isoformat(timespec='seconds')}
        (folder / 'staged.json').write_text(json.dumps(summary))
        for name in os.listdir(folder):  # only the unpacked export and its summary stay
            if name not in ('export', 'staged.json'):
                portable.shred_tree(folder / name)
        return summary
    except BaseException:
        portable.shred_tree(folder)
        raise


def staged(config_path, now=None):
    """The summary of an export waiting to be imported (stage), or None. One older than STAGED_HOURS is shredded."""
    folder = _staged_dir(config_path)
    try:
        summary = json.loads((folder / 'staged.json').read_text())
    except (OSError, ValueError):
        return None
    at = dt.datetime.fromisoformat(summary.get('staged_at') or '1970-01-01T00:00:00+00:00')
    if (now or dt.datetime.now(dt.timezone.utc)) - at > dt.timedelta(hours=STAGED_HOURS):
        discard_staged(config_path)
        return None
    return summary


def discard_staged(config_path):
    portable.shred_tree(_staged_dir(config_path))


def apply_staged(config_path, workspace=None, openclaw_home=None, force=False, now=None, home=None, keep_hosted=False):
    """Put the staged export in place, with the service stopped. The staged folder is shredded afterwards."""
    folder = _staged_dir(config_path)
    if not staged(config_path, now):
        raise MoveError('There is no export waiting to be imported; upload it again')
    with offline_target(config_path):
        return _import(None, config_path, None, workspace, openclaw_home, force, now, home, keep_hosted, staged=folder)


def _unpack_staged(folder):
    unpacked = Path(folder) / 'export'
    manifest = json.loads((unpacked / 'manifest.json').read_text())
    _check(unpacked, manifest)
    return unpacked, manifest, json.loads((unpacked / 'config/config.json').read_text())


def _check(unpacked, manifest):
    """Every file the manifest lists is there with its checksum (format 2 on), before anything is replaced."""
    for entry, found in (manifest.get('files') or {}).items() if isinstance(manifest.get('files'), dict) else []:
        path = unpacked / entry
        if _outside(entry) or not path.is_file() or inventory.file_digest(path) != (found or {}).get('sha256'):
            raise MoveError('The export is damaged (a file does not match its checksum); nothing was imported.')


def _hold(config, manifest, data, now):
    """What waited to go out stays waiting for the owner (machine/export/hold.py). {what: count}."""
    held = {}
    main = Path(config.get('database') or data / 'events.sqlite').expanduser()
    since = manifest.get('created_at') or now.isoformat(timespec='seconds')
    if main.is_file():
        with closing(sqlite3.connect(main, timeout=30)) as db, db:
            held.update(moved.hold(db, now.isoformat(timespec='seconds'), since, bool(manifest.get('includes_keys')),
                                   manifest.get('source')))
    for path in data.rglob('telegram.sqlite'):
        with closing(sqlite3.connect(path, timeout=30)) as db, db:
            count = moved.hold_telegram(db, now.isoformat(timespec='seconds'))
        if count:
            held['telegram'] = held.get('telegram', 0) + count
    return held


def _unpack(archive_path, temp, passphrase):
    """Open, unpack and check an export into the private folder `temp`: (unpacked folder, manifest, its config).
    Nothing of this install is touched."""
    archive_path = Path(archive_path)
    plain = archive_path
    if archive_path.name.endswith('.enc'):
        if not passphrase:
            raise MoveError('This export is encrypted; give its export code or passphrase')
        plain = _decrypt(archive_path, temp, passphrase)
    unpacked = temp / 'export'
    try:
        with (zipfile.ZipFile(plain) if zipfile.is_zipfile(plain) else tarfile.open(plain, 'r:gz')) as archive:
            _safe_extract(archive, unpacked)
    except (tarfile.TarError, zipfile.BadZipFile, OSError):
        raise MoveError('This is not an export of The Machine, or it is damaged') from None
    try:
        manifest = json.loads((unpacked / 'manifest.json').read_text())
    except (OSError, ValueError):
        raise MoveError('This archive has no manifest; it is not an export of The Machine') from None
    if not isinstance(manifest, dict) or not isinstance(manifest.get('format', 0), int):
        raise MoveError('The export manifest is invalid; nothing was imported')
    if manifest.get('format', 0) > FORMAT:
        raise MoveError('This export is newer than this install; update The Machine first')
    _check(unpacked, manifest)
    try:
        original_config = json.loads((unpacked / 'config/config.json').read_text())
        if not isinstance(manifest, dict) or not isinstance(original_config, dict):
            raise ValueError('not an object')
        if not isinstance(original_config.get('accounts', []), list) or not isinstance(original_config.get('credentials', {}), dict):
            raise ValueError('invalid configuration')
    except (OSError, ValueError, TypeError):
        raise MoveError('The exported configuration is invalid; nothing was imported') from None
    # Validate every database before replacing any live file.
    for root in (unpacked / 'data', unpacked / 'secrets/data'):
        for path in root.rglob('*') if root.is_dir() else []:
            if path.suffix in ('.sqlite', '.db') and path.is_file():
                try:
                    with closing(sqlite3.connect(f'file:{path}?mode=ro', uri=True)) as check:
                        valid = check.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
                except sqlite3.Error:
                    valid = False
                if not valid:
                    raise MoveError('An exported database failed its integrity check; nothing was imported.')
    return unpacked, manifest, original_config


def _import(archive_path, config_path, passphrase=None, workspace=None, openclaw_home=None, force=False, now=None, home=None,
            keep_hosted=False, staged=None):
    """Put an export back on this computer. Returns {'restored', 'reconnect', 'notes', 'telegram', 'held', 'parts',
    'not_exported'}. keep_hosted: a hosted Machine takes an export of a computer, keeping its own hosted settings."""
    config_path = Path(config_path).expanduser()
    now, home_dir = now or dt.datetime.now(dt.timezone.utc), home
    if config_path.exists() and not force:
        try:
            existing = json.loads(config_path.read_text())
        except ValueError:
            existing = {}
        if existing.get('accounts'):
            raise MoveError(f'{config_path} already has connected sources; import into a fresh install, '
                            'or pass --force to replace it (the current data folder is kept as a copy first)')
    data = config_path.parent
    temp = staged or Path(portable.private_dir(data.parent, f'.{data.name}.import-'))  # what it unpacks: private, overwritten after
    try:
        if staged:
            unpacked, manifest, original_config = _unpack_staged(staged)
        else:
            unpacked, manifest, original_config = _unpack(archive_path, temp, passphrase)
        hosted_here = {}
        if keep_hosted and config_path.exists():
            try:
                hosted_here = json.loads(config_path.read_text())
            except ValueError:
                hosted_here = {}
        if force and data.exists() and any(data.iterdir()):
            keep = data.with_name(f'{data.name}.before-import-{now:%Y%m%d-%H%M%S}')
            shutil.copytree(data, keep)
        data.mkdir(mode=0o700, parents=True, exist_ok=True)
        restored, notes = [], []
        for folder, mode in (('data', 0o600), ('secrets/data', 0o600)):
            root = unpacked / folder
            for path in sorted(root.rglob('*')) if root.is_dir() else []:
                if path.is_file():
                    target = data / path.relative_to(root)
                    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                    _atomic_copy(path, target, mode)
                    restored.append(str(target))
        config = _rebase(original_config, manifest.get('data_dir'), str(data))
        config = _rebase(config, manifest.get('workspace_dir'), str(_workspace(workspace)))
        for key in HOSTED_KEYS:
            config.pop(key, None)
            if key in hosted_here:
                config[key] = hosted_here[key]
        for name in HOSTED_ONLY:
            (config.get('credentials') or {}).pop(name, None)
            if name in (hosted_here.get('credentials') or {}):
                config.setdefault('credentials', {})[name] = hosted_here['credentials'][name]
        if (config.get('enrichment') or {}).get('by') == 'hosting':
            config['enrichment'] = {'enabled': False}  # hosting did the look-ups; set up your own service to turn it on
            notes.append('organization look-ups were done by the hosting; the profiles found so far are kept')
        for account in config.get('accounts') or []:
            if account.get('transport') == 'broker' and account.get('service') in ('outlook', 'outlook_calendar'):
                account['transport'] = 'graph'  # Microsoft from here on goes through your own app registration
            elif account.get('transport') == 'broker':
                account['transport'] = 'gog'  # Google from here on goes through your own sign-in
        for name, path in list((config.get('credentials') or {}).items()):
            if not Path(path).expanduser().exists() and (unpacked / 'secrets/elsewhere' / Path(path).name).is_file():
                target = data / Path(path).name
                _place(unpacked / 'secrets/elsewhere' / Path(path).name, target, notes)
                config['credentials'][name] = str(target)
        # Always copy external identity keys into this installation, even on the same computer.
        # Keep their destination separate when a credential has the same basename.
        found = config.get('network_keys')
        if found:
            name = Path(found).name
            source = next((p for p in (unpacked / 'secrets/network' / name, unpacked / 'secrets/elsewhere' / name) if p.is_file()), None)
            if source:
                target = data / name
                credential_paths = {Path(p).expanduser().resolve() for p in (config.get('credentials') or {}).values()}
                if target.resolve() in credential_paths or (target.exists() and target.read_bytes() != source.read_bytes()):
                    target = data / 'network-identity' / name
                    number = 2
                    while target.resolve() in credential_paths or (target.exists() and target.read_bytes() != source.read_bytes()):
                        target = data / 'network-identity' / f'{name}.{number}'
                        number += 1
                _atomic_copy(source, target)
                config['network_keys'] = str(target)
                restored.append(str(target))
            elif not manifest.get('includes_keys') or not Path(found).expanduser().is_file():
                config.pop('network_keys')  # never reuse the exporting Machine's external path in a plain import
        if config_path.exists():
            shutil.copyfile(config_path, config_path.with_name(config_path.name + '.bak'))
        fd = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, 'w') as handle:
            handle.write(json.dumps(config, indent=2) + '\n')
        restored.append(str(config_path))
        space = _workspace(workspace)
        for folder in ('workspace', 'secrets/workspace'):
            for path in sorted((unpacked / folder).rglob('*')) if (unpacked / folder).is_dir() else []:
                if path.is_file():
                    target = space / path.relative_to(unpacked / folder)
                    _place(path, target, notes)
                    restored.append(str(target))
        for path in sorted((unpacked / 'connectors').rglob('*')) if (unpacked / 'connectors').is_dir() else []:
            if path.is_file():
                target = APP / path.relative_to(unpacked / 'connectors')
                _place(path, target, notes, mode=0o644)
                restored.append(str(target))
        home = _openclaw_home(openclaw_home)
        for path in sorted((unpacked / 'secrets/openclaw').rglob('*')) if (unpacked / 'secrets/openclaw').is_dir() else []:
            if path.is_file():
                target = home / path.relative_to(unpacked / 'secrets/openclaw')
                _place(path, target, notes)
                restored.append(str(target))
        stamp = f'{now:%Y%m%d-%H%M%S}'
        for folder in ('openclaw', 'home', 'agents-home'):
            for path in sorted((unpacked / folder).rglob('*')) if (unpacked / folder).is_dir() else []:
                if not path.is_file():
                    continue
                entry = str(path.relative_to(unpacked))
                target = elsewhere.target_for(entry, home, home_root(openclaw_home, home_dir), data, config)
                if target is None:
                    continue
                if folder == 'openclaw' and path.suffix == '.sqlite':
                    restored.append(str(elsewhere.restore_db(path, target, notes, stamp)))
                else:
                    _place(path, target, notes)
                    restored.append(str(target))
        held = _hold(config, manifest, data, now)
        return {'restored': restored, 'reconnect': manifest.get('reconnect') or [], 'notes': notes,
                'telegram': manifest.get('telegram'), 'held': held, 'parts': manifest.get('parts') or {},
                'not_exported': manifest.get('not_exported') or []}
    finally:
        portable.shred_tree(temp)

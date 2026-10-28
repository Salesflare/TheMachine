"""The pinned Telegram libraries for the Telegram chats mirror (telegram_mirror.py): Telethon and its pure-Python
dependencies, one exact file each from PyPI, checked against the sha256 kept in telegram-pin.json before anything is
unpacked. No pip, no virtual environment and no compiler: only the package folders are unpacked into a directory of
their own (`<data>/telegram-lib/<pin digest>`), which the mirror puts first on its path. A changed pin unpacks into a
new directory, so a half-written install is never used. telegram-requirements.txt lists the same files for
dependency scanners."""
import hashlib
import io
import json
import os
import shutil
import tarfile
import urllib.request
import zipfile
from pathlib import Path

PIN_FILE = Path(__file__).with_name('telegram-pin.json')
REQUIREMENTS = Path(__file__).with_name('telegram-requirements.txt')
DONE = '.complete'


def pin(path=PIN_FILE):
    return json.loads(Path(path).read_text())


def digest(data):
    """A short name for this exact set of files: a new pin installs next to the old one."""
    return hashlib.sha256(json.dumps([[p['name'], p['sha256']] for p in data['packages']]).encode()).hexdigest()[:16]


def version(data=None):
    data = data or pin()
    return next(p['version'] for p in data['packages'] if p['name'] == 'telethon')


def requirements(data):
    """The pin as telegram-requirements.txt lines (name==version --hash=sha256:...)."""
    return [f"{p['name']}=={p['version']} --hash=sha256:{p['sha256']}" for p in data['packages']]


def _fetch(url):
    if not url.startswith('https://files.pythonhosted.org/'):
        raise RuntimeError('a Telegram library must come from PyPI')
    with urllib.request.urlopen(url, timeout=300) as response:
        return response.read()


def _safe(name):
    parts = Path(name).parts
    return name and not Path(name).is_absolute() and '..' not in parts


def unpack(blob, package, target):
    """The package folders of one wheel or source archive into target, nothing else (no setup.py runs)."""
    wanted = tuple(package['packages'])
    if package['url'].endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            for name in archive.namelist():
                if _safe(name) and not name.endswith('/') and name.split('/')[0] in wanted:
                    out = target / name
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_bytes(archive.read(name))
        return
    with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
        for member in archive.getmembers():
            parts = member.name.split('/', 1)
            if member.isfile() and len(parts) == 2 and _safe(parts[1]) and parts[1].split('/')[0] in wanted:
                out = target / parts[1]
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(archive.extractfile(member).read())


def installed(base, data=None):
    """The library directory for this pin when it is fully unpacked, else None."""
    data = data or pin()
    path = Path(base) / digest(data)
    return path if (path / DONE).exists() else None


def install(base, data=None, fetch=_fetch):
    """Downloads every pinned file, checks each against its sha256 (all of them before anything is unpacked) and
    unpacks them into base/<digest>. Returns that directory. Raises RuntimeError on a mismatch."""
    data = data or pin()
    ready = installed(base, data)
    if ready:
        return ready
    blobs = []
    for package in data['packages']:
        blob = fetch(package['url'])
        if hashlib.sha256(blob).hexdigest() != package['sha256']:
            raise RuntimeError(f"the {package['name']} download did not match its pinned checksum")
        blobs.append((package, blob))
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    final = base / digest(data)
    temporary = base / (final.name + '.new')
    shutil.rmtree(temporary, ignore_errors=True)
    temporary.mkdir()
    for package, blob in blobs:
        unpack(blob, package, temporary)
    (temporary / 'NOTICE').write_text(''.join(f"{p['name']} {p['version']}: {p['license']}\n" for p in data['packages']))
    (temporary / DONE).write_text(digest(data) + '\n')
    shutil.rmtree(final, ignore_errors=True)
    os.replace(temporary, final)
    for old in base.iterdir():  # earlier pins: nothing uses them once this one is in place
        if old.is_dir() and old.name != final.name and not old.name.endswith('.new'):
            shutil.rmtree(old, ignore_errors=True)
    return final

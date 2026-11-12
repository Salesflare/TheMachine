"""The pinned signal-cli build for the Signal mirror (signal_mirror.py): one release of github.com/AsamK/signal-cli
(GPL-3.0-only, run as its own program, never linked into The Machine), checked against the sha256 in signal-pin.json
before anything is unpacked. Linux x86_64 gets the native build, which needs no Java. Other computers get the Java build,
which needs Java 25 or later on the PATH; without it, Signal says so plainly instead of half installing.

It unpacks into `<data>/signal-cli/<version>`; a new pin unpacks next to it, so a half-written install is never used."""
import hashlib
import io
import os
import platform
import re
import shutil
import subprocess
import tarfile
import urllib.request
import json
from pathlib import Path

PIN_FILE = Path(__file__).with_name('signal-pin.json')
DONE = '.complete'


def pin(path=PIN_FILE):
    return json.loads(Path(path).read_text())


def version(data=None):
    return (data or pin())['tag'].removeprefix('v')


def build_key(system=None, machine=None):
    """'linux_amd64' where the native build runs, else 'java'."""
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    return 'linux_amd64' if system == 'linux' and machine in ('x86_64', 'amd64') else 'java'


def java_version(run=subprocess.run):
    """The major version of the `java` on the PATH, or 0 when there is none."""
    java = shutil.which('java')
    if not java:
        return 0
    try:
        out = run([java, '-version'], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    found = re.search(r'version "(\d+)', (out.stderr or '') + (out.stdout or ''))
    return int(found[1]) if found else 0


def download_url(data, key):
    return f"https://github.com/{data['repository']}/releases/download/{data['tag']}/{data['builds'][key]['archive']}"


def _fetch(url):
    if not url.startswith('https://github.com/AsamK/signal-cli/releases/download/'):
        raise RuntimeError('signal-cli must come from its own GitHub releases')
    with urllib.request.urlopen(url, timeout=600) as response:
        return response.read()


def _safe(name):
    parts = Path(name).parts
    return bool(name) and not Path(name).is_absolute() and '..' not in parts


def binary_path(folder, data, key):
    build = data['builds'][key]
    name = build['binary'] + ('.bat' if key == 'java' and platform.system() == 'Windows' else '')
    return Path(folder) / name


def installed(base, data=None, key=None):
    """The signal-cli program for this pin when it is fully unpacked, else None."""
    data, key = data or pin(), key or build_key()
    folder = Path(base) / version(data)
    path = binary_path(folder, data, key)
    return path if (folder / DONE).exists() and path.exists() else None


def install(base, data=None, key=None, fetch=_fetch, java=java_version):
    """Downloads the pinned build for this computer, checks its sha256 and unpacks it into base/<version>. Returns the
    program's path. Raises RuntimeError when there is no build here, Java is missing or the download doesn't match."""
    data, key = data or pin(), key or build_key()
    ready = installed(base, data, key)
    if ready:
        return ready
    build = data['builds'].get(key)
    if not build:
        raise RuntimeError('there is no signal-cli build for this computer')
    if build.get('java') and java() < build['java']:
        raise RuntimeError(f"Signal needs Java {build['java']} or later on this computer")
    blob = fetch(download_url(data, key))
    if hashlib.sha256(blob).hexdigest() != build['sha256']:
        raise RuntimeError('the signal-cli download did not match its pinned checksum')
    base = Path(base)
    base.mkdir(parents=True, exist_ok=True)
    final = base / version(data)
    temporary = base / (final.name + '.new')
    shutil.rmtree(temporary, ignore_errors=True)
    temporary.mkdir()
    with tarfile.open(fileobj=io.BytesIO(blob)) as archive:
        for member in archive.getmembers():
            name = member.name.lstrip('./')
            if not member.isfile() or not _safe(name):
                continue
            out = temporary / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(archive.extractfile(member).read())
            if member.mode & 0o111:
                out.chmod(0o755)
    program = binary_path(temporary, data, key)
    if not program.exists():
        shutil.rmtree(temporary, ignore_errors=True)
        raise RuntimeError('the signal-cli download had no program in it')
    program.chmod(0o755)
    (temporary / 'NOTICE').write_text(f"signal-cli {version(data)}: {data['license']}, source: https://github.com/{data['repository']}/tree/{data['tag']}\n")
    (temporary / DONE).write_text(version(data) + '\n')
    shutil.rmtree(final, ignore_errors=True)
    os.replace(temporary, final)
    for old in base.iterdir():  # earlier pins: nothing uses them once this one is in place
        if old.is_dir() and old.name != final.name and not old.name.endswith('.new'):
            shutil.rmtree(old, ignore_errors=True)
    return binary_path(final, data, key)

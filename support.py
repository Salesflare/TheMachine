"""`assistant support-bundle`: one archive with what is needed to see why an install misbehaves, without secrets.

It holds versions, `assistant doctor`, the service status and recent log, the OpenClaw Gateway's status and recent
log, and config.json with every key, token, password and address taken out. Nothing is sent anywhere: the owner
looks at the file and passes it on.

`report()` is the same report for Help, Report a bug in the dashboard: the parts as lines and fields, scrubbed the
way the control plane scrubs a support report (cloud/support.py; a control plane test keeps LINE_SCRUB equal), so
what the owner sees before sending is exactly what arrives."""
import datetime as dt
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import service

ROOT = Path(__file__).resolve().parent
SENSITIVE_KEY = re.compile(r'token|secret|password|passphrase|key|credential|cookie|auth|session|owner|email|phone|host', re.I)
PATTERNS = [
    (re.compile(r'(?i)\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]{8,}'), r'\1 <redacted>'),
    (re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]*'), '<jwt>'),
    (re.compile(r'\b\d{6,12}:[A-Za-z0-9_-]{30,}\b'), '<bot-token>'),
    (re.compile(r'\b(sk|pk|rk)-[A-Za-z0-9_-]{16,}'), '<api-key>'),
    (re.compile(r'\b(gh[pousr]_[A-Za-z0-9]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|ya29\.[A-Za-z0-9_-]{20,}|1//[A-Za-z0-9_-]{20,})'), '<token>'),
    (re.compile(r'(?i)([?&](?:key|token|code|secret|sig|signature|access_token|k)=)[^&\s"\']+'), r'\1<redacted>'),
    (re.compile(r'(?i)(#k=)[^\s"\']+'), r'\1<redacted>'),
    (re.compile(r'\b[0-9a-f]{32,}\b', re.I), '<hex>'),
    (re.compile(r'(?<![/\w.-])[A-Za-z0-9+_-]{40,}={0,2}'), '<secret>'),
    (re.compile(r'[\w.+-]+@[\w-]+(\.[\w-]+)+'), '<email>'),
    (re.compile(r'(?i)((?:token|secret|password|passphrase|api[_-]?key)\s*[=:]\s*)\S+'), r'\1<redacted>'),
]


def scrub(text):
    """Text with anything that looks like a secret or an address taken out."""
    text = str(text or '')
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def scrub_config(value, key=''):
    """config.json with sensitive values replaced; structure and harmless settings kept."""
    if isinstance(value, dict):
        return {k: scrub_config(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub_config(v, key) for v in value]
    if isinstance(value, str) and (SENSITIVE_KEY.search(key) or '@' in value):
        return '<redacted>' if value else ''
    if isinstance(value, (int, float)) and SENSITIVE_KEY.search(key) and not isinstance(value, bool):
        return '<redacted>'
    return scrub(value) if isinstance(value, str) else value


# The control plane's scrub of a support report (cloud/support.py SCRUB, the same in its agent): keys and tokens,
# quoted text, links' paths, addresses, phone numbers, what a message says and who it is from or to.
_CONTENT_KEYS = (r'text|body|content|message|msg|prompt|preview|snippet|subject|caption|title|query|reply|name|first_?name|'
                 r'last_?name|display_?name|full_?name|from|to|sender|recipient|chat|chat_?title|contact|user|username|author|cc|bcc|'
                 r'session_?(?:id|key)|peer(?:_?id)?|chat_?id|sender_?id|user_?id|account_?id|thread_?id|conversation_?id')
_TALK = r'inbound|outbound|incoming|reply|replied|message|messages|msg|dm|email|mail|said|wrote'
_UNTIL_KEY = r'(?:(?!\s[A-Za-z_]\w*=|\s[A-Z]\w*(?:Error|Exception)\b).)*'


def _quoted(found):
    kind = re.match(r'\s*([A-Z][A-Za-z0-9]*(?:Error|Exception|Failure|Timeout))\b', found[0][1:-1])
    return f'"{kind[1]}: …"' if kind else '"…"'


def _long(found):
    parts = re.split(r'[-/._=+]', found[0])
    return '[redacted]' if any(len(p) >= 24 or (len(p) >= 16 and re.search(r'\d', p) and re.search(r'[A-Za-z]', p)) for p in parts) else found[0]


LINE_SCRUB = ((re.compile(r'\b(?:sk|pk|rk|ghp|gho|ghs|ghu|github_pat|glpat|xox[abprs]|ya29|AIza)[-_.][A-Za-z0-9_\-.]{8,}'), '[redacted]'),
              (re.compile(r'(?i)\b(bearer|token|secret|password|passwd|api[_-]?key|authorization|cookie|key)\b(["\']?\s*[:=]\s*|\s+)\S+'), r'\1\2[redacted]'),
              (re.compile(r'"[^"]*"|\'[^\']*\'|“[^”]*”'), _quoted), (re.compile(r'https?://([^/\s?#]+)\S*'), r'https://\1/…'),
              (re.compile(r'[\w.+-]+@[\w-]+(\.[\w-]+)+'), '[email]'),
              (re.compile(rf'(?i)\b({_CONTENT_KEYS})=' + _UNTIL_KEY), r'\1=…'),
              (re.compile(rf'(?i)\b({_TALK})\b((?:\s+[\w-]+){{0,2}}?)\s+(from|to|by)\b' + _UNTIL_KEY), r'\1\2 \3 …'),
              (re.compile(r'(?<![\w.-])(?!\d{4}-\d\d-\d\d)\+?\d[\d ()-]{7,}\d(?![\w.:/-])'), '[number]'),
              (re.compile(r'[A-Za-z0-9_\-+/=.]{24,}'), _long))
TROUBLE = re.compile(r'warn|error|fail|exception|traceback|critical|fatal|denied|refused|timed? ?out|oom|killed|abort|drain|'
                     r'restart|reload|sigterm|sigkill|low memory', re.I)
CONTENT_KEY = re.compile(rf'(?i)^(?:{_CONTENT_KEYS}|signature|voice|notes?|about|bio|address|label)$')
# Settings that name a person or what the owner keeps out (an admin's name, a handle or login, exclusion terms): no value
# under these either. The same in cloud/support.py; a test there keeps them equal.
PERSONAL_KEY = re.compile(r'(?i)^(?:\w+_name|handle|login|primary|\w*emails|senders|excluded\w*|exclude_\w+)$')
REPORT_LINES = {'service-log': 200, 'openclaw-log': 120, 'doctor': 80, 'versions': 30}
REPORT_CHARS = 48000  # all lines together, as the control plane caps a report's logs


def scrub_line(line):
    """One line as the control plane keeps it in a support report."""
    line = str(line or '')
    for pattern, replace in LINE_SCRUB:
        line = pattern.sub(replace, line)
    return line[:240]


def scrub_value(value):
    """Every string in a structure scrubbed by line (cloud/support.py scrub_value)."""
    if isinstance(value, str):
        return scrub_line(value)
    if isinstance(value, dict):
        return {scrub_line(k): scrub_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [scrub_value(v) for v in value]
    return value


def _settings(value, key=''):
    """config.json as a report holds it: scrub_config, and no value under a key that holds what someone wrote."""
    if isinstance(value, dict):
        return {k: _settings(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [_settings(v, key) for v in value][:40]
    if isinstance(value, str) and value and (CONTENT_KEY.match(key or '') or PERSONAL_KEY.match(key or '')):
        return '<redacted>'
    return value


HOME = re.compile(r'(?<![\w.])(/home/|/Users/|[A-Za-z]:\\Users\\)[^/\\\s"\']+')  # a home folder is often a person's name


def _unhomed(value):
    if isinstance(value, str):
        return HOME.sub(lambda m: m[1] + '…', value)
    if isinstance(value, dict):
        return {k: _unhomed(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_unhomed(v) for v in value]
    return value


def report(config_path, doctor=None, lines=1000):
    """The support report for Report a bug: {'parts': {name: [lines]}, 'settings': {...}}, scrubbed and capped.
    The same sources as the bundle; only warnings, errors and lifecycle lines of the service's log."""
    try:
        config = json.loads(Path(config_path).expanduser().read_text())
    except (OSError, ValueError):
        config = {}
    raw = {'versions': versions(config).splitlines(),
           'service-status': (service.status_text() if service.available() else f'no service manager ({service.manager()})').splitlines()[:20]}
    if service.available():
        raw['service-log'] = [line for line in (service.logs(lines=lines) or '').splitlines() if TROUBLE.search(line)]
    if doctor:
        try:
            raw['doctor'] = [f'{mark} {text}' + (f' (fix: {fix})' if fix else '') for mark, text, fix in doctor(config_path)]
        except Exception as error:  # the report is most needed when things are broken
            raw['doctor'] = [f'doctor failed: {type(error).__name__}']
    openclaw = config.get('openclaw') or shutil.which('openclaw')
    if openclaw:
        raw['openclaw-log'] = [line for line in _run([openclaw, 'logs', '--limit', '1500', '--plain'], 60).splitlines()
                               if re.search(r'\s(warn|error|fatal)\s', line) and '[agent:' not in line]
    parts = {name: [scrub_line(_unhomed(scrub(line))) for line in items if str(line).strip()][-REPORT_LINES.get(name, 40):] for name, items in raw.items()}
    while sum(len(line) for items in parts.values() for line in items) > REPORT_CHARS:
        max(parts.values(), key=lambda items: sum(map(len, items))).pop(0)
    return {'parts': parts, 'settings': scrub_value(_unhomed(_settings(scrub_config(config))))}


def _run(args, timeout=60):
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout, errors='replace')
        return (result.stdout + ('\n' + result.stderr if result.stderr.strip() else '')).strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        return f'({" ".join(map(str, args[:3]))}: {error})'


def versions(config):
    lines = [f'when: {dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}',
             f'os: {platform.platform()}', f'wsl: {service.wsl()}', f'service manager: {service.manager()}',
             f'python: {sys.version.split()[0]} ({sys.executable})', f'app: {ROOT}',
             'commit: ' + _run(['git', '-C', str(ROOT), 'log', '-1', '--format=%h %cd', '--date=short'])]
    for name in ('node', 'openclaw', 'gog', 'tailscale', 'wacli'):
        binary = (config or {}).get(name) or shutil.which(name)
        lines.append(f'{name}: ' + (_run([binary, '--version'], 30).splitlines() or ['?'])[0] if binary else f'{name}: not found')
    return '\n'.join(lines)


def windows_desktop():
    """Inside WSL: the Windows Desktop folder, so the bundle is easy to find and attach."""
    if not service.wsl() or not shutil.which('cmd.exe') or not shutil.which('wslpath'):
        return None
    profile = _run(['cmd.exe', '/c', 'echo %USERPROFILE%'], 20).splitlines()
    if not profile:
        return None
    folder = Path(_run(['wslpath', '-u', profile[-1].strip()], 20).strip()) / 'Desktop'
    return folder if folder.is_dir() else None


def bundle(config_path, out=None, doctor=None, lines=1000):
    """Write the archive and return its path."""
    try:
        config = json.loads(Path(config_path).expanduser().read_text())
    except (OSError, ValueError):
        config = {}
    parts = {'versions.txt': versions(config),
             'service-status.txt': service.status_text() if service.available() else f'no service manager ({service.manager()})',
             'service-log.txt': service.logs(lines=lines) if service.available() else ''}
    if doctor:
        try:
            parts['doctor.txt'] = '\n'.join(f'{mark} {text}' + (f'\n    fix: {fix}' if fix else '') for mark, text, fix in doctor(config_path))
        except Exception as error:  # the bundle is most needed when things are broken
            parts['doctor.txt'] = f'doctor failed: {type(error).__name__}: {error}'
    openclaw = config.get('openclaw') or shutil.which('openclaw')
    if openclaw:
        parts['openclaw-gateway.txt'] = _run([openclaw, 'gateway', 'status'], 60)
        # Warnings and errors only, shortened: info lines can carry what the agent said.
        parts['openclaw-log.txt'] = '\n'.join(line[:240] for line in _run([openclaw, 'logs', '--limit', '1500', '--plain'], 60).splitlines()
                                              if re.search(r'\s(warn|error|fatal)\s', line) and '[agent:' not in line)
    parts['config.json'] = json.dumps(scrub_config(config), indent=2)
    stamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
    folder = Path(out).expanduser() if out else (windows_desktop() or Path.cwd())
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'the-machine-logs-{stamp}.tar.gz'
    with tarfile.open(path, 'w:gz') as archive:
        for name, text in parts.items():
            data = scrub(text).encode() if name != 'config.json' else text.encode()
            info = tarfile.TarInfo(f'the-machine-logs-{stamp}/{name}')
            info.size, info.mtime, info.mode = len(data), int(dt.datetime.now().timestamp()), 0o600
            archive.addfile(info, io.BytesIO(data))
    os.chmod(path, 0o600)
    return path

"""Serving the dashboard (refactor PR 19): its hosts and origin, the CSRF token and cache scope in the page, the page
itself, which answers are compressed and how (brotli, zstd or gzip), ETags, and the status it reports. Moved out of
assistant.py as is."""
import gzip
import hashlib
import hmac
import json
import re
import subprocess
import time

import dashboard_parts
import locale_prefs
from machine.config import ROOT
import portable


_DASHBOARD_VERSION = {}


def dashboard_version():
    """A short hash of the dashboard page being served (dashboard.html with its parts, dashboard_parts): an open page
    that runs another one reloads itself."""
    try:
        mtime = tuple(path.stat().st_mtime_ns for path in dashboard_parts.files(ROOT))
    except OSError:
        return ''
    if _DASHBOARD_VERSION.get('mtime') != mtime:
        page = dashboard_parts.assemble(ROOT).encode('utf-8')
        _DASHBOARD_VERSION.update(mtime=mtime, version=hashlib.sha256(page).hexdigest()[:12])
    return _DASHBOARD_VERSION['version']


def dashboard_hosts(config):
    """The dashboard's own origin (`dashboard_host`, used for new links) plus older addresses that
    keep working for existing Telegram links. Port 8443 since 2026-10-13: the OpenClaw web app
    installed on the phone claims every path on :443, so the assistant needs its own origin."""
    return [config['dashboard_host'], *config.get('dashboard_aliases', [])]


_WHOIS = {}


def tailnet_login(ip):
    """Tailscale login of the tailnet peer at `ip`, for requests Caddy forwards (a custom
    domain such as assistant.example.com): Tailscale Serve can't serve a custom domain, so Caddy holds :443 and passes the
    client address in X-Tailnet-Client instead of Tailscale's own identity headers. Cached a minute."""
    hit = _WHOIS.get(ip)
    if hit and hit[0] > time.monotonic():
        return hit[1]
    try:
        out = subprocess.run([portable.tailscale() or 'tailscale', 'whois', '--json', ip], capture_output=True, text=True, timeout=5)
        login = json.loads(out.stdout).get('UserProfile', {}).get('LoginName', '') if out.returncode == 0 else ''
    except (OSError, subprocess.TimeoutExpired, ValueError):
        login = ''
    _WHOIS[ip] = (time.monotonic() + 60, login)
    return login


def dashboard_csrf(token, owner):
    """The dashboard's CSRF token: the same for every page of this owner on this Machine."""
    return hmac.new(token.encode(), owner.encode(), hashlib.sha256).hexdigest()


def dashboard_cache_scope(token, owner):
    """Whose last data the dashboard may keep on a device (encrypted, see docs/architecture.md): another owner or a new
    Machine token is another scope, and the device drops what it kept for the old one. It says nothing about either."""
    return hmac.new(token.encode(), b'dashboard-cache\0' + owner.encode(), hashlib.sha256).hexdigest()[:32]


def dashboard_page(token, owner, base):
    """dashboard.html as served (with its parts, dashboard_parts): the release, the base path and the device cache's
    scope filled in. Never the CSRF token: the page asks api/session for it (as a page opened from the app's on-device
    copy always did), so the page holds no secret and can go compressed (compressible below)."""
    return _filled(dashboard_parts.assemble(ROOT), token, owner, base)


def _filled(source, token, owner, base):
    return (source.replace('__CSRF__', '').replace('__UI_VERSION__', dashboard_version()).replace('__BASE__', base)
            .replace('__CACHE_SCOPE__', dashboard_cache_scope(token, owner)))


SCRIPT_NAME = re.compile(r'/(app|lazy-[a-z]+)-[0-9a-f]{16}\.js')  # the main script, a LAZY group's file
SCRIPT_CACHE = 'private, max-age=31536000, immutable'  # its name changes with every change to it
BRAND_CACHE = 'private, max-age=86400'  # brand images and typefaces: same names across releases, so a day, then a 304


def dashboard_script(page):
    """(page, name, script): the dashboard page with its main script (the last one, 1.6 MB) as a file of its own, named
    by its contents. A browser keeps that file and its compiled code between starts, where a script in the page is
    parsed and compiled again on every start. The script holds nothing per owner or request (those are in the page's
    first lines), so the file is the same for every page of a release. (page, None, None) when there is none."""
    start, end = page.rfind('<script>\n'), page.rfind('</script></html>')
    if start < 0 or end < start or page[end:].strip() != '</script></html>':
        return page, None, None
    script = page[start + len('<script>\n'):end]
    name = 'app-' + hashlib.sha256(script.encode()).hexdigest()[:16] + '.js'
    return page[:start] + f'<script src="{name}"></script></html>' + page[end + len('</script></html>'):], name, script


def dashboard_files(token, owner, base):
    """(page, {name: script}): the dashboard as a browser gets it. The page (dashboard_page) without the parts that load
    when first needed (dashboard_parts.LAZY): each group of them is a file of its own, lazy-<group>-<hash>.js, named by
    its contents and named in the page's self.LAZY_FILES, just before its main script, which is a file of its own too
    (dashboard_script). Like the main script, a group's file holds nothing per owner or request.
    Made once per release (the source files' mtimes, as dashboard_version) and page: every script a page asks for came
    here, and assembling and hashing it all again took 40-90 ms each, with a fresh page's parts asked for together."""
    try:
        mtime = tuple(path.stat().st_mtime_ns for path in dashboard_parts.files(ROOT))
    except OSError:
        mtime = None
    key = (token, owner, base)
    if mtime is not None and _DASHBOARD_FILES.get('mtime') == mtime and key in _DASHBOARD_FILES['made']:
        return _DASHBOARD_FILES['made'][key]
    made = _dashboard_files(token, owner, base)
    if mtime is not None:
        if _DASHBOARD_FILES.get('mtime') != mtime or len(_DASHBOARD_FILES['made']) >= 8:
            _DASHBOARD_FILES.update(mtime=mtime, made={})
        _DASHBOARD_FILES['made'][key] = made
    return made


_DASHBOARD_FILES = {}


def _dashboard_files(token, owner, base):
    source, lazy = dashboard_parts.assemble_split(ROOT)
    files = {f'lazy-{group}-' + hashlib.sha256(script.encode()).hexdigest()[:16] + '.js': script
             for group, script in lazy.items() if script}
    page, name, script = dashboard_script(_filled(source, token, owner, base))
    if not name:
        return page, files
    files[name] = script
    named = json.dumps({name.rsplit('-', 1)[0][len('lazy-'):]: name for name in files if name.startswith('lazy-')})
    tag = f'<script src="{name}"></script></html>'
    return page.replace(tag, f'<script>self.LAZY_FILES={named}</script>' + tag), files


def served_file(files, name):
    """(name, script): the file a page asks for by name among dashboard_files. A name from another release gets this
    release's file of the same kind (the main script, or the same group's), under its own name, so it isn't kept under
    the old one: the page then sees the new release and loads it. (None, None) when there is none."""
    if name in files:
        return name, files[name]
    kind = name.rsplit('-', 1)[0]
    return next(((other, script) for other, script in files.items() if other.rsplit('-', 1)[0] == kind), (None, None))


# Compressed answers for the dashboard (the page is about 1 MB and api/status close to that; on a phone over 4G that
# was most of the start). Only the answers in COMPRESSIBLE, and only because none of them holds a secret: compressing a
# secret next to text an outsider can influence (an email's words in a card) would let them guess the secret from the
# compressed size (BREACH). The CSRF token is only in api/session, which is never compressed, nor is anything else not
# listed here (file downloads, the browser view, streams). Brotli when the module is there, else zstd (Python 3.14),
# else gzip; the client's Accept-Encoding decides, q=0 refuses one.
COMPRESSIBLE = frozenset({'/', '/sw.js', '/manifest.webmanifest', *(f'/i18n/{code}.json' for code in locale_prefs.LANGUAGES), '/api/status', '/api/events', '/api/calendar', '/api/meeting-notes', '/api/graph',
                          '/api/graph/list', '/api/graph/timeline', '/api/cards/done', '/api/promise'})


COMPRESS_MIN = 1024  # smaller answers fit a packet or two anyway
try:
    import brotli as _brotli
except ImportError:
    _brotli = None
try:
    from compression import zstd as _zstd
except ImportError:
    _zstd = None


def content_codings(accept):
    """The codings this server can send, best first, that the client's Accept-Encoding takes (q > 0)."""
    taken, star = {}, None
    for part in str(accept or '').split(','):
        name, _, params = part.strip().partition(';')
        name, q = name.strip().lower(), 1.0
        for param in params.split(';'):
            key, _, value = param.strip().partition('=')
            if key.strip().lower() == 'q':
                try:
                    q = float(value)
                except ValueError:
                    q = 0.0
        if name == '*':
            star = q
        elif name:
            taken[name] = q
    own = (['br'] if _brotli else []) + (['zstd'] if _zstd else []) + ['gzip']
    return [c for c in own if taken.get(c, star or 0) > 0]


def compress_body(data, coding, best=False):
    """`data` in `coding`; `best` for answers kept and sent many times (the page), else fast enough for every request."""
    if coding == 'br':
        return _brotli.compress(data, quality=9 if best else 5)
    if coding == 'zstd':
        return _zstd.compress(data, 12 if best else 3)
    return gzip.compress(data, 9 if best else 6, mtime=0)


def etag_base(tag):
    """An ETag without the coding it was sent in ("abc-gzip" is "abc"): the page is the same, only its transfer differs."""
    tag = tag.strip()
    tag = tag[2:] if tag.startswith('W/') else tag
    return re.sub(r'-(br|zstd|gzip)"$', '"', tag)


def etag_matches(if_none_match, etag):
    return any(etag_base(t) == etag for t in str(if_none_match or '').split(',') if t.strip())


REVIEWS_SHOWN = 20  # of the status' 100 (mostly their summaries: 88 KB on a busy Machine)


def dashboard_status(status):
    """api/status as the dashboard needs it: without what it never reads. A finished review's signal list (only its
    count shows, and checked_count has it), its session names, a card's dedupe key and saved pre-close state, a
    delivery's message bookkeeping (its row shows status, to-do, time and error), a card's next_action when next_actions
    has it (the page reads next_actions first), and of a connector's sync state (a Slack one is tens of KB of cursors)
    all but what Connections reads, and the newest reviews only. The status action itself (CLI, plugin) keeps everything; copies, never its rows."""
    def without(rows, keys, when=lambda row: True):
        return [{k: v for k, v in row.items() if k not in keys} if isinstance(row, dict) and when(row) else row for row in rows or []]
    status, drop = dict(status), {'analyses': {'owner_session', 'owner_run'}, 'suggestions': {'dedupe_key', 'closed_state'},
                                  'deliveries': {'previous_message_ids', 'notification_message_id', 'last_notified_at',
                                                 'edit_retry_at', 'edit_failures', 'message_id', 'send_kind', 'reminder'}}
    for name, keys in drop.items():
        if isinstance(status.get(name), list):
            status[name] = without(status[name], keys)
    if isinstance(status.get('analyses'), list):  # the newest REVIEWS_SHOWN: Connections' review history shows 3, then 10 more
        status['analyses'] = without(status['analyses'][:REVIEWS_SHOWN], {'items'}, lambda r: r.get('status') == 'complete' and r.get('checked_count') is not None)
    if isinstance(status.get('suggestions'), list):
        status['suggestions'] = without(status['suggestions'], {'next_action'}, lambda r: 'next_actions' in r)
    if isinstance(status.get('connectors'), list):
        status['connectors'] = [{**c, 'state': sync_state_shown(c['state'])} if isinstance(c, dict) and c.get('state') else c for c in status['connectors']]
    return status


SYNC_STATE_SHOWN = ('mode', 'resync_reason', 'watermark', 'transport', 'reconciliation_error')  # connections-cards.js syncPlain, phone


def sync_state_shown(state):
    """A connector's sync state (checkpoints.state, JSON text) with only the keys the Connections page reads."""
    try:
        state = json.loads(state) if isinstance(state, str) else state
    except ValueError:
        return '{}'
    return json.dumps({k: state[k] for k in SYNC_STATE_SHOWN if k in state} if isinstance(state, dict) else {}, separators=(',', ':'))


def dashboard_base(config, host):
    """The dashboard's own host serves it at `dashboard_path` (for example / on a custom
    domain); ts.net aliases keep it under `dashboard_alias_path` (/assistant/)."""
    return config.get('dashboard_path', '/') if host == config.get('dashboard_host') else config.get('dashboard_alias_path', '/assistant/')

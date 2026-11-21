"""Bringing saved sign-ins in from a password manager, into the store the sign-in dialog uses (browser_login.LoginStore).

Three ways, all started by the owner on the dashboard and all ending in a review where they tick which to keep:

- An export file (CSV) from 1Password, LastPass, Bitwarden or Chrome (Edge, Brave and Firefox write the same columns),
  or Bitwarden's unencrypted JSON. parse() reads it in memory; nothing of it is written anywhere until the owner keeps
  some.
- The password manager's own export page in the Machine's browser (export_open: LastPass's vault, Bitwarden's web
  vault, Google Password Manager). The owner signs in there; then a fixed script (login_export_guide, never the
  model) clicks on to the export step, and what proves it's them stays theirs: the sign-in, 2FA, the master password
  asked again, an email to confirm. Nothing is typed for them and no field is read. The browser saves the download
  into a private folder of its own for this one export, and the file is read and deleted from disk as soon as it is
  whole (it holds every password in plain text).
- 1Password's `op` or LastPass's `lpass` command-line tool, when it is installed on this computer and the owner has
  signed in to it themselves. The list shows names, addresses and usernames only; a password is read from the tool
  only for the ones the owner keeps, at that moment. Nothing here signs in to a password manager, starts one's sign-in
  or asks for a master password: a tool that is signed out says so, and the tools run with no terminal and pinentry
  turned off, so they can't ask either.

What a review holds stays in this process's memory for ten minutes at most (PENDING), keyed by a random token, and goes
as soon as it is kept or dropped. Passwords never reach the dashboard (rows carry none), a log, the model or an error:
errors are fixed sentences that quote nothing from the file or the tool. Each kept sign-in is bound to the exact origin
of its address (browser_login.origin), so it only ever goes into that site's own page.
"""
from __future__ import annotations

import csv
import io
import json
import logging
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import threading
import time

import browser_login
import login_export_guide
from machine.owner_error import OwnerError

LOG = logging.getLogger('personal-assistant')
MAX_BYTES = 5 * 1024 * 1024
MAX_ROWS = 5000
KEEP_SECONDS = 600
TOOL_SECONDS = 30
MANAGERS = {'1password': '1Password', 'lastpass': 'LastPass', 'bitwarden': 'Bitwarden', 'chrome': 'Chrome', 'csv': 'CSV'}

_pending = {}
_pending_lock = threading.Lock()


# Export files

def kind_of(header):
    """Which password manager wrote a CSV, by its header row; None when it isn't one we read."""
    names = {str(h or '').strip().lower() for h in header}
    if {'login_uri', 'login_username', 'login_password'} <= names:
        return 'bitwarden'
    if {'title', 'url', 'username', 'password'} <= names and names & {'otpauth', 'archived', 'favorite'}:
        return '1password'
    if {'title', 'website', 'username', 'password'} <= names:
        return '1password'  # 1Password 7
    if {'url', 'username', 'password'} <= names and names & {'grouping', 'extra'}:
        return 'lastpass'
    if {'name', 'url', 'username', 'password'} <= names:
        return 'chrome'
    if {'url', 'username', 'password'} <= names:
        return 'csv'  # Firefox and others with the same three columns
    return None


def _cell(row, *names):
    for name in names:
        value = row.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ''


def _addresses(value):
    """A cell's addresses: Bitwarden puts several in one, comma or line separated."""
    return [a.strip() for a in value.replace('\n', ',').split(',') if a.strip()]


def parse(text):
    """An export file's sign-ins: (kind, [{key, title, origin, username, password}], skipped). Rows with no web
    address, a non-https address (other than this computer), no password or a note instead of a login are skipped and
    only counted. Raises OwnerError, quoting nothing from the file."""
    if not isinstance(text, str) or not text.strip():
        raise OwnerError('That file is empty')
    if len(text.encode('utf-8', 'ignore')) > MAX_BYTES:
        raise OwnerError('That file is too big (5 MB at most)')
    text = text.lstrip('﻿')
    if text.lstrip().startswith('{'):
        return 'bitwarden', *_collect(_bitwarden_json(text))
    try:
        reader = csv.DictReader(io.StringIO(text, newline=''))
        kind = kind_of(reader.fieldnames or [])
        if not kind:
            raise OwnerError('That isn’t a password export this can read. Export a CSV from 1Password, LastPass, Bitwarden or Chrome.')
        return kind, *_collect(_csv_entries(reader, kind))
    except csv.Error:
        raise OwnerError('That file couldn’t be read as a CSV') from None


def _csv_entries(reader, kind):
    """(title, addresses, username, password) per row; None for a row that isn't a login."""
    lower = {h: str(h or '').strip().lower() for h in reader.fieldnames or []}
    for raw in reader:
        row = {lower.get(k, k): v for k, v in raw.items() if isinstance(k, str)}
        if kind == 'bitwarden' and _cell(row, 'type') not in ('', 'login'):
            yield None
            continue
        address = {'bitwarden': _cell(row, 'login_uri'), '1password': _cell(row, 'url', 'website')}.get(kind) or _cell(row, 'url')
        username = _cell(row, 'login_username') if kind == 'bitwarden' else _cell(row, 'username')
        password = (row.get('login_password') if kind == 'bitwarden' else row.get('password')) or ''
        yield _cell(row, 'name', 'title'), _addresses(address), username, password


def _bitwarden_json(text):
    """Bitwarden's .json export, unencrypted: its logins (type 1). An encrypted one says so."""
    try:
        doc = json.loads(text)
    except ValueError:
        doc = None
    if not isinstance(doc, dict) or not isinstance(doc.get('items'), list):
        raise OwnerError('That isn’t a password export this can read. Export a CSV from 1Password, LastPass, Bitwarden or Chrome.')
    if doc.get('encrypted') or doc.get('passwordProtected'):
        raise OwnerError('That export is encrypted. Export it again as .csv or .json, without a file password.')
    for item in doc['items']:
        login = item.get('login') if isinstance(item, dict) and item.get('type') == 1 else None
        if not isinstance(login, dict):
            yield None
            continue
        uris = [str(u.get('uri') or '') for u in login.get('uris') or [] if isinstance(u, dict)]
        yield str(item.get('name') or '').strip(), [u.strip() for u in uris if u.strip()], \
            str(login.get('username') or '').strip(), str(login.get('password') or '')


def _collect(entries):
    """([{key, title, origin, username, password}], skipped) from (title, addresses, username, password) entries."""
    skipped, seen = 0, {}
    for count, entry in enumerate(entries):
        if count >= MAX_ROWS:
            raise OwnerError('That file has too many rows (5,000 at most)')
        if entry is None:
            skipped += 1
            continue
        title, addresses, username, password = entry
        origins = [o for o in (browser_login.origin(a) for a in addresses) if o and _fillable(o)]
        if not origins or not password:
            skipped += 1
            continue
        for bound in dict.fromkeys(origins):
            seen[(bound, username, password)] = {'title': title[:80], 'origin': bound, 'username': username[:1000], 'password': password[:1000]}
    return [{'key': secrets.token_hex(6), **row} for row in seen.values()], skipped


def _fillable(bound):
    """An origin the sign-in dialog would fill: https, or http on this computer."""
    if bound.startswith('https://'):
        return True
    host = bound.split('://', 1)[1].rsplit(':', 1)[0].strip('[]')
    return host in browser_login.LOOPBACK


# Password managers' command-line tools

def _env():
    # No terminal to ask on and no pinentry: a tool that wants its master password fails instead of asking for it.
    return {**os.environ, 'LPASS_DISABLE_PINENTRY': '1', 'LPASS_ASKPASS': shutil.which('false') or '/bin/false'}


def _run(args, timeout=TOOL_SECONDS):
    """Runs a tool with no input, returning (exit code, stdout). Its output is never logged or quoted."""
    try:
        done = subprocess.run(args, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout, env=_env())
    except (OSError, subprocess.SubprocessError):
        return 1, ''
    return done.returncode, done.stdout


TOOLS = {'1password': 'op', 'lastpass': 'lpass'}


def tool_state(manager):
    """'missing' (not installed here), 'signed_out' (installed, not signed in: the owner signs in to it themselves)
    or 'ready'."""
    name = TOOLS.get(manager)
    if not name:
        raise OwnerError('Which password manager?')
    path = shutil.which(name)
    if not path:
        return 'missing'
    check = [path, 'whoami', '--format', 'json'] if manager == '1password' else [path, 'status', '--quiet']
    code, _ = _run(check, timeout=15)
    return 'ready' if code == 0 else 'signed_out'


def tool_list(manager):
    """The tool's logins with a web address, [{key, title, origin, username}], no password. Raises OwnerError when
    the tool is missing or signed out."""
    state = tool_state(manager)
    if state != 'ready':
        raise OwnerError(TOOL_SAYS[manager][state])
    path = shutil.which(TOOLS[manager])
    rows = []
    if manager == '1password':
        code, out = _run([path, 'item', 'list', '--categories', 'Login', '--format', 'json'])
        try:
            items = json.loads(out) if code == 0 else None
        except ValueError:
            items = None
        if not isinstance(items, list):
            raise OwnerError('1Password didn’t list your logins. Check that op is signed in, then try again.')
        for item in items[:MAX_ROWS]:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str):
                continue
            hrefs = [u.get('href') for u in item.get('urls') or [] if isinstance(u, dict)]
            for bound in dict.fromkeys(o for o in (browser_login.origin(h) for h in hrefs) if o and _fillable(o)):
                rows.append({'key': item['id'], 'title': str(item.get('title') or '')[:80], 'origin': bound,
                             'username': str(item.get('additional_information') or '')[:1000]})
    else:
        sep = '\x1f'
        code, out = _run([path, 'ls', '--sync=no', '--format', sep.join(('%ai', '%an', '%al', '%au'))])
        if code != 0:
            raise OwnerError('LastPass didn’t list your logins. Check that lpass is signed in, then try again.')
        for line in out.splitlines()[:MAX_ROWS]:
            parts = line.split(sep)
            if len(parts) != 4 or not parts[0].strip().isdigit():
                continue
            bound = browser_login.origin(parts[2])
            if bound and _fillable(bound):
                rows.append({'key': parts[0].strip(), 'title': parts[1][:80], 'origin': bound, 'username': parts[3][:1000]})
    return rows


def _tool_secret(manager, key):
    """(username, password) of one item, read from the tool now; ('', '') when it doesn't give them."""
    path = shutil.which(TOOLS[manager])
    if not path or not isinstance(key, str) or not key or key.startswith('-') or len(key) > 100:
        return '', ''
    if manager == '1password':
        code, out = _run([path, 'item', 'get', key, '--format', 'json', '--reveal'])
        try:
            item = json.loads(out) if code == 0 else {}
        except ValueError:
            item = {}
        fields = [f for f in (item.get('fields') or []) if isinstance(f, dict)] if isinstance(item, dict) else []
        pick = lambda purpose, ident: next((str(f.get('value') or '') for f in fields if f.get('purpose') == purpose or f.get('id') == ident), '')
        return pick('USERNAME', 'username'), pick('PASSWORD', 'password')
    if not key.isdigit():
        return '', ''
    code, out = _run([path, 'show', '--sync=no', '--json', key])
    try:
        items = json.loads(out) if code == 0 else []
    except ValueError:
        items = []
    item = items[0] if isinstance(items, list) and items and isinstance(items[0], dict) else {}
    return str(item.get('username') or ''), str(item.get('password') or '')


TOOL_SAYS = {
    '1password': {'missing': '1Password’s command-line tool (op) isn’t installed on this computer.',
                  'signed_out': 'Sign in to 1Password’s op on this computer first, then try again.'},
    'lastpass': {'missing': 'LastPass’s command-line tool (lpass) isn’t installed on this computer.',
                 'signed_out': 'Sign in to LastPass’s lpass on this computer first, then try again.'},
}


# Export pages in the Machine's browser

# Where each password manager exports, on the web. 1Password has no web export (only its apps, or op).
EXPORT_PAGES = {'lastpass': 'https://lastpass.com/vault/',
                'bitwarden': 'https://vault.bitwarden.com/#/tools/export',
                'chrome': 'https://passwords.google.com/options'}
EXPORT_SECONDS = 1200  # how long an export page waits for its download
OPEN_SECONDS = 90  # how long opening it may take (a browser that starts first) before it fails with a sentence
EXPORT_POLL = 1.5
OPEN_FAILED = 'I couldn’t open the export page in your Machine’s browser'
_exports = {}
_exports_lock = threading.Lock()


def export_open(base, manager, data_dir, store, shown=None, mail=None):
    """Starts the export and answers at once with {watch}: a thread of its own opens the manager's export page in a new
    tab of the browser at `base` (loopback DevTools), with its downloads going into a private folder made for this
    export only, calls shown(tab) to bring it to the front, and follows the page and that folder. The browser can take
    a while to start, so the dashboard's call never waits on it. export_check(watch) says how far it got: the step
    the owner is on (login_export_guide) and the review once the file is in. Starting one stops any other.
    mail(manager, since, seen): the verification link mailed since the click that started the export, or None
    (login_export_mail.link); _verify asks it while this export waits on that email."""
    if manager not in EXPORT_PAGES:
        raise OwnerError('Which password manager?')
    with _exports_lock:
        for old in _exports.values():
            old['stop'].set()
        _exports.clear()
    watch = {'token': secrets.token_urlsafe(18), 'manager': manager, 'state': 'waiting', 'step': 'opening',
             'stop': threading.Event(), 'opened': time.monotonic(), 'until': time.monotonic() + EXPORT_SECONDS,
             'base': base, 'tab': None, 'mail': mail, 'mails': set(), 'asked': None, 'verify_opened': False}
    with _exports_lock:
        _exports[watch['token']] = watch
    threading.Thread(target=_open_and_follow, args=(watch, Path(data_dir), store, shown), daemon=True, name='login-export').start()
    return {'watch': watch['token']}


def _open_and_follow(watch, data_dir, store, shown):
    folder = data_dir / ('login-export-' + secrets.token_hex(8))
    folder.mkdir(mode=0o700, parents=True)
    cdp = browser_login.browser_cdp
    session = None
    try:
        session = cdp.Session.browser(watch['base'], timeout=20)
        # held while the export is followed: the browser keeps this download folder for as long as the session is open
        session.call('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': str(folder)})
        _close_old_tabs(watch['base'])
        watch['before'] = {tab for tab, _ in cdp.pages(watch['base'], timeout=20)}
        watch['tab'] = cdp.open_tab(watch['base'], EXPORT_PAGES[watch['manager']])
        watch['tabs'] = {watch['tab']}
        with _exports_lock:
            _export_tabs.add(watch['tab'])
    except (cdp.CdpError, OSError, ValueError, TypeError, KeyError):
        if session:
            session.ws.close()
        _clear(folder)
        watch['error'], watch['state'] = OPEN_FAILED, 'failed'
        return
    if watch['stop'].is_set():  # Back while it opened
        _close_tabs(watch)
        _follow_end(session, folder)
        return
    watch['step'] = 'signin'
    if shown:
        try:
            shown(watch['tab'])
        except Exception:  # bringing it to the front is a nicety; the export goes on without it
            pass
    _follow(watch, session, folder, store)


_export_tabs = set()  # tabs exports opened or followed, closed when their export ends or the next one starts


def _close_old_tabs(base):
    """An earlier export's tabs that are still open (each try opened its own, and the manager opens more): closed, so
    tabs don't pile up and the guide never follows a stale one."""
    with _exports_lock:
        old = set(_export_tabs)
        _export_tabs.clear()
    for tab in old:
        try:
            browser_login.browser_cdp.close_tab(base, tab)
        except (browser_login.browser_cdp.CdpError, OSError):
            pass


def _close_tabs(watch):
    for tab in watch.get('tabs') or ():
        try:
            browser_login.browser_cdp.close_tab(watch['base'], tab)
        except (browser_login.browser_cdp.CdpError, OSError):
            pass
    with _exports_lock:
        _export_tabs.difference_update(watch.get('tabs') or ())


def _pick_tab(watch):
    """The tab to follow now: the manager's page the browser used last among the export's own tabs and the tabs opened
    since it started (the manager may sign in or open the vault in a new tab). Only addresses are compared, inside
    this process; none is kept or logged. Answers 'gone' when the browser answers and none is left, None when it
    doesn't answer."""
    cdp = browser_login.browser_cdp
    try:
        open_now = cdp.pages(watch['base'])
    except (cdp.CdpError, OSError, TypeError, KeyError, AttributeError):
        return None
    ids = {tab for tab, _ in open_now}
    watch['tabs'] &= ids
    ours = [tab for tab, url in open_now if (tab in watch['tabs'] or tab not in watch['before'])
            and login_export_guide.owns(watch['manager'], url)]
    if not ours:
        return watch['tab'] if watch['tab'] in ids else 'gone'
    if ours[0] != watch['tab']:
        LOG.info('login export follows another tab manager=%s tabs=%d', watch['manager'], len(ours))
        watch['tab'] = ours[0]
        watch['tabs'].add(ours[0])
        with _exports_lock:
            _export_tabs.add(ours[0])
    return watch['tab']


def _follow(watch, session, folder, store):
    """Waits for the export's download, reads it, deletes it and holds its review; meanwhile the guide clicks the page
    on to its export step and says what is left for the owner. Then puts the browser's downloads back and removes the
    folder, whatever happened."""
    sizes, guide = {}, login_export_guide.start()
    try:
        while not watch['stop'].wait(EXPORT_POLL):
            if time.monotonic() > watch['until']:
                watch['state'] = 'expired'
                return
            try:  # again each round: another DevTools client of the browser may have set its own download folder
                session.call('Browser.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': str(folder)})
            except (browser_login.browser_cdp.CdpError, OSError):
                pass
            path = _whole_file(folder, sizes)
            if not path:
                if _pick_tab(watch) == 'gone':
                    LOG.info('login export tab closed manager=%s', watch['manager'])
                    watch['error'], watch['state'] = 'The export page was closed. Try again.', 'failed'
                    return
                if watch['step'] != 'manual':
                    said = login_export_guide.step(watch['base'], watch['tab'], watch['manager'], guide)
                    if said and said != watch['step']:
                        LOG.info('login export step manager=%s step=%s', watch['manager'], said)
                    if said:
                        watch['step'], watch['focus'] = said, guide['box']
                    _verify(watch, guide)
                continue
            try:
                kind, rows, skipped = parse(_take(path))
                watch['review'] = start(kind, rows, skipped, store)
                watch['state'] = 'review'
            except OwnerError as error:
                watch['error'], watch['state'] = str(error), 'failed'
            return
    finally:
        LOG.info('login export ended manager=%s state=%s step=%s', watch['manager'], watch['state'], watch['step'])
        _close_tabs(watch)
        _follow_end(session, folder)


VERIFY_SECONDS = 600  # how long after the click that started the export its email's link may be opened
VERIFY_POLL = 10  # seconds between looks in the mailboxes
VERIFY_LOAD = 15  # seconds the link's page gets to load before its tab is closed


def _verify(watch, guide):
    """While this export waits on the manager's email to confirm it (the guide clicked the step that starts it, at
    most VERIFY_SECONDS ago): looks for that mail's link (watch['mail'], login_export_mail.link) and opens it once in
    this export's browser, in a tab of its own closed afterwards; then the guide may start the export once more.
    Nothing without a running export and its click; at most one link per export. Answers whether it opened one."""
    started, mail = guide.get('started'), watch.get('mail')
    if not mail or started is None or guide.get('verified') or watch['verify_opened'] or watch['stop'].is_set():
        return False
    now = time.monotonic()
    if now - started > VERIFY_SECONDS or (watch['asked'] is not None and now - watch['asked'] < VERIFY_POLL):
        return False
    watch['asked'] = now
    try:
        link = mail(watch['manager'], guide['started_at'], watch['mails'])
    except Exception:  # a mailbox that can't be read now: the owner confirms by hand, as before
        LOG.info('login export verify unread manager=%s', watch['manager'])
        return False
    if not login_export_guide.allowed(watch['manager'], link):
        return False
    watch['verify_opened'] = True  # once per export, whatever happens next
    opened = _open_link(watch['base'], link)
    LOG.info('login export verify opened manager=%s ok=%s', watch['manager'], 'yes' if opened else 'no')
    if opened:
        login_export_guide.verified(guide)
    return opened


def _open_link(base, link):
    """Opens the link in a new tab of the export's browser, gives its page time to load and closes the tab."""
    cdp = browser_login.browser_cdp
    try:
        tab = cdp.open_tab(base, link)
    except (cdp.CdpError, OSError, ValueError, TypeError, KeyError):
        return False
    try:
        end = time.monotonic() + VERIFY_LOAD
        while time.monotonic() < end:
            try:
                if cdp.evaluate(base, tab, '() => document.readyState') == 'complete':
                    time.sleep(2)  # the page's own script confirms after it loaded
                    break
            except (cdp.CdpError, OSError, ValueError, TypeError, KeyError):
                pass
            time.sleep(0.5)
        return True
    finally:
        try:
            cdp.close_tab(base, tab)
        except (cdp.CdpError, OSError):
            pass


def _follow_end(session, folder):
    try:
        session.call('Browser.setDownloadBehavior', {'behavior': 'default'})
    except (browser_login.browser_cdp.CdpError, OSError):
        pass
    session.ws.close()
    _clear(folder)


def _whole_file(folder, sizes):
    """The download in `folder` once it is whole: no partial file left and its size the same as the last look."""
    try:
        files = [p for p in folder.iterdir() if p.is_file()]
    except OSError:
        return None
    if any(p.name.endswith('.crdownload') for p in files):
        return None
    for path in files:
        size = path.stat().st_size
        if sizes.get(path.name) == size and size:
            return path
        sizes[path.name] = size
    return None


def _take(path):
    """The file's text, read once, and the file gone from disk right after."""
    try:
        with open(path, 'rb') as handle:
            data = handle.read(MAX_BYTES + 1)
    finally:
        path.unlink(missing_ok=True)
    if len(data) > MAX_BYTES:
        raise OwnerError('That file is too big (5 MB at most)')
    return data.decode('utf-8-sig', 'replace')


def _clear(folder):
    """The export's folder and anything left in it (a partial download holds passwords too)."""
    shutil.rmtree(folder, ignore_errors=True)


def export_check(token):
    """{state: waiting, step} while the export page is open (step: opening, signin, working, password, email or
    manual, login_export_guide.step); the review (state: review) once its file was read; {state: failed, error} or
    {state: expired}. A finished one is answered once."""
    with _exports_lock:
        watch = _exports.get(token) if isinstance(token, str) else None
        if not watch:
            return {'state': 'expired'}
        if watch['step'] == 'opening' and watch['state'] == 'waiting' and time.monotonic() - watch['opened'] > OPEN_SECONDS:
            watch['stop'].set()
            watch['error'], watch['state'] = OPEN_FAILED, 'failed'
        if watch['state'] != 'waiting':
            _exports.pop(token, None)
    if watch['state'] == 'review':
        return {**watch['review'], 'state': 'review'}
    if watch['state'] == 'failed':
        return {'state': 'failed', 'error': watch['error']}
    if watch['state'] == 'waiting':
        return {'state': 'waiting', 'step': watch['step']}
    return {'state': watch['state']}


def export_focus():
    """Where the owner types on the export page now (sign-in or master password), as fractions of the browser's
    window, for the live view to zoom to on a phone (browser_viewer.on_screen); None at any other step."""
    with _exports_lock:
        return next((w.get('focus') for w in _exports.values() if w['state'] == 'waiting' and w.get('focus')), None)


def export_stop(token):
    with _exports_lock:
        watch = _exports.pop(token, None) if isinstance(token, str) else None
    if watch:
        watch['stop'].set()
        if watch.get('review'):
            drop(watch['review']['token'])
    return watch is not None


# Reviews

def _sweep():
    cutoff = time.monotonic() - KEEP_SECONDS
    for token in [t for t, p in _pending.items() if p['at'] < cutoff]:
        _pending.pop(token, None)


def start(kind, rows, skipped=0, store=None):
    """Holds a review's rows (with their passwords, for a file) in memory and returns what the dashboard shows:
    {token, kind, manager, rows: [{key, title, site, origin, username, saved}], skipped}. `saved`: the account names
    already kept for that exact origin."""
    token = secrets.token_urlsafe(24)
    with _pending_lock:
        _sweep()
        while len(_pending) >= 5:
            _pending.pop(next(iter(_pending)))
        # a tool's rows carry no password (it is read at Keep); an export file's always do, also LastPass's or 1Password's
        tool = kind in TOOLS and not any('password' in r for r in rows)
        _pending[token] = {'at': time.monotonic(), 'kind': kind, 'tool': tool, 'rows': {r['key'] + '|' + r['origin']: r for r in rows}}
    have = {}
    for entry in (store.list() if store else []):
        have.setdefault(entry['origin'], []).append(entry['account'])
    shown = [{'key': r['key'] + '|' + r['origin'], 'title': r.get('title') or browser_login.brand(r['origin'].split('://', 1)[1]),
              'site': browser_login.origin_label(r['origin']), 'origin': r['origin'], 'username': r.get('username') or '',
              'saved': have.get(r['origin'], [])} for r in rows]
    shown.sort(key=lambda r: (browser_login.site(r['site']), r['username'].lower()))
    return {'token': token, 'kind': kind, 'manager': MANAGERS.get(kind, kind), 'rows': shown, 'skipped': skipped}


def keep(store, token, keys, account=None):
    """Keeps the rows the owner ticked under `account`, then drops the review. A tool's passwords are read now, for
    those rows only. Returns how many were kept."""
    with _pending_lock:
        _sweep()
        review = _pending.pop(token, None) if isinstance(token, str) else None
    if not review:
        raise OwnerError('That review has expired. Start the import again.')
    if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
        raise OwnerError('Which sign-ins?')
    chosen = [review['rows'][k] for k in dict.fromkeys(keys) if k in review['rows']]
    if review['tool']:
        items = []
        for row in chosen:
            username, password = _tool_secret(review['kind'], row['key'])
            items.append({'origin': row['origin'], 'username': username or row.get('username'), 'password': password})
        source = review['kind']
    else:
        items = [{'origin': r['origin'], 'username': r.get('username'), 'password': r.get('password')} for r in chosen]
        source = 'csv:' + review['kind']
    return store.save_many([i for i in items if i['password']], account=account, source=source)


def drop(token):
    with _pending_lock:
        return _pending.pop(token, None) is not None if isinstance(token, str) else False

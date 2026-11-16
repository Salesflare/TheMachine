"""Bringing saved sign-ins in from a password manager, into the store the sign-in dialog uses (browser_login.LoginStore).

Two ways, both started by the owner on the dashboard and both ending in a review where they tick which to keep:

- An export file (CSV) from 1Password, LastPass, Bitwarden or Chrome (Edge, Brave and Firefox write the same columns).
  parse() reads it in memory; nothing of it is written anywhere until the owner keeps some.
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
import os
import secrets
import shutil
import subprocess
import threading
import time

import browser_login
from machine.owner_error import OwnerError

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
    try:
        reader = csv.DictReader(io.StringIO(text, newline=''))
        header = reader.fieldnames or []
        kind = kind_of(header)
        if not kind:
            raise OwnerError('That isn’t a password export this can read. Export a CSV from 1Password, LastPass, Bitwarden or Chrome.')
        lower = {h: str(h or '').strip().lower() for h in header}
        found, skipped, seen = [], 0, {}
        for count, raw in enumerate(reader):
            if count >= MAX_ROWS:
                raise OwnerError('That file has too many rows (5,000 at most)')
            row = {lower.get(k, k): v for k, v in raw.items() if isinstance(k, str)}
            if kind == 'bitwarden' and _cell(row, 'type') not in ('', 'login'):
                skipped += 1
                continue
            address = {'bitwarden': _cell(row, 'login_uri'), '1password': _cell(row, 'url', 'website')}.get(kind) or _cell(row, 'url')
            username = _cell(row, 'login_username') if kind == 'bitwarden' else _cell(row, 'username')
            password = (row.get('login_password') if kind == 'bitwarden' else row.get('password')) or ''
            title = _cell(row, 'name', 'title')
            origins = [o for o in (browser_login.origin(a) for a in _addresses(address)) if o and _fillable(o)]
            if not origins or not password:
                skipped += 1
                continue
            for bound in dict.fromkeys(origins):
                seen[(bound, username, password)] = {'title': title[:80], 'origin': bound, 'username': username[:1000], 'password': password[:1000]}
    except csv.Error:
        raise OwnerError('That file couldn’t be read as a CSV') from None
    rows = [{'key': secrets.token_hex(6), **row} for row in seen.values()]
    return kind, rows, skipped


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
        _pending[token] = {'at': time.monotonic(), 'kind': kind, 'rows': {r['key'] + '|' + r['origin']: r for r in rows}}
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
    if review['kind'] in TOOLS:
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

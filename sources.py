"""Reading the owner's sources: plain functions any module may import (nothing of the app's own beyond the Google and
Microsoft clients, and machine/services.py, a leaf).

SourceError and how a failure is judged (rate_limited, upstream_busy, transient); the credentials in config.json's
`credentials` (or systemd's CREDENTIALS_DIRECTORY); gog_read, the one read of a Google or Outlook mailbox or calendar;
which accounts are mail, calendar or Microsoft; and gog's sign-in on disk. `config` is The Machine's config.json and
`account` one of its `accounts`."""
import base64
import datetime as dt
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import subprocess
import sys
import threading
import time

import caldav_calendar
import ews_calendar
import google_api
import ics_feed
import imap_mail
import ms_graph
import smtp_mail
from machine import services

# The service's "busy, try again" statuses (5xx it recovers from by itself, 429): one quick retry, then the normal wait
UPSTREAM_BUSY = {429, 500, 502, 503, 504}
# Go runtime settings for each gog process: a gog read is a new process per message when there is no token to read
# Gmail with in-process (gog_token; gog has no batched or long-running read of whole messages), and most of its CPU is
# Go starting up on every core and collecting garbage it is about to drop at exit. One core and no collection under
# 256 MiB cut a read's CPU by about a third; its output is the same. A value already set in the service's own
# environment wins.
GOG_RUNTIME = {'GOMAXPROCS': '1', 'GOGC': 'off', 'GOMEMLIMIT': '256MiB'}


def rate_limited(error):
    """The service asked to slow down (HTTP 429, or its own ratelimited label): expected, and retried after its wait."""
    category = str(getattr(error, 'category', '') or '')
    return getattr(error, 'status', None) == 429 or bool(re.match(r'[a-z0-9_]*rate_?limit', category))


def upstream_busy(error):
    """The service answered 429 or a transient 5xx (500, 502, 503, 504): its hiccup, not ours, and retried."""
    return getattr(error, 'status', None) in UPSTREAM_BUSY or rate_limited(error)


def transient(error):
    """A sync failure that is no bug: the service busy (upstream_busy), or the network (network:..., *_network,
    *_unreachable, a timeout), a browser reader's own hiccup (a tab that didn't answer, the browser busy with another
    read, one slow request), or a 400 on the quick retry right after the service was busy (after_busy, set by
    App.sync_retrying). Retried; only reported when it keeps happening (TRANSIENT_REPORT_AFTER)."""
    category = str(getattr(error, 'category', '') or '')
    return upstream_busy(error) or getattr(error, 'after_busy', False) or category.startswith('network:') or category == 'timeout' or \
        bool(re.fullmatch(r'[a-z0-9_]*_(?:network|unreachable|browser_stalled|browser_busy|read_timeout)', category))


# X's own web app answering oddly or slowly for a while (its page in another shape, a 5xx, a tab that didn't answer)
SHORT_OUTAGE = re.compile(r'x_(?:query_unavailable|query_failed:HTTP_5\d\d|read_timeout|browser_stalled)')
SHORT_OUTAGE_TRIES = 3


def short_outage(error, failures):
    """A failed read that often passes by itself, with under SHORT_OUTAGE_TRIES tries in a row failed: its connection
    still shows as connected (Recent syncs lists the tries). From then on it shows, until a read works."""
    return (failures or 0) < SHORT_OUTAGE_TRIES and bool(SHORT_OUTAGE.fullmatch(str(error or '')))


def outage_backoff(error, delay, failures, poll):
    """Seconds until the next read: for such an outage twice as long after each failed one, up to the usual poll, so
    a long one isn't met with a read every few minutes. Any other failure keeps its own `delay`."""
    return min(delay * 2 ** min(failures or 0, 10), max(delay, poll)) if SHORT_OUTAGE.fullmatch(str(error)) else delay


class SourceError(Exception):
    """Only redacted, structured error labels are allowed in logs/checkpoints. `route` is the endpoint that failed with its
    ids masked (/accounts/{id}/feed), logged next to the category so support can tell which request it was."""
    def __init__(self, category, status=None, retry_after=None, route=None):
        self.category, self.status, self.retry_after, self.route = category, status, retry_after, route
        super().__init__(category + (f':HTTP_{status}' if status else ''))


def credential(config, name):
    directory = os.environ.get('CREDENTIALS_DIRECTORY')
    path = Path(directory) / name if directory and (Path(directory) / name).exists() else Path(config['credentials'][name]).expanduser()
    return path.read_text().strip()


def owner_credential(config):
    """The Gateway plugin's second key for owner taps. The API token alone (CLI, scripts, anything
    an agent could copy) can read and save, but cannot record a decision or approve a send."""
    path = Path(config['credentials'].get('owner-token') or Path(config['database']).expanduser().parent / 'owner-token').expanduser()
    if not path.exists():
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as handle:
            handle.write(secrets.token_hex(32))
    return path.read_text().strip()


def gog_read(config, account, api, version, method, params, scope):
    """Use the existing account's gog token; never authorize or write from ingestion. An account with
    "transport": "broker" gets a short-lived token from the configured Google broker instead (google_api.py).
    An Outlook account (Microsoft 365 or Outlook.com) answers the same Gmail and Calendar reads from Graph (ms_graph.py)."""
    if account.get('service') == 'imap':  # any other mailbox, read over IMAP in Gmail's shapes (imap_mail.py)
        if api != 'gmail':
            raise SourceError('unsupported_transport')
        try:
            return imap_mail.gmail_call(config, credential, account, method, params)
        except imap_mail.ImapError as error:
            raise SourceError(error.category, error.status, error.retry_after) from None
    if account.get('transport') in OTHER_CALENDAR_READERS:  # CalDAV, a calendar link or Exchange Server, in Google's shape
        if api != 'calendar':
            raise SourceError('unsupported_transport')
        try:
            return OTHER_CALENDAR_READERS[account['transport']].calendar_call(config, credential, account, method.split('.', 1)[1], params)
        except caldav_calendar.CalendarError as error:
            raise SourceError(error.category, error.status, error.retry_after) from None
    if account.get('service') in MICROSOFT_SERVICES:
        try:
            if api == 'calendar':
                return ms_graph.calendar_call(config, credential, account, method.split('.', 1)[1], params)
            return ms_graph.gmail_call(config, credential, account, method, params)
        except ms_graph.GraphError as error:
            raise SourceError(error.category, error.status, error.retry_after, route=error.route) from None
    if account['transport'] == 'broker':
        try:
            return google_api.call(config, credential, account, method, params, scope)
        except google_api.BrokerError as error:
            raise SourceError(error.category, error.status, getattr(error, 'retry_after', None)) from None
    if account['transport'] != 'gog':
        raise SourceError('unsupported_transport')
    if api == 'gmail' and method in google_api.READ:
        access = gog_token(config, account)
        if access:
            try:
                data = google_api.read_with(access, method, params)
            except google_api.BrokerError as error:
                if error.status not in (401, 403) or (error.status == 403 and error.reason not in SCOPE_REFUSALS):
                    raise SourceError(error.category, error.status, error.retry_after) from None
                gog_token_refused(account, error.status)  # gog's own call below says what is wrong, or refreshes it
            else:
                if not isinstance(data, dict):
                    raise SourceError('invalid_response')
                return data
    data = gog_call(config, account, api, version, method, params, scope)
    if api == 'gmail':
        gog_token_refreshed(account)
    return data


# A self-hosted Gmail account's reads without a gog process each (gog_read): gog keeps the account's current access
# token in its file keyring and refreshes it there; `gog auth tokens export` hands it over, so one gog process serves
# every read until GOG_TOKEN_MARGIN before it expires. Same account, client and grant as gog's own calls, nothing new
# asked of Google, only the allowlisted reads in google_api.READ, and the token stays in memory (never logged or written).
# The refresh token the export also carries is dropped at once: gog alone refreshes. When there is no token to take
# (an older gog without the export, Windows, a token about to expire), each read goes through gog as before.
GOG_TOKEN_MARGIN = 60  # seconds before its expiry a token is no longer used
GOG_EXPORT_WAIT = 3600  # after an export that gave nothing usable (an older gog, a token refused): gog alone this long
SCOPE_REFUSALS = {'ACCESS_TOKEN_SCOPE_INSUFFICIENT', 'insufficientPermissions'}
_gog_tokens: dict = {}  # (email, client) -> {'access', 'expires', 'retry_at', 'stale', 'waiting'}
_gog_lock = threading.Lock()


def _gog_key(account):
    return (str(account.get('email') or '').lower(), str(account.get('client') or ''))


def gog_token(config, account):
    """The account's current access token from gog's keyring, or None: then the read goes through gog."""
    if os.name == 'nt' or not account.get('email') or not account.get('client'):
        return None
    with _gog_lock:
        held = _gog_tokens.setdefault(_gog_key(account), {})
        if held.get('access') and held['expires'] - GOG_TOKEN_MARGIN > time.time():
            return held['access']
        if time.time() < held.get('retry_at', 0):
            return None
        access, expires = _gog_export(config, account)
        if access and expires - GOG_TOKEN_MARGIN > time.time():
            held.update(access=access, expires=expires, retry_at=0, stale=0, waiting=False)
            return access
        if access and expires > time.time():  # about to expire: gog refreshes it only once it has, so try again then
            held.pop('access', None)
            held.update(retry_at=expires, waiting=False)
            return None
        # Expired in the keyring: gog's next read refreshes it there, and the try after that (gog_token_refreshed) takes
        # it. A second stale one, or none at all, means this gog doesn't keep one: gog alone for GOG_EXPORT_WAIT.
        _gog_wait(held, held.get('stale', 0) + 1 if access else 2)
        return None


def _gog_wait(held, stale):
    held.pop('access', None)
    held.update(stale=stale, waiting=stale == 1, retry_at=time.time() + GOG_EXPORT_WAIT)


def gog_token_refreshed(account):
    """A gog read just went through: when the token held was stale, the keyring now holds a fresh one."""
    with _gog_lock:
        held = _gog_tokens.get(_gog_key(account))
        if held and held.get('waiting'):
            held.update(retry_at=0, waiting=False)


def gog_token_refused(account, status):
    """Google refused the token (401: expired early; 403: it lacks Gmail's read scope): not used again. A 401 tries the
    keyring once more after gog's own read; a 403 leaves the account to gog for GOG_EXPORT_WAIT."""
    with _gog_lock:
        _gog_wait(_gog_tokens.setdefault(_gog_key(account), {}), 1 if status == 401 else 2)


def _gog_export(config, account):
    """(access token, expiry as a Unix time) from `gog auth tokens export`, or (None, 0). Its output goes to a pipe."""
    command = [config['gog'], 'auth', 'tokens', 'export', account['email'], '--client', account['client'],
               '--out', '/dev/stdout', '--overwrite', '--no-input']
    try:
        result = subprocess.run(command, env=gog_env(config), capture_output=True, text=True, timeout=30)
        found, _ = json.JSONDecoder().raw_decode(result.stdout.lstrip()) if not result.returncode else ({}, 0)
    except (subprocess.TimeoutExpired, OSError, ValueError, KeyError):
        return None, 0
    if not isinstance(found, dict):
        return None, 0
    access, at = found.get('access_token'), found.get('access_token_expires_at')
    same = (str(found.get('email') or '').lower(), str(found.get('client') or account['client'])) == _gog_key(account)
    found.clear()  # the refresh token with it: never kept here
    if not same:  # only the account's own sign-in
        return None, 0
    try:
        expires = dt.datetime.fromisoformat(str(at).replace('Z', '+00:00')).timestamp()
    except ValueError:
        return None, 0
    return (access, expires) if isinstance(access, str) and access.strip() else (None, 0)


def gog_env(config):
    env = {**GOG_RUNTIME, **os.environ}
    env.update(GOG_KEYRING_BACKEND='file', GOG_KEYRING_PASSWORD=credential(config, 'gog-password'))
    env.pop('DBUS_SESSION_BUS_ADDRESS', None)
    return env


def gog_call(config, account, api, version, method, params, scope):
    """One `gog api call`: a new gog process."""
    env = gog_env(config)
    params = json.dumps(params, ensure_ascii=False, sort_keys=True, separators=(',', ':'))  # as assistant.encoded
    command = [config['gog'], 'api', 'call', api, version, method, '--params', params,
               '--scope', scope, '--account', account['email'], '--client', account['client'],
               '--json', '--readonly', '--no-input']
    try:
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        raise SourceError('timeout') from None
    if result.returncode:
        if re.search(r'invalid_grant|expired or revoked', result.stderr):
            # The stored Google sign-in is gone; retrying every cycle can't help until the owner runs
            # `gog auth add <email> --client <client>` again, so say so and back off for an hour.
            raise SourceError(api + ':google_signin_expired_run_gog_auth_add', retry_after=3600)
        match = re.search(r'\b(400|401|403|404|410|429|5\d\d)\b', result.stderr)
        raise SourceError(api, int(match[1]) if match else None)
    try:
        data = json.loads(result.stdout)
    except ValueError:
        raise SourceError('invalid_json') from None
    if not isinstance(data, dict) or data.get('error'):
        raise SourceError('invalid_response')
    return data

# Outlook mail and calendar: they flow through the same sync, cards and sends as Gmail and Google Calendar, and their
# messages are stored with the same 'gmail.message' kind (it means "an email" everywhere in the app).
MICROSOFT_SERVICES = services.of(signin='microsoft')
# Any other mailbox over IMAP ('imap', imap_mail.py) flows through the same sync the same way, and sends through its own
# SMTP server (smtp_mail.py).
MAIL_SERVICES = services.of(group=services.MAIL)
# Calendars beyond Google and Outlook, read only: iCloud and any other CalDAV server (caldav_calendar.py), Proton
# Calendar and any calendar link (ics_feed.py), Exchange Server (ews_calendar.py). They answer Google's calendar reads.
OTHER_CALENDARS = ('icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')
CALENDAR_SERVICES = services.of(group=services.CALENDAR)  # Google, Outlook and OTHER_CALENDARS
OTHER_CALENDAR_READERS = {'caldav': caldav_calendar, 'ics': ics_feed, 'ews': ews_calendar}


def mail_account(account):
    """An owner's mailbox we can read and send from: Gmail (gog or broker), Outlook (broker or own app) or Other email."""
    service = account.get('service', 'gmail')
    return (service == 'gmail' and account.get('transport') in ('gog', 'broker')) or (
        service == 'outlook' and account.get('transport') in ('broker', 'graph')) or smtp_mail.sends(account)


def mailbox_name(config, action):
    """Gmail, Outlook or Your mail server: what an email action's account is, for the owner's messages."""
    account = next((a for a in config.get('accounts', []) if a.get('id') == action.get('account_id')), {})
    return {'outlook': 'Outlook', 'imap': 'Your mail server'}.get(account.get('service'), 'Gmail')


def gog_signin_command(config, account):
    """The command that signs a Google account in again where the assistant reads it: gog's file
    keyring, unlocked with the password file it was given. A plain `gog auth add` lands in the
    desktop keyring, which the assistant never reads. Shows the password file's path, never its contents."""
    base = f"gog auth add {shlex.quote(account.get('email', ''))} --client {shlex.quote(account.get('client', ''))}"
    path = (config.get('credentials') or {}).get('gog-password')
    if not path:
        return base
    return f'GOG_KEYRING_BACKEND=file GOG_KEYRING_PASSWORD="$(cat {shlex.quote(str(Path(path).expanduser()))})" ' + base


def gog_token_path(config, account):
    """gog's file-keyring entry for this account's refresh token (token:<client>:<email>, base64url)."""
    name = base64.urlsafe_b64encode(f"token:{account.get('client', '')}:{account.get('email', '')}".encode()).decode().rstrip('=')
    root = config.get('gog_keyring_dir')
    if not root:
        # gog keeps its data in the platform's own place: XDG on Linux, Application Support on macOS.
        found = [Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local/share') / 'gogcli/keyring']
        if sys.platform == 'darwin':
            found.insert(0, Path.home() / 'Library/Application Support/gogcli/keyring')
        root = next((folder for folder in found if folder.is_dir()), found[-1])
    return Path(root).expanduser() / ('_gogcli_key_v1_' + name)


def gog_signed_in_since(config, account, since):
    """True when the account's stored Google sign-in was written, or its Microsoft account connected again, after
    `since` (an ISO time)."""
    if account.get('service') in MICROSOFT_SERVICES and since:
        return ms_graph.connected_since(config, account, since)
    if (account.get('service') == 'imap' or account.get('service') in OTHER_CALENDARS) and since:  # a new password saved (Reconnect): try it at once
        try:
            path = Path(os.environ.get('CREDENTIALS_DIRECTORY') or '/nonexistent') / account['credential']
            path = path if path.exists() else Path(config['credentials'][account['credential']]).expanduser()
            return path.stat().st_mtime > dt.datetime.fromisoformat(since).timestamp()
        except (OSError, KeyError, TypeError, ValueError):
            return False
    if account.get('transport') not in ('gog', 'graph') or not since:
        return False
    try:
        written = (ms_graph.credential_path(config, account) if account['transport'] == 'graph'
                   else gog_token_path(config, account)).stat().st_mtime
        return written > dt.datetime.fromisoformat(since).timestamp()
    except (OSError, ValueError, ms_graph.GraphError):
        return False

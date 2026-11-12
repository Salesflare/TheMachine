"""Reading the owner's sources: plain functions any module may import (nothing of the app's own beyond the Google and
Microsoft clients).

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

import caldav_calendar
import ews_calendar
import google_api
import ics_feed
import imap_mail
import ms_graph
import smtp_mail

# The service's "busy, try again" statuses (5xx it recovers from by itself, 429): one quick retry, then the normal wait
UPSTREAM_BUSY = {429, 500, 502, 503, 504}


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
            raise SourceError(error.category, error.status, error.retry_after) from None
    if account['transport'] == 'broker':
        try:
            return google_api.call(config, credential, account, method, params, scope)
        except google_api.BrokerError as error:
            raise SourceError(error.category, error.status, getattr(error, 'retry_after', None)) from None
    if account['transport'] != 'gog':
        raise SourceError('unsupported_transport')
    env = os.environ.copy()
    env.update(GOG_KEYRING_BACKEND='file', GOG_KEYRING_PASSWORD=credential(config, 'gog-password'))
    env.pop('DBUS_SESSION_BUS_ADDRESS', None)
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
MICROSOFT_SERVICES = ('outlook', 'outlook_calendar')
# Any other mailbox over IMAP ('imap', imap_mail.py) flows through the same sync the same way, and sends through its own
# SMTP server (smtp_mail.py).
MAIL_SERVICES = ('gmail', 'outlook', 'imap')
# Calendars beyond Google and Outlook, read only: iCloud and any other CalDAV server (caldav_calendar.py), Proton
# Calendar and any calendar link (ics_feed.py), Exchange Server (ews_calendar.py). They answer Google's calendar reads.
OTHER_CALENDARS = ('icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')
CALENDAR_SERVICES = ('calendar', 'outlook_calendar', *OTHER_CALENDARS)
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

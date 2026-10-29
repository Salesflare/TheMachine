"""Sign in with Slack: the owner's own Slack sign-in, through The Machine's Slack app at the hosting control plane.

The control plane holds the app's client secret; the sign-in itself (a refresh token, Slack's token rotation) lives on
this Machine only, sealed in mail_grants.py under "slack:<team id>:<user id>". For each access token (12 hours) the
Machine sends it to the broker, which asks Slack and passes back the access token and, when Slack rolled it, the new
refresh token, keeping neither. Reads and the owner-approved direct messages then go straight to Slack's Web API.

    {"id": "work-slack", "service": "slack", "transport": "broker", "team_id": "T...", "user_id": "U...", ...}
    "slack_broker": {"url": "https://app.example.com/api/slack/token"},
    "credentials": {"slack-broker": "~/.local/share/personal-assistant/google-broker"}

The broker answers POST {"email": "<team id>:<user id>", "refresh_token"} with {"access_token", "expires_in", "scopes",
"refresh_token"}. A Slack account connected through Maton ("transport": "maton") keeps reading as before until the
owner signs in with Slack (Connections shows Reconnect Slack); that switches the same account over, history and all.

The user token's scopes (the control plane's cloud/slack_app.py USER_SCOPES) are what the reader and the Slack
transport use, nothing more: read the conversations the owner is in, the people in them, and send one direct message
the owner approved."""
from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

API = 'https://slack.com/api/'
_tokens = {}
_lock = threading.Lock()


class TokenError(Exception):
    """No access token: `label` says why (redacted, no token), `status` the broker's HTTP status."""

    def __init__(self, label, status=None, retry_after=None):
        super().__init__(label)
        self.label, self.status, self.retry_after = label, status, retry_after


def key(account):
    """The sign-in's name in mail_grants.py: '<team id>:<user id>', lower case."""
    team, user = str(account.get('team_id') or '').strip().lower(), str(account.get('user_id') or '').strip().lower()
    return f'{team}:{user}' if team and user else ''


def _credential(config, name):
    directory = os.environ.get('CREDENTIALS_DIRECTORY')
    path = Path(directory) / name if directory and (Path(directory) / name).exists() else Path(config['credentials'][name]).expanduser()
    return path.read_text().strip()


def broker_token(config, account, fresh=False):
    """A short-lived access token for a Slack account signed in with Slack: (token, seconds left). Sends the sign-in
    kept here to the broker and keeps the one Slack rolled."""
    import mail_grants
    name = key(account)
    if not name:
        raise TokenError('slack_no_account')
    with _lock:
        hit = _tokens.get(name)
        if hit and not fresh and hit[1] > time.monotonic():
            return hit[0], int(hit[1] - time.monotonic())
        url = (config.get('slack_broker') or {}).get('url')
        if not url or not str(url).startswith('https://'):
            raise TokenError('slack_broker_not_configured')
        try:
            secret = _credential(config, 'slack-broker')
        except (KeyError, OSError):
            raise TokenError('slack_broker_credential') from None
        for attempt in (0, 1):
            try:
                kept = mail_grants.get(config, 'slack', name)
            except mail_grants.GrantError:
                raise TokenError('slack_signin_unreadable') from None
            if not kept:
                raise TokenError('slack_signin_expired')
            request = urllib.request.Request(url, method='POST', data=json.dumps({'email': name, 'refresh_token': kept}).encode(),
                                             headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json',
                                                      'Accept': 'application/json'})
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    answer = json.loads(response.read(200_000))
                break
            except urllib.error.HTTPError as error:
                retry = error.headers.get('Retry-After', '') if error.headers else ''
                error.close()
                if error.code in (401, 404):
                    try:
                        moved = mail_grants.get(config, 'slack', name) not in (None, kept)
                    except mail_grants.GrantError:
                        moved = False
                    if moved and not attempt:
                        continue  # another process (a check while connecting) rolled it just now: the newer one
                    raise TokenError('slack_signin_expired', error.code) from None
                raise TokenError('slack_broker', error.code, int(retry) if retry.isdigit() else None) from None
            except (urllib.error.URLError, TimeoutError, OSError, ValueError):
                raise TokenError('slack_broker_unreachable') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        if not isinstance(access, str) or not access:
            raise TokenError('slack_broker')
        rotated = answer.get('refresh_token')
        if isinstance(rotated, str) and rotated and rotated != kept:
            mail_grants.rotate(config, 'slack', name, kept, rotated)  # the one sent may be spent now: keep the new one
        left = max(0, int(answer.get('expires_in') or 0) - 300)
        _tokens[name] = (access, time.monotonic() + left)
        return access, left


def forget_token(account):
    """Drop a cached access token (Slack refused it, or the account was disconnected)."""
    with _lock:
        _tokens.pop(key(account), None)

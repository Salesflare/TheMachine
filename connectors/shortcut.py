"""Shortcut pipeline moves, via GET-only story search and history.

Uses the standard library, with no SDK or write endpoints. Search uses a one-day overlap for date precision and
indexing delays. History supplies individual transitions, including multiple moves between polls.

Two ways in:
- Sign in with Shortcut (the usual one): the hosting control plane runs Shortcut's OAuth consent with scope `read`
  only, for The Machine's public client (no client secret, PKCE), and hands the result here as the credential, JSON:
  {"client_id", "access_token", "refresh_token", "expires_at"}. The access token goes as a Bearer token. Shortly
  before it runs out (or when Shortcut turns it down once), this Machine refreshes it itself at Shortcut's token
  endpoint with the client id and the refresh token, and keeps the new pair in the same private credential file.
- A pasted personal API token (the fallback): it has full account access (Shortcut has no read-only token);
  this reader never uses it to write.
"""
import copy
import datetime as dt
import hashlib
import html
import http.client
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

import i18n
import locale_prefs

KINDS = {'shortcut.move': 'Shortcut'}
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {'shortcut.move': 'card'}
APP = 'Shortcut'
# Shortcut's own API Tokens page. Without a workspace in the address, Shortcut opens it in the workspace the owner
# last used; the check names the workspace the token belongs to, so a token from another one shows right away.
TOKEN_URL = 'https://app.shortcut.com/settings/account/api-tokens'
SETUP = {
    'label': 'Shortcut',
    'what': 'Stories that change state, with their owners and deadlines.',
    'account': {'id': 'shortcut', 'service': 'shortcut', 'transport': 'api',
                'boundary': 'work', 'credential': 'shortcut', 'poll_seconds': 300},
    # No workspace to type: the token's own member check (GET /member) says which workspace it is. Sign in with
    # Shortcut answers this same prompt with its read-only sign-in (JSON); pasting a personal token is the fallback.
    'secret': 'Shortcut API token',
    'token_url': TOKEN_URL,
    # Signed in at the hosting control plane (hosted: its account page; self-hosted: paired, from Connections, + Add)
    'account_page': 'source-shortcut',
    'note': 'Sign in with Shortcut from Connections, + Add. Or get a token at '
            'https://app.shortcut.com/settings/account/api-tokens and paste it here. '
            'It only reads, never changes anything in Shortcut.',
    'hints': {'shortcut_signin_expired': 'Shortcut asks you to sign in again'},
    # What the owner reads when the check turns the token down (onboarding.connect): plain words and what to do.
    'errors': {'shortcut_signin_expired': ('Shortcut didn’t accept that sign-in', 'sign in with Shortcut again'),
               'shortcut_http:HTTP_401': ('Shortcut didn’t accept that token', 'copy it again from Shortcut and paste it here'),
               'shortcut_http:HTTP_403': ('Shortcut didn’t accept that token', 'copy it again from Shortcut and paste it here'),
               'shortcut_credential_unavailable': ('That doesn’t look like a Shortcut token', 'copy it again from Shortcut and paste it here'),
               'shortcut_network': ('Shortcut didn’t answer', 'try again in a minute'),
               'account_identity_mismatch': ('That token is for another Shortcut workspace', 'add it as another Shortcut account')},
}
BASE = 'https://api.app.shortcut.com'
PREFIX = '/api/v3/'
PAGES = 3
LIMIT = 25
# Shortcut's OAuth token endpoint (its authorization server metadata at BASE/.well-known/oauth-authorization-server)
OAUTH_TOKEN = BASE + '/oauth-authorization-code-flow/token'
REFRESH_EARLY = 120  # seconds before the access token runs out that it is refreshed
TOKEN = re.compile(r'[\x21-\x7e]{8,4000}')  # Shortcut's sign-in tokens are opaque: any printable text without spaces


def expires_at(answer):
    """When the access token runs out, epoch seconds: expires_in, else Shortcut's access_token_expires_at (ISO 8601). 0: not said."""
    seconds = answer.get('expires_in')
    if isinstance(seconds, (int, float)) and not isinstance(seconds, bool) and seconds > 0:
        return int(time.time() + seconds)
    stamp = answer.get('access_token_expires_at')
    if isinstance(stamp, str):
        try:
            when = dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
            return int((when if when.tzinfo else when.replace(tzinfo=dt.timezone.utc)).timestamp())
        except ValueError:
            pass
    return 0


def signin(secret):
    """The sign-in from Sign in with Shortcut ({client_id, access_token, refresh_token?, expires_at?}), or None for a
    pasted token."""
    if not secret.startswith('{'):
        return None
    try:
        value = json.loads(secret)
    except ValueError:
        return None
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) and TOKEN.fullmatch(value[k]) for k in ('client_id', 'access_token')) \
            or not isinstance(value.get('refresh_token', ''), str) or (value.get('refresh_token') and not TOKEN.fullmatch(value['refresh_token'])) \
            or not isinstance(value.get('expires_at', 0), (int, float)):
        return None
    return value


def timestamp(value, helpers):
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError
        return parsed.astimezone(dt.timezone.utc)
    except (ValueError, TypeError, AttributeError):
        raise helpers.SourceError('shortcut_invalid_timestamp') from None


def plain(value):
    value = html.unescape(re.sub(r'<[^>]*>', '', str(value or '')))
    return re.sub(r'(?i)\b(password|passcode|one[- ]time code|verification code|otp)\s*[:=]\s*\S+',
                  r'\1: [omitted]', value)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the credential to a redirect target.


class Source:
    def __init__(self, config, account, helpers):
        self.helpers, self.account = helpers, account
        # Empty while connecting: verify() takes it from the token. Once saved, the token must stay in that workspace.
        workspace = account.get('workspace', '')
        if not isinstance(workspace, str):
            raise helpers.SourceError('shortcut_invalid_workspace')
        match = re.fullmatch(r'https://app\.shortcut\.com/([a-zA-Z0-9_-]+)(?:/[^?#]*)?/?', workspace)
        self.workspace = match[1] if match else workspace
        if self.workspace and not re.fullmatch(r'[a-zA-Z0-9_-]+', self.workspace):
            raise helpers.SourceError('shortcut_invalid_workspace')
        self.config, self.name = config, account.get('credential', 'shortcut')
        secret = helpers.credential(config, self.name)
        if not isinstance(secret, str):
            raise helpers.SourceError('shortcut_credential_unavailable')
        secret = secret.strip()
        self.signin = signin(secret)
        if self.signin is None and (not secret or not re.fullmatch(r'[A-Za-z0-9_-]+', secret)):
            raise helpers.SourceError('shortcut_credential_unavailable')
        self.headers = {'Accept': 'application/json', 'User-Agent': 'TheMachine/1'}
        self.headers.update({'Authorization': 'Bearer ' + self.signin['access_token']} if self.signin else {'Shortcut-Token': secret})
        self.opener = urllib.request.build_opener(NoRedirect())
        if self.signin and self.signin.get('expires_at') and self.signin['expires_at'] - REFRESH_EARLY < time.time():
            self.refresh()

    def refresh(self):
        """A new access token for the sign-in, from Shortcut's token endpoint (public client: the client id, no secret),
        kept in the credential file. A sign-in that can't be refreshed any more: shortcut_signin_expired."""
        if not self.signin.get('refresh_token'):
            raise self.helpers.SourceError('shortcut_signin_expired')
        form = urllib.parse.urlencode({'grant_type': 'refresh_token', 'refresh_token': self.signin['refresh_token'],
                                       'client_id': self.signin['client_id']}).encode()
        request = urllib.request.Request(OAUTH_TOKEN, data=form, method='POST', headers={
            'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json', 'User-Agent': 'TheMachine/1'})
        try:
            with self.opener.open(request, timeout=30) as response:
                answer = json.loads(response.read(200_001))
        except urllib.error.HTTPError as error:
            if error.code in (400, 401):
                raise self.helpers.SourceError('shortcut_signin_expired', error.code) from None
            raise self.helpers.SourceError('shortcut_http', error.code) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('shortcut_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('shortcut_invalid_json') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        if not isinstance(access, str) or not TOKEN.fullmatch(access):
            raise self.helpers.SourceError('shortcut_signin_expired')
        rotated = answer.get('refresh_token')
        self.signin = {**self.signin, 'access_token': access,
                       **({'refresh_token': rotated} if isinstance(rotated, str) and TOKEN.fullmatch(rotated) else {}),
                       'expires_at': expires_at(answer)}
        self.headers['Authorization'] = 'Bearer ' + access
        self.keep()

    def keep(self):
        """The refreshed sign-in, written over the credential file (mode 600, replaced whole). A credential handed in by
        the service manager (CREDENTIALS_DIRECTORY) is read-only: then only this run uses the new token."""
        directory = os.environ.get('CREDENTIALS_DIRECTORY')
        if directory and (Path(directory) / self.name).exists():
            return
        place = (self.config.get('credentials') or {}).get(self.name)
        if not place:
            return
        path = Path(place).expanduser()
        fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name + '.')
        try:
            with os.fdopen(fd, 'w') as handle:
                handle.write(json.dumps(self.signin, separators=(',', ':')) + '\n')
            os.chmod(temp, 0o600)
            os.replace(temp, path)
        except OSError:
            if os.path.exists(temp):
                os.unlink(temp)
            raise self.helpers.SourceError('shortcut_credential_unwritable') from None

    def get(self, path, again=True):
        # Only these read endpoints are allowed, including server-provided continuations.
        parts = urllib.parse.urlsplit(path)
        if parts.scheme or parts.netloc or parts.fragment or not (
                parts.path in (PREFIX + 'member', PREFIX + 'search/stories')
                or re.fullmatch(PREFIX + r'stories/[1-9][0-9]*/history', parts.path)):
            raise self.helpers.SourceError('shortcut_path_not_allowed')
        try:
            request = urllib.request.Request(BASE + path, headers=self.headers, method='GET')
            with self.opener.open(request, timeout=30) as response:
                raw = response.read(10_000_001)
            if len(raw) > 10_000_000:
                raise self.helpers.SourceError('shortcut_response_too_large')
            return json.loads(raw)
        except urllib.error.HTTPError as error:
            if error.code == 401 and self.signin and again:  # ran out early, or revoked: one refresh, then it says so
                self.refresh()
                return self.get(path, again=False)
            if error.code == 401 and self.signin:
                raise self.helpers.SourceError('shortcut_signin_expired', 401) from None
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            delay = min(3600, max(1, int(retry))) if retry.isdigit() else (60 if error.code == 429 else None)
            raise self.helpers.SourceError('shortcut_http', error.code, retry_after=delay) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('shortcut_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('shortcut_invalid_json') from None

    def verify(self):
        """GET /member: who the token belongs to and in which workspace. A new account takes that workspace; a saved one
        refuses a token from another. Keeps the workspace and the names to show on the account (never the token)."""
        member = self.get(PREFIX + 'member')
        if not isinstance(member, dict) or not member.get('id') or not isinstance(member.get('workspace2'), dict):
            raise self.helpers.SourceError('shortcut_invalid_member')
        space = member['workspace2']
        slug = space.get('url_slug')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-zA-Z0-9_-]+', slug):
            raise self.helpers.SourceError('shortcut_invalid_member')
        if self.workspace and slug != self.workspace:
            raise self.helpers.SourceError('account_identity_mismatch')
        self.workspace = slug
        name = ' '.join(plain(member.get('name') or member.get('mention_name')).split())[:100]
        self.account.update(workspace=slug, workspace_name=' '.join(plain(space.get('name')).split())[:100] or slug,
                            **({'member_name': name} if name else {}))
        return member


def continuation(value, helpers):
    if not value:
        return None
    if not isinstance(value, str):
        raise helpers.SourceError('shortcut_invalid_cursor')
    # The API returns a path and query string, not an arbitrary URL or endpoint.
    parts = urllib.parse.urlsplit(value)
    if parts.scheme or parts.netloc or parts.fragment or parts.path != PREFIX + 'search/stories' or not parts.query:
        raise helpers.SourceError('shortcut_invalid_cursor')
    return value


def moves(source, story, window, member, helpers):
    if not isinstance(story, dict) or type(story.get('id')) is not int or story['id'] <= 0:
        raise helpers.SourceError('shortcut_invalid_story')
    if (not isinstance(story.get('owner_ids', []), list)
            or any(not isinstance(owner, str) for owner in story.get('owner_ids', []))):
        raise helpers.SourceError('shortcut_invalid_story')
    history = source.get(PREFIX + f"stories/{story['id']}/history")
    if not isinstance(history, list):
        raise helpers.SourceError('shortcut_invalid_history')
    events = []
    for item in history:
        if not isinstance(item, dict) or not item.get('id') or not isinstance(item.get('actions'), list):
            raise helpers.SourceError('shortcut_invalid_history')
        stamp = timestamp(item.get('changed_at'), helpers)
        if not timestamp(window['since'], helpers) <= stamp <= timestamp(window['until'], helpers):
            continue
        refs = item.get('references') or []
        if not isinstance(refs, list) or any(not isinstance(r, dict) for r in refs):
            raise helpers.SourceError('shortcut_invalid_history')
        names = {r.get('id'): plain(r.get('name')) for r in refs if r.get('entity_type') == 'workflow-state'}
        for action in item['actions']:
            if not isinstance(action, dict):
                raise helpers.SourceError('shortcut_invalid_history')
            if action.get('entity_type') != 'story' or action.get('id') != story['id']:
                continue
            changes = action.get('changes') or {}
            if not isinstance(changes, dict):
                raise helpers.SourceError('shortcut_invalid_history')
            change = changes.get('workflow_state_id')
            if change is None:
                continue
            if not isinstance(change, dict) or any(type(change.get(k)) is not int for k in ('old', 'new')):
                raise helpers.SourceError('shortcut_invalid_move')
            old, new = change['old'], change['new']
            if old == new:
                continue
            before, after = names.get(old) or str(old), names.get(new) or str(new)
            title = plain(action.get('name') or story.get('name') or 'Story')
            body = '\n'.join([f'Moved: {before} → {after}',
                              'Current story context (may be newer than this move):',
                              f"Current state ID: {story.get('workflow_state_id', '')}",
                              f"Owner IDs: {', '.join(story.get('owner_ids') or [])}",
                              f"Requested by: {story.get('requested_by_id') or ''}",
                              f"Deadline: {story.get('deadline') or ''}",
                              f"Blocked: {bool(story.get('blocked'))}; completed: {bool(story.get('completed'))}",
                              plain(story.get('description'))])
            key = f"{story['id']}:{item['id']}:{old}:{new}"
            events.append({'account_id': source.account['id'], 'source_id': hashlib.sha256(key.encode()).hexdigest(),
                           'kind': 'shortcut.move', 'occurred_at': stamp.isoformat(), 'title': title[:1000],
                           'body': plain(body)[:40000], 'deleted': False,
                           'metadata': {'source_url': f"https://app.shortcut.com/{source.workspace}/story/{story['id']}",
                                        'story_id': story['id'], 'history_id': item['id'],
                                        'previous_state_id': old, 'state_id': new,
                                        'previous_state': before, 'state': after,
                                        'owner_ids': story.get('owner_ids') or [], 'deadline': story.get('deadline'),
                                        'from': item.get('member_id') or '',
                                        'sender_display': plain(item.get('actor_name')),
                                        'from_me': bool(item.get('member_id')) and item['member_id'] == member['id']}})
    return events


def read_as(kind, title, body, metadata):
    """How a move reads in the message viewer: the move, what is set on the story and its text, without the ids and
    the bookkeeping around them (the owners, the state and who asked come as ids)."""
    shown = []
    for line in str(body or '').split('\n'):
        if re.fullmatch(r'Current story context \(.*\):|Current state ID: ?\d*|Owner IDs:.*|Requested by:(?: [0-9a-f-]{36})? ?|Deadline: ?|Moved: \d+ → .*|Moved: .* → \d+', line):
            continue
        if found := re.fullmatch(r'Moved: (.+) → (.+)', line):
            line = i18n.t('Moved from {} to {}', found[1], found[2])
        elif found := re.fullmatch(r'Deadline: (\d{4}-\d\d-\d\d).*', line):
            line = i18n.t('Deadline: {}', locale_prefs.day_text(dt.date.fromisoformat(found[1])))
        elif found := re.fullmatch(r'Blocked: (True|False); completed: (?:True|False)', line):
            line = i18n.t('Blocked') + '\n' if found[1] == 'True' else ''  # a blank line before its text
        shown.append(line)
    text = '\n'.join(shown)
    return {'body': re.sub(r'\n{3,}', '\n\n', text).strip('\n')}


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    member = source.verify()
    state = copy.deepcopy(store.checkpoint(account['id']) or {})
    now = timestamp(helpers.now(), helpers)

    def fresh():
        since = timestamp(state['since'], helpers) - dt.timedelta(days=1) if state.get('since') else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
        return {'since': since.isoformat(), 'until': now.isoformat()}

    window = state.get('catchup') or fresh()
    count = read = 0
    reset = False
    seen = set()
    for _ in range(PAGES):
        query = 'moved:' + timestamp(window['since'], helpers).date().isoformat() + '..*'
        path = continuation(window.get('cursor'), helpers) or PREFIX + 'search/stories?' + urllib.parse.urlencode(
            {'query': query, 'page_size': LIMIT, 'detail': 'full'})
        try:
            page = source.get(path)
        except helpers.SourceError as error:
            if error.status in (400, 422) and window.get('cursor') and not reset:
                # Expired search snapshots restart a bounded recent window; replay is idempotent.
                window, reset = fresh(), True
                query = 'moved:' + timestamp(window['since'], helpers).date().isoformat() + '..*'
                page = source.get(PREFIX + 'search/stories?' + urllib.parse.urlencode(
                    {'query': query, 'page_size': LIMIT, 'detail': 'full'}))
            else:
                raise
        if not isinstance(page, dict) or not isinstance(page.get('data'), list):
            raise helpers.SourceError('shortcut_invalid_page')
        # Shortcut caps search at 1000 results. Never claim complete coverage if it truncates.
        if not isinstance(page.get('total'), int) or page['total'] > 1000:
            raise helpers.SourceError('shortcut_search_limit')
        cursor = continuation(page.get('next'), helpers)
        if cursor and (not page['data'] or cursor == window.get('cursor') or cursor in seen):
            raise helpers.SourceError('shortcut_invalid_cursor')
        events = []
        for story in page['data']:
            events.extend(moves(source, story, window, member, helpers))
        count += len(events)
        read += len(page['data'])
        more = bool(cursor)
        if more:
            seen.add(cursor)
            window['cursor'] = cursor
            state['catchup'] = window
        else:
            state['since'] = window['until']
            state.pop('catchup', None)
        state.update(mode='incremental', coverage_complete=not more,
                     coverage='Shortcut story history pages are still being collected.' if more else 'Shortcut pipeline moves caught up.')
        store.commit_page(account['id'], state, events)
        if not more:
            break
    return {'mode': 'incremental', 'events': count, 'read': read, 'more': more}


def check(config, account, helpers):
    """Verify workspace access, with no store or checkpoint writes."""
    Source(config, account, helpers).verify()

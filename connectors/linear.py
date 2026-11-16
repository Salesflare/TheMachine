"""Linear as a connection: issues assigned to the owner, mentions, comments on their issues, review and triage requests
and due dates come in; a comment, a state or assignee change and a new issue go out, each only after the owner's OK.

What comes in (each an event, linked to people by their Linear address), from Linear's GraphQL API:
- linear.issue: an issue assigned to the owner, new or with a changed state, due date or title, with its due date,
  state and priority. Once Linear says it is done (a state of type completed or canceled) the same event says so and
  its to-do closes by itself (Store.close_done_linear).
- From the owner's own Linear inbox (notifications), by Linear's category for it, never by the words in it:
  linear.mention (mentions), linear.comment (comments and replies on issues they follow: theirs, or ones they are in),
  linear.review (reviews), linear.triage (triage) and linear.due (reminders: a due date coming up or passed).
  Assignment notifications are left to linear.issue; reactions, status changes and the rest stay in Linear.
Whether one needs the owner is the to-do review's call, by what it says, like every other signal.
The first sync goes back 7 days (bootstrap_days); later ones overlap two hours.

Two ways in:
- Sign in with Linear (the usual one): The Machine's OAuth app, through the hosting control plane, which exchanges the
  code (PKCE and the app's client secret) and hands the result here sealed, as the credential, JSON:
  {access_token, refresh_token?, expires_at, scope}. Linear's access tokens last a day; a refresh needs the client
  secret, which only the control plane has, so it goes through it (POST /api/linear/token hosted, <Network>/linear-token
  paired): it uses the refresh token for that one call and keeps nothing. Linear rotates the refresh token; the new pair
  is kept here, in the same private credential file. Tokens are opaque: any printable text without spaces.
- A pasted personal API key (the fallback), from Linear's Settings, Security & access. It goes as the Authorization
  header without "Bearer", as Linear asks.

Scopes: read and write. write is what a state or assignee change needs, and it covers comments and new issues, so
nothing narrower would do all four; a sign-in without it only reads.

Abilities (abilities.py): Brings in signals is the sync. Can do things: the writes in linear_writes.py, each only after
the owner's OK on exactly that: a comment on an issue of the to-do, its state or assignee changed, a new issue. Every
call is one of the fixed operations below (READS, WRITES); nothing else is ever sent."""
import datetime as dt
import hashlib
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

from machine import kinds as kind_rows

KINDS = {kind: row['name'] for kind, row in kind_rows.KINDS.items() if row['service'] == 'linear'}  # machine/kinds.py says
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {kind: 'card' for kind in KINDS}
APP = 'Linear'
TOKEN_URL = 'https://linear.app/settings/account/security'
SETUP = {
    'label': 'Linear',
    'what': 'Issues, mentions, reviews and due dates. Changes wait for your OK.',
    'account': {'id': 'linear', 'service': 'linear', 'transport': 'api', 'boundary': 'work', 'credential': 'linear',
                'poll_seconds': 300},
    # Sign in with Linear answers this same prompt with its sign-in (JSON); pasting a personal API key is the fallback.
    # No workspace to type: the key says which one it is (viewer.organization).
    'secret': 'Linear API key',
    'token_url': TOKEN_URL,
    # Signed in at the hosting control plane (hosted: its account page; self-hosted: paired, from Connections, + Add)
    'account_page': 'source-linear',
    'note': 'Sign in with Linear from Connections, + Add. Or make a personal API key in Linear under Settings, '
            'Security & access, and paste it here.',
    'hints': {'linear_signin_expired': 'Linear asks you to sign in again'},
    'errors': {'linear_signin_expired': ('Linear didn’t accept that sign-in', 'sign in with Linear again'),
               'linear_http:HTTP_401': ('Linear didn’t accept that key', 'copy it again from Linear and paste it here'),
               'linear_unauthorized': ('Linear didn’t accept that key', 'copy it again from Linear and paste it here'),
               'linear_credential_unavailable': ('That doesn’t look like a Linear API key', 'copy it again from Linear and paste it here'),
               'linear_network': ('Linear didn’t answer', 'try again in a minute'),
               'account_identity_mismatch': ('That key is for another Linear workspace', 'add it as another Linear account')},
}
API = 'https://api.linear.app/graphql'
REFRESH_EARLY = 300  # seconds before the access token runs out that it is refreshed
TOKEN = re.compile(r'[\x21-\x7e]{8,4000}')  # Linear's tokens and keys are opaque: any printable text without spaces
UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
IDENTIFIER = re.compile(r'[A-Z][A-Z0-9_]{0,9}-[1-9][0-9]{0,8}')
OVERLAP_HOURS = 2
PAGE = 50
MAX_PAGES = 4        # inbox and assigned-issue pages per run
MAX_TEXT = 4000      # of an issue's description or a comment, in an event
SEEN_KEEP = 2000
DONE_TYPES = ('completed', 'canceled')
# Linear's own category for an inbox item -> the kind it comes in as. Assignments come in through the assigned issues.
CATEGORIES = {'mentions': 'linear.mention', 'commentsAndReplies': 'linear.comment', 'reviews': 'linear.review',
              'triage': 'linear.triage', 'reminders': 'linear.due'}
# For a Linear that sends no category yet: its notification type, the same split
TYPES = {'issueMention': 'linear.mention', 'issueCommentMention': 'linear.mention', 'issueNewComment': 'linear.comment',
         'issueAddedToTriage': 'linear.triage', 'issueDue': 'linear.due', 'issueReminder': 'linear.due'}

USER = 'id name displayName email'
ISSUE = 'id identifier title url description dueDate priorityLabel updatedAt state { id name type } team { id key name } ' \
        'assignee { ' + USER + ' } creator { ' + USER + ' }'
# Every call this connector makes, by name: the reads, and the writes only linear_writes.py runs after the owner's OK
READS = {
    'Viewer': 'query Viewer { viewer { ' + USER + ' organization { id name urlKey } } }',
    'Inbox': 'query Inbox($first: Int!, $after: String, $since: DateTimeOrDuration!) { notifications(first: $first, after: $after, '
             'filter: { createdAt: { gt: $since } }, orderBy: createdAt) { nodes { id type createdAt readAt archivedAt '
             '... on IssueNotification { category actor { ' + USER + ' } issue { ' + ISSUE + ' } '
             'comment { id body url createdAt user { ' + USER + ' } parent { id body user { ' + USER + ' } } } } } '
             'pageInfo { hasNextPage endCursor } } }',
    'Assigned': 'query Assigned($first: Int!, $after: String, $since: DateTimeOrDuration!) { viewer { assignedIssues(first: $first, '
                'after: $after, filter: { updatedAt: { gt: $since } }, orderBy: updatedAt) { nodes { ' + ISSUE + ' } '
                'pageInfo { hasNextPage endCursor } } } }',
    'Issue': 'query Issue($id: String!) { issue(id: $id) { ' + ISSUE + ' } }',
    'Comment': 'query Comment($id: String!) { comment(id: $id) { id body url issue { id } } }',
    'Teams': 'query Teams { teams(first: 100) { nodes { id key name } } }',
    'TeamStates': 'query TeamStates($id: String!) { team(id: $id) { id key name states(first: 100) { nodes { id name type position } } } }',
    'TeamMembers': 'query TeamMembers($id: String!) { team(id: $id) { id members(first: 250) { nodes { ' + USER + ' } } } }',
}
WRITES = {
    'CommentCreate': 'mutation CommentCreate($input: CommentCreateInput!) { commentCreate(input: $input) { success comment { id url } } }',
    'IssueUpdate': 'mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success '
                   'issue { id identifier url state { id name type } assignee { ' + USER + ' } } } }',
    'IssueCreate': 'mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier url title } } }',
}


def expires_at(answer):
    """When the access token runs out, epoch seconds: expires_in, else an expires_at the answer gives. 0: not said."""
    seconds = answer.get('expires_in')
    if isinstance(seconds, (int, float)) and not isinstance(seconds, bool) and seconds > 0:
        return int(time.time() + seconds)
    stamp = answer.get('expires_at')
    if isinstance(stamp, (int, float)) and not isinstance(stamp, bool) and stamp > 0:
        return int(stamp)
    return 0


def scopes(value):
    """Linear's scope, as a set: a space- or comma-separated string, or (an app made before December 2023) a list."""
    if isinstance(value, list):
        return {str(s).strip() for s in value if str(s).strip()}
    return {s for s in re.split(r'[\s,]+', str(value or '')) if s}


def signin(secret):
    """The sign-in from Sign in with Linear, or None for a pasted key."""
    if not secret.startswith('{'):
        return None
    try:
        value = json.loads(secret)
    except ValueError:
        return None
    if not isinstance(value, dict) or not isinstance(value.get('access_token'), str) or not TOKEN.fullmatch(value['access_token']) \
            or not isinstance(value.get('refresh_token', ''), str) or (value.get('refresh_token') and not TOKEN.fullmatch(value['refresh_token'])) \
            or not isinstance(value.get('expires_at', 0), (int, float)) or isinstance(value.get('expires_at', 0), bool):
        return None
    return value


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def short_id(*parts):
    return hashlib.sha256('\x00'.join(str(p) for p in parts).encode()).hexdigest()[:32]


def oneline(text, size=1000):
    return ' '.join(str(text or '').split())[:size]


def clip(text, size=MAX_TEXT):
    text = str(text or '').strip()
    return text if len(text) <= size else text[:size].rstrip() + '…'


def person(user):
    """(name, email) of a Linear user: their full name, else their display name; the address when it is one."""
    user = user if isinstance(user, dict) else {}
    email = str(user.get('email') or '').strip().lower()
    return oneline(user.get('name') or user.get('displayName'), 120), (email if re.fullmatch(r'[^@\s<>]{1,64}@[^@\s<>]{1,253}', email) else '')


def sender(name, email):
    return f'{name} <{email}>' if name and email else email or name


def issue_name(issue):
    """"ENG-12 Fix the export", as Linear lists it."""
    return oneline(f"{issue.get('identifier') or ''} {issue.get('title') or ''}", 300) or 'Linear issue'


def done(issue):
    return str(((issue or {}).get('state') or {}).get('type') or '') in DONE_TYPES


def refresh_place(config, helpers):
    """(url, credential name) where this Machine refreshes a Linear sign-in: its own control plane. Hosted: its broker's
    host, with its broker credential. Self-hosted and paired: the Network, with its own device token."""
    if config.get('manage_url'):
        base = (config.get('google_broker') or {}).get('url') or config['manage_url']
        parts = urllib.parse.urlsplit(str(base))
        if parts.scheme != 'https' or not parts.netloc:
            raise helpers.SourceError('linear_signin_expired')
        return f'https://{parts.netloc}/api/linear/token', 'google-broker'
    import fleet  # noqa: PLC0415
    home = fleet.settings(config)
    if not home or not str(home.get('url') or '').startswith('https://') or not (config.get('credentials') or {}).get('fleet'):
        raise helpers.SourceError('linear_signin_expired')
    return home['url'].rstrip('/') + '/linear-token', 'fleet'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the credential to a redirect target.


def error_codes(answer):
    """The extensions codes of a GraphQL answer's errors (AUTHENTICATION_ERROR, RATELIMITED, FORBIDDEN, ...)."""
    errors = answer.get('errors') if isinstance(answer, dict) else None
    return {str(((e or {}).get('extensions') or {}).get('code') or '').upper() for e in errors or () if isinstance(e, dict)} - {''}


class Source:
    """Linear's GraphQL API with the owner's sign-in or key: only READS, and WRITES for linear_writes.py."""

    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        self.name = account.get('credential', 'linear')
        try:
            secret = helpers.credential(config, self.name)
        except Exception:  # noqa: BLE001 - no file yet: the prompt asks for it
            raise helpers.SourceError('linear_credential_unavailable') from None
        secret = str(secret or '').strip()
        self.signin = signin(secret)
        if self.signin is None and not TOKEN.fullmatch(secret):
            raise helpers.SourceError('linear_credential_unavailable')
        self.key = None if self.signin else secret
        self.opener = urllib.request.build_opener(NoRedirect())
        if self.signin and self.signin.get('expires_at') and self.signin['expires_at'] - REFRESH_EARLY < time.time():
            self.refresh()

    def authorization(self):
        # OAuth: a Bearer token. A personal API key goes as is (Linear's own rule for keys).
        return 'Bearer ' + self.signin['access_token'] if self.signin else self.key

    def ops(self):
        """The changes this sign-in may make, by its scopes: comments:create a comment, issues:create a state or
        assignee change and a new issue (Linear: "creating and updating issues"), write all of them. A pasted key's own
        permissions are Linear's to say when it writes."""
        everything = {'comment', 'state', 'assign', 'create'}
        if not self.signin:
            return everything
        granted = scopes(self.signin.get('scope'))
        if not granted or granted & {'write', 'admin'}:
            return everything
        return ({'comment'} if 'comments:create' in granted else set()) | \
            ({'state', 'assign', 'create'} if 'issues:create' in granted else set())

    def can_write(self):
        return bool(self.ops())

    def refresh(self):
        """A new access token from the control plane (it holds the app's secret and keeps nothing), kept in the
        credential file. A sign-in that can't be refreshed any more: linear_signin_expired."""
        if not self.signin or not self.signin.get('refresh_token'):
            raise self.helpers.SourceError('linear_signin_expired')
        url, name = refresh_place(self.config, self.helpers)
        try:
            bearer = str(self.helpers.credential(self.config, name)).strip()
        except Exception:  # noqa: BLE001
            raise self.helpers.SourceError('linear_signin_expired') from None
        request = urllib.request.Request(url, method='POST', data=json.dumps({'refresh_token': self.signin['refresh_token']}).encode(),
                                         headers={'Authorization': 'Bearer ' + bearer, 'Content-Type': 'application/json',
                                                  'Accept': 'application/json'})
        try:
            with self.opener.open(request, timeout=30) as response:
                answer = json.loads(response.read(200_001))
        except urllib.error.HTTPError as error:
            error.close()
            if error.code in (400, 401, 404, 409):
                raise self.helpers.SourceError('linear_signin_expired', error.code) from None
            raise self.helpers.SourceError('linear_http', error.code, retry_after=60 if error.code == 429 else None) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('linear_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('linear_invalid_json') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        if not isinstance(access, str) or not TOKEN.fullmatch(access):
            raise self.helpers.SourceError('linear_signin_expired')
        rotated = answer.get('refresh_token')
        granted = answer.get('scope')
        self.signin = {**self.signin, 'access_token': access,
                       **({'refresh_token': rotated} if isinstance(rotated, str) and TOKEN.fullmatch(rotated) else {}),
                       **({'scope': ' '.join(sorted(scopes(granted)))} if granted else {}),
                       'expires_at': expires_at(answer)}
        self.keep()

    def keep(self):
        """The refreshed sign-in, written over the credential file (mode 600, replaced whole). One handed in by the
        service manager (CREDENTIALS_DIRECTORY) is read-only: then only this run uses the new token."""
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
            raise self.helpers.SourceError('linear_credential_unwritable') from None

    def call(self, operation, variables=None, write=False, again=True):
        """One named operation (READS, or WRITES when write) and its data. GraphQL errors: by their code."""
        query = (WRITES if write else READS).get(operation)
        if not query:
            raise self.helpers.SourceError('linear_operation_not_allowed')
        data = json.dumps({'query': query, 'variables': variables or {}, 'operationName': operation}, ensure_ascii=False).encode()
        request = urllib.request.Request(API, method='POST', data=data, headers={
            'Authorization': self.authorization(), 'Content-Type': 'application/json', 'Accept': 'application/json',
            'User-Agent': 'TheMachine/1'})
        answer = None
        try:
            with self.opener.open(request, timeout=30) as response:
                raw = response.read(10_000_001)
            if len(raw) > 10_000_000:
                raise self.helpers.SourceError('linear_response_too_large', route=operation)
            answer = json.loads(raw)
        except urllib.error.HTTPError as error:
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            try:
                answer = json.loads(error.read(200_001) or b'{}')
            except (ValueError, UnicodeError, OSError, http.client.HTTPException):
                answer = {}
            error.close()
            codes = error_codes(answer)
            if error.code == 401 or 'AUTHENTICATION_ERROR' in codes:
                return self.unauthorized(operation, variables, write, again)
            if error.code == 429 or 'RATELIMITED' in codes:
                delay = min(3600, max(1, int(retry))) if retry.isdigit() else 60
                raise self.helpers.SourceError('linear_http', 429, retry_after=delay, route=operation) from None
            if 'FORBIDDEN' in codes or error.code == 403:
                raise self.helpers.SourceError('linear_forbidden', 403, route=operation) from None
            if error.code == 400 and isinstance(answer, dict) and answer.get('errors'):  # a GraphQL error: entity not found, bad input
                raise self.helpers.SourceError('linear_graphql_error', 400, route=operation) from None
            raise self.helpers.SourceError('linear_http', error.code, route=operation) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('linear_network', route=operation) from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('linear_invalid_json', route=operation) from None
        if not isinstance(answer, dict):
            raise self.helpers.SourceError('linear_invalid_json', route=operation)
        codes = error_codes(answer)
        if 'AUTHENTICATION_ERROR' in codes:
            return self.unauthorized(operation, variables, write, again)
        if 'RATELIMITED' in codes:
            raise self.helpers.SourceError('linear_http', 429, retry_after=60, route=operation)
        if 'FORBIDDEN' in codes:
            raise self.helpers.SourceError('linear_forbidden', 403, route=operation)
        if answer.get('errors') and not isinstance(answer.get('data'), dict):
            raise self.helpers.SourceError('linear_graphql_error', 400, route=operation)
        return answer.get('data') if isinstance(answer.get('data'), dict) else {}

    def unauthorized(self, operation, variables, write, again):
        if self.signin and again:  # ran out early: one refresh, then it says so
            self.refresh()
            return self.call(operation, variables, write, again=False)
        if self.signin:
            raise self.helpers.SourceError('linear_signin_expired', 401, route=operation)
        raise self.helpers.SourceError('linear_unauthorized', 401, route=operation)

    # ------------------------------------------------------------------------------------------- who and where
    def verify(self):
        """viewer: who the sign-in or key belongs to, and in which workspace. A new account takes that workspace; a saved
        one refuses one from another. Keeps the workspace's name for the card, and the owner (never the token)."""
        me = (self.call('Viewer') or {}).get('viewer')
        org = (me or {}).get('organization') if isinstance(me, dict) else None
        if not isinstance(me, dict) or not isinstance(me.get('id'), str) or not isinstance(org, dict) or not isinstance(org.get('id'), str):
            raise self.helpers.SourceError('linear_invalid_viewer')
        if self.account.get('workspace_id') and self.account['workspace_id'] != org['id']:
            raise self.helpers.SourceError('account_identity_mismatch')
        if self.account.get('member_id') and self.account['member_id'] != me['id']:
            raise self.helpers.SourceError('account_identity_mismatch')
        name, email = person(me)
        key = str(org.get('urlKey') or '')
        self.account.update(workspace_id=org['id'], workspace_name=oneline(org.get('name'), 100) or key or 'Linear', member_id=me['id'],
                            **({'workspace': key} if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', key) else {}),
                            **({'member_name': name} if name else {}), **({'member_email': email} if email else {}))
        return {'id': me['id'], 'name': name, 'email': email}

    def pages(self, operation, since, path):
        """Every node of a paged read since `since`, at most MAX_PAGES pages: (nodes, complete)."""
        found, after = [], None
        for _ in range(MAX_PAGES):
            data = self.call(operation, {'first': PAGE, 'after': after, 'since': since.isoformat().replace('+00:00', 'Z')})
            for step in path:
                data = (data or {}).get(step) if isinstance(data, dict) else None
            if not isinstance(data, dict):
                raise self.helpers.SourceError('linear_invalid_page', route=operation)
            found += [n for n in data.get('nodes') or () if isinstance(n, dict) and n.get('id')]
            info = data.get('pageInfo') or {}
            after = info.get('endCursor')
            if not info.get('hasNextPage') or not after:
                return found, True
        return found, False

    # ------------------------------------------------------------------------------------------- for the writes
    def one(self, operation, field, node_id):
        """One issue or comment by its id; None when Linear has none (it answers a missing one with an error, not null)."""
        try:
            found = (self.call(operation, {'id': node_id}) or {}).get(field)
        except self.helpers.SourceError as error:
            if error.category == 'linear_graphql_error':
                return None
            raise
        return found if isinstance(found, dict) and found.get('id') else None

    def issue(self, issue_id):
        return self.one('Issue', 'issue', issue_id)

    def teams(self):
        return [t for t in ((self.call('Teams') or {}).get('teams') or {}).get('nodes') or () if isinstance(t, dict) and t.get('id')]

    def states(self, team_id):
        team = (self.call('TeamStates', {'id': team_id}) or {}).get('team') or {}
        return sorted((s for s in (team.get('states') or {}).get('nodes') or () if isinstance(s, dict) and s.get('id')),
                      key=lambda s: s.get('position') or 0)

    def members(self, team_id):
        team = (self.call('TeamMembers', {'id': team_id}) or {}).get('team') or {}
        return [u for u in (team.get('members') or {}).get('nodes') or () if isinstance(u, dict) and u.get('id')]

    def comment(self, comment_id):
        return self.one('Comment', 'comment', comment_id)


# ------------------------------------------------------------------------------------------- events

def event(account, kind, key, at, title, body, meta, reviewed=False):
    return {'account_id': account['id'], 'source_id': kind.split('.')[1] + ':' + key, 'kind': kind, 'occurred_at': at,
            'title': oneline(title or 'Linear issue', 1000), 'body': str(body or '')[:40000], 'metadata': meta, 'deleted': False,
            **({'reviewed': True} if reviewed else {})}


def issue_meta(account, issue):
    state = issue.get('state') or {}
    team = issue.get('team') or {}
    link = str(issue.get('url') or '')
    return {'provider': 'linear', 'issue_id': issue['id'], 'identifier': str(issue.get('identifier') or ''),
            'issue_title': oneline(issue.get('title'), 300), 'team_id': str(team.get('id') or ''), 'team': oneline(team.get('name'), 100),
            'state': oneline(state.get('name'), 60), 'state_type': str(state.get('type') or ''), 'due': issue.get('dueDate') or None,
            'done': done(issue), 'to': account.get('member_email') or '', **({'source_url': link} if link.startswith('https://') else {})}


def facts(issue):
    """One line on where an issue stands: its state, due date, priority and assignee."""
    state = oneline((issue.get('state') or {}).get('name'), 60)
    who = person(issue.get('assignee'))[0]
    parts = ([f'Status: {state}.'] if state else []) + ([f"Due {issue['dueDate']}."] if issue.get('dueDate') else []) \
        + ([f"Priority: {issue['priorityLabel']}."] if issue.get('priorityLabel') and issue['priorityLabel'] != 'No priority' else []) \
        + ([f'Assigned to {who}.'] if who else ['Not assigned.'])
    return ' '.join(parts)


def assigned_events(account, owner, issues, tasks, start):
    """linear.issue events: an issue assigned to the owner that is new, or whose state, due date or title changed."""
    out = []
    for issue in issues:
        if ((issue.get('assignee') or {}).get('id')) != owner:
            continue
        mark = [str((issue.get('state') or {}).get('name') or ''), issue.get('dueDate') or '', short_id(issue.get('title')), done(issue)]
        before = tasks.get(issue['id'])
        if before == mark:
            continue
        tasks[issue['id']] = mark
        if before is None and mark[3]:
            continue  # done before it was ever seen: nothing to do
        at = stamp(issue.get('updatedAt'))
        head = 'Assigned to you in Linear.' if before is None else 'Your Linear issue changed.'
        body = head + ' ' + facts(issue) + (' Done in Linear.' if mark[3] else '') \
            + ('\n\n' + clip(issue.get('description')) if issue.get('description') and before is None else '')
        creator = person(issue.get('creator'))
        out.append(event(account, 'linear.issue', issue['id'] + ':' + short_id(*mark)[:12], (at or start).isoformat(), issue_name(issue), body,
                         {**issue_meta(account, issue), 'task': True,
                          **({'from': sender(*creator), 'from_name': creator[0]} if creator[0] and issue.get('creator', {}).get('id') != owner else {}),
                          **({'from_email': creator[1]} if creator[1] and issue.get('creator', {}).get('id') != owner else {})},
                         reviewed=bool(before is not None and (mark[3] or before[3]))))
    return out


def inbox_events(account, owner, items, seen, now):
    """Events from the owner's Linear inbox, by Linear's category for each item: mentions, comments, reviews, triage and
    due-date reminders. Never one the owner caused, nor one already brought in."""
    out = []
    for item in items:
        kind = CATEGORIES.get(str(item.get('category') or '')) or TYPES.get(str(item.get('type') or ''))
        issue = item.get('issue') if isinstance(item.get('issue'), dict) else None
        if not kind or not issue or not issue.get('id') or item['id'] in seen:
            continue
        actor = item.get('actor') if isinstance(item.get('actor'), dict) else {}
        if actor.get('id') == owner:
            continue
        seen[item['id']] = 1
        name, email = person(actor)
        comment = item.get('comment') if isinstance(item.get('comment'), dict) else {}
        said = clip(comment.get('body'))
        parent = comment.get('parent') if isinstance(comment.get('parent'), dict) else {}
        earlier = f"{person(parent.get('user'))[0] or 'Someone'}: {clip(parent.get('body'), 1500)}\n\n" if parent.get('body') else ''
        who = name or 'Someone'
        body = {'mention': f'{earlier}{who}: {said}' if said else f'{who} mentioned you on this issue.',
                'comment': f'{earlier}{who}: {said}' if said else f'{who} commented on this issue.',
                'review': f'{who} asked for your review.' + (f'\n\n{said}' if said else ''),
                'triage': f'New in triage{(" from " + name) if name else ""}.' + (f"\n\n{clip(issue.get('description'))}" if issue.get('description') else ''),
                'due': 'Due date reminder.'}[kind.partition('.')[2]]
        link = str(comment.get('url') or issue.get('url') or '')
        at = stamp(item.get('createdAt'))
        out.append(event(account, kind, item['id'], (at or now).isoformat(), issue_name(issue),
                         body + '\n\n' + facts(issue),
                         {**issue_meta(account, issue), 'notification_id': item['id'], 'notification_type': str(item.get('type') or ''),
                          **({'comment_id': comment['id']} if comment.get('id') else {}),
                          **({'from': sender(name, email), 'from_name': name} if name or email else {}),
                          **({'from_email': email} if email else {}), **({'source_url': link} if link.startswith('https://') else {})}))
    return out


def trim(mapping, keep):
    return dict(list(mapping.items())[-keep:]) if len(mapping) > keep else mapping


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    owner = source.verify()['id']
    state = dict(store.checkpoint(account['id']) or {})
    now = stamp(helpers.now())
    since = stamp(state.get('since'))
    start = (since - dt.timedelta(hours=OVERLAP_HOURS)) if since else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    seen, tasks = dict(state.get('seen') or {}), dict(state.get('tasks') or {})
    assigned, whole = source.pages('Assigned', start, ('viewer', 'assignedIssues'))
    items, complete = source.pages('Inbox', start, ('notifications',))
    events = assigned_events(account, owner, assigned, tasks, start) + inbox_events(account, owner, items, seen, now)
    more = not (whole and complete)
    state.update(seen=trim(seen, SEEN_KEEP), tasks=trim(tasks, 1000), coverage_complete=not more,
                 writes=sorted(writes_on(config, account, helpers, source)), provider='linear',
                 coverage='Linear catching up.' if more else 'Linear caught up.')
    if not more:
        state['since'] = now.isoformat()
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events), 'more': more}


def check(config, account, helpers):
    """A real read without storing anything: the sign-in or key works and says whose it is, in which workspace."""
    Source(config, account, helpers).verify()


def refresh(store, config, account, helpers):
    """An action-only connection (Brings in signals off): nothing read, only what it may do, kept for its card."""
    state = dict(store.checkpoint(account['id']) or {})
    state.update(provider='linear', writes=sorted(writes_on(config, account, helpers)), coverage='Action-only: nothing synced.')
    store.commit_page(account['id'], state, [], record_sync=False)


def writes_on(config, account, helpers, source=None):
    """What a Linear connection may do after the owner's OK: comment, change state or assignee, create an issue. A
    sign-in with only read only reads; a Fleet-shared one only reads."""
    if account.get('shared'):
        return set()
    if source is None:
        try:
            source = Source(config, account, helpers)
        except Exception:  # noqa: BLE001 - no credential yet: nothing it may do
            return set()
    return source.ops()


# ------------------------------------------------------------------------------------------- the writes

class Writer(Source):
    """The writes linear_writes.py runs, each after the owner's OK on exactly that. Each carries its own id (a comment's
    or a new issue's, made from the approval), so a retry can never make a second one."""

    def __init__(self, config, account, helpers):
        if account.get('shared'):
            raise helpers.SourceError('linear_writes_unsupported')
        super().__init__(config, account, helpers)
        if not self.can_write():
            raise helpers.SourceError('linear_writes_unsupported')

    def post_comment(self, issue_id, body, comment_id, parent_id=None):
        done_ = (self.call('CommentCreate', {'input': {'id': comment_id, 'issueId': issue_id, 'body': body,
                                                       **({'parentId': parent_id} if parent_id else {})}}, write=True) or {}).get('commentCreate') or {}
        return done_.get('comment') if done_.get('success') else None

    def update(self, issue_id, change):
        done_ = (self.call('IssueUpdate', {'id': issue_id, 'input': change}, write=True) or {}).get('issueUpdate') or {}
        return done_.get('issue') if done_.get('success') else None

    def create(self, issue_id, team_id, title, description='', assignee_id=None):
        done_ = (self.call('IssueCreate', {'input': {'id': issue_id, 'teamId': team_id, 'title': title,
                                                     **({'description': description} if description else {}),
                                                     **({'assigneeId': assignee_id} if assignee_id else {})}}, write=True) or {}).get('issueCreate') or {}
        return done_.get('issue') if done_.get('success') else None

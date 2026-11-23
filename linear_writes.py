"""Owner-approved Linear changes (connectors/linear.py): a comment on an issue, its state or assignee changed, a new issue.

How: a to-do offers one as a next action {kind: 'linear', op: ...}; the card shows exactly what it does, and it runs
only after the owner's confirm. Which issues: only the ones this to-do's own Linear events are about. Which states and
people: the issue's team's, read from Linear while the to-do is prepared, so a name that doesn't fit is refused before
the owner ever sees it. A new issue goes to one of the connection's teams, in the to-do's area (Work or Personal).

Each write carries an id made from the approval (a comment's, a new issue's), so a retry or a lost answer never makes
a second one; an unclear outcome is checked by reading Linear back, never by writing again."""
from __future__ import annotations

import hashlib
import json
import re
import uuid

import doc_writes
from machine.owner_error import OwnerError

KIND = 'linear'
SERVICE = 'linear'
OPS = ('comment', 'state', 'assign', 'create')
KEYS = {'kind', 'op', 'label', 'account_id', 'issue', 'body', 'reply_to', 'state', 'assignee', 'team', 'title', 'description'}
MAX_BODY = 10_000
MAX_TITLE = 250
MAX_DESCRIPTION = 20_000
UNCLEAR = 'I couldn’t confirm the Linear change. I’m checking Linear; I won’t make it twice.'


def _text(value, field, limit, newlines=True):
    if not isinstance(value, str) or '\x00' in value or not value.strip():
        raise OwnerError(f'{field} is text')
    if len(value) > limit:
        raise OwnerError(f'{field} is at most {limit} characters')
    return value.strip() if newlines else ' '.join(value.split())


def _key(value):
    return ' '.join(str(value or '').split()).casefold()


def issues_of(db, event_ids):
    """The Linear issues this to-do's own events are about: {issue_id: {account_id, identifier, title, team_id, state,
    url?, comment_ids}}: the latest event's facts, and every comment the events bring."""
    found = {}
    for account_id, kind, raw in db.execute("SELECT e.account_id,e.kind,e.metadata FROM events e JOIN json_each(?) ids ON ids.value=e.id "
                                            "WHERE e.kind LIKE 'linear.%' ORDER BY e.occurred_at", (event_ids,)):
        m = json.loads(raw or '{}')
        if not m.get('issue_id'):
            continue
        before = found.get(str(m['issue_id'])) or {}
        link = m.get('source_url') if kind == 'linear.issue' else before.get('url') or m.get('source_url')
        found[str(m['issue_id'])] = {'account_id': account_id, 'identifier': str(m.get('identifier') or ''),
                                     'title': str(m.get('issue_title') or ''), 'team_id': str(m.get('team_id') or ''),
                                     'state': str(m.get('state') or ''), **({'url': link} if link else {}),
                                     'comment_ids': before.get('comment_ids', []) + ([m['comment_id']] if m.get('comment_id') else [])}
    return found


def accounts(config, connector, helpers, area=None, home=()):
    """The owner's own Linear connections in this to-do's area that may write: {account_id: {name, writes}}. Those its
    own issues came in on (home) too, wherever its area is, for those issues only (outside: never a new issue)."""
    import abilities  # noqa: PLC0415 - abilities imports next_actions, which imports this module
    out = {}
    for a in (config or {}).get('accounts') or ():
        if a.get('service') != SERVICE or a.get('shared') or not abilities.actions_on(a):
            continue
        inside = doc_writes.fits(a.get('boundary'), area)
        if not inside and a['id'] not in home:
            continue
        writes = connector.writes_on(config, a, helpers) if connector else set()
        if writes:
            out[a['id']] = {'name': str(a.get('display_name') or a.get('workspace_name') or 'Linear'), 'writes': sorted(writes),
                            **({} if inside else {'outside': True})}
    return out


def context(config, connector, helpers, issues, value, area=None):
    """What validate needs, read now: the to-do's issues, the connections that may write, and for the ops asked for, the
    team's states, people or teams, straight from Linear."""
    ops = [a for a in (value if isinstance(value, list) else [value]) if isinstance(a, dict) and a.get('kind') == KIND]
    home = {i['account_id'] for i in (issues or {}).values()}
    found = {'issues': issues or {}, 'accounts': accounts(config, connector, helpers, area, home) if ops else {}, 'states': {},
             'members': {}, 'teams': {}}
    if not ops or not connector:
        return found
    sources = {}

    def source(account_id):
        if account_id not in sources:
            account = next(a for a in config['accounts'] if a['id'] == account_id)
            sources[account_id] = connector.Source(config, account, helpers)
        return sources[account_id]
    for op in ops:
        try:
            if op.get('op') in ('state', 'assign'):
                issue = pick_issue(found['issues'], op.get('issue'))
                if issue and issue['account_id'] in found['accounts'] and issue['team_id']:
                    key = (issue['account_id'], issue['team_id'])
                    if op['op'] == 'state' and key not in found['states']:
                        found['states'][key] = source(issue['account_id']).states(issue['team_id'])
                    if op['op'] == 'assign' and key not in found['members']:
                        found['members'][key] = source(issue['account_id']).members(issue['team_id'])
            if op.get('op') == 'create':
                account_id = create_account(found, op)
                if account_id and account_id not in found['teams']:
                    found['teams'][account_id] = source(account_id).teams()
                    for team in found['teams'][account_id] if op.get('assignee') else ():
                        found['members'].setdefault((account_id, team['id']), None)
        except helpers.SourceError:
            raise OwnerError('I couldn’t reach Linear to check that. Try again in a minute.') from None
        except OwnerError:
            raise
    for key, people in list(found['members'].items()):
        if people is None:
            found['members'][key] = source(key[0]).members(key[1])
    return found


def pick_issue(issues, wanted):
    """The to-do's issue an action names, by its id or its identifier (ENG-12); the only one when it names none."""
    if wanted in (None, '') and len(issues) == 1:
        issue_id = next(iter(issues))
        return {'id': issue_id, **issues[issue_id]}
    text = str(wanted or '').strip()
    for issue_id, issue in issues.items():
        if text and (text == issue_id or text.upper() == issue['identifier'].upper()):
            return {'id': issue_id, **issue}
    return None


def create_account(found, value):
    inside = [k for k, a in found['accounts'].items() if not a.get('outside')]
    if value.get('account_id'):
        return value['account_id'] if value['account_id'] in inside else None
    linked = {i['account_id'] for i in found['issues'].values() if i['account_id'] in inside}
    if len(linked) == 1:
        return next(iter(linked))
    return inside[0] if len(inside) == 1 else None


def person_of(people, wanted, owner_id=None):
    """The one team member an assignee names: 'me', an address, or an exact full or display name. Never a guess."""
    text = _key(wanted)
    if text in ('me', 'myself', 'owner') and owner_id:
        found = [p for p in people if p.get('id') == owner_id]
    elif '@' in text:
        found = [p for p in people if _key(p.get('email')) == text]
    else:
        found = [p for p in people if text and text in (_key(p.get('name')), _key(p.get('displayName')))]
    if len(found) != 1:
        raise OwnerError(f'Name one person on the issue’s team for assignee: {str(wanted)[:80]} is not one of them'
                         if not found else f'{str(wanted)[:80]} fits more than one person on the team. Use their email address.')
    return found[0]


def validate(value, found, config=None):
    """A Linear change as the owner will see it, without a revision. `found` is context(): the to-do's issues, the
    connections that may write, and the teams' states, people and teams read just now."""
    value = dict(value)
    if set(value) - KEYS:
        raise ValueError('A Linear change has op, issue, body, reply_to, state, assignee, team, title, description and account_id')
    found = found or {'issues': {}, 'accounts': {}}
    op = value.get('op')
    if op not in OPS:
        raise ValueError('op is comment, state, assign or create')
    named = {'label': value['label']} if value.get('label') else {}  # next_actions.validate checked it
    return {**_validate(value, found, config, op), **named}


def _allowed(found, account_id, op):
    """A sign-in's scopes say which changes it may make: comments:create a comment, issues:create the rest."""
    if op not in (found['accounts'][account_id].get('writes') or ()):
        raise OwnerError('That Linear connection can’t make this change. Sign in with Linear again to allow it, after your OK.')


def _validate(value, found, config, op):
    if op == 'create':
        account_id = create_account(found, value)
        if not account_id:
            raise OwnerError('Connect Linear with permission to make changes, in this to-do’s area, to create an issue'
                             if all(a.get('outside') for a in found['accounts'].values()) else 'Say which Linear connection (account_id) the new issue goes to')
        _allowed(found, account_id, op)
        teams = (found.get('teams') or {}).get(account_id) or []
        wanted = _key(value.get('team'))
        team = next((t for t in teams if wanted and wanted in (_key(t.get('key')), _key(t.get('name')))), None) \
            or (teams[0] if len(teams) == 1 and not wanted else None)
        if not team:
            raise OwnerError('Name the Linear team for the new issue: ' + ', '.join(f"{t.get('name')} ({t.get('key')})" for t in teams[:20])
                             if teams else 'That Linear workspace has no team the connection can see')
        result = {'kind': KIND, 'op': op, 'account_id': account_id, 'workspace': found['accounts'][account_id]['name'],
                  'team_id': team['id'], 'team': str(team.get('name') or team.get('key')),
                  'title': _text(value.get('title'), 'title', MAX_TITLE, newlines=False)}
        if value.get('description') not in (None, ''):
            result['description'] = _text(value['description'], 'description', MAX_DESCRIPTION)
        if value.get('assignee') not in (None, ''):
            owner = next((a.get('member_id') for a in (config or {}).get('accounts') or () if a.get('id') == account_id), None)
            who = person_of((found.get('members') or {}).get((account_id, team['id'])) or [], value['assignee'], owner)
            result.update(assignee_id=who['id'], assignee=str(who.get('name') or who.get('displayName')))
        return result
    issue = pick_issue(found['issues'], value.get('issue'))
    if not issue:
        raise ValueError('issue is the id or identifier (like ENG-12) of a Linear issue this to-do’s own events are about')
    if issue['account_id'] not in found['accounts']:
        raise OwnerError('That Linear connection can only read. Sign in with Linear again to let it make changes, after your OK.')
    _allowed(found, issue['account_id'], op)
    result = {'kind': KIND, 'op': op, 'account_id': issue['account_id'], 'workspace': found['accounts'][issue['account_id']]['name'],
              'issue_id': issue['id'], 'identifier': issue['identifier'], 'issue_title': issue['title'], **({'url': issue['url']} if issue.get('url') else {})}
    if op == 'comment':
        result['body'] = _text(value.get('body'), 'body', MAX_BODY)
        if value.get('reply_to'):
            if value['reply_to'] not in (found['issues'].get(issue['id']) or {}).get('comment_ids', ()):
                raise ValueError('reply_to is the comment_id of a Linear comment this to-do’s own events are about')
            result['reply_to'] = value['reply_to']
        return result
    key = (issue['account_id'], issue['team_id'])
    if op == 'state':
        states = (found.get('states') or {}).get(key) or []
        wanted = _key(value.get('state'))
        state = next((s for s in states if wanted and _key(s.get('name')) == wanted), None)
        if not state:
            raise OwnerError('Use one of the team’s states: ' + ', '.join(str(s.get('name')) for s in states[:30]) if states
                             else 'I couldn’t read that team’s states in Linear')
        if _key(issue['state']) == _key(state.get('name')):
            raise OwnerError(f"{issue['identifier']} is {state.get('name')} already")
        result.update(state_id=state['id'], state=str(state['name']), was=issue['state'])
        return result
    owner = next((a.get('member_id') for a in (config or {}).get('accounts') or () if a.get('id') == issue['account_id']), None)
    who = person_of((found.get('members') or {}).get(key) or [], value.get('assignee'), owner)
    result.update(assignee_id=who['id'], assignee=str(who.get('name') or who.get('displayName')))
    return result


def label(action):
    return action.get('label') or {'comment': 'Post comment', 'state': 'Change status', 'assign': 'Reassign', 'create': 'Create issue'}[action['op']]


def where(action):
    return action.get('identifier') or 'the issue'


def done(action):
    """What happened, once it went through: "Commented on ENG-12 in Linear"."""
    return {'comment': lambda: f'Commented on {where(action)} in Linear',
            'state': lambda: f"Moved {where(action)} to {action['state']} in Linear",
            'assign': lambda: f"Assigned {where(action)} to {action['assignee']} in Linear",
            'create': lambda: f"Created “{action['title']}” in Linear"}[action['op']]()


def preview(action):
    head = f"{action.get('identifier', '')} {action.get('issue_title', '')}".strip()
    if action['op'] == 'comment':
        return f'Comment on {head} in Linear' + (', as a reply' if action.get('reply_to') else '') + '\n\n' + action['body']
    if action['op'] == 'state':
        return f"Move {head} to {action['state']}" + (f" (now {action['was']})" if action.get('was') else '')
    if action['op'] == 'assign':
        return f"Assign {head} to {action['assignee']}"
    lines = [f"New issue in {action['team']} ({action['workspace']})", action['title']]
    if action.get('assignee'):
        lines.append('Assignee: ' + action['assignee'])
    if action.get('description'):
        lines += ['', action['description']]
    return '\n'.join(lines)


def write_id(job, part):
    """A UUID made from the approved job: the same on every try of it, so Linear never makes a second one."""
    digest = hashlib.sha256(f"linear:{part}:{job['id']}".encode()).digest()[:16]
    return str(uuid.UUID(bytes=digest, version=4))


class LinearTransport:
    """Runs one approved Linear change: checks first (the connection may write, the issue is there), then one write.
    An unknown outcome is checked by reading Linear back, never by writing again."""

    def __init__(self, config, connector, helpers):
        self.config, self.connector, self.helpers = config, connector, helpers

    def writer(self, action):
        if action.get('kind') != KIND:
            raise OwnerError('Only an approved Linear change uses the Linear transport')
        account = next((a for a in self.config['accounts'] if a['id'] == action['account_id'] and a.get('service') == SERVICE), None)
        if not account:
            raise OwnerError('That Linear account is no longer connected. Nothing was changed.')
        try:
            return self.connector.Writer(self.config, account, self.helpers)
        except self.helpers.SourceError:
            raise OwnerError('That Linear connection can only read. Nothing was changed.') from None

    def preflight(self, action):
        writer = self.writer(action)
        if action['op'] == 'create':
            return
        try:
            issue = writer.issue(action['issue_id'])
        except self.helpers.SourceError:
            raise OwnerError('I couldn’t reach Linear. Nothing was changed; tap it again.') from None
        if not issue:
            raise OwnerError(f"{where(action)} is gone from Linear. Nothing was changed.")

    def send(self, action, job):
        writer = self.writer(action)
        try:
            if action['op'] == 'comment':
                made = writer.post_comment(action['issue_id'], action['body'], write_id(job, 'comment'), action.get('reply_to'))
            elif action['op'] == 'state':
                made = writer.update(action['issue_id'], {'stateId': action['state_id']})
            elif action['op'] == 'assign':
                made = writer.update(action['issue_id'], {'assigneeId': action['assignee_id']})
            else:
                made = writer.create(write_id(job, 'issue'), action['team_id'], action['title'], action.get('description', ''),
                                     action.get('assignee_id'))
        except self.helpers.SourceError as error:
            if error.status == 429:
                return {'not_sent': True}
            if error.status in (401, 403):
                return {'rejected': error.status}
            return {}  # unknown: reconcile reads Linear, never writes again
        if not made:
            return {}
        return {'message_id': 'linear:' + str(made.get('id') or action.get('issue_id')), **({'url': made['url']} if made.get('url') else {})}

    def reconcile(self, action, job):
        try:
            writer = self.writer(action)
            if action['op'] == 'comment':
                found = writer.comment(write_id(job, 'comment'))
                return {'message_id': 'linear:' + found['id']} if found else {}
            if action['op'] == 'create':
                found = writer.issue(write_id(job, 'issue'))
                return {'message_id': 'linear:' + found['id'], **({'url': found['url']} if found.get('url') else {})} if found else {}
            issue = writer.issue(action['issue_id'])
        except (ValueError, self.helpers.SourceError):
            return {}
        if not issue:
            return {}
        landed = ((issue.get('state') or {}).get('id') == action['state_id']) if action['op'] == 'state' \
            else ((issue.get('assignee') or {}).get('id') == action['assignee_id'])
        return {'message_id': 'linear:' + issue['id']} if landed else {}


def prompt(config):
    """The preparation's lines on Linear changes, when a connection in some area may make them."""
    if not any(a.get('service') == SERVICE and not a.get('shared') for a in (config or {}).get('accounts') or ()):
        return ''
    return ("\n- Linear: a change runs only after the owner's OK, as next action {kind:'linear', op, ...}. "
            "op:'comment' {issue, body, reply_to?} posts a comment on an issue this to-do's own Linear events are about "
            "(issue: its identifier like ENG-12 or its metadata.issue_id; reply_to: a metadata.comment_id to answer in its thread). "
            "op:'state' {issue, state} moves it to one of its team's states, by name. op:'assign' {issue, assignee} gives it to one "
            "person on its team: 'me', an email address or their exact name. op:'create' {team, title, description?, assignee?, "
            "account_id?} makes a new issue in one of the connection's teams (team: its key or name). Offer one only when the "
            "to-do needs it; the comment is written as the owner, in their words and language.")

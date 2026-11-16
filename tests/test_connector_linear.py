"""Linear tests: a made-up workspace served by a fake Linear GraphQL API, in the shapes Linear documents (POST /graphql
answering {data} or {errors[].extensions.code}; POST /oauth/token answering access_token, expires_in, scope, a rotated
refresh_token). No live calls; nothing sent or written anywhere."""
import copy
import json
import os
from pathlib import Path
import stat
import tempfile
import time
import types
import unittest
import urllib.error
from unittest.mock import patch

from connectors import linear
from test_connectors import Response
import graph
import linear_writes
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors
import next_actions
from machine.owner_error import OwnerError
import sources

NOW = '2026-11-16T12:00:00+00:00'
OWNER, ROBIN, KIT = 'u-owner', 'u-robin', 'u-kit'
ISSUE, OTHER_ISSUE, TEAM = '1a2b3c4d-0000-4000-8000-000000000001', '1a2b3c4d-0000-4000-8000-000000000002', 'team-eng'
PASTED = 'lin_api_' + 'x' * 40  # a made-up personal API key
SIGNIN = {'access_token': 'lin_oauth_fixture_access', 'refresh_token': 'lin_refresh_fixture', 'expires_at': 4102444800,
          'scope': 'read issues:create comments:create'}  # the narrow scopes the app asks
PEOPLE = {OWNER: {'id': OWNER, 'name': 'Owner Example', 'displayName': 'owner', 'email': 'owner@example.com'},
          ROBIN: {'id': ROBIN, 'name': 'Robin Example', 'displayName': 'robin', 'email': 'robin@partner.example'},
          KIT: {'id': KIT, 'name': 'Kit Navarro', 'displayName': 'kit', 'email': 'kit@example.com'}}
STATES = [{'id': 's-todo', 'name': 'Todo', 'type': 'unstarted', 'position': 1}, {'id': 's-doing', 'name': 'In Progress', 'type': 'started', 'position': 2},
          {'id': 's-done', 'name': 'Done', 'type': 'completed', 'position': 3}, {'id': 's-cancel', 'name': 'Canceled', 'type': 'canceled', 'position': 4}]


def issue(iid=ISSUE, ident='ENG-12', title='Fix the export', state='s-doing', assignee=OWNER, due='2026-11-20', updated='2026-11-16T09:00:00.000Z'):
    st = next(s for s in STATES if s['id'] == state)
    return {'id': iid, 'identifier': ident, 'title': title, 'url': f'https://linear.app/example/issue/{ident}/fix-the-export',
            'description': 'The CSV export drops the last row.', 'dueDate': due, 'priorityLabel': 'High', 'updatedAt': updated,
            'state': {k: st[k] for k in ('id', 'name', 'type')}, 'team': {'id': TEAM, 'key': 'ENG', 'name': 'Engineering'},
            'assignee': PEOPLE.get(assignee), 'creator': PEOPLE[ROBIN]}


def note(nid, category, ntype, actor=ROBIN, comment=None, of=None, at='2026-11-16T10:00:00.000Z'):
    return {'__typename': 'IssueNotification', 'id': nid, 'type': ntype, 'category': category, 'createdAt': at, 'readAt': None,
            'archivedAt': None, 'actor': PEOPLE.get(actor), 'issue': of or issue(), 'comment': comment}


class Linear:
    """The fake API: what it holds, and every request it got."""

    def __init__(self, test):
        self.test = test
        self.issues = {ISSUE: issue()}
        self.notifications = [
            note('n1', 'mentions', 'issueCommentMention', comment={'id': 'c1', 'body': 'Can you check this, @owner?', 'url': 'https://linear.app/example/issue/ENG-12#comment-c1',
                                                                   'createdAt': '2026-11-16T10:00:00.000Z', 'user': PEOPLE[ROBIN], 'parent': None}),
            note('n2', 'commentsAndReplies', 'issueNewComment', comment={'id': 'c2', 'body': 'Pushed a fix to staging.', 'url': None,
                                                                         'createdAt': '2026-11-16T10:05:00.000Z', 'user': PEOPLE[ROBIN],
                                                                         'parent': {'id': 'c0', 'body': 'Is this on staging?', 'user': PEOPLE[OWNER]}}),
            note('n3', 'reviews', 'issueReviewRequested'),
            note('n4', 'triage', 'issueAddedToTriage', of=issue(OTHER_ISSUE, 'ENG-13', 'Login loops on Safari', 's-todo', assignee=None, due=None)),
            note('n5', 'reminders', 'issueDue', actor=None),
            note('n6', 'assignments', 'issueAssignedToYou'),  # left to the assigned-issue scan
            note('n7', 'reactions', 'issueReaction'),  # stays in Linear
            note('n8', 'commentsAndReplies', 'issueNewComment', actor=OWNER),  # the owner's own
        ]
        self.comments, self.made, self.calls, self.refreshes = {}, [], [], []
        self.token, self.fail, self.revoked = 'Bearer lin_oauth_fixture_access', None, False

    def respond(self, request, timeout):
        self.test.assertEqual(timeout, 30)
        body = json.loads(request.data)
        if request.full_url != linear.API:  # the control plane's refresh: the refresh token only, with this Machine's own key
            self.test.assertEqual(request.full_url, 'https://app.example.test/api/linear/token')
            self.test.assertEqual(request.get_header('Authorization'), 'Bearer broker-fixture')
            self.refreshes.append(body)
            if self.revoked:
                raise urllib.error.HTTPError(request.full_url, 401, 'Unauthorized', {}, None)
            self.token = 'Bearer lin_oauth_fixture_new'
            # Linear's token answer: a day's token, its scope as a string, and a new refresh token (they rotate)
            return Response(json.dumps({'access_token': 'lin_oauth_fixture_new', 'token_type': 'Bearer', 'expires_in': 86399,
                                        'scope': 'read write', 'refresh_token': 'lin_refresh_rotated'}).encode())
        self.test.assertEqual(request.get_method(), 'POST')
        name = body['operationName']
        self.test.assertEqual(body['query'], {**linear.READS, **linear.WRITES}[name])  # only the fixed operations
        self.calls.append((name, body['variables']))
        if self.fail:
            code, status = self.fail
            self.fail = None
            raise urllib.error.HTTPError(linear.API, status, 'error', {'Retry-After': '7'} if code == 'RATELIMITED' else {},
                                         Response(json.dumps({'errors': [{'message': 'nope', 'extensions': {'code': code}}]}).encode()))
        if request.get_header('Authorization') != self.token:
            # Linear: an expired or revoked token is an AUTHENTICATION_ERROR
            raise urllib.error.HTTPError(linear.API, 400, 'Bad Request', {}, Response(json.dumps(
                {'errors': [{'message': 'Authentication required, not authenticated', 'extensions': {'code': 'AUTHENTICATION_ERROR'}}]}).encode()))
        return Response(json.dumps(self.answer(name, body['variables'])).encode())

    def answer(self, name, v):
        page = {'hasNextPage': False, 'endCursor': None}
        if name == 'Viewer':
            return {'data': {'viewer': {**PEOPLE[OWNER], 'organization': {'id': 'org-1', 'name': 'Example Team', 'urlKey': 'example'}}}}
        if name == 'Inbox':
            return {'data': {'notifications': {'nodes': [n for n in self.notifications if n['createdAt'] > v['since']], 'pageInfo': page}}}
        if name == 'Assigned':
            nodes = [i for i in self.issues.values() if (i['assignee'] or {}).get('id') == OWNER and i['updatedAt'] > v['since']]
            return {'data': {'viewer': {'assignedIssues': {'nodes': nodes, 'pageInfo': page}}}}
        if name == 'Issue':
            if v['id'] not in self.issues:
                return {'data': None, 'errors': [{'message': 'Entity not found: Issue', 'extensions': {'code': 'INVALID_INPUT'}}]}
            return {'data': {'issue': self.issues[v['id']]}}
        if name == 'Comment':
            found = self.comments.get(v['id'])
            return {'data': {'comment': found}} if found else {'data': None, 'errors': [{'message': 'Entity not found: Comment'}]}
        if name == 'Teams':
            return {'data': {'teams': {'nodes': [{'id': TEAM, 'key': 'ENG', 'name': 'Engineering'}]}}}
        if name == 'TeamStates':
            return {'data': {'team': {'id': TEAM, 'key': 'ENG', 'name': 'Engineering', 'states': {'nodes': STATES}}}}
        if name == 'TeamMembers':
            return {'data': {'team': {'id': TEAM, 'members': {'nodes': list(PEOPLE.values())}}}}
        self.made.append((name, v))
        if name == 'CommentCreate':
            made = {'id': v['input']['id'], 'body': v['input']['body'], 'url': 'https://linear.app/example/issue/ENG-12#comment-new', 'issue': {'id': v['input']['issueId']}}
            self.comments[made['id']] = made
            return {'data': {'commentCreate': {'success': True, 'comment': {'id': made['id'], 'url': made['url']}}}}
        if name == 'IssueUpdate':
            found = self.issues[v['id']]
            if 'stateId' in v['input']:
                st = next(s for s in STATES if s['id'] == v['input']['stateId'])
                found['state'] = {k: st[k] for k in ('id', 'name', 'type')}
            if 'assigneeId' in v['input']:
                found['assignee'] = PEOPLE[v['input']['assigneeId']]
            return {'data': {'issueUpdate': {'success': True, 'issue': found}}}
        if name == 'IssueCreate':
            made = issue(v['input']['id'], 'ENG-14', v['input']['title'], 's-todo', v['input'].get('assigneeId'))
            self.issues[made['id']] = made
            return {'data': {'issueCreate': {'success': True, 'issue': made}}}
        raise AssertionError(name)


class LinearTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.store = machine_main.Store(self.dir / 'events.sqlite')
        self.cred = self.dir / 'linear'
        self.cred.write_text(json.dumps(SIGNIN))
        (self.dir / 'broker').write_text('broker-fixture')
        self.account = copy.deepcopy(linear.SETUP['account'])
        self.config = {'accounts': [self.account], 'credentials': {'linear': str(self.cred), 'google-broker': str(self.dir / 'broker')},
                       'manage_url': 'https://app.example.test/account', 'database': str(self.dir / 'events.sqlite')}
        self.helpers = types.SimpleNamespace(SourceError=sources.SourceError, now=lambda: NOW,
                                             iso=machine_sources_connectors.CONNECTOR_HELPERS.iso, credential=sources.credential)
        self.api = Linear(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.api.respond).start()
        patch.dict(os.environ, {'MESSAGE_SEAL_AUDIT': '1'}).start()
        os.environ.pop('CREDENTIALS_DIRECTORY', None)
        self.addCleanup(patch.stopall)

    def sync(self):
        return linear.sync(self.store, self.config, self.account, self.helpers)

    def events(self):
        with self.store.connect() as db:
            return [{**dict(r), 'metadata': json.loads(r['metadata'])} for r in db.execute('SELECT * FROM events ORDER BY occurred_at,id')]

    def test_tokens_are_opaque_and_the_expiry_is_linears_own_field(self):
        self.assertEqual(linear.signin(json.dumps({**SIGNIN, 'access_token': 'lin_oauth_8f2e+/=.~x'}))['access_token'], 'lin_oauth_8f2e+/=.~x')
        self.assertIsNone(linear.signin('lin_api_' + 'x' * 40))  # a pasted key
        self.assertIsNone(linear.signin('{"access_token": "has space"}'))
        before = time.time()
        self.assertGreaterEqual(linear.expires_at({'access_token': 'a', 'expires_in': 86399}), int(before) + 86399)
        self.assertEqual(linear.expires_at({'expires_at': 4102444800}), 4102444800)
        self.assertEqual(linear.expires_at({}), 0)
        self.assertEqual(linear.scopes('read write'), {'read', 'write'})
        self.assertEqual(linear.scopes(['read', 'write']), {'read', 'write'})  # an app made before December 2023
        self.assertEqual(linear.scopes('read,issues:create'), {'read', 'issues:create'})
        self.cred.write_text('not a key')
        with self.assertRaises(sources.SourceError) as caught:
            linear.Source(self.config, self.account, self.helpers)
        self.assertEqual(caught.exception.category, 'linear_credential_unavailable')

    def test_a_pasted_key_goes_without_bearer(self):
        self.cred.write_text(PASTED)
        self.api.token = PASTED
        linear.check(self.config, self.account, self.helpers)
        self.assertEqual(self.account['workspace_name'], 'Example Team')
        self.assertEqual(linear.writes_on(self.config, self.account, self.helpers), {'comment', 'state', 'assign', 'create'})

    def test_first_sync_brings_in_what_may_need_the_owner_and_names_the_card_by_workspace(self):
        self.assertEqual(self.sync()['events'], 6)
        self.assertEqual(self.account['workspace_name'], 'Example Team')  # machine/names.py names the card by it, no ids
        self.assertEqual((self.account['member_id'], self.account['workspace']), (OWNER, 'example'))
        found = {e['kind']: e for e in self.events()}
        self.assertEqual(set(found), {'linear.issue', 'linear.mention', 'linear.comment', 'linear.review', 'linear.triage', 'linear.due'})
        mine = found['linear.issue']
        self.assertEqual(mine['title'], 'ENG-12 Fix the export')
        self.assertTrue(mine['body'].startswith('Assigned to you in Linear. Status: In Progress. Due 2026-11-20. Priority: High.'))
        self.assertEqual((mine['metadata']['due'], mine['metadata']['done'], mine['metadata']['identifier']), ('2026-11-20', False, 'ENG-12'))
        said = found['linear.mention']
        self.assertEqual((said['metadata']['comment_id'], said['metadata']['from']), ('c1', 'Robin Example <robin@partner.example>'))
        self.assertIn('Robin Example: Can you check this, @owner?', said['body'])
        self.assertIn('Owner Example: Is this on staging?', found['linear.comment']['body'])  # the comment it answers
        self.assertEqual(found['linear.triage']['title'], 'ENG-13 Login loops on Safari')
        self.assertTrue(found['linear.due']['body'].startswith('Due date reminder.'))
        self.assertEqual(self.api.made, [])  # it only reads
        self.assertEqual(self.sync()['events'], 0)  # the same again is nothing new
        self.assertEqual(self.store.checkpoint(self.account['id'])['writes'], ['assign', 'comment', 'create', 'state'])

    def test_an_expired_sign_in_refreshes_through_the_control_plane_and_keeps_the_rotated_token(self):
        self.cred.write_text(json.dumps({**SIGNIN, 'expires_at': int(time.time()) - 10}))
        self.sync()
        self.assertEqual(self.api.refreshes, [{'refresh_token': 'lin_refresh_fixture'}])
        kept = json.loads(self.cred.read_text())
        self.assertEqual((kept['access_token'], kept['refresh_token']), ('lin_oauth_fixture_new', 'lin_refresh_rotated'))
        self.assertGreater(kept['expires_at'], time.time() + 86000)
        self.assertEqual(stat.S_IMODE(self.cred.stat().st_mode), 0o600)

    def test_a_token_linear_stops_accepting_refreshes_once_then_asks_to_sign_in_again(self):
        self.api.token = 'Bearer lin_oauth_fixture_new'  # revoked early: AUTHENTICATION_ERROR, one refresh, then it works
        self.sync()
        self.assertEqual(len(self.api.refreshes), 1)
        self.api.token, self.api.revoked = 'Bearer something-else', True  # the control plane: Linear refused the refresh token
        with self.assertRaises(sources.SourceError) as caught:
            self.sync()
        self.assertEqual(caught.exception.category, 'linear_signin_expired')

    def test_rate_limits_wait_as_linear_says(self):
        self.api.fail = ('RATELIMITED', 400)
        with self.assertRaises(sources.SourceError) as caught:
            self.sync()
        self.assertEqual((caught.exception.status, caught.exception.retry_after), (429, 7))

    def test_a_read_only_or_shared_sign_in_does_nothing(self):
        self.cred.write_text(json.dumps({**SIGNIN, 'scope': 'read'}))
        self.assertEqual(linear.writes_on(self.config, self.account, self.helpers), set())
        with self.assertRaises(sources.SourceError):
            linear.Writer(self.config, self.account, self.helpers)
        self.cred.write_text(json.dumps({**SIGNIN, 'scope': 'read comments:create'}))
        self.assertEqual(linear.writes_on(self.config, self.account, self.helpers), {'comment'})
        self.cred.write_text(json.dumps({**SIGNIN, 'scope': 'read issues:create'}))
        self.assertEqual(linear.writes_on(self.config, self.account, self.helpers), {'state', 'assign', 'create'})
        self.cred.write_text(json.dumps(SIGNIN))
        self.assertEqual(linear.writes_on(self.config, self.account, self.helpers), {'comment', 'state', 'assign', 'create'})
        self.assertEqual(linear.writes_on(self.config, {**self.account, 'shared': True}, self.helpers), set())

    def test_an_issue_done_in_linear_closes_its_to_do_with_undo(self):
        self.sync()
        ids = [e['id'] for e in self.events() if e['kind'] in ('linear.issue', 'linear.mention')]
        sid = self.store.suggest('l1', 'Fix the export', 'Due Friday.', ids)['id']
        self.assertEqual(self.store.close_done_linear(), [])
        self.api.issues[ISSUE] = issue(state='s-done', updated='2026-11-16T11:30:00.000Z')
        self.sync()
        done = [e for e in self.events() if e['kind'] == 'linear.issue' and e['metadata']['done']]
        self.assertEqual(len(done), 1)
        self.assertIn('Done in Linear.', done[0]['body'])
        self.assertEqual(self.store.close_done_linear(), [sid])
        self.assertEqual(self.store.close_done_linear(), [])
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, self.config
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'completed')
            self.assertEqual([i['text'] for i in app.card_chat_service(db, sid)[0] if i['kind'] == 'event'], ['Done in Linear'])
        self.assertEqual(self.store.decide(sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertEqual(self.store.close_done_linear(), [])  # the same done never closes it again

    def test_people_link_to_the_graph_by_address_and_one_issue_is_one_thread(self):
        owner = types.SimpleNamespace(mine=lambda a: a == 'owner@example.com')
        found = graph._touches('linear.mention', {'from': 'Robin Example <robin@partner.example>', 'from_name': 'Robin Example'}, owner, set())
        self.assertEqual(found[0][:2], ('email:robin@partner.example', 'Robin Example'))
        self.assertEqual(graph._touches('linear.comment', {'from': 'Owner Example <owner@example.com>'}, owner, set()), [])
        self.assertEqual(graph.thread_key('linear.comment', {'issue_id': ISSUE}), ('linear:' + ISSUE, True))

    # ------------------------------------------------------------------------------------------- the writes
    def context(self, value):
        self.sync()
        with self.store.connect() as db:
            ids = json.dumps([e['id'] for e in self.events() if e['metadata'].get('issue_id') == ISSUE])
            issues = linear_writes.issues_of(db, ids)
        return linear_writes.context(self.config, linear, self.helpers, issues, value)

    def test_each_change_is_checked_against_linear_before_the_owner_sees_it(self):
        value = {'kind': 'linear', 'op': 'state', 'issue': 'ENG-12', 'state': 'done'}
        action = next_actions.validate(value, self.config, [self.account['id']], linear_context=self.context(value))
        self.assertEqual((action['state_id'], action['state'], action['was'], action['identifier']), ('s-done', 'Done', 'In Progress', 'ENG-12'))
        self.assertEqual(next_actions.label(action), 'Change status')
        self.assertIn('Move ENG-12 Fix the export to Done', next_actions.preview(action))
        with self.assertRaises(OwnerError) as caught:
            linear_writes.validate({'kind': 'linear', 'op': 'state', 'issue': 'ENG-12', 'state': 'Shipped'}, self.context(value))
        self.assertIn('Todo, In Progress, Done, Canceled', str(caught.exception))
        with self.assertRaises(ValueError):  # only an issue this to-do is about
            linear_writes.validate({'kind': 'linear', 'op': 'comment', 'issue': 'ENG-99', 'body': 'Hi'}, self.context(value))
        who = {'kind': 'linear', 'op': 'assign', 'issue': ISSUE, 'assignee': 'kit@example.com'}
        self.assertEqual(linear_writes.validate(who, self.context(who))['assignee_id'], KIT)
        with self.assertRaises(OwnerError):  # never a guess
            linear_writes.validate({**who, 'assignee': 'Kit N'}, self.context(who))
        made = {'kind': 'linear', 'op': 'create', 'team': 'ENG', 'title': 'Add a CSV test', 'assignee': 'me'}
        found = linear_writes.validate(made, self.context(made), self.config)
        self.assertEqual((found['team_id'], found['assignee_id'], found['workspace']), (TEAM, OWNER, 'Example Team'))
        self.assertEqual(self.api.made, [])  # checking writes nothing

    def test_an_approved_comment_posts_once_even_when_its_answer_is_lost(self):
        value = {'kind': 'linear', 'op': 'comment', 'issue': 'ENG-12', 'body': 'Thanks, checking it now.', 'reply_to': 'c1'}
        action = next_actions.validate(value, self.config, [self.account['id']], linear_context=self.context(value))
        transport = linear_writes.LinearTransport(self.config, linear, self.helpers)
        job = {'id': 'job-1'}
        self.assertEqual(transport.reconcile(action, job), {})  # not there yet: never assumed sent
        transport.preflight(action)
        sent = transport.send(action, job)
        self.assertTrue(sent['message_id'].startswith('linear:'))
        posted = self.api.made[0][1]['input']
        self.assertEqual((posted['issueId'], posted['parentId'], posted['body']), (ISSUE, 'c1', 'Thanks, checking it now.'))
        self.assertEqual(posted['id'], linear_writes.write_id(job, 'comment'))  # the same id on every try of this approval
        self.assertEqual(transport.reconcile(action, job), {'message_id': 'linear:' + posted['id']})
        self.assertEqual(linear_writes.done(action), 'Commented on ENG-12 in Linear')

    def test_status_assignee_and_new_issue_land_and_reconcile_by_reading_back(self):
        transport = linear_writes.LinearTransport(self.config, linear, self.helpers)
        for n, value in enumerate(({'kind': 'linear', 'op': 'state', 'issue': 'ENG-12', 'state': 'Done'},
                                   {'kind': 'linear', 'op': 'assign', 'issue': 'ENG-12', 'assignee': 'Robin Example'},
                                   {'kind': 'linear', 'op': 'create', 'team': 'Engineering', 'title': 'Add a CSV test'})):
            action = linear_writes.validate(value, self.context(value), self.config)
            job = {'id': f'job-{n}'}
            self.assertTrue(transport.send(action, job)['message_id'])
            self.assertTrue(transport.reconcile(action, job)['message_id'])
        self.assertEqual(self.api.issues[ISSUE]['state']['name'], 'Done')
        self.assertEqual(self.api.issues[ISSUE]['assignee']['id'], ROBIN)
        self.assertIn(linear_writes.write_id({'id': 'job-2'}, 'issue'), self.api.issues)

    def test_a_rate_limited_write_waits_and_a_refused_one_says_so(self):
        value = {'kind': 'linear', 'op': 'comment', 'issue': 'ENG-12', 'body': 'On it.'}
        action = linear_writes.validate(value, self.context(value))
        transport = linear_writes.LinearTransport(self.config, linear, self.helpers)
        self.api.fail = ('RATELIMITED', 400)
        self.assertEqual(transport.send(action, {'id': 'j'}), {'not_sent': True})
        self.api.fail = ('FORBIDDEN', 403)
        self.assertEqual(transport.send(action, {'id': 'j'}), {'rejected': 403})
        self.assertEqual(self.api.made, [])


if __name__ == '__main__':
    unittest.main()

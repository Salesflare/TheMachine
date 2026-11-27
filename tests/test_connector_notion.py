"""Notion tests: a made-up workspace served by a fake Notion API; no live calls, nothing sent or written anywhere."""
import copy
import json
import os
from pathlib import Path
import stat
import tempfile
import types
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

from connectors import notion
from test_connectors import Response
import doc_writes
import graph
import machine.main as machine_main
import machine.sources.connectors as machine_sources_connectors
from machine import todo_kinds
import sources

NOW = '2026-11-16T12:00:00+00:00'
OWNER, OTHER, BOT, THIRD = 'a' * 32, 'b' * 32, 'c' * 32, 'e' * 32
MINE, THEIRS, TASK, DB, ASKED, D1, D2, D3 = '1' * 32, '3' * 32, '4' * 32, '5' * 32, '6' * 32, '2' * 32, '7' * 32, '8' * 32
B1, B2 = '9' * 32, 'f' * 32
SIGNIN = {'access_token': 'ntn_fixture_access', 'refresh_token': 'ntn_fixture_refresh', 'expires_at': 4102444800,
          'bot_id': BOT, 'workspace_id': 'd' * 32, 'workspace_name': 'Example Team', 'owner_id': OWNER}
PEOPLE = {OWNER: ('Owner Example', 'owner@example.com'), OTHER: ('Robin Example', 'robin@partner.example'),
          THIRD: ('Kit Navarro', '')}


def user(uid):
    return {'object': 'user', 'id': uid}


def text(value, link=None, bold=False):
    return {'type': 'text', 'text': {'content': value, **({'link': {'url': link}} if link else {})}, 'plain_text': value,
            'annotations': {'bold': bold}}


def mention(uid, name):
    return {'type': 'mention', 'mention': {'type': 'user', 'user': user(uid)}, 'plain_text': '@' + name}


def page(pid, title, by, at='2026-11-15T09:00:00.000Z', edited='2026-11-15T10:00:00.000Z', edited_by=None, parent=None, props=None):
    return {'object': 'page', 'id': notion.dashed(pid), 'created_time': at, 'last_edited_time': edited,
            'created_by': user(by), 'last_edited_by': user(edited_by or by), 'url': f'https://www.notion.so/Example-{pid}',
            'parent': parent or {'type': 'workspace', 'workspace': True},
            'properties': {'title': {'type': 'title', 'title': [text(title)]}, **(props or {})}}


def comment(cid, discussion, by, runs, at='2026-11-15T11:00:00.000Z'):
    return {'object': 'comment', 'id': cid, 'discussion_id': notion.dashed(discussion), 'created_by': user(by),
            'created_time': at, 'last_edited_time': at, 'rich_text': runs}


def task(status='In progress', option='o1'):
    return page(TASK, 'Write the launch notes', OTHER, parent={'type': 'database_id', 'database_id': notion.dashed(DB)}, props={
        'Assignee': {'type': 'people', 'people': [user(OWNER)]},
        'Due': {'type': 'date', 'date': {'start': '2026-11-20'}},
        'Status': {'type': 'status', 'status': {'id': option, 'name': status}}})


SCHEMA = {'object': 'database', 'properties': {'Status': {'type': 'status', 'status': {
    'options': [{'id': 'o0', 'name': 'Not started'}, {'id': 'o1', 'name': 'In progress'}, {'id': 'o2', 'name': 'Shipped'}],
    'groups': [{'name': 'To-do', 'option_ids': ['o0']}, {'name': 'In progress', 'option_ids': ['o1']},
               {'name': 'Complete', 'option_ids': ['o2']}]}}}}


class Notion:
    """The fake API: what it holds, and every request it got."""

    def __init__(self, test):
        self.test = test
        self.pages = {MINE: page(MINE, 'Launch plan', OWNER), THEIRS: page(THEIRS, 'Partner brief', OTHER), TASK: task()}
        self.comments = {MINE: [comment('c1', D1, OTHER, [text('Can we move this to June?')])],
                         THEIRS: [comment('c2', D2, OTHER, [text('Thoughts, '), mention(OWNER, 'Owner Example'), text('?')])]}
        self.blocks = {MINE: [{'object': 'block', 'id': notion.dashed(B1), 'type': 'paragraph', 'last_edited_time': '2026-11-15T10:00:00.000Z',
                               'paragraph': {'rich_text': [text('We launch in '), text('May', bold=True), text(' with the '),
                                                           text('beta', link='https://example.com/beta'), text('.')]}},
                              {'object': 'block', 'id': notion.dashed(B2), 'type': 'heading_2', 'last_edited_time': '2026-11-15T10:00:00.000Z',
                               'heading_2': {'rich_text': [text('Next steps')]}}]}
        self.requests, self.writes, self.refreshes = [], [], []
        self.token = 'ntn_fixture_access'
        self.fail = {}  # (method, path, start_cursor or None) -> the HTTP status Notion answers it with

    def respond(self, request, timeout):
        self.test.assertEqual(timeout, 30)
        parts = urllib.parse.urlsplit(request.full_url)
        method, body = request.get_method(), json.loads(request.data) if request.data else None
        if parts.netloc != 'api.notion.com':  # the control plane's refresh: the refresh token only, with this Machine's own key
            self.test.assertEqual(request.full_url, 'https://app.example.test/api/notion/token')
            self.test.assertEqual(request.get_header('Authorization'), 'Bearer broker-fixture')
            self.refreshes.append(body)
            self.token = 'ntn_fixture_new'
            return Response(json.dumps({'access_token': 'ntn_fixture_new', 'refresh_token': 'ntn_fixture_rotated', 'expires_in': 3600}).encode())
        self.test.assertEqual(request.get_header('Notion-version'), notion.VERSION)
        if request.get_header('Authorization') != 'Bearer ' + self.token:
            raise urllib.error.HTTPError(request.full_url, 401, 'unauthorized', {}, None)
        path = parts.path[len('/v1/'):]
        query = dict(urllib.parse.parse_qsl(parts.query))
        self.requests.append((method, path))
        status = self.fail.get((method, path, (body or {}).get('start_cursor') or query.get('start_cursor')))
        if status:
            raise urllib.error.HTTPError(request.full_url, status, 'error', {}, None)
        if method != 'GET' and path != 'search':
            self.writes.append((method, path, body))
        return Response(json.dumps(self.answer(method, path, query, body)).encode())

    def answer(self, method, path, query, body):
        if path == 'users/me':
            return {'object': 'user', 'type': 'bot', 'id': BOT, 'bot': {'workspace_name': 'Example Team', 'owner': {
                'type': 'user', 'user': {'id': OWNER, 'name': 'Owner Example', 'person': {'email': 'owner@example.com'}}}}}
        if path.startswith('users/'):
            uid = notion.plain_id(path.split('/')[1])
            name, email = PEOPLE[uid]
            return {'object': 'user', 'type': 'person', 'id': uid, 'name': name, 'person': {'email': email} if email else {}}
        if path == 'users':
            return {'results': [{'object': 'user', 'type': 'person', 'id': u, 'name': n, 'person': {'email': e}}
                                for u, (n, e) in PEOPLE.items()], 'has_more': False}
        if path == 'search':
            found = sorted(self.pages.values(), key=lambda p: p['last_edited_time'], reverse=True)
            if body.get('query'):
                found = [p for p in found if body['query'].lower() in notion.page_title(p).lower()]
            return {'results': found, 'has_more': False, 'next_cursor': None}
        if path == 'comments' and method == 'GET':
            return {'results': self.comments.get(notion.plain_id(query['block_id']), []), 'has_more': False}
        if path == 'comments':
            made = comment(notion.dashed('cd' * 16), notion.plain_id(body['discussion_id']), BOT, body['rich_text'], at='2026-11-16T12:00:00.000Z')
            self.comments.setdefault(MINE, []).append(made)
            return made
        if path.startswith('databases/'):
            return SCHEMA
        if path.startswith('blocks/') and path.endswith('/children'):
            pid = notion.plain_id(path.split('/')[1])
            if method == 'PATCH':
                made = [{**b, 'id': notion.dashed(f'{i:032x}')} for i, b in enumerate(body['children'], 100)]
                self.blocks.setdefault(pid, []).extend(made)
                return {'results': made}
            return {'results': self.blocks.get(pid, []), 'has_more': False}
        if path.startswith('blocks/'):
            return {'object': 'block'}
        if path.startswith('pages/') and method == 'GET':
            return self.pages[notion.plain_id(path.split('/')[1])]
        if path.startswith('pages/'):
            return {'object': 'page'}
        if path == 'pages':
            return {'object': 'page', 'id': notion.dashed('ab' * 16), 'url': 'https://www.notion.so/New-' + 'ab' * 16}
        raise AssertionError(path)


class NotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.store = machine_main.Store(self.dir / 'events.sqlite')
        self.cred = self.dir / 'notion'
        self.cred.write_text(json.dumps(SIGNIN))
        (self.dir / 'broker').write_text('broker-fixture')
        self.account = copy.deepcopy(notion.SETUP['account'])
        self.config = {'accounts': [self.account], 'credentials': {'notion': str(self.cred), 'google-broker': str(self.dir / 'broker')},
                       'manage_url': 'https://app.example.test/account', 'database': str(self.dir / 'events.sqlite')}
        self.helpers = types.SimpleNamespace(SourceError=sources.SourceError, now=lambda: NOW,
                                             iso=machine_sources_connectors.CONNECTOR_HELPERS.iso, credential=sources.credential)
        self.api = Notion(self)
        patch('urllib.request.OpenerDirector.open', side_effect=self.api.respond).start()
        patch.dict(os.environ, {'MESSAGE_SEAL_AUDIT': '1'}).start()
        os.environ.pop('CREDENTIALS_DIRECTORY', None)
        self.addCleanup(patch.stopall)

    def sync(self):
        return notion.sync(self.store, self.config, self.account, self.helpers)

    def events(self):
        with self.store.connect() as db:
            return [{**dict(r), 'metadata': json.loads(r['metadata'])} for r in db.execute('SELECT * FROM events ORDER BY id')]

    def test_a_pages_text_names_the_files_on_it(self):
        self.api.blocks[MINE].append({'object': 'block', 'id': notion.dashed('ba' * 16), 'type': 'pdf', 'pdf': {
            'type': 'file', 'name': 'Offer.pdf', 'caption': [], 'file': {'url': 'https://files.example/signed'}}})
        text = notion.read_text(self.config, self.account, MINE, self.helpers)['text']
        self.assertIn('\n[file] Offer.pdf', text)
        self.assertNotIn('signed', text)

    def test_signin_or_pasted_token(self):
        self.assertEqual(notion.signin(json.dumps(SIGNIN))['bot_id'], BOT)
        self.assertIsNone(notion.signin('ntn_' + 'x' * 40))
        self.assertIsNone(notion.signin('{"access_token": "has space"}'))
        self.cred.write_text('not a token')
        with self.assertRaises(sources.SourceError) as caught:
            notion.Source(self.config, self.account, self.helpers)
        self.assertEqual(caught.exception.category, 'notion_credential_unavailable')

    def test_first_sync_brings_in_comments_mentions_and_tasks_and_names_the_card_by_workspace(self):
        self.assertEqual(self.sync()['events'], 3)
        self.assertEqual(self.account['workspace_name'], 'Example Team')  # machine/names.py names the card by it, no ids
        self.assertEqual(self.account['member_id'], OWNER)
        found = {e['kind']: e for e in self.events()}
        self.assertEqual(set(found), {'notion.comment', 'notion.mention', 'notion.task'})
        said = found['notion.comment']
        self.assertEqual((said['title'], said['metadata']['file_id'], said['metadata']['comment_id']), ('Launch plan', MINE, D1))
        self.assertEqual(said['metadata']['from'], 'Robin Example <robin@partner.example>')
        self.assertIn('Can we move this to June?', said['body'])
        self.assertTrue(found['notion.mention']['metadata']['mention'])
        work = found['notion.task']
        self.assertEqual(work['body'], 'Assigned to you in Notion. Due 2026-11-20. Status: In progress.')  # Calendar: the to-do's due date
        self.assertEqual((work['metadata']['due'], work['metadata']['done']), ('2026-11-20', False))
        self.assertFalse(any(m == 'POST' and p != 'search' for m, p in self.api.requests))  # it only reads
        self.assertEqual(self.sync()['events'], 0)  # the same again is nothing new
        # a page someone else adds after the first sync is news; the owner's own is not
        self.api.pages['ab' * 16] = page('ab' * 16, 'Partner pricing', OTHER, at='2026-11-16T11:00:00.000Z', edited='2026-11-16T11:00:00.000Z')
        # nor one this connection made itself (an approved new page)
        self.api.pages['ba' * 16] = page('ba' * 16, 'Draft the owner approved', BOT, at='2026-11-16T11:00:00.000Z', edited='2026-11-16T11:00:00.000Z')
        self.sync()
        added = [e for e in self.events() if e['kind'] == 'notion.page']
        self.assertEqual([e['title'] for e in added], ['Partner pricing'])

    def test_a_person_without_an_address_is_linked_only_by_a_full_name_one_graph_person_has(self):
        self.api.comments[MINE] = [comment('c3', D3, THIRD, [text('Looks good to me')])]
        self.sync()
        said = next(e for e in self.events() if e['kind'] == 'notion.comment')
        self.assertNotIn('from_email', said['metadata'])  # nobody in the Graph by that name yet: no link, no guess
        owner = types.SimpleNamespace(mine=lambda a: a == 'owner@example.com')
        found = graph._touches('notion.comment', {'from': 'Robin Example <robin@partner.example>', 'from_name': 'Robin Example'}, owner, set())
        self.assertEqual(found[0][:2], ('email:robin@partner.example', 'Robin Example'))
        self.assertEqual(graph._touches('notion.comment', {'from': 'Kit Navarro'}, owner, set()), [])
        self.assertEqual(graph.thread_key('notion.comment', {'file_id': MINE, 'comment_id': D1}), ('doc:' + MINE + ':' + D1, True))

    def test_a_task_done_in_notion_closes_its_to_do_with_undo(self):
        self.sync()
        event_id = next(e['id'] for e in self.events() if e['kind'] == 'notion.task')
        sid = self.store.suggest('n1', 'Write the launch notes', 'Due Friday.', [event_id])['id']
        self.assertEqual(self.store.close_done_notion(), [])
        self.api.pages[TASK] = task('Shipped', 'o2')
        self.api.pages[TASK]['last_edited_time'] = '2026-11-16T11:30:00.000Z'
        self.sync()
        self.assertTrue(next(e for e in self.events() if e['kind'] == 'notion.task')['metadata']['done'])
        self.assertEqual(self.store.close_done_notion(), [sid])
        self.assertEqual(self.store.close_done_notion(), [])
        app = object.__new__(machine_main.App)
        app.store, app.config = self.store, self.config
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()[0], 'completed')
            self.assertEqual([i['text'] for i in app.card_chat_service(db, sid)[0] if i['kind'] == 'event'], ['Done in Notion'])
        self.assertEqual(self.store.decide(sid, 'undo', '', 'u1', 'dashboard')['status'], 'pending')
        self.assertEqual(self.store.close_done_notion(), [])  # the same done never closes it again

    def test_a_page_gone_since_it_was_listed_is_set_aside_not_a_failed_round(self):
        # A page of the owner's, deleted or no longer shared with the integration after the search listed it: reading its
        # blocks answered 404 and raised notion_http:HTTP_404 as the round's failure. Left pending, it failed every round.
        self.api.fail[('GET', f'blocks/{MINE}/children', None)] = 404
        self.api.fail[('GET', 'databases/' + DB, None)] = 404  # the task's database no longer shared
        self.api.fail[('GET', 'users/' + OTHER, None)] = 404  # a person who left the workspace
        result = self.sync()
        self.assertFalse(result['more'])
        self.assertIsNone(self.store.checkpoint(self.account['id'])['cycle'])  # nothing left pending to fail on again
        self.assertEqual({e['kind'] for e in self.events()}, {'notion.comment', 'notion.mention', 'notion.task'})  # the rest is read
        self.api.pages[MINE]['last_edited_time'] = '2026-11-16T11:00:00.000Z'
        self.assertEqual(self.sync()['events'], 0)  # listed again, still gone: no failure either
        for status in (401, 429, 500):  # the sign-in's own and Notion's trouble stay the connection's
            self.api.fail[('GET', f'blocks/{MINE}/children', None)] = status
            self.api.pages[MINE]['last_edited_time'] = f'2026-11-16T11:{status % 60:02d}:00.000Z'
            with self.assertRaises(sources.SourceError):
                self.sync()

    def test_a_task_in_a_database_with_several_data_sources_is_still_read(self):
        # Notion refuses such a database to API version 2022-06-28 (400 validation_error). Reading the task's schema
        # raised notion_http:HTTP_400 as the round's failure, every round the task was listed.
        self.api.fail[('GET', 'databases/' + DB, None)] = 400
        self.assertEqual(self.sync()['events'], 3)
        work = next(e for e in self.events() if e['kind'] == 'notion.task')
        self.assertEqual((work['metadata']['status'], work['metadata']['done']), ('In progress', False))  # from its own properties
        self.api.pages[TASK] = task('Done', option='o9')
        self.api.pages[TASK]['last_edited_time'] = '2026-11-16T11:00:00.000Z'
        self.sync()
        self.assertTrue([e for e in self.events() if e['kind'] == 'notion.task'][-1]['metadata']['done'])  # done by its name
        self.api.fail[('GET', 'blocks/' + MINE + '/children', None)] = 400  # a 400 elsewhere stays the connection's
        self.api.pages[MINE]['last_edited_time'] = '2026-11-16T11:30:00.000Z'
        with self.assertRaises(sources.SourceError):
            self.sync()

    def test_a_search_cursor_notion_no_longer_takes_starts_the_search_over_once(self):
        self.store.commit_page(self.account['id'], {'cycle': {'at': '2026-11-16T11:00:00+00:00', 'cursor': 'run-out', 'pending': []}}, [])
        self.api.fail[('POST', 'search', 'run-out')] = 400
        self.assertEqual(self.sync()['events'], 3)
        self.assertEqual([r for r in self.api.requests if r[1] == 'search'], [('POST', 'search')] * 2)
        self.assertIsNone(self.store.checkpoint(self.account['id'])['cycle'])
        # a fresh search refused, or the kept cursor refused again after starting over: the connection's, no loop
        source = notion.Source(self.config, self.account, self.helpers)
        self.api.fail[('POST', 'search', None)] = 400
        self.api.requests.clear()
        for cursor in (None, 'run-out'):
            with self.assertRaises(sources.SourceError) as caught:
                source.pages(notion.stamp(NOW), cursor)
            self.assertEqual(caught.exception.status, 400)
        self.assertEqual(len(self.api.requests), 3)

    def test_a_page_the_owner_asked_to_change_being_changed_is_a_quiet_heads_up(self):
        self.api.pages[ASKED] = page(ASKED, 'Pricing page', OTHER)
        self.api.comments[ASKED] = [comment('c4', '0' * 31 + '1', OWNER, [text('Please update the prices')], at='2026-11-15T12:00:00.000Z')]
        self.sync()
        self.assertFalse([e for e in self.events() if e['kind'] == 'notion.edit'])
        self.api.pages[ASKED]['last_edited_time'] = '2026-11-16T11:00:00.000Z'
        self.api.pages[ASKED]['last_edited_by'] = user(OTHER)
        self.sync()
        heads_up = [e for e in self.events() if e['kind'] == 'notion.edit']
        self.assertEqual([e['title'] for e in heads_up], ['Pricing page'])
        self.api.pages[ASKED]['last_edited_time'] = '2026-11-16T11:20:00.000Z'
        self.api.pages[ASKED]['last_edited_by'] = user(BOT)  # an edit this connection applied after the owner's OK
        self.sync()
        self.assertEqual(len([e for e in self.events() if e['kind'] == 'notion.edit']), 1)
        sid = self.store.suggest('n2', 'Check the pricing page', 'It changed.', [heads_up[0]['id']])['id']
        with self.store.connect() as db:
            self.assertTrue(todo_kinds.quiet(db, sid))  # never a buzz

    def test_an_approved_reply_posts_once_in_its_discussion(self):
        replier = notion.Replier(self.config, self.account, self.helpers)
        before = replier.mine(replier.comment(MINE, D1))
        self.assertEqual(before, [])
        posted = replier.reply(MINE, D1, 'June works.')
        self.assertEqual(self.api.writes[-1][:2], ('POST', 'comments'))
        self.assertEqual(self.api.writes[-1][2]['discussion_id'], notion.dashed(D1))
        self.assertEqual(posted, {'id': 'cd' * 16})
        self.assertEqual([said for _, _, said in replier.mine(replier.comment(MINE, D1))], ['June works.'])

    def test_an_edit_writes_only_into_the_page_as_the_owner_saw_it(self):
        writer = notion.Writer(self.config, self.account, self.helpers)
        seen = writer.snapshot(MINE)
        self.assertEqual([p['text'] for p in seen['paragraphs']], ['We launch in May with the beta.', 'Next steps'])
        changes = doc_writes.resolve(seen, [{'find': 'May', 'replace': 'June'}, {'after': 'Next steps', 'insert': 'Tell partners'}])
        self.api.blocks[MINE][1]['heading_2']['rich_text'] = [text('Next steps soon')]
        self.assertEqual(writer.edit(MINE, changes, seen['version']), {'rejected': 409})  # it changed since: nothing written
        self.assertEqual(self.api.writes, [])
        self.api.blocks[MINE][1]['heading_2']['rich_text'] = [text('Next steps')]
        self.assertEqual(writer.edit(MINE, changes, seen['version']), {'message_id': 'docwrite:' + MINE})
        patched = next(b for m, p, b in self.api.writes if p == 'blocks/' + B1)
        runs = patched['paragraph']['rich_text']
        self.assertEqual(''.join(r['text']['content'] for r in runs), 'We launch in June with the beta.')
        self.assertTrue(any(r['text']['content'] == 'June' and r['annotations']['bold'] for r in runs))  # keeps its formatting
        self.assertTrue(any(r['text'].get('link') for r in runs))  # and the link around it
        added = next(b for m, p, b in self.api.writes if p == f'blocks/{MINE}/children')
        self.assertEqual((added['after'], added['children'][0]['paragraph']['rich_text'][0]['text']['content']), (notion.dashed(B2), 'Tell partners'))

    def test_a_new_private_page_and_a_task_marked_done_after_the_owners_ok(self):
        transport = doc_writes.DocWriteTransport(self.config, machine_sources_connectors.load_connector('docs'), self.helpers)
        action = {'kind': 'doc_write', 'op': 'create', 'account_id': 'notion', 'provider': 'notion', 'title': 'Launch notes',
                  'body': '# Launch notes\nShip on Friday', 'last': True}
        transport.preflight(action)
        self.assertEqual(transport.send(action, {})['message_id'], 'docwrite:' + 'ab' * 16)
        made = next(b for m, p, b in self.api.writes if p == 'pages')
        self.assertEqual(made['parent'], {'type': 'workspace', 'workspace': True})  # the owner's Private section, shared with nobody
        self.assertEqual(doc_writes.link_of('docwrite:' + 'ab' * 16, 'notion'), 'https://www.notion.so/' + 'ab' * 16)
        done = {'kind': 'doc_write', 'op': 'done', 'account_id': 'notion', 'provider': 'notion', 'file_id': TASK, 'doc_title': 'Write the launch notes'}
        self.assertEqual(transport.send(done, {}), {'message_id': 'docwrite:' + TASK})
        self.assertEqual(self.api.writes[-1], ('PATCH', 'pages/' + TASK, {'properties': {'Status': {'status': {'name': 'Shipped'}}}}))
        self.assertEqual(doc_writes.done(done), 'Marked “Write the launch notes” done in Notion')
        self.assertEqual(doc_writes.label(done), 'Mark done')

    def test_done_is_offered_only_for_a_notion_task_of_the_to_do(self):
        context = {'accounts': {'notion': {'provider': 'notion', 'writes': ['create', 'done', 'edit']}},
                   'files': {TASK: {'account_id': 'notion', 'doc_title': 'Write the launch notes', 'provider': 'notion', 'task': True},
                             MINE: {'account_id': 'notion', 'doc_title': 'Launch plan', 'provider': 'notion'}}}
        found = doc_writes.validate({'kind': 'doc_write', 'op': 'done', 'file_id': TASK, 'last': True}, context)
        self.assertEqual((found['op'], found['file_id'], found['provider']), ('done', TASK, 'notion'))
        with self.assertRaises(ValueError):
            doc_writes.validate({'kind': 'doc_write', 'op': 'done', 'file_id': MINE}, context)
        self.assertEqual(doc_writes.file_id_of(f'https://www.notion.so/Launch-plan-{MINE}?pvs=4'), MINE)

    def test_an_expired_sign_in_refreshes_through_the_control_plane_and_is_kept_privately(self):
        self.cred.write_text(json.dumps({**SIGNIN, 'expires_at': 1}))
        self.api.token = 'ntn_fixture_new'
        notion.check(self.config, self.account, self.helpers)
        self.assertEqual(self.api.refreshes, [{'refresh_token': 'ntn_fixture_refresh', 'bot_id': BOT}])  # never a client secret
        kept = json.loads(self.cred.read_text())
        self.assertEqual((kept['access_token'], kept['refresh_token']), ('ntn_fixture_new', 'ntn_fixture_rotated'))
        self.assertEqual(stat.S_IMODE(self.cred.stat().st_mode), 0o600)

    def test_a_pasted_token_finds_its_owner_by_their_address(self):
        self.cred.write_text('ntn_' + 'x' * 40)
        self.api.token = 'ntn_' + 'x' * 40
        self.config['accounts'].append({'id': 'mail', 'service': 'gmail', 'email': 'owner@example.com'})
        served = self.api.answer  # an internal integration's bot has no owner: the workspace's people say who it is
        self.api.answer = lambda m, p, q, b: {'object': 'user', 'type': 'bot', 'id': BOT, 'bot': {'workspace_name': 'Example Team'}} \
            if p == 'users/me' else served(m, p, q, b)
        notion.check(self.config, self.account, self.helpers)
        self.assertEqual((self.account['member_id'], self.account['member_email']), (OWNER, 'owner@example.com'))


if __name__ == '__main__':
    unittest.main()

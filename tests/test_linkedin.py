"""LinkedIn connector plugin and the owner-approved LinkedIn Send. No live calls."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import next_actions as n
import test_ux as ux
a = ux.a
li = a.load_connector('linkedin')
H = a.CONNECTOR_HELPERS

ACCOUNT = {'id': 'li', 'service': 'linkedin', 'transport': 'linkedin-inbox', 'email': 'LinkedIn', 'boundary': 'work:linkedin'}
CONV = 'urn:li:msg_conversation:(urn:li:fsd_profile:ME,2-ABC==)'
NOW = '2026-10-13T10:00:00+00:00'


def raw(**extra):
    return {'urn': 'urn:li:msg_message:(urn:li:fsd_profile:ME,2-M1==)', 'conversation': CONV, 'with': 'Ada Lovelace',
            'from': 'Ada Lovelace', 'fromMe': False, 'at': 1791880000000, 'text': 'Can we talk Friday?', 'subject': None,
            'headline': 'Engineer', 'group': False, 'categories': ['INBOX'], **extra}


class Source:
    def __init__(self, rows):
        self.rows, self.calls = rows, []

    def page(self, since, state):
        self.calls.append(since)
        return {'messages': self.rows, 'state': {}, 'more': False}


class LinkedInSource(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'a.sqlite')
        a.set_timezone('Europe/Amsterdam')

    def test_event_shape_thread_link_and_invalid_rows(self):
        e = li.event(ACCOUNT, raw(), H)
        self.assertEqual(e['kind'], 'linkedin.message')
        self.assertEqual(e['metadata']['conversation_id'], CONV)
        self.assertEqual(e['metadata']['source_url'], 'https://www.linkedin.com/messaging/thread/2-ABC%3D%3D/')
        self.assertEqual(li.event(ACCOUNT, raw(fromMe=True), H)['metadata']['from'], 'You')
        for bad in (raw(urn='x'), raw(at='soon'), raw(fromMe=None), raw(conversation=None)):
            with self.assertRaises(a.SourceError):
                li.event(ACCOUNT, bad, H)

    def test_sync_is_incremental_dedupes_and_sleeps_at_night(self):
        src = Source([raw(), raw()])
        with patch.object(a, 'now', return_value=NOW):
            self.assertEqual(li.sync(self.store, {}, ACCOUNT, H, src)['events'], 1)
            li.sync(self.store, {}, ACCOUNT, H, src)
        self.assertEqual(src.calls[1], int(a.dt.datetime.fromisoformat(NOW).timestamp() * 1000) - 3600000)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM events').fetchone()[0], 1)
        with patch.object(a, 'now', return_value='2026-10-13T23:30:00+00:00'):  # 01:30 local time
            li.sync(self.store, {}, ACCOUNT, H, src)
        self.assertEqual(len(src.calls), 2)

    def test_reader_only_runs_read_commands_and_maps_errors(self):
        source = li.Source({'linkedin_inbox': '/bin/linkedin-inbox-test'}, ACCOUNT, H)
        with self.assertRaises(a.SourceError):
            source.run(['send', '--yes'])
        ok = subprocess.CompletedProcess([], 0, json.dumps({'messages': [], 'state': {}, 'more': False}), '')
        with patch.object(a.subprocess, 'run', return_value=ok) as run:
            source.page(5, {'cursor': 'C1'})
        command = run.call_args.args[0]
        self.assertEqual(command[:4], ['/bin/linkedin-inbox-test', 'sync', '--since', '5'])
        self.assertEqual(json.loads(command[command.index('--state') + 1]), {'cursor': 'C1'})
        for stderr, code, wait in (('the OpenClaw browser is busy (x)', 'linkedin_browser_busy', 600),
                                   ('LinkedIn is signed out in the OpenClaw browser', 'linkedin_signed_out', 3600),
                                   ('LinkedIn is not signed in in the browser', 'linkedin_signed_out', 3600),
                                   ('the browser did not answer in time; try again', 'linkedin_read_timeout', 900),
                                   ('LinkedIn lookup failed: boom', 'linkedin_read_failed', 900)):
            with patch.object(a.subprocess, 'run', return_value=subprocess.CompletedProcess([], 2, '', 'linkedin-inbox: ' + stderr)):
                with self.assertRaises(a.SourceError) as caught:
                    source.page(0, {})
            self.assertEqual((caught.exception.category, caught.exception.retry_after), (code, wait))
        with patch.object(a.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '{"messages": []}', '')):
            with self.assertRaises(a.SourceError):
                source.page(0, {})
        self.assertTrue(li.READER.exists())

    def test_partial_scan_keeps_floor_and_cursor_across_long_outage(self):
        class Paged:
            def __init__(self): self.calls = []
            def page(self, since, state):
                self.calls.append((since, state))
                return {'messages': [raw()], 'state': {'cursor': 'page2'} if len(self.calls) == 1 else {}, 'more': len(self.calls) == 1}
        src = Paged()
        with patch.object(a, 'now', return_value=NOW):
            self.assertTrue(li.sync(self.store, {}, ACCOUNT, H, src)['more'])
        with patch.object(a, 'now', return_value='2026-10-30T10:00:00+00:00'):
            self.assertFalse(li.sync(self.store, {}, ACCOUNT, H, src)['more'])
        self.assertEqual(src.calls[0][0], src.calls[1][0])
        self.assertEqual(src.calls[1][1], {'cursor': 'page2'})
        self.assertTrue(self.store.checkpoint('li')['coverage_complete'])

    def test_review_context_source_line_and_promises(self):
        self.store.commit_page('li', {}, [li.event(ACCOUNT, raw(urn='urn:li:msg_message:(urn:li:fsd_profile:ME,2-M0==)', at=1791870000000, text='Hello?'), H),
                                          li.event(ACCOUNT, raw(), H)])
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM events ORDER BY occurred_at')]
        context = self.store.conversation_context([rows[1]])
        self.assertEqual(len(context[rows[1]['id']]), 1)
        self.assertTrue(context[rows[1]['id']][0].endswith('Ada Lovelace: Hello?'))
        self.assertTrue(a.source_line([rows[1]]).startswith('Source: LinkedIn from Ada Lovelace · '))
        watch = a.awaiting_key(rows[1])
        self.assertEqual(watch['conversation'], CONV)
        self.assertTrue(a.awaiting_match(watch, {**rows[1], 'metadata': {**json.loads(rows[1]['metadata']), 'message_id': 'later'}}))
        self.assertIsNone(a.awaiting_key({**rows[1], 'metadata': {**json.loads(rows[1]['metadata']), 'from_me': True}}))


class LinkedInSend(unittest.TestCase):
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        self.store.commit_page('li', {}, [li.event(ACCOUNT, raw(), H)])
        with self.store.connect() as db:
            event_id = db.execute("SELECT id FROM events WHERE kind='linkedin.message'").fetchone()[0]
        self.sid = self.store.suggest('li-task', 'Reply to Ada', 'Ada asks about Friday.', [event_id])['id']

    def app(self):
        app = object.__new__(a.App)
        app.store = self.store
        app.config = {'accounts': [ACCOUNT, {'id': 'work', 'email': 'owner@example.com', 'service': 'gmail', 'transport': 'gog'}]}
        return app

    def ready(self, **draft):
        self.decide('accept')
        action = {'kind': 'linkedin', 'label': 'Send reply', 'account_id': 'li', 'conversation_id': CONV, 'body': 'Friday works.', **draft}
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'Reply ready.', 'next_action': action})
        return self.row()['next_action']

    def confirm(self, key='owner-approval'):
        return self.app().action('confirm_action', {'suggestion_id': self.sid, 'revision': self.row()['next_action']['revision'],
                                                    'approval_id': key}, owner_dashboard=True)

    def job(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM action_jobs ORDER BY created_at DESC LIMIT 1').fetchone())

    def transport(self, send=None, preflight=None, reconcile=None):
        class T:
            def preflight(self, action): return preflight(action) if preflight else None
            def send(self, action, job): return send(action, job) if send else {'message_id': 'urn:li:msg_message:X'}
            def reconcile(self, action, job): return reconcile(action, job) if reconcile else {}
        return T()

    def test_draft_names_recipient_from_task_and_offers_send(self):
        action = self.ready()
        self.assertEqual(action['to_name'], 'Ada Lovelace')
        self.assertIn('LinkedIn message to Ada Lovelace', n.preview(action))
        self.assertEqual(a.controls(self.row())['blocks'][0]['buttons'][0]['label'], 'Send reply')

    def test_only_task_conversations_or_named_profiles(self):
        self.decide('accept')
        for bad in ({'conversation_id': 'urn:li:msg_conversation:(other)'}, {'conversation_id': None, 'profile': 'ada'},
                    {'conversation_id': CONV, 'profile': 'ada', 'to_name': 'Ada'}, {'account_id': 'work'}, {'label': 'Reply'},
                    {'body': 'x' * 8001}):
            action = {'kind': 'linkedin', 'account_id': 'li', 'conversation_id': CONV, 'body': 'Hi', **bad}
            action = {k: v for k, v in action.items() if v is not None}
            with self.assertRaises(ValueError):
                self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'x', 'next_action': action})
        self.app().action('prepare', {'suggestion_id': self.sid, 'body': 'x', 'next_action':
                                      {'kind': 'linkedin', 'account_id': 'li', 'profile': 'ada-l', 'to_name': 'Ada Lovelace', 'body': 'Hi'}})

    def test_owner_edit_keeps_recipient_and_has_no_subject(self):
        action = self.ready()
        revised = self.app().action('revise_draft', {'suggestion_id': self.sid, 'revision': action['revision'], 'body': 'Friday at ten works.'},
                                    owner_dashboard=True)
        self.assertEqual(revised['status'], 'revised')
        current = self.row()['next_action']
        self.assertEqual((current['body'], current['conversation_id'], current.get('subject')), ('Friday at ten works.', CONV, None))

    def test_approved_send_runs_once_and_card_says_linkedin(self):
        self.ready()
        self.confirm()
        self.confirm('second-click')
        calls = []
        self.app().action_step(self.transport(send=lambda action, job: (calls.append(action), {'message_id': 'urn:li:msg_message:X'})[1]))
        self.app().action_step(self.transport(send=lambda *_: self.fail('Duplicate send')))
        self.assertEqual([c['body'] for c in calls], ['Friday works.'])
        self.assertEqual(self.job()['status'], 'sent')
        self.assertIn('✓ LinkedIn message sent to Ada Lovelace at ', str(a.card(self.row())))

    def test_reply_in_that_conversation_answers_the_card(self):
        self.ready()
        self.confirm()
        with patch.object(a, 'now', return_value='2026-10-13T10:00:00+00:00'):
            self.app().action_step(self.transport())
        later = li.event(ACCOUNT, raw(urn='urn:li:msg_message:(urn:li:fsd_profile:ME,2-M2==)', at=1792000000000, text='Great, see you then.'), H)
        own = li.event(ACCOUNT, raw(urn='urn:li:msg_message:(urn:li:fsd_profile:ME,2-M3==)', at=1792000000001, fromMe=True), H)
        self.store.commit_page('li', {}, [later, own])
        with self.store.connect() as db:
            rows = {json.loads(r['metadata'])['message_id']: dict(r) for r in db.execute("SELECT * FROM events WHERE occurred_at>'2026-10-14'")}
        replies = self.store.card_replies(list(rows.values()))
        self.assertEqual([replies[r['id']]['suggestion_id'] for r in rows.values() if r['id'] in replies], [self.sid])
        self.assertIn(rows[later['metadata']['message_id']]['id'], replies)

    def test_busy_browser_waits_without_blocking_or_sending(self):
        self.ready()
        self.confirm()
        def busy(_): raise n.LinkedInBusy()
        self.assertEqual(self.app().action_step(self.transport(preflight=busy, send=lambda *_: self.fail('sent while busy'))), 'waiting')
        job = self.job()
        self.assertEqual(job['status'], 'queued')
        self.assertIsNotNone(job['retry_at'])

    def test_unknown_outcome_never_resends_and_no_intent_requeues(self):
        self.ready()
        self.confirm()
        self.app().action_step(self.transport(send=lambda *_: {}))
        self.assertEqual(self.job()['status'], 'uncertain')
        self.assertIn('LinkedIn message', self.job()['error'])
        with self.store.connect() as db:
            db.execute('UPDATE action_jobs SET retry_at=NULL')
        self.app().action_step(self.transport(reconcile=lambda *_: {}, send=lambda *_: self.fail('resent an uncertain message')))
        self.assertEqual(self.job()['status'], 'uncertain')
        self.assertIn('LinkedIn message', self.job()['error'])


class Transport(unittest.TestCase):
    config = {'accounts': [ACCOUNT], 'linkedin_inbox': '/bin/linkedin-inbox-test'}
    action = {'kind': 'linkedin', 'account_id': 'li', 'profile': 'ada-l', 'to_name': 'Ada Lovelace', 'body': 'Hi Ada'}

    def test_preflight_checks_profile_name_and_send_uses_job_token(self):
        t = n.LinkedInTransport(self.config)
        seen = []
        def run(args, **_):
            seen.append(args)
            if '--yes' in args:
                return subprocess.CompletedProcess(args, 0, json.dumps({'sent': 'sent', 'messageUrn': 'urn:li:msg_message:Q'}), '')
            return subprocess.CompletedProcess(args, 0, json.dumps({'preview': {'name': 'Ada  lovelace'}}), '')
        with patch.object(n.subprocess, 'run', side_effect=run):
            t.preflight(self.action)
            self.assertEqual(t.send(self.action, {'id': 'J1'}), {'message_id': 'urn:li:msg_message:Q'})
        self.assertEqual(seen[0][:4], ['/bin/linkedin-inbox-test', 'send', '--profile', 'ada-l'])
        self.assertNotIn('--yes', seen[0])
        self.assertEqual(seen[1][seen[1].index('--send-id') + 1], 'assistant-J1')
        wrong = subprocess.CompletedProcess([], 0, json.dumps({'preview': {'name': 'Bob Other'}}), '')
        with patch.object(n.subprocess, 'run', return_value=wrong), self.assertRaises(ValueError):
            t.preflight(self.action)

    def test_an_account_with_its_own_browser_profile_reads_and_sends_there(self):
        ok = subprocess.CompletedProcess([], 0, json.dumps({'messages': [], 'state': {}, 'more': False}), '')
        with patch.object(a.subprocess, 'run', return_value=ok) as run:
            li.Source({}, ACCOUNT, H).page(5, {})
        self.assertIsNone(run.call_args.kwargs['env'])  # no profile of its own: the reader's default
        second = {**ACCOUNT, 'id': 'li-2', 'browser_profile': 'machine-2', 'browser_cdp': 'http://127.0.0.1:9304'}
        with patch.object(a.subprocess, 'run', return_value=ok) as run:
            li.Source({}, second, H).page(5, {})
        self.assertEqual(run.call_args.kwargs['env']['LINKEDIN_INBOX_BROWSER_PROFILE'], 'machine-2')
        t = n.LinkedInTransport({'accounts': [ACCOUNT, second], 'linkedin_inbox': '/bin/linkedin-inbox-test'})
        with patch.object(n.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')) as run:
            t.reconcile({**self.action, 'account_id': 'li-2'}, {'id': 'J1'})
        self.assertEqual(run.call_args.kwargs['env']['LINKEDIN_INBOX_BROWSER_PROFILE'], 'machine-2')
        self.assertEqual(run.call_args.kwargs['env']['LINKEDIN_INBOX_BROWSER_CDP'], 'http://127.0.0.1:9304')

    def test_default_reader_is_the_bundled_one(self):
        self.assertEqual(n.LinkedInTransport({'accounts': [ACCOUNT]}).cli(self.action), str(n.LINKEDIN_INBOX))
        self.assertTrue(n.LINKEDIN_INBOX.exists())

    def test_refusal_unknown_and_busy_outcomes(self):
        t = n.LinkedInTransport(self.config)
        cases = [(subprocess.CompletedProcess([], 4, json.dumps({'sent': 'failed', 'status': 422}), ''), {'rejected': 422}),
                 (subprocess.CompletedProcess([], 4, json.dumps({'sent': 'uncertain'}), ''), {}),
                 (subprocess.CompletedProcess([], 2, '', 'not sending again'), {}),
                 (subprocess.CompletedProcess([], 2, '', 'browser is busy'), {'not_sent': True})]
        for result, expected in cases:
            with patch.object(n.subprocess, 'run', return_value=result):
                self.assertEqual(t.send(self.action, {'id': 'J'}), expected)
        none = subprocess.CompletedProcess([], 0, json.dumps({'found': False, 'attempted': False}), '')
        with patch.object(n.subprocess, 'run', return_value=none):
            self.assertEqual(t.reconcile(self.action, {'id': 'J'}), {})
        with patch.object(n.subprocess, 'run', return_value=subprocess.CompletedProcess([], 2, '', 'the OpenClaw browser is busy')):
            with self.assertRaises(n.LinkedInBusy):
                t.preflight(self.action)

    def test_action_transport_routes_linkedin(self):
        email, linkedin = object(), object()
        router = n.ActionTransport(email, linkedin)
        self.assertIs(router.pick({'kind': 'linkedin'}), linkedin)
        self.assertIs(router.pick({'kind': 'email'}), email)


if __name__ == '__main__':
    unittest.main()


class Tabs(unittest.TestCase):
    """The browser readers close what they open, also after a run that was stopped halfway."""
    def test_signed_out_shows_where_to_sign_in_again(self):
        hosted = a.sign_in_help('linkedin', 'linkedin_signed_out', 'https://app.example.test/setup')
        self.assertEqual(hosted['sign_in_url'], 'https://app.example.test/open?to=browser&site=linkedin')
        self.assertTrue(hosted['signed_out'])
        self.assertIn('not signed in to LinkedIn', hosted['sign_in_hint'])
        self.assertEqual(a.sign_in_help('x', 'x_signed_out', 'https://app.example.test/setup')['sign_in_url'],
                         'https://app.example.test/open?to=browser&site=x')
        self.assertIsNone(a.sign_in_help('linkedin', 'linkedin_signed_out', None)['sign_in_url'])  # self-hosted: the hint only
        self.assertEqual(a.sign_in_help('linkedin', 'linkedin_read_failed', 'https://app.example.test/setup'), {})
        self.assertEqual(a.sign_in_help('linkedin', None, None), {})

    def test_with_a_devtools_address_the_readers_skip_openclaw(self):
        import importlib.util
        for name in ('linkedin_inbox', 'x_inbox'):
            spec = importlib.util.spec_from_file_location(name, Path(__file__).parent.parent / 'integrations' / f'{name}.py')
            reader = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(reader)
            cdp, calls = reader.browser_cdp, []

            def evaluate(base, target, js, timeout_ms):
                calls.append(('evaluate', target))
                if len([c for c in calls if c[0] == 'evaluate']) == 1:
                    raise cdp.CdpError('script failed: Execution context was destroyed.')  # still navigating
                return {'ok': True}
            fakes = {'open_tab': lambda base, url: calls.append(('open', url)) or 'T1',
                     'close_tab': lambda base, target: calls.append(('close', target)),
                     'tab_ids': lambda base: {'OWNER'}, 'evaluate': evaluate,
                     'navigate': lambda base, target, url: calls.append(('navigate', target, url))}
            with tempfile.TemporaryDirectory() as tmp, patch.object(reader, 'CDP', 'http://127.0.0.1:9222'), \
                    patch.multiple(cdp, **fakes), patch.object(reader, 'OPEN_TABS', Path(tmp) / 'tabs'), \
                    patch.object(reader, 'lease', lambda *a, **k: subprocess.CompletedProcess(a, 0, '', '')), \
                    patch.object(reader.subprocess, 'run', side_effect=AssertionError('no OpenClaw call')), \
                    patch.object(reader.time, 'sleep', lambda s: None):
                self.assertEqual(reader.with_tab('https://example.test', lambda t: [reader.evaluate(t, 'f') for _ in range(2)][-1]), {'ok': True})
                self.assertEqual(reader.evaluate('T1', 'f').get('ok'), True)
            self.assertTrue(calls[0][1].startswith('about:blank#the-machine-'), name)
            self.assertIn(('navigate', 'T1', 'https://example.test'), calls)
            self.assertIn(('close', 'T1'), calls, name)
            with patch.object(reader, 'CDP', 'http://127.0.0.1:9222'), \
                    patch.object(cdp, 'evaluate', side_effect=cdp.CdpError('browser not reachable')), self.assertRaises(reader.Fail):
                reader.evaluate('T1', 'f')

    def test_through_openclaw_a_reader_never_opens_an_about_page(self):
        # OpenClaw's gateway refuses every non-http(s) address, about:blank#... included.
        import importlib.util
        for name in ('linkedin_inbox', 'x_inbox'):
            spec = importlib.util.spec_from_file_location(name, Path(__file__).parent.parent / 'integrations' / f'{name}.py')
            reader = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(reader)
            opened, urls = [], {}

            def oc(*args, timeout=60):
                if args[0] in ('open', 'navigate') and not args[-1].startswith(('http://', 'https://')):
                    raise reader.Fail('browser command failed: Navigation blocked: unsupported protocol "about:"')
                if args[0] == 'open':
                    opened.append(args[-1])
                    urls['T1'] = args[-1] + ''
                    return 'id: T1\n'
                if args[:2] == ('--json', 'tabs'):
                    return json.dumps({'tabs': [{'targetId': t, 'url': u} for t, u in urls.items()]})
                if args[0] == 'close':
                    urls.pop(args[1], None)
                return ''
            with tempfile.TemporaryDirectory() as tmp, patch.object(reader, 'oc', oc), patch.object(reader, 'CDP', ''), \
                    patch.object(reader, 'OPEN_TABS', Path(tmp) / 'tabs'), patch.object(reader, 'lease', lambda *a, **k: subprocess.CompletedProcess(a, 0, '', '')):
                reader.with_tab('https://example.test/inbox#old', lambda target: None)
                self.assertEqual(len(opened), 1, name)
                self.assertRegex(opened[0], r'^https://example\.test/inbox#the-machine-[0-9a-f]{32}$', name)
                self.assertEqual(urls, {}, name)
                # A lost receipt is still recovered by the fragment, even if the page added a query.
                urls['LOST'] = 'https://example.test/inbox?x=1' + opened[0][opened[0].index('#'):]
                urls['OTHER'] = 'https://example.test/inbox#the-machine-' + '0' * 32
                self.assertEqual(reader.recover_tab(opened[0]), 'LOST', name)

    def test_a_stopped_run_leaves_no_tab_and_the_owners_tabs_stay(self):
        import importlib.util
        for name in ('linkedin_inbox', 'x_inbox'):
            spec = importlib.util.spec_from_file_location(name, Path(__file__).parent.parent / 'integrations' / f'{name}.py')
            reader = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(reader)
            tabs, closed, urls = {'OWNER'}, [], {'OWNER': 'https://owner.test'}

            def oc(*args, timeout=60):
                if args[:2] == ('--json', 'tabs'):
                    return json.dumps({'tabs': [{'targetId': t, 'url': urls[t]} for t in tabs]})
                if args[0] == 'navigate':
                    urls[args[2]] = args[3]
                    return ''
                if args[0] == 'tabs':
                    return ''.join(f'id: {t}\n' for t in sorted(tabs))
                if args[0] == 'open':
                    urls['NEW%d' % len(tabs)] = args[-1]
                    tabs.add('NEW%d' % len(tabs))
                    return 'id: NEW%d\n' % (len(tabs) - 1)
                if args[0] == 'close':
                    tabs.discard(args[1])
                    closed.append(args[1])
                    return ''
            with tempfile.TemporaryDirectory() as tmp, patch.object(reader, 'oc', oc), \
                    patch.object(reader, 'OPEN_TABS', Path(tmp) / 'tabs'), patch.object(reader, 'lease', lambda *a, **k: subprocess.CompletedProcess(a, 0, '', '')):
                first = reader.open_tab('reader-1', 'https://example.test')  # the run is killed here: never closed
                reader.with_tab('https://example.test', lambda target: None)
                self.assertIn(first, closed)
                self.assertEqual(tabs, {'OWNER'}, name)

                def slow(*args, timeout=60):  # the tab appears, then the open times out
                    if args[0] == 'open':
                        tabs.add('LATE')
                        urls['LATE'] = args[-1]
                        tabs.add('UNRELATED')
                        urls['UNRELATED'] = 'https://another-reader.test'
                        raise reader.Fail('timed out')
                    return oc(*args, timeout=timeout)
                with patch.object(reader, 'oc', slow), self.assertRaises(reader.Fail):
                    reader.with_tab('https://example.test', lambda target: None)
                self.assertEqual(tabs, {'OWNER', 'UNRELATED'}, name)


class ReadWindow(unittest.TestCase):
    """Sources with read hours tell the dashboard when they read again, so a night's pause never reads as stale."""
    def test_when_it_opened_and_when_it_reads_again(self):
        x = {'id': 'me-x', 'service': 'x', 'boundary': 'work'}
        cases = [('2026-10-28T02:00:00+00:00', x, {'hours': [7, 23], 'reads_again_at': '2026-10-28T06:00:00+00:00'}),  # 03:00 local
                 ('2026-10-28T09:00:00+00:00', x, {'hours': [7, 23], 'opened_at': '2026-10-28T06:00:00+00:00'}),
                 ('2026-10-28T22:30:00+00:00', x, {'hours': [7, 23], 'reads_again_at': '2026-10-29T06:00:00+00:00'}),  # 23:30 local
                 # LinkedIn's own hours; the evening before the clocks go back, 07:00 is an hour later in UTC
                 ('2026-10-24T20:30:00+00:00', {**x, 'service': 'linkedin'}, {'hours': [7, 22], 'reads_again_at': '2026-10-25T06:00:00+00:00'}),
                 ('2026-10-28T12:00:00+00:00', {**x, 'active_hours': [9, 17]}, {'hours': [9, 17], 'opened_at': '2026-10-28T08:00:00+00:00'}),
                 ('2026-10-28T02:00:00+00:00', {**x, 'active_hours': [0, 24]}, None),  # around the clock
                 ('2026-10-28T02:00:00+00:00', {**x, 'service': 'github'}, None)]
        for at, account, want in cases:
            with self.subTest(at=at, account=account), patch.object(a, 'LOCAL_TZ', a.ZoneInfo('Europe/Amsterdam')):
                self.assertEqual(a.read_window(account, at), want)

    def test_the_dashboard_gets_it_with_each_source(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(a, 'now', return_value='2026-10-28T02:00:00+00:00'), \
                patch.object(a, 'LOCAL_TZ', a.ZoneInfo('Europe/Amsterdam')):
            store = a.Store(Path(tmp) / 'events.sqlite')
            found = {c['id']: c['read_window'] for c in store.snapshot([{**ACCOUNT, 'service': 'linkedin'}, {'id': 'gh', 'service': 'github', 'boundary': 'work'}])['connectors']}
        self.assertEqual(found, {'li': {'hours': [7, 22], 'reads_again_at': '2026-10-28T06:00:00+00:00'}, 'gh': None})

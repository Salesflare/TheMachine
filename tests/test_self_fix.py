"""The Machine fixes itself: its own errors become signals (code locations only), and an owner-approved
Merge applies a fix made and tested in a clone, never in the running code."""
import json
import logging
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
import next_actions as n
import test_ux as ux
from test_gateway import FakeJournal
a = ux.a


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), '-c', 'user.name=Test', '-c', 'user.email=test@example.com', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


class Faults(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'a.sqlite')
        self.log = a.FaultLog(self.store, 'abc123')

    def rows(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM faults')]

    def fail_in_code(self, error):
        try:
            raise error
        except Exception:
            self.log.emit(logging.LogRecord('personal-assistant', logging.ERROR, __file__, 1, 'graph error=%s', ('KeyError',), None))

    def test_code_errors_are_kept_as_locations_without_messages(self):
        for _ in range(3):
            self.fail_in_code(KeyError('alex@example.com private subject'))
        [row] = self.rows()
        self.assertEqual((row['kind'], row['location'], row['count'], row['version']), ('KeyError', 'graph', 3, 'abc123'))
        frames = json.loads(row['frames'])
        self.assertEqual(frames[-1]['function'], 'fail_in_code')
        self.assertEqual(frames[-1]['file'], 'tests/test_self_fix.py')
        self.assertNotIn('alex@example.com', json.dumps(row))
        self.assertEqual(row['message'], '<text>')  # quoted text is content, never kept

    def test_the_message_is_kept_without_anything_private(self):
        self.fail_in_code(ValueError('The Network said 500'))
        self.assertEqual(self.rows()[0]['message'], 'The Network said 500')
        cases = {
            "KeyError: 'box'": KeyError('box'),
            'Expecting value: line 1 column 1 (char 0)': ValueError('Expecting value: line 1 column 1 (char 0)'),
            'bad token=<secret> for <link> from <email>, call <number>':
                ValueError('bad token=abc123 for https://example.com/x?key=1 from sam@example.com, call +32 470 12 34 56'),
            'Bearer <secret> refused for <id>': ValueError('Bearer abcdefghijklmnopqrstuvwxyz012345 refused for 3f2b8c1e-1111-2222-3333-444455556666'),
            'Unknown person <text>': ValueError('Unknown person "Sam Example"'),
        }
        for expected, error in cases.items():
            self.assertEqual(('KeyError: ' if isinstance(error, KeyError) else '') + a.fault_message(error), expected)
        self.assertIsNone(a.fault_message(ValueError()))
        self.assertLessEqual(len(a.fault_message(ValueError('word ' * 200))), 200)

    def test_trouble_outside_the_code_is_not_a_bug(self):
        for error in (a.SourceError('gmail'), TimeoutError(), ConnectionResetError(), a.sqlite3.OperationalError('database is locked')):
            self.fail_in_code(error)
        self.log.emit(logging.LogRecord('personal-assistant', logging.ERROR, __file__, 1, 'no exception here', (), None))
        self.assertEqual(self.rows(), [])

    def test_a_thread_that_dies_is_recorded(self):
        previous = threading.excepthook
        self.addCleanup(setattr, threading, 'excepthook', previous)
        threading.excepthook = lambda args: None  # keep the test output quiet
        self.addCleanup(a.LOG.removeHandler, a.watch_faults(self.store, Path(__file__).resolve().parent.parent))
        thread = threading.Thread(target=lambda: 1 / 0, name='graph')
        thread.start()
        thread.join()
        self.assertEqual([(r['kind'], r['location']) for r in self.rows()], [('ZeroDivisionError', 'thread graph')])

    def test_the_gateway_source_reports_faults_once_per_step(self):
        gateway, other = {'id': 'openclaw-gateway', 'service': 'gateway'}, {'id': 'second-gateway', 'service': 'gateway'}
        config = {'accounts': [gateway, other], 'app_dir': '/srv/machine', 'fix_dir': '/tmp/fixes'}
        self.fail_in_code(KeyError('x'))
        a.sync_gateway(self.store, config, other, FakeJournal())
        self.assertEqual(self.store.events([other['id']]), [])  # only the first Gateway source carries them
        a.sync_gateway(self.store, config, gateway, FakeJournal())
        [event] = self.store.events([gateway['id']])
        self.assertEqual(event['kind'], 'machine.fault')
        self.assertIn('Graph failed 1 time', event['body'])
        self.assertIn("Error: KeyError: 'x'", event['body'])
        self.assertTrue(event['body'].startswith('Updating who knows whom failed. Who-knows-whom answers may be out of date. Nothing to do yet.'))
        self.assertIn('test_self_fix.py:', event['body'])
        self.assertEqual(json.loads(event['metadata'])['app_dir'] if isinstance(event['metadata'], str) else event['metadata']['app_dir'], '/srv/machine')
        self.fail_in_code(KeyError('x'))
        a.sync_gateway(self.store, config, gateway, FakeJournal())
        self.assertEqual(self.store.events([gateway['id']])[0]['title'], 'The Machine: KeyError in fail_in_code')  # 2 is not a step
        self.fail_in_code(KeyError('x'))
        a.sync_gateway(self.store, config, gateway, FakeJournal())
        self.assertEqual(self.store.events([gateway['id']])[0]['title'], 'The Machine: KeyError in fail_in_code (3×)')


    def test_the_signal_says_in_plain_words_who_acts_and_keeps_code_locations_under_details(self):
        gateway = {'id': 'openclaw-gateway', 'service': 'gateway'}
        config = {'accounts': [gateway]}
        for _ in range(3):
            try:
                raise ValueError('The Network said 500')
            except ValueError:
                self.log.emit(logging.LogRecord('personal-assistant', logging.ERROR, __file__, 1, 'fleet error=%s at=%s', ('ValueError', 'x'), None))
        a.sync_gateway(self.store, config, gateway, FakeJournal())
        [view] = self.store.event_views([e['id'] for e in self.store.events([gateway['id']])])
        self.assertEqual(view['from'], 'The Machine')
        self.assertEqual(view['body'].splitlines()[0], 'Talking with your Fleet on The Machine Network failed. Teammates’ questions and answers may come late; '
                         'your own to-dos are fine. The Machine can fix this itself: it tests a fix in a copy, and a small one merges by itself (undo for a day).')
        self.assertIn('Error: ValueError: The Network said 500', view['body'])
        self.assertNotIn('test_self_fix.py', view['body'])
        self.assertTrue(view['details'].startswith('Where (innermost last):\n  tests/test_self_fix.py:'))
        self.assertIn('Code version: abc123', view['details'])
        self.assertIn('you review it and tap Merge', a.fault_plain('fleet', 3, {'self_fix_auto': False}))
        self.assertTrue(a.fault_plain('thread graph', 1, {}).startswith('Updating who knows whom failed.'))
        self.assertTrue(a.fault_plain('odd place', 1, {}).startswith('Part of The Machine (odd place) failed. Probably nothing yet'))


    def test_an_outside_service_failing_is_named_retried_and_needs_nothing(self):
        import io, urllib.error
        import fleet
        gateway = {'id': 'openclaw-gateway', 'service': 'gateway'}

        def translated(code, url):  # a client turning an HTTP error into a bare ValueError, as clients do
            try:
                raise urllib.error.HTTPError(url, code, 'error', {}, io.BytesIO(b''))
            except urllib.error.HTTPError:
                raise ValueError(f'The service said {code}') from None

        for error_at in (lambda: translated(500, 'https://www.googleapis.com/x'),):
            try:
                error_at()
            except ValueError as error:
                self.assertEqual(a.fault_origin(error), {'service': 'Google', 'status': 500})
        try:
            raise fleet.NetworkUnavailable('The Network had a problem')
        except ValueError as error:
            self.assertEqual(a.fault_origin(error), {'service': 'The Machine Network', 'status': None})
        self.assertIs(fleet.Unavailable, fleet.NetworkUnavailable)
        try:
            translated(400, 'https://slack.com/api/x')  # a refusal may be The Machine's own mistake
        except ValueError as error:
            self.assertIsNone(a.fault_origin(error))
        try:
            try:
                raise TimeoutError()
            except TimeoutError:
                {}['missing']  # a bug while handling a timeout is still a bug
        except KeyError as error:
            self.assertIsNone(a.fault_origin(error))
        try:
            try:
                raise urllib.error.URLError('down')
            except urllib.error.URLError as cause:
                raise ValueError('Slack did not answer') from cause
        except ValueError as error:
            self.assertEqual(a.fault_origin(error), {'service': 'An outside service', 'status': None})

        for _ in range(3):
            try:
                translated(503, 'https://app.themachine.computer/api/fleet/directory')
            except ValueError:
                self.log.emit(logging.LogRecord('personal-assistant', logging.ERROR, __file__, 1, 'fleet error=%s', ('ValueError',), None))
        a.sync_gateway(self.store, {'accounts': [gateway]}, gateway, FakeJournal())
        [event] = self.store.events([gateway['id']])
        self.assertTrue(event['body'].startswith('Talking with your Fleet on The Machine Network failed because The Machine Network had a problem '
                                                 '(it answered 503), not The Machine. Teammates’ questions and answers may come late; your own to-dos '
                                                 'are fine. The Machine tries again by itself; nothing is needed from you.'), event['body'])
        self.assertNotIn('fix this itself', event['body'])
        metadata = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'])
        self.assertEqual(metadata['outside'], {'service': 'The Machine Network', 'status': 503})


class FaultCardsSettle(unittest.TestCase):
    """A card about an error that an update fixed closes by itself."""
    def setUp(self):
        clock = patch.object(a, 'now', return_value='2026-10-22T12:00:00+00:00')  # the fixture's error is two days old
        clock.start(); self.addCleanup(clock.stop)
        ux.UX.setUp(self)
        with self.store.connect() as db:
            db.execute("UPDATE events SET kind='machine.fault',metadata=? WHERE id=1", (json.dumps({'fingerprint': 'fp-fleet'}),))
            db.execute("INSERT INTO faults(fingerprint,day,kind,frames,location,version,first_at,last_at,count) VALUES('fp-fleet','2026-10-20','ValueError','[]','fleet','old111',"
                       "'2026-10-20T20:01:00+00:00','2026-10-20T20:04:00+00:00',5)")
            db.execute("INSERT INTO fault_versions VALUES('fp-fleet','old111','2026-10-20','ValueError','2026-10-20T20:01:00+00:00','2026-10-20T20:04:00+00:00',5)")

    def status(self):
        with self.store.connect() as db:
            return db.execute('SELECT status FROM suggestions WHERE id=?', (self.sid,)).fetchone()[0]

    def test_a_stale_error_card_closes_once_newer_code_stays_quiet(self):
        self.assertEqual(self.store.settle_faults('old111'), [])  # the version that had it still runs
        self.assertEqual(self.status(), 'pending')
        self.assertEqual(self.store.settle_faults('new222'), [self.sid])
        self.assertEqual(self.status(), 'completed')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT feedback,source FROM decisions WHERE suggestion_id=?', (self.sid,)).fetchone()[:],
                             ('The error stopped after an update: not seen for a day.', 'assistant'))

    def test_a_recent_error_or_a_card_about_more_stays_open(self):
        with self.store.connect() as db:
            db.execute('UPDATE faults SET last_at=?', (a.now(),))
        self.assertEqual(self.store.settle_faults('new222'), [])
        with self.store.connect() as db:
            db.execute("UPDATE faults SET last_at='2026-10-20T20:04:00+00:00'")
        self.store.commit_page('work', {}, [ux.event(source='other-message')])
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (json.dumps([1, 2]), self.sid))
        self.assertEqual(self.store.settle_faults('new222'), [])
        self.assertEqual(self.status(), 'pending')


class Merge(unittest.TestCase):
    setUp_ux = ux.UX.setUp
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.setUp_ux()
        self.root = Path(tempfile.mkdtemp(prefix='machine-merge-'))
        self.addCleanup(subprocess.run, ['rm', '-rf', str(self.root)])
        self.upstream, self.app_dir, self.fixes = self.root / 'upstream.git', self.root / 'app', self.root / 'fixes'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.upstream)], check=True)
        subprocess.run(['git', 'clone', '-q', str(self.upstream), str(self.app_dir)], check=True, capture_output=True)
        (self.app_dir / 'graph.py').write_text('def rebuild(rows):\n    return rows["missing"]\n')
        git(self.app_dir, 'add', '.')
        git(self.app_dir, 'commit', '-qm', 'Start')
        git(self.app_dir, 'push', '-q', '-u', 'origin', 'HEAD:main')
        self.restarts = []
        self.config = {'accounts': [], 'app_dir': str(self.app_dir), 'fix_dir': str(self.fixes), 'self_test': ['true']}

    def fix(self, name='job1'):
        clone = self.fixes / name
        subprocess.run(['git', 'clone', '-q', str(self.app_dir), str(clone)], check=True, capture_output=True)
        (clone / 'graph.py').write_text('def rebuild(rows):\n    return rows.get("missing")\n')
        git(clone, 'commit', '-qam', 'Graph: a missing key is not a crash')
        return clone

    def action(self, clone, **extra):
        return n.validate({'kind': 'merge', 'clone': str(clone), 'summary': 'The graph rebuild no longer stops on a missing key.', **extra}, self.config, [])

    def transport(self):
        return n.MergeTransport(self.config, lambda: self.restarts.append(1) or True)

    def test_a_committed_fix_in_a_clone_becomes_a_reviewable_merge(self):
        clone = self.fix()
        action = self.action(clone)
        self.assertEqual((action['kind'], action['label'], action['commits'], action['files']), ('merge', 'Merge fix', 1, ['graph.py']))
        self.assertEqual(action['base'], git(self.app_dir, 'rev-parse', 'HEAD'))
        self.assertEqual(action['head'], git(clone, 'rev-parse', 'HEAD'))
        self.assertIn('+    return rows.get("missing")', action['diff'])
        self.assertIn('Merge now runs the tests again', n.preview(action))
        self.assertFalse(action['plugin'])

    def test_only_a_clean_committed_clone_under_the_fix_folder(self):
        with self.assertRaisesRegex(ValueError, 'under'):
            self.action(self.app_dir)  # never the running code
        clone = self.fix()
        (clone / 'graph.py').write_text('changed after the commit\n')
        with self.assertRaisesRegex(ValueError, 'uncommitted'):
            self.action(clone)
        git(clone, 'checkout', '-q', 'graph.py')
        (self.app_dir / 'other.py').write_text('x = 1\n')
        git(self.app_dir, 'add', '.')
        git(self.app_dir, 'commit', '-qm', 'Moved on')
        with self.assertRaisesRegex(ValueError, 'not on top'):
            self.action(clone)
        with self.assertRaisesRegex(ValueError, 'nothing to merge'):
            fresh = self.fixes / 'job2'
            subprocess.run(['git', 'clone', '-q', str(self.app_dir), str(fresh)], check=True, capture_output=True)
            self.action(fresh)

    def test_merge_now_tests_fast_forwards_pushes_and_restarts(self):
        action = self.action(self.fix())
        transport = self.transport()
        transport.preflight(action)
        result = transport.send(action, {'id': 'job'})
        self.assertEqual(result['message_id'], 'merge:' + action['head'][:12])
        self.assertEqual(self.restarts, [])  # restart waits until the receipt is committed
        effects=transport.complete(action,result)
        self.assertEqual(effects, {'pushed':True,'held':None,'activation_ready':True})
        self.assertEqual(git(self.app_dir, 'rev-parse', 'HEAD'), action['head'])
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), action['head'])
        self.assertIn('rows.get', (self.app_dir / 'graph.py').read_text())
        self.assertEqual(transport.reconcile(action, {})['message_id'], 'merge:' + action['head'][:12])

    def test_nothing_is_merged_when_tests_fail_or_anything_moved(self):
        action = self.action(self.fix())
        self.config['self_test'] = ['false']
        with self.assertRaisesRegex(ValueError, 'tests fail'):
            self.transport().preflight(action)
        self.config['self_test'] = ['true']
        (self.fixes / 'job1' / 'graph.py').write_text('edited after review\n')
        with self.assertRaisesRegex(ValueError, 'changed after you reviewed'):
            self.transport().preflight(action)
        git(self.fixes / 'job1', 'checkout', '-q', 'graph.py')
        (self.app_dir / 'graph.py').write_text('local edit\n')
        with self.assertRaisesRegex(ValueError, 'uncommitted changes'):
            self.transport().preflight(action)
        git(self.app_dir, 'checkout', '-q', 'graph.py')
        (self.app_dir / 'other.py').write_text('x = 1\n')
        git(self.app_dir, 'add', '.')
        git(self.app_dir, 'commit', '-qm', 'Moved on')
        with self.assertRaisesRegex(ValueError, 'changed since this fix was made'):
            self.transport().preflight(action)
        self.assertEqual(self.restarts, [])

    def test_the_owner_merges_from_the_card_and_the_agent_cannot(self):
        self.decide('accept')
        app = object.__new__(a.App)
        app.store, app.config = self.store, self.config
        merge = {'kind': 'merge', 'clone': str(self.fix()), 'summary': 'The graph rebuild no longer stops on a missing key.'}
        with self.assertRaisesRegex(ValueError, 'send_now'):
            app.action('prepare', {'suggestion_id': self.sid, 'body': 'Fixed and tested in a copy.', 'next_action': merge, 'send_now': True})
        app.action('prepare', {'suggestion_id': self.sid, 'body': 'Fixed and tested in a copy.', 'next_action': merge})
        row = self.row()
        self.assertEqual([b['label'] for b in a.controls(row)['blocks'][0]['buttons']][:1], ['Merge fix'])
        self.assertEqual(git(self.app_dir, 'log', '--format=%s', '-1'), 'Start')  # saving the result changed nothing
        app.action('confirm_action', {'suggestion_id': self.sid, 'revision': row['next_action']['revision'], 'approval_id': 'owner-tap'}, owner_dashboard=True)
        self.assertEqual(app.action_step(next_actions_transport(self)), 'sent')
        self.assertIn('Merged. The Machine restarts with the fix.', a.card(self.row()))
        self.assertEqual(git(self.app_dir, 'log', '--format=%s', '-1'), 'Graph: a missing key is not a crash')
        self.assertEqual(app.action_step(next_actions_transport(self)), None)  # merged once
        self.assertEqual(self.restarts, [1])


class AutoMerge(unittest.TestCase):
    """Private: a small, tested fix to The Machine's own error merges by itself, and stays undoable."""
    setUp_ux = ux.UX.setUp
    setUp_merge = Merge.setUp
    fix_clone = Merge.fix
    transport = Merge.transport
    row = ux.UX.row
    decide = ux.UX.decide

    def setUp(self):
        self.setUp_merge()
        with self.store.connect() as db:
            db.execute("UPDATE events SET kind='machine.fault',metadata=? WHERE id=1", (json.dumps({'fingerprint': 'fp-graph'}),))
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        self.decide('accept')

    def fix(self, proof=True, name='job1'):
        clone = self.fix_clone(name)
        (clone / 'test_graph.py').write_text('import unittest\nimport graph\n\n\nclass Graph(unittest.TestCase):\n'
                                             + ('    def test_missing_key(self):\n        self.assertIsNone(graph.rebuild({}))\n' if proof
                                                else '    def test_present_key(self):\n        self.assertEqual(graph.rebuild({"missing": 1}), 1)\n'))
        git(clone, 'add', '.')
        git(clone, 'commit', '-qm', 'Test the missing key')
        return clone

    def save(self, clone):
        return self.app.action('prepare', {'suggestion_id': self.sid, 'body': 'Fixed and tested in a copy.',
                                           'next_action': {'kind': 'merge', 'clone': str(clone), 'summary': 'The graph rebuild no longer stops on a missing key.'}})

    def labels(self):
        return [b['label'] for block in a.controls(self.row())['blocks'] for b in block['buttons']]

    def merged(self):
        saved = self.save(self.fix())
        self.assertTrue(saved['auto_merge'].startswith('queued'))
        self.assertIn('It merges by itself if every check passes.', a.card(self.row()))
        self.assertNotIn('Merge fix', self.labels())
        self.assertEqual(self.app.action_step(next_actions_transport(self)), 'sent')
        self.assertEqual(git(self.app_dir, 'log', '--format=%s', '-1'), 'Test the missing key')
        return git(self.app_dir, 'rev-parse', 'HEAD')

    def test_a_new_test_in_tests_that_imports_a_helper_beside_it_proves_the_fix(self):
        clone = self.fix_clone('job1')
        (clone / 'tests').mkdir()
        (clone / 'tests' / 'test_graph_rows.py').write_text('EMPTY = {}\n')
        (clone / 'tests' / 'test_graph.py').write_text('import unittest\nimport graph\nfrom test_graph_rows import EMPTY\n\n\n'
                                                       'class Graph(unittest.TestCase):\n    def test_missing_key(self):\n'
                                                       '        self.assertIsNone(graph.rebuild(EMPTY))\n')
        git(clone, 'add', '.')
        git(clone, 'commit', '-qm', 'Test the missing key')
        self.assertTrue(self.save(clone)['auto_merge'].startswith('queued'))
        self.assertEqual(self.app.action_step(next_actions_transport(self)), 'sent')
        self.assertEqual(git(self.app_dir, 'log', '--format=%s', '-1'), 'Test the missing key')

    def test_a_fix_for_an_outside_service_failing_never_merges_by_itself(self):
        with self.store.connect() as db:
            db.execute('UPDATE events SET metadata=? WHERE id=1', (json.dumps({'fingerprint': 'fp-graph', 'outside': {'service': 'Google', 'status': 502}}),))
        saved = self.save(self.fix())
        self.assertIn('outside service', saved['auto_merge'])

    def test_a_small_tested_fix_merges_by_itself_and_the_owner_can_undo_it(self):
        start = git(self.upstream, 'rev-parse', 'main')
        head = self.merged()
        self.assertIn('Merged by itself and restarted. You can undo it for 24 hours', a.card(self.row()))
        self.assertIn('Kept on this machine, not pushed upstream', a.card(self.row()))
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), start)  # sharing it is the owner's call
        self.assertIn('Undo merge', self.labels())
        with self.assertRaisesRegex(ValueError, 'owner'):  # the agent cannot undo or redo it
            self.app.action('undo_merge', {'suggestion_id': self.sid, 'approval_id': 'agent'})
        self.app.action('undo_merge', {'suggestion_id': self.sid, 'approval_id': 'owner-undo'}, owner_dashboard=True)
        self.assertIn('Undoing the merge…', a.card(self.row()))
        self.assertEqual(self.app.undo_step(self.transport()), 'undone')
        self.assertIn('rows["missing"]', (self.app_dir / 'graph.py').read_text())
        self.assertFalse((self.app_dir / 'test_graph.py').exists())
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), start)  # neither the fix nor its undo went out
        self.assertTrue(git(self.app_dir, 'log', '--format=%s', '-1').startswith('Undo: The graph rebuild'))
        self.assertEqual(self.restarts, [1, 1])
        self.assertIn('Merge undone. The Machine restarts on the previous code.', a.card(self.row()))
        self.assertFalse({'Merge fix', 'Undo merge'} & set(self.labels()))
        self.assertTrue(self.app.action('undo_merge', {'suggestion_id': self.sid, 'approval_id': 'again'}, owner_dashboard=True)['duplicate'])
        self.assertNotEqual(head, git(self.app_dir, 'rev-parse', 'HEAD'))

    def test_a_fix_merged_by_itself_is_never_pushed_along_unless_allowed(self):
        start = git(self.upstream, 'rev-parse', 'main')
        self.merged()
        # The owner's next Merge doesn't carry the unshared fix upstream either.
        with self.store.connect() as db:
            db.execute("UPDATE action_jobs SET updated_at='2020-01-01T00:00:00+00:00'")
        clone = self.fixes / 'job2'
        subprocess.run(['git', 'clone', '-q', str(self.app_dir), str(clone)], check=True, capture_output=True)
        (clone / 'other.py').write_text('x = 2\n')
        git(clone, 'add', '.')
        git(clone, 'commit', '-qm', 'Another fix')
        action = n.validate({'kind': 'merge', 'clone': str(clone), 'summary': 'Another small fix to the service.'}, self.config, [])
        transport = self.transport()
        receipt = transport.send(action, {'id': 'job'})
        result = transport.complete(action, receipt)
        self.assertEqual((result['pushed'], result['held']), (None, 'unshared'))
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), start)
        # Allowed explicitly: a fix that merges by itself is pushed like any other.
        self.config['self_fix_auto_push'] = True
        git(self.app_dir, 'push', '-q')
        clone = self.fixes / 'job3'
        subprocess.run(['git', 'clone', '-q', str(self.app_dir), str(clone)], check=True, capture_output=True)
        (clone / 'other.py').write_text('x = 3\n')
        git(clone, 'commit', '-qam', 'Third fix')
        third = n.validate({'kind': 'merge', 'clone': str(clone), 'summary': 'A third small fix to the service.'}, self.config, [])
        approved={**third,'auto':True}
        self.assertEqual(transport.complete(approved,transport.send(approved,{'id':'job'}))['pushed'],True)
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), third['head'])
        self.assertEqual(transport.complete(third,transport.revert(third),'undo')['pushed'], True)  # a shared fix shares its undo
        self.assertEqual(git(self.upstream, 'rev-parse', 'main'), git(self.app_dir, 'rev-parse', 'HEAD'))

    def test_it_undoes_itself_when_the_fixed_error_comes_back(self):
        head = self.merged()
        self.store.record_fault('fp-other', 'KeyError', [], 'graph', 'oldversion0')  # the old code, before the restart
        self.assertIsNone(self.app.undo_step(self.transport()))
        self.store.record_fault('fp-graph', 'KeyError', [], 'graph', head[:12])
        self.assertEqual(self.app.undo_step(self.transport()), 'undone')
        self.assertIn('The error it fixed (KeyError) came back, so I undid the merge.', a.card(self.row()))
        self.assertIsNone(self.app.undo_step(self.transport()))  # once

    def test_it_undoes_itself_when_a_new_error_shows_up_right_after(self):
        head = self.merged()
        self.store.record_fault('fp-new', 'TypeError', [], 'digest', head[:12])
        self.assertEqual(self.app.undo_step(self.transport()), 'undone')
        self.assertIn('A new error (TypeError) showed up right after the merge, so I undid it.', a.card(self.row()))

    def test_anything_less_than_safe_waits_for_the_owner(self):
        action = {'kind': 'merge', 'files': ['graph.py', 'test_graph.py'], 'lines': 2, 'commits': 2, 'plugin': False, 'diff': '+x'}
        self.assertIsNone(n.unsafe_merge(action, {}))
        for change, reason in [({'files': ['graph.py']}, 'no test'), ({'plugin': True}, 'more than'), ({'files': ['AGENTS.md', 'test_graph.py']}, 'more than'),
                               ({'lines': 51}, 'bigger'), ({'files': ['a.py', 'b.py', 'c.py', 'd.py', 'test_a.py']}, 'bigger'),
                               ({'diff': '+        db.execute("ALTER TABLE events ADD x")'}, 'database')]:
            self.assertIn(reason, n.unsafe_merge({**action, **change}, {}))
        self.assertIn('off', n.unsafe_merge(action, {'self_fix_auto': False}))
        # A test that passes without the fix proves nothing: the card waits for Merge fix, which still works.
        self.assertTrue(self.save(self.fix(proof=False))['auto_merge'].startswith('queued'))
        self.assertEqual(self.app.action_step(next_actions_transport(self)), 'blocked')
        self.assertIn('doesn’t prove the fix. Not merged by itself. Tap Merge fix to merge it anyway.', a.card(self.row()))
        self.assertIn('Merge fix', self.labels())
        self.assertEqual(git(self.app_dir, 'log', '--format=%s', '-1'), 'Start')
        revision = self.row()['next_action']['revision']
        self.app.action('confirm_action', {'suggestion_id': self.sid, 'revision': revision, 'approval_id': 'owner-tap'}, owner_dashboard=True)
        self.assertEqual(self.app.action_step(next_actions_transport(self)), 'sent')
        self.assertIn('Merged. The Machine restarts with the fix.', a.card(self.row()))

    def test_only_fixes_to_its_own_errors_and_one_a_day(self):
        with self.store.connect() as db:
            db.execute("UPDATE events SET kind='gmail.message' WHERE id=1")
        self.assertIn('recorded errors', self.save(self.fix())['auto_merge'])
        with self.store.connect() as db:
            db.execute("UPDATE events SET kind='machine.fault' WHERE id=1")
            db.execute("INSERT INTO action_jobs VALUES('old','other','r','{\"kind\":\"merge\"}','sent',?,?,'owner','dashboard','','merge:abc',NULL,NULL)", (a.now(), a.now()))
        self.assertEqual(self.store.auto_merge(self.sid, self.config), 'another merge happened in the last day')


def next_actions_transport(test):
    return n.ActionTransport(None, None, merge=test.transport())


if __name__ == '__main__':
    unittest.main()

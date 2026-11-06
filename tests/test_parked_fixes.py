"""The Machine's own changes an update set aside (refs/machine/parked/, scripts/release.py) come back as to-dos, one
each and once, through the first Gateway source."""
import datetime as dt
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

import parked_fixes

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('parked_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
WHO = ['-c', 'user.name=t', '-c', 'user.email=t@example.invalid']
GATEWAY = {'id': 'openclaw-gateway', 'service': 'gateway'}


def git(app, *args):
    return subprocess.run(['git', *WHO, *args], cwd=app, check=True, capture_output=True, text=True).stdout.strip()


class NoJournal:
    def read(self, cursor=None, since=None):
        return []


class ParkedFixes(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.app = Path(tmp.name) / 'app'
        self.app.mkdir()
        git(self.app, 'init', '-q', '-b', 'main')
        self.start = self.commit('app.py', 'one', 'Start')
        self.store = a.Store(Path(tmp.name) / 'a.sqlite')
        self.config = {'accounts': [GATEWAY], 'app_dir': str(self.app)}

    def commit(self, name, text, subject, body=''):
        (self.app / name).write_text(text)
        git(self.app, 'add', name)
        git(self.app, 'commit', '-qm', subject + ('\n\n' + body if body else ''))
        return git(self.app, 'rev-parse', 'HEAD')

    def park(self, *shas):
        """Set aside as an update does: kept under PARKED, and the checkout moved on without them."""
        for sha in shas:
            git(self.app, 'update-ref', parked_fixes.PARKED + sha, sha)
        git(self.app, 'reset', '-q', '--hard', self.start)

    def todos(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT title, body FROM suggestions ORDER BY created_at, rowid')]

    def test_pending_lists_each_fix_and_leaves_out_a_fix_undone_with_it(self):
        fix = self.commit('graph.py', 'fixed', 'Graph: a KeyError on an empty name')
        other = self.commit('fleet.py', 'fixed', 'Fleet: the digest skips a day')
        undo = self.commit('fleet.py', 'back', 'Undo: Fleet: the digest skips a day', 'Machine-Undo: ' + other)
        (self.app / 'app.py').write_text('edited')
        changes = git(self.app, 'stash', 'create', 'Uncommitted changes set aside by an update')
        self.park(fix, other, undo, changes)
        found = parked_fixes.pending(self.app)
        self.assertEqual(sorted((f['sha'], f['changes'], f['subject']) for f in found),
                         sorted([(fix, False, 'Graph: a KeyError on an empty name'),
                                 (changes, True, 'On main: Uncommitted changes set aside by an update')]))
        self.assertEqual(parked_fixes.pending(self.app / 'nowhere'), [])

    def test_each_comes_back_as_a_to_do_once(self):
        fix = self.commit('graph.py', 'fixed', 'Graph: a KeyError on an empty name')
        self.park(fix)
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())  # the next sync: no second one
        [todo] = self.todos()
        self.assertEqual(todo['title'], 'Redo a fix the update set aside')
        self.assertIn('Ask to redo it on the new version', todo['body'])
        with self.store.connect() as db:
            event = db.execute("SELECT kind, version, analyzed_version, body FROM events WHERE source_id=?", ('parked:' + fix,)).fetchone()
        self.assertEqual(tuple(event)[:3], ('machine.parked_fix', 1, 1))  # read already: no review makes another to-do
        # what was kept is the signal, what to do is the to-do: the open to-do shows each once
        self.assertIn('“Graph: a KeyError on an empty name”', event['body'])
        self.assertIn(fix[:12], event['body'])
        self.assertNotIn(fix[:12], todo['body'])
        self.assertNotIn(todo['body'], event['body'])
        self.assertEqual(a.todo_source('machine.parked_fix'), 'The Machine itself')

    def test_one_still_on_the_checkout_is_left_out(self):
        # an update that parked a fix and then could not move: the fix never left, so there is nothing to redo
        fix = self.commit('graph.py', 'fixed', 'Graph: a fix')
        git(self.app, 'update-ref', parked_fixes.PARKED + fix, fix)
        self.assertEqual(parked_fixes.pending(self.app), [])
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        self.assertEqual(self.todos(), [])

    def test_only_the_first_gateway_source_brings_them(self):
        self.park(self.commit('graph.py', 'fixed', 'Graph: a fix'))
        a.sync_gateway(self.store, {'app_dir': str(self.app)}, GATEWAY, NoJournal())
        self.assertEqual(self.todos(), [])


if __name__ == '__main__':
    unittest.main()

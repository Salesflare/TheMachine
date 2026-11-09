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
        self.assertIn('Redo it on the new version', todo['body'])
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


    def test_files_an_update_renamed_come_back_as_one_to_do_per_update_once(self):
        release = 'a' * 40
        log = self.app / '.git' / parked_fixes.KEPT
        log.write_text(f'2026-11-06T04:00:00\t{release}\tnotes.md\tnotes.md.local-20261106\n'
                       f'2026-11-06T04:00:00\t{release}\ttools/run.sh\ttools/run.sh.local-20261106\n'
                       'not a record\n')
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())  # the next sync: no second one
        [todo] = self.todos()
        self.assertEqual(todo['title'], 'Your update kept 2 of your own files')
        self.assertIn(':\nnotes.md → notes.md.local-20261106\ntools/run.sh → tools/run.sh.local-20261106\n', todo['body'])  # one a line
        with self.store.connect() as db:
            [event] = db.execute("SELECT kind, body FROM events WHERE source_id=?", ('parked:kept-' + release,)).fetchall()
        self.assertEqual(event['kind'], 'machine.parked_fix')
        self.assertNotIn('notes.md', event['body'])  # the names once, in the to-do
        with self.store.connect() as db:
            row = dict(db.execute("SELECT * FROM suggestions WHERE dedupe_key=?", ('parked:kept-' + release,)).fetchone())
        self.assertEqual((row['origin'], row['source_line']), ('machine', None))  # no thread to read
        taps = [b['action']['value'].rsplit(':', 1)[1] for k in a.controls(row)['blocks'] for b in k['buttons']]
        self.assertEqual(taps, ['complete', 'snooze'])  # nothing to plan
        with log.open('a') as out:  # a later update that renamed one more: a to-do of its own
            out.write(f'2026-11-07T04:00:00\t{"b" * 40}\tUSER.md\tUSER.md.local-20261107\n')
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        self.assertEqual([t['title'] for t in self.todos()],
                         ['Your update kept 2 of your own files', 'Your update kept 1 of your own files'])

    def card(self):
        with self.store.connect() as db:
            card = dict(db.execute("SELECT * FROM suggestions WHERE dedupe_key LIKE 'parked:%' ORDER BY rowid DESC").fetchone())
            self.store.machine_fix_views(db, [card])
        return card

    def machine(self):
        app = object.__new__(a.App)
        app.store, app.config = self.store, {**self.config, 'fix_dir': str(self.app.parent / 'fixes')}
        return app

    def test_redo_it_leads_and_starts_the_usual_self_fix_run_from_the_set_aside_commit(self):
        fix = self.commit('graph.py', 'fixed', 'Graph: a KeyError on an empty name')
        self.park(fix)
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        card = self.card()
        self.assertEqual(card['parked_redo'], 'redo')  # nothing runs on it: the dashboard offers Redo it
        self.assertIn('Redo it on the new version', card['body'])
        labels = [b['label'] for k in a.controls(card)['blocks'] for b in k['buttons']]
        taps = [b['action']['value'].rsplit(':', 1)[1] for k in a.controls(card)['blocks'] for b in k['buttons']]
        self.assertEqual((labels, taps), (['Redo it', 'Mark done', 'Snooze'], ['accept', 'complete', 'snooze']))
        self.store.decide(card['id'], 'accept', '', 'd1', 'dashboard')
        calls = []
        self.machine().preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        [start] = calls
        message = start['message']
        # the usual self-fix: a clone of the running code, the set-aside commit fetched into it, saved as a merge to review
        self.assertIn(f'git clone {self.app} {self.app.parent / "fixes"}/', message)
        self.assertIn(f'git fetch {self.app} refs/machine/parked/{fix}', message)
        self.assertIn('{kind:merge,label:Merge fix', message)
        self.assertNotIn('only the owner can do themselves', message)  # not an owner-only step any more
        self.assertNotIn('send_now:true', message.split('Follow the preparation rules')[0])
        card = self.card()
        self.assertEqual([b['action']['value'].rsplit(':', 1)[1] for k in a.controls(card)['blocks'] for b in k['buttons']],
                         ['complete', 'snooze'])  # running: no second Redo it
        with self.store.connect() as db:
            owner, _ = self.machine().card_chat_service(db, card['id'])
        events = [i['text'] for i in owner if i['kind'] == 'event']
        self.assertEqual(events, ['Started redoing the fix'])  # what happened, without "You"

    def test_a_stuck_redo_offers_try_again(self):
        self.park(self.commit('graph.py', 'fixed', 'Graph: a fix'))
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        card = {**self.card(), 'status': 'accepted', 'preparation_status': 'blocked'}
        taps = [b['action']['value'].rsplit(':', 1)[1] for k in a.controls(card)['blocks'] for b in k['buttons']]
        self.assertEqual(taps, ['complete', 'retry', 'snooze'])
        card['preparation_reason'] = 'The tests fail on the new code.'  # with a reason: Answer leads, as on any to-do
        taps = [b['action']['value'].rsplit(':', 1)[1] for k in a.controls(card)['blocks'] for b in k['buttons']]
        self.assertIn('retry', taps)
        self.assertNotIn('accept', taps)

    def test_changes_and_kept_files_have_no_redo_it(self):
        (self.app / 'app.py').write_text('edited')
        changes = git(self.app, 'stash', 'create', 'Uncommitted changes set aside by an update')
        self.park(changes)
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        card = self.card()
        self.assertEqual(card['title'], 'Bring back changes the update set aside')
        self.assertNotIn('parked_redo', card)
        self.assertEqual([b['label'] for k in a.controls(card)['blocks'] for b in k['buttons']], ['Mark done', 'Snooze'])
        self.assertIsNone(parked_fixes.redoable({'commit': 'kept-' + 'a' * 40}))

    def test_once_the_redo_merged_the_set_aside_fix_goes(self):
        fix = self.commit('graph.py', 'fixed', 'Graph: a fix')
        self.park(fix)
        a.sync_gateway(self.store, self.config, GATEWAY, NoJournal())
        card = self.card()
        app = self.machine()

        class Merged:
            restart = None

            def complete(self, action, receipt, operation):
                return {'activation_ready': False}

        job = {'id': 'job1', 'suggestion_id': card['id'], 'error': None}
        with self.store.connect() as db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "VALUES('job1',?,'r1','{}','sent',?,?,'ap','dashboard','')", (card['id'], a.now(), a.now()))
        app.merge_effect({**job, 'id': 'undo1'}, {'kind': 'merge'}, {'commit': 'c' * 40}, 'undo', Merged())
        self.assertTrue(git(self.app, 'for-each-ref', parked_fixes.PARKED))  # an undo keeps it
        app.merge_effect(job, {'kind': 'merge'}, {'commit': 'c' * 40}, 'merge', Merged())
        self.assertEqual(git(self.app, 'for-each-ref', parked_fixes.PARKED), '')
        self.assertEqual(parked_fixes.pending(self.app), [])
        self.assertFalse(parked_fixes.drop(self.app, 'not a commit'))


if __name__ == '__main__':
    unittest.main()

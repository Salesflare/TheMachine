"""Signed releases (scripts/release.py): only a release tag signed with the pinned key is installed."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('release', HERE / 'scripts' / 'release.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
WHO = ['-c', 'user.name=t', '-c', 'user.email=t@example.invalid']


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class Releases(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.key, self.other = self.tmp / 'key', self.tmp / 'other'
        for k in (self.key, self.other):
            run('ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', 'test', '-f', str(k), cwd=self.tmp)
        self.origin, self.app = self.tmp / 'origin', self.tmp / 'app'
        self.origin.mkdir()
        run('git', 'init', '-q', '-b', 'main', cwd=self.origin)
        self.commit('one')
        run('git', 'clone', '-q', str(self.origin), str(self.app), cwd=self.tmp)
        (self.app / 'deploy').mkdir()
        self.signers = f'{release.PRINCIPAL} namespaces="git" {" ".join((self.key.with_suffix(".pub")).read_text().split()[:2])}\n'
        (self.app / 'deploy' / 'release-signers').write_text(self.signers)
        patch = mock.patch.multiple(release, ROOT=self.app, SIGNERS=self.app / 'deploy' / 'release-signers')
        patch.start()
        self.addCleanup(patch.stop)
        gate = mock.patch.object(release, 'require_release_scan', return_value={'gate_passed': True})
        self.gate = gate.start()
        self.addCleanup(gate.stop)

    def commit(self, text):
        (self.origin / 'app.py').write_text(text)
        run('git', 'add', '.', cwd=self.origin)
        run('git', *WHO, 'commit', '-qm', text, cwd=self.origin)
        return run('git', 'rev-parse', 'HEAD', cwd=self.origin)

    def tag(self, name, key=None, signed=True):
        sign = ['-c', 'gpg.format=ssh', '-c', f'user.signingkey={key or self.key}'] if signed else []
        run('git', *WHO, *sign, 'tag', '-s' if signed else '-a', '-m', name, name, cwd=self.origin)

    def test_a_signed_release_verifies_and_others_are_refused(self):
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        self.tag('release-20261021-1300', key=self.other)
        self.tag('release-20261021-1400', signed=False)
        run('git', 'fetch', '-q', '--tags', 'origin', cwd=self.app)
        self.assertEqual(release.verify('release-20261021-1200'), ('release-20261021-1200', sha))
        for tag, why in (('release-20261021-1300', 'not signed with the release key'), ('release-20261021-1400', 'not signed')):
            with self.assertRaisesRegex(release.Refused, why):
                release.verify(tag)

    def test_a_signed_tag_under_another_name_is_refused(self):
        self.tag('release-20261021-1200')
        raw = subprocess.run(['git', 'cat-file', 'tag', 'release-20261021-1200'], cwd=self.origin, capture_output=True).stdout
        release.signed_commit(raw, 'release-20261021-1200', self.signers)
        with self.assertRaisesRegex(release.Refused, 'does not name itself'):
            release.signed_commit(raw, 'release-20261022-1200', self.signers)  # an old release replayed as a new one
        with self.assertRaisesRegex(release.Refused, 'not signed with'):
            release.signed_commit(raw.replace(b'\n\nrelease', b'\n\nchanged'),
                                  'release-20261021-1200', self.signers)

    def test_update_takes_the_newest_signed_release_and_never_an_unsigned_one(self):
        good = self.commit('two')
        self.tag('release-20261021-1200')
        self.commit('three, unsigned')
        self.tag('release-20261021-1300', signed=False)
        with self.assertRaises(SystemExit) as refused:
            release.main(['update'])
        self.assertIn('Unsigned update refused', str(refused.exception))
        self.assertNotEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), good)
        release.main(['update', '--tag', 'release-20261021-1200'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), good)

    def test_a_first_install_starts_from_the_newest_signed_release_not_main(self):
        good = self.commit('two')
        self.tag('release-20261021-1200')
        self.commit('three, on main only')
        run('git', 'pull', '-q', '--ff-only', cwd=self.app)  # a fresh clone: main, ahead of the release
        self.assertEqual(release.first_install(), ('release-20261021-1200', good))
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), good)
        self.assertEqual((self.app / 'app.py').read_text(), 'two')
        self.assertIsNone(release.first_install())  # the release's own installer: already there

    def test_a_first_install_with_no_signed_release_changes_nothing(self):
        self.commit('two')
        self.tag('release-20261021-1200', key=self.other)
        run('git', 'pull', '-q', '--ff-only', cwd=self.app)
        before = run('git', 'rev-parse', 'HEAD', cwd=self.app)
        with self.assertRaisesRegex(release.Refused, 'not signed with the release key'):
            release.first_install()
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), before)

    def own_commit(self, name, text):
        (self.app / name).write_text(text)
        run('git', 'add', name, cwd=self.app)
        run('git', *WHO, 'commit', '-qm', 'own: ' + name, cwd=self.app)

    def test_update_replays_the_machines_own_commits_on_the_release(self):
        self.own_commit('fix.py', 'a merged self-fix')
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        release.main(['update'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD^', cwd=self.app), sha)
        self.assertEqual((self.app / 'fix.py').read_text(), 'a merged self-fix')
        self.assertEqual((self.app / 'app.py').read_text(), 'two')
        release.main(['update'])  # nothing new: stays
        self.assertEqual(run('git', 'rev-parse', 'HEAD^', cwd=self.app), sha)

    def parked(self):
        out = run('git', 'for-each-ref', '--format=%(refname) %(objectname)', release.PARKED, cwd=self.app)
        return [line.split() for line in out.splitlines()]

    def test_own_commits_that_do_not_apply_are_set_aside_and_the_update_goes_on(self):
        self.own_commit('app.py', 'mine')
        own = run('git', 'rev-parse', 'HEAD', cwd=self.app)
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        with mock.patch('builtins.print') as said:
            release.main(['update'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), sha)  # never stuck on the old version
        self.assertEqual((self.app / 'app.py').read_text(), 'two')
        self.assertEqual(run('git', 'status', '--porcelain', '--untracked-files=no', cwd=self.app), '')
        self.assertEqual(self.parked(), [[release.PARKED + own, own]])  # kept, to come back as a to-do
        self.assertIn('set aside', said.call_args[0][0])
        release.main(['update'])  # nothing new: stays, nothing more set aside
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), sha)
        self.assertEqual(len(self.parked()), 1)

    def test_uncommitted_changes_in_the_way_are_set_aside(self):
        (self.app / 'app.py').write_text('edited here')
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        release.main(['update'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), sha)
        self.assertEqual((self.app / 'app.py').read_text(), 'two')
        [(name, kept)] = self.parked()
        self.assertEqual(run('git', 'show', f'{kept}:app.py', cwd=self.app), 'edited here')

    def test_changes_out_of_the_way_stay_and_own_commits_still_replay(self):
        self.own_commit('fix.py', 'a merged self-fix')
        (self.app / 'app.py').write_text('edited here')  # in the way of the release
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        release.main(['update'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD^', cwd=self.app), sha)  # the fix applies, so it stays
        self.assertEqual((self.app / 'fix.py').read_text(), 'a merged self-fix')
        self.assertEqual(len(self.parked()), 1)  # only the changes went aside
        # changes nothing touches are kept in place, as before
        (self.app / 'fix.py').write_text('still editing')
        self.commit('three')
        self.tag('release-20261021-1300')
        release.main(['update'])
        self.assertEqual((self.app / 'fix.py').read_text(), 'still editing')
        self.assertEqual(len(self.parked()), 1)

    def own_sha(self, name, text):
        self.own_commit(name, text)
        return run('git', 'rev-parse', 'HEAD', cwd=self.app)

    def test_only_the_own_commits_that_do_not_apply_are_set_aside(self):
        first = self.own_sha('fix.py', 'applies')
        clash = self.own_sha('app.py', 'mine')
        last = self.own_sha('z.py', 'applies too')
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        release.main(['update'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD~2', cwd=self.app), sha)  # the two that apply, on the release
        self.assertEqual(run('git', 'log', '--format=%s', '-2', cwd=self.app).split('\n'), ['own: z.py', 'own: fix.py'])
        self.assertEqual((self.app / 'app.py').read_text(), 'two')
        self.assertEqual(self.parked(), [[release.PARKED + clash, clash]])
        self.assertNotIn(first, run('git', 'rev-list', 'HEAD', cwd=self.app))  # replayed as new commits, refs dropped
        self.assertNotIn(last, run('git', 'rev-list', 'HEAD', cwd=self.app))

    def test_a_rerun_after_a_run_cut_off_mid_rebase_loses_no_commit(self):
        first = self.own_sha('fix.py', 'applies')
        clash = self.own_sha('app.py', 'mine')
        last = self.own_sha('z.py', 'applies too')
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        run('git', 'fetch', '-q', '--tags', 'origin', cwd=self.app)
        subprocess.run(['git', *WHO, 'rebase', '-q', '--onto', sha, first + '^'], cwd=self.app, capture_output=True)
        self.assertTrue((self.app / '.git' / 'rebase-merge').exists())  # stopped on the clash, as a killed run leaves it
        release.main(['update'])
        self.assertFalse((self.app / '.git' / 'rebase-merge').exists())
        self.assertEqual(run('git', 'rev-parse', 'HEAD~2', cwd=self.app), sha)
        self.assertTrue((self.app / 'fix.py').exists() and (self.app / 'z.py').exists())
        self.assertEqual(self.parked(), [[release.PARKED + clash, clash]])  # a full sha: no "needs merge" ref
        release.main(['update'])  # and the next update still works
        self.assertEqual(run('git', 'rev-parse', 'HEAD~2', cwd=self.app), sha)

    def test_a_run_cut_off_after_the_checkout_moved_keeps_the_own_commits(self):
        own = self.own_sha('fix.py', 'a merged self-fix')
        (self.app / 'app.py').write_text('edited here')
        self.commit('two')
        self.tag('release-20261021-1200')
        real = release.git

        def cut_off(*args, **kwargs):
            if 'cherry-pick' in args:
                raise KeyboardInterrupt('the service stopped')
            return real(*args, **kwargs)
        with mock.patch.object(release, 'git', cut_off), self.assertRaises(KeyboardInterrupt):
            release.main(['update'])
        kept = dict(self.parked())
        self.assertEqual(kept.pop(release.PARKED + own), own)  # the own commit and the changes both kept
        [changes] = kept.values()
        self.assertEqual(run('git', 'show', f'{changes}:app.py', cwd=self.app), 'edited here')

    def test_the_service_reads_the_same_folder(self):
        import parked_fixes
        self.assertEqual(parked_fixes.PARKED, release.PARKED)

    def test_install_waits_while_something_runs_and_then_installs(self):
        sha = self.commit('two')
        self.tag('release-20261021-1200')
        installs = []
        real = subprocess.run
        def fake(args, **kwargs):
            if str(args[0]).endswith('install.sh'):
                installs.append(args[1:])
                return subprocess.CompletedProcess(args, 0)
            return real(args, **kwargs)
        with mock.patch.object(release, 'busy', return_value=True), mock.patch.object(release.subprocess, 'run', fake):
            release.main(['update', '--install'])
        self.assertNotEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), sha)
        self.assertEqual(installs, [])
        with mock.patch.object(release, 'busy', return_value=False), mock.patch.object(release.subprocess, 'run', fake):
            release.main(['update', '--install'])
        self.assertEqual(run('git', 'rev-parse', 'HEAD', cwd=self.app), sha)
        self.assertEqual(installs, [['--non-interactive']])

    def test_cut_signs_origin_main_with_the_key_and_verifies_it(self):
        sha = self.commit('two')
        release.main(['cut', '--key', str(self.key), '--no-push'])
        self.gate.assert_called_once_with('TheMachine', sha, cwd=self.app)
        tags = release.releases()
        self.assertEqual(len(tags), 1)
        self.assertEqual(release.verify(tags[0])[1], sha)
        release.main(['cut', '--key', str(self.key), '--no-push'])  # nothing new on main: no second tag
        self.assertEqual(release.releases(), tags)
        self.gate.assert_called_once()

    def test_failed_scan_never_creates_or_pushes_a_release(self):
        self.commit('two')
        self.gate.side_effect = RuntimeError('scan did not pass')
        with self.assertRaisesRegex(SystemExit, 'Not released: scan did not pass'):
            release.main(['cut', '--key', str(self.key)])
        self.assertEqual(release.releases(), [])
        self.assertEqual(run('git', 'tag', '--list', cwd=self.origin), '')

    def test_cut_with_a_key_that_is_not_pinned_tags_nothing(self):
        self.commit('two')
        with self.assertRaises(SystemExit) as refused:
            release.main(['cut', '--key', str(self.other), '--no-push'])
        self.assertIn('Not released', str(refused.exception))
        self.assertEqual(release.releases(), [])


if __name__ == '__main__':
    unittest.main()

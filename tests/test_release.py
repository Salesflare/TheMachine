"""Signed releases (scripts/release.py): only a release tag signed with the pinned key is installed."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent.parent
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

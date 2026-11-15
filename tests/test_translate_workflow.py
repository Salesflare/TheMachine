"""The daily translation (.github/workflows/translate.yml) never pushes translations built on a main that moved on.

A run that queued behind the last one built on main without that run's pull request, translated the same strings again,
and pushed after that pull request merged: the new pull request conflicted with main, GitHub started no tests for it,
and it could never merge. These tests run the step's own shell against a scratch repository whose main moves."""
import pathlib
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLOW = ROOT / '.github/workflows/translate.yml'


def steps():
    """name -> the step's text, in order (the checkout step is named by its action)."""
    text = FLOW.read_text()
    jobs = text[text.index('\n    steps:\n'):text.index('\n  failed:\n')]
    out = {}
    for part in re.split(r'\n      - ', jobs)[1:]:
        name = re.match(r'(?:name: (.+)|uses: (\S+))', part)
        out[name.group(1) or name.group(2).split('@')[0]] = part
    return out


def run_block(step):
    return textwrap.dedent(step[step.index('run: |\n') + len('run: |\n'):])


def git(cwd, *args):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class TranslateWorkflowTest(unittest.TestCase):
    def test_waits_for_the_open_pull_request_before_checking_out(self):
        names = list(steps())
        self.assertLess(names.index('Let the open pull request merge first'), names.index('actions/checkout'))
        wait = steps()['Let the open pull request merge first']
        self.assertIn('select(.autoMergeRequest != null)', wait)
        self.assertIn('seq 1 60', wait)  # bounded: then this run replaces it, as before

    def test_approve_loop_names_a_conflict(self):
        pr = steps()['Open or update the pull request']
        self.assertIn('[ "$mergeable" = CONFLICTING ]', pr)
        self.assertIn('conflicts with main', pr)
        self.assertLess(pr.index('git fetch --quiet --no-tags origin main'), pr.index('git push'))

    @unittest.skipUnless(shutil.which('bash') and shutil.which('git'), 'needs bash and git')
    def test_step_scripts_parse(self):
        for name, step in steps().items():
            if 'run: |' in step:
                script = re.sub(r'\$\{\{[^}]*\}\}', 'x', run_block(step))
                subprocess.run(['bash', '-n'], input=script, text=True, check=True)

    def rebuild(self, main_change):
        """The step's rebuild-on-main part, on a scratch clone whose main gets main_change after the run checked out.
        Returns (clone, main's head, the script's output)."""
        pr = run_block(steps()['Open or update the pull request'])
        start = pr.index('git fetch --quiet --no-tags origin main')
        block = pr[start:pr.index('\nfi\n', start) + 4]
        tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        origin, work = tmp / 'origin', tmp / 'work'
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(origin)], check=True)
        for path, text in {
            'i18n/de.json': '{"a": "A"}\n',
            'docs/help/de/start.md': '# Start\n',
            # stand-ins: the translator writes the missing key; the checks pass
            'scripts/translate.py': "import pathlib\np = pathlib.Path('i18n/de.json')\n"
                                    "if '\"b\"' not in p.read_text(): p.write_text(p.read_text()[:-2] + ', \"b\": \"B (again)\"}\\n')\n",
            'scripts/help_check.py': '',
            'tests/test_i18n.py': 'import unittest\n\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n',
        }.items():
            (origin / path).parent.mkdir(parents=True, exist_ok=True)
            (origin / path).write_text(text)
        for args in (('config', 'user.name', 't'), ('config', 'user.email', 't@example.invalid'), ('add', '-A'), ('commit', '-qm', 'start')):
            git(origin, *args)
        subprocess.run(['git', 'clone', '-q', str(origin), str(work)], check=True)
        git(work, 'config', 'user.name', 't')
        git(work, 'config', 'user.email', 't@example.invalid')
        git(work, 'switch', '-q', '-C', 'translate/daily')
        (work / 'i18n/de.json').write_text('{"a": "A", "b": "B"}\n')  # this run's translation
        git(work, 'commit', '-qam', 'translations')
        main_change(origin)
        out = subprocess.run(['bash', '-e', '-c', block + 'echo PUSH\n'], cwd=work, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return work, git(origin, 'rev-parse', 'main'), out.stdout

    def test_main_moved_elsewhere_rebases_onto_it(self):
        def other(origin):
            (origin / 'notes.txt').write_text('x\n')
            git(origin, 'add', '-A')
            git(origin, 'commit', '-qm', 'other')
        work, main, out = self.rebuild(other)
        self.assertEqual(git(work, 'rev-parse', 'HEAD~1'), main)
        self.assertIn('"b": "B"', (work / 'i18n/de.json').read_text())
        self.assertIn('PUSH', out)

    def test_main_changed_the_same_files_translates_again_on_it(self):
        def same(origin):
            (origin / 'i18n/de.json').write_text('{"a": "A", "c": "C"}\n')
            git(origin, 'commit', '-qam', 'the last run merged')
        work, main, out = self.rebuild(same)
        self.assertIn('translating again', out)
        self.assertEqual(git(work, 'rev-parse', 'HEAD~1'), main)
        self.assertEqual((work / 'i18n/de.json').read_text(), '{"a": "A", "c": "C", "b": "B (again)"}\n')
        self.assertNotIn('<<<<<<<', (work / 'i18n/de.json').read_text())

    def test_main_has_it_all_already_pushes_nothing(self):
        def merged(origin):
            (origin / 'i18n/de.json').write_text('{"a": "A", "b": "B"}\n')
            git(origin, 'commit', '-qam', 'the last run merged')
        work, main, out = self.rebuild(merged)
        self.assertIn('nothing to push', out)
        self.assertNotIn('PUSH', out)
        self.assertEqual(git(work, 'rev-parse', 'HEAD'), main)


if __name__ == '__main__':
    unittest.main()

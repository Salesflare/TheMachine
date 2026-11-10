"""scripts/test_select.py: a pull request runs the tests its change needs, and never skips one that change can break.
Each check here finds the tests that depend on a change in its own simple way (a grep) and makes sure the selection
has them all."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('test_select', ROOT / 'scripts' / 'test_select.py')
select = importlib.util.module_from_spec(spec)
spec.loader.exec_module(select)

REPO = select.Repo(select.tracked())
TESTS = sorted(path for path in REPO.paths if select.is_test(path))
SOURCE = {path: (ROOT / path).read_text(encoding='utf-8', errors='replace') for path in TESTS}


def picked(*changed):
    return select.select(list(changed), repo=REPO)


def names(paths):
    return {Path(path).name for path in paths}


class Selection(unittest.TestCase):
    def assertRuns(self, changed, needed):
        got = picked(*changed)
        if got is None:
            return  # everything runs
        missing = sorted(names(needed) - set(got))
        self.assertEqual(missing, [], f'{changed} skips tests that depend on it')

    def test_the_test_machinery_runs_everything(self):
        for path in ('scripts/test.py', 'scripts/test_select.py', '.github/workflows/ci.yml', 'package-lock.json', 'tests/test-env.mjs'):
            self.assertIsNone(picked(path), path)

    def test_a_file_nothing_names_runs_everything(self):
        # names put together here, so this file doesn't name them itself
        self.assertIsNone(picked('some-new-' + 'tool.cfg'))
        self.assertIsNone(picked('brand-new-' + 'helper.mjs'))

    def test_a_changed_test_runs_with_the_repository_checks(self):
        got = picked('tests/test_moving.py')
        self.assertIsNotNone(got)
        self.assertIn('test_moving.py', got)
        self.assertLessEqual(set(select.ALWAYS) & names(TESTS), set(got))
        self.assertLess(len(got), 30)

    def test_a_python_module_runs_every_test_that_imports_or_runs_it(self):
        # every test that imports the module by name (also inside python -c in a Node test) or names its file in quotes
        # every 8th module (each one is a full selection, a few seconds on a busy runner), plus ones loaded in odd ways
        modules = [path for path in REPO.paths if path.endswith('.py') and not path.startswith(('tests/', 'scripts/'))][::8]
        modules += ['qr.py', 'i18n.py', 'connectors/trello.py', 'integrations/browser_cdp.py', 'machine/store/conversation.py', 'onboarding.py']
        for path in dict.fromkeys(modules):
            mod = select.module_name(path)
            last = mod.rsplit('.', 1)
            pattern = re.compile(r'\b(?:import|from)\s+' + re.escape(mod) + r'\b'
                                 + (r'|\bfrom\s+' + re.escape(last[0]) + r'\s+import\s+[^\n]*\b' + re.escape(last[1]) + r'\b' if len(last) == 2 else '')
                                 + r'''|['"/]''' + re.escape(Path(path).name) + r'''['"]''')
            needed = [test for test, text in SOURCE.items() if pattern.search(text)]
            with self.subTest(module=path):
                self.assertRuns([path], needed)

    def test_a_module_reached_through_another_runs_that_ones_tests(self):
        # machine/store/conversation.py reaches the tests through assistant.py, which loads it
        needed = [test for test, text in SOURCE.items() if "'assistant.py'" in text or re.search(r'^\s*import assistant\b', text, re.M)]
        self.assertTrue(needed)
        self.assertRuns(['machine/store/conversation.py'], needed)

    def test_a_dashboard_part_runs_every_test_that_loads_the_page(self):
        needed = [test for test, text in SOURCE.items() if 'dashboard-page.mjs' in text or 'dashboard.html' in text]
        self.assertGreater(len(needed), 100)
        for part in ('dashboard/todos-snooze.js', 'dashboard/shell-core.js', 'dashboard/settings-panels.html', 'dashboard/todos-cards.css', 'dashboard.html'):
            with self.subTest(part=part):
                self.assertRuns([part], needed)

    def test_a_catalog_runs_the_tests_that_serve_the_catalogs(self):
        needed = [test for test, text in SOURCE.items() if 'i18n' in text]
        self.assertTrue(needed)
        self.assertRuns(['i18n/de.json'], needed)

    def test_a_help_article_runs_the_help_tests(self):
        needed = [test for test, text in SOURCE.items() if 'docs/help' in text or "'help'" in text and "'docs'" in text]
        self.assertTrue(needed)
        got = picked('docs/help/weekly-recap.md')
        self.assertIsNotNone(got, 'a help article alone runs only what reads help articles')
        self.assertRuns(['docs/help/weekly-recap.md'], needed)

    def test_a_deleted_module_runs_its_importers(self):
        repo = select.Repo(REPO.paths, extra_modules=['qr.py'])
        got = select.select(['qr.py'], repo=repo)
        if got is not None:
            self.assertIn('test_setup_card_dashboard.mjs', got)  # python -c 'import qr'

    def test_a_python_change_leaves_the_browser_tests_that_never_run_python(self):
        got = picked('machine/store/conversation.py')
        self.assertIsNotNone(got)
        self.assertNotIn('test_export_dashboard.mjs', got)

    def test_every_test_that_looks_over_the_repository_runs_always(self):
        # a test that walks every file, or a whole folder of the repository, can fail on a new file nothing names
        walks = re.compile(r'''ROOT\.rglob\(|git', 'ls-files'|\(ROOT / '[\w-]+'\)\.r?glob\(|joinpath\('(?:connectors|integrations)'\)\.glob\(''')
        walkers = sorted(Path(test).name for test, text in SOURCE.items() if walks.search(text))
        self.assertTrue(walkers)
        self.assertEqual(sorted(set(walkers) - select.ALWAYS), [], 'add these to ALWAYS in scripts/test_select.py')
        self.assertEqual(sorted(select.ALWAYS - names(TESTS)), [], 'ALWAYS names a test that is gone')


MODULE = '''"""doc"""
import json
LIMIT = 3


@register
def helper(x=LIMIT):
    return x


class Box:
    size = 2

    def fill(self):
        def inner():
            return json.dumps(self.size)
        return inner()


def make():
    class Handler:
        def get(self):
            return 'page'
    return Handler
'''


class WithTheMap(unittest.TestCase):
    """With the test-impact map, a change runs the tests that ran what it changed."""

    def setUp(self):
        self.patched = {name: getattr(select, name) for name in ('diff_lines', 'git_text')}

    def tearDown(self):
        for name, value in self.patched.items():
            setattr(select, name, value)

    def impact(self, ran, skip=()):
        tests = sorted(Path(t).name for t in TESTS if Path(t).name not in skip)
        index = {name: i for i, name in enumerate(tests)}
        files = {}
        for (path, qualname), names in ran.items():
            files.setdefault(path, {})[qualname] = [index[n] for n in names]
        return select.Impact({'tests': tests, 'known': [p for p in REPO.paths if p.endswith('.py')], 'files': files})

    def change(self, path, lines):
        text = (ROOT / path).read_text(encoding='utf-8')
        select.git_text = lambda base, p: text if p == path else None
        select.diff_lines = lambda base, p: (set(lines), set(lines)) if p == path else (set(), set())

    def test_where_each_line_sits(self):
        scopes = select.Scopes(MODULE)
        line = {text.strip(): n for n, text in enumerate(MODULE.split('\n'), 1)}
        self.assertEqual(scopes.at(line['return x']), ('func', 'helper'))
        self.assertEqual(scopes.at(line['@register']), ('func', 'helper'))
        self.assertEqual(scopes.at(line['def helper(x=LIMIT):']), ('func', 'helper'))
        self.assertEqual(scopes.at(line['LIMIT = 3']), ('names', {'LIMIT'}))
        self.assertEqual(scopes.at(line['import json']), ('local', {'json'}))
        self.assertEqual(scopes.at(line['size = 2']), ('names', {'size'}))
        self.assertEqual(scopes.at(line['return json.dumps(self.size)']), ('func', 'Box.fill.<locals>.inner'))
        self.assertEqual(scopes.at(line['return inner()']), ('func', 'Box.fill'))
        self.assertEqual(scopes.at(line["return 'page'"]), ('func', 'make.<locals>.Handler.get'))  # as co_qualname
        self.assertIsNone(scopes.at(line['"""doc"""']))

    def test_a_changed_function_runs_the_tests_that_ran_it(self):
        path = 'i18n.py'
        scopes = select.Scopes((ROOT / path).read_text(encoding='utf-8'))
        start, end, qualname = next(f for f in scopes.funcs if '.' not in f[2] and f[1] - f[0] > 1)
        self.change(path, [start + 1])
        readers = {Path(t).name for t in REPO.named_by(path) if select.is_test(t)}
        impact = self.impact({(path, qualname): ['test_moving.py'], (path, '_other'): sorted(readers)})
        got = select.select([path], repo=REPO, impact=impact, base='HEAD')
        self.assertIsNotNone(got)
        self.assertIn('test_moving.py', got)
        self.assertLessEqual(set(select.ALWAYS) & names(TESTS), set(got))
        self.assertEqual(sorted(set(got) - select.ALWAYS - {'test_moving.py'}), [])

    def test_a_test_the_map_does_not_know_follows_imports(self):
        path = 'machine/store/conversation.py'
        self.change(path, [1])
        old = set(select.select([path], repo=REPO) or ())
        new_test = sorted(old - select.ALWAYS)[0]
        got = select.select([path], repo=REPO, impact=self.impact({}, skip={new_test}), base='HEAD')
        self.assertIn(new_test, got)

    def test_a_catalog_change_runs_the_tests_that_name_its_text(self):
        text = 'A sentence no test names, ' + 'made up here'
        strings = select.catalog_strings('{"Done": "Klaar"}', '{"Done": "Gedaan", "%s": "x"}' % text)
        self.assertEqual(strings, {'Done', 'Klaar', 'Gedaan', text, 'x'})
        pattern = select.text_pattern({'Snoozed {what} until {when}'})
        self.assertTrue(pattern.search("expect(text).toContain('Snoozed the to-do until')"))
        self.assertFalse(select.text_pattern({'OK'}).search('BROKEN'))

    def test_a_catalog_alone_runs_the_catalog_checks_and_the_tests_that_name_its_text(self):
        import json
        catalog = json.loads((ROOT / 'i18n' / 'en.json').read_text(encoding='utf-8'))
        key = sorted(catalog)[len(catalog) // 2]
        before = dict(catalog, **{key: catalog[key] + ' (before)'})
        select.git_text = lambda base, p: json.dumps(before) if p == 'i18n/en.json' else None
        got = select.select(['i18n/en.json'], repo=REPO, impact=self.impact({}), base='HEAD')
        self.assertIsNotNone(got)
        pattern = select.text_pattern({key, catalog[key], before[key]})
        allowed = select.ALWAYS | {Path(t).name for t in TESTS if select.CATALOG_CHECKS.search(Path(t).name)
                                   or pattern.search(SOURCE[t])}
        self.assertEqual(sorted(set(got) - allowed), [])
        self.assertIn('test_i18n.py', got)

    def test_a_folder_names_the_files_on_the_way_to_it(self):
        self.assertTrue(select.names_exactly("HELP = ROOT / 'docs' / 'help'", 'docs/help/history.md'))
        self.assertTrue(select.names_exactly("open('docs/help/' + name)", 'docs/help/history.md'))
        self.assertFalse(select.names_exactly('See docs/development.md.', 'docs/code-map.md'))
        self.assertFalse(select.names_exactly("ROOT / 'docs' / 'brand'", 'docs/help/history.md'))


if __name__ == '__main__':
    unittest.main()

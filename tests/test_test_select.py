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
        needed = [test for test, text in SOURCE.items() if 'docs/help' in text or re.search(r"""['"]docs['"]\s*/\s*['"]help['"]""", text)]
        self.assertTrue(needed)
        got = picked('docs/help/weekly-recap.md')
        self.assertIsNotNone(got, 'a help article alone runs only what reads help articles')
        self.assertRuns(['docs/help/weekly-recap.md'], needed)

    def test_a_doc_runs_the_tests_of_what_reads_its_folder_not_all_that_loads_those(self):
        # assistant.py reads docs/ for its own reasons: a doc reaches its tests, not every test that imports it
        for path in ('docs/code-map.md', 'docs/help/routines.md'):
            got = picked(path)
            self.assertIsNotNone(got)
            self.assertLess(len(got), 150, path)
            self.assertIn('test_help.py', got)

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
        self.patched = {name: getattr(select, name) for name in ('diff_lines', 'git_text', 'map_text')}

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

    def test_a_short_piece_of_a_text_is_found_only_with_the_rest(self):
        pattern = select.text_pattern({'{} and {} more'})
        self.assertTrue(pattern.search("toContain('Ann and 2 more')"))
        self.assertFalse(pattern.search("// a Show more button"))
        self.assertFalse(pattern.search("expect(more).toBe(true)"))
        self.assertTrue(select.text_pattern({'Matched to people in your Graph: {}'}).search('Matched to people in your Graph: 3'))
        self.assertEqual(select.without_comments("a\n  # more\n// more\nb"), 'a\n\n\nb')

    def test_a_plural_text_counts_with_its_forms(self):
        changes = select.catalog_changes('{"Keep": "Hou"}', '{"Keep": "Hou", "Add {} people": {"one": "Add {} person", "other": "Add {} people"}}')
        self.assertEqual(changes, {'Add {} people': {'Add {} people', 'Add {} person'}})

    def catalog_key(self):
        """A key of the English catalog quoted in just one Python file the map knows, in a function."""
        import json
        catalog = json.loads((ROOT / 'i18n' / 'en.json').read_text(encoding='utf-8'))
        python = {p: REPO.text[p] for p in REPO.paths if p.endswith('.py') and not p.startswith(('tests/', 'scripts/')) and p in REPO.text}
        for key in sorted(catalog)[::7]:
            if len(key) < 25 or not isinstance(catalog[key], str):
                continue
            forms = [q + key + q for q in '\'"`']
            if any(key in t for p, t in REPO.text.items() if not p.endswith('.py') and not select.is_test(p)):
                continue
            where = [p for p, t in python.items() if any(f in t for f in forms)]
            if len(where) != 1:
                continue
            text = python[where[0]]
            line = text.count('\n', 0, min(text.find(f) for f in forms if f in text)) + 1
            scope = select.Scopes(text).at(line)
            if scope and scope[0] == 'func':
                return catalog, key, where[0], scope[1]
        self.skipTest('no key quoted in one function only')

    def test_a_catalog_text_runs_the_tests_that_draw_it_and_assert_it(self):
        import json
        catalog, key, path, qualname = self.catalog_key()
        before = dict(catalog, **{key: catalog[key] + ' (before)'})
        select.git_text = lambda base, p: json.dumps(before) if p == 'i18n/en.json' else None
        current = REPO.text[path]
        select.map_text = lambda commit, p: current if p == path else None
        pattern = select.text_pattern({key, before[key]})
        asserts = {Path(t).name for t in TESTS if pattern.search(select.without_comments(SOURCE[t]))}
        drawer = sorted(asserts - select.ALWAYS)[:1] or ['test_moving.py']
        got = select.select(['i18n/en.json'], repo=REPO, impact=self.impact({(path, qualname): drawer}), base='HEAD')
        named = {Path(t).name for t in TESTS if any(q + key + q in SOURCE[t] for q in '\'"`')}
        allowed = select.ALWAYS | named | set(drawer) | {Path(t).name for t in TESTS if select.CATALOG_CHECKS.search(Path(t).name)}
        self.assertEqual(sorted(set(got) - allowed), [])
        self.assertIn('test_i18n.py', got)
        # where the map can't place it (the file changed since the map), every test that asserts the text runs
        select.map_text = lambda commit, p: None
        got = select.select(['i18n/en.json'], repo=REPO, impact=self.impact({(path, qualname): drawer}), base='HEAD')
        self.assertLessEqual(asserts, set(got))

    def test_css_rules_and_the_names_they_need(self):
        css = '/* x{} */\n.a{b:1}\n@media (max-width:5px){.c .d,#e:not(.f){g:2}}\n@keyframes k{from{o:0}to{o:1}}\n'
        rules = select.css_rules(css)
        self.assertEqual([r[2] for r in rules], ['.a', '.c .d,#e:not(.f)', '@keyframes k'])
        self.assertEqual(rules[1][3], [(css.index('\n@media'), css.index('{.c') + 1)])
        self.assertEqual(select.css_tokens('.c .d,#e:not(.f)'), [{'c', 'd'}, {'e'}])
        self.assertEqual(select.css_tokens('.x button[aria-pressed="true"]'), [{'x', 'aria-pressed'}])
        # a rule with only a tag: where markup or code makes that element
        self.assertEqual(select.css_tokens('.x,button:hover'), [{'x'}, {'<button'}])
        self.assertEqual(select.css_tokens('option,select optgroup'), [{'<option'}, {'<optgroup'}])
        self.assertTrue(all(select.token_word('<option').search(t) for t in ('`<option value=1>`', 'new Option(a)', "createElement('option')")))
        self.assertFalse(select.token_word('<option').search('<options>'))
        self.assertEqual(select.css_tokens(':is(.model-pick,.select-like) svg'), [{'model-pick'}, {'select-like'}])
        self.assertIsNone(select.css_tokens(':root'))
        self.assertIsNone(select.css_tokens('body'))
        self.assertIsNone(select.css_tokens('*'))
        self.assertIsNone(select.css_tokens('@keyframes k'))
        self.assertIsNone(select.css_rules('.a{'))
        self.assertTrue(select.token_word('data-mail-check').search('b.dataset.mailCheck'))
        html = '<p class="x">\n<dialog id="d1" aria-label="a"><p class="x y"></p></dialog><dialog id="d2" open><b class="z"></b></dialog>'
        self.assertEqual(select.closed_dialogs(html, select.token_word('y')), {'d1'})
        self.assertIsNone(select.closed_dialogs(html, select.token_word('x')))  # one is on show at load
        self.assertIsNone(select.closed_dialogs(html, select.token_word('z')))  # an open dialog
        # a hidden panel holds it too; an include line names a file, not an element
        html = '<script>/*@include dashboard/p-x.js*/</script><div id="p-x" hidden><b class="w"></b></div>'
        self.assertEqual(select.closed_dialogs(html, select.token_word('w')), {'p-x'})
        self.assertEqual(select.closed_dialogs(html, select.token_word('p-x')), {'p-x'})
        self.assertTrue(select.TABLE_LINE.fullmatch("'graph_role': 'graph_role_action', 'graph_same': 'graph_same_action',"))
        self.assertFalse(select.TABLE_LINE.fullmatch("'graph_role': role_action(),"))

    def page_map(self, part, ran):
        """A map whose browser half knows part as it is now: one function, all of it, that the test ran ran; every page
        test loaded it."""
        text = (ROOT / part).read_text(encoding='utf-8')
        pages = sorted(Path(t).name for t in TESTS if t.endswith('_dashboard.mjs'))
        impact = self.impact({})
        at = {name: i for i, name in enumerate(impact.tests)}
        impact.commit = 'map'
        impact.js = {part: {'top': [at[t] for t in pages], 'funcs': [[0, len(text), [at[ran]]]]}}
        impact.js_tests = set(pages)
        select.map_text = lambda commit, p: text if p == part else None
        idle = next(t for t in pages if t != ran and not re.search(r'mail-check|mc-line|mailCheck', SOURCE['tests/' + t]))
        return impact, idle

    def test_a_stylesheet_change_runs_the_page_tests_that_draw_what_it_styles(self):
        css, part = 'dashboard/todos-mail-check.css', 'dashboard/todos-mail-check.js'
        ran = 'test_mail_check_dashboard.mjs'
        impact, idle = self.page_map(part, ran)
        text = (ROOT / css).read_text(encoding='utf-8')
        rule = text.index('.mail-check .mc-line{')
        old = text[:rule] + text[rule:].replace('gap:6px', 'gap:5px', 1)
        select.git_text = lambda base, p: old if p == css else None
        got = select.select([css], repo=REPO, impact=impact, base='HEAD')
        self.assertIn(ran, got)
        self.assertNotIn(idle, got)
        self.assertLess(len(got), 60)
        # a rule no class finds (:root, button) styles every page: every page test
        tokens = 'dashboard/base-tokens.css'
        text = (ROOT / tokens).read_text(encoding='utf-8')
        select.git_text = lambda base, p: text.replace(':root{', ':root{--x:1;', 1) if p == tokens else None
        got = select.select([tokens], repo=REPO, impact=impact, base='HEAD')
        self.assertTrue(got is None or idle in got)

    def test_a_new_part_runs_what_uses_it_unless_it_does_more_at_load(self):
        part = 'dashboard/todos-mail-check.js'
        impact, idle = self.page_map('dashboard/shell-core.js', 'test_mail_check_dashboard.mjs')
        select.git_text = lambda base, p: None  # new: not in the map, not in the base
        got = select.select([part], repo=REPO, impact=impact, base='HEAD')
        self.assertIsNotNone(got)
        self.assertNotIn(idle, got)  # its declarations and its click listener on [data-mail-check]
        statements = select.js_split("const a=1;\nfunction f(x){return x}\ndocument.addEventListener('click',e=>{const b=e.target.closest('[data-q]');if(!b)return;go(b)})\nstart()\n")
        self.assertEqual(len(statements), 4)
        self.assertEqual(select.DELEGATED.match(statements[2])[3], '[data-q]')
        self.assertIsNone(select.DELEGATED.match("document.addEventListener('click',e=>{go(e)})"))

    def test_a_function_tests_only_start_with_runs_where_tests_use_it(self):
        impact = self.impact({('x.py', 'f'): ['test_moving.py', 'test_help.py', 'test_i18n.py', 'test_paging.py', 'test_still_needed.py'],
                              ('x.py', 'boot'): ['test_moving.py', 'test_help.py']})
        at = {name: i for i, name in enumerate(impact.tests)}
        impact.seconds = {'test_help.py': 1.0, 'test_i18n.py': 2.0, 'test_paging.py': 3.0, 'test_still_needed.py': 4.0}
        impact.setup = {'x.py': {'f': [at[t] for t in ('test_help.py', 'test_i18n.py', 'test_paging.py', 'test_still_needed.py')],
                                 'boot': [at['test_moving.py'], at['test_help.py']]}}
        # test_moving.py ran f past its setUp; of the four that only set up with it, the three quickest
        self.assertEqual(impact.exercised('x.py', 'f'), {'test_moving.py', 'test_help.py', 'test_i18n.py', 'test_paging.py'})
        # start code no test runs past its start: every test that ran it
        self.assertEqual(impact.exercised('x.py', 'boot'), {'test_moving.py', 'test_help.py'})
        page = ['test_accent_dashboard.mjs', 'test_activity_dashboard.mjs']
        impact.load = {'dashboard/a.js': {(0, 10): [at[page[1]]]}}
        self.assertEqual(impact.js_exercised('dashboard/a.js', 0, 10, [at[t] for t in page]), set(page))  # 1 quick one kept
        impact.load = {'dashboard/a.js': {(0, 10): [at[t] for t in page]}}
        self.assertEqual(impact.js_exercised('dashboard/a.js', 0, 10, [at[t] for t in page]), set(page))

    def test_a_change_is_placed_in_the_maps_text_when_main_moved_since(self):
        old = 'a\nfunction f(){\n  x()\n}\nb\n'
        base = 'a\nadded since the map\nfunction f(){\n  x()\n}\nb\n'
        new = base.replace('x()', 'y()')
        spans = select.moved_spans(old, base, new)
        self.assertEqual([old[a:b] for a, b, _, _ in spans], ['x'])  # only this change, where the map has it
        self.assertEqual([new[a:b] for _, _, a, b in spans], ['y'])
        # the change is on a line main changed since the map: its counterpart there (the same statement, edited again)
        spans = select.moved_spans(old, base.replace('x()', 'z()'), new)
        self.assertEqual([old[a:b] for a, b, _, _ in spans], ['x'])
        # where main put more lines in its place: all of those
        spans = select.moved_spans(old, base.replace('  x()', '  z()\n  w()'), new)
        self.assertEqual({old[a:b] for a, b, _, _ in spans}, {'  x()\n'})
        self.assertEqual(select.moved_spans(old, old, new.replace('added since the map\n', '')), select.changed_spans(old, new.replace('added since the map\n', '')))

    def test_markup_that_starts_hidden_is_shown_by_the_code_that_opens_it(self):
        html = '<main><p>on show</p><div id="panel" hidden><form><input id="q"><b>x</b></form></div>' \
               '<dialog id="d"><div><i>y</i></div></dialog><dialog id="o" open>z</dialog></main>'
        at = lambda text: (html.index(text), html.index(text) + len(text))
        self.assertEqual(select.hidden_holders(html, [at('<b>x</b>'), at('<i>y</i>')]), {'panel', 'd'})
        self.assertEqual(select.hidden_holders(html, [at('id="panel" hidden')]), {'panel'})
        self.assertIsNone(select.hidden_holders(html, [at('on show')]))
        self.assertIsNone(select.hidden_holders(html, [at('z')]))  # an open dialog
        part = 'dashboard/settings-panels.html'
        text = (ROOT / part).read_text(encoding='utf-8')
        inner = text.index('id="addr-maybe"')
        self.assertEqual(select.hidden_holders(text, [(inner, inner + 5)]), {'addr-maybe'})

    def test_include_lines_of_parts_the_change_adds_reach_only_those_parts(self):
        page, part = 'dashboard.html', 'dashboard/todos-mail-check.js'
        text = (ROOT / page).read_text(encoding='utf-8')
        line = '/*@include dashboard/todos-mail-check.js*/\n'
        old = text.replace(line, '', 1)
        select.git_text = lambda base, p: old if p == page else None
        at = text[:text.index(line)].count('\n') + 1
        select.diff_lines = lambda base, p: ({at}, set()) if p == page else (set(), set())
        impact, idle = self.page_map('dashboard/shell-core.js', 'test_mail_check_dashboard.mjs')
        got = select.select([page, part], repo=REPO, impact=impact, base='HEAD')
        self.assertIsNotNone(got)
        self.assertNotIn(idle, got)
        got = select.select([page], repo=REPO, impact=impact, base='HEAD')  # the part itself unchanged: it moved
        self.assertTrue(got is None or idle in got)

    def test_a_folder_names_the_files_on_the_way_to_it(self):
        self.assertTrue(select.names_exactly("HELP = ROOT / 'docs' / 'help'", 'docs/help/history.md'))
        self.assertTrue(select.names_exactly("open('docs/help/' + name)", 'docs/help/history.md'))
        self.assertFalse(select.names_exactly('See docs/development.md.', 'docs/code-map.md'))
        self.assertFalse(select.names_exactly("ROOT / 'docs' / 'brand'", 'docs/help/history.md'))

    def browser(self, old):
        """A map whose browser half knows dashboard/shell-core.js as old: localeFmt ran in one page test, applyLocale in
        another, a third only loaded the page; every other line is a function no test ran, but line 3 (let DL=...)."""
        part = 'dashboard/shell-core.js'
        pages = [Path(t).name for t in TESTS if t.endswith('_dashboard.mjs')]
        quiet = [t for t in pages if not re.search(r'\b(DL|H12|applyLocale|localeFmt|start)\b|shell-core',
                                                    (ROOT / 'tests' / t).read_text(encoding='utf-8'))]
        fmt, arrow, idle = quiet[:3]
        impact = self.impact({})
        at = {name: i for i, name in enumerate(impact.tests)}
        start = old.index('function localeFmt(')
        end = old.index('\n', old.index('return f.format(d)}', start))
        funcs, offset = [[start, end, [at[fmt]]]], 0
        for n, line in enumerate(old.split('\n'), 1):
            if n != 3 and line and not line.startswith('//') and not start <= offset <= end:
                funcs.append([offset, offset + len(line), [at[arrow]] if line.startswith('const applyLocale=') else []])
            offset += len(line) + 1
        impact.commit = 'map'
        impact.js = {part: {'top': [at[t] for t in pages], 'funcs': funcs}}
        impact.js_tests = set(pages)
        select.map_text = lambda commit, p: old if p == part else None
        git_text = self.patched['git_text']
        select.git_text = lambda base, p: old if p == part else git_text(base, p)  # the branch left main at the map
        return part, impact, fmt, arrow, idle

    def test_a_dashboard_function_runs_the_page_tests_that_ran_it(self):
        text = (ROOT / 'dashboard/shell-core.js').read_text(encoding='utf-8')
        part, impact, fmt, arrow, idle = self.browser(text.replace('LOCALE_FMT.size>500', 'LOCALE_FMT.size>400', 1))
        got = select.select([part], repo=REPO, impact=impact, base='HEAD')
        self.assertIn(fmt, got)
        self.assertNotIn(arrow, got)
        self.assertNotIn(idle, got)
        self.assertLess(len(got), 100)

    def test_a_dashboard_global_runs_what_uses_it(self):
        text = (ROOT / 'dashboard/shell-core.js').read_text(encoding='utf-8')
        part, impact, fmt, arrow, idle = self.browser(text.replace("let DL='en-US'", "let DL='en-GB'", 1))
        got = select.select([part], repo=REPO, impact=impact, base='HEAD')
        self.assertIn(arrow, got)  # applyLocale sets DL
        self.assertNotIn(idle, got)

    def test_dashboard_code_that_runs_at_load_runs_every_page_test(self):
        text = (ROOT / 'dashboard/shell-core.js').read_text(encoding='utf-8')
        part, impact, fmt, arrow, idle = self.browser(text.replace("let DL='en-US',H12=false;", "let DL='en-US',H12=false;start();", 1))
        got = select.select([part], repo=REPO, impact=impact, base='HEAD')
        self.assertIn(idle, got)

    def test_what_a_top_level_statement_does(self):
        declared = lambda text: select.js_declared(select.js_blank(text))
        self.assertEqual(declared("let DL='en-US',H12=false;"), {'DL', 'H12'})
        self.assertEqual(declared('function go(a){return a()}'), {'go'})
        self.assertEqual(declared('const f=async(a,b)=>{await a(b)}'), {'f'})
        self.assertEqual(declared('const seen=new Map()'), {'seen'})
        self.assertEqual(declared('const fbN=n=>(+n||0).toLocaleString(DL)'), {'fbN'})  # an expression body runs later
        self.assertEqual(declared("const a=x=>x.y,b=()=>go(1)"), {'a', 'b'})
        self.assertIsNone(declared('const a=x=>x.y,b=go()'))
        self.assertEqual(declared('// a comment'), set())
        self.assertIsNone(declared("document.addEventListener('click',e=>{go(e)})"))
        self.assertIsNone(declared('const width=measure()'))
        self.assertIsNone(declared('const {a,b}=state'))
        self.assertIsNone(declared('LIMIT=4'))

    def test_changed_spans_are_offsets_in_the_old_text(self):
        old, new = 'let a=1;\nfunction f(){return 2}\n', 'let a=1;\nfunction f(){return 3}\ngo();\n'
        spans = select.changed_spans(old, new)
        self.assertEqual([(old[s:e], new[ns:ne]) for s, e, ns, ne in spans], [('2', '3'), ('', 'go();\n')])


if __name__ == '__main__':
    unittest.main()

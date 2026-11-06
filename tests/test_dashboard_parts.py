"""The dashboard's source and the one way to read it (dashboard_parts.py, tests/dashboard-page.mjs, docs/code-map.md).

The page is served as one document. Its source may be split into parts (dashboard/<name>.js, .css and .html, each
standing for the lines a /*@include dashboard/<name>.js*/, /*@include dashboard/<name>.css*/ or
<!--@include dashboard/<name>.html--> line in dashboard.html takes), so everything reads it assembled: the service,
the scripts and the tests, in Python through dashboard_parts and in Node through tests/dashboard-page.mjs."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

import dashboard_parts

ROOT = Path(__file__).resolve().parent.parent
# Files that may name dashboard.html as a file to read or write: the two readers, the scripts that rewrite the source
# itself (scripts/merge_friendly.py, scripts/split_dashboard.py) and this test.
READERS = {'dashboard_parts.py', 'tests/dashboard-page.mjs', 'scripts/merge_friendly.py', 'scripts/split_dashboard.py',
           'tests/test_dashboard_parts.py'}
# dashboard.html as a path in code: ROOT / 'dashboard.html', new URL('../dashboard.html', ...), joinpath/with_name(...)
DIRECT = re.compile(r"""/\s*['"]dashboard\.html['"]|['"](?:\.\./|\./)?dashboard\.html['"]\s*,\s*(?:import\.meta\.url|root)"""
                    r"""|(?:joinpath|with_name)\(\s*['"]dashboard\.html['"]|['"]\.\./dashboard\.html['"]""")


def node():
    return shutil.which('node')


def split_tool():
    import importlib.util
    spec = importlib.util.spec_from_file_location('split_dashboard', ROOT / 'scripts' / 'split_dashboard.py')
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    return tool


def places(source):
    """(line number, part name, where the line is: 'script', 'style' or 'markup') for each include line of a source."""
    out, where = [], 'markup'
    tag = re.compile(r'<script\b[^>]*>|</script>|<style\b[^>]*>|</style>')
    for n, line in enumerate(source.split('\n'), 1):
        if name := dashboard_parts.included(line):
            out.append((n, name, where))
            continue
        for m in tag.finditer(line):
            where = 'markup' if m[0].startswith('</') else 'script' if m[0].startswith('<script') else 'style'
    return out


def node_page(page=None):
    """The page as tests/dashboard-page.mjs assembles it."""
    script = ("import {dashboardPage} from './tests/dashboard-page.mjs';"
              "process.stdout.write(await dashboardPage(process.argv[1]||undefined));")
    return subprocess.run([node(), '--input-type=module', '-e', script, str(page or '')], cwd=ROOT, capture_output=True,
                          check=True, timeout=60).stdout.decode('utf-8')


class DashboardParts(unittest.TestCase):
    def test_nothing_reads_dashboard_html_itself(self):
        files = subprocess.run(['git', 'ls-files', '*.py', '*.mjs', '*.js'], cwd=ROOT, capture_output=True, text=True,
                               check=True).stdout.split()
        direct = []
        for name in files:
            if name in READERS or not (ROOT / name).is_file():
                continue
            for n, line in enumerate((ROOT / name).read_text(encoding='utf-8', errors='replace').split('\n'), 1):
                if DIRECT.search(line):
                    direct.append(f'{name}:{n}: {line.strip()[:120]}')
        self.assertEqual(direct, [], 'Read the dashboard through dashboard_parts.assemble() (Python) or dashboardPage() '
                                     '(tests/dashboard-page.mjs), not dashboard.html itself: its parts are in dashboard/.\n'
                         + '\n'.join(direct))

    def test_every_part_is_included_once(self):
        included = dashboard_parts.includes((ROOT / dashboard_parts.PAGE).read_text(encoding='utf-8'))
        self.assertEqual(sorted(set(included)), sorted(included), 'a part is included twice')
        folder = ROOT / 'dashboard'
        parts = sorted(p.name for p in folder.iterdir()) if folder.is_dir() else []
        self.assertEqual(parts, sorted(included), 'every file in dashboard/ is a part dashboard.html includes, and back')
        self.assertEqual(dashboard_parts.files(ROOT)[1:], [folder / name for name in included])

    def test_the_service_serves_the_assembled_page(self):
        import assistant
        page = assistant.dashboard_page('token', 'owner', '/base/')
        self.assertEqual(page, dashboard_parts.assemble(ROOT).replace('__CSRF__', '')
                         .replace('__UI_VERSION__', assistant.dashboard_version()).replace('__BASE__', '/base/')
                         .replace('__CACHE_SCOPE__', assistant.dashboard_cache_scope('token', 'owner')))
        self.assertNotIn('/*@include dashboard/', page)

    def test_parts_fill_in_their_lines_and_python_and_node_agree(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'dashboard').mkdir()
            (tmp / 'dashboard' / 'area-one.js').write_text('function one(){return 1}\n// one\n', encoding='utf-8')
            (tmp / 'dashboard' / 'b2.js').write_text('const b2=2;\n', encoding='utf-8')
            source = ('<script>\nlet x=0;\n/*@include dashboard/area-one.js*/\n  /*@include dashboard/b2.js*/\n'
                      'x++;\n/*@include dashboard/b2.js*/')
            (tmp / 'dashboard.html').write_text(source, encoding='utf-8')
            want = ('<script>\nlet x=0;\nfunction one(){return 1}\n// one\n  /*@include dashboard/b2.js*/\n'
                    'x++;\nconst b2=2;')  # only whole lines are markers; the last line keeps having no newline
            self.assertEqual(dashboard_parts.assemble(tmp), want)
            self.assertEqual(dashboard_parts.assemble(page=tmp / 'dashboard.html'), want)
            self.assertEqual(dashboard_parts.includes(source), ['area-one.js', 'b2.js'])
            if node():
                self.assertEqual(node_page(tmp / 'dashboard.html'), want)
            (tmp / 'dashboard' / 'b2.js').write_text('const b2=2;', encoding='utf-8')
            with self.assertRaises(ValueError):
                dashboard_parts.assemble(tmp)
        with self.assertRaises(ValueError):
            dashboard_parts.marker('../x.js')
        with self.assertRaises(ValueError):
            dashboard_parts.marker('x.txt')
        self.assertEqual(dashboard_parts.marker('graph-1.js'), '/*@include dashboard/graph-1.js*/')
        self.assertEqual(dashboard_parts.marker('base-1.css'), '/*@include dashboard/base-1.css*/')
        self.assertEqual(dashboard_parts.marker('shell-1.html'), '<!--@include dashboard/shell-1.html-->')

    def test_css_and_html_parts_fill_in_their_lines_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / 'dashboard').mkdir()
            (tmp / 'dashboard' / 'base-a.css').write_text('a{color:red}\n', encoding='utf-8')
            (tmp / 'dashboard' / 'shell-a.html').write_text('<p id="a">A</p>\n', encoding='utf-8')
            (tmp / 'dashboard' / 'shell-a.js').write_text('let a=1;\n', encoding='utf-8')
            source = ('<style>\n/*@include dashboard/base-a.css*/\n</style>\n<!--@include dashboard/shell-a.html-->\n'
                      '<!--@include dashboard/shell-a.css-->\n/*@include dashboard/shell-a.html*/\n<script>\n'
                      '/*@include dashboard/shell-a.js*/\n</script>')
            (tmp / 'dashboard.html').write_text(source, encoding='utf-8')
            want = ('<style>\na{color:red}\n</style>\n<p id="a">A</p>\n<!--@include dashboard/shell-a.css-->\n'
                    '/*@include dashboard/shell-a.html*/\n<script>\nlet a=1;\n</script>')  # a kind takes its own marker only
            self.assertEqual(dashboard_parts.assemble(tmp), want)
            self.assertEqual(dashboard_parts.includes(source), ['base-a.css', 'shell-a.html', 'shell-a.js'])
            self.assertEqual(dashboard_parts.files(tmp)[1:], [tmp / 'dashboard' / n for n in ('base-a.css', 'shell-a.html',
                                                                                              'shell-a.js')])
            self.assertEqual(dashboard_parts.expand(source, tmp / 'dashboard', ('css',)),
                             source.replace('/*@include dashboard/base-a.css*/', 'a{color:red}'))
            if node():
                self.assertEqual(node_page(tmp / 'dashboard.html'), want)
            self.assertEqual(places(source), [(2, 'base-a.css', 'style'), (4, 'shell-a.html', 'markup'),
                                              (8, 'shell-a.js', 'script')])

    def test_each_include_line_is_in_its_place(self):
        # A script's part in a script, a stylesheet's in the <style>, markup outside both: so a part can only ever be
        # the kind of text that was there.
        want = {'js': 'script', 'css': 'style', 'html': 'markup'}
        wrong = [f'dashboard.html:{n}: {name} is in the {where}' for n, name, where in
                 places((ROOT / dashboard_parts.PAGE).read_text(encoding='utf-8')) if want[name.rsplit('.', 1)[1]] != where]
        self.assertEqual(wrong, [], 'a .js part goes in a script, a .css part in the stylesheet, an .html part in the markup')

    def test_each_css_part_is_whole_rules(self):
        # A stylesheet part starts and ends between rules: its braces match, and it ends outside every comment and
        # string. Its runs follow each other in the page's order, so the cascade is the one of the whole sheet.
        tool, bad = split_tool(), []
        for path in sorted((ROOT / 'dashboard').glob('*.css')):
            try:
                tool.css_top_level_lines(path.read_text(encoding='utf-8'))
            except ValueError as e:
                bad.append(f'{path.name}: {e}')
        self.assertEqual(bad, [], 'a stylesheet part is not whole rules')
        for text in ('a{', 'a}', '/* a', 'a{content:"}"', '@media x{a{b:c}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                tool.css_top_level_lines(text)
        self.assertEqual(tool.css_top_level_lines('/* {\n */a{\nb:"}"}\n@media x{a{b:c}\n}\nd{}'), [0, 3, 5])

    def test_each_html_part_is_whole_elements(self):
        tool = split_tool()
        bad = [f'{path.name}: {"; ".join(problems[:3])}' for path in sorted((ROOT / 'dashboard').glob('*.html'))
               if (problems := tool.html_problems(path.read_text(encoding='utf-8')))]
        self.assertEqual(bad, [], 'a markup part is not whole elements')
        self.assertEqual(tool.html_problems('<div id="a"><img src="x"><svg><path d="M0"/></svg></div\n'), [])
        self.assertEqual(tool.html_problems('><p id="b">B</p\n'), [])
        self.assertTrue(tool.html_problems('<div><p>x</div></p>\n'))
        self.assertTrue(tool.html_problems('<div>\n'))
        self.assertTrue(tool.html_problems('</div>\n'))

    def test_each_part_is_whole_statements(self):
        # A part is whole top-level statements: it parses as a script on its own, and so does the main script that
        # stays in dashboard.html (the include lines are comments to it).
        if not node():
            self.skipTest('no node')
        folder = ROOT / 'dashboard'
        files = sorted(folder.glob('*.js')) if folder.is_dir() else []
        if not files:
            self.skipTest('no parts')
        script = ("import vm from 'node:vm';import {readFileSync} from 'node:fs';const bad=[];"
                  "for(const f of process.argv.slice(1)){try{new vm.Script(readFileSync(f,'utf8'),{filename:f})}"
                  "catch(e){bad.push(f+': '+e.message)}}process.stdout.write(bad.join('\\n'))")
        lines = (ROOT / 'dashboard.html').read_text(encoding='utf-8').split('\n')
        with tempfile.TemporaryDirectory() as tmp:
            main = Path(tmp) / 'dashboard-main-script.js'
            first = lines.index('<script>', next(i for i, x in enumerate(lines) if x.startswith('<script id="i18n">'))) + 1
            end = max(i for i, x in enumerate(lines) if x.startswith('</script>'))
            main.write_text('\n'.join(lines[first:end]), encoding='utf-8')
            bad = subprocess.run([node(), '--input-type=module', '-e', script, *map(str, files), str(main)], capture_output=True,
                                 text=True, check=True, timeout=60).stdout
        self.assertEqual(bad, '', 'a part (or the main script around the include lines) does not parse on its own')

    def test_the_split_tool_loses_nothing(self):
        # scripts/split_dashboard.py split cuts the assembled page into parts and nothing else: cutting it again and
        # putting it back gives the same bytes (the PR that split it showed the page was byte for byte the one before).
        tool = split_tool()
        page = dashboard_parts.assemble(ROOT)
        try:
            html, parts = tool.cut(page)
        except KeyError as gone:
            self.skipTest(f'the split tool\'s anchors have moved on ({gone}); it is only for rebasing the split')
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'dashboard').mkdir()
            for name, text in parts.items():
                (Path(tmp) / 'dashboard' / name).write_text(text, encoding='utf-8')
            (Path(tmp) / 'dashboard.html').write_text(html, encoding='utf-8')
            self.assertEqual(dashboard_parts.assemble(tmp), page)
        self.assertGreater(len(parts), 1)

    def test_the_css_and_html_cuts_lose_nothing(self):
        # split-css and split-html cut only their own kind: cutting what dashboard.html holds now (its other parts as
        # include lines) and putting it back gives the same page.
        tool, page = split_tool(), dashboard_parts.assemble(ROOT)
        source = (ROOT / dashboard_parts.PAGE).read_text(encoding='utf-8')
        for kind, cut in (('css', tool.cut_css), ('html', tool.cut_html)):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                try:
                    html, parts = cut(dashboard_parts.expand(source, ROOT / 'dashboard', (kind,)))
                except KeyError as gone:
                    self.skipTest(f'the split tool\'s anchors have moved on ({gone}); it is only for rebasing the split')
                shutil.copytree(ROOT / 'dashboard', Path(tmp) / 'dashboard')
                for old in (Path(tmp) / 'dashboard').glob(f'*.{kind}'):
                    old.unlink()
                for name, text in parts.items():
                    (Path(tmp) / 'dashboard' / name).write_text(text, encoding='utf-8')
                (Path(tmp) / 'dashboard.html').write_text(html, encoding='utf-8')
                self.assertEqual(dashboard_parts.assemble(tmp), page)

    def test_node_and_python_assemble_the_same_page(self):
        if not node():
            self.skipTest('no node')
        self.assertEqual(node_page(), dashboard_parts.assemble(ROOT))


if __name__ == '__main__':
    unittest.main()

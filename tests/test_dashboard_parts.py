"""The dashboard's source and the one way to read it (dashboard_parts.py, tests/dashboard-page.mjs, docs/code-map.md).

The page is served as one document. Its source may be split into parts (dashboard/<name>.js, each standing for the
lines a /*@include dashboard/<name>.js*/ line in dashboard.html takes), so everything reads it assembled: the service,
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
        self.assertEqual(dashboard_parts.marker('graph-1.js'), '/*@include dashboard/graph-1.js*/')

    def test_node_and_python_assemble_the_same_page(self):
        if not node():
            self.skipTest('no node')
        self.assertEqual(node_page(), dashboard_parts.assemble(ROOT))


if __name__ == '__main__':
    unittest.main()

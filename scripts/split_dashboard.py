#!/usr/bin/env python3
"""Mechanical steps for splitting the dashboard's source (docs/code-map.md, dashboard_parts.py). Each one can be run
again after a rebase instead of merging by hand: it does the same thing to whatever the files hold then.

    python3 scripts/split_dashboard.py readers   # tests read the page through dashboard_parts / tests/dashboard-page.mjs

`readers` rewrites every test that reads dashboard.html itself to read the assembled page instead; the forms it knows
are the ones the tests use. tests/test_dashboard_parts.py fails on any direct read it leaves."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / 'tests'

# Node tests: readFile(...dashboard.html...,'utf8') -> dashboardPage(...)
NODE = [
    (re.compile(r"readFile\(new URL\('\.\./dashboard\.html',import\.meta\.url\),'utf8'\)"), 'dashboardPage()'),
    (re.compile(r"readFile\(new URL\('dashboard\.html',root\),'utf8'\)"), 'dashboardPage()'),
    (re.compile(r"readFile\((process\.env\.\w+)\|\|new URL\('\.\./dashboard\.html',import\.meta\.url\),'utf8'\)"),
     r'dashboardPage(\1)'),
    (re.compile(r"readFile\(new URL\((process\.env\.\w+)\|\|'\.\./dashboard\.html',import\.meta\.url\),'utf8'\)"),
     r'dashboardPage(\1&&new URL(\1,import.meta.url))'),
]
NODE_IMPORT = "import {dashboardPage} from './dashboard-page.mjs';\n"

# Python tests: (<folder> / 'dashboard.html').read_text(...) and the like -> dashboard_parts.assemble(<folder>)
FOLDER = r"[\w.]+(?:\([\w.]*\))?(?:\.\w+)*"
PYTHON = [
    (re.compile(rf"\(({FOLDER}) / 'dashboard\.html'\)\.read_text\([^)]*\)"), r'dashboard_parts.assemble(\1)'),
    (re.compile(r"\(Path\(([\w.]+)\)\.with_name\('dashboard\.html'\)\)\.read_text\(\)"), r'dashboard_parts.assemble(Path(\1).parent)'),
    (re.compile(r"\(Path\(__file__\)\.parent\.parent\.joinpath\('dashboard\.html'\)\)\.read_text\(\)"),
     'dashboard_parts.assemble(Path(__file__).parent.parent)'),
    (re.compile(r"Path\(__file__\)\.parent\.parent\.joinpath\('dashboard\.html'\)\.read_text\(\)"),
     'dashboard_parts.assemble(Path(__file__).parent.parent)'),
]
PYTHON_IMPORT = 'import dashboard_parts\n'


def add_import(text, line, node):
    """text with the import line added among its imports: after the last top-level import before any code."""
    if line in text:
        return text
    lines = text.splitlines(keepends=True)
    last = None
    for i, current in enumerate(lines):
        if current.startswith(('import ', 'from ')):
            last = i
        elif node and current.startswith(('const ', 'let ', 'function ', 'await ')):
            break
        elif not node and current.startswith(('def ', 'class ', 'if __name__')):
            break
    lines.insert(0 if last is None else last + 1, line)
    return ''.join(lines)


def rewrite(path, rules, line, node):
    before = path.read_text(encoding='utf-8')
    after = before
    for shape, replacement in rules:
        after = shape.sub(replacement, after)
    if after == before:
        return False
    path.write_text(add_import(after, line, node), encoding='utf-8')
    return True


def readers():
    changed = [p.name for p in sorted(TESTS.glob('*.mjs')) if p.name != 'dashboard-page.mjs' and rewrite(p, NODE, NODE_IMPORT, True)]
    changed += [p.name for p in sorted(TESTS.glob('*.py')) if rewrite(p, PYTHON, PYTHON_IMPORT, False)]
    print(f'{len(changed)} tests now read the assembled page')
    return 0


COMMANDS = {'readers': readers}

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    sys.exit(COMMANDS[sys.argv[1]]())

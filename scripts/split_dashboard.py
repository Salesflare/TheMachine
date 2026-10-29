#!/usr/bin/env python3
"""Mechanical steps for splitting the dashboard's source (docs/code-map.md, dashboard_parts.py). Each one can be run
again after a rebase instead of merging by hand: it does the same thing to whatever the files hold then.

    python3 scripts/split_dashboard.py readers       # tests read the page through dashboard_parts / dashboard-page.mjs
    python3 scripts/split_dashboard.py split         # dashboard.html's main script into dashboard/<area>-<what>.js
    python3 scripts/split_dashboard.py verify [REF]  # the assembled page is byte for byte the one at REF (git)

`readers` rewrites every test that reads dashboard.html itself to read the assembled page instead; the forms it knows
are the ones the tests use. tests/test_dashboard_parts.py fails on any direct read it leaves.

`split` first assembles the page (so it can run again on a page split before), then cuts the main script into the
PARTS below: each part runs from its first statement (with the comment lines right above it) to just before the
statement that starts the next part (or the given end), and its lines are replaced by one include line. Statements are
found by a small scanner of the script (strings, templates, comments, regular expressions, brackets): a part starts and
ends only at a top-level declaration (function, const, let, class) or at a top-level line given by its start. Nothing
is reordered and no byte changes: `verify` proves the assembled page is the one before, and each part and what stays
in dashboard.html parse as scripts on their own (node --check). A part whose anchors are gone fails loudly."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / 'tests'
sys.path.insert(0, str(ROOT))
import dashboard_parts  # noqa: E402

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


# --- split -----------------------------------------------------------------------------------------------------------

# (part, first, end): the part dashboard/<part>.js holds the main script's statements from `first` up to `end`. An
# anchor is the name of a top-level declaration, or the start of a top-level line (a listener: "$('nav').add..."), the
# first after the previous anchor; end None is the end of the script. Parts are in the page's order; what lies between
# them stays in dashboard.html: the core (locale and error reports, network and outbox, render and refresh, toast,
# boot). Areas as in scripts/i18n_extract.py AREAS, plus fleet and the email view.
PARTS = [
    ('settings-models', 'modelName', 'cardFiles'),
    ('todos-cards', 'cardFiles', 'DAYS'),
    ('settings-general', 'DAYS', 'offline'),
    ('settings-skills', 'skillsKey', 'connectorHealth'),
    ('connections-cards', 'connectorHealth', 'originals'),
    ('events-email', 'originals', 'POKES'),
    ('todos-game', 'POKES', 'folded'),
    ('todos-learned', 'folded', 'turnOn'),
    ('todos-list', 'resultId', 'pushOK'),
    ('settings-device', 'pushOK', 'notifyPresence'),
    ('todos-chat', 'notifyPresence', 'TAB_LINKS'),
    ('shell-tabs', 'TAB_LINKS', 'GRAPH_SUBS'),
    ('graph-nav', 'GRAPH_SUBS', 'CAL_BACK'),
    ('calendar-view', 'CAL_BACK', "$('nav').addEventListener("),
    ('fleet-view', 'fleetPost', 'pageApprove'),
    ('todos-task-pages', 'pageApprove', "$('#people-view').addEventListener("),
    ('graph-view', "$('#people-view').addEventListener(", 'search'),
    ('events-list', 'search', 'renderMonth'),
    ('todos-snooze', 'renderMonth', 'toast'),
    ('connections-signin', 'signinWaiting', 'showNote'),
    ('new-todo', 'nc', "$('#side-find').addEventListener("),
    ('todos-rows', 'mergeOther', 'KB_MAC'),
    ('shell-keys', 'KB_MAC', 'helpMarkup'),
    ('help-panel', 'helpMarkup', None),
]
DECLARATION = re.compile(r'(?:async )?function\*? ?([\w$]+)|(?:const|let|var|class) ([\w$]+)')
BEFORE_REGEX = {'return', 'typeof', 'instanceof', 'in', 'of', 'new', 'delete', 'void', 'throw', 'case', 'do', 'else',
                'yield', 'await'}
WORD = re.compile(r'[A-Za-z_$][\w$]*')
NUMBER = re.compile(r'[\w.]+')


def top_level_lines(text):
    """The numbers (from 0) of the lines of a classic script that start outside every bracket, string, template and
    comment. Not a parser: enough for this page, and `split` has node check what it cut."""
    out, i, n, line = [], 0, len(text), 0
    frames = [['code', 0]]  # ['code', open brackets] or ['tpl']; a template's ${ opens a code frame
    last, line_start = '', True
    while i < n:
        c, frame = text[i], frames[-1]
        if line_start:
            if len(frames) == 1 and frame[1] == 0:
                out.append(line)
            line_start = False
        if frame[0] == 'tpl':
            if c == '\\':
                line += text[i + 1] == '\n'
                i += 2
            elif c == '`':
                frames.pop()
                i, last = i + 1, 'str'
            elif text.startswith('${', i):
                frames.append(['code', 0])
                i, last = i + 2, '{'
            else:
                line += c == '\n'
                i += 1
            continue
        if c == '\n':
            line, line_start, i = line + 1, True, i + 1
        elif c in ' \t\r':
            i += 1
        elif text.startswith('//', i):
            j = text.find('\n', i)
            i = n if j < 0 else j
        elif text.startswith('/*', i):
            j = text.index('*/', i + 2)
            line += text.count('\n', i, j)
            i = j + 2
        elif c in '\'"':
            j = i + 1
            while text[j] != c:
                if text[j] == '\n':
                    raise ValueError(f'a line break in a string, script line {line + 1}')
                if text[j] == '\\':
                    line += text[j + 1] == '\n'
                    j += 1
                j += 1
            i, last = j + 1, 'str'
        elif c == '`':
            frames.append(['tpl'])
            i += 1
        elif c == '/' and (not last or (len(last) == 1 and last in '(,=:[!&|?{};+-*%<>~^') or last in BEFORE_REGEX):
            j, in_class = i + 1, False
            while text[j] != '/' or in_class:
                if text[j] == '\n':
                    raise ValueError(f'a line break in a regular expression, script line {line + 1}')
                if text[j] == '\\':
                    j += 1
                elif text[j] == '[':
                    in_class = True
                elif text[j] == ']':
                    in_class = False
                j += 1
            j += 1
            while j < n and text[j].isalpha():
                j += 1
            i, last = j, 're'
        elif c in '([{':
            frame[1] += 1
            i, last = i + 1, c
        elif c in ')]}':
            if c == '}' and frame[1] == 0 and len(frames) > 1:
                frames.pop()  # the end of a template's ${...}
            elif frame[1] == 0:
                raise ValueError(f'an unbalanced {c}, script line {line + 1}')
            else:
                frame[1] -= 1
            i, last = i + 1, c
        elif m := WORD.match(text, i):
            i, last = m.end(), m.group(0)
        elif c.isdigit():
            i, last = NUMBER.match(text, i).end(), 'num'
        else:
            i, last = i + 1, c
    if frames != [['code', 0]]:
        raise ValueError(f'the script ends inside {frames[-1][0]}')
    return out


def main_script(lines):
    """(first, end): the main <script>'s lines (after the i18n script, up to the closing </script>)."""
    i18n = next(i for i, line in enumerate(lines) if line.startswith('<script id="i18n">'))
    first = next(i for i in range(i18n, len(lines)) if lines[i] == '<script>') + 1
    end = max(i for i, line in enumerate(lines) if line.startswith('</script>'))
    return first, end


def cut(page):
    """(dashboard.html, {part file: text}) for an assembled page."""
    lines = page.split('\n')
    first, end = main_script(lines)
    starts = [first + k for k in top_level_lines('\n'.join(lines[first:end]))]
    names = {}
    for at in starts:
        if m := DECLARATION.match(lines[at]):
            names.setdefault(m.group(1) or m.group(2), at)

    def find(anchor, after):
        if anchor is None:
            return end
        if re.fullmatch(r'[\w$]+', anchor):
            at = names.get(anchor)
        else:
            at = next((s for s in starts if s > after and lines[s].startswith(anchor)), None)
        if at is None or at <= after:
            raise KeyError(f'dashboard.html: no top-level {anchor!r} after line {after + 1} (scripts/split_dashboard.py PARTS)')
        while at - 1 > after and at - 1 in starts_set and lines[at - 1].startswith('//'):
            at -= 1  # the comment right above it goes with it
        return at

    starts_set = set(starts)
    spans, after = [], first - 1
    for name, start, stop in PARTS:
        a = find(start, after)
        b = find(stop, a)
        spans.append((name, a, b))
        after = b - 1
    out, parts, at = [], {}, 0
    for name, a, b in spans:
        out += lines[at:a] + [dashboard_parts.marker(f'{name}.js')]
        parts[f'{name}.js'] = '\n'.join(lines[a:b]) + '\n'
        at = b
    return '\n'.join(out + lines[at:]), parts


def node_check(page, parts):
    """Each part, and the main script that stays in dashboard.html, parse as scripts on their own."""
    node = shutil.which('node')
    if not node:
        raise SystemExit('split needs node to check what it cut')
    lines = page.split('\n')
    first, end = main_script(lines)
    scripts = {'dashboard.html (main script)': '\n'.join(lines[first:end]) + '\n', **parts}
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in scripts.items():
            path = Path(tmp) / 'part.js'
            path.write_text(text, encoding='utf-8')
            done = subprocess.run([node, '--check', str(path)], capture_output=True, text=True)
            if done.returncode:
                raise SystemExit(f'{name} does not parse on its own:\n{done.stderr}')


def split():
    page = dashboard_parts.assemble(ROOT)
    html, parts = cut(page)
    node_check(html, parts)
    folder = ROOT / dashboard_parts.FOLDER
    folder.mkdir(exist_ok=True)
    for old in folder.glob('*.js'):
        if old.name not in parts:
            old.unlink()
    for name, text in parts.items():
        (folder / name).write_text(text, encoding='utf-8')
    (ROOT / dashboard_parts.PAGE).write_text(html, encoding='utf-8')
    if dashboard_parts.assemble(ROOT) != page:
        raise SystemExit('the assembled page changed: nothing should')
    kept = html.count('\n') + 1
    print(f'{len(parts)} parts in {dashboard_parts.FOLDER}/ ({sum(t.count(chr(10)) for t in parts.values())} lines); '
          f'dashboard.html keeps {kept} lines')
    return 0


# --- verify ----------------------------------------------------------------------------------------------------------

def page_at(ref):
    """The dashboard page assembled from git's REF."""
    show = lambda path: subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=ROOT, capture_output=True, check=True).stdout
    source = show(dashboard_parts.PAGE).decode('utf-8')
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / dashboard_parts.FOLDER).mkdir()
        for name in dashboard_parts.includes(source):
            (Path(tmp) / dashboard_parts.FOLDER / name).write_bytes(show(f'{dashboard_parts.FOLDER}/{name}'))
        (Path(tmp) / dashboard_parts.PAGE).write_text(source, encoding='utf-8')
        return dashboard_parts.assemble(tmp)


def verify(ref='HEAD'):
    before, now = page_at(ref), dashboard_parts.assemble(ROOT)
    if before != now:
        print(f'The assembled page differs from {ref}\'s ({len(before)} and {len(now)} characters)')
        return 1
    print(f'The assembled page is byte for byte {ref}\'s ({len(now.encode())} bytes, '
          f'{len(dashboard_parts.includes((ROOT / dashboard_parts.PAGE).read_text(encoding="utf-8")))} parts now)')
    return 0


COMMANDS = {'readers': readers, 'split': split, 'verify': verify}

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    sys.exit(COMMANDS[sys.argv[1]](*sys.argv[2:]))

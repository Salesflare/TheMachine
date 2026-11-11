#!/usr/bin/env python3
"""Which test files a change needs, for pull requests (main, release tags and the weekly run always run everything).

Given the changed paths, it follows what depends on them, from the files in this checkout:
- a Python file: every file that imports it, again and again up the chain (so a change to a module a test reaches through
  assistant.py runs that test), and every file that names it in a string (spec_from_file_location, a subprocess);
- any other file (a dashboard part, a catalog, a help article, a helper in tests/, a plugin file): every file that names
  it, its file name or its folder ('dashboard/', 'i18n/'), again and again through files that aren't Python. A Python
  file that names it counts, and with it the files that import that Python file;
- a test file: itself.
The tests that look over the whole repository (ALWAYS) run on every change. Anything it can't place runs everything:
a changed file nothing names that isn't plainly inert, a change to the test machinery (FULL), or more files than it
helps to pick from. Prints the test file names, one per line, or ALL.

With the test-impact map (--impact, from scripts/test_impact.py: which tests ran each function on main's last full run)
and the commit the change is on (--base), it's much narrower (select_mapped): a changed function runs the tests that ran
it, not every test that imports its file (assistant.py and machine/app/ load nearly everything); a module-level change
runs the tests of the functions that use the names it defines; a catalog change runs the tests that name a text it
changed. A dashboard part (dashboard/*.js) goes the same way by the map's browser half: the page tests that ran the
functions it touched in Chromium, the ones that run what uses a global it declares, or every page test when it changes
what runs at load (a top-level call). What the map doesn't know (a test or a file newer than it, a file that doesn't parse) goes the way above.

scripts/test_select.py changed.txt          (changed paths, one per line; - reads them from stdin)
scripts/test_select.py --impact map.json.gz --base HEAD^1 changed.txt
scripts/test_select.py --why tests/test_x.py changed.txt   (why that test was picked, or not)"""
import ast
import gzip
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tokenize

ROOT = Path(__file__).resolve().parent.parent

# A change to these runs everything: the way tests run, what they run on, and this selection itself.
FULL = {
    'scripts/test.py', 'scripts/test_select.py', '.github/workflows/ci.yml', 'package.json', 'package-lock.json',
    'openclaw-pin.json', 'openclaw-root.mjs', 'tests/test-env.mjs', 'tests/seams.py',
}
# Folders whose files no test reads: a change there that nothing names runs only ALWAYS. Everything else that nothing
# names runs everything, since it isn't clear what it touches.
INERT = ('docs/', 'mobile/', 'brand/', 'source-notes/', '.github/workflows/ios.yml', '.github/workflows/wacli-pin.yml')
INERT_FILES = {'LICENSE', 'README.md', 'CONTRIBUTING.md', 'SECURITY.md', 'TRADEMARKS.md', 'THIRD_PARTY_NOTICES.md', '.gitignore'}
# Tests that look over the whole repository (every Python file, every tracked file, every dashboard part): a new file
# anywhere can fail them without anything naming it. tests/test_test_select.py checks this list stays complete.
ALWAYS = {
    'test_architecture.py', 'test_dashboard_parts.py', 'test_message_seal.py', 'test_export_complete.py', 'test_error_feed.py',
    'test_seams.py', 'test_owner_boundary.py', 'test_us_english.py', 'test_owner_names.py', 'test_connectors.py',
    'test_test_select.py',
}
# Python that only puts the dashboard page together from its parts and serves it: a part's change reaches the Python
# tests that look at the page, and those name dashboard_parts or the page (they're picked by name), not every test that
# imports the app. Every other Python file that reads a changed file counts as changed itself.
PAGE = {'dashboard_parts.py', 'machine/web/serving.py'}
# More than this share of the files picked: run them all, the difference isn't worth a partial run.
ENOUGH = 0.85
# A change to a function tests ran past setting up (or after their page loaded) runs those tests, plus this many of the
# quickest that ran it only while starting, so a change that breaks the start still meets one.
STARTS = 3
# Folders on the import path besides the root (scripts/test.py puts tests/ there; scripts and integrations add their own).
IMPORT_ROOTS = ('', 'tests/', 'scripts/', 'integrations/')
IMPORT = re.compile(r'^[ \t]*(?:import[ \t]+(?P<plain>[\w.]+(?:[ \t]+as[ \t]+\w+)?(?:[ \t]*,[ \t]*[\w.]+(?:[ \t]+as[ \t]+\w+)?)*)'
                    r'|from[ \t]+(?P<dots>\.*)(?P<module>[\w.]*)[ \t]+import[ \t]+(?P<names>\([^)]*\)|[^\n#;]+))', re.M)
# The files that can depend on another one: code and the page's parts. Docs, catalogs and data only get read.
QUOTED_PY = re.compile(r'''['"`/]([\w.-]+\.py)['"`]''')
IMPORTED = re.compile(r'\b(?:import|from)\s+([\w.]+(?:\s*,\s*[\w.]+)*)')
CODE = {'.py', '.mjs', '.js', '.ts', '.html', '.css', '.sh'}
NOT_CODE = ('docs/', 'mobile/', 'brand/', 'source-notes/', 'i18n/')


def tracked():
    try:
        out = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split('\n')
    except (OSError, subprocess.CalledProcessError):
        out = [str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and 'node_modules' not in p.parts]
    return sorted(path for path in out if path and (ROOT / path).is_file())


def is_test(path):
    return path.startswith('tests/test_') and path.count('/') == 1 and path.endswith(('.py', '.mjs'))


def code_view(path, text):
    """The text a file names others with where it counts. A test counts wherever it names something. App code counts
    only in its lines that hold a string before any comment: a mention in a comment or a docstring ('see
    docs/architecture.md') reads nothing."""
    if is_test(path) or not path.endswith(('.py', '.mjs', '.js', '.ts')):
        return text
    comment = '#' if path.endswith('.py') else '//'
    kept, doc = [], False
    for line in text.split('\n'):
        # a Python docstring (and any triple-quoted text) is prose, not a path the code opens
        if comment == '#' and (doc or line.lstrip().startswith(('"""', "'''", 'r"""', 'f"""'))):
            doc = doc != ((line.count('"""') + line.count("'''")) % 2 == 1)
            continue
        quote = min((i for i in (line.find("'"), line.find('"'), line.find('`')) if i >= 0), default=-1)
        at = line.find(comment)
        if quote >= 0 and (at < 0 or at > quote) and not line.lstrip().startswith('*'):
            kept.append(line)
    return '\n'.join(kept)


def mentions(text, word, before, after):
    """word in text as a whole name: no letter, digit, _ or one of `before` right before it, nor of `after` right after."""
    at = text.find(word)
    while at >= 0:
        prev, nxt = text[at - 1:at], text[at + len(word):at + len(word) + 1]
        if not (prev and (prev.isalnum() or prev == '_' or prev in before)) and not (nxt and (nxt.isalnum() or nxt == '_' or nxt in after)):
            return True
        at = text.find(word, at + 1)
    return False


def mentions_folder(text, folder):
    """The folder as a path: 'dashboard/x', ROOT / 'dashboard', joinpath('connectors'); not the bare word."""
    at = text.find(folder)
    while at >= 0:
        prev, nxt = text[at - 1:at], text[at + len(folder):at + len(folder) + 1]
        if nxt == '/' and not (prev and (prev.isalnum() or prev in '_.-')):
            return True
        if prev in ('"', "'") and nxt == prev and text[max(0, at - 40):at - 1].rstrip().endswith(('/', 'joinpath(')):
            return True
        at = text.find(folder, at + 1)
    return False


def module_name(path):
    name = path[:-3].replace('/', '.')
    return name[:-len('.__init__')] if name.endswith('.__init__') else name


class Repo:
    def __init__(self, paths, extra_modules=()):
        self.paths = paths
        self._named = {}
        self.text = {}
        for path in paths:
            if Path(path).suffix in CODE and not path.startswith(NOT_CODE):
                try:
                    self.text[path] = (ROOT / path).read_text(encoding='utf-8', errors='replace')
                except OSError:
                    pass
        # module name -> path, for the Python files here and the ones a change deleted (so their importers still count)
        self.modules = {}
        for path in [*paths, *extra_modules]:
            if path.endswith('.py'):
                self.modules.setdefault(module_name(path), path)
        self.imports = {path: self._imports(path) for path in self.text if path.endswith('.py')}
        self.importers = {}
        for path, found in self.imports.items():
            for target in found:
                self.importers.setdefault(target, set()).add(path)
        # what names a data file: code and tests, not the dashboard's own parts (they are all in the one page anyway)
        self.views = {path: code_view(path, text) for path, text in self.text.items() if not path.startswith('dashboard/')}
        # who names a Python file: quoted as a file ('cli.py', 'machine/x.py'), or imported by name in any language
        self.quoted, self.imported = {}, {}
        for path, text in self.text.items():
            for name in set(QUOTED_PY.findall(text)):
                self.quoted.setdefault(name, set()).add(path)
            for found in set(IMPORTED.findall(text)):
                for name in re.split(r'\s*,\s*', found):
                    self.imported.setdefault(name, set()).add(path)

    def _resolve(self, name, here):
        """The repository files a dotted import name loads: the module and the packages above it."""
        found = set()
        own = str(Path(here).parent) + '/' if '/' in here else ''
        for base in dict.fromkeys([*IMPORT_ROOTS, own]):
            prefix = base.replace('/', '.')
            parts = name.split('.')
            for n in range(1, len(parts) + 1):
                path = self.modules.get(prefix + '.'.join(parts[:n]))
                if path:
                    found.add(path)
        return found

    def _imports(self, path):
        """Import statements anywhere in the file (also inside functions), read line by line: much faster than a full
        parse on a busy runner, and an import inside a string only adds a test, never drops one."""
        package = module_name(path).rsplit('.', 1)[0] if '/' in path else ''
        if path.endswith('__init__.py'):
            package = module_name(path)
        found = set()
        for match in IMPORT.finditer(self.text[path]):
            if match.group('plain'):
                for item in match.group('plain').split(','):
                    found |= self._resolve(item.split(' as ')[0].strip(), path)
                continue
            dots, module = len(match.group('dots')), match.group('module') or ''
            if dots:
                base = package.split('.') if package else []
                base = base[:len(base) - (dots - 1)] if dots > 1 else base
                module = '.'.join(base + ([module] if module else []))
            if module:
                found |= self._resolve(module, path)
            for item in re.split(r'[,\s]+', match.group('names').replace('(', ' ').replace(')', ' ')):
                if item and item not in ('as', '\\') and item.isidentifier():
                    found |= self._resolve(f'{module}.{item}' if module else item, path)
        found.discard(path)
        return found

    def named_by(self, path):
        """The files that name this one: its path, or its file name, or (outside the root) its folder, as text. A Python
        file counts when it's quoted as a file ('cli.py') or imported by name from another language (python -c 'import qr')."""
        if path in self._named:
            return self._named[path]
        name, folder = Path(path).name, str(Path(path).parent)
        if path.endswith('.py'):
            found = (self.quoted.get(name, set()) | self.imported.get(module_name(path), set())) - {path}
            found = {other for other in found if not (other.endswith('.py') and path in self.imports.get(other, ()))}
            self._named[path] = found
            return found
        stem = Path(path).stem if path.startswith('dashboard/') and Path(path).suffix in ('.js', '.css', '.html') else None
        # its folder and the ones above it ('docs/help/de', 'docs/help', 'docs'), written either way: 'docs/help/' or
        # ROOT / 'docs' / 'help'
        folders = [str(p) for p in Path(path).parents if str(p) not in ('.', 'tests')]
        joined = [form for f in folders for form in ("' / '".join(f.split('/')), '" / "'.join(f.split('/'))) if '/' in f]
        found = {other for other, text in self.views.items() if other != path and (
            name in text and mentions(text, name, '.-', '-') or path in text
            or any(f in text and mentions_folder(text, f) for f in folders) or any(j in text for j in joined)
            or stem and stem in text and mentions(text, stem, '-', '-'))}
        self._named[path] = found
        return found


def select(changed, repo=None, why=None, impact=None, base=None):
    """The test files (names in tests/) the changed paths need, or None for all of them. With the test-impact map
    (impact) and the commit the change is on (base), a Python change runs the tests that ran what it changed."""
    changed = [c.strip().removeprefix('./') for c in changed if c.strip()]
    if not changed:
        return None
    if repo is None:
        repo = Repo(tracked(), extra_modules=[c for c in changed if c.endswith('.py')])
    if impact is not None and base:
        return select_mapped(changed, repo, impact, base, why)
    reasons = {}

    def add(path, reason):
        if path not in reasons:
            reasons[path] = reason
            return True
        return False

    pending = []
    for path in changed:
        if path in FULL:
            if why is not None:
                why['*'] = f'{path} is test machinery'
            return None
        if add(path, 'changed'):
            pending.append(path)
    while pending:
        path = pending.pop()
        if path.endswith('.py'):
            # importers, all the way up; and files that name it as a file
            for other in repo.importers.get(path, ()):
                if add(other, f'imports {path}'):
                    pending.append(other)
            for other in repo.named_by(path):
                # a dashboard part or a doc that mentions it doesn't run it: only Python, tests and their helpers go on
                if add(other, f'names {path}') and not other.startswith('dashboard/'):
                    pending.append(other)
        elif is_test(path):
            continue
        else:
            users = repo.named_by(path)
            if not users and path in changed and not (path.startswith(INERT) or path in INERT_FILES):
                if why is not None:
                    why['*'] = f'nothing names {path}'
                return None  # nothing names it, and it isn't plainly inert: not clear what it touches
            for other in users:
                if path.startswith('docs/') and is_test(other):
                    add(other, f'names {path}')  # it reads the doc: it runs, what imports it doesn't change
                    continue
                if path.startswith('docs/') and not names_file(python_strings(other, repo.text.get(other, '')), path):
                    # it reads the folder (every help article, every doc): its own tests, not all that loads it; an
                    # article's own words are checked by the tests that name it
                    for user in repo.importers.get(other, set()) | repo.named_by(other):
                        if is_test(user):
                            add(user, f'{"imports" if user in repo.importers.get(other, ()) else "names"} {other}, which reads {Path(path).parent}/')
                    continue
                if not add(other, f'names {path}'):
                    continue
                if other in PAGE:
                    # the page's own assembly: its importers, one step (the Python tests that look at the page name it)
                    for user in repo.importers.get(other, ()):
                        add(user, f'imports {other}, which names {path}')
                elif other.endswith('.py'):
                    # a Python file that reads it changes with it: the whole chain above it, as for a change to its code
                    pending.append(other)
                elif not other.startswith('dashboard/'):
                    # a helper (tests/dashboard-page.mjs, a root .mjs module, the plugin's i18n.ts): whatever names it in
                    # turn. Another dashboard part that names this one is in the same page already, so the chain stops there.
                    pending.append(other)
    picked = {Path(p).name for p in [*reasons, *(f'tests/{name}' for name in ALWAYS)] if is_test(p) and (ROOT / p).exists()}
    every = [p for p in repo.paths if is_test(p)]
    if why is not None:
        why.update({Path(p).name: r for p, r in reasons.items() if is_test(p)})
    if len(picked) >= ENOUGH * len(every):
        return None
    return sorted(picked)


class Scopes:
    """Where each line of a Python file sits: in a function (its qualified name, as Python's co_qualname; its decorators
    and signature count as the function), or in a statement at module or class level (the names it defines)."""

    def __init__(self, text):
        self.funcs, self.stmts = [], []
        self._walk(ast.parse(text).body, '', None)

    def _walk(self, body, prefix, owner):
        for stmt in body:
            start = min([stmt.lineno] + [d.lineno for d in getattr(stmt, 'decorator_list', [])])
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qual = prefix + stmt.name
                # its decorators and signature too: what they set (a default, a wrapper) shows when it runs
                self.funcs.append((start, stmt.end_lineno, qual))
                self._walk(stmt.body, qual + '.<locals>.', ('func', qual))
            elif isinstance(stmt, ast.ClassDef) and owner is not None and owner[0] == 'func':
                # a class made inside a function: its methods are that function's '<locals>.Class.method'; the rest of
                # its body runs with the function
                self._walk(stmt.body, prefix + stmt.name + '.', ('func', owner[1]))
            elif isinstance(stmt, ast.ClassDef) and (owner is None or owner[0] == 'class'):
                names = {stmt.name} | (owner[1] if owner else set())
                first = stmt.body[0].lineno
                self.stmts.append((start, first - 1, names))
                self._walk(stmt.body, prefix + stmt.name + '.', ('class', names))
            elif owner is None or owner[0] == 'class':
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str):
                    continue  # a docstring
                # an import defines its names for this file alone (what else reads them imports them itself)
                self.stmts.append((start, stmt.end_lineno, defined(stmt), isinstance(stmt, (ast.Import, ast.ImportFrom))))
            else:
                self._walk([s for s in ast.iter_child_nodes(stmt) if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))],
                           prefix, owner)

    def at(self, line):
        """('func', qualname), ('names', {names}) (empty: a statement that defines nothing, as a call at import), or None."""
        inner = None
        for start, end, qual in self.funcs:
            if start <= line <= end and (inner is None or start >= inner[0]):
                inner = (start, end, qual)
        if inner:
            return 'func', inner[2]
        for start, end, names, *local in self.stmts:
            if start <= line <= end:
                return ('local' if local and local[0] else 'names'), names
        return None


def defined(stmt):
    """The names a module- or class-level statement defines."""
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {stmt.name}
    names = set()
    for node in ast.walk(stmt):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((alias.asname or alias.name).split('.')[0] for alias in node.names if alias.name != '*')
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            names.add(node.attr)
    return names


class Impact:
    """The test-impact map (scripts/test_impact.py): which test files ran each function, from main's last full run."""

    def __init__(self, data):
        self.tests = data['tests']
        self.mapped = set(self.tests)
        self.known = set(data.get('known') or ())
        self.files = data['files']
        self.commit = data.get('commit') or ''
        self.js = data.get('js') or {}
        self.js_tests = {self.tests[i] for i in data.get('js_tests') or ()}
        self.seconds = data.get('seconds') or {}
        self.wide = False  # a push to main: every test that ran a changed function (see few in select_mapped)
        # what tests ran only while setting up, and a part's functions they ran only while their page loaded
        self.setup = data.get('setup') or {}
        self.load = {part: {(a, b): ids for a, b, ids in spans} for part, spans in (data.get('load') or {}).items()}

    def ran(self, path, qualname):
        return {self.tests[i] for i in self.files.get(path, {}).get(qualname, ())}

    def quickest(self, names, count=STARTS):
        return set(sorted(names, key=lambda name: (self.seconds.get(name, 1e9), name))[:count])

    def _past_start(self, ran, only):
        if not only or only >= ran:  # start code (or a map without phases): every test that ran it
            return ran
        return (ran - only) | self.quickest(only)

    def exercised(self, path, qualname):
        """The tests that ran a function past setting up, and a few that ran it only then; every test that ran it when
        it only runs while tests set up."""
        return self._past_start(self.ran(path, qualname), {self.tests[i] for i in self.setup.get(path, {}).get(qualname, ())})

    def js_exercised(self, part, start, end, ids):
        """The same for a dashboard part's function at [start, end): the tests that ran it after their page loaded."""
        return self._past_start({self.tests[i] for i in ids}, {self.tests[i] for i in self.load.get(part, {}).get((start, end), ())})

    def ran_any(self, path):
        return {self.tests[i] for ids in self.files.get(path, {}).values() for i in ids}


def map_text(commit, path):
    """path as the map's commit had it: a pull request's checkout may not have that commit yet (fetch-depth 2)."""
    if not commit:
        return None
    text = git_text(commit, path)
    if text is None:
        subprocess.run(['git', 'fetch', '--quiet', '--depth=1', 'origin', commit], cwd=ROOT, capture_output=True, timeout=120)
        text = git_text(commit, path)
    return text


def changed_spans(old, new):
    """Where new differs from old: (start, end, new start, new end) character offsets, in old and in new (start == end:
    an insertion there)."""
    import difflib
    old_lines, new_lines = old.splitlines(keepends=True), new.splitlines(keepends=True)
    old_at, new_at = [0], [0]
    for line in old_lines:
        old_at.append(old_at[-1] + len(line))
    for line in new_lines:
        new_at.append(new_at[-1] + len(line))
    spans = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes():
        if tag == 'equal':
            continue
        a, b = ''.join(old_lines[i1:i2]), ''.join(new_lines[j1:j2])
        if len(a) + len(b) > 40000:  # a rewrite: all of it
            spans.append((old_at[i1], old_at[i2], new_at[j1], new_at[j2]))
            continue
        for tag2, k1, k2, l1, l2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag2 != 'equal':
                spans.append((old_at[i1] + k1, old_at[i1] + k2, new_at[j1] + l1, new_at[j1] + l2))
    return spans


def placer(old, text, loose=False):
    """A function that takes an offset in text to the same place in old, where its line is one old has unchanged too
    (None where it isn't): the map's commit and a pull request's base can be some commits apart. loose: a line that
    changed since goes to its counterpart, in a run of as many changed lines on both sides (the same statement, edited
    again), else to the start of the lines that replaced it there, or with last=True to their end."""
    import bisect
    import difflib
    if old == text:
        return lambda at: at
    old_lines, lines = old.splitlines(keepends=True), text.splitlines(keepends=True)
    old_at, at_ = [0], [0]
    for line in old_lines:
        old_at.append(old_at[-1] + len(line))
    for line in lines:
        at_.append(at_[-1] + len(line))
    same, block = {}, {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old_lines, lines, autojunk=False).get_opcodes():
        if tag == 'equal' or loose and tag == 'replace' and i2 - i1 == j2 - j1:
            same.update({j1 + k: i1 + k for k in range(j2 - j1)})
        elif loose and tag == 'replace':
            block.update({j1 + k: (old_at[i1], old_at[i2] - 1) for k in range(j2 - j1)})
    same[len(lines)] = len(old_lines)  # the end

    def place(at, last=False):
        line = bisect.bisect_right(at_, at) - 1
        if line in block:
            return block[line][last]
        if line not in same:
            return None
        return old_at[same[line]] + min(at - at_[line], max(old_at[same[line] + 1] - old_at[same[line]] - 1, 0)) if same[line] < len(old_lines) else old_at[same[line]]
    return place


def moved_spans(old, base, new):
    """changed_spans(base, new) with their old-side offsets in old (the map's text), or None when one sits where old
    and base differ already."""
    if base == old:
        return changed_spans(old, new)
    if new == old:  # the map was made with this change in (from its own branch): where it is now
        return [(c, d, c, d) for _, _, c, d in changed_spans(base, new)]
    place, out = placer(old, base, loose=True), []
    for start, end, new_start, new_end in changed_spans(base, new):
        a, b = place(start), place(max(start, end - 1), last=True)
        if a is None or b is None:
            return None
        out.append((a, b + (end > start or b > a), new_start, new_end))
    return out


# a line of a name -> method table: 'graph_role': 'graph_role_action', (maybe opening or closing it)
TABLE_LINE = re.compile(r"""(?:[A-Za-z_]\w*\s*=\s*\{\s*)?(?:['"][\w.-]+['"]\s*:\s*['"][\w.-]+['"]\s*,?\s*)+\}?""")

# a function more tests than this run past their start: on a pull request, the quickest few of them and those that
# name it (scripts/test_select.py --wide, as a push to main runs, takes them all)
EVERYWHERE, EVERYWHERE_KEEP = 60, 12

JS_WORD = r'[A-Za-z_$][\w$]*'


def js_blank(text):
    """text with its strings, comments and bracketed parts blanked: what's left of a statement at the top level."""
    out, depth, i, quote = [], 0, 0, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in '\'"`':
            quote = c
            out.append(c + c if depth == 0 else '')
        elif text.startswith('//', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            continue
        elif text.startswith('/*', i):
            end = text.find('*/', i + 2)
            i = len(text) if end < 0 else end + 2
            continue
        elif c in '([{':
            if depth == 0:
                out.append(c)
            depth += 1
        elif c in ')]}':
            depth = max(depth - 1, 0)
            if depth == 0:
                out.append(c)
        elif depth == 0:
            out.append(c)
        i += 1
    return ''.join(out)


def js_split(text):
    """text's top-level statements, as written: split at a ; or a line start outside strings, comments and brackets,
    where the line before doesn't go on."""
    out, depth, i, quote, start = [], 0, 0, None, 0
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in '\'"`':
            quote = c
        elif text.startswith('//', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
            continue
        elif text.startswith('/*', i):
            end = text.find('*/', i + 2)
            i = len(text) if end < 0 else end + 2
            continue
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth = max(depth - 1, 0)
        elif depth == 0 and (c == ';' or c == '\n' and not re.match(r'[\s)\]}.?:,]', text[i + 1:i + 2])
                             and not re.search(r'[,(\[{=+\-*/&|?:]\s*$', js_blank(text[start:i]))):
            if text[start:i + (c == ';')].strip():
                out.append(text[start:i + (c == ';')])
            start = i + 1
        i += 1
    if text[start:].strip():
        out.append(text[start:])
    return out


# A listener for clicks anywhere that does nothing unless the click is on what a selector finds:
# document.addEventListener('click',e=>{const b=e.target.closest('[data-x]');if(!b)return;...})
DELEGATED = re.compile(r"""\s*document\.addEventListener\(\s*'(?:click|change|input|submit|keydown)'\s*,\s*(?:async\s*)?(\w+)\s*=>\s*\{\s*"""
                       r"""const\s+(\w+)\s*=\s*\1\.target\.closest(?:\?\.)?\(\s*'([^'\\]+)'\s*\)\s*;?\s*if\s*\(\s*(?:!\2\s*\)\s*return\s*[;}]|\2\s*\)\s*\{)""")


def js_brackets(text):
    """The bracket pairs of JavaScript text, (open, close) offsets: strings, comments and the text of templates
    skipped, their ${...} parts not."""
    pairs, stack, i, n = [], [], 0, len(text)
    modes = ['code']  # code, or template; a ${ in a template opens code that its } closes
    while i < n:
        c = text[i]
        if modes[-1] == 'template':
            if c == '\\':
                i += 2
                continue
            if c == '`':
                modes.pop()
            elif text.startswith('${', i):
                modes.append('code')
                stack.append(('${', i + 1))
                i += 2
                continue
            i += 1
            continue
        if c in '\'"':
            j = i + 1
            while j < n and text[j] != c and text[j] != '\n':
                j += 2 if text[j] == '\\' else 1
            i = j + 1
            continue
        if c == '`':
            modes.append('template')
        elif text.startswith('//', i):
            j = text.find('\n', i)
            i = n if j < 0 else j
            continue
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        elif c in '([{':
            stack.append((c, i))
        elif c in ')]}':
            if stack:
                kind, at = stack.pop()
                pairs.append((at, i))
                if kind == '${':
                    modes.pop()
        i += 1
    return pairs


def in_function(text, start, end):
    """Whether [start, end) of JavaScript text sits inside the body of a function there (an arrow's or a function's
    {...}, or an arrow's expression in brackets)."""
    if text is None:
        return False
    for at, close in sorted(js_brackets(text), key=lambda p: p[0] - p[1]):  # innermost first
        if not (at < start and max(end, start + 1) <= close):
            continue
        if text[at] != '{':
            continue
        before = text[:at].rstrip()
        if before.endswith('=>'):
            return True
        if before.endswith(')'):
            opened = next((a for a, c in js_brackets(before + ' ') if c == len(before) - 1), None)
            word = re.search(r'([\w$]+)\s*$', before[:opened]) if opened is not None else None
            if word and word[1] not in ('if', 'for', 'while', 'switch', 'catch', 'with'):
                return True
    return False


def block_end(text, at):
    """Where the bracket at text[at] closes (strings, templates and comments skipped), or None."""
    depth, i, quote = 0, at, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in '\'"`':
            quote = c
        elif text.startswith('//', i):
            i = text.find('\n', i)
            if i < 0:
                return None
            continue
        elif text.startswith('/*', i):
            i = text.find('*/', i + 2)
            if i < 0:
                return None
            i += 2
            continue
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def js_declared(statement):
    """The names a top-level statement (blanked) only declares, or None when it does more at load (a call, an
    assignment, new): those run for every page."""
    # an arrow function, its body too: a block, or an expression up to the next declaration (x=>(+x||0).toFixed(1))
    text = re.sub(r'(?:async\s*)?(?:\(\)|' + JS_WORD + r')\s*=>[^,;]*', 'F', statement.strip()).strip(' ;\n\t')
    if not text or not re.search(r'[\w$]', text) or text == 'F':  # F: a function, whose own change its tests cover
        return set()
    match = re.fullmatch(r'(?:export\s+)?(?:async\s+)?function\s*\*?\s*(' + JS_WORD + r')\s*\(\)\s*\{\}', text)
    if match:
        return {match[1]}
    match = re.fullmatch(r'(?:export\s+)?class\s+(' + JS_WORD + r')(?:\s+extends\s+' + JS_WORD + r')?\s*\{\}', text)
    if match:
        return {match[1]}
    match = re.fullmatch(r'(?:export\s+)?(?:const|let|var)\s+(.+)', text, re.S)
    plain = r"F|\{\}|\[\]|''|\"\"|``|-?[\d.]+|true|false|null|undefined|" + JS_WORD
    if not match:
        # NAME[key]=value or NAME.x.y=value with a value that runs nothing: what reads NAME
        match = re.fullmatch(r'(' + JS_WORD + r')(?:\[\]|\.' + JS_WORD + r')+\s*=\s*(' + plain + r')', text)
        return {match[1]} if match else None
    names = set()
    for part in match[1].split(','):
        target, eq, value = part.partition('=')
        target, value = target.strip(), value.strip()
        if re.fullmatch(JS_WORD, target):
            names.add(target)
        elif target in ('{}', '[]'):
            return None  # a destructuring: its names are in the blanked part
        else:
            return None
        # a value that runs nothing: a literal, an object or array, a function, another name
        if eq and not re.fullmatch(r"F|new (?:Map|Set|WeakMap|WeakSet)\(\)|\{\}|\[\]|''|\"\"|``|-?[\d.]+|true|false|null|undefined|" + JS_WORD + r"|(?:async\s+)?function\s*\*?\s*" + JS_WORD + r"?\s*\(\)\s*\{\}", value):
            return None
    return names


def git_text(base, path):
    try:
        return subprocess.run(['git', 'show', f'{base}:{path}'], cwd=ROOT, capture_output=True, text=True,
                              errors='replace', check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


def diff_lines(base, path):
    """(new lines, old lines) a change touched in path, from git diff -U0 between base and the working tree."""
    out = subprocess.run(['git', 'diff', '-U0', '--no-color', '--no-ext-diff', base, '--', path], cwd=ROOT,
                         capture_output=True, text=True, errors='replace', check=True).stdout
    new, old = set(), set()
    for match in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', out, re.M):
        a, b, c, d = int(match[1]), int(match[2] or 1), int(match[3]), int(match[4] or 1)
        old.update(range(a, a + b))
        new.update(range(c, c + d))
    return new, old


def catalog_changes(old, new):
    """key -> the texts a catalog change added, removed or changed for it (the key is the English text; a plural's
    forms count as its texts)."""
    old, new = json.loads(old or '{}'), json.loads(new or '{}')
    if not (isinstance(old, dict) and isinstance(new, dict)):
        raise ValueError('not a catalog')
    found = {}
    for key in set(old) | set(new):
        if old.get(key) != new.get(key):
            texts = found.setdefault(key, {key})
            for value in (old.get(key), new.get(key)):
                if isinstance(value, str):
                    texts.add(value)
                elif isinstance(value, dict):
                    texts.update(v for v in value.values() if isinstance(v, str))
    return found


def catalog_strings(old, new):
    """The keys and texts a catalog change added, removed or changed (the keys are the English text)."""
    return set().union(*catalog_changes(old, new).values())


def text_pattern(strings):
    """A pattern for any of these texts, or their longest piece around {slots}, as whole words. When that piece is short
    ('{} and {} more': more), all the pieces in their order, each slot filled with a short run of text ('Ann and 2
    more')."""
    found = set()
    for text in strings:
        raw = re.split(r'\{[^}]*\}', text)
        parts = [p.strip() for p in raw if p.strip()]
        piece = max(parts, key=len) if parts else ''
        if len(piece) < 2:
            continue
        if len(parts) > 1 and len(piece) < SHORT_PIECE:
            inner = list(raw)
            while not inner[0].strip():
                inner.pop(0)
            while not inner[-1].strip():
                inner.pop()
            inner[0], inner[-1] = inner[0].lstrip(), inner[-1].rstrip()
            body = SLOT.join(re.escape(p) for p in inner)
            found.add((len(piece), (r'\b' if inner[0][0].isalnum() else '') + body + (r'\b' if inner[-1][-1].isalnum() else '')))
        else:
            found.add((len(piece), (r'\b' if piece[0].isalnum() else '') + re.escape(piece) + (r'\b' if piece[-1].isalnum() else '')))
    if not found:
        return None
    return re.compile('|'.join(p for _, p in sorted(found, reverse=True)))


# A piece of a catalog text shorter than this ('more', 'Saved') is found only with the other pieces around its slots.
SHORT_PIECE = 12
SLOT = r"""[^\n'"`<>]{1,40}?"""


def without_comments(text):
    """text without its whole-line comments (# or //): a test names a text where it asserts it, not where it says why."""
    return '\n'.join('' if line.lstrip().startswith(('#', '//')) else line for line in text.split('\n'))


def token_word(token):
    """A class, id or attribute name as code uses it: whole, and a data-x attribute as dataset.x too. <tag: where
    markup or code makes that element."""
    if token.startswith('<'):
        tag = re.escape(token[1:])
        made = r'|\bnew Option\(' if token == '<option' else ''
        return re.compile(r'<' + tag + r'(?![\w-])|createElement\(\s*[\'"`]' + tag + r'[\'"`]\s*\)' + made, re.I)
    forms = [r'(?<![\w-])' + re.escape(token) + r'(?![\w-])']
    if token.startswith('data-') and len(token) > 5:
        key = re.sub(r'-([a-z])', lambda m: m[1].upper(), token[5:])
        forms.append(r'\bdataset(?:\.' + re.escape(key) + r'\b|\[\s*[\'"]' + re.escape(key) + r'[\'"])')
    return re.compile('|'.join(forms))


def closed_dialogs(html, word):
    """The ids of the elements that start hidden (a closed <dialog>, a hidden panel) every place word finds in html
    sits in, the innermost one each, or None when one isn't in one. An include line (/*@include dashboard/x.js*/)
    names a file, not an element."""
    html = re.sub(r'/\*@include [^*]*\*/|<!--@include [^>]*-->', lambda m: ' ' * len(m[0]), html)
    spans = [(m.start(), m.end()) for m in word.finditer(html)]
    return hidden_holders(html, spans) if spans else set()


class _Elements(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.starts = [0] + [i + 1 for i, c in enumerate(text) if c == '\n']
        self.open, self.done, self.end = [], [], len(text)
        self.feed(text)
        self.close()
        self.done += [(start, self.end, attrs) for _, start, attrs in self.open]

    def at(self):
        line, column = self.getpos()
        return self.starts[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.open.append((tag, self.at(), dict(attrs) | {'<': tag}))

    def handle_endtag(self, tag):
        for i in range(len(self.open) - 1, -1, -1):
            if self.open[i][0] == tag:
                at = self.at()
                for _, start, attrs in self.open[i:]:
                    self.done.append((start, at + len(tag) + 3, attrs))
                del self.open[i:]
                return


def hidden_holders(html, spans):
    """The ids of the elements that start hidden (a hidden attribute, a <dialog> that isn't open) that each span of
    html sits in, the innermost one each; None when a span isn't in one."""
    try:
        elements = _Elements(html).done
    except Exception:  # markup the parser can't follow
        return None
    found = set()
    for a, b in spans:
        around = [(start, attrs) for start, end, attrs in elements if start <= a and max(b, a + 1) <= end
                  and attrs.get('id') and ('hidden' in attrs or attrs['<'] == 'dialog' and 'open' not in attrs)]
        if not around:
            return None
        found.add(max(around, key=lambda e: e[0])[1]['id'])
    return found


def css_rules(text):
    """The style rules of a stylesheet: (start, end, selector, groups), from the rule's start (just after what came
    before it) to after its }, and the (start, end) of each @media, @supports or @container block it sits in, up to its
    {, so a change to the condition reaches every rule in it. @keyframes, @font-face and the like are one rule whose
    selector starts with @; a rule nested in another is part of it. None when the braces don't add up."""
    clean = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m[0]), text, flags=re.S)
    rules, stack, start = [], [], 0
    for i, c in enumerate(clean):
        if c == '{':
            prelude = clean[start:i].strip()
            if stack and stack[-1][0] in ('rule', 'inner'):
                kind = 'inner'
            elif re.match(r'@(?:media|supports|container|layer|scope)\b', prelude):
                kind = 'group'
            else:
                kind = 'rule'
            stack.append((kind, start, i + 1, prelude))
            start = i + 1
        elif c == '}':
            if not stack:
                return None
            kind, at, brace, prelude = stack.pop()
            if kind == 'rule':
                rules.append((at, i + 1, prelude, [(g[1], g[2]) for g in stack if g[0] == 'group']))
            start = i + 1
        elif c == ';' and not (stack and stack[-1][0] in ('rule', 'inner')):
            start = i + 1
    return None if stack else rules


def css_tokens(selector):
    """For each selector in a list, the classes, ids and attribute names an element it styles has (not the ones in
    :not(), :has() and the like, which it may lack; :is(.a,.b) x counts as .a x and .b x); None when one of them names
    none (button, :root, @keyframes): those style what no name finds."""
    if selector.startswith('@'):
        return None
    alternative = re.search(r':(?:is|where)\(((?:[^()]|\([^()]*\))*)\)', selector)
    if alternative:  # :is(.a,.b) x: .a x or .b x
        out = []
        for one in split_top(alternative[1]):
            found = css_tokens(selector[:alternative.start()] + one + selector[alternative.end():])
            if found is None:
                return None
            out += found
        return out
    out = []
    for piece in split_top(selector):
        plain = re.sub(r':[\w-]+\((?:[^()]|\([^()]*\))*\)', ' ', piece)
        names = set(re.findall(r'[.#](-?[A-Za-z_][\w-]*)', plain)) | set(re.findall(r'\[\s*([A-Za-z_][\w-]*)', plain))
        if not names:
            # only a tag (option, select option): where markup or code makes that element; not the page's own frame
            tag = re.match(r'([a-z][a-z0-9-]*)(?![\w-])', re.split(r'[\s>+~]+', plain.strip())[-1])
            if not tag or tag[1] in ('html', 'body', 'head'):
                return None
            names = {'<' + tag[1]}
        out.append(names)
    return out


def split_top(text):
    """text split at its commas outside brackets."""
    out, depth, piece = [], 0, ''
    for c in text + ',':
        if c == ',' and depth == 0:
            out.append(piece)
            piece = ''
            continue
        depth += c in '(['
        depth -= c in ')]'
        piece += c
    return out


def folder_named(text, folder, rest):
    """The folder named as the way to this file: 'docs/' + name, f'docs/{x}', ROOT / 'docs', ROOT / 'docs' / 'help' (for
    a file in docs/help), but not 'docs/development.md' or ROOT / 'docs' / 'brand' (another file in it)."""
    at = text.find(folder)
    while at >= 0:
        prev, after = text[at - 1:at], text[at + len(folder):at + len(folder) + 80]
        if not (prev and (prev.isalnum() or prev in '_.-')):
            if after.startswith('/'):
                nxt = re.match(r'[\w.-]*', after[1:]).group()
                if not nxt or rest and nxt == rest[0]:
                    return True
            elif prev in ('"', "'") and after[:1] == prev and text[max(0, at - 40):at - 1].rstrip().endswith(('/', 'joinpath(')):
                deeper = re.match(r'''\s*/\s*['"]([\w.-]+)['"]''', after[1:])
                if not deeper or rest and deeper.group(1) == rest[0]:
                    return True
        at = text.find(folder, at + 1)
    return False


def names_exactly(text, path):
    """text names path: its path, its file name, a dashboard part's name, or (folder_named) its folder."""
    name = Path(path).name
    if path in text or name in text and mentions(text, name, '.-', '-'):
        return True
    stem = Path(path).stem if path.startswith('dashboard/') and Path(path).suffix in ('.js', '.css', '.html') else None
    if stem and stem in text and mentions(text, stem, '-', '-'):
        return True
    parts = path.split('/')
    folders = [('/'.join(parts[:n]), parts[n:]) for n in range(1, len(parts)) if '/'.join(parts[:n]) != 'tests']
    if any(folder in text and folder_named(text, folder, rest) for folder, rest in folders):
        return True
    return any(form in text for folder, rest in folders if '/' in folder for form in ("' / '".join(folder.split('/')), '" / "'.join(folder.split('/'))))


def names_file(text, path):
    """text names this file itself (its path or file name), not only a folder it's in."""
    name = Path(path).name
    return path in text or name in text and mentions(text, name, '.-', '-')


def python_strings(path, text):
    """A Python file's strings but its docstrings ('see docs/code-map.md' reads nothing); other files as they are."""
    if not path.endswith('.py'):
        return text
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return text
    docs = {id(node.value) for node in ast.walk(tree) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)}
    return '\n'.join(node.value for node in ast.walk(tree)
                     if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs)


def mention_lines(text, path):
    """The lines of a file that name another one (names_exactly), or import it when it's Python."""
    stem = Path(path).stem if path.endswith('.py') else None
    found = []
    for number, line in enumerate(text.split('\n'), 1):
        if names_exactly(line, path) or stem and stem in line and re.search(r'\b(?:import|from)\b[^\n]*\b' + re.escape(stem) + r'\b', line):
            found.append(number)
    return found


# The tests that check the catalogs themselves (keys, slots, every language). With the map, a catalog change runs these
# and the tests that name a text it changed; a test that only serves a catalog to the page shows what it asserts.
CATALOG_CHECKS = re.compile(r'^test_(?:i18n|locale)')
# A script that looks over files in bulk (a glob, git ls-files).
WALKS = re.compile(r"""\.r?glob\(|['"]ls-files['"]""")
_NAMES = {}


def code_names(path, text):
    """(name -> lines where it's used bare, name -> lines where it's used after a dot or as a string that is just the name,
    as getattr(x, 'name')). Not in comments or other text ('it timed out' doesn't use timed)."""
    if path not in _NAMES:
        bare, dotted, after_dot = {}, {}, False
        try:
            for tok in tokenize.generate_tokens(io.StringIO(text).readline):
                if tok.type == tokenize.NAME:
                    (dotted if after_dot else bare).setdefault(tok.string, set()).add(tok.start[0])
                elif tok.type == tokenize.STRING:
                    inner = tok.string.lstrip('rbuRBU').strip('\'"')
                    if inner.isidentifier():
                        dotted.setdefault(inner, set()).add(tok.start[0])
                if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT):
                    after_dot = tok.type == tokenize.OP and tok.string == '.'
        except (tokenize.TokenError, SyntaxError, IndentationError):
            for number, line in enumerate(text.split('\n'), 1):
                for word in re.findall(r'\w+', line):
                    bare.setdefault(word, set()).add(number)
                    dotted.setdefault(word, set()).add(number)
        _NAMES[path] = bare, dotted
    return _NAMES[path]


def imported_names(repo, path, source):
    """The names path takes from source with from ... import (as it calls them)."""
    found = set()
    try:
        tree = ast.parse(repo.text.get(path, ''))
    except (SyntaxError, ValueError):
        return found
    package = module_name(path).rsplit('.', 1)[0] if '/' in path else ''
    if path.endswith('__init__.py'):
        package = module_name(path)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ''
            if node.level:
                base = package.split('.') if package else []
                base = base[:len(base) - (node.level - 1)] if node.level > 1 else base
                module = '.'.join(base + ([module] if module else []))
            if source in repo._resolve(module, path):
                found.update((alias.name, alias.asname or alias.name) for alias in node.names)
    return found


def select_mapped(changed, repo, impact, base, why=None):
    """select() with the test-impact map: a change to a function runs the tests that ran it; a change at module level
    runs the tests of the functions that use what it defines; a catalog change runs the tests that name a text it
    changed. Files the map doesn't know, and tests it doesn't know, are picked by following imports, as before."""
    reasons, fallback, scopes, seen = {}, set(), {}, set()
    tests = {p for p in repo.paths if is_test(p)}

    def add(test, reason):
        name = Path(test).name
        if name not in reasons:
            reasons[name] = reason

    def few(picked, name):
        """A function more than EVERYWHERE tests run past their start (a render every page does, App.action): on a pull
        request, the quickest EVERYWHERE_KEEP of them and those that name it. A push to main (--wide) runs them all."""
        if impact.wide or len(picked) <= EVERYWHERE:
            return picked
        word = re.compile(r'(?<![\w$])' + re.escape(name.split('.')[-1]) + r'(?![\w$])') if name else None
        return impact.quickest(picked, EVERYWHERE_KEEP) | {t for t in picked if word and word.search(repo.text.get(f'tests/{t}', ''))}

    def js_function_name(part, at):
        """The name of the function that starts at offset at of part, as the map's commit had it, or None."""
        text = js_old(part)[0] or ''
        found = re.match(r'(?:async\s+)?function\s*\*?\s*([\w$]+)', text[at:at + 120]) or \
            re.search(r'([\w$]+)\s*[=:]\s*(?:async\s*)?$', text[max(0, at - 80):at])
        return found[1] if found else None

    def scope_of(path, text):
        if path not in scopes:
            try:
                scopes[path] = Scopes(text)
            except (SyntaxError, ValueError):
                scopes[path] = None
        return scopes[path]

    def users(path):
        """Python files that can see what path defines: itself, what imports it, what names it."""
        return {path} | repo.importers.get(path, set()) | {p for p in repo.named_by(path) if p.endswith('.py')}

    def lines_in(path, lines, why_text, depth=0, text=None, key=None):
        """The tests the given lines of a Python file reach."""
        if is_test(path):
            add(path, why_text)
            return
        if path not in impact.known:
            fallback.add(path)
            return
        text = text if text is not None else repo.text.get(path)
        found = scope_of(key or path, text) if text is not None else None
        if found is None:
            fallback.add(path)
            return
        for line in lines:
            plain = text.split('\n')[line - 1].strip() if 0 < line <= text.count('\n') + 1 else ''
            if not plain or plain.startswith('#'):
                continue
            where = found.at(line)
            if where is None:
                continue
            if where[0] == 'func':
                ran = impact.ran(path, where[1])
                if not ran and impact.files.get(path) is not None and where[1] not in old_functions(path):
                    # a new function: what calls it
                    for name in {where[1].split('.<locals>.')[0].split('.')[-1]}:
                        names_in(path, name, why_text, depth)
                for test in few(impact.exercised(path, where[1]), where[1]):
                    add(test, f'ran {path}:{where[1]} ({why_text})')
            elif where[1]:
                if where[0] == 'names' and TABLE_LINE.fullmatch(plain) and table_entries(path, found, text, plain, where[1], why_text):
                    continue
                for name in where[1]:
                    names_in(path, name, why_text, depth, local=where[0] == 'local')
            else:
                for test in impact.ran_any(path):
                    add(test, f'ran {path}, which runs code at import ({why_text})')

    def table_entries(path, found, text, plain, names, why_text):
        """Entries of a name -> method table ('graph_role': 'graph_role_action',) that changed: the tests that ran those
        methods or name those keys (a test, a dashboard part that sends it, Python that passes it), and those that read
        the whole table (that name it, or a table made from it at import). False when a key's users aren't all clear."""
        for key, value in re.findall(r"""['"]([\w.-]+)['"]\s*:\s*['"]([\w.-]+)['"]""", plain):
            for _, _, qual in found.funcs:
                if qual == value or qual.endswith('.' + value):
                    for test in few(impact.exercised(path, qual), qual):
                        add(test, f'ran {path}:{qual} ({why_text})')
            if not string_users(key, path, f'{path} maps {key!r} ({why_text})'):
                return False
        words, pending = set(names), [(path, name) for name in names]
        while pending:
            source, name = pending.pop()
            for other in users(source):
                other_text = repo.text.get(other)
                if other == source or other_text is None or name not in other_text or is_test(other):
                    continue
                bare, dotted = code_names(other, other_text)
                where = scope_of(other, other_text)
                if where is None:
                    return False
                for line in sorted(set(dotted.get(name, ())) | set(bare.get(name, ()))):
                    at = where.at(line)
                    code = other_text.split('\n')[line - 1]
                    if at is None or at[0] == 'local':
                        continue
                    if at[0] == 'names':  # a table made from it at import (what it assigns, not a loop's names)
                        for made in {m for m in at[1] - words if re.search(r'\b' + re.escape(m) + r'\s*(?::[^=\n]*)?=(?!=)', code)}:
                            words.add(made)
                            pending.append((other, made))
                    elif not re.search(r'\b' + re.escape(name) + r'(?:\[|\.get\()|\bin\s+(?:self\.|\w+\.)?' + re.escape(name) + r'\b', code):
                        for test in few(impact.exercised(other, at[1]), at[1]):  # it goes over the table: what it gives changes
                            add(test, f'ran {other}:{at[1]}, which reads {name} ({why_text})')
        for test in tests:
            test_text = repo.text.get(test, '')
            if any(re.search(r'\b' + re.escape(word) + r'\b', test_text) for word in words):
                add(test, f'names {sorted(words)[0]} ({why_text})')
        return True

    def string_users(key, path, why_text):
        """The tests that run code that has key as a whole string: False when one such place can't be told."""
        quoted = re.compile(r"""(['"`])""" + re.escape(key) + r'\1')
        for other in repo.paths:
            other_text = repo.text.get(other)
            if other == path or not other_text or key not in other_text or other.startswith(NOT_CODE):
                continue
            spots = [m.start() + 1 for m in quoted.finditer(other_text)]
            if not spots:
                continue
            if is_test(other):
                add(other, f'names {key!r} ({why_text})')
            elif other.startswith('dashboard/') and other.endswith('.js'):
                if other in changed:
                    continue
                old_text = js_old(other)[0]
                if other not in impact.js or old_text is None:
                    return False
                place = placer(old_text, other_text)
                at = [place(a) for a in spots]
                if any(a is None for a in at):
                    js_loaders(other, f'loads {other}, which sends {key!r} ({why_text})')
                    continue
                for a in at:
                    js_place(other, a, a + len(key), key, why_text, 0)
            elif other.endswith('.py'):
                lines_in(other, sorted({other_text.count('\n', 0, a) + 1 for a in spots}), f'{other} names {key!r} ({why_text})')
            elif Path(other).suffix in CODE:
                return False
        return True

    def old_functions(path):
        key = ('old', path)
        if key not in scopes:
            old = git_text(base, path) if base else None
            try:
                scopes[key] = {q for _, _, q in Scopes(old).funcs} if old else set()
            except (SyntaxError, ValueError):
                scopes[key] = set()
        return scopes[key]

    def names_in(path, name, why_text, depth, local=False):
        """The tests that run what uses name, defined at module or class level in path."""
        if (path, name) in seen:
            return
        seen.add((path, name))
        word = re.compile(r'\b' + re.escape(name) + r'\b')
        for other in ({path} if local else users(path)):
            text = repo.text.get(other)
            if text is None or name not in text:
                continue
            if is_test(other):
                lines = [1] if word.search(text) else []
            else:
                bare, dotted = code_names(other, text)
                # in another file the name is this one only after a dot (module.name, self.name) or imported by name
                used = set(dotted.get(name, ()))
                for local in ([name] if other == path else [a for n, a in imported_names(repo, other, path) if n == name]):
                    used |= bare.get(local, set())
                lines = sorted(used)
            if not lines:
                continue
            if depth >= 10 and not is_test(other):  # a chain this long: every test that ran that file
                for test in impact.ran_any(other):
                    add(test, f'ran {other}, which uses {name} ({why_text})')
                continue
            lines_in(other, lines, f'{other} uses {name} from {path}' if other != path else why_text, depth + 1)

    js_texts, js_seen = {}, set()
    plain_tests, drawn_keys = {}, {}

    def plain_test(test, text):
        if test not in plain_tests:
            plain_tests[test] = without_comments(text)
        return plain_tests[test]

    def key_drawn(key):
        """The tests that ran code that has key quoted (a call to t()), or None when the map can't place each place
        that has it: a file it doesn't know, one this change or one since the map's commit changed, or no place at all
        (the key is put together, or gone)."""
        if key not in drawn_keys:
            drawn_keys[key] = key_places(key)
        return drawn_keys[key]

    def key_places(key):
        forms = [q + key + q for q in '\'"`']
        found, places = set(), 0
        for other in repo.paths:
            if is_test(other) or other.startswith(NOT_CODE):
                continue
            text = repo.text.get(other)
            if not text or key not in text:
                continue
            at = [m.start() for form in forms for m in re.finditer(re.escape(form), text)]
            if not at:
                continue
            places += 1
            if other in changed:
                return None
            if other.endswith('.py') and other in impact.known:
                found_scopes = scope_of(other, text)
                if found_scopes is None or (map_text(impact.commit, other) or '') != text:
                    return None
                for start in at:
                    where = found_scopes.at(text.count('\n', 0, start) + 1)
                    found |= impact.ran(other, where[1]) if where and where[0] == 'func' else impact.ran_any(other)
            elif other.startswith('dashboard/') and other.endswith('.js') and other in impact.js:
                old_text, funcs, _ = js_old(other)
                if old_text is None:
                    return None
                old_at = [m.start() for form in forms for m in re.finditer(re.escape(form), old_text)]
                if len(old_at) != len(at):
                    return None
                for start in old_at:
                    inner = [f for f in funcs if f[0] <= start < f[1]]
                    if inner:
                        found |= js_ran(min(inner, key=lambda f: f[1] - f[0])[2])
                    else:  # at load: what loads the part, and what runs any of it
                        found |= js_ran(impact.js[other].get('top', ())) | {t for f in funcs for t in js_ran(f[2])}
            else:
                return None
        return found if places else None

    def js_old(part):
        """part as the map's commit had it, its functions, and its text with every function blanked to F: what runs at
        the top level."""
        if part not in js_texts:
            text = map_text(impact.commit, part)
            funcs = sorted(impact.js.get(part, {}).get('funcs', []), key=lambda f: (f[0], -f[1]))
            top = None
            if text is not None:
                chars, end = list(text), -1
                for start, stop, _ in funcs:
                    if start >= end and 0 <= start < stop <= len(text):  # an outermost one
                        for i in range(start, stop):
                            if chars[i] != '\n':
                                chars[i] = ' '
                        chars[start] = 'F'
                        end = stop
                top = ''.join(chars)
            js_texts[part] = (text, funcs, top)
        return js_texts[part]

    def js_ran(ids):
        return {impact.tests[i] for i in ids}

    def js_statement(text, start, end):
        """The top-level statements of text around [start, end), blanked: whole lines, and the lines that continue them."""
        if end > start and text[end - 1] == '\n':
            end -= 1
        a = text.rfind('\n', 0, start) + 1
        b = text.find('\n', end)
        b = len(text) if b < 0 else b
        while a > 0:
            previous = text.rfind('\n', 0, a - 1) + 1
            if not re.match(r'[\s)\]}.?:,+\-*/&|]', text[a:a + 1]) and not re.search(r'[,(\[{=+\-*/&|?:]\s*$', text[previous:a - 1]):
                break
            a = previous
        while b < len(text):
            following = text.find('\n', b + 1)
            following = len(text) if following < 0 else following
            if not re.match(r'[ \t)\]}.?:,+\-*/&|]', text[b + 1:b + 2]) and not re.search(r'[,(\[{=+\-*/&|?:]\s*$', text[a:b]):
                break
            b = following
        return [piece for piece in re.split(r';|\n(?=[^\s)\]}.?:,])', js_blank(text[a:b])) if piece.strip()]

    page_wide = set()  # changed files whose change reaches every page test after all: the walk as without the map

    def js_loaders(part, reason):
        if part not in impact.js:  # a part the map doesn't know (a new one): every page test loads it
            page_wide.add(part)
            return
        for test in js_ran(impact.js.get(part, {}).get('top', ())):
            add(test, reason)

    def js_place(other, start, end, name, why_text, depth):
        """The tests that run what's at [start, end) of part other, as the map's commit had it: the innermost function
        there, or what uses what the top-level statement there declares."""
        text, funcs, top = js_old(other)
        inner = [f for f in funcs if f[0] <= start < f[1]]
        if inner:
            f = min(inner, key=lambda f: f[1] - f[0])
            for test in few(impact.js_exercised(other, *f), js_function_name(other, f[0])):
                add(test, f'runs {other} code that uses {name} ({why_text})')
        else:
            js_top(other, js_statement(top, start, end), f'{other} uses {name}', depth + 1)

    blanks = {}

    def js_clash(part, name):
        """Another part declares name at its top level too: the page stops at load."""
        for other in repo.paths:
            if other != part and other.startswith('dashboard/') and other.endswith('.js'):
                if other not in blanks:
                    blanks[other] = js_blank(repo.text.get(other, ''))
                if re.search(r'(?:\b(?:const|let|var|function\*?|class)\s+|,\s*)' + re.escape(name) + r'(?![\w$])\s*[=({;,\n]', blanks[other]):
                    return other
        return None

    def js_top(part, statements, why_text, depth):
        """The tests a change to these top-level statements of part reaches: what uses the names they declare, or every
        test that loads the page when they do more than declare."""
        for statement in statements:
            names = js_declared(statement)
            if names is None:
                js_loaders(part, f'loads {part}, whose top level changed ({why_text})')
                return
            for name in names:
                clash = js_clash(part, name)
                if clash:
                    js_loaders(part, f'loads {part}, which declares {name} as {clash} does ({why_text})')
                    return
                js_name(part, name, why_text, depth)

    def js_name(part, name, why_text, depth):
        """The tests that run code of the dashboard's parts that uses name, a global part declares."""
        if name in js_seen:
            return
        js_seen.add(name)
        if depth >= 10:
            js_loaders(part, f'loads {part}, which uses {name} ({why_text})')
            return
        word = re.compile(r'(?<![\w$.])' + re.escape(name) + r'(?![\w$])|(?:window|globalThis|self)\.' + re.escape(name) + r'(?![\w$])')
        for other in sorted(impact.js):
            if name not in repo.text.get(other, name):
                continue
            text, funcs, top = js_old(other)
            if text is None:
                continue
            for found in word.finditer(text):
                js_place(other, found.start(), found.end(), name, why_text, depth)
        handler = re.compile(r'\bon\w+=[^>]*\b' + re.escape(name) + r'\b')
        for other in repo.paths:
            if other.startswith('dashboard/') and not other.endswith('.js') and handler.search(repo.text.get(other, '')):
                js_loaders(part, f'loads {other}, whose handler uses {name} ({why_text})')
        named = re.compile(r'\b' + re.escape(name) + r'\b')
        for test in tests:
            if named.search(repo.text.get(test, '')):
                add(test, f'names {name} ({why_text})')

    def js_part(path, new):
        """A dashboard part's change, by the map's browser half: the tests that ran the functions it touched. False when
        the map can't place it."""
        if new is None:
            return False
        if path not in impact.js:
            if git_text(base, path) is not None:
                return False
            # a new part: what uses what it declares (a new name: the parts that call it changed too), the tests that
            # name it, and a few page tests for what it does at load; a name another part declares runs every page test
            for statement in js_split(new):
                listener = DELEGATED.match(statement)
                if listener and statement[listener.end() - 1] == '{':  # if(b){...}: nothing after that block
                    close = block_end(statement, listener.end() - 1)
                    listener = listener if close and re.match(r'\s*;?\s*\}', statement[close + 1:]) else None
                if listener and js_declared(js_blank(statement)) is None:
                    # a click on what has data-x: the tests that draw such elements (the change that draws them in
                    # this part runs its own)
                    if not drawn_by(css_tokens(listener[3]), f'{path} listens for clicks on {listener[3]}'):
                        return False
                    continue
                if js_declared(js_blank(statement)) is None:
                    for test in impact.quickest(impact.js_tests):
                        add(test, f'loads {path}, which is new')
                    continue
                js_top(path, [js_blank(statement)], f'{path} is new', 0)
            return path not in page_wide
        text, funcs, top = js_old(path)
        if text is None:
            return False
        # this change's own spans, placed in the map's text (main may have moved since the map: those changes aren't
        # this one's); where that can't be told, every difference from the map's text
        base_text = git_text(base, path)
        spans = moved_spans(text, base_text, new) if base_text is not None else None
        for start, end, new_start, new_end in (changed_spans(text, new) if spans is None else spans):
            inside = [f for f in funcs if (f[0] <= start and end <= f[1]) if start < end or f[0] < start < f[1]]
            if inside:
                # past the guard of a listener for clicks anywhere that acts only on what a selector finds: what
                # clicks such an element (the tests that draw it), not every test that clicks
                outer = max(inside, key=lambda f: f[1] - f[0])
                line = text.rfind('\n', 0, outer[0]) + 1
                listener = DELEGATED.match(text, line)
                guarded = listener and min(outer[1], (block_end(text, listener.end() - 1) if text[listener.end() - 1] == '{' else None) or outer[1])
                guarded = guarded if listener and (text[listener.end() - 1] != '{' or block_end(text, listener.end() - 1)) else None
                if listener and line <= outer[0] < listener.end() <= start and end <= (guarded or 0):
                    if drawn_by(css_tokens(listener[3]), f'{path} listens for clicks on {listener[3]}'):
                        for test in impact.quickest(impact.js_exercised(path, *outer)):
                            add(test, f'ran {path}:{outer[0]}-{outer[1]}')
                        continue
                inner = min(inside, key=lambda f: f[1] - f[0])
                for test in few(impact.js_exercised(path, *inner), js_function_name(path, inner[0])):
                    add(test, f'ran {path}:{inner[0]}-{inner[1]}')
                continue
            for f in funcs:
                if f[0] < end and start < f[1]:
                    for test in few(impact.js_exercised(path, *f), js_function_name(path, f[0])):
                        add(test, f'ran {path}:{f[0]}-{f[1]}')
            if in_function(top, start, end) and in_function(new, new_start, new_end):
                # inside a function no test ran: no test runs it; the quickest that load the part see it parse
                for test in impact.quickest(js_ran(impact.js.get(path, {}).get('top', ()))):
                    add(test, f'loads {path}, whose code no test ran changed')
                continue
            # whole lines put in between two others change no statement there (one that continues the line before is
            # in the new side's statement)
            between = start == end and (start == 0 or text[start - 1] == '\n')
            js_top(path, ([] if between else js_statement(top, start, end)) + js_statement(new, new_start, new_end), f'{path} changed', 0)
        return True

    def css_token_sites(token):
        """Where a class, id or attribute name is used outside stylesheets: (files, built). built: {file: [offsets]}
        where some code may put it together ('cl-' + kind, `fb-${x}`), so a file that has it whole isn't every one
        that makes it: those places draw it too."""
        word = token_word(token)
        # data-x and aria-x name what follows: a data-${key} elsewhere doesn't make every data- name
        cuts = [] if token.startswith('<') else [i for i, c in enumerate(token) if c == '-' and 0 < i < len(token) - 1 and token[:i] not in ('data', 'aria')]
        # 'chat-' + x or `chat-${x}` makes chat-back where 'back' is a string there too
        built = [(re.compile(r'(?<![\w-])' + re.escape(token[:i + 1]) + r"""(?:\$\{|['"`]\s*\+)"""),
                  re.compile(r"""['"`]""" + re.escape(token[i + 1:]) + r"""['"`]""")) for i in cuts]
        built += [(re.compile(r"""(?:\}|\+\s*['"`])""" + re.escape(token[i:]) + r'(?![\w-])'),
                   re.compile(r"""['"`]""" + re.escape(token[:i]) + r"""['"`]""")) for i in cuts]
        files, builders = [], {}
        for other in repo.paths:
            if Path(other).suffix not in ('.js', '.mjs', '.ts', '.html', '.py') or other.startswith(NOT_CODE):
                continue
            text = repo.text.get(other)
            if not text or token.startswith('<') and not word.search(text):
                continue
            if token not in text and not any(token[:i + 1] in text or token[i:] in text for i in cuts) and 'dataset' not in text and not token.startswith('<'):
                continue
            if word.search(text):
                files.append(other)
            if not is_test(other):  # a test draws no page
                at = sorted({m.start() for b, rest in built if rest.search(text) for m in b.finditer(text)})
                if at:
                    builders[other] = at
        return files, builders

    def css_part(path, new):
        """A stylesheet part's change: the tests that run the code that draws what the changed rules style, found by a
        class, id or attribute name each of their selectors needs (the one used in the fewest places). False when that
        isn't clear: a rule no such name finds (button, :root, @keyframes), a name nothing uses or some code puts
        together, or markup in the page itself."""
        old = git_text(base, path) if base else None
        if new is None:
            return False
        old_rules, new_rules = css_rules(old or ''), css_rules(new)
        if old_rules is None or new_rules is None:
            return False
        spans = changed_spans(old or '', new)
        selectors = set()
        for rules, ends in ((old_rules, [(s, e) for s, e, _, _ in spans]), (new_rules, [(s, e) for _, _, s, e in spans])):
            for a, b in ends:
                for start, end, selector, groups in rules:
                    if any(x < max(b, a + 1) and a < y for x, y in [(start, end), *groups]):
                        selectors.add(selector)
        for selector in sorted(selectors):
            if not drawn_by(css_tokens(selector), f'{path} styles it'):
                return False
        return True

    def drawn_by(needs, why_text):
        """The tests that run the code that draws elements that have, for each set in needs, one of its names (the
        one used in the fewest places): False when that isn't clear (see css_part)."""
        if needs is None:
            return False
        for names in needs:
            best = None
            for token in sorted(names):
                files, builders = css_token_sites(token)
                # only tests name it: the code that draws it puts it together some other way
                size = len(files) + sum(len(at) for at in builders.values())
                if any(not is_test(f) for f in files) and (best is None or size < best[0]):
                    best = (size, token, files, builders)
            if best is None:
                return False
            _, token, files, builders = best
            word = token_word(token)
            for other, at in builders.items():
                # where code may put the name together: the tests that run that code
                text = repo.text.get(other, '')
                if other.endswith('.js') and other.startswith('dashboard/') and other not in changed:
                    old_text = js_old(other)[0]
                    if other not in impact.js or old_text is None:
                        return False
                    place = placer(old_text, text)
                    spots = [place(a) for a in at]
                    if any(a is None for a in spots):
                        js_loaders(other, f'loads {other}, which may put {token} together ({why_text})')
                        continue
                    for a in spots:
                        js_place(other, a, a + 1, token, why_text, 0)
                elif other.endswith('.py') and not other.startswith('tests/'):
                    lines_in(other, sorted({text.count('\n', 0, a) + 1 for a in at}), f'{other} may put {token} together ({why_text})')
                elif other not in changed:
                    return False
            for other in files:
                text = repo.text.get(other, '')
                if is_test(other):
                    add(other, f'names {token} ({why_text})')
                elif other.endswith('.js') and other.startswith('dashboard/'):
                    if other in changed:
                        continue  # its own change's tests: what it draws with the name, whole
                    if other not in impact.js:
                        return False
                    old_text = js_old(other)[0]
                    if old_text is None:
                        js_loaders(other, f'loads {other}, which uses {token} ({why_text})')
                        continue
                    # each place the part uses it now, where the map's text has it too
                    place = placer(old_text, text)
                    at = [place(found.start()) for found in word.finditer(text)]
                    if any(a is None or not word.match(old_text, a) for a in at):
                        # main moved those lines since the map: the places the map's text has it, when that has it
                        # in no fewer places than now
                        at = [found.start() for found in word.finditer(old_text)]
                        if len(at) < len(list(word.finditer(text))):
                            js_loaders(other, f'loads {other}, which uses {token} ({why_text})')
                            continue
                    for a in at:
                        js_place(other, a, a + len(token), token, why_text, 0)
                elif other.endswith('.py') and not other.startswith('tests/'):
                    lines = [n for n, line in enumerate(text.split('\n'), 1) if word.search(line)]
                    lines_in(other, lines, f'{other} uses {token} ({why_text})')
                elif other == 'dashboard.html' or other.startswith('dashboard/') and other.endswith('.html'):
                    # in a closed dialog: drawn when the code that opens it runs
                    dialogs = closed_dialogs(text, word)
                    if dialogs is None:
                        return False  # the page's own markup, on show at load
                    for dialog in dialogs - {token} - dialogs_seen:
                        dialogs_seen.add(dialog)
                        if not drawn_by([{dialog}], f'{dialog} holds {token} ({why_text})'):
                            return False
                else:
                    return False  # code elsewhere that draws it
        return True

    dialogs_seen = set()

    def html_part(path, new):
        """A markup part's change inside elements that start hidden (a closed dialog, a hidden settings panel): the
        tests that run the code that shows them. False when a change is on show at load."""
        old = git_text(base, path)
        if new is None or old is None:
            return False
        holders = set()
        for text, ends in ((old, [(a, b) for a, b, _, _ in changed_spans(old, new)]),
                           (new, [(a, b) for _, _, a, b in changed_spans(old, new)])):
            found = hidden_holders(text, ends)
            if found is None:
                return False
            holders |= found
        for holder in sorted(holders - dialogs_seen):
            dialogs_seen.add(holder)
            if not drawn_by([{holder}], f'{path} changed inside #{holder}'):
                return False
        return True

    def includes_only(path):
        """A change to dashboard.html that only adds or removes include lines of parts this change adds or removes too:
        those parts' own changes say what it reaches."""
        if base is None:
            return False
        try:
            new_lines, old_lines = diff_lines(base, path)
        except (OSError, subprocess.CalledProcessError):
            return False
        new_text = (ROOT / path).read_text(encoding='utf-8', errors='replace').split('\n')
        old_text = (git_text(base, path) or '').split('\n')
        marker = re.compile(r'^(?:/\*@include (dashboard/[a-z0-9-]+\.(?:js|css))\*/|<!--@include (dashboard/[a-z0-9-]+\.html)-->)$')
        for lines, text in ((new_lines, new_text), (old_lines, old_text)):
            for n in lines:
                found = marker.match(text[n - 1].strip() if 0 < n <= len(text) else '')
                part = found and (found[1] or found[2])
                if not part or part not in changed or (ROOT / part).is_file() == (git_text(base, part) is not None):
                    return False
        return True

    for path in changed:
        if path in FULL:
            if why is not None:
                why['*'] = f'{path} is test machinery'
            return None
    for path in changed:
        new = (ROOT / path).read_text(encoding='utf-8', errors='replace') if (ROOT / path).is_file() else None
        if is_test(path):
            add(path, 'changed')
        elif path.endswith('.py'):
            old = git_text(base, path) if base else None
            if old is None and new is not None and path not in impact.known:
                # a new module: what it changes is where it's loaded
                for test in repo.named_by(path) & tests:
                    add(test, f'names {path}')
                for other in repo.importers.get(path, set()) | repo.named_by(path):
                    if other.endswith('.py') and other not in changed and other in repo.text:
                        lines_in(other, mention_lines(repo.text[other], path) or [1], f'loads {path}')
                    elif not other.endswith('.py') and other not in changed:
                        fallback.add(path)
                continue
            if path not in impact.known or base is None:
                fallback.add(path)
                continue
            try:
                new_lines, old_lines = diff_lines(base, path)
            except (OSError, subprocess.CalledProcessError):
                fallback.add(path)
                continue
            if new is not None:
                lines_in(path, sorted(new_lines), 'changed', text=new)
            if old is not None and old_lines:
                lines_in(path, sorted(old_lines), 'changed', text=old, key=('was', path))
            # a test that names the file other than to load it (spec_from_file_location, import) and runs none of it
            # reads it as text: it runs. One that loads it is covered by the functions it ran.
            loads = re.compile(r'(?:spec_from_file_location|load_module|module_from_spec)\([^\n]*' + re.escape(Path(path).name) + r'''|(?:import|from)\s+'''
                               + re.escape(module_name(path)) + r'\b')
            for test in {p for p in repo.named_by(path) if is_test(p)}:
                text = repo.text.get(test, '')
                if Path(test).name in impact.ran_any(path):
                    continue
                if Path(test).name not in impact.mapped or text.count(Path(path).name) > len(loads.findall(text)):
                    add(test, f'names {path}')
        elif path.startswith('i18n/') and path.endswith('.json') and base:
            try:
                keys = catalog_changes(git_text(base, path), new)
            except ValueError:
                fallback.add(path)
                continue
            for test in sorted(tests):
                text = repo.text.get(test)
                if text is not None and CATALOG_CHECKS.search(Path(test).name) and names_exactly(text, path):
                    add(test, f'checks the catalogs ({path})')
            for key, strings in sorted(keys.items()):
                # a test that asserts a text and runs code that draws that key; where the map can't say what draws
                # it (new code, a part it doesn't know), any test that asserts the text
                pattern, drawn = text_pattern(strings), key_drawn(key)
                literal = [q + key + q for q in '\'"`']
                for test in sorted(tests):
                    text = repo.text.get(test)
                    if text is None:
                        continue
                    name = Path(test).name
                    if any(form in text for form in literal):
                        add(test, f'names {key!r} ({path})')
                    elif pattern and (drawn is None or name in drawn or name not in impact.mapped) and pattern.search(plain_test(test, text)):
                        add(test, f'names a text {path} changed ({key!r})')
        else:
            # a dashboard part's functions: the tests that ran them in Chromium (scripts/test_impact_js.mjs). What else
            # names it follows, but past what names the part itself, only for the tests the browser half doesn't know.
            browser = path.startswith('dashboard/') and path.endswith('.js') and base is not None and js_part(path, new)
            if path.startswith('dashboard/') and path.endswith('.css') and base is not None:
                browser = css_part(path, new)
            elif path == 'dashboard.html':
                browser = includes_only(path)
            elif path.startswith('dashboard/') and path.endswith('.html') and base is not None:
                browser = html_part(path, new)
            browser = browser and path not in page_wide
            # a data file, a dashboard part, a helper: what names it, as before, but a Python file that reads it reaches
            # the tests of the functions that read it, not every test that imports that file
            pending, visited = [path], {path}
            while pending:
                current = pending.pop()
                named = {o for o in repo.named_by(current) if names_exactly(repo.views.get(o, ''), current)}
                if not named and current == path and not (path.startswith(INERT) or path in INERT_FILES):
                    if why is not None:
                        why['*'] = f'nothing names {path}'
                    return None
                for other in named:
                    if other in visited:
                        continue
                    visited.add(other)
                    if is_test(other):
                        if not (browser and current != path and Path(other).name in impact.js_tests):
                            add(other, f'names {current}')
                    elif other in PAGE:
                        for user in repo.importers.get(other, ()):
                            if is_test(user):
                                add(user, f'imports {other}, which names {current}')
                    elif other.endswith('.py'):
                        lines_in(other, mention_lines(repo.text.get(other, ''), current) or [1], f'{other} reads {current}')
                    elif not other.startswith('dashboard/'):
                        pending.append(other)
    # a check script that walks the repository (i18n_extract: every source file's English; help_check: every article)
    # can fail on any file without running it: the tests that run those scripts go with every change but a test's own
    if any(not is_test(path) for path in changed):
        for script in (p for p in repo.paths if p.startswith('scripts/') and p.endswith('.py')):
            if WALKS.search(repo.text.get(script, '')):
                for test in impact.ran_any(script):
                    add(test, f'runs {script}, which reads every file')
    picked = set(reasons) | set(ALWAYS)
    if fallback:
        # the old way, for what the map can't place; a test it knows is kept only where the map can't speak for it
        old_why = {}
        old = select(sorted(fallback), repo=repo, why=old_why)
        if old is None:
            if why is not None:
                why['*'] = old_why.get('*', 'the import chain runs everything')
            return None
        for name in old:
            reasons.setdefault(name, old_why.get(name, 'import chain'))
        picked = set(reasons) | set(ALWAYS)
    # tests the map doesn't know (new since main's last full run): the import chain for the whole change
    unknown = {Path(t).name for t in tests} - impact.mapped
    if unknown:
        old_why = {}
        old = select(changed, repo=repo, why=old_why)
        for name in (unknown if old is None else set(old) & unknown):
            reasons.setdefault(name, old_why.get(name, 'new test, not in the map yet'))
        picked = set(reasons) | set(ALWAYS)
    picked = {name for name in picked if (ROOT / 'tests' / name).exists()}
    if why is not None:
        why.update(reasons)
    if len(picked) >= ENOUGH * len(tests):
        return None
    return sorted(picked)


def load_impact(path):
    """The map at path (gzipped JSON from scripts/test_impact.py), or None."""
    try:
        with gzip.open(path, 'rt', encoding='utf-8') as source:
            data = json.load(source)
        return Impact(data) if isinstance(data, dict) and data.get('tests') else None
    except (OSError, ValueError, EOFError, KeyError):
        return None


def main(argv):
    show = impact = base = None
    wide = False
    while argv[:1] and argv[0].startswith('--'):
        if argv[0] == '--why':
            show, argv = Path(argv[1]).name, argv[2:]
        elif argv[0] == '--impact':
            impact, argv = load_impact(argv[1]), argv[2:]
        elif argv[0] == '--base':
            base, argv = argv[1], argv[2:]
        elif argv[0] == '--wide':
            wide, argv = True, argv[1:]
        else:
            break
    source = argv[0] if argv else '-'
    lines = (sys.stdin if source == '-' else open(source, encoding='utf-8')).read().splitlines()
    why = {}
    if impact is not None:
        impact.wide = wide
    picked = select(lines, why=why, impact=impact, base=base)
    if show:
        print(f'{show}: ' + (why.get(show) or ('always' if show in ALWAYS else 'not picked')) + (' (all run)' if picked is None else ''))
        return 0
    print('ALL' if picked is None else '\n'.join(picked))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

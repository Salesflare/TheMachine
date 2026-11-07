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

scripts/test_select.py changed.txt          (changed paths, one per line; - reads them from stdin)
scripts/test_select.py --why tests/test_x.py changed.txt   (why that test was picked, or not)"""
from pathlib import Path
import re
import subprocess
import sys

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


def select(changed, repo=None, why=None):
    """The test files (names in tests/) the changed paths need, or None for all of them."""
    changed = [c.strip().removeprefix('./') for c in changed if c.strip()]
    if not changed:
        return None
    if repo is None:
        repo = Repo(tracked(), extra_modules=[c for c in changed if c.endswith('.py')])
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


def main(argv):
    show = None
    if argv[:1] == ['--why']:
        show, argv = Path(argv[1]).name, argv[2:]
    source = argv[0] if argv else '-'
    lines = (sys.stdin if source == '-' else open(source, encoding='utf-8')).read().splitlines()
    why = {}
    picked = select(lines, why=why)
    if show:
        print(f'{show}: ' + (why.get(show) or ('always' if show in ALWAYS else 'not picked')) + (' (all run)' if picked is None else ''))
        return 0
    print('ALL' if picked is None else '\n'.join(picked))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

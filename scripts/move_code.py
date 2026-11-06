#!/usr/bin/env python3
"""Move code from one module to another with its text unchanged (docs/code-map.md).

    python3 scripts/move_code.py assistant.py machine/text.py message_body QUOTED seal_copy
    python3 scripts/move_code.py assistant.py support_app.py:SupportApp App.bug_queue_worker App.REPORT_BUDGET
    python3 scripts/move_code.py --export assistant.py machine/text.py message_body QUOTED

A NAME is a top-level function, class or constant (an assignment to that name) of the source module. Class.NAME is a
method or class attribute of a class there; those go into the class named after the target (target.py:Class), at its
end. Each item goes with its decorators and the comment lines right above it, in the order given, after what the
target already has. The target must exist: its docstring and imports are written by hand (or it's an empty file).

The text of each moved item is the same, line for line; the run checks that, and that both files still parse. Run it
again on a newer source to redo a move (after a rebase) instead of merging by hand. It changes no imports:
tests/test_architecture.py names what the moved code lacks. --export adds the moved top-level names to the source's
imports from the target (one per line, sorted), so code and tests that use them from the source keep working."""
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def defines(node, name):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return node.name == name
    if isinstance(node, ast.Assign):
        return any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
    if isinstance(node, ast.AnnAssign):
        return isinstance(node.target, ast.Name) and node.target.id == name
    return False


def find(body, name, where):
    found = [node for node in body if defines(node, name)]
    if not found:
        raise SystemExit(f'{where} has no {name}')
    if len(found) > 1:
        raise SystemExit(f'{name} is defined {len(found)} times in {where}: move it by hand')
    return found[0]


def find_class(tree, name, where):
    node = find(tree.body, name, where)
    if not isinstance(node, ast.ClassDef):
        raise SystemExit(f'{name} in {where} is not a class')
    return node


def span(lines, node):
    """The 0-based [start, end) lines of an item: its decorators and the comment lines right above it."""
    start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])]) - 1
    while start and lines[start - 1].strip().startswith('#'):
        start -= 1
    return start, node.end_lineno


def locate(lines, tree, item, where):
    """(span, owner class or None) of NAME or Class.NAME."""
    cls, _, name = item.rpartition('.')
    if cls:
        return span(lines, find(find_class(tree, cls, where).body, name, f'{where}:{cls}')), cls
    return span(lines, find(tree.body, item, where)), None


def parse(path, lines):
    try:
        return ast.parse('\n'.join(lines), str(path))
    except SyntaxError as e:
        raise SystemExit(f'{path} does not parse: {e}')


def target_spec(target):
    path, _, cls = target.partition(':')
    return path, cls or None


def move(source, target, items, export=False, root=ROOT):
    target, into = target_spec(target)
    source_path, target_path = root / source, root / target
    if not target_path.is_file():
        raise SystemExit(f'{target} does not exist: write its docstring and imports first (or create it empty)')
    lines = source_path.read_text(encoding='utf-8').split('\n')
    tree = parse(source, lines)
    spans, moved = {}, {}
    for item in items:
        (a, b), cls = locate(lines, tree, item, source)
        if bool(cls) != bool(into):
            raise SystemExit(f'{item}: class members go into a class (target.py:Class), top-level names to a module\'s '
                             'top level')
        spans[item], moved[item] = (a, b), lines[a:b]
    if len({a for a, _ in spans.values()}) < len(spans):
        raise SystemExit('two names share one statement: move them by hand')
    for a, b in sorted(spans.values(), reverse=True):
        # the blank lines on one side of an item go with it, so its neighbors stay as far apart as they were from it
        before = next((n for n in range(a + 1) if n == a or lines[a - 1 - n].strip()), 0)
        after = next((n for n in range(len(lines) - b + 1) if b + n == len(lines) or lines[b + n].strip()), 0)
        del lines[a:b + min(before, after)]
    target_text = target_path.read_text(encoding='utf-8')
    target_lines = target_text.rstrip('\n').split('\n') if target_text.strip() else []
    gap = [''] if into else ['', '']
    if into:
        end = find_class(parse(target, target_lines), into, target).end_lineno
    else:
        end = len(target_lines)
    added = []
    for item in items:
        added += (gap if added or target_lines else []) + moved[item]
    target_lines[end:end] = added
    while lines and not lines[-1].strip():  # a file ends with one newline, also when its last item moved
        lines.pop()
    lines.append('')
    if export and not into:
        lines = add_export(lines, module_name(target), items)
    parse(source, lines)
    parse(target, target_lines)
    source_path.write_text('\n'.join(lines), encoding='utf-8')
    target_path.write_text('\n'.join(target_lines) + '\n', encoding='utf-8')
    check(source, target, into, moved, root)


def module_name(target):
    parts = list(Path(target).with_suffix('').parts)
    if parts[-1] == '__init__':
        parts.pop()
    return '.'.join(parts)


def add_export(lines, module, names):
    """lines with `from module import (\n    name,\n)` holding names, merged into that block when it's there already,
    else added after the module's first run of imports."""
    head = f'from {module} import ('
    if head in lines:
        start = lines.index(head)
        end = lines.index(')', start)
        have = {line.strip().rstrip(',') for line in lines[start + 1:end]}
        lines[start + 1:end] = [f'    {name},' for name in sorted(have | set(names))]
        return lines
    tree = parse('source', lines)
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    after = 0
    for node in tree.body:
        if node not in imports and not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
            break
        after = node.end_lineno
    block = [head] + [f'    {name},' for name in sorted(set(names))] + [')']
    lines[after:after] = block
    return lines


def check(source, target, into, moved, root=ROOT):
    """Each moved item is in the target with the same text and no longer in the source."""
    lines = (root / target).read_text(encoding='utf-8').split('\n')
    tree = parse(target, lines)
    body = find_class(tree, into, target).body if into else tree.body
    for item, text in moved.items():
        name = item.rpartition('.')[2]
        a, b = span(lines, find(body, name, target))
        if lines[a:b] != text:
            raise SystemExit(f'{item}: its text changed in the move')
    source_lines = (root / source).read_text(encoding='utf-8').split('\n')
    source_tree = parse(source, source_lines)
    for item in moved:
        cls, _, name = item.rpartition('.')
        body = find_class(source_tree, cls, source).body if cls else source_tree.body
        if any(defines(node, name) for node in body):
            raise SystemExit(f'{item} is still in {source}')


if __name__ == '__main__':
    args = sys.argv[1:]
    export = '--export' in args
    args = [a for a in args if a != '--export']
    if len(args) < 3:
        raise SystemExit(__doc__)
    move(args[0], args[1], args[2:], export=export)
    print(f'moved {len(args) - 2} items from {args[0]} to {args[1]}')

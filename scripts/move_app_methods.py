#!/usr/bin/env python3
"""Move App methods out of assistant.py into a domain mixin (<domain>_app.py), text unchanged (docs/code-map.md).

    python3 scripts/move_app_methods.py support_app.py SupportApp bug_queue_worker REPORT_BUDGET bug_with_report

Each name is a method of App (with its decorators and the comment lines right above it) or a class attribute of App.
They are cut from assistant.py and added, in the order given, to the end of the class in the target file, which already
exists with that class (its docstring, imports and ACTIONS are written by hand). The text of each moved member is the
same, line for line; the run checks that. Run it again on a newer assistant.py to redo a move (a rebase) instead of
merging by hand. It changes no imports: tests/test_architecture.py names what a moved method needs and lacks."""
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent


def member(cls, name):
    for node in cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node
    raise KeyError(f'App has no {name}')


def span(lines, node):
    """The 0-based [start, end) lines of a class member: its decorators and the comment lines right above it."""
    start = min([node.lineno] + [d.lineno for d in getattr(node, 'decorator_list', [])]) - 1
    while start and lines[start - 1].strip().startswith('#'):
        start -= 1
    return start, node.end_lineno


def find_class(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)


def move(target, cls_name, names, root=ROOT):
    source_path, target_path = root / 'assistant.py', root / target
    lines = source_path.read_text(encoding='utf-8').split('\n')
    app = find_class(ast.parse('\n'.join(lines)), 'App')
    spans = {name: span(lines, member(app, name)) for name in names}
    moved = {name: lines[a:b] for name, (a, b) in spans.items()}
    for a, b in sorted(spans.values(), reverse=True):
        # the blank line after a member goes with it (members are kept one blank line apart)
        if b < len(lines) and not lines[b].strip() and a and not lines[a - 1].strip():
            b += 1
        del lines[a:b]
    text = target_path.read_text(encoding='utf-8')
    target_lines = text.rstrip('\n').split('\n')
    end = find_class(ast.parse(text), cls_name).end_lineno
    added = []
    for name in names:
        added += [''] + moved[name]
    target_lines[end:end] = added
    source_path.write_text('\n'.join(lines), encoding='utf-8')
    target_path.write_text('\n'.join(target_lines) + '\n', encoding='utf-8')
    check(target, cls_name, moved, root)


def check(target, cls_name, moved, root=ROOT):
    """Each moved member is in the target class with the same text and no longer in App."""
    lines = (root / target).read_text(encoding='utf-8').split('\n')
    cls = find_class(ast.parse('\n'.join(lines)), cls_name)
    for name, text in moved.items():
        a, b = span(lines, member(cls, name))
        if lines[a:b] != text:
            raise SystemExit(f'{name}: its text changed in the move')
    app = find_class(ast.parse((root / 'assistant.py').read_text(encoding='utf-8')), 'App')
    for name in moved:
        try:
            member(app, name)
        except KeyError:
            continue
        raise SystemExit(f'{name} is still in App')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    move(sys.argv[1], sys.argv[2], sys.argv[3:])
    print(f'moved {len(sys.argv) - 3} App members to {sys.argv[1]} ({sys.argv[2]})')

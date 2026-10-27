"""Lay out the two files every pull request adds to so parallel pull requests merge cleanly (CONTRIBUTING.md).

    python3 scripts/merge_friendly.py      # rewrite assistant.py's action lists and dashboard.html's long markup lines

assistant.py: each module-level *_ACTIONS set or tuple gets one name per line, spreads (*X) first, then the names, each
sorted, with trailing commas. Comments inside a list move above it. tests/test_owner_boundary.py checks the order.
dashboard.html: a static markup line longer than LONG breaks before each element with an id, inside the previous tag
(`</div` newline `><div id=...>`), so the parsed page is exactly the same. Running it again changes nothing."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LONG = 3000


def actions(src):
    lines = src.splitlines(keepends=True)
    jobs = []
    for node in ast.parse(src).body:
        if not isinstance(node, ast.Assign):
            continue
        t, extra = node.targets[0], ''
        if isinstance(t, ast.Name) and t.id.endswith('_ACTIONS'):
            name, value = t.id, node.value
        elif isinstance(t, ast.Tuple) and isinstance(t.elts[0], ast.Name) and t.elts[0].id.endswith('_ACTIONS') and isinstance(node.value, ast.Tuple):
            name, value = t.elts[0].id, node.value.elts[0]  # UPLOAD_ACTIONS, UPLOAD_REQUEST_BYTES = {...}, n
            extra = ''.join(f'{a.id} = {ast.unparse(v)}\n' for a, v in zip(t.elts[1:], node.value.elts[1:]))
        else:
            continue
        wrap = None
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and len(value.args) == 1:
            wrap, value = value.func.id, value.args[0]  # frozenset({...})
        if not isinstance(value, (ast.Set, ast.Tuple)) or not all(isinstance(e, (ast.Starred, ast.Constant)) for e in value.elts):
            continue
        stars = sorted(ast.unparse(e) for e in value.elts if isinstance(e, ast.Starred))
        names = sorted(e.value for e in value.elts if isinstance(e, ast.Constant))
        open_, close = ('(', ')') if isinstance(value, ast.Tuple) else ('{', '}')
        seg = lines[node.lineno - 1:node.end_lineno]
        inner = [m.group(1) for line in seg[:-1] for m in [re.match(r'\s*(#.*)$', line)] if m]
        after = re.search(r'[)}\d]\s*(#.*)$', seg[-1].rstrip('\n'))
        text = (''.join(c + '\n' for c in inner) + f'{name} = ' + (f'{wrap}({open_}' if wrap else open_) + '\n'
                + ''.join(f'    {s},\n' for s in stars) + ''.join(f'    {s!r},\n' for s in names)
                + close + (')' if wrap else '') + (f'  {after.group(1)}' if after else '') + '\n' + extra)
        jobs.append((node.lineno, node.end_lineno, text))
    for start, end, text in reversed(jobs):
        lines[start - 1:end] = [text]
    return ''.join(lines)


def markup(src):
    lines = src.split('\n')
    start = next(i for i, line in enumerate(lines) if line.startswith('</style>'))
    end = next(i for i, line in enumerate(lines) if line.startswith('<script id="i18n">'))
    for i in range(start + 1, end):
        if len(lines[i]) > LONG:
            lines[i] = re.sub(r'>(?=<[a-z][a-z0-9-]*\s[^<>]*\bid=")', '\n>', lines[i])
    return '\n'.join(lines)


def main():
    for name, fix in (('assistant.py', actions), ('dashboard.html', markup)):
        path = ROOT / name
        before = path.read_text(encoding='utf-8')
        after = fix(before)
        if after != before:
            path.write_text(after, encoding='utf-8')
            print(f'rewrote {name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

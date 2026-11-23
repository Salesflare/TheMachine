"""Every CSS custom property the pages use is defined somewhere on them (docs/design.md, Tokens).

A name nothing defines falls back to its fixed color, which follows no theme, or makes the whole declaration void: that
is how errors were dark red on dark gray. Definitions are read from the source itself, so no list is kept here: a
declaration in a stylesheet, an inline style or a style string, setProperty, and the keys and calls that end up in one
({'--c-bg': bg}, set('--vv-h', ...))."""
import re
import unittest
from pathlib import Path

import dashboard_parts

ROOT = Path(__file__).resolve().parent.parent
MOBILE = ROOT / 'mobile' / 'www'
NAME = r'--[a-zA-Z][\w-]*'
COMMENT = re.compile(r'/\*.*?\*/', re.S)
# `--x:` as a declaration or an object's key, and '--x' as the first argument of a call that takes the value next
DEFINED = (re.compile(rf'''(?<![\w-])({NAME})['"`]?\s*:'''), re.compile(rf'''\(\s*['"`]({NAME})['"`]\s*,'''))
USED = re.compile(rf'var\(\s*({NAME})')
# var(--i-${k}): a name finished when drawn, so one that starts like it has to exist
PREFIX = re.compile(r'var\(\s*(--[\w-]*)\$\{')


def undefined(sources):
    """{file: text} -> 'file:line: --name' for each use of a custom property none of them defines."""
    blank = {f: COMMENT.sub(lambda m: re.sub(r'[^\n]', ' ', m[0]), t) for f, t in sources.items()}
    defined = {m[1] for t in blank.values() for rule in DEFINED for m in rule.finditer(t)}
    out = []
    for f, t in blank.items():
        for m in USED.finditer(t):
            if m[1] not in defined and not t.startswith('${', m.end()):
                out.append(f'{f}:{t.count(chr(10), 0, m.start()) + 1}: {m[1]}')
        for m in PREFIX.finditer(t):
            if not any(n.startswith(m[1]) for n in defined):
                out.append(f'{f}:{t.count(chr(10), 0, m.start()) + 1}: {m[1]}${{...}}')
    return out


class CssTokens(unittest.TestCase):
    def check(self, files):
        found = undefined({str(p.relative_to(ROOT)): p.read_text(encoding='utf-8') for p in files})
        self.assertEqual(found, [], 'Nothing defines these: use the token the page has for that meaning (docs/design.md, '
                                    'dashboard/base-design.css), so it follows the theme.\n' + '\n'.join(found))

    def test_the_dashboard_uses_only_tokens_it_defines(self):
        self.check(dashboard_parts.files(ROOT))

    def test_the_apps_screens_use_only_tokens_they_define(self):
        files = [p for p in sorted(MOBILE.rglob('*')) if p.suffix in ('.css', '.html', '.js')]
        self.assertTrue(files)
        self.check(files)

    def test_what_counts_as_defined(self):
        defined = {'a.css': ':root{--css:1}/* --comment:1 */', 'b.js': 'el.style.setProperty("--set",v);set(\'--helper\',1);'
                   'const v={\'--key\':fg};html`<i style="--inline:${n}">`;', 'c.js': 'const gone=1'}
        use = lambda *names: undefined({**defined, 'use.css': '\n'.join(f'x{{color:var({n},#c00)}}' for n in names)})
        self.assertEqual(use('--css', '--set', '--helper', '--key', '--inline', '--in${k}'), [])
        self.assertEqual(use('--css', '--comment', '--danger', '--no-${k}'),
                         ['use.css:2: --comment', 'use.css:3: --danger', 'use.css:4: --no-${...}'])


if __name__ == '__main__':
    unittest.main()

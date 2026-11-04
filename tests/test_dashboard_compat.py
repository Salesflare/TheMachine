"""The dashboard keeps working in an older browser, such as an Android System WebView before Chrome 92.

Such a WebView ran the page (it parses everything the page writes, ??= included) but threw on every newer built-in or
selector it lacks: `.at` ("w.at is not a function" in initials, closedAt, actMerged) and `:modal` ("not a valid
selector" in toastLift). The page's first script fills in the few newer built-ins it uses (.at, findLast,
findLastIndex, replaceChildren, crypto.randomUUID), and selectors from script use only what such a browser knows, with
:modal and :focus-visible asked behind a try (modalOpen, focusVisible). This test keeps it that way."""
from pathlib import Path
import json
import re
import shutil
import subprocess
import unittest

import dashboard_parts

ROOT = Path(__file__).resolve().parent.parent
PAGE = dashboard_parts.assemble()
SCRIPTS = re.findall(r'<script\b[^>]*>(.*?)</script>', PAGE, re.S)
POLYFILL = SCRIPTS[0]
CODE = '\n'.join(SCRIPTS[1:])

# Built-ins newer than such a browser that the page doesn't fill in: use something older instead (or add it to the
# polyfill, with its own line in test_polyfill_fills_in).
NEWER = {
    'structuredClone': r'\bstructuredClone\s*\(',
    'Object.hasOwn': r'\bObject\.hasOwn\s*\(',
    'replaceAll': r'\.replaceAll\s*\(',
    'toSorted/toReversed/toSpliced': r'\.(?:toSorted|toReversed|toSpliced)\s*\(',
    'Object.groupBy/Map.groupBy': r'\b(?:Object|Map)\.groupBy\s*\(',
    'Promise.withResolvers': r'\bPromise\.withResolvers\b',
    'Array.fromAsync': r'\bArray\.fromAsync\b',
    'AbortSignal.timeout/any': r'\bAbortSignal\.(?:timeout|any)\b',
    'URL.canParse/URL.parse': r'\bURL\.(?:canParse|parse)\s*\(',
    'checkVisibility': r'\.checkVisibility\s*\(',
    'isWellFormed/toWellFormed': r'\.(?:isWellFormed|toWellFormed)\s*\(',
    'Set methods': r'\.(?:union|intersection|symmetricDifference|isSubsetOf|isSupersetOf|isDisjointFrom)\s*\(',
}
# Selector pieces such a browser rejects with a SyntaxError in querySelector, matches or closest.
SELECTOR = re.compile(r':(?:has|is|where|modal|focus-visible|popover-open|user-invalid|user-valid|open|state)\b(?=[(\s,\'"`>+~)\]]|$)')
STRING = re.compile(r"""'(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*"|`(?:[^`\\]|\\.)*`""")
# Where one may still appear: behind a try with a fallback, or where the page already checked the browser has it.
ALLOWED = {
    "const modalOpen=()=>{try{return!!document.querySelector('dialog[open]:modal')}",
    "const focusVisible=el=>{try{return el.matches(':focus-visible')}",
    "if(m.hidePopover&&m.matches(':popover-open'))",
    "if(m.showPopover&&!m.matches(':popover-open'))",
}


class OlderBrowser(unittest.TestCase):
    def test_polyfill_is_the_first_script(self):
        self.assertIn('Older browsers', POLYFILL)
        for name in ("'at'", "'findLast'", "'findLastIndex'", "'replaceChildren'", "'randomUUID'"):
            self.assertIn(name, POLYFILL)

    def test_no_newer_builtins(self):
        found = [f'{name}: …{CODE[max(0, m.start() - 60):m.end() + 20]}…'
                 for name, pattern in NEWER.items() for m in re.finditer(pattern, CODE)]
        self.assertEqual(found, [], 'built-ins an older browser lacks (see this test\'s docstring)')

    def test_no_newer_selectors_from_script(self):
        found = []
        for line in CODE.split('\n'):
            for s in STRING.finditer(line):
                text = s.group()
                if not SELECTOR.search(text) or any(a in line and text in a for a in ALLOWED):
                    continue
                # a string with a selector piece that isn't a selector: data keys such as 'waiting:open'
                if re.fullmatch(r"""['"`][\w-]*:open['"`]""", text):
                    continue
                found.append(f'{text} in …{line[max(0, s.start() - 80):s.end() + 20]}…')
        self.assertEqual(found, [], 'selectors an older browser rejects (see this test\'s docstring)')

    @unittest.skipUnless(shutil.which('node'), 'node not installed')
    def test_polyfill_fills_in(self):
        """The polyfill run where those built-ins are missing gives what the real ones give."""
        script = r"""
const vm=require('node:vm'),src=process.argv[1];
const ctx=vm.createContext({});
vm.runInContext(`delete Array.prototype.at;delete String.prototype.at;delete Object.getPrototypeOf(Int8Array).prototype.at;
delete Array.prototype.findLast;delete Array.prototype.findLastIndex;
class Element{constructor(){this.kids=[]}set textContent(v){this.kids=[]}append(...k){this.kids.push(...k)}}
class DocumentFragment extends Element{}
var window=globalThis,crypto={getRandomValues:a=>{for(let i=0;i<a.length;i++)a[i]=(i*37+11)&255;return a}};`,ctx);
vm.runInContext(src,ctx);
const out=vm.runInContext(`const e=new Element();e.append('x');e.replaceChildren('a','b');
[[1,2,3].at(-1),[1,2,3].at(0),[1,2,3].at(5),'abc'.at(-1),new Uint8Array([4,5]).at(-1),[].at(-1),
[1,2,3,4].findLast(x=>x%2),[1,2,3,4].findLastIndex(x=>x>9),e.kids,crypto.randomUUID()]`,ctx);
process.stdout.write(JSON.stringify(out));
"""
        out = json.loads(subprocess.run([shutil.which('node'), '-e', script, POLYFILL], capture_output=True, text=True,
                                        check=True, timeout=60).stdout)
        self.assertEqual(out[:6], [3, 1, None, 'c', 5, None])
        self.assertEqual(out[6:9], [3, -1, ['a', 'b']])
        self.assertRegex(out[9], r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_polyfill_leaves_real_ones(self):
        """Only filled in where missing, so a current browser keeps its own."""
        self.assertIn("if(o&&!(k in o))", POLYFILL)


if __name__ == '__main__':
    unittest.main()

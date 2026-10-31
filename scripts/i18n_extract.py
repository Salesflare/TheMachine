"""Every user-facing English string, for the string catalog (i18n/): the dashboard, the server text it shows and the plugin.

    python3 scripts/i18n_extract.py            # what's missing from i18n/en.json, everywhere
    python3 scripts/i18n_extract.py --add      # add it to en.json (then translate it in every language)
    python3 scripts/i18n_extract.py --check    # exit 1 when anything is missing (CI)
    python3 scripts/i18n_extract.py --area todos   # one dashboard area only (AREAS)
    python3 scripts/i18n_extract.py --sort     # rewrite every i18n/*.json in its canonical form (run before pushing)
    python3 scripts/i18n_extract.py --merge    # during a git merge: settle the catalogs' conflicts key by key

The dashboard translates by source text (the i18n script in dashboard.html): an element's text, placeholder, aria-label or
title that equals a catalog key reads in the owner's language. So a string only needs to be a key in en.json (and
translated in every language); nothing in the markup changes. What is read:

- dashboard.html: all of its markup and every script in it (AREAS only groups them for a report);
- server text the dashboard shows: every error the Python modules raise with a message (it reaches the dashboard as
  the request's error), the strings in SERVER_TEXT's functions (lines the dashboard shows as they come) and every
  i18n.t() key;
- the OpenClaw plugin (openclaw-plugin/*.ts): every t() key and the button labels it translates.

tests/test_i18n.py fails when any of it is neither in en.json nor in i18n/not-ui.json (strings the extractor finds that
nobody reads: ids, codes, search keywords, examples, text only a model reads).

The catalogs are kept sorted by key, one key per line (canonical()), so pull requests that add different strings touch
different lines and merge without conflicts; add a key anywhere and --sort puts it in its place. tests/test_i18n.py
fails on a catalog that isn't in that form."""
from __future__ import annotations

import html.parser
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import dashboard_parts  # noqa: E402  (the dashboard's source, assembled from its parts)

CATALOG = ROOT / 'i18n'

# area: (ids of static elements, ranges of top-level functions that build it: (first, last) by name, each range taking
# every top-level statement from the first function to the end of the last)
AREAS = {
    'shell': (['topbar', 'app-side', 'browser-pane', 'limit-banner', 'needs-you', 'page-head', 'copyright', 'help-link'],
              [('renderLimitBanner', 'limitNote'), ('renderNeedsYou', 'needsYouPlace'), ('render', 'render'),
               ('showTab', 'drawerClose'), ('palScore', 'kbHints')]),
    'todos': (['inbox', 'snooze-dialog', 'send-dialog', 'result-dialog'],
              [('cardBody', 'paintPeek'), ('learnedShow', 'promisesList'), ('withoutListedFiles', 'openSnoozeLink'),
               ('chatMarkdown', 'chatGo'), ('renderMonth', 'toast')]),
    'settings': (['settings'],
                 [('renderModelPanel', 'skillUpdateOpen'), ('settingsSync', 'sigTool'), ('skillMeta', 'skillShow'),
                  ('installKind', 'renderNotify')]),
    'graph': (['people', 'project-dialog', 'record-dialog', 'crm-dialog', 'board-dialog'],
              [('graphCountsSet', 'graphHashSync'), ('helpLink', 'saveDecision'), ('graphStash', 'openConversation')]),
    'calendar': (['calendar', 'cal-dialog', 'cal-view'], [('calFetchWeek', 'calSave')]),
    'connections': (['health', 'signin-dialog'], [('connectorHealth', 'connectorCard'), ('signinMode', 'browserShow')]),
    'help': ([], [('helpMarkup', 'supportAccessRender')]),
    'events': (['events', 'email-dialog'], [('search', 'openEvent')]),
    'new': ([], [('ncDue', 'newMenu')]),
}
MOVED = ['shell', 'todos', 'settings', 'graph', 'calendar', 'connections', 'help', 'events', 'new']

ATTRS = ('placeholder', 'aria-label', 'title', 'alt', 'label')
SKIP_TAGS = {'script', 'style', 'svg', 'code', 'pre', 'textarea'}


def looks_ui(text):
    """English someone reads: a letter, no code."""
    text = text.strip()
    if len(text) < 2 or not re.search(r'[A-Za-z]{2}', text):
        return False
    if re.search(r'[<>{}=\\]|;(?!\s)|\$\{|^[.#\[]|^https?:|^[a-z0-9_-]+$|^[a-z]+[A-Z]\w*$|^api/|^[\w-]+\.(?:png|webp|js|json|md)$', text):
        return False
    return True


class _Static(html.parser.HTMLParser):
    def __init__(self, ids):
        super().__init__(convert_charrefs=True)
        self.ids, self.stack, self.found = set(ids), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        inside = (a.get('id') in self.ids) or (self.stack and self.stack[-1][1])
        skip = tag in SKIP_TAGS or (self.stack and self.stack[-1][2]) or a.get('translate') == 'no'
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'path', 'circle', 'rect', 'wbr'):
            self.stack.append((tag, bool(inside), bool(skip)))
        if inside and not skip:
            for name in ATTRS:
                if a.get(name) and looks_ui(a[name]):
                    self.found.append(a[name].strip())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'path', 'circle', 'rect', 'wbr') and self.stack:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][1] and not self.stack[-1][2] and looks_ui(data):
            self.found.append(' '.join(data.split()))


def markup(source):
    """The static markup: between the stylesheet and the first big script."""
    start = source.index('</style>', source.index('<style>')) + len('</style>')
    end = source.index('\n<script>\n', start)  # inline <script> tags in the markup are skipped by the parser
    return source[start:end]


def functions(source, ranges):
    """The source of each range of top-level functions: from the first one's line to the next top-level statement
    after the last one."""
    lines, out = source.split('\n'), []
    starts = [i for i, line in enumerate(lines) if re.match(r'(?:async )?function |const |let |\$\(|document\.|window\.|// ', line)]
    where = {}
    for i, line in enumerate(lines):
        # a function, or a const holding an arrow function (const openEvent=(ev,title)=>...)
        found = re.match(r'(?:async )?function ([A-Za-z0-9_]+)|const ([A-Za-z0-9_]+)=(?:async )?(?:\([^)]*\)|[A-Za-z0-9_]+)=>', line)
        if found:
            where.setdefault(found.group(1) or found.group(2), i)
    for first, last in ranges:
        if first not in where or last not in where:
            raise KeyError(f'dashboard.html has no function {first if first not in where else last} (i18n_extract AREAS)')
        end = next((j for j in starts if j > where[last]), len(lines))
        out.append('\n'.join(lines[where[first]:end]))
    return out


_LITERAL = re.compile(r"'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\"|`((?:[^`\\]|\\.)*)`")


def _texts(literal):
    """UI text in one JS string: whole, or the text between its tags; ${...} parts become {0}, {1}."""
    holes = []

    def hole(m):
        holes.append(m.group(0))
        return '{' + str(len(holes) - 1) + '}'
    plain = re.sub(r'\$\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}', hole, literal)
    plain = plain.replace("\\'", "'").replace('\\"', '"').replace('\\n', ' ')
    parts = re.split(r'<[^>]*>', plain) if '<' in plain else [plain]
    out = []
    # the text attributes of the markup a string builds (placeholder="...", aria-label="..."): read as written
    for tag in re.findall(r'<[a-z][^>]*>', plain):
        for value in re.findall(r'\b(?:placeholder|aria-label|title|alt)="([^"]*)"', tag):
            value = re.sub(r'\{\d+\}', '{}', ' '.join(value.split()))
            words = value.replace('{}', '')
            if '{}' in value and not re.search(r'\w\{\}', value) and re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}|[A-Z][a-z]+', words) and not re.search(r'[=;()]', words):
                out.append(value)  # aria-label="Owner of ${name}"
            elif '{' not in value and looks_ui(value) and (' ' in value or value[0].isupper()):
                out.append(value)
    for part in parts:
        part = ' '.join(part.split())
        part = re.sub(r'&nbsp;', ' ', part).strip()
        if '{' in part:
            # a run with holes: keep it when it reads as a sentence around them
            words = re.sub(r'\{\d*\}', '', part)
            if not (len(re.findall(r'[A-Za-z]{2,}', words)) >= 2 or re.search(r'[A-Z][a-z]+', words)
                    or re.fullmatch(r'\s*[a-z]{3,}(?:/[a-z]{3,})?\s*', words) and re.fullmatch(r'\{\d*\} \w+|\w+ \{\d*\}', part)) \
                    or re.search(r'[=;]|\(|\)|=>', words):  # a sentence around them, or "{} connected" 
                continue
            part = re.sub(r'\{\d+\}', '{}', part)
            out.append(part)
        elif looks_ui(part) and (' ' in part or part[0].isupper() or re.fullmatch(r'\([a-z]+\)', part)):
            out.append(part)
    return out


def _uncomment(code):
    """Line comments out (they hold apostrophes that read as strings); a // inside a string (a URL) stays."""
    out = []
    for line in code.split('\n'):
        out.append(re.sub(r'(^|[;{}),\s])//(?:\s|$).*$', r'\1', line) if not line.lstrip().startswith('//') else '')
    return '\n'.join(out)


def translatable(text):
    """A string the dashboard shows whole: starts with a capital (or a placeholder, digit or symbol), no code bits, and no
    placeholder glued to a word (to-do{} is a plural made in code: those get a plural entry instead)."""
    return not re.search(r'\$\{|:\'|\w\{\}|\{\}\w|^[a-z]|prefers-color-scheme|^\+ ', text)


def _regex_starts(code, i):
    """A / that starts a regular expression literal (/'/ would otherwise read as a string): after an operator, an
    opening bracket, a comma or a keyword like return, not after a value."""
    j = i - 1
    while j >= 0 and code[j] in ' \t':
        j -= 1
    if j < 0 or code[j] in '(,=:[!&|?{};+-*%<>~^\n':
        return code[i + 1:i + 2] not in ('/', '*')
    word = re.search(r'([A-Za-z_$]+)$', code[max(0, j - 10):j + 1])
    return bool(word and word.group(1) in ('return', 'typeof', 'case', 'in', 'of', 'void', 'delete'))


def _regex_end(code, i):
    """The index after a regular expression literal starting at i (its flags included)."""
    j, n, klass = i + 1, len(code), False
    while j < n and code[j] != '\n':
        c = code[j]
        if c == '\\':
            j += 2
            continue
        if c == '[':
            klass = True
        elif c == ']':
            klass = False
        elif c == '/' and not klass:
            j += 1
            while j < n and code[j].isalpha():
                j += 1
            return j
        j += 1
    return i + 1  # not a regex after all: a lone /


def literals(code):
    """(text, start) for every string in some JS: '...', "..." and `...`, also the ones inside a template's ${...} (a
    label picked in a ternary inside a row's markup). A template's own text keeps its ${...} parts."""
    out, n = [], len(code)

    def expr(i, close):
        """Scan code from i to the } (or the end) that closes it; returns the index after it."""
        depth = 0
        while i < n:
            c = code[i]
            if c in '\'"':
                j = i + 1
                while j < n and code[j] != c and code[j] != '\n':
                    j += 2 if code[j] == '\\' else 1
                out.append((code[i + 1:j], i))
                i = j + 1
            elif c == '`':
                i = template(i)
            elif c == '/' and code[i + 1:i + 2] == '*':
                end = code.find('*/', i + 2)
                i = n if end < 0 else end + 2
            elif c == '/' and _regex_starts(code, i):
                i = _regex_end(code, i)
            elif c == '{':
                depth += 1
                i += 1
            elif c == '}':
                if depth == 0 and close:
                    return i + 1
                depth -= 1
                i += 1
            else:
                i += 1
        return i

    def template(i):
        start, j, text = i, i + 1, []
        while j < n and code[j] != '`':
            if code[j] == '\\':
                text.append(code[j:j + 2])
                j += 2
            elif code.startswith('${', j):
                end = expr(j + 2, True)
                text.append(code[j:end])
                j = end
            else:
                text.append(code[j])
                j += 1
        out.append((''.join(text), start))
        return j + 1

    expr(0, False)
    return sorted(out, key=lambda x: x[1])


def script_strings(code):
    found, code = [], _uncomment(code)
    for literal, start in literals(code):
        before = code[max(0, start - 40):start]
        # selectors, keys and events: $('#x'), .querySelector('x'), {key:'x'}, addEventListener('click'
        if re.search(r"(?:\$|querySelector(?:All)?|closest|matches|getElementById|addEventListener|getItem|setItem|"
                     r"removeItem|classList\.\w+|getAttribute|setAttribute|dataset\.?\w*|request|fetch|startsWith|"
                     r"endsWith|includes|split|replace|join|cachedGet|createElement|toggle|location\.\w+)\(\s*$", before):
            continue
        if re.search(r"\b(?:t|tr)\(\[\s*$", before):  # t(['{} guest','{} guests'],n): the catalog keys the plural by its other form
            continue
        if re.search(r"\b(?:t|tr)\(\s*$", before) and "${" not in literal and re.search(r'[A-Za-z]{2}', literal):
            found.append(literal.replace("\\'", "'"))  # t('{} new/changed', n): a key as written, whatever its words
            continue
        if re.search(r"(?:===?|!==?)\s*$", before) or re.search(r"\b(?:action|kind|tab|service|mode|state|status|role|type|keywords|"
                                                              r"id|cls|class|value|name|key|href|src):\s*$", before):
            continue
        found.extend(_texts(literal))
    return found


def element(html_text, element_id):
    """The markup of the element with this id, up to its own closing tag (nested ones of the same tag counted), so a
    stray unclosed tag earlier on can't end it early."""
    found = re.search(r'<([a-z][a-z0-9-]*)\b[^>]*\bid="' + re.escape(element_id) + '"', html_text)
    if not found:
        return ''
    tag, depth = found.group(1), 0
    for m in re.compile(r'<(/?)' + tag + r'\b[^>]*>').finditer(html_text, found.start()):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return html_text[found.start():m.end()]
    return html_text[found.start():]


def area_strings(area, source=None):
    source = source if source is not None else dashboard_parts.assemble(ROOT)
    ids, names = AREAS[area]
    static, out = markup(source), []
    for element_id in ids:
        parser = _Static([element_id])
        parser.feed(element(static, element_id))
        out.extend(parser.found)
    for code in functions(source, names):
        out.extend(script_strings(code))
    seen, unique = set(), []
    for text in out:
        if text not in seen:
            seen.add(text)
            unique.append(text)
    return unique


def canonical(data):
    """A catalog's text: keys sorted (a list, as not-ui.json, sorted too), indent 1, UTF-8 as is, a final newline."""
    if isinstance(data, list):
        data = sorted(data)
    return json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + '\n'


def write_catalog(path, data):
    path.write_text(canonical(data), encoding='utf-8')


def unsorted():
    """The catalogs (i18n/*.json) whose text isn't canonical(): what --sort rewrites."""
    out = []
    for path in sorted(CATALOG.glob('*.json')):
        text = path.read_text(encoding='utf-8')
        if text != canonical(json.loads(text)):
            out.append(path)
    return out


def sort_all():
    for path in unsorted():
        write_catalog(path, json.loads(path.read_text(encoding='utf-8')))


def _git(*args):
    import subprocess
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True, check=False).stdout


def merge_conflicts():
    """In a git merge: each conflicted catalog becomes the other side's plus what this side changed since the merge
    base (added, changed or removed keys), in canonical form. For a branch made before the catalogs were sorted."""
    base = _git('merge-base', 'HEAD', 'MERGE_HEAD').strip()
    done = []
    for name in _git('diff', '--name-only', '--diff-filter=U', '--', 'i18n/').split():
        if not name.endswith('.json'):
            continue
        b, ours, theirs = ((json.loads(_git('show', f'{rev}:{name}') or 'null')) for rev in (base, 'HEAD', 'MERGE_HEAD'))
        if isinstance(theirs, list) or isinstance(ours, list):
            b, ours, theirs = set(b or []), set(ours or []), set(theirs or [])
            out = sorted((theirs | (ours - b)) - (b - ours))
        else:
            b, ours, out = b or {}, ours or {}, dict(theirs or {})
            out.update({k: v for k, v in ours.items() if b.get(k) != v})
            for k in set(b) - set(ours):
                out.pop(k, None)
        write_catalog(ROOT / name, out)
        _git('add', name)
        done.append(name)
    return done


def catalog(lang):
    path = CATALOG / f'{lang}.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def not_ui():
    path = CATALOG / 'not-ui.json'
    return set(json.loads(path.read_text(encoding='utf-8'))) if path.exists() else set()


def dashboard_strings(source=None):
    """Every string in dashboard.html: the whole markup after the stylesheet (outside its scripts) and every script."""
    source = source if source is not None else dashboard_parts.assemble(ROOT)
    body = source[source.index('</style>', source.index('<style>')) + len('</style>'):]
    scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', body, re.S)
    parser = _Whole()
    parser.feed(re.sub(r'<script\b[^>]*>.*?</script>', '', body, flags=re.S))
    out = list(parser.found)
    for code in scripts:
        out.extend(script_strings(code))
    return _unique(s for s in out if not _code_bit(s))


class _Whole(_Static):
    """The markup, all of it read."""

    def __init__(self):
        super().__init__([])

    def handle_starttag(self, tag, attrs):
        if not self.stack:  # every top-level element counts as inside
            self.ids = {dict(attrs).get('id') or '-'}
            attrs = [*[a for a in attrs if a[0] != 'id'], ('id', self.ids.copy().pop())]
        super().handle_starttag(tag, attrs)

    def handle_data(self, data):
        if not self.stack and looks_ui(data):
            self.found.append(' '.join(data.split()))
        else:
            super().handle_data(data)


def _code_bit(text):
    """A piece of a template the literal scanner cut out of its code (`:'') +(x?`), a tag name or a class list."""
    return bool(re.search(r"`|'\)|\+\s*\(|\?'|:'|\)\s*\+|&&|\|\||\$\{|^\W*\d+\W*$", text)
                or re.fullmatch(r'[A-Z]{2,}', text) or re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)+(?: [a-z][a-z0-9-]*)*', text))


def _unique(items):
    seen, out = set(), []
    for text in items:
        if text not in seen:
            seen.add(text)
            out.append(text)
    return out


# Server text the dashboard shows. Every module's raised messages are read (they come back as a request's error); these
# modules only talk to a terminal, a model or another Machine, never to the dashboard.
NOT_DASHBOARD = {'cli.py', 'installer.py', 'network_crypto.py', 'message_seal.py', 'message_keyring.py', 'openclaw_pin.py',
                 'wacli_release.py', 'service.py', 'portable.py', 'rollout_health.py', 'i18n.py', 'locale_prefs.py',
                 'dashboard_parts.py', 'ai_reach.py'}  # ai_reach.py: errors go to the log; Settings shows its state
# Functions whose strings are lines the dashboard shows as the server wrote them (a reason, a sync line, a hint).
SERVER_TEXT = {
    'own_addresses.py': ['suggest_reason', 'classify', 'SENT_ONLY', 'NAMED_ONLY', 'LABELS'],
    'onboarding.py': ['WHAT', 'LABELS'],
    'shared_graph.py': ['why'],          # why a thread is shared or not, under Sharing
    'graph.py': ['likely_same'],         # why two people look like one
    'crm.py': ['org_doubles'],           # why two organizations look like one
    'fleet.py': ['KIND_LABEL'],          # what a Fleet asks about, in a sentence and (capitalized) as a row's name
    'family.py': ['LABELS'],
    'assistant.py': ['TODO_SOURCE', 'TODO_SOURCE_OTHER'],  # Feedback's rows: where the to-dos came from
}
# Constants the dashboard also shows capitalized (cap()) as a label
CAPITALIZED = {'fleet.py': ['KIND_LABEL'], 'family.py': ['LABELS']}
# Every connector's SETUP (its label, what it brings in, the setup form's text; not its account record) and KINDS (a
# card's source line names its kind)
CONNECTOR_TEXT = ['SETUP', 'KINDS']


def _py_text(node):
    """A string literal, an f-string ({} for each hole) or a + of them; None for anything else."""
    import ast
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return ''.join(v.value if isinstance(v, ast.Constant) else '{}' for v in node.values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _py_text(node.left), _py_text(node.right)
        if left is None and right is None:
            return None
        return (left if left is not None else '{}') + (right if right is not None else '{}')
    return None


def _english(text):
    """A word or a phrase someone reads (tests/test_i18n_server.py english()), holes counted as words."""
    s = text.replace('{}', 'x').strip()
    if not any(c.isalpha() for c in s) or s.startswith(('http', '/', '#', '(?', 'SELECT', 'UPDATE', 'INSERT', 'assistant:')):
        return False
    if '_' in s or '\\' in s or '%' in s or '$' in s:
        return False
    words = [w for w in s.split() if w.isalpha() and len(w) > 1]
    return len(words) >= 2 or (len(words) == 1 and s[0].isupper() and s[1:2].islower())


def _const_strings(node):
    """The string values in a constant (dict values, list and tuple items), leaving out an 'account' record and a
    connector's 'no_oauth' reason (for reviewers, never shown)."""
    import ast
    if isinstance(node, ast.Dict):
        return [s for k, v in zip(node.keys, node.values)
                if not (isinstance(k, ast.Constant) and k.value in ('account', 'no_oauth')) for s in _const_strings(v)]
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return [s for v in node.elts for s in _const_strings(v)]
    text = _py_text(node)
    return [text] if text else []


def _is_t(node):
    import ast
    return isinstance(node, ast.Call) and (isinstance(node.func, ast.Name) and node.func.id == 't'
                                           or isinstance(node.func, ast.Attribute) and node.func.attr == 't')


# Keys of the dicts a server answer carries whose string values the dashboard shows as they are
SHOWN_KEYS = {'label', 'text', 'title', 'hint', 'error', 'message', 'summary'}


def server_strings(root=ROOT):
    """{module: [strings]}: raised messages, SERVER_TEXT's strings and t() keys of the Python modules."""
    import ast
    out = {}
    for path in sorted([*root.glob('*.py'), *root.glob('connectors/*.py')]):
        rel = path.relative_to(root).as_posix()
        if rel in NOT_DASHBOARD or path.name.startswith('test'):
            continue
        tree, found = ast.parse(path.read_text(encoding='utf-8')), []
        names = set(SERVER_TEXT.get(rel, [])) | (set(CONNECTOR_TEXT) if rel.startswith('connectors/') else set())
        for node in tree.body:  # module constants the dashboard shows as they come: their string values
            values = []
            if isinstance(node, ast.Assign) and any(isinstance(x, ast.Name) and x.id in names for x in node.targets):
                values = _const_strings(node.value)
            elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute)
                  and node.value.func.attr == 'update' and getattr(node.value.func.value, 'id', None) in names):
                values = [x for a in node.value.args for x in _const_strings(a)] + [x for k in node.value.keywords for x in _const_strings(k.value)]
            caps = set(CAPITALIZED.get(rel, []))
            name = (getattr(node.value.func.value, 'id', None) if values and isinstance(node, ast.Expr)
                    else next((x.id for x in getattr(node, 'targets', []) if isinstance(x, ast.Name)), None))
            for v in values:
                v = v.strip()
                if not re.search(r'[A-Za-z]{2}', v) or re.fullmatch(r'[a-z_]+', v) and '_' in v:
                    continue
                if _english(v) or ' ' in v or name in caps:
                    found.append(v)
                    if name in caps:
                        found.append(v[:1].upper() + v[1:])
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):  # {'label': 'View in browser'}, {'error': 'Not available'}: text the dashboard shows
                for k, v in zip(node.keys, node.values):
                    if (isinstance(k, ast.Constant) and k.value in SHOWN_KEYS and isinstance(v, ast.Constant) and isinstance(v.value, str)
                            and v.value[:1].isupper() and re.search(r'[a-z]{2}', v.value)):
                        found.append(v.value.strip())
            if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args:
                text = _py_text(node.exc.args[0])
                if text and _english(text):
                    found.append(text.strip())
            elif _is_t(node) and node.args:
                # t(lead + ': {}'): a key made in code is each lead's own key, not this frame
                text = None if isinstance(node.args[0], ast.BinOp) and None in (_py_text(node.args[0].left), _py_text(node.args[0].right)) else _py_text(node.args[0])
                if text:
                    found.append(text)
            elif isinstance(node, ast.FunctionDef) and node.name in names:
                inner = {id(v) for j in ast.walk(node) if isinstance(j, ast.JoinedStr) for v in j.values}  # an f-string's pieces
                for n in ast.walk(node):
                    if id(n) in inner:
                        continue
                    text = _py_text(n) if isinstance(n, (ast.Constant, ast.JoinedStr)) else None
                    if text and _english(text) and not (isinstance(n, ast.Constant) and n is getattr(node.body[0], 'value', None)):
                        found.append(text.strip())
        if found:
            out[rel] = _unique(found)
    return out


PLUGIN = ROOT / 'openclaw-plugin'


def plugin_strings(folder=PLUGIN):
    """{file: [strings]}: the plugin's t() keys and the labels its buttons translate ([['Snooze', 'snooze'], ...])."""
    out = {}
    for path in sorted(folder.glob('*.ts')):
        code, found = _uncomment(path.read_text(encoding='utf-8')), []
        for m in re.finditer(r"\bt\(\s*'((?:[^'\\\n]|\\.)*)'", code):
            found.append(m.group(1).replace("\\'", "'"))
        for m in re.finditer(r"\[\s*'([A-Z][^'\n]*)'\s*,\s*'[a-z_]+'\s*\]", code):
            found.append(m.group(1))
        for m in re.finditer(r"(?:\?|:)\s*'([A-Z][a-z][^'\n]*)'(?=\s*[:;),])", code):  # a label picked in a ternary
            if _english(m.group(1)):
                found.append(m.group(1))
        if found:
            out[path.name] = _unique(found)
    return out


VIEWER = ROOT / 'deploy' / 'browser' / 'machine-view.js'


def viewer_strings(path=VIEWER):
    """[strings]: the browser viewer's t() keys, and English it sets straight on the page (textContent, a title or
    aria-label, text between tags in its HTML), which should go through t() too."""
    code, found = _uncomment(path.read_text(encoding='utf-8')), []
    for m in re.finditer(r"\bt\(\s*(?:'((?:[^'\\\n]|\\.)*)'|\"((?:[^\"\\\n]|\\.)*)\")", code):
        found.append((m.group(1) if m.group(1) is not None else m.group(2)).replace("\\'", "'"))
    for m in re.finditer(r"(?:textContent|title|innerText)\s*=\s*['\"`]([^'\"`\n]+)['\"`]", code):
        if _english(m.group(1)):
            found.append(m.group(1))
    for m in re.finditer(r"(?:aria-label|title)=\"([^\"\n]+)\"|>([A-Za-z][^<>'\n]*)<", code):
        text = m.group(1) or m.group(2)
        if _english(text):
            found.append(text)
    return _unique(found)


# Words glued to a value with + that nobody reads as a sentence of their own: units, class names, a window title's
# prefix, search keywords, a file name, a channel name before its localized date
GLUED_OK = {' KB', ' MB', ' B', 'Pasted image.', 'prep t-', 'The Machine · ', ' (a closeness)', 'Telegram ',
            'projects board kanban '}


def glued(source=None):
    """[(literal, context)]: dashboard words glued to a value with + ("'Hand to '+name") without a catalog entry that
    frames them ("Hand to {}"). The page only translates whole lines, so such a line reads English in every language:
    use t('Hand to {}', name) instead."""
    source = source if source is not None else dashboard_parts.assemble(ROOT)
    body = source[source.index('</style>', source.index('<style>')) + len('</style>'):]
    en = catalog('en')
    keys = list(en) + [f for v in en.values() if isinstance(v, dict) for f in v.values()]
    out = []
    for code in re.findall(r'<script\b[^>]*>(.*?)</script>', body, re.S):
        code = _uncomment(code)
        for lit, start in literals(code):
            if code[start] == '`':
                continue
            end = start + len(lit) + 2
            before, after = code[max(0, start - 3):start], code[end:end + 3]
            if not (re.search(r'\+\s*$', before) or re.match(r'\s*\+', after)):
                continue
            if lit in GLUED_OK or ' ' not in lit or '/' in lit or not re.search(r'[A-Za-z]{2,}', lit) or not looks_ui(lit):
                continue
            if re.search(r'(keywords|id|key):\s*$', code[max(0, start - 12):start]):
                continue
            word = re.escape(lit.strip())
            left = r'\{\d*\}\s*' if lit[:1] == ' ' else r'(^|\{\d*\}\s*)'
            right = r'\s*\{\d*\}' if lit[-1:] == ' ' else r'(\s*\{\d*\}|$)'
            if not any(re.search(left + word + right, k) for k in keys):
                out.append((lit, code[max(0, start - 40):end + 40].replace('\n', ' ')))
    return out


def missing(areas=None):
    """{where: [strings missing from en.json]}: the dashboard, each server module, each plugin file. With areas, only
    those dashboard areas."""
    en, skip, out = catalog('en'), not_ui(), {}
    # a key, or a form of a plural entry (the English singular in t(['{} promise', '{} promises'], n))
    keys = set(en) | {form for value in en.values() if isinstance(value, dict) for form in value.values()}
    source = dashboard_parts.assemble(ROOT)
    if areas:
        groups = {area: area_strings(area, source) for area in areas}
    else:
        groups = {'dashboard': dashboard_strings(source)}
        groups.update({'server:' + k: v for k, v in server_strings().items()})
        groups.update({'plugin:' + k: v for k, v in plugin_strings().items()})
        groups['viewer'] = viewer_strings()
    for where, strings in groups.items():
        gone = [s for s in strings if s not in keys and s not in skip]
        if gone:
            out[where] = gone
    return out


def main(argv):
    if '--merge' in argv:
        print('\n'.join(f'merged {n}' for n in merge_conflicts()) or 'no catalog conflicts')
        return 0
    if '--sort' in argv:
        fixed = unsorted()
        sort_all()
        print('\n'.join(f'sorted {p.relative_to(ROOT)}' for p in fixed) or 'every catalog is sorted')
        return 0
    areas = [argv[argv.index('--area') + 1]] if '--area' in argv else None
    gone = missing(areas)
    if '--add' in argv:
        en = catalog('en')
        for strings in gone.values():
            for s in strings:
                en.setdefault(s, s)
        write_catalog(CATALOG / 'en.json', en)
    print(json.dumps(gone, ensure_ascii=False, indent=1))
    return 1 if '--check' in argv and gone else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

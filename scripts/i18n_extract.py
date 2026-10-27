"""The dashboard's user-facing English, per area, for the string catalog (i18n/).

    python3 scripts/i18n_extract.py            # what's missing from i18n/en.json in the moved areas
    python3 scripts/i18n_extract.py --add      # add it to en.json (then translate it in every language)
    python3 scripts/i18n_extract.py --all      # every area, moved or not

The dashboard translates by source text (the i18n script in dashboard.html): an element's text, placeholder, aria-label or
title that equals a catalog key reads in the owner's language. So moving an area into the catalog means its strings
are keys in en.json, nothing in the markup changes. AREAS says where each area lives: element ids in the static markup
and the names of the functions that build it. tests/test_i18n.py fails when a moved area (MOVED) has English that is
neither in en.json nor in i18n/not-ui.json (strings the extractor finds that nobody reads: ids, codes, examples)."""
from __future__ import annotations

import html.parser
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASHBOARD = ROOT / 'dashboard.html'
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
    if re.search(r'[<>{}=;\\]|\$\{|^[.#\[]|^https?:|^[a-z0-9_-]+$|^[a-z]+[A-Z]\w*$|^api/|^[\w-]+\.(?:png|webp|js|json|md)$', text):
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
        found = re.match(r'(?:async )?function ([A-Za-z0-9_]+)', line)
        if found:
            where.setdefault(found.group(1), i)
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
    for part in parts:
        part = ' '.join(part.split())
        part = re.sub(r'&nbsp;', ' ', part).strip()
        if '{' in part:
            # a run with holes: keep it when it reads as a sentence around them
            words = re.sub(r'\{\d+\}', '', part)
            if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}|[A-Z][a-z]+', words) or re.search(r'[=;]|\(|\)|=>', words):
                continue
            part = re.sub(r'\{\d+\}', '{}', part)
            out.append(part)
        elif looks_ui(part) and (' ' in part or part[0].isupper()):
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
        if re.search(r"(?:===?|!==?)\s*$", before) or re.search(r"\b(?:action|kind|tab|service|mode|state|status|role|type|"
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
    source = source if source is not None else DASHBOARD.read_text(encoding='utf-8')
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


def catalog(lang):
    path = CATALOG / f'{lang}.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def not_ui():
    path = CATALOG / 'not-ui.json'
    return set(json.loads(path.read_text(encoding='utf-8'))) if path.exists() else set()


def missing(areas=MOVED):
    en, skip, out = catalog('en'), not_ui(), {}
    # a key, or a form of a plural entry (the English singular in t(['{} promise', '{} promises'], n))
    keys = set(en) | {form for value in en.values() if isinstance(value, dict) for form in value.values()}
    source = DASHBOARD.read_text(encoding='utf-8')
    for area in areas:
        gone = [s for s in area_strings(area, source) if s not in keys and s not in skip]
        if gone:
            out[area] = gone
    return out


def main(argv):
    areas = list(AREAS) if '--all' in argv else MOVED
    gone = missing(areas)
    if '--add' in argv:
        en = catalog('en')
        for strings in gone.values():
            for s in strings:
                en.setdefault(s, s)
        (CATALOG / 'en.json').write_text(json.dumps(en, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(gone, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

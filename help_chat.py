"""Help in the dashboard: questions about how The Machine works, answered from the help articles (docs/help) first
and the app's own code second, with links to what the answer used.

Cheap by design: only the few sections that match the question go in (never every article), with a short prompt,
as a one-shot turn on the Machine's own model through OpenClaw (`openclaw infer model run --gateway`: its own
session, no tools, no workspace files), so it can answer and change nothing. Nothing about the owner goes in: no
messages, people or settings, only the question, the last few turns of this help chat and the public docs and code."""
from __future__ import annotations

import json
import math
import re
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HELP = ROOT / 'docs' / 'help'
SITE = 'https://themachine.computer/help/'
CODE = 'https://github.com/Salesflare/TheMachine/blob/main/'
SECTIONS, SNIPPETS = 4, 2          # what goes in: the best help sections, then a couple of code docstrings
SECTION_CHARS, SNIPPET_CHARS = 1400, 700
QUESTION_CHARS, HISTORY_TURNS, TURN_CHARS = 600, 4, 600
PER_HOUR = 30
TIMEOUT = 120
CODE_FILES = ('*.py', 'connectors/*.py')  # the app's own modules; never config, data or tests
STOP = set('a an and are as at be by can do does for from has have how i if in is it its me my of on or so that the this '
           'to was what when where which who why will with you your'.split())
WORD = re.compile(r'[a-z0-9]+')
_cache = {}
_lock = threading.Lock()
_asked = []


class Unavailable(Exception):
    """No answer now: no model, too many questions, or the model run failed. Its text is for the owner."""


def words(text):
    return [w[:-1] if len(w) > 4 and w.endswith('s') else w for w in WORD.findall(str(text).lower()) if w not in STOP]


def heading_id(text):
    """The id the site gives a heading (scripts/help_check.py, cloud/help.py's anchor())."""
    return re.sub(r'[^a-z0-9]+', '-', re.sub(r'[`*]', '', text).lower()).strip('-')


def _front(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}, text
    fields = dict((k.strip(), v.strip()) for k, _, v in (line.partition(':') for line in m[1].splitlines()))
    return fields, text[m.end():]


def help_sections(folder=HELP):
    """Every help article split at its headings: {slug, anchor, title, heading, text}."""
    out = []
    for path in sorted(Path(folder).glob('*.md')):
        fields, body = _front(path.read_text(encoding='utf-8'))
        title = fields.get('title') or path.stem
        parts = re.split(r'^#{2,3} (.+)$', body, flags=re.M)
        intro = (fields.get('summary', '') + '\n' + parts[0]).strip()
        out.append({'slug': path.stem, 'anchor': '', 'title': title, 'heading': '', 'text': intro})
        for heading, text in zip(parts[1::2], parts[2::2]):
            out.append({'slug': path.stem, 'anchor': heading_id(heading), 'title': title, 'heading': heading.strip(), 'text': text.strip()})
    return out


DOCSTRING = re.compile(r'^[ \t]*(?:async[ \t]+)?(?:def|class)[ \t]+(\w+)[^\n]*:[ \t]*\n[ \t]*[rb]?"""(.*?)"""', re.M | re.S)
MODULE_DOC = re.compile(r'\A(?:#[^\n]*\n|\s)*[rb]?"""(.*?)"""', re.S)


def code_snippets(root=ROOT):
    """The docstrings of the app's modules, classes and functions: {path, name, line, text}. Read with a pattern,
    not parsed: parsing the whole app takes seconds."""
    out = []
    for pattern in CODE_FILES:
        for path in sorted(Path(root).glob(pattern)):
            if path.name.startswith('test') or path.name == 'help_chat.py':
                continue
            try:
                source = path.read_text(encoding='utf-8')
            except (OSError, ValueError):
                continue
            rel = path.relative_to(root).as_posix()
            head = MODULE_DOC.match(source)
            if head:
                out.append({'path': rel, 'name': rel, 'line': 1, 'text': ' '.join(head[1].split())})
            for m in DOCSTRING.finditer(source):
                text = ' '.join(m[2].split())
                if len(text) >= 60:
                    out.append({'path': rel, 'name': m[1], 'line': source.count('\n', 0, m.start()) + 1, 'text': text})
    return out


class Index:
    """BM25 over a list of documents' words."""

    def __init__(self, docs, text):
        self.docs = docs
        self.terms = [words(text(d)) for d in docs]
        self.avg = sum(map(len, self.terms)) / max(1, len(self.terms))
        self.df = {}
        for terms in self.terms:
            for w in set(terms):
                self.df[w] = self.df.get(w, 0) + 1

    def search(self, query, k):
        q = set(words(query))
        if not q:
            return []
        n, scored = len(self.docs), []
        for doc, terms in zip(self.docs, self.terms):
            counts = {}
            for w in terms:
                if w in q:
                    counts[w] = counts.get(w, 0) + 1
            if not counts:
                continue
            score = sum(math.log(1 + (n - self.df[w] + 0.5) / (self.df[w] + 0.5)) * c * 2.2 / (c + 1.2 * (0.25 + 0.75 * len(terms) / self.avg))
                        for w, c in counts.items())
            scored.append((score, doc))
        scored.sort(key=lambda x: -x[0])
        return scored[:k]


def indexes(folder=HELP, root=ROOT):
    key = (str(folder), str(root))
    with _lock:
        if key not in _cache:
            # a heading and the article's title count twice: they say what a section is about
            _cache[key] = (Index(help_sections(folder), lambda d: f"{d['title']} {d['title']} {d['heading']} {d['heading']} {d['text']}"),
                           Index(code_snippets(root), lambda d: f"{d['name']} {d['text']}"))
        return _cache[key]


def link(section):
    return SITE + section['slug'] + ('#' + section['anchor'] if section['anchor'] else '')


def retrieve(question, history=(), folder=HELP, root=ROOT):
    """(help sections, code snippets) for a question: help first; code only for what the help leaves open."""
    docs, code = indexes(folder, root)
    query = ' '.join([question, *[t['text'] for t in history if t.get('role') == 'user'][-1:]])
    found = docs.search(query, SECTIONS)
    best = found[0][0] if found else 0
    found = [doc for score, doc in found if score >= best * 0.35]
    # An article named in the question ("Do it", "Snooze") leads, even when its name is only common words
    named = [d for d in docs.docs if not d['anchor'] and any(len(n) > 3 and re.search(rf'(?i)\b{re.escape(n)}\b', question)
                                                              for n in {d['title'], re.split(r',| and ', d['title'])[0].strip()})]
    found = ([d for d in named if d not in found] + found)[:SECTIONS]
    best = max(best, 6 if named else 0)
    snippets = [doc for score, doc in code.search(query, SNIPPETS)] if len(found) < SECTIONS or best < 6 else []
    return found, snippets[:SNIPPETS]


def sources(sections, snippets):
    seen, out = set(), []
    for s in sections:
        url = link(s)
        if url not in seen:
            seen.add(url)
            out.append({'kind': 'help', 'title': s['title'] + (f": {s['heading']}" if s['heading'] else ''), 'url': url})
    for s in snippets:
        url = f"{CODE}{s['path']}#L{s['line']}"
        if url not in seen:
            seen.add(url)
            out.append({'kind': 'code', 'title': f"{s['path']}" + (f" ({s['name']})" if s['name'] != s['path'] else ''), 'url': url})
    return out


def clean_history(history):
    out = []
    for turn in (history or [])[-HISTORY_TURNS:]:
        if isinstance(turn, dict) and turn.get('role') in ('user', 'assistant') and isinstance(turn.get('text'), str):
            out.append({'role': turn['role'], 'text': ' '.join(turn['text'].split())[:TURN_CHARS]})
    return out


def prompt(question, history, sections, snippets):
    """The whole turn: a short brief, the matching sections and snippets, the last few turns and the question."""
    parts = ["You answer questions about The Machine, an assistant app, in its dashboard's Help panel. Answer only from the "
             "help sections below; use the code notes only for what they leave open, and say when you are not sure. If neither covers "
             "it, say so and suggest Report a bug or support@themachine.computer. You can't see or change the person's Machine, "
             "settings or data, and you take no actions: tell them where to click instead. Reply in at most 120 words, short "
             "sentences, in light markdown: **bold** for what to click, a - list for steps, no headings, no em dashes. Mark "
             "each fact with the number of its source, like [1].", '']
    n = 0
    for s in sections:
        n += 1
        parts += [f"[{n}] Help: {s['title']}" + (f" > {s['heading']}" if s['heading'] else ''), s['text'][:SECTION_CHARS], '']
    for s in snippets:
        n += 1
        parts += [f"[{n}] Code note: {s['path']} {s['name']}", s['text'][:SNIPPET_CHARS], '']
    if not n:
        parts += ['(No help section matches this question.)', '']
    if history:
        parts += ['Earlier in this help chat:'] + [f"{'Person' if t['role'] == 'user' else 'You'}: {t['text']}" for t in history] + ['']
    parts += ['Question: ' + question]
    return '\n'.join(parts)


def openclaw_model_run(config, text, model=None):
    """One raw model turn through the Gateway (its own session, no tools); the reply's text."""
    args = [str((config or {}).get('openclaw') or 'openclaw'), 'infer', 'model', 'run', '--gateway', '--json', '--prompt', text]
    if model:
        args += ['--model', model]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT)
        data = json.loads(result.stdout or '{}')
    except subprocess.TimeoutExpired:
        raise Unavailable('Help took too long to answer. Try again.') from None
    except (OSError, ValueError):
        raise Unavailable('Help can’t reach your model right now.') from None
    texts = [o.get('text') for o in data.get('outputs') or [] if isinstance(o, dict) and isinstance(o.get('text'), str)]
    if result.returncode != 0 or not data.get('ok') or not texts:
        raise Unavailable('Help can’t reach your model right now.')
    return '\n'.join(texts).strip()


def limited(now=None):
    now = time.monotonic() if now is None else now
    with _lock:
        _asked[:] = [t for t in _asked if now - t < 3600]
        if len(_asked) >= PER_HOUR:
            return True
        _asked.append(now)
    return False


def ask(question, history=(), run=None, config=None, model=None, folder=HELP, root=ROOT):
    """{'answer', 'sources'} for one question. `run(config, prompt, model)` makes the model turn."""
    question = ' '.join(str(question or '').split())[:QUESTION_CHARS]
    if not question:
        raise ValueError('Type a question first.')
    history = clean_history(history)
    sections, snippets = retrieve(question, history, folder, root)
    if limited():
        raise Unavailable('That’s a lot of questions for one hour. Try again a bit later.')
    answer = (run or openclaw_model_run)(config, prompt(question, history, sections, snippets), model)
    used = sources(sections, snippets)
    cited = {int(n) for n in re.findall(r'\[(\d{1,2})\]', answer)}
    shown = re.sub(r'[ \t]?\[\d{1,2}\](?:\[\d{1,2}\])*', '', answer).strip()  # the links show the sources
    return {'answer': shown[:4000], 'sources': [s for i, s in enumerate(used, 1) if not cited or i in cited] or used}

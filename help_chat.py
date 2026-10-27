"""Help in the dashboard: questions about how The Machine works, answered from the help articles (docs/help) first
and the app's own code second, with links to what the answer used.

Cheap by design: only the few sections that match the question go in (never every article), with a short prompt,
as a one-shot turn on the Machine's own model through OpenClaw (`openclaw infer model run --gateway`: its own
session, no tools, no workspace files), so it can answer and change nothing. Nothing about the owner goes in: no
messages, people or settings, only the question, the last few turns of this help chat, the public docs and code, and
one line on how technical they likely are (level), guessed here from their setup, the role in USER.md and how they
write; the role itself stays out.

Each answer also names its topic in a few generic words (TOPIC:), for The Machine team's count of what people ask
(help_topics.py); the question never leaves."""
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
BUG = re.compile(r'^[ \t]*\**BUG:?\**[ \t]*$', re.M)  # the model's own line before a bug write-up
BUG_CHARS = 1500
TOPIC_LINE = re.compile(r'^[ \t]*\**TOPIC:?\**[ \t]*(.*)$', re.M | re.I)  # the model's last line: what the question is about
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


IRREGULAR = {'wrote': 'write', 'written': 'write', 'writes': 'write', 'tone': 'tone', 'sent': 'send', 'got': 'get'}


def stem(w):
    """A rough stem, so "writing", "wrote" and "write", or "personalize" and "personalized", find the same section."""
    w = IRREGULAR.get(w, w)
    if len(w) > 4 and w.endswith('s') and not w.endswith('ss'):
        w = w[:-1]
    for suffix in ('ation', 'ing', 'ed'):
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            w = w[:-len(suffix)]
            break
    if len(w) > 6 and w.endswith(('is', 'ise')):
        w = w[:w.rindex('is')] + 'iz'  # British -ise as -ize
    return w[:-1] if len(w) > 3 and w.endswith('e') else w


def words(text):
    return [stem(w) for w in WORD.findall(str(text).lower()) if w not in STOP]


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
        # keywords: words people use for it that the article doesn't ("personalize", "tone"), searched, never shown
        out.append({'slug': path.stem, 'anchor': '', 'title': title, 'heading': '', 'text': intro, 'keywords': fields.get('keywords', '')})
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
            _cache[key] = (Index(help_sections(folder), lambda d: f"{d['title']} {d['title']} {d['heading']} {d['heading']} "
                                                              f"{d.get('keywords', '')} {d.get('keywords', '')} {d['text']}"),
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
    # A page that matches as a whole brings its own sections: its intro only says what it is about
    if found and not found[0]['anchor']:
        own = [d for d in docs.docs if d['slug'] == found[0]['slug'] and d['anchor']]
        found = [found[0], *[d for d in found if d in own], *[d for d in own if d not in found], *[d for d in found[1:] if d not in own]][:SECTIONS]
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


LEVELS = {
    'everyday': 'plain everyday words, no file names, code, commands, config or technical terms; name the button to tap',
    'some': 'plain words; name the setting or screen, and a technical term only with a few words on what it means',
    'technical': 'precise and brief; config keys, commands and code names are fine where they help',
}
TECH_ROLE = re.compile(r'(?i)\b(?:engineer\w*|develop\w*|programm\w*|devops|sysadmin|cto|it|software|data scien\w*|architect|sre|'
                       r'technical|security|infrastructure|platform|backend|frontend|full[ -]?stack|ml|ai researcher)\b')
TECH_WORDS = re.compile(r'(?i)\b(?:api|cli|ssh|json|yaml|config\.json|terminal|docker|git|token|webhook|systemd|python|regex|localhost|'
                        r'port|env|sql|repo|deploy|stack ?trace|log ?file|gateway|openclaw|cron)\b|`|\$ \w')
PLAIN_WORDS = re.compile(r'(?i)\b(?:what does .{1,30} mean|i\'?m not (?:very )?technical|not good with (?:computers|tech)|confus\w+|simple words)\b')


def level(config=None, role='', said=()):
    """(level, why): how technical the owner likely is, from what this Machine knows: how it runs (on their own
    computer, or hosted), GitHub or a coding agent set up, the role in USER.md and the words they use in this chat.
    Only the level and these plain reasons go into the turn."""
    config, points, why = config or {}, 0, []
    if config and not str(config.get('manage_url') or '').startswith('https://'):
        points, why = points + 1, why + ['runs The Machine on their own computer']
    services = {a.get('service') for a in config.get('accounts') or [] if isinstance(a, dict)}
    if 'github' in services or config.get('agents'):
        points, why = points + 1, why + ['set up GitHub or a coding agent']
    if role and TECH_ROLE.search(role):
        points, why = points + 2, why + ['has a technical role']
    text = ' '.join(said)
    if TECH_WORDS.search(text):
        points, why = points + 1, why + ['uses technical words here']
    if PLAIN_WORDS.search(text):
        points, why = points - 2, why + ['asks for plain words here']
    return ('technical' if points >= 3 else 'some' if points >= 1 else 'everyday'), why


def prompt(question, history, sections, snippets, audience=None):
    """The whole turn: a short brief, the matching sections and snippets, the last few turns and the question."""
    name, why = audience or ('everyday', [])
    parts = ["You answer questions about The Machine, an assistant app, in its dashboard's Help panel. Answer only from the "
             "help sections below; use the code notes only for what they leave open. If neither covers "
             "it, say so and suggest Report a bug or support@themachine.computer. You can't see or change the person's Machine, "
             "settings or data, and you take no actions: tell them where to click instead. Reply in at most 120 words, short "
             "sentences, in light markdown: **bold** for what to click, a - list for steps, no headings, no em dashes. Mark "
             "each fact with the number of its source, like [1].",
             "Give the answer itself: the concrete things from the sections that do what they ask, most useful first, with "
             "where to click. Don't send them off to read a page instead; the source numbers link it. Never comment on how "
             "the question is worded, or on what the pages don't say or promise. Ask a question back only when the answer "
             "really depends on it.",
             "Prefer what The Machine already does by itself (it learns from what they send, edit, dismiss and say in a to-do's "
             "chat) and what they can set in Settings over building something new. Suggest a skill, an agent or code only when "
             "nothing built in covers it, or they ask for one.",
             f"How technical they likely are: {name}" + (f" ({', '.join(why)})" if why else '') + f". Answer in {LEVELS[name]}. "
             "If how they write in this chat says otherwise, follow that.",
             "Judge from what they mean, not from the words they use, "
             "whether they describe something in The Machine not working as it should (a bug, not a how-to question). Only then, "
             "after your answer, add a line that is just BUG: and below it a short report for The Machine team, in their "
             "language: what they did, what they expected and what happened, one line each, from what they said only.",
             "Last, always end with one line TOPIC: and 2 to 5 lowercase English words for what the question is about, the way "
             "the help pages would say it, like \"snooze a to-do\" or \"writing style\". Never a name, company, address, "
             "number or their own words.", '']
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


def openclaw_model_run(config, text, model=None, thinking=None):
    """One raw model turn through the Gateway (its own session, no tools); the reply's text."""
    args = [str((config or {}).get('openclaw') or 'openclaw'), 'infer', 'model', 'run', '--gateway', '--json', '--prompt', text]
    if model:
        args += ['--model', model]
    if thinking:
        args += ['--thinking', thinking]
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


def ask(question, history=(), run=None, config=None, model=None, folder=HELP, root=ROOT, role='', thinking=None):
    """{'answer', 'sources', 'topic', 'answered'} for one question. `run(config, prompt, model)` makes the model turn
    (with thinking=... too when a thinking level was picked, chat_model.py). `role` is the owner's role from USER.md, for
    level() only."""
    question = ' '.join(str(question or '').split())[:QUESTION_CHARS]
    if not question:
        raise ValueError('Type a question first.')
    history = clean_history(history)
    sections, snippets = retrieve(question, history, folder, root)
    if limited():
        raise Unavailable('That’s a lot of questions for one hour. Try again a bit later.')
    audience = level(config, role, [question, *[t['text'] for t in history if t['role'] == 'user']])
    answer = (run or openclaw_model_run)(config, prompt(question, history, sections, snippets, audience), model,
                                         **({'thinking': thinking} if thinking else {}))
    answer, topic = split_topic(answer)
    answer, bug = split_bug(answer)
    used = sources(sections, snippets)
    cited = {int(n) for n in re.findall(r'\[(\d{1,2})\]', answer)}
    shown = re.sub(r'[ \t]?\[\d{1,2}\](?:\[\d{1,2}\])*', '', answer).strip()  # the links show the sources
    out = {'answer': shown[:4000], 'sources': [s for i, s in enumerate(used, 1) if not cited or i in cited] or used}
    if bug:
        out['bug'] = bug  # the dashboard offers Report this bug, prefilled with it; nothing is sent from here
    # For help_topics.record, never shown: the model's words for the topic, else the best section's own title
    best = sections[0] if sections else None
    out['topic'] = topic or (f"{best['title']} {best['heading']}".strip().lower() if best else '')
    out['answered'] = bool(sections)
    return out


def split_topic(answer):
    """(answer, topic or ''): the TOPIC: line the turn ends with, taken out of what the owner sees."""
    found = list(TOPIC_LINE.finditer(answer or ''))
    if not found:
        return answer, ''
    m = found[-1]
    return (answer[:m.start()] + answer[m.end():]).strip(), ' '.join(m[1].strip(' "\'.*').split())[:80]


def vocabulary(folder=HELP, root=ROOT):
    """Every word stem the public help pages use: a topic may use only these (help_topics.clean)."""
    docs, _ = indexes(folder, root)
    return {w for terms in docs.terms for w in terms}


def split_bug(answer):
    """(answer, bug write-up or None): the model ends a reply with a BUG: line and a short report when it judged the
    person describes a bug. The write-up only prefills Report a bug, where the owner edits, reviews and sends it."""
    m = BUG.search(answer or '')
    if not m:
        return answer, None
    bug = re.sub(r'[ \t]?\[\d{1,2}\](?:\[\d{1,2}\])*', '', answer[m.end():]).strip()[:BUG_CHARS]
    return answer[:m.start()].rstrip(), bug or None

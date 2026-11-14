#!/usr/bin/env python3
"""Translate what English has and another language doesn't yet: catalog keys (i18n/<code>.json) and help articles
(docs/help/<code>/*.md). The model is gpt-6-luna behind Salesflare's Azure API gateway (the startup credits), with the
glossary (i18n/glossary.md) in every request. The languages are the app's own (locale_prefs.LANGUAGES), with their
names and plural forms from i18n.py, so a new language here is the same change that adds it to the app.

    AZ_TRANSLATE_KEY=... python3 scripts/translate.py catalog   # en.json keys missing in i18n/<code>.json
    AZ_TRANSLATE_KEY=... python3 scripts/translate.py help      # docs/help/*.md -> docs/help/<code>/*.md
    AZ_TRANSLATE_KEY=... python3 scripts/translate.py all       # both
    python3 scripts/translate.py all --check                    # what is missing or out of date, no model calls

Only what is missing or out of date is sent. A catalog key is missing when its language has no entry for it (keys are
the English text, so new English is a new key), or an entry of another shape (a plural entry for a plain one).
Entries English no longer has are dropped. A translated article carries the hash of the English it was made from
(`translated:` in its front matter); an article without one, from before this script, counts as current when git shows
no change to the English after its last change. Each answer is checked before it is written (the same placeholders,
names and glossary terms, the same headings, paragraphs and list items, no em dash); an answer that fails is asked
again once with what was wrong, then left out, so the app shows English there until the next run.
The key is read from the environment only (never a flag or a file), and never printed.
.github/workflows/translate.yml runs `all` once a day on main as it is then, opens or replaces one pull request and
approves its tests' run; scripts/release.py cut refuses a commit where `all --check` finds anything."""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import functools
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
import i18n  # noqa: E402
import i18n_extract  # noqa: E402
import locale_prefs  # noqa: E402

ENDPOINT = 'https://salesflare-ai-apim.azure-api.net/ai/openai/v1/responses'
MODEL = 'gpt-6-luna'
CATALOG = ROOT / 'i18n'
GLOSSARY = CATALOG / 'glossary.md'
HELP = ROOT / 'docs' / 'help'
HOLE = re.compile(r'\{\d*\}')
WORKERS = int(os.environ.get('TRANSLATE_WORKERS', '6'))
PLURAL_ORDER = ('zero', 'one', 'two', 'few', 'many', 'other')


def languages():
    """The app's languages other than English: each has a catalog and a help folder."""
    return [code for code in locale_prefs.LANGUAGES if code != 'en']


def plural_forms(lang):
    """The plural categories lang's entries have, from i18n.plural_form (CLDR): ('one', 'other') in most of them."""
    found = {i18n.plural_form(lang, n) for n in (0, 1, 2, 3, 4, 5, 11, 12, 21, 22, 25, 101, 111, 1.5)}
    return tuple(c for c in PLURAL_ORDER if c in found)


# ---------------------------------------------------------------------------------------------- glossary

def glossary(text=None):
    """(names, {english: {code: forms}}, {code: gender rule}, tone, {english: {code: [checked forms]}}, exceptions) from
    glossary.md: every table with a column per language, the Names list, the gender table, the Tone paragraph, the
    Terms table that tests/test_i18n.py checks and its Exceptions."""
    text = text if text is not None else GLOSSARY.read_text(encoding='utf-8')
    names_part = text.split('## Names', 1)[1].split('##', 1)[0]
    names_line = ' '.join(line for line in names_part.splitlines()[3:] if line.strip())
    names = [n for n in (re.sub(r'\s*\(.*?\)', '', n).strip() for n in re.sub(r'\(.*?\)', '', names_line).rstrip('.').split(',')) if n]
    terms, gender, checked = {}, {}, {}
    for section in re.split(r'\n## ', text)[1:]:
        heading, _, body = section.partition('\n')
        rows = [[c.strip() for c in line.strip().strip('|').split('|')] for line in body.splitlines() if line.startswith('|')]
        if len(rows) < 3:
            continue
        head = rows[0]
        if heading.startswith('The Machine'):  # | Language | Gender | Rule |
            for row in rows[2:]:
                gender[row[0]] = ' '.join(row[1:])
            continue
        if 'nl' not in head:
            continue
        for row in rows[2:]:
            terms[row[0]] = {head[i]: row[i] for i in range(1, min(len(head), len(row))) if row[i]}
            if heading.strip() == 'Terms':
                checked[row[0]] = {h: [f.strip() for f in v.split(',')] for h, v in terms[row[0]].items()}
    tone = ' '.join(text.split('Tone:', 1)[1].split('\n\n', 1)[0].split()) if 'Tone:' in text else ''
    plurals = ' '.join(text.split('Plurals:', 1)[1].split('\n\n', 1)[0].split()) if 'Plurals:' in text else ''
    exceptions = set(re.findall(r'^- `(.+?)`', text.split('## Exceptions', 1)[1].split('##', 1)[0], re.M)) if '## Exceptions' in text else set()
    return {'names': names, 'terms': terms, 'gender': gender, 'tone': ' '.join(p for p in (tone, plurals) if p),
            'checked': checked, 'exceptions': exceptions}


def term_in(term, english):
    """tests/test_i18n.py's rule: a capitalized term counts capitalized only, an inflection counts, a file name doesn't."""
    flags = 0 if term[0].isupper() else re.I
    return re.search(r'(?<![\w.-])' + re.escape(term) + r'(?:s|es|d|ed|ing)?(?![\w-]|\.md)', english, flags) is not None


@functools.lru_cache(maxsize=None)
def wrong_gender():
    """{code: pattern} of forms that are always wrong for The Machine: the `wrong` table of tests/test_i18n.py's gender
    test, read without running it, so an answer the test would fail is asked again instead."""
    try:
        tree = ast.parse((ROOT / 'tests' / 'test_i18n.py').read_text(encoding='utf-8'))
    except (OSError, SyntaxError):
        return {}
    for node in ast.walk(tree):
        if (isinstance(node, ast.FunctionDef) and 'gender' in node.name):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'wrong' for t in sub.targets):
                    try:
                        return ast.literal_eval(sub.value)
                    except ValueError:
                        return {}
    return {}


def language_name(lang):
    return i18n.language_name(lang)


def instructions(lang, texts, what, words=None):
    words = words or glossary()
    blob = ' '.join(texts).lower()
    used = [(en, row[lang]) for en, row in words['terms'].items()
            if lang in row and re.search(r'(?<![\w-])' + re.escape(en.lower().split(' (')[0]), blob)]
    name = language_name(lang)
    lines = [
        f'You translate {what} for The Machine, an AI assistant product, from English into {name} ({lang}).',
        'Write it the way a native product would say it: short, natural, plain. Never word for word. Keep the meaning, '
        'every fact and every qualification; do not add, summarize or leave out anything.',
        f'Tone and conventions: {words["tone"]}' if words['tone'] else '',
        'Never use an em dash (—).',
        'Keep these names exactly as written, never translated or inflected into another word: ' + ', '.join(words['names']) + '.',
        'Keep exactly as they are: placeholders in braces ({}, {0}, {1}; a translation may number them {0}, {1} to '
        'reorder), text in angle brackets (<job id>), URLs, email addresses, file names, commands, code, JSON, numbers '
        'and people, company and place names.',
        f'The Machine, and an owner\'s Machine, in {name}: {words["gender"][lang]}' if lang in words['gender'] else '',
        'Use these terms (English = this language; when several forms are given, the first is the base form and the '
        'others are its inflections):\n' + '\n'.join(f'- {en} = {tr}' for en, tr in used) if used else '',
    ]
    return '\n'.join(line for line in lines if line)


# ---------------------------------------------------------------------------------------------- the model

def _key():
    key = os.environ.get('AZ_TRANSLATE_KEY', '').strip()
    if not key:
        raise SystemExit('AZ_TRANSLATE_KEY is not set: export it (the "translate" environment\'s secret in CI). '
                         'It is never a flag or a file.')
    return key


def ask(lang, instruction, payload, cache_key):
    """One request: the instructions, a JSON payload, a JSON object back."""
    payload = payload if 'json' in payload.lower() else 'Answer in JSON.\n' + payload  # the endpoint's json mode asks for the word
    body = json.dumps({'model': MODEL, 'instructions': instruction, 'input': payload, 'text': {'format': {'type': 'json_object'}},
                       'prompt_cache_key': cache_key}).encode()
    error = None
    for attempt in range(5):
        if attempt:
            time.sleep(2 * 2 ** attempt)
        request = urllib.request.Request(ENDPOINT, data=body, headers={'authorization': _key(), 'content-type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                answer = json.load(response)
        except urllib.error.HTTPError as e:
            error = f'HTTP {e.code}'
            if e.code == 429 or e.code >= 500:
                continue
            raise SystemExit(f'translate: {error}')
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            error = type(e).__name__
            continue
        text = answer.get('output_text') or ''.join(c.get('text') or '' for item in answer.get('output') or [] for c in item.get('content') or [])
        try:
            return json.loads(text)
        except ValueError as e:
            error = f'not JSON: {e}'
    raise RuntimeError(f'translate ({lang}): {error}')


# ---------------------------------------------------------------------------------------------- checks

TERM_PROBLEM = ' (a glossary term)'


def holes_ok(key, text):
    """As many placeholders as the key; numbered ones ({0}, {1}) cover each position once."""
    want, got = HOLE.findall(key), HOLE.findall(text)
    if len(want) != len(got):
        return False
    numbered = [h[1:-1] for h in got if h != '{}']
    return not numbered or (len(numbered) == len(got) and sorted(numbered) == [str(i) for i in range(len(got))])


def string_problems(key, text, lang, words):
    """What is wrong with one translated form of a catalog key, as notes for the model ([] when nothing)."""
    if not isinstance(text, str) or not text.strip():
        return ['empty']
    out = []
    if not holes_ok(key, text):
        out.append('keep every placeholder ({}, or {0} {1} to reorder) exactly as many times as in the English')
    if '—' in text:
        out.append('no em dash')
    out += [f'keep the name "{n}"' for n in words['names'] if re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', key) and n not in text]
    if key not in words['exceptions']:
        out += [f'"{term}" must read one of: {", ".join(forms[lang])}' + TERM_PROBLEM for term, forms in words['checked'].items()
                if lang in forms and term_in(term, key) and not any(f.lower() in text.lower() for f in forms[lang])]
    pattern = wrong_gender().get(lang)
    if pattern and re.search(pattern, text):
        out.append(f'The Machine is never masculine here: {words["gender"].get(lang, "")}')
    return out


def entry_problems(key, value, lang, words):
    """Problems with a whole catalog entry: a string, or a plural entry with exactly lang's forms."""
    if isinstance(value, dict):
        forms = plural_forms(lang)
        if sorted(value) != sorted(forms):
            return [f'a plural entry has exactly these forms: {", ".join(forms)}']
        whole = ' '.join(v for v in value.values() if isinstance(v, str))
        return sorted({p for form in value.values() for p in string_problems(key, form, lang, words)
                       if not p.endswith(TERM_PROBLEM)} | {p for p in string_problems(key, whole, lang, words) if p.endswith(TERM_PROBLEM)})
    return string_problems(key, value, lang, words)


# ---------------------------------------------------------------------------------------------- catalog keys

def load(lang):
    path = CATALOG / f'{lang}.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


def catalog_todo(lang, en=None, cat=None):
    """The en.json keys lang has no fitting entry for: none, or one of another shape."""
    en = load('en') if en is None else en
    cat = load(lang) if cat is None else cat
    forms = sorted(plural_forms(lang))
    return [k for k, v in en.items() if k not in cat or isinstance(v, dict) != isinstance(cat[k], dict)
            or isinstance(v, dict) and sorted(cat[k]) != forms]


def catalog_stale(lang, en=None, cat=None):
    """Entries lang has that en.json no longer has (the English changed or went): dropped by the next run."""
    en = load('en') if en is None else en
    cat = load(lang) if cat is None else cat
    return sorted(set(cat) - set(en))


def source(key, value):
    """What the model reads for one entry: the English, and the key as a note when it says more ("Close (a closeness)")."""
    if isinstance(value, dict):
        return {'english': value}
    return {'english': value, 'meaning': key} if value != key else {'english': value}


def translate_entries(lang, keys, en, words=None, ask=ask):
    """{key: translation} for catalog keys, in batches; an entry whose answer fails its checks twice is left out."""
    words = words or glossary()
    forms = plural_forms(lang)
    what = ('the user interface of a web app, one string each (a button, a label, a status line, a message; '
            'a plural entry is one string per count form)')
    done = {}

    def batch(chunk, notes=None):
        items = {str(i): source(k, en[k]) for i, k in enumerate(chunk)}
        payload = ('Return one JSON object {"t": {"<id>": <translation>}} with every id. Translate each "english" on '
                   'its own; "meaning", when there, says what it is and is not translated. A plain "english" string '
                   'becomes a string. An "english" object of count forms (one, other) becomes an object with exactly '
                   f'these keys for {language_name(lang)}: {json.dumps(list(forms))}, each the whole text for that count.'
                   + (f'\nLast time these answers were wrong: {json.dumps(notes, ensure_ascii=False)}' if notes else '')
                   + '\n' + json.dumps(items, ensure_ascii=False))
        texts = [json.dumps(en[k], ensure_ascii=False) for k in chunk]
        got = (ask(lang, instructions(lang, texts, what, words), payload, f'machine-app:{lang}') or {}).get('t') or {}
        return {chunk[int(i)]: v for i, v in got.items() if i.isdigit() and int(i) < len(chunk)}

    chunks, size, current = [], 0, []
    for k in dict.fromkeys(keys):
        length = len(json.dumps(en[k], ensure_ascii=False))
        if current and (len(current) >= 40 or size + length > 6000):
            chunks.append(current)
            current, size = [], 0
        current.append(k)
        size += length
    if current:
        chunks.append(current)
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        for got in pool.map(batch, chunks):
            done.update(got)
    retry = {k: entry_problems(k, done.get(k), lang, words) for k in keys}
    retry = {k: p for k, p in retry.items() if p}
    again = {}
    for i in range(0, len(retry), 40):
        chunk = list(retry)[i:i + 40]
        again.update(batch(chunk, {str(n): {'answer': done.get(k), 'fix': retry[k]} for n, k in enumerate(chunk)}))
    for k in retry:
        if entry_problems(k, again.get(k), lang, words):
            done.pop(k, None)
            print(f'{lang}: left in English after two tries: {k[:80]!r}', file=sys.stderr)
        else:
            done[k] = again[k]
    return {k: done[k] for k in keys if k in done}


def run_catalog(langs, check=False, ask=ask):
    en, words, left = load('en'), None, 0
    for lang in langs:
        cat = load(lang)
        todo, stale = catalog_todo(lang, en, cat), catalog_stale(lang, en, cat)
        print(f'{lang}: {len(todo)} catalog keys to translate, {len(stale)} no longer in en.json')
        if check:
            left += len(todo)
            continue
        if todo:
            words = words or glossary()
            cat.update(translate_entries(lang, todo, en, words, ask))
        for k in stale:
            cat.pop(k, None)
        if todo or stale:
            i18n_extract.write_catalog(CATALOG / f'{lang}.json', cat)
        left += len(catalog_todo(lang, en, cat))
    return left


# ---------------------------------------------------------------------------------------------- help articles

LINK = re.compile(r'\]\(([^)\s]+)\)')
CODE = re.compile(r'`[^`]+`')
HEADING = re.compile(r'^(#{2,3}) ', re.M)
ITEM = re.compile(r'^(- |\d+\. )', re.M)
CODE_TOKEN = re.compile(r'`§(\d+)`')
FRONT = re.compile(r'---\n(.*?)\n---\n', re.S)
BOLD = re.compile(r'\*\*(.+?)\*\*')
ARTICLE_HOLE = re.compile(r'\{[a-z_.0-9]*\}')


def front(text):
    """(ordered [(key, value)] of the front matter, body)."""
    m = FRONT.match(text)
    if not m:
        return [], text
    return [(k.strip(), v.strip()) for k, _, v in (line.partition(':') for line in m[1].splitlines())], text[m.end():]


def blocks(body):
    """Per section: its paragraphs and list items (scripts/help_check.py's rule for kept-in-step translations)."""
    return [sum(len(b.splitlines()) if re.match(r'(- |\d+\. )', b) else 1 for b in re.split(r'\n\s*\n', part.strip()) if b.strip() and not b.startswith('#'))
            for part in re.split(r'^(?=#{2,3} )', body, flags=re.M)]


def same(pattern, a, b):
    return sorted(pattern.findall(a)) == sorted(pattern.findall(b))


def article_problems(en, tr):
    out = []
    for name, pattern in (('link targets', LINK), ('code in backticks', CODE), ('placeholders', ARTICLE_HOLE)):
        if not same(pattern, en, tr):
            # plain text, not a Python list: its repr doubles every backslash, and the model copies what it reads
            out.append(f'keep the same {name} exactly: {", ".join(sorted(pattern.findall(en)))}')
    if HEADING.findall(en) != HEADING.findall(tr):
        out.append('keep the same ## and ### headings in the same order')
    elif blocks(en) != blocks(tr):
        out.append('keep the same paragraphs and list items in each section, one list item per line, as - or 1.')
    if '—' in tr:
        out.append('no em dash')
    return out


def protect_code(body):
    """body with each `code` span swapped for `§1`, `§2`, ... and the spans: the model never sees what is inside code,
    so it can neither translate it nor spell a backslash in it wrong in its JSON answer."""
    spans = []

    def swap(m):
        spans.append(m.group(0))
        return f'`§{len(spans)}`'
    return CODE.sub(swap, body), spans


def restore_code(text, spans):
    # a function, not a replacement string: re.sub would read the backslash in `DOMAIN\name` as an escape
    return CODE_TOKEN.sub(lambda m: spans[int(m[1]) - 1] if 0 < int(m[1]) <= len(spans) else m.group(0), text)


def stamp(path):
    """The English article's hash: a translation made from it carries it as `translated:`."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def articles(folder=HELP):
    return sorted(p for p in folder.glob('*.md') if re.fullmatch(r'[a-z0-9-]+', p.stem))


class History:
    """When each file under docs/help last changed, in main's order (squash merges keep it a line): a translation
    without a stamp is current when its English didn't change after it. None without git history (a shallow clone)."""

    def __init__(self, folder=HELP):
        self.order = None
        try:
            shallow = subprocess.run(['git', '-C', str(folder), 'rev-parse', '--is-shallow-repository'],
                                     capture_output=True, text=True, timeout=60)
            if shallow.returncode or shallow.stdout.strip() != 'false':
                return
            log = subprocess.run(['git', '-C', str(folder), 'log', '--format=@%H', '--name-only', '--', '.'],
                                 capture_output=True, text=True, timeout=600)
            top = subprocess.run(['git', '-C', str(folder), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return
        if log.returncode or top.returncode:
            return
        root, self.order, n = Path(top.stdout.strip()), {}, 0
        for line in log.stdout.splitlines():
            if line.startswith('@'):
                n += 1
            elif line.strip():
                self.order.setdefault(str((root / line.strip()).resolve()), n)  # newest first: the first one is the last change

    def changed_after(self, english, translation):
        """True when the English changed after the translation; None when git can't tell."""
        if self.order is None:
            return None
        e, t = self.order.get(str(english.resolve())), self.order.get(str(translation.resolve()))
        if e is None or t is None:
            return None
        return e < t


def help_state(lang, path, folder=HELP, history=None):
    """'missing', 'stale', 'current' or 'unstamped' (current, made before stamps) for one article in lang."""
    local = folder / lang / path.name
    if not local.is_file():
        return 'missing'
    fields, body = front(local.read_text(encoding='utf-8'))
    found = dict(fields).get('translated')
    if found:
        return 'current' if found == stamp(path) else 'stale'
    after = history.changed_after(path, local) if history else None
    if after is None:  # no history to go by: current while it still has the English's headings
        after = HEADING.findall(front(path.read_text(encoding='utf-8'))[1]) != HEADING.findall(body)
    return 'stale' if after else 'unstamped'


def help_todo(langs, folder=HELP, history=None):
    """{lang: [(path, state)]} for every article that is not current in lang."""
    history = history if history is not None else History(folder)
    out = {}
    for lang in langs:
        out[lang] = [(p, s) for p in articles(folder) for s in [help_state(lang, p, folder, history)] if s != 'current']
    return out


def app_labels(lang, body):
    """{english label: the app's translation} for every **label** in the article that lang's catalog has, so the
    article names a button the way the app shows it."""
    catalog = load(lang)
    out = {}
    for label in BOLD.findall(body):
        bare = label.strip().rstrip('.:')
        if isinstance(catalog.get(bare), str) and not HOLE.search(bare):
            out[bare] = catalog[bare]
    return out


def translate_article(lang, path, words=None, ask=ask):
    words = words or glossary()
    fields, body = front(path.read_text(encoding='utf-8'))
    fields = dict(fields)
    sent, spans = protect_code(body.strip())
    src = {'title': fields.get('title', ''), 'summary': fields.get('summary', ''), 'body': sent}
    what = 'a help article (Markdown)'
    labels = app_labels(lang, body)
    base = ('Return one JSON object {"title": "...", "summary": "...", "body": "..."}: the article translated. The body is '
            'Markdown: keep its structure exactly (the same ## and ### headings in the same order, the same paragraphs and '
            'list items, **bold**, `code` unchanged, links as [translated text](unchanged target)). Inside `code` nothing is '
            'translated; each `§1`, `§2`, ... stands for a piece of code: keep every one exactly once, as it is. '
            'Words the app shows on a button, tab or setting are in bold.'
            + ('\nThe app shows these labels so in this language; write each in bold exactly like this: '
               + json.dumps(labels, ensure_ascii=False) if labels else ''))
    notes = None
    for attempt in range(2):
        payload = base + (f'\nLast time it was wrong: {"; ".join(notes)}' if notes else '') + '\n' + json.dumps(src, ensure_ascii=False)
        got = ask(lang, instructions(lang, [src['title'], src['summary'], sent], what, words), payload, f'machine-app-help:{lang}') or {}
        answer = got.get('body') if isinstance(got.get('body'), str) else ''
        got['body'] = restore_code(answer, spans)
        problems = article_problems(sent, answer) or article_problems(body.strip(), got['body'].strip())
        for k in ('title', 'summary'):
            if src[k]:
                text = got.get(k)
                if not isinstance(text, str) or not text.strip() or '\n' in text.strip():
                    problems.append(f'a one-line {k}')
                elif '—' in text:
                    problems.append(f'no em dash in the {k}')
        # a label not as the app shows it is asked again once; the second time the article is kept anyway
        wrong = [f'write **{tr}** for {en}' for en, tr in labels.items() if f'**{tr}' not in got['body']]
        if not problems and (not wrong or attempt):
            return got
        notes = problems + wrong
    print(f'{lang}: {path.name} left as it was after two tries: {"; ".join(notes)}', file=sys.stderr)
    return None


def article_text(path, title, summary, body):
    """The translation's file: the English front matter with its title and summary translated and the stamp."""
    lines = []
    for k, v in front(path.read_text(encoding='utf-8'))[0]:
        if k != 'translated':
            lines.append(f'{k}: {" ".join({"title": title, "summary": summary}.get(k, v).split())}')
    lines.append(f'translated: {stamp(path)}')
    return '---\n' + '\n'.join(lines) + '\n---\n' + body.strip() + '\n'


def add_stamp(lang, path, folder=HELP):
    """A current translation from before stamps gets the English's hash, nothing else changes."""
    local = folder / lang / path.name
    fields, body = front(local.read_text(encoding='utf-8'))
    fields = dict(fields)
    local.write_text(article_text(path, fields.get('title', ''), fields.get('summary', ''), body), encoding='utf-8')


def run_help(langs, check=False, folder=HELP, ask=ask, history=None):
    todo = help_todo(langs, folder, history)
    left = 0
    for lang in langs:
        gone = sorted(p for p in (folder / lang).glob('*.md') if not (folder / p.name).is_file()) if (folder / lang).is_dir() else []
        counts = {s: sum(1 for _, x in todo[lang] if x == s) for s in ('missing', 'stale', 'unstamped')}
        print(f'{lang}: {counts["missing"]} help articles to translate, {counts["stale"]} out of date'
              + (f', {counts["unstamped"]} to stamp' if counts['unstamped'] else '') + (f', {len(gone)} no longer in English' if gone else ''))
        if check:
            left += counts['missing'] + counts['stale'] + len(gone)
            continue
        for old in gone:
            old.unlink()
        for path, state in todo[lang]:
            if state == 'unstamped':
                add_stamp(lang, path, folder)
    if check:
        return left
    words = glossary()
    jobs = [(lang, path) for lang in langs for path, state in todo[lang] if state != 'unstamped']
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(translate_article, lang, path, words, ask): (lang, path) for lang, path in jobs}
        for future in concurrent.futures.as_completed(futures):
            lang, path = futures[future]
            got = future.result()
            if got:
                (folder / lang).mkdir(exist_ok=True)
                (folder / lang / path.name).write_text(article_text(path, got['title'], got['summary'], got['body']), encoding='utf-8')
            else:
                left += 1
    return left


def problems(langs=None, folder=HELP):
    """What a release would ship untranslated, as lines ([] when everything is translated): for scripts/release.py."""
    langs = langs or languages()
    out, en, history = [], load('en'), History(folder)
    for lang in langs:
        todo = catalog_todo(lang, en)
        if todo:
            out.append(f'{lang}: {len(todo)} catalog keys not translated (first: {todo[0][:60]!r})')
        for path, state in help_todo([lang], folder, history)[lang]:
            if state != 'unstamped':
                out.append(f'{lang}: docs/help/{path.name} {"not translated" if state == "missing" else "out of date with its English"}')
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('what', choices=('catalog', 'help', 'all'))
    p.add_argument('--lang', action='append', choices=languages(), help='only this language (repeat for more)')
    p.add_argument('--check', action='store_true', help='list what is missing or out of date, call nothing (exit 1 when something is)')
    args = p.parse_args(argv)
    langs = args.lang or languages()
    left = 0
    if args.what in ('catalog', 'all'):
        left += run_catalog(langs, check=args.check)
    if args.what in ('help', 'all'):
        left += run_help(langs, check=args.check)
    if left:
        print(f'{left} left: {"run without --check to translate them" if args.check else "the next run tries them again"}')
    return 1 if left else 0


if __name__ == '__main__':
    sys.exit(main())

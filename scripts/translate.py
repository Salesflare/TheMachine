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
(`translated:` in its front matter), written only here: a translation without one is out of date, and a pull request
never moves a stamp by hand (an English edit that changes no meaning still puts its translations out of date for a
day). Each answer is checked before it is written (the English's shape, a string or count forms, the same placeholders as
often, names and glossary terms, field names, values and date formats a model reads, the same headings, paragraphs and list
items, link targets and code, no em dash); an answer that fails is asked again once with what was wrong, then left
out, so the app shows English there until the next run. In an article, a **label** the app has reads as the app's
translation and a link whose English text is the target's title reads as its translated title: both are put right
in the answer itself, not asked for again. A translated article that fails that check, or whose body
scripts/translate_stale.json lists, is out of date whatever its stamp says: the next run translates it again.
New instructions reach only what is sent: new and changed English, never a retranslation of what is current.
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
STALE_BODIES = ROOT / 'scripts' / 'translate_stale.json'
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
    Terms table that tests/test_i18n.py checks, its Exceptions and what a key means (means)."""
    text = text if text is not None else GLOSSARY.read_text(encoding='utf-8')
    names_part = text.split('## Names', 1)[1].split('##', 1)[0]
    names_line = ' '.join(line for line in names_part.splitlines()[3:] if line.strip())
    names = [n for n in (re.sub(r'\s*\(.*?\)', '', n).strip() for n in re.sub(r'\(.*?\)', '', names_line).rstrip('.').split(',')) if n]
    terms, gender, checked, means = {}, {}, {}, {}
    button_rule, buttons = '', {}
    for section in re.split(r'\n## ', text)[1:]:
        heading, _, body = section.partition('\n')
        rows = [[c.strip() for c in line.strip().strip('|').split('|')] for line in body.splitlines() if line.startswith('|')]
        if heading.startswith('Buttons') and 'Buttons:' in body:  # the rule (without its notes on the table), | Language | Rule |
            button_rule = ' '.join(body.split('Buttons:', 1)[1].split('\n\n', 1)[0].split()).split(' The table gives', 1)[0]
            buttons = {row[0]: row[1] for row in rows[2:] if len(row) > 1}
            continue
        if heading.startswith('What a key means'):  # | Key | Meaning |
            means = {row[0].strip('`'): row[1] for row in rows[2:] if len(row) > 1}
            continue
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
            'checked': checked, 'exceptions': exceptions, 'means': means, 'button_rule': button_rule, 'buttons': buttons}


def term_in(term, english, names):
    """Does english use the glossary term? A capitalized term counts capitalized only, an inflection counts ("Snoozed",
    "To-dos"), a file name doesn't (.skill, SKILL.md), and a name spelled like the term (Signal, the app) is that name as
    it is written, not the term. tests/test_i18n.py asks this too."""
    for name in names:
        if name != term and name.lower() == term.lower():
            english = re.sub(r'(?<![\w-])' + re.escape(name) + r'(?![\w-])', ' ', english)
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
    named = {n.lower() for n in words['names']}  # "signal = señal" goes along only with texts that mean a signal, not the app Signal
    used = [(en, row[lang]) for en, row in words['terms'].items()
            if lang in row and re.search(r'(?<![\w-])' + re.escape(en.lower().split(' (')[0]), blob)
            and (en in words['names'] or en.lower() not in named or any(term_in(en, t, words['names']) for t in texts))]
    name = language_name(lang)
    lines = [
        f'You translate {what} for The Machine, an AI assistant product, from English into {name} ({lang}).',
        'Write it the way a native product would say it: short, natural, plain. Never word for word. Keep the meaning, '
        'every fact and every qualification; do not add, summarize or leave out anything.',
        f'Tone and conventions: {words["tone"]}' if words['tone'] else '',
        f'Short UI copy: {words["button_rule"]}' if words.get('button_rule') else '',
        f'Buttons in {name}: {words["buttons"][lang]}' if lang in words.get('buttons', {}) else '',
        'Never use an em dash (—), also where this language\'s own typography would (as in Russian "X — это Y"): '
        'write a colon, a comma or two sentences instead.',
        'Keep these names exactly as written, never translated or inflected into another word: ' + ', '.join(words['names']) + '.',
        'Keep exactly as they are: placeholders in braces ({}, {0}, {1}; a translation may number them {0}, {1} to '
        'reorder), text in angle brackets (<job id>), URLs, email addresses, file names, commands, code, JSON, numbers '
        'and people, company and place names.',
        'Text that code or a model reads stays as written, also inside instructions meant for a model: field names, '
        'keys, enum and op values (due, op, create, done) and date formats (YYYY-MM-DD). Only the words around them '
        'are translated.',
        'A label the app shows (in bold in help) reads exactly as the app\'s own translation of that label, and a link '
        'to another article reads as that article\'s translated title.',
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
KIND_FIRST = ('{} to {} (a message)', '{} from {} (a source)')  # a to-do's source line: "WhatsApp to Anna", never "From {} to {}"
# What code or a model reads in an instruction for one ("op is create, update or delete", "due must be YYYY-MM-DD",
# "A refund needs due: ..."): translated, the model writes a field or value the code doesn't know.
DATE_FORMAT = re.compile(r'(?<![\w-])(?:YYYY|YY|MM|DD|HH|hh|mm|ss)(?:[-/:.T]?(?:YYYY|YY|MM|DD|HH|hh|mm|ss))+(?![\w-])')
SNAKE = re.compile(r'(?<![\w./-])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![\w-])')
FIELD = re.compile(r'^([a-z]+) (is|must|needs)\b(.*)|\bneeds ([a-z]+):')
ENUM = re.compile(r'(?:^|, |,? or )([a-z]+)(?= \(|,| or |$)')
QUOTED = re.compile(r'["\']([a-z]+)["\']')
NOT_FIELDS = frozenset('it there this that nothing everything something someone none'.split())


def literals(key):
    """The words of an English entry that stay as written: date formats and snake_case names anywhere; in an
    instruction about a field (an entry that starts "<field> is" or "<field> must", or says "needs <field>:" next to a
    date format), the field, its listed values and the quoted ones. "A new board needs stages: ..." is the owner's
    message, so "needs" alone doesn't make a field: a false hit would leave the string in English."""
    out = DATE_FORMAT.findall(key) + SNAKE.findall(key)
    m = FIELD.search(key)
    field = m and (m[1] or (m[4] if DATE_FORMAT.search(key) else None))
    if field and field not in NOT_FIELDS:
        out.append(field)
        # "op is comment, state or create" lists values; "issue is the id or identifier (like ENG-12)" describes one
        if m[2] == 'is' and not re.match(r'(?:the|a|an|one) ', m[3].strip()):
            out += ENUM.findall(m[3].strip().split(':')[0].split(';')[0])
        out += QUOTED.findall(key)
    return list(dict.fromkeys(out))


def literal_problems(key, text):
    missing = [w for w in literals(key) if not re.search(r'(?<![A-Za-z0-9_])' + re.escape(w) + r'(?![A-Za-z0-9_])', text)]
    return [f'keep these exactly as written, the code reads them: {", ".join(missing)}'] if missing else []


# What a translation says the way its English means it, whatever the model made of the words: the owner's Machine is
# Machine (never "The Machine", the product, nor the language's word for a machine), Signal is the app, and a date,
# weekday or 15th reads the language's way. tests/test_translate.py holds every catalog and current article to it.
MACHINE_NOUN = {'de': r'Maschine', 'es': r'\b[mM][aá]quina', 'it': r'\b[mM]acchin', 'pt-BR': r'\b[mM][aá]quina',
                'ru': r'[мМ]ашин', 'zh-CN': r'机器(?!人|学习)', 'ja': r'マシン', 'ko': r'머신|기계', 'fr': r'\bmachine',
                'nl': r'\bmachine'}
OWNED_MACHINE = re.compile(r"\b(?:[Yy]our|[Tt]heir|[Tt]his|[Tt]hat|[Ee]ach|[Ee]very|[Aa]|[Aa]nother|[Hh]is|[Hh]er|[Oo]ne|[Mm]y"
                           r"|[Ss]omeone[’']s) Machine")
EN_DATE = re.compile(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|June|July|August'
                     r'|September|October|November|December)\b'
                     r'|\b(?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) \d{1,2}\b'
                     r'|\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),? \d{1,2}\b|\b\d{1,2}(?::\d\d)? ?(?:am|pm|AM|PM)\b|\b\d{1,2}(?:st|nd|rd|th)\b',
                     re.A)  # ASCII word edges: "Tuesday试点" and "November 14までに" count too
SAME_DATE = {'de': re.compile(r'^(?:April|August|September|November)$|^\d{1,2} am$')}  # German months; "50 am Tag"
DATE_EXAMPLES = frozenset({'2:05 PM', 'Oct 24'})  # the 12-hour and English-region examples a setting shows on purpose


def wording_problems(english, text, lang):
    """What a translated string or article paragraph says another way than its English means ([] when nothing)."""
    out = []
    if 'Machine' in english and not re.search(r'\bmachines?\b|Machinery', english):
        noun = re.search(MACHINE_NOUN.get(lang, '(?!)'), text)
        owned = len(OWNED_MACHINE.findall(english))
        if noun:
            out.append(f'Machine is a name: write Machine, not {noun[0]!r}')
        elif owned and text.count('The Machine') > english.count('The Machine') and len(re.findall(r'(?<!The )Machine', text)) < owned:
            out.append("someone's own Machine is Machine (\"your Machine\"), not The Machine")
    if re.search(r'(?<![\w-])Signal(?![\w-])', english) and not re.search(r'Signal(?![a-zà-ÿ])', text):
        out.append('Signal is the app: keep the name Signal')
    dates = [m[0] for m in EN_DATE.finditer(text)
             if m[0] not in DATE_EXAMPLES and not (lang in SAME_DATE and SAME_DATE[lang].search(m[0]))]
    if dates:
        out.append(f'write dates and weekdays the language\'s way, not {dates[0]!r}')
    return out


def hole_positions(holes):
    """The argument each placeholder fills, sorted: {} in order, {0} {1} by number (None when the two are mixed)."""
    numbered = [h[1:-1] for h in holes if h != '{}']
    if not numbered:
        return [str(i) for i in range(len(holes))]
    return sorted(numbered) if len(numbered) == len(holes) else None


def holes_ok(key, text):
    """The same placeholders as the key: each argument filled as many times ({} may be numbered {0}, {1} to reorder,
    and a key that repeats {0} keeps repeating it)."""
    got = hole_positions(HOLE.findall(text))
    return got is not None and got == hole_positions(HOLE.findall(key))


def string_problems(key, text, lang, words):
    """What is wrong with one translated form of a catalog key, as notes for the model ([] when nothing)."""
    if not isinstance(text, str) or not text.strip():
        return ['empty']
    out = []
    if not holes_ok(key, text):
        out.append('keep every placeholder ({}, or {0} {1} to reorder) exactly as many times as in the English')
    if '—' in text:
        out.append(no_em_dash(text))
    if key in KIND_FIRST and (m := HOLE.search(text)) and m[0] in ('{}', '{0}') and text[:m.start()].strip():
        out.append(f'the first placeholder is the kind of message ("WhatsApp"), not a person: no word before it, so not {text!r}')
    out += literal_problems(key, text)
    out += [f'keep the name "{n}"' for n in words['names'] if re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', key) and n not in text]
    if key not in words['exceptions']:
        out += [f'"{term}" must read one of: {", ".join(forms[lang])}' + TERM_PROBLEM for term, forms in words['checked'].items()
                if lang in forms and term_in(term, key, words['names']) and not any(f.lower() in text.lower() for f in forms[lang])]
    pattern = wrong_gender().get(lang)
    if pattern and re.search(pattern, text):
        out.append(f'The Machine is never masculine here: {words["gender"].get(lang, "")}')
    return out


def entry_problems(key, value, lang, words, english=None):
    """Problems with a whole catalog entry: a string, or a plural entry with exactly lang's forms, of the English's
    shape. catalog_todo counts an entry of another shape as missing, so one let through here is asked for forever."""
    if english is not None and isinstance(english, dict) != isinstance(value, dict):
        if isinstance(english, dict):
            return [f'an object of count forms with exactly these keys: {", ".join(plural_forms(lang))}']
        return ['one plain string, not count forms, even when it holds a count']
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


def source(key, value, means=None):
    """What the model reads for one entry: the English, and as a note what glossary.md says it means (means),
    else the key when it says more ("Close (a closeness)", "{} tickets (to an event)" for a plural entry)."""
    if key in (means or {}):
        return {'english': value, 'meaning': means[key]}
    shown = value.get('other') if isinstance(value, dict) else value
    return {'english': value, 'meaning': key} if shown != key else {'english': value}


def translate_entries(lang, keys, en, words=None, ask=ask):
    """{key: translation} for catalog keys, in batches; an entry whose answer fails its checks twice is left out."""
    words = words or glossary()
    forms = plural_forms(lang)
    what = ('the user interface of a web app, one string each (a button, a label, a status line, a message; '
            'a plural entry is one string per count form)')
    done = {}

    def batch(chunk, notes=None):
        items = {str(i): source(k, en[k], words.get('means')) for i, k in enumerate(chunk)}
        payload = ('Return one JSON object {"t": {"<id>": <translation>}} with every id. Translate each "english" on '
                   'its own; "meaning", when there, says what it is and is not translated. A plain "english" string '
                   'becomes a string, also when it holds a count. An "english" object of count forms (one, other) becomes an object with exactly '
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
    retry = {k: entry_problems(k, done.get(k), lang, words, en[k]) for k in keys}
    retry = {k: p for k, p in retry.items() if p}
    again = {}
    for i in range(0, len(retry), 40):
        chunk = list(retry)[i:i + 40]
        again.update(batch(chunk, {str(n): {'answer': done.get(k), 'fix': retry[k]} for n, k in enumerate(chunk)}))
    for k in retry:
        if entry_problems(k, again.get(k), lang, words, en[k]):
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
FENCE = re.compile(r'^[ \t]*```.*?^[ \t]*```|^[ \t]*~~~.*?^[ \t]*~~~', re.M | re.S)  # a code block, whole
HEADING = re.compile(r'^(#{2,3}) ', re.M)
ITEM = re.compile(r'^(- |\d+\. )', re.M)
CODE_TOKEN = re.compile(r'`§(\d+)`')
FRONT = re.compile(r'---\n(.*?)\n---\n', re.S)
BOLD = re.compile(r'\*\*(.+?)\*\*')
TAIL = re.compile(r'[\s.:：。  ]*$')  # a bold label's closing colon or stop, as the language writes it
ARTICLE_HOLE = re.compile(r'\{[a-z_.0-9]*\}')


def front(text):
    """(ordered [(key, value)] of the front matter, body)."""
    m = FRONT.match(text)
    if not m:
        return [], text
    return [(k.strip(), v.strip()) for k, _, v in (line.partition(':') for line in m[1].splitlines())], text[m.end():]


def blocks(body):
    """Per section: its paragraphs and list items. A translation with other ones than its English is out of date."""
    return [sum(len(b.splitlines()) if re.match(r'(- |\d+\. )', b) else 1 for b in re.split(r'\n\s*\n', part.strip()) if b.strip() and not b.startswith('#'))
            for part in re.split(r'^(?=#{2,3} )', body, flags=re.M)]


def same(pattern, a, b):
    return sorted(pattern.findall(a)) == sorted(pattern.findall(b))


def article_problems(en, tr):
    """What a translation tr does differently from its English en. The site's help (themachine-cloud) shows a
    translation only when its link targets, code and placeholders are the English's too, so this is held to the same:
    the translator checks every answer with it, and help_state counts a translation that fails it as out of date."""
    out = []
    for name, pattern in (('link targets', LINK), ('code in backticks', CODE), ('code blocks', FENCE), ('placeholders', ARTICLE_HOLE)):
        if not same(pattern, en, tr):
            # plain text, not a Python list: its repr doubles every backslash, and the model copies what it reads
            out.append(f'keep the same {name} exactly: {", ".join(sorted(pattern.findall(en)))}')
    if HEADING.findall(en) != HEADING.findall(tr):
        out.append('keep the same ## and ### headings in the same order')
    elif blocks(en) != blocks(tr):
        out.append('keep the same paragraphs and list items in each section, one list item per line, as - or 1.')
    if '—' in tr:
        out.append(no_em_dash(tr))
    return out


def no_em_dash(text, where=''):
    """The em dash note, with where the answer has them: a bare "no em dash" was ignored twice by languages whose own
    typography writes one (Russian "X — это Y"), so the article stayed out of date run after run."""
    spots = [' '.join(text[max(0, m.start() - 40):m.end() + 40].split()) for m in re.finditer('—', text)][:5]
    return (f'no em dash (—){where}: rewrite each of these without it, with a colon, a comma or two sentences '
            f'(no other dash in its place): ' + ' | '.join(f'"{s}"' for s in spots))


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


def body_hash(body):
    return hashlib.sha256(body.strip().encode('utf-8')).hexdigest()[:16]


@functools.lru_cache(maxsize=None)
def stale_bodies():
    """{"<lang>/<article>": the hash of a body} from STALE_BODIES: translations that carry the stamp of their current
    English without being made from it. Until 2026-11-22 an article without a stamp counted as current when git showed
    no change to its English after the translation's last change; a later edit to the translation (a renamed label in
    every language) made one that never followed the English look newer, and it was stamped current. A body listed here
    is out of date; a translation or hand fix changes the body, and then its entry no longer applies."""
    try:
        return json.loads(STALE_BODIES.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def help_state(lang, path, folder=HELP):
    """'missing', 'stale' or 'current' for one article in lang. Current is made from this English: its stamp is the
    English's hash. Without a stamp it is out of date: a hand-made translation goes through the translator too."""
    local = folder / lang / path.name
    if not local.is_file():
        return 'missing'
    fields, body = front(local.read_text(encoding='utf-8'))
    found = dict(fields).get('translated')
    english = front(path.read_text(encoding='utf-8'))[1]
    # Out of step with the English (its sections, paragraphs and list items, link targets, code and code blocks), it is
    # out of date whatever its stamp says: a stamp moved onto an older translation, or one from before these checks.
    # The site's help refuses the same ones, so the next run translates them again.
    if not found or found != stamp(path) or article_problems(english, body):
        return 'stale'
    return 'stale' if stale_bodies().get(f'{lang}/{path.name}') == body_hash(body) else 'current'


def help_todo(langs, folder=HELP):
    """{lang: [(path, state)]} for every article that is not current in lang."""
    return {lang: [(p, s) for p in articles(folder) for s in [help_state(lang, p, folder)] if s != 'current'] for lang in langs}


def label_catalog(lang):
    """lang's catalog and its ambiguous labels: what app_labels reads, once for many articles."""
    catalog = load(lang)
    return catalog, {k[:k.index(' (')] for k in catalog if k.endswith(')') and ' (' in k}


def app_labels(lang, body, known=None):
    """{english label: the app's translation} for every **label** in the article that lang's catalog has, so the
    article names a button the way the app shows it. A label the catalog also has with a context ("Start" and
    "Start (a button)") is left to the model: the bare key may be another meaning (a time field's label). known: label_catalog(lang)."""
    catalog, ambiguous = known or label_catalog(lang)
    out = {}
    for label in BOLD.findall(body):
        bare = label.strip().rstrip('.:')
        if isinstance(catalog.get(bare), str) and not HOLE.search(bare) and bare not in ambiguous:
            out[bare] = catalog[bare]
    return out


ARTICLE_LINK = re.compile(r'\[([^\]]+)\]\(([a-z0-9-]+)\.md(?:#[^)\s]*)?\)')


def units(body):
    """The article's paragraphs and list items, in order: a translation has the same ones (article_problems)."""
    out = []
    for block in re.split(r'\n\s*\n', body.strip()):
        out += block.splitlines() if re.match(r'(- |\d+\. )', block) else [block]
    return out


def fix_units(en, tr, fix):
    """tr with fix(english unit, translated unit) applied to each pair; tr as it is when the units don't pair up."""
    a, b = units(en), units(tr)
    if len(a) != len(b):
        return tr
    out, at = tr, 0
    for e, t in zip(a, b):
        at = out.index(t, at)
        new = fix(e, t)
        out = out[:at] + new + out[at + len(t):]
        at += len(new)
    return out


def fix_labels(en, tr, labels):
    """Each **label** the app has a translation for, written as the app shows it: where a paragraph or list item has
    as many bold parts as its English, the one in the English's place, when the app's text is not in it yet. Cheaper
    and surer than asking again. Only where the bold parts are known to keep the English's order: every one that
    already reads as the app shows a label sits in that label's place, or only one label is missing and none is
    there to go by. A sentence that puts them in another order ("**Suggested for you** at the top of
    **Connections**") is left as it is: the English's place would swap two labels."""
    def fix(e, t):
        want, got = BOLD.findall(e), list(BOLD.finditer(t))
        if len(want) != len(got):
            return t
        bare_en = [w.strip().rstrip('.:') for w in want]
        bare_tr = [TAIL.sub('', g[1].strip()) for g in got]
        todo = [i for i, b in enumerate(bare_en) if b in labels and labels[b] not in bare_tr]
        shown = {labels[b] for b in bare_en if b in labels}
        anchors = [(i, j) for i, b in enumerate(bare_en) if b in labels for j, x in enumerate(bare_tr) if x == labels[b]]
        if not todo or any(bare_tr[i] in shown for i in todo):
            return t
        if not (anchors and all(i == j for i, j in anchors) or not anchors and len(todo) == 1):
            return t
        for i in reversed(todo):
            g = got[i]
            tail = TAIL.search(g[1])[0]  # "Qui :", "誰：" keep their colon as the language writes it
            t = t[:g.start()] + f'**{labels[bare_en[i]]}{tail}**' + t[g.end():]
        return t
    return fix_units(en, tr, fix) if labels else tr


def link_titles(lang, folder=HELP):
    """{slug: (English title, its title in lang)} for each article translated from its current English."""
    out = {}
    for path in articles(folder):
        local = folder / lang / path.name
        if local.is_file():
            fields = dict(front(local.read_text(encoding='utf-8'))[0])
            if fields.get('title') and fields.get('translated') == stamp(path):
                out[path.stem] = (dict(front(path.read_text(encoding='utf-8'))[0]).get('title', ''), fields['title'])
    return out


def fix_links(en, tr, titles):
    """A link whose English text is the target article's title reads as that article's translated title. Only the
    title as written ("See [Writing](writing.md)"): words of a sentence that link to an article ("your
    [history](history.md)") take the sentence's grammar, a case or a plural, in the language."""
    def fix(e, t):
        want = [(m[2], m[1].strip()) for m in ARTICLE_LINK.finditer(e)]
        got = list(ARTICLE_LINK.finditer(t))
        if [s for s, _ in want] != [m[2] for m in got]:
            return t
        for (slug, text), m in reversed(list(zip(want, got))):
            title = titles.get(slug)
            if title and text == title[0].strip() and m[1] != title[1]:
                t = t[:m.start(1)] + title[1] + t[m.end(1):]
        return t
    return fix_units(en, tr, fix) if titles else tr


def translate_article(lang, path, words=None, ask=ask):
    words = words or glossary()
    fields, body = front(path.read_text(encoding='utf-8'))
    fields = dict(fields)
    sent, spans = protect_code(body.strip())
    src = {'title': fields.get('title', ''), 'summary': fields.get('summary', ''), 'body': sent}
    what = 'a help article (Markdown)'
    labels = app_labels(lang, body)
    titles = link_titles(lang, path.parent)
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
        got['body'] = fix_links(body.strip(), fix_labels(body.strip(), restore_code(answer, spans).strip(), labels), titles)
        problems = article_problems(sent, answer) or article_problems(body.strip(), got['body'].strip())
        for k in ('title', 'summary'):
            if src[k]:
                text = got.get(k)
                if not isinstance(text, str) or not text.strip() or '\n' in text.strip():
                    problems.append(f'a one-line {k}')
                elif '—' in text:
                    problems.append(no_em_dash(text, f' in the {k}'))
        # a label not as the app shows it is asked again once; the second time the article is kept anyway. Wording
        # that says another thing than the English is never kept: the catalog test refuses it in a current article.
        wrong = [f'write **{tr}** for {en}' for en, tr in labels.items() if f'**{tr}' not in got['body']]
        pairs = [(src['title'], got.get('title')), (src['summary'], got.get('summary'))] + list(zip(units(body.strip()), units(got['body'])))
        problems += sorted({f'{p} (in {t[:60]!r})' for e, t in pairs if e and isinstance(t, str) for p in wording_problems(e, t, lang)})
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
            # an empty value is "covers:", never "covers: ": the site copies these byte for byte and refuses trailing spaces
            lines.append(f'{k}: {" ".join({"title": title, "summary": summary}.get(k, v).split())}'.rstrip())
    lines.append(f'translated: {stamp(path)}')
    return '---\n' + '\n'.join(lines) + '\n---\n' + body.strip() + '\n'


def run_help(langs, check=False, folder=HELP, ask=ask):
    todo = help_todo(langs, folder)
    left = 0
    for lang in langs:
        gone = sorted(p for p in (folder / lang).glob('*.md') if not (folder / p.name).is_file()) if (folder / lang).is_dir() else []
        counts = {s: sum(1 for _, x in todo[lang] if x == s) for s in ('missing', 'stale')}
        print(f'{lang}: {counts["missing"]} help articles to translate, {counts["stale"]} out of date'
              + (f', {len(gone)} no longer in English' if gone else ''))
        if check:
            left += counts['missing'] + counts['stale'] + len(gone)
            continue
        for old in gone:
            old.unlink()
    if check:
        return left
    words = glossary()
    jobs = [(lang, path) for lang in langs for path, _ in todo[lang]]
    written = []
    with concurrent.futures.ThreadPoolExecutor(WORKERS) as pool:
        futures = {pool.submit(translate_article, lang, path, words, ask): (lang, path) for lang, path in jobs}
        for future in concurrent.futures.as_completed(futures):
            lang, path = futures[future]
            got = future.result()
            if got:
                (folder / lang).mkdir(exist_ok=True)
                (folder / lang / path.name).write_text(article_text(path, got['title'], got['summary'], got['body']), encoding='utf-8')
                written.append((lang, path))
            else:
                left += 1
    align_help(langs, folder)
    return left


def align_help(langs, folder=HELP):
    """Every current translation names **labels** as the catalog now has them and links articles by their titles as
    they now read, also those this run translated: a catalog or title change reaches the articles that use it, without
    the model (tests/test_translate.py holds the articles to it)."""
    for lang in langs:
        titles = link_titles(lang, folder)
        for path in articles(folder):
            local = folder / lang / path.name
            if not local.is_file() or help_state(lang, path, folder) != 'current':
                continue
            text = local.read_text(encoding='utf-8')
            body = front(text)[1].strip()
            en = front(path.read_text(encoding='utf-8'))[1].strip()
            fixed = fix_links(en, fix_labels(en, body, app_labels(lang, en)), titles)
            if fixed != body:
                local.write_text(text.replace(body, fixed, 1), encoding='utf-8')


def problems(langs=None, folder=HELP):
    """What a release would ship untranslated, as lines ([] when everything is translated): for scripts/release.py."""
    langs = langs or languages()
    out, en = [], load('en')
    for lang in langs:
        todo = catalog_todo(lang, en)
        if todo:
            out.append(f'{lang}: {len(todo)} catalog keys not translated (first: {todo[0][:60]!r})')
        for path, state in help_todo([lang], folder)[lang]:
            out.append(f'{lang}: docs/help/{path.name} {"not translated" if state == "missing" else "out of date with its English"}')
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('what', choices=('catalog', 'help', 'all'))
    p.add_argument('--lang', action='append', choices=languages(), help='only this language (repeat for more)')
    p.add_argument('--check', action='store_true', help='count what is missing or out of date, call nothing (exit 1 when something is)')
    p.add_argument('--list', action='store_true', help='with --check and all: one line per language and article left, for scripts/release.py')
    args = p.parse_args(argv)
    langs = args.lang or languages()
    if args.check and args.list and args.what == 'all':
        lines = problems(langs)
        print('\n'.join(lines))
        return 1 if lines else 0
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

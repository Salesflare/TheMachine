"""Server-built text in the owner's language: Telegram, emails, event lines (the catalogs in i18n/, glossary.md).

    t('Snoozed it')                       # 'Gesnoozed' when the owner reads Dutch, the English when there is no entry
    t('{} to-dos', 3)                     # a plural entry: {"one": "{} to-do", "other": "{} to-dos"}
    t('Due {}', when, lang='fr')          # an explicit language (another person's), else locale_prefs.language()

Keys are the English text itself, as in the dashboard (dashboard.html, the i18n script), so English stays the source and
the fallback: a string without an entry reads as written. {} placeholders fill in order; a translation may use {0}, {1}
to reorder them. A plural entry picks its form by the first number among the values (CLDR one/other: the four
languages here all have just those two in UI copy, French and Brazilian Portuguese counting 0 and 1 as one)."""
from __future__ import annotations

import functools
import json
import re
from pathlib import Path

import locale_prefs

FOLDER = Path(__file__).resolve().parent / 'i18n'
_HOLE = re.compile(r'\{(\d*)\}')


@functools.lru_cache(maxsize=None)
def catalog(lang):
    """{english: translation} for one language; {} when there is none (English, or a missing file)."""
    if lang not in locale_prefs.LANGUAGES:
        return {}
    path = FOLDER / f'{lang}.json'
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def plural_form(lang, n):
    """'one' or 'other' for n in lang."""
    try:
        n = abs(float(n))
    except (TypeError, ValueError):
        return 'other'
    if lang in ('fr', 'pt-BR'):
        return 'one' if n < 2 else 'other'
    return 'one' if n == 1 else 'other'


def fill(text, args):
    """{} in order, {0} {1} by position."""
    count = iter(range(len(args)))

    def hole(m):
        i = int(m.group(1)) if m.group(1) else next(count, None)
        return str(args[i]) if i is not None and i < len(args) else m.group(0)
    return _HOLE.sub(hole, text)


def t(text, *args, lang=None):
    """text in the owner's language (or lang), with args filled in."""
    lang = lang or locale_prefs.language()
    found = catalog(lang).get(text) if lang != 'en' else None
    if found is None:
        found = catalog('en').get(text, text)
    if isinstance(found, dict):
        n = next((a for a in args if isinstance(a, (int, float))), None)
        found = found.get(plural_form(lang, n)) or found.get('other') or text
    return fill(found, args)


def language_name(lang=None):
    """'Dutch' for nl: how a prompt names the owner's language."""
    return {'en': 'English', 'nl': 'Dutch', 'fr': 'French', 'de': 'German', 'es': 'Spanish', 'it': 'Italian',
            'pt-BR': 'Brazilian Portuguese'}.get(lang or locale_prefs.language(), 'English')


def written_in(lang=None):
    """What the model writes the owner's own text in, for a prompt: 'US English (organization, color, prioritize)' or
    'Dutch'."""
    lang = lang or locale_prefs.language()
    return 'US English (organization, color, prioritize)' if lang == 'en' else language_name(lang)


def prompt_rule(lang=None):
    """The language line in the review, preparation and chat prompts: drafts to other people in the language of their
    thread, the owner's own text (card titles, summaries, notes, replies to them) in the owner's UI language."""
    return (f'Languages: a draft or message to someone else is in the language of that thread (or what they write to the '
            f'owner in). What the owner reads from you (to-do titles, summaries, bodies, notes, steps, chat replies) is in '
            f'{written_in(lang)}, unless the owner writes to you in another language. Product names stay as they are.')

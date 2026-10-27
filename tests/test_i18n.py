"""Languages (i18n/, i18n.py, glossary.md): the catalogs are complete and follow the glossary, the moved areas of the
dashboard have no English outside the catalog, and server text and dates read in the owner's language."""
import datetime as dt
import json
import pathlib
import re
import sys
import unittest

import i18n
import locale_prefs

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import i18n_extract  # noqa: E402

LANGS = [code for code in locale_prefs.LANGUAGES if code != 'en']
HOLE = re.compile(r'\{\d*\}')


def load(name):
    return json.loads((ROOT / 'i18n' / name).read_text(encoding='utf-8'))


def forms(value):
    return list(value.values()) if isinstance(value, dict) else [value]


def glossary():
    """(names, terms): names stay verbatim; terms {english: {lang: [accepted forms]}}."""
    text = (ROOT / 'i18n' / 'glossary.md').read_text(encoding='utf-8')
    names_part = text.split('## Names', 1)[1].split('## Terms', 1)[0]
    names_line = ' '.join(line for line in names_part.splitlines()[3:] if line.strip())
    names = [re.sub(r'\s*\(.*?\)', '', n).strip() for n in re.sub(r'\(.*?\)', '', names_line).rstrip('.').split(',')]
    table = text.split('## Terms', 1)[1].split('##', 1)[0]
    rows = [[c.strip() for c in line.strip('|').split('|')] for line in table.splitlines() if line.startswith('|')]
    head, terms = rows[0], {}
    for row in rows[2:]:
        terms[row[0]] = {head[i]: [f.strip() for f in row[i].split(',')] for i in range(1, len(head))}
    exceptions = set(re.findall(r'^- `(.+?)`', text.split('## Exceptions', 1)[1].split('##', 1)[0], re.M)) if '## Exceptions' in text else set()
    return [n for n in names if n], terms, exceptions


def term_in(term, english):
    """'to-do' in 'Find a to-do' and 'To-dos', not in 'to-door'; 'snooze' in 'Snoozed'; a capitalized term (a status or
    screen name: Ready) only capitalized; never in a file name (.skill, SKILL.md)."""
    flags = 0 if term[0].isupper() else re.I
    return re.search(r'(?<![\w.-])' + re.escape(term) + r'(?:s|es|d|ed|ing)?(?![\w-]|\.md)', english, flags) is not None


class CatalogTest(unittest.TestCase):
    def test_every_language_has_every_string_with_the_same_placeholders(self):
        en = load('en.json')
        for lang in LANGS:
            cat = load(f'{lang}.json')
            with self.subTest(lang=lang):
                self.assertEqual(sorted(set(en) - set(cat)), [], f'{lang}.json misses these')
                self.assertEqual(sorted(set(cat) - set(en)), [], f'{lang}.json has keys en.json lacks')
                for key, value in cat.items():
                    self.assertEqual(type(value), type(en[key]), key)
                    for form in forms(value):
                        self.assertEqual(len(HOLE.findall(form)), len(HOLE.findall(key)), f'{lang}: {key!r} -> {form!r}')
                        self.assertNotIn('—', form, f'{lang}: no em dashes ({key!r})')

    def test_the_catalogs_follow_the_glossary(self):
        names, terms, exceptions = glossary()
        self.assertIn('Graph', names)
        self.assertIn('to-do', terms)
        en, problems = load('en.json'), []
        for lang in LANGS:
            cat = load(f'{lang}.json')
            for key, value in cat.items():
                if key in exceptions:
                    continue
                text = ' '.join(forms(value))
                for name in names:
                    if re.search(r'(?<![\w-])' + re.escape(name) + r'(?![\w-])', key) and name not in text:
                        problems.append(f'{lang}: keep {name!r} in {key!r} -> {text!r}')
                for term, by_lang in terms.items():
                    if term_in(term, key) and not any(f.lower() in text.lower() for f in by_lang[lang]):
                        problems.append(f'{lang}: {term!r} reads {by_lang[lang][0]!r} in {key!r} -> {text!r}')
        self.assertEqual(problems, [], '\n'.join(problems[:40]))
        self.assertTrue(en)

    def test_the_moved_areas_have_no_english_outside_the_catalog(self):
        # A new string in a moved area: add it with `python3 scripts/i18n_extract.py --add`, translate it in every
        # language, or list it in i18n/not-ui.json when nobody reads it as is.
        self.assertEqual(i18n_extract.missing(), {})


class ServerTextTest(unittest.TestCase):
    def tearDown(self):
        locale_prefs.configure({})

    def test_t_translates_fills_and_falls_back_to_english(self):
        locale_prefs.configure({'language': 'nl'})
        self.assertEqual(i18n.t('Language'), 'Taal')
        self.assertEqual(i18n.t('Language', lang='fr'), 'Langue')
        self.assertEqual(i18n.t('Not in any catalog {}', 3), 'Not in any catalog 3')
        self.assertEqual(i18n.t('Forgot {} saved sign-ins.', 1), '1 opgeslagen login vergeten.')
        self.assertEqual(i18n.t('Forgot {} saved sign-ins.', 2), '2 opgeslagen logins vergeten.')
        self.assertEqual(i18n.t('Forgot {} saved sign-ins.', 1, lang='en'), 'Forgot 1 saved sign-in.')
        self.assertEqual(i18n.fill('{1} then {0}', ['a', 'b']), 'b then a')
        self.assertEqual(i18n.plural_form('fr', 0), 'one')
        self.assertEqual(i18n.plural_form('pt-BR', 0), 'one')
        self.assertEqual(i18n.plural_form('it', 0), 'other')
        self.assertEqual(i18n.t('{} meetings', 2, lang='pt-BR'), '2 reuniões')
        self.assertEqual(i18n.t('{} meetings', 1, lang='it'), '1 riunione')
        self.assertEqual(i18n.language_name(), 'Dutch')
        locale_prefs.configure({})
        self.assertEqual(i18n.t('Language'), 'Language')

    def test_the_digest_reads_in_the_owners_language(self):
        import notify
        locale_prefs.configure({'language': 'nl'})
        out = notify.compose([{'at': '2026-10-27T09:00', 'title': 'Standup', 'guests': []}], [{'title': 'A'}], [{'title': 'B'}, {'title': 'C'}])
        self.assertEqual(out['subject'], 'Je ochtend: 1 afspraak · 1 te doen · 2 nieuw')
        self.assertTrue(out['text'].startswith('Vandaag\n• 09:00 Standup'))
        locale_prefs.configure({})
        self.assertEqual(notify.compose([], [{'title': 'A'}], [])['subject'], 'Your morning: 1 due')

    def test_prompts_ask_for_the_owners_language_and_drafts_in_the_threads(self):
        import assistant
        locale_prefs.configure({'language': 'fr'})
        prompt = assistant.review_prompt('run1', ['mail'])
        self.assertIn('What the owner reads from you (to-do titles, summaries, bodies, notes, steps, chat replies) is in French', prompt)
        self.assertIn('a draft or message to someone else is in the language of that thread', prompt)
        self.assertIn('Write in French.', assistant.import_prompt('run1'))
        locale_prefs.configure({})
        self.assertIn('is in US English (organization, color, prioritize)', assistant.review_prompt('run1', ['mail']))

    def test_dates_read_in_the_owners_language(self):
        moment = dt.datetime(2026, 10, 24, 14, 5)
        expected = {'en': 'Sat 24 Oct at 14:05', 'nl': 'za 24 okt om 14:05', 'fr': 'sam. 24 oct. à 14:05',
                    'de': 'Sa. 24. Okt. um 14:05', 'es': 'sáb 24 oct a las 14:05', 'it': 'sab 24 ott alle 14:05',
                    'pt-BR': 'sáb. 24 de out. às 14:05'}
        for lang, text in expected.items():
            locale_prefs.configure({'locale': 'en-BE', 'language': lang})
            self.assertEqual(locale_prefs.at_text(moment), text)
        self.assertEqual(locale_prefs.view()['date_locale'], 'pt-BR')  # Brazilian dates wherever the owner is
        locale_prefs.configure({'locale': 'en-BE', 'language': 'it'})
        self.assertEqual(locale_prefs.view()['date_locale'], 'it-BE')

    def test_the_language_comes_from_the_choice_then_signup_then_english(self):
        self.assertEqual(locale_prefs.language_of({'language': 'de', 'locale': 'nl-BE'}), 'de')
        self.assertEqual(locale_prefs.language_of({'locale': 'nl-BE'}), 'nl')  # signup's Accept-Language
        self.assertEqual(locale_prefs.language_of({'locale': 'en-BE'}), 'en')
        self.assertEqual(locale_prefs.language_of({'language': 'xx'}), 'en')
        self.assertEqual(locale_prefs.view({'locale': 'en-BE'})['language_set'], False)
        self.assertEqual(locale_prefs.view({'language': 'fr'})['language_set'], True)
        self.assertEqual(locale_prefs.pick_language('nl-BE,nl;q=0.9,en;q=0.8'), 'nl')
        self.assertEqual(locale_prefs.pick_language('en-US,fr;q=0.5'), 'en')
        self.assertEqual(locale_prefs.pick_language('ja,fr-CA;q=0.4,de;q=0.6'), 'de')
        self.assertEqual(locale_prefs.pick_language(['ja', 'es-419']), 'es')
        self.assertEqual(locale_prefs.settings({'language': 'FR'}), {'language': 'fr'})
        self.assertEqual(locale_prefs.settings({'language': 'pt-br'}), {'language': 'pt-BR'})
        # Italian and Brazilian Portuguese; Portuguese from Portugal (or just pt) reads Brazilian for now
        self.assertEqual(locale_prefs.pick_language('it-CH,it;q=0.9'), 'it')
        self.assertEqual(locale_prefs.pick_language('pt-BR,pt;q=0.9'), 'pt-BR')
        self.assertEqual(locale_prefs.pick_language('pt-PT,en;q=0.5'), 'pt-BR')
        self.assertEqual(locale_prefs.pick_language(['pt']), 'pt-BR')
        self.assertEqual(locale_prefs.language_of({'locale': 'pt-BR'}), 'pt-BR')
        self.assertEqual(locale_prefs.language_of({'locale': 'it-IT'}), 'it')
        self.assertEqual(locale_prefs.language_of({'language': 'pt-BR'}), 'pt-BR')
        self.assertEqual(locale_prefs.normalize('pt-BR'), 'pt-BR')
        with self.assertRaises(ValueError):
            locale_prefs.settings({'language': 'xx'})


if __name__ == '__main__':
    unittest.main()

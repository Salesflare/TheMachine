"""People's own questions find the right help section (evals/help-questions/cases.json): the search only, no model."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import help_chat  # noqa: E402
import help_search  # noqa: E402

CASES = json.loads((ROOT / 'evals' / 'help-questions' / 'cases.json').read_text(encoding='utf-8'))['cases']
# Found at the first search when this was written: 96 of all 127, 67 of the 93 English ones. A few less is fine (an
# article edited, its translation a day behind); never lower the floor for a change that finds less.
FLOOR, ENGLISH = 90, 63


class Questions(unittest.TestCase):
    def test_the_search_finds_the_right_section(self):
        helps, missed = {}, {'en': [], 'other': []}
        for case in CASES:
            lang = case['lang']
            if lang not in helps:
                helps[lang] = help_search.Help(help_chat.help_sections(lang=lang), lang)
            found = {s['slug'] + ('#' + s['anchor'] if s['anchor'] else '') for _, s, _, _ in help_chat.fitting(helps[lang].search(case['q']))}
            if not found & set(case['want']):
                missed['en' if lang == 'en' else 'other'].append(case['id'])
        english = sum(c['lang'] == 'en' for c in CASES)
        self.assertGreaterEqual(english - len(missed['en']), ENGLISH, missed['en'])
        self.assertGreaterEqual(len(CASES) - len(missed['en']) - len(missed['other']), FLOOR, missed)

    def test_every_question_names_sections_that_exist(self):
        there = {s['slug'] + ('#' + s['anchor'] if s['anchor'] else '') for s in help_chat.help_sections()}
        for case in CASES:
            self.assertLessEqual(set(case['want']), there, f"{case['id']}: a heading changed? Change it in evals/help-questions/cases.json too")

    def test_every_keyword_line_is_an_articles(self):
        self.assertLessEqual(set(json.loads(help_chat.KEYWORDS.read_text(encoding='utf-8'))), {p.stem for p in help_chat.HELP.glob('*.md')})

    def test_what_goes_in_stays_small(self):
        docs = help_search.Help(help_chat.help_sections())
        for case in CASES:
            if case['lang'] == 'en':
                got = help_chat.fitting(docs.search(case['q']))
                self.assertLessEqual(len(got), help_chat.SECTIONS)
                self.assertLessEqual(sum(len(x[3]) for x in got[1:]) + min(len(got[0][3]), help_chat.HELP_CHARS), help_chat.HELP_CHARS, case['id'])


class Words(unittest.TestCase):
    def test_a_word_answers_for_its_group_once(self):
        section = lambda slug, title, text: {'slug': slug, 'anchor': '', 'title': title, 'heading': '', 'text': text}
        docs = help_search.Help([section('people', 'People', 'Delete a person.'), section('plan', 'Plan', 'Cancel, quit, unsubscribe or end it.'),
                                 *[section(f's{n}', f'Other {n}', 'Nothing about it.') for n in range(8)]])
        self.assertEqual(docs.search('remove a contact')[0][1]['slug'], 'people')
        self.assertEqual(docs.search('stop it and delete a person')[0][1]['slug'], 'people')  # four words for stop aren't four matches

    def test_endings_accents_and_compounds(self):
        self.assertEqual(help_search.stem('stopped'), help_search.stem('stop'))
        self.assertEqual(help_search.stem('replies'), help_search.stem('reply'))
        self.assertEqual(help_search.words('configuracion', 'es'), help_search.words('configuración', 'es'))
        self.assertTrue(set(help_search.words('Benachrichtigung', 'de')) & set(help_search.words('Benachrichtigungen', 'de')))


if __name__ == '__main__':
    unittest.main()

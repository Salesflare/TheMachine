"""The daily translator (scripts/translate.py): what it finds missing, what it sends, what it checks and writes. The
model is a stand-in here; no request leaves the test."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import translate as T  # noqa: E402

ARTICLE = '''---
title: Projects
area: graph
summary: What is going on, on boards.
code: graph.py
order: 4
---
Your Machine names projects. Open **Settings** to change it.

## Add a project

- One `assistant projects` line.
- See [Graph](graph.md).
'''


def no_model(*args, **kwargs):
    raise AssertionError('a check must not call the model')


class Model:
    """Answers like the model: each "english" with a marker, a plural entry with the forms asked for. `bad` keys are
    answered without their placeholders; once in `once` (fixed when asked again), always in `bad`."""

    def __init__(self, bad=(), once=()):
        self.bad, self.once, self.calls = set(bad), set(once), []

    def __call__(self, lang, instruction, payload, cache_key):
        self.calls.append((lang, instruction, payload))
        items = json.loads(payload[payload.index('\n{'):])
        retry = 'Last time' in payload
        out = {}
        for i, item in items.items():
            english = item['english']
            if isinstance(english, dict):
                out[i] = {f: f'[{lang}] {english.get(f, english["other"])}' for f in T.plural_forms(lang)}
                continue
            broken = english in self.bad or english in self.once and not retry
            out[i] = f'[{lang}] ' + (english.replace('{}', '') if broken else english)
        return {'t': out}


class Catalog(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        folder = Path(self.dir.name)
        (folder / 'glossary.md').write_text((ROOT / 'i18n' / 'glossary.md').read_text(encoding='utf-8'), encoding='utf-8')
        en = {'Open {}': 'Open {}', 'Close (a closeness)': 'Close', '{} to-dos': {'one': '{} to-do', 'other': '{} to-dos'},
              'Snooze {} until {}': 'Snooze {} until {}', 'Gone soon': 'Gone soon'}
        (folder / 'en.json').write_text(json.dumps(en), encoding='utf-8')
        (folder / 'nl.json').write_text(json.dumps({'Open {}': 'Open {}', 'Old English': 'Oud'}), encoding='utf-8')
        for name, value in (('CATALOG', folder), ('GLOSSARY', folder / 'glossary.md')):
            patcher = mock.patch.object(T, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.folder = folder

    def test_missing_keys_are_translated_and_gone_ones_dropped(self):
        model = Model()
        self.assertEqual(T.catalog_todo('nl'), ['Close (a closeness)', '{} to-dos', 'Snooze {} until {}', 'Gone soon'])
        self.assertEqual(T.catalog_stale('nl'), ['Old English'])
        self.assertEqual(T.run_catalog(['nl'], ask=model), 0)
        nl = json.loads((self.folder / 'nl.json').read_text(encoding='utf-8'))
        self.assertEqual(nl['Close (a closeness)'], '[nl] Close')
        self.assertEqual(nl['{} to-dos'], {'one': '[nl] {} to-do', 'other': '[nl] {} to-dos'})
        self.assertNotIn('Old English', nl)
        self.assertEqual(nl['Open {}'], 'Open {}', 'what is there stays')
        self.assertEqual((self.folder / 'nl.json').read_text(encoding='utf-8'), T.i18n_extract.canonical(nl), 'sorted, one key per line')
        # the key says what the text is when it says more than the English
        self.assertIn('"meaning": "Close (a closeness)"', model.calls[0][2])
        self.assertIn('Tone and conventions:', model.calls[0][1])

    def test_a_wrong_answer_is_asked_again_once_then_left_in_english(self):
        model = Model(bad={'Snooze {} until {}'}, once={'Open {}'})
        got = T.translate_entries('fr', ['Open {}', 'Snooze {} until {}', 'Gone soon'], json.loads((self.folder / 'en.json').read_text()), ask=model)
        self.assertEqual(got, {'Open {}': '[fr] Open {}', 'Gone soon': '[fr] Gone soon'})
        self.assertEqual(len(model.calls), 2)
        self.assertIn('placeholder', model.calls[1][2])

    def test_a_check_counts_without_the_model(self):
        self.assertEqual(T.run_catalog(['nl'], check=True, ask=no_model), 4)

    def test_plural_forms_follow_the_apps_rules(self):
        self.assertEqual(T.plural_forms('nl'), ('one', 'other'))
        with mock.patch.object(T.i18n, 'plural_form', lambda lang, n: 'other'):
            self.assertEqual(T.plural_forms('ja'), ('other',))
        russian = lambda lang, n: 'other' if n != int(n) else 'one' if n % 10 == 1 and n % 100 != 11 else 'few' if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else 'many'
        with mock.patch.object(T.i18n, 'plural_form', russian):
            self.assertEqual(T.plural_forms('ru'), ('one', 'few', 'many', 'other'))
            # an entry with the European two forms is redone for a language with four
            self.assertEqual(T.catalog_todo('ru', {'{} to-dos': {'one': '{} to-do', 'other': '{} to-dos'}},
                                            {'{} to-dos': {'one': 'a', 'other': 'b'}}), ['{} to-dos'])


class Checks(unittest.TestCase):
    def test_the_glossary_and_the_gender_rules_are_read(self):
        words = T.glossary()
        self.assertIn('Graph', words['names'])
        self.assertIn('to-do', words['checked'])
        self.assertIn('nl', words['gender'])
        self.assertIn('fr', T.wrong_gender())

    def test_an_answer_is_checked_like_the_catalog_test_does(self):
        words = T.glossary()
        self.assertEqual(T.string_problems('Open {}', 'Ouvrir {}', 'fr', words), [])
        self.assertEqual(T.string_problems('{} from {}', '{1} de {0}', 'fr', words), [], 'numbered to reorder')
        self.assertTrue(T.string_problems('{} from {}', '{0} de {0}', 'fr', words))
        self.assertTrue(T.string_problems('Open the Graph', 'Ouvrir le graphe', 'fr', words), 'a name stays')
        self.assertTrue(T.string_problems('Snooze it', 'Faites-le', 'fr', words), 'a glossary term')
        self.assertTrue(T.string_problems('Done', 'Fait — oui', 'fr', words), 'no em dash')
        self.assertTrue(T.string_problems('Your Machine is ready', 'Le Machine est prêt', 'fr', words), 'The Machine is she')


class Help(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.help = Path(self.dir.name) / 'help'
        (self.help / 'nl').mkdir(parents=True)
        (self.help / 'projects.md').write_text(ARTICLE, encoding='utf-8')
        self.history = mock.Mock(changed_after=lambda en, tr: None)

    def answer(self, body=None):
        def ask(lang, instruction, payload, cache_key):
            src = json.loads(payload[payload.index('\n{'):])
            return {'title': 'Projecten', 'summary': 'Wat er speelt.', 'body': body if body is not None else src['body'].replace('Your', 'Je')}
        return ask

    def test_a_missing_article_is_translated_with_the_english_front_matter_and_a_stamp(self):
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'missing')
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer(), history=self.history), 0)
        text = (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\ntitle: Projecten\narea: graph\nsummary: Wat er speelt.\ncode: graph.py\norder: 4\n'
                                        f'translated: {T.stamp(self.help / "projects.md")}\n---\nJe Machine'), text)
        self.assertIn('`assistant projects`', text, 'code is put back as it was')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'current')
        # the English changes: out of date until translated again
        (self.help / 'projects.md').write_text(ARTICLE.replace('names projects', 'names your projects'), encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'stale')
        self.assertEqual(T.run_help(['nl'], check=True, folder=self.help, ask=no_model, history=self.history), 1)

    def test_an_answer_that_loses_structure_is_left_out(self):
        broken = 'Je Machine.\n\n## Een project\n\n- Een regel.'
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer(broken), history=self.history), 1)
        self.assertFalse((self.help / 'nl' / 'projects.md').exists())

    def test_a_translation_from_before_stamps_counts_by_history(self):
        old = ARTICLE.replace('title: Projects', 'title: Projecten')
        (self.help / 'nl' / 'projects.md').write_text(old, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'unstamped', 'no history: same headings')
        later = mock.Mock(changed_after=lambda en, tr: True)
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, later), 'stale')
        # a run stamps it without asking the model
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=no_model, history=self.history), 0)
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'current')
        self.assertIn('title: Projecten', (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8'))

    def test_a_translation_out_of_step_with_the_english_is_out_of_date_whatever_its_stamp(self):
        # a list item short of the English: stamped or not, the next run translates it again
        short = ARTICLE.replace('title: Projects', 'title: Projecten').replace('\n- ', '\n', 1)
        self.assertNotEqual(T.blocks(T.front(short)[1]), T.blocks(T.front(ARTICLE)[1]))
        (self.help / 'nl' / 'projects.md').write_text(short, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'stale')
        stamped = short.replace('\n---\n', f'\ntranslated: {T.stamp(self.help / "projects.md")}\n---\n', 1)
        (self.help / 'nl' / 'projects.md').write_text(stamped, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help, self.history), 'stale')
        self.assertEqual(T.problems(['nl'], self.help)[-1], 'nl: docs/help/projects.md out of date with its English')

    def test_an_article_english_no_longer_has_goes(self):
        (self.help / 'nl' / 'gone.md').write_text(ARTICLE, encoding='utf-8')
        T.run_help(['nl'], folder=self.help, ask=self.answer(), history=self.history)
        self.assertFalse((self.help / 'nl' / 'gone.md').exists())

    def test_the_help_check_accepts_the_stamp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('help_check', ROOT / 'scripts' / 'help_check.py')
        help_check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(help_check)
        T.run_help(['nl'], folder=self.help, ask=self.answer(), history=self.history)
        found = {'projects': help_check.front(ARTICLE), 'graph': ({}, '')}
        self.assertEqual([p for p in help_check.check_translations(found, self.help) if p.startswith('docs/help/nl/')], [])


if __name__ == '__main__':
    unittest.main()

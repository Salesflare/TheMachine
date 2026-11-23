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

    def test_an_answer_of_another_shape_than_the_english_is_asked_again_never_written(self):
        # Russian's model answered the plain "{} tickets" with count forms: let through, catalog_todo still counted it
        # missing, so every run asked again and the daily run stayed red
        en = {'{} tickets': '{} tickets', '{} guests': {'one': '{} guest', 'other': '{} guests'}}
        forms = T.plural_forms('ru')

        def model(fixes):
            def ask(lang, instruction, payload, cache_key):
                retry = 'Last time' in payload
                items = json.loads(payload[payload.index('\n{'):])
                out = {}
                for i, item in items.items():
                    plain = isinstance(item['english'], str)
                    wrong = not retry or not fixes
                    out[i] = ({f: 'x {}' for f in forms} if plain else 'x {}') if wrong else ('x {}' if plain else {f: 'x {}' for f in forms})
                return {'t': out}
            return ask

        got = T.translate_entries('ru', list(en), en, ask=model(fixes=True))
        self.assertEqual(got, {'{} tickets': 'x {}', '{} guests': {f: 'x {}' for f in forms}})
        self.assertEqual(T.catalog_todo('ru', en, got), [])
        self.assertEqual(T.translate_entries('ru', list(en), en, ask=model(fixes=False)), {}, 'left in English, not written')
        words = T.glossary()
        self.assertTrue(T.entry_problems('{} tickets', {f: 'x {}' for f in forms}, 'ru', words, '{} tickets'))
        # a plural entry's key says what it counts, as a plain one's does: tickets to an event, not support tickets
        tickets = {'one': '{} ticket', 'other': '{} tickets'}
        self.assertEqual(T.source('{} tickets (to an event)', tickets), {'english': tickets, 'meaning': '{} tickets (to an event)'})
        self.assertEqual(T.source('{} guests', {'one': '{} guest', 'other': '{} guests'}), {'english': {'one': '{} guest', 'other': '{} guests'}})
        for lang in ('zh-CN', 'ja', 'ko'):  # one count form: a plural entry answered with a bare string
            self.assertTrue(T.entry_problems('{} guests', 'x {}', lang, words, en['{} guests']), lang)
            self.assertEqual(T.entry_problems('{} guests', {'other': 'x {}'}, lang, words, en['{} guests']), [], lang)

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

    def test_every_request_says_how_buttons_read_in_its_language(self):
        # a button translated word for word ("Haal je Machine" for "Get your Machine"): each request carries the
        # glossary's button rule and the language's own verbs, so short UI copy reads the way a native app says it
        words = T.glossary()
        self.assertIn('native', words['button_rule'])
        self.assertNotIn('scripts/translate.py', words['button_rule'])
        self.assertEqual(sorted(words['buttons']), sorted(T.languages()))
        nl = T.instructions('nl', ['Get the phone app'], 'app strings', words)
        self.assertIn(words['button_rule'], nl)
        self.assertIn('Never Haal je', nl)
        self.assertNotIn('Lancer votre Machine', nl)  # only its own language's row
        self.assertIn('开通你的Machine', T.instructions('zh-CN', ['Get it'], 'app strings', words))

    def test_an_answer_is_checked_like_the_catalog_test_does(self):
        words = T.glossary()
        self.assertEqual(T.string_problems('Open {}', 'Ouvrir {}', 'fr', words), [])
        self.assertEqual(T.string_problems('{} from {}', '{1} de {0}', 'fr', words), [], 'numbered to reorder')
        self.assertTrue(T.string_problems('{} from {}', '{0} de {0}', 'fr', words))
        key = 'Connect {0}? {1} emails from {0} this month.'
        self.assertEqual(T.string_problems(key, '{0} koppelen? {1} e-mails van {0} deze maand.', 'nl', words), [],
                         'a key that repeats {0} repeats it')
        self.assertEqual(T.string_problems(key, '{1} e-mails van {0} deze maand: {0} koppelen?', 'nl', words), [])
        self.assertTrue(T.string_problems(key, '{0} koppelen? {1} e-mails deze maand.', 'nl', words), 'one {0} dropped')
        self.assertTrue(T.string_problems(key, '{} koppelen? {} e-mails van {} deze maand.', 'nl', words), 'no third arg')
        self.assertTrue(T.string_problems(key, '{0} koppelen? {1} e-mails van {1} deze maand.', 'nl', words))
        self.assertTrue(T.string_problems('Open the Graph', 'Ouvrir le graphe', 'fr', words), 'a name stays')
        self.assertTrue(T.string_problems('Snooze it', 'Faites-le', 'fr', words), 'a glossary term')
        self.assertTrue(T.string_problems('Done', 'Fait — oui', 'fr', words), 'no em dash')
        self.assertTrue(T.string_problems('Your Machine is ready', 'Le Machine est prêt', 'fr', words), 'The Machine is she')

    def test_what_code_or_a_model_reads_stays_as_written(self):
        # field names, op values and date formats in an instruction for a model: translated, the code can't read them
        words = T.glossary()
        self.assertEqual(T.string_problems('op is create, update or delete', 'op ist create, update oder delete', 'de', words), [])
        self.assertEqual(T.string_problems('op is create, update or delete', 'op: aanmaken, bijwerken of verwijderen', 'nl', words),
                         ['keep these exactly as written, the code reads them: create, update, delete'])
        self.assertTrue(T.string_problems('due is YYYY-MM-DD', 'due is JJJJ-MM-DD', 'nl', words))
        self.assertTrue(T.string_problems('A refund needs due: the last day, as YYYY-MM-DD', 'Un reembolso necesita una fecha: el último día, en YYYY-MM-DD', 'es', words))
        self.assertEqual(T.string_problems('due must be YYYY-MM-DD', 'dueはYYYY-MM-DD形式です', 'ja', words), [], 'next to CJK text')
        self.assertEqual(T.literals('A new board needs stages: 2 to 7 names'), [], "the owner's message, not a field")
        self.assertEqual(T.literals('it is a key'), [])
        self.assertEqual(T.literals('Use salesforce_broker in config.json'), ['salesforce_broker'])


class Help(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.help = Path(self.dir.name) / 'help'
        (self.help / 'nl').mkdir(parents=True)
        (self.help / 'projects.md').write_text(ARTICLE, encoding='utf-8')
        patcher = mock.patch.object(T, 'STALE_BODIES', Path(self.dir.name) / 'stale.json')
        patcher.start()
        self.addCleanup(patcher.stop)
        T.stale_bodies.cache_clear()
        self.addCleanup(T.stale_bodies.cache_clear)

    def answer(self, body=None):
        def ask(lang, instruction, payload, cache_key):
            src = json.loads(payload[payload.index('\n{'):])
            return {'title': 'Projecten', 'summary': 'Wat er speelt.', 'body': body if body is not None else src['body'].replace('Your', 'Je')}
        return ask

    def test_a_label_with_two_meanings_in_the_catalog_is_not_forced(self):
        # "Start" is a time field's label, "Start (a button)" the button: the bare key must not name the button
        cat = {'Start': 'Beginn', 'Start (a button)': 'Starten', 'Stop': 'Stoppen'}
        with mock.patch.object(T, 'load', lambda lang: cat):
            self.assertEqual(T.app_labels('de', '- **Stop**: nothing comes in until you press **Start**.'), {'Stop': 'Stoppen'})

    def test_a_missing_article_is_translated_with_the_english_front_matter_and_a_stamp(self):
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'missing')
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer()), 0)
        text = (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\ntitle: Projecten\narea: graph\nsummary: Wat er speelt.\ncode: graph.py\norder: 4\n'
                                        f'translated: {T.stamp(self.help / "projects.md")}\n---\nJe Machine'), text)
        self.assertIn('`assistant projects`', text, 'code is put back as it was')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'current')
        # the English changes: out of date until translated again
        (self.help / 'projects.md').write_text(ARTICLE.replace('names projects', 'names your projects'), encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'stale')
        self.assertEqual(T.run_help(['nl'], check=True, folder=self.help, ask=no_model), 1)

    def test_an_empty_front_matter_value_is_written_without_a_trailing_space(self):
        # "covers: " broke the site's whitespace check, which copies these files byte for byte
        (self.help / 'projects.md').write_text(ARTICLE.replace('code: graph.py', 'covers:\ncode: graph.py'), encoding='utf-8')
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer()), 0)
        text = (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8')
        self.assertIn('\ncovers:\ncode: graph.py\n', text)
        self.assertEqual([line for line in text.split('\n---\n')[0].split('\n') if line != line.rstrip()], [])

    def test_an_answer_that_loses_structure_is_left_out(self):
        broken = 'Je Machine.\n\n## Een project\n\n- Een regel.'
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer(broken)), 1)
        self.assertFalse((self.help / 'nl' / 'projects.md').exists())

    def test_wording_the_catalog_test_refuses_is_asked_again_then_left_out(self):
        # The second answer was once kept anyway, and the pull request's own tests refused the article it wrote.
        payloads = []

        def ask(lang, instruction, payload, cache_key):
            payloads.append(payload)
            src = json.loads(payload[payload.index('\n{'):])
            return {'title': 'Projecten', 'summary': 'Wat er speelt.', 'body': src['body'].replace('Your Machine', 'The Machine')}
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=ask), 1)
        self.assertEqual(len(payloads), 2)
        self.assertIn('not The Machine (in \'The Machine names projects.', payloads[1])
        self.assertFalse((self.help / 'nl' / 'projects.md').exists())

    def test_an_em_dash_is_asked_again_with_where_it_is(self):
        # A bare "no em dash" was ignored twice in a row (a language whose typography writes one), so the article stayed
        # out of date run after run: the second ask quotes the spots and says what to write instead.
        payloads = []

        def ask(lang, instruction, payload, cache_key):
            payloads.append(payload)
            src = json.loads(payload[payload.index('\n{'):])
            body = src['body'].replace('Your Machine names', 'Je Machine — benoemt' if len(payloads) == 1 else 'Je Machine benoemt')
            return {'title': 'Projecten', 'summary': 'Wat er speelt.', 'body': body}
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=ask), 0)
        self.assertEqual(len(payloads), 2)
        self.assertIn('"Je Machine — benoemt projects.', payloads[1])
        self.assertIn('a colon, a comma or two sentences', payloads[1])
        self.assertNotIn('—', (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8'))

    def test_a_translation_without_a_stamp_is_out_of_date(self):
        # A run once stamped these current when git showed the translation changed after its English; an edit to the
        # translation alone (a label renamed in every language) made one that never followed the English look newer.
        old = ARTICLE.replace('title: Projects', 'title: Projecten')
        (self.help / 'nl' / 'projects.md').write_text(old, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'stale')
        self.assertEqual(T.run_help(['nl'], check=True, folder=self.help, ask=no_model), 1)
        self.assertEqual(T.run_help(['nl'], folder=self.help, ask=self.answer()), 0)
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'current')

    def test_a_body_listed_as_stale_is_out_of_date_until_it_changes(self):
        T.run_help(['nl'], folder=self.help, ask=self.answer())
        local = self.help / 'nl' / 'projects.md'
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'current')
        T.STALE_BODIES.write_text(json.dumps({'nl/projects.md': T.body_hash(T.front(local.read_text(encoding='utf-8'))[1])}))
        T.stale_bodies.cache_clear()
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'stale', 'its stamp is current, its body is not')
        # translated again (or fixed by hand), the body is another one: current
        def again(lang, instruction, payload, cache_key):
            return {**self.answer()(lang, instruction, payload, cache_key), 'title': 'Projecten opnieuw'}
        T.run_help(['nl'], folder=self.help, ask=lambda *a: {**again(*a), 'body': again(*a)['body'].replace('Je', 'Jouw')})
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'current')

    def test_labels_and_link_texts_are_put_right_in_the_answer(self):
        # the model wrote its own word for a label and for a linked article's title: fixed without asking again
        (self.help / 'graph.md').write_text('---\ntitle: Graph\narea: graph\nsummary: People.\n---\nPeople.\n', encoding='utf-8')
        (self.help / 'nl' / 'graph.md').write_text('---\ntitle: Grafiek\narea: graph\nsummary: Mensen.\ntranslated: '
                                                    + T.stamp(self.help / 'graph.md') + '\n---\nMensen.\n', encoding='utf-8')
        calls = []

        def ask(lang, instruction, payload, cache_key):
            calls.append(payload)
            src = json.loads(payload[payload.index('\n{'):])
            body = src['body'].replace('Your', 'Je').replace('**Settings**', '**Opties**').replace('[Graph]', '[Netwerk]')
            return {'title': 'Projecten', 'summary': 'Wat er speelt.', 'body': body}
        with mock.patch.object(T, 'load', lambda lang: {'Settings': 'Instellingen'}):
            self.assertEqual(T.run_help(['nl'], folder=self.help, ask=ask), 0)
        text = (self.help / 'nl' / 'projects.md').read_text(encoding='utf-8')
        self.assertIn('**Instellingen**', text)
        self.assertIn('[Grafiek](graph.md)', text)
        self.assertEqual(len(calls), 1, 'no second ask')

    def test_fixes_leave_other_bold_and_link_text_alone(self):
        en = 'Open **Settings**, then **Save**. See [the graph page](graph.md).'
        tr = 'Open **Opties** en daarna **Bewaar**. Zie [de grafiekpagina](graph.md).'
        self.assertEqual(T.fix_labels(en, tr, {'Settings': 'Instellingen'}),
                         'Open **Instellingen** en daarna **Bewaar**. Zie [de grafiekpagina](graph.md).')
        self.assertEqual(T.fix_links(en, tr, {'graph': ('Graph', 'Grafiek')}), tr, 'the link text is not the title')
        self.assertEqual(T.fix_labels(en, 'Open **Opties**.', {'Settings': 'Instellingen'}), 'Open **Opties**.',
                         'another number of bold parts: not guessed')

    def test_a_translation_out_of_step_with_the_english_is_out_of_date_whatever_its_stamp(self):
        # a list item short of the English: stamped or not, the next run translates it again
        short = ARTICLE.replace('title: Projects', 'title: Projecten').replace('\n- ', '\n', 1)
        self.assertNotEqual(T.blocks(T.front(short)[1]), T.blocks(T.front(ARTICLE)[1]))
        (self.help / 'nl' / 'projects.md').write_text(short, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'stale')
        stamped = short.replace('\n---\n', f'\ntranslated: {T.stamp(self.help / "projects.md")}\n---\n', 1)
        (self.help / 'nl' / 'projects.md').write_text(stamped, encoding='utf-8')
        self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), 'stale')
        self.assertEqual(T.problems(['nl'], self.help)[-1], 'nl: docs/help/projects.md out of date with its English')

    def test_a_translation_with_other_links_or_code_is_out_of_date_whatever_its_stamp(self):
        # the site's help refuses these (themachine-cloud tests/test_help.py), so the next run translates them again
        good = ARTICLE.replace('title: Projects', 'title: Projecten').replace('Your Machine names', 'Je Machine noemt')
        stamp = f'\ntranslated: {T.stamp(self.help / "projects.md")}\n---\n'
        dropped_link = good.replace('See [Graph](graph.md).', 'Zie Graph.')
        extra_code = good.replace('Open **Settings**', 'Open **Settings** (`assistant settings`)')
        extra_block = good.replace('to change it.', 'to change it.\n\n```\nassistant settings\n```', 1)
        for name, text, state in (('correct', good, 'current'), ('a dropped link', dropped_link, 'stale'),
                                  ('an extra code span', extra_code, 'stale'), ('an extra code block', extra_block, 'stale')):
            with self.subTest(name):
                (self.help / 'nl' / 'projects.md').write_text(text.replace('\n---\n', stamp, 1), encoding='utf-8')
                self.assertEqual(T.help_state('nl', self.help / 'projects.md', self.help), state)
                self.assertEqual(T.run_help(['nl'], check=True, folder=self.help, ask=no_model),
                                 int(state == 'stale'))
        both = dropped_link.replace('Open **Settings**', 'Open **Settings** (`assistant settings`)')
        problems = T.article_problems(T.front(ARTICLE)[1], T.front(both)[1])
        self.assertEqual([p.split(':')[0] for p in problems], ['keep the same link targets exactly', 'keep the same code in backticks exactly'])

    def test_an_article_english_no_longer_has_goes(self):
        (self.help / 'nl' / 'gone.md').write_text(ARTICLE, encoding='utf-8')
        T.run_help(['nl'], folder=self.help, ask=self.answer())
        self.assertFalse((self.help / 'nl' / 'gone.md').exists())

    def test_the_help_check_accepts_the_stamp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('help_check', ROOT / 'scripts' / 'help_check.py')
        help_check = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(help_check)
        T.run_help(['nl'], folder=self.help, ask=self.answer())
        found = {'projects': help_check.front(ARTICLE), 'graph': ({}, '')}
        self.assertEqual([p for p in help_check.check_translations(found, self.help) if p.startswith('docs/help/nl/')], [])


class Wording(unittest.TestCase):
    def test_labels_in_another_order_than_the_english_are_left_alone(self):
        # "**Suggested for you** at the top of **Connections**" put the other way round: the English's place would swap them
        en = '**Suggested for you** at the top of **Connections**.'
        tr = 'Oben unter **Verbindungen** steht **Vorschläge**.'
        labels = {'Suggested for you': 'Für dich vorgeschlagen', 'Connections': 'Verbindungen'}
        self.assertEqual(T.fix_labels(en, tr, labels), tr)
        self.assertEqual(T.fix_labels('**Who:** their name.', '**Wer :** ihr Name.', {'Who': '誰'}), '**誰 :** ihr Name.',
                         'the colon as the language writes it')

    def test_a_link_in_running_text_keeps_the_sentences_grammar(self):
        en = 'See your [history](history.md) or [History](history.md).'
        tr = 'Смотрите в вашей [истории](history.md) или [История](history.md).'
        self.assertEqual(T.fix_links(en, tr, {'history': ('History', 'История писем')}),
                         'Смотрите в вашей [истории](history.md) или [История писем](history.md).')

    def test_a_field_described_not_listed_keeps_only_its_name(self):
        self.assertEqual(T.literals('issue is the id or identifier (like ENG-12) of a Linear issue'), ['issue'])
        self.assertEqual(T.literals('op is comment, state, assign or create'), ['op', 'comment', 'state', 'assign', 'create'])

    def test_machine_signal_and_dates_read_as_the_english_means_them(self):
        ok = T.wording_problems
        self.assertTrue(ok('Your Machine reads it.', 'The Machine liest es.', 'de'), "someone's own Machine")
        self.assertEqual(ok('Your Machine reads it.', 'Deine Machine liest es.', 'de'), [])
        self.assertEqual(ok('The Machine has no AI of its own.', 'The Machine hat keine eigene KI.', 'de'), [], 'the product')
        self.assertTrue(ok('Your Machine reads it.', 'Твоя машина читает.', 'ru'), 'the common noun')
        self.assertTrue(ok('Dana asked on Signal.', 'Dana ha chiesto su Segnale.', 'it'))
        self.assertEqual(ok('Signal chats', 'Signal-Chats', 'de'), [])
        self.assertTrue(ok('Pay by November 14', 'November 14までに支払う', 'ja'))
        self.assertTrue(ok('Pilot call Tuesday', 'Tuesday试点通话', 'zh-CN'))
        self.assertEqual(ok('Pay by November 14', 'Bis 14. November bezahlen', 'de'), [], 'the same word in German')
        self.assertEqual(ok('Like 2:05 PM', 'Wie 2:05 PM', 'de'), [], "a setting's example")



class Translations(unittest.TestCase):
    """The catalogs and every current help article, in every language: what code reads stays as written, the owner's
    Machine, Signal and dates read as the English means them, and labels and article links read as the app and the
    linked article's title do (scripts/translate.py align_help keeps them so after a catalog change)."""

    langs = T.languages()
    maxDiff = None

    def test_catalogs(self):
        en, wrong = T.load('en'), []
        for lang in self.langs:
            for key, value in T.load(lang).items():
                english = en.get(key, key)
                english = ' '.join(english.values()) if isinstance(english, dict) else english
                for form in value.values() if isinstance(value, dict) else [value]:
                    if isinstance(form, str):
                        wrong += [f'{lang}: {key[:60]!r}: {p}' for p in T.literal_problems(key, form) + T.wording_problems(english, form, lang)]
        self.assertEqual(wrong, [])

    def test_current_help_articles(self):
        wrong = []
        for lang in self.langs:
            titles, known = T.link_titles(lang), T.label_catalog(lang)
            for path in T.articles():
                local = T.HELP / lang / path.name
                if not local.is_file() or T.help_state(lang, path) != 'current':
                    continue
                ef, en = T.front(path.read_text(encoding='utf-8'))
                tf, tr = T.front(local.read_text(encoding='utf-8'))
                en, tr, ef, tf = en.strip(), tr.strip(), dict(ef), dict(tf)
                where = f'docs/help/{lang}/{path.name}'
                fixed = T.fix_links(en, T.fix_labels(en, tr, T.app_labels(lang, en, known)), titles)
                wrong += [f'{where}: {a[:80]!r} should read {b[:80]!r}' for a, b in zip(T.units(tr), T.units(fixed)) if a != b]
                pairs = [(ef.get(k, ''), tf.get(k, '')) for k in ('title', 'summary')] + list(zip(T.units(en), T.units(tr)))
                wrong += [f'{where}: {t[:80]!r}: {p}' for e, t in pairs if e for p in T.wording_problems(e, t, lang)]
        self.assertEqual(wrong, [])


if __name__ == '__main__':
    unittest.main()

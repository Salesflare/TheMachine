"""People's own questions find the right help section (evals/help-questions/cases.json): the search only, no model."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import help_chat  # noqa: E402
import help_search  # noqa: E402

spec = importlib.util.spec_from_file_location('help_questions_run', ROOT / 'evals' / 'help-questions' / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
CASES = run.load()
# Found at the first search when this was written: 318 of all 399, 132 of the 161 English ones. A few less is fine (an
# article edited, its translation a day behind); never lower the floor for a change that finds less.
FLOOR, ENGLISH = 310, 128


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

    def test_to_do_is_one_word(self):
        for said in ('to-do', 'to-dos', 'to-do’s', 'ToDo', 'todo', '同僚のToDoを'):
            self.assertIn('todo', help_search.words(said), said)
        self.assertEqual(help_search.words('to do'), [])
        self.assertEqual(help_search.words('back-ups'), help_search.words('backups'))

    def test_peoples_own_words_in_every_language(self):
        """Sharing a to-do with a colleague, and the backups, in the words people use: nobody asks for a "teammate" to "hand off" to."""
        helps = {lang: help_search.Help(help_chat.help_sections(lang=lang), lang) for lang in ('en', *json.loads(help_search.LOCAL.read_text(encoding='utf-8')))}
        self.assertEqual(set(helps), {'en', *(p.name for p in help_chat.HELP.iterdir() if p.is_dir())})
        for lang, share, backups in (
                ('en', 'how do I share a to-do with a colleague', 'where are my backups kept and can you open them'),
                ('nl', 'hoe deel ik een to-do met een collega', 'waar staan mijn back-ups en kunnen jullie ze openen'),
                ('de', 'Wie kann ich eine Aufgabe an einen Kollegen weitergeben?', 'Wo liegen meine Backups und könnt ihr sie öffnen?'),
                ('fr', 'comment partager une tâche avec un collègue', 'où sont mes sauvegardes et pouvez-vous les ouvrir'),
                ('es', '¿Cómo comparto una tarea con un compañero?', '¿dónde se guardan mis copias de seguridad?'),
                ('it', 'posso delegare un’attività a un collega', 'dove sono i miei backup e potete aprirli'),
                ('pt-BR', 'como compartilho uma tarefa com um colega', 'onde ficam meus backups e vocês podem abri-los'),
                ('ru', 'как передать задачу коллеге', 'где хранятся мои резервные копии'),
                ('zh-CN', '怎么把待办分享给同事', '我的备份存放在哪里'),
                ('ja', '同僚とToDoを共有するには', 'バックアップはどこに保存されますか'),
                ('ko', '동료와 할 일을 어떻게 공유하나요', '백업은 어디에 보관되나요')):
            found = lambda q: {(s['slug'], s['anchor']) for _, s, _, _ in help_chat.fitting(helps[lang].search(q))}
            self.assertTrue(found(share) & {('handoffs', ''), ('handoffs', 'hand-off-a-to-do'), ('handoffs', 'what-they-see'),
                                            ('common-questions', 'share-a-to-do')}, (lang, found(share)))
            self.assertIn(('security-and-privacy', 'backups'), found(backups), lang)

        for lang, later in (('en', 'how do I send an email later'), ('nl', 'kan ik een mail later versturen'), ('de', 'Kann ich eine E-Mail für morgen früh planen?'),
                            ('fr', 'puis-je programmer l’envoi d’un mail demain matin'), ('ru', 'можно отправить письмо позже')):
            self.assertIn('send-later', {s['slug'] for _, s, _, _ in help_chat.fitting(helps[lang].search(later))}, lang)
        found = {(s['slug'], s['anchor']) for _, s, _, _ in help_chat.fitting(helps['en'].search('can I schedule an email for tomorrow morning'))}
        self.assertIn(('send-later', 'schedule-a-message'), found)


if __name__ == '__main__':
    unittest.main()

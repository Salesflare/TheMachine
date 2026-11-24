"""The draft check reads a draft's marks in every language The Machine ships: a placeholder by where its bracket stands,
a sentence's end by its script's own mark, a name under a closing by its letters. It was English and ASCII: it refused
"Gracias por todo" and a handoff ending in 。, and let "Hallo [Vorname]" through."""
import json
import unittest
from pathlib import Path

import next_actions as n
from machine import draft_marks as d

LANGUAGES = {p.stem for p in (Path(__file__).resolve().parent.parent / 'i18n').glob('*.json')} - {'not-ui'}

# language: (drafts with a placeholder left in: each one's bracket, a finished draft, a finished handoff, one that runs on, closing and name)
TABLE = {
    'en': (['Hi [First name],\n\nok', 'I work at [Your company].', 'About [client name]: see you', 'Best,\n[Your name]'],
           'Hi Kim,\n\nThe room is still TBD, I’ll tell you Friday. My to-do app helps.\n\nBest,\nEva',
           'Can you call them? Thanks! 🙏', 'can you call them by friday', 'Regards,\nJean de Wit'),
    'nl': (['Dag [naam],\n\nok', 'Ik werk bij [Uw bedrijf].', 'Groeten,\n[Uw naam]'], 'Tot straks xxx', 'Kan je hen bellen? 😊',
           'kan je hen bellen voor vrijdag', 'Groeten,\nJan van der Berg'),
    'fr': (['Bonjour [prénom],\n\nok', 'À propos de [nom du client], oui.', 'Cordialement,\n[Votre nom]'], 'Bonjour Léa,\n\nC’est fait.',
           'Peux-tu les appeler ?', 'peux-tu les appeler', 'Cordialement,\nÉlise'),
    'de': (['Hallo [Vorname],\n\nok', 'Hallo [Name einsetzen],', 'Viele Grüße\n[Ihr Name]'], 'Hallo Jörg,\n\nalles erledigt.',
           'Kannst du sie anrufen? Es ist „dringend.“', 'kannst du sie anrufen', 'Viele Grüße,\nÄnne Maria Müller'),
    'es': (['Hola [nombre]:\n\nok', 'Trabajo en [su empresa].', 'Un saludo,\n[Tu nombre]'], 'Hola Ana,\n\nGracias por todo. Nos vemos el lunes.',
           '¡Gracias por todo!', 'puedes llamarlos', 'Un saludo,\nMaría de la Cruz'),
    'it': (['Ciao [nome],\n\nok', 'Lavoro in [la tua azienda].'], 'Ciao Anna,\n\nTutto fatto: grazie di tutto xxx', 'Puoi chiamarli?',
           'puoi chiamarli entro venerdì', 'Saluti,\nÈlia Rossi'),
    'pt-BR': (['Olá [nome],\n\nok', 'Sobre [nome do cliente], sim.'], 'Olá Ana,\n\nVou estar fora todo o dia.\n\nAbraço,\nEva',
              'Pode ligar para eles?', 'pode ligar para eles', 'Abraço,\nÂngela dos Santos'),
    'ru': (['Здравствуйте, [имя]!\n\nДа', 'Я работаю в [название компании].', 'С уважением,\n[Ваше имя]'], 'Привет!\n\nГотово.',
           'Позвоните им, пожалуйста…', 'позвоните им до пятницы', 'С уважением,\nИван'),
    'ja': (['[名前]様\n\nお世話になります。', 'こんにちは、[お名前]さん', '［氏名］様'], '田中様\n\n全て完了しました。',
           '資料を確認してください。', '資料を確認してください', '敬具、\n山田'),
    'ko': (['안녕하세요 [이름]님,\n\n네', '저는 [회사명]에서 일합니다.'], '김민수님,\n\n완료했습니다.', '자료를 확인해 주세요!',
           '자료를 확인해 주세요', '감사합니다,\n김민수'),
    'zh-CN': (['您好，[姓名]：\n\n好的', '我在[公司名称]工作。'], '您好，王明：\n\n已经完成。', '请确认文件。', '请确认文件', '祝好，\n王明'),
}


def email(body, **more):
    return {'kind': 'email', 'label': 'Send reply', 'to': ['ana@x.example'], 'subject': 'Hi', 'body': body, **more}


def placeholders(action):
    return [p for p in n.check(action) if 'placeholder' in p]


class DraftMarks(unittest.TestCase):
    def test_every_shipped_language(self):
        self.assertEqual(set(TABLE), LANGUAGES)
        for lang, (left, fine, ends, runs_on, signed) in TABLE.items():
            for body in left:
                with self.subTest(lang=lang, left=body):
                    self.assertEqual(len(placeholders(email(body))), 1)
            with self.subTest(lang=lang, fine=fine):
                self.assertEqual(n.check(email(fine)), [])
            with self.subTest(lang=lang, ends=ends):
                handoff = {'kind': 'handoff', 'label': 'Hand off', 'to_name': 'Kim', 'body': ends}
                self.assertEqual(n.check(handoff), [])
                self.assertIn('runs on', n.check({**handoff, 'body': runs_on})[0])
            with self.subTest(lang=lang, signed=signed):
                closing, name = signed.split('\n')
                self.assertEqual(d.closing_spaced(f'Ok.\n\n{signed}\n'), f'Ok.\n\n{closing}\n\n{name}')
                self.assertEqual(d.closing_spaced(f'Ok.\n\n{closing}\n\n{name}'), f'Ok.\n\n{closing}\n\n{name}')  # once

    def test_brackets_with_an_everyday_use_are_left_alone(self):
        for body in ('As shown [1], it works [2, 3].', 'See [the report](https://a.example/r) and ![a photo](https://a.example/p.png).',
                     '- [ ] Book the room\n- [x] Call Kim\n* [X] Pay', 'Fixed in [ABC-123], ticket [#4521] of [2026-11-24] at [10:30].',
                     'He wrote they “recieved [sic] it”. It was [sic] late.', '“We met [Kim] in May [...] and agreed.”', '> Hi [Name],\n\nThat one went out.',
                     'Use `[name]` or `{{ name }}` there:\n\n```\nHi [first name],\n[section]\n```\n', 'items[index] and list[str] and f(x)[key]',
                     'It is \\[Name\\] in the form.', '[Optional] Bring a jacket.\n- [Bug] Search is slow\n1. [Docs] Say so', '**[Update]** It is live.',
                     '[NL] Dag allemaal, het is klaar.\n[EN] Hi all, it is done.', '[ACTION REQUIRED] Pay the bill.', '[Kim]: hi', '[INFO] started',
                     'See [the guide][guide].\n\n[guide]: https://a.example', 'See [^note] and [@kim], [a@b.example], [C:\\x], [--flag], [key=value].',
                     'Their article about the launch [Dutch]\nhttps://a.example', 'Image file too large [New]: 3 pages', '[Logo]<https://a.example>',
                     'Love you all XXX', 'Super.\nXXX', 'tot snel xxx', 'see you xx', 'The date is TBD.', 'My todo list, a Todo app.', 'TODO INCLUIDO',
                     'The TODO in that file is mine.'):
            with self.subTest(body=body):
                self.assertIsNone(d.placeholder(body))

    def test_what_is_left_to_fill_in(self):
        for body, left in (('Hi [NAME],', '[NAME]'), ('Dag [ voornaam ],', '[ voornaam ]'), ('[Vorname] [Nachname],\n\nok', '[Vorname]'), ('[Name],\n\nok', '[Name]'),
                           ('See you [date] at [time].', '[date]'), ('[Insert a line about their launch] We would love to.', '[Insert a line about their launch]'),
                           ('Hi **[Name]**,', '[Name]'), ('Hi {{first_name}},', '{{first_name}}'), ('TODO: ask Kim', 'TODO'), ('It costs XXX euro.', 'XXX'),
                           ('It costs €XXX.', 'XXX'), ('Hi, [...] and', '[...]'), ('Lorem ipsum dolor', 'Lorem ipsum'), ('Hi <name>,', '<name>'),
                           ('Read `x` first.\n\nBest,\n[Your name]', '[Your name]'), ('The room is [TBD].', '[TBD]'), ('नमस्ते [नाम],', '[नाम]')):
            with self.subTest(body=body):
                self.assertEqual(d.placeholder(body), left)
        self.assertEqual(len(placeholders({'kind': 'finish', 'label': 'Post reply', 'instructions': 'Post it.', 'preview': 'The reply', 'message': 'Hallo [Vorname],'})), 1)

    def test_a_subject_may_carry_tags(self):
        for subject in ('[list] Topic', 'Re: [External] Topic', 'AW: [EXT] Re: Topic', '回复：[通知] 会议', 'Topic [EXTERN]', '[Bug] Search is slow', 'Re: Topic'):
            with self.subTest(subject=subject):
                self.assertIsNone(d.placeholder('Ok.', subject))
        for subject in ('Intro to [company] on Friday', 'Question for [client name] today', '[Company]'):
            with self.subTest(subject=subject):
                self.assertEqual(len(placeholders(email('Ok.', subject=subject))), 1)
                self.assertEqual(placeholders(email('Ok.', subject=subject, in_reply_to='<a@b.example>')), [])  # the thread's own subject

    def test_ends_of_sentences(self):
        for text in ('Ok.', 'Ok!”', 'Ok?)', '**Friday.**', 'مرحبا؟', 'یہ ہے۔', 'कृपया फ़ाइल देखें।', 'やった！」', 'Τι κάνεις;', 'Բարև։', 'ขอบคุณครับ', 'ជំរាបសួរ។',
                     'Thanks ❤️', 'Thanks 👍🏽', 'Bel ze 👨‍👩‍👧', 'Thanks :)', 'お願いします〜', 'See https://a.example/x', 'Ok.  \n'):
            with self.subTest(text=text):
                self.assertTrue(d.ends_sentence(text))
        for text in ('take it', 'take it,', 'take it;', 'the list:', 'see (the tracker)', 'Иван', 'कृपया', '東京、', '"', ''):
            with self.subTest(text=text):
                self.assertFalse(d.ends_sentence(text))

    def test_only_a_name_gets_its_blank_line(self):
        for body in ('Ok.\n\nBest,\nsee you on Monday', 'As discussed,\nWe will come by later today', 'Best,\nEva!', 'Hi,\nok', 'Kim,\n123', 'Eva', '',
                     '好的，\n明天早上我们一起去办公室看看那份新的资料', 'Ok.\n那么，\n明天见', 'x' * 41 + ',\nEva', 'Best\nEva'):
            with self.subTest(body=body):
                self.assertEqual(d.closing_spaced(body), body)
        for name in ('Eva', 'Elise O’Neil', 'J. Smith', 'Ana Maria Lopez', 'E\u0301lise', 'Jean-Luc', 'María de la Cruz', 'أحمد', 'प्रिया', 'Zoë van den Berg'):
            with self.subTest(name=name):
                self.assertEqual(d.closing_spaced(f'Ok.\n\nBest,\n{name}'), f'Ok.\n\nBest,\n\n{name}')


if __name__ == '__main__':
    unittest.main()

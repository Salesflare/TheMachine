"""The help articles (docs/help/, shown at themachine.computer/help) stay in line with the code: scripts/help_check.py."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
import dashboard_parts

HERE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('help_check', HERE / 'scripts' / 'help_check.py')
help_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(help_check)

GOOD = '''---
title: Gmail
area: connections
summary: Reads your mail.
covers: connector:gmail
code: onboarding.py
---
Open **Connections**. See [Slack](slack.md) and [Security](/security).
'''


class HelpArticles(unittest.TestCase):
    def test_every_feature_has_an_article_and_every_article_matches_the_code(self):
        self.assertEqual(help_check.check(), [])

    def write(self, folder, name, text):
        (Path(folder) / name).write_text(text, encoding='utf-8')

    def problems(self, text, extra=()):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, 'gmail.md', text)
            self.write(d, 'slack.md', GOOD.replace('connector:gmail', 'connector:slack'))
            for name, body in extra:
                self.write(d, name, body)
            return [p for p in help_check.check(Path(d)) if p.startswith('docs/help/gmail.md')]

    def test_links_go_to_help_articles_never_to_docs_on_github(self):
        html = dashboard_parts.assemble(HERE)
        self.assertNotRegex(html, r'github\.com/Salesflare/TheMachine/(blob|tree)/[^/]+/docs/')
        self.assertIn('href="https://themachine.computer/help/work-hours"', html)
        found = help_check.articles()
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / 'page.html'
            page.write_text('<a href="https://github.com/Salesflare/TheMachine/blob/main/docs/usage.md#work-hours">Learn more</a>'
                            '<a href="https://themachine.computer/help/no-such-article">x</a>'
                            '<a href="https://themachine.computer/help/work-hours#no-such-heading">x</a>'
                            '<a href="${HELP}friends#find-people-you-know">x</a>', encoding='utf-8')
            problems = help_check.check_links(found, [page])
        self.assertEqual(len(problems), 3, problems)
        self.assertIn('on GitHub', problems[0])
        self.assertTrue(any('no-such-article' in p for p in problems) and any('no-such-heading' in p for p in problems))

    def test_a_good_article_passes(self):
        self.assertEqual(self.problems(GOOD), [])

    def test_text_the_app_no_longer_shows_fails(self):
        self.assertIn('names "Connect it now"', ' '.join(self.problems(GOOD.replace('**Connections**', '**Connect it now**'))))
        self.assertIn('route /no-such-page', ' '.join(self.problems(GOOD + 'Go to `/no-such-page`.\n')))
        self.assertIn('`assistant teleport`', ' '.join(self.problems(GOOD + 'Run `assistant teleport`.\n')))
        self.assertEqual(self.problems(GOOD.replace('code: onboarding.py', 'code: onboarding.py\nsite: Connect it now')
                                       .replace('**Connections**', '**Connect it now**')), [])  # hosted pages' text

    def test_a_feature_or_path_that_is_gone_fails(self):
        self.assertIn('connector:fax', ' '.join(self.problems(GOOD.replace('connector:gmail', 'connector:fax'))))
        self.assertIn('gone.py does not exist', ' '.join(self.problems(GOOD.replace('onboarding.py', 'gone.py'))))

    def test_a_feature_without_an_article_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, 'gmail.md', GOOD)
            problems = help_check.check(Path(d))
        self.assertIn('connector:slack has no help article: add one in docs/help/ with "covers: connector:slack" (or a reason in PENDING)', problems)
        self.assertNotIn('connector:gmail has no help article', ' '.join(problems))

    def test_house_style(self):
        for text, want in ((GOOD + 'Fast — and calm.\n', 'em dash'), (GOOD + 'You can open it.\n', 'starts with "You"'),
                           (GOOD + '- You can open it.\n', 'starts with "You"'), (GOOD + 'a' * 430 + '\n', 'over 420'),
                           (GOOD + '| a | b |\n', 'does not render'), (GOOD + '# Big\n', 'does not render'),
                           (GOOD + '[x](nowhere.md)\n', 'not an article'), (GOOD + '[x](slack.md#nowhere)\n', 'a heading slack.md does not have'),(GOOD + 'From {price.cheap}.\n', 'unknown placeholder'), (GOOD + '[x](/nowhere)\n', 'not a page of the site'),
                           (GOOD.replace('area: connections', 'area: misc'), 'area')):
            self.assertIn(want, ' '.join(self.problems(text)), text[-40:])

    def test_a_site_text_the_article_does_not_use_fails(self):
        # the site's daily help sync checks this too, and stops on it
        self.assertIn('lists "Connect it now" under site: but does not use it',
                      ' '.join(self.problems(GOOD.replace('code: onboarding.py', 'code: onboarding.py\nsite: Connect it now'))))

    def test_a_current_translation_matches_and_an_older_or_out_of_step_one_waits_for_the_translator(self):
        import sys
        sys.path.insert(0, str(HERE / 'scripts'))
        import translate
        de = GOOD.replace('Open **Connections**.', 'Öffne **Verbindungen**.')
        english = GOOD + '\n## Remove it\n\nOpen it.\n\n- One.\n- Two.\n'
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            gmail = lambda: [p for p in help_check.check_translations(help_check.articles(folder), folder) if 'gmail' in p]
            self.write(d, 'gmail.md', english)
            self.write(d, 'slack.md', GOOD.replace('connector:gmail', 'connector:slack'))
            (folder / 'de').mkdir()
            self.assertEqual(gmail(), [], 'not translated yet: Help shows the English one, the translator adds it')
            stamped = lambda text: text.replace('---\nOpen', f'translated: {translate.stamp(folder / "gmail.md")}\n---\nOpen', 1).replace('---\nÖffne', f'translated: {translate.stamp(folder / "gmail.md")}\n---\nÖffne', 1)
            # a list item short, stamped all the same: out of date, so the translator makes it again and a release waits
            self.write(folder / 'de', 'gmail.md', stamped(de + '\n## Entfernen\n\nÖffne es.\n\n- Eins.\n'))
            self.assertEqual(gmail(), [])
            self.assertEqual(translate.help_state('de', folder / 'gmail.md', folder), 'stale')
            self.write(folder / 'de', 'gmail.md', stamped(de + '\n## Entfernen\n\nÖffne es.\n\n- Eins.\n- Zwei.\n'))
            self.assertEqual(translate.help_state('de', folder / 'gmail.md', folder), 'current')
            self.assertEqual(gmail(), [])
            self.write(folder / 'de', 'gmail.md', stamped(de + '\n## Entfernen\n\nÖffne [es](nirgends.md).\n\n- Eins.\n- Zwei.\n'))
            # a link the English doesn't have: out of date too (the site's help refuses it), so the translator makes it
            # again and a release waits
            self.assertEqual(translate.help_state('de', folder / 'gmail.md', folder), 'stale')
            self.assertEqual(gmail(), [])
            # a pull request changes the English only: the translation is out of date, not wrong
            self.write(d, 'gmail.md', english + '\n## Reconnect\n\nOpen it again.\n')
            self.assertEqual(gmail(), [])
            self.write(folder / 'de', 'gmail.md', de + 'Schnell — und ruhig.\n')
            self.assertEqual(gmail(), ['docs/help/de/gmail.md: an em dash'], 'never an em dash')
            (folder / 'gmail.md').unlink()  # English no longer has it: the translator removes it
            self.write(folder / 'de', 'gmail.md', de)
            self.assertEqual(gmail(), [])

if __name__ == '__main__':
    unittest.main()

"""A to-do's body never repeats its title (machine/text.py body_after_title, the dashboard's bodyAfterTitle): New
to-do, Talk, a share from the phone and a routine all make their to-do through Store.owner_card, and a connected AI
through App.ai_card. Words that are only the title keep them as the body (the review reads them; the card shows
none); a first line or sentence that is the title keeps only what follows. The owner's own words stay whole."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('bodytitle_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.text import body_after_title  # noqa: E402 (assistant.py puts the app on the path)


class BodyAfterTitle(unittest.TestCase):
    def test_the_rule(self):
        cases = [
            ('Call the plumber', 'Call the plumber', ''),
            ('Call the plumber', '  call   the plumber.  ', ''),
            ('Call the plumber!', 'Call the plumber', ''),
            ('Plan a trip', 'Plan a trip\nA weekend in May.', 'A weekend in May.'),
            ('Plan a trip', 'Plan a trip. A weekend in May.', 'A weekend in May.'),
            ('Groceries:', 'Groceries: milk, eggs', 'milk, eggs'),
            ('Book the dentist', 'Book the dentist before Friday', 'Book the dentist before Friday'),
            ('Write the report for the board and…', 'Write the report for the board and the investors', 'Write the report for the board and the investors'),
            ('Send Sam the contract', 'Sam asked on Monday.', 'Sam asked on Monday.'),
            ('Call Pat', 'Call', 'Call'),
            ('', 'Anything', 'Anything'),
            ('Café à Paris', 'café à paris', ''),
        ]
        for title, body, want in cases:
            with self.subTest(title=title, body=body):
                self.assertEqual(body_after_title(title, body), want)


class Creators(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'w', 'boundary': 'work:acme.example'}]}

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT title,body,owner_words FROM suggestions WHERE id=?', (sid,)).fetchone())

    def test_new_todo_words_only_the_title(self):
        made = self.app.action('card_new', {'text': 'Read the product review against the vision'}, owner_dashboard=True)
        row = self.row(made['id'])
        self.assertEqual(row['title'], 'Read the product review against the vision')
        self.assertEqual(body_after_title(row['title'], row['body']), '')  # nothing shown under the title
        self.assertEqual(row['owner_words'], 'Read the product review against the vision')

    def test_talk_title_then_a_note_keeps_only_the_note(self):
        made = self.app.action('card_new', {'text': 'Plan a trip to Antwerp\nA weekend in May, two nights.'}, owner_dashboard=True)
        row = self.row(made['id'])
        self.assertEqual((row['title'], row['body']), ('Plan a trip to Antwerp', 'A weekend in May, two nights.'))
        self.assertEqual(row['owner_words'], 'Plan a trip to Antwerp\nA weekend in May, two nights.')  # their words stay whole

    def test_one_long_line_keeps_it_whole(self):
        text = 'Write the long report about the quarter for the board and the investors, with the numbers from finance and sales'
        made = self.app.action('card_new', {'text': text}, owner_dashboard=True)
        row = self.row(made['id'])
        self.assertTrue(row['title'].endswith('…'))
        self.assertEqual(row['body'], text)

    def test_a_connected_ai_todo(self):
        sid = self.app.ai_card('Claude', 'Plan a trip to Antwerp\nA weekend in May.', 'work')
        row = self.row(sid)
        self.assertEqual((row['title'], row['body']), ('Plan a trip to Antwerp', 'A weekend in May.'))
        row = self.row(self.app.ai_card('Claude', 'Call the plumber', 'work'))
        self.assertEqual(body_after_title(row['title'], row['body']), '')


if __name__ == '__main__':
    unittest.main()

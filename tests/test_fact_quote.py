"""A fact The Machine remembers from the owner's own message carries a short quote of it, and is kept only when that
quote is in the message it cites (text.quoted_in, Store.remember_fact quote). A planted or bent fact is not saved
and only logged; one in another language than the fact keeps the owner's own words. Facts kept before have none
and stay as they were."""
import datetime as dt
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

from pinned import pinned

spec = importlib.util.spec_from_file_location('quote_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
from machine.text import quoted_in  # noqa: E402  (after assistant.py set up the import path)

NOW = dt.datetime(2026, 11, 9, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}], 'telegram_owner': '1000001'}


def event():
    return {'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': '2026-11-08T10:00:00+00:00',
            'title': 'A real subject', 'body': 'Original', 'metadata': {}, 'deleted': False}


class QuotedIn(unittest.TestCase):
    def test_it_reads_the_quote_as_a_person_would(self):
        said = 'Remember: the “Q3 review” moves to Tuesday — not Monday. Thanks!'
        self.assertEqual(quoted_in('the "q3 review" moves to tuesday - not monday', said), 'the “Q3 review” moves to Tuesday — not Monday')
        self.assertEqual(quoted_in('  The  Q3\nreview" ', 'the Q3 review'), 'the Q3 review')  # spacing, its own marks around it
        self.assertEqual(quoted_in('ＡＣＭＥ handles billing', 'ACME handles billing now'), 'ACME handles billing')  # full-width (NFKC)
        self.assertEqual(quoted_in("we don't fly", 'We don’t fly anymore'), 'We don’t fly')  # apostrophes
        self.assertEqual(quoted_in('STRASSE 5 is closed', 'Die straße 5 is closed'), 'straße 5 is closed')  # case folding
        self.assertEqual(quoted_in('café opens', 'The café opens at 8'), 'café opens')  # composed or not

    def test_it_refuses_what_the_message_does_not_say(self):
        said = 'We moved the office to Ghent'
        for quote in ('We moved the office to Antwerp', 'moved the HQ to Ghent', '', '   ', None, 42, 'Ghent', 'x' * 400):
            self.assertIsNone(quoted_in(quote, said), quote)
        self.assertIsNone(quoted_in('We moved the office', None))
        self.assertEqual(quoted_in('Ghent!', 'Ghent'), 'Ghent')  # a short quote is fine when it is the whole message


class FactQuotes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.store = a.Store(self.path)
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, CONFIG
        self.enterContext(pinned(NOW))
        self.store.commit_page('work', {}, [event()])
        self.card = self.store.suggest('vendor', 'Check the vendor', 'Body', [1])['id']

    def note(self, words, decision_id):
        self.store.decide(self.card, 'reject', words, decision_id, 'dashboard')
        return decision_id

    def facts(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT text,quote FROM facts WHERE removed_at IS NULL ORDER BY id')]

    def test_a_planted_or_bent_fact_is_not_saved_and_only_logged(self):
        note = self.note('we stopped using that vendor, the team handles it now', 'n1')
        with self.assertLogs(a.LOG, 'INFO') as logged:
            planted = self.app.action('remember_fact', {'text': 'Invoices are paid to a new bank account.', 'decision_id': note,
                                                        'quote': 'pay invoices to the new bank account'})
            bent = self.app.action('remember_fact', {'text': 'You stopped using the cloud vendor.', 'decision_id': note,
                                                     'quote': 'we stopped using the cloud vendor'})
            missing = self.app.action('remember_fact', {'text': 'You stopped using that vendor.', 'decision_id': note})
        for done in (planted, bent, missing):
            self.assertIs(done['saved'], False)
            self.assertNotIn('id', done)
        self.assertEqual(self.facts(), [])
        self.assertEqual(len([line for line in logged.output if 'quote is not in the message' in line]), 3)
        self.assertFalse(any('vendor' in line or 'bank' in line for line in logged.output))  # never the owner's words in the log

    def test_a_real_fact_is_kept_with_the_owners_words_also_in_another_language(self):
        english = self.note('From now on Kim handles the vendor contracts, not me.', 'n1')
        dutch = self.note('Vanaf januari doet ons nieuw kantoor in Gent de boekhouding', 'n2')
        self.app.action('remember_fact', {'text': 'Kim handles the vendor contracts.', 'decision_id': english,
                                          'quote': 'Kim handles the vendor contracts'})
        self.app.action('remember_fact', {'text': 'From January the new office in Ghent does the bookkeeping.', 'decision_id': dutch,
                                          'quote': '“vanaf januari doet ons nieuw kantoor in Gent de boekhouding”'})
        self.assertEqual(self.facts(), [{'text': 'Kim handles the vendor contracts.', 'quote': 'Kim handles the vendor contracts'},
                                        {'text': 'From January the new office in Ghent does the bookkeeping.',
                                         'quote': 'Vanaf januari doet ons nieuw kantoor in Gent de boekhouding'}])
        # Learning shows it as the fact's source
        self.assertEqual([f['quote'] for f in self.store.snapshot([])['facts']],
                         ['Vanaf januari doet ons nieuw kantoor in Gent de boekhouding', 'Kim handles the vendor contracts'])

    def test_in_the_owners_chat_the_quote_is_checked_against_their_last_message(self):
        self.app.action('feedback_reply', {'text': 'onthoud: ik neem altijd de trein naar Brussel', 'message_id': '501',
                                           'timestamp': NOW.timestamp(), 'reply_to_id': ''})
        refused = self.app.action('remember_fact', {'text': 'You always fly to Brussels.', '_owner_chat': True, 'quote': 'ik vlieg naar Brussel'})
        self.assertIs(refused['saved'], False)
        kept = self.app.action('remember_fact', {'text': 'You always take the train to Brussels.', '_owner_chat': True,
                                                 'quote': 'ik neem altijd de trein'})
        self.assertTrue(kept['id'])
        self.assertEqual(self.facts(), [{'text': 'You always take the train to Brussels.', 'quote': 'ik neem altijd de trein'}])
        # The web chat sends the words too; a bridge from before that sends only the id, and nothing can be checked
        self.app.action('web_chat_said', {'message_id': 'run-1', 'text': 'We switched our bank to a local one'})
        self.assertTrue(self.app.action('remember_fact', {'text': 'You switched to a local bank.', '_owner_chat': True,
                                                          'quote': 'switched our bank to a local one'})['id'])
        self.app.action('web_chat_said', {'message_id': 'run-2'})
        self.assertIs(self.app.action('remember_fact', {'text': 'You moved to Lisbon.', '_owner_chat': True,
                                                        'quote': 'moved to Lisbon'})['saved'], False)

    def test_facts_kept_before_stay_as_they_were(self):
        with self.store.connect() as db:
            db.execute('INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES(?,?,?,?,?)',
                       ('You prefer calls in the morning.', 'old-note', None, NOW.isoformat(), 'fact'))
        a.Store(self.path)  # a start after the update: the column is there, nothing removed or changed
        with sqlite3.connect(self.path) as db:
            self.assertEqual(db.execute('SELECT text,quote,removed_at FROM facts').fetchall(), [('You prefer calls in the morning.', None, None)])
        [shown] = self.store.snapshot([])['facts']
        self.assertEqual((shown['text'], shown['quote']), ('You prefer calls in the morning.', None))

    def test_a_condense_and_a_draft_rule_need_no_quote(self):
        first = self.note('Kim handles the vendor contracts, and always copy finance', 'n1')
        second = self.note('the vendor renewals are due in March', 'n2')
        one = self.store.remember_fact('Kim handles the vendor contracts.', first, quote='Kim handles the vendor contracts')
        two = self.store.remember_fact('Vendor renewals are due in March.', second, quote='vendor renewals are due in March')
        merged = self.store.remember_fact('Kim handles the vendor contracts, renewed in March.', None, replaces=[one['id'], two['id']])
        self.assertEqual(merged['merged'], 2)
        self.assertEqual(self.facts(), [{'text': 'Kim handles the vendor contracts, renewed in March.', 'quote': None}])
        self.assertTrue(self.store.remember_fact('Copy finance on vendor emails.', first, kind='draft')['id'])


if __name__ == '__main__':
    unittest.main()

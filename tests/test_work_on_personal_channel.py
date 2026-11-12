"""Work is Work, also when it comes in on a personal account: a client writing on the owner's personal chat app, or an
order for their business in their personal mailbox, stayed Personal when the owner has one company, since the review
could only move a to-do from Work to Personal. Now the review is told the owner's company and their personal accounts
with one company too, and judges by meaning whether to add company=<id>: the to-do is then that company's Work from the
start, as after a move. The owner's own choice always stands: a to-do they moved, or added with Work or Personal
picked, is never placed elsewhere by the review. Made-up data; offline: nothing is sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('work_personal_channel_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.store.cards import owner_placed  # noqa: E402

ACCOUNTS = [{'id': 'home-chat', 'service': 'whatsapp', 'boundary': 'personal:whatsapp'},
            {'id': 'home-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@home.example', 'boundary': 'personal:me'},
            {'id': 'acme-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
            {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'}]


def chat(source_id, text, thread):
    return {'account_id': 'home-chat', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': '2026-11-06T09:00:00+00:00',
            'title': 'Sam', 'body': text, 'metadata': {'from': 'Sam', 'chat_id': thread, 'thread_id': thread}, 'deleted': False}


class Prompt(unittest.TestCase):
    def test_one_company_and_a_personal_account_the_review_may_place_work(self):
        line = a.companies_prompt({'accounts': ACCOUNTS})
        self.assertIn('Work is Work', line)
        self.assertIn('home-chat, home-mail', line)
        self.assertIn('company=<its id> to suggest (work:Acme)', line)
        self.assertIn('never by a word or a name in the text alone', line)
        self.assertNotIn("The owner's companies", line)  # one company: nothing about mail for another one
        self.assertEqual(a.companies_prompt({'accounts': ACCOUNTS[2:]}), '')  # no personal account
        self.assertEqual(a.companies_prompt({'accounts': ACCOUNTS[:2]}), '')  # no company

    def test_a_company_whose_to_dos_are_personal_is_not_offered(self):
        side = [{**ACCOUNTS[2], 'scope': 'personal'}, ACCOUNTS[0]]
        self.assertEqual(a.companies_prompt({'accounts': side}), '')


class Placing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'prepare_ahead': False, 'database': str(Path(self.temp.name) / 'e.sqlite')}
        self.store.config = self.app.config
        self.store.commit_page('home-chat', {}, [chat('w1', 'Can you send the signed quote for the pilot?', 'c1'),
                                                  chat('w2', 'Any news on the quote?', 'c1')])

    def suggest(self, **extra):
        return self.app.action('suggest', {'dedupe_key': 'chat:quote', 'title': 'Send the signed quote for the pilot',
                                           'body': 'The client asks for the signed quote.', 'event_ids': [1], **extra})['id']

    def row(self, sid):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())

    def scope(self, sid):
        with self.store.connect() as db:
            row = dict(db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone())
            self.store.card_views(db, [row])
        return row['scope']

    def test_without_the_reviews_word_it_stays_personal(self):
        self.assertEqual(self.scope(self.suggest()), 'personal')

    def test_the_review_places_work_from_a_personal_chat_in_work(self):
        sid = self.suggest(company='work:Acme')
        row = self.row(sid)
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['acme-mail'], 'work:Acme'))
        self.assertEqual(self.scope(sid), 'work')

    def test_the_owners_move_stands(self):
        sid = self.suggest()
        self.app.action('card_move', {'suggestion_id': sid, 'area': 'work:Acme', 'decision_id': 'm1'}, owner_dashboard=True)
        self.app.action('card_move', {'suggestion_id': sid, 'undo': 'm1', 'decision_id': 'm2'}, owner_dashboard=True)
        self.assertEqual(self.scope(sid), 'personal')  # moved back by the owner: Personal, with no area pinned
        self.app.action('suggest', {'dedupe_key': 'chat:quote:2', 'title': 'Send the signed quote for the pilot',
                                    'body': 'The client asks again.', 'event_ids': [2], 'card_id': sid, 'company': 'work:Acme'})
        self.assertEqual(self.scope(sid), 'personal')

    def test_an_owners_to_do_with_personal_picked_stays_personal(self):
        sid = self.app.action('card_new', {'text': 'Send the signed quote for the pilot', 'scope': 'personal'}, owner_dashboard=True)['id']
        with self.store.connect() as db:
            self.assertTrue(owner_placed(db, db.execute('SELECT * FROM suggestions WHERE id=?', (sid,)).fetchone()))
        self.app.action('suggest', {'dedupe_key': 'chat:quote:own', 'title': 'Send the signed quote for the pilot',
                                    'body': 'The client asks for it.', 'event_ids': [1], 'card_id': sid, 'company': 'work:Acme'})
        self.assertEqual(self.scope(sid), 'personal')

    def test_an_unmoved_card_is_placed_on_a_later_signal(self):
        sid = self.suggest()
        self.app.action('suggest', {'dedupe_key': 'chat:quote:2', 'title': 'Send the signed quote for the pilot',
                                    'body': 'The client asks again.', 'event_ids': [2], 'card_id': sid, 'company': 'work:Acme'})
        self.assertEqual(self.scope(sid), 'work')


if __name__ == '__main__':
    unittest.main()

"""Work is Work, also when it comes in on a personal account: a client writing on the owner's personal chat app, or an
order for their business in their personal mailbox, stayed Personal when the owner has one company, since the review
could only move a to-do from Work to Personal. Now the review is told the owner's company and their personal accounts
with one company too, and judges by meaning whether to add company=<id>: the to-do is then that company's Work from the
start, as after a move. The owner's own choice always stands: a to-do they moved, or added with Work or Personal
picked, is never placed elsewhere by the review. Made-up data; offline: nothing is sent."""
import json
import tempfile
import unittest
from pathlib import Path
import machine.app.preparation as machine_app_preparation
import machine.main as machine_main
import machine.prompts.review as machine_prompts_review
import machine.sources.connectors as machine_sources_connectors
import next_actions

from machine.store.cards import own_life_evidence, owner_placed  # noqa: E402

ACCOUNTS = [{'id': 'home-chat', 'service': 'whatsapp', 'boundary': 'personal:whatsapp'},
            {'id': 'home-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@home.example', 'boundary': 'personal:me'},
            {'id': 'acme-mail', 'service': 'gmail', 'transport': 'gog', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
            {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'}]


def chat(source_id, text, thread):
    return {'account_id': 'home-chat', 'source_id': source_id, 'kind': 'whatsapp.message', 'occurred_at': '2026-11-06T09:00:00+00:00',
            'title': 'Sam', 'body': text, 'metadata': {'from': 'Sam', 'chat_id': thread, 'thread_id': thread}, 'deleted': False}


class Prompt(unittest.TestCase):
    def test_one_company_and_a_personal_account_the_review_may_place_work(self):
        line = machine_sources_connectors.companies_prompt({'accounts': ACCOUNTS})
        self.assertIn('Work is Work', line)
        self.assertIn('home-chat, home-mail', line)
        self.assertIn('company=<its id> to suggest (work:Acme), and to promise the same way', line)
        self.assertIn('personal or company as for suggest', machine_prompts_review.review_prompt('r1', ['home-chat']))
        self.assertIn('never by a word or a name in the text alone', line)
        self.assertNotIn("The owner's companies", line)  # one company: nothing about mail for another one
        self.assertEqual(machine_sources_connectors.companies_prompt({'accounts': ACCOUNTS[2:]}), '')  # no personal account
        self.assertEqual(machine_sources_connectors.companies_prompt({'accounts': ACCOUNTS[:2]}), '')  # no company

    def test_a_company_whose_to_dos_are_personal_is_not_offered(self):
        side = [{**ACCOUNTS[2], 'scope': 'personal'}, ACCOUNTS[0]]
        self.assertEqual(machine_sources_connectors.companies_prompt({'accounts': side}), '')


class Placing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.accounts = ACCOUNTS
        self.app = object.__new__(machine_main.App); self.app.store = self.store
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

    def test_work_marked_by_the_review_or_a_move_still_replies_where_the_thread_lives(self):
        placed = self.suggest(company='work:Acme')
        moved = self.app.action('suggest', {'dedupe_key': 'chat:other', 'title': 'Confirm the pilot date',
                                            'body': 'The client asks for a date.', 'event_ids': [2], 'separate': True})['id']
        self.app.action('card_move', {'suggestion_id': moved, 'area': 'work:Acme', 'decision_id': 'm3'}, owner_dashboard=True)
        for sid in (placed, moved):
            row = self.row(sid)
            self.assertEqual((self.scope(sid), json.loads(row['account_ids'])), ('work', ['acme-mail']))
            # the run is told to answer in its own chat, from the account it came in on, and not to ask for a move
            with self.store.connect() as db:
                line = machine_app_preparation.area_prompt(self.app.config, row['account_ids'], machine_app_preparation.card_sources(db, sid), owner_started=True)
            self.assertIn('A reply in one of its own chats goes in that chat, from the account it came in on (home-chat), also one labeled Personal', line)
            self.assertIn('It stays Work.', line)
            # and the WhatsApp reply in that chat is valid for the Work to-do
            action = next_actions.validate({'kind': 'whatsapp', 'account_id': 'home-chat', 'chat_id': 'c1', 'body': 'Sent it, thanks!'},
                                             self.app.config, json.loads(row['account_ids']), whatsapp_chats={'c1': {'account_id': 'home-chat', 'name': 'Sam'}})
            self.assertEqual((action['kind'], action['account_id']), ('whatsapp', 'home-chat'))

    def test_an_email_reply_after_a_move_to_work_goes_from_the_personal_mailbox_it_came_in_on(self):
        replied = {'<order@shop.example>': {'account_id': 'home-mail', 'thread_id': 't9', 'homes': {}}}
        draft = {'kind': 'email', 'account_id': 'home-mail', 'to': ['orders@shop.example'], 'subject': 'Re: Your order',
                 'body': 'Thanks, the invoice is fine.', 'in_reply_to': '<order@shop.example>'}
        action = next_actions.validate(draft, self.app.config, ['acme-mail'], replied=replied)
        self.assertEqual((action['account_id'], action['from']), ('home-mail', 'robin@home.example'))
        new = {k: v for k, v in draft.items() if k != 'in_reply_to'}
        with self.assertRaises(ValueError):  # a new email is not its thread: it goes from the area's accounts
            next_actions.validate(new, self.app.config, ['acme-mail'], replied=replied)

    def test_an_unmoved_card_is_placed_on_a_later_signal(self):
        sid = self.suggest()
        self.app.action('suggest', {'dedupe_key': 'chat:quote:2', 'title': 'Send the signed quote for the pilot',
                                    'body': 'The client asks again.', 'event_ids': [2], 'card_id': sid, 'company': 'work:Acme'})
        self.assertEqual(self.scope(sid), 'work')

    # A to-do made from a promise, and one that is Personal only from who is on it

    def friend(self):
        """Sam, who writes on the home chat, is in the owner's Friends on the Network."""
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,last_at,signals,gap_days,quiet,trend,info) VALUES('p:sam','person','Sam',1,NULL,1,NULL,0,NULL,?)",
                       (json.dumps({'side': 'personal', 'side_why': 'network'}),))
            db.executemany("INSERT INTO graph_events(node_id,event_id,at,probable,direct) VALUES('p:sam',?,'2026-11-06',0,1)", [(1,), (2,)])

    def promise(self, **extra):
        self.store.promise({'direction': 'theirs', 'event_id': 1, 'who': 'Sam', 'what': 'send the pilot contract', **extra})
        with self.store.connect() as db:
            return dict(db.execute("SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE what='send the pilot contract'").fetchone())

    def due(self, p):
        with self.store.connect() as db:
            db.execute("UPDATE promises SET check_at='2026-11-07T08:00:00+00:00' WHERE id=?", (p['id'],))
        return self.app.promise_card(p)['id']

    def again(self, sid, **extra):
        self.app.action('suggest', {'dedupe_key': f'chat:pilot:{sid}', 'title': 'Send the pilot contract', 'body': 'Sam asks again.',
                                    'event_ids': [2], 'card_id': sid, **extra})

    def test_a_promise_about_work_becomes_a_work_to_do_also_from_a_friend(self):
        self.friend()
        row = self.row(self.due(self.promise(company='work:Acme')))
        self.assertEqual((json.loads(row['account_ids']), row['area'], self.scope(row['id'])), (['acme-mail'], 'work:Acme', 'work'))

    def test_a_promise_without_the_reviews_word_goes_where_it_did(self):
        sid = self.due(self.promise())
        self.assertEqual((self.row(sid)['area'], self.scope(sid)), (None, 'personal'))

    def test_a_friends_promise_without_the_reviews_word_is_personal(self):
        self.friend()
        row = self.row(self.due(self.promise()))
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['home-chat', 'home-mail'], 'personal'))

    def test_a_promise_of_their_own_life_on_a_work_mailbox_becomes_a_personal_to_do(self):
        self.store.commit_page('acme-mail', {}, [{'account_id': 'acme-mail', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': '2026-11-06T09:00:00+00:00',
                                                  'title': 'Party', 'body': 'I will book the venue.', 'deleted': False,
                                                  'metadata': {'from': 'Sam <sam@mail.example>', 'to': 'robin@acme.example', 'thread_id': 't1'}}])
        row = self.row(self.due(self.promise(event_id=3, personal=True)))
        self.assertEqual((json.loads(row['account_ids']), row['area']), (['home-chat', 'home-mail'], 'personal'))

    def test_a_promise_says_one_of_the_owners_companies(self):
        with self.assertRaisesRegex(ValueError, 'work:Acme'):
            self.promise(company='work:Other')

    def test_a_promise_whose_company_is_no_longer_set_up_follows_its_account(self):
        p = self.promise(company='work:Acme')
        self.app.config['accounts'] = self.store.accounts = [a for a in ACCOUNTS if a['id'] != 'acme-mail']
        self.assertEqual(self.row(self.due(p))['area'], None)

    def test_the_review_places_a_promise_it_already_has(self):
        p = self.promise()
        self.assertEqual(self.promise(company='work:Acme')['area'], 'work:Acme')  # said again, now with its company
        self.store.promise({'id': p['id'], 'due': '2026-11-20', 'reason': 'moved', 'personal': True})
        self.assertEqual(self.promise()['area'], 'personal')

    def test_personal_only_from_who_is_on_it_gives_way_to_the_reviews_word(self):
        self.friend()
        for sid in (self.due(self.promise()), self.suggest(separate=True)):  # one from a promise, one the review made
            self.assertEqual(self.row(sid)['area'], 'personal')
            self.again(sid, company='work:Acme')
            row = self.row(sid)
            self.assertEqual((json.loads(row['account_ids']), row['area'], self.scope(sid)), (['acme-mail'], 'work:Acme', 'work'))

    def test_personal_from_who_is_on_it_stays_without_the_reviews_word(self):
        self.friend()
        sid = self.due(self.promise())
        self.again(sid)
        self.assertEqual((self.row(sid)['area'], self.scope(sid)), ('personal', 'personal'))

    def test_personal_by_the_reviews_own_word_stays(self):
        sid = self.suggest(personal=True)  # Sam is nobody from the owner's own life: the review judged the matter
        self.again(sid, company='work:Acme')
        self.assertEqual(self.scope(sid), 'personal')

    def test_the_owners_move_to_personal_stands_over_the_reviews_word(self):
        self.friend()
        sid = self.due(self.promise(company='work:Acme'))
        self.app.action('card_move', {'suggestion_id': sid, 'area': 'personal', 'decision_id': 'm4'}, owner_dashboard=True)
        self.again(sid, company='work:Acme')
        self.assertEqual(self.scope(sid), 'personal')

    def test_a_friends_thread_is_still_their_own_life(self):
        """The to-do is Work; the person, and so what a Work Fleet may see of their messages, is as it was (graph.own_life)."""
        self.friend()
        self.due(self.promise(company='work:Acme'))
        with self.store.connect() as db:
            self.assertTrue(own_life_evidence(db, [1]))


if __name__ == '__main__':
    unittest.main()

"""A question typed into Messages search, on made-up data: an English question about a booking whose code sits in a
Dutch mail. The word match leaves out the question's own words; the best match by words stays in the first three
results even when meaning ranks other "discount code" chats above it; a phone's preview of a message found in full shows
once, as the message, and repeated previews once; and Ask (search_ask.py) reads that mail, so its answer cites it."""
import json
import re
import unittest
from unittest.mock import patch

import test_embeddings as te

a, emb = te.a, te.emb
import search_ask  # noqa: E402
from machine.text import fold_previews  # noqa: E402

QUESTION = "what's the regenboog discount code?"
BOOKING = ('Bevestiging van je jaarabonnement', 'Bedankt voor je bestelling. Voordelen: 10% korting op een kinderfeestje '
           "bij Speelpark de Regenboog. Gebruik de kortingscode 'FEEST10' bij het afrekenen. "
           'Toon je QR-code bij de entree.')
CHAT = 'Party at Regenboog on the 16th, who is coming along with the kids?'


def note(source_id, title, body):
    return te.event(source_id, title, body, account='phone', kind='android.notification',
                    metadata={'app_name': 'Chats', 'package_name': 'com.example.chats'})


class MessagesQuestion(unittest.TestCase):
    embed_all, ids = te.Embeddings.embed_all, te.Embeddings.ids

    def setUp(self):
        te.Embeddings.setUp(self)
        others = [te.event(f'd{n}', f'Discount code {n}', f'Here is the discount code for the {topic}, what a deal.')
                  for n, topic in enumerate(('webinar', 'shoes', 'flights', 'hotel', 'course', 'books', 'pizza', 'cinema', 'tickets', 'gym'))]
        self.store.commit_page('work', {}, [te.event('booking', *BOOKING), *others])
        self.store.commit_page('chat', {}, [te.event('c1', 'Family group', CHAT, account='chat', kind='whatsapp.message',
                                                     metadata={'chat_name': 'Family group', 'from': 'Ana'})])
        self.store.commit_page('phone', {}, [note('n1', 'Family group', CHAT), note('n2', 'Planner', 'Which party at Regenboog: adventure or bowling?'),
                                             note('n3', 'Planner', 'Which party at Regenboog: adventure or bowling?')])
        self.app.config = {'accounts': [{'id': 'work', 'scope': 'work'}, {'id': 'home', 'scope': 'personal'}, {'id': 'chat', 'scope': 'personal'},
                                        {'id': 'phone', 'scope': 'personal'}], 'embeddings': te.SETTINGS}
        self.embed_all()
        search_ask._asked.clear()

    def booking(self):
        return self.ids('work', 'booking')

    def test_question_words_stay_out_of_the_word_match(self):
        self.assertEqual(emb.search_words(QUESTION), ['regenboog', 'discount', 'code'])
        self.assertEqual(emb.search_words('wat is de kortingscode'), ['kortingscode'])
        self.assertEqual(emb.search_words('what is the'), ['what', 'is', 'the'])  # only question words: kept, still a search
        self.assertEqual(emb.words_lead([1, 2, 3, 4, 5], [5], 3), [1, 2, 5, 3, 4])
        self.assertEqual(emb.words_lead([1, 2, 3], [2], 3), [1, 2, 3])  # already in front: as it was
        self.assertEqual(emb.words_lead([1, 2], [9], 3), [1, 2, 9])

    def test_the_mail_with_the_code_stays_on_top_for_an_english_question(self):
        meaning = [i for i, _ in emb.related(self.store.connect, te.SETTINGS, ['work', 'chat', 'phone'], query=QUESTION, limit=40)]
        self.assertGreater(meaning.index(self.booking()), 2)  # as it was: other "discount code" mails ranked above it
        rows = self.app.action('events', {'account_ids': ['all'], 'query': QUESTION, 'semantic': True, 'full': True})
        ids = [r['id'] for r in rows]
        self.assertIn(self.booking(), ids[:3])
        previews = [r for r in rows if r['kind'] == 'android.notification']
        self.assertEqual([r['body'] for r in previews], ['Which party at Regenboog: adventure or bowling?'])  # once, and not the chat's
        self.assertIn(CHAT, [r['body'] for r in rows if r['kind'] == 'whatsapp.message'])

    def test_previews_fold_into_what_is_there_in_full(self):
        rows = [{'kind': 'android.notification', 'title': 'Ana', 'body': 'Party at Regenboog on the 16th, who is com…'},
                {'kind': 'whatsapp.message', 'title': 'Family group', 'body': CHAT},
                {'kind': 'android.notification', 'title': 'Bank', 'body': 'Card used'},
                {'kind': 'android.notification', 'title': 'Bank', 'body': 'Card used'}]
        self.assertEqual(fold_previews(rows), rows[1:3])  # a cut-off preview of the chat goes; one of a repeat stays

    def test_ask_reads_the_mail_and_cites_it(self):
        prompts = []

        def model(config, text):
            if 'reply with one JSON object' in text:
                return json.dumps({'question': True, 'person': None, 'said_by': 'both', 'from': None, 'to': None, 'about': 'Regenboog discount code'})
            prompts.append(text)
            n = re.search(r'\[(\d+)\] gmail from [^\n]*Bevestiging', text)
            return f'The code is FEEST10, for 10% off a kids\' party [{n[1]}].' if n else 'These messages don\'t say.'
        self.app.ask_model = model
        found = self.app.action('search_ask', {'query': QUESTION, 'area': 'all'}, owner_dashboard=True)
        self.assertIn('FEEST10', prompts[0])
        self.assertEqual(found['answer'], 'The code is FEEST10, for 10% off a kids\' party.')
        self.assertEqual([s['title'] for s in found['sources']], [BOOKING[0]])
        with patch.object(self.app, 'ask_model', lambda config, text: model(config, text) if 'JSON' in text else 'These messages don\'t say.'):
            self.assertEqual(self.app.action('search_ask', {'query': QUESTION, 'area': 'all'}, owner_dashboard=True)['sources'], [])  # the page shows nothing


if __name__ == '__main__':
    unittest.main()

"""What the owner states in their own private chat becomes a fact under Learning: the bridge marks the chat
(_owner_chat, never the model), the service ties the fact to their last message there (feedback_reply, which takes the
owner key), and nothing else saves a fact without one of the owner's notes (feedback.py owner_said,
graph_actions.py remember_fact_action, Store.remember_fact said)."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pinned import pinned

spec = importlib.util.spec_from_file_location('said_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
graph = a.graph
feedback = a.FeedbackApp.__dict__['owner_said'].__globals__
NOW = dt.datetime(2026, 11, 9, 12, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'work', 'email': 'sam@acme.com'}], 'telegram_owner': '1000001'}


class SaidFacts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, CONFIG
        self.enterContext(pinned(NOW))  # end days and expiry are checked against this moment, not the day the test runs

    def says(self, text, message_id):
        return self.app.action('feedback_reply', {'text': text, 'message_id': message_id, 'timestamp': NOW.timestamp(), 'reply_to_id': ''})

    def save(self, text, **args):
        return self.app.action('remember_fact', {'text': text, '_owner_chat': True, **args})

    def test_a_fact_the_owner_states_in_their_chat_shows_under_learning_with_where_it_came_from(self):
        with self.assertRaisesRegex(ValueError, 'owner’s own words'):
            self.save('The office moved to Ghent.')  # nothing said yet: nothing to save it from
        self.assertFalse(self.says('remember that we moved the office to Ghent', '501')['handled'])
        saved = self.save('The office moved to Ghent.')
        with self.store.connect() as db:
            row = dict(db.execute('SELECT decision_id,suggestion_id,source,kind FROM facts WHERE id=?', (saved['id'],)).fetchone())
        self.assertEqual(row, {'decision_id': 'telegram-said:501', 'suggestion_id': None, 'source': None, 'kind': 'fact'})
        self.assertIsNone(a.ai_fact_by(row))  # the owner's own, not third-party text
        # Under Learning (the status the dashboard lists), and in what reviews and drafts read
        self.assertEqual([f['text'] for f in self.store.snapshot([])['facts']], ['The office moved to Ghent.'])
        self.assertEqual(self.store.facts_text(), '- The office moved to Ghent.')
        # The owner's controls work on it as on any fact
        self.app.action('edit_fact', {'id': saved['id'], 'text': 'The office moved to Ghent in November.'}, owner_dashboard=True)
        self.app.action('forget_fact', {'id': saved['id']}, owner_dashboard=True)
        self.assertEqual(self.store.snapshot([])['facts'], [])
        # One message can hold several; a sort and an end day are kept
        trip = self.save('You are in Lisbon until Friday.', kind='event', until='2026-11-13')  # the Friday after NOW
        self.assertEqual((trip['kind'], trip['until']), ('event', '2026-11-13'))

    def test_it_is_tied_to_the_person_it_is_about(self):
        mail = {'account_id': 'work', 'source_id': 'm1', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=2)).isoformat(),
                'title': 'Pricing', 'body': 'Hello', 'deleted': False,
                'metadata': {'from': 'Ann Example <ann@client.com>', 'to': 'sam@acme.com', 'cc': '', 'labels': ['INBOX'], 'message-id': '<1@x>', 'thread_id': 't1'}}
        self.store.commit_page('work', {}, [mail])
        self.store.owner_user_ids = set()
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())
        self.says('Ann only takes calls before 10', '502')
        hers = self.save('Ann prefers calls before 10.', kind='preference', about=['email:ann@client.com'])
        self.assertEqual(hers['about'], ['email:ann@client.com'])
        known = [f['text'] for f in self.app.graph_action({'node_id': 'email:ann@client.com'})['open'].get('known', [])]
        self.assertEqual(known, ['Ann prefers calls before 10.'])
        # Who it is about never costs what the owner said: the owner themselves (never a record), a first name the
        # graph can't place or someone it never met is left off, and the fact is kept with the record that matched
        self.says('Ann and I agreed: quotes to her go out on Mondays', '504')
        kept = self.save('Quotes to Ann go out on Mondays.', about=['Sam Owner', 'email:ann@client.com', 'email:nobody@x.com'])
        self.assertEqual(kept['about'], ['email:ann@client.com'])
        self.assertEqual(kept['about_skipped'], ['Sam Owner', 'email:nobody@x.com'])
        self.says('my sister Mila swims on Saturdays', '505')
        alone = self.save('Mila has swimming lessons on Saturdays.', about=['Mila'])
        self.assertEqual((alone.get('about') or [], alone['about_skipped']), ([], ['Mila']))
        self.assertIn('Mila has swimming lessons on Saturdays.', [f['text'] for f in self.store.facts()])
        # Outside the owner's chat a wrong about still stops the save: a review names records it read
        with self.store.connect() as db, self.assertRaisesRegex(ValueError, 'not a person, organization or project'):
            self.store.fact_subjects(db, ['email:nobody@x.com'])

    def test_code_modes_guess_of_the_argument_is_the_fact(self):
        """In Code Mode the model never sees the tool's description and writes the sentence as fact, not text."""
        self.says('the team offsite moved to March', '506')
        saved = self.app.action('remember_fact', {'fact': 'The team offsite moved to March.', '_owner_chat': True})
        self.assertEqual([f['text'] for f in self.store.facts() if f['id'] == saved['id']], ['The team offsite moved to March.'])

    def test_only_the_owners_own_chat_and_only_what_they_just_said(self):
        self.says('we stopped using TranslateCo', '503')
        # Any other session (a review, a to-do's run) carries no mark from the bridge: a note's id as before
        with self.assertRaisesRegex(ValueError, 'owner’s own written notes'):
            self.app.action('remember_fact', {'text': 'We stopped using TranslateCo.'})
        for claimed in ('telegram-said:503', 'telegram-said:1'):  # a model can't name the message itself
            with self.assertRaisesRegex(ValueError, 'owner’s own written notes'):
                self.app.action('remember_fact', {'text': 'We stopped using TranslateCo.', 'decision_id': claimed})
            with self.assertRaisesRegex(ValueError, 'owner’s own written notes'):
                self.store.remember_fact('We stopped using TranslateCo.', claimed)
        with self.assertRaises(ValueError):
            self.store.remember_fact('We stopped using TranslateCo.', 'owner-note', said=True)  # vouched for, but no chat message
        with self.assertRaisesRegex(ValueError, 'owner’s own written notes'):
            self.app.action('remember_fact', {'text': 'We stopped using TranslateCo.', '_owner_chat': 'yes'})
        # Half an hour later the turn is no longer the answer to that message
        late = NOW.timestamp() + feedback['OWNER_SAID_MINUTES'] * 60 + 1
        with patch.object(feedback['time'], 'time', return_value=NOW.timestamp()):
            self.says('we stopped using TranslateCo', '504')
            self.assertEqual(self.app.owner_said(), 'telegram-said:504')
        with patch.object(feedback['time'], 'time', return_value=late):
            self.assertIsNone(self.app.owner_said())
            with self.assertRaisesRegex(ValueError, 'owner’s own words'):
                self.save('We stopped using TranslateCo.')
        # A command or an empty message is nothing the owner stated
        self.app.owner_said_last = None
        for text in ('/status', '   '):
            self.says(text, '505')
            self.assertIsNone(self.app.owner_said())
        self.assertEqual(self.store.facts(), [])
        # The words themselves are kept nowhere
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM decisions').fetchone()[0], 0)

    def test_the_web_chat_saves_what_the_owner_said_there(self):
        # the bridge notes the owner's web chat message (owner key, before_dispatch); the words never reach the service
        self.assertIn('web_chat_said', a.OWNER_ACTIONS)
        self.assertEqual(self.app.action('web_chat_said', {'message_id': 'run-7f3a'}), {'noted': True})
        saved = self.save('You take the train to the office.')
        with self.store.connect() as db:
            row = dict(db.execute('SELECT decision_id,suggestion_id,source FROM facts WHERE id=?', (saved['id'],)).fetchone())
        self.assertEqual(row, {'decision_id': 'webchat-said:run-7f3a', 'suggestion_id': None, 'source': None})
        self.assertEqual([f['text'] for f in self.store.snapshot([])['facts']], ['You take the train to the office.'])
        # a model can't name a web chat message itself, and a made-up id is refused
        with self.assertRaisesRegex(ValueError, 'owner’s own written notes'):
            self.app.action('remember_fact', {'text': 'You take the bus.', 'decision_id': 'webchat-said:run-7f3a'})
        with self.assertRaisesRegex(ValueError, 'web chat message id'):
            self.app.action('web_chat_said', {'message_id': 'x y'})
        # half an hour later it no longer counts
        with patch.object(feedback['time'], 'time', return_value=NOW.timestamp() + feedback['OWNER_SAID_MINUTES'] * 60 + 3600):
            self.app.owner_said_last = ('webchat-said:run-8', NOW.timestamp())
            with self.assertRaisesRegex(ValueError, 'owner’s own words'):
                self.save('You take the bus.')

    def test_a_connected_ais_fact_stays_marked_as_third_party_text(self):
        self.assertIn('said', a.Store.remember_fact.__code__.co_varnames)
        with self.assertRaisesRegex(ValueError, 'connected AI'):  # said never loosens what an AI's fact needs
            self.store.remember_fact('Likes tea a lot', 'telegram-said:1', source='ai:Helper', said=True)


if __name__ == '__main__':
    unittest.main()

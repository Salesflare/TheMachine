"""A to-do's chat asks (Store.set_chat_asks): up to two short things the owner may want to say in its chat, specific to
it, written by the review with the to-do (suggest's asks, no model call of their own) and shown as taps over the chat's
message box. Anything else is dropped, none rather than a canned line, and each update says them again. Sealed at rest
like the to-do's text. No Gateway, nothing sent."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import message_seal

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('chat_asks_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class ChatAsks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.store.commit_page('g', {}, [{'account_id': 'g', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': f'2026-10-28T07:0{n}:00+00:00',
                                          'title': 'Venue dates', 'body': 'Monday 9:00 or Tuesday 10:00?', 'deleted': False,
                                          'metadata': {'from': 'Alex <alex@venue.example>', 'thread_id': 't1'}} for n in (1, 2)])
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'g'}], 'prepare_ahead': False}

    def suggest(self, event_ids=(1,), **args):
        return self.app.action('suggest', {'dedupe_key': 'alex-venue', 'title': 'Reply to Alex about the venue dates',
                                           'body': 'Alex offers Monday 9:00 or Tuesday 10:00.', 'event_ids': list(event_ids), 'when': 'now', 'newer_checked': [2], **args})

    def asks(self, sid):
        with self.store.connect() as db:
            value = db.execute('SELECT chat_asks FROM suggestions WHERE id=?', (sid,)).fetchone()[0]
        return json.loads(value) if value else None

    def test_the_reviews_asks_are_kept_short_and_at_most_two(self):
        sid = self.suggest(asks=['Offer  Tuesday 10:00 instead', 'Offer Tuesday 10:00 instead', 7, '',
                                 'A line far too long to be a tap over the message box, so it is left out', 'Ask Alex for the price list', 'A third'])['id']
        self.assertEqual(self.asks(sid), ['Offer Tuesday 10:00 instead', 'Ask Alex for the price list'])

    def test_none_without_asks_and_an_update_says_them_again(self):
        sid = self.suggest()['id']
        self.assertIsNone(self.asks(sid))
        self.assertIsNone(self.asks(self.suggest(asks='Offer Tuesday')['id']))  # not a list: nothing
        self.suggest(event_ids=(1, 2), card_id=sid, asks=['Offer Tuesday 10:00 instead'])
        self.assertEqual(self.asks(sid), ['Offer Tuesday 10:00 instead'])
        self.suggest(event_ids=(1, 2), card_id=sid, dedupe_key='alex-venue-2')  # updated again without asks: none, never stale ones
        self.assertIsNone(self.asks(sid))

    def test_they_are_sealed_at_rest_like_the_to_dos_text(self):
        self.assertIn('chat_asks', message_seal.DERIVED['suggestions'])

    def test_the_review_is_told_to_leave_them_out_rather_than_be_generic(self):
        prompt = a.review_prompt('r1', ['g'])
        self.assertIn('Chat asks:', prompt)
        self.assertIn('leave asks out rather than add one', prompt)


if __name__ == '__main__':
    unittest.main()

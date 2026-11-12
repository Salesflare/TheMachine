"""A to-do waiting on someone follows the chat with them: the owner's own new follow-up, sent straight from the chat app
and not from the to-do, updates what it says it waits on. A review once read that follow-up (and the answer to it),
judged them as needing no new to-do, and left the waiting to-do saying it still waited on an older check-in. A fake
review drives the real begin_analysis, suggest and finish_analysis; no model and nothing is sent."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('waiting_followup_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
graph = a.graph
NOW = dt.datetime(2026, 10, 28, 12, 0, tzinfo=dt.timezone.utc)
CONFIG = {'accounts': [{'id': 'chat', 'service': 'whatsapp', 'email': 'Personal WhatsApp'}]}
counter = iter(range(1, 10**6))


def chat(days_ago, phone, name, body, mine=False):
    n = next(counter)
    return {'account_id': 'chat', 'source_id': f'w{n}', 'kind': 'whatsapp.message', 'occurred_at': (NOW - dt.timedelta(days=days_ago)).isoformat(),
            'title': name, 'body': body, 'deleted': False,
            'metadata': {'chat_id': phone + '@s.whatsapp.net', 'chat_name': name, 'from_me': mine, 'from': 'You' if mine else name,
                         'sender_id': None if mine else phone + '@s.whatsapp.net'}}


class WaitingFollowUp(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start()
        self.addCleanup(clock.stop)
        # Last week: they said they'd look at it; the owner checked in once. The to-do waits on them since.
        self.promise, self.check_in = self.add(chat(7, '3161', 'Kim', 'I will take a look tomorrow'),
                                               chat(6, '3161', 'Kim', 'tried?', mine=True))
        self.build()
        card = self.store.suggest('chat:kim-look', 'Waiting on Kim: take a look', 'Kim said they would look. You checked in once.',
                                  [self.promise], match=True)
        self.card = card['id']
        self.store.suggest('chat:kim-look', 'Waiting on Kim: take a look', 'You checked in with "tried?". No reply since.',
                           [self.check_in], match=True, card_id=self.card, waiting_on='Kim to reply to your first check-in')
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version')
        self.assertEqual(self.outcome()['waiting_on'], 'Kim to reply to your first check-in')

    def add(self, *events):
        for e in events:
            self.store.commit_page(e['account_id'], {}, [e])
        with self.store.connect() as db:
            return [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]

    def build(self):
        with self.store.connect() as db:
            db.isolation_level = None
            graph.build(db, {**CONFIG, 'embeddings': {'model': 'test', 'dims': 4}}, NOW.isoformat())

    def outcome(self):
        with self.store.connect() as db:
            row = db.execute('SELECT status,outcome FROM suggestions WHERE id=?', (self.card,)).fetchone()
        return {'status': row['status'], **json.loads(row['outcome'] or '{}')}

    def test_the_owners_own_follow_up_updates_what_the_to_do_waits_on(self):
        nudge, = self.add(chat(0.1, '3161', 'Kim', 'Any luck? Happy to help on a call', mine=True))
        other, = self.add(chat(0.1, '3199', 'Lee', 'See you tonight'))  # someone else: not about this to-do
        self.build()
        claim = self.store.begin_analysis(['chat'], 120)
        shown = {e['id']: e for e in claim['events']}
        self.assertEqual(shown[nudge]['waiting_card']['card_id'], self.card)
        self.assertTrue(shown[nudge]['waiting_card']['yours'])
        self.assertEqual(shown[nudge]['waiting_card']['waiting_on'], 'Kim to reply to your first check-in')
        self.assertNotIn('waiting_card', shown[other])
        # What the review did on the owner's Machine: no to-do for the new message, the waiting to-do left as it was.
        with self.assertRaisesRegex(ValueError, rf'to-do {self.card} .*event_ids \[{nudge}\].*waiting_on naming that latest follow-up'):
            self.store.finish_analysis(claim['analysis_id'], 'Outbound check-in awaits them', no_todo=[{'event_id': nudge, 'why': 'Already followed up'}])
        with self.store.connect() as db:  # refused as a whole: still to review
            self.assertEqual(db.execute('SELECT analyzed_version FROM events WHERE id=?', (nudge,)).fetchone()[0], 0)
        self.store.suggest('chat:kim-look', 'Waiting on Kim: take a look', 'You followed up again today and offered a call.',
                           [nudge], match=True, card_id=self.card, waiting_on="Kim to reply to today's follow-up")
        self.store.finish_analysis(claim['analysis_id'], 'Updated the waiting to-do')
        self.assertEqual(self.outcome(), {**self.outcome(), 'status': 'prepared', 'state': 'waiting', 'waiting_on': "Kim to reply to today's follow-up"})

    def test_their_answer_brings_it_back_and_an_unrelated_message_can_say_why(self):
        answer, = self.add(chat(0.1, '3161', 'Kim', 'Sorry, busy week, will try Friday'))
        self.build()
        claim = self.store.begin_analysis(['chat'], 120)
        self.assertFalse(next(e for e in claim['events'] if e['id'] == answer)['waiting_card']['yours'])
        with self.assertRaisesRegex(ValueError, 'Not finished yet'):
            self.store.finish_analysis(claim['analysis_id'], 'Nothing new')
        self.store.suggest('chat:kim-look', 'Kim will try Friday', 'Kim had a busy week and plans to try Friday.', [answer], match=True, card_id=self.card)
        self.store.finish_analysis(claim['analysis_id'], 'Kim answered')
        self.assertEqual(self.outcome()['status'], 'pending')  # back as an open to-do
        # A later message with them about something else: the review says why, and the to-do stays as it is.
        later, = self.add(chat(0.05, '3161', 'Kim', 'Happy birthday!', mine=True))
        self.build()
        with self.store.connect() as db:  # waiting again, as after the owner answered
            db.execute("UPDATE suggestions SET status='prepared',outcome=? WHERE id=?",
                       (json.dumps({'state': 'waiting', 'waiting_on': 'Kim to try it Friday'}), self.card))
        claim = self.store.begin_analysis(['chat'], 120)
        self.assertEqual(next(e for e in claim['events'] if e['id'] == later)['waiting_card']['card_id'], self.card)
        self.store.finish_analysis(claim['analysis_id'], 'Birthday wish', replies=[{'event_id': later, 'why': 'A birthday wish, not about it'}])
        self.assertEqual(self.outcome()['waiting_on'], 'Kim to try it Friday')

    def test_the_review_is_told(self):
        prompt = a.review_prompt('run', ['chat'])
        self.assertIn("A signal's waiting_card is such a to-do", prompt)


if __name__ == '__main__':
    unittest.main()

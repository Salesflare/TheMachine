"""A rename the owner asks for in a to-do's chat. The run saves it as their own title (as the dashboard's Rename would),
so a later review keeps it; the saved result says which title the to-do shows now, and a title_note when the one given
didn't apply, so the reply can't claim a rename that didn't happen; and the chat's own read carries the title, so the
heading and the sidebar show it with the reply (tests/test_chat_rename_dashboard.mjs). Synthetic data only."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import machine.main as machine_main

ROOT = Path(__file__).parent.parent
TITLE = 'Send Sam the bounty receipt'
NEW = 'Gather and send Sam the receipt and two invoices by Tuesday'


def mail(n, body, day=21):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': f'2026-10-{day}T09:00:00+00:00',
            'title': 'Bounty', 'body': body, 'deleted': False,
            'metadata': {'from': 'Sam <sam@example.com>', 'to': 'owner@example.com', 'thread_id': 't1', 'labels': ['INBOX']}}


class ChatRename(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'service': 'gmail', 'transport': 'gog', 'email': 'owner@example.com', 'boundary': 'work:Example'}]}
        self.store.commit_page('work', {}, [mail(1, 'Thanks, it arrived. Could you send me a receipt?')])
        self.sid = self.store.suggest('bounty', TITLE, 'Sam asks for a receipt. I can send it.', [1])['id']

    def card(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT title,title_suggested,title_source FROM suggestions WHERE id=?', (self.sid,)).fetchone())

    def turn(self, text, key, choice='other'):
        """The owner writes in the to-do's chat (choice other) or taps Do it (accept): its run starts."""
        self.store.decide(self.sid, choice, text, key, 'dashboard')
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='running'")
            return db.execute('SELECT job_id FROM preparations').fetchone()[0]

    def save(self, job, **extra):
        return self.app.action('prepare', {'suggestion_id': self.sid, 'job_id': job, 'body': 'The files are still to send.',
                                           'outcome': 'needs_you', 'needs': 'send the files', 'note_kind': 'continue', **extra})

    def finish(self, job, **extra):
        return self.save(job, body='Sent.', outcome='done', **{'needs': None, **extra})

    def test_a_rename_asked_in_the_chat_is_their_own_title(self):
        saved = self.save(self.turn(f'Rename it to "{NEW}"', 'chat-1'), title=NEW, rename=True)
        self.assertEqual(saved['title'], NEW)
        self.assertNotIn('title_note', saved)
        self.assertEqual(self.card(), {'title': NEW, 'title_suggested': TITLE, 'title_source': 'user'})
        # A later review keeps their title; its own waits for Reset
        self.store.commit_page('work', {}, [mail(2, 'Any news on the receipt?', day=22)])
        self.store.suggest('bounty-2', 'Reply to Sam about the receipt', 'Sam asks again.', [2], card_id=self.sid, match=True)
        self.assertEqual(self.card()['title'], NEW)

    def test_a_rename_replaces_a_title_they_gave_before(self):
        self.store.rename_card(self.sid, 'Receipt for Sam', decision_id='rename-1')
        self.save(self.turn(f'Call it "{NEW}"', 'chat-1'), title=NEW, rename=True)
        self.assertEqual(self.card(), {'title': NEW, 'title_suggested': TITLE, 'title_source': 'user'})

    def test_a_rename_also_holds_on_a_result_that_finishes_it(self):
        saved = self.finish(self.turn(f'Rename it to "{NEW}", it is done', 'chat-1'), title=NEW, rename=True)
        self.assertEqual((saved['title'], self.card()['title']), (NEW, NEW))

    def test_a_generated_title_that_did_not_apply_says_so(self):
        # Their own title stays over a generated one: the result names the title it kept, so the reply doesn't say renamed
        self.store.rename_card(self.sid, 'Receipt for Sam', decision_id='rename-1')
        saved = self.save(self.turn('What is left here?', 'chat-1'), title=NEW)
        self.assertEqual(saved['title'], 'Receipt for Sam')
        self.assertIn('Title not changed', saved['title_note'])
        self.assertIn("Don't say it was renamed", saved['title_note'])
        self.assertEqual(self.card()['title'], 'Receipt for Sam')

    def test_a_finishing_result_keeps_the_title_and_says_so(self):
        saved = self.finish(self.turn('It is done', 'chat-1'), title=NEW)
        self.assertEqual(saved['title'], TITLE)
        self.assertIn('finishes the to-do', saved['title_note'])

    def test_a_result_without_a_title_names_the_current_one_quietly(self):
        saved = self.save(self.turn('What is left here?', 'chat-1'))
        self.assertEqual(saved['title'], TITLE)
        self.assertNotIn('title_note', saved)

    def test_rename_needs_the_owners_own_message(self):
        with self.assertRaisesRegex(ValueError, 'rename needs the owner'):
            self.save(self.turn('', 'tap', 'accept'), title=NEW, rename=True)
        self.assertEqual(self.card()['title'], TITLE)
        with self.assertRaisesRegex(ValueError, 'rename is true or false'):
            self.save(self.turn('Rename it', 'chat-2'), title=NEW, rename='yes')

    def test_the_chat_read_carries_the_title(self):
        self.save(self.turn(f'Rename it to "{NEW}"', 'chat-1'), title=NEW, rename=True)
        with patch.object(machine_main.App, 'card_chat_gateway', return_value={'kind': 'delta', 'messages': [], 'deltaCursor': 'c1'}):
            read = self.app.card_chat(self.sid)
            again = self.app.card_chat(self.sid, read['cursor'])
        self.assertEqual((read['title'], read['title_suggested']), (NEW, TITLE))
        self.assertTrue(again.get('unchanged'))
        self.assertEqual(again['title'], NEW)  # also on a read where the conversation didn't move

    def test_the_instructions_say_it(self):
        text = (ROOT / 'machine/app/preparation.py').read_text()
        self.assertIn('asks to rename the to-do, add title=<their name for it, under 90 characters> and rename:true', text)
        self.assertIn('with a title_note, say it wasn\'t', text)


if __name__ == '__main__':
    unittest.main()

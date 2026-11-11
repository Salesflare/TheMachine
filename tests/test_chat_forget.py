"""The owner asks their main chat to forget something learned (the bridge's assistant_forget, forget_learned): one clear
match of their own is forgotten as Learning's Remove does it and is gone from every reader; several or none come back
for the chat to ask; a connected AI's fact is never forgotten this way; Undo in Activity (or in the chat) brings it
back. A temporary store with made-up data. No model call, no send."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('chat_forget_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import activity_log  # noqa: E402
import learning_loop  # noqa: E402
from machine.app import ask_memory  # noqa: E402

NOW = dt.datetime(2026, 11, 10, 7, tzinfo=dt.timezone.utc)
MOVED = 'You moved to Ghent last spring.'
KLM = 'You fly KLM to Rome.'
KLM_TOO = 'You fly KLM to Oslo for work.'
AI = 'You moved to Antwerp in the summer.'


class ChatForget(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.store = a.Store(self.dir / 'events.sqlite')
        self.config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}], 'timezone': 'Europe/Brussels',
                       'database': str(self.dir / 'events.sqlite'), 'openclaw_workspace': str(self.dir / 'ws')}
        self.store.config = self.config
        self.store.accounts = self.config['accounts']
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        with self.store.connect() as db:  # the owner's own, from their notes; and a connected AI's, not the owner's word
            self.ids = {text: db.execute("INSERT INTO facts(text,decision_id,created_at,kind) VALUES(?,'note-1',?,'fact')", (text, NOW.isoformat())).lastrowid
                        for text in (MOVED, KLM, KLM_TOO, 'You go to the gym on Tuesdays.')}
            self.ai = db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES(?,'ai:c1',?,'fact','ai:Claude','work')",
                                 (AI, NOW.isoformat())).lastrowid
            db.execute("INSERT INTO fact_vectors(fact_id,model,vector) VALUES(?,'m:2',x'00')", (self.ids[MOVED],))
        self.app.action('web_chat_said', {'message_id': 'run-1'})  # the owner just wrote in their own chat

    def forget(self, **args):
        return self.app.action('forget_learned', {'_owner_chat': True, **args})

    def current(self):
        return {f['text'] for f in self.store.facts()}

    def readers(self, words):
        """What the main chat, Ask and Talk find for these words."""
        chat = self.app.action('recall_learned', {'words': words, '_owner_chat': True})['found']
        ask = ask_memory.facts(self.app, {'area': None, 'subjects': [], 'accounts': ['work'], 'question': words}, 1000)
        talk = ' '.join(f['text'] for f in ask_memory.learned(self.store, words))
        return chat, ask, talk

    def activity(self):
        with self.store.connect() as db:
            return [x for x in activity_log.page(db, self.config)['items'] if x['kind'] == 'memory']

    def test_one_clear_match_is_forgotten_everywhere_and_undo_brings_it_back(self):
        self.assertTrue(all(MOVED in found for found in self.readers('moved to Ghent')))
        done = self.forget(words='that I moved to Ghent')
        self.assertEqual(done['forgot'], MOVED)
        self.assertNotIn(MOVED, self.current())
        for found in self.readers('moved to Ghent'):
            self.assertNotIn('Ghent', found)
        with self.store.connect() as db:  # as Learning's Remove: the row stays, its vector goes
            self.assertIsNotNone(db.execute('SELECT removed_at FROM facts WHERE id=?', (self.ids[MOVED],)).fetchone()[0])
            self.assertIsNone(db.execute('SELECT 1 FROM fact_vectors WHERE fact_id=?', (self.ids[MOVED],)).fetchone())
        line, = self.activity()
        self.assertEqual(line['what'], 'Forgot: ' + MOVED)
        self.assertFalse(line['what'].startswith('You'))
        self.assertEqual(line['undo'], {'action': 'learning_undo', 'id': done['undo']})
        with self.store.connect() as db:  # Learning, Changes has it too, with the same Undo
            self.assertEqual([(c['kind'], c['text']) for c in learning_loop.recent(db)], [('forgot', MOVED)])
        self.app.action('learning_undo', {'id': line['undo']['id']}, owner_dashboard=True)  # Undo in Activity
        self.assertIn(MOVED, self.current())
        self.assertTrue(all(MOVED in found for found in self.readers('moved to Ghent')))
        line, = self.activity()
        self.assertEqual((line['outcome'], line['undo']), ('undone', None))

    def test_the_chat_can_undo_what_it_just_forgot(self):
        done = self.forget(words='moved to Ghent')
        self.assertEqual(self.forget(undo=done['undo']), {'brought_back': True})
        self.assertIn(MOVED, self.current())
        with self.assertRaisesRegex(ValueError, 'already undone'):
            self.forget(undo=done['undo'])

    def test_an_unclear_request_asks_which_one_and_forgets_nothing(self):
        before = self.current()
        done = self.forget(words='flying KLM')
        self.assertIsNone(done['forgot'])
        self.assertEqual({c['text'] for c in done['candidates']}, {KLM, KLM_TOO})
        none = self.forget(words='quarterly board budget')
        self.assertEqual((none['forgot'], none.get('candidates')), (None, None))
        self.assertEqual(self.current(), before)
        self.assertEqual(self.activity(), [])
        # the owner picks one: only an id the chat was offered
        self.assertEqual(self.forget(words='flying KLM')['forgot'], None)
        with self.assertRaisesRegex(ValueError, 'candidates this tool offered'):
            self.forget(id=self.ids[MOVED])
        self.assertEqual(self.forget(id=self.ids[KLM_TOO])['forgot'], KLM_TOO)
        self.assertEqual(self.current(), before - {KLM_TOO})
        with self.assertRaisesRegex(ValueError, 'candidates this tool offered'):  # an offer is used once
            self.forget(id=self.ids[KLM])

    def test_a_connected_ais_fact_is_never_forgotten_this_way(self):
        done = self.forget(words='moved to Antwerp')
        self.assertIsNone(done['forgot'])
        self.assertNotIn(AI, [c['text'] for c in done.get('candidates', [])])
        with self.assertRaisesRegex(ValueError, 'candidates this tool offered'):
            self.forget(id=self.ai)
        self.assertIn(AI, self.current())
        # "moved" alone: only the owner's own fact, never the AI's, so it is the one clear match
        self.assertEqual(self.forget(words='where I moved')['forgot'], MOVED)
        self.assertIn(AI, self.current())

    def test_only_on_the_owners_own_request_in_their_own_chat(self):
        with self.assertRaisesRegex(ValueError, 'own main chat'):
            self.app.action('forget_learned', {'words': 'moved to Ghent'})
        self.app.owner_said_last = None  # nothing the owner wrote lately
        with self.assertRaisesRegex(ValueError, 'Forget only when the owner asks'):
            self.forget(words='moved to Ghent')
        self.assertIn(MOVED, self.current())
        self.assertIn('forget_learned', a.OWNER_ACTIONS)  # never the local CLI, the agent's own tool
        self.assertNotIn('forget_learned', a.DASHBOARD_ACTIONS)


if __name__ == '__main__':
    unittest.main()

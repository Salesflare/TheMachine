"""One fact through its whole life across every surface, the way the owner lives it, on a store file with made-up data:
said in passing in the web chat and in their private chat (no "remember this"), read back by the main chat
(assistant_memory), Ask, a to-do's preparation and chat, and Talk; corrected in plain words; removed; and each step
again after a restart (a fresh Store and App on the same database file, as a new process opens it). Then scope and
privacy: a fact about a Personal person never reaches a Work to-do, Ask in Work or the team, a connected AI's fact
is never the owner's word, and each surface keeps to its budget.

The chat model is played by the test: it calls the tools the bridge gives it (openclaw-plugin/index.ts) with the
arguments they take, through App.action as the bridge's call does. Embeddings are a made-up local function. No model
call, no send."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('memory_e2e_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import team_learnings  # noqa: E402
from machine.app import ask_memory  # noqa: E402
from machine.app import retained_facts  # noqa: E402
from machine.app.recall import recall  # noqa: E402
from machine.export import knowledge  # noqa: E402
from machine.store.facts import AI_FACTS_HEAD, suggestion_scope  # noqa: E402

NOW = dt.datetime(2026, 11, 10, 9, tzinfo=dt.timezone.utc)
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 3}
ANN = 'email:ann@client.example'
MIA = 'email:mia.example@gmail.com'

# What the owner says, and the one sentence the chat model saves from it (the tool asks for one plain sentence)
GHENT_SAID, GHENT = 'btw I moved to Ghent last month', 'You moved to Ghent last month.'
KLM_SAID, KLM = 'I only fly KLM these days', 'You only fly KLM these days.'
ANTWERP_SAID, ANTWERP = "actually it's Antwerp, not Ghent", 'You moved to Antwerp last month.'
MIA_SAID, MIA_FACT = 'oh and Mia is allergic to peanuts', 'Mia Example is allergic to peanuts.'
AI_FACT = 'Ann Example says you fly Lufthansa these days.'  # a connected AI's claim


def embed(settings, texts, timeout=120):
    """Made-up vectors: where the owner lives, how they fly and the rest each point their own way."""
    out = []
    for t in texts:
        low = t.casefold()
        out.append([1.0, 0.0, 0.0] if any(w in low for w in ('ghent', 'antwerp', 'move', 'live', 'home')) else
                   [0.0, 1.0, 0.0] if any(w in low for w in ('fly', 'flight', 'klm', 'airline')) else [0.0, 0.0, 1.0])
    return out


def mail(n, account, sender, to, title, body, labels=('INBOX',)):
    return {'account_id': account, 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=1, hours=n)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'cc': '', 'labels': list(labels), 'message-id': f'<m{n}@x>', 'thread_id': f't{n}'}}


class MemoryEndToEnd(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.path = self.dir / 'events.sqlite'
        self.config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme.example'},
                                    {'id': 'home', 'email': 'sam@mail.example'}],
                       'telegram_owner': '1000001', 'owner_name': 'Sam Owner', 'timezone': 'Europe/Brussels', 'database': str(self.path),
                       'openclaw_workspace': str(self.dir / 'ws'), 'openclaw_state': str(self.dir / 'none.sqlite'), 'embeddings': SETTINGS}
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        embedder = patch.object(a.embeddings, 'embed', side_effect=embed)
        embedder.start()
        self.addCleanup(embedder.stop)
        self.reopen()
        self.store.commit_page('work', {}, [mail(1, 'work', 'Ann Example <ann@client.example>', 'sam@acme.example', 'Fair', 'Shall we meet at the fair in Amsterdam?')])
        self.store.commit_page('home', {}, [mail(2, 'home', 'Mia Example <mia.example@gmail.com>', 'sam@mail.example', 'Sunday', 'Dinner at ours on Sunday?')])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.config, NOW.isoformat())
        with self.store.connect() as db:
            a.graph.person_edit(db, MIA, {'side': 'personal'}, NOW.isoformat())  # the owner set her Type to Personal
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.config, NOW.isoformat())
            events = {r[0]: r[1] for r in db.execute('SELECT source_id,id FROM events')}
        self.work_todo = self.store.suggest('fair', 'Book the flight to the Amsterdam fair', 'Ann asks to meet at the fair in Amsterdam.', [events['m1']])['id']
        self.home_todo = self.store.suggest('dinner', 'Answer Mia about Sunday dinner', 'Mia asks you to dinner on Sunday.', [events['m2']])['id']
        self.app.memory_search = lambda request: {'error': 'off'}

    def reopen(self):
        """A fresh process: a new Store and App on the same database file, nothing carried over in memory."""
        self.store = a.Store(self.path)
        self.store.config = self.config
        self.store.accounts = self.config['accounts']
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        self.app.memory_search = lambda request: {'error': 'off'}

    # The chat model's side: what the owner wrote reaches the service as the bridge sends it, then the model saves
    def web_chat(self, said, n, saved, **args):
        """The owner writes in the web chat's main session: before_dispatch notes the message's id (never the words),
        then the model calls assistant_remember, which the bridge sends as remember_fact with its chat mark."""
        self.assertTrue(said)
        self.app.action('web_chat_said', {'message_id': f'run-{n}'})
        return self.app.action('remember_fact', {'text': saved, '_owner_chat': True, **args})

    def private_chat(self, said, n, saved, **args):
        """The owner writes in their private Telegram chat: feedback_reply takes the message (owner key), then the model
        calls assistant_signals remember_fact, and the bridge adds the chat mark (privateMain)."""
        self.app.action('feedback_reply', {'text': said, 'message_id': str(n), 'timestamp': NOW.timestamp(), 'reply_to_id': ''})
        return self.app.action('remember_fact', {'text': saved, '_owner_chat': True, **args})

    def ai_fact(self):
        """A connected AI saves a fact about Ann (ai_app.py's path: source ai:<name>, an area, about someone)."""
        return self.store.remember_fact(AI_FACT, 'ai:c1', about=[ANN], source='ai:Helper', side='work')['id']

    # The surfaces, each read the way its own code path reads it
    def main_chat(self, words):
        return self.app.action('recall_learned', {'words': words, '_owner_chat': True})['found']

    def ask(self, question, area=None, room=1000):
        accounts = [x['id'] for x in self.config['accounts'] if area is None or suggestion_scope([x['id']], self.config['accounts']) == area]
        return ask_memory.facts(self.app, {'area': area, 'subjects': [], 'accounts': accounts, 'question': question}, room)

    def preparation(self, todo):
        memory = recall(self.app, 'preparation', {'todo': todo})
        return memory.text('facts') + '\n' + memory.text('retained')

    def talk(self, words):
        return [f['text'] for f in self.app.talk_recall(words)['found']]

    def chat_turn(self, n, text):
        """The owner writes in the Work to-do's chat; its turn runs in the preparation's session. Its message."""
        with self.store.connect() as db:
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=? WHERE finished_at IS NULL", (NOW.isoformat(),))
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (self.work_todo,))
        self.store.decide(self.work_todo, 'other', text, f'chat-{n:036d}', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c['message'] for c in calls if c.get('message'))

    def start_preparation(self):
        self.store.decide(self.work_todo, 'accept', '', 'click', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c['message'] for c in calls if c.get('message'))

    def everywhere(self):
        """Every surface's text for questions about where the owner lives, as one list of (surface, text)."""
        return [('main chat', self.main_chat('where did I move')), ('main chat', self.main_chat('Ghent')), ('main chat', self.main_chat('Antwerp')),
                ('ask', self.ask('Where did I move to?')), ('ask work', self.ask('Where did I move to?', 'work')),
                ('preparation', self.preparation(self.work_todo)), ('talk', '\n'.join(self.talk('where I moved'))),
                ('talk', '\n'.join(self.talk('Ghent'))), ('talk', '\n'.join(self.talk('Antwerp')))]

    def export(self):
        reader = knowledge.StoreReader(self.store, self.config)
        return [f['text'] for f in reader.facts()], [f['text'] for f in reader.fact_history()]

    def fact(self, fact_id):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM facts WHERE id=?', (fact_id,)).fetchone())

    def never_current(self, surfaces, word):
        """word shows nowhere, or only in a line marked as history."""
        for name, found in surfaces:
            for line in str(found).splitlines():
                if word in line:
                    self.assertIn(retained_facts.HISTORY, line, (name, line))

    def nowhere(self, surfaces, word):
        for name, found in surfaces:
            self.assertNotIn(word, str(found), name)

    def test_said_in_passing_found_everywhere_corrected_and_forgotten_also_after_a_restart(self):
        # 1. Said in passing, no "remember": the web chat and the private chat path each save one, tied to the message
        self.assertNotIn('remember', GHENT_SAID + KLM_SAID)
        ghent = self.web_chat(GHENT_SAID, 1, GHENT)['id']
        klm = self.private_chat(KLM_SAID, 801, KLM, kind='preference')['id']
        row = self.fact(ghent)
        self.assertEqual((row['decision_id'], row['source'], row['side'], row['suggestion_id']), ('webchat-said:run-1', None, None, None))
        row = self.fact(klm)
        self.assertEqual((row['decision_id'], row['source'], row['side'], row['fact_kind']), ('telegram-said:801', None, None, 'preference'))
        self.assertIsNone(a.ai_fact_by(row))  # the owner's own word; no area of its own: about no one, so it holds in Work and Personal
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM fact_about WHERE fact_id IN (?,?)', (ghent, klm)).fetchone()[0], 0)
        for restarted in (False, True):
            if restarted:
                self.reopen()
            # 2. Asked later: the main chat, Ask (with and without embeddings), a preparation and Talk each find both
            self.assertIn(GHENT, self.main_chat('where did I move'))
            self.assertIn(KLM, self.main_chat('which airline do I fly'))
            self.assertIn(GHENT, self.ask('Where did I move to?'))
            self.assertIn(KLM, self.ask('Which airline do I fly?', 'work'))
            self.assertIn(KLM, self.ask('Which airline do I fly?', 'personal'))
            with patch.dict(self.config, {'embeddings': None}):
                self.assertIn(GHENT, self.ask('Where did I move to?'))
                self.assertIn(KLM, self.talk('flying KLM')[0])
            facts = self.preparation(self.work_todo)
            self.assertIn(GHENT, facts)
            self.assertIn(KLM, facts)
            self.assertIn(GHENT, self.talk('where I moved')[0])
            self.assertIn(KLM, self.talk('which airline I fly')[0])
            self.assertEqual(self.export()[0], [GHENT, KLM])

        # The Work to-do's preparation starts, then the owner corrects in the web chat
        self.assertIn(GHENT, self.start_preparation())
        clock = [NOW + dt.timedelta(hours=1)]
        later = patch_everywhere(a, 'now', lambda: clock[0].isoformat())
        later.start()
        self.addCleanup(later.stop)
        # 3. A correction in plain words: the new one takes the old one's place; the old one is history only
        antwerp = self.web_chat(ANTWERP_SAID, 2, ANTWERP)
        self.assertEqual(antwerp['replaced'], ghent)
        antwerp = antwerp['id']
        self.assertEqual(self.fact(ghent)['merged_into'], f'fact:{antwerp}')
        for restarted in (False, True):
            if restarted:
                self.reopen()
            surfaces = self.everywhere()
            for name, found in surfaces[:1] + surfaces[3:7]:
                self.assertIn(ANTWERP, found, name)
            self.never_current(surfaces, 'Ghent')
            history = [line for line in self.main_chat('Ghent').splitlines() if 'Ghent' in line]
            self.assertEqual(len(history), 1)  # the main chat can still say it was Ghent, marked as history
            self.assertTrue(history[0].startswith('- ' + retained_facts.HISTORY), history[0])
            current, past = self.export()
            self.assertEqual(current, [KLM, ANTWERP])
            self.assertIn(GHENT, past)  # the export keeps it as history, apart from what holds
        chat = self.chat_turn(1, 'Which airport is closest to home?')
        block = chat[chat.index(retained_facts.NEW_HEAD):].split('\n\n')[0]
        self.assertIn(ANTWERP, block)  # the to-do chat's session read Ghent: told what changed
        self.never_current([('to-do chat', block)], 'Ghent')

        # 4. Forgotten: removed under Learning. Gone from every surface, the indexes and the export
        clock[0] = NOW + dt.timedelta(hours=2)
        self.app.action('forget_fact', {'id': antwerp}, owner_dashboard=True)
        chat = self.chat_turn(2, 'And from the office?')
        block = chat[chat.index(retained_facts.NEW_HEAD):].split('\n\n')[0]
        self.assertIn(retained_facts.GONE, block)  # the to-do chat's session had it: told to stop using it
        for restarted in (False, True):
            if restarted:
                self.reopen()
            surfaces = self.everywhere()
            for word in ('Ghent', 'Antwerp', 'moved'):
                self.nowhere(surfaces, word)
            self.assertIn(KLM, self.main_chat('which airline do I fly'))  # the rest stays
            current, past = self.export()
            self.assertEqual(current, [KLM])
            self.assertFalse([t for t in past if 'Ghent' in t or 'Antwerp' in t], past)
            self.assertEqual([f['id'] for f in self.store.facts()], [klm])
            with self.store.connect() as db:
                self.assertEqual(db.execute('SELECT count(*) FROM fact_vectors WHERE fact_id IN (?,?)', (ghent, antwerp)).fetchone()[0], 0)
                # the keyword index (fact_search) still holds the removed row's words, as the row stays behind as a
                # tombstone (a review saving it again is suppressed; Undo merge); what reads the index finds nothing
                self.assertEqual(retained_facts.candidates(db, retained_facts.starting(db, {'ghent', 'antwerp', 'mov'})), [])
                self.assertEqual(retained_facts.candidates(db, [ghent, antwerp]), [])
            chat = self.chat_turn(3 + int(restarted), 'Anything else?')  # told once: the next turns say nothing of it
            for word in ('Ghent', 'Antwerp'):
                self.assertNotIn(word, chat)

    def test_a_personal_fact_stays_out_of_work_and_the_team_and_an_ais_fact_is_not_the_owners(self):
        mia = self.private_chat(MIA_SAID, 901, MIA_FACT, about=[MIA])
        self.assertEqual(mia['about'], [MIA])
        klm = self.private_chat(KLM_SAID, 902, KLM, kind='preference')['id']
        ai = self.ai_fact()
        with self.store.connect() as db:
            side = {r[0]: json.loads(r[1] or '{}').get('side') for r in db.execute('SELECT id,info FROM graph_nodes WHERE id IN (?,?)', (MIA, ANN))}
        self.assertEqual(side, {MIA: 'personal', ANN: 'work'})
        for restarted in (False, True):
            if restarted:
                self.reopen()
            # Personal: on Mia's to-do and in the owner's own chat when they name her; never on a Work to-do or in Work's Ask
            self.assertIn(MIA_FACT, self.preparation(self.home_todo))
            self.assertNotIn('peanuts', self.preparation(self.work_todo))
            self.assertIn(MIA_FACT, self.main_chat('is Mia allergic to anything'))
            self.assertNotIn('peanuts', self.main_chat('who is allergic to peanuts'))  # not named: not hers
            self.assertNotIn('peanuts', self.ask('Who is allergic to peanuts?', 'work'))
            self.assertIn(MIA_FACT, self.ask('Who is allergic to peanuts?', 'personal'))
            with patch.dict(self.config, {'embeddings': None}):
                self.assertNotIn('peanuts', self.ask('Who is allergic to peanuts?', 'work'))
            with self.store.connect() as db:  # never to the team: not in what the learnings turn reads
                rows = team_learnings.evidence(db, current=NOW + dt.timedelta(minutes=1), accounts=self.config['accounts'])['rows']
            texts = [r.get('text') for r in rows if r['what'] == 'fact']
            self.assertIn(KLM, texts)
            self.assertNotIn(MIA_FACT, texts)
            self.assertNotIn(AI_FACT, texts)
            # A connected AI's fact: never read back as the owner's word, only as that AI's data where it is about the to-do
            self.assertNotIn('Lufthansa', self.main_chat('which airline do I fly'))
            self.assertEqual([t for t in self.talk('fly these days') if 'Lufthansa' in t], [])
            with patch.dict(self.config, {'embeddings': None}):
                self.assertNotIn('Lufthansa', self.ask('Which airline do I fly these days?', 'work'))
            facts = recall(self.app, 'preparation', {'todo': self.work_todo}).text('facts')
            self.assertIn(KLM, facts)
            self.assertGreater(facts.index(AI_FACT), facts.index(AI_FACTS_HEAD))  # inside the AI's data block
            self.assertNotIn('Lufthansa', self.preparation(self.home_todo))  # its area is Work
        # a correction is never made against an AI's fact, nor does an AI's fact replace the owner's
        said = self.private_chat('I only fly Lufthansa these days', 903, 'You only fly Lufthansa these days.', kind='preference')
        self.assertEqual(said.get('replaced'), klm)
        self.assertEqual(self.fact(ai)['removed_at'], None)

    def test_every_surface_keeps_to_its_budget(self):
        for n in range(40):  # many facts that all match the same words
            self.private_chat(f'flight note {n}', 1000 + n, f'Flight note number {n}: you fly KLM from gate area {n} with a window seat and {"extra " * 6}legroom.')
        found = self.main_chat('which flights do I fly KLM')
        self.assertTrue(found)
        self.assertLessEqual(len(found), ask_memory.CHAT_CHARS)
        self.assertLessEqual(len(self.talk('fly KLM')), ask_memory.LEARNED)
        block = self.ask('Which flights do I fly with KLM?', room=500)
        self.assertLessEqual(len(block), 500)
        self.assertLessEqual(block.count('[F'), ask_memory.FACTS)
        memory = recall(self.app, 'preparation', {'todo': self.work_todo})
        self.assertLessEqual(len(memory.text('facts')), 3000)
        self.assertLessEqual(len(memory.text('retained')), retained_facts.CHARS)
        self.start_preparation()
        clock = patch_everywhere(a, 'now', lambda: (NOW + dt.timedelta(hours=1)).isoformat())
        clock.start()
        self.addCleanup(clock.stop)
        for n in range(6):
            self.private_chat(f'flight extra {n}', 2000 + n, f'Flight extra {n}: KLM lounges at the Amsterdam fair airport gate {n}.')
        chat = self.chat_turn(1, 'Which flight to the Amsterdam fair?')
        block = chat[chat.index(retained_facts.NEW_HEAD):].split('\n\n')[0]
        self.assertLessEqual(len(block), retained_facts.NEW_CHARS)
        self.assertLessEqual(block.count('\n- '), retained_facts.NEW_LINES)


if __name__ == '__main__':
    unittest.main()

"""What the owner's Machine learns reaches the work that needs it (docs/memory-reach.md): for each way knowledge comes
in (the owner's chat and corrections, what a review learns from messages, the owner's OpenClaw notes) and each
workflow that should use it (chat answers, reviews, preparations and drafts, routines, the morning digest), the path
from one to the other, on a temporary store with made-up data. No model call, no send."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('memory_reach_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import bring_in  # noqa: E402
import memory_use  # noqa: E402
from machine.app import ask_memory  # noqa: E402
from machine.app import retained_facts  # noqa: E402
from machine.app import recall as recall_module  # noqa: E402
from machine.app.recall import recall  # noqa: E402
from machine.store import voices  # noqa: E402

NOW = dt.datetime(2026, 11, 10, 7, tzinfo=dt.timezone.utc)  # a Tuesday, 08:00 in Brussels
TODAY = '2026-11-10'
ANN = 'email:ann@client.example'
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}

# One thing learned through each way in
SAID = 'You only book aisle seats on flights.'                     # the owner's own chat: "remember ..."
FIXED = 'Lee Park handles the invoices now, not Ann.'               # a correction on a to-do
NOTE = 'Quotes always go out as a PDF, never as a link.'           # MEMORY.md, ticked under Bring these in
NOTE_RULE = 'Sign every email with the first name only.'           # MEMORY.md, a rule
NOTE_ANN = 'Ann Example is vegetarian.'                            # USER.md, about someone: on her page
PROMISED = 'send the revised quote'                                # a review read it in the owner's own mail
ROLE = 'Head of Procurement'                                       # a review read it in Ann's signature


def mail(n, sender, to, title, body, labels=('INBOX',)):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(days=1, hours=n)).isoformat(),
            'title': title, 'body': body, 'deleted': False,
            'metadata': {'from': sender, 'to': to, 'cc': '', 'labels': list(labels), 'message-id': f'<m{n}@x>', 'thread_id': 't1'}}


def embed(settings, texts, timeout=120):
    """Made-up vectors: the flight fact and a question about seats are close, everything else far."""
    return [[1.0, 0.0] if 'aisle' in t or 'seat' in t else [0.0, 1.0] for t in texts]


def fly(settings, texts, timeout=120):
    """Made-up vectors: anything about flying is close to the rest of it, everything else far."""
    return [[1.0, 0.0] if 'fly' in t or 'flight' in t else [0.0, 1.0] for t in texts]


def plane(settings, texts, timeout=120):
    """Made-up vectors: flying, flights and planes are close; any other question far from every fact."""
    return [[1.0, 0.0, 0.0] if any(w in t for w in ('fly', 'flight', 'plane')) else
            [0.0, 0.0, 1.0] if t.startswith(a.embeddings.QUERY_PREFIX) else [0.0, 1.0, 0.0] for t in texts]


class MemoryReach(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.store = a.Store(self.dir / 'events.sqlite')
        self.config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example', 'boundary': 'work:acme.example'}], 'telegram_owner': '1000001',
                       'owner_name': 'Sam Owner', 'timezone': 'Europe/Brussels', 'database': str(self.dir / 'events.sqlite'),
                       'openclaw_workspace': str(self.dir / 'ws'), 'openclaw_state': str(self.dir / 'none.sqlite')}
        self.store.config = self.config
        self.store.accounts = self.config['accounts']
        self.app = object.__new__(a.App)
        self.app.store, self.app.config = self.store, self.config
        started = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        started.start()
        self.addCleanup(started.stop)
        self.store.commit_page('work', {}, [
            mail(1, 'Ann Example <ann@client.example>', 'sam@acme.example', 'Contract', f'Can we sign this week?\n\nAnn Example\n{ROLE}, Client Co'),
            mail(2, 'Sam Owner <sam@acme.example>', 'ann@client.example', 'Re: Contract', 'I will send the revised quote tomorrow.', ('SENT',))])
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.config, NOW.isoformat())
        self.todo = self.store.suggest('contract', 'Answer Ann about the contract', 'Ann asks to sign this week.', [1])['id']
        # 1. The owner's chat: a fact they state in their own private chat, and a correction on a to-do
        self.app.action('feedback_reply', {'text': 'remember that I only book aisle seats', 'message_id': '501', 'timestamp': NOW.timestamp(), 'reply_to_id': ''})
        self.app.action('remember_fact', {'text': SAID, '_owner_chat': True})
        other = self.store.suggest('invoice', 'Pay the Client Co invoice', 'An invoice came in.', [1])['id']
        self.store.decide(other, 'reject', 'Lee handles invoices now', 'note-1', 'dashboard')
        self.app.action('remember_fact', {'text': FIXED, 'decision_id': 'note-1'})
        # 2. Messages: what a review learned from the mail (a promise the owner made, Ann's role)
        self.store.promise({'direction': 'mine', 'event_id': 2, 'who': 'Ann Example', 'what': PROMISED, 'due': TODAY})
        with self.store.connect() as db:
            a.graph.set_role(db, ANN, ROLE, 'agent', NOW.isoformat(), 1, ROLE)
        # 3. The owner's OpenClaw notes: lines they ticked under Bring these in, one then put on Ann's page
        with self.store.connect() as db:
            bring_in.ensure(db)
            ids = [db.execute('INSERT INTO bring_in_items(file,key,text,kind,created_at) VALUES(?,?,?,?,?)', (file, f'k{n}', text, kind, NOW.isoformat())).lastrowid
                   for n, (file, text, kind) in enumerate((('MEMORY.md', NOTE, 'preference'), ('MEMORY.md', NOTE_RULE, 'rule'), ('USER.md', NOTE_ANN, 'fact')))]
        self.assertEqual(bring_in.decide(self.store, keep=ids)['saved'], 3)
        with self.store.connect() as db:  # its own words name her (fact_links); notes_people.py ties the ones that don't
            self.assertEqual([tuple(r) for r in db.execute('SELECT f.text,a.node_id FROM fact_about a JOIN facts f ON f.id=a.fact_id')], [(NOTE_ANN, ANN)])

    def learned(self):
        return (SAID, FIXED, NOTE, NOTE_ANN)

    def test_a_review_reads_what_came_in_every_way(self):
        memory = recall(self.app, 'review', {'run': 'review-1'})
        facts = memory.text('facts')
        for text in self.learned():
            self.assertIn(text, facts)
        self.assertIn(PROMISED, memory.text('promises'))
        self.assertIn('[', facts)  # with ids: a newer message can end one

    def test_a_preparation_and_its_draft_read_what_came_in_every_way(self):
        memory = recall(self.app, 'preparation', {'todo': self.todo})
        facts, rules = memory.text('facts'), memory.text('rules')
        for text in self.learned():
            self.assertIn(text, facts)  # few: all of them
        self.assertIn(NOTE_RULE, rules)
        self.assertIn(ROLE, memory.text('records'))  # what a review read about Ann, on the to-do's record
        # the to-do's chat runs in this preparation's session (preparation.chat_prompt): it has what this prompt had

    def test_a_correction_said_in_chat_takes_the_place_of_the_fact_it_corrects(self):
        said = lambda text, n, **args: (self.app.action('feedback_reply', {'text': text, 'message_id': str(n), 'timestamp': NOW.timestamp(), 'reply_to_id': ''}),
                                        self.app.action('remember_fact', {'text': text, '_owner_chat': True, **args}))[1]
        old = said('Your office is in Ghent.', 601)
        new = said('Your office is in Brussels now.', 602)
        self.assertEqual(new['replaced'], old['id'])  # the chat saw no ids; code found the one it corrects
        facts = recall(self.app, 'preparation', {'todo': self.todo}).text('facts')
        self.assertIn('Brussels', facts)
        self.assertNotIn('Ghent', facts)  # never both values in one draft
        drink = said('You drink coffee every morning.', 603)
        self.assertEqual(said('You no longer drink coffee every morning.', 604)['replaced'], drink['id'])
        # another fact that only shares words, or one about someone else, stays
        self.assertNotIn('replaced', said('Your office has a quiet room for calls.', 605))
        self.assertNotIn('replaced', said('Ann Example lives in Ghent.', 606, about=[ANN]))
        self.assertNotIn('replaced', said('You only book aisle seats on trains.', 607))  # another word in a scope: another matter
        # Undo merge under Learning brings the old one back
        self.store.unmerge_fact(new['id'])
        facts = recall(self.app, 'preparation', {'todo': self.todo}).text('facts')
        self.assertIn('Ghent.', facts)
        self.assertNotIn('Brussels', facts)

    def chat_turn(self, n, text):
        """The owner writes in the to-do's chat; its turn runs in the preparation's session. Returns its message."""
        with self.store.connect() as db:
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=? WHERE finished_at IS NULL", (NOW.isoformat(),))
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared' WHERE id=?", (self.todo,))
        self.store.decide(self.todo, 'other', text, f'chat-{n:036d}', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        return next(c['message'] for c in calls if c.get('message'))

    def test_a_to_do_chat_gets_what_was_learned_after_its_session_read_the_list(self):
        self.store.decide(self.todo, 'accept', '', 'click', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        first = next(c['message'] for c in calls if c.get('message'))
        self.assertIn(NOTE, first)
        clock = [NOW + dt.timedelta(hours=1)]
        later = patch_everywhere(a, 'now', lambda: clock[0].isoformat())
        later.start()
        self.addCleanup(later.stop)
        # learned after the preparation started: in the owner's chat, an edit of one it had, and one the owner removed
        fresh = self.app.action('remember_fact', {'text': 'Contracts with Client Co are signed through the e-sign portal.', '_owner_chat': True})['id']
        with self.store.connect() as db:
            said, note = (db.execute('SELECT id FROM facts WHERE text=?', (t,)).fetchone()[0] for t in (SAID, NOTE))
        self.store.edit_fact(note, 'Quotes always go out as a PDF attachment, never as a link.')
        self.store.forget_fact(said)
        chat = self.chat_turn(1, 'How do we sign it?')
        block = chat[chat.index(retained_facts.NEW_HEAD):].split('\n\n')[0]
        self.assertIn('e-sign portal', block)
        self.assertIn('PDF attachment', block)
        self.assertIn(retained_facts.GONE, block)  # forgotten: the session is told to stop using it
        self.assertLessEqual(len(block), retained_facts.NEW_CHARS)
        self.assertLessEqual(block.count('\n- '), retained_facts.NEW_LINES)
        self.assertNotIn(FIXED, block)  # the session already has it
        with self.store.connect() as db:
            logged = {(r[0], r[1]) for r in db.execute("SELECT kind,row_id FROM memory_use WHERE purpose='todo_chat' AND suggestion_id=?", (self.todo,))}
        self.assertTrue({('fact', str(fresh)), ('fact', str(note)), ('fact', str(said))} <= logged)
        # the next turn doesn't send it again; a fact that ended since it was sent comes back as history
        self.assertNotIn(retained_facts.NEW_HEAD, self.chat_turn(2, 'And who signs?'))
        clock[0] = NOW + dt.timedelta(hours=2)
        self.store.commit_page('work', {}, [mail(9, 'Ann Example <ann@client.example>', 'sam@acme.example', 'Portal', 'We stopped using the e-sign portal.')])
        with self.store.connect() as db:
            event = db.execute("SELECT id FROM events WHERE source_id='m9'").fetchone()[0]
        self.store.fact_overturned(fresh, 'Client Co stopped using the e-sign portal', [event])
        block = self.chat_turn(3, 'Still the portal?')
        self.assertIn(retained_facts.HISTORY + ' (ended', block)
        self.assertNotIn(f'{retained_facts.GONE}', block.split(retained_facts.NEW_HEAD, 1)[1].split('\n\n')[0])

    def test_a_to_do_chat_skips_new_facts_that_dont_bear_on_it_once_the_list_is_long(self):
        self.store.decide(self.todo, 'accept', '', 'click', 'dashboard')
        self.app.preparation_step(lambda r: {'status': 'admitted'})
        later = patch_everywhere(a, 'now', lambda: (NOW + dt.timedelta(hours=1)).isoformat())
        later.start()
        self.addCleanup(later.stop)
        self.app.action('remember_fact', {'text': 'Contracts with Client Co are signed through the e-sign portal.', '_owner_chat': True})
        self.app.action('remember_fact', {'text': 'The garden hedge is trimmed every spring.', '_owner_chat': True})
        with patch.object(retained_facts, 'FACTS_ALL_UNDER', 0):
            chat = self.chat_turn(1, 'How do we sign the contract?')
        self.assertIn('e-sign portal', chat)  # its words match the to-do
        self.assertNotIn('garden hedge', chat)

    def test_a_correction_that_swaps_a_plain_word_takes_the_place_of_the_fact_it_corrects(self):
        said = lambda text, n, **args: (self.app.action('feedback_reply', {'text': text, 'message_id': str(n), 'timestamp': NOW.timestamp(), 'reply_to_id': ''}),
                                        self.app.action('remember_fact', {'text': text, '_owner_chat': True, **args}))[1]
        with self.store.connect() as db:
            aisle = db.execute('SELECT id FROM facts WHERE text=?', (SAID,)).fetchone()[0]
        window = said('You only book window seats on flights.', 701)
        self.assertEqual(window['replaced'], aisle)
        memory = recall(self.app, 'preparation', {'todo': self.todo})
        facts = memory.text('facts')
        self.assertIn('window seats', facts)
        self.assertNotIn('aisle seats', facts)  # never both in one draft
        self.app.memory_search = lambda request: {'error': 'off'}
        found = [f['text'] for f in self.app.talk_recall('seats on flights')['found']]
        self.assertEqual(len(found), 1)  # Talk recalls the new one only
        self.assertIn('window seats', found[0])
        with self.store.connect() as db:  # the old one stays as history behind the new one, with Undo merge
            self.assertEqual(db.execute('SELECT merged_into FROM facts WHERE id=?', (aisle,)).fetchone()[0], f"fact:{window['id']}")
        trip = self.store.suggest('trip', 'Book the flights and seats for the trip', 'Flights for the offsite.', [1])['id']
        history = recall(self.app, 'preparation', {'todo': trip}).text('retained')
        self.assertIn('Historical, not current', history)  # a to-do it bears on sees it as history, with what it says now
        self.assertIn('aisle seats', history)
        # the same frame about another matter, or about someone else, stays apart
        drink = said('You drink green tea every morning.', 702)
        self.assertEqual(said('You drink black tea every morning.', 703)['replaced'], drink['id'])
        # the same frame about another matter, or about someone else, stays apart
        for n, text, args in ((704, 'You buy apples and pears at the weekly market.', {}),
                              (705, 'You buy apples and plums at the weekly market.', {}),  # one more item of a list
                              (706, 'Lunch with the team is at noon on Fridays.', {}),
                              (707, 'Dinner with the team is at noon on Fridays.', {}),   # the subject: another matter
                              (708, 'Ann Example drinks green tea every morning.', {'about': [ANN]}),  # someone else
                              (709, 'You like coffee.', {}), (710, 'You like tea.', {})):  # too short a frame to tell
            self.assertNotIn('replaced', said(text, n, **args), text)
        with self.store.connect() as db:
            ann = db.execute("SELECT id FROM facts WHERE text='Ann Example drinks green tea every morning.'").fetchone()[0]
        self.assertEqual(said('Ann Example drinks black tea every morning.', 711, about=[ANN])['replaced'], ann)  # same records: hers
        # Undo merge under Learning brings the old one back, and the correction goes
        self.store.unmerge_fact(window['id'])
        facts = recall(self.app, 'preparation', {'todo': self.todo}).text('facts')
        self.assertIn(SAID, facts)
        self.assertNotIn('window seats', facts)

    def test_ask_reads_facts_on_the_record_and_by_meaning(self):
        about = {'area': None, 'subjects': [{'id': ANN, 'name': 'Ann Example'}], 'accounts': ['work'], 'question': 'What does Ann eat?'}
        self.assertIn(NOTE_ANN, ask_memory.facts(self.app, about, 1000))  # the notes fact, on her page
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=embed):
            found = ask_memory.facts(self.app, {**about, 'subjects': [], 'question': 'Which seat do I like?'}, 1000)
        self.assertIn(SAID, found)  # the chat fact, by meaning

    def test_ask_without_embeddings_matches_short_words(self):
        ask = lambda question: ask_memory.facts(self.app, {'area': None, 'subjects': [], 'accounts': ['work'], 'question': question}, 1000)
        for text in ('You go to the gym on Tuesday mornings.', 'Your car is parked at the station.', 'You go to Ghent on Fridays.'):
            self.store.remember_fact(text, 'note-1')
        found = ask('When do I go to the gym?')
        self.assertIn('the gym', found)  # "gym" is what the question is about, short as it is
        self.assertNotIn('Ghent', found)  # sharing only "go" is no match
        self.assertIn('Your car', ask('Where is my car?'))
        self.assertEqual(ask('What do I do?'), '')  # question words alone find nothing
        self.assertEqual(ask('Where did I go?'), '')

    def test_ask_finds_facts_about_no_one_with_and_without_embeddings(self):
        ask = lambda question: ask_memory.facts(self.app, {'area': None, 'subjects': [], 'accounts': ['work'], 'question': question}, 1000)
        seats = 'Which seats do I book on flights?'
        gone = self.store.remember_fact('You only take aisle seats on trains.', 'note-1')['id']
        self.store.forget_fact(gone)  # forgotten: never comes back
        ended = self.store.remember_fact('You book aisle seats on flights for the fair this week.', 'note-1')['id']
        old = self.store.remember_fact('You book seats on flights through the travel desk.', 'note-1')['id']
        new = 'You book seats on flights yourself now.'
        self.store.remember_fact(new, 'note-1', replaces=[old])  # replaced: history, not how things are now
        with self.store.connect() as db:
            db.execute('UPDATE facts SET valid_until=? WHERE id=?', ('2026-11-01', ended))
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES('You book seats on flights in first class.','ai:c1',?,'fact','ai:Claude','work')",
                       (NOW.isoformat(),))  # a connected AI's, not the owner's word
        self.store.retire_expired()
        outside = ('aisle seats on trains', 'for the fair', 'travel desk', 'first class')
        # no embeddings on this Machine: the owner's own facts that share the question's words
        found = ask(seats)
        self.assertIn(SAID, found)  # what the owner said about themselves, about no one
        self.assertIn(new, found)
        for text in outside:
            self.assertNotIn(text, found)
        self.assertIn(NOTE, ask('What format do quotes go out in?'))  # a general fact from the notes
        self.assertEqual(ask('What do I do?'), '')  # no distinctive word: nothing
        self.assertEqual(ask('quarterly board budget'), '')
        memory = memory_use.Recalled('ask', {'question': seats}).add('facts', ask)
        memory.read('facts', seats)
        self.assertEqual({i.how for i in memory.picked()['fact']}, {'match'})  # logged as picked by words
        # embeddings on: by meaning, the same left out
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=embed):
            found = ask(seats)
        self.assertIn(SAID, found)
        for text in outside[:3]:
            self.assertNotIn(text, found)
        # embeddings on but the server down: the words again
        with patch.object(a.embeddings, 'embed', side_effect=a.embeddings.EmbeddingError('down')):
            found = ask(seats)
        self.assertIn(SAID, found)
        self.assertNotIn('first class', found)

    def test_talk_recalls_what_was_learned_with_memory_search_off(self):
        self.app.memory_search = lambda request: {'error': 'off'}
        for words, text in (('aisle seat', SAID), ('invoices', FIXED), ('quotes as PDF', NOTE), ('Ann vegetarian', NOTE_ANN)):
            found = self.app.talk_recall(words)['found']
            self.assertIn(text, found[0]['text'], words)
            self.assertEqual(found[0]['from'], 'what The Machine learned')
        self.assertEqual(self.app.talk_recall('quarterly board budget')['found'], [])  # nothing shares the words: nothing
        with self.store.connect() as db:
            self.assertEqual({r[0] for r in db.execute("SELECT kind FROM memory_use WHERE purpose='talk'")}, {'fact'})
        self.assertEqual(ask_memory.learned(self.store, 'the'), [])  # filler words alone find nothing
        with self.store.connect() as db:  # a connected AI's fact is not the owner's word: never recalled as theirs
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES('Ann Example wants aisle seats too.','ai:c1',?,'fact','ai:Claude','work')",
                       (NOW.isoformat(),))
        self.assertEqual([f['text'] for f in ask_memory.learned(self.store, 'aisle seats')], [SAID])
        # memory search on: what was learned first, then the excerpts it found
        self.app.memory_search = lambda request: {'results': [{'source': 'memory', 'text': 'Seat notes from last spring.'}]}
        found = self.app.talk_recall('aisle seat')['found']
        self.assertEqual([f['from'] for f in found], ['what The Machine learned', 'the notes'])

    def test_talk_recalls_beyond_the_exact_words_with_and_without_embeddings(self):
        self.app.memory_search = lambda request: {'error': 'off'}
        texts = lambda words: [f['text'] for f in ask_memory.learned(self.store, words, a.embeddings.settings(self.app.config))]
        gone = self.store.remember_fact('You fly economy on short trips.', 'note-1')['id']
        ended = self.store.remember_fact('You fly to the fair on Friday.', 'note-1')['id']
        old = self.store.remember_fact('You fly through the travel desk.', 'note-1')['id']
        with self.store.connect() as db:
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES('You fly first class on long trips.','ai:c1',?,'fact','ai:Claude','work')",
                       (NOW.isoformat(),))  # a connected AI's, not the owner's word
        with patch.object(a.embeddings, 'embed', side_effect=fly):  # what a preparation stores: every fact's vector
            self.store.facts_ranked('none', self.store.facts(), SETTINGS)
        self.store.forget_fact(gone)
        new = 'You fly with your own booking tool now.'
        self.store.remember_fact(new, 'note-1', replaces=[old])
        with self.store.connect() as db:
            db.execute('UPDATE facts SET valid_until=? WHERE id=?', ('2026-11-01', ended))
        self.store.retire_expired()
        outside = ('economy', 'the fair', 'travel desk', 'first class')
        # no embeddings: the words in their plain form
        with patch.object(a.embeddings, 'embed', side_effect=AssertionError('no embedding request without embeddings')):
            self.assertEqual(texts('seat'), [SAID])  # "seat" finds "seats"
            self.assertEqual(texts('booking an aisle seat'), [SAID])  # "booking" finds "book"
            self.assertEqual(texts('quoting in PDF'), [NOTE])
            self.assertEqual(texts('invoice'), [FIXED])
            self.assertEqual(texts('flying'), [new])  # "flying" finds "fly", and only the current one of them
            self.assertNotIn(SAID, texts('flying'))  # "flights" is another stem: by meaning only
        # embeddings on: the stored vectors bring what means the same, never more than LEARNED
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=fly) as embed_call:
            found = self.app.talk_recall('flying')['found']
            self.assertEqual(embed_call.call_count, 1)  # the words only: the facts' vectors were stored
            said = [f['text'] for f in found]
            self.assertTrue(any(SAID in t for t in said), said)  # "flying" finds "flights"
            self.assertTrue(any(new in t for t in said), said)
            for text in outside:
                self.assertFalse(any(text in t for t in said), (text, said))
            self.assertEqual(texts('seat')[0], SAID)  # words first
            self.assertLessEqual(len(texts('flying flights travel trips')), ask_memory.LEARNED)
        with self.store.connect() as db:
            self.assertIn('closeness', {r[0] for r in db.execute("SELECT how FROM memory_use WHERE purpose='talk'")})
        # the embedding server down: words only, no error
        with patch.object(a.embeddings, 'embed', side_effect=a.embeddings.EmbeddingError('down')):
            self.assertEqual(texts('flying'), [new])
            self.assertEqual(texts('seats'), [SAID])

    def test_the_owners_chat_finds_facts_on_a_persons_page(self):
        known = [k['text'] for k in self.app.graph_action({'node_id': ANN})['open'].get('known', [])]
        self.assertIn(NOTE_ANN, known)  # OpenClaw's chat asks graph for a person: what was learned about them comes along

    def chat(self, question):
        """A later question in the owner's main chat, as the bridge's assistant_memory tool asks it."""
        return self.app.action('recall_learned', {'words': question, '_owner_chat': True})

    def test_the_owners_chat_reads_back_what_it_was_told(self):
        # said in the chat (setUp), asked later in the chat: the answer has it, and the draft rule from the notes
        found = self.chat('Which seats do I book on flights?')['found']
        self.assertIn(SAID, found)
        self.assertLessEqual(len(found), ask_memory.CHAT_CHARS)
        self.assertIn('- Draft rule: ' + NOTE_RULE, self.chat('how do I sign an email')['found'])
        with self.store.connect() as db:  # logged as the main chat's read, ids only
            self.assertEqual({tuple(r) for r in db.execute("SELECT kind,how FROM memory_use WHERE purpose='chat'")}, {('fact', 'match'), ('rule', 'match')})
        self.assertEqual(self.chat('quarterly board budget'), {'found': '', 'note': 'Nothing The Machine learned matches those words.'})
        # only the owner's own chat: no mark from the bridge, no answer
        with self.assertRaisesRegex(ValueError, 'own main chat'):
            self.app.action('recall_learned', {'words': 'aisle seats'})

    def test_the_owners_chat_never_reads_a_forgotten_fact(self):
        said = lambda text, n: (self.app.action('feedback_reply', {'text': text, 'message_id': str(n), 'timestamp': NOW.timestamp(), 'reply_to_id': ''}),
                                self.app.action('remember_fact', {'text': text, '_owner_chat': True}))[1]
        gym = said('You go to the gym on Thursdays.', 701)
        self.assertIn('gym on Thursdays', self.chat('when do I go to the gym')['found'])
        self.app.action('forget_fact', {'id': gym['id']}, owner_dashboard=True)
        self.assertEqual(self.chat('when do I go to the gym')['found'], '')  # not as current, not as history
        # a correction: the old one comes back only marked as history; once the owner removes the new one, neither
        old = said('Your office is in Ghent.', 702)
        new = said('Your office is in Brussels now.', 703)
        self.assertEqual(new['replaced'], old['id'])
        found = self.chat('where is my office')['found'].splitlines()
        self.assertIn('- Your office is in Brussels now.', found)
        ghent = [line for line in found if 'Ghent' in line]
        self.assertEqual(len(ghent), 1)
        self.assertTrue(ghent[0].startswith('- Historical, not current (ended '), ghent[0])
        self.app.action('forget_fact', {'id': new['id']}, owner_dashboard=True)
        self.assertEqual(self.chat('where is my office')['found'], '')

    def test_the_owners_chat_reads_a_persons_facts_only_when_asked_about_them(self):
        self.assertNotIn(NOTE_ANN, self.chat('who is vegetarian')['found'])
        self.assertIn(NOTE_ANN, self.chat('is Ann vegetarian')['found'])
        with self.store.connect() as db:  # a connected AI's fact is not the owner's word
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES('You prefer window seats on flights.','ai:c1',?,'fact','ai:Claude','work')",
                       (NOW.isoformat(),))
        self.assertNotIn('window', self.chat('seats on flights')['found'])

    def flights_learned(self):
        """What was learned about flying, every fact's vector stored as a preparation stores it (plane): one current,
        one the owner forgot, one ended, and a connected AI's. The current one's text."""
        klm = 'You only fly KLM.'
        self.store.remember_fact(klm, 'note-1')
        gone = self.store.remember_fact('You fly from the small airport.', 'note-1')['id']
        ended = self.store.remember_fact('You fly Lufthansa to the fair.', 'note-1')['id']
        with self.store.connect() as db:  # a connected AI's, not the owner's word
            db.execute("INSERT INTO facts(text,decision_id,created_at,kind,source,side) VALUES('You fly first class on long trips.','ai:c1',?,'fact','ai:Claude','work')",
                       (NOW.isoformat(),))
        with patch.object(a.embeddings, 'embed', side_effect=plane):
            self.store.facts_ranked('none', self.store.facts(), SETTINGS)
        self.app.action('forget_fact', {'id': gone}, owner_dashboard=True)
        with self.store.connect() as db:
            db.execute('UPDATE facts SET valid_until=? WHERE id=?', ('2026-11-01', ended))
        self.store.retire_expired()
        return klm

    def test_the_owners_chat_finds_what_was_learned_by_meaning(self):
        klm = self.flights_learned()
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=plane) as embed_call:
            for question in ('flying', 'which airline for my flights', 'plane trip next week'):
                embed_call.reset_mock()
                found = self.chat(question)['found']
                self.assertEqual(embed_call.call_count, 1, question)  # the question only, never one call per fact
                self.assertIn(klm, found, question)
                self.assertNotIn('first class', found)  # a connected AI's
                self.assertLessEqual(len(found), ask_memory.CHAT_CHARS)
            lufthansa = [line for line in found.splitlines() if 'Lufthansa' in line]  # ended: only as history
            self.assertEqual(len(lufthansa), 1)
            self.assertTrue(lufthansa[0].startswith('- Historical, not current (ended '), lufthansa[0])
            self.assertEqual(self.chat('quarterly board budget')['found'], '')  # far in meaning: nothing
        with self.store.connect() as db:
            self.assertIn('closeness', {r[0] for r in db.execute("SELECT how FROM memory_use WHERE purpose='chat'")})

    def test_the_owners_chat_never_finds_a_forgotten_fact_by_meaning(self):
        klm = self.flights_learned()
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=plane):
            for question in ('flying', 'which airline for my flights', 'plane trip next week', 'small airport'):
                self.assertNotIn('small airport', self.chat(question)['found'], question)  # its vector is still stored
            self.assertIn(klm, self.chat('plane trip next week')['found'])
            self.app.action('forget_fact', {'id': next(f['id'] for f in self.store.facts() if f['text'] == klm)}, owner_dashboard=True)
            self.assertNotIn(klm, self.chat('plane trip next week')['found'])
            self.assertNotIn(klm, self.chat('flying')['found'])

    def test_the_owners_chat_without_embeddings_finds_by_words(self):
        klm = self.flights_learned()
        # none configured: words in their plain form, no embedding request; "flights" and "plane" are other stems
        with patch.object(a.embeddings, 'embed', side_effect=AssertionError('no embedding request without embeddings')):
            self.assertIn(klm, self.chat('which airline when flying')['found'])
            self.assertNotIn(klm, self.chat('which airline for my flights')['found'])
            self.assertEqual(self.chat('plane trip next week')['found'], '')
        # the embedding server down: the same words, no error
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=a.embeddings.EmbeddingError('down')):
            self.assertIn(klm, self.chat('flying')['found'])
            self.assertEqual(self.chat('plane trip next week')['found'], '')

    def test_the_owners_chat_answer_by_meaning_fits_its_budget(self):
        self.flights_learned()
        for n in range(40):
            self.store.remember_fact(f'You fly route {n} on the early plane when the meeting is before ten in the morning.', 'note-1')
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=plane):
            self.store.facts_ranked('none', self.store.facts(), SETTINGS)
            found = self.chat('plane trip next week')['found']
        self.assertGreater(len(found.splitlines()), 3)
        self.assertLessEqual(len(found), ask_memory.CHAT_CHARS)

    def test_a_routine_run_reads_what_came_in_every_way(self):
        sent = []
        for name, value in (('routines_now', lambda s: NOW.astimezone(s.routines_tz())),
                            ('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: sent.append(request) or {'status': 'admitted'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        made = self.app.action('routine_new', {'words': 'every weekday at 8, draft a short update for the team'}, owner_dashboard=True)['made']
        self.app.action('routine_run_now', {'id': made}, owner_dashboard=True)
        self.app.routines_step()
        message = next(s['message'] for s in sent if s['action'] == 'start')
        for text in self.learned() + (NOTE_RULE,):
            self.assertIn(text, message)
        with self.store.connect() as db:  # logged once the turn was admitted
            self.assertEqual({r[0] for r in db.execute("SELECT kind FROM memory_use WHERE purpose='routine'")}, {'fact', 'rule'})

    def routine_message(self, words, made=None):
        """A routine with these words (new, or made again), run now: (its id, the run's id, its turn's message). An
        earlier run is over by then."""
        with self.store.connect() as db:
            db.execute("UPDATE routine_runs SET state='nothing',finished_at=? WHERE state='running'", (NOW.isoformat(),))
            if made:  # its next run: another period
                db.execute("UPDATE routine_runs SET period=period||'-'||id WHERE routine_id=?", (made,))
        sent = []
        for name, value in (('routines_now', lambda s: NOW.astimezone(s.routines_tz())),
                            ('background_pause', lambda s, **k: None), ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: sent.append(request) or {'status': 'admitted'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        made = made or self.app.action('routine_new', {'words': words}, owner_dashboard=True)['made']
        self.app.action('routine_run_now', {'id': made}, owner_dashboard=True)
        self.app.routines_step()
        start = next(s for s in sent if s['action'] == 'start')
        return made, start['job_id'], start['message']

    def routine_hands_in(self, run, draft):
        return self.app.action('routine_result', {'_routine_session': 'agent:main:assistant-review-routine-' + run, 'text': 'Made a draft.', 'draft': draft},
                               owner_dashboard=False)

    def test_a_routine_that_leaves_a_draft_writes_in_the_owners_voice_for_its_channel(self):
        for channel, text in (('All', 'Short sentences, no exclamation marks.'), ('Email', 'Opens with Hi and the first name.\nSigns off with Cheers.'),
                              ('Slack', 'all lowercase, no greeting.'), ('LinkedIn', 'One emoji at most.')):
            self.store.save_voice(channel, text, 'owner')
        # No run of it left a draft yet: its message has no voice, whatever its words (any language)
        made, run, message = self.routine_message('elke werkdag om 8: een korte update voor het team')
        self.assertNotIn(voices.VOICE_HEAD, message)
        self.assertNotIn('Short sentences', message)
        # It hands one in: the voice of the account it goes out from, and All; nothing saved until it follows it
        draft = {'title': 'Update for the team', 'text': 'Hallo allemaal!', 'account': 'work'}
        answer = self.routine_hands_in(run, draft)
        self.assertFalse(answer['saved'])
        self.assertIn('Signs off with Cheers.', answer['voice'])
        self.assertIn('no exclamation marks', answer['voice'])
        self.assertNotIn('all lowercase', answer['voice'])
        self.assertLessEqual(len(answer['voice']), recall_module.ROUTINE_VOICE)
        with self.store.connect() as db:
            self.assertEqual({('All', 'always'), ('Email', 'match')},
                             {tuple(r) for r in db.execute("SELECT row_id,how FROM memory_use WHERE purpose='routine' AND kind='voice' AND run_id=?", (run,))})
            self.assertFalse(db.execute("SELECT 1 FROM events WHERE kind='routine.draft'").fetchone())
        self.assertTrue(self.routine_hands_in(run, dict(draft, text='Hi all, a short update. Cheers'))['saved'])  # once per run
        # Its next run had a draft before it: the voice is in its message, the account's channel
        _, run, message = self.routine_message('', made)
        self.assertIn(voices.VOICE_HEAD, message)
        block = message[message.index(voices.VOICE_HEAD):]
        self.assertIn('Signs off with Cheers.', block)
        self.assertNotIn('all lowercase', block)
        self.assertTrue(self.routine_hands_in(run, draft)['saved'])  # it had the voice: no second ask
        # A service its draft names (a proper noun) goes first
        _, run, _ = self.routine_message('elke werkdag om 9: de winst van de dag')
        answer = self.routine_hands_in(run, {'title': 'Post in Slack: de winst van de week', 'text': 'goed bezig'})
        self.assertIn('all lowercase', answer['voice'])
        # A run that hands in no draft gets no voice
        _, run, message = self.routine_message('elke werkdag om 10: tel de open tickets')
        self.assertNotIn(voices.VOICE_HEAD, message)
        self.assertTrue(self.routine_hands_in(run, None)['saved'])
        with self.store.connect() as db:
            self.assertFalse(db.execute("SELECT 1 FROM memory_use WHERE kind='voice' AND run_id=?", (run,)).fetchone())

    def test_a_routines_voice_stays_in_its_budget(self):
        for channel in ('All', 'Email'):
            self.store.save_voice(channel, '\n'.join([f'{channel} line {n} ' + 'x' * 70 for n in range(4)]), 'owner')
        text = recall(self.app, 'routine', {'run': 'r'}).text('voice', ['Email'])
        self.assertLessEqual(len(text), recall_module.ROUTINE_VOICE)
        self.assertIn('All line 0', text)
        self.assertNotIn('Email line', text)  # a whole block or none: Email's doesn't fit next to All's
        self.store.save_voice('All', '', 'owner')
        self.assertEqual('', recall(self.app, 'routine', {'run': 'r'}).text('voice', ['Telegram']))  # no voice there: nothing

    def test_the_morning_digest_has_the_promise_a_review_read_in_the_mail(self):
        digest = self.app.digest(NOW)
        self.assertIn(PROMISED, digest['text'].casefold())


if __name__ == '__main__':
    unittest.main()

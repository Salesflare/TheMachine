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
from machine.app.recall import recall  # noqa: E402

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
        self.assertNotIn('replaced', said('You only book window seats on flights.', 607))  # a plain word swapped: left to the condense pass
        # Undo merge under Learning brings the old one back
        self.store.unmerge_fact(new['id'])
        facts = recall(self.app, 'preparation', {'todo': self.todo}).text('facts')
        self.assertIn('Ghent.', facts)
        self.assertNotIn('Brussels', facts)

    def test_ask_reads_facts_on_the_record_and_by_meaning(self):
        about = {'area': None, 'subjects': [{'id': ANN, 'name': 'Ann Example'}], 'accounts': ['work'], 'question': 'What does Ann eat?'}
        self.assertIn(NOTE_ANN, ask_memory.facts(self.app, about, 1000))  # the notes fact, on her page
        self.app.config = {**self.config, 'embeddings': SETTINGS}
        with patch.object(a.embeddings, 'embed', side_effect=embed):
            found = ask_memory.facts(self.app, {**about, 'subjects': [], 'question': 'Which seat do I like?'}, 1000)
        self.assertIn(SAID, found)  # the chat fact, by meaning

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

    def test_the_morning_digest_has_the_promise_a_review_read_in_the_mail(self):
        digest = self.app.digest(NOW)
        self.assertIn(PROMISED, digest['text'].casefold())


if __name__ == '__main__':
    unittest.main()

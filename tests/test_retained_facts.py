"""Facts outside the current list (set aside, ended, replaced) come back into a review, a preparation and a to-do's
chat when they bear on it (machine/app/retained_facts.py): a set-aside one as the fact it still is, the others
marked as history with their day and what replaced them, a forgotten one never. Made-up data, with and without
embeddings."""
import datetime as dt
import importlib.util
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('retained_facts_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.app import retained_facts  # noqa: E402
from machine.app.recall import recall  # noqa: E402

START = dt.datetime(2026, 9, 1, 12, tzinfo=dt.timezone.utc)
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}
NEAR, FAR = [1.0, 0.0], [0.0, 1.0]
ACCOUNTS = [{'id': 'work', 'email': 'sam@acme.example'}]

ASIDE = 'The Lisbon offsite always books the riverside venue with catering.'
ASIDE_OTHER = 'Quarterly taxes are filed by the bookkeeper in March.'
ASIDE_MEANING = 'Prefers morning flights for any work travel.'
ASIDE_NAMED = 'Robin Vale answers fastest on a Tuesday morning.'
ENDED = 'The offsite venue contact is Dana at Riverside Hall.'
ENDED_REASON = 'Riverside Hall closed, the offsite venue is booked through Harbor Lofts'
PAST = 'The offsite catering menu is on hold until the headcount is final.'
OLD = 'Offsite budget per team is capped in euros.'
NEW = 'Offsite spending needs approval from finance first.'
REWORDED_OLD = 'Venue invoices go to accounting.'
REWORDED_NEW = 'Venue invoices go to accounting with the booking number.'
FORGOTTEN = 'The Lisbon offsite venue needs a deposit by Friday.'
CHAIN_OLD = 'The offsite venue shortlist lives in the planning sheet.'
CHAIN_NEW = 'Offsite venue options are tracked by the events team now.'


def mail(n, at, sender, title, body):
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': 'gmail.message', 'occurred_at': at.isoformat(), 'title': title, 'body': body,
            'deleted': False, 'metadata': {'from': sender, 'to': 'sam@acme.example', 'cc': '', 'labels': ['INBOX'], 'message-id': f'<m{n}@x>',
                                            'thread_id': f't{n}'}}


class RetainedFactsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': ACCOUNTS, 'database': str(Path(temp.name) / 'events.sqlite'),
                           'openclaw_config': str(Path(temp.name) / 'openclaw.json')}
        self.clock = [START]
        for started in (patch_everywhere(a, 'now', lambda: self.clock[0].isoformat()),
                        patch.object(a.embeddings, 'embed', side_effect=AssertionError('no embedding request'))):
            started.start()
            self.addCleanup(started.stop)
        self.store.commit_page('work', {}, [mail(1, START, 'Lee Park <lee@globex.example>', 'Invoice', 'The September invoice is open.')])
        note = self.store.suggest('note', 'Plan the team offsite', 'Body', [1])['id']
        self.store.decide(note, 'reject', 'notes on the offsite', 'owner-note', 'dashboard')
        self.ids = {}
        for text in (ASIDE, ASIDE_OTHER, ASIDE_MEANING, ASIDE_NAMED):  # learned long ago and not used since
            self.ids[text] = self.learn(text)
        for i in range(72):  # a full list of facts used lately, so the old ones are set aside to make room
            self.clock[0] = START + dt.timedelta(days=30, minutes=i)
            self.learn(f'Filler fact number {i} about how the owner keeps their week.')
        self.clock[0] = START + dt.timedelta(days=31)
        for text in (ENDED, OLD, REWORDED_OLD, FORGOTTEN, CHAIN_OLD):
            self.ids[text] = self.learn(text)
        self.ids[PAST] = self.store.remember_fact(PAST, 'owner-note', 'event', until=(START + dt.timedelta(days=33)).date().isoformat())['id']
        self.ids[NEW] = self.store.remember_fact(NEW, 'owner-note', replaces=[self.ids[OLD]])['id']
        self.ids[REWORDED_NEW] = self.store.remember_fact(REWORDED_NEW, 'owner-note', replaces=[self.ids[REWORDED_OLD]])['id']
        self.ids[CHAIN_NEW] = self.store.remember_fact(CHAIN_NEW, 'owner-note', replaces=[self.ids[CHAIN_OLD]])['id']
        self.store.forget_fact(self.ids[FORGOTTEN])
        self.store.forget_fact(self.ids[CHAIN_NEW])  # the owner removed the newer one: its history goes with it
        self.clock[0] = START + dt.timedelta(days=32)  # a newer message overturns one
        self.store.commit_page('work', {}, [mail(2, self.clock[0], 'Robin Vale <robin@harbor.example>', 'Lisbon offsite venue options',
                                                 'Riverside Hall closed, we can host the offsite at Harbor Lofts.')])
        self.store.fact_overturned(self.ids[ENDED], ENDED_REASON, [2])
        self.clock[0] = START + dt.timedelta(days=40)
        self.store.retire_expired()  # past its end day, and the ones not used in 21 days set aside
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, self.app.config, self.clock[0].isoformat())
            self.state = {r['id']: r['merged_into'] for r in db.execute('SELECT id,merged_into FROM facts WHERE removed_at IS NOT NULL')}
        self.todo = self.store.suggest('offsite', 'Book the Lisbon offsite venue', 'Robin offers Harbor Lofts for the offsite; the catering menu and the team budget are still open.', [2])['id']

    def learn(self, text):
        return self.store.remember_fact(text, 'owner-note')['id']

    def vectors(self, facts, events):
        key = f"{SETTINGS['model']}:{SETTINGS['dims']}"
        with self.store.connect() as db:
            db.executemany('INSERT OR REPLACE INTO fact_vectors(fact_id,model,vector) VALUES(?,?,?)',
                           [(self.ids[t], key, a.embeddings.pack(v)) for t, v in facts.items()])
            db.executemany('INSERT OR REPLACE INTO event_vectors(event_id,version,model,dims,vector) VALUES(?,1,?,?,?)',
                           [(e, SETTINGS['model'], SETTINGS['dims'], a.embeddings.pack(v)) for e, v in events.items()])

    def retained(self, purpose='preparation'):
        memory = recall(self.app, purpose, {'todo': self.todo} if purpose != 'review' else {'run': 'r'}, 60000)
        return memory.text('retained'), memory.rows()

    def test_the_data_is_what_the_store_keeps(self):
        for text in (ASIDE, ASIDE_OTHER, ASIDE_MEANING, ASIDE_NAMED):
            self.assertEqual(self.state[self.ids[text]], f'aside:{self.ids[text]}')
        for text in (ENDED, PAST):
            self.assertEqual(self.state[self.ids[text]], f'expired:{self.ids[text]}')
        self.assertEqual(self.state[self.ids[OLD]], f'fact:{self.ids[NEW]}')
        self.assertIsNone(self.state[self.ids[FORGOTTEN]])

    def test_a_preparation_gets_what_bears_on_its_to_do_without_embeddings(self):
        text, rows = self.retained()
        lines = text.splitlines()
        self.assertEqual(retained_facts.TODO_HEAD, lines[0])
        self.assertEqual(['- ' + ASIDE_NAMED, '- ' + ASIDE], lines[1:3])  # set aside: still holds, as the fact it is, first
        self.assertTrue(lines[3].startswith('- Historical, not current (ended '))  # then history, in the room left
        self.assertEqual(len(lines) - 1, retained_facts.LINES)
        self.assertLessEqual(len(text), retained_facts.CHARS)
        self.assertEqual({'fact'}, {r[0] for r in rows})
        self.assertEqual({0}, {r[5] for r in rows})  # never a use: a set-aside fact stays set aside
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            lines = self.retained()[0].splitlines()
        self.assertIn(f'- Historical, not current (ended {(START + dt.timedelta(days=32)).date()}; now: {ENDED_REASON}): {ENDED}', lines)
        self.assertIn(f'- Historical, not current (ended {(START + dt.timedelta(days=31)).date()}; now: {NEW}): {OLD}', lines)
        self.assertIn(f'- Historical, not current (ended {(START + dt.timedelta(days=33)).date()}): {PAST}', lines)  # past its end day
        self.assertNotIn('- ' + ASIDE_OTHER, lines)  # nothing to do with it
        self.assertNotIn('- ' + ASIDE_MEANING, lines)  # close only in meaning, and meaning search is off

    def test_never_a_forgotten_one_or_one_that_says_nothing_new(self):
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            text, _ = self.retained()
            review, _ = self.retained('review')
        for gone in (FORGOTTEN, CHAIN_OLD, CHAIN_NEW, REWORDED_OLD):
            self.assertNotIn(gone, text + review)
        self.assertIn(ENDED, text)

    def test_a_name_on_the_to_do_brings_a_set_aside_fact_about_them(self):
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            text, rows = self.retained()
        self.assertIn('- ' + ASIDE_NAMED, text)  # Robin Vale wrote the to-do's message
        self.assertIn((str(self.ids[ASIDE_NAMED]), 'about'), [(r[1], r[2]) for r in rows])

    def test_with_embeddings_a_fact_close_in_meaning_comes_in_from_stored_vectors(self):
        self.app.config['embeddings'] = SETTINGS
        self.vectors({ASIDE_MEANING: NEAR, ASIDE_OTHER: FAR}, {2: NEAR})
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            text, rows = self.retained()
        self.assertIn('- ' + ASIDE_MEANING, text)
        self.assertNotIn(ASIDE_OTHER, text)
        self.assertIn((str(self.ids[ASIDE_MEANING]), 'closeness', 1.0), [(r[1], r[2], r[3]) for r in rows])
        self.vectors({ASIDE_MEANING: FAR}, {2: NEAR})
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            self.assertNotIn(ASIDE_MEANING, self.retained()[0])

    def test_nothing_that_matches_leaves_the_prompt_as_it_was(self):
        other = self.store.suggest('tax', 'Renew the parking permit', 'The city sent a renewal form.', [1])['id']
        self.assertEqual('', recall(self.app, 'preparation', {'todo': other}).text('retained'))

    def test_a_review_gets_what_bears_on_the_waiting_signals(self):
        text, _ = self.retained('review')
        self.assertTrue(text.startswith(retained_facts.REVIEW_HEAD))
        self.assertIn('- ' + ASIDE, text)
        self.assertNotIn(ASIDE_OTHER, text)
        self.assertNotIn('[', text.split('\n', 1)[1])  # no ids: nothing here is the review's to end or replace
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version')
        self.assertEqual('', self.retained('review')[0])  # nothing waits: nothing to match

    def test_the_review_prompt_has_it_after_the_slow_part(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,attempts,planned) VALUES('review-1','starting',?,?,0,1)",
                       (self.clock[0].isoformat(), self.clock[0].isoformat()))
        calls = []
        self.app.config['review_worker'] = {'enabled': True}
        self.app.review_step(lambda r: calls.append(dict(r)) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        self.assertIn('- ' + ASIDE, message[message.index(retained_facts.REVIEW_HEAD):].split('\n\n')[0])
        self.assertLess(message.index('Facts the owner told you earlier'), message.index(retained_facts.REVIEW_HEAD))
        self.assertLess(message.index(retained_facts.REVIEW_HEAD), message.index('This turn: review run'))

    def test_a_preparation_and_a_chat_turn_carry_it(self):
        self.store.decide(self.todo, 'accept', '', 'click', 'dashboard')
        calls = []
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        first = next(c['message'] for c in calls if c.get('message'))
        self.assertIn('- ' + ASIDE, first[first.index(retained_facts.TODO_HEAD):].split('\n\n')[0])
        with self.store.connect() as db:
            db.execute("UPDATE preparation_runs SET status='ok',finished_at=?", (self.clock[0].isoformat(),))
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared'")
        self.store.decide(self.todo, 'other', 'Does the riverside catering still apply?', 'chat-' + 'a' * 36, 'dashboard')
        calls.clear()
        self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        chat = next(c['message'] for c in calls if c.get('message'))
        self.assertIn('wrote to you in the chat', chat)
        block = chat[chat.index(retained_facts.TODO_HEAD):].split('\n\n')[0]
        self.assertIn('- ' + ASIDE, block)
        self.assertLessEqual(len(block), retained_facts.CHAT_CHARS)
        with self.store.connect() as db:
            logged = {r[0] for r in db.execute("SELECT purpose FROM memory_use WHERE kind='fact' AND row_id=?", (str(self.ids[ASIDE]),))}
            used = db.execute('SELECT used_at FROM facts WHERE id=?', (self.ids[ASIDE],)).fetchone()[0]
        self.assertEqual({'preparation', 'todo_chat'}, logged)
        self.assertIsNone(used)

    def test_without_embeddings_a_current_fact_that_shares_the_to_dos_words_beats_newer_ones(self):
        now = self.clock[0]
        self.clock[0] = START + dt.timedelta(days=25)  # older than every filler, so by weight alone it is left out
        old = self.store.remember_fact('Riverside catering for the Lisbon offsite is ordered a week ahead.', 'owner-note', 'preference')['id']
        unrelated = self.store.remember_fact('Parking permits are renewed online in January.', 'owner-note')['id']
        self.clock[0] = now
        picked = self.store.facts_for(self.todo, 'fact', None, accounts=ACCOUNTS)
        self.assertGreater(sum(len(f['text']) for f in self.store.facts()), 3000)  # more than fits: picking matters
        self.assertTrue(picked.startswith('- Riverside catering for the Lisbon offsite'))  # first, within the same limit
        self.assertNotIn('Parking permits', picked)
        self.assertLessEqual(len(picked), 3000)
        with self.store.connect() as db:  # picked for its words: used, like one picked by meaning
            used = {r[0]: r[1] for r in db.execute('SELECT id,used_at FROM facts WHERE id IN (?,?)', (old, unrelated))}
        self.assertEqual((used[old], used[unrelated]), (now.isoformat(), None))
        memory = recall(self.app, 'preparation', {'todo': self.todo}, 60000)
        memory.text('facts')
        self.assertIn((str(old), 'match'), [(r[1], r[2]) for r in memory.rows()])

    def test_a_fact_of_the_other_area_stays_out(self):
        with self.store.connect() as db:
            db.execute("UPDATE facts SET side='personal' WHERE id=?", (self.ids[ASIDE],))  # as a connected AI's area would say
        self.app.config['accounts'] = [{**ACCOUNTS[0], 'boundary': 'work:acme'}]
        self.assertNotIn(ASIDE, self.retained()[0])

    def test_years_of_facts_outside_the_list_are_all_looked_at_quickly(self):
        self.app.config['embeddings'] = SETTINGS
        key = f"{SETTINGS['model']}:{SETTINGS['dims']}"
        later = (START + dt.timedelta(days=41)).isoformat()  # each left the list after the ones that bear on the to-do
        with self.store.connect() as db:
            for i in range(3000):  # one shared word each ("offsite"): looked at, and too little to match
                fact = db.execute("INSERT INTO facts(text,decision_id,created_at,removed_at,kind) VALUES(?,'owner-note',?,?,'fact')",
                                  (f'Archived offsite note {i} on ledger zq{i}x.', START.isoformat(), later)).lastrowid
                db.execute('UPDATE facts SET merged_into=? WHERE id=?', (f'aside:{fact}', fact))
                db.execute('INSERT INTO fact_vectors(fact_id,model,vector) VALUES(?,?,?)', (fact, key, a.embeddings.pack(FAR)))
        self.vectors({ASIDE_MEANING: NEAR}, {2: NEAR})
        with self.store.connect() as db:
            newer = db.execute("SELECT count(*) FROM facts WHERE merged_into LIKE 'aside:%' AND removed_at>?",
                               (self.clock[0].isoformat(),)).fetchone()[0]
        self.assertGreater(newer, 500)  # past the 500 most lately removed that were looked at before
        with patch.object(retained_facts, 'LINES', 20), patch.object(retained_facts, 'CHARS', 5000):
            started = time.monotonic()
            text, rows = self.retained()
            review, _ = self.retained('review')
            took = time.monotonic() - started
        for fact in (ASIDE, ASIDE_NAMED, ASIDE_MEANING):  # by words, by name and by meaning
            self.assertIn('- ' + fact, text)
        self.assertIn('- ' + ASIDE, review)
        self.assertNotIn('Archived offsite note', text + review)
        self.assertNotIn(FORGOTTEN, text + review)
        self.assertLess(took, 10)  # some 0.3 s on a desktop

    def test_an_older_database_gets_the_index_once_after_a_copy(self):
        with self.store.connect() as db:
            for name in ('fact_search_insert', 'fact_search_update', 'fact_search_delete'):
                db.execute(f'DROP TRIGGER {name}')
            db.execute('DROP TABLE fact_search')
            db.execute('DROP INDEX fact_about_node')
        self.store = self.app.store = a.Store(self.store.path)
        copies = list(self.store.path.parent.glob('events.sqlite.before-fact-index-*'))
        self.assertEqual(1, len(copies))
        self.assertFalse(self.store.index_facts())  # once: the next start only reads the schema
        self.assertEqual(copies, list(self.store.path.parent.glob('events.sqlite.before-fact-index-*')))
        self.assertIn('- ' + ASIDE, self.retained()[0])  # facts from before the index are in it
        with self.store.connect() as db:  # kept up to date as facts change
            db.execute('UPDATE facts SET text=? WHERE id=?', ('Quarterly taxes for the Lisbon offsite venue are filed in March.', self.ids[ASIDE_OTHER]))
            db.execute('DELETE FROM facts WHERE id=?', (self.ids[ASIDE],))
            found = {r[0] for r in db.execute("SELECT rowid FROM fact_search WHERE fact_search MATCH 'lisbon'")}
        self.assertIn(self.ids[ASIDE_OTHER], found)
        self.assertNotIn(self.ids[ASIDE], found)


if __name__ == '__main__':
    unittest.main()

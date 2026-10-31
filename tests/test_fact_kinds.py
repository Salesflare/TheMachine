"""What sort a learned fact is (event, commitment, preference, fact), how fast it fades, the day it ends, and the cap that
only counts facts about no one (assistant.py remember_fact, facts_for, condense_text, retire_expired)."""
import datetime as dt
import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)

NOW = '2026-10-31T10:00:00+00:00'


def event():
    return {'account_id': 'work', 'source_id': 'one', 'kind': 'gmail.message', 'occurred_at': '2026-10-09T10:00:00+00:00',
            'title': 'A real subject', 'body': 'Original', 'metadata': {}, 'deleted': False}


class FactKinds(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.store = assistant.Store(self.path)
        self.store.commit_page('work', {}, [event()])
        self.sid = self.store.suggest('facts', 'Check the vendor', 'Body', [1])['id']
        self.store.decide(self.sid, 'reject', 'we stopped using them', 'owner-note', 'dashboard')

    def at(self, when):
        return patch.object(assistant, 'now', return_value=when)

    def test_a_fact_keeps_its_sort_and_end_day_and_an_event_ends_by_itself(self):
        with self.at(NOW):
            pref = self.store.remember_fact('Prefers calls after 10am.', 'owner-note', 'preference')
            trip = self.store.remember_fact('Is in Lisbon for a conference this week.', 'owner-note', 'event')
            due = self.store.remember_fact('Sends the board deck every first Monday.', 'owner-note', 'commitment', until='2026-12-31')
            plain = self.store.remember_fact('Uses Stripe for invoices.', 'owner-note')
            rule = self.store.remember_fact('Put the order number in the subject.', 'owner-note', 'draft', until='2026-12-01')
        self.assertEqual((pref['kind'], trip['kind'], trip['until'], due['until'], plain['kind']),
                         ('preference', 'event', '2026-11-30', '2026-12-31', 'fact'))
        with self.store.connect() as db:
            self.assertIsNone(db.execute('SELECT valid_until FROM facts WHERE id=?', (rule['id'],)).fetchone()[0])  # a rule has no end
        with self.at(NOW), self.assertRaises(ValueError):
            self.store.remember_fact('Was off sick last week.', 'owner-note', 'event', until='2026-10-01')
        with self.at(NOW), self.assertRaises(ValueError):
            self.store.remember_fact('Likes short replies.', 'owner-note', 'mood')
        facts = {f['text']: f for f in self.store.snapshot([])['facts']}
        self.assertEqual((facts['Prefers calls after 10am.']['fact_kind'], facts['Is in Lisbon for a conference this week.']['valid_until']),
                         ('preference', '2026-11-30'))
        with self.at(NOW):
            self.assertIn('- Is in Lisbon for a conference this week. (noted 2026-10-31, until 2026-11-30)', self.store.facts_text())

    def test_a_fact_past_its_end_leaves_the_prompts_and_the_condense_pass_retires_it_restorably(self):
        with self.at(NOW):
            trip = self.store.remember_fact('Is in Lisbon until Friday.', 'owner-note', 'event', until='2026-11-06')
            self.store.remember_fact('Uses Stripe for invoices.', 'owner-note')
        later = '2026-11-08T09:00:00+00:00'
        with self.at(later):
            self.assertNotIn('Lisbon', self.store.facts_text())
            self.assertNotIn('Lisbon', self.store.facts_for(self.sid))
            self.assertEqual(self.store.retire_expired(), 1)
            self.assertEqual(self.store.retire_expired(), 0)
            self.assertNotIn('Lisbon', self.store.condense_text(least=1))
            snap = self.store.snapshot([])
        self.assertEqual([f['text'] for f in snap['facts_ended']], ['Is in Lisbon until Friday.'])
        app = object.__new__(assistant.App); app.store = self.store; app.config = {'accounts': []}
        with self.assertRaises(ValueError):  # only the owner brings one back
            app.action('unmerge_fact', {'expired': trip['id']})
        with self.at(later):
            app.action('unmerge_fact', {'expired': trip['id']}, owner_dashboard=True)
            self.assertIn('Lisbon', self.store.facts_text())  # back, without an end day, so it doesn't retire again
            self.assertEqual(self.store.retire_expired(), 0)
            with self.assertRaises(ValueError):
                self.store.unmerge_fact(expired=trip['id'])

    def test_weight_fades_by_sort_and_starts_over_when_said_again(self):
        made = '2026-10-01T10:00:00+00:00'
        w = lambda sort, at, **more: assistant.fact_weight({'fact_kind': sort, 'created_at': made, **more}, at)
        self.assertAlmostEqual(w('event', '2026-10-08T10:00:00+00:00'), 0.3679, places=3)  # one half-life: e^-1, as GBrain
        self.assertGreater(w('preference', '2026-10-08T10:00:00+00:00'), 0.9)
        self.assertGreater(w('fact', '2027-01-01T10:00:00+00:00'), w('commitment', '2027-01-01T10:00:00+00:00'))
        self.assertEqual(w(None, made), 1.0)  # older facts and rules read as fact
        self.assertEqual(w('fact', '2026-11-02T10:00:00+00:00', valid_until='2026-11-01'), 0.0)
        self.assertEqual(w('event', '2026-10-08T10:00:00+00:00', confirmed_at='2026-10-08T10:00:00+00:00'), 1.0)
        with self.at(made):
            first = self.store.remember_fact('Is moving house this month.', 'owner-note', 'event')
        with self.at(NOW):
            self.assertTrue(self.store.remember_fact('is moving house this month.', 'owner-note', 'event')['duplicate'])
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT confirmed_at FROM facts WHERE id=?', (first['id'],)).fetchone()[0], NOW)

    def test_a_preparation_puts_what_still_counts_first(self):
        # More than FACTS_ALL_UNDER: without embeddings, the facts that count most go first, not just the newest.
        with self.at('2026-06-01T10:00:00+00:00'):
            old_event = self.store.remember_fact('Had a long offsite planning week with the whole team in June.', 'owner-note', 'event', until='2026-12-31')
        with self.at('2026-10-01T10:00:00+00:00'):
            for n in range(30):
                self.store.remember_fact(f'Vendor number {n} is handled by the finance team, not by the owner.', 'owner-note')
        with self.at(NOW):
            out = self.store.facts_for('another-card', limit=400)
        self.assertNotIn('offsite', out)
        self.assertIn('Vendor number', out)
        self.assertTrue(old_event['id'])

    def test_facts_about_someone_dont_count_toward_the_cap(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO graph_nodes(id,kind,name,strength,signals,info) VALUES('email:lee@globex.example','person','Lee',1,0,'{}')")
        with self.at(NOW):
            for n in range(assistant.FACTS_GENERAL_MAX):
                self.store.remember_fact(f'General fact number {n} about how the owner works.', 'owner-note')
            with self.assertRaises(ValueError):
                self.store.remember_fact('One general fact too many for the list.', 'owner-note')
            for n in range(5):  # about someone: still saved
                self.assertIn('id', self.store.remember_fact(f'Lee prefers email over calls, note {n}.', 'owner-note', 'preference',
                                                             about=['email:lee@globex.example']))
            # Condensing two general facts frees their places for the one they become.
            with self.store.connect() as db:
                ids = [r[0] for r in db.execute("SELECT id FROM facts WHERE text LIKE 'General fact number 1_ %' ORDER BY id LIMIT 2")]
            self.assertEqual(self.store.remember_fact('General facts ten and eleven, said once.', None, replaces=ids)['merged'], 2)

    def test_an_old_database_gets_the_new_columns_and_keeps_its_facts(self):
        with self.store.connect() as db:  # the facts table as it was before sorts and end days
            db.execute("INSERT INTO facts(text,decision_id,suggestion_id,created_at,kind) VALUES('Uses Stripe for invoices.','owner-note',?,?,'fact')",
                       (self.sid, NOW))
        raw = sqlite3.connect(self.path)
        raw.executescript('''CREATE TABLE facts_old(id INTEGER PRIMARY KEY,text TEXT NOT NULL,decision_id TEXT NOT NULL,suggestion_id TEXT,
                             created_at TEXT NOT NULL,removed_at TEXT,kind TEXT NOT NULL DEFAULT 'fact',merged_into TEXT);
                             INSERT INTO facts_old SELECT id,text,decision_id,suggestion_id,created_at,removed_at,kind,merged_into FROM facts;
                             DROP TABLE facts; ALTER TABLE facts_old RENAME TO facts;''')
        raw.close()
        raw = sqlite3.connect(self.path)
        self.assertNotIn('fact_kind', {r[1] for r in raw.execute('PRAGMA table_info(facts)')})
        raw.close()
        store = assistant.Store(self.path)
        with store.connect() as db:
            self.assertLessEqual({'fact_kind', 'valid_until', 'confirmed_at'}, {r[1] for r in db.execute('PRAGMA table_info(facts)')})
        with self.at(NOW):
            self.assertEqual(store.facts_text(), '- Uses Stripe for invoices.')
            self.assertEqual(store.retire_expired(), 0)
            self.assertIn('(fact)', store.condense_text(least=1))
            self.assertEqual(store.remember_fact('Off on Fridays in November.', 'owner-note', 'event', until='2026-11-30')['until'], '2026-11-30')
        assistant.Store(self.path)  # opening again changes nothing


if __name__ == '__main__':
    unittest.main()

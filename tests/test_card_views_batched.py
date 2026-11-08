"""The to-do list's card views (card_views, suggestion_result) read what every card needs once for all cards, not once
per card: the payload is the same as card by card, and a card with nothing in a table costs no read of that table."""
import datetime as dt
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('batched_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
NOW = dt.datetime(2026, 11, 8, 9, tzinfo=dt.timezone.utc)
ACCOUNTS = [{'id': 'work', 'email': 'sam@acme.com'}]


def event(n, kind='gmail.message', url=None):
    meta = {'from': 'Ann <ann@client.com>', 'to': 'sam@acme.com', 'message-id': f'<{n}@x>', 'thread_id': f't{n}'}
    if url:
        meta['source_url'] = url
    return {'account_id': 'work', 'source_id': f'm{n}', 'kind': kind, 'occurred_at': (NOW - dt.timedelta(hours=n)).isoformat(),
            'title': f'Mail {n}', 'body': 'Hello', 'deleted': False, 'metadata': meta}


def insert(db, table, **values):
    """A row with the given values, the other required columns filled in (the schema grows; the test need not)."""
    for _, name, kind, notnull, default, pk in db.execute(f'PRAGMA table_info({table})').fetchall():
        if notnull and default is None and not pk and name not in values:
            values[name] = 0 if 'INT' in (kind or '').upper() else ''
    db.execute(f'INSERT INTO {table}({",".join(values)}) VALUES({",".join("?" * len(values))})', list(values.values()))


class CardViewsBatched(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        self.store.owner_user_ids = set()
        self.store.accounts = ACCOUNTS
        clock = patch_everywhere(a, 'now', lambda: NOW.isoformat())
        clock.start(); self.addCleanup(clock.stop)
        events = [event(1, url='https://example.com/one'), event(2, url='https://example.com/two'), event(3), event(4, url='https://example.com/one')]
        for e in events:
            self.store.commit_page('work', {}, [e])
        with self.store.connect() as db:
            ids = [db.execute('SELECT id FROM events WHERE source_id=?', (e['source_id'],)).fetchone()[0] for e in events]
        # Cards that share messages, in another order, with none, and one that is done
        self.cards = [self.store.suggest('k1', 'Answer Ann', 'Ann asked.', [ids[1], ids[0]])['id'],
                      self.store.suggest('k2', 'Send the deck', 'The deck.', [ids[0], ids[3], ids[0]])['id'],
                      self.store.suggest('k3', 'Book the room', 'A room.', [ids[2]])['id'],
                      self.store.suggest('k4', 'Plan the week', 'Plan.', [ids[2]])['id']]
        self.ids = ids
        with self.store.connect() as db:
            first, second, third, fourth = self.cards
            db.execute("UPDATE suggestions SET event_ids='[]' WHERE id=?", (fourth,))  # none: a to-do the owner made
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (third,))
            db.execute("UPDATE suggestions SET project='Launch' WHERE id IN (?,?)", (first, second))
            insert(db, 'projects', name='Launch', created_at=NOW.isoformat())
            insert(db, 'preparations', suggestion_id=first, decision_id='d1', job_id='job-1', status='ready', reason='Drafted',
                   created_at=NOW.isoformat(), updated_at=NOW.isoformat())
            insert(db, 'skill_clusters', id='c1', fact_ids='[]', name='Decks', description='Sending decks', body='Send it.', suggestion_id=second,
                   status='pending', created_at=NOW.isoformat(), updated_at=NOW.isoformat())
            for n, (card, text) in enumerate([(first, 'Shorter please'), (first, 'Even shorter'), (third, 'Done by hand')]):
                insert(db, 'decisions', id=f'fb{n}', suggestion_id=card, choice='other', feedback=text, source='dashboard',
                       created_at=(NOW + dt.timedelta(minutes=n)).isoformat())

    def views(self, ids):
        with self.store.connect() as db:
            cards = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (i,)).fetchone()) for i in ids]
            self.store.card_views(db, cards, jobs=False)
            self.store.card_views(db, cards, jobs=True)
        return {c['id']: json.loads(json.dumps(c, sort_keys=True, default=str)) for c in cards}

    def test_all_at_once_is_card_by_card(self):
        together = self.views(self.cards)
        one_by_one = {}
        for i in self.cards:
            one_by_one.update(self.views([i]))
        self.assertEqual(together, one_by_one)
        first, second, third, fourth = self.cards
        self.assertEqual(together[first]['original_urls'], ['https://example.com/two', 'https://example.com/one'])  # in the card's order
        self.assertEqual(together[second]['original_urls'], ['https://example.com/one'])  # once, though two messages link it
        self.assertEqual(together[first]['latest_feedback']['feedback'], 'Even shorter')
        self.assertIsNone(together[second]['latest_feedback'])
        self.assertEqual(together[first]['project_node']['name'], 'Launch')
        self.assertEqual(together[fourth]['original_urls'], [])

    def test_batched_reads_match_the_reads_per_card(self):
        with self.store.connect() as db:
            cards = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (i,)).fetchone()) for i in self.cards]
            pre = self.store.card_reads(db, cards)
            for card in cards:
                self.assertEqual(self.store.suggestion_result(dict(card), db, pre), self.store.suggestion_result(dict(card), db), card['title'])

    def test_a_card_with_nothing_in_a_table_costs_no_read_of_it(self):
        many = [self.store.suggest(f'x{n}', f'Card {n}', 'Body.', [self.ids[n % 4]])['id'] for n in range(12)]
        seen = []
        with self.store.connect() as db:
            cards = [dict(db.execute('SELECT * FROM suggestions WHERE id=?', (i,)).fetchone()) for i in self.cards + many]
            db.set_trace_callback(seen.append)
            self.store.card_views(db, cards, jobs=False)
            self.store.card_views(db, cards, jobs=True)
            db.set_trace_callback(None)
        batched = {'skill_clusters': 'SELECT * FROM skill_clusters WHERE suggestion_id=', 'skills': 'SELECT * FROM skills WHERE task=',
                   'skill_task_decided': 'SELECT name,choice FROM skill_task_decided WHERE task=', 'preparations': 'SELECT job_id,status,reason FROM preparations WHERE suggestion_id=',
                   'action_jobs': 'SELECT j.id,j.revision', 'decisions': 'SELECT id,feedback,choice'}
        having = {'skill_clusters': 1, 'skills': 0, 'skill_task_decided': 0, 'preparations': 0, 'action_jobs': 0, 'decisions': 2}
        for table, start in batched.items():  # one read per card that has a row there, none for the others
            self.assertEqual(sum(s.startswith(start) for s in seen), having[table], table)
        self.assertLessEqual(sum('FROM events' in s and 'json_each' not in s for s in seen), 1, 'the cards\' messages are read once')
        self.assertLessEqual(sum("kind='whatsapp.message'" in s for s in seen), 1, 'WhatsApp photos are looked up once')


if __name__ == '__main__':
    unittest.main()

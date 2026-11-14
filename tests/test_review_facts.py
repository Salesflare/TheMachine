"""The facts a review gets once they no longer all fit (machine/app/review_facts.py): inside the same cap, the
standing ones first, then the ones closest to the batch, and a turn for the one a review saw longest ago."""
import datetime as dt
import importlib.util
import os
import re
import tempfile
import unittest
from pathlib import Path

from seams import patch_everywhere

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location('review_facts_assistant', ROOT / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import memory_use  # noqa: E402
from machine.app import review_facts  # noqa: E402
from machine.app.recall import recall  # noqa: E402

NOW = dt.datetime(2026, 10, 16, 12, tzinfo=dt.timezone.utc)
SETTINGS = {'url': 'http://embed.invalid', 'model': 'm', 'dims': 2}
NEAR, FAR = [1.0, 0.0], [0.0, 1.0]
CAP = review_facts.LIMIT


def mail(n, title):
    return {'account_id': 'work', 'source_id': f'p{n}', 'kind': 'gmail.message', 'occurred_at': (NOW - dt.timedelta(hours=n)).isoformat(),
            'title': title, 'body': 'Body', 'deleted': False,
            'metadata': {'from': 'Ann Example <ann@client.example>', 'to': 'sam@acme.example', 'cc': '', 'labels': ['INBOX'],
                         'message-id': f'<p{n}@x>', 'thread_id': f'tp{n}'}}


class ReviewFactsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.store = a.Store(Path(temp.name) / 'events.sqlite')
        self.app = object.__new__(a.App)
        self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}], 'embeddings': SETTINGS, 'review_worker': {'enabled': True}}
        self.clock = [NOW]
        started = patch_everywhere(a, 'now', lambda: self.clock[0].isoformat())
        started.start()
        self.addCleanup(started.stop)
        self.store.commit_page('work', {}, [mail(1, 'Pilot timing')])
        self.signal = 1
        other = self.store.suggest('other', 'Pay the vendor', 'Body', [1])['id']
        self.store.decide(other, 'reject', 'we stopped using them', 'owner-note', 'dashboard')  # the note the facts come from

    def learn(self, count, start=0, about='org:client.example'):
        """Facts about a record (about=None: about no one), each a minute later, so the newest is the newest."""
        ids = []
        for i in range(start, start + count):
            self.clock[0] += dt.timedelta(minutes=1)
            ids.append(self.store.remember_fact(f'Fact number {i} about how the owner works with pilots and renewals there.', 'owner-note', quote='we stopped using them')['id'])
        if about:
            with self.store.connect() as db:
                db.executemany("INSERT INTO fact_about(fact_id,node_id,by,created_at) VALUES(?,?,'review',?)", [(i, about, NOW.isoformat()) for i in ids])
        return ids

    def vectors(self, facts, signal=NEAR):
        """Stored vectors, as a preparation and the embedding worker leave them: {fact id: vector}, and the waiting signal's."""
        with self.store.connect() as db:
            db.executemany('INSERT OR REPLACE INTO fact_vectors(fact_id,model,vector) VALUES(?,?,?)',
                           [(i, 'm:2', a.embeddings.pack(v)) for i, v in facts.items()])
            version = db.execute('SELECT version FROM events WHERE id=?', (self.signal,)).fetchone()[0]
            db.execute('INSERT OR REPLACE INTO event_vectors(event_id,version,model,dims,vector) VALUES(?,?,?,?,?)',
                       (self.signal, version, 'm', 2, a.embeddings.pack(signal)))

    def read(self, run='run', log=True):
        """One review's two fact blocks the way its builder reads them, logged as an admitted run's are."""
        self.clock[0] += dt.timedelta(minutes=30)
        memory = recall(self.app, 'review', {'run': run}, 100000)
        first, batch = memory.text('facts'), memory.text('batch_facts')
        if log:
            memory_use.record(self.store, 'review', memory.rows(), run)
        return first, batch, memory

    @staticmethod
    def listed(text):
        return [int(i) for i in re.findall(r'^- \[(\d+)\] ', text, re.M)]

    def test_while_they_fit_the_review_gets_the_whole_list_as_before(self):
        self.learn(20)
        first, batch, memory = self.read()
        self.assertEqual(first, self.store.facts_text(ids=True))
        self.assertEqual('', batch)
        self.assertEqual(20, len(self.listed(first)))
        self.assertEqual({'always'}, {i.how for i in memory.items()})

    def test_the_cap_holds_and_the_prompt_is_no_bigger_than_the_cut_list_was(self):
        ids = self.learn(60)
        self.vectors({i: NEAR if n % 2 else FAR for n, i in enumerate(ids)})
        before = self.store.facts_text(ids=True)
        self.assertTrue(before.endswith('\n…'))  # past the cap: main cut it here
        for run in range(8):
            first, batch, _ = self.read(f'run-{run}')
            self.assertLessEqual(len(first) + len(batch), CAP)
            self.assertLessEqual(len(first) + len(batch), len(before))
            self.assertEqual(len(set(self.listed(first + '\n' + batch))), len(self.listed(first + '\n' + batch)))  # none twice
        self.app.config.pop('embeddings')  # and without meaning search
        first, batch, _ = self.read('run-off')
        self.assertLessEqual(len(first) + len(batch), CAP)

    def test_standing_facts_keep_their_place_whatever_the_batch(self):
        ids = self.learn(60)
        general = self.learn(3, 60, about=None)  # about no one: they hold for any batch, and are close to none
        kept = ids[3]
        self.store.edit_fact(kept, 'The owner wrote this one about them in their own words, so it stays.')
        self.vectors({i: FAR for i in ids + general if i != kept})  # far from the batch, and the edited one has no vector yet
        texts = set()
        for run in range(6):
            first, batch, memory = self.read(f'run-{run}')
            texts.add(first)
            self.assertEqual([kept, *general], self.listed(first))  # in id order
            self.assertFalse({kept, *general} & set(self.listed(batch)))
            how = {int(i.row_id): i.how for i in memory.items()}
            self.assertEqual({'always'}, {how[i] for i in (kept, *general)})
        self.assertEqual(1, len(texts))  # the same bytes every time
        message = a.review_prompt('r' * 32, ['work'], 'history', first, promises='promises', batch_facts=batch)
        self.assertLess(message.index(f'- [{kept}] '), message.index('What the owner did with suggestions'))
        self.assertLess(message.index('Open promises'), message.index('More facts the owner told you earlier'))
        self.assertLess(message.index('More facts the owner told you earlier'), message.index('This turn: review run'))

    def test_more_standing_facts_than_half_the_room_the_latest_stay_and_the_others_take_turns(self):
        general = self.learn(60, about=None)
        self.app.config.pop('embeddings')
        reached = set()
        for run in range(12):
            first, batch, memory = self.read(f'run-{run}')
            standing = self.listed(first)
            self.assertLessEqual(len(first), CAP * review_facts.STANDING_SHARE)
            self.assertEqual(general[-len(standing):], standing)  # the most lately said, as the old cut chose
            self.assertLessEqual(len(first) + len(batch), CAP)
            reached |= set(standing) | set(self.listed(batch))
        self.assertEqual(set(general), reached)

    def test_a_fact_about_who_a_waiting_signal_is_with_gets_in_first(self):
        ids = self.learn(60, about='org:other.example')
        theirs = set(ids[:3])  # the oldest: main's cut left exactly these out
        with self.store.connect() as db:
            db.executemany("UPDATE fact_about SET node_id='org:client.example' WHERE fact_id=?", [(i,) for i in theirs])
            db.execute("INSERT INTO graph_events(node_id,event_id,at) VALUES('org:client.example',?,?)", (self.signal, NOW.isoformat()))
        self.vectors({i: FAR if i in theirs else NEAR for i in ids})  # by meaning alone the others would lead
        for label in ('on', 'off'):
            for run in range(4):
                _, batch, memory = self.read(f'{label}-{run}')
                self.assertLessEqual(theirs, set(self.listed(batch)))
                self.assertEqual({'about'}, {i.how for i in memory.items() if int(i.row_id) in theirs})
            self.app.config.pop('embeddings', None)

    def test_a_fact_close_to_the_batch_gets_in_over_a_far_one(self):
        ids = self.learn(60)
        near = set(ids[:5])  # the oldest: main's cut left exactly these out
        self.assertFalse(near & set(self.listed(self.store.facts_text(ids=True))))
        self.vectors({i: NEAR if i in near else FAR for i in ids})
        for run in range(4):
            _, batch, memory = self.read(f'run-{run}')
            how = {int(i.row_id): (i.how, i.score) for i in memory.items()}
            self.assertLessEqual(near, set(self.listed(batch)))
            self.assertEqual({'closeness'}, {how[i][0] for i in near})
            self.assertTrue(all(how[i][1] > 0.9 for i in near))
            far = [i for i in self.listed(batch) if i not in near]
            self.assertTrue(far and len(far) < 55)  # the far ones share the rest of the room by turns
            self.assertEqual({('rotation', None)}, {how[i] for i in far})
        self.vectors({}, signal=FAR)  # another batch: now the others are the close ones
        _, batch, memory = self.read('run-far')
        self.assertEqual({'closeness'}, {i.how for i in memory.items() if int(i.row_id) not in near and i.how != 'rotation'})
        self.assertFalse({i.row_id for i in memory.items() if i.how == 'closeness'} & {str(i) for i in near})

    def test_no_fact_is_left_out_forever_with_or_without_meaning_search(self):
        ids = self.learn(60)
        for label, vectors in (('off', None), ('on', {i: FAR for i in ids})):
            if vectors is None:
                self.app.config.pop('embeddings')
            else:
                self.app.config['embeddings'] = SETTINGS
                self.vectors(vectors, signal=FAR)  # every fact as close as the next: closeness alone would keep one set
            reached, waits, last = set(), {}, {}
            for run in range(12):
                first, batch, memory = self.read(f'{label}-{run}')
                for i in self.listed(first + '\n' + batch):
                    waits[i] = max(waits.get(i, 0), run - last.get(i, run))
                    last[i] = run
                reached |= set(self.listed(batch))
            self.assertEqual(set(ids), reached, label)
            self.assertLessEqual(max(waits.values()), 8, label)
            hows = {i.how for i in memory.items()}
            self.assertEqual({'recency', 'rotation'} if vectors is None else {'closeness', 'rotation'}, hows)
        new = self.learn(1, 60)[0]  # a new one is shown at once, before it has a vector
        self.assertIn(new, self.listed(self.read('new')[1]))

    def test_a_review_that_was_not_sent_takes_no_turn(self):
        self.learn(60)
        self.app.config.pop('embeddings')
        one = self.read('a', log=False)[1]
        self.assertEqual(one, self.read('b', log=False)[1])  # nothing was logged: the same facts wait their turn
        self.read('c')
        self.assertNotEqual(one, self.read('d')[1])

    def test_the_pick_is_logged_with_how_and_score_and_is_not_a_use(self):
        ids = self.learn(60)
        self.vectors({i: NEAR if n < 5 else FAR for n, i in enumerate(ids)})
        with self.store.connect() as db:
            db.execute("UPDATE facts SET used_at='2026-09-01T00:00:00+00:00'")
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,attempts,planned) VALUES('review-1','starting',?,?,0,1)",
                       (self.clock[0].isoformat(), self.clock[0].isoformat()))
        calls = []
        self.app.review_step(lambda r: calls.append(dict(r)) or {'status': 'admitted'})
        message = next(c for c in calls if c.get('message'))['message']
        with self.store.connect() as db:
            rows = [tuple(r) for r in db.execute("SELECT row_id,how,score,chars,run_id FROM memory_use WHERE purpose='review' AND kind='fact' ORDER BY id")]
            used = {r[0] for r in db.execute('SELECT used_at FROM facts')}
        self.assertEqual(sorted(self.listed(message)), sorted(int(r[0]) for r in rows))
        close = [r for r in rows if r[1] == 'closeness']
        self.assertEqual({str(i) for i in ids[:5]}, {r[0] for r in close})
        self.assertTrue(all(r[2] is not None and r[2] > 0.9 for r in close))
        turns = [r for r in rows if r[1] == 'rotation']
        self.assertTrue(turns and all(r[2] is None for r in turns))
        self.assertTrue(all(r[3] > 0 and r[4] == 'review-1' for r in rows))
        for r in rows:  # the characters are those of its line in the prompt
            self.assertEqual(r[3], len(next(line for line in message.splitlines() if line.startswith(f'- [{r[0]}] '))))
        self.assertEqual({'2026-09-01T00:00:00+00:00'}, used)  # a review's pick never stamps used_at

    def test_two_batches_share_the_prompt_up_to_the_picked_block(self):
        ids = self.learn(60)
        self.store.edit_fact(ids[0], 'The owner wrote this one in their own words, so it stays.')
        self.vectors({i: NEAR if n < 5 else FAR for n, i in enumerate(ids)})
        first, one, _ = self.read('a')
        self.vectors({}, signal=FAR)
        again, two, _ = self.read('b')
        self.assertEqual(first, again)
        self.assertNotEqual(one, two)
        build = lambda run, batch: a.review_prompt(run, ['work'], 'history', first, promises='promises', batch_facts=batch)
        shared = os.path.commonprefix([build('a' * 32, one), build('b' * 32, two)])
        self.assertIn('Open promises', shared)  # everything that changes slowly is still one cached prefix
        self.assertIn('More facts the owner told you earlier', shared)


if __name__ == '__main__':
    unittest.main()

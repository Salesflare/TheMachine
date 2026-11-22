"""Search by meaning scores from an in-memory 8-bit copy of the vectors (embeddings.Index) and reads only the close ones
exactly: the same results as reading and comparing every stored vector, kept current as vectors change."""
import array
import contextlib
import math
import random
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import embeddings as emb
import machine.main as machine_main

DIMS = 256
SETTINGS = {'url': 'http://127.0.0.1:9', 'model': 'm', 'dims': DIMS}


def unit(vector):
    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [x / norm for x in vector]


class Fake:
    """Vectors around a few topics, so many are close to a question and to each other, like real mail."""
    def __init__(self, seed):
        self.rnd = random.Random(seed)
        self.topics = [unit([self.rnd.gauss(0, 1) for _ in range(DIMS)]) for _ in range(12)]

    def vector(self, topic=None, noise=None):
        centre = self.topics[self.rnd.randrange(len(self.topics)) if topic is None else topic]
        noise = self.rnd.uniform(0.6, 2.5) if noise is None else noise
        return unit([x + self.rnd.gauss(0, 1) * noise / 16 for x in centre])


class Bounds(unittest.TestCase):
    def test_every_estimate_is_within_its_error_bound(self):
        fake, index = Fake(1), emb.Index(None, DIMS)
        rows = [fake.vector() for _ in range(300)] + [[1.0] + [0.0] * (DIMS - 1), [DIMS ** -0.5] * DIMS, [0.0] * DIMS,
                                                     unit([(-1) ** i * (i % 7) for i in range(DIMS)])]
        for n, vector in enumerate(rows):
            index.put(n << emb.SHIFT, emb.pack(vector))
        stored = [array.array('f', emb.pack(v)) for v in rows]
        probes = [fake.vector() for _ in range(8)]
        for probe in probes + [rows[0], [1.0] + [0.0] * (DIMS - 1), unit([1.0] * DIMS)]:
            values, off, step, spread = index.lanes(probe)
            for slot, vector in enumerate(stored):
                exact = math.sumprod(probe, vector)
                scale, size = index.scales[slot], index.sizes[slot]
                estimate, error = (values[slot] - off) * step * scale, scale * spread + step / 2 * size + emb.SLACK
                self.assertLessEqual(abs(exact - estimate), error, slot)
                if probe in probes and slot < 300:
                    self.assertLess(error, 0.05)  # tight enough to leave out nearly everything
        self.assertIsNone(index.lanes([0.0] * DIMS))  # a probe of zeros: every cosine is 0

    def test_a_slot_used_again_and_vectors_added_since_the_last_search_score_as_theirs(self):
        # Values are kept by dimension and new vectors wait until a search: a freed slot written over, between and after
        # searches, scores as the vector now in it
        fake, index = Fake(4), emb.Index(None, DIMS)
        rows = [fake.vector() for _ in range(40)]
        for n, vector in enumerate(rows):
            index.put(n << emb.SHIFT, emb.pack(vector))
        probe = fake.vector()
        index.lanes(probe)
        for slot in (3, 17):
            index.keys[slot] = -1
            index.free.append(slot)
        for n in range(6):
            rows.append(fake.vector())
            index.put((40 + n) << emb.SHIFT, emb.pack(rows[-1]))
        where = {key >> emb.SHIFT: slot for slot, key in enumerate(index.keys)}
        self.assertEqual(len(index.keys), 44)
        values, off, step, spread = index.lanes(probe)
        for event_id in range(46):
            if event_id in (3, 17):
                continue
            slot = where[event_id]
            exact = math.sumprod(probe, array.array('f', emb.pack(rows[event_id])))
            scale, size = index.scales[slot], index.sizes[slot]
            estimate, error = (values[slot] - off) * step * scale, scale * spread + step / 2 * size + emb.SLACK
            self.assertLessEqual(abs(exact - estimate), error, event_id)

    def test_memory_is_the_values_at_8_bits_and_a_few_numbers_per_vector(self):
        index, fake = emb.Index(None, DIMS), Fake(2)
        for n in range(1000):
            index.put(n << emb.SHIFT, emb.pack(fake.vector()))
        held = index.held() + index.keys.itemsize * len(index.keys) + index.scales.itemsize * 2 * len(index.scales)
        self.assertEqual(held, 1000 * (DIMS + 16))


class Search(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = machine_main.Store(Path(self.temp.name) / 'events.sqlite')
        for kept in (emb.INDEXES, emb.FAILED, emb.BUILDING):
            kept.clear(); self.addCleanup(kept.clear)
        self.fake = fake = Fake(3)
        with self.store.connect() as db:
            db.executemany("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                           "VALUES(?,?,'meeting.transcript','2026-11-01T00:00:00+00:00',?,?,'{}','h','2026-11-01T00:00:00+00:00')",
                           [('work' if i % 3 else 'home', str(i), f'plan {i % 9}', f'notes on item {i % 13} and plan {i % 5}') for i in range(1500)])
            self.events = [r[0] for r in db.execute('SELECT id FROM events ORDER BY id')]
            db.executemany('INSERT INTO event_vectors(event_id,version,model,dims,vector) VALUES(?,1,?,?,?)',
                           [(i, 'm', DIMS, emb.pack(fake.vector())) for i in self.events])
            db.executemany('INSERT INTO event_passages(event_id,seq,version,model,dims,start,chars,vector) VALUES(?,?,1,?,?,?,80,?)',
                           [(i, s, 'm', DIMS, 2000 + 100 * s, emb.pack(fake.vector())) for i in self.events[:60] for s in range(6)])
            db.executemany('UPDATE events SET deleted=1 WHERE id=?', [(i,) for i in self.events[::41]])
            db.executemany('UPDATE events SET version=2 WHERE id=?', [(i,) for i in self.events[5::37]])  # vector not current
            db.executemany('UPDATE events SET history=1 WHERE id=?', [(i,) for i in self.events[7::29]])

    def search(self, probe, query='', seeds=(), **kwargs):
        with patch.object(emb, 'embed', side_effect=lambda settings, texts, timeout=30: [probe] * len(texts)):
            found = emb.related(self.store.connect, SETTINGS, kwargs.pop('accounts', ['work', 'home']), seeds, query, **kwargs)
        return [(hit[0], hit[1], hit.start, hit.chars) for hit in found]

    def every_vector(self, *args, **kwargs):
        with patch.object(emb, 'held_index', lambda *args: contextlib.nullcontext()):
            return self.search(*args, **kwargs)

    def assert_same(self, rounds=10):
        fake, some = self.fake, 0
        for n in range(rounds):
            probe = fake.vector(noise=fake.rnd.uniform(0.3, 1.2))
            cases = [((probe, 'plan 3 notes'), {}), ((probe, 'item 4'), {'accounts': ['work'], 'signals_only': True, 'limit': 20}),
                     ((probe, 'zzz'), {'limit': 3, 'query_floor': 0.1}),
                     ((None, '', [self.events[60 + 11 * n]]), {'floor': 0.2}),
                     ((probe, 'plan', self.events[100 + n:102 + n]), {'floor': 0.25, 'exclude': self.events[200:260]})]
            if n == 0:
                cases.append(((probe, 'notes'), {'floor': 0.0, 'query_floor': -1.0, 'limit': 40}))  # everything ranks
            for args, kwargs in cases:
                found = self.search(*args, **dict(kwargs))
                self.assertEqual(found, self.every_vector(*args, **dict(kwargs)), (n, kwargs))
                some += any(similarity is not None for _, similarity, _, _ in found)
        self.assertGreater(some, rounds * 4)  # the fixture has close ones: most searches find some by meaning

    def test_results_are_the_same_as_comparing_every_stored_vector_also_after_changes(self):
        reads = []
        real_read = emb.Index.read
        with patch.object(emb.Index, 'read', lambda index, db, model, changed: (reads.append(changed), real_read(index, db, model, changed))[1]):
            self.assert_same()
            self.assertEqual(reads[0], None)  # the first search reads them all, the next ones nothing
            self.assertEqual({tuple(r) if r is not None else None for r in reads[1:]}, {()})
            fake, events = self.fake, self.events
            with self.store.connect() as db:  # re-embedded, gone, a new version, new passages, a new signal
                db.executemany('UPDATE event_vectors SET vector=? WHERE event_id=?', [(emb.pack(fake.vector()), i) for i in events[300:340]])
                db.executemany('DELETE FROM event_vectors WHERE event_id=?', [(i,) for i in events[400:420]])
                db.executemany('DELETE FROM event_passages WHERE event_id=? AND seq=2', [(i,) for i in events[:30]])
                db.executemany('UPDATE events SET version=version+1 WHERE id=?', [(i,) for i in events[500:510]])
                db.executemany('INSERT INTO event_passages(event_id,seq,version,model,dims,start,chars,vector) VALUES(?,9,1,?,?,3000,80,?)',
                               [(i, 'm', DIMS, emb.pack(fake.vector())) for i in events[600:620]])
                db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                           "VALUES('work','new','gmail.message','2026-11-02T00:00:00+00:00','plan 3','notes','{}','h','2026-11-02T00:00:00+00:00')")
                db.execute("INSERT INTO event_vectors(event_id,version,model,dims,vector) SELECT id,1,'m',?,? FROM events WHERE source_id='new'",
                           (DIMS, emb.pack(fake.topics[0])))
            reads.clear()
            self.assert_same(4)
            self.assertEqual(len(reads[0]), 40 + 20 + 30 + 20 + 1)  # only the changed signals again
            self.assertNotIn(None, reads)
            with self.store.connect() as db:  # another model: its own index, the first one's kept as it was
                db.executemany("INSERT INTO event_vectors(event_id,version,model,dims,vector) VALUES(?,1,'m2',?,?) "
                               "ON CONFLICT(event_id) DO UPDATE SET model='m2',vector=excluded.vector", [(i, DIMS, emb.pack(fake.vector())) for i in events[:200]])
            SETTINGS['model'] = 'm2'
            try:
                self.assert_same(2)
            finally:
                SETTINGS['model'] = 'm'
            self.assertEqual(sorted(k[1] for k in emb.INDEXES), ['m', 'm2'])

    def test_an_index_left_behind_by_the_change_log_reads_everything_again(self):
        probe = self.fake.vector()
        self.assertEqual(self.search(probe, 'plan'), self.every_vector(probe, 'plan'))
        with self.store.connect() as db, patch.object(emb, 'CHANGES_KEPT', 10):
            db.executemany('UPDATE event_vectors SET vector=? WHERE event_id=?', [(emb.pack(self.fake.vector()), i) for i in self.events[:50]])
            emb.trim_changes(db)
            self.assertEqual(db.execute('SELECT count(*) FROM event_vector_changes').fetchone()[0], 10)
        reads = []
        real_read = emb.Index.read
        with patch.object(emb.Index, 'read', lambda index, db, model, changed: (reads.append(changed), real_read(index, db, model, changed))[1]):
            self.assertEqual(self.search(probe, 'plan'), self.every_vector(probe, 'plan'))
        self.assertEqual(reads, [None])

    def test_vectors_it_cannot_hold_are_searched_by_reading_each(self):
        with self.store.connect() as db:
            db.execute('UPDATE event_vectors SET vector=? WHERE event_id=?', (emb.pack([0.5] * 4), self.events[1]))  # another length
        probe = self.fake.vector()
        reads = []
        real_read = emb.Index.read
        with patch.object(emb.Index, 'read', lambda index, db, model, changed: (reads.append(changed), real_read(index, db, model, changed))[1]):
            for _ in range(2):
                self.assertEqual(self.search(probe, 'plan'), self.every_vector(probe, 'plan'))
        self.assertEqual((emb.INDEXES, reads), ({}, [None]))  # tried once, not on every search

    def test_a_big_index_is_read_by_a_thread_while_searches_read_every_vector(self):
        probe, reads = self.fake.vector(), []
        real_read = emb.Index.read
        with patch.object(emb, 'INLINE', 1000), \
                patch.object(emb.Index, 'read', lambda index, db, model, changed: (reads.append(changed), real_read(index, db, model, changed))[1]):
            self.assertEqual(self.search(probe, 'plan'), self.every_vector(probe, 'plan'))
            for thread in threading.enumerate():
                if thread.name == 'meaning-index':
                    thread.join()
            self.assertEqual(([key[1:] for key in emb.INDEXES], reads), ([('m', DIMS)], [None]))
            self.assertEqual(self.search(probe, 'plan'), self.every_vector(probe, 'plan'))
        self.assertEqual(reads, [None, []])  # then kept current like any other

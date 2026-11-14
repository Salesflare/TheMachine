"""Long meetings and conversations found by what was said late in them: more vectors per signal, one per passage
(embeddings.passages, passage_pass), and a hit that hands back the part that matched."""
import unittest
from pathlib import Path
from unittest.mock import patch

import search_ask
import test_embeddings as te

a, emb, SETTINGS, event = te.a, te.emb, te.SETTINGS, te.event
ASKED = 'zeppelin hangar lease'


def long_body(late='Ben Sample: the zeppelin hangar lease renewal, the zeppelin hangar lease terms'):
    """About 60,000 characters of a call, a speaker's turn per line; what `late` says comes in its last third only."""
    turns = lambda n, words: [f'Ann Example: {words} point {i} of the agenda' for i in range(n)]
    return '\n'.join(turns(450, 'budget planning for the quarter') + turns(450, 'hiring an engineer and a designer')
                     + [late] * 20 + turns(60, 'closing words and thanks'))


class Passages(unittest.TestCase):
    setUp, ids, vectors, embed_all = te.Embeddings.setUp, te.Embeddings.ids, te.Embeddings.vectors, te.Embeddings.embed_all

    def add(self, source='t1', account='work', kind='meeting.transcript', body=None, title='Weekly call'):
        self.store.commit_page(account, {}, [event(source, title, long_body() if body is None else body, account=account, kind=kind)])
        self.embed_all()
        return self.ids(account, source)

    def split(self, budget=emb.PASSAGE_BATCH):
        passes = 0
        while emb.passage_pass(self.store.connect, SETTINGS, budget)[1]:
            passes += 1
        return passes

    def stored(self, event_id=None):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM event_passages WHERE ?1 IS NULL OR event_id=?1 ORDER BY event_id,seq', (event_id,))]

    def test_what_was_said_late_in_a_long_call_is_found_by_meaning_and_the_hit_reads_that_part(self):
        call = self.add()
        body = ' '.join(long_body().split())
        find = lambda: next(h for h in emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED) if h[0] == call)
        self.assertIsNone(find()[1])  # its words only: the one vector covers the call's start
        self.split()
        hit = find()
        self.assertGreater(hit[1], 0.5)
        self.assertGreater(hit.start, len(body) * 2 // 3)
        self.assertIn(ASKED, emb.passage_text(long_body(), hit.start, hit.chars))
        self.assertEqual(body[hit.start:hit.start + hit.chars], emb.passage_text(long_body(), hit.start, hit.chars))
        # The review's tools: the body from the passage on, with the offset to read around it
        for name, args in (('related', {'query': ASKED}), ('events', {'query': ASKED, 'semantic': True})):
            view = next(e for e in self.app.action(name, {'account_ids': ['work'], **args})['events'] if e['id'] == call)
            self.assertEqual((view['body_offset'], view['body_matched'], view['body_clipped']), (hit.start, True, True), name)
            self.assertTrue(view['body'].startswith(body[hit.start:hit.start + 200]), name)
            self.assertIn(ASKED, view['body'][:hit.chars])
        # ... and read on from anywhere else as before
        view = self.app.action('related', {'account_ids': ['work'], 'query': ASKED, 'body_offset': 100})['events']
        self.assertEqual([e['body_offset'] for e in view if e['id'] == call], [100])
        # A preparation's list says where to read it
        self.store.commit_page('work', {}, [event('9', 'Hangar lease', 'The zeppelin hangar lease is up for renewal')])
        self.embed_all()
        sid = self.store.suggest('lease', 'Renew the hangar lease', 'I can check it.', [self.ids('work', '9')])['id']
        self.assertRegex(self.app.related_lines(sid), rf'- {call} \(work\) [^\n]*Weekly call · matches at body_offset {hit.start}(\n|$)')

    def test_search_reads_the_part_of_a_long_conversation_that_matched(self):
        chat = self.add('c1', kind='intercom.conversation', title='Conversation with Ann')
        self.split()
        rows = self.app.search_ask_rows(ASKED, None)
        found = search_ask.sources(rows)
        self.assertIn(ASKED, next(s['text'] for s in found if s['id'] == chat))
        self.assertTrue(all(len(s['text']) <= search_ask.SOURCE_CHARS for s in found))

    def test_short_signals_stay_exactly_as_they_were(self):
        self.embed_all()
        one = self.ids('work', '1')
        asks = lambda: [emb.related(self.store.connect, SETTINGS, ['work'], [one]), emb.related(self.store.connect, SETTINGS, ['work', 'home'], query='unpaid invoice'),
                        self.app.action('related', {'account_ids': ['work'], 'event_ids': [one]}), self.app.related_lines(self.sid)]
        self.sid = self.store.suggest('invoice', 'Pay the September invoice', 'I can check it.', [one])['id']
        before, vectors, sent = asks(), self.vectors(), self.calls.call_count
        self.assertEqual(before[0], [(self.ids('work', '2'), 0.666)])  # plain pairs, as before
        self.assertEqual(self.split(), 0)
        self.assertEqual(self.calls.call_count - sent, 0)  # looked at, nothing embedded
        self.assertEqual(self.stored(), [])
        self.assertEqual({i: {**v, 'passages': None} for i, v in self.vectors().items()}, vectors)
        self.assertEqual({v['passages'] for v in self.vectors().values()}, {0})
        self.assertEqual(asks(), before)
        self.assertEqual(emb.passages('Plan', 'x ' * 900), [])  # all of it is in the first vector
        # Mail is left to its first vector and its words, however long
        self.add('m1', kind='gmail.message')
        self.split()
        self.assertEqual(self.stored(), [])

    def test_a_signal_shows_once_with_its_best_part(self):
        body = '\n'.join(f'Ben Sample: the zeppelin hangar lease, part {i} of the zeppelin hangar lease talk' for i in range(300))
        call = self.add(body=body, title='Zeppelin hangar lease')
        self.split()
        self.assertGreater(len(self.stored(call)), 5)
        for found in (emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED, limit=20),
                      emb.related(self.store.connect, SETTINGS, ['work'], [self.add('9', kind='gmail.message', body='The zeppelin hangar lease')], limit=20)):
            self.assertEqual([i for i, _ in found].count(call), 1)
        result = self.app.action('related', {'account_ids': ['work'], 'query': ASKED, 'limit': 20})
        self.assertEqual([e['id'] for e in result['events']].count(call), 1)

    def test_a_changed_signal_loses_its_old_passages(self):
        call = self.add()
        self.split()
        self.assertTrue(self.stored(call))
        self.store.commit_page('work', {}, [event('t1', 'Weekly call', 'Moved to next week.', kind='meeting.transcript')])
        # until its new vector is in, the old passages match nothing
        self.assertIsNone(next(h for h in emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED + ' moved week') if h[0] == call)[1])
        self.embed_all()
        self.assertEqual(self.stored(call), [])
        self.split()
        self.assertEqual((self.stored(call), self.vectors()[call]['passages']), ([], 0))
        self.assertEqual([h for h in emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED) if h[0] == call], [])
        # a longer version gets its own
        self.store.commit_page('work', {}, [event('t1', 'Weekly call', long_body('Ben Sample: the lighthouse keeper rota'), kind='meeting.transcript')])
        self.embed_all(); self.split()
        self.assertEqual({p['version'] for p in self.stored(call)}, {3})
        with self.store.connect() as db:
            db.execute('DELETE FROM events WHERE id=?', (call,))
        self.assertEqual(self.stored(call), [])

    def test_the_backfill_stops_at_its_budget_and_goes_on_from_there(self):
        old, new = self.add('t0'), self.add('t1')
        parts = emb.passages('Weekly call', long_body())
        self.assertGreater(len(parts), 30)
        self.assertTrue(all(len(text.encode()) <= emb.PASSAGE_BYTES + emb.PASSAGE_SOFT // 4 + 200 for _, _, text in parts))
        self.assertTrue(all(text.split('| text: ')[1].startswith(('Ann Example:', 'Ben Sample:')) for _, _, text in parts))  # whole turns
        sent = self.calls.call_count
        self.assertEqual(emb.passage_pass(self.store.connect, SETTINGS), (emb.PASSAGE_BATCH, True))
        # small requests: a search's query finds a slot free (emb.BACKGROUND_INPUTS)
        sizes = [len(call.args[1]) for call in self.calls.call_args_list[sent:]]
        self.assertEqual(sum(sizes), emb.PASSAGE_BATCH)
        self.assertLessEqual(max(sizes), emb.BACKGROUND_INPUTS)
        self.assertEqual([(p['event_id'], p['seq']) for p in self.stored()], [(new, n) for n in range(emb.PASSAGE_BATCH)])  # the newest first
        self.assertIsNone(self.vectors()[new]['passages'])
        self.assertEqual(emb.passage_pass(self.store.connect, SETTINGS, 7), (7, True))
        self.assertEqual([p['seq'] for p in self.stored(new)], list(range(emb.PASSAGE_BATCH + 7)))  # on from where it stopped
        self.split(16)
        for call in (old, new):
            self.assertEqual([(p['seq'], p['start'], p['chars']) for p in self.stored(call)], [(n, s, c) for n, (s, c, _) in enumerate(parts)])
            self.assertEqual(self.vectors()[call]['passages'], len(parts))
        self.assertEqual(emb.passage_pass(self.store.connect, SETTINGS), (0, False))
        # The service: only when nothing holds history back, and it rests ten times as long as a pass took
        app_history = a.sys.modules[a.App.history_hold.__module__]
        self.add('t2')
        with patch.object(a.App, 'history_hold', return_value='first_look'), patch.object(emb, 'passage_pass') as held:
            self.assertEqual(self.app.passage_step(SETTINGS), app_history.WAIT_SECONDS)
        held.assert_not_called()
        with patch.object(a.App, 'history_hold', return_value=None):
            self.assertEqual(self.app.passage_step(SETTINGS), app_history.PASSAGE_GAP_SECONDS)
            with patch.object(app_history.time, 'monotonic', side_effect=[100.0, 109.0]):
                self.assertEqual(self.app.passage_step(SETTINGS), 9.0 * app_history.PASSAGE_REST)
            self.split()
            self.assertEqual(self.app.passage_step(SETTINGS), app_history.WAIT_SECONDS)

    def test_a_passage_the_server_refuses_ends_that_split_and_not_the_rest(self):
        bad, good = self.add('t0', body=long_body('Ben Sample: refuse this one')), self.add('t1')
        sent = self.llama(refuse=lambda text: 'refuse this one' in text)
        self.split(8)
        self.assertEqual(self.vectors()[good]['passages'], len(self.stored(good)))
        self.assertLess(self.vectors()[bad]['passages'], len(emb.passages('Weekly call', long_body('Ben Sample: refuse this one'))))
        self.assertTrue(self.stored(bad) and sent)
        self.add('t2')
        self.llama(up=False)
        with self.assertRaises(emb.EmbeddingError):  # the server's failure marks nothing done
            emb.passage_pass(self.store.connect, SETTINGS)
        self.assertIsNone(self.vectors()[self.ids('work', 't2')]['passages'])

    llama = te.Embeddings.llama

    def test_passages_stay_with_their_signal_in_exports_forgetting_and_sharing(self):
        work, home = self.add(), self.add('h1', account='home')
        self.split()
        ids = lambda found: [i for i, _ in found]
        # Search reads the given accounts only: a personal call's passages never answer a Work search
        self.assertIn(work, ids(emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED)))
        self.assertNotIn(home, ids(emb.related(self.store.connect, SETTINGS, ['work'], query=ASKED)))
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['home'], query=ASKED)[0][0], home)
        self.assertNotIn(home, ids(emb.related(self.store.connect, SETTINGS, ['work'], [home])))  # nor as what to look for
        # Like the first vector, they are an index of this Machine's own messages: nothing that shares, publishes or
        # sends reads either table, and an export leaves both out the same way
        root = Path(a.__file__).parent
        for name in ('shared_graph.py', 'shared_graph_app.py', 'shared_graph_kept.py', 'fleet.py', 'graph_publish.py', 'network.py', 'contact_share.py', 'portable.py'):
            source = root.joinpath(name).read_text()
            self.assertNotIn('event_passages', source, name); self.assertNotIn('event_vectors', source, name)
        from machine.export import coverage, inventory
        self.assertEqual(inventory.TABLES['event_passages'], inventory.TABLES['event_vectors'])
        reason = lambda table: next(why for why, tables in coverage.LEFT_OUT.items() if table in tables)
        self.assertEqual(reason('event_passages'), reason('event_vectors'))
        # Forgetting someone drops their messages' passages with the messages
        lee = {'from': 'Lee Parker <lee@globex.example>', 'to': 'sam@acme.example'}
        self.store.commit_page('work', {}, [event('f0', 'Hello', 'Hello from Lee', metadata=lee),
                                            event('f1', 'Call with Lee', long_body(), kind='intercom.conversation', metadata=lee)])
        self.embed_all(); self.split()
        gone = self.ids('work', 'f1')
        self.assertTrue(self.stored(gone))
        config = {'accounts': [{'id': 'work', 'email': 'sam@acme.example'}, {'id': 'home', 'email': 'sam@home.example'}]}
        with self.store.connect() as db:
            db.isolation_level = None
            a.graph.build(db, config, a.now())
        with self.store.connect() as db:
            a.graph.delete_person(db, 'email:lee@globex.example', config, a.now())
            self.assertIsNone(db.execute('SELECT 1 FROM events WHERE id=?', (gone,)).fetchone())
        self.assertEqual(self.stored(gone), [])
        self.assertTrue(self.stored(work))
        # The table holds numbers only: the text stays in the sealed body
        with self.store.connect() as db:
            self.assertEqual({r[1]: r[2] for r in db.execute('PRAGMA table_info(event_passages)')},
                             {'event_id': 'INTEGER', 'seq': 'INTEGER', 'version': 'INTEGER', 'model': 'TEXT', 'dims': 'INTEGER', 'start': 'INTEGER',
                              'chars': 'INTEGER', 'vector': 'BLOB'})

    def test_a_database_from_before_keeps_its_vectors(self):
        self.embed_all()
        with self.store.connect() as db:
            before = [tuple(r) for r in db.execute('SELECT event_id,version,model,dims,vector FROM event_vectors ORDER BY event_id')]
            db.execute('DROP INDEX event_vectors_unsplit'); db.execute('DROP TABLE event_passages')
            db.execute('ALTER TABLE event_vectors DROP COLUMN passages')
        store = a.Store(self.store.path)
        with store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT event_id,version,model,dims,vector FROM event_vectors ORDER BY event_id')], before)
            self.assertEqual(db.execute('SELECT count(*) FROM event_vectors WHERE passages IS NULL').fetchone()[0], len(before))
        self.assertEqual(emb.embed_pending(store.connect, SETTINGS), 0)  # nothing is embedded again
        self.assertEqual(emb.passage_pass(store.connect, SETTINGS), (0, False))


if __name__ == '__main__':
    unittest.main()

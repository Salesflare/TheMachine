import importlib.util
import math
import re
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('embeddings_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
emb = a.embeddings
REAL_REQUEST = emb.request  # the HTTP call; every other test replaces it with fake vectors
SETTINGS = {'url': 'http://127.0.0.1:9', 'model': 'embeddinggemma-300m', 'dims': 256, 'floor': 0.3, 'query_floor': 0.2}
PROMPT_WORDS = {'title', 'text', 'task', 'search', 'result', 'query', 'none'}


def fake_request(settings, texts, timeout=120):
    """Deterministic bag-of-words vectors (768 wide, like the model): shared words mean similar."""
    out = []
    for text in texts:
        vector = [0.0] * 768
        for word in re.findall(r'[a-z]+', text.lower()):
            if word not in PROMPT_WORDS:
                vector[zlib.crc32(word.encode()) % 256] += 1.0  # meaning sits in the leading (Matryoshka) dims
        vector[255] += 0.01
        out.append(vector)
    return out


def event(source_id, title, body, account='work', kind='gmail.message', metadata=None):
    return {'account_id': account, 'source_id': source_id, 'kind': kind, 'occurred_at': a.now(), 'title': title,
            'body': body, 'metadata': metadata or {'from': 'Ann Example <ann@example.com>'}, 'deleted': False}


class Embeddings(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'events.sqlite')
        patcher = patch.object(emb, 'request', side_effect=fake_request); self.calls = patcher.start(); self.addCleanup(patcher.stop)
        self.store.commit_page('work', {}, [
            event('1', 'Invoice overdue', 'The invoice for September is still unpaid, please pay the invoice'),
            event('2', 'Invoice reminder', 'Second reminder: the September invoice is unpaid'),
            event('3', 'Lunch on Friday', 'Shall we grab lunch on Friday near the office?'),
            event('4', 'Team offsite', 'Planning the offsite agenda and the hotel booking')])
        self.store.commit_page('home', {}, [event('5', 'Invoice unpaid', 'Your invoice is unpaid, pay the invoice today', account='home')])
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'work'}, {'id': 'home'}], 'embeddings': SETTINGS}

    def ids(self, account, source):
        with self.store.connect() as db:
            return db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account, source)).fetchone()[0]

    def vectors(self):
        with self.store.connect() as db:
            return {r['event_id']: dict(r) for r in db.execute('SELECT * FROM event_vectors')}

    def embed_all(self):
        while emb.embed_pending(self.store.connect, SETTINGS, 2):
            pass

    def test_document_prompt_drops_quoted_history_and_keeps_the_start(self):
        body = 'New reply text\n> quoted line\n\n[Quoted earlier messages: first 10 of 10 characters kept.]\nOn Mon, Ann wrote: old'
        self.assertEqual(emb.document('Re: Plan', body), 'title: Re: Plan | text: New reply text')
        self.assertEqual(len(emb.document('', 'x' * 5000)), len('title: none | text: ') + emb.BODY_CHARS)

    def test_vectors_are_normalized_versioned_and_cascade_on_delete(self):
        self.embed_all()
        rows = self.vectors(); first = self.ids('work', '1')
        self.assertEqual(len(rows), 5)
        self.assertEqual((rows[first]['version'], rows[first]['dims'], rows[first]['model'], len(rows[first]['vector'])), (1, 256, 'embeddinggemma-300m', 1024))
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in emb.unpack(rows[first]['vector']))), 1.0, places=5)
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS), 0)  # nothing changed, nothing re-embedded
        self.store.commit_page('work', {}, [event('1', 'Invoice overdue', 'Paid now, thanks')])
        with self.store.connect() as db:
            self.assertEqual([r['id'] for r in emb.pending(db, SETTINGS, 10)], [first])
        self.embed_all()
        self.assertEqual(self.vectors()[first]['version'], 2)
        self.assertEqual(emb.embed_pending(self.store.connect, {**SETTINGS, 'dims': 128}, 10), 5)  # another size re-embeds
        with self.store.connect() as db:
            db.execute('DELETE FROM events WHERE id=?', (first,))
        self.assertNotIn(first, self.vectors())

    def test_related_stays_within_accounts_excludes_given_ids_and_respects_floor_and_limit(self):
        self.embed_all()
        one, two, home = self.ids('work', '1'), self.ids('work', '2'), self.ids('home', '5')
        found = emb.related(self.store.connect, SETTINGS, ['work'], [one])
        self.assertEqual(found[0][0], two)
        self.assertNotIn(one, [i for i, _ in found]); self.assertNotIn(home, [i for i, _ in found])
        self.assertTrue(all(s >= 0.3 for _, s in found))
        self.assertEqual(len(emb.related(self.store.connect, SETTINGS, ['work'], [one], limit=1)), 1)
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['work'], [one], floor=0.99), [])
        self.assertNotIn(two, [i for i, _ in emb.related(self.store.connect, SETTINGS, ['work'], [one], exclude=[two])])
        # Another account's event is not a probe either: nothing to compare against.
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['work'], [home]), [])
        with self.assertRaises(ValueError):
            emb.related(self.store.connect, SETTINGS, [], [one])
        result = self.app.action('related', {'account_ids': ['home'], 'query': 'unpaid invoice'})
        self.assertEqual({e['account_id'] for e in result['events']}, {'home'})
        with self.assertRaises(ValueError):  # unconfigured accounts are refused like events
            self.app.action('related', {'account_ids': ['elsewhere'], 'query': 'invoice'})

    def test_related_action_returns_the_events_shape_with_similarity(self):
        self.embed_all()
        one = self.ids('work', '1')
        result = self.app.action('related', {'account_ids': ['work'], 'event_ids': [one], 'limit': 50})
        self.assertTrue(result['semantic'])
        top = result['events'][0]
        self.assertEqual((top['id'], top['title']), (self.ids('work', '2'), 'Invoice reminder'))
        self.assertIn('body', top); self.assertGreater(top['similarity'], 0.3)
        self.assertNotIn(one, [e['id'] for e in result['events']])
        with self.assertRaises(ValueError):
            self.app.action('related', {'account_ids': ['work']})

    def test_changed_candidate_is_not_ranked_with_its_old_vector(self):
        self.embed_all()
        seed, candidate = self.ids('work', '1'), self.ids('work', '2')
        self.assertIn(candidate, [i for i, _ in emb.related(self.store.connect, SETTINGS, ['work'], [seed])])
        self.store.commit_page('work', {}, [event('2', 'Garden weekend', 'Plant tulips roses daffodils outdoors')])
        self.assertNotIn(candidate, [i for i, _ in emb.related(self.store.connect, SETTINGS, ['work'], [seed])])

    def test_changed_seed_is_embedded_before_matching(self):
        self.store.commit_page('work', {}, [event('garden', 'Garden weekend', 'Plant tulips roses daffodils outdoors')])
        self.embed_all()
        seed, garden = self.ids('work', '1'), self.ids('work', 'garden')
        self.store.commit_page('work', {}, [event('1', 'Garden plan', 'Plant tulips roses daffodils outdoors')])
        before = self.calls.call_count
        found = emb.related(self.store.connect, SETTINGS, ['work'], [seed])
        self.assertEqual(found[0][0], garden)
        self.assertEqual(self.calls.call_count, before + 1)
        self.assertEqual(self.vectors()[seed]['version'], 2)

    def test_old_embedding_completion_cannot_replace_a_newer_vector(self):
        self.embed_all()
        seed = self.ids('work', '1')
        with self.store.connect() as db:
            old = dict(db.execute('SELECT id,version,title,body FROM events WHERE id=?', (seed,)).fetchone())
        old_vector = emb.unpack(self.vectors()[seed]['vector'])
        self.store.commit_page('work', {}, [event('1', 'Garden plan', 'Plant tulips roses daffodils outdoors')])
        self.embed_all()
        current = self.vectors()[seed]
        with self.store.connect() as db:
            emb.save(db, SETTINGS, [old], [old_vector])
        self.assertEqual(self.vectors()[seed], current)

    def test_seed_changed_during_embedding_is_not_used_or_saved(self):
        self.embed_all()
        seed = self.ids('work', '1')
        self.store.commit_page('work', {}, [event('1', 'Invoice overdue', 'Please pay the invoice')])
        def request(settings, texts, timeout=120):
            self.store.commit_page('work', {}, [event('1', 'Garden plan', 'Plant tulips roses daffodils outdoors')])
            return fake_request(settings, texts, timeout)
        self.calls.side_effect = request
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['work'], [seed]), [])
        self.assertEqual(self.vectors()[seed]['version'], 1)

    def test_deleted_seed_does_not_trigger_embedding_or_matching(self):
        self.embed_all()
        seed = self.ids('work', '1')
        with self.store.connect() as db:
            db.execute('UPDATE events SET deleted=1 WHERE id=?', (seed,))
        before = self.calls.call_count
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['work'], [seed]), [])
        self.assertEqual(self.calls.call_count, before)

    def test_hybrid_fuses_keyword_and_meaning(self):
        self.embed_all()
        offsite, lunch = self.ids('work', '4'), self.ids('work', '3')
        # Nothing clears the floor by meaning: keyword matches still come back, without a score.
        self.assertEqual(emb.related(self.store.connect, SETTINGS, ['work'], query='hotel', floor=0.99, query_floor=0.99), [(offsite, None)])
        # A query is held to its own (lower) floor: query-to-message cosines run lower than message-to-message.
        by_query = emb.related(self.store.connect, SETTINGS, ['work'], query='unpaid invoice', floor=0.99)
        self.assertTrue(by_query and all(s is not None and s >= 0.2 for _, s in by_query[:2]))
        found = emb.related(self.store.connect, SETTINGS, ['work'], query='friday lunch offsite', floor=0.1)
        self.assertEqual({i for i, _ in found[:2]}, {offsite, lunch})
        # events with semantic:true finds what the strict all-words keyword search misses.
        plain = self.app.action('events', {'account_ids': ['work'], 'query': 'unpaid bills invoice'})
        semantic = self.app.action('events', {'account_ids': ['work'], 'query': 'unpaid bills invoice', 'semantic': True})
        self.assertEqual(plain['events'], [])
        self.assertEqual({e['title'] for e in semantic['events'][:2]}, {'Invoice overdue', 'Invoice reminder'})
        self.assertEqual({e['account_id'] for e in semantic['events']}, {'work'})
        # ["all"] searches every configured account, by meaning and keywords; begin_analysis still needs explicit accounts.
        everything = self.app.action('events', {'account_ids': ['all'], 'query': 'unpaid bills invoice', 'semantic': True})
        self.assertEqual({e['account_id'] for e in everything['events']}, {'work', 'home'})
        self.assertIn('Invoice unpaid', {e['title'] for e in everything['events'][:3]})
        self.assertEqual({e['account_id'] for e in self.app.action('related', {'account_ids': 'all', 'query': 'invoice'})['events']}, {'work', 'home'})
        with self.assertRaises(ValueError):
            self.app.action('begin_analysis', {'account_ids': ['all']})

    def test_server_down_falls_back_to_keywords_and_the_worker_retries_later(self):
        self.calls.side_effect = emb.EmbeddingError('unreachable')
        with self.assertLogs(a.LOG, 'ERROR') as logs:
            result = self.app.action('related', {'account_ids': ['work'], 'query': 'invoice'})
        self.assertFalse(result['semantic']); self.assertEqual(len(result['events']), 2)
        self.assertIn('related error=unreachable', logs.output[0])
        self.app.stop = type('Stop', (), {'n': 0, 'wait': lambda s, t: (setattr(s, 'n', s.n + 1), s.n > 1)[1]})()
        with self.assertLogs(a.LOG, 'ERROR') as logs:
            self.app.embedding_worker()
        self.assertEqual([line.split(':', 2)[2] for line in logs.output], ['embeddings error=unreachable'])  # redacted class only
        self.assertEqual(self.vectors(), {})

    def test_a_server_serving_another_model_is_refused(self):
        import io, json
        def urlopen(request, timeout=0):
            url = request if isinstance(request, str) else request.full_url
            reply = {'data': [{'id': 'other-model'}]} if url.endswith('/models') else {'data': [{'index': 0, 'embedding': [1.0] * 768}]}
            return io.BytesIO(json.dumps(reply).encode())
        emb.SERVED.clear()
        with patch.object(emb.urllib.request, 'urlopen', side_effect=urlopen), patch.object(emb, 'request', REAL_REQUEST):
            with self.assertRaises(emb.EmbeddingError) as error:
                emb.embed(SETTINGS, ['x'])
            self.assertEqual(str(error.exception), 'model_mismatch')
            emb.SERVED.clear()
            self.assertEqual(len(emb.embed({**SETTINGS, 'model': 'other-model'}, ['x'])[0]), 256)
        emb.SERVED.clear()

    def test_feature_off_without_config(self):
        for config in ({'accounts': [{'id': 'work'}]}, {'accounts': [{'id': 'work'}], 'embeddings': {**SETTINGS, 'enabled': False}}):
            self.app.config = config
            with self.assertRaises(ValueError):
                self.app.action('related', {'account_ids': ['work'], 'query': 'invoice'})
            semantic = self.app.action('events', {'account_ids': ['work'], 'query': 'invoice unpaid', 'semantic': True})
            plain = self.app.action('events', {'account_ids': ['work'], 'query': 'invoice unpaid'})
            self.assertEqual(semantic, plain)
        self.calls.assert_not_called()

    def test_example_config_ships_the_feature_off(self):
        import json
        example = json.loads(Path(__file__).parent.parent.joinpath('config.example.json').read_text())
        self.assertIsNone(emb.settings(example))  # the installer copies new example keys into existing configs
        self.assertEqual(emb.settings({**example, 'embeddings': {**example['embeddings'], 'enabled': True}})['dims'], 256)
        self.assertEqual(emb.settings({'embeddings': SETTINGS}), SETTINGS)  # no `enabled` key: on
        self.assertIsNone(emb.settings({'embeddings': {}}))

    def test_preparation_lists_related_signals_only_when_on(self):
        one = self.ids('work', '1')
        sid = self.store.suggest('invoice', 'Pay the September invoice', 'I can check it.', [one])['id']
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET status='sent',message_id='100' WHERE suggestion_id=?", (sid,))
        self.app.config = {'accounts': [{'id': 'work'}]}
        self.store.decide(sid, 'accept', '', 'click-1', 'telegram')
        calls = []; self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        self.assertNotIn('Possibly related', next(c['message'] for c in calls if c.get('message')))
        self.calls.assert_not_called()
        with self.store.connect() as db:
            db.execute('DELETE FROM preparation_runs'); db.execute('DELETE FROM preparations')
        self.app.config = {'accounts': [{'id': 'work'}, {'id': 'home'}], 'embeddings': SETTINGS}
        self.embed_all()
        self.store.decide(sid, 'accept', '', 'click-2', 'telegram')
        calls = []; self.app.preparation_step(lambda r: calls.append(r) or {'status': 'admitted'})
        message = next(c['message'] for c in calls if c.get('message'))
        related = message.split('Possibly related', 1)[1]
        self.assertIn(f"- {self.ids('work', '2')} (work) email from Ann Example", related)
        self.assertIn('Invoice reminder', related)
        self.assertNotIn(f'- {one} ', related); self.assertNotIn(f"- {self.ids('home', '5')} ", related)


    def llama(self, refuse=lambda text: False, up=True):
        """urlopen like llama-server (-ub 2048): HTTP 500 for the whole request when one input has more tokens
        than that (tokens counted as UTF-8 bytes, the worst case), or when `refuse` says so."""
        import io, json
        sent = []
        def urlopen(request, timeout=0):
            url = request if isinstance(request, str) else request.full_url
            if url.endswith('/models'):
                return io.BytesIO(json.dumps({'data': [{'id': SETTINGS['model']}]}).encode())
            texts = json.loads(request.data)['input']
            sent.append(texts)
            if not up or any(len(t.encode()) > 2048 or refuse(t) for t in texts):
                raise emb.urllib.error.HTTPError(url, 500, 'input is too large to process', {}, io.BytesIO())
            return io.BytesIO(json.dumps({'data': [{'index': i, 'embedding': v} for i, v in enumerate(fake_request(SETTINGS, texts))]}).encode())
        emb.SERVED.clear(); self.addCleanup(emb.SERVED.clear)
        for patcher in (patch.object(emb.urllib.request, 'urlopen', side_effect=urlopen), patch.object(emb, 'request', REAL_REQUEST)):
            patcher.start(); self.addCleanup(patcher.stop)
        return sent

    def test_one_long_message_no_longer_blocks_the_batch(self):
        # Seen live: a mail with ~1,600 invisible tag characters and 2,000 characters of non-Latin text came to
        # 5,374 tokens; llama-server refused the whole batch with HTTP 500, every five minutes, so nothing new got a vector.
        hidden = '\U000e0041\u200b' * 800 + '漢字のテキスト' * 400
        self.store.commit_page('work', {}, [event('6', 'Newsletter', hidden), event('7', 'Invoice paid', 'The invoice is paid')])
        sent = self.llama()
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 7)
        self.assertEqual(len(self.vectors()), 7)
        self.assertTrue(all(len(t.encode()) <= 2048 - emb.SPECIAL_TOKENS for batch in sent for t in batch))
        self.assertNotIn('\u200b', ''.join(sent[0]))  # invisible characters are dropped, not embedded
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 0)

    def test_an_input_the_server_still_refuses_is_set_aside_and_the_rest_embedded(self):
        self.store.commit_page('work', {}, [event('6', 'Poison', 'this one breaks the server'), event('7', 'Invoice paid', 'The invoice is paid')])
        sent = self.llama(refuse=lambda text: 'breaks the server' in text)
        with self.assertNoLogs(a.LOG, 'ERROR'):
            self.app.stop = type('Stop', (), {'n': 0, 'wait': lambda s, t: (setattr(s, 'n', s.n + 1), s.n > 1)[1]})()
            self.app.embedding_worker()
        poison = self.ids('work', '6')
        self.assertEqual(set(self.vectors()), {self.ids('work', s) for s in '12347'} | {self.ids('home', '5')})
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT event_id,version,model,reason FROM event_vector_skips')], [(poison, 1, 'embeddinggemma-300m', 'http_500')])
        sent.clear()
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 0)
        self.assertEqual(sent, [])  # not sent again every pass
        with patch.object(emb.time, 'time', return_value=emb.time.time() + emb.SKIP_SECONDS + 1), self.store.connect() as db:
            self.assertEqual([r['id'] for r in emb.pending(db, SETTINGS, 10)], [poison])  # tried again a day later
        self.store.commit_page('work', {}, [event('6', 'Poison', 'fixed now')])
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 1)  # a new version is tried again
        self.assertIn(poison, self.vectors())

    def test_a_lone_refused_input_is_set_aside_when_the_server_works(self):
        self.embed_all()
        self.store.commit_page('work', {}, [event('6', 'Poison', 'this one breaks the server')])
        self.llama(refuse=lambda text: 'breaks the server' in text)
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 1)
        self.assertEqual(emb.embed_pending(self.store.connect, SETTINGS, 16), 0)

    def test_a_failing_server_sets_nothing_aside(self):
        self.llama(up=False)
        with self.assertRaises(emb.EmbeddingError) as error:
            emb.embed_pending(self.store.connect, SETTINGS, 16)
        self.assertEqual(str(error.exception), 'http_500')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM event_vector_skips').fetchone()[0], 0)
            self.assertEqual(len(emb.pending(db, SETTINGS, 16)), 5)
        for code in ('unreachable', 'timeout', 'model_mismatch', 'http_401', 'http_429'):
            self.assertFalse(emb.refused(emb.EmbeddingError(code)))

    def test_requests_stay_within_the_provider_limits(self):
        self.assertEqual(emb.limits(SETTINGS), (2048, 8192, 64, 1.0))
        self.assertEqual(emb.limits({**SETTINGS, 'url': 'https://api.openai.com/v1'}), (8191, 300000, 2048, 1.0))
        custom = {**SETTINGS, 'max_input_tokens': 512, 'max_batch_tokens': 1024, 'bytes_per_token': 2}
        self.assertEqual(emb.limits(custom), (512, 1024, 64, 2.0))
        self.assertEqual(len(emb.fit('é' * 2000, 512, 2.0).encode()), (512 - emb.SPECIAL_TOKENS) * 2)  # never half a character
        groups = list(emb.batches(['x' * 3000] * 10, SETTINGS))
        self.assertEqual([len(g) for g in groups], [4, 4, 2])  # 2,048 tokens each at most, 8,192 a request
        self.assertTrue(all(sum(emb.tokens(t) for t in g) <= 8192 for g in groups))
        self.assertEqual([len(g) for g in emb.batches(['x'] * 100, SETTINGS)], [64, 36])
        sent = self.llama()
        self.assertEqual(len(emb.embed(SETTINGS, ['y ' * 3000] * 10)), 10)
        self.assertEqual([len(batch) for batch in sent], [4, 4, 2])

if __name__ == '__main__':
    unittest.main()

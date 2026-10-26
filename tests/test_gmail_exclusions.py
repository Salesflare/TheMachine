import base64
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
assistant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assistant)
WORK = {'id': 'work-gmail', 'email': 'owner@example.com', 'excluded_terms': ['zq7wx']}


def raw(source='warmup', plain='ordinary', markup='', subject='Hello', snippet=''):
    parts = [{'mimeType': mime, 'body': {'data': base64.urlsafe_b64encode(value.encode()).decode()}}
             for mime, value in [('text/plain', plain), ('text/html', markup)]]
    return {'id': source, 'internalDate': '1791540000000', 'snippet': snippet,
            'payload': {'headers': [{'name': 'Subject', 'value': subject}], 'parts': parts}}


class GmailExclusions(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'
        self.store = assistant.Store(self.path)

    def test_full_mime_alternatives_headers_snippet_case_and_substring(self):
        for message in [raw(plain='x' * 41000 + 'prefixZQ7WXsuffix'),
                        raw(markup='<a href="https://example.test/zq7wx">link</a>'),
                        raw(markup='zq7w&#120;'), raw(subject='prefixzq7wxsuffix'),
                        raw(snippet='zq7wx')]:
            with self.subTest(message=message['id']):
                self.assertIsNone(assistant.message_event(WORK, message))
        self.assertIsNotNone(assistant.message_event(WORK, raw(plain='zq7wy')))
        work2 = {'id': 'work2-gmail', 'email': 'owner@example.org'}
        self.assertIsNotNone(assistant.message_event(work2, raw(plain='zq7wx')))

    def test_purge_preserves_other_account_checkpoint_reviews_and_search(self):
        unfiltered = {**WORK, 'excluded_terms': []}
        good = assistant.message_event(unfiltered, raw(source='good', plain='Keep this real message'))
        warmup = assistant.message_event(unfiltered, raw(plain='zq7wx uniquejunkword'))
        self.store.commit_page(WORK['id'], {'history_id': 'saved'}, [good, warmup])
        other = {**warmup, 'account_id': 'work2-gmail'}
        self.store.commit_page(other['account_id'], {'history_id': 'other'}, [other])
        review = self.store.begin_analysis([WORK['id']])
        warmup_id = next(e['id'] for e in review['events'] if e['source_id'] == 'warmup')
        with self.store.connect() as db:
            before = dict(db.execute('SELECT * FROM checkpoints WHERE account_id=?', (WORK['id'],)).fetchone())
        self.assertEqual(self.store.purge_gmail_exclusions(WORK), {'removed': 1})
        self.assertEqual(self.store.purge_gmail_exclusions(WORK), {'removed': 0})
        self.assertEqual(self.store.events([WORK['id']], query='uniquejunkword'), [])
        self.assertEqual(len(self.store.events(['work2-gmail'], query='uniquejunkword')), 1)
        with self.store.connect() as db:
            self.assertEqual(dict(db.execute('SELECT * FROM checkpoints WHERE account_id=?', (WORK['id'],)).fetchone()), before)
            items = json.loads(db.execute('SELECT items FROM analyses WHERE id=?', (review['analysis_id'],)).fetchone()[0])
            self.assertTrue(next(i for i in items if i['id'] == warmup_id)['excluded'])
            db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")
        self.store.finish_analysis(review['analysis_id'], 'Retained real evidence; warmup removed')
        self.assertEqual(self.store.events([WORK['id']], pending=True), [])

    def test_bootstrap_and_history_exclusions_advance_atomically(self):
        class FakeGmail:
            def __init__(self, config, account): pass
            def profile(self): return {'historyId': '20'}
            def get(self, route, params):
                if route == 'messages': return {'messages': [{'id': 'warmup'}]}
                if route == 'history':
                    return {'historyId': '30', 'history': [{'messagesAdded': [{'message': {'id': 'warmup'}}]}]}
                return raw(plain='zq7wx')
        with patch.object(assistant, 'Gmail', FakeGmail):
            first = assistant.sync_gmail(self.store, {}, WORK)
            self.assertEqual(first['filtered'], 1)
            self.assertEqual(self.store.checkpoint(WORK['id'])['history_id'], '20')
            unfiltered = {**WORK, 'excluded_terms': []}
            old = assistant.message_event(unfiltered, raw(plain='zq7wx'))
            self.store.commit_page(WORK['id'], self.store.checkpoint(WORK['id']), [old])
            second = assistant.sync_gmail(self.store, {}, WORK)
            self.assertEqual(second['filtered'], 1)
            self.assertEqual(self.store.checkpoint(WORK['id'])['history_id'], '30')
            self.assertEqual(self.store.events([WORK['id']]), [])
        self.store.commit_page(WORK['id'], {'history_id': '30'}, [old])
        bad = dict(old, source_id='bad'); del bad['title']
        with self.assertRaises(KeyError):
            self.store.commit_page(WORK['id'], {'history_id': '31'}, [bad], excluded_source_ids=['warmup'])
        self.assertEqual(len(self.store.events([WORK['id']])), 1)
        self.assertEqual(self.store.checkpoint(WORK['id'])['history_id'], '30')

    def test_legacy_migration_preserves_fts_and_never_reuses_removed_ids(self):
        # Reconstruct the pre-filter schema, including externally derived FTS.
        with self.store.connect() as db:
            for trigger in ['search_insert', 'search_update', 'search_delete']:
                db.execute('DROP TRIGGER ' + trigger)
            schema = db.execute("SELECT sql FROM sqlite_master WHERE name='events'").fetchone()[0]
            db.execute(schema.replace('"events"', 'events_legacy').replace('CREATE TABLE events(', 'CREATE TABLE events_legacy(').replace(' AUTOINCREMENT', ''))
            db.execute('DROP TABLE events')
            db.execute('ALTER TABLE events_legacy RENAME TO events')
            sample = assistant.message_event({**WORK, 'excluded_terms': []}, raw(plain='zq7wx'))
            db.execute('INSERT INTO events(id,account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (42, WORK['id'], sample['source_id'], sample['kind'], sample['occurred_at'],
                        sample['title'], sample['body'], '{}', 0, 'hash', 1, 0, assistant.now()))
            db.execute('INSERT INTO event_search(rowid,title,body) VALUES(42,?,?)', (sample['title'], sample['body']))
        legacy = assistant.Store(self.path)
        old_id = legacy.events([WORK['id']])[0]['id']
        self.assertEqual(old_id, 42)
        self.assertEqual(len(legacy.events([WORK['id']], query='zq7wx')), 1)
        legacy.purge_gmail_exclusions(WORK)
        reopened = assistant.Store(self.path)
        reopened.commit_page(WORK['id'], {}, [assistant.message_event(WORK, raw(source='real', plain='realcontext'))])
        self.assertGreater(reopened.events([WORK['id']])[0]['id'], old_id)
        self.assertEqual(len(reopened.events([WORK['id']], query='realcontext')), 1)
        with reopened.connect() as db:
            db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")


if __name__ == '__main__':
    unittest.main()

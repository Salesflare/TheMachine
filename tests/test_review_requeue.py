"""Once, after the update (machine/store/review_requeue.py): before release-20261107-1942 a review whose to-do saves
failed ("That didn't go through", a left-out dedupe_key) still marked its messages reviewed, or set them aside after two
tries, so their to-dos were never made. A test persona lost its accountant's receipts request that way. The agent's own
transcripts show those failed saves; their messages that are in no to-do go back to the review once."""
import datetime as dt
import importlib.util
import json
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from seams import patch_everywhere  # noqa: E402,F401
from machine.store import review_requeue, review_saves  # noqa: E402

spec = importlib.util.spec_from_file_location('review_requeue_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

NOW = dt.datetime(2026, 11, 8, 12, tzinfo=dt.timezone.utc)
FAILED = {'status': 'failed', 'code': 'internal_error', 'error': "Error: That didn't go through. Reload the page and try again."}


def mail(source_id, days_ago):
    return {'account_id': 'work', 'source_id': source_id, 'kind': 'gmail.message', 'title': 'Receipts for the VAT return',
            'occurred_at': (NOW - dt.timedelta(days=days_ago)).isoformat(), 'body': 'Could you send the receipts?', 'deleted': False,
            'metadata': {'from': 'Accountant <books@example.com>', 'thread_id': source_id, 'labels': ['INBOX']}}


def packed(text):
    try:
        from compression import zstd
    except ImportError:
        return None
    return zstd.compress(text.encode())


class Transcript:
    """An agent transcript as OpenClaw keeps it: events in JSON, older ones packed with zstd."""
    def __init__(self, path):
        self.path, self.seq = path, 0
        path.parent.mkdir(parents=True)
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE transcript_events(session_id TEXT, seq INTEGER, event_json TEXT, created_at INTEGER, event_zstd BLOB)')

    def add(self, message, at, pack=False):
        self.seq += 1
        text = json.dumps({'type': 'message', 'id': f'e{self.seq}', 'message': message})
        blob = packed(text) if pack else None
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('INSERT INTO transcript_events VALUES(?,?,?,?,?)',
                       ('s1', self.seq, None if blob else text, int(at.timestamp() * 1000), blob))

    def call(self, code, result, at, pack=False):
        call_id = f'call_{self.seq}'
        self.add({'role': 'assistant', 'content': [{'type': 'toolCall', 'id': call_id, 'name': 'exec', 'arguments': {'code': code}}]}, at, pack)
        self.add({'role': 'toolResult', 'toolCallId': call_id, 'toolName': 'exec', 'content': [{'type': 'text', 'text': json.dumps(result)}],
                  'details': {'status': result['status']}}, at, pack)


def suggest(ids, title='Send the receipts'):
    return f"json(await assistant_signals({{action:'suggest',args:{{event_ids:{json.dumps(ids)},title:'{title}',body:'They asked.'}}}}));"


class RequeueFailedSaves(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.store = a.Store(self.dir / 'events.sqlite')
        # 1 reviewed, 2 set aside, 3 in a to-do, 4 too old, 5 saved fine, 6 "read what came after first", 7 a later failure
        self.store.commit_page('work', {}, [mail('m1', 2), mail('m2', 2), mail('m3', 2), mail('m4', 20), mail('m5', 2), mail('m6', 2), mail('m7', 1)])
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version')
            db.execute('UPDATE events SET analyzed_version=0,deferrals=2 WHERE id=2')
        self.store.suggest('k3', 'Pay the invoice', 'It is due.', [3], 'digest', '08:30')
        with self.store.connect() as db:
            review_saves.ensure(db)
            db.execute("INSERT INTO review_save_failures(event_id,failed_at,error,tries) VALUES(7,?, 'KeyError', 3)", (NOW.isoformat(),))
        self.transcript = Transcript(self.dir / 'agent' / 'openclaw-agent.sqlite')
        nov7 = dt.datetime(2026, 11, 7, 9, tzinfo=dt.timezone.utc)
        self.transcript.call(suggest([1, 2]), FAILED, nov7, pack=True)  # as the persona's review: kept packed by now
        self.transcript.call(suggest([3]) + " json(await assistant_signals({action:'promise',args:{event_id:9}}));", FAILED, nov7)
        self.transcript.call(suggest([4]), FAILED, nov7)
        self.transcript.call(suggest([5]), {'status': 'completed', 'value': {}}, nov7)
        self.transcript.call(suggest([6]), {'status': 'failed', 'error': 'Error: Something happened after this to-do\'s evidence.'}, nov7)
        self.transcript.call(suggest([7]), FAILED, nov7)
        self.transcript.call(suggest([2]), FAILED, dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc))  # before the window: not read

    def state(self, event_id):
        with self.store.connect() as db:
            return tuple(db.execute('SELECT analyzed_version<version, deferrals FROM events WHERE id=?', (event_id,)).fetchone())

    def test_messages_of_failed_saves_with_no_to_do_go_back_to_the_review_once(self):
        self.assertEqual(review_requeue.requeue(self.store, self.transcript.path, now=NOW), 2)
        self.assertEqual(self.state(1), (1, 0))  # was reviewed: pending again
        self.assertEqual(self.state(2), (1, 0))  # was set aside: pending, no deferrals
        for left in (3, 4, 5, 6, 7):  # in a to-do, too old, saved, a step of the review, held by the fix itself
            self.assertEqual(self.state(left)[0], 0, left)
        claim = self.store.begin_analysis(['work'], 40)  # the next review gets them
        self.assertEqual(sorted(e['id'] for e in claim['events']), [1, 2])
        copies = list(self.dir.glob('events.sqlite.before-failed-saves-requeue-*Z'))
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].stat().st_mode & 0o777, 0o600)
        with closing(sqlite3.connect(copies[0])) as copy:  # the copy is from before
            self.assertEqual(copy.execute('SELECT analyzed_version>=version FROM events WHERE id=1').fetchone()[0], 1)
        self.assertIn(copies[0], __import__('retention').backup_copies(self.temp.name, [self.dir / 'events.sqlite']))
        # once only: the next start changes nothing, and no second copy
        self.assertEqual(review_requeue.requeue(self.store, self.transcript.path, now=NOW), 0)
        self.assertEqual(len(list(self.dir.glob('events.sqlite.before-*'))), 1)

    def test_a_message_that_has_its_to_do_by_now_stays_reviewed(self):
        self.store.suggest('k1', 'Send the receipts', 'They asked.', [1], 'digest', '08:30')  # a later review made it
        self.assertEqual(review_requeue.requeue(self.store, self.transcript.path, now=NOW), 1)
        self.assertEqual(self.state(1), (0, 0))
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM suggestions').fetchone()[0], 2)

    def test_without_transcripts_it_is_done_with_nothing_to_send_back(self):
        self.assertEqual(review_requeue.requeue(self.store, self.dir / 'none.sqlite', now=NOW), 0)
        self.assertEqual(list(self.dir.glob('events.sqlite.before-*')), [])
        with self.store.connect() as db:
            self.assertTrue(db.execute('SELECT 1 FROM store_fixes WHERE name=?', (review_requeue.NAME,)).fetchone())

    def test_suggest_calls_are_read_from_the_exec_code(self):
        code = suggest([4, 8]) + " await assistant_signals({action:'suggest_save',args:{event_ids:[1]}}); await assistant_signals({action:'events',args:{event_ids:[2]}});"
        self.assertEqual(review_requeue.suggested_ids({'code': code}), [4, 8])
        self.assertEqual(review_requeue.suggested_ids({'action': 'suggest', 'args': {'event_ids': [5]}}), [5])
        self.assertEqual(review_requeue.suggested_ids({'code': "await assistant_signals({action:'finish_analysis',args:{reviewed_ids:[1]}})"}), [])

    def test_packed_events_open_with_node_on_older_pythons(self):
        node = shutil.which('node')
        if not node or subprocess.run([node, '-e', "process.exit(require('zlib').zstdDecompressSync?0:1)"]).returncode:
            self.skipTest('needs a node with zstd (22.15 or later)')
        blob = subprocess.run([node, '-e', "process.stdout.write(require('zlib').zstdCompressSync(Buffer.from('{\"a\": 1}')))"],
                              capture_output=True, check=True).stdout
        real = __import__('builtins').__import__

        def no_compression(name, *args, **kwargs):
            if name == 'compression':
                raise ImportError(name)
            return real(name, *args, **kwargs)
        from unittest.mock import patch
        with patch('builtins.__import__', no_compression):
            self.assertEqual(review_requeue.unpack([blob], node), ['{"a": 1}'])


if __name__ == '__main__':
    unittest.main()

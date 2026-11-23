"""Message contents sealed at rest (message_seal.py): every source's text is unreadable without the owner's key, the
app reads, searches and exports as before, and support's learnings export never holds it."""
import base64
import contextlib
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import unittest.mock

ROOT = Path(__file__).resolve().parent.parent
import learnings
import message_seal
import moving
import plain_columns
from machine.store import review_whys
from seams import patch_everywhere  # noqa: E402
import datetime as dt
import machine.app.status as machine_app_status
import machine.config as machine_config
import machine.faults as machine_faults
import machine.main as machine_main
import machine.store.events as machine_events
import machine.text as machine_text

CANARY = 'Zanzibarquill'  # in every message's text; never in a sealed database's files
# Two team learnings as a pass may keep them: general, one sentence, no capitalized word mid-sentence
LEARNED = f'Refund requests are answered from the support inbox with the {CANARY.lower()} template.'
LEARNED_TOO = f'Renewal quotes are made in the {CANARY.lower()} billing tool before a call.'
SOURCES = ['gmail.message', 'outlook.message', 'imap.message', 'slack.message', 'whatsapp.message', 'telegram.message',
           'signal.message', 'linkedin.message', 'x.dm', 'teams.message', 'sms.message', 'android.notification',
           'intercom.conversation', 'github.comment', 'zoom.transcript', 'calendar.event', 'brand_new_connector.thing']


def event(i, kind, extra=None):
    return {'account_id': 'acct', 'source_id': f'{kind}:{i}', 'kind': kind, 'occurred_at': f'2026-10-{10 + i % 9:02d}T09:00:00+00:00',
            'title': f'{CANARY} subject {i}', 'body': f'Dear owner, the {CANARY} contract is ready. Óscar will sign on Friday {i}.',
            'deleted': False, 'metadata': {'thread_id': f't{i}', 'from': 'Pat <pat@example.com>', 'labels': ['INBOX'],
                                            'snippet': f'{CANARY} preview', 'attachments': [f'{CANARY}.pdf'],
                                            'a_key_no_one_reviewed_yet': f'{CANARY} quoted text', **(extra or {})}}


def files(path):
    return b''.join(p.read_bytes() for p in Path(path).parent.glob(Path(path).name + '*'))


# The first look's old summary (removed) kept what the owner left off it here; Machines that used it still have the table
LEARNED_FIXES = 'CREATE TABLE IF NOT EXISTS learned_fixes(key TEXT PRIMARY KEY,state TEXT NOT NULL,text TEXT,at TEXT NOT NULL)'


class Sealer(unittest.TestCase):
    def setUp(self):
        self.sealer = message_seal.Sealer(os.urandom(32))

    def test_round_trip_and_fresh_nonce(self):
        for text in ['a', 'Grüße 👋\n' * 500, CANARY]:
            sealed = self.sealer.seal(text)
            self.assertTrue(message_seal.is_sealed(sealed))
            if len(text) > 4:  # one letter turns up among random bytes by chance
                self.assertNotIn(text.encode(), sealed)
            self.assertEqual(self.sealer.open(sealed), text)
        self.assertNotEqual(self.sealer.seal('same'), self.sealer.seal('same'))
        for value in [None, '', 3, b'\x00plain blob']:
            self.assertEqual(self.sealer.seal(value), value)
            self.assertEqual(self.sealer.open(value), value)

    def test_tampering_and_another_key_fail_loudly(self):
        sealed = bytearray(self.sealer.seal('pay the invoice'))
        sealed[-20] ^= 1
        with self.assertRaises(message_seal.SealError):
            self.sealer.open(bytes(sealed))
        with self.assertRaises(message_seal.SealError):
            message_seal.Sealer(os.urandom(32)).open(self.sealer.seal('pay the invoice'))

    def test_a_small_value_read_again_opens_once_a_damaged_one_fails_each_time(self):
        """Each status poll reads the same rows again: a small value or JSON opened once is kept for this key; a long one
        (a body) is opened each time, and a damaged one never opens."""
        small, big = self.sealer.seal('pay the invoice'), self.sealer.seal('x' * (message_seal.KEEP_OPENED[0] + 1))
        meta = self.sealer.seal_json(json.dumps({'thread_id': 't1', 'snippet': CANARY}))
        damaged = bytearray(self.sealer.seal('pay the invoice'))
        damaged[-20] ^= 1
        with unittest.mock.patch.object(self.sealer, '_stream', wraps=self.sealer._stream) as stream:
            for _ in range(3):
                self.assertEqual(self.sealer.open_any(small), 'pay the invoice')
                self.assertEqual(json.loads(self.sealer.open_any(meta)), {'thread_id': 't1', 'snippet': CANARY})
                self.assertEqual(len(self.sealer.open_any(big)), message_seal.KEEP_OPENED[0] + 1)
                with self.assertRaises(message_seal.SealError):
                    self.sealer.open_any(bytes(damaged))
            self.assertEqual(stream.call_count, 1 + 1 + 3)
        with self.assertRaises(message_seal.SealError):  # kept per key: another key still can't open it
            message_seal.Sealer(os.urandom(32)).open(small)

    def test_text_the_gateway_plugin_seals_opens_here_and_fails_loudly_otherwise(self):
        sealed = self.sealer.seal_inbox(CANARY + ' Grüße 👋')
        self.assertTrue(sealed.startswith(message_seal.INBOX))
        self.assertNotIn(CANARY, sealed)
        self.assertEqual(message_seal.open_inbox(self.sealer, sealed), CANARY + ' Grüße 👋')
        self.assertNotEqual(self.sealer.seal_inbox('same'), self.sealer.seal_inbox('same'))
        for value in ['plain, from before', '', None]:
            self.assertEqual(message_seal.open_inbox(self.sealer, value), value)
            self.assertEqual(message_seal.open_inbox(None, value), value)
        with self.assertRaises(message_seal.SealError):
            message_seal.Sealer(os.urandom(32)).open_inbox(sealed)
        with self.assertRaises(message_seal.SealError):
            message_seal.open_inbox(None, sealed)

    def test_metadata_keeps_only_lookup_keys_in_the_clear_new_keys_sealed(self):
        text = machine_text.encoded(event(1, 'gmail.message')['metadata'])
        sealed = self.sealer.seal_json(text)
        self.assertNotIn(CANARY, sealed)
        self.assertEqual(set(json.loads(sealed)), {'thread_id', 'from', 'labels', message_seal.SEALED_KEY})
        self.assertEqual(self.sealer.open_json(sealed), text)  # byte for byte what the app wrote (sorted keys)
        self.assertEqual(self.sealer.seal_json(sealed), sealed)
        only_plain = machine_text.encoded({'thread_id': 'x', 'from_me': True})
        self.assertEqual(self.sealer.seal_json(only_plain), only_plain)
        self.assertTrue(message_seal.is_sealed(self.sealer.seal_json('"not an object"', frozenset())))

    def test_plain_metadata_marker_is_not_an_encrypted_envelope(self):
        for metadata in ({'thread_id': 't1', 'snippet': CANARY + ' mentions mc1_sealed'},
                         {'thread_id': 't1', 'mc1_sealed': CANARY},
                         {'thread_id': 't1', 'mc1_sealed': None}):
            text = json.dumps(metadata)
            self.assertFalse(message_seal.is_sealed_json(text))
            self.assertEqual(self.sealer.open_any(text), text)
            sealed = self.sealer.seal_json(text)
            self.assertNotIn(CANARY, sealed)
            self.assertTrue(message_seal.is_sealed_json(sealed))
            self.assertEqual(json.loads(self.sealer.open_json(sealed)), metadata)
            self.assertEqual(self.sealer.seal_json(sealed), sealed)

    def test_index_words_fold_like_sqlite_and_hide_the_word(self):
        self.assertEqual(self.sealer.words('Óscar, OSCAR oscar'), ' '.join([self.sealer.words('oscar')] * 3))
        self.assertNotIn('oscar', self.sealer.words('Óscar'))
        self.assertEqual(self.sealer.words('e-mail'), self.sealer.words('e mail'))


class Protected(unittest.TestCase):
    def setUp(self):
        # these tests choose plain or sealed themselves, also when the whole suite runs sealed
        patcher = unittest.mock.patch.dict(os.environ)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop('MESSAGE_PROTECTION_TEST', None)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'events.sqlite'

    def fill(self, store):
        store.commit_page('acct', {'cursor': 1}, [event(i, kind) for i, kind in enumerate(SOURCES)])
        with store.connect() as db:
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,next_action,outcome) "
                       "VALUES('s1','k1',?,?,'[1]','[\"acct\"]','2026-10-10',?,?)",
                       (f'Reply about {CANARY}', f'Draft: {CANARY} looks good', json.dumps({'kind': 'email', 'body': CANARY}),
                        json.dumps({'state': 'needs_you', 'needs': CANARY})))
            db.execute("INSERT INTO draft_edits VALUES('d1','s1','a','b','edit',?,?,?,?,'owner','2026-10-10')", (CANARY,) * 4)
            db.execute("INSERT INTO facts(text,decision_id,created_at) VALUES('Prefers short replies','x','2026-10-10')")

    def test_every_source_is_sealed_at_rest_and_the_app_reads_and_searches_as_before(self):
        store = machine_main.Store(self.path, protect=True)
        self.fill(store)
        self.assertNotIn(CANARY.encode(), files(self.path))
        self.assertNotIn(CANARY.lower().encode(), files(self.path))
        rows = store.events(['acct'], limit=100)
        self.assertEqual({r['kind'] for r in rows}, set(SOURCES))
        self.assertTrue(all(CANARY in r['title'] and CANARY in r['body'] and r['metadata']['snippet'] for r in rows))
        self.assertEqual(len(store.events(['acct'], query=CANARY.lower())), len(SOURCES))
        self.assertEqual(len(store.events(['acct'], query='oscar friday')), len(SOURCES))  # folded like before
        self.assertEqual(store.events(['acct'], query='absent'), [])
        with store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE json_extract(metadata,'$.thread_id')='t3'").fetchone()[0], 1)
            card = db.execute('SELECT * FROM suggestions').fetchone()
            self.assertIn(CANARY, card['title'])
            self.assertEqual(json.loads(card['next_action'])['body'], CANARY)
            db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")
        raw = sqlite3.connect(self.path)
        self.assertEqual(raw.execute("SELECT json_extract(next_action,'$.kind'), json_extract(outcome,'$.state') FROM suggestions").fetchone(),
                         ('email', 'needs_you'))
        self.assertEqual(raw.execute("SELECT text FROM facts").fetchone()[0], 'Prefers short replies')  # a learning stays readable

    def test_without_the_key_nothing_reads_or_writes_message_text(self):
        store = machine_main.Store(self.path, protect=True)
        self.fill(store)
        raw = sqlite3.connect(self.path)
        self.assertEqual(raw.execute('SELECT typeof(title), typeof(body) FROM events LIMIT 1').fetchone(), ('blob', 'blob'))
        with self.assertRaises(sqlite3.OperationalError):  # a tool without the key can't slip plain text in
            raw.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                        "VALUES('a','b','k','t','plain','plain','{}','h','t')")
        message_seal.key_path(self.path).rename(self.path.with_name('elsewhere'))
        with self.assertRaises(message_seal.SealError):
            machine_main.Store(self.path)

    def test_a_path_that_forgets_to_seal_is_sealed_by_the_database(self):
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:  # plain SQL, as a future code path might write
            db.execute("INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,content_hash,ingested_at) "
                       "VALUES('acct','x','new.kind','2026-10-10',?,?,?,'h','t')", (CANARY, CANARY, json.dumps({'note': CANARY})))
            db.execute("UPDATE events SET body=? WHERE source_id='x'", (CANARY + ' again',))
        self.assertNotIn(CANARY.encode(), files(self.path))
        self.assertEqual(store.events(['acct'], query=CANARY.lower())[0]['body'], CANARY + ' again')

    def stored_plain(self):
        """The sealed columns whose rows, as SQLite has them (no key), hold anything in the clear but the plain keys."""
        with contextlib.closing(sqlite3.connect(self.path)) as raw:
            return [f'{table}.{column}' for table, column, plain in message_seal.sealed_columns(raw)
                    for (value,) in raw.execute(f"SELECT {column} FROM {table} WHERE typeof({column})='text' AND {column}!=''")
                    if plain is None or set(json.loads(value)) - plain - {message_seal.SEALED_KEY}]

    def test_every_sealed_column_seals_what_any_code_writes_plain(self):
        """Not one writer but the database keeps these columns sealed: each takes a plain INSERT and a plain UPDATE, as
        code that never heard of sealing would write them, and the row as stored holds none of it."""
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:
            self.assertEqual(make_source_tables(db), set())
        seen, values = set(), {}
        with store.connect() as db:
            db.execute('PRAGMA foreign_keys=OFF')
            db.execute('PRAGMA ignore_check_constraints=ON')
            for table, column, plain in message_seal.sealed_columns(db):
                values.setdefault(table, {})[column] = plain
            for table, columns in values.items():
                info = db.execute(f'PRAGMA table_info({table})').fetchall()
                say = lambda c, text: machine_text.encoded({'note': text}) if columns[c] is not None else text
                row = {r['name']: say(r['name'], CANARY) if r['name'] in columns else 7 if 'INT' in r['type'].upper() else 'x'
                       for r in info if r['name'] in columns or r['notnull'] or r['pk']}
                with self.subTest(table=table):
                    db.execute(f"INSERT INTO {table}({','.join(row)}) VALUES({','.join('?' * len(row))})", list(row.values()))
                    self.assertEqual(db.execute(f'SELECT {",".join(columns)} FROM {table}').fetchone()[:], tuple(row[c] for c in columns))
                    for column in columns:
                        db.execute(f'UPDATE {table} SET {column}=?', (say(column, CANARY + ' again'),))
                        seen.add((table, column))
                    self.assertEqual(db.execute(f'SELECT {",".join(columns)} FROM {table}').fetchone()[:], tuple(say(c, CANARY + ' again') for c in columns))
        self.assertEqual(len(seen), sum(len(c) for c in values.values()))
        self.assertLessEqual({('events', c) for c in ('title', 'body', 'metadata')}, seen)
        self.assertEqual(self.stored_plain(), [])
        self.assertNotIn(CANARY.encode(), files(self.path))

    def test_the_stores_writers_of_events_leave_them_sealed(self):
        """The Store's ways of writing a message's title, text or metadata (one added later is covered by the test above),
        then the rows and the files as stored."""
        store = machine_main.Store(self.path, protect=True)
        feed = {'transport': 'existing_openclaw_feed', 'app_name': CANARY, 'is_active': True, 'snapshot_content_hash': '1'}
        talk = lambda **facts: {**event(1, 'intercom.conversation'), 'metadata': {'conversation_id': '1', 'subject': CANARY, **facts}}
        reply = lambda name: {'at': 100, 'admin_id': '51', 'name': f'{CANARY} {name}'}
        phone = lambda n: {**event(2, 'android.notification'), 'metadata': {**feed, 'updates_merged': n}}
        slack = lambda title: {**event(3, 'slack.message'), 'title': title, 'body': f'hi {CANARY}',
                               'metadata': {'channel_name': 'DM U02AB3CD4', 'user_id': 'U02AB3CD4', 'sender_id': 'U02AB3CD4'}}
        store.commit_page('acct', {'c': 1}, [talk(), phone(1), slack(f'#DM U02AB3CD4: hi {CANARY}'), event(4, 'gmail.message')])
        raw = lambda what: sqlite3.connect(self.path).execute(f'SELECT {what} FROM events ORDER BY id').fetchall()
        before = raw('content_hash,version,analyzed_version')
        # the same message again, with other facts beside it: kept, and no new version
        store.commit_page('acct', {'c': 2}, [talk(team_reply=reply('Sam')), phone(2), slack(f'#DM Sam Lee: hi {CANARY}')])
        self.assertEqual(raw('content_hash,version,analyzed_version'), before)
        meta = lambda i: next(r['metadata'] for r in store.events(['acct'], limit=100) if r['source_id'].endswith(f':{i}'))
        seen = meta(1)['team_reply']['seen']  # when the Machine first had it: read back from the row as sealed
        with unittest.mock.patch('machine.store.events.now', return_value='2099-01-01T00:00:00+00:00'):
            store.commit_page('acct', {'c': 3}, [talk(team_reply=reply('Sam'))])
        self.assertEqual((meta(1)['team_reply'], meta(2)['updates_merged']), ({**reply('Sam'), 'seen': seen}, 2))
        titles = lambda: [r['title'] for r in store.events(['acct'], limit=100) if r['kind'] == 'slack.message']
        self.assertEqual(titles(), [f'#DM Sam Lee: hi {CANARY}'])
        store.commit_page('acct', {'c': 3}, [slack(f'#DM U02AB3CD4: hi {CANARY}')])
        with unittest.mock.patch('graph.slack_names', return_value={'U02AB3CD4': f'Kim {CANARY}'}):
            store.name_slack_titles('acct')
        self.assertEqual(len(titles()), 1)
        quoted = f'Yes, {CANARY}.\n\nOn Mon, Oct 5, 2026 at 9:00 AM Pat <pat@example.com> wrote:\n' + f'> an older {CANARY} line\n' * 400
        store.commit_page('acct', {'c': 3}, [{**event(6, 'gmail.message'), 'body': quoted}])
        store.trim_stored_quoted_history()
        forwarded = {**event(7, 'android.notification'), 'source_id': 'forwarded:one',
                     'metadata': {'transport': 'existing_openclaw_feed', 'notification_key_hash': 'key', 'package_name': 'com.example.app', 'change': 'posted'}}
        store.commit_page('acct', {'c': 3}, [forwarded])
        with unittest.mock.patch('machine.store.events.now', return_value='2026-10-30T09:00:00+00:00'):
            self.assertEqual(store.coalesce_android_history({'id': 'acct'})['signals_after'], 1)
        store.commit_page('acct', {'c': 4}, [{**event(4, 'gmail.message'), 'body': f'{CANARY} edited'}])  # an edit
        store.keep_found('acct', [event(5, 'gmail.message')])
        made = store.reviewed_event('acct', 'meet:1', 'meet.time', CANARY, CANARY, {'note': CANARY})
        store.machine_card('acct', 'gateway.fault', 'fault:1', CANARY, CANARY, CANARY, {'note': CANARY})
        store.owner_card(f'Call {CANARY} back', 'acct')
        with store.connect() as db:
            machine_events.add_ai_request(db, 'acct', 'ai:1', '2026-10-10T09:00:00+00:00', CANARY, CANARY, {'note': CANARY})
            note = {'account_id': 'acct', 'source_id': 'notes:1', 'kind': 'meeting.notes', 'occurred_at': '2026-10-10T09:00:00+00:00', 'title': CANARY, 'body': CANARY,
                    'metadata': json.dumps({'note': CANARY}), 'content_hash': 'h', 'ingested_at': '2026-10-10T09:00:00+00:00'}
            kept = machine_events.save_meeting_notes(db, ('insert', note))
            machine_events.save_meeting_notes(db, ('update', kept['notes_id'], note))
        store.suggest('brief', f'{CANARY} brief', CANARY, [made])
        with store.connect() as db:
            sid = db.execute("SELECT suggestion_id FROM suggestion_keys WHERE dedupe_key='brief'").fetchone()
            sid = sid[0] if sid else db.execute("SELECT id FROM suggestions WHERE dedupe_key='brief'").fetchone()[0]
            db.execute("UPDATE events SET kind='fleet.brief' WHERE id=?", (made,))
        self.assertTrue(store.brief_reword(sid, f'{CANARY} anew', CANARY))
        self.assertTrue(store.cleanup_grow(sid, made, f'{CANARY} grown', CANARY, {'note': CANARY}, kind='fleet.brief'))
        self.assertEqual(store.events(['acct'], query=f'{CANARY} grown', limit=1)[0]['metadata'], {'note': CANARY})
        self.assertEqual(self.stored_plain(), [])
        self.assertNotIn(CANARY.encode(), files(self.path))
        self.assertNotIn(CANARY.lower().encode(), files(self.path))

    def test_a_table_made_later_is_guarded_and_sealed(self):
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:
            db.execute('DROP TABLE IF EXISTS network_replies')
        with sqlite3.connect(self.path) as raw:  # made, and written to, by code that knew nothing of sealing
            raw.execute('CREATE TABLE network_replies(ask_id TEXT PRIMARY KEY,body TEXT NOT NULL,at TEXT NOT NULL)')
            raw.execute("INSERT INTO network_replies VALUES('a',?,'t')", (CANARY,))
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT body FROM network_replies').fetchone()[0], CANARY)
            db.execute("INSERT INTO network_replies VALUES('b',?,'t')", (CANARY,))
        with store.connect():
            pass
        self.assertEqual(sqlite3.connect(self.path).execute("SELECT count(*) FROM network_replies WHERE typeof(body)='blob'").fetchone()[0], 2)

    def stopped_run(self, store):
        """A preparation that stopped on a question, a permission it asked for, and a review's why: all through the app's
        own code."""
        questions = [{'q': f'Which {CANARY}?', 'a': [f'the {CANARY} one']}]
        with store.connect() as db:
            db.execute("INSERT INTO preparations(suggestion_id,decision_id,job_id,status,error,reason,details,questions,created_at,updated_at) "
                       "VALUES('s1','d','j1','blocked','needs_owner',?,?,?,'t','t')", (f'Needs {CANARY}', json.dumps([f'{CANARY} asked']), json.dumps(questions)))
        store.tool_approval_proposal(hashlib.sha256(f'exec {CANARY}'.encode()).hexdigest(), f'Send to {CANARY}', f'exec {CANARY}')
        return questions

    def test_what_a_stopped_run_says_is_sealed_and_read_as_before(self):
        store = machine_main.Store(self.path, protect=True)
        self.fill(store)
        questions = self.stopped_run(store)
        self.assertNotIn(CANARY.encode(), files(self.path))
        with store.connect() as db:
            row = db.execute('SELECT * FROM preparations').fetchone()
            self.assertEqual((row['status'], row['error'], row['reason'], json.loads(row['details']), json.loads(row['questions'])),
                             ('blocked', 'needs_owner', f'Needs {CANARY}', [f'{CANARY} asked'], questions))
            self.assertEqual(db.execute("SELECT count(*) FROM preparations p WHERE trim(coalesce(p.reason,''))<>''").fetchone()[0], 1)  # AHEAD_BLOCKERS
        self.assertEqual(store.tool_approval_document(hashlib.sha256(f'exec {CANARY}'.encode()).hexdigest())['detail'], f'exec {CANARY}')
        with store.connect() as db:
            db.execute('UPDATE suggestions SET next_action=NULL')
        self.assertIn(f'Needs {CANARY}', json.dumps(store.snapshot([{'id': 'acct', 'boundary': 'work'}]), default=str))
        raw = sqlite3.connect(self.path)  # without the key: the states support reads, none of the words
        self.assertEqual(raw.execute('SELECT status,error,typeof(reason),typeof(details),typeof(questions) FROM preparations').fetchone(),
                         ('blocked', 'needs_owner', 'blob', 'blob', 'blob'))
        self.assertNotIn(CANARY, json.dumps(learnings.export(self.path), default=str))

    def test_an_update_seals_what_stopped_runs_already_kept_plain_also_by_an_older_release(self):
        older = {t: tuple(c for c in cs if (t, c) not in {('preparations', 'reason'), ('preparations', 'details'), ('preparations', 'questions'),
                                                          ('tool_approval_proposals', 'title'), ('tool_approval_proposals', 'detail'), ('analyses', 'whys')})
                 for t, cs in message_seal.DERIVED.items()}
        with unittest.mock.patch.dict(message_seal.DERIVED, older):
            before = machine_main.Store(self.path, protect=True)
            self.fill(before)
            self.stopped_run(before)
            with before.connect() as db:
                self.old_review(db)
        self.assertIn(CANARY.encode(), files(self.path))
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT reason FROM preparations').fetchone()[0], f'Needs {CANARY}')
            self.assert_moved(db)
        self.assertNotIn(CANARY.encode(), files(self.path))
        # Back on the older release: it reads them sealed (a row opens whatever is sealed in it) and what it writes is
        # sealed by the guards, which stay in the database
        with unittest.mock.patch.dict(message_seal.DERIVED, older):
            back = machine_main.Store(self.path, protect=True)
            with back.connect() as db:
                self.assertEqual(db.execute('SELECT reason FROM preparations').fetchone()[0], f'Needs {CANARY}')
                db.execute('UPDATE preparations SET reason=?', (f'Still needs {CANARY}',))
            with back.connect() as db:
                self.assertEqual(db.execute('SELECT reason FROM preparations').fetchone()[0], f'Still needs {CANARY}')
        self.assertNotIn(CANARY.encode(), files(self.path))

    def old_review(self, db):
        """A finished review from before its whys were kept apart: the words in its items, two reviews."""
        for n, items in enumerate(([{'id': 1, 'version': 1, 'no_todo': f'Only {CANARY}'}, {'id': 2, 'version': 1, 'no_reply': f'Thanks {CANARY}'},
                                    {'id': 3, 'version': 1, 'no_todo': f'Gone {CANARY}', 'excluded': 'person_deleted'}], [{'id': 4, 'version': 1}])):
            db.execute("INSERT INTO analyses(id,started_at,finished_at,items,status) VALUES(?,'t','t',?,'complete')", (f'r{n}', json.dumps(items)))

    def assert_moved(self, db):
        self.assertEqual(json.loads(db.execute("SELECT items FROM analyses WHERE id='r0'").fetchone()[0]),
                         [{'id': 1, 'version': 1}, {'id': 2, 'version': 1, 'no_reply': True}, {'id': 3, 'version': 1, 'excluded': 'person_deleted'}])
        whys = review_whys.read(db.execute("SELECT whys FROM analyses WHERE id='r0'").fetchone()[0])
        self.assertEqual(whys, {1: {'no_todo': f'Only {CANARY}'}, 2: {'no_reply': f'Thanks {CANARY}'}})

    def test_why_a_review_made_no_to_do_moves_out_of_its_items_sealed(self):
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:
            self.old_review(db)
        store = machine_main.Store(self.path, protect=True)
        self.assertNotIn(CANARY.encode(), files(self.path))
        with store.connect() as db:
            self.assert_moved(db)
            self.assertEqual(review_whys.move(db), 0)
            review_whys.drop(db, 'r0', {1})  # the owner deleted that message
            self.assertEqual(review_whys.read(db.execute("SELECT whys FROM analyses WHERE id='r0'").fetchone()[0]), {2: {'no_reply': f'Thanks {CANARY}'}})

    def test_a_fix_keeps_no_quote_or_reason_readable(self):
        import corrections
        import learning_loop
        store = machine_main.Store(self.path, protect=True)
        rows = {'rows': [{'identifier': 'a@x', 'role': 'accountant', 'source': 'owner', 'quote': CANARY}]}
        with store.connect() as db:
            learning_loop.ensure(db)
        with store.connect() as db:  # as fixes were kept before
            learning_loop.record(db, 'fix:1', 'source', json.dumps({'type': 'role', 'where': {'id': 'a@x', 'ids': ['a@x']}, 'line': ['{}', 'Ann'], 'after': rows}),
                                 json.dumps({'text': 'lawyer', 'state': rows}), 'Ann is the accountant', '')
        self.assertIn(CANARY.encode(), files(self.path))
        with store.connect() as db:
            corrections.drop_quotes(db)
        self.assertNotIn(CANARY.encode(), files(self.path))
        with store.connect() as db:
            row = db.execute('SELECT * FROM learning_changes').fetchone()
        self.assertTrue(corrections._same('role', rows, json.loads(row['target'])['after']), 'Undo still compares what it left')
        self.assertEqual(json.loads(row['before'])['state'], rows)

    def test_a_waiting_notification_keeps_its_to_do_title_sealed_and_sends_it_readable(self):
        import notify
        store = machine_main.Store(self.path, protect=True)
        title = f'Reply about {CANARY}'
        with store.connect() as db:
            notify.ensure(db)
        with store.connect() as db:
            notify.hold(db, 'push', 'todo', title, 5000.0, ref='suggestion:s1', payload={'title': title, 'tag': 's1'}, clock=lambda: 5000.0)
            notify.hold(db, 'email', 'todo', title, 5000.0, ref='suggestion:s1', clock=lambda: 5000.0)
            notify.app_line_save(db, 's1', f'Ready: {title}', body=f'1 to-do: {title}')
        # a sent digest, kept to open again from its notification: this morning's, so it is never past DIGEST_KEEP
        at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
        with store.connect() as db:
            notify.digest_claim(db, at.date().isoformat(), at.isoformat())
        with store.connect() as db:
            notify.digest_done(db, at.date().isoformat(), 'sent', ['push'], notify.compose([], [{'title': title}], []))
        self.assertNotIn(CANARY.encode(), files(self.path))
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT typeof(body) FROM notify_digests').fetchone()[0], 'blob')
            self.assertEqual({r[0] for r in raw.execute('SELECT typeof(title) FROM notify_queue')}, {'blob'})
            self.assertEqual(raw.execute("SELECT typeof(payload) FROM notify_queue WHERE channel='push'").fetchone()[0], 'blob')
            self.assertEqual(raw.execute('SELECT typeof(line),typeof(body) FROM notify_app_lines').fetchone(), ('blob', 'blob'))
        with store.connect() as db:
            self.assertEqual(notify.app_line(db, 's1'), f'Ready: {title}')
            self.assertEqual(notify.app_line_body(db, 's1'), f'1 to-do: {title}')
            self.assertIn(title, notify.digest_shown(db, 'morning')['text'])
            with unittest.mock.patch.object(notify, 'active', return_value=False), unittest.mock.patch.object(notify, 'push_now', return_value=True), \
                    unittest.mock.patch.object(notify, 'last_seen', return_value=0.0):
                pushes, lines = notify.take_due(db, clock=lambda: 5000.0)
        self.assertEqual([p['payload'] for p in pushes], [{'title': title, 'tag': 's1'}])
        self.assertEqual([line['title'] for line in lines], [title])

    def test_an_update_seals_the_notifications_a_sealed_machine_already_kept_plain(self):
        import notify
        store = machine_main.Store(self.path, protect=True)
        with sqlite3.connect(self.path) as raw:  # as the version before left it: the tables there, without guards, the rows plain
            for statement in (notify.SCHEMA, notify.DIGESTS, notify.QUEUE, notify.APP_DEVICES, notify.APP_LINES_TABLE):
                raw.execute(statement)
            raw.execute("INSERT INTO notify_queue(channel,kind,title,payload,created,due) VALUES('email','todo',?,?,1,1)", (CANARY, json.dumps({'title': CANARY})))
            raw.execute("INSERT INTO notify_app_lines(tag,line,at,body) VALUES('s1',?,?,?)", (CANARY, notify.wall(), CANARY))
        store = machine_main.Store(self.path)  # the updated app starts
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT title,payload FROM notify_queue').fetchone()[:], (CANARY, json.dumps({'title': CANARY})))
            self.assertEqual(notify.app_line(db, 's1'), CANARY)
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT typeof(title),typeof(payload) FROM notify_queue').fetchone(), ('blob', 'blob'))
            self.assertEqual(raw.execute('SELECT typeof(line),typeof(body) FROM notify_app_lines').fetchone(), ('blob', 'blob'))
            with self.assertRaises(sqlite3.OperationalError):  # no key: a plain write fails, it is never stored
                raw.execute("INSERT INTO notify_queue(channel,kind,title,created,due) VALUES('email','todo','plain',1,1)")

    def learn(self, db, run_id='run1'):
        """A finished team learnings pass with two learnings, one dropped: kept as the app keeps them."""
        import fleet
        import fleet_learnings
        evidence = {'fleet_learn': True, 'fleet': 'f1', 'companies': {'1': 'a' * 16, '2': 'b' * 16}, 'read': ['t1']}
        draft = {'learnings': [{'kind': 'process', 'text': LEARNED, 'confidence': 0.9, 'threads': [1, 2]},
                               {'kind': 'tool', 'text': LEARNED_TOO, 'confidence': 0.8, 'threads': [1, 2]},
                               {'kind': 'personal', 'text': f'Someone at {CANARY} is moving house soon.', 'confidence': 0.9, 'threads': [1, 2]}]}
        db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,draft) VALUES(?,'ok','2026-11-01','2026-11-01',?,'fleet_learn',?)",
                   (run_id, json.dumps(evidence), json.dumps(draft)))
        return fleet_learnings.finish(db, run_id, [], log=lambda *args: fleet.Fleet.log(None, *args))

    def test_team_learnings_learned_changes_and_the_fleet_log_are_sealed_and_read_as_before(self):
        import fleet
        import fleet_learnings
        import learning_loop
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:  # the tables a Fleet and the first look make, at their first use
            for statement in fleet.SCHEMA.split(';'):
                if statement.strip():
                    db.execute(statement)
            fleet_learnings.ensure(db)
            db.execute(LEARNED_FIXES)
        with store.connect() as db:
            self.assertEqual([k['text'] for k in self.learn(db)], [LEARNED, LEARNED_TOO])
            self.assertEqual(fleet_learnings.remove(db, 'f1', fleet_learnings.fingerprint(LEARNED_TOO)), LEARNED_TOO)
            learning_loop.record(db, 'run2', 'fact', '7', json.dumps({'id': 6, 'text': f'Old {CANARY} fact'}), f'New {CANARY} fact', f'Corrected the {CANARY} to-do.')
            db.execute("INSERT INTO learned_fixes(key,state,text,at) VALUES('hours','removed',?,'2026-11-01')", (f'Works {CANARY} hours',))
            learning_loop.record(db, 'learned:off:1', 'learned', 'hours', None, f'Works {CANARY} hours', 'Corrected after the first look.')
        for word in (CANARY.encode(), CANARY.lower().encode()):
            self.assertNotIn(word, files(self.path))  # nor in the pass's draft, which keeps only a count
        with sqlite3.connect(self.path) as raw:
            for table, columns in (('fleet_learnings', 'text'), ('fleet_learn_removed', 'text'), ('learned_fixes', 'text'), ('fleet_log', 'what'),
                                   ('learning_changes', 'after'), ('learning_changes', 'why')):
                self.assertEqual({r[0] for r in raw.execute(f'SELECT typeof({columns}) FROM {table}')}, {'blob'}, table)
            self.assertEqual({r[0] for r in raw.execute('SELECT typeof(before) FROM learning_changes')}, {'blob', 'null'})
            self.assertEqual(raw.execute("SELECT draft FROM profile_runs WHERE run_id='run1'").fetchone()[0], '{"drafted": 3}')
            # what SQL filters, sorts and joins on stays plain
            self.assertEqual(raw.execute('SELECT fleet,fp,kind,confidence,run_id FROM fleet_learnings').fetchall(),
                             [('f1', fleet_learnings.fingerprint(LEARNED), 'process', 0.9, 'run1'), ('f1', fleet_learnings.fingerprint(LEARNED_TOO), 'tool', 0.8, 'run1')])
            self.assertEqual(raw.execute('SELECT key,state FROM learned_fixes').fetchall(), [('hours', 'removed')])
            self.assertEqual(raw.execute("SELECT kind,target,status FROM learning_changes WHERE run_id='run2'").fetchall(), [('fact', '7', 'applied')])
        with store.connect() as db:
            self.assertEqual([(i['text'], i['mine']) for i in fleet_learnings.view(db, 'f1', {})], [(LEARNED, True)])
            self.assertEqual(fleet_learnings.removed(db, 'f1'), {fleet_learnings.fingerprint(LEARNED_TOO): LEARNED_TOO})
            self.assertEqual([i['text'] for i in fleet_learnings.pick(db, 'f1', 'Refund request', 'A customer asks for a refund via the support inbox.')], [LEARNED])
            # what goes to teammates is the opened text, for the Team Graph to seal for them as it does the rest
            sent = fleet_learnings.records(db, 'f1', lambda local: local)
            self.assertEqual(sorted((r['t'], r.get('text')) for r in sent.values()), [('learning', LEARNED), ('unlearn', None)])
            self.assertEqual(fleet_learnings.finish(db, 'run1', []), [])  # the same pass again: nothing twice
            changes = {c['kind']: c for c in learning_loop.recent(db)}
            self.assertEqual((changes['fact']['text'], changes['fact']['before'], changes['fact']['why']),
                             (f'New {CANARY} fact', f'Old {CANARY} fact', f'Corrected the {CANARY} to-do.'))
            self.assertEqual(changes['learned']['text'], f'Works {CANARY} hours')
            self.assertEqual(learning_loop.undo(db, changes['learned']['id'])['undone'], changes['learned']['id'])
            self.assertEqual([r['what'] for r in db.execute('SELECT what FROM fleet_log ORDER BY id')], [LEARNED, LEARNED_TOO])

    def test_an_update_seals_the_learnings_a_sealed_machine_already_kept_plain(self):
        import fleet
        import fleet_learnings
        import learning_loop
        store = machine_main.Store(self.path, protect=True)
        kept = {'fleet_learnings': ('text', LEARNED), 'fleet_learn_removed': ('text', LEARNED_TOO), 'learned_fixes': ('text', f'Works {CANARY} hours'),
                'fleet_log': ('what', LEARNED)}
        with sqlite3.connect(self.path) as raw:  # as the version before left it: the tables there, without guards, the rows plain
            for statement in (fleet.SCHEMA + ';' + fleet_learnings.SCHEMA + ';' + LEARNED_FIXES).split(';'):
                if statement.strip():
                    raw.execute(statement)
            for name in [r[0] for r in raw.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND (name LIKE 'mc_learning_changes_%' OR name LIKE 'mc_learned_fixes_%')")]:
                raw.execute(f'DROP TRIGGER {name}')
            raw.execute("INSERT INTO fleet_learnings(fleet,fp,kind,text,confidence,run_id,at) VALUES('f1','a','process',?,0.9,'r','2026-11-01')", (LEARNED,))
            raw.execute("INSERT INTO fleet_learn_removed(fleet,fp,text,by,at) VALUES('f1','b',?,'me','2026-11-01')", (LEARNED_TOO,))
            raw.execute("INSERT INTO learned_fixes(key,state,text,at) VALUES('hours','removed',?,'2026-11-01')", (kept['learned_fixes'][1],))
            raw.execute("INSERT INTO fleet_log(at,direction,fleet,kind,what,outcome) VALUES('2026-11-01','out','f1','learning',?,'shared')", (LEARNED,))
            raw.execute("INSERT INTO learning_changes(run_id,at,kind,target,before,after,why,status) VALUES('r','2026-11-01','fact','7',?,?,?,'applied')",
                        (json.dumps({'id': 6, 'text': CANARY}), CANARY, f'Corrected the {CANARY} to-do.'))
        self.assertIn(CANARY.lower().encode(), files(self.path))
        store = machine_main.Store(self.path)  # the updated app starts
        with store.connect() as db:
            for table, (column, text) in kept.items():
                self.assertEqual(db.execute(f'SELECT {column} FROM {table}').fetchone()[0], text, table)
            self.assertEqual(learning_loop.recent(db)[0] | {'at': None, 'id': None},
                             {'id': None, 'at': None, 'kind': 'fact', 'channel': None, 'text': CANARY, 'before': CANARY, 'why': f'Corrected the {CANARY} to-do.', 'undone': False})
        with sqlite3.connect(self.path) as raw:
            for table, (column, _) in kept.items():
                self.assertEqual(raw.execute(f'SELECT typeof({column}) FROM {table}').fetchone()[0], 'blob', table)
            self.assertEqual(raw.execute('SELECT typeof(before),typeof(after),typeof(why) FROM learning_changes').fetchone(), ('blob', 'blob', 'blob'))
            with self.assertRaises(sqlite3.OperationalError):  # no key: a plain write fails, it is never stored
                raw.execute("INSERT INTO fleet_log(at,direction,fleet,kind,what,outcome) VALUES('2026-11-01','out','f1','learning','plain','shared')")
        for word in (CANARY.encode(), CANARY.lower().encode()):
            self.assertNotIn(word, files(self.path))

    def test_bring_in_candidates_are_sealed_and_read_as_before(self):
        import bring_in
        store = machine_main.Store(self.path, protect=True)
        workspace = Path(self.temp.name) / 'workspace'
        workspace.mkdir()
        notes = [f'Mira at {CANARY} wants every quote as a PDF, never a link.', f'The {CANARY} school board only reads messages after 8 pm.']
        (workspace / 'MEMORY.md').write_text('# MEMORY.md\n\n' + ''.join(f'- {n}\n' for n in notes))
        with store.connect() as db:  # the tables the first pass makes, at its first use
            bring_in.ensure(db)
        with store.connect() as db:
            state = bring_in.prepare(db, workspace, {})
            reply = json.dumps([{'n': 1, 'text': notes[0], 'kind': 'preference'}, {'n': 2, 'text': notes[1], 'kind': 'fact'}])
            self.assertEqual(bring_in.conclude(db, state, reply), {'offered': 2})
        for word in (CANARY.encode(), CANARY.lower().encode()):
            self.assertNotIn(word, files(self.path))  # nor in the lines a pass has read, which are kept as a hash
        with sqlite3.connect(self.path) as raw:
            self.assertEqual({r[0] for r in raw.execute('SELECT typeof(text) FROM bring_in_items')}, {'blob'})
            # what SQL filters and matches on stays plain
            self.assertEqual(raw.execute('SELECT file,kind,status,key FROM bring_in_items ORDER BY id').fetchall(),
                             [('MEMORY.md', 'preference', 'offered', bring_in._key(notes[0])), ('MEMORY.md', 'fact', 'offered', bring_in._key(notes[1]))])
        with store.connect() as db:
            items = bring_in.offered(db)
            self.assertEqual([(i['text'], i['kind'], i['file']) for i in items], [(notes[0], 'preference', 'MEMORY.md'), (notes[1], 'fact', 'MEMORY.md')])
        self.assertEqual(bring_in.status(store.connect), items)
        # a ticked one becomes a fact like any other; the other stays dismissed, sealed
        self.assertEqual(bring_in.decide(store, keep=[items[0]['id']], dismiss=[items[1]['id']]), {'saved': 1, 'dismissed': 1})
        self.assertEqual([(f['text'], f['source']) for f in store.snapshot([])['facts']], [(notes[0], 'notes:MEMORY.md')])
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT status,typeof(text) FROM bring_in_items ORDER BY id').fetchall(), [('saved', 'blob'), ('dismissed', 'blob')])

    def test_an_update_seals_the_bring_in_candidates_a_sealed_machine_already_kept_plain(self):
        import bring_in
        store = machine_main.Store(self.path, protect=True)
        line = f'Mira at {CANARY} wants every quote as a PDF, never a link.'
        with sqlite3.connect(self.path) as raw:  # as the version before left it: the tables there, without guards, the rows plain
            bring_in.ensure(raw)
            raw.execute("INSERT INTO bring_in_items(file,key,text,kind,created_at) VALUES('MEMORY.md','k1',?,'preference','2026-11-01')", (line,))
            raw.execute("INSERT INTO bring_in_items(file,key,text,kind,status,created_at) VALUES('USER.md','k2',?,'fact','dismissed','2026-11-01')", (f'{CANARY} gone',))
        self.assertIn(CANARY.encode(), files(self.path))
        store = machine_main.Store(self.path)  # the updated app starts
        with store.connect() as db:
            self.assertEqual([(i['text'], i['kind'], i['file']) for i in bring_in.offered(db)], [(line, 'preference', 'MEMORY.md')])
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT status,typeof(text) FROM bring_in_items ORDER BY id').fetchall(), [('offered', 'blob'), ('dismissed', 'blob')])
            with self.assertRaises(sqlite3.OperationalError):  # no key: a plain write fails, it is never stored
                raw.execute("INSERT INTO bring_in_items(file,key,text,kind,created_at) VALUES('MEMORY.md','k3','plain','fact','2026-11-01')")
        for word in (CANARY.encode(), CANARY.lower().encode()):
            self.assertNotIn(word, files(self.path))

    def test_project_sort_note_is_sealed_and_legacy_notes_are_migrated(self):
        store = machine_main.Store(self.path, protect=True)
        import graph
        with store.connect() as db:
            graph.ensure(db)
            db.execute("INSERT INTO projects(name,created_at,sort_note) VALUES('Sample project','2026-10-24',?)", (CANARY,))
            self.assertEqual(db.execute('SELECT sort_note FROM projects').fetchone()[0], CANARY)
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT typeof(sort_note) FROM projects').fetchone()[0], 'blob')
            raw.execute('DROP TRIGGER mc_projects_sort_note_update')
            raw.execute('UPDATE projects SET sort_note=?', (CANARY + ' before sealing',))
        with store.connect():
            pass
        with sqlite3.connect(self.path) as raw:
            self.assertEqual(raw.execute('SELECT typeof(sort_note) FROM projects').fetchone()[0], 'blob')
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT sort_note FROM projects').fetchone()[0], CANARY + ' before sealing')

    def test_a_reviews_board_check_answer_is_sealed_also_when_written_before(self):
        store = machine_main.Store(self.path, protect=True)
        import graph
        with store.connect() as db:
            graph.ensure(db)
            db.execute("INSERT OR REPLACE INTO board_offers(id,run_id,offered_at) VALUES(1,'r1','2026-10-24T00:00:00+00:00')")
            graph.board_check_answer(db, 'r1', f'none: {CANARY} is a one-off')
        self.assertNotIn(CANARY.encode(), files(self.path))
        with sqlite3.connect(self.path) as raw:  # an answer written before the column was sealed
            raw.execute('DROP TRIGGER mc_board_offers_answer_update')
            raw.execute('UPDATE board_offers SET answer=?', (f'none: {CANARY} in the clear',))
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT answer FROM board_offers').fetchone()[0], f'none: {CANARY} in the clear')
        with store.connect():
            pass
        self.assertEqual(sqlite3.connect(self.path).execute("SELECT typeof(answer) FROM board_offers").fetchone()[0], 'blob')
        self.assertEqual(store.boards_text('r2'), '')  # still counts as answered today

    def test_a_phone_notification_waits_sealed_and_arrives_readable(self):
        store = machine_main.Store(self.path, protect=True)
        account = {'id': 'phone', 'service': 'android'}
        key = 'a' * 64
        for i, text in enumerate([store.sealer.seal_inbox(CANARY + ' sealed'), CANARY + ' from before the update']):
            envelope = {'id': f'n{i}', 'at_ms': 1000 + i, 'change': 'posted', 'package_name': 'com.example',
                        'notification_key_hash': key + str(i), 'text': text}
            with sqlite3.connect(self.path) as raw:  # as the Gateway's plugin writes it: no key on that connection
                raw.execute('INSERT INTO android_inbox VALUES(?,?,?)', (envelope['id'], json.dumps(envelope), '2020-01-01T00:00:00+00:00'))
        with store.connect() as db:
            rows = db.execute('SELECT * FROM android_inbox ORDER BY id').fetchall()
        events, consumed = store.android_feed_batch(account, rows)
        self.assertEqual(sorted(e['body'] for e in events), [CANARY + ' from before the update', CANARY + ' sealed'])
        self.assertEqual(sorted(consumed), ['n0', 'n1'])

    def test_role_quotes_promises_and_run_evidence_sealed_in_place_and_promises_still_dedupe(self):
        store = machine_main.Store(self.path, protect=True)
        self.fill(store)
        columns = (('person_roles', 'quote'), ('person_roles', 'hints'), ('promises', 'what'), ('promises', 'note'), ('promises', 'refund'),
                   ('profile_runs', 'evidence'))
        with sqlite3.connect(self.path) as raw:  # a database sealed before these columns were: no guards, plain text
            for table, column in columns:
                for when in ('insert', 'update'):
                    raw.execute(f'DROP TRIGGER mc_{table}_{column}_{when}')
            raw.execute("INSERT INTO person_roles(identifier,role,source,created_at,event_id,quote,hints) VALUES('email:pat@example.com','lawyer','review','t',1,?,?)",
                        (f'{CANARY} counsel', json.dumps([f'{CANARY} invoices'])))
            raw.execute("INSERT INTO promises(direction,who,what,check_at,event_id,account_id,status,note,created_at,updated_at,refund) "
                        "VALUES('theirs','Pat',?,'2026-10-20',1,'acct','answered',?,'t','t',?)", (f'send the {CANARY} contract', f'They wrote again: {CANARY}',
                                                                                                json.dumps({'ref': CANARY})))
            raw.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind) VALUES('r','ok','t','t',?,'profile')",
                        (json.dumps({'messages': [CANARY]}),))
        self.assertIn(CANARY.encode(), files(self.path))
        store = machine_main.Store(self.path, protect=True)
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT quote FROM person_roles').fetchone()[0], f'{CANARY} counsel')
            self.assertEqual(json.loads(db.execute('SELECT evidence FROM profile_runs').fetchone()[0]), {'messages': [CANARY]})
        raw = sqlite3.connect(self.path)
        for table, column in columns:
            self.assertEqual(raw.execute(f'SELECT typeof({column}) FROM {table}').fetchone()[0], 'blob', f'{table}.{column}')
        raw.close()
        first = store.promise({'direction': 'theirs', 'who': 'Pat', 'what': f'send the {CANARY} contract', 'event_id': 1})
        self.assertTrue(first['duplicate'])
        other = store.promise({'direction': 'theirs', 'who': 'Pat', 'what': 'confirm the seat count', 'event_id': 1})
        self.assertEqual(store.promise({'direction': 'theirs', 'who': 'Pat', 'what': 'confirm the seat count', 'event_id': 1}),
                         {'id': other['id'], 'status': 'open', 'duplicate': True})
        self.assertEqual(sorted(p['what'] for p in store.promises()), ['confirm the seat count', f'send the {CANARY} contract'])
        self.assertNotIn(CANARY.encode(), files(self.path))

    def test_migration_seals_existing_messages_and_rolls_back(self):
        plain = machine_main.Store(self.path)
        self.fill(plain)
        self.assertIn(CANARY.encode(), files(self.path))
        self.assertEqual(len(plain.events(['acct'], query=CANARY.lower())), len(SOURCES))
        sealed = machine_main.Store(self.path, protect=True)
        self.assertNotIn(CANARY.encode(), files(self.path))  # VACUUM: no free page keeps the old text
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir() if 'protection' in p.name), [])  # the copy goes once checked
        self.assertEqual(len(sealed.events(['acct'], query=CANARY.lower())), len(SOURCES))
        self.assertTrue(message_seal.is_protected(sqlite3.connect(self.path)))
        machine_main.Store(self.path)  # no setting: stays as it is
        self.assertTrue(message_seal.is_protected(sqlite3.connect(self.path)))
        opened = machine_main.Store(self.path, protect=False)
        self.assertFalse(message_seal.is_protected(sqlite3.connect(self.path)))
        self.assertIn(CANARY.encode(), files(self.path))
        self.assertEqual(len(opened.events(['acct'], query=CANARY.lower())), len(SOURCES))
        opened.commit_page('acct', {'cursor': 2}, [event(99, 'slack.message')])
        self.assertEqual(sqlite3.connect(self.path).execute("SELECT count(*) FROM events WHERE typeof(body)='blob'").fetchone()[0], 0)
        with opened.connect() as db:
            db.execute("INSERT INTO event_search(event_search,rank) VALUES('integrity-check',1)")

    def test_a_failed_migration_changes_nothing(self):
        plain = machine_main.Store(self.path)
        self.fill(plain)
        original = message_seal.protect
        message_seal.protect = lambda db: (original(db), (_ for _ in ()).throw(RuntimeError('power cut')))
        try:
            with self.assertLogs(machine_config.LOG, 'ERROR'):  # logged; the app starts as it was
                self.assertFalse(machine_main.Store(self.path, protect=True).protected)
        finally:
            message_seal.protect = original
        self.assertFalse(message_seal.is_protected(sqlite3.connect(self.path)))
        self.assertEqual(sorted(p.name for p in self.path.parent.iterdir() if 'protection' in p.name), [])  # no copy stays behind
        self.assertEqual(len(machine_main.Store(self.path).events(['acct'], query=CANARY.lower())), len(SOURCES))

    def everything_but_the_database(self):
        return b''.join(p.read_bytes() for p in self.path.parent.rglob('*') if p.is_file() and not p.name.startswith('events.sqlite'))

    def test_the_copy_while_switching_is_encrypted(self):
        self.fill(machine_main.Store(self.path))
        seen = []
        original = message_seal.protect
        def look(db):
            seen.append(self.everything_but_the_database())
            safety = self.path.with_name('.events.sqlite.before-protection.d')
            seen.append(sorted(p.name for p in safety.iterdir()))
            seen.append(oct(safety.stat().st_mode & 0o777))
            return original(db)
        message_seal.protect = look
        try:
            machine_main.Store(self.path, protect=True)
        finally:
            message_seal.protect = original
        self.assertNotIn(CANARY.encode(), seen[0])
        self.assertEqual(seen[1:], [['events.sqlite.before-protection.sealed'], '0o700'])
        self.assertFalse(self.path.with_name('.events.sqlite.before-protection.d').exists())

    def test_a_change_that_does_not_open_is_put_back(self):
        self.fill(machine_main.Store(self.path))
        original = machine_main.Store.check_sealed
        calls = []
        def broken(store):
            calls.append(1)
            if len(calls) == 1:
                raise message_seal.SealError('does not open')
            return original(store)
        machine_main.Store.check_sealed = broken
        try:
            with self.assertLogs(machine_config.LOG, 'ERROR'):
                store = machine_main.Store(self.path, protect=True)
        finally:
            machine_main.Store.check_sealed = original
        self.assertFalse(store.protected)
        self.assertFalse(message_seal.is_protected(sqlite3.connect(self.path)))  # put back as it was
        self.assertFalse(self.path.with_name('.events.sqlite.before-protection.d').exists())
        self.assertEqual(len(machine_main.Store(self.path).events(['acct'], query=CANARY.lower())), len(SOURCES))

    def test_a_plain_copy_from_an_earlier_version_is_removed_once_the_database_checks_out(self):
        self.fill(machine_main.Store(self.path, protect=True))
        legacy = self.path.with_name('events.sqlite.before-protection')
        legacy.write_bytes(CANARY.encode() * 100)
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-protection-failed'])
        machine_main.Store(self.path, protect=True)
        self.assertFalse(legacy.exists())
        self.assertEqual(message_seal.problems(self.path), [])

    def test_a_plain_copy_stays_when_the_database_does_not_check_out(self):
        self.fill(machine_main.Store(self.path, protect=True))
        legacy = self.path.with_name('events.sqlite.before-protection')
        legacy.write_bytes(b'kept')
        original = machine_main.Store.database_ok
        machine_main.Store.database_ok = lambda store: False
        try:
            with self.assertLogs(machine_config.LOG, 'ERROR'):
                machine_main.Store(self.path, protect=True)
        finally:
            machine_main.Store.database_ok = original
        self.assertTrue(legacy.exists())
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-protection-failed'])

    def test_an_encrypted_copy_opens_only_with_its_key(self):
        self.fill(machine_main.Store(self.path))
        key, there = os.urandom(32), Path(self.temp.name) / 'copy.sealed'
        machine_text.seal_copy(self.path, there, key)
        self.assertNotIn(CANARY.encode(), there.read_bytes())
        self.assertEqual(sorted(p.name for p in there.parent.iterdir() if p.name.startswith('copy')), ['copy.sealed'])
        back = Path(self.temp.name) / 'back.sqlite'
        machine_text.open_copy(there, back, key)
        self.assertEqual(sqlite3.connect(back).execute('PRAGMA integrity_check').fetchone()[0], 'ok')
        with self.assertRaises(message_seal.SealError):
            machine_text.open_copy(there, back, os.urandom(32))
        there.write_bytes(there.read_bytes()[:-20])
        with self.assertRaises(message_seal.SealError):
            machine_text.open_copy(there, back, key)

    def test_an_export_opens_the_messages_and_leaves_the_key_behind(self):
        config = Path(self.temp.name) / 'config.json'
        config.write_text(json.dumps({'database': str(self.path), 'accounts': []}))
        self.fill(machine_main.Store(self.path, protect=True))
        found = self.exported(config)
        self.assertNotIn(f'data/{message_seal.KEY_NAME}', found)
        db = Path(self.temp.name) / 'exported.sqlite'
        db.write_bytes(found['data/events.sqlite'])
        self.assertFalse(message_seal.is_protected(sqlite3.connect(db)))
        self.assertIn(CANARY.encode(), db.read_bytes())

    def exported(self, config):
        import tarfile
        archive, manifest = moving.export(config, Path(self.temp.name) / 'out', workspace=Path(self.temp.name) / 'ws',
                                          openclaw_home=Path(self.temp.name) / 'oc')
        plain = Path(self.temp.name) / 'opened.tar.gz'
        moving._openssl(['-in', str(archive), '-out', str(plain)], manifest['code'], decrypt=True)
        with tarfile.open(plain, 'r:gz') as opened:
            return {m.name: opened.extractfile(m).read() for m in opened.getmembers() if m.isfile()}

    def app(self, **config):
        app = object.__new__(machine_main.App)
        app.config, app.stop = {'database': str(self.path), **config}, __import__('threading').Event()
        return app

    def test_on_by_default_off_only_when_config_says_so(self):
        self.assertTrue(self.app().protection_now({'database': str(self.path)}))  # a new install
        self.assertTrue(self.app().protection_now({'database': str(self.path), 'message_protection': None}))
        self.assertFalse(self.app().protection_now({'database': str(self.path), 'message_protection': False}))
        self.fill(machine_main.Store(self.path))
        app = self.app()
        store = machine_main.Store(self.path, protect=app.protection_now(app.config))  # an upgrade, with nothing running
        self.assertTrue(store.protected and message_seal.is_protected(sqlite3.connect(self.path)))
        self.assertNotIn(CANARY.encode(), files(self.path))
        self.assertEqual(oct(message_seal.key_path(self.path).stat().st_mode & 0o777), '0o600')

    def test_an_upgrade_waits_until_nothing_runs_then_restarts_to_seal(self):
        self.fill(machine_main.Store(self.path))
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r1','running',?,?)", (now, now))
        app = self.app()
        self.assertIsNone(app.protection_now(app.config))  # a review runs: it is not cut off
        self.assertTrue(app.protection_waits)
        self.assertFalse(machine_main.Store(self.path, protect=None).protected)
        restarts = []
        with patch_everywhere(machine_faults, 'restart_self', lambda: restarts.append(1) or True):
            waiter = __import__('threading').Thread(target=app.protection_waiter, kwargs={'every': 0.05})
            waiter.start()
            __import__('time').sleep(0.3)
            self.assertEqual(restarts, [])
            with sqlite3.connect(self.path) as db:
                db.execute("UPDATE review_runs SET status='complete'")
            waiter.join(5)
        self.assertEqual(restarts, [1])
        self.assertTrue(machine_main.Store(self.path, protect=app.protection_now(app.config)).protected)
        self.assertFalse(app.protection_waits)

    def test_the_key_is_checked_by_doctor_and_the_dashboard(self):
        machine_main.Store(self.path, protect=True)
        self.assertEqual(message_seal.problems(self.path), [])
        key = message_seal.key_path(self.path)
        key.chmod(0o644)
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-key-open'])
        self.assertEqual(machine_app_status.needs_you({'database': str(self.path), 'accounts': []})[0]['action'], f'Run: chmod 600 {key}')
        key.rename(key.with_name('elsewhere'))
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-key-missing'])

    def test_a_key_the_host_keeps_off_the_disk_is_waited_for_and_never_made_anew(self):
        self.fill(machine_main.Store(self.path, protect=True))
        key = message_seal.key_path(self.path)
        memory = Path(self.temp.name) / 'run' / message_seal.KEY_NAME  # the host's copy in memory (/run)
        memory.parent.mkdir()
        key.rename(memory)
        key.symlink_to(memory)
        self.assertTrue(message_seal.held_elsewhere(self.path))
        store = machine_main.Store(self.path, protect=True)  # read through the link, as before
        self.assertEqual(len(store.events(['acct'], query=CANARY.lower())), len(SOURCES))
        self.assertEqual(message_seal.problems(self.path), [])
        saved = memory.read_bytes()
        memory.unlink()  # a restart: /run is empty until the host puts the key back
        self.assertEqual([p[0] for p in message_seal.problems(self.path)], ['message-key-waiting'])
        with self.assertRaises(message_seal.SealError):
            machine_main.Store(self.path, protect=True)
        with self.assertRaises(message_seal.SealError):
            message_seal.load_key(self.path, create=True)
        self.assertFalse(memory.exists())  # no new key that would leave the messages unreadable
        said = []
        self.assertFalse(message_seal.wait_for_key(self.path, say=said.append, every=0.01, limit=0.03))
        self.assertIn('Waiting for the message key', said[0])
        memory.write_bytes(saved)
        self.assertTrue(message_seal.wait_for_key(self.path, say=said.append, every=0.01, limit=0.03))
        self.assertTrue(machine_main.Store(self.path).protected)
        import work_removal
        config = Path(self.temp.name) / 'config.json'
        config.write_text(json.dumps({'database': str(self.path), 'accounts': []}))
        folder = work_removal.backup(config, {'database': str(self.path), 'accounts': []})
        self.assertFalse((folder / message_seal.KEY_NAME).exists())  # its own copy would put the key back on the disk

    def test_an_export_moves_over_and_is_sealed_again_with_the_new_machines_key(self):
        config = Path(self.temp.name) / 'config.json'
        config.write_text(json.dumps({'database': str(self.path), 'accounts': []}))
        self.fill(machine_main.Store(self.path, protect=True))
        there = Path(self.temp.name) / 'there' / 'events.sqlite'
        there.parent.mkdir()
        there.write_bytes(self.exported(config)['data/events.sqlite'])
        app = self.app(database=str(there))
        store = machine_main.Store(there, protect=app.protection_now(app.config))
        self.assertTrue(store.protected)
        self.assertNotEqual(message_seal.key_path(there).read_bytes(), message_seal.key_path(self.path).read_bytes())
        self.assertNotIn(CANARY.encode(), files(there))
        self.assertEqual(len(store.events(['acct'], query=CANARY.lower())), len(SOURCES))

    def test_learnings_hold_what_the_machine_learned_never_message_text(self):
        store = machine_main.Store(self.path, protect=True)
        self.fill(store)
        with store.connect() as db:
            db.execute("INSERT INTO decisions VALUES('d','s1','dismiss','Too pushy','dashboard','2026-10-11')")
        workspace = Path(self.temp.name) / 'ws'
        (workspace / 'memory').mkdir(parents=True)
        (workspace / 'USER.md').write_text('# About me\nShort answers.')
        (workspace / 'memory' / 'notes.md').write_text('Likes Fridays off.')
        out = learnings.export(self.path, workspace, {'accounts': [{'id': 'gmail:owner@example.com', 'service': 'gmail'}],
                                                      'credentials': {'api-token': '/secret'}})
        text = json.dumps(out)
        self.assertNotIn(CANARY.lower(), text.lower())
        self.assertNotIn('owner@example.com', text)
        self.assertNotIn('/secret', text)
        self.assertIn('Too pushy', text)
        self.assertIn('Prefers short replies', text)
        self.assertEqual(out['notes']['USER.md'], '# About me\nShort answers.')
        self.assertEqual(out['tables']['suggestions'][0]['status'], 'pending')
        self.assertEqual(out['tables']['action_jobs'], [])
        self.assertEqual(sum(r['n'] for r in out['counts']['signals']), len(SOURCES))
        self.assertEqual(learnings.export(self.path)['tables']['suggestions'][0]['kind'], 'gmail.message')


# Kept in a database of its own, never in the Machine's: checked there
OTHER_DATABASES = {'telegram_store.py': "the Telegram account's own store, its text sealed by telegram_store itself",
                   'signal_store.py': "the Signal account's own store, its text sealed by signal_store itself"}
# A migration's copy of a table, renamed to that table at once (machine/store/core.py): the same columns
RENAMED = {'promises_next', 'events_monotonic'}
MADE = re.compile(r'CREATE TABLE(?: IF NOT EXISTS)? (\w+)')
ADDED = re.compile(r'ALTER TABLE (\w+) ADD COLUMN (\w+) (\w+)')
# An ALTER TABLE put together at run time: its columns are made by the module's own ensure (or the Store's start)
BUILT = re.compile(r"ADD COLUMN ['{]")
ENSURED = {name + '.py': name for name in ('ai_access', 'fleet', 'graph', 'meeting_prep', 'notify', 'project_about', 'project_success', 'recurring',
                                          'routines', 'team_learnings')}


def source_modules():
    return [p for p in sorted(ROOT.rglob('*.py'))
            if not {'tests', 'node_modules', '.git', '.venv', 'sandbox', 'scripts'} & set(p.relative_to(ROOT).parts[:-1])
            and not p.name.startswith('test_') and p.relative_to(ROOT).as_posix() not in OTHER_DATABASES]


def make_source_tables(db):
    """Make in `db` every table a CREATE TABLE in the source's strings makes, and every column an ALTER TABLE written
    out in full adds. Returns the table names the source mentions that could not be made (a statement built at run
    time): such a table has to be written so this can read it."""
    import ast
    named = set()
    for path in source_modules():
        source = path.read_text(encoding='utf-8')
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and 'CREATE TABLE' in node.value:
                for statement in node.value.split(';'):
                    statement = re.sub(r'(?m)^\s*--.*$', '', statement)  # a comment above it
                    made = MADE.search(statement)
                    if made and statement.strip().startswith('CREATE TABLE'):
                        named.add(made[1])
                        try:
                            db.execute(statement)
                        except sqlite3.OperationalError:  # there already; or no statement by itself: named, so it
                            pass                          # has to be there in the end
        for table, column, kind in ADDED.findall(source):
            try:
                db.execute(f'ALTER TABLE {table} ADD COLUMN {column} {kind}')
            except sqlite3.OperationalError:  # there already, or a table of another database
                pass
    return named - RENAMED - {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}


class NothingOutsideTheSealedFields(unittest.TestCase):
    def test_learnings_never_select_a_sealed_column(self):
        sealed = {('events', c) for c in ('title', 'body', 'metadata')}
        sealed |= {(t, c) for t, cs in message_seal.DERIVED.items() for c in cs}
        sealed |= {(t, c) for t, c, _ in message_seal.DERIVED_JSON}
        for table, columns in learnings.TABLES.items():
            for column in columns:
                self.assertNotIn((table, column), sealed)
                if ' AS ' in column:  # computed: only a JSON column's plain keys, counts, or another table's kind
                    for t, c, plain in message_seal.DERIVED_JSON:
                        if t == table and c in column:
                            self.assertTrue(re.search(r"'\$\.(\w+)'", column)[1] in plain)

    def sealed_json(self, db):
        """What sealed_sql_scan needs: each sealed JSON column with its table and plain keys, and the other tables that
        have a column of that name (their SQL is not this one's business)."""
        columns = {'metadata': ('events', message_seal.PLAIN_METADATA)}
        columns.update({column: (table, plain) for table, column, plain in message_seal.DERIVED_JSON})
        others = {column: set() for column in columns}
        for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall():
            for row in db.execute(f'PRAGMA table_info({table})').fetchall():
                if row[1] in columns and table != columns[row[1]][0]:
                    others[row[1]].add(table)
        return columns, others

    def test_no_sql_reads_a_key_the_seal_hides(self):
        """SQL sees only the plain keys of events.metadata and of the DERIVED_JSON columns on a sealed Machine: a
        statement that reads another key (json_extract, json_each, ->, ->>), or searches or compares the column's
        text, gets NULL there and fails without a sound. Read the rows instead (they open as they are read) and decide
        in Python; tests/test_sealed_sql.py has the places that did it wrong.

        What this cannot see: a key or path only known at run time (listed in RUN_TIME_KEYS, each with where its keys
        come from, and those are checked below); a sealed column given another name in a subquery or view and read by
        that name; SQL put together from pieces in different statements; sandbox/, scripts/ and the other databases'
        modules, which source_modules leaves out. SQL that compares a wholly sealed text column (events.title) is
        another matter and not looked at here."""
        import ai_app
        import missed_work
        import sealed_sql_scan
        from machine.store import conversation, review_last_look, voices
        with tempfile.TemporaryDirectory() as temp:
            with machine_main.Store(Path(temp) / 'events.sqlite').connect() as db:
                make_source_tables(db)
                columns, others = self.sealed_json(db)
        self.assertEqual(sorted(columns), ['metadata', 'next_action', 'outcome', 'payload'])
        self.assertTrue({'notify_queue', 'calendar_writes'} <= others['payload'] and 'agent_jobs' in others['outcome'], others)
        found = sealed_sql_scan.scan(source_modules(), ROOT, columns, others)
        hidden = {where: lines for where, lines in found.items() if where[2] != 'key ?'}
        self.assertEqual(hidden, {}, 'SQL cannot read this on a sealed Machine: read the rows and decide in Python (file, column, what: lines)')
        # A path only known at run time: the statements that have one, and where each takes its keys from. Exact, so
        # that a new one is looked at and one that is gone leaves this list
        RUN_TIME_KEYS = {
            'ai_app.py': (1, 'a key of ai_app.THREAD_KEYS'),
            'machine/app/follow_ups.py': (1, 'thread_id, channel_id, chat_id or conversation_id, picked in the line above'),
            'machine/store/conversation.py': (2, 'a bound path made from conversation.CONTEXT_KEYS'),
            'machine/store/review.py': (1, "channel_id, chat_id or conversation_id from the function's own `keys`"),
            'machine/store/review_last_look.py': (1, 'a key of review_last_look.THREAD_KEYS'),
            'machine/store/voices.py': (1, 'the keys of voices.CONVERSATION_KEYS'),
            'missed_work.py': (1, 'a key of missed_work.THREAD_KEYS'),
        }
        self.assertEqual({(file, column): len(lines) for (file, column, _), lines in found.items()},
                         {(file, 'events.metadata'): count for file, (count, _) in RUN_TIME_KEYS.items()})
        plain = set(message_seal.PLAIN_METADATA)
        self.assertLessEqual(set(ai_app.THREAD_KEYS), plain)
        self.assertLessEqual(set(conversation.CONTEXT_KEYS.values()), plain)
        self.assertLessEqual({key for keys in voices.CONVERSATION_KEYS.values() for key in keys}, plain)
        self.assertLessEqual({key for key, _ in missed_work.THREAD_KEYS}, plain)
        self.assertLessEqual(set(review_last_look.THREAD_KEYS), plain)
        for file, words in (('machine/app/follow_ups.py', ('thread_id', 'channel_id', 'chat_id', 'conversation_id')),
                            ('machine/store/review.py', ('channel_id', 'chat_id', 'conversation_id'))):
            self.assertLessEqual(set(words), plain)
            self.assertTrue(all(f"'{word}'" in (ROOT / file).read_text(encoding='utf-8') for word in words), file)

    def test_the_sql_check_catches_each_way_of_reading_a_hidden_key(self):
        import sealed_sql_scan
        columns = {'metadata': ('events', message_seal.PLAIN_METADATA), 'payload': ('action_jobs', ('kind',)), 'outcome': ('suggestions', ('state',))}
        others = {'metadata': set(), 'payload': {'notify_queue'}, 'outcome': {'agent_jobs'}}

        def reads(text, context=None):
            return sealed_sql_scan.reads(text, context or text, columns, others)
        caught = {
            "SELECT id FROM events WHERE json_extract(metadata,'$.cc') LIKE ?": [('events.metadata', 'key cc')],
            "SELECT 1 FROM events e WHERE coalesce(json_extract(e.metadata,'$.location'),occurred_at)>?": [('events.metadata', 'key location')],
            "SELECT value FROM events, json_each(events.metadata,'$.attendees')": [('events.metadata', 'key attendees')],
            "SELECT 1 FROM events, json_each(metadata)": [('events.metadata', 'whole')],
            "SELECT metadata->>'$.chat_name' FROM events": [('events.metadata', 'key chat_name')],
            "SELECT metadata->>'task_status' FROM events": [('events.metadata', 'key task_status')],
            # asking whether a row has a sealed member does not make a hidden key readable
            "SELECT 1 FROM events WHERE json_extract(metadata,'$.organizer') IS NULL AND json_extract(metadata,'$.mc1_sealed') IS NOT NULL":
                [('events.metadata', 'key organizer')],
            "SELECT 1 FROM events WHERE metadata LIKE ?": [('events.metadata', 'text')],
            "SELECT 1 FROM events WHERE instr(metadata,?)": [('events.metadata', 'text')],
            "SELECT 1 FROM events WHERE json_extract(metadata,?)=?": [('events.metadata', 'key ?')],
            "SELECT 1 FROM events WHERE json_extract(metadata,'$.\x00')=?": [('events.metadata', 'key ?')],
            "SELECT 1 FROM action_jobs WHERE json_extract(payload,'$.finish_result.state')='completed'": [('action_jobs.payload', 'key finish_result')],
            "SELECT 1 FROM suggestions s JOIN agent_jobs j ON j.id=s.id WHERE json_extract(s.outcome,'$.follow_up')='stop'": [('suggestions.outcome', 'key follow_up')],
            "CREATE INDEX i ON events(json_extract(metadata,'$.sender_id'))": [('events.metadata', 'key sender_id')],
            "SELECT 1 FROM events WHERE json_extract(\x00,'$.cc')=?": [('?', 'column ?')],
        }
        for text, expected in caught.items():
            self.assertEqual(reads(text), expected, text)
        # the table can be named in another string of the same statement
        self.assertEqual(reads("AND json_extract(payload,'$.to')=?", "SELECT 1 FROM action_jobs WHERE status=? AND json_extract(payload,'$.to')=?"),
                         [('action_jobs.payload', 'key to')])
        for text in ("SELECT 1 FROM events WHERE json_extract(metadata,'$.thread_id')=?",
                     # a routing key (message_seal.ROUTING_KEYS), with the rows sealed before it was plain
                     "SELECT 1 FROM events WHERE json_extract(metadata,'$.chat_kind')='group' OR (json_extract(metadata,'$.chat_kind') IS NULL "
                     "AND json_extract(metadata,'$.mc1_sealed') IS NOT NULL)",
                     "SELECT 1 FROM events WHERE CAST(json_extract(metadata,'$.end_at') AS TEXT)>? AND metadata->>'status'!='cancelled'",
                     "SELECT 1 FROM events e, json_each(json_extract(e.metadata,'$.labels')) l WHERE l.value=?",
                     """SELECT 1 FROM events WHERE instr(metadata,'"SENT"')""",
                     "CREATE INDEX i ON events(json_extract(metadata,'$.conversation_id'))",
                     "SELECT metadata FROM events WHERE metadata IS NOT NULL",
                     "SELECT 1 FROM action_jobs WHERE json_extract(payload,'$.kind')='finish'",
                     "SELECT 1 FROM suggestions WHERE json_extract(outcome,'$.state')='already_done'",
                     "SELECT 1 FROM notify_queue WHERE json_extract(payload,'$.title')=?",
                     "SELECT 1 FROM agent_jobs j WHERE json_extract(j.outcome,'$.summary')=?",
                     "the metadata of an event, like its cc"):
            self.assertEqual(reads(text), [], text)

    def source_database(self, db):
        """Every table the source can make, whenever it makes it, with every column: a table the Store's own start does
        not make was never looked at here, and notify_queue kept to-do titles plain."""
        missing = make_source_tables(db)
        self.assertEqual(missing, set(), 'a table the source names was not made here: this check cannot see its columns')
        built = {p.relative_to(ROOT).as_posix() for p in source_modules() if BUILT.search(p.read_text(encoding='utf-8'))}
        self.assertEqual(built - {'machine/store/core.py'}, set(ENSURED), 'an ALTER TABLE put together at run time: its module has to be in ENSURED')
        for name in ENSURED.values():
            importlib.import_module(name).ensure(db)

    def test_every_text_column_is_sealed_or_plain_for_a_reason(self):
        """A new text column has to be sealed (message_seal.DERIVED) or listed in plain_columns, as a code (which is
        checked: the guard below) or as words that stay plain, with why."""
        with tempfile.TemporaryDirectory() as temp:
            with machine_main.Store(Path(temp) / 'events.sqlite').connect() as db:
                self.source_database(db)
                every = {f'{t}.{c}' for t, cs in plain_columns.columns(db).items() for c in cs}
        sealed, codes, words = plain_columns.sealed_names(), set(plain_columns.CODES.split()), plain_columns.worded()
        named = {name for name in every if plain_columns.CODE_NAME.search(name)}
        self.assertEqual(sorted(every - sealed - codes - words - named), [], 'seal it (message_seal.DERIVED), or say in plain_columns why it may stay plain')
        self.assertEqual(sorted((codes | words) - every), [], 'no such column any more')
        self.assertEqual(sorted((codes & words) | (sealed & (codes | words)) | (codes & named)), [], 'listed twice')

    def test_words_written_to_a_code_column_are_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            with machine_main.Store(Path(temp) / 'events.sqlite').connect() as db:
                plain_columns.guard(db)
                db.execute("INSERT INTO todo_moves(suggestion_id,from_status,to_status,reason,at) VALUES('s','pending','done','owner_done','t')")
                for reason in ('she wrote that she signs on Monday', json.dumps({'why': 'she wrote that she signs'})):
                    with self.assertRaisesRegex(sqlite3.IntegrityError, 'a plain column of todo_moves holds words'):
                        db.execute('UPDATE todo_moves SET reason=?', (reason,))
                db.execute('UPDATE todo_moves SET reason=?', (json.dumps({'ids': [1, 2, 3, 4, 5], 'a': 'b', 'c': 'd', 'e': 'f'}),))  # JSON of codes

    def test_the_suites_that_write_most_run_with_that_guard(self):
        runner = (ROOT / 'scripts' / 'test.py').read_text(encoding='utf-8')
        checked = re.findall(r'\w+', re.search(r'^PLAIN_CHECKED = \((.*?)\)', runner, re.M)[1])
        self.assertTrue(checked)
        for stem in checked:
            self.assertTrue((ROOT / 'tests' / (stem + '.py')).is_file(), stem)
        self.assertIn("'plain_columns' if file.stem in PLAIN_CHECKED else 'unittest'", runner)

    def test_connectors_store_only_through_the_sealed_path(self):
        for path in sorted((ROOT / 'connectors').glob('*.py')) + sorted((ROOT / 'integrations').glob('*.py')):
            text = path.read_text()
            with self.subTest(path=path.name):
                self.assertNotRegex(text, r'\bsqlite3\b|INSERT\s+INTO|UPDATE\s+\w+\s+SET')
        # every module, subfolders included, so code moved into a folder stays covered. The sandbox's fixture loader
        # writes made-up events into a throwaway database through Store.connect(), so they are sealed as the app's are.
        allowed = {'machine/main.py', 'machine/store/cards.py', 'machine/store/core.py', 'machine/store/events.py',
                   'machine/store/machine_cards.py', 'machine/store/review.py', 'sandbox/load.py'}  # the Store and App (machine/main.py) and the Store's parts
        modules = [p for p in sorted(ROOT.rglob('*.py'))
                   if not {'tests', 'node_modules', '.git', '.venv'} & set(p.relative_to(ROOT).parts[:-1]) and not p.name.startswith('test_')]
        self.assertIn(ROOT / 'connectors' / 'x.py', modules)
        writes = [f'{p.relative_to(ROOT).as_posix()}: {m.group(0)}' for p in modules
                  for m in re.finditer(r'(INSERT(?: OR \w+)? INTO|UPDATE) events\b', p.read_text(encoding='utf-8'))
                  if p.relative_to(ROOT).as_posix() not in allowed]
        self.assertEqual(writes, [])

    def test_a_connector_putting_message_text_in_a_plain_field_is_caught(self):
        leaky = event(1, 'new.connector', {'thread_id': 'Dear owner the zanzibarquill contract is ready'})
        self.assertEqual(message_seal.plain_leaks(leaky), ['metadata.thread_id'])
        self.assertEqual(message_seal.plain_leaks(event(1, 'new.connector'), {'cursor': 'abc'}), [])
        self.assertEqual(message_seal.plain_leaks(event(1, 'x'), {'last': 'the zanzibarquill contract is ready'}), ['cursor'])

    def test_every_connector_is_tested_with_the_seal_audit_on(self):
        """A connector in connectors/ is tested by its own test_connector_<name>.py, which the runner audits by its name,
        or names its suite in SEAL_COVERED_BY. A new connector with neither fails here, so none is left out by hand."""
        spec = importlib.util.spec_from_file_location('test_runner', ROOT / 'scripts' / 'test.py')
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        audited = set(runner.SEAL_AUDIT)
        connectors = sorted(p.stem for p in (ROOT / 'connectors').glob('*.py') if not p.stem.startswith('_'))
        self.assertTrue(connectors)
        unaudited = [name for name in connectors
                     if f'test_connector_{name}' not in audited and runner.SEAL_COVERED_BY.get(name) not in audited]
        self.assertEqual(unaudited, [], 'add tests/test_connector_<name>.py, or name its suite in SEAL_COVERED_BY (scripts/test.py)')
        self.assertLessEqual({p.stem for p in (ROOT / 'tests').glob('test_connector_*.py')}, audited)
        self.assertEqual(sorted(set(runner.SEAL_COVERED_BY) - set(connectors)), [], 'SEAL_COVERED_BY names a connector that is gone')

    def test_every_connector_keeps_message_text_in_the_sealed_fields(self):
        """The connector suites again, with commit_page refusing any event whose text shows in a plain field. The test
        runner (scripts/test.py) runs them so itself, so there this would only run them twice."""
        spec = importlib.util.spec_from_file_location('test_runner', ROOT / 'scripts' / 'test.py')
        runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
        suites = list(runner.SEAL_AUDIT)
        self.assertTrue(all((ROOT / 'tests' / f'{suite}.py').exists() for suite in suites), suites)
        if os.environ.get('THE_MACHINE_SEAL_AUDITED', '').split(',') == suites:
            self.skipTest('scripts/test.py runs the connector suites with MESSAGE_SEAL_AUDIT=1 itself')
        result = subprocess.run([sys.executable, '-m', 'unittest', *suites], cwd=ROOT, capture_output=True, text=True, timeout=900,
                                env={**os.environ, 'MESSAGE_SEAL_AUDIT': '1'})
        self.assertNotIn('keeps message text in the clear', result.stderr)
        self.assertEqual(result.returncode, 0, result.stderr[-3000:])


if __name__ == '__main__':
    unittest.main()

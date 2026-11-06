"""After an import (machine/export/hold.py): nothing goes out by itself, and what happened before the export never comes
back as a new signal (the history line, machine/store/history.py, read by Store.commit_page). Synthetic data only."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing

sys.path.insert(0, str(Path(__file__).parent))
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_export_hold', Path(__file__).parent.parent / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
from machine.export import hold  # noqa: E402
import moving  # noqa: E402

NOW = '2026-11-06T09:00:00+00:00'
EXPORTED = '2026-11-01T12:00:00+00:00'
MAIL = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}


def mail(n, at, subject='Quarterly numbers'):
    import datetime as dt
    stamp = int(dt.datetime.fromisoformat(at).timestamp() * 1000)
    return {'id': f'm{n}', 'threadId': f't{n}', 'internalDate': str(stamp), 'labelIds': ['INBOX'],
            'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'Subject', 'value': subject},
                                                              {'name': 'From', 'value': 'Sam <sam@example.org>'},
                                                              {'name': 'To', 'value': 'owner@example.com'}],
                        'body': {'data': a.base64.urlsafe_b64encode(b'Here are the numbers.').decode()}}}


class HistoryLine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        clock = patch_everywhere(a, 'now', return_value=NOW); clock.start(); self.addCleanup(clock.stop)

    def rows(self):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute('SELECT source_id,history,version,analyzed_version FROM events ORDER BY source_id')]

    def test_before_an_import_every_new_row_is_a_signal(self):
        self.store.commit_page(MAIL['id'], {}, [a.message_event(MAIL, mail(1, '2026-10-01T10:00:00+00:00'))])
        self.assertEqual([('m1', 0, 1, 0)], self.rows())

    def test_after_an_import_what_came_before_it_is_history(self):
        self.store.commit_page(MAIL['id'], {}, [a.message_event(MAIL, mail(1, '2026-10-01T10:00:00+00:00'))])
        with self.store.connect() as db:
            hold.hold(db, NOW, EXPORTED)
        # Google signed in again after the move: the mailbox is read again from the start
        self.store.commit_page(MAIL['id'], {}, [a.message_event(MAIL, mail(1, '2026-10-01T10:00:00+00:00', 'Quarterly numbers, relabeled')),
                                                a.message_event(MAIL, mail(2, '2026-10-20T10:00:00+00:00', 'Older, never read here')),
                                                a.message_event(MAIL, mail(3, '2026-11-05T10:00:00+00:00', 'New since the move'))])
        rows = self.rows()
        self.assertEqual(('m1', 0, 2, 2), rows[0])  # an edit of an old signal: kept, never reviewed again
        self.assertEqual(('m2', 1, 1, 1), rows[1])  # older than the export, only seen now: history
        self.assertEqual(('m3', 0, 1, 0), rows[2])  # after the export: a signal, as always


class Hold(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')

    def test_queued_sends_wait_and_sending_ones_are_never_resent(self):
        with self.store.connect() as db:
            for job, status in (('q', 'queued'), ('s', 'sending'), ('d', 'sent')):
                db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                           "VALUES(?,?,?,?,?,?,?,?,?,?)", (job, 'card-' + job, 'r', json.dumps({'kind': 'email'}), status, NOW, NOW, 'a', 'card', '<x@example>'))
            held = hold.hold(db, NOW, EXPORTED)
            found = dict(db.execute('SELECT id,status FROM action_jobs').fetchall())
        self.assertEqual({'q': 'blocked', 's': 'uncertain', 'd': 'sent'}, found)
        self.assertEqual(1, held['sends'])
        self.assertEqual(1, held['sends_unsure'])

    def test_without_keys_old_tokens_go_and_with_keys_they_stay(self):
        with self.store.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS ai_tokens(hash TEXT PRIMARY KEY,kind TEXT NOT NULL,connection_id TEXT NOT NULL,client_id TEXT,"
                       "code_hash TEXT,expires_at TEXT NOT NULL,used_at TEXT,created_at TEXT NOT NULL)")
            db.execute("INSERT INTO ai_tokens(hash,kind,connection_id,expires_at,created_at) VALUES('h','access','c','2027-01-01',?)", (NOW,))
            hold.hold(db, NOW, EXPORTED, keys=True)
            self.assertEqual(1, db.execute('SELECT count(*) FROM ai_tokens').fetchone()[0])
            hold.hold(db, NOW, EXPORTED, keys=False)
            self.assertEqual(0, db.execute('SELECT count(*) FROM ai_tokens').fetchone()[0])

    def test_telegram_outbox_stops(self):
        with closing(sqlite3.connect(Path(self.tmp.name) / 'telegram.sqlite')) as db, db:
            db.execute("CREATE TABLE outbox(id TEXT PRIMARY KEY, op TEXT NOT NULL, chat_id TEXT, text BLOB, approval TEXT, created_at TEXT NOT NULL,"
                       " status TEXT NOT NULL DEFAULT 'queued', msg_id INTEGER, error TEXT, done_at TEXT)")
            db.execute("INSERT INTO outbox(id,op,chat_id,created_at) VALUES('t','send','1',?)", (NOW,))
            self.assertEqual(1, hold.hold_telegram(db, NOW))
            self.assertEqual('held', db.execute('SELECT status FROM outbox').fetchone()[0])


class Staged(unittest.TestCase):
    """A hosted Machine's dashboard stages an upload (moving.stage); its server applies it with the service stopped."""

    def test_stage_checks_at_once_and_apply_puts_it_in_place(self):
        tmp = Path(tempfile.mkdtemp(prefix='export-stage-'))
        self.addCleanup(__import__('portable').shred_tree, tmp)
        data = tmp / 'old/data'
        data.mkdir(parents=True)
        config = data / 'config.json'
        config.write_text(json.dumps({'database': str(data / 'events.sqlite'), 'accounts': [{'id': 'm', 'service': 'gmail', 'transport': 'gog'}]}))
        a.Store(data / 'events.sqlite')
        claw = tmp / 'old/.openclaw'
        claw.mkdir()
        archive, _ = moving.export(config, tmp / 'out', passphrase='a long synthetic passphrase', workspace=tmp / 'none', openclaw_home=claw)
        target = tmp / 'new/data/config.json'
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps({'manage_url': 'https://manage.example.test', 'accounts': [{'id': 'h', 'service': 'gmail', 'transport': 'broker'}],
                                      'credentials': {'google-broker': str(target.parent / 'machine-token')}}))
        with self.assertRaisesRegex(moving.MoveError, 'Wrong export code or passphrase'):
            moving.stage(archive, target, 'not the right one')
        self.assertIsNone(moving.staged(target))
        summary = moving.stage(archive, target, 'a long synthetic passphrase')
        self.assertIn('messages', summary['parts'])
        self.assertTrue(moving.staged(target))
        result = moving.apply_staged(target, workspace=tmp / 'new/ws', openclaw_home=tmp / 'new/.openclaw', force=True, keep_hosted=True)
        self.assertIsNone(moving.staged(target))
        placed = json.loads(target.read_text())
        self.assertEqual('https://manage.example.test', placed['manage_url'])  # the hosted settings stay
        self.assertEqual(str(target.parent / 'machine-token'), placed['credentials']['google-broker'])
        self.assertEqual(['m'], [x['id'] for x in placed['accounts']])
        self.assertTrue((target.parent / 'events.sqlite').is_file())
        self.assertIn('held', result)


if __name__ == '__main__':
    unittest.main()

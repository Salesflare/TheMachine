"""The round trip (moving.py, machine/export/): a fully seeded install is exported, imported into a fresh one, and
every table and every file is compared. They must be the same, apart from the documented exceptions (EXCEPTIONS,
docs/moving.md): what an import holds so nothing goes out by itself, and the new install's own sign-ins.

Everything here is synthetic: the sandbox's made-up install (sandbox/load.py) plus made-up OpenClaw conversations,
photos, send logs and agent transcripts. Nothing is read from or written to this computer's own home folder."""
import datetime as dt
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import unittest
from contextlib import closing

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import message_seal  # noqa: E402
import moving  # noqa: E402
from machine.export import hold, home as elsewhere, inventory  # noqa: E402

PASSPHRASE = 'a synthetic passphrase for tests'
# What an import changes on purpose, by table: the rows are compared without these columns, and each change is
# checked on its own in the tests below.
EXCEPTIONS = {
    'action_jobs': ('status', 'error', 'retry_at', 'updated_at'),   # queued sends wait for the owner
    'deliveries': ('needs_edit',),                                   # their to-dos show Send again
    'agent_jobs': ('status', 'error', 'error_kind', 'progress', 'updated_at', 'finished_at'),  # local jobs stop, work kept
    'activity_blocks': None,                                         # the hold's line, per held send
    'follow_up_pauses': None,                                        # automated follow-ups paused
    'notify_queue': None,                                            # notifications for the old Machine dropped
    'ai_tokens': None, 'ai_codes': None, 'push_subscriptions': None,  # tokens for the old address, without keys
    'moved_in': None,                                                # the history line
    'outbox': ('status', 'error', 'done_at'),                        # Telegram sends wait for the owner
}
OLD = '2026-10-01T09:00:00+00:00'


def tables_of(path):
    """{table: [row as a tuple]} of a database, message text opened with its own key (when it has one)."""
    key = message_seal.load_key(path)
    out = {}
    with closing(inventory.connect(path, key)) as db:
        for table, virtual in inventory.tables(db):
            if not virtual:
                out[table] = [dict(r) for r in inventory.rows(db, table)]
    return out


def files_of(root, skip=()):
    out = {}
    for path in sorted(Path(root).rglob('*')):
        rel = str(path.relative_to(root))
        if path.is_file() and not any(rel == s or rel.startswith(s + '/') for s in skip):
            out[rel] = path.read_bytes()
    return out


class RoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix='export-roundtrip-'))
        cls.old_home, cls.new_home = cls.tmp / 'old', cls.tmp / 'new'
        cls.data = cls.old_home / '.local/share/personal-assistant'
        env = {**os.environ, 'HOME': str(cls.old_home)}
        env.pop('CLAUDE_CONFIG_DIR', None)
        env.pop('CODEX_HOME', None)
        subprocess.run([sys.executable, str(ROOT / 'sandbox/load.py'), '--dir', str(cls.data), '--state', 'all'],
                       check=True, env=env, cwd=str(ROOT), capture_output=True, timeout=900)
        cls.config = cls.data / 'config.json'
        cls.seed_extra()
        cls.before = {name: tables_of(path) for name, path in inventory.databases(cls.config)}
        cls.archive, cls.manifest = moving.export(cls.config, cls.tmp / 'out', passphrase=PASSPHRASE,
                                                  workspace=cls.old_home / '.openclaw/workspace',
                                                  openclaw_home=cls.old_home / '.openclaw', source='local')
        cls.seed_new_install()
        cls.new_config = cls.new_home / '.local/share/personal-assistant/config.json'
        cls.result = moving.import_(cls.archive, cls.new_config, passphrase=PASSPHRASE,
                                    workspace=cls.new_home / '.openclaw/workspace', openclaw_home=cls.new_home / '.openclaw')
        cls.after = {name: tables_of(path) for name, path in inventory.databases(cls.new_config)}

    @classmethod
    def seed_extra(cls):
        """What the sandbox doesn't have: OpenClaw's conversations, pending work, photos, send logs, transcripts."""
        old, data = cls.old_home, cls.data
        with closing(sqlite3.connect(data / 'events.sqlite')) as db, db:
            db.execute("INSERT INTO action_jobs(id,suggestion_id,revision,payload,status,created_at,updated_at,approval_id,source,rfc_message_id) "
                       "SELECT 'job-queued',id,'r1','{\"kind\":\"email\"}','queued',?,?,'a1','card','<synthetic@example>' FROM suggestions LIMIT 1", (OLD, OLD))
            db.execute("INSERT INTO deliveries(suggestion_id,status,updated_at) SELECT suggestion_id,'queued',? FROM action_jobs "
                       "WHERE id='job-queued' AND suggestion_id NOT IN (SELECT suggestion_id FROM deliveries)", (OLD,))
            db.execute("UPDATE agent_jobs SET status='running',place='local',session_id='0f0f0f0f-1111-2222-3333-444455556666',tool='claude'")
            db.execute("INSERT INTO ai_tokens(hash,kind,connection_id,expires_at,created_at) VALUES('h1','access','c1','2027-01-01',?)", (OLD,))
            db.execute("CREATE TABLE IF NOT EXISTS notify_queue(id INTEGER PRIMARY KEY,channel TEXT NOT NULL,kind TEXT NOT NULL,ref TEXT,"
                       "title TEXT NOT NULL,payload TEXT,show INTEGER NOT NULL DEFAULT 1,created REAL NOT NULL,due REAL NOT NULL)")
            db.execute("INSERT INTO notify_queue(channel,kind,title,created,due) VALUES('push','todo','A synthetic notice',1,2)")
            board = db.execute('SELECT id FROM boards LIMIT 1').fetchone()[0]
            db.execute("INSERT OR REPLACE INTO follow_up_rules(scope,ref,settings,updated_at) VALUES('board',?,'{\"on\": true}',?)", (board, OLD))
            cls.board = board
        store = data / 'telegram/home-telegram'
        store.mkdir(parents=True)
        (store / 'session.sealed').write_bytes(b'synthetic session')
        with closing(sqlite3.connect(store / 'telegram.sqlite')) as db, db:
            db.execute("CREATE TABLE outbox(id TEXT PRIMARY KEY, op TEXT NOT NULL, chat_id TEXT, text BLOB, approval TEXT, created_at TEXT NOT NULL,"
                       " status TEXT NOT NULL DEFAULT 'queued', msg_id INTEGER, error TEXT, done_at TEXT)")
            db.execute("INSERT INTO outbox(id,op,chat_id,text,created_at) VALUES('t1','send','42','Synthetic hello',?)", (OLD,))
        (data / 'chat-files').mkdir(exist_ok=True)
        (data / 'chat-files/photo.jpg').write_bytes(b'\xff\xd8synthetic photo')
        (data / 'agent-jobs/7/work').mkdir(parents=True)
        (data / 'agent-jobs/7/work/notes.md').write_text('Synthetic work\n')
        (data / 'agent-jobs/7/turn-1.jsonl').write_text('{"type":"result"}\n')
        claw = old / '.openclaw'
        (claw / 'workspace/memory').mkdir(parents=True)
        (claw / 'workspace/USER.md').write_text('A synthetic owner\n')
        (claw / 'workspace/memory/2026-10-01.md').write_text('A synthetic memory\n')
        (claw / 'agents/main/sessions').mkdir(parents=True)
        (claw / 'agents/main/sessions/abc.jsonl').write_text('{"role":"user","text":"synthetic"}\n')
        (claw / 'agents/main/sessions/old.jsonl.deleted.2026-10-01T00-00-00.000Z.zst').write_bytes(b'deleted')
        (claw / 'agents/main/agent').mkdir(parents=True)
        with closing(sqlite3.connect(claw / 'agents/main/agent/openclaw-agent.sqlite')) as db, db:
            db.execute('CREATE TABLE transcript_events(id INTEGER PRIMARY KEY, session TEXT, body TEXT)')
            db.execute("INSERT INTO transcript_events(session,body) VALUES('abc','A synthetic conversation')")
            db.execute('CREATE TABLE auth_profile_store(id TEXT PRIMARY KEY, value TEXT)')
            db.execute("INSERT INTO auth_profile_store VALUES('old','old-sign-in')")
        (claw / 'state').mkdir()
        with closing(sqlite3.connect(claw / 'state/openclaw.sqlite')) as db, db:
            db.execute('CREATE TABLE cron_jobs(id TEXT PRIMARY KEY, spec TEXT)')
            db.execute("INSERT INTO cron_jobs VALUES('morning','0 8 * * *')")
            db.execute('CREATE TABLE secret_store_entries(id TEXT PRIMARY KEY, value TEXT)')
            db.execute("INSERT INTO secret_store_entries VALUES('k','synthetic-secret')")
        (claw / 'media/inbound').mkdir(parents=True)
        (claw / 'media/inbound/photo.png').write_bytes(b'\x89PNG synthetic')
        (claw / 'media/browser').mkdir(parents=True)
        (claw / 'media/browser/shot.png').write_bytes(b'cache')
        (old / '.local/share/x-inbox').mkdir(parents=True)
        (old / '.local/share/x-inbox/sends.jsonl').write_text('{"sent":"synthetic"}\n')
        folder = '-' + str(data / 'agent-jobs/7/work').strip('/').replace('/', '-').replace('.', '-')
        (old / '.claude/projects' / folder).mkdir(parents=True)
        (old / '.claude/projects' / folder / '0f0f0f0f-1111-2222-3333-444455556666.jsonl').write_text('{"synthetic":true}\n')

    @classmethod
    def seed_new_install(cls):
        """A fresh install: an empty data folder and OpenClaw with its own sign-in."""
        agent = cls.new_home / '.openclaw/agents/main/agent'
        agent.mkdir(parents=True)
        with closing(sqlite3.connect(agent / 'openclaw-agent.sqlite')) as db, db:
            db.execute('CREATE TABLE transcript_events(id INTEGER PRIMARY KEY, session TEXT, body TEXT)')
            db.execute('CREATE TABLE auth_profile_store(id TEXT PRIMARY KEY, value TEXT)')
            db.execute("INSERT INTO auth_profile_store VALUES('new','this-computers-sign-in')")

    @classmethod
    def tearDownClass(cls):
        portable_tree = __import__('portable').shred_tree
        portable_tree(cls.tmp)

    # --- the manifest --------------------------------------------------------------------------------------------

    def test_manifest_lists_every_part_with_counts_and_checksums(self):
        manifest = self.manifest
        self.assertEqual(moving.FORMAT, manifest['format'])
        self.assertNotIn('other', manifest['parts'], 'a file or table without a part: add it to machine/export/inventory.py')
        for part in ('messages', 'todos', 'drafts', 'promises', 'graph', 'conversations', 'attachments', 'agents', 'workspace'):
            self.assertIn(part, manifest['parts'])
        events = manifest['tables']['events.sqlite/events']
        self.assertEqual(len(self.before['events.sqlite']['events']), events['rows'])
        self.assertEqual(64, len(events['sha256']))
        for entry, found in manifest['files'].items():
            self.assertEqual(64, len(found['sha256']), entry)
        whats = ' '.join(x['what'] for x in manifest['not_exported'])
        self.assertIn('WhatsApp', whats)
        self.assertIn('deleted', whats)
        self.assertTrue(all(x['why'] for x in manifest['not_exported']))

    def test_no_keys_or_tokens_without_asking(self):
        self.assertFalse(self.manifest['includes_keys'])
        names = set(self.manifest['files'])
        self.assertFalse([n for n in names if n.startswith('secrets/')])
        self.assertNotIn('data/telegram/home-telegram/session.sealed', names)
        self.assertNotIn('data/owner-token', names)
        self.assertNotIn('data/message-content.key', names)
        plain = self.tmp / 'peek.tar.gz'
        moving._openssl(['-in', str(self.archive), '-out', str(plain)], PASSPHRASE, decrypt=True)
        with tarfile.open(plain, 'r:gz') as archive:
            agent = archive.extractfile('openclaw/agents/main/agent/openclaw-agent.sqlite').read()
        plain.unlink()
        self.assertNotIn(b'old-sign-in', agent)
        self.assertIn(b'A synthetic conversation', agent)

    def test_keys_need_a_passphrase(self):
        with self.assertRaises(moving.MoveError):
            moving.export(self.config, self.tmp / 'out2', keys=True, workspace=self.old_home / '.openclaw/workspace',
                          openclaw_home=self.old_home / '.openclaw')

    # --- every table ---------------------------------------------------------------------------------------------

    def test_every_table_comes_back_the_same(self):
        self.assertEqual(set(self.before), set(self.after))
        for name, tables in self.before.items():
            for table, rows in tables.items():
                with self.subTest(db=name, table=table):
                    self.assertIn(table, self.after[name])
                    skip = EXCEPTIONS.get(table, ())
                    if skip is None:
                        continue
                    strip = lambda found: [{k: v for k, v in r.items() if k not in skip} for r in found]
                    self.assertEqual(strip(rows), strip(self.after[name][table]))
        added = {(name, t) for name in self.after for t in self.after[name]} - {(name, t) for name in self.before for t in self.before[name]}
        self.assertEqual(set(), {t for _, t in added} - set(EXCEPTIONS), 'an import made a table the export did not have')

    def test_ids_links_and_times_stay(self):
        before, after = self.before['events.sqlite'], self.after['events.sqlite']
        self.assertEqual([(r['id'], r['occurred_at'], r['ingested_at']) for r in before['events']],
                         [(r['id'], r['occurred_at'], r['ingested_at']) for r in after['events']])
        self.assertEqual([(r['id'], r['created_at']) for r in before['suggestions']], [(r['id'], r['created_at']) for r in after['suggestions']])

    # --- every file ----------------------------------------------------------------------------------------------

    def test_every_file_comes_back_the_same(self):
        data_after = self.new_config.parent
        secret = {kind_path[2][len('secrets/data/'):] for kind_path in moving.plan(self.config, openclaw_home=self.old_home / '.openclaw')
                  if kind_path[0] == 'secret' and kind_path[2].startswith('secrets/data/')}
        before = {k: v for k, v in files_of(self.data).items() if not k.endswith(('.sqlite', '-wal', '-shm')) and k not in secret
                  and k != 'message-content.key' and k != 'config.json'}
        after = files_of(data_after)
        for name, content in before.items():
            with self.subTest(file=name):
                self.assertEqual(content, after.get(name))
        self.assertNotIn('telegram/home-telegram/session.sealed', after)
        new, old = self.new_home, self.old_home
        for rel in ('.openclaw/workspace/USER.md', '.openclaw/workspace/memory/2026-10-01.md', '.openclaw/agents/main/sessions/abc.jsonl',
                    '.openclaw/media/inbound/photo.png', '.local/share/x-inbox/sends.jsonl'):
            with self.subTest(file=rel):
                self.assertEqual((old / rel).read_bytes(), (new / rel).read_bytes())
        self.assertFalse(list((new / '.openclaw/agents/main/sessions').glob('*.deleted.*')))
        self.assertFalse((new / '.openclaw/media/browser').exists())

    def test_agent_transcripts_follow_the_job_folder(self):
        found = list((self.new_home / '.claude/projects').glob('*/0f0f0f0f-1111-2222-3333-444455556666.jsonl'))
        self.assertEqual(1, len(found))
        moved = '-' + str(self.new_config.parent / 'agent-jobs/7/work').strip('/').replace('/', '-').replace('.', '-')
        self.assertEqual(moved, found[0].parent.name)

    def test_openclaw_conversations_come_with_the_new_sign_ins(self):
        path = self.new_home / '.openclaw/agents/main/agent/openclaw-agent.sqlite'
        with closing(sqlite3.connect(path)) as db:
            self.assertEqual([('A synthetic conversation',)], db.execute('SELECT body FROM transcript_events').fetchall())
            self.assertEqual([('new', 'this-computers-sign-in')], db.execute('SELECT * FROM auth_profile_store').fetchall())
        with closing(sqlite3.connect(self.new_home / '.openclaw/state/openclaw.sqlite')) as db:
            self.assertEqual([('morning', '0 8 * * *')], db.execute('SELECT * FROM cron_jobs').fetchall())
            self.assertEqual([], db.execute('SELECT * FROM secret_store_entries').fetchall())

    # --- nothing goes out, nothing old comes back ----------------------------------------------------------------

    def test_nothing_is_sent_by_itself(self):
        after = self.after['events.sqlite']
        job = next(r for r in after['action_jobs'] if r['id'] == 'job-queued')
        self.assertEqual(('blocked', hold.MOVED_SEND), (job['status'], job['error']))
        self.assertFalse([r for r in after['action_jobs'] if r['status'] in ('queued', 'sending')])
        self.assertEqual(['failed'], sorted({r['status'] for r in after['agent_jobs']}))
        self.assertEqual('moved', after['agent_jobs'][0]['error_kind'])
        self.assertEqual([], after['notify_queue'])
        self.assertEqual([], after['ai_tokens'])
        self.assertTrue([r for r in after['follow_up_pauses'] if r['ref'] == self.board and r['end_at'] is None])
        tg = self.after[next(n for n in self.after if n.endswith('telegram.sqlite'))]['outbox']
        self.assertEqual(['held'], [r['status'] for r in tg])
        self.assertGreaterEqual(self.result['held']['sends'], 1)

    def test_the_history_line_is_the_exports_moment(self):
        moved = self.after['events.sqlite']['moved_in']
        self.assertEqual([self.manifest['created_at']], [r['since'] for r in moved])
        from machine.store import history
        line = dt.datetime.fromisoformat(self.manifest['created_at'])
        self.assertTrue(history.from_before(OLD, line))
        self.assertFalse(history.from_before((line + dt.timedelta(minutes=1)).isoformat(), line))
        self.assertFalse(history.from_before('not a time', line))

    def test_a_damaged_export_imports_nothing(self):
        damaged = self.tmp / 'damaged.tar.gz'
        plain = self.tmp / 'plain.tar.gz'
        moving._openssl(['-in', str(self.archive), '-out', str(plain)], PASSPHRASE, decrypt=True)
        with tarfile.open(plain, 'r:gz') as source, tarfile.open(damaged, 'w:gz') as target:
            for member in source.getmembers():
                data = source.extractfile(member).read() if member.isfile() else None
                if member.name == '.openclaw' or member.name.endswith('USER.md'):
                    data = b'changed on the way'
                    member.size = len(data)
                target.addfile(member, __import__('io').BytesIO(data) if data is not None else None)
        plain.unlink()
        config = self.tmp / 'third/data/config.json'
        with self.assertRaises(moving.MoveError):
            moving.import_(damaged, config, workspace=self.tmp / 'third/ws', openclaw_home=self.tmp / 'third/.openclaw')
        self.assertFalse(config.exists())


if __name__ == '__main__':
    unittest.main()

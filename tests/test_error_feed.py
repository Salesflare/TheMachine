"""Error reports for The Machine team (error_feed.py): each error becomes a signature (type, normalized message, place
in The Machine's own code, version, count), deduplicated and rate-limited here, sent in batches over the Network, and
nothing at all once the owner turns it off. The Network is a stand-in here: nothing is sent anywhere."""
import datetime as dt
import importlib.util
import json
import logging
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

import agent_jobs
import error_feed as ef

spec = importlib.util.spec_from_file_location('error_feed_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

JWT = '.'.join(['eyJ' + 'hbGciOiJIUzI1NiJ9', 'eyJ' + 'zdWIiOiIxMjM0NTY3ODkwIn0', 'c2lnbmF0dXJlLXNpZ25hdHVyZQ'])  # made up
NOW = dt.datetime(2026, 10, 27, 9, 0, tzinfo=dt.timezone.utc)
SECRETS = ('sam.lee@globex.example', 'ghp_abcdefghijklmnopqrstuvwxyz0123456789', 'sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz',
           JWT, 'Hi Sam, the contract is attached',
           '/home/jeroen', 'jeroen', 'Globex', 'Sam', 'Lee', 'C:\\Users\\Marie', 'Marie', '+32 470 12 34 56', '4111111111111111',
           'https://globex.example/deal/42?token=abc', 'globex.example', 'hunter2', 'Müller', 'Zoë')
ATTEMPTS = (
    'Failed to send to sam.lee@globex.example: 550 rejected',
    'GitHub said 401 for token ghp_abcdefghijklmnopqrstuvwxyz0123456789',
    'Authorization: Bearer sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz',
    f'bad jwt {JWT}',
    'could not parse reply "Hi Sam, the contract is attached" from the draft',
    "KeyError on 'Hi Sam, the contract is attached'",
    'No such file or directory: /home/jeroen/.openclaw/workspace/memory/2026-10-27.md',
    'cannot open C:\\Users\\Marie\\AppData\\Local\\x.db',
    'person Sam Lee at Globex has no email',
    'Müller and Zoë have no role',
    'call +32 470 12 34 56 failed, card 4111111111111111',
    'fetch https://globex.example/deal/42?token=abc timed out; see globex.example',
    'password=hunter2 rejected',
)


class Network:
    def __init__(self):
        self.sent, self.fail = [], False

    def call(self, method, path, body=None, timeout=40):
        assert (method, path) == ('POST', '/errors'), (method, path)
        if self.fail:
            raise OSError('away')
        self.sent.append(json.loads(json.dumps(body)))
        return {'ok': True, 'taken': len(body['signatures'])}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'a.sqlite'
        self.net = Network()

    def tearDown(self):
        self.tmp.cleanup()

    def connect(self):
        db = sqlite3.connect(self.path)
        return _Tx(db)

    def rec(self, message='list index out of range', kind='IndexError', function='review_step', line=12, at=None, source='service'):
        with self.connect() as db:
            return ef.record(db, source, kind, message, 'assistant.py', function, line, 'abc123def456', at=(at or NOW).isoformat())

    def send(self, at=NOW, names=()):
        return ef.send(self.connect, self.net.call, names, current=at)


class _Tx:
    """sqlite3's connection as a context manager that commits and closes, like Store.connect."""
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, kind, *_):
        with closing(self.db):
            if kind is None:
                self.db.commit()


class Scrub(Base):
    def test_nothing_private_survives(self):
        for attempt in ATTEMPTS:
            with self.subTest(attempt=attempt):
                out = ef.normalize(attempt, names=['Sam', 'Lee', 'Globex', 'jeroen'])
                self.assertTrue(ef.allowed(out), out)
                for secret in SECRETS:
                    self.assertNotIn(secret.lower(), out.lower(), f'{secret!r} leaked from {attempt!r}: {out!r}')

    def test_a_capitalized_word_it_doesnt_know_goes_even_without_the_names(self):
        self.assertEqual(ef.normalize('person Sam Lee at Globex has no email'), 'person <word> at <word> has no email')
        self.assertEqual(ef.normalize('lookup of globex.com failed'), 'lookup of <url> failed')

    def test_what_tells_the_bug_stays(self):
        self.assertEqual(ef.normalize("'NoneType' object has no attribute 'get'"), '"NoneType" object has no attribute "…"')
        self.assertEqual(ef.normalize('list index out of range'), 'list index out of range')
        self.assertEqual(ef.normalize("Cannot read properties of undefined (reading 'title')"), 'Cannot read properties of undefined (reading "…")')
        self.assertEqual(ef.normalize('timeout after 30.5s on row 12345'), 'timeout after <n> s on row <n>')

    def test_a_plain_code_is_not_a_secret(self):
        # Seen in the feed: "android <secret>" for error=android_feed_unavailable. Codes of lowercase words stay;
        # anything with digits, capitals or one long run of letters still goes.
        self.assertEqual(ef.normalize('android error=android_feed_unavailable'), 'android error = android_feed_unavailable')
        self.assertEqual(ef.normalize('delivery status=delivery_outcome_unknown'), 'delivery status = delivery_outcome_unknown')
        for secret in ('xoxb_1234_abcdefghijklmnopqrstuvwx', 'ABCdefGHIjklMNOpqrSTUvwxYZ012345', 'abcdefghijklmnopqrstuvwxyzabcd',
                       'abc-defghijklmnopqrstuvwxyzabcdefg'):
            self.assertEqual(ef.normalize('sync failed ' + secret), 'sync failed <secret>', secret)
        self.assertEqual(ef.normalize('token=abc_def_ghi_jkl_mno_pqr'), 'token = <secret>')
        self.assertEqual(a.fault_message(RuntimeError('feed failed error=android_feed_unavailable')), 'feed failed error=android_feed_unavailable')
        self.assertEqual(a.fault_message(RuntimeError('bad ABCdefGHIjklMNOpqrSTUvwxYZ012345')), 'bad <secret>')

    def test_the_shape_check_refuses_anything_else(self):
        for bad in ('Sam’s card', 'naïve', 'a' * 200, 'x\ny', "it's"):
            self.assertFalse(ef.allowed(bad), bad)

    def test_only_a_place_in_our_code(self):
        self.assertIsNone(ef.where('/home/jeroen/app/assistant.py', 'f', 1))
        self.assertIsNone(ef.where('../etc/passwd', 'f', 1))
        self.assertIsNone(ef.where('C:\\Users\\Marie\\x.py', 'f', 1))
        self.assertEqual(ef.where('connectors/gmail.py', 'sync', 40), 'connectors/gmail.py:sync:40')
        with self.connect() as db:
            self.assertIsNone(ef.record(db, 'service', 'KeyError', 'x', '/home/jeroen/a.py', 'f', 1))


class Dedupe(Base):
    def test_a_repeat_counts_and_a_moved_line_is_the_same_error(self):
        first = self.rec(line=12)
        self.assertEqual(self.rec(line=12, at=NOW + dt.timedelta(minutes=1)), first)
        self.assertEqual(self.rec(line=14, at=NOW + dt.timedelta(minutes=2)), first)  # a release moved it
        other = self.rec(message='Sam broke it', kind='ValueError')
        self.assertNotEqual(other, first)
        self.assertEqual(self.rec(message='Lee broke it', kind='ValueError'), other)  # the name was never part of it
        with self.connect() as db:
            rows = dict(db.execute('SELECT id,count FROM error_feed').fetchall())
        self.assertEqual(rows, {first: 3, other: 2})

    def test_a_flood_of_different_errors_keeps_the_first_ones(self):
        for n in range(ef.MAX_SIGNATURES + 20):
            self.rec(function=f'f{n}')
        with self.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM error_feed').fetchone()[0], ef.MAX_SIGNATURES)

    def test_batches_are_rate_limited_and_resend_only_what_grew(self):
        sid = self.rec()
        self.rec(function='other')
        self.assertEqual(self.send(), 2)
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=1)), 0)  # too soon, and nothing new anyway
        self.rec(at=NOW + dt.timedelta(minutes=2))
        self.rec(at=NOW + dt.timedelta(minutes=3))
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=5)), 0)  # still too soon
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=11)), 1)
        last = self.net.sent[-1]['signatures']
        self.assertEqual([(s['id'], s['count'], s['total']) for s in last], [(sid, 2, 3)])
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=30)), 0)  # nothing grew

    def test_a_batch_is_capped_and_the_day_too(self):
        for n in range(ef.BATCH + 5):
            self.rec(function=f'f{n}')
        self.assertEqual(self.send(), ef.BATCH)
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=11)), 5)
        with self.connect() as db:
            ef.set_pref(db, 'day_count', ef.DAY_CAP)
        self.rec(function='late')
        self.assertEqual(self.send(NOW + dt.timedelta(minutes=30)), 0)
        self.assertEqual(self.send(NOW + dt.timedelta(days=1)), 1)  # a new day

    def test_a_failed_send_goes_again_later(self):
        self.rec()
        self.net.fail = True
        with self.assertRaises(OSError):
            self.send()
        self.net.fail = False
        self.assertEqual(self.send(NOW + dt.timedelta(seconds=30)), 1)  # never marked sent, so not held back

    def test_names_this_machine_knows_go_before_sending(self):
        self.rec(message='lookup failed for globex')
        self.send(names=lambda: ['Globex'])
        self.assertEqual(self.net.sent[0]['signatures'][0]['message'], 'lookup failed for <name>')

    def test_what_is_sent_is_only_the_signature(self):
        self.rec(message=ATTEMPTS[0])
        self.send()
        sig = self.net.sent[0]['signatures'][0]
        self.assertEqual(sorted(sig), ['count', 'first_seen', 'id', 'kind', 'last_seen', 'message', 'source', 'total', 'version', 'where'])
        self.assertEqual((sig['kind'], sig['message'], sig['where'], sig['version']),
                         ('IndexError', 'Failed to send to <email>: <n> rejected', 'assistant.py:review_step:12', 'abc123def456'))

    def test_kept_30_days(self):
        self.rec(at=NOW - dt.timedelta(days=31))
        self.rec(function='fresh')
        with self.connect() as db:
            self.assertEqual(ef.prune(db, NOW), 1)


class OptOut(Base):
    def test_off_records_nothing_sends_nothing_and_drops_what_waited(self):
        self.rec()
        with self.connect() as db:
            ef.set_on(db, False)
            self.assertEqual(db.execute('SELECT count(*) FROM error_feed').fetchone()[0], 0)
        self.assertIsNone(self.rec(function='after'))
        self.assertEqual(self.send(), 0)
        self.assertEqual(self.net.sent, [])
        with self.connect() as db:
            self.assertEqual(ef.view(db)['on'], False)
            ef.set_on(db, True)
        self.rec()
        self.assertEqual(self.send(), 1)

    def test_turned_off_while_a_batch_went(self):
        self.rec()

        def call(method, path, body=None):
            with self.connect() as db:
                ef.set_on(db, False)
            return {'ok': True}
        ef.send(self.connect, call, current=NOW)
        with self.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM error_feed').fetchone()[0], 0)

    def test_the_dashboard_switch(self):
        app = types_app(self.path)
        app.action('set_error_reports', {'on': False}, owner_dashboard=True)
        self.assertFalse(app.learnings_view()['errors'])
        with self.assertRaises(ValueError):
            app.action('set_error_reports', {'on': True})  # only the owner, from the dashboard
        app.action('set_error_reports', {'on': True}, owner_dashboard=True)
        self.assertTrue(app.learnings_view()['errors'])


def types_app(path):
    app = object.__new__(a.App)
    app.store = a.Store(path)
    app.fleet = None
    app.config = {'accounts': []}
    return app


class Sources(Base):
    def test_the_dashboard_posts_only_its_own_code(self):
        app = types_app(self.path)
        out = app.action('client_error', {'errors': [
            {'kind': 'TypeError', 'message': "Cannot read properties of undefined (reading 'sam@globex.example')", 'file': 'dashboard.html',
             'function': 'renderCard', 'line': 4021},
            {'kind': 'TypeError', 'message': 'x', 'file': 'chrome-extension://abc/content.js', 'function': 'f', 'line': 1},
            {'kind': 'Error', 'message': 'x', 'file': '/home/jeroen/x.js', 'function': 'f', 'line': 1},
        ] * 5})
        self.assertEqual(out['counted'], 4)  # the first CLIENT_MAX of 15 looked at, only the dashboard's own
        with app.store.connect() as db:
            rows = db.execute('SELECT source,kind,message,location,count FROM error_feed').fetchall()
        self.assertEqual([tuple(r) for r in rows],
                         [('dashboard', 'TypeError', 'Cannot read properties of undefined (reading "…")', 'dashboard.html:renderCard:4021', 4)])

    def test_service_errors_come_through_the_fault_log(self):
        store = a.Store(self.path)
        log = a.FaultLog(store, 'abc123def456')
        try:
            {}['Sam Lee']
        except KeyError as error:
            log.record(error, 'review')
        with store.connect() as db:
            row = db.execute('SELECT source,kind,message,location,version FROM error_feed').fetchone()
        self.assertEqual(tuple(row)[:3], ('service', 'KeyError', '"…"'))
        self.assertTrue(row['location'].startswith('tests/test_error_feed.py:test_service_errors_come_through_the_fault_log:'), row['location'])

    def test_a_failed_sync_names_the_service_only(self):
        store = a.Store(self.path)
        store.failed('gmail:sam.lee@globex.example', a.SourceError('Token for sam.lee@globex.example expired'))
        with store.connect() as db:
            row = db.execute('SELECT source,kind,message,location FROM error_feed').fetchone()
        self.assertEqual(tuple(row), ('sync', 'SourceError', 'Token for <email> expired', 'sync:gmail'))

    def test_a_rate_limited_sync_is_not_an_error_until_it_keeps_failing(self):
        store = a.Store(self.path)
        for _ in range(a.RATE_LIMIT_REPORT_AFTER - 1):
            store.failed('work-slack', a.SourceError('slack:conversations.history', 429, 120))
            store.failed('work-slack-2', a.SourceError('slack_ratelimited:conversations.history', retry_after=60))
        with store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM error_feed').fetchone()[0], 0)
        store.failed('work-slack', a.SourceError('slack:conversations.history', 429, 120))
        store.failed('other-slack', a.SourceError('slack:conversations.history', 403))
        with store.connect() as db:
            rows = sorted(tuple(r) for r in db.execute('SELECT message,location FROM error_feed'))
        self.assertEqual(rows, [('slack: conversations.history: HTTP_ <n>', 'sync:other-slack'),
                                ('slack: conversations.history: HTTP_ <n>', 'sync:work-slack')])

    def test_a_failed_agent_job_names_the_tool_and_kind_only(self):
        store = a.Store(self.path)
        jobs = object.__new__(agent_jobs.AgentJobs)
        jobs.connect = store.connect
        with store.connect() as db:
            db.execute(agent_jobs.SCHEMA) if ';' not in agent_jobs.SCHEMA else db.executescript(agent_jobs.SCHEMA)
            db.execute("INSERT INTO agent_jobs(id,suggestion_id,tool,place,status,brief,created_at,updated_at) VALUES('j','s','claude','local','running','Fix Sam''s card',?,?)",
                       (NOW.isoformat(), NOW.isoformat()))
        jobs.finish('j', 'failed', error='Sam said no', error_kind='auth')
        with store.connect() as db:
            row = db.execute('SELECT source,kind,message,location FROM error_feed').fetchone()
        self.assertEqual(tuple(row), ('job', 'auth', '', 'agent_jobs.py:claude'))


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    unittest.main()

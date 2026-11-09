"""History backfill: older messages and meetings kept to search and read, never as signals (machine/store/history.py,
machine/app/history.py). Every source is faked: no network, no wacli, no model."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
from seams import patch_everywhere  # noqa: E402

spec = importlib.util.spec_from_file_location('assistant_history', Path(__file__).parent.parent / 'assistant.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import bounces  # noqa: E402
import check_now  # noqa: E402
import embeddings  # noqa: E402
import graph  # noqa: E402
import ms_graph  # noqa: E402
from machine.store import graph_history  # noqa: E402
from machine.app import history as app_history  # noqa: E402
from machine.store import history  # noqa: E402

FREE_DISK = app_history.free_disk  # the real one: the tests below patch it out
FREE_MEMORY = app_history.free_memory

NOW = '2026-11-06T09:00:00+00:00'
WA = {'id': 'wa', 'service': 'whatsapp', 'store': '/nowhere', 'identity_sha256': 'x', 'boundary': 'personal:whatsapp'}
MAIL = {'id': 'work', 'service': 'gmail', 'email': 'owner@example.com', 'boundary': 'work:Example'}
CAL = {'id': 'cal', 'service': 'calendar', 'email': 'owner@example.com', 'boundary': 'work:Example'}


def wa_row(n, at, text='Hello'):
    return {'ChatJID': '3200000000@s.whatsapp.net', 'MsgID': f'SYNTHETIC-{n}', 'Timestamp': at, 'FromMe': False,
            'SenderJID': '3200000000@s.whatsapp.net', 'Text': text, 'ChatName': 'Sample chat'}


def mail(n, at, subject='Quarterly numbers', sender='Sam <sam@example.org>'):
    stamp = int(dt.datetime.fromisoformat(at).timestamp() * 1000)
    return {'id': f'm{n}', 'threadId': f't{n}', 'internalDate': str(stamp), 'labelIds': ['INBOX'],
            'payload': {'mimeType': 'text/plain', 'headers': [{'name': 'Subject', 'value': subject}, {'name': 'From', 'value': sender},
                                                              {'name': 'To', 'value': 'owner@example.com'}],
                        'body': {'data': a.base64.urlsafe_b64encode(b'Here are the numbers.').decode()}}}


class FakeWhatsApp:
    rows, reads = [], []

    def __init__(self, config, account):
        pass

    def read(self, command):
        FakeWhatsApp.reads.append(command)
        after, before = command[command.index('--after') + 1], command[command.index('--before') + 1]
        return {'messages': [r for r in FakeWhatsApp.rows if after <= r['Timestamp'].replace('Z', '+00:00') < before]}


class FakeGmail:
    pages, reads = {}, []

    def __init__(self, config, account):
        pass

    def profile(self):
        return {'emailAddress': 'owner@example.com', 'historyId': '1'}

    def get(self, resource, params=None):
        FakeGmail.reads.append((resource, dict(params or {})))
        if resource == 'messages':
            return FakeGmail.pages[(params or {}).get('pageToken')]
        return FakeGmail.messages[resource.split('/')[1]]


class FakeCalendar:
    items, reads = [], []

    def __init__(self, config, account):
        pass

    def profile(self):
        return {'id': 'owner@example.com', 'timeZone': 'UTC'}

    def get(self, method, params):
        FakeCalendar.reads.append(params)
        return {'items': FakeCalendar.items, 'nextSyncToken': 'x'}


class Base(unittest.TestCase):
    accounts = [WA]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.store = a.Store(Path(self.tmp.name) / 'events.sqlite')
        clock = patch_everywhere(a, 'now', return_value=NOW); clock.start(); self.addCleanup(clock.stop)
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': list(self.accounts), 'database': str(self.store.path)}
        self.app.collector_resting = {x['id'] for x in self.accounts}
        self.app.HISTORY_SOURCES = {'whatsapp': (FakeWhatsApp, a.whatsapp_event), 'mail': (FakeGmail, a.message_event),
                                    'calendar': (FakeCalendar, a.calendar_event, a.calendar_title_excluded),
                                    'slack': (None, a.slack_event)}
        FakeWhatsApp.rows, FakeWhatsApp.reads, FakeGmail.reads, FakeCalendar.reads = [], [], [], []
        with self.store.connect() as db:  # each connection's own first week is in (OnboardingFirst tests one that isn't)
            db.executemany('INSERT INTO milestones(name,at) VALUES(?,?)', [('first_import:' + i, NOW) for i in ('wa', 'work', 'cal')])
        for x in [p for p in (mock.patch.object(app_history, 'free_disk', return_value=True),
                              mock.patch.object(app_history, 'free_memory', return_value=True))]:
            x.start(); self.addCleanup(x.stop)

    def first_look_over(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at,detail) VALUES('first_dig_done',?,'cards')", (NOW,))

    def rows(self, sql='SELECT source_id,history,version,analyzed_version FROM events ORDER BY source_id'):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute(sql)]


class TheLine(Base):
    """History rows are stored reviewed and stay so; everything that makes signals skips them; search finds them."""

    def setUp(self):
        super().setUp()
        self.store.commit_page(MAIL['id'], {}, [a.message_event(MAIL, mail(1, '2026-11-05T10:00:00+00:00', 'Signal now'))])
        kept = self.store.commit_page(MAIL['id'], None, [a.message_event(MAIL, mail(2, '2026-03-02T10:00:00+00:00', 'Old numbers')),
                                                         a.message_event(MAIL, mail(1, '2026-11-05T10:00:00+00:00', 'Signal now'))],
                                      record_sync=False, history=True)
        self.assertEqual(kept, 1)  # the signal already here stays a signal, untouched
        with self.store.connect() as db:
            self.old, self.new = (db.execute('SELECT id FROM events WHERE source_id=?', (s,)).fetchone()[0] for s in ('m2', 'm1'))

    def test_history_is_reviewed_from_the_start_and_through_edits(self):
        self.assertEqual(self.rows(), [('m1', 0, 1, 0), ('m2', 1, 1, 1)])
        edited = a.message_event(MAIL, mail(2, '2026-03-02T10:00:00+00:00', 'Old numbers, relabeled'))
        self.store.commit_page(MAIL['id'], {}, [edited])  # the mailbox's own sync sees a label change on it
        self.assertEqual(self.rows(), [('m1', 0, 1, 0), ('m2', 1, 2, 2)])
        again = self.store.commit_page(MAIL['id'], None, [a.message_event(MAIL, mail(2, '2026-03-02T10:00:00+00:00', 'Other'))],
                                       record_sync=False, history=True)
        self.assertEqual(again, 0)  # a replayed page keeps nothing twice and never rewrites a row
        self.assertEqual(self.rows('SELECT title FROM events WHERE source_id=\'m2\''), [('Old numbers, relabeled',)])

    def test_no_review_first_look_or_new_count_sees_history(self):
        pending = self.store.events([MAIL['id']], pending=True, limit=100)
        self.assertEqual([r['id'] for r in pending], [self.new])
        with self.store.connect() as db:
            self.assertEqual(check_now.waiting(db), 1)
            self.assertEqual(db.execute('SELECT count(*) FROM events WHERE analyzed_version=0').fetchone()[0], 1)  # the first look's own
        connector = next(c for c in self.store_status()['connectors'] if c['id'] == MAIL['id'])
        self.assertEqual(connector['signals_24h'], 1)  # history in today is no "new" signal

    def store_status(self):
        return self.store.snapshot([MAIL])

    def test_graph_embeddings_and_bounces_read_signals_only(self):
        with self.store.connect() as db:
            self.assertEqual([s[0] for s in graph._signals(db, '2025-01-01')], [self.new])
            self.assertEqual([r['id'] for r in embeddings.pending(db, {'model': 'm', 'dims': 4}, 10)], [self.new])
            db.execute("UPDATE events SET metadata=json_set(metadata,'$.from','MAILER-DAEMON@example.org')")
            seen = []
            with mock.patch.object(bounces, '_one', side_effect=lambda db, row, own: seen.append(row['id']) or []):
                bounces.scan(db)  # the first pass over every message collected before
                db.execute("UPDATE email_bounce_scan SET last_event=0")
                bounces.scan(db)  # and the passes over new ones
            self.assertEqual(seen, [self.new, self.new])

    def test_search_finds_history_and_says_so(self):
        found = self.store.events([MAIL['id']], query='old numbers', limit=10)
        self.assertEqual([r['id'] for r in found], [self.old])
        self.assertTrue(a.review_view(found[0])['history'])
        self.assertNotIn('history', a.review_view(self.store.events([MAIL['id']], event_ids=[self.new])[0]))


class WhenItRuns(Base):
    """Onboarding stays fast: nothing is read before the first look ended, or while a review, a first import or a
    sync read runs."""

    def test_a_new_install_reads_no_history_until_the_first_look_ended(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO sync_activity VALUES('s1','wa',?,'success',3,NULL,NULL)", (NOW,))
        FakeWhatsApp.rows = [wa_row(1, '2026-06-01T10:00:00Z')]
        self.assertEqual(self.app.history_wait(), 'first_look')
        self.assertFalse(self.app.history_step())
        self.assertEqual(FakeWhatsApp.reads, [])  # not one read on the source while setup runs
        self.first_look_over()
        self.assertIsNone(self.app.history_wait())

    def test_an_older_machine_without_a_first_look_starts_a_day_after_its_first_read(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO sync_activity VALUES('s1','wa','2026-10-01T09:00:00+00:00','success',3,NULL,NULL)")
        self.assertIsNone(self.app.history_wait())

    def test_waits_for_a_review_a_first_import_and_room(self):
        self.first_look_over()
        with self.store.connect() as db:
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r','running',?,?)", (NOW, NOW))
        self.assertEqual(self.app.history_wait(), 'review')
        with self.store.connect() as db:
            db.execute("UPDATE review_runs SET status='ok'")
            db.execute("INSERT INTO checkpoints(account_id,state) VALUES('work',?)", (json.dumps({'mode': 'bootstrap', 'after': 1}),))
        self.assertEqual(self.app.history_wait(), 'first_import')
        with self.store.connect() as db:
            db.execute("UPDATE checkpoints SET state=?", (json.dumps({'mode': 'incremental'}),))
        self.app.collector_resting = set()  # a sync read holds back only its own connection (history_step), never all
        self.assertIsNone(self.app.history_wait())
        self.app.collector_resting = {'wa'}
        with mock.patch.object(app_history, 'free_disk', return_value=False):
            self.assertEqual(self.app.history_wait(), 'disk')
        with mock.patch.object(app_history, 'free_memory', return_value=False):
            self.assertEqual(self.app.history_wait(), 'memory')
        self.app.config['history_days'] = 0
        self.assertEqual(self.app.history_wait(), 'off')

    def test_disk_room_is_absolute_on_a_big_disk_and_relative_on_a_small_one(self):
        gb, db = 1024 ** 3, self.store.path
        def room(total, free, path=db):
            usage = app_history.shutil._ntuple_diskusage(total * gb, (total - free) * gb, free * gb)
            with mock.patch.object(app_history.shutil, 'disk_usage', return_value=usage):
                return FREE_DISK(path)
        self.assertTrue(room(469, 43))  # 91% used, but 43 GB is plenty: a tenth of a big disk is capped at 5 GB
        self.assertFalse(room(469, 4.5))
        self.assertFalse(room(32, 3))  # a small disk still keeps a tenth free
        self.assertTrue(room(32, 3.5))
        self.assertFalse(room(16, 1.9))  # never under 2 GB
        big = Path(self.tmp.name) / 'big.sqlite'
        with open(big, 'wb') as f:
            f.truncate(3 * gb)  # sparse: takes no real space
        self.assertTrue(room(469, 43, big))
        self.assertFalse(room(469, 5.5, big))  # twice the database must fit
        with mock.patch.object(app_history.shutil, 'disk_usage', side_effect=OSError):
            self.assertTrue(FREE_DISK(db))  # can't tell: no reason to wait

    def test_depth_is_a_setting_with_a_safe_default(self):
        self.assertEqual(history.depth({}), 365)
        self.assertEqual(history.depth({'history_days': 90}), 90)
        self.assertEqual(history.depth({'history_days': 10 ** 6}), history.MAX_DAYS)
        self.assertEqual(history.depth({'history_days': 'lots'}), 365)

    def test_only_own_connections_with_a_store_go_back(self):
        self.app.config['accounts'] = [WA, {**MAIL, 'shared': True}, {**WA, 'id': 'wa2', 'store': ''}, CAL]
        self.assertEqual([x['id'] for x in self.app.history_accounts()], ['wa', 'cal'])

    def test_memory_figure(self):
        path = Path(self.tmp.name) / 'meminfo'
        path.write_text('MemTotal: 3900000 kB\nMemAvailable: 300000 kB\n')
        self.assertFalse(FREE_MEMORY(path))
        path.write_text('MemTotal: 3900000 kB\nMemAvailable: 900000 kB\n')
        self.assertTrue(FREE_MEMORY(path))


class WhatsAppHistory(Base):
    def test_walks_back_a_week_a_step_to_its_depth_and_resumes(self):
        self.first_look_over()
        self.app.config['history_days'] = 30
        FakeWhatsApp.rows = [wa_row(1, '2026-10-20T10:00:00Z', 'Older'), wa_row(2, '2026-10-12T10:00:00Z', 'Oldest'),
                             wa_row(3, '2026-11-05T10:00:00Z', 'This week'), wa_row(4, '2025-01-01T10:00:00Z', 'Too old')]
        steps = 0
        while self.app.history_step():
            steps += 1
            self.assertLess(steps, 10)
        self.assertEqual(steps, 4)  # 22 days from the week the sync rereads back to 30 days: four reads of a week or less
        self.assertEqual(sorted(r[0] for r in self.rows('SELECT body,history,analyzed_version FROM events')), ['Older', 'Oldest'])
        self.assertTrue(all(r[1] == 1 and r[2] == 1 for r in self.rows('SELECT body,history,analyzed_version FROM events')))
        with self.store.connect() as db:
            self.assertEqual(history.progress(db, ['wa']), {'wa': {'back_to': '2026-10', 'done': True, 'kept': 2}})
        reads = len(FakeWhatsApp.reads)
        self.assertFalse(self.app.history_step())  # done: no more reads
        self.assertEqual(len(FakeWhatsApp.reads), reads)
        self.app.config['history_days'] = 365  # deeper since: it walks on from where it stopped, not again
        self.assertTrue(self.app.history_step())
        after = FakeWhatsApp.reads[-1]
        self.assertEqual(after[after.index('--before') + 1][:10], '2026-10-07')

    def test_a_restart_goes_on_from_the_saved_cursor(self):
        self.first_look_over()
        self.app.config['history_days'] = 30
        self.assertTrue(self.app.history_step())
        with self.store.connect() as db:
            cursor = history.get(db, 'wa')['state']['cursor']
        again = object.__new__(a.App); again.__dict__.update(self.app.__dict__)
        self.assertTrue(again.history_step())
        last = FakeWhatsApp.reads[-1]
        self.assertEqual(last[last.index('--before') + 1], cursor)


class BetweenSyncs(Base):
    """A Machine with many sources has some sync reading nearly all the time. History steps in between them: a
    connection's own read holds back only that connection, a short while, and the wait is logged once per change."""
    accounts = [WA, {'id': 'slack', 'service': 'slack', 'boundary': 'work:Example'}]

    def test_other_reads_never_hold_it_back_and_its_own_only_briefly(self):
        self.first_look_over()
        FakeWhatsApp.rows = [wa_row(1, '2026-10-20T10:00:00Z', 'Older')]
        self.app.collector_resting = {'wa'}  # Slack reads all the time
        self.assertTrue(self.app.history_step())
        self.assertIsNone(self.app.history_why)
        self.app.collector_resting = {'slack'}  # WhatsApp's own sync reads now
        with self.assertLogs(app_history.LOG, 'INFO') as logged:
            reads = len(FakeWhatsApp.reads)
            self.assertFalse(self.app.history_step())
            self.assertFalse(self.app.history_step())
            self.assertEqual(len(FakeWhatsApp.reads), reads)
            self.assertEqual(self.app.history_why, 'sync')
            self.assertIn('sync', app_history.SHORT_WAITS)  # tried again in STEP_GAP_SECONDS, not WAIT_SECONDS
            self.app.collector_resting = {'wa', 'slack'}
            self.assertTrue(self.app.history_step())
        self.assertEqual([r.getMessage() for r in logged.records if 'history' in r.getMessage() and 'kept' not in r.getMessage()],
                         ['history waits reason=sync', 'history goes'])  # once per change, not every step


class MailHistory(Base):
    accounts = [MAIL]

    def test_pages_of_older_mail_kept_as_history_without_reading_what_is_here(self):
        self.first_look_over()
        with self.store.connect() as db:
            db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?)', ('work', json.dumps({'mode': 'incremental', 'after': 1793350800})))
        self.store.commit_page('work', None, [a.message_event(MAIL, mail(2, '2026-10-01T10:00:00+00:00'))], record_sync=False)
        FakeGmail.messages = {'m1': mail(1, '2026-10-20T10:00:00+00:00'), 'm2': mail(2, '2026-10-01T10:00:00+00:00'),
                              'm3': mail(3, '2026-02-01T10:00:00+00:00', 'Contract draft')}
        FakeGmail.pages = {None: {'messages': [{'id': 'm1'}, {'id': 'm2'}], 'nextPageToken': 'p2'}, 'p2': {'messages': [{'id': 'm3'}]}}
        self.assertTrue(self.app.history_step())
        self.assertTrue(self.app.history_step())
        self.assertFalse(self.app.history_step())
        q = FakeGmail.reads[0][1]['q']
        self.assertEqual(q, f"after:{int(dt.datetime.fromisoformat('2025-11-06T09:00:00+00:00').timestamp())} before:1793350800")
        self.assertNotIn(('messages/m2', {'format': 'full'}), FakeGmail.reads)  # already here: not read again
        self.assertEqual(self.rows('SELECT source_id,history FROM events ORDER BY source_id'), [('m1', 1), ('m2', 0), ('m3', 1)])
        with self.store.connect() as db:
            self.assertEqual(history.progress(db, ['work'])['work'], {'back_to': '2026-02', 'done': True, 'kept': 2})
        connector = next(c for c in self.app.store.snapshot([MAIL])['connectors'] if c['id'] == 'work')
        self.assertEqual(connector['backfill'], {'back_to': '2026-02', 'done': True, 'kept': 2})  # its card's (not WhatsApp's own `history`)

    def test_outlook_reads_the_same_window(self):
        calls = []
        with mock.patch.object(ms_graph, 'call', side_effect=lambda *x, **k: calls.append(x[4]) or {'value': []}):
            ms_graph.gmail_call({}, None, MAIL, 'gmail.users.messages.list', {'q': 'after:1735689600 before:1793350800', 'maxResults': 20})
        self.assertEqual(calls[0]['$filter'], 'receivedDateTime ge 2025-01-01T00:00:00Z and receivedDateTime lt 2026-10-30T09:00:00Z')


class CalendarHistory(Base):
    accounts = [CAL]

    def test_a_year_of_meetings_and_the_calendar_starts_there(self):
        self.first_look_over()
        FakeCalendar.items = [{'id': 'e1', 'summary': 'Board meeting', 'status': 'confirmed', 'start': {'dateTime': '2026-03-03T10:00:00Z'},
                               'end': {'dateTime': '2026-03-03T11:00:00Z'}},
                              {'id': 'e2', 'summary': 'Gone', 'status': 'cancelled', 'start': {'dateTime': '2026-03-04T10:00:00Z'},
                               'end': {'dateTime': '2026-03-04T11:00:00Z'}}]
        with self.store.connect() as db:
            self.assertIsNone(history.calendar_start(db, ['cal']))
        self.assertTrue(self.app.history_step())
        self.assertEqual(FakeCalendar.reads[0]['timeMin'][:10], '2025-11-06')
        self.assertEqual(self.rows('SELECT source_id,history,analyzed_version FROM events'), [('e1', 1, 1)])
        with self.store.connect() as db:
            self.assertEqual(history.calendar_start(db, ['cal']), '2025-11-06')
        with self.store.connect() as db:
            db.execute("INSERT INTO sync_activity VALUES('s1','cal','2026-10-30T09:00:00+00:00','success',3,NULL,NULL)")
        with mock.patch.object(a.App, 'started_at', return_value='2026-10-30T09:00:00+00:00'):
            self.assertEqual(self.app.calendar_starts(), {'day': '2025-11-06', 'joined': False, 'history': True})  # the line moves back
        meetings = self.store.calendar(['cal'], '2026-03-01T00:00:00+00:00', '2026-03-08T00:00:00+00:00')
        self.assertEqual([m['title'] for m in meetings], ['Board meeting'])  # readable on the Calendar

    def test_no_start_line_while_older_meetings_still_come_in(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO sync_activity VALUES('s1','cal','2026-10-30T09:00:00+00:00','success',3,NULL,NULL)")
            history.save(db, 'cal', {'target': '2025-11-06T09:00:00+00:00'}, a.now(), 3, '2026-06-01T10:00:00+00:00')
        with mock.patch.object(a.App, 'started_at', return_value='2026-10-30T09:00:00+00:00'):
            self.assertIsNone(self.app.calendar_starts())  # its meetings land before the first-read start: no edge there yet


class OnboardingFirst(Base):
    """History never holds back onboarding: a connection's own first week first (also one added later), nothing of
    history (backfill, Graph passes, embeddings) while the first look or a check runs, and a 429 to history rests
    history alone, never live sync."""
    accounts = [MAIL]

    def setUp(self):
        super().setUp()
        FakeGmail.messages = {'m3': mail(3, '2026-02-01T10:00:00+00:00', 'Contract draft')}
        FakeGmail.pages = {None: {'messages': [{'id': 'm3'}]}}

    def test_a_connection_added_after_setup_waits_for_its_own_first_week(self):
        self.first_look_over()
        with self.store.connect() as db:
            db.execute("DELETE FROM milestones WHERE name='first_import:work'")  # added just now: never read yet
        self.assertFalse(self.app.history_step())
        self.assertEqual((FakeGmail.reads, self.app.history_why), ([], 'first_import'))
        self.assertIn('first_import', app_history.SHORT_WAITS)  # looked at again soon, then it goes
        with self.store.connect() as db:  # its first week is coming in
            db.execute("INSERT INTO milestones(name,at) VALUES('first_page:work',?)", (NOW,))
            db.execute('INSERT INTO checkpoints(account_id,state,last_success) VALUES(?,?,?)', ('work', json.dumps({'mode': 'incremental'}), NOW))
        self.assertFalse(self.app.history_step())
        self.assertEqual(FakeGmail.reads, [])
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_import:work',?)", (NOW,))
        self.assertTrue(self.app.history_step())
        self.assertTrue(FakeGmail.reads)

    def test_setup_runs_no_history_work_at_all(self):
        with self.store.connect() as db:
            db.execute("INSERT INTO sync_activity VALUES('s1','work',?,'success',3,NULL,NULL)", (NOW,))
        self.store.commit_page('work', None, [a.message_event(MAIL, mail(4, '2026-01-01T10:00:00+00:00'))], record_sync=False, history=True)
        with mock.patch.object(embeddings, 'embed_pending', side_effect=AssertionError('no history embedding during setup')):
            for why in ('first_look', 'review'):
                if why == 'review':
                    self.first_look_over()
                    with self.store.connect() as db:
                        db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('r','running',?,?)", (NOW, NOW))
                self.assertEqual(self.app.history_wait(), why)
                self.assertFalse(self.app.history_step())
                self.assertFalse(self.app.history_graph_step())
                self.assertEqual(self.app.history_embed_step({'url': 'http://127.0.0.1:1', 'model': 'm'}), app_history.WAIT_SECONDS)
        self.assertEqual(FakeGmail.reads, [])
        with self.store.connect() as db:
            self.assertIsNone(graph_history.since(db))  # so a build during setup reads no history row
            db.isolation_level = None
            self.assertEqual(graph.build(db, self.app.config, NOW, history=True)['history'], 0)

    def test_a_history_429_rests_history_and_never_live_sync(self):
        self.first_look_over()

        def busy(resource, params=None):
            FakeGmail.reads.append((resource, params))
            raise a.SourceError('gmail', 429, retry_after=60)
        with mock.patch.object(FakeGmail, 'get', side_effect=busy):
            self.assertFalse(self.app.history_step())
        self.assertEqual(len(FakeGmail.reads), 1)  # no quick retry: none of the budget live sync needs
        self.assertEqual(self.app.history_why, 'rate_limit')
        self.assertEqual(self.app.history_wait(), 'rate_limit')  # all history work rests
        self.assertFalse(self.app.history_graph_step())
        with self.store.connect() as db:  # what live sync waits on is untouched
            self.assertIsNone(db.execute("SELECT 1 FROM checkpoints WHERE account_id='work' AND (error IS NOT NULL OR retry_at IS NOT NULL)").fetchone())
        self.app.history_rested = 0.0  # its rest over: it goes on
        self.assertIsNone(self.app.history_wait())

    def test_a_live_429_holds_history_back(self):
        self.first_look_over()
        with self.store.connect() as db:
            db.execute('INSERT INTO checkpoints(account_id,state,error,error_at,failures) VALUES(?,?,?,?,1)',
                       ('work', json.dumps({'mode': 'incremental'}), 'gmail:HTTP_429', NOW))
        self.assertEqual(self.app.history_wait(), 'rate_limit')
        self.assertFalse(self.app.history_step())
        self.assertEqual(FakeGmail.reads, [])

    def test_history_embeddings_come_after_signals_newest_first_and_rest_on_a_429(self):
        self.first_look_over()
        self.store.commit_page('work', {}, [a.message_event(MAIL, mail(1, '2026-11-05T10:00:00+00:00', 'Live'))])
        for n, at in ((5, '2026-01-01T10:00:00+00:00'), (6, '2026-06-01T10:00:00+00:00')):
            self.store.commit_page('work', None, [a.message_event(MAIL, mail(n, at, f'Old {n}'))], record_sync=False, history=True)
        settings = {'url': 'http://127.0.0.1:1', 'model': 'm', 'dims': 4}
        with self.store.connect() as db:
            self.assertEqual([r['title'] for r in embeddings.pending(db, settings, 10)], ['Live'])
            self.assertEqual([r['title'] for r in embeddings.pending(db, settings, 10, history=True)], ['Old 6', 'Old 5'])
        with mock.patch.object(embeddings, 'embed_pending', return_value=2) as embedded:
            self.assertEqual(self.app.history_embed_step(settings), app_history.EMBED_GAP_SECONDS)
        self.assertEqual(embedded.call_args.kwargs, {'history': True})
        with mock.patch.object(embeddings, 'embed_pending', side_effect=embeddings.EmbeddingError('http_429')):
            self.assertEqual(self.app.history_embed_step(settings), app_history.WAIT_SECONDS)
        self.assertEqual(self.app.history_wait(), 'rate_limit')


SLACK = {'id': 'slack', 'service': 'slack', 'transport': 'broker', 'team_id': 'T0ACME0001', 'user_id': 'U0OWNER01',
         'email': 'owner@example.com', 'slack_host': 'acme-example.slack.com', 'boundary': 'work:Example'}
LIVE_AFTER = dt.datetime.fromisoformat(NOW) - dt.timedelta(days=7)


def ts(at):
    return f'{dt.datetime.fromisoformat(at).timestamp():.6f}'


def slack_msg(at, user, text, **more):
    return {'type': 'message', 'ts': ts(at), 'user': user, 'text': text, **more}


class FakeSlackClient:
    """The collector's Slack client as history uses it: its pacing and conversations.history / replies pages."""

    def __init__(self, account, pages):
        self.account, self.pages, self.reads, self.wait, self.round, self.fail = account, pages, [], 0, 180, None

    def limited_wait(self):
        return self.wait

    def limited_gap(self):
        return 65

    def get(self, method, params):
        self.reads.append((method, dict(params)))
        if self.fail:
            raise self.fail
        return self.pages[(method, params['channel'], params.get('ts'), params.get('cursor'))]


class SlackHistory(Base):
    """Slack's year of history: the collector's own conversations only, newest first, a page at a time in a slow lane
    that never takes a minute the collector wants, resting on a 429 and going on from its saved cursor."""
    accounts = [SLACK]
    KICKOFF = '2026-05-01T10:00:00+00:00'

    def setUp(self):
        super().setUp()
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_import:slack',?)", (NOW,))
            db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?)', ('slack', json.dumps({
                'mode': 'incremental', 'phase': 'scan', 'index': 0, 'after': f'{LIVE_AFTER.timestamp():.6f}', 'channels': [
                    {'id': 'C0SALES001', 'name': 'sales', 'type': 'channel', 'last_activity': 1790000000.0, 'threads': []},
                    {'id': 'D0SAM00001', 'name': 'DM U0SAM0001', 'type': 'dm', 'last_activity': 1793000000.0, 'threads': []},
                    {'id': 'C0LEFT0001', 'name': 'left-it', 'type': 'channel', 'error': 'slack_not_in_channel', 'threads': []}]})))
        self.client = FakeSlackClient(SLACK, {
            ('conversations.history', 'D0SAM00001', None, None): {'messages': [slack_msg('2026-09-01T10:00:00+00:00', 'U0SAM0001', 'Can we talk pricing?')],
                                                                  'response_metadata': {'next_cursor': 'dm2'}},
            ('conversations.history', 'D0SAM00001', None, 'dm2'): {'messages': [slack_msg('2026-03-01T10:00:00+00:00', 'U0OWNER01', 'Sent the deck')]},
            ('conversations.history', 'C0SALES001', None, None): {'messages': [slack_msg(self.KICKOFF, 'U0ROBIN01', 'Kickoff notes', reply_count=1)]},
            ('conversations.replies', 'C0SALES001', ts(self.KICKOFF), None): {'messages': [
                slack_msg(self.KICKOFF, 'U0ROBIN01', 'Kickoff notes', reply_count=1),
                slack_msg('2026-05-02T10:00:00+00:00', 'U0SAM0001', 'Looks good', thread_ts=ts(self.KICKOFF))]}})
        self.app.slack_sources = {'slack': self.client}
        self.app.collector_rest_until = {'slack': app_history.time.monotonic() + 300}
        gap = mock.patch.object(app_history, 'SLACK_GAP_SECONDS', 0); gap.start(); self.addCleanup(gap.stop)

    def test_a_year_of_its_own_conversations_newest_first_then_thread_replies(self):
        self.first_look_over()
        for _ in range(5):
            self.assertTrue(self.app.history_step())
        self.assertFalse(self.app.history_step())
        self.assertEqual(self.app.history_why, 'done')
        self.assertEqual([(m, p['channel'], p.get('cursor')) for m, p in self.client.reads],
                         [('conversations.history', 'D0SAM00001', None), ('conversations.history', 'D0SAM00001', 'dm2'),
                          ('conversations.history', 'C0SALES001', None), ('conversations.replies', 'C0SALES001', None)])
        params = self.client.reads[0][1]  # back a year, up to where the live import starts; Slack's page size
        self.assertEqual((params['oldest'], params['latest'], params['limit']),
                         (ts('2025-11-06T09:00:00+00:00'), f'{LIVE_AFTER.timestamp():.6f}', 15))
        self.assertNotIn('C0LEFT0001', json.dumps(self.client.reads))  # never a conversation the live sync can't read
        rows = self.rows('SELECT title,history,version=analyzed_version FROM events ORDER BY occurred_at')
        self.assertEqual([(r[1], r[2]) for r in rows], [(1, 1)] * 4)  # history, reviewed from the start: no to-do sees it
        self.assertEqual(len(rows), 4)  # the thread's first message once
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM events WHERE history=0').fetchone()[0], 0)
            self.assertEqual(history.progress(db, ['slack'])['slack'], {'back_to': '2026-03', 'done': True, 'kept': 4})
            graph_history.ensure(db)
            self.assertTrue(graph_history.advance(db, '2025-01-01T00:00:00+00:00', NOW))
            self.assertEqual(len(graph_history.rows(db, '2025-01-01T00:00:00+00:00')), 4)  # the Graph counts it
        connector = next(c for c in self.app.store.snapshot([SLACK])['connectors'] if c['id'] == 'slack')
        self.assertEqual(connector['backfill'], {'back_to': '2026-03', 'done': True, 'kept': 4})  # the card's History line

    def test_a_conversation_slack_refuses_never_holds_up_the_others(self):
        # An answer about one conversation that isn't "gone" (a label Slack.read doesn't know, a missing scope for its
        # kind) kept that conversation first in line, so this connection's history never went on.
        self.first_look_over()
        read = self.client.get
        def get(method, params):
            if params['channel'] == 'D0SAM00001':
                self.client.reads.append((method, dict(params)))
                raise a.SourceError('slack_invalid_response:' + method)
            return read(method, params)
        self.client.get = get
        for _ in range(8):
            if not self.app.history_step():
                break
        self.assertEqual(self.app.history_why, 'done')
        self.assertEqual([(m, p['channel']) for m, p in self.client.reads],
                         [('conversations.history', 'D0SAM00001'), ('conversations.history', 'C0SALES001'), ('conversations.replies', 'C0SALES001')])

    def test_its_slow_lane_never_takes_a_minute_the_collector_wants(self):
        self.first_look_over()
        self.assertTrue(self.app.history_step())  # the list: no Slack call
        self.app.collector_resting = set()  # the collector reads now
        self.assertFalse(self.app.history_step())
        self.app.collector_resting = {'slack'}
        self.app.collector_rest_until = {'slack': app_history.time.monotonic() + 60}  # it reads again within a minute
        self.assertFalse(self.app.history_step())
        self.app.collector_rest_until = {'slack': app_history.time.monotonic() + 300}
        self.client.wait = 120  # this connection's minute of the round is two minutes off
        self.assertFalse(self.app.history_step())
        self.assertEqual((self.client.reads, self.app.history_why), ([], 'sync'))
        self.client.wait = 0
        self.assertTrue(self.app.history_step())
        self.assertEqual(len(self.client.reads), 1)
        with mock.patch.object(app_history, 'SLACK_GAP_SECONDS', 180):
            self.assertTrue(self.app.history_step())  # the lane's gap starts with this read
            self.assertFalse(self.app.history_step())  # and holds the next one back
        self.assertEqual(len(self.client.reads), 2)

    def test_a_429_rests_all_history_and_the_walk_goes_on_from_its_cursor(self):
        self.first_look_over()
        self.assertTrue(self.app.history_step())
        self.assertTrue(self.app.history_step())  # the direct message's first page: its cursor is saved
        self.client.fail = a.SourceError('slack:conversations.history', 429, retry_after=3600)
        self.assertFalse(self.app.history_step())
        self.assertEqual(self.app.history_why, 'rate_limit')
        self.assertGreater(self.app.history_rested - app_history.time.monotonic(), 3500)  # Slack's Retry-After, over the usual rest
        self.assertEqual(self.app.history_wait(), 'rate_limit')
        with self.store.connect() as db:
            self.assertIsNone(db.execute("SELECT 1 FROM checkpoints WHERE account_id='slack' AND (error IS NOT NULL OR retry_at IS NOT NULL)").fetchone())
            self.assertEqual(history.get(db, 'slack')['state']['cursor'], 'dm2')
        # a restart after the rest: a new service, the same database
        self.app = restarted = object.__new__(a.App)
        restarted.store, restarted.config, restarted.HISTORY_SOURCES = self.store, {'accounts': [SLACK], 'database': str(self.store.path)}, {'slack': (None, a.slack_event)}
        restarted.collector_resting, restarted.slack_sources = {'slack'}, {'slack': self.client}
        restarted.collector_rest_until = {'slack': app_history.time.monotonic() + 300}
        self.client.fail, self.client.reads = None, []
        later = (dt.datetime.fromisoformat(NOW) + dt.timedelta(hours=2)).isoformat()
        with mock.patch.object(app_history, 'now', return_value=later):
            self.assertTrue(restarted.history_step())
        self.assertEqual([(m, p['channel'], p.get('cursor')) for m, p in self.client.reads], [('conversations.history', 'D0SAM00001', 'dm2')])

    def test_the_real_client_shares_one_minute_between_collector_and_history(self):
        client = a.Slack({}, SLACK)
        self.assertEqual((client.round, client.limited_gap()), (180, 65))
        client.last_limited, client.last_call = app_history.time.monotonic() - 10, 0
        self.assertGreater(client.limited_wait(), 54)  # a read ten seconds ago: not within the same minute
        client.last_limited = app_history.time.monotonic() - 500
        with mock.patch.object(client, 'slot_wait', return_value=0):
            self.assertEqual(client.limited_wait(), 0)
        self.assertTrue(client.limited_lock.acquire(blocking=False)); client.limited_lock.release()


class TeamsHistory(Base):
    accounts = [{'id': 'teams', 'service': 'teams', 'email': 'owner@example.com', 'boundary': 'work:Example'}]

    def test_a_teams_history_from_before_channels_walks_its_channels_too(self):
        self.first_look_over()
        with self.store.connect() as db:
            db.execute("INSERT INTO milestones(name,at) VALUES('first_import:teams',?)", (NOW,))
            history.save(db, 'teams', {'chats': [], 'upper': '2026-10-29T09:00:00+00:00', 'target': '2025-11-06T09:00:00+00:00'},
                         NOW, 5, '2026-01-01T00:00:00+00:00', True, 365)
        seen = []

        def page(config, account, helpers, state, upper, target):
            seen.append((dict(state), upper, target))
            state['channels'] = []
            return [], True
        import machine.sources.connectors as connectors
        with mock.patch.object(connectors, 'load_connector', return_value=mock.Mock(history_page=page)):
            self.assertTrue(self.app.history_step())
            self.assertFalse(self.app.history_step())  # its channels are in: done again
        self.assertEqual(seen[0][1:], ('2026-10-29T09:00:00+00:00', '2025-11-06T09:00:00+00:00'))  # the same window
        self.assertEqual(seen[0][0]['chats'], [])  # its chats are not read again


if __name__ == '__main__':
    unittest.main()

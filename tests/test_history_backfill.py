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
from machine.app import history as app_history  # noqa: E402
from machine.store import history  # noqa: E402
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
                                    'calendar': (FakeCalendar, a.calendar_event, a.calendar_title_excluded)}
        FakeWhatsApp.rows, FakeWhatsApp.reads, FakeGmail.reads, FakeCalendar.reads = [], [], [], []
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


if __name__ == '__main__':
    unittest.main()

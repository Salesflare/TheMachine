"""The routing keys that became plain metadata keys (message_seal.ROUTING_KEYS: end_at, status, recurring_event_id,
chat_kind) and the one-time pass that makes them readable to SQL in the messages kept before
(machine/store/plain_keys.py): from scratch, stopped halfway and run again, without the message key, with a row that
does not open, on a plain database. And the three reads that filter on them in SQL now (the Calendar, the Connections
count, the Telegram lookup) give what the old reads gave before the pass, halfway through it and after it.
No real names or mail."""
import datetime as dt
import importlib.util
import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from seams import patch_everywhere
import enrichment
import message_seal
from machine.store import plain_keys
from machine.text import encoded

spec = importlib.util.spec_from_file_location('plain_keys_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

OLD_PLAIN = message_seal.PLAIN_METADATA - message_seal.ROUTING_KEYS
NOW = '2026-10-09T12:00:00+00:00'
SEES = "SELECT count(*) FROM events WHERE json_extract(metadata,'$.mc1_sealed') IS NOT NULL AND (json_extract(metadata,'$.end_at') IS NOT NULL OR json_extract(metadata,'$.chat_kind') IS NOT NULL)"


def event(account, source, kind, at, metadata, title='Note', body='Hello'):
    return {'account_id': account, 'source_id': source, 'kind': kind, 'occurred_at': at, 'title': title, 'body': body, 'deleted': False,
            'metadata': metadata}


def day(n, hour=9):
    return (dt.datetime(2026, 10, 1, hour, tzinfo=dt.timezone.utc) + dt.timedelta(days=n)).isoformat()


def meeting(n, status='confirmed', days=0, account='cal'):
    return event(account, f'm{n}-{status}-{days}', 'calendar.event', day(n), {
        'end_at': day(n + days, 10), 'status': status, 'recurring_event_id': 'series1' if n % 2 else None, 'location': 'Room 4',
        'attendees': [{'email': 'pat@client.example'}]}, title=f'Meeting {n}')


def said(n, chat, kind, sender, account='tg'):
    return event(account, f't{n}', 'telegram.message', day(n % 20, 8), {'chat_id': chat, 'chat_kind': kind, 'sender_id': sender, 'chat_name': 'Chat'})


def task(n, status='Waiting on someone else'):
    return event('sf', f'task{n}', 'salesforce.activity', day(n), {'type': 'task', 'status': status, 'due': '2026-11-12', 'closed': False})


def as_before(store, ids=None):
    """Rows as the version before this one stored them: on a sealed store the routing keys go into the sealed member."""
    with store.connect() as db:
        for row in db.execute('SELECT id,metadata FROM events ORDER BY id').fetchall():
            if store.sealer and (ids is None or row['id'] in ids):
                db.execute('UPDATE events SET metadata=? WHERE id=?', (store.sealer.seal_json(encoded(json.loads(row['metadata'])), plain=OLD_PLAIN), row['id']))


def stored(store):
    """Every event as SQLite has it, sealed values sealed."""
    with plain_keys._raw(store) as db:
        return {r[0]: r[1:] for r in db.execute('SELECT id,metadata,title,body,content_hash,version FROM events')}


def opened(store):
    with store.connect() as db:
        return {r['id']: (json.loads(r['metadata']), r['title'], r['body']) for r in db.execute('SELECT id,metadata,title,body FROM events')}


def copies(store):
    return sorted(store.path.parent.glob(f'{store.path.name}.before-{plain_keys.NAME}-*'))


class Base(unittest.TestCase):
    def store(self, protect=True):
        return a.Store(Path(self.enterContext(tempfile.TemporaryDirectory())) / 'events.sqlite', protect=protect)

    def filled(self, protect=True, count=30):
        store = self.store(protect)
        store.commit_page('cal', {}, [meeting(n, 'cancelled' if n % 5 == 0 else 'confirmed') for n in range(count)])
        store.commit_page('tg', {}, [said(n, '777' if n % 3 else '444', 'group' if n % 3 else 'dm', str(500 + n)) for n in range(count)])
        as_before(store)
        return store

    def run_pass(self, store, **options):
        return plain_keys.run(store, pause=0, **options)


class ThePass(Base):
    def test_the_keys_are_plain_and_the_others_are_not(self):
        self.assertEqual(message_seal.ROUTING_KEYS, {'end_at', 'status', 'recurring_event_id', 'chat_kind'})
        self.assertLessEqual(message_seal.ROUTING_KEYS, message_seal.PLAIN_METADATA)
        for key in ('cc', 'attendees', 'organizer', 'location', 'sender_id', 'chat_name', 'admin_emails', 'task_status', 'host_email'):
            self.assertNotIn(key, message_seal.PLAIN_METADATA)

    def test_a_new_message_keeps_them_in_the_clear_and_seals_the_rest(self):
        store = self.store()
        store.commit_page('cal', {}, [meeting(1, days=2)])
        with plain_keys._raw(store) as db:
            seen = json.loads(db.execute('SELECT metadata FROM events').fetchone()[0])
        self.assertEqual({k: seen[k] for k in ('end_at', 'status', 'recurring_event_id')}, {'end_at': day(3, 10), 'status': 'confirmed', 'recurring_event_id': 'series1'})
        self.assertEqual(sorted(seen), ['end_at', 'mc1_sealed', 'recurring_event_id', 'status'])
        self.assertNotIn('Room 4', json.dumps(seen))
        self.assertNotIn('client.example', json.dumps(seen))
        self.assertEqual(self.run_pass(store)['changed'], 0)  # nothing to do for it
        self.assertEqual(copies(store), [])

    def test_from_scratch_every_row_becomes_readable_and_says_what_it_said(self):
        store = self.filled()
        before_open, before = opened(store), stored(store)
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 0)
        report = self.run_pass(store, batch=7)
        self.assertEqual(report, {'state': 'done', 'changed': 60, 'unread': 0})
        after = stored(store)
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 60)
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE json_extract(metadata,'$.status')='cancelled'").fetchone()[0], 6)
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE json_extract(metadata,'$.recurring_event_id')='series1'").fetchone()[0], 15)
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE json_extract(metadata,'$.chat_kind')='group'").fetchone()[0], 20)
            # what is hidden stays hidden
            self.assertEqual(db.execute("SELECT count(*) FROM events WHERE json_extract(metadata,'$.location') IS NOT NULL OR json_extract(metadata,'$.sender_id') IS NOT NULL "
                                        "OR json_extract(metadata,'$.attendees') IS NOT NULL OR json_extract(metadata,'$.chat_name') IS NOT NULL").fetchone()[0], 0)
            self.assertTrue(store.fix_done(plain_keys.NAME))
        self.assertEqual(opened(store), before_open)
        for row_id, row in after.items():  # only metadata was rewritten: title, body, hash and version are as they were
            self.assertEqual(row[1:], before[row_id][1:])
            self.assertNotEqual(row[0], before[row_id][0])
            self.assertNotIn('Room 4', row[0])
        self.assertEqual(len(copies(store)), 1)
        self.assertEqual(copies(store)[0].stat().st_mode & 0o777, 0o600)
        # the same event from its source again is no change: nothing goes back to the review
        store.commit_page('cal', {}, [meeting(3)])
        self.assertEqual(stored(store)[4][4], 1)
        # and a second run does nothing
        self.assertIsNone(self.run_pass(store))
        self.assertEqual(stored(store), {**after, 4: stored(store)[4]})
        self.assertEqual(len(copies(store)), 1)

    def test_stopped_halfway_it_goes_on_from_there_and_seals_nothing_twice(self):
        store = self.filled()
        before_open = opened(store)
        self.assertEqual(self.run_pass(store, batch=10, batches=2), {'state': 'stopped', 'changed': 20, 'unread': 0})
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 20)
            self.assertEqual(plain_keys.progress(db), {'last_id': 20, 'top_id': 60, 'copied': 1, 'changed': 20, 'unread': 0, 'done': False})
            self.assertFalse(store.fix_done(plain_keys.NAME))
        halfway = stored(store)
        self.assertEqual(opened(store), before_open)
        # a message that arrives meanwhile is stored with today's keys and is none of the pass's business
        store.commit_page('cal', {}, [meeting(40)])
        new = stored(store)[61]
        stop = threading.Event()
        stop.set()  # the service is stopping: nothing more is done
        self.assertEqual(plain_keys.run(store, stop, batch=10)['state'], 'stopped')
        self.assertEqual(stored(store), {**halfway, 61: new})
        self.assertEqual(self.run_pass(store, batch=10), {'state': 'done', 'changed': 60, 'unread': 0})
        after = stored(store)
        for row_id in range(1, 21):  # the ones done before the stop were not sealed again
            self.assertEqual(after[row_id], halfway[row_id])
        self.assertEqual(after[61], new)
        self.assertEqual({k: v for k, v in opened(store).items() if k != 61}, before_open)
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 61)
        self.assertEqual(len(copies(store)), 1)  # one copy, from before the first change

    def test_the_cursor_set_back_changes_nothing(self):
        # as after a crash between a batch's write and the next: the rows are done, the cursor says they are not
        store = self.filled()
        self.run_pass(store, batch=10, batches=3)
        halfway = stored(store)
        with store.connect() as db:
            db.execute('UPDATE plain_key_pass SET last_id=0')
        self.assertEqual(self.run_pass(store, batch=10), {'state': 'done', 'changed': 60, 'unread': 0})
        after = stored(store)
        for row_id in range(1, 31):
            self.assertEqual(after[row_id], halfway[row_id])

    def test_without_the_message_key_it_waits_and_touches_nothing(self):
        store = self.filled()
        before, sealer = stored(store), store.sealer
        store.sealer = None  # the key is not there (kept by the hosting or the keyring)
        self.assertEqual(self.run_pass(store), {'state': 'waiting', 'changed': 0, 'unread': 0})
        store.sealer = message_seal.Sealer(b'\x07' * 32)  # another key: opens nothing
        self.assertEqual(self.run_pass(store), {'state': 'waiting', 'changed': 0, 'unread': 0})
        store.sealer = sealer
        self.assertEqual(stored(store), before)
        self.assertEqual(copies(store), [])
        with store.connect() as db:
            self.assertIsNone(plain_keys.progress(db))
            self.assertFalse(store.fix_done(plain_keys.NAME))
        # the key is there: it runs
        self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 60, 'unread': 0})

    def test_the_worker_waits_for_the_key_and_runs_once_it_is_there(self):
        from machine.app import workers
        store = self.filled()
        states, sealer = [], store.sealer
        store.sealer = None

        class Stop:
            def wait(_, seconds):
                states.append(seconds)
                if len(states) == 3:
                    store.sealer = sealer
                return len(states) > 6

            def is_set(_):
                return False
        app = type('App', (), {'store': store, 'stop': Stop()})()
        with patch.object(plain_keys, 'PAUSE', 0):
            workers.WorkersApp.plain_keys_worker(app)
        self.assertEqual(states, [0, 60, 60])  # twice without the key, then it ran and the worker ended
        self.assertTrue(store.fix_done(plain_keys.NAME))
        workers.WorkersApp.plain_keys_worker(app)  # at the next start: done, nothing to do
        self.assertEqual(states, [0, 60, 60, 0])

    def test_a_row_that_does_not_open_is_left_as_it_is(self):
        store = self.filled()
        other = message_seal.Sealer(b'\x07' * 32)
        damaged = other.seal_json(encoded({'end_at': day(3), 'location': 'Elsewhere'}), plain=OLD_PLAIN)
        with store.connect() as db:
            db.execute('UPDATE events SET metadata=? WHERE id=12', (damaged,))
        before = stored(store)
        self.assertEqual(self.run_pass(store, batch=10), {'state': 'done', 'changed': 59, 'unread': 1})
        after = stored(store)
        self.assertEqual(after[12], before[12])
        self.assertEqual(sum(after[i] != before[i] for i in after), 59)

    def test_a_row_a_sync_changed_while_its_batch_was_read_is_left_to_the_sync(self):
        store = self.filled()
        real, seen = plain_keys._copy, []

        def copy(store):  # between the batch's read and its write
            real(store)
            store.commit_page('cal', {}, [{**meeting(3), 'title': 'Moved'}])
            seen.append(stored(store)[4])
        with patch.object(plain_keys, '_copy', copy):
            self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 59, 'unread': 0})
        self.assertEqual(stored(store)[4], seen[0])
        self.assertEqual(opened(store)[4][1], 'Moved')
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 60)

    def test_a_copy_that_fails_leaves_everything_for_the_next_try(self):
        store = self.filled()
        before = stored(store)

        def fails(name):
            store.path.with_name(f'{store.path.name}.before-{name}-half').write_bytes(b'half')
            raise OSError('disk full')
        with patch.object(store, 'copy_before', fails), self.assertRaises(OSError):
            self.run_pass(store)
        self.assertEqual((stored(store), copies(store)), (before, []))
        self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 60, 'unread': 0})

    def test_an_empty_store_and_a_plain_one_are_done_at_once(self):
        for protect in (True, False):
            store = self.store(protect)
            self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 0, 'unread': 0})
            self.assertIsNone(self.run_pass(store))
        store = self.filled(protect=False)
        before = stored(store)
        self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 0, 'unread': 0})
        self.assertEqual((stored(store), copies(store)), (before, []))

    def test_a_salesforce_tasks_status_is_not_a_routing_value_and_gets_its_own_sealed_name(self):
        # the Status of a Salesforce task is a word the organization's admin chose: it never becomes readable
        import connectors.salesforce as salesforce
        self.assertIn("'task_status': row.get('Status')", Path(salesforce.__file__).read_text(encoding='utf-8'))
        for protect in (True, False):
            with self.subTest(sealed=protect):
                store = self.store(protect)
                store.commit_page('sf', {}, [task(1), task(2, 'Completed')])
                store.commit_page('cal', {}, [meeting(1)])
                as_before(store)
                self.assertEqual(self.run_pass(store), {'state': 'done', 'changed': 3 if protect else 2, 'unread': 0})
                found = opened(store)
                self.assertEqual(found[1][0], {'type': 'task', 'task_status': 'Waiting on someone else', 'due': '2026-11-12', 'closed': False})
                self.assertEqual(found[3][0]['status'], 'confirmed')  # a calendar event's status stays `status`
                with plain_keys._raw(store) as db:
                    raw = [r[0] for r in db.execute("SELECT metadata FROM events WHERE kind='salesforce.activity'")]
                if protect:
                    self.assertEqual([sorted(json.loads(text)) for text in raw], [['mc1_sealed']] * 2)
                    self.assertNotIn('Waiting', ''.join(raw))
                # the task as today's connector stores it is the same event: no new version, nothing to review again
                store.commit_page('sf', {}, [{**task(1), 'metadata': found[1][0]}])
                self.assertEqual(stored(store)[1][4], 1)
                self.assertEqual(len(copies(store)), 1)


def old_calendar(db, accounts, start, end):
    """The Calendar's rows as the version before read them: end_at from the opened rows."""
    sql = ("SELECT id,metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND +account_id IN (" + ','.join('?' for _ in accounts)
           + ') AND occurred_at>? AND occurred_at<%s? ORDER BY occurred_at,id')
    back = (dt.datetime.fromisoformat(start) - dt.timedelta(days=35)).isoformat()
    rows = [r for r in db.execute(sql % '=', (*accounts, back, start)) if str(json.loads(r['metadata'] or '{}').get('end_at') or '') > start]
    return [r['id'] for r in (rows + db.execute((sql % '') + ' LIMIT 300', (*accounts, start, end)).fetchall())[:300]]


def old_upcoming(db, account, at):
    return sum((json.loads(m or '{}').get('status') or '') != 'cancelled' for (m,) in db.execute(
        'SELECT metadata FROM events WHERE account_id=? AND deleted=0 AND occurred_at>=? AND occurred_at<?',
        (account, at, (dt.datetime.fromisoformat(at) + dt.timedelta(days=7)).isoformat())))


def old_telegram(db, wanted, accounts):
    found = {}
    marks = ','.join('?' * len(accounts))
    for chat, account in db.execute(f"SELECT DISTINCT json_extract(metadata,'$.chat_id'),account_id FROM events WHERE kind='telegram.message' AND account_id IN ({marks})",
                                    list(accounts)).fetchall():
        chat = str(chat or '')
        if not enrichment.TELEGRAM_USER.fullmatch(chat) or 'tg:' + chat not in wanted or 'tg:' + chat in found:
            continue
        one = db.execute("SELECT metadata FROM events WHERE kind='telegram.message' AND account_id=? AND json_extract(metadata,'$.chat_id')=? LIMIT 1", (account, chat)).fetchone()
        if one and json.loads(one[0]).get('chat_kind') != 'group':
            found['tg:' + chat] = (account, chat)
    groups = 0
    for metadata, account in db.execute(f"SELECT metadata,account_id FROM events WHERE kind='telegram.message' AND account_id IN ({marks}) ORDER BY occurred_at DESC LIMIT ?",
                                        [*accounts, enrichment.TELEGRAM_READ]):
        m = json.loads(metadata)
        if m.get('chat_kind') != 'group':
            continue
        groups += 1
        if groups > enrichment.TELEGRAM_SCAN or len(found) == len(wanted):
            break
        sender = str(m.get('sender_id') or '')
        if enrichment.TELEGRAM_USER.fullmatch(sender) and 'tg:' + sender in wanted:
            found.setdefault('tg:' + sender, (account, sender))
    return found


class TheReads(Base):
    """The three reads give what the old ones gave: on a plain store, and on a sealed one before the pass, halfway
    through it (some rows done, some not, some stored since) and after it."""
    ACCOUNT = {'id': 'cal', 'email': 'owner@example.com', 'boundary': 'personal', 'service': 'outlook_calendar'}
    WANTED = {'tg:444', 'tg:445', 'tg:501', 'tg:502', 'tg:777', 'tg:888', 'tg:530'}

    def fill(self, store):
        events = []
        for n in range(0, 40):
            events.append(meeting(n, 'cancelled' if n % 4 == 0 else 'tentative' if n % 4 == 1 else 'confirmed', days=n % 6))
        events.append(event('cal', 'no-end', 'calendar.event', day(5), {'location': 'Room 4'}))  # no end, no status
        events.append(event('cal', 'empty', 'calendar.event', day(7), {}))
        store.commit_page('cal', {}, events)
        store.commit_page('cal2', {}, [event('cal2', 'other', 'calendar.event', day(6), {'end_at': day(9), 'status': 'confirmed'})])
        chats = []
        for n in range(60):
            dm = n % 4 == 0
            chats.append(said(n, ('444' if n % 8 else '445') if dm else '777', 'dm' if dm else 'group', str(500 + n % 35)))
        chats.append(event('tg', 'bare', 'telegram.message', day(3), {'chat_id': '888'}))  # no kind: a private chat, as before
        store.commit_page('tg', {}, chats)

    def check(self, store, state):
        with patch_everywhere(a, 'now', return_value=NOW):
            new_count = store.snapshot([self.ACCOUNT])['connectors'][0]['upcoming_7d']
        with store.connect() as db:
            self.assertEqual(new_count, old_upcoming(db, 'cal', NOW), state)
            self.assertGreater(new_count, 0)
            for start, days in ((day(8, 0), 7), (day(20, 0), 1), (day(0, 0), 15), (day(45, 0), 7)):
                end = (dt.datetime.fromisoformat(start) + dt.timedelta(days=days)).isoformat()
                for accounts in (['cal'], ['cal', 'cal2'], ['none']):
                    self.assertEqual([r['id'] for r in store.calendar(accounts, start, end)], old_calendar(db, accounts, start, end), (state, start, accounts))
            began = db.execute("SELECT count(*) FROM events WHERE account_id='cal' AND occurred_at>? AND occurred_at<?", (day(8, 0), day(15, 0))).fetchone()[0]
            self.assertGreater(len(store.calendar(['cal'], day(8, 0), day(15, 0))), began)  # some began before and still run
            for wanted in (self.WANTED, {'tg:501'}, {'tg:777'}, {'tg:999'}):
                for accounts in (['tg'], ['none']):
                    self.assertEqual(enrichment.telegram_addresses(db, wanted, accounts), old_telegram(db, wanted, accounts), (state, wanted))
            found = enrichment.telegram_addresses(db, self.WANTED, ['tg'])
            self.assertEqual(sorted(found), ['tg:444', 'tg:445', 'tg:501', 'tg:502', 'tg:530', 'tg:888'])

    def test_on_a_plain_store(self):
        store = self.store(protect=False)
        self.fill(store)
        self.check(store, 'plain')
        plain_keys.run(store, pause=0)
        self.check(store, 'plain, after the pass')

    def test_on_a_sealed_store_before_during_and_after_the_pass(self):
        store = self.store()
        self.fill(store)
        self.check(store, 'stored by this version')
        as_before(store)
        with store.connect() as db:
            self.assertEqual(db.execute(SEES).fetchone()[0], 0)
        self.check(store, 'before the pass')
        self.assertEqual(plain_keys.run(store, pause=0, batch=25, batches=2)['state'], 'stopped')
        # stored since (their own titles: the Calendar shows a meeting that is there twice once)
        store.commit_page('cal', {}, [{**meeting(9, days=3), 'title': 'Since'}, {**meeting(10, 'cancelled', days=1), 'title': 'Since, off'}])
        store.commit_page('tg', {}, [said(70, '777', 'group', '530'), said(71, '445', 'dm', '445')])
        with store.connect() as db:
            done = db.execute(SEES).fetchone()[0]
            self.assertTrue(0 < done < db.execute('SELECT count(*) FROM events').fetchone()[0] - 10)
        self.check(store, 'halfway')
        self.assertEqual(plain_keys.run(store, pause=0, batch=25)['state'], 'done')
        self.check(store, 'after the pass')

    def test_the_telegram_lookup_reads_only_group_messages_once_the_keys_are_plain(self):
        # 5 group messages among 40 private ones, and room to read 8 rows: the old read never got to the group
        store = self.store()
        store.commit_page('tg', {}, [said(n, '444', 'dm', '444') for n in range(40)] + [
            event('tg', f'g{n}', 'telegram.message', day(0, 1), {'chat_id': '777', 'chat_kind': 'group', 'sender_id': '555'}) for n in range(5)])
        with patch.object(enrichment, 'TELEGRAM_SCAN', 2), patch.object(enrichment, 'TELEGRAM_READ', 8), store.connect() as db:
            self.assertEqual(old_telegram(db, {'tg:555'}, ['tg']), {})
            self.assertEqual(enrichment.telegram_addresses(db, {'tg:555'}, ['tg']), {'tg:555': ('tg', '555')})


if __name__ == '__main__':
    unittest.main()

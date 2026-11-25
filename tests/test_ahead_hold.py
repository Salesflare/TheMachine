"""Drafts ahead wait while reviews are far behind (machine/store/ahead_hold.py): what waits, what never does, when it ends,
and that nothing is lost, late, doubled or left behind. Fake data, a fake clock, no model."""
import datetime as dt
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from seams import patch_everywhere  # noqa: E402

import machine.app.ahead_hold as app_hold
import machine.delivery.deliver as deliver
import machine.delivery.telegram as delivery_telegram
import machine.main as machine_main
from machine.store import ahead_hold, review_catch_up
import timeutil

START = dt.datetime(2026, 11, 24, 12, 0, tzinfo=dt.timezone.utc)  # a Tuesday


def usage(short=20, week=5):
    return [{'provider': 'openai', 'name': 'ChatGPT', 'windows': [{'label': '5h', 'used': short, 'reset': time.time() + 3600},
                                                                {'label': 'Week', 'used': week, 'reset': time.time() + 86400}]}]


class Fake(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        kept = timeutil.PINNED
        self.addCleanup(lambda: setattr(timeutil, 'PINNED', kept))
        self.path = Path(temp.name) / 'events.sqlite'
        self.at(0)
        self.start()
        self.n = 0
        self.commit(3)
        with self.store.connect() as db:
            db.execute('UPDATE events SET analyzed_version=version')
            db.execute("DELETE FROM milestones WHERE name IN ('tracking_since','first_card_shown','first_ahead_started')")
            db.executemany('INSERT INTO milestones(name,at) VALUES(?,?)',
                           [(name, '2026-10-01T00:00:00+00:00') for name in ('tracking_since', 'first_card_shown', 'first_ahead_started')])
            db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at) VALUES('one','running',?,?)", (timeutil.now(),) * 2)

    def at(self, hours):
        self.clock = START + dt.timedelta(hours=hours)
        timeutil.pin(self.clock)

    def start(self):
        """The service starts (again) on what is on disk."""
        self.store = machine_main.Store(self.path)
        self.store.accounts = [{'id': 'work', 'service': 'gmail'}]
        self.app = object.__new__(machine_main.App)
        self.app.store = self.store
        self.app.config = {'accounts': self.store.accounts, 'review_worker': {'enabled': True}}
        self.app.model_usage = usage()

    def commit(self, count):
        self.store.commit_page('work', {}, [{'account_id': 'work', 'source_id': f's{self.n + i}', 'kind': 'gmail.message', 'occurred_at': timeutil.now(), 'title': 'Question',
                                             'body': 'Can you confirm?', 'metadata': {'from': 'Ann <ann@people.example>', 'thread_id': f't{self.n + i}'}, 'deleted': False}
                                            for i in range(count)])
        self.n += count

    def waits(self, count):
        """This many signals wait for a review, the rest is read; a review has some of them."""
        with self.store.connect() as db:
            db.execute('DELETE FROM analyses')
            db.execute('UPDATE events SET analyzed_version=version')
            db.execute(f'UPDATE events SET analyzed_version=0 WHERE id IN (SELECT id FROM events ORDER BY id LIMIT {count})')
            have = db.execute('SELECT count(*) FROM events').fetchone()[0]
        if have < count:
            self.commit(count - have)
        with self.store.connect() as db:
            db.execute("INSERT INTO analyses(id,started_at,items,status,owner_session,owner_run) SELECT 'a1',?,json_group_array(json_object('id',id,'version',version)),"
                       "'running','s','one' FROM (SELECT * FROM events ORDER BY id LIMIT 40)", (timeutil.now(),))

    def behind(self):
        self.waits(300)

    def save(self, key, event=1, **extra):
        return self.app.action('suggest', {'dedupe_key': key, 'title': f'Answer about {key}', 'body': 'I can draft it.', 'event_ids': [event], 'when': 'now',
                                           'separate': True, 'prepare_ahead': True, **extra})

    def step(self):
        self.app.ahead_behind_at = -1e9  # a minute passed
        return self.app.ahead_hold_step()

    def q(self, sql, *args):
        with self.store.connect() as db:
            return [tuple(r) for r in db.execute(sql, args)]

    def held(self):
        return [r[0] for r in self.q('SELECT suggestion_id FROM ahead_holds ORDER BY rowid')]

    def status(self, sid):
        return self.q('SELECT status,early FROM suggestions WHERE id=?', sid)[0]

    def done(self):
        """Every draft under way is finished."""
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared' WHERE id IN (SELECT suggestion_id FROM preparations)")

    def day(self, n):
        return (self.clock.astimezone(timeutil.local_tz()).date() + dt.timedelta(days=n)).isoformat()


class Held(Fake):
    def test_the_to_do_is_there_at_once_like_any_without_a_draft(self):
        self.behind()
        made = self.save('a')
        self.assertEqual((made['status'], made.get('prepared_ahead')), ('pending', None))
        self.assertEqual(self.held(), [made['id']])
        self.app.config['prepare_ahead'] = False
        plain = self.save('b')
        self.app.config['prepare_ahead'] = True
        seen = {c['id']: c for c in self.store.snapshot(self.store.accounts, connectors=False)['suggestions']}
        differs = {k for k in seen[made['id']] if seen[made['id']][k] != seen[plain['id']].get(k)} - {'id', 'title', 'dedupe_key', 'rowid'}
        self.assertEqual(differs, set())  # nothing on it says a draft waits, and nothing says one is under way
        rows = self.q('SELECT d.status,d.reminder,s.deliver_after FROM deliveries d JOIN suggestions s ON s.id=d.suggestion_id WHERE s.id IN (?,?)', made['id'], plain['id'])
        self.assertEqual(rows[0], rows[1])
        self.assertEqual(self.q('SELECT count(*) FROM preparations'), [(0,)])

    def test_not_behind_a_draft_starts_as_always(self):
        self.waits(240)  # two whole reviews: not far behind
        self.assertEqual(self.save('a')['status'], 'accepted')
        self.assertEqual(self.held(), [])

    def test_the_weight_counts_not_the_number(self):
        self.waits(400)
        with self.store.connect() as db:
            db.execute("UPDATE events SET metadata=json_set(metadata,'$.labels',json('[\"CATEGORY_PROMOTIONS\"]'))")
        self.assertEqual(self.save('a', mail_asks='renew the card')['status'], 'accepted')  # 400 newsletters take a quarter each

    def test_pressing_or_closing_soon_is_never_held(self):
        self.behind()
        for key, extra in (('urgent', {'urgent': True}), ('today', {'due': self.day(0)}), ('soon', {'due': self.day(2)}), ):
            self.assertEqual(self.save(key, **extra)['status'], 'accepted', key)
        self.assertFalse(self.app.ahead_waits({'event_ids': [1], 'expires_at': (self.clock + dt.timedelta(days=1)).isoformat()}))
        self.assertTrue(self.app.ahead_waits({'event_ids': [1], 'expires_at': (self.clock + dt.timedelta(days=5)).isoformat()}))
        self.assertEqual(self.save('later', due=self.day(9))['status'], 'pending')
        self.assertFalse(self.app.ahead_waits({'event_ids': [1], 'urgent': True}))
        self.assertFalse(self.app.ahead_waits({'event_ids': [1], 'due': self.day(1)}))

    def test_a_new_owners_first_ones_are_never_held(self):
        self.behind()
        cases = {'no draft yet': "DELETE FROM milestones WHERE name='first_ahead_started'", 'first look': "DELETE FROM milestones WHERE name='first_card_shown'",
                 'first day': "UPDATE milestones SET at='2026-11-23T13:00:00+00:00' WHERE name='tracking_since'"}
        for why, sql in cases.items():
            with self.store.connect() as db:
                kept = db.execute('SELECT name,at,detail FROM milestones').fetchall()
                db.execute(sql)
            self.assertFalse(self.app.ahead_waits({'event_ids': [1]}), why)
            with self.store.connect() as db:
                db.execute('DELETE FROM milestones')
                db.executemany('INSERT INTO milestones(name,at,detail) VALUES(?,?,?)', [tuple(r) for r in kept])
        self.assertTrue(self.app.ahead_waits({'event_ids': [1]}))
        for column, value in (('preview', 1), ('window_hours', 24), ('promising', 1)):  # the first look and its next batches
            with self.store.connect() as db:
                db.execute(f'UPDATE review_runs SET {column}=?', (value,))
            self.assertFalse(self.app.ahead_waits({'event_ids': [1]}), column)
            with self.store.connect() as db:
                db.execute(f'UPDATE review_runs SET {column}=0')

    def test_only_what_a_review_under_way_saves(self):
        self.behind()
        with self.store.connect() as db:
            db.execute("UPDATE analyses SET owner_run='a chat'")
        self.assertEqual(self.save('chat')['status'], 'accepted')
        with self.store.connect() as db:
            db.execute("UPDATE analyses SET owner_run='one',status='complete'")
        self.assertEqual(self.save('after')['status'], 'accepted')
        # What the service makes itself calls Store.suggest without hold
        self.assertEqual(self.store.suggest('service', 'Say happy birthday', 'B', [1], separate=True, ahead=True)['status'], 'accepted')

    def test_the_owners_own_to_do_never_waits(self):
        self.behind()
        own = self.store.suggest('mine', 'Call Bo', 'B', [2])['id']
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET origin='owner',created_at='2026-11-01T00:00:00+00:00' WHERE id=?", (own,))
        self.assertEqual(self.save('mine-2', separate=False, card_id=own)['status'], 'accepted')
        self.assertEqual(self.held(), [])

    def test_an_update_of_a_to_do_that_had_a_run_never_waits(self):
        self.behind()
        sid = self.store.suggest('one', 'Answer Ann', 'B', [2], ahead=True)['id']
        self.done()
        self.assertEqual(self.save('again', separate=False, card_id=sid)['status'], 'accepted')
        self.assertEqual(self.held(), [])
        with self.store.connect() as db:  # one whose run was stopped, waiting on the owner again
            db.execute("UPDATE preparations SET status='cancelled'")
            db.execute("UPDATE suggestions SET status='pending',early=0 WHERE id=?", (sid,))
        self.assertEqual(self.save('once more', separate=False, card_id=sid)['status'], 'accepted')
        self.assertEqual(self.held(), [])
        plain = self.store.suggest('two', 'Answer Bo', 'B', [3], separate=True)['id']
        self.assertEqual(self.save('two-again', separate=False, card_id=plain)['status'], 'pending')
        self.assertEqual(self.held(), [plain])  # never worked on: its first draft waits

    def test_without_plan_windows_nothing_waits(self):
        self.behind()
        for reading in (None, [], [{'provider': 'openai', 'windows': []}], [{'provider': 'openai', 'windows': [{'label': '5h', 'used': None}]}]):
            self.app.model_usage = reading
            self.assertFalse(self.app.ahead_waits({'event_ids': [1]}), reading)
        self.app.model_usage = usage()
        with patch.object(self.app, 'fallback_covers', lambda: True, create=True):  # billed apart: the plan's window isn't the limit
            self.assertFalse(self.app.ahead_waits({'event_ids': [1]}))
        self.app.config['review_worker'] = {'enabled': False}
        self.assertFalse(self.app.ahead_waits({'event_ids': [1]}))
        self.app.config['review_worker'] = {'enabled': True}
        self.assertTrue(self.app.ahead_waits({'event_ids': [1]}))

    def test_those_that_wait_take_their_place_in_the_day(self):
        self.behind()
        self.assertEqual([self.save(f'k{n}')['status'] for n in range(9)], ['pending'] * 9)
        self.assertEqual(len(self.held()), 7)  # the last 3 of 10 stay for pressing work
        self.assertEqual([self.save(f'p{n}', urgent=True)['status'] for n in range(4)], ['accepted'] * 3 + ['pending'])


class Released(Fake):
    def hold(self, count=3):
        self.behind()
        out = []
        for n in range(count):
            self.at(n / 60)
            out.append(self.save(f'k{n}')['id'])
        self.assertEqual(self.held(), out)
        return out

    def test_caught_up_the_newest_first_one_at_a_time(self):
        sids = self.hold()
        self.assertEqual(self.step(), [])
        self.waits(100)
        order = []
        for _ in sids:
            order += self.step()
            self.assertEqual(self.step(), [])  # the next one waits for this one
            self.assertEqual(self.status(order[-1]), ('accepted', 1))
            self.done()
        self.assertEqual(order, sids[::-1])
        self.assertEqual(self.held(), [])
        self.assertEqual(self.step(), [])
        self.assertEqual(self.q("SELECT count(*) FROM decisions WHERE choice='prepare_ahead' AND source='assistant'"), [(3,)])

    def test_around_the_line_it_does_not_flip(self):
        first = self.hold(1)
        self.waits(200)  # below the line it started at, above the one it ends at
        self.assertEqual(self.step(), [])
        self.assertEqual(self.save('more')['status'], 'pending')
        self.waits(120)
        with self.assertLogs('personal-assistant', 'INFO') as logs:
            self.assertEqual(len(self.step()), 1)
        self.assertTrue(any('why=caught_up count=2' in line for line in logs.output), logs.output)
        self.waits(200)  # caught up since: the higher line counts again, also while the last one waits its turn
        self.assertEqual(self.save('now')['status'], 'accepted')
        self.behind()
        self.done()
        self.assertEqual(self.step(), first)  # let go already: a newer backlog doesn't take it back

    def test_always_behind_every_draft_is_made_after_the_longest_wait_the_oldest_first(self):
        sids = self.hold(4)
        self.at(ahead_hold.HOLD_HOURS - 0.1)
        self.assertEqual(self.step(), [])
        self.at(ahead_hold.HOLD_HOURS + 0.1)
        order = []
        for _ in sids:
            order += self.step()
            self.assertEqual(self.step(), [])
            self.done()
        self.assertEqual(order, sids)
        self.assertEqual(self.held(), [])

    def test_always_behind_for_days_nothing_piles_up(self):
        self.behind()
        waited, made = {}, 0
        for hour in range(0, 24 * 5):
            self.at(hour)
            for sid in self.step():
                made += 1
                waited.pop(sid)
            self.done()
            saved = self.save(f'h{hour}')
            if saved['id'] in self.held():
                waited[saved['id']] = hour
            self.assertLessEqual(len(self.held()), 7)
            self.assertTrue(all(hour - since <= ahead_hold.HOLD_HOURS + 1 for since in waited.values()), waited)
        self.assertGreaterEqual(made, 5 * 5)  # they keep coming, all five days

    def test_pressing_work_all_day_does_not_starve_those_that_wait(self):
        sids = self.hold(2)
        for n in range(12):
            self.save(f'p{n}', urgent=True)
        with self.store.connect() as db:
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE suggestions SET status='prepared' WHERE id IN (SELECT suggestion_id FROM preparations)")
        self.at(ahead_hold.HOLD_HOURS + 0.1)
        for sid in sids:
            self.assertEqual(self.step(), [sid])
            self.done()

    def test_a_pause_holds_the_start_and_leaves_none_behind(self):
        sids = self.hold(1)
        self.at(ahead_hold.HOLD_HOURS + 1)
        for reading in (usage(short=70), usage(week=95), usage(short=100)):
            self.app.model_usage = reading
            self.assertEqual(self.step(), [])
            self.assertEqual(self.status(sids[0]), ('pending', 0))  # never shown as preparing while it can't
        self.at(50)
        self.app.model_usage = usage()
        self.assertEqual(self.step(), sids)

    def test_caught_up_during_a_pause_it_starts_after_it(self):
        sids = self.hold(1)
        self.waits(0)
        self.app.model_usage = usage(short=70)
        self.assertEqual((self.step(), self.status(sids[0])), ([], ('pending', 0)))
        self.behind()
        self.app.model_usage = usage()
        self.assertEqual(self.step(), sids)

    def test_the_days_number_holds_also_then(self):
        sids = self.hold(2)
        with self.store.connect() as db:
            db.executemany("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'prepare_ahead','','assistant',?)",
                           [(f'used-{n}', sids[0], timeutil.now()) for n in range(9)])
        self.waits(0)
        self.assertEqual(self.step(), [sids[1]])
        self.done()
        self.assertEqual((self.step(), self.status(sids[0])), ([], ('pending', 0)))  # the day's 10 are used
        self.at(25)
        self.assertEqual(self.step(), [sids[0]])

    def test_a_due_date_that_comes_close_starts_it_also_while_behind(self):
        self.behind()
        sid = self.save('later', due=self.day(4))['id']
        other = self.save('other')['id']
        self.assertEqual(self.step(), [])
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET due=? WHERE id=?', (self.day(1), sid))
        self.assertEqual(self.step(), [sid])
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET expires_at=? WHERE id=?', ((self.clock + dt.timedelta(hours=30)).isoformat(), other))
        self.assertEqual(self.step(), [other])  # also with another draft under way

    def test_opened_it_starts(self):
        sids = self.hold()
        self.store.note_activity('opened', sids[1])
        self.assertEqual(self.step(), [sids[1]])
        self.assertEqual(self.held(), [sids[0], sids[2]])

    def test_do_it_is_do_it_and_nothing_starts_twice(self):
        sid = self.hold(1)[0]
        self.store.decide(sid, 'accept', '', 'click', 'dashboard')
        self.assertEqual(self.q('SELECT count(*) FROM preparations'), [(1,)])
        before = self.q('SELECT job_id,decision_id FROM preparations')
        self.waits(0)
        self.assertEqual(self.step(), [])
        self.assertEqual((self.held(), self.q('SELECT job_id,decision_id FROM preparations'), self.status(sid)), ([], before, ('accepted', 0)))

    def test_one_tick_after_another_starts_it_once(self):
        sid = self.hold(1)[0]
        self.waits(0)
        self.assertEqual(self.step(), [sid])
        again = object.__new__(machine_main.App)
        again.store, again.config, again.model_usage = self.store, self.app.config, usage()
        self.assertEqual(again.ahead_hold_step(), [])
        self.assertEqual(self.q("SELECT count(*) FROM decisions WHERE choice='prepare_ahead'"), [(1,)])
        requests = []
        for _ in range(2):
            self.app.preparation_step(lambda r: requests.append(r) or {'status': 'admitted'})
        self.assertEqual(len([r for r in requests if r.get('message')]), 1)  # the run the review would have had
        self.assertIn('The owner has NOT tapped Do it yet', next(r['message'] for r in requests if r.get('message')))

    def test_one_no_longer_needed_is_dropped(self):
        sids = self.hold(5)
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed' WHERE id=?", (sids[0],))
            db.execute("UPDATE suggestions SET status='rejected',undo_until=? WHERE id=?", ((self.clock + dt.timedelta(minutes=5)).isoformat(), sids[1]))
            db.execute("UPDATE suggestions SET status='snoozed',snoozed_until=? WHERE id=?", ((self.clock + dt.timedelta(days=3)).isoformat(), sids[2]))  # Later, or handed off
            db.execute('CREATE TABLE IF NOT EXISTS agent_jobs(id TEXT PRIMARY KEY,suggestion_id TEXT)')
            db.execute("INSERT INTO agent_jobs(id,suggestion_id) VALUES('aj',?)", (sids[3],))
        self.step()
        self.assertEqual(self.held(), [sids[1], sids[4]])  # Undo can still bring that one back
        self.at(0.5)
        self.step()
        self.assertEqual(self.held(), [sids[4]])
        with self.store.connect() as db:  # merged into another, or deleted
            db.execute('PRAGMA foreign_keys=OFF')
            db.execute('DELETE FROM suggestions WHERE id=?', (sids[4],))
        self.step()
        self.assertEqual(self.held(), [])
        self.assertEqual(self.q('SELECT count(*) FROM preparations'), [(0,)])

    def test_undo_keeps_it_waiting(self):
        sid = self.hold(1)[0]
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='completed',undo_until=? WHERE id=?", ((self.clock + dt.timedelta(minutes=5)).isoformat(), sid))
        self.waits(0)
        self.assertEqual(self.step(), [])  # closed: not started
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET status='pending',undo_until=NULL WHERE id=?", (sid,))
        self.assertEqual(self.step(), [sid])

    def test_one_that_looks_done_waits_for_the_answer(self):
        sid = self.hold(1)[0]
        with self.store.connect() as db:
            db.execute("UPDATE suggestions SET handled_hint='x' WHERE id=?", (sid,))
        self.waits(0)
        self.assertEqual((self.step(), self.held()), ([], [sid]))
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET handled_hint=NULL WHERE id=?', (sid,))
        self.assertEqual(self.step(), [sid])

    def test_a_restart_carries_on(self):
        sids = self.hold(2)
        self.start()
        self.app.model_usage = None  # not read yet: not a word on whether it is behind
        self.assertEqual((self.step(), self.held()), ([], sids))
        self.assertEqual(self.q('SELECT count(*) FROM ahead_holds WHERE released_at IS NULL'), [(2,)])
        self.app.model_usage = usage()
        self.assertEqual(self.step(), [])
        self.waits(0)
        self.assertEqual(self.step(), [sids[1]])
        self.start()
        self.behind()
        self.done()
        self.assertEqual(self.step(), [sids[0]])  # let go before the restart

    def test_off_a_plan_or_off_altogether_it_ends(self):
        sids = self.hold(2)
        self.app.model_usage = [{'provider': 'openai', 'windows': []}]  # an API key now
        self.assertEqual(self.step(), [sids[1]])
        self.app.config['prepare_ahead'] = False
        self.assertEqual((self.step(), self.held()), ([], []))

    def test_nothing_waiting_costs_one_read_and_the_backlog_is_asked_once_a_minute(self):
        self.behind()
        with patch.object(review_catch_up, 'waits', side_effect=AssertionError):
            self.assertEqual(self.step(), [])
        self.hold(1)
        with patch.object(review_catch_up, 'waits', return_value=True) as asked:
            self.step()
            for _ in range(5):
                self.app.ahead_hold_step()
            self.assertEqual(asked.call_count, 1)
        self.assertEqual(app_hold.CHECK_SECONDS, 60)


class Delivered(Fake):
    def deliver(self):
        sent = []

        class Noon(dt.datetime):
            @classmethod
            def now(cls, tz=None):
                return dt.datetime(2026, 11, 24, 12, tzinfo=timeutil.local_tz()).astimezone(tz or dt.timezone.utc)
        with patch.object(dt, 'datetime', Noon), patch_everywhere(delivery_telegram, 'telegram', side_effect=lambda *x, **k: (sent.append(x[1]['id']), {'messageId': '7'})[1]):
            deliver.deliver_one(self.store, self.app.config, edit_cards=False)
        return sent

    def test_told_once_when_it_comes_in_and_the_draft_arrives_quietly(self):
        self.behind()
        sid = self.save('a', urgent=False)['id']
        with self.store.connect() as db:
            db.execute('UPDATE suggestions SET deliver_after=NULL')
        self.assertEqual(self.deliver(), [sid])  # with its draft still waiting
        self.waits(0)
        self.assertEqual(self.step(), [sid])
        self.assertEqual(self.q('SELECT needs_edit FROM deliveries'), [(1,)])  # its message shows it is being prepared
        with self.store.connect() as db:
            db.execute("UPDATE deliveries SET needs_edit=0")
            db.execute("UPDATE suggestions SET status='prepared'")
            db.execute("UPDATE preparations SET status='done'")
            db.execute("UPDATE deliveries SET status='queued',reminder=1")
        self.assertEqual(self.deliver(), [])
        self.assertEqual(self.q('SELECT status,reminder,needs_edit FROM deliveries'), [('sent', 0, 1)])

    def test_do_it_meanwhile_pings_as_always(self):
        row = {'id': 'x', 'message_id': '7', 'early': 0, 'status': 'prepared'}
        with self.store.connect() as db:
            self.assertFalse(ahead_hold.quiet(db, row))
            db.execute("INSERT INTO preparations(suggestion_id,job_id,decision_id,status,created_at,updated_at) VALUES('x','j',?,'done',?,?)",
                       (ahead_hold.DECISION + 'y', timeutil.now(), timeutil.now()))
            self.assertFalse(ahead_hold.quiet(db, row))
            self.assertTrue(ahead_hold.quiet(db, {**row, 'early': 1}))
            self.assertFalse(ahead_hold.quiet(db, {**row, 'early': 1, 'message_id': None}))


class Behind(unittest.TestCase):
    def test_one_definition_two_lines(self):
        rows = [json.dumps(n) for n in range(150)]
        self.assertFalse(review_catch_up.behind({'a': 150}, rows, lambda r: 1))
        self.assertTrue(review_catch_up.behind({'a': 150}, rows, lambda r: 1, ahead_hold.EASE_RUNS))
        self.assertLess(ahead_hold.EASE_RUNS, review_catch_up.BEHIND_RUNS)


if __name__ == '__main__':
    unittest.main()

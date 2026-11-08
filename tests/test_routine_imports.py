"""Old OpenClaw jobs as routine suggestions (routine_imports.py, routines.py, routines_app.py, docs/help/routines.md).
OpenClaw's state is only read: a job's schedule becomes a routine's rhythm, OpenClaw's own upkeep never qualifies,
tokens never reach a run. Jobs are sorted one at a time while fewer than three suggestions wait; a sorting run makes a
suggestion with a real preview, a recurring to-do offer, or nothing, and a job is sorted once. Add and No thanks are
the owner's; a week of good runs offers to turn the old job off, which happens only on the owner's tap."""
import datetime as dt
import hashlib
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('imports_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import routine_imports as ri  # noqa: E402
import routines as rt  # noqa: E402

D, T = dt.date, dt.datetime
SESSION = 'agent:main:assistant-review-routine-'
JOB = 'a268718c-b416-4ff7-9875-35c901407432'


def cron(expr):
    return {'kind': 'cron', 'expr': expr, 'tz': 'Europe/Brussels'}


def job_row(job_id, name, prompt, schedule, enabled=1, kind='agentTurn', description=None, order=0):
    return (job_id, name, description, enabled, kind, json.dumps({'schedule': schedule, 'payload': {'kind': kind, 'message': prompt}}), order)


def openclaw(path, rows):
    with closing(sqlite3.connect(path)) as db, db:
        db.execute('CREATE TABLE cron_jobs(job_id TEXT PRIMARY KEY,name TEXT,description TEXT,enabled INTEGER,payload_kind TEXT,'
                   'job_json TEXT,sort_order INTEGER)')
        db.executemany('INSERT INTO cron_jobs VALUES(?,?,?,?,?,?,?)', rows)


class Rhythm(unittest.TestCase):
    today = D(2026, 11, 8)  # a Sunday

    def test_schedules_become_rhythms(self):
        for schedule, want in (
                (cron('0 7 * * *'), ({'unit': 'day', 'n': 1}, D(2026, 11, 8), '07:00')),
                (cron('0 13 * * 1-5'), ({'unit': 'weekday', 'n': 1}, D(2026, 11, 9), '13:00')),
                (cron('0 17 * * 5'), ({'unit': 'week', 'n': 1}, D(2026, 11, 13), '17:00')),
                (cron('17 9 * * 1,4'), ({'unit': 'week', 'n': 1}, D(2026, 11, 9), '09:17')),  # twice a week: weekly on the first
                (cron('0 9 1 * *'), ({'unit': 'month', 'n': 1}, D(2026, 12, 1), '09:00'))):
            self.assertEqual(ri.rhythm(schedule, self.today), want, schedule)
        every = ri.rhythm({'kind': 'every', 'everyMs': 14 * ri.DAY_MS, 'anchorMs': 1776441600000}, self.today)
        self.assertEqual(every[0], {'unit': 'week', 'n': 2})
        self.assertGreaterEqual(every[1], self.today)
        self.assertEqual(ri.rhythm({'kind': 'every', 'everyMs': 88 * ri.DAY_MS, 'anchorMs': 0}, self.today)[0], {'unit': 'month', 'n': 3})

    def test_more_than_once_a_day_never_qualifies(self):
        for schedule in (cron('*/5 * * * *'), cron('0 8,17 * * *'), {'kind': 'every', 'everyMs': 3600000}, {'kind': 'at', 'at': 'x'}, None):
            self.assertIsNone(ri.rhythm(schedule, self.today), schedule)


class Reading(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'openclaw.sqlite'

    def test_only_jobs_that_could_be_routines_and_never_a_write(self):
        prompt = 'Sum up what each developer shipped today from GitHub, short. '
        openclaw(self.path, [
            job_row(JOB, 'Dev summary', prompt + 'token sk-abcdefghijklmnop1234 and Bearer abc.def', cron('0 18 * * *'), order=1),
            job_row('b1', 'Memory upkeep', prompt, cron('0 3 * * *'), description='[managed-by=memory-core] promote'),
            job_row('c2c2c2c2', 'Off', prompt, cron('0 9 * * *'), enabled=0),
            job_row('d3d3d3d3', 'Heartbeat', prompt, {'kind': 'every', 'everyMs': 3600000}, kind='heartbeat'),
            job_row('e4e4e4e4', 'Collector', prompt, cron('45 17 * * *'), kind='command'),
            job_row('f5f5f5f5', 'Old', prompt, cron('0 9 * * *'), description='INACTIVE migrated job'),
            job_row('a6a6a6a6', 'Hourly', prompt, cron('0 * * * *'))])
        before = hashlib.sha256(self.path.read_bytes()).hexdigest()
        got = ri.jobs({'openclaw_state': str(self.path)}, D(2026, 11, 8))
        self.assertEqual([j['id'] for j in got], [JOB])
        self.assertNotIn('sk-abcdefghijklmnop1234', got[0]['prompt'])
        self.assertNotIn('abc.def', got[0]['prompt'])
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), before)
        self.assertTrue(ri.still_on({'openclaw_state': str(self.path)}, JOB))
        self.assertFalse(ri.still_on({'openclaw_state': str(self.path)}, 'c2c2c2c2'))
        self.assertEqual(ri.jobs({'openclaw_state': str(self.path) + '.none'}, D(2026, 11, 8)), [])

    def test_a_long_prompt_keeps_its_end_where_corrections_go(self):
        text = ri.prompt_of({'payload': {'message': 'start ' + 'x ' * 9000 + 'CORRECTION: only weekdays'}})
        self.assertLessEqual(len(text), ri.PROMPT_MAX + 10)
        self.assertTrue(text.startswith('start') and text.endswith('CORRECTION: only weekdays'))

    def test_a_short_name_fits_a_phone_row(self):
        self.assertEqual(rt.short_name('Daily standup summary → memory'), 'Daily standup')
        self.assertEqual(rt.short_name('Monday deals summary'), 'Monday deals')
        self.assertLessEqual(len(rt.short_name('Supercalifragilisticexpialidocious')), rt.SHORT_MAX)


class Sorting(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.claw = Path(self.temp.name) / 'openclaw.sqlite'
        self.jobs = [job_row(f'{i:08d}-job', f'Job {i}', f'Every day sum up thing number {i} for me from my mail.', cron('0 7 * * *'), order=i)
                     for i in range(1, 6)]
        openclaw(self.claw, self.jobs)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'w', 'boundary': 'work:acme.example'}], 'timezone': 'Europe/Brussels',
                           'openclaw_state': str(self.claw)}
        self.now = T(2026, 11, 9, 6, 0)
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.gateway(request))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.sent, self.answer = [], {'start': {'status': 'admitted'}, 'status': {'status': 'pending'}}

    def gateway(self, request):
        self.sent.append(request)
        return self.answer.get(request['action'], {'status': 'unavailable'})

    def act(self, action, owner=True, **args):
        return self.app.action(action, args, owner_dashboard=owner)

    def rows(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routines ORDER BY created_at')]

    def running(self):
        with self.store.connect() as db:
            return db.execute("SELECT id FROM routine_runs WHERE state='running'").fetchone()[0]

    def answer_run(self, **args):
        self.app.routines_step()
        run = self.running()
        self.act('routine_result', owner=False, _routine_session=SESSION + run, **args)
        self.app._routines_jobs_at = 0
        return run

    def test_a_job_becomes_a_suggestion_with_a_real_preview(self):
        self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start']
        self.assertEqual(len(start), 1)
        self.assertIn('thing number 1', start[0]['message'])
        self.assertIn('never send', start[0]['message'])
        self.assertIn('corrections', start[0]['message'])
        self.assertEqual(self.rows()[0]['state'], 'sorting')
        self.assertEqual(self.app.routines_view()['suggested'], [])  # sorting is never shown
        run = self.running()
        with self.assertRaisesRegex(ValueError, 'kind'):
            self.act('routine_result', owner=False, _routine_session=SESSION + run, text='x')
        self.act('routine_result', owner=False, _routine_session=SESSION + run, kind='routine', name='Thing one summary for me',
                 instructions='Sum up thing one from my mail', text='**Thing one** moved.')
        got = self.app.routines_view()
        self.assertEqual(got['routines'], [])
        s = got['suggested'][0]
        self.assertEqual((s['name'], s['instructions'], s['runs'][0]['result'], s['from_openclaw']),
                         ('Thing one summary', 'Sum up thing one from my mail', '**Thing one** moved.', True))
        self.assertLessEqual(len(s['name']), rt.SHORT_MAX)
        self.assertNotIn('origin', s)

    def test_three_suggestions_wait_at_most_and_a_job_is_sorted_once(self):
        for i in range(3):
            self.app._routines_jobs_at = 0
            self.answer_run(kind='routine', name=f'Thing {i}', instructions=f'Sum up thing {i}', text='Something')
        self.app._routines_jobs_at = 0
        self.app.routines_step()
        self.assertEqual(len(self.rows()), 3)  # the fourth waits for an answer
        first = self.app.routines_view()['suggested'][0]['id']
        with self.assertRaises(ValueError):
            self.act('routine_accept', owner=False, id=first)
        self.act('routine_accept', id=first)
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['state'], mine['runs'][0]['result'], mine['next_due']), ('on', 'Something', '2026-11-09'))
        second = self.app.routines_view()['suggested'][0]['id']
        self.act('routine_state', id=second, to='stop')  # No thanks
        self.app._routines_jobs_at = 0
        self.answer_run(kind='routine', name='Thing 3', instructions='Sum up thing 3', text='Something')
        self.answer_run(kind='skip', why='A duplicate')  # one at a time: the fifth only after the fourth
        self.app.routines_step()
        origins = [r['origin'] for r in self.rows()]
        self.assertEqual(len(origins), len(set(origins)))  # never the same job twice
        self.assertEqual(len(origins), 5)

    def test_a_reminder_becomes_a_recurring_to_do_offer_and_a_misfit_is_skipped(self):
        self.answer_run(kind='todo', name='Renew the access key')
        self.answer_run(kind='skip', why='Only posts to a chat')
        with self.store.connect() as db:
            offer = dict(db.execute('SELECT * FROM recurring_offers').fetchone())
        self.assertEqual((offer['key'], offer['source'], offer['title'], json.loads(offer['rule'])),
                         ('openclaw:00000001-job', 'openclaw', 'Renew the access key', {'unit': 'day', 'n': 1}))
        self.assertEqual([r['state'] for r in self.rows()], ['skipped', 'skipped'])
        self.assertEqual(self.app.routines_view(), {'routines': [], 'suggested': [], 'trying': []})

    def test_a_sorting_run_that_didnt_work_runs_once_more_then_the_job_is_skipped(self):
        self.answer['status'] = {'status': 'ok'}  # each turn ends without a report
        for _ in range(6):
            self.app.routines_step()
        first = self.rows()[0]
        self.assertEqual(first['state'], 'skipped')
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM routine_runs WHERE routine_id=? AND state='failed'", (first['id'],)).fetchone()[0], 2)

    def test_a_job_turned_off_in_openclaw_meanwhile_is_skipped_without_a_run(self):
        self.answer['start'] = {'status': 'unavailable'}
        self.app.routines_step()
        with closing(sqlite3.connect(self.claw)) as db, db:
            db.execute('UPDATE cron_jobs SET enabled=0')
        self.answer['start'] = {'status': 'admitted'}
        before = len(self.sent)
        self.app.routines_step()
        self.assertEqual(self.rows()[0]['state'], 'skipped')
        self.assertEqual([s for s in self.sent[before:] if s['action'] == 'start'], [])

    def test_a_week_of_good_runs_offers_to_turn_the_old_job_off_on_a_tap_only(self):
        self.answer_run(kind='routine', name='Thing one', instructions='Sum up thing one', text='Something')
        rid = self.app.routines_view()['suggested'][0]['id']
        self.act('routine_accept', id=rid)
        self.assertFalse(self.app.routines_view()['routines'][0]['old_job'])
        week_ago = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=8)).isoformat()
        with self.store.connect() as db:
            db.execute('UPDATE routines SET accepted_at=? WHERE id=?', (week_ago, rid))
            for day in range(3):
                run = rt.begin(db, rid, f'2026-11-0{day + 1}', (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3 - day)).isoformat())
                rt.finish(db, run, 'nothing' if day else 'ready', 'x', result='ok')
        self.assertTrue(self.app.routines_view()['routines'][0]['old_job'])
        calls = []
        with patch.object(a.App, 'openclaw_job_off', lambda s, job: calls.append(job) or False):
            with self.assertRaisesRegex(ValueError, 'Couldn’t turn the old job off'):
                self.act('routine_old_job', id=rid, choice='off')
        self.assertTrue(self.app.routines_view()['routines'][0]['old_job'])  # still asked
        with self.assertRaises(ValueError):
            self.act('routine_old_job', owner=False, id=rid, choice='off')
        with patch.object(a.App, 'openclaw_job_off', lambda s, job: calls.append(job) or True):
            self.act('routine_old_job', id=rid, choice='off')
        self.assertEqual(calls, ['00000001-job', '00000001-job'])
        self.assertFalse(self.app.routines_view()['routines'][0]['old_job'])  # asked once

    def test_keep_it_never_asks_again_and_never_touches_openclaw(self):
        self.answer_run(kind='routine', name='Thing one', instructions='Sum up thing one', text='Something')
        rid = self.app.routines_view()['suggested'][0]['id']
        self.act('routine_accept', id=rid)
        with patch.object(a.App, 'openclaw_job_off', lambda s, job: self.fail('touched OpenClaw')):
            self.act('routine_old_job', id=rid, choice='keep')
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT old_job FROM routines WHERE id=?', (rid,)).fetchone()[0], 'kept')

    def test_an_older_routines_table_gets_its_new_columns(self):
        with tempfile.TemporaryDirectory() as tmp, closing(sqlite3.connect(Path(tmp) / 'x.sqlite')) as db:
            db.execute('CREATE TABLE routines(id TEXT PRIMARY KEY,name TEXT NOT NULL,instructions TEXT NOT NULL,rule TEXT NOT NULL,'
                       "anchor TEXT NOT NULL,at TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'on',work INTEGER NOT NULL DEFAULT 0,"
                       'version INTEGER NOT NULL DEFAULT 1,next_due TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)')
            rt.ensure(db)
            self.assertTrue({'origin', 'accepted_at', 'old_job'} <= {r[1] for r in db.execute('PRAGMA table_info(routines)')})

    def test_turning_a_job_off_only_turns_that_job_off(self):
        text = (Path(__file__).parent.parent / 'openclaw-cron-off.mjs').read_text()
        self.assertIn("callGatewayFromCli('cron.update'", text)
        self.assertIn('patch:{enabled:false}', text)
        for other in ('cron.remove', 'cron.run', 'cron.add', 'enabled:true'):
            self.assertNotIn(other, text)


if __name__ == '__main__':
    unittest.main()

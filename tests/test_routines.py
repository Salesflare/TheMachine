"""Routines (routines.py, routines_app.py, docs/help/routines.md): work The Machine does on its own, on a rhythm. Plain
words to a rhythm and a time, one run per period (missed days don't stack, a period never runs twice), one run at a
time that waits for the usage budget, three honest ends (Ready, Nothing new, Didn't work: a run that ends without a
result didn't work), a result only from the run's own session, and the owner's Pause, Resume, Change when, Stop and Run
now from the dashboard only. Separate from recurring to-dos: only recurring.py's rhythm math is shared."""
import datetime as dt
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('routines_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import routines as rt  # noqa: E402
import routines_app  # noqa: E402
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS, ROUTINE_ACTIONS  # noqa: E402

D, T = dt.date, dt.datetime
ACCOUNTS = [{'id': 'w', 'boundary': 'work:acme.example'}]
SESSION = 'agent:main:assistant-review-routine-'


class Words(unittest.TestCase):
    today = D(2026, 11, 7)  # a Saturday

    def test_a_routine_in_plain_words(self):
        got = rt.read('every Monday at 9, sum up my open deals', self.today)
        self.assertEqual((got['rule'], got['anchor'], got['at'], got['instructions']), ({'unit': 'week', 'n': 1}, D(2026, 11, 9), '09:00', 'Sum up my open deals'))
        self.assertEqual(rt.read('every weekday at 5:30pm list replies I owe', self.today)['at'], '17:30')
        self.assertEqual(rt.read('elke dag om 7 vat mijn mail samen', self.today)['at'], '07:00')

    def test_a_part_of_the_day_or_no_time(self):
        got = rt.read('every morning tell me what changed in my deals', self.today)
        self.assertEqual((got['rule']['unit'], got['at'], got['instructions']), ('day', '08:00', 'Tell me what changed in my deals'))
        self.assertEqual(rt.read('every Friday list deals that went quiet', self.today)['at'], rt.DEFAULT_AT)

    def test_what_is_missing_is_said(self):
        for words, said in (('', 'Say what it should do and when'), ('sum up my deals', 'Say when it should run'), ('every Monday', 'Say what it should do')):
            with self.assertRaisesRegex(ValueError, said):
                rt.read(words, self.today)
        with self.assertRaises(ValueError):
            rt.clean_at('25:00')


class Dates(unittest.TestCase):
    rule = {'unit': 'day', 'n': 1}

    def row(self, due, state='on', at='09:00'):
        return {'state': state, 'next_due': due, 'rule': '{"unit": "day", "n": 1}', 'anchor': '2026-11-01', 'at': at}

    def test_due_only_once_its_time_passed(self):
        self.assertIsNone(rt.due_period(self.row('2026-11-07'), T(2026, 11, 7, 8, 59)))
        self.assertEqual(rt.due_period(self.row('2026-11-07'), T(2026, 11, 7, 9, 0)), '2026-11-07')
        self.assertIsNone(rt.due_period(self.row('2026-11-07', state='paused'), T(2026, 11, 7, 10)))

    def test_missed_days_dont_stack(self):
        # off from Monday to Saturday morning: only the newest missed date runs (Friday's; Saturday's is at 9)
        self.assertEqual(rt.due_period(self.row('2026-11-02'), T(2026, 11, 7, 8)), '2026-11-06')

    def test_the_first_date(self):
        self.assertEqual(rt.first_due(self.rule, D(2026, 11, 7), '09:00', T(2026, 11, 7, 8)), D(2026, 11, 7))
        self.assertEqual(rt.first_due(self.rule, D(2026, 11, 7), '09:00', T(2026, 11, 7, 10)), D(2026, 11, 8))
        week = {'unit': 'week', 'n': 1}
        self.assertEqual(rt.first_due(week, D(2026, 11, 2), '09:00', T(2026, 11, 7, 10)), D(2026, 11, 9))


class Runs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [dict(x) for x in ACCOUNTS], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}  # no OpenClaw jobs (test_routine_imports.py)
        self.now = T(2026, 11, 9, 6, 0)  # a Monday, early
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: self.paused),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.gateway(request))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.paused, self.sent, self.answer = None, [], {'start': {'status': 'admitted'}, 'status': {'status': 'pending'}}

    def gateway(self, request):
        self.sent.append(request)
        return self.answer.get(request['action'], {'status': 'unavailable'})

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def runs(self):
        with self.store.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM routine_runs ORDER BY started_at')]

    def make(self, words='every Monday at 9, sum up my open deals'):
        return self.act('routine_new', words=words)['made']

    def test_only_the_owner_on_the_dashboard_makes_and_changes_routines(self):
        with self.assertRaises(ValueError):
            self.act('routine_new', owner=False, words='every Monday at 9, sum up my open deals')
        rid = self.make()
        for name, args in (('routine_state', {'id': rid, 'to': 'pause'}), ('routine_run_now', {'id': rid}), ('routine_when', {'id': rid, 'words': 'every day'})):
            with self.assertRaises(ValueError):
                self.act(name, owner=False, **args)
        self.assertTrue(ROUTINE_ACTIONS <= OWNER_ACTIONS & DASHBOARD_ACTIONS)
        self.assertNotIn('routine_result', OWNER_ACTIONS | DASHBOARD_ACTIONS)

    def test_a_due_run_starts_once_and_its_report_is_its_result(self):
        rid = self.make()
        self.app.routines_step()
        self.assertEqual(self.sent, [])  # 6:00, due at 9:00
        self.now = T(2026, 11, 9, 9, 1)
        self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start']
        self.assertEqual(len(start), 1)
        self.assertEqual((start[0]['kind'], start[0]['background']), ('routine', True))
        self.assertIn('never send', start[0]['message'])
        run = self.runs()[0]
        self.assertEqual((run['period'], run['state'], bool(run['admitted_at'])), ('2026-11-09', 'running', True))
        self.app.routines_step(); self.app.routines_step()  # still running: never a second start, never a second run
        self.assertEqual(len([s for s in self.sent if s['action'] == 'start']), 1)
        self.assertEqual(len(self.runs()), 1)
        # the result comes from the run's own session only
        for args, owner in (({'text': 'x'}, False), ({'text': 'x', '_routine_session': SESSION + 'f' * 32}, False),
                            ({'text': 'x', '_routine_session': SESSION + run['id']}, True)):
            with self.assertRaises(ValueError):
                self.act('routine_result', owner=owner, **args)
        self.act('routine_result', owner=False, _routine_session=SESSION + run['id'], text='**2 deals** went quiet.')
        with self.assertRaisesRegex(ValueError, 'over'):
            self.act('routine_result', owner=False, _routine_session=SESSION + run['id'], text='again')
        self.answer['status'] = {'status': 'ok'}
        self.app.routines_step()
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual(mine['id'], rid)
        self.assertEqual((mine['runs'][0]['state'], mine['runs'][0]['result'], mine['next_due']), ('ready', '**2 deals** went quiet.', '2026-11-16'))

    def test_the_first_run_names_a_routine_and_edit_keeps_its_name_unless_it_no_longer_fits(self):
        rid = self.make('every Monday at 9, sum up last week\'s team standup from the chat and the calendar')
        start = lambda: [s for s in self.sent if s['action'] == 'start'][-1]['message']
        result = lambda name: self.app.action('routine_result', {'_routine_session': SESSION + self.runs()[-1]['id'], 'text': 'ok', 'name': name}, owner_dashboard=False)
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertIn('Also pass name: a short name', start())  # no model call of its own: the run it does anyway
        result('Weekly team standup')
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Weekly team')  # at most 18, cut at a word
        self.answer['status'] = {'status': 'ok'}; self.app.routines_step(); del self.answer['status']
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertNotIn('Also pass name', start())
        result('Something else')  # named already: a run never renames it by itself
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Weekly team')
        self.answer['status'] = {'status': 'ok'}; self.app.routines_step(); del self.answer['status']
        self.act('routine_edit', id=rid, words='Sum up last week\'s team standup and the blockers')
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Weekly team')  # Edit keeps it
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertIn('Its name is "Weekly team": pass it again unless it no longer fits.', start())
        result('Standup blockers')
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Standup blockers')

    def test_a_run_that_ends_without_a_result_didnt_work(self):
        self.make('every day at 7 tell me what changed in my deals')
        self.now = T(2026, 11, 9, 7, 1)
        self.app.routines_step()
        self.answer['status'] = {'status': 'ok'}
        self.app.routines_step()
        run = self.app.routines_view()['routines'][0]['runs'][0]
        self.assertEqual((run['state'], run['why']), ('failed', 'It finished without a result.'))
        self.assertNotIn('error', run)

    def test_a_run_past_its_time_is_stopped(self):
        self.make('every day at 7 tell me what changed in my deals')
        self.now = T(2026, 11, 9, 7, 1)
        self.app.routines_step()
        with self.store.connect() as db:
            db.execute("UPDATE routine_runs SET admitted_at='2026-01-01T05:00:00+00:00'")
        self.answer['stop'] = {'status': 'timed_out', 'error': 'runtime_timeout'}
        self.app.routines_step()
        self.assertEqual(self.sent[-1]['action'], 'stop')
        self.assertEqual(self.app.routines_view()['routines'][0]['runs'][0]['why'], 'It took too long.')

    def test_it_waits_for_the_budget_and_runs_one_at_a_time(self):
        self.make('every day at 7 tell me what changed in my deals')
        self.make('every day at 7 list replies I owe')
        self.now = T(2026, 11, 9, 7, 1)
        self.paused = {'window': '5h', 'limited': False}
        self.app.routines_step()
        self.assertEqual(self.sent, [])
        self.paused = None
        self.app.routines_step(); self.app.routines_step()
        self.assertEqual(len([s for s in self.sent if s['action'] == 'start']), 1)
        self.assertEqual(sum(bool(r['admitted_at']) for r in self.runs()), 1)

    def test_a_run_that_couldnt_start_all_day_didnt_work(self):
        self.make('every day at 7 tell me what changed in my deals')
        self.now = T(2026, 11, 9, 7, 1)
        self.paused = {'window': 'limit', 'limited': True}
        self.app.routines_step()
        with self.store.connect() as db:
            db.execute("UPDATE routine_runs SET started_at='2026-01-01T05:00:00+00:00'")
        self.app.routines_step()
        self.assertEqual(self.runs()[0]['state'], 'failed')

    def test_run_now_pause_resume_change_and_stop(self):
        rid = self.make()
        self.act('routine_run_now', id=rid)
        with self.assertRaisesRegex(ValueError, 'running already'):
            self.act('routine_run_now', id=rid)
        self.assertTrue(self.runs()[0]['period'].startswith('now:'))
        self.act('routine_state', id=rid, to='pause')
        self.now = T(2026, 11, 20, 10)
        self.act('routine_state', id=rid, to='resume')  # what was missed while paused doesn't run
        self.assertEqual(self.app.routines_view()['routines'][0]['next_due'], '2026-11-23')
        self.act('routine_when', id=rid, words='every weekday at 8')
        r = self.app.routines_view()['routines'][0]
        self.assertEqual((r['rule']['unit'], r['at'], r['next_due']), ('weekday', '08:00', '2026-11-23'))
        self.act('routine_state', id=rid, to='stop')
        self.assertEqual(self.app.routines_view()['routines'], [])
        with self.assertRaisesRegex(ValueError, 'gone'):
            self.act('routine_run_now', id=rid)

    def test_edit_changes_what_it_does_and_keeps_when_and_its_runs(self):
        rid = self.make()
        self.act('routine_run_now', id=rid)
        before = self.app.routines_view()['routines'][0]
        with self.assertRaises(ValueError):
            self.act('routine_edit', owner=False, id=rid, words='Sum up my won deals')
        with self.assertRaisesRegex(ValueError, 'Say what it should do'):
            self.act('routine_edit', id=rid, words=' ')
        self.act('routine_edit', id=rid, words='Sum up my won deals.  And the lost ones')
        r = self.app.routines_view()['routines'][0]
        self.assertEqual((r['instructions'], r['name']), ('Sum up my won deals. And the lost ones', 'Sum up my won deals'))
        self.assertEqual((r['rule'], r['at'], r['next_due'], len(r['runs'])), (before['rule'], before['at'], before['next_due'], 1))
        with self.store.connect() as db:  # a name of its own stays
            db.execute("UPDATE routines SET name='Deals'")
        self.act('routine_edit', id=rid, words='Sum up my open deals')
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Deals')

    def test_a_weekdays_routine_never_starts_on_a_weekend(self):
        self.now = T(2026, 11, 7, 6)  # a Saturday
        with self.store.connect() as db:
            rid = rt.create(db, 'List replies I owe', {'unit': 'weekday', 'n': 1}, D(2026, 11, 7), '08:00', self.now, 's')
        self.assertEqual(self.app.routines_view()['routines'][0]['next_due'], '2026-11-09')
        self.assertTrue(rid)

    def test_a_period_never_runs_twice(self):
        rid = self.make()
        with self.store.connect() as db:
            self.assertTrue(rt.begin(db, rid, '2026-11-09', 's1'))
            self.assertIsNone(rt.begin(db, rid, '2026-11-09', 's2'))

    def test_the_runner_and_the_plugin_know_the_routine_session(self):
        root = Path(__file__).parent.parent
        self.assertIn("routine:'agent:main:assistant-review-routine-'", (root / 'preparation-run.mjs').read_text())
        self.assertEqual(routines_app.SESSION.pattern, '^' + SESSION + '([a-f0-9]{32})$')


if __name__ == '__main__':
    unittest.main()

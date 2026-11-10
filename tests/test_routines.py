"""Routines (routines.py, routines_app.py, docs/help/routines.md): work The Machine does on its own, on a rhythm. Plain
words to a rhythm and a time, one run per period (missed days don't stack, a period never runs twice), one run at a
time that waits for the usage budget, three honest ends (Ready, Nothing new, Didn't work: a run that ends without a
result didn't work), a result only from the run's own session, and the owner's Pause, Resume, Change when, Stop and Run
now from the dashboard only. Separate from recurring to-dos: only recurring.py's rhythm math is shared."""
import datetime as dt
import importlib.util
import shlex
import sys
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
        self.store.accounts = self.app.config['accounts']  # as the App sets it (machine/main.py)
        self.now = T(2026, 11, 9, 6, 0)  # a Monday, early
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: self.paused),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.gateway(request)),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):  # script steps inline
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

    def test_before_its_first_run_a_routine_has_a_short_name_from_its_words(self):
        words = 'check what shipped functionally for the project in the open source repository and summarize it for the blog'
        rid = self.make('every Friday at 4, ' + words)
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual(mine['name'], 'Check what shipped')  # a phone's title line, never the whole prompt cut short
        self.assertLessEqual(len(mine['name']), rt.PLACEHOLDER_MAX)
        with self.store.connect() as db:  # one made before names were short: it gets short, and its first run still names it
            db.execute('UPDATE routines SET name=? WHERE id=?', (rt._long_name_of(mine['instructions']), rid))
            self.assertGreater(len(db.execute('SELECT name FROM routines').fetchone()[0]), 60)
            rt.ensure(db)
            row = db.execute('SELECT * FROM routines WHERE id=?', (rid,)).fetchone()
        self.assertEqual(row['name'], 'Check what shipped')
        self.assertTrue(rt.needs_name(row))
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.app.action('routine_result', {'_routine_session': SESSION + self.runs()[-1]['id'], 'text': 'ok', 'name': 'Shipped this week'}, owner_dashboard=False)
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Shipped this week')

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

    def test_edit_takes_the_owners_name_and_no_run_renames_it(self):
        rid = self.make('every Monday at 9 sum up my open deals')
        edit = lambda words, **more: self.app.action('routine_edit', {'id': rid, 'words': words, **more}, owner_dashboard=True)  # noqa: E731 (act's own name)
        for bad, why in (('  ', 'Give it a name'), ('x' * 81, 'under 80 characters')):
            with self.assertRaisesRegex(ValueError, why):
                edit('Sum up my open deals', name=bad)
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Sum up my open deals')  # nothing kept
        edit('Sum up my open deals', name='  Deals   digest ')
        r = self.app.routines_view()['routines'][0]
        self.assertEqual((r['name'], r['instructions']), ('Deals digest', 'Sum up my open deals'))
        edit('Sum up my won deals')  # new words keep the owner's name
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Deals digest')
        with self.store.connect() as db:
            row = rt.get(db, rid)
            self.assertFalse(rt.needs_name(row))  # a run never asks for a name
            rt.named(db, rid, 'Won deals', 'now')
            rt.ensure(db)
        self.assertEqual(self.app.routines_view()['routines'][0]['name'], 'Deals digest')
        edit('Sum up my won deals', name='Sum up my won deals')  # even the words' own start
        with self.store.connect() as db:
            self.assertFalse(rt.needs_name(rt.get(db, rid)))

    def test_change_names_a_new_one_on_trial_and_its_words_never_rename_it(self):
        tr = lambda **args: self.app.action('routine_try', args, owner_dashboard=True)  # noqa: E731 (act's own name)
        rid = tr(words='every Monday at 9, sum up my open deals')['made']

        def done():  # its test run ended: the next Change may run
            with self.store.connect() as db:
                db.execute("UPDATE routine_runs SET state='ready',result='x'")
        done()
        tr(id=rid, words='Sum up my open deals', name='  Deals   digest ')
        done()
        r = self.app.routines_view()['trying'][0]
        self.assertEqual(r['name'], 'Deals digest')
        tr(id=rid, words='Sum up my won deals')  # new words keep the owner's name
        done()
        with self.store.connect() as db:
            row = rt.get(db, rid, ('trying',))
            self.assertEqual(row['name'], 'Deals digest')
            self.assertFalse(rt.needs_name(row))
        with self.assertRaisesRegex(ValueError, 'Give it a name'):
            tr(id=rid, words='Sum up my won deals', name=' ')

    def tables(self):
        """Every row outside the routines' own tables: a test run must leave them as they were. data_stamps only counts
        writes to tables the to-dos' views read (routines among them), for their cache."""
        with self.store.connect() as db:
            names = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'routine%' "
                                               "AND name NOT LIKE 'sqlite_%' AND name<>'data_stamps'")]
            return {n: [tuple(r) for r in db.execute(f'SELECT * FROM "{n}"')] for n in names}

    def report(self, text, **more):
        self.app.action('routine_result', {'_routine_session': SESSION + self.runs()[-1]['id'], 'text': text, **more}, owner_dashboard=False)
        self.answer['status'] = {'status': 'ok'}; self.app.routines_step(); del self.answer['status']

    def test_a_new_routine_is_tried_first_and_kept_only_on_add(self):
        before = self.tables()
        rid = self.act('routine_try', words='every Monday at 9, sum up last week\'s team standup from the chat')['made']
        view = self.app.routines_view()
        self.assertEqual(view['routines'], [])  # not kept, not scheduled
        self.assertEqual((view['trying'][0]['id'], view['trying'][0]['test']['state'], view['trying'][0]['next_due']), (rid, 'running', None))
        with self.assertRaisesRegex(ValueError, 'running already'):  # one run per press
            self.act('routine_try', id=rid, words='Sum up the standup')
        self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start']
        self.assertEqual(len(start), 1)  # the owner pressed it: no wait for the next date
        self.assertEqual(start[0]['kind'], 'routine')  # the plugin's read-only routine session (test_review_hooks.mjs)
        self.assertIn('This is a test run', start[0]['message'])
        self.report('**3 blockers** this week.', name='Team standup')
        # dry: nothing outside the routine's own rows changed, and the Gateway only started it and asked how it went
        self.assertEqual(self.tables(), before)
        self.assertLessEqual({s['action'] for s in self.sent}, {'start', 'status'})
        trying = self.app.routines_view()['trying'][0]
        self.assertEqual((trying['name'], trying['test']['result'], trying['runs']), ('Team standup', '**3 blockers** this week.', []))
        self.act('routine_accept', id=rid)
        view = self.app.routines_view()
        self.assertEqual(view['trying'], [])
        mine = view['routines'][0]
        self.assertEqual((mine['state'], mine['next_due'], mine['test']), ('on', '2026-11-09', None))
        self.assertEqual(mine['runs'][0]['result'], '**3 blockers** this week.')  # Add keeps what it showed

    def test_cancel_drops_a_new_one_and_another_try_replaces_it(self):
        first = self.act('routine_try', words='every day at 7, tell me what changed in my deals')['made']
        second = self.act('routine_try', words='every Friday, sum up my week')['made']
        self.assertEqual([r['id'] for r in self.app.routines_view()['trying']], [second])  # one at a time
        self.act('routine_state', id=second, to='stop')
        self.assertEqual(self.app.routines_view()['trying'], [])
        self.assertEqual(self.runs(), [])
        with self.assertRaises(ValueError):
            self.act('routine_accept', id=first)

    def test_a_job_that_ends_in_a_post_reads_up_to_it_and_drafts_it(self):
        words = 'every day at 9, check what shipped in the open source repo and draft a short post on X'
        rid = self.make(words)
        post = {'title': 'Post on X about the faster search', 'text': 'Two new things shipped today.', 'act': 'post'}
        self.act('routine_try', id=rid, words='Check what shipped in the open source repo and draft a short post on X'); self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        for said in ('the browser to look', 'gh or git commands that only read', 'Would post on X', 'nothing goes out.',
                     'what it is about and where it goes, specific and short', 'act: post or send',
                     'This is its first run: what is new means the last 24 hours, since Sunday 2026-11-08 06:00'):
            self.assertIn(said, start)
        self.assertNotIn('You can only read', start)
        self.report('Would post on X: Two new things shipped today.', draft=post)
        with self.store.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM suggestions').fetchone()[0], 0)  # a test run only shows it
        self.act('routine_run_now', id=rid); self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        self.assertIn('a to-do to approve; nothing goes out without them', start)
        self.assertIn('This is its first run', start)  # a test run is not the last run
        with self.assertRaisesRegex(ValueError, 'draft needs title'):
            self.report('Would post on X: hi', draft='hi')
        with self.assertRaisesRegex(ValueError, 'draft act is post or send'):
            self.report('Would post on X: hi', draft={**post, 'act': 'publish'})
        self.report('Would post on X: Two new things shipped today.', draft=post, name='Check what shipped')
        with self.store.connect() as db:
            self.assertEqual([tuple(r) for r in db.execute('SELECT title,body FROM suggestions')], [('Post on X about the faster search', 'Two new things shipped today.')])
            card = dict(db.execute('SELECT * FROM suggestions').fetchone())
            view = self.store.suggestion_result(card, db)
        # The to-do says it is the routine's, by the routine's name (its name now: this run named it), with a link to it
        # while the routine is on the Routines page, and its button names the step
        # (the day is the day the draft was made, by the real clock: any day, not the one this test was written on)
        self.assertRegex(card['source_line'], r'^Source: your routine Check what shipped in the · [A-Z][a-z]{2}, [A-Z][a-z]{2} \d{1,2}$')
        self.assertEqual(view['routine'], {'id': rid, 'name': 'Check what shipped', 'live': True})
        self.assertEqual(view['labels'], {'accept': 'Post it'})
        self.now = T(2026, 11, 10, 9, 30)
        self.act('routine_run_now', id=rid); self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        self.assertIn('The last run started', start)
        self.assertNotIn('This is its first run', start)
        # Stopped: no longer on the Routines page, so no link, and the name it had
        self.act('routine_state', id=rid, to='stop')
        with self.store.connect() as db:
            view = self.store.suggestion_result(card, db)
        self.assertEqual(view['routine'], {'id': rid, 'name': 'Check what shipped in the', 'live': False})

    def test_a_draft_starts_in_the_area_of_the_account_it_goes_out_from(self):
        # A Personal routine whose post is a company's product news, from that company's X account: its to-do starts in
        # that company's Work with its accounts, so its run has what it needs and never stops to ask for a move
        mine = [{'id': 'home-phone', 'service': 'android', 'boundary': 'personal:phone'},
                {'id': 'acme-mail', 'service': 'gmail', 'email': 'robin@acme.example', 'boundary': 'work:Acme'},
                {'id': 'side-x', 'service': 'x', 'boundary': 'work:Side Labs'},
                {'id': 'gateway', 'service': 'gateway', 'boundary': 'owner:system'}]
        self.app.config['accounts'] = self.store.accounts = mine
        rid = self.make('every day at 9, check what shipped in the open source repo and draft a short post on X')
        self.act('routine_run_now', id=rid); self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        self.assertIn('Accounts: home-phone (android, Personal), acme-mail (gmail, Work at acme.example), side-x (x, Work at Side Labs).', start)
        self.assertIn('account: the id of the account it goes out from', start)
        post = {'title': 'Post on X about the faster search', 'text': 'Two new things shipped today.', 'act': 'post'}
        with self.assertRaisesRegex(ValueError, 'draft account is the id of the account it goes out from: home-phone, acme-mail, side-x'):
            self.report('Would post on X: hi', draft={**post, 'account': 'gateway'})
        self.report('Would post on X: Two new things shipped today.', draft={**post, 'account': 'side-x'})
        with self.store.connect() as db:
            card = dict(db.execute('SELECT * FROM suggestions').fetchone())
            source = db.execute('SELECT account_id FROM events WHERE kind=?', ('routine.draft',)).fetchone()[0]
        self.assertEqual((card['area'], card['account_ids'], source), ('work:Side Labs', '["side-x"]', 'side-x'))
        # Without an account it keeps the routine's side, as before
        self.now = T(2026, 11, 10, 9, 30)
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.report('Would post on X: One more thing shipped.', draft={**post, 'text': 'One more thing shipped.'})
        with self.store.connect() as db:
            later = dict(db.execute("SELECT * FROM suggestions WHERE id!=?", (card['id'],)).fetchone())
        self.assertEqual((later['area'], later['account_ids']), (None, '["home-phone"]'))

    def test_try_it_shows_new_words_without_changing_the_routine(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        self.act('routine_run_now', id=rid); self.app.routines_step(); self.report('2 open deals.', name='Open deals')
        before = self.tables()
        self.act('routine_try', id=rid, words='Sum up my open deals and who to call first')
        self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        self.assertIn('who to call first', start)
        self.assertNotIn('Also pass name', start)
        self.assertIn('The last result', start)  # what changed since the kept result
        self.report('Call the first one.', name='Something else')
        self.assertEqual(self.tables(), before)
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['name'], mine['version'] if 'version' in mine else 1, mine['runs'][0]['result']), ('Open deals', 1, '2 open deals.'))
        self.assertNotIn('call first', mine['instructions'])
        self.assertEqual((mine['test']['result'], mine['test']['trial']), ('Call the first one.', 'Sum up my open deals and who to call first'))
        with self.store.connect() as db:
            self.assertEqual(rt.last_result(db, rid)['result'], '2 open deals.')  # never the next run's "last time"
        self.act('routine_edit', id=rid, words='Sum up my open deals and who to call first')
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['instructions'], mine['runs'][0]['result'], mine['test']), ('Sum up my open deals and who to call first', 'Call the first one.', None))
        self.act('routine_try', id=rid, words='Something else entirely'); self.app.routines_step(); self.report('x')
        self.act('routine_edit', id=rid, words='Sum up my open deals, briefly')  # saved other words: that try goes
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['runs'][0]['result'], mine['test']), ('Call the first one.', None))

    def test_a_run_follows_the_owners_skills_that_fit_and_says_which(self):
        import skills
        with self.store.connect() as db:
            skills.ensure(db)
            for slug, name, desc, body, status in (
                    ('team-standup', 'Team standup', 'How I sum up the standup', 'One line per person: shipped, next, blocked.', 'on'),
                    ('blog-voice', 'Blog voice', 'How posts for the team blog sound', 'Short, playful, no jargon.', 'on'),
                    ('old-way', 'Old standup way', 'Not used now', 'Long paragraphs.', 'off')):
                db.execute("INSERT INTO skills(id,slug,name,description,body,status,origin,sha,created_at,updated_at) "
                           "VALUES(?,?,?,?,?,?,'mine','x','s','s')", (slug, slug, name, desc, body, status))
        rid = self.make('every Monday at 9, sum up the team standup from the chat')
        self.act('routine_run_now', id=rid); self.app.routines_step()
        start = [s for s in self.sent if s['action'] == 'start'][-1]['message']
        self.assertIn('Skill Team standup (it fits this routine', start)
        self.assertIn('One line per person', start)  # the one that fits, in full
        self.assertIn('- Blog voice: How posts for the team blog sound', start)  # another only by name and what it is for
        self.assertNotIn('Short, playful', start)
        self.assertNotIn('Old standup way', start)  # off: never offered
        self.assertIn('never makes a routine send', start)
        self.report('**Avery**: shipped the export.', skills=['team standup', 'Old standup way', 'Made up'])
        run = self.app.routines_view()['routines'][0]['runs'][0]
        self.assertEqual(run['used'], ['Team standup'])  # only skills that are on, by their own name

    def test_without_skills_the_prompt_says_nothing_of_them(self):
        rid = self.make()
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertNotIn('skill', [s for s in self.sent if s['action'] == 'start'][-1]['message'].lower())
        self.report('ok')
        self.assertEqual(self.app.routines_view()['routines'][0]['runs'][0]['used'], [])

    @staticmethod
    def py(code):
        """A Get data or Check command: this Python running code."""
        return shlex.join([sys.executable, '-c', code])

    def starts(self):
        return [s for s in self.sent if s['action'] == 'start']

    def test_get_data_runs_first_and_its_output_goes_to_the_run(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        for action in ('routine_edit', 'routine_try'):  # script steps are the owner's, on the dashboard only
            with self.assertRaises(ValueError):
                self.app.action(action, {'id': rid, 'words': 'x', 'steps': {'get': {'command': 'true'}}}, owner_dashboard=False)
        self.assertEqual(self.app.routines_view()['routines'][0]['steps'], {})
        self.act('routine_edit', id=rid, words='Sum up my open deals', steps={'get': {
            'command': self.py("import os; print('3 open deals in', os.getcwd(), 'key sk-abcdefghijklmnop1234')"), 'cwd': self.temp.name}})
        self.assertEqual(self.app.routines_view()['routines'][0]['steps']['get']['timeout'], 60)
        self.act('routine_run_now', id=rid)
        self.app.routines_step()  # Get data first: no turn yet
        self.assertEqual(self.starts(), [])
        self.assertEqual(self.app.routines_view()['routines'][0]['runs'][0]['state'], 'running')
        self.app.routines_step()
        message = self.starts()[0]['message']
        self.assertIn('Get data ran on the owner\'s Machine', message)
        self.assertIn('3 open deals in ' + self.temp.name, message)  # in its folder
        self.assertNotIn('sk-abcdefghijklmnop1234', message)  # token-like strings never reach a run
        self.report('**3** open deals.')
        self.assertEqual(self.app.routines_view()['routines'][0]['runs'][0]['result'], '**3** open deals.')

    def test_with_no_words_the_output_is_the_result_and_check_says_if_it_worked(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        get = {'command': self.py("print('**Ready:** 2 renewals')")}
        self.act('routine_edit', id=rid, words='', steps={'get': get})
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertEqual(self.starts(), [])  # no model turn at all
        run = self.app.routines_view()['routines'][0]['runs'][0]
        self.assertEqual((run['state'], run['result'], run['got']), ('ready', '**Ready:** 2 renewals', True))
        check = self.py("import sys; t = sys.stdin.read(); sys.exit(0 if 'Ready' in t else 'no Ready line')")
        self.act('routine_edit', id=rid, words='', steps={'get': get, 'check': {'command': check}})
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.assertEqual(self.app.routines_view()['routines'][0]['runs'][0]['state'], 'ready')  # the check passed
        self.act('routine_edit', id=rid, words='', steps={'get': {'command': self.py("print('nothing to see')")}, 'check': {'command': check}})
        self.act('routine_run_now', id=rid); self.app.routines_step()
        run = self.app.routines_view()['routines'][0]['runs'][0]
        self.assertEqual((run['state'], run['why'], run['detail']), ('failed', 'The check said it didn’t work.', 'no Ready line'))

    def test_a_check_after_the_runs_own_result(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        self.act('routine_edit', id=rid, words='Sum up my open deals', steps={'check': {'command': self.py('import sys; sys.exit(3)')}})
        self.act('routine_run_now', id=rid); self.app.routines_step()
        self.app.action('routine_result', {'_routine_session': SESSION + self.runs()[-1]['id'], 'text': 'Two deals.'}, owner_dashboard=False)
        run = self.app.routines_view()['routines'][0]['runs'][0]
        self.assertEqual((run['state'], run['why']), ('failed', 'The check said it didn’t work.'))

    def test_get_data_that_fails_or_takes_too_long_didnt_work(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        for step, said in (({'command': self.py("import sys; sys.exit('no such report')")}, 'no such report'),
                           ({'command': self.py('import time; time.sleep(5)'), 'timeout': 1}, 'timeout after 1 s'),
                           ({'command': 'no-such-command-here'}, 'No such file or directory')):
            self.act('routine_edit', id=rid, words='Sum up my open deals', steps={'get': step})
            self.act('routine_run_now', id=rid); self.app.routines_step()
            run = self.app.routines_view()['routines'][0]['runs'][0]
            self.assertEqual((run['state'], run['why']), ('failed', 'Get data didn’t work.'))
            self.assertIn(said, run['detail'])
        self.assertEqual(self.starts(), [])
        with self.assertRaisesRegex(ValueError, '1 to 600'):
            self.act('routine_edit', id=rid, words='x y z w', steps={'get': {'command': 'true', 'timeout': 9999}})
        with self.assertRaisesRegex(ValueError, 'open quote'):
            self.act('routine_edit', id=rid, words='x y z w', steps={'get': {'command': 'echo "open'}})

    def test_a_test_run_runs_get_data_too_and_says_so(self):
        rid = self.make('every Monday at 9, sum up my open deals')
        self.act('routine_try', id=rid, words='', steps={'get': {'command': self.py("print('fresh numbers')")}})
        self.app.routines_step()
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['test']['result'], mine['test']['got']), ('fresh numbers', True))
        self.assertEqual(mine['steps'], {})  # Try it never changes the routine
        self.assertEqual(mine['runs'], [])

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

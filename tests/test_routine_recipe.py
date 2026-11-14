"""A routine's recipe (routine_recipe.py, docs/help/routines.md): the Machine writes the reading part of a routine
itself, from a run's own report; the next runs read it in plain code before the turn, which only judges and writes.
Only reads pass (the Machine's events, and gh or git commands that only read), checked again each run; dates are
filled in by the Machine; a recipe that fails hands the reading back to the turn, which repairs it, and goes after
three runs without a repair. New words drop it; the owner's Get data comes first."""
import datetime as dt
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('recipe_assistant', Path(__file__).parent.parent.joinpath('assistant.py'))
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
import routine_recipe as rr  # noqa: E402

T = dt.datetime
SESSION = 'agent:main:assistant-review-routine-'
INVOICES = {'events': {'query': 'invoice', 'kinds': ['gmail.message'], 'limit': 10, 'since_days': 30}}


class Clean(unittest.TestCase):
    def test_only_reads_pass(self):
        ok = rr.clean({'steps': [INVOICES, {'command': ['gh', 'pr', 'list', '--repo', 'acme/widgets', '--state', 'merged',
                                                       '--search', 'merged:>={since}', '--json', 'number,title']},
                                 {'command': ['git', '-C', '~/code/site', 'log', '--since={days_ago:7}', '--oneline']},
                                 {'command': ['gh', 'api', 'repos/acme/widgets/releases', '-X', 'GET']}]})
        self.assertEqual(len(ok['steps']), 4)
        for argv in (['gh', 'pr', 'create'], ['gh', 'pr', 'merge', '1'], ['gh', 'api', 'repos/x/y/issues', '-X', 'POST'],
                     ['gh', 'api', 'repos/x/y/issues', '-f', 'title=x'], ['gh', 'api', 'graphql'], ['gh', 'pr', 'view', '1', '--web'],
                     ['git', 'push'], ['git', 'ls-remote', '--upload-pack=touch /tmp/x', 'origin'], ['git', '-c', 'core.pager=sh', 'log'],
                     ['git', 'log', '--output=/tmp/x'], ['git', 'diff', '--ext-diff'], ['rm', '-rf', '~'], ['sh', '-c', 'gh pr list'],
                     ['python3', '-c', 'print(1)'], ['gh', 'pr', 'list', '$(id)'], ['git', 'log', '{home}']):
            with self.assertRaises(ValueError, msg=argv):
                rr.clean({'steps': [{'command': argv}]})
        for bad in ({'steps': []}, {'steps': [INVOICES] * 5}, {'steps': [{'events': {'kinds': ['not a kind']}}]},
                    {'steps': [{'events': {'limit': 400}}]}, {'steps': [{'events': {'since_days': 900}}]}, {'steps': [{'web': 'x'}]}):
            with self.assertRaises(ValueError, msg=bad):
                rr.clean(bad)

    def test_the_machine_fills_in_the_dates(self):
        now, since = T(2026, 11, 13, 16, 0), T(2026, 11, 6, 16, 0)
        self.assertEqual(rr.fill(['gh', 'search', 'prs', 'merged:>={since}', 'until {today}', '{days_ago:7}', '{days_ahead:3}'], now, since),
                         ['gh', 'search', 'prs', 'merged:>=2026-11-06', 'until 2026-11-13', '2026-11-06', '2026-11-16'])
        self.assertEqual(rr.fill(['x{since}'], now, None), ['x2026-11-12'])  # no run yet: a day ago


class Runs(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = a.Store(Path(self.temp.name) / 'e.sqlite')
        self.app = object.__new__(a.App); self.app.store = self.store
        self.app.config = {'accounts': [{'id': 'w', 'boundary': 'work:acme.example'}], 'timezone': 'Europe/Brussels',
                           'openclaw_state': self.temp.name + '/none.sqlite'}
        self.now = T(2026, 11, 9, 6, 0)
        for name, value in (('routines_now', lambda s: self.now), ('background_pause', lambda s, **k: None),
                            ('background_spaced', lambda s: True), ('background_started', lambda s: None),
                            ('preparation_gateway', lambda s, request: self.sent.append(request) or {'status': 'admitted'}),
                            ('routine_spawn', lambda s, target, run_id: target(run_id))):
            p = patch.object(a.App, name, value); p.start(); self.addCleanup(p.stop)
        self.sent = []
        stamp = self.now.replace(tzinfo=dt.timezone.utc)  # the routine's clock, so "40 days back" stays past since_days
        self.store.commit_page('w', {}, [
            {'account_id': 'w', 'source_id': f'm{i}', 'kind': 'gmail.message', 'occurred_at': (stamp - dt.timedelta(days=d)).isoformat(),
             'title': title, 'body': body, 'metadata': {'from': 'billing@example.org'}, 'deleted': False}
            for i, (d, title, body) in enumerate(((2, 'Invoice 4411 from Northwind', 'Due Nov 14, $1,200'),
                                                  (40, 'Invoice 3900 from Corvid', 'Due Oct 1, paid'),
                                                  (1, 'Lunch on Friday?', 'Just lunch, at the usual place')))])
        self.repo = Path(self.temp.name) / 'repo'; self.repo.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)

    def act(self, name, owner=True, **args):
        return self.app.action(name, args, owner_dashboard=owner)

    def run_now(self, rid):
        self.act('routine_run_now', id=rid); self.app.routines_step(); self.app.routines_step()
        return self.start()

    def start(self):
        return [s for s in self.sent if s['action'] == 'start'][-1]['message']

    def last_run(self):
        with self.store.connect() as db:
            return dict(db.execute('SELECT * FROM routine_runs ORDER BY started_at DESC, rowid DESC LIMIT 1').fetchone())

    def report(self, **args):
        return self.act('routine_result', owner=False, _routine_session=SESSION + self.last_run()['id'], **args)

    def test_a_run_writes_a_recipe_and_the_next_one_reads_it_first(self):
        rid = self.act('routine_new', words='every Monday at 9, list the invoices due this week')['made']
        message = self.run_now(rid)
        self.assertIn('also pass recipe', message)  # no recipe yet: the turn may write one
        recipe = {'steps': [INVOICES, {'command': ['git', '-C', str(self.repo), 'status', '--short']}]}
        self.assertEqual(self.report(text='**Northwind** 4411, due Nov 14', recipe=recipe)['recipe'], 'kept')
        self.assertEqual(self.app.routines_view()['routines'][0]['recipe'],
                         ['events query="invoice" kinds=gmail.message since_days=30 limit=10',
                          f'git -C {self.repo} status --short'])
        message = self.run_now(rid)
        self.assertIn('already read this with the routine\'s recipe', message)
        self.assertIn('Invoice 4411 from Northwind', message)
        self.assertNotIn('Invoice 3900', message)  # 40 days back: past since_days
        self.assertNotIn('Lunch on Friday', message)  # not an invoice
        self.assertNotIn('also pass recipe', message)
        self.assertEqual(json.loads(self.last_run()['recipe']), {'ok': True})

    def test_a_recipe_that_fails_goes_back_to_the_turn_which_repairs_it(self):
        rid = self.act('routine_new', words='every Monday at 9, list the invoices due this week')['made']
        self.run_now(rid)
        broken = {'steps': [{'command': ['git', '-C', str(Path(self.temp.name) / 'gone'), 'status']}]}
        self.report(text='x', recipe=broken)
        for i in range(rr.REPAIR_TRIES):
            message = self.run_now(rid)
            self.assertIn('recipe didn\'t work this time', message)
            self.assertIn('pass recipe: a repaired one', message)
            if i < rr.REPAIR_TRIES - 1:
                self.assertIsNotNone(self.app.routines_view()['routines'][0]['recipe'])
            self.report(text='read it myself')
        self.assertIsNone(self.app.routines_view()['routines'][0]['recipe'])  # three runs without a repair: gone
        self.assertIn('also pass recipe', self.run_now(rid))
        self.report(text='y', recipe={'steps': [INVOICES]})  # a repair is kept, and counts from 0
        self.assertIn('already read this', self.run_now(rid))

    def test_a_recipe_that_doesnt_pass_is_not_kept_and_the_result_still_is(self):
        rid = self.act('routine_new', words='every Monday at 9, list the invoices due this week')['made']
        self.run_now(rid)
        said = self.report(text='**Northwind**', recipe={'steps': [{'command': ['gh', 'pr', 'merge', '7']}]})
        self.assertTrue(said['recipe'].startswith('not kept'))
        mine = self.app.routines_view()['routines'][0]
        self.assertEqual((mine['recipe'], mine['runs'][0]['result']), (None, '**Northwind**'))
        with self.store.connect() as db:  # a recipe changed behind its back is checked again before it runs
            db.execute('UPDATE routines SET recipe=? WHERE id=?', (json.dumps({'steps': [{'command': ['rm', '-rf', '/tmp/x']}]}), rid))
        message = self.run_now(rid)
        self.assertIn('recipe didn\'t work this time (It no longer passes the read-only check)', message)

    def test_new_words_drop_it_and_a_try_of_other_words_never_writes_or_reads_one(self):
        rid = self.act('routine_new', words='every Monday at 9, list the invoices due this week')['made']
        self.run_now(rid)
        self.report(text='x', recipe={'steps': [INVOICES]})
        self.act('routine_try', id=rid, words='List the overdue invoices')
        self.app.routines_step(); message = self.start()
        self.assertNotIn('recipe', message)
        self.assertTrue(self.report(text='y', recipe={'steps': [INVOICES]})['recipe'].startswith('not kept'))
        self.assertIsNotNone(self.app.routines_view()['routines'][0]['recipe'])  # the routine's own stays
        self.act('routine_edit', id=rid, words='List the overdue invoices')
        self.assertIsNone(self.app.routines_view()['routines'][0]['recipe'])

    def test_the_owners_get_data_comes_first(self):
        rid = self.act('routine_new', words='every Monday at 9, list the invoices due this week')['made']
        self.run_now(rid)
        self.report(text='x', recipe={'steps': [INVOICES]})
        self.act('routine_edit', id=rid, words='List the invoices due this week', steps={'get': {'command': 'echo owner data'}})
        message = self.run_now(rid)
        self.assertIn('owner data', message)
        self.assertNotIn('recipe', message)


if __name__ == '__main__':
    unittest.main()

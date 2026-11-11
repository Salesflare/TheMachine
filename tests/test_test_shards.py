"""scripts/test_shards.py, scripts/test_impact.py merge and scripts/ci_runs.py: a full run splits the test files into
shards of about equal time and runs every file exactly once, the shards' test-impact maps add up to the map one job
would make, and a push to main builds on the newest commit under it whose full run passed."""
import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


shards = load('test_shards')
impact = load('test_impact')
ci = load('ci_runs')


class Shards(unittest.TestCase):
    def test_every_file_runs_once(self):
        files = shards.every_test()
        self.assertGreater(len(files), 100)
        for count in (1, 3, 4, 7):
            got = shards.split(files, {}, count)
            self.assertEqual(len(got), count)
            flat = [name for shard in got for name in shard]
            self.assertEqual(sorted(flat), sorted(files))

    def test_shards_take_about_as_long_and_list_the_longest_first(self):
        files = [f'test_{i}.py' for i in range(40)]
        seconds = {name: float(5 + (i * 37) % 120) for i, name in enumerate(files)}
        got = shards.split(files, seconds, 4)
        totals = [sum(seconds[name] for name in shard) for shard in got]
        self.assertLessEqual(max(totals) - min(totals), max(seconds.values()))
        for shard in got:
            self.assertEqual(shard, sorted(shard, key=lambda name: -seconds[name]))

    def test_a_file_the_map_does_not_know_is_guessed_from_its_size(self):
        files = shards.every_test()[:20]
        known = {name: 10.0 for name in files[:10]}
        took = shards.estimate(files, known)
        self.assertEqual(set(took), set(files))
        self.assertTrue(all(took[name] > 0 for name in files))

    def test_fewer_files_than_shards(self):
        self.assertEqual(shards.split(['test_a.py'], {}, 4), [['test_a.py']])
        self.assertEqual(shards.split([], {}, 4), [[]])

    def test_a_small_selection_stays_one_job(self):
        files = shards.every_test()
        self.assertEqual(shards.needed(files[:5], {}, 4, 1800), 1)
        self.assertEqual(shards.needed(files, {}, 4, 1800), 4)
        self.assertEqual(shards.needed(files, {}, 4, 0), 4)
        self.assertEqual(shards.needed(files[:2], {files[0]: 2000.0, files[1]: 1000.0}, 4, 1800), 2)

    def test_durations_come_from_the_map(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder, 'map.json.gz')
            with gzip.open(path, 'wt', encoding='utf-8') as sink:
                json.dump({'tests': ['test_a.py'], 'seconds': {'test_a.py': 12.5, 'test_b.mjs': 'x'}}, sink)
            self.assertEqual(shards.recorded(path), {'test_a.py': 12.5})
            self.assertEqual(shards.recorded(Path(folder, 'missing.json.gz')), {})


class Base(unittest.TestCase):
    """What a run of main proved, from its artifacts' names, and the commit the next push's selection starts from."""

    def api(self, runs, artifacts):
        def call(path):
            if '/artifacts' in path:
                return {'artifacts': [{'name': n} for n in artifacts.get(int(path.split('/runs/')[1].split('/')[0]), [])]}
            if 'head_sha=' in path:
                sha = path.split('head_sha=')[1].split('&')[0]
                return {'workflow_runs': [r for r in runs if r['head_sha'] == sha]}
            return {'workflow_runs': runs}
        return call

    def ci_run(self, id, sha, event='push', conclusion='success'):
        return {'id': id, 'head_sha': sha, 'event': event, 'conclusion': conclusion}

    def test_the_newest_full_run_under_head(self):
        a, b, c, other = 'a' * 40, 'b' * 40, 'c' * 40, 'd' * 40
        runs = [self.ci_run(5, other), self.ci_run(4, c), self.ci_run(3, b, event='pull_request'), self.ci_run(2, b), self.ci_run(1, a, event='schedule')]
        artifacts = {5: ['tested-full'], 4: [f'tested-since-{a}'], 2: ['tested-full']}
        under = {a, b, c}  # other is on another branch
        found = ci.base(c, api=self.api(runs, artifacts), ancestor=lambda old, new: old in under)
        self.assertEqual(found, b)
        self.assertEqual(ci.tested(runs[1], self.api(runs, artifacts)), a)
        self.assertEqual(ci.tested(runs[4], self.api(runs, artifacts)), 'full')  # a run from before the names

    def test_a_pull_requests_run_proves_no_commit_of_main(self):
        a = 'a' * 40
        runs = [self.ci_run(1, a, event='pull_request')]
        self.assertIsNone(ci.base(a, api=self.api(runs, {1: ['tested-full']}), ancestor=lambda old, new: True))
        self.assertFalse(ci.passed_full(a, api=self.api(runs, {1: ['tested-full']})))

    def test_a_selected_run_is_not_a_full_one(self):
        a, b = 'a' * 40, 'b' * 40
        runs = [self.ci_run(2, b), self.ci_run(1, a)]
        api = self.api(runs, {2: [f'tested-since-{a}'], 1: ['tested-full']})
        self.assertFalse(ci.passed_full(b, api=api))
        self.assertTrue(ci.passed_full(a, api=api))
        self.assertEqual(ci.base(b, api=api, ancestor=lambda old, new: True), a)


class Gate(unittest.TestCase):
    """The check main's rules require (the gate job): green only when the plan and every shard passed."""

    def test_green_only_when_every_shard_passed(self):
        self.assertTrue(ci.gate('success', 'success', '["1","2","3"]')[0])
        self.assertTrue(ci.gate('success', 'success', '["1"]')[0])  # one job
        for tests in ('failure', 'cancelled', ''):
            self.assertFalse(ci.gate('success', tests, '["1","2"]')[0], tests)
            self.assertFalse(ci.gate('success', tests, '["1"]')[0], tests)

    def test_skipped_shards_pass_only_when_no_tests_were_picked(self):
        self.assertTrue(ci.gate('success', 'skipped', '[]')[0])
        self.assertTrue(ci.gate('success', 'skipped', ' []\n')[0])
        self.assertFalse(ci.gate('success', 'skipped', '["1"]')[0])
        self.assertFalse(ci.gate('success', 'skipped', '')[0])

    def test_a_plan_that_did_not_pass_fails(self):
        for plan in ('failure', 'cancelled', 'skipped', ''):
            self.assertFalse(ci.gate(plan, 'skipped', '[]')[0], plan)
            self.assertFalse(ci.gate(plan, 'success', '["1"]')[0], plan)

    def test_the_command_exits_by_the_result(self):
        import subprocess, sys
        command = [sys.executable, str(ROOT / 'scripts' / 'ci_runs.py'), 'gate']
        self.assertEqual(subprocess.run(command + ['success', 'skipped', '[]'], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(command + ['success', 'failure', '["1"]'], capture_output=True).returncode, 1)

    def test_the_workflow_names_the_required_check(self):
        text = (ROOT / '.github' / 'workflows' / 'ci.yml').read_text()
        job = text[text.index('\n  gate:\n'):text.index('\n  impact:\n')]
        self.assertIn('    name: tests (3.12, 24.22.1, 2026.11.2)\n', job)
        self.assertIn('needs: [plan, tests]', job)
        self.assertIn('if: always()', job)
        self.assertIn('ci_runs.py gate "$PLAN" "$TESTS" "$SHARDS"', job)
        self.assertIn('"python":"3.12","node":"24.22.1","openclaw":"2026.11.2"', text)


class Merge(unittest.TestCase):
    def write(self, folder, name, data):
        path = Path(folder, name)
        with gzip.open(path, 'wt', encoding='utf-8') as sink:
            json.dump(data, sink)
        return path

    def test_the_shards_maps_add_up(self):
        one = {'commit': 'abc', 'tests': ['test_a.py', 'test_c.mjs'], 'known': ['x.py'], 'seconds': {'test_a.py': 3.0, 'test_c.mjs': 9.0},
               'files': {'x.py': {'f': [0], 'g': [0]}}, 'js_tests': [1],
               'js': {'dashboard/a.js': {'top': [1], 'funcs': [[0, 10, [1]]]}}}
        two = {'commit': 'abc', 'tests': ['test_b.py', 'test_d.mjs'], 'known': ['x.py', 'y.py'], 'seconds': {'test_b.py': 4.0},
               'files': {'x.py': {'f': [0]}, 'y.py': {'h': [0]}}, 'js_tests': [1],
               'js': {'dashboard/a.js': {'top': [1], 'funcs': [[0, 10, [1]], [20, 30, []]]}}}
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder, 'out.json.gz')
            impact.merge(out, [self.write(folder, 'p1.json.gz', one), self.write(folder, 'p2.json.gz', two)])
            with gzip.open(out, 'rt', encoding='utf-8') as source:
                got = json.load(source)
        tests = got['tests']
        self.assertEqual(tests, ['test_a.py', 'test_b.py', 'test_c.mjs', 'test_d.mjs'])
        ran = lambda ids: sorted(tests[i] for i in ids)
        self.assertEqual(got['commit'], 'abc')
        self.assertEqual(got['known'], ['x.py', 'y.py'])
        self.assertEqual(got['seconds'], {'test_a.py': 3.0, 'test_b.py': 4.0, 'test_c.mjs': 9.0})
        self.assertEqual(ran(got['files']['x.py']['f']), ['test_a.py', 'test_b.py'])
        self.assertEqual(ran(got['files']['x.py']['g']), ['test_a.py'])
        self.assertEqual(ran(got['files']['y.py']['h']), ['test_b.py'])
        self.assertEqual(ran(got['js_tests']), ['test_c.mjs', 'test_d.mjs'])
        part = got['js']['dashboard/a.js']
        self.assertEqual(ran(part['top']), ['test_c.mjs', 'test_d.mjs'])
        self.assertEqual([[a, b, ran(ids)] for a, b, ids in part['funcs']], [[0, 10, ['test_c.mjs', 'test_d.mjs']], [20, 30, []]])

    def test_build_keeps_each_files_time(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'passed').write_text('test_a.py\n', encoding='utf-8')
            Path(folder, 'seconds').write_text('test_a.py\t3.4\ntest_b.py\t7.0\n', encoding='utf-8')
            out = Path(folder, 'map.json.gz')
            impact.build(folder, out)
            with gzip.open(out, 'rt', encoding='utf-8') as source:
                got = json.load(source)
        self.assertEqual(got['tests'], ['test_a.py'])
        self.assertEqual(got['seconds'], {'test_a.py': 3.4, 'test_b.py': 7.0})


    def test_what_ran_only_while_starting_is_kept_apart(self):
        """setUp's calls ("s") and a page's load ("L"): the map keeps, per function, the tests that ran it only then."""
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'passed').write_text('test_a.py\ntest_b.py\ntest_c.mjs\n', encoding='utf-8')
            Path(folder, 'test_a.py.1.rec').write_text('x.py\tf\ts\nx.py\tg\ts\nx.py\tg\n', encoding='utf-8')
            Path(folder, 'test_b.py.2.rec').write_text('x.py\tf\n', encoding='utf-8')
            Path(folder, 'test_c.mjs.3.jsrec').write_text(
                'dashboard/a.js\t-1\t-1\t1\tL\ndashboard/a.js\t0\t10\t1\tL\ndashboard/a.js\t20\t30\t1\tL\n'
                'dashboard/a.js\t20\t30\t1\ndashboard/a.js\t40\t50\t0\tL\n', encoding='utf-8')
            out = Path(folder, 'map.json.gz')
            impact.build(folder, out)
            with gzip.open(out, 'rt', encoding='utf-8') as source:
                got = json.load(source)
            tests = got['tests']
            ran = lambda ids: sorted(tests[i] for i in ids)
            self.assertEqual(ran(got['files']['x.py']['f']), ['test_a.py', 'test_b.py'])
            self.assertEqual({q: ran(ids) for q, ids in got['setup']['x.py'].items()}, {'f': ['test_a.py']})  # g ran in a test too
            part = got['js']['dashboard/a.js']
            self.assertEqual(ran(part['top']), ['test_c.mjs'])
            self.assertEqual([[a, b, ran(ids)] for a, b, ids in part['funcs']], [[0, 10, ['test_c.mjs']], [20, 30, ['test_c.mjs']], [40, 50, []]])
            self.assertEqual([[a, b, ran(ids)] for a, b, ids in got['load']['dashboard/a.js']], [[0, 10, ['test_c.mjs']]])
            # merged with another shard's map, each test keeps what it ran only while starting
            other = {'commit': '', 'tests': ['test_d.py'], 'files': {'x.py': {'g': [0]}}, 'setup': {'x.py': {'g': [0]}},
                     'js': {}, 'load': {}}
            merged = Path(folder, 'merged.json.gz')
            impact.merge(merged, [out, self.write(folder, 'other.json.gz', other)])
            with gzip.open(merged, 'rt', encoding='utf-8') as source:
                got = json.load(source)
            ran = lambda ids: sorted(got['tests'][i] for i in ids)
            self.assertEqual({q: ran(ids) for q, ids in got['setup']['x.py'].items()}, {'f': ['test_a.py'], 'g': ['test_d.py']})
            self.assertEqual([[a, b, ran(ids)] for a, b, ids in got['load']['dashboard/a.js']], [[0, 10, ['test_c.mjs']]])

    def test_the_recorder_notes_what_setup_ran_apart(self):
        source = impact.HOOK_SOURCE % {'root': '/nowhere', 'out': '/nowhere'}
        compile(source, 'hook', 'exec')
        self.assertIn("'\\ts' if state['phase'] else ''", source)
        self.assertIn('mon.restart_events()', source)


class Room(unittest.TestCase):
    """scripts/test.py starts a file only while the shared runner's load leaves room, with one file always going."""

    def test_a_busy_runner_holds_back_all_but_one_file(self):
        import threading
        runner = load('test')
        load_now = [40.0]
        room = runner.Room(1.5, cores=16, load=lambda: load_now[0], pause=0.01)
        room.enter()  # the first file always starts: the run keeps moving
        started = threading.Event()
        second = threading.Thread(target=lambda: (room.enter(), started.set()))
        second.start()
        self.assertFalse(started.wait(0.1), 'load 40 on 16 cores: the second file waits')
        load_now[0] = 20.0
        self.assertTrue(started.wait(2), 'under 24: it starts')
        second.join()
        self.assertEqual(room.going, 2)
        self.assertGreater(room.held, 0)
        room.leave(), room.leave()
        load_now[0] = 99.0
        room.enter()
        self.assertEqual(room.going, 1, 'nothing going: a file starts whatever the load')

    def test_no_limit_unless_asked(self):
        runner = load('test')
        room = runner.Room(0, cores=16, load=lambda: 99.0)
        for _ in range(8):
            room.enter()
        self.assertEqual((room.going, room.held), (8, 0))

    def test_ci_sets_it_on_the_self_hosted_runner(self):
        workflow = (ROOT / '.github' / 'workflows' / 'ci.yml').read_text(encoding='utf-8')
        self.assertIn("THE_MACHINE_TEST_LOAD: ${{ runner.environment == 'self-hosted' && '2' || '' }}", workflow)


if __name__ == '__main__':
    unittest.main()

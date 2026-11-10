"""scripts/test_shards.py and scripts/test_impact.py merge: main's full run splits the test files into shards of about
equal time, runs every file exactly once, and the shards' test-impact maps add up to the map one job would make."""
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

    def test_durations_come_from_the_map(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder, 'map.json.gz')
            with gzip.open(path, 'wt', encoding='utf-8') as sink:
                json.dump({'tests': ['test_a.py'], 'seconds': {'test_a.py': 12.5, 'test_b.mjs': 'x'}}, sink)
            self.assertEqual(shards.recorded(path), {'test_a.py': 12.5})
            self.assertEqual(shards.recorded(Path(folder, 'missing.json.gz')), {})


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


if __name__ == '__main__':
    unittest.main()

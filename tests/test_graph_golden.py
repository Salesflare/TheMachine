"""The Graph built from the sandbox is the stored snapshot, row for row (tests/graph_golden.py): a refactor of the build
(graph.py) changes none of it, and a change meant to change the Graph shows each row it changes in the snapshot's diff."""
import difflib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tests'))
import graph_golden  # noqa: E402


class GraphGoldenTest(unittest.TestCase):
    def built(self, seed):
        """The rows of a build in a process of its own (the sandbox sets HOME before it imports anything), with its own
        hash seed: set order never decides a row."""
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / 'graph.json'
            subprocess.run([sys.executable, str(ROOT / 'tests' / 'graph_golden.py'), str(out)], cwd=ROOT, check=True, timeout=300,
                           capture_output=True, env={**os.environ, 'PYTHONHASHSEED': str(seed)})
            return out.read_text()

    def test_graph_is_the_snapshot(self):
        want = graph_golden.SNAPSHOT.read_text()
        for seed in (0, 1):
            with self.subTest(seed=seed):
                have = self.built(seed)
                if have != want:
                    diff = ''.join(list(difflib.unified_diff(want.splitlines(True), have.splitlines(True), 'snapshot', 'built', n=0))[:60])
                    self.fail('the Graph differs from tests/graph_golden.json; when the change is meant to change it, run '
                              f'python3 tests/graph_golden.py --write and check the diff:\n{diff}')


if __name__ == '__main__':
    unittest.main()

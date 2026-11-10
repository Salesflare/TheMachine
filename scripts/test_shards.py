#!/usr/bin/env python3
"""Splits the test files into shards that take about as long each, so CI's full run (.github/workflows/ci.yml) runs as
several jobs side by side on our runner instead of one long one.

How long each file takes comes from the test-impact map of main's last full run (scripts/test_impact.py, its
"seconds"). A file the map doesn't know yet is guessed from its size. Each shard lists its files longest first, so a
slow one starts early (scripts/test.py --in-order).

scripts/test_shards.py --shards 4 [--target 1800] [--impact map.json.gz] [picked.txt]
    prints {"1": "test_a.py test_b.mjs ...", "2": ...} (JSON); picked.txt names the files to split (one per line, or
    ALL; empty: none, and {} is printed), every test file without it. With --target, only as many shards (at most
    --shards) as it takes for each to hold about that many seconds of files: a small selection stays one job."""
import gzip
import json
import math
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / 'tests'
TYPICAL = 10  # seconds a test file takes on our runner, on average (main's full runs, 2026-11)


def every_test():
    return [path.name for path in sorted(TESTS.glob('test_*.py')) + sorted(TESTS.glob('test_*.mjs'))]


def recorded(path):
    """{test file: seconds} from the map at path; {} without one."""
    try:
        with gzip.open(path, 'rt', encoding='utf-8') as source:
            data = json.load(source)
        seconds = data.get('seconds') if isinstance(data, dict) else None
        return {name: float(s) for name, s in (seconds or {}).items() if isinstance(s, (int, float)) and s >= 0}
    except (OSError, ValueError, EOFError, TypeError):
        return {}


def estimate(files, seconds):
    """{file: seconds}: recorded, else its size times the median seconds per byte of the recorded ones (just the size,
    in bytes, when nothing is recorded: then only the proportions count)."""
    size = {name: max((TESTS / name).stat().st_size if (TESTS / name).exists() else 0, 1) for name in files}
    rates = [seconds[name] / size[name] for name in files if name in seconds]
    rate = statistics.median(rates) if rates else 1.0
    return {name: seconds[name] if name in seconds else size[name] * rate for name in files}


def split(files, seconds, count):
    """count lists that together hold every file once, of about the same total time: the longest file goes to the
    shard with the least so far. Each list longest first; none empty unless there are fewer files than shards."""
    took = estimate(files, seconds)
    shards = [[] for _ in range(max(1, count))]
    totals = [0.0] * len(shards)
    for name in sorted(files, key=lambda f: (-took[f], f)):
        least = min(range(len(shards)), key=lambda i: (totals[i], i))
        shards[least].append(name)
        totals[least] += took[name]
    return [shard for shard in shards if shard] or [[]]


def needed(files, seconds, count, target):
    """How many shards of about target seconds of files each, at most count. Without recorded times a file counts as
    TYPICAL seconds (about the average on our runner)."""
    if not target:
        return count
    total = sum(estimate(files, seconds).values()) if seconds else TYPICAL * len(files)
    return max(1, min(count, math.ceil(total / target)))


def main(argv):
    count, impact, source, target = 1, None, None, 0
    while argv:
        if argv[0] == '--shards':
            count, argv = int(argv[1]), argv[2:]
        elif argv[0] == '--target':
            target, argv = float(argv[1]), argv[2:]
        elif argv[0] == '--impact':
            impact, argv = argv[1], argv[2:]
        else:
            source, argv = argv[0], argv[1:]
    files = every_test()
    if source:
        picked = [Path(line.strip()).name for line in Path(source).read_text(encoding='utf-8').splitlines() if line.strip()]
        if not picked:
            print('{}')
            return 0
        if picked[:1] != ['ALL']:
            files = picked
    seconds = recorded(impact) if impact else {}
    shards = split(files, seconds, needed(files, seconds, count, target))
    print(json.dumps({str(i): ' '.join(shard) for i, shard in enumerate(shards, 1)}))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

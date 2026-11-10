#!/usr/bin/env python3
"""What each run of CI's tests (.github/workflows/ci.yml) proved, for main's runs and scripts/release.py.

A push to main runs only the tests the change needs since the newest commit under it whose full run passed (the
"base"), so it never repeats what is proven already; the nightly run, a manual run and a run whose selection needs
everything run every test. The plan job of each such run names an artifact after what it ran:

  tested-full          every test file
  tested-since-<sha>   the files scripts/test_select.py picks for everything changed since <sha>, a commit whose
                       full run passed

A passed tested-since-<sha> run is main's green or red signal: every test passed on <sha>, and every test the
selection says the changes since then can break passed on this one. A release needs more (scripts/release.py): a
passed tested-full run on its exact commit, since a dependency the selection missed must never reach one. A run from
before these names ran every test, so a run without one counts as full.

scripts/ci_runs.py base SHA   the newest commit under SHA (or SHA itself) whose full run passed; nothing when none"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
REPO = 'Salesflare/TheMachine'
# The runs that test main's commits (a pull request's run tests its merge commit, never main's).
MAIN_RUN = ('push', 'schedule', 'workflow_dispatch')
FULL = 'tested-full'
SINCE = re.compile(r'tested-since-([0-9a-f]{40})')


def _default_api(path):
    spec = importlib.util.spec_from_file_location('test_impact', ROOT / 'scripts' / 'test_impact.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    import os
    return json.loads(module._api(path, os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')))


def tested(run, api=_default_api):
    """'full' or the base commit's sha: what a run tested, from its artifacts' names."""
    names = [a.get('name', '') for a in api(f'repos/{REPO}/actions/runs/{run["id"]}/artifacts?per_page=100').get('artifacts', [])]
    for name in names:
        if found := SINCE.fullmatch(name):
            return found.group(1)
    return 'full'


def passed_full(sha, api=_default_api):
    """Whether a full run passed on exactly this commit."""
    runs = api(f'repos/{REPO}/actions/workflows/ci.yml/runs?head_sha={sha}&status=success&per_page=30').get('workflow_runs', [])
    return any(r['event'] in MAIN_RUN and r['conclusion'] == 'success' and tested(r, api) == 'full' for r in runs)


def is_ancestor(old, new):
    return subprocess.run(['git', 'merge-base', '--is-ancestor', old, new], cwd=ROOT, capture_output=True).returncode == 0


def base(head, api=_default_api, ancestor=is_ancestor, pages=3):
    """The newest commit at or under head whose full run passed, or None (then everything runs)."""
    for page in range(1, pages + 1):
        runs = api(f'repos/{REPO}/actions/workflows/ci.yml/runs?status=success&per_page=100&page={page}').get('workflow_runs', [])
        for run in runs:
            if run['event'] in MAIN_RUN and run['conclusion'] == 'success' and ancestor(run['head_sha'], head) \
                    and tested(run, api) == 'full':
                return run['head_sha']
        if len(runs) < 100:
            break
    return None


def main(argv):
    if argv[:1] == ['base'] and len(argv) == 2:
        head = subprocess.run(['git', 'rev-parse', argv[1]], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        try:
            found = base(head)
        except Exception as error:  # anything that goes wrong: no base, so everything runs
            print(f'no base: {error}', file=sys.stderr)
            found = None
        print(found or '')
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

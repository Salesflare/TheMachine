#!/usr/bin/env python3
"""Which functions each test file runs (the test-impact map), so scripts/test_select.py can pick the tests a change to
a function needs instead of every test that imports its module (assistant.py and machine/app/ load nearly everything).

A full run on main records it: every Python process the tests start (a test, a server it starts, a script it runs) notes
each function of this checkout it runs, once (sys.monitoring, Python 3.12 and newer: one callback per function, then
it's switched off, so the tests barely slow down). A process that cleared its environment still counts for its test:
the hook finds the test in its parents' environment on Linux. Only the files that passed go in the map; a test the map
doesn't know is picked the old way. Every Node process scripts/test.py starts loads scripts/test_impact_js.mjs too
(NODE_OPTIONS): a page a test opens in Chromium notes the functions of the dashboard's parts (dashboard/*.js) that ran,
from V8's coverage.

scripts/test_impact.py install DIR        record into DIR from now on (a .pth file in site-packages; scripts/test.py
                                          loads scripts/test_impact_js.mjs into Node when THE_MACHINE_IMPACT_DIR is set)
scripts/test_impact.py remove             stop recording
scripts/test_impact.py build DIR OUT      the map from DIR's records (DIR/passed lists the files that passed), gzipped JSON
                                          (with DIR/seconds, how long each file took, for scripts/test_shards.py)
scripts/test_impact.py merge OUT MAP...   one map from the maps of a full run's shards
scripts/test_impact.py fetch [OUT]        the newest map main's CI made (needs gh), for scripts/test.py --changed"""
import gzip
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import sysconfig
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent.parent
HOOK = 'themachine_impact_hook'
REPO = 'Salesflare/TheMachine'
ARTIFACT = 'test-impact'
CACHE = Path.home() / '.cache' / 'the-machine' / 'test-impact.json.gz'

HOOK_SOURCE = r'''"""The Machine's test-impact recorder (scripts/test_impact.py install): notes each function of the checkout a
process runs, once, for the test file that started it."""
import os
import sys

ROOT = %(root)r
OUT = %(out)r


def _test():
    name = os.environ.get('THE_MACHINE_IMPACT_TEST')
    if name:
        return name
    pid = os.getppid()
    for _ in range(40):  # a process started with a cleared environment: its parents know the test
        if pid <= 1:
            return None
        try:
            with open('/proc/%%d/environ' %% pid, 'rb') as env:
                for item in env.read().split(b'\0'):
                    if item.startswith(b'THE_MACHINE_IMPACT_TEST='):
                        return item.split(b'=', 1)[1].decode()
            with open('/proc/%%d/stat' %% pid) as stat:
                pid = int(stat.read().rsplit(')', 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            return None
    return None


def _start():
    if not os.path.isdir(OUT) or not hasattr(sys, 'monitoring'):
        return
    test = _test()
    if not test or '/' in test:
        return
    mon = sys.monitoring
    tool = next((t for t in range(6) if mon.get_tool(t) is None), None)
    if tool is None:
        return
    fd = os.open(os.path.join(OUT, '%%s.%%d.rec' %% (test, os.getpid())), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    prefix = ROOT + os.sep
    disable = mon.DISABLE

    def ran(code, offset):
        path = code.co_filename
        if not path.startswith(prefix):
            if path.startswith('<') or os.path.isabs(path):
                return disable
            path = os.path.realpath(path)
            if not path.startswith(prefix):
                return disable
        if code.co_flags & 1:  # a function (CO_OPTIMIZED); a module or class body only runs on import
            try:
                os.write(fd, ('%%s\t%%s\n' %% (path[len(prefix):], code.co_qualname)).encode('utf-8', 'replace'))
            except OSError:
                pass
        return disable

    mon.use_tool_id(tool, 'themachine-impact')
    mon.register_callback(tool, mon.events.PY_START, ran)
    mon.set_events(tool, mon.events.PY_START)


try:
    _start()
except Exception:  # recording must never break a test
    pass
'''


def site_packages():
    return Path(sysconfig.get_paths()['purelib'])


def install(out):
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    folder = site_packages()
    (folder / f'{HOOK}.py').write_text(HOOK_SOURCE % {'root': str(ROOT), 'out': str(out)}, encoding='utf-8')
    (folder / f'{HOOK}.pth').write_text(f'import {HOOK}\n', encoding='utf-8')
    print(f'Recording which functions each test runs into {out}')


def remove():
    for name in (f'{HOOK}.pth', f'{HOOK}.py'):
        (site_packages() / name).unlink(missing_ok=True)


def build(records, out):
    records = Path(records)
    passed = set((records / 'passed').read_text(encoding='utf-8').split()) if (records / 'passed').exists() else set()
    tests = sorted(passed)
    index = {name: i for i, name in enumerate(tests)}
    files = {}
    for rec in records.glob('*.rec'):
        test = rec.name.rsplit('.', 2)[0]
        if test not in index:
            continue
        for line in rec.read_text(encoding='utf-8', errors='replace').splitlines():
            path, _, qualname = line.partition('\t')
            if qualname:
                files.setdefault(path, {}).setdefault(qualname, set()).add(index[test])
    # the browser half (scripts/test_impact_js.mjs): per dashboard part, its functions by offsets, with the tests that
    # ran each (none for one no test ran), and the tests that loaded it ('top')
    js, js_tests = {}, set()
    for rec in records.glob('*.jsrec'):
        test = rec.name.rsplit('.', 2)[0]
        if test not in index:
            continue
        js_tests.add(index[test])
        for line in rec.read_text(encoding='utf-8', errors='replace').splitlines():
            fields = line.split('\t')
            if len(fields) != 4 or not fields[0].startswith('dashboard/'):
                continue
            part = js.setdefault(fields[0], {'top': set(), 'funcs': {}})
            span = (int(fields[1]), int(fields[2]))
            ids = part['top'] if span[0] < 0 else part['funcs'].setdefault(span, set())
            if fields[3] == '1':
                ids.add(index[test])
    try:
        commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        known = [p for p in subprocess.run(['git', 'ls-files', '*.py'], cwd=ROOT, capture_output=True, text=True,
                                           check=True).stdout.split('\n') if p]
    except (OSError, subprocess.CalledProcessError):
        commit, known = '', []
    seconds = {}
    if (records / 'seconds').exists():
        for line in (records / 'seconds').read_text(encoding='utf-8').splitlines():
            name, _, took = line.partition('\t')
            try:
                seconds[name] = round(float(took), 1)
            except ValueError:
                pass
    data = {'commit': commit, 'tests': tests, 'known': known, 'seconds': dict(sorted(seconds.items())),
            'files': {path: {q: sorted(ids) for q, ids in sorted(funcs.items())} for path, funcs in sorted(files.items())},
            'js_tests': sorted(js_tests),
            'js': {part: {'top': sorted(found['top']), 'funcs': [[a, b, sorted(ids)] for (a, b), ids in sorted(found['funcs'].items())]}
                   for part, found in sorted(js.items())}}
    with gzip.open(out, 'wt', encoding='utf-8') as sink:
        json.dump(data, sink, separators=(',', ':'))
    print(f'{len(tests)} test files, {sum(len(f) for f in files.values())} functions in {len(files)} files, '
          f'{sum(len(p["funcs"]) for p in js.values())} in {len(js)} dashboard parts ({len(js_tests)} browser tests) -> {out}')


def merge(out, parts):
    """One map from several (a full run's shards, each with its own test files): the tests of all of them, each
    function and dashboard part with the tests that ran it in any."""
    maps = []
    for part in parts:
        with gzip.open(part, 'rt', encoding='utf-8') as source:
            maps.append(json.load(source))
    tests = sorted({name for data in maps for name in data.get('tests') or ()})
    index = {name: i for i, name in enumerate(tests)}
    files, js, js_tests, seconds, known = {}, {}, set(), {}, set()
    for data in maps:
        mine = data.get('tests') or []
        ids = lambda found: {index[mine[i]] for i in found}
        known.update(data.get('known') or ())
        seconds.update(data.get('seconds') or {})
        js_tests.update(ids(data.get('js_tests') or ()))
        for path, funcs in (data.get('files') or {}).items():
            for qualname, found in funcs.items():
                files.setdefault(path, {}).setdefault(qualname, set()).update(ids(found))
        for name, found in (data.get('js') or {}).items():
            part = js.setdefault(name, {'top': set(), 'funcs': {}})
            part['top'].update(ids(found.get('top') or ()))
            for start, end, ran in found.get('funcs') or ():
                part['funcs'].setdefault((start, end), set()).update(ids(ran))
    commits = {data.get('commit') or '' for data in maps}
    merged = {'commit': commits.pop() if len(commits) == 1 else '', 'tests': tests, 'known': sorted(known),
              'seconds': dict(sorted(seconds.items())),
              'files': {path: {q: sorted(found) for q, found in sorted(funcs.items())} for path, funcs in sorted(files.items())},
              'js_tests': sorted(js_tests),
              'js': {name: {'top': sorted(found['top']), 'funcs': [[a, b, sorted(ran)] for (a, b), ran in sorted(found['funcs'].items())]}
                     for name, found in sorted(js.items())}}
    with gzip.open(out, 'wt', encoding='utf-8') as sink:
        json.dump(merged, sink, separators=(',', ':'))
    print(f'{len(tests)} test files from {len(maps)} shards -> {out}')


class _Stay(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # the download's redirect goes to storage that must not get the token


def _api(url, token):
    """GitHub's API: with a token (CI's GITHUB_TOKEN) over HTTPS, else through gh (a developer's own sign-in)."""
    if not token:
        return subprocess.run(['gh', 'api', url], capture_output=True, timeout=300, check=True).stdout
    full = url if url.startswith('https://') else f'https://api.github.com/{url}'
    request = urllib.request.Request(full, headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.build_opener(_Stay).open(request, timeout=120) as response:
            return response.read()
    except urllib.error.HTTPError as moved:
        if moved.code not in (301, 302, 303, 307, 308):
            raise
        with urllib.request.urlopen(moved.headers['Location'], timeout=300) as response:
            return response.read()


def fetch(out=CACHE):
    """The newest map main's CI made, kept at out (reused while it's still the newest). None when there's none."""
    out = Path(out)
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    try:
        listing = json.loads(_api(f'repos/{REPO}/actions/artifacts?name={ARTIFACT}&per_page=30', token))
        found = [a for a in listing.get('artifacts', [])
                 if not a.get('expired') and (a.get('workflow_run') or {}).get('head_branch') == 'main']
        if not found:
            return None
        newest = max(found, key=lambda a: a['created_at'])
        stamp = out.with_name(out.name + '.id')
        if out.exists() and stamp.exists() and stamp.read_text().strip() == str(newest['id']):
            return out
        with zipfile.ZipFile(io.BytesIO(_api(newest['archive_download_url'], token))) as archive:
            data = archive.read('test-impact.json.gz')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        stamp.write_text(str(newest['id']))
        return out
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.SubprocessError, urllib.error.URLError):
        return out if out.exists() else None


def main(argv):
    if argv[:1] == ['install'] and len(argv) == 2:
        install(argv[1])
    elif argv[:1] == ['remove']:
        remove()
    elif argv[:1] == ['build'] and len(argv) == 3:
        build(argv[1], argv[2])
    elif argv[:1] == ['merge'] and len(argv) >= 3:
        merge(argv[1], argv[2:])
    elif argv[:1] == ['fetch']:
        got = fetch(*argv[1:2])
        print(got or 'no map: the selection follows imports')
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

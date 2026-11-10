#!/usr/bin/env python3
"""Run every Python and Node suite with a disposable HOME and no account configuration.

Each test file runs in its own process with its own HOME, several at once (as many as the computer has cores, at
most 8; THE_MACHINE_TEST_JOBS=1 runs them one by one). A file's output is printed when it's done, in full when it
failed. The tests live in tests/ and run from the repository root. Name files to run only those (with or without tests/):
scripts/test.py test_moving.py tests/test_fleet_dashboard.mjs"""
import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / 'tests'


def openclaw_package(node):
    """OpenClaw beside this node (a global npm install), else wherever the `openclaw` on PATH comes from
    (a per-user install, as on hosted machines)."""
    beside = Path(node).parent.parent / 'lib' / 'node_modules' / 'openclaw'
    if beside.is_dir():
        return None
    found = shutil.which('openclaw')
    for folder in Path(os.path.realpath(found)).parents if found else ():
        if folder.name == 'openclaw' and (folder / 'package.json').exists():
            return str(folder)
    return None


# Files that test Linux-only parts, skipped elsewhere with the reason (macOS runs natively under launchd; on
# Windows The Machine runs inside WSL2, which is Linux, so there only the portable core is tested natively).
BROWSER_VIEWER = 'the browser sign-in runs Chrome in the browser viewer (Xvfb and noVNC), which is Linux-only for now'
SKIP = {
    'test_browser_login.py': {'darwin': BROWSER_VIEWER, 'win32': BROWSER_VIEWER},
}


# On Windows The Machine runs inside WSL2, which is Linux, so the Linux jobs test it. Natively, Windows runs the
# parts that do not depend on the operating system: the portable core, connectors, parsing and the Node helpers.
WINDOWS_NATIVE = {
    'test_portable.py', 'test_install.py', 'test_gateway.py', 'test_profile.py', 'test_connectors.py',
    'test_new_connectors.py', 'test_connector_shortcut.py', 'test_connector_google_meet.py', 'test_connector_teams.py', 'test_connector_trello.py', 'test_github_stripe.py',
    'test_salesflare.py', 'test_google_broker.py', 'test_mail_grants.py', 'test_discovery.py', 'test_enrichment.py', 'test_email_bodies.py',
    'test_exclusions.py', 'test_gmail_exclusions.py', 'test_ingestion_recovery.py', 'test_android_coalescing.py',
    'test_friends.py', 'test_fleet_free.py', 'test_fleet_brief.py', 'test_fleet_receipts.py', 'test_review_worker.py',
    'test_browser_cdp.py', 'test_browser_login_recovery.py', 'test_android_feed.mjs', 'test_x_paging.mjs',
    'test_taglines.mjs', 'test_telegram_receipt.mjs',
}
IN_WSL2 = 'on Windows The Machine runs inside WSL2 (Linux), which the Linux jobs test'


# The connector suites run with MESSAGE_SEAL_AUDIT=1: commit_page refuses any event whose message text shows in a plain
# field, and a file whose output says so fails. test_message_seal runs them so itself when run on its own.
SEAL_AUDIT = (
    'test_connectors', 'test_new_connectors', 'test_x', 'test_linkedin', 'test_whatsapp', 'test_ms_graph', 'test_salesflare',
    'test_connector_trello', 'test_github_stripe', 'test_connector_shortcut', 'test_connector_google_meet', 'test_connector_teams', 'test_email_bodies', 'test_gmail_exclusions',
    'test_android_coalescing', 'test_gateway', 'test_ingestion_recovery',
)
SEAL_LEAK = 'keeps message text in the clear'


def skipped(file):
    if sys.platform == 'win32' and file.name not in WINDOWS_NATIVE:
        return IN_WSL2
    for platforms, reason in SKIP.get(file.name, {}).items():
        if sys.platform.startswith(platforms):
            return reason
    return None


def browsers():
    """Chrome or Chromium, by name on PATH, then where macOS and Windows install them."""
    for name in ('chromium', 'chromium-browser', 'google-chrome-stable', 'google-chrome', 'chrome'):
        if found := shutil.which(name):
            yield found
    if sys.platform == 'darwin':
        yield from ('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium')
    if os.name == 'nt':
        for base in (os.environ.get('PROGRAMFILES'), os.environ.get('PROGRAMFILES(X86)'), os.environ.get('LOCALAPPDATA')):
            if base:
                yield str(Path(base) / 'Google/Chrome/Application/chrome.exe')


def execute(command, env, limit, folder):
    """Run one test file: (passed, output, CPU seconds or None). On Linux and macOS the CPU time is the file's own
    process and every process it waited for (a browser, a server), from wait4."""
    if not hasattr(os, 'wait4'):
        try:
            result = subprocess.run(command, cwd=ROOT, env=env, timeout=limit, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, errors='replace')
            return result.returncode == 0, result.stdout, None
        except subprocess.TimeoutExpired as timeout:
            out = timeout.output or ''
            return False, (out.decode(errors='replace') if isinstance(out, bytes) else out) + f'\nTimed out after {limit} s', None
    log = folder / '.test-output'
    with open(log, 'wb') as sink:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=sink, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    deadline, status, usage, late = time.monotonic() + limit, 0, None, False
    while True:
        pid, status, usage = os.wait4(process.pid, os.WNOHANG)
        if pid:
            break
        if time.monotonic() > deadline:
            process.kill()
            _, status, usage = os.wait4(process.pid, 0)
            late = True
            break
        time.sleep(0.1)
    process.returncode = os.waitstatus_to_exitcode(status)
    output = log.read_bytes().decode(errors='replace')
    if late:
        return False, output + f'\nTimed out after {limit} s', usage.ru_utime + usage.ru_stime
    return process.returncode == 0, output, usage.ru_utime + usage.ru_stime


def changed_tests(args):
    """scripts/test.py --changed [REF]: the test files this worktree's change needs, against where it left origin/main
    (or REF): commits, staged and unstaged edits and new files, picked as on a pull request (scripts/test_select.py with
    the test-impact map from main's CI, fetched with gh; without it, by following imports). None: every file."""
    import importlib.util
    ref = args[0] if args else 'origin/main'

    def git(*command):
        return subprocess.run(['git', *command], cwd=ROOT, capture_output=True, text=True, check=True).stdout

    try:
        base = git('merge-base', ref, 'HEAD').strip()
        paths = sorted(set(git('diff', '--name-only', base).split()) | set(git('ls-files', '--others', '--exclude-standard').split()))
    except (OSError, subprocess.CalledProcessError):
        print(f'--changed: no {ref} to compare with (git fetch origin first)', file=sys.stderr)
        sys.exit(2)
    if not paths:
        print(f'Nothing changed against {ref}: no tests to run.')
        return []
    modules = {}
    for name in ('test_select', 'test_impact'):
        spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
        modules[name] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modules[name])
    found = modules['test_impact'].fetch()
    impact = modules['test_select'].load_impact(found) if found else None
    why = {}
    picked = modules['test_select'].select(paths, why=why, impact=impact, base=base)
    how = 'the test-impact map from main' if impact else 'imports (no test-impact map: gh could not fetch it)'
    if picked is None:
        print(f'{len(paths)} changed files need every test file ({why.get("*", "most of them are picked")}).', flush=True)
        return None
    print(f'{len(picked)} test files for {len(paths)} changed files, picked by {how}.', flush=True)
    return picked


def main():
    node = shutil.which('node')
    if not node:
        print('Node.js is required; see README prerequisites.', file=sys.stderr)
        return 1
    node = subprocess.check_output([node,'-p','process.execPath'],text=True).strip()
    if not (ROOT / 'node_modules' / '@openclaw' / 'gateway-client').is_dir():  # the pinned packages (package-lock.json), as the installer does
        npm = shutil.which('npm')
        if not npm or subprocess.run([npm, 'ci', '--omit=dev', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=ROOT).returncode:
            print('npm ci failed: the pinned Node packages are needed for the tests.', file=sys.stderr)
            return 1
    cache = Path.home() / '.cache'
    cache.mkdir(exist_ok=True)
    # A HOME under /tmp would exercise the service's forbidden PrivateTmp attachment path.
    with tempfile.TemporaryDirectory(prefix='themachine-tests-',dir=cache) as home:
        env = {k:v for k,v in os.environ.items() if not k.startswith(('ASSISTANT_','OPENCLAW_','GOG_'))
               and k not in ('DBUS_SESSION_BUS_ADDRESS','XDG_RUNTIME_DIR','XDG_CONFIG_HOME','XDG_DATA_HOME','XDG_CACHE_HOME')}
        env.update(HOME=home,PATH=str(Path(node).parent)+os.pathsep+os.environ.get('PATH',''))
        # The suites import the app from the root (their working folder) and their shared helpers from tests/.
        env['PYTHONPATH'] = os.pathsep.join(filter(None, (str(TESTS), os.environ.get('PYTHONPATH'))))
        if os.environ.get('THE_MACHINE_IMPACT_DIR'):
            # recording the test-impact map: Node notes which functions of the dashboard's parts each page test runs
            # (set here: GitHub won't take NODE_OPTIONS from a step's $GITHUB_ENV)
            hook = '--import=' + (ROOT / 'scripts' / 'test_impact_js.mjs').as_uri()
            env['NODE_OPTIONS'] = ' '.join(filter(None, (os.environ.get('NODE_OPTIONS'), hook)))
        if os.name == 'nt':
            env['PYTHONUTF8'] = '1'  # the console's code page can't print everything the suites print
        package = os.environ.get('OPENCLAW_PACKAGE_DIR') or openclaw_package(node)
        if package:
            env['OPENCLAW_PACKAGE_DIR'] = package
        browser = os.environ.get('CHROMIUM_PATH') or next((found for found in browsers() if Path(found).exists()), None)
        if browser:
            env['CHROMIUM_PATH'] = browser
        env['THE_MACHINE_SEAL_AUDITED'] = ','.join(SEAL_AUDIT)  # test_message_seal: these run audited here already
        chosen = sys.argv[1:]
        if chosen[:1] == ['--changed']:
            chosen = changed_tests(chosen[1:])
            if chosen == []:
                return 0
        files =[TESTS / Path(name).name for name in chosen] if chosen else sorted(TESTS.glob('test_*.py')) + sorted(TESTS.glob('test_*.mjs'))
        jobs = max(1, int(os.environ.get('THE_MACHINE_TEST_JOBS') or min(os.cpu_count() or 2, 8)))
        configured_limit = os.environ.get('THE_MACHINE_TEST_TIMEOUT')
        skips = {file.name: reason for file in files if (reason := skipped(file))}
        files = [file for file in files if file.name not in skips]
        for name, reason in sorted(skips.items()):
            if reason != IN_WSL2:
                print(f'skip {name}: {reason}', flush=True)
        if wsl2 := sum(reason == IN_WSL2 for reason in skips.values()):
            print(f'skip {wsl2} files: {IN_WSL2}', flush=True)

        def run(file):
            limit = int(configured_limit or 600)
            command = [sys.executable, '-m', 'unittest', file.stem] if file.suffix == '.py' else [node, str(file)]
            started = time.monotonic()
            own = Path(home) / file.name
            own.mkdir()
            # which test file started a process: scripts/test_impact.py's recorder files what it runs under this name
            audit = {'THE_MACHINE_IMPACT_TEST': file.name}
            audit.update({'MESSAGE_SEAL_AUDIT': '1'} if file.stem in SEAL_AUDIT else {})
            # Windows finds the home folder through USERPROFILE, not HOME.
            ok, output, cpu = execute(command, {**env, **audit, 'HOME': str(own), 'USERPROFILE': str(own)}, limit, own)
            if 'MESSAGE_SEAL_AUDIT' in audit and SEAL_LEAK in output:
                ok, output = False, output + f'\nA connector {SEAL_LEAK} (MESSAGE_SEAL_AUDIT)'
            return file.name, ok, output, time.monotonic() - started, cpu

        failed, took, cpu_total = [], [], 0.0
        # THE_MACHINE_TEST_MAX_FAILURES=N: after N failed files, start no more (the ones running finish), so a change that
        # breaks much doesn't hold a CI slot for the whole suite. Unset or 0: run everything.
        max_failures = int(os.environ.get('THE_MACHINE_TEST_MAX_FAILURES') or 0)
        wall = time.monotonic()
        print(f'Running {len(files)} test files, {jobs} at a time' + (f' ({len(skips)} skipped on {sys.platform})' if skips else ''), flush=True)
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            # the biggest files first, so a slow one doesn't start last and keep everyone waiting
            started = [pool.submit(run, file) for file in sorted(files, key=lambda f: -f.stat().st_size)]
            for done in concurrent.futures.as_completed(started):
                if done.cancelled():
                    continue
                name, ok, output, seconds, cpu = done.result()
                took.append((seconds, name))
                cpu_total += cpu or 0
                print(f'{"ok  " if ok else "FAIL"} {name} ({seconds:.0f} s' + (f', {cpu:.0f} s CPU' if cpu is not None else '') + ')', flush=True)
                if not ok:
                    failed.append(name)
                    print(output.rstrip() + '\n', flush=True)
                    if max_failures and len(failed) == max_failures:
                        skipped_now = sum(future.cancel() for future in started)
                        if skipped_now:
                            print(f'{len(failed)} files failed: {skipped_now} not started (THE_MACHINE_TEST_MAX_FAILURES)', flush=True)
        wall = time.monotonic() - wall
        if cpu_total:
            # how busy the files kept the computer: about `jobs` here means the workers fit the cores they have
            print(f'CPU {cpu_total:.0f} s in {wall:.0f} s: {cpu_total / wall:.1f} cores busy on average, {jobs} workers')
        print('Slowest: ' + ', '.join(f'{name} {seconds:.0f} s' for seconds, name in sorted(took, reverse=True)[:10]))
        if record := os.environ.get('THE_MACHINE_IMPACT_DIR'):
            # the files that passed: only their records go in the test-impact map (scripts/test_impact.py build)
            passed = sorted(name for _, name in took if name not in failed)
            Path(record, 'passed').write_text('\n'.join(passed) + '\n', encoding='utf-8')
        print('\n'+('Failed: '+', '.join(sorted(failed)) if failed else 'All Python and Node suites passed.'))
        return 1 if failed else 0

if __name__=='__main__':
    sys.exit(main())

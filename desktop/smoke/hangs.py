"""What can keep the app waiting on a real Mac, on CI's own throwaway computer (desktop.yml): a keychain that asks, a Machine that
never answers, a page or a main thread that is stuck. After each the robot has to answer a click within 3 seconds.

  python3 smoke/hangs.py <sandbox build> - <folder for the pictures>
"""
import contextlib
import json
import os
import pathlib
import plistlib
import shutil
import signal
import time

import mac_tools
from mac_tools import ID, LIBRARY, PORT, App, click, finish, fresh, in_front, move, need, other, out, page, png, run, sandbox, saved, step, until
from standin import Machine

FOLDER = LIBRARY / 'Application Support' / ID
CHAIN, WORD = str(out.parent / 'made-up.keychain-db'), 'made-up'
ITEM = f'com.apple.WebKit.WebCrypto.master+{ID}'
SEARCHED = [x.strip().strip('"') for x in run('security', 'list-keychains', '-d', 'user').stdout.splitlines()]
DEFAULT = run('security', 'default-keychain', '-d', 'user').stdout.strip().strip('"')
machine = Machine(PORT)
machine.window = machine.compact = True
app = None
mac_tools.hangs['wanted'] = True  # each step looks itself


def log():
    with contextlib.suppress(FileNotFoundError):
        return (FOLDER / 'hangs.log').read_text()
    return ''


def stacks():
    return {p.name: p.read_text() for p in FOLDER.glob('hang-*.txt')}


def keep(name):
    """What the watch wrote, beside the pictures."""
    for file in [FOLDER / 'hangs.log', *FOLDER.glob('hang-*.txt')]:
        with contextlib.suppress(FileNotFoundError):
            shutil.copy(file, out / f'{name}-{file.name}')


def start(at=None, window=True, bundle=sandbox, anew=True, **more):
    global app
    if app:
        app.kill()
    if anew:
        fresh()
        if at:
            FOLDER.mkdir(parents=True, exist_ok=True)
            (FOLDER / 'app.json').write_text(json.dumps({'machine': at}))
    app = App(bundle, window=window, more=more)


def kept(word='kept'):
    """What the dashboard's page wrote with a key of its own."""
    def told():
        with contextlib.suppress(OSError, ValueError):
            return page('app', 'document.querySelector("#kept")?.textContent')
    found = until(told, 30)
    need(found == word, f'{found}; {log()}')


def clicked(seconds=3, twice=True):
    """The robot answers: the pointer over it, and a click opens and closes the box."""
    other()
    need(until(app.robot, 10), 'the robot is there')
    move(*app.center())
    time.sleep(0.4)
    png('over-the-robot')
    shows = lambda: (bool(app.box()), len(app.plain()), in_front())
    for _ in range(1 + twice):
        had, since = shows(), time.time()
        click(*app.center())
        need(until(lambda had=had: shows() != had, seconds, 0.1), f'a click does something within {seconds} s; {had} {log()}')
        took = time.time() - since
        time.sleep(1)
    since = time.time()
    need(until(app.answers, seconds), 'its page answers')
    return f'a click {took:.1f} s, its page {time.time() - since:.1f} s'


def stuck(seconds=20):
    """Whether the main thread stops answering, as the watch says."""
    return until(lambda: 'the main thread doesn' in log(), seconds)


def quit_it():
    app.again('--quit')
    need(app.ended(), 'the process is gone')


def chain(locked):
    if not pathlib.Path(CHAIN).exists():
        run('security', 'create-keychain', '-p', WORD, CHAIN)
        run('security', 'set-keychain-settings', CHAIN)
        run('security', 'list-keychains', '-d', 'user', '-s', CHAIN)
        run('security', 'default-keychain', '-d', 'user', '-s', CHAIN)
    if locked:
        run('security', 'lock-keychain', CHAIN)
    else:
        run('security', 'unlock-keychain', '-p', WORD, CHAIN)
    return run('security', 'default-keychain', '-d', 'user').stdout.strip()


def made():
    """WebKit's own key in the keychain."""
    return run('security', 'find-generic-password', '-a', ITEM, CHAIN).returncode == 0


def another():
    """The same, as a build that is signed otherwise."""
    copy = out.parent / 'another' / 'The Machine.app'
    shutil.rmtree(copy, ignore_errors=True)
    run('ditto', sandbox, str(copy))
    info = copy / 'Contents/Info.plist'
    info.write_bytes(plistlib.dumps({**plistlib.loads(info.read_bytes()), 'MadeUp': 'another'}))
    need(run('codesign', '--force', '--sign', '-', str(copy)).returncode == 0, 'signed')
    return str(copy)


def as_it_was(name, **how):
    """WebKit asks for the keychain: told, not judged, as that is macOS' own."""
    start(machine.at + '/', MACHINE_SANDBOX_KEYCHAIN='1', **how)
    found = stuck()
    time.sleep(2)
    png(name)
    keep(name)
    asks = [x['kCGWindowOwnerName'] for x in mac_tools.all_windows() if x['kCGWindowOwnerName'] in ('SecurityAgent', 'coreauthd', 'Keychain Access')]
    of = [(n, [w for w in ('defaultWebCryptoMasterKey', 'SecItemCopyMatching', 'SecItemAdd') if w in t]) for n, t in stacks().items()]
    answers = app.answers()
    told = log().strip().splitlines()
    app.kill()
    return f'{"STUCK" if found else "not stuck"}; the robot answers: {answers}; asked by {asks}; in its stacks: {of}; {told[:2]}'


def now(**how):
    start(machine.at + '/', **how)
    kept()
    told = clicked()
    need(not log(), log())
    return told


other()


@step('a locked keychain')
def _():
    where = chain(True)
    told = now()
    quit_it()
    start(anew=False)
    kept('kept again')
    need(len(saved()['pages']) == 32, 'its own')
    quit_it()
    chain(False)
    need(not made(), 'nothing of it in the keychain')
    return f'{where}; {told}'


@step('another build reads it too')
def _():
    chain(True)
    start(machine.at + '/')
    kept()
    quit_it()
    start(anew=False, bundle=another())
    kept('kept again')
    told = clicked()
    need(not log(), log())
    quit_it()
    return told


@step('a Machine that never answers')
def _():
    start('https://10.255.255.1/')
    for _ in range(3):
        told = clicked()
        time.sleep(12)
    png('never-answers')
    need(not log(), log())
    return told


@step('not signed in')
def _():
    start()
    need(until(app.window, 30), 'its window')
    time.sleep(2)
    told = clicked(twice=False)
    need(not log(), log())
    return told


@step('three starts at once')
def _():
    app.kill()
    fresh()
    for _ in range(3):
        run('open', '-n', sandbox, '--env', 'MACHINE_SANDBOX_ACCOUNT=' + machine.at)
    need(until(lambda: len(app.pids()) == 1, 20), app.pids())
    start(machine.at + '/')
    for _ in range(2):
        run('open', sandbox)
    time.sleep(3)
    told = clicked()
    need(not log(), log())
    return told


@step('it slept')
def _():
    start(machine.at + '/', window=False)
    need(until(app.robot, 20), 'the robot')
    os.kill(app.pid, signal.SIGSTOP)
    time.sleep(20)
    os.kill(app.pid, signal.SIGCONT)
    time.sleep(3)
    told = clicked()
    need(not log(), log())
    return told


@step('the page of the robot is stuck')
def _():
    start(machine.at + '/', window=False)
    need(until(app.robot, 20) and until(app.answers, 20), 'the robot')
    time.sleep(3)
    pages = [int(p) for p in run('pgrep', '-f', 'com.apple.WebKit.WebContent').stdout.split()]
    need(pages, 'pages')
    for p in pages:
        os.kill(p, signal.SIGSTOP)
    try:
        for _ in range(4):
            move(*app.center())
            time.sleep(1)
            click(*app.center())
            time.sleep(2)
        run('screencapture', '-x', '-C', str(out / 'stuck-page-with-the-pointer.png'))
        need(until(lambda: "the robot's page is made again" in log(), 150), log())
        need(until(app.answers, 10), 'a page that answers')
        png('page-made-again')
    finally:
        keep('stuck-page')
        for p in pages:
            with contextlib.suppress(ProcessLookupError):
                os.kill(p, signal.SIGCONT)
    need('the main thread' not in log(), log())
    told = ' | '.join(log().splitlines())
    time.sleep(5)
    return f'{clicked()}; {told}'


@step('the main thread is stuck')
def _():
    start(machine.at + '/', window=False)
    need(until(app.robot, 20), 'the robot')
    time.sleep(3)
    app.again('--hang', '14')
    need(stuck(12), 'the watch says so')
    need(until(lambda: 'answers again' in log(), 40), log())
    keep('stuck')
    told = stacks()
    need(told and all('Call graph:' in t and '/Users/' not in t for t in told.values()), f'{log()} {[t[:300] for t in told.values()]}')
    need(any('the_machine_desktop' in t for t in told.values()), 'with names')
    return f'{clicked()}; ' + ' | '.join(log().splitlines())


# How it was before its pages had a key of their own. Last, as what macOS asks may stay on the screen.
@step('a key of another build, as it was')
def _():
    chain(False)
    start(machine.at + '/', MACHINE_SANDBOX_KEYCHAIN='1')
    kept()
    need(made(), 'a key in the keychain')
    quit_it()
    return as_it_was('keychain-of-another', bundle=another())


@step('a locked keychain, as it was')
def _():
    run('security', 'delete-generic-password', '-a', ITEM, CHAIN)
    chain(True)
    return as_it_was('keychain-locked')


app.kill()
run('security', 'default-keychain', '-d', 'user', '-s', DEFAULT)
run('security', 'list-keychains', '-d', 'user', '-s', *SEARCHED)
run('security', 'delete-keychain', CHAIN)
finish()

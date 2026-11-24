"""What window.py needs of a Mac."""
import contextlib
import json
import os
import pathlib
import subprocess
import threading
import time

import mac_tools
from mac_tools import (  # noqa: F401 (window.py's)
    A, C, CMD, CTRL, ENTER, ESCAPE, F, ID, LIBRARY, MAIL, NAME, PORT, Q, V, W, App, click, drag, finish, fresh, in_front, key, need, need_window, no_browser, other,
    out, page, png, press, run, sandbox, saved, says, screens, step, until, work_area, write,
)

SYSTEM, VERSION, DOWNLOADS = 'mac', 'macOS ' + mac_tools.VERSION + ' ' + json.dumps(screens()), pathlib.Path.home() / 'Downloads'
R, G, ZERO, PLUS, MINUS, COMMA, S, LEFT, M, Z = 15, 5, 29, 24, 27, 43, 1, 33, 46, 6
SHIFT = 1 << 17
KEYS = {'close': W, 'find': F, 'reload': R, 'save': S, 'all': A, 'copy': C, 'paste': V, 'undo': Z, 'zoom none': ZERO, 'zoom in': PLUS, 'zoom out': MINUS, 'settings': COMMA, 'back': LEFT}


def hit(name):
    if name in ('full', 'find back'):
        return key(F, CMD | CTRL) if name == 'full' else key(G, CMD | SHIFT)
    key(KEYS[name], CMD)


def ask(what):
    return run('osascript', '-e', f'tell application "System Events" to tell process "{NAME}" to {what}')


def names(app):
    return ask('get name of every window').stdout.strip()


def menu(of, name):
    made = ask(f'click menu item "{name}" of menu 1 of menu bar item "{of}" of menu bar 1')
    need(made.returncode == 0, made.stderr)
    time.sleep(0.5)


def dialog(app):
    told = ask('get value of static texts of sheet 1 of window 1')
    return told.stdout.strip() if told.returncode == 0 else ''


def here(app, selector, name='app'):
    """Where something in a window is on the screen: its page may be zoomed, under the title bar."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [e.x + e.width / 2, e.y + e.height / 2, innerWidth, innerHeight] }})()')
    r = need_window(app.window() if name == 'app' else app.settings())
    by = r.width / at[2]
    return round(r.left + at[0] * by), round(r.bottom - (at[3] - at[1]) * by)


def ours():
    return ID in in_front()


def reopen(app):
    run('open', sandbox)


def back_to_it(app):
    until(lambda: 'Safari' not in in_front(), 8)
    if not ours():
        reopen(app)
    need(until(ours, 10), f'in front: {in_front()}')
    time.sleep(1)


def minimize(app):
    key(M, CMD)


def quit_it(app):
    key(Q, CMD)


def settings_open(app):
    menu('The Machine', 'Settings…')


def clipboard(text=None):
    return run('pbpaste').stdout if text is None else run('pbcopy', input=text)


def place(app, x, y, wide, high):
    of = '(first window whose subrole is "AXStandardWindow")'
    ask(f'set position of {of} to {{{x}, {y}}}')
    ask(f'set size of {of} to {{{wide}, {high}}}')


def area():
    return work_area()


def whole():
    return screens()[0]['whole']


def dark(on):
    run('osascript', '-e', f'tell application "System Events" to tell appearance preferences to set dark mode to {str(on).lower()}')


def like_any_app(app):
    kind = run('lsappinfo', 'info', '-only', 'ApplicationType', ID).stdout.strip()
    need('Foreground' in kind, kind)


def marked(file):
    return 'com.apple.quarantine' in run('xattr', str(file)).stdout


def choose(file):
    key(G, CMD | SHIFT)
    time.sleep(1)
    write(str(file))
    time.sleep(0.5)
    key(ENTER)
    time.sleep(1)
    key(ENTER)


@contextlib.contextmanager
def drop_from(app, *files):
    source = out.parent / 'source'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-o', str(source), str(pathlib.Path(__file__).with_name('source.m')))
    need(made.returncode == 0, made.stderr)
    grab = subprocess.Popen([str(source), *map(str, files)])
    try:
        time.sleep(1.5)
        x, y = here(app, '#drop')
        need(not (40 <= x <= 440 and 100 <= y <= 200), f'the drop is beside it: {x},{y} in {app.window()}')
        yield 100, 150
    finally:
        grab.terminate()


def icon_there():
    return ask('get name of menu bar item 1 of menu bar 2').returncode == 0


def pages_killed():
    pids = [int(x) for x in run('pgrep', '-f', 'com.apple.WebKit.WebContent').stdout.split()]
    need(pids, 'its process')
    for pid in pids:
        os.kill(pid, 9)


def link(app, address):
    need(run('open', '-a', sandbox, address).returncode == 0, 'the link it goes to')


def second(app, look):
    """At two pixels a point, on a screen that isn't there."""
    maker = out.parent / 'screen'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-framework', 'CoreGraphics', '-Wl,-U,_OBJC_CLASS_$_CGVirtualDisplay', '-o', str(maker), str(pathlib.Path(__file__).with_name('screen.m')))
    need(made.returncode == 0, made.stderr)
    runs = subprocess.Popen([str(maker)], stdout=subprocess.PIPE, text=True)
    try:
        if not until(lambda: len(screens()) == 2, 10):
            return print('no second screen here', flush=True)
        time.sleep(2)
        free = work_area(1)
        place(app, free[0] + 20, free[1] + 20, 1200, 700)
        time.sleep(3)
        look()
    finally:
        runs.terminate()
        runs.wait()
        time.sleep(2)


def crashes():
    return [p.name for p in (LIBRARY / 'Logs/DiagnosticReports').glob(NAME + '*')]


def nothing_left():
    pass


def no_network():
    """Python, not the app, may be asked about: it is said no to, as it needs nothing there."""
    while True:
        of = 'tell application "System Events" to tell process "UserNotificationCenter"'
        if 'Python' in run('osascript', '-e', f'{of} to get value of static texts of window 1').stdout:
            run('osascript', '-e', f'{of} to click button "Don’t Allow" of window 1')
        time.sleep(3)


threading.Thread(target=no_network, daemon=True).start()

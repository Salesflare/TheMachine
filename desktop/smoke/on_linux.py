"""What window.py needs of Linux: on a screen that isn't there, with a home of its own (linux.sh), and never on a desktop in use."""
import contextlib
import json
import os
import pathlib
import shutil
import signal
import socket
import subprocess
import sys
import time
import traceback

import answers

HOME = pathlib.Path.home()
if not (HOME / '.made-up-home').exists():
    sys.exit('only by linux.sh')
PORT, DEBUG, ID = 8941, 9227, 'computer.themachine.desktop'
SYSTEM, VERSION, DOWNLOADS = 'linux', 'Linux, ' + os.environ.get('GDK_BACKEND', ''), HOME / 'Downloads'
ENTER, ESCAPE = 'Return', 'Escape'
KEYS = {'close': 'ctrl+w', 'find': 'ctrl+f', 'find back': 'ctrl+shift+g', 'reload': 'ctrl+r', 'save': 'ctrl+s', 'all': 'ctrl+a', 'copy': 'ctrl+c', 'paste': 'ctrl+v', 'undo': 'ctrl+z',
        'zoom none': 'ctrl+0', 'zoom in': 'ctrl+plus', 'zoom out': 'ctrl+minus', 'settings': 'ctrl+comma', 'back': 'alt+Left', 'full': 'F11'}
sandbox = str(pathlib.Path(sys.argv[1]).resolve())
out = pathlib.Path(sys.argv[3]).resolve()
out.mkdir(parents=True, exist_ok=True)
MAIL = out / 'mail.txt'
results = []


def run(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, timeout=kw.pop('timeout', 30), **kw)


def x(*args):
    return run('xdotool', *map(str, args)).stdout.strip()


def png(name):
    time.sleep(0.4)
    run('import', '-window', 'root', str(out / f'{name}.png'))


def until(what, seconds=15, every=0.25):
    end = time.time() + seconds
    while True:
        found = what()
        if found or time.time() > end:
            return found
        time.sleep(every)


def need(ok, text):
    if not ok:
        raise AssertionError(text)


def pointer():
    return [int(v.split(':')[1]) for v in x('getmouselocation').split()[:2]]


def click(at_x, at_y):
    x('mousemove', at_x - 3, at_y, 'mousemove', at_x, at_y)
    time.sleep(0.15)
    x('mousedown', 1)
    time.sleep(0.06)
    x('mouseup', 1)
    time.sleep(0.5)


def drag(a, b, steps=25):
    x('mousemove', *a)
    time.sleep(0.2)
    x('mousedown', 1)
    for i in range(1, steps + 1):
        x('mousemove', round(a[0] + (b[0] - a[0]) * i / steps), round(a[1] + (b[1] - a[1]) * i / steps))
        time.sleep(0.03)
    for i in range(4):
        time.sleep(0.25)
        x('mousemove', b[0] + i % 2, b[1])
    x('mouseup', 1)
    time.sleep(0.4)


def key(name):
    x('key', '--clearmodifiers', name)
    time.sleep(0.1)


def hit(name):
    key(KEYS[name])


def write(text):
    x('type', '--delay', 20, text)
    time.sleep(0.2)


class Rect:
    def __init__(self, window, told):
        of = dict(line.split('=') for line in told.split('\n') if '=' in line)
        self.id, self.left, self.top, self.width, self.height = window, int(of['X']), int(of['Y']), int(of['WIDTH']), int(of['HEIGHT'])
        self.right, self.bottom = self.left + self.width, self.top + self.height

    def __repr__(self):
        return f'{self.left},{self.top} {self.width}x{self.height}'


def named(window):
    return x('getwindowname', window)


class App:
    last = None

    def __init__(self, program, window=True, account=None):
        if App.last:
            App.last.kill()
        self.env = dict(os.environ, MACHINE_SANDBOX_ACCOUNT=account or f'http://127.0.0.1:{PORT}', MACHINE_SANDBOX_MAIL=str(MAIL), MACHINE_SANDBOX_DEBUG=str(DEBUG))
        self.program = program
        with (out / 'app.txt').open('a') as told:
            self.process = subprocess.Popen([program, *(() if window else ('--login',))], env=self.env, stdout=told, stderr=told)
        App.last = self

    def pids(self):
        return [self.process.pid] if self.process.poll() is None else []

    def again(self, *args, seconds=15):
        return subprocess.run([self.program, *args], env=self.env, timeout=seconds, capture_output=True).returncode

    def all(self):
        """Its windows: each, and whether it stays on top."""
        found = []
        looks = lambda: run('xdotool', 'search', '--all', '--onlyvisible', '--pid', str(self.process.pid), '')
        told = looks()
        if told.returncode and 'X Error' in told.stderr:  # a window went while it looked
            told = looks()
        for window in told.stdout.split():
            told = x('getwindowgeometry', '--shell', window)
            state = run('obxprop', '--id', window).stdout
            if 'WIDTH=' in told and '_NET_WM_WINDOW_TYPE' in state and '_NET_WM_WINDOW_TYPE_TOOLTIP' not in state:
                r = Rect(window, told)
                if r.width > 40 and r.height > 20:
                    found.append((r, '_NET_WM_STATE_ABOVE' in state or '_NET_WM_STATE_SKIP_TASKBAR' in state))
        return found

    def raw(self):
        return self.all()

    def plain(self):
        return [r for r, above in self.all() if not above]

    def window(self):
        if not getattr(self, 'its', None):
            self.its = next((r.id for r in self.plain() if named(r.id) in ('The Machine', 'Stand-in ') or named(r.id).startswith('The Machine')), None)
        return next((r for r in self.plain() if r.id == self.its), None)

    def settings(self):
        return next((r for r in self.plain() if named(r.id) == 'Settings'), None)

    def sized(self, least, most):
        return next((r for r, above in self.all() if above and least <= r.width < most), None)

    def robot(self):
        return self.sized(40, 250)

    def box(self):
        return self.sized(350, 999)

    def card(self):
        return self.sized(333, 350)

    def center(self):
        r = self.robot()
        need(r, 'the robot is there')
        return (r.left + r.right) // 2, (r.top + r.bottom) // 2

    def answers(self, name='robot'):
        try:
            return page(name, '1') == 1
        except (OSError, ValueError):
            return False

    def ended(self, seconds=8):
        return until(lambda: self.process.poll() is not None, seconds)

    def kill(self):
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait()


def page(name, script, wait=10):
    """What a page says about itself: only read, never clicked this way."""
    with socket.create_connection(('127.0.0.1', DEBUG), wait) as s:
        s.sendall(f'{name}\nJSON.stringify({script}) ?? "null"'.encode())
        s.shutdown(socket.SHUT_WR)
        raw = b''.join(iter(lambda: s.recv(65536), b'')).decode()
    told = json.loads(raw) if raw else None
    return json.loads(told) if isinstance(told, str) else told


def says(selector, name='box'):
    shown = page(name, f'(e => e && e.getClientRects().length ? e.innerText : "")(document.querySelector({json.dumps(selector)}))')
    return (shown or '').strip()


def here(app, selector, name='app'):
    """Where something in a window is on the screen: its page may be zoomed, under the bar that finds."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [e.x + e.width / 2, e.y + e.height / 2, innerWidth, innerHeight] }})()')
    r = {'app': app.window, 'settings': app.settings, 'box': app.box, 'card': app.card}[name]()
    need(r, f'the window is there: {name}')
    by = r.width / at[2]
    return round(r.left + at[0] * by), round(r.bottom - (at[3] - at[1]) * by)


def press(app, selector, name='box'):
    was, at = None, here(app, selector, name)
    for _ in range(20):  # it may still be getting as tall as what is in it
        if at == was:
            break
        time.sleep(0.2)
        was, at = at, here(app, selector, name)
    click(*at)


def in_front():
    window = x('getactivewindow')
    return named(window), x('getwindowpid', window)


def ours():
    return App.last and in_front()[1] == str(App.last.process.pid)


OTHER = """
import gi, sys
gi.require_version('Gtk', '3.0'), gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
w = Gtk.Window(title='other')
w.move(20, 700), w.set_default_size(300, 100)
w.add(Gtk.Entry())
w.connect('destroy', Gtk.main_quit)
w.show_all()
Gtk.main()
"""
SOURCE = """
import gi, pathlib, sys
gi.require_version('Gtk', '3.0'), gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
w = Gtk.Window(title='source')
w.set_default_size(160, 100), w.move(40, 60), w.set_keep_above(True)
b = Gtk.EventBox()
b.add(Gtk.Label(label='files'))
b.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
b.drag_source_add_uri_targets()
b.connect('drag-data-get', lambda b, c, data, i, t: data.set_uris([pathlib.Path(p).as_uri() for p in sys.argv[1:]]))
w.add(b)
w.show_all()
Gtk.main()
"""
PYTHON = '/usr/bin/python3'
others = []


def other():
    """Another program in front, with the keys."""
    if not others or others[0].poll() is not None:
        others[:] = [subprocess.Popen([PYTHON, '-c', OTHER])]
    there = lambda: x('search', '--onlyvisible', '--name', '^other$').split()
    need(until(there, 10), 'another program')
    x('windowactivate', there()[0])
    need(until(lambda: in_front()[0] == 'other', 5), f'it is in front: {in_front()}')
    time.sleep(1)
    return in_front()


def reopen(app):
    app.again()


def back_to_it(app):
    app.again()
    need(until(ours, 10), f'in front: {in_front()}')
    time.sleep(1)


def no_browser():
    """linux.sh's xdg-open shows nothing."""


def minimize(app):
    x('windowminimize', app.window().id)


def quit_it(app):
    key('ctrl+q')


def settings_open(app):
    hit('settings')


def dialog(app):
    """The page waits for an answer."""
    try:
        return page('app', '1', 1.5) != 1
    except OSError:
        return True


def clipboard(text=None):
    if text is None:
        return run('xclip', '-o', '-selection', 'clipboard').stdout
    subprocess.run(['xclip', '-selection', 'clipboard'], input=text, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def place(app, at_x, at_y, wide, high):
    window = app.window().id
    x('windowsize', window, wide, high)
    x('windowmove', window, at_x, at_y)


def area():
    return whole()


def whole():
    wide, high = map(int, x('getdisplaygeometry').split())
    return 0, 0, wide, high


def dark(on):
    """linux.sh's THEME, for the whole run."""


def like_any_app(app):
    need(app.window() in app.plain() or app.window(), 'a window like any')


def marked(file):
    return True  # nothing on Linux marks them


def names(app):
    return ', '.join(named(r.id) for r in app.plain())


@contextlib.contextmanager
def drop_from(app, *files):
    place(app, 500, 80, 1100, 760)
    source = subprocess.Popen([PYTHON, '-c', SOURCE, *map(str, files)])
    try:
        need(until(lambda: x('search', '--onlyvisible', '--name', '^source$'), 10), 'a window to drag from')
        time.sleep(1)
        yield 100, 110
    finally:
        source.kill()


def choose(file):
    time.sleep(1)
    write('/')  # shows the field
    time.sleep(0.8)
    write(str(file)[1:])
    time.sleep(0.8)
    key(ENTER)


def icon_there():
    return False


def pages_killed():
    """Only those of this home: there may be a person's own."""
    killed = 0
    for of in pathlib.Path('/proc').glob('[0-9]*'):
        with contextlib.suppress(OSError):
            if 'WebKitWebProces' in (of / 'comm').read_text() and f'HOME={HOME}'.encode() in (of / 'environ').read_bytes().split(b'\0'):
                os.kill(int(of.name), signal.SIGKILL)
                killed += 1
    need(killed, 'its process')


def link(app, address):
    app.again(address)


def second(app, look):
    print('no second screen here', flush=True)


def crashes():
    return []


def kept():
    """The notifications the desktop shows."""
    return ['one'] * int(run('dunstctl', 'count', 'displayed').stdout.strip() or 0)


def known_there():
    return 'The Machine'


def on_screen(text):
    found = x('search', '--onlyvisible', '--class', 'Dunst').split()
    r = found and Rect(found[0], x('getwindowgeometry', '--shell', found[0]))
    return (r.left + r.width // 2, r.top + r.height // 2) if r else None


def nothing_left():
    need(not kept(), f'its notifications: {kept()}')


def fresh():
    for folder in ('.config', '.local/share', '.cache'):
        shutil.rmtree(HOME / folder / ID, ignore_errors=True)


def saved():
    return json.loads((HOME / '.config' / ID / 'app.json').read_text())


def step(name):
    def do(f):
        try:
            results.append((name, True, f() or ''))
        except Exception as e:  # noqa: BLE001 (the next steps still tell something)
            results.append((name, False, f'{type(e).__name__}: {e}'))
            traceback.print_exc()
        robot = App.last and App.last.pids() and answers.after(HOME / '.config' / ID / 'hangs.log', out, len(results), App.last.center, pointer, lambda *at: x('mousemove', *at), lambda: page('robot', '1', 4))
        if robot and results[-1][1]:
            results[-1] = (name, False, f'{robot}; {results[-1][2]}')
        png(f'{len(results):02d}-{name.replace(" ", "-")}')
        print(line(*results[-1]), flush=True)
    return do


def line(name, ok, told):
    told = str(told)
    return f"{'FAIL' if not ok else 'skip' if told.startswith('NOT TESTED') else 'ok  '} {name}  {told}"


def finish():
    failed = [r for r in results if not r[1]]
    lines = [line(*r) for r in results]
    skipped = sum(x.startswith('skip') for x in lines)
    lines.append(f'{VERSION}: {len(results) - len(failed) - skipped} ok, {len(failed)} failed, {skipped} skipped')
    (out / 'results.txt').write_text('\n'.join(lines) + '\n')
    print(lines[-1])
    for p in others:
        p.kill()
    sys.exit(bool(failed))

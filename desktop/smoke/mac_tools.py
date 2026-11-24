"""What mac.py and mac_window.py share: the screen, the mouse and the keys, the app's windows and pages, and the steps."""
import base64
import ctypes
import json
import os
import pathlib
import plistlib
import shutil
import socket
import subprocess
import sys
import time
import traceback
import uuid

PORT, DEBUG, ID, NAME = 8941, 9227, 'computer.themachine.desktop', 'the-machine-desktop'
cg = ctypes.CDLL('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')
cf = ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')


class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]


P, U = ctypes.c_void_p, ctypes.c_uint32
for f, r, a in ((cg.CGEventCreateMouseEvent, P, [P, U, Point, U]), (cg.CGEventCreateKeyboardEvent, P, [P, ctypes.c_uint16, ctypes.c_bool]),
                (cg.CGEventSetIntegerValueField, None, [P, U, ctypes.c_int64]), (cg.CGEventSetFlags, None, [P, ctypes.c_uint64]),
                (cg.CGEventKeyboardSetUnicodeString, None, [P, ctypes.c_ulong, P]), (cg.CGEventPost, None, [U, P]), (cf.CFRelease, None, [P]),
                (cg.CGWindowListCopyWindowInfo, P, [U, U]), (cf.CFPropertyListCreateData, P, [P, P, ctypes.c_long, U, P]),
                (cf.CFDataGetBytePtr, P, [P]), (cf.CFDataGetLength, ctypes.c_long, [P])):
    f.restype, f.argtypes = r, a

out = pathlib.Path(sys.argv[3]).resolve()
MAIL = out / 'mail.txt'  # where the app leaves an address for the mail app
out.mkdir(parents=True, exist_ok=True)
CERTIFICATE = pathlib.Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
results = []


# The screen, the mouse and the keys

def run(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, timeout=kw.pop('timeout', 60), **kw)


def js(script):
    made = run('osascript', '-l', 'JavaScript', '-e', "ObjC.import('AppKit');" + script)
    return json.loads(made.stdout) if made.stdout.strip() else None


def png(name):
    time.sleep(0.4)
    run('screencapture', '-x', *[str(out / f'{name}{n}.png') for n in ('', '-second-screen')[:len(screens())]])


def screens():
    """Each screen: its whole, and what the menu bar and the Dock leave of it, counted from the main one's top left."""
    found = js('''const all = $.NSScreen.screens.js, top = all[0].frame.size.height;
      const r = f => [f.origin.x, top - f.origin.y - f.size.height, f.origin.x + f.size.width, top - f.origin.y].map(Math.round);
      JSON.stringify(all.map(s => ({name: s.localizedName.js, whole: r(s.frame), free: r(s.visibleFrame), scale: s.backingScaleFactor})))''')
    need(found, 'the screens are known')
    return found


def work_area(n=0):
    return screens()[n]['free']


def post(event):
    cg.CGEventPost(0, event)
    cf.CFRelease(event)


def mouse(kind, x, y, button=0, count=0, flags=0):
    event = cg.CGEventCreateMouseEvent(None, kind, Point(x, y), button)
    cg.CGEventSetFlags(event, flags)  # else Command or Control may still be down
    if count:
        cg.CGEventSetIntegerValueField(event, 1, count)
    post(event)


def move(x, y):
    mouse(5, x, y)
    time.sleep(0.03)


def click(x, y, right=False, flags=0):
    move(x - 3, y)
    move(x, y)
    time.sleep(0.15)
    mouse(3 if right else 1, x, y, int(right), 1, flags)
    time.sleep(0.06)
    mouse(4 if right else 2, x, y, int(right), 1, flags)
    time.sleep(0.5)


def drag(a, b, steps=25):
    move(*a)
    time.sleep(0.2)
    mouse(1, *a, 0, 1)
    for i in range(1, steps + 1):
        mouse(6, a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps)
        time.sleep(0.03)
    time.sleep(0.3)
    mouse(2, *b, 0, 1)
    time.sleep(0.2)
    move(b[0] + 1, b[1])  # as a hand does: macOS 15 may only tell that the button is up with what comes next
    time.sleep(0.4)


ENTER, ESCAPE, DOWN, UP, BACK, TAB, A, C, V, Q, W, F = 36, 53, 125, 126, 51, 48, 0, 8, 9, 12, 13, 3
CMD, CTRL = 1 << 20, 1 << 18


def key(code, flags=0):
    for down in (True, False):
        event = cg.CGEventCreateKeyboardEvent(None, code, down)
        cg.CGEventSetFlags(event, flags)
        post(event)
        time.sleep(0.03)
    time.sleep(0.05)


def write(text):
    for c in text:
        raw = c.encode('utf-16-le')
        for down in (True, False):
            event = cg.CGEventCreateKeyboardEvent(None, 0, down)
            cg.CGEventSetFlags(event, 0)
            cg.CGEventKeyboardSetUnicodeString(event, len(raw) // 2, raw)
            post(event)
        time.sleep(0.02)
    time.sleep(0.2)


def all_windows():
    """What is on the screen, the front one first."""
    found = cg.CGWindowListCopyWindowInfo(1 | 16, 0)
    data = cf.CFPropertyListCreateData(None, found, 100, 0, None)
    raw = ctypes.string_at(cf.CFDataGetBytePtr(data), cf.CFDataGetLength(data))
    cf.CFRelease(data), cf.CFRelease(found)
    return plistlib.loads(raw)


def in_front():
    told = run('lsappinfo', 'info', '-only', 'bundleid', run('lsappinfo', 'front').stdout.strip()).stdout
    return told.split('"')[-2] if told.count('"') >= 2 else told.strip()


# The app's windows and pages

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


class Rect:
    def __init__(self, b):
        self.left, self.top = round(b['X']), round(b['Y'])
        self.width, self.height = round(b['Width']), round(b['Height'])
        self.right, self.bottom = self.left + self.width, self.top + self.height

    def __repr__(self):
        return f'{self.left},{self.top} {self.width}x{self.height}'


class App:
    def __init__(self, bundle, debug=True, over=None, window=False, account=None):
        self.bundle, self.program = bundle, str(pathlib.Path(bundle, 'Contents/MacOS', NAME))
        for pid in self.pids():  # a step before this one failed
            os.kill(pid, 9)
        until(lambda: not self.pids(), 5)
        env = {'MACHINE_SANDBOX_ACCOUNT': account or f'http://127.0.0.1:{PORT}', 'MACHINE_SANDBOX_MAIL': str(MAIL), **({'MACHINE_SANDBOX_DEBUG': str(DEBUG)} if debug else {})}
        if over:
            env.update(MACHINE_SANDBOX_ACCOUNT=over.at, MACHINE_SANDBOX_ROOT=str(CERTIFICATE / 'root.pem'))
        self.env = dict(os.environ, **env)
        # As Finder does, or as macOS at login: that takes nothing from the front
        made = run('open', '-n', *(() if window else ('-g',)), bundle, *[x for k, v in env.items() for x in ('--env', f'{k}={v}')], *(() if window else ('--args', '--login')))
        need(made.returncode == 0, made.stderr)
        self.pid = until(lambda: next(iter(self.pids()), None), 20)

    def pids(self):
        return [int(x) for x in run('pgrep', '-x', NAME).stdout.split()]

    def again(self, *args, seconds=15):
        return subprocess.run([self.program, *args], env=self.env, timeout=seconds).returncode

    def raw(self):
        return [x for x in all_windows() if x['kCGWindowOwnerPID'] == self.pid and 0 < x['kCGWindowLayer'] < 20 and x['kCGWindowBounds']['Width'] > 40]

    def windows(self):
        return [Rect(x['kCGWindowBounds']) for x in self.raw()]

    def plain(self):
        """Its windows like any program's, the front one first."""
        own = [x for x in all_windows() if x['kCGWindowOwnerPID'] == self.pid and x['kCGWindowLayer'] == 0]
        return [r for r in (Rect(x['kCGWindowBounds']) for x in own) if r.width > 300 and r.height > 100]

    def window(self):
        return next((r for r in self.plain() if r.height >= 400), None)

    def settings(self):
        return next((r for r in self.plain() if r.height < 400 and r.width == 420), None)

    def robot(self):
        return next((r for r in self.windows() if r.width < 250), None)

    def wide(self):
        return [r for r in self.windows() if r.width >= 250]

    def sized(self, least, most):
        return next((r for r in self.wide() if least <= r.width < most), None)

    def box(self):
        return self.sized(350, 999)

    def card(self):
        return self.sized(333, 350)

    def bubble(self):
        return self.sized(250, 333)

    def center(self):
        r = need_window(self.robot())
        return (r.left + r.right) // 2, (r.top + r.bottom) // 2

    def answers(self, name='robot'):
        try:
            return page(name, '1') == 1
        except (OSError, ValueError):
            return False

    def ended(self, seconds=8):
        return until(lambda: not self.pids(), seconds)

    def kill(self):
        for pid in self.pids():
            os.kill(pid, 9)


def need_window(found):
    need(found, 'the window is there')
    return found


def page(name, script):
    """What a page says about itself: only read, never clicked this way."""
    with socket.create_connection(('127.0.0.1', DEBUG), 10) as s:
        s.sendall(f'{name}\nJSON.stringify({script}) ?? "null"'.encode())
        s.shutdown(socket.SHUT_WR)
        raw = b''.join(iter(lambda: s.recv(65536), b'')).decode()
    told = json.loads(raw) if raw else None
    return json.loads(told) if isinstance(told, str) else told


def says(selector, name='box'):
    shown = page(name, f'(e => e && e.getClientRects().length ? e.innerText : "")(document.querySelector({json.dumps(selector)}))')
    return (shown or '').strip()


def press(app, selector, name='box'):
    """A real click on something in a page, where it says it is."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [e.x + e.width / 2, e.y + e.height / 2] }})()')
    r = need_window({'box': app.box, 'card': app.card, 'bubble': app.bubble}[name]())
    click(round(r.left + at[0]), round(r.top + at[1]))


def shut(app):
    """The dashboard's window closed, and another program in front."""
    need(until(app.window), 'the window is there')
    key(W, CMD)
    need(until(lambda: not app.window()), 'it closes')
    other()
    need(until(app.robot), 'the robot is there')


def in_corner(app, n=0):
    """In the bottom right corner of what the Dock and the menu bar leave: 16 and 12 from its edges."""
    r, area = need_window(app.robot()), work_area(n)
    return abs(area[2] - r.right - 16) <= 1 and abs(area[3] - r.bottom - 12) <= 1 and r.width == 88, f'robot {r}, free {area}, {screens()[n]["scale"]} pixels a point'


def step(name):
    def do(f):
        try:
            told = f() or ''
            results.append((name, True, told))
        except Exception as e:  # noqa: BLE001 (the next steps still tell something)
            results.append((name, False, f'{type(e).__name__}: {e}'))
            traceback.print_exc()
        try:
            png(f'{len(results):02d}-{name.replace(" ", "-")}')
        except Exception:  # noqa: BLE001
            traceback.print_exc()
        print(line(*results[-1]), flush=True)
    return do


def line(name, ok, told):
    told = str(told)
    return f"{'FAIL' if not ok else 'skip' if told.startswith('NOT TESTED') else 'ok  '} {name}  {told}"


LIBRARY = pathlib.Path.home() / 'Library'


def fresh():
    for folder in ('Application Support', 'Caches', 'WebKit'):
        shutil.rmtree(LIBRARY / folder / ID, ignore_errors=True)
    run('defaults', 'delete', ID)


def saved():
    return json.loads((LIBRARY / 'Application Support' / ID / 'app.json').read_text())


def other(name='TextEdit'):
    """Another program in front, with the keys."""
    run('open', '-a', name)
    need(until(lambda: name.lower() in in_front().lower(), 15), f'{name} is in front: {in_front()}')
    time.sleep(1)
    return in_front()


def tray(app):
    """Where its icon in the menu bar is."""
    ask = lambda: run('osascript', '-e', f'tell application "System Events" to tell process "{NAME}" to get {{position, size}} of menu bar item 1 of menu bar 2')
    until(lambda: ask().returncode == 0, 5)
    told = ask()
    need(told.returncode == 0, told.stderr)
    x, y, wide, high = (int(v) for v in told.stdout.split(','))
    return x + wide // 2, y + high // 2


def tray_menu(app, name):
    at = tray(app)
    click(*at)
    told = run('osascript', '-e', f'tell application "System Events" to tell process "{NAME}" to get name of menu items of menu 1 of menu bar item 1 of menu bar 2').stdout.strip()
    png('menu-bar-' + name.lower().replace(' ', '-'))
    need(name in told, f'its menu: {told}')
    for _ in range([x.strip() for x in told.split(',')].index(name) + 1):
        key(DOWN)
    key(ENTER)
    return told


def downloaded(bundle):
    """A copy, marked as what a browser downloaded, and opened."""
    copy = out.parent / 'downloads' / 'The Machine.app'
    shutil.rmtree(copy, ignore_errors=True)
    run('ditto', bundle, str(copy))
    run('xattr', '-r', '-w', 'com.apple.quarantine', f'0083;{int(time.time()):08x};Safari;{uuid.uuid4()}', str(copy))
    subprocess.Popen(['open', str(copy)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return copy


def asks(button=None):
    """The buttons of what macOS asks about it; one of them is clicked."""
    of = 'tell application "System Events" to tell process "CoreServicesUIAgent"'
    told = run('osascript', '-e', f'{of} to get name of buttons of window 1').stdout.strip()
    if button and button in told:
        run('osascript', '-e', f'{of} to click button "{button}" of window 1')
    return told


def finish():
    for report in (LIBRARY / 'Logs/DiagnosticReports').glob(NAME + '*'):
        shutil.copy(report, out)
    (out / 'note.txt').unlink()
    failed = [r for r in results if not r[1]]
    lines = [line(*r) for r in results]
    skipped = sum(x.startswith('skip') for x in lines)
    lines.append(f'macOS {VERSION}: {len(results) - len(failed) - skipped} ok, {len(failed)} failed, {skipped} skipped')
    (out / 'results.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(lines[-1])
    sys.exit(bool(failed))


sandbox, people = (p if p == '-' else str(pathlib.Path(p).resolve()) for p in sys.argv[1:3])
VERSION = run('sw_vers', '-productVersion').stdout.strip() + ' ' + os.uname().machine

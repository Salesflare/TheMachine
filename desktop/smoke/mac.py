"""Runs the app on a Mac as a person would: real mouse and keys, against a made-up Machine, with a screenshot of each step.
For CI's own throwaway computer (desktop.yml): it moves the mouse, changes the screen, the Dock and dark mode.

  python3 smoke/mac.py <sandbox build> <build for people> <folder for the pictures>
  python3 smoke/mac.py - <signed build for people> <folder for the pictures>
"""
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

from standin import SNOOZE, Machine, TODOS

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
out.mkdir(parents=True, exist_ok=True)
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
    def __init__(self, bundle, debug=True):
        self.bundle, self.program = bundle, str(pathlib.Path(bundle, 'Contents/MacOS', NAME))
        for pid in self.pids():  # a step before this one failed
            os.kill(pid, 9)
        until(lambda: not self.pids(), 5)
        env = {'MACHINE_SANDBOX_ACCOUNT': f'http://127.0.0.1:{PORT}', **({'MACHINE_SANDBOX_DEBUG': str(DEBUG)} if debug else {})}
        self.env = dict(os.environ, **env)
        made = run('open', '-n', bundle, *[x for k, v in env.items() for x in ('--env', f'{k}={v}')])  # as Finder does
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

    def answers(self):
        try:
            return page('robot', '1') == 1
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
fresh()
VERSION = run('sw_vers', '-productVersion').stdout.strip() + ' ' + os.uname().machine
print('macOS', VERSION, json.dumps(screens()), flush=True)
png('00-before')
(out / 'note.txt').write_text('made up')


# The build for people, as it first starts

ours = other()
app = App(people, debug=False)


@step('first start')
def _():
    need(until(app.robot, 60), 'the robot shows')
    time.sleep(3)
    ok, told = in_corner(app)
    need(ok, told)
    return f'{VERSION}; {told}; in front {in_front()}; {[(x["kCGWindowLayer"], Rect(x["kCGWindowBounds"])) for x in app.raw()]}'


@step('first start opens the sign-in')
def _():
    need(until(app.box, 10), 'the box opens by itself')


@step('click closes and opens')
def _():
    had = bool(app.box())
    for wanted in (not had, had, not had, True):
        if bool(app.box()) == wanted:
            continue
        click(*app.center())
        need(until(lambda: bool(app.box()) == wanted, 8), f'the box is {"open" if wanted else "closed"}')


@step('quit from a second start')
def _():
    app.again('--quit')
    need(app.ended(), 'the process is gone')


app.kill()
fresh()
SIGNED = sandbox == '-'


@step('opened as a download')
def _():
    global app
    told = run('spctl', '--status')
    copy = downloaded(people)
    try:
        buttons = until(asks, 120)  # an Intel runner takes its time
        time.sleep(1)
        png('macos-asks-about-the-download')
        told = f'{(told.stdout + told.stderr).strip()}; {run("spctl", "--assess", "-vv", str(copy)).stderr.strip()}; asks: {buttons}'
        if not buttons:
            return 'NOT TESTED: macOS asks nothing here: ' + told
        if SIGNED:
            need('Open' in buttons, told)
            asks('Open')
            need(until(app.pids, 30), 'it starts ' + told)
            app.pid = app.pids()[0]
            need(until(app.robot, 30) and until(app.box, 10), 'the robot shows, with its box')
            time.sleep(2)
            png('the-download-open')
            app.again('--quit')
            need(app.ended(), 'the process is gone')
            subprocess.Popen(['open', str(copy)])
            need(until(app.pids, 20), 'the second time nothing is asked')
            app.again('--quit')
        else:
            asks('Done')
            time.sleep(1)
            run('open', 'x-apple.systempreferences:com.apple.settings.PrivacySecurity.extension?Security')
            time.sleep(6)
            png('macos-settings-open-anyway')
            run('osascript', '-e', 'tell application "System Settings" to quit')
        return told
    finally:
        app.kill()
        shutil.rmtree(copy, ignore_errors=True)
        fresh()


if SIGNED:
    finish()


# The same with a made-up Machine

socket.getfqdn = lambda *_: 'localhost'  # else Python looks for this computer's name on the network, and macOS asks about that
machine = Machine(PORT)
other()
app = App(sandbox)


@step('sandbox first start')
def _():
    need(until(app.box, 30), 'the box opens by itself')
    need(until(lambda: says('#signin-go'), 10), 'it offers the sign-in')
    need(says('#state') == 'Not signed in', says('#state'))
    levels = [(x['kCGWindowLayer'], Rect(x['kCGWindowBounds'])) for x in app.raw()]
    return says('#panel').replace('\n', ' | ') + f' {levels}'


@step('a click takes no program from the front')
def _():
    was = other()
    if app.box():
        click(*app.center())
        need(until(lambda: not app.box()), 'the box closes')
    need(in_front() == was, f'a click on the robot: {in_front()}')
    click(*app.center())
    need(until(app.box), 'the box opens')
    need(in_front() == was, f'the box opens: {in_front()}')
    press(app, '#signin-other')
    need(in_front() == was, f'a click in the box: {in_front()}')
    need(until(lambda: says('#address') is not None and page('box', 'document.activeElement.id') == 'address'), 'the keys are in its address')
    need(page('box', 'document.hasFocus()'), 'it has the keys')
    press(app, '#signin-other')


@step('drag')
def _():
    a, b = app.center(), (500, 300)
    drag(a, b)
    c = app.center()
    need(abs(c[0] - b[0]) < 6 and abs(c[1] - b[1]) < 6, f'from {a} to {b}, it is at {c}')
    need(app.answers(), 'its main thread answers')
    need(saved()['places'], 'its place is kept')
    return f'{a} to {c}, {saved()["monitor"]}'


@step('a click beside the robot')
def _():
    r = app.robot()
    took = []
    for x, y in ((r.left + 3, r.top + 3), (r.right - 3, r.bottom - 3)):
        click(x, y)
        took.append(bool(until(app.box, 2)))
        if took[-1]:
            click(*app.center())
            need(until(lambda: not app.box()), 'it closes')
    return f'in its corners: {"taken" if any(took) else "goes through"}'


@step('right click')
def _():
    click(*app.center(), right=True)
    need(until(app.box), 'the box opens')
    need(until(lambda: 'Quit' in says('#menu')), 'on its menu')
    told = says('#menu').replace('\n', ' | ')
    key(ESCAPE)
    need(until(lambda: not says('#menu')), 'Escape closes the menu')
    press(app, '#close')
    click(*app.center(), flags=CTRL)
    need(until(lambda: 'Quit' in says('#menu')) and app.box(), 'a Control-click opens it too')
    key(ESCAPE)
    need(until(lambda: not says('#menu')), 'Escape closes that')
    return told


@step('wrong address')
def _():
    press(app, '#signin-other')
    press(app, '#address')
    write('http://127.0.0.1:1')
    key(ENTER)
    need(until(lambda: says('#signin-error'), 25), 'it says why not')
    return says('#signin-error')


LINES = 'x => x.innerText.split("\\n").map(y => y.trim()).filter(y => y).join("\\n")'  # WebKit has empty ones between them


def listed():
    return page('box', f'[...document.querySelectorAll("#todos li")].map({LINES})') or []


def greeted(name=', Sam'):
    part = lambda: 'morning' if 5 <= time.localtime().tm_hour < 12 else 'afternoon' if 12 <= time.localtime().tm_hour < 18 else 'evening'
    return says('#state') == f'Good {part()}{name}'


@step('sign in by address, with Command keys')
def _():
    press(app, '#address')
    key(A, CMD)
    run('pbcopy', input=f'http://127.0.0.1:{PORT}')
    key(V, CMD)
    need(until(lambda: page('box', 'document.getElementById("address").value') == f'http://127.0.0.1:{PORT}', 3), 'Command-A and Command-V')
    key(ENTER)
    need(until(lambda: says('#compose')), 'signed in')
    need(until(greeted), says('#state'))
    need(until(lambda: len(listed()) == 4), 'three to-dos and more')
    need(listed() == [title for _, title in TODOS[:3]] + ['1 more'] and says('#ready-name') == 'For you 4', f"{says('#ready-name')}: {listed()}")
    return says('#panel').replace('\n', ' | ')


@step('the menu says where')
def _():
    press(app, '#more')
    need(until(lambda: f'Signed in to 127.0.0.1:{PORT}' in says('#menu')), says('#menu'))
    need('Always' in says('#menu') and 'Never' in says('#menu') and 'Disturb' not in says('#menu'), says('#menu'))
    png('menu')
    key(ESCAPE)
    need(until(lambda: not says('#menu')), 'it closes')


def reopen():
    click(*app.center())
    click(*app.center())


@step('nothing for them')
def _():
    machine.todos = []
    reopen()
    need(until(lambda: says('#state') == 'Nothing needs you right now, Sam.', 12), says('#state'))
    png('nothing-for-them')
    machine.todos = list(TODOS)
    reopen()
    need(until(greeted, 12), says('#state'))


@step('add a to-do')
def _():
    press(app, '#text')
    write('Call the printer about the flyers')
    key(ENTER)
    need(until(lambda: len(listed()) == 4 and listed()[0] == 'Call the printer about the flyers\nJust added · Needs you'), str(listed()))
    need(not page('box', 'document.getElementById("text").value') and not says('#said'), 'ready for the next one')
    need(machine.actions[-1][:2] == ('card_new', {'text': 'Call the printer about the flyers'}), str(machine.actions))
    machine.todos = list(TODOS)
    press(app, '#close')
    need(until(lambda: not app.box()), 'the box closes')
    click(*app.center())
    need(until(lambda: len(listed()) == 4 and not says('#added')), 'the next time it is a row like any other')


@step('ask')
def _():
    press(app, '#kind-ask')
    write('When is lunch with Nora?')
    key(ENTER)
    need(until(lambda: '12:30' in says('#answer')), says('#answer'))
    need(machine.actions[-1][0] == 'search_ask', str(machine.actions))


def dot():
    return page('robot', '!document.getElementById("dot").hidden')


@step('Command W closes the box')
def _():
    need(app.box(), 'it is open')
    key(W, CMD)
    need(until(lambda: not app.box()), 'the box closes')
    need(app.pids() and app.robot(), 'the robot stays')
    need(not dot(), 'nothing is new since the box was open')


@step('the dot is what is new')
def _():
    since = time.time()
    machine.todos = list(TODOS) + [('aa05', 'Answer the caterer')]
    need(until(dot, 40), 'something new: the dot, with the box closed')
    took = time.time() - since
    png('the-dot')
    machine.todos = list(TODOS)
    need(until(lambda: not dot(), 40), 'it was handled elsewhere: no dot')
    return f'{took:.0f} s'


def hidden():
    r = app.robot()
    return r and r.height == 40 and r.bottom == work_area()[3]


def back():
    r = app.robot()
    return r and (r.left, r.top, r.height) == stood


def hide():
    global stood
    r = app.robot()
    stood = r.left, r.top, r.height
    click(*app.center(), right=True)
    need(until(lambda: 'Hide' in says('#menu')), 'the menu opens')
    press(app, '#menu-hide')
    need(until(hidden), f'it only looks over the bottom edge: {app.robot()}')


@step('hide says where it is')
def _():
    hide()
    need(until(lambda: 'bring it back' in says('#notice')), 'the box says how to bring it back')
    png('hidden-with-the-line')
    press(app, '#notice-ok')
    need(until(lambda: not app.box()), 'the box closes')
    need(hidden(), 'it is still there')


@step('a click brings it back')
def _():
    click(*app.center())
    need(until(back), 'it is where it stood')
    need(not app.box(), 'and no box opens')


@step('right click while hidden')
def _():
    hide()
    click(*app.center(), right=True)
    need(until(lambda: 'Show robot' in says('#menu')), 'the menu has Show robot')
    png('hidden-menu')
    press(app, '#menu-show')
    need(until(back), 'it is where it stood')


@step('hide and open it again from Finder')
def _():
    was = other()
    hide()
    run('open', sandbox)
    need(until(back), 'it is back')
    time.sleep(1.5)
    need(in_front() == was, 'the program in front stays there: ' + in_front())
    need(len(app.pids()) == 1, 'and the only one')


@step('the menu bar icon')
def _():
    told = tray_menu(app, 'Hide')
    need(until(hidden), 'Hide')
    tray_menu(app, 'Show robot')
    need(until(back), 'Show robot')
    was = other()
    tray_menu(app, 'Open')
    need(until(app.box), 'Open')
    need(in_front() == was, in_front())
    press(app, '#close')
    return told


def open_it():
    if not app.box():
        click(*app.center())
    need(until(app.box), 'the box opens')
    need(until(lambda: len(listed()) == 4), str(listed()))


def over(n, seconds=1.2):
    at = page('box', f'(() => {{ const e = document.querySelectorAll("#todos li")[{n}].getBoundingClientRect(); return [e.x + 60, e.y + e.height / 2] }})()')
    r = need_window(app.box())
    move(round(r.left + at[0]) - 4, round(r.top + at[1]))
    move(round(r.left + at[0]), round(r.top + at[1]))
    time.sleep(seconds)


def row(n):
    return page('box', f'(r => ({{names: [...r.querySelectorAll(".quick button")].map(b => b.title), shown: r.querySelector(".quick") ? getComputedStyle(r.querySelector(".quick")).opacity : "",'
                f' tip: r.querySelector(".name")?.title ?? null, text: ({LINES})(r) }}))(document.querySelectorAll("#todos li")[{n}])')


def quick(n, act):
    over(n, 0.3)
    press(app, f'#todos li:nth-child({n + 1}) [data-act={act}]')


@step('quick buttons')
def _():
    open_it()
    need(until(lambda: row(0)['names'] == ['Do it', 'Snooze', 'Mark done']), str(row(0)))
    move(40, 200)
    move(50, 200)
    need(until(lambda: row(0)['shown'] == '0', 3), str(row(0)))
    over(0)
    need(row(0)['shown'] == '1', str(row(0)))
    png('quick-buttons')


def decided():
    return [a[1] for a in machine.actions if a[0] == 'decide'][-1]


def picks():
    return page('box', '[...document.querySelectorAll(".choices button")].map(b => b.innerText)')


@step('snooze and undo')
def _():
    open_it()
    need(until(lambda: row(0)['names']), 'its buttons')
    quick(0, 'snooze2h')
    choices = [text for _, text in SNOOZE] + ['Choose date']
    need(until(lambda: picks() == choices), str(picks()))
    focused = lambda: page('box', 'document.activeElement.innerText || document.activeElement.ariaLabel')
    need(until(lambda: focused() == '2 hours'), focused())
    png('snooze-choices')
    key(ESCAPE)
    need(until(lambda: not picks()) and app.box(), 'Escape closes the choices only')
    quick(0, 'snooze2h')
    need(until(picks), 'they open again')
    key(DOWN)
    key(DOWN)
    need(until(lambda: focused() == choices[2]), focused())
    key(ENTER)
    need(until(lambda: row(0)['text'].startswith('Snoozed it · ')), str(listed()))
    png('snoozed')
    told, d = row(0)['text'], decided()
    need(d['choice'] == 'snooze' and d['snooze_option'] == '3d', str(d))
    press(app, '#todos li:first-child .link')
    need(until(lambda: listed()[0] == TODOS[0][1]), str(listed()))
    return told


@step('it says how Do it goes')
def _():
    need(until(lambda: row(0)['names'][:1] == ['Do it']), str(row(0)))
    quick(0, 'prepare')
    need(until(lambda: row(0)['text'] == TODOS[0][1] + '\nPreparing…'), row(0)['text'])
    png('being-prepared')
    for status, word in (({'preparation_status': 'working'}, 'Working…'), ({'status': 'prepared', 'preparation_status': 'done'}, 'Prepared')):
        machine.status['aa01'] = {'status': 'accepted', **status}
        need(until(lambda: row(0)['text'].endswith('\n' + word), 40), f"{word}: {row(0)['text']}")
    machine.status.clear()
    press(app, '#close')


def again():
    global machine
    was, machine = machine, Machine(PORT)
    machine.cookies = was.cookies


@step('refused, and not reachable')
def _():
    open_it()
    machine.no = 'Open the to-do to do this.'
    need(until(lambda: row(0)['names'][:1] == ['Do it']), 'its buttons')
    quick(0, 'prepare')
    need(until(lambda: says('#said') == machine.no), says('#said'))
    png('refused')
    machine.no = None
    machine.stop()
    try:
        if row(0)['names']:  # else it noticed by itself
            quick(0, 'prepare')
    except TypeError:
        pass  # it noticed meanwhile
    try:
        need(until(lambda: 'reach' in says('#state'), 40), says('#state'))
        time.sleep(1)
        png('cannot-reach')
        told = says('#state')
    finally:
        again()
    reopen()
    need(until(greeted, 25), says('#state'))
    press(app, '#close')
    return told


def carded(todo):
    need(until(app.card, 20), f'the to-do shows {says("#panel")}')
    need(until(lambda: says('h1', 'card') == 'To-do ' + todo), says('h1', 'card'))
    b, c = app.box(), app.card()
    need(b.left < c.left < c.right < b.right and b.top < c.top < c.bottom < b.bottom, f'within the box: {c} in {b}')


@step('a to-do in the box')
def _():
    was = other()
    open_it()
    machine.compact = True
    since = time.time()
    press(app, '#todos li:nth-child(2) .name')
    carded('aa02')
    took = time.time() - since
    need(says('#ipc', 'card') == 'refused', 'nothing of the app for it: ' + says('#ipc', 'card'))
    png('a-to-do-in-the-box')
    short = app.box().height
    press(app, '#long', 'card')
    need(until(lambda: app.box().height > short + 60), 'a longer one: the box grows with it')
    press(app, '#more', 'card')
    need(until(lambda: says('dialog', 'card')), 'a dialog of its own')
    key(ESCAPE)
    need(until(lambda: not says('dialog', 'card')) and app.card(), 'Escape closes that')
    time.sleep(1)
    need(app.card(), 'only that')
    press(app, 'a[href="/elsewhere"]', 'card')
    time.sleep(1)
    need(says('h1', 'card') == 'To-do aa02', 'it stays on its page')
    b = app.box()
    click((b.left + b.right) // 2, b.top + 30)
    time.sleep(0.5)
    need(app.card(), 'above the box, also after a click on that')
    need(app.raw()[0]['kCGWindowBounds']['Width'] < 350, 'in front of it')
    png('a-to-do-in-the-box-clicked-beside')
    press(app, 'h1', 'card')
    need(in_front() == was, in_front())
    key(ESCAPE)
    need(until(lambda: not app.card() and app.box()), 'Escape: back to the list')
    press(app, '#todos li:nth-child(1) .name')
    carded('aa01')
    press(app, '#done', 'card')
    need(until(lambda: not app.card(), 15), 'done there: back by itself')
    quick(0, 'snooze2h')
    need(until(picks), 'its choices')
    press(app, '.choices [data-until=date]')
    carded('aa01')
    press(app, '#card-close')
    need(until(lambda: not app.wide()), 'both go')
    machine.compact = False
    return f'{took:.1f} s'


# A screenshot: with macOS' permission and without

def allow(yes):
    """What the person said in System Settings, written where macOS keeps it."""
    db = '/Library/Application Support/com.apple.TCC/TCC.db'
    run('sudo', 'sqlite3', db, f"delete from access where service='kTCCServiceScreenCapture' and client='{ID}'")
    if yes is not None:
        told = run('sudo', 'sqlite3', db, 'insert into access (service, client, client_type, auth_value, auth_reason, auth_version, indirect_object_identifier_type, indirect_object_identifier, flags) '
                   f"values ('kTCCServiceScreenCapture', '{ID}', 0, {2 if yes else 0}, 4, 1, 0, 'UNUSED', 0)")
        need(told.returncode == 0, told.stderr)
    run('sudo', 'pkill', '-x', 'tccd')
    time.sleep(1)


def picker_alert():
    """macOS asks again, now and then, whether it may go on taking them."""
    for owner in ('UserNotificationCenter', 'universalAccessAuthWarn', 'CoreServicesUIAgent'):
        told = run('osascript', '-e', f'tell application "System Events" to tell process "{owner}" to get name of buttons of window 1').stdout.strip()
        if 'Allow' in told:
            png('macos-asks-again')
            run('osascript', '-e', f'tell application "System Events" to tell process "{owner}" to click button "Allow" of window 1')
            return f'{owner}: {told}'
    return ''


def shot():
    if page('box', 'document.querySelector("#plus").hidden'):
        press(app, '#kind-todo')
    until(lambda: not page('box', 'document.querySelector("#plus").hidden'))
    press(app, '#plus')
    need(until(lambda: says('#add-shot')), 'the menu')
    press(app, '#add-shot')


@step('a screenshot macOS was not asked for yet')
def _():
    open_it()
    shot()
    need(until(lambda: 'System Settings' in says('#said'), 15), 'the box says where to allow it: ' + says('#said'))
    time.sleep(3)
    png('macos-asks')
    asked = [x.get('kCGWindowOwnerName') for x in all_windows() if x.get('kCGWindowName') == 'Screen Recording' or x['kCGWindowBounds']['Width'] == 420]
    for owner in ('universalAccessAuthWarn', 'UserNotificationCenter'):
        run('osascript', '-e', f'tell application "System Events" to tell process "{owner}" to click button "Deny" of window 1')
    need(not page('box', 'document.querySelector("#files img")') and app.box(), 'the box stays')
    key(ESCAPE)
    return f"{says('#said')} {asked}"


def restarted():
    app.again('--quit')
    need(app.ended(), 'the process is gone')
    made = App(sandbox)
    need(until(made.robot, 30), 'the robot shows')
    time.sleep(3)
    return made


@step('a screenshot that is refused')
def _():
    global app
    allow(False)
    app = restarted()
    open_it()
    shot()
    need(until(lambda: 'System Settings' in says('#said'), 15), says('#said'))
    return says('#said')


@step('a screenshot')
def _():
    global app
    allow(True)
    app = restarted()
    open_it()
    shot()
    need(until(lambda: not app.windows(), 8), 'the robot and its box are away')
    time.sleep(2)
    png('picking')
    if told := picker_alert():
        time.sleep(1)
    drag((300, 300), (520, 420))
    need(until(app.box, 30), 'the box is back')
    need(until(lambda: 'Screenshot.png' in says('#files')), says('#files') + ' | ' + says('#said'))
    size = page('box', '(i => [i.naturalWidth, i.naturalHeight])(document.querySelector("#files img"))')
    need(size[0] >= 200, str(size))
    need(until(lambda: machine.actions[-1][0] == 'chat_upload'), str(machine.actions[-1][0]))
    need(base64.b64decode(machine.actions[-1][1]['data'])[:4] == b'\x89PNG', 'a PNG')
    png('a-screenshot')
    press(app, '#files button')
    need(until(lambda: machine.actions[-1][0] == 'chat_file_remove'), str(machine.actions[-1]))
    shot()
    need(until(lambda: not app.windows(), 8), 'away again')
    time.sleep(2)
    key(ESCAPE)
    need(until(app.box, 20), 'Escape: the box is back')
    time.sleep(1)
    need(not says('#files') and not says('#said'), 'with nothing: ' + says('#said'))
    return f'{size} {told} {picker_alert()}'


@step('add a file')
def _():
    was = other()
    open_it()
    press(app, '#plus')
    need(until(lambda: says('#add-file')), 'the menu ' + says('#adds'))
    press(app, '#add-file')
    chooses = until(lambda: not in_front().startswith(was), 60)
    time.sleep(3)
    png('choosing-a-file')
    need(chooses, 'it has the keys')
    key(5, CMD | (1 << 17))  # Command-Shift-G: a path
    time.sleep(1.5)
    write(str(out / 'note.txt'))
    time.sleep(1)
    key(ENTER)
    time.sleep(1.5)
    png('choosing-a-file-found')
    key(ENTER)
    need(until(lambda: 'note.txt' in says('#files'), 10), says('#files') + ' | ' + says('#said'))
    need(app.box(), 'the box stays')
    png('a-file')
    press(app, '#files button')
    press(app, '#close')
    need(until(lambda: in_front() == was, 5), 'what was in front is again: ' + in_front())


@step('drop anything on it')
def _():
    if app.box():
        press(app, '#close')
    source, one, two = out.parent / 'source', out / 'notes.txt', out / 'plan & b.txt'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-o', str(source), str(pathlib.Path(__file__).with_name('source.m')))
    need(made.returncode == 0, made.stderr[-800:])
    for f in (one, two):
        f.write_text('made up')
    was = other()
    runs = subprocess.Popen([str(source), str(one), str(two)])
    try:
        time.sleep(3)
        from_ = lambda n: (40 + 130 * n + 60, 150)
        value = lambda: page('box', 'document.getElementById("text").value')

        def empty():
            press(app, '#text')
            key(A, CMD)
            key(BACK)
            press(app, '#close')
        before = len(machine.actions)
        drag(from_(1), app.center())
        need(until(app.box), 'the box opens')
        need(until(lambda: value() == 'Ask Dana <b>about</b> the pilot'), str(value()))
        need(until(lambda: in_front() == was, 3), 'what was in front is again: ' + in_front())
        need(until(lambda: page('box', 'document.activeElement.id') == 'text' and page('box', 'document.hasFocus()'), 3), 'ready to go on')
        key(V)
        need(until(lambda: value().endswith('pilotv'), 3), 'the keys come in it ' + value())
        key(BACK)
        png('dropped-text')
        drag(from_(2), app.center())
        need(until(lambda: 'https://example.com/pilot?x=1' in value().split('\n')), str(value()))
        need(len(machine.actions) == before, f'nothing is sent: {machine.actions[before:]}')
        b = app.box()
        drag(from_(0), ((b.left + b.right) // 2, (b.top + b.bottom) // 2))
        need(until(lambda: 'notes.txt' in says('#files') and 'plan & b.txt' in says('#files')), says('#files') + ' | ' + says('#said'))
        need(until(lambda: len(machine.actions) == before + 2), str(machine.actions[before:]))
        need({n for n, *_ in machine.actions[before:]} == {'chat_upload'}, 'the files are attached, as with +')
        png('dropped-files')
        for _ in range(2):
            press(app, '#files button')
        empty()
        drag(from_(0), app.center())
        need(until(lambda: 'notes.txt' in says('#files')), 'files on the robot ' + says('#files') + ' | ' + says('#said'))
        for _ in range(2):
            press(app, '#files button')
        press(app, '#close')
        hide()
        time.sleep(1)
        told = ''
        for place in (28, 16, 8):  # points below its top: the Dock takes what is dropped close above it
            r = app.robot()
            drag(from_(1), ((r.left + r.right) // 2, r.top + place))
            if until(app.box, 4):
                told = f'on a hidden one {place} of {r.height} points below its top'
                break
        need(app.box() and until(back), 'a hidden one comes back with it')
        need(until(lambda: value().startswith('Ask Dana')), str(value()))
        empty()
        return told
    finally:
        runs.kill()


@step('toggle from a second start')
def _():
    if app.box():
        press(app, '#close')
        need(until(lambda: not app.box()), 'it was open')
    app.again('--toggle')
    need(until(app.box), 'the box opens')
    app.again('--toggle')
    need(until(lambda: not app.box()), 'the box closes')


@step('signed out elsewhere')
def _():
    machine.refuse = True
    reopen()
    if not app.box():
        click(*app.center())
    need(until(lambda: says('#signin') and says('#state'), 25), 'it offers the sign-in')
    told = says('#panel').replace('\n', ' | ')
    machine.refuse = False
    reopen()
    need(until(lambda: says('#compose'), 25), 'and is back')
    return told


@step('sign out')
def _():
    press(app, '#more')
    press(app, '#menu-signout')
    time.sleep(1)
    if not app.box():
        click(*app.center())
    need(until(lambda: says('#state') == 'Not signed in'), says('#state'))


def script(text, *told):
    return run('osascript', '-l', 'JavaScript', '-e', "ObjC.import('AppKit'); function run(argv) { " + text + ' }', *told).stdout.strip()


def goes_to(link):
    return pathlib.Path(script('return $.NSWorkspace.sharedWorkspace.URLForApplicationToOpenURL($.NSURL.URLWithString(argv[0])).path.js', link)).resolve()


def made_up_app(lsregister):
    """Another app that names the same links, as the phone's app on a Mac does, and has them."""
    there = out.parent / 'Made up.app'
    (there / 'Contents/MacOS').mkdir(parents=True, exist_ok=True)
    told = plistlib.loads((pathlib.Path(sandbox) / 'Contents/Info.plist').read_bytes())
    told.update(CFBundleIdentifier='computer.themachine.app', CFBundleName='Made up', CFBundleDisplayName='Made up', CFBundleExecutable='made-up')
    (there / 'Contents/Info.plist').write_bytes(plistlib.dumps(told))
    program = there / 'Contents/MacOS/made-up'
    program.write_text('#!/bin/sh\nsleep 5\n')
    program.chmod(0o755)
    run(lsregister, '-f', str(there))
    script('const done = $.NSWorkspace.sharedWorkspace.setDefaultApplicationAtURLToOpenURLsWithSchemeCompletionHandler($.NSURL.fileURLWithPath(argv[0]), argv[1], null);'
           ' $.NSRunLoop.currentRunLoop.runUntilDate($.NSDate.dateWithTimeIntervalSinceNow(2))', str(there), 'computer.themachine.app')
    return there.resolve()


@step('account sign-in')
def _():
    if says('#signin-other') != 'Self-hosted?':
        press(app, '#signin-other')
    lsregister = '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister'
    run(lsregister, '-u', people)  # there are two here, and only one on somebody's Mac
    run(lsregister, '-f', sandbox)
    phone, link = made_up_app(lsregister), 'computer.themachine.app://'
    need(until(lambda: goes_to(link) == phone, 10), f'the other app has the links: {goes_to(link)}')
    press(app, '#signin-go')
    need(until(lambda: machine.links, 60), 'the browser opens the account')
    time.sleep(2)
    png('account-in-the-browser')
    was = in_front()
    need(goes_to(link) == pathlib.Path(sandbox).resolve(), f'the links come here now: {goes_to(link)}')
    need(run('open', machine.links[-1]).returncode == 0, 'macOS knows whose link it is')  # as the browser does
    need(until(lambda: says('#compose'), 25), f'signed in {app.pid} {app.pids()} {in_front()} {says("#panel")}')
    need(machine.cookies and saved()['cookie'] in machine.cookies, 'with its session')
    need(oct((LIBRARY / 'Application Support' / ID / 'app.json').stat().st_mode)[-3:] == '600', 'in a file of its own')
    need(len(app.pids()) == 1, 'one program')
    need(until(lambda: goes_to(link) == phone, 5), f'and then go where they went: {goes_to(link)}')
    run(lsregister, '-u', str(phone))
    shutil.rmtree(phone)
    run('osascript', '-e', 'tell application "Safari" to quit')
    return says('#state') + f' | the browser was {was}'


# What it opens on the dashboard: in the installed app, or else in the browser

HERE = f'http://127.0.0.1:{PORT}/'


def opens(press_it, at, seconds=40):
    open_it()
    del machine.seen[:]
    press_it()
    seen = until(lambda: next((s for s in machine.seen if s.get('at', '') == at), None), seconds)
    need(seen, f'opened {machine.seen}, in front {in_front()}')
    need(until(lambda: not app.box()), 'the box closes')
    return seen


def todo(n):
    return lambda: press(app, f'#todos li:nth-child({n}) button')


@step('a to-do without an app')
def _():
    seen = opens(todo(1), '#card=aa01')
    time.sleep(1)
    need(app.robot(), 'the robot stays')
    return f'{seen}, in front {in_front()}'


run('osascript', '-e', 'tell application "Safari" to quit')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def shims():
    return [p for p in (pathlib.Path.home() / 'Applications').rglob('*.app')] if (pathlib.Path.home() / 'Applications').exists() else []


@step('a to-do in the app Chrome installed')
def _():
    if not pathlib.Path(CHROME).exists():
        return 'NOT TESTED: no Chrome here'
    subprocess.run(['sudo', 'mkdir', '-p', '/Library/Managed Preferences'])
    policy = out / 'com.google.Chrome.plist'
    policy.write_bytes(plistlib.dumps({'WebAppInstallForceList': [{'url': HERE, 'default_launch_container': 'window'}], 'BrowserSignin': 0}))
    run('sudo', 'cp', str(policy), '/Library/Managed Preferences/com.google.Chrome.plist')
    run('sudo', 'mkdir', '-p', f'/Library/Managed Preferences/{os.environ["USER"]}')
    run('sudo', 'cp', str(policy), f'/Library/Managed Preferences/{os.environ["USER"]}/com.google.Chrome.plist')
    policy.unlink()
    run('sudo', 'killall', 'cfprefsd')
    time.sleep(2)
    chrome = subprocess.Popen([CHROME, '--no-first-run', '--no-default-browser-check', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not until(shims, 60, 1):
            return 'NOT TESTED: Chrome installed no app here'
        time.sleep(5)
        info = plistlib.loads((shims()[0] / 'Contents/Info.plist').read_bytes())
        told = {k: v for k, v in info.items() if k.startswith('CrAppMode') or k.startswith('CrBundle') or k == 'CFBundleIdentifier'}
        png('chrome-app-installed')
        seen = opens(todo(2), '#card=aa02')
        need(seen.get('app') == 'yes', f'in the app: {machine.seen} {shims()}')
        need(until(lambda: info['CFBundleIdentifier'] == in_front(), 40), f'{info["CFBundleIdentifier"]} {in_front()}')
        need(until(lambda: not app.robot(), 8), 'the robot goes while the app is in front')
        png('the-app-in-front')
        was = other()
        need(until(app.robot, 8), 'another program in front: it is back')
        need(in_front() == was, 'and takes nothing from the front: ' + in_front())
        seen2 = opens(todo(1), '#card=aa01')
        need(seen2['me'] == seen['me'], 'the same window')
        need(until(lambda: not app.robot(), 8), 'away again')
        click(*[(screens()[0]['whole'][2]) // 2, 400])
        need(not app.robot(), 'a click in the app leaves it away')
        app.again('--toggle')
        need(until(app.box), 'a key still opens the box')
        press(app, '#text')
        write('Half a to-do')
        time.sleep(2)
        need(app.robot() and app.box(), 'it stays while the box is open')
        press(app, '#close')
        other()
        need(until(app.robot, 8), 'the robot is back')
        return str(told)
    finally:
        chrome.terminate()
        run('osascript', '-e', 'tell application "Google Chrome" to quit')
        run('pkill', '-f', 'Google Chrome')
        time.sleep(2)


# Other Spaces, screens and looks

@step('beside a full-screen app')
def _():
    was = other('Safari')
    key(F, CMD | CTRL)
    time.sleep(4)
    png('full-screen')
    wide = [Rect(x['kCGWindowBounds']) for x in all_windows() if x['kCGWindowOwnerName'] == 'Safari' and x['kCGWindowLayer'] == 0]
    try:
        need(wide and wide[0].width == screens()[0]['whole'][2], f'Safari is full screen: {wide}')
        need(app.robot(), 'the robot is there')
        click(*app.center())
        need(until(app.box), 'the box opens there')
        need(until(lambda: page('box', 'document.hasFocus()')), 'with the keys')
        png('full-screen-box')
        need(in_front() == was, in_front())
        click(*app.center())
        need(until(lambda: machine.desks[-1][1] == '0', 10), 'and it says it does not speak now')
    finally:
        key(F, CMD | CTRL)
        time.sleep(3)
        run('osascript', '-e', 'tell application "Safari" to quit')
    need(until(lambda: machine.desks[-1][1] == '1', 45), 'it speaks again')


@step('dark mode')
def _():
    dark = lambda on: run('osascript', '-e', f'tell application "System Events" to tell appearance preferences to set dark mode to {on}')
    told = dark('true')
    time.sleep(2)
    open_it()
    over(0)
    need(told.returncode == 0 and page('box', 'matchMedia("(prefers-color-scheme: dark)").matches'), 'the box is dark ' + told.stderr)
    png('dark')
    dark('false')
    time.sleep(1)
    press(app, '#close')


@step('the Dock elsewhere')
def _():
    r, area = app.robot(), work_area()
    gap = area[2] - r.right, area[3] - r.bottom
    drag(app.center(), (area[2] - 200, area[3] - 200))
    r = app.robot()
    gap = area[2] - r.right, area[3] - r.bottom
    told = [gap]
    try:
        for side in ('right', 'left', 'bottom'):
            run('defaults', 'write', 'com.apple.dock', 'orientation', side)
            run('killall', 'Dock')
            time.sleep(5)
            fits = lambda: (r := app.robot()) and (work_area()[2] - r.right, work_area()[3] - r.bottom) == gap
            need(until(fits, 12), f'{side}: {app.robot()} in {work_area()}, it was {gap} from the corner')
            told.append((side, work_area()))
    finally:
        run('defaults', 'write', 'com.apple.dock', 'orientation', 'bottom')
        run('killall', 'Dock')
        time.sleep(4)
    return str(told)


@step('a second, sharper screen')
def _():
    maker = out.parent / 'made-up-screen'
    made = run('clang', '-fobjc-arc', '-framework', 'AppKit', '-framework', 'CoreGraphics', '-Wl,-U,_OBJC_CLASS_$_CGVirtualDisplay', '-o', str(maker), str(pathlib.Path(__file__).with_name('screen.m')))
    need(made.returncode == 0, made.stderr[-800:])
    second = subprocess.Popen([str(maker)], stdout=subprocess.PIPE, text=True)
    try:
        if not until(lambda: len(screens()) == 2, 15):
            return 'NOT TESTED: this Mac takes no made-up screen'
        moves = []
        for _ in range(8):
            moves.append((app.center(), [x['whole'] for x in screens()]))
            time.sleep(0.5)
        s = screens()[1]
        a, b = app.center(), ((s['free'][0] + s['free'][2]) // 2, (s['free'][1] + s['free'][3]) // 2)
        drag(a, b, 60)
        c = app.center()
        need(abs(c[0] - b[0]) < 6 and abs(c[1] - b[1]) < 6, f'dragged from {a} to {b} on {s}, it is at {c}; {moves}')
        need(page('robot', 'devicePixelRatio') == s['scale'], f"sharp: {page('robot', 'devicePixelRatio')}")
        need(app.robot().width == 88, str(app.robot()))
        click(*c)
        need(until(app.box), 'the box opens there')
        r = app.box()
        need(s['whole'][0] <= r.left and r.right <= s['whole'][2] + 14, f'on that screen: {r}')
        open_it()
        over(0)
        png('second-screen')
        press(app, '#close')
        told = f'{s}, dragged to {c}, saved as {saved()["monitor"]}'
    finally:
        second.kill()
    need(until(lambda: len(screens()) == 1, 15), 'the screen is gone')
    need(until(lambda: (r := app.robot()) and r.right <= screens()[0]['whole'][2] and r.bottom <= screens()[0]['whole'][3], 10), f'back on the one that is left: {app.robot()}')
    drag(app.center(), (screens()[0]['free'][2] - 100, screens()[0]['free'][3] - 100))
    return told


# It speaks up

def comes(todo):
    if app.box():
        press(app, '#close')
    need(until(lambda: not app.wide(), 20), 'nothing is there')
    machine.notices = [{'key': f'{time.time_ns():x}', 'id': todo, 'kind': 'todo', 'snooze': SNOOZE}]
    need(until(app.bubble, 45, 0.05), f'the bubble shows {machine.desks[-2:]}')
    need(until(lambda: says('#title', 'bubble')), 'with its words')


def away():
    move(60, 500)


@step('it speaks up')
def _():
    machine.todos = list(TODOS)
    away()
    was = other()
    comes('aa02')
    came = time.time()
    png('it-speaks-up')
    need(in_front() == was, 'the keys stay where they were: ' + in_front())
    need(says('#title', 'bubble') == TODOS[1][1], says('#panel', 'bubble'))
    need(until(lambda: not app.bubble(), 20, 0.05), 'it goes')
    stayed = time.time() - came
    need(10 < stayed < 16, f'after about 12 s: {stayed:.1f}')
    comes('aa03')
    b = app.bubble()
    move((b.left + b.right) // 2 - 5, (b.top + b.bottom) // 2)
    move((b.left + b.right) // 2, (b.top + b.bottom) // 2)
    time.sleep(14)
    need(app.bubble(), 'it stays under the pointer')
    away()
    move(62, 502)
    need(until(lambda: not app.bubble(), 20), 'and goes after')
    comes('aa04')
    press(app, '#buttons [data-act^=snooze]', 'bubble')
    need(until(lambda: says('#choices', 'bubble')), 'the choices')
    png('it-speaks-up-snooze')
    press(app, '#choices [data-until="3d"]', 'bubble')
    need(until(lambda: says('#said', 'bubble').startswith('Snoozed it · ')), says('#panel', 'bubble'))
    press(app, '#said .link', 'bubble')
    need(until(lambda: any(x[0] == 'aa04' for x in machine.todos)), 'it is back')
    need(in_front() == was, in_front())
    away()
    need(until(lambda: not app.bubble(), 15), 'it goes')
    return f'{stayed:.1f} s'


@step('a meeting that starts soon')
def _():
    at = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 600))
    meets = {'id': 'aa02', 'event': 7, 'at': at, 'who': 'Dana', 'others': 2, 'join': None}
    said = lambda: [t for t in page('bubble', '[...document.querySelectorAll("#buttons button")].map(b => b.innerText)')]
    for join, line in (('https://zoom.us.example.com/j/1', 'Meeting'), ('https://zoom.us/j/1', 'Call')):
        machine.meeting = {**meets, 'event': len(line), 'join': join}
        need(until(app.bubble, 45, 0.05), 'the bubble shows')
        need(until(lambda: says('#title', 'bubble') in [f'{line} with Dana and 2 others in {m} min' for m in (8, 9, 10)]), says('#panel', 'bubble'))
        need(said() == ['Open brief', *(['Join'] if line == 'Call' else [])], str(said()))
        png(f'a-meeting-{line.lower()}')
        need(until(lambda: not app.bubble(), 20), 'it goes')
    machine.meeting = None


@step('Command Q quits')
def _():
    open_it()
    press(app, '#panel h1')
    key(Q, CMD)
    need(app.ended(), 'the process is gone')


was = other()
app = App(sandbox)


@step('next start')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(4)
    need(not app.box(), 'signed in: the box waits for a click')
    need(in_front() == was, f'and takes nothing from the front: {in_front()}')
    write('x')  # into the program in front
    need(not says('#signin'), 'signed in')
    need(app.again() == 0 and len(app.pids()) == 1, 'a second start ends')
    return in_front()


@step('quit from the menu bar')
def _():
    tray_menu(app, 'Quit')
    need(app.ended(), 'the process is gone')


app = App(sandbox)


@step('quit from the menu')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(2)
    click(*app.center(), right=True)
    need(until(lambda: 'Quit' in says('#menu')), 'the menu opens')
    press(app, '#menu-quit')
    need(app.ended(), 'the process is gone')


app = App(sandbox)


@step('quit from a second start while it is stuck')
def _():
    need(until(app.robot, 30), 'the robot shows')
    time.sleep(2)
    app.again('--hang')
    time.sleep(1)
    need(not app.answers(), 'its main thread is stuck')
    since = time.time()
    app.again('--quit')
    need(app.ended(), 'the process is gone')
    return f'gone after {time.time() - since:.1f} s'


app.kill()


@step('nothing is left')
def _():
    need(until(lambda: not app.pids(), 5), 'no process')
    sent = {a for a, _, _ in machine.actions}
    need(sent <= {'card_new', 'search_ask', 'decide', 'chat_upload', 'chat_file_remove'}, str(sent))
    crashes = [p.name for p in (LIBRARY / 'Logs/DiagnosticReports').glob(NAME + '*')]
    need(not crashes, f'no crash reports: {crashes}')
    return [str(p) for p in LIBRARY.glob(f'*/{ID}*')]


finish()

"""Windows' Text size (Settings, Accessibility) and its scale: every window is as wide as its page, all of it on the screen, and a
click lands on what is drawn there. For CI's own throwaway computer (desktop.yml): it changes both, and the resolution.

  python smoke/text.py <sandbox build> - <folder for the pictures>
"""
import ctypes
import json
import os
import pathlib
import subprocess
import time
import winreg
from ctypes import wintypes as w

import on_windows as on
import windows_tools
from on_windows import App, ID, PORT, click, finish, fresh, need, page, png, resolution, sandbox, step, until, user, work_area
from standin import SNOOZE, Machine, TODOS

WIDE = {'robot': 88, 'box': 368, 'card': 336, 'bubble': 328, 'settings': 420}
PLACE, LAYERS = r'Software\Microsoft\Accessibility', r'Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers'
program = str(pathlib.Path(sandbox).resolve())
machine = Machine(PORT)
machine.window = machine.compact = True
app, size, zoom, flag = None, 100, 100, None


def text(percent):
    """As Settings leaves it; the app and WebView2 ask Windows for it."""
    global size
    size = percent
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, PLACE) as key:
        winreg.SetValueEx(key, 'TextScaleFactor', 0, winreg.REG_DWORD, percent)
    user.SendMessageTimeoutW(0xFFFF, 0x1A, 0, 0, 2, 2000, None)
    time.sleep(1)


def told_by_windows():
    ask = '[void][Windows.UI.ViewManagement.UISettings,Windows.UI.ViewManagement,ContentType=WindowsRuntime];[Windows.UI.ViewManagement.UISettings]::new().TextScaleFactor'
    return subprocess.run(['powershell', '-NoProfile', '-Command', ask], capture_output=True, text=True).stdout.strip()


def scale(percent):
    global zoom
    if percent != zoom and not windows_tools.scale(percent):
        return False
    zoom = percent
    return True


def said(label, script):
    try:
        return page(label, script)
    except OSError:
        return None  # it is only starting


def its(label):
    """What a page says of its size, and of what has to be in it."""
    inside = {'robot': ['#face'], 'box': ['#panel', '#close', '#more'], 'card': ['body'], 'bubble': ['#panel', '#close'], 'settings': ['#panel', '#login']}.get(label, [])
    return said(label, '({w: innerWidth, h: innerHeight, dpr: devicePixelRatio, out: ' + json.dumps(inside) + '.filter(s => { const r = (document.querySelector(s) || document.body).getBoundingClientRect(); '
                'return r.width && s != "body" && (r.left < -1 || r.top < -1 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) })})')


def window(label):
    """Its window's place and size inside, in real pixels."""
    if label in ('app', 'settings'):
        r = app.window() if label == 'app' else app.settings()
        hwnd = r and r.hwnd
    else:
        dpr, hwnd = (its(label) or {}).get('dpr', 1), None
        for handle, r in app.all(True):
            own = user.GetDpiForWindow(handle) / 96
            if any(abs((r.right - r.left) / f - WIDE[label]) < 1 for f in (own, own * size / 100, dpr, dpr * zoom / 100, zoom / 100, zoom * size / 10000)):
                hwnd = handle
                break
    if not hwnd:
        return None
    r, at = w.RECT(), w.POINT(0, 0)
    user.GetClientRect(w.HWND(hwnd), ctypes.byref(r))
    user.ClientToScreen(hwnd, ctypes.byref(at))
    return hwnd, at.x, at.y, r.right, r.bottom


def right(label, wrong):
    """Its page fills its window, no more and no less, and all of it is on the screen."""
    need(until(lambda: window(label), 10), f'the {label} is there')
    # A program that Windows takes for an older one is drawn at 100%, and stretched
    by = lambda p, f: zoom / 100 if abs(p['w'] * p['dpr'] - f[3]) > p['dpr'] + 1 and flag == '~ DPIUNAWARE' else 1
    fits = lambda: (p := its(label)) and (f := window(label)) and abs(p['w'] * p['dpr'] * by(p, f) - f[3]) <= p['dpr'] + 1 and abs(p['h'] * p['dpr'] * by(p, f) - f[4]) <= p['dpr'] + 1 and not p['out'] and abs(p['w'] - WIDE.get(label, p['w'])) <= 1
    ok = until(fits, 6)
    p, (_, x, y, wide, tall), area = its(label), window(label), work_area()
    told = f"{label}: {wide}x{tall} at {x},{y}; its page {p['w']}x{p['h']} at {p['dpr']:.3f}"
    print(f'  {told}', flush=True)
    if not ok:
        wrong.append(f"{told}, cut off: {p['out']}")
    edge = 16 * p['dpr']
    if x < area.left - edge or y < area.top - edge or x + wide > area.right + edge or y + tall > area.bottom + edge:
        wrong.append(f'{told}, not all on the screen {area.right}x{area.bottom}')
    return wide


def tap(selector, label):
    """A real click where it is drawn."""
    at = page(label, f'(() => {{ const r = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [(r.x + r.width / 2) * devicePixelRatio, (r.y + r.height / 2) * devicePixelRatio] }})()')
    _, x, y, wide, tall = window(label)
    need(at[0] < wide and at[1] < tall, f'{selector} is drawn at {at}, outside the window, {wide}x{tall}')
    by = 1
    if its(label)['dpr'] and abs(its(label)['w'] * its(label)['dpr'] - wide) > 2:
        by = wide / (its(label)['w'] * its(label)['dpr'])  # Windows stretches a program it takes for an older one
    click(round(x + at[0] * by), round(y + at[1] * by))


def robot():
    _, x, y, wide, tall = window('robot')
    click(x + wide // 2, y + tall // 2)


def box():
    """Open, with its list. Each part on its own, so a failure says which one was missing."""
    if not window('box'):
        robot()
    if not until(lambda: window('box'), 12):
        mine = [(r.right - r.left, user.GetDpiForWindow(h) / 96) for h, r in app.all(True)]
        need(False, f'a click on the robot opens the box: its windows (width, scale) {mine}, the box page {its("box")}')
    rows = lambda: page('box', 'document.querySelectorAll("#todos li").length') or 0
    if not until(lambda: rows() > 1, 12):
        shown = said('box', '["signin", "notice", "compose"].filter(s => !document.getElementById(s).hidden)')
        need(False, f'the box with its list: {rows()} rows, it shows {shown}, the Machine was asked {len(machine.desks)} times')
    time.sleep(0.6)


def start():
    global app
    fresh()
    folder = pathlib.Path(os.environ['APPDATA'], ID)
    folder.mkdir(parents=True)
    (folder / 'app.json').write_text(json.dumps({'machine': machine.at + '/'}))
    machine.todos, machine.notices = list(TODOS), []
    before = len(machine.desks)
    app = App(program, window=False)
    need(until(lambda: window('robot'), 40), 'the robot')
    # Its first look: until the Machine has said what waits, the box has nothing to list
    need(until(lambda: len(machine.desks) > before, 40), 'it asks the Machine what waits')
    time.sleep(2)


def whole(name):
    """Each window, and a click in each."""
    wrong, wide = [], {}

    def part(f):
        try:
            f()
        except Exception as e:  # noqa: BLE001 (the other windows still tell something)
            wrong.append(f'{type(e).__name__}: {e}')

    def list_():
        wide['robot'] = right('robot', wrong)
        box()
        wide['box'] = right('box', wrong)
        png(f'{name}-box')
        tap('#todos li:nth-child(2) .name', 'box')
        need(until(lambda: window('card'), 15), 'a click on a row opens it')
        time.sleep(1)
        right('card', wrong)
        right('box', wrong)
        png(f'{name}-card')
        tap('#card-back', 'box')
        need(until(lambda: not window('card'), 8), 'a click goes back')

    def menu():
        box()
        tap('#more', 'box')
        need(until(lambda: page('box', '!document.querySelector("#menu").hidden'), 5), 'a click opens the menu')
        time.sleep(0.6)
        right('box', wrong)
        png(f'{name}-menu')
        tap('#menu-settings', 'box')
        need(until(app.settings, 10), 'a click opens Settings')
        time.sleep(1.5)
        right('settings', wrong)
        png(f'{name}-settings')
        for on_ in (True, False):
            tap('#login', 'settings')
            need(until(lambda on_=on_: page('settings', 'document.querySelector("#login").checked') is on_, 6), f'a click on a switch: {on_}')
        user.PostMessageW(w.HWND(app.settings().hwnd), 0x10, 0, 0)

    def bubble():
        if window('box'):
            robot()
        on.other()
        machine.notices = [{'key': f'{time.time_ns():x}', 'id': 'aa02', 'kind': 'todo', 'snooze': SNOOZE}]
        need(until(lambda: window('bubble'), 60), 'its bubble')
        time.sleep(1.5)
        right('bubble', wrong)
        png(f'{name}-bubble')
        tap('#buttons [data-act^=snooze]', 'bubble')
        need(until(lambda: page('bubble', '!document.querySelector("#choices").hidden'), 6), 'a click on Snooze')
        time.sleep(0.6)
        right('bubble', wrong)
        tap('#close', 'bubble')
        need(until(lambda: not window('bubble'), 8), 'a click closes it')

    def dashboard():
        box()
        tap('#more', 'box')
        time.sleep(0.8)
        tap('#menu-dashboard', 'box')
        need(until(app.window, 15), 'its window')
        need(until(lambda: page('app', '!!document.querySelector("#field")'), 15), 'its page')
        time.sleep(1)
        right('app', wrong)
        png(f'{name}-dashboard')
        tap('#field', 'app')
        need(until(lambda: page('app', 'document.activeElement.id') == 'field', 5), 'a click in it')

    for f in (list_, menu, bubble, dashboard):
        part(f)
    print(f'{name}: Windows says {told_by_windows()}', flush=True)
    need(not wrong, '; '.join(wrong))
    return f'text {told_by_windows()}; {wide}'


def case(zoomed, percent, screen=(1920, 1080), runs=None):
    name = f'scale {zoomed} text {percent}' + (f' at {screen[0]}' if screen[0] != 1920 else '') + (f' {runs.split()[-1]}' if runs else '')

    @step(name)
    def _():
        global flag
        flag = runs
        if not resolution(*screen):
            return f'NOT TESTED: this computer has no {screen}'
        if not scale(zoomed):
            return f'NOT TESTED: this screen has no {zoomed}%'
        text(percent)
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, LAYERS) as key:
            if flag:
                winreg.SetValueEx(key, program, 0, winreg.REG_SZ, flag)
        try:
            start()
            return whole(name.replace(' ', '-'))
        finally:
            app.kill()
            time.sleep(1)
            if flag:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, LAYERS, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, program)


ALL = [(100, 100), (100, 150), (100, 225), (150, 150), (150, 100), (125, 200), (175, 150), (100, 225, (1280, 720)), (150, 150, (1920, 1080), '~ HIGHDPIAWARE'), (150, 150, (1920, 1080), '~ DPIUNAWARE'),
       (150, 100, (1920, 1080), '~ DPIUNAWARE')]
for zoomed, percent, *more in ALL if 'TEXT_ALL' in os.environ else [x for x in ALL if x in ((100, 150), (150, 150), (100, 225, (1280, 720)))]:
    case(zoomed, percent, *more)


@step('the text size changes while it runs')
def _():
    global flag
    flag = None
    resolution(1920, 1080)
    scale(100)
    text(100)
    start()
    wide, wrong = [], []
    for percent in (100, 150, 225, 100):
        text(percent)
        need(until(lambda: abs((window('robot') or (0,) * 5)[3] - 88 * percent / 100) <= 1 or percent > 150, 10), f'{percent}: {window("robot")}')
        time.sleep(4)
        box()
        wide.append((percent, right('robot', wrong), right('box', wrong)))
        png(f'changed-to-{percent}')
        robot()
        need(until(lambda: not window('box'), 8), 'closed')
    need(not wrong, '; '.join(wrong))
    return wide


def token(pid):
    """How Windows trusts a program: its level (8192 as the person, 12288 as an administrator), and whether it has another token."""
    kernel, advapi = ctypes.WinDLL('kernel32'), ctypes.WinDLL('advapi32')
    kernel.OpenProcess.restype = w.HANDLE
    process, handle, size = kernel.OpenProcess(0x1000, False, pid), w.HANDLE(), w.DWORD()
    if not advapi.OpenProcessToken(w.HANDLE(process), 8, ctypes.byref(handle)):
        return None
    kind, level = w.DWORD(), ctypes.create_string_buffer(64)
    advapi.GetTokenInformation(handle, 18, ctypes.byref(kind), 4, ctypes.byref(size))
    advapi.GetTokenInformation(handle, 25, level, 64, ctypes.byref(size))
    return int.from_bytes(level.raw[size.value - 4:size.value], 'little'), kind.value


def pids(name):
    lines = subprocess.run(['tasklist', '/fi', f'imagename eq {name}', '/fo', 'csv', '/nh'], capture_output=True, text=True).stdout.splitlines()
    return [int(line.split(',')[1].strip('"')) for line in lines if line.lower().startswith(f'"{name.lower()}')]


def titled(pid, name):
    found = []

    def each(hwnd, _):
        its_ = w.DWORD()
        user.GetWindowThreadProcessId(hwnd, ctypes.byref(its_))
        if its_.value == pid and user.IsWindowVisible(hwnd) and windows_tools.title(hwnd) == name and not user.GetWindowLongW(hwnd, -20) & 8:
            found.append(hwnd)
        return True
    user.EnumWindows(windows_tools.EACH(each), 0)
    return found


@step('started as an administrator, it starts again by the desktop')
def _():
    app.kill()
    time.sleep(1)
    fresh()
    (pathlib.Path(os.environ['TEMP']) / 'the-machine-desktop-elevated').unlink(missing_ok=True)
    name = os.path.basename(program)
    env = dict(os.environ, MACHINE_SANDBOX_ELEVATED='1')
    first = subprocess.Popen([program], env=env)
    need(until(lambda: first.poll() is not None, 10), 'the first one ends')
    found = until(lambda: pids(name), 20)
    need(found and first.pid not in found, f'another is there: {found}')
    need(until(lambda: titled(found[-1], 'The Machine'), 30), 'with its window, as at any start')
    told = f'this {token(os.getpid())}, the desktop {[token(p) for p in pids("explorer.exe")]}, the new one {token(found[-1])}'
    subprocess.run([program, '--quit'], timeout=20)
    need(until(lambda: not pids(name), 20), 'it quits')
    second = subprocess.Popen([program], env=env)  # at once again: it doesn't go round
    need(until(lambda: titled(second.pid, 'The Machine'), 30), f'it goes on as it is: {second.poll()}')
    subprocess.run([program, '--quit'], env=env, timeout=20)
    need(until(lambda: not pids(name), 20), 'it quits too')
    return told


@step('back as it was')
def _():
    app.kill()
    text(100)
    scale(100)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PLACE, 0, winreg.KEY_SET_VALUE) as key:
        winreg.DeleteValue(key, 'TextScaleFactor')


finish()

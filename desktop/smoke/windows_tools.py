"""What windows.py and window.py share on Windows: the screen, the mouse and the keys, the app's windows and pages, and the steps."""
import base64
import ctypes
import json
import os
import pathlib
import shutil
import socket
import struct
import subprocess
import sys
import time
import traceback
import urllib.request
import winreg
import uuid
import zlib
from ctypes import wintypes as w

PORT, DEBUG, ID, BUBBLE = 8941, 9227, 'computer.themachine.desktop', 'bubble.html'
user, gdi = ctypes.WinDLL('user32', use_last_error=True), ctypes.WinDLL('gdi32')
user.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))  # physical pixels everywhere
for f, r in ((user.GetDC, w.HDC), (gdi.CreateCompatibleDC, w.HDC), (gdi.CreateCompatibleBitmap, w.HBITMAP), (user.GetForegroundWindow, w.HWND), (user.FindWindowW, w.HWND)):
    f.restype = r
gdi.BitBlt.argtypes = [w.HDC, *[ctypes.c_int] * 4, w.HDC, ctypes.c_int, ctypes.c_int, w.DWORD]
gdi.SelectObject.argtypes = [w.HDC, w.HGDIOBJ]
gdi.DeleteObject.argtypes, gdi.DeleteDC.argtypes = [w.HGDIOBJ], [w.HDC]
gdi.CreateCompatibleBitmap.argtypes = [w.HDC, ctypes.c_int, ctypes.c_int]
gdi.CreateCompatibleDC.argtypes, user.ReleaseDC.argtypes = [w.HDC], [w.HWND, w.HDC]
gdi.GetDIBits.argtypes = [w.HDC, w.HBITMAP, w.UINT, w.UINT, ctypes.c_void_p, ctypes.c_void_p, w.UINT]
user.GetWindowLongW.argtypes, user.IsIconic.argtypes = [w.HWND, ctypes.c_int], [w.HWND]
for f in (user.GetWindowRect, user.ClientToScreen, user.IsWindowVisible, user.GetDpiForWindow):
    f.argtypes = [w.HWND] + ([ctypes.c_void_p] if f in (user.GetWindowRect, user.ClientToScreen) else [])
user.SendMessageTimeoutW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM, w.UINT, w.UINT, ctypes.c_void_p]
EACH = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
SM = user.GetSystemMetrics

out = pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
CERTIFICATE = pathlib.Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
results = []
STATE = (out / 'state.txt').resolve()  # what the app takes for Windows' word on notifications
STATE.write_text('5')
MAIL = (out / 'mail.txt').resolve()  # where the app leaves an address for the mail app
SNIP = (out / 'snip.cmd').resolve()  # what the app takes for Windows' own snip, while it is there


# The screen, the mouse and the keys

def png(name):
    time.sleep(0.4)
    x, y, wide, high = SM(76), SM(77), SM(78), SM(79)  # all monitors
    screen = user.GetDC(None)
    memory = gdi.CreateCompatibleDC(screen)
    bitmap = gdi.CreateCompatibleBitmap(screen, wide, high)
    gdi.SelectObject(memory, bitmap)
    gdi.BitBlt(memory, 0, 0, wide, high, screen, x, y, 0x40CC0020)  # SRCCOPY | CAPTUREBLT
    header = ctypes.create_string_buffer(struct.pack('<IiiHHIIiiII', 40, wide, -high, 1, 32, 0, 0, 0, 0, 0, 0), 44)
    raw = ctypes.create_string_buffer(wide * high * 4)
    gdi.GetDIBits(memory, bitmap, 0, high, raw, header, 0)
    gdi.DeleteDC(memory)
    gdi.DeleteObject(bitmap)
    user.ReleaseDC(None, screen)
    px = bytearray(raw.raw)
    rgb = bytearray(wide * high * 3)
    rgb[0::3], rgb[1::3], rgb[2::3] = px[2::4], px[1::4], px[0::4]
    rows = b''.join(b'\0' + rgb[i * wide * 3:(i + 1) * wide * 3] for i in range(high))
    part = lambda kind, data: struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    (out / f'{name}.png').write_bytes(b'\x89PNG\r\n\x1a\n' + part(b'IHDR', struct.pack('>IIBBBBB', wide, high, 8, 2, 0, 0, 0))
                                     + part(b'IDAT', zlib.compress(bytes(rows), 6)) + part(b'IEND', b''))


class Mouse(ctypes.Structure):
    _fields_ = [('dx', w.LONG), ('dy', w.LONG), ('data', w.DWORD), ('flags', w.DWORD), ('time', w.DWORD), ('extra', ctypes.c_size_t)]


class Key(ctypes.Structure):
    _fields_ = [('vk', w.WORD), ('scan', w.WORD), ('flags', w.DWORD), ('time', w.DWORD), ('extra', ctypes.c_size_t)]


class Either(ctypes.Union):
    _fields_ = [('mouse', Mouse), ('key', Key)]


class Input(ctypes.Structure):
    _fields_ = [('type', w.DWORD), ('is_', Either)]


def send(one):
    if user.SendInput(1, ctypes.byref(one), ctypes.sizeof(Input)) != 1:
        raise OSError(f'SendInput: {ctypes.get_last_error()}')


def mouse(flags, x=0, y=0):
    send(Input(0, Either(mouse=Mouse(x, y, 0, flags, 0, 0))))


def move(x, y):
    left, top, wide, high = SM(76), SM(77), SM(78), SM(79)
    mouse(0xC001, round((x - left) * 65535 / (wide - 1)), round((y - top) * 65535 / (high - 1)))
    time.sleep(0.03)


def click(x, y, right=False):
    move(x - 3, y)
    move(x, y)
    time.sleep(0.15)
    mouse(8 if right else 2)
    time.sleep(0.06)
    mouse(16 if right else 4)
    time.sleep(0.5)


def drag(a, b, steps=25):
    move(*a)
    time.sleep(0.2)
    mouse(2)
    for i in range(1, steps + 1):
        move(a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps)
    time.sleep(0.3)
    mouse(4)
    time.sleep(0.6)


def key(vk, up=None):
    for flag in (0, 2) if up is None else (2,) if up else (0,):
        send(Input(1, Either(key=Key(vk, 0, flag, 0, 0))))
    time.sleep(0.05)


def alt_f4():
    key(0x12, False)
    key(0x73)
    key(0x12, True)


def write(text):
    for c in text:
        for flag in (4, 6):
            send(Input(1, Either(key=Key(0, ord(c), flag, 0, 0))))
        time.sleep(0.01)
    time.sleep(0.2)


ENTER, ESCAPE = 0x0D, 0x1B


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


class App:
    last = None

    def __init__(self, program, *args, debug=True, over=None, window=False, account=None):
        if App.last and App.last.poll() is None:  # a step before this one failed
            App.last.kill()
            App.last.wait()
        env = dict(os.environ, MACHINE_SANDBOX_ACCOUNT=account or f'http://127.0.0.1:{PORT}', MACHINE_SANDBOX_SNIP=str(SNIP), MACHINE_SANDBOX_STATE=str(STATE), MACHINE_SANDBOX_MAIL=str(MAIL),
                   MACHINE_SANDBOX_WINDOW=str(int(window)))
        if over:
            env.update(MACHINE_SANDBOX_ACCOUNT=over.at, MACHINE_SANDBOX_ROOT=str(CERTIFICATE / 'root.pem'))
        if debug:
            env['MACHINE_SANDBOX_DEBUG'] = str(DEBUG)
        self.env, self.program = env, program
        self.process = App.last = subprocess.Popen([program, *args], env=env)
        App.last_app = self

    def again(self, *args, seconds=15):
        return subprocess.run([self.program, *args], env=self.env, timeout=seconds).returncode

    def all(self, topmost):
        """Its windows, the front one first: what stays on top (the robot, its box), or those like any program's."""
        found = []

        def each(hwnd, _):
            pid, rect = w.DWORD(), w.RECT()
            user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value == self.process.pid and user.IsWindowVisible(hwnd) and not user.IsIconic(hwnd):
                user.GetWindowRect(hwnd, ctypes.byref(rect))
                if rect.right - rect.left > 40 and bool(user.GetWindowLongW(hwnd, -20) & 8) == topmost:
                    found.append((hwnd, rect))
            return True
        user.EnumWindows(EACH(each), 0)
        return found

    def windows(self):
        return self.all(True)

    def plain(self):
        return self.all(False)

    def titled(self, name):
        return next((x for x in self.plain() if title(x[0]) == name), None)

    def window(self):
        self.its = getattr(self, 'its', None) or next((h for h, _ in self.plain() if title(h) == 'The Machine'), None)
        return next((x for x in self.plain() if x[0] == self.its), None)

    def settings(self):
        return self.titled('Settings')

    def robot(self):
        return next((x for x in self.windows() if x[1].right - x[1].left < 250), None)

    def wide(self):
        return [x for x in self.windows() if x[1].right - x[1].left >= 250]

    def sized(self, least, most):
        return next((x for x in self.wide() if least <= (x[1].right - x[1].left) * 96 / user.GetDpiForWindow(x[0]) < most), None)

    def box(self):
        return self.sized(350, 999)

    def card(self):
        """A to-do open in the box."""
        return self.sized(333, 350)

    def bubble(self):
        return self.sized(250, 333)

    def center(self):
        r = need_window(self.robot())[1]
        return (r.left + r.right) // 2, (r.top + r.bottom) // 2

    def answers(self):
        """Whether its main thread takes messages."""
        windows = self.windows()
        return bool(windows) and all(user.SendMessageTimeoutW(h, 0, 0, 0, 0, 3000, None) for h, _ in windows)

    def ended(self, seconds=8):
        return until(lambda: self.process.poll() is not None, seconds)


def title(hwnd):
    text = ctypes.create_unicode_buffer(200)
    user.GetWindowTextW(w.HWND(hwnd), text, 200)
    return text.value


def need_window(found):
    need(found, 'the window is there')
    return found


def page(name, script, wait=10):
    """What a page says about itself: only read, never clicked this way. The page: what its address has in it, or a test of it."""
    pages = json.load(urllib.request.urlopen(f'http://127.0.0.1:{DEBUG}/json', timeout=5))
    address = next(p['webSocketDebuggerUrl'] for p in pages if (name(p['url']) if callable(name) else name in p['url']))
    host, path = address.removeprefix('ws://').split('/', 1)
    host, port = host.split(':')
    with socket.create_connection((host, int(port)), wait) as s:
        s.sendall(f'GET /{path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                  f'Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
        f = s.makefile('rb')
        while f.readline().strip():
            pass
        body = json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}).encode()
        mask = os.urandom(4)
        s.sendall(struct.pack('>BBH', 0x81, 0x80 | 126, len(body)) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(body)))
        while True:
            _, n = f.read(2)
            n = struct.unpack('>H', f.read(2))[0] if n == 126 else struct.unpack('>Q', f.read(8))[0] if n == 127 else n
            told = json.loads(f.read(n))
            if told.get('id') == 1:
                return told['result']['result'].get('value')


def says(selector, name='box.html'):
    shown = page(name, f'(e => e && e.getClientRects().length ? e.innerText : "")(document.querySelector({json.dumps(selector)}))')
    return (shown or '').strip()


def press(app, selector, name='box.html'):
    """A real click on something in the box, or in the to-do open in it, where its page says it is."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); '
                          'return [e.x + e.width / 2, e.y + e.height / 2].map(v => v * devicePixelRatio) })()')
    point = w.POINT(0, 0)
    user.ClientToScreen(need_window(app.box() if name == 'box.html' else app.bubble() if name == BUBBLE else app.card())[0], ctypes.byref(point))
    click(round(point.x + at[0]), round(point.y + at[1]))


def work_area():
    r = w.RECT()
    user.SystemParametersInfoW(0x30, 0, ctypes.byref(r), 0)
    return r


def in_corner(app):
    """In the bottom right corner of the work area, where it starts: 16 and 12 from its edges."""
    hwnd, r = need_window(app.robot())
    area, scale = work_area(), user.GetDpiForWindow(hwnd) / 96
    told = (f'robot {r.left},{r.top} {r.right - r.left}x{r.bottom - r.top}, work area {area.left},{area.top} to '
            f'{area.right},{area.bottom}, scale {scale}')
    return abs(area.right - r.right - 16 * scale) <= 2 and abs(area.bottom - r.bottom - 12 * scale) <= 2 and abs(r.right - r.left - 88 * scale) <= 2, told


def step(name):
    def run(f):
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
    return run


def line(name, ok, told):
    told = str(told)
    return f"{'FAIL' if not ok else 'skip' if told.startswith('NOT TESTED') else 'ok  '} {name}  {told}"


def fresh():
    for base in ('APPDATA', 'LOCALAPPDATA'):
        for _ in range(10):  # the page cache is let go of a moment after the app
            shutil.rmtree(pathlib.Path(os.environ[base], ID), ignore_errors=True)
            if not pathlib.Path(os.environ[base], ID).exists():
                break
            time.sleep(0.5)


def scheme():
    try:
        winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Classes\computer.themachine.app').Close()
        return True
    except FileNotFoundError:
        return False


def saved():
    return json.loads(pathlib.Path(os.environ['APPDATA'], ID, 'app.json').read_text())


def reasons():
    return pathlib.Path(os.environ['APPDATA'], ID, 'speaks.log').read_text()


class Id(ctypes.Structure):
    _fields_ = [('size', w.DWORD), ('hwnd', w.HWND), ('id', w.UINT), ('guid', ctypes.c_byte * 16)]


def tray(app):
    """Where its icon is: behind the taskbar's arrow, opened first, unless the person moved it out."""
    at, rect = [], w.RECT()

    def each(hwnd, _):
        pid, name = w.DWORD(), ctypes.create_unicode_buffer(64)
        user.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        user.GetClassNameW(hwnd, name, 64)
        if pid.value == app.process.pid and name.value.startswith('tray_icon'):
            at.append(hwnd)
        return True
    user.EnumWindows(EACH(each), 0)
    need(at, 'it has one')

    def where():
        found = any(not ctypes.windll.shell32.Shell_NotifyIconGetRect(ctypes.byref(Id(ctypes.sizeof(Id), at[0], n)), ctypes.byref(rect)) for n in range(1, 6))
        need(found, 'Windows shows it')
        return (rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2
    here = where()
    if here[1] < work_area().bottom:
        return here
    for _ in range(3):
        click(*here)
        if until(lambda: where()[1] < work_area().bottom, 3):
            time.sleep(0.5)
            return where()
    return here


class Mode(ctypes.Structure):
    _fields_ = [('name', w.WCHAR * 32), ('v', w.WORD * 2), ('size', w.WORD), ('extra', w.WORD), ('fields', w.DWORD), ('x', w.LONG),
                ('y', w.LONG), ('o', w.DWORD * 2), ('s', ctypes.c_short * 5), ('form', w.WCHAR * 32), ('px', w.WORD), ('bits', w.DWORD),
                ('width', w.DWORD), ('height', w.DWORD), ('rest', w.DWORD * 10)]


def resolution(wide, high):
    mode = Mode(size=ctypes.sizeof(Mode), fields=0x180000, width=wide, height=high)
    if user.ChangeDisplaySettingsW(ctypes.byref(mode), 0):
        return False
    time.sleep(2)
    return (SM(0), SM(1)) == (wide, high)


def scale(percent):
    """Settings > Display > Scale, by the call Settings uses. False: this computer's screen doesn't offer it."""
    paths, modes = w.UINT(), w.UINT()
    user.GetDisplayConfigBufferSizes(2, ctypes.byref(paths), ctypes.byref(modes))
    path, mode = ctypes.create_string_buffer(72 * paths.value), ctypes.create_string_buffer(64 * modes.value)
    user.QueryDisplayConfig(2, ctypes.byref(paths), path, ctypes.byref(modes), mode, None)
    source = path.raw[:12]  # adapter, id
    get = ctypes.create_string_buffer(struct.pack('<iI', -3, 32) + source + bytes(12), 32)
    if user.DisplayConfigGetDeviceInfo(get):
        return False
    least, _, most = struct.unpack('<iii', get.raw[20:32])
    steps = [100, 125, 150, 175, 200, 225, 250, 300]
    wanted = least + steps.index(percent)  # its steps count from the recommended one
    if wanted > most:
        return False
    if user.DisplayConfigSetDeviceInfo(ctypes.create_string_buffer(struct.pack('<iI', -4, 24) + source + struct.pack('<i', wanted), 24)):
        return False
    time.sleep(3)
    return True


def in_front():
    """The window in front: its title, its program."""
    hwnd, title, pid = user.GetForegroundWindow(), ctypes.create_unicode_buffer(200), w.DWORD()
    user.GetWindowTextW(w.HWND(hwnd), title, 200)
    user.GetWindowThreadProcessId(w.HWND(hwnd), ctypes.byref(pid))
    line = subprocess.run(['tasklist', '/fi', f'pid eq {pid.value}', '/fo', 'csv', '/nh'], capture_output=True, text=True).stdout
    return title.value, line.split(',')[0].strip('"').lower()


def to_front(hwnd):
    key(0x12)  # Windows lets a program do this after a key
    user.ShowWindow(w.HWND(hwnd), 9)
    user.SetForegroundWindow(w.HWND(hwnd))
    return until(lambda: user.GetForegroundWindow() == hwnd, 5)


def browsers_closed():
    for name in ('msedge.exe', 'chrome.exe'):
        subprocess.run(['taskkill', '/f', '/t', '/im', name], capture_output=True)
    time.sleep(1)


# A window to drag from, as Explorer, a browser and an editor put it
SOURCE = r"""
Add-Type -A System.Windows.Forms,System.Drawing
$f = New-Object Windows.Forms.Form -Property @{Text='source'; StartPosition='Manual'; Left=40; Top=40; Width=400; Height=160; TopMost=$true}
$files = New-Object Collections.Specialized.StringCollection
$args[0].Split('|') | % { [void]$files.Add($_) }
$file = New-Object Windows.Forms.DataObject; $file.SetFileDropList($files)
$text = New-Object Windows.Forms.DataObject; $text.SetText('Ask Dana <b>about</b> the pilot')
$link = New-Object Windows.Forms.DataObject; $link.SetText('https://example.com/pilot?x=1')
$link.SetData('UniformResourceLocatorW', (New-Object IO.MemoryStream (,[Text.Encoding]::Unicode.GetBytes("https://example.com/pilot?x=1`0"))))
$i = 0
foreach ($d in $file, $text, $link) {
  $l = New-Object Windows.Forms.Label -Property @{Left=130*$i; Top=0; Width=125; Height=110; BackColor='LightGray'; Text="$i"; Tag=$d}
  $l.add_MouseDown({ [void]$this.DoDragDrop($this.Tag, 'Copy') }); $f.Controls.Add($l); $i++
}
$t = New-Object Windows.Forms.Timer -Property @{Interval=300}; $where = $args[1]
$t.add_Tick({ $o = $f.PointToScreen([Drawing.Point]::Empty); [IO.File]::WriteAllText($where, "$($o.X) $($o.Y)") }); $t.Start()
[Windows.Forms.Application]::Run($f)
"""


def finish(end=''):
    failed = [r for r in results if not r[1]]
    lines = [line(*r) for r in results]
    skipped = sum(x.startswith('skip') for x in lines)
    lines.append(f'{end}{len(results) - len(failed) - skipped} ok, {len(failed)} failed, {skipped} skipped')
    (out / 'results.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(lines[-1])
    sys.exit(bool(failed))


sandbox, people = (str(pathlib.Path(p).resolve()) for p in sys.argv[1:3])

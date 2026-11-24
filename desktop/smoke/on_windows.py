"""What window.py needs of Windows."""
import contextlib
import ctypes
import json
import os
import pathlib
import subprocess
import sys
import time
import winreg
from ctypes import wintypes as w

import windows_tools
from windows_tools import (  # noqa: F401 (window.py's)
    ENTER, ESCAPE, ID, MAIL, PORT, SM, SOURCE, browsers_closed, click, drag, finish, fresh, in_front, key, need, out, png, resolution, sandbox, saved, step, title,
    to_front, tray, until, user, work_area, write,
)

SYSTEM, VERSION = 'windows', 'Windows ' + '.'.join(map(str, sys.getwindowsversion()[:3]))
DOWNLOADS = pathlib.Path.home() / 'Downloads'
KEYS = {'close': 'W', 'find': 'F', 'reload': 'R', 'save': 'S', 'all': 'A', 'copy': 'C', 'paste': 'V', 'undo': 'Z', 'zoom none': '0', 'zoom in': 0xBB, 'zoom out': 0xBD, 'settings': 0xBC}
resolution(1920, 1080)


class Rect:
    def __init__(self, found):
        self.hwnd, r = found
        self.left, self.top, self.right, self.bottom = r.left, r.top, r.right, r.bottom
        self.width, self.height = r.right - r.left, r.bottom - r.top

    def __repr__(self):
        return f'{self.left},{self.top} {self.width}x{self.height}'


def rect(found):
    return found and Rect(found)


class App(windows_tools.App):
    def __init__(self, program, window=True, account=None):
        super().__init__(program, *([] if window else ['--login']), window=True, account=account)

    def plain(self):
        return [Rect(x) for x in self.all(False)]

    def window(self):
        self.its = getattr(self, 'its', None) or next((r.hwnd for r in self.plain() if title(r.hwnd) == 'The Machine'), None)
        return next((r for r in self.plain() if r.hwnd == self.its), None)

    def settings(self):
        return next((r for r in self.plain() if title(r.hwnd) == 'Settings'), None)

    def robot(self):
        return rect(super().robot())

    def box(self):
        return rect(super().box())

    def card(self):
        return rect(super().card())

    def center(self):
        r = self.robot()
        need(r, 'the robot is there')
        return (r.left + r.right) // 2, (r.top + r.bottom) // 2

    def raw(self):
        return [(title(h), r.left, r.top, r.right, r.bottom) for h, r in self.windows()]

    def pids(self):
        return [self.process.pid] if self.process.poll() is None else []

    def kill(self):
        if self.process.poll() is None:
            self.process.kill()

    def answers(self, name='robot'):
        try:
            return page(name, '1') == 1
        except (OSError, ValueError, StopIteration, KeyError):
            return False


def which(name):
    if name == 'app':
        own = ('http://tauri.localhost/app.html', f'http://127.0.0.1:{PORT}/', f'http://127.0.0.1:{PORT + 1}/', 'http://127.0.0.1:8970/')
        return lambda url: url.startswith(own) and 'compact=1' not in url and '/api/' not in url
    part = {'card': 'compact=1'}.get(name, f'/{name}.html')
    return lambda url: part in url


def page(name, script, wait=10):
    try:
        return windows_tools.page(which(name), script, wait)
    except StopIteration:
        return None  # it isn't there yet


def says(selector, name='box'):
    shown = page(name, f'(e => e && e.getClientRects().length ? e.innerText : "")(document.querySelector({json.dumps(selector)}))')
    return (shown or '').strip()


def here(app, selector, name='app'):
    """Where something in a window is on the screen: its page may be zoomed, under the title bar."""
    at = page(name, f'(() => {{ const e = document.querySelector({json.dumps(selector)}).getBoundingClientRect(); return [e.x + e.width / 2, e.y + e.height / 2].map(v => v * devicePixelRatio) }})()')
    r = {'app': app.window, 'settings': app.settings, 'box': app.box, 'card': app.card}[name]()
    need(r, f'the window is there: {name}')
    point = w.POINT(0, 0)
    user.ClientToScreen(r.hwnd, ctypes.byref(point))
    return round(point.x + at[0]), round(point.y + at[1])


def press(app, selector, name='box'):
    was, at = None, here(app, selector, name)
    for _ in range(20):  # it may still be getting as tall as what is in it
        if at == was:
            break
        time.sleep(0.2)
        was, at = at, here(app, selector, name)
    click(*at)


def hit(name):
    if name == 'full':
        return key(0x7A)
    held = 0x12 if name == 'back' else 0x11
    code = 0x25 if name == 'back' else KEYS[name]
    key(held, False), key(ord(code) if isinstance(code, str) else code), key(held, True)


def ours():
    return in_front()[1] == os.path.basename(sandbox).lower()


def other():
    """Another program in front, with the keys."""
    there = lambda: user.FindWindowW('Notepad', None)
    if not there():
        subprocess.Popen(['notepad.exe'])
    need(until(there, 10), 'another program')
    time.sleep(0.5)
    need(to_front(there()), f'it is in front: {in_front()}')
    time.sleep(1)
    return in_front()


def reopen(app):
    """As a person starts it again."""
    app.again()


def back_to_it(app):
    app.again()
    need(until(ours, 10), f'in front: {in_front()}')
    time.sleep(1)


def minimize(app):
    user.ShowWindow(w.HWND(app.window().hwnd), 6)


def quit_it(app):
    app.again('--quit')


def like_any_app(app):
    style = user.GetWindowLongW(w.HWND(app.window().hwnd), -20)
    need(not style & 0x88, f'in the taskbar, and not on top: {style:x}')


def whole():
    return 0, 0, SM(0), SM(1)


def link(app, address):
    os.startfile(address)  # as the browser does: by the registered scheme


def second(app, look):
    print('no second screen here', flush=True)


def nothing_left():
    need(not known_there(), f'its name for notifications: {known_there()}')
    need(not kept(), f'its notifications: {kept()}')


no_browser = browsers_closed


def dialog(app):
    """The page waits for an answer."""
    try:
        page('app', '1', 1.5)
        return False
    except OSError:
        return True


def clipboard(text=None):
    if text is not None:
        return subprocess.run(['clip'], input=text, text=True)
    return subprocess.run(['powershell', '-noprofile', '-command', 'Get-Clipboard'], capture_output=True, text=True).stdout.strip()


def place(app, x, y, wide, high):
    user.SetWindowPos(w.HWND(app.window().hwnd), None, round(x), round(y), round(wide), round(high), 0x14)


def dark(on):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize') as k:
        for name in ('AppsUseLightTheme', 'SystemUsesLightTheme'):
            winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, int(not on))
    user.SendMessageTimeoutW(0xFFFF, 0x1A, 0, ctypes.cast(ctypes.c_wchar_p('ImmersiveColorSet'), ctypes.c_void_p).value, 2, 2000, None)


def area():
    r = work_area()
    return r.left, r.top, r.right, r.bottom


def marked(file):
    try:
        with open(f'{file}:Zone.Identifier') as f:
            return 'ZoneId=3' in f.read()
    except OSError:
        return False


def names(app):
    return ', '.join(title(r.hwnd) for r in app.plain())


@contextlib.contextmanager
def drop_from(app, *files):
    place(app, 500, 80, 1100, 760)
    time.sleep(1)
    script, where = out / 'source.ps1', (out / 'source.txt').resolve()
    script.write_text(SOURCE, encoding='utf-8')
    where.unlink(missing_ok=True)
    source = subprocess.Popen(['powershell', '-sta', '-noprofile', '-executionpolicy', 'bypass', '-file', str(script.resolve()), '|'.join(map(str, files)), str(where)])
    try:
        need(until(lambda: where.exists() and where.read_text().strip(), 30), 'a window to drag from')
        x, y = map(int, where.read_text().split())
        yield x + 60, y + 60
    finally:
        source.kill()
        script.unlink()
        time.sleep(0.5)
        where.unlink(missing_ok=True)


def choose(file):
    time.sleep(3)  # typed, it loses some while it still fills its list
    clipboard(str(file))
    hit('all')
    hit('paste')
    time.sleep(0.5)
    key(ENTER)


def settings_open(app):
    hit('settings')


def icon_there():
    tray(windows_tools.App.last_app)
    return True


def pages_killed():
    killed = subprocess.run(['powershell', '-noprofile', '-command', "Get-CimInstance Win32_Process -Filter \"Name='msedgewebview2.exe'\" | ? { $_.CommandLine -match '--type=renderer' } | % { Stop-Process -Id $_.ProcessId -Force; $_.ProcessId }"],
                            capture_output=True, text=True).stdout.split()
    need(killed, 'its process')


def crashes():
    folder = pathlib.Path(os.environ['LOCALAPPDATA'], 'CrashDumps')
    return [p.name for p in folder.glob(os.path.basename(sandbox) + '*')] if folder.exists() else []


def kept():
    """The notifications Windows keeps of it."""
    script = ('$null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime];'
              f"[Windows.UI.Notifications.ToastNotificationManager]::History.GetHistory('{ID}') | % {{ $_.Tag }}")
    return subprocess.run(['powershell', '-noprofile', '-command', script], capture_output=True, text=True).stdout.split()


def known_there():
    """Whether Windows knows the app's notifications by name."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Classes\\AppUserModelId\\' + ID) as k:
            return winreg.QueryValueEx(k, 'DisplayName')[0]
    except OSError:
        return None


def center():
    """Opens or closes where Windows keeps the notifications."""
    key(0x5B, False)
    key(ord('N'))
    key(0x5B, True)
    time.sleep(2)


def on_screen(text):
    """Where a notification with these words is."""
    script = ('Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes; $A = [Windows.Automation.AutomationElement];'
              "$is = New-Object Windows.Automation.PropertyCondition($A::ClassNameProperty, 'Windows.UI.Core.CoreWindow');"
              "foreach ($w in $A::RootElement.FindAll('Children', $is)) { foreach ($e in $w.FindAll('Descendants', [Windows.Automation.Condition]::TrueCondition)) {"
              f"if ($e.Current.Name -like '*{text}*' -and $e.Current.BoundingRectangle.Width -gt 0) {{"
              "$r = $e.Current.BoundingRectangle; \"$([int]($r.X + $r.Width / 2)) $([int]($r.Y + $r.Height / 2))\"; exit } } }")
    found = subprocess.run(['powershell', '-noprofile', '-command', script], capture_output=True, text=True).stdout.split()
    return tuple(map(int, found)) if len(found) == 2 else None

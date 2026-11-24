"""A newer version in place of the one that runs, and on Windows its installer: for throwaway computers only.

  updates.py <the app; on Windows its installer> <the newer one to fetch, its .sig beside it> <folder for the pictures>

Both are sandbox builds, signed with the made-up key whose other half is MACHINE_SANDBOX_UPDATES_KEY. See desktop.yml."""
import http.server
import importlib
import json
import os
import pathlib
import platform
import plistlib
import shutil
import subprocess
import sys
import threading
import time

from standin import Machine

on = importlib.import_module({'darwin': 'on_mac', 'win32': 'on_windows'}[sys.platform])
App, SYSTEM, PORT, need, out, page, png, press, step, until = on.App, on.SYSTEM, on.PORT, on.need, on.out, on.page, on.png, on.press, on.step, on.until
newer = pathlib.Path(sys.argv[2]).resolve()
NEW = '9.9.9'
WINDOWS = SYSTEM == 'windows'
on.fresh()
machine = Machine(PORT)
machine.window = machine.compact = True
spoiled = False
asked = []


class Updates(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        asked.append((self.path, dict(self.headers)))
        body = newer.read_bytes()
        if self.path == '/latest.json':
            chip = {'arm64': 'aarch64', 'AMD64': 'x86_64'}.get(platform.machine(), platform.machine())
            of = {'signature': newer.with_name(newer.name + '.sig').read_text(), 'url': f'http://127.0.0.1:{served.server_port}/newer'}
            body = json.dumps({'version': NEW, 'platforms': {f'{"windows" if WINDOWS else "darwin"}-{chip}': of}}).encode()
        elif spoiled:
            body = body[:-1] + bytes([body[-1] ^ 1])
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass


served = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Updates)
threading.Thread(target=served.serve_forever, daemon=True).start()
os.environ['MACHINE_SANDBOX_UPDATES'] = f'http://127.0.0.1:{served.server_port}/latest.json'
KEYS = {k: os.environ[k] for k in ('MACHINE_SANDBOX_UPDATES', 'MACHINE_SANDBOX_UPDATES_KEY')}

if WINDOWS:
    import winreg
    HOME = pathlib.Path(os.environ['LOCALAPPDATA'], 'The Machine')
    program = HOME / 'the-machine-desktop.exe'
    UNINSTALL = r'Software\Microsoft\Windows\CurrentVersion\Uninstall'

    def keys(path):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                return {winreg.EnumKey(key, i) for i in range(winreg.QueryInfoKey(key)[0])}
        except OSError:
            return set()

    def values(path):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                return {(v := winreg.EnumValue(key, i))[0]: v[1] for i in range(winreg.QueryInfoKey(key)[1])}
        except OSError:
            return {}

    def left():
        """What of it there is on this computer."""
        ours = lambda name: any(x in name.lower() for x in ('the machine', 'the-machine', 'themachine', 'salesflare'))
        at = {'Classes': keys(r'Software\Classes'), 'AppUserModelId': keys(r'Software\Classes\AppUserModelId'), 'Uninstall': keys(UNINSTALL), 'Software': keys('Software'),
              'Run': set(values(r'Software\Microsoft\Windows\CurrentVersion\Run'))}
        found = {f'{place}: {name}' for place, names in at.items() for name in names if ours(name)}
        roots = [os.environ['LOCALAPPDATA'], os.environ['APPDATA'], os.path.join(os.environ['APPDATA'], r'Microsoft\Windows\Start Menu\Programs'), os.path.expanduser('~/Desktop')]
        return found | {str(p) for root in roots for p in pathlib.Path(root).glob('*') if ours(p.name)}

    def version():
        return values(UNINSTALL + r'\The Machine').get('DisplayVersion')

    def setup(which, *args):
        done = subprocess.run([which, '/S', *args], timeout=300)
        need(done.returncode == 0, f'{which} {done.returncode}')

    def running():
        told = subprocess.run(['powershell', '-NoProfile', '-Command', f"(Get-Process the-machine-desktop -ErrorAction SilentlyContinue | Where-Object Path -eq '{program}').Id"], capture_output=True, text=True).stdout
        return [int(x) for x in told.split()]

    def start():
        return App(str(program))
else:
    HOME = out.parent / 'applications' / 'The Machine.app'
    program = HOME

    def version():
        return plistlib.loads((HOME / 'Contents/Info.plist').read_bytes())['CFBundleShortVersionString']

    def running():
        return app.pids()

    def start():
        return App(str(program), window=True, more=KEYS)

before = left() if WINDOWS else None


@step('it is installed')
def _():
    if not WINDOWS:
        shutil.rmtree(HOME.parent, ignore_errors=True)
        HOME.parent.mkdir()
        subprocess.run(['ditto', on.sandbox, str(HOME)], check=True)
        return version()
    need(not before, before)
    setup(on.sandbox)
    need(program.exists(), 'in the person\'s own folder')
    need(version() == '0.0.1', version())
    said = values(UNINSTALL + r'\The Machine')
    need(not running(), 'it starts when the person starts it')
    return f'{said.get("Publisher")}, {sorted(p.name for p in HOME.iterdir())}; {sorted(left())}'


def settings():
    app.settings() or on.settings_open(app)
    need(until(app.settings), 'its window')
    time.sleep(0.8)


def offered():
    return page('settings', '!document.querySelector("#update").hidden')


@step('one that was changed on the way is not used')
def _():
    global app, spoiled
    spoiled = True
    app = start()
    need(until(app.window, 60), 'it runs')
    need(until(lambda: any(p == '/newer' for p, _ in asked), 60), f'it is fetched {asked}')
    time.sleep(5)
    settings()
    need(not offered(), 'not offered')
    png('no-update')
    app.kill()
    spoiled = False
    told = [h for p, h in asked if p == '/latest.json'][0]
    need(not any('0.0.1' in v for v in told.values()), f'it says nothing of itself {told}')
    return str(told)


@step('a newer version')
def _():
    global app
    had = len(asked)
    app = start()
    need(until(app.window, 60), 'it runs')
    need(until(lambda: any(p == '/newer' for p, _ in asked[had:]), 60), 'it is fetched')
    time.sleep(3)
    settings()
    need(until(offered, 20), 'it is offered')
    png('an-update')
    was = running()
    need(page('settings', 'document.querySelector("#update-hint").innerText') == f'{NEW} is ready', 'says so')
    press(app, '#update', 'settings')
    need(until(lambda: version() == NEW, 90), f'it is in place: {version()}')
    need(until(lambda: running() and not set(running()) & set(was), 60), f'it runs again: {was} {running()}')
    time.sleep(6)
    png('updated')
    need(len(running()) == 1, running())
    return f'{was} {running()}'


@step('it goes, and leaves nothing')
def _():
    if not WINDOWS:
        app.kill()
        for pid in running():
            os.kill(pid, 9)
        return 'NOT TESTED: a Mac app is deleted by the person'
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run') as key:
        winreg.SetValueEx(key, 'The Machine', 0, winreg.REG_SZ, f'"{program}" --login')
    had = left()
    setup(str(HOME / 'uninstall.exe'))
    need(until(lambda: not left(), 60), f'left: {left()} of {had}')
    need(not running(), 'it runs no more')
    return f'{len(had)} places'


on.finish()

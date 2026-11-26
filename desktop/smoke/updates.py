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
App, SYSTEM, PORT, need, out, page, png, step, until = on.App, on.SYSTEM, on.PORT, on.need, on.out, on.page, on.png, on.step, on.until
newer = pathlib.Path(sys.argv[2]).resolve()
NEW = '9999.0.0'  # newer than a release's own version too (tools/version.py)
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

    def refused():
        return ''
else:
    HOME = out.parent / 'applications' / 'The Machine.app'
    program = HOME

    def version():
        return plistlib.loads((HOME / 'Contents/Info.plist').read_bytes())['CFBundleShortVersionString']

    def running():
        return app.pids()

    def start():
        return App(str(program), window=True, more=KEYS)

    def refused():
        return on.mac_tools.asks()

    def stop():
        need(until(lambda: not on.mac_tools.asks('Done'), 30), 'what macOS asks is answered')  # the one that waits for it ends, and nothing is in front of what is tried next
        app.kill()
        for pid in running():
            os.kill(pid, 9)

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
    told = {k.lower(): v for k, v in [h for p, h in asked if p == '/latest.json'][0].items()}
    need(set(told) == {'accept', 'user-agent', 'host'} and told['user-agent'].startswith('tauri-plugin-updater/'), f'it says nothing of itself {told}')
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
    on.click(*on.here(app, '#update', 'settings'))
    need(until(lambda: version() == NEW, 90), f'it is in place: {version()}')
    again = lambda: running() and not set(running()) & set(was)
    if not until(lambda: again() or refused(), 60) or not again():
        png('updated')
        told = refused()
        need(told, f'it runs again: {was} {running()}')
        stop()
        return f'NOT TESTED: that it starts again; macOS opens no new app that Apple did not notarize: {told}'
    time.sleep(6)
    png('updated')
    need(len(running()) == 1, running())
    return f'{was} {running()}'


@step('it goes, and leaves nothing')
def _():
    if not WINDOWS:
        stop()
        shutil.rmtree(HOME.parent)  # so that nothing after this opens it
        return 'NOT TESTED: a Mac app is deleted by the person'
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run') as key:
        winreg.SetValueEx(key, 'The Machine', 0, winreg.REG_SZ, f'"{program}" --login')
    had = left()
    kept = pathlib.Path(os.environ['APPDATA'], 'computer.themachine.desktop', 'app.json')
    kept.parent.mkdir(exist_ok=True)
    kept.write_text('{}')
    # As the installer does it, when the person has it take the older one away first
    subprocess.run(f'"{HOME}\\uninstall.exe" /S _?={HOME}', timeout=300)
    need(not program.exists() and kept.exists(), f'a newer one after it finds what was kept: {left()}')
    was = kept.read_text()  # the one that ran wrote its own when it quit
    setup(on.sandbox)
    need(program.exists(), 'installed again')
    need(kept.read_text() == was, f'what was kept is as it was: {kept.read_text()}')
    setup(str(HOME / 'uninstall.exe'))
    need(until(lambda: not left(), 60), f'left: {left()} of {had}')
    need(not running(), 'it runs no more')
    return f'{len(had)} places'


on.finish()
